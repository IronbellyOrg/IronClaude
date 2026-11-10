# QA Report - Gate 2 Synthesis Content Verification After Fixes (Phase 5, Fix Cycle 1)

**Status:** Complete
**Date:** 2026-11-08
**Topic:** BMAD first-use directory creation in a project that never had BMAD
**Phase:** fix-cycle (task-qualitative / report-qualitative), fix_authorization: false

---

## Check (a): the 8 Blocking = yes findings, resolved by substance or by wording?

Method: read the consolidated findings (31 rows, BLOCKING_COUNT 8) and the fix log in full, then re-read the product code and the edited synth lines for each finding. Product files re-read this session: `modules.tf:78-109`, `catalogue/bmad/manifest.yaml:1-30`, `catalogue/bmad/install.sh:1-62`, `Dockerfile.coder:128-147`, and (read-only evidence) `/opt/nvm/versions/node/v24.22.2/lib/node_modules/bmad-method/tools/installer/ui.js:222-267`.

| # | Finding | Result | Evidence |
|---|---|---|---|
| 1 | F-04 unguarded manual command | RESOLVED (substance: condition added to steps 2.2 and 2.5, map row names them, SC-07 says "new mechanism only") | synth-04:28, :62, :65; synth-02:69 and :110. Matches `manifest.yaml:12-14` (command has no guard) and `ui.js:233-262` (`--yes` goes to quick-update when installed, no version test in that block). The fix is honest that it is wording, not a technical guard. |
| 2 | `orca_retirement` "removes only" | RESOLVED | synth-01:220, synth-04:150, :263, :301 now cite `modules.tf:101-104` for the conditional link removal and name line 105 as the unconditional `rm -rf`. Matches `modules.tf:101-106` as read. No "removes only" text remains. |
| 3 | "pure exec stand-in" comment | RESOLVED | synth-03:142 and synth-04:157 now quote what `Dockerfile.coder:133-135` says (file not symlink, NVM node not on PATH). Matches the code as read. Grep over `synthesis/` for "pure exec|stand-in" finds no match; synth-03:123 "today a pure `exec`" is accurate (`Dockerfile.coder:142`). |
| 4 | Welcome text called unconditional | RESOLVED | synth-01:146, synth-02:115 and :171, synth-03:86, synth-04:65 now say conditional on a seed but not on the install guards (`install.sh:22-25`) or a failed install (`install.sh:42-46`). Matches `manifest.yaml:12-13` and `install.sh`. Step 2.5 now gives a concrete rewording. Grep for "unconditional|without a seed" finds only synth-02:206 (D-12, a different meaning: a stub written with no seed). |
| 5 | Option F listed as certain break | RESOLVED | synth-01:312, :476, :488; synth-02:68, :80, :112, :149; synth-04:180, :196 now keep E conditional and say F has no code path (G-25). synth-03 Table 1 F column agrees (:261). No remaining certain-break list includes F. |
| 6 | Option C for the CLI reading | PARTLY RESOLVED, see N-1, N-2, N-3 | synth-03:130, :321, :335, :364 and synth-04:134, :158, :344 now say Stage 0 only and no `status`/`uninstall` interception. But the fix left synth-02 stale and left plan steps and the gap map assuming a shipped block under every reading. |
| 7 | Q2(b) "BMAD slash skill" | RESOLVED, with one wording note (M-1) | synth-02:32, synth-03:313-314, :352, :365, synth-04:123, :135, :344-345 now say a named bootstrap skill, state that a literal `/bmad-*` needs a user-level `bmad-*` artifact that step 3.6 forbids, and make it an explicit owner choice. Q1 and Q2 remain unanswered. |
| 8 | Section 7 says D-1/D-2 decided | RESOLVED | synth-03:320 now says "plan defaults, not settled decisions" for D-1, D-2, D-3, D-10 and points to rows 10, 6, 5. synth-04:119, :120, :352 agree (bare `_bmad` existence, no atomic step, owner open). The deviation from the proposed wording (D-3 and D-10 also open) is correct: synth-04:121 and :348 show them owner-open. |

---

