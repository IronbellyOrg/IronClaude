# Research Notes: Implement merged-report-v2 §(d) — /sc:troubleshoot generalization refactor (R-01..R-19)

**Date:** 2026-09-19
**Scenario:** A (explicit — spec names every file, insertion line, and test)
**Depth Tier:** Deep (25 target files across skill / 7 refs / 2 agents / command / tests; cross-file consistency is the main risk)
**Track Count:** 1 (all changes are one coherent edit to a single skill; R-items cross-reference each other by number)
**Status:** Complete

**SPEC_PATH:** `/config/workspace/Coder/.claude/worktrees/gh-automation-orca-run/.dev/research/sysbox-retrospective-20260918/merged-report-v2.md` §(d) lines ~148-660 (R-01..R-19 + rescore table)
**CROSS-ITEM DECISIONS:** `.../sysbox-retrospective-20260918/spec-panel-critique.md` (36 findings; 2 CRITICAL fixes already folded into v2; 14 dangling refs resolved)
**CLI_MODE:** false (default skill-mode POST gate)

---

## EXISTING_FILES

All under `/config/workspace/IronClaude/` (source of truth is `src/superclaude/`; `.claude/` is `make sync-dev` output, gitignored, never staged).

**Skill:**
- `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` — 602 lines. Wave map `:93-108`; Wave 1 `:156-175`; Wave 1.6 `:217-270` (S1.6.0 `:230`, hard-stop `:241`, counter `:248`); Wave 1.7 `:272-288`; Wave 3 `:312-373` (`:333-336` MCP enrichment, `:337-343` prompt contents, `:346` cluster-by-fix, `:372` converge-skip); Wave 4 `:377-402` (`:381` precondition); Wave 4.5 `:406-422` (`:410` trigger, `:414` H0); Wave 5 `:426-481` (`:439` Evidence bullet, `:450` last compose bullet, `:451-452` validator); Will Not `:532-545`; cost profile `:572-582`; Refs table `:584-602`.

**Refs (7 to edit, 1 to create):**
- `refs/triage-checklist.md` — 65 lines; cause-class table `:20-34` (Build/packaging row at `:33`); evidence-or-drop `:36-44`; refuse-Tier-1 `:56-65`. R-15 adds one row + one bullet + one refuse clause.
- `refs/diagnosability-audit.md` — 340 lines; S1-S13 rubric `:134-150`; complexity signals `:169-177`; hard constraints `:242-247`. R-03 adds S14 + task type 5 + emitter-search; R-06 adds falsifier columns; R-15 adds complexity signal.
- `refs/hypothesis-card-template.md` — 154 lines; claim classes `:16-22`; "If I'm wrong" `:76-78`; Falsification standard `:80-82`; filling rule `:91`. R-07 replaces `:80-82` with the discriminator form; adds `runs-in=` field (R-01) and `behaviour-definition: row N` (R-09).
- `refs/escalation-rubric.md` — 90 lines; formula `:20`; rules `:52-72` (`:63-69` ordered list). R-08 adds one rule.
- `refs/hardening-output-contract.md` — 71 lines; enum `:5,:15`; latch `:66-71` (`:68`). R-16 adds `blocked-on-authorization`.
- `refs/report-template.md` — 319 lines; hard-stop variant `:170-206`; rendering rules `:255-260`. R-10 Diagnosis-section rule; R-13 timestamp rule.
- `refs/calibrator-eval-cases.md` — 81 lines; `:81` names `tests/troubleshoot/test_calibrator_eval_cases.py` as the landing path (R-19 non-regression test 12 keeps fixtures 1-9 unchanged).
- **NEW** `refs/primitive-differential.md` — R-05 owns the six-kind probe-form table (read/parse, call/return, lookup, reach, permission, timing × exact/reference/control) + threshold-bracketing rule; optional example packs live under it.

