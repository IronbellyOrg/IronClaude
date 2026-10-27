# Spec Panel Review — TDD Skill Refactor Spec

Reviewed spec: `/config/workspace/IronClaude/.dev/releases/backlog/tdd-skill-refactor/tdd-refactor-spec.md`
Mode: `critique`
Focus: `correctness, architecture`
Date: 2026-04-02

## Executive Assessment

- **Overall quality**: strong structure, good decomposition intent, clear acceptance criteria scaffolding.
- **Gate result**: **FAIL (requires edits before implementation)**.
- **Primary blockers**:
  1. **Source-of-truth pathing is architecturally inconsistent** with repo rules (spec targets `.claude/skills/tdd/*` as implementation location instead of `src/superclaude/skills/tdd/*` first).
  2. **Correctness invariants are underspecified** for the fidelity process (what exactly counts as “zero drift” under allowed path updates is not formally encoded).
  3. **Phase-loading contract is not machine-verifiable as written** (no explicit negative assertions per phase for disallowed refs).

---

## Prioritized Recommendations (actionable, immediate edits)

| Priority | Severity | Target section/lines | Required edit |
|---|---|---|---|
| P0 | CRITICAL | **Sections 1.1, 3 (FR-TDD-R.2..R.5), 4.1, 4.2, 8, Appendix B** — lines **35, 102-103, 113-114, 124-125, 135-136, 169-173, 179, 371-378** | Replace implementation target paths from `.claude/skills/tdd/...` to **`src/superclaude/skills/tdd/...`** as canonical. Add explicit step: sync to `.claude/` via `make sync-dev` and validate via `make verify-sync`. Keep `.claude/...` as dev-copy validation target only. |
| P0 | CRITICAL | **FR-TDD-R.7** — lines **154-160** | Formalize fidelity invariant to resolve exception ambiguity: define an allowlist for permitted edits (e.g., path-reference rewrites only), and define exact drift check method (normalized diff + checksum markers + block ID map). Current text conflicts between “word-for-word” and “except path ref updates.” |
| P1 | MAJOR | **Section 5.3 phase_contracts** — lines **216-249** | Add explicit `forbidden_loads` per phase and deterministic validation rule (e.g., if loaded_ref ∉ declared_loads then fail). Current “no unnecessary refs” is not fully testable without explicit negatives. |
| P1 | MAJOR | **Section 8 Test Plan** — lines **274-287** | Add concrete test commands and pass/fail thresholds (e.g., exact scripts/checks for line-budget, block-diff, contract conformance). Avoid non-measurable “functional parity dry run” without oracle definition. |
| P1 | MAJOR | **Section 4.6 Implementation Order** — lines **203-209** | Insert prerequisite ordering: update canonical `src/` first, then run sync/verify, then run fidelity checks against canonical source, then dev-copy parity checks. |
| P2 | MAJOR | **Open Items OI-01/OI-02** — lines **315-317** | Convert open items into resolved requirement text or explicit decision gate with owner/date. Current ambiguity can produce divergent implementations. |
| P2 | MINOR | **Section 2.2 + 4.4 + 5.3** — lines **66-80, 189-198, 216-249** | Harmonize terminology (`load`, `reference`, `reads`) and actor naming (`orchestrator`, `builder`) into one contract dictionary to prevent interpretation drift in tests and automation. |

---

## Architecture Findings

### 1) Canonical-path violation (CRITICAL)
- The spec operationally treats `.claude/skills/tdd/*` as the primary edit target (multiple acceptance criteria and file tables).
- Project rules define **`src/superclaude/` as source of truth** and `.claude/` as synced dev copies.
- This is a release-quality correctness issue: implementation could pass local checks while diverging from distributable source.

**Fix**: update all implementation requirements to target `src/superclaude/skills/tdd/*`, then add explicit sync/verify steps and acceptance criteria for parity.

### 2) Incomplete contract for allowed transformations (MAJOR)
- Requirements claim both “word-for-word migration” and “path-reference updates allowed.”
- Without a formal transformation allowlist, reviewers can disagree on what edits are legal.

**Fix**: add a transformation contract table:
- Allowed: path token replacements in BUILD_REQUEST cross-refs only.
- Forbidden: wording edits, header renames, numbering changes, checklist reorder, markdown table schema changes.
- Validation: normalized diff by block ID + checksum markers + explicit exception log.

### 3) Phase contract not fully enforceable (MAJOR)
- `phase_contracts` defines what loads should happen but does not encode explicit prohibited loads.
- Enforcement is weaker for regression prevention.

**Fix**: add `forbidden_loads` arrays for each phase and test rule `declared_loads ∩ forbidden_loads = ∅`.

---

## Correctness Findings (with adversarial framing)

