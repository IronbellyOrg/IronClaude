# Research: Evaluation harnesses and evidence

**Investigation type:** Pattern Investigator + Doc Analyst
**Scope:** E2 (`git show 4a22d742:.dev/eval-workspaces/tasklist-review-panel/20261111-a1/...`: tools/run-reviewer.sh, tools/tmp-scripts/{judge-one.sh,anon-combos.sh,README.md}, analysis/{final-table.py,three-way.py}, COMBO-REPORT.md, PILOT-REPORT.md, combos/SPEC.md, manifest.md, one package's ground-truth.json + resolution-*.json); E1 (`.dev/tasks/done/TASK-WF-implementStages0-20261111-202912/artifacts/shadow-standalone-evaluation.md`, `.dev/reflect/pre-*-shadow*`, `.dev/eval-workspaces/shadow-model-combos/{PLAN.md,FINDINGS.md,results.md,combos.json}`, `scripts/reflect_shadow_exit.py` output, untracked `runs/pre-TASK-WF-designSpec-20261107-075614-comboC-r3/artifacts/base-e8db2fe6/`); E3 (`.dev/experiments/346-validation/phase5/final-bundle/`)
**Status:** Complete
**Date:** 2026-11-13

**Citation form.** `E2:<path>:<line>` = `git show 4a22d74213f93837d00c2c314075dd967b9a98e3:.dev/eval-workspaces/tasklist-review-panel/20261111-a1/<path>` at that line (`cat -n` numbering). `CR` = E2 `COMBO-REPORT.md`, `PR` = E2 `PILOT-REPORT.md`, `SPEC` = E2 `combos/SPEC.md`. `HO` = `research/scope/00-handoff-copy.md`; `S01`/`S04` = scope slices `research/scope/01-other-branch-study.md` and `04-this-session-artifacts.md`. `SSE` = `.dev/tasks/done/TASK-WF-implementStages0-20261111-202912/artifacts/shadow-standalone-evaluation.md`. `COMBO` = `.dev/eval-workspaces/shadow-model-combos/`. `BUNDLE` = `.dev/experiments/346-validation/phase5/final-bundle/`. Every source file was read in this session on 2026-11-13 unless marked otherwise.

---

## 1. E2 harness: the single-reviewer runner (`tools/run-reviewer.sh`, 87 lines) [E2]

What it is: a bash script that runs ONE reviewer for ONE package in a fresh `claude -p` session. Usage `run-reviewer.sh <EVAL abs> <pkg id> <reviewer_id> <model> [subdir]` (E2:tools/run-reviewer.sh:2, :5-6).

Data flow (all at E2:tools/run-reviewer.sh):

1. **Input in.** Candidate copied to a fixed sandbox path `/tmp/evalsb/cand/$PKG/candidate.md` (:7-8). `source.md` is pulled from a hard-coded path in ANOTHER worktree, `/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/tasks/done/$PKG/source.md` (:10), and copied next to the candidate only if it exists (:11; the trailing `|| true` makes a missing source silent). [CODE-VERIFIED]
2. **Brief.** `BRIEF` (:13-17) = `/sc:spec-panel @$CAND_SB --mode critique` plus review-1-of-3 rules, the blocking "grading check" sentence, the findings-v1 block format (id, severity, blocking, category list incl. `unpassable-check`, anchor 12-200 chars, anchor2, refs, claim) and a final `verdict:` line. The brief names only the candidate path and its sha256, never `source.md` [CODE-VERIFIED, :13-17; this is HO D8]. It tells the reviewer to read `~/.claude/rules/prompts/document_review_loop_prompts.md` first (:17), so the brief depends on an installed file outside the eval tree.
3. **Dispatch.** `( cd /tmp/evalsb/repo && timeout 3000 claude -p --model "$MODEL" --output-format json --no-session-persistence --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit <<<"$BRIEF" )` (:48). Bash is not denied and permission mode is bypass [CODE-VERIFIED]; the "read-only reviewer" property rests on the after-the-fact audit C (CR:373, per S01 H23), not on the runner.
4. **Per-attempt checks** (`run_attempt`, :45-60): result text extracted from the JSON transcript (:50); observed model = unique top-level assistant `message.model`, subagent turns excluded via `parent_tool_use_id==null` (:51); `MODEL_OK` if observed equals requested case-insensitively or equals `<requested>-build`, and is not empty or `<synthetic>` (:55-56); `BLOCK_OK` only greps for a line starting with ```` ```findings-v1 ```` (:57) and does NOT validate the lines; `APIERR` if the result text contains `API Error` (:54). Writes `<rid>.attempt<N>.meta.json` with `expected_model, observed_model, model_ok, findings_block, attempt, wall_s, output_tokens_main, output_tokens_all, exit` (:58).
5. **Retry and fallback.** Two attempts on the requested model (:61-64). If still not ok and `NOFALLBACK` is unset, walk a hard-coded associative-array ladder `FALLBACK[...]` (:23-43) with guards added 2026-11-12: `EXCLUDE_MODELS` default `"glm-5.3 Qwen3.8-max"` (:69) and never-revisit (:70-71); each hop logged to `<rid>.fallback.log` (:75). After a hop `MODEL="$NEXT"` (:76), so the next `meta.json` records the fallback model as `expected_model` (:58) [CODE-VERIFIED]. The originally requested model survives only in `fallback.log`; `MODEL_LADDER` (:44, :76) is never written to disk.
6. **Output.** Final = last attempt copied to `<rid>.md` and `<rid>.meta.json` (:85); `<rid>.cost.json` = attempt count, total wall seconds, total output tokens summed over every `attempt*.meta.json` (:87).

Design decisions: fresh session per reviewer; identity observed from the transcript, not self-reported; retry before switching model; cost summed over all attempts.

Edge cases and defects found in the source:
- `expected_model` is overwritten by the fallback (:58 with :76), and E2's own `analysis/final-table.py:44` groups panels by `meta["expected_model"]`. So a run that fell back is counted under the fallback model, not the panel it was launched for [CODE-VERIFIED, both lines read]. HO 2.5 says wrong-model rows were quarantined and rerun; whether every fallback row was removed before the final tables is [UNVERIFIED].
- The cost glob `"$OUT/$RID".attempt*.meta.json` (:87) also sums stale attempt files from an earlier launch of the same id (S01 2.2 cites audit-A/summary.md:15: stale attempt files affected 5 runs).
- `BLOCK_OK` is a fence grep only (:57); invalid lines are dropped later by the product merge (HO D1) and the runner cannot see that loss.
- `--output-format json` stores whole transcripts; these `*.attemptN.json` files are the 1.48 GB left uncommitted (HO 1.4).

Portability (question 1): hard-coded `/tmp/evalsb/repo` and `/tmp/evalsb/cand` (:7, :48), the other worktree's absolute path (:10), the `/sc:spec-panel` command and tasklist review text (:13-17), gateway model ids and tier order (:31-43), positional args and `reviews/<subdir>` layout (:6). The sandbox repo `/tmp/evalsb/repo` is built outside this script (see section 5, `manifest.md`).

Key Takeaways
- [E2] The runner pattern (fresh session, observed identity, block gate, retry, guarded fallback, cost over attempts) is reusable; the script is not portable (5 hard-coded path or model groups).
- [E2] Two latent data defects: `expected_model` overwritten on fallback (and used by `final-table.py:44` for grouping), and the cost sum over a glob of attempt files.
- [E1][E2] Bash is not denied under `bypassPermissions`; a unified runner must deny writes mechanically, as reflect intends with the `reflect-reviewer` tool allowlist (reflect side not re-read here, [UNVERIFIED] in this file).

---

## 2. E2 harness: blind judge and anonymisation (`tools/tmp-scripts/judge-one.sh` 31 lines; `anon-combos.sh` 28 lines; `README.md` 7 lines) [E2]

**Anonymiser** (E2:tools/tmp-scripts/anon-combos.sh):
- Hard-coded `EVAL` absolute path into the other worktree (:4), the 3 package ids (:5) and a fixed list of 13 combo rows (`c1..c4`, `r1..r4`, `n1..n5`, :6). This copy covers only those rows; later batches used other `anon-*.sh` scripts (not read, [UNVERIFIED]).
- For each `combos/<C>/<P>/merged-1.md` (:9): pick a random unused label Q..V (:14), write `label-key.json` mapping label to combo (:16) in `<C>/<P>/`, outside the judge folder `<C>/<P>/<L>/` (:11, :15).
- Reviewer ids matching `\bt[0-9a-z]+-[0-9]+\b` become `R1..Rn` (:17, :19-23); the EVAL path becomes `<EVAL>` (:18); candidate and report paths are redacted (:24-25).
- Not anonymised: the combo name stays in the judge folder path `arms/scoring/combos/<C>/<P>/<L>` (:11, :15), which the judge brief names (judge-one.sh:6, :16). Model names inside the merged report body (if any) are not scrubbed; whether `merged-1.md` contains them is [UNVERIFIED].

**Blind judge** (E2:tools/tmp-scripts/judge-one.sh):
- Inputs: `ground-truth.json` (:8), `candidate.md` (:9), `merged-anon.md` (:10). No `source.md` [CODE-VERIFIED, :12-16].
- Brief (:12-23): "Do not read anything outside the files named here" (:12); per GT item: covered at any severity, and covered by a BLOCKING ledger row (:19); blocking rows with no GT match counted as `wrong_blockers` (:20); output `score.json` with `label, combo, package, gt_total, gt_covered_any[], gt_covered_blocking[], ledger_rows_total, ledger_rows_blocking, blocking_rows_gt_matched, wrong_blockers, notes` (:21).
- **The judge is told the combo name**: the required schema literally contains `\"combo\":\"$C\"` (:21), and combo names encode models (e.g. `r2-haiku2-grok`, anon-combos.sh:6). [CODE-VERIFIED] So "blind" means blind to reviewer ids, not to panel identity. HO 3 lesson 1 and CR:296 (audit E re-judge 12/12) do not mention this.
- Dispatch: `timeout 900 claude -p --model claude-opus-5-5 --output-format json --no-session-persistence --permission-mode bypassPermissions` (:25-27), no tool deny list. Skip if `score.json` exists (:7). Failure only on non-zero exit or unparsable `judge.json` (:28-29); a judge that exits 0 without writing `score.json` is logged `OK` (:31), and the aggregator then skips that row-package silently (`final-table.py:48` `if sf:`).
- "Real blocking" is not judged: the GT field `blocking_in_implement` is listed (:14) but only judge-blocking is asked (:19); real blocking is computed afterwards at `final-table.py:34` (`rb = [g for g in jb if GT[p].get(g)]`) [CODE-VERIFIED].

**README** (E2:tools/tmp-scripts/README.md): copied 2026-11-13 from `/tmp`; "many hard-code /tmp paths ... read before re-running" (:4); lists `checks-gate8` as a key script (:7) though it was not copied (S01 H29) — **[STALE DOC]** README.md:7.

Key Takeaways
- [E2] Judge is blind to reviewer ids but NOT to panel name (`judge-one.sh:21`, path at :6). A reusable benchmark must pass an opaque label only and keep `label-key.json` out of reach.
- [E2] Judge has no tool restrictions and no `source.md`; real blocking is a post-computation.
- [E2] A judge that exits 0 without `score.json` is silently dropped from tables.

---

## 3. E2 aggregation: `analysis/final-table.py` (83 lines) and `analysis/three-way.py` (63 lines) [E2]

**final-table.py** (E2:analysis/final-table.py):
- Hard-coded root `E=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/...` (:7), package ids (:8), short model names `SH` (:10).
- `valid(row)` (:11-13) decides "valid era" by **row-name pattern** (`-src` suffix, `b4-` prefix, `-ember` suffix, `e/g/h<digit>` prefix, two named rows; excluding `contaminated|superseded|quarantine|invalid` and `i1-`/`i2-`). Era membership is not derived from timestamps or from whether `source.md` was shipped; it depends on naming discipline [CODE-VERIFIED].
- Ground truth loaded as `{id: blocking_in_implement}` per package (:14).
- Audit exclusions read from `/tmp/audit-{A,B,D,E,F}/flags.tsv` (:22-23); **a missing file is skipped silently** (`if not os.path.exists(f): continue`, :24). On another machine the AUDIT-CLEAN view equals AS-SCORED with no warning [CODE-VERIFIED]. Checks counted as exclusions: B incomplete/short, D blockok/conserve/dropped-blocking/path/stale, F completeness; every A and E flag (:20).
- Per row-package metrics (:31-37): `any`, `jb` (judge blocking), `rb` (real blocking), `wb` (wrong blockers), tokens summed from `t*.cost.json`, reviewer-seconds `rs`, elapsed `el` = max reviewer wall (parallel assumption).
- Panel identity = sorted multiset of `expected_model` from designSpec `meta.json` files (:42-44) — the field the runner overwrites on fallback (section 1).
- Family stats (:50-67): means summed over the two defect-rich packages ("Found /14", "Real blocking /8"); control mean separate; `sd_any` computed (:65) but never printed (dead). Table sorted by found then real blocking (:71); columns include found and real-blocking per 100k tokens (:74).
- Writes `/tmp/final-table.md`, `/tmp/final-clean.json`, `/tmp/final-all.json` (:80-82) — outputs go to `/tmp`, not the repo; the committed `analysis/final-table.md` (59 lines per S01) is a manual copy [inference from :80; how it was copied is UNVERIFIED].

**three-way.py** (E2:analysis/three-way.py):
- `exec(open("/tmp/final-table.py").read().split("rows = {}")[0])` (:4): imports helpers by executing the first half of a `/tmp` copy of `final-table.py` as text. It cannot run from the commit without first copying `final-table.py` to `/tmp` [CODE-VERIFIED].
- Hard-coded families by row names (:5-10): sonnet+2x luna (6 rows), ember+2x luna (6 rows), sonnet+luna+ember (5 rows), sonnet+2x luna+2x ember h2 (4 rows).
- A run counts only if all 3 packages are scored (:16).
- Two-sided permutation test on run-level means, 20,000 shuffles, seed 1 (:33-38), for 4 pairs x 7 metrics (:41-44) = 28 p-values printed, no multiple-comparison correction [CODE-VERIFIED].
- Reviewer-level counts of dropped findings and source-blind runs read `/tmp/audit-C/flags.tsv` and `/tmp/audit-D/flags.tsv` (:48, :52) with no existence check (would crash if missing).

Repo-portability changes needed (question 1): (a) replace absolute and `/tmp` paths with arguments; (b) store era as data (a run manifest field such as `source_shipped: true` plus timestamp) not row-name regex; (c) record intended panel separately from served model; (d) commit the audit `flags.tsv` files next to the analysis or fail loudly if absent; (e) make `three-way.py` import a module, not `exec` a `/tmp` file; (f) multiple-comparison note or correction.

Key Takeaways
- [E2] Both analysis scripts depend on `/tmp` state (`/tmp/audit-*/flags.tsv`, `/tmp/final-table.py`); `final-table.py` silently drops the audit-clean filter when the files are missing.
- [E2] Valid era and panel identity are inferred from row names and the overwritable `expected_model`; a benchmark must record both as data.
- [E2] The permutation test (20,000 shuffles, run-level) is the reusable piece; 28 uncorrected p-values per run of `three-way.py`.

---

## 4. E2 benchmark data: ground truth, resolution files, manifest (control package `TASK-WF-design-20261108-041415`) [E2][E3]

Package tree (`git ls-tree`): `candidate.md`, `ground-truth-draft.json`, `ground-truth.json`, `resolution-default.json`, `resolution-live7.json`, `reviews/`, `reviews-failed-launch-1/`. No `source.md` [CODE-VERIFIED].

**Ground-truth format** (E2:TASK-WF-design-20261108-041415/ground-truth.json:1-48):
- Top keys `package` (:2), `items` (:3), `dropped` (:35, empty here), `verification` (:36-47).
- Item keys: `id` (`GT1`), `class` (`missing-task` :6, `ambiguity` :22), `plan_quote` (verbatim plan text, :7, :23), `description` (what went wrong in implement, :8, :24), `evidence[]` (file:line into `.dev/tasks/done/<pkg>/...` implement artifacts and one `src/` file, :9-16, :25-30), `cost` (`human_acceptance`, :17, :31), `blocking_in_implement` (false for both control items, :18, :32).
- `verification[]`: per item `quote_grep_count` (1) and `evidence_ok` (true) (:37-46) — an integrity check that the quote really occurs once in the candidate.
- Evidence paths point into `.dev/tasks/done/TASK-WF-design-20261108-041415/...` (e.g. :10-15). Those folders are the implement history the sandbox removes (`manifest.md:10`). Whether they exist on master or this branch is [UNVERIFIED] (not checked).
- The format is target-neutral in shape (quote + description + evidence + blocking flag); the `class` values and the evidence source (implement artifacts) are tasklist-specific.

**Resolution files reuse the product resolver output** [E2][E3]:
- `resolution-live7.json` top keys: `environment, review_kind, reviewers, run_id, schema, template_id, template_sha256, template_version, tiers_sha256, tiers_version` (jq); `schema: "review-panel-resolution/1"` (:128), `run_id: "TASK-WF-design-20261108-041415"` (:127), `environment: "gateway"` (:2).
- Per reviewer: `alias, fallback_depth, fallbacks[], launch, model, model_name, reviewer_id, seed, slot_id, stand_in, strategy, tier` (e.g. :5-21).
- The 7 resolved models for this package are `claude-sonnet-5-5, Qwen3.8-max, glm-5.3, Qwen3.8-max, glm-5.3, claude-haiku-5-5, gpt-6-luna` (jq) — **Qwen3.8-max and glm-5.3 each appear twice** in one `@live7` panel [CODE-VERIFIED in data]. This is concrete evidence for HO D11 (`distinct_across_slots` silently allows duplicates when the pool is exhausted), which HO marks "not observed in the eval". It was observed in the eval's own resolution input, but the eval later chose models by hand, so it did not affect scores.
- `resolution-default.json`: 4 reviewers, `claude-sonnet-5-5, Qwen3.8-max, glm-5.3, glm-5.3` (jq) — again a duplicate (glm twice).
- Fallback lists here (`fallbacks`, e.g. :8-11, :25-31) are the product tier file's data; E2's runner ignored them and used its own bash ladder (section 1). So E2 kept two fallback ladders, one unused.

**Manifest** (E2:manifest.md:1-16): EVAL dated 2026-11-11 (:4); base `HEAD == origin/master == ec259f1b` (:6-8); `T2bModel01=gpt-6.1-terra; @live7 resolves 7 reviewers` (:9); sandbox `/tmp/evalsb/repo` = git archive of HEAD without `.dev/tasks/done`, `.dev/eval-workspaces`, `.dev/research` "so reviewers cannot read implement history or ground truth" (:10); dispatch by raw gateway id, "Tier aliases serve only the first model of a tier, so they are NOT used" (:11); GT sha256 hashes for the 3 packages (:14-16). "local, never pushed" (:5) is **[STALE DOC]** (branch is on origin now, S01 H37).

Key Takeaways
- [E2] Ground truth = defects observed in real implement runs, with a verbatim plan quote, evidence file:line and `blocking_in_implement`; a `verification` block checks the quote. Reusable shape; class list and evidence source are tasklist-specific.
- [E2][E3] E2's resolution inputs are product `review-panel-resolution/1` files; the `@live7` and `@default` resolutions for the control package both contain duplicate models (data evidence for HO D11).
- [E2] The GT sha256 hashes in `manifest.md` make the benchmark tamper-evident; the sandbox exclusion list is the leakage guard.

---

## 5. E2 pilot report (`PILOT-REPORT.md`, 83 lines; dated 2026-11-11, pre-`source.md` era) [E2]

- Setup (PR:7-14): 3 packages (designSpec 10 GT/5 blocking, alias 4/3, control 2/0); arms cut from the same reviewer runs: A = sonnet alone, B = @default minus Qwen, C = @live7 minus Qwen (PR:8-11). Qwen3.8-max disqualified after 3 of 3 slots timed out, 3000 s each, 9000 s wasted (PR:12). 9 `.catfix.md` copies fixed the `unpassable-ac` label (PR:13). 9 blind Opus judges, labels X/Y/Z (PR:14).
- Totals (PR:46-50): A 2/16 any, 0/8 blocking recall, 93,098 tokens, 2.15 catches per 100k; B 3/16, 0/8, 394,305 tokens, 0.76; C 4/16, 0/8, 604,096 tokens, 0.66; wrong blockers 0/1/3.
- **Judge cost**: "9 Opus subagents, 1,034,575 output tokens total, ~139 s summed wall" (PR:52) = about 115k output tokens per scoring (1,034,575 / 9 = 114,953) [doc-sourced number; the judge code path is `judge-one.sh:25` CODE-VERIFIED, but the token count is only in the report, so the number is [UNVERIFIED] against raw `judge.json`, which is uncommitted]. Note "9 Opus subagents" (PR:14, :52) vs the later `claude -p` judge script; the pilot judges may have been in-session subagents, which would explain ~139 s summed wall for 1M tokens (implausibly fast for 9 separate 115k-token generations). Which dispatch the pilot used is [UNVERIFIED].
- Judge cost exceeded the reviewer tokens of the largest arm (1,034,575 vs 604,096; PR:50, :52).
- Fixed rule (PR:56): recommend a panel only if it catches >= 2x arm A on defect-rich packages AND <= 1 wrong blocker per control plan. Only C passes, by one defect (PR:58, :61).
- Honest read (PR:71): all arms 0/8 real blocking recall; "Single-reviewer Arm A passed both defect-rich packages — the worst observed outcome for a gate whose job is to fail bad plans."
- Stated limits (PR:75-79): n=3 packages; one judge pass, variance unmeasured; Qwen removal; novel true defects score as wrong blockers (structural bias).
- Paired comparisons (PR:65-67): sign tests p=0.5 and 0.25; B costs 4.2x A tokens, C 6.5x.

Key Takeaways
- [E2] Pilot (n=3 packages, 2026-11-11, before `source.md` was shipped): bigger panels caught 1-2 more non-blocking defects at 4.2-6.5x tokens; 0/8 real blocking for all arms; sonnet alone passed both defect-rich plans.
- [E2] Judge scoring cost ~115k output tokens per (package, arm) in the pilot — more than the reviewers it scored. A judge-based regression run over 3 packages x 1 panel costs about 345k judge tokens.
- [E2] The pilot is the only part of E2 with a pre-registered decision rule (PR:56).

---

## 6. E2 headline results (`COMBO-REPORT.md` 289-506 and `combos/SPEC.md` 1-152; model behaviour dated 2026-11-11 to 2026-11-13, one gateway) [E2]

All numbers below are doc-sourced from E2 reports (aggregated from `score.json`/`cost.json` files I did not re-read). They are tagged [UNVERIFIED] against raw data; the computation path (`final-table.py`, `three-way.py`) is [CODE-VERIFIED] in section 3.

**Scale and era.** "FINAL RESULTS AND DECISION (2026-11-13) - supersedes every earlier table" (CR:289). 71 valid-era rows, 213 row-packages (CR:290, :301); 69 row-packages carry an audit EXCLUDE flag (CR:301), "about a third of the data" (CR:361). All-sets census: 106 scored runs in 62 sets incl. 3 pilot arms; batch 10 dropped (CR:431). `source.md` first shipped 2026-11-12 12:59:34; first valid-era run 13:02:27 (CR:373). 106 runs = 76 source-era + 30 pre-source (ALL vs ALL-src rows, CR:497-498).

**Ceiling: about 1.6-2.5 of 14 per run.** Replicated panels (4-6 runs per package) score 1.60-2.50 found /14 AS SCORED (CR:315-333): ember + sonnet 2.50 (n=4), ember + luna 2.25 (n=4), haiku + 2x luna 2.20 (n=5), ember + 2x luna 1.83 (n=6), 2x ember + luna 1.60 (n=5); ember + terra 0.50 (n=4) is the outlier low (CR:336). Batch 11 sonnet + 2x luna n=6: 2.33 (sd 0.94, range 1-4) (CR:424). Only n=1 rows reach 3-4/14 (CR:306-314) and none replicated (CR:370).

**Never-found issues.** "Never found by any of the 106 runs: B1, B2 ..., I5 ... and I6 ... Found exactly once: B6 (luna + terra + wonder)" (CR:501; B6 = alias GT1 per legend CR:412). The older sentence at CR:287 ("alias GT3 in 1 row") is superseded **[STALE DOC]**; CR:503 says B8 (alias GT3) was found in 2 runs overall; ALL-src row shows B8=1 (CR:498). HO R2 (HO:78) repeats the stale CR:287 wording — correction confirmed (S01 H4). Three issues carry almost every score: B3 95 of 106 runs, I8 76, I2 71 (CR:502).

**No panel significantly better.** Three-way permutation p 0.54-1.0 on found, real blocking, wrong blockers, control; tokens p 0.002-0.009 (CR:381). Batch 11: sonnet + 2x luna vs ember + 2x luna found p=0.51, real blocking p=1.0, wrong blockers p=1.0, control p=0.28; tokens 139k vs 64k p=0.003; elapsed 821 s vs 348 s p=0.003 (CR:425). Only three statistics survive audit F (CR:298): second luna raises control found +0.83 (Welch p 0.004, permutation 0.048); 2x luna + 2x ember +2.75-3.25 wrong blockers (p 0.005-0.03); ember + terra -1.75 found (p 0.029). n=4-6 per panel.

**Default and tiers (final, CR:428).** Default = ember + 2x luna (n=6: 1.83/14, 0.17 real blocking, control 0.83, 63,644 tokens, 348 s elapsed; CR:331, :366, :378). Optional quality tier = sonnet + 2x luna "only if issues like control GT1 matter (reached in 3 of 6 runs vs 0 of 6) and the extra ~75k tokens and ~8 minutes are acceptable" (CR:428); Fisher p ~0.012, "post-hoc and exploratory" (CR:426). Best measured real blocking: haiku + 2x luna 1.2/8, 191k tokens, 3.0 wrong blockers, n=5 (CR:319, :367).

**Sonnet "standard" rejected.** The DECISION UPDATE (CR:383) made sonnet + 2x luna the standard from n=1 (4/14); batch 11's 5 replicates averaged 2.0/14 (CR:424), "Verdict on the decision update: NOT CONFIRMED" (CR:428). So CR:375-383 is superseded by CR:421-428 within the same file **[STALE DOC]** (CR:383 still reads as current guidance unless the reader reaches :421).

**"Sonnet alone gives most catches per token"** (wording from S04 0.13 / COMBO/PLAN.md:18-24). Source is the pilot only: arm A sonnet 2/16 at 93,098 tokens = 2.15 catches per 100k vs B 0.76 and C 0.66 (PR:48-50), n=1 run per package, pre-`source.md` era (2026-11-11). In the valid-era tables, cheaper panels exceed it on that metric: ember + luna 4.29, ember + 2x luna 2.88 per 100k (CR:317, :331); single-model sol 8.63 and terra 13.81 per 100k at n=1 (CR:334-335). No valid-era sonnet-alone row exists (the only sonnet-alone set is S62, pre-src, 1 run, 1.00/14; CR:496). So the claim is true only for the pilot comparison and must not be carried as a current fact [UNVERIFIED as a valid-era claim; contradicted by E2's own valid-era tables, see Gaps].

**Corrections already known (date 2026-11-13):**
- Verdict flips: CR:292 says "Four verdicts flipped FAIL->PASS" but lists three named rows "plus total-loss merges"; audit-D/summary.md:20 names 3 (S01 H15). HO:105 says 4. Use 3 named flips + total-loss merges.
- Once-found issue = alias GT1 (B6), not alias GT3 (CR:501 vs CR:287).
- Source-blind runs: 156 of 665 valid-era runs (CR:373) replaces 161 (CR:293 and CR:371) **[STALE DOC]** at CR:371 (the Decision paragraph still says "161 runs").
- Per-model dropped counts at CR:292 (luna 30, ember 33, ...) are all dropped findings, not blocking ones (S01 H14).
- Judge-blocking vs real blocking: 65 judge "blocking" catches, 38 real (CR:291).

**Harness-incident history relevant to reuse (SPEC):** concurrency of 12 workers caused gateway identity bleed (SPEC:78); muse misroute 2026-11-11 ~22:40 UTC (SPEC:82) and again 2026-11-12 ~15:46 UTC (SPEC:117); glm misroute 2026-11-12 ~08:25 UTC (SPEC:88); stop rule "if any reviewer fails the observed-model check twice, STOP that worker" (SPEC:79); cyclic ladder incident "69 FALLBACK lines in 3 s", "Both would have passed model_ok because expected_model is overwritten by the fallback model" (SPEC:141) — confirms the runner defect in section 1 from the study's own record; batch 11 used `NOFALLBACK=1` (SPEC:151, CR:422). Many operational paths live in `/tmp` (launchers, logs, `/tmp/audit-A..F`, SPEC:95, :100, :114, :134, :140, :147).

**What the study measured and did not** (HO 2.7, cross-checked with CR): first reviews only, one round; 3 packages, 16 GT items; deterministic merge only — no calibrator, no debate, no orchestrator (S04 0.13 citing COMBO/PLAN.md:25); the merge-drop defect (HO D1) and source-blindness depress every number (CR:371).

Key Takeaways
- [E2] About 1.6-2.5 of 14 known defects per run for every replicated panel (n=4-6 each, 2026-11-12/13); no quality difference survives testing; only tokens and time differ (p 0.002-0.009).
- [E2] Default ember + 2x luna (n=6); sonnet + 2x luna kept only as an optional tier (n=6, exploratory I7 reach); sonnet "standard" rejected by batch 11.
- [E2] "Sonnet alone most catches per token" is pilot-only (n=1 per package, pre-source era); valid-era cheaper panels beat it per token.
- [E2] Corrections: 3 named verdict flips (not 4), once-found = alias GT1 (B6), 156 not 161 source-blind runs, dropped-by-model counts are all findings.

---

## 7. E1 shadow harness: generalisation plan and overlap with existing eval tooling [E1][E3]

**Source:** SSE (132 lines, dated 2026-11-12, SSE:3), read fully.

What the document says (doc claims; code was not re-read for every cite here, tags as noted):
- "the shadow run is not a program": the agent executes prose steps 1-10 of reflect SKILL.md §4.3a (SSE:7-9); only `review/manifest.py` and `review/manifest_cmd.py` mention `t2_engine` (SSE:8-9). [CODE-VERIFIED by S04 0.16 grep, same session 2026-11-13; not re-run here]
- Classification table generic vs reflect-specific (SSE:12-29): generic = authority rule idea, manifest mechanism (hashes, ordered stages, idempotent attempts, resume, atomic save), publish guard, panel resolver, deterministic clustering, citation pre-check, exit-script skeleton; reflect-specific = steps 1-10, manifest constants, `card_convert.py`, `panel_lint.py`, shadow brief line. Line cites into `manifest.py` etc. [UNVERIFIED in this file; slice 08 covers run recording].
- Minimal generic contract, 5 parts (SSE:35-50): frozen variant, authoritative path, recording, comparison, exit measurement. Key limit: "reflect's shadow variant produces no verdict of its own; it reuses the legacy reviewers' dispatch ... so it measures side signals (agreement, compliance, parity), not quality" (SSE:47-48).
- Complexity Medium (harness) / Large (variant with own comparable output; doubles spend) (SSE:67-72); ~1,700 lines in play (SSE:71-72: manifest 534, manifest_cmd 240, exit 410, replay 184, lint 366). Spot-check: `scripts/reflect_shadow_exit.py` is 410 lines (`wc -l`, 2026-11-13) [CODE-VERIFIED for that one count].
- Risks (SSE:85-96): test pins on `mf.STATES`; skill-contract test limits SKILL.md edits; contract 1.8.0 coupling; "The mechanism has never run for real: `test_shadow_exit_script.py:292-302` asserts 'shadow runs counted: 0 of 20'". This last risk is now **[STALE DOC]**: 15 shadow dirs exist and 13 count (section 8 below). The test may still assert 0 of 20 on its fixture; not re-read [UNVERIFIED].
- **Extraction plan (SSE:100-123)**: (1) gate on 20 real shadow runs PASSing `reflect_shadow_exit.py`; (2) profile-parametrised run-manifest module moving `review/manifest.py` logic unchanged; (3) reflect profile with today's constants, re-exported so `mf.STATES` imports keep working; (4) profile-aware CLI, `superclaude review manifest` stays as reflect alias; (5) split `reflect_shadow_exit.py` into generic aggregator + reflect check plugin; (6) shared protocol ref by installed path, `make sync-dev`/`verify-sync`; (7) SKILL.md §4.3a pointer only; (8) golden byte-for-byte manifest check + verdict replay of recorded `pre-*` runs; (9) keep 13 named test files green, then `make test`; (10) only then wire one second consumer the owner names.
- Recommendation (SSE:127-132): extract only after the 20 runs and only if the owner names a second skill.

**Generalisation assessment for the unified panel (question 2):**
- The E1 harness answers "did the new path run alongside the old one without changing it, and do the side signals look sane?"; the E2 harness answers "does a panel find known defects?". They are complementary, not overlapping: E1 has no ground truth and no quality score (SSE:47-48); E2 has no shadow/authority mechanism and no run manifest (sections 1-3). A unified evaluation story needs both: shadow for rollout safety, GT benchmark for quality. [E1][E2]
- E1's planned generic piece (manifest profile + exit-aggregator skeleton) could host E2's runs as a "profile": E2 already records per-run `meta.json`/`cost.json` but no frozen input hash per run (only GT hashes in `manifest.md:14-16`) and no stage commits. [inference from read code; not designed anywhere, UNVERIFIED as a plan]
- The gate in step 1 (20 PASSing shadow runs) is not met today: 13 of 20 and FAIL (section 8).

**Overlap with existing eval tooling** (existence checked by Glob; headers read 2026-11-13):
- `scripts/eval_runner.py` (364 lines): "v3.0 Eval Runner — orchestrates parallel local + global eval runs" with modes `local|global|full` (:1-8); runs fixed pytest files under `tests/roadmap/` and `tests/audit/` (`EVAL_FILES`, :26-32) and `scripts/eval_1..3.py` (:34-38). It evaluates roadmap/audit pipeline behaviour, not review panels. Overlap with a panel benchmark: low (process pattern only: local vs master checkout comparison). [CODE-VERIFIED header only; body UNVERIFIED]
- `scripts/ab_test_workflows.py` (290 lines): "A/B Testing Framework for Workflow Variants" (:2-11), loads `docs/memory/workflow_metrics.jsonl` (:271), Welch-style `perform_ttest` via `scipy.stats` (:17, :72), `determine_winner` (:87). Overlap: the statistics step (two-variant comparison of a metric). E2 uses permutation tests instead (`three-way.py:33-38`). Whether `workflow_metrics.jsonl` is still written by anything is [UNVERIFIED].
- `src/superclaude/cli/eval/` (cliEval, 26 modules; `runner.py` 1,251 lines, `models.py` 946): "IronClaude real-eval harness" (`__init__.py:1`); per-eval lifecycle isolation → hooks → spawn → inject → observe → assert → teardown (`runner.py:1-13`), PASS/FAIL/ERRORED mapping (`runner.py:17-26`); drives the real `claude` binary through `ClaudeProcessAdapter` with per-eval `HOME` isolation (`claude_process.py:1-20`). Overlap with E2's `run-reviewer.sh`: both spawn a fresh real `claude` session in an isolated environment and assert on output. cliEval has the isolation, timeout, retry (`retry.py` exists) and reporting machinery E2 re-implemented in bash; it has no ground-truth judge, no panel merge and no model-identity check that I found [UNVERIFIED: only headers read; no grep for identity in cli/eval done]. This is the most plausible host for a repo-portable E2 benchmark runner.

Key Takeaways
- [E1] The shadow harness measures non-interference and side signals, never quality (SSE:47-48); its extraction is gated on 20 PASSing runs and a named second consumer (SSE:101, :123, :131).
- [E1][E2] Shadow (rollout safety) and GT benchmark (quality) are complementary; a unified panel needs both.
- [E1][E2] `src/superclaude/cli/eval/` already provides real-`claude` spawning with HOME isolation, retry and PASS/FAIL reporting — the likely home for a portable E2 runner; `eval_runner.py` (roadmap tests) and `ab_test_workflows.py` (t-test over workflow metrics) overlap only in pattern.
- [E1] SSE's "never run for real" risk is stale (13 shadow runs now counted).

---

## 8. E1 Stage 2 exit: full `reflect_shadow_exit.py` output and failure classification of shadow runs 08-15 [E1]

**Command and exit code (run 2026-11-13 by this agent, read-only):** `uv run python scripts/reflect_shadow_exit.py` from the repository root, default runs root `.dev/reflect`. **Exit code 1** = Stage 2 exit criteria not met (expected; not a tool failure).

**Full output (re-run read-only in the Phase 3 fix cycle 1 on 2026-11-13T20:53:34Z UTC, HEAD `792cf8c52`, from the repository root; exit code 1; 73 lines; byte-identical to the copy in `research/07-reflect-merge-contract.md` §5, lines 192-264, checked with `diff`):**

```text
Stage 2 shadow-exit report

shadow runs counted: 13 of 20 required
  incomplete (not counted): pre-TASK-WF-detachTheCcsessi-20261102-034618-shadow02 (state clustered)
MALFORMED audit.log rows: 0 (must be 0)
EV-1 failure rate (len(reviewer_cards) rule, Wave 4 runs only): shadow 8/13 = 0.615; legacy baseline 3/39 = 0.077 (must be no higher)
parity assertion per run (recomputed):
  pre-TASK-WF-addTheSharedCode-20261111-193909-shadow04: FAILS (card model 'claude-gw-tier1b[1m]' differs from the resolved 'claude-sonnet-5-5')
  pre-TASK-WF-analyzeCodegraph-20261111-193557-shadow15: FAILS (the legacy rotation (reviewer_personas, reviewer_models) is not in the contract)
  pre-TASK-WF-authorizedNarrow-20261106-214325-shadow06: holds
  pre-TASK-WF-designOutput-20261111-193642-shadow14: holds
  pre-TASK-WF-detachTheCcsessi-20261102-034618-shadow03: holds
  pre-TASK-WF-devGuideFenceFix-20261104-204854-shadow12: holds
  pre-TASK-WF-fixIssue412SVeri-20261106-215543-shadow13: holds
  pre-TASK-WF-fixTheScIssueWor-20261104-162205-shadow05: FAILS (card model 'claude-gw-tier1b' differs from the resolved 'claude-sonnet-5-5'); recorded true but recomputed false
  pre-TASK-WF-implementFrOnb1O-20261023-180618-shadow10: holds
  pre-TASK-WF-implementIronbel-20261104-130647-shadow09: FAILS (card model 'claude-gw-tier1b[1m]' differs from the resolved 'claude-sonnet-5-5')
  pre-TASK-WF-implementTheDesi-20261031-182028-shadow11: holds
  pre-TASK-WF-planTheExplicitl-20261110-024937-shadow08: FAILS (card model 'claude-gw-tier1b[1m]' differs from the resolved 'claude-sonnet-5-5')
  pre-TASK-WF-renameTheScIssue-20261104-174359-shadow07: FAILS (the legacy rotation (reviewer_personas, reviewer_models) is not in the contract); recorded true but recomputed false
contract lint and manifest per run:
  pre-TASK-WF-addTheSharedCode-20261111-193909-shadow04: 1 problem(s)
    no contract
  pre-TASK-WF-analyzeCodegraph-20261111-193557-shadow15: 1 problem(s)
    L6 EV-1: reviewer-cards/ holds 0 card(s), fewer than the required 3 (reviewers_resolved from panel/manifest.json)
  pre-TASK-WF-authorizedNarrow-20261106-214325-shadow06: 1 problem(s)
    L6 EV-1: neither a merged adversarial verdict nor a loud fallback is on disk (merged-verdict: absent; fallback missing: adversarial_unavailable: true, merge_method: single-reviewer-fallback, audit.log F2/F3 row)
  pre-TASK-WF-designOutput-20261111-193642-shadow14: clean
  pre-TASK-WF-detachTheCcsessi-20261102-034618-shadow03: 1 problem(s)
    L6 EV-1: neither a merged adversarial verdict nor a loud fallback is on disk (merged-verdict: absent; fallback missing: adversarial_unavailable: true, merge_method: single-reviewer-fallback)
  pre-TASK-WF-devGuideFenceFix-20261104-204854-shadow12: clean
  pre-TASK-WF-fixIssue412SVeri-20261106-215543-shadow13: 2 problem(s)
    L2 stable keys: top-level key 'zero_drop_flag' is not in the 1.8.0 stable field list or the telemetry block
    B bump rule: the contract leaves 1.8.0 (1 stable-key violation(s), 0 EV-2 value violation(s)); a new stable key or merge_method value needs a contract version bump, which this plan does not make
  pre-TASK-WF-fixTheScIssueWor-20261104-162205-shadow05: 1 problem(s)
    L6 EV-1: neither a merged adversarial verdict nor a loud fallback is on disk (merged-verdict: absent; fallback missing: adversarial_unavailable: true, merge_method: single-reviewer-fallback)
  pre-TASK-WF-implementFrOnb1O-20261023-180618-shadow10: clean
  pre-TASK-WF-implementIronbel-20261104-130647-shadow09: 1 problem(s)
    no contract
  pre-TASK-WF-implementTheDesi-20261031-182028-shadow11: clean
  pre-TASK-WF-planTheExplicitl-20261110-024937-shadow08: 1 problem(s)
    no contract
  pre-TASK-WF-renameTheScIssue-20261104-174359-shadow07: 5 problem(s)
    L2 stable keys: top-level key 'memory_status' is not in the 1.8.0 stable field list or the telemetry block
    L2 stable keys: top-level key 'notes' is not in the 1.8.0 stable field list or the telemetry block
    L2 stable keys: top-level key 'zero_drop_flag' is not in the 1.8.0 stable field list or the telemetry block
    L6 EV-1: neither a merged adversarial verdict nor a loud fallback is on disk (merged-verdict: absent; fallback missing: adversarial_unavailable: true, merge_method: single-reviewer-fallback, audit.log F2/F3 row)
    B bump rule: the contract leaves 1.8.0 (3 stable-key violation(s), 0 EV-2 value violation(s)); a new stable key or merge_method value needs a contract version bump, which this plan does not make
verdict replay against the legacy baseline (42 runs): new degraded reasons 0

Stage 2 counts:
  2-of-3 shortfalls: 0
  unknown executor class (executor_class_resolved false): 9
  findings-block compliance rate (mean over 9 run(s)): 0.704
  cluster_agreement (9 run(s)): min 1.000, median 1.000, max 1.000

failure: EV-1 failure rate is higher than the legacy baseline
failure: pre-TASK-WF-addTheSharedCode-20261111-193909-shadow04: parity does not hold
failure: pre-TASK-WF-analyzeCodegraph-20261111-193557-shadow15: parity does not hold
failure: pre-TASK-WF-fixTheScIssueWor-20261104-162205-shadow05: parity does not hold
failure: pre-TASK-WF-implementIronbel-20261104-130647-shadow09: parity does not hold
failure: pre-TASK-WF-planTheExplicitl-20261110-024937-shadow08: parity does not hold
failure: pre-TASK-WF-renameTheScIssue-20261104-174359-shadow07: parity does not hold
failure: pre-TASK-WF-addTheSharedCode-20261111-193909-shadow04: lint or manifest problems
failure: pre-TASK-WF-analyzeCodegraph-20261111-193557-shadow15: lint or manifest problems
failure: pre-TASK-WF-authorizedNarrow-20261106-214325-shadow06: lint or manifest problems
failure: pre-TASK-WF-detachTheCcsessi-20261102-034618-shadow03: lint or manifest problems
failure: pre-TASK-WF-fixIssue412SVeri-20261106-215543-shadow13: lint or manifest problems
failure: pre-TASK-WF-fixTheScIssueWor-20261104-162205-shadow05: lint or manifest problems
failure: pre-TASK-WF-implementIronbel-20261104-130647-shadow09: lint or manifest problems
failure: pre-TASK-WF-planTheExplicitl-20261110-024937-shadow08: lint or manifest problems
failure: pre-TASK-WF-renameTheScIssue-20261104-174359-shadow07: lint or manifest problems
OVERALL: FAIL (shadow runs 13 of 20)
EXIT_CODE=1
```

Key lines of the full output above, summarised:

- `shadow runs counted: 13 of 20 required`; `incomplete (not counted): ...-shadow02 (state clustered)`.
- `MALFORMED audit.log rows: 0 (must be 0)`.
- `EV-1 failure rate (len(reviewer_cards) rule, Wave 4 runs only): shadow 8/13 = 0.615; legacy baseline 3/39 = 0.077 (must be no higher)`.
- Parity recomputed: FAILS for shadow04, 05, 07, 08, 09, 15 (04/05/08/09: `card model 'claude-gw-tier1b[1m]'` (05: `'claude-gw-tier1b'`) `differs from the resolved 'claude-sonnet-5-5'`; 07/15: `the legacy rotation (reviewer_personas, reviewer_models) is not in the contract`); 05 and 07 `recorded true but recomputed false`; holds for 03, 06, 10, 11, 12, 13, 14.
- Lint/manifest: `no contract` for 04, 08, 09; 15 `L6 EV-1: reviewer-cards/ holds 0 card(s), fewer than the required 3`; 03, 05, 06, 07 `L6 EV-1: neither a merged adversarial verdict nor a loud fallback is on disk`; 13 `L2 stable keys: top-level key 'zero_drop_flag'` + `B bump rule`; 07 three L2 keys (`memory_status`, `notes`, `zero_drop_flag`) + B; clean: 10, 11, 12, 14.
- `verdict replay against the legacy baseline (42 runs): new degraded reasons 0`; `2-of-3 shortfalls: 0`; `unknown executor class (executor_class_resolved false): 9`; `findings-block compliance rate (mean over 9 run(s)): 0.704`; `cluster_agreement (9 run(s)): min 1.000, median 1.000, max 1.000`.
- `OVERALL: FAIL (shadow runs 13 of 20)`.

This matches S04 0.15 and adds the head of the output S04 did not capture (EV-1 8/13 vs 3/39; per-run reasons). [CODE-VERIFIED: output of the script at HEAD `792cf8c52`]

**How the script decides (read 2026-11-13):** a run counts only if `panel/manifest.json` has `t2_engine_effective == "shadow"` and `state == "published"` (`scripts/reflect_shadow_exit.py:209-223`). The contract is `_yaml_map(run/"return-contract.yaml") or {}` (:224); **an unparseable contract becomes `{}`, which yields lint `["no contract"]` (:240-242) and `ev1_fail = True` (:243)**. Parity: card headers come only from `panel/cards/reviewer-<N>.md` (:98-110), the card `model:` must equal `resolution.json` `reviewers[i].model` by string (:148-152), and the contract must hold `reviewer_personas`/`reviewer_models` lists (:154-162). EV-1 card count uses `_CARD_FILE = ^reviewer-(\d+)-card\.(yaml|yml|md)$` (`src/superclaude/cli/reflect/panel_lint.py:188`, :219-227, :273-276). [CODE-VERIFIED]

**Timeline evidence (file mtimes, UTC, this worktree; host TZ is UTC):** commit `9874d63fb` 2026-11-13T01:54:25Z, commit `c2e3347d3` 2026-11-13T02:57:12Z (`git log`). Run files: shadow08 01:19-01:48, shadow09 01:23-01:35, shadow10 01:21-01:38, shadow11 01:16-01:40 (all **before** `9874d63fb`); shadow12 02:24-02:49, shadow13 02:07-02:27, shadow14 02:10-02:53, shadow15 01:59-02:47 (all **after** `9874d63fb`, before `c2e3347d3`). Brief text confirms it: the `9874d63fb` schema line ("never a table") is in all 3 briefs of shadow12-15 and in none of shadow03-11; the `c2e3347d3` line ("exact heading line") is in **no** shadow run's briefs (grep of `reviewer-briefs/*.md`). So **no recorded shadow run exercised `c2e3347d3`**, and only 4 runs (12-15) exercised `9874d63fb`. Whether the installed `SKILL.md` (not only `refs/reviewer-spec.md`) was updated before shadow12-15 is inferred from the brief line, not proven [UNVERIFIED].

**What the fixes changed (from `git show`, read 2026-11-13):** `9874d63fb` rewrote SKILL.md §4.3a steps 2 (card `model:` copied verbatim from `panel/resolution.json`, harness model on `model_observed:`), 4 (compliance measured on first parse, orchestrator never remaps findings), 7 (write `adversarial/merged-verdict.yaml`, confirm the exact path), 10 (contract must carry `reviewer_personas`/`reviewer_models`, no new top-level key), the schema + example line in `refs/reviewer-spec.md`, and the exit-script test no longer pins "0 shadow runs" (commit message; resolves the [UNVERIFIED] note in section 7 about `test_shadow_exit_script.py`). `c2e3347d3` only makes the brief name the literal heading `## Findings block` (not `## Findings`). [CODE-VERIFIED in the diff]

**Classification, runs 08-15** (categories: harness defect = the measuring script or the run harness; skill-text defect already fixed = the skill text lacked the instruction and a later commit added it; real panel defect = the shadow mechanism or its orchestrator fails even with correct text):

| Run | Ran vs fixes | Exit result | Evidence | Classification |
|---|---|---|---|---|
| shadow08 | before `9874d63fb` | parity FAILS (alias in card header); `no contract` | `return-contract.yaml:103` `reviewer_models: [claude-gw-tier1b[1m], claude-gw-tier4[1m], claude-gw-tier1a[1m]]` — PyYAML error "expected ',' or ']', but got '['" at line 103 col 35; only `adversarial/merged-verdict.md` exists, no `.yaml` | Parity: **skill-text defect already fixed** (step 2). `no contract`: **real defect, NOT fixed** — the legacy contract writer emits invalid YAML when gateway aliases carrying `[1m]` go unquoted into a flow list; the script then also counts EV-1 as failed (:243). Missing `.yaml` verdict: skill-text defect fixed (step 7) |
| shadow09 | before | parity FAILS (alias); `no contract` | same YAML error at `return-contract.yaml:103`; card 1 header is free prose `# Reviewer 1 card — ... model: claude-gw-tier1b[1m] (sonnet-5-5)`; `adversarial/merged-verdict.yaml` present | Parity: **skill-text defect already fixed** (step 2). `no contract`: **real defect, not fixed** (unquoted `[1m]` aliases) |
| shadow10 | before | holds, clean | — | pass |
| shadow11 | before | holds, clean | compliance 0.67 recorded | pass (compliance is not a gate) |
| shadow12 | after `9874d63fb` | holds, clean | compliance 1.0 | pass |
| shadow13 | after | lint: top-level `zero_drop_flag` + bump rule | `return-contract.yaml:43` `zero_drop_flag: true`; step 10 (added by `9874d63fb`) forbids new top-level keys | **real panel defect** — orchestrator ignored skill text that already existed (prose-following lapse) |
| shadow14 | after | holds, clean | first-parse compliance **0.0 (0/3)**: reviewers wrote `## Findings`; orchestrator then rewrote the heading in all 3 cards (`panel/notes.md:4-6`) | exit-clean, but: heading miss = **skill-text defect, fixed later by `c2e3347d3`** (untested); the orchestrator's heading edit breaks the step-4 rule "never edits ... a reviewer's findings" in letter (heading only, per notes:6) |
| shadow15 | after | parity FAILS (legacy rotation not in contract); L6 EV-1 0 cards | contract has `reviewer_cards:` (:45-48) but no `reviewer_personas`/`reviewer_models`; telemetry written to a separate `telemetry.yaml` (:28); legacy cards saved as `reviewer-cards/reviewer-<N>.md`, not the `reviewer-<N>-card.*` name of SKILL.md:695 and `panel_lint.py:188`; `adversarial/merged-verdict.yaml` present (step 7 worked) | **real panel defect** (orchestrator ignored step 10 and the legacy card naming); the strict file-name regex is a contributing harness strictness, not the root cause |

**EV-1 8/13 decomposition** (from the per-run lines above): 03, 05, 06, 07 (verdict file absent — pre-fix, step 7), 04, 08, 09 (unparseable contract counted as EV-1 fail by :243), 15 (card naming). After `9874d63fb`: 1 of 4 runs fails EV-1 (15), 0 of 4 for verdict placement. The comparison against the legacy baseline 3/39 is therefore inflated by 3 YAML-parse failures that are not EV-1 failures in substance [inference from :243 + the parse errors; whether the legacy baseline loader treats unparseable contracts the same way was not read, UNVERIFIED].

**Compliance per run (recorded `findings_block_compliance_rate`):** 03 1.0 (after re-ask), 04 1.0 (after re-ask), 05 0.33, 06 1.0, 07 0.333, 08 1.0, 09 1.0 (after 2 normalize fixes), 10 1.0, 11 0.67, 12 1.0, 13 1.0, 14 0.0, 15 not in contract (1.0 in `telemetry.yaml:47`). Pre-fix values mix first-parse and after-re-ask definitions (comments in 03, 04, 09), which S04 F-10 already flagged; post-fix values are first-parse: 1.0, 1.0, 0.0, 1.0 (n=4).

Key Takeaways
- [E1] Stage 2: FAIL, exit 1, 13 of 20 runs (2026-11-13). Of runs 08-15, 4 pass (10, 11, 12, 14) and 4 fail (08, 09, 13, 15).
- [E1] Pre-fix failures (08, 09) are mostly the skill-text defects `9874d63fb` fixed, **plus one unfixed real defect: contracts become unparseable YAML when `[1m]` gateway aliases are written unquoted** (also hit shadow04) — and the exit script then counts them as EV-1 failures.
- [E1] Post-fix failures (13, 15) are real defects of the prose-driven orchestrator: it ignored step 10 and the card naming even with correct text. Only 4 runs saw `9874d63fb` and 0 saw `c2e3347d3`, so neither fix is validated.
- [E1][E2] Shared lesson with E2's runner (section 1): any record keyed on model ids must quote/escape them and must keep requested and observed identity in separate fields.

---

## 9. E1 5x3 model-combination study: leads, dated (`COMBO/PLAN.md`, `FINDINGS.md`, `results.md`, `combos.json`; runs 2026-11-13) [E1][E2]

**Design (doc, cross-checked against data files):** 5 combos x 3 repeats on one fixed input, `TASK-WF-designSpec-20261107-075614` (plan + `source.md` only, hashes in `combos.json` `input`), skill hashes frozen per block (FINDINGS.md:3). Orchestrator per combo (`combos.json` `combos[].orchestrator`): A `claude-gw-tier3[1m]`, B-E `claude-gw-tier1b[1m]` [CODE-VERIFIED in `combos.json`]. Pre-set lead rule: ranges do not overlap, median gap > A's own range, >= 2 of 3 runs dispatched as designed; ~40 comparisons so chance separations expected (PLAN.md:181-184).

**Leads (FINDINGS.md:29-31; per-run values in results.md:5-19, all n=3 per combo, one package, 2026-11-13):**
1. **Orchestrator speed.** A 63.9 and 67.9 min in its two as-designed runs (A3 collapsed, 19.4) vs B 23.4-38.5 min (results.md:5-10). FINDINGS says "Cause not isolated" (FINDINGS.md:29). **New evidence from the stream logs (read 2026-11-13):** the top-level (`parent_tool_use_id == null`) assistant turns of comboA-r1 were served by `glm-5.3` (150 turns) and `qwen3.8-max` (63 turns), comboA-r2 by `glm-5.3` (142) and `qwen3.8-max` (71), while comboB-r1 was `claude-sonnet-5-5` (133) [CODE-VERIFIED in `logs/*.jsonl`]. So "tier3 vs tier1b" was in fact **non-Anthropic GLM/Qwen vs Claude Sonnet** as orchestrator, consistent with PLAN.md:193-194 ("2026-11-11 probe: tier3 = GLM 5.3", marked UNVERIFIED there). E2 excluded exactly these two models from its reviewer fallbacks (`EXCLUDE_MODELS` default `"glm-5.3 Qwen3.8-max"`, run-reviewer.sh:69) and the pilot disqualified Qwen after 3/3 timeouts (PR:12). [E1][E2]
2. **Calibrated confidence.** D 0.62-0.66 and E 0.53-0.68 below A 0.75-0.84 (FINDINGS.md:30); calibrator models differ across combos (results.md:33-47: A/B/C calibrators mostly opus, D sonnet or luna, E haiku), so the lead is confounded. Whether lower confidence is better calibrated is not measured.
3. **First-pass compliance.** A 0.67 in all 3 runs, B/C/D 1.0 in all 9, E 1.0/0.67/0.33 (results.md:5-19). With item 1, the A orchestrator (GLM/Qwen) is the plausible common cause of both A leads [inference; not isolated].

**Dispatch facts (3/3-type facts, PLAN.md:187-188):** the "haiku" slot in A and B was served by `gpt-6.1-sol` (results.md:33-38); A3 collapsed to `claude-sonnet-5-5` for every reviewer and calibrator (results.md:35); E had 3 reviewers but 2 distinct models (results.md:17-19, 45-47); E1 shows 7 reviewer calls (results.md:45, extra calls not explained in FINDINGS). None of this is visible in `panel/resolution.json`, card headers or `panel_parity` (FINDINGS.md:15).

**Blind ground-truth scoring was NOT done and NOT approved.** PLAN.md:171-174 lists it as "optional, separate approval (spends tokens)": anonymise REPORT.md and merged verdict, one Opus judge per run against E2's `ground-truth.json` for designSpec (10 defects, 5 blocking) via `git show b4db265a8:...`. FINDINGS.md:3 and :42 confirm it was not run. So the study says nothing about which combo finds more real defects. [E1, reusing E2's GT]

**Cost (results.md:5-19):** output tokens 93,616-367,381 per run; USD figures are Claude Code estimates, "do not compare" (FINDINGS.md:37).

Key Takeaways
- [E1] Three leads at n=3 (2026-11-13): orchestrator speed (A 64-68 min vs B 23-39), lower calibrated confidence in D/E (confounded by calibrator model), A compliance 0.67 every run.
- [E1][E2] New: combo A's "tier3" orchestrator was served by GLM 5.3 + Qwen3.8-max (non-Anthropic), the two models E2 banned from its fallback ladder — the speed and compliance leads are likely about the orchestrator model family, not "tier3".
- [E1] No quality evidence: blind GT scoring against E2's ground truth was planned as a separately approved step and not run.
- [E1] `combos.json` still says `"status": "designed, not run"` **[STALE DOC]**.

---

## 10. The untracked `runs/pre-TASK-WF-designSpec-20261107-075614-comboC-r3/artifacts/base-e8db2fe6/` folder [E1]

**Contents (find, 2026-11-13):** 129 files — `src/superclaude` 43, `tests/pr_submit` 81, `tests/cli` 1, `tests/skills` 1, `docs/user-guide` 2, `Makefile` 1; every file mtime `2026-11-07T06:13Z` = the commit time of `e8db2fe66` (2026-11-07T01:13:48-05:00), as `git archive` sets it. `git status` shows only this folder untracked in that run (`??`).

**Who made it and why [CODE-VERIFIED in the run's stream log]:** the comboC-r3 stream log `logs/pre-TASK-WF-designSpec-20261107-075614-comboC-r3.jsonl` holds a Bash call `mkdir -p $B; git archive e8db2fe66 src/superclaude/pr_submit src/superclaude/skills/sc-pr-submit-protocol ... tests/pr_submit ...` with `B=$OUT/artifacts/base-e8db2fe6`, issued by the **orchestrator** (assistant turn with `parent_tool_use_id: null`, served `claude-sonnet-5-5`), not by a reviewer subagent. The orchestrator's own reason is recorded in `t1-card.md:10` and `REPORT.md:20`: the spec says it read master `e8db2fe66`; HEAD already contains the implementation (`0b8a5801d`, 2026-11-07, "feat(pr-submit): hold the PR as a draft..."), so "Every repository fact below was read from a `git archive` of `e8db2fe66`". The briefs point reviewers there (`reviewer-briefs/reviewer-1.md:9`, :17, and `### .../base-e8db2fe6/src/superclaude/pr_submit/recovery.py:33-42` grounding hunks at :148, :165, :199); `artifacts/mkbriefs.py:10` sets `SNAP = f"{out}/artifacts/base-e8db2fe6"`; reviewer 2 cites `artifacts/base-e8db2fe6/tests/pr_submit/test_static_grep.py:37-53` (`reviewer-cards/reviewer-2-card.md:29`).

**Did a reviewer read outside the input snapshot?** The run's `artifacts/input-snapshot-repo-paths.yaml` lists only 2 files (plan + `source.md`, `file_count: 2`) and neither snapshot file mentions `base-e8db2fe6`. Reading repository code outside the 2-file snapshot is normal in every reflect pre run (grounding reads the repo); the snapshot pins input identity, not the read set. What is unusual: in C3 the reviewers read a **different repository view** (base commit) than in the other 14 runs (HEAD, which contains the finished implementation). The plan accepted HEAD grounding on purpose: the input copy leaves out the implement history (`progress.md`, `artifacts/retries/`, "the answer key") but "grounding reads post-implementation code (same for every combo)" (PLAN.md:114-119, read 2026-11-13). C3 broke that "same for every combo" condition. "Temporal anchor" notes appear in the t1 cards of B1, C3, D2, D3, E1, E2, E3 (7 of 15), but only C3 built an archive (grep `git archive` in `runs/*/t1-card.md`: 1 of 15). So the folder shows **an uncontrolled per-run variation by the orchestrator, which reduces answer exposure in C3 but makes C3 not identical in protocol to the others**. It does not show a reviewer reading a forbidden file; whether reviewers in the other runs read implemented code at HEAD (answer leakage) was not checked [UNVERIFIED; PLAN.md:169-170 defines a `leak` column as citations into `.dev/tasks/done/`, which `results.md` does not report].

Key Takeaways
- [E1] The folder is a partial `git archive` of the plan's base commit made by the comboC-r3 orchestrator (Sonnet) to avoid reading the implemented HEAD; reviewers were pointed to it.
- [E1] Not evidence of a reviewer escaping the snapshot; it is evidence that the orchestrator varies the grounding view per run (1 of 15 archived, 7 of 15 noted the anchor), a confound for any GT scoring of the 15 runs.
- [E1][E2] A unified benchmark should fix the grounding view in the harness (E2 did: sandbox `git archive` of HEAD minus `.dev/tasks/done`, manifest.md:10), not leave it to the orchestrator.

---

## 11. E3 experiment bundle: verdicts and the no-valid-success caveat (`BUNDLE/SNAPSHOT-STATE.txt` 3 lines; `BUNDLE/reports/phase5/FINAL-REPORT.md` 259 lines, read fully 2026-11-13) [E3]

**Status of the documents.** FINAL-REPORT frontmatter: `status: "reviewed-report; design and final assembly pending"`, dated 2026-11-09 (FINAL-REPORT.md:6-9); "Scientific conclusion | Convergence not proven; no validated winner" (:42). SNAPSHOT-STATE.txt:1-3: "a preservation bundle in progress, not a final success report"; exploratory diffgate/ponytail repeats PAUSED for missing owner authorization; a fresh design session hit API 429 and "no completed design or actual design Skill invocation is yet verified"; **"No valid-success verdict is implied."** (:3); the legacy `SHA256SUMS` is historical, `REPORT-STAGE-INVENTORY.sha256` is the report-stage inventory (:3).

**Headline verdict (FINAL-REPORT.md:75):** "PR 427 is not proven to make review loops converge. None of the completed, measured loops reached a clean PASS. None of the five proposed variants has a valid, repeated convergence result."

**Per-arm results (FINAL-REPORT.md:94-107; one scenario, 57,763-byte start spec, 3 reviews + 2 fix cycles per loop; dates 2026-11-08/09):**

| Arm | n loops | New CRITICAL+MAJOR labels r1/r2/r3 | Growth | Outcome |
|---|---|---|---|---|
| Pre-427 controls | 2 | 11/9/8; 12/7/4 | 57.72%; 69.34% | FAIL both |
| Exact 427 | 2 | 9/5/6; 9/7/5 | 23.11%; 36.27% | FAIL both |
| 427 + re-review flags | 2 | 16/5/6; 17/6/1 | 27.78%; 32.14% | FAIL both |
| Diffgate | 1 | 7/2/2 | 10.31% | FAIL, cap escalation; separate full audit 4 MAJOR (:120) |
| Ponytail | 1 | 9/7/0 | 22.03% | FAIL; verdict parser failed; final reviewer changed model (:104, :134, :199) |
| Ledger | 1 | 13/9/3 | 22.16% | ESCALATE; sweep found 9 MAJOR + 3 MINOR (:105, :120) |
| Stoprule | 0 | review 1 only (6 blockers of 8 sealed claims) | — | invalid: transcript-integrity verifier failed on asynchronous grader replies (:106, :162) |
| Minfix | 0 | — | — | build halted at task 3 (:107, :166) |

Fixed screen (not a statistical test, :87): control mean final proxy 6, limit 3; control growth 63.51%, limit 44.457% (:129). 427 arms fail the count and spread conditions (:131-132); diffgate's improvement 4 equals but does not exceed control spread 4 (:133); ponytail fails same-model validity (:134); ledger 3 < spread 4 (:135). Variant growth below both controls supports "observed size reduction", not a repeatable effect (:137).

**Validity failures named by the report (:197-204):** single scenario; no valid variant repeats (n=1 each); model continuity failed (ponytail final review `claude-opus-5-5` requested, `gpt-6.1-sol` recorded; ledger part-Sol, :199) — the same served-model drift seen in E1 (S04 F-12) and E2 (SPEC:82-88); restricted review coverage; answer exposure in diffgate (:201); proxy counts; unaudited ponytail zero. Coordinator deviation: the coordinator selected repeats on weaker screens and called them authorized; an independent review returned FAIL on that claim (:208).

**What it recommends (FINAL-REPORT.md:171-192):** do not ship a combined variant; candidates are hypotheses: limit revisions to confirmed blockers, mechanical finding identity/disposition tracking, optional severity/necessity audit, honest coverage statement, fail-closed parsing and provenance (:173-179); a refactor spec must keep <= 3 reviews / 2 fix cycles, record "actual reviewer model, input hashes and scope" (:185-190).

**Cross-check against code [partial]:** the report names product mechanisms (`fix_audit.py` `cmd_verdict`, stoprule `transcript_blocks`/`cmd_verify_transcript`, :152, :162). These are experiment-variant scripts installed only under `~/.claude/` per the task context; not read here [UNVERIFIED in this file].

Key Takeaways
- [E3] Bundle verdict (2026-11-09): convergence not proven, no validated winner; every completed loop ended FAIL or ESCALATE; n=2 per 427 arm, n=1 per variant, 2 variants never completed. "No valid-success verdict is implied" (SNAPSHOT-STATE.txt:3).
- [E3] Only robust observation: smaller document growth under 427 and the variants (10-36% vs 58-69%), not fewer defects.
- [E1][E2][E3] All three efforts hit served-model drift (requested Claude, served `gpt-6.1-sol` or another family); "record actual reviewer model" is a shared requirement.
- [E3] Reusable for the unified panel: fixed pre-registered screen, frozen endpoint hashes, an evidence-consistency checker (`final_report_check.py`, no model calls, :250) — the E3 counterpart of E2's GT hashes and E1's exit script.

---

## 12. Tier 2 cost versus worth (slice 04 assignment 10) [E1][E2]

**Inputs and what each measures:**

| Evidence | Value | Sample / date | Measures | Does not measure |
|---|---|---|---|---|
| T2 is the typical reflect pre path | MR:142: 37 of 38 recorded pre runs escalated to T2, 34 by the parsed-sparse pre-filter, 0 stopped at T1 on the rubric. **Re-counted 2026-11-13** over non-shadow `.dev/reflect/pre-*/artifacts/tier_decision.yaml`: 39 files, `selected_tier: 2` in 38, `1` in 1, `parsed-sparse` in 35 [CODE-VERIFIED in data] | census of one repo's history | how often T2 cost is paid | whether T2 finds more |
| H-A (worth) | MR:527: T2 recall must beat T1 by >= 15 pp on seeded defects; if not, the owner chooses "between shrinking T2 to 2 reviewers and tuning the rubric (O-8)" | **not measured** (pilot designed, not run; S04 4.2) | — | — |
| O-8 | MR:556: "the cheaper lever may be the rubric: 34 of 38 recorded pre decisions escalated because of the parsed-sparse pre-filter, not plan risk; decide after H-A" | open | — | — |
| E2 ceiling | every replicated panel 1.60-2.50 of 14 known defects per run, n=4-6 per panel (CR:315-333); "All panels sit at about 2-2.5 of 14" (CR:428) | 3 packages, 2026-11-12/13 | tasklist first-review recall of spec-panel critique, deterministic merge | reflect T1 vs T2; calibration, debate |
| E2 size effect | no quality difference between replicated panels (p 0.54-1.0), only tokens differ (p 0.002-0.009) (CR:381); 4-reviewer `2x luna + 2x ember` adds 2.75-3.25 wrong blockers (p 0.005-0.03, CR:298); chosen default is a 3-reviewer panel at 63,644 tokens (CR:331, :428) | n=4-6 | more reviewers ≠ more found; more reviewers = more false blockers; the 2-reviewer panels ember + sonnet 2.50/14 (n=4) and ember + luna 2.25/14 (n=4) score as high as any 3-reviewer panel (CR:315-333, section 6) | 2 vs 3 reviewers inside reflect (with calibration and debate) |
| "Sonnet alone most catches per token" | pilot arm A 2/16 at 93,098 tokens = 2.15 per 100k vs 0.76 and 0.66 (PR:48-50) | n=1 run per package, pre-`source.md` era, 2026-11-11 | single reviewer is cheapest per catch in the pilot | valid-era claim — contradicted by cheaper valid-era panels (section 6) |
| Reflect T2 spend | shadow contracts' orchestrator estimates, e.g. shadow08 `token_usage` wave_3 137,000 (`return-contract.yaml:102`), shadow04 wave_3 90,000 + wave_4 240,000 (`:102`); combo runs 185,086-367,381 output tokens per whole run for B-E (results.md:8-19) | 2026-11-13 | order of magnitude of T2 cost | billed cost (estimates; PLAN.md:164 says "record, never compare") |

**What the evidence supports (2026-11-13):**
1. **T2 cost is almost always paid**, and mostly for an input-format reason, not plan risk (35 of 39 parsed-sparse). This is measured. [E1]
2. **Adding reviewers beyond three does not raise recall in E2's setting** and adds wrong blockers (CR:298, :381); replicated 2-reviewer panels match the 3-reviewer ones (2.25-2.50 vs 1.60-2.33 of 14). This supports "not more than 3" (MR's cap, S04 4.1), and in E2's setting (spec-panel critique, deterministic merge, no calibration or debate) it supports "2 is as good as 3". [E2]
3. **Whether T2 (3 reviewers + calibration + debate) beats T1 (single agent) on reflect plans is not measured.** E2 never ran reflect, a calibrator, or a debate (S04 0.13; section 6), so its ceiling cannot be read as the T2 ceiling, and H-A remains unmeasured. A 2-reviewer reflect T2 is also not measured anywhere.
4. **The rubric lever is cheaper by construction and is evidence-backed on the cost side only:** if the parsed-sparse pre-filter stopped forcing T2 for workflow packages, up to 34-35 of 38-39 recorded runs would have been eligible to stop at T1. How many of those would then be wrongly stopped (missed defects) is **not measured**.

**Verdict for the unified panel:** the evidence supports **fixing the rubric first (O-8) as the default lever**, because it acts on the measured driver of T2 spend (parsed-sparse escalation) and needs no new reviewer-count decision; and it supports **capping at 3 reviewers**. E2 leans toward 2 reviewers being enough, but only for its own setting; for reflect it does **not** decide between 2 and 3 reviewers, nor whether T2 is worth its cost over T1 — both wait on H-A (MR:527), which needs the seeded-defect pilot (pilot-design.md, S04 0.2). E2's harness (ground truth + blind judge, sections 2-4) is the only existing instrument that could measure T1-vs-T2 recall on plans, after the portability fixes in section 3 and with a reflect consumer added. [E1][E2]

Key Takeaways
- [E1] Measured: T2 runs on 38 of 39 recorded pre plans (2026-11-13), 35 via the parsed-sparse pre-filter.
- [E2] Measured: beyond 3 reviewers, no recall gain and more wrong blockers (n=4-6 per panel, one gateway, 2026-11-12/13).
- [E1][E2] Not measured: T2 vs T1 recall (H-A), 2 vs 3 reflect reviewers, rubric-change miss rate. Recommendation the evidence allows: rubric first, cap 3, decide reviewer count only after H-A.

---

## Gaps and Questions

**UNVERIFIED claims (from all sections):**
1. [E2] Whether every fallback row (where `expected_model` was overwritten, section 1) was removed before E2's final tables (HO 2.5 says quarantined and rerun).
2. [E1] The `reflect-reviewer` tool allowlist as the mechanical write-deny for reflect reviewers (section 1; not re-read here; S04 0.7 reports 3/3 survival under `model` override).
3. [E2] The later `anon-*.sh` scripts (only `anon-combos.sh` read) and whether `merged-1.md` bodies contain model names the anonymiser misses (section 2).
4. [E2] How the committed `analysis/final-table.md` was produced from the `/tmp` outputs (section 3).
5. [E2] Whether the GT evidence paths (`.dev/tasks/done/TASK-WF-design-20261108-041415/...`) exist on master or this branch (section 4).
6. [E2] The ~115k judge tokens per scoring (doc number, PR:52; raw `judge.json` uncommitted) and whether pilot judges were in-session subagents or `claude -p` (section 5).
7. [E2] All E2 headline numbers are doc-sourced from COMBO-REPORT; raw `score.json`/`cost.json` were not re-aggregated (section 6).
8. [E1] SSE line cites into `review/manifest.py`, `manifest_cmd.py`, `panel_lint.py` sizes (section 7; only the 410-line exit script count was checked).
9. [E1] `scripts/eval_runner.py` body, the writer of `docs/memory/workflow_metrics.jsonl`, and whether `src/superclaude/cli/eval/` has any model-identity check (section 7; headers only).
10. [E1][E2] Hosting E2's runs as an E1 manifest "profile" is an inference, not a designed plan (section 7).
11. [E1] Whether the installed `SKILL.md` (not only `refs/reviewer-spec.md`) carried `9874d63fb` when shadow12-15 ran (section 8; inferred from the brief line).
12. [E1] Whether the legacy EV-1 baseline (3/39) treats unparseable contracts as failures the way the shadow side does (`reflect_shadow_exit.py:243`) (section 8).
13. [E1] Cause of the combo leads: the GLM/Qwen orchestrator in A is a strong candidate but not isolated; why E1 shows 7 reviewer calls (results.md:45) (section 9).
14. [E1] Whether reviewers in the 14 HEAD-grounded combo runs cited implemented code (answer exposure); `results.md` has no `leak` column although PLAN.md:169-170 defines one (section 10).
15. [E3] The variant scripts named in FINAL-REPORT (`fix_audit.py` `cmd_verdict`, stoprule `transcript_blocks`, `cmd_verify_transcript`) were not read (section 11).

**CODE-CONTRADICTED doc claims (or contradicted by data):**
1. [E2] HO 3 lesson 1 / CR "blind" judge: the judge brief carries the combo name (`judge-one.sh:21`) and the folder path (`:6`); blind to reviewer ids only (section 2).
2. [E2][E3] HO D11 "duplicate models not observed in the eval": the control package's `resolution-live7.json` and `resolution-default.json` contain duplicate models (section 4).
3. [E2] "Sonnet alone gives most catches per token" as a current fact: pilot-only (n=1 per package, pre-source era); E2's valid-era tables show cheaper panels with more catches per 100k (section 6).
4. [E1] SSE:85-96 "the mechanism has never run for real": 15 shadow dirs, 13 counted (section 8); `9874d63fb` also changed the test that pinned 0 runs.
5. [E1] COMBO FINDINGS "A differs only in the orchestrator (tier1b instead of tier3)": true as configured, but the served A orchestrator was `glm-5.3` + `qwen3.8-max` (stream logs), a model-family change the document does not state (section 9).
6. [E1] `combos.json` `"status": "designed, not run"`: all 15 runs exist and were published (section 9).
7. [E1] MR:142 counts (37 of 38, 34 parsed-sparse) are superseded by the 2026-11-13 recount (38 of 39, 35) — same conclusion, newer numbers (section 12).

**Open questions for the synthesis:**
- Should the unified panel's contract writer quote model ids (the `[1m]` YAML break, section 8), and should the exit gate distinguish "unparseable contract" from "EV-1 failure"?
- Should the next shadow runs (7 more to reach 20) be held until `c2e3347d3` is installed, since no run has exercised it?
- Is a blind GT scoring of the 15 combo runs still worth its approval given the C3 grounding variation (section 10) and the GLM/Qwen orchestrator in A?
- Who owns the E2 benchmark port (cliEval host, section 7) so that H-A can be measured on reflect?

## Stale Documentation Found

- **[STALE DOC]** E2 `tools/tmp-scripts/README.md:7` lists `checks-gate8`, which was not copied into the commit (section 2).
- **[STALE DOC]** E2 `manifest.md:5` "local, never pushed" — the branch is on origin (section 4).
- **[STALE DOC]** E2 `COMBO-REPORT.md:287` "alias GT3 in 1 row" superseded by CR:501 (once-found = alias GT1, B6); repeated in HO:78 R2 (section 6).
- **[STALE DOC]** E2 `COMBO-REPORT.md:375-383` DECISION UPDATE (sonnet + 2x luna standard) superseded by CR:421-428 "NOT CONFIRMED" (section 6).
- **[STALE DOC]** E2 `COMBO-REPORT.md:371` (and :293) "161" source-blind runs superseded by CR:373 "156 of 665" (section 6).
- **[STALE DOC]** HO:105 "4 verdicts flipped" — audit D names 3 plus total-loss merges (section 6).
- **[STALE DOC]** E1 `shadow-standalone-evaluation.md:85-96` "never run for real" (section 7/8).
- **[STALE DOC]** E1 `.dev/eval-workspaces/shadow-model-combos/combos.json` `status: "designed, not run"`, and PLAN.md:1-3 "designed, NOT run" per S04 0.13 (section 9).
- **[STALE DOC]** S04 0.15 "head of the script output (EV-1 counts) was not captured — UNVERIFIED numbers": now captured, EV-1 shadow 8/13 vs legacy 3/39 (section 8).
- **[STALE DOC]** MR:142 history counts (37/38, 34) vs 2026-11-13 data (38/39, 35) (section 12).

## Summary

[E2] The other session's benchmark (ground truth from real implement failures, a "blind" Opus judge without `source.md`, permutation-test aggregation) is the only quality instrument any of the three efforts built, but it is not repo-portable: it hard-codes `/tmp` and another worktree, silently drops the audit filter when `/tmp/audit-*` is missing, lets the judge see the panel name, and overwrites the requested model on fallback; its measured result (2026-11-12/13, n=4-6 per panel, 3 packages) is a 1.6-2.5 of 14 ceiling with no panel significantly better, ember + 2x luna as default, and 2-reviewer panels as good as 3-reviewer ones. [E1] This session's shadow harness measures non-interference, not quality: Stage 2 is FAIL (exit 1, 13 of 20 runs, EV-1 8/13 vs 3/39); of runs 08-15, the pre-fix failures are mostly skill-text defects `9874d63fb` fixed plus one unfixed defect (unquoted `[1m]` model aliases make contracts unparseable YAML, which the exit script also counts as EV-1 failures), and the post-fix failures (13, 15) are the orchestrator ignoring correct text; no run has exercised `c2e3347d3`. [E1][E2] The 5x3 combo study's leads (speed, confidence, compliance; n=3, 2026-11-13) are likely driven by combo A's orchestrator being served by GLM 5.3 and Qwen3.8-max, the same models E2 banned, and no ground-truth scoring was approved or run; the untracked `base-e8db2fe6` folder is an orchestrator-made base-commit archive (not a reviewer escaping the snapshot) that makes run C3 protocol-different. [E3] The #346 bundle states convergence not proven and "No valid-success verdict is implied" (n=1-2 loops per arm), with served-model drift shared by all three efforts. [E1][E2] On Tier 2 cost versus worth, the evidence supports fixing the parsed-sparse rubric first (38 of 39 recorded pre runs reach T2, 35 by that pre-filter) and capping at 3 reviewers; T2-versus-T1 recall (H-A) and 2-versus-3 reflect reviewers are not measured, and E2's harness, once made portable, is the instrument that could measure them.
