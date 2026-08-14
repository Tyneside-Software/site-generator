# Domain model

Generic language on purpose: **job**, **field_worker**, **service_type**, **zone**, **org**.  
UI copy may say “driver / cleaner / passenger / customer”; the schema stays stable.

Review note (accepted): Phase 1 is an iCabbi-class spine; Phase 2 re-skins and specialises — not a second product.

---

## Language mapping (taxi ↔ cleaning)

Keep UI strings localised by vertical; **never fork the schema**.

| Generic (schema / API) | Taxi-shaped UI | Cleaning UI |
|------------------------|----------------|-------------|
| `org` | Fleet | Cleaning business |
| `field_worker` | Driver | Cleaner |
| `booker` | Passenger / customer | Customer |
| `service_type` | Vehicle / tariff class | Clean pack / SKU |
| `zone` | Operating area | Service ward (e.g. Howden) |
| `job` | Trip / booking | Clean / visit |
| `requested` | Requested | Requested |
| `quoted` | Quote sent | Quote sent (often skipped) |
| `confirmed` | Confirmed | Confirmed / booked |
| `assigned` | Driver assigned | Cleaner assigned |
| `en_route` | Driver en route | Cleaner on the way |
| `on_site` | On scene / POB-adjacent | On site / in progress |
| `completed` | Completed | Completed |
| `cancelled` | Cancelled | Cancelled |
| `no_show` | No-show | No-show / access failed |
| `failed` | Failed | Failed |
| Ops console | Dispatch desk | Cleaning ops desk |
| Booker app | Passenger booker | Customer booker |
| Field app | Driver app | Cleaner app |

---

## Multi-tenant from day one

Even with a single live organisation, **every tenant-owned row carries `org_id`**.

| Principle | Rule |
|-----------|------|
| Isolation | Queries and mutations always scoped by `org_id` (never trust client org alone) |
| First org | Seed “Tyneside” (or Tyneside Cleaning) as org #1 |
| Sales multi-tenant | Parked until real Howden volume (Phase 3+ idea only) |

See [ADR-006](decisions.html) (auth + org scoping).

---

## Three front-ends, one data model

Same API and entities; **three thin UIs** — not one mega app.

| Front-end | Actor | Phase 1 priority |
|-----------|--------|------------------|
| **Ops** | Dispatch / admin | Build early (dog-food) |
| **Field** | Field worker | Mobile web first-class |
| **Booker** | Booker / customer | After ops + field can run a job |

See [ADR-011](decisions.html).

---

## Core entities

| Entity | Purpose | Phase 1 | Phase 2 notes |
|--------|---------|---------|----------------|
| **org** | Tenant boundary | One org | Same |
| **zone** | Geographic / service area | First-class early (e.g. Howden) | Expand wards |
| **service_type** | What can be booked | At least one type | Clean packs, commercial SKUs, charity free |
| **booker** | Demand-side person | Passenger / customer | Same record |
| **field_worker** | Supply-side person | Driver-shaped + availability | Cleaner-shaped + calendar |
| **job** | Unit of work | Trip-shaped + **price snapshot** | Clean / visit |
| **job_event** | Append-only audit / timeline | **MVP** | Same |
| **job_attachment** | Notes / files / checklist | Schema + notes MVP | Photos + checklists UI |

### service_type (catalogue pricing)

Catalogue defines *how* something is priced and how long it takes. The **job** stores what the customer was actually charged.

| Field (illustrative) | Notes |
|----------------------|--------|
| `name`, `code` | e.g. `saloon`, `clean_2h` |
| `duration_minutes` | Null for open-ended taxi-style; set for packs |
| `pricing_mode` | `estimate` \| `fixed` \| `free` |
| `price_gbp` | Catalogue list price when fixed/free (free = 0) |
| `funding_flag` | e.g. charity-funded hours |
| `prebook_max_days` | Default **14 or 30** (not iCabbi’s 7) |
| `active` | Soft disable |

**Charity free cleans:** normal `service_type` with `price_gbp = 0` and `funding_flag` — no separate code path.

### zone

| Field (illustrative) | Notes |
|----------------------|--------|
| `name`, `code` | Howden Ward first |
| `org_id` | Tenant |
| Geo later | Polygon optional; Phase 1 label + postcode list is enough |

### field_worker — availability early

Even in Phase 1, workers need a **simple availability concept** so cleaning capacity is natural later:

| Field / concept | Phase 1 | Phase 2 |
|-----------------|---------|---------|
| `status` | available / busy / offline | Same |
| **`busy_until`** | Timestamp (nullable) | Same |
| Busy intervals | Optional simple list | Full calendar |
| `last_lat`, `last_lng`, `last_seen_at` | Nullable; map-ready | Tracking later |
| `active_job_id`, `zone_id` | For dispatch + future map | Same |

Availability API uses zone + service duration + worker busy state. Over-book blocked server-side.

### job

