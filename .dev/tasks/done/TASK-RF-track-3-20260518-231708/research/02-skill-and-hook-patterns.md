# Research — Track 3: Skill Output-Routing & Hook Precedent (FU-003)

**Date:** 2026-05-18
**Task:** TASK-RF-track-3 (parallel research)
**Scope:** PRD-skill CWD-default output routing — hook layer
**Status:** Complete

## Goal
Determine whether to extend `reject-workspace-writes.sh` or introduce a sibling
hook to block stray PRD writes at `<repo-root>/prd-*-test/` and
`<repo-root>/prd-*/`. Document the existing precedent (reject-workspace-writes
+ skill-creator addendum) and recommend an approach.

---

## 1. Existing `reject-workspace-writes.sh` Hook

**File:** `src/superclaude/hooks/scripts/reject-workspace-writes.sh` (40 lines total)

### Purpose & contract
- Header comment (lines 1–13) declares this is a **PreToolUse(Write|Edit)**
  reject-with-redirect for the skill-creator sibling-workspace convention.
- Decision contract is explicit (lines 6–8):
  - `exit 0` → allow (path does not match)
  - `exit 2 + stderr` → block; stderr is surfaced to Claude as the deny reason
- Negative cases (lines 11–13) are spelled out so the script cannot misfire on
  `.claude/skills/<X>/file.md` or `.claude/skills/<X>/workspace.md`.

### Input parsing
- Line 17: `INPUT="$(cat 2>/dev/null || true)"` — slurps stdin (hook protocol).
- Line 20: `TARGET="$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty' …)"`
  — extracts `file_path` (the canonical key for `Write` and `Edit` tool inputs).
- Line 23: `[ -z "${TARGET:-}" ] && exit 0` — **fail-open** when no path.

### Match pattern
- Line 28: `if [[ "$TARGET" =~ \.claude/skills/([^/]+)-workspace/(.*)$ ]]; then`
  - Uses a Bash regex, anchored at the trailing `-workspace/<remainder>` segment.
  - Captures `SKILL_X` and `REMAINDER` into `BASH_REMATCH[1]` / `[2]`.
  - The trailing `/` after `-workspace` is what makes this directory-segment
    precise (avoids matching `something-workspace.md` files).

### Redirect message format (lines 31–35)
```
Workspace path rejected: write to `.claude/skills/${SKILL_X}-workspace/${REMAINDER}` blocked. Use `.dev/eval-workspaces/${SKILL_X}/${REMAINDER}` instead.

Reason: skill-creator's sibling-workspace convention places eval workspaces next to the skill directory under `.claude/skills/`, which mixes throwaway artifacts with the source-of-truth skill packages. This project relocates them under `.dev/eval-workspaces/<skill-name>/`. See `.dev/README.md` for the published convention, or run `make eval-skill SKILL=${SKILL_X}` to create the correct destination.
```

Two-paragraph structure: **(1)** specific source→destination redirect line,
**(2)** rationale + pointer to canonical docs + suggested fix command.

### Exit semantics
- Block path: `exit 2` (line 36) — Claude Code surfaces the stderr message and
  Claude is expected to retry the tool call against the redirected path.
- Allow path: `exit 0` (line 39).

---

## 2. Hook Registration Anatomy

### Source-of-truth registry: `src/superclaude/hooks/hooks.json`
The canonical hooks registry (95 lines, full file read) lists:
- `SessionStart` (lines 3–23): `session-init.sh`, `freshness-session-start.sh`
- `UserPromptSubmit` (24–34): `freshness-user-prompt.sh`
- **`PreToolUse` (35–46): ONLY `freshness-pre-edit.sh`** with matcher
  `Edit|Write|mcp__serena__replace_content|mcp__serena__replace_symbol_body|mcp__serena__insert_after_symbol|mcp__serena__insert_before_symbol`
- `PostToolUse` (47–69): `freshness-post-read.sh`, `auggie-flag-clear.sh`
- `SubagentStart` / `SubagentStop` (70–93): freshness hooks

