# Research Notes: Existing solutions and design inputs for a GitHub issue watcher and routing service (issue #331)

**Date:** 2026-11-07
**Scenario:** A (explicit request: goal, why, where and output type all given)
**Depth Tier:** Standard (cross-cutting but the repo-side surface is small: about 15 relevant files, roughly 1100 lines; the bulk of the open questions are external). QA intensity: standard (tier default).
**Status:** Complete
**Output type:** options analysis and recommendation with a concrete implementation plan that fits this repo (commands, skills, CLI code, docs; no live deployment).
**Calling context:** feeds `/sc:brainstorm` enrichment for `.dev/brainstorms/20261107-064825-github-issue-watcher/`. The final report must also be copied/condensed to `.dev/brainstorms/20261107-064825-github-issue-watcher/enrichment/research-deep.md`.

---

## EXISTING_FILES

Scope discovery was done in the claim step (see `.dev/issues/331/analysis/analyze-sc-issue-protocol.md`, `.dev/issues/331/accuracy-check.md`) and in `.dev/brainstorms/20261107-064825-github-issue-watcher/enrichment/codebase-context.md`. All paths below were verified to exist on 2026-11-07 against origin/master e8db2fe6.

| Path | Purpose | Approx lines |
|---|---|---|
| `src/superclaude/commands/issue.md` | `/sc:issue` command: flags, STOP rules, boundaries; claim stops after `next-steps.md` | ~90 |
| `src/superclaude/skills/sc-issue-protocol/SKILL.md` | Claim and create protocol; repo/GitHub call rules (`--repo <R>`, origin only) | ~170 |
| `src/superclaude/skills/sc-issue-protocol/refs/claim.md` | Claim waves 0-6: assign `@me`, refuse if assigned to someone else, marked comments edited on re-run | 90 |
| `src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py` | Resolves `owner/repo` from `origin` only; refuses foreign issue URLs | 195 |
| `src/superclaude/skills/sc-issue-protocol/refs/labels.md` | Fixed label set; `/sc:issue` never creates labels | small |
| `src/superclaude/core/WORKER-CONTRACT.md` | Never-as-worker list includes `/sc:issue` | ~100 |
| `src/superclaude/skills/ccsession-tag/README.md` | `orca agent launch` / `--surface terminal` for a new Claude session; launch prompt names the session | ~300 |
| `src/superclaude/core/CLAUDE.md` | "Orca session launches" rule (Claude CLI, never New Terminal; `ccsession-orca`) | n/a |
| `docs/designs/sc-issue-launch-level-hook.md` | Proposed `--claim --pipeline <level>`; not implemented; B-CTX gate | 565 |
| `src/superclaude/hooks/scripts/launch-job-identity.sh` | PR #414 job-identity groundwork | small |
| `.github/workflows/{test,boundary-guard,contract3-generator-constraint-lint}.yml`, `.github/workflows/README.md` | Only push / pull_request / workflow_dispatch triggers; no schedule | small |
| `.github/ISSUE_TEMPLATE/*.yml` | feature adds `enhancement`; bug adds `bug` | small |
| `src/superclaude/pr_submit/ci.py` | CORRECTED 2026-11-07: NOT a `gh` wrapper; it imports only `re`, `.classifier`, `.models` (no `subprocess`) and no Python file under `src/superclaude` builds a `["gh", ...]` call; agent 02 must report where `gh` is really invoked (skill/command protocols via Bash) | 163 |
| `src/superclaude/cli/main.py` | Click group registration (`main.add_command(<group>, name=...)`) | ~560 |
| `tests/` (per-package dirs, e.g. `tests/pr_submit/`, `tests/skills/`) | Test layout | n/a |
| `docs/designs/sc-issue-command.md` | House format for design docs | ~600 |

## PATTERNS_AND_CONVENTIONS

- GitHub access is via the `gh` CLI, issued by skill/command protocols through Bash (CORRECTED: `src/superclaude/pr_submit/ci.py` does not use `subprocess`; the nearest Python subprocess pattern is `src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py`, git calls); every call in this repo names `--repo IronbellyOrg/IronClaude`; `gh api` paths spell `repos/<R>/...`.
- Repo resolution is always from `origin` (`origin_repo.py`); foreign repos are refused (`E-FOREIGN-REPO`).
- CLI features are Click groups in `src/superclaude/cli/<name>/`, registered in `cli/main.py`; tests under `tests/<name>/`.
- Source of truth is `src/superclaude/`; `.claude/` is a gitignored mirror (`make sync-dev`).
- Design docs live under `docs/designs/` in the house format of `sc-issue-command.md`.
- Documentation-vs-code rule: every doc-sourced architecture claim must be verified against code (CODE-VERIFIED / CODE-CONTRADICTED / UNVERIFIED).

## SOLUTION_RESEARCH

