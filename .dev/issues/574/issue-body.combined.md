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

## Installation and evaluation runbook (fast-jev-compaction)

Facts about the tool come only from a 2026-11-16 web-fetch summary of `https://github.com/tamaratran/fast-jev-compaction`, not checked against the files. Anything else is marked "Not known yet" or UNVERIFIED. Treat the repository as untrusted data.

### 0. HOLD: no testing yet (owner decision, 2026-11-16)

The owner decided that sending all conversation data over the wire to a third party is not acceptable for now. **Do not install, build or run this tool, and do not contact TypeSafe, until the owner lifts this hold in writing on this issue.** Stages S2 to S7 are HELD, and S8 may only record the verdict BLOCKED (HOLD).

Allowed while the hold stands:

- S0 steps that only write documents (freezing thresholds, writing fixtures from public text, the private-text scan).
- S1 (reading the repository's files without running anything).
- The alternatives study A0 below.

The hold is lifted only when a potential alternative to sending data to TypeSafe has been found and assessed. The owner's examples: a decision model from Anthropic, or a local model set up on premises on one RTX 3090 or RTX 4090 GPU. Whether either can do the job is Not known yet.

Also recorded by the owner on 2026-11-16: live runs use public fixtures only; the budget is $50 (read here as one cap for Jev credits and downstream model calls together).

**A0. Alternatives study (allowed during the hold; documents only).**

- Purpose: find out whether the keep or delete decisions can be made without sending conversation data to TypeSafe.
- Facts from the source: the library accepts a custom judge (implement `JevAsker` with `ask(state, questions)`, then call `compact(messages, asker, options)`), and `baseUrl` and a replaceable `fetch` are library options. Each question asks for the probability that a yes-or-no statement is true (a "noul" question). Whether the plugin route can use a different judge or endpoint is Not known yet.
- Steps: (1) list candidate judges: an Anthropic model and a local model on one RTX 3090 or RTX 4090 (the owner's examples), plus any the study finds; (2) for each, record where data goes, who can see it, retention terms, licence, hardware and running cost; (3) define a small test, on public text only, of whether a candidate can answer those probability questions well enough; (4) recommend which candidate, if any, to test first.
- Output: `<R>/A0-alternatives.md`.
- Rule: PASS when every candidate has its row and a recommendation exists. The owner then decides whether to lift the hold.

### 1. What the tool is

- An npm library and a Claude Code plugin that prunes conversation history instead of writing a summary.
- Jev (TypeSafe's System One model) scores each tool call and result: keep, keep the call with a truncated result, or delete.
- User and assistant prose stays unchanged and in order; retained content is not rewritten.
- Jev receives prose and tool inputs, with tool outputs replaced by short placeholders, fitted into `maxStateTokens` (default 25000).
- Keep the result if `keepResult` >= `keepThreshold` (0.5); else keep the call plus the first `truncateHeadChars` (300) characters if `keepCall` >= `keepThreshold`; else delete both.
- The first message and the newest `preserveRecentMessages` (6) messages are protected.
- The plugin (`hooks/fast-jev.ts`) replaces `/compact` and automatic compaction; on errors or too little reduction it falls back to Claude Code's built-in summarisation.
- The README reports no numbers for latency, savings, accuracy or comparisons.

### 2. Gates and safety (read before any install step)

**G1. Data leaves the machine (hard rule).** Every compaction sends the conversation representation (user and assistant prose, tool inputs, placeholders for tool outputs) to `https://api.typesafe.ai/v1/systemone` with `TYPESAFE_API_KEY`. The owner's approval for sending private text to TypeSafe/Jev is NOT established (open item OD3 in the blocker-classifier work, IronClaude#552; the Jev plugin install is IronClaude#553). Owner answer, 2026-11-16: public fixtures only. Once the section 0 hold is lifted, every run that calls the live API uses only synthetic or public fixtures: no private repository text, no IronClaude source, no secrets, no client data. The S5 plugin session runs in an empty scratch directory, never in a repository.

Checklist item, ticked in `S0-gates.md` before stage S3 starts:

- [ ] Every input that will reach the live API is synthetic or public, the section 6 private-text scan passed, and no live run will start in or near a private repository.

**G2. The key.** `TYPESAFE_API_KEY` comes from the environment only. A human (the owner or someone the owner names) exports it in the executor's shell before the session. Never print it, never write it to a file (including `~/.typesafe_key` and any `settings.json`), never type it on a logged command line, and redact it in every log as `[REDACTED]`. Check presence without printing it:

```
test -n "${TYPESAFE_API_KEY:-}" && echo key-present || echo key-absent
```

Without a key, stages S3, S5, S6 and the live parts of S4 and S7 end as BLOCKED, not failed.

**G3. Claude Code version and early-access hooks.** The plugin needs Claude Code 2.1.274 or newer and the early-access variable `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS`. Not known yet whether this workspace meets it. S0 records:

```
claude --version
```

Below 2.1.274, S5 is BLOCKED. Behaviour with versions other than 2.1.274 is Not known yet.

**G4. Isolated HOME for every plugin test.** Enabling the plugin changes `/compact` and automatic compaction for that session, so never install or enable it in the owner's real `~/.claude`. Create a temporary HOME, pass it to one command at a time, delete it afterwards:

```
mktemp -d /tmp/fastjev-home.XXXXXXXX
HOME=<ISOHOME> claude --version
rm -rf <ISOHOME>
```

The settings directory is then `<ISOHOME>/.claude`. Whether Claude Code reads configuration outside HOME is Not known yet; record what you observe. How Claude Code authenticates inside a fresh HOME here is Not known yet. Never copy the owner's credential files into `<ISOHOME>`; if the session cannot authenticate, S5 is BLOCKED.

**G5. Third-party code.** Pin the exact commit and record it. Before running anything, read `hooks/fast-jev.ts` and `package.json` (scripts and dependencies, especially any `preinstall`, `install`, `postinstall` or `prepare` script). Run installs only in throwaway directories under `/tmp`. No change to IronClaude source files. Python here is UV-only; the tool is npm, so its `node_modules` never goes inside the repository or any IronClaude worktree.

**G6. Licence.** MIT (contents not shown by the source). S1 reads `LICENSE` and records "licence file read" and its first line.

### 3. Installation

Placeholders: `<SRC>` pinned checkout, `<LIBDIR>` library throwaway directory, `<ISOHOME>` isolated HOME, `<PIN>` recorded commit. Commands marked (source) appear in the source file; git, mktemp, cp and rm are standard tooling, not from the README.

**Step 1. Read-only inspection of a pinned checkout.**

```
mktemp -d /tmp/fastjev-src.XXXXXXXX
git clone https://github.com/tamaratran/fast-jev-compaction <SRC>
git -C <SRC> rev-parse HEAD
```

- Expected: folders `.claude-plugin`, `demo/JevDemo`, `examples`, `hooks`, `src`, `tests`, `types`; files `LICENSE`, `package.json`, `package-lock.json`.
- Verify: record `<PIN>`; read `LICENSE`, `package.json`, `hooks/fast-jev.ts`, `hooks/README.md`, `.claude-plugin/marketplace.json`.
- Undo: `rm -rf <SRC>`.

**Step 2. Library route (throwaway directory).**

```
mktemp -d /tmp/fastjev-lib.XXXXXXXX
cd <LIBDIR>
npm install fast-jev-compaction
```

(source: `npm install fast-jev-compaction`)

- Expected: `<LIBDIR>/node_modules/fast-jev-compaction`.
- Verify: record the version from its `package.json`. Whether the npm version matches `<PIN>` is Not known yet; record both.
- Undo: `rm -rf <LIBDIR>`.

**Step 3. Offline checks in the pinned checkout (no key in the environment).**

```
cd <SRC>
test -n "${TYPESAFE_API_KEY:-}" && echo key-present || echo key-absent
npm install
npm run typecheck
npm test
npm run build
HOME=<ISOHOME> npm run validate:plugin
```

(source: `npm install`, `npm run typecheck`, `npm test`, `npm run build`, `npm run validate:plugin`)

- Expected: `key-absent`, then exit 0 for each npm command. Unit tests use a fake Jev. `validate:plugin` calls `claude plugin validate`, so it gets the isolated HOME.
- Verify: record exit code, duration and test counts per command.
- Undo: `rm -rf <SRC>/node_modules`.

**Step 4. Live demo (only after G1, G2 and the S0 checklist).** The source form reads the key from a file, which G2 forbids:

```
TYPESAFE_API_KEY="$(cat ~/.typesafe_key)" npm run demo
```

Use instead, with the key already exported by the human:

```
cd <SRC>
npm run demo
```

- Expected: one live compaction of the demo input. What that input contains is Not known yet; read it first and confirm it is synthetic.
- Verify: exit 0; save output with the key redacted; check `git -C <SRC> status` for files the demo wrote (Not known yet).
- Undo: delete any files it wrote.

**Step 5. Plugin route (isolated HOME only).** Preferred for measured runs, because it uses the pinned checkout:

```
cd <SRC>
HOME=<ISOHOME> CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude --plugin-dir .
```

(source: `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude --plugin-dir .`; the `HOME=` prefix is added here)

Marketplace route, for the install-effort KPI only (it installs whatever the repository serves at that moment, not `<PIN>`):

```
HOME=<ISOHOME> claude plugin marketplace add tamaratran/fast-jev-compaction
HOME=<ISOHOME> claude plugin install fast-jev-compaction@fast-jev-compaction
```

- The source puts `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS` and `TYPESAFE_API_KEY` under `env` in `~/.claude/settings.json`. Here, write only `{"env": {"CLAUDE_CODE_ENABLE_FUNCTION_HOOKS": "1"}}` to `<ISOHOME>/.claude/settings.json` with the Write tool; the key stays in the environment (the source says defaults use the environment credential). Leave the install prompt's API key empty. Where prompt answers are stored is Not known yet.
- Then restart Claude Code or run `/reload-plugins` (source).
- Expected: `/compact` and automatic compaction use Jev; a notification reports retained and total messages, or explains the fallback.
- Verify the key was not stored (prints file names only; must print nothing): `grep -rlF "$TYPESAFE_API_KEY" <ISOHOME>`.
- Undo: an uninstall command is Not known yet; delete the whole isolated HOME (Step 6).

**Step 6. Uninstall and cleanup.**

```
rm -rf <ISOHOME>
rm -rf <LIBDIR>
rm -rf <SRC>
```

Then confirm the real `~/.claude/settings.json` modification time equals the value recorded in S0, and that no `node_modules` exists in the IronClaude checkout or its worktrees.

**Not evaluated: the macOS SwiftUI demo** (`demo/JevDemo/build.sh`). It is scripted, makes no API calls and runs on macOS only, so it is no evidence of real behaviour.

### 4. KPIs

Every threshold is PROPOSED and must be frozen by the owner in `S0-frozen.md` before the first measured run. No threshold is justified by the tool's README, which reports no benchmark numbers. A to E are the baselines in section 5.

| id | KPI | definition and formula | how an agent measures it | instrument | starting threshold |
|---|---|---|---|---|---|
| K1 | Reduction, characters | 1 - chars_after / chars_before per fixture; median and min | recount characters of input and output; compare with `result.stats` | bench script (S4) | PROPOSED median >= 0.25 (mirrors the README's illustrative fallback check, not a benchmark) |
| K2 | Reduction, real tokens | 1 - tokens_after / tokens_before by a separate tokenizer (the tool's counts are estimates); also the estimate's error | count input and output with one independent tokenizer | independent token counter (which one: Not known yet; record name and version) | PROPOSED median >= 0.25 |
| K3 | Decision mix | share per reason: keep result, keep call with truncated result, delete | count `result.decisions` by reason | bench script | no threshold, report only |
| K4 | Critical-fact survival | canaries present after / planted (paths, error messages, constraints such as "do not edit src/generated", commands) | exact-string search of the compacted transcript | canary script | PROPOSED >= 0.95 and not below B |
| K5 | Downstream task success | share of follow-up tasks solved from the compacted history; D vs A, B, C | run each fixture's follow-up task per baseline; judge with the frozen rubric | task runner plus blind judge (S6) | PROPOSED D >= B, and D within 5 points of A |
| K6 | Verbatim preservation | retained messages byte-identical to input / retained messages | byte comparison per retained message | integrity script | PROPOSED 100% |
| K7 | Protected-message preservation | first and newest `preserveRecentMessages` messages unchanged / expected | byte comparison at protected positions | integrity script | PROPOSED 100% |
| K8 | Structural integrity | every tool_result has its tool_use, no empty messages, valid schema | pair by `tool_use_id`, validate schema | integrity script | PROPOSED 100% |
| K9 | Latency | p50 and p95 wall time per compaction; requests per compaction | timer around `compactMessages`; requests from `result.stats` | bench script | PROPOSED p95 <= 30 s; requests report only |
| K10 | Jev cost and calls | calls x price (price Not known yet) vs downstream tokens saved x model price | count requests with a wrapped `fetch`; savings from K2 | fetch wrapper | no threshold, report only |
| K11 | Failure and fallback | per case (bad key, timeout, malformed answer, history too large, reduction too small): clean error or fallback / cases; live errors / live runs | inject faults via the `fetch` option or a custom `JevAsker` (S7) | fault script | PROPOSED 100% clean handling; live error rate <= 5% |
| K12 | Repeatability | same input 3 times: share of calls with the same decision in all runs | compare `result.decisions` | bench script | PROPOSED >= 0.90 |
| K13 | Threshold sensitivity | K1, K4, K5 at `keepThreshold` 0.3, 0.5, 0.7 and `preserveRecentMessages` 4, 6, 10 | sweep on non-held-out fixtures | bench script | no threshold, report only |
| K14 | Recovery cost | share of deleted results re-run downstream; extra tool calls and tokens | count re-runs of tools whose results were deleted | task runner logs | PROPOSED <= 10% of deleted results |
| K15 | Prompt-cache effect | cache read and write tokens on the 3 turns after compaction, vs B | Not known yet how; proposed: read cache usage fields from the downstream model's API or headless output, same prompts per baseline | task runner logs (UNVERIFIED that fields are exposed) | no threshold, report only |
| K16 | Privacy exposure | characters and field names sent per compaction; private-text hits in sent bodies | wrapped `fetch` logs body length and top-level field names (no headers); run the section 6 scan on sent bodies | fetch wrapper | PROPOSED 0 private-text hits (hard); sizes report only |
| K17 | Install and operational effort | steps, restarts, failures, minutes per route | executor logs each section 3 step | stage logs | no threshold, report only |
| K18 | Interplay with built-in compaction | fallback frequency; whether automatic compaction triggers Jev; session usable after fallback | observe notifications and session state in S5 | S5 log | PROPOSED usable after fallback 100%; rest report only |

### 5. Baselines

- **A. No compaction**: the full history (quality ceiling, zero savings).
- **B. Claude Code built-in summarising compaction**: `/compact` in S5 with the plugin disabled. How to load a synthetic transcript into a session is Not known yet; if impossible, use B-proxy (a fixed summarisation prompt to the same model, frozen in S0) and label B results as proxy.
- **C. Naive drop**: delete the oldest tool results until D's character reduction is reached, keeping prose and pairing (short script in S4).
- **D. fast-jev defaults**: `keepThreshold` 0.5, `preserveRecentMessages` 6, other README defaults.
- **E. fast-jev sweeps**: `keepThreshold` 0.3, 0.5, 0.7 and `preserveRecentMessages` 4, 6, 10, one parameter at a time.

### 6. Fixtures

- **Content**: public or generated text only. No IronClaude source, private repository text, secrets or client data.
- **Set**: at least 12 synthetic transcripts in three kinds (debugging, refactoring, research) and three sizes (about 20k, 60k and 150k tokens by the tool's estimate), every kind and size covered, plus a held-out set of at least 3 never used for threshold choices.
- **Format**: Claude Code session messages with `tool_use` and `tool_result` blocks (the README says `Message` is a subset of Claude Code's `SessionMessage`).
- **Canaries**: at least 8 unique exact strings per transcript (file paths, error messages, constraints such as "do not edit src/generated", commands), some in prose and some only in tool results, each with a follow-up question that needs it; record each location.
- **Seed**: 20261116 for every random choice; record the generating model.
- **Location**: `.dev/eval-workspaces/fast-jev-compaction/fixtures/` (outside every source directory) with `manifest.json` (file, kind, size, seed, canaries, held-out flag).
- **Private-text check** (must pass before S3): scan for IronClaude-specific strings, owner names, internal hostnames and key-like patterns:

```
grep -rniE "superclaude|ironclaude|ironbelly|api[_-]?key|secret|BEGIN [A-Z ]*PRIVATE KEY" .dev/eval-workspaces/fast-jev-compaction/fixtures/
```

Expected: no output, or only hits a human confirms are planted synthetic canaries.

### 7. Agentic procedure (stages S0 to S8)

**Who runs it.** Each stage is one supervised Orca worker, one stage per worker, dispatched by the coordinator per the Orca orchestration guide. Every worker records the model it actually served, writes results only as files under `.dev/eval-workspaces/fast-jev-compaction/results/` (`<R>` below), and never merges, pushes or posts. Worker task spec fields:

- **target**: the stage and its input files;
- **change**: only the stage's output files and `/tmp` throwaway directories;
- **constraints**: sections 2 and 6; no IronClaude source changes; no key in any file or log;
- **ownership**: only its output files and its `/tmp` directories, deleted at the end;
- **observable acceptance**: the output file exists, has a `status:` line (PASS, FAIL or BLOCKED) and the stage's evidence.

Every output file starts with: stage, date, worker, served model, `<PIN>`, `claude --version`, status.

**S0. Gates and prerequisites.**
- Purpose: check G1 to G6; freeze thresholds, rubric, judge model and the B method; build fixtures.
- Commands: `claude --version`; the G2 presence check; record the real `~/.claude/settings.json` modification time (read only). Fixtures by a worker whose model is recorded, then the section 6 scan.
- Output: `<R>/S0-gates.md` (with the G1 tick box), `<R>/S0-frozen.md`, fixtures and manifest.
- Rule: PASS if version >= 2.1.274, the scan passes and thresholds are frozen. BLOCKED if thresholds are not frozen, or while the section 0 hold stands (a missing key blocks only live stages). FAIL if the scan finds private text.

**S1. Read-only inspection and licence.**
- Purpose: pin the commit and review code before anything runs.
- Commands: section 3, Step 1.
- Output: `<R>/S1-inspection.md`: `<PIN>`, licence read, install lifecycle scripts, dependencies, network endpoints in code, where the plugin reads the key, anything surprising.
- Rule: PASS if nothing unexpected. FAIL if code sends data beyond the documented endpoint or has unexpected install scripts (stop; the owner decides).

**S2. Offline build and tests.**
- Purpose: the pinned code builds and its tests pass without TypeSafe.
- Commands: section 3, Step 3.
- Output: `<R>/S2-offline.md` (exit codes, durations, test counts).
- Rule: PASS if all exit 0, else FAIL.

**S3. Live smoke test (one synthetic call).**
- Precondition: G1 tick in `S0-gates.md`.
- Script: write `.dev/eval-workspaces/fast-jev-compaction/scripts/smoke.mjs`: import `compactMessages` and `reductionRatio`, wrap the `fetch` option to log request count, body length and top-level field names (never headers), compact the smallest fixture once, write `result.decisions`, `result.stats` and the ratio to JSON. Copy it into `<LIBDIR>` so imports resolve from `<LIBDIR>/node_modules`:

```
cp .dev/eval-workspaces/fast-jev-compaction/scripts/smoke.mjs <LIBDIR>/
cd <LIBDIR>
node smoke.mjs <FIXTURE-ABSOLUTE-PATH> <R-ABSOLUTE-PATH>/S3-smoke.json
```

- Output: `<R>/S3-smoke.json`, `<R>/S3-smoke.md`.
- Rule: PASS if one compaction returns valid output. BLOCKED without key or G1 tick. FAIL on any other error (redacted).

**S4. Library benchmark.**
- Purpose: K1 to K4, K6 to K10, K12, K13, K16 for A, C, D, E.
- Scripts (same copy-and-run pattern): `bench.mjs` (D once, D twice more for K12, E sweeps, C; save every output; time each call), `integrity.mjs` (K6 to K8), `canary.mjs` (K4), plus the independent token count (K2).
- Output: `<R>/S4-outputs/`, `<R>/S4-metrics.csv` (row per fixture, baseline, run), `<R>/S4-bench.md`.
- Rule: PASS if every fixture ran for every baseline. BLOCKED without key. FAIL if scripts cannot run. KPI misses are recorded, not stage failures.

**S5. Plugin integration, isolated headless session.**
- Purpose: K17, K18 and baseline B in a real session.
- Commands: section 3, Step 5 in `<ISOHOME>`, working directory an empty `/tmp` scratch directory with one synthetic task. Headless (print) mode flags are not in the source: check `claude --help` first. Run until `/compact`; repeat with the plugin disabled for B. Then Step 6.
- Output: `<R>/S5-plugin.md` (notifications, fallbacks, restarts, steps, minutes, key-not-stored check), `<R>/S5-session-logs/` (redacted).
- Rule: PASS if Jev compaction or a reported fallback happens and the session stays usable. BLOCKED if version < 2.1.274, no key, or no authentication in the isolated HOME. FAIL if the session breaks or the key is found in `<ISOHOME>`.

**S6. Quality evaluation, blind judge.**
- Purpose: K5, K14, K15.
- Method: run each fixture's follow-up task on A, B (or B-proxy), C and D outputs. A judge from a different model class than the fixture writer scores against the rubric frozen in S0, blind to baseline (outputs relabelled with random ids; the mapping file is never shown to the judge). Final numbers use the held-out set.
- Output: `<R>/S6-judge.csv`, `<R>/S6-quality.md`, `<R>/S6-label-map.json`.
- Rule: PASS if all fixtures and baselines are judged. BLOCKED without key or a judge of another model class. FAIL if blinding broke.

**S7. Robustness and failure injection.**
- Purpose: K11.
- Script: `faults.mjs`: timeout and malformed answer via the `fetch` option or a custom `JevAsker` (offline); bad key via a deliberately invalid value (live, synthetic input); history too large via a tiny `maxStateTokens`; reduction too small via a fixture with almost no tool output (library: ratio below 0.25; plugin: fallback in an S5-style session).
- Output: `<R>/S7-faults.md` (expected vs observed per case).
- Rule: PASS if every case ran; BLOCKED for live cases without key. A crash or corrupted output is a K11 miss, not a stage failure.

**S8. Report and decision.**
- Purpose: fill section 8 from S0 to S7 files and apply the rule.
- Output: `<R>/S8-decision.md`.
- Rule: PASS when every KPI cell holds a value, BLOCKED, or "not measured" with a reason.

### 8. Report template and decision rule

| id | KPI | A | B | C | D | E (best) | PROPOSED threshold | met? |
|---|---|---|---|---|---|---|---|---|
| K1 | Reduction, characters | | | | | | | |
| ... | one row per KPI, K1 to K18 | | | | | | | |

Verdict, applied in order with the thresholds frozen in S0:

1. **BLOCKED**: S0, S3, S4 or S6 is BLOCKED, so K4 or K5 has no value. This includes every run made while the section 0 hold stands.
2. **REJECT**: a hard KPI misses (K6, K7 or K8 below 100%, or K16 private-text hits above 0), or K4 is below threshold, or D's K5 is more than 5 points below B.
3. **ADOPT**: every PROPOSED threshold met, D at least as good as B on K4 and K5, K10 shows a net saving, S5 passed, AND the owner approved data sharing (OD3). Without that approval the best verdict is PILOT, because the evidence is synthetic only.
4. **PILOT**: everything else.

Open questions: every "Not known yet" still open at S8. Artifacts: all files under `<R>` named in section 7, the fixtures and `manifest.json`, and the scripts under `.dev/eval-workspaces/fast-jev-compaction/scripts/`.

### 9. Risks and unknowns

- No benchmark in the README: no latency, savings, accuracy or comparison numbers; the macOS animation is scripted.
- Only tool calls and results can be deleted; prose is never shortened, so prose-heavy sessions may reduce little.
- The tool's token counts are estimates (about one token per six letters, calibrated slightly above Jev's counts).
- A probability does not prove a deletion is safe; recovery is re-running the tool (K14).
- Each request repeats the fitted state; near the state limit one request per small group of questions may be needed, raising requests, cost and latency.
- Tags and releases were not shown; the marketplace route installs an unpinned version.
- Function hooks are early access; behaviour with Claude Code versions other than 2.1.274 is Not known yet.
- Install prompts may store settings, possibly the key, in an unknown place (checked in S5).
- Loading a synthetic transcript into a session for baseline B is Not known yet.
- Jev pricing and rate limits are Not known yet.
- The source is a model summary of the page; S1 must confirm each fact used here.

### 10. Open questions for the owner

- Answered 2026-11-16: public fixtures only, and sending all conversation data over the wire is not acceptable for now (section 0). Does the risk and legal assessment you required for jev-pruner also apply here, and who does it?
- Who supplies a TypeSafe key, and may it live only in the environment?
- Answered 2026-11-16: budget $50. Does it cover Jev credits and downstream model calls together, as read here?
- May early-access function hooks run on your own Claude Code sessions?
- Which alternative judge is studied first (an Anthropic model or a local model on a 3090 or 4090), and who runs the alternatives study (A0)?
- Which PROPOSED thresholds in section 4 do you freeze, at what values?


<!-- sc:issue:create template=issue-feature-simple -->
