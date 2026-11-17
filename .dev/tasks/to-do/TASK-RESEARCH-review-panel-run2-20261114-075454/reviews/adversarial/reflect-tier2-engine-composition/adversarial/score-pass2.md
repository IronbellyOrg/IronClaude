ORDER: Variant 2 then Variant 1

# Qualitative Scoring, Pass 2 (reverse order): slot C-04 `reflect-tier2-engine-composition`

Method: 30-criterion additive binary rubric, Claim-Evidence-Verdict. Variant 2 = Proposal B (`variant-2-original.md`, "reconcile at the contract"). Variant 1 = Proposal A (`variant-1-original.md`, "compose"). Each variant is scored as its original text stands. The debate record, `diff-analysis.md` (V-01..V-34, X-001..X-009) and `invariant-probe.md` are used only as evidence about correctness and gaps. Source requirements: row C-04 of `phase-outputs/discovery/undecidable-conflicts.md` (conflicts RE-1, RE-4, CV-8 intent, CV-4, CV-5; invariants INV-A, INV-B, INV-L, INV-M, INV-K). The CV-4 text (`synth-06-conflict-log.md:189`: engine A emits `1.0`, skill and `panel_lint.py:185` demand `1.8.0`) was read to check whether each variant treats it.

# Part A: Variant 2 (Proposal B)

## Completeness

### C1 covers all explicit requirements (Variant 2)
CLAIM: The document covers every conflict and invariant the C-04 row names.
EVIDENCE: Header line 8 names "RE-1, RE-4, CV-8 (intent), CV-4, CV-5". RE-1: §1 position and §2 module table. CV-8: §2 row for `sc-tasklist-protocol/SKILL.md:1141, 1152, 1165` and `task-builder/SKILL.md:2247`; evidence E15. CV-5: §2 row for `ensemble.py:773`. CV-4 is not named in the body but is treated through E13 ("`contract_version "1.0"` with 32 keys ... 89 of the 110 stable names absent") and the INV-A row ("Engine A's `1.0` contract and its 10 extra keys stay as they are"). RE-4: §8, "OQ-20 ... RE-4 is carried as [UNVERIFIED] ... does not state either vocabulary as fact". §4 has rows for exactly INV-A, INV-B, INV-L, INV-M, INV-K. How CV-4 and CV-5 are resolved is scored under K, not here.
VERDICT: MET

### C2 addresses edge cases and failure scenarios (Variant 2)
CLAIM: Failure scenarios of the position are named.
EVIDENCE: §4 INV-L row: "A serializer bug there changes a legacy output". §4 list of exposures: "The production T5 gate keeps saying PASS without a deviation audit"; "`--fix` stays structurally dormant". §7 point 4 and M1: "a helper was skipped by the orchestrator". E9 (restricted child may not spawn the Agent tool) with probe M3 and the stated result for each outcome.
VERDICT: MET

### C3 includes dependencies and prerequisites (Variant 2)
CLAIM: Dependencies on adjudicated slots and prior decisions are stated.
EVIDENCE: §0 table, column "Dependency, agreement or disagreement": C-01 "dependency is on INV-020 (weaker reading)"; C-02 condition kept; C-03 shortfall pins. INV-A row: "those edits need the allow-list widened in the same change". §8 names GQ-067 / OQ-8 as an answer needed before any retirement of engine A. §2 relies on RE-2 as decided.
VERDICT: MET

### C4 defines success/completion criteria (Variant 2)
CLAIM: Pass and fail conditions are registered before any run.
EVIDENCE: §5 table M1-M4 has columns "What counts for Position B" and "What counts against". M1 reuses the exit script's gate: "shadow EV-1 failure rate no higher than the legacy baseline (3 of 39 = 0.077 ...); parity and lint problems 0; leaked keys 0". §5 also gives the single-engine trigger: "(a) the owner answers ... or (b) M4 shows ...".
VERDICT: MET

### C5 specifies what is explicitly out of scope (Variant 2)
CLAIM: Exclusions are stated.
EVIDENCE: §2 closing paragraph "What this position leaves as it is, on purpose"; §1 "(iv) no capability moves between the engines now"; §2 `--t2-engine` row "No new value"; §6 last bullet "that is slot C-11 and is not changed by this position"; §8 "Open items this proposal does not close".
VERDICT: MET

## Correctness

