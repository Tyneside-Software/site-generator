# tyneside.store

Aspirational brand site. **Not a Tyneside till.**

A friend’s shop: [RST Wholesale](https://rst-wholesale.com/). This site mirrors the public catalogue so people can browse with Tyneside framing; every product and collection **links through to RST**.

Later stretch (not happening on those click-throughs): take the order here, add 2%, donate that 2% to [tyneside.charity](https://tyneside.charity/). Gift Aid only if that programme is a registered charity — it is not today.

Listed on the group sketchbook: [tyneside.group/next.html](https://tyneside.group/next.html).

## Catalogue sync

```powershell
python scripts/sync_rst_catalog.py
python -m site_generator store
```

Open `output/store/index.html`.
