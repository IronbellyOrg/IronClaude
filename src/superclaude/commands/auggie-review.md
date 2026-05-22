---
name: auggie-review
description: "Auggie-powered code review for PRs, local diffs, or file snapshots — narrow bugs + architectural risks + anti-patterns, with auto-posted PR review and optional remediation handoff"
category: quality
complexity: advanced
mcp-servers: [sequential, serena]
personas: [analyzer, architect, security, qa, refactorer]
argument-hint: "[<PR-num|PR-URL>|--diff <base>...HEAD|--snapshot <path>] [--focus security,architecture,quality,performance,all] [--depth quick|standard|deep] [--post-pr|--no-post-pr] [--remediation-offer|--no-remediation-offer]"
---

# /sc:auggie-review - Auggie-Powered Code Review

## Triggers

**Explicit only** — this command does NOT auto-activate from conversational keywords like "review", "audit", or "check". It activates only via:

1. **Direct invocation**: User types `/sc:auggie-review ...`
2. **PR-creation hook**: After `gh pr create` succeeds, the `offer-pr-review.sh` hook prompts the user; if the user accepts, the assistant invokes this command
3. **Programmatic call**: Another `/sc:*` command invokes the `sc:auggie-review-protocol` skill directly

The trigger discipline exists because deep reviews are expensive (Auggie indexing + multi-persona synthesis) and false-positive activation in mid-conversation wastes user time. See "Boundaries → Will Not" below.

## Required Input

**MANDATORY**: One of the following review targets:

- **Remote PR**: `<PR-number>` or `<PR-URL>` (resolved via `gh pr view`)
- **Local diff**: `--diff <base-ref>...HEAD` (or implicit `--diff origin/<default-branch>...HEAD` if no target given and a dirty working tree is detected)
- **File snapshot**: `--snapshot <path>` (single file or directory; no diff, full-content review)

**STOP** if none of the above are resolvable. Do not invent a target.

## Usage

```bash
/sc:auggie-review 62                                    # Review PR #62 (auto-detect repo)
/sc:auggie-review https://github.com/org/repo/pull/62   # Review PR by URL
/sc:auggie-review --diff origin/master...HEAD           # Review local branch changes
/sc:auggie-review --snapshot src/superclaude/cli/       # Review a subtree (no diff)
/sc:auggie-review 62 --focus security,architecture      # Focus areas only
/sc:auggie-review 62 --depth deep --no-post-pr          # Deep review, do not post to PR
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--focus` | `all` | Comma-separated subset of `security,architecture,quality,performance,anti-patterns,tests,docs,all` |
| `--depth` | `standard` | `quick` (auggie single-pass, ~2min), `standard` (auggie + Claude synthesis, ~5min), `deep` (auggie + per-persona Claude passes + cross-reference, ~10-15min) |
| `--post-pr` | `true` when target is a PR | Auto-post the markdown report as a `gh pr review --comment`. Inline comments for `Critical` and `High` findings via `gh api`. **No confirmation prompt — the user opted in by invoking the command on a PR.** |
| `--no-post-pr` | — | Generate the report only; do not touch GitHub |
| `--remediation-offer` | `true` | After the review completes, offer to chain `/sc:design` → `task-builder` → `/sc:reflect --type task --analyze` → execute → `/sc:reflect --type task --validate` |
| `--no-remediation-offer` | — | Suppress the remediation chain offer |
| `--output-dir` | `.dev/reviews/<target-slug>-<timestamp>/` | Where to write the markdown report, raw auggie JSON, and audit log |
| `--auggie-model` | (auggie default) | Override the model auggie uses (e.g., `--auggie-model claude-sonnet-4-6`) |

## Behavioral Flow

The full multi-wave protocol lives in the skill. The command file performs only:

1. **Parse arguments** → resolve target type (PR / diff / snapshot)
2. **Validate environment** → `auggie` on PATH, `gh` authed (if PR target), repo is a git working tree
3. **Hand off to the skill** via the Activation section below
4. **On skill return**, surface the report path, PR URL (if posted), and remediation-chain prompt (if enabled)

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:auggie-review-protocol

Do NOT proceed with protocol execution using only this command file. The full behavioral specification — Auggie invocation, finding validation, severity rubric, PR posting, remediation handoff — is in the protocol skill.

## MCP Integration

- **Sequential**: Multi-step synthesis when reconciling Auggie findings with Claude's diff-level checks
- **Serena**: Symbol-level cross-reference when validating Auggie's file:line citations against actual code

