# Results (written by analyze.py; do not edit by hand)

## Sample

- Accelerated companies: 61; with a codable hackathon pitch video: 43 (lost 18).
- Controls drawn: 60 (one company had no eligible control); coded: 47; lost 13 of 60 (22%).
- Analysed: 43 winners, 47 controls.

## Winners vs controls: coded variables

Two-sided Fisher exact. Holm over all 22 tests, and over the 19 left after the 3 dropped for low agreement. Agreement (percent) and Cohen's kappa: second pass on 18 projects (same model, same prompt), at the level of each test; n = projects where at least one pass gave a value.

| Variable | Winners | Controls | p | Holm (22) | Holm (19) | Agreement | Kappa | n |
|---|---|---|---|---|---|---|---|---|
| Any traction | 34/43 | 12/47 | <0.001 | <0.001 | <0.001 | 0.94 | 0.89 | 18 |
| Traction with a number | 23/43 | 9/47 | <0.001 | 0.019 | 0.016 | 1.00 | 1.00 | 18 |
| A team credential | 37/43 | 25/47 | 0.001 | 0.024 | 0.021 | 1.00 | 1.00 | 18 |
| Face on camera | 35/41 | 24/43 | 0.004 | 0.077 | 0.065 | 1.00 | 1.00 | 17 |
| Revenue as the traction | 7/43 | 1/47 | 0.025 | 0.46 | 0.38 | 1.00 | 1.00 | 18 |
| Competition mentioned | 31/43 | 26/47 | 0.13 | 1.00 | 1.00 | 0.94 | 0.87 | 18 |
| Onchain proof on screen | 4/33 | 10/35 | 0.13 | 1.00 | 1.00 | 0.86 | 1.00 | 14 |
| Explicit why Solana | 21/43 | 16/47 | 0.20 | 1.00 | 1.00 | 0.89 | 0.73 | 18 |
| Opens with the product | 26/43 | 23/47 | 0.30 | 1.00 | dropped | 0.61 | 0.32 | 18 |
| Revenue model stated | 25/43 | 22/47 | 0.30 | 1.00 | 1.00 | 0.94 | 0.89 | 18 |
| B2B (incl. B2B2C) | 15/43 | 12/47 | 0.37 | 1.00 | 1.00 | 1.00 | 1.00 | 18 |
| Problem stated with a number | 19/43 | 16/47 | 0.39 | 1.00 | 1.00 | 1.00 | 1.00 | 18 |
| Opens by introducing the team | 9/43 | 13/47 | 0.48 | 1.00 | dropped | 0.61 | 0.28 | 18 |
| Product running on screen | 20/37 | 23/36 | 0.48 | 1.00 | 1.00 | 0.79 | 0.83 | 14 |
| An ask or next steps | 31/43 | 30/47 | 0.50 | 1.00 | 1.00 | 1.00 | 1.00 | 18 |
| A specific, named user | 21/42 | 19/45 | 0.52 | 1.00 | 1.00 | 0.76 | 0.39 | 17 |
| Existed before the hackathon | 15/16 | 6/7 | 0.53 | 1.00 | 1.00 | 1.00 | 1.00 | 4 |
| Market size with a number | 18/43 | 17/47 | 0.67 | 1.00 | 1.00 | 1.00 | 1.00 | 18 |
| Opens with the problem or a story | 4/43 | 3/47 | 0.71 | 1.00 | 1.00 | 1.00 | 1.00 | 18 |
| Real-world domain (incl. both) | 21/43 | 25/47 | 0.83 | 1.00 | 1.00 | 0.94 | 0.89 | 18 |
| Full-time commitment stated | 4/4 | 3/3 | 1.00 | 1.00 | dropped | 0.50 | n/a | 2 |
| Token mentioned | 8/42 | 9/46 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 18 |

Holm over all 36 tests (the 22 above plus the 14 language metrics): below 0.05 for Any traction, A team credential, Traction with a number.

## Traction with a number, among projects that cite traction

Winners 23/34, controls 9/12, Fisher p 0.73.

## By period (2024: Renaissance, Radar; 2025-26: Breakout, Cypherpunk, Frontier)

| Variable | Winners 2024 | Controls 2024 | p | Winners 2025-26 | Controls 2025-26 | p |
|---|---|---|---|---|---|---|
| Any traction | 8/11 | 3/17 | 0.006 | 26/32 | 9/30 | <0.001 |
| A team credential | 9/11 | 9/17 | 0.23 | 28/32 | 16/30 | 0.005 |
| Face on camera | 6/10 | 12/17 | 0.68 | 29/31 | 12/26 | <0.001 |

## Traction by type (projects per type)

- winners: users 19, partnerships 15, none 9, volume 9, grants_prizes 7, revenue 7, lois_pilots 5, waitlist 1
- controls: none 35, partnerships 7, lois_pilots 3, users 3, waitlist 3, grants_prizes 3, volume 2, revenue 1

Winners citing no traction (9): archer-exchange, banger, kormos, reflect-protocol, rekt, tapedrive, typex-keyboard, urani, welikesports.

## Language metrics (rhetoric.py), winners vs controls

