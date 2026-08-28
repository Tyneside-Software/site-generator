# Holy Bible — World English Bible

**Live:** https://tyneside.software/bible/

Public-domain modern English. Same reader chrome as [michael-book](https://tyneside.software/michael-book/).

## Build

```powershell
cd C:\Users\MichaelThomson\source\TTS
python scripts/build_bible.py
python -m site_generator software
```

Writes `sites/software/static/bible/index.html` and `books/*.html`.
The site generator copies `static/` into `output/software/bible/`.
Push `site-generator` `main` and CI publishes tyneside.software.

## Translation

[World English Bible](https://worldenglish.bible/) — public domain modern English
from the American Standard Version, with paragraph and poetic line data from
[TehShrike/world-english-bible](https://github.com/TehShrike/world-english-bible).
Sixty-six book Protestant canon. Not NIV/NLT/ESV.
