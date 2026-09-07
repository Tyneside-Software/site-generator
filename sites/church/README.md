# tyneside.church

Aspirational brand site. Domain bought **on a whim**.

The sketch: multi-faith conversation for Michael’s own education — talking with local church people and friends from other religions. Maybe a **monthly meetup**. Not a congregation and not a registered place of worship.

Listed on the group sketchbook: [tyneside.group/next.html](https://tyneside.group/next.html).

## Bible reading (`/bible`)

First page, last page, then generative jumps. The library publishes **every chapter** of the Catholic Douay-Rheims canon (73 books, including deuterocanon). House modern English is labelled in lilac; chapters we have not rendered yet show the **Douay-Rheims (Challoner)** and say so.

```powershell
# one-time: copy secrets/xai.key.example -> secrets/xai.key and paste the console.x.ai key
.\scripts\tts-bible.ps1            # bookends only, then rebuild church
.\scripts\tts-bible.ps1 -Force     # redo those two MP3s
python scripts/church_bible.py next --count 1
python scripts/church_bible.py reader   # index + every book page
python scripts/church_bible.py check-key
```

Translation: our modern English rendering of the **Douay-Rheims** (public domain). Genesis 1 and Apocalypse 22 are Master’s locked wording in `sites/church/bible-source/custom/`. `next` renders new jump-path chapters in that same style. The full canon is filled from gitignored `sites/church/bible-source/DRC.json` (fetched on first build if missing). Audio uses xAI TTS (`scripts/xai_tts.py`, voice `leo`). Key: gitignored `secrets/xai.key` — see `secrets/README.md`. Default TTS is **first and last pages only**.

## Local preview

```powershell
python -m site_generator church
```

Open `output/church/index.html`.

## When it is ready to stand with the others

1. Set `aspirational=False` on the `church` entry in `src/site_generator/sites.py`.
2. Add a live doorway on `templates/group_home.html`.
3. Point DNS for `tyneside.church` at GitHub Pages.
4. Enable Pages on this repo (`main` / root).
