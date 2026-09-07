# tyneside.green

Aspirational brand site. Domain is held; **nothing has started**.

The published sketch:

1. **Easy** — pay [Greenacres](https://greenacresbng.co.uk/) (Stannington, Morpeth) directly for BNG / carbon / trees.
2. **Further** — volunteer planting so money is not the only input.
3. **Stretch** — route gifts via [tyneside.charity](https://tyneside.charity/) for Gift Aid **once that programme is a registered charity** (it is not today).

Working figure on the site: a lifetime of personal CO₂ on the order of **£25k**. That is a sketch number from looking at Greenacres’ BNG pages, not a quote and not a product we have bought.

Listed on the group sketchbook: [tyneside.group/next.html](https://tyneside.group/next.html).

## Local preview

```powershell
python -m site_generator green
```

Open `output/green/index.html`.

## When it is ready to stand with the others

1. Set `aspirational=False` on the `green` entry in `src/site_generator/sites.py`.
2. Add a live doorway on `templates/group_home.html` (and drop it from being “next-only”).
3. Point DNS for `tyneside.green` at GitHub Pages.
4. Enable Pages on this repo (`main` / root).
