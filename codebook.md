# Codebook

Codebook v1 was fixed on 2026-09-30, before any transcript was read. The Demo Day addendum was fixed on 2026-10-05, before any Demo Day pitch was coded. This is an English translation of both; the field names and allowed values are the ones the coder used.

## Coder instructions

The coder codes one pitch video at a time from `transcript.txt` (lines `[mm:ss] speech`) and the frames in `frames/` (`index.json` gives each image's timestamp; up to 12 JPGs). It must open every frame listed. It does not know whether the project won and must not try to find out. It must not use outside knowledge about the project, open any other file or use the web.

Evidence rule: every field that is not a measured number carries `evidence` (a short literal quote from the transcript, or "frame f_00X.jpg: <what it shows>") and `t` (mm:ss). No evidence → the value is `null`, never a guess. `null` = the material doesn't say. `false` = the material shows it isn't there.

If a transcript is empty or clearly not a pitch or product demo, the coder writes `"material_ok": false` and leaves the other fields `null`.

The official criterion each variable maps to is in brackets: R = the judging section (§8) of the Crypto World's Fair rules (functionality, impact, novelty, UX, open source, business plan); P = Colosseum's hackathon page (founder-market fit, insight, product and execution, market size, founder communication, viability, traction).

## Output: one JSON per project, exactly these keys

```json
{
  "pid": "P000",
  "material_ok": true,
  "sections": [{"label": "hook|team|problem|solution|demo|how_it_works|why_solana|traction|market|business_model|competition|roadmap|ask|other", "start": "mm:ss"}],
  "hook_type": {"value": "problem_story|stat_number|product_first|team_intro|vision_statement|question|other", "evidence": "", "t": ""},
  "t_problem": {"value": "mm:ss|null", "evidence": ""},
  "t_product_on_screen": {"value": "mm:ss|null", "evidence": "frame ..."},
  "format": {"value": "slides|product_screen|mixed|talking_head", "evidence": ""},
  "face_on_camera": {"value": true, "evidence": "frame ..."},
  "speakers_n": {"value": 1, "evidence": ""},
  "problem_quantified": {"value": true, "evidence": "", "t": ""},
  "named_user": {"value": "specific|generic|null", "evidence": "", "t": ""},
  "live_product_shown": {"value": "working_product|mockup_or_figma|none", "evidence": "", "t": ""},
  "onchain_proof_shown": {"value": true, "evidence": "", "t": ""},
  "why_solana": {"value": "cost|speed|stablecoins_liquidity|composability_ecosystem|users_already_there|other|absent", "evidence": "", "t": ""},
  "traction": {"value": ["none|waitlist|users|revenue|volume|lois_pilots|partnerships|grants_prizes"], "numbers": "quote with the numbers", "t": ""},
  "existed_before_hackathon": {"value": true, "evidence": "", "t": ""},
  "business_model": {"value": "fees|subscription|saas_b2b|spread_yield|token|ads|none_stated", "evidence": "", "t": ""},
  "market_size": {"value": "tam_number|comparable_company|qualitative|absent", "evidence": "", "t": ""},
  "competition": {"value": true, "evidence": "", "t": ""},
  "team_credentials": {"value": ["domain_expertise|prior_startup_or_exit|big_tech_or_finance|technical_depth|none_stated"], "evidence": "", "t": ""},
  "full_time_commitment": {"value": true, "evidence": "", "t": ""},
  "ask_or_next_steps": {"value": true, "evidence": "", "t": ""},
  "token": {"value": "absent|utility|governance|incentive_points|speculative|launched", "evidence": "", "t": ""},
  "audience": {"value": "b2b|b2c|devs|b2b2c", "evidence": ""},
  "domain": {"value": "real_world|crypto_native|both", "evidence": ""},
  "one_line_claim": {"value": "the sentence that best sums up what they say they do, literal", "t": ""},
  "strongest_moment": {"value": "the most convincing passage, literal, and why in one sentence", "t": ""},
  "weakest_moment": {"value": "the weakest passage, literal, and why in one sentence", "t": ""}
}
```

Mapping: hook_type, sections, speakers, face [P founder communication] · problem_quantified, named_user, competition [P insight] · t_product_on_screen, live_product_shown, onchain_proof_shown [R functionality, P product and execution] · why_solana [R UX] · traction, existed_before_hackathon [P traction, viability] · business_model [R business plan, P viability] · market_size [R impact, P market size] · team_credentials, full_time_commitment [P founder-market fit] · token [hype check].

Computed in code, not by the coder: duration, words per minute, buzzword and crypto-jargon density per minute (fixed lists in `rhetoric.py`), "first/only" claims.

## Demo Day addendum (2026-10-05)

Codebook v1 applies unchanged. One key is added, for "seconds until saying what the company does":

```json
"t_what_it_does": {"value": "mm:ss|null", "evidence": "the first literal sentence that says what the product or company does"}
```

Definition: the first moment the speaker says, in one sentence, what the product or company does or is ("we're building X for Y", "X lets you…", "X is a … that …"). The name alone ("I'm the founder of P201") doesn't count. A problem, statistic, story or vision without saying what the product does doesn't count. Never said → `null`.

The company name was replaced by its ID (`P2xx`) in the transcript and blacked out in the frames where OCR found it. The coder treats `P2xx` as the name.

## What is published

`data/projects.csv`, `data/demoday.csv` and `data/second_pass.csv` keep the coded values of every key above except `pid`, `material_ok`, `sections`, `one_line_claim`, `strongest_moment`, `weakest_moment` and every `evidence`, `numbers` and `t` field, which are transcript text. Times are converted to seconds (`t_problem_s`, `t_product_on_screen_s`, `t_what_it_does_s`). List values are joined with `;`. An empty cell is `null`.

One column is derived, not coded: `traction_number_stated` is true when the coder's `traction.numbers` quote contains a digit and `traction.value` has a type other than `none`. It is a regular expression over the coder's free text, not a judgement the coder was asked to make.

## The 22 tests

Each test turns one field into yes/no; projects where the field is `null` are left out of that test's denominator.

| Test | Field | Yes when |
|---|---|---|
| Opens with the problem or a story | hook_type | problem_story |
| Opens with the product | hook_type | product_first |
| Opens by introducing the team | hook_type | team_intro |
| Problem stated with a number | problem_quantified | true |
| A specific, named user | named_user | specific |
| Product running on screen | live_product_shown | working_product |
| Onchain proof on screen | onchain_proof_shown | true |
| Explicit why Solana | why_solana | anything but absent |
| Existed before the hackathon | existed_before_hackathon | true |
| Revenue model stated | business_model | anything but none_stated |
| Market size with a number | market_size | tam_number |
| Competition mentioned | competition | true |
| Full-time commitment stated | full_time_commitment | true |
| An ask or next steps | ask_or_next_steps | true |
| Token mentioned | token | anything but absent |
| Face on camera | face_on_camera | true |
| B2B (incl. B2B2C) | audience | b2b or b2b2c |
| Real-world domain (incl. both) | domain | real_world or both |
| Any traction | traction | any type but none |
| Revenue as the traction | traction | includes revenue |
| A team credential | team_credentials | any type but none_stated |
| Traction with a number | traction_number_stated | true |
