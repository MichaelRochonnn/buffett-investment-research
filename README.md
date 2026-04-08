# Buffett Investment Research

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
![Codex Skill](https://img.shields.io/badge/codex-skill-blue)
![Framework](https://img.shields.io/badge/framework-Buffett-orange)
![Research Style](https://img.shields.io/badge/research-primary--source--first-lightgrey)

A Codex skill for Buffett-style company analysis, value-investing research, and structured investment memos.

This repository turns Buffett's investing principles into an operational research workflow. Instead of producing a fast opinion, it pushes Codex to do the slower, more important work first: define the exact business, gather primary sources, judge moat and management, stress-test the balance sheet, estimate normalized owner earnings, and only then talk about price.

## What This Is

This is not just a prompt.

It is a reusable skill that helps Codex analyze a company the way Buffett often described in Berkshire shareholder letters:

- understand the business before projecting outcomes
- treat stocks as partial ownership interests in businesses
- separate business quality from price attractiveness
- reject weak culture, fragile financing, and promotional management
- accept `pass` and `outside competence` as legitimate outcomes

## Why This Is Different From A Normal Research Prompt

Most investment prompts produce a quick synthesis.

This skill is designed to produce a disciplined memo.

### A normal prompt often:

- starts from a narrative or market angle
- mixes primary facts with commentary too early
- overweights valuation multiples
- hides uncertainty behind confident language
- forces a buy or sell tone even when the evidence is mixed

### This skill instead:

- starts with filings, annual reports, proxy materials, and official IR sources
- uses a fixed Buffett-style evaluation sequence
- applies hard filters before scoring attractive traits
- treats moat, management, and capital allocation as first-class questions
- prefers normalized owner earnings over EBITDA storytelling
- allows `Watchlist`, `Reject`, and `Outside competence` as honest conclusions

In short: it is built for investment judgment, not content generation.

## What You Get

When you give the skill a company name or ticker, it can return a structured memo covering:

1. Investment snapshot
2. Circle of competence
3. Business economics
4. Moat assessment
5. Management and culture
6. Balance sheet and crisis resilience
7. Capital allocation
8. Valuation
9. Key risks
10. Final verdict

Each memo is meant to be decision support, not personalized financial advice.

## Buffett Framework Used Here

The skill evaluates companies across seven dimensions:

1. Understandability
2. Moat durability
3. Management and culture
4. Capital allocation
5. Financial strength
6. Reinvestment runway
7. Valuation and margin of safety

It then assigns one of five verdicts:

- `Strong fit`
- `Watchlist`
- `Weak fit`
- `Reject`
- `Outside competence`

## Best Use Cases

This skill works especially well when you want to:

- screen a business through a Buffett-style lens
- compare several companies on moat and capital allocation quality
- produce a repeatable investment memo instead of an ad hoc opinion
- decide whether a business is inside your circle of competence
- challenge a superficially cheap stock with deeper business-quality questions
- evaluate whether management behaves like owner-operators or empire builders

## Example Inputs

### Chinese

- `用巴菲特框架分析拼多多`
- `分析腾讯是否符合巴菲特标准，并输出完整投资备忘录`
- `按巴菲特框架评估贵州茅台，重点看护城河、管理层和估值`
- `帮我判断 Costco 现在是否具备 Buffett 式的安全边际`
- `分析一家银行是否在我的能力圈内，并说明为什么`

### English

- `Analyze Apple using a Buffett-style investment framework.`
- `Write a Buffett-style investment memo on Moody's.`
- `Assess whether Coca-Cola is a Strong fit or only a Watchlist candidate today.`
- `Evaluate this company using Buffett framework with special focus on moat and capital allocation.`
- `Is this business inside or outside Buffett's circle of competence?`

## Example Output

This is an abridged example of the kind of output the skill is designed to produce:

```text
Buffett Investment Memo (abridged)
Company: PDD Holdings (NASDAQ: PDD)
Verdict: Watchlist
Confidence: Medium

Circle of competence
- Marketplace economics are understandable
- VIE structure and cross-border expansion reduce certainty

Moat
- Low-price habit, merchant density, and scale are real advantages
- Moat exists, but not yet a classic Buffett-grade set-and-forget moat

Management and culture
- Strong execution
- Minority-shareholder structure and disclosure complexity deserve a discount

Valuation
- Cash-rich business; headline multiple may look cheap
- The key question is durability, not just the multiple

What could upgrade the rating
- Clear proof that reinvestment still earns high returns
- Evidence that the moat is widening rather than being defended by spend
```

A full run should also include source links, filing references, missing facts, and a clear explanation of what would break the thesis.

## How The Workflow Works

The skill follows a deliberate sequence:

1. Identify the exact entity
   Ticker, exchange, geography, segments, and ownership structure.

2. Gather primary sources first
   Annual reports, 10-K or equivalent, proxy, regulator filings, official IR materials, and earnings disclosures.

3. Build a base fact set
   Revenue mix, margins, leverage, share count, capital-allocation history, and management context.

4. Apply the Buffett framework
   Moat, culture, incentives, resilience, reinvestment runway, and valuation.

5. Explain the verdict
   The memo shows why the business qualifies or fails, not just the final label.

## U.S. Company Helper Script

For U.S. issuers, the repo includes a small SEC snapshot helper:

```bash
python3 scripts/sec_company_snapshot.py "AAPL"
python3 scripts/sec_company_snapshot.py "American Express"
```

The script helps bootstrap research with:

- company match and CIK
- latest annual filing
- latest quarterly or current filings
- proxy links
- high-level financial facts from SEC company facts
- a conservative owner-earnings proxy

## How To Install

Place this folder at:

```text
$CODEX_HOME/skills/buffett-investment-research
```

In many local Codex setups, that path looks like:

```text
~/.codex/skills/buffett-investment-research
```

Once installed, ask Codex for Buffett-style company analysis, value-investing research, moat assessment, management review, capital-allocation analysis, or a Buffett-style investment memo.

## Repository Structure

```text
.
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── framework.md
│   ├── memo-template.md
│   └── timeline.md
└── scripts/
    └── sec_company_snapshot.py
```

- `SKILL.md`: the core instructions Codex follows
- `references/framework.md`: the Buffett scorecard and hard filters
- `references/memo-template.md`: the required memo structure
- `references/timeline.md`: Buffett's philosophical evolution, mistakes, and crisis lessons
- `scripts/sec_company_snapshot.py`: a U.S. filings bootstrap helper

## Research Philosophy

This skill is built around a few simple ideas:

- a stock is a partial ownership interest in a business
- good business and good price are different questions
- `pass` is a valid answer
- weak culture, fragile financing, and promotional management can invalidate a cheap valuation
- the best investment process often begins with elimination

## Important Notes

- This is not personalized financial advice.
- The skill is designed for framework-based judgment, not prediction.
- It works best when current filings, prices, and management information can be verified live.
- `Outside competence` is an acceptable and sometimes best answer.

## Source Base

The skill was built from a structured synthesis of Buffett's shareholder letters and then translated into a repeatable research workflow.

Primary conceptual inputs include:

- Berkshire Hathaway shareholder letters
- Berkshire annual reports and reporting archives
- Buffett's commentary on moat, management, capital allocation, owner earnings, mistakes, and risk

## Suggested GitHub Topics

If you want this repository to be more discoverable on GitHub, these topics fit well:

- `codex-skill`
- `investing`
- `value-investing`
- `warren-buffett`
- `equity-research`
- `company-analysis`
- `financial-analysis`
- `moat`
- `capital-allocation`
- `due-diligence`

## License

This project is licensed under the `MIT` License.

See [LICENSE](LICENSE) for the full text.
