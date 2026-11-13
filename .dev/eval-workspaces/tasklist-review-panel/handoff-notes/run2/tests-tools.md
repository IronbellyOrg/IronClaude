# Tests and tools inventory (run2)

Repo: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
Date: 2026-11-14. Read-only. UNVERIFIED marks claims not checked directly.

## 1. Tests covering src/superclaude/cli/review/* and the review-loop prompts/skills

Source under test: src/superclaude/cli/review/ = __init__.py(33 lines) findings.py(457) ledger.py(494) ledger_cmd.py(137) merge_cmd.py(118) panel.py(525) panel_cmd.py(87) telemetry.py(447) telemetry_cmd.py(98); data/ = review-panel.default.json, review-panel.live7.json, review-tiers.default.json. Registered as `superclaude review` in src/superclaude/cli/main.py:568-570.
Review-loop prompt file: src/superclaude/rules/prompts/document_review_loop_prompts.md (74 lines).
Other files that grep-hit review modules: tests/skills/test_model_alias_policy.py (1 hit), tests/pr_submit/test_conflict_sync_protocol.py (3 hits) - incidental, not counted. tests/cli/reflect/* is the /sc:reflect ensemble, not this module - excluded. tests/cli has NO file covering cli/review.

All runs: `uv run pytest <file> -q --no-header -p no:cacheprovider`, 2026-11-14. Combined collect-only: 304 tests collected in 0.38s. ALL 304 PASS, 0 fail, 0 skip.

| File | def test_ | collected | result | time | Covers |
|---|---|---|---|---|---|
| tests/review/test_review_cli.py | 9 | 9 | pass | 0.34s | CLI surface: help lists subcommands; panel resolve JSON; gateway when T3Model01 set; unknown env fails; panel validate exit codes; merge->revise->verdict round trip incl. --resolution (valid file only); verdict exit codes 0/10/11; telemetry commands; merge refuses round with no valid block and writes nothing |
| tests/review/test_review_findings.py | 23 | 23 | pass | 0.27s | findings-v1/fixmap-v1 parsing, bad JSON line keeps good lines, MINOR+blocking error, field validation (anchor <12 and 201, claim 301, refs 9, bad category "weird", severity HIGH, bad id, duplicate id, non-bool blocking), last of two blocks wins, unclosed blocks invalid, prior lines, fixmap table fallback, anchors/locate/spans across wraps, fingerprints, clusters, same-defect within/beyond 3 lines |
| tests/review/test_review_ledger.py | 24 | 24 | pass | 0.31s | ledger statuses/events: round 1 rows, refound/regressed/cleared, revise -> resolved_check, sha mismatch refused, rounds 1-3 verdict+decision (ESCALATE at 3), defer, capture export, round merged twice / out of order refused, no-valid-block refused (3 forms), one valid block enough + warnings non-empty, atomic save |
| tests/review/test_review_panel.py | 26 | 41 | pass | 0.47s | panel schema errors (16 parametrized), total 9 rejected, 2 fixed / 0 fixed rejected, tier schema errors incl. duplicate model in an alias list, stand-ins, fallback depth, fallbacks wrap, random reproducible, exclude only when another candidate exists, distinct_across_slots, data-edit-only alias changes, determinism, round_robin, env precedence, template/tier lookup precedence, importlib.resources defaults |
| tests/review/test_review_panel_live7.py | 14 | 14 | pass | 0.30s | @live7 valid with 7 reviewers; anthropic-only -> 1 Sonnet + 6 Haiku; re-review -> anchor only; packaged tier2b models in order; gateway resolves seven; placeholder tier2b fails closed (lib + CLI); env var SUPERCLAUDE_REVIEW_PANEL=@live7; CLI @live7; unknown/malformed packaged names rejected; default panel unchanged |
| tests/review/test_review_rules_text.py | 5 | 5 | pass | 0.02s | rules file: insertion lines A/B/C exactly once after their brief lines, heading order Findings block < Fix map < Review panel < Never, contract example line text, older pins, no "src/superclaude" in file |
| tests/review/test_review_telemetry.py | 10 | 10 | pass | 0.30s | telemetry record schema, append-only routing, no document text in records, task variables, loader idempotent + bad lines, model score arithmetic/supersession, stratum tag, conflicting stratum excluded, short context labels |
| tests/skills/test_review_brief_placement.py | 5 | 5 | pass | 0.26s | prompt text lives only in the rules file; spec-panel gate is one sentence; routing guide points at gate; guide/plugin twin byte-equal; installer + plugin ship rules file |
| tests/skills/test_review_loop_extension.py | 9 | 18 | pass | 0.04s | spec-panel Review Loop extension prose pins (both src and plugins copies) |
| tests/skills/test_review_prompt_overrides.py | 14 | 33 | pass | 0.61s | brief lint: no quotas, "assume defects remain", "apply all findings", any-severity FAIL; t07/t09 original briefs flagged; shipped briefs pass |
| tests/skills/test_review_severity_mapping.py | 8 | 14 | pass | 0.05s | consequence-based severity, Medium tier after S5 in pragmatic.md, boundary table rows |
| tests/skills/test_review_severity_rule.py | 21 | 62 | pass | 3.20s | S1-S5 severity rule copied verbatim to 10 files, 2-fix-cycle cap, cap-edits/sweep-edits fixture rows hold, no zero-tolerance/any-severity wording in tracked primitives |
| tests/skills/test_spec_panel_review_loop.py | 11 | 46 | pass | 0.08s | /sc:spec-panel ## Review Loop section: 7 bullets in order, cap text, vocabulary, routing-guide flags, release guides |
| TOTAL | 159 | 304 | 304 pass | ~6.3s summed | |

### NOT covered (checked against source)

- Length limits (findings.py:79-121): tested only out-of-range values (anchor "short" = 5 chars and 201 chars, claim 301, refs 9). Exact boundaries (anchor 12 and 200, claim 300, refs 8) not tested. anchor2 over/under-length not tested (only a valid anchor2). claim has no minimum. Length is counted after whitespace flattening (flat()); only indirectly exercised.
- Prompt/code drift: the rules file (document_review_loop_prompts.md:60) states category list and anchor 12-200, but does NOT state claim <= 300 chars, refs <= 8, or the id regex ^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$ - yet the parser rejects violations. No test asserts that the prompt's category list / limits equal findings.CATEGORIES / _check_flat limits.
- Accepted categories (findings.py:15-22: contradiction, unpassable-check, data-loss, safety, missing-requirement, other): only "contradiction" and "other" are used in passing tests; only "weird" is tested as rejected. The other four accepted values are never parsed in a test. Case variants (e.g. "Contradiction") untested.
- Resolution files (merge --resolution, merge_cmd.py:73-83): only a valid resolution is tested. Untested: malformed resolution (ClickException path), a --report reviewer id absent from the resolution (model silently None), and a resolved reviewer that has no --report (merge never checks report set == resolution set; a missing reviewer is silently absent). --report without "=" error untested.
- @live7: well covered (lib, env var, CLI, placeholder fail-closed, gateway, anthropic-only). Gap: gateway test (test_review_panel_live7.py:85-101) asserts only pairwise t2!=t2b, t3-1!=t3-2, t4-1!=t4-2; it does NOT assert all seven models distinct. Verified by running `superclaude review panel resolve --template @live7 --env gateway --run-id <id>`: run-a itself resolves glm-5.3 twice (t2b-1 and t3-2), and 26 of 40 run ids r1..r40 contain a duplicate model (r19 has glm-5.3 three times). Cause: panel.py:405/408 falls back to the full candidate list when every candidate is already chosen (`... or candidates`), and tier2/tier2b/tier3 share glm-5.3 and Qwen3.8-max. Also each reviewer's `fallbacks` list may contain models other reviewers already use - untested and unhandled.
- Duplicate models: tier-file duplicate within one alias list is tested (rejected). Cross-slot duplicates in a resolution are not rejected or warned anywhere (by design in anthropic-only: 6 Haiku). "duplicate reviewer id in one round" (ledger.py:120-121) has no test (grep found none).
- Ledger rounds: rounds 1-3 and ESCALATE at cap 3 tested; merging round 4+ after ESCALATE is NOT refused by merge_round (only n == len(rounds)+1 is checked) and is untested. Non-default --cap untested (grep for --cap/cap= found none in tests/review).
- Dropped-finding reporting: an invalid finding line is dropped (findings.py:188-192); merge_round adds ONE warning per reviewer carrying the error count and only the FIRST message (ledger.py:130-134). The merged report shows only "block ok false" per reviewer (ledger.py:421-424); it does not list dropped findings or the warnings. Warnings are only in the CLI's stdout JSON. Test coverage: only `assert res["warnings"]` (test_review_ledger.py:384). No test of merged-report text for a broken reviewer, of the warning content, or of a valid-JSON-but-invalid finding line (e.g. claim 301) being dropped while the reviewer's block still counts for clearing. Note: clearing (ledger.py:254-258) ignores block_ok, so a resolved_check row clears if no parsed finding matches it, even if the reviewer who would have re-found it had that line dropped.

## 2. Inventory of .dev/eval-workspaces/tasklist-review-panel/20261111-a1/

### Top level
- COMBO-REPORT.md (83,296 B, 506 lines): master report. Sections: What was run; Master table; Ranking; Cross-cutting; Verdict; Limits; Artifacts; Batch 3 addendum/final; CORRECTION 2026-11-12 (blocking-count parser bug + luna quarantine); Batch 4/5; 6; 7; 8 + FINAL TABLE; 9; untried combos; "FINAL RESULTS AND DECISION (2026-11-13) - supersedes every earlier table" (line 289); DECISION UPDATE three-way (375); Issue-by-panel table (385); Batch 11 result - decision update REJECTED (421); Every combination ever run (430).
- PILOT-REPORT.md (6,835 B): 2026-11-11 pilot through Step 4 blind scoring on 3 packages.
- manifest.md (1,271 B), full content summarized: EVAL path; UTC 2026-11-11; branch ironbelly/eval-tasklist-review-panel "(local, never pushed)" [now stale - see section 3]; HEAD == origin/master == ec259f1b718c...; `superclaude review --help` works; T2bModel01=gpt-6.1-terra; @live7 resolves 7 reviewers; reviewer sandbox /tmp/evalsb/repo = git archive of HEAD without .dev/tasks/done, .dev/eval-workspaces, .dev/research; dispatch = `claude -p --model <raw gateway model id>`, observed model = assistant message.model; tier aliases NOT used because they serve only the first model of a tier; ground-truth sha256 for the 3 packages (designSpec 3e56551d..., makeTheAliasOnly 79e32057..., design e3585b8e...).
- 3 package dirs TASK-WF-{design-20261108-041415, designSpec-20261107-075614, makeTheAliasOnly-20261105-051649}: candidate.md, ground-truth.json, ground-truth-draft.json, resolution-default.json, resolution-live7.json, reviews/ (pilot reviewer outputs + reviews/combos/<row>/ + live7-t3-1/), reviews-failed-launch-1/. Pilot reports have *.md.catfix.md copies (unpassable-ac -> unpassable-check normalisation).
- arms/{A,B,C}/<pkg>/ pilot arm merges; arms/scoring/<pkg>/ and arms/scoring/combos/<row>/<pkg>/<label>/ blind scoring (merged-anon.md, score.json, label-key.json, judge.json [judge.json not committed]).
- combos/: 107 entries = SPEC.md + 106 row dirs (c*, b4-*, e*, g1-g9 r1-r4, h1/h2 r1-r4, j1 r1-r5, n2/n4/n5 variants incl. *-contaminated-20261111, r*-*, *-src, r2-sonnet-superseded-20261112, sol-alone-src, terra-*). Each row holds <pkg>/{ledger.json, merge-stdout.txt, merged-1.md, resolution.json} (checked on g1-ember-luna2-r1). Only 19 of 106 rows have a RESULT.md (why later rows lack it is UNVERIFIED; which rows lack it was not listed).
- probe/probe.json (Stage 0 dispatch probe).
- quarantine-pre-src-luna/: pre-source.md luna-era data (3 package copies, _combos, _fallback-smoke) quarantined by owner order 2026-11-12 15:16 UTC.
- tools/ (below), analysis/ (below).

### tools/
- run-reviewer.sh (88 lines, current; detailed below). GENERIC-ish: any <pkg> with candidate.md, brief is a generic `/sc:spec-panel --mode critique` first review. Tasklist/eval-specific bits: line 10 hard-codes /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/tasks/done/$PKG/source.md; /tmp/evalsb sandbox; raw gateway model ids in the ladder.
- run-reviewer.sh.bad-launch (4,302 B): first version; brief passed as positional argv (not stdin), unconditional cp of candidate; brief category list says `unpassable-ac`.
- run-reviewer.sh.unpassable-ac (4,352 B): stdin brief + cmp-guarded copy; still lists category `unpassable-ac` (parser accepts only `unpassable-check` -> those finding lines were dropped; SPEC.md:38-39 Correction prescribes *.catfix.md sed copies). No fallback ladder, no APIERR check, 2 attempts.
- tmp-scripts/ (55 files; README.md says verbatim copies from /tmp made 2026-11-13, many hard-code /tmp paths and the 20261111-a1 dir). ALL are eval-specific (hard-coded EVAL path and/or the 3 TASK-WF package ids) unless noted:
  - Anonymisation for blind scoring: anon-arms.sh (pilot arms -> arms/scoring/<pkg>/<label>/merged-anon.md), anon-combos.sh, anon-b7/b8/b9/b11.sh (same for each batch's combos).
  - Merging: arm-merges.sh (pilot arm merges with catfix copies, refuses to overwrite merged-1.md), merge-b6.sh (merge pattern later merge-bN derive from), merge-src-rows.sh (source.md-era rows).
  - Batch launchers/runners: b4-run.sh (serial source.md impact study), b4-run-noglm.sh (glm dropped 2026-11-12 14:40), b4-par.sh (10 concurrent, muse semaphore 4), b4-par-launch.sh (two xargs streams P4 muse / P6 other over /tmp job lists), b4-job-one.sh (job runner, honours /tmp/cancel-<row>), b4-luna-muse.sh, b4-luna-muse-gated.sh, b4-luna-nomuse.sh, b4-terra-alone.sh, b5-jobs-gen.sh (writes /tmp/b5-*.txt), b6-launch.sh (muse-ember replacement study), b10-rerun-one.sh (NOFALLBACK=1 rerun of one reviewer).
  - Per-row drivers (one-offs): c1-driver.sh, c2-run.sh, c3-run.sh, c5-chain.sh, n2sonnet-run.sh, n2terra-run.sh, n2terra-wait.sh, n3-run.sh, n4terra-run.sh, n5-driver.sh, n5-finish.sh, n5s-run.sh, n5sol-run.sh, n5sol-run2.sh, n5terra-jobs.sh, n5terra-run.sh, r2-sonnet-driver.sh and r2terra-run.sh (both send hard-coded Orca heartbeats with fixed terminal/task/dispatch ids), r2s-run.sh, r2sol-run.sh, r3-run.sh, r5-run.sh.
  - Orchestration: startcombo.sh / startcombo2.sh / startcombo3.sh (`orca orchestration worker-start` with a spec pointing at combos/SPEC.md for one row).
  - Judging: gen-judge-list.sh (39 judge dispatches -> /tmp/combo-judges.tsv), judge-one.sh (blind judge: `claude -p --model claude-opus-5-5`, bypassPermissions, no tool restriction, reads GT + candidate + merged-anon.md, writes score.json; prompt is generic to "candidate plan" + GT file), run-combo-judges.sh (39 judges, 4 at a time).
  - stats.sh (per-row stats over reviews/combos; uses $PWD).
  - NOT this eval despite README's claim: brief_c1.py, drift-b3.py, snap.py, rlog-r3.sh reference /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/eval-workspaces/shadow-model-combos (a different eval); snap.py WRITES into that other worktree.

### analysis/ (script purposes from docstrings/headers)
- attrib.py: per-model GT attribution from judge notes + merge ledgers (source.md-era rows); approximate prose parse. -> attrib.json/attrib.out.
- doubles.py: panels with 2 reviewers of the same model: GT caught by run A/B, union, overlap, wrong blockers. Reads /tmp/attrib.json. -> doubles.out.
- b8-table.py: final replicate table, per-family mean(range), wall/tokens, 2x-vs-1x deltas. b9-table.py: batch 9 table; `exec`s /tmp/b8-table.py.
- final-table.py: FINAL table by reviewer-model multiset, AS-SCORED vs AUDIT-CLEAN views, JUDGE vs REAL blocking. -> final-table.md, final-all.json, final-clean.json.
- three-way.py: sonnet+2luna vs ember+2luna vs sonnet+luna+ember (+h2); `exec`s /tmp/final-table.py.
- untried.py: model-presence effects and untried model sets. -> untried.out.
- allsets/allsets-setup.py (inventory every scored run, group by era + model multiset -> /tmp/allsets.json), allsets/allsets-table.py (direct per-set issue counts, cross-check of agents) -> allsets-table.md; allsets-chunks/, allsets-out/, allsets.json, allsets-direct.json.
- issue-table/: issue-setup.py (legend I#/B# + top-10 map; `exec`s /tmp/final-table.py), issue-table.py (issue-by-panel counts from score.json), issue-compare.py (agent vs direct); issue-01..10.{json,tsv}, issue-legend.*, top10.json, issue-table-final.md.
- Launch/merge records: b7/b8/b9/b10/b11-launch.sh, merge-b7..b11.sh, b11-rerun-one.sh (NOFALLBACK=1), logs b10.log, b8/b11-judge-run.log, b11-rerun.log, judge TSVs b7..b11, b10-fix.txt, b11-fix.txt, b8-final.md, b9-final.md, gt2-hits.txt, combo-est-{A,B,self}.md.
- audits/audit-A..F (no docstrings; purpose from summary.md / flags.tsv check names): A = model identity and attempts (890 runs); B = incomplete/short reports (patch.py, patch2.py edit audit.py in place); C = era/input leakage (candwrites.py, leakdbg.py); D = merge and ledger integrity (264 merged-1.md, all ledger round 1 only; flags include "block ok false; raw findings=2, ledger members=1" = real dropped findings); E = scoring sources/quarantine; F = aggregation completeness/recompute. Summaries cite /tmp/audit-*/ paths.
- RAW-TRANSCRIPTS-NOT-COMMITTED.md: ~1.48 GB / 2,916 raw `*.attempt<N>.json` and `judge.json` left out; read COMBO-REPORT "FINAL RESULTS AND DECISION" first.
- Reproducibility hazard: b9-table.py, three-way.py, issue-setup.py exec /tmp copies; doubles.py, allsets-table.py, issue-*.py, audit-F/extra*.py, audit-D/mk.py read /tmp JSON. They do not run from the committed tree alone.

