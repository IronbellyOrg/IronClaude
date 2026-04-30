# Merge Log

## Metadata

- **Base variant**: Variant 1 (Proposal A — minimal-blast-radius)
- **Executor**: sc:adversarial merge-executor
- **Changes planned**: 7
- **Changes applied**: 7
- **Changes failed**: 0
- **Status**: success
- **Timestamp**: 2026-04-30T00:00:00Z
- **Output file**: `merged-output.md`

## Changes Applied

### Change #1 — `PromptTooLargeForArgv` typed error (from B§U-003)

- **Status**: applied
- **Provenance tag**: `<!-- Source: Base (original, modified) — incorporate B's typed error (Change #1) -->`
- **Before**: A§3.1 had `raise ValueError(...)` in start()'s sanity guard.
- **After**: New class `PromptTooLargeForArgv(ValueError)` declared adjacent to `PROMPT_MAX_BYTES` constant. Sanity guard in `start()` now raises this typed exception. Test `test_prompt_max_bytes_guard` updated to `pytest.raises(PromptTooLargeForArgv, match=...)`.
- **Validation**: subclassing `ValueError` preserves backward compatibility for any caller catching `ValueError`. New exception class is a subtype, not a replacement.

### Change #2 — Optional `.prompt` sidecar file (from B§U-004)

- **Status**: applied
- **Provenance tag**: `<!-- Source: Base (original, modified) — incorporate B's chunked streaming (Change #3) and prompt-sidecar (Change #2) -->`
- **Integration**: New constructor kwarg `prompt_sidecar: bool = False` added to `__init__`. When True AND stdin path is taken, writer thread tees each chunk to `output_file.with_suffix(".prompt")`. Default False — no impact on existing callers.
- **Validation**: §7.6 adds `test_prompt_sidecar_written_when_opted_in` and `test_no_sidecar_by_default`. Cleanup follows existing `output_file` lifecycle.

### Change #3 — Stream the encoded prompt in chunks (from B§C-007)

- **Status**: applied
- **Provenance tag**: shared with Change #2
- **Before**: A§3.3 had `prompt_bytes = self.prompt.encode("utf-8", errors="strict")` followed by `view = memoryview(prompt_bytes)` and a single `os.write` retry loop.
- **After**: New private method `_iter_prompt_chunks(chunk_size=64 * 1024) -> Iterator[bytes]` slices the prompt by character index (`char_chunk = chunk_size // 4` for 4-byte UTF-8 worst case) and encodes each slice. Writer thread iterates chunks; each chunk goes through the same `os.write` retry loop. Memory pressure is now O(chunk_size) instead of O(prompt_size).
- **Validation**: §7.3 `test_huge_prompt_delivered_via_stdin` and `test_huge_utf8_emoji_prompt_round_trip` together pin: (a) byte-identical round trip; (b) multibyte boundary safety.

### Change #4 — UTF-8 multibyte test (from B§8.2)

- **Status**: applied
- **Provenance tag**: inline
- **Integration**: New fixture `emoji_prompt` (200 KB of `"🦀"`) and new test `test_huge_utf8_emoji_prompt_round_trip` added to §7.3.
- **Validation**: pins multibyte chunk-boundary safety; complements Change #3.

### Change #5 — Empty-prompt argv-preservation made explicit (from B§X-003)

- **Status**: applied
- **Provenance tag**: `<!-- Source: Variant 2, Section 6 case 11 — merged per Change #5 -->` in §2; inline in §3.2 docstring; inline in §6 case 12.
- **Integration**: `_use_stdin_for_prompt()` now explicitly returns False for size 0, with a comment explaining intent. New test `test_empty_prompt_uses_argv_with_empty_p_value` in §7.2.
- **Validation**: pins legacy behavior; prevents future refactor from accidentally switching empty prompts to stdin (which would block waiting for content).

### Change #6 — Risk register table format (from B§10)