Medians; two-sided Mann-Whitney. Numbers are counted one per number.

| Metric | Winners | Controls | p |
|---|---|---|---|
| words | 490.00 | 413.00 | 0.076 |
| words_per_sentence | 17.20 | 14.20 | 0.41 |
| share_short_sentences | 0.40 | 0.43 | 0.53 |
| share_long_sentences | 0.21 | 0.12 | 0.24 |
| share_sentences_with_number | 0.17 | 0.12 | 0.13 |
| numbers_per_min | 1.93 | 1.79 | 0.050 |
| analogies | 0.00 | 0.00 | 0.12 |
| contrast_per_min | 0.50 | 0.34 | 0.12 |
| you_per_100w | 1.10 | 1.53 | 0.40 |
| i_story_per_100w | 0.14 | 0.23 | 0.50 |
| questions | 0.00 | 0.00 | 0.33 |
| product_verbs_per_min | 0.00 | 0.00 | 0.10 |
| flesch_reading_ease | 59.00 | 64.60 | 0.41 |
| syllables_per_word | 1.54 | 1.51 | 0.72 |

Not tested, medians only:

- duration_s: winners 177.0, controls 176.0
- wpm: winners 169.8, controls 153.4
- jargon_per_min: winners 1.6, controls 2.0
- seconds to the problem: winners 15.5, controls 15.0

## What the sample could detect

For each variable with p >= 0.1: the winner rate a two-sided Fisher test at 0.05 would detect with 80% power, holding the control rate and both sample sizes as observed.

| Variable | Winners | Controls (rate) | Detectable winner rate: below / above |
|---|---|---|---|
| Opens with the problem or a story | 4/43 | 3/47 (6%) | none / 29% |
| Opens with the product | 26/43 | 23/47 (49%) | 20% / 78% |
| Opens by introducing the team | 9/43 | 13/47 (28%) | 6% / 58% |
| Problem stated with a number | 19/43 | 16/47 (34%) | 9% / 65% |
| A specific, named user | 21/42 | 19/45 (42%) | 15% / 73% |
| Product running on screen | 20/37 | 23/36 (64%) | 30% / 91% |
| Onchain proof on screen | 4/33 | 10/35 (29%) | 3% / 64% |
| Explicit why Solana | 21/43 | 16/47 (34%) | 9% / 65% |
| Existed before the hackathon | 15/16 | 6/7 (86%) | 22% / none |
| Revenue model stated | 25/43 | 22/47 (47%) | 18% / 76% |
| Market size with a number | 18/43 | 17/47 (36%) | 11% / 67% |
| Competition mentioned | 31/43 | 26/47 (55%) | 26% / 84% |
| Full-time commitment stated | 4/4 | 3/3 (100%) | 5% / none |
| An ask or next steps | 31/43 | 30/47 (64%) | 33% / 89% |
| Token mentioned | 8/42 | 9/46 (20%) | 1% / 48% |
| B2B (incl. B2B2C) | 15/43 | 12/47 (26%) | 4% / 56% |
| Real-world domain (incl. both) | 21/43 | 25/47 (53%) | 24% / 82% |

## Demo Day

65 Demo Day pitches, cohorts C1-C5: C1 11, C2 12, C3 10, C4 11, C5 21.
Outcomes: unknown 50, raised 7, acquired 3, closed 3, token 2.

### Raised a new round after Demo Day vs the rest (cohorts C1-C4: 6 vs 38)

Raised by cohort: C1 4/11, C2 2/12, C3 0/10, C4 0/11.

| Variable | Raised | Rest | p | Holm |
|---|---|---|---|---|
| Token mentioned | 5/6 | 7/38 | 0.004 | 0.11 |
| Opens by introducing the team (dropped) | 2/6 | 1/38 | 0.045 | 1.00 |
| t_problem_s (median) | 26.00 | 8.00 | 0.065 | 1.00 |
| t_what_it_does_s (median) | 12.50 | 4.00 | 0.11 | 1.00 |
| Onchain proof on screen | 1/3 | 0/21 | 0.12 | 1.00 |
| jargon_per_min (median) | 2.54 | 0.97 | 0.14 | 1.00 |
| A specific, named user | 0/6 | 12/38 | 0.17 | 1.00 |
| Opens with the product (dropped) | 1/6 | 18/38 | 0.21 | 1.00 |
| first_only_claims (median) | 0.00 | 0.00 | 0.38 | 1.00 |
| Market size with a number | 4/6 | 16/38 | 0.39 | 1.00 |
| Product running on screen | 1/3 | 15/26 | 0.57 | 1.00 |
| Face on camera | 5/5 | 28/34 | 0.57 | 1.00 |
| Explicit why Solana | 3/6 | 14/38 | 0.66 | 1.00 |
| Real-world domain (incl. both) | 2/6 | 19/38 | 0.67 | 1.00 |
| t_product_on_screen_s (median) | 37.50 | 46.00 | 0.67 | 1.00 |
| Traction with a number | 3/6 | 23/38 | 0.68 | 1.00 |
| numbers_per_min (median) | 2.89 | 1.65 | 0.68 | 1.00 |
| duration_s (median) | 139.00 | 134.50 | 0.69 | 1.00 |
| buzz_per_min (median) | 0.00 | 0.00 | 0.89 | 1.00 |
| wpm (median) | 158.55 | 165.30 | 0.99 | 1.00 |
| Opens with the problem or a story | 1/6 | 8/38 | 1.00 | 1.00 |
| Problem stated with a number | 3/6 | 16/37 | 1.00 | 1.00 |
| Existed before the hackathon | 2/2 | 6/7 | 1.00 | 1.00 |
| Revenue model stated | 2/6 | 14/38 | 1.00 | 1.00 |
| Competition mentioned | 4/6 | 27/38 | 1.00 | 1.00 |
| An ask or next steps | 6/6 | 38/38 | 1.00 | 1.00 |
| B2B (incl. B2B2C) | 2/6 | 12/38 | 1.00 | 1.00 |
| Any traction | 4/6 | 25/38 | 1.00 | 1.00 |
| Revenue as the traction | 0/6 | 4/38 | 1.00 | 1.00 |
| A team credential | 5/6 | 32/38 | 1.00 | 1.00 |
| Full-time commitment stated (dropped) | 0/0 | 2/2 | n/a | n/a |

