# Research: Verification & Sync Mechanics

**Topic type:** Test & Verification
**Scope:** Makefile, pre-commit, CI, per-file lint commands
**Status:** Complete
**Date:** 2026-05-20

---

## 1. Target file locations (canonical, source-of-truth)

The three files PR #64 remediation touches live under `src/superclaude/`. The
`.claude/` copies are sync-dev output and MUST NOT be edited directly.

| Fix | Source-of-truth (edit here) | Sync-dev mirror |
|-----|-----------------------------|-----------------|
| M1 — offer-pr-review.sh | `/config/workspace/IronClaude/src/superclaude/hooks/scripts/offer-pr-review.sh` | `/config/workspace/IronClaude/.claude/hooks/offer-pr-review.sh` |
| M2 — SKILL.md | `/config/workspace/IronClaude/src/superclaude/skills/sc-auggie-review-protocol/SKILL.md` | `/config/workspace/IronClaude/.claude/skills/sc-auggie-review-protocol/SKILL.md` |
| M4 — evals.json | `/config/workspace/IronClaude/src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json` | `/config/workspace/IronClaude/.claude/skills/sc-auggie-review-protocol/evals/evals.json` |

There is also a venv install copy at
`/config/workspace/IronClaude/.venv/lib/python3.12/site-packages/superclaude/_src/superclaude/hooks/scripts/offer-pr-review.sh`
— do NOT edit; reinstalled by `uv pip install -e .`.

---

## 2. Makefile targets — exact recipes (evidence: `Makefile` lines)

### 2.1 `make sync-dev` (Makefile:109–163)

Copies `src/superclaude/{skills,agents,commands,hooks/scripts,templates}` →
`.claude/{skills,agents,commands/sc,hooks,templates}`. Specifically for the
files in this PR:

- Hooks loop at **Makefile:138–143**:

  ```
  for hook in src/superclaude/hooks/scripts/*.sh; do
      [ -f "$hook" ] || continue;
      name=$(basename "$hook");
      cp "$hook" ".claude/hooks/$name";
      chmod +x ".claude/hooks/$name";
  done
  ```

  → `offer-pr-review.sh` is copied with `chmod +x`. **No interpretation of
  shell content** — a syntactically broken script will copy and become broken
  in `.claude/hooks/` as well.

- Skills loop at **Makefile:112–125** recursively copies every file under
  `src/superclaude/skills/<name>/` (excluding `__init__.py` and
  `__pycache__/`). So `SKILL.md`, `evals/evals.json`, and `refs/*.md` all
  copy across.

### 2.2 `make verify-sync` (Makefile:166–353) — drift detector (CI-friendly, exits 1 on drift)

Performs `diff -rq` between src/ and .claude/ for skills (Makefile:178),
agents (Makefile:210), commands (Makefile:236), hooks (Makefile:262), and
templates (Makefile:288). For this PR:

- **Hooks check (Makefile:255–278):** Reports `❌ MISSING` or `⚠️ DIFFERS`
  for `offer-pr-review.sh` if `src/` and `.claude/` versions don't match
  byte-for-byte. Exit code 1 → CI fails.
