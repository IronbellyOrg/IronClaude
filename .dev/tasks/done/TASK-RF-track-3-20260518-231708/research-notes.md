# Research Notes — TASK-RF-track-3 (FU-003: PRD-skill CWD-default output routing)

**Scenario:** A (Explicit — stubs gave hypotheses, references, acceptance criteria)
**Depth Tier:** Standard
**Track Count:** 3 of 3 (multi-track build)
**Template:** 02 (Complex — discovery + fix + test + validation phases)

---

## GOAL

Route PRD-skill dry-run/test output to `.dev/eval-workspaces/<slug>/` instead of repo root, and add a PreToolUse hook (or guard in skill) that rejects writes to `<repo-root>/prd-*-test/`, `<repo-root>/prd-*/`.

## WHY

`tests/cli/prd/test_prompts.py` creates `prd-test-product/` and `prd-dry-run-test/` at the repo root every test run. The Phase 3 `.gitignore` guards are a retroactive safety net; the root fix is in the test harness + PRD skill output resolver.

---

## 1. EXISTING_FILES

- `src/superclaude/skills/prd/SKILL.md` (likely contains output-path-resolution prose)
- `src/superclaude/skills/prd/refs/` (the skill's reference docs)
- `tests/cli/prd/test_prompts.py` — CONFIRMED CREATOR (per grep)
- `.claude/hooks/reject-workspace-writes.sh` + `src/superclaude/hooks/scripts/reject-workspace-writes.sh` — existing hook pattern to extend
- `.claude/settings.json` (PreToolUse registration site for hooks)
- `src/superclaude/hooks/hooks.json` — source-of-truth hook config
- Reference stub: `.dev/tasks/to-do/follow-ups/FU-003-prd-skill-cwd-default-output-routing.md`
- CLAUDE.md "Plugin Override — Skill-Creator Workspace Destination" section (intended convention)

## 2. PATTERNS_AND_CONVENTIONS

- Hook registration: `_FRESHNESS_SCRIPTS` in `src/superclaude/cli/install_hooks.py`; settings.json PreToolUse matchers
- Sync model: `src/` is source of truth; `make sync-dev` copies to `.claude/`; verify-sync gates
- skill-creator addendum precedent (CLAUDE.md) — skill writes a workspace; override redirects to `.dev/eval-workspaces/<skill-name>/`

## 3. GAPS_AND_QUESTIONS

- Does the PRD skill have a Python entry point (CLI command) that owns output routing, or is it pure prompt text in SKILL.md? (SKILL.md is markdown prompt; the test harness is what actually creates the dirs.)
- Should the fix be (a) only in the test harness `tests/cli/prd/test_prompts.py`, (b) only in a PreToolUse hook, or (c) both?
- What is the exact mechanism by which `tests/cli/prd/test_prompts.py` creates the dirs? (Calls a real PRD-runner with `--output prd-test-product`? Uses `subprocess.run`? Spawns Claude Code?)

## 4. RECOMMENDED_OUTPUTS

4 researchers — Track 3 is the most complex:

- `research/01-test-harness.md` — read `tests/cli/prd/test_prompts.py` fully, document how it creates `prd-test-product/` and `prd-dry-run-test/`, identify the output-path argument
- `research/02-skill-and-hook-patterns.md` — read SKILL.md output-routing prose + `reject-workspace-writes.sh` hook + `.claude/settings.json` registration pattern (skill-creator addendum precedent)
- `research/03-integration-points.md` — `_FRESHNESS_SCRIPTS` registration + `hooks.json` + sync model; verify any changes will propagate cleanly
- `research/04-template-examples.md` — Template 02 PART 1 + analogous hook-addition tasks under `.dev/tasks/done/`

## 5. SUGGESTED_PHASES

1. Inventory test-harness + skill output paths
2. Decide fix scope (test fix only vs hook addition vs both)
3. Implement fix (`test_prompts.py` output redirect + optional new hook)
4. Hook registration if applicable (`_FRESHNESS_SCRIPTS` + `hooks.json` + `settings.json`)
5. Sync via `make sync-dev` + verify-sync
6. Test phase (no `prd-*` dirs at repo root after pytest)
7. Validation + Completion

## 6. TEMPLATE_NOTES

Template 02. Standard tier (4 researchers because of integration with hook + sync model).

## 7. AMBIGUITIES_FOR_USER

- Whether to add a new hook (defense-in-depth) or only fix the test harness (minimal)
- Whether to mirror skill-creator's reject pattern exactly or invent a PRD-specific variant
