---
product: Meridian retail site and app
feature: AI availability assistant
kata: 3.W.7
date: 2026-06-25
---

# SPEC.md — Meridian AI Availability Assistant

## User story
As a click-&-collect shopper, I want to see a confidence-graded availability estimate for my chosen store — with a freshness label and a fallback when the system can't confirm — so I know before I drive whether the item is likely to be there.

## Components

### 1. `AvailabilityIndicator`

| State | Trigger | Label text | Color token | Icon | Timestamp shown |
|-------|---------|-----------|-------------|------|----------------|
| `in-stock` | `confidence_score` ≥ 0.7 AND freshness < 6h | "In stock" | `color.feedback.success` | ✓ | Yes — "Confirmed {N} min ago" |
| `likely` | `confidence_score` 0.6–0.69 OR freshness 6–12h | "Likely in stock" | `color.feedback.warning` | ⚠ | Yes — "Estimated from data synced {N} min ago" |
| `uncertain` | `confidence_score` < 0.6 OR verdict = `UNCERTAIN` | "Uncertain — check before travelling" | `color.feedback.warning-muted` | ⚠ | Yes |
| `not-available` | verdict = `NOT_AVAILABLE` | "Not available at this store" | `color.feedback.error` | ✕ | No |
| `cannot-confirm` | freshness > 30 min OR verdict = `NO_DATA` OR timeout | "Can't confirm right now — call the store" | `color.neutral.subtle` | ⚠ | No — store phone shown instead |
| `loading` | request in-flight, < 1.5 s | Skeleton (3 lines) | `color.neutral.skeleton` | — | No |

**Placement:** inline on the product page, below the store selector, before the Reserve button activates.
**Typography:** `typography.label.s` for verdict text; `typography.body.xs` for timestamp.
**Disclosure link:** every state except `not-available` and `loading` carries an "Estimated from store data" tappable label. On tap: bottom sheet with confidence score, sync timestamp, and "not a guaranteed hold" statement.

---

### 2. `AlternativeStoreList`

Shown when primary store state is `uncertain`, `not-available`, or `cannot-confirm`.

| Field | Detail |
|-------|--------|
| Max items | 2 stores |
| Radius | ≤ 25 km from shopper's selected store |
| Ranking | Confidence descending, then distance ascending |
| Each row | Store name · distance · `AvailabilityIndicator` (compact) |
| Empty state | "No confirmed stock nearby — consider delivery" + delivery CTA |
| Placement | Below the primary `AvailabilityIndicator` block |
| Typography | Store name: `typography.label.m`; distance + meta: `typography.body.xs`; empty state: `typography.body.s` |
| Color tokens | Store name: `color.text.default`; distance: `color.text.subtle`; row divider: `color.border.subtle` |
| Spacing | Row padding: `spacing.md`; gap between rows: `spacing.sm` |

---

### 3. `FallbackBanner` (cannot-confirm state)

| Field | Detail |
|-------|--------|
| Trigger | `AvailabilityIndicator` state = `cannot-confirm` |
| Content | "Stock data is over 30 min old. Call the store to check before travelling." |
| CTA | `tel:` link to store phone number |
| Color token | `color.neutral.subtle` background; `color.border.default` border |
| Typography | `typography.body.s` |

---

### 4. `PickupFeedbackPrompt`

Shown on the order pickup-confirmation screen (post-collection).

| Field | Detail |
|-------|--------|
| Trigger | Order status = `COLLECTED` (or `READY_FOR_COLLECTION` for pre-pickup) |
| Question | "Was the availability estimate accurate?" |
| Responses | "Yes, it was there" / "Item wasn't there" |
| On submit | POST to `/feedback/availability` with `{ store_id, sku, verdict_at_reservation, outcome, timestamp }` |
| Logging | Server-side only; non-PII; aggregated weekly per store |

---

## AI-AC refinements (design level)

**AI-AC1 (confidence) — `AvailabilityIndicator` likely state:**
- Component: `AvailabilityIndicator` · Variant: `likely`
- Color token: `color.feedback.warning` (amber, contrast ≥ 4.5:1 on white)
- Typography: `typography.label.s`
- Placement: inline, below store selector, before Reserve button
- Visual gate: WHEN `confidence_score` < 0.7 → suppress green state, render `likely` variant with amber icon + timestamp

**AI-AC2 (refusal/fallback) — `FallbackBanner` + `AvailabilityIndicator` cannot-confirm state:**
- Component: `FallbackBanner` + `AvailabilityIndicator` · Variant: `cannot-confirm`
- Color token: `color.neutral.subtle` background; `color.border.default` border
- Typography: `typography.body.s` (banner message); `typography.label.s` (store phone CTA)
- Placement: replaces all positive availability indicators; phone CTA below the banner
- Visual gate: WHEN freshness > 30 min OR API timeout after 4 s → remove `in-stock` / `likely` states, render `cannot-confirm` + `FallbackBanner`

**AI-AC6 (negative AC) — carried verbatim into spec:**
> The `AvailabilityIndicator` MUST NOT render the `in-stock` state (green label, ✓ icon) when `confidence_score` < 0.7 OR `data_freshness_minutes` > 12*60. The Reserve button MAY remain active regardless of state — availability assessment never blocks checkout.

---

## Definition of Handoff Done — checklist

- [x] User story + base AC present (`04-ai-ac.md` AC1–AC4)
- [x] ≥ 3 AI-AC refined to component / variant / token / placement / visual gate (AI-AC1, AI-AC2, AI-AC6 above)
- [x] CONTEXT.md covers feature + audience + environment + constraints + out-of-scope (`06-context.md`)
- [x] SPEC.md lists ≥ 2 components with states + token references (`AvailabilityIndicator`, `AlternativeStoreList`, `FallbackBanner`, `PickupFeedbackPrompt`)
- [x] Asset / data reference explicit and resolvable (Availability API: `GET /api/v1/availability?sku={sku}&store_id={id}`; design tokens: `@meridian/ds`; feedback endpoint: `POST /api/v1/feedback/availability`)
- [x] Negative AC carried into SPEC.md (AI-AC6 verbatim in component spec)