### combos/SPEC.md (152 lines) structure
Title "Speed-weighted reviewer combinations (Qwen3.8-max excluded)" + rationale (pilot wall times) + c1..c5 table; "Procedure for ONE combo" (run-reviewer.sh max 2 at once; build resolution.json from resolution-live7.json via jq; `superclaude review merge --round 1 ... --resolution`; rerun once if refused; RESULT.md table); "Hard limits" (read-only repo, no GT, own row only, no worktrees); Correction (unpassable-ac -> catfix); Batch 2; Batch 3; Batch 3 contamination re-run; muse outage; Cooldown; glm outage; Batch 4 (source.md impact); Batch 4 amendment; Quarantine pre-source.md luna; Batch 5; Muse misroute recurrence; Batch 6 (muse-ember); Fallback ladder v2 (2026-11-12 18:10); Batch 7; 8; 9; 10; Batch 10 DROPPED; Batch 11 (sonnet + 2x luna x5). It is an append-only ops log, not a spec.

### tools/run-reviewer.sh - full read (88 lines)
- Usage (l.2): run-reviewer.sh <EVAL abs> <pkg id> <reviewer_id> <model> [subdir]; l.6 OUT=$EVAL/$PKG/reviews[/$5].
- Inputs (l.7-12): copies candidate.md to /tmp/evalsb/cand/$PKG/candidate.md if different; copies .dev/tasks/done/$PKG/source.md (absolute worktree path) next to it if present; never removes a stale source.md; brief does not mention source.md. SHA = sha256 of sandbox candidate.
- Dispatch (l.48): `cd /tmp/evalsb/repo && timeout 3000 claude -p --model "$MODEL" --output-format json --no-session-persistence --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit <<<"$BRIEF"` -> attemptN.json/.err. Bash is not disallowed.
- Checks per attempt (l.50-59): .md = first result text; OBS = unique main-thread assistant message.model; TOK/TOKALL output tokens; APIERR if .md contains "API Error"; MODEL_OK if OBS non-empty, not "<synthetic>", equals MODEL or MODEL-build (case-insensitive); BLOCK_OK if any line starts with ```findings-v1 (presence only, no parse/validation); meta.json written; success = MODEL_OK && BLOCK_OK && !APIERR.
- Retries (l.61-64): up to 2 attempts per model, no backoff.
- Fallback ladder (l.19-43, 65-83): FALLBACK map glm-5.3->Qwen3.8-max->gpt-6-luna->muse-ember-1.0->claude-haiku-5-5->grok-4.7->gpt-6.1-sol->glm-5.3 (cycle); muse-wonder-1.0->muse-spark-1.3->gpt-6.1-terra->gpt-6-luna; claude-sonnet-5-5, muse-wonder-full-1.0, claude-opus-5-5 -> gpt-6.1-sol. Escalates if primary failed (or APIERR) and NOFALLBACK is empty. EXCLUDE_MODELS default "glm-5.3 Qwen3.8-max" (skipped as fallback targets only; a primary in the list still runs). VISITED prevents revisiting (if the next non-excluded model was visited, the ladder stops). Each fallback model gets 2 attempts; loop continues while !(MODEL_OK && BLOCK_OK) - an APIERR result with model+block ok ends the ladder. Logs "FALLBACK a -> b (time)" to $RID.fallback.log.
- Ladder differs from packaged tiers: includes muse-ember-1.0 (not in review-tiers.default.json tier4) and is a separate hand-kept map, not read from the tier file.
- Outputs (l.85-87): $RID.md and $RID.meta.json = LAST attempt of LAST model even if it failed; $RID.cost.json = jq -s over $RID.attempt*.meta.json. BUG: attempt counter resets per fallback model (l.76), so a fallback model's attempt1/attempt2 files OVERWRITE the primary's; cost.json then undercounts the overwritten attempts and the primary's raw output is lost (fallback.log is the only trace).
- Brief text (verbatim, lines 13-17):
  l.13: `BRIEF="/sc:spec-panel @$CAND_SB --mode critique`
  l.14: (blank)
  l.15: `Review the candidate $CAND_SB (sha256 of the file: $SHA) against the requirements it states, review 1 of 3. Inspect behavior and the dependencies it touches. Report concrete wrong outcomes, not a minimum number of findings. Minor findings are notes and never fail the review; list Medium and minor findings under follow-up candidates. If an input is missing or unreadable, return incomplete. Do not edit the candidate and do not start another review. State what you covered.`
  l.16: (blank)
  l.17: `First-review rules (from ~/.claude/rules/prompts/document_review_loop_prompts.md, read it first): write 'review: 1 of 3' once as the first line of the report. Grading check, for each finding before you mark it blocking: write the sentence 'An implementer who follows the stated text as written builds X, and X is wrong because Y.' Blocking needs a sentence that holds with no further assumption: two stated texts that contradict each other, a stated text that causes data loss or breaks a security or safety boundary, or a stated text that an acceptance criterion cannot pass. Grade it Medium when the sentence needs a guess that the implementer picks the worse of two readings the text allows, or when the finding is a requirement the document never states rather than a stated text that does harm. End the report with the '## Findings block' (one fenced code block with info string findings-v1, one JSON object per line: id, severity CRITICAL|MAJOR|MINOR, blocking, category contradiction|unpassable-check|data-loss|safety|missing-requirement|other, anchor = 12 to 200 chars copied exactly from the candidate, optional anchor2, refs, claim) and a final 'verdict: PASS' or 'verdict: FAIL' line. Your final reply must be the complete report text."`
  The brief, like the rules file, does not state claim <= 300 chars, refs <= 8, or the id pattern; violating lines are dropped by the merge.