| Field | Notes |
|-------|--------|
| `org_id`, `service_type_id`, `zone_id` | Required scoping |
| `status` | Enum — see FSM below |
| `booker_id`, `field_worker_id` | Worker null until assigned |
| **`address_text`** | **Required free-text** for Phase 1 |
| **`lat` / `lng`** | **Optional** — no full geocoding required in Phase 1; fill when known for nav deep-links |
| `scheduled_start` / `scheduled_end` | Pre-book + duration |
| **`price_snapshot`** | **Frozen at booking / confirm** — not live catalogue lookup later |
| `pricing_mode_snapshot` | Mode used at book time |
| `priority` | Lightweight rules |
| `notes` | Free-text; also see attachments |

#### Pricing snapshot ([ADR-009](decisions.html))

**Pricing is stored on the job at booking time (snapshot), not looked up live later.**

- Catalogue `service_type.price_gbp` may change; historical jobs keep their snapshot.  
- Estimate mode: snapshot = estimate returned when booker confirmed.  
- Fixed / free: snapshot = catalogue value at confirm (0 for free).  
- Receipts and ops always show snapshot fields.

#### Address rules ([ADR-009](decisions.html))

- Phase 1: **free-text address is enough** to run the product.  
- `lat`/`lng` optional; when present, field app deep-links to maps.  
- No geocoding pipeline required for Phase 1 exit.

### job_event (MVP)

Append-only. Every transition records:

| Field | Notes |
|-------|--------|
| `job_id`, `org_id` | |
| `from_status`, `to_status` | |
| `actor_type` | `ops` \| `booker` \| `field_worker` \| `system` |
| `actor_id` | Nullable for system |
| `at` | Timestamp (UTC) |
| `note` | Optional |

Powers ops timeline, booker status view, audit, and (with notifications) WhatsApp copy.

### job_attachment (day one)

Notes and files from day one — cleaning will need them immediately in Phase 2.

| Kind | Phase 1 | Phase 2 |
|------|---------|---------|
| Text note | UI + API | Same |
| Photo | Storage stub OK | Cleaner UI |
| Checklist item | Schema | Cleaner UI |

Do not redesign `job` later to “add attachments”.

---

## Status machine (stable enum)

```text
requested
  → quoted            (optional; skip for fixed-price packs)
  → confirmed         (customer accepted / paid / deposit)  ← price_snapshot frozen by here
  → assigned
  → en_route
  → on_site           (UI: in progress / on the way complete)
  → completed

Terminal / exit (validated server-side):
  → cancelled
  → no_show
  → failed
```

### Rules

1. Enum immutable for clients.  
2. Transitions validated **server-side** only.  
3. Every transition → `job_event`.  
4. Fixed-price packs may go `requested → confirmed` (skip `quoted`).  
5. Status changes in Phase 1 trigger **WhatsApp** as primary notification channel ([ADR-010](decisions.html)).

### Suggested allowed transitions (MVP)

| From | To |
|------|-----|
| `requested` | `quoted`, `confirmed`, `cancelled` |
| `quoted` | `confirmed`, `cancelled` |
| `confirmed` | `assigned`, `cancelled` |
| `assigned` | `en_route`, `confirmed` (unassign), `cancelled`, `no_show` |
| `en_route` | `on_site`, `cancelled`, `failed`, `no_show` |
| `on_site` | `completed`, `failed`, `cancelled` |
| terminal states | — |

---

## Capacity & scheduling

| Concept | Phase 1 | Phase 2 |
|---------|---------|---------|
| Worker `busy_until` / busy intervals | **Yes** | Richer calendar |
| Duration on type / job window | **Yes** | Same |
| Availability API | Simple | Strict |
| Over-book | API rejects | Same |

---

## Notifications ([ADR-010](decisions.html))

| Channel | Phase 1 | Notes |
|---------|---------|--------|
| **WhatsApp** | **Primary** for status-change notifications | Shared tyneside-api helpers |
| In-app chat | Later | Do not build for MVP |
| Email / SMS | Optional later | |

Notify booker (and optionally ops/worker) on meaningful transitions: confirmed, assigned, en_route, completed, cancelled, etc.

---

## Phase 1 → Phase 2 hand-off

| Already true in Phase 1 | Phase 2 only adds |
|-------------------------|-------------------|
| `org_id` + three role UIs | Cleaning copy / theme |
| Zones + service_types | Full clean catalogue |
| Price **snapshot** on job | Pack catalogue depth |
| Free-text address + optional lat/lng | Same (geocode optional later) |
| Worker availability hooks | Real cleaner calendars |
| Attachments schema | Checklist + photo UI |
| WhatsApp status notifications | Same channel |
| Seed + demo path | Live Howden jobs |

**Prefer one themed booker** over dual UIs.

---

## Related docs

- [Feature map](features.html) · [Roadmap](roadmap.html) · [Decisions](decisions.html) · [Tasks](tasks.html)  
