---
Status: Complete
---

# Research Notes: cliEval Post-Sprint Remediation (H1-H5 + M1-M6 + CC1-CC3)

**Date:** 2026-05-22
**Scenario:** A (explicit — full remediation spec already produced with file:line citations + acceptance criteria + 8-phase implementation order)
**Depth Tier:** Standard (4 researchers)
**Track Count:** 1 (single cohesive remediation against one module)

---

## EXISTING_FILES

### Source — `src/superclaude/cli/eval/` (edit targets)

- `commands.py` — `eval_run` Click entry + 11 helpers; anchors H1/H3/H5, M1/M2/M3/M6
- `coverage.py` — `coverage_gate`; H2 anchor (corrupt settings.json silent-green)
- `config.py` — `resolve_scratch_root`; H4 anchor (bare-prefix foot-gun)
- `artifact_layout.py` — `compose_run_dir` + `_EVAL_ID_RE`; H1 reach + CC1 anchor
- `reporter.py` — `write` / artifact emission; M4 anchor (artifact-set divergence)
- `run_report.py` — `write_aggregated_report`; M4 second anchor
- `isolation.py` — AC12 allowlist machinery; H5 reach
- `loader.py` — `validate_eval_id`; CC1 reach (FR-SCH2 regex duplicated)
- **NEW** `exit_codes.py` — CC2 consolidation target (does not yet exist)

### Tests — `tests/cli/eval/` (test-pattern source-of-truth)

- 75 existing test files, including: `test_eval_run.py`, `test_coverage_gate.py`, `test_coverage_gate_integration.py`, `test_config.py`, `test_artifact_layout.py`, `test_eval_id_regex.py`, `test_exit_codes.py`, `test_home_isolation.py`, `test_home_isolation_extend.py`, `test_eval_lifecycle.py`, `test_orchestrator.py`, `test_ban_import_rule.py`, `test_containment.py`
- Existing `test_eval_id_regex.py` and `test_exit_codes.py` are direct precedents for T8 (CC1) and T9 (CC2)
- `test_config.py` is the home for the H4 invert (`test_accepts_tmp_eval_runs_root_itself` lives here per spec §3.H4)

### Reference docs

- `.dev/reviews/snapshot-src-superclaude-cli-eval-20260522142818/REVIEW.md` — source review
- `.dev/reviews/snapshot-src-superclaude-cli-eval-20260522142818/remediation-spec.md` — authoritative spec
- `.dev/reviews/snapshot-src-superclaude-cli-eval-20260522142818/claude-side-review.md` — independent grounding evidence

## PATTERNS_AND_CONVENTIONS

(researchers fill — preliminary observations from prior validation pass:)

- Test naming: `test_<unit>_<scenario>.py`; one assertion-focus per test function
- Click options use `path_type=Path`; `eval run` vs `eval doctor` known to be inconsistent (M6)
- `_EVAL_ID_RE` lives at `artifact_layout.py:99`; duplicate in `loader.validate_eval_id`
- Exit code `2` appears 7+ times as magic literal (CC2)
- Reporter imports: stdlib + yaml + `.models` + `.run_report` only (FR-G1 already clean — verified during review)

## GAPS_AND_QUESTIONS

- Exact existing fixtures available for `corrupt settings.json` test (T3) — researcher to map
- Whether `EVAL_STATUSES` is currently a single enum / set / list constant — researcher to confirm and report the import path the builder should use (impacts H3 + M3 fix)
- The current location of the 7 magic `2` literals for CC2 consolidation — exact file:line list
- Existing precedent for `WARNING`-level log emission from `commands.py` helpers (does eval module use `logging`, `click.echo`, or both?) — impacts M2 implementation choice
- Whether `compose_run_dir` already supports being called twice idempotently (impacts H1 implementation — does it need to short-circuit on already-composed paths?)

## RECOMMENDED_OUTPUTS

| # | Topic | Output File |
|---|-------|-------------|
| 01 | File Inventory + helper/exports map for the 9 source files | `research/01-file-inventory.md` |
| 02 | Patterns & Conventions — test naming, fixture style, Click option style, logging style | `research/02-patterns-conventions.md` |
| 03 | Integration Points — exit-code call sites (CC2), `_EVAL_ID_RE` call sites (CC1), `EVAL_STATUSES` consumers (H3/M3), allowlist call graph (H5) | `research/03-integration-points.md` |
| 04 | Template & Examples — MDTM template 02 study + existing cliEval task-folder examples (P1-P4 patterns) | `research/04-template-examples.md` |

