# QA Report — Task File Qualitative Review (operational-correctness)

**Topic:** TASK-RF-uc2-reachability-gate FR-RH1 UC-2 contracted-sink reachability gate
**Date:** 2026-06-20
**Phase:** task-qualitative
**Lens:** operational-correctness
**Fix cycle:** N/A
**fix_authorization:** false (report-only)

---

## Overall Verdict: PASS

The task file would execute correctly. Every operationally load-bearing claim — wrapper symbol
names, tmux inner-command builder name, recursion-guard env var, eval workspace layout
(`cases/` vs `evals/`), test file existence, docs-parity parser shape, dataclass field ordering,
contract version semantics, and R7 field names — was independently verified against actual source
and matches. The single highest-risk concern flagged in the spawn prompt (a wrong tmux
inner-command builder name) is NOT present: the item names the real symbol `_build_inner_command`.
The real-boot eval case is correctly marked conditional.

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run (`make sync-dev`/`verify-sync`, `uv run pytest`, POST wrapper) | none | PASS | All four pytest targets exist (test_cli_smoke.py, test_docs_cli_parity.py, test_promote_plumbing.py, test_verdict_mapping.py). `make` targets are standard per CLAUDE.md. POST wrapper command shape verified against Click flags. |
| 2 | Project convention compliance (src→.claude sync) | none | PASS | All edits target `src/superclaude/` (skills/cli/commands/docs/tests). Phase 6 item 212 runs sync-dev→verify-sync. `.claude/` non-staging enforced in Phase 6/7 items. |
| 3 | Intra-phase execution order | none | PASS | Phase 1 creates requirements-map → Phase 2 patches requirements → Phase 3 protocol → Phase 4 wrapper → Phase 5 tests → Phase 6 sync+QA → Phase 7 POST. No item reads an artifact a later item creates. |
| 4 | Function signature verification (ReflectConfig, resolve_config, run(), _build_prompt, _build_inner_command) | none | PASS | All symbols verified at real line locations; modifications compatible (see Source Verification). |
| 5 | Module context analysis (dataclass field ordering, negative-only prompt precedent) | none | PASS | ReflectConfig has zero defaulted fields → adding non-default `reachability: bool` is valid. `_build_prompt` `--no-promote` precedent at runner.py:346 is exact template for `--no-reachability`. |
| 6 | Downstream consumer analysis (docs-parity, help test, tmux) | none | PASS | Click flag-pair flows to `_cli_long_flags()` (both opts + secondary_opts) and `_SPEC9_FLAGS`; both consumers addressed by Phase 5 items. |
| 7 | Test validity (real fixtures + assertions, not stubs) | none | PASS | Fixtures use canonical R7 fields; plumbing tests assert `.split().count("--no-reachability")==1`; producer eval is a distinct falsifier fixture, not a consumer stub. |
| 8 | Test coverage of primary use case | none | PASS | Consumer contract tolerance, telemetry-only skips, advisory semantic fallback, proxy-oracle-unproven, and producer Step 5.6 emission all covered. |
| 9 | Error path coverage (skip telemetry, no false Regression) | none | PASS | Skip fixtures assert null ledger / zero counters / no needs_human_decision; falsifier asserts proxy/oracle evidence never greens Regression. |
| 10 | Runtime failure path trace (real-boot envelope, recursion) | none | PASS | §6.1.1 envelope strips marker via `env -u`; real-boot eval correctly conditional. POST shell-guard is harmless redundancy with built-in group-callback guard. |
| 11 | Completion scope honesty (patch requirements before impl) | none | PASS | Phase 2 mandates patching/amending merged-requirements before any source edit; Phase 2 verdict gate blocks Phase 3 on stale clauses. |
| 12 | Ambient dependency completeness | none | PASS | Click decorator + run() param + resolve_config call + ReflectConfig field + tmux forward + prompt branch + docs + help test + parity test all enumerated. |
| 13 | Kwarg sequencing red flags | none | PASS | Item 176 adds ReflectConfig field, 178 adds resolve_config param, 180 adds Click option+run() param — signature-before-use order is correct. |
| 14 | Function existence claims grep-verified | none | PASS | `_build_inner_command` (commands.py:279), `_build_prompt` (runner.py:341), `resolve_config` (config.py:123), `ReflectConfig` (models.py:58), recursion env (commands.py:44) all confirmed. |
| 15 | Cross-reference accuracy for templates/anchors | none | PASS | Step 5.5 exists (SKILL.md:474/490), `--no-verify` row exists (reflect.md flag table), contract 1.5.0=D13 confirmed (REPORT:101), R7 fields verbatim (REPORT:60-66). |

