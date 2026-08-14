# Roadmap

Living plan. Detail: [Tasks](tasks.html) · model: [Domain](domain.html) · research: [iCabbi](icabbi.html).

---

## Phase 0 — Platform plumbing

Prioritise **real host + CORS** so development targets production URLs early.

- [x] Brand site + docs + app shell  
- [x] `tyneside-api` brand package `/v1/logistics/*`  
- [x] Domain: **logistics.tyneside.software**  
- [x] Pages repo created  
- [ ] DNS + GitHub Pages custom domain **live**  
- [ ] Cloud Run `CORS_ORIGINS` includes logistics subdomain  
- [ ] Deploy generator + API to production  

---

## Phase 1 — iCabbi-style clone (MVP)

**Definition of done (sharp):**  
**Operator can complete 10 jobs end-to-end with zero spreadsheet use** — on mobile browser where it matters for field; every status change writes `job_event`; WhatsApp notified when configured; OpenAPI covers ops, booker, and field.

### Priority order to execute next

| # | Focus | Notes |
|---|--------|--------|
| **1** | **Auth ADR + org-scoped auth** | Implement basic multi-tenant auth ([ADR-006](decisions.html)) |
| **2** | **Core models + status machine + job_events** | Incl. price snapshot, address text, attachments schema |
| **3** | **Seed data** | First-class deliverable — one org, workers, jobs across statuses |
| **4** | **Minimal ops console** | List + assign + timeline (dog-food) |
| **5** | **Field worker mobile web flow** | First-class, not optional |
| **6** | **Booker flow** | Book now / pre-book + status timeline |
| **7** | **WhatsApp status notifications** | Primary channel ([ADR-010](decisions.html)) |
| **8** | **Polish end-to-end demo path** | Scripted path over seed data |

### Cross-cutting (bake into steps 2–8)

- Worker availability (`busy_until` / simple busy)  
- Three thin UIs — not one mega UI  
- Optional lat/lng only; no geocoding required  
- Language mapping for UI strings (taxi vs cleaning)  

### Explicitly deferred in Phase 1

Exchange / roaming, NEMT, Voice IVR, NFC, CarPlay, in-app chat, full geocoding, live map UI, multi-tenant **sales**.

---

## Phase 2 — Cleaning bookings

**Definition of done (sharp):**  
**First real Howden clean fully closed in system, including any payment/receipt path** (using job `price_snapshot`).

### Emphasise

1. Service catalogue = list duration + price; jobs still snapshot.  
2. Capacity rules block over-booking at API (cleaner busy calendar).  
3. Prefer **themed booker** over dual UIs.  
4. Checklist + photos on existing attachments.  
5. Charity free = type with list price 0 + funding flag.  

---

## Phase 3+ (ideas only)

- Stronger maps / ETAs / geocoding pipeline  
- Corporate accounts, ratings maturity  
- Multi-tenant **sales** readiness — parked until Howden volume  

---

## Success metrics

| Phase | Signal |
|-------|--------|
| 0 | Docs + API reachable on real logistics host |
| **1** | **Operator completes 10 jobs E2E with zero spreadsheet use** |
| **2** | **First real Howden clean fully closed in system** (incl. payment/receipt path) |
| Later | Utilisation, no-show rate, time-to-assign |

---

## Highest-leverage refinements (accepted)

1. Stronger domain foundations early: auth, org, events, capacity hooks  
2. Robust status + **price snapshot** so Phase 2 needs no surgery  
3. WhatsApp + mobile web as **first-class**  
4. Demo-driven Phase 1 exit (seed + 10-job path)  
