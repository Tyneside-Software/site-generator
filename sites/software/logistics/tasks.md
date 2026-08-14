# Tasks & tracker

Update in git. Strategy: **Phase 1 iCabbi-class spine** → **Phase 2 cleaning**.  
See [Overview](overview.html) · [Domain](domain.html) · [Roadmap](roadmap.html) · [Features](features.html) · [Decisions](decisions.html).

**Next execution order:** auth → models/FSM/events → seed → ops → field → booker → WhatsApp → demo polish.

---

## Now — plumbing & docs

- [x] Register `logistics` + site scaffold  
- [x] API brand package  
- [x] Host `logistics.tyneside.software`  
- [x] Docs (domain, features, ADRs, review refinements)  
- [ ] DNS + Pages live  
- [ ] CORS for logistics subdomain  
- [ ] Deploy generator + API  
- [ ] Delete unused `tyneside.logistics` repo (needs `delete_repo` scope)  

---

## Phase 1 — execution order

### 1. Auth + org

- [ ] Implement [ADR-006](decisions.html): org-scoped auth  
- [ ] Ops: session/JWT + email password or magic link  
- [ ] Booker: magic link or OTP  
- [ ] Field: magic link or short-lived PIN/token  
- [ ] Enforce `org_id` on all tenant data access  

### 2. Core models + FSM + events

- [ ] `org`, `zone`, `service_type`, `booker`, `field_worker`, `job`, `job_event`, `job_attachment`  
- [ ] Server-validated status transitions  
- [ ] Every transition → `job_event`  
- [ ] **`price_snapshot`** (+ mode) frozen at confirm — not live catalogue lookup  
- [ ] **`address_text` required**; `lat`/`lng` optional (no geocoding required)  
- [ ] Worker **`busy_until`** (or simple busy intervals)  
- [ ] Availability endpoint (simple)  
- [ ] Light assign rules (priority + zone + availability)  
- [ ] Worker status fields map-ready  

### 3. Seed data (first-class deliverable)

- [ ] One org, 3–5 workers, 10–15 jobs across statuses  
- [ ] Scripted demo path documented  
- [ ] Re-runnable seed command  

### 4. Ops console (minimal)

- [ ] Day board / list: status, date, zone, worker filters  
- [ ] One-click assign + reassign  
- [ ] Job detail + full event timeline  
- [ ] Minimal type + zone admin  

### 5. Field worker mobile web

- [ ] Mobile-optimised list + detail  
- [ ] Status buttons + confirmation  
- [ ] Deep-link nav from address / optional lat/lng  
- [ ] Today / this week completed counters  
- [ ] Notes; photo stub OK  

### 6. Booker flow

- [ ] Book now + pre-book (14/30 day window config)  
- [ ] Estimate / fixed price → snapshot on job  
- [ ] Status timeline  
- [ ] No in-app chat  

### 7. WhatsApp status notifications

- [ ] On meaningful transitions, notify via WhatsApp helpers  
- [ ] Soft-fail if credentials missing  
- [ ] Booker (and optional ops/worker) targets  

### 8. Demo polish

- [ ] **10 jobs E2E with zero spreadsheet use**  
- [ ] Mobile browser happy path for field  
- [ ] OpenAPI for ops, booker, field  
- [ ] Thin payment link / Tide pattern if needed for “closed” story  

---

## Phase 1 exit bar (must all be true)

- [ ] Operator completes **10 jobs** end-to-end with **zero spreadsheet use**  
- [ ] Every status change produces a `job_event`  
- [ ] WhatsApp path implemented (credentials optional at runtime)  
- [ ] Three role UIs exist (even if thin)  
- [ ] OpenAPI documented for three actors  

---

## Phase 2 — Cleaning bookings

- [ ] Catalogue depth for packs; jobs still snapshot price  
- [ ] Charity free type (price 0 + funding flag)  
- [ ] Cleaner capacity calendar; API over-book block  
- [ ] Themed booker (prefer single UI)  
- [ ] Checklist + photos UI  
- [ ] **First real Howden clean fully closed in system** (incl. payment/receipt path)  

---

## Later / backlog

- [ ] Geocoding pipeline  
- [ ] Live map UI  
- [ ] In-app chat  
- [ ] Utilisation / no-show / time-to-assign dashboards  
- [ ] Multi-tenant sales readiness  

---

## How to add a task

1. Edit `sites/logistics/docs/tasks.md`.  
2. `python -m site_generator logistics`.  
3. Merge to `main` → CI publishes Pages.  
