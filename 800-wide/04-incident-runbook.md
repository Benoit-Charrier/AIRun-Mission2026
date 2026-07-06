# K 8.W.4 — Incident diagnosis + runbook: cart-api OOMKill

**Incident:** Half of `cart-api`'s pods are in `CrashLoopBackOff`. Events show `OOMKilled`. Crash started 20 minutes after a deploy that added the AI summarise step. Error rate climbing; latency rising on healthy pods as they absorb load.

---

## Three ranked hypotheses

| Rank | Hypothesis | Evidence from incident + manifest | Cheapest confirming step |
|------|-----------|----------------------------------|--------------------------|
| 1 | **Missing memory limit + AI step memory spike** — The summarise step buffers the full prompt (1,200 tokens) and completion (200 tokens) per request. With no `resources.limits.memory` set in the manifest, pods grow unbounded until the node OOM-kills them. | `OOMKilled` in events; 20-min timing matches the deploy; manifest audit (K 8.W.2) confirmed no `limits:` block. Direct link. | `kubectl top pod -l app=cart-api` — if memory is climbing on healthy pods toward node capacity, confirms. Also: `kubectl describe pod <crashlooping-pod>` and look for `Limits: <none>`. |
| 2 | **No rolling update strategy → multi-pod simultaneous replacement** — Without `strategy: RollingUpdate / maxUnavailable: 0`, the deploy controller replaced all pods at once. All new pods started the AI step simultaneously, exhausting node memory faster than a staggered rollout would. | Manifest has no `strategy:` field (K 8.W.2 gap #5); no `readinessProbe` (gap #2) means Kubernetes couldn't throttle pod readiness to gate the rollout. | Check deploy events: `kubectl describe deployment cart-api` — if `Updated Replicas: 3` flipped in a single event rather than incrementally, confirms. |
| 3 | **Memory leak in the AI summarise code** — The new code path holds a reference to the LLM response buffer across requests, growing heap with each call. | Timing matches the deploy. However, OOM within 20 minutes suggests a spike, not a slow leak — a leak typically takes hours to surface. This is the weakest hypothesis unless pod memory was already near the node ceiling before the deploy. | Check pod restart count and timing: `kubectl get pods -l app=cart-api` — if pods crash within seconds of starting (not after serving traffic), a leak on request is less likely; a startup spike (hypothesis 1) is more likely. |

**Most-likely root cause:** Hypothesis 1 — missing `resources.limits.memory`, combined with the AI step's per-request memory footprint. The manifest gap was identified in K 8.W.2 and the timing is exact.

---

## Immediate mitigation

Roll back the deploy to the pre-AI-step image:

```bash
kubectl rollout undo deployment/cart-api
kubectl rollout status deployment/cart-api --timeout=120s
```

The hardened CI workflow from K 8.W.3 includes `kubectl rollout status || kubectl rollout undo` — the rollback is one command or runs automatically.

---

## Durable fix

1. Set `resources.limits.memory: "512Mi"` (and `requests.memory: "256Mi"`) in the deployment manifest — the gap K 8.W.2 flagged as its first finding.
2. Profile the AI step's peak memory under load (prompt + completion + any buffering) and set the limit to at least 2× that ceiling.
3. Add `readinessProbe` so the rolling update waits for each pod to be healthy before replacing the next (gap #2 from K 8.W.2).
4. Re-deploy the AI summarise step only after memory limits and the readiness probe are in place.

---

## Runbook entry

| Row | Content |
|-----|---------|
| **Detection** | Alert: `cart-api pod OOMKilled` (event `reason=OOMKilled` on any cart-api pod) OR error rate > 5% for 2 consecutive minutes OR `CrashLoopBackOff` on ≥ 1 cart-api pod. |
| **Diagnosis** | 1. `kubectl get pods -l app=cart-api` — confirm CrashLoopBackOff count. 2. `kubectl describe pod <pod>` — confirm `OOMKilled` in Events and `Limits: <none>`. 3. `kubectl top pod -l app=cart-api` — record memory on surviving pods. 4. Check recent deploys: `kubectl rollout history deployment/cart-api`. |
| **Fix** | If the crash followed a recent deploy: roll back (`kubectl rollout undo deployment/cart-api`). Then set `resources.limits.memory` in the manifest and redeploy. If no recent deploy: check for node pressure (`kubectl describe node`) and whether a traffic spike exhausted an existing but too-low limit. |
| **Rollback** | `kubectl rollout undo deployment/cart-api` — reverts to the previous replica set. Verify with `kubectl rollout status deployment/cart-api`. Requires `revisionHistoryLimit ≥ 1` in spec (K 8.W.2 production manifest sets it to 3). |
| **Owning support tier** | **L2** — rolling back and setting a resource limit requires no code change; the runbook above is complete. Escalate to **L3** only if OOM persists after rollback (leak in existing code) or if the AI step requires a code-level memory optimisation before it can be safely re-deployed. |

---

## Key finding

The OOMKill was predictable from the manifest: K 8.W.2's fresh-session audit named `missing resources.limits` as its first finding and noted it was the direct cause of this class of incident. A missing limit is not a cosmetic gap — it is the difference between a pod that consumes what it needs and a pod that evicts its neighbours. The AI summarise step amplified the risk because its memory footprint is a function of prompt size, which grows with cart size. Neither the step nor the limit can ship without the other.