- **Skills check (Makefile:171–200):** Catches drift in any file inside the
  skill directory (SKILL.md, evals/evals.json, refs/*.md).
- **Installer registration check (Makefile:307–326):** Calls
  `from superclaude.cli.install_hooks import _FRESHNESS_SCRIPTS` and verifies
  the set of `*.sh` filenames matches `src/superclaude/hooks/scripts/`. If
  `offer-pr-review.sh` is added/removed from the directory but the Python
  constant `_FRESHNESS_SCRIPTS` is not updated, verify-sync fails. (For PR
  #64 we only EDIT the existing file, so this check should remain pass.)
- **Hooks cross-consistency check (Makefile:328–346):** Compares
  `mcp__auggie*` matchers between `hooks.json` and `auggie-flag-clear.sh`.
  Unrelated to our PR but runs regardless.

### 2.3 `make lint` (Makefile:48–50)

```
uv run ruff check .
```

Runs ruff against the entire repo. Lints `.py` only; bash scripts and JSON
are not covered. For PR #64 (no Python edits) this should be a no-op pass,
but run it anyway to confirm no accidental Python touch.

### 2.4 `make format` (Makefile:53–55)

```
uv run ruff format .
```

Same scope as lint. Run `uv run ruff format --check .` (without writing)
if you want a check-only pre-commit gate equivalent.

### 2.5 `make test` (Makefile:13–15)

```
uv run pytest
```

Runs full pytest suite. Not directly required for PR #64 verification but
needed before merge.

### 2.6 `make lint-architecture` (Makefile:356–472)

10 architecture-policy checks. Skills frontmatter completeness (Check 8,
Makefile:421–429) verifies SKILL.md still has `name:`, `description:`,
`allowed-tools:` fields. M2's SKILL.md edit appends a pipeline note — must
not break frontmatter.

---

## 3. Pre-commit hooks — what runs on `git commit`

Evidence: `.pre-commit-config.yaml`

| Hook id | File | Effect on PR #64 fixes |
|---------|------|-----------------------|
| `trailing-whitespace` (line 9, excludes `*.md`) | all non-md | Strips trailing WS from offer-pr-review.sh, evals.json |
| `end-of-file-fixer` (line 11) | all | Ensures trailing newline on every edited file |
| `check-yaml` (line 12) | YAML | Not triggered |
| `check-json` (line 14) | JSON | **Validates evals.json parses as JSON** — fails if M4 fix introduces malformed JSON |
| `check-toml` (line 15) | TOML | Not triggered |
| `check-added-large-files` (line 16, --maxkb=1000) | all | Pass; our files <1MB |
| `check-merge-conflict` (line 18) | all | Pass |
| `check-case-conflict` (line 19) | all | Pass |
| `mixed-line-ending` (line 20, --fix=lf) | all | Forces LF |
| `detect-secrets` (line 27) | all | Should pass; review scripts don't embed secrets |
| `detect-private-key` (line 44) | all | Pass |
| Custom hardcoded-secrets regex (line 46–54) | all | Pass |
| `conventional-pre-commit` (line 60, stage commit-msg) | commit msg | Forces conventional commit format |
| `markdownlint --fix` (line 68) | `*.md` | **Lints SKILL.md** — may auto-fix MD style issues (line length, list spacing, fenced-code language tags). Excludes CHANGELOG.md only. |
| `yamllint` (line 81, line-length max 120) | YAML | Not triggered |
| `shellcheck --severity=warning` (line 88) | `*.sh` | **Lints offer-pr-review.sh** at warning severity. Will catch case statement bugs, unquoted vars, etc. CRITICAL gate for M1. |
| `verify-sync` local hook (line 97–102) | files in `src/superclaude/(skills\|agents\|commands\|hooks)/` or `.claude/(skills\|agents\|commands\|hooks)/` | Runs `make verify-sync`. **Blocks commit if src/ and .claude/ are not in sync.** Pass requires `make sync-dev` first. |

`default_stages: [commit]`, `fail_fast: false` (line 105–106).

---

## 4. CI workflow — `.github/workflows/test.yml`

Triggers: push/PR to `master` or `integration` (line 5–7).

Jobs (line 10–205):

1. **test** (line 11–62, matrix py 3.10/3.11/3.12) — runs `pytest -v --tb=short --color=yes` (line 48); coverage on 3.10 (line 53).
2. **lint** (line 64–92):
   - `ruff check src/ tests/` (line 88)
   - `ruff format --check src/ tests/` (line 92)
   Note: CI's lint scope is `src/ tests/`, narrower than `make lint`'s `.`.
3. **plugin-check** (line 94–122) — verifies pytest plugin loads and exposes fixtures.
4. **verify-deps** (line 124–148) — runs `make verify-deps` (dependency allow-list, AC3).
5. **doctor-check** (line 150–174) — runs `superclaude doctor --verbose`.
6. **test-summary** (line 176–205) — gates merge on all above.

**No `make verify-sync` job in CI** — the only enforcement of src/↔.claude/
parity is the pre-commit `verify-sync` local hook. Therefore if a contributor
bypasses pre-commit (e.g., `git commit --no-verify`), drift can land. PR #64
must run `make verify-sync` locally before commit.

---

## 5. Per-file verification one-liners

### 5.1 Fix M1 — `offer-pr-review.sh`

```bash
# Syntax check (always available, no external deps)
bash -n /config/workspace/IronClaude/src/superclaude/hooks/scripts/offer-pr-review.sh && echo "SYNTAX OK" || echo "SYNTAX FAIL"

# Shellcheck at warning severity (matches pre-commit config)
shellcheck --severity=warning /config/workspace/IronClaude/src/superclaude/hooks/scripts/offer-pr-review.sh && echo "SHELLCHECK OK"

# Verify executable bit preserved (sync-dev re-chmods; src/ should already be +x)
test -x /config/workspace/IronClaude/src/superclaude/hooks/scripts/offer-pr-review.sh && echo "EXECUTABLE OK"

# Functional trace: feed a sample stdin payload through the prefilter case
# (Build a minimal hook input JSON matching the script's expected schema.
# Researcher-01 will provide the exact case body and sample tool_name strings.)
echo '{"tool_name":"Bash","tool_input":{"command":"echo test"}}' | \
  /config/workspace/IronClaude/src/superclaude/hooks/scripts/offer-pr-review.sh; echo "exit=$?"

# Diff between src/ and .claude/ copies (should be identical AFTER sync-dev)
diff /config/workspace/IronClaude/src/superclaude/hooks/scripts/offer-pr-review.sh \
     /config/workspace/IronClaude/.claude/hooks/offer-pr-review.sh && echo "SYNC OK"
```

**Pass criteria for M1:**

- `bash -n` exit 0
- `shellcheck --severity=warning` exit 0 (or only acceptable info-level notes)
- sample stdin payload trace exits as expected for each `tool_name` case branch (early-exit for non-PR tools; proceed for PR-related tools)
- `diff` shows no difference after `make sync-dev`

### 5.2 Fix M2 — `SKILL.md` (sc-auggie-review-protocol)

```bash
# Read the changed lines to visually confirm exact pipeline string
sed -n '1,40p' /config/workspace/IronClaude/src/superclaude/skills/sc-auggie-review-protocol/SKILL.md
# (Or use Read tool on lines around the M2 edit point — researcher-01 supplies exact line range)

# Frontmatter sanity (must still have required keys; lint-architecture Check 8)
grep -E '^(name|description|allowed-tools):' \
  /config/workspace/IronClaude/src/superclaude/skills/sc-auggie-review-protocol/SKILL.md
# Expect: at least 3 lines printed (name:, description:, allowed-tools:)

# Markdownlint dry-run (matches pre-commit hook)
npx markdownlint /config/workspace/IronClaude/src/superclaude/skills/sc-auggie-review-protocol/SKILL.md 2>&1 \
  || echo "markdownlint not on PATH — pre-commit will run it instead"

# Pipeline-string exact-match grep (researcher-01 supplies the literal string)
grep -F "<EXACT_PIPELINE_STRING_FROM_RESEARCHER_01>" \
  /config/workspace/IronClaude/src/superclaude/skills/sc-auggie-review-protocol/SKILL.md \
  && echo "PIPELINE STRING PRESENT"

# Diff src/ vs .claude/ (post sync-dev)
diff /config/workspace/IronClaude/src/superclaude/skills/sc-auggie-review-protocol/SKILL.md \
     /config/workspace/IronClaude/.claude/skills/sc-auggie-review-protocol/SKILL.md && echo "SYNC OK"
```

**Pass criteria for M2:**

- Frontmatter still contains `name:`, `description:`, `allowed-tools:` (lint-architecture Check 8 stays green)
- Pipeline string appears verbatim (`grep -F` finds 1 match)
- src/ and .claude/ identical after sync-dev
- `make lint-architecture` exits 0

### 5.3 Fix M4 — `evals.json`

```bash
# Parse-valid JSON (matches pre-commit check-json hook)
jq . /config/workspace/IronClaude/src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json > /dev/null \
  && echo "JSON VALID"

# Pretty-print to eyeball structure
jq . /config/workspace/IronClaude/src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json | head -60

# Count assertions per scenario (M4 requires each scenario to have exactly 3 assertions)
# NOTE: exact JSON shape comes from researcher-02 (eval-harness DSL). Likely shapes:
#   .scenarios[] | {name, assertion_count: (.assertions | length)}
#   .evals[]    | {name, assertion_count: (.assertions | length)}
jq '.scenarios[] | {name: .name, assertion_count: (.assertions | length)}' \
  /config/workspace/IronClaude/src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json

# Fail-fast check: every scenario must have len(assertions) == 3
jq -e '[.scenarios[] | (.assertions | length) == 3] | all' \
  /config/workspace/IronClaude/src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json \
  && echo "ALL SCENARIOS HAVE 3 ASSERTIONS" \
  || echo "FAIL - at least one scenario does not have exactly 3 assertions"

# Diff src/ vs .claude/ (post sync-dev)
diff /config/workspace/IronClaude/src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json \
     /config/workspace/IronClaude/.claude/skills/sc-auggie-review-protocol/evals/evals.json && echo "SYNC OK"
```

**Pass criteria for M4:**

- `jq .` exits 0 (valid JSON)
- Every scenario has exactly 3 assertions (`jq -e ... | all` exits 0)
- `check-json` pre-commit hook passes
- src/ and .claude/ identical after sync-dev

---

## 6. Full post-edit verification chain (run in this order)

Run from repo root `/config/workspace/IronClaude/`:

```bash
# 1. Per-file fast gates (run BEFORE sync)
bash -n src/superclaude/hooks/scripts/offer-pr-review.sh
shellcheck --severity=warning src/superclaude/hooks/scripts/offer-pr-review.sh
jq . src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json > /dev/null
jq -e '[.scenarios[] | (.assertions | length) == 3] | all' \
   src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json
grep -E '^(name|description|allowed-tools):' \
   src/superclaude/skills/sc-auggie-review-protocol/SKILL.md

# 2. Propagate src/ -> .claude/
make sync-dev

# 3. Confirm parity
make verify-sync   # exits 1 on any drift

# 4. Architecture policy
make lint-architecture   # checks SKILL.md frontmatter (Check 8), command/skill pairs

# 5. Python lint/format (no-op for this PR but confirms no accidental .py touch)
make lint
uv run ruff format --check .

# 6. Optional: run pytest if any test files were touched (PR #64 should not touch tests)
make test

# 7. Skill protocol self-validation (project mandate from user)
# /sc:reflect --type task --validate
#   <- invoke as a slash command in Claude Code session; not a CLI binary.

# 8. Pre-commit dry-run (catches anything the gates above missed)
pre-commit run --all-files
# OR scope to changed files only:
pre-commit run --files \
   src/superclaude/hooks/scripts/offer-pr-review.sh \
   src/superclaude/skills/sc-auggie-review-protocol/SKILL.md \
   src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json \
   .claude/hooks/offer-pr-review.sh \
   .claude/skills/sc-auggie-review-protocol/SKILL.md \
   .claude/skills/sc-auggie-review-protocol/evals/evals.json
```

**Overall pass criteria:** every step exits 0. If `verify-sync` reports drift,
re-run `make sync-dev` and re-check. If pre-commit auto-modifies any file
(markdownlint --fix, end-of-file-fixer, mixed-line-ending), re-stage and
re-run before committing.

---

## 7. What happens when the user commits

1. `pre-commit` runs all hooks in section 3.
2. The `verify-sync` local hook (`.pre-commit-config.yaml:97–102`) fires
   because edited paths match the trigger regex
   `^(src/superclaude/(skills|agents|commands|hooks)|\.claude/(skills|agents|commands|hooks))/`.
   It runs `make verify-sync` — if drift, commit is blocked.
3. `shellcheck` flags any new warning in offer-pr-review.sh; `check-json`
   rejects malformed evals.json; `markdownlint --fix` may auto-modify
   SKILL.md (re-stage if so).
4. `conventional-pre-commit` validates the commit message format (e.g.,
   `fix(sc-auggie-review): ...`).
5. On push, CI in section 4 runs `pytest`, `ruff check src/ tests/`,
   `ruff format --check src/ tests/`, plugin checks, dependency allow-list,
   and doctor. **CI does NOT run verify-sync** — this is the pre-commit
   gate's exclusive responsibility.

---

## 8. Gaps / caveats

- **CI does not enforce src/↔.claude/ parity.** A `--no-verify` commit can
  bypass `verify-sync`. The task file should explicitly forbid `--no-verify`.
- **`make lint-architecture` is not in CI either** — only invoked manually.
  Task file should require it.
- **`/sc:reflect --type task --validate`** is a Claude Code slash command,
  not a CLI; it cannot be wired into pre-commit or CI. Must be invoked from
  inside a Claude session before the user commits, per user constraint.
- **shellcheck may not be installed locally** — if `command -v shellcheck`
  fails, pre-commit will pull a pinned version
  (`shellcheck-py v0.9.0.6` per `.pre-commit-config.yaml:86`). For local
  pre-flight, run `pre-commit run shellcheck --files <file>` to use the
  pinned version.
- **markdownlint --fix may rewrite SKILL.md.** Re-stage after pre-commit
  if `git status` shows the file modified.
- **evals.json assertion-count `jq` query is shape-dependent.** Researcher-02
  is delivering the eval-harness DSL definitive shape; if it's
  `.evals[].assertions` instead of `.scenarios[].assertions`, swap the
  jq path accordingly in the one-liners above.

---

## Summary

All three fixes in PR #64 have well-defined verification gates:

- **M1 (offer-pr-review.sh)**: `bash -n` + `shellcheck --severity=warning`
  (pre-commit-pinned) + stdin trace + post-sync diff.
- **M2 (SKILL.md)**: frontmatter grep + literal pipeline-string `grep -F` +
  markdownlint (via pre-commit) + lint-architecture Check 8 + post-sync diff.
- **M4 (evals.json)**: `jq .` parse + `jq -e '[...|all]'` count check +
  pre-commit `check-json` + post-sync diff.

The mandatory post-edit chain is: per-file gates → `make sync-dev` →
`make verify-sync` → `make lint-architecture` → `make lint` →
`ruff format --check` → (optional) `make test` → `/sc:reflect --type task
--validate` (in-session) → `pre-commit run --files <changed>`. Every step
must exit 0 before commit. The pre-commit `verify-sync` local hook is the
sole gate enforcing src/↔.claude/ parity (CI does not).
