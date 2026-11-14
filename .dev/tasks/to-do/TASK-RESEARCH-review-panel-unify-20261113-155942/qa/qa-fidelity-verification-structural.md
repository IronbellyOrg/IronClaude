# Source-Fidelity Gate (Gate 4): Structural Verification, Cycle 1

**Task:** TASK-RESEARCH-review-panel-unify-20261113-155942
**Report checked:** `RESEARCH-REPORT-review-panel-unification.md` (4283 lines)
**Role:** structural (rf-qa, fix_authorization: false; no file edited except this report)
**Date:** 2026-11-14
**Inputs read:** `qa/qa-fidelity-consolidated-findings.md` (F4-B1 to F4-B9), `qa/qa-fidelity-fix-log.md`, the report, the cited sources (E2 via `git show 4a22d74213f93837d00c2c314075dd967b9a98e3:<path>`)

## (a) Finding by finding

| Finding ID | Fixed? | Evidence |
|---|---|---|
| F4-B1 | Yes | Re-ran `uv run superclaude review panel resolve --env anthropic-only --template <t> --run-id x` with and without `--strict-distinct` for `@default`, `@live7`, `@reflect-lite`, `@reflect-pre`, `@reflect-post`, `@reflect-enterprise`, `@reflect-pre-x2`, `@reflect-post-x2`, and listed the non-empty `fallbacks` per run (jq). Result: `t1a-1 ["claude-sonnet-5-5"]` in soft `@reflect-pre`, `@reflect-post`, `@reflect-enterprise` and in both modes for the two `-x2` templates; every other list is `[]`, including `@reflect-pre/-post/-enterprise` under `--strict-distinct`. This matches the corrected C-03 bullet (report L1371) exactly. `src/superclaude/cli/review/data/review-tiers.default.json:5` (tier1a = opus, sonnet) and `:33` (anthropic-only `available`) confirm the cause. L562 (K-10), L632 (MS-06), L1337-1338 (C-03 Option A), L2834 (7.3), L3430 (V-492), L3946 (Q-02) all now say "fallbacks only on tier1a (one, sonnet)". `[CODE-VERIFIED by run]` stays only on the narrowed statement. C-03 winner A and Q-02 unchanged. |
| F4-B2 | Yes | Packaged tiers file lines 7-9: tier2 = [sol, glm-5.3, grok, Qwen3.8-max, wonder, spark]; tier2b = [terra, glm-5.3, Qwen3.8-max, wonder]; tier3 = [glm-5.3, Qwen3.8-max]. V-042 (L2980) says glm-5.3 is first of two tier3 models, 2nd of 6 in tier2, 2nd of 4 in tier2b: true. V-130 (L3068) says Qwen3.8-max is 4th of 6, 3rd of 4, 2nd of 2 and glm 2nd, 2nd, 1st of 2: true. V-043 and Section 2.2 agree. Both rows keep 7 columns (script below). |
| F4-B3 | Yes | `findings_v2.py:1-7` read: the docstring is a line-level claim ("A line that findings-v1 accepts and whose keys are all in V1_FIELDS passes check_finding unchanged ... Prior lines are rejected."); `:147-149` requires `deviation_class` under lens `reflect-post`; `:279-283` rejects `prior`; `:291-298` is the empty-block rule; `:299-303` sets `invalid`. `findings.py:124-196` has no empty-block rule and accepts `prior` (`:175-186`). All ten places (L355, 627, 663, 1210, 2559, 2764, 3162, 3554, 3643, 4108) now state this; none quotes "compatible with v1" or "a v1-valid line passes v2 unchanged"; DOC-02 is tagged `[STALE DOC, incomplete rather than false]`; M1-01 and 6.X Option A say "add the block-level v1 rules the code lacks ... and correct the docstring". |
| F4-B4 | Yes | `SKILL.md:654-655` (2 reviewers: sonnet, haiku; 3 default: sonnet, haiku, else opus); `SKILL.md:1248-1253` and `refs/reflection-rubric.md:139-157`: `degraded` only when the disjoint set is empty; Example A (`:153`) reviewers {sonnet, haiku} gives `full`; `refs/reviewer-spec.md:96-97` same table. All nine places (L642, 1496, 1562, 2649, 2774, 3089, 3449, 3518, 3678) now carry the condition "three-reviewer default (sonnet, haiku, opus) ... `degraded`; with `--reviewers 2` ... `full`". L2649 restates the proposed grader as a design note. No "always `degraded`" left. C-05 and C-06 winners unchanged. |
| F4-B5 | Yes | E2 at 4a22d742: `combos/SPEC.md:5` has "glm-5.3 805-1435"; `:98` has "ALL glm runs removed from batch 4 (owner: massive delays)"; `COMBO-REPORT.md:54,73` carry the "800-1800 s" and glm-pattern text and sit above `:289`, whose heading "supersedes every earlier table, ranking and recommendation"; current all-sets table rows S33 to S44 (every glm set) are `pre-src`. L203 and V-042 now say exactly this and state the old wording is superseded and not carried. |
| F4-B6 | Yes | `analysis/audits/audit-D/summary.md:18` (kept/raw: sonnet 446/446, terra 103/103, sol 8/8); `COMBO-REPORT.md:373` (never referenced `source.md`: sonnet 1 of 63, terra 0 of 44, sol 0 of 3). L203 now reads "`claude-sonnet-5-5` never had findings dropped at merge (446 of 446 kept) and read `source.md` in 62 of 63 runs (terra and sol also lost none ... 44 of 44 and 3 of 3)". "Only" is gone. |
| F4-B7 | Yes | Troubleshoot `REPORT.md:36`: "The 0.67 mean mixes both definitions"; `research/11:267,297` mean 0.704 over 9 runs; `research/11:323` per-run values. V-362 (L3300) says recorded compliance mixes first-parse and after-re-ask definitions and gives the four post-fix first-parse values 1.0, 1.0, 0.0, 1.0 (n=4). "(mixed definitions)" is added at L161, V-275 (L3213) and V-353 (L3291). "first-pass compliance is still low" is gone. |
| F4-B8 | Yes | `src/superclaude/commands/design.md:117` is `## Unattended mode`; `:124` is the Gates bullet ("There is no gate, and no person-mode flag. Under `--unattended` ..."); `:139` and `:149` keep the design-approval rule; `grep -c -i review design.md` = 0. L635 (MS-09), L2790 (both places), L3378 (V-440), L3701 (M3-09), L4189 (Q-55) state the true basis and no longer use `design.md:124` as a precedent. L407 ("`design.md` step 4 is self-validation") is true (`design.md:33`). |
| F4-B9 | Yes | `src/superclaude/pr_submit/fsm.py:1064` is `fallback_only = not any(isinstance(f.comment_id, int) for f in verified)`; `grep -c thread_id fsm.py` = 0. L618 (BL-15), L2820, L3486 (V-548), L3711 (M4-01) now say "a finder that supplies no integer `comment_id` is fallback-only (reply, no resolve; `fsm.py:1064`)". The only remaining `thread_id` hits (L621, 2809, 3393) are about PR finding fields absent from findings v1/v2, which is correct. |

