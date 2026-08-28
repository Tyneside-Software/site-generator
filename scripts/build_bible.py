"""Build the tyneside.software/bible reader from the World English Bible.

Public-domain modern English. Same chrome as michael-book: sidebar nav,
serif reading column, gold on dark. One HTML file per book (the whole
Bible is ~780k words — too large for a single page).

Usage:
  python scripts/build_bible.py
"""
from __future__ import annotations

import json
import re
import shutil
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "sites" / "software" / "bible-source" / "web"
CHURCH_WEB = ROOT / "sites" / "church" / "bible-source" / "web"
OUT_DIR = ROOT / "sites" / "software" / "static" / "bible"
BOOKS_DIR = OUT_DIR / "books"
WEB_URL = "https://raw.githubusercontent.com/TehShrike/world-english-bible/master/json/{stem}.json"
UA = "tyneside.software-bible/1.0 (public-domain World English Bible reader)"

# name, json stem, testament, group, aliases
BOOKS: list[tuple[str, str, str, str, list[str]]] = [
    ("Genesis", "genesis", "ot", "Law", ["gen", "ge", "gn"]),
    ("Exodus", "exodus", "ot", "Law", ["exod", "exo", "ex"]),
    ("Leviticus", "leviticus", "ot", "Law", ["lev", "le", "lv"]),
    ("Numbers", "numbers", "ot", "Law", ["num", "nu", "nm"]),
    ("Deuteronomy", "deuteronomy", "ot", "Law", ["deut", "de", "dt"]),
    ("Joshua", "joshua", "ot", "History", ["josh", "jos", "jsh"]),
    ("Judges", "judges", "ot", "History", ["judg", "jdg", "jg"]),
    ("Ruth", "ruth", "ot", "History", ["rth", "ru"]),
    ("1 Samuel", "1samuel", "ot", "History", ["1sam", "1sa", "1sm", "isamuel"]),
    ("2 Samuel", "2samuel", "ot", "History", ["2sam", "2sa", "2sm", "iisamuel"]),
    ("1 Kings", "1kings", "ot", "History", ["1kgs", "1ki", "1k", "ikings"]),
    ("2 Kings", "2kings", "ot", "History", ["2kgs", "2ki", "2k", "iikings"]),
    ("1 Chronicles", "1chronicles", "ot", "History", ["1chr", "1ch", "ichronicles"]),
    ("2 Chronicles", "2chronicles", "ot", "History", ["2chr", "2ch", "iichronicles"]),
    ("Ezra", "ezra", "ot", "History", ["ezr"]),
    ("Nehemiah", "nehemiah", "ot", "History", ["neh", "ne"]),
    ("Esther", "esther", "ot", "History", ["est", "es"]),
    ("Job", "job", "ot", "Wisdom", ["jb"]),
    ("Psalms", "psalms", "ot", "Wisdom", ["ps", "psa", "psalm", "pss"]),
    ("Proverbs", "proverbs", "ot", "Wisdom", ["prov", "pro", "prv"]),
    ("Ecclesiastes", "ecclesiastes", "ot", "Wisdom", ["eccl", "ecc", "eccles"]),
    ("Song of Solomon", "songofsolomon", "ot", "Wisdom", ["song", "sos", "so", "cant"]),
    ("Isaiah", "isaiah", "ot", "Prophets", ["isa", "is"]),
    ("Jeremiah", "jeremiah", "ot", "Prophets", ["jer", "je"]),
    ("Lamentations", "lamentations", "ot", "Prophets", ["lam", "la"]),
    ("Ezekiel", "ezekiel", "ot", "Prophets", ["ezek", "eze", "ezk"]),
    ("Daniel", "daniel", "ot", "Prophets", ["dan", "da", "dn"]),
    ("Hosea", "hosea", "ot", "Prophets", ["hos", "ho"]),
    ("Joel", "joel", "ot", "Prophets", ["jl"]),
    ("Amos", "amos", "ot", "Prophets", ["am"]),
    ("Obadiah", "obadiah", "ot", "Prophets", ["obad", "ob"]),
    ("Jonah", "jonah", "ot", "Prophets", ["jon", "jnh"]),
    ("Micah", "micah", "ot", "Prophets", ["mic", "mc"]),
    ("Nahum", "nahum", "ot", "Prophets", ["nah", "na"]),
    ("Habakkuk", "habakkuk", "ot", "Prophets", ["hab", "hb"]),
    ("Zephaniah", "zephaniah", "ot", "Prophets", ["zeph", "zep", "zp"]),
    ("Haggai", "haggai", "ot", "Prophets", ["hag", "hg"]),
    ("Zechariah", "zechariah", "ot", "Prophets", ["zech", "zec", "zc"]),
    ("Malachi", "malachi", "ot", "Prophets", ["mal", "ml"]),
    ("Matthew", "matthew", "nt", "Gospels", ["matt", "mt", "mat"]),
    ("Mark", "mark", "nt", "Gospels", ["mrk", "mk", "mr"]),
    ("Luke", "luke", "nt", "Gospels", ["luk", "lk"]),
    ("John", "john", "nt", "Gospels", ["joh", "jhn", "jn"]),
    ("Acts", "acts", "nt", "History", ["act", "ac"]),
    ("Romans", "romans", "nt", "Letters", ["rom", "ro", "rm"]),
    ("1 Corinthians", "1corinthians", "nt", "Letters", ["1cor", "1co", "icorinthians"]),
    ("2 Corinthians", "2corinthians", "nt", "Letters", ["2cor", "2co", "iicorinthians"]),
    ("Galatians", "galatians", "nt", "Letters", ["gal", "ga"]),
    ("Ephesians", "ephesians", "nt", "Letters", ["eph", "ep"]),
    ("Philippians", "philippians", "nt", "Letters", ["phil", "php", "pp"]),
    ("Colossians", "colossians", "nt", "Letters", ["col", "co"]),
    ("1 Thessalonians", "1thessalonians", "nt", "Letters", ["1thess", "1th", "ithessalonians"]),
    ("2 Thessalonians", "2thessalonians", "nt", "Letters", ["2thess", "2th", "iithessalonians"]),
    ("1 Timothy", "1timothy", "nt", "Letters", ["1tim", "1ti", "itimothy"]),
    ("2 Timothy", "2timothy", "nt", "Letters", ["2tim", "2ti", "iitimothy"]),
    ("Titus", "titus", "nt", "Letters", ["tit", "ti"]),
    ("Philemon", "philemon", "nt", "Letters", ["phlm", "phm", "pm"]),
    ("Hebrews", "hebrews", "nt", "Letters", ["heb", "he"]),
    ("James", "james", "nt", "Letters", ["jas", "jm"]),
    ("1 Peter", "1peter", "nt", "Letters", ["1pet", "1pe", "1pt", "ipeter"]),
    ("2 Peter", "2peter", "nt", "Letters", ["2pet", "2pe", "2pt", "iipeter"]),
    ("1 John", "1john", "nt", "Letters", ["1jn", "1jo", "1jhn", "ijohn"]),
    ("2 John", "2john", "nt", "Letters", ["2jn", "2jo", "2jhn", "iijohn"]),
    ("3 John", "3john", "nt", "Letters", ["3jn", "3jo", "3jhn", "iiijohn"]),
    ("Jude", "jude", "nt", "Letters", ["jud", "jd"]),
    ("Revelation", "revelation", "nt", "Revelation", ["rev", "re", "apoc", "apocalypse"]),
]

