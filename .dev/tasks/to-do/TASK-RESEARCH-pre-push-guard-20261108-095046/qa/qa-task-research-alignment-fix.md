# QA Fix Report: Task-Integrity / Research-Alignment (A.10.25, single cycle)

**QA mode:** task-integrity (fix)
**Fix authorization:** true
**Date:** 2026-11-08
**Task file:** .dev/tasks/to-do/TASK-RESEARCH-pre-push-guard-20261108-095046/TASK-RESEARCH-pre-push-guard-20261108-095046.md
**Findings:** qa/qa-task-validation-consolidated.md (A.10.25 RA1-RA8); detail in qa/qa-task-research-alignment-report.md
**Sources re-read before citing:** src/superclaude/hooks/scripts/launch-job-identity.sh lines 20-229; docs/designs/sc-issue-launch-level-hook.md lines 489-578; .dev/brainstorms/20261108-094705-l2-pre-push-guard/seed-brief.md (79 lines); research/research-notes.md line 5; `ls -d .dev/brainstorms/20261106-l2-prepush-decisions` (No such file or directory)

---

## Fixes

Line numbers are task-file lines after all edits.

| ID | fixed (yes/no) | what changed (step/item, line) |
|----|----------------|--------------------------------|
| RA1 | yes | Step 4.1 (line 213): the web-01 prompt gains a research area "Pushes via other tools", which is documentation reading only. It covers libgit2/pygit2, JGit, isomorphic-git, dulwich, GitPython, the GitHub REST refs API, `gh api` and curl to the smart-HTTP `git-receive-pack` endpoint (http-protocol, gitprotocol-http and git-receive-pack docs). It reasons from githooks that pre-push is a client-side hook run by `git push`, and gives a verdict on the design 19.3 claim at line 520, with citations. The prompt says explicitly: "no network call that writes (no gh api writes, no curl POST, no push)". It adds an other-tools table and an "Other tools" Key External Findings bullet, and the ensuring clause now requires both. Step 4.1's context now also passes on the Step 2.5 `ROUTE web-01:` lines. Step 2.2 (line 176) already had these tools as static-reading candidates for L1. |
| RA2 | yes | Step 2.1 (line 173) analyses the HOME-unset, relative and storeless cases (launch-job-identity.sh 102-106 and 220-225, ordinary on FileNotFoundError), the early exit at 20-24 and the behaviour with uv absent (25-53). Step 2.4 (line 182): the hook log records HOME, PATH, `command -v uv` (or UV-ABSENT), the names of non-GIT variables, and CCSESSION_LAUNCH_ID/CLAUDECODE as yes/no. It adds pass-through experiments (HOME=$SANDBOX/home2 with a marker variable and a PATH prefix; `env -u HOME`; a PATH without uv) and a results column "Hook HOME/PATH/uv as seen". Step 2.2 (line 176) adds the environment push candidates. |
| RA3 | yes | Step 2.3 (line 179): the handoff that could not happen is removed. Git claims stay [UNVERIFIED] and are listed as `UNVERIFIED-GIT D19-n` lines. Step 2.4 (line 182) adds these experiments: a configured `remote.origin.push` onto main and `push.default=upstream`; a SHA-256 pair (oid length 64); a rejected non-fast-forward push; the protected ref last and in reverse order; the look-alikes mainline, feature/main, main2 and refs/tags/main; `--atomic` with hook exit 0 and 1; and `--force-with-lease`. New Step 2.5 (line 185) runs alone after 2.3 and 2.4. It cross-checks each `UNVERIFIED-GIT` line against file 04, runs follow-up experiments in its own mktemp sandbox, appends a section to file 04 before Gaps and Questions, and routes what it cannot settle to web-01. The executor then verifies that the sandbox is removed. The Phase 2 intro (line 170) says that 2.5 is outside the parallel group. Step 3.4 (line 206) carries the `ROUTE web-01:` lines forward, and the staleness note (line 413) now names Steps 2.3, 2.4 and 2.5. The research file set is still 01-04, so Phase 3 and Phase 5 need no change. |
| RA4 | yes | Step 5.3 (line 229): every option states whether it complies with design 19.2 (lines 510-514). Options that need `core.hooksPath` or `extensions.worktreeConfig` are labelled "excluded by design 19.2; would reopen the decision". The Options Comparison gains a "Design 19.2 compliance" row. Section 7 must either recommend a compliant option or explicitly recommend reopening 19.2, with the reason. Section 8 handles "foreign pre-push present" and "core.hooksPath already set" by reporting W-L2-ABSENT (design line 514). The ensuring clause is updated to match. |
| RA5 | yes | Step 2.1 (line 173) adds a question on whether publish() can be reused for an executable hook (fchmod 0o400 at line 171, payload at 169, temp name at 165), together with the ownership and self-test check (design line 512). |
| RA6 | yes | Step 2.3 (line 179) covers 19.6 (design lines 536-545). The agent Globs the four Q-artifact paths (lines 540-543) and tags the claims that depend on them (lines 524 and 534) as [UNVERIFIED: source artifact absent from checkout]. The directory is missing (ls: No such file or directory). |
| RA7 | yes (comment, value kept) | Frontmatter line 22: `depth: "deep"` now carries the comment "reflect TCS band only; the research depth tier is Standard (research-notes.md line 5) and governs agent depth". I kept the value because TCS 320 falls in the reflect deep band, and the comment removes the ambiguity. |
| RA8 | yes | Step 2.1 (line 173) cites seed-brief line 73 and treats unknown identity as DECIDED. Step 5.2 (line 226): Target State applies the owner decision (refuse only main or master pushes, with a diagnostic, and allow the rest) in place of "fail closed where the research supports it". Step 5.4 (line 232): Section 9 does not list unknown identity as open; it keeps only the open details, such as seed-brief line 78. Its ensuring clause is updated. |

## Reread and well-formedness check

- I reread Steps 2.3 and 2.4 (lines 178-184), lines 204-232 (Steps 3.4, 4.1, 4.2 and 5.1-5.4) and frontmatter line 22 with Read after editing. I checked the Phase 2 intro (line 170), the Step 5.3 wording and the staleness note (line 413) with Grep.
- A Bash check over lines 173, 176, 179, 182, 185, 213, 216, 223, 226, 229 and 232 (every changed agent item and its neighbours) found, for each item:
  - the line begins `- [ ] `;
  - it holds the SAFETY block exactly once, byte-identical to the required text;
  - it has an `ensuring` clause;
  - it ends with `Once done, mark this item as complete.`
- Each changed item is still a single paragraph with no nested checkbox. Every prompt is fully embedded, and Grep finds no "see above".
- Gate items are unchanged: the counts 3/3/7/2/2 and max 2 fix cycles stand, and the Post-Completion checks still come before the user summary, with Task Summary and Done last. I edited no gate, Phase 6 or Phase 7 item.
- The research file set is still 01-04 plus web-01 and web-02, so the consumers in Gate 1, Phase 5 and Phase 6 still match. Step 2.5 writes only into file 04.
- Minor note: the Overview line 94 phrase "the four Phase 2 assignments" describes research-notes.md, so it is still accurate. Step 2.5 is a cross-check that produces no new research file.

VERDICT: PASS

