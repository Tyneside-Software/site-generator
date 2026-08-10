# iCabbi research (reference product)

**Status:** Internal product research for Tyneside Logistics  
**Also styled:** “icabby” / “iCabby” (common spoken forms)  
**Role for us:** Phase 1 **capability clone target** — not a partnership claim, not reverse-engineering their code. We study *what fleets and passengers get*, then build our own stack under `logistics.tyneside.software` + `tyneside-api`.

> This page captures Master’s research notes, structured for build planning. Facts are approximate (company marketing, public statements over time). Re-check before external claims.

---

## One-line summary

**iCabbi is cloud taxi / private hire (PHV) dispatch and fleet management software.**  
It is **not** a consumer ride-hail brand like Uber or Lyft. Local fleets run on iCabbi; passengers usually use a **white-labelled app** branded as their local company. Drivers use a shared **iCabbi Driver App**.

---

## Company background

| Topic | Notes |
|-------|--------|
| **Founded** | Idea ~2009; company often dated 2009/2010 |
| **Origin** | Dublin / Howth area, Ireland (Sutton Cross / Eastpoint Business Park) |
| **Founder** | Gavan Walsh (co-founder & long-time CEO). Idea: lost on a walk in remote Portugal with then-pregnant partner — wanted nearby taxis on a map and one-tap booking |
| **Co-founders** | Niall O’Callaghan (technical), Bob Nixon |
| **Ownership** | June 2018: RCI Bank and Services (Groupe Renault; later Mobilize mobility brand) took a **75%** majority stake. Positioned as a Renault/Mobilize company |
| **Leadership** | Walsh stepped down as CEO early 2023; **Mick Tope** current CEO (as of research) |
| **HQ** | Dublin, Ireland |
| **Other presence** | Sheffield (UK), Ottawa (Canada), Atlanta / Woodstock area (USA), elsewhere |
| **Headcount** | Roughly 50–200 (LinkedIn-scale figures ~140+) |
| **Model** | SaaS for taxi/PHV operators; claimed high uptime (**99.999%**); automation (some fleets **90%+** booking automation); driver retention + passenger UX |

### Scale (approximate, company statements over time)

- ~**100,000** taxis / vehicles powered  
- **800+** fleets (800th fleet ~2020)  
- **1B+** trips/bookings by late 2022  
- Markets: Ireland, UK, USA, Canada, Australia, New Zealand, Finland; expansion via partners (e.g. Nordics / Cabonline; Brazil via acquisition)  
- **Taxi Alliance** (JV with independent UK/Ireland fleets, ~2022): 500+ companies, tens of thousands of licenses  

**Vision (theirs):** put traditional taxi companies at the centre of mobility.

---

## How the three sides experience it

### Passengers

1. Download a **local fleet’s branded app** (powered by iCabbi).  
2. Book / track / pay in a way comparable to ride-hail — but with **licensed local taxis/PHVs**.  
3. **App Roaming / The Exchange:** same familiar app can work in **200+** locations via partner fleets (UK/Europe; US cities expanding).

Claimed: app users take **~2.2×** more trips annually than phone bookers.

### Drivers

- Log into **iCabbi Driver App** (iOS & Android; Coolnagour Ltd / iCabbi on stores) with **fleet credentials**.  
- Accept / bid on jobs, navigate, chat, track earnings, manage status.  
- Store reviews mixed (~**3–3.4** stars often): features praised; navigation quirks, bugs, or penalties criticised.

### Fleets (operators)

- Full **back-office** control: dispatch, automation, analytics, customer/driver retention tools.  
- Highly configurable cloud dispatch (marketing: **1,000+** real-time configuration points).  
- Integrates **Google Fleet Engine** for advanced tracking/ETAs (partnership from ~2023+).

---

## Core products (feature inventory for our clone)

### 1. Dispatch system

- Cloud dispatch engine; supply/demand matching  
- Automation + workflows + real-time ops  
- Customisation / configuration depth  
- Google Fleet Engine integration (reference architecture — we decide later what maps stack we use)

### 2. Passenger app (white-label)