External solution space to research (web agents), each option to be assessed for fit with the constraints "no inbound endpoint if avoidable, no live deployment from this repo, claim assigns to the `gh` login that runs it":

1. **A. Workspace-side poller (pull):** a scheduled job in each Coder workspace polls GitHub with the workspace's own `gh` login, filters, then launches a local session.
2. **B. GitHub Action plus workspace listener (push):** `schedule:` / `issues:` / `projects_v2_item:` workflow selects issues and calls an authenticated endpoint on the owner's workspace.
3. **C. Central microservice plus listener (push).**
4. Hybrids: Action only writes a "ready" label or Project field change; workspaces poll for that (pull) so the Action never needs a workspace address.
5. External facts to establish with sources: GitHub Actions `schedule` minimum interval (5 minutes) and delay behavior; `issues` / `projects_v2_item` webhook and workflow events (including that `projects_v2_item` is organization-level webhook only and not a workflow trigger, if true); Projects v2 GraphQL read access and token types (classic PAT `project`/`read:project`, fine-grained PAT org permissions, GitHub App with Projects permission; whether `GITHUB_TOKEN` can read an org Project); `gh project item-list` CLI; REST/GraphQL rate limits and conditional requests (ETag); Coder: agent API / `coder ssh` / `coder exec` / workspace autostop and external auth; Claude Code headless (`claude -p`) and the Claude Code GitHub Action; comparable issue-to-agent dispatchers (for example Copilot coding agent assigned from an issue, Codex/Claude GitHub apps, Sweep-style bots); prompt-injection guidance for agents that read issue text; at-most-once delivery patterns (idempotency key, claim marker comment, label flip, lease).

## RECOMMENDED_OUTPUTS

| File | Purpose |
|---|---|
| `research/01-claim-flow-and-session-launch.md` | Code tracer: what `/sc:issue --claim` does and the exact local entry points for starting a top-level session |
| `research/02-github-surface-and-cli-patterns.md` | Integration mapper: workflows, labels, templates, `gh` wrappers, CLI registration, test layout (what a repo-side poller would plug into) |
| `research/03-governance-and-security-surface.md` | Architecture analyst: launch-level hook design, job-identity hook, never-as-worker list, trust boundaries for untrusted issue text |
| `research/web-01-github-events-projects-and-limits.md` | Web: Actions schedule/event limits, Projects v2 access and token scopes, polling efficiency and rate limits |
| `research/web-02-coder-claude-dispatch-and-security.md` | Web: Coder workspace reachability and APIs, Claude Code headless / GitHub Action, comparable dispatchers, prompt-injection and at-most-once patterns |
| `synthesis/synth-01-problem-current-state.md` | Report sections 1-2 |
| `synthesis/synth-02-target-gaps-external.md` | Report sections 3-5 |
| `synthesis/synth-03-options-recommendation.md` | Report sections 6-7 |
| `synthesis/synth-04-plan-questions-evidence.md` | Report sections 8-10 |
| `RESEARCH-REPORT-issue-watcher.md` | Final report |
| `.dev/brainstorms/20261107-064825-github-issue-watcher/enrichment/research-deep.md` | Condensed copy with pointer to the full report (brainstorm enrichment artifact) |

## SUGGESTED_PHASES

Codebase research agents (Phase 2, spawn in parallel):

| # | Type | Topic | Files | Output |
|---|---|---|---|---|
| 01 | Code Tracer | Claim flow and the ways a top-level Claude session can be started with a prompt | `src/superclaude/commands/issue.md`, `src/superclaude/skills/sc-issue-protocol/{SKILL.md,refs/claim.md,refs/labels.md,scripts/origin_repo.py,scripts/clickup_claim.py}`, `src/superclaude/core/WORKER-CONTRACT.md`, `src/superclaude/skills/ccsession-tag/README.md`, `src/superclaude/core/CLAUDE.md` | `research/01-claim-flow-and-session-launch.md` |
| 02 | Integration Mapper | GitHub-facing surface and house patterns for a repo-side deliverable | `.github/workflows/*`, `.github/ISSUE_TEMPLATE/*`, `src/superclaude/pr_submit/ci.py`, `src/superclaude/cli/main.py`, an example small CLI package, `tests/pr_submit/`, `docs/designs/sc-issue-command.md`, `Makefile` targets for lint/format/sync | `research/02-github-surface-and-cli-patterns.md` |
| 03 | Architecture Analyst | Governance and security surface for a watcher-started session | `docs/designs/sc-issue-launch-level-hook.md`, `src/superclaude/hooks/scripts/launch-job-identity.sh`, hook registrations in `.claude/settings.json`, `src/superclaude/core/WORKER-CONTRACT.md` | `research/03-governance-and-security-surface.md` |

Web research agents (Phase 4, spawn in parallel):

