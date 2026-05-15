# S2 Adversarial Debate Transcript

**Solution**: S2 — Route Manifest Findings to Roadmap Target
**Reviewer**: adversarial / root-cause analyst
**Date**: 2026-05-15

---

## 1. Evidence reviewed

- `spec-fidelity.md`: 3-run convergence, structural HIGH = 15 → 15 → 10, halted
  with 10 active HIGHs, TurnLedger exhausted (consumed=46, available=15).
- `deviation-registry.json`: 10 ACTIVE findings (6 data_models/file_missing, 4
  nfrs — encryption/hash/<1%/<2%); 5 FIXED in Run 2
  (signatures/phantom_id D-001 + SC-001..SC-004). **Every finding has
  `files_affected: []`.**
- `_make_finding` (`structural_checkers.py:117`): **does not accept a
  `files_affected` argument.** Confirmed: the helper constructs a `Finding`
  with no `files_affected`, so the dataclass default (`[]`) is what ships.
- `semantic_layer.py:514`: same omission for semantic findings.
- `enforce_allowlist` (`remediate_executor.py:173`): SKIPS findings with
  empty `files_affected` (with a WARNING). So in theory remediation should
  no-op, not corrupt the spec — but the failing run shows it DID corrupt
  the TDD. Inference: a different code path (convergence executor) is
  bypassing `enforce_allowlist` or providing the spec file as a default
  target. The 71.3%/38.1% diffs against the TDD prove the agent touched it.
- `build_remediation_prompt` (`remediate_prompts.py:17`): emits the bare
  `fix_guidance` field. `_make_finding` sets that field to
  `"Address {mismatch_type} in {dimension} dimension"` — generic boilerplate
  with no actionable instruction.
- `_check_diff_size` (`remediate_executor.py:367`): whole-file 30% guard
  (changed_lines / max_lines). `check_patch_diff_size` (line 311) is the
  per-patch variant but is only used when `RemediationPatch` objects exist;
  convergence path uses the whole-file check.
- `MAX_WORKERS = len(all_target_files)` (line 775): one-file → one worker,
  ten findings → one prompt stack.

## 2. Attacks raised

**A1. Does the agent know HOW to add a manifest row?**
Original S2 just says "point `files_affected` at the roadmap." But the
`fix_guidance` field is the only actionable instruction the agent gets, and
it's "Address file_missing in data_models dimension." Useless. Even with
correct routing, the agent will guess — probably by regenerating the entire
section, again tripping the diff guard.

