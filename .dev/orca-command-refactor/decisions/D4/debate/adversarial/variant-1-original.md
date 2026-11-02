# D4 option (a): the brief may authorize a named outward action when the user's own instruction names it

Position: a worker may push, open a PR, post to GitHub, install, provision or run a paid external job only when the user's own instruction to the coordinator names that action for that Task; the coordinator quotes that instruction in the brief and passes the command's explicit flag. Without it every outward default is off (WC-9, `SPEC:73`; `SPEC:346`). On worker commits: a local commit is authorized the same way (the issue #326 evaluation's F0/F1 wording).

Citation key: `SPEC:N` = spec line; `PRL:N` = `src/superclaude/skills/sc-post-release-protocol/SKILL.md:N`; `HWW:N` = `src/superclaude/core/HOW-WE-WORK.md:N`; `EVAL:N` = `.dev/orca-command-refactor/review/issue-326-evaluation.md:N`.

## Strongest case for it
- **It matches existing repo wording.** post-release confirms outward steps "unless the user pre-authorized them this session" (`PRL:351`) and will not commit, push, open a PR, provision a VM or run real-target installs "without confirmation (or standing authorization)" (`PRL:340`). Pre-authorization is already a recognised form.
- **Workers can deliver whole results.** post-release's value is the new-user install run "to green on the classified target" with a transcript (`PRL:333`); under (b) or (c) that step always moves back to the coordinator.
- **Issue #326 wants it.** The owner asks for commits "after each task" and for status updates through GitHub (`EVAL:19`, `EVAL:18`). The spec's ban on worker commits rests on this planning run's own README rule, not repo policy (`EVAL:50`; `.dev/orca-command-refactor/README.md:31`); repo policy is "commit only when asked" (`CLAUDE.md:37`).
- Flags stay explicit and per command (auggie-review `--post-pr`, `SPEC:123`), so nothing turns on by default.

## Safety
- Authorization crosses sessions through an agent. The user's words reach the worker only as the coordinator's quotation in the brief; the worker cannot check them. The repo's own outward rules say "this session" (`PRL:351`) and "explicit, separate, deliberate user authorization in the same session" (`CLAUDE.md:68`); a worker is a different session. This is the same provenance gap the spec refuses for Rulings under D2 (`SPEC:334`).
- Pushes and posts done by an unwatched worker are hard to reverse: a published comment or PR is visible at once.

## Reliability
- Testable: AC-4.2 already checks that nothing outward happens without flags (`SPEC:275`); with flags, each authorized action needs its own live check on a scratch fork PR.

## How a person works day to day
- The person says once, up front, "workers may push and open the PR for task X"; workers then finish end to end. The person must phrase authorizations per action and per Task, and trust the coordinator's quoting.

## Implementation cost
- Spec: WC-9 sentence plus the section 4 `/sc:git` row change (`EVAL:50-51`). Commands: each outward flag must be honoured under `--unattended` and reported in the contract. Later tightening means re-auditing every brief template.
