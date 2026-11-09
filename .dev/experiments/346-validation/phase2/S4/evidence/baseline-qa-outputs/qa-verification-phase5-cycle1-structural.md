# QA Report - Gate 2 Fix Verification (Phase 5, cycle 1, structural)

**Status:** Complete
**Date:** 2026-11-08
**Topic:** BMAD first-use directory creation in a project that never had BMAD
**Fix authorization:** false

---

## Inputs read

Read in full: `qa/qa-consolidated-findings-phase5.md` (8 blocking rows), `qa/qa-fix-log-phase5-cycle1.md`, `synth-03` (all 398 lines), `synth-04` (all 473 lines), `synth-02` lines 12-119 and 191-209 and line 154, `synth-01` lines 214-223, 303-314, 380-383. Code re-read for fix verification (not taken from the fix log): `templates/VSCode-AIDev02/modules.tf:78-113`, `image/Dockerfile.coder:128-147`, `image/catalogue/bmad/manifest.yaml:1-30`, `image/catalogue/bmad/install.sh:1-62`, `/opt/nvm/.../bmad-method/tools/installer/ui.js:222-266`, `installer.js:1233` (Grep), `src/scripts/resolve_config.py:156` (Grep).

## (a) Blocking findings 1-8: was each addressed at the cited location?

| # | Finding | Result | Evidence |
|---|---|---|---|
| 1 | F-04 manual command unguarded | FIXED | synth-04 step 2.2 (line 62) carries the condition "run this only in a project that has no `_bmad/` and no `.claude/skills/bmad-*`; if `_bmad/` already exists ... updates it", and says it is wording, not a guard; gap map F-04 row (line 28) names steps 2.2 and 2.5; synth-02 F-04 (line 110) and SC-07 (line 69) say the manual command is closed by wording only. `manifest.yaml:14` re-read: the literal command is unguarded, so the claim is true. |
| 2 | `orca_retirement` "removes only" | FIXED | `modules.tf:101-106` re-read: 102-104 `rm -f` links on exact readlink match, 105 is an unconditional `rm -rf`. synth-01:220, synth-04 4B.5 (150), 7.3 (263), (v)(3) 4B row (301) now cite 101-104 as the precedent and name line 105 as unconditional. Grep over `synthesis/` for "removes only", "remove only", "only removes": 0 hits. synth-01:173 and synth-04 row 7 make no "only" claim. |
| 3 | "pure exec stand-in" comment | FIXED | `Dockerfile.coder:133-135` re-read: comment is about `#!/usr/bin/env node` and NVM node, not "pure exec stand-in". Grep "pure exec", "stand-in": 0 hits. synth-03:142 and synth-04 4C.1 (157) now quote the real reason. (synth-03:123 "today a pure `exec`" is a description of the wrapper body at `Dockerfile.coder:142`, true.) |
| 4 | Welcome text "unconditional" | FIXED | `manifest.yaml:12-13` re-read: sentence is conditional on a seed. synth-01:146, synth-02 F-09 (115) and CC-12 (171), synth-03:86, synth-04 step 2.5 (65) all restate the defect as "not conditional on the install guards (`install.sh:22-25`) or a failed install (`install.sh:41-46`)", both line ranges re-read and correct; step 2.5 gives a concrete rewording. Grep "without a seed", "unconditional": no claim that the sentence is unconditional. |
| 5 | Option F listed as a certain break | FIXED | Grep for E/F break lists: synth-01:312, 382, 476, synth-02:68, 80, 112, synth-04:180 and Table 5.1 row `test-57:450` (196) all say F has no code path and its X cells are void (G-25); E is conditional on running from `install.sh`. synth-03 Table 1 F column (261) agrees. No remaining list names F as a certain break. |
| 6 | Option C for the CLI reading | FIXED (with residual wording, see N1, N2) | synth-03:130, 321, 335, 364 and synth-04 branch table (134), 4C.2 (158), Section 9 row 2 (344) all say: the existing `bmad install` satisfies the CLI reading, recommendation is Stage 0 only, C only for a new separately named command, no `status`/`uninstall` interception. 4C.2 gives the reason (`bmad uninstall` would install then uninstall). |
| 7 | Q2(b) mapped to a mechanism the plan cannot give | FIXED | synth-02:32 and 198, synth-03:313-314, 352, 362-366, synth-04:15, 123 (3.6), 135, 344, 345 now say "named bootstrap skill", state that a literal `/bmad-*` name needs a user-level `bmad-*` artifact that step 3.6 forbids, and make it an owner choice in Section 9 rows 2 and 3. |
| 8 | Section 7 says D-1, D-2 decided | FIXED | synth-03:320 now reads "plan defaults, not settled decisions" for D-1, D-2, D-3, D-10 and points to Section 9 rows 10, 6, 5; synth-04 step 3.2 cond. 2 (119), 3.3 (120), row 10 (352) agree (bare `_bmad/` existence, no atomic step, report not repair). I re-read rows 5, 6, 10: they are open owner questions with plan defaults, so the deviation from the proposed wording (D-3 and D-10 also defaults) is evidence-based and correct. |

