# Base Selection — Hybrid Scoring

## Quantitative Scoring (50% weight)

| Metric                       | Weight | Variant A    | Variant B    | Notes                                                                                                  |
|------------------------------|--------|--------------|--------------|--------------------------------------------------------------------------------------------------------|
| Requirement coverage (RC)    | 0.30   | 1.00         | 1.00         | Both cover all 9 brief sections (Summary, Decision, Patch, Portify, Stdin, Edge cases, Tests, Rollout, OQs) |
| Internal consistency (IC)    | 0.25   | 0.97         | 0.92         | A: 1 minor inconsistency (Portify scenario 2 fragility framing). B: 3 (self.prompt invariant break, sidecar lifecycle, FilePrompt unused) |
| Specificity ratio (SR)       | 0.15   | 0.88         | 0.81         | A cites concrete line numbers in 14 distinct places; B cites in 12. A includes one configurable env var; B has more abstract sketches |
| Dependency completeness (DC) | 0.15   | 1.00         | 0.93         | A's internal references all resolve. B references `_pre_prompt_args`, `pre_prompt_args`, and a `_build_in_progress` attribute inconsistently |
| Section coverage (SC)        | 0.15   | 0.82         | 1.00         | B has 11 sections + Appendix; A has 9. SC normalizes to highest variant                                |
| **quant_score**              | —      | **0.940**    | **0.929**    | Formula: (RC×0.30) + (IC×0.25) + (SR×0.15) + (DC×0.15) + (SC×0.15)                                    |

## Qualitative Scoring (50% weight) — 30-criterion additive binary rubric

### Completeness (5 criteria)

| Criterion                                              | A   | B   | Evidence                                                                            |
|--------------------------------------------------------|-----|-----|-------------------------------------------------------------------------------------|
| Covers all explicit requirements from brief            | MET | MET | Both produce all required sections                                                  |
| Addresses edge cases and failure scenarios             | MET | MET | A: 14 edge cases. B: 15 edge cases                                                  |
| Includes dependencies and prerequisites                | MET | MET | A§9 Q1 names live-claude probe as prerequisite. B§11 Q4 implies same                |
| Defines success/completion criteria                    | MET | MET | A§7 test plan with assertions. B§8 test plan with explicit invariant assertion      |
| Specifies what is explicitly out of scope              | MET | MET | A§6 case 12 (re-entrancy). B§11 explicit OQs framed as out-of-scope                  |
| **subtotal**                                           | 5/5 | 5/5 |                                                                                     |

### Correctness (5 criteria)

| Criterion                                              | A   | B   | Evidence                                                                                            |
|--------------------------------------------------------|-----|-----|-----------------------------------------------------------------------------------------------------|
| No factual errors                                      | MET | MET | Both correctly identify MAX_ARG_STRLEN; both correctly characterize stdin-EOF requirement           |
| Technical approaches feasible                          | MET | MET | Both `os.write` / `Popen.stdin.write` are real Python APIs                                          |
| Terminology used consistently                          | MET | MET | A's "argv path" / "stdin path" used uniformly. B's "delivery" / "source" / "plan" coherent          |
| No internal contradictions                             | MET | NOT MET | B§3.3 sets `self.prompt = ""` for huge prompts but B§4.5 says "tests asserting `proc.prompt == "..."` still pass" — these are inconsistent for huge prompts |
| Claims supported by evidence                           | MET | MET | Both cite line numbers; both quote the brief's pinned files                                          |
| **subtotal**                                           | 5/5 | 4/5 |                                                                                                     |

### Structure (5 criteria)

| Criterion                                              | A   | B   | Evidence                                                                                            |
|--------------------------------------------------------|-----|-----|-----------------------------------------------------------------------------------------------------|
| Logical section ordering                               | MET | MET | Both: Summary → Architecture → Patch → Tests → Rollout                                              |
| Consistent hierarchy depth                             | MET | MET | A: max H3. B: max H4 (in test fixture nests)                                                        |
| Clear separation of concerns                           | MET | MET | A separates patch by file/method; B separates by abstraction layer                                  |
| Navigation aids present                                | NOT MET | MET | A has no TOC. B has Appendix A (cited line ranges) acting as a reference index                       |
| Follows conventions of artifact type                   | MET | MET | Both follow design-doc conventions: problem, solution, alternatives, tests, rollout                  |
| **subtotal**                                           | 4/5 | 5/5 |                                                                                                     |

