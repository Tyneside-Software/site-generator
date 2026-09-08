# tyneside.beer

Aspirational brand site. Domain was bought as a **joke**. The idea behind it is real enough to sketch.

Dropship beer from [Dynamite Valley](https://www.dynamitevalley.co.uk/) (Ponsanooth, Cornwall) — a brewery a friend of Michael’s owns. Not produced on Tyneside.

The money idea: order through Tyneside, **+2% to [tyneside.charity](https://tyneside.charity/)**, the actual order goes to the friend’s brewery. Not live — no till, no licence on this brand.

Listed on the group sketchbook: [tyneside.group/next.html](https://tyneside.group/next.html).

## Local preview

```powershell
python -m site_generator beer
```

Open `output/beer/index.html`.

## When it is ready to stand with the others

1. Set `aspirational=False` on the `beer` entry in `src/site_generator/sites.py`.
2. Add a live doorway on `templates/group_home.html`.
3. Point DNS for `tyneside.beer` at GitHub Pages.
4. Enable Pages on this repo (`main` / root).
5. Alcohol sales need proper UK licensing before any checkout exists. This page is not a shop.