External tool (not MCP, but central): **`auggie` CLI** is the primary review engine. The skill shells out to `auggie --print --output-format json --ask` to offload deep analysis to Auggie's indexed codebase context, dramatically reducing Claude token consumption.

## Tool Coordination

- **Bash(auggie *)**: Invoke the Auggie CLI for the deep review pass
- **Bash(gh *)**: Fetch PR metadata, post review comments
- **Bash(git *)**: Resolve diff ranges, list changed files
- **Read / Grep / Glob**: Validate Auggie's file:line citations against actual files
- **mcp__auggie__codebase-retrieval**: In-session codebase queries when validating findings without spawning a full Auggie subprocess
- **Write**: Emit the markdown report and audit log under `--output-dir`
- **Task**: Delegate per-persona deep passes to `auggie-reviewer` agent in `--depth deep` mode

## Examples

### Review a PR by number (most common)

```
/sc:auggie-review 62
# - Auggie pass: indexed codebase context + diff → JSON findings
# - Claude validates each file:line, dedupes, severity-tags
# - Markdown report written to .dev/reviews/pr-62-<ts>/REVIEW.md
# - Auto-posted to PR #62 as a review comment (default)
# - Inline comments attached for Critical / High findings
# - Prompts user: "Run /sc:design → task-builder → /sc:reflect chain on these findings?"
```

### Review uncommitted local changes

```
/sc:auggie-review --diff origin/master...HEAD --no-post-pr
# - Same protocol, but target is git diff, no PR posting
# - Useful pre-commit / pre-push self-review
```

### Snapshot review of a module (no diff)

```
/sc:auggie-review --snapshot src/superclaude/cli/ --focus architecture,anti-patterns
# - Full-content review of the subtree, no diff baseline
# - Auggie answers architecture-level questions; Claude grounds findings in real files
```

### Hook-driven post-PR-creation review

```
# After: gh pr create --title "..." --body "..."
# The offer-pr-review.sh hook detects the gh pr create call,
# prints a one-line offer to the assistant, who relays it to the user.
# User says yes → assistant invokes /sc:auggie-review <new-PR-num>.
```

### Deep review with full remediation chain

```
/sc:auggie-review 62 --depth deep
# After report posts, user accepts the remediation offer:
#   1. /sc:design <report-path> --type architecture --format spec  → remediation spec
#   2. Invoke task-builder skill on the spec  → MDTM task file
#   3. /sc:reflect --type task --analyze       → tasklist sanity check
#   4. User sign-off OR refactor task          → execute
#   5. /sc:reflect --type task --validate      → pre-commit validation
```

## Boundaries

**Will:**

- Run a deep, evidence-based code review combining Auggie's indexed codebase context with Claude's diff-level reasoning
- Catch both narrow bugs (off-by-one, null-deref, race conditions, leaked resources) and architectural risks (layering violations, coupling smells, missing abstractions, anti-patterns)
- Auto-post the report to the PR when the target is a PR (no confirmation; the user opted in by invoking the command)
- Attach inline `gh` review comments for Critical and High findings, anchored to real file:line in the diff
- Validate every Auggie-emitted file:line citation against the actual file before including it (no hallucinated locations in the report)
- Offer the `/sc:design` → `task-builder` → `/sc:reflect` remediation chain after the report posts, gated on user confirmation
- Write the full markdown report, raw Auggie JSON, and an audit log to `--output-dir` for later reference

**Will Not:**

- Activate on conversational keywords ("review", "audit", "check") — explicit invocation or hook-driven only
- Modify any code under review (advisory only — code changes happen later via the remediation chain)
- Approve, request-changes, or merge the PR (the report posts as a `--comment` review, never `--approve` or `--request-changes`)
- Run without `auggie` on PATH or, for PR targets, without an authed `gh` CLI — STOP with a clear error
- Bypass the file:line validation step (a finding that cannot be grounded in a real file is dropped, not promoted to "low confidence")
- Auto-trigger the remediation chain — that step always requires explicit user confirmation
- Post to a PR when `--no-post-pr` is specified, regardless of target type

## Related Commands

- **`/sc:design`** — Used in the remediation chain to convert review findings into an architecture/component remediation spec
- **`/sc:reflect --type task`** — Used twice in the remediation chain (analyze + validate gates)
- **`task-builder` skill** — Invoked between `/sc:design` and execution to produce an MDTM task file
- **`/sc:adversarial`** — Complementary; use `/sc:adversarial` when you need multi-model debate on a single artifact, vs this command's auggie-centric whole-diff review
- **`/sc:cleanup-audit`** — Complementary; whole-repo audit vs this command's diff/PR-scoped review