def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _fetch(stem: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    church = CHURCH_WEB / f"{stem}.json"
    if church.is_file() and church.stat().st_size > 200:
        shutil.copy2(church, dest)
        return dest
    url = WEB_URL.format(stem=stem)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        dest.write_bytes(resp.read())
    return dest


def ensure_sources() -> None:
    SRC_DIR.mkdir(parents=True, exist_ok=True)
    missing = []
    for _name, stem, *_rest in BOOKS:
        path = SRC_DIR / f"{stem}.json"
        if not path.is_file() or path.stat().st_size < 200:
            missing.append(stem)
    if not missing:
        return
    print(f"Fetching {len(missing)} World English Bible JSON files…")
    errors: list[str] = []

    def one(stem: str) -> tuple[str, Exception | None]:
        try:
            _fetch(stem, SRC_DIR / f"{stem}.json")
            return stem, None
        except Exception as exc:  # noqa: BLE001
            return stem, exc

    with ThreadPoolExecutor(max_workers=8) as pool:
        futs = [pool.submit(one, stem) for stem in missing]
        for fut in as_completed(futs):
            stem, err = fut.result()
            if err:
                errors.append(f"{stem}: {err}")
            else:
                print(f"  {stem}.json")
    if errors:
        raise SystemExit("Failed to fetch:\n  " + "\n  ".join(errors))


def vn_html(chapter: int, verse: int, first: bool) -> str:
    cls = "vn first" if first else "vn"
    vid = f"c-{chapter}-v-{verse}"
    return (
        f'<span class="{cls}" id="{vid}">'
        f'<a href="#{vid}">{verse}</a></span>'
    )


def parse_book(tokens: list[dict]) -> dict[int, dict]:
    """Return {chapter: {verses, words, html}} preserving WEB paragraphs/stanzas."""
    chapters: dict[int, dict] = {}
    mode: str | None = None
    buf: list[str] = []
    last_verse: int | None = None
    current_ch: int | None = None
    verse_first = True

    def ensure(ch: int) -> dict:
        if ch not in chapters:
            chapters[ch] = {"verses": set(), "words": 0, "parts": []}
        return chapters[ch]

    def flush() -> None:
        nonlocal buf, last_verse, verse_first
        if current_ch is None or not buf:
            buf = []
            return
        html = "".join(buf).strip()
        buf = []
        last_verse = None
        verse_first = True
        if not html:
            return
        tag = "p class=\"stanza\"" if mode == "stanza" else "p"
        close = "p"
        chapters[current_ch]["parts"].append(f"<{tag}>{html}</{close}>")

    def add_text(ch: int, verse: int, text: str, linebreak: bool = False) -> None:
        nonlocal last_verse, current_ch, verse_first
        if current_ch != ch:
            flush()
            current_ch = ch
        rec = ensure(ch)
        rec["verses"].add(verse)
        rec["words"] += len(text.split())
        piece = escape(re.sub(r"\s+", " ", text).strip())
        if not piece and not linebreak:
            return
        if verse != last_verse:
            marker = vn_html(ch, verse, verse_first)
            verse_first = False
            last_verse = verse
            if buf and not buf[-1].endswith((" ", ">")):
                buf.append(" ")
            buf.append(marker)
        if piece:
            if buf and not buf[-1].endswith((" ", ">")):
                buf.append(" ")
            buf.append(piece)
        if linebreak:
            buf.append("<br>\n")

    for tok in tokens:
        kind = tok.get("type")
        if kind in ("paragraph start", "stanza start"):
            flush()
            mode = "stanza" if kind.startswith("stanza") else "para"
        elif kind in ("paragraph end", "stanza end", "break"):
            flush()
            mode = None
        elif kind == "line break":
            if buf:
                buf.append("<br>\n")
        elif kind in ("paragraph text", "line text"):
            ch = int(tok["chapterNumber"])
            verse = int(tok["verseNumber"])
            add_text(ch, verse, tok.get("value") or "", linebreak=False)

    flush()
    return chapters


def load_book(stem: str) -> dict[int, dict]:
    tokens = json.loads((SRC_DIR / f"{stem}.json").read_text(encoding="utf-8"))
    chapters = parse_book(tokens)
    if not chapters:
        raise ValueError(f"No chapters in {stem}")
    return chapters


def page_shell(
    title: str,
    description: str,
    asset_prefix: str,
    body_attrs: str,
    toggle_label: str,
    aside: str,
    main: str,
) -> str:
    css = f"{asset_prefix}bible.css"
    canon = f"{asset_prefix}canon.js"
    js = f"{asset_prefix}bible.js"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}">
  <meta name="theme-color" content="#0f1419">
  <link rel="stylesheet" href="{css}">
  <script defer src="{canon}"></script>
  <script defer src="{js}"></script>
