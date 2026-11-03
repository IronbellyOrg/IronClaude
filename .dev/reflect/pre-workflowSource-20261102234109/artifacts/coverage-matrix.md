# Coverage matrix (Wave 1B, UC-1 pre)

- Spec: `.dev/tasks/to-do/TASK-WF-workflowSource-20261102-233731/source.md` (52 lines)
- Tasklist: `.dev/tasks/to-do/TASK-WF-workflowSource-20261102-233731/TASK-WF-workflowSource-20261102-233731.md` (66 tasks)
- Item detail: `.dev/releases/current/v5.0.0/post-release/CONSOLIDATED-PLAN.md`
- Generator: `/tmp/wave1b_coverage_mapper.py` (deterministic; `uv run python`)

## Pass 1 (regex, authoritative)

`ID_REGEX = \b(R-\d+|REQ-\d+|SPEC-\d+|T-\d+)\b`, fenced code skipped.

- Hits: **0** 

## Pass 2 (inferred requirements) and containment matching

Containment rule: case-fold; tokens `[a-z0-9]+([-_./'][a-z0-9]+)*`; unique content words after stripping a fixed stopword set (articles, conjunctions, prepositions, auxiliaries); ratio = |quote words in task text| / |quote words|; task text = `## Task N:` heading through the line before the next `## ` heading; best ratio wins, first task on ties; match at ratio >= 0.6, else `none`.

Rows dropped for missing quote or citation: 0