| Area | Capabilities (reference) |
|------|---------------------------|
| Accounts | Quick sign-in; personal / business accounts |
| Booking | Book now; pre-book (up to ~7 days); airport / flight-aware options |
| Pricing | Fare estimates; multiple vehicle types (incl. accessible); recent / favourites |
| Live trip | Live tracking, Google-powered ETAs, share trip, vehicle details |
| Payments | Card, Apple Pay, Google Pay, cash; tipping; corporate accounts |
| Accessibility | Voice, TTS, contrast, font size, dark mode |
| Engagement | Chat with driver, ratings/reviews, digital receipts, promo codes, trip history |
| Newer (2025–2026 redesign notes) | Live Activities; improved payments; **Pair & Pay** (street hail + app pay); live meter tracking; better vehicle selector with upfront pricing |

### 3. Driver app

- Job bidding + maps  
- Turn-by-turn Google navigation  
- Passenger live location (Fleet Engine narrative)  
- Status management, earnings dashboard, chat  
- Vias (extra stops)  
- NFC payments  
- Panic / fatigue tools  
- CarPlay & Android Auto  
- Ratings; day/night; TTS personalisation  

Goal of the product: help drivers **maximise earnings** and **reduce downtime**.

### 4. Network layer — The Exchange (~May 2025)

Inter-fleet networking:

- **Dispatch networking** — share excess demand  
- **App networking** — passenger app roaming nationwide/internationally  
- **Phone-call networking**  

Ambition: keep work inside traditional taxi sector vs pure ride-hail. Scale notes from research: potential to pool ~**60,000** taxis UK/Ireland; **32,000+** cars cited in mid-2026 posts.

### 5. Adjacent tools

| Product | Role |
|---------|------|
| **Move AI** | Route optimisation for **NEMT** (non-emergency medical transport) |
| **Voice AI / voice** | Automate call centres / IVR |
| **Driver Pay** | Instant / scheduled payouts |
| **Driver Docs** | Onboarding / compliance docs |
| **Business / corporate** | Account billing for organisations |
| **Open API** | Integrations |
| **Partner marketplace** | Ecosystem |

Acquisitions (capability expansion, not a clone checklist): Mobile Knowledge (N. America), Original Software (Brazil), Moovex, Javelin, etc.

---

## Notable events & context

- **Google partnership (2023+):** Fleet Engine for real-time tracking / ETAs.  
- **Data incident (2024):** Unprotected AWS file from a **customer data migration** exposed names, emails, phones, IDs of nearly **300k** UK/Ireland passengers (incl. high-profile domains). Found by researcher; iCabbi: human error, restricted access, deleted data, notified fleets; stated **core system was not hacked**.  
  → **Lesson for us:** migration artefacts, least-privilege storage, no public buckets, passenger PII design from day one.  
- Marketing: **“Love Local Taxi & Private Hire”** — independent fleets over global ride-hail.  
- Continuous product updates; passenger app redesign emphasised into 2026.

---

## What we are *not* doing

- Claiming affiliation with iCabbi, Renault, or Mobilize  
- Copying their branding, apps, or proprietary code  
- Building “App Roaming / The Exchange” at UK national scale on day one  
- Multi-country fleet SaaS out of the box  

We **are** using this research as a **product capability map** for Phase 1.

---

## Mapping to Tyneside Logistics phases

| iCabbi area | Phase 1 (generic spine) | Phase 2 (cleaning bookings) |
|-------------|-------------------------|------------------------------|
| Dispatch | Job board, manual assign + light rules, `job_event` timeline | Same; zones + capacity stricter |
| Passenger app | Booker web; status timeline; WhatsApp not in-app chat | Themed booker; fixed packs first-class |
| Driver app | Field worker mobile web; FSM; nav deep-link; today/week counters | Cleaner skin; checklist + photos UI |
| Payments | Stub / link | Tide / Tyneside patterns |
| Fleet back-office | Ops day board (dog-food first) | Cleaning day board |
| Pre-book window | Configurable 14–30 days default | Same (7 days too short for packs) |
| Exchange / roaming | Out of scope | N/A |
| NEMT Move AI | Out of scope | Optional later |
| Voice / IVR | Out of scope | WhatsApp primary |

Authoritative model: [Domain](domain.html) · prioritisation: [Features](features.html) · order: [Roadmap](roadmap.html).