## Check (b): fixes did not overclaim and did not leave recommendation, plan and gap table inconsistent

Result: FAIL. Fixes 1 to 5, 7 and 8 added no claim stronger than their evidence (each states "wording only", "plan default", "doc-only" or "UNVERIFIED" where that applies). Fix 6 made a real decision change (CLI reading now ends at Stage 0) and did not carry it through. Three new or residual issues:

- **N-1 (IMPORTANT, blocking). synth-02 still maps the CLI reading to a wrapper that installs.** `synth-02-target-gaps-external.md:31` (section 3.1 reading table): "The user runs a `bmad` CLI command | image wrapper `/usr/local/bin/bmad` evaluates the predicate, then installs | C". `synth-02:198` (Owner Q2 row): "a `bmad` command (C)". synth-03:130 and :362 and synth-04:134, :158, :344 now say the wrapper must pass `install` unchanged and the CLI reading is satisfied by the existing `bmad install` (Stage 0 only). The fix log for finding 6 lists only synth-03 and synth-04; synth-02 was not edited for it (it was edited for finding 7 on the same table, line 32, which makes the stale line 31 sit directly above the corrected line). Required fix: reword synth-02:31 to "the existing `bmad install` already creates the directories; C only for a new, separately named command" and synth-02:198 to match (Option C only for a new command name).
- **N-2 (IMPORTANT, blocking). Plan and gap table still assume a shipped first-use block under every reading.** Under the CLI reading the recommendation (synth-03:321, :364; synth-04:15, :19, :134) builds no Phase 4 branch, so no first-use block is ever shipped. But: the gap-to-step map (`synth-04:25`) closes F-01 (rated Critical, synth-02:107) only through "Phase 4 (4B, 4C or 4D)"; Phase 3 steps 3.1 to 3.6 are "embedded in the Phase 4 block (no file of its own)" (:118-123); step 5.3 (`synth-04:186`) is "all branches" and extracts "the shipped text" of that block; Integration Checklist :319 and :327 require the block and the cases (a) to (g) unconditionally. Under the CLI reading none of these has a target, and F-01 has no closing step. Required fix: state once, in the Plan basis and the gap map, what F-01 is under the CLI reading (closed by the existing `bmad install`, owner to confirm in row 2), and mark Phase 3 steps 3.1 to 3.6, steps 5.2 to 5.4 and checklist lines :319, :327, :328 as applying only when a Phase 4 branch is built.
- **N-3 (IMPORTANT, blocking). Recommendation contradicts itself on whether Stage 0 / Option A satisfies the decision.** `synth-03:330` (Rationale 1): "The decision asks for creation on first use, so A alone fails it"; `synth-03:86` (Option A Cons): "Creates nothing on first use, so it does not satisfy the 2026-11-07 decision". But for the CLI reading `synth-03:364` and `synth-04:344` recommend "Stage 0 only" (the documentation half of A plus records) because the existing `bmad install` "already satisfies" first use, and the Section 7 diagram (`synth-03:310-312`) lists "user types the documented command: A" and "(1) a `bmad` CLI command is run: existing `bmad install` already counts" as the same event. A reader cannot tell whether A alone satisfies the decision. Required fix: add to Rationale 1 and Option A Cons "except under reading (1), where first use is the existing command", or state that reading (1) is A and that the owner must confirm that this meets the 2026-11-07 decision.

## Check (c): Feasibility statement and both unanswered owner questions

