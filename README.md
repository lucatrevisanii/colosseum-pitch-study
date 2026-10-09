# Colosseum pitch study

What did the hackathon pitch videos of Colosseum accelerator companies say more often than matched projects from the same hackathon that won nothing? And what changed when the same companies pitched at Demo Day?

This repository holds the coded values per project, the code that computes every count and test, and the results. It holds no video, no transcript and no quote: the videos belong to their teams and are not included.

Study run 2026-09-30 to 2026-10-06. Results: [results.md](results.md), written by `analyze.py`.

## Design

- **Winners.** The 61 companies Colosseum took into its accelerator, cohorts 1 to 5, from five hackathons: Renaissance (2024), Radar (2024), Breakout (2025), Cypherpunk (2025) and Frontier (2026). 43 had a hackathon pitch video that could be downloaded and coded; for the other 18 the video was private, removed, access-blocked, or the link pointed to a deck instead of a video.
- **Controls.** For each accelerated company, one project drawn at random from the same hackathon and the same primary category (colosseum-copilot's label), with no prize, no honourable mention, no accelerator place and a pitch video link. The draw is seeded by the company's slug, so it can be repeated. 60 were drawn (one company had no eligible project) and 47 were coded; the other 13 (22%) were lost to the same video problems or, in one case, a video the coder judged not to be a pitch. `data/pairs.csv` lists every pair and what was lost.
- **Material.** Each video downloaded at up to 480p, transcribed with whisper.cpp (model large-v3-turbo), plus up to 12 frames picked by scene change (ffmpeg, threshold 0.3). Anything visual (product on screen, onchain proof, face on camera) was judged from those stills, not from the video.
- **Demo Day.** 65 Demo Day pitches from cohorts 1 to 5 (11, 12, 10, 11, 21), cut from the public Demo Day recordings (YouTube for cohorts 1 to 4, X for cohort 5), coded with the same codebook plus one key. 43 of them pair with a coded hackathon pitch of the same company. Outcome after Demo Day (new round, acquired, closed, token, unknown) was looked up in public sources as of 2026-10-06: Colosseum's blog and portfolio, company sites and accounts, DefiLlama and CoinGecko, without a general web search. 50 of 65 are unknown, which means "not found", not "didn't raise". A round led only by Colosseum doesn't count, a round inside the Demo Day window doesn't count, and a token sale counts as a token, not a round.
- **Categories.** Submission and winner counts per primary category come from colosseum-copilot's labels (version 2026-09-25-v2) for all 8,286 submissions and 180 winners of the five hackathons.

## Who coded, and how

- **A language model coded every video** (Claude Opus 5.5, Anthropic, model id `claude-opus-5-5`, run in September and October 2026), from the transcript and the frames, with the closed codebook in [codebook.md](codebook.md) (fixed before any transcript was read) and the instructions at its top. No person coded the videos.
- **The second pass is the same model with the same prompt**, run again on a random sample without access to the first pass: 18 of the 90 projects here and 13 of the 65 Demo Day pitches. Agreement between the two passes measures how stable the model is, not whether a person would code the same way. `results.md` reports percent agreement and Cohen's kappa per test.
- **Dropped variables.** Before the comparison was read, tests with agreement below 0.6 were dropped: opening with the product (0.57), opening by introducing the team (0.57) and full-time commitment (0.5). That second pass had 21 projects; 3 of them were coded in the same batch for a separate question and are not part of this study, so the 18 published here give 0.61 for the two opening tests, with kappa 0.32 and 0.28. Low either way.
- **Blinding covers the group only.** Coders got a random ID, the transcript and the frames, never the group or the key, in shuffled batches that mixed winners and controls. But in the hackathon videos the project name stays in the transcript and on the frames, which were not redacted. In the Demo Day videos the name was replaced by the ID in the transcript and blacked out by OCR in 184 of 335 frames; one renamed company still leaked in the text, and stylised logos remain. The instruction not to use outside knowledge is an instruction, not a control: a model can recognise a well-known project.
- **"Traction with a number" is derived**, not coded: a regular expression for any digit in the coder's free-text quote of the traction numbers. That quote is transcript text and is not published; the derived yes/no is.

## Tests

- Winners vs controls: two-sided Fisher exact per variable, 22 tests. The original analysis ran them uncorrected; the Holm correction in `results.md` was added afterwards, at review, and was not pre-registered. Language metrics: two-sided Mann-Whitney, 14 tests.
- The controls were drawn one per winner, but the losses broke the pairs, so the comparison is between the two groups (Fisher), not paired.
- Demo Day: Fisher between companies that raised afterwards and the rest (cohorts 1 to 4, 6 vs 38), and exact McNemar on the 43 companies with both pitches.
- Power: for each variable that didn't separate, `results.md` gives the winner rate the sample could have detected with 80% power. With these sizes, only gaps of roughly 25 to 35 percentage points.

## What it found (details and every number in results.md)

- Two things separate after correction: citing any traction (34/43 winners vs 12/47 controls) and a team credential (37/43 vs 25/47). Traction with a number also passes (23/43 vs 9/47), but it is a subset of traction: among projects that cite traction, 23/34 vs 9/12 say a number, so the number is not a separate signal.
- Face on camera (35/41 vs 24/43) doesn't survive correction and appears only in 2025-26. The credential gap doesn't hold in 2024 alone (9/11 vs 9/17).
- No difference was detected for the product on screen, onchain proof on screen, why Solana, market size, token, problem with a number, named user, revenue model, competition, the ask, or any language metric, including numbers per minute (1.9 vs 1.8 a minute, p 0.05 uncorrected, one of 14 metrics).
- Category: DePIN won 17 of the 119 prizes in Renaissance, Radar and Breakout, where its share of submissions predicts 3.7; verifiable records won 0 of 180 across all five, where 3.7 were expected. The other category gaps checked fit chance.

## Limits

- Association, not cause. Traction and credentials may only mark stronger companies.
- Pitch video only: the demo video, the written submission and the interview round were not coded.
- Top vs bottom: accelerated winners against projects that won nothing. Track winners and honourable mentions who weren't accelerated are in neither group.
- A model coded everything, with partial blinding and stills for anything visual.
- 22 coded tests plus 14 language metrics; anything that doesn't survive correction may be noise.
- 18 of 61 winners and 13 of 60 controls lost to missing videos. The surviving controls may skew stronger.
- Demo Day: 6 companies raised against 38; cohort matters more than pitch (4 of 11 raised from cohort 1, none from cohorts 3 and 4).

## Reproduce

```
uv run analyze.py      # or: python3 analyze.py — standard library only
```

It reads `data/*.csv` and rewrites `results.md`.

`data/language.csv` comes from `rhetoric.py`, which needs the transcripts. To rebuild it: open each project's page on `https://colosseum.com/arena/projects/<slug>`, download its pitch video, transcribe it with whisper.cpp into `transcripts/hackathon/<slug>.txt` (Demo Day: `transcripts/demoday/<company_slug>.txt`) as `[mm:ss] text` lines, then run `uv run rhetoric.py transcripts`. A different whisper version or a re-encoded video will shift the counts a little.

To re-code, give a model or a person the codebook and its instructions, one video at a time.

## Data

| File | Rows | What |
|---|---|---|
| `data/projects.csv` | 90 | Winners and controls: slug, group, hackathon, category, cohort (winners), the winner a control was drawn for, and the coded values |
| `data/pairs.csv` | 61 | Every accelerated company, its drawn control, and whether each video was coded |
| `data/second_pass.csv` | 31 | The second pass: 18 hackathon projects, 13 Demo Day pitches |
| `data/demoday.csv` | 65 | Demo Day pitches: company slug, cohort, hackathon project slug if any, outcome, whether it raised after Demo Day, the outcome's source link, coded values |
| `data/language.csv` | 155 | `rhetoric.py` metrics per transcript |
| `data/categories.csv` | 217 | Submissions and winners per hackathon and primary category |

Column meanings are in [codebook.md](codebook.md). Slugs are Colosseum's public project slugs.

## License

MIT ([LICENSE](LICENSE)), for the code and this study's coded tables. The pitch videos and their transcripts belong to their teams and are not included; project slugs and outcome links point to public pages.