## (b) New blocking issues introduced by the fixes

Checked for: new fabricated claims, document-only claims in Sections 2, 6, 7, 8, broken tables, placeholders, hallucinated paths, lost sections. Result: none found. New citations in the changed text (`modules.tf:101-105`, `Dockerfile.coder:133-135, 139, 142`, `manifest.yaml:12-14`, `install.sh:22-25, 41-46`, `ui.js:233-262`, `installer.js:1233`, `resolve_config.py:156`) were each re-opened and match. `ui.js:233-262` shows quick-update is offered only when `existingInstall.installed` (else `update`), which supports the existing MINOR row 12 and does not contradict the new text of step 3.2 (a tree with `core/` counts as installed per the research).

Notes (all MINOR, not blocking, not rechecked in later cycles unless the orchestrator wishes):

| # | Severity | Location | Issue | Suggested fix |
|---|---|---|---|---|
| N1 | MINOR | synth-04 step 4C.1 (line 157) and 4C.4 (line 160) | New 4C.1 text (written in this cycle for finding 3) says the wrapper "now also runs the first-use block for the chosen subcommands", and 4C.4 says "acting only on the chosen subcommands or the new name"; 4C.2 says no existing subcommand is intercepted, only a new name. The phrase reintroduces the concept finding 6 removed. | Replace "the chosen subcommands" with "the new command name" in both places. |
| N2 | MINOR | synth-02 section 3.1 row 1 (line 31) and 4.4 Q2 row (line 198) | Reading (a) is still described as "image wrapper evaluates the predicate, then installs (C)"; Sections 6 to 8 now say the existing `bmad install` already satisfies it and C adds only a new command name. Wording drift between sections, no false fact. | Align row 1 with synth-03:364. |
| N3 | MINOR | synth-04 step 2.5 (line 65) | Quotes the manual-command condition as "only in a repo that has no `_bmad/`", while step 2.2 and the F-04 map row also require no `.claude/skills/bmad-*`. | Quote the full condition from step 2.2. |
| N4 | MINOR | synth-03 lines 339-340 | No blank line between the "Prior positions overridden" paragraph and `### Feasibility statement` heading. | Insert a blank line. |

## (c) Section-to-file mapping

Headings re-listed with Grep: synth-01 holds `## 1. Problem Statement` (line 10) and `## 2. Current State Analysis` (26) with 2.1-2.6; synth-02 holds `## 3. Target State` (12), `## 4. Gap Analysis` (99), `## 5. External Research Findings` (232); synth-03 holds `## 6. Options Analysis` (11) and `## 7. Recommendation` (301); synth-04 holds `## 8. Implementation Plan` (13), `## 9. Open Questions` (337), `## 10. Evidence Trail` (398). Mapping intact; no section lost, no placeholder text found in the files read.

## Self-Audit

What I actively checked, with tools: Read of the consolidated findings, the fix log, synth-03 and synth-04 end to end, and the changed regions of synth-01 and synth-02; Read of `modules.tf`, `Dockerfile.coder`, `manifest.yaml`, `install.sh`, and `ui.js` (222-266); Grep for the false phrases of findings 2, 3, 4 ("removes only", "pure exec", "stand-in", "unconditional", "without a seed": the remaining hits are legitimate, for example the `sc-` stale removal and `specstory-cleanup`), for F in certain-break lists, for the status/uninstall interception, for "chosen subcommands", for `option C` in synth-02, and a heading Grep for the section mapping. I reproduced the premise of each blocking finding in code first (the `rm -rf` at `modules.tf:105`, the comment text, the conditional welcome sentence, the unguarded command at `manifest.yaml:14`), then traced each changed claim in the synth files to it.

Why 0 blocking issues and 4 MINOR notes is credible: all 8 rows were confirmed fixed at the cited lines and at the secondary places the fix log claims; I looked specifically for leftovers of the fixed claims and found only the wording drifts N1 to N4, which I rate MINOR because none states a false fact or a wrong plan action (4C.2 is explicit about what the wrapper acts on).

UNVERIFIED by me: `existing-install.js:111`, `ui.js:226-262` beyond the lines read, `test-19`, `test-57`, `test-startup-boot` line citations, `image/bin/specstory-cleanup` behaviour, all web-01 and web-02 claims (doc-only, not rechecked), and the research files (not opened; the changed claims were traced to code, not to research text). Per-file numbers in rows I did not touch were not re-derived. Tool engagement: Read 21 | Grep 9 | Glob 1 | Bash 0 (Read+Grep+Glob = 31 >= 8 blocking checks plus 3 sub-checks).

Confidence: Verified: 11 / 11 checks (8 blocking rows, new-issue scan, mapping, new-citation check) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% for the stated scope (research-file tracing and doc-only claims are outside the scope of this check and listed above).

## Verdict

**VERDICT: PASS**

Counts: blocking findings fixed 8 / 8; unfixed blocking 0; new blocking issues 0; CRITICAL 0, IMPORTANT 0, MINOR 4 (N1 to N4, notes only).

## QA Complete
