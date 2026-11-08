# Phase 2 research inventory

Files found: 3 of 3 expected. Files with Status: Complete: 3. Missing: none. Counts below come from `wc -l` and `grep` over the actual files on 2026-11-07.

| File | Investigation type | Status | Line count | Doc-claim tags present | Key Takeaways (one line) |
|---|---|---|---|---|---|
| research/01-claim-flow-and-session-launch.md | Code Tracer | Complete | 288 | yes (59 tag hits) | `/sc:issue --claim <N>` never prompts, assigns `@me`, stops at `next-steps.md`; launch route is `orca agent launch --agent claude --worktree path:<abs> --surface terminal --prompt "/sc:issue --claim <int>"`; no mutual exclusion on a claim race; `/sc:issue` is never-as-worker so a top-level session is required. |
| research/02-github-surface-and-cli-patterns.md | Integration Mapper | Complete | 211 | yes (26 tag hits) | Only push, pull_request, workflow_dispatch triggers exist; no Python `gh` wrapper exists (ci.py claim CODE-CONTRADICTED), the repo mocks `gh` with PATH-stub executables; new CLI group registers after `main.py:561`; fork has only 9 default labels. |
| research/03-governance-and-security-surface.md | Architecture Analyst | Complete | 231 | yes (33 tag hits) | Only `launch-job-identity.sh` exists (never denies); `--claim --pipeline` and `launch-level-guard.sh` are design only; integer-only protects the launch prompt but the claim still reads issue title/body/comments; no approver allow-list exists; at-most-once needs poller-side dedupe. |

## All items from the Gaps and Questions sections

### 01 (8 numbered gaps plus tagged claims)
1. `/sc:issue --claim <N>` as an initial prompt of `orca agent launch --prompt`: slash command executed? [UNVERIFIED]
2. Argv versus typed paste delivery of `--prompt`; real JSON error body of `agent launch`. [UNVERIFIED]
3. One person with several workspaces polling with one login (same-login race).
4. Coder workspace has Orca runtime reachable, `ccsession-orca`, tier picker IDs, permission mode? [UNVERIFIED]
5. Can the workspace `gh` token read the org Project (Project and Backlog filters)? [UNVERIFIED]
6. Whether tests pin the claim-stops-after-`next-steps.md` text.
7. Is an existing `<D>` tolerated on re-run?
8. Does `--claim` work under `claude --print`? [UNVERIFIED]
Tagged: CODE-CONTRADICTED the issue's expectation that claim orchestrates the pipeline; UNVERIFIED never-as-worker reading as owner intent; UNVERIFIED sessions stay open after claim; CODE-VERIFIED `--claim --pipeline` is design only.

### 02 (10 gaps)
1. `orca agent launch` flags and prompt behavior not read from the live CLI here. [UNVERIFIED]
2. GitHub-side selection fields: `gh issue list --json` fields, Project v2 field and Status access. [UNVERIFIED]
3. Whether `labeled` issue events are a trustworthy "who approved" signal. [UNVERIFIED]
4. ci.py is not a mockable `gh` subprocess wrapper. [CODE-CONTRADICTED]
5. `tests/pr_submit/conftest.py:3-4` describes `mock_gh` as a gh-wrapper seam. [CODE-CONTRADICTED]
6. `tests/cli/test_cli_registration.py:28-30` frozen-snapshot claim. [CODE-CONTRADICTED]
7. The fork has none of the `type:*` / `complexity:*` labels that `/sc:issue --create` expects.
8. Trigger and approval label names and the Project/Status mapping are not defined anywhere in the repo.
9. Whether a poller `gh` login can read the org Project at all. [UNVERIFIED]
10. Race behavior with several workspaces polling (same developer, several workspaces).

### 03 (14 gaps)
1. `launch-level-guard.sh` described in present tense but absent. [CODE-CONTRADICTED]
2. `/sc:issue --claim --pipeline <level>` does not exist. [CODE-CONTRADICTED]
3. Packaged hooks.json registers `launch-job-identity.sh` but this host does not. [CODE-CONTRADICTED on this host]
4. Does `orca agent launch --prompt` submit the prompt or prefill it? [UNVERIFIED]
5. Orca Claude command and permission mode on watcher hosts. [UNVERIFIED per host]
6. Policy for the claim's own reads of title, body and comments. [OPEN DECISION]
7. Can a post-approval edit of an issue body be detected? [UNVERIFIED]
8. Project permissions and `project_v2_item_status_changed` payload; `read:project` token scope missing. [UNVERIFIED]
9. Whether org owners outside the collaborator list can apply labels. [UNVERIFIED]
10. Where the approver allow-list lives. [OPEN DECISION]
11. At-most-once: local dedupe state versus "assigned to my login and no claim marker comment of mine". [OPEN DECISION]
12. Whether an `orca agent launch --worktree issue:<number>` selector triggers forbidden Orca-to-GitHub linking. [UNVERIFIED]
13. Bodies of `freshness-pre-edit.sh`, `sc-recommend-phase0.sh`, `issue-worker-t2.md`, `issue-worker-t1.md` not read. [NOT READ]
14. Any Coder-side tie of a workspace to a GitHub account (Coder#477). [UNVERIFIED outside the repo]