## SUGGESTED_PHASES

- **Researcher 1 (File Inventory)** — `src/superclaude/cli/eval/{commands,coverage,config,artifact_layout,reporter,run_report,isolation,loader}.py` — for each file: purpose, key exports relevant to the remediation, the *current* line numbers of the symbols cited in remediation-spec.md §3 (H1: 1710-1714/1853/1918, H2: 294-302, H3: 1526-1539, H4: 243-249, H5: 1735-1746), `compose_run_dir` signature, `coverage_gate` signature, `resolve_scratch_root` signature. **Other researchers cover:** patterns (R2), integration call graph (R3), templates (R4).

- **Researcher 2 (Patterns & Conventions)** — read `tests/cli/eval/test_eval_run.py`, `test_coverage_gate.py`, `test_config.py`, `test_home_isolation.py`, `test_artifact_layout.py`, `test_eval_id_regex.py`, `test_exit_codes.py`, `conftest.py` — extract: pytest fixture style (tmp_path, monkeypatch usage), assertion idioms, parametrize patterns, mock/patch conventions, file-creation helpers. Also read 3-5 helpers from `commands.py` to extract logging / `click.echo` convention. **Other researchers cover:** file inventory (R1), call graphs (R3), templates (R4).

- **Researcher 3 (Integration Points)** — produce four maps:
  1. **CC2 — magic `2` literals:** `grep -rn "exit(2)\|Exit(2)\|return 2" src/superclaude/cli/eval/` — list every occurrence with file:line + 3-line context
  2. **CC1 — `_EVAL_ID_RE` / FR-SCH2 regex:** `grep -rn "_EVAL_ID_RE\|EVAL_ID_PATTERN\|re\.compile.*eval" src/superclaude/cli/eval/` — list call sites
  3. **H3 / M3 — `EVAL_STATUSES`:** locate the definition; `grep -rn "EVAL_STATUSES" src/superclaude/cli/eval/` — every consumer
  4. **H5 — allowlist call graph:** trace `commands.py:1735-1746` `home_root.mkdir` callers and downstream consumers; identify `resolve_scratch_root` signature and how to thread `allowlist + [home_root]`
   **Other researchers cover:** file inventory (R1), patterns (R2), templates (R4).

- **Researcher 4 (Template & Examples)** — read `.claude/templates/workflow/02_mdtm_template_complex_task.md` PART 1 fully (rules A3, A4, B2, L1-L6); read `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P*` folders' task files — extract patterns proven on this exact module: phase decomposition for cliEval, test-first ordering, verification gate format, hand-off blocks. **Other researchers cover:** file inventory (R1), patterns (R2), call graphs (R3).

## TEMPLATE_NOTES

- **Template selection:** **02** (Complex Task) — implementation requires phased ordering with quality gates, conditional fix loops, and verification after each phase per spec §8/§9
- **Tier:** Standard — 9 source files touched + 9 new tests; not multi-track; well-scoped
- **MDTM features the generated task file should use:**
  - Per-file granular items (no batch "fix all Highs in one item") per A3
  - Test-first ordering: T3, T5, T6 items appear BEFORE their source-change items (spec §8 Phase 1)
  - Verification clause on every item: `Verify: <make/uv command> exits 0 + grep gate passes`
  - Each spec acceptance criterion (§3.H#/§3.M#) becomes a Completion gate on the corresponding item
  - Use the `## Execution Context` block: ≥3 source areas (commands.py, coverage.py, config.py, artifact_layout.py, exit_codes.py, …) so AUTO emission applies
- **Required QA gate cadence:** `QA_GATE_REQUIREMENTS: PER_PHASE` — each phase ends with a gate item that runs `make verify-sync && uv run pytest tests/cli/eval/ && uv run ruff check --select F401,F821 src/superclaude/cli/eval/`

## AMBIGUITIES_FOR_USER

None — intent is fully specified by the remediation-spec.md (§3 per-finding contracts + §6 test list + §8 implementation order + §10 exit criteria). Builder proceeds with spec as authoritative.