| id | kind | quote | citation | best task | ratio | match_method | content words | plan-wide carriage (semantic note, not a match) |
|---|---|---|---|---|---|---|---|---|
| INF-001 | What | update and create IronClaude's external-surface artifacts for the shipped 5.0.0 release, exactly as itemized in `.dev/releases/current/v5.0.0/post-release/CONSOLIDATED-PLAN.md` | source.md:3-4 | Task 8 | 0.1818 | none | 11 | carried: plan Goal (tasklist:15) and Constraints (tasklist:19) |
| INF-002 | Why | The release's docs must agree with the tagged code (v5.0.0 = d953b983). | source.md:8 | Task 3 | 0.2857 | none | 7 | carried: Goal (tasklist:15) and Constraints (tasklist:21-22) |
| INF-003 | In-scope 1 | Writer worklist, Workstream A** — items A-W1 … A-W22 (section "Writer worklist" → "Workstream A"), including the new `docs/user-guide/codegraph.md` (A-W22). A-W3 edits `src/superclaude/core/HOW-WE-WORK.md` and its byte-identical mirror `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (and the repo CLAUDE.md note about re-running the level-table copy applies if the level table changes; it should not). | source.md:12-15 | Task 6 | 0.2759 | none | 29 | - |
| INF-004 | In-scope 2 | Writer worklist, Workstream B** — items B-W1 … B-W22, including the four new technical notes under `docs/developer-guide/` (B-W19 codegraph-integration.md, B-W20 session-memory.md, B-W21 review-severity-rule.md, B-W22 release-procedure.md). B-W1 edits `src/superclaude/rules/core/changelog_maintenance.md` (an installed primitive). | source.md:16-18 | Task 47 | 0.3333 | none | 24 | - |
| INF-005 | In-scope 3 | Writer worklist, Workstream C** — items C-W1 (docs/getting-started/installation.md), C-W2 (docs/user-guide/mcp-installation.md), C-W3 (new docs/getting-started/upgrading.md). The verified install/upgrade evidence is the Workstream C e2e transcript `docs/testing/v5.0.0/c-e2e-transcript.txt` (GREEN, new user and 4.3.5→5.0.0 upgrade) and `docs/testing/v5.0.0/c-e2e-run.sh`. | source.md:19-22 | Task 3 | 0.2917 | none | 24 | - |
| INF-006 | In-scope 4 | Workstream D** — 16 user-facing human-test guides `docs/testing/v5.0.0/user/D01-…md` … `D16-…md` exactly as listed in "Test guide plan (D and E)", each built from `~/.claude/skills/sc-post-release-protocol/templates/user-test-guide.md` (Read the template; every expected result cites real code file:line, `--help` output or the e2e transcript; anything not derivable is marked UNVERIFIED; every step carries its cost tag `[FREE]`/`[LOCAL-WRITE]`/`[CLAUDE-SESSION]`/ `[API-LONG]`/`[PROXY]`/`[EXTERNAL]`). | source.md:23-28 | Task 48 | 0.3333 | none | 48 | - |
| INF-007 | In-scope 5 | Workstream E** — 2 sysop guides `docs/testing/v5.0.0/sysop/E01-ccsession-tier-policy.md` and `E02-ccsession-model-data-publishing.md` from `templates/sysop-test-guide.md`, with the gate evidence listed in the plan. | source.md:29-30 | Task 7 | 0.2500 | none | 12 | - |
| INF-008 | In-scope 6 | `docs/testing/v5.0.0/README.md` — index of D01-D16 and E01-E02 with cost tags, plus pointers to the e2e transcript and script. | source.md:31-32 | Task 66 | 0.5455 | none | 11 | - |
| INF-009 | Out-of-scope | Deferred gaps 71-84 and the out-of-scope code findings O1-O22 (no code changes; no issue filing in this plan). | source.md:36 | Task 2 | 0.2308 | none | 13 | carried: Constraints (tasklist:23) 'code findings O1-O22 are out of scope. Deferred gaps 71-84 are out of scope' |
| INF-010 | Out-of-scope | `docs/releases/v5.0.0.md`, `CHANGELOG.md` (published record), the GitHub release, the tag. | source.md:37 | Task 46 | 0.2857 | none | 7 | partially carried: Constraints (tasklist:23) bars docs/releases/v5.0.0.md and CHANGELOG.md; GitHub release and tag not named, but no task creates them and tasklist:28 'Commit nothing' |
| INF-011 | Out-of-scope | `post-release-report.md` and `post-release-manifest.json` (the post-release orchestrator writes them after this plan). | source.md:38 | Task 48 | 0.2500 | none | 8 | not carried in Constraints; no task writes post-release-report.md or post-release-manifest.json (grep: 0 hits) - honoured by omission |
| INF-012 | Constraint | Match on quoted text, not on scan line numbers (lines are from d953b983). | source.md:42 | Task 6 | 0.2222 | none | 9 | carried: Constraints (tasklist:20) |
| INF-013 | Constraint | After editing anything under `src/superclaude/` or `plugins/`, run `make sync-dev` and `make verify-sync`; never stage `.claude/` (only `.claude/settings.json` is tracked). No `src/superclaude/...` paths inside installed primitives. | source.md:43-44 | Task 26 | 0.4211 | none | 19 | carried (scoped): Constraints (tasklist:24) names the two src/ primitives; plugins/ mirror edit sits in Task 6, which runs make sync-dev + make verify-sync |
| INF-014 | Constraint | Repo is a fork: every `gh` call uses `--repo IronbellyOrg/IronClaude`; issue links point at IronbellyOrg/IronClaude. | source.md:45 | Task 46 | 0.4000 | none | 10 | partially carried: Constraints (tasklist:25) covers gh commands written into docs and IronbellyOrg links; plan executes no gh calls itself |
| INF-015 | Constraint | Do not run installs against the real `~/.claude`, real pipx, or running ccsession shims. | source.md:46 | Task 3 | 0.3333 | none | 9 | carried: Constraints (tasklist:26, tasklist:28) |
| INF-016 | Constraint | Verification per item: re-read the edited/created file against its plan item and the cited code; markdownlint (`make lint` covers markdown via pre-commit config if configured; otherwise `npx markdownlint-cli2` per repo config) and the repo's doc/primitive tests (`uv run pytest tests/ -q -k "doc or primitive or how_we_work or severity"` as a smoke, then the full `make test` once at the end). | source.md:47-50 | Task 6 | 0.2821 | none | 39 | partially carried: per-file markdownlint via npx markdownlint-cli@0.38.0 (tasklist:27, every task AC); pytest smoke '-k "doc or primitive or how_we_work or severity"' NOT in plan (only Task 6 runs '-k "how_we_work or routing or level_table"'); final full `make test` NOT in any task (grep: 0 hits) |
| INF-017 | Constraint | Commit nothing in this plan; the orchestrator commits and opens one PR with `/sc:pr-submit --monitor 3`. | source.md:51 | Task 54 | 0.3077 | none | 13 | carried: Constraints (tasklist:28) 'Commit nothing; the post-release orchestrator commits and opens the PR' |

## Worklist item and guide naming check (exactly one task each)

| item | tasks naming it | status |
|---|---|---|
| A-W1 | Task 4 | ok |
| A-W2 | Task 5 | ok |
| A-W3 | Task 6 | ok |
| A-W4 | Task 7 | ok |
| A-W5 | Task 8 | ok |
| A-W6 | Task 9 | ok |
| A-W7 | Task 10 | ok |
| A-W8 | Task 11 | ok |
| A-W9 | Task 12 | ok |
| A-W10 | Task 13 | ok |
| A-W11 | Task 14 | ok |
| A-W12 | Task 15 | ok |
| A-W13 | Task 16 | ok |
| A-W14 | Task 18 | ok |
| A-W15 | Task 19 | ok |
| A-W16 | Task 20 | ok |
| A-W17 | Task 21 | ok |
| A-W18 | Task 22 | ok |
| A-W19 | Task 23 | ok |
| A-W20 | Task 24 | ok |
| A-W21 | Task 25 | ok |
| A-W22 | Task 17 | ok |
| B-W1 | Task 26 | ok |
| B-W2 | Task 27 | ok |
| B-W3 | Task 28 | ok |
| B-W4 | Task 29 | ok |
| B-W5 | Task 30 | ok |
| B-W6 | Task 31 | ok |
| B-W7 | Task 32 | ok |
| B-W8 | Task 33 | ok |
| B-W9 | Task 34 | ok |
| B-W10 | Task 35 | ok |
| B-W11 | Task 36 | ok |
| B-W12 | Task 37 | ok |
| B-W13 | Task 47 | ok |
| B-W14 | Task 38 | ok |
| B-W15 | Task 39 | ok |
| B-W16 | Task 40 | ok |
| B-W17 | Task 41 | ok |
| B-W18 | Task 42 | ok |
| B-W19 | Task 43 | ok |
| B-W20 | Task 44 | ok |
| B-W21 | Task 45 | ok |
| B-W22 | Task 46 | ok |
| C-W1 | Task 1 | ok |
| C-W2 | Task 2 | ok |
| C-W3 | Task 3 | ok |
| D01 (`D01-install-upgrade-doctor.md`) | Task 48 | ok |
| D02 (`D02-mcp-servers.md`) | Task 49 | ok |
| D03 (`D03-codegraph-graph-impact.md`) | Task 50 | ok |
| D04 (`D04-session-memory.md`) | Task 51 | ok |
| D05 (`D05-routing-core-files-issue-templates.md`) | Task 52 | ok |
| D06 (`D06-plan-implement-review-cap.md`) | Task 53 | ok |
| D07 (`D07-pr-submit.md`) | Task 54 | ok |
| D08 (`D08-ccsession.md`) | Task 55 | ok |
| D09 (`D09-hooks-freshness-pragmatic.md`) | Task 56 | ok |
| D10 (`D10-sprint.md`) | Task 57 | ok |
| D11 (`D11-roadmap-tasklist.md`) | Task 58 | ok |
| D12 (`D12-reflect.md`) | Task 59 | ok |
| D13 (`D13-prd-portify-cleanup-audit.md`) | Task 60 | ok |
| D14 (`D14-swarm.md`) | Task 61 | ok |
| D15 (`D15-eval-harness.md`) | Task 62 | ok |
| D16 (`D16-init-lite-recommend-ic.md`) | Task 63 | ok |
| E01 (`E01-ccsession-tier-policy.md`) | Task 64 | ok |
| E02 (`E02-ccsession-model-data-publishing.md`) | Task 65 | ok |
| docs/testing/v5.0.0/README.md | Task 66 | ok |

Guide matching uses the exact plan filename (from the CONSOLIDATED-PLAN `Test guide plan (D and E)` tables) as it appears in the task text; Task 66 names the guides as an index by range (`D01-D16`), which is the in-scope item 6 deliverable, not a duplicate build.

- Items missing: none
- Items duplicated: none

## Target existence check

Update targets must exist; create targets must not exist yet. `named` = the path or its basename appears in the task text.

| task | mode | path | exists | expectation met | named in task |
|---|---|---|---|---|---|
| 1 | update | `docs/getting-started/installation.md` | True | yes | yes |
| 2 | update | `docs/user-guide/mcp-installation.md` | True | yes | yes |
| 3 | create | `docs/getting-started/upgrading.md` | False | yes | yes |
| 3 | update | `docs/getting-started/installation.md` | True | yes | yes |
| 3 | update | `README.md` | True | yes | yes |
| 4 | update | `README.md` | True | yes | yes |
| 5 | update | `docs/getting-started/quick-start.md` | True | yes | yes |
| 6 | update | `src/superclaude/core/HOW-WE-WORK.md` | True | yes | yes |
| 6 | update | `docs/user-guide/how-we-work.md` | True | yes | yes |
| 6 | update | `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` | True | yes | yes |
| 7 | update | `docs/user-guide/commands.md` | True | yes | yes |
| 8 | update | `docs/user-guide/flags.md` | True | yes | yes |
| 9 | update | `docs/user-guide/modes.md` | True | yes | yes |
| 10 | update | `docs/user-guide/agents.md` | True | yes | yes |
| 11 | update | `docs/user-guide/session-management.md` | True | yes | yes |
| 12 | update | `docs/user-guide/memory-system.md` | True | yes | yes |
| 13 | update | `docs/user-guide/mcp-servers.md` | True | yes | yes |
| 14 | update | `docs/user-guide/freshness-hooks.md` | True | yes | yes |
| 15 | update | `docs/user-guide/brainstorm.md` | True | yes | yes |
| 16 | update | `docs/user-guide/eval-pipeline.md` | True | yes | yes |
| 17 | create | `docs/user-guide/codegraph.md` | False | yes | yes |
| 17 | update | `README.md` | True | yes | yes |
| 17 | update | `docs/user-guide/mcp-installation.md` | True | yes | yes |
| 18 | update | `docs/swarm/README.md` | True | yes | yes |
| 18 | update | `docs/swarm/command-reference.md` | True | yes | yes |
| 18 | update | `docs/swarm/user-guide.md` | True | yes | yes |
| 18 | update | `docs/swarm/wizard-guide.md` | True | yes | yes |
| 18 | update | `docs/swarm/lens-catalog.md` | True | yes | yes |
| 19 | update | `docs/guides/sprint-cli-tools-release-guide.md` | True | yes | yes |
| 20 | update | `docs/guides/reflect-cli-tools-guide.md` | True | yes | yes |
| 21 | update | `docs/guides/cli-portify-and-pipeline-runner-guide.md` | True | yes | yes |
| 22 | update | `docs/guides/roadmap-cli-tools-release-guide.md` | True | yes | yes |
| 23 | update | `docs/guides/prd-skill-release-guide.md` | True | yes | yes |
| 24 | update | `docs/guides/tdd-skill-release-guide.md` | True | yes | yes |
| 25 | update | `docs/guides/suites-guide.md` | True | yes | yes |
| 26 | update | `src/superclaude/rules/core/changelog_maintenance.md` | True | yes | yes |
| 27 | update | `docs/reference/common-issues.md` | True | yes | yes |
| 28 | update | `docs/reference/troubleshooting.md` | True | yes | yes |
| 29 | update | `docs/reference/mcp-server-guide.md` | True | yes | yes |
| 30 | update | `docs/mcp/mcp-optional-design.md` | True | yes | yes |
| 31 | update | `docs/mcp/mcp-integration-policy.md` | True | yes | yes |
| 32 | update | `docs/reference/diagnostic-reference.md` | True | yes | yes |
| 33 | update | `docs/reference/deviation-report-format.md` | True | yes | yes |
| 33 | update | `docs/reference/pm-agent-autonomous-reflection.md` | True | yes | yes |
| 34 | update | `docs/developer-guide/technical-architecture.md` | True | yes | yes |
| 35 | update | `docs/developer-guide/contributing-code.md` | True | yes | yes |
| 36 | update | `docs/developer-guide/testing-debugging.md` | True | yes | yes |
| 37 | update | `docs/developer-guide/README.md` | True | yes | yes |
| 38 | update | `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` | True | yes | yes |
| 39 | update | `docs/dev/sync-discipline.md` | True | yes | yes |
| 39 | update | `docs/dev/lens-contribution-policy.md` | True | yes | yes |
| 40 | update | `docs/sprint-cli-deep-dive.md` | True | yes | yes |
| 41 | update | `docs/swarm/operator-runbook.md` | True | yes | yes |
| 41 | update | `docs/swarm/monitoring-patterns.md` | True | yes | yes |
| 41 | update | `docs/swarm/rollback-procedure.md` | True | yes | yes |
| 42 | update | `KNOWLEDGE.md` | True | yes | yes |
| 42 | update | `CONTRIBUTING.md` | True | yes | yes |
| 43 | create | `docs/developer-guide/codegraph-integration.md` | False | yes | yes |
| 44 | create | `docs/developer-guide/session-memory.md` | False | yes | yes |
| 45 | create | `docs/developer-guide/review-severity-rule.md` | False | yes | yes |
| 46 | create | `docs/developer-guide/release-procedure.md` | False | yes | yes |
| 47 | update | `docs/developer-guide/documentation-index.md` | True | yes | yes |
| 48 | create | `docs/testing/v5.0.0/user/D01-install-upgrade-doctor.md` | False | yes | yes |
| 49 | create | `docs/testing/v5.0.0/user/D02-mcp-servers.md` | False | yes | yes |
| 50 | create | `docs/testing/v5.0.0/user/D03-codegraph-graph-impact.md` | False | yes | yes |
| 51 | create | `docs/testing/v5.0.0/user/D04-session-memory.md` | False | yes | yes |
| 52 | create | `docs/testing/v5.0.0/user/D05-routing-core-files-issue-templates.md` | False | yes | yes |
| 53 | create | `docs/testing/v5.0.0/user/D06-plan-implement-review-cap.md` | False | yes | yes |
| 54 | create | `docs/testing/v5.0.0/user/D07-pr-submit.md` | False | yes | yes |
| 55 | create | `docs/testing/v5.0.0/user/D08-ccsession.md` | False | yes | yes |
| 56 | create | `docs/testing/v5.0.0/user/D09-hooks-freshness-pragmatic.md` | False | yes | yes |
| 57 | create | `docs/testing/v5.0.0/user/D10-sprint.md` | False | yes | yes |
| 58 | create | `docs/testing/v5.0.0/user/D11-roadmap-tasklist.md` | False | yes | yes |
| 59 | create | `docs/testing/v5.0.0/user/D12-reflect.md` | False | yes | yes |
| 60 | create | `docs/testing/v5.0.0/user/D13-prd-portify-cleanup-audit.md` | False | yes | yes |
| 61 | create | `docs/testing/v5.0.0/user/D14-swarm.md` | False | yes | yes |
| 62 | create | `docs/testing/v5.0.0/user/D15-eval-harness.md` | False | yes | yes |
| 63 | create | `docs/testing/v5.0.0/user/D16-init-lite-recommend-ic.md` | False | yes | yes |
| 64 | create | `docs/testing/v5.0.0/sysop/E01-ccsession-tier-policy.md` | False | yes | yes |
| 65 | create | `docs/testing/v5.0.0/sysop/E02-ccsession-model-data-publishing.md` | False | yes | yes |
| 66 | create | `docs/testing/v5.0.0/README.md` | False | yes | yes |

- Target-existence mismatches: none

### Inputs the plan relies on

| path | exists |
|---|---|
| `docs/testing/v5.0.0/c-e2e-transcript.txt` | True |
| `docs/testing/v5.0.0/c-e2e-run.sh` | True |
| `.dev/releases/current/v5.0.0/post-release/scan/A1-core-user-docs.md` | True |
| `.dev/releases/current/v5.0.0/post-release/scan/A2-feature-user-docs.md` | True |
| `.dev/releases/current/v5.0.0/post-release/scan/B-technical-docs.md` | True |
| `.dev/releases/current/v5.0.0/post-release/scan/C-install-surface.md` | True |
| `.dev/releases/current/v5.0.0/post-release/scan/DE1-cli-surface.md` | True |
| `.dev/releases/current/v5.0.0/post-release/scan/DE2-claude-surface.md` | True |
| `.dev/releases/current/v5.0.0/DECISIONS.md` | True |
| `.dev/releases/current/v5.0.0/RELEASE-READINESS.md` | True |
| `tests/skills/test_review_severity_rule.py` | True |
| `.markdownlint.json` | True |
| `docs/releases/v5.0.0.md` | True |
| `docs/developer-guide/git-standards-protocols.md` | True |
| `~/.claude/skills/sc-post-release-protocol/templates/user-test-guide.md` | True |
| `~/.claude/skills/sc-post-release-protocol/templates/sysop-test-guide.md` | True |

- Missing inputs: none

## Computed fields

- parsed_count: 0
- inferred_count: 17
- coverage_pct: null (parsed_count is 0)
- coverage_pct_union: 0.0 (0/17)
- unmapped_requirements_union: ['INF-001', 'INF-002', 'INF-003', 'INF-004', 'INF-005', 'INF-006', 'INF-007', 'INF-008', 'INF-009', 'INF-010', 'INF-011', 'INF-012', 'INF-013', 'INF-014', 'INF-015', 'INF-016', 'INF-017']
- S_scope: 66
- S_domains: 3 (code, docs, tests; rule: `src/`+`plugins/` = code, `docs/testing/` = tests, other `.md` = docs; no infra or config targets)
- S_dev_density: 1.0 (unmapped_union 17 / total_union 17; missing_implementations_count = 0, docs-only plan)
- coverage_degraded: parsed-sparse

## Semantic notes (do not change the containment result)

1. Why containment is 0/17: every INF row is an aggregate requirement (one in-scope item spans 2-22 tasks) or a plan-wide constraint. A single task's text cannot hold 60% of such a quote's words by construction; the highest ratio is INF-008 at 0.5455 (Task 66). The rule as specified matched nothing, so `coverage_pct_union = 0.0` and `S_dev_density = 1.0` are mechanical artifacts of the rule, not evidence of missing work.
2. Item-level completeness is 100%: A-W1..A-W22, B-W1..B-W22, C-W1..C-W3, D01-D16, E01, E02 and `docs/testing/v5.0.0/README.md` are each named by exactly one task (53 of 53, no duplicates). Every update target exists and every create target is still absent.
3. Constraint gaps (from the carriage column): INF-016 is only partly carried. The plan has per-file markdownlint, but it lacks the spec's pytest smoke (`-k "doc or primitive or how_we_work or severity"`) and the final full `make test`; no task runs `make test` (tasklist grep: 0 hits). INF-011 (do not write `post-release-report.md` / `post-release-manifest.json`) is met only by omission.
4. Sub-item link targets that the plan item lists but the task text does not name (implied by "per item X", so they could be missed): A-W22 item 9 says to link `codegraph.md` from `docs/user-guide/commands.md` and `mcp-servers.md`. Task 17 names `README.md` and `mcp-installation.md` instead (CONSOLIDATED-PLAN.md:392, tasklist:175). B-W22 item 6 also asks for a pointer in `docs/developer-guide/git-standards-protocols.md` (CONSOLIDATED-PLAN.md:544), and no task names that file. B-W12 item 6 says "Link the four new notes" (CONSOLIDATED-PLAN.md:481), but Task 37 does not name them and has no dependency on Tasks 43-46.
