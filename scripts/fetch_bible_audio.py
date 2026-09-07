"""Fetch the public-domain WEB British Edition chapter MP3 listing.

Writes sites/software/static/bible/audio-manifest.json — URLs only, not the
files (the zip is ~1.1 GB; GitHub Pages cannot host it). The reader streams
and offers download from eBible.org.

Usage:
  python scripts/fetch_bible_audio.py
"""
from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sites" / "software" / "static" / "bible" / "audio-manifest.json"
LIST_URL = "https://ebible.org/eng-webbe/mp3/"
UA = "tyneside.software-bible/1.0 (public-domain WEB reader)"

# Our book stems → WEBBE filename book codes
STEM_CODE = {
    "genesis": "GEN",
    "exodus": "EXO",
    "leviticus": "LEV",
    "numbers": "NUM",
    "deuteronomy": "DEU",
    "joshua": "JOS",
    "judges": "JDG",
    "ruth": "RUT",
    "1samuel": "1SA",
    "2samuel": "2SA",
    "1kings": "1KI",
    "2kings": "2KI",
    "1chronicles": "1CH",
    "2chronicles": "2CH",
    "ezra": "EZR",
    "nehemiah": "NEH",
    "esther": "EST",
    "job": "JOB",
    "psalms": "PSA",
    "proverbs": "PRO",
    "ecclesiastes": "ECC",
    "songofsolomon": "SNG",
    "isaiah": "ISA",
    "jeremiah": "JER",
    "lamentations": "LAM",
    "ezekiel": "EZK",
    "daniel": "DAN",
    "hosea": "HOS",
    "joel": "JOL",
    "amos": "AMO",
    "obadiah": "OBA",
    "jonah": "JON",
    "micah": "MIC",
    "nahum": "NAM",
    "habakkuk": "HAB",
    "zephaniah": "ZEP",
    "haggai": "HAG",
    "zechariah": "ZEC",
    "malachi": "MAL",
    "matthew": "MAT",
    "mark": "MRK",
    "luke": "LUK",
    "john": "JHN",
    "acts": "ACT",
    "romans": "ROM",
    "1corinthians": "1CO",
    "2corinthians": "2CO",
    "galatians": "GAL",
    "ephesians": "EPH",
    "philippians": "PHP",
    "colossians": "COL",
    "1thessalonians": "1TH",
    "2thessalonians": "2TH",
    "1timothy": "1TI",
    "2timothy": "2TI",
    "titus": "TIT",
    "philemon": "PHM",
    "hebrews": "HEB",
    "james": "JAS",
    "1peter": "1PE",
    "2peter": "2PE",
    "1john": "1JN",
    "2john": "2JN",
    "3john": "3JN",
    "jude": "JUD",
    "revelation": "REV",
}

EXPECTED = {
    "GEN": 50, "EXO": 40, "LEV": 27, "NUM": 36, "DEU": 34, "JOS": 24, "JDG": 21, "RUT": 4,
    "1SA": 31, "2SA": 24, "1KI": 22, "2KI": 25, "1CH": 29, "2CH": 36, "EZR": 10, "NEH": 13, "EST": 10,
    "JOB": 42, "PSA": 150, "PRO": 31, "ECC": 12, "SNG": 8, "ISA": 66, "JER": 52, "LAM": 5, "EZK": 48, "DAN": 12,
    "HOS": 14, "JOL": 3, "AMO": 9, "OBA": 1, "JON": 4, "MIC": 7, "NAM": 3, "HAB": 3, "ZEP": 3, "HAG": 2, "ZEC": 14, "MAL": 4,
    "MAT": 28, "MRK": 16, "LUK": 24, "JHN": 21, "ACT": 28, "ROM": 16, "1CO": 16, "2CO": 13, "GAL": 6, "EPH": 6,
    "PHP": 4, "COL": 4, "1TH": 5, "2TH": 3, "1TI": 6, "2TI": 4, "TIT": 3, "PHM": 1, "HEB": 13,
    "JAS": 5, "1PE": 5, "2PE": 3, "1JN": 5, "2JN": 1, "3JN": 1, "JUD": 1, "REV": 22,
}


def main() -> None:
    req = urllib.request.Request(LIST_URL, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as resp:
        html = resp.read().decode("utf-8", "replace")
    files = re.findall(r'href="(eng-webbe_\d+_([A-Za-z0-9]+)_\d+\.mp3)"', html)
    by_code: dict[str, dict[int, str]] = {}
    for name, code in files:
        m = re.search(r"_(\d+)\.mp3$", name)
        if not m:
            continue
        ch = int(m.group(1))
        by_code.setdefault(code, {})[ch] = LIST_URL + name

    books: dict[str, dict[str, str]] = {}
    missing: list[str] = []
    for stem, code in STEM_CODE.items():
        want = EXPECTED[code]
        got = by_code.get(code) or {}
        if sorted(got) != list(range(1, want + 1)):
            missing.append(f"{stem}/{code}: want {want}, got {sorted(got)[:8]}… n={len(got)}")
            continue
        books[stem] = {str(ch): got[ch] for ch in range(1, want + 1)}
    if missing:
        raise SystemExit("Audio listing incomplete:\n  " + "\n  ".join(missing))

    n = sum(len(v) for v in books.values())
    payload = {
        "source": {
            "name": "World English Bible British Edition",
            "list_url": LIST_URL,
            "license": "Public domain",
            "audio_by": "PublicDomainAudioBibles.com",
            "text_by": "eBible.org",
            "note": (
                "British/international English chapter MP3s of the WEB British Edition. "
                "No North-East English recording of the World English Bible is known. "
                "On-page text remains the American WEB (public domain); the audio uses "
                "British spelling (honour, favour) and LORD rather than Yahweh."
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