**Agents:**
- `src/superclaude/agents/confidence-calibrator.md` — 141 lines; frontmatter `:5-8` (`tools: Read`, sonnet, 25 turns, plan); inputs `:45-51`; step 5a at `:62`; Stage-2 trace `:88-96`; Notes `:111-115`; Will-Not `:127-134`. R-14 adds C1-C8 as step 5b, `structural_flags` trace row, `card_mtime` input.
- `src/superclaude/agents/evidence-validator.md` — 128 lines; frontmatter `:5-8` (Read/Grep/Glob, no Bash `:58`); inputs `:41-44`; responsibilities `:51-58`; output `:63-97`; status `:99-103`. R-14 adds A1-A10 as responsibility 2b + `## Structural assertions` output table + inputs `calibration_paths`, `diff_path`, `artifact_paths`.
- `src/superclaude/agents/root-cause-analyst.md` — 56 lines; no frontmatter tools/model. Not edited by spec (R-02 producers table is pasted into its brief by SKILL, not by editing the agent).

**Command:**
- `src/superclaude/commands/troubleshoot.md` — 204 lines; `:8` argument-hint; `:46-60` options; `:69` on-return list; `:103` Bash bullet. R-18 winner B: one generic sentence at `:69` + one at `:103`; NO new flag.

**Tests:**
- `tests/troubleshoot/` exists: `test_hardening_h0..h4.py`, `test_hardening_output_contract.py`, `test_hardening_verdict.py`, `backtest/`, `e2e-backtest-scenarios.md`. Pattern: content-assertion tests over the source-of-truth markdown (`REPO_ROOT / "src" / "superclaude" / ...`, `read_text`, `assert token in low`). R-19 lands 19 generic property tests + 1 parametrized regression at `tests/troubleshoot/`, fixtures at `tests/troubleshoot/fixtures/{io,nonio,regression-sysbox}/`.
- `tests/troubleshoot/test_calibrator_eval_cases.py` — does NOT exist yet (deferred per `refs/calibrator-eval-cases.md:81`); R-19 test 12 is a non-regression over fixtures 1-9.

**Sync:** `Makefile:109 sync-dev` copies `src/superclaude/skills/*` → `.claude/skills/`, agents likewise; `Makefile:166 verify-sync`. `.claude/` is gitignored except `settings.json`; pre-commit only blocks staging `.claude/` mirrors (does NOT run verify-sync); CI quick-check runs verify-sync.

**Template:** `.claude/templates/workflow/02_mdtm_template_complex_task.md` (also at `src/superclaude/templates/workflow/`).

## PATTERNS_AND_CONVENTIONS

- SKILL.md waves are `### Wave N — Title` blocks separated by `---`; each ends with an exit-criteria "Emit:" line and a token target; refs are lazy-loaded per wave (`SKILL:602`).
- Refs use numbered bullets + tables; ref-local footer "Loaded by Wave N only" (`refs/diagnosability-audit.md:338-340`).
- Agents: YAML frontmatter (`name, description, tools, model, maxTurns, permissionMode`) then `## Inputs`, `## Process`, `## Output`, `## Will Not`. Read-only agents never get Bash (validator `:58` explicit).
- Tests: pytest, content assertions over markdown; `from __future__ import annotations`; `REPO_ROOT = Path(__file__).resolve().parents[2]`; one concern per test function; docstring cites the FR/AC.
- UV only: `uv run pytest tests/troubleshoot/ -v`.
- Git: feature branch from master (`feature/troubleshoot-generalize`); never commit to master; PR target fork `IronbellyOrg/IronClaude` with `--repo`.
- Never stage `.claude/*` except `settings.json`.

## GAPS_AND_QUESTIONS

- G1: The v2 spec's SKILL.md insertion lines were computed against the 602-line baseline. Inserting R-01 (Wave 1) shifts every later line. The task file must sequence edits **bottom-up** (Wave 5 → Wave 3 → Wave 1.7 → 1.6 → 1) or anchor on text, not line numbers. Researcher must verify each anchor sentence still exists verbatim.
- G2: `hypothesis-card-template.md` is edited by three R-items (R-01 `runs-in=`, R-07 form, R-09 `behaviour-definition`); need a single merged edit plan to avoid conflicting Edits.
- G3: `diagnosability-audit.md` is edited by R-03, R-06, R-15; same.
- G4: Test fixture shape for the property tests — the spec says "synthetic minimal fixtures (5-10 line markdown/shell per assertion, io/ and nonio/ domains, pos+neg)". The exact fixture content per test is NOT in the spec; the task must author them. Researcher should extract the assertion text per validator/calibrator rule (A1-A10, C1-C8) from v2 R-14 so each fixture is derivable.
- G5: Does anything else in the repo consume `pipeline_hardening_verdict` enum (R-16 adds a fifth value)? `tests/troubleshoot/test_hardening_output_contract.py` and `test_hardening_verdict.py` likely assert the 4-token enum — they will need updating or the change breaks them.
- G6: R-17 renames H0-H5 → HC0-HC5 in SKILL + refs but keeps output-contract field names; `tests/troubleshoot/test_hardening_h0..h4.py` grep for `H0`/`h0` tokens — likely break. Must be enumerated.
- G7: `.claude/skills/sc-troubleshoot-protocol/` mirror — after edits run `make sync-dev && make verify-sync`; confirm no drift before the change (verify-sync currently passes on master? unknown).

