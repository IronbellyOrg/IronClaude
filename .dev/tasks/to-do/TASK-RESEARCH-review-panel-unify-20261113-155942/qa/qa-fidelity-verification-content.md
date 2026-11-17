# QA Report: Source-Fidelity Fix Verification, ROLE content

**Topic:** review-panel-unify (TASK-RESEARCH-review-panel-unify-20261113-155942)
**Date:** 2026-11-14
**Phase:** report-qualitative, fix-cycle verification (rf-qa-qualitative, `fix_authorization: false`)
**Fix cycle:** 1
**Report under review:** `RESEARCH-REPORT-review-panel-unification.md` (4283 lines)
**Inputs read:** `qa/qa-fidelity-consolidated-findings.md` (9 findings F4-B1 to F4-B9), `qa/qa-fidelity-fix-log.md`, the report, and the source files each finding cites (E2 via `git show 4a22d74213f93837d00c2c314075dd967b9a98e3:<path>`).

---

## Overall Verdict: PASS

## Finding-by-finding result

| Finding ID | Fixed? | Evidence |
|---|---|---|
| F4-B1 | Yes | Re-ran `uv run superclaude review panel resolve --env anthropic-only --template <t> --run-id x` with and without `--strict-distinct` for all 8 templates and listed `slot, model, fallbacks` with `jq`. Result: `t1a-1 claude-opus-5-5` has `["claude-sonnet-5-5"]` in soft `@reflect-pre`, `@reflect-post`, `@reflect-enterprise` and in both modes for `@reflect-pre-x2`, `@reflect-post-x2`; every other list is `[]` (including `@default`, `@live7`, `@reflect-lite`, and the three reflect templates under `--strict-distinct`). `review-tiers.default.json:5` (tier1a = opus, sonnet) and `:33` (anthropic-only `available`) confirm the cause. Report L1371 (C-03 evidence, still tagged `[CODE-VERIFIED by run]`, now narrowed and noting that 04 §4.1 is corrected), L562 (K-10), L632 (MS-06), L1337-1338 (C-03 Option A pros and cons), L2834 (7.3), L3430 (V-492) and L3946 (Q-02) all now say "fallbacks only on tier1a (one, sonnet)". No residual "at most one model per tier" or "every fallbacks list is empty" text (grep, 0 hits). C-03 winner A (L1171, `partial`) and Q-02 (O-2) read consistently with the corrected fact. |
| F4-B2 | Yes | `review-tiers.default.json:5-9`: tier2 = sol, glm, grok, Qwen, wonder, spark; tier2b = terra, glm, Qwen, wonder; tier3 = glm, Qwen. V-042 (L2980) now says glm-5.3 is first of the two packaged tier3 models and also tier2 (2nd of 6) and tier2b (2nd of 4); V-130 (L3068) gives Qwen3.8-max tier2 4th of 6, tier2b 3rd of 4, tier3 2nd of 2, glm tier2 2nd, tier2b 2nd, tier3 1st of 2, and says the hand-off phrase undercounts. All positions match the JSON. Grep for "only (packaged) tier3" and "glm only": the only remaining occurrences are the deliberate quotation in V-042/V-130 of the superseded or hand-off wording. |
| F4-B3 | Yes | `findings_v2.py:3-5` read: "A line that findings-v1 accepts and whose keys are all in V1_FIELDS passes check_finding unchanged. ... Prior lines are rejected." The invented quotes are gone (grep for `compatible with v1`, `v1-valid`, `the docstring claims`: no hit in the fidelity sense; "v1-compatibility" appears only as "line-level v1-compatibility claim" in DOC-02). Code evidence for the real gaps: `:147-149` (deviation_class required under reflect-post), `:279-281` (prior lines rejected), `:291-298` (empty block needs coverage observation), `:299-303` (whole-block `invalid`); `findings.py:175-186` accepts `prior` lines and has no empty-block rule. Updated places read: 2.4 table L355, MS-01 L627, DOC-02 L663 (`[STALE DOC, incomplete rather than false]`), C-01 Option A cons L1210, 6.X Option A L2559, 7.1.3 L2764, V-224 L3162, V-616 L3554, M1-01 L3643, D-02 L4108. **Premise re-examined, not reworded:** C-01 cons now says "strict subset" needs code and tests; M1-01 and 6.X Option A now require adding the block-level rules (empty block, `prior` lines, `reflect-post`) and correcting the docstring, which rests on real code gaps. The 2.4 table already listed "Empty block: valid in v1 / invalid in v2", so Sections 2, 4, 6, 7, 8 and 9 agree. |
| F4-B4 | Yes | `SKILL.md:654-655` (2 reviewers sonnet, haiku; 3 default sonnet, haiku, else opus), `SKILL.md:1248-1253` and `reflection-rubric.md:139-157` (`degraded` only when the disjoint set is empty; Example A at `:153`: reviewers {sonnet, haiku} gives `calibrator_diversity: full`; Example C: three Anthropic reviewers gives `degraded`), `reviewer-spec.md:96-97`. All nine places carry the condition: MS-16 L642, C-05 Option C cons L1496, C-06 Option A cons L1562, Section 7 point 7 L2649 (grader restated as a design note: not code, no `calibrator_diversity` field), 7.1.3 Calibration row L2774, V-151 L3089, V-511 L3449, V-580 L3518, M2-05 L3678. Grep for "always degraded" and "calibrator always": 0 hits. **Premise re-examined:** C-06 Evidence says `calibrator_diversity: degraded` changes no verdict in code, and neither C-05 nor C-06 winners rest on the degraded claim (C-06 winner stays Option B; C-05 winner B unchanged at L1173). |
| F4-B5 | Yes | E2 at 4a22d742: `combos/SPEC.md:5` ("glm-5.3 805-1435"), `:98` ("ALL glm runs removed from batch 4 (owner: massive delays) ... No glm data collected in batch 4"); `COMBO-REPORT.md:54,73` hold the "800-1800 s" and "glm pattern" text and sit above line 289, whose heading says it supersedes every earlier table and recommendation; all glm sets S33-S44 in the all-sets table are `pre-src`. Report L203 and V-042 now state the dated SPEC facts, say no source-era glm data exists, and name the superseded wording as not carried. "slow and adds nothing", "costly, no extra catches" and "excluded by owner after batch 4" are gone (grep: "adds nothing" remains only in unrelated rows and inside the explicit "not carried" notes). |
| F4-B6 | Yes | `audit-D/summary.md:18`: sonnet 446/446, terra 103/103, sol 8/8 kept; `COMBO-REPORT.md:373`: never referenced `source.md`: sonnet 1 of 63, terra 0 of 44, sol 0 of 3. Report L203 now reads "sonnet never had findings dropped at merge (446 of 446) and read source.md in 62 of 63 runs", with terra and sol also lost none, `source.md` in 44 of 44 and 3 of 3, reviews empty or incomplete. Matches V-036 and the source. |
| F4-B7 | Yes | `.dev/troubleshoot/shadow-failures-20261113014240/REPORT.md:36` ("The 0.67 mean mixes both definitions ... first-pass 1 of 3") and `research/11` line 323 (post-fix first-parse 1.0, 1.0, 0.0, 1.0, n=4; mean 0.704 over 9 runs at lines 267 and 297). V-362 (L3300) no longer says "first-pass"; it says recorded compliance mixes definitions and gives the four post-fix first-parse values with the 0.0 attributed to the heading miss fixed by `c2e3347d3` (`research/11` L318). "(mixed definitions)" is present after every 0.704: L161, V-275 L3213, V-353 L3291 (grep shows 5 mentions of 0.704, all caveated). |
| F4-B8 | Yes | `design.md:117` is `## Unattended mode`; `:124` is the Gates bullet ("There is no gate ... Under `--unattended` consent is never given"), applies only with `--unattended`; `:139` and `:149` carry the design-approval rule; `grep -c -i review design.md` = 0. Report MS-09 L635, 7.1 thin-module table L2790 (two places), V-440 L3378, M3-09 L3701, Q-55 L4189 (two places) now say `design.md` has no review or spec-panel step, `:124` is in the unattended worker section only, and the advisory default is a design choice (Q-55) and not a precedent. Grep for "matching `design", "like `design", "123-124": 0 hits. 2.5 L407 ("step 4 is self-validation with codegraph") matches `design.md:33`. **Premise re-examined:** the advisory-hook default is now explicitly an owner-decided design choice, still consistent across 7.1, 8.2 and 9.5. |
| F4-B9 | Yes | `fsm.py:1064` is `fallback_only = not any(isinstance(f.comment_id, int) for f in verified)`; `grep -c thread_id fsm.py` = 0. BL-15 L618, 7.2 L2820, V-548 L3486, M4-01 L3711 now say "a finder that supplies no integer `comment_id` is fallback-only (reply, no resolve; `fsm.py:1064`)". The three remaining `thread_id` hits (BL-18 L621, L2809, L3393) concern absent findings fields, not `fsm.py`, and are correct. |

