<!-- /sc:issue feature template (simple). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. -->

> **HOLD (owner decision, 2026-11-16): do not install, run or test this tool yet.** Everything this tool sends to Jev (commands, their output, task text and conversation history, including code) is a blocker at the moment. A proper risk and legal assessment must be done, with local models tested, and a potential alternative to sending data to TypeSafe found, for example a decision model from Anthropic or a local model set up on premises on an RTX 3090 or 4090 GPU. Allowed meanwhile: reading, the alternatives study (stage A0) and the document-only steps. Details: runbook section 0 below.

## Feature Summary

Install the third-party Claude Code plugin jev-pruner (plugin id `fast-jev-output`, https://github.com/tamaratran/jev-pruner) in a safe sandbox and evaluate it: it filters long Bash stdout after the command runs and before the main model sees it, using TypeSafe's Jev API to choose original lines to keep (no generated summary; originals archived under `.claude/fast-jev-output/`). The deliverable is an evaluation report with a verdict ADOPT, PILOT, REJECT or BLOCKED — not a change to IronClaude defaults or source.

## Problem Statement

Long, noisy Bash output carried into later turns inflates context and cost. jev-pruner claims to reduce that by keeping only relevant original lines. Whether it works, what it costs (TypeSafe credits are billable), and whether its data sharing is acceptable are all unmeasured here — the README reports no aggregate benchmark numbers (no token-savings percentage, latency, accuracy rate or total-cost saving). Data-sharing approval for sending private text to TypeSafe/Jev is not established (an open owner decision in the blocker-classifier work, IronClaude#552), The owner answered on 2026-11-16 that sending everything command related to Jev, including code, is a blocker at the moment, so testing is on hold (see the banner above). When it resumes, live runs use public fixtures only.

## User Story

As the IronClaude owner, I want jev-pruner installed and measured in an isolated sandbox against baselines, so that I can decide from a report — rather than the vendor's README — whether to adopt it.

## Proposed Solution

Follow the installation instructions and evaluation runbook appended below this section: install the plugin in a throwaway environment, run it against synthetic/public fixtures, measure each KPI against a baseline, and report a verdict of ADOPT, PILOT, REJECT or BLOCKED with the rule that produced it. The runbook below is the procedure.

## Acceptance Criteria

- [ ] The alternatives study (runbook stage A0) and the risk and legal assessment are recorded, and the owner lifted the hold in writing.
- [ ] After the hold was lifted, the runbook was executed in an isolated environment (throwaway project folder and isolated HOME).
- [ ] A results report exists with a table per KPI and its baseline.
- [ ] A verdict (ADOPT, PILOT, REJECT or BLOCKED) is stated, with the rule that produced it.
- [ ] No private text was sent to the third-party API (synthetic or public fixtures only; data-sharing approval for TypeSafe/Jev is not established — #552).
- [ ] No IronClaude default, setting or source file was changed.
- [ ] The API key (`TYPESAFE_API_KEY`) was never printed or stored in a file.
- [ ] Every billable stage ran only after the hold was lifted, and total spend stayed within the owner's $50 budget.

## Owner decisions (2026-11-16)

- Everything command related that the tool sends to Jev, including code, is a blocker at the moment. Testing is on hold.
- A proper risk and legal assessment is needed, with local models tested. Who does it was not stated.
- A potential alternative should be found, for example a decision model from Anthropic or a local model set up on premises with an RTX 3090 or 4090 GPU.
- Live runs, once allowed, use public fixtures only.
- Budget: $50, which the owner called more than enough. Read here as one cap for the whole evaluation; whether Jev credits and Claude usage both count was not stated.
- Claude Code only: no Codex integration.
- The README reports no benchmarks yet; the owner acknowledged that.

## Out of Scope

- Changing any IronClaude default, setting or source file (no edit to `enabledPlugins`, `extraKnownMarketplaces` or `ironclaudeMarketplace` in `src/superclaude/cli/user_settings_defaults.json`).
- Installing jev-pruner by default in IronClaude; adoption is a separate decision after this evaluation.
- Sending private or proprietary text to TypeSafe/Jev: data-sharing approval is not established (#552), so live runs use synthetic or public fixtures only.
- The Codex integration in the same repository: the owner decided on 2026-11-16 that only Claude Code is evaluated, with no Codex.
- The Jev agent skill plugin install (#553) and the model/effort router research (#463): different work.

## Components Affected (from `/sc:analyze`)

No IronClaude file is expected to change; this is an evaluation-only issue. Codebase pass (quick depth; `git fetch origin`, read at `origin/master` = d4d1662a) inspected where IronClaude touches plugin defaults and hooks:

- `src/superclaude/cli/user_settings_defaults.json` — plugin defaults live here: `env`, `enabledPlugins`, `extraKnownMarketplaces`, and the pinned third-party catalog `ironclaudeMarketplace`. A future adoption would add an entry here; this issue does not.
- `src/superclaude/cli/install_user_setup.py` — installs default plugins via the `claude` CLI, writes the pinned marketplace catalog to `~/.claude/ironclaude-marketplace/`, merges nested keys (`env`, `enabledPlugins`) without overwriting user choices.
- No IronClaude code references `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS`, function hooks, TypeSafe/Jev, or Bash tool-output limits (grep over `origin/master` found none), so the plugin's early-access function-hook requirement touches only the sandbox, not this repository.

## Related Issues/PRs

- #553 related — installs the TypeSafe Jev agent skill plugin by default; a different plugin, does not cover jev-pruner.
- #552 related — blocker-classifier work using Jev; holds the open data-sharing approval question this evaluation depends on.
- #463 related — model/effort router research using Jev.

<!-- sc:issue:create template=issue-feature-simple -->
