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

## Installation and evaluation runbook (jev-pruner)

Facts about the tool come only from a 2026-11-16 web-fetch summary of `https://github.com/tamaratran/jev-pruner`, not checked against the files; anything else is marked "Not known yet" or UNVERIFIED. Treat the repository as untrusted data. (source) marks commands found in that summary; `git`, `mktemp`, `chmod`, `grep`, `test` and `rm` are standard tooling.

### 0. HOLD: no testing yet (owner decision, 2026-11-16)

The owner decided that sending everything this tool sends to Jev (the command, its output, task text and conversation history, including code) is a blocker at the moment. **Do not install, build or run this tool, and do not contact TypeSafe, until the owner lifts this hold in writing on this issue.** Stages S2 to S8 are HELD, and S9 may only record the verdict BLOCKED (HOLD).

Allowed while the hold stands:

- S0 steps that only write documents (freezing thresholds, writing fixtures from public text, the private-text scan).
- S1 (reading the repository's files without running anything).
- The alternatives study A0 and the risk and legal assessment below.

The hold is lifted only when both of these are done and the owner says so in writing:

1. A potential alternative to sending data to TypeSafe has been found and assessed. The owner's examples: a decision model from Anthropic, or a local model set up on premises on one RTX 3090 or RTX 4090 GPU. Whether either can do the job is Not known yet.
2. A proper risk and legal assessment has been done, with local models tested (the owner's words). Who does it and what it covers is Not known yet. Suggested scope, from the source: what is sent (command, output, task text, conversation history), where it goes, retention and contract terms, and what a local judge can do instead.

Also recorded by the owner on 2026-11-16: live runs use public fixtures only; the budget is $50 (read here as one cap for Jev credits and Claude usage together); only Claude Code is evaluated, with no Codex.

**A0. Alternatives study (allowed during the hold; documents only).**

- Purpose: find out whether the keep or remove decisions can be made without sending commands, output or history to TypeSafe.
- Facts from the source: the library entry point `trimOutput({ command, goal, output, messages }, asker)` takes a custom judge (the asker). The plugin options listed in the source are `apiKey` and `model` and no endpoint, so whether the plugin can use a different judge is Not known yet.
- Steps: (1) list candidate judges: an Anthropic model and a local model on one RTX 3090 or RTX 4090 (the owner's examples), plus any the study finds; (2) for each, record where data goes, who can see it, retention terms, licence, hardware and running cost; (3) define a small test, on public text only, of whether a candidate can answer the tool's yes-or-no probability questions well enough; (4) recommend which candidate, if any, to test first.
- Output: `<R>/A0-alternatives.md`.
- Rule: PASS when every candidate has its row and a recommendation exists. The owner then decides whether to lift the hold.

### 1. What the tool is

- A Claude Code plugin that filters long Bash output after the command runs and before the main model sees it.
- It keeps ORIGINAL lines chosen by TypeSafe's Jev API instead of writing a summary; removed runs of lines become one omission marker.
- Only output above 10,000 estimated tokens is eligible. Errors, structured or document-like output (JSON, XML, YAML, diffs, source code) and protected commands (for example `cat`, `jq`, `git diff`) are never pruned.
- The full output is archived under `.claude/fast-jev-output/` in the project folder (locally git-excluded) before scoring; on any read, scoring or archive failure the original result is kept.
- The repository is `jev-pruner`; the Claude plugin and marketplace id is `fast-jev-output`.
- A separate, opt-in Codex integration exists. The README reports no aggregate savings, latency or accuracy numbers.

### 2. Gates and safety (read before any install step)

**G1. Data leaves the machine (hard rule).** For each eligible command, Jev receives the command, its output, the task text and conversation history (user and assistant text, tool inputs and results) at `https://api.typesafe.ai/v1/systemone`, with `TYPESAFE_API_KEY`. The README says there is no transcript redaction, and that not archiving credential-like output does not stop it being sent. The owner's approval for sending private text to TypeSafe/Jev is NOT established (open item OD3 in the blocker-classifier work, IronClaude#552; the Jev plugin install is IronClaude#553). Owner answer, 2026-11-16: everything command related that goes to Jev, including code, is a blocker at the moment. Once the section 0 hold is lifted, every run that calls the live API uses only public fixtures, in a throwaway project folder: no private repository text, no IronClaude source, no secrets, no client data, no real session history.

Checklist item, ticked in `S0-gates.md` before the first live stage (S3):

- [ ] Every input that can reach Jev (fixtures, prompts, the session's own history) is synthetic or public, the section 6 private-text scan passed, and every live session starts in an empty throwaway folder with an isolated HOME.

**G2. Billing.** Jev calls and Claude usage are both billable. The author's long-session test has a default $10 Claude cap that does not include Jev; the archive-recovery test has a $2 Claude cap per call. TypeSafe credits are needed; HTTP 402 means none are left. The owner set a $50 budget on 2026-11-16 (read here as one cap for Jev credits and Claude usage together; the owner did not say whether both count). Record it in `S0-frozen.md`; every billable stage (S3 to S8) stays BLOCKED while the section 0 hold stands. The first billable run is the 2-stage smoke run (S3). Jev price is Not known yet; a human reads the credit balance on the TypeSafe billing page before and after each billable stage.

**G3. The key.** `TYPESAFE_API_KEY` comes from the environment only, exported by the owner or a human the owner names. Never print it, never write it to a file (no `settings.json`, no `apiKey` option, no evidence file), never put it on a logged command line; redact it in logs as `[REDACTED]`. The source file shows no key-presence check, so the allowed check is Not known yet; the proposed one below (standard shell, UNVERIFIED as owner-approved) prints only `key-present` or `key-absent`:

```
test -n "${TYPESAFE_API_KEY:-}" && echo key-present || echo key-absent
```

Without a key, live stages end BLOCKED, not failed.

**G4. Claude Code version and early-access hooks.** The plugin needs early-access function hooks and `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1`. Its declarations were generated with Claude Code 2.1.274; a minimum version is not shown. Not known yet whether this workspace meets it. S0 records:

```
claude --version
```

**G5. Isolation.** The plugin rewrites every long Bash result and writes archives into the project folder, so every plugin test runs in a throwaway project with an isolated HOME (settings in `<ISOHOME>/.claude`), never in the owner's real configuration or an IronClaude checkout or worktree. Export HOME for one command at a time; delete the folders afterwards:

```
mktemp -d /tmp/jevpruner-home.XXXXXXXX
mktemp -d /tmp/jevpruner-proj.XXXXXXXX
git init <PROJ>
HOME=<ISOHOME> claude --version
rm -rf <ISOHOME>
rm -rf <PROJ>
```

`git init` lets the archive's git exclusion be checked. How Claude Code authenticates inside a fresh HOME is Not known yet. Never copy the owner's credential files into `<ISOHOME>` without the owner's approval; if the session cannot authenticate, live stages are BLOCKED.

**G6. Third-party code.** Pin the exact commit and record it. Before running anything, read `hooks/` and `package.json` (scripts and dependencies, especially any `preinstall`, `install`, `postinstall` or `prepare` script). Run installs only in throwaway folders under `/tmp`; `node_modules` never goes inside the IronClaude repository or a worktree. No change to IronClaude source files. Python in this repository is UV-only; this tool is npm.

**G7. Licence.** MIT (full text not shown by the source). S1 reads `LICENSE` and records "licence file read" with its first line.

**G8. Out of scope.** The Codex integration is not evaluated at all: the owner decided on 2026-11-16 that only Claude Code is in scope. The macOS demo (recorded, no API requests, measures nothing) is not evaluated either.

### 3. Installation

Placeholders: `<SRC>` pinned checkout, `<PIN>` recorded commit, `<ISOHOME>` isolated HOME, `<PROJ>` throwaway project, `<R>` results folder `.dev/eval-workspaces/jev-pruner/results/`.

**Step a. Read-only inspection of a pinned checkout.**

```
mktemp -d /tmp/jevpruner-src.XXXXXXXX
git clone https://github.com/tamaratran/jev-pruner.git <SRC>
git -C <SRC> rev-parse HEAD
```

(source: the clone URL)

- Expected: `hooks/`, `.claude-plugin/`, `tests/`, `LICENSE` and `package.json` exist.
- Verify: record `<PIN>`; read `LICENSE`, `package.json`, every file in `hooks/` and `.claude-plugin/`, and the synthetic fixtures used by the long-session test (names Not known yet).
- Undo: `rm -rf <SRC>`.

**Step b. Offline checks (no key in the environment).**

```
cd <SRC>
test -n "${TYPESAFE_API_KEY:-}" && echo key-present || echo key-absent
npm ci
npm test
npm run typecheck
npm run build
HOME=<ISOHOME> npm run validate:plugin
```

(source: all npm commands)

- Expected: `key-absent` (if present, unset it for this step), then exit 0 for each. `validate:plugin` needs an installed Claude Code CLI, so it gets the isolated HOME.
- Verify: record exit code, duration and test counts.
- Undo: `rm -rf <SRC>/node_modules`.

**Step c. Plugin route (isolated HOME and throwaway project only).** Preferred for measured runs because it uses `<PIN>`. The source form runs from the repository root:

```
CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude --plugin-dir .
```

That would write archives into the checkout, so the session starts in `<PROJ>` instead (UNVERIFIED that `--plugin-dir` accepts an absolute path from another folder; if not, record it and stop):

```
cd <PROJ>
HOME=<ISOHOME> CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude --plugin-dir <SRC>
```

Marketplace route, for the install-effort KPI only (installs whatever the repository serves now, not `<PIN>`):

```
HOME=<ISOHOME> claude plugin marketplace add tamaratran/jev-pruner
HOME=<ISOHOME> claude plugin install fast-jev-output@fast-jev-output
```

- The key stays in the environment (the source allows the shell's key), never in `env` settings or the `apiKey` option. Start a fresh session after install (source).
- Expected (source): a long Bash result shows a reduction toast and omission markers; originals appear under `<PROJ>/.claude/fast-jev-output/`.
- Verify: an output under 10,000 estimated tokens is unchanged; the key is not stored (prints file names only; must print nothing): `grep -rlF "$TYPESAFE_API_KEY" <ISOHOME> <PROJ>`.
- Undo: an uninstall command is Not known yet; delete `<ISOHOME>` (step e).

**Step d. Configuration.** Inside the session (source):

```
/plugin configure fast-jev-output
```

Settings live under `pluginConfigs` -> `fast-jev-output@fast-jev-output` -> `options` (which file: Not known yet; record it). Defaults from the source:

| option | default | note |
|---|---|---|
| `apiKey` | TYPESAFE_API_KEY | leave empty here (G3) |
| `minTokens` | 10000 | cannot go below 10,000 |
| `persistedOutputs` | true | work on Claude's saved full-output file |
| `persistedMaxChars` | 8000 | 0 removes the cap; native preview size stays an upper bound |
| `maxScoringRequests` | 11 | extra calls; 0 allows one; at most 12 requests, also capped by ceil(visibleChars / 192) |
| `chunkLines` | 20 | lines per chunk |
| `chunkChars` | 0 | optional character chunking |
| `diagnostics` | false | set true for evaluation |
| `keepThreshold` | 0.5 | scores above 0.1 are also kept |
| `maxStateTokens` | 25000 | history plus output budget |
| `model` | `jev-latest` | |

Turn `diagnostics` on for every evaluation run: it reports decision reasons, sizes, request count and elapsed time without recording text. Where it reports them, and how to set options headless, is Not known yet (S3).

**Step e. Uninstall and cleanup.**

```
rm -rf <PROJ>
rm -rf <ISOHOME>
rm -rf <SRC>
```

This also removes the archive folder. Delete any `/tmp` evidence folder after copying its redacted summary. Confirm the real `~/.claude/settings.json` modification time equals the S0 value, nothing new in `~/jev-long-sessions/`, and no `node_modules` or `.claude/fast-jev-output/` in the IronClaude checkout or worktrees.

### 4. KPIs

Every threshold is PROPOSED and must be frozen by the owner in `S0-frozen.md` before the first measured run. No threshold is justified by the README, which reports no aggregate numbers. A to E are the baselines in section 5. "Canary" is a planted line the task needs (section 6).

| id | KPI | definition and formula | how an agent measures it | instrument | starting threshold |
|---|---|---|---|---|---|
| K1 | Reduction, characters | 1 - chars_seen / chars_original per command; median per category (build/install/test, search, unknown or wrapped) | fixture vs tool result in the session transcript (UNVERIFIED that it stores the filtered result) | bench script | PROPOSED median >= 0.5 for build/test |
| K2 | Reduction, real tokens | same with a separate tokenizer (the tool's numbers are estimates); also the estimate's error | one independent tokenizer (which: Not known yet; record name and version) | token counter | PROPOSED median >= 0.5 for build/test |
| K3 | Canary retention | canaries seen / planted (required values, errors, failed tests, totals, final status, artifact paths) | exact-string search | canary script | PROPOSED >= 0.98 and >= B |
| K4 | False-removal rate | needed lines removed / needed lines | canaries plus lines the rubric marks needed | canary script | PROPOSED <= 0.02 |
| K5 | False-keep rate | kept noise lines / noise lines | lines marked noise when generated | canary script | no threshold, report only |
| K6 | Verbatim preservation | kept lines byte-identical to an original line / kept lines | line match, ignoring omission markers | integrity script | PROPOSED 100% (hard) |
| K7 | Archive integrity | archives byte-identical to the original / archived outputs | compare bytes in `<PROJ>/.claude/fast-jev-output/` | integrity script | PROPOSED 100% (hard) |
| K8 | Recovery success | removed lines recovered through the footer reference / tasks needing it | S5 recovery tasks | S5 log | PROPOSED >= 0.95 |
| K9 | Eligibility behaviour | unchanged / total for: outputs at or below 10,000 estimated tokens, protected formats, protected commands, errors | byte comparison | integrity script | PROPOSED 100% (hard) |
| K10 | Latency overhead | p50 and p95 extra seconds per eligible command | diagnostics elapsed time; wall time vs A | diagnostics | PROPOSED p95 <= 30 s |
| K11 | Requests per command | requests vs cap min(12, ceil(visibleChars / 192)) | diagnostics request count | diagnostics | PROPOSED never above cap (hard) |
| K12 | Jev cost | credits per command and per session; price Not known yet | balance before and after (human-read) / requests | billing page | no threshold, report only |
| K13 | Net saving | downstream Claude tokens saved x model price - Jev cost | from K2, K15, K12 | report | PROPOSED > 0 for ADOPT |
| K14 | Failure and fallback | original kept / injected cases (bad key, HTTP 402, timeout, network blocked, oversized state, archive write failure) | S7 injections | fault log | PROPOSED 100% (hard) |
| K15 | Whole-task effect | success, turns, input tokens, cost per task; C vs A and B | headless runs plus blind judge | task runner, S6 | PROPOSED C success within 5 points of A and >= B |
| K16 | Privacy exposure | bytes of command, output and history sent per command; private-text hits; handling of a fake credential-like string | diagnostics sizes if they cover requests (Not known yet); section 6 scan | diagnostics, scan | PROPOSED 0 private-text hits (hard); sizes report only |
| K17 | Local side effects | archive growth per command; git exclusion works; files outside `<PROJ>` and `<ISOHOME>` | `du`, `git status`, file lists before and after | side-effect script | PROPOSED exclusion works, 0 outside files (hard) |
| K18 | Long-session behaviour | 40+ commands: history partitioning, request growth, retention misses | author's long-session harness and report | harness | PROPOSED exit 0, partitioning seen |
| K19 | Repeatability | same input 3 times: mean pairwise Jaccard of kept lines | compare kept lines | bench script | PROPOSED >= 0.90 |
| K20 | Threshold sensitivity | K1, K3, K4, K10, K11 per sweep value (D) | non-held-out fixtures | bench script | no threshold, report only |
| K21 | Prompt-cache effect | cache read and write tokens on later turns, C vs A | Not known yet; proposed: cache usage fields of headless JSON output (UNVERIFIED), same prompts per baseline | task runner | no threshold, report only |
| K22 | Interplay | other active hooks; co-install with fast-jev-compaction (E) works without conflict | S8 observation | S8 log | PROPOSED no breakage |
| K23 | Install and operational effort | steps, restarts, failures, minutes per route | workers log every step | stage logs | no threshold, report only |
| K24 | Author-harness agreement | author suites pass on `<PIN>`; README example reproducible | exit status and reports of S3, S5, S7 | harness | report only; author results are claims, not evidence |

### 5. Baselines

- **A. No plugin**: the host's native preview and saved-file behaviour (no Jev cost).
- **B. Naive truncation**: first and last lines of each long output, sized to C's character count, pre-computed by a script and printed by the fixture command.
- **C. Plugin defaults**: step d table, `diagnostics` true.
- **D. Plugin sweeps**, one parameter at a time from C: `keepThreshold` 0.3, 0.5, 0.7; `chunkLines` 10, 20, 40; `minTokens` 10000, 20000; `persistedMaxChars` 4000, 8000, 16000; `maxScoringRequests` 4, 11, 20.
- **E. Optional**: C plus the sibling plugin fast-jev-compaction, only if that issue's gates have passed.

### 6. Fixtures

- **Content**: generated or public text only. No IronClaude source, private repository text, secrets or client data.
- **Set**: at least 12 tasks in three kinds: failing test run (`npm test` in a throwaway `package.json`), verbose build or install, wide search (`rg` over a generated tree); plus one unknown or wrapped command per kind. Sizes around 15k, 40k and 100k estimated tokens, every kind and size covered. Never print fixtures with protected commands such as `cat`, except in K9 controls (one output under 10,000 estimated tokens, one JSON, one diff, one source file, one error exit).
- **Held-out set**: at least 3 tasks never used for threshold choices.
- **Canaries**: at least 6 unique planted lines per output (task-required value, error line, failed test name, total, final status, artifact path), each with a task question that needs it; record line numbers; mark the rest as noise. Add one clearly fake, generated credential-like string in one fixture for K16.
- **Author fixtures**: reuse the author's synthetic fixtures named by S1 (for example the long-session noisy-command fixtures) as inputs only, after S1 confirms they are synthetic.
- **Seed**: 20261116 for every random choice; record the generating model.
- **Location**: `.dev/eval-workspaces/jev-pruner/fixtures/` with `manifest.json` (file, kind, size, command, seed, canaries, held-out flag). Copy into `<PROJ>` for each run.
- **Private-text check** (must pass before S3):

```
grep -rniE "superclaude|ironclaude|ironbelly|api[_-]?key|secret|BEGIN [A-Z ]*PRIVATE KEY" .dev/eval-workspaces/jev-pruner/fixtures/
```

Expected: no output, or only hits a human confirms are planted synthetic canaries (including the K16 fake string).

### 7. Agentic procedure (stages S0 to S9)

Ten stages are named, so the report is S9.

**Who runs it.** Each stage is one supervised Orca worker, one stage per worker, dispatched by the coordinator per the Orca orchestration guide. Every worker records the model it actually served, writes results only as files under `<R>`, and never merges, pushes or posts. Worker task spec fields:

- **target**: the stage and its input files;
- **change**: only the stage's output files plus `/tmp` throwaway folders;
- **constraints**: sections 2 and 6; no IronClaude source changes; no key in any file or log; the frozen budget;
- **ownership**: its output files and `/tmp` folders, deleted at the end (step e);
- **observable acceptance**: the output file exists, starts with stage, date, worker, served model, `<PIN>`, `claude --version`, and has a `status:` line (PASS, FAIL or BLOCKED) with evidence.

**S0. Gates and prerequisites.**
- Purpose: check G1 to G8; owner freezes thresholds, money budget, judge model and rubric; build fixtures.
- Commands: `claude --version`; the G3 check; record the real `~/.claude/settings.json` modification time (read only); build fixtures; the section 6 scan.
- Output: `<R>/S0-gates.md` (with the G1 tick box), `<R>/S0-frozen.md`, fixtures and manifest.
- Rule: PASS if the scan passes and thresholds, budget and rubric are frozen. BLOCKED if any is not frozen, or while the section 0 hold stands. FAIL if the scan finds private text.

**S1. Read-only inspection and licence.**
- Commands: section 3 step a.
- Output: `<R>/S1-inspection.md`: `<PIN>`, licence read, lifecycle scripts, dependencies, network endpoints, where the key is read, where diagnostics and settings go, whether author fixtures are synthetic, whether the 76,379-character example is in the repository.
- Rule: PASS if nothing unexpected. FAIL if code sends data beyond the documented endpoint or has unexpected install scripts (stop; the owner decides).

**S2. Offline build and tests.**
- Commands: section 3 step b. Output: `<R>/S2-offline.md`.
- Rule: PASS if all exit 0, else FAIL.

**S3. Live smoke run (2 stages).** First billable run; needs the G1 tick, a key and a budget.

```
cd <SRC>
mktemp -d /tmp/jevpruner-evidence.XXXXXXXX
HOME=<ISOHOME> JEV_LONG_SESSION_TURNS=2 JEV_LONG_SESSION_BUDGET_USD=<OWNER-CAP> JEV_LONG_SESSION_DIR=<EVID> npm run test:long-session
npm run report:long-session -- <EVID>
grep -rlF "$TYPESAFE_API_KEY" <EVID>
```

(source: the variable names and both npm commands; `<OWNER-CAP>` comes from `S0-frozen.md`)

- Output: `<R>/S3-smoke.md` (exit status, report summary, diagnostics location, credits used, key-scan result).
- Rule: PASS if exit 0 and the key scan prints nothing. BLOCKED without key, budget, G1 tick or authentication in `<ISOHOME>`. FAIL otherwise (errors redacted).

**S4. Independent fixture benchmark (headless).**
- Purpose: K1 to K6, K9 to K12, K15 to K17, K19, K21 for A, B, C.
- Method: per fixture and baseline, a fresh `<PROJ>` with the fixture copied in, then a headless Claude session in `<ISOHOME>` given the task prompt. Headless flags are not in the source: check `claude --help` first. C runs three times (K19). Write `bench.mjs`, `canary.mjs`, `integrity.mjs` and `sideeffects.mjs` under `.dev/eval-workspaces/jev-pruner/scripts/`; copy them to `/tmp` to run.
- Output: `<R>/S4-outputs/`, `<R>/S4-metrics.csv` (row per fixture, baseline, run), `<R>/S4-bench.md`.
- Rule: PASS if every fixture ran for every baseline. BLOCKED without key, budget or authentication. FAIL if scripts cannot run. KPI misses are recorded, not stage failures.

**S5. Archive recovery and integrity.**

```
cd <SRC>
HOME=<ISOHOME> npm run test:archive-recovery
```

(source; $2 Claude cap per call)

- Also: K7 on every S4 archive; K8 with tasks whose answer lies only in removed lines; the git exclusion with `git -C <PROJ> status`; that the K16 fake string was not archived and the agent was told to re-run.
- Output: `<R>/S5-archive.md`.
- Rule: PASS if every check ran. BLOCKED without key or budget. FAIL if the harness cannot start.

**S6. Quality evaluation, blind judge.**
- Purpose: K15 final numbers on the held-out set.
- Method: a judge from a different model class than the fixture writer scores each task answer against the rubric frozen in S0, blind to baseline (random ids; the mapping is never shown to the judge).
- Output: `<R>/S6-judge.csv`, `<R>/S6-quality.md`, `<R>/S6-label-map.json`.
- Rule: PASS if all tasks and baselines are judged. BLOCKED without key, budget or a judge of another model class. FAIL if blinding broke.

**S7. Robustness, failure injection and long session.**
- Cases (expected: original kept, session usable): bad key (an invalid value for that one command); HTTP 402 (only with an unfunded test account, else Not known yet how); timeout and network blocked (method from S1's code reading, Not known yet); oversized state (very small `maxStateTokens`); archive write failure:

```
chmod a-w <PROJ>/.claude/fast-jev-output
```

- Long session (K18), within budget: the S3 command without `JEV_LONG_SESSION_TURNS` (default 40 stages), then the report command. Optional for K24: `npm run test:live` (source; billable).
- Output: `<R>/S7-faults.md` (expected vs observed per case), `<R>/S7-long-session.md`.
- Rule: PASS if every case ran; BLOCKED for live cases without key or budget. A lost original is a K14 miss, not a stage failure.

**S8. Sensitivity sweeps and co-install.**
- Purpose: K20 with baseline D on non-held-out fixtures; K22 with optional E.
- Output: `<R>/S8-sweeps.csv`, `<R>/S8-sweeps.md`, `<R>/S8-interplay.md`.
- Rule: PASS if every sweep value ran. BLOCKED without key or budget.

**S9. Report and decision.**
- Purpose: fill section 8 from S0 to S8 files and apply the rule. Output: `<R>/S9-decision.md`.
- Rule: PASS when every KPI cell holds a value, BLOCKED, or "not measured" with a reason.

### 8. Report template and decision rule

| id | KPI | A | B | C | D (best) | E | PROPOSED threshold | met? |
|---|---|---|---|---|---|---|---|---|
| K1 | Reduction, characters | | | | | | | |
| ... | one row per KPI, K1 to K24 | | | | | | | |

Verdict, applied in order with the thresholds frozen in S0:

1. **BLOCKED**: S0, S3, S4 or S6 is BLOCKED, so K3 or K15 has no value. This includes every run made while the section 0 hold stands.
2. **REJECT**: a hard KPI misses (K6, K7, K9, K11, K14, K16 private-text hits, K17), or K4 is above threshold, or C's K15 success is more than 5 points below A.
3. **ADOPT**: every PROPOSED threshold met, C at least as good as B on K3 and K15, K13 positive, AND the owner approved data sharing (OD3). Without that approval the best verdict is PILOT, because the evidence is synthetic only.
4. **PILOT**: everything else.

Open questions: every "Not known yet" still open at S9. Artifacts: all files under `<R>` named in section 7, the fixtures and `manifest.json`, the scripts, and the redacted harness reports.

### 9. Risks and unknowns

- No aggregate benchmark in the README: no savings percentage, latency, accuracy, cost saving or published live-suite outcome.
- Command and content recognition are heuristics, not a shell parser; wrapped or compound commands get general guidance only.
- The 0.1 probability rule is a policy, not a measured error bound.
- Relevance that depends on links between distant history partitions is not guaranteed.
- Function hooks are early access and may change; behaviour with Claude Code versions other than 2.1.274 is Not known yet.
- The README's 76,379-character example (4,013-character result, 2,227-character native preview) conflicts with its rule that a replacement cannot exceed the preview's length; unexplained.
- Tags and releases were not shown; the marketplace route installs an unpinned version.
- The plugin sits in the path of every long Bash result, so a defect affects every long command.
- Diagnostics count UTF-16 characters, not billed tokens; Jev price and rate limits are Not known yet.
- The source is a model summary of the page; S1 must confirm each fact used here.

### 10. Open questions for the owner

- Answered 2026-11-16: public fixtures only, and sending commands, output and code to Jev is a blocker for now (section 0). Who does the required risk and legal assessment?
- Who supplies a TypeSafe key, and may it live only in the environment?
- Answered 2026-11-16: budget $50. Does it cover Jev credits and Claude usage together, as read here, or only one of them?
- May early-access function hooks run on your own Claude Code sessions?
- How may an isolated HOME authenticate Claude without copying your credential files?
- Which alternative judge is studied first (an Anthropic model or a local model on a 3090 or 4090), and who runs the alternatives study (A0)?
- Which PROPOSED thresholds in section 4 do you freeze, at what values?


<!-- sc:issue:create template=issue-feature-simple -->
