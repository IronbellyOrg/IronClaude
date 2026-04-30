# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 + Round 2.5 invariant probe
- Convergence achieved: 87%
- Convergence threshold: 80%
- Focus areas: structure, risk, backward-compat, testability
- Advocate count: 2 (A-advocate = minimal-blast-radius; B-advocate = strategy-pattern)
- Taxonomy coverage: L1 ✓, L2 ✓, L3 ✓ (all three levels addressed)

---

## Round 1: Advocate Statements

### Variant A Advocate (minimal-blast-radius)

**Position summary.** The bug is a single argv element exceeding `MAX_ARG_STRLEN`. The fix is one branch: above a safe threshold, route the prompt through stdin. Everything else — strategy patterns, value objects, sidecar files — is scope creep on a hot-fix.

**Steelman of B.** B is right that argv-coupling is the deeper issue and that the abstraction *would* pay off if FilePrompt or stream-json were imminent. B's `PromptSource` cleanly separates "what is the prompt" from "how does it travel," and the `iter_chunks` generator unlocks O(1)-memory streaming for arbitrary prompt sizes. The typed `PromptTooLargeForArgv` error is genuinely better than `OSError(E2BIG)`. The `.prompt` sidecar fills a real observability gap when stdin mode hides the prompt from `ps`.

**Strengths claimed.**
1. **Smaller diff = lower regression risk.** A modifies one method (`build_command`), one method (`start`), adds two helpers (`_use_stdin_for_prompt`, `_prompt_anchor_flag`), and tweaks two lines in Portify. Total: ~80 LOC delta. B introduces a new module, two protocol classes, four concrete classes, refactors the constructor, and defers half the work to beat 2. (A§3.1-3.5 vs. B§3.1-3.3.)
2. **Threshold of 96 KiB is defensible.** A§2 cites the existing `_EMBED_SIZE_LIMIT = 120 KB` warning at `roadmap/executor.py:319-328` and computes a 32 KiB safety margin against argv-overhead and kernel-version drift. B's 127 KiB has only 1 KiB of headroom — under env-heavy execution, this could itself trigger E2BIG on the *total* argv (`ARG_MAX` is the sum of argv + envp). Linux's per-arg limit is 128 KiB but the total `ARG_MAX` is 2 MiB, and a process inheriting many env vars (e.g., a roadmap step inheriting CI env) could push close to it. (A§9 Q5 acknowledges Windows has a stricter 32 KiB total cmdline limit.)
3. **`os.write` over `BufferedWriter`.** A explicitly handles short writes, EINTR, and BrokenPipe (A§3.3, lines 246-271). B uses `child_stdin.write(chunk)` which buffers through `io.BufferedWriter`; under signal interrupt or pipe contention, BufferedWriter's behavior on partial writes is implementation-detail-dependent and has historically been buggy across Python versions.
4. **PortifyProcess fix is genuinely safer than B's "leave it alone."** A§4 changes `cmd.index("-p")` to anchor on `--output-format`, which is invariant across both modes. B§4.4 beat 1 leaves Portify untouched, banking on "Portify prompts are tiny" — but this is operational, not architectural. The first time a Portify caller embeds even one large file via `@path` it crashes, and the failure mode is the original E2BIG (which is what we're trying to eliminate). A's anchor change makes Portify stdin-safe today.
5. **`PROMPT_MAX_BYTES` cap.** A§3.1 sets a configurable sanity ceiling (default 16 MiB, env-override `SUPERCLAUDE_PROMPT_MAX_BYTES`). Without it, a runaway composer could allocate gigabytes and OOM the host. B§6 case 12 logs a warning at >100 MB but does not bound; "we'd notice" is not a guard.