### K1 no factual errors or hallucinated claims (Variant 2)
CLAIM: The document contains defects that the debate verified against code or that its own advocate conceded.
EVIDENCE: (1) §6, "the only importer of swarm stays `cli/reflect/ensemble.py`": false, `fallback.py` and `_diversity.py:5` also import `cli.swarm` (V-03). (2) §2 "two stale inline comments ... `:838` ... `:839`": only `:839` is a comment (V-15). (3) `reviewer_briefs_materialized` is treated as the single line `refs/reviewer-spec.md:78`; it sits on `:51, :57, :78` (V-16; conceded in Round 1). (4) §1 and §8 use GQ-067 for two different questions (X-006; conceded). (5) E11 says engine A "hard-codes" deviations clean; B's own Round 2 R-4 corrects this: `build_reflect_contract` takes the counts as parameters (`ensemble.py:722-749`). (6) §2 "Reuse, not new logic": extractors cover 1 of 6 `merged-verdict.yaml` fields (V-29) and `recompute_parity` is outside the wheel (N2); conceded. (7) §2 resolves CV-5 against the decided row (`synth-06:190` calls the label non-conforming; conceded, R-1). Several verified errors.
VERDICT: NOT MET

### K2 technical approaches are feasible with stated constraints (Variant 2)
CLAIM: The central approach is feasible, with secondary defects that are repairable.
EVIDENCE: §2: additive helper subcommands called "the way it already calls `panel resolve`, `manifest init/advance`, `cluster`, `verify-citations`"; engine A files untouched; 36-test matrix untouched. Debate: B's helper-in-kernel placement with a lazy import of the `panel_lint` constants survived into both Round 2 hybrids (R-2). Constraints are stated (frozen 9.1, fence allow-list, INV-L replay check). Not feasible as written: parity recorded by `recompute_parity` at step 2 (N2 HOLDS: the function is in `scripts/` outside the wheel and needs the finished contract). B dropped the step-2 helper in Round 2.
VERDICT: MET

### K3 terminology used consistently and accurately (Variant 2)
CLAIM: A key identifier is used for two different things.
EVIDENCE: §1: "the owner (r06 gap 1, GQ-067: 'does the wrapper switch to engine B, or does engine A gain exclusion?')". §8: "GQ-067 / OQ-8: readers outside `src/superclaude` of engine A's ten extra keys". `synth-10` Q-08 maps GQ-067 to the readers question only (V-32); B conceded the slip (Round 1 concession 3).
VERDICT: NOT MET

### K4 no internal contradictions (Variant 2)
CLAIM: CV-5 is given two meanings.
EVIDENCE: §1(i): "CV-5 `merge_method: adversarial` means a disk-confirmed merge". §2 `ensemble.py` row: "the count-derived label is engine A's own meaning and that EV-2's disk-confirmed meaning applies only to engine B contracts". This is X-009 in the diff analysis; conceded in Round 2 R-1.
VERDICT: NOT MET

### K5 claims supported by evidence or rationale (Variant 2)
CLAIM: Claims carry tagged evidence and the decisive ones are code-verified.
EVIDENCE: §3 tables E1-E22, each with citation and a tag. Decisive rows are [CODE-VERIFIED]: E1 `runner.py:538-545`; E6 `openai_compat.py:384-388`; E11 `ensemble.py:779-785`; E12 `ensemble.py:773`. Unverified research claims are labelled [UNVERIFIED] with their source file. Weakness: the "reuse" rationale cites `ensemble.py:633-697`, which covers only part of the output.
VERDICT: MET

## Structure

### S1 logical section ordering (Variant 2)
CLAIM: Order runs from inputs to position, design, evidence, invariants, measurement, effects, objection, open items.
EVIDENCE: Headings §0 through §8. §0 (adjudicated slots) precedes the position (S-001, low severity).
VERDICT: MET

### S2 consistent hierarchy depth (Variant 2)
CLAIM: Heading depth is uniform.
EVIDENCE: `##` sections throughout; `###` appears only inside §3 (3.1-3.5).
VERDICT: MET

### S3 clear separation of concerns (Variant 2)
CLAIM: Position, design, evidence, invariants and measurement are in separate sections.
EVIDENCE: §1 position; §2 per-module design table; §3 evidence tables; §4 invariants; §5 measurement; §7 objection.
VERDICT: MET

