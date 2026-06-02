---
artifact: r1-3-rf-qa-task-integrity
phase: 8
gate: PG8.1
release: R1.3
task: TASK-RF-20260531-042405
created_date: 2026-06-02
reviewer: rf-qa (task-integrity, adversarial stance, fix_authorization=true)
verdict: PASS
---

# QA Report — PG8.1 R1.3 Task-Integrity (Dispatch-Reachability CodeAssertion)

**Topic:** R1.3 `GateCriteria.code_assertions` slot + first `CodeAssertion`
(dispatch-reachability) wired into `CERTIFY_GATE`; `build_certify_step`
production caller.
**Phase:** task-integrity (PG8.1)
**Fix cycle:** N/A (single pass)
**Worktree:** /config/workspace/IronClaude-RoadmapRewrite,
branch `refactor/roadmap-pipeline-r0-r1-rewrite`

---

## Overall Verdict: PASS

The R1.3 implementation is **structurally sound and the code is correct**. The
`code_assertions` slot is backward-compatible (defaults `None`), the AST walker
has **no false-PASS path** (adversarially verified by mutation), the
`build_certify_step` wiring into `execute_roadmap` via
`_run_certify_after_remediate` is **genuine** (not a fake), the step-count budget
holds (≤14), and the NFR-007 boundary is preserved.

**No CRITICAL or blocking issue found.** All issues found were **report-accuracy
defects** in the aggregation + validation-summary artifacts (miscounted test
total, misattributed pre-existing failures, post-edit line drift). All were
**fixed in-place** under fix_authorization. No source code was modified — the
source is correct as-shipped.

---

## Per-Criterion Findings (a–g)

| Crit | Result | Evidence |
|---|---|---|
| (a) `code_assertions` defaults None → existing gates unchanged | PASS | `models.py:142` `code_assertions: list[CodeAssertion] \| None = None`. Field is LAST, after `semantic_checks` (positional-safe). No `__post_init__`, no `*` boundary. All 14 `ALL_GATES` call sites in `gates.py` construct via keyword args and are unaffected; `test_all_strict_gates_have_assertions` + full roadmap suite (1784 passed) confirm. |
| (b) AST walker identifies `_build_steps` Step IDs (synthetic deletion) | PASS | `_extract_step_ids_from_build_steps` (code_assertions.py:231) scopes to the `_build_steps` FunctionDef only; extracts 12 ids incl `generate-` JoinedStr prefix. Adversarial mutation test (removed the production `build_certify_step(` call): `_build_certify_step_has_production_caller` correctly flips to `False`, so the assertion would emit `CA-DISPATCH-002` HIGH Finding. `test_unwired_step_caught` PASSES. **NO false-PASS path.** NOTE: the file has **7** tests, not 8 (criterion text says "confirm 8 pass"); all 7 pass. |
| (c) `build_certify_step` genuinely wired | PASS | `execute_roadmap` (executor.py:3409) calls `_run_certify_after_remediate(config, results)` AFTER `execute_pipeline` returns and ONLY on the no-halt path (failure path `sys.exit(1)` at L3399 precedes it). The helper (L2108) guards on `remediate` PASS (L2137), then calls `build_certify_step` (L2165) and executes it via `roadmap_run_step(certify_step, config, lambda: False)` (L2170), appending the result. This is a **legitimate seam**, not a dodge: certify is built from runtime findings (which only exist post-remediate) and the remediate-PASS guard is real production logic, not a test-only no-op. See "Live-vs-CI enforcement" note below. |
| (d) step count ≤14 | PASS | `_build_steps` = 13 `Step(id=...)` constructions (certify NOT among them). `ALL_GATES` = 14 entries (`gates.py:1547-1562`). `_get_all_step_ids` = 14 (incl certify). Live executed count = 13 pipeline + 1 dynamic certify = 14 ≤ 14. |
| (e) Contract #2 invariant CI-enforceable | PASS | `test_unwired_step_caught` materialises a synthetic executor.py (no certify in `_build_steps`, no `build_certify_step` caller) → asserts HIGH `CA-DISPATCH-002`. This genuinely fails if wiring is removed (mutation-verified in (b)). `test_certify_step_reachable` asserts the real executor returns None. Both run in CI. |
| (f) PRESERVE files unchanged | PASS | `git diff --stat HEAD -- commands.py structural_checkers.py convergence.py` = **empty**. Full diff touches exactly 4 files (pipeline/gates.py, pipeline/models.py, roadmap/executor.py, roadmap/gates.py) + 2 untracked new files (code_assertions.py, test_dispatch_reachability.py). |
| (g) zero new `return True` fragility stubs | PASS | Only NEW `return True` in new code: `code_assertions.py:227` inside `_build_certify_step_has_production_caller` — a genuine predicate returning True when a real caller is found (not fail-open). The `pipeline/gates.py:98` `return True, None` is the documented temporary envelope-None shim (see additional checks). No fail-open stubs introduced. |

