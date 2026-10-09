# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Language metrics per pitch transcript, written to data/language.csv.

Input: a folder with one subfolder per study (`hackathon/`, `demoday/`), each holding one
transcript per pitch named `<slug>.txt`, one line per segment as "[mm:ss] text" (the format
whisper.cpp prints). The transcripts are not in this repository; see README.md.

Every metric is a plain count over the transcript text. Numbers are counted one per number:
"$70,000", "330 million", "1.5", "10x" and "a hundred thousand" are one number each; digits
inside a word ("web3", "x402", "a16z") are not numbers.

Usage: uv run rhetoric.py <transcripts_dir> [<out_csv>]
"""

from __future__ import annotations

import csv
import logging
import re
import sys
from pathlib import Path

log = logging.getLogger("rhetoric")

STAMP = re.compile(r"^\[(\d+):(\d+)\]")
TS = re.compile(r"^\[\d+:\d+\]\s*")
NOISE = re.compile(r"^\s*[\[(]?\s*(music|applause|blank_audio|silence)\s*[\])]?\.?\s*$", re.I)

SCALE = r"(?:hundred|thousand|million|billion|trillion|percent)"
NUMBER_WORD = (
    r"(?:hundred|thousand|million|billion|trillion|percent|half|double|twice|"
    r"ten|twenty|thirty|fifty|dozen)"
)
# One match per number: a digit run with its separators, currency, suffix and scale words,
# or a number word with its scale words. Digits glued to letters or after a hyphen are skipped.
NUMBER = re.compile(
    rf"(?<![A-Za-z0-9-])[$€£]?\d[\d,.]*(?:bn|st|nd|rd|th|[kmbxs])?\+?%?(?![A-Za-z0-9])"
    rf"(?:[\s-]+{SCALE}\b)*"
    rf"|\b{NUMBER_WORD}(?:[\s-]+{SCALE})*\b",
    re.IGNORECASE,
)
ANALOGY = re.compile(
    r"\b(?:it's like|it is like|think of (?:it|us|this)|imagine|just like|similar to|"
    r"like (?:a|an) \w+ for)\b|\bthe [A-Z][A-Za-z]+ (?:of|for)\b"
)
CONTRAST = re.compile(r"\b(?:but|instead|however|yet|except)\b")
YOU = re.compile(r"\b(?:you|your)\b")
I_STORY = re.compile(r"\b(?:I was|when I|I saw|I spent|I worked|I built|I ran|my )\b")
PRODUCT_VERBS = re.compile(r"\b(?:lets|helps|allows|enables|turns|makes)\b")
FIRST_ONLY = re.compile(r"\b(?:the first|the only|first ever)\b")
BUZZ = [
    "revolutionary", "revolutionize", "game-changing", "game changer", "seamless", "disrupt",
    "next-generation", "next generation", "cutting-edge", "cutting edge", "innovative", "unlock",
    "empower", "paradigm", "groundbreaking", "leverage", "frictionless", "world's first",
]  # fmt: skip
JARGON = [
    "web3", "decentralized", "on-chain", "onchain", "blockchain", "token", "defi", "dao",
    "smart contract", "wallet", "nft", "liquidity", "staking", "protocol", "depin", "trustless",
    "permissionless", "airdrop", "memecoin", "tvl", "composab",
]  # fmt: skip
COLUMNS = [
    "study", "slug", "duration_s", "words", "wpm", "jargon_per_min", "buzz_per_min",
    "first_only_claims", "words_per_sentence", "share_short_sentences", "share_long_sentences",
    "share_sentences_with_number", "numbers_per_min", "analogies", "contrast_per_min",
    "you_per_100w", "i_story_per_100w", "questions", "product_verbs_per_min",
    "flesch_reading_ease", "syllables_per_word",
]  # fmt: skip


class TranscriptError(ValueError):
    """A transcript with no timestamped line."""


def syllables(word: str) -> int:
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups) - (1 if w.endswith("e") and len(groups) > 1 else 0)
    return max(n, 1)


def speech_lines(text: str) -> list[str]:
    """Timestamped lines, without whisper's non-speech markers such as "[Music]"."""
    out: list[str] = []
    for ln in text.splitlines():
        body = TS.sub("", ln).strip()
        if body and not NOISE.match(body):
            out.append(ln)
    return out


def count_numbers(sentence: str) -> int:
    return len(NUMBER.findall(sentence))


def features(lines: list[str]) -> dict[str, float]:
    stamps = [int(m.group(1)) * 60 + int(m.group(2)) for ln in lines if (m := STAMP.match(ln))]
    if not stamps:
        raise TranscriptError("no timestamped line")
    raw = " ".join(TS.sub("", ln).strip() for ln in lines if ln.strip())
    low = raw.lower()
    sents = [s.strip() for s in re.split(r"(?<=[.?!])\s+", raw) if len(s.split()) >= 2]
    words = raw.split()
    nw, ns = len(words), max(len(sents), 1)
    duration = max(stamps) + 5
    mins = max(duration / 60, 0.25)
    syl = sum(syllables(w) for w in words)
    lens = [len(s.split()) for s in sents]
    return {
        "duration_s": duration,
        "words": nw,
        "wpm": round(nw / mins, 1),
        "jargon_per_min": round(sum(low.count(j) for j in JARGON) / mins, 2),
        "buzz_per_min": round(sum(low.count(b) for b in BUZZ) / mins, 2),
        "first_only_claims": len(FIRST_ONLY.findall(low)),
        "words_per_sentence": round(nw / ns, 1),
        "share_short_sentences": round(sum(1 for x in lens if x <= 12) / ns, 2),
        "share_long_sentences": round(sum(1 for x in lens if x >= 25) / ns, 2),
        "share_sentences_with_number": round(sum(1 for s in sents if NUMBER.search(s)) / ns, 2),
        "numbers_per_min": round(sum(count_numbers(s) for s in sents) / mins, 2),
        "analogies": len(ANALOGY.findall(raw)),
        "contrast_per_min": round(len(CONTRAST.findall(low)) / mins, 2),
        "you_per_100w": round(100 * len(YOU.findall(low)) / max(nw, 1), 2),
        "i_story_per_100w": round(100 * len(I_STORY.findall(raw)) / max(nw, 1), 2),
        "questions": raw.count("?"),
        "product_verbs_per_min": round(len(PRODUCT_VERBS.findall(low)) / mins, 2),
        "flesch_reading_ease": round(206.835 - 1.015 * (nw / ns) - 84.6 * (syl / max(nw, 1)), 1),
        "syllables_per_word": round(syl / max(nw, 1), 2),
    }


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    if len(sys.argv) < 2:
        log.error("usage: rhetoric.py <transcripts_dir> [<out_csv>]")
        return 2
    src = Path(sys.argv[1])
    out = (
        Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).parent / "data" / "language.csv"
    )
    rows: list[dict[str, object]] = []
    for study in ("hackathon", "demoday"):
        for path in sorted((src / study).glob("*.txt")):
            try:
                feats = features(speech_lines(path.read_text()))
            except TranscriptError as exc:
                log.warning("skipped %s: %s", path, exc)
                continue
            rows.append({"study": study, "slug": path.stem, **feats})
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    log.info("%d transcripts -> %s", len(rows), out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
