# Research Notes: Implement `sc:submit-pr` PR Review Auto-Remediation Monitor (V1.0)

**Date:** 2026-06-11
**Scenario:** A (Explicit — driven by a comprehensive 1085-line adversarial-merged spec)
**Depth Tier:** Deep (20+ files across skills/commands/hooks/scripts/tests; multi-subsystem; new skill package)
**Track Count:** 1 (single cohesive feature; all components build one deliverable on a dependency DAG)
**Spec Path:** `/config/workspace/IronClaude/.dev/brainstorms/20260610-234750-pr-review-auto-remediation/merged-spec.md`

---

## EXISTING_FILES

Confirmed during orchestrator scope discovery (paths relative to repo root `/config/workspace/IronClaude/`):

- **Reuse — C3 severity rubric:** `src/superclaude/skills/sc-auggie-review-protocol/refs/severity-rubric.md` (the rubric the spec's C3 `severity-routing.md` defers to; FR-3.1 re-grade).
- **Reuse — C3a grounding discipline:** `src/superclaude/skills/sc-auggie-review-protocol/` (SKILL.md, refs/auggie-prompts.md, refs/remediation-handoff.md) — grounding/verification pass to mirror for verify-before-remediate.
- **Reuse — C3b dispatch + adversarial discipline:** `src/superclaude/skills/sc-troubleshoot-protocol/` (SKILL.md + refs/: escalation-rubric.md, remediation-handoff.md, hypothesis-card-template.md, triage-checklist.md, report-template.md, calibrator-eval-cases.md, diagnosability-audit.md, doc-discovery.md). The `/sc:troubleshoot` invocation contract C3b seeds.
- **Edit — C5 hook:** `src/superclaude/hooks/scripts/offer-pr-review.sh` (FULL content read). Fail-open PostToolUse(Bash) hook that fires after `gh pr create`, prints a `<sc-auggie-review-offer>` block. FR-7.1 adds an `sc:submit-pr --monitor` mention. Other hooks in `src/superclaude/hooks/scripts/` (freshness-*.sh, reject-workspace-writes.sh, sc-recommend-phase0.sh) show hook conventions.
- **Command registration target:** `src/superclaude/commands/` (43 `.md` command files; `troubleshoot.md` frontmatter read — `name/description/category/complexity/mcp-servers/personas/argument-hint` + `## Triggers` / `## Required Input` body). New file: `commands/submit-pr.md` (C1).
- **New skill package (does NOT exist yet):** `src/superclaude/skills/sc-submit-pr-protocol/` with `SKILL.md` + `refs/` (detection-contract.md, state-machine.md, severity-routing.md, augment-poll.md, troubleshoot-dispatch.md, finding-verify.md, thread-reply.md, loop-guard.md) + `scripts/` (poll-augment-review.sh, reply-resolve-thread.sh).
- **Tests (new):** `tests/submit_pr/` (does not exist). Existing peers for patterns: `tests/cli_portify/`, `tests/recommend/`, `tests/hooks/`, `tests/skills/`, `tests/sprint/`. Conftest peers: `tests/conftest.py`, `tests/recommend/conftest.py`, `tests/sprint/conftest.py`.
- **MDTM template (the GENERATED task file's own template):** `.claude/templates/workflow/02_mdtm_template_complex_task.md` (and `src/superclaude/templates/workflow/02_...`).
- **Sync model:** `make sync-dev` (src→.claude), `make verify-sync`. `make lint` (ruff check) + `uv run ruff format --check src/ tests/` (the two-gate CI gotcha, spec VG-3/VG-4). `make test` = `uv run pytest`.

## PATTERNS_AND_CONVENTIONS

- **Skill package shape:** `sc-<name>-protocol/SKILL.md` + `refs/*.md` (+ optional `scripts/`, `evals/`). Source-of-truth = `src/superclaude/`; never edit `.claude/` directly; `.claude/{skills,commands,agents,hooks}` is gitignored sync-dev output (only `.claude/settings.json` tracked).
- **Command file shape:** YAML frontmatter (`name`, `description`, `category`, `complexity`, `mcp-servers`, `personas`, `argument-hint`) + `## Triggers` + `## Required Input` markdown body. Command body delegates to the protocol skill.
- **Hook conventions:** bash, `set -u`, read stdin JSON, cheap prefilter `case` before `jq`, exit 0 = pass-through (stdout surfaced as context), exit 2 = block. Fail-open (`|| true`, `// empty`). offer-pr-review.sh is the canonical example.
- **gh/git discipline (CLAUDE.md ABSOLUTE RULES — binding):** every `gh`/`gh api` pins `--repo IronbellyOrg/IronClaude` / `repos/IronbellyOrg/IronClaude/...`; push target `origin` never `upstream`; commit trailer `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`. Spec §1/§19 encode these as FR-1.3/AC-7/VG-6.
- **Single-line paste-ready commands; absolute paths in user-facing prompts** (memory `feedback_no_multiline_paste`, `feedback_always_absolute_paths`; spec NFR-5).

## GAPS_AND_QUESTIONS

Researchers must verify (not assume) the following — these are the high-risk seams:

1. **R1 DET probe is operational, not pure-code.** `detection-contract.md.locked` gates the entire build (§3 step 0, §7, AC-8). The probe requires empirically hitting a live GitHub PR with the Augment Code GitHub App installed to capture the real bot login + emission shape. Researcher must determine: is the probe a manual operator step the task file encodes as a HALT/human-decision item, or can fixtures stand in (§18.4 says synthetic-until-probe)? The build sequencing makes locking the contract a prerequisite — the task file must handle "probe-not-yet-run" cleanly (build BLOCKS while `locked:false`).
2. **Can a skill actually *arm* the Monitor tool, and how?** FR-1.5/FR-2.4 — "Monitor hosted by Monitor tool". Verify how (or whether) protocol skills invoke the Monitor harness tool, and the realistic shape of `poll-augment-review.sh` emitting one JSON line per poll into a Monitor stream. This determines whether the FSM loop is skill-orchestrated prose or a real Monitor stream.
3. **`/sc:troubleshoot` programmatic invocation contract** (C3b): exact flags the dispatcher passes (`--fix`, `--depth deep --fix`, `--scope`), and how seeding (file:line + evidence body) is delivered so troubleshoot does not re-derive (FR-3.3).
4. **Reuse surface of severity-rubric.md** — read it fully: what categories/confidence/diff-locality adjustments exist, so C3 `severity-routing.md` reuses rather than reinvents (FR-3.1, QD-6, T-301/T-302).
5. **pytest marker registration** — `@pytest.mark.loop_guard/autonomy/recovery/p0` (§18.2) must be registered (pyproject.toml `[tool.pytest.ini_options]` markers or conftest) or `--strict-markers` fails. Verify current marker registry + coverage config (`--cov=superclaude.skills...`).
6. **How are skill behaviors unit-tested?** The spec asserts on `run_skill(...)` returning `round_counter`, `push_count`, `states_visited`, etc. — this implies a Python harness/shim modeling the FSM, not just markdown. Researcher must determine whether the test surface is (a) a Python module implementing the deterministic core (FSM/router/loop-guard/classifier) that tests import, or (b) pure-markdown skill with tests over scripts only. The 115-test matrix (esp. unit FSM/loop-guard/router) strongly implies a Python deterministic-core module exists alongside the markdown refs. THIS IS THE PIVOTAL ARCHITECTURE QUESTION for the task file.

## RECOMMENDED_OUTPUTS

Research files to create in `${TASK_DIR}research/`:

- `01-component-inventory.md` — verify every C1–C6 path; exists-vs-new; line counts of reuse targets.
- `02-skill-command-hook-conventions.md` — skill/refs/command/hook structural patterns with file:line evidence.
- `03-reuse-surfaces.md` — severity-rubric.md (C3), auggie-review grounding (C3a), troubleshoot dispatch contract (C3b) — exact reusable APIs.
- `04-test-infra-and-deterministic-core.md` — tests/ layout, conftest/subprocess/gh mocking, marker+coverage registration, AND the deterministic-core-module-vs-markdown question (Gap #6) — pivotal.
- `05-integration-points.md` — Monitor tool arming (Gap #2), /sc:troubleshoot invocation (Gap #3), command→skill registration, sync-dev/install, gh/git discipline surfaces.
- `06-detection-probe-and-gh-surface.md` — R1 DET probe operationality (Gap #1), gh API surfaces for poll (reviews/comments/check-runs), GraphQL resolveReviewThread, hook-test patterns.
- `07-mdtm-template-and-examples.md` — MDTM template 02 PART 1 rules (A3/A4/B2, M3/M4/I19–I22, L1–L6), prior TASK-RF examples.

## SUGGESTED_PHASES (researcher assignments — spawn ALL in one message, Deep tier = 7)

- **R1 — File Inventory:** scope = all C1–C6 paths in §2 + reuse targets. Output `01-component-inventory.md`. Others cover conventions/reuse/tests/integration/probe/template — do not duplicate.
- **R2 — Patterns & Conventions:** scope = skill package shape, command frontmatter, hook conventions (read 2-3 skills + 2-3 commands + 2 hooks). Output `02-...`.
- **R3 — Reuse Surfaces:** scope = severity-rubric.md (full), sc-auggie-review grounding, sc-troubleshoot dispatch/handoff refs. Output `03-...`.
- **R4 — Test Infra + Deterministic Core (PIVOTAL):** scope = tests/ peers, conftest mocking, marker/coverage registration, pyproject; resolve whether the deterministic core is a Python module the tests import. Output `04-...`.
- **R5 — Integration Points:** scope = Monitor tool arming reality, /sc:troubleshoot invocation contract, command/skill registration, sync-dev/install, gh/git rules. Output `05-...`.
- **R6 — Detection Probe + gh Surface:** scope = R1 probe operationality, gh poll/REST/GraphQL surfaces, hook-test patterns. Output `06-...`.
- **R7 — MDTM Template & Examples:** scope = template 02 PART 1, prior TASK-RF examples. Output `07-...`.

## TEMPLATE_NOTES

- **Generated task file template:** 02 (Complex) — discovery (R1 probe), build across a dependency DAG (§3), validation, test phases, QA gates. Not a direct transformation.
- **Tier:** Deep. Single track.
- **QA gates in generated file:** PER_PHASE (Template 02 default) given the multi-phase DAG; final-document not applicable (this builds code+tests, not a >500-line document — M4 fidelity gate likely N/A, but I21 must be evaluated by the builder).
- **Granularity:** one checklist item per component file (C1 SKILL.md, each of the 8 refs, each of 2 scripts, command, hook edit) and ideally per test file (21 test files in §6.3) — the spec is exhaustive enough to support per-file items. Build order MUST follow the §3 DAG (DET gate first).
- **POST reflect gate:** ENABLED; SPEC_PATH = merged-spec.md; DEPTH floored at standard (likely deep given TCS — cross-subsystem + new package).

## AMBIGUITIES_FOR_USER

- **R1 DET probe execution.** The spec makes locking `detection-contract.md` a hard build gate requiring a live empirical probe of the Augment GitHub App on a real PR. Whether that probe can be run now (is the Augment app installed + a live PR available?) or must be deferred is an operational question the task file should surface as a `needs_human_decision` / explicit prerequisite item rather than silently assume. Researchers will characterize it; the builder will encode it as a gating prerequisite, but the *decision to run the probe* is the operator's.
- Otherwise intent is clear from the spec and codebase context — the spec is a complete, adversarially-merged design with FR/NFR/AC/INV all mapped to concrete test IDs.