</head>
<body {body_attrs}>
  <a class="skip" href="#main">Skip to reading</a>
  <button type="button" class="nav-toggle" id="nav-toggle" aria-expanded="false" aria-controls="chapter-side">{escape(toggle_label)}</button>
  <div class="nav-backdrop" id="nav-backdrop" hidden></div>
  <aside class="side" id="chapter-side" aria-label="Navigation">
    <button type="button" class="nav-close" id="nav-close" aria-label="Close navigation">×</button>
    {aside}
  </aside>
  <div class="shell">
    <div class="side-spacer" aria-hidden="true"></div>
    <main class="main" id="main">
      {main}
    </main>
  </div>
  <a class="top" href="#">Top</a>
</body>
</html>
"""


def write_canon(stats: list[dict]) -> None:
    payload = [
        {
            "name": s["name"],
            "slug": s["stem"],
            "chapters": s["chapter_count"],
            "testament": s["testament"],
            "group": s["group"],
            "aliases": s["aliases"],
        }
        for s in stats
    ]
    (OUT_DIR / "canon.js").write_text(
        "window.BIBLE_CANON = " + json.dumps(payload, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )


def grouped_book_nav_fixed(stats: list[dict], current: str | None = None) -> str:
    """Book nav with OT/NT group labels, History split correctly."""
    parts: list[str] = []
    last_key = None
    for s in stats:
        key = (s["testament"], s["group"])
        if key != last_key:
            prefix = "OT · " if s["testament"] == "ot" else "NT · "
            parts.append(f'<div class="nav-group">{prefix}{escape(s["group"])}</div>')
            last_key = key
        active = " is-active" if current == s["stem"] else ""
        href = f'{s["stem"]}.html' if current else f'books/{s["stem"]}.html'
        filt = escape(s["name"] + " " + s["stem"] + " " + " ".join(s["aliases"]))
        parts.append(
            f'<a class="nav-item book-link{active}" href="{href}" data-filter="{filt}">'
            f'<span class="t">{escape(s["name"])}</span>'
            f'<span class="ch">{s["chapter_count"]}</span></a>'
        )
    return "".join(parts)


def jump_block() -> str:
    return """
      <form class="jump" id="jump-form" action="#" method="get">
        <input id="jump-input" type="search" placeholder="John 3:16" autocomplete="off" aria-label="Jump to a verse">
        <button type="submit">Go</button>
      </form>
      <p class="jump-err" id="jump-err" role="status"></p>
      <input class="filter" id="nav-filter" type="search" placeholder="Filter books or chapters" aria-label="Filter navigation">
    """


def render_index(stats: list[dict], total_chapters: int, total_words: int, built: str) -> str:
    nav = grouped_book_nav_fixed(stats)
    aside = f"""
    <div class="side-head">
      <div class="brand"><a href="../index.html">tyneside.software</a> · bible</div>
      <h1>Holy Bible</h1>
      <p class="sub">World English Bible</p>
      <div class="epigraph">
        Sixty-six books. Public-domain modern English.
        From <em>In the beginning</em> to Amen.
      </div>
      <div class="stats">
        <div><strong>{len(stats)}</strong> books</div>
        <div><strong>{total_chapters:,}</strong> chapters</div>
        <div><strong>{total_words:,}</strong> words</div>
        <div>{escape(built)}</div>
      </div>
      {jump_block()}
    </div>
    <nav class="nav" aria-label="Books">{nav}</nav>
    """

    def cards(testament: str, heading: str) -> str:
        out = [f"<h2>{escape(heading)}</h2>"]
        last_group = None
        open_cards = False
        for s in stats:
            if s["testament"] != testament:
                continue
            if s["group"] != last_group:
                if open_cards:
                    out.append("</div>")
                out.append(f'<h3>{escape(s["group"])}</h3><div class="cards">')
                open_cards = True
                last_group = s["group"]
            nch = s["chapter_count"]
            ch_label = "1 chapter" if nch == 1 else f"{nch} chapters"
            out.append(
                f'<a class="card" href="books/{s["stem"]}.html">'
                f'<span class="card-name">{escape(s["name"])}</span>'
                f'<span class="card-meta">{ch_label} · {s["words"]:,} words</span>'
                f"</a>"
            )
        if open_cards:
            out.append("</div>")
        return "".join(out)

    main = f"""
      <header class="hero">
        <div class="badge">World English Bible · public domain</div>
        <h1>Holy Bible</h1>
        <p>The whole Protestant canon in modern English, laid out like a book — chapters you can sit with, a sidebar that knows where you are, and a jump box for John 3:16.</p>
        <div class="hero-actions">
          <a class="btn-fill" href="books/genesis.html#c-1">Begin Genesis</a>
          <a class="btn-ghost" href="books/john.html#c-1">Open John</a>
          <a class="btn-ghost" id="resume-link" href="books/genesis.html" hidden>Continue reading</a>
        </div>
      </header>
      <section class="library" id="library">
        {cards("ot", "Old Testament")}
        {cards("nt", "New Testament")}
      </section>
      <footer class="foot">
        World English Bible (public domain) · {len(stats)} books · {total_chapters:,} chapters ·
        <a href="../michael-book/">ΑΩ</a> · tyneside.software
      </footer>
    """
    return page_shell(
        title="Holy Bible — World English Bible",
        description="The whole Bible in modern English. World English Bible, public domain. Read with chapter navigation at tyneside.software/bible.",
        asset_prefix="",
        body_attrs='data-page="index"',
        toggle_label="Books",
        aside=aside,
        main=main,
    )


def render_book(
    spec: tuple,
    chapters: dict[int, dict],
    stats: list[dict],
    prev_book: dict | None,
    next_book: dict | None,
    built: str,
) -> str:
    name, stem, testament, group, aliases = spec
    nchap = max(chapters)
    words = sum(ch["words"] for ch in chapters.values())
    verses = sum(len(ch["verses"]) for ch in chapters.values())
    testament_label = "Old Testament" if testament == "ot" else "New Testament"
    kicker_book = "Psalm" if name == "Psalms" else name

    chap_nav = []
    for n in sorted(chapters):
        title = f"Psalm {n}" if name == "Psalms" else f"Chapter {n}"
        chap_nav.append(
            f'<a class="nav-item" href="#c-{n}" data-filter="{n} {title}">'
            f'<span class="n">{n}</span><span class="t">{escape(title)}</span></a>'
        )

    sections = []
    ordered = sorted(chapters)
    for i, n in enumerate(ordered):
        rec = chapters[n]
        heading = f"Psalm {n}" if name == "Psalms" else f"Chapter {n}"
        prev_link = (
            f'<a href="#c-{ordered[i-1]}">← {("Psalm" if name == "Psalms" else "Chapter")} {ordered[i-1]}</a>'
            if i
            else "<span></span>"
        )
        next_link = (
            f'<a href="#c-{ordered[i+1]}">{("Psalm" if name == "Psalms" else "Chapter")} {ordered[i+1]} →</a>'
            if i < len(ordered) - 1
            else "<span></span>"
        )
        sections.append(
            f'<article class="chapter" id="c-{n}">'
            f'<header class="ch-head">'
            f'<p class="kicker">{escape(kicker_book)}</p>'
            f"<h2>{escape(heading)}</h2>"
            f'<p class="meta">{len(rec["verses"])} verses · {rec["words"]:,} words · World English Bible</p>'
            f"</header>"
            f'<div class="body">{"".join(rec["parts"])}</div>'
            f'<p class="ch-end">{prev_link}{next_link}</p>'
            f"</article>"
        )

    prev_html = (
        f'<a href="{prev_book["stem"]}.html">← {escape(prev_book["name"])}</a>'
        if prev_book
        else '<a href="../index.html">← All books</a>'
    )
    next_html = (
        f'<a href="{next_book["stem"]}.html">{escape(next_book["name"])} →</a>'
        if next_book
        else '<a href="../index.html">All books →</a>'
    )

    aside = f"""
    <div class="side-head">
      <div class="brand"><a href="../../index.html">tyneside.software</a> · <a href="../index.html">bible</a></div>
      <h1>{escape(name)}</h1>
      <p class="sub">{escape(testament_label)} · {escape(group)}</p>
      <div class="epigraph">World English Bible. Public domain modern English.</div>
      <div class="stats">
        <div><strong>{nchap}</strong> chapters</div>
        <div><strong>{verses:,}</strong> verses</div>
        <div><strong>{words:,}</strong> words</div>
        <div>{escape(built)}</div>
      </div>
      {jump_block()}
    </div>
    <nav class="nav" aria-label="Chapters">{"".join(chap_nav)}</nav>
    <p class="side-lib"><a href="../index.html">← All books</a></p>
    """

    main = f"""
      <header class="hero">
        <div class="badge">{escape(testament_label)} · {escape(group)}</div>
        <h1>{escape(name)}</h1>
        <p>{nchap} chapters · {verses:,} verses · {words:,} words</p>
      </header>
      <nav class="book-nav" aria-label="Nearby books">{prev_html}{next_html}</nav>
      {"".join(sections)}
      <nav class="book-nav" aria-label="Nearby books">{prev_html}{next_html}</nav>
      <footer class="foot">
        {escape(name)} · World English Bible · <a href="../index.html">Holy Bible</a>
      </footer>
    """
    return page_shell(
        title=f"{name} — World English Bible",
        description=f"{name} in the World English Bible. {nchap} chapters of public-domain modern English.",
        asset_prefix="../",
        body_attrs=f'data-page="book" data-book="{stem}"',
        toggle_label="Chapters",
        aside=aside,
        main=main,
    )


def write_readme() -> None:
    (OUT_DIR / "README.md").write_text(
        """# Holy Bible — World English Bible

