# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Every count and test of the study, from the CSVs in data/. Writes results.md.

Standard library only. Fisher exact and McNemar exact are computed exactly; Mann-Whitney uses
the normal approximation with tie and continuity correction (as scipy's asymptotic method).

Usage: uv run analyze.py   (or: python3 analyze.py)
"""

from __future__ import annotations

import csv
import logging
import math
import statistics
from collections import Counter
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

log = logging.getLogger("analyze")

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
AGREEMENT_FLOOR = 0.6
# Dropped before the comparison was read: test-level agreement below AGREEMENT_FLOOR on the
# original second pass of 21 projects (0.57, 0.57 and 0.5). Three of those 21 were coded in the
# same batch for another question and are not published, so the 18 in data/second_pass.csv
# give slightly different values; see README.md.
DROPPED = {"Opens with the product", "Opens by introducing the team", "Full-time commitment stated"}
ALPHA = 0.05
POWER = 0.8
YEAR_2024 = {"renaissance", "radar"}

Row = dict[str, str]


@dataclass(frozen=True, slots=True)
class Test:
    label: str
    field: str
    pred: Callable[[str], bool]


def items(v: str) -> list[str]:
    return [x for x in v.split(";") if x]


def any_but(v: str, empty: str) -> bool:
    return any(x != empty for x in items(v))


TESTS: list[Test] = [
    Test("Opens with the problem or a story", "hook_type", lambda v: v == "problem_story"),
    Test("Opens with the product", "hook_type", lambda v: v == "product_first"),
    Test("Opens by introducing the team", "hook_type", lambda v: v == "team_intro"),
    Test("Problem stated with a number", "problem_quantified", lambda v: v == "true"),
    Test("A specific, named user", "named_user", lambda v: v == "specific"),
    Test("Product running on screen", "live_product_shown", lambda v: v == "working_product"),
    Test("Onchain proof on screen", "onchain_proof_shown", lambda v: v == "true"),
    Test("Explicit why Solana", "why_solana", lambda v: v != "absent"),
    Test("Existed before the hackathon", "existed_before_hackathon", lambda v: v == "true"),
    Test("Revenue model stated", "business_model", lambda v: v != "none_stated"),
    Test("Market size with a number", "market_size", lambda v: v == "tam_number"),
    Test("Competition mentioned", "competition", lambda v: v == "true"),
    Test("Full-time commitment stated", "full_time_commitment", lambda v: v == "true"),
    Test("An ask or next steps", "ask_or_next_steps", lambda v: v == "true"),
    Test("Token mentioned", "token", lambda v: v != "absent"),
    Test("Face on camera", "face_on_camera", lambda v: v == "true"),
    Test("B2B (incl. B2B2C)", "audience", lambda v: v in {"b2b", "b2b2c"}),
    Test("Real-world domain (incl. both)", "domain", lambda v: v in {"real_world", "both"}),
    Test("Any traction", "traction", lambda v: any_but(v, "none")),
    Test("Revenue as the traction", "traction", lambda v: "revenue" in items(v)),
    Test("A team credential", "team_credentials", lambda v: any_but(v, "none_stated")),
    Test("Traction with a number", "traction_number_stated", lambda v: v == "true"),
]  # fmt: skip
BY_LABEL = {t.label: t for t in TESTS}
LANGUAGE = [
    "words", "words_per_sentence", "share_short_sentences", "share_long_sentences",
    "share_sentences_with_number", "numbers_per_min", "analogies", "contrast_per_min",
    "you_per_100w", "i_story_per_100w", "questions", "product_verbs_per_min",
    "flesch_reading_ease", "syllables_per_word",
]  # fmt: skip
DESCRIPTIVE = ["duration_s", "wpm", "jargon_per_min"]
DD_CONTINUOUS = [
    "duration_s", "wpm", "numbers_per_min", "jargon_per_min", "buzz_per_min",
    "first_only_claims", "t_what_it_does_s", "t_problem_s", "t_product_on_screen_s",
]  # fmt: skip
HYPE = [
    ("agent-control-plane", ("frontier",)),
    ("token-launch", ("renaissance", "radar", "breakout", "cypherpunk", "frontier")),
    ("verifiable-records", ("renaissance", "radar", "breakout", "cypherpunk", "frontier")),
    ("depin", ("renaissance", "radar", "breakout")),
    ("depin", ("cypherpunk", "frontier")),
    ("games", ("renaissance",)),
    ("games", ("cypherpunk",)),
]


# ---------- data ----------


def load(name: str) -> list[Row]:
    with (DATA / name).open(newline="") as fh:
        return list(csv.DictReader(fh))


def verdict(row: Row, test: Test) -> bool | None:
    v = row.get(test.field, "")
    return None if v == "" else test.pred(v)


def share(rows: Sequence[Row], test: Test) -> tuple[int, int]:
    known = [x for x in (verdict(r, test) for r in rows) if x is not None]
    return sum(known), len(known)


def nums(rows: Sequence[Row], field: str) -> list[float]:
    return [float(r[field]) for r in rows if r.get(field, "") != ""]


def median(xs: Sequence[float]) -> float:
    return statistics.median(xs) if xs else math.nan


# ---------- statistics ----------


def fisher_p(a: int, b: int, c: int, d: int) -> float:
    """Two-sided Fisher exact test for [[a, b], [c, d]]."""
    n, r1, c1 = a + b + c + d, a + b, a + c
    denom = math.comb(n, c1)

    def pmf(x: int) -> float:
        return math.comb(r1, x) * math.comb(n - r1, c1 - x) / denom

    p0 = pmf(a)
    lo, hi = max(0, r1 + c1 - n), min(r1, c1)
    return min(1.0, sum(p for x in range(lo, hi + 1) if (p := pmf(x)) <= p0 * (1 + 1e-9)))


def fisher_shares(w: tuple[int, int], c: tuple[int, int]) -> float:
    if not w[1] or not c[1]:
        return math.nan
    return fisher_p(w[0], w[1] - w[0], c[0], c[1] - c[0])


def holm(ps: Sequence[float]) -> list[float]:
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    m, running = len(ps), 0.0
    adj = [0.0] * m
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (m - rank) * ps[i]))
        adj[i] = running
    return adj


def mann_whitney_p(a: Sequence[float], b: Sequence[float]) -> float:
    """Two-sided Mann-Whitney U, normal approximation with tie and continuity correction."""
    n1, n2 = len(a), len(b)
    if not n1 or not n2:
        return math.nan
    pooled = sorted([(x, 0) for x in a] + [(x, 1) for x in b])
    ranks = [0.0] * len(pooled)
    ties = 0.0
    i = 0
    while i < len(pooled):
        j = i
        while j + 1 < len(pooled) and pooled[j + 1][0] == pooled[i][0]:
            j += 1
        for k in range(i, j + 1):
            ranks[k] = (i + j) / 2 + 1
        t = j - i + 1
        ties += t**3 - t
        i = j + 1
    r1 = sum(r for r, (_, g) in zip(ranks, pooled, strict=True) if g == 0)
    u = r1 - n1 * (n1 + 1) / 2
    n = n1 + n2
    sd = math.sqrt(n1 * n2 / 12 * ((n + 1) - ties / (n * (n - 1))))
    if sd == 0:
        return 1.0
    z = (abs(u - n1 * n2 / 2) - 0.5) / sd
    return min(1.0, math.erfc(max(z, 0.0) / math.sqrt(2)))


def mcnemar_p(gained: int, lost: int) -> float:
    """Exact McNemar: two-sided binomial test on the discordant pairs."""
    n = gained + lost
    if n == 0:
        return math.nan
    k = min(gained, lost)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2**n)


def agreement(pairs: Sequence[tuple[bool | None, bool | None]]) -> tuple[float, float, int]:
    """Percent agreement (a missing value against a present one counts as a disagreement)
    and Cohen's kappa on the pairs where both passes gave a value."""
    some = [(x, y) for x, y in pairs if x is not None or y is not None]
    pct = sum(x == y for x, y in some) / len(some) if some else math.nan
    both = [(x, y) for x, y in pairs if x is not None and y is not None]
    if not both:
        return pct, math.nan, 0
    n = len(both)
    po = sum(x == y for x, y in both) / n
    p1 = sum(x for x, _ in both) / n
    p2 = sum(y for _, y in both) / n
    pe = p1 * p2 + (1 - p1) * (1 - p2)
    kappa = (po - pe) / (1 - pe) if pe < 1 else math.nan
    return pct, kappa, len(some)


def binom_pmf(k: int, n: int, p: float) -> float:
    return math.comb(n, k) * p**k * (1 - p) ** (n - k)


def detectable(nw: int, nc: int, pc: float) -> tuple[float | None, float | None]:
    """Winner rates (below, above the control rate pc) that a two-sided Fisher test at
    ALPHA detects with POWER, given the sample sizes. None if no rate in [0, 1] reaches it."""
    region = [
        (a, c)
        for a in range(nw + 1)
        for c in range(nc + 1)
        if fisher_p(a, nw - a, c, nc - c) <= ALPHA
    ]
    ctrl = [binom_pmf(c, nc, pc) for c in range(nc + 1)]

    def power(pw: float) -> float:
        win = [binom_pmf(a, nw, pw) for a in range(nw + 1)]
        return sum(win[a] * ctrl[c] for a, c in region)

    grid = [i / 1000 for i in range(1001)]
    below = [p for p in grid if p < pc and power(p) >= POWER]
    above = [p for p in grid if p > pc and power(p) >= POWER]
    return (max(below) if below else None, min(above) if above else None)


def hypergeom(total: int, marked: int, draws: int) -> list[float]:
    denom = math.comb(total, draws)
    return [
        math.comb(marked, k) * math.comb(total - marked, draws - k) / denom
        for k in range(min(marked, draws) + 1)
    ]


def convolve(a: Sequence[float], b: Sequence[float]) -> list[float]:
    out = [0.0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


# ---------- formatting ----------


def fp(p: float) -> str:
    if math.isnan(p):
        return "n/a"
    if p < 0.001:
        return "<0.001"
    return f"{p:.3f}" if p < 0.1 else f"{p:.2f}"


def fx(x: float, nd: int = 2) -> str:
    return "n/a" if math.isnan(x) else f"{x:.{nd}f}"


def tag(label: str) -> str:
    return f"{label} (dropped)" if label in DROPPED else label


def frac(s: tuple[int, int]) -> str:
    return f"{s[0]}/{s[1]}"


def pct(x: float | None) -> str:
    return "none" if x is None else f"{round(100 * x)}%"


# ---------- sections ----------


def sample_section(pairs: list[Row], proj: list[Row]) -> list[str]:
    accel_coded = sum(r["accelerated_coded"] == "true" for r in pairs)
    drawn = [r for r in pairs if r["control_slug"]]
    ctrl_coded = sum(r["control_coded"] == "true" for r in drawn)
    lost = len(drawn) - ctrl_coded
    groups = Counter(r["group"] for r in proj)
    return [
        "## Sample",
        "",
        f"- Accelerated companies: {len(pairs)}; with a codable hackathon pitch video: "
        f"{accel_coded} (lost {len(pairs) - accel_coded}).",
        f"- Controls drawn: {len(drawn)} (one company had no eligible control); coded: "
        f"{ctrl_coded}; lost {lost} of {len(drawn)} ({round(100 * lost / len(drawn))}%).",
        f"- Analysed: {groups['winner']} winners, {groups['control']} controls.",
        "",
    ]


def agreement_table(
    first: dict[str, Row], second: dict[str, Row]
) -> dict[str, tuple[float, float, int]]:
    out: dict[str, tuple[float, float, int]] = {}
    for t in TESTS:
        pairs = [(verdict(first[s], t), verdict(r, t)) for s, r in second.items() if s in first]
        out[t.label] = agreement(pairs)
    return out


def main_section(
    proj: list[Row], agree: dict[str, tuple[float, float, int]], n_second: int
) -> tuple[list[str], dict[str, float]]:
    win = [r for r in proj if r["group"] == "winner"]
    ctl = [r for r in proj if r["group"] == "control"]
    shares = {t.label: (share(win, t), share(ctl, t)) for t in TESTS}
    ps = {lab: fisher_shares(w, c) for lab, (w, c) in shares.items()}
    labels = [t.label for t in TESTS]
    adj22 = dict(zip(labels, holm([ps[x] for x in labels]), strict=True))
    kept = [x for x in labels if x not in DROPPED]
    adjkept = dict(zip(kept, holm([ps[x] for x in kept]), strict=True))
    lines = [
        "## Winners vs controls: coded variables",
        "",
        f"Two-sided Fisher exact. Holm over all {len(labels)} tests, and over the {len(kept)} "
        f"left after the {len(DROPPED)} dropped for low agreement. Agreement (percent) and "
        f"Cohen's kappa: second pass on {n_second} projects (same model, same prompt), at the "
        "level of each test; n = projects where at least one pass gave a value.",
        "",
        f"| Variable | Winners | Controls | p | Holm ({len(labels)}) | Holm ({len(kept)}) "
        "| Agreement | Kappa | n |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for lab in sorted(labels, key=lambda x: ps[x]):
        w, c = shares[lab]
        pa, k, n = agree[lab]
        hk = "dropped" if lab in DROPPED else fp(adjkept[lab])
        lines.append(
            f"| {lab} | {frac(w)} | {frac(c)} | {fp(ps[lab])} | {fp(adj22[lab])} | {hk} | "
            f"{fx(pa)} | {fx(k)} | {n} |"
        )
    lines.append("")
    return lines, ps


def sub_sections(proj: list[Row]) -> list[str]:
    win = [r for r in proj if r["group"] == "winner"]
    ctl = [r for r in proj if r["group"] == "control"]
    any_tr = BY_LABEL["Any traction"]
    num_tr = BY_LABEL["Traction with a number"]
    w_tr = [r for r in win if verdict(r, any_tr)]
    c_tr = [r for r in ctl if verdict(r, any_tr)]
    ws, cs = share(w_tr, num_tr), share(c_tr, num_tr)
    lines = [
        "## Traction with a number, among projects that cite traction",
        "",
        f"Winners {frac(ws)}, controls {frac(cs)}, Fisher p {fp(fisher_shares(ws, cs))}.",
        "",
        "## By period (2024: Renaissance, Radar; 2025-26: Breakout, Cypherpunk, Frontier)",
        "",
        "| Variable | Winners 2024 | Controls 2024 | p | Winners 2025-26 | Controls 2025-26 | p |",
        "|---|---|---|---|---|---|---|",
    ]
    for lab in ("Any traction", "A team credential", "Face on camera"):
        t = BY_LABEL[lab]
        cells: list[str] = []
        for early in (True, False):
            w = share([r for r in win if (r["hackathon"] in YEAR_2024) == early], t)
            c = share([r for r in ctl if (r["hackathon"] in YEAR_2024) == early], t)
            cells += [frac(w), frac(c), fp(fisher_shares(w, c))]
        lines.append(f"| {lab} | " + " | ".join(cells) + " |")
    types: dict[str, Counter[str]] = {
        g: Counter(x for r in rows for x in set(items(r["traction"])))
        for g, rows in (("winners", win), ("controls", ctl))
    }
    lines += ["", "## Traction by type (projects per type)", ""]
    for g, cnt in types.items():
        lines.append(f"- {g}: " + ", ".join(f"{k} {v}" for k, v in cnt.most_common()))
    no_tr = sorted(r["slug"] for r in win if verdict(r, any_tr) is False)
    lines += ["", f"Winners citing no traction ({len(no_tr)}): {', '.join(no_tr)}.", ""]
    return lines


def language_section(proj: list[Row], lang: dict[str, Row]) -> tuple[list[str], list[float]]:
    win = [lang[r["slug"]] for r in proj if r["group"] == "winner"]
    ctl = [lang[r["slug"]] for r in proj if r["group"] == "control"]
    lines = [
        "## Language metrics (rhetoric.py), winners vs controls",
        "",
        "Medians; two-sided Mann-Whitney. Numbers are counted one per number.",
        "",
        "| Metric | Winners | Controls | p |",
        "|---|---|---|---|",
    ]
    ps: list[float] = []
    for m in LANGUAGE:
        a, b = nums(win, m), nums(ctl, m)
        p = mann_whitney_p(a, b)
        ps.append(p)
        lines.append(f"| {m} | {fx(median(a))} | {fx(median(b))} | {fp(p)} |")
    lines += ["", "Not tested, medians only:", ""]
    for m in DESCRIPTIVE:
        lines.append(
            f"- {m}: winners {fx(median(nums(win, m)), 1)}, controls {fx(median(nums(ctl, m)), 1)}"
        )
    t_win = [r for r in proj if r["group"] == "winner"]
    t_ctl = [r for r in proj if r["group"] == "control"]
    lines.append(
        f"- seconds to the problem: winners {fx(median(nums(t_win, 't_problem_s')), 1)}, "
        f"controls {fx(median(nums(t_ctl, 't_problem_s')), 1)}"
    )
    lines.append("")
    return lines, ps


def power_section(proj: list[Row], ps: dict[str, float]) -> list[str]:
    win = [r for r in proj if r["group"] == "winner"]
    ctl = [r for r in proj if r["group"] == "control"]
    lines = [
        "## What the sample could detect",
        "",
        f"For each variable with p >= 0.1: the winner rate a two-sided Fisher test at "
        f"{ALPHA} would detect with {round(100 * POWER)}% power, holding the control rate "
        "and both sample sizes as observed.",
        "",
        "| Variable | Winners | Controls (rate) | Detectable winner rate: below / above |",
        "|---|---|---|---|",
    ]
    for t in TESTS:
        if ps[t.label] < 0.1:
            continue
        w, c = share(win, t), share(ctl, t)
        if not c[1] or not w[1]:
            continue
        pc = c[0] / c[1]
        lo, hi = detectable(w[1], c[1], pc)
        lines.append(f"| {t.label} | {frac(w)} | {frac(c)} ({pct(pc)}) | {pct(lo)} / {pct(hi)} |")
    lines.append("")
    return lines


def demoday_section(
    dd: list[Row], proj: list[Row], lang: dict[str, Row], dd_lang: dict[str, Row]
) -> list[str]:
    for r in dd:
        r.update(
            {k: v for k, v in dd_lang[r["company_slug"]].items() if k not in {"study", "slug"}}
        )
    early = [r for r in dd if r["cohort"] != "C5"]
    raised = [r for r in early if r["raised_after_demo_day"] == "true"]
    rest = [r for r in early if r["raised_after_demo_day"] != "true"]
    cohorts = sorted({r["cohort"] for r in dd})
    lines = [
        "## Demo Day",
        "",
        f"{len(dd)} Demo Day pitches, cohorts {cohorts[0]}-{cohorts[-1]}: "
        + ", ".join(f"{c} {sum(r['cohort'] == c for r in dd)}" for c in cohorts)
        + ".",
        "Outcomes: "
        + ", ".join(f"{k} {v}" for k, v in Counter(r["outcome"] for r in dd).most_common())
        + ".",
        "",
        f"### Raised a new round after Demo Day vs the rest (cohorts {cohorts[0]}-C4: "
        f"{len(raised)} vs {len(rest)})",
        "",
        "Raised by cohort: "
        + ", ".join(
            f"{c} {sum(r['cohort'] == c and r['raised_after_demo_day'] == 'true' for r in dd)}"
            f"/{sum(r['cohort'] == c for r in dd)}"
            for c in cohorts
            if c != "C5"
        )
        + ".",
        "",
        "| Variable | Raised | Rest | p | Holm |",
        "|---|---|---|---|---|",
    ]
    rows: list[tuple[str, str, str, float]] = []
    for t in TESTS:
        a, b = share(raised, t), share(rest, t)
        rows.append((tag(t.label), frac(a), frac(b), fisher_shares(a, b)))
    for m in DD_CONTINUOUS:
        a, b = nums(raised, m), nums(rest, m)
        rows.append((f"{m} (median)", fx(median(a)), fx(median(b)), mann_whitney_p(a, b)))
    valid = [i for i, r in enumerate(rows) if not math.isnan(r[3])]
    adj = dict(zip(valid, holm([rows[i][3] for i in valid]), strict=True))
    for i in sorted(range(len(rows)), key=lambda i: (math.isnan(rows[i][3]), rows[i][3])):
        lab, a, b, p = rows[i]
        lines.append(f"| {lab} | {a} | {b} | {fp(p)} | {fp(adj[i]) if i in adj else 'n/a'} |")
    lines += ["", f"Holm over the {len(valid)} tests in this table.", ""]

    winners = {r["slug"]: r for r in proj if r["group"] == "winner"}
    pairs = [(winners[r["project_slug"]], r) for r in dd if r["project_slug"] in winners]
    lines += [
        f"### Same company, hackathon pitch vs Demo Day pitch ({len(pairs)} pairs)",
        "",
        "| Variable | n | Hackathon | Demo Day | Gained | Lost | McNemar p |",
        "|---|---|---|---|---|---|---|",
    ]
    for t in TESTS:
        trip = [(verdict(h, t), verdict(d, t)) for h, d in pairs]
        both = [(x, y) for x, y in trip if x is not None and y is not None]
        gained = sum(1 for x, y in both if not x and y)
        lost = sum(1 for x, y in both if x and not y)
        yes_h, yes_d = sum(x for x, _ in both), sum(y for _, y in both)
        lines.append(
            f"| {tag(t.label)} | {len(both)} | {yes_h} | {yes_d} | "
            f"{gained} | {lost} | {fp(mcnemar_p(gained, lost))} |"
        )
    lines += [
        "",
        "| Metric | Hackathon median | Demo Day median | Lower at Demo Day |",
        "|---|---|---|---|",
    ]
    for m in ("duration_s", "wpm", "numbers_per_min", "jargon_per_min"):
        both_m = [(float(lang[h["slug"]][m]), float(d[m])) for h, d in pairs if d.get(m)]
        lower = sum(1 for x, y in both_m if y < x)
        med_h, med_d = median([x for x, _ in both_m]), median([y for _, y in both_m])
        lines.append(f"| {m} | {fx(med_h)} | {fx(med_d)} | {lower}/{len(both_m)} |")
    ask = BY_LABEL["An ask or next steps"]
    a_dd = share(dd, ask)
    a_hk = share([h for h, _ in pairs], ask)
    lines += [
        "",
        f"An ask or next steps, all Demo Day pitches vs the paired hackathon pitches: "
        f"{frac(a_dd)} vs {frac(a_hk)} (Fisher p {fp(fisher_shares(a_dd, a_hk))}).",
        "",
    ]
    return lines


def second_pass_dd(dd: list[Row], second: list[Row]) -> list[str]:
    first = {r["company_slug"]: r for r in dd}
    sec = {r["slug"]: r for r in second if r["study"] == "demoday"}
    agree = agreement_table(first, sec)
    low = [lab for lab, (p, _, _) in agree.items() if p < AGREEMENT_FLOOR]
    return [
        f"Demo Day second pass: {len(sec)} pitches; tests with agreement below "
        f"{AGREEMENT_FLOOR}: {', '.join(low) if low else 'none'}.",
        "",
    ]


def hype_section(cats: list[Row]) -> list[str]:
    totals = {r["hackathon"]: r for r in cats if r["category"] == "_all"}
    by = {(r["hackathon"], r["category"]): r for r in cats}
    lines = [
        "## Category share of submissions vs wins (colosseum-copilot primary category)",
        "",
        "Expected wins = the category's share of each hackathon's submissions times that "
        "hackathon's winners. P = exact probability, if winners were drawn at random from "
        "submissions within each hackathon, of a count at least as far from expected in the "
        "observed direction.",
        "",
        "| Category | Hackathons | Submissions | Wins | Expected | P |",
        "|---|---|---|---|---|---|",
    ]
    for cat, hacks in HYPE:
        dist: list[float] = [1.0]
        subs = wins = 0
        expected = 0.0
        for h in hacks:
            r = by.get((h, cat))
            s = int(r["submissions"]) if r else 0
            w = int(r["winners"]) if r else 0
            tot, tw = int(totals[h]["submissions"]), int(totals[h]["winners"])
            subs, wins = subs + s, wins + w
            expected += tw * s / tot
            dist = convolve(dist, hypergeom(tot, s, tw))
        p = sum(dist[: wins + 1]) if wins <= expected else sum(dist[wins:])
        lines.append(
            f"| {cat} | {', '.join(hacks)} | {subs} | {wins} | {expected:.1f} | {fp(min(p, 1.0))} |"
        )
    lines += [
        "",
        f"All five hackathons: {sum(int(t['submissions']) for t in totals.values())} "
        f"submissions, {sum(int(t['winners']) for t in totals.values())} winners.",
        "",
    ]
    return lines


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    proj = load("projects.csv")
    pairs = load("pairs.csv")
    second = load("second_pass.csv")
    dd = load("demoday.csv")
    cats = load("categories.csv")
    lang_rows = load("language.csv")
    lang = {r["slug"]: r for r in lang_rows if r["study"] == "hackathon"}
    dd_lang = {r["slug"]: r for r in lang_rows if r["study"] == "demoday"}

    first = {r["slug"]: r for r in proj}
    sec = {r["slug"]: r for r in second if r["study"] == "hackathon"}
    agree = agreement_table(first, sec)
    main_lines, ps = main_section(proj, agree, len(sec))
    lang_lines, lang_ps = language_section(proj, lang)
    all36 = holm([ps[t.label] for t in TESTS] + lang_ps)
    robust = [t.label for t, p in zip(TESTS, all36[: len(TESTS)], strict=True) if p < ALPHA]

    out = [
        "# Results (written by analyze.py; do not edit by hand)",
        "",
        *sample_section(pairs, proj),
        *main_lines,
        f"Holm over all {len(all36)} tests (the {len(TESTS)} above plus the {len(LANGUAGE)} "
        f"language metrics): below {ALPHA} for {', '.join(robust)}.",
        "",
        *sub_sections(proj),
        *lang_lines,
        *power_section(proj, ps),
        *demoday_section(dd, proj, lang, dd_lang),
        *second_pass_dd(dd, second),
        *hype_section(cats),
    ]
    (HERE / "results.md").write_text("\n".join(out))
    log.info("wrote %s", HERE / "results.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