## (b) Old-wording grep (report, all lines)

| Pattern | Hits |
|---|---|
| `at most one model per tier`, `every .fallbacks. list is empty`, `the docstring claims`, `compatible with v1`, `always .degraded`, `null .thread_id`, `Only .claude-sonnet`, `first-pass compliance is still low`, `glm-5.3 is the only packaged tier3`, `only packaged tier3`, `v1-valid line passes`, `the rules the docstring`, `after batch 4` | 0 |
| `design.md:123` / `design.md:124` as hook precedent | 0 as precedent (the five remaining mentions say `:124` is the unattended worker section) |
| `glm only tier3` | 1 (V-130, L3068): a deliberate quotation of the hand-off wording, labelled as undercounting |
| `800-1800` | 2 (L203, V-042 L2980): deliberate quotations, each stated to be superseded and "not carried" |
| `adds nothing` | the same two quotations plus unrelated rows (L197, 1389, V-033, V-051, V-089), as the fix log said |

## (c) Structural script (a private /tmp script, run with `uv run python`, removed afterwards)

| Check | Result |
|---|---|
| Section 8.1 rows have 7 columns | 691 V rows, all 7 columns (backtick- and escaped-pipe-aware split), header has 7 columns, 691 unique ids, rows contiguous (L2939-3629) |
| Table of Contents matches headings | 72 entries, 72 level 2-3 headings after it, none missing either way, 0 slug mismatches, same order |
| Section 4 gap table is one table | One block, L586-732, 147 lines (header, separator, 145 rows), every row 5 columns; the other Section 4 tables (4.1, 4.2, 4.3) are separate blocks under their own headings |
| Section 9.1 | G-01 to G-94: 94 references, 94 unique, none missing, none repeated, none extra; Q-01 to Q-61: 61 rows, each once. The main Section 9 tables list each Q once as well (46 in the main table, Q-47 to Q-61 in 9.5) |
| `[CONTRADICTION` text | Only the Section 7.1.3 flag (L2777) and its echoes (L2911, 2919, 3371, 3633, 3649, 3650, 3658, 3700, 3891, 3921, 3929, 4188); identical to the fix log's list; V-037's old assembler flag is gone |