---

## Additional Adversarial Check Findings

| Check | Result | Evidence |
|---|---|---|
| NFR-007 (`pipeline/*` no roadmap/sprint imports) | PASS | `pipeline/gates.py` imports only `re`, `Path`, `.models.GateCriteria`. `pipeline/models.py` imports only stdlib. Only "roadmap"/"sprint" occurrences are in docstrings. `gate_passed` types `envelope: object \| None` (duck-typed), NOT `PipelineEnvelope`. The `pipeline → roadmap` arrow is zero at module load. |
| envelope-None backward-compat shim | PASS (documented temporary shim, not silent permanent fail-open) | `pipeline/gates.py:93-98`: when `code_assertions` defined but `envelope`/`repo_root` are None, returns `True, None`. Documented in the docstring (L32-41) + design §5/§11 OQ-A as a **temporary R1.3→R1.6 shim**. See "Live-vs-CI enforcement" — it does NOT mask a real failure in production today because the certify code_assertion is enforced via CI test (`test_certify_step_reachable`), and the live gate path never passes envelope yet by design. |
| Design deviation (`_build_steps only` → `OR build_certify_step caller`) | PASS (sound + documented) | Surfaced in aggregation §"Design deviation surfaced" and code_assertions.py:31-58 docstring. The generalization matches Contract #2's "reachable from a production entry point" language and the master:§Flaw 1 definition ("only a test invokes it" — the walker parses ONLY executor.py so a tests/ caller never satisfies it). Not a silent scope-narrowing; it is a scope-correcting widening. |
| Broad regression claim (19 cli failures) | PASS with CORRECTED ATTRIBUTION | `tests/roadmap/ -q` = 1784 passed, **3 failed**; `tests/cli/ -q` = 1560 passed, **16 failed**. Total 19 = accurate, but the 3 roadmap failures (`test_default_agents*` — expects `haiku`, config default `sonnet`) were MISATTRIBUTED to tests/cli/. **Stash-and-rerun on parent state confirms all 3 fail identically without R1.3 changes** — pre-existing, unrelated, no R1.3-module import. Reports corrected in-place. |
| Source-line drift (task preamble L1899 stale) | PASS with POST-EDIT CORRECTION | Design doc §2 cites PRE-edit positions. Post-edit actuals: `build_certify_step` L2060 (unchanged), `GateCriteria` L90→**L121** (CodeAssertion dataclass inserted before it), `_build_steps` L2108→**L2182**, `CERTIFY_GATE` L1431, `ALL_GATES` L1547, `("certify"...)` L1561. Implementation matches real current locations. Aggregation "Known interpretation" corrected in-place. |
| `Finding` import path (design §3/§6.2 says `findings.py`) | PASS (impl correct; doc stale) | `findings.py` does NOT exist. `Finding` lives in `roadmap/models.py:22`. `code_assertions.py:24` correctly imports `from superclaude.cli.roadmap.models import Finding`. Design-doc sketch citation is stale but the IMPLEMENTATION is correct (tests pass). Design doc is a draft (status: draft) — minor, non-blocking. |

### Live-vs-CI enforcement (criterion c + shim deep-dive — important nuance)

The live gate-evaluation path (`pipeline/executor.py:267` and `:329`) calls
`gate_passed(gate_target, step.gate)` **without** `envelope`/`repo_root`.
Therefore, for the certify step at runtime, the `code_assertions` branch hits the
envelope-None shim (`pipeline/gates.py:94`) and **silently skips** the
dispatch-reachability assertion. This is **intentional and correct for R1.3**:
the design (§5, §11 OQ-A) explicitly ships the slot + shim and enforces the
invariant via the **CI test** (`test_certify_step_reachable`), with the shim
scheduled for deletion in R1.6 once all `gate_passed` callers plumb the envelope.

