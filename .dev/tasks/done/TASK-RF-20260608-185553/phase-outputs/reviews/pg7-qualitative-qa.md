# QA Report — Task-Qualitative (PG7, Operational/Spec-Intent)

**Topic:** `superclaude reflect run` thin CLI wrapper for the POST reflect gate
**Date:** 2026-06-09
**Phase:** task-qualitative (final operational gate)
**Fix cycle:** N/A (initial pass; fix_authorization: true)
**Document type:** Executed Task File — evaluated against actual outputs on disk
**Reviewer stance:** Adversarial (assume errors exist)

---

## Overall Verdict: PASS (with 2 fixes applied in-place)

The wrapper genuinely implements the central thesis — "a gate consumer must never
accept a silently degraded Tier-2 audit." The FR-11 degradation routing catches every
chain-critical loss the prompt named; the fail-closed posture is real (only a clean,
full, non-degraded, durably-written T2 pass exits 0); and the wrapper is genuinely thin
(no reflect-logic reimplementation). Two findings were identified and fixed in-place
(both in `tests/cli/reflect/*`): a missing end-to-end test for the load-bearing
FR-6 write-back-stale → BLOCKED downgrade (which a code comment falsely claimed was
covered), and the now-stale comment itself. After fixes: 35/35 tests pass, ruff
check + format clean.

---

