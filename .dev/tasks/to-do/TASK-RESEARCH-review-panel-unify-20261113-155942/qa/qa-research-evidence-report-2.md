# QA Report — Research Gate (Partition 2 of 2, evidence-quality lens)

**Topic:** Unified Review Panel (E1 reflect Tier 2 panel, E2 tasklist review-panel study, E3 #346 review loop)
**Date:** 2026-11-13
**Phase:** research-gate
**Fix cycle:** N/A
**Lens:** evidence-quality (checklist items 1-4)
**Assigned files:** research/07-reflect-merge-contract.md, 08-run-recording-telemetry.md, 09-consumer-plugpoints.md, 10-future-consumers.md, 11-evaluation-evidence.md, 12-test-pins-regression.md
**Fix authorization:** false (report only)

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file verification requires merging all partition reports.]

---

## Analyst reports

(in progress)

## Re-run command results

| Command (repository root) | Fresh result (2026-11-13) | Research claim | Match |
|---|---|---|---|
| `uv run pytest --collect-only -q tests/review tests/cli/reflect` | `1004 tests collected in 0.81s` | file 12: 651 + 353 = 1004 | yes |
| `uv run pytest --collect-only -qq tests/review` (per-file uniq) | 651, 19 files; every per-file count equals the file 12 §1 table (23/24/13/41/15/5/10/92/119/113/32/15/8/40/32/17/21/14/17) | 651 | yes |
| `uv run pytest --collect-only -qq tests/cli/reflect` (per-file uniq) + `ls tests/cli/reflect/test_*.py \| wc -l` | 353 collected; **38** test files; every per-file count equals the §2 table | 353 collected, **37** files | count yes, file count off by one (see finding 1) |
| `uv run pytest --collect-only -qq` six `tests/skills` files | 178 (5/18/33/14/62/46) | 178 (5/18/33/14/62/46) | yes |
| `uv run python scripts/reflect_shadow_exit.py` | exit 1; `shadow runs counted: 13 of 20`; 1 incomplete (`...-shadow02`, state clustered); MALFORMED 0; EV-1 shadow 8/13 = 0.615 vs legacy 3/39 = 0.077; parity FAILS on shadow04/05/07/08/09/15 (05 and 07 "recorded true but recomputed false"); lint clean on 10/11/12/14; replay vs 42-run legacy baseline: 0 new degraded reasons; Stage 2 counts: 0 2-of-3 shortfalls, 9 unknown executor class, findings-block compliance 0.704 over 9 runs, cluster_agreement min/median/max 1.000; `OVERALL: FAIL (shadow runs 13 of 20)` | see files 07 and 11 sections | see per-file sections |
| Grep `rf-qa\|rf-qa-qualitative\|rf-analyst` over `src/superclaude/skills/` (count mode) | 591 matching lines in 19 files (task-builder 112, readme 98, roadmap 92, tech-research 81, operational-guide 70, tech-reference 51, task 32, prd/SKILL 5, tdd/SKILL 5, prd refs 3+5+9+4, tdd refs 4+9+3+4, sc-reflect-protocol/SKILL 3, sc-reflect-protocol/refs/remediation-handoff 1) | see file 10 section | see file 10 section |

## Per-file verification

### File 12 — `research/12-test-pins-regression.md` (348 lines)

Status: Complete (line 5); `## Summary` present (line 346); `## Gaps and Questions` present (line 322).

Claims re-verified by opening the source:

