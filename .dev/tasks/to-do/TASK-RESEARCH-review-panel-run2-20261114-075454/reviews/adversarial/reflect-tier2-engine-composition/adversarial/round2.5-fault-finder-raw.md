# Round 2.5 Fault-Finder Raw Findings: slot C-04 reflect-tier2-engine-composition

Role: independent fault-finder (not an advocate). Subject: the emerging consensus H-C04 / H-C04B (42 of 45 diff points agreed). Method: six-category checklist, each finding checked against code read in this session (read-only; no test or script run, nothing written except this file and `invariant-probe.md`). Code state: worktree `brainstorm-reflect-panel`, branch `ironbelly/shadow-runs`.
Conventions: `RF` = `src/superclaude/cli/reflect`, `RV` = `src/superclaude/cli/review`, `EXIT` = `scripts/reflect_shadow_exit.py`, `REPLAY` = `scripts/reflect_verdict_replay.py`, `SKILL` = `src/superclaude/skills/sc-reflect-protocol/SKILL.md`. Counts taken from research files (8/13, 6/13, 7 of 28) were not re-derived and are marked as such.
Severity calibration: no finding below rises to HIGH. The two nearest are INV-001 (the sibling-versus-authoritative switch is unspecified) and INV-017 (the skip-detectability claim is forgeable); both are specification gaps in a design that already defers authority, not defects that make the consensus unsafe as written.

## State variables

ID: INV-001
CATEGORY: state_variables
ASSUMPTION: A code helper writes a comparison sibling (not the legacy-authoritative file) while the engine is `shadow`, and the consensus never says where the helper reads that mode: the frozen manifest field `t2_engine_effective`, or an argument the orchestrator passes.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: round2-advocate-B D2a/E-1 and round2-advocate-A D2a name siblings under `panel/` but no switch. The kernel's own switch is the manifest field frozen at `init` (`RV/manifest.py:123-127`, refusal keyed on it at `:496-500`); an engine change starts a new invocation at `frozen` (`:443-470`), so a later promotion flip resets the stage chain while invocation-1 siblings stay on disk. A's D2(b) "card writer that owns `reviewer-<N>-card.*` names" uses the legacy-authoritative directory name (`RF/panel_lint.py:188`, read at `:273`); a helper that defaults to it writes the INV-L files in shadow, and the legacy debate reads that directory (`SKILL.md:693-695` per B E-1).

ID: INV-002
CATEGORY: state_variables
ASSUMPTION: B's E-3 safe-list: `calibrated` is safe for a helper-owned stage advance because the card writer is "a pure function of the saved calibrator response and cards" (identical payload is a no-op, different payload raises `Conflict`).
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `SKILL.md:344` advances `calibrated` at the end of step 5; `SKILL.md:345` then tells the orchestrator to fix `panel/cards/` and rerun the cluster command whenever calibration ids differ from finding ids. A card-writer rerun after that fix changes the `outputs` hash and raises `Conflict` (`RV/manifest.py:293-299`); a hand fix leaves a stale hash because nothing compares `outputs` with files (`:285-291` check the hex format only). E-3 analysed only the documented `clustered` rerun, not this one.

ID: INV-003
CATEGORY: state_variables
ASSUMPTION: Arm A (D1 only, at least 20 fresh runs) and M-B (helpers, at least 20 fresh runs) can each be read off the exit script's verdict, and the "20-run threshold" is a clean run set.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `EXIT:collect` counts every `pre-*/panel/manifest.json` with effective engine shadow under the root and state published, with no date, arm or invocation filter (`EXIT:209-223`); the default root `.dev/reflect` (`EXIT:392`) already holds the 13 recorded runs (8 EV-1 failures, 6 parity failures per A's run of the script, not re-derived here), so any new run set that reuses it can never pass (EV-1 rate gate `EXIT:307-314`, parity zero tolerance `EXIT:316-324`). A fresh root fixes that but drops the legacy baseline (INV-012). Two arms of 20 are at least 40 live audits, not stated in D6. The EV-1 denominator also excludes Tier-1 runs (`EXIT:189-195`, `:197-200`), so "20 runs" can mean fewer EV-1 observations; the 1/20 = 0.05 versus 0.077 point is already handled (round2-advocate-B R-3).

