# Core MVP features (Phase 1)

1. **User roles** — Client (member), Practitioner, Admin. Organisation accounts later.  
2. **Membership system** with **Stripe** — monthly/annual plans, Customer Portal.  
3. **Practitioner directory** — profiles, specialties, verification badges.  
4. **Monthly timetable / class listing** — members see and join sessions.  
5. **Live sessions (MVP)** — practitioner-provided **Zoom or Teams** links, **only visible to active members**. Later: embed Daily.co or LiveKit.  
6. **Recordings library** — upload or Zoom cloud links; membership-gated; **explicit consent** required.  
7. **Simple admin tools** — approve practitioners and sessions.  
8. **Account UX** — clean signup, login, account management, contact.  
9. **Legal** — strong privacy notice, terms, and disclaimers.  

## Explicitly later than MVP

- Full embedded video stack (Daily.co / LiveKit)  
- Organisation self-serve portals  
- NHS commissioning workflows  
- Heavy SPA client  

## Access rule (join links & recordings)

| Actor | Can see join URL / recording? |
|-------|--------------------------------|
| Anonymous | No |
| Logged-in without active membership | No (upsell) |
| Active member | Yes |
| Practitioner (own session) | Yes |
| Admin | Yes |
