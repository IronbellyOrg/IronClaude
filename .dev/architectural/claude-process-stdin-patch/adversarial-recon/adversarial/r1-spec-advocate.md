# Round 1 — Spec-Advocate Position

**Role:** Spec-keeper / QA lead arguing for `variant-2-spec.md` (RECONCILED_DESIGN.md)
**Round:** 1 · **Focus:** spec coverage · missing implementations · drift

---

## Position Summary

The 5 patches landed cleanly and the test file is structurally sound — but the diff-analysis headline of **22 unique-to-B unimplemented items** is not a runbook footnote. It represents the spec's process scaffolding (acceptance ledger, deferral tracking, deployment validation, provenance map) that "approved-with-nits" silently writes off. The spec is the contract; under-delivery against §10's 8-item checklist and the §3.2 deferral ledger means we shipped *code* without shipping *closure*.

---

## Steelman of Impl-Advocate's Position

- **Code-level convergence is genuinely high (C-001..C-044).** Every P-001..P-005 patch matches B's "After" block. Forty-four content rows are Low-severity matches — no missed patch.
- **All 11 T-NNN tests landed (C-037..C-044).** Payloads match (400 KB ASCII, 200 KB emoji, oversize cap, SIGTERM-no-hang, BrokenPipe). A *exceeds* B with `test_prompt_under_cap_passes_guard` (U-008) and `test_tool_write_mode_false` (U-009).
- **Mechanical correctness verified.** EINTR retry (C-007), `finally`-close (C-014), `_stdin_error` capture + `_log.warning` in both `wait()`/`terminate()` (C-008) match B§4 P-004 exactly.
- **`tool_write_mode` regression net in tree (C-036).** P-005 was test-only by design; A delivered T-007 + negative companion. Previously-zero coverage gap closed.
- **A is *stricter* than B in 4 places.** T-001 ceiling at 4 KiB vs MAX_ARG_STRLEN's 128 KiB (C-011); T-005 hang budget 18s vs 16s; U-003 explains 4799719 history; spawn log carries `prompt_bytes=N` per D-099.
- **DEFER-TO-BEAT-2 (U-024) is *correctly* deferred.** Sidecar/monkey-patch/`pre_prompt_args`/`--input-format=stream-json` are out-of-scope. B itself routes them to beat 2 (§3.2 L128).
- **Risk #1 (P0 probe) resolved upstream (U-019).** A bases on `142ce15` so 4799719 + 39d5100 survive — exactly per B§2.
- **Drift items (U-001..U-016) are mostly defensive coding gloss** — pragmas, `if n <= 0: break`, `getattr` reads — none altering user-visible contract.

---

## Strengths Claimed

1. **§1 supersession is load-bearing and survives.** B§1 names 4799719 + 39d5100 as load-bearing; A's branch base preserves both (maps to A-001).
2. **§2 LOC inventory tracks 7 files (S-003).** A diffs only 3 — `sprint/process.py`, `cleanup_audit/process.py`, `test_process_hooks.py`, `cli_portify/test_process.py` are *unverified* for non-regression (A-010).
3. **§3.1 in-scope ledger has ~40 D-NNN items.** A's commits preserve at most 5 (the P-IDs), losing D-007/014/020/021/025/026/032/034/036/040/046–048/052/058–062/066/068/071/099/107/108 traceability (S-008).
4. **§3.2 SUPERSEDED list (12 items) records *consciously dropped* work** — D-002/004/017–19/023/024/028/042/050/053–55/057/075/109. Zero in-tree counterpart (U-023/S-004); future readers cannot distinguish "rejected" from "forgotten."
5. **§3.2 DEFER-TO-BEAT-2 (15 items) names post-baseline work.** Sidecar (D-016/022/035/064/065/072/073), monkey-patch (D-077/085/087), beat-2 architecture (D-093/095/096/097), `force_prompt_via` (D-098). A drops it (U-024).
6. **§4 patches are atomic and provenance-tagged.** Each P-NNN cites D-NNN, AC, provenance, file, anchor lines. A's commits ship code but lose the cross-walk.
7. **§5 test table prescribes mocking + pass/fail per test.** A delivers mechanics but not the documented pass/fail criteria.
8. **§6 risks-resolved cites P0 probe date + claude version.** A doesn't restate verification in-tree (U-025).
9. **§7 R-1..R-6 risk register.** R-2 (sync stall, HIGH) and R-3 (silent BrokenPipe) mitigated by P-004; R-4 (empty-prompt) and R-5 (heap-doubling) *accepted* deferral. Without the register in-tree, future readers can't tell "fixed" from "accepted."
10. **§8 commit sequence prescribes ordering + rationale.** Step 1: P-001 first as "regression baseline." A's `git log` shows `526a606` as the *oldest* commit (X-001) — final state right, rationale lost.
11. **§9.1 pre-merge test commands explicit:** `tests/pipeline/`, `tests/cli_portify/test_process.py`, `tests/roadmap/test_file_passing.py`, `test_inline_fallback.py`, `make test`. No in-tree run-evidence (U-029/030).
12. **§9.2 deployment plan: pipx rebuild + Coder repro (U-031, HIGH).** `uv build`, `pipx install --force`, re-run of the originally-failing 338 KB roadmap. Zero artifact in A.
13. **§10 8-item checkbox is verifiable closure (U-032, HIGH).** A satisfies items 1–3; items 4–8 (AC verdicts, Risk verdicts, sync-clean, Coder repro) have no satisfaction artifact.
14. **§10's AC-1..AC-10 verdict mapping ties delta to DESIGN.md.** Without it, "approved-with-nits" lacks a checklist to be approved against.
15. **§11 provenance appendix is the audit-trail spine.** Maps P-NNN/T-NNN to D-NNN/AC/Risk; A's commits drop these refs (S-008).
16. **D-086 re-run 338 KB roadmap is the original-bug-repro (U-021, HIGH).** Only validation that the patch fixes the failure mode it was built for. Zero evidence in A.
17. **D-067 CI integration (U-017).** No `.github/` change; CI unverified.

