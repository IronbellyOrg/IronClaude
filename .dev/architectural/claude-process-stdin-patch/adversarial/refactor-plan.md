# Refactor Plan — Merge B's strengths into base A

## Overview

- **Base variant**: Proposal A (`variant-1-original.md`)
- **Variants incorporated**: Proposal B (`variant-2-original.md`)
- **Change count**: 7 incorporations + 6 rejections
- **Risk profile**: Low (all incorporations are additive or local refinements; no architectural change)
- **Beats**: 1 — single-pass merge

## Planned Changes

### Change #1 — Add `PromptTooLargeForArgv` typed error (from B§U-003)

- **Source**: B§3.1 (last block) and B§8.3 negative test
- **Target location**: A§3.1 imports/constants section, A§3.3 `start()` method
- **Integration approach**: Define class adjacent to `PROMPT_MAX_BYTES`; raise it in the path where a caller could theoretically force-bypass `_use_stdin_for_prompt()` returning True (defensive — current callers never bypass, but the error type is the right ABI for future explicit-mode kwarg).
- **Rationale**: Debate confidence 90% (U-003). `OSError(7, "Argument list too long", "claude")` looks generic; a typed exception with delivery-mode context is catchable and documentable.
- **Risk level**: Low. Additive; no existing exception type changes.

### Change #2 — Optional `.prompt` sidecar file, opt-in (from B§U-004, B§7)