## Summary
- Checks passed: 15 / 15
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 0
- Issues fixed in-place: 0 (report-only)

## Source Verification (the spawn-prompt's explicit asks)

1. **`make sync-dev` / `make verify-sync` apply** — PASS. All implementation edits land under
   `src/superclaude/{skills,commands,cli}` and `docs/`/`tests/`; Phase 6 item 212 runs both make
   targets. `.claude/` staging is forbidden per Phase 6/7 items + CLAUDE.md.

2. **`uv run pytest` paths exist** — PASS. Verified on disk: `tests/cli/reflect/test_cli_smoke.py`,
   `test_docs_cli_parity.py`, `test_promote_plumbing.py`, `test_verdict_mapping.py` all present.
   Item 202's command lists exactly these four absolute paths.

3. **Wrapper plumbing names real symbols** — PASS.
   - `ReflectConfig` dataclass: models.py:58 (fields 66-86, no defaults → new `reachability: bool`
     valid anywhere without ordering hazard).
   - `resolve_config()`: config.py:123 (keyword-only signature; item adds `reachability: bool=True`
     and passes into `ReflectConfig(...)` at 220-240, mirroring the `promote`/`fix` pattern).
   - Click `run()`: commands.py:148 (option block 81-147; `--promote/--no-promote` default=True
     precedent at 90-94 is the exact template).
   - `_build_prompt()`: runner.py:341 (negative-only `--no-promote` branch at 346-347 is the
     insertion template — item 182 mirrors it exactly).

4. **tmux inner-command builder name** — PASS / NOT THE FEARED BUG. The spawn prompt asked me to
   flag if the item assumes a wrong name. The real function is `_build_inner_command(config)` at
   **commands.py:279**. Task item 180 AND research 03 both name it `_build_inner_command(config)`.
   They match the source. The promote-forwarding precedent inside it (line 299:
   `cmd.append("--promote" if config.promote else "--no-promote")`) is the template for forwarding
   disabled reachability.

5. **POST reflect wrapper shell-out** — PASS. Item 248 runs
   `superclaude reflect run <task-file> --depth deep --fix --promote` with a recursion guard on
   `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`. Verified: that env var is the real marker
   (commands.py:44, runner.py:53). `--fix` (commands.py:128) and `--promote` (commands.py:90) are
   valid flags. No `--base`, no `--reflect`, no `<base>..HEAD` range, no `/sc:task`, no agent-spawn
   directive — matches the required shape. The shell `if [...]=="1"` guard is **redundant** with the
   built-in group-callback breaker (commands.py:62-73) but harmless (belt-and-suspenders), and the
   group callback uses the identical `== "1"` truthiness rule, so semantics agree.

6. **Eval workspace path/manifest layout** — PASS. Verified: `.dev/eval-workspaces/sc-reflect/`
   contains `cases/` (case directories), `evals/evals.json` (manifest), and top-level `grader.py`.
   Items 200/204 reference exactly `evals/evals.json`, `grader.py`, and `cases/` — placement is
   correct (cases live under `cases/`, NOT under `evals/`).

7. **Real-boot eval case conditionality** — PASS. The §6.1.1 verification envelope (SKILL.md:508)
   runs scoped non-mutating commands and strips `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` via
   `env -u`; it cannot run a prod binary that re-enters the gate. The task respects this: item 200
   gates the real-boot case behind "and, **if implementable in the harness**,
   `uc2-reachability-real-boot-regression-proof`", and item 204 explicitly permits logging a
   harness limitation rather than fabricating a real-boot result. R8 bounds real boot to "cap 1"
   (REPORT). Correctly marked conditional/optional.

