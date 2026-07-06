# R2 — Patterns & Conventions (Skill / Command / Hook)

**Status: In Progress**

Research for building `sc:submit-pr` skill package + command + hook edit.
Topic: SKILL.md structure, refs/ organization, scripts/ wiring, command frontmatter schema,
hook script conventions, SoT sync discipline. All findings evidence-cited with file:line.

**Closest analog for `sc:submit-pr`:** `sc-auggie-review-protocol` (PR-oriented, gh-shelling,
remediation handoff, hook-driven via `offer-pr-review.sh`). Mirror it for structure; mirror
`sc-bare-review` for the `scripts/` orchestration pattern.

---

## 1. SKILL.md Structure & Frontmatter

### 1.1 Frontmatter schema (two flavors observed)

**Flavor A — minimal frontmatter + HTML-comment extended metadata** (used by the richest
protocol skills: auggie-review, troubleshoot). Only `name`, `description`, `allowed-tools`
are real parsed YAML; everything else (category/complexity/mcp-servers/personas) lives in an
HTML comment block explicitly marked "not parsed".

Evidence — `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:1-12`:
```yaml
---
name: sc:auggie-review-protocol
description: "Auggie-powered code review protocol for PRs, local diffs, and file snapshots — ..."
allowed-tools: Read, Grep, Glob, Bash(auggie *), Bash(gh *), Bash(git *), Bash(jq *), Bash(wc *), Bash(find *), Bash(mkdir *), Bash(cat *), Bash(mv *), Bash(cp *), Bash(date *), TodoWrite, Task, Write, Edit, Skill
---

<!-- Extended metadata (for documentation, not parsed):
category: quality
complexity: advanced
mcp-servers: [sequential, serena, auggie]
personas: [analyzer, architect, security, qa, refactorer]
-->
```
Note: `allowed-tools` uses **scoped Bash globs** — `Bash(gh *)`, `Bash(git *)`, `Bash(jq *)`,
etc. This is the pattern to copy for `sc:submit-pr` (which needs `Bash(gh *)`, `Bash(git *)`).

`src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:1-12` — same flavor, but
`allowed-tools` also lists MCP tools inline (`mcp__auggie__codebase-retrieval`,
`mcp__serena__find_symbol`, ...). The HTML-comment metadata block sits below frontmatter.

**Flavor B — full YAML frontmatter** (used by cli-portify, bare-review). All metadata is real
frontmatter; no HTML comment.

Evidence — `src/superclaude/skills/sc-cli-portify-protocol/SKILL.md:1-10`:
```yaml
---
name: sc-cli-portify-protocol
description: "Full behavioral protocol for sc:cli-portify — ..."
category: development
complexity: high
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task
mcp-servers: [sequential, serena, context7, auggie-mcp]
personas: [architect, analyzer, backend]
argument-hint: "--workflow <skill-name-or-path> [--name <cli-name>] [--output <dir>] [--dry-run]"
---
```

Evidence — `src/superclaude/skills/sc-bare-review/SKILL.md:1-6` adds a `model:` key:
```yaml
---
name: sc-bare-review
description: Infrastructure skill that dispatches 2-4 bare ... Delegate-only — no slash command.
allowed-tools: Read, Glob, Grep, Bash, Write
model: sonnet
---
```

**`name:` convention quirk:** auggie-review uses `name: sc:auggie-review-protocol` (colon),
troubleshoot uses `name: sc:troubleshoot-protocol` (colon), cli-portify uses
`name: sc-cli-portify-protocol` (hyphen), bare-review uses `name: sc-bare-review` (hyphen,
no `-protocol`). The directory name is always hyphenated (`sc-auggie-review-protocol/`). The
`sc:` vs `sc-` in the `name:` field is inconsistent across the repo; the **directory name**
is the load-bearing identifier. **Recommendation for submit-pr:** directory
`src/superclaude/skills/sc-submit-pr-protocol/`, frontmatter `name: sc:submit-pr-protocol`,
matching the auggie-review (PR-sibling) convention.

### 1.2 Section ordering (canonical, from auggie-review)