## (d) Regression spot-check of the report-validation fixes

| Fix | Result |
|---|---|
| P6-B1 | V-037 (L2975) reads "30 findings lost at merge (all dropped findings, not only blocking ones; E2's blocking-lost total is 49)"; 0 hits for "30 blocking findings lost"; no assembler flag. Intact |
| P6-B12 | SC-18 to SC-22 present (L542-546); M2-03 and M3-03 still reference them. Intact |
| P6-B18 | MS-24 present (L650); Section 4 gap table still 145 rows; Q-59 in 9.1 (L4056) and 9.5 (L4193). Intact |
| P6-B19 | SC-14 and 6.X Option B say "once M1 delivers exposures X1-X14"; M1-20 and M1-21 present (L3662-3663). Intact |
| P6-B34 | `plugins/superclaude/` named 5 times, including M1-11, M3-01, M3-08. Intact |
| P6-B36 | G2 split at `:277-298` (no replacement) and `:299-304` (pinned) at L3847 and L2777, 2880, 3658. Intact |

## (e) Binding facts

| Fact | Result |
|---|---|
| No debate winner changed | The four `reviews/adversarial/*/adversarial/return-contract.yaml` all say `status: "partial"`; base variants: ledger-model B (Option B), model-tier-config A, panel-size-cost B (Option B), who-judges-blocking B (Option D). The report says C-03 A, C-05 B (Option D), C-13 B, C-14 B, each `partial` (L1382, 1540, 2053, 2120, 2678-2682). Unchanged |
| E2 stays at commit 4a22d742 only | 14 full-hash and 6 short-hash mentions, all `4a22d74213f93837d00c2c314075dd967b9a98e3` / `4a22d742`; no other E2 commit |
| No roadmap | 13 "roadmap" mentions, all negations or "later roadmap" (L7, 101, 1157, 2541, 2621, 2826, 2915-2917); no roadmap content |
| Report-only scope | `git status` shows no `src/` change; only the report and the fix log are new files |

## New-defects table

| # | Severity | Location | Defect | Fix |
|---|---|---|---|---|
| 1 | MINOR (note) | `RESEARCH-REPORT-review-panel-unification.md` and `qa/qa-fidelity-fix-log.md` | `git status` shows both as untracked (`??`); `.dev/tasks/` must stay staged | `git add .dev/tasks` at the next staging step (not a fidelity defect) |
| 2 | MINOR (note) | Report L203, L2980 | The superseded phrases "adds nothing" and "800-1800 s" still appear, only as quoted, labelled-superseded text | None needed; optional to drop the quotes |
| 3 | MINOR (note) | Report L355, L663 (F4-B3 wording) | "the whole-block `invalid` state (`:299-303`)" is listed as a v2-only difference, but v1 also sets `ok: False` on any error; the difference is mainly the `state` vocabulary | Optional rewording; the finding's main points (empty-block rule, `prior` lines, `reflect-post`) are correct |
| 4 | MINOR (note) | Report L1371 | The data file is cited as `review-tiers.default.json:5,33` without its path (`src/superclaude/cli/review/data/`); the lines are correct | None needed |

No blocking defect was introduced: no broken table, header or citation, no lost required content, no changed winner.

## Summary

- Confidence: Verified: 24/24 (9 findings, 5 structural checks, 6 regression spot-checks, 4 binding facts) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement: Read: 12 | Grep: 1 | Glob: 0 | Bash: 17 (grep, sed, jq, git show, the structural script, the 16 `panel resolve` runs); no web research
- Blocking defects open: 0. Minor notes: 4.

## Verdict: PASS
