# ab4 READY (design d4: lint pre-pass + k=2 first reviews + cleaned VERIFY)

Root: `$SP/p16/ab4` (SP = /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad). Python: `python3` (stdlib only; `uv run --no-project python` also works). No git, no repo clone, no network used. p12/ab1 and p13/* untouched.

## Files
| file | role |
|---|---|
| `harness.py` | build/prep/ingest/merge(k=2)/verify/tokens/analyze (copy of ab1 harness, modified) |
| `advance.py` | state machine (`--dry-run` supported); launch ledger `launch-ledger.jsonl` (stratum + model per launch) |
| `score_themes.py` | ids_from extended (item 4c); `cut_block` / `clean_body` / `finding_block` (item 4a) |
| `reqlint.py` | PN2 lint, byte-identical copy of p13/clones/pn2 `cli/review/lint.py` (stdlib only; test asserts identity) |
| `decision.json` | all decision constants (data, not code) incl. D6 limits, frozen-file hashes, lint check set |
| `frozen/` | `command.md` (product command == frozen audit command, sha e62e70b9...), `rules.md` (built by `make_rules.py`), `audit-rules.md` (p11/rules.md), sources `rules-ab1.md`, `rules-pn2.md` |
| `make_rules.py` | builds `frozen/rules.md` = ab1 rules + the two PN2 "Lint evidence" bullets (verbatim, PN2 positions) + "three" -> "two" first reviews |
| `tests/test_ab4.py`, `tests/fixtures/` | 21 tests; fixtures are real ab1 reports (18) + one real multi-row verify reply |
| `$SP/drive.sh` | unchanged dispatch (`cd $SP/$d && uv run --no-project python advance.py`) already works for `p16/ab4`; only extended the grep with `LOST` (ab1 printed `LOST ...` in upper case, the filter only had `lost`) |

## Design items
1. Lint: `prep` of R1a/R1b runs the PN2 lint (check set REF) on the candidate -> `ws/.dev/orca-command-refactor/review/lint-1.md`, also copied into `r1a/ws` and `r1b/ws` (the reviewers' own sandboxes). Brief wording as PN2: `Values: candidate=<spec>, lint=<review>/lint-1.md.` `prep R2` / `prep R3` re-run on the revised spec -> lint-2.md / lint-3.md, referenced as `lint=` in the re-review brief. Verified: lint-1 is byte-identical to PN2's l2-r1 lint-1. Each run is logged in `state.log.LINT1..3` (findings count, ids, by_check, sha).
2. k=2: R1a = ab1 FIRST-REVIEW brief (+ lint value). R1b = R1a + one sentence (test asserts R1b == R1a + exactly that sentence). Sentence sits at the end of the `Values:` line.
3. MERGE over `round1-a/b`, same dedup rule (same theme and cited-line Jaccard >= 0.5), header "over two independent first reviews".
4. a) Finding lists are cleaned at source: `finding_block()` cuts each finding at the first banner (`=== ... ===`, `### === ...`) or non-finding heading (Reviser brief, follow-up, architecture/adversarial analysis, guard table, verdict...) and `clean_body()` drops recommendation / option / (a)(b) / priority / origin / verification-status / "Reviser brief note" lines together with their indented children. Used by merge, `findings_text` (VF2/VF3) and the round1.md render. `check_findings_text()` is run on every list before a VF prompt is written; a violation raises and `advance` prints `MANUAL <run> VFn not prepared` instead of launching a contaminated verifier. b) `reconcile_confirmed()` (pure, tested on the real b1h-r3 verify-1 where M4.a rejects and M4.b holds). c) `ids_from` now parses `=== REVISER BRIEF ===`, `Blocking: / Blocking findings: B1, B2` inline lists, and review-3 lines "Open blocking findings ...: N2 (open) and N4 (new)", "Open blocking findings: N3.", "Blocking findings open: 1 (B2, ...)"; also stops a prose "Reviser brief (blocking finding ids only; ...): revise ..." line from being read as an id list. Checked on all 69 FAIL reports in p12/ab1 + p13/ab2: no id set changed except the 7 that previously needed setids (now equal to the manual ids).
5. Tokens: `scan_by_prompt` matches the transcript's first user text (whitespace-normalised) to a PROMPT-<STEP>.md (exact, or prompt contained in a wrapped message), or the short launch `Read <abs path>/PROMPT.md and follow it exactly` (path resolved: runs/<run>/PROMPT-<STEP>.md, any existing prompt file by text, or `<run>/<sandbox>/PROMPT.md` by sandbox dir name). Output tokens = max per message id, each id once (`transcript_info`). `advance` uses it for finish detection too; `harness.py tokens [RUN]` writes `output_tokens`.
6. Names: Sonnet d4-r1..r6, Haiku d4h-r1..r4, extension d4-r7..r9 (`build --extend`, once, only if metrics.json says n=6 INCONCLUSIVE). Every state, step log record and ledger line carries `stratum` (+ `model`); AUD/AUD2 are always Sonnet (`expected_model`, plus an assert in advance).
7. analyze: ab1's decide() and thresholds, constants in decision.json (A_BASE 100,424; one audit 69,044; B_BASE 169,468). Added: per-theme capture table for k=2 (R1a / R1b / union vs baseline k=1), per-run lint-findings column (lint-1/2/3) in the run table and design table.

## Where D2 / D3 / D4 / D6 are encoded
- D2: `decision.json` A_BASE / AUD_BASE / B_BASE; `harness.decide()` (R_LOOP = loop-only mean / A_BASE decides; R_B = loop + first audit / B_BASE reported only); message ids counted once in `transcript_info`. Test `test_loop_only_cost_decides_and_b_is_reported`.
- D3: `decision.json` N_HAIKU / `haiku{}`; `build()` stratum, `expected_model()`, `haiku_stratum()` / `final_outcome()` ("ADOPT (Haiku robustness pending)"), stratum tag on state, step records, ledger. Test `test_run_names_strata_and_aud_model`.
- D4: `decision.json` N_EXTEND / MIN_COMPLETED; `build(extend=True)` refuses unless metrics.json records n=6 + extension_eligible, and refuses a second extension; `analyze()` uses n=9 once d4-r7 exists. Test `test_extension_rule_d4`.
- D6: `decision.json` rules.DROP2_RLOOP_LIMIT = 2.69 with formula and original L=2.0 as comment; cost enters only in `decide()` (post hoc); no token check in advance.py (test greps for abort/kill and for R_LOOP in advance.py).

## Tests
`cd $SP/p16/ab4 && python3 tests/test_ab4.py` -> `21/21 passed` (pytest is not importable here; the functions are also pytest-collectable). Mutation check: disabling the banner cut makes 5 of the tests fail. Covered: ids_from (3 formats + all fixtures resolve), no banner/recommendation line in finding lists built from 18 real reports (and the ab1 slicing is shown to be contaminated on >= 5 of them), merge over two reports + dedup, confirmed-line authority (parse level and ingest level), lint equals PN2 / briefs / lint-2,3 / R1b sentence, rules wording, tokens (pasted, wrapped, short launch, max-per-id, wrong-model ignored), names/strata/AUD model, D4 extension, decision constants and loop-only cost, a full fake loop R1 -> AUD2 -> analyze on fixtures (no setids needed for the review-3 report).

## Dry run (clean state; nothing launched)
```
python3 harness.py build --all      # built d4-r1..r6, d4h-r1..r4 (10 sandboxes)
python3 advance.py --dry-run        # writes PROMPT-R1a/R1b + lint-1.md for all 10 runs; state.launched is {} everywhere
```
First LAUNCH lines the coordinator will see (`./drive.sh p16/ab4`, MAX_CONCURRENT 6; Haiku runs start as slots free):
```
LAUNCH p16/ab4/runs/d4-r1/PROMPT-R1a.md model=sonnet
LAUNCH p16/ab4/runs/d4-r1/PROMPT-R1b.md model=sonnet
LAUNCH p16/ab4/runs/d4-r2/PROMPT-R1a.md model=sonnet
LAUNCH p16/ab4/runs/d4-r2/PROMPT-R1b.md model=sonnet
LAUNCH p16/ab4/runs/d4-r3/PROMPT-R1a.md model=sonnet
LAUNCH p16/ab4/runs/d4-r3/PROMPT-R1b.md model=sonnet
```
The sandboxes are built and the dry run is done; the coordinator's first real `./drive.sh p16/ab4` marks these six launched. (Do not run drive.sh before intending to launch: it is live, not a dry run.)

## Open questions
1. Rules file: ab1's rules file has no lint text, so ab4's `frozen/rules.md` adds PN2's two "Lint evidence" bullets and changes "three" to "two" first reviews in 5 coordinator-side places (diff vs ab1: `diff frozen/rules-ab1.md frozen/rules.md`). Brief says keep everything else identical; this is the minimum that makes the lint value and k=2 coherent. Revert by dropping the `subs` list in make_rules.py if you want ab1 wording.
2. Lint check set: REF only, as PN2's live set (decision.json lint.checks). Change there to widen.
3. Merge now cuts findings at banners before computing cited lines, so its dedup may differ slightly from ab1's. Audit/reviewer scoring (`run_record`, `baseline_values`) keeps ab1 slicing so comparisons with ab1/baseline are unchanged.
4. Baseline second audit (`p12/baseline-audit2`) and Haiku baseline (`p14/haiku-baseline/results.json`) are read from the same paths as ab1; if absent, analyze says PROVISIONAL / Haiku pending exactly as ab1 did.
5. Cannot import pytest here; tests run as plain asserts.
