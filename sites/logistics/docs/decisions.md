# Decisions

Lightweight ADRs. Newest first.

---

## ADR-011 — Three thin front-ends (ops, booker, field)

**Status:** Accepted  
**Date:** 2026-08-10

### Decision

One domain API; **three role-based front-ends** sharing the same data:

1. **Ops** — day board, assign, timeline  
2. **Field** — mobile web job list + status transitions  
3. **Booker** — book + status timeline  

Avoid a single mega UI that mixes all roles. Skin/theme may differ in Phase 2; roles stay separate.

---

## ADR-010 — WhatsApp is the primary notification channel (Phase 1)

**Status:** Accepted  
**Date:** 2026-08-10

### Decision

1. **WhatsApp** (via existing tyneside-api helpers) is the **primary** channel for **job status-change notifications** in Phase 1.  
2. In-app chat is **Later** — not MVP.  
3. Mobile web field + booker UIs are **first-class**, not optional afterthoughts.  
4. Notification copy can be driven from `job_event` + language mapping (taxi vs cleaning labels later).

### Consequences

Wire WhatsApp into the status transition path once the FSM exists; treat missing WhatsApp credentials as soft-fail with logged skip (same pattern as charity donate intents).

---

## ADR-009 — Price snapshot on job; addresses free-text first

**Status:** Accepted  
**Date:** 2026-08-10

### Decision

1. **Pricing is stored on the job at booking/confirm time (`price_snapshot`), not looked up live later** from the catalogue.  
2. Catalogue `service_type` remains the source of *list* prices and modes; jobs freeze what was agreed.  
3. **Addresses are free-text + optional lat/lng** in Phase 1 — **no full geocoding pipeline required** for MVP.  
4. When lat/lng are present, field app uses them for map deep-links.

### Consequences

Receipts, ops history, and disputes always use snapshot fields. Geocoding can be added later without blocking Phase 1 exit.

---

## ADR-008 — Capacity and pricing modes designed in Phase 1 for Phase 2

**Status:** Accepted  
**Date:** 2026-08-10

### Decision

1. **`zone`** is first-class in Phase 1 (Howden first).  
2. **`service_type`** carries duration, pricing mode (`estimate` \| `fixed` \| `free`), list price, pre-book window, optional funding flag.  
3. Workers have simple availability early (`busy_until` / busy intervals).  
4. **Availability** is an API concern; over-booking is rejected server-side, not only in UI.  
5. Charity free cleans are normal service types with list price 0 + funding flag — no parallel workflow.  
6. Default pre-book window is **14 or 30 days** (configurable), not iCabbi’s ~7.  
7. Job-level **price_snapshot** rules: see ADR-009.

### Consequences

Phase 2 adds catalogue depth and real busy calendars; it does not invent a second booking engine.

---

## ADR-007 — Job status machine + append-only job_event

**Status:** Accepted  
**Date:** 2026-08-10

### Decision

Stable enum and server-validated transitions:

```text
requested → quoted? → confirmed → assigned → en_route → on_site → completed
exit paths: cancelled | no_show | failed
```

- `quoted` optional (skip for fixed-price packs).  
- UI labels may vary; enum does not.  
- **Every** transition writes append-only **`job_event`** (from, to, actor, timestamp, optional note).  
- Timeline views (ops + booker) read events, not ad-hoc status fields alone.

Detail: [Domain model](domain.html).

---

## ADR-006 — Auth model and org scoping (MVP)

**Status:** Accepted  
**Date:** 2026-08-10

### Context

Auth was the missing ADR. Field, booker, and ops need different friction. Multi-tenant sales are later, but **schema must not assume a single global table**.

### Decision

| Actor | MVP auth |
|-------|----------|
| **Ops / admin** | Session or simple JWT; email + password **or** magic link |
| **Booker** | Magic link or OTP (low friction) |
| **Field worker** | Magic link or short-lived PIN / token |
| **Service-to-service** | API keys later only — not primary human auth |

Rules:

1. Every tenant-owned row has **`org_id`**.  
2. Authorisation checks **org membership + role** server-side.  
3. One live org is fine; zero “global jobs” tables.  
4. WhatsApp remains the primary human messaging channel (existing helpers).

### Consequences

Implement auth + org scaffolding **before** deep UI polish ([Roadmap](roadmap.html) step 1).

---

## ADR-005 — Phase 1 is an iCabbi-class capability clone; Phase 2 is cleaning

**Status:** Accepted  
**Date:** 2026-08-10

### Context

Cleaning is a near-term need; starting only from “cleaning CRM” risks a thin tool. iCabbi-class dispatch is a mature reference for demand → dispatch → field worker → complete.

### Decision

1. Phase 1: generic iCabbi-class capability spine (our code/brand).  
2. Phase 2: specialise for Tyneside Cleaning on the same spine.  
3. No partnership claim; no Exchange/roaming early.  
4. Prefer **themed booker** over dual UIs when cleaning goes live.

### Consequences

Generic names (`job`, `field_worker`, `service_type`) stay. Feature prioritisation: [features.html](features.html).

---

## ADR-004 — Public host is logistics.tyneside.software

**Status:** Accepted  
**Date:** 2026-08-10

- Domain: `logistics.tyneside.software`  
- Pages repo: `Tyneside-Software/logistics.tyneside.software`  
- CNAME and CORS match this host only (we do not own `tyneside.logistics`).

---

## ADR-003 — Docs live in the static site, not only the API

**Status:** Accepted  
**Date:** 2026-08-10

Product docs and tasks under `sites/logistics/docs/`. Cloud Run `/docs` is OpenAPI for runtime only.

---

## ADR-002 — Brand pairing: site-generator + tyneside-api

**Status:** Accepted  
**Date:** 2026-08-10

Interactive brands pair `sites/<id>/` with `app/brands/<id>/`. Routes `/v1/<brand>/…` on shared Cloud Run.

---

## ADR-001 — Shared Cloud Run service, not a second deployable

**Status:** Accepted  
**Date:** 2026-08-10

Logistics is a brand router on **tyneside-api**. Split services only if scale or blast-radius demands it.