## New-defects table

| # | Severity | Location | Issue | Required fix |
|---|---|---|---|---|
| N-1 | MINOR (note, not rechecked) | V-362 L3300 | "runs 03, 04, 09 recorded the rate after the re-ask": `research/11` L323 says run 09 was "after 2 normalize fixes", not after the re-ask; only 03 and 04 are "after re-ask". | Optional wording: "03 and 04 after the re-ask, 09 after normalize fixes". |
| N-2 | MINOR (note) | V-362 L3300, source figure | "0.67 over runs 03-07" is the troubleshoot report's figure; the recorded per-run values for 03-07 (1.0, 1.0, 0.33, 1.0, 0.333) average 0.733. The discrepancy is inherited from the source and was in the report before this fix. | Optional: cite it as the troubleshoot report's figure. |
| N-3 | MINOR (note) | 2.2 L203 | The sentence about terra and sol (empty or incomplete reviews) now appears twice in the same paragraph. | Optional de-duplication. |

No new blocking defect.

## Check-by-check against the assigned criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | Each fix resolves the distortion in every place listed and the report says what the source says | PASS | All 9 findings, every listed location read; table above. |
| 2 | Conclusions that rested on the wrong premise re-examined | PASS | F4-B3: M1-01 and 6.X Option A now rest on the three real block-level gaps. F4-B4: condition restored in all nine places; grader paragraph restated as design note; C-05/C-06 winners do not depend on it. F4-B1: Q-02 and C-03 Option A pros/cons match the run output. F4-B8: advisory default now a design choice. F4-B9: field is `comment_id` in all four places. |
| 3 | No debate winner overturned; four debates `partial`; Section 7 `[CONTRADICTION]` still raised openly | PASS | L1171 C-03 winner A partial; L1173 C-05 B partial; L1181 C-13 B narrowly partial; L1182 C-14 B partial. `[CONTRADICTION: ...]` full text at L2777 (Section 7.1.3) plus 12 echoes (L2911, 2919, 3371, 3633, 3649, 3650, 3658, 3700, 3891, 3921, 3929, 4188), identical to the fix log's list; no other `[CONTRADICTION` text. |
| 4 | Still report-only, no roadmap; parsed-sparse counts only | PASS | L7 scope note "report only; no roadmap"; Section 8 title "not a roadmap"; every parsed-sparse mention (L163, 720, 753, 1849, 2059, 2103-2120, 2637) gives counts (38 of 39, 35 of 39, 34 of 38, decisive in 0 for certain, at most 1), no rate presented as a finding. |
| 5 | Coherence across Sections 2, 6, 7, 8, 9 | PASS | Cross-read of every edited fact in each section (fallbacks 2/4/6/7/8/9; docstring 2/4/6/7/8/9; calibrator 4/6/7/8; design.md 4/7/8/9; `comment_id` 4/7/8). Table integrity spot check by script: 691 V rows all 7 columns; MS 24, DOC 71, M rows 48, K 11, BL 18 uniform. |