## 3. Git state (2026-11-14; origin/master as of the last fetch - no fetch run here, so its freshness is UNVERIFIED)

`git log --oneline -6`:
- 4a22d7421 docs(eval): add review-panel unification hand-off report and /tmp helper scripts
- 2d06a4382 docs(eval): add batch 11, issue-by-panel tables and all-combinations issue table
- b4db265a8 docs(eval): tasklist review panel model-combination study (#346 live gateway models)
- ec259f1b7 346 claude ab experiment artifacts (#500)
- 4ab620d1f fix(pr-submit): name an Augment review whose status marker is unreadable instead of polling silently (#382, #456) (#499)
- 9163bd1c7 Merge 346Claude-integration into master (#346 review loop, @live7 panel, ccsession Tier 2b) ... (#498)

`git status -sb | head -1`: `## ironbelly/eval-tasklist-review-panel...origin/ironbelly/eval-tasklist-review-panel` (no ahead/behind -> in sync with its remote branch). `git ls-remote --heads origin ironbelly/eval-tasklist-review-panel` = 4a22d742... = local HEAD.

`git diff --stat origin/master...HEAD -- src tests`: EMPTY. The branch changes no source and no tests. Whole branch diff: 9313 files, +341,392, all under .dev/eval-workspaces/.

Commits on branch not on origin/master (3), all docs(eval), all under .dev/eval-workspaces/tasklist-review-panel/:
- b4db265a8 (2026-11-13 01:38 UTC) 8814 files +314,276: package dirs (designSpec 2050, makeTheAliasOnly 2001, design 1924 files), arms 1237, combos 1100, quarantine-pre-src-luna 417, analysis 78, tools 3.
- 2d06a4382 (2026-11-13 15:03 UTC) 445 files +25,742: package reviews (96/89/75), analysis 63, combos 61, arms 60, COMBO-REPORT.md.
- 4a22d7421 (2026-11-13 15:55 UTC) 56 files +1,374: tools/tmp-scripts (55) + .dev/eval-workspaces/tasklist-review-panel/HANDOFF-review-panel-unification.md (not opened, per independence rule).
origin/master is 11 commits ahead of the branch's base (d2d8a2d16 #519 reflect Tier 2 review panel ... 9e2608b03 #503); branch is not rebased. Note #519 "Tier 2 review panel" on master may overlap the unification topic (UNVERIFIED, not inspected).

Tracked modifications: NONE (`git status --short | grep -v '^??'` prints nothing; checked before and after the test runs).

Untracked: 3041 files, ALL under .dev/eval-workspaces/tasklist-review-panel/20261111-a1/ (none elsewhere), ~1.5 GB (du):
- 1380 `*.attempt<N>.json` (raw reviewer claude -p transcripts)
- 1352 `*.attempt<N>.meta.json` (per-attempt meta; small)
- 309 `judge.json` (blind-judge transcripts, under arms/)
By location: design pkg 851, designSpec 884, makeTheAliasOnly 869, arms 309, quarantine-pre-src-luna 128. Not gitignored (check-ignore: not ignored). Committed tree has 0 attempt*.json / judge.json.
Discrepancy: analysis/RAW-TRANSCRIPTS-NOT-COMMITTED.md says 2,916 raw files (~1.48 GB) were left out; git shows 1380 + 309 = 1689 raw transcripts plus 1352 per-attempt meta files (3041 total). The per-attempt *.meta.json files are also uncommitted although that note implies meta.json is committed (only the final <rid>.meta.json is). Exact reconciliation UNVERIFIED.
manifest.md line "Worktree branch: ... (local, never pushed)" is stale: the branch is pushed.

Summary of state:
- Committed AND pushed: all 3 eval commits (HEAD 4a22d742 on origin).
- Committed local-only: none.
- Uncommitted: 3041 untracked raw transcript/meta files (1.5 GB) in the eval dir; no tracked edits.
- CLAUDE.md rule ".dev/tasks/ is always staged" does not cover .dev/eval-workspaces; whether these raw files should be committed is an owner decision (the eval deliberately left them out).
