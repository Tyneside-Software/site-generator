# Confirmed tech stack

| Layer | Choice |
|-------|--------|
| Backend | **Django 5.x** (Python) |
| Styling | **Tailwind CSS** (django-tailwind or equivalent; CDN allowed for early scaffold) |
| Interactivity | **HTMX + Alpine.js** where useful — no heavy SPA for MVP |
| Database | **PostgreSQL** (SQLite OK for local scaffold only) |
| Auth | Django built-in + custom roles/permissions (django-allauth optional later) |
| Payments | **Stripe** subscriptions + webhooks + Customer Portal |
| Recordings storage | **S3-compatible** via django-storages + boto3 — prefer **Cloudflare R2** |
| Hosting target | **Railway**, **Render**, or **Fly.io** |

## Repo layout (code)

```
lauren/
  config/           # Django project settings & urls
  accounts/         # User + roles
  practitioners/    # Directory + verification
  catalogue/        # Sessions & timetable
  memberships/      # Plans + Stripe entitlement
  recordings/       # Gated library + consent
  core/             # Marketing, legal stubs
  templates/ static/
```

GitHub: [Tyneside-Software/lauren](https://github.com/Tyneside-Software/lauren) (private).

## Future host

`lauren.tyneside.software` — DNS and deploy only when ready to go live.
