# K 8.W.5 — Monthly cost estimate + DIAL cap: cart-api

---

## Line-by-line arithmetic

### Cloud rent (flat)

| Component | Monthly cost |
|-----------|-------------|
| 3 cart-api pods (compute) | — |
| 1 Postgres database | — |
| 1 Redis cache | — |
| 1 load balancer | — |
| **Cloud rent subtotal** | **$1,500** |

Cloud rent is flat — it does not scale with request volume or AI call count.

---

### AI meter (scales with traffic)

| Line | Calculation | Cost |
|------|------------|------|
| Input tokens | 3,000,000 calls × 1,200 tokens/call = 3,600,000,000 tokens = **3,600 M tokens** × $2.50/M | **$9,000** |
| Output tokens | 3,000,000 calls × 200 tokens/call = 600,000,000 tokens = **600 M tokens** × $10/M | **$6,000** |
| **AI meter subtotal** | | **$15,000** |

Hand-check: input line alone = 3,000,000 × 1,200 / 1,000,000 × $2.50 = 3,600 × $2.50 = **$9,000** ✓

---

### Monthly total

| Subtotal | Amount | Share |
|---------|--------|-------|
| Cloud rent | $1,500 | 9% |
| AI meter | $15,000 | 91% |
| **Total** | **$16,500** | 100% |

The AI meter is **10× the cloud rent**. A 2× traffic spike doubles the monthly bill; a runaway loop (uncapped retries, repeated calls per request) would multiply it further.

---

## Attribution owner

The AI meter is owned by the **product team / cart feature P&L** — it is a direct function of the "summarise my cart" feature usage. The cloud rent is shared infrastructure owned by **ops / platform P&L**. These must be tracked and reported separately; lumping them hides which team's decisions are driving cost.

---

## Ship / ship-with-mitigation / reject

**Verdict: Ship with mitigation.**

At $16,500/month the cost is defensible for a feature serving 3M monthly users — approximately $0.005 per AI call. However, shipping without a gateway cost cap creates the same exposure Team A experienced: an uncapped retry loop or a prompt-size regression can double or triple the AI meter in days without a hard stop. The mitigation is the DIAL cap below; it must be in place before the AI step reaches production.

---

## DIAL hard cap

| Setting | Value | Rationale |
|---------|-------|-----------|
| Alert threshold | **$15,000/month** | Fires when spend reaches the expected level — signals that traffic is at plan or above; requires no action but triggers review |
| Hard cap | **$20,000/month** | Allows ~33% headroom for traffic spikes above plan; stops runaway at 1.3× expected before it compounds |

The alert must be set **below** the hard cap. If the first signal is a hard refusal in production (DIAL returning 429 / budget-exceeded), customers see errors; the alert gives the team time to investigate before the cap fires.

Equivalent per-day cap: $20,000 / 30 ≈ **$667/day** hard, **$500/day** alert.

---

## Key finding

91% of cart-api's cost is the AI meter, not the cloud rent. This means the cost profile is not a function of cluster size — it is a function of cart-summary call volume and prompt size. A product decision that increases the cart summary frequency (e.g. triggering on every page load instead of on checkout) or that grows the prompt (e.g. including product descriptions alongside SKUs) would multiply the AI meter without touching the infrastructure bill. The DIAL cap is the only control that bounds this class of change before it becomes a billing incident.
