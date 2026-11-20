53a5007d42628bd0ce82b1bd6a387ebc3cc2a16f
# Review of Task 15, attempt 1

Earlier blocking findings: none (first review).

Checked live: the diff, the files on disk, the DF-14 rationale, and `uv run pytest tests/issue_pipeline tests/issue_watch -q` (3160 passed in 23.69 s).

DF-14 rationale (.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/research/06-gap-fill-decisions.md:37 and :87): it only requires `$after: String` to be nullable, `first: 100`, and no `mutation`. It does not forbid non-null variables, so the task's stop condition does not apply. The repository literal in the draft is what the task replaces.

## Per-AC marks

- T15.AC1 met. T15.AC1@tests/issue_watch/test_github.py:262 (every argv for `Other-Org/Other.Repo`, `argv_events` and `argv_comments` included, carries the repo and not the default), :273 (default stays the fork), :282 (refuses `a/b/c`, empty, space, leading dash, and more, for all seven argv builders), :298 (public reads raise before any call). Source: src/superclaude/cli/issue_watch/github.py:206 (`valid_repo`), :253, :293, :298, :303, :345.
- T15.AC2 met. T15.AC2@tests/issue_watch/test_security_invariants.py:948 (regex `\$(\w+): String!` gives owner and name, `count("String!") == 2`, no literal repository, no mutation or subscription, `$after: String)` stays nullable). The no-mutation checks on the constants still pass (test_security_invariants.py:936-941). Queries at github.py:85, :99, :123 carry `$owner: String!, $name: String!` and `$after: String`.
- T15.AC3 met. T15.AC3@tests/issue_pipeline/test_stage_status.py:646 (no `--repo` gives exit 2 and the output names `--repo`), :655 (a non-`owner/name` value exits 1 with `refused:bad-repo` and no call was made), :664 (reread, events, comments, edits and approval-events argv all carry `Other/Repo`, none names `IronClaude` or `IronbellyOrg`), :697 (the `Router` at :631 serves a different world per repo; the IronClaude `labeled` event never approves the other repo, and the same call for the default repo does see it). `read_stage_evidence` coverage: tests/issue_pipeline/test_reads.py:331 (required `repo`), :343 (ValueError before any call), :352 (all four reads carry the repo). Source: src/superclaude/cli/issue_pipeline/cli.py:380 (required option), :426-428 (strict check before any call), :321 and :324 (repo passed to `gh.reread` and `read_stage_evidence`); src/superclaude/cli/issue_pipeline/reads.py:69, :115, :143 (no defaults).
- T15.AC4 met. T15.AC4@`uv run pytest tests/issue_pipeline tests/issue_watch -q`: 3160 passed.

## Findings

F1.1 ac=scope at=tests/hooks/test_launch_level_guard_worker.py:401 anchor=tests/hooks/test_launch_level_guard_worker.py:401 chk=n,n,n,n family=stale-example fix=optional: add `--repo Owner/Name` to the example command so it matches the verb's required option; the guard test still passes as written: Non-blocking. The test feeds `superclaude issue-pipeline stage-status 12 --json` (no `--repo`) to the guard only to show the guard does not classify it; the command would now be a usage error if run.

No blocking findings.