| # | Claim (file 12 location) | What the source shows | Result |
|---|---|---|---|
| 12-1 | §0: 1182 = 651 + 353 + 178 | fresh collections 651, 353, 178 (table above) | VERIFIED |
| 12-2 | §0/§2: `tests/cli/reflect/` holds 37 test files; "the other 33 predate the panel work" | `ls tests/cli/reflect/test_*.py` = 38; the §2 table itself lists 38 files; 38 - 4 = 34 | WRONG COUNT (minor; the "not 12" correction and the 353/82/271 figures stand) |
| 12-3 | §0: merge-base = `d2d8a2d16`; branch test diff = `test_shadow_skill_contract.py` +42, `test_shadow_exit_script.py` +6/-9 | `git merge-base HEAD origin/master` = d2d8a2d16; `git diff --stat d2d8a2d16 HEAD -- tests/` = +42 and 15 lines changed (48 ins, 9 del total) | VERIFIED |
| 12-4 | §1: `test_review_cli.py` 9 defs before d2d8a2d16, 13 after; live7 has 15 defs before and after | `git show d2d8a2d16~1:...test_review_cli.py \| grep -c '^def test_'` = 9, now 13; live7 15/15 | VERIFIED |
| 12-5 | §3.1: `test_review_ledger.py:376-385` asserts `block_ok == {"t1b-1": True, "t2-1": False}`, truthy warnings, L1 `resolved`; `ledger.py:150-157` raises only when `not any(block_ok.values())`; `ledger.py:254-258` clears `resolved_check` rows with no cluster; docstring `ledger.py:112` | read test :376-385 and ledger.py :107-264: exact | VERIFIED (D2 docstring contradiction confirmed) |
| 12-6 | §3.1/D1: `ledger.py:130-134` keeps only the first error; `:141-149` entry stores only `block_ok` | ledger.py :130-134 `parsed["errors"][0]["msg"]`; :141-149 entry keys reviewer_id/model/report/report_sha256/block_ok | VERIFIED |
| 12-7 | §3.2: `test_review_ledger.py:408-417` asserts `span is None`, `status == "open"`, `blocking is True` | read :408-417: exact | VERIFIED |
| 12-8 | §3.3: `test_review_panel_exclusion.py:208-213` (6 Haiku), `:94-103` with soft `:97-98`, golden test `:56-72` = 16 cases, `:72` asserts no `skipped_slots`/`excluded` | read :50-213: 8 golden keys x `explicit` [False, True] = 16; :72 exact; :213 `count(HAIKU) == 6` | VERIFIED |
| 12-9 | §9/D4: `test_review_ledger.py:129` `brief_ids == ["L1","L2","L4"]`; :136 `cap_reviews == 3` | read :118-137: exact | VERIFIED |
| 12-10 | §6 C1/C6/C14: HEAD-relative (`git()` helper :23-30; C1 :42-49; C6 :52-75 allowed `### 3.1`/`4.3a`/`5.4`/`9.2`, `--t2-engine`; C14 :78-98 `git grep -c`) | read test_shadow_skill_contract.py :20-99: exact | VERIFIED |
| 12-11 | §6 C2: `panel_lint.py:33` STABLE_FIELDS_1_8_0, `:146` TELEMETRY_FIELDS, `:184` LEGAL_MERGE_METHODS = ("adversarial", "single-reviewer-fallback") | Grep: :33, :146, :184 exact | VERIFIED |
| 12-12 | §6 C3: bump message at `panel_lint.py:333` | :333 is the L3 merge_method (EV-2) message; the "B bump rule" message is at `panel_lint.py:361-365` | LINE DRIFT (minor) |
| 12-13 | §7: `test_review_loop_extension.py:120-127` forbids parser/script/state machine/transcript/asynchronous in the Review Loop section | read :120-127: exact | VERIFIED |
| 12-14 | §3.7: `test_review_telemetry.py:327` rejects `stratum="gpt"`; `test_review_cluster.py:784-795` import set `{"refs_norm", "_check_citation"}` | Grep :327 exact; read :784-795 exact | VERIFIED |
| 12-15 | §4 D7: regex at `findings.py:29` and `telemetry.py:23`; §Gaps `_ID_RE` at :24 | findings.py:29 `_REF_TOKEN`; telemetry.py:23 `_ID_TOKEN`, :24 `_ID_RE` | VERIFIED |
| 12-16 | §2: first-add commits of the six skill files (95f2c6e43, 5d9a0ae70, 77e0a7029, 80f934de5, f90aca51a, 9163bd1c7) and dates | `git log --diff-filter=A` for each: exact | VERIFIED |
| 12-17 | §1: fixtures added by d2d8a2d16 | `git diff --stat d2d8a2d16~1 d2d8a2d16 -- tests/review/fixtures` = 9 files, includes frozen tiers and reflect_cards | VERIFIED |

Evidence density: Dense (16 of 17 sampled claims exact; 1 off-by-one file count, 1 line drift). All cited paths exist (opened above). Doc-sourced claims (hand-off §8, scope slice 2) are tagged `[CODE-CONTRADICTED]`/`[STALE DOC]`/`[UNVERIFIED]` in "Gaps and Questions" and "Stale Documentation Found". `findings.py:349-358` is marked "from scope slice 2, not re-read" and listed `[UNVERIFIED]` in Gaps — acceptable.

### File 07 — `research/07-reflect-merge-contract.md` (488 lines)

Status: Complete (line 5); `## Summary` present (line 486); Gaps (457) and Stale Documentation (477) present.

Exit-script comparison: the verbatim output recorded in §5 (lines 191-265) is byte-for-byte the same as the fresh run above (13 of 20, shadow02 incomplete, EV-1 8/13 vs 3/39, the six parity failures, nine lint/manifest problem runs, 42-run replay with 0 new degraded reasons, compliance 0.704, cluster_agreement 1.000, exit 1). The §5.1 reading (3 no-contract runs 04/08/09; EV-1 placement 03/05/06/07; 0 cards on 15; extra keys on 13 and 07; clean runs 10/11/12/14) matches the fresh output.

