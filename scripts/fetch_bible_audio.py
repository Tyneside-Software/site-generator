"""Build audio-manifest.json from Winfred Henson's WEB chapter MP3s.

Professional single-narrator recording (LibriVox 4.4/5). Public domain.
Chapter files live at https://ebible.org/eng-web/audio/

Usage:
  python scripts/fetch_bible_audio.py
"""
from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sites" / "software" / "static" / "bible" / "audio-manifest.json"
INDEX = "https://ebible.org/eng-web/audio/"
UA = "tyneside.software-bible/1.0 (public-domain WEB reader)"

STEMS = [
    "genesis", "exodus", "leviticus", "numbers", "deuteronomy",
    "joshua", "judges", "ruth", "1samuel", "2samuel",
    "1kings", "2kings", "1chronicles", "2chronicles", "ezra",
    "nehemiah", "esther", "job", "psalms", "proverbs",
    "ecclesiastes", "songofsolomon", "isaiah", "jeremiah", "lamentations",
    "ezekiel", "daniel", "hosea", "joel", "amos",
    "obadiah", "jonah", "micah", "nahum", "habakkuk",
    "zephaniah", "haggai", "zechariah", "malachi",
    "matthew", "mark", "luke", "john", "acts",
    "romans", "1corinthians", "2corinthians", "galatians", "ephesians",
    "philippians", "colossians", "1thessalonians", "2thessalonians",
    "1timothy", "2timothy", "titus", "philemon", "hebrews",
    "james", "1peter", "2peter", "1john", "2john", "3john", "jude",
    "revelation",
]

EXPECTED = {
    "genesis": 50, "exodus": 40, "leviticus": 27, "numbers": 36, "deuteronomy": 34,
    "joshua": 24, "judges": 21, "ruth": 4, "1samuel": 31, "2samuel": 24,
    "1kings": 22, "2kings": 25, "1chronicles": 29, "2chronicles": 36, "ezra": 10,
    "nehemiah": 13, "esther": 10, "job": 42, "psalms": 150, "proverbs": 31,
    "ecclesiastes": 12, "songofsolomon": 8, "isaiah": 66, "jeremiah": 52,
    "lamentations": 5, "ezekiel": 48, "daniel": 12, "hosea": 14, "joel": 3,
    "amos": 9, "obadiah": 1, "jonah": 4, "micah": 7, "nahum": 3, "habakkuk": 3,
    "zephaniah": 3, "haggai": 2, "zechariah": 14, "malachi": 4,
    "matthew": 28, "mark": 16, "luke": 24, "john": 21, "acts": 28,
    "romans": 16, "1corinthians": 16, "2corinthians": 13, "galatians": 6,
    "ephesians": 6, "philippians": 4, "colossians": 4, "1thessalonians": 5,
    "2thessalonians": 3, "1timothy": 6, "2timothy": 4, "titus": 3, "philemon": 1,
    "hebrews": 13, "james": 5, "1peter": 5, "2peter": 3, "1john": 5,
    "2john": 1, "3john": 1, "jude": 1, "revelation": 22,
}

ONES = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9,
    "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
}
TENS = {
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
    "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
}


def get(url: str) -> str:
    last: Exception | None = None
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read().decode("utf-8", "replace")
        except Exception as exc:  # noqa: BLE001
            last = exc
            import time

            time.sleep(1.5 * (attempt + 1))
    raise last or RuntimeError(url)


class HrefParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        for k, v in attrs:
            if k == "href" and v:
                self.hrefs.append(v)


def hrefs(html: str) -> list[str]:
    p = HrefParser()
    p.feed(html)
    return p.hrefs


def words_to_int(tokens: list[str]) -> int | None:
    n = 0
    hundred = 0
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t == "hundred":
            hundred = (hundred or 1) * 100
            i += 1
            continue
        if t in TENS:
            hundred += TENS[t]
            i += 1
            continue
        if t in ONES:
            hundred += ONES[t]
            i += 1
            continue
        i += 1
    n += hundred
    return n or None


