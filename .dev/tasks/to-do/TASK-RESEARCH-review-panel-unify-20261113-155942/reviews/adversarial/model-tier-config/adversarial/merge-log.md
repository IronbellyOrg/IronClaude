# Merge Log: proposal-merged.md

## Metadata
- Base: Variant A (`variant-1-original.md`, proposal-a, anthropic-only class launch)
- Non-base source: Variant B (`variant-2-original.md`, proposal-b)
- Plan: `refactor-plan.md` (19 planned changes, Group U, 8 changes not made)
- Executor: merge-executor agent (Step 5 of the sc:adversarial run)
- Output: `../proposal-merged.md`
- Changes applied: 19 of 19 (failed 0, skipped 0); two sub-items carried as open decisions (PI-2)
- Status: partial
- Timestamp: 2026-11-14T00:00:08+00:00 (finish; start 2026-11-13T23:50:58+00:00)

<!-- Per-change entries are appended below, one section per change, in plan order. -->

## Per-Change Log

Line numbers refer to `proposal-merged.md` as finally written. Provenance tags are the `<!-- Source: ... -->` comments in that file. Header, title and Position: rewritten per the executor brief (step 6), see "Wording choices and deviations" below.

### Change 1: Launch grammar decision and closed parse (Group P)
- Status: Applied
- Source: Variant B Design Core 1 and 8, `parse_launch` (U-011); timing positions from debate Round 2
- Target: `## Design`, Core item 6 (new)
- Before: Core had items 1 to 5 only.
- After: Item 6 states the grammar `<adapter>:<argument>`, the bare-string rule, the closed set `{agent-class}`, `cli-model` and `swarm` reserved but not accepted, the raw string as recorded form, both timing positions (PR 2 per B advocate, C09 PR per A advocate) and the read-only-guard limit of a single string argument.
- Provenance tag: `Variant B (proposal-b) Design Core 1 and 8 ... merged per Change #1`
- Validation: heading level unchanged; timing left open and carried to Open items (C-003) and Decision points row 3. A first draft said "in PR 2" and "positions stay open" in the same item; fixed during the contradiction re-scan (see PI-3 below).

### Change 2: Minimal provenance, coupling test, checklist line (Group P)
- Status: Applied
- Source: Variant B Design Core 3, evidence rows 15-16 (U-014)
- Target: Core item 3; Evidence group 7 (EV-24); Correctness step 6
- Before: "Tier file bytes do not change ... The packaged-tier golden ... stays valid"; step 6 "nothing dated enters `review-tiers.default.json`".
- After: Item 3 reads "PR 1 changes no tier-file byte; PR 2 adds two enforceable provenance fields": `tiers_as_of`, `ccsession_models_version`, the coupling test, the fourth checklist file, one golden regeneration; `evidence[]` and `gateway_observed_on` not adopted; the live-from-master risk (Variant B R4) stated. Step 6 now reads "no new dated facts beyond two enforceable fields".
- Provenance tag: `Base (original, modified) ... per Change #2`
- Validation: the old sentences are gone (grep for "nothing dated", "Tier file bytes do not change": no hits in body). Related statements qualified for PR 1: test "stay green" list, Cost, R8, contract table.

### Change 3: Command-layer slot and env-slot drift check (Group P)
- Status: Applied
- Source: Variant B Design Core 5 and V2 (U-013); B advocate Round 2 set comparison
- Target: Core item 2 (sentence on D12); CLI surface (append)
- Before: "This removes the D12 single-variable detection ... because there is no gateway dispatch to protect."
- After: The flip removes the detection from the default path only; D12 and the drift check stay as a command-layer check; sets, not lists (live T3 lists `Qwen3.8-max` twice). CLI surface gets a "Command-layer slot and drift check" bullet. Timing listed under Group U (C-006).
- Provenance tag: `Base (original, modified) ... per Change #3`
- Validation: C-006 appears in Open items and Decision points row 4.