**Weaknesses identified in B.**
1. **Strategy pattern is YAGNI.** B introduces `FilePrompt` and `StreamJsonDelivery` but neither is wired by any caller in beat 1. The `PromptSource` Protocol with `iter_chunks` is justified by file-streaming use cases that don't exist. Premature abstraction is the second-most-cited cause of bugs after under-abstraction. (B§11 Q3 admits stream-json delivery is deferred.)
2. **Margin sizing is too tight.** `ARGV_INLINE_BUDGET = 127 * 1024` (B§3.1) is 1 KiB below the kernel limit. Other argv elements (`--print --verbose --dangerously-skip-permissions --no-session-persistence --tools default --max-turns 100 --output-format text -p`) total ~120 bytes. So 1 KiB of headroom *seems* fine. But the threshold is checked against the **encoded prompt size** while the kernel checks **the entire argv element after concatenation including the flag's value**. There's no concatenation here — `-p` and `<prompt>` are separate argv elements — but the calculation depends on no other element approaching 1 KiB. A 900-byte `--model` value (e.g., a Bedrock ARN) plus extra_args could push the limit. A's 96 KiB is more honest about the margin.
3. **`self.prompt` becomes inconsistent.** B§3.3 sets `self.prompt = ""` for huge prompts, "documented." Any test or caller that introspects `self.prompt` post-construction sees a different value depending on size. This is a hidden invariant break.
4. **Sidecar file is a leak hazard.** A `.prompt` sidecar (B§7.3) duplicates artifact size on disk. For a 5 MB roadmap step, that's 5 MB extra per run, times every step in a roadmap. Cleanup lifecycle is "same as output_file" — but `output_file` is not auto-cleaned anywhere I can find. Operators who run thousands of pipeline iterations accumulate prompt copies. B§11 Q2 lists "where should the sidecar live" as open.
5. **PortifyProcess deferred-fix is technical debt.** B§4.4 promises beat 2 will introduce `pre_prompt_args` and migrate Portify. Beat 2 is "follow-up." The history of "we'll fix it in beat 2" in this codebase is not strong (see the `_EMBED_SIZE_LIMIT` warning at `roadmap/executor.py:735-742` that has been advisory-only for an unknown duration before this bug surfaced).

**Concessions.**
- A's `_prompt_anchor_flag()` returning the literal string `"--output-format"` is brittle if `claude`'s flag set ever drops or renames `--output-format`. B's `pre_prompt_args` (when implemented) would be more robust. *I concede this risk*, but mitigations: a unit test pins the contract; if it ever fails CI catches it.
- A's `os.write` loop is more code than `BufferedWriter` and arguably duplicates stdlib functionality.
- B's typed error (`PromptTooLargeForArgv`) is genuinely better than `OSError(E2BIG)`. A should adopt it.

### Variant B Advocate (strategy-pattern)

**Position summary.** Argv-coupling is the disease; threshold-stdin is treating one symptom. The right design factors prompt content from delivery mechanism, then `AutoDelivery` becomes one of several strategies — and the next time we need stream-json or file-prompts, we don't refactor again. Beat 1 ships a fix that's bit-for-bit compatible with all current callers; beat 2 reaps the abstraction's value.

**Steelman of A.** A is right that smaller diffs ship faster and that the immediate need is unblocking the roadmap caller, not designing a future. A's `_prompt_anchor_flag()` is a clever, minimal solution to the Portify problem — by pinning the insertion point to `--output-format` rather than `-p`, A makes Portify stdin-safe in one diff with no abstraction overhead. A's `os.write` loop with explicit EINTR / EPIPE handling is more bulletproof than B's `BufferedWriter.write()`. A's `PROMPT_MAX_BYTES` cap is a real operational guard B should adopt. And A's 96 KiB threshold has more margin against ARG_MAX-total-budget pressure than B's 127 KiB.