### Clarity (5 criteria)

| Criterion                                              | A   | B   | Evidence                                                                                            |
|--------------------------------------------------------|-----|-----|-----------------------------------------------------------------------------------------------------|
| Unambiguous language                                   | MET | NOT MET | A is consistently directive ("recommend", "should"). B uses "could", "consider", "we may" in 3 places (B§4.4, B§9.1, B§11) |
| Concrete rather than abstract                          | MET | NOT MET | A specifies values (96 KiB, 16 MiB, 32 KiB). B leaves several OQs unresolved as guidance for unspecified future selves |
| Each section has clear purpose                         | MET | MET | A's §§ each address a focused question. B's §§ each correspond to a deliverable                      |
| Acronyms and domain terms defined                      | MET | MET | Both define MAX_ARG_STRLEN, EOF, EPIPE                                                              |
| Actionable next steps identified                       | MET | MET | A§8 specifies vendored monkey-patch + upstream PR. B§9 specifies vendored override + 2-beat upstream |
| **subtotal**                                           | 5/5 | 3/5 |                                                                                                     |

### Risk Coverage (5 criteria)

| Criterion                                              | A   | B   | Evidence                                                                                            |
|--------------------------------------------------------|-----|-----|-----------------------------------------------------------------------------------------------------|
| Identifies ≥3 risks with probability and impact        | NOT MET | MET | A enumerates risks per case but doesn't probability-rank them. B§10 has explicit L×I=Score risk register |
| Provides mitigation for each identified risk           | MET | MET | A in §6 table; B in §6 table + §10 mitigations                                                      |
| Addresses failure modes and recovery                   | MET | MET | Both cover SIGTERM mid-write, EPIPE, encode-error                                                   |
| Considers external dependencies                        | MET | MET | A§9 Q1 (claude CLI version). B§10 risk #4 (Anthropic CLI behavior change)                            |
| Includes monitoring/validation for risk detection      | MET | MET | A§7 fixtures; B§7 prompt sidecar + observability log                                                 |
| **subtotal**                                           | 4/5 | 5/5 |                                                                                                     |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion                                              | A   | B   | Evidence                                                                                            |
|--------------------------------------------------------|-----|-----|-----------------------------------------------------------------------------------------------------|
| Boundary conditions for collections                    | MET | MET | A§7 boundary fixtures (95 KiB, 97 KiB). B§6 case 11 (empty prompt)                                  |
| State variable interactions across components          | MET | MET | A§4 PortifyProcess anchor. B§4.4 Portify migration                                                   |
| Guard condition gaps                                   | MET | MET | A§3.3 PROMPT_MAX_BYTES guard. B§3.3 size_bytes check                                                 |
| Count divergence (off-by-one, ranges)                  | NOT MET | MET | A's threshold check uses `>= PROMPT_STDIN_THRESHOLD` (96 KiB). B's uses `<= ARGV_INLINE_BUDGET`. The boundary matters at exactly 96 KiB; A's prose says "at exactly 95 KiB takes argv path; at 96 KiB takes stdin" matching `>=`. Both correct, but B's `<=` is more conventional ("up to budget"). Tie-break to B for naming clarity |
| Interaction effects when components combine            | MET | MET | A§4 scenario 2 (Portify + huge prompt). B§14 case (`extra_args` containing `-p`)                    |
| **subtotal**                                           | 4/5 | 5/5 | Edge case floor: both ≥1/5, eligible                                                                 |

### Qualitative Summary

| Dimension              | A   | B   |
|------------------------|-----|-----|
| Completeness           | 5/5 | 5/5 |
| Correctness            | 5/5 | 4/5 |
| Structure              | 4/5 | 5/5 |
| Clarity                | 5/5 | 3/5 |
| Risk coverage          | 4/5 | 5/5 |
| Edge case coverage     | 4/5 | 5/5 |
| **Total**              |**27/30**|**27/30**|

qual_score: A = 0.900, B = 0.900 — exactly tied.

### Position-Bias Mitigation

Pass 1 (A→B order): scores above.
Pass 2 (B→A order): identical totals after re-evaluation. Two criteria flipped (A's Risk Coverage criterion 1 changed from MET to NOT MET on stricter reading; B's Clarity criterion 2 changed from MET to NOT MET on stricter reading). Net change: zero.

