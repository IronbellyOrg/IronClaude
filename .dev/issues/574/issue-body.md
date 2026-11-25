> **HOLD (owner decision, 2026-11-16): do not install, run or test this tool yet.** Sending all conversation data over the wire to a third party is not acceptable for now. Testing waits until a potential alternative is found and assessed, for example a decision model from Anthropic or a local model set up on premises on an RTX 3090 or 4090 GPU. Allowed meanwhile: reading, the alternatives study (stage A0) and the document-only steps. Details: runbook section 0 below.

## Feature Summary

Install and evaluate the third-party tool `fast-jev-compaction` (https://github.com/tamaratran/fast-jev-compaction) in a safe sandbox: install it, measure it against baselines on relevant KPIs, and report a verdict (ADOPT / PILOT / REJECT / BLOCKED). This issue delivers an evaluation report, not a change to IronClaude defaults, settings or source.

## Problem Statement

Claude Code's built-in compaction writes a summary, which can lose paths, errors, constraints and commands from long sessions (the tool's stated motivation). `fast-jev-compaction` instead prunes tool calls and tool outputs during compaction, using TypeSafe's Jev API (`https://api.typesafe.ai/v1/systemone`, model `jev-latest`) to decide what to keep, truncate or delete; user and assistant prose stays unchanged. The README reports no benchmark numbers (no latency, token-savings, accuracy or comparison figures), so its usefulness for IronClaude's long sessions is unmeasured.

Data-sharing approval for sending private text to TypeSafe/Jev is **not established** (it is an open owner decision in the blocker-classifier work, IronClaude#552). The owner answered on 2026-11-16 that sending all conversation data over the wire is not acceptable for now, so testing is on hold (see the banner above). When it resumes, live runs use public fixtures only and never private conversation text.

The tool requires `TYPESAFE_API_KEY` and the early-access function hooks of Claude Code 2.1.274 or newer (`CLAUDE_CODE_ENABLE_FUNCTION_HOOKS`), and it replaces `/compact` and automatic compaction behaviour for the session. Each request sends conversation text (prose and tool inputs, with placeholders for tool outputs) off the machine to TypeSafe.

## User Story

As an IronClaude owner, I want an evidence-based evaluation of `fast-jev-compaction` run in an isolated environment on synthetic or public fixtures, so that I can decide whether adopting it is safe and worthwhile without exposing private conversation data or changing any IronClaude default.

## Proposed Solution

Follow the evaluation runbook appended below this section (installation instructions and the agentic evaluation procedure are provided there). In outline: install the tool in an isolated sandbox (fresh checkout or `--plugin-dir` run, Claude Code 2.1.274+, `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1`, `TYPESAFE_API_KEY` set in the sandbox environment only), run it against synthetic or public session fixtures, measure the KPIs the runbook defines against baselines (no-plugin compaction and, where applicable, no compaction), and record the results. The runbook below is the procedure; this issue does not add another one.

## Acceptance Criteria

- [ ] The alternatives study (runbook stage A0) is recorded and the owner lifted the hold in writing.
- [ ] After the hold was lifted, the runbook below was executed in an isolated environment (no IronClaude checkout, settings or home directory used as the test bed).
- [ ] A results report exists with one table per KPI, each including the baseline measurement alongside the tool's measurement.
- [ ] A verdict of ADOPT, PILOT, REJECT or BLOCKED is stated in the report, together with the decision rule that produced it.
- [ ] No private text was sent to the third-party API: all live fixtures were synthetic or public, and the report names the fixtures used.
- [ ] No IronClaude default, setting or source file was changed; `git status` in the IronClaude checkout is clean of tool-related changes.
- [ ] The `TYPESAFE_API_KEY` was never printed to output or stored in any file that survives the evaluation.
- [ ] Total spend on Jev credits and downstream model calls stayed within the owner's $50 budget.

## Owner decisions (2026-11-16)

- Sending all conversation data over the wire is not acceptable for now. Testing is on hold until a potential alternative is found, for example a decision model from Anthropic or a local model set up on premises with an RTX 3090 or 4090 GPU.
- Live runs, once allowed, use public fixtures only.
- Budget: $50, which the owner called more than enough. Read here as one cap for the whole evaluation; the owner did not say whether both Jev credits and downstream model calls count toward it.
- The README reports no benchmarks yet; the owner acknowledged that.

## Out of Scope

- Changing IronClaude defaults, settings, hooks or source (including `src/superclaude/cli/user_settings_defaults.json` and ccsession compaction-window handling) — this issue is evaluation only.
- Installing the tool for real sessions or enabling it by default. That is a separate decision after the evaluation; #553 covers a different plugin (the Jev agent skill).
- Sending private or real conversation text to TypeSafe/Jev: data-sharing approval is not established (open owner decision in #552), so live runs use synthetic or public fixtures only.
- Adversarial security audit of the third-party codebase beyond what the runbook specifies. Not known yet whether a deeper audit is wanted.

## Components Affected (from `/sc:analyze`)

No IronClaude file is expected to change; this is an evaluation-only issue. Inspected in the codebase pass (quick depth, `origin/master` at d4d1662a8):

- `src/superclaude/cli/user_settings_defaults.json` — plugin/defaults surface; contains `enabledPlugins` and an `env` block, currently no `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS` or `TYPESAFE_API_KEY` entries and no fast-jev plugin.
- `docs/reference/claude-code-history-management.md` — existing notes on Claude Code compaction and `/clear` guidance; the natural home for any future findings, but not modified by this issue.
- `docs/testing/v5.0.0/user/D08-ccsession.md` and `docs/testing/v5.0.0/sysop/E01-ccsession-tier-policy.md` — ccsession context-window / auto-compact window behaviour documentation.
- Codegraph was not consulted (no codegraph MCP tools available in this worker); the pass used Grep and `git show origin/master:` reads.

## Related Issues/PRs

- #553 — related: installing the TypeSafe Jev agent skill plugin by default; a different plugin from the one evaluated here.
- #552 — related: blocker-classifier work that would use Jev; holds the open owner decision on data-sharing approval that constrains this evaluation.
- #463 — related: model/effort router research that would also use Jev.

<!-- sc:issue:create template=issue-feature-simple -->
