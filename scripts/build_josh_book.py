"""
Build tyneside.software/josh-book learning page from Experience Therefore chapter
audio + spoken scripts. Pattern matches Lewis Learning (Brain OS), but all chapters
are unlocked from the start.
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEWIS_HTML = Path(
    r"C:\Users\MichaelThomson\Desktop\New folder\repo-work\lewis_learning\index.html"
)
SPOKEN = Path(r"C:\Users\MichaelThomson\Downloads\Experience Therefore - chapters\spoken")
AUDIO_SRC = Path(r"C:\Users\MichaelThomson\Downloads\Experience Therefore - chapters\audio")
DEST = ROOT / "sites" / "software" / "static" / "josh-book"
# MP3s staged here for GitHub Release upload (not committed into Pages static)
AUDIO_STAGE = ROOT / "output" / "_josh_book_audio_stage"

# Hosted audio (GitHub Release). Local audio/ still works if AUDIO_BASE_URL is "".
AUDIO_BASE_URL = (
    "https://github.com/michaelthomsoncc/daily-news-site/releases/download/"
    "josh-book-audio-v1"
)

# source filename -> web filename, id, num, title, desc, quiz, correct
CHAPTERS = [
    {
        "id": "front",
        "num": "Intro",
        "intro": True,
        "src_stem": "00_Front_Matter",
        "file": "00-front-matter.mp3",
        "script": "00-front-matter.txt",
        "title": "Dedication & Title",
        "desc": "Dedication, title page, and copyright for Experience, Therefore by Joshua Thomson.",
        "quiz": [
            {
                "id": "front-1",
                "type": "single",
                "text": "Who wrote Experience, Therefore?",
                "options": [
                    "Joshua Thomson",
                    "Michael Thomson",
                    "Descartes",
                    "Spinoza",
                ],
            },
            {
                "id": "front-2",
                "type": "single",
                "text": "What is the book dedicated to?",
                "options": [
                    "Ellerose The Unicorn",
                    "Newcastle United",
                    "A university department",
                    "No dedication is given",
                ],
            },
            {
                "id": "front-3",
                "type": "single",
                "text": "Which subtitle ideas appear on the title material?",
                "options": [
                    "The Existence of God and The Impossibility Of Hell",
                    "A guide to better exam technique",
                    "Ten steps to financial freedom",
                    "A children's adventure novel only",
                ],
            },
            {
                "id": "front-4",
                "type": "multiple",
                "text": "Which statements match the front matter? (Select all that apply)",
                "options": [
                    "It is a third edition, revised and expanded",
                    "All rights are reserved by the author",
                    "It claims to be an official church doctrine manual",
                    "An email contact is given for inquiries",
                ],
            },
        ],
        "correct": {
            "front-1": "Joshua Thomson",
            "front-2": "Ellerose The Unicorn",
            "front-3": "The Existence of God and The Impossibility Of Hell",
            "front-4": [
                "It is a third edition, revised and expanded",
                "All rights are reserved by the author",
                "An email contact is given for inquiries",
            ],
        },
    },
    {
        "id": "ch1",
        "num": 1,
        "src_stem": "01_Chapter_1_The_Foundation",
        "file": "01-chapter-1-the-foundation.mp3",
        "script": "01-chapter-1-the-foundation.txt",
        "title": "The Foundation",
        "desc": "I experience, therefore I am. Experiential Axiomatism: existence is certain; everything within it is open to agnostic doubt.",
        "quiz": [
            {
                "id": "ch1-1",
                "type": "single",
                "text": "What is the book's foundational axiom?",
                "options": [
                    "Existence exists",
                    "Everything is an illusion with no experience",
                    "Only mathematics is real",
                    "Hell is required for morality",
                ],
            },
            {
                "id": "ch1-2",
                "type": "single",
                "text": "What does the 6 vs 9 floor example illustrate?",
                "options": [
                    "Frameworks change how evidence is read, but the experience of perceiving still exists",
                    "One person is always objectively wrong about everything",
                    "Numbers cannot exist",
                    "Only authority can decide truth",
                ],
            },
            {
                "id": "ch1-3",
                "type": "single",
                "text": "What new ontological framework does the chapter name?",
                "options": [
                    "Experiential Axiomatism",
                    "Radical nihilism",
                    "Pure dualism",
                    "Materialist physicalism only",
                ],
            },
            {
                "id": "ch1-4",
                "type": "multiple",
                "text": "Which claims match Chapter 1? (Select all that apply)",
                "options": [
                    "You can be certain your experience of this moment exists",
                    "We must be agnostic about everything within existence",
                    "Every sentence of the book is objectively true content",
                    "Postmodernism and objectivism are each described as about 99% right",
                ],
            },
            {
                "id": "ch1-5",
                "type": "single",
                "text": "What bold conclusion does the chapter preview?",
                "options": [
                    "Because you woke up today, Hell cannot exist because God must",
                    "Nothing exists at all",
                    "Faith alone decides every metaphysical question",
                    "Logic has no role in ontology",
                ],
            },
        ],
        "correct": {
            "ch1-1": "Existence exists",
            "ch1-2": "Frameworks change how evidence is read, but the experience of perceiving still exists",
            "ch1-3": "Experiential Axiomatism",
            "ch1-4": [
                "You can be certain your experience of this moment exists",
                "We must be agnostic about everything within existence",
                "Postmodernism and objectivism are each described as about 99% right",
            ],
            "ch1-5": "Because you woke up today, Hell cannot exist because God must",
        },
    },
    {
        "id": "ch2",
        "num": 2,
        "src_stem": "02_Chapter_2_The_True_Binary",
        "file": "02-chapter-2-the-true-binary.mp3",
        "script": "02-chapter-2-the-true-binary.txt",
        "title": "The True Binary",
        "desc": "Existence, therefore, is united. Separation is apparent; a true outside boundary collapses into paradox.",
        "quiz": [
            {
                "id": "ch2-1",
                "type": "single",
                "text": "What is the true binary in Chapter 2?",
                "options": [
                    "Existence exists vs existence does not exist",
                    "Good vs evil as equal fundamentals",
                    "Mind vs matter with no shared fabric",
                    "Faith vs science only",
                ],
            },
            {
                "id": "ch2-2",
                "type": "single",
                "text": "Which door remains after logic is applied?",
                "options": [
                    "Door A — the Unity Model",
                    "Door B — fundamental plural separation",
                    "Door C — nihilism",
                    "None of the doors",
                ],
            },
            {
                "id": "ch2-3",
                "type": "single",
                "text": "Why does a hard boundary between separate realms fail?",
                "options": [
                    "It must exist and not exist at once, or triggers infinite regress",
                    "Boundaries are always painted red",
                    "Science forbids all distinctions",
                    "Unity means nothing can ever look different",
                ],
            },
            {
                "id": "ch2-4",
                "type": "multiple",
                "text": "Which points match the chapter? (Select all that apply)",
                "options": [
                    "Difference is not the same as separation",
                    "You cannot stand outside existence to point at a crack",
                    "All existence is equal in its share of existing",
                    "Nihilism is proven by the fact you are reading",
                ],
            },
        ],
        "correct": {
            "ch2-1": "Existence exists vs existence does not exist",
            "ch2-2": "Door A — the Unity Model",
            "ch2-3": "It must exist and not exist at once, or triggers infinite regress",
            "ch2-4": [
                "Difference is not the same as separation",
                "You cannot stand outside existence to point at a crack",
                "All existence is equal in its share of existing",
            ],
        },
    },
    {
        "id": "ch3",
        "num": 3,
        "src_stem": "03_Chapter_3_Existence_therefore_is_eternal",
        "file": "03-chapter-3-existence-therefore-is-eternal.mp3",
        "script": "03-chapter-3-existence-therefore-is-eternal.txt",
        "title": "Existence is Eternal",
        "desc": "No beginning from non-existence. Ex nihilo nihil fit. Time is internal to existence, not its container.",
        "quiz": [
            {
                "id": "ch3-1",
                "type": "single",
                "text": "What Latin maxim is used against creation from absolute nothing?",
                "options": [
                    "Ex nihilo nihil fit",
                    "Cogito ergo sum only",
                    "Carpe diem",
                    "Memento mori as a physics law",
                ],
            },
            {
                "id": "ch3-2",
                "type": "single",
                "text": "Why is a beginning of existence treated as impossible here?",
                "options": [
                    "It would require crossing from non-existence into existence",
                    "Scientists measured the start precisely",
                    "Books cannot discuss time",
                    "Unity requires constant novelty only",
                ],
            },
            {
                "id": "ch3-3",
                "type": "single",
                "text": "How does the chapter treat time?",
                "options": [
                    "As an internal, actualised property within existence",
                    "As a fundamental infinite past that must be fully traversed",
                    "As non-existent in every sense",
                    "As a force that dominates and limits the whole of existence from outside",
                ],
            },
            {
                "id": "ch3-4",
                "type": "multiple",
                "text": "Which conclusions match Chapter 3? (Select all that apply)",
                "options": [
                    "Existence has no beginning and no end",
                    "An infinite past as fundamental time is also problematic",
                    "Existence transcends chronological origins",
                    "Existence began five minutes ago from pure nothing",
                ],
            },
        ],
        "correct": {
            "ch3-1": "Ex nihilo nihil fit",
            "ch3-2": "It would require crossing from non-existence into existence",
            "ch3-3": "As an internal, actualised property within existence",
            "ch3-4": [
                "Existence has no beginning and no end",
                "An infinite past as fundamental time is also problematic",
                "Existence transcends chronological origins",
            ],
        },
    },
    {
        "id": "ch4",
        "num": 4,
        "src_stem": "04_Chapter_4_The_eternity_of_all_potential",
        "file": "04-chapter-4-the-eternity-of-all-potential.mp3",
        "script": "04-chapter-4-the-eternity-of-all-potential.txt",
        "title": "The Eternity of All Potential",
        "desc": "Existence, therefore, is everything. Actualised and potential modes; the gatekeeper paradox of limits.",
        "quiz": [
            {
                "id": "ch4-1",
                "type": "single",
                "text": "What third attribute follows from unity and eternity?",
                "options": [
                    "Existence is everything and all-encompassing",
                    "Existence is limited by a gatekeeper outside it",
                    "Only actualised matter exists",
                    "Potential is unreal and worthless",
                ],
            },
            {
                "id": "ch4-2",
                "type": "single",
                "text": "What is the gatekeeper paradox about?",
                "options": [
                    "Any enforcer of a limit on existence must itself exist and so fails to stand outside",
                    "Airport security metaphors only",
                    "Why locks need keys in houses",
                    "How to limit reading time",
                ],
            },
            {
                "id": "ch4-3",
                "type": "single",
                "text": "How does the chapter distinguish modes of existence?",
                "options": [
                    "Actualised existence vs potential existence",
                    "Real matter vs fake ideas with no status",
                    "Heaven-only vs earth-only substances",
                    "Past vs future with no present",
                ],
            },
            {
                "id": "ch4-4",
                "type": "multiple",
                "text": "Which points match Chapter 4? (Select all that apply)",
                "options": [
                    "The impossibility of nothing is the inevitability of everything",
                    "Unactualised concepts are not a lesser form of existence",
                    "There is a hierarchy where some things more-exist than others",
                    "Omnipotence is discussed via the rock-so-big puzzle",
                ],
            },
        ],
        "correct": {
            "ch4-1": "Existence is everything and all-encompassing",
            "ch4-2": "Any enforcer of a limit on existence must itself exist and so fails to stand outside",
            "ch4-3": "Actualised existence vs potential existence",
            "ch4-4": [
                "The impossibility of nothing is the inevitability of everything",
                "Unactualised concepts are not a lesser form of existence",
                "Omnipotence is discussed via the rock-so-big puzzle",
            ],
        },
    },
    {
        "id": "ch5",
        "num": 5,
        "src_stem": "05_Chapter_5_Existence_therefore_is_conscious",
        "file": "05-chapter-5-existence-therefore-is-conscious.mp3",
        "script": "05-chapter-5-existence-therefore-is-conscious.txt",
        "title": "Existence is Conscious",
        "desc": "Because existence is everything, consciousness and volition cannot be alien add-ons from nowhere.",
        "quiz": [
            {
                "id": "ch5-1",
                "type": "single",
                "text": "What does the chapter conclude about existence?",
                "options": [
                    "Existence, therefore, is conscious",
                    "Consciousness is impossible",
                    "Only rocks exist",
                    "Volition proves non-existence",
                ],
            },
            {
                "id": "ch5-2",
                "type": "single",
                "text": "Why is putting down the book an example used in the chapter?",
                "options": [
                    "It shows conscious preference and volition existing within existence",
                    "It proves books are not real",
                    "It proves free will is always unlimited",
                    "It proves only the author is conscious",
                ],
            },
            {
                "id": "ch5-3",
                "type": "single",
                "text": "What is denied about consciousness as a bolt-on from a void?",
                "options": [
                    "It cannot spawn from non-existence or stand as wholly other than source",
                    "It must be identical to every human personality detail",
                    "It only exists in computers",
                    "It is irrelevant to ontology",
                ],
            },
            {
                "id": "ch5-4",
                "type": "multiple",
                "text": "Which ideas match Chapter 5? (Select all that apply)",
                "options": [
                    "Experience cannot not-be-experienced in the same way existence cannot not-exist",
                    "Inherent qualities are ongoing willing conscious choices, not mere limiting forces",
                    "You are fundamentally alien to the whole of existence",
                    "Physical and immaterial properties are encompassed by everythingness",
                ],
            },
        ],
        "correct": {
            "ch5-1": "Existence, therefore, is conscious",
            "ch5-2": "It shows conscious preference and volition existing within existence",
            "ch5-3": "It cannot spawn from non-existence or stand as wholly other than source",
            "ch5-4": [
                "Experience cannot not-be-experienced in the same way existence cannot not-exist",
                "Inherent qualities are ongoing willing conscious choices, not mere limiting forces",
                "Physical and immaterial properties are encompassed by everythingness",
            ],
        },
    },
    {
        "id": "ch6",
        "num": 6,
        "src_stem": "06_Chapter_6_Existence_therefore_prefers",
        "file": "06-chapter-6-existence-therefore-prefers.mp3",
        "script": "06-chapter-6-existence-therefore-prefers.txt",
        "title": "Existence Prefers",
        "desc": "Preference without anthropomorphism. Chance and forced inevitability both self-refute as ultimate accounts.",
        "quiz": [
            {
                "id": "ch6-1",
                "type": "single",
                "text": "What does the chapter conclude?",
                "options": [
                    "Existence, therefore, prefers",
                    "Preference is always anthropomorphic emotion only",
                    "Chance is a complete ultimate explanation",
                    "Nothing ever actualises",
                ],
            },
            {
                "id": "ch6-2",
                "type": "single",
                "text": "How does the chapter want 'preference' treated?",
                "options": [
                    "Strip anthropomorphic connotation and define carefully",
                    "Treat it only as human mood swings",
                    "Ignore the word entirely",
                    "Equate it only with religious dogma",
                ],
            },
            {
                "id": "ch6-3",
                "type": "single",
                "text": "What happens to pure chance and pure forced inevitability as ultimate accounts?",
                "options": [
                    "Both options self-refute",
                    "Both are proven true forever",
                    "Only chance survives",
                    "Only inevitability survives",
                ],
            },
            {
                "id": "ch6-4",
                "type": "multiple",
                "text": "Which claims match Chapter 6? (Select all that apply)",
                "options": [
                    "Preference is fundamental, not merely emergent illusion",
                    "Any sentient volition anywhere is not a brand-new ability from nowhere",
                    "Content (furniture) and context (the room) are carefully distinguished",
                    "Preference must mean human-style favouritism with feelings only",
                ],
            },
        ],
        "correct": {
            "ch6-1": "Existence, therefore, prefers",
            "ch6-2": "Strip anthropomorphic connotation and define carefully",
            "ch6-3": "Both options self-refute",
            "ch6-4": [
                "Preference is fundamental, not merely emergent illusion",
                "Any sentient volition anywhere is not a brand-new ability from nowhere",
                "Content (furniture) and context (the room) are carefully distinguished",
            ],
        },
    },
    {
        "id": "ch7",
        "num": 7,
        "src_stem": "07_Chapter_7_Experience_therefore_has_meaning",
        "file": "07-chapter-7-experience-therefore-has-meaning.mp3",
        "script": "07-chapter-7-experience-therefore-has-meaning.txt",
        "title": "Experience Has Meaning",
        "desc": "Chaos and order, both&, and why experience is not a meaningless accident under the axiom.",
        "quiz": [
            {
                "id": "ch7-1",
                "type": "single",
                "text": "What does Chapter 7 conclude?",
                "options": [
                    "Experience, therefore, has meaning",
                    "Experience is meaningless by necessity",
                    "Only chaos is real",
                    "Only order is real and chaos never appears",
                ],
            },
            {
                "id": "ch7-2",
                "type": "single",
                "text": "What does the axiom 'Existence exists' do to the need for faith in the chapter's framing?",
                "options": [
                    "It disarms the need for faith by starting from first principles",
                    "It requires blind faith to accept any experience",
                    "It proves every religion word-for-word",
                    "It forbids using logic",
                ],
            },
            {
                "id": "ch7-3",
                "type": "single",
                "text": "How are chaos and order treated when separation is not fundamental?",
                "options": [
                    "Both can be hosted within unity without requiring a hard outside",
                    "One must delete the other from reality entirely",
                    "They prove Door B separation",
                    "They prove nihilism",
                ],
            },
            {
                "id": "ch7-4",
                "type": "multiple",
                "text": "Which ideas match Chapter 7? (Select all that apply)",
                "options": [
                    "Without cold, warmth loses experiential meaning",
                    "Faith and religions stumble when equating something partial with the whole",
                    "You have a both& experience of limited free will",
                    "Meaning requires non-existence to win",
                ],
            },
        ],
        "correct": {
            "ch7-1": "Experience, therefore, has meaning",
            "ch7-2": "It disarms the need for faith by starting from first principles",
            "ch7-3": "Both can be hosted within unity without requiring a hard outside",
            "ch7-4": [
                "Without cold, warmth loses experiential meaning",
                "Faith and religions stumble when equating something partial with the whole",
                "You have a both& experience of limited free will",
            ],
        },
    },
    {
        "id": "ch8",
        "num": 8,
        "src_stem": "08_Chapter_8_The_Final_Stress_Test",
        "file": "08-chapter-8-the-final-stress-test.mp3",
        "script": "08-chapter-8-the-final-stress-test.txt",
        "title": "The Final Stress Test",
        "desc": "Ultimate paradox / proof. Hell's impossibility, the willing illusion of Door B, and Soli Deo Gloria.",
        "quiz": [
            {
                "id": "ch8-1",
                "type": "single",
                "text": "According to the stress test, what are the only two options for the ontology?",
                "options": [
                    "Total non-existence or total existence",
                    "Blue or green walls",
                    "Faith or science with no overlap",
                    "Past or future with no present",
                ],
            },
            {
                "id": "ch8-2",
                "type": "single",
                "text": "Why is Hell treated as impossible in this framework?",
                "options": [
                    "Even the slightest creation of non-existence would fracture the fabric eternally",
                    "Because no religious texts mention judgment",
                    "Because suffering never appears in experience",
                    "Because logic forbids all stories",
                ],
            },
            {
                "id": "ch8-3",
                "type": "single",
                "text": "How is the willing illusion of Door B framed?",
                "options": [
                    "As the divine question asked from genuine neutrality and amnesia",
                    "As proof that separation is fundamental forever",
                    "As proof that existence does not exist",
                    "As a claim that no books should be written",
                ],
            },
            {
                "id": "ch8-4",
                "type": "multiple",
                "text": "Which themes appear in Chapter 8? (Select all that apply)",
                "options": [
                    "You are the question and the answer",
                    "The impossibility of Hell is confirmed by the logic of unity",
                    "Soli Deo Gloria closes the chapter",
                    "The axiom requires objective certainty about every furniture detail",
                ],
            },
        ],
        "correct": {
            "ch8-1": "Total non-existence or total existence",
            "ch8-2": "Even the slightest creation of non-existence would fracture the fabric eternally",
            "ch8-3": "As the divine question asked from genuine neutrality and amnesia",
            "ch8-4": [
                "You are the question and the answer",
                "The impossibility of Hell is confirmed by the logic of unity",
                "Soli Deo Gloria closes the chapter",
            ],
        },
    },
    {
        "id": "ch9",
        "num": 9,
        "src_stem": "09_Chapter_9_Existence_therefore_so_what",
        "file": "09-chapter-9-existence-therefore-so-what.mp3",
        "script": "09-chapter-9-existence-therefore-so-what.txt",
        "title": "So What?",
        "desc": "Limits of deduction. Live boldly. Treat others as versions of yourself. Sentio Ergo Sum.",
        "quiz": [
            {
                "id": "ch9-1",
                "type": "single",
                "text": "What does the chapter say about the 'so what?'",
                "options": [
                    "Here we reach the limit of pure logical deduction — experience it yourself",
                    "It is fully deduced with mathematical certainty like the axiom",
                    "It proves you must never make choices",
                    "It deletes the rest of the book",
                ],
            },
            {
                "id": "ch9-2",
                "type": "single",
                "text": "How does the chapter reframe loving your neighbour?",
                "options": [
                    "Treat others as a parallel-dimension version of yourself",
                    "Ignore others completely",
                    "Compete to prove superiority only",
                    "Never forgive anyone",
                ],
            },
            {
                "id": "ch9-3",
                "type": "single",
                "text": "What Latin line is paired with 'Experience, therefore'?",
                "options": [
                    "Sentio Ergo Sum",
                    "Veni Vidi Vici",
                    "Amor Fati only as rejection of experience",
                    "Tabula Rasa",
                ],
            },
            {
                "id": "ch9-4",
                "type": "multiple",
                "text": "Which practical notes match Chapter 9? (Select all that apply)",
                "options": [
                    "Know that you are God without the usual connotations — just as much as anyone else",
                    "Forgiving others is forgiving oneself",
                    "Rest in not needing to win every disagreement",
                    "The so what is fully objective furniture truth",
                ],
            },
        ],
        "correct": {
            "ch9-1": "Here we reach the limit of pure logical deduction — experience it yourself",
            "ch9-2": "Treat others as a parallel-dimension version of yourself",
            "ch9-3": "Sentio Ergo Sum",
            "ch9-4": [
                "Know that you are God without the usual connotations — just as much as anyone else",
                "Forgiving others is forgiving oneself",
                "Rest in not needing to win every disagreement",
            ],
        },
    },
    {
        "id": "add1",
        "num": "A1",
        "src_stem": "10_Addendum_1_Existence_Therefore_Refute",
        "file": "10-addendum-1-existence-therefore-refute.mp3",
        "script": "10-addendum-1-existence-therefore-refute.txt",
        "title": "Addendum 1 — Refute",
        "desc": "A challenge list: what would have to be shown for the ontology to fall.",
        "quiz": [
            {
                "id": "add1-1",
                "type": "single",
                "text": "What does 'irrefutable' mean in the author's challenge?",
                "options": [
                    "Nothing within existence refutes it — not that criticism is forbidden",
                    "No one is allowed to disagree",
                    "It has been proven by laboratory experiment only",
                    "It is closed and cannot be tested",
                ],
            },
            {
                "id": "add1-2",
                "type": "single",
                "text": "What is listed among possible refutation targets?",
                "options": [
                    "Disprove the binary of existence and non-existence",
                    "Prove the cover colour is wrong",
                    "Show the author lives in Essex only",
                    "Prove MP3s cannot exist",
                ],
            },
            {
                "id": "add1-3",
                "type": "multiple",
                "text": "Which appear on the refute list themes? (Select all that apply)",
                "options": [
                    "Show a leap or circular reasoning in the chain",
                    "Prove content can control and limit context",
                    "Prove non-existence exists to gap the fabric",
                    "Prove the book has no dedication",
                ],
            },
            {
                "id": "add1-4",
                "type": "single",
                "text": "How does the addendum close the posture of the challenge?",
                "options": [
                    "Until one point is proven certain, the ontology stands as a humble anchor",
                    "Debate is banned forever",
                    "Only academics may speak",
                    "The axiom is cancelled",
                ],
            },
        ],
        "correct": {
            "add1-1": "Nothing within existence refutes it — not that criticism is forbidden",
            "add1-2": "Disprove the binary of existence and non-existence",
            "add1-3": [
                "Show a leap or circular reasoning in the chain",
                "Prove content can control and limit context",
                "Prove non-existence exists to gap the fabric",
            ],
            "add1-4": "Until one point is proven certain, the ontology stands as a humble anchor",
        },
    },
    {
        "id": "add2",
        "num": "A2",
        "src_stem": "11_Addendum_2_Experience_Therefore_Reform",
        "file": "11-addendum-2-experience-therefore-reform.mp3",
        "script": "11-addendum-2-experience-therefore-reform.txt",
        "title": "Addendum 2 — Reform",
        "desc": "Standing on earlier thinkers. Semper Reformanda — always reforming.",
        "quiz": [
            {
                "id": "add2-1",
                "type": "single",
                "text": "Which thinkers are named as shoulders this ontology stands on?",
                "options": [
                    "Descartes, Einstein, Martin Luther, Spinoza",
                    "Only living TikTok philosophers",
                    "Nobody — the book claims total originality with no past",
                    "Only engineers at xAI",
                ],
            },
            {
                "id": "add2-2",
                "type": "single",
                "text": "What Latin reform motto appears?",
                "options": [
                    "Semper Reformanda",
                    "Status Quo Ante",
                    "Caveat Emptor",
                    "Deus Ex Machina",
                ],
            },
            {
                "id": "add2-3",
                "type": "multiple",
                "text": "Which claims match Addendum 2? (Select all that apply)",
                "options": [
                    "The ontology is not closed",
                    "It replaces doubt with the tool of certainty for building",
                    "Reform is both a return and a rebuilding",
                    "No future readers should expand it",
                ],
            },
        ],
        "correct": {
            "add2-1": "Descartes, Einstein, Martin Luther, Spinoza",
            "add2-2": "Semper Reformanda",
            "add2-3": [
                "The ontology is not closed",
                "It replaces doubt with the tool of certainty for building",
                "Reform is both a return and a rebuilding",
            ],
        },
    },
    {
        "id": "epi",
        "num": "End",
        "src_stem": "12_Epilogue",
        "file": "12-epilogue.mp3",
        "script": "12-epilogue.txt",
        "title": "Epilogue",
        "desc": "About Joshua Thomson — theology, pastoring, dark night of the soul, Newcastle, performer.",
        "quiz": [
            {
                "id": "epi-1",
                "type": "single",
                "text": "What did Joshua study before becoming a Pentecostal pastor?",
                "options": [
                    "Applied Theology",
                    "Nuclear engineering",
                    "Marine biology",
                    "Accountancy only",
                ],
            },
            {
                "id": "epi-2",
                "type": "single",
                "text": "Where does he live now, according to the epilogue?",
                "options": [
                    "Newcastle-upon-Tyne",
                    "Paris",
                    "Sydney",
                    "Reykjavik",
                ],
            },
            {
                "id": "epi-3",
                "type": "multiple",
                "text": "Which details match the epilogue? (Select all that apply)",
                "options": [
                    "He is a self-described addict of the interesting",
                    "He worked as a Pentecostal pastor in Northern Ireland",
                    "He now works as a croupier and performer",
                    "He claims never to have left Essex",
                ],
            },
        ],
        "correct": {
            "epi-1": "Applied Theology",
            "epi-2": "Newcastle-upon-Tyne",
            "epi-3": [
                "He is a self-described addict of the interesting",
                "He worked as a Pentecostal pastor in Northern Ireland",
                "He now works as a croupier and performer",
            ],
        },
    },
]


def js_string(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def load_script(stem: str, web_script: str) -> str:
    # Prefer spoken cleaned text matching stem
    src = SPOKEN / f"{stem}.txt"
    if not src.exists():
        raise FileNotFoundError(src)
    text = src.read_text(encoding="utf-8").strip()
    # Write web script copy
    (DEST / web_script).write_text(text + "\n", encoding="utf-8")
    return text


def patch_runtime(runtime: str) -> str:
    runtime = runtime.replace(
        "function isEpisodeUnlocked(index) {\n"
        "      if (index === 0) return true;\n"
        "      return !!lockedState[episodes[index - 1].id];\n"
        "    }",
        "function isEpisodeUnlocked(index) {\n"
        "      return true; // josh-book: all chapters unlocked from the start\n"
        "    }",
    )
    runtime = runtime.replace(
        "function isScriptUnlocked(ep) {\n"
        "      return !!lockedState[ep.id];\n"
        "    }",
        "function isScriptUnlocked(ep) {\n"
        "      return true; // josh-book: scripts available immediately\n"
        "    }",
    )
    # Labels: Chapter / Addendum rather than Episode when num is not int-only
    runtime = runtime.replace(
        'function episodeLabel(ep) {\n'
        '      return ep.intro ? "Intro — " + ep.title : "Episode " + ep.num + " — " + ep.title;\n'
        "    }",
        "function episodeLabel(ep) {\n"
        '      if (ep.intro) return "Intro — " + ep.title;\n'
        '      if (typeof ep.num === "string" && ep.num.startsWith("A")) return "Addendum " + ep.num.slice(1) + " — " + ep.title;\n'
        '      if (ep.num === "End") return "Epilogue — " + ep.title;\n'
        '      return "Chapter " + ep.num + " — " + ep.title;\n'
        "    }",
    )
    runtime = runtime.replace(
        'const lines = ["Brain OS — Quiz Answers", ""];',
        'const lines = ["Experience, Therefore — Quiz Answers", ""];',
    )
    runtime = runtime.replace(
        "Answer from memory after listening — no script until you lock in. Then you can read it and move to the next episode.",
        "Answer from memory after listening if you can. Scripts are available any time. Lock in to see which answers you got right.",
    )
    runtime = runtime.replace(
        ' (nextEpisodeLabel(episodes.indexOf(ep)) ? " Next episode unlocked." : " Walk complete.");',
        ' (nextEpisodeLabel(episodes.indexOf(ep)) ? " On to the next chapter when you are ready." : " Book complete.");',
    )
    runtime = runtime.replace(
        "function nextEpisodeLabel(index) {\n"
        "      if (index >= episodes.length - 1) return null;\n"
        "      const next = episodes[index + 1];\n"
        '      return next.intro ? "Intro" : "Episode " + next.num;\n'
        "    }",
        "function nextEpisodeLabel(index) {\n"
        "      if (index >= episodes.length - 1) return null;\n"
        "      const next = episodes[index + 1];\n"
        '      if (next.intro) return "Intro";\n'
        '      if (typeof next.num === "string" && String(next.num).startsWith("A")) return "Addendum " + String(next.num).slice(1);\n'
        '      if (next.num === "End") return "Epilogue";\n'
        '      return "Chapter " + next.num;\n'
        "    }",
    )
    return runtime


def build_episodes_js() -> tuple[str, str, str]:
    scripts_obj: dict[str, str] = {}
    correct_obj: dict = {}
    episodes = []

    for ch in CHAPTERS:
        script_text = load_script(ch["src_stem"], ch["script"])
        scripts_obj[ch["id"]] = script_text
        correct_obj.update(ch["correct"])

        ep = {
            "id": ch["id"],
            "num": ch["num"],
            "file": ch["file"],
            "script": ch["script"],
            "title": ch["title"],
            "desc": ch["desc"],
            "quiz": ch["quiz"],
        }
        if ch.get("intro"):
            ep["intro"] = True
        episodes.append(ep)

        # stage audio for release upload (not bloating Pages repo)
        src_mp3 = AUDIO_SRC / f"{ch['src_stem']}.mp3"
        if not src_mp3.exists():
            raise FileNotFoundError(src_mp3)
        shutil.copy2(src_mp3, AUDIO_STAGE / ch["file"])

    return (
        "const SCRIPTS = " + json.dumps(scripts_obj, ensure_ascii=False, indent=2) + ";",
        "const CORRECT = " + json.dumps(correct_obj, ensure_ascii=False, indent=2) + ";",
        "const episodes = " + json.dumps(episodes, ensure_ascii=False, indent=2) + ";",
    )


def main() -> None:
    if not LEWIS_HTML.exists():
        raise SystemExit(f"Missing Lewis template: {LEWIS_HTML}")

    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir(parents=True)
    if AUDIO_STAGE.exists():
        shutil.rmtree(AUDIO_STAGE)
    AUDIO_STAGE.mkdir(parents=True)

    html = LEWIS_HTML.read_text(encoding="utf-8")
    css = html[html.index("<style>") : html.index("</style>") + len("</style>")]
    runtime = html[
        html.index("function formatTime") : html.index(
            "</script>", html.index("function formatTime")
        )
    ]
    runtime = patch_runtime(runtime)

    scripts_js, correct_js, episodes_js = build_episodes_js()

    page = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Experience, Therefore — Joshua Thomson</title>
  <meta name="description" content="Audiobook companion for Experience, Therefore by Joshua Thomson. Listen chapter by chapter with scripts and recall checks. All chapters unlocked.">
  __CSS__
</head>
<body>
  <div class="wrap">
    <header>
      <div class="badge">tyneside.software · josh-book</div>
      <h1>Experience, Therefore</h1>
      <p class="subtitle">The Existence of God and The Impossibility Of Hell — audiobook companion by Joshua Thomson. Listen, read the script, and try the recall checks.</p>
      <div class="meta">
        <span>13 parts</span>
        <span>Chapters + addenda + epilogue</span>
        <span>All unlocked</span>
      </div>
    </header>

    <div class="instructions">
      <strong>How to use this:</strong> Every chapter is unlocked from the start — listen in any order. After each part, try the recall check and press <strong>Lock in answers</strong> to see feedback (you do not need a perfect score). Use <strong>Read script</strong> for the full text of that part. Progress saves on this device.
    </div>

    <div class="quiz-toolbar">
      <p><strong>Recall check:</strong> Answer the quiz for practice and lock in to see results. Export/import if you want to continue on another device.</p>
      <div class="quiz-toolbar-actions">
        <button type="button" class="btn-copy" id="copy-all">Copy all Q&amp;A</button>
        <button type="button" class="btn-copy" id="export-progress">Export progress</button>
        <button type="button" class="btn-copy" id="import-progress">Import progress</button>
        <button type="button" class="btn-reset" id="clear-session">Reset progress</button>
      </div>
    </div>

    <div class="progress-transfer" id="import-panel">
      <label for="import-code">Paste your progress code</label>
      <textarea id="import-code" placeholder="Paste the code from Export progress…"></textarea>
      <div class="progress-transfer-actions">
        <button type="button" class="btn-lock" id="import-confirm">Restore progress</button>
        <button type="button" class="btn-reset" id="import-cancel">Cancel</button>
      </div>
    </div>

    <div class="episode-list" id="episodes"></div>

    <footer>
      Experience, therefore.<br>
      <strong>Sentio Ergo Sum</strong> — Joshua Thomson
    </footer>
  </div>

  <div class="copy-toast" id="copy-toast" aria-live="polite">Copied to clipboard</div>

  <script>
    // Prefer hosted release audio (keeps Pages repo small). Local audio/ works if empty.
    const AUDIO_BASE_URL = __AUDIO_BASE__;

    function pageBaseUrl() {
      const { origin, pathname } = window.location;
      if (pathname.endsWith("/")) return origin + pathname;
      const last = pathname.split("/").pop() || "";
      if (/\\.[a-z0-9]+$/i.test(last)) return origin + pathname.replace(/[^/]+$/, "");
      return origin + pathname + "/";
    }

    function pageAssetUrl(relativePath) {
      return new URL(relativePath.replace(/^\\//, ""), pageBaseUrl()).href;
    }

    function audioUrl(filename) {
      const base = AUDIO_BASE_URL.trim().replace(/\\/$/, "");
      return base ? base + "/" + filename : pageAssetUrl("audio/" + filename);
    }

    const STORAGE_KEY = "josh-book-quiz-answers";
    const LOCKED_KEY = "josh-book-quiz-locked";
    const PROGRESS_PREFIX = "joshbook1:";

    __SCRIPTS_JS__

    __CORRECT_JS__

    __EPISODES_JS__

    const list = document.getElementById("episodes");
    const copyToast = document.getElementById("copy-toast");
    const episodeCards = new Map();
    let currentAudio = null;
    let currentCard = null;
    let quizAnswers = loadAnswers();
    let lockedState = loadLocked();

    __RUNTIME__
  </script>
</body>
</html>
"""
    page = (
        page.replace("__CSS__", css)
        .replace("__AUDIO_BASE__", js_string(AUDIO_BASE_URL))
        .replace("__SCRIPTS_JS__", scripts_js)
        .replace("__CORRECT_JS__", correct_js)
        .replace("__EPISODES_JS__", episodes_js)
        .replace("__RUNTIME__", runtime)
    )

    (DEST / "index.html").write_text(page, encoding="utf-8")

    # Also keep scripts folder mirror
    scripts_dir = DEST / "scripts"
    scripts_dir.mkdir(exist_ok=True)
    for ch in CHAPTERS:
        shutil.copy2(DEST / ch["script"], scripts_dir / ch["script"])

    # Tiny placeholder so audio/ path exists if someone clears AUDIO_BASE_URL
    (DEST / "audio").mkdir(exist_ok=True)
    (DEST / "audio" / "README.txt").write_text(
        "MP3s are hosted on the GitHub Release set as AUDIO_BASE_URL in index.html.\n",
        encoding="utf-8",
    )

    print(f"Built {DEST}")
    print(f"  index.html {(DEST / 'index.html').stat().st_size:,} bytes")
    print(f"  staged audio: {AUDIO_STAGE} ({len(list(AUDIO_STAGE.glob('*.mp3')))} files)")
    print(f"  scripts: {len(list(DEST.glob('*.txt')))}")
    print(f"  AUDIO_BASE_URL: {AUDIO_BASE_URL}")


if __name__ == "__main__":
    main()