ID: INV-004
CATEGORY: state_variables
ASSUMPTION: The recursion marker `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` does not silence the new helpers, and the lazy review-to-reflect import adds no start-up or layering cost.
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE: Verified, not just repeated: the `reflect` group callback exits 0 under the marker before any subcommand (`RF/commands.py:75-79`), `review_group` has no guard (`RV/__init__.py:14-16`), `cli/main.py:559-570` already imports both groups at start-up, and `RF/__init__.py:17-20` pulls only `.commands` (stdlib and click imports, `RF/commands.py:15-24`), `.config`, `.contract`, `.models`, so A's N6 cost holds only for in-process importers. Pins (ii reversed) and (iii) cover it. Residual: the marker is set only in the wrapper's own children (`RF/runner.py:560`), so pin (iii) tests a condition that production shadow runs reach only at Stage 5.

## Guard conditions

ID: INV-005
CATEGORY: guard_conditions
ASSUMPTION: A serializer that validates names against `STABLE_FIELDS_1_8_0 | TELEMETRY_FIELDS` (and pins "every verdict-read key is in the accepted set") yields a contract `derive_verdict` reads the same way.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `degraded_components` is a TELEMETRY name (`RF/panel_lint.py:152`) but `derive_verdict` reads it only at the top level (`RF/contract.py:197`; triggers 1-5 at `:274`). The lint accepts telemetry names at top level or nested (`RF/panel_lint.py:316`); `SKILL.md:948` keeps it top level while `SKILL.md:969` says shadow fields nest under `telemetry:`. The recorded corpus has both placements (top level: `.dev/reflect/pre-TASK-WF-fixTheScIssueWor-20261104-162205-shadow05/return-contract.yaml:105`; indented: `.dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-113538-20261106113956/return-contract.yaml:95`). A name-only pin cannot tell them apart and the M-A replay will show a difference whichever placement the serializer chooses, with no stated rule to adjudicate; a nested value makes the chain-critical degrade silently vanish once the contract is authoritative.

ID: INV-006
CATEGORY: guard_conditions
ASSUMPTION: "Helper refuses (validate, never filter)", "helper advances its own stage" and the shadow rule "a step that cannot run records `panel_fallback_reason` and the run continues as legacy" are mutually compatible.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `SKILL.md:338` (continue as legacy, stages advanced in order, none skipped). `advance_stage` raises `OutOfOrder` if any earlier stage was skipped by the orchestrator (`RV/manifest.py:302-306`), so a helper's in-process advance refuses even though the helper did its work; `manifest_cmd.advance_cmd` turns that into a non-zero ClickException (`RV/manifest_cmd.py:206-209`). Not defined anywhere in the debate: write-then-advance order, whether the written file survives an `OutOfOrder`, the exit code on refusal, and how the presence signal tells "helper skipped" from "helper refused because the orchestrator skipped an earlier advance".

ID: INV-007
CATEGORY: guard_conditions
ASSUMPTION: M-A's pass rule "every recorded run yields a contract `lint_panel_contract` accepts" can hold with a serializer that refuses on a foreign key and never filters.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: round2-advocate-A D6 step 1 and B's narrowing (E-7). Recorded failures include contracts with leaked keys (7 of 28 per research/06 via B E-1, not re-derived); the lint reports a foreign key as L2 (`RF/panel_lint.py:316-321`). A refusing serializer produces no contract for those runs, which is neither "lint-clean" nor the stated fail case "a recorded failure that needs judgment". For the 3 unparseable contracts the input is JSON (E-7), so the unquoted `[1m]` alias defect is never exercised by replay ("covered by construction" means untested; `EXIT:74-79` maps them to None). The rule must say that a refusal carrying the lint's own L2 line counts as a pass, and a unit test must cover alias quoting.

## Count divergence

