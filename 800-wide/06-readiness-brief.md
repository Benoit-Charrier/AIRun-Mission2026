# K 8.W.6 — Cloud Operations & Support Pack: cart-api

**Service:** cart-api — Meridian Retail Group checkout service  
**AI step:** "Summarise my cart" — ~3,000,000 DIAL calls/month  
**Pack assembled from:** `01-stack-map.md` · `02-deploy-manifest.md` · `03-ci-workflow.md` · `04-incident-runbook.md` · `05-cost-estimate.md`

---

## Six readiness questions

| # | Question | Answer | Source |
|---|---------|--------|--------|
| 1 | **How does it deploy and roll back?** | Rolling update via `kubectl set image` in the CI workflow; each deploy is SHA-tagged. Rollback: `kubectl rollout undo deployment/cart-api` (one command; requires `revisionHistoryLimit: 3` set in the production manifest). The hardened pipeline (K 8.W.3) runs rollback automatically if `kubectl rollout status` fails within 120s. | `02-deploy-manifest.md`, `03-ci-workflow.md` |
| 2 | **Who gets paged?** | The observability stack watches all 7 components. Application-layer failures (pod OOMKill, error rate, latency) → **product team** on-call. Platform failures (LB, Postgres, Redis, DIAL gateway) → **ops team** on-call. Specific on-call rotation and escalation contacts: **UNKNOWN — owner needed** (ops team must provide the alert routing config). | `01-stack-map.md` |
| 3 | **What is monitored?** | Standard: metrics (CPU, memory, request rate, error rate, latency percentiles), logs, traces via the observability stack. DIAL gateway adds token consumption per request (prompt + completion tokens — the AI-specific signal). Two gaps the dashboard does not cover: (a) silent wrong answers — bad cart summaries that return HTTP 200; (b) latency degradation below the error threshold. Both require content-checking or SLO alerting, not standard uptime monitoring. | `01-stack-map.md`, `800-assessment.md` |
| 4 | **What does it cost per month, and what is the cap?** | **$16,500/month** ($1,500 cloud rent flat + $15,000 AI meter). DIAL cap: **$20,000/month hard** (alert at $15,000). Attribution: AI meter is product-team P&L, cloud rent is platform P&L. | `05-cost-estimate.md` |
| 5 | **What is the kill-switch?** | Application: `kubectl rollout undo deployment/cart-api` (reverts to prior image; takes ~30s). AI step only: set DIAL gateway token budget for `cart-api` to 0 (ops action; disables summarise calls, service continues without AI). Full service: ops scales deployment to 0 replicas. | `02-deploy-manifest.md`, `03-ci-workflow.md` |
| 6 | **Which support tier owns the top two ticket types?** | (1) **OOMKilled pods / CrashLoopBackOff** → **L2**: roll back deploy, set `resources.limits.memory`, redeploy (see `04-incident-runbook.md`; no code change required). (2) **AI summarise step not responding / wrong output** → **L2/ops** for gateway errors (check DIAL token budget, gateway status); **L3** if the prompt or parsing logic needs a code fix. | `04-incident-runbook.md` |

---

## Maturity gaps

| Gap | Severity | Status |
|-----|----------|--------|
| `resources.limits` missing in original manifest | **High** — direct cause of the K 8.W.4 OOMKill incident | Closed in production-ready manifest (`02-deploy-manifest.md`) |
| CI actions pinned to tags not SHAs | **High** — mutable tag is a supply-chain attack vector | Closed in hardened workflow (`03-ci-workflow.md`) |
| Long-lived registry secrets (not OIDC) | **High** — permanent credential exposure if repo is compromised | Closed in hardened workflow |
| Image not signed (no cosign) | **Medium** — consumer cannot verify build provenance | Closed in hardened workflow |
| On-call escalation path | **Medium** — routing config not confirmed | **UNKNOWN — owner needed** (ops team) |
| Silent-failure monitoring (semantic errors, sub-threshold latency) | **Medium** — green dashboard can miss both failure modes | **UNKNOWN — owner needed** (observability team) |

---

## L1–L3 support handover

| Ticket type | L1 | L2 | L3 |
|------------|----|----|-----|
| OOMKilled pods / CrashLoopBackOff | Acknowledge page; confirm pod status via `kubectl get pods -l app=cart-api`; escalate to L2 if OOMKilled | Run `04-incident-runbook.md`: roll back deploy, verify recovery, set memory limits before redeploy | Only if OOM persists after rollback (requires code change to reduce AI step memory footprint) |
| AI summarise not responding / wrong output | Acknowledge; check DIAL gateway health dashboard; escalate to L2/ops | Check DIAL token budget (is cap hit?); check gateway error logs; escalate to L3 if code change needed | Fix prompt, response parsing, or retry logic in cart-api code; redeploy via CI pipeline |

---

## Two-line verdict

**Not yet ready for the AI summarise step.** The hardened manifest and pipeline close the deployment and supply-chain gaps, but the on-call escalation routing and silent-failure monitoring are unresolved `UNKNOWN`s — without them, an OOMKill or a silent wrong-answer regression at 3 a.m. has no confirmed owner and no detection path.

**One blocker before the AI step ships:** confirm the on-call escalation path with the ops team and add at least one content-quality check (e.g. empty-response rate or a spot-check sample) to the observability stack. Everything else is documented and closeable.
