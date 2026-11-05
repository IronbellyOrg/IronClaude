# Coordinator constraints for this /sc:implement run

Source: Orca coordinator brief, task task_81fa7346d9b9, dispatch ctx_5d16ae12c2f5, received 2026-11-04 13:25 UTC.
These constraints are binding and override the plan text where they conflict. They are recorded here because the ledger (`../progress.md`) accepts only its fixed record grammar. Each task brief handed to a reviewer carries the constraints that apply to that task, labelled "Coordinator constraint".

## C1 (round-2 finding F-14), applies to Task 3

The three `issue-worker-t*` agent files must NOT carry `permissionMode: plan` or any read-only permission mode. The design requires them to write files under `.dev/issues/`. Do not copy that line from `evidence-validator.md`. Task 3's test must assert it is absent.

## C2 (round-2 finding F-01), applies to Task 1, Task 6 and Task 17

Never run a live `/sc:issue --claim` or `--create` against any real issue or repository: not `octocat/Hello-World`, not `IronbellyOrg/IronClaude` issue 302, not anything else. For Task 17 item 4, implement the deterministic URL-versus-origin check the design requires (`E-FOREIGN-REPO`, source.md section 20) with unit tests as F-01 recommends (same repo, foreign owner, same owner with a different repo, a repo-name prefix, a `/pull/<N>` URL, a trailing slash or fragment, digits in the owner or repo never becoming N), and verify item 4 through those tests. Any live run is recorded as pending in the post-restart runbook (C3), never executed.

How applied: the check lives in `scripts/origin_repo.py` (Task 1, the script source.md section 15 makes Wave 0's tested code) and Wave 0 of `SKILL.md` calls it (Task 6).

## C3 (round-2 findings F-02, F-06, F-11, F-12), applies to Task 15, Task 16 and Task 17

`/sc:implement` cannot ask the user mid-run. Record the worker smoke spawns (Task 15), the ClickUp smoke claim (Task 16; `CLICKUP_*` variables are not set in this environment) and every live acceptance item as pending with the reason. End Task 17's artifact with a short post-restart runbook listing them in order, with exact commands and the variables to export.

## C4, applies to every task

Apply any other round-2 minor finding only when it is a correctness fix inside the task being implemented. Log every other minor finding as not applied. No unrequested additions.

The per-finding disposition is recorded in `./round2-minor-findings.md`.