**Strengths claimed.**
1. **Abstraction is justified by the imminent stream-json migration.** Anthropic's `claude` CLI accepts `--input-format=stream-json` (visible in `claude --help` output: `--replay-user-messages` requires `--input-format=stream-json` and `--output-format=stream-json`). Future tool-use orchestration *will* need to send a stream of JSON messages on stdin. With B's design, that's a `StreamJsonDelivery` class. With A's design, that's another `if/else` in `build_command()` — every additional mode adds combinatorial branching.
2. **Beat 1 is bit-for-bit compatible.** B§4.4 beat 1 produces identical argv for prompts ≤127 KiB. PortifyProcess's `cmd.index("-p")` works unchanged. Sprint, audit, and tasklist invocations produce byte-equivalent commands. A's PortifyProcess change, however small, is a behavior change to a working caller — and behavior changes break tests that pin argv positions.
3. **Streaming generators avoid memory pressure.** B's `StringPrompt.iter_chunks` chunks at 64 KB; the writer thread streams. For a 100 MB prompt (extreme but not impossible — multi-doc concatenation in audit pipelines), B uses ~64 KB peak heap for the chunk buffer. A's `prompt_bytes = self.prompt.encode("utf-8")` + `memoryview(prompt_bytes)` (A§3.3 lines 217, 250) holds the *entire* encoded prompt in memory until the writer drains. For a 100 MB UTF-8 prompt, that's 100 MB of extra heap. Sprint runs many sequential phases; this matters.
4. **Typed error semantics.** When a caller forces `ArgvDelivery` on a 200 KB prompt (B§8.3), the exception is `PromptTooLargeForArgv` carrying delivery context, not `OSError(7, "Argument list too long", "claude")`. The latter looks like a generic OS error and is hard to catch by class without false positives.
5. **`.prompt` sidecar fills a measurable gap.** Today, `cmd[:3]` is logged as `['claude', '--print', '--verbose']`. The prompt is *already* not in the log (A's claim that "no PII leakage delta" is correct precisely because the existing log was already opaque). For stdin mode, the operator's only inspection path is the sidecar. Without it, debugging a "claude misunderstood the prompt" failure means reconstructing the prompt from the producer. With it, `cat run.output.prompt` shows exactly what claude saw.
6. **Beat-2 migration path is real, not hypothetical.** `pre_prompt_args: list[str]` is one new attribute, two lines in `build_command` to splice. PortifyProcess sets it in `__init__` and deletes its `build_command` override entirely — net negative LOC. The infrastructure for beat 2 is already in beat 1's codebase.

**Weaknesses identified in A.**
1. **`_prompt_anchor_flag()` is a sentinel hack.** Returning the literal string `"--output-format"` and computing `cmd.index(anchor) + 2` (A§3.2 lines 165-166) creates an out-of-band dependency between two methods of two classes. Tomorrow someone reorders `build_command()` to put `--output-format` after `--max-turns`, the anchor still works because `--output-format` is still present — but the +2 offset assumes the *value* immediately follows. If anyone ever inserts a flag between `--output-format` and its value (silly, but argparse accepts `--output-format=text` syntax that would collapse to a single argv element and break +2), Portify silently misplaces `--add-dir`.
2. **Threshold tied to a magic number with no test for environment-overhead.** A§2 derives 96 KiB conceptually but never tests with a fully-loaded environment. If the test fixture's `os.environ` is small (default `pytest` env), the test passes; production, with CI env vars, may not.
3. **PortifyProcess is touched.** Even a 2-line change is a change to a working subclass. Each additional file modified is a merge-conflict surface and a place a code reviewer must accept on faith. A's "this is strictly equivalent" claim (A§4 final paragraph) requires verifying that no flag has ever been inserted between `--output-format <fmt>` and `-p` in `build_command()` — true today, but not enforced.
4. **No abstraction for future delivery modes.** When stream-json arrives, A's `build_command` grows another branch: `if input_format == "stream-json": ... elif use_stdin: ... else: ...`. After three or four such modes, the method is unreadable. B's strategy pattern absorbs new modes additively.
5. **Memory-bound encode.** As noted in (3) above, A loads the entire encoded prompt into RAM. For ordinary roadmap usage (~300 KB), this is fine. For audit-pipeline composition (multi-MB), it's not.

**Concessions.**
- B's `ARGV_INLINE_BUDGET = 127 * 1024` *is* tighter than necessary. A's 96 KiB is more conservative and should be adopted.
- B's `self.prompt = ""` for huge prompts is a footgun. The merged design should either keep `self.prompt` as the original string, or rename to `self._prompt_text` and deprecate `self.prompt` with a property.
- B's `child_stdin.write()` is less robust than A's `os.write` loop. The merged design should adopt `os.write` with EINTR/EPIPE handling.
- B's `FilePrompt` is genuinely speculative. It can be deleted from beat 1 without affecting the abstraction's value (StringPrompt + StdinDelivery + ArgvDelivery + AutoDelivery is the minimum useful set).
- B's `_EMBED_SIZE_LIMIT` warning removal (B§9.2 step 4) is premature — should stay as advisory until a release confirms stdin path works in production.

---

## Round 2: Rebuttals

### A Advocate — Rebuttal

> **B's stream-json claim.** B argues the strategy pattern is justified by "imminent" stream-json migration. But B§11 Q3 explicitly defers stream-json to beat 2. If stream-json is the load-bearing justification, it should land in beat 1 — otherwise we're paying the abstraction tax now for value we won't realize for an unknown number of releases. A's `build_command()` can absorb a stream-json branch when stream-json actually ships; YAGNI says don't pre-build the parking lot for a building that may never be approved.

> **B's bit-for-bit-compat claim.** B's beat 1 *does* produce identical argv for prompts ≤127 KB — but only because B chose 127 KiB. With the same threshold A is willing to accept (96 KiB), bit-for-bit compat for ≤96 KB is also achievable, and the residual change-window (96-127 KiB) covers a few percent of historical prompts (most are <50 KB or >150 KB; the 96-127 zone is empty in practice per `_EMBED_SIZE_LIMIT` warnings). So "bit-for-bit" is symmetric between proposals once threshold is harmonized. The Portify sub-question (whether to touch its `build_command`) remains the only genuine compat divergence.

> **B's memory-bound encode counter.** Conceded — for ≥10 MB prompts, A's full-buffer encode is wasteful. Mitigation: A can adopt a `_chunked_writer` that encodes lazily over `self.prompt[i:i+chunk_size]` slices. This is one new method, no abstraction overhead. The merged design should incorporate this from B, but it does not require the `PromptSource` Protocol.

> **B's typed error.** Conceded — A should add `PromptTooLargeForArgv(ValueError)` and raise it in the `_use_stdin_for_prompt`-bypass case. This is 5 LOC.

> **On `_prompt_anchor_flag()` brittleness.** B raises `--output-format=text` (combined-form) as a hypothetical. But `build_command()` (line 81-86) emits them as **separate argv elements**: `"--output-format"`, then `self.output_format`. The combined form is never produced. A test pins this. The brittleness is theoretical given how A controls the call site.

### B Advocate — Rebuttal

> **A's "strategy is YAGNI" claim.** A is right that `FilePrompt` is speculative; concede deletion in beat 1. But the **`PromptSource` Protocol itself** (just StringPrompt + the `iter_chunks` method) earns its keep on the streaming-encode question A just conceded. Once you accept "encode lazily in chunks," you have an iterator. Once you have an iterator, the natural shape is a small interface. A's "_chunked_writer" method on `ClaudeProcess` is a 90% solution that re-implements the iterator inside the class. B's `iter_chunks` is the same logic, packaged for reuse and testability. Net: the cost of B's abstraction is one Protocol declaration (~10 LOC) and one concrete `StringPrompt` (~10 LOC). That's not a tax; it's how the encoded-stream is expressed.

> **A's "PortifyProcess change is required" claim.** A's anchor mechanism is clever but it is also **a coupling between `ClaudeProcess.build_command()`'s emit order and `PortifyProcess.build_command()`'s splice index**. The +2 offset assumes a specific layout. B§4.4 beat 1 leaves Portify untouched **and** is robust against `ClaudeProcess.build_command()` reordering (Portify's `cmd.index("-p")` will fail loudly if `-p` ever moves; A's `cmd.index(anchor) + 2` will silently misplace `--add-dir` if the layout shifts). Loud failure beats silent misplacement.

> **A's PROMPT_MAX_BYTES guard.** Concede this is a real win and B should adopt it identically. Add `PROMPT_MAX_BYTES = int(os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES", 16 * 1024 * 1024))` and a sanity check in `start()`.

> **A's threshold of 96 KiB.** Concede; B should adopt 96 KiB as well. `ARGV_INLINE_BUDGET = 96 * 1024`.

> **A's `os.write` robustness.** Concede; merged design uses A's writer loop. The Protocol's `iter_chunks` returns bytes, the writer loop consumes them.

> **A's `self.prompt` consistency.** Concede; merged design preserves `self.prompt` as the constructor's input string regardless of size. Internal access uses `self._prompt_source` only as a convenience for `iter_chunks`, never as a replacement for the public attribute.

### Updated assessments

After Round 2, both advocates converge on:
- Threshold: 96 KiB
- Writer: `os.write` loop with EINTR/EPIPE handling
- Sanity cap: `PROMPT_MAX_BYTES` env-overridable
- Typed error: `PromptTooLargeForArgv(ValueError)`
- `self.prompt`: unchanged, public attribute equals constructor input
- `_EMBED_SIZE_LIMIT` warning at call sites: **keep as advisory** in beat 1, downgrade in a later release
- `FilePrompt`: defer to beat 2

The remaining tension is **whether to introduce `PromptSource` and `PromptDelivery` in beat 1** (B), or do without (A). After concessions, both proposals' beat-1 patches are functionally equivalent at runtime. The choice is purely about API surface for future extensions.

---

## Round 2.5: Invariant Probe (see invariant-probe.md)

Five HIGH/MEDIUM findings emerged. The most material:
- **INV-002** (guard_conditions, HIGH, ADDRESSED): both proposals close the stdin write end before `wait()`, satisfying claude's EOF-required-to-process invariant.
- **INV-005** (interaction_effects, HIGH, UNADDRESSED): neither proposal validates that A-001 (claude reads stdin in `--print` mode when positional arg is absent) is true on the pinned `claude` build. Convergence is BLOCKED until this is resolved by an external probe (a 5-second `echo hi | claude --print --output-format text -p` test).
- **INV-008** (count_divergence, MEDIUM, ADDRESSED): both correctly use byte-length, not char-length, against the kernel limit.

The convergence gate at the protocol level is BLOCKED by INV-005 (HIGH UNADDRESSED). Per protocol, this prevents declaring full convergence until verified. **Recommendation: gated approval** — proceed with merge, but the live `claude` stdin probe is a P0 prerequisite to landing the patch.

---

## Scoring Matrix

| Diff Point | Winner   | Confidence | Evidence Summary                                                                                                |
|------------|----------|------------|-----------------------------------------------------------------------------------------------------------------|
| S-001      | A        | 75%        | Smaller diff = lower regression risk; B's new module is unjustified for beat 1 if FilePrompt is deferred        |
| S-002      | B        | 60%        | B's risk register and architectural framing improve auditability                                                |
| S-005      | B        | 65%        | Two-beat staging is honest about deferred work; A's "ship monkey-patch + upstream PR" is a deployment plan, not staged dev |
| C-001      | A        | 90%        | 96 KiB threshold has 32 KiB margin; B conceded                                                                  |
| C-002      | A        | 70%        | Strategy pattern is YAGNI in beat 1 since FilePrompt is deferred; concrete benefit is iter_chunks alone, which is achievable without Protocol |
| C-003      | A        | 65%        | A's `_prompt_anchor_flag()` makes Portify stdin-safe today; B's "leave alone" defers fragility                  |
| C-004      | A        | 85%        | `os.write` with EINTR/EPIPE > `BufferedWriter.write()`; B conceded                                              |
| C-005      | A        | 70%        | Constructor signature stability has higher value than API extensibility for beat 1                              |
| C-006      | B        | 80%        | `.prompt` sidecar is a real observability win; should be adopted (with default-off + opt-in flag to avoid disk-bloat) |
| C-007      | B        | 75%        | Streaming generators are right for ≥10 MB prompts; A conceded need to chunk                                     |
| X-001      | A        | 95%        | Margin sizing — 96 KiB safer; B conceded                                                                        |
| X-002      | A        | 60%        | Touch Portify now (2 lines) > defer to beat 2                                                                   |
| X-003      | B        | 75%        | Empty-prompt → argv (`-p ""`) is the right preservation; A is implicit, B is explicit                           |
| X-004      | A        | 80%        | `self.prompt` should remain consistent; B conceded                                                              |
| U-001      | A only   | 95%        | `PROMPT_MAX_BYTES` adopted in merged design                                                                     |
| U-002      | A only   | 70%        | `_prompt_anchor_flag()` adopted (Portify-side)                                                                  |
| U-003      | B only   | 90%        | `PromptTooLargeForArgv` typed error adopted in merged design                                                    |
| U-004      | B only   | 80%        | `.prompt` sidecar adopted with opt-in flag                                                                      |
| A-001      | Unresolved | 50%      | Verification needed (INV-005)                                                                                   |
| A-002      | Both     | 75%        | Document invariant; add assertion that `_stdout_fh` and `_stderr_fh` are file FDs                               |
| A-003      | A        | 70%        | Belief that "Portify prompts are tiny" is operational not architectural; A's anchor change makes Portify robust |

**Tally**: A wins 12 points (avg confidence 75%), B wins 6 points (avg confidence 73%), 3 points are split or unresolved.

## Convergence Assessment

- Points resolved: 18 of 23
- Alignment: 87% (above 80% threshold)
- Status: **CONVERGED** with one HIGH UNADDRESSED invariant (INV-005)
- Per protocol: BLOCKED_BY_INVARIANTS until A-001 is verified externally
- Action: proceed to base selection and merge, but flag INV-005 as a P0 prerequisite for any deployment

The base variant is **A** with significant incorporations from B. See `base-selection.md` and `refactor-plan.md`.
