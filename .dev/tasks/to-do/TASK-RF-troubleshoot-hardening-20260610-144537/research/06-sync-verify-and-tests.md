# Research: Sync/Verify + Tests
**Topic type:** Test & Verification
**Scope:** Makefile + lint + tests/
**Status:** Complete
**Date:** 2026-06-10
---

## 1. Makefile — `sync-dev` and `verify-sync` mechanics

`.PHONY` confirms both targets exist (`Makefile:1`).

### `sync-dev` (Makefile:109–163)

For each skill dir under `src/superclaude/skills/*/` (skipping `__*`), if it has a `SKILL.md`/`skill.md`, it mirrors **every file recursively** into `.claude/skills/<name>/`, preserving subdir structure (Makefile:112–125):

```make
@for skill_dir in src/superclaude/skills/*/; do \
    skill_name=$$(basename "$$skill_dir"); \
    case "$$skill_name" in __*) continue;; esac; \
    if [ -f "$$skill_dir/SKILL.md" ] || [ -f "$$skill_dir/skill.md" ]; then \
        mkdir -p ".claude/skills/$$skill_name"; \
        find "$$skill_dir" -type f ! -name '__init__.py' ! -path '*/__pycache__/*' -exec sh -c ' \
            src="$$1"; skill_dir="$$2"; target_base="$$3"; \
            rel=$${src#$$skill_dir}; \
            target_dir="$$target_base/$$(dirname "$$rel")"; \
            mkdir -p "$$target_dir"; \
            cp "$$src" "$$target_dir/" \
        ' _ {} "$$skill_dir" ".claude/skills/$$skill_name" \; ; \
    fi; \
done
```

