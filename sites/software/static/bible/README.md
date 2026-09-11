# Holy Bible — World English Bible

**Live:** https://tyneside.software/bible/

Public-domain modern English. Scripture-style reader chrome with sidebar navigation.

## Build

```powershell
cd C:\\Users\\MichaelThomson\\source\\TTS
python scripts/build_bible.py
python -m site_generator software
```

Writes `sites/software/static/bible/index.html`, `overview.html`, and `books/*.html`.
Book summaries live in `sites/software/bible-source/about.json` (merged into overview.json at build).
Chapter guides live in `sites/software/bible-source/chapter-guides/` (one note per chapter).
Chapter audio URLs live in `sites/software/static/bible/audio-manifest.json`
(refresh with `python scripts/fetch_bible_audio.py`). Files are streamed from
eBible.org — the zip is ~5.4 GB and does not belong in GitHub Pages.
The site generator copies `static/` into `output/software/bible/`.
Push `site-generator` `main` and CI publishes tyneside.software. If the token is missing: `.\scripts\deploy-pages.ps1 software`.

## Translation

[World English Bible](https://worldenglish.bible/) — public domain modern English
from the American Standard Version, with paragraph and poetic line data from
[TehShrike/world-english-bible](https://github.com/TehShrike/world-english-bible).
Sixty-six book Protestant canon. Not NIV/NLT/ESV.

## Audio

Each chapter has play and download. Source:
[Winfred Wardell Henson](https://ebible.org/eng-web/audio/) reading the classic
World English Bible. Professional voice artist, one narrator, public domain.
LibriVox 4.4/5 (97 ratings). Matches the on-page WEB text.
