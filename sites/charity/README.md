# tyneside.charity

Welcome-home free cleans programme (not a registered charity yet).

## Public tracker

Source of truth: **`tracker.yaml`**

| Field | Meaning |
|-------|---------|
| `donations[]` | Public donor list: `date`, `name`, `location`, `amount_gbp` |
| `cleans_delivered` | Anonymous count of 2-hour cleans completed |
| `gbp_per_clean` | Promise unit (£30 → one 2-hour clean) |

At build time the site computes:

- **Raised** = sum of donation amounts  
- **Cleans paid for** = floor(raised ÷ 30)  
- **Still to deliver** = paid for − delivered  

### Manual update (target: within 3 business days)

1. Confirm the payment in **Tide** (Tyneside Cleaning account).  
2. Add a row under `donations` in `tracker.yaml`.  
3. When a free clean is completed, increment `cleans_delivered` (no family details).  
4. Set `updated` to today’s date.  
5. Rebuild and deploy:

```powershell
python -m site_generator charity
# then deploy / push via the usual Pages workflow
```

## Tide Instant Checkout

Paste Instant Checkout URLs into `static/donate-config.js` → `tideLinks`.

**Payment reference:** Tide Instant Checkout does **not** accept a custom reference via URL.  
Create items named clearly (e.g. `Welcome-home clean donation · £30`).  
Donors enter name/location on the site; we match amount + date in Tide and list them from the donor line / WhatsApp within 3 business days.