### Change 4: `panel verify` reduced to V1, V2, V4; V3 warn-only (Group P)
- Status: Applied
- Source: Variant B CLI surface V1-V4 (U-012); debate C-005, C-009
- Target: CLI surface; Core (Position and Cost mention)
- Before: "No new command and no new flag."
- After: "No new command ... in PR 1"; staged `panel verify` with V1, V2, V4 and a warn-only V3 labelled derived, with `--parent-model`, never "ok".
- Provenance tag: `Base (original, modified) ... per Change #14 and Change #4`
- Validation: V3 has no "ok" state anywhere in the text; Position, CLI surface and Cost agree (Position first said "limited to V1, V2 and V4"; fixed, PI-4).

### Change 5: Completeness and backward-compatibility tests (Group P)
- Status: Applied
- Source: Variant B test table (U-015, U-016)
- Target: `## Test coverage needed`, new tests 8 and 9
- Before: 7 new tests.
- After: Tests 8 (completeness, applies when PR 3 ships gateway entries) and 9 (backward compatibility, applies when PR 2 ships) marked "lands with the piece it guards".
- Provenance tag: `Variant B (proposal-b) Test coverage ... merged per Change #5`
- Validation: numbering 8 and 9 continue the base. See Change 15 for test 7.

### Change 6: Staged delivery with gates replaces the flat cost table (Group P)
- Status: Applied
- Source: Variant B Cost B-1..B-4 and Gate column (U-018); A advocate's PR order (debate Round 2)
- Target: `## Cost`
- Before: flat table, "C03-specific total XS to S", `Items I did not check`.
- After: table with columns Stage, Content, Size, Gate (PR 1 S, PR 2 S, PR 3 counted under C09); sizes explained; recurring-cost and "items not checked" paragraphs kept (first person rewritten).
- Provenance tag: `Variant B (proposal-b), Cost stages ... merged per Change #6`
- Validation: the old "XS to S" survives only as Variant A's own estimate (stated as such). No contradiction left between PR 1 "S" and the old total.

### Change 7: Evidence-tag legend gains the `[RES]` meaning (Group P)
- Status: Applied
- Source: Variant B preamble legend
- Target: header "Evidence tags" paragraph
- Before: legend without `[RES]`.
- After: one sentence appended: "`[RES]` marks a claim taken from a research file and not re-read in code by the author."; a second sentence on origin tags for debate and probe content (executor addition, see deviations).
- Provenance tag: `Base (original, modified) ... per Change #7`
- Validation: `[RES]` used in Core items 3 and 6 and EV-24.

### Change 8: Mitigations for A's risks R7 and R9 (Group P, Variant B style)
- Status: Applied
- Source: Variant B risk table; rubric RK2
- Target: `## Risks and mitigations`, rows R7 and R9
- Before: R7 "Out of C03. Record as an open item ..."; R9 "Out of scope here: it needs one agent file per model and its own read-only allowlist (C18)."
- After: R7 "Owner-gated item for the UC-2 Stage 5 decision. The grammar of Core item 6 reserves `swarm:` ..."; R9 "The grammar of Core item 6 reserves `cli-model`. The frontmatter route needs one agent file per model and its own read-only allowlist (C18); the guard composition ... (`--agent reflect-reviewer --model <id>`, UNVERIFIED) is a C09 design item (C18)."
- Provenance tag: `Base (original, modified) ... R7 and R9 (mitigations per Change #8 ...)`
- Validation: every row R1-R10 now has a mitigation cell with an action.

### Change 9: Owner and dispatcher decision gates (Group P)
- Status: Applied
- Source: Variant B Cost Gate column and R1 mitigation
- Target: new `### Decision points` at the end of `## Cost`
- Before: none.
- After: table with Decision, Owner, Trigger, What it unlocks. Rows 1-5 are the five decisions the plan names (O-2, C09 dispatcher delivery, timing of `parse_launch`, timing of the slot and drift check, loop prompt edited with the flip). Rows 6-8 added (see deviations D-3).
- Provenance tag: `Variant B (proposal-b), Cost Gate column ... merged per Change #9 (CL5)`
- Validation: owners are roles ("Repository owner", "The C09 work") because no source names a person.

