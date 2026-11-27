# Summary: #611 Keyword-baseline analysis for the Jev comparison

- Issue: https://github.com/IronbellyOrg/IronClaude/issues/611
- Type: feature
- Complexity: medium (rubric: `refs/claim.md`)
- Effort estimate: 10 hours
- spec-route: design — A single, bounded evaluation has explicit acceptance criteria; the remaining owner decisions can be recorded as execution prerequisites.

## What the issue asks for

Compare the corrected troubleshoot keyword table with Jev on about 30 human-labelled public historical prompts, and record a decision about whether a later preflight is justified. This analysis follows `/sc:analyze` without a depth override on `src/superclaude/skills/sc-troubleshoot-protocol/`, with the command interface, related tests and #871's verification artifacts as supporting evidence. It is a static review, not an evaluation run, and uses the issue-summary template's existing sections because the issue-protocol template directory contains no separate analysis-report template. No source was changed, tests executed, key accessed, prompt submitted, or TypeSafe/model endpoint called.

## Relevant files and systems (cheatsheet)

| Path or system | Why it matters |
|---|---|
| `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` | Markdown instruction protocol, not an executable classifier. Wave 0 at lines 145–183 specifies the baseline. |
| `src/superclaude/commands/troubleshoot.md` | Markdown public interface; lines 50–52 distinguish the six-way type choice from depth and scope. |
| `.dev/tasks/done/TASK-WF-issueSummary-20261126-115114/artifacts/manual-evidence.txt` | Prior #610 verification and its limitations; lines 2–12 distinguish observed Wave 0 classification from installed-command resolution and clean CLI execution. |
| `.dev/tasks/done/TASK-WF-issueSummary-20261126-115114/artifacts/classification-exact/audit.log` | Prior source-skill observation: the everyday loading prompt selects performance without a type override. |
| `.dev/tasks/done/TASK-WF-issueSummary-20261126-115114/artifacts/classification-leak/audit.log` | Prior source-skill observation: ambiguous leak leaves type unset and retains security candidates. |
| `docs/memory/reflect/deviation-patterns-issue-610.md` | Warns against claiming runtime coverage from merely updating a mirror. |
| `tests/troubleshoot/` | Existing diagnostic-protocol/backtest tests. Bounded phrase/Jev searches did not find an evaluation matcher; these tests do not establish the requested comparison. |
| `.dev/` | Requested location for the future frozen corpus and result record; exact evaluation subdirectory is Not known yet. |
| TypeSafe, #609 and #612 | External live-call boundary, parent decision record, and conditional follow-up product issue; none is modified by this review. |

## Analysis

Codegraph: index_state=fresh, checked_at=2026-11-26T13:56:18Z; degraded: graph:unlisted

Readiness: worktree_root=`/home/coder/workspaces/worktrees/IronClaude/issue-611`; access=cli. The opt-out switch was not set, no active init/index process was found, one guarded CLI `codegraph status` reported an up-to-date index, and `codegraph --version` returned the pinned 1.6.2. MCP lookup tools and Augment/auggie were not available in the actual tool list. All discovery, scanning and impact reasoning therefore used Glob, Grep and Read; no graph lookup, initialization or synchronization was performed. Markdown protocol files are outside codegraph's symbol index in any event.

**Baseline and discovery.** HEAD and `origin/integration` are `37765a800d0b232cc231cf58b796fec23b26f8a8`. The table-file Git blob is `76bcb3d94182371250ffe99a7b60b9124b05c368`. Commit `949a70aa4` from #871 added the three everyday performance phrases and expanded the existing leak ambiguity explanation. The PR merged and closed #610. The earlier #653 command/skill diff changes remediation routing, not type detection. The saved 134 merged-PR titles/file manifests were screened for this area; individual returned file-list completeness remains unverified.

**Quality and correctness findings.**

