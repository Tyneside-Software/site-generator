# Feature map

Reference capabilities from [iCabbi research](icabbi.html), mapped to **our** build.  
Domain detail: [Domain model](domain.html).

Legend: **MVP** = Phase 1 target · **P2** = cleaning phase · **Later** · **No** = out of scope for now

---

## Dispatch & back office

| Capability (iCabbi-class) | Ours | Notes |
|---------------------------|------|--------|
| Cloud dispatch / job board | **MVP** | Heart of the product |
| Manual assign + reassign | **MVP** | Primary Phase 1 path |
| Lightweight rules engine | **MVP** | Priority + zone + availability filters — not pure manual forever |
| Intelligent auto-assign | Later | Rules get smarter; no full AI dispatch yet |
| Job history / event log | **MVP** | Append-only `job_event` for timeline + audit |
| 1,000+ config knobs | No | Small config surface first |
| Live map of supply | Later | Design worker status API for map later (lat/lng/last_seen) |
| Workflows / automation % | Later | Measure after manual + rules path works |
| Analytics / reports | Later | Event log enables later reporting |
| Google Fleet Engine | Later | Evaluate only if tracking quality demands it |

---

## Booker / passenger

| Capability | Ours | Notes |
|------------|------|--------|
| Book now | **MVP** | |
| Pre-book | **MVP** | Configurable window; default **14 or 30 days** (not iCabbi’s ~7) |
| Fare / price estimate | **MVP** | Stub OK; result **snapshotted on job** at confirm |
| Service types | **MVP** | Duration + price band on type from day one |
| Status timeline | **MVP** | Always visible; driven by `job_event` |
| Status notifications | **MVP** | **WhatsApp** primary (not in-app chat) |
| Favourites / recent | Later | |
| Live tracking + share trip | Later | Timeline first; map later |
| Card / Apple / Google Pay | Later | Stub or Tide / payment-link patterns |
| Cash | Later | Cleaning less relevant |
| Tipping | Later | |
| Corporate accounts | Later | P2 commercial cleans may need it |
| Accessibility suite | Later | Don’t block MVP; keep UI simple |
| Comms with field worker | **MVP** via WhatsApp | Primary channel — shared API helpers |
| In-app chat | Later | Do not build chat MVP |
| Ratings / receipts / promos | Later | Receipt stub useful early |
| App roaming / Exchange | **No** | |
| Pair & Pay street hail | **No** (P1) | Taxi-only later idea |
| Airport / flight-aware | Later | |

**Phase 2 booker:** same flows; catalogue = cleans; capacity from availability API. Prefer **themed booker** over dual UIs.

---

## Driver / field worker

| Capability | Ours | Notes |
|------------|------|--------|
| Job list / assigned jobs | **MVP** | Mobile-first web |
| Accept / decline | **MVP** | Bidding optional later |
| Explicit status transitions | **MVP** | Server-validated FSM + safety/terminal states |
| Navigation | **MVP** deep-link | **Address free-text required**; lat/lng optional (no geocode pipeline P1) |
| Availability / busy | **MVP** | At least `busy_until` (or simple busy intervals) |
| Earnings stub | **MVP** | Plus **jobs completed today / this week** counters |
| Notes on job | **MVP** | |
| Checklist + photos | Schema **MVP** | Attachments day one; UI can wait for P2 |
| In-app chat | Later | WhatsApp primary |
| Vias / multi-stop | Later | |
| NFC pay | **No** early | |
| Panic / fatigue | Later | Safety states on job FSM first |
| CarPlay / Android Auto | Later | |
| Day/night, TTS | Later | |

**Phase 2 cleaner:** same app; checklist + photos UI; counters still matter.

---

## Network & adjacent (iCabbi)

| Capability | Ours |
|------------|------|
| The Exchange / inter-fleet | **No** |
| Move AI NEMT | **No** early |
| Voice AI / IVR | **No** early (WhatsApp) |
| Driver Pay instant payout | Later |
| Driver Docs onboarding | Later / P2 light |
| Open API | **MVP** (our frontends) |
| Partner marketplace | **No** |

---

## Capacity, zones, cleaning (design in Phase 1)

| Capability | Ours | Notes |
|------------|------|--------|
| Zone as first-class entity | **MVP** | Howden first |
| Duration on service_type / job | **MVP** | Shapes availability endpoints early |
| Fixed price bands | **MVP** model | £30 / 2h packs etc. when types exist |
| Availability endpoint | **MVP** (simple) | Respects busy / capacity; hardens in P2 |
| API-level over-book block | **MVP** intent | Not UI-only |
| Charity free cleans | **P2** type | `price = 0` + funding flag — no separate path |
| Cleaner busy calendar | **P2** | Same availability API |

---

## Status machine (summary)

```text
requested
  → quoted            (optional; skip for fixed-price packs)
  → confirmed
  → assigned
  → en_route
  → on_site           (in_progress label OK in UI)
  → completed
  → cancelled | no_show | failed
```

Every transition → `job_event` (actor, timestamp, optional note).  
Full tables: [Domain model](domain.html).