### S4 navigation aids present (Variant 2)
CLAIM: Cross-references and a tag key exist, no table of contents.
EVIDENCE: Tag key at line 10; evidence row ids cited from §7 ("E6 to E10", "E16, E17, E19"); invariants cite "section 4, items 2 and 3". One cross-reference is wrong: §1 says the trigger is in "section 6", it is in §5.
VERDICT: MET

### S5 follows position-paper conventions (Variant 2)
CLAIM: Position, evidence, invariants, measurement, objection all present.
EVIDENCE: §1, §3, §4, §5, §7 plus §8 open items.
VERDICT: MET

## Clarity

### L1 unambiguous language (Variant 2)
CLAIM: Commitments are stated without hedge words.
EVIDENCE: §1 "(iv) no capability moves between the engines now"; §5 trigger "(a) ... or (b) ...; It is not named when only M1 fails". Residual ambiguity: header line 7 lists three alternatives as the position (S-009, cosmetic); §1 resolves it.
VERDICT: MET

### L2 concrete rather than abstract (Variant 2)
CLAIM: Claims are tied to files, lines and counts.
EVIDENCE: `runner.py:538-545`, `contract.py:310-326`, `test_shadow_skill_contract.py:42-49`, "507 matches ... across 44 files".
VERDICT: MET

### L3 each section has a clear purpose (Variant 2)
CLAIM: Each section reduces to one sentence.
EVIDENCE: §0 "which adjudicated outcomes this relies on"; §2 "what each module is"; §4 "invariants kept or endangered"; §5 "tests that show it right or wrong".
VERDICT: MET

### L4 acronyms and domain terms defined on first use (Variant 2)
CLAIM: Most identifiers are glossed where first used.
EVIDENCE: §1(i) glosses CV-1, CV-2, CV-3, CV-5, CV-6, CV-8, CV-9 inline; line 10 defines the tags and `r06` shorthand; E2 and E3 gloss UC-2 and UC-1. Residual: EV-1 and "T5" are never defined.
VERDICT: MET

### L5 actionable next steps or decision points (Variant 2)
CLAIM: Decision points and next measurements are explicit.
EVIDENCE: §5 M3 states in advance what each probe result means; single-engine trigger; §8 open items (GQ-067, OQ-20, E9, INV-L wording).
VERDICT: MET

## Risk Coverage

### R1 at least 3 risks with probability and impact (Variant 2)
CLAIM: Risks are listed without any rating.
EVIDENCE: §4 "Invariants Position B endangers or leaves open" lists four items (INV-L serializer; PASS without deviation audit; dormant `--fix`; C-01 INV-020). None carries a probability, impact or severity label.
VERDICT: NOT MET

### R2 mitigation for each identified risk (Variant 2)
CLAIM: Some listed risks have no mitigation.
EVIDENCE: INV-L has one (replay check "before it replaces the draft"). Item 2 is "documents instead of removing"; item 3 "keeps passing `--fix` to a loop that cannot fire"; item 4 "needed, not resolved". The skipped-helper risk has measurement M1 but no remedy; B's own advocate conceded "an M1 failure ... no remedy attached".
VERDICT: NOT MET

### R3 failure modes and recovery procedures (Variant 2)
CLAIM: Failure modes are named; recovery is mostly absent.
EVIDENCE: §5: if M1 fails because a helper was skipped, "the 'unskippable' property of a code-driven shell has value that Position B lacks", which is a consequence, not a recovery. Only INV-L has a guard (check against the orchestrator draft with `scripts/reflect_verdict_replay.py` before replacing it).
VERDICT: NOT MET

### R4 external dependencies and their failure scenarios (Variant 2)
CLAIM: External dependencies are named with outcomes.
EVIDENCE: E9 and M3 (can a `reviewer_profile=True` child spawn the Agent tool; each outcome stated); §8 GQ-067 / OQ-8 ("nothing outside `src/superclaude` was searched", INV-A row); owner answer to r06 gap 1.
VERDICT: MET

### R5 monitoring or validation mechanism (Variant 2)
CLAIM: Validation mechanisms are specified.
EVIDENCE: M1 (20 fresh runs, exit script, audit log shows helpers called), M2 (`uv run pytest tests/cli/reflect -q`, pins), `reflect_verdict_replay.py` check in INV-L row.
VERDICT: MET