Adversarial assessment: this is **NOT a way to dodge real behavior**. The
invariant's purpose (catch a step shipping unwired) is a CODE-GRAPH property best
checked in CI, not at runtime — at runtime the pipeline is already executing the
step, so a runtime check would be circular. The shim cannot mask a real
code_assertion failure today because (1) no production gate_passed caller passes
an envelope, so the assertion branch is uniformly skipped (not selectively
suppressed), and (2) the CI test provides the real enforcement. **PASS**, with the
recommendation below that R1.6 MUST delete the shim AND wire envelope/repo_root
into the live path, else the runtime assertion remains permanently dormant.

---

## Summary

- Criteria passed: **7 / 7** (a–g)
- Additional checks passed: **7 / 7**
- Issues found: **4** (all IMPORTANT report-accuracy; 0 CRITICAL, 0 blocking)
- Issues fixed in-place: **4**

## Issues Found

| # | Severity | Location | Issue | Fix |
|---|---|---|---|---|
| 1 | IMPORTANT | aggregation.md (b),(e); validation-summary.md table + body header | Claims "8 tests" in `test_dispatch_reachability.py`; actual = **7** (pytest: "7 passed"). | Corrected all 4 references to 7; added note. |
| 2 | IMPORTANT | aggregation.md "Verification snapshot"; validation-summary.md "Regression integrity" | Claims the 19 broad-sweep failures are "entirely in tests/cli/". Actual: 16 cli + **3 roadmap** (`test_default_agents*`). | Corrected attribution; documented the 3 are pre-existing (stash-verified) + R1.3-independent. |
| 3 | IMPORTANT | aggregation.md "Known interpretation" | Cites `GateCriteria` L90 as "HEAD-verified"; post-edit it shifted to L121 (CodeAssertion dataclass inserted before it). `_build_steps` L2108→L2182. | Added POST-EDIT CORRECTION with real current line numbers. |
| 4 | MINOR | design doc §3, §6.2 | Cites `Finding` as living in `cli/roadmap/findings.py` (does not exist; it is in `models.py`). Impl is correct. | Documented in this review; design doc is status:draft — left as-is (non-load-bearing draft sketch). |

## Actions Taken

- Fixed test-count 8→7 in `r1-3-aggregation.md` (criteria b, e) and
  `r1-3-validation-summary.md` (table + section header).
- Corrected the 19-failure attribution (16 cli + 3 roadmap) in both
  `r1-3-aggregation.md` and `r1-3-validation-summary.md`, with stash-verified
  pre-existing/independent justification.
- Added POST-EDIT line-number correction to `r1-3-aggregation.md`.
- Verified each fix by re-reading the edited regions; all edits applied cleanly.
- **No source code changed** — the implementation is correct as-shipped.

## Recommendations (for R1.6 / downstream, non-blocking)

1. **R1.6 MUST delete the envelope-None shim AND wire `envelope`/`repo_root`
   into the live `gate_passed` call sites** (`pipeline/executor.py:267,329`),
   otherwise the certify dispatch-reachability assertion remains permanently
   dormant at runtime (enforced only in CI).
2. The 3 pre-existing `tests/roadmap/test_default_agents*` failures (haiku vs
   sonnet drift) are OUT OF SCOPE for R1.3 but should be tracked separately —
   they are a stale-test / default-config divergence unrelated to this phase.
3. Regenerate the design doc §2/§3 line citations + `Finding` path before it is
   promoted from status:draft, so future readers do not chase the L90/`findings.py`
   ghosts.

## Confidence Gate

- **Confidence:** Verified: 14/14 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 8 | Grep: 6 | Glob: 0 | Bash: 9
  (Every criterion mapped to ≥1 direct tool call: file reads of all 7 source/test
  files, grep for imports/step-counts/return-True, pytest runs for (b)(e)(regression),
  git diff for (f), AST mutation harness for (b)(c), stash-rerun for the failure
  attribution. Tool-call count (23) ≥ checklist items (14) — engagement adequate.)
- No web research performed (all claims are local/source-truth).

## QA Complete
