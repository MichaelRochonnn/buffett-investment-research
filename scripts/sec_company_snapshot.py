#!/usr/bin/env python3
"""Fetch a simple SEC snapshot for a U.S.-listed company."""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


USER_AGENT = "buffett-investment-research/1.0 (contact: noreply@example.com)"
TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
COMPANYFACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
ANNUAL_FORMS = {"10-K", "10-K/A", "20-F", "20-F/A", "40-F", "40-F/A"}


@dataclass
class Match:
    title: str
    ticker: str
    cik: int


def fetch_json(url: str) -> Any:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json,text/plain,*/*",
            "Accept-Encoding": "identity",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def pick_match(query: str, tickers: list[dict[str, Any]]) -> Match | None:
    q_norm = normalize(query)
    q_upper = query.upper().strip()

    for item in tickers:
        if item["ticker"].upper() == q_upper:
            return Match(item["title"], item["ticker"], int(item["cik_str"]))

    for item in tickers:
        if normalize(item["title"]) == q_norm:
            return Match(item["title"], item["ticker"], int(item["cik_str"]))

    partials = []
    for item in tickers:
        title_norm = normalize(item["title"])
        ticker_norm = normalize(item["ticker"])
        if q_norm and (q_norm in title_norm or q_norm in ticker_norm):
            partials.append(item)
    if partials:
        partials.sort(key=lambda item: (len(item["title"]), item["title"]))
        item = partials[0]
        return Match(item["title"], item["ticker"], int(item["cik_str"]))

    names = [item["title"] for item in tickers] + [item["ticker"] for item in tickers]
    close = difflib.get_close_matches(query, names, n=1, cutoff=0.75)
    if not close:
        return None
    target = close[0]
    for item in tickers:
        if item["title"] == target or item["ticker"] == target:
            return Match(item["title"], item["ticker"], int(item["cik_str"]))
    return None


def recent_filings(submissions: dict[str, Any], forms: list[str]) -> list[dict[str, str]]:
    recent = submissions.get("filings", {}).get("recent", {})
    if not recent:
        return []

    rows = []
    forms_set = set(forms)
    count = len(recent.get("form", []))
    for idx in range(count):
        form = recent["form"][idx]
        if form not in forms_set:
            continue
        accession = recent["accessionNumber"][idx]
        accession_nodash = accession.replace("-", "")
        primary = recent["primaryDocument"][idx]
        filing_date = recent["filingDate"][idx]
        cik = str(submissions["cik"]).zfill(10)
        url = (
            f"https://www.sec.gov/Archives/edgar/data/"
            f"{int(cik)}/{accession_nodash}/{primary}"
        )
        rows.append(
            {
                "form": form,
                "filing_date": filing_date,
                "accession": accession,
                "url": url,
            }
        )
    return rows


def choose_fact(facts: dict[str, Any], tags: list[str], unit: str) -> dict[str, Any] | None:
    gaap = facts.get("facts", {}).get("us-gaap", {})
    candidates: list[dict[str, Any]] = []
    for tag in tags:
        entry = gaap.get(tag)
        if not entry:
            continue
        units = entry.get("units", {})
        for item in units.get(unit, []):
            if item.get("form") not in ANNUAL_FORMS:
                continue
            if "fy" not in item or "val" not in item:
                continue
            candidate = dict(item)
            candidate["tag"] = tag
            candidates.append(candidate)
    if not candidates:
        return None
    candidates.sort(
        key=lambda item: (
            int(item.get("fy", 0)),
            item.get("filed", ""),
            item.get("frame", ""),
        ),
        reverse=True,
    )
    return candidates[0]


def fmt_money(value: float | int | None) -> str:
    if value is None:
        return "n/a"
    sign = "-" if value < 0 else ""
    value = abs(float(value))
    if value >= 1_000_000_000:
        return f"{sign}${value / 1_000_000_000:.2f}B"
    if value >= 1_000_000:
        return f"{sign}${value / 1_000_000:.2f}M"
    return f"{sign}${value:,.0f}"


def fmt_shares(value: float | int | None) -> str:
    if value is None:
        return "n/a"
    value = float(value)
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    return f"{value:,.0f}"


def build_summary(match: Match, submissions: dict[str, Any], facts: dict[str, Any]) -> dict[str, Any]:
    cik10 = str(match.cik).zfill(10)
    filings_page = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={match.ticker}"
    companyfacts_page = COMPANYFACTS_URL.format(cik=cik10)

    latest_10k = recent_filings(submissions, ["10-K", "10-K/A", "20-F", "20-F/A", "40-F", "40-F/A"])
    latest_10q = recent_filings(submissions, ["10-Q", "10-Q/A", "6-K"])
    latest_proxy = recent_filings(submissions, ["DEF 14A", "DEFA14A"])
    latest_8k = recent_filings(submissions, ["8-K"])

    revenue = choose_fact(
        facts,
        [
            "RevenueFromContractWithCustomerExcludingAssessedTax",
            "RevenueFromContractWithCustomerIncludingAssessedTax",
            "SalesRevenueNet",
            "Revenues",
        ],
        "USD",
    )
    operating_income = choose_fact(facts, ["OperatingIncomeLoss"], "USD")
    net_income = choose_fact(facts, ["NetIncomeLoss", "ProfitLoss"], "USD")
    cfo = choose_fact(facts, ["NetCashProvidedByUsedInOperatingActivities"], "USD")
    capex = choose_fact(
        facts,
        [
            "PaymentsToAcquirePropertyPlantAndEquipment",
            "PropertyPlantAndEquipmentAdditions",
        ],
        "USD",
    )
    cash = choose_fact(facts, ["CashAndCashEquivalentsAtCarryingValue"], "USD")
    debt = choose_fact(
        facts,
        [
            "LongTermDebtAndFinanceLeaseObligations",
            "LongTermDebtAndCapitalLeaseObligations",
            "LongTermDebt",
            "LongTermBorrowings",
        ],
        "USD",
    )
    current_debt = choose_fact(
        facts,
        ["LongTermDebtCurrent", "ShortTermBorrowings", "ShortTermDebt"],
        "USD",
    )
    shares = choose_fact(facts, ["CommonStockSharesOutstanding"], "shares")

    cfo_val = float(cfo["val"]) if cfo else None
    capex_val = abs(float(capex["val"])) if capex else None
    cash_val = float(cash["val"]) if cash else None
    debt_val = float(debt["val"]) if debt else 0.0
    current_debt_val = float(current_debt["val"]) if current_debt else 0.0
    total_debt = debt_val + current_debt_val if (debt or current_debt) else None
    owner_earnings_proxy = None
    if cfo_val is not None and capex_val is not None:
        owner_earnings_proxy = cfo_val - capex_val
    net_cash = None
    if cash_val is not None and total_debt is not None:
        net_cash = cash_val - total_debt

    return {
        "match": {
            "company": match.title,
            "ticker": match.ticker,
            "cik": cik10,
            "filings_page": filings_page,
            "companyfacts_page": companyfacts_page,
        },
        "filings": {
            "latest_10k": latest_10k[:3],
            "latest_10q": latest_10q[:3],
            "latest_proxy": latest_proxy[:2],
            "latest_8k": latest_8k[:3],
        },
        "annual_metrics": {
            "revenue": revenue,
            "operating_income": operating_income,
            "net_income": net_income,
            "operating_cash_flow": cfo,
            "capex_total": capex,
            "owner_earnings_proxy": owner_earnings_proxy,
            "cash": cash,
            "debt_long_term": debt,
            "debt_current": current_debt,
            "net_cash_or_debt": net_cash,
            "shares_outstanding": shares,
        },
    }


def render_text(summary: dict[str, Any]) -> str:
    match = summary["match"]
    annual = summary["annual_metrics"]
    lines = [
        f"Company: {match['company']} ({match['ticker']})",
        f"CIK: {match['cik']}",
        f"SEC filings page: {match['filings_page']}",
        f"SEC companyfacts: {match['companyfacts_page']}",
        "",
        "Recent filings:",
    ]

    def add_filing_block(label: str, entries: list[dict[str, str]]) -> None:
        lines.append(f"- {label}:")
        if not entries:
            lines.append("  none found")
            return
        for entry in entries:
            lines.append(
                f"  {entry['form']} | {entry['filing_date']} | {entry['url']}"
            )

    add_filing_block("Annual", summary["filings"]["latest_10k"])
    add_filing_block("Quarterly", summary["filings"]["latest_10q"])
    add_filing_block("Proxy", summary["filings"]["latest_proxy"])
    add_filing_block("Current reports", summary["filings"]["latest_8k"])

    lines.extend(["", "Latest annual metrics:"])

    def line_for_fact(label: str, fact: dict[str, Any] | None, shares: bool = False) -> None:
        if not fact:
            lines.append(f"- {label}: n/a")
            return
        value = fmt_shares(fact["val"]) if shares else fmt_money(fact["val"])
        lines.append(f"- {label}: {value} | FY{fact.get('fy', 'n/a')} | tag={fact.get('tag')}")

    line_for_fact("Revenue", annual["revenue"])
    line_for_fact("Operating income", annual["operating_income"])
    line_for_fact("Net income", annual["net_income"])
    line_for_fact("Operating cash flow", annual["operating_cash_flow"])
    line_for_fact("Capex (total)", annual["capex_total"])
    owner = annual["owner_earnings_proxy"]
    lines.append(f"- Owner earnings proxy (CFO - total capex): {fmt_money(owner)}")
    line_for_fact("Cash", annual["cash"])
    line_for_fact("Long-term debt", annual["debt_long_term"])
    line_for_fact("Current debt", annual["debt_current"])
    lines.append(f"- Net cash / (net debt): {fmt_money(annual['net_cash_or_debt'])}")
    line_for_fact("Shares outstanding", annual["shares_outstanding"], shares=True)
    lines.extend(
        [
            "",
            "Notes:",
            "- Owner earnings proxy is a shortcut. Read the filing to estimate maintenance capex and working-capital normalization.",
            "- Missing values are common. Use the filing itself when companyfacts coverage is incomplete.",
            "- This helper is for U.S. SEC filers. Non-U.S. companies need local regulator and IR sources.",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch a simple SEC snapshot for a U.S.-listed company.")
    parser.add_argument("query", help="Ticker or company name")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of text")
    args = parser.parse_args()

    try:
        raw_tickers = fetch_json(TICKERS_URL)
        tickers = list(raw_tickers.values()) if isinstance(raw_tickers, dict) else raw_tickers
        match = pick_match(args.query, tickers)
        if not match:
            print(
                "No SEC match found. This helper only works for U.S. SEC filers. "
                "Use official IR and local regulator sources for non-U.S. companies.",
                file=sys.stderr,
            )
            return 1

        cik10 = str(match.cik).zfill(10)
        submissions = fetch_json(SUBMISSIONS_URL.format(cik=cik10))
        facts = fetch_json(COMPANYFACTS_URL.format(cik=cik10))
        summary = build_summary(match, submissions, facts)
        if args.json:
            print(json.dumps(summary, indent=2))
        else:
            print(render_text(summary))
        return 0
    except urllib.error.HTTPError as exc:
        print(f"SEC request failed: {exc}", file=sys.stderr)
        return 2
    except urllib.error.URLError as exc:
        print(f"Network error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
