# Refactoring Plan: Merge into Base (Variant 2, Proposal B)

Slot C-07 (dispatch-and-launch-mechanism). Base file: `variant-2-original.md` (Proposal B). Non-base: `variant-1-original.md` (Proposal A). Evidence for every change comes from this debate only: `debate-transcript.md` and its round files (`round1-advocate-A.md`, `round1-advocate-B.md`, `round2-advocate-A.md`, `round2-advocate-B.md`), `diff-analysis.md`, `invariant-probe.md`, `base-selection.md`. Point IDs (S-, C-, X-, A-) are those of the diff analysis; confidence figures are those of the scoring matrix in the debate transcript. The merged file adds no claim the debate did not conclude.

## Overview
- Base: Variant 2 (Proposal B; default model, default persona), final score 0.9233 against 0.8053, margin 11.80%.
- Incorporating strengths from: Variant 1 (Proposal A).
- Planned changes: 12
- Risk level: Medium (overall). Two changes are High risk: Change 1 (the base's central data edit is replaced, not edited) and Change 3 (the gated launcher, where the two advocates split).
- Output file: `../merged-dispatch-and-launch-mechanism.md` (one level above `adversarial/`), with provenance tags per section.
- Convergence at the end of Round 2: 21 of 26 points agreed (80.77%), BLOCKED_BY_INVARIANTS (INV-017, HIGH). The merged file must state this and must list the 5 unresolved points and the invariants left unaddressed.

## Planned Changes

### Change 1: Replace the packaged `gateway.launch` class-word fill with "binding as data in an explicit environment" (from Round 2 of both advocates)
- **Source**: Base s1 and s2 (`environments.gateway.launch` fill, model-to-class-word pairs; rewrite of `test_gateway_resolution_prints_launch_null`); Variant 1 s2 (additive `adapters` map); `round2-advocate-B.md` section 0 items 1-3, Response row 1, "Updated assessment" S2, S5, S6; `round2-advocate-A.md` N1, N3, N4, V1' items 1 and 5, S5.
- **Target**: Base s1 (position) and s2 (design consequence, `review-tiers.default.json` row and the "dispatch contract" row), replace. Also fix every other base sentence that relies on the withdrawn packaged fill: the s2 `panel.py` row clause "so a three-reviewer gateway panel fits without relaxing it" (A-004 is QUALIFY/QUALIFY: the cap is accepted, "three words suffice" is not accepted for the packaged random-slot templates), the first sentence of the s4 last paragraph ("`test_gateway_resolution_prints_launch_null` ... is rewritten", no longer true under S2), and s7 answer point 3 ("so the data edit removes it without relaxing the profile"). Base s5 item 3 is replaced by Change 7. (Added in review: the original target list left these sentences contradicting the merged position.)
- **Rationale**: scoring matrix C-003 Hybrid 73%: neither a packaged class-word fill (wrong per seed: over 400 run ids `reflect-pre` slot `t4` varies across three models; the documented default binding disagrees with every tier 4 model; any packaged tier edit changes `tiers_sha256` and orphans recorded shadow runs, `reflect_shadow_exit.py:128-132`; `gateway` is the default environment when `$T3Model01` is set, `panel.py:485-494`) nor Variant 1's `adapters` key (rejected by `validate_tiers`, `panel.py:371-373`). Both advocates agree that for the ship-now set packaged `gateway.launch` stays `{}`, `_REFLECT_LAUNCH` and the 3-reviewer cap stay, D4 keeps routing gateway to the legacy rotation, and `tiers_sha256` is unchanged. They split on later: advocate A fills `gateway.launch` with `claude-p` for the ids that pass G1-G3 (residual R1), advocate B never fills the packaged `gateway` environment and uses a new environment name for any future packaged data (RB6); that split is carried in Change 3, not decided here. The text must state S5 as the advocates stated it: B's form is `panel resolve --tiers <file> --env <new env name>` with `available`, `stand_ins`, one-word-per-model `launch` and `note`; A's form is a project or user tier file found by `find_path`; the debate did not choose between them and INV-003 (MEDIUM, UNADDRESSED) records that the `find_path` form silently replaces the packaged tiers for every shadow resolve.
- **Integration point**: rewrite the two paragraphs and the table row; keep the base's sentence that the `--env gateway` refusal comes from an empty map, not the ceiling (both advocates confirmed it).
- **Risk**: High. It removes the base's headline remedy; INV-018 (MEDIUM, UNADDRESSED) says the ship-now set does not by itself change behaviour in a gateway workspace, and the merged text must say so.

### Change 2: Insert the ship-now set: S1-S5 shared, S6-S7 from advocate B only (from Round 2 of both advocates)
- **Source**: `round2-advocate-A.md` "What ships now" S1-S5; `round2-advocate-B.md` "What ships now" S1-S7.
- **Target**: Base, new section after s2, titled "Resolution reached by the debate: what ships now".
- **Rationale**: both advocates named the same S1-S5 (C-001 Hybrid 69%; the measurement items also fall under S-003 Hybrid 68%; S5 is stated in two forms, see Change 1); S6 and S7 are advocate B's additions and advocate A's Round 2 file neither adopts nor rejects them, so the merged text must label them "B" and not call them agreed: S1 dispatch rule (the `launch` word from `panel resolve` is the Agent `model` argument; a missing argument or `launch: null` is a dispatch error); S2 no packaged tier, resolver, validator or ceiling change; S3 one transcript reader (`model_requested`, `model_observed`, `identity_source`, tool names seen; first input the Agent sidechain transcript via `SubagentStop` `agent_transcript_path`; home is slot C-08); S4 the deferred dynamic read-only test run on the Agent path; S5 bindings as data (Change 1); S6 (B) binding-shape tests on a test fixture; S7 (B) PreToolUse guard on `Agent` calls named but not built (payload unverified).
- **Integration point**: new numbered list; each item keeps its test or measurement as the advocates wrote it. Three statements the debate did reach must sit in the list: (a) S1 is a prompt rule today with no enforcer, as advocate B conceded (Response row 3), and the collapse replay runs after the votes; (b) on whether the omitted-`model` failure (A-006, unresolved) can be made mechanical on the class-word path, advocate A holds that only a Python-built `--model` argument does (R4), advocate B holds this is not established and that a PreToolUse guard on `Agent` calls is a candidate whose payload is unverified, one spike answering it (RB4); (c) S3 is unbuilt: `SubagentStop` is registered only for a freshness counter (`hooks.json:179`), the one-reviewer spike is unrun, and each row is judged against the id requested for that attempt, never against a fallback that overwrote it.
- **Risk**: Medium. INV-004 (LOW), INV-005 (MEDIUM), INV-010 (MEDIUM), INV-015 (MEDIUM) and INV-017 (HIGH) apply to this list and must be shown next to it, not hidden in a later section.

### Change 3: Insert the gated `claude-p` launcher design (from Variant 1, as corrected in Round 2)
- **Source**: Variant 1 s1, s2, s6 (M-1, M-2, M-3, M-4); `round2-advocate-A.md` V1' items 1-5, "What is gated" G1-G4, N5, N6, N7; `round2-advocate-B.md` "What is gated".
- **Target**: Base, new section after Change 2, titled "Gated: an id-addressed `claude-p` reviewer".
- **Rationale**: C-001 Hybrid 69%, C-002 Variant 1 70%, C-005 Variant 2 69%, C-007 Variant 2 73%, X-008 Variant 2 75%, X-009 Variant 2 80%. Content both advocates accepted: one `launch` vocabulary (a class word, or `claude-p`), no `adapters` key and no `read_only: unproven` marker; the class-word half is a rule plus a reader, not a launcher; any `claude-p` launcher is a caller of `ClaudeProcess` (`process.py:150-165`: `--model`, `reviewer_profile`, `extra_args`), not a rebuild of E2's shell; it walks the resolution `fallbacks` once with an exclusion list (E2's cyclic ladder ran a review on Qwen3.8-max); G2 read-only plus tool surface (no Bash/Edit/Write call, `git status` unchanged, init tool list has the grounding MCP tools and excludes Bash), accepted as written by both; widening `_REFLECT_LAUNCH` by one value is the reviewed edit taken only after G2 (both), which is how A's rule "a module that needs INV-G refuses an unproven reviewer" is realized now that the `read_only: unproven` marker is withdrawn. The gates the advocates did not treat alike: G1 identity and reach under the restricted flag set (five gateway ids no class word reaches, three attempts each; E2's `bypassPermissions` evidence does not transfer) is a gate that must pass for A, but for B a measurement worth running now and an admission gate for building, not a ship gate; G3 no regression of the packaged `reflect-*` templates under `anthropic-only` and G4 cost (informational) are advocate A's, and advocate B's Round 2 file does not address them.
- **Integration point**: new section; the two positions on what happens after G1-G3 pass are stated side by side (A: launcher, `gateway.launch` fill with `claude-p` for the ids that passed and the ceiling widening ship together, launcher module in the shared review layer; B: no build until a named consumer needs more than three distinct served models or a model no class word can name, launcher in the consuming engine, packaged `gateway` never filled). The debate left this open (Residuals R1-R5 of advocate A, RB1-RB6 of advocate B).
- **Risk**: High. INV-007 (MEDIUM) and INV-016 (MEDIUM) apply: G2 lacks a "reads its inputs and returns a valid findings block" criterion, and once `claude-p` is a permitted `launch` value the reflect check tests the value, not the model.

