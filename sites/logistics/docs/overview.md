# Product overview

## Working name

**Tyneside Logistics** — field operations platform under the Tyneside brand family.  
**Public URL:** [logistics.tyneside.software](https://logistics.tyneside.software)

## Strategy (two phases)

We are **not** inventing a vague “logistics suite” first. We copy a proven vertical shape, then specialise.

| Phase | Name | Goal |
|-------|------|------|
| **1** | **iCabbi-style clone** | Clean, **generic** dispatch spine: demand → dispatch → field worker → complete. Our code, our brand. Research: [iCabbi notes](icabbi.html). |
| **2** | **Cleaning bookings** | Same spine for **Tyneside Cleaning** — catalogue, zones, capacity, cleaner UI. Not a rewrite. |

Generic domain language is intentional and high-leverage:

- `job` · `field_worker` · `service_type` · `zone` · `org` · `job_event`

UI says “driver / cleaner”; schema does not fork.

```
  Phase 1                         Phase 2
  ────────                        ────────
  Booker  →  Dispatch  →  Driver   Customer → Ops desk → Cleaner
     \          |          /            \       |        /
      \____ Job lifecycle ____/          \__ same spine __/
```

## Why this product exists

- Tyneside Software’s long-term story includes **vertical logistics / field work-management**.  
- Cleaning needs a **real ops product**, not only a marketing form.  
- iCabbi-class systems prove the UX of dispatch; we clone **capabilities**, then expand into cleaning.

## What “good” looks like early

| Signal | Meaning |
|--------|---------|
| Ops dog-foods first | Dispatcher console before fancy booker polish |
| Multi-tenant ready | `org_id` on every row from day one (one org live) |
| Auditable jobs | Every status change → `job_event` |
| Phase 2-safe APIs | Zones, duration, **price snapshot**, availability / `busy_until` |
| Comms | **WhatsApp** primary for status notifications |
| UIs | **Three thin front-ends** (ops, booker, field) — not one mega app |
| Demo | Seed + scripted path; **10 jobs E2E, zero spreadsheets** |

## Intended users

### Phase 1 (taxi-shaped clone)

| Role | Needs |
|------|--------|
| **Booker** | Book now / pre-book, price, **status timeline**, WhatsApp for human comms |
| **Field worker** | Jobs, accept, status transitions, nav deep-link, today/week counters |
| **Ops** | Day board, assign, rules filters, full event timeline |

### Phase 2 (cleaning)

| Role | Maps from Phase 1 |
|------|-------------------|
| **Customer** | Booker |
| **Cleaner** | Field worker |
| **Cleaning ops** | Ops desk |
| **Job** | Clean pack / commercial visit |

## Surfaces (ours)

| Surface | Status | Notes |
|---------|--------|-------|
| Marketing home | Scaffolded | `logistics.tyneside.software` |
| Documentation | Active | `/docs/` — including [domain](domain.html) |
| Web app | Placeholder | `/app/` |
| API | Scaffolded | `tyneside-api` → `/v1/logistics/*` |
| Cleaning site | Exists | Prefer eventual **themed booker** over dual UIs |

## Domain (summary)

Full model: **[Domain model](domain.html)**.

| Entity | Role |
|--------|------|
| **org** | Tenant; everything scoped |
| **zone** | First-class early (Howden first) |
| **service_type** | Duration, pricing mode, pre-book window |
| **booker** / **field_worker** | Demand / supply people |
| **job** | Work unit; **address_text**; optional lat/lng; **price_snapshot** |
| **job_event** | MVP append-only timeline |
| **job_attachment** | Notes/files day one; P2 checklist/photos UI |
| **field_worker** | Incl. simple availability (`busy_until`) |

**Status spine:**  
`requested` → (`quoted`) → `confirmed` → `assigned` → `en_route` → `on_site` → `completed`  
plus terminal `cancelled` / `no_show` / `failed`.

Language mapping (driver ↔ cleaner, etc.): [Domain model](domain.html).

## Phase 1 → Phase 2 hand-off (clean)

| Built in Phase 1 | Phase 2 adds |
|------------------|--------------|
| Org-scoped spine + FSM + events | Real cleaner capacity calendars |
| Zones + service_types; job **price snapshot** | Full clean catalogue + charity free type |
| Free-text addresses (optional lat/lng) | Optional geocoding later |
| Availability + worker busy hooks | Strict over-book in prod |
| Attachments schema | Checklist + photo UI |
| Three role UIs | Cleaning theme / copy |
| WhatsApp status notifications | Same helpers |

Do **not** invent a parallel “cleaning module” that bypasses jobs.

## Out of scope (for now)

- National/international **Exchange** / app roaming  
- Affiliation with iCabbi / Renault / Mobilize  
- Selling multi-tenant SaaS before Howden volume  
- Full NEMT / Voice AI / NFC / CarPlay as launch blockers  
- In-app chat (WhatsApp first)  
- Secrets in the static Pages repo  

## Related brands

- [tyneside.software](https://tyneside.software/) — jobs engine story  
- [tyneside.cleaning](https://tyneside.cleaning/) — Phase 2 demand  
- [tyneside.group](https://tyneside.group/) — family portal  
- [tyneside-api](https://github.com/Tyneside-Software/tyneside-api) — shared backend  

## Doc map

| Doc | Use |
|-----|-----|
| [Domain](domain.html) | Entities, FSM, capacity |
| [Features](features.html) | Prioritisation |
| [Roadmap](roadmap.html) | Build order |
| [Tasks](tasks.html) | Checklist |
| [Decisions](decisions.html) | ADRs |
| [iCabbi](icabbi.html) | Reference research |
