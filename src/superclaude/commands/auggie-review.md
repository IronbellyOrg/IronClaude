---
name: auggie-review
description: "Code review for PRs, local diffs, or file snapshots by the auggie-reviewer agent with Serena hints — narrow bugs + architectural risks + anti-patterns, every finding grounded by Read, with auto-posted PR review and optional remediation handoff"
category: quality
complexity: advanced
mcp-servers: [serena]
personas: [analyzer, architect, security, qa, refactorer]
argument-hint: "[<PR-num|PR-URL>|--diff <base>...HEAD|--snapshot <path>] [--focus security,architecture,quality,performance,all] [--depth quick|standard|deep] [--post-pr|--no-post-pr] [--remediation-offer|--no-remediation-offer]"
---

# /sc:auggie-review - Agent Code Review

## Triggers

**Explicit only** — this command does NOT auto-activate from conversational keywords like "review", "audit", or "check". It activates only via:

1. **Direct invocation**: User types `/sc:auggie-review ...`
2. **Programmatic call**: Another `/sc:*` command invokes the `sc:auggie-review-protocol` skill directly (e.g. the `/sc:pr-submit` decline fallback)

The trigger discipline exists because deep reviews are expensive (several opus agent passes) and false-positive activation in mid-conversation wastes user time. See "Boundaries → Will Not" below.

## Required Input

**MANDATORY**: One of the following review targets:

- **Remote PR**: `<PR-number>` or `<PR-URL>` (resolved via `gh pr view`)
- **Local diff**: `--diff <base-ref>...HEAD` (committed changes only), or, if no target is given and the working tree is dirty, the implicit `git diff $(git merge-base origin/<default-branch> HEAD)`, which includes uncommitted tracked edits. Untracked files are listed in a WARN and are not reviewed.
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
| `--depth` | `standard` | `quick` (one agent pass per chunk), `standard` (same as quick), `deep` (plus security, architect, performance and qa persona passes, once each on the whole diff) |
| `--post-pr` | `true` when target is a PR | Auto-post the markdown report as a `gh pr review --comment`. Inline comments for `Critical` and `High` findings via `gh api`. **No confirmation prompt — the user opted in by invoking the command on a PR.** |
| `--no-post-pr` | — | Generate the report only; do not touch GitHub |
| `--remediation-offer` | `true` | After the review completes, offer to chain `/sc:design` → `sc:workflow` → `/sc:reflect --mode pre` → user-run `/sc:implement` → `/sc:reflect --mode post`. With `--depth deep`, `task-builder` → `/task` (and `/sc:reflect --type task --analyze|--validate`) replaces the workflow/implement pair |
| `--no-remediation-offer` | — | Suppress the remediation chain offer |
| `--output-dir` | `.dev/reviews/<target-slug>-<timestamp>/` | Where to write the markdown report, findings JSON, and audit log |

## Behavioral Flow

The full multi-wave protocol lives in the skill. The command file performs only:

1. **Parse arguments** → resolve target type (PR / diff / snapshot)
2. **Validate environment** → `gh` authed (if PR target), repo is a git working tree
3. **Hand off to the skill** via the Activation section below
4. **On skill return**, surface the report path, PR URL (if posted), and remediation-chain prompt (if enabled)

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:auggie-review-protocol

Do NOT proceed with protocol execution using only this command file. The full behavioral specification — agent passes, finding validation, severity rubric, PR posting, remediation handoff — is in the protocol skill.

## MCP Integration

- **Serena**: caller and symbol hints. A hint is never evidence; every cited line is Read.

## Tool Coordination

- **Bash(gh *)**: Fetch PR metadata and diff, post review comments
- **Bash(git *)**: Resolve diff ranges, list changed files
- **Read / Grep / Glob**: Validate every file:line citation against actual files
- **Write**: Emit the findings JSON, markdown report, and audit log under `--output-dir`
- **Task**: Run the `auggie-reviewer` agent at every depth

## Examples

### Review a PR by number (most common)