ID: INV-008
CATEGORY: count_divergence
ASSUMPTION: "Exactly one verdict-read key, `adversarial_subrun_status`, is outside both frozen lists" (A-001 REJECT, both advocates), so the only open point is the accepted-set dispute (A: lint set plus that key; B: exactly the lint set with one named exemption).
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: The two advocates do not agree on the base count: A reports 19 verdict-read keys (18 in the lists plus one), B reports 18 `contract.get("...")` literals. Neither counts the alias reads: `_make_result` reads through `c.get(...)` (`RF/contract.py:112-134`) and `_extract_deviations` through `(contract or {}).get(...)` (`:92`). Three of those, `verification_verified`, `reviewers_verified`, `regression_verified` (`:132-134`), are in neither list (no match in `RF/panel_lint.py`) and are written into the tasklist frontmatter (`RF/runner.py:130-132`, `:250-252`). So B's "named exemption list of one member" fails its own pin, and A's literal-regex pin under-covers. The dispute itself is settled by the code in B's favour: the lint flags every non-listed key (`RF/panel_lint.py:316-321`), so A's accepted set would emit a contract its own lint rejects. Also, "137 names" double counts: `citations_dropped_extrapolated` is in both tuples (`RF/panel_lint.py:97`, `:157`) and `telemetry` is a member of `TELEMETRY_FIELDS` (`:173`), giving 136 distinct names.

ID: INV-009
CATEGORY: count_divergence
ASSUMPTION: D1's line lists are complete: "CV-8 list is complete: tasklist `:1141, :1152, :1165, :1170, :1177`, `task-builder:2389`, and `:2247` described as what it says" (A R2), and the CV-1 prose edits cover the 0.75 text.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Grep for `executor-disjoint` over the two skills also hits `sc-tasklist-protocol/SKILL.md:1621` and `task-builder/SKILL.md:1666` (both describe the UC-1 skill path and read as true; a bulk replace would damage them) and `task-builder/SKILL.md:2238` and `:2373` ("the wrapper runs reflect's POST audit as a disjoint `claude --print` subprocess"), which production contradicts: standard and deep Tier 2 goes to `run_tier2_ensemble` and launches no skill child (`RF/runner.py:540-545`). `task-builder/SKILL.md:2247` is a MUST ("the `claude --print` POST subprocess MUST resolve to OUR `sc-reflect-protocol` skill") that the code does not satisfy, so "described as what it says" leaves a false requirement. CV-1: `0.75` is on 10 `SKILL.md` lines (703, 707, 710, 1304, 1317, 1326, 1398, 1400, 1401, 1944) and 2 lines of `refs/grader-extensions.md` (316, 342); D1 names two for CV-1. The unlisted lines were not classified here (not read), only counted.

ID: INV-010
CATEGORY: count_divergence
ASSUMPTION: One recorded reviewer-count rule ([2,4] clamp versus kernel cap 3) and a replacement for the I1 fan-out witness are sufficient preconditions for the single D3/D7 engine decision.
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE: The cap mismatch is covered (A-004: `RF/config.py:334-335` clamps to 1 or [2,4]; `RV/panel.py:72-73` fixes three launch slots and a maximum of 3). Not covered: the value 1. `config.py:334-335` keeps 1 as the negative witness, `SKILL.md:340` says `review panel resolve` has no reviewer-count option, and the I2 witness `tests/cli/reflect/test_ensemble_stub_integration.py:174-196` pins that a 1-reviewer run degrades and falsifies the I1 positive set (`:125-138`, NFR-RH2.3). Replacing I1 without an I2 equivalent leaves the replacement witness unfalsifiable; neither D3 nor Option 3 preconditions name it.

## Collection boundaries

ID: INV-011
CATEGORY: collection_boundaries
ASSUMPTION: M-B can require zero parity failures over the 20 fresh runs ("zero tolerance on presence", parity zero tolerance in the exit rule).
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: The exit script treats the 2-of-3 shortfall as a normal, counted case (`EXIT:244-245`, `:349`) but `recompute_parity` fails any run whose card-header count differs from the resolved reviewer count (`EXIT:139-143`), and every parity failure is a hard failure (`EXIT:323-324`). A card writer that "copies, never invents" (`SKILL.md:346`) cannot supply the missing third card, so a shortfall run in the 20 fails M-B whatever the helpers do (false FAIL). The rule needs a shortfall carve-out or a comparison over completed reviewers only; D6 states neither.

ID: INV-012
CATEGORY: collection_boundaries
ASSUMPTION: D1's CV-9 edit at `EXIT:313` closes "an empty baseline is no baseline, not 0.0".
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: The decided row's evidence is "29 new degraded reasons reproduced on the combo root" (`synthesis/synth-06-conflict-log.md:194`). Those come from `REPLAY.compare` (`scripts/reflect_verdict_replay.py:119-122`: an unpaired shadow run whose degraded reason is absent from an empty `legacy_reasons` counts as new), which feeds an exit failure (`EXIT:337-346`), not from line 313. A fresh root (INV-003) has no legacy runs (`REPLAY.legacy_runs`, `scripts/reflect_verdict_replay.py:92-103`), so after the 313 edit the replay check still fails spuriously. What "no baseline" does to the EV-1 comparison is also unstated: if it skips the comparison the gate is silent, and an EV-1 rate of 20/20 failing passes that leg.

