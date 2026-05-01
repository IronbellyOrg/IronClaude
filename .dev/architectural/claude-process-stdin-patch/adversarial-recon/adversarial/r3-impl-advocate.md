# Round 3 — Implementation-Advocate Final Position

**Variant defended**: `variant-1-implementation.md` (8-commit diff `142ce15..db8cffe`).
**Round**: 3 (final after invariant-probe blocked convergence on 2 HIGH UNADDRESSED items).

---

## Final Position (1-3 sentences)

The base-class delta is mechanically correct and the eleven T-NNN tests are in tree, but the invariant probe is right that the PRD subclass override at `prd/process.py:239-279` is a regression-by-omission for P-004's `_stdin_error` surfacing — that *is* an in-code residual on this branch, not a process artefact, and it must land before merge as a 4-line fix plus regression test, paired with a cheap `_resolve_prompt_max_bytes()` helper closing F's MEDIUM-2. I treat the spec-advocate's reframed critique as substantively right on subclass propagation and operator-hostile env parsing while still rejecting the demand that operational artefacts (§9.2 pipx rebuild on Coder, §10 eight-item ledger, §3.2 SUPERSEDED narrative) live inside this code diff.

---

## Resolution of HIGH UNADDRESSED Invariants

### INV-004 — `PrdClaudeProcess.terminate()` does not surface `_stdin_error`

**Concede the gap.** Verified: `src/superclaude/cli/prd/process.py:239-279` is missing the surfacing block. Compare base at `src/superclaude/cli/pipeline/process.py:288-291`:

```python
if getattr(self, "_stdin_error", None) is not None:
    _log.warning("stdin_error pid=%s err=%r", self._process.pid, self._stdin_error)
```

PRD's override jumps from SIGKILL block (`:281`) past `_log.debug("exit ...")` analog directly to `_on_exit` and `_close_handles()` at `:277-279`. Under SIGTERM-only paths (executor calls `terminate()` without `wait()`), PRD silently swallows BrokenPipe — the exact failure mode P-004 was authored to fix.

**Remediation (R3 patch, lands this branch):**
- File:line: `src/superclaude/cli/prd/process.py:277` — insert 4-line block immediately before `_close_handles()`, byte-identical to `pipeline/process.py:288-291`.
- Owner: branch author (same as P-004).
- Commit: `fix(prd): surface stdin_error from PrdClaudeProcess.terminate`.
- Acceptance: `git diff` shows 4-line addition; review confirms byte-equal to base block.

### INV-025 — `PrdClaudeProcess + BrokenPipe + terminate-without-wait` zero test coverage

**Concede the gap.** T-005 (`test_process_stdin.py:412-446`) and T-011 (`:465-488`) are base-class only. Nothing pins PRD subclass surfacing.

**Remediation (R3 test, lands this branch):**
- New file: `tests/pipeline/test_prd_process_stdin.py` with `test_prd_terminate_surfaces_stdin_error` using `monkeypatch.setattr(os, "write", _raise_broken_pipe)` for deterministic injection (same mechanism resolving X-006).
- Asserts `caplog` contains WARNING with `"stdin_error"` after `proc.start(); proc.terminate()`.
- Owner: branch author.
- Commit: `test(prd): pin PRD terminate stdin_error surfacing`.
- Acceptance: passes after INV-004 fix; **fails** if 4-line block removed (mutation-kill validated).

**Net**: both HIGH items collapse to a 4-line code change + ~15-line test on the same branch, same owner, before merge.

---

## Final Concessions

Cumulative across all rounds:

1. **U-007** (R1) — `wait()` direct attribute access; init `self._stdin_error = None` in `__init__`. **R3.**
2. **X-004** (R1) — `prompt_via=stdin` literal missing from spawn log at `pipeline/process.py:181-186`. One-line edit. **R3.**
3. **X-006** (R1) — T-011 conditional assertion. Replace with `monkeypatch` mock-injected unconditional. **R3.**
4. **U-035** (R1) — D-NNN traceability lost. Add `TRACEABILITY.md` mapping commit→D-NNN. **R3.**
5. **U-024** (R1) — 15 DEFER-TO-BEAT-2 items untracked. Add `BEAT_2_BACKLOG.md`. **R3.**
6. **U-021** (R1) — D-086 338 KB Coder repro. PR-comment artefact. **Pre-merge, post-code.**
7. **INV-004 / F MEDIUM-1** (R3 NEW) — PRD subclass surfacing. 4-line patch. **R3.**
8. **INV-025** (R3 NEW) — PRD subclass test gap. New test file. **R3.**
9. **INV-009 / F MEDIUM-2** (R3 NEW) — `int(os.environ.get(...))` import-time crash at `pipeline/process.py:27-29`. Replace with `_resolve_prompt_max_bytes()` helper that catches `ValueError` and falls back to default with `_log.warning`. **R3.**
10. **INV-002** (R3 NEW) — `_stdin_error` not in `__init__`. Init alongside U-007 fix. **R3.**
11. **INV-014** (R3 NEW) — `n <= 0` silent break in chunk loop. Set `self._stdin_error = OSError(f"zero-byte write at offset {offset}/{len(view)}")` before `break` so truncation is observable. **R3.**
12. **W-L9** (R2) — NUL-byte prompt round-trip not pinned. Add `test_nul_byte_prompt_round_trip` (`b"\x00" * 1024`). **R3.**
13. **W-L10** (R2) — `finally`-close mutation-kill missing. Inject OSError via `monkeypatch`, assert `_process.stdin.closed` post-call. Pairs with X-006 fix. **R3.**

