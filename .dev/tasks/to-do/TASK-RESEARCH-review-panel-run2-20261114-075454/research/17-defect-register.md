# Research: Defect register (de-duplicated) for the unified Review Panel
**Investigation type:** Code Tracer
**Scope:** scope slices 01, 02, 03, 04, 09, 10, 11 in research/scope/; code at HEAD 50d4d2b9d (cli/review, reflect Tier 2 engines); E2 tip 6c0984326cbb8fb06c4a36065de58b171d3f8175 via git show / git ls-tree only
**Status:** Complete
**Date:** 2026-11-14
---

## Conventions

- Working IDs `DR-nnn` are assigned at first sight in slice order; the final de-duplicated register (with the crosswalk of the three numbering schemes) is appended at the end. Per-slice sections below are the evidence trail; the final register is authoritative.
- Slice line cites are `NN:line` (scope slice NN, line in that file). HEAD = 50d4d2b9d on `ironbelly/shadow-runs`. `RV` = `src/superclaude/cli/review`. E2 tip = 6c0984326cbb8fb06c4a36065de58b171d3f8175; `EV` = `.dev/eval-workspaces/tasklist-review-panel/20261111-a1` (E2 tip tree, via `git show` / `git ls-tree` only).
- Reproduction status: REPRODUCED (read-only `uv run python` at HEAD, script in `/tmp/review-panel-run2-2.17/repro1.py`, deleted before return; `git status` afterwards showed no new paths), TRACED (read the code), NOT-REPRODUCED, UNVERIFIED.
- Fix owner: CORE / MODULE-<name> / EVAL / HARNESS / DROP.

## Slice 01 (run-2 hand-off): evidence

Reproduction output at HEAD (single run, read-only; the repository `git status` before and after is the same four pre-existing untracked paths):

- D1: anchor of 201 chars -> `ok=False`, finding F1 dropped, F2 kept, error `anchor must have at most 200 characters` (`findings.py:104-106`, `parse_block` `:188-192`). Boundary 200/300/8 accepted; claim 301 rejected (`:118`). CRITICAL + `blocking=false` accepted (`:100-101` only rejects MINOR + blocking).
- D7: `refs_norm({'anchor':'Task T01.02 does x','claim':'T01.02 bad','refs':['T01.02','AC-0.4','1.2']})` -> `['1.2','AC-0.4']` (`findings.py:29` `_REF_TOKEN`).
- D2/D3: round 1 two reviewers find L1 (FAIL); revision applied; round 2 reviewer `a` clean + reviewer `b` with a broken block -> `verdict=PASS decision=PASS block_ok={'a': True, 'b': False}` with one warning, L1 `resolved`. The round entry keys are `block_ok, model, report, report_sha256, reviewer_id` (no dropped-count or dropped-ids field).
- D9: after a two-reviewer round 1, a round-2 re-review by single reviewer `b` reporting the same defect MINOR non-blocking -> `verdict=PASS`, `row.blocking=False`.
- D11: `apply_revision` with the same `--old` twice: span `[2,3]` -> `[3,4]` -> `[4,5]`; the second call is accepted (no error).
- D4: three findings at lines 3, 6, 9 (each pair of neighbours within 3 lines, ends 6 apart) -> 1 row with 3 members (chain).
- D6: an anchor absent from the document -> `anchor_status=missing`, `span=None`; the blocking row is kept (`verdict=FAIL`).
- P1: `pnl.resolve` over `run1..run40`, env gateway, kind first: `@live7` 30/40 and `@default` 18/40 resolutions hold a duplicate model. Slice 01 states 26/40 for `@live7` (run ids not stated) -> NOT reproduced with this id set.
- P2: all `launch` values `None` (gateway). P3: `muse-ember` absent from the tier data. P4: `glm-5.3`, `Qwen3.8-max` present in the tier lists. P5: `select_env(None, {'T2bModel01': 'x'})` -> `anthropic-only`. P6: re-review resolves to `['t1b-1']` only. P7: `round_robin` with no `--sequence` picked `['glm-5.3','Qwen3.8-max']`, with `date.today().toordinal()` = 739934 at run time.

### Register rows from slice 01 (provisional DR ids)