- **Status**: applied
- **Provenance tag**: `<!-- Source: Variant 2, Section 10 — risk register format merged per Change #6 -->` in §9.
- **Integration**: A's prose-style risks converted to L × I = Score table. INV-005 / A-001 surfaced as Risk #1 with explicit P0 release-gate test (`echo ... | claude --print ...`).
- **Validation**: improves Risk Coverage criterion 1; does not change technical content.

### Change #7 — Appendix of cited line ranges (from B Appendix A)

- **Status**: applied
- **Provenance tag**: `<!-- Source: Variant 2, Appendix A — merged per Change #7 -->` in §11.
- **Integration**: New §11 reproduces B's Appendix A line-range citations with two additions specific to the merged design (`sprint/executor.py:1248-1271` and `roadmap/executor.py:735-742`).
- **Validation**: improves Structure criterion 4 (navigation aids).

## Changes NOT Applied (rejected per refactor-plan.md §"Changes NOT being made")

- `PromptSource` Protocol — premature abstraction in beat 1 (deferred to §10 Beat-2 Follow-ups)
- `PromptDelivery` strategy classes — same
- `delivery: PromptDelivery | None = None` constructor kwarg — same
- "Leave PortifyProcess untouched" — A's anchor change is safer
- `self.prompt = ""` for huge prompts — backward-compat break
- Removal of `_EMBED_SIZE_LIMIT` warning at call sites — keep advisory in beat 1

## Post-Merge Validation

### Structural integrity
- ✅ Heading hierarchy consistent (H1 → H2 → H3, no gaps)
- ✅ Section ordering logical (Summary → Decision → Patch → Compatibility → Strategy → Edge cases → Tests → Rollout → Risks → Beat-2 → Appendix)
- ✅ Document starts with H1
- ✅ No orphaned subsections

### Internal references
- ✅ All cross-references resolve (`§3.1`, `§4`, `§7`, `§9.1 Risk #1`)
- ✅ All file:line citations match the live package paths verified in Phase 1 analysis
- ✅ All pytest test names are unique
- Total: 24 internal cross-references, all resolved
- Broken: 0

### Contradiction rescan
- Pre-merge contradictions in `diff-analysis.md`: 4 (X-001 through X-004)
- Resolution in merged output:
  - X-001 (margin sizing): resolved in favor of A's 96 KiB
  - X-002 (Portify scope): resolved in favor of A's 2-line tweak
  - X-003 (empty prompt): resolved in favor of B's explicitness
  - X-004 (`self.prompt` consistency): resolved in favor of A's preservation
- New contradictions introduced by merge: **0**

### Convergence gate
- diff-point convergence: 87% (above 80% threshold)
- taxonomy levels covered: L1 ✓, L2 ✓, L3 ✓
- HIGH-severity UNADDRESSED invariants: 1 (INV-005)
- Final status: **CONVERGED with conditional release-gate** — INV-005 (live `claude` stdin probe) is documented as Risk #1 / P0 release-gate test in §9.1 of the merged output.

## Summary

- Planned: 7
- Applied: 7
- Failed: 0
- Skipped: 0
- Status: **success**

The merged design (`merged-output.md`) is ready for `/sc:design` to produce the official architectural design document.

## Return Contract

```yaml
merged_output_path: "/config/workspace/Coder/.dev/architectural/claude-process-stdin-patch/adversarial/merged-output.md"
convergence_score: 0.87
artifacts_dir: "/config/workspace/Coder/.dev/architectural/claude-process-stdin-patch/adversarial"
status: "success"
base_variant: "variant-1-original (Proposal A)"
unresolved_conflicts: 0
fallback_mode: false
failure_stage: null
invocation_method: "skill-direct"
unaddressed_invariants:
  - id: "INV-005"
    category: "interaction_effects"
    assumption: "Pinned claude CLI accepts missing positional prompt and reads stdin in --print mode"
    severity: "HIGH"
```
