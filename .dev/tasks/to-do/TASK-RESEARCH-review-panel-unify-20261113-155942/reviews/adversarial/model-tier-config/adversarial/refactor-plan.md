# Refactoring Plan: Merge into Base (Variant A, proposal-a)

## Overview
- Base: Variant A (`variant-1-original.md`, proposal-a: central panel targets anthropic-only, launch by class name; synth-04 C-03 Option A)
- Incorporating strengths from: Variant B (`variant-2-original.md`, proposal-b: gateway, launch adapters, dated tier data; synth-04 C-03 Option B), selected by debate result and scoring
- Also applying debate-derived corrections to the base (source: debate transcript Rounds 1-2 and the Round 2.5 invariant probe), because the probe found two HIGH problems in the base design
- Planned changes: 19 (Group P: 10 incorporations from B; Group D: 9 corrections from the debate and probe); 8 rejected alternatives in "Changes NOT Being Made"
- Risk level: Medium overall (text-level merge of a design proposal; the design itself remains Medium risk, XS-S core plus staged pieces)
- Output of the merge: `proposal-merged.md` in the parent folder of `adversarial/`; merged text must keep the unresolved conflicts and the HIGH invariants visible (see Group U)
- Section names below refer to Variant A's headings: Header, `## Design` (Core items 1-5, consumer table), `## How it works` (Data flow 1-6, contract fields table, CLI surface), `## Evidence` (EV-1..EV-22 in 6 groups), `## Correctness argument` (steps 1-7, "What this argument does not show"), `## Risks and mitigations` (weakest-point paragraph, R1-R10), `## Test coverage needed` (changes, stay-green, new tests 1-7, run set), `## Cost` (table, recurring cost, items not checked)

## Planned Changes

### Group P: strengths incorporated from Variant B

#### Change 1: Launch grammar decision and closed parse (from Variant B)
- **Source**: Variant B, Design Core 1 and 8 ("Launch grammar", `parse_launch`); unique contribution U-011
- **Target**: Base, `## Design` Core, new item 6 after item 5 (insert)
- **Rationale**: Debate points C-003 (MERGE, 60%): both advocates support deciding the grammar now (`<adapter>:<argument>`, a bare string means `agent-class:<string>`), matching the adapter names already used by decided C09; A advocate conceded that validate_tiers accepts any string (`panel.py:364-368`), so a typo like `haikuu` passes validation. Gateway `cli-model` entries are NOT added (Change N1).
- **Integration point**: New Core item "Launch grammar (decision now, code staged)": grammar text, bare-string compatibility, closed adapter set `{agent-class}` in PR 2 (validate time), `cli-model` and `swarm` reserved but not accepted by packaged data until the C09 dispatcher exists. Keep the two timing positions visible (PR 2 per B advocate, the C09 PR per A advocate); do not pick one (Group U).
- **Risk**: Low. No bytes change in PR 1; a closed parse changes validation only.

#### Change 2: Minimal provenance, version-coupling test and checklist line (from Variant B)
- **Source**: Variant B, Design Core 3 and evidence rows 15-16; unique contribution U-014
- **Target**: Base, `## Design` Core item 3 ("Tier file bytes do not change") and Evidence group 5 (replace in part, append)
- **Rationale**: C-004 (MERGE, 67%): the repo checklist (Coder env, `ccsession-models.json`, `MODEL-TIERS.md`) omits `review-tiers.default.json`, and the only coupling test compares list lengths (`test_review_panel_live7.py:92-106`). A advocate conceded that "nothing dated enters packaged data" was too broad; B advocate conceded that `evidence[]` and `gateway_observed_on` are unchecked free text.
- **Integration point**: Rewrite item 3: "PR 1 changes no tier-file byte. PR 2 adds `tiers_as_of` and `ccsession_models_version` only, a coupling test (provenance version equals `ccsession-models.json` `version`), and a fourth file in the `MODEL-TIERS.md` update checklist; one regeneration of the packaged-tier golden." Add evidence rows for the checklist omission. Replace A's correctness step 6 wording "nothing dated enters" with "no new dated facts beyond two enforceable fields".
- **Risk**: Medium. One golden regeneration in PR 2; `ccsession-models.json` is fetched live from master at launch (B R4), so the coupling test must not break launches.

