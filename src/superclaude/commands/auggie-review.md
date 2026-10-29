---
name: auggie-review
description: "Auggie-powered code review for PRs, local diffs, or file snapshots — narrow bugs + architectural risks + anti-patterns, with auto-posted PR review and optional remediation handoff"
category: quality
complexity: advanced
mcp-servers: []
personas: [analyzer, architect, security, qa, refactorer]
argument-hint: "[<PR-num|PR-URL>|--diff <base>...HEAD|--snapshot <path>] [--focus security,architecture,quality,performance,all] [--depth quick|standard|deep] [--post-pr|--no-post-pr] [--remediation-offer|--no-remediation-offer] [--revagent opus|sonnet|haiku|fable]"
---

# /sc:auggie-review - Auggie-Powered Code Review

## Triggers

**Explicit only** — this command does NOT auto-activate from conversational keywords like "review", "audit", or "check". It activates only via:

1. **Direct invocation**: User types `/sc:auggie-review ...`
2. **Programmatic call**: Another `/sc:*` command invokes the `sc:auggie-review-protocol` skill directly

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
/sc:auggie-review 62 --depth deep --revagent sonnet     # Deep review; internal reviewer agent runs on sonnet
/sc:auggie-review 62 --depth deep --revagent opus       # Deep review; internal reviewer agent pinned to opus
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--focus` | `all` | Comma-separated subset of `security,architecture,quality,performance,anti-patterns,tests,docs,all` |
| `--depth` | `standard` | `quick` (auggie single-pass, ~2min), `standard` (auggie + Claude synthesis, ~5min), `deep` (auggie + per-persona Claude passes + cross-reference, ~10-15min) |
| `--post-pr` | `true` when target is a PR | Auto-post the markdown report as a `gh pr review --comment`. Inline comments for `Critical` and `High` findings via `gh api`. **No confirmation prompt — the user opted in by invoking the command on a PR.** |
| `--no-post-pr` | — | Generate the report only; do not touch GitHub |
| `--remediation-offer` | `true` | After the review completes, offer to chain `/sc:design` → `sc:workflow` → `/sc:reflect --mode pre` → user-run `/sc:implement` → `/sc:reflect --mode post` |
| `--no-remediation-offer` | — | Suppress the remediation chain offer |
| `--output-dir` | `.dev/reviews/<target-slug>-<timestamp>/` | Where to write the markdown report, raw auggie JSON, and audit log |
| `--auggie-model` | `prism-b` | Override the model auggie uses; when omitted and `AUGGIE_MODEL` is unset, uses `prism-b` (e.g., `--auggie-model <model-id>`) |
| `--revagent` | unset: reviewer agents use their frontmatter model | Model for the INTERNAL review-agent spawns only (the `--depth deep` `auggie-reviewer` pass and any re-spawn of it); it does not change the lead session model or `--auggie-model`. Accepted: `opus`, `sonnet`, `haiku`, `fable`. These are the native Agent tool `model` aliases; a missing value or any other value (e.g. `connect`, a full model ID, a gateway alias) STOPs with an error before any work, and never falls back to the default. `--revagent` picks the request alias; which concrete model an alias resolves to is Claude Code / gateway configuration (e.g. `ANTHROPIC_DEFAULT_SONNET_MODEL`, a LiteLLM alias), and `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` overrides per-invocation models. At `--depth quick` or `standard` no internal reviewer runs, so the flag only prints a WARN |

## Behavioral Flow

The full multi-wave protocol lives in the skill. The command file performs only:

1. **Parse arguments** → resolve target type (PR / diff / snapshot) and validate `--revagent`: a missing or unsupported value STOPs here, before step 2 environment checks
2. **Validate environment** → `auggie` on PATH, `gh` authed (if PR target), repo is a git working tree
3. **Hand off to the skill** via the Activation section below
4. **On skill return**, surface the report path, PR URL (if posted), and remediation-chain prompt (if enabled)

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:auggie-review-protocol

Do NOT proceed with protocol execution using only this command file. The full behavioral specification — Auggie invocation, finding validation, severity rubric, PR posting, remediation handoff — is in the protocol skill.

## MCP Integration

- **Native reasoning**: Multi-step synthesis when reconciling Auggie findings with Claude's diff-level checks
- **Serena**: Symbol-level cross-reference when validating Auggie's file:line citations against actual code

External tool (not MCP, but central): **`auggie` CLI** is the primary review engine. The skill shells out to `auggie --print --output-format json --ask` to offload deep analysis to Auggie's indexed codebase context, dramatically reducing Claude token consumption.

## Tool Coordination

- **Bash(auggie *)**: Invoke the Auggie CLI for the deep review pass
- **Bash(gh *)**: Fetch PR metadata, post review comments
- **Bash(git *)**: Resolve diff ranges, list changed files
- **Read / Grep / Glob**: Validate Auggie's file:line citations against actual files
- **mcp__auggie__codebase-retrieval**: In-session codebase queries when validating findings without spawning a full Auggie subprocess
- **Write**: Emit the markdown report and audit log under `--output-dir`
- **Task**: Spawn the `auggie-reviewer` agent for the `--depth deep` cross-check pass (protocol Wave 2 step 5), passing the `model` parameter when `--revagent` is set (per-persona deep passes are Auggie CLI calls, not agents)

## Examples

### Review a PR by number (most common)

```text
/sc:auggie-review 62
# - Auggie pass: indexed codebase context + diff → JSON findings
# - Claude validates each file:line, dedupes, severity-tags
# - Markdown report written to .dev/reviews/pr-62-<ts>/REVIEW.md
# - Auto-posted to PR #62 as a review comment (default)
# - Inline comments attached for Critical / High findings
# - Prompts user: "Run /sc:design → sc:workflow → /sc:reflect → /sc:implement chain on these findings?"
```

### Review uncommitted local changes

```text
/sc:auggie-review --diff origin/master...HEAD --no-post-pr
# - Same protocol, but target is git diff, no PR posting
# - Useful pre-commit / pre-push self-review
```

### Snapshot review of a module (no diff)

```text
/sc:auggie-review --snapshot src/superclaude/cli/ --focus architecture,anti-patterns
# - Full-content review of the subtree, no diff baseline
# - Auggie answers architecture-level questions; Claude grounds findings in real files
```

### Remediation chain

```text
/sc:auggie-review 62
# After report posts, user accepts the remediation offer:
#   1. /sc:design <report-path> --type architecture --format spec  → remediation spec
#   2. /sc:workflow on the spec                 → tasklist package .dev/tasks/to-do/<id>/<id>.md
#   3. (built in) workflow's own /sc:reflect --mode pre → plan sanity check, result surfaced
#   4. User sign-off OR refactor plan          → user runs /sc:implement <tasklist>
#   5. /sc:reflect --mode post                 → pre-commit validation
```

## Boundaries

**Will:**

- Run a deep, evidence-based code review combining Auggie's indexed codebase context with Claude's diff-level reasoning
- Catch both narrow bugs (off-by-one, null-deref, race conditions, leaked resources) and architectural risks (layering violations, coupling smells, missing abstractions, anti-patterns)
- Auto-post the report to the PR when the target is a PR (no confirmation; the user opted in by invoking the command)
- Attach inline `gh` review comments for Critical and High findings, anchored to real file:line in the diff
- Validate every Auggie-emitted file:line citation against the actual file before including it (no hallucinated locations in the report)
- Offer the `/sc:design` → `sc:workflow` → `/sc:reflect` → `/sc:implement` remediation chain after the report posts, gated on user confirmation
- Write the full markdown report, raw Auggie JSON, and an audit log to `--output-dir` for later reference

**Will Not:**

- Activate on conversational keywords ("review", "audit", "check") — explicit `/sc:auggie-review` invocation or a programmatic call from another `/sc:*` command only
- Modify any code under review (advisory only — code changes happen later via the remediation chain)
- Approve, request-changes, or merge the PR (the report posts as a `--comment` review, never `--approve` or `--request-changes`)
- Run without `auggie` on PATH or, for PR targets, without an authed `gh` CLI — STOP with a clear error
- Bypass the file:line validation step (a finding that cannot be grounded in a real file is dropped, not promoted to "low confidence")
- Auto-trigger the remediation chain — that step always requires explicit user confirmation
- Post to a PR when `--no-post-pr` is specified, regardless of target type

## Related Commands

- **`/sc:design`** — Used in the remediation chain to convert review findings into an architecture/component remediation spec
- **`/sc:reflect`** — Pre + post gates in the remediation chain. The pre gate is `sc:workflow`'s built-in `--mode pre` (not re-run), the post gate is `--mode post`
- **`/sc:workflow`** → **`/sc:implement`** — Remediation chain: workflow turns the design spec into a tasklist package (and runs its own `/sc:reflect --mode pre`), the user runs implement
- **`/sc:adversarial`** — Complementary; use `/sc:adversarial` when you need multi-model debate on a single artifact, vs this command's auggie-centric whole-diff review
- **`/sc:cleanup-audit`** — Complementary; whole-repo audit vs this command's diff/PR-scoped review