**Notable finding:** `reject-workspace-writes.sh` is **NOT registered in
`src/superclaude/hooks/hooks.json`**. It only appears in
`.claude/settings.json`. This is either (a) an oversight in the
src-of-truth registry, or (b) an intentional choice to keep
`reject-workspace-writes` as a project-local-only hook outside the
distributable hook bundle. (Recent commit `efaa33d chore(hooks): resolve
OQ-2/OQ-3` on the current branch suggests the sync gap is being addressed.)

### Active registration: `.claude/settings.json`
The settings file (17 lines, full read) wires one PreToolUse entry:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "description": "Reject-with-redirect: writes to `.claude/skills/*-workspace/**` are denied with a message naming the correct destination `.dev/eval-workspaces/<skill>/<remainder>`. ...",
        "hooks": [
          { "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/reject-workspace-writes.sh",
            "timeout": 3 }
        ]
      }
    ]
  }
}
```

- **Matcher format:** pipe-separated tool name list (`Write|Edit`). Tools the
  hook should intercept; no MCP-symbol variants needed because Edit/Write are
  the only built-ins that take `file_path`.
- **Command path:** `$CLAUDE_PROJECT_DIR/.claude/hooks/<script>.sh` — relative
  to project root via the standard env var.
- **Description field:** carries full prose contract (matcher precision,
  source citation, semantics). This is the convention to follow for any new
  sibling hook.
- **Timeout:** 3 seconds (consistent with other fast-decision hooks).

---

## 3. PRD `SKILL.md` Output-Routing Prose

**File:** `src/superclaude/skills/prd/SKILL.md` (455 lines, full read)

### Output-path declarations
- **Line 43 (Input section #4):** "If creating from scratch, follow the project
  convention: `docs/docs-product/tech/[feature-name]/PRD_[FEATURE-NAME].md`."
- **Lines 95–131 (Output Locations section):** All persistent artifacts go
  into `.dev/tasks/to-do/TASK-PRD-YYYYMMDD-HHMMSS/`. Final PRD goes to
  `docs/docs-product/tech/[feature-name]/PRD_[FEATURE-NAME].md`. Template at
  `src/superclaude/examples/prd_template.md`. **No reference whatsoever to
  `prd-*/`, `prd-*-test/`, or any repo-root output.**
- **Line 257:** "Create the task folder: `.dev/tasks/to-do/TASK-PRD-YYYYMMDD-HHMMSS/`"
- **Line 421:** "Output paths and file naming conventions for all research,
  synthesis, and assembly artifacts" — generic, no concrete path.

### Test mode / dry-run awareness
- `grep -niE "prd-.*-test|prd-test|dry-run|test mode|prd-tmp"` against the
  full file → **zero matches**.
- The skill prompt **does not acknowledge any test-mode override** nor a
  CWD-relative output destination. There is no mention of the test harness
  (`tests/cli/prd/test_prompts.py`) or that an output override may be passed
  through fixtures.

### Convention awareness (CLAUDE.md plugin override)
- The skill is **silent on the skill-creator addendum / sibling-workspace
  override**. It does not reference `.dev/eval-workspaces/` either (which
  would be the natural target if PRD ever needed an eval workspace).
- Because the skill never instructs Claude to write under `prd-*-test/` at
  repo root, those paths can only arise from one of:
  1. The test harness (Track 1) leaking its temp prefix
  2. Claude improvising an output path when the skill's "OUTPUT location" is
     vague ("Where the final PRD goes")
  3. A previous run's residue not cleaned up

The hook layer should therefore catch (2) and (3) defensively, and Track 1
fixes (1) directly.

---

## 4. Skill-Creator Addendum Precedent (CLAUDE.md §"Plugin Override")

**Citation:** `CLAUDE.md` lines 108–116.

### Verbatim directives (the override)
- Line 110 (**Override**): "The `skill-creator` plugin (and any plugin
  following the same convention) creates an eval/iteration workspace as a
  **sibling to the skill directory** … **In this project that convention is
  overridden.**"
- Line 112 (**Destination rule**): "When invoking `skill-creator` or any plugin
  that uses a sibling-workspace convention, the eval workspace **MUST** be
  written to `.dev/eval-workspaces/<skill-name>/` … This applies regardless
  of any path the plugin itself suggests or attempts."
- Line 114 (**Rationale**): `.claude/skills/<skill-name>/` is reserved for
  the distributable skill package. "Anything generated by a skill's
  evaluation, debugging, or release workflow belongs under `.dev/`, never
  under `.claude/skills/`."
- Line 116 (**Authoritative source**): "Enforcement is layered: the PreToolUse
  hook in `.claude/settings.json` rejects writes to
  `.claude/skills/*-workspace/**` … and `.gitignore` matches
  `.claude/skills/*-workspace/` so any misplaced workspace cannot be committed."

### Analogous mapping for PRD
The PRD case is structurally identical:

| Aspect | skill-creator (existing) | PRD (proposed) |
|---|---|---|
| Anti-pattern path | `.claude/skills/<X>-workspace/<remainder>` | `<repo-root>/prd-*-test/<remainder>`, `<repo-root>/prd-*/<remainder>` |
| Canonical destination | `.dev/eval-workspaces/<X>/<remainder>` | `.dev/tasks/to-do/TASK-PRD-YYYYMMDD-HHMMSS/` (artifacts) or `docs/docs-product/tech/<feature>/PRD_<NAME>.md` (final) |
| Rationale | Distributable skill dir must not contain ephemeral output | Repo root must not contain ephemeral test/output dirs (pollutes git status, breaks `.gitignore`, leaks into commits) |
| Enforcement layers | PreToolUse hook + `.gitignore` | PreToolUse hook + (recommended) `.gitignore` addition for `prd-*/` and `prd-*-test/` |

The addendum's directive — "**MUST** be written to [canonical path] …
regardless of any path the plugin itself suggests or attempts" — translates
directly to PRD: a hook must override repo-root prd-* writes regardless of
what the test harness or improvising skill attempts.

---

## 5. Recommended Hook Approach

### Decision: **Option C** — generic `reject-skill-root-writes.sh` parameterized over prefix patterns

### Rationale
- **Option A (extend `reject-workspace-writes.sh`):** Tempting for proximity,
  but the existing script's contract is precisely scoped: "skill-creator
  sibling-workspace convention." Its filename, header comment (lines 1–13),
  and redirect message all reference `.claude/skills/*-workspace/` and
  `make eval-skill`. Adding a second concern (repo-root prd-*/ writes) would
  violate single-responsibility, complicate the redirect message format, and
  make the matcher logic harder to reason about. **Rejected.**
