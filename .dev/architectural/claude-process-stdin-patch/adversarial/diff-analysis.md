# Diff Analysis: ClaudeProcess stdin-patch design comparison

## Metadata
- Generated: 2026-04-30
- Variants compared: 2 (Proposal A — minimal-blast-radius; Proposal B — strategy-pattern redesign)
- Total differences found: 23 (S: 5, C: 7, X: 4, U: 4, A: 3)
- Focus areas: structure, risk, backward-compat, testability

## Structural Differences

| #     | Area                          | Variant A                                                            | Variant B                                                                          | Severity |
|-------|-------------------------------|----------------------------------------------------------------------|------------------------------------------------------------------------------------|----------|
| S-001 | Module scope                  | Single-file edit to `pipeline/process.py` + tiny tweak in Portify    | New module `pipeline/prompt_source.py` + refactored `process.py` constructor       | High     |
| S-002 | Section count                 | 9 sections (Summary → Open Questions)                                | 11 sections + Appendix (adds Architectural Framing, Risk Register)                 | Medium   |
| S-003 | Code-fragment density         | Before/After diff blocks anchored to live line numbers               | Pseudocode + dataclass sketch + sequence diagram-as-text                           | Medium   |
| S-004 | Edge case enumeration         | 14 cases tabulated                                                   | 15 cases tabulated                                                                 | Low      |
| S-005 | Rollout staging               | Single-phase patch (immediate monkey-patch + upstream PR)            | Explicit two-beat migration (beat 1 = abstraction, beat 2 = pre_prompt_args)       | High     |

## Content Differences

| #     | Topic                              | Variant A Approach                                                                                        | Variant B Approach                                                                                                                | Severity |
|-------|------------------------------------|-----------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|----------|
| C-001 | Stdin-trigger threshold            | 96 KiB (32 KiB margin under MAX_ARG_STRLEN); hard-coded constant                                          | 127 KiB (1 KiB margin); class-level constant `ARGV_INLINE_BUDGET` on `AutoDelivery`                                               | High     |
| C-002 | Abstraction layer                  | None — direct `if/else` on encoded length inside `build_command()`                                        | `PromptSource` (Protocol + StringPrompt + FilePrompt) and `PromptDelivery` (Protocol + Argv/Stdin/Auto)                          | High     |
| C-003 | PortifyProcess strategy            | Modify Portify to anchor on `--output-format` (2-line tweak via new `_prompt_anchor_flag()`)              | Beat 1: no Portify change (relies on tiny prompts → argv → `cmd.index("-p")` still works); Beat 2: introduce `pre_prompt_args`   | High     |
| C-004 | Stdin write primitive              | `os.write(fd, view)` loop with explicit EINTR / BrokenPipe / short-write handling                         | `child_stdin.write(chunk)` over Python `BufferedWriter`; `try/finally close()`                                                    | Medium   |
| C-005 | Constructor signature              | Unchanged (`prompt: str` only); zero new kwargs                                                           | Adds `prompt: str \| PromptSource` and new `delivery: PromptDelivery \| None = None` kwarg                                        | High     |
| C-006 | Observability beyond existing log  | Adds `prompt_via=stdin\|argv` + `prompt_bytes=N` fields to existing debug log                             | Adds the same fields PLUS `.prompt` sidecar file (gated per-pipeline) PLUS SHA-256 head/tail digest                              | Medium   |
| C-007 | Streaming model                    | Single in-memory bytes buffer (`memoryview` over the encoded prompt)                                       | `iter_chunks(chunk_size=64 KB)` generator — never holds full bytes for `FilePrompt`                                              | Medium   |

## Contradictions

| #     | Point of Conflict             | Variant A Position                                                                | Variant B Position                                                                                                | Impact   |
|-------|-------------------------------|-----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|----------|
| X-001 | Margin vs the 128 KiB limit   | A§3.1: 96 KiB threshold leaves 32 KiB margin — "we never come close to ARG_MAX"   | B§3.1: `ARGV_INLINE_BUDGET = 127 * 1024` "leave 1 KB headroom for argv-other elements"                            | High     |
| X-002 | Whether Portify needs touched | A§4: tweak Portify (~2 lines) to anchor on `--output-format`                      | B§4.4 Beat 1: leave Portify alone — argv layout is "bit-for-bit" identical for ≤127 KB prompts                   | High     |
| X-003 | Empty-prompt handling         | Implicit: encode("") = 0 bytes < 96 KiB → argv path with `-p ""` (legacy)         | B§6 case 11 explicit: AutoDelivery picks argv (`-p ""`); never silently switches to stdin for empty strings       | Low      |
| X-004 | Backwards compat of `self.prompt` | Unchanged — always equals constructor arg                                      | "Empty string for huge prompts (documented), code that needs the bytes uses `self._prompt_source`"                | Medium   |

## Unique Contributions

| #     | Variant   | Contribution                                                                                                                  | Value Assessment |
|-------|-----------|-------------------------------------------------------------------------------------------------------------------------------|------------------|
| U-001 | A         | `PROMPT_MAX_BYTES` env-overridable sanity cap (default 16 MiB) raises before fork on pathological inputs                      | High             |
| U-002 | A         | `_prompt_anchor_flag()` helper as a stable insertion target for ALL subclasses, not just Portify                              | High             |
| U-003 | B         | Typed `PromptTooLargeForArgv` error when caller forces `ArgvDelivery` on oversized prompt — replaces `OSError(E2BIG)`         | Medium           |
| U-004 | B         | `.prompt` sidecar file for operator inspection in stdin mode (operator's "what did claude actually see?" answer)              | High             |

## Shared Assumptions

| A-NNN | Agreement Source                                                                       | Assumption                                                                                                       | Classification | Promoted |
|-------|----------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|----------------|----------|
| A-001 | Both: "claude --print reads stdin when positional prompt omitted"                      | The pinned `claude` CLI version reads from stdin in `--print` mode when `-p` value is absent                     | UNSTATED       | Yes      |
| A-002 | Both rely on stdout/stderr being non-PIPE → no two-pipe deadlock                       | The current `_stdout_fh`/`_stderr_fh` file-redirect contract is invariant; no caller switches them to PIPEs      | UNSTATED       | Yes      |
| A-003 | Both: PortifyProcess prompts are tiny (B explicit, A implicit)                         | All present and foreseeable Portify invocations produce prompts < 96 KiB                                          | STATED         | No       |

> A-001 is the single biggest live risk. Both proposals depend on it; neither has verified it on the pinned `claude` build. A-002 holds today but is not enforced anywhere — a future caller passing `stdout=PIPE` would break the deadlock argument.

## Summary

- Total structural differences: 5
- Total content differences: 7
- Total contradictions: 4 (X-001 high-impact: margin sizing; X-002 high-impact: Portify scope)
- Total unique contributions: 4 (2 per variant; A skews infrastructure, B skews observability)
- Total shared assumptions surfaced: 3 (UNSTATED: 2, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: S-001, S-005, C-001, C-002, C-003, C-005, X-001, X-002

The two proposals **agree on 80% of the mechanics** (daemon writer thread, file-redirected stdout/stderr removes deadlock, claude reads stdin under `--print`, PortifyProcess prompts are tiny in practice) and **diverge on scope**:
- A optimizes for minimum-diff and ships behavior change in one beat.
- B introduces a `PromptSource`/`PromptDelivery` abstraction and stages the migration.

The contested ground is whether the strategy-pattern abstraction earns its keep today, or is YAGNI given that B explicitly defers `FilePrompt` and `pre_prompt_args` to beat 2.