Result: PASS. Feasibility statement present and unchanged in substance at `synth-03:340-346` ("Yes ... [CODE-VERIFIED; nothing was run.]", "Stop condition: not triggered") and restated at `synth-04:346` (Section 9 row 4). Q1 and Q2 are present and marked "(unanswered)" at `synth-04:343-344` and in `synth-03:360`; the new sub-questions from fixes 6 and 7 are labelled owner sub-questions, not answers. No answer was invented. Note M-1 below.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| N-1 | IMPORTANT (blocking) | synth-02-target-gaps-external.md:31, :198 | Stale: CLI reading still mapped to a wrapper that "evaluates the predicate, then installs" (Option C); contradicts the corrected synth-03 and synth-04 | Reword both to the Stage 0 / new-command-name position |
| N-2 | IMPORTANT (blocking) | synth-04-plan-questions-evidence.md:25, :118-123, :186, :319, :327-328 | F-01 closure, Phase 3 and test step 5.3 assume a shipped block under every reading; under the CLI reading no block ships | Add the CLI-reading statement for F-01; mark Phase 3, steps 5.2 to 5.4 and the checklist lines conditional on a built Phase 4 branch |
| N-3 | IMPORTANT (blocking) | synth-03-options-recommendation.md:86, :330 vs :310-312, :364 | "A alone fails the decision" vs "Stage 0 only satisfies the CLI reading" | Reconcile Rationale 1 and Option A Cons with reading (1) |
| M-1 | MINOR | synth-04-plan-questions-evidence.md:339 | Section 9 intro says rows 1 and 2 are "copied unanswered from the task file"; Q2(b) is now reworded (original wording is kept in a parenthesis, task file line 164 says "invoking a BMAD slash skill") | Say "copied, with Q2(b) reworded as noted in row 2" |
| M-2 | MINOR | synth-04-plan-questions-evidence.md:158 | A "new, separately named command" is placed in the `bmad` wrapper (:157 edits the group at `Dockerfile.coder:142`); a different command name would not pass through that wrapper | State whether the new name is a case inside the `bmad` wrapper or a second file in `/usr/local/bin` |

## Self-Audit

1. Factual claims independently checked against source: 14. `modules.tf:98-106` (lines 101-105: link removal is conditional, line 105 `rm -rf` unconditional); `manifest.yaml:12-14` (conditional on a seed, command unguarded); `install.sh:22-25, 41-46, 58-61` (guards, failure path, marker); `Dockerfile.coder:133-135, 136-145` (comment text, "pure exec" absent, wrapper group at 142, pin at 139); `ui.js:226-262` (installed tree takes quick-update under `--yes`, no version test in that block); synth-04 lines 28, 62, 65, 118-123, 134, 150, 157-158, 186, 263, 301, 319, 327, 343-346; synth-03 lines 86, 123, 130, 142, 261, 310-364; synth-02 lines 31, 32, 68-69, 110-115, 149, 171, 198; synth-01 lines 220, 312, 382, 433, 476, 487-488; task file lines 163-164.
2. Files read: the consolidated findings, the fix log, all four synth files (the parts named above; synth-01 and synth-02 only partly, by Grep plus targeted Read), the four product files above, `ui.js`, and the task file prompt line plus Q lines. Greps run: F-04/SC-07, "removes only|orca_retirement", "pure exec|stand-in|unconditional|without a seed|already set up", "Option F|G-25", "wrapper", "E and F", "certain", "CLI reading|Stage 0 only|no branch".
3. Why the count is credible: seven of the eight fixes verified clean against code and Grep (no stale phrase left), so the zero-finding result for them rests on reproduced evidence. The three new findings come from following fix 6's decision into the files the fix log did not list (synth-02) and into the plan steps that depend on the block (Phase 3, 5.3, checklist).
4. Not checked (UNVERIFIED): whole of synth-01 and synth-02 beyond the quoted lines; `existing-install.js:111` and the 35-hit count (MINOR rows, not rechecked per the prompt); MINOR rows 9 to 31 of the consolidated findings (notes only, not rechecked).
5. Tool engagement: Read 15 | Grep 9 | Glob 2 | Bash 0. Confidence: Verified 3 of 3 checks (a, b, c) with tool evidence; Unverifiable 0; Unchecked 0.

## Verdict

**FAIL.** Unresolved or new blocking issues: N-1 (synth-02:31, :198), N-2 (synth-04:25, :118-123, :186, :319, :327-328), N-3 (synth-03:86, :330 vs :364). Counts: CRITICAL 0, IMPORTANT 3 (blocking), MINOR 2 (notes). Findings 1 to 5, 7 and 8 are resolved by substance; finding 6 is only partly resolved. Feasibility statement and both owner questions: present, unanswered, correct.

**Status:** Complete