### Change 10: Evidence rows B verified that A lacks (Group P)
- Status: Applied
- Source: Variant B evidence rows 8, 16, 19, 20; B advocate Round 2 counts; invariant probe INV-008
- Target: `## Evidence`, new group 7 "tier-file drift and guards", EV-23 to EV-26
- Before: EV-1 to EV-22 in six groups.
- After: EV-23 (validator checks string-map shape only), EV-24 (checklist omits the tier file; length-only coupling test), EV-25 (live versus repo counts, tier0 absent, OBSERVED-RUNTIME 2026-11-13), EV-26 (`T2bModel01` unread, D12 uncovered).
- Provenance tag: `Variant B (proposal-b), Evidence rows 8, 16, 19, 20 - merged per Change #10 (U-014) ...`
- Validation: all four ids are defined and referenced (26 of 26 EV ids defined; see Post-Merge Validation). Tags keep the legend; the Variant B author's `[CODE]` is written `[CODE-VERIFIED by the Variant B author]`. See PI-7 for the attribution of the `validate_tiers` check.

### Change 11: Limit the sufficiency claims (Group D; INV-013, INV-010, CR1)
- Status: Applied
- Source: invariant probe INV-013, INV-010; debate Round 2 (B advocate "Staging test")
- Target: `## Correctness argument` intro, steps 1 and 2; consumer table loop row
- Before: step 1 "The launch value is valid by construction"; step 2 "forgetting `--env` yields a panel that can run".
- After: step 1 limited to "a consumer that reads it" and names the missing consumers; step 2 says the flip makes the printed resolution dispatchable but changes dispatch only for a consumer that passes `launch`, today none; the probe's two falsifying conditions and five gates listed; consumer-table loop row rewritten; intro narrowed to match.
- Provenance tag: `Base (original, modified) ... per Change #11 (INV-013, INV-010; debate Round 2 "Staging test")`
- Validation: the claim "forgetting --env yields a panel that can run" survives only as a quoted sentence that the text then limits.

