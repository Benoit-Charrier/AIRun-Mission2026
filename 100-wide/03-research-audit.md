# 03-research-audit

Date: 2026-06-24
Case: Case A - Meridian Retail
Inputs audited: `01-context-brief.md`, `02-primary-signal.md`

## Audit method

- Included only load-bearing claims that later katas (use cases, canvas, ROI, deck) would rely on.
- Tagged each claim as:
  - **sourced**: source exists and supports claim as stated.
  - **unverified**: source is weak for the claim strength or cannot be independently validated enough for decision-grade use.
  - **cut**: source mismatch, overreach, or duplicated claim that should not propagate.

## Trust ledger (load-bearing claims)

| # | Claim | Origin | Tag | Reason / evidence check | Decision |
|---|---|---|---|---|---|
| 1 | 78% of EU internet users bought online in 2025. | 01-context-brief | sourced | Directly stated in Eurostat article with date and dataset links. | Keep |
| 2 | EU online-buying share rose from 62% (2015) to 78% (2025). | 01-context-brief | sourced | Directly stated in Eurostat highlights section. | Keep |
| 3 | In Italy, 28% of internet users did not buy online in 2025. | 01-context-brief | sourced | Directly stated in Eurostat "Last purchase and frequency" section. | Keep |
| 4 | Delivery speed and poor website usability are common ecommerce frictions. | 01-context-brief | sourced | Eurostat problem-frequency section explicitly lists both. | Keep |
| 5 | Inditex 1Q2026 sales were EUR 8.7B (+5.8%) and May 1-Jun 1 store+online sales were +11.5% constant currency. | 01-context-brief | sourced | Stated in Inditex First Quarter 2026 Results release. | Keep |
| 6 | Amazon.nl launched lockers with next-day collection and 7-day pickup. | 01-context-brief / 02-primary-signal | sourced | Stated in About Amazon EU locker launch page. | Keep |
| 7 | Competitive direction converges on convenience infrastructure, putting pressure on fragmented operators. | 01-context-brief | unverified | Reasonable synthesis but inferential; only two competitor datapoints used. | Keep as hypothesis |
| 8 | DSA now imposes operational obligations relevant to marketplaces (traceability, reporting, transparency). | 01-context-brief | sourced | Supported by EC DSA impact page sections on marketplace obligations and reporting. | Keep |
| 9 | "Compliance-by-design is now a product requirement, not legal afterthought" for Meridian's segment. | 01-context-brief | unverified | Strategic interpretation; directionally supported but not directly evidenced for this exact segment. | Keep as hypothesis |
| 10 | Three "verbatims" in 02-primary-signal represent customer-side primary signal. | 02-primary-signal | cut | Quotes are competitor press copy, not customer/user interviews or support transcripts. | Remove from decision-grade evidence |
| 11 | Competitor teardown findings (solved/partial/unsolved) are enough to re-rate Meridian pain points. | 02-primary-signal | unverified | Teardown is desk-based from one page, no live product walk and no customer transcript triangulation. | Keep with low confidence |
| 12 | Pain point re-ratings (sharpened/sharpened/confirmed) are final enough for downstream ROI assumptions. | 02-primary-signal | cut | Evidence base is too thin for "final" status before audit hardening. | Re-rate as provisional only |

## Survival count

- **Claims in:** 12
- **Survived as sourced or provisional unverified:** 10
- **Cut:** 2
- **Survival ratio:** 10/12 (83%)

## One-line reasons for each cut

1. Claim #10 cut: primary signal did not use customer verbatims; it used competitor publication text.
2. Claim #12 cut: re-ratings were treated as final despite low-confidence primary-signal evidence.

## Weakest claim still kept (explicitly flagged)

- **Claim kept with highest risk:** #11 (teardown sufficient to re-rate pains).
- **Flag:** confirm before exec review.
- **Why kept anyway:** still useful as directional hypothesis to guide next-kata ideation, but not strong enough for quantified ROI assumptions.

## Propagation rules for next kata (K1.W.5)

Use only these as hard inputs:
- #1, #2, #3, #4, #5, #6, #8.

Use these only as soft hypotheses:
- #7, #9, #11.

Do not carry forward:
- #10, #12.
