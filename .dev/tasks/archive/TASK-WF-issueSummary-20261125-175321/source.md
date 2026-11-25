# Summary: #834 /sc:issue --create asks only about contradictions

- Issue: https://github.com/IronbellyOrg/IronClaude/issues/834
- Type: feature
- Complexity: medium (rubric: `refs/claim.md`)
- Effort estimate: 12 hours
- spec-route: design — Medium scope with explicit acceptance criteria for question counts, conflict classification, retained additions and regression checks.

## What the issue asks for

Change issue creation so useful additions, including clearly stated assumptions, never require an approval question. Ask exactly one combined question only for a supported contradiction of the user's own description, instruction or supplied flag, resolve it before posting, and retain all unrelated additions in the body, notes and final output. The four requested conflict categories are reversed choice, dropped requirement, changed flag and a user-stated fact contradicted by verified code; `None` is not an item, and worker disagreement is not a contradiction when the filed issue honors the user's flag. The live Owner note says recent unnecessary pauses are recurring defects, but their frequency and the individual Orca-sleep incident were not independently reproduced.

Use `origin/integration`, not the issue's `origin/master`, as the implementation base. The accuracy verdict is `out_of_date` because the base and some context need correction, not because the fix landed: D14 still asks for additions alone at `src/superclaude/skills/sc-issue-protocol/refs/create.md:84`. Preserve claim assignment, ClickUp, Orca, watcher and launch safeguards, post-create flag pushback, required planning sections, and the launched `worktree` agent's approval boundary. Type remains feature, matching the filed request and scout; this does not dismiss the owner's description of the unwanted pauses as defects.

Estimated work: 2 hours for classification/decision rules, 2 hours for instruction/template/docs alignment, 3 hours for static regression and mutation cases, 3 hours for controlled create-run verification across depths, and 2 hours for full-suite/lint/sync gates and review follow-up. This is one issue-creation subsystem, over 4 and at most 16 hours, with no requested security or migration change, so the rubric gives medium. The estimate assumes an available isolated runner that intercepts GitHub writes; its availability and the runtime of the full suite are not known yet.

## Relevant files and systems (cheatsheet)

| Path or system | Why it matters |
|---|---|
| `src/superclaude/skills/sc-issue-protocol/refs/create.md:57,63-69,82-84,97` | Main change: keep assumption recording, define contradiction-only prompting and resolution, and disclose retained additions in final output. |
| `src/superclaude/skills/sc-issue-protocol/SKILL.md:4,76,102-103` | Retain `AskUserQuestion` for real conflicts; align the only-prompt rule, drafting step and posting output. |
| `src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md:3-15` | Two lists already exist. Define their different consequences, four conflict categories, supporting user quotation/evidence and `None` handling. |
| `src/superclaude/agents/issue-worker-t1.md:24`, `issue-worker-t2.md:24`, `issue-worker-t3.md:24` | Drafting workers already record additions and contradictions at all depths. Change guidance only if needed for consistent classification; preserve their shared planning rule. |
| `src/superclaude/commands/issue.md:19,82-85,108-114` | Align the direct-posting promise and actual output inventory; keep protocol activation. The issue's 78-80 output citation needs correction to 82-85. |
| `docs/designs/sc-issue-command.md:223-225,460`; `docs/user-guide/commands.md:357` | Two design statements still encode the broad trigger; explain the narrow exception beside the user-facing direct-posting promise. |
| `tests/skills/test_issue_protocol.py:40,137-144,726-819,1162-1180` | Preserve allowed tools, markers, headings and required-plan checks; retain the newer stage-claim recommendation test. Add the four proposed create-decision tests, currently absent. |
| `tests/commands/test_issue_command.py:67-100,258-270`; `tests/cli/test_issue_body_templates.py:27-97` | Extend command/protocol agreement without replacing metadata, option, activation, installed Handoff/Backlog or rule-10 guards. |
| `tests/skills/test_issue_worker_agents.py:34-39,535-559`; `tests/skills/test_worker_contract.py:3066-3087` | Preserve the exact shared planning sentence/carve-out and unrelated field-write/lookup assertions. |
| `src/superclaude/skills/sc-issue-protocol/refs/claim.md:79-82,86-96`; `refs/chains.md:29,40`; `templates/launch-prompt.md:25` | Preservation only: ordinary claims retain recommendation fallback; staged claims skip recommendation after #833. Only the launched `worktree` level waits at the plan boundary. |
| `Makefile:13-15,48-50,109-136,166-250`; `src/superclaude/cli/install_skills.py:75-76,100-110`; `install_skill.py:26-52` | Canonical source is `src/`; project mirrors come from `make sync-dev`, not hand edits. The home install needs its supported refresh mechanism separately. |
| Controlled create runs and regression gates | Verify empty/additions-only notes ask zero questions; each supported nonempty contradiction list asks exactly once, applies the answer, then posts once. Exercise all depths, all categories, mixed/multiple conflicts and preserved user flags. Static assertions alone do not prove agent behavior. |

## Analysis

- [Current-source analysis](analysis/analyze-sc-issue-protocol.md): standard `/sc:analyze` pass, without `--depth`, against integration at `a6fec24480e8cc65abbb16b194625e2ea52238c7`; source evidence, prioritized changes, preservation requirements and verification limits.
- [Accuracy check](accuracy-check.md): claim-by-claim corrections and all eight scout PR relevance decisions. Three PRs postdate creation; #833 predates it and changes claim-stage behavior, not D14; #846 does not fix this request.
- Proposed gates, not results: `uv run pytest tests/skills/test_issue_protocol.py tests/skills/test_issue_worker_agents.py tests/skills/test_worker_contract.py tests/commands/test_issue_command.py tests/cli/test_issue_body_templates.py -v`, then `make test`, `make lint`, `make sync-dev` and `make verify-sync`. No tests, source edits, mirror refreshes or live create experiments were performed by this read-only check.
