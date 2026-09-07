# tyneside.garden

Aspirational brand site. Domain is held; **not a public booking yet**.

This is **paid local gardening / outdoor house maintenance** — not
[tyneside.green](https://tyneside.green/) (carbon, Greenacres, volunteers).

The practical start: a person who already does house maintenance for Michael
could take on gardens.

Listed on the group sketchbook: [tyneside.group/next.html](https://tyneside.group/next.html).

## Local preview

```powershell
python -m site_generator garden
```

Open `output/garden/index.html`.

## When it is ready to stand with the others

1. Set `aspirational=False` on the `garden` entry in `src/site_generator/sites.py`.
2. Add a live doorway on `templates/group_home.html`.
3. Point DNS for `tyneside.garden` at GitHub Pages.
4. Enable Pages on this repo (`main` / root).
