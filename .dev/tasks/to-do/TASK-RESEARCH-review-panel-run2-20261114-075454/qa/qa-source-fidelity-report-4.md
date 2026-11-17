# QA Report - Source-Document Fidelity (Agent 4: E3 variants, consumers and repository constraints)

**Report reviewed:** `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/RESEARCH-REPORT-review-panel-unification-run2.md`
**Topic:** one unified central Review Panel (shared core plus thin modules) from E1, E2 and E3 (run 2, report only)
**Phase:** source-fidelity (Gate 4, fidelity agent 4)
**Grading:** `qa/grading-override.md` applies (blocking only for decision-bearing defects, missing deliverables, safety risk)
**Assigned sources:** spec-panel.md, document_review_loop_prompts.md, installed variants (sc-review-ledger, sc-spec-panel-stoprule-protocol, sc-diffgate, sc-fix-audit, finding-grader, spec-panel-{ledger,stoprule,diffgate,ponytail,armb}), phase5 experiments, 346 research files, consumers (workflow, tasklist, brainstorm, design, pr_submit, auggie-review, rf-qa family, cli/tasklist), repo rules (CLAUDE.md, Makefile, plugins/superclaude, dual-surface test), research files 11-14 and 18.
**Date:** 2026-11-14
**Status:** Complete

---

## Source-Document Fidelity Report

