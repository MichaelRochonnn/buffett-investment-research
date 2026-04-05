# Buffett Investment Research

A Codex skill for Buffett-style company analysis and value-investing research.

This repository packages a reusable research workflow that evaluates a business the way Warren Buffett often described in his shareholder letters: first understand the business, then judge moat, management, capital allocation, balance-sheet resilience, reinvestment runway, and only then ask whether the current price offers a margin of safety.

It is built for decision support, not certainty. The goal is to produce a structured investment memo, not a hot take.

## What This Skill Does

When you give the skill a company name or ticker, it can:

- identify the exact entity, ticker, exchange, geography, and business mix
- gather primary sources first, including filings, annual reports, proxy materials, and official IR releases
- analyze the business with a Buffett-style framework
- judge whether the company is understandable, durable, well-managed, financially resilient, and sensibly priced
- return a structured memo with a clear verdict band and source links

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

## Typical Output

The memo follows a consistent structure:

1. Investment snapshot
2. Circle of competence
3. Business economics
4. Moat assessment
5. Management and culture
6. Balance sheet and crisis resilience
7. Capital allocation
8. Valuation
9. Key risks
10. Verdict

This makes the output useful for repeated company screening, side-by-side comparison, and follow-up diligence.

## Example Inputs

You can invoke the skill with prompts like these:

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

## How To Use

### 1. Install the skill

Place this folder at:

```text
$CODEX_HOME/skills/buffett-investment-research
```

In many local Codex setups, that path looks like:

```text
~/.codex/skills/buffett-investment-research
```

### 2. Ask Codex to use it

The skill is designed to trigger when the request clearly asks for:

- Buffett-style company analysis
- value investing research
- moat assessment
- management and culture evaluation
- capital allocation review
- Buffett-style investment memo or recommendation

### 3. Let the workflow gather evidence

The skill prioritizes:

- company filings and annual reports
- SEC or regulator pages
- investor-relations materials
- official earnings releases and call transcripts
- competitor filings and industry disclosures

Secondary commentary is used only after the primary facts are pinned down.

### 4. Read the verdict in context

The result is not meant to be a blind buy or sell signal. It is a structured memo that makes the reasoning explicit and shows what evidence is still missing.

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

## Repository Structure

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── framework.md
│   ├── memo-template.md
│   └── timeline.md
└── scripts/
    └── sec_company_snapshot.py
```

- `SKILL.md`: core instructions for Codex
- `references/framework.md`: the Buffett scorecard and hard filters
- `references/memo-template.md`: required memo structure
- `references/timeline.md`: philosophical evolution, mistakes, and crisis lessons
- `scripts/sec_company_snapshot.py`: SEC bootstrap script for U.S.-listed companies

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

The skill was originally built from a structured synthesis of Buffett's shareholder letters and then turned into an operational workflow for company research.

Primary conceptual inputs include:

- Berkshire Hathaway shareholder letters
- Berkshire annual reports and reporting archives
- Buffett's long-running commentary on moat, management, capital allocation, owner earnings, and risk

## License

No license has been added yet. If you want others to reuse or adapt this skill, add a license before wider distribution.