## Invariant and Edge Case Coverage

### I1 boundary conditions for collections (Variant 2)
CLAIM: One boundary is covered; reviewer-count bounds are not.
EVIDENCE: §1(i) and §2 exit-script row: "CV-9 an empty baseline is 'no baseline'", fix at `scripts/reflect_shadow_exit.py:313`; E12 `ensemble.py:773` "reviewer_count >= 2". No treatment of engine A's clamp [2,4] versus the kernel cap 3 (A-004, V-26), nor of 2-of-3 shortfall runs against the parity rule (INV-011).
VERDICT: MET

### I2 state-variable interactions across component boundaries (Variant 2)
CLAIM: Cross-component state paths are traced.
EVIDENCE: E15: `executor_model` "reaches only the Tier-1 prompt (r06 s4.2, `runner.py:480-481`)", never the swarm. `merge_method` produced in `ensemble.py:773` but defined by EV-2 in the skill. INV-L: skill-run writers versus a kernel helper.
VERDICT: MET

### I3 guard condition gaps (Variant 2)
CLAIM: Missing guards in existing code are identified.
EVIDENCE: E11 `ensemble.py:808-809` `verification_ran False`, `no-verification-stage`; E15 documents promise exclusion that the code never applies; E12 count-derived label with no disk check, `_ev1` never called by the runner. Missed: a frozen-list serializer would drop `adversarial_subrun_status`, which `contract.py:306` reads (V-11, A-001).
VERDICT: MET

### I4 count divergence (Variant 2)
CLAIM: The document itself carries count errors and misses count mismatches.
EVIDENCE: §2 "two stale inline comments" at `SKILL.md:838-839` (one comment, V-15); `reviewer_briefs_materialized` given as one ref line, actually three (V-16); "the only importer of swarm" (V-03); "19 fields" carried [UNVERIFIED] (the debate counted 18 distinct keys); reviewer-count mismatch [2,4] versus 3 not noticed.
VERDICT: NOT MET

### I5 interaction effects when components combine (Variant 2)
CLAIM: Combination effects are named.
EVIDENCE: INV-A row: "the one place where keeping INV-A byte-identical and finishing CV-2 and CV-3 in the skill text pull apart"; INV-L row: a deterministic writer for an authoritative file in shadow; fence allow-list must widen with the prose edits.
VERDICT: MET

# Part B: Variant 1 (Proposal A)

## Completeness

### C1 covers all explicit requirements (Variant 1)
CLAIM: All conflicts and the five named invariants are covered.
EVIDENCE: §0 lists "RE-1 (two engines), RE-4 (vocabularies, carried as [UNVERIFIED], not argued), CV-8 (intent ...), CV-4 and CV-5". RE-1: §1 and §3. CV-8: §3.5 executor-exclusion bullet. CV-5: §3.5 first bullet. CV-4: E4 "89 of the 110 stable names are absent from engine A's contract". §5 has all 14 invariant rows including INV-A, INV-B, INV-L, INV-M, INV-K. RE-4 and CV-4 are treated thinly.
VERDICT: MET

### C2 addresses edge cases and failure scenarios (Variant 1)
CLAIM: Failure scenarios are named.
EVIDENCE: INV-I row: "A code finalizer that cannot write a lint-clean contract must make the run BLOCKED"; §3.4 headless lane limits; INV-B row (reason slug changes from `null-convergence` to `single-reviewer-fallback`); §4.3 "No run has used a code-written contract".
VERDICT: MET

### C3 includes dependencies and prerequisites (Variant 1)
CLAIM: Dependencies are explicit.
EVIDENCE: §2 points (a)-(c) for C-01, "C-02 condition", "C-03 dependencies"; §3.5 "depends on the tier-source decision of slot C-09"; §3.3 first `cli/reflect` to `cli/review` import edge; INV-A row "the `reviewer_briefs_materialized` conflict must be settled first".
VERDICT: MET

### C4 defines success/completion criteria (Variant 1)
CLAIM: Pass and fail conditions are given per measurement.
EVIDENCE: §6 M2: "A is right on its own terms if every recorded run yields a contract that `lint_panel_contract` accepts ... A is wrong, or incomplete, if a recorded failure needs judgment to repair". M3 counts of 0; M4 stub run result; M5 names the deciding measurement.
VERDICT: MET