| DR | Original id | Slice:line | Statement | file:line (HEAD / E2 tip) | Repro status | Pinned by test | Fix owner |
|---|---|---|---|---|---|---|---|
| DR-001 | D1 (run-2) | 01:174-175 | A finding whose anchor/anchor2 > 200, claim > 300, refs > 8, id > 16, bad severity, or MINOR+blocking is dropped whole; the same limits exist in findings_v2 [CODE-VERIFIED] | `RV/findings.py:79-87,90-121,188-192`; `RV/findings_v2.py:80,111,114-120,126,128,132,136` | REPRODUCED (v1); v2 TRACED | Limits only partly pinned: `tests/review/test_review_findings.py:111-122` tests `short`, 201, 301, 9 refs; exact boundaries 200/300/8 untested | CORE (repair or truncate, count drops, one parser) |
| DR-002 | D2 | 01:176 | Partial-panel failure is invisible: merge refuses only when no reviewer has a valid block; the warning keeps the first error only; the ledger entry stores only `block_ok` [CODE-VERIFIED] | `RV/ledger.py:127-134,141-149,150-157,421-424`; `RV/merge_cmd.py:117-118` | REPRODUCED | YES as intended: `tests/review/test_review_ledger.py:376-385` `test_one_valid_block_is_enough_and_the_invalid_reviewer_is_reported` | CORE merge (surface dropped counts and ids) |
| DR-003 | D3 | 01:177 | Docstring says an invalid-block reviewer "is skipped for clearing"; the clearing loop never reads `block_ok`, so a broken reviewer does not stop a row clearing [CODE-VERIFIED] | docstring `RV/ledger.py:112`; loop `:254-258` | REPRODUCED (L1 -> resolved, verdict PASS) | YES: same test `test_review_ledger.py:376-385` asserts `status(led)["L1"] == "resolved"` with `t2-1` broken | CORE ledger (decide: docstring or loop is right) |
| DR-004 | D4 | 01:178 | Union-find over `same_defect` with 3-line tolerance chains distinct defects; the row keeps the first member's anchor/claim [CODE-VERIFIED] | `RV/findings.py:367-407`; `RV/ledger.py:182-199`; v2 `cluster.py` flags chains but still builds them | REPRODUCED (1 row, 3 members) | v2 only: `tests/review/test_review_cluster.py:108,124,471` pin chain flagging in cluster_v2; none for v1 | CORE cluster |
| DR-005 | D5 | 01:179 | A ref mismatch splits one defect; refs are scraped from free text [CODE-VERIFIED] | `RV/findings.py:321-337,373-374` | TRACED | none found | CORE cluster |
| DR-006 | D6 | 01:180 | Missing anchor kept with span None; `anchor_status`/`anchor_ambiguous` computed and never read [CODE-VERIFIED] | `RV/findings.py:349-358` | REPRODUCED | none found | CORE anchor |
| DR-007 | D7 | 01:181 | Task ids such as `T01.02` are not refs; same pattern in telemetry [CODE-VERIFIED] | `RV/findings.py:29`; `RV/telemetry.py:23` | REPRODUCED | none (grep `T01.02` in `tests/review` found nothing, 01:237) | MODULE-tasklist (ref syntax per target) |
| DR-008 | D8 | 01:182 | Any single blocking finding fails the round; `confidence` is computed and printed but never used [CODE-VERIFIED] | `RV/ledger.py:86-90,99-104,187,273-274` | TRACED | none found | CORE ledger (quorum/calibrator is an open design decision) |
| DR-009 | D9 | 01:183 | A refound row takes the current round's blocking call; a one-reviewer re-review can downgrade [CODE-VERIFIED] | `RV/ledger.py:210-218`; `apply_to: ["first"]` in packaged templates | REPRODUCED (PASS, `row.blocking=False`) | YES as intended: `test_review_ledger.py:518` `test_refound_as_nonblocking_stops_failing_the_review` | CORE loop (decide the rule) |
| DR-010 | D10 | 01:184 | Cluster matches only the first existing row (`break`) [CODE-VERIFIED] | `RV/ledger.py:165-171` | TRACED | none found | CORE ledger |
| DR-011 | D11 | 01:185 | `ledger revise` can run twice and remap spans twice; no new-text hash stored [CODE-VERIFIED] | `RV/ledger.py:301-347`; `RV/ledger_cmd.py:61-71` | REPRODUCED (spans [2,3] -> [3,4] -> [4,5]) | none found | CORE ledger |
| DR-012 | D12 | 01:186 | `merge` always exits 0; `ledger verdict` maps 0/10/11 [CODE-VERIFIED] | `RV/merge_cmd.py:117-118`; `RV/ledger_cmd.py:13,109` | TRACED | YES as intended: `tests/review/test_review_cli.py:229` (merge exit 0 with verdict FAIL/REVISE at `:232-233`), `:245` verdict exit 10 | CORE CLI (low) |
| DR-013 | D13 (run-2) | 01:187 | A `--report` id missing from `--resolution` gets model None; no cross-check [CODE-VERIFIED] | `RV/merge_cmd.py:94` | TRACED | none found | CORE CLI (low) |
| DR-014 | P1 | 01:193-194 | `distinct_across_slots` silently falls back to duplicates when exclusion empties the pool; `--strict-distinct` / `--hard-exclude-class` exist but are opt-in [CODE-VERIFIED] | `RV/panel.py:539-543`; `RV/panel_cmd.py:53-62` | REPRODUCED (30/40 `@live7`, 18/40 `@default`; slice figure 26/40 [UNVERIFIED]) | YES as intended: `tests/review/test_review_panel.py:204-214`; `tests/review/test_review_panel_exclusion.py:208` `test_soft_distinct_without_exclusion_still_repeats_a_model` | CORE panel (default behaviour decision) |
| DR-015 | P2 | 01:195 | Gateway environment has an empty `launch` map | `RV/data/review-tiers.default.json:29`; `RV/panel.py:679` | REPRODUCED (all `None`) | YES: `test_review_panel.py:303-308` `test_gateway_resolution_prints_launch_null` | CORE dispatch |
| DR-016 | P3 | 01:196 | `muse-ember-1.0` absent from tier data | `RV/data/review-tiers.default.json:5-10` | REPRODUCED | none | CORE panel data (owner-controlled) |
| DR-017 | P4 | 01:197 | Excluded Qwen/glm models remain in the tier lists | `RV/data/review-tiers.default.json:7-9,18-23` | REPRODUCED | none | CORE panel data |
| DR-018 | P5 | 01:198 | Environment is guessed from `$T3Model01`; the other slot variables are never read | `RV/panel.py:485-494` | REPRODUCED | YES as intended: `test_review_panel.py:331-339` `test_select_env_precedence` | CORE panel |
| DR-019 | P6 | 01:199 | Re-review resolves to the single fixed anchor (`apply_to: ["first"]`) | `RV/panel.py:600-605` | REPRODUCED (`['t1b-1']`) | YES: `test_review_panel.py:288-291` `test_re_review_resolves_only_the_anchor` | CORE loop (by design) |
| DR-020 | P7 | 01:200 | `round_robin` uses today's date when `--sequence` is absent | `RV/panel.py:623-628` | REPRODUCED | not pinned; `test_review_panel.py:311-328` and `test_review_panel_reflect_profile.py:152` test only the explicit-sequence path | CORE panel (low) |
| DR-021 | T1 | 01:201 | No automatic caller of `append_record`; the one caller is the manual `review telemetry append`; `model.observed` has no producer | `RV/telemetry.py:287,49`; `RV/telemetry_cmd.py:67` | TRACED | none | CORE telemetry |
| DR-022 | T2 | 01:202 | Telemetry strata hard-code sonnet/haiku | `RV/telemetry.py:112,267` | TRACED | partly: `tests/review/test_review_telemetry.py:324` `test_stratum_tag_is_optional_validated_stored_and_never_pooled` | CORE telemetry |
| DR-023 | B-1 | 01:208 | The reviewer brief never names the source document | `RV/rules/prompts/document_review_loop_prompts.md:15-21,32` | TRACED | none | CORE brief |
| DR-024 | B-2 | 01:209 | Parser limits (claim <= 300, refs <= 8, id <= 16, MINOR not blocking) are not stated in the prompt | prompt `:60` | TRACED | none (`test_review_rules_text.py` pins structure, not constants, 01:236) | CORE brief |
| DR-025 | B-3 | 01:210 | Blocking semantics conflict between spec-panel text, prompt and parser | `commands/spec-panel.md:259`; prompt `:31`; `RV/findings.py:100-101` | REPRODUCED (CRITICAL non-blocking accepted) | none | CORE (decide once) |
| DR-026 | B-4 | 01:211 | Report-ending conflict: last line `verdict:` vs last section `## Findings block` | `commands/spec-panel.md:260,263`; prompt `:58` | TRACED | none | MODULE-spec (low) |
| DR-027 | B-5 | 01:212 | No anchor guidance for `missing-requirement`, uniqueness, whitespace | prompt `:60`; `RV/findings.py:349-352` | TRACED | none | CORE brief |
| DR-028 | B-6 | 01:213 | Harness category `unpassable-ac` vs parser `unpassable-check` | `RV/findings.py:17`; E2 `EV/tools/run-reviewer.sh:17` | TRACED | none (only `test_review_card_convert.py:426` maps it) | DROP (fixed in the harness) |
| DR-029 | B-7 | 01:214 | Reviewers are not told one blocking row from any reviewer fails the round | prompt `:62` vs `RV/ledger.py:273-274` | TRACED | none | CORE brief |
| DR-030 | H1 | 01:352 | Cyclic fallback ladder spun and ran excluded models | E2 `EV/tools/run-reviewer.sh:66-83` (guard text and `EXCLUDE_MODELS` read at tip) | TRACED | n/a | HARNESS (fixed; OPS lesson) |
| DR-031 | H2 | 01:353 | On fallback, `expected_model` in meta is the fallback model (`MODEL="$NEXT"` before meta is written with `$MODEL`) | E2 `run-reviewer.sh:58,76` | TRACED | n/a | HARNESS / CORE (model identity) |
| DR-032 | H3 | 01:353 | Attempt counter resets per fallback model, so attempt files overwrite and cost undercounts | E2 `run-reviewer.sh:76,85-87` | TRACED | n/a | HARNESS |
| DR-033 | H4 | 01:353 | `BLOCK_OK` only greps the fence line (`^```findings-v1`), not the parse | E2 `run-reviewer.sh:57` | TRACED | n/a | HARNESS / CORE (use the real parser) |
| DR-034 | H5 | 01:354 | Stale attempt files inflate cost for 5 runs | E2 audit-A (cited run2:206) | UNVERIFIED (audit-A not opened) | n/a | EVAL (disclosed) |
| DR-035 | H6 | 01:355 | Stale merges (n2-terra, r2-sol, n5-sol, n5-terra) | E2 `EV/analysis/audits/audit-D/summary.md` (C5 and "Other EXCLUDE causes" read at tip) | TRACED | n/a | EVAL (disclosed, flagged EXCLUDE) |
| DR-036 | H7 | 01:356 | An API-error judge left a plausible score | E2 COMBO-REPORT (cited CR:146-147) | UNVERIFIED | n/a | EVAL (fixed by procedure) |
| DR-037 | H8 | 01:357 | Blocking counted by grep without space tolerance | E2 CR:105 | UNVERIFIED | n/a | DROP (fixed) |
| DR-038 | H9 | 01:357 | `attrib.py` credits by ledger membership | E2 CR:197 | UNVERIFIED | n/a | DROP (retracted) |
| DR-039 | H10 | 01:358 | Analysis scripts read or exec `/tmp` copies | E2 `final-table.py:23`, `three-way.py:4`, `b9-table.py:3`, `issue-table/issue-setup.py:3` (as in 01:73) | UNVERIFIED here (01 verified at tip) | n/a | EVAL (rewrite) |
| DR-040 | H11 | 01:359 | 12 concurrent workers caused gateway model-identity bleed | E2 `combos/SPEC.md:77-79` | UNVERIFIED | n/a | HARNESS (ops lesson, caps) |
| DR-041 | H12 | 01:359 | `claude` binary replaced mid-run three times (exit 127) | E2 `combos/SPEC.md:141,148,152` | UNVERIFIED | n/a | HARNESS (ops lesson) |

Slice 01 rows not in the D/P/T/B/H lists (defects in the run-1 hand-off, or errors inside the hand-offs):

| DR | Original id | Slice:line | Statement | file:line | Repro status | Pinned by test | Fix owner |
|---|---|---|---|---|---|---|---|
| DR-042 | run-1 D13 | 01:87 | `lint_cmd` and `estimate_cmd` are registered in the review group but no such modules exist; `ModuleNotFoundError` is swallowed [CODE-VERIFIED] | `RV/__init__.py:24-25` (names), `:30-35` (swallow); the Glob of `RV/*.py` lists no `lint_cmd.py` or `estimate_cmd.py` | REPRODUCED by Glob (negative evidence: 16 `.py` files, neither present) | none | CORE (remove the dead names or add the modules) |
| DR-043 | run-1 D16 | 01:89 | Round 4 is accepted after ESCALATE; `--cap` is ignored on an existing ledger; verify-only rounds are prompt-only | `RV/ledger.py:114-115` (only `n == len(rounds)+1`); `RV/merge_cmd.py:101-104`; `RV/ledger.py:93-96` | TRACED | none (01:513 names it a test gap) | CORE ledger |
| DR-044 | run-1 D14 (second half) | 01:88 | Review-ledger, diffgate, stoprule, fix-audit skills, the `finding-grader` agent and the spec-panel variant commands exist only as installed copies and as experiment builds, not in `src/superclaude` | slice 01:88 (Glob of `src/superclaude/skills` and `agents`) | UNVERIFIED (not re-derived here; E3 slice 12 is outside my list) | n/a | MODULE-spec (E3 variants) |
| DR-045 | doc error C1 | 01:67 | The hand-off (and the E2 comparison at cmp:22) attribute the `RV` changes to #518 (167184c6b); `git diff-tree --name-only -r 167184c6b` lists 0 paths under `src/superclaude/cli/review` (this run: `grep -c` = 0) | `git` (commit 167184c6b) | REPRODUCED read-only | n/a | DROP (documentation correction only) |
| DR-046 | doc error C15 | 01:81 | Both hand-offs and CR:292 label per-model drop counts (luna 30, ember 33, wonder 14, glm 7, haiku 7, grok 1 = 92) as "blocking findings lost"; audit-D shows they are all dropped findings and only 49 were blocking | E2 `EV/analysis/audits/audit-D/summary.md` ("By model", "49 dropped findings were BLOCKING"; read at tip) | REPRODUCED by reading (92 = 30+33+14+7+7+1) | n/a | EVAL (retraction) |
| DR-047 | doc error | 01:144,266 | "106 row folders in `combos/`": the tree holds 96 directories (`git ls-tree -d --name-only` = 96, run twice with two path forms); 106 is the scored-run count, not a folder count | E2 tip tree `EV/combos/` | REPRODUCED (96) | n/a | EVAL (retraction) |
| DR-048 | doc error | 01:145 | "4 verdict flips": audit-D lists 3 flips (g3-sonnet-luna-ember-r3/alias, g5-ember2-luna-r2/alias, n5-sonnet-ember/design) plus 5 total-loss merges | E2 `EV/analysis/audits/audit-D/summary.md` ("VERDICT FLIPS") | REPRODUCED by reading (3 listed) | n/a | EVAL (retraction) |
| DR-049 | doc error | 01:143 | "55 files + README" (run2:74) vs 55 files including the README: `git ls-tree -r --name-only` over `EV/tools/tmp-scripts/` = 55 | E2 tip tree | REPRODUCED (55 including README) | n/a | DROP (off by one) |
| DR-050 | doc error | 01:146 | Run-1 says "alias GT3 found once"; the legend maps the once-found defect to B6 = alias GT1 (CR:497-505 per slice) | E2 CR:497-505 | UNVERIFIED (not re-derived, taken from slice) | n/a | DROP (run-1 wrong, run-2 right) |
| DR-051 | doc error | 01:72,259 | Raw-file count disagreement: hand-offs say 3,041 untracked files; the committed note says 2,916 files (~1.48 GB) | E2 `EV/analysis/RAW-TRANSCRIPTS-NOT-COMMITTED.md:2` (read at tip: "2,916 files") | REPRODUCED for the 2,916 text; reconciliation with 3,041 UNVERIFIED | n/a | EVAL (disclosure) |

Notes for slice 01:
- The harness script path is `EV/tools/run-reviewer.sh` (under the `20261111-a1` folder), not `tools/run-reviewer.sh` at the eval root; slice 01 uses the short form.
- `.gitignore:13` at HEAD reads `lib/` (read directly); its relevance is for slices 10 or 11 and is checked when those are read.
- Run-1 numbering clashes with run-2: run-1 D13 (missing modules) is not run-2 D13 (missing `--report` id). They are separate rows (DR-042 vs DR-013).

**Key Takeaways (slice 01)**
- All 41 original ids (D1-D13, P1-P7, T1-T2, B-1..B-7, H1-H12) are in DR-001..DR-041 (count in 41, count out 41). Of these, 34 were reproduced or traced against code at HEAD or the E2 tip; H5, H7, H8, H9, H10, H11, H12 stay UNVERIFIED because they rest on E2 report lines I did not re-open. Ten more rows DR-042..DR-051 cover run-1-only defects and errors in the hand-offs.
- Eight of the run-2 "defects" are pinned by tests as intended behaviour: D2, D3 (`test_review_ledger.py:376-385`), D9 (`:518`), D12 (`test_review_cli.py:229,245`), P1 (`test_review_panel.py:204-214`, `test_review_panel_exclusion.py:208`), P2 (`test_review_panel.py:303-308`), P5 (`:331-339`), P6 (`:288-291`). A fix to any of them must change the test in the same change.
- D1 exists in BOTH parsers at HEAD (findings.py and findings_v2.py), so a unified parser must fix it once.

## Slice 02 (run1-vs-run2 comparison and per-run notes): evidence and numbering map

### Numbering schemes (open item c, scope slice 02 Q-A at 02:624 and the table at 02:131-144)

Four schemes name the same defects. I read the defect lists of the run-2 notes directly at the E2 tip (`git show 6c0984326...:.dev/eval-workspaces/tasklist-review-panel/handoff-notes/run2/code-merge.md` lines 129-151 and `code-panel.md` lines 165-185) and the run-2 hand-off table (slice 01). Unified scheme = `DR-nnn`; the crosswalk is in the final register section.

| Scheme | Ids | Where defined |
|---|---|---|
| A: run-2 hand-off ("report") | D1-D13, P1-P7, T1-T2, B-1..B-7, H1-H12 | run2:160-217 (read through slice 01) |
| B: run-2 merge notes (R2CM) | D1-D23 | `handoff-notes/run2/code-merge.md:129-151` [CODE-VERIFIED at the E2 tip by `git show`] |
| C: run-2 panel notes (R2CP) | defects 1-19 | `handoff-notes/run2/code-panel.md` section 6 (lines 167-185) |
| D: run-1 report and notes | D1-D16 (report), R1CM defects, R1CP 1-16 | slice 01 section 3.5 (crosswalk run-1 to run-2), slice 02 X8 |

Scheme B to scheme A (slice 02 table 2.4 re-checked against the R2CM text): B-D1 = A-D2; B-D2 = A-D3; B-D3 = A-D5; B-D4 = A-D6; B-D5 = A-D4; B-D6 = A-D10; B-D7 + B-D8 = A-D11; B-D9 = A-D1 + A-B-2; B-D11 = A-D12; B-D14 = A-D13; B-D12 and B-D13 = run-1 D16 (DR-043). B-D10, B-D15..B-D23 have no scheme-A id (new rows below). Scheme C to A: C1 = B-1; C2 = D7; C3 = P2; C4 = P1; C5 = D8; C6 = D9 + P6; C7 = B-3; C8 = T1; C11 = P7; C12 = D6 (sub-case, no new row); C13 = D13; C14 = B-4; C15 = T2; C9, C10, C16, C17, C18 are new rows; C19 = DR-044.

### Reproduction at HEAD (second read-only run, `/tmp/review-panel-run2-2.17/repro2.py`)

- D19 (B-D19): a fence `json findings-v1` gives `ok=False`, error `no fenced block with info string findings-v1 after the heading` (`findings.py:27` `_FENCE` takes one token).
- D20 (B-D20): a quoted example block plus the real block -> `ok=False`, `more than one findings-v1 block; the last one is used` (kept id `F1`, the real one); a missing heading says `heading '## Findings block' is missing` while `### findings BLOCK` is accepted (`findings.py:31,131,143-150`).
- D22 (B-D22): `claim=""` accepted (`findings.py:118`, `lo=None`). D23 (B-D23): `refs_norm` with lowercase `ac-1` -> `[]`, uppercase `AC-1` -> `['AC-1']` (`findings.py:29`, no `re.I`). Free-text tokens `UTF-8`, `ISO-8601`, `CVE-2024` all become refs (D5 mechanism, `findings.py:321-337`).
- D18 (B-D18): a document holding a form feed inside a line has 5 newline characters but `splitlines()` returns 6 lines; `locate` counts `\n` (`findings.py:295-296`) while `section_of` and `opcodes` use `splitlines` (`:309,415`).
- D10 (B-D10): after a refound round the row keeps the first claim (`first claim`) and the same `fp` (`ledger.py:207-238` updates anchor, span, severity_max, blocking, never fp, refs, claim, category).
- D15 (B-D15): `defer` of the only blocking row -> last round `PASS PASS`, status `deferred` (`ledger.py:350-360`).
- D16 (B-D16): a fix-map table row `| L1 | applied-not-really, rejected |` yields an `applied` item (`findings.py:199-223`, `_TABLE_APPLIED` matches `applied\b`); `fixmap_ok` is only reported (`ledger_cmd.py:70`).
- D17 (B-D17): after round 2 the row L1 is `resolved` with `blocking=True`; it is not listed under `## Other findings` (`ledger.py:467-468` lists `not r["blocking"]` rows only). Whether it appears in a prose section is decided by `brief_ids` (open or regressed only, `ledger.py:99-104`), so it is in neither; the ledger table carries it. I did not diff the full rendered prose.
- Run-1 D16 / B-D12 / B-D13: with `new_ledger(cap=1)` rounds 2, 3, 4 were all accepted after round 1 ESCALATE (`rounds merged past cap=1: [1, 2, 3, 4]`, last decision ESCALATE) (`ledger.py:114-121`).
- E-6: `resolve_slot(["a","b"], "fixed", ..., exclude=("a",))` -> `a` (a fixed slot ignores the soft exclusion).

### Register rows from slice 02 (new ids and added anchors)

| DR | Original id | Slice:line | Statement | file:line (HEAD / E2 tip) | Repro status | Pinned by test | Fix owner |
|---|---|---|---|---|---|---|---|
| DR-052 | R2CM D10 | 02:212,138 (R2CM:138) | A refound row never updates `fp`, `refs`, `claim` or `category`; after revisions move sections the fp path compares a stale section | `RV/ledger.py:207-238` | REPRODUCED (claim and fp unchanged) | none | CORE ledger |
| DR-053 | R2CM D15 | 02:222 | `defer` has no status precondition, rewrites the stored last-round verdict/decision to PASS, no undefer, no record of who | `RV/ledger.py:350-360` | REPRODUCED (`PASS PASS`) | `test_review_cli.py:296-312` exercises defer then verdict 0 (as a feature, not read in full) [UNVERIFIED as a pin] | CORE ledger |
| DR-054 | R2CM D16 | 02:221 | Fix-map items for non-open rows are skipped without an output entry; the table fallback treats any row whose second cell starts "applied" as applied; `fixmap_ok` is reported but not enforced | `RV/ledger.py:328-329`; `RV/findings.py:199-223`; `RV/ledger_cmd.py:61-71` | REPRODUCED (table fallback) | none | CORE ledger |
| DR-055 | R2CM D17 | 02:220 | `## Other findings` lists only rows with `blocking=False`; a blocking row that is resolved or deferred is in neither prose section | `RV/ledger.py:467-468` | REPRODUCED (not in Other findings) / TRACED (rest) | none | CORE report renderer |
| DR-056 | R2CM D18 | 02:176 | Line-model mismatch: `locate` and `_blocks_after` count `\n`, `section_of` and `opcodes` use `splitlines()` | `RV/findings.py:48-49,295-296,309,415` | REPRODUCED (5 vs 6) | none | CORE anchor |
| DR-057 | R2CM D19 | 02:160 | A two-token fence info string does not match, the block is not found | `RV/findings.py:27` | REPRODUCED | none | CORE parser / brief |
| DR-058 | R2CM D20 | 02:161,164 | A quoted example block plus the real block -> "more than one block", `ok=False`; the heading error names `## Findings block` only | `RV/findings.py:31,131,143-150` | REPRODUCED | none | CORE parser |
| DR-059 | R2CM D21 | 02:218,224 | `merge --out` and `capture --out` writes are not atomic and capture does not create parent dirs; the ledger save is atomic but has no lock; the report is written before the ledger is saved | `RV/merge_cmd.py:113-116`; `RV/ledger_cmd.py:134-136`; `RV/ledger.py:52-63` | TRACED | none | CORE CLI |
| DR-060 | R2CM D22 | 02:165 | An empty claim is accepted | `RV/findings.py:118` | REPRODUCED | none | CORE parser |
| DR-061 | R2CM D23 | 02:172 | `_REF_TOKEN` is case-sensitive, lowercase `ac-1` is not a ref; free-text tokens (`UTF-8`, `ISO-8601`, `CVE-2024`) become refs | `RV/findings.py:29,321-337` | REPRODUCED | none | CORE (id grammar from the profile) |
| DR-062 | R2CP 9 | 02:414 | `confidence-calibrator` is troubleshoot-shaped (6 dimensions, escalation rubric) while reflect expects a 5-dimension mean | `src/superclaude/agents/confidence-calibrator.md` lines 3, 15, 48, 61, 67 as cited in slice 02:414 | UNVERIFIED (file not re-read in this item) | n/a | MODULE-reflect / CORE calibrator |
| DR-063 | R2CP 10 | 02:415 | `reflect-reviewer` output is UC-2-shaped, yet Tier 2 spawns it for every mode including UC-1 (partly answered by findings-v2 `lens: reflect-pre` in shadow) | slice 02:415 cites `reflect-reviewer.md:3,:71-99` and `SKILL.md:646` | UNVERIFIED (not re-read here) | n/a | MODULE-reflect |
| DR-064 | R2CP 16 / E-10 | 02:265 | `claude-fable-5-1` is available and launchable in `anthropic-only` but is in no tier list (and reflect rejects Fable by rule) | `RV/data/review-tiers.default.json:14,19,33,35` (the model name appears only in names, class map, available and launch) | REPRODUCED by Grep (4 lines, none in an `aliases.*.models` list) | none | CORE panel data |
| DR-065 | R2CP 17 | 02:416 | The tasklist skill text says reflect "offers a Tier-3 `task-builder` remediation", but reflect's default Tier-3 route is `sc:workflow` | slice 02:416 (`sc-tasklist-protocol/SKILL.md:1640`) | UNVERIFIED (not re-read here) | n/a | MODULE-tasklist (text fix) |
| DR-066 | R2CP 18 / C-S5 | 02:269,406,535 | Three or four model registries: reflect skill aliases, reflect CLI `T2Model0N`, the panel tier JSON, and the E2 harness ladder; at HEAD shadow mode resolves through the panel, so the claim "neither reads the tier file" is partly stale | `src/superclaude/cli/reflect/ensemble.py:7,186-198`; `RV/panel.py`; E2 `run-reviewer.sh:19-43` | TRACED via slice (ensemble.py not re-read) [UNVERIFIED] | n/a | CORE (single registry) |
| DR-067 | RR-9 | 02:326 | Harness: an API-error-only result with the right model and block never enters the ladder loop: the entry guard includes `|| $APIERR`, the loop condition does not | E2 `EV/tools/run-reviewer.sh:66,73` (both lines seen at the tip) | TRACED | n/a | HARNESS |
| DR-068 | RR-1 | 02:318 | Harness reviewer sessions disallow only Edit, Write, NotebookEdit; Bash is not disallowed | E2 `run-reviewer.sh:48` | UNVERIFIED (line 48 not re-read in this item) | n/a | HARNESS / CORE (read-only reviewer agent, FX-8) |
| DR-069 | RR-2 | 02:319 | Harness hard-codes `/tmp/evalsb/{repo,cand}` and an absolute worktree path for `source.md` (`SRC_EVAL=/home/coder/.../eval-tasklist-review-panel/.dev/tasks/done/$PKG/source.md`) and never removes a stale copy | E2 `run-reviewer.sh:7-11` (line 10 confirmed by slice 01) | TRACED via slice 01:269 | n/a | HARNESS |
| DR-070 | RR-8 / E-12 | 02:267,325 | The ladder is a hand-kept map not read from the tier file and includes `muse-ember-1.0`, which the tier file lacks | E2 `run-reviewer.sh:19-43`; `RV/data/review-tiers.default.json` (no `muse-ember`, DR-016) | TRACED | n/a | CORE (ladder from tier data) |
| DR-071 | E-6 | 02:261 | A `fixed` slot ignores the soft exclusion; only `strict_distinct` or `hard_exclude` filter the candidates first | `RV/panel.py:536-537` | REPRODUCED (`a` kept) | none found | CORE panel |
| DR-072 | P-5 | 02:249 | A project or user file silently overrides the packaged default, and only `template_sha256` shows which file was used | `RV/panel.py:380-483` (`find_path`, `load_panel`, `load_tiers`) | UNVERIFIED (not re-read here) | n/a | CORE panel (low) |
| DR-073 | TS-6..TS-9 / V-38 | 02:307-310 | Test gaps: exact length boundaries; four of six categories never parsed in a test; malformed or absent resolution; duplicate reviewer id; rounds past cap; `--cap`; merged-report text for a broken reviewer; `@live7` all-seven-distinct | `tests/review/test_review_findings.py:111-122` (field test); `tests/review/test_review_ledger.py:376-385`; `tests/review/test_review_panel_live7.py` | TRACED (slice 01 at 01:235-239 re-derived part) | n/a | CORE tests |
| DR-074 | TS-2 (item e1) | 02:303 | The E2 notes claim "159" test functions; the per-file column sums to 179 | E2 `handoff-notes/run2/tests-tools.md:29` (TOTAL row) and `HANDOFF-run1-vs-run2.md:29` | REPRODUCED by re-summing (see below) | n/a | DROP (documentation error, EVAL note) |
| DR-075 | X2 | 02:83 | Run-2 notes say `T2bModel01` is not referenced anywhere in `src/` or `tests/`; slice 02 says `ccsession-models.json:107`, `README.md:445` and `tests/unit/test_ccsession_tiers.py:72,73,239` at the base contradict that | slice 02:83 | UNVERIFIED (not re-derived; my own slice-01 check, 01:80, found `T2bModel01` only under `skills/ccsession-tag/*` and `sc-implement-protocol/refs/retry.md` at HEAD) | n/a | DROP (documentation error) |
| DR-076 | W-4 | 02:338,615 | E2 notes say `combos/` holds 107 entries (SPEC.md + 106 row dirs); the tree has 96 directories (slice 02 says 97 entries) | E2 tip tree `EV/combos/` (my `git ls-tree -d --name-only` = 96 dirs, same as DR-047) | REPRODUCED (96 dirs) | n/a | EVAL (retraction) |
| DR-077 | C-S13 group | 02:41-42,543-545 | Internal inconsistencies of the comparison note: "four facts" against eight rows; "each claim checked" against rows 5-7 "not re-checked"; "line numbers stale on master" false for the six byte-identical files; the source-blind cause stated as fact while `COMBO-REPORT.md:373` says inference | slice 02:41-42,73,544-545 | UNVERIFIED (not re-derived; my own check of the byte-identical claim: `findings.py` 457 and `ledger.py` 494 lines at HEAD, equal to the hand-off's figures, 01:220) | n/a | DROP (documentation errors) |
| DR-078 | K-3 / GS-6 | 02:123,357 | `manifest.md:5` says "(local, never pushed)", which is stale | E2 `EV/manifest.md:5` (slice 01:262 read it at the tip) | TRACED via slice 01 | n/a | EVAL |

Item (e)1 re-sum of the E2 per-file table (read by `git show 6c0984326...:.dev/eval-workspaces/tasklist-review-panel/handoff-notes/run2/tests-tools.md`, lines 14-28; the `159` figure is in the TOTAL row at line 29):

- `def test_` column, `tests/review`: 9 + 23 + 24 + 26 + 14 + 5 + 10 = 111. `tests/skills`: 5 + 9 + 14 + 8 + 21 + 11 = 68. Sum = 179. The stated total is 159, 20 too low.
- `collected` column: 9 + 23 + 24 + 41 + 14 + 5 + 10 = 126 and 5 + 18 + 33 + 14 + 62 + 46 = 178; sum = 304, which matches the stated 304.
- The "159" is not in the run-2 hand-off (grep for `159` in `HANDOFF-review-panel-unification-run2.md` returned no line); it is in the notes' TOTAL row and in `HANDOFF-run1-vs-run2.md:29`. Both figures: 159 stated [CODE-CONTRADICTED], 179 re-summed [CODE-VERIFIED by arithmetic over the table]. I did not recount the functions in the test files at the E2 base.

Item (e)2 (memory lesson "fenced yaml calibration not parsed by cluster"): at HEAD `src/superclaude/cli/review/cluster_cmd.py:27` `_FENCE = re.compile(r"```[ \t]*ya?ml[ \t]*\n(.*?)\n[ \t]*```", re.S | re.I)` and `:33-34` build the source list with fenced yaml blocks first and unfenced `calibration:` blocks after; `_embedded_calibration` (`:31-47`) then reads `calibration.per_finding`. Executed read-only: a card with a fenced `yaml` block gave `{'F1': 0.8, 'F2': 0.4}` and an unfenced block gave `{'F1': 0.7}`. `tests/review/test_review_cluster_cmd.py:30-40` builds cards with `fenced=True` by default and `:188-196` covers the unfenced path. So the lesson is [CODE-CONTRADICTED] for HEAD. `git log` of the file shows one commit, `d2d8a2d16` (#519, 2026-11-12), so the code did not change after that date; which CLI version was installed when the lesson was recorded is [UNVERIFIED] (no install log was opened). The register row for this is in the slice 11 section (X-16).

**Key Takeaways (slice 02)**
- Slice 02 adds 27 rows (DR-052..DR-078). Rows DR-052, 053, 054, 055, 056, 057, 058, 060, 061, 064, 071, 074 and 076 carry a REPRODUCED status in their own cell; the others are TRACED or UNVERIFIED as stated in each cell. The run-1 D16 evidence (rounds past cap) was reproduced and is recorded under DR-043 and DR-079.
- The three numbering schemes are now mapped; the crosswalk table in the final register lists every original id.
- DR-053 (`defer`) note: I did not read `test_review_cli.py:296-312` in full, so I do not claim it as a pin.

## Slice 03 (E2 original study, reports and tooling): evidence and rows

Slice 03 has its own two lists (section 11.1 product P1-P10, section 11.2 harness H1-H19, lines 357-392 of the slice, plus the code cross-check C1-C17 at lines 308-324). Mapping to the register (the same defect keeps its first DR id): slice03 P1 = DR-001/002/003; P2 = DR-002 (+ DR-088); P3 = DR-004; P4 = DR-006; P5 = DR-079; P6 = DR-002; P7 = DR-015; P8 = DR-017; P9 = DR-080; P10 = DR-001 (v2 side). slice03 H1 = DR-081; H2 = DR-028; H3 = DR-082 (+ DR-023); H4 = DR-031 and DR-030; H5 = DR-041; H6 = DR-040; H7 = DR-037; H8 = DR-036; H9 = DR-083; H10 = DR-038; H11 = DR-035; H12 = DR-084; H13 = DR-034; H14 = DR-033; H15 = DR-039 and DR-069; H16 = DR-024; H17 = DR-068; H18 = DR-085; H19 = DR-086.

Re-checks made for this slice (E2 tip via `git show`, HEAD via Grep):

- `findings_v2.py` imports `_check_flat` at `:21` and applies it at `:80` (citation quote 12-200), `:111` (claim 300), `:126` and `:132` (anchor 12-200), `:136` (anchor2 12-200), so the v1 drop limits reach reflect Tier 2 (P10) [CODE-VERIFIED].
- Slice 03 C4 says COMBO-REPORT:292 is wrong that findings are "discarded with no error": my repro (above, D2/D3) got `warnings=1` for the broken reviewer and `ledger.py:130-134` builds the warning. The line at the E2 tip reads "discarded with no error" (`COMBO-REPORT.md:292` printed at the tip) [CODE-CONTRADICTED on "no error"]. What is true: the warning names only the first error and never the dropped ids (see DR-002).
- `EV/tools/run-reviewer.sh` at the tip: the launch line passes `--disallowedTools Edit Write NotebookEdit` only and `--permission-mode bypassPermissions`, so Bash, WebFetch and /tmp writes are open to the reviewer (H17). The brief text states the 12-200 anchor limit and the categories but not the 300 claim cap (H16) (lines 13-18 and 44-50 printed at the tip).
- `EV/tools/run-reviewer.sh.bad-launch:19` puts `--disallowedTools Edit Write NotebookEdit "$BRIEF"` before the positional prompt: the variadic option swallows the prompt (H1; the failure text itself lives in `reviews-failed-launch-1/*/t1b-1.attempt1.err`, which I did not open) [TRACED].
- `EV/tools/tmp-scripts/README.md` (printed at the tip) lists `checks-gate8` among the key scripts; `git ls-tree` over that folder finds no file with that name (count 0) (H19) [CODE-VERIFIED].
- `EV/tools/tmp-scripts/judge-one.sh:7` is `[ -f "$D/score.json" ] && { echo "SKIP ..."; exit 0; }`, so a judge that wrote a plausible `score.json` and then died is never re-run (H8); the judge prompt asks "covered by a BLOCKING ledger row" without reference to `blocking_in_implement` (H9) [TRACED].
- `EV/analysis/audits/audit-D/summary.md:12,26` says 45 merges have no `merge-stdout.txt` [CODE-VERIFIED].

### Register rows from slice 03

| DR | Original id | Slice:line | Statement | file:line (HEAD / E2 tip) | Repro status | Pinned by test | Fix owner |
|---|---|---|---|---|---|---|---|
| DR-079 | slice03 P5 | 03:364 | `merge` is not re-runnable for a round: an existing ledger gives "the ledger expects round 2"; operators moved ledgers to `stale-r1/` | `RV/ledger.py:114-118`; `RV/merge_cmd.py:101-109` | TRACED (the same check made `round 4` after ESCALATE accepted in my repro, DR-043) | `tests/review/test_review_ledger.py:388` `test_round_cannot_be_merged_twice_or_out_of_order` pins the refusal as intended | CORE ledger (decide: idempotent re-merge or explicit `--redo`) |
| DR-080 | slice03 P9 | 03:368 | Three category vocabularies: ground-truth classes (`unpassable-ac`, `missing-task`, `ambiguity`, `contradiction`), findings categories (`unpassable-check`, `missing-requirement`, ...) and the reflect map in findings_v2 (`ordering`, `acceptance`, `coverage`, `contradiction`, `risk`, `deviation`) | `RV/findings.py:15-22`; `RV/findings_v2.py:41-48`; E2 `ground-truth.json` classes [UNVERIFIED, file not opened] | TRACED for the two code sides | `tests/review/test_review_findings_v2.py` (not read for this) | CORE schema (one vocabulary with per-module mapping) |
| DR-081 | slice03 H1 | 03:374 | Harness: the variadic `--disallowedTools` swallowed the positional prompt, so every first launch failed | E2 `EV/tools/run-reviewer.sh.bad-launch:19` | TRACED | n/a | HARNESS (fixed: prompt on stdin) |
| DR-082 | slice03 H3 | 03:376 | Harness: `source.md` was not shipped to the reviewer sandbox; terra and sol returned "incomplete" and luna returned empty reviews on affected packages; fixed 12:59:34 on 2026-11-12, all earlier luna data quarantined; the brief still does not name the file | E2 `run-reviewer.sh:7-11` (ship), `:13-17` (brief without `source.md`) | TRACED | n/a | HARNESS (fixed) / CORE brief (DR-023 stays open) |
| DR-083 | slice03 H9 | 03:382 | The judge counts "blocking" by a blocking-flagged ledger row, ignoring `blocking_in_implement`: 65 judge-blocking against 38 real over 71 rows (figures [UNVERIFIED], from `COMBO-REPORT.md:291`) | E2 `tools/tmp-scripts/judge-one.sh` (prompt step 2) | TRACED (prompt); figures UNVERIFIED | n/a | EVAL (metric definition) |
| DR-084 | slice03 H12 | 03:385 | Row names hid composition (`r2` treated as a muse row); "valid era" was chosen by row-name regex; retracted 2026-11-12 19:05 UTC | E2 `COMBO-REPORT.md:170-174`, `analysis/final-table.py` `valid()` [UNVERIFIED, not opened] | UNVERIFIED | n/a | EVAL |
| DR-085 | slice03 H18 | 03:391 | Pilot arms B and C used randomly drawn compositions per package (arm B: designSpec = sonnet, muse-spark, glm; design = sonnet, glm, glm) so the arms differ across packages | E2 `resolution-*.json` per package [UNVERIFIED, not opened] | UNVERIFIED | n/a | EVAL (disclosed) |
| DR-086 | slice03 H19 | 03:392 | `tools/tmp-scripts/README.md` lists `checks-gate8` as a key script; the file is absent from the 55-file folder | E2 `EV/tools/tmp-scripts/README.md`; `git ls-tree` count 0 | REPRODUCED | n/a | EVAL |
| DR-087 | doc error | 03:311,576 | `COMBO-REPORT.md:292` says the merge discards findings "with no error"; the code emits a per-reviewer warning (first error only) | E2 `COMBO-REPORT.md:292`; `RV/ledger.py:130-134` | REPRODUCED (`warnings=1`) | n/a | DROP (wording correction; the real defect is DR-002) |
| DR-088 | slice03 P2 (part) | 03:361 | 45 merges have no saved `merge-stdout.txt`, so even the first-error warning is lost for them | E2 `EV/analysis/audits/audit-D/summary.md:12,26` | REPRODUCED by reading at the tip | n/a | HARNESS (save merge stdout in the ledger or the report) |
| DR-089 | slice03 gaps 4-5 | 03:558-559 | Counts disagree: Qwen slots ("all 3" at `PILOT-REPORT.md:12`, "4 reviewer ids" per slice, "3 of 4 runs" at `SPEC.md:3`); quarantine files ("428" at `COMBO-REPORT.md:107`, "417" files in the tree) | E2 `PILOT-REPORT.md:12` (printed at the tip: "all 3 of its slots (one per package)"), `COMBO-REPORT.md:107` | UNVERIFIED (the 4 / 3-of-4 / 417 figures not re-derived) | n/a | EVAL (disclosure) |
| DR-090 | slice03 P8 | 03:367 | The product `tier3` list is exactly the two owner-excluded models (`glm-5.3`, `Qwen3.8-max`) and both packaged panels draw two tier-3 reviewers from it | `RV/data/review-tiers.default.json` tier3 list; `RV/data/review-panel.default.json:11` (same as DR-017, kept as a separate consequence row) | REPRODUCED (repro1: P4 line lists `glm-5.3`, `Qwen3.8-max` under every tier that holds them) | none | CORE panel data (merge into DR-017 in the final register) |

Notes: DR-090 duplicates DR-017 and is merged there in the final register (kept here so no slice id disappears). DR-034 (slice01 H5) gains the slice03 H13 detail: `cost.json` also counts a WebFetch auxiliary call (about 512 tokens) (audit-A:15,22, [UNVERIFIED], audit-A not opened).

**Key Takeaways (slice 03)**
- Slice 03 adds 12 rows (DR-079..DR-090); 5 of its original ids are product defects already in the register, the rest are harness or evaluation process faults (HARNESS or EVAL owners), which the core does not fix but must not repeat (identity check, atomic per-attempt files, real parser for the block check).
- One of its claims is corrected by reading code: "no error" on drops (COMBO-REPORT:292) is wrong, a first-error warning exists. Its P10 (findings-v2 shares the limits through `_check_flat`) is confirmed.

## Slice 04 (E2 original study, analyses and audits): evidence and rows

Slice 04 section S7 (lines 218-245) lists 26 items 7.1-7.26 and section S3 (lines 46-62) lists script defects 3.1-3.15. Mapping to existing rows: 7.5 = DR-048; 7.9 = DR-079; 7.10 = DR-002 and DR-087; 7.11 = DR-004; 7.12 = DR-006; 7.14 and 7.15 = DR-034; 7.18 = DR-083; 3.5 (`attrib.py`) = DR-038; 3.1 (flags) = DR-091. The remaining items are new rows below. All of them are about E2 artifacts and none touches source code outside `.dev/eval-workspaces/`.

Re-checks (E2 tip via `git show`; scratch snippet run with `uv run python -c`, nothing written):

- `EV/analysis/final-table.py:15-18` (`fullpkg`): `p.startswith(s) or s.startswith(p[:12]) and p.startswith(s[:12])`. Running a copy of the function on the control package id `TASK-WF-design-20261108-041415` returned `TASK-WF-designSpec-20261107-075614` (designSpec). So every exclusion flag that names the control package is applied to designSpec [REPRODUCED]. The slice's recomputed tables (69 vs 71 excluded row-packages; corrected clean tables) are [UNVERIFIED]: I did not run the script on the full data.
- `EV/analysis/three-way.py:19` builds `flagged=[p[:8] for p in PK]`; the same slice of the three package ids is `['TASK-WF-', 'TASK-WF-', 'TASK-WF-']` [REPRODUCED].
- `EV/analysis/audits/audit-D/flags.tsv`: `grep -c 'j1-'` = 0 lines, so batch j1 is absent from audit D (slice 04 7.2 says the same for all six flags files; I checked only D) [CODE-VERIFIED for D; A, B, C, E, F UNVERIFIED].
- `EV/analysis/audits/audit-A/summary.md:3` says 890 reviewer runs and `:22` says "59 WARN" for check E2; the flags.tsv count of 54 is slice 04's recount [UNVERIFIED].
- `EV/analysis/final-table.py:11-14` (`valid()`) excludes `contaminated`, `superseded`, `quarantine`, `invalid` and rows starting `i1-`, `i2-`; slice 04 3.15 says five other scripts use different predicates [UNVERIFIED for the other five].

### Register rows from slice 04

| DR | Original id | Slice:line | Statement | file:line (E2 tip) | Repro status | Pinned by test | Fix owner |
|---|---|---|---|---|---|---|---|
| DR-091 | slice04 7.1 / 3.1 | 04:48,220 | `fullpkg()` resolves the control package to designSpec (12-character prefix test), so control-package AUDIT-CLEAN exclusions hit the wrong package; 11 more flags carry truncated or `*` package names that resolve to `None` and exclude all three packages | `EV/analysis/final-table.py:15-18` | REPRODUCED (function copy); effect on the committed AUDIT-CLEAN table UNVERIFIED | none (no tests in A1) | EVAL (fix before reuse) |
| DR-092 | slice04 7.2 | 04:221 | Batch j1 (45 runs, evidence for the "sonnet + 2x luna" decision update) is in none of the six audits | `EV/analysis/audits/audit-D/flags.tsv` (0 lines with `j1-`) | REPRODUCED for audit D only | n/a | EVAL |
| DR-093 | slice04 7.3 | 04:222 | Audit-A summary prose does not match its own flags file (59 vs 54 for E2; 9 vs 1 for E11; "930 runs" vs 890) | `EV/analysis/audits/audit-A/summary.md:3,22,30` | prose lines TRACED; flags recount UNVERIFIED | n/a | EVAL |
| DR-094 | slice04 7.4 | 04:223 | Audit D explains 92 dropped findings by validity rules but 109 were dropped net: 17 have no recorded reason (haiku 7 vs 23, grok 1 vs 2) | `EV/analysis/audits/audit-D/summary.md` lines 16-18 | UNVERIFIED (the 109 comes from `run1.txt`, not opened) | n/a | EVAL (and CORE: the merge should record why it dropped) |
| DR-095 | slice04 7.6 | 04:225 | "16 empty terra reviews in valid-era rows" is 14 terra and 2 luna by slice 04's recount | E2 `COMBO-REPORT.md:294` | UNVERIFIED | n/a | EVAL (retraction) |
| DR-096 | slice04 7.7 | 04:226 | "2x luna + 2x ember has 2.75-3.25 more wrong blockers than every comparator" conflates two panels: the +3.25 row is h2 (sonnet + 2x luna + 2x ember), and g6 was not tested against h1, h2, sonnet+ember or haiku+2x luna | E2 `COMBO-REPORT.md:298`; `analysis/audits/audit-F/stats.tsv` | UNVERIFIED | n/a | EVAL (retraction) |
| DR-097 | slice04 7.8 / 3.4 | 04:51,227 | 48 tests with no multiplicity correction, n = 4-6 per panel, a permutation minimum p of 0.029 for 4 vs 4, and the same three packages reused (pseudo-replication) | E2 `analysis/three-way.py`; `audits/audit-F/flags.tsv:56` | UNVERIFIED | n/a | EVAL (stats protocol) |
| DR-098 | slice04 7.13 | 04:232 | Reviewer outputs were hand-edited (`.catfix.md`, category rename) and merged instead of the originals; one `R1.catfix.md` appears in a `merged-anon.md` (audit-E leak flag) | E2 `reviews/**/*.catfix.md` (20 files per slice 03:28) | UNVERIFIED | n/a | EVAL (hygiene; same root as DR-028) |
| DR-099 | slice04 7.16 | 04:235 | `elapsed` sums the slowest reviewer per package and excludes quarantined re-runs and the 42-minute Qwen run, so wall-clock comparisons are optimistic | E2 `audits/audit-F/flags.tsv:54` | UNVERIFIED | n/a | EVAL (metric) |
| DR-100 | slice04 7.17 | 04:236 | A refusal is recorded as `verdict: FAIL` with an empty findings block (39 of 51 incompletes have `blocking=0 verdict=FAIL`); with no fallback, a merge sees a refusing reviewer as a reviewer with no findings | merge side: `RV/ledger.py:127-157` (a block with zero findings is `ok=True`); v2 side: `RV/findings_v2.py:40` `COMPLETION_STATES` has no "refused" or "incomplete" state | TRACED (merge treats an empty valid block as clean); the 39/51 figures UNVERIFIED (audit-B not opened) | none found | CORE (explicit incomplete status; the `incomplete` return is a prompt rule only, `RP:32`) |
| DR-101 | slice04 7.19/7.20 | 04:238-239 | Benchmark concentration: three defects (DS GT3, DS GT7, AL GT2) account for 131 of 147 catches (89%); four GT items never caught in 106 runs; 89 real-blocking catches by any row vs 38 by a blocking row | E2 `analysis/presence.txt:10-11`, `allsets-table.md:65` | UNVERIFIED | n/a | EVAL (ground truth) |
| DR-102 | slice04 7.24 / 3.15 | 04:62,243 | Six different "valid-era" predicates give different row populations (71, 76, 665 runs) | E2 `final-table.py:11-14` (one of six; the other five not read) | partly TRACED | n/a | EVAL |
| DR-103 | slice04 7.25 | 04:244 | `COMBO-REPORT.md` above line 289 still shows retracted numbers (n2-sonnet-src 8/14-5/8; "second run adds nothing"; "haiku overlap 8 of 8"; "ember is weaker than wonder") | E2 `COMBO-REPORT.md:132` and following (slice 01:318 reports the stale headline at tip) | UNVERIFIED here | n/a | EVAL (supersession header exists at `:289`) |
| DR-104 | slice04 7.26 | 04:245 | `three-way.py` prints the first eight characters of each package id (`TASK-WF-`) as its flagged list, so the exposure per package cannot be read | E2 `analysis/three-way.py:19` | REPRODUCED | n/a | EVAL |
| DR-105 | slice04 3.7 | 04:54 | `untried.py` `ok()` does not exclude `i1`/`i2` or "invalid" rows and uses judge-blocking, not real blocking | E2 `analysis/untried.py:7-8` | UNVERIFIED (not opened) | n/a | EVAL |
| DR-106 | slice04 3.8 / 7.21-7.23 | 04:55,240-242 | Unverifiable artifacts: `gt2-hits.txt` has no generator script; the blind re-judge of 12 rows (12/12, 19/19) and audit-E `check2.py` output have no committed artifact; raw judge sessions are not in the commit | E2 `analysis/gt2-hits.txt`; `analysis/RAW-TRANSCRIPTS-NOT-COMMITTED.md:2` (2,916 files, read at the tip) | UNVERIFIED | n/a | EVAL (disclosure) |

**Key Takeaways (slice 04)**
- Slice 04 adds 16 rows (DR-091..DR-106), all EVAL except DR-100 (CORE): the only core-relevant new defect is that a refusal is indistinguishable from an empty review.
- Two slice-04 defects were reproduced by running copies of the E2 code (DR-091, DR-104). The recomputed numbers behind them were not re-run.

## Slice 09 (review package code): evidence and rows

Slice 09 section G (lines 247-279) holds D-1..D-31 (scheme E: "slice 09 D-n", written with a hyphen). Scheme E ids collide in spelling with scheme A ids (D1-D13), so every cite below says "slice09 D-n". Open item (b) lists D-1, D-2, D-3, D-5, D-6, D-11, D-25, D-26 as pinned by tests; I checked each pin against the test file names and lines (results in the rows). Mapping to existing rows: slice09 D-2 = DR-002; D-3 = DR-006 (+ DR-108 for the stuck-row effect); D-5 = DR-014; D-6 = DR-007, DR-061 and DR-005; D-8 = DR-021; D-14 = DR-059; D-18 = DR-020; D-19 = DR-054; D-27 = DR-058; D-28 = DR-010; D-29 = DR-018, DR-022 and DR-125 (new). Everything else is a new row.

Reproduction at HEAD (third read-only run, `/tmp/review-panel-run2-2.17/repro4.py`; `git status` unchanged afterwards):

- D-6 token matrix (refs passed through `refs_norm`): matched `UTF-8`, `GPT-4`, `ISO-8601`, `US-001`, `TASK-003.2`, `NFR-1`, `P1`; not matched `fr-9`, `FR-12a`, `P10`, `STORY-1`, `T01.02`, `REQ_1`, `AC1` (`findings.py:29`).
- D-7: a fixed slot with `count: 2` validates (`validate_panel` returns `[]`) and resolves to `['claude-sonnet-5-5', 'claude-sonnet-5-5']` (`panel.py:230,536-537`).
- D-10: `@reflect-pre`, `@reflect-lite`, `@reflect-post` in the gateway environment all raise `ValueError: invalid reflect resolution: t1b-1: launch None is not one of sonnet, opus, haiku ...` (`panel.py:153-156`).
- D-15: a 7-reviewer template named `reflect-big` validates with no errors when no tier file is passed, and with the tier file gives `a reflect template allows at most 3 reviewers; found 7` (`panel_cmd.py:124`, `panel.py:447-467`).
- D-11: a `deferred` row re-found as blocking stays `deferred`, verdict `PASS`, `brief_ids=[]` (`ledger.py:99-104,235-238`).
- D-12: `findings.annotate` on a findings-v2 line that carries `citations` and no `anchor` raises `KeyError: 'anchor'` (`findings.py:346-349`).
- D-13: after `apply_revision` the row is `resolved_check` while `ledger.verdict()` still returns `FAIL` (`ledger.py:363-372`).
- D-1: a row reported by reviewers `a` and `b`, revised, then re-reviewed by a different reviewer `c` with an empty block, becomes `resolved` and the verdict is `PASS` (`ledger.py:254-258`).
- D-4: a row with `span=None` and a fix map entry `applied` lands in `named_not_touched` and stays `open` (`ledger.py:331-339`).
- D-27: two `## Findings block` headings with a block each -> `ok=False`, `more than one findings-v1 block; the last one is used`, kept id from the last block (same mechanism as DR-058).

Static checks (Grep or Read at HEAD): `cluster_cmd.py:151` calls `fv2.parse_block(text, assigned_rows=..., observed_rows=...)` without `lens` (D-20); `verify_cmd.py:125-128` fails when the coverage file lacks a card while `cluster_cmd.py:148` uses `cover.get(rid)` (D-21); `channel_of` (`findings_v2.py:190`), `V1_FIELDS` (`:25`), `COMPLETION_STATES` (`:40`), `manifest.read_committed` (`manifest.py:176`) and `manifest.reusable_stages` (`manifest.py:402`) are referenced only by `tests/review/*` and the defining files; `scripts/` has no hit (D-22); `cluster.py:35-38` docstring says the spec divides by the sum of calibrated confidences and the code uses each reviewer's best finding (D-26); `cluster.py:119-123` `_fingerprint` joins an empty string where v1 has the section (D-25); `telemetry.py:196-268` `validate_record` checks keys, the `context` values, `by_severity` shape, `stratum`, `ts_utc`, never the type of the values inside the six groups (D-31, by reading, not executed); `telemetry.py:418,428` use `INSERT OR IGNORE` (D-16).

### Register rows from slice 09

| DR | Original id | Slice:line | Statement | file:line (HEAD) | Repro status | Pinned by test | Fix owner |
|---|---|---|---|---|---|---|---|
| DR-107 | slice09 D-1 | 09:249 | Clearing by absence: a `resolved_check` row becomes `resolved` when no member of the current round matched it; nothing requires that the reviewers who found it took part, that their block was valid, or that they had the revised region in scope | `RV/ledger.py:254-258`; `RV/panel.py:600-605` | REPRODUCED (reviewer `c` cleared a row `a` and `b` had found) | YES as intended: `tests/review/test_review_ledger.py:193` `test_cleared_after_the_next_round_and_refound_stays_open` and `:376` | CORE ledger ("find once, then verify" per row) |
| DR-108 | slice09 D-4 | 09:252 | A row with no span can never be moved to `resolved_check` by a fix: it goes to `named_not_touched` forever and stays blocking until escalation | `RV/ledger.py:331-339` | REPRODUCED | partly: `test_review_ledger.py:153` covers `named_not_touched` for a span row | CORE (with DR-006) |
| DR-109 | slice09 D-7 | 09:255 | A fixed slot with `count` > 1 resolves to the same model N times even with `distinct_across_slots: true`; `validate_panel` allows count 1..4 for it | `RV/panel.py:230,536-537` | REPRODUCED (two Sonnet) | none found | CORE panel (cap fixed count at 1 or apply `exclude`) |
| DR-110 | slice09 D-9(b) | 09:257 | Telemetry column `output_by_severity` is created but always NULL; records populate `output_by_severity_CRITICAL/_MAJOR/_MINOR` | `RV/telemetry.py:313-343` (lines 323 and 340 set the suffixed names; the bare column not re-read) | UNVERIFIED (the `[RUN]` count of 59 columns not re-run) | none | CORE telemetry |
| DR-111 | slice09 D-10 | 09:258 | The packaged reflect templates cannot resolve in the `gateway` environment: `launch` is `None` and the reflect check accepts only sonnet/opus/haiku | `RV/panel.py:137-157`; `RV/data/review-tiers.default.json:25-30` | REPRODUCED (three templates raise) | not pinned: the gateway tests cover default and live7 only (`test_review_panel.py:303`) | CORE (launch policy per environment; links DR-015) |
| DR-112 | slice09 D-11 | 09:259 | A `deferred` row that is re-found as blocking keeps status `deferred` and is ignored by `_brief_ids`; deferral has no owner, reason check or expiry | `RV/ledger.py:99-104,235-238,350-360` | REPRODUCED | partly: `test_review_ledger.py:396` `test_defer_turns_a_blocking_row_into_deferred` pins deferral as a feature; reopening is untested | CORE ledger (decide and document) |
| DR-113 | slice09 D-12 | 09:260 | v1 `annotate` raises `KeyError: 'anchor'` on a findings-v2 line with citations and no anchor, so v2 findings cannot enter the v1 ledger without an adapter | `RV/findings.py:346-349`; `RV/findings_v2.py:122-133` | REPRODUCED | none | CORE (one finding model, two locators) |
| DR-114 | slice09 D-13 | 09:261 | The stored verdict is not derived: after `revise` or `defer` the stored last-round verdict is stale (FAIL while every blocking row is `resolved_check`) | `RV/ledger.py:350-372`; `RV/ledger_cmd.py:94-109` | REPRODUCED | indirect | CORE ledger |
| DR-115 | slice09 D-15 | 09:263 | `review panel validate` does not apply the reflect profile when no tier file is given | `RV/panel_cmd.py:116-129`; `RV/panel.py:447-467` | REPRODUCED | `test_review_cli.py:170` covers generic files only | CORE CLI |
| DR-116 | slice09 D-16 | 09:264 | The telemetry loader drops changed duplicates silently (`INSERT OR IGNORE` on `record_id`) and `append_record` routes a run id to the first existing month directory | `RV/telemetry.py:287-307,415-435` | TRACED (lines 418 and 428 read) | idempotency pinned: `tests/review/test_review_telemetry.py:201-221` (range from slice 09, not re-opened) | CORE telemetry |
| DR-117 | slice09 D-17 | 09:265 | `model_scores` can count a run's cost twice when it has two non-superseded outcomes of the same truth basis | `RV/telemetry.py:362-379` | UNVERIFIED (slice 09 did not execute it either) | 1:1 arithmetic pinned (`test_review_telemetry.py:223-322`) | CORE telemetry (verify first) |
| DR-118 | slice09 D-20 | 09:268 | `cluster_cmd` never passes `lens` to `findings_v2.parse_block`, so the lens-dependent rules apply only when each line carries its own `lens` | `RV/cluster_cmd.py:151` | TRACED | `test_review_findings_v2.py:160-175` tests the argument form only (slice 09) | CORE (lens as a run parameter) |
| DR-119 | slice09 D-21 | 09:269 | Inconsistent strictness between sibling commands: `verify-citations --coverage` fails on a missing card entry, `cluster --coverage` does not; `verify-citations` verifies findings of an invalid block, `cluster` drops them | `RV/verify_cmd.py:125-139`; `RV/cluster_cmd.py:148-163` | TRACED | partly | CORE (one shared card loader) |
| DR-120 | slice09 D-22 | 09:270 | Dead or decorative API in the E1 code: `channel_of`, `V1_FIELDS`, `COMPLETION_STATES`, `read_committed`, `reusable_stages` have no production caller; the `channel` field never influences clustering, verdict or manifest | `RV/findings_v2.py:25,40,190`; `RV/manifest.py:176,402` | REPRODUCED by Grep (callers only in `tests/review/*`) | tests only (`test_review_manifest.py:207-342`, `test_review_findings_v2.py:404-418`) | CORE (expose or drop) |
| DR-121 | slice09 D-23 | 09:271 | The run manifest has no lock: `advance` and `record_attempt` are load-modify-save, so two concurrent coordinator calls can lose an update; "one coordinator writes" is documented, not enforced | `RV/manifest.py:156-163`; `RV/manifest_cmd.py:169-205` | UNVERIFIED (not re-read; slice 09 read only) | none | CORE manifest |
| DR-122 | slice09 D-24 | 09:272 | `card_convert` is lossy: medium/important/should-fix/low/nit/info map to MINOR non-blocking, `refs` always `[]`, no quote, so a converted card can never raise `quote-not-found` | `RV/card_convert.py:71-82,209-221` | UNVERIFIED (not re-read) | `test_review_card_convert.py:56,405` | MODULE-reflect (migration shim only) |
| DR-123 | slice09 D-25 | 09:273 | The v2 fingerprint has no section (always empty) and equality still needs non-empty `refs_norm`, so v2 clustering without ref tokens relies on same-path line proximity | `RV/cluster.py:119-123,161-181` | TRACED (the empty string at `:121` read) | YES as intended: `tests/review/test_review_cluster.py:233-260` (range from slice 09, not re-opened) | CORE cluster |
| DR-124 | slice09 D-26 | 09:274 | Design/code drift: the `cluster.py` docstring admits the code divides by each reviewer's best finding confidence, not by the sum of calibrated confidences the spec names | `RV/cluster.py:35-38,389-399` | TRACED (docstring read) | YES: `test_review_cluster.py:361-400` pins the code form (range from slice 09, not re-opened) | CORE cluster (record as a spec/code conflict) |
| DR-125 | slice09 D-29 | 09:277 | Policy hard-coded in code: env names `gateway` / `anthropic-only` and `T3Model01`, strata sonnet/haiku, `_REFLECT_LAUNCH` = (sonnet, opus, haiku) | `RV/panel.py:72,485-494`; `RV/telemetry.py:112-115` | REPRODUCED (D-10 error text names the three values) | pinned: `test_review_panel.py:331` | CORE (expose as configuration) |
| DR-126 | slice09 D-30 | 09:278 | The ledger holds one document (`doc` path, line-range spans), so a multi-file target (PR diff, tasklist bundle) has no representation; `apply_revision` refuses an `--old` with another hash | `RV/ledger.py:37-38,301-314` | TRACED (read) | `test_review_ledger.py:505` `test_revision_from_a_text_other_than_the_reviewed_one_is_refused` pins the refusal | CORE (needed for PR review) |
| DR-127 | slice09 D-31 | 09:279 | The "no document text in a record" rule is a convention: `validate_record` checks keys, `context` values and the `by_severity` shape, never the type of the values inside the six groups | `RV/telemetry.py:3,196-281` | TRACED (read; not executed) | `test_review_telemetry.py:156-163` checks only 40-character windows | CORE telemetry (type-check group values) |

Open item (b), pins re-checked (the eight ids named in the assignment):

| slice09 id | Test pin found | Verdict |
|---|---|---|
| D-1 | `test_review_ledger.py:193`, `:376` | confirmed |
| D-2 | `test_review_ledger.py:376-385` | confirmed (read in full) |
| D-3 | `test_review_ledger.py:408` `test_missing_anchor_is_kept_without_a_span`; `test_review_findings.py:215-230` (`anchor_status`/`anchor_ambiguous` asserted) | confirmed by test names and lines |
| D-5 | `test_review_panel.py:204-214`, `test_review_panel_exclusion.py:208` (names read), `:208-213`, `test_review_panel_live7.py:48-60`, `test_review_reflect_templates.py:127` | first two read in full; the other two by slice 09 only |
| D-6 | `test_review_findings.py:201-212` (line 212: `assert "FR-9" not in got  # lower-case ids are not matches`) | confirmed |
| D-11 | `test_review_ledger.py:396-405` (deferral feature; reopening not tested) | partly confirmed |
| D-25 | `test_review_cluster.py:233-260` | by slice 09 only [UNVERIFIED] |
| D-26 | `test_review_cluster.py:361-400` | by slice 09 only [UNVERIFIED] |

Corrections to earlier rows (the final register carries them): DR-006 is pinned by `test_review_ledger.py:408` and `test_review_findings.py:215-230`; DR-061 is pinned by `test_review_findings.py:201-212`; DR-054 is pinned by `test_review_findings.py:163` `test_fixmap_table_fallback`; DR-058 is pinned by `test_review_findings.py:125` `test_last_of_two_blocks_wins`; DR-053 deferral is pinned as a feature by `test_review_ledger.py:396`.

**Key Takeaways (slice 09)**
- Slice 09 adds 21 rows (DR-107..DR-127); its other 10 ids map onto existing rows. Of the 21 new rows, 10 are REPRODUCED (DR-107, 108, 109, 111, 112, 113, 114, 115, 120, 125), 7 TRACED (DR-116, 118, 119, 123, 124, 126, 127) and 4 UNVERIFIED (DR-110, 117, 121, 122).
- The test pins matter for the core: D-1, D-2, D-3, D-5, D-6 are asserted as intended behaviour, so fixing them is a contract change, not a bug fix.

## Slice 10 (the reflect side, E1): evidence and rows

Slice 10 has three lists: defects D-01..D-25 (section S14, lines 359-385; zero-padded, "slice10 D-nn"), conflicts C-01..C-19 (S17, lines 464-484) and hand-off claims H-01..H-12 (S20, lines 527-540; these H ids are not the harness H1-H12). Mapping: slice10 D-09 = DR-062; D-24 and C-10 see below; C-01 = D-06; C-02 = D-07; C-03 = D-01; C-04 = D-09; C-05 = D-10; C-08 = D-20; C-09 = D-02; C-11 = D-08; C-12 = D-13; C-13 = D-23; C-15 = D-04; C-16 = D-19; C-17 = D-18; C-18 = D-17; H-02 = D-13.

Static re-checks at HEAD (Grep or Read):

- `src/superclaude/cli/reflect/ensemble.py:74` `REFLECT_CONTRACT_VERSION = "1.0"`, `:773` `merge_method = "adversarial" if reviewer_count >= 2 else "single-reviewer-fallback"`, `:788,806` write them into the contract. `contract.py:299` is the only backstop (null convergence at tier 2).
- Convergence thresholds: `sc-reflect-protocol/SKILL.md:703` says `>=0.75 PASS, >=0.60 PARTIAL, <0.60 FAIL`; `cli/reflect/contract.py:309-326` degrades a present score below `0.80` (`_score_f < 0.80`, return `low-convergence`).
- Single vendor: `SKILL.md:146,839` say warn-only in v1; `contract.py:286-288` returns `single-vendor` (a degrade) unless `allow_single_vendor`.
- Diversity vocabulary: `SKILL.md` L838 (slice 10) says `full | degraded`; `cli/reflect/_diversity.py:15` returns `"full" if len(distinct_model_ids) >= 2 else "insufficient"`.
- `refs/reflection-rubric.md:39` names `{Aligned, Refinement, Drift, Regression}`; the taxonomy elsewhere uses Authorized expansion / Necessary deviation / Drift / Regression (slice 10).
- `reviewer_briefs_materialized` is emitted by `refs/reviewer-spec.md:78` and mentioned at `:51`; Grep over `src` finds no occurrence in `cli/reflect/panel_lint.py` (the lint field lists).
- `cli/reflect/commands.py:239` help says "default: --promote" and `:538` forwards `--promote`/`--no-promote` explicitly; `cli/reflect/runner.py:457` comment says "FR-9: --no-promote is the hard default; dropped only on --promote".
- `tests/cli/reflect/test_shadow_exit_script.py:292-299` asserts only `code in set(se.EXIT.values())` and report text; it skips when `.dev/reflect` is absent.
- `cli/reflect/contract.py:403` cites `SKILL.md:754`; `SKILL.md:858` holds `needs_human_decision: bool` (slice 10 says the fields are at 761 and 858).
- `cli/reflect/__init__.py:1-15` describes a wrapper that launches `/sc:reflect --mode post` as a subprocess and lists five modules (models, config, contract, runner, commands); slice 10 says there are ten.
- A Grep for `t2-engine` over `src/superclaude/commands/**/*.md` and `src/superclaude/cli/**/*.py` finds only `cli/review/manifest*.py` (the manifest keys and one option), none in the reflect command file or the reflect CLI.
- I did not re-run `scripts/reflect_shadow_exit.py` (it writes a report file to `--out` at `:404-405`, and I did not check the default path), so D-12, D-13, D-21, D-22 rest on slice 10's recorded output.

### Register rows from slice 10

| DR | Original id | Slice:line | Statement | file:line (HEAD) | Repro status | Pinned by test | Fix owner |
|---|---|---|---|---|---|---|---|
| DR-128 | slice10 D-01 / C-03 | 10:361,468 | The code-driven reflect engine emits `contract_version "1.0"` and keys outside the 1.8.0 lists, so the 1.8.0 lint would fail it | `src/superclaude/cli/reflect/ensemble.py:74,787-832` | TRACED (`:74` and `:788` read; the 10 extra keys and the probe result are slice 10 only [UNVERIFIED]) | none found | MODULE-reflect |
| DR-129 | slice10 D-02 / C-09 | 10:362,474 | The code engine sets `merge_method = "adversarial"` whenever there are two or more reviewers, even if the adversarial scorer failed; only the null-convergence trigger backstops it | `ensemble.py:773`; `cli/reflect/contract.py:299` | TRACED | none found | MODULE-reflect |
| DR-130 | slice10 D-03 | 10:363 | The code engine's deviation signal defaults to CLEAN unless the adversarial seam supplies it, so a code-engine PASS means "converged and no fatal errors", not "no deviation found" | `ensemble.py:87-118,446-465,527-533` (slice 10; not re-read) | UNVERIFIED | none found | MODULE-reflect |
| DR-131 | slice10 D-04 / C-15 | 10:364,480 | Code-engine swarm reviewers see only the tasklist body (no diff, spec or hunks) | `ensemble.py:608-630` (slice 10) | UNVERIFIED | none found | MODULE-reflect |
| DR-132 | slice10 D-05 / C-14 | 10:365,479 | The code engine has no executor-class exclusion, calibrator, evidence validator or per-finding schema; 9 of 13 recorded shadow runs had `executor_class_resolved: false` | `cli/reflect/*` (slice 10 Grep) | UNVERIFIED | none found | MODULE-reflect / CORE |
| DR-133 | slice10 D-06 / C-01 | 10:366,466 | Convergence thresholds differ: 0.75 / 0.60 in the skill, 0.80 in the wrapper, `< 0.75` in a falsifier case | `SKILL.md:703`; `cli/reflect/contract.py:309-326` | TRACED (two sides read; the falsifier line `SKILL.md` L1944 not re-read) | wrapper side pinned by `test_low_convergence_tier2_degrades` and `test_convergence_at_or_above_threshold_passes` (names from slice 10; my capped Grep did not list them) | CORE (one threshold, one owner) |
| DR-134 | slice10 D-07 / C-02 | 10:367,467 | Single vendor is warn-only in the skill but a DEGRADE in the wrapper unless `--allow-single-vendor`; 9 of 42 recorded legacy runs replay as `degraded/single-vendor` (slice 10) | `SKILL.md:146,839`; `cli/reflect/contract.py:286-288` | TRACED (both sides read; the 9 of 42 figure UNVERIFIED) | pinned in the wrapper: `tests/cli/reflect/test_fallback_select.py:42` (quorum, same vendor needs the flag) and the `degraded_single_vendor.yaml` fixture (slice 10) | CORE policy / MODULE-reflect |
| DR-135 | slice10 D-08 / C-11 | 10:368,476 | `t2_model_class_diversity` is `full | degraded` in the skill and `full | insufficient` in code | `cli/reflect/_diversity.py:15`; `SKILL.md` L838 (slice 10) | TRACED | none found | MODULE-reflect (wording) |
| DR-136 | slice10 D-10 / C-05 | 10:370,470 | `reflection-rubric.md` names the deviation classes `{Aligned, Refinement, Drift, Regression}`, everything else `Authorized expansion / Necessary deviation / Drift / Regression` | `src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md:39` | REPRODUCED by Grep | none found | MODULE-reflect (doc fix) |
| DR-137 | slice10 D-11 | 10:371 | The calibrator class capability ordering `{opus, sonnet, haiku, qwen, kimi, deepseek}` is an open question and `refs/model-capability-tiers.md` does not exist | `refs/reflection-rubric.md` L175-177 (slice 10) | UNVERIFIED | n/a | MODULE-reflect / CORE |
| DR-138 | slice10 D-12 | 10:372 | The Stage 2 shadow-exit result: 8 of 13 shadow runs fail EV-1 against 3 of 39 legacy runs; 6 parity failures; 9 of 13 runs have lint or manifest problems | `scripts/reflect_shadow_exit.py` output recorded in slice 10 S10.2 | UNVERIFIED (not re-run) | `test_shadow_exit_script.py:292` accepts any documented exit code (DR-140) | MODULE-reflect |
| DR-139 | slice10 D-13 / D-25 / C-12 / H-02 | 10:373,384,477,530 | The orchestrator writes unknown top-level keys (`zero_drop_flag`, `memory_status`, `notes`) into the contract in 2 of 13 shadow runs, violating "no key outside the stable list"; only the after-the-fact lint catches it | `SKILL.md:349` (rule), `cli/reflect/panel_lint.py:316-321` (lint; slice 10) | UNVERIFIED | none | MODULE-reflect |
| DR-140 | slice10 D-14 / slice11 X-20 | 10:374; 11:250 | `test_the_current_repository_reports_without_crashing` accepts any documented exit code, so a Stage 2 FAIL does not fail CI | `tests/cli/reflect/test_shadow_exit_script.py:292-299` | REPRODUCED by reading | is the test | MODULE-reflect (tighten or drop) |
| DR-141 | slice10 D-15 | 10:375 | HEAD-relative pins in `test_shadow_skill_contract.py` guard only uncommitted edits | `tests/cli/reflect/test_shadow_skill_contract.py:42-98` (slice 10) | UNVERIFIED | is the test | MODULE-reflect |
| DR-142 | slice10 D-16 | 10:376 | The `cli/reflect/__init__.py` docstring is stale: it describes a subprocess fan-out and lists five modules of ten | `src/superclaude/cli/reflect/__init__.py:1-15` | TRACED (five modules listed, read; "ten" from slice 10) | none | MODULE-reflect (doc) |
| DR-143 | slice10 D-17 / C-18 | 10:377,483 | The `contract.py` docstring cites `SKILL.md:754` for the needs_human_decision invariant; the field is at `SKILL.md:858` now | `cli/reflect/contract.py:403`; `SKILL.md:858` | REPRODUCED by Grep | none | MODULE-reflect (doc) |
| DR-144 | slice10 D-18 / C-17 | 10:378,482 | A runner comment says `--no-promote` is the hard default; the Click default is `--promote` | `cli/reflect/runner.py:457`; `cli/reflect/commands.py:236-239,538` | REPRODUCED by reading | none | MODULE-reflect (comment) |
| DR-145 | slice10 D-19 / C-16 | 10:379,481 | `commands/reflect.md` and the reflect CLI do not list `--t2-engine` (the skill documents it); the other omitted flags are not checked | `src/superclaude/commands/reflect.md` L10 (slice 10); Grep over `commands/**/*.md` and `cli/**/*.py` for `t2-engine` finds no reflect file | REPRODUCED for `--t2-engine` only | none | MODULE-reflect |
| DR-146 | slice10 D-20 / C-08 | 10:380,473 | Shadow cards live at `panel/cards/reviewer-<N>.md`, the EV-1 lint expects `reviewer-cards/reviewer-<N>-card.*`: two card layouts | `cli/reflect/panel_lint.py` L188; `reflect_shadow_exit.py` L59 (slice 10) | UNVERIFIED | none | CORE (one card layout) |
| DR-147 | slice10 D-21 | 10:381 | `cluster_agreement` is 1.000 in all 9 runs that recorded it (min = median = max); its meaning is unverified | shadow-exit script output (slice 10) | UNVERIFIED | none | MODULE-reflect (investigate; links DR-004 chaining) |
| DR-148 | slice10 D-22 / slice11 X-18 | 10:382; 11:248 | `shadow01` ran as legacy because the 2026-11-12 installed CLI lacked the panel options and `@reflect-pre` (installed-vs-dev drift); the dev tree now has them | `src/superclaude/cli/review/data/` (templates exist at HEAD); shadow01 `tier_decision.yaml` (slice 11) | UNVERIFIED for the installed CLI of that day | n/a | OPS (install-lag lesson) |
| DR-149 | slice10 D-23 / C-13 | 10:383,478 | `reviewer_briefs_materialized` is emitted by `reviewer-spec.md:78` but is not in the lint field lists, so a faithful emission fails lint L2 | `refs/reviewer-spec.md:51,78`; `cli/reflect/panel_lint.py` (no occurrence, Grep over `src`) | REPRODUCED by Grep (absence) | none | MODULE-reflect |
| DR-150 | slice10 C-07 | 10:472 | `--reviewers` is 2-3 (default 3) in the skill and the command, the wrapper clamps to [2,4] and allows 1 as a negative witness, and the panel uses `N_eff = min(--reviewers, alias count, 3)` | `SKILL.md:86,321`; `cli/reflect/config.py:334-335` (slice 10) | UNVERIFIED (not re-read) | none | MODULE-reflect |
| DR-151 | slice10 C-19 | 10:484 | The reflect skill directory carries 25 lines that mention `src/superclaude` (CLAUDE.md forbids reading installed primitives through that path); the test bounds the count to HEAD's; classification per line not done | `src/superclaude/skills/sc-reflect-protocol/*` (counts from slice 10) | UNVERIFIED | `test_no_new_src_superclaude_hit_in_the_skill_directory` bounds, does not zero | MODULE-reflect |
| DR-152 | slice10 H-11 | 10:539 | `test_no_nesting_guard.py` keeps an `xfail` marker although the test XPASSes now | `tests/cli/reflect/test_no_nesting_guard.py` (slice 10) | UNVERIFIED | is the test | MODULE-reflect |
| DR-153 | slice10 C-06 / slice11 X-16 | 10:471; 11:246 | The memory lesson "Fenced yaml calibration blocks are NOT parsed by cluster; use a bare indented calibration: mapping" is contradicted by the code | memory file `docs/memory/reflect/deviation-patterns-brainstorm-reflect-panel.md:64` (read); `RV/cluster_cmd.py:27-34` (see slice 02 item (e)2) | REPRODUCED (fenced yaml parsed at HEAD) | `tests/review/test_review_cluster_cmd.py:30-40` builds fenced cards by default | DROP (stale lesson; fix the memory note, installed-CLI version unverified) |
| DR-154 | slice10 D-24 / slice11 X-15 | 10:385; 11:245 | Hygiene: the memory file `docs/memory/reflect/deviation-patterns-brainstorm-reflect-panel.md` is untracked (101 lines per slice 10) and the experiment's memory write-back leaks run lessons into tracked and gitignored memory directories | session `git status` at start: `?? docs/memory/reflect/deviation-patterns-brainstorm-reflect-panel.md` | REPRODUCED (status line in the session context) | n/a | HARNESS / OPS |

**Key Takeaways (slice 10)**
- Slice 10 adds 27 rows (DR-128..DR-154); its D-09 reuses DR-062 and most of its conflict ids restate its own D ids (mapping at the top of the slice 10 section). The reflect-engine rows (DR-128..DR-132, DR-138, DR-139) belong to the reflect module, not the core; the core must only avoid copying their gaps (no per-finding schema, no executor-class rule, two thresholds).
- Policy conflicts the core must decide once: convergence threshold (DR-133), single-vendor warn or degrade (DR-134), the blocking rule (DR-025 plus findings-v2 `reflect_category` rule), and one card layout (DR-146).

## Slice 11 (E1 evidence artifacts): evidence and rows

Slice 11 section 8 (lines 229-252) lists X-1..X-22 (scheme G, "slice11 X-n"). Mapping: X-2 = DR-146 (+ lint regex below); X-6 = DR-139 and DR-149; X-15 = DR-154; X-16 = DR-153; X-18 = DR-148; X-20 = DR-140. The memory lesson (open item e2) is X-16; its row and the code reading are DR-153 and the slice 02 section.

Re-checks at HEAD:

- X-1: `scripts/reflect_shadow_exit.py:313` is `if (s_rate or 0.0) > (l_rate or 0.0):` with the message `EV-1 failure rate is higher than the legacy baseline` at `:314`; a missing legacy rate counts as 0.0 [CODE-VERIFIED].
- X-2: `src/superclaude/cli/reflect/panel_lint.py:188` `_CARD_FILE = re.compile(r"^reviewer-(\d+)-card\.(?:yaml|yml|md)$")`, used at `:273` against `reviewer-cards/` [CODE-VERIFIED].
- X-7: `scripts/reflect_stage0a_replay.py:68-69` set `PLAN_ID` and `PLAN_NUMBERS = {"card_dirs": 42, "merged": 33, "nulls": 7}`; that the replay cannot read `panel/cards/` blocks was not re-run [UNVERIFIED].
- X-14: the session `git status` lists `?? .dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboC-r3/artifacts/base-e8db2fe6/` [CODE-VERIFIED].
- `.gitignore:13` is `lib/` (read at HEAD); `git check-ignore -v` names `.gitignore:13:lib/` for `.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r5/lib/r5/x.py` and for `.../r3/lib/common.sh`, and `.gitignore:79:*.log` for `x/build.log`; `git ls-tree -r --name-only 6c0984326 .../20261113-collab | grep -c '/lib/'` = 0. So no file under any `lib/` folder of the E2 collaboration harnesses is in the commit [CODE-VERIFIED]. `.gitignore:114` is `.superclaude/`.

### Register rows from slice 11 and the `.gitignore:13` anchor

| DR | Original id | Slice:line | Statement | file:line | Repro status | Pinned by test | Fix owner |
|---|---|---|---|---|---|---|---|
| DR-155 | `.gitignore:13` (slices 07, 08 own the evidence) | 08:424,553-555,634; 07:256,341 | The `lib/` rule in the root `.gitignore` silently excludes every `lib/` folder from `git add`: the E2 collaboration harnesses lost `lib/` code (r2 `bin/lib/`, r3 `lib/{common,reviewer,package}.sh`, r5 `lib/r5/*.py`; r4 per slice 08), and `*.log` (`:79`) drops build logs, so the committed harnesses cannot run | `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.gitignore:13,79` | REPRODUCED (`git check-ignore -v`; 0 `/lib/` paths at the tip) | none | HARNESS (rename the folder or add `!` rules); core rule: a shared harness must not live under `lib/` |
| DR-156 | slice11 X-1 | 11:231 | The Stage 2 exit script treats an empty legacy baseline as 0.0, so any shadow EV-1 failure fails a runs root without legacy runs, and the verdict replay reports every degraded run as "new" | `scripts/reflect_shadow_exit.py:313-314` | REPRODUCED by reading | none found | MODULE-reflect (harness script) |
| DR-157 | slice11 X-3 | 11:233 | `merged-verdict.yaml` must be at `adversarial/merged-verdict.yaml`; the child skill leaves it at `adversarial/adversarial/` in shadow03, 06, 07 | `cli/reflect/panel_lint.py:271` (path rule, slice 11); artifacts under `.dev/eval-workspaces/shadow-model-combos/runs/` | UNVERIFIED (child-skill cause not investigated, artifacts not opened) | none | MODULE-reflect / EVAL |
| DR-158 | slice11 X-4 | 11:234 | Recorded `panel_parity: true` was wrong in 2 pilot runs and 4 combo runs (recorded true, recomputed false) | `.dev/reflect/` exit-ref and exit-combo outputs (slice 11) | UNVERIFIED | `recompute_parity` exists (`reflect_shadow_exit.py` L117-177 per slice 10 H-03) | MODULE-reflect (shadow protocol: copy the pin, recompute the parity) |
| DR-159 | slice11 X-5 | 11:235 | Contract diversity telemetry is blind to dispatch collapse: A3 reported `calibrator_diversity: full` and no identity mismatch while every agent served `claude-sonnet-5-5` | combo A3 contract, `results.md:35` (slice 11) | UNVERIFIED | none | CORE (observed-model identity check, links DR-031) |
| DR-160 | slice11 X-7 | 11:237 | The Stage 0a replay cannot read the `panel/cards/` findings-v2 blocks, reports shadow runs as 45 unconvertible cards and cannot measure T-9; `PLAN_NUMBERS` is frozen at 42/33/7 | `scripts/reflect_stage0a_replay.py:68-69` | TRACED (constants read; the unreadable-card behaviour not re-run) | `tests/review/test_reflect_stage0a_replay.py` exists (content not read) | MODULE-reflect |
| DR-161 | slice11 X-8 | 11:238 | Evidence-validator `drop_rate` is inconsistent with its counts (shadow03: `drop_rate 0.0` with `citations_dropped 1` of 16) | shadow03 `metrics.json` and contract (slice 11) | UNVERIFIED | none | MODULE-reflect |
| DR-162 | slice11 X-9 | 11:239 | `merged-verdict.yaml` has no uniform schema: blocking/medium/minor are `None` in 13 of 15 combo rows, verdict strings have 12 or more variants | combo `results.md:4-19` (slice 11) | UNVERIFIED | none | CORE (merged output schema) / MODULE-reflect |
| DR-163 | slice11 X-10 | 11:240 | The experiment ran on an installed skill that lags `src/` (reviewer-spec hash `b1032d61` against `177db4a7`) | `~/.claude/skills/sc-reflect-protocol/refs/reviewer-spec.md` against `src/.../refs/reviewer-spec.md` (hash comparison per slice 11) | UNVERIFIED (hashes not recomputed) | n/a | OPS (install lag) |
| DR-164 | slice11 X-11 | 11:241 | `PLAN.md:1-3` and `combos.json:4` still say "designed, NOT run" | `.dev/eval-workspaces/shadow-model-combos/` (slice 11) | UNVERIFIED | n/a | EVAL (doc) |
| DR-165 | slice11 X-12 | 11:242 | `runs.jsonl` has 14 of 15 combo rows (A-r2 missing), non-uniform ids, and `wall_clock_ms` estimates up to 3.8x off measured | `.dev/reflect/runs.jsonl` (gitignored per slice 11) | UNVERIFIED | n/a | EVAL / CORE (telemetry store replaces it) |
| DR-166 | slice11 X-13 | 11:243 | E1 made 7 reviewer-agent calls and the reason is unrecorded | `results.md:45` (slice 11) | UNVERIFIED | n/a | EVAL |
| DR-167 | slice11 X-14 | 11:244 | An untracked grounding checkout `runs/...comboC-r3/artifacts/base-e8db2fe6/` sits in the evidence tree | session `git status` | REPRODUCED (status line) | n/a | EVAL (clean up) |
| DR-168 | slice11 X-17 | 11:247 | shadow02 aborted at clustering: all 11 findings cited the same tasklist and chained into one cluster, `cluster_agreement null`, no root-cause record | shadow02 `audit.log` last line, manifest state `clustered` (slice 11) | UNVERIFIED (mechanism is DR-004/DR-123, chain flag at `RV/cluster.py:33-34`) | `test_review_cluster.py:108` pins chain flagging | CORE cluster / MODULE-reflect |
| DR-169 | slice11 X-19 | 11:249 | `analysis/extract.py` has a non-uv subprocess, `"cur" in dir()` and tuple medians | `.dev/eval-workspaces/shadow-model-combos/analysis/extract.py:85,106,167-169` (slice 11) | UNVERIFIED (not opened) | none | EVAL |
| DR-170 | slice11 X-21 | 11:251 | `combos.json` records only the class rotation, not the served model; `resolution.json` strategy `random` with seeds `2073600319|t4|1` | shadow03 `resolution.json` (slice 11) | UNVERIFIED | n/a | EVAL (model identity) |
| DR-171 | slice11 X-22 | 11:252 | Self-reported model identity is an alias echo: E1-E3 reviewer 3 reported `claude-gw-tier4[1m]` while the served model was `gpt-6-luna` | `results.jsonl` self_reports against `results.md:45-47` (slice 11) | UNVERIFIED | n/a | CORE (never trust self-reports, links DR-031 and DR-159) |

**Key Takeaways (slice 11)**
- Slice 11 adds 17 rows (DR-155..DR-171), of which only the `.gitignore:13` row, X-1 and X-7 constants, X-14 and X-16 (as DR-153) were checked against code or tree; the other rows are experiment artifacts I did not open, so they are UNVERIFIED by construction.
- The anchors named in the assignment resolve as follows: `findings.py:29` = DR-007 and DR-061; `telemetry.py:23` = DR-007 (copy); `findings_v2.py:15-22` = DR-001 (shared `_check_flat` import); `cluster_cmd.py:27-34` = DR-153; `.gitignore:13` = DR-155; `tests/review/test_review_ledger.py:376-385` = DR-002 and DR-003 (pin).

## Final de-duplicated register

**How to read it.** The authoritative register is the union of the per-slice row tables above: 171 rows, `DR-001` to `DR-171`, no gaps, every row with all eight columns filled (checked by a read-only script over this file: 171 rows, 0 empty cells, 0 duplicate ids). `DR-090` repeats `DR-017` and is merged into it, so there are 170 distinct defects. Where a later section corrects an earlier row, the correction below wins.

### Counts in and out (open item d)

| Scheme | Ids defined in the slices | Mapped to a DR row |
|---|---|---|
| A: run-2 hand-off (D1-D13, P1-P7, T1-T2, B-1..B-7, H1-H12) | 41 | 41 (DR-001..DR-041) |
| B: run-2 merge notes (D1-D23) | 23 | 23 |
| C: run-2 panel notes (defects 1-19) | 19 | 19 |
| D: run-1 hand-off (D1-D16) | 16 | 16 |
| slice 03 (P1-P10, H1-H19) | 29 | 29 |
| slice 04 (7.1-7.26) | 26 | 26 |
| slice 09 (D-1..D-31) | 31 | 31 |
| slice 10 (D-01..D-25, C-01..C-19, H-01..H-12) | 56 | 46; the 10 ids H-01, H-03, H-04, H-05, H-06, H-07, H-08, H-09, H-10, H-12 are claim checks with no defect (see Gaps) |
| slice 11 (X-1..X-22) | 22 | 22 |
| Total | 263 | 253 mapped (many to the same row), 10 claim checks with no row, 0 silently missing |

Slice 02 also lists 20 defect groups (V-20..V-39) and 13 disagreements (X1-X13); they map onto existing rows as follows: V-20 = DR-001; V-21 = DR-002; V-22 = DR-003; V-23 = DR-006; V-24 = DR-005, DR-007, DR-061; V-25 = DR-004, DR-010; V-26 = DR-009, DR-019; V-27 = DR-011, DR-054; V-28 = DR-053; V-29 = DR-043; V-30 = DR-012, DR-059; V-31 = DR-056, DR-057, DR-058; V-32 = DR-023..DR-027, DR-029; V-33 = DR-014, DR-015, DR-018, DR-020, DR-071, DR-072; V-34 = DR-016, DR-017, DR-064, DR-070; V-35 = DR-021, DR-022; V-36 = DR-042; V-37 = DR-031, DR-032, DR-033, DR-067, DR-068; V-38 = DR-073; V-39 = DR-062, DR-063, DR-065, DR-066. X2 = DR-075, X10 and the T2bModel01 and MODEL-TIERS quote are documentation drifts (no row beyond DR-075).

### Open item (c): one numbering scheme

Use `DR-nnn`. Crosswalk from the other schemes (each cell lists the unified id; scheme A is the run-2 hand-off table, B the run-2 merge notes, C the run-2 panel notes):

| DR | A (hand-off) | B (merge notes) | C (panel notes) | D (run-1 report) | slice 09 | slice 10 / 11 |
|---|---|---|---|---|---|---|
| DR-001 | D1, B-2 | D9 | | D1 | | slice 03 P1, P10 |
| DR-002 | D2 | D1 | | D3 | D-2 | slice 03 P2, P6 |
| DR-003 | D3 | D2 | | D2 | (D-1 case) | |
| DR-004 | D4 | D5 | | D6 | | slice 03 P3; X-17 (DR-168) |
| DR-005 | D5 | D3 | | D6 | D-6 | |
| DR-006 | D6 | D4 | 12 | D5 | D-3 | slice 03 P4 |
| DR-007 | D7 | | 2 | D7 | D-6 | |
| DR-008 | D8 | | 5 | D4 | | |
| DR-009 | D9 | | 6 | | | |
| DR-010 | D10 | D6 | | | D-28 | |
| DR-011 | D11 | D7, D8 | | | | |
| DR-012 | D12 | D11 | | | | |
| DR-013 | D13 | D14 | 13 | | | |
| DR-014 | P1 | | 4 | D11 | D-5 | |
| DR-015 | P2 | | 3 | | | slice 03 P7 |
| DR-016 | P3 | | | | | |
| DR-017 | P4 | | | | | slice 03 P8 (DR-090) |
| DR-018 | P5 | | | D12 | D-29 | |
| DR-019 | P6 | | 6 | | | |
| DR-020 | P7 | | 11 | | D-18 | |
| DR-021 | T1 | | 8 | D15 | D-8 | |
| DR-022 | T2 | | 15 | D15 | D-29 | |
| DR-023 | B-1 | | 1 | D8 | | |
| DR-024 | B-2 | | | | | slice 03 H16 |
| DR-025 | B-3 | | 7 | D9 | | |
| DR-026 | B-4 | | 14 | | | |
| DR-027 | B-5 | | | | | |
| DR-028 | B-6 | | | D10 | | slice 03 H2 |
| DR-029 | B-7 | | | | | |
| DR-030..DR-041 | H1..H12 | | | | | slice 03 H4 = DR-031/030, H5 = DR-041, H6 = DR-040, H7 = DR-037, H8 = DR-036, H9 = DR-083, H10 = DR-038, H11 = DR-035, H13 = DR-034, H14 = DR-033, H15 = DR-039/069, H17 = DR-068 |
| DR-042 | | | | D13 | D-9(a) | |
| DR-043 | | D12, D13 | | D16 | | |
| DR-044 | | | 19 | D14 (second half) | | |
| DR-052..DR-061 | | D10, D15..D23 in order (D10 = DR-052, D15 = DR-053, D16 = DR-054, D17 = DR-055, D18 = DR-056, D19 = DR-057, D20 = DR-058, D21 = DR-059, D22 = DR-060, D23 = DR-061) | | | D-4 = DR-108, D-27 = DR-058 | |
| DR-062, 063, 065, 066, 064 | | | 9, 10, 17, 18, 16 | | | slice 10 D-09 = DR-062 |
| DR-107..DR-127 | | | | | D-1, D-4, D-7, D-9(b), D-10..D-13, D-15..D-17, D-20..D-26, D-30, D-31 | |
| DR-128..DR-154 | | | | | | slice 10 D-01..D-25, C-07, C-19, H-02, H-11; slice 11 X-15, X-16, X-18, X-20 |
| DR-155..DR-171 | | | | | | slice 11 X-1..X-22 (those not above) and `.gitignore:13` |

Run-1 D14 first half ("no tasklist review step exists in the skills") is contradicted by code (slice 01 C2): `sc-workflow-protocol/SKILL.md:89` and `sc-tasklist-protocol/SKILL.md:1621,1630` run `/sc:reflect --mode pre`; this is a wrong claim in a document, not a code defect, so it has no row.

### Corrections to earlier rows (the version here wins)

| Row | Earlier cell | Correct cell |
|---|---|---|
| DR-006 | pinned: none found | pinned as intended: `tests/review/test_review_ledger.py:408` `test_missing_anchor_is_kept_without_a_span`; `tests/review/test_review_findings.py:215-230` (`anchor_status` and `anchor_ambiguous` asserted) |
| DR-007, DR-061 | pinned: none | `tests/review/test_review_findings.py:201-212` asserts lower-case ids are not refs (line 212); no test covers `T01.02` |
| DR-054 | pinned: none | `tests/review/test_review_findings.py:163` `test_fixmap_table_fallback` pins the fallback |
| DR-058 | pinned: none | `tests/review/test_review_findings.py:125` `test_last_of_two_blocks_wins` pins "more than one block, last used" |
| DR-053 | pinned: unverified | deferral is pinned as a feature by `tests/review/test_review_ledger.py:396`; the `PASS PASS` rewrite is not tested |
| DR-080 | `test_review_findings_v2.py` listed in the pinned column | not a pin (that file was not read for this row); pinned: none found |
| DR-090 | separate row | merged into DR-017 |

### Open item (b): tests that pin a defect as intended behaviour

| Defect | Pin (file:line) | Checked |
|---|---|---|
| slice09 D-1 (DR-107) | `tests/review/test_review_ledger.py:193`, `:376` | test names and lines read; behaviour reproduced |
| slice09 D-2 (DR-002) | `test_review_ledger.py:376-385` | read in full |
| slice09 D-3 (DR-006) | `test_review_ledger.py:408`; `test_review_findings.py:215-230` | names and lines |
| slice09 D-5 (DR-014) | `tests/review/test_review_panel.py:204-214`; `test_review_panel_exclusion.py:208` | read in full for the first; name for the second |
| slice09 D-6 (DR-061, DR-007) | `test_review_findings.py:201-212` | line 212 read |
| slice09 D-11 (DR-112) | `test_review_ledger.py:396` (deferral as a feature); reopening untested | name and line |
| slice09 D-25 (DR-123) | `test_review_cluster.py:233-260` | from slice 09 only [UNVERIFIED] |
| slice09 D-26 (DR-124) | `test_review_cluster.py:361-400` | from slice 09 only [UNVERIFIED] |
| also pinned | DR-009 (`test_review_ledger.py:518`), DR-012 (`test_review_cli.py:229,245`), DR-015 (`test_review_panel.py:303-308`), DR-018 (`:331-339`), DR-019 (`:288-291`), DR-079 (`test_review_ledger.py:388`), DR-125 (`test_review_panel.py:331`), DR-126 (`test_review_ledger.py:505`), DR-140 (the test itself) | read |

### Fix owner buckets (computed over the rows; the first word of the owner cell decides)

| Owner | Count | Rows |
|---|---|---|
| CORE | 75 (74 distinct, DR-090 is the repeat of DR-017) | 001-006, 008-025, 027, 029, 042, 043, 052-061, 064, 066, 070-073, 079, 080, 090, 100, 107-121, 123-127, 133, 134, 146, 159, 162, 168, 171 |
| MODULE-reflect | 29 | 062, 063, 122, 128-132, 135-145, 147, 149-152, 156-158, 160, 161 |
| MODULE-tasklist | 2 | 007, 065 |
| MODULE-spec | 2 | 026, 044 |
| HARNESS | 14 | 030-033, 040, 041, 067-069, 081, 082, 088, 154, 155 |
| EVAL | 36 | 034-036, 039, 046-048, 051, 076, 078, 083-086, 089, 091-099, 101-106, 164-167, 169, 170 |
| OPS | 2 | 148, 163 |
| DROP (with reason in the row) | 11 | 028, 037, 038, 045, 049, 050, 074, 075, 077, 087, 153 |

The core must fix, in this order of consequence for a unified design: the verdict and clearing rules (DR-002, 003, 008, 009, 107, 108, 112, 114), the silent drop and anchor family (DR-001, 004, 005, 006, 056-058, 060, 061, 113, 123), the panel resolution family (DR-014, 015, 016, 017, 018, 020, 071, 109, 111, 115, 125), the brief and parser contract (DR-023-027, 029), the persistence and CLI family (DR-011, 012, 013, 043, 053-055, 059, 079, 126), telemetry (DR-021, 022, 110, 116, 117, 127) and the E1 additions (DR-118-121, 124, 146, 159, 162, 168, 171). Rows pinned by a test change a contract, so each needs a deliberate test change.

### Open item (a): reproduction summary

REPRODUCED 64 rows, TRACED 46 rows (read the code, did not execute), 2 rows mixed (DR-093 and DR-102), UNVERIFIED 59 rows, NOT-REPRODUCED 0 rows (counts computed over the Repro column). The one number that did not reproduce is the P1 count (`@live7` 30 of 40 here, slice figure 26 of 40; the run ids behind 26 are not stated), recorded inside DR-014. Scripts used (all read-only, all in `/tmp/review-panel-run2-2.17/`, deleted before return): `repro1.py`, `repro2.py`, `repro3.py`, `repro4.py` (findings, ledger, panel, cluster_cmd behaviours), `batch1.sh`, `batch2.sh` (git reads of the E2 tip), `count.py` (row counts). `git status` after the runs showed only the four paths that were already untracked at session start.

### Open item (e): the two [CODE-CONTRADICTED] claims

1. E2 hand-off "159 functions" of tests (DR-074): the per-file `def test_` column of `handoff-notes/run2/tests-tools.md` sums to 179 (111 in `tests/review`, 68 in `tests/skills`); the stated total is 159 (in the notes' TOTAL row and in `HANDOFF-run1-vs-run2.md:29`, not in the run-2 hand-off itself); the collected column sums to 304, matching the stated 304. Both figures: 159 stated, 179 re-summed. Details in the slice 02 section. [159 is CODE-CONTRADICTED; 179 is arithmetic over the table, the underlying counts were not recounted.]
2. Memory lesson "fenced yaml calibration not parsed by cluster" (DR-153, slice 11 X-16): at HEAD `src/superclaude/cli/review/cluster_cmd.py:27` `_FENCE` matches fenced `yaml`/`yml` blocks and `:31-47` `_embedded_calibration` tries them first, then unfenced `calibration:` blocks (`:28,34`); executed read-only, a fenced card returned `{'F1': 0.8, 'F2': 0.4}`. The file has one commit, `d2d8a2d16` (2026-11-12). The memory file line 64 (`docs/memory/reflect/deviation-patterns-brainstorm-reflect-panel.md:64`) says the opposite. The version of the installed CLI at run time is [UNVERIFIED].

## Gaps and Questions

Not verified or not checkable (each with the search I tried):

1. 59 rows are UNVERIFIED. They rest on E2 artifacts I did not open (audits A, B, C, E, F bodies, `COMBO-REPORT.md` beyond lines 292 and 132, judge JSON, `analysis/extract.py`, `attrib.py`), on E1 experiment artifacts under `.dev/eval-workspaces/shadow-model-combos/` (shadow runs, `results.md`, `runs.jsonl`), and on reflect engine lines in `ensemble.py` I did not re-read (DR-130..DR-132, DR-137, DR-150). Searches tried: `git show` and `git ls-tree` of the E2 tip for the paths I needed; Grep of `src` and `scripts` at HEAD.
2. DR-014 count: 30 of 40 (`@live7`) and 18 of 40 (`@default`) with run ids `run1..run40`; slice 01 and slice 02 report 26 of 40; the run ids behind 26 are unknown [UNVERIFIED].
3. `scripts/reflect_shadow_exit.py` was not re-run: it writes a report to `--out` (`:404-405`) and I did not check the default path, so DR-138, DR-139, DR-147 rest on slice 10's recorded output.
4. Pins for `slice09 D-25` and `D-26` (`test_review_cluster.py:233-260`, `:361-400`) were not opened.
5. The 10 slice 10 claim checks with no defect: H-01 (legacy engine never calls the panel; verified for the Python wrapper by slice 10), H-03 (parity recompute exists), H-04 (lint constants match the skill; test green), H-05 (PR #199 forensic file claims; partly UNVERIFIED), H-06 and H-07 (paths exist), H-08 (default output package not checked), H-09 (sign-off file not opened), H-10 (kernel has no caller outside registration), H-12 (installed path, not in this worktree).
6. Slices 05, 06, 07, 08, 12 are outside this item. `.gitignore:13` (DR-155) is checked at HEAD and at the tip, but the per-harness evidence (r2 `bin/lib/`, r3, r4, r5 detail) is from slices 07 and 08 only; their other defects (for example D-R3-1 and D-R5-1 as numbered there, C-11 sandbox flag) have no row here and need their own owner.
7. The pytest suite was not run (the assignment did not ask for it).
8. Negative evidence (searches that returned nothing): `159` in `HANDOFF-review-panel-unification-run2.md`; `lint_cmd.py` and `estimate_cmd.py` among the 16 files of `cli/review`; `muse-ember` in `review-tiers.default.json`; `checks-gate8` under `tools/tmp-scripts/`; `j1-` in `audit-D/flags.tsv`; any path containing `/lib/` in the E2 collab tree at the tip; `T01.02` in `tests/review`; `t2-engine` in the reflect command file and reflect CLI; `reviewer_briefs_materialized` in `panel_lint.py`; production callers of `channel_of`, `read_committed`, `reusable_stages`, `COMPLETION_STATES`, `V1_FIELDS`, `append_record` (other than the manual CLI).
9. Independence: no content of `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/` or `REVIEW-PANEL-UNIFY-RUN2-QUEUED.md` was read, listed, grepped or cited. Slice 03 (gap 10) records that one of its own greps printed folder names under the run-1 directory; I opened none of those files and cite nothing from them. `.dev/tasks/` was not searched.

Questions for the owner (they decide which rows are bugs and which are contract):
- Is "clear a `resolved_check` row when the reviewer's block was invalid, or when no one re-checked it" (DR-003, DR-107) a bug or a contract? Existing tests pin it.
- Should the core keep drop-and-warn at 200/300/8 (DR-001) or repair, truncate and re-ask? Both parsers share the limits (`findings_v2.py:21`).
- One convergence threshold (0.75 or 0.80, DR-133) and one single-vendor rule (warn or degrade, DR-134)?
- One blocking rule (DR-025, with `findings_v2.py` `reflect_category`)?
- Is strict distinctness the default (DR-014, DR-109)?
- Should `lib/` stay ignored (DR-155) given that three E2 harnesses lost their code?

## Stale Documentation Found

- **[STALE DOC]** E2 hand-offs attribute the `cli/review` changes to #518 (167184c6b); that commit touches 0 files under `cli/review` (DR-045). [CODE-CONTRADICTED]
- **[STALE DOC]** "106 row folders in `combos/`" and "107 entries": the tip tree has 96 directories (DR-047, DR-076). [CODE-CONTRADICTED]
- **[STALE DOC]** "4 verdict flips": audit D lists 3 (DR-048). "Per-model counts are blocking findings lost": they are all dropped findings (DR-046). [CODE-CONTRADICTED]
- **[STALE DOC]** "159 functions" (DR-074). [CODE-CONTRADICTED]
- **[STALE DOC]** `COMBO-REPORT.md:292` "discarded with no error": a first-error warning exists (DR-087). [CODE-CONTRADICTED]
- **[STALE DOC]** `ledger.py:112` docstring "skipped for clearing" (DR-003). `findings.py:322` docstring "Uppercase" for `refs_norm` (DR-061). `cluster.py:35-38` weight-rule docstring (DR-124). `contract.py:403` cite `SKILL.md:754` (DR-143). `cli/reflect/__init__.py:1-15` module list (DR-142). `runner.py:457` comment (DR-144). `refs/reflection-rubric.md:39` class names (DR-136). [CODE-CONTRADICTED]
- **[STALE DOC]** `manifest.md:5` "(local, never pushed)" and the tmp-scripts README `checks-gate8` (DR-078, DR-086). [CODE-CONTRADICTED]
- **[STALE DOC]** Memory file line 64, fenced yaml lesson (DR-153). [CODE-CONTRADICTED]; installed-CLI version [UNVERIFIED]
- **[STALE DOC]** Line numbers in the run-2 hand-off for `panel.py`, `panel_cmd.py` and `review-tiers.default.json` are shifted at HEAD (`panel.py` 525 to 707 lines, `panel_cmd.py` 87 to 129, tiers 32 to 38); the cites for `findings.py`, `ledger.py`, `ledger_cmd.py`, `merge_cmd.py`, `telemetry.py` are exact at HEAD (slice 01 section 4, line counts re-checked: 457 and 494 for the first two). [CODE-VERIFIED]
- **[STALE DOC]** "T2bModel01 not referenced anywhere in src/ or tests/" (DR-075): [UNVERIFIED] here; slice 02 says it is contradicted at the base.

## Summary

The register holds 171 rows (170 distinct) built from slices 01, 02, 03, 04, 09, 10 and 11, covering 263 original ids from nine numbering schemes (253 mapped, 10 claim checks, none lost). I re-verified against HEAD or the E2 tip: 64 rows were reproduced by running read-only snippets or direct commands, 46 traced by reading code, 59 stay UNVERIFIED because their evidence is outside what this item may open. Seventy-five rows belong to the core (parsing and silent drops, the verdict and clearing rules, panel resolution, brief and parser contract, persistence, telemetry), 29 to the reflect module, 4 to the tasklist and spec modules, and the rest to evaluation, harness, ops or are dropped. Of the eight defects the assignment named as test-pinned, six are confirmed pinned by a test I read (D-1, D-2, D-3, D-5, D-6, D-11 partly) and two (D-25, D-26) rest on slice 09 alone; about a dozen more rows are pinned too, so fixing them changes a contract. The two [CODE-CONTRADICTED] claims (159 functions; the fenced yaml lesson) are resolved with both figures and the code line range.