Observed top-level section sequence in `sc-auggie-review-protocol/SKILL.md`:
1. `# <Title>` (line 14)
2. `## Purpose` (line 16) — includes bolded "contract" paragraphs (token-efficiency,
   hallucination contracts) at `:20,:22`
3. `## Required Input (STOP if missing)` (line 24) — a markdown table of modes + a bulleted
   **STOP** list (`:34`) and **WARN (proceed)** list (`:41`)
4. `## Output Contract` (line 48) — a `| Field | Type | Description |` table (`:51`)
5. `## Wave Structure` (line 62) — a fenced ASCII diagram listing waves + which ref each loads
6. Per-wave `### Wave N: <name>` sections (`:76`, `:110`, `:134`, `:198`, `:297`) each with
   **Preconditions / Steps / Exit criteria / Failure handling** sub-structure
7. `## Will Do` (line 336) / `## Will Not Do` (line 346) — bulleted boundary lists
8. `## Error Handling` (line 357) — scenario→behavior→fallback table
9. `## Token Cost Profile` (line 370) — depth→cost table

troubleshoot mirrors this (`## Purpose`, `## Required Input (STOP if missing)`,
`## Output Contract`, `## Wave Structure`) — `SKILL.md:14,26,38,77`.

cli-portify uses `## Purpose` → `## What Gets Generated` → `## Required Input` →
`## Behavioral Flow` (with `### Phase N`) → `## Boundaries` (Will Do / Will Not Do) →
`## Return Contract Schema` (`cli-portify SKILL.md:16,30,53,68,444,462`).

**Wave/Phase lazy-ref-loading is a hard convention.** Each wave header states which ref to
load *at that point*, never pre-loaded. Evidence — `sc-auggie-review-protocol/SKILL.md:64`:
"Refs are loaded **per-wave**, never pre-loaded." and `:136` "**Load `refs/auggie-prompts.md`**",
`:149` "Read `refs/auggie-prompts.md` (NOT before now — lazy loading)."

### 1.3 Output Contract pattern

A structured dict/table returned on **every** invocation including failure. auggie-review's is
a `| Field | Type | Description |` table at `SKILL.md:51-60` (status / report_path /
audit_log_path / pr_review_url / findings_count / dropped_count / remediation_offered /
remediation_accepted). cli-portify formalizes this as a full YAML `## Return Contract Schema`
with `contract_version`, failure-type enumeration, and failure-path defaults
(`cli-portify SKILL.md:462-577`). For `sc:submit-pr`, copy auggie-review's lighter table form
unless R5/R7 require the richer YAML schema.

---

## 2. refs/ Organization & Cross-Linking

### 2.1 Layout

Each protocol skill keeps a flat `refs/` directory of `.md` files, one per behavioral concern.
Observed trees:

- `sc-troubleshoot-protocol/refs/`: `calibrator-eval-cases.md`, `diagnosability-audit.md`,
  `doc-discovery.md`, `escalation-rubric.md`, `hypothesis-card-template.md`,
  `remediation-handoff.md`, `report-template.md`, `triage-checklist.md` (8 refs).
- `sc-auggie-review-protocol/refs/`: `auggie-prompts.md`, `remediation-handoff.md`,
  `severity-rubric.md` (3 refs) + a sibling `evals/evals.json`.
- `sc-cli-portify-protocol/refs/`: `analysis-protocol.md`, `code-templates.md`,
  `pipeline-spec.md` (3 refs).
- `sc-bare-review/refs/`: `output-template.md`, `prompts.md`, plus a nested
  `refs/templates/bare-review-output.md`.

**Naming convention:** kebab-case, named by *function* — `<concern>-rubric.md`,
`<concern>-template.md`, `<concern>-checklist.md`, `<concern>-handoff.md`, `<concern>-prompts.md`.

### 2.2 Cross-linking from SKILL.md → refs

Refs are referenced **inline within the wave that consumes them**, with a bold "Load" verb and
an explicit "not before now" note. Canonical pattern:

- Wave-Structure ASCII map annotates each wave with its ref —
  `sc-auggie-review-protocol/SKILL.md:66-72`:
  ```
  Wave 2: Auggie Deep Pass     ← loads refs/auggie-prompts.md
  Wave 3: Validate & Synthesize ← loads refs/severity-rubric.md
  Wave 4: Post & Handoff       ← loads refs/remediation-handoff.md
  ```
- The wave body re-states it as a **Preconditions** line: `SKILL.md:136` "**Load
  `refs/auggie-prompts.md`** for the structured prompt templates." and a Step: `:149`
  "Read `refs/auggie-prompts.md` (NOT before now — lazy loading)."
- `:200` "**Load `refs/severity-rubric.md`**", `:299` "**Load `refs/remediation-handoff.md`**".

cli-portify uses the same pattern with Phase wording — `cli-portify SKILL.md:73` "Load
`refs/analysis-protocol.md` before this phase. It contains the discovery checklist..." and
`:109` "Load `refs/pipeline-spec.md` before this phase."

### 2.3 Ref file internal structure

A ref is a focused `.md` with an `# H1` title and explanatory prose + fenced templates.
Evidence — `sc-auggie-review-protocol/refs/remediation-handoff.md:1-3`: starts `# Remediation
Handoff`, then a one-paragraph "what this pins" intro, then `## When the offer fires` (`:5`)
with numbered conditions, then `## The offer prompt (exact text)` (`:16`) with a verbatim
fenced ```text block the skill emits to the user. This "pin the exact wording in a ref" pattern
is directly reusable for a `sc:submit-pr` PR-body template / confirmation-prompt ref.

**Template-ref idiom:** when a ref IS a template, the file is named `*-template.md` and the
SKILL loads it at the synthesis wave (e.g. troubleshoot `refs/report-template.md` loaded at
Wave 5, `troubleshoot SKILL.md:88`).

---

## 3. scripts/ Wiring (the bare-review pattern)

Only `sc-bare-review` and `sc-cli-portify-protocol` bundle a `scripts/` dir.
`sc-bare-review/scripts/` is the cleanest, most replicable model for `sc:submit-pr` if it needs
deterministic shell helpers (gh/git probing, PR-body assembly).

### 3.1 Layout & roles

`sc-bare-review/scripts/`: `t2_preflight.sh`, `t2_dispatch.sh`, `t2_normalize.py` (+ a
`__pycache__/`). The SKILL describes the split explicitly — `sc-bare-review/SKILL.md:34-37`:
"A thin orchestrator over three bundled scripts ... The scripts own the deterministic work;
this SKILL.md owns sequencing and the single-message parallel dispatch."

### 3.2 How SKILL invokes scripts — `$SKILL_DIR` convention

Scripts are called via a `$SKILL_DIR/scripts/<name>` path. Evidence —
`sc-bare-review/SKILL.md:88-92` (preflight), `:112-118` (dispatch), `:125-127` (normalize):
```bash
"$SKILL_DIR/scripts/t2_preflight.sh" --target <target> --reviewers <N> --output <output-dir> ...
```
Python is run through UV per project rule — `SKILL.md:126-127`:
```bash
# Project rule (CLAUDE.md): all Python runs through UV — never bare `python3 script.py`.
uv run python "$SKILL_DIR/scripts/t2_normalize.py" --manifest "<output-dir>/manifest.json"
```

### 3.3 Script internal conventions (from `t2_preflight.sh`)

`sc-bare-review/scripts/t2_preflight.sh` is the gold-standard template for a bundled shell
helper:
- `#!/usr/bin/env bash` shebang (`:1`), a header-comment block describing purpose + usage +
  exit codes + spec citation (`:2-18`), and **`# Source of truth lives in src/superclaude/;
  do not edit the .claude/ mirror.`** (`:18`) — a SoT reminder baked into the script itself.
- `set -euo pipefail` (`:20`) — note: stricter than the hooks, which use `set -u` only.
- `die() { printf 'sc-bare-review: %s\n' "$1" >&2; exit "${2:-1}"; }` helper (`:22`).
- Manual `while/case` arg parser over `--flag value` (`:28-38`).
- Toolchain guards: `command -v curl >/dev/null 2>&1 || die "..."` (`:41-42`) — the same
  `command -v` STOP pattern the auggie-review SKILL uses for `auggie`/`gh`.