---

## Weaknesses Identified in Implementation

### HIGH

- **W-H1 (U-021 / D-086):** Original-bug-repro step is unexecuted. The 338 KB Coder prompt was the failure that motivated this patch; without re-running it, we have no production-validation that chunked write fixes the case it was built for. *Unit coverage ≠ repro-resolution at the original failure point.*
- **W-H2 (U-031 / §9.2):** Pipx rebuild + Coder re-run deployment plan entirely unaddressed. Operators cannot consume this fix until pipx is rebuilt. The vendored-monkey-patch alternative (D-077/085/087) is also deferred — so until §9.2 runs, the downstream consumer is *still broken*.
- **W-H3 (U-032 / §10):** Acceptance checklist is satisfied at most 3-of-8. Items 4–8 (AC-1..AC-10 verdicts, Risk #1..#6 verdicts, `make sync-dev`/`make verify-sync` clean, Coder roadmap-run succeeds) have no in-tree satisfaction artifact. "Approved-with-nits" overstates closure.
- **W-H4 (U-024 / §3.2 DEFER ledger):** 15-item deferral list has *no owner, no tracking issue, no TODO*. Sidecar, monkey-patch, `pre_prompt_args`, `--input-format=stream-json`, sidecar rotation, `PromptSource` Protocol, `force_prompt_via`. **Deferred work without a tracking surface is lost work.** Single largest spec-coverage gap.
- **W-H5 (S-004 / §3.2 SUPERSEDED ledger):** ~12-item SUPERSEDED list has zero in-tree audit trail. Future readers cannot distinguish "rejected with reason" from "forgotten." A maintainer reading DESIGN.md who sees D-002/D-004 unimplemented cannot tell the always-stdin migration superseded them.

### MEDIUM

- **W-M1 (X-004 / D-071):** Debug log token `prompt_via=stdin` is **missing** from A. A logs `"spawn pid=%d cmd=%s prompt_bytes=%d"`; B specified `"... prompt_via=stdin prompt_bytes=%d"`. **Operators grepping `prompt_via=stdin` get zero matches.** Telemetry contract D-099 silently broken.
- **W-M2 (X-006 / T-011):** BrokenPipe-surfacing is **conditionally** asserted (diff L484-488: "If it did break, ensure we surfaced it; otherwise nothing to assert"). Spec promised unconditional. **Test cannot fail if surfacing logic is removed** — mutation-kill for BrokenPipe→`_log.warning` is zero in some race outcomes.
- **W-M3 (U-007 / inconsistency):** Asymmetric `_stdin_error` read. `wait()` uses direct access (L180); `terminate()` uses `getattr` (L191). **If `terminate()` is called before `start()`, `wait()` AttributeErrors but `terminate()` doesn't.**
- **W-M4 (X-001 / commit order):** §8 step 1: P-001 first as "regression baseline." A's `git log` shows `526a606` as *oldest* commit — final state right, rationale lost on cherry-pick.
- **W-M5 (S-002 / supersession):** A's `fde1431` flips DESIGN.md to historical but cross-link to RECONCILED_DESIGN.md is unverified (U-028 partial).
- **W-M6 (S-008 / provenance):** Loss of D-NNN linkage in commit messages. Future audit tooling has no edges to follow.
- **W-M7 (U-029 / pre-merge tests):** §9.1 prescribes `tests/cli_portify/test_process.py` (517 LOC), `tests/roadmap/test_file_passing.py`, `test_inline_fallback.py`. No run evidence.
- **W-M8 (U-017 / D-067 CI):** No `.github/` change. CI wiring unverified.
- **W-M9 (U-026 / R-4 empty-prompt):** §7 R-4 classified DEFER-TO-BEAT-2 accepted but A has no follow-up tracking. T-006 commits us to current behavior without contract-test on `claude --print` empty-stdin semantics.
- **W-M10 (U-027 / R-5 heap-doubling):** §7 R-5: "deferred to beat 2 if telemetry shows it matters." **A has no telemetry hook.** Deferral committed without instrumentation to validate.
- **W-M11 (U-014 / undocumented commit):** `db8cffe docs: STRICT-tier review` is in A but not B's §8 (7 commits vs A's 8).
- **W-M12 (U-018/U-020):** Single-PR + upstream-PR opening — diff shows no PR creation or RECONCILED_DESIGN.md attachment.
- **W-M13 (A-002 / blocking-FD):** `os.write` loop assumes blocking FD. UNSTATED. On non-blocking, EINTR-only retry would underwrite (no `EAGAIN`).
- **W-M14 (A-010 / subclass non-regression):** `sprint/process.py` + `cleanup_audit/process.py` could regress if base shape changed. Diff scope provides no assurance.
- **W-M15 (A-011 / `make sync-dev`):** Per CLAUDE.md, `make verify-sync` is mandatory pre-commit. A's diff shows `src/superclaude/` only — `.claude/` mirror unverified.