ID: INV-013
CATEGORY: collection_boundaries
ASSUMPTION: M-B's presence rule (manifest `outputs` of each helper-owned stage; a non-published run without a recorded fallback is a failure) and a finalizer that refuses without merged output work for every legitimate run shape.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: EV-1 accepts a run without `merged-verdict.yaml` when the contract carries `adversarial_unavailable: true`, `merge_method: single-reviewer-fallback` and an audit.log F2/F3 row (`RF/panel_lint.py:279-298`); `wave4_ev1` returns None for Tier 1 (`EXIT:189-195`). Such a run must still advance `debated` to reach `published` (no stage can be skipped: `RV/manifest.py:241-243`, `:302-306`) with no merged file to hash: a rule that demands `debated` outputs flags a legitimate run, and accepting an empty `outputs` is the forgeable payload of INV-017. The `collect()` scan does not parse any "recorded fallback" (`EXIT:203-250`). An all-excluded panel adds a mismatch: `advance_stage` accepts `reviewers_resolved: 0` (`RV/manifest.py:309-316`) but the lint rejects anything below a positive integer (`RF/panel_lint.py:258-264`).

## Interaction effects

ID: INV-014
CATEGORY: interaction_effects
ASSUMPTION: M-B can run "the exit rule on code-built siblings" and `reflect_verdict_replay.py` can show "0 verdict differences on the code-built contracts" with no script or lint change beyond D1's `EXIT:313`.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `lint_panel_contract` and `_ev1` read fixed paths under one output directory: `return-contract.yaml`, `panel/manifest.json`, `adversarial/merged-verdict.yaml`, `reviewer-cards/`, `audit.log` (`RF/panel_lint.py:252, :271, :273, :282, :305`). `REPLAY.load` reads `<run>/return-contract.yaml` (`scripts/reflect_verdict_replay.py:64`) and `compare` pairs runs by directory name (`:106-123`); the exit pairs legacy directories against shadow directories, which are different runs, so `changed` is always empty in exit use (`EXIT:266-275`). It cannot show that a code-built contract equals the orchestrator's contract of the same run. Siblings need a mirrored output tree, a path parameter, or a new comparison command; none is in D1 or D2.

ID: INV-015
CATEGORY: interaction_effects
ASSUMPTION: The card writer has one target, and D1's CV-9 item (`EXIT:313`) applies the whole decided row.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: CV-9 (`synthesis/synth-06-conflict-log.md:194`) pairs the empty-baseline defect with a card-name mismatch: `RF/panel_lint.py:188` (`reviewer-<N>-card.*`, for `reviewer-cards/`) versus `EXIT:59` (`reviewer-<N>.md`, for `panel/cards/`, used by parity at `EXIT:98-114`). D1 names only `:313`. A's D2(b) names `reviewer-<N>-card.*`; B's D2 step 5 names `panel/cards/reviewer-<N>.md` (`SKILL.md:344`). Two directories, two regexes and two authority classes (panel-only versus legacy-authoritative for INV-L) are merged into "the card writer" in the consensus bullet.

ID: INV-016
CATEGORY: interaction_effects
ASSUMPTION: Widening the SKILL.md edit fence is bookkeeping: D1's prose fixes leave INV-L ("shadow changes no verdict; legacy stays unchanged") and the Stage 2 legacy baseline untouched.
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE: `SKILL.md:703` ("Convergence routing: >=0.75 PASS, >=0.60 PARTIAL, <0.60 FAIL") and `:1480-1481` (error-matrix rows) are instructions the orchestrator follows in legacy Wave 4 and error handling, outside `### 4.3a`; the fence exists to confine Stage 2 edits to shadow sections (`tests/cli/reflect/test_shadow_skill_contract.py:52-75`). The fence test diffs only against HEAD (`:53`) and matches the nearest heading by prefix (`:61-72`), so widening must name each nearest sub-heading, not `## 8`. After D1, fresh runs follow different Wave-4 prose than the 39-run baseline (3/39, 42 recorded contracts), so shadow-versus-legacy comparison is cross-time; neither transcript says INV-L was re-read for this. Fence widening itself is covered (round2-advocate-B C-016).