### Change 12: Dispatch rule split by engine mode (Group D; INV-009)
- Status: Applied
- Source: invariant probe INV-009 (orchestrator-verified at `SKILL.md:336-342`)
- Target: consumer table Reflect row; Data flow step 5; new test 10
- Before: "Dispatch passes `model` from `reviewers[N].launch` on every Agent call (C09)" and step 5 "model = reviewers[i].launch".
- After: shadow mode passes an explicit `model` equal to the class the legacy rotation selected; at `engine=panel` it passes `model == reviewers[i].launch`; stated as not debated; carried to Open items and Decision points row 7; test 10 (parity independence); C6 pinned sections and needle tests flagged for re-check.
- Provenance tag: `Base (original, modified) ... per Change #12 (INV-009 ...)`
- Validation: no remaining unqualified "every Agent call carries model == launch" statement (the three remaining hits are the probe's quoted rule, the Reflect row and test 4, each with the engine-mode qualifier).

### Change 13: Harden `launch_binding` (Group D; INV-001, INV-002, INV-014, A-002)
- Status: Applied, with one sub-item not resolvable from the sources (PI-2)
- Source: invariant probe INV-001, INV-002, INV-014; debate Round 2 (B advocate: derived values outside the hash; A advocate: map `Conflict`)
- Target: Core item 4; Data flow step 4; contract fields table; test 5
- Before: binding "as Wave 0 resolved them" in the payload, no `parent_model`, no reader.
- After: payload carries the three raw values and `parent_model` (`unverified` when unreadable); derived expected-first-model computed at report time from `tiers_sha256`, never hashed; `Conflict` mapped to `alias_set_changed_mid_run`; a reader labels the model `requested-pinned` and prints the binding; the legacy-payload rule is stated as two options without a choice.
- Provenance tag: `Base (original, modified) ... per Change #13`
- Validation: the plan says "accepted as 'not recorded' or fails with a clear message (state which)". Neither the plan nor the debate says which. I did not choose; the choice is Decision points row 6.

### Change 14: The flip ships with a loop consumer, or is withheld (Group D; C-001, INV-013)
- Status: Applied
- Source: B advocate Round 2 "Staging test"; INV-010, INV-012, INV-013; A advocate Round 2
- Target: Core item 2; test coverage (flipped tests); related conditional wording
- Before: the flip was unconditional ("Default environment becomes the supported cell").
- After: item 2 presents (i) flip plus a one-line loop instruction as one unit (needle test, plugin mirror, `E_FIRST` unchanged), (ii) flip alone with the narrowed claim, (iii) withhold; no choice made. The orchestrator's note is in Open items (C-001 row). Flip-dependent text made conditional: Data flow step 2, contract fields `environment`, CLI surface, tests 1 and the two flipped tests, R5, R8, Cost PR 1, Correctness step 2.
- Provenance tag: `Debate/probe ... merged per Change #14. The merge executor does not choose.`
- Validation: contradiction re-scan item (d) below. PI-10 notes that the plan names two options in Change 14 but three in Group U.

### Change 15: Same-class collapse warning replaces the vacuous ceiling test (Group D; INV-006)
- Status: Applied
- Source: invariant probe INV-006; debate Round 2 (B advocate single-model warning)
- Target: test 7; R4; R6
- Before: test 7 "Class-ceiling test. A template whose resolved reviewers need more than three distinct classes is rejected ..."
- After: test 7 "Same-class collapse warning and class floor": N reviewers sharing one class print a single-model warning on stderr from `panel_cmd.py`, `resolve` stdout byte-identical, and fewer than 2 distinct eligible classes is rejected (rule D3, `SKILL.md:319`); the three-class ceiling stays as a stated fact in R4. R6 gains the warning and the note that the R1 warning misses this case.
- Provenance tag: `Base (original, modified) - the base "class-ceiling test" replaced in place per Change #15 (INV-006) ...`
- Validation: test 7 was replaced in place, so no renumbering was needed. Tests 8 and 9 (Change 5) and 10 to 12 (Changes 12, 14, 17) continue after it; every "test N" mention (1, 4, 5, 7, 8, 10, 11, 12) resolves.

### Change 16: Launch-value guard for every template and a D4 equivalent for the loop (Group D; INV-003, INV-004)
- Status: Applied, with one sentence of the base text replaced (PI-9) and the allowed set answered from the base (PI-2)
- Source: invariant probe INV-003, INV-004
- Target: Core item 1; test 4
- Before: "The other consumers get the same rule from the dispatcher ..., not from a second copy in `panel.py`."
- After: enforcement in a code check for every template (PR 2) plus the dispatcher; allowed set is the three classes everywhere and `fable` is a dispatch error (base test 4), with the note that the Agent docs accept `fable` and the debate did not decide; the loop's recovery rule (null launch is reported and one reviewer runs) stated; test 4 extended.
- Provenance tag: `Base (original, modified) - last sentence of base item 1 ... replaced per Change #16 (INV-003, INV-004) ...`
- Validation: the base sentence contradicted the plan ("a code check for all templates"), so it was replaced, not kept.

### Change 17: Reviewer-count mapping (Group D; INV-005)
- Status: Applied, with one sub-item not resolvable from the sources (PI-2)
- Source: invariant probe INV-005
- Target: Data flow steps 4 and 5; new test 12
- Before: step 4 payload `{"reviewers_requested": N, "reviewers_resolved": M, ...}` with no statement of what N is.
- After: states `N_eff = min(--reviewers, alias count, 3)` (`SKILL.md:321`), that `resolve` does not apply it (`SKILL.md:340`), that `advance_stage` raises `Invalid` when resolved exceeds requested (`manifest.py:312-315`), and that the skill never says which count `reviewers_requested` records or which reviewers drop; the text requires the skill to say both; test 12.
- Provenance tag: `Base (original, modified) ... count reference per Change #17`
- Validation: the plan asks to "state which count ... and which reviewers are dropped". No source gives the answer. Left as Decision points row 8; not invented.

### Change 18: Shared assumptions written as decisions (Group D; A-001..A-004)
- Status: Applied
- Source: diff analysis shared assumptions; both advocates' final stances; Scoring Matrix
- Target: new `## Assumptions this proposal rests on` before `## Correctness argument`; EV-14
- Before: none; EV-14 said ember was absent from the gateway list.
- After: four paragraphs (A-001 ACCEPT 85%, A-002 QUALIFY 77%, A-003 ACCEPT with limit 71%, A-004 REJECT 85%); EV-14 now states ember is set live as `T4Model04`, absent from packaged data and `ccsession-models.json`, serving unknown.
- Provenance tag: `Debate/probe ... merged per Change #18`; EV-14 `Base (original, modified) - corrected per Change #18 (A-004)`
- Validation: A-002 items are copied from the two advocates' final lists (docs order, family rule, Opus-only override, binding and V3 are expectations, sonnet benign here, haiku and opus UNVERIFIED, slot 1 equals first model).

### Change 19: "What this argument does not show" extended (Group D)
- Status: Applied
- Source: base paragraph (kept) plus debate convergence assessment
- Target: end of `## Correctness argument`
- Before: one paragraph of four sentences.
- After: the original four sentences unchanged, plus three: served identity unobservable in-session (EV-13), haiku and opus family-alias behaviour UNVERIFIED, `--agent` plus `--model` composition UNVERIFIED.
- Provenance tag: `Base (original) for the first four sentences; Debate/probe ... for the last three sentences - merged per Change #19`
- Validation: no existing sentence altered.

## Group U and Changes NOT Being Made

### Group U (unresolved items)
- Status: Applied as `## Open items and unresolved conflicts`, between the header paragraphs and `## Design`.
- Content: debate status (standard depth, no third round, agreement 86.2% = 25 of 29, BLOCKED_BY_INVARIANTS, no convergence declared, O-2 stays an owner decision); an 8-row table with both advocates' positions, evidence and the decision needed (C-001, C-006, S-007, X-003, INV-009, INV-013, C-003 sub-dispute, O-2); the two HIGH invariants and the seven MEDIUM invariants with one line each and the place where each is handled.
- Added to the plan table: one column "Evidence" (the plan folded evidence into "Status and what is needed").
- Validation: no position was chosen. The orchestrator's note on C-001 is attributed to the refactoring plan.

### Changes NOT Being Made (8 rows of the plan)
- N1 (gateway `cli-model` entries now): not applied. Position, Core item 3, Cost PR 3 and Decision points row 1 keep them out.
- N2 (`swarm:` slot in code): not applied; only the name is reserved (Core item 6, R7).
- N3 (`tier0` and ember data): not applied; EV-25 and the drift check report them. See PI-5.
- N4 (adapter-aware `_check_reflect_resolution`): not applied; no text touches it.
- N5 (`evidence[]`, `gateway_observed_on`): not adopted; Core item 3 and Correctness step 6 say so.
- N6 ("default is the gateway for every consumer except reflect"): not applied.
- N7 (self-preference literature): not applied; no row added.
- N8 (convert A's Evidence bullets to tables): not applied; Evidence stays in bullets.

## Wording choices and deviations from the plan

- **D-1. Placement of the Open items section.** The brief says "right after the Position paragraph, before `## Design`". The base has two more header paragraphs (Source of the conflict, Evidence tags) between them. I kept those two paragraphs in the header block and made `## Open items and unresolved conflicts` the first H2, directly before `## Design`. (PI-1)
- **D-2. Two header sentences added.** A terminology sentence (what "Option A", "Variant B", "the A advocate" mean) and an origin-tag sentence (debate and probe content names its origin). Both follow from the brief's voice rules; neither is a plan change.
- **D-3. Decision points rows 6 to 8.** The plan names five decisions for Change 9. Changes 13, 17 and 12 each say "state which" or "required decision" without giving the answer, so I added rows 6 (legacy payload rule), 8 (count rule) and 7 (confirm the INV-009 split) instead of inventing answers.
- **D-4. Contract fields table.** Two rows added (launch grammar; `tiers_as_of` and `ccsession_models_version`) so the table does not omit fields that Core items 3 and 6 introduce. The `launch_binding` row and a new "binding label" reader row follow Change 13.
- **D-5. Tests.** Test 5 extended with the Change 13 behaviours (the plan names no test for them; test 5 was already the binding test). Test 7 replaced in place (Change 15), so no renumbering. Tests 10 (INV-009), 11 (loop-prompt needle, Change 14 and the recovery rule) and 12 (INV-005) appended. Four rows added to "Existing tests that change": the PR 2 golden regeneration and the coupling test (from Variant B's test table, needed once Change 2 is applied), the loop-prompt pin, and the reflect needle tests (INV-012). The "stay green" list qualified for PR 1.
- **D-6. Recovery rule placement.** Change 16 gives the loop a recovery rule but no PR. I listed it in the PR 2 row, after the code check it depends on, and said so in the text.
- **D-7. Position and Source paragraphs.** Written to the brief (step 6); the Position states no convergence and the limited sufficiency claim.
- **D-8. Consequential wording.** Correctness intro narrowed (matches Change 11); one sentence added to step 4 (the binding reaches the card only through the reader, INV-014); R1 mitigation gained the reader; R6 gained the single-model warning; R8 gained the C-014 caveat from the debate (a `launch_binding` key already written is not removed by reverting); R5 rewritten conditionally.
- **D-9. Group U table.** One "Evidence" column added to the plan's four columns, as the brief asks for evidence in each row. The invariants are in a second subsection `### Invariants from the probe that this text keeps visible`; both subsections sit inside the section the plan names.
- **D-10. Allowed launch set (Change 16).** The plan says "say which applies outside reflect". The debate did not decide. I stated the base's own rule (three classes everywhere; `fable` is a dispatch error, base test 4), noted that the Agent docs accept `fable`, and said the debate did not decide. (PI-2)
- **D-11. `parent_model` placement.** The JSON example in Data flow step 4 puts `parent_model` inside `launch_binding`. The sources say "the three values and `parent_model`" without fixing the nesting.
- **D-12. First-person rewrites.** Every first-person claim of the base (tag legend, `git show` note, EV-5 fetch note, correctness step 5, R5 "I prefer", "Items I did not check") was rewritten as a claim of the Variant A author on 2026-11-13 or as neutral wording. A grep for first-person pronouns finds only the quoted "I did not check" inside a provenance comment.

## Plan inconsistencies found (reported, not hidden)

- **PI-1.** Group U says the section goes "right after the Position paragraph", but the base has two more header paragraphs there (see D-1).
- **PI-2.** Changes 13 and 17 ask the text to "state which" (legacy payload rule; which count `reviewers_requested` records and which reviewers drop). Change 16 asks to say which launch set applies outside reflect. The plan and the debate give no answer for the first two. Both are recorded as options with no choice and carried to Decision points rows 6 and 8. The orchestrator should decide them or confirm that they stay open. For Change 16 the answer was taken from the base (D-10).
- **PI-3.** Change 16 places the all-template code check "in PR 2 with the closed parse of Change 1", while Change 1 and Group U keep the parse timing open (PR 2 or the C09 PR). The merged text keeps the code check in PR 2 and leaves the parse timing open; the two are decoupled. A first draft of Core item 6 said "in PR 2" and "timing open" in one item; fixed.
- **PI-4.** The Position I first wrote listed `panel verify` as "V1, V2 and V4" only, which conflicts with Change 4 (V3 warn-only is part of verify). Fixed. This one was my error, not the plan's.
- **PI-5.** The brief's Position says `tier0` and ember data stay out "until the C09 dispatcher exists and the owner decides O-2". Plan row N3 and the debate give different conditions: `tier0` when a template needs Fable (A advocate), ember Coder-first and outside this repo (both advocates). The PR 3 row shows each condition and its Gate column carries O-2 and C09, which follows the brief. The two readings are not identical.
- **PI-6.** Change 6 says "PR 1 XS-S (A's items plus Group D corrections, size to be re-estimated: S)". I wrote S and kept "XS to S" as Variant A's own estimate.
- **PI-7.** Change 10's rationale credits the orchestrator with verifying the `validate_tiers` launch check at `panel.py:364-368`. In the files I read, that check is verified by the B advocate (`:364-373`, debate Round 1) and reported by the invariant probe (INV-003, `:364-368`); the diff analysis does not list it among the orchestrator's checks. I used the attributions I could see.
- **PI-8.** The plan's approval timestamp (23:55) is later than the plan file's modification time (23:46) and the clock at the start of this merge (23:50). No effect on content.
- **PI-9.** Core item 1 of the base ends with "not from a second copy in `panel.py`", which contradicts Change 16 (a code check for all templates). The sentence was replaced (Change 16).
- **PI-10.** Change 14 lists two options; the Group U row for C-001 lists three (adds "withhold the flip"), and Change 14's rollback is "withhold the flip". The text shows all three.

## Post-Merge Validation

Checks were run with read-only `grep` commands against the finished `proposal-merged.md` (298 lines, one private batch script, `BATCH_DONE`, temp directory removed by trap), then re-run after the late fixes listed under "Late fixes" below.

### (a) Structural integrity: PASS
- Heading hierarchy: one H1 (the title), nine H2, eleven H3, no H4 or deeper. No level gap; every H3 sits under an H2.
- H2 order: Open items and unresolved conflicts, Design, How it works, Evidence, Assumptions this proposal rests on, Correctness argument, Risks and mitigations, Test coverage needed, Cost. The seven base H2 sections are kept in the base order; the two added H2 sections are the two the plan names, in the places it names. `### Decision points` is the last subsection of `## Cost`.
- Added H3 not named in the plan: `### Unresolved points` and `### Invariants from the probe that this text keeps visible`, both inside the section the plan names (D-9).
- No leftover append markers, placeholders or TODO text (grep for `APPEND-POINT`, `PLACEHOLDER`, `TODO`: no hits).
- Provenance: three header comments (Provenance, Base, Merge date) and 52 `Source:` comments covering every H2, every Core item, every table and every significant block. The merge date comment says 2026-11-13, the day the merge started; it finished 2026-11-14.

### (b) Internal references: PASS (0 unresolved)
- EV ids: 26 used, 26 defined (EV-1 to EV-26), 0 unresolved.
- R ids: R1 to R10 used and defined. "Variant B R1", "Variant B R4" and "Variant B P7" are labelled and resolve in `variant-2-original.md`.
- Test numbers: tests 1 to 12 defined; mentions of tests 1, 4, 5, 7, 8, 10, 11, 12 all resolve.
- INV ids: 12 distinct (INV-001 to INV-006, INV-008, INV-009, INV-010, INV-012, INV-013, INV-014), all defined in `invariant-probe.md`; 0 unresolved.
- Point ids: C-001, C-003, C-006, C-014, S-007, X-003, A-001 to A-004 (10 distinct), all defined in `diff-analysis.md` or the debate transcript; 0 unresolved.
- Change references: none in the body text (grep for "Change N" outside comments: no hits). Comments cite plan change numbers, which resolve in `refactor-plan.md`.
- Core item and option references (item 2, item 4, item 6, options (i) to (iii)) resolve inside the document. Section references (`## Cost`, `### Decision points`, `## Correctness argument`) resolve.
- Identifiers not defined in the adversarial folder and not resolved by this merge: C03, C04, C08, C09, C14, C15, C17, C18, C20, O-2, G-33, SC-4, SC-7 and "rule D3/D4/D12". These are synthesis, research or skill-text identifiers carried over from the base (the base-selection report scored the base CL4 NOT MET for this) or cited from the probe (D3, `SKILL.md:319`). I did not add definitions, because the plan does not ask for them.

### (c) Contradiction re-scan: PASS after fixes; two real tensions reported
Checked as the brief asks:
1. **Change 2 versus the old "Tier file bytes do not change" and "nothing dated enters".** Both sentences are gone. Remaining "untouched" and "stays valid" statements are limited to PR 1 (Core item 3, the stay-green list, Cost PR 1). R8 first said the tier file was untouched; it now says the gateway cell and `launch` schema are untouched and PR 2's fields are additive. The old Cost row "Tier file, goldens, templates: none" left with the table. No conflict remains.
2. **Change 6 sizes versus the old "XS to S" total.** The old total row is replaced. "XS to S" remains only as Variant A's own estimate, and the text says PR 1 is re-estimated at S (PI-6). No conflict.
3. **Change 12 split rule versus the old Data flow step 5.** Step 5 is rewritten. Leftovers fixed: Correctness step 1 ("the call's `model` must equal it") and test 4 now carry "where the engine mode requires it". The three remaining hits of "every Agent call ... model == launch" are the probe's quoted rule, the Reflect row (which states the split) and test 4 (qualified). No conflict; the split itself stays an open decision (Open items, Decision points row 7).
4. **Change 14's two options versus text that assumed the flip.** Leftovers found and made conditional: Data flow step 2, contract-table `environment` row, CLI surface paragraph, tests 1 and the two flipped tests, R5 (including the base "I prefer"), R8, Cost PR 1, Correctness step 2, Position. Present-tense statements in EV-1 to EV-3 and EV-20 describe today's behaviour and need no change.
5. **Other leftovers fixed:** Core item 1 (base sentence "not from a second copy in `panel.py`", PI-9); Position said `panel verify` had V1, V2, V4 only (PI-4); Core item 2 said "the base argument" (now "Variant A's argument"); Core items 1 and 6 and the contract row said the parse lands "in PR 2" while the timing is open (PI-3).
6. **Real tensions that are reported and not hidden:**
   - T-1. The all-template code check is placed in PR 2 (Change 16), while the closed parse timing is open (Change 1, C-003). The plan ties them; the merged text decouples them (PI-3).
   - T-2. The brief's Position keeps `tier0` and ember data out "until the C09 dispatcher exists and the owner decides O-2"; the plan and the debate give narrower conditions (PI-5).
   - T-3. Open decisions that the text cannot resolve: legacy payload rule, count rule, INV-009 split (PI-2, Decision points rows 6 to 8).

### Late fixes made during validation
Position (verify wording and timing), Core item 2 ("the base argument"), Core item 1 and Core item 6 and the contract row (PR 2 versus open timing), Cost PR 2 row (loop recovery rule placement). All were wording leftovers, not plan changes.

## Summary

- Changes applied: 19 of 19 (Changes 1 to 19). Failed: 0. Skipped: 0.
- Sub-items of two applied changes could not be satisfied from the sources and are carried as open decisions, not invented: the legacy-payload rule of Change 13 and the count mapping of Change 17 (PI-2). Hence the status is `partial`.
- Group U: applied in full, with both advocates' positions, evidence and decision needed for 8 items; the two HIGH and seven MEDIUM invariants are listed with where each is handled.
- Changes not made: 8 of 8 respected (no content from them entered the merged text).
- Post-merge validation: structural PASS, references PASS (0 unresolved), contradiction re-scan PASS after fixes with three reported tensions.
- Files written: `proposal-merged.md` and this log, and nothing else.
- Merge started 2026-11-13T23:50:58+00:00, finished 2026-11-14T00:00:08+00:00.
