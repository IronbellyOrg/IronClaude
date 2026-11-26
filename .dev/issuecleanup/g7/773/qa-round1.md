VERDICT: FAIL

# QA of findings.md for issue #773

## Blocking defects

1. Next step 5 and the related-issues list miss issue #777, which already carries the "simplification review of the whole chain".
   - Evidence: `gh issue view 777 --repo IronbellyOrg/IronClaude` shows OPEN, author clayphi, created 2026-11-24T18:43:42Z. Title: "Too many manual pieces to track per issue: map the whole watcher and coordinator chain and decide what to automate". Its body quotes gap 7 and the same UNVERIFIED "no whole-chain review" sentence that #773 uses.
   - findings.md step 5 says the review "should be a separate small issue or part of #761 follow-up". Its "Related issues" list does not mention #777. Its PR/issue-search line says "Issue search found no duplicate".
   - Consequence: it changes a next step. Someone following step 5 would file a duplicate issue. The right step is to link or fold #773's last acceptance criterion into #777, and to note that #773 overlaps #777 on gap 7. #777 is later than #773, so the search may have run before it existed. Either way the findings should be refreshed.

## Claims that held up

- Issue state: OPEN, label `enhancement`, no assignee, 0 comments, Project Status Backlog, author clayphi, created 2026-11-24T18:27:54Z. All match.
- PR 707: MERGED, mergedAt 2026-11-20T22:09:24Z. I did not check the commit hash `2ea524514`. #722 and #698 are both OPEN.
- No PR is linked to #773. `gh pr list --search 773` is empty, and the only open PR is #762 (swarm, unrelated).
- Citations, all re-read at HEAD a7ae3dd30:
  - `complete.py:124`: the `updateProjectV2ItemFieldValue` mutation. Correct.
  - `github.py:109`: the Pipeline `fieldValueByName` read. Correct.
  - `create.md:97`: "No self-assignment". Correct.
  - `SKILL.md:87`: Wave 3 assign. Correct.
  - `claim.md:48`: `gh issue edit --add-assignee @me`. Correct.
  - `commands/issue.md:102-103`: the Will Not lines "Create labels..." and "Write any issue field other than Complexity". Correct.
  - `commands/issue.md:43`: the `--pipeline` row is the launch level. The naming trap is real.
  - `requirements.md:64`: R38. Correct.
- Only one writer of Project fields exists in `src/superclaude`. Grep for `updateProjectV2ItemFieldValue`, `addProjectV2`, `issue-field-values`, `add-label` and `issue edit` found only `complete.py:124`.
  - The skill docs `create.md` and `claim.md` write the Complexity field through `issue-field-values` and assign through `gh issue edit`. That is the Complexity field and assignment, not the Pipeline, Status or label fields. The claim holds.
  - `ensure_trigger_label` is called from `first_run.py:195` and creates the repository label only.
- `scripts/` holds exactly `clickup_claim.py`, `orca_worktree.py` and `origin_repo.py`.
- Verdict still-relevant, medium/M, and P2 are justified. Nothing is built, the owner gates (#722, #698) are open, and the manual workaround exists. The P2 reasoning is sound.

## Minor notes

- The findings could say the `launch-level-guard.sh` hook blocks `gh api` calls with a method or field. This is relevant if an agent session ran the Project writes. It does not change the verdict.
- "UNVERIFIED" marks on R38 coverage and non-admin write rights are appropriate.

## What I checked

I read findings.md in full and the live #773 (body and comments). I re-read every cited line, listed `scripts/`, and ran the broad grep over `src/superclaude` for label, project and field writers. I checked the states of #722, #698, #777 and PR 707, and searched issues and PRs for overlap. I edited nothing on GitHub and did not touch findings.md.