## RECOMMENDED_OUTPUTS

Research files in `${TASK_DIR}research/`:
- `01-file-inventory.md` — SKILL.md + 7 refs + 2 agents + command: every anchor line the spec cites, verified verbatim, with the R-items that touch each file (resolves G1-G3).
- `02-patterns-conventions.md` — wave block shape, ref footer pattern, agent frontmatter shape, test file shape, sync/branch rules.
- `03-spec-extraction.md` — per R-item (01..19): change / layer / anchor text / exact insertion content (quoted from v2) / must-NOT / tests that cover it; plus the critique's resolutions that constrain wording (X-01..X-12, AD-01..05, GB-*). Doc-cross-validator style: tag each anchor [CODE-VERIFIED]/[CODE-CONTRADICTED].
- `04-test-verification.md` — existing `tests/troubleshoot/*` content, what they assert about H0-H5 / verdict enum (G5, G6); pytest conventions; a fixture design per R-19 test (path, minimal content, pos/neg expectation) resolving G4.
- `05-integration-points.md` — cross-file dependencies: which SKILL sentences reference which ref sections; which agent inputs the SKILL passes; command ↔ skill return contract; sync-dev mechanics; any other repo consumer of the edited refs (grep).
- `06-template-examples.md` — MDTM template 02 PART 1 rules (A3, A4, B2, L1-L6, M3/M4/I19-I22), and a prior TASK-RF-troubleshoot-hardening task file as a shape example.

## SUGGESTED_PHASES

Six researchers, all parallel:
1. File Inventory — scope: SKILL.md, refs/*.md, the 2 agents, commands/troubleshoot.md; output `01-file-inventory.md`. Others cover: patterns (2), spec mapping (3), tests (4), integration (5), template (6).
2. Patterns & Conventions — scope: 3 refs + 2 agents + 2 existing tests + CLAUDE.md git/sync rules; output `02-patterns-conventions.md`.
3. Spec Extraction / Doc Cross-Validator — scope: merged-report-v2.md §(d) + spec-panel-critique.md; verify each anchor against the repo; output `03-spec-extraction.md`.
4. Test & Verification — scope: tests/troubleshoot/, tests/conftest.py, refs/calibrator-eval-cases.md, v2 R-14 + R-19; output `04-test-verification.md`.
5. Integration Points — scope: grep for every ref filename / H0-H5 / verdict enum / `execution_locus` etc. across src/, tests/, docs/; Makefile sync targets; output `05-integration-points.md`.
6. Template & Examples — scope: templates/workflow/02, one prior TASK-RF-troubleshoot-hardening task file; output `06-template-examples.md`.

## TEMPLATE_NOTES

Template 02 (complex): discovery (anchor verification) → build (bottom-up edits across 11 files) → tests (author 20 test files + fixtures) → validation (`uv run pytest`, `make sync-dev`, `make verify-sync`, `make lint`) → QA gate (M3 lens sequence, ≥6 agents, fidelity gate per I21 since spec→implementation transformation) → reflect POST (skill mode) → done. Tier Deep because 25 files, cross-file consistency, and two known breakage surfaces (G5, G6).

## AMBIGUITIES_FOR_USER

- A1: R-17 (HC0-HC5 rename) will break existing `test_hardening_h*.py` unless they are updated in the same task. Spec says "output-contract field names unchanged"; the tests assert ref *text*. Default: update tests to the new names in the same PR (they are content-assertion tests over the refs being renamed). Flag in Open Questions.
- A2: Fixture authoring for 19 property tests is design work not fully specified by v2 (which gives the assertion, not the fixture bytes). Default: task items author minimal fixtures per the R-14 assertion text; the sysbox regression fixtures are vendored byte copies from the Coder worktrees with sha256 in a MANIFEST.