- **Medium — stale prerequisite information.** The November 24 review and the findings linked from the November 26 comment say #610 is open and the phrases absent. Current `SKILL.md:155–159` contradicts that source premise. Use the repaired revision as the baseline and retain the old review only as history. This removes the source prerequisite, not the owner-approval prerequisites.
- **Medium — an invented baseline parser would invalidate the comparison.** `SKILL.md:152–159` calls for keyword plus structural cues and explicitly abstains on ambiguity; it does not specify case handling, phrase normalization or a first-match implementation. “leak” belongs to two rows for a reason. Document and freeze the exact method used to apply this prose, including ambiguous cases, without adding new inference rules or silently improving the table. If actual skill execution is selected, record which copy and revision executed; if manual application is selected, record that it is manual rather than runtime measurement. Choice of method is Not known yet.
- **Medium — scoring details remain unsettled.** #611 gives six labels plus “none fits”, abstention, error and probability requirements, but does not fix the numeric improvement margin, acceptable median latency, exact threshold endpoints, treatment of none-fit abstentions, or accuracy denominator for failed calls. Before a live run, record these decisions and freeze them with the labels. Recommendation, not an approved rule: retain every attempted prompt in the result table and report failures separately so errors cannot disappear from the comparison.

**Security and data-handling finding.**

- **High — live sending and key use are gated.** The issue expressly asks for owner approval to send the chosen public prompts to TypeSafe, a budget, and use of `TYPESAFE_API_KEY`. Its historical hold-lift statement and the earlier evaluations' $50 budgets are not authorization for this experiment. No such approval appears in the supplied body/comments. Keep live work blocked until the specific approval and cap are recorded; check public provenance and remove secrets before any later submission. Never print or persist the key. This is an experiment boundary review, not a request to change a security subsystem.

**Performance and cost.** The issue requests pinned `jev-1.14.0`, one request per prompt with a six-way Choice and companion fit Noul, and an uncertainty band between 0.3 and 0.7. It quotes about $0.00004 per call at $0.042 per million input tokens and says under $1 should suffice. These are issue-text estimates, not verified current prices or an approved cap. This comparison's actual median/slowest latency, accuracy, abstention, error rate and spend are Not known yet; no benchmark was run. Confirm the requested pin, API contract and pricing at execution time without substituting an alias or model silently.

**Architecture and impact.** No production CLI, hook, gateway, installed primitive or troubleshoot behavior needs modification to satisfy #611. Its deliverables are one fixed question file, a frozen labelled corpus and a reproducible result/decision record under `.dev/`, followed by coordinator-owned issue updates. #609 receives the decision; #612 proceeds only on a positive result under the rule fixed beforehand. No depth/scope comparison or product preflight belongs in this issue.

**Evidence metrics and limits.** The source interface has six type categories, one three-phrase baseline extension, and a deliberate two-row “leak” overlap; the requested sample is about 30, not a collected sample of 30. #871's retained verification reports four namespaced Wave 0 observations and 404 tests passing. Its corrected CLI process still ended with a budget error after the observations; the global skill stayed old. Those historical records were read, not rerun. No new test pass, runtime classification, external availability, price, latency or model-quality result is claimed by this static analysis. Searches do not establish absence of work in other checkouts or unpushed branches.

**Smallest complete next-work sequence.**

1. Record the repaired table revision and the selected method for applying it. Choose about 30 historical public prompts with provenance covering all six types and ambiguous/none-fit cases; freeze human labels before either arm runs.
2. Freeze the question file, uncertainty/error/scoring rules, owner-set improvement margin and acceptable median latency. Obtain explicit sending/budget/key-use approval. Preparation is not permission to call the service.
3. Check the future scorer offline with a unique performance cue, an ambiguous leak, a none-fit case, uncertainty-band boundaries and an injected call failure; verify totals and median/slowest calculations using synthetic results. Do not contact a model for these checks.
4. Only after approval, execute the bounded comparison under the fixed cap, preserving probabilities, per-prompt answers, abstentions, failures and latency. Stop rather than exceed the cap or hide errors.
5. Recompute the aggregate numbers from the retained rows, apply the pre-agreed decision unchanged, and hand the records to the coordinator for #611/#609/#612 updates. No source implementation is needed.

Effort estimate: 3 hours for corpus/provenance/labels, 2 for the fixed protocol and scoring record, 2 for offline checks, 1 for the approved run and measurement capture, and 2 for analysis/decision handoff: **10 active hours**, excluding waiting for owner decisions. This fits Medium's over-4-to-16-hour rubric in one evaluation area, with no production security or data-migration change. The actual approval, live experiment and subsequent issue updates remain unperformed.