- Env-var resolution with defaults (`:57-64`), absolute-path normalization
  (`TARGET_ABS="$(cd "$(dirname "$TARGET")" && pwd)/$(basename "$TARGET")"`, `:80`).
- Emits a `manifest.json` via `jq -n --arg ...` (`:199-216`) that the SKILL then `Read`s to
  drive subsequent steps — clean script↔skill data handoff.

**For `sc:submit-pr`:** a `scripts/submit_pr_preflight.sh` doing `git`/`gh` validation
(remote check, branch-ahead check, rebase detection per CLAUDE.md PR rules) and emitting a
manifest the SKILL reads is the idiomatic shape. If logic is light, it can live inline in the
SKILL's Bash steps instead (auggie-review has NO scripts/ — it inlines all gh/git Bash).

---

## 4. Command File (`src/superclaude/commands/*.md`) Conventions

### 4.1 Frontmatter schema

The command frontmatter is **richer** than the SKILL's and always full-YAML (no HTML comment).
Canonical fields, from `src/superclaude/commands/auggie-review.md:1-9`:
```yaml
---
name: auggie-review
description: "Auggie-powered code review for PRs, local diffs, or file snapshots — ..."
category: quality
complexity: advanced
mcp-servers: [sequential, serena]
personas: [analyzer, architect, security, qa, refactorer]
argument-hint: "[<PR-num|PR-URL>|--diff <base>...HEAD|--snapshot <path>] [--focus ...] [--depth ...] [--post-pr|--no-post-pr] [--remediation-offer|--no-remediation-offer]"
---
```
Key differences from SKILL frontmatter:
- `name:` is the **bare command** (`auggie-review`, NOT `sc:auggie-review` and NOT
  `sc-...-protocol`). The `/sc:` prefix is implied by install location, not the `name:` field.
- `argument-hint:` is mandatory-ish — a one-line usage signature with all flags. Present in
  auggie-review (`:8`), cli-portify (`commands/cli-portify.md` lacks it but uses an `## Usage`
  fenced block instead). cli-portify command frontmatter adds `version: "1.0.0"` (`:9`).

cli-portify command frontmatter — `src/superclaude/commands/cli-portify.md:1-10`:
```yaml
---
name: cli-portify
description: "Port inference-based SuperClaude workflows into programmatic CLI pipelines ..."
category: development
complexity: high
allowed-tools: Read, Glob, Grep, Write, Bash, TodoWrite, Skill
mcp-servers: [sequential, serena, context7]
personas: [architect, analyzer, backend]
version: "1.0.0"
---
```

### 4.2 Command body sections (canonical from auggie-review.md)

