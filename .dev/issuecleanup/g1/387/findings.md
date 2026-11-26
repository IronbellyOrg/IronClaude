# Issue 387: bare-Python hook bypass review

Structure: Findings template in ../362/report-template.md, read before creating this stub; required fields come from the coordinator brief.

## Verdict and evidence
**Verdict: still-relevant.** Reviewed on 2026-11-23 at checkout `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`. Both exact reported inputs still return hook exit 0 (allowed), not the required exit 2; the added backtick variant also returns 0. Plain bare Python is blocked and an ordinary UV command is allowed, so this is a selective parser defect rather than a disabled hook.

Evidence: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/scripts/block-bare-python.sh:84-86, :130-140 and :261-292. The named coprocess is treated as an ordinary wrapper followed by a command name; shell-fed heredocs skip the parent-expansion state and incorrectly apply child-shell quoting to parent-shell substitutions. Source and hook test history still ends at PR 359, merge `605da2ffb83b93302ca51d654e9c2075e85217a7`. PR 367, merge `35d6ab9cc62b24e5685f41fe921effc140e876d7`, recorded these unresolved defects, not fixes. Its committed evidence is /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/followups/20261104-pr359-pr360.md:26-45.

The live issue remains OPEN, its project status is Backlog, and no closing PR is recorded. Its two 2026-11-17 comments first confirmed the gaps, then recorded the owner's choice to patch them. No evidence of implementation progress was found in this checkout or the relevant PR searches; prior delivery of the underlying hook is not progress on this follow-up fix.

## Real current state
The installed-distribution source includes a working Bash-command policy scanner and its matching plugin copy. Both remain byte-identical (`cmp` exit 0). Existing behavior and packaging/installation checks pass: **134 passed, 45 deselected in 2.62 seconds**, using `uv run pytest tests/hooks/test_block_bare_python.py tests/cli/test_install_hooks.py -k block_bare_python -q`. This includes the existing 100 KB timing check and 200 KB stdin check, but not regression cases for either issue-specific gap.

Supplemental task-level probes passed JSON command strings to the hook without executing those strings:

| Input held as scanner data | Observed exit | Required behavior |
|---|---:|---|
| `python3 -c 1` | 2 | Block, control passes |
| `uv run python -c 1` | 0 | Allow, control passes |
| `bash <<EOF` / `echo '$(python3 -c 1)'` / `EOF` (three lines) | 0 | Block, issue remains |
| `bash <<EOF` / ``echo '`python3 -c 1`'`` / `EOF` (three lines) | 0 | Block, same parent-expansion gap |
| `coproc worker { python3 -c 1; }` | 0 | Block, issue remains |
| `coproc { python3 -c 1; }` | 2 | Block, unnamed case already works |

The tests currently cover unquoted expansion into cat and quoted shell heredocs, not their problematic combination, and contain no coproc case: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/hooks/test_block_bare_python.py:80-143. The existing hook is delivered; the requested parser corrections and their regressions are not present in the reviewed tree.

## Concrete next steps
1. Apply the owner's recorded 2026-11-17 choice: patch the two parser gaps, retaining the existing design. Do not substitute the broader word-blocking redesign that the owner declined.
2. Recognize coproc's optional name and compound-command body; retain unnamed-body scanning and add blocked/allowed cases for both forms.
3. Preserve both heredoc obligations: scan substitutions executed by the parent for unquoted delimiters, then account for the receiving shell's body. Add dollar-substitution and backtick regressions, plus quoted-delimiter/ordinary-text controls to prevent false blocks.
4. Keep the source and plugin hook byte-identical; update header/changelog claims to the actual corrected behavior. Rerun the existing hook and installation tests, including the 100 KB under-one-second requirement, with the new regression cases. Preserve the bash/jq/awk-only scanner and exit 0/2 fail-open contract.

Affected source: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/scripts/block-bare-python.sh. Mirror: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/plugins/superclaude/hooks/scripts/block-bare-python.sh. Regressions: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/hooks/test_block_bare_python.py. Packaging checks: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/cli/test_install_hooks.py. Documentation: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/CHANGELOG.md and the hook header. These are future implementation steps, not changes made by this task.

