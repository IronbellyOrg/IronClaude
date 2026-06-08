# Research Notes: MultiModelSwarm Anti-Instinct Audit Remediation

**Date:** 2026-05-31
**Scenario:** A (explicit — full proposal already provided line-level fix scope)
**Depth Tier:** Quick (well-scoped, ≤8 files touched, single concern)
**Track Count:** 1

---

## EXISTING_FILES

| File | Purpose | Current state | Edit type |
|---|---|---|---|
| `.dev/releases/Current/MultiModelSwarm/roadmap.md` | Failed audit roadmap (71KB) | 6 "stub transport" refs (lines 207, 211, 213); missing `normalizer_strategy`/`final_path`/`MULTIMODEL` fingerprints | Roadmap rename + additive rows + frontmatter |
| `src/superclaude/cli/roadmap/fingerprint.py` | Spec fingerprint extractor/coverage checker | `_EXCLUDED_CONSTANTS` frozenset lines 30-86 already excludes MUST/SHALL/SHOULD/YAML/JSON/TODO; missing HTML/WILL/UNADDRESSED | Add 3 constants + docblock |
| `tests/roadmap/test_fingerprint.py` | Unit tests for fingerprint extractor (NOTE: actual path is `tests/roadmap/`, NOT `tests/cli/roadmap/` as proposal hinted) | `TestExpandedExcludedConstants` class at line 376 already covers MUST/SHALL/etc. — perfect home for new tests | Append test methods to existing class |
| `.dev/releases/Current/MultiModelSwarm/merged-requirements.compressed.md` | Compressed spec input to roadmap pipeline | Frontmatter has `spec_id: SPEC-MULTIMODEL-SWARM` but no `type` field | Annotate frontmatter with `type: Technical Design Document` |
| `.dev/releases/Current/MultiModelSwarm/.roadmap-state.json` | Pipeline state (anti-instinct step status=FAIL) | `tdd_file: null, prd_file: null, input_type: "spec"` | Set tdd_file path + input_type "tdd" |
| `.dev/releases/Current/MultiModelSwarm/anti-instinct-remediation.md` | THIS task's source spec | Authoritative scope | Read-only reference |

**Test path correction:** proposal said `tests/cli/roadmap/test_fingerprint.py` but the actual path is `tests/roadmap/test_fingerprint.py`. Task items must use the actual path.

## PATTERNS_AND_CONVENTIONS

**Fingerprint exclusion test pattern** (`tests/roadmap/test_fingerprint.py:376-411`):

```python
class TestExpandedExcludedConstants:
    def test_emphasis_words_excluded(self):
        for word in ["MUST", "SHALL", "SHOULD", "MANDATORY", "REQUIRED", "OPTIONAL"]:
            assert word in _EXCLUDED_CONSTANTS, f"'{word}' should be excluded"
```

Two-tier test pattern per category: (1) membership assertion (`word in _EXCLUDED_CONSTANTS`); (2) end-to-end extraction assertion against a representative spec fixture (`word not in texts` after `extract_code_fingerprints(spec)`).

**Source-of-truth flow** (from CLAUDE.md): edit `src/superclaude/cli/roadmap/fingerprint.py` → run `make sync-dev` if applicable (fingerprint.py is in cli/, not in `skills/` or `agents/` — sync-dev does not apply; pytest runs against `src/` directly via editable install).

**Python testing rules** (from global CLAUDE.md): UV only — `uv run pytest tests/roadmap/test_fingerprint.py -v`.

**Roadmap edit method:** the roadmap.md is a plain markdown file with YAML frontmatter; line numbers in proposal (207, 211, 213) refer to the audit-time snapshot. Implementer must re-confirm line numbers via grep before each Edit (lines may have shifted if other edits land first).

## GAPS_AND_QUESTIONS

1. **`make sync-dev` applicability** — fingerprint.py is core code (cli/), not a synced artifact. The CLAUDE.md sync rule applies to `src/superclaude/{skills,agents,commands,hooks,templates}`. The edit IS the source of truth, no `.claude/` mirror to sync. Task should NOT include a sync-dev step for fingerprint.py.
2. **`final_path` literal already in roadmap line 307** — verified via grep earlier: `grep -ic "final_path"` returned 0 on roadmap.md but grep with line numbers DID return line 307 with `final_path` in backticks. Re-verify before edit; the audit may have read a stale snapshot or the substring may be split across a markdown structure. Task includes a verify-first item.
3. **Spec_id format** — roadmap.md already has frontmatter, just append `spec_id: SPEC-MULTIMODEL-SWARM` line. No risk of conflict.
4. **`.roadmap-state.json` schema** — confirmed via Read earlier; fields `tdd_file`, `prd_file`, `input_type` already exist (set to null/"spec"). Edit is value-only.
5. **Re-run scope** — `superclaude roadmap run --resume` will pick up at `anti-instinct` step (currently FAIL). The audit re-run is the verification gate.

## RECOMMENDED_OUTPUTS

Single MDTM Template 02 task file at:
`.dev/tasks/to-do/TASK-MULTIMODELSWARM-AUDIT-REMEDIATION-20260531/TASK-MULTIMODELSWARM-AUDIT-REMEDIATION-20260531.md`

5 phases mapping to remediation .md sections:
- Phase 1: Preflight verification (read current state of 6 target files, confirm line numbers, capture pre-edit audit metrics)
- Phase 2: Scanner-side fix — `_EXCLUDED_CONSTANTS` + tests
- Phase 3: Roadmap-text fix — stub rename + frontmatter additions + content additions
- Phase 4: TDD-ingestion wiring — spec frontmatter + .roadmap-state.json
- Phase 5: Verification — re-run audit, inspect, document outcome

## SUGGESTED_PHASES

Single-track, sequential phases (each phase has at least one verification step before phase boundary). No parallelism within remediation execution — scanner edit must precede audit re-run; roadmap edit must precede audit re-run; both must complete before verification.

## TEMPLATE_NOTES

- **Template 02** (complex): multi-phase work with discovery (Phase 1 preflight), code edit (Phase 2), prose edit (Phase 3), config edit (Phase 4), verification (Phase 5).
- Per MDTM Template 02 rule B2: each item is self-contained (Context + Action + Output + Verification + Completion gate).
- Per rule A3: granular per-file/per-edit; no batched "fix all the things" items.
- Final phase contains the task-status-update item (anti-orphaning rule).
- Task tier metadata: STRICT (modifying core scanner code + production artifacts).

## AMBIGUITIES_FOR_USER

None — proposal is fully specified.