**Live:** https://tyneside.software/bible/

Public-domain modern English. Same reader chrome as [michael-book](https://tyneside.software/michael-book/).

## Build

```powershell
cd C:\\Users\\MichaelThomson\\source\\TTS
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
""",
        encoding="utf-8",
    )


def build() -> None:
    ensure_sources()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    BOOKS_DIR.mkdir(parents=True, exist_ok=True)
    built = _now()

    parsed: list[tuple[tuple, dict[int, dict]]] = []
    stats: list[dict] = []
    for spec in BOOKS:
        name, stem, testament, group, aliases = spec
        chapters = load_book(stem)
        parsed.append((spec, chapters))
        stats.append(
            {
                "name": name,
                "stem": stem,
                "testament": testament,
                "group": group,
                "aliases": aliases,
                "chapter_count": max(chapters),
                "words": sum(ch["words"] for ch in chapters.values()),
                "verses": sum(len(ch["verses"]) for ch in chapters.values()),
            }
        )
        print(f"  parsed {name}: {max(chapters)} ch, {stats[-1]['words']:,} words")

    write_canon(stats)
    total_chapters = sum(s["chapter_count"] for s in stats)
    total_words = sum(s["words"] for s in stats)
    (OUT_DIR / "index.html").write_text(
        render_index(stats, total_chapters, total_words, built), encoding="utf-8"
    )

    for i, (spec, chapters) in enumerate(parsed):
        prev_book = stats[i - 1] if i else None
        next_book = stats[i + 1] if i < len(stats) - 1 else None
        html = render_book(spec, chapters, stats, prev_book, next_book, built)
        (BOOKS_DIR / f"{spec[1]}.html").write_text(html, encoding="utf-8")

    write_readme()
    print(f"Wrote {OUT_DIR}")
    print(f"Books: {len(stats)}  Chapters: {total_chapters}  Words: {total_words:,}")


if __name__ == "__main__":
    build()