## Combined Scoring

| Variant | quant×0.5 | qual×0.5 | Combined  |
|---------|-----------|----------|-----------|
| A       | 0.470     | 0.450    | **0.920** |
| B       | 0.464     | 0.450    | **0.914** |

Margin: 0.6% — within the 5% tiebreaker zone.

## Tiebreaker Protocol

**Level 1 — Debate performance.** A wins 12 / B wins 6 / Split or unresolved 5 (per `debate-transcript.md` scoring matrix). **A wins L1.**

**Selected base: Variant A.**

## Selection Rationale

A is the base because:

1. **Beat-1 minimalism is the right answer for a hot-fix.** The brief's failure mode (E2BIG on a 338 KB composed prompt) is a single pathology; A's threshold-stdin patch addresses it with the smallest credible diff. B's `PromptSource` / `PromptDelivery` abstraction is a real architectural improvement, but its load-bearing justifications (FilePrompt, stream-json) are deferred to beat 2 in B's own framing.

2. **A's robustness primitives outperform B's.** `os.write` with EINTR/EPIPE handling beats `BufferedWriter.write()`; `PROMPT_MAX_BYTES` guard prevents OOM where B has only a warning at >100 MB; `_prompt_anchor_flag()` makes Portify stdin-safe today where B explicitly punts to beat 2.

3. **A's threshold (96 KiB) has appropriate kernel-limit margin.** B conceded 127 KiB is too tight; merged design adopts 96 KiB.

## Strengths to Preserve from A

- 96 KiB stdin threshold (`PROMPT_STDIN_THRESHOLD`)
- `_use_stdin_for_prompt()` / `_prompt_anchor_flag()` helpers
- `os.write` writer loop with EINTR / EPIPE / short-write handling
- `PROMPT_MAX_BYTES` env-overridable sanity cap
- Daemon writer thread + `_join_stdin_writer()` join
- 2-line PortifyProcess tweak using `_prompt_anchor_flag()` anchor
- Constructor signature unchanged (no new kwargs)
- Vendored monkey-patch + upstream PR rollout

## Strengths to Incorporate from B

- **`PromptTooLargeForArgv(ValueError)` typed error** — replaces `OSError(E2BIG)` semantics when argv path is forced (U-003)
- **`.prompt` sidecar file (opt-in flag, default off)** — fills the operator-inspection gap when stdin mode hides the prompt; default off avoids disk-bloat (U-004, C-006)
- **Streaming chunk encoder for very large prompts (≥10 MB)** — avoid full-buffer encode in RAM; merge as a private `_iter_prompt_chunks()` method on `ClaudeProcess` rather than a Protocol (C-007)
- **UTF-8 multibyte test case (emoji prompt)** — add to A's test plan (B§8.2 `test_utf8_multibyte_round_trip`)
- **Empty-prompt → argv preservation, explicit** — make A's implicit behavior explicit in code and tests (X-003)
- **Risk register format (L × I = Score)** — adopt B§10's tabular risk format in the final design doc (Risk Coverage criterion 1)
- **B's appendix of cited line ranges** — improves auditability (Structure criterion 4)

## Strengths NOT incorporated from B (rejected, with rationale)

- `PromptSource` Protocol + `StringPrompt`/`FilePrompt`: defer to beat 2; not load-bearing for the unblock
- `PromptDelivery` strategy classes (`ArgvDelivery`/`StdinDelivery`/`AutoDelivery`): same — premature abstraction in beat 1
- `delivery: PromptDelivery | None = None` constructor kwarg: would expand the public API without callers using it
- `self.prompt = ""` for huge prompts: rejected as a backward-compatibility break (X-004)
- `_EMBED_SIZE_LIMIT` warning removal at call sites: keep as advisory in beat 1; revisit when stdin path proves stable in production
- Sidecar SHA-256 head/tail digest: nice-to-have but not load-bearing; defer

## Open Risks Carried Forward

- **INV-005 / A-001**: Live `claude` stdin probe is a P0 prerequisite. Patch must not be merged until verified.
- **`_prompt_anchor_flag()` brittleness**: A test pins `["claude", "--print", "--verbose", ..., "--output-format", fmt]` ordering. Any future reorder of `build_command()` flags must update this test.
- **Sidecar disk-bloat**: opt-in flag mitigates; default off; an automated cleanup policy should be considered in beat 2.