#### Change 3: Command-layer slot check and env-slot drift check (from Variant B)
- **Source**: Variant B, Design Core 5 (`check_required_env`), V2; unique contribution U-013; B advocate Round 2 extension (set comparison)
- **Target**: Base, `## Design` Core item 2 (the sentence about removing D12) and `## How it works` CLI surface (append)
- **Rationale**: C-006 (unresolved, B-leaning): both advocates want a command-layer check that keeps `resolve` pure; they differ on timing. Live evidence: this machine has `T3Model01..06`, `T4Model04=muse-ember-1.0`, `T0Model01/02`, while the tier file has tier3 with 2 models, tier4 with 3, no tier0 (verified by the B advocate). A's "no gateway dispatch to protect" is true only for the default path; explicit `--env gateway` still needs a slot check.
- **Integration point**: Replace the claim that the flip "removes the D12 single-variable detection" with: the flip removes the single-variable detection from the default path; D12 and the drift check (set comparison, because live T3 lists `Qwen3.8-max` twice) stay as a command-layer check. List the timing disagreement under Group U.
- **Risk**: Low to Medium. Reads env vars only; false failures block a preflight, not a run.

#### Change 4: `panel verify` reduced to V1, V2, V4; V3 warn-only (from Variant B)
- **Source**: Variant B, CLI surface V1-V4; unique contribution U-012
- **Target**: Base, `## How it works` CLI surface ("No new command and no new flag"), Core
- **Rationale**: C-005 (MERGE 66%) and C-009 (MERGE 55%): A has no pre-run warning for the haiku-served-by-`gpt-6.1-sol` case; V3's route chain ignores the documented family-alias rule and rests on the unverified "alias serves its first model" rule (B P7, A R2), so it may only warn, never print "ok", and needs a parent-model input.
- **Integration point**: Keep "no new command in PR 1". Add a staged note: from PR 2 or 3, `panel verify` with V1 launch completeness, V2 slot existence, V4 provenance age; V3 route check as warn-only labelled derived, with `--parent-model`. Do not give V3 an "ok" state.
- **Risk**: Medium. New command surface; mitigated by staging and warn-only V3.

#### Change 5: Completeness and backward-compatibility tests (from Variant B)
- **Source**: Variant B, `## Test coverage needed` new tests "Packaged-data completeness" and "Backward compatibility"; U-015, U-016
- **Target**: Base, `## Test coverage needed` new tests (append as tests 8 and 9, marked "lands with the piece it guards")
- **Rationale**: C-012 (MERGE 62%): each variant's unique tests cover the other's gap. Completeness test would have caught `launch: {}`; backward-compat test pins that the grammar is a strict superset.
- **Integration point**: Append two tests with the staging note: they apply only when PR 2 (grammar and provenance) or PR 3 (gateway entries) ship.
- **Risk**: Low.