### LOW

- **W-L1 (X-002):** A asserts `elapsed < 18.0`; B says "< 16s." Off-spec by 2s.
- **W-L2 (X-003):** A uses `< 4*1024`; B says `≤ 4 KB`. Off-by-one inversion.
- **W-L3 (X-005):** B's spec text says `proc.poll()` (nonexistent on `ClaudeProcess`); A correctly uses `proc._process.poll()`. B's spec is wrong; A right but in conflict with literal spec.
- **W-L4 (U-022 / D-088):** B caps `pipeline/process.py` at "+40-60 LOC"; A's diff is +60/-7 — at upper edge. No tracking artifact.
- **W-L5 (U-037 / D-068):** B specifies `pytest.fixture` set; A inlines payloads. Functional equivalent, not the structured form.
- **W-L6:** Two `# pragma: no cover` annotations not in B (U-001/U-002). Harmless drift.
- **W-L7:** A's PortifyProcess comment block (diff L34-40) more verbose than B requested.
- **W-L8:** A scopes caplog to `"superclaude.pipeline.process"`; B doesn't specify logger.
- **W-L9 (NUL-byte gap):** Neither A nor B exercise NUL bytes (`\x00`) in the prompt. Possible mojibake or premature-EOF on some `os.write` fast paths. **Mutation-kill gap** for the encoding path.
- **W-L10 (finally-close mutation kill):** T-011's conditional assertion (W-M2) means the `finally: stdin.close()` block has no test that *fails* if the close moves out of `finally`. Coverage exists; mutation-kill does not.

**Total: 30 weaknesses** (HIGH=5, MEDIUM=15, LOW=10).

---

## Concessions

1. **The 5 patches landed cleanly.** P-001..P-005 match B's "After" blocks (35 Low-severity matches in C-001..C-035).
2. **The new test file is structurally sound.** 11 functions/6 classes, payloads correctly sized, mocking pattern reusable.
3. **Chunked-write EINTR retry is textbook correct** (C-007 matches B§4 P-004); `finally: stdin.close()` correct (C-014/D-108).
4. **`tool_write_mode` regression net exceeds spec.** A shipped T-007 + a negative companion (U-009); B asked for one.
5. **Portify `--output-format` anchor fix (P-001) is mechanically right.** Splice at `index+2`, defensive `extend` fallback, T-008/T-009/T-010 pin the new contract.
6. **A is stricter than B in three useful places:** T-001 4 KiB ceiling, `prompt_under_cap_passes_guard` boundary, `tool_write_mode_false` negative.
7. **`4799719` + `39d5100` correctly preserved.** Branch base at `142ce15` ensures stdin migration + `tool_write_mode` survive. Spec accommodation was correct.
8. **DEFER-TO-BEAT-2 *content* identification is correct.** Sidecar/monkey-patch/`pre_prompt_args` are genuinely not-now. Deferral *decision* sound; only *tracking* missing.
9. **Test strength 4/5 is honest.** Missing 1/5 lives in mutation-kill rate (W-L9, W-L10, W-M2) — coverage exists, mutations slip past in race outcomes. F's 4/5 is fair; gap real but not fatal.
10. **Code-level drift is mostly defensible.** U-001/002/005/008/009/010/011/012 are *positive-value* drift. Only U-007 (asymmetric `getattr`) is genuinely problematic.

