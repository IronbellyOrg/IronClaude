# Emerging consensus after Round 2 (13/13 points agreed), refactor cycle 1

Verdict: not_ready. Meaning: cycle-0 findings are fixed apart from the items below; scope and Fix 1-4 coverage remain sound; two medium acceptance defects and one medium structural miss remain.

Must-fix (medium):
- R1-1 Task 1/9: Task 1 hashes every baseline path outside the allowed folders, including files already under .dev/reflect/, .dev/troubleshoot/, .dev/workflow/ (48 .dev/reflect/ entries exist in the baseline today); Task 9's cmp (tasklist:183) has no tooling exemption, so a rewritten pre-existing tooling file fails a correct run. Fix: Task 1 skips the three tooling roots when writing t1-hashes-before.txt and lists them separately.
- R1-2 Task 6: nothing checks that the `gh pr list` call keeps `--head sync/framework --base master --repo "$GITHUB_REPOSITORY"`; the stub prints the count regardless (tasklist:117, :128-133). Fix: a static check on the list line, and assert the stub log of runs (a) and (b) shows `--head sync/framework`.
- R2-1 Depends on (source:82): Tasks 3-6 are not ancestors of Tasks 8-9. Fix: renumber 1 baseline, 2 GitHub settings/docs, 3 three-dot proof, 4 boundary-guard edit, 5 sync edit, 6 Codecov research, 7 Codecov edit, 8 workflows README, 9 scripts README + scope; chain each task on the one before it. (Runtime order is already safe: /sc:implement runs sequentially in source order, SKILL.md:97.)

Low:
- Renames under -z: git emits `XY new\0old\0`; record both paths; old path hashed as MISSING; a new path outside the allow-list fails.
- Task 7 must not change ./artifacts/t2-codecov-v4.md: hash it at the end of Task 2's successor and cmp after Task 7.
- Job-name check: forbid the old phrase `human review required`, not the bare substring `required`.
- Decision line: fixed format, e.g. `Decision: file-input=files; token=secrets.CODECOV_TOKEN`, with regex `^Decision: file-input=(file|files);`.
- Task 6: "zero `<` characters in the edited workflow"; PR body as a quoted string, never a heredoc.
- Task 5 instruction for the `::warning` line should say the line must contain the word `advisory` (the check already requires it).
- Optional hardening: Task 5 whole-document comparison of boundary-guard.yml (runs-on, env, checkout, fetch-depth: 0); Task 9 accept exactly the four named workflow files (contract3 residual).

Rejected: R1-8 (Task 9 states the 3,000 conclusion as source:80 instructs), R1-9 (scripts/README.md line 30 not a publish-workflow leftover per source:81), R2-8 (reflect matrix corrections only, no tasklist edit).
Shared assumptions: A-001 holds (SKILL.md:97); A-002 holds (bare git only); A-003 qualified (no high, but the medium list is mandatory).