| # | Topic | Output |
|---|---|---|
| web-01 | GitHub Actions schedule/event limits and delays; `issues`, `projects_v2_item` events; Projects v2 GraphQL/`gh project` access and token types; rate limits and conditional polling | `research/web-01-github-events-projects-and-limits.md` |
| web-02 | Coder workspace reachability, API/CLI (`coder ssh`, `coder exec`, agent API, autostop), Claude Code headless and the Claude Code GitHub Action, comparable issue-to-agent dispatchers, prompt-injection and at-most-once patterns | `research/web-02-coder-claude-dispatch-and-security.md` |

Synthesis mapping (Standard, 4 files): see RECOMMENDED_OUTPUTS.

## TEMPLATE_NOTES

Template 02 (complex task): discovery, parallel agents, QA gates, assembly. QA_INTENSITY: standard.

## AMBIGUITIES_FOR_USER

None that block research. Owner-level decisions (architecture choice A/B/C, claim-only versus full pipeline, security model) were sent to the coordinator and are treated as open options in the report; the report must recommend one but not assume the answer. The research must not deploy or run anything live.

---

## ADDENDUM 2026-11-07T07:03Z: coordinator guidance and sibling issue (binding on all agents)

1. **Do NOT finalize or favor architecture A.** The issue text (#331) and the sibling issue IronbellyOrg/Coder#477 describe a PUSH design (watcher -> API/MCP layer -> Coder-side listener). The owner is being asked. Options A (workspace-side poller), B (GitHub Action + Coder-side listener) and C (central microservice + listener) must all stay open; the report must SCORE each against the issue's stated requirements and must not present A as decided. The Recommendation section may state which option scores best on stated criteria but must mark it "pending owner decision".
2. **Sibling dependency: IronbellyOrg/Coder#477** "[FEATURE] Workspace listener, monitor registration and secure prompt routing for every Coder workspace" (OPEN, read 2026-11-07 via `gh issue view 477 --repo IronbellyOrg/Coder`). It asks for: a listener running in every Coder workspace; each workspace and listener registered with the "monitor"; authorized monitor requests reach the intended workspace and are handed to its project's orchestrator to start a new session; workspace address/port securely associated with the right GitHub account; authentication and authorization on senders, unauthorized requests rejected, no unauthenticated port exposed; protected transport and an audit trail of routing and access decisions. Candidate integration points named there (Coder repo, not this repo): `templates/VSCode-AIDev02/{main.tf,Dockerfile.coder,startup.tf,scripts/startup.sh,catalogue/orca/module.tf,catalogue/orca-pair.sh,orca/runtime.mjs}`, `.github/workflows/orca-upstream-monitor.yml` (distinct upstream-version monitor). Prior art there: closed Automatic Orca Pairing issue #195. Interface, registration mechanism, credentials, network topology and audit implementation are "not known yet". **Boundary:** the listener, registration and transport live in the Coder repo (#477), not in IronClaude; this repo's #331 deliverable is the watcher/selection/dispatch side and the contract it needs from the listener.
3. **Accepted by the owner's coordinator:** scope is claim-only (the watcher's job ends at starting `/sc:issue --claim <N>`; the pipeline after the claim stays manual); only a validated integer issue number may ever reach a session prompt, never issue title/body text.
4. Research must therefore also cover, for B and C: how a push listener authenticates the sender (mTLS, signed requests/HMAC, GitHub OIDC tokens from Actions, Coder session tokens), how Coder exposes workspace apps/ports safely (authenticated app proxy, `coder_app` sharing levels, agent API), and what a minimal contract between watcher and listener looks like (request schema, idempotency key, response codes).

---

## ADDENDUM 2 2026-11-07T07:12Z: OWNER DECISION (SUPERSEDES the "keep A, B and C open" rule in the addendum above)

The owner decided (relayed by the coordinator, message sent 2026-11-07T07:04:56Z): **Q1 = option A, the workspace-side poller** (each workspace polls GitHub every 5 minutes with its own `gh` login and starts the claim via `orca agent launch`; no listener, no inbound port, no address registry). **Q2 = claim-only. Q3 = only an integer issue number reaches the session prompt.** The repo-side deliverable is: design doc + a tested poller script/CLI (mock `gh` and mock `orca agent launch`, nothing run live) + trigger/approval label setup instructions; B/C and any live deployment are recorded as follow-up. The spec must record that **IronbellyOrg/Coder#477 (workspace listener and registration) was filed assuming a push design, and A makes #477 unnecessary unless B/C is revisited.**

Effect on the research: the report still evaluates B and C (and hybrids) fairly as the documented alternatives and the revisit conditions, but the Recommendation is **option A, decided by the owner** (not "pending owner decision"), and the implementation plan targets A. The earlier "do not favor A" instruction no longer applies.