## Complexity and size
**Complexity: medium. Size: M.** Two bounded parser-state interactions and their false-block controls need careful regression work across the source, plugin mirror, tests and documentation; no new subsystem or dependency is needed.

## Priority
**P2.** The gaps weaken the repository's UV-only development policy in uncommon shell syntax, but ordinary bare calls are blocked, the hook explicitly fails open by design, and no production outage, data loss or release-blocking dependency was established. This is a genuine correctness fix, not evidence of a hardened security boundary.

## Dependencies
Needs: no open prerequisite verified. Issue 357 (original hook request) is CLOSED and its implementation PR 359 is merged. Blocks: no issue dependencies are recorded; the live blockedBy and blocking lists each have totalCount 0. No parent or sub-issues are recorded. Correcting the hook is technically independent of the broader release-cleanup plan in issue 571.

## Related issues
- [357](https://github.com/IronbellyOrg/IronClaude/issues/357): CLOSED, original request to enforce the UV rule before Bash calls. Its implementation exists; this issue repairs its remaining syntax gaps.
- [571](https://github.com/IronbellyOrg/IronClaude/issues/571): OPEN, broader release/command cleanup, mentioned in the status-review comment. Its live body contains no specific fix for this hook; contextual only, not a verified blocker or replacement.
- Keyword search also returned 365 and 394; no direct dependency on either was established. Do not infer related work from search hits alone.

## Related PRs
- [359](https://github.com/IronbellyOrg/IronClaude/pull/359): MERGED 2026-11-04, original hook implementation, merge `605da2ffb83b93302ca51d654e9c2075e85217a7`. Read its body, comments/review summaries, file metadata and merge evidence. The two inline review discussions are identified in issue 387 and the committed follow-up record.
- [367](https://github.com/IronbellyOrg/IronClaude/pull/367): MERGED 2026-11-04, notes recording these open findings, merge `35d6ab9cc62b24e5685f41fe921effc140e876d7`; its body explicitly says no code changes. This corrects the issue's description of earlier diagnoses as local/uncommitted: the earlier round diagnosis folders were committed by this PR, while the two final bypasses were recorded as unresolved notes.
- No later fix PR verified. All-state searches for `"block-bare-python"` returned only 359; `"coproc"` returned 359 and 367. A broad `387` search returned unrelated 54, 120 and 260, not evidence of a fix. Results are search evidence, not proof that no unmentioned branch exists.

## Verification limits and negative evidence
- **Timeline UNVERIFIED in full.** Attempted `gh issue view 387 --repo IronbellyOrg/IronClaude --json timelineItems`; this CLI rejects timelineItems as an unknown field. Recovered the available history via createdAt (2026-11-05), updatedAt (2026-11-17), both comments, project/dependency fields and closing-PR references. The brief permits only issue/pr view/list reads, so no API/browser workaround was used. Label, assignment and cross-reference event chronology remains unverified.
- **Exact inline discussion text and current resolution status UNVERIFIED.** PR view exposes comments and review summaries, not the two inline threads. Issue 387 and the committed PR 367 notes preserve their claims; source inspection and scanner-only probes independently verify the actual defects.
- **Remote default-branch freshness UNVERIFIED.** No fetch or branch movement was performed. Code findings are scoped to supplied checkout HEAD, not asserted against unseen later commits or private working branches.
- No actual bare Python payload was executed. The probes exercised only the hook's decisions; Bash execution semantics were checked against source reasoning and the issue/follow-up evidence, not re-executed with bare Python.
- No full repository suite, live user-home installation, exhaustive shell grammar audit or fuzzing. The narrow existing tests all passed; passing them does not close this issue because the failing combinations are absent.
- Required architecture analysis and its command handoff are under /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/387/analyze/. Codegraph was fresh at readiness but does not index this shell file, so direct reads were used. Initial report edits were blocked by the freshness hook until the newly written stubs were explicitly read; retries then succeeded.
- Only task-local reports/evidence were written. No source edits, staging, commits, issue/PR mutations or outward publication were performed.
