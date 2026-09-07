# Holy Bible — World English Bible

**Live:** https://tyneside.software/bible/

Public-domain modern English. Same reader chrome as [michael-book](https://tyneside.software/michael-book/).

## Build

```powershell
cd C:\\Users\\MichaelThomson\\source\\TTS
python scripts/build_bible.py
python -m site_generator software
```

Writes `sites/software/static/bible/index.html`, `overview.html`, and `books/*.html`.
Book summaries live in `sites/software/bible-source/about.json` (merged into overview.json at build).
Chapter guides live in `sites/software/bible-source/chapter-guides/` (one note per chapter).
The site generator copies `static/` into `output/software/bible/`.
Push `site-generator` `main` and CI publishes tyneside.software. If the token is missing: `.\scripts\deploy-pages.ps1 software`.

## Translation

[World English Bible](https://worldenglish.bible/) — public domain modern English
from the American Standard Version, with paragraph and poetic line data from
[TehShrike/world-english-bible](https://github.com/TehShrike/world-english-bible).
Sixty-six book Protestant canon. Not NIV/NLT/ESV.
