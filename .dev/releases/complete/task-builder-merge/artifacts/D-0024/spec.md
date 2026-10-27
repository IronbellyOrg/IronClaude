# D-0024 — T02.10 Spec: Verify NFR-CONV.7 evidence-bound preservation

**Task:** T02.10 (Phase 2)
**Roadmap items:** R-046
**Invariant under test:** NFR-CONV.7 — Per-item Context fields MUST
retain `file:line` citations OR `<!-- evidence-absence: ... -->`
justified-absence comments. Validated by TB-Add-8 (rf-qa.md:310;
SKILL.md:1073, 1826) on every per-item Context paragraph. The M2
introduction of the `## Execution Context` header (FR-CONV.2) MUST NOT
relax this invariant.

## Scope

Re-run the M1 TEST-003 three-fixture triple against M2-generated MDTM
that now carries the FR-CONV.2 `## Execution Context` header. Assert
the verdict matrix (bare-path FAIL / file:line PASS / justified-absence
PASS) is byte-identical to the M1 baseline, and that TB-Add-8 error
citations continue to refer to per-item Context fields — never to the
header byte range.

## Deliverables

1. Three frozen M2-style MDTM fixtures under
   `tests/audit/fixtures/execution_context/`:
   - `evidence_bound_bare_path.md` — bare module path, no `:N` line
     anchor, no justified-absence comment → TB-Add-8 must FAIL.
   - `evidence_bound_file_line.md` — Context cites
     `src/superclaude/agents/rf-qa.md:310` and
     `src/superclaude/skills/task-builder/SKILL.md:1073` → TB-Add-8 must
     PASS.
   - `evidence_bound_justified_absence.md` — Context carries an
     `<!-- evidence-absence: ... -->` justification → TB-Add-8 must PASS.
2. TB-Add-8 verifier `tests/audit/test_evidence_bound_tb_add_8.py`
   implementing the rule defined at `rf-qa.md:310` and exercising the
   three fixtures.
3. NFR-CONV.7 preservation report at `D-0024/evidence.md`.

## Acceptance criteria (mirrors phase-2-tasklist.md:492-496)

- AC1. TEST-003 triple re-run produces FAIL/PASS/PASS verdicts unchanged
  from M1.
- AC2. TB-Add-8 error citations refer to per-item Context fields, not
  the header.
- AC3. NFR-CONV.7 preservation report written to `D-0024/evidence.md`.
- AC4. Per-item Context fields retain `file:line` form post-M2.

## Source-of-truth references

- TB-Add-8 rule text: `src/superclaude/agents/rf-qa.md:310`
- TB-Add-8 A.10 mirror: `src/superclaude/skills/task-builder/SKILL.md:1073`
- TB-Add-8 checklist mirror: `src/superclaude/skills/task-builder/SKILL.md:1826`
- NFR-CONV.7 evidence-bound invariant: `src/superclaude/agents/rf-task-builder.md:417`
- Roadmap row R-046: `.dev/releases/current/task-builder-merge/roadmap.compressed.md:157`