## Self-Audit

**(a) Reliance list:** No structural verdict was supplied; no rf-qa PASS item was relied on. The structural role is a separate agent.

**(b) Independent semantic checks:**
- Fallbacks claim: re-ran `panel resolve` for 8 templates x 2 modes and compared per-slot `fallbacks` with report L1371.
- Calibrator rule: read `SKILL.md:654-655, 1248-1253`, `reflection-rubric.md:139-157`, `reviewer-spec.md:96-97` and compared with nine report places.
- E2 claims: `git show 4a22d74...` for `combos/SPEC.md:5,98`, `COMBO-REPORT.md:54,73,289,373,467-478`, `audit-D/summary.md:18`.
- Code claims: read `findings_v2.py:1-12,140-152,276-305`, `findings.py` prior/empty grep, `fsm.py:1058-1068`, `design.md:115-150` and its review grep, `review-tiers.default.json:1-40`.
- Compliance figures: `research/11` L267, 297, 318, 323 and the troubleshoot `REPORT.md:30-40`.

Claims independently verified: about 75. Files read: the consolidated findings, fix log, report (targeted lines for 60+ locations), `findings_v2.py`, `findings.py`, `fsm.py`, `design.md`, `review-tiers.default.json`, `SKILL.md`, `reflection-rubric.md`, `reviewer-spec.md`, `research/11`, the troubleshoot REPORT, and four E2 files.

Limit: the report is untracked, so no pre-fix copy exists for a diff; I verified the post-fix state by pattern search over the whole report and by reading each listed location. Text under unusual wording elsewhere in the 4283 lines could have escaped.

**Confidence:** Verified: 14/14 checklist items (9 findings plus 5 criteria) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 5 | Grep: 2 | Glob: 0 | Bash: 22 (plus one `jq` loop and one table-integrity script run through Bash)

## Verdict

**Verdict: PASS** (0 CRITICAL, 0 IMPORTANT, 3 MINOR notes)

## QA Complete