#### Change 6: Staged delivery with gates replaces the flat cost table (from Variant B)
- **Source**: Variant B, `## Cost` stages B-1..B-4 and the Gate column; U-018
- **Target**: Base, `## Cost` (replace the table, keep A's sizes and "Items I did not check")
- **Rationale**: S-007 (unresolved, B-leaning): both advocates adopt staged delivery. A advocate's 3-PR order (PR 1 core with no tier-file bytes; PR 2 minimal provenance and coupling; PR 3 with the C09 dispatcher) is the base ordering; B contributes the gate column and the owner-decision gate.
- **Integration point**: Cost table with columns Stage, Content, Size, Gate. PR 1 XS-S (A's items plus Group D corrections, size to be re-estimated: S); PR 2 S; PR 3 counted under C09. Gate for gateway `cli-model` entries: owner decision O-2 and the C09 dispatcher.
- **Risk**: Low.

#### Change 7: Evidence-tag legend gains the "read in code" versus "taken from research" distinction (from Variant B)
- **Source**: Variant B, preamble legend (`[CODE]`, `[RES]`, `[E2@4a22d74]`, `[UNVERIFIED]`)
- **Target**: Base, header "Evidence tags" paragraph (append one sentence)
- **Rationale**: S-003 (MERGE, 59%): A's RUN tags say what was re-run, B's `[RES]` says what was not re-read; both are useful.
- **Integration point**: Add: "`[RES]` marks a claim taken from a research file and not re-read in code by the author." Keep A's tags and bullet layout; do not convert the Evidence section to B's tables.
- **Risk**: Low.

#### Change 8: Mitigations for A's two risks that have none (from Variant B style)
- **Source**: Variant B, risk table (every row has a mitigation); rubric RK2 (A NOT MET)
- **Target**: Base, `## Risks and mitigations`, rows R7 and R9 (replace mitigation cells)
- **Rationale**: Both scorers marked A NOT MET on RK2 because R7 reads "Out of C03. Record as an open item" and R9 "Out of scope here".
- **Integration point**: R7: owner-gated item "UC-2 Stage 5 decision; the grammar of Change 1 reserves `swarm:`"; R9: "the grammar of Change 1 reserves `cli-model`; the read-only guard composition (`--agent reflect-reviewer --model <id>`, UNVERIFIED) is a C09 design item (C18)".
- **Risk**: Low.

#### Change 9: Owner and dispatcher decision gates made explicit (from Variant B)
- **Source**: Variant B, `## Cost` Gate column, R1 mitigation ("Do not ship the gateway entries before the owner accepts that gap")
- **Target**: Base, new subsection `### Decision points` at the end of `## Cost` (insert)
- **Rationale**: Both scorers marked A NOT MET on CL5 (no ordered next steps or gates); B MET.
- **Integration point**: Table of decisions: O-2 (target environment; open owner item), C09 dispatcher delivery, timing of `parse_launch`, timing of the slot and drift check, whether the loop prompt is edited with the flip (C-001). Each with owner, trigger and what it unlocks.
- **Risk**: Low.

#### Change 10: Evidence rows B verified that A lacks (from Variant B)
- **Source**: Variant B, evidence rows 8 (validator checks only string-map shape), 16 (checklist omits the tier file), 19 (no `tier0` in the tier file), 20 (`T2bModel01` set but unread)
- **Target**: Base, `## Evidence` (new group 7, "tier-file drift and guards")
- **Rationale**: These facts support Changes 1-4 and were verified in code by the orchestrator or advocates (orchestrator: `validate_tiers` launch check at `panel.py:364-368`; B advocate: slot counts live versus repo).
- **Integration point**: New group with four EV-23..EV-26 items, tagged as in the legend; include the live-versus-repo counts as an OBSERVED-RUNTIME fact dated 2026-11-13.
- **Risk**: Low.

### Group D: corrections to the base from the debate and the invariant probe (content not present in either variant)

#### Change 11: Limit the sufficiency claims in the correctness argument (INV-013, INV-010, CR1)
- **Source**: Invariant probe INV-013 and INV-010; both scorers' CR1 NOT MET for A; debate transcript Round 2 (B advocate "Staging test")
- **Target**: Base, `## Correctness argument` step 1 ("valid by construction") and step 2 ("a panel that can run"), plus the `## Design` consumer table row for the E3 loop
- **Rationale**: The loop prompt (`document_review_loop_prompts.md:70`) has no instruction to pass `model` from `launch`; reflect passes `--env anthropic-only` itself, so the flip never reaches it. After the flip the loop prints different names and dispatches as before. A's "forgetting `--env` yields a panel that can run" is true only for the record, not for dispatch.
- **Integration point**: Rewrite step 2 as: "the flip makes the resolution printed for an omitted `--env` a dispatchable one; it changes what is dispatched only for a consumer that passes `launch`, today none of the loop's text does". State the falsifying conditions from INV-013 and the gate enumeration (flip reached only by the loop, resolve complete for anthropic-only, no consumer reads `launch`, Agent-tool family-alias rule, binding-to-served-model chain unverified).
- **Risk**: Low (text), but changes the proposal's main claim.

#### Change 12: Dispatch rule split by engine mode (INV-009)
- **Source**: Invariant probe INV-009 (verified by orchestrator at `SKILL.md:336-342`)
- **Target**: Base, `## Design` consumer table (Reflect row) and `## How it works` Data flow step 5
- **Rationale**: "Every Agent call carries `model == launch`" collides with shadow mode: `SKILL.md:342` "Dispatch is the legacy dispatch" and `panel_parity` compares the resolution with the legacy rotation as it ran; forcing dispatch to follow `launch` makes parity true by construction.
- **Integration point**: Two-part rule. In shadow mode (`engine=shadow`) every Agent call passes an explicit `model` equal to the class the legacy rotation selected, so the frontmatter default can never replace the panel while parity still compares two independent things. At `engine=panel` (Stage 3) the call passes `model == reviewers[i].launch`. State that this reconciliation was NOT debated and is a required decision (Group U), and add a test that parity stays independent in shadow mode.
- **Risk**: Medium. Touches reflect skill text inside the C6 pinned sections; needle tests in `tests/cli/reflect/test_shadow_skill_contract.py` must be re-checked.

#### Change 13: Harden `launch_binding` (INV-001, INV-002, INV-014, A-002)
- **Source**: Invariant probe INV-001, INV-002, INV-014; debate Round 2 (B advocate: keep derived values out of the hashed payload; A advocate: map `Conflict` to `alias_set_changed_mid_run`; add `parent_model`)
- **Target**: Base, `## Design` Core item 4 and `## How it works` Data flow step 4, Contract fields table
- **Rationale**: The payload is a JSON file written by the orchestrating model; `parent_model` has no mechanical source (`ANTHROPIC_MODEL` empty); `advance_stage` hashes the whole payload, so a run started before the change would raise `Conflict` on replay; nothing reads the binding, so card headers still say "Claude Haiku 5.5".
- **Integration point**: Payload carries only the raw three values and `parent_model` (marked `unverified` when it cannot be read); the derived expected-first-model is computed at report time from `tiers_sha256` and never hashed; `Conflict` is mapped to `alias_set_changed_mid_run` for a genuine env change; a payload without `launch_binding` is accepted as "not recorded" or fails with a clear message (state which); add a reader: the panel report or card header labels the model `requested-pinned` and prints the binding.
- **Risk**: Medium. Manifest hash behaviour for in-flight runs.

#### Change 14: The flip ships with a loop consumer, or is withheld (C-001, INV-013)
- **Source**: B advocate Round 2 ("Staging test"), invariant probe INV-010, INV-012, INV-013; A advocate Round 2 (holds the flip alone)
- **Target**: Base, `## Design` Core item 2 and `## Test coverage needed` (flipped tests)
- **Rationale**: C-001 is UNRESOLVED (A advocate: A at 72; B advocate: MERGE at 58). The probe confirms the B advocate's reading that the flip alone is a relabel for the loop.
- **Integration point**: Present both positions side by side under Group U. State the orchestrator's note: the stated outcome in step 2 cannot be claimed under the "flip alone" reading. The options are (i) flip plus a one-line loop-prompt instruction ("pass `model` from `launch`, refuse a null launch") as one unit with a needle test, mirrored to `plugins/superclaude/rules/prompts/` (INV-012) and keeping the pinned sentence `E_FIRST` unchanged; (ii) flip alone, claimed only as "stop printing a record with no launch value". Do not choose.
- **Risk**: Medium. Changes the loop's real dispatch from the session default to sonnet plus three haiku-class reviewers (one gpt model on this machine) under reading (i); no test pins that today.

#### Change 15: Same-class collapse warning replaces the vacuous ceiling test (INV-006, A R6)
- **Source**: Invariant probe INV-006; debate Round 2 (B advocate: single-model warning in the command layer)
- **Target**: Base, `## Test coverage needed` new test 7 and `## Risks` R4, R6
- **Rationale**: The "max 3 distinct classes" test is near vacuous (class count is bounded by construction; `default` resolves 4 reviewers on 2 classes, `live7` 7 reviewers on 2 classes). The real collapse is N reviewers on one class sharing one bound model.
- **Integration point**: Replace test 7 with "a panel of N reviewers sharing one class prints a single-model warning on stderr from `panel_cmd.py` and leaves `resolve` stdout byte-identical", and add the floor "at least 2 distinct eligible classes" (rule D3, `SKILL.md:319`). Keep the three-class ceiling statement as a fact, not a test.
- **Risk**: Low.

#### Change 16: Launch-value guard for every template and a D4 equivalent for the loop (INV-003, INV-004)
- **Source**: Invariant probe INV-003, INV-004
- **Target**: Base, `## Design` Core item 1 and `## Test coverage needed` new test 4
- **Rationale**: The only code-level launch check is `_check_reflect_resolution` (`panel.py:137-157`) and only for `reflect-` templates; the loop prompt has no D4 fallback if `SUPERCLAUDE_REVIEW_ENV=gateway`.
- **Integration point**: State where the dispatch error is enforced (a code check for all templates, in PR 2 with the closed parse of Change 1), and the loop's recovery rule (a null launch means the loop reports it and runs one reviewer, as its existing no-command fallback). Define the allowed set: `fable` is in the anthropic-only map but excluded from `_REFLECT_LAUNCH`; say which applies outside reflect.
- **Risk**: Low to Medium.

#### Change 17: Reviewer-count mapping (INV-005)
- **Source**: Invariant probe INV-005
- **Target**: Base, `## How it works` Data flow step 4 and 5
- **Rationale**: `N_eff = min(--reviewers, alias count, 3)` (`SKILL.md:321`), resolve does not apply it (`SKILL.md:340`), `advance_stage` rejects `reviewers_resolved > reviewers_requested`.
- **Integration point**: State which count `reviewers_requested` records and which reviewers are dropped when `N_eff` is below the resolution count; add one test.
- **Risk**: Low.

#### Change 18: Record the shared assumptions as written decisions (A-001..A-004)
- **Source**: Diff analysis shared assumptions; both advocates' final stances; debate transcript scoring matrix
- **Target**: Base, new `## Assumptions this proposal rests on` before `## Correctness argument` (insert)
- **Rationale**: A-001 ACCEPT (C03 alone enforces nothing; loop prompt has no consumer of `launch`), A-002 QUALIFY (docs resolution order parameter, frontmatter, `CLAUDE_CODE_SUBAGENT_MODEL`, main model; family alias runs on the parent's exact model; the override is documented only for Opus; binding and V3 are expectations; sonnet benign on this machine because the parent model equals the SONNET binding), A-003 ACCEPT with limit (Python readers enumerated: `panel.py:153,595,679`, `select_env` one caller; skills, tests, plugin mirror not enumerated), A-004 REJECT as stated ("ember set live as `T4Model04`, absent from packaged data, serving unknown").
- **Integration point**: Four short paragraphs, one per assumption, each with the stance and what to write down. Correct A's EV-14 wording on ember accordingly.
- **Risk**: Low.

#### Change 19: Replace the "what this argument does not show" paragraph's scope with the debate's open items
- **Source**: Base (retain) plus debate transcript convergence assessment
- **Target**: Base, `## Correctness argument` closing paragraph
- **Rationale**: Keep A's candour and add what the debate left open: observation of served identity still absent for in-session runs (A EV-13), the haiku and opus family-alias behaviour UNVERIFIED, the `--agent` plus `--model` composition UNVERIFIED.
- **Integration point**: Append three sentences; no change to existing text.
- **Risk**: Low.

### Group U: unresolved items that the merged text must keep visible (no resolution is invented)

The merged proposal gets a section `## Open items and unresolved conflicts` placed right after the Position paragraph, listing each item below with both positions, the evidence, and what decision it needs. The merge executor must not choose between positions here.

| Item | Position of Variant A advocate | Position of Variant B advocate | Status and what is needed |
|------|--------------------------------|--------------------------------|---------------------------|
| C-001 target environment and the flip | A at 72%: the flip is the right default fix; only the class path is executable today | MERGE at 58%: class launch ships first, gateway later; the flip is only a relabel unless the loop prompt also passes `model` from `launch` | UNRESOLVED (agreement 50%). INV-013 (HIGH) supports the B reading. Decision: flip as one unit with a loop-prompt edit (Change 14 option i), or flip alone with a narrowed claim (option ii), or withhold the flip. |
| C-006 slot and drift check timing | B at 58%: add a command-layer check, but ship with the dispatcher | MERGE at 55%: ship it in PR 2, same code as the drift check; only V3 and gateway entries wait for C09 | UNRESOLVED (50%), both want the check. Decision: PR 2 or PR 3. |
| S-007 staging | B at 65% (gated stages) | MERGE at 62% (B's gated stages, A's PR order) | UNRESOLVED (50%); substance converged on a 3-PR staging. Decision is editorial, folded into Change 6. |
| X-003 does filling or leaving the launch map make the record honest | A at 58%: A's label is false but controlled and flagged; B ships entries nothing executes | NEITHER at 62%: both labels can differ from what serves until C08 observation exists | UNRESOLVED (50%). Not resolvable by C03 alone; needs C08 observation (`identity_source: observed` has no code, `SKILL.md:348`). |
| INV-009 (HIGH) dispatch rule versus shadow mode | not raised | not raised | UNADDRESSED in debate. Change 12 proposes a split rule; the proposal itself was not debated. Decision: confirm the split or pick another reconciliation. |
| INV-013 (HIGH) sufficiency of PR 1 | not raised | partly raised (loop prompt) | UNADDRESSED in debate. Change 11 narrows the claim; Change 14 shows the options. |
| C-003 sub-dispute: when `parse_launch` lands | in the C09 dispatcher PR | at validate time in PR 2 | Agreed on direction (MERGE), timing open. |
| O-2 target environment (owner decision, synth-04) | defers gateway models to operator class binding | defers gateway entries until the owner accepts R1 | Not decided by this debate; stays an owner item. The merged text must not claim to decide it. |

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| C-002 / N1 | Fill `environments.gateway.launch` with `cli-model:<raw id>` for 12 ids now | A wins at 76% with B's concession (R1: entries describe a route no code executes; the loop dispatches in-session and B's R3 says a raw id cannot be passed on an Agent call). Entries wait for the C09 dispatcher and O-2. |
| C-010 / N2 | `swarm:` adapter slot in the grammar and a place for the code-driven engine | A wins at 71%: no packaged data and no executor use it; C17 keeps the engine until UC-2 Stage 5. The grammar of Change 1 only reserves the name. |
| C-007 / N3 | Add `tier0` (Fable, `gpt-6-astra`) and `muse-ember-1.0` to the packaged tier file | A wins at 68% with B's concession: the "no tier0" rule is testable with a synthetic tier file (as `test_adding_a_model_family_is_a_data_edit_only` does); ember is Coder-first and outside this repo. The drift check of Change 3 must still report both. |
| C-008 / N4 | `_check_reflect_resolution` tests the parsed adapter; gateway error names the adapter | A wins at 74% with B's concession: the existing check already rejects any non-class launch and prints it; the change is cosmetic. |
| C-004 / N5 | `provenance.evidence[]` and `gateway_observed_on` free-text fields | Both advocates agree they are unchecked free text; only `tiers_as_of` and `ccsession_models_version` are enforceable. |
| X-002, C-001 / N6 | "Default environment is the gateway" for every consumer except reflect, with `select_env` unchanged | Internally inconsistent (X-002, A at 72% with B's concession that it is "loose"); the default is the gateway only where `T3Model01` is set. |
| C-015 / N7 | External self-preference literature (B rows 26-27) | A wins at 72% with B's concession: tangential and 2023-era; the platform-documentation evidence (EV-5) is decisive for the launch form. |
| S-003 / N8 | Convert A's Evidence bullets to B's claim / research file / code location / tag tables | Large diff for low value; Change 7 takes the useful part (the `[RES]` tag meaning). |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Low | Grammar decision mis-specified; later change to the closed set | Remove the Core item |
| 2 | Medium | Golden regeneration and coupling test block a Coder-side tier change | Drop the coupling test, keep the checklist line |
| 3 | Low-Medium | False failures in a preflight | Make the check warn-only |
| 4 | Medium | V3 gives a false warn or false ok | V3 is warn-only by construction; remove V3 |
| 5 | Low | Tests pin staged pieces too early | Land with the piece, not earlier |
| 6 | Low | Stage ordering disputed | Editorial |
| 7, 8, 9, 10 | Low | Text only | Revert the paragraph |
| 11 | Low (text), high effect | Main claim weakened | Restore step 2 text (not recommended) |
| 12 | Medium | Reflect shadow parity semantics change; C6 pinned sections and needle tests affected | Keep the rule as prose until the C09 decision |
| 13 | Medium | Manifest replay behaviour for in-flight runs | Keep binding outside the hashed payload as a sidecar |
| 14 | Medium | Loop's real dispatch changes under option (i); no test pins it today | Withhold the flip |
| 15, 16, 17 | Low-Medium | Added tests and text mismatch skill needles | Revert the specific test |
| 18, 19 | Low | Text only | Revert |

## Review Status
- [x] Auto-approved (default, non-interactive run)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-13T23:55:00+00:00