## Items Reviewed (15-item task-qualitative checklist)

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | none | PASS | `superclaude reflect run` registered in `main.py:438`; `_build_prompt` emits only real reflect flags (research 08 §1.1 confirms all 8); wrapper flags (`--timeout`/`--allow-single-vendor`/`--dry-run`) correctly kept OUT of the slash prompt (research 08 §8.3). `--no-promote` is a hard prompt flag (FR-9) at runner.py:328-329. |
| 2 | Project-convention compliance | none | PASS | Edits confined to `src/superclaude/cli/reflect/*` + `tests/cli/reflect/*`; no `.claude/` touch. `ruff check` + `ruff format --check` both clean (CI runs them separately per CLAUDE.md). UV used for all test runs. |
| 3 | Intra-phase execution simulation | none | PASS | runner.run() ordering traced: preflight(no ClaudeProcess) → prompt → dry-run gate → env alias count → blocker→blocked → resume short-circuit → launch → parse → derive → write-back → sidecar. No step consumes a later step's output. |
| 4 | Function-signature verification | none | PASS | `ClaudeProcess.__init__` (process.py:37-54) is keyword-only and accepts every kwarg the runner passes (`prompt`, `output_file`, `error_file`, `model`, `timeout_seconds`, `max_turns`, `output_format`, `env_vars`). `build_env()` exists, is side-effect-free, pops `CLAUDECODE`/`CLAUDE_CODE_ENTRYPOINT`, preserves `ANTHROPIC_DEFAULT_*` (process.py:98-112) — matches FR-10. |
| 5 | Module-context analysis | none | PASS | `_IndentDumper` (yamllint indent-sequences), `_FRONTMATTER_RE`, `_REFLECT_POST_KEY_RE`, `_MODEL_ALIAS_ENV_VARS` all consistent across runner write-back, resume read, and sidecar. `contract.py` is a pure module (stdlib + PyYAML + `.models` only) as documented. |
| 6 | Downstream-consumer analysis | none | PASS | Dual gate signal verified: exit code (`Verdict.exit_code` 0/10/11/2) + `reflect_post` block + `wrapper-result.yaml` sidecar. SKILL.md wrapper arm (L2021-2027) gates Done on exit code AND `reflect_post.verdict == pass` (rule #19, L2137). Sidecar always written, even on unwritable frontmatter. |
| 7 | Test validity | weakened-criteria | FAIL→FIXED | e2e tests drive the REAL runner with a fixture-writing `.wait()` stub (not vacuous) and assert verdict + exit_code + written-back frontmatter. BUT the load-bearing FR-6 stale→BLOCKED downgrade (runner.py:465-467) had ZERO coverage while test_writeback.py:135 falsely claimed "verified in e2e tests." Fixed: added 2 e2e tests + corrected comment. |
| 8 | Test coverage of primary use case | none | PASS | Verdict matrix (pass/halted/degraded/blocked/timeout/unknown-major/single-vendor±flag/verification-exempt/benign-token/extrapolated-citations) all covered; e2e covers full launch→writeback for pass/halted/degraded/blocked; G1 max_turns + G2 resume both/clean+stale covered. Post-fix the FR-6 fail-closed downgrade is covered too. |
| 9 | Error-path coverage | none | PASS | `blocked` slugs: timeout(124), child-crash, contract-missing, contract-version-missing, unknown-major, malformed-degraded-components, claude-binary-missing, tasklist-missing, base/head-unresolved, `--output`-under-`.claude` (config.py:199-203). Malformed `degraded_components` → blocked (not silent). |
| 10 | Runtime-failure-path trace | none | PASS | Traced every exit-0 path: (a) genuine pass requires status==success AND tier_reached==expected AND no degraded/halted trigger AND write_status=="written"; (b) dry-run/print-command return PASS but never launch and are excluded from sentinel write; (c) resume short-circuit trusts a PRIOR fail-closed `verdict==pass`+matching HEAD. No degraded audit can reach exit 0. The stale/unwritable write-back downgrades PASS→BLOCKED (verified post-fix). |
| 11 | Completion-scope honesty | contradictions | FAIL→FIXED | test_writeback.py:135 comment asserted the runner stale-downgrade was "verified in e2e tests" when no such test existed — a claim contradicting the actual test suite. Fixed by adding the tests AND correcting the comment to point at the real test name. |
| 12 | Ambient-dependency completeness | none | PASS | `__init__.py` exports `reflect_group` + all public symbols; `main.py:436-438` registers the command (deferred import, documented). Help text exposes all 10 spec §9 flags (test_cli_smoke asserts). Verdict→exit_code centralized in `models.Verdict` (never hardcoded twice). |
| 13 | Kwarg sequencing | none | PASS | No "add kwarg before add parameter" pattern. `max_turns` is threaded explicitly (G1) and `ClaudeProcess` already declares it (process.py:43). Resume-read/write-back share the same regex helpers in dependency order. |
| 14 | Function-existence-claims verification | none | PASS | grep-verified: `ClaudeProcess.build_env` exists (process.py:98); `extract_frontmatter` exists (imported config.py:22) and is deliberately NOT used for write-back (drops nested mapping) — claim accurate; `reflect_group` registered. No phantom references. |
| 15 | Template cross-references | none | PASS | SKILL.md `POST_REFLECT_MODE: wrapper` arm exists (L2021), is a Bash shell-out (`superclaude reflect run {TASK_FILE} --depth {DEPTH}`), contains no Agent/Task nesting tokens (NFR-7), and the Done item gates on exit code + verdict==pass. no-nesting guard test (Layer A) enforces this against the SOURCE skill. |

---

## Summary
- Checks passed: 15 / 15 (2 after in-place fix)
- Checks failed (pre-fix): 2 (items 7, 11 — same root cause: untested fail-closed downgrade + false coverage claim)
- Critical issues: 0
- Issues fixed in-place: 2
- Tests: 35 passed (was 33; +2 new e2e fail-closed downgrade tests)
- Lint/format: ruff check clean, ruff format clean

## Central-thesis operational validation (spec §1, §11)

1. **FR-11 degradation routing genuinely catches chain-critical losses** — traced the
   actual predicates in `contract._degraded_reason`:
   - single-vendor "Tier 2" → `single-vendor` degraded (unless `--allow-single-vendor`) ✓ (trigger 8, test covers both flag states)
   - expected-T2-but-ran-T1 → `degraded-tier1` ✓ (trigger 6, precedes the halted tier-mismatch fallback, so it wins correctly)
   - `t2_model_class_diversity != full` → `degraded-model-diversity` ✓ (trigger 7, guarded so T1-null does not misfire)
   - null adversarial convergence at T2 → `null-convergence` ✓ (trigger 11, guarded on `tier_reached == 2`)
   - benign telemetry token (`search_deps:lsp_unindexed`, `serena:onboarding-parse`) does NOT over-HALT ✓ (EXACT frozenset membership, not substring; test_benign_degraded_component_does_not_over_halt)
   - `serena_summary_corroboration: unavailable` correctly NOT a halt (cross-session expected, research 02 §2.2 / spec FM-13) ✓

2. **Fail-closed posture is REAL** — every exit-0 branch traced (genuine pass,
   dry-run/print, resume short-circuit, write-back). The write-back-stale and
   frontmatter-missing cases downgrade a derived PASS to BLOCKED (runner.py:465-467),
   now test-covered. No degraded/halted/blocked path can leak as a green gate.
   Ordering is exact: blocked → degraded → halted → pass (first-match-wins).

3. **Wrapper is genuinely THIN (NFR-1)** — no deviation-taxonomy / tier-rubric /
   promotion-gate logic reimplemented in Python. The wrapper reads contract fields
   for routing + write-back only; it never parses diff hunks or classifies deviations.
   `contract.py` carries only contract field names, no reflect reasoning.

4. **Fixtures are semantically valid §9.1-shaped contracts** — field names
   (`report_path`, `deviation_count_by_class`, `t2_model_class_diversity`,
   `t2_vendor_diversity`, `merge_method`, `adversarial_convergence_score`,
   `verification_ran`, `verification_skip_reason`, `citations_dropped`,
   `input_drift_detected`, `degraded_components`) all match research 02's authoritative
   §9.1 catalog. `contract_version: "1.3.0"` quoted-string matches research 02 TL;DR.
   The G2 resume and G1 max_turns e2e tests genuinely exercise behavior (resume:
   `mock_cls.assert_not_called()` on clean head, `assert_called_once()` on stale;
   G1: asserts `call_args.kwargs["max_turns"] == 250`).

## Issues Found
| # | Severity | Location | Issue | Required Fix | Status |
|---|----------|----------|-------|--------------|--------|
| 1 | IMPORTANT | tests/cli/reflect/ (missing) | The FR-6 write-back-stale → BLOCKED downgrade (runner.py:465-467) — the load-bearing race-safe fail-closed defense, directly the "degraded audit leaks green" scenario the central thesis guards against — had zero test coverage. | Add e2e tests patching `write_reflect_post` to return `frontmatter-stale` / `frontmatter-missing` and assert PASS contract downgrades to BLOCKED/exit 2. | FIXED |
| 2 | MINOR | test_writeback.py:135 | Comment claimed the stale downgrade was "verified in e2e tests" — false; no such test existed (completion-scope dishonesty). | Add the test (issue 1) and repoint the comment to the real test name. | FIXED |

## Observations (NOT defects — documented for the record)
- **`expected_tier = 2` for `--depth standard`** (runner.py:354): research 08 §3 notes
  `standard` means "T1, escalate by rubric," so a genuinely simple task at standard depth
  could legitimately resolve to T1 and then route `degraded`. This is the INTENDED
  fail-closed behavior for the POST gate (research 08 §4 L84 explicitly: "for a post gate
  that EXPECTS T2... 0-1 aliases → tier_reached==1 → degraded") — the builder only emits
  the wrapper arm for medium/complex (depth ≥ standard) tasklists. Correct, not a bug.
- **`_claude_argv_preview`** (runner.py:341-347) is a hand-rolled dry-run string that
  diverges cosmetically from the actual `ClaudeProcess.build_command()` (omits
  `--no-session-persistence`, `--tools default`, differs in ordering). Preview-only,
  never executed — illustrative not authoritative. MINOR, not flagged as a defect.

## Actions Taken
- Added `test_e2e_frontmatter_stale_downgrades_pass_to_blocked` to test_runner_e2e.py — drives the real runner with a clean `pass.yaml` contract, patches `write_reflect_post` → `"frontmatter-stale"`, asserts verdict BLOCKED / exit 2 / reason `frontmatter-stale`.
- Added `test_e2e_frontmatter_missing_downgrades_pass_to_blocked` — same for the `frontmatter-missing` write status.
- Corrected the misleading comment in test_writeback.py:135 to reference the now-real e2e test.
- Verified fixes: `uv run pytest tests/cli/reflect/` → 35 passed; `ruff check` + `ruff format --check` clean on both modified files.

## Self-Audit
**Factual claims independently verified against source code:** 12+ — ClaudeProcess
signature + build_env (process.py read), main.py registration (grep), SKILL.md wrapper
arm + Done-gate rule (grep), fixture field names vs research 02 catalog (cat + cross-ref),
all 14 FR-11 predicates in contract.py (read), every exit-0 branch in runner.run (read),
the absent stale-downgrade e2e test (grep -n confirming only the unrelated resume-stale
test existed), the false coverage comment (read).

**Files read to verify:** contract.py, runner.py, config.py, commands.py, models.py,
__init__.py, all 5 test files, conftest.py, all 7 fixtures, pipeline/process.py,
SKILL.md (wrapper arm region), research 02 + 08, merged-requirements.md.

**Why trust the 0-CRITICAL verdict:** I did not start from "it looks fine." I traced
every exit-0 path looking for a degraded-leak (the named falsifier), found the
untested fail-closed downgrade, confirmed via grep that a code comment lied about
covering it, and closed the gap with tests that genuinely fail if the downgrade is
removed. The degradation predicates were checked one-by-one against research 08's
14-row routing table, not sampled.

**Web research:** none performed (review was entirely local-file + source-bound).
Tavily-first rule therefore not triggered.

## Recommendations
- None blocking. The 2 fixes are applied and verified. Ready to proceed.
- Optional (not gating): consider deleting/regenerating `_claude_argv_preview` to render
  from `ClaudeProcess.build_command()` so the dry-run preview cannot drift from the real
  argv. Cosmetic only.

## QA Complete
