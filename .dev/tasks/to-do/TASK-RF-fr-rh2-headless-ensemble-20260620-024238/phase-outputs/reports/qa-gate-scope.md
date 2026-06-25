# FINAL QA Gate — Review Scope Manifest

Date: 2026-06-20
This is the single entry-point the 6 lens agents read. Every implementation file
and evidence artifact under review for FR-RH2 is listed with its purpose and the
FR-RH2.N/NFR-RH2.N it serves.

## Source files (implementation)

| File | Purpose | Serves |
|------|---------|--------|
| `src/superclaude/cli/reflect/ensemble.py` | NEW Tier-2 driver: swarm dispatch fan-out + reduce + OI-1 contract mapping + adversarial Mode-A scorer handoff | FR-RH2.1, .3, .4, .9; NFR-RH2.1, .2, .5, .7, .8 |
| `src/superclaude/cli/reflect/runner.py` | `_audit_once` rewire: Tier-2 → ensemble; Tier-1 ClaudeProcess unchanged (spec §9 identity seam) | FR-RH2.1; NFR-RH2.2, .6 |
| `src/superclaude/cli/reflect/contract.py` | derive_verdict + Verdict map (UNCHANGED — preserved) | FR-RH2.7 |
| `src/superclaude/cli/reflect/config.py` | resolve_config: `transport`/`reviewers` fields + Q8 pre-clamp | §5.1 CLI surface |
| `src/superclaude/cli/reflect/models.py` | ReflectConfig fields `transport`/`reviewers`; Verdict enum (untouched) | §5.1; FR-RH2.7 |
| `src/superclaude/cli/reflect/commands.py` | `--transport`/`--reviewers` Click options | §5.1, §5.3 transport_enum |
| `src/superclaude/cli/swarm/lenses/reflect_review.py` | NEW reflect-review lens (suspect, T2, default_workers 3, /sc:adversarial, no model literal) | FR-RH2.2 |
| `src/superclaude/cli/swarm/lenses/templates/reflect-review-output.md` | NEW per-reviewer output template (frontmatter + Suspect files) | FR-RH2.2 |
| `src/superclaude/cli/swarm/lenses/__init__.py` | 3 registry edits (import + LENS_NAMES + LENSES), import-order fix | FR-RH2.2 |

## Test files

| File | Purpose | Serves |
|------|---------|--------|
| `tests/cli/reflect/test_ensemble_unit.py` | U1-U9 unit matrix | FR-RH2.2,.4,.7,.8; NFR-RH2.1,.5,.8 |
| `tests/cli/reflect/test_ensemble_stub_integration.py` | I1-I9 non-mocked stub witnesses | FR-RH2.1,.3,.4,.5,.6,.7,.9; NFR-RH2.3,.4,.7 |
| `tests/cli/reflect/test_no_nesting_guard.py` | NFR-7 guard extended to ensemble.py | FR-RH2.8; NFR-RH2.1,.2 |

## Decision records / discovery

- `phase-outputs/decisions/q6-mzero-slug-decision.md` — Q6 → Option B (`contract-missing`)
- `phase-outputs/decisions/adversarial-seam-decision.md` — Option (b), launch site ensemble.py
- `phase-outputs/discovery/oi1-mapping-table-validated.md` — validated 20-row provenance (6 DERIVED + 2 MAPPED + 12 SYNTHESIZED)
- `phase-outputs/reports/dod-traceability-matrix.md` — FR/NFR → test → evidence

## Evidence (test-results)

- `phase2-u1u2-output.txt`, `phase3-u3u4u5u6u8-output.txt`, `phase5-transport-reviewers-output.txt`
- `phase4-reflect-floor-output.txt`, `phase8-final-floor-output.txt`
- `phase6-i1-output.txt` … `phase6-i9-output.txt`, `phase6-integration-full-output.txt`
- `phase7-u7u9-guard-output.txt`

## Spec / TDD oracle

- Spec (WINS on wording conflict): `.dev/reflect-hardening/issue-2-headless-ensemble/spec.md`
- TDD (paths/signatures/§15 test ids): `.dev/reflect-hardening/issue-2-headless-ensemble/tdd.md`

No omissions: every NEW or MODIFIED file for FR-RH2 is listed above.
