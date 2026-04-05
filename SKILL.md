---
name: buffett-investment-research
description: Buffett-style company analysis and value-investing research. Use when Codex needs to analyze a business or listed company with Warren Buffett's framework, including 巴菲特框架, 价值投资, 护城河, 管理层, 企业文化, 资本配置, 财务韧性, 回购, 错误复盘, 危机应对, or when asked for a Buffett-style investment memo or recommendation.
---

# Buffett Investment Research

Use this skill to produce a Buffett-style research memo, not a hot take. The goal is to judge business quality, management quality, capital allocation, balance-sheet resilience, reinvestment runway, and price discipline.

Treat the output as decision support rather than personalized financial advice. Give a framework-based verdict, state assumptions plainly, and make uncertainty visible.

## Workflow

1. Define the company clearly.
   Confirm the exact entity, ticker, exchange, geography, business mix, and whether the business is within the current circle of competence.

2. Gather primary sources first.
   Always browse for current analysis because filings, prices, management teams, leverage, and capital allocation can change.

3. For U.S. issuers, start with the SEC helper script.
   Run `python3 /Users/fane/.codex/skills/buffett-investment-research/scripts/sec_company_snapshot.py "Company or Ticker"`.

4. For non-U.S. issuers, start with official sources.
   Prioritize the investor-relations site, annual report, exchange filings, regulator filings, proxy or AGM materials, and earnings-call transcripts.

5. Read the local references in this order.
   Start with `references/framework.md`.
   Then read `references/memo-template.md`.
   Read `references/timeline.md` when the user asks for deeper philosophical context, historical evolution, Buffett's mistakes, or crisis playbooks.

6. Write the memo.
   Judge the business first, then the price. Do not start from the chart.

## Source Priority

- Official annual reports, 10-K or equivalent, proxy, regulator filings
- Official earnings-call transcripts, investor presentations, and capital-markets materials
- Competitor filings and industry disclosures
- Credit-rating commentary, regulator data, and trustworthy trade sources
- Secondary commentary only after primary-source facts are pinned down

## Buffett Rules To Preserve

- Analyze a stock as a partial ownership interest in a business.
- Do not forecast the market, macro cycle, rates, or FX unless the company is directly exposed and the exposure is contractual or balance-sheet based.
- Prefer simple and durable businesses over complicated stories.
- Reject businesses outside the circle of competence instead of forcing a verdict.
- Distinguish business quality from price attractiveness.
- Reject weak culture, aggressive accounting, or fragile financing even when valuation appears cheap.
- Prefer patience over false precision. `Pass` is a valid answer.

## Hard Filters

Reject or downgrade sharply when one of these is true:

- The business model cannot be explained simply
- Economics depend on commodity pricing with no durable edge
- The company needs continuous external capital to survive
- Leverage or refinancing risk can impair permanent capital
- Management lacks candor or capital-allocation discipline
- Industry change is too fast to estimate normalized economics
- The thesis only works if a greater fool pays more later

## Output Requirements

Use the structure in `references/memo-template.md`. Always include:

- Circle-of-competence judgment
- Moat assessment with concrete evidence
- Management and culture assessment
- Capital-allocation assessment
- Balance-sheet and crisis-resilience assessment
- Valuation logic using normalized owner earnings or a conservative proxy
- A clear verdict: `Strong fit`, `Watchlist`, `Weak fit`, `Reject`, or `Outside competence`
- A confidence level and the top missing facts that could change the conclusion
- Source links

## Notes On Recommendations

If the user asks whether to invest, answer in Buffett-style language:

- Say what kind of business this is
- Say whether it appears to have a durable moat
- Say whether management acts like owner-operators or empire builders
- Say whether the balance sheet can survive stress
- Say whether the price implies an attractive prospective return
- State the main reasons to pass even if the company is excellent

Never pretend certainty. If the business is good but the price is not, say so plainly.