Section sequence in `commands/auggie-review.md`:
1. `# /sc:auggie-review - <tagline>` (line 11)
2. `## Triggers` (line 13) — for explicit-only commands, states "Explicit only" + enumerates
   the 3 activation paths (direct / hook / programmatic). `:15-21`. **This is where the
   hook→command linkage is documented** (`:18`: "PR-creation hook: After `gh pr create`
   succeeds, the `offer-pr-review.sh` hook prompts...").
3. `## Required Input` (line 23) with **STOP** clause `:31`.
4. `## Usage` (line 33) — fenced block of example invocations.
5. `## Options` (line 44) — `| Flag | Default | Description |` table.
6. `## Behavioral Flow` (line 57) — explicitly states the command does ONLY parse/validate/
   handoff, the protocol lives in the skill (`:59`).
7. `## Activation` (line 66) — **THE critical delegation section** (see 4.3).
8. `## MCP Integration` (line 73), `## Tool Coordination` (line 80), `## Examples` (line 90),
   `## Boundaries` (Will / Will Not, line 141), `## Related Commands` (line 163).

cli-portify command is leaner — `# /sc:cli-portify` → `## Triggers` → `## Usage` →
`## Arguments` table → `## Input Validation` (error-code list) → `## Activation` →
`## Examples` → `## Boundaries` (`commands/cli-portify.md:12,17,21,30,46,77,94,109`).

### 4.3 How the command delegates to its protocol skill (`## Activation`)

This is the load-bearing convention. The command file is a thin shim; the body MUST contain an
`## Activation` section that invokes the skill with a **MANDATORY** marker and a blockquote
`> Skill <skill-name>` line.

Evidence — `commands/auggie-review.md:66-71`:
```markdown
## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:auggie-review-protocol

Do NOT proceed with protocol execution using only this command file. The full behavioral
specification — Auggie invocation, finding validation, severity rubric, PR posting,
remediation handoff — is in the protocol skill.
```

Evidence — `commands/cli-portify.md:76-91`:
```markdown
## Activation

**Classification**: STRICT -- multi-file code generation operation with API conformance requirements.

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:cli-portify-protocol

Pass the following context:
- Workflow path: ...
- CLI name: ...
...
Do NOT attempt to execute portification using only this command file.
```

**Pattern for `sc:submit-pr`:** command `name: submit-pr`, an `## Activation` with
`> Skill sc:submit-pr-protocol`, and a "Pass the following context:" bullet list of the parsed
flags. The command does arg-parse + env-validate + handoff only.

This is reinforced by the project ABSOLUTE RULE in `CLAUDE.md` ("Custom Command Skill
Invocation"): when a message starts with `/sc:<command>`, the skill MUST be invoked before any
other output — the `## Activation` block is what encodes that contract in the command file.

---

## 5. Hook Script Conventions (`src/superclaude/hooks/scripts/`)

Three hooks studied: `offer-pr-review.sh` (PostToolUse/Bash, fail-open emit),
`reject-workspace-writes.sh` (PreToolUse/Write|Edit, blocking deny), `freshness-file-changed.sh`
(state-tracking, async). `sc:submit-pr` will most likely **edit/extend `offer-pr-review.sh`**
(it already fires on `gh pr create`) — that script is the direct integration point.

### 5.1 Common skeleton (all hooks share this)

1. `#!/usr/bin/env bash` shebang.
2. A header comment block documenting: the hook event it binds to, the **stdin JSON schema**,
   and the **exit-code contract**. Evidence — `offer-pr-review.sh:1-13`,
   `reject-workspace-writes.sh:1-13`, `freshness-file-changed.sh:1-20`.
3. `set -u` (hooks use the looser `set -u`, NOT `set -euo pipefail` — because a `jq` miss or
   grep-no-match must not abort the hook; fail-open). Evidence — `offer-pr-review.sh:15`,
   `reject-workspace-writes.sh:15`, `freshness-file-changed.sh:21`.
4. Read stdin: `INPUT="$(cat 2>/dev/null || true)"`. Evidence —
   `offer-pr-review.sh:17`, `reject-workspace-writes.sh:17`, `freshness-file-changed.sh:28`.

### 5.2 The exit-code contract (documented in every hook header)

- **exit 0** = pass-through / allow. If stdout is non-empty, Claude Code surfaces it as
  *additional context* for the next turn. Evidence — `offer-pr-review.sh:6-7`.
- **exit 2** = block the tool; stderr is surfaced to Claude as the deny reason. Evidence —
  `reject-workspace-writes.sh:8-9` and the two deny branches `exit 2` at `:36,:61`.
- PostToolUse hooks that observe (don't gate) always end `exit 0` — `offer-pr-review.sh:74`.

### 5.3 Cheap prefilter before expensive jq (mandatory performance idiom)

`offer-pr-review.sh:19-21`:
```bash
# Cheap prefilter: bail out immediately if the payload doesn't even mention `gh pr create`.
# Saves three jq invocations on every non-matching Bash tool call.
case "$INPUT" in *'"command"'*'gh'*'pr'*'create'*) ;; *) exit 0;; esac
```
A glob `case` over the raw stdin string short-circuits before any `jq`. **Copy this** for any
new prefilter in `sc:submit-pr` hook logic.

### 5.4 stdin JSON field extraction via jq

`offer-pr-review.sh:24,27,38,43`:
```bash
TOOL_NAME="$(printf '%s' "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)"
CMD="$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)"
TOOL_ERROR="$(printf '%s' "$INPUT" | jq -r '.tool_response.error // empty' 2>/dev/null)"
TOOL_STDOUT="$(printf '%s' "$INPUT" | jq -r '.tool_response.stdout // .tool_response.output // empty' ...)"
```
PreToolUse payload uses `.tool_input.file_path` — `reject-workspace-writes.sh:20`. Every `jq`
has `2>/dev/null` and a `// empty` default → fail-open.

### 5.5 Fail-open discipline (explicit)

`reject-workspace-writes.sh:22-23`: "No path → cannot enforce → allow (fail-open)." then
`[ -z "${TARGET:-}" ] && exit 0`. `freshness-file-changed.sh:9` notes "Fail-open per NFR-3."
The rule: **if the hook cannot confidently determine it should act, it exits 0 and gets out of
the way.** A `sc:submit-pr` hook (e.g. detecting `gh pr create` to offer a follow-up) MUST be
fail-open.

### 5.6 Precise command matching (avoid false positives)

`offer-pr-review.sh:33` uses a bash regex to match `gh pr create` while allowing flags between
`gh` and `pr create`, and explicitly NOT matching `gh pr view`/`gh pr list`:
```bash
if ! [[ "$CMD" =~ (^|[[:space:]\;\&\|])gh([[:space:]]+-[^[:space:]]+)*[[:space:]]+pr[[:space:]]+create([[:space:]]|$) ]]; then
    exit 0
fi
```

### 5.7 Emitting an "offer" to the user (the relay pattern)

When a PostToolUse hook wants the assistant to ask the user something, it prints a fenced
pseudo-XML block to stdout with **exact framing the assistant must not paraphrase**, plus a
"wait for confirmation, do not auto-invoke" instruction. Evidence —
`offer-pr-review.sh:60-72` (`<sc-auggie-review-offer ...>` block with the verbatim question and
`:70` "Do not auto-invoke ... without confirmation. If the user declines, do not bring it up
again in this session."). **This is the exact mechanism `sc:submit-pr` would extend** — either
add a new offer block, or chain the submit→review offer.

### 5.8 Hook registration in `.claude/settings.json` (the ONE tracked .claude file)

Hooks are registered under `hooks.<Event>[].hooks[]` with a `matcher`, a human `description`,
and a `command` pointing at `$CLAUDE_PROJECT_DIR/.claude/hooks/<name>.sh` + `timeout`.
Evidence — `.claude/settings.json:3-39`:
```json
"PreToolUse": [
  { "matcher": "Write|Edit", "description": "...", 
    "hooks": [ { "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/reject-workspace-writes.sh", "timeout": 3 } ] },
  { "matcher": "Skill", "description": "...sc-recommend...",
    "hooks": [ { "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/sc-recommend-phase0.sh", "timeout": 3 } ] }
],
"PostToolUse": [
  { "matcher": "Bash", "description": "After a successful `gh pr create`, emit an offer...",
    "hooks": [ { "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/offer-pr-review.sh", "timeout": 3 } ] }
]
```
CRITICAL PATH NOTE: the `command` points at `.claude/hooks/<name>.sh` (the synced/installed
location, flat — NOT `.claude/hooks/scripts/`), while the **source** lives at
`src/superclaude/hooks/scripts/<name>.sh`. The `timeout` is `3` (seconds) for all three.
The `description` field is verbose and names the source SKILL/spec.

**`.claude/settings.json` IS tracked in git** (it is the sole exception to the .claude
gitignore — see §6). So a hook EDIT for `sc:submit-pr` touches BOTH
`src/superclaude/hooks/scripts/<name>.sh` (source, run `make sync-dev`) AND, if a new hook is
registered, `.claude/settings.json` (tracked, edited directly + staged). Verify whether
`make sync-dev` also copies hooks — see open question in §7.

---

## 6. SoT Sync Discipline (`src/` → `make sync-dev` → `.claude/`)

**The rule:** `src/superclaude/` is the canonical source of truth for all distributable
components (skills, agents, commands, hooks, templates). Edit there FIRST, then
`make sync-dev` copies to `.claude/`. Never edit `.claude/` directly without syncing back.

Evidence — project `CLAUDE.md:141`: "**Source of truth**: `src/superclaude/` is the canonical
location for all distributable components". `CLAUDE.md:122-123`:
```
make sync-dev         # Copy src/superclaude/{skills,agents} → .claude/
make verify-sync      # Check src/ and .claude/ are in sync (CI-friendly)
```
Workflow `CLAUDE.md:146-149`: edit `src/superclaude/skills/` or `.../agents/`, run
`make sync-dev`, run `make verify-sync` (also before committing).

Global `~/.claude/CLAUDE.md:47`: "Source of truth is `src/superclaude/`. Always edit there
first, then `make sync-dev`." and Core Rule 6 (`:83`): "**Component edits** —
`src/superclaude/` → `make sync-dev` → `.claude/`; never reverse without syncing back".

**The never-stage-.claude rule (ABSOLUTE):** project `CLAUDE.md:16-31`:
- `:18`: "`.claude/{skills,commands,agents,hooks,templates}/*` is **gitignored sync-dev
  output** of `src/superclaude/`. The ONLY tracked file under `.claude/` is
  `.claude/settings.json`."
- `:22`: NEVER `git add .claude/skills/...`, `.claude/commands/...`, `.claude/agents/...`,
  `.claude/hooks/...`, `.claude/templates/...`.
- `:27` ("The `-f` rule"): "If `git add` requires `-f` on any `.claude/` path, that `-f` is the
  violation siren. STOP. Move the change to `src/superclaude/` first, run `make sync-dev`, and
  stage only the `src/` side."
- `:31`: enforcement is the gitignore (`.claude/` + `!.claude/settings.json`) + pre-commit
  `verify-sync` local hook.

**Net staging rule for `sc:submit-pr` deliverables:**
- Stage: `src/superclaude/skills/sc-submit-pr-protocol/**`, `src/superclaude/commands/submit-pr.md`,
  `src/superclaude/hooks/scripts/<hook>.sh`, and `.claude/settings.json` (if a hook is
  registered — the ONE allowed `.claude/` path).
- NEVER stage: any `.claude/skills/`, `.claude/commands/`, `.claude/hooks/` mirror — those are
  `make sync-dev` output.
- Run `make sync-dev` after editing `src/`, then `make verify-sync` before committing.

---

## 7. Replicable Templates & Open Questions for the Builder

### 7.1 File set to create (mirroring auggie-review)

| New file | Mirror source | Notes |
|----------|---------------|-------|
| `src/superclaude/skills/sc-submit-pr-protocol/SKILL.md` | `sc-auggie-review-protocol/SKILL.md` | Flavor-A frontmatter; `allowed-tools` incl. `Bash(gh *)`, `Bash(git *)`; Wave structure; Output Contract table |
| `src/superclaude/skills/sc-submit-pr-protocol/refs/*.md` | auggie-review `refs/remediation-handoff.md` | e.g. `pr-body-template.md`, `preflight-checklist.md` — kebab-case, function-named, lazy-loaded per wave |
| `src/superclaude/skills/sc-submit-pr-protocol/scripts/*.sh` (optional) | `sc-bare-review/scripts/t2_preflight.sh` | `set -euo pipefail`, `die()`, `command -v` guards, abs-path norm, `jq -n` manifest, SoT reminder comment |
| `src/superclaude/commands/submit-pr.md` | `commands/auggie-review.md` | Full-YAML frontmatter, `name: submit-pr`, `argument-hint`, `## Triggers`/`## Activation` with `> Skill sc:submit-pr-protocol` |
| Hook edit: `src/superclaude/hooks/scripts/offer-pr-review.sh` (extend) OR new `<name>.sh` | `offer-pr-review.sh` | `set -u`, stdin `cat`, glob prefilter, `jq // empty`, fail-open, exit 0/2 contract |
| `.claude/settings.json` (edit, ONLY if new hook) | existing PostToolUse block `:27-39` | matcher + description + `$CLAUDE_PROJECT_DIR/.claude/hooks/<name>.sh` + `timeout:3` |

### 7.2 Open questions to resolve before building

1. **Does `make sync-dev` copy `hooks/`?** `CLAUDE.md:122` only names `{skills,agents}`; global
   `:37` names `{skills,agents,commands}`. Neither lists `hooks`. The hooks clearly DO get to
   `.claude/hooks/` (settings.json references them), so SOME sync path exists. The builder must
   grep the `Makefile` `sync-dev` target to confirm hooks are synced (R1/R4 territory) — do
   NOT assume. (This R2 pass did not read the Makefile; flagged as a dependency.)
2. **`.claude/hooks/` is flat, source is `hooks/scripts/`** — confirm the sync flattens
   `scripts/` → `.claude/hooks/`. (settings.json points at `.claude/hooks/<name>.sh`, source is
   `src/superclaude/hooks/scripts/<name>.sh`.)
3. Whether submit-pr should EXTEND `offer-pr-review.sh` (already fires on `gh pr create`) or be
   a separate pre-create flow — depends on R5 (integration) / spec §2.

---

**Status: Complete**

## Summary

Researched skill/command/hook conventions by reading auggie-review (closest analog),
cli-portify, troubleshoot, and bare-review packages plus three hooks and `.claude/settings.json`.

**Key findings (all file:line cited above):**
- **SKILL.md**: two frontmatter flavors — Flavor A (minimal `name`/`description`/`allowed-tools`
  + HTML-comment metadata, used by auggie-review/troubleshoot) vs Flavor B (full YAML, used by
  cli-portify/bare-review). `allowed-tools` uses scoped Bash globs `Bash(gh *)`. Canonical
  section order: Purpose → Required Input (STOP) → Output Contract table → Wave Structure →
  per-wave Preconditions/Steps/Exit → Will/Will-Not → Error Handling. Refs are LAZY-loaded
  per-wave, never pre-loaded.
- **refs/**: flat, kebab-case, function-named (`*-rubric.md`, `*-template.md`, `*-handoff.md`);
  cross-linked inline at the consuming wave with a bold "Load `refs/X.md`" verb; a ref can pin
  verbatim user-facing text (auggie-review's `remediation-handoff.md`).
- **scripts/**: `$SKILL_DIR/scripts/<name>` invocation; Python via `uv run python`; bare-review's
  `t2_preflight.sh` is the gold template (`set -euo pipefail`, `die()`, `command -v` guards,
  abs-path norm, `jq -n` manifest handed back to the SKILL via Read, SoT reminder comment).
  auggie-review has NO scripts/ — inlines all gh/git Bash, a valid lighter option.
- **command files**: full-YAML frontmatter, `name:` is the BARE command (`auggie-review`),
  `argument-hint:` one-liner. Body MUST have an `## Activation` section with `**MANDATORY**` +
  `> Skill sc:<name>-protocol` blockquote — the command is a thin parse/validate/handoff shim.
  `## Triggers` is where hook→command linkage is documented.
- **hooks**: `set -u` (NOT pipefail — fail-open), stdin `cat`, glob `case` prefilter before jq,
  `jq -r '... // empty' 2>/dev/null`, exit 0 = pass/emit-context, exit 2 = block (stderr =
  reason). `offer-pr-review.sh` already fires on `gh pr create` and emits a verbatim user-offer
  block — the direct integration point for submit-pr. Registered in `.claude/settings.json`
  (the ONE tracked .claude file) via matcher+description+`$CLAUDE_PROJECT_DIR/.claude/hooks/<name>.sh`+`timeout:3`.
- **SoT**: edit `src/superclaude/` → `make sync-dev` → `.claude/` → `make verify-sync` before
  commit. NEVER `git add .claude/{skills,commands,agents,hooks,templates}` (gitignored sync
  output); `.claude/settings.json` is the SOLE tracked exception. The `-f` siren rule applies.

**Flagged dependency (not resolved in R2):** confirm via Makefile that `make sync-dev` copies
`hooks/scripts/` → `.claude/hooks/` (flattening `scripts/`) — `CLAUDE.md` doc lists only
skills/agents/commands. Builder must verify before relying on hook sync (R1/R4).