- **Option B (sibling `reject-prd-repo-root-writes.sh`):** Clean SRP, but
  PRD is unlikely to be the only skill that risks repo-root pollution.
  TDD, tech-research, task-builder, and roadmap all have similar slug-based
  output paths that an improvising agent could place at the root. Creating a
  per-skill hook for each is registry sprawl. **Rejected.**
- **Option C (generic `reject-skill-root-writes.sh`):** Matches the pattern
  established by `reject-workspace-writes.sh` (one hook, one concern: deny
  writes to anti-pattern paths with a clear redirect), but parameterized
  over a list of repo-root slug prefixes. Adding a future skill is one
  prefix entry. **Selected.**

### Script body (proposed, ~30 lines)

`src/superclaude/hooks/scripts/reject-skill-root-writes.sh`:

```bash
#!/usr/bin/env bash
# PreToolUse(Write|Edit) — reject-with-redirect for skill-generated
# repo-root output directories that should live under .dev/ instead.
#
# Decision contract:
#   - exit 0          → allow
#   - exit 2 + stderr → block; stderr surfaced to Claude
#
# Pattern: <repo-root>/<prefix>/<remainder> where <prefix> matches one of
# the listed skill-output anti-patterns. Subdirectories of legitimate
# locations (e.g. docs/, src/, .dev/) are NEVER matched because the regex
# is anchored to the start of a path segment that equals the project root.

set -u

# Repo-root anti-pattern prefixes (extend here for future skills).
PATTERNS=(
    'prd-[^/]*-test'   # PRD test-harness leakage (FU-003)
    'prd-[^/]+'        # PRD improvised repo-root output
    # 'tdd-[^/]*-test' # (future: TDD skill, when added)
)

INPUT="$(cat 2>/dev/null || true)"
TARGET="$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)"
[ -z "${TARGET:-}" ] && exit 0

# Resolve to absolute and strip the project root prefix so the regex
# matches only true repo-root segments (not e.g. docs/prd-foo/).
ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
REL="${TARGET#${ROOT}/}"

for PAT in "${PATTERNS[@]}"; do
    if [[ "$REL" =~ ^(${PAT})/(.*)$ ]]; then
        BAD_DIR="${BASH_REMATCH[1]}"
        REMAINDER="${BASH_REMATCH[2]}"
        cat >&2 <<EOF
Repo-root write rejected: \`${BAD_DIR}/${REMAINDER}\` would pollute the project root.

The PRD skill writes artifacts under \`.dev/tasks/to-do/TASK-PRD-YYYYMMDD-HHMMSS/\` and the final PRD under \`docs/docs-product/tech/<feature>/PRD_<NAME>.md\`. Test-harness output must use the tmp_path fixture, not a repo-root \`${BAD_DIR}/\` directory.

See \`src/superclaude/skills/prd/SKILL.md\` "Output Locations" section, and CLAUDE.md "Plugin Override — Skill-Creator Workspace Destination" for the canonical convention.
EOF
        exit 2
    fi
done

exit 0
```

