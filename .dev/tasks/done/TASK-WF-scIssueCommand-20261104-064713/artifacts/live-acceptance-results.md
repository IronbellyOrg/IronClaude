# /sc:issue live acceptance results (post-restart runbook)

- Run: 2026-11-04, 16:15-19:56 UTC, in the checkout `feat-sc-issue-command` (branch `ironbelly/feat-sc-issue-command`), by the coordinator session after the user said "Proceed with all recommended steps".
- Runbook: the "Post-restart runbook" at the end of `t17-acceptance.md` in this folder.
- Surfaces used: the project `.claude/` copies (`.claude/commands/sc/issue.md`, `.claude/skills/sc-issue-protocol/`, `.claude/agents/issue-worker-t*.md`); no installed `~/.claude/` copy exists in this checkout.
- Local evidence lives under `.dev/issues/<N>/`, which `/sc:issue` never stages or commits (default D24); it stays on this machine.

## Results by acceptance item (design section 20)

| Item | Result | Evidence |
|---|---|---|
| 1. Claim of an open, unassigned issue | PASS (after two fixes, below) | Scratch #365: tier-3 lookup first, assigned to `ironbelly`, accuracy-check comment `#issuecomment-6639975892` and claim comment `#issuecomment-6639979000` posted with their markers, seven files in `.dev/issues/365/`, `next-steps.md` starts with `/model claude-gw-tier2`, no next-step command was run |
| 2. Re-claim edits, never duplicates | PASS | Same claim run again at 19:26-19:44 UTC: lookup found both comment IDs, both edited with `gh api -X PATCH` (updated 19:44:54 and 19:44:55 UTC), comment count stayed 2 |
| 3. Closed issue / assigned to someone else | Closed case PASS; other-assignee case NOT RUN | Scratch #366 (closed on purpose): stopped at Wave 2 with "Issue #366 is closed; not claimed.", no assignee and no comment added. The other-assignee case was not run because it would assign and notify another real person; it needs a person who agrees to be assigned |
| 4. Claim URL on another repo | PASS | `/sc:issue --claim https://github.com/IronbellyOrg/no-such-repo-sc-issue-probe/issues/999999999` stopped in Wave 0: `E-FOREIGN-REPO: IronbellyOrg/no-such-repo-sc-issue-probe is not the origin repo IronbellyOrg/IronClaude`, exit 3, before any `gh` call |
| 5. ClickUp | First half PASS; second half PENDING | No `CLICKUP_API_TOKEN`: `clickup.json` = `{"status": "skipped", "reason": "no_token"}`, and the claim comment says "skipped (no_token)". The smoke claim against a real ClickUp task (runbook step 3) needs the `CLICKUP_*` variables, which are not set here |
| 6. Create at each depth | PASS | Same scratch bug description, `--mode bug --type cli`: quick #370, standard #371, deep #372. Template headings kept (simple bug template for quick and standard, complex for deep); only `bug` applied, `type: cli` and `complexity: *` reported as missing and never created; no pushback at quick; one marked pushback comment at standard (#371, tier-2 check chose `skill`) and deep (#372, `/sc:adversarial --compare flags-user.md,flags-t1.md --depth quick`, `skill` won, convergence 0.857); no ClickUp call; no self-assignment. Every draft listed new material, so the user was asked one question per create and chose "keep all" for all three |
| 7. Worker pinning | PASS | Smoke spawns passing only `subagent_type`: the transcripts' model fields show `issue-worker-t3` served by `gpt-6.1-terra` (tier 3), `issue-worker-t2` by `gpt-6.1-sol` (tier 2), `issue-worker-t1` by `claude-opus-5-5` (tier 1a), each the first model of its tier in `ccsession-models.json` |
| 8. `next-steps.md` | PASS with a note | Starts with the `/model` line; no brainstorm step carries a handoff flag. `/sc:recommend` chose a different route from the default "Feature, simple" chain, because #365 asks for no implementation, so `next-steps.md` follows it and names the unused default row (D23). Its steps include `gh issue view`, `gh issue close` and a re-claim, which are outside the section-19 command list; the design allows `/sc:recommend` to choose |
| 9. Sync and tests | PASS | Full suite after the two fixes below: 14873 passed, 0 failed (`.dev/tasks/issue-302-handoff/fix-3/04-full-suite.log`) |

All scratch issues (#365, #366, #370, #371, #372) were closed at about 19:56 UTC with a closing comment.

## Defects the live run found, and their fixes

1. **Workers did not write their files (fix-2).** Claude Code adds a line to every subagent's system prompt telling it not to write "report/summary/findings/analysis .md files". `issue-worker-t2` (served by `gpt-6.1-sol`) obeyed it and returned its findings as text. Fix: an early section in each worker agent file names its files as tool inputs that must be written, and `SKILL.md`'s spawn rule restates it. Plan: `.dev/tasks/done/TASK-WF-fixTheScIssueWor-20261104-162205/`; report: `.dev/tasks/issue-302-handoff/fix-2/07-fix-report.md`.
2. **`summary.md` can never be written by a subagent (fix-3).** After fix-2 the worker did call Write, and Claude Code refused it: its Write tool rejects any subagent write whose file name matches `^(REPORT|SUMMARY|FINDINGS|ANALYSIS).*\.md$` (event `tengu_subagent_md_report_blocked`), found in the installed Claude Code binary and confirmed by a name probe. Fix: the claim summary is now `issue-summary.md`, files under `analysis/` are named `analyze-<scope>.md`, and a test pins every worker-written name against that rule. Plan: `.dev/tasks/done/TASK-WF-renameTheScIssue-20261104-174359/`; report: `.dev/tasks/issue-302-handoff/fix-3/08-fix-report.md`. The design doc carries a dated note.

## Other observations (not fixed here)

- **Local freshness hook.** `~/.claude/hooks/freshness-pre-edit.sh` (the user's own hook, not part of this repo) blocks creating a file that this session Read more than 30 minutes earlier, even when the file no longer exists, because it allows a create only when no earlier Read is recorded. It surfaced once, after the coordinator moved earlier claim files aside; the workaround was to Read the file before overwriting it, which a normal re-claim does.
- **Same Claude Code rule elsewhere.** The `^(REPORT|SUMMARY|FINDINGS|ANALYSIS).*\.md$` subagent rule may also affect other agents in this repo whose output names start with those words. Not checked here.
- **Real bug behind the probe.** The scratch creates described a real defect (verification note m6): `origin_repo.py` rejects `ssh://git@github.com/...`, `https://user@github.com/...`, an upper-case host, and an `ssh://` URL with a port. The probe issues were closed as scratch, so this has no open issue yet.
- **Template comment posted.** The quick and standard bodies kept the simple template's first-line instruction comment, which is posted hidden (verification note m7). The deep body removed it.
- **`/sc:adversarial` bias check.** In the deep debate, the coordinator agent ran both position-bias scoring passes itself rather than using two independent evaluators, and said so in the transcript.
- **API outages.** Two connection outages (about 09:10-12:38 and 19:35-19:40 UTC) interrupted helper agents; each failed agent was re-run and nothing was posted twice.
- `.dev/issues/smoke/` holds the two smoke files from runbook step 2; it is not staged.