1. **I can break this specification by Divergence Attack.** The invariant at **FR-TDD-R.7 (lines 154-160)** fails when **path updates alter non-path textual tokens but still pass informal review**. Concrete attack: **Before: block text includes section prose. Attack: replace adjacent wording while updating refs. After: semantic drift introduced but interpreted as allowable path update.**
- Severity: **CRITICAL**

2. **I can break this specification by Sequence Attack.** The invariant at **Section 4.6 (lines 203-209)** fails when **implementation edits `.claude/` first, then sync direction is reversed or skipped**. Concrete attack: **Before: src and dev copy aligned. Attack: patch dev copy only and run partial checks. After: repository ships stale `src/` content.**
- Severity: **CRITICAL**

3. **I can break this specification by Zero/Empty Attack.** The invariant at **FR-TDD-R.7 + Section 8.1 (lines 157-159, 276-279)** fails when **fidelity index has empty block mappings or missing checksum endpoints**. Concrete attack: **Before: expected B01-B34 map. Attack: one block mapping left blank. After: test still passes if script checks only file existence.**
- Severity: **MAJOR**

4. **I can break this specification by Sentinel Collision Attack.** The invariant at **placeholder sentinel test (line 278, line 159)** fails when **legitimate instructional text matches sentinel pattern heuristics**. Concrete attack: **Before: real content includes placeholder-like token in examples. Attack: naive scanner flags and blocks valid output, or ignores true unresolved sentinel due to broad ignore list.**
- Severity: **MAJOR**

5. **I can break this specification by Accumulation Attack.** The invariant at **Section 2.2 / 4.4 pipeline (lines 66-80, 189-198)** fails when **added refs grow over time and phase constraints are not re-baselined**. Concrete attack: **Before: 5 refs. Attack: add 2 new refs without updating phase contracts. After: hidden token creep and undeclared loads.**
- Severity: **MAJOR**

---

## Mandatory Artifact — State Variable Registry

| Variable Name | Type | Initial Value | Invariant | Read Operations | Write Operations |
|---|---|---|---|---|---|
| `skill_line_count` | integer | unknown (pre-refactor) | `< 500` post-refactor | line-budget test, CI checks | SKILL.md edits |
| `source_block_count` | integer | 34 (B01-B34) | conserved across destination mapping | fidelity index audit | mapping manifest updates |
| `mapped_block_count` | integer | 0 | must equal `source_block_count` | fidelity verification | migration execution |
| `allowed_transformations` | set | undefined | only approved transformations allowed | diff validator | spec policy updates |
| `declared_phase_loads` | map(phase->set) | from Section 5.3 | runtime loads subset of declarations | phase matrix test | spec contract edits |
| `forbidden_phase_loads` | map(phase->set) | not defined | no runtime load appears in forbidden set | contract conformance tests | spec contract edits |
| `placeholder_count` | integer | unknown | must be 0 in outputs | sentinel scanner | generated artifacts |
| `src_dev_sync_state` | enum {unknown, synced, drifted} | unknown | must be `synced` after implementation | verify-sync | sync-dev + edits |

---