**Report reviewed:** `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/RESEARCH-REPORT-review-panel-unification-run2.md` (5,098 lines; read in full for sections 2.4, 2.7, 2.8, 3.1-3.4, 6.10, 6.11 and the C8-C10 constraint rows; the value inventory (Appendix A, 5,950 rows) is outside this agent's sources and was not read)
**Source files checked:** about 60 files (the assigned shipped files, 17 installed variant files, 4 variant scripts read at the cited lines, phase5 and 346 research docs, consumer and agent files, repository rules, 9 test files, research files 14 and 18 read in full, 11 to 13 by their claims in the report), about 14,000 lines read or searched
**Date:** 2026-11-14

### Claims verified against source (phantom-claim sweep, 48 claims; each by Read, Grep, or one read-only batch script)

| # | Claim in the report | Source checked | Result |
|---|---|---|---|
| 1 | `spec-panel.md` `## Review Loop` at 256, seven bullets 258-264, hard gate 266-268; each bullet's content | `src/superclaude/commands/spec-panel.md:254-268` | exact |
| 2 | prompts file 74 lines; placeholders 15-21; grading sentence 31; `findings-v1`/`fixmap-v1` 56-66; verdict sentences 62 and 70; anti-inflation 74 | `document_review_loop_prompts.md` read whole | exact |
| 3 | plugin `spec-panel.md` differs by 18 changed lines; Review Loop bullets identical; hard gate EXTENDED with `${CLAUDE_PLUGIN_ROOT}`; rules file byte-identical | `diff`, `cmp`, `plugins/.../spec-panel.md:266` | exact (the 18 lines split 1+1+2+2+12 as the report lists) |
| 4 | five installed commands, agent `finding-grader.md` 35 lines, four skill dirs; script sizes 2,668 / 2,050 / 1,740 / 1,131 = 7,589 | `wc -l`, `ls` | exact |
| 5 | 17 installed files listed in the install log; none in `src`, `.claude/commands/sc`, or `.claude/skills` | install-log.md table (17 rows), `ls` | exact |
| 6 | `install_commands.py:41-79` iterates package `*.md` only; `install_skills.py:88-115` iterates package skills, removes only package skills that have a command | read both | exact; the variants are neither installed nor removed |
| 7 | variant scripts contain no `superclaude`, `cli.review`, `review panel`; no `findings-v1`, `fixmap-v1`, `review-ledger/1`, `resolved_check` in the four skill folders or five commands | Grep count: 0 matches both ways | exact |
| 8 | only stoprule has `## Activation` (l.12); ledger refuses standalone `--unattended` (l.256); stoprule has no `## Unattended mode` (l.18); no `follow-up candidates` or hard gate in any variant command | Grep over the five commands | exact |
| 9 | ARM B = 472-line PR 427 text with only the `name:` line renamed; sha prefix `c8d80346a96cb528` | `diff` vs `provenance/spec-panel-427.md`, `sha256sum`, DESIGN-BRIEF.md:9 | exact (the prefix belongs to the 427 text, not to the armb file) |
| 10 | `CAP_REVIEWS = 3` in ledger (l.35) and diffgate (l.23); `MERGE_GAP = 2`, `VIA_CAP = 2` | Grep | exact |
| 11 | diffgate: FAIL if any open blocking row (l.796); silence keeps a prior blocker open (754-760) | read | exact |
| 12 | stoprule `compute_verdict` at 1162; `cmd_verify_transcript` returns `EXIT_OK` in every branch including `grader-integrity: mismatch` (1793-1815); a saved output records `mismatch` | read, Grep of `runtime/s1v/stoprule-r1-integrity.txt` | exact |
| 13 | ledger `SKILL.md:84` (sweep after every terminal decision) and `:117` (`headline_raw = U3 + W + O`, owner rule) | read | exact |
| 14 | ledger statuses `open, fixed, verified, reopened, deferred` (l.508); `_blocking_spec_panel` at 41 | Grep | exact |
| 15 | `fix_audit.py` write order 877 before 898-903; no-prior-rows path at 1028; `ponytail:ponytail-review` dependency | read | defects as described; the dependency has a fallback (finding 5) |
| 16 | `FINAL-REPORT.md:42` "Convergence not proven; no validated winner"; start spec 57,763 bytes; 63,717 / 70,488 / 70,565 bytes; 10.31 / 22.03 / 22.16 percent; 91-byte audit | Grep and read | exact |
| 17 | stale rows: `FINAL-REPORT.md:6`, `:54-55`, `:219`; `coordinator-log.md:45` "all variants gained Activation"; `live7.md:3` names branch `346Claude-ab-experiment-artifacts` | read | exact; only stoprule has the heading (claim 8) |
| 18 | `FINAL-RESULTS.md:21` (all p at least 0.38) and `:24` (PN1, ab3, ab4 p 0.003 / 0.022 / 0.027; no design converges); `p17/LEDGER-RESULTS.md` table | read | exact (see finding 6 on "not reconciled") |
| 19 | `346-plan-merged.md:117` and `:202` ("A2 replaces it"); `SNAPSHOT-STATE.txt:3` API429 and no completed design | read | exact |
| 20 | `review-panel-live7.md` 15.7/15.3 vs 19.3/17.7, pooled +3.0 p = 0.013, second batch +2.3 p = 0.17; `p19/rep/RESULTS.md:41-44` | read | exact |
| 21 | workflow SKILL.md 107 lines; Wave 4 at 85-93 (call at 89, unattended variant 91, advisory rule 93), "Will" line 105; contract keys and enum | read | exact |
| 22 | tasklist: T1 20 checks (1279-1290); Stage 7 five dimensions and `split = ceil(task_count / 2)` (1356, 1378-1382); synthetic-dnsp branch (1427-1431); P2 loop cap, monotonicity and halt strings (1604-1615); Stage 10.5 (1619-1646) with "non-blocking" (1640) and "advisory-blocking" (1646) | read | exact except findings 2-4 |
| 23 | tasklist severity High / Medium / Low at 1386; `SKILL.md:226` is the one `tasklist validate` mention | read | exact |
| 24 | `cli/tasklist`: step `tasklist-fidelity`, 600 s, `retry_limit=1`; gate only on `high_severity_count`; `medium_severity_count` required | `executor.py:172-183`, `gates.py:25-38` | exact |
| 25 | `pr_submit`: 6,511 lines in 12 modules plus `contract_setup/`; `is_groundable` (`fsm.py:364-372`); `Severity` 5 tiers (`models.py:106-113`); 18 categories (`severity_router.py:34-53`); `DEFAULT_MAX_ROUNDS = 2`, `HARD_CAP_MAX_ROUNDS = 5` defined in both `fsm.py:32-33` and `loop_guard.py:19-20`; no import of `cli/review` | read, Grep, `wc -l` | exact |
| 26 | `merge_guard` triggers on a verified Medium-or-higher finding; pr-submit must run in the main session (`SKILL.md:47-49`) | read | exact |
| 27 | auggie-review 402 lines; hallucination contract at `:22`; `auggie-reviewer` `model: opus`; `--revagent` native aliases; `reflect_status` read at `:348` | read, Grep | exact |
| 28 | rf-qa 551, qualitative 1,154, analyst 428 lines; `permissionMode: bypassPermissions` on all three (l.5); rf-qa 5 phases; qualitative 8 document types plus fix cycle; analyst 5 analysis types; confidence formula and 95 percent gate; `[HALT-MONOTONICITY] |F|=<n>` | Grep of headings and lines | exact |
| 29 | `/task` gate: floors 6 / 8 / 10 / 12 by output size; lens agents spawned with `bypassPermissions` and `fix_authorization: false`; one fix agent; verification round | `task/SKILL.md:196-256` | exact |
| 30 | 44 structured `subagent_type: rf-*` lines in 8 SKILL.md files; `synthetic-dnsp` defined in 5 files and 30 lines (rf-analyst 5, rf-qa 3, qualitative 2, tasklist 9, task-builder 11) | Grep counts | exact |
| 31 | swarm lens registry 9 entries with `custom` placeholder; `LensEntry` fields; no `/sc:code-review` command file | read, `ls` | exact |
| 32 | brainstorm default models `opus,sonnet,haiku`; adversarial PASS at least 0.65, PARTIAL at least 0.50; design has no skill and a self-check Validate step; plugin design differs by 57 lines, brainstorm by 16; plugin brainstorm command points to a skill the plugin does not ship | Grep, `diff`, `ls` | exact |
| 33 | plugin: 125 tracked files; 4 skills; no rf-*, reflect-reviewer, auggie-reviewer, evidence-validator agent; 28 commands; `pyproject.toml:78-87`; build script copies `rules/` | `git ls-files`, `ls`, read | exact |
| 34 | `CLAUDE.md` lines 16-18, 31, 35-37, 39-78, 80-100, 292-299, 303-344 (rule 307-317, link flags 315) say what the report says | read, Grep | exact |
| 35 | `.claude/` tracks two files (`cache/sc-recommend-lookup.yaml`, `settings.json`) against `CLAUDE.md:18` and `sync-discipline.md:42` | `git ls-files .claude` | exact |
| 36 | `Makefile:549` prints "6 of 10 checks"; `.pre-commit-config.yaml` has `block-claude-generated-mirrors` and no `verify-sync` hook (only a comment); `pyproject.toml:54` ruff `==0.15.20`; `.gitignore:127-128` and `83-85`; `launch-level-guard.sh:74-77`; `test_pre_pr_checks.py:34-38, 80-83` | read | exact |
| 37 | no `integration` branch (only remote `346Claude-integration` and `346GPT-integration`); remote is only `origin` = the fork; CI lists `integration` (`test.yml:4-7`) | `git for-each-ref`, `git remote -v`, read | exact |
| 38 | `docs/designs/spec-panel-review-loop.md:3` "Design only (nothing implemented)" against the shipped loop | read | exact |
| 39 | reflect `--t2-engine panel` rejected (`SKILL.md:87, 309-311`); `§9.3` row at 1001 lists fields absent from the tasklist skill | read, Grep (no match in tasklist skill) | exact |
| 40 | workflow and tasklist pins: `test_workflow_command.py:243-261`, `test_tasklist_cli.py:573-580`; Python importers `cli/main.py:568`, three E1 scripts | read, Grep | exact |
| 41 | `tests/skills/test_primitive_dual_surface_lookup.py:28-62`; the nine named test files exist | read, `ls` | exact |
| 42 | `sc-implement-protocol/refs/qa.md`: severity derived from four yes/no answers; 5-attempt ladder, `E-HALT-QA`; `pragmatic.md:224-231` binary rule and the `/sc:implement` exemption | read | exact |
| 43 | branch ref rule observation (scratch repositories, exact `fatal: cannot lock ref` text, both orders, dash sibling coexists) | R18 section 3 read in full; the report quotes it correctly; the consequence (valid layouts) sits in conflict row CO-34 | exact (the test itself is not re-run: no git write allowed) |
| 44 | R14 conclusions in 2.4B and 6.10 (value classes c1-c6, option effort and risk notes, shadowing D9) match R14 sections 3, 4, 7 | R14 read in full | exact |
| 45 | `final-bundle/runtime/s1v/stoprule-r1-integrity.txt` records `grader-integrity: mismatch (B2#1, B1#1 ...)` | Grep | exact |
| 46 | `4115f2a979800af8` is the 486-line master text, not the 472-line PR 427 text | install-log.md:2 plus R14 3.1 | consistent (the `.bak` file was not re-hashed) |
| 47 | installed `spec-panel.md` equals the `src` text (490 lines both) | `wc -l`, sha256 | consistent |
| 48 | forbidden-upstream rule: no push, fetch, pull, PR or Orca link flag; fallback `gh pr create --repo ... --base master` | `CLAUDE.md:39-78, 315`; report row C9, C10 | exact |

Not re-verified by this agent (reliance on R14 or outside my sources; counted as UNVERIFIABLE): the three model-change counts from surviving session transcripts (17 opus / 3 synthetic / 120 sol; 47 / 43; 102 / 0), the six control `metrics.json` figures (the files do not exist), the pooled p = 0.013 source data, the 175 prose spawn lines (247 total) and the 23 rf-qa test files, the `git show` content of the E2 tip (`HANDOFF-review-panel-unification-run2.md` lines 301, 436, 457), and the six E2 audit counts of 2.8 B.

### Fidelity Findings

All findings below are MINOR under the grading override (`(minor under grading override)`): none changes a decision, a recommendation, a conflict-log outcome, a value-inventory destination or a number the recommendation rests on, and none is a missing deliverable or a safety risk. The Severity column is an information label only.

| # | Type | Source file | Report section | Finding | Severity |
|---|---|---|---|---|---|
| 1 | Distorted | `p19/roi/ROI-OF-EXTRA-REVIEWS.md:18`; R14 section 4 s4 and key takeaway; `p19/rep/RESULTS.md:44` | 2.4 C, last bullet (line 468) | The report says "the only measured positive effect of extra reviewers (doubled Haiku, about +2.7 fixes of 44) is a model with independence assumptions". The +2.7 is the ROI capture model; the measured effect is the pooled +3.0 (p = 0.013, actual runs with Haiku stand-ins) that the report itself quotes two bullets earlier (line 467). The sentence merges the two and reads as if the measured result were only a model. The correct form is in gap row G-110 (line 1345: "doubled-Haiku +2.7 fixes is a model"). (minor under grading override) | IMPORTANT label, MINOR under override |
| 2 | Inaccurate | `sc-tasklist-protocol/SKILL.md:1171, 1179` | 2.7 consumer map, T5 row | The row says the terminal task also fails at exit 0 on "subrun `partial` / `failed`, convergence below 0.80". The source fails it on `adversarial_subrun_status` partial or failed, and on convergence below 0.80 only when `tier_reached == 2` and the score is present; it also says worst-of `subrun_status` never fails the gate. The qualifier is dropped. K-2 and SC-17 state the 0.80 rule correctly and no decision uses the row. (minor under grading override) | MINOR |
| 3 | Missing | `sc-tasklist-protocol/SKILL.md:1685-1686` (and table 1677-1681) | 2.7 consumer map, T4 row | The depth rule lists score bands only. The source also forces `--depth deep --tier 2` when `n_cpo >= 1` or `n_strict >= 2`, skips reflect when `n_tasks == 0`, and sets `--tier auto` for the 4-9 band. This matters for GQ-140 (how many Stage 10.5 phases reach Tier 2), which the report already lists as not verified. (minor under grading override) | MINOR |
| 4 | Missing | `sc-workflow-protocol/SKILL.md:87` | 2.7 consumer map, Wave 4 row | Wave 4 also has an advisory codegraph Pre-check written to `<pkg>/artifacts/codegraph-grounding.md`; the row names only the reflect call. It is not a panel path, so the "reaches the panel? no" conclusion holds. (minor under grading override) | MINOR |
| 5 | Inaccurate | `~/.claude/skills/sc-fix-audit/SKILL.md:23`, `refs/auditor-brief.md:10` | 2.4 B (end of the variants paragraph), 6.10 Option 2 cons | "depends on the external plugin skill `ponytail:ponytail-review`" omits that the skill and the brief carry an `auditor: inline-rubric` fallback when the skill cannot be loaded. The dependency is soft. The 6.10 axis is already UNDECIDABLE-BY-EVIDENCE (owner decision), so no outcome changes. (minor under grading override) | MINOR |
| 6 | Distorted | `FINAL-RESULTS.md:24` | 2.4 C (line 467) | The report says R14 "does not reconcile" the two statements (all p at least 0.38 vs PN1, ab3, ab4 significant). The source's own update paragraph gives the reason: a frozen audit samples about 7 percent of the blocking defects, so the audit scores cannot separate the designs, and the 44-defect ledger rescoring can. Both statements are quoted correctly; the omitted explanation makes a resolved instrument change look like an open contradiction. G-110 already notes the circularity of the ledger. (minor under grading override) | MINOR |
| 7 | Inaccurate | `tests/pr_submit/`; repo-wide `git grep` for `t2-engine` | 2.7 consumer map (T-rows, "8 files"), 3.3 SC-26, 6.11 Option 2 | "50 `tests/pr_submit/` files" is not reproducible: 49 `.py` files (47 `test_*.py`) and 91 files with fixtures. "Grep of `t2-engine` finds 8 files": 5 files under `src`, `tests`, `docs`, `scripts`, `plugins`; many more under `.dev/`. The conclusions (many pins; no workflow or tasklist file mentions it) hold. (minor under grading override) | MINOR |

No Phantom finding. No finding of an aspirational claim: the future PR-review and rf-qa modules appear only as blockers, options and "exposure" (2.7 table, 6.11, 3.1 T-5 "kept unblocked"); the plugin Wave 4 consequence is labelled an inference "not executed".

### Checklist results

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Semantic coverage: every major E3 variant idea, consumer behaviour, severity vocabulary and repository constraint of the sources has an accurate finding | PASS | variants (2.4 B, 6.10, the six values); consumers (2.7 map plus 7 vocabularies and blockers); repo rules (2.8 E, K-4 to K-9, C8-C10); R14 sections 3, 4, 7, R18 sections 1-9 all traced |
| 2 | Detail preservation: line anchors, counts (17 files, 7,589 lines, 18 changed lines, 148 lines in 56 files), caps (3 reviews, 2 cycles, 2 vs 5 rounds), tiers (5 PR tiers, 18 categories), the ref-constraint text | PASS | claims 1-48 |
| 3 | Phantom finding detection: at least 20 claims verified in the cited files | PASS | 48 claims, zero phantom |
| 4 | Accuracy of characterization (installed-only and archives; tasklist advisory or blocking; fork-only rule) | PASS with notes | variants only installed and in two archive trees (claims 5-7); tasklist blocking in T1, T3, advisory in T4 and Wave 4 as the code says (claims 21-23); fork-only rule exact (claim 48); findings 1, 2, 3, 5, 6 are imprecisions |
| 5 | No aspirational claims | PASS | see the note under the findings table |

### Summary

- Source files checked: about 60 files, about 14,000 lines read or searched.
- Claims verified: 48 verified against source (46 exact, 2 consistent), 0 phantom; UNVERIFIABLE by this agent: 6 groups, listed above.
- Fidelity issues: 7, all MINOR under the grading override; blocking findings under the override: 0.
- Confidence: Verified: 48/54 | Unverifiable: 6 | Unchecked: 0 | Confidence: 100.0% of the checkable items (48 / (54 - 6)).
- Tool engagement: Read: 27 | Grep: 25 | Glob: 0 | Bash: 10 (read-only; seven of them one batch script each under the policy) | no web research (tavily_search: 0, tavily_extract: 0, web_search_fallback: 0, web_fetch_fallback: 0).
- Verdict: **PASS** (zero blocking findings under the override; 7 minor notes for the follow-up list).

Status: Complete