## Additional operational confirmations

- **Docs-parity silent-failure point cleared.** `_documented_flags()` (test_docs_cli_parity.py:69)
  collects every `--flag` on bullet lines matching `^\s*-\s+\`--`; `_cli_long_flags()` (line 36)
  collects `param.opts` + `param.secondary_opts`, so a `--reachability/--no-reachability` pair
  injects BOTH long flags into the CLI set. `test_documented_flags_match_cli_flags` asserts set
  equality. Item 184 correctly requires the bullet to contain both long flags and start with
  `- \`--`. Without both, the parity test fails — the item is written to satisfy it.
- **Boolean-default loop.** `test_documented_defaults_match_cli_defaults` iterates
  `("fix","promote")`; item 198/research require adding `reachability` so the guide must state
  `Default: \`--reachability\``. Matches the loop shape.
- **argument-hint hedge is correct.** reflect.md:10 argument-hint does NOT enumerate `--no-verify`,
  so item 174's "add to the argument hint **if flags are enumerated**" correctly results in a no-op
  for the hint, avoiding a spurious edit.
- **Contract semantics verbatim.** R7 fields (REPORT:60-66) and `1.6.0` additive / `1.5.0` D13-only
  (REPORT:21,91-101) match every task item that cites them.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` block was present in the spawn prompt; this was a standalone
  task-qualitative review. No structural reliance claimed — all structural facts were independently
  re-verified.

**(b) Independent semantic checks (≥1 required, INV-019):**
- tmux inner-command builder name — grep + Read confirmed `_build_inner_command` at
  commands.py:279 (tool: Bash grep + Read).
- Recursion-guard env var identity — grep confirmed `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` at
  commands.py:44 / runner.py:53 matches the POST item's shell guard (tool: Bash grep).
- Dataclass field-ordering hazard — Read models.py:58-86 confirmed zero defaulted fields, so a new
  non-default `reachability` field is safe (tool: Read).
- Eval layout cases-vs-evals — `find`/`ls` confirmed `cases/` holds cases and `evals/evals.json`
  is the manifest (tool: Bash).
- Docs-parity flag-pair handling — Read test_docs_cli_parity.py:36-80 confirmed both long flags of
  a Click pair must appear in the bullet (tool: Read).

### Self-Audit answers
1. **Factual claims independently verified against source:** ~25 (every wrapper symbol + line,
   recursion env var, 7 R7 field names, 2 contract versions, Step 5.5 anchor, 4 test-file
   existences, 6 ref-file existences, eval workspace layout, docs-parity parser, dataclass ordering).
2. **Files read to verify:** task file (full, 325 lines); research 03/04/06; commands.py, config.py,
   runner.py, models.py; test_promote_plumbing.py, test_docs_cli_parity.py; reflect.md (flag table);
   SKILL.md (anchors); canonical REPORT.md (grep); plus `ls`/`find`/`grep` over eval workspace,
   fixtures, and ref dirs.
3. **Why trust this with a PASS:** The verdict rests on grep/Read evidence at named line numbers,
   not on document self-assertion. The one symbol the spawn prompt specifically suspected
   (tmux inner-command builder) was checked first and found correct. Every operational seam where a
   silent failure could hide (docs-parity set equality, dataclass ordering, recursion env var,
   cases/-vs-evals/) was opened and inspected.
4. **Web research:** None performed — review was fully local-file-bound; no external lookup needed.

## Confidence
Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

## Tool engagement
Read: 8 | Grep: 4 | Glob: 0 | Bash: 4

## Recommendations
- None blocking. The task is execution-ready as written.
- (Non-gating observation, not a defect) The POST-wrapper shell `if [...]` recursion guard in item
  248 duplicates the wrapper's built-in group-callback breaker. It is harmless and arguably a
  defensive belt-and-suspenders; no change required.

## QA Complete

VERDICT: PASS