## Mandatory Artifact — Guard Condition Boundary Table

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `skill_line_count < 500` | FR-TDD-R.1 (line 89) | Zero/Empty | 0 lines | true | would pass mathematically but invalid artifact | GAP |
| `skill_line_count < 500` | FR-TDD-R.1 (line 89) | One/Minimal | 1 line | true | no minimum viable content constraint defined | GAP |
| `skill_line_count < 500` | FR-TDD-R.1 (line 89) | Typical | 420 lines | true | acceptable | OK |
| `skill_line_count < 500` | FR-TDD-R.1 (line 89) | Maximum/Overflow | 500 lines | false | fail expected | OK |
| `skill_line_count < 500` | FR-TDD-R.1 (line 89) | Sentinel Value Match | 499 with hidden includes | true (apparent) | include-resolution behavior unspecified | GAP |
| `skill_line_count < 500` | FR-TDD-R.1 (line 89) | Legitimate Edge Case | 499 with duplicated boundaries omitted | true | completeness check unspecified | GAP |
| `textual_drift == 0` | FR-TDD-R.2..R.5, R.7 (lines 99-137, 154-160) | Zero/Empty | empty destination block | false | should fail, but failure oracle not formalized | GAP |
| `textual_drift == 0` | FR-TDD-R.2..R.5, R.7 | One/Minimal | 1-char diff | false | should fail | OK |
| `textual_drift == 0` | FR-TDD-R.2..R.5, R.7 | Typical | exact verbatim | true | pass | OK |
| `textual_drift == 0` | FR-TDD-R.2..R.5, R.7 | Maximum/Overflow | many diffs | false | fail | OK |
| `textual_drift == 0` | FR-TDD-R.5 exception (line 132) | Sentinel Value Match | path update touches nearby prose | ambiguous | exception boundary unspecified | GAP |
| `textual_drift == 0` | FR-TDD-R.7 | Legitimate Edge Case | newline/whitespace-only changes | ambiguous | normalization policy unspecified | GAP |
| `loaded_ref ∈ declared_phase_loads` | Section 5.3 (lines 216-249) | Zero/Empty | no refs loaded | true in A.1-A.6 | pass expected | OK |
| `loaded_ref ∈ declared_phase_loads` | Section 5.3 | One/Minimal | only build-request-template in A.7 | true | pass expected | OK |
| `loaded_ref ∈ declared_phase_loads` | Section 5.3 | Typical | all declared builder refs loaded | true | pass expected | OK |
| `loaded_ref ∈ declared_phase_loads` | Section 5.3 | Maximum/Overflow | undeclared extra ref loaded | false | rejection mechanism unspecified | GAP |
| `loaded_ref ∈ declared_phase_loads` | Section 5.3 | Sentinel Value Match | alias/symlink path to ref | ambiguous | path canonicalization unspecified | GAP |
| `loaded_ref ∈ declared_phase_loads` | Section 5.3 | Legitimate Edge Case | declared ref not loaded though required | ambiguous | required-vs-optional semantics not fully explicit | GAP |
| `placeholder_count == 0` | FR-TDD-R.7 + 8.1 (lines 159, 278) | Zero/Empty | 0 | true | pass | OK |
| `placeholder_count == 0` | FR-TDD-R.7 + 8.1 | One/Minimal | 1 unresolved token | false | fail | OK |
| `placeholder_count == 0` | FR-TDD-R.7 + 8.1 | Typical | few placeholders resolved | true | pass | OK |
| `placeholder_count == 0` | FR-TDD-R.7 + 8.1 | Maximum/Overflow | many unresolved tokens | false | fail | OK |
| `placeholder_count == 0` | FR-TDD-R.7 + 8.1 | Sentinel Value Match | legitimate literal token resembles placeholder | ambiguous | detection precision unspecified | GAP |
| `placeholder_count == 0` | FR-TDD-R.7 + 8.1 | Legitimate Edge Case | escaped placeholder in code sample | ambiguous | handling rule unspecified | GAP |

**Gate implications**:
- Per FR-8/FR-9 equivalents in your panel template quality gates, every `GAP` above should be elevated to at least **MAJOR** until specified.

---

## Mandatory Artifact — Quantity Flow Diagram (Pipeline Dimensional Analysis)

Triggered by Section 2.2 + Section 4.6 multi-stage decomposition pipeline.

```text
[Source SKILL.md: 1364 lines, blocks B01-B34]
    --> [Stage 1: Partition by block ranges]
            in: 34 blocks
            out: 34 blocks (0 loss required)
    --> [Stage 2: Relocate to destinations]
            in: 34 blocks
            out: 34 blocks across {SKILL core + 5 refs}
            divergence point: 1 source file -> 6 destination files
    --> [Stage 3: Path reference rewrites (allowed subset)]
            in: K references
            out: K rewritten references
            divergence risk: K' > K if accidental edits introduced
    --> [Stage 4: Sync canonical -> dev copy]
            in: src/superclaude/skills/tdd/*
            out: .claude/skills/tdd/*
            mismatch risk if stage skipped or reversed
    --> [Consumers]
            - fidelity verifier expects 34 mapped blocks
            - phase loader tests expect declared refs only
            - maintainers expect source-of-truth in src/
```

**Critical mismatch identified**: current spec routes implementation primarily through `.claude/...`, while architecture rules require `src/...` first. This is a pipeline contract break.

---

## Suggested Patch Points (minimal edits)

1. **Section 4.1 New Files**: duplicate each path row as canonical `src/...` and synced `.claude/...` artifact, with canonical flagged as authoritative.
2. **Section 4.6 Implementation Order**: prepend step 0: “Edit/create files under `src/superclaude/skills/tdd/` only.” Add final steps for `make sync-dev` and `make verify-sync`.
3. **FR-TDD-R.2..R.5 acceptance criteria**: replace absolute `.claude` existence checks with dual checks: canonical exists + synced dev copy exists after sync.
4. **FR-TDD-R.7**: add an “Allowed Transformations” sub-bullet list and “Normalization Rules” for diffing.
5. **Section 8**: include explicit command-level checks and expected outputs for each test.

---

## Final Verdict

This spec is close, but not implementation-safe yet. Apply the P0/P1 edits above before task generation. Once canonical pathing and fidelity invariants are formalized, the plan should meet both correctness and architecture quality gates with low residual risk.