### Registration
Add to `.claude/settings.json` `PreToolUse` array (and mirror into
`src/superclaude/hooks/hooks.json` — addressing the same source-of-truth gap
already raised in `hook-sync-and-matcher-fix`):

```json
{
  "matcher": "Write|Edit",
  "description": "Reject-with-redirect: writes to repo-root <skill-prefix>*/ directories (e.g. prd-foo/, prd-foo-test/) are denied with a redirect to the canonical .dev/ or docs/ destination. Extend PATTERNS in the script for new skills. Source: FU-003.",
  "hooks": [
    { "type": "command",
      "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/reject-skill-root-writes.sh",
      "timeout": 3 }
  ]
}
```

### Defense-in-depth recommendations (out of scope, noted for tracker)
1. Add `prd-*/` and `prd-*-test/` to repo-root `.gitignore` to match the
   skill-creator convention (CLAUDE.md line 116).
2. Track 1 (test harness) is the primary fix; this hook is the secondary
   guardrail. Both should land together.
3. Track 3 of `hook-sync-and-matcher-fix` should register
   `reject-workspace-writes.sh` in `src/superclaude/hooks/hooks.json`
   alongside the new `reject-skill-root-writes.sh` so `make verify-sync`
   covers both.

---

## Summary
- `reject-workspace-writes.sh` (40 lines) is a well-scoped PreToolUse hook
  using `exit 2 + stderr` semantics, a precise Bash regex
  (`\.claude/skills/([^/]+)-workspace/(.*)$`), and a two-paragraph redirect
  message format. It is registered in `.claude/settings.json` (line 10) but
  **not** mirrored in `src/superclaude/hooks/hooks.json` — a known gap.
- The PRD `SKILL.md` is **silent** on repo-root anti-patterns and test-mode
  output overrides; it never instructs Claude to write under `prd-*/`, so
  those paths arise from test-harness leakage or agent improvisation.
- The CLAUDE.md "Plugin Override" addendum (lines 108–116) establishes the
  exact precedent: PreToolUse hook + `.gitignore` to enforce a canonical
  destination "regardless of any path the plugin itself suggests or attempts."
- **Recommendation: Option C** — add a generic
  `src/superclaude/hooks/scripts/reject-skill-root-writes.sh`
  parameterized over a `PATTERNS` array (initially `prd-[^/]*-test`,
  `prd-[^/]+`), register in both `.claude/settings.json` and
  `src/superclaude/hooks/hooks.json`, and document the matching `.gitignore`
  addition.
