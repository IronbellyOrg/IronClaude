VERDICT: PASS

# QA of findings.md for issue #773

Reviewed: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g7/773/findings.md (HEAD a7ae3dd30, checked 2026-11-24). Read-only; nothing edited or posted.

## Blocking defects

None.

## Minor notes (do not change verdict, complexity, size, priority, a step, a dependency or a safety claim)

1. Related/overlap list is incomplete. Besides #777, these open issues overlap or touch the same ground and are not listed: #776 (skill for the two approvals; #773's own body calls it "the sibling issue" it hands the approval step to), #772 (stage flow and what Pipeline Full means; bears on which Status/Pipeline values a setup command may set), #770 (watcher hands claim to coordinator), #775 (comment cancels approval), #753 (always accept maintainers/admins as approvers; touches the #698 approver rule). #777's body lists 770, 772, 775, 776 as the filed suggestions it maps. Suggest adding #776 and #772 as soft dependencies and the rest as related. Step 5 (fold into #777) stays correct.
2. Related list says "#761 ... this covers 1 and 7"; #777 also claims gap 7. This is already handled in step 5. Note that #777's body says it "would replace" #773's Moving pieces section as the topic's home, which supports step 5.
3. The findings say "No pull request covers this". Verified: the only open PR is #762, unrelated (swarm completion markers).

## What I checked (all against live source and GitHub)

- Citations, each re-read at the stated line: `complete.py:124` (`updateProjectV2ItemFieldValue`, in `MOVE_MUTATION`); `github.py:109` (`pipeline: fieldValueByName(name: "Pipeline")`, a read query); `create.md:97` ("No self-assignment" in step 8); `SKILL.md:87` (Wave 3 assign, `--add-assignee @me`); `claim.md:48` (`gh issue edit ... --add-assignee @me`); `commands/issue.md:102-103` ("Create labels, issue types, issue fields..." and "Write any issue field other than Complexity", under Will Not) and `:43` (`--pipeline` row, launch level worktree/full/none); `requirements.md:64` (R38 text matches the quote). All correct.
- No other writer: grep of `src/superclaude` (py, sh, md) for `updateProjectV2ItemFieldValue`, `addLabels`, `--add-label`, `issue-field-values`, `add-assignee`, `item-edit`, `project item`. The only Project-field mutation in code is `complete.py`. `issue-field-values` and `--add-assignee` appear only in skill markdown (Complexity POST in create.md; assignment in claim). `launch-level-guard.sh` only blocks such calls. `ensure_trigger_label` (`repo_init.py:108`, called from `first_run.py:195`) creates the repository label only; no code applies it to an issue. The trigger label is only used as a read filter in `cycle.py` and `github.py`.
- `scripts/` of the skill: `clickup_claim.py`, `orca_worktree.py`, `origin_repo.py`; no Project setup helper. Repo `scripts/` has nothing related.
- Live states: #773 OPEN, label enhancement, no assignee, no comments, Backlog (opened 2026-11-24T18:27:54Z by clayphi); #777 OPEN (2026-11-24T18:43:42Z, clayphi); #722 OPEN with the ironbelly review (still-relevant, Complex/L, P1) and clayphi's reply that it is lower priority; #698 OPEN with ironbelly review (still-relevant, Complex/M, P2); #761 OPEN; PR #707 MERGED 2026-11-20T22:09:24Z, commit 2ea524514 exists. #655 CLOSED; #716, #721, #733 OPEN.
- Issue body: priority section says High, set by Clay, matching the findings' statement; acceptance criteria say "not approval to build now"; the three open questions and the UNVERIFIED non-admin write question match the findings.
- Verdict (still-relevant), medium/M, P2: justified. No code or PR delivers the work; it is gated on owner answers (#722, #698) and R38 confirmation; a manual workaround exists. Next steps are ordered correctly (answers first, no write authorized, flag name must avoid `--pipeline`). The naming-trap note is correct per `issue.md:43`.
- Safety claims (R38 scope UNVERIFIED, non-admin write UNVERIFIED, trial write not authorized) are appropriately hedged.
