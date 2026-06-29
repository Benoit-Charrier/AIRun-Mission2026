# 06-roi-uc3

Date: 2026-06-24
Case: Case A - Meridian Retail
Use case: UC-03 - Cross-channel identity and loyalty account resolution copilot
Currency: EUR millions unless noted

## Method

- Horizon: annualized run-rate view (steady-state) with one-time implementation costs.
- Payback formula: months until cumulative value > cumulative cost.
- Simplification used for this kata: steady-state annual net benefit converted to monthly.

$$
\text{Annual Net Benefit} = \text{Annual Value} - \text{Annual Run Cost}
$$

$$
\text{Payback Months} = \frac{\text{One-time Cost}}{\text{Annual Net Benefit}/12}
$$

## Assumption register (all numbers tagged)

| Driver | Pessimistic | Base | Optimistic | Source tag |
|---|---:|---:|---:|---|
| One-time build and integration | 2.0 | 1.5 | 1.0 | `unverified - confirm before exec review` |
| One-time identity data cleanup and migration | 1.4 | 1.0 | 0.7 | `unverified - confirm before exec review` |
| One-time change management and training | 0.7 | 0.5 | 0.3 | `unverified - confirm before exec review` |
| Annual model/inference/infra run cost | 0.9 | 0.7 | 0.5 | `unverified - confirm before exec review` |
| Annual manual review operations | 1.0 | 0.7 | 0.4 | `unverified - confirm before exec review` |
| Annual monitoring/compliance/audit ops | 0.4 | 0.3 | 0.2 | `unverified - confirm before exec review` |
| Annual loyalty revenue-contribution uplift | 2.4 | 3.8 | 5.6 | `unverified - confirm before exec review` |
| Annual campaign waste reduction | 0.8 | 1.3 | 1.9 | `unverified - confirm before exec review` |
| Annual identity-support ticket savings | 0.3 | 0.5 | 0.75 | `unverified - confirm before exec review` |
| Annual churn-avoidance contribution | 0.5 | 0.9 | 1.4 | `unverified - confirm before exec review` |
| Annual risk-avoidance expected value | 0.1 | 0.25 | 0.45 | `unverified - confirm before exec review` |

Reference-case context used to shape ranges (non-monetary):
- Fragmented loyalty and identity across regions are explicit in Case A.
- Phase 1 includes unified identity and checkout scope.
- Source: `curriculum-public/modules/001-reference-cases.md`.

## Three-scenario ROI table

| Row | Pessimistic | Base | Optimistic |
|---|---:|---:|---:|
| One-time costs (total) | 4.10 | 3.00 | 2.00 |
| Annual run costs (total) | 2.30 | 1.70 | 1.10 |
| Annual value (total) | 4.10 | 6.75 | 10.10 |
| Annual net benefit | 1.80 | 5.05 | 9.00 |
| Payback period (months) | 27.3 | 7.1 | 2.7 |

## Interpretation

- Pessimistic case does not pay back within 12 months; this is intentionally conservative.
- Base case payback is under 12 months with meaningful upside from retention and campaign efficiency.
- Optimistic case is strong but depends on high precision and low manual-review burden.

## Top-2 sensitivity drivers (base case, +/-20%)

### 1) Loyalty revenue-contribution uplift (largest upside driver)
- Base value: 3.8
- At -20%: 3.04 -> annual net benefit becomes 4.29 -> payback ~8.4 months.
- At +20%: 4.56 -> annual net benefit becomes 5.81 -> payback ~6.2 months.

### 2) Manual review operations cost (largest execution-risk cost driver)
- Base cost: 0.7
- At +20%: 0.84 -> annual net benefit becomes 4.91 -> payback ~7.3 months.
- At -20%: 0.56 -> annual net benefit becomes 5.19 -> payback ~6.9 months.

## Decision note

- Financially viable in base and optimistic scenarios, but governance and data-quality execution are gating risks.
- Before executive review, replace `unverified` monetary assumptions with at least one internal benchmark per line (finance baseline, support ticket volume, loyalty conversion baseline, and migration staffing plan).