### C5 specifies what is explicitly out of scope (Variant 1)
CLAIM: Exclusions are stated, scattered over sections.
EVIDENCE: §0 decided rows "not debated"; §2 "A takes no position on the C-06 policy"; §3.4 "Whether a headless run may be PASS-eligible at all ... A does not answer"; §6 M5 "A does not measure quality".
VERDICT: MET

## Correctness

### K1 no factual errors or hallucinated claims (Variant 1)
CLAIM: Verified or conceded defects exist.
EVIDENCE: (1) §3.4 grounded lane "reached through ... the `ClaudeProcess` else-branch (`runner.py:546-572`)": production Tier 2 never reaches it (V-07; conceded in full, Round 2 W1). (2) §5 INV-K "SKILL.md edits stay under `### 4.3a`" while §3.5 reconciles `:703, :839, :1317, :1481` outside the fence (V-15; conceded W11). (3) §8 answer 2 "The new code is the write side only. The readers exist" (V-29: 1 of 6 fields; N2; conceded W7). (4) INV-B rated "Endangered, MEDIUM" while the I1 witness `test_ensemble_stub_integration.py:141-168` would flip PASS to DEGRADED (conceded W3). (5) §3.2 step 10 allowlist drops `adversarial_subrun_status` (V-11; conceded W4).
VERDICT: NOT MET

### K2 technical approaches are feasible with stated constraints (Variant 1)
CLAIM: The headline composition has no working seam.
EVIDENCE: Production Tier 2 routes to `run_tier2_ensemble` (`runner.py:538-545`), the child branch is dead for standard/deep (V-07, X-001). N1: the `reflect` group exits 0 under the recursion marker (`commands.py:75-79`), so a reflect-group finalizer would be a silent no-op. N3: `reviewer_profile=True` drops the permission bypass (`process.py:150-154`) while the steps write files. V-28: the lint reads directories the headless lane never creates. A's own Round 2 removed the grounded lane from the design (D3 DEFERRED).
VERDICT: NOT MET

### K3 terminology used consistently and accurately (Variant 1)
CLAIM: Terms are used consistently.
EVIDENCE: "engine A / engine B", "grounded lane / headless lane", "write side", "shell" are used the same way throughout. GQ-067 is used for the readers question in §4.3, which matches `synth-10` Q-08 (V-32). §0 defines shorthand and tags.
VERDICT: MET

### K4 no internal contradictions (Variant 1)
CLAIM: INV-M and M4 cannot both hold.
EVIDENCE: INV-M row: "`reflect_status` enum and headless output directories ... Preserved". M4: "A stub-lane run builds its contract through the serializer and passes the lint". `panel_lint.py:252, :271-273, :282` read `panel/manifest.json`, `merged-verdict.yaml`, `reviewer-cards/`, `audit.log`, which the headless lane does not create (X-008, V-28; conceded W5).
VERDICT: NOT MET

### K5 claims supported by evidence or rationale (Variant 1)
CLAIM: The central claim lacks supporting evidence in the document.
EVIDENCE: §8 answer 1 ("the only option in which no capability on that list is dropped") rests on E7, whose loss analysis is tagged [UNVERIFIED] (research/06 s8(d), "an analysis for the synthesizer, not a verified fact"). §4.3: "A is an analysis, not an observation". The document's own E1 shows production Tier 2 is engine A with the `/sc:reflect` child "launched only in the other branch", which does not support §3.4.
VERDICT: NOT MET

## Structure

### S1 logical section ordering (Variant 1)
CLAIM: Order is conventions, position, consistency, design, evidence, invariants, measurement, effects, objection.
EVIDENCE: Headings §0-§8.
VERDICT: MET

### S2 consistent hierarchy depth (Variant 1)
CLAIM: Depth is uniform.
EVIDENCE: `##` sections; `###` only in §3 (3.1-3.5) and §4 (4.1-4.3).
VERDICT: MET

### S3 clear separation of concerns (Variant 1)
CLAIM: Concerns are separated with some overlap.
EVIDENCE: Design in §3, evidence in §4, invariants in §5, measurement in §6. Overlap: the §3.2 table carries the observed failures (evidence) and §3.5 mixes decisions with code facts.
VERDICT: MET