## Sufficiency challenge

ID: INV-017
CATEGORY: sufficiency_challenge
ASSUMPTION: CLAIM "helpers that advance their own manifest stage make skipping detectable". Falsifier: the orchestrator calls `manifest advance --stage calibrated --payload <hashes it computed with Bash>` or advances with an empty payload; the stage record carries no actor, so the manifest cannot tell a helper from the orchestrator.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Source enumeration: `RV/manifest.py:279` (payload may be empty), `:284-291` (outputs only checked as 64-hex strings, no file read), `:317-326` (stage record = `payload_sha256`, `outputs`, `deps`, `invocation`; no actor field); `RV/manifest_cmd.py:140-145, :172, :201-203` (payload optional; `published` auto-hashes whatever files exist); `SKILL.md:338` (the orchestrator is the caller of `manifest advance`). The hash-versus-file check is "optional" in both A's D2 and B's acceptance; round2-advocate-A W2 concedes an invented hash is possible. Detection holds only if M-B requires named outputs per helper stage and recomputes the file hashes in the exit script, which D6 does not say.

ID: INV-018
CATEGORY: sufficiency_challenge
ASSUMPTION: CLAIM "D1 prose fixes plus D2 helpers remove the observed Stage 2 exit failures". Falsifier: arm A fails the exit after D1 and the owner keeps INV-L strict, so helpers write only siblings while the exit reads the legacy files.
STATUS: ADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Enumeration of what the exit reads: EV-1 reads `adversarial/merged-verdict.yaml` and `reviewer-cards/` (`RF/panel_lint.py:271-273`), lint L0-L5 read the legacy `return-contract.yaml` (`:305`), parity reads `panel/cards` (helper-written) and the legacy rotation from the legacy contract (`EXIT:98-114, :154-162`). So only parity can improve directly. Handled by round2-advocate-B E-1 and D2a (comparison before promotion; the owner decides how INV-L reads if arm A fails); the debate records the condition.

ID: INV-019
CATEGORY: sufficiency_challenge
ASSUMPTION: CLAIM "comparison siblings let promotion be decided without risk". Falsifiers: (a) in shadow an absent sibling has no effect, but after promotion absence is a refusal or BLOCKED, a path the comparison never exercises; (b) sibling content comes from the same orchestrator input, so equality with the draft proves serializer fidelity, not content; (c) promotion is an engine flip that starts a new invocation; (d) the `read_committed` guard proposed for Option 3 is satisfied in shadow by the orchestrator's own `advance published`.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `RV/manifest.py:491-492` (publish needs exactly the three files), `:505-508` (state must be `validated`), `:443-470` (engine change makes a new invocation), `:496-500` (publish refused in shadow), `:527-534` and `RV/manifest_cmd.py:201-203` (`published` hashes any existing files, so `read_committed` at `RV/manifest.py:176-186` passes for an orchestrator-advanced shadow manifest); `SKILL.md:311` (UC-2 ignores the flag until Stage 5). round2-advocate-B E-2 calls the guard a "paper design" and E-5 gives a deadline, but neither tests the absence path or the shadow-guard gap.

ID: INV-020
CATEGORY: sufficiency_challenge
ASSUMPTION: CLAIM "no capability moves now keeps INV-L and the 36 verdict-map tests intact".
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE: Proof by file enumeration. Consensus changes: `SKILL.md` (`### 4.3a` plus widened sections), `refs/reviewer-spec.md:51, :57, :78`, `sc-tasklist-protocol/SKILL.md`, `task-builder/SKILL.md`, `scripts/reflect_shadow_exit.py` (`:313`, parity move), `tests/cli/reflect/test_shadow_skill_contract.py:65`, new helper modules and tests. Not changed: `RF/contract.py`, `RF/ensemble.py`, `RF/runner.py`, `RF/fallback.py`, `tests/cli/reflect/test_verdict_mapping.py` (36 tests per diff-analysis V-04, `derive_verdict` only reads a dict, `RF/contract.py:138-260`). So the 36 tests hold by construction. INV-L holds only conditionally on INV-001 (sibling switch) and on INV-016; the debate records INV-L as endangered at three points (round2-advocate-B E-1).

