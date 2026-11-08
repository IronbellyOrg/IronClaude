# QA Report: Fix Verification (task-integrity, verification round)

**Topic:** issue-watcher task file TASK-RESEARCH-issue-watcher-20261107-064950
**Date:** 2026-11-07
**Phase:** task-integrity / fix-cycle verification
**Fix cycle:** 1
**fix_authorization:** false (task file not modified)

Scope: verify blocking findings I-1, I-2, I-3, I-4, I-5 (b2 report) and B-1 (structure report) against the actual task file text; check for newly introduced defects.

(Sections appended incrementally below.)

## Mechanical checks (run on the task file as it stands now)

- File: 466 lines, 318,479 bytes. `grep -c '^- \[ \]'` = 64 items (unchanged from the 64 claimed by the fix log).
- Frontmatter parses with PyYAML (`uv run python`): 35 keys, id and status present.
- `grep -nE 'TODO|TBD|FIXME'` = 0 matches (the N-8 reword to "T-O-D-O / T-B-D" spelling holds).
- Phrase scan: "same agents with the same" appears once (line 448, Deviations; checked below for context). "no inbound endpoint" appears only inside prohibitions (checked below). "pending owner decision" appears only inside prohibitions or inside the quoted supersession sentence of the embedded addendum (checked below).

## Evidence log (reads done so far)

- Lines 1-170 (frontmatter, Overview, Objectives, References, Source Areas, Key Constraints): read in full.
- Lines 171-190 (Phase 1, Step 2.1 items 01-03): read in full.
- Lines 191-221 (Step 2.2, Gate 1 Steps 3.1-3.4, gaps file): read in full.
- Lines 223-246 (Phase 4 web items, Phase 5 synth items): read in full.
- Lines 247-286 (Gate 2 Steps 5.2-5.5, Phase 6 Steps 6.1, 6.2 first three lenses): read in full.

- Lines 287-346 (rest of Gate 3 lenses, Steps 6.5-6.8), 347-370 (Phase 7) and 371-466 (Task Log, Deviations): read in full.
- Scripted structure check (Python, read-only) over all 64 `- [ ]` lines: no nested or malformed checkboxes; every item has a completion gate except the pre-existing summary item (line 361, wording "Once the summary is complete, mark this item as complete"); no odd double-quote counts after "prompt in full" (no broken quoting); no `<!-- evidence-absence -->` comment inside or after a quoted prompt; zero hits for "named above", "see above", "as above", "the five files named"; the only hit for "same prompts" is line 448 (historical note). The flagged "no verification clause" items (219, 269, 311, 327, 343, 357) all carry "Ensuring ..." with a capital E (false positives of a case-sensitive regex); items 175, 365, 369 are unedited completion items.
- Scripted comparison: the embedded ADDENDUM 2 + points 2-4 block (3,323 characters) is byte-identical in all six prompts that embed it (lines 227, 229, 239, 241, 243, 245), and its key sentences match `research/research-notes.md` lines 102-104 and 110-112.
- Phase item counts by line: Phase 1 = 2, Phase 2 = 4, Phase 3 = 9, Phase 4 = 3, Phase 5 = 12, Phase 6 = 28, Phase 7 = 6, total 64; same as the counts the consolidated findings cite for the pre-fix file.
- Glob: `.dev/issues/331/issue-summary.md`, `.dev/issues/331/analysis/analyze-sc-issue-protocol.md` and `.dev/brainstorms/20261107-064825-github-issue-watcher/enrichment/codebase-context.md` exist.

## Per-finding verification

### I-1 (addendum research requirements not carried into web and synthesis items): FIXED

| Required fix | Where it now is | Correct? |
|---|---|---|
| (a) research-notes.md read + addenda named binding in both web items | Line 227 (web-01) and 229 (web-02): the item text reads "the sections 'ADDENDUM 2026-11-07T07:03Z' and 'ADDENDUM 2 2026-11-07T07:12Z' of research-notes.md (binding; embedded in the prompt below)", and the prompt starts "Binding addenda (...) read both sections first; they are binding on all agents". Same for all four synthesis items: 239, 241, 243, 245. | Yes |
| (b) web-02 questions on sender authentication (mTLS, HMAC with timestamp, GitHub Actions OIDC claims, Coder session/API tokens), `coder_app` share levels and app proxy, minimal contract with idempotency key and response codes | Line 229 prompt, questions (7), (8), (9); verification clause requires answers to (7), (8), (9) with source URLs and "the Coder#477 repo boundary respected". Topic line also extended. | Yes |
| (c) Coder#477 summary and repo boundary embedded in web-02 and synth-02/03/04 | The embedded block (point 2 and "Boundary:" sentence) is in 229, 241, 243, 245 (and 227, 239). Frontmatter `related_docs` (line 41-42), References (line 114), Source Areas (line 130) and Key Constraints (lines 138, 140) also carry it. | Yes |
| B-1 (e): addendum logged in Deviations with timestamp | Lines 456 (07:03) and 457 (07:12). | Yes |