---

## Response to Shared Assumptions (A-NNN)

| ID | Verdict | Reasoning |
|----|---------|-----------|
| **A-001** (claude accepts unbounded stdin) | **ACCEPT-with-promotion** | B§6 cites 2026-04-30 P0 probe on `claude 2.1.123`. Load-bearing across all of A. Risk: claude version drift breaks the world. Pin version in §9.1 deployment notes. |
| **A-002** (blocking FD) | **ACCEPT-with-promotion** | UNSTATED in both. EINTR-only retry assumes blocking; `EAGAIN` not handled. Action: assert `os.get_blocking(fd) is True` or document. |
| **A-003** (`tool_write_mode` ⊥ stdin redirect) | **ACCEPT-with-promotion** | B's P-005 says "preserve dual stdout-handle path." Promote to docstring-asserted contract on `tool_write_mode` parameter. |
| **A-004** (Portify never emits `-p`) | **REJECT-as-shared** | Already STATED in both (B§3.1 D-051) and ENFORCED in T-006/T-008. No promotion. |
| **A-005** (Linux MAX_ARG_STRLEN on all targets) | **QUALIFY** | STATED for Linux; UNSTATED for non-Linux. WSL inherits. T-001's 4 KiB ceiling is portable enough. Note in deployment docs. |
| **A-006** (single-shot `ClaudeProcess`) | **ACCEPT-with-promotion** | UNSTATED. Reusing instance after `wait()` carries stale `_stdin_error`. Promote: docstring `start()` "single-shot; second call undefined." |
| **A-007** (~64 KiB pipe buffer) | **REJECT-as-shared** | STATED-with-fudge in both; tuning hint, not invariant. |
| **A-008** (`os.write` returns 0 only on error) | **REJECT-as-shared** | STATED via `if n <= 0: break`. Explicit. |
| **A-009** (EINTR sole transient) | **QUALIFY** | LINKED to A-002. Resolution lives in A-002's docstring/assertion. |
| **A-010** (out-of-scope files unchanged) | **ACCEPT-with-promotion** | UNSTATED. Subclass files inherit base shape. Promote: §9.1 should add `tests/sprint/ tests/cleanup_audit/` to pre-merge gate. |
| **A-011** (`make sync-dev` ran) | **ACCEPT-with-promotion** | STATED in B§9.1; UNVERIFIED in A. Per CLAUDE.md, `make verify-sync` is mandatory pre-commit. Should be a gate, not honor system. |

**Promotions: 7 of 11** (6 strict + 2 qualified linked). 3 rejected as already-stated.

---

## Focus Coverage

Per `--focus "spec coverage, missing implementations, drift"`:

- **Spec coverage:** Strengths §1-17 cite B§1-§11 section-by-section; W-H4/H5/M6/M7 hit §3.2 ledger, §9.1 test commands, §11 provenance. 22-unimplemented headline is the load-bearing gap.
- **Missing implementations:** W-H1 (D-086 repro), W-H2 (§9.2 deployment), W-H3 (§10 checklist), W-M8 (D-067 CI), W-M11–M15 (PR, sync-dev, subclass non-regression) — 7 distinct items.
- **Drift:** W-M1 (log token), W-M2 (conditional assertion), W-M3 (asymmetric defensive), W-M4 (commit order), W-L1–L3 (test thresholds), W-L6–L8 (defensive coding). Distinguished *positive-value* drift (Concession 10) from *contract* drift (W-M1/M2/M3).

All three lenses addressed. Drift is smallest issue; spec-coverage and missing-implementations are the load-bearing critique. The implementation is *good code* against the *patch portion* of the spec, but *incomplete delivery* against the *spec as a whole*. RECONCILED_DESIGN.md is a closure contract, not just a patch list — §10's checkbox, §9.2's deployment plan, §3.2's deferral ledger, §11's provenance spine are deliverables, not commentary. The 22-unimplemented count is the gap between *patches landed* and *delta closed*.