**FINDING (deliverable #1):** The `find ... -type f` copies *all* files under the skill dir except `__init__.py` / `__pycache__`. So **5 new refs created at `src/superclaude/skills/sc-troubleshoot-protocol/refs/*.md` are auto-mirrored** to `.claude/skills/sc-troubleshoot-protocol/refs/` by `sync-dev` — no per-file registration. The `rel=$${src#$$skill_dir}` logic preserves the `refs/` subpath. Edited SKILL.md / report / handoff under `src/` are re-copied (overwrite). Commands mirror separately (Makefile:131–136: `src/superclaude/commands/*.md` → `.claude/commands/sc/`), so an edited `sc-troubleshoot.md` command also syncs.

### `verify-sync` (Makefile:166–353)

Bidirectional drift check; `exit 1` on ANY drift (Makefile:348–353). Per component:

- **Skills (Makefile:171–200):** Each `src/` skill must have `.claude/skills/<name>` AND `diff -rq --exclude='__init__.py' --exclude='__pycache__'` must be empty (Makefile:178). Reverse pass flags any `.claude/skills/*` lacking a `src/` counterpart or lacking `SKILL.md` (Makefile:188–200).
- **Commands (Makefile:229–252):** Each `src/superclaude/commands/*.md` must have a `diff -q`-clean `.claude/commands/sc/<name>`; reverse orphan check too.

**FINDING (deliverable #1):** `verify-sync` does a recursive `diff -rq` of the whole skill dir. Creating 5 NEW refs is fine **as long as `sync-dev` ran first** so both sides are byte-identical. There is **NO ref-count assertion, NO ref-filename allow-list, NO manifest**. New refs cannot break verify-sync provided src↔.claude match. Only failure modes: forgetting `sync-dev` (→ "MISSING in .claude/" or "DIFFERS"), or a `.claude/` file with no `src/` origin.

Other verify-sync sections (Agents 203–226, Hooks 254–278, Templates 280–305, Installer Registration 307–326, Hooks Cross-Consistency 328–346) are **not touched** by this task — no agent/hook/template/installer changes in scope.

---

## 2. Pre-commit / markdownlint config

### `.markdownlint.json` (full file)

```json
{
  "default": true,
  "MD024": { "siblings_only": true },
  "MD013": false,
  "MD029": false,
  "MD036": false,
  "MD033": false
}
```

- `"default": true` → all markdownlint rules ON except those disabled below.
- **MD025 (single H1 / no multiple top-level headings) is ENABLED** (not disabled). New refs must have exactly one `#` H1. Watch the frontmatter-title trap (memory `reference_markdownlint_md025_frontmatter_title.md`): if a ref has BOTH frontmatter `title:` AND a body `# H1`, MD025's `front_matter_title` counts the frontmatter as the H1 → demote body `# ` to `## `.
- `MD024` siblings_only → duplicate headings allowed only if not siblings.
- Disabled: MD013 (line length), MD029 (ordered-list prefix), MD036 (emphasis-as-heading), MD033 (inline HTML). So long lines, bold-as-heading, and inline HTML are permitted.
- Other defaults stay ON: MD012 (no multiple blanks), MD022 (headings surrounded by blanks), MD031/MD032 (fenced blocks / lists surrounded by blanks), MD040 (fenced code language), MD041 (first line = top-level heading), MD047 (file ends with single newline), MD009 (no trailing spaces), etc.

### markdownlint pre-commit hook (.pre-commit-config.yaml:70–82)

```yaml
- repo: https://github.com/igorshubovych/markdownlint-cli
  rev: v0.38.0
  hooks:
    - id: markdownlint
      args: ['--fix']
      exclude: |
        (?x)^(
          CHANGELOG\.md|
          .*node_modules.*|
          .*\.min\.md$|
          \.dev/.*
        )$
```

**FINDING (deliverable #2):**
- markdownlint **DOES run on `src/superclaude/**/*.md`** (and on `.claude/` mirrors), and runs with `--fix` (auto-corrects fixable rules like trailing newline, blank-line spacing on staged files).
- markdownlint **EXCLUDES `\.dev/.*`** (line 81) → the generated MDTM task file under `.dev/tasks/...` is NOT markdownlinted. The task file itself is exempt; the **edited skill/command/report/handoff and the 5 new refs under `src/superclaude/skills/sc-troubleshoot-protocol/` ARE linted** and must satisfy MD025/MD041/MD040/MD047/etc.

### Other relevant pre-commit hooks

- `end-of-file-fixer`, `mixed-line-ending --fix=lf`, `check-added-large-files --maxkb=1000` (refs must be < 1MB, trivially true).
- `trailing-whitespace` excludes `\.md$` (line 10) — so trailing-whitespace on `.md` is handled by markdownlint MD009, not this hook.
- `detect-secrets` / `detect-private-key` / hardcoded-secrets grep — refs are prose, no secrets expected.
- **`block-claude-generated-mirrors` (local, .pre-commit-config.yaml:102–109):** `entry: scripts/precommit_block_claude_mirrors.sh`, `files: '^\.claude/(skills|agents|commands|hooks|templates)/'` → **rejects any staged `.claude/` mirror on the commit path.** This is the mechanical enforcement of the CLAUDE.md "never stage `.claude/`" rule.
- `verify-bare-review-mirror-matches-src` (local, :117–124) is scoped `files: '^src/superclaude/skills/sc-bare-review/'` — does NOT fire for troubleshoot.
- **There is NO `verify-sync` pre-commit hook** in `.pre-commit-config.yaml`. The comments at :100 and :115 explicitly state `make verify-sync` remains the *authoritative CI gate*, and pre-commit deliberately does NOT require staging mirrors. (CLAUDE.md's phrase "pre-commit `verify-sync` local hook" is slightly imprecise; the actual local hooks are `block-claude-generated-mirrors` + the narrow bare-review parity check. Full verify-sync runs in CI / manually via `make verify-sync`.) Confirmed: `grep verify-sync .pre-commit-config.yaml` only matches comment lines, not a hook.

---

## 3. Tests — metadata / refs / structure / install

Searched `tests/` for: command frontmatter parsing, ref counting/enumeration, troubleshoot skill structure validation, install/package expectations.

- `tests/cli/test_verify_sync_hooks.py` — exercises ONLY the `=== Hooks ===`, `=== Installer Registration ===`, `=== Hooks Cross-Consistency ===` sections (docstring lines 1–26, scenarios V1–V7). It mutates `src/superclaude/hooks/` and `install_hooks.py`. It does **NOT** assert on Skills or Commands diff sections, and never reads troubleshoot files. Adding refs / editing the troubleshoot command summary does NOT affect it. (grep for `Skills|Commands|refs` in this file → no matches.)
- `tests/pipeline/test_diagnostic_chain.py` — `DiagnosticStage.TROUBLESHOOT` is a **CLI pipeline diagnostic stage** (`superclaude.cli.pipeline.diagnostic_chain`), unrelated to the `sc-troubleshoot-protocol` skill. Not affected.
- `tests/test_sc_roadmap_refactor.sh` — greps `allowed-tools`/`name:`/`description:` but scoped strictly to `src/superclaude/commands/roadmap.md` and `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` (lines 57–107). Does **NOT** touch troubleshoot.
- No test reads `src/superclaude/skills/sc-troubleshoot-protocol/*` (grep for `sc-troubleshoot-protocol|skills/sc-troubleshoot|sc_troubleshoot` in `tests/` → **zero matches**).
- All `len(...refs...)` / `refs == N` assertions belong to unrelated subsystems: `tests/sprint/test_recovery.py:210`, `tests/cli_portify/test_prompts.py` / `test_process.py` / `test_discover_components.py`, `tests/v3.3/*` `spec_refs`. None count skill `refs/` files.
- The swarm tests that grep-matched "troubleshoot" reference a hypothesis-table fixture (`tests/swarm/fixtures/.../troubleshoot_hypothesis.raw.txt`), not the skill package.

**FINDING (deliverable #3) — TESTING_REQUIREMENTS = NONE.** No test in `tests/` parses the troubleshoot command/skill frontmatter, counts or enumerates skill refs, or validates the troubleshoot skill's structure. Spec §9's conditional ("targeted tests for sync/install/package expectations *if* command/skill metadata is parsed by tests") evaluates FALSE — the antecedent does not hold. Adding 5 refs + editing the behavioral summary cannot break any existing test. The task does **not** need to add or modify any pytest test. The only verification surface is `make sync-dev` + `make verify-sync` + markdownlint, all run during the validation phase (not as new automated tests).

---

## 4. CLAUDE.md rule confirmation — never stage `.claude/` except settings.json

Confirmed against project CLAUDE.md "ABSOLUTE RULE: Never Stage or Commit `.claude/` Contents" and memory `feedback_claude_dir_gitignored.md`:
- `.claude/{skills,commands,agents,hooks,templates}/*` is gitignored sync-dev output. ONLY `.claude/settings.json` is tracked.
- Mechanical enforcement: `.gitignore` (`.claude/` + `!.claude/settings.json`) PLUS the pre-commit local hook `block-claude-generated-mirrors` (.pre-commit-config.yaml:102–109) which rejects any staged `.claude/(skills|agents|commands|hooks|templates)/` path.
- If `git add` requires `-f` on a `.claude/` path → STOP; move change to `src/` and `make sync-dev`.

**Task implication:** The validation phase MUST run `make sync-dev` (to mirror src→.claude so verify-sync passes) and `make verify-sync` (drift gate), but the task may stage ONLY the `src/superclaude/skills/sc-troubleshoot-protocol/**` and `src/superclaude/commands/sc-troubleshoot.md` (if the command is edited) sources — NEVER the `.claude/` mirror. `git status` after sync-dev will show modified/new files under `.claude/skills/sc-troubleshoot-protocol/`; those are expected and must remain unstaged.

---

## TESTING_REQUIREMENTS recommendation

**NONE.** No automated test parses troubleshoot command/skill metadata or counts refs (deliverable #3 verified, zero matches). Spec §9's conditional for adding targeted tests does not trigger. Do NOT add or modify pytest tests for this task. Verification is performed entirely by the validation command sequence below — these are run by the task executor as validation steps, not committed as new tests.

## VALIDATION command sequence (for the task's validation phase)

Run from repo root `/config/workspace/IronClaude`, after the 4 edits + 5 new refs land under `src/superclaude/skills/sc-troubleshoot-protocol/` (and any command edit under `src/superclaude/commands/`):

1. **Mirror src → .claude:**
   `make sync-dev`
2. **Drift gate (authoritative, must exit 0):**
   `make verify-sync`
   Expect the `=== Skills ===` block to show `✅ sc-troubleshoot-protocol` and `=== Commands ===` to show `✅ sc-troubleshoot.md` if edited; final line `✅ All components in sync.`
3. **Markdownlint the edited + new source markdown (only the in-scope files; `.dev/` is excluded by config so the task file is exempt):**
   `npx markdownlint-cli@0.38.0 src/superclaude/skills/sc-troubleshoot-protocol/**/*.md`
   (or `uv run pre-commit run markdownlint --files <the changed src .md files>`). Must report 0 errors. Pay attention to MD025/MD041 (single H1, H1 first line), MD040 (fenced code language), MD047 (final newline) on the 5 new refs.
4. **Confirm NO `.claude/` staging (CLAUDE.md absolute rule):**
   `git status --porcelain | grep '^[AM].*\.claude/'` → must produce NO output (other than possibly `.claude/settings.json` if intentionally changed, which is not in scope here).
   Stage ONLY `src/` paths: `git add src/superclaude/skills/sc-troubleshoot-protocol src/superclaude/commands/sc-troubleshoot.md` (the latter only if edited).
5. (Optional sanity) `git diff --cached --name-only | grep -c '\.claude/'` → must be `0`.

Note: do not invoke `pre-commit run --all-files` blindly during validation if it would try to stage/inspect `.claude/` mirrors — the `block-claude-generated-mirrors` hook is keyed on staged `.claude/` paths, so as long as only `src/` is staged it stays green.