Holm over the 30 tests in this table.

### Same company, hackathon pitch vs Demo Day pitch (43 pairs)

| Variable | n | Hackathon | Demo Day | Gained | Lost | McNemar p |
|---|---|---|---|---|---|---|
| Opens with the problem or a story | 43 | 4 | 5 | 5 | 4 | 1.00 |
| Opens with the product (dropped) | 43 | 26 | 22 | 6 | 10 | 0.45 |
| Opens by introducing the team (dropped) | 43 | 9 | 2 | 1 | 8 | 0.039 |
| Problem stated with a number | 43 | 19 | 25 | 10 | 4 | 0.18 |
| A specific, named user | 42 | 21 | 13 | 2 | 10 | 0.039 |
| Product running on screen | 27 | 17 | 16 | 4 | 5 | 1.00 |
| Onchain proof on screen | 21 | 4 | 1 | 0 | 3 | 0.25 |
| Explicit why Solana | 43 | 21 | 15 | 5 | 11 | 0.21 |
| Existed before the hackathon | 4 | 4 | 4 | 0 | 0 | n/a |
| Revenue model stated | 43 | 25 | 19 | 5 | 11 | 0.21 |
| Market size with a number | 43 | 18 | 21 | 12 | 9 | 0.66 |
| Competition mentioned | 43 | 31 | 30 | 8 | 9 | 1.00 |
| Full-time commitment stated (dropped) | 1 | 1 | 1 | 0 | 0 | n/a |
| An ask or next steps | 43 | 31 | 39 | 11 | 3 | 0.057 |
| Token mentioned | 41 | 7 | 8 | 4 | 3 | 1.00 |
| Face on camera | 37 | 32 | 34 | 3 | 1 | 0.62 |
| B2B (incl. B2B2C) | 43 | 15 | 17 | 4 | 2 | 0.69 |
| Real-world domain (incl. both) | 43 | 21 | 26 | 7 | 2 | 0.18 |
| Any traction | 43 | 34 | 34 | 6 | 6 | 1.00 |
| Revenue as the traction | 43 | 7 | 5 | 2 | 4 | 0.69 |
| A team credential | 43 | 37 | 38 | 5 | 4 | 1.00 |
| Traction with a number | 43 | 23 | 30 | 11 | 4 | 0.12 |

| Metric | Hackathon median | Demo Day median | Lower at Demo Day |
|---|---|---|---|
| duration_s | 177.00 | 133.00 | 33/43 |
| wpm | 169.80 | 167.10 | 21/43 |
| numbers_per_min | 1.93 | 1.95 | 20/43 |
| jargon_per_min | 1.64 | 0.99 | 24/43 |

An ask or next steps, all Demo Day pitches vs the paired hackathon pitches: 58/65 vs 31/43 (Fisher p 0.037).

Demo Day second pass: 13 pitches; tests with agreement below 0.6: none.

## Category share of submissions vs wins (colosseum-copilot primary category)

Expected wins = the category's share of each hackathon's submissions times that hackathon's winners. P = exact probability, if winners were drawn at random from submissions within each hackathon, of a count at least as far from expected in the observed direction.

| Category | Hackathons | Submissions | Wins | Expected | P |
|---|---|---|---|---|---|
| agent-control-plane | frontier | 144 | 0 | 1.4 | 0.23 |
| token-launch | renaissance, radar, breakout, cypherpunk, frontier | 244 | 3 | 5.7 | 0.17 |
| verifiable-records | renaissance, radar, breakout, cypherpunk, frontier | 175 | 0 | 3.7 | 0.023 |
| depin | renaissance, radar, breakout | 120 | 17 | 3.7 | <0.001 |
| depin | cypherpunk, frontier | 72 | 0 | 1.1 | 0.33 |
| games | renaissance | 114 | 4 | 3.6 | 0.49 |
| games | cypherpunk | 88 | 0 | 1.8 | 0.15 |

All five hackathons: 8286 submissions, 180 winners.