### S4 navigation aids present (Variant 1)
CLAIM: Cross-references and conventions are present.
EVIDENCE: §0 conventions and shorthand; cross-references "(section 6, measurement M2)" in the INV-L row, "(3.5)" in INV-A, "(3.3)" in INV-K; these resolve correctly.
VERDICT: MET

### S5 follows position-paper conventions (Variant 1)
CLAIM: All five parts exist.
EVIDENCE: §1 position, §4 evidence, §5 invariants, §6 measurement, §8 objection and answer.
VERDICT: MET

## Clarity

### L1 unambiguous language (Variant 1)
CLAIM: Commitments are stated plainly; non-answers are labelled.
EVIDENCE: "Neither engine is retired"; "must fail the run closed (INV-I)"; open points are labelled ("A does not answer", "[UNVERIFIED]"). Residual vagueness: "The lane is a runtime property (transport, availability, credit)" gives no selection rule.
VERDICT: MET

### L2 concrete rather than abstract (Variant 1)
CLAIM: Claims are tied to lines and run outputs.
EVIDENCE: §4.2 prints the exit script's output ("13 of 20 required", "8/13 = 0.615", shadow04/05/07/08/09/15); §3.1 table with line ranges.
VERDICT: MET

### L3 each section has a clear purpose (Variant 1)
CLAIM: Each section reduces to one sentence.
EVIDENCE: §2 "consistency with C-01/C-02/C-03"; §3 "what is kept, what moves to code, where it lives"; §5 "invariant by invariant".
VERDICT: MET

### L4 acronyms and domain terms defined on first use (Variant 1)
CLAIM: Identifiers are glossed.
EVIDENCE: §0 defines the tags, `r06/r07/r11/r04/r13/r18`, `s05/s06`, INV-A..INV-N and glosses the decided rows (CV-1 "0.80 is the enforced threshold", CV-2, RE-2, RE-3, CV-6, CV-9, RX-15). Residual: EV-1 undefined.
VERDICT: MET

### L5 actionable next steps or decision points (Variant 1)
CLAIM: Conditions and decisions are stated; no trigger for a later single-engine step.
EVIDENCE: §2 (a): "that conflict has to be resolved before A can hold"; INV-L: code-built contract is a comparison artifact until M2 passes; §4.3: "A needs that answer before the 1.0-shaped keys are dropped"; §6 M2, M3.
VERDICT: MET

## Risk Coverage

### R1 at least 3 risks with probability and impact (Variant 1)
CLAIM: Three risks carry a rating (combined severity, no separate probability).
EVIDENCE: §5: INV-L "Endangered, HIGH"; INV-A "Endangered, MEDIUM, until then"; INV-B "Endangered, MEDIUM", each with reason and condition. The label merges likelihood and impact.
VERDICT: MET

### R2 mitigation for each identified risk (Variant 1)
CLAIM: Not every rated risk has a mitigation.
EVIDENCE: INV-L: M2 replay and comparison artifact. INV-A: settle the CV-6 conflict first. INV-B: effect and pin lines listed, "which of them pin a slug and not only an exit code is [UNVERIFIED]", no mitigation. The headless-PASS risk is only "moved into one place where a lint can see it".
VERDICT: NOT MET

### R3 failure modes and recovery procedures (Variant 1)
CLAIM: A fail-closed recovery path is specified.
EVIDENCE: INV-I: finalizer failure "must make the run BLOCKED, never skip silently"; `runner.py:573-580` passes `None` to `derive_verdict`, routed to BLOCKED `contract-missing`. INV-L: comparison artifact under `panel/` until M2 passes. §8 answer 4: "it must fail the run closed (INV-I), not invent".
VERDICT: MET

### R4 external dependencies and their failure scenarios (Variant 1)
CLAIM: External dependencies are named.
EVIDENCE: GQ-067 outside readers (§4.3); slot C-09 tier source (§3.5); C-08 `model_observed` (§2 C-03 dependency 2); lane choice by "transport, availability, credit" (§3.4); the unmeasured first-pass compliance 0.704 / 0.867 (§2 point b).
VERDICT: MET

### R5 monitoring or validation mechanism (Variant 1)
CLAIM: Validation mechanisms are specified.
EVIDENCE: §6 M1 pins, M2 replay oracle, M3 failure-class completeness with exit-script counts of 0, M4 stub run; lint run "as a publish gate" (§3.2 step 10).
VERDICT: MET

## Invariant and Edge Case Coverage