→ **FORCED REFACTOR**: §4 Prompt-template adjustments. `_make_finding` now
emits a templated, mismatch-specific `fix_guidance` ("Add a row referencing
`{spec_quote}` to the File Manifest section…"). Plus a Constraints-section
nudge to prefer small additive edits.

**A2. Single-file bottleneck and diff bloat (issue (b))**
Ten findings all routed to `roadmap.md` → one ThreadPoolExecutor worker →
one giant patch. On a small roadmap (~30 lines), adding 10 manifest rows +
4 NFR lines = ~14 added lines / max(44) lines ≈ 32% — STILL TRIPS THE 30%
GUARD.

→ **PARTIAL REFACTOR**: §5 Chunking strategy documented as three layers.
Layer A (per-patch guard) already exists in code but isn't on the
convergence path. Layer B (cap findings per agent, sequential calls)
explicitly scoped OUT of this release as a known limitation. Layer C
relies on the templated guidance keeping each fix to ~1 line. Honest
residual risk: very small roadmaps may still fail. Mitigation: if Layer C
proves insufficient in practice, the failure mode is now visible and
diagnosable (one agent, one file) — vastly cleaner than the current
"corrupts the spec" state.

**A3. Spec-defect mis-routing (issue (c))**
"Security primitive 'encryption' from spec NFRs not addressed in roadmap"
could mean (i) the roadmap is missing it, or (ii) the spec mentioned
encryption but it's not actually a project requirement (spec defect).
Blindly routing to `roadmap.md` would force the agent to invent an NFR.

→ **FORCED REFACTOR**: §3 Ambiguous-case fallback. `nfrs/security_missing`
is now routed to `roadmap.md` BUT carries `deviation_class="AMBIGUOUS"`
and a bi-conditional `fix_guidance` that explicitly tells the agent: add
NFR to roadmap, OR document the deviation in `extraction.md` (which is
already on the EDITABLE_FILES allowlist). The spec is never modified.
Conceded: this is a soft control — a determined agent could still
hallucinate. Stricter solution would need human-in-the-loop, out of scope.

**A4. Tests** (issue (d))
Tests in `tests/roadmap/test_structural_checkers.py` don't reference
`_make_finding` directly (grepped, no hits), so adding an argument is
non-breaking. New assertions for `files_affected` are additive.

→ **SURVIVED**: documented in §6 with concrete test cases.

**A5. Phantom-ID cascade**
Removing `SC-001` from the roadmap may leave orphan cross-references
elsewhere in the roadmap (broken markdown anchors, dangling cross-link
text). The original solution didn't address this.

→ **REFACTORED**: §1 risks added a note; the templated `fix_guidance` for
`phantom_id` now says "Remove the reference to `{roadmap_quote}` from the
roadmap (the ID is not defined in the spec)" with an implied "and update
any references to it." A separate follow-up could add a referential-integrity
checker.

**A6. `spec_quote`/`roadmap_quote` quoting in templated guidance**
F-string interpolation of regex match groups (e.g.,
`Step(name=foo, type=bar)`) into a `fix_guidance` string is generally safe
because markdown doesn't treat parens/equals as control chars. But if a
spec_quote contains a literal `}` (rare in Python code blocks but possible
in YAML), naive f-string interpolation could break. Recommended a
`_safe_fmt` helper if it shows up in practice.

→ **NOTED AS RESIDUAL RISK** in §Risks, not blocking.

## 3. Attacks that survived

- **A1 (no actionable instruction)** — fully addressed via templated
  `fix_guidance` + Constraints nudge.
- **A3 (spec-defect mis-routing)** — addressed for `security_missing` with
  AMBIGUOUS class + bi-conditional guidance. Other NFR mismatch types
  (`threshold_contradicted`, `coverage_mismatch`) are lower-risk because
  they compare concrete values, not the existence of a concept.
- **A4 (tests)** — additive changes only, no regressions.
- **A5 (phantom-ID cascade)** — templated guidance includes a removal
  instruction. A future referential-integrity pass would harden this.

## 4. Attacks that forced refactors

- **A1** → added §4 (prompt-template adjustments). This is the **single
  most important change** the debate produced. Without it, S2 would still
  fail because correct routing without correct instructions still yields
  regenerative agent behavior.
- **A2** → added §5 (chunking layers), with Layer B explicitly scoped OUT
  as a Phase 2 follow-up. The original S2 hand-waved this as "the roadmap
  is short and edits are additive." That's not always true; now it's a
  named residual risk with a follow-up.
- **A3** → added §3 (ambiguous routing) for `nfrs/security_missing`.
  Original solution implicitly assumed the spec was always right.

## 5. Residual concerns

1. **Very small roadmaps may still trip the 30% guard** even with
   templated guidance. Diagnosable post-Phase 1; mitigated by Phase 2 §5
   Layer B.
2. **`AMBIGUOUS` is a soft control.** The agent may ignore the
   bi-conditional fix_guidance. Mitigation: prompt template enforces it
   structurally (a dedicated "Choose ONE of these two paths" block could
   be added in a future iteration).
3. **Convergence path uses whole-file diff guard**, not per-patch.
   Migrating it is non-trivial because callers expect different return
   shapes. Documented in "Out of scope" §Phase 2.
4. **`semantic_layer.py` Finding construction is duplicated logic.**
   Eventually `_make_finding` should be shared between structural and
   semantic layers. Not blocking.

## 6. Confidence scores

| Score | Value | Reasoning |
|---|---|---|
| **Standalone** | **78/100** | The routing fix is necessary AND now sufficient for the data_models manifest findings (6 of 10 in the failing case). The templated `fix_guidance` makes correct routing actionable. Remaining 4 (NFR/security/threshold) carry the soft-control AMBIGUOUS risk. Single-file bottleneck is a known unfixed risk for tiny roadmaps. |
| **Combined with other fixes** | **88/100** | Combined with the convergence executor's per-patch diff guard (S?, if proposed), the chunking limitation in §5 Layer B becomes moot. Combined with a prompt-template hardening fix (S?, if proposed) the AMBIGUOUS soft control becomes a structural choice the agent cannot bypass. With those two companion fixes S2 becomes the most direct, minimum-LOC path to convergence. |

## 7. Recommended sequencing

1. Land S2 as refactored (routing + templated guidance + AMBIGUOUS class).
2. Run the failing case end-to-end; verify 10 HIGHs → ≤2 in Run 1.
3. If small-roadmap diff bloat appears, land §5 Layer B as Phase 2.
4. Independently consider migrating convergence path to
   `check_patch_diff_size`.