**Total concessions: 13** (R1: 6 + R2: 0 net new + R3: 7 new in-code).

---

## Remaining Disagreements

1. **W-H2 / U-031 (§9.2 pipx rebuild on Coder).** Spec demands closure pre-merge; impl maintains cross-host operational delivery cannot live in `git diff`. **Compromise**: `make ship-coder` Makefile target documenting the recipe (`uv build` → `pipx install --force` → re-run failing roadmap) lands this branch; release-engineer runs it post-merge. Divided ownership.

2. **W-M11 / U-014 (8th commit `db8cffe`).** Spec calls "undocumented" because §8 lists 7 commits. That commit imports F-strict-review.md which spec-advocate's R2 cites repeatedly (R2 New Evidence #1, #2 ARE F findings). §8 was written before F-review existed. **STILL-DISPUTED**, low impact.

3. **W-L1 / X-002 (18s vs 16s SIGTERM).** Spec calls off-spec. Impl: `start()` prelude (file open, Popen fork) consumes wall time before 10s SIGTERM + 5s SIGKILL window; 18s is mathematically conservative, 16s could flake on slow CI. **STILL-DISPUTED on numeric symmetry; agreed on functional equivalence.**

4. **W-M4 / X-001 (commit-order rationale).** `git log --oneline` displays newest-first; `526a606` IS the oldest (first-applied) commit, matching §8 step 1. Rationale lives in merge-commit body and PR description. **STILL-DISPUTED on framing; agreed on physical chronology.**

5. **§3.2 SUPERSEDED ledger (W-H5 / S-004).** Spec wants in-tree audit trail for ~12 SUPERSEDED items. Items made obsolete by `4799719`/`39d5100` are visible in `git log` plus RECONCILED_DESIGN.md §3.2. If reviewers still object after R3, append SUPERSEDED to BEAT_2_BACKLOG.md as second appendix. **DEFERRED-WITH-OWNER (branch author, contingent on reviewer pushback).**

---

## Convergence Reassessment

**HIGH UNADDRESSED status (impl-advocate view)**:
- INV-004: **ADDRESSED** by R3 (4-line patch at `prd/process.py:277`, owner = branch author, pre-merge).
- INV-025: **ADDRESSED** by R3 (new `tests/pipeline/test_prd_process_stdin.py`, owner = branch author, pre-merge).

Both have explicit file:line, fix sketch, owner, acceptance criteria. **Convergence no longer blocked.**

**Final per-bucket counts**:

| Bucket | Count | Items |
|---|---|---|
| ACCEPTED (lands R3) | 13 | All Final Concessions §1-§13 |
| DEFERRED-WITH-OWNER | 4 | U-021 (release-eng, PR-comment), U-031 partial (release-eng via `make ship-coder`), §3.2 SUPERSEDED appendix (branch author, contingent), TRACEABILITY.md scope details (branch author) |
| REJECTED (no fix) | 7 | W-L1 (X-002), W-L3 (X-005), W-L4 (LOC budget), W-L5 (fixture style), W-L6 (pragma), W-L7 (verbose comment), W-L8 (caplog scope) — all stylistic / contract-equivalent |
| STILL-DISPUTED | 4 | W-H2 framing, W-M11 8th commit, W-L1 numeric symmetry, W-M4 commit-order framing |

**Recommended convergence score**: **0.85**.

Rationale: all spec-claimed in-code residuals (subclass propagation, env-var crash, log token, mutation-kills, defensive asymmetry) have remediation patches with file:line and owner, all R3. Four operational/process items DEFERRED-WITH-OWNER with named accountability (release-engineer for Coder repro and `make ship-coder`, branch author for traceability artefacts). Four stylistic disputes are contract-equivalent. Score 0.85 reflects strong consensus on substance with non-blocking residual process disagreements.

---

**End of r3-impl-advocate.md**