| # | Claim | What the source shows | Result |
|---|---|---|---|
| 07-1 | SKILL.md is 2033 lines; `--t2-engine` rule and panel reject message at :87 | `wc -l` 2033; :87 text exact | VERIFIED |
| 07-2 | :311 legacy keeps 1.8.0 unchanged ("no stable field, `merge_method` value or contract version changes") | :311 exact | VERIFIED |
| 07-3 | :727 `contract_version: "1.8.0"` with 1.7.x EV-1/EV-2 "no stable-field change" history | :727 exact | VERIFIED |
| 07-4 | :837 EV-2 legal values exactly {adversarial, single-reviewer-fallback}; :895 "Contract version is `v1.8.0`"; :969 `telemetry:` nesting rule; :703 convergence bands 0.75/0.6 | all exact | VERIFIED |
| 07-5 | :1955 testability row encodes only EV-1 branch (a); :1958 names `telemetry memory_status`, a key absent from §9.2 | :1955 and :1958 exact; `grep memory_status` hits only :1958 | VERIFIED |
| 07-6 | `contract.py` (420 lines): `_LOAD_BEARING_BOOL_FIELDS` :47-57 (7 fields); `parse_contract` returns None on YAMLError (:76-79); major != "1" BLOCKED (:187-194); trigger 10 single-reviewer-fallback (:294-296); null-convergence (:298-300); 0.80 floor (:317-326) | read those ranges: exact | VERIFIED |
| 07-7 | `panel_lint.py` (366 lines): `_CARD_FILE` regex :188; `_ev1` branch (a) :271-278; branch (b) demands `single-reviewer-fallback` unconditionally (:290-291) — stricter than SKILL.md:714 | read :186-190, :268-298: exact | VERIFIED ([CODE-CONTRADICTED] tag correct) |
| 07-8 | `reflect_shadow_exit.py` (410 lines): `_yaml_map(...) or {}` :224; no contract → `"ev1_fail": True` (:243) | read :224, :238-244: exact | VERIFIED |
| 07-9 | shadow04 `return-contract.yaml:103` holds `reviewer_models: [claude-gw-tier1b[1m], ...]` (unquoted `[1m]` breaks YAML) | sed :103 exact | VERIFIED |
| 07-10 | shadow09 `adversarial/` holds only `merged-verdict.yaml`; `merge_method: adversarial` "inline Mode-A merge"; `judge_class_collision: true`; `convergence_score: 0.93 # cluster agreement 0.933` | `ls` and grep: exact | VERIFIED |
| 07-11 | §7.2 table: judge_identity and `adversarial_convergence_score` per shadow run; "inline" judge in 6 of 14 (04, 09, 10, 11, 12, 13); convergence 1.0 in 9 of 14 | grep of every `pre-*-shadow*/return-contract.yaml`: all 14 values match; 6 inline; 9 at 1.0 | VERIFIED |
| 07-12 | Installed `sc-adversarial-protocol/SKILL.md` (2991 lines) return contract :436-448 has no `merge_method`, no judge, writes no `merged-verdict.yaml` | read :436-448; `grep -c 'merge_method\|merged-verdict'` = 0 | VERIFIED |
| 07-13 | `refs/reviewer-spec.md:39` hard-codes lens `"reflect-pre"` | :39 contains `lens "reflect-pre"`; only one `reflect-pre` hit in the file | VERIFIED |
| 07-14 | 48 `.dev/reflect/post-*` dirs | `ls -d .dev/reflect/post-* \| wc -l` = 48 | VERIFIED |
| 07-15 | `test_panel_contract_lint.py:184-190` (`merge_method: "panel"` fails L3 + B) and :193-201 (`1.9.0` fails L1) | read :184-201: exact | VERIFIED |
| 07-16 | §4: `tests/cli/reflect/` has 38 `test_*.py` files | `ls` = 38 | VERIFIED (contradicts file 12's 37; file 07 is right) |

Evidence density: Dense (16 of 16 sampled claims exact). Doc-sourced claims (hand-off §5.6, scope slices 03/04, MR decisions) are explicitly marked "context only, not evidence" or `[UNVERIFIED]`; protocol-text claims are labelled "the protocol says". Recommendation-bearing claims re-verified: contract 1.8.0 pins (07-3, 07-4, 12-11), `merge_method` values (07-4, 12-11), the 0.80 floor and major-version gate (07-6), EV-1 lint behaviour (07-7).

### File 08 — `research/08-run-recording-telemetry.md` (487 lines)

Status: Complete (line 5); `## Summary` present (line 485); Gaps (457), Stale Documentation (477) and a doc-claim verification table (§12, line 436) present.

| # | Claim | What the source shows | Result |
|---|---|---|---|
| 08-1 | File sizes: manifest.py 534, manifest_cmd.py 240, telemetry.py 447, telemetry_cmd.py 98, extract.py 193 | `wc -l`: exact | VERIFIED |
| 08-2 | `manifest.py:38` schema `review-panel-manifest/1`; `ENGINES` :51 includes `panel`; `COMPLETIONS` :52; `PER_REVIEWER_STAGES` :53; `PUBLISH_FILES` :54 | sed :38, :51-54: exact | VERIFIED |
| 08-3 | Attempt payload stored only as `payload_sha256` (`manifest.py:353`); a new attempt after `complete` raises Conflict "would add a vote" (:378-381); failed run comes back unchanged on resume (:449-450) | sed :353, :378-381, :449-450: exact | VERIFIED |
| 08-4 | `manifest_cmd._path` :19-20 = `<out>/panel/manifest.json`; save only when not `reused` (:121-122) | exact | VERIFIED |
| 08-5 | D15: `STRATA = ("sonnet", "haiku")` (`telemetry.py:112-115`, owner decision D3); rejection message :267-268; `KINDS` :19 is the review kind; `cost_per_confirmed_tp` uses `tokens_out` only (:371) | exact | VERIFIED |
| 08-6 | `telemetry_cmd.py:12` `DEFAULT_DIR = ".dev/benchmarks/review-telemetry"` | exact | VERIFIED |
| 08-7 | `merge_cmd.py` imports only json, os, click, ledger (:5-10); no telemetry | grep imports: exact | VERIFIED |
| 08-8 | Telemetry callers in `src/superclaude`: only `telemetry.py` and `telemetry_cmd.py` | Grep hits only those two sources (plus their `.pyc`) | VERIFIED |
| 08-9 | E2 `tools/run-reviewer.sh` is 87 lines; served id from top-level `message.model` (:51); meta jq at :58 writes `exp` = `$MODEL`; `EXCLUDE_MODELS` default (:69); fallback line (:75); `MODEL="$NEXT"` and `attempt=0` (:76); `cost.json` jq (:87) | `git show 4a22d742:...` lines: exact | VERIFIED |
| 08-10 | Commit holds 1263 `*.meta.json`, 0 `fallback.log`, 0 `attemptN.json`, 0 `attemptN.meta.json`; only audits A and D have `summary.md` | `git ls-tree -r` counts: 1263/0/0/0; summary files only for A and D | VERIFIED |
| 08-11 | Audit A summary :12 (0 fallback logs, overwrite flaw), :15-16 (5 stale), :22 (59 extra modelUsage, 57 auxiliary tier2 call); audit D :8 (49 dropped blocking), :10 (16 stale), :29 (195 of 1398 chains) | `git show` of both summaries: exact | VERIFIED |
| 08-12 | `audit-A/audit.py:33` uses `fam` before it is assigned in the loop (:38) | `git show` :30-38: `stats[fam]` at :33, `fam = family(row)` at :38 | VERIFIED |
| 08-13 | `cluster.py:422` marks `chained` | :422 `"chained": [...]` | VERIFIED |

Evidence density: Dense (13 of 13 sampled claims exact). Doc-sourced claims are tracked in §12 with explicit `[CODE-VERIFIED]` / `[CODE-CONTRADICTED]` / `[UNVERIFIED]` tags; the untested items (SKILL.md:722 writer, audit-D chain-replay script, `panel_cmd.py` telemetry) are honestly `[UNVERIFIED]`.

### File 09 — `research/09-consumer-plugpoints.md` (294 lines)

Status: Complete (line 5); `## Summary` present (line 292); Gaps (267) and Stale Documentation (284) present.

| # | Claim | What the source shows | Result |
|---|---|---|---|
| 09-1 | `cli/main.py:568` imports `review_group`, `:570` registers it as `review` | sed :568, :570: exact | VERIFIED |
| 09-2 | `review/__init__.py:3-4` docstring "Subcommand modules are optional"; nine names at :19-29 incl. `lint_cmd`, `estimate_cmd`; swallow only when `_exc.name` is that module (:30-35) | sed :3-4, :19-36: exact | VERIFIED |
| 09-3 | origin/master = `d2d8a2d16`; `git diff --stat origin/master HEAD -- src/superclaude/cli/review` is empty | `git rev-parse` d2d8a2d16; diff output 0 lines | VERIFIED |
| 09-4 | `review --help` lists exactly seven commands (cluster, ledger, manifest, merge, panel, telemetry, verify-citations) | fresh `uv run superclaude review --help`: the same seven | VERIFIED |
| 09-5 | No `lint_cmd.py`/`estimate_cmd.py` in the package; they live on `448048aec` (PN2) and `c503587d9` (PN3), both 2026-11-10; `git log -S '"lint_cmd"'` → `9163bd1c7` | `ls` fails for both; `git log -1` titles and dates exact; `-S` oldest hit 9163bd1c7 | VERIFIED |
| 09-6 | `spec-panel.md` 490 lines; `## Review Loop` at :256 with seven bullets :258-264; hard gate :266-268 | `wc -l` 490; sed :256-268: seven numbered bullets then `## Review-loop prompts (hard gate)` | VERIFIED |
| 09-7 | `document_review_loop_prompts.md` 74 lines; placeholders :17-21 (no source placeholder); fallback sentence at :70; installed copy byte-identical | `wc -l` 74; :17-21 five placeholders; :70 sentence exact; `diff -q` identical | VERIFIED |
| 09-8 | `sc-workflow-protocol/SKILL.md:89` reflect pre call; `:93` advisory and read-only | sed :89, :93: exact | VERIFIED |
| 09-9 | `sc-tasklist-protocol/SKILL.md:1630-1635` Stage 10.5 call; `:1646` "ships regardless of verdict"; `:1162` post gate `superclaude reflect run ... --depth deep --fix --no-promote` | sed/grep: exact | VERIFIED |
| 09-10 | `commands/reflect.md:98` `--depth` default `standard`; `design.md` 149 lines, "There is no gate" at :124 | exact | VERIFIED |
| 09-11 | Grep `superclaude review\|review_ledger\|review panel resolve` over skills/commands/core hits only `sc-reflect-protocol/SKILL.md` :338, :340, :345, :347, :349 | Grep: exactly those five lines | VERIFIED |
| 09-12 | `install_user_setup.py:153-179` `install_rules`, "never auto-loaded" at :179 | sed :153, :179: exact | VERIFIED |
| 09-13 | Installed variants: armb 472, diffgate 481, ledger 475, ponytail 483, stoprule 481 lines | `wc -l`: exact | VERIFIED |

Evidence density: Dense (13 of 13 sampled claims exact). Hand-off D13/D14 claims are tagged `[STALE DOC]`/`[CODE-CONTRADICTED]`; the one inference (workflow `Task N` ids vs the ref regex) is labelled "INFERENCE ... not tested".

### File 10 — `research/10-future-consumers.md` (230 lines)

Status: Complete (line 5); `## Summary` present (line 228); Gaps (204) and Stale Documentation (219) present.

Census comparison (re-run Grep `rf-qa|rf-qa-qualitative|rf-analyst` over `src/superclaude/skills/`): 19 files — matches. The Grep tool's count mode and `grep -r ... | wc -l` both give **591 matching lines**; `grep -o ... | wc -l` gives **997 occurrences**. File 10 §3 calls 591 "occurrences" and says the scope slice's 521 "counted matching *lines*, which is consistent"; its Stale Documentation entry repeats "521 is a line count, so both are correct". Both statements are wrong: 591 is the line count, and 521 matches neither the line count (591) nor the occurrence count (997). The "198 lines also contain spawn|..." figure reproduces only with a case-insensitive second filter (`grep -ciE` = 198; case-sensitive = 133). The 39-call-site / 11-file / 28-need-fix census is a manual per-gate reading and does not depend on the 591/521 figures, so no conclusion changes (finding 3, minor).

| # | Claim | What the source shows | Result |
|---|---|---|---|
| 10-1 | `reviewers.py:41` `REVIEWERS = ("augment", "codex")` | exact | VERIFIED |
| 10-2 | `_CATEGORY_TABLE` (`severity_router.py:34-53`) has 18 keys, no `error-handling`; rubric has none either; `auggie-prompts.md:49` lists `error-handling` | 18 key lines; Grep `error-handling` hits only `auggie-prompts.md:49` | VERIFIED |
| 10-3 | `in_diff is False` drop at `severity_router.py:178-189`; step 5 `if deep:` drop at :191-193 | read :178-193: exact | VERIFIED |
| 10-4 | No caller passes `deep=True` (callers `reviewers.py:301`, `fsm.py:447`, `SKILL.md:126,151`, tests) | Grep `remap_severity(`: none passes `deep=`; one extra internal caller `severity_router.py:210` (in `route`) not listed, also without `deep=` | VERIFIED (conclusion holds) |
| 10-5 | `rf-qa.md:41` and `rf-qa-qualitative.md:41` keep "0 issues is suspect"; independent-stance wording at `rf-qa.md:92` / `rf-qa-qualitative.md:91` | Grep "0 issues is suspect" hits both :41 lines; :92 / :91 hold the independent stance | VERIFIED |
| 10-6 | `test_review_prompt_overrides.py:3-7` docstring says "a zero is suspect" wording was removed; `REMOVED_PHRASES` (:140-148) bans only "surfaces zero issues as suspect" | read :3-7, :140-148: exact | VERIFIED ([CODE-CONTRADICTED] tag correct) |
| 10-7 | `task-builder/SKILL.md:1422` reads a `VERDICT:` line | :1422 exact | VERIFIED |
| 10-8 | `task/SKILL.md:203` ≥3 rf-qa + ≥3 rf-qa-qualitative; :254 one fix agent with `fix_authorization: true` | exact | VERIFIED |
| 10-9 | `sc-reflect-protocol/SKILL.md:632-633` rf-qa / rf-qa-qualitative as UC-2 Wave 3B reviewers, `fix_authorization: false` | exact | VERIFIED |
| 10-10 | `rf-analyst.md` has no fix-authorization field | `grep -ci fix.authorization` = 0 | VERIFIED |
| 10-11 | `reflect-reviewer.md:5` read-only tools; `:8` `permissionMode: plan` | exact | VERIFIED |
| 10-12 | `findings_v2.py:36` closed `LENSES`; `findings.py:14-22` SEVERITIES and 6 CATEGORIES; `panel_cmd.py:40-46` `--kind` first/re-review only; `ledger.py:86-90` `_confidence`; `:93-96` `_decision`; `merge_cmd.py:29-35` `--doc` single file | read all ranges: exact | VERIFIED |

Evidence density: Dense (12 of 12 sampled claims exact; the census unit wording is wrong, see finding 3). Rubric/router divergences are explicitly tagged `[UNVERIFIED as a bug]` with the code behaviour `[CODE-VERIFIED]`; doc-sourced scope-slice citations not re-read (X2 axes, X9 fixmap lines) are marked `[UNVERIFIED]` in Gaps 7-8.

### File 11 — `research/11-evaluation-evidence.md` (403 lines)

Status: Complete (line 5); `## Summary` present (line 401); Gaps (354) and Stale Documentation (388) present.

Exit-script comparison: §8 (lines 209-217) records exit code 1 and a condensed set of "key output lines, verbatim". Every value matches the fresh run: 13 of 20, shadow02 incomplete (state clustered), MALFORMED 0, EV-1 8/13 = 0.615 vs 3/39 = 0.077, parity FAILS for 04/05/07/08/09/15 with the same reasons, holds for 03/06/10/11/12/13/14, lint "no contract" for 04/08/09, 15 zero cards, 03/05/06/07 EV-1 placement, 13 and 07 L2 keys, clean 10/11/12/14, 42-run replay with 0 new reasons, 9 unknown executor class, 0.704 compliance, cluster_agreement 1.000, `OVERALL: FAIL (shadow runs 13 of 20)`. The 15 `failure:` lines are not reproduced (see analyst finding 6 assessment below).

| # | Claim | What the source shows | Result |
|---|---|---|---|
| 11-1 | shadow08 `return-contract.yaml:103` = `reviewer_models: [claude-gw-tier1b[1m], claude-gw-tier4[1m], claude-gw-tier1a[1m]]`; only `adversarial/merged-verdict.md` (no `.yaml`) | sed :103 exact; `ls adversarial/` shows `merged-verdict.md`, no `.yaml` | VERIFIED |
| 11-2 | shadow13 `return-contract.yaml:43` `zero_drop_flag: true` | exact | VERIFIED |
| 11-3 | shadow14 `panel/notes.md:4-6`: first-parse 0.0 (0/3), reviewers wrote `## Findings`, orchestrator replaced the heading in all three cards | exact | VERIFIED |
| 11-4 | shadow15 cards saved as `reviewer-cards/reviewer-<N>.md`; contract has no `reviewer_personas`/`reviewer_models` | `ls` = reviewer-1/2/3.md; grep count 0 | VERIFIED |
| 11-5 | Commit times `9874d63fb` 2026-11-13T01:54:25Z, `c2e3347d3` 02:57:12Z; the `9874d63fb` brief line ("never a table") is in all 3 briefs of shadow12-15 and none of 01-11; the `c2e3347d3` line ("exact heading line") is in no run's briefs | `git log` times exact; per-run grep: nt=3 for 12/13/14/15 only, eh=0 everywhere; `git show c2e3347d3` confirms the added phrase is `exact heading line "## Findings block"` | VERIFIED |
| 11-6 | Tier recount: 39 non-shadow `tier_decision.yaml`, `selected_tier: 2` in 38, `1` in 1, `parsed-sparse` in 35; MR:142 says 37 of 38 (34 parsed-sparse); MR:527 is H-A | counts 39/38/1/35; MR = `.dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md`, :142 and :527 exact | VERIFIED (but `MR` is never defined in the file's citation legend, line 8; finding 5, minor) |
| 11-7 | comboA-r1 top-level assistant turns served by `glm-5.3` (150) and `qwen3.8-max` (63) | `jq` over `logs/...comboA-r1.jsonl`: 150 glm-5.3, 63 qwen3.8-max | VERIFIED |
| 11-8 | `combos.json` still says `"status": "designed, not run"`; `base-e8db2fe6` holds 129 files; SSE is 132 lines | grep, `find \| wc -l` = 129, `wc -l` = 132 | VERIFIED |
| 11-9 | E2 `judge-one.sh` (31 lines) passes `\"combo\":\"$C\"` at :21 (judge sees panel name) | `git show 4a22d742:...`: :21 contains it; 31 lines | VERIFIED |
| 11-10 | E2 `final-table.py:24` skips a missing audit file silently; `:44` groups by `meta["expected_model"]`; `three-way.py:4` `exec`s `/tmp/final-table.py` | `git show`: exact | VERIFIED |
| 11-11 | E2 control package `resolution-live7.json` holds Qwen3.8-max and glm-5.3 twice each (7 models) | `git show` + grep: sonnet, Qwen, glm, Qwen, glm, haiku, luna | VERIFIED |
| 11-12 | PR:52 judge cost "9 Opus subagents, 1,034,575 output tokens ... ~139 s"; CR:428 "NOT CONFIRMED" | `git show` PILOT-REPORT :52 and COMBO-REPORT :428 exact | VERIFIED |
| 11-13 | BUNDLE `SNAPSHOT-STATE.txt:3` "No valid-success verdict is implied"; `FINAL-REPORT.md` 259 lines, :75 headline verdict | exact | VERIFIED |

Evidence density: Dense (13 of 13 sampled claims exact). Doc-sourced E2 headline numbers are explicitly tagged `[UNVERIFIED]` against raw `score.json` with the computation path `[CODE-VERIFIED]`; contradicted doc claims are listed under "CODE-CONTRADICTED doc claims".

---

## Scope coverage (item 3)

research-notes EXISTING_FILES (lines 30-69) against the six topics:
- Reflect consumer: SKILL.md §3.1/§4.3a/§9.1/§9.2 (07), `panel_lint.py` and `contract.py` (07), `reflect_verdict_replay.py` and `reflect_shadow_exit.py` (07, 08), `tests/cli/reflect/` (07, 12), `reviewer-spec.md` (07). Covered.
- Shared review CLI files in these topics: `manifest.py`, `manifest_cmd.py`, `telemetry.py`, `telemetry_cmd.py`, `merge_cmd.py` (08); `__init__.py`, `panel_cmd.py` registration (09). Covered.
- E1 evidence: `shadow-standalone-evaluation.md`, `shadow-model-combos/*`, `pre-*-shadow01..15` (07, 08, 11). Covered.
- E2: `manifest.md`, `PILOT-REPORT.md`, `COMBO-REPORT.md` :289+, `combos/SPEC.md`, `run-reviewer.sh`, `judge-one.sh`, `anon-combos.sh`, `final-table.py`, `three-way.py`, audits A and D (08, 11). Covered.
- E3: `spec-panel.md`, `document_review_loop_prompts.md`, installed variants, bundle `SNAPSHOT-STATE.txt`, the six skill-text tests (09, 11, 12). Covered.
- Consumers: workflow, tasklist, brainstorm, design (09); pr-submit refs and code, auggie refs, rf-* agents, rf-* census (10). Covered.

No EXISTING_FILES entry belonging to topics 07-12 is unexamined. Out-of-list file found by the partition-2 cross-validation analyst: `src/superclaude/cli/reflect/ensemble.py` (see analyst assessment, finding 6).

## Analyst reports (verified)

Both partition-2 analyst reports exist (`analyst-completeness-report-2.md`, verdict FAIL with 2 blocking; `analyst-cross-validation-report-2.md`, verdict FAIL with 1 blocking). I re-checked each of their blocking claims against the source:

| Analyst finding | My check | My severity |
|---|---|---|
| Completeness #4 (IMPORTANT): file 10 census rows 7, 17, 25 bundle several gates; row 7 leaves `fix_authorization` "per gate" | `task/SKILL.md:211-217` is a table of three gates (research, synthesis, task-integrity) with different agent mixes; the bundling is real | Defect confirmed. In my lens MINOR: the count moves from 39 to about 43 call sites, but the conclusions (most review call sites need an in-place fix step; lens → consolidate → one fix agent → verify pattern) do not change. The merge rule takes the more severe rating. |
| Completeness #6 (IMPORTANT): file 11 §8 gives a condensed paraphrase, not the full exit-script output | Task item for file 11 (task file line 204) says "use its full output ... record the output and the exit code"; the gate checklist requires the full output for 07 and 11. File 11 omits the 15 `failure:` lines and merges per-run lines | Deviation confirmed. In my lens MINOR: every number matches the fresh run and file 07 holds the verbatim block from the same HEAD `792cf8c52`. The merge rule takes the more severe rating. |
| Cross-validation #1 (IMPORTANT): `cli/reflect/ensemble.py` writes the UC-2 contract and `merge_method` in code; no assigned file examines it | Read `ensemble.py:418-473` and `:722-815`: `merge_method = "adversarial" if reviewer_count >= 2 else "single-reviewer-fallback"` (:773) regardless of whether the adversarial child ran or succeeded (child runs only if no score is supplied and ≥2 workers succeeded, :424; a failed child leaves the deviation flags at clean defaults, :442-471); the contract carries `mode: post` (:797), top-level `adversarial_subrun_status` (:793) and `verification_verified: False` (:814) | **Concur, IMPORTANT (blocking).** It resolves claims that files 07 and 08 left `[UNVERIFIED]` (08 §6/§12 "no Python writer of `return-contract.yaml`"; 07 §3 "whether any producer writes `verification_verified`, `reviewers_verified`, `regression_verified` or `adversarial_subrun_status`") and shows the `merge_method: adversarial` label is set by reviewer count in code on the path the blocking tasklist post gate uses (09 §4.2). File 07's merge-path conclusions (§7.5, Q1, Q8) cover the UC-1 skill path only. |

Non-blocking analyst items I confirmed: 37 vs 38 files (my finding 1), `panel_lint.py:333` vs :361-365 (my finding 2), the 591/521 census mislabel (my finding 3; re-run confirms 521 = matching lines for `rf-qa|rf-qa-qualitative` without `rf-analyst`, so both figures are line counts over different patterns).

---

## Overall Verdict: FAIL

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | File inventory | PASS | All six files exist; each has `**Status:** Complete` (line 5) and a `## Summary` (07:486, 08:485, 09:292, 10:228, 11:401, 12:346) |
| 2 | Evidence density | PASS (with notes) | 84 claims re-verified by opening the cited source (07: 16, 08: 13, 09: 13, 10: 12, 11: 13, 12: 17); all Dense; every cited path opened exists; three re-runs match (collect-only 1004 = 651 + 353; exit script byte-identical to file 07; census 19 files). Minor count/label/line drifts only (findings 1-5) |
| 3 | Scope coverage | PASS | Every EXISTING_FILES entry for topics 07-12 is examined (section above). `ensemble.py` is not in EXISTING_FILES; it is handled under item 6 |
| 4 | Documentation cross-validation | PASS | Doc-sourced claims are tagged in all six files (07 "context only" + Gaps; 08 §12 table; 09 Stale Doc; 10 `[UNVERIFIED as a bug]`; 11 CR/PR numbers `[UNVERIFIED]` against raw data; 12 hand-off counts `[CODE-CONTRADICTED]`). Recommendation-bearing `[CODE-VERIFIED]` claims re-verified: contract 1.8.0 pins (07-3, 07-4, 12-11), `merge_method` values (07-4, 12-11), 0.80 floor and major-version gate (07-6), telemetry strata (08-5), CLI loader names (09-2, 09-4, 09-5), PR severity router rows (10-2, 10-3, 10-4) — all exact |
| 5 | Contradiction resolution | PASS (notes) | 07 (38 files) vs 12 (37): code says 38 (finding 1). 07 §5.1 attributes shadow15's failure to fixed skill text; 11 §8 shows shadow15 ran after `9874d63fb` — 11 is right (verified brief-line grep) |
| 6 | Gap severity | FAIL | One IMPORTANT gap, verified in code: the UC-2 Python contract writer `ensemble.py` (finding 6) |
| 7 | Depth appropriateness | PASS | Deep: end-to-end traces present (07 §5-7 merge path from SKILL text to lint to recorded runs; 08 §1-11 run record across three efforts) |
| 8 | Integration point coverage | PASS (notes) | 09 maps every consumer plug point; the UC-2 wrapper contract writer is the missing integration point (finding 6) |
| 9 | Pattern documentation | PASS | Patterns documented (10 §3 lens → consolidate → fix → verify; 08 §11.3 run record design; 11 §1 runner pattern) |
| 10 | Incremental writing compliance | PASS | Files carry per-section Key Takeaways, scope inputs, and later additions (e.g. 07 §0 scope inputs; 11 §8 timeline added on top of S04) |

## Summary

- Checks passed: 9 / 10
- Checks failed: 1 (item 6, via finding 6)
- Critical issues: 0
- Important issues: 1 (finding 6)
- Minor issues: 5 (findings 1-5), plus analyst completeness #4 and #6 graded MINOR in my lens
- Issues fixed in-place: 0 (fix_authorization: false)

## Findings

| # | Severity | File | Claim | What the source shows | Fix |
|---|---|---|---|---|---|
| 1 | MINOR | 12-test-pins-regression.md:19, :23, :72, :277, :327, :348 | `tests/cli/reflect/` holds 37 test files; "the other 33" predate the panel | `ls tests/cli/reflect/test_*.py` = 38; collect-only draws from 38 files; the file's own §2 table lists 38; file 07:139 says 38. Collected counts 353/82/271 are correct | Change 37 → 38 and 33 → 34 |
| 2 | MINOR | 12-test-pins-regression.md:230 (C3 row) | Bump-rule message at `panel_lint.py:333` | :333 is the L3 merge_method message; the "B bump rule" text is at `panel_lint.py:361-365` (file 07 cites :360-365 correctly) | Cite `panel_lint.py:360-365` |
| 3 | MINOR | 10-future-consumers.md:78 and :225 | "19 files and 591 occurrences (the scope slice's 521 counted matching lines, which is consistent)" | 591 is the matching-line count (`grep -r ... \| wc -l`); occurrences are 997; 521 is the line count for `rf-qa\|rf-qa-qualitative` without `rf-analyst`. The 39-site census is manual and unaffected | Say "591 matching lines (997 occurrences); slice 05's 521 omits `rf-analyst`" |
| 4 | MINOR | 10-future-consumers.md:78 | "198 lines also contain spawn\|subagent_type\|Agent tool\|launch\|dispatch" | Reproduces only case-insensitively (`grep -ci` = 198; case-sensitive = 133) | State the match was case-insensitive |
| 5 | MINOR | 11-evaluation-evidence.md:8 (citation legend) and §12 (:331-345) | Cites `MR:142`, `MR:527`, `MR:556` | `MR` is never defined in the file; it is `.dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md` (:142 and :527 verified exact) | Add `MR` = that path to the citation legend |
| 6 | IMPORTANT | 07-reflect-merge-contract.md §3 (:128), §7.5, Gaps :469; 08-run-recording-telemetry.md §6 (:190), §12 (:445), Gaps 15 | Contract writer and the producer of `verification_verified` / `reviewers_verified` / `regression_verified` / `adversarial_subrun_status` left `[UNVERIFIED]`; "no Python writer of `return-contract.yaml`"; merge-path conclusions drawn from the skill (UC-1) path only | `src/superclaude/cli/reflect/ensemble.py:722-815` `build_reflect_contract` writes the UC-2 contract (`mode: post`, :797) used by `superclaude reflect run`, the blocking tasklist post gate's path (09 §4.2, `sc-tasklist-protocol/SKILL.md:1162`). It sets `merge_method = "adversarial"` whenever ≥2 reviewers succeeded (:773), even when the adversarial child failed or never ran (:424, :436-471), writes `adversarial_subrun_status` (:793) and `verification_verified: False` (:814) at top level. Same finding as analyst cross-validation #1 | Add a short section to file 07 (and a cross-reference in 08) reading `ensemble.py` `run`/`build_reflect_contract`: who writes the UC-2 contract, how `merge_method` is set, how a failed child routes (null convergence → DEGRADE in `contract.py:298-300`), and restate the merge-path and EV-1 self-attestation conclusions for both UC-1 and UC-2 |

Analyst-report items not repeated as my findings: completeness #4 (census row granularity) and #6 (file 11 condensed exit output) are confirmed defects that I grade MINOR in the evidence lens (see Analyst reports section); the partition merge takes the more severe rating.

## Confidence Gate

- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 40 | Grep: 9 | Glob: 0 | Bash: 21
- Web research: none performed (no claim in scope required an external lookup).
- UNCHECKED items: none. UNVERIFIABLE items: none.
- Claims re-verified: 84 (listed per file above). Re-run commands: collect-only (1004; per-area 651/353/178), exit script (exit 1, output identical to file 07 §5), rf-* census Grep (591 lines / 19 files).

## Recommendations

- Resolve finding 6 before synthesis: add the `ensemble.py` UC-2 contract-writer trace to file 07 (cross-referenced from 08), so the merge-path and target-architecture sections cover both reflect paths.
- Apply the minor corrections (findings 1-5) in the same fix pass if convenient; they are notes and are not rechecked.

## Verdict

**FAIL** — 1 blocking finding (finding 6, IMPORTANT: the UC-2 Python contract writer `cli/reflect/ensemble.py` is unexamined, leaving the merge-path conclusions UC-1-only); 5 MINOR notes.

## QA Complete

