# Round 2 — Spec-Advocate Rebuttals

**Role**: Spec-keeper / QA lead arguing for `variant-2-spec.md` (RECONCILED_DESIGN.md).
**Round**: 2 (rebuttal to impl-advocate's R1 strengths and weaknesses-of-spec).

---

## Response to Impl-Advocate's R1 Strengths

R1-impl claimed 15 strengths. Per-strength reply:

**Strength #1 — pre-spawn guard pipeline implemented identically (`pipeline/process.py:60-93`).**
**Acknowledge.** P-002 + P-003 mechanics match spec line-for-line at `pipeline/process.py:27-40, 137-145`. **But** F-strict-review surfaces a real residual: `int(os.environ.get(...))` at `:27-29` crashes on non-numeric env (F MEDIUM-2). The "identically" claim is true at the algorithm level and false at operator-hostility level. The spec did not require try/except, but R1-impl's claim of full parity over-states the result.

**Strength #2 — chunked stdin write faithful to spec at `_write_prompt_to_stdin` (`pipeline/process.py:192-229`).**
**Reframe.** The base-class implementation IS faithful. **But** `PrdClaudeProcess.terminate()` at `src/superclaude/cli/prd/process.py:239-279` is a near-clone of pre-P-004 base `terminate()` and omits the 4-line `_stdin_error` log surfacing block (F MEDIUM-1). The strength addresses base correctness; it does not address subclass propagation. PRD pipeline silently swallows BrokenPipe during stdin write under SIGTERM-only paths.

**Strength #3 — chunked-loop NOT a thread (architectural choice respected).**
**Acknowledge.** R1-impl correctly notes spec §4 P-004 L407 chose chunked-loop over daemon thread, and A respects it. **But** the trade-off the spec documented ("if future production telemetry shows stalls, the writer-thread upgrade is a localized follow-up") has no telemetry hook in A — the spawn debug log records `prompt_bytes=N` but no parent-stall duration, no chunk-write latency. The deferral was conditional on telemetry; the telemetry is absent.

**Strength #4 — Portify `--output-format` anchor + historical-context comment (`cli_portify/process.py:208-219`).**
**Acknowledge.** P-001 mechanically correct. **But** the Portify base contract is dependency-injected via `--output-format` always being present in the base `build_command()` (`pipeline/process.py:108-110`); the `# pragma: no cover` on the except branch (`cli_portify/process.py:218`) IS reachable if `extra_args` ever shadows `--output-format`. T-008 pins adjacency but not the "must be exactly one `--output-format` in cmd" invariant — a future change adding a second `--output-format` would land `--add-dir` at index+2 of the *first* one, which may be wrong. Strength is real; invariant net is incomplete.

**Strength #5 — argv invariant `< 4 KiB` is stricter than spec (T-001).**
**Acknowledge.** A is one byte stricter. Strict subset; cannot fail when spec passes.

**Strength #6 — eleven T-NNN tests delivered 1:1.**
**Reframe.** Counts match. **But** strength counts existence, not strength. T-005's timer fires *before* `start()` runs Popen (F NIT-2 / `test_process_stdin.py:230-234`); if the 0.5s timer fires while `_process is None`, `terminate()` is a noop and the test passes via the wrong code path. T-011's BrokenPipe assertion is conditional (X-006) — fast-machine race lets it pass without exercising `_stdin_error`. T-007's regression net does not exercise the `tool_write_mode + extra_args + add_dir` interaction. **The 11-of-11 count is a roof, not a ceiling.**

**Strength #7 — A adds value beyond spec (T-prompt_under_cap, T-tool_write_mode_false).**
**Acknowledge.** Real positive drift. R0/U-008/U-009 captured this. No reframe.

**Strength #8 — D-080 implicitly satisfied by base SHA `142ce15`.**
**Acknowledge.** Mechanical: `142ce15` is post-`4799719`, so building on it preserves the stdin migration. No counter.

**Strength #9 — D-088 LOC budget respected.**
**Acknowledge in part.** +60/-7 net is at the upper spec edge. Within bound.

**Strength #10 — D-080 / P-005 "no source patch" honored.**
**Acknowledge.** Commit `01cf2ef test(pipeline): pin tool_write_mode contract` is test-only. Spec compliance verified.

**Strength #11 — pipe-buffer 64 KiB is correctly approximated in both.**
**Acknowledge.** STATED-with-fudge by both per A-007. No counter.

**Strength #12 — A corrected B's `proc.poll()` typo (X-005).**
**Acknowledge.** Spec text was wrong; A used `_process.poll()` correctly.

**Strength #13 — `stdin.close()` in `finally` (`pipeline/process.py:225-229`).**
**Acknowledge mechanically.** **But** there is **no test that fails if a future refactor moves `close()` out of the `finally`** (F's "Mutation kill rate" §6 explicitly identifies this gap). Coverage exists; mutation-kill does not. The Strength is structurally correct; the regression net is incomplete.

**Strength #14 — `# pragma: no cover` annotations are correct hygiene.**
**Acknowledge.** Defensible drift; spec did not request, A added correctly.

**Strength #15 — 8 commits map cleanly to 7 spec steps.**
**Reframe.** Mapping is mostly right; the 8th commit (`db8cffe docs: STRICT-tier verification review`) imports F's review *into* the design package, which is itself an artefact the impl-advocate's own argument depends on. The R1-impl repeatedly cites F's review without acknowledging it surfaces TWO MEDIUMs (PrdClaudeProcess + env-var crash) that R1-impl never raised. Strength is correct on commit ordering; weak on what the 8th commit's contents reveal.

---

## Response to Impl-Advocate's Weaknesses-of-Spec

R1-impl listed 8 weaknesses in B. Defense or concession per item:

**Weakness-of-B #1 — `proc.poll()` is unrunnable as written.**
**Concede.** Spec text at §5 row 5 is wrong. A's correction (`_process.poll()`) is right.

**Weakness-of-B #2 — `_stdin_error is not None` was promised unconditionally; race makes it not always true.**
**Defend.** The spec promised the *contract*; the implementation chose the *mechanism* (raw 1 MB payload + child-exits-immediately stand-in) that has a race. Replace the mechanism, not the contract: a `monkeypatch.setattr(os, "write", _raise_BrokenPipe)` mock injects BrokenPipe deterministically, satisfying the unconditional assertion. The spec was correct; the test was lazy. Concede the spec didn't prescribe the mock approach explicitly, but defending the spec contract is straightforward.

**Weakness-of-B #3 — §9.1 cites tests outside diff scope (`tests/pipeline/test_process.py:54, :176-177`).**
**Defend.** The spec's job is to enumerate the regression surface; running tests is CI's job. Citing existing-test line numbers is exactly what a closure document should do. The reviewer's verification path is `make test` + grep the cited line numbers — neither requires the tests to live in the diff scope.

**Weakness-of-B #4 — §10 acceptance checklist mixes 4 categories (source state, CI green, cross-doc verdicts, on-Coder validation).**
**Concede in part.** Yes, the checklist mixes categories. **But** that is correct for a closure document: closing a release means hitting all four. Defending the spec: the items are owned by different roles (engineer for source state, CI for green, spec-keeper for verdict mapping, release-engineer for on-Coder validation) but all four must close. R1-impl's complaint reframes a feature as a bug.

**Weakness-of-B #5 — §9.2 production-rebuild straddles two repos; "category error" to ask if A implements §9.2.**
**Concede in part.** §9.2 is operational. **But** without §9.2 the bug is unfixed for the consumer — the `/config/workspace/Coder` user is the original bug-reporter and the only meaningful definition of "delta closed." Calling it out-of-scope is technically correct and pragmatically inadequate. Concrete remediation that works inside the IronClaude branch: add a `Makefile` target `make ship-coder` documenting the upgrade recipe so the operational task has a reproducible script.

**Weakness-of-B #6 — §3.2 DEFER-TO-BEAT-2 list provides no tracking surface.**
**Concede.** Real spec gap. The spec named items but didn't specify the tracking mechanism (issue tracker? in-tree TODO? file?). Concrete defense: spec-advocate proposed in W-H4 of R1 that a `BEAT_2_BACKLOG.md` file lands in this delta. The spec's omission becomes the implementation's fix-in-flight.

**Weakness-of-B #7 — §6 risks-resolved cite code already in `4799719`; nothing for A to "implement".**
**Defend.** Yes, those are *resolved-prior* attestations; their job is to record verification status, not action items. The spec correctly distinguishes "resolved-prior" (§6) from "resolved-by-this-delta" (§7 mitigation column). R1-impl mistook documentation for an unmet requirement.

**Weakness-of-B #8 — §11 demands D-NNN traceability in commits without specifying convention.**
**Concede in part.** The spec doesn't specify whether D-NNN should appear in commit subject, body, or a separate file. **But** any of the three would close it; the implementation chose none. Concession: spec should have specified; implementation should have picked one. Net: both share blame; R2 fix is a single `TRACEABILITY.md` mapping commit → D-NNN.

---

## New Evidence Not Presented in R1

Reading the impl-advocate's R1 + reading source surfaced four new in-code observations that sharpen the spec-advocate's case:

1. **`PrdClaudeProcess.terminate()` is a regression-by-omission (F MEDIUM-1).** Direct read of `src/superclaude/cli/prd/process.py:239-279` confirms the override is a pre-P-004 clone missing the `_stdin_error` log block. R1-impl's Strength #2 ("error-surfacing delivered faithfully") is true for the base class only. **This is a HIGH-severity finding the spec-advocate did not have in R1**: the entire P-004 error-surfacing benefit is silently nullified for the PRD pipeline under SIGTERM-only paths (i.e., when `wait()` does not run after `terminate()`). The spec should have included an invariant check: "all subclasses overriding `terminate()` must call `super().terminate()` or replicate the surfacing block." It did not, and PRD diverged.

2. **`PROMPT_MAX_BYTES` import-time crash on non-numeric env (F MEDIUM-2).** Direct read of `pipeline/process.py:27-29` confirms `int(os.environ.get(...))` raises at *module import time*. **Every consumer of `superclaude.cli.pipeline.process` crashes** if an operator typos `SUPERCLAUDE_PROMPT_MAX_BYTES=16MB` in a Dockerfile or systemd unit. Spec §4 P-002 did not require try/except — this is a spec gap, not just an implementation gap. R2 should land the 5-line `_resolve_prompt_max_bytes()` helper AND amend the spec to require resilient env parsing.

3. **`PROMPT_MAX_BYTES = 0` admits empty prompts (F Q7).** Spec did not consider `PROMPT_MAX_BYTES=0` as an edge case. With `prompt=""`, `len(b"") > 0` is False — empty prompts pass the guard even with cap=0. With any non-empty prompt, the guard fires. The behavior "0 means disable empty prompts only" is non-obvious. Spec should explicitly state minimum cap (or document the corner case). Minor but real spec gap.

4. **`build_command()` is invoked twice per `start()` (F NIT-3).** At `pipeline/process.py:163` (Popen) and `:184` (debug log slice). For PortifyProcess this re-runs the dual-`--add-dir` accumulation logic. T-010 pins idempotency so correctness holds, but it is wasted work and a micro-coupling: a future PortifyProcess override that mutates `self._consolidated_dirs` between calls would silently corrupt argv. Spec did not pin "build_command() must be called exactly once per start()." Minor invariant gap.

Together, findings 1 and 2 are HIGH-impact in-code residuals that R1-impl's "patches landed faithfully" framing under-weighted. The spec-advocate's R1 critique was about process artefacts (deployment, checklist, traceability); these new findings sharpen the case to *also* include downstream-subsystem propagation and operator-hostility — categories that the original DESIGN.md's "always-stdin migration" reconciliation did not cover.

**Updated spec-advocate position**: the original "22 unique-to-B unimplemented" headline is correct in count but mis-weighted in severity. The two highest-severity residuals are NOT in the original 22 (which were process artefacts); they are PrdClaudeProcess.terminate (subclass propagation) and the env-var parser (operator-hostility), both surfaced post-R1 by F and confirmed by direct source read. R2 should land both fixes inside the same branch.

---

**End of r2-spec-advocate.md**