```text
/sc:auggie-review 62
# - auggie-reviewer agent pass over the gh pr diff → findings JSON
# - Claude validates each file:line, dedupes, severity-tags
# - Markdown report written to .dev/reviews/pr-62-<ts>/REVIEW.md
# - Auto-posted to PR #62 as a review comment (default)
# - Inline comments attached for Critical / High findings
# - Prompts user: "Run /sc:design → sc:workflow → /sc:reflect → /sc:implement chain on these findings?"
```

### Review local branch changes

```text
/sc:auggie-review --diff origin/master...HEAD --no-post-pr
# - Same protocol, but target is the committed git diff, no PR posting
# - With no target and a dirty tree, the implicit diff also covers uncommitted tracked edits
```

### Snapshot review of a module (no diff)

```text
/sc:auggie-review --snapshot src/superclaude/cli/ --focus architecture,anti-patterns
# - Full-content review of the subtree, no diff baseline
```

### Default remediation chain (plan route)

```text
/sc:auggie-review 62
# After report posts, user accepts the remediation offer:
#   1. /sc:design <report-path> --type architecture --format spec  → remediation spec
#   2. /sc:workflow on the spec                 → tasklist package .dev/tasks/to-do/<id>/<id>.md
#   3. (built in) workflow's own /sc:reflect --mode pre → plan sanity check, result surfaced
#   4. User sign-off OR refactor plan          → user runs /sc:implement <tasklist>
#   5. /sc:reflect --mode post                 → pre-commit validation
```

### Deep review with MDTM remediation chain

```text
/sc:auggie-review 62 --depth deep
# After report posts, user accepts the remediation offer (route = mdtm):
#   1. /sc:design <report-path> --type architecture --format spec  → remediation spec
#   2. Invoke task-builder skill on the spec  → MDTM task file
#   3. /sc:reflect --type task --analyze       → tasklist sanity check
#   4. User sign-off OR refactor task          → user runs /task <path>
#   5. /sc:reflect --type task --validate      → pre-commit validation
```

## Boundaries

**Will:**

- Run an evidence-based code review with the `auggie-reviewer` agent over a diff defined by `git` and `gh`
- Catch both narrow bugs (off-by-one, null-deref, race conditions, leaked resources) and architectural risks (layering violations, coupling smells, missing abstractions, anti-patterns)
- Auto-post the report to the PR when the target is a PR (no confirmation; the user opted in by invoking the command)
- Attach inline `gh` review comments for Critical and High findings, anchored to real file:line in the diff
- Validate every file:line citation against the actual file before including it (no hallucinated locations in the report)
- Offer the `/sc:design` → `sc:workflow` → `/sc:reflect` → `/sc:implement` remediation chain after the report posts (`task-builder` → `/task` only when `--depth deep`), gated on user confirmation
- Write the full markdown report, findings JSON, and an audit log to `--output-dir` for later reference

**Will Not:**

- Activate on conversational keywords ("review", "audit", "check") — explicit or programmatic invocation only
- Modify any code under review (advisory only — code changes happen later via the remediation chain)
- Approve, request-changes, or merge the PR (the report posts as a `--comment` review, never `--approve` or `--request-changes`)
- Run a PR target without an authed `gh` CLI — STOP with a clear error
- Bypass the file:line validation step (a finding that cannot be grounded in a real file is dropped, not promoted to "low confidence")
- Auto-trigger the remediation chain — that step always requires explicit user confirmation
- Post to a PR when `--no-post-pr` is specified, regardless of target type

## Related Commands

- **`/sc:design`** — Used in the remediation chain to convert review findings into an architecture/component remediation spec
- **`/sc:reflect`** — Pre + post gates in the remediation chain. Plan route: the pre gate is `sc:workflow`'s built-in `--mode pre` (not re-run), the post gate is `--mode post`; `--type task --analyze|--validate` on the MDTM route
- **`/sc:workflow`** → **`/sc:implement`** — Default remediation route: workflow turns the design spec into a tasklist package (and runs its own `/sc:reflect --mode pre`), the user runs implement
- **`task-builder` skill** — Only with `--depth deep`: invoked between `/sc:design` and execution to produce an MDTM task file for `/task`
- **`/sc:adversarial`** — Complementary; use `/sc:adversarial` when you need multi-model debate on a single artifact, vs this command's whole-diff review
- **`/sc:cleanup-audit`** — Complementary; whole-repo audit vs this command's diff/PR-scoped review
