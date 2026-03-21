# ISS-020: fidelity.py is dead code

## Status Check
- Superseded by upstream? **NO** — No CRITICAL, HIGH, or MEDIUM issue addresses fidelity.py. ISS-008 covers deviation_registry.py extraction, and ISS-001/002/003 cover convergence.py, semantic_layer.py, and remediate_executor.py respectively, but none touch the `relates_to` frontmatter entry for fidelity.py. This LOW issue is independent.

## Proposal A: Remove fidelity.py from relates_to frontmatter

Since fidelity.py has zero imports across the entire codebase and is superseded by Finding + DeviationRegistry, the spec should stop listing it as a related file. The file itself is a codebase cleanup task (delete dead code), not a spec concern, but the spec's frontmatter should not reference a file that will be deleted.

**Before** (spec line 16, YAML frontmatter `relates_to` list):
> ```yaml
>   - src/superclaude/cli/roadmap/fidelity.py
> ```

**After**:
> *(line removed entirely)*

## Proposal B: Replace with comment noting deprecation

If there is value in preserving traceability (documenting that the spec intentionally supersedes fidelity.py), replace the entry with an inline comment rather than silent removal.

**Before** (spec line 16, YAML frontmatter `relates_to` list):
> ```yaml
>   - src/superclaude/cli/roadmap/fidelity.py
> ```

**After**:
> ```yaml
>   # fidelity.py removed — dead code superseded by Finding (models.py) + DeviationRegistry (convergence.py/deviation_registry.py)
> ```

Note: YAML comments are valid syntax and will be ignored by parsers, but remain visible to human readers.

## Recommendation

**Adopt Proposal A** (simple removal). Rationale:
1. The `relates_to` field is a navigation aid, not a historical record. Listing a dead file actively misleads readers.
2. Traceability of the deletion is better served by the git commit message and this issue's record in issues-classified.md (ISS-020), not by a YAML comment in the spec frontmatter.
3. Proposal B adds clutter to an already long frontmatter list for marginal benefit.