### I1 boundary conditions for collections (Variant 1)
CLAIM: Single, maximum and empty cases appear.
EVIDENCE: M4 "A one-reviewer stub run still yields `single-reviewer-fallback` and exit 11"; §3.1 kernel reflect profile "at most 3 reviewers at `panel.py:71-73`"; CV-9 empty baseline listed in §0. Missed: engine A clamps `--reviewers` to [2,4] (V-26, A-004).
VERDICT: MET

### I2 state-variable interactions across component boundaries (Variant 1)
CLAIM: State paths across components are traced.
EVIDENCE: §3.5: `executor_model` read at `reflect/config.py:351-355`, turned into a CLI argument only at `reflect/runner.py:480-481`, no `cli/swarm` file matches; headless models come from the `T2Model0N` pool, not the tier file. §2 C-02: the `--fix` loop re-audits "with the same `--base` each turn", so no row identity across audits.
VERDICT: MET

### I3 guard condition gaps (Variant 1)
CLAIM: Hard-coded and unguarded values are inventoried.
EVIDENCE: §3.4: `verification_ran: False` (`ensemble.py:808-809`), four deviation counts zero (`:779-785`), `status: "success"` (`:789`), `merge_method` from reviewer count (`:773`); INV-I guard for finalizers. Missed: its own allowlist would drop `adversarial_subrun_status` (V-11).
VERDICT: MET

### I4 count divergence (Variant 1)
CLAIM: Counts are reconciled by execution or grep.
EVIDENCE: §4.2 ran the exit script: "shadow runs counted: 13 of 20 required", "shadow 8/13 = 0.615; legacy baseline 3/39 = 0.077", parity failures in six named runs, lint problems in nine; §3.1 "36 test functions ... by `grep -c`"; §4.1 E3 "32 keys counted"; `reviewer_briefs_materialized` correctly on three ref lines `:51, :57, :78` (V-16); INV-B names the trigger order `:295` before `:299`. Residual: "19 fields" tagged [UNVERIFIED] (18 by the debate); [2,4] versus 3 missed.
VERDICT: MET

### I5 interaction effects when components combine (Variant 1)
CLAIM: Combination effects are analysed.
EVIDENCE: INV-B: a disk-confirmed `merge_method` changes the verdict reason (`contract.py:295` before `:299`); INV-L: change of writer for authoritative files; §3.3 first import edge; §3.4 lens template change from a table to a findings-v2 block; §2 C-02 reopens if the fix loop gains cross-round identity.
VERDICT: MET

## Verdict Table

| Criterion | Variant 1 | Variant 2 |
|---|---|---|
| C1 | MET | MET |
| C2 | MET | MET |
| C3 | MET | MET |
| C4 | MET | MET |
| C5 | MET | MET |
| K1 | NOT MET | NOT MET |
| K2 | NOT MET | MET |
| K3 | MET | NOT MET |
| K4 | NOT MET | NOT MET |
| K5 | NOT MET | MET |
| S1 | MET | MET |
| S2 | MET | MET |
| S3 | MET | MET |
| S4 | MET | MET |
| S5 | MET | MET |
| L1 | MET | MET |
| L2 | MET | MET |
| L3 | MET | MET |
| L4 | MET | MET |
| L5 | MET | MET |
| R1 | MET | NOT MET |
| R2 | NOT MET | NOT MET |
| R3 | MET | NOT MET |
| R4 | MET | MET |
| R5 | MET | MET |
| I1 | MET | MET |
| I2 | MET | MET |
| I3 | MET | MET |
| I4 | MET | NOT MET |
| I5 | MET | MET |

## Subtotals

| Dimension | Variant 1 | Variant 2 |
|---|---|---|
| Completeness (C1-C5) | 5/5 | 5/5 |
| Correctness (K1-K5) | 1/5 | 2/5 |
| Structure (S1-S5) | 5/5 | 5/5 |
| Clarity (L1-L5) | 5/5 | 5/5 |
| Risk Coverage (R1-R5) | 4/5 | 2/5 |
| Invariant & Edge Case Coverage (I1-I5) | 5/5 | 4/5 |
| **Total** | **25/30** | **23/30** |

Edge-case floor check (Invariant & Edge Case Coverage >= 1/5 for eligibility as base): Variant 1 5/5, eligible. Variant 2 4/5, eligible.