### I-2 (recommendation items steer to pull design / force one option): FIXED, in the decided-A form

- (a) "no inbound endpoint if avoidable" removed from synth-02 Target State constraints. Line 241 now says the Target State "must NOT list 'no inbound endpoint' as a constraint or success criterion (inbound exposure is one scored criterion in Section 6 ...)" and the Constraints list (line 241) is: no live deployment, claim assigns to the gh login that runs it, claim-only, integer-only, repo target. Verification clause of 241: "the Target State constraints do not contain 'no inbound endpoint'". Line 139 (Key Constraints) states inbound exposure is ONE scored criterion, "not a Target State pre-filter". Every other occurrence of the phrase (lines 241, 249, 251, 275, 277) is a prohibition or a check that it is absent. No leftover pre-penalty.
- (b) Scoring against the issue's stated requirements: synth-03 (line 243) adds a "### Requirement Scoring" table scoring EACH of A, B, C, D (and any further hybrid) against nine enumerated requirements taken from `.dev/issues/331/issue-summary.md`, the issue text and Coder#477, with Meets / Partly / Does not meet, a one-line reason and a citation in every cell, and instructs "report the scores honestly even where A scores lower than B or C". Option D is described as a documented hybrid, no longer pull-biased wording; the Options Comparison keeps Inbound exposure as one criterion.
- (c) Single plan: synth-04 (line 245) targets option A; B and C appear in a closing "Follow-up, not in this plan" table with revisit conditions. This supersedes the per-option branch the original fix text asked for, per ADDENDUM 2 (owner decided A). Consistent with the instruction in the verification brief.
- (d) The "pending owner decision" label is NOT added anywhere as a requirement (correct under ADDENDUM 2); instead the recommendation is "option A labelled 'decided by the owner (ADDENDUM 2)'" in 243, and the condensed copy / presentation items (349, 353) match.
- Revisit conditions: 243 adds "### Revisit conditions for options B and C" with columns Condition / Option it would favor / Evidence or source. Present.

### I-3 (scope and boundary items not encoded; gates did not check the addendum): FIXED