def chapter_from_name(name: str) -> int | None:
    stem = urllib.parse.unquote(name)
    stem = re.sub(r"\.mp3$", "", stem, flags=re.I)
    stem = stem.replace("_", " ").replace("-", " ")
    # 01_21_Genesis_Chapter_Twenty_One
    m = re.search(r"(?:^|/)\d{2}_(\d{1,3})_", name)
    if m:
        return int(m.group(1))
    # drop leading catalogue numbers
    stem = re.sub(r"^[\d\s]+", "", stem)
    stem = re.sub(r"\s*\(\d+\)\s*$", "", stem)
    low = stem.lower()
    if "chapter" in low:
        tail = low.split("chapter", 1)[1]
    else:
        # Psalms-Twenty One
        parts = re.split(r"psalms|psalm", low, maxsplit=1)
        tail = parts[-1] if len(parts) > 1 else low
    tokens = re.findall(r"[a-z]+", tail)
    skip = {
        "chapter", "psalm", "psalms", "revelations", "revelation",
        "genesis", "exodus", "the", "of", "and",
    }
    tokens = [t for t in tokens if t not in skip]
    return words_to_int(tokens)


def sort_key(filename: str) -> tuple:
    raw = urllib.parse.unquote(filename)
    m = re.search(r"(?:^|/)\d{2}_(\d{1,3})_", filename)
    if m:
        return (0, int(m.group(1)), raw)
    m = re.match(r"^(\d{2,4})\b", raw.strip())
    if m:
        return (1, int(m.group(1)), raw)
    nums = re.findall(r"\d+", raw)
    if nums:
        return (2, int(nums[0]), raw)
    return (3, 0, raw)


def pick_files(names: list[str], want: int) -> list[str]:
    mp3s = [n for n in names if n.lower().endswith(".mp3")]
    mp3s = [n for n in mp3s if "(1)" not in urllib.parse.unquote(n)]
    scored: list[tuple[int, str]] = []
    for n in mp3s:
        ch = chapter_from_name(n)
        if ch:
            scored.append((ch, n))
    by_ch: dict[int, str] = {}
    for ch, n in scored:
        if 1 <= ch <= want and ch not in by_ch:
            by_ch[ch] = n
    if len(by_ch) == want:
        return [by_ch[i] for i in range(1, want + 1)]
    ordered = sorted(mp3s, key=sort_key)
    if len(ordered) >= want:
        return ordered[:want]
    raise SystemExit(f"only {len(ordered)} mp3s, want {want}")


def main() -> None:
    index = get(INDEX)
    folders: dict[int, str] = {}
    for h in hrefs(index):
        m = re.match(r"^(\d{2})_[^/]+/$", h)
        if m:
            folders[int(m.group(1))] = urllib.parse.urljoin(INDEX, h)
    if len(folders) != 66:
        raise SystemExit(f"expected 66 book folders, got {sorted(folders)}")

    books: dict[str, dict[str, str]] = {}
    for i, stem in enumerate(STEMS, 1):
        folder = folders[i]
        html = get(folder)
        names = [h for h in hrefs(html) if h.lower().endswith(".mp3")]
        want = EXPECTED[stem]
        chosen = pick_files(names, want)
        books[stem] = {
            str(ch): urllib.parse.urljoin(folder, name)
            for ch, name in enumerate(chosen, 1)
        }
        print(f"  {stem}: {want} ok  e.g. {chosen[0]}")

    n = sum(len(v) for v in books.values())
    payload = {
        "source": {
            "name": "World English Bible, read by Winfred Wardell Henson",
            "list_url": INDEX,
            "license": "Public domain",
            "audio_by": "Winfred Wardell Henson (professional voice artist)",
            "text_by": "eBible.org",
            "reviews": "LibriVox 4.4/5 from 97 ratings; one narrator for the whole Bible",
            "note": (
                "Human reading of the classic World English Bible (matches the on-page text, "
                "including Yahweh). American English. Public domain. "
                "Chosen over the British Edition TTS, which was poorly read."
            ),
        },
        "chapter_count": n,
        "books": books,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} ({n} chapters, {len(books)} books)")


if __name__ == "__main__":
    main()