- **Source**: B§7 ("Add a prompt sidecar file alongside output_file")
- **Target location**: New constructor kwarg `prompt_sidecar: bool = False`; written by writer thread alongside the stdin write
- **Integration approach**:
  - Add `prompt_sidecar: bool = False` to `ClaudeProcess.__init__`. Default off (no disk-bloat for sprint/audit's high-frequency phases).
  - When `prompt_sidecar=True` AND stdin path is taken: writer thread tees each chunk to `self.output_file.with_suffix(".prompt")`.
  - When stdin path is not taken (small-prompt argv path): no sidecar (the prompt is already in argv and visible to anyone with access to the host).
  - Roadmap callers (where the original bug surfaced) opt in by default; sprint/audit opt out.
- **Rationale**: Debate confidence 80% (U-004 / C-006). Real observability gap when stdin mode hides the prompt from `ps`. Opt-in placates A's disk-bloat concern.
- **Risk level**: Low. Off by default; no impact unless explicitly enabled.

### Change #3 — Stream the encoded prompt in chunks rather than full-buffer (from B§C-007)

- **Source**: B§3.1 `iter_chunks(chunk_size=64 KB)` and B§5.3 (streaming for >1 MB)
- **Target location**: A§3.3 writer thread closure (replace `view = memoryview(prompt_bytes); ...; while n < total: written = os.write(fd, view[n:])` with chunked encode)
- **Integration approach**:
  - Keep the writer thread + `os.write` loop from A.
  - Replace the upfront `prompt_bytes = self.prompt.encode("utf-8", errors="strict")` with a small helper `_iter_prompt_chunks(chunk_size=64 * 1024) -> Iterator[bytes]` that slices `self.prompt` and encodes each slice.
  - The writer thread iterates chunks; each chunk goes through the same `os.write` retry loop.
  - The `PROMPT_MAX_BYTES` check still uses `len(self.prompt.encode("utf-8"))` upfront (one full encode for the size check; we can defer to a chunked-size estimator if memory pressure ever bites at this layer too — out of scope for beat 1).
- **Rationale**: Debate confidence 75% (C-007). For ≥10 MB prompts, A's full-buffer encode doubles peak heap. B's iterator approach unlocks O(1) memory streaming with the same robustness primitives.
- **Risk level**: Low-medium. Mid-codepoint splits are valid in a byte stream (B§6 case 4); we slice the **string**, encode each slice, and concatenate at byte level — no character-boundary corruption.

### Change #4 — Add UTF-8 multibyte test (from B§8.2)

- **Source**: B's `test_utf8_multibyte_round_trip`
- **Target location**: A§7.3 end-to-end test section
- **Integration approach**: Add a test case `test_huge_utf8_emoji_prompt_round_trip` with a 200 KB UTF-8 prompt of 4-byte emoji codepoints (`"🦀" * 50_000`).
- **Rationale**: Debate confidence 100% (uncontested). UTF-8 is the single most common production encoding hazard; A's plan didn't cover multibyte explicitly.
- **Risk level**: Low. Test addition only.

### Change #5 — Make empty-prompt argv-preservation explicit (from B§X-003)

- **Source**: B§6 case 11 (empty prompt → `-p ""` preservation)
- **Target location**: A§3.2 `_use_stdin_for_prompt()` method docstring; A§7 unit tests
- **Integration approach**:
  - Add explicit comment: `# Empty prompts (size 0) take the argv path with -p "" to preserve legacy behavior; we do not silently switch to stdin for empty strings.`
  - Add test `test_empty_prompt_uses_argv_with_empty_p_value`.
- **Rationale**: Debate confidence 75% (X-003). Implicit behavior is correct in A but could regress under future refactor; making it explicit prevents this.
- **Risk level**: Low.

### Change #6 — Risk register table format (from B§10)

- **Source**: B§10 risk register (L × I = Score, top 5)
- **Target location**: A§9 (currently "Open Questions") — rename to "Risk Register & Open Questions"
- **Integration approach**: Convert A's prose-style risks into a table with columns: Risk, Likelihood (L/M/H), Impact (L/M/H), Score (L×I), Mitigation. Keep A's open questions list separate.
- **Rationale**: Risk Coverage criterion 1 (B won 5/5 vs A's 4/5).
- **Risk level**: Low. Documentation polish.

### Change #7 — Appendix of cited line ranges (from B Appendix A)

- **Source**: B Appendix A
- **Target location**: New A§10 "Appendix: Cited Line Ranges"
- **Integration approach**: Copy B's appendix verbatim with adjustments for any line numbers A asserts differently. Acts as a quick-reference for code reviewers.
- **Rationale**: Structure criterion 4 (navigation aids).
- **Risk level**: Low.

## Changes NOT being made (rejected alternatives)

| Diff Point | Rejected approach (from B)                                        | Rationale (debate evidence)                                                                                                                                                |
|------------|-------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| C-002      | `PromptSource` Protocol + concrete `StringPrompt`, `FilePrompt`   | B-advocate conceded `FilePrompt` is speculative; without it the abstraction reduces to one concrete class behind a Protocol — a needless indirection. Defer to beat 2 if/when stream-json or @file delivery actually ships |
| C-002      | `PromptDelivery` strategy classes                                 | Same as above. Beat 1 has exactly one branching point (`if _use_stdin_for_prompt()`); promoting it to a strategy pattern is YAGNI                                          |
| C-005      | `delivery: PromptDelivery \| None = None` constructor kwarg       | Adds public API surface that no caller uses today                                                                                                                          |
| X-002      | "Leave PortifyProcess untouched" (B beat 1)                       | A's anchor change makes Portify stdin-safe today rather than relying on the operational invariant that Portify prompts are always small                                     |
| X-004      | `self.prompt = ""` for huge prompts                               | Backward-compat break; existing tests / callers may introspect `self.prompt`                                                                                                |
| —          | Removal of `_EMBED_SIZE_LIMIT` warning at roadmap call sites      | Keep as advisory in beat 1; revisit after stdin path proves stable in production (B-advocate conceded this)                                                                |

## Risk Summary

| Change # | Risk                                                              | Impact | Rollback                                                                                          |
|----------|-------------------------------------------------------------------|--------|---------------------------------------------------------------------------------------------------|
| #1       | New exception class is unused initially                           | None   | Delete the class                                                                                  |
| #2       | Sidecar disk usage if operator forgets to disable                 | Low    | `prompt_sidecar=False` default; opt-in only                                                        |
| #3       | Streaming chunk encode subtle bug                                 | Medium | Unit test asserts byte-identical round trip; revert to full-buffer encode by reverting one method  |
| #4       | None — test addition only                                         | None   | Delete the test                                                                                    |
| #5       | None — comment + test addition                                    | None   | Delete the comment and test                                                                        |
| #6, #7   | None — documentation polish                                       | None   | Revert prose                                                                                       |

## Review Status

- Approval: **auto-approved** (non-interactive mode)
- Approver: sc:adversarial protocol (debate-orchestrator)
- Timestamp: 2026-04-30T00:00:00Z
- Conditions: Merge proceeds. INV-005 (live claude stdin probe) is a P0 release-gate test recorded in `merge-log.md` and reproduced in the final merged design.