### Change 4: Correct base statements the debate showed to be wrong or overstated
- **Source**: `diff-analysis.md` X-002, X-005, X-006, X-007; `round1-advocate-B.md` Concessions 1, 2, 3; `round2-advocate-B.md` section 0 and Response rows 1-7.
- **Target**: Base s4 (last paragraph, "Position A rewrites the same test"), s3.1 E7 ("silent swap"), E9 and s2 `cli/reflect` row (scope of the `ClaudeProcess` substrate), s5 item 4 ("I did not find such a test"), s4 INV-L row ("changes a resolution printed under `--env gateway` only"), s3.1 E11 ("0 of the 12 under the tier-1b orchestrator"), s9 last bullet ("Which `--env` the shadow runs pass"). (E11 and s9 added in review: the debate corrected both and the original target list omitted them.)
- **Rationale**: X-002 Variant 1 90% (the pin passes under A's additive form); X-005 Neither 75% (the ladder step is logged, what is lost is the original slot id); X-006 unresolved (A: Variant 2 60%, B: Neither 60%; the facts are shared: both true at scope, the callers launch one model per run); E11: advocate B withdrew "0 of the 12" in Round 2 as not re-derived and agreed that 1 failure in 15 runs is too small a sample to call the failure rare (`round2-advocate-B.md` Response row 3); s4 INV-L and s9: the open item "which `--env` the shadow runs pass" is answered by `SKILL.md:340` (shadow step 1 passes `--env anthropic-only` literally; A-005 ACCEPT/ACCEPT), so the [UNVERIFIED] tag on it is replaced; X-007 Neither 65% (`tests/cli/reflect/test_reviewer_readonly_tools.py` exists, pins the `tools:` line, does not pin `permissionMode`, defers the dynamic test); the INV-L row also gains the shadow-hash dependence (`reflect_shadow_exit.py:128-132,205-207`: any packaged tier edit makes earlier shadow runs "not proven").
- **Integration point**: in-place edits keeping each row's tag; corrected rows carry a short "corrected in debate" note.
- **Risk**: Low (text corrections, cited to code the advocates read).

### Change 5: Add the Round 2 evidence rows that the debate verified
- **Source**: `round2-advocate-A.md` N1-N8; `round2-advocate-B.md` NB1-NB8; `round1-advocate-A.md` Strengths 1-2 and Weaknesses 2, 5; `diff-analysis.md` A-005.
- **Target**: Base s3.1 evidence table, new rows E16 onward, and s3.2 (what the evidence does not show).
- **Rationale**: new rows with their tags as the advocates gave them: `validate_tiers` rejects unknown environment keys (`panel.py:371-373`, `:477-481`); the packaged-template arithmetic (`review-panel.reflect-pre.json:9-11`, `panel.py:545,606-610`; 400-run in-memory result: `t1b` sonnet 400, `t1a` opus 400, `t4` three models); documented default binding (`docs/reference/model-aliases.md:26-35`, `results.jsonl` A-r1/A-r2); shadow-hash dependence; `--tiers` is a shipped option (`panel_cmd.py:26-37`); `--restricted`, `--tools`, `--strict-mcp-config` exist on 2.1.325 (`claude --help`) and `--restricted` ignores settings files (no gateway-id run exists); `ClaudeProcess` flags; shadow step 1 passes `--env anthropic-only` literally (`SKILL.md:340`); an `Agent` PreToolUse hook has repo precedent (`hooks.json:116`, `launch-level-guard.sh:182-205`) with the `model` payload unverified. s3.2 gains: no run of `--restricted` on a gateway id; no measured cost of either path.
- **Integration point**: append rows; keep the base's tag legend; mark rows carried from an advocate file and not re-read by the orchestrator as [CARRIED].
- **Risk**: Low.

### Change 6: Rewrite the invariants section with the probe results
- **Source**: Base s4 (invariant table); Variant 1 s4 (rated Preserved/Endangered split); `invariant-probe.md`; `round2-advocate-B.md` section 0 item 2 and NB4.
- **Target**: Base s4.
- **Rationale**: S-002 Hybrid 58%: A's rated Preserved/Endangered split with B's one-row-per-invariant coverage, plus the shadow-hash row B missed. Add a subsection "Invariants the debate left unaddressed" listing INV-001..INV-019 with status and severity exactly as in `invariant-probe.md` (1 HIGH UNADDRESSED: INV-017; 12 MEDIUM UNADDRESSED; 3 LOW UNADDRESSED; 3 ADDRESSED).
- **Integration point**: keep the base's invariant table (INV-A, B, G, L, F, C/D/E/J, I, K/N); add the A-style rating to each endangered row; append the unaddressed list.
- **Risk**: Medium (INV-G is the HIGH invariant; the table must keep the base's statement that it is preserved only for reviewers launched as agent files).

### Change 7: Rewrite the measurement section in the right-if / wrong-if format
- **Source**: Base s5 items 1-6; Variant 1 s6 (M-1..M-4); `round2-advocate-A.md` S4, G1-G4; `round2-advocate-B.md` S4, S6, G2.
- **Target**: Base s5.
- **Rationale**: S-003 Hybrid 68%: A's right-if/wrong-if rule and stated fallback on every measurement applied to B's head-to-head, collapse replay and `SubagentStop` spike, plus S6 shape tests. Both advocates adopted the dynamic read-only test on the Agent path (S4). The merged list must carry, from the invariant probe, the open criteria it says are missing: INV-005 (the replay prediction "flags A-r3 and no other" is false if calibrator rows are read: six of 15 runs have a null calibrator word), INV-006 (S4 passes if the model declines in prose; no effective-tool-list source on the Agent path), INV-007 (G2 lacks an inputs-readable criterion), INV-010 (S6's "same panel for any run id" is false for the `x2` templates; exclusion paths untested), INV-012 (assert `set(launch) == set(available)`).
- **Integration point**: replace the list; each item states what result shows the position right, what shows it wrong, and the fallback.
- **Risk**: Medium.

### Change 8: Update the consumer section (PR review, rf-qa, C-12)
- **Source**: Base s6; Variant 1 s5; `round1-advocate-A.md` Concession 8 and Weakness 5; `round2-advocate-A.md` B-W6.
- **Target**: Base s6.
- **Rationale**: C-008 Variant 2 57%, C-009 Neither 50%. Keep the base's statements (`--revagent` takes the four class words; rf-qa lenses differ by lens; the C-12 hook-exchange cost). Add from Variant 1: the cost of up to N `claude -p` children per PR round (each loads host hooks without `--bare`), that untrusted PR diffs use the agent-class path until G2 passes, and that both costs are unmeasured. State that neither position serves `live7` or a panel needing more than three or four distinct served models today.
- **Integration point**: append to the existing bullets.
- **Risk**: Low.

### Change 9: Add the C-06 and C-08 interface constraints to the consistency section
- **Source**: Base s8; Variant 1 s4 (dependencies on C-06 and C-08); `diff-analysis.md` U-004.
- **Target**: Base s8, new bullets.
- **Rationale**: a bounded re-ask needs a persisted session; `ClaudeProcess` always passes `--no-session-persistence` (`process.py:152`) and `--resume` for gateway ids is unverified; so a `claude-p` launcher must be able to keep a session id if C-06 needs it. The recorder's home is slot C-08; the model-to-class-word map owner is slot C-09. The text stays an interface constraint, not a decision. Also add the fault-finder's INV-011 (reader key: reviewer id and attempt id, since attempts are not reviewers).
- **Integration point**: new bullets under C-01..C-03 consistency.
- **Risk**: Low.

### Change 10: Add the debate outcome table and the unresolved points
- **Source**: `debate-transcript.md` scoring matrix and convergence assessment; `diff-analysis.md`.
- **Target**: Base, new section near the end, "Debate outcome (26 points)".
- **Rationale**: transparency. Reproduce the 26-row matrix (winner, confidence, one-line evidence) and the tally: Variant 1 2, Variant 2 9, Hybrid 5, Neither 5, unresolved 5 (X-001, X-006, A-003, A-004, A-006); convergence 21 of 26 = 80.77% against 80%, status BLOCKED_BY_INVARIANTS (INV-017). State the shared-assumption labels (A-002 QUALIFY/QUALIFY, A-003 QUALIFY/QUALIFY, A-004 QUALIFY/QUALIFY, A-005 ACCEPT/ACCEPT, A-006 REJECT/REJECT; A-001, not promoted, was answered in Round 1 only: A QUALIFY, B ACCEPT). For A-003, A-004 and A-006 the two advocates gave the same label but named different superior approaches, so the points are unresolved at 50%; the debate does not call these label differences over converged substance. The substance still open is in advocate A's R3 and R4 and advocate B's RB3 and RB4 (what to count for the reach trigger; whether the omitted-argument failure is fixable only in Python).
- **Integration point**: table plus short list.
- **Risk**: Low.

### Change 11: Fix the base's clarity weakness (terms defined on first use)
- **Source**: `score-reeval.md` pair 7 (Variant 2 L4 NOT MET: the header uses INV-G, INV-L, INV-F and C-S6, CO-10, FX-13 before any gloss; "sidechain" and "shim" undefined).
- **Target**: Base header block and s1.
- **Rationale**: the base lost L4; adding a one-line gloss at first use for INV-G (reviewers mutually blind and mechanically read-only), INV-L (shadow mode changes no verdict), INV-F (installed-path rule), "shim" (the local gateway alias proxy in the evidence chain), "sidechain" (the subagent's own transcript), C-S6 (the `--env gateway` refusal, as `invariant-probe.md` INV-018 labels it) and CO-10 (the unmeasured cost, advocate A's G4) uses only definitions that appear in the base or in the debate files. No debate file defines FX-13 or the pointer "synth-06 6.12.0": the merged text must not invent a definition for either; it keeps FX-13 as a bare citation id with its source locator and either drops the pointer or marks the definitions as external. (Added in review: the original rationale left C-S6, CO-10 and FX-13, which `score-reeval.md` pair 7 also names, unaddressed.)
- **Integration point**: inline glosses; no new claims.
- **Risk**: Low.

### Change 12: Add provenance, status line and the return pointers
- **Source**: SKILL.md `provenance_system`; `artifact-templates.md` Section 6.
- **Target**: Whole merged file.
- **Rationale**: document header comments (produced by /sc:adversarial; base Variant 2; merge date); a `<!-- Source: ... -->` tag per section; final status line naming `ADJUDICATION-RESULT.md` is not part of the merged file (the orchestrator writes it).
- **Integration point**: top of file and per section.
- **Risk**: Low.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| C-003 | Variant 1's additive `adapters` map per environment | Rejected by `validate_tiers` (`panel.py:371-373`) and a version-skew failure on an older CLI; both advocates dropped it in Round 2 (INV-008 ADDRESSED). |
| C-005, X-009 | Variant 1's `read_only: unproven` data marker and a ceiling that accepts `adapter == claude-p` now | Variant 1's advocate withdrew the marker; the ceiling stays and widening by one value is the gated, reviewed edit after G2 (C-004 Variant 2 71%, X-009 Variant 2 80%). |
| C-001, C-007 | Variant 1's "closed set of two launch adapters" with a rebuilt E2 launcher in `cli/review` now | The `agent-class` half launches nothing (the orchestrator makes the Agent call) and `ClaudeProcess` already carries the flags; the launcher is gated and built over `ClaudeProcess` (C-007 Variant 2 73%). |
| C-004 | Widening the reflect launch ceiling at ship time | Both advocates keep `_REFLECT_LAUNCH` and the cap now. |
| X-001, X-006, A-003, A-004, A-006 | Either side's position on the unresolved points | Not resolved in the debate; recorded as unresolved with both positions. |
| (base) | Base s2's packaged `gateway.launch` class-word fill and the rewrite of `test_gateway_resolution_prints_launch_null` | Withdrawn by the base's own advocate in Round 2 (replaced in Change 1). |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | High | The merged file keeps a remedy the debate showed wrong, or drops the base's remedy without the replacement | Restore the base s1/s2 text and append the Round 2 withdrawal note |
| 2 | Medium | Ship-now set misstated; probe findings INV-004/005/010/015/017 not shown next to it | Re-derive from the two Round 2 files |
| 3 | High | Gated design presented as agreed where the advocates split (build commitment, location) | Replace with the side-by-side form in the plan |
| 4 | Low | Corrected rows lose their tag | Revert the row to the base text with a note |
| 5 | Low | Evidence rows lose provenance tags | Mark all new rows [CARRIED] |
| 6 | Medium | Invariants table drops the base's INV-G qualification | Restore the base row |
| 7 | Medium | A measurement loses its right-if/wrong-if rule | Restore from the Round 2 file |
| 8-9 | Low | A consumer cost or interface constraint omitted | Add back from the round files |
| 10 | Low | Matrix transcription error | Re-copy from the debate transcript |
| 11-12 | Low | Gloss adds a claim not in the debate | Remove the gloss |

## Review Status
- [x] Auto-approved (default; no `--interactive`)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-14 (the run date; the merge-executor records the merge timestamp)