- Key Constraints line 137 records D1 = option A, D2 = claim-only ("the earlier open question 'claim-only versus full pipeline' is closed"), D3 = integer-only prompt, and says "the words 'pending owner decision' must not appear". Overview paragraph (line 77) and Objective 3 (line 85) say the same. The old "kept open" D2 wording is gone (grep for "pending owner", "remain open", "stay(s) open" shows only prohibitions and the intentional "details the addenda leave open" in 243/245).
- Integer-only rule evaluated by research agents: line 185 (01) question (8) asks how `/sc:issue --claim <N>` validates its argument and whether the launch prompt can be the single line `/sc:issue --claim <N>`; line 189 (03) question (2) asks whether hooks and claim checks support or undermine the rule and where the claim itself reads issue title or body; line 199 (analyst, Gate 1) lists the question among the assigned questions; 229 (web-02) contract (9) uses "only an integer issue number and the repository name". Carried into synthesis: 241 (Gap row for the integer-only guard), 243 (Section 7 security model), 245 (validation step in the plan).
- Gates check the addendum: Gate 2 (249 analyst "ADDENDUM CONFORMANCE (a violation is a blocking finding)", 251 rf-qa checklist item 13, 253 qualitative check 7, 263 and 265 verifiers); validation checklist (277 checks 17 and 19); Gate 3 lenses (283 a, 289 d and e, 293 f); Gate 3 verifiers (309, 311); Gate 4 (315 and 317 check 6, 325, 327); Gate 5 (331 and 333 extra ADDENDUM CONFORMANCE rows, OMITTED = CRITICAL). Checks name the same items (A decided, B/C scored with revisit conditions, Coder#477 with boundary and the unnecessary-under-A statement, integer-only rule).

### I-4 (fix cycle 2 by back-reference; cycle-1 file names contradict -cycle2): FIXED for all five gates

| Gate | Decision item | 3a consolidate | 3b fix agent prompt in full | 3c two verifiers prompts in full | 3d | `-cycle2` paths consistent with cycle-1 base names |
|---|---|---|---|---|---|---|
| 1 | 219 | yes, file named, columns given | yes | yes (rf-qa + rf-qa-qualitative) | yes | `qa-consolidated-findings-phase3-cycle2.md`, `qa-fix-log-phase3-cycle2.md`, `qa-verification-phase3-structural-cycle2.md`, `...-content-cycle2.md` match bases `...phase3`, `qa-fix-log-phase3`, `qa-verification-phase3-structural/content` |
| 2 | 269 | yes | yes (adds addenda conformance) | yes | yes | phase5 names match |
| 3 | 311 | yes | yes | yes | yes | `qa-consolidated-findings-phase6-cycle2.md`, `qa-fix-log-cycle2.md`, `qa-fix-verification-cycle2.md`, `qa-fix-verification-qualitative-cycle2.md` match bases `qa-fix-log.md`, `qa-fix-verification.md`, `qa-fix-verification-qualitative.md` (items 303, 307, 309) |
| 4 | 327 | yes | yes | yes | yes | `qa-fidelity-*-cycle2.md` match bases (319, 321, 323, 325) |
| 5 | 343 | yes | yes | yes | yes | `qa-anti-omission-*-cycle2.md` match bases (335, 337, 339, 341) |

- The "same agents with the same prompts" wording is gone from every item. Each decision item states "the gate agents ... are NOT re-run" and, for Gate 3, "the seven lens agents of Steps 6.2 to 6.4 are NOT re-run, so the glob `qa-lens-*.md` of Step 6.5 is used in cycle 1 only", which resolves the glob-versus-seven-reports contradiction. Regression check, then monotonicity, then 2-cycle cap order is retained in every gate; cycle-2 inputs are the cycle-1 verification reports, and the cycle-2 prompts write only to `-cycle2` outputs.
- The only remaining occurrence of the phrase is line 448 in Deviations, which quotes it to explain the revision ("the earlier ... wording was a back-reference ..."). It is documentation of the change, not an instruction (see M-2).

### I-5 (dangling "five files named above" in anti-omission prompts): FIXED

- Line 331 (agent 1) prompt: "Assigned input files (exactly these five): research/01-claim-flow-and-session-launch.md, research/02-github-surface-and-cli-patterns.md, research/03-governance-and-security-surface.md, gaps-and-questions.md, synthesis/synth-01-problem-current-state.md" with full relative paths. Line 333 (agent 2): web-01, web-02, synth-02, synth-03, synth-04, full paths. Both match the item wrapper lists. Grep for "named above" returns no hits in the file. Extra ADDENDUM CONFORMANCE rows added with REPRESENTED / OMITTED status, OMITTED = CRITICAL.

### B-1 (task file did not carry the binding ADDENDUM): FIXED

Four gaps from the structure report: (1) Coder#477 and boundary in References (114), Source Areas (130), Key Constraints (138), Overview (77), frontmatter (41-42), every agent prompt; (2) A/B/C scoring: Requirement Scoring table in 243, conformance in validation checklist 19 (277); (3) accepted scope and integer-only rule: Key Constraints 137, Overview 77; D2 reconciled as closed and logged in Deviations 457; (4) extra research scope for B and C: Key Constraints 141, web-02 questions (7)-(9) at 229, Section 5 subsections demanded in 241. Frontmatter `related_docs` description (line 32) no longer calls the notes pre-addendum scope; it names both addenda as binding. Deviations 456 and 457 log both addenda with timestamps.

## New-defect review (adversarial pass over the edited text)

| # | Check | Result | Evidence |
|---|---|---|---|
| N1 | Item IDs and phase structure unchanged, 64 items | PASS | 64 `- [ ]` lines; per-phase counts 2/4/9/3/12/28/6 match the pre-fix counts cited in the consolidated findings; Step labels 1.1 to 7.6 intact (lines 173-369). |
| N2 | No leftover "pending owner decision" as a requirement | PASS | All 50 hits are prohibitions ("never write", "must not appear", "appear nowhere") or the quoted name of the superseded rule inside the embedded addendum text (lines 137, 227-333, 457). No item asks for the label. |
| N3 | No leftover "same agents with the same prompts" instruction | PASS | Only line 448 (Deviations), quoted as the replaced wording. |
| N4 | No leftover "no inbound endpoint if avoidable" pre-penalty | PASS | Phrase appears only in prohibitions and absence checks (241, 249, 251, 275, 277); Key Constraints line 139 states the opposite. |
| N5 | Embedded prompts self-contained | PASS | No "named above"/"see above"/"as above" anywhere; addenda block byte-identical in six prompts; Phase 2 and Gate prompts carry full paths; the only open slots are the deliberate `[INSERT THE BRIEF]` (227, 229), `[INSERT THE LIST]` (315) and `[INSERT THE FILE-02 CODEBASE LIST]`/`[INSERT THE URL LIST]` (317), each with an explicit "inserting your brief/the list" instruction in the item. |
| N6 | Frontmatter still parses | PASS | PyYAML load: 35 keys, `id`, `status` present; `related_docs` has the new Coder#477 entry with `path` and `description`. |
| N7 | B2 five components on edited items | PASS | Scripted check: every edited item has context ("because ..." / purpose), action (Read/Spawn/Use Glob/Create), output path, verification clause ("ensuring"/"Ensuring"), failure branch ("If ...") and the completion gate; the only items without the literal "Once done, mark this item as complete" is 361 (unedited, uses "Once the summary is complete"). |
| N8 | No TBD/TODO/FIXME tokens | PASS | Grep: 0 matches for `TODO|TBD|FIXME`. |
| N9 | Evidence-absence comments outside quoted prompts | PASS | Scripted check: no `<!--` after "prompt in full" in any item; comments sit in the item Context before it (185, 187, 189, 201, 243, 245, 291, 315, 317). |
| N10 | Wording consistently reflects the owner decision | PASS | A decided (137, 77, 85, 243, 245, 349, 353, 369); B/C scored as alternatives with revisit conditions (85, 137, 243, 245); Coder#477 unnecessary unless B/C revisited (42, 77, 114, 138, 140, 457); integer-only and claim-only (137, 185, 189, 229, 241, 245). No item treats D1-D3 as open. |
| N11 | TB-Add-7 Source areas reappear in item Contexts; header has no file:line | PASS | New Source Area "External: IronbellyOrg/Coder#477" (line 130) reappears in the Contexts of items 229, 241, 243, 245; scripted regex finds no `path.ext:NN` in the Execution Context block (lines 109-141). |
| N12 | Cross-item consistency of the new cycle-2 file names | PASS | See I-4 table; each cycle-2 name is the cycle-1 base name plus `-cycle2`, and each is created exactly once (3a, 3b, 3c). |
| N13 | Execution-order dependencies still hold | PASS | synth-04 (245) still runs after synth-03 (243); the new input `.dev/issues/331/issue-summary.md` exists (Glob); Step 7.1 now reads all five verdict files, whose creating items (219, 269, 311, 327, 343) precede it. |

### Issues found (all MINOR, notes only; none blocks)

| # | Severity | Location | Issue | Suggested handling |
|---|---|---|---|---|
| M-1 | MINOR (execution hazard, worth acting on) | `qa/qa-fix-log.md` and `qa/qa-fix-verification.md` versus task items 303, 307, 309, 311 | The orchestrator's task-validation fix log and this verification report use the same file names as the Gate 3 fix log (item 303) and Gate 3 verification report (item 307) that the executor will create later. At execution time Gate 3 would overwrite the A.10 audit trail, and a stale file with a VERDICT line could satisfy item 311's "report exists with a PASS or FAIL verdict" check if the Gate 3 agent fails to write. The task file's names are the designed ones; the collision comes from the QA-round file names. | Before the executor starts, move the A.10 files (`qa-task-validation-*`, `qa-fix-log.md`, `qa-fix-verification.md`) into a subfolder such as `qa/a10-task-validation/`, or rename them. Do not rename the task file's items. |
| M-2 | MINOR | Line 448 | Deviations note quotes "same agents with the same prompts" as the replaced wording; a literal grep for the phrase still hits. It is history, not an instruction. | Optional: reword to "an earlier back-reference wording" to keep a literal scan clean. |
| M-3 | MINOR | Line 245 verification clause | "options B and C appear only in the closing follow-up table" sits next to Section 9, which must also list the B/C revisit conditions in the 'Decided by the owner' table, and Section 10. A literal verifier could fail a correct synth-04. Section 8 is clearly what is meant. | Optional: say "within Section 8, options B and C appear only in the closing follow-up table". |
| M-4 | MINOR (pre-existing, not rechecked) | Frontmatter | `created`, `template`, `tracks` absent (N-1 of the structure report); the previously recorded minor notes N-1, N-3 to N-7, N-9, N-10 were not rechecked per the severity rule. | None. |

## Items Reviewed

| Finding | Check | Verdict |
|---|---|---|
| I-1 | addenda read and embedded in both web items and four synthesis items; web-02 questions (7)-(9) on sender authentication, `coder_app` share levels, contract; Coder#477 and boundary in prompts (lines 227, 229, 239, 241, 243, 245) | PASS |
| I-2 | "no inbound endpoint" removed from Target State constraints and replaced by a prohibition (241, 139); A/B/C/D scored against issue requirements (243); B/C revisit conditions; plan targets A with B/C as follow-up (245); decided-A wording instead of "pending owner decision" per ADDENDUM 2 | PASS |
| I-3 | D1-D3 recorded as decided (137, 77, 85); integer-only rule evaluated by research agents (185, 189, 199, 229) and carried into synthesis (241, 243, 245); addendum-conformance checks in Gates 2-5, validation checklist and lenses (249-253, 263-265, 277, 283, 289, 293, 315-317, 331-333) | PASS |
| I-4 | explicit self-contained cycle-2 sub-steps 3a-3d with full prompts and `-cycle2` paths in all five gates (219, 269, 311, 327, 343); glob/seven-report contradiction resolved; Deviations note rewritten (448) | PASS |
| I-5 | explicit five paths inside both anti-omission prompts (331, 333); "named above" absent from the file | PASS |
| B-1 | Coder#477 + boundary (References, Source Areas, Key Constraints, frontmatter, Overview), scoring, accepted scope, extra B/C research scope, Deviations log (456-457) | PASS |
| New | 64 items, phases and step IDs unchanged | PASS |
| New | no leftover "pending owner decision" (as requirement), "same agents with the same prompts" (as instruction), "no inbound endpoint if avoidable" | PASS (M-2 note) |
| New | embedded prompts self-contained, addenda block byte-identical in six prompts | PASS |
| New | frontmatter parses (35 keys) | PASS |
| New | B2 five components on every edited item | PASS |
| New | no TBD/TODO/FIXME | PASS |
| New | wording consistent with owner decision (A decided, B/C alternatives, Coder#477 unnecessary unless revisited, integer-only, claim-only) | PASS |
| New | TB-Add-7 and evidence-absence placement | PASS |
| New | file-name collision with Gate 3 artifacts | MINOR (M-1) |

## Summary

- Blocking findings re-checked: 6 (I-1, I-2, I-3, I-4, I-5, B-1); resolved: 6; still open: 0.
- New blocking defects introduced by the fixes: 0.
- New minor notes: 3 (M-1 execution hazard, M-2, M-3), plus the unrechecked pre-existing minors (M-4).
- Cycle accounting: this is the first verification of fix cycle 1; blocking count went from 6 to 0, so the monotonicity guard is satisfied and no regression of a previously passing item was found.

## Confidence

Verified: 20/20 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (20 = 6 findings + 14 new-defect checks N1-N13 and the M-1 collision check)

Tool engagement: Read: 23 | Grep: 4 | Glob: 3 | Bash: 7 (read-only: wc/grep/stat-free; PyYAML parse and two read-only Python scripts run through `uv run python`, temporary scripts in /tmp removed; plus two appends to this report). Every read targeted a line range of the task file or a named binding file; no web lookups were needed (no external claim was verified), so no Tavily or fallback calls.

Unchecked / unverifiable items: none. Limits: the check of "B2 five components" on prose quality was mechanical for presence (completion gate, verification clause, failure branch, output path) and manual for the edited items; item 361, 365, 369 were not edited by the fix round and were not re-judged.

## Recommendations

- No further fix cycle is needed. Before execution starts, handle M-1 (move or rename the A.10 QA files that share names with Gate 3 artifacts).
- M-2 and M-3 are optional wording touches.

## QA Complete

VERDICT: PASS
