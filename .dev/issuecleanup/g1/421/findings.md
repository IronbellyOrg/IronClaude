# Issue 421: Codex security-review completion

Template: task-local findings structure registered in ../362/report-template.md, adapted to issue 421 and the coordinator's required fields.

## Verdict and evidence

**Verdict: still-relevant.** Keep the issue open. Static inspection confirms both the code-only completion gate and the missing review recheck after the CI wait. No evidence establishes an active implementation of this fix.

- Issue: https://github.com/IronbellyOrg/IronClaude/issues/421, OPEN and in Backlog when read on 2026-11-23. Its sole comment, dated 2026-11-17, also says the bug remains. `closedByPullRequestsReferences` is empty.
- Checkout inspected: `a7ae3dd30fcf88aaab655c37e94e58e121c2d863` on `ironbelly/Issuecleanup`. This report describes that checkout, not an independently fetched latest master.
- `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/pr_submit/reviewers.py:113-133` parses and returns only `code_review`; `:180-207` accepts completion on that half's status and head. A sibling `security_review` with a running status or stale head cannot affect that decision.
- `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/pr_submit/reviewers.py:245-246` allows clean when no unresolved roots are selected, and `:384-389` makes clean/findings immediately done, before the timeout branch.
- `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:312-313` switches to CI polling and permits `TERMINAL_CLEAN` on clean CI without requiring a fresh review snapshot. Its end-of-wait reread concerns merge conflicts, not reviewer completion.
- Original integration: PR #337, merged as `d4ac8a3d906883bd40337149eebc0d6cc932d096`. Later related PR #499, merged as `4ab620d1fad0588b145ac99a3f934881e10e31fc`, handles malformed Augment markers, not Codex security completion. Local path history shows those two relevant reviewer changes, not a security-half fix.

## Real current state

**Present:** shared reviewer snapshots, Codex identity/head/time validation, collection of Codex thread roots, bounded waits, and combined reviewer results already exist. The missing piece is completion across both Codex activities, not a missing Codex integration.

**Still missing:** validation and completion gating of `security_review`; a post-CI review refresh before a final clean result; and tests that distinguish completed code review from running or stale security review. The current contract explicitly says security review is ignored at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md:119-140`.

The timing concern is corroborated by live PR reviews: PR #360 has separate Codex reviews at 16:38:00Z (code) and 16:44:29Z (security) on 2026-11-04 for head `7674c709fb`. PR #358 has a security review at 14:02:19Z. These timestamps confirm separate later security submissions, but do not independently prove the monitor's earlier clean events; those are quoted historical evidence in issue #421.

The issue's old related-issue status is partly stale: #381 is CLOSED today, alongside #382, #456 and #361. That administrative change does not fix #421. PR #369 fixed the installer findings from #360; it did not fix the monitor that missed them. PR #367 explicitly recorded the premature Codex clean as an open monitor follow-up.

## Concrete next steps

1. Extend the existing Codex marker parser and completion decision, rather than adding a second monitor. When a security half is present, validate its status, head and finding count independently; require both halves to be completed for the expected head before either clean or findings can finish the wait. Keep older markers without a security half compatible. Treat a completed security `has_any_findings: null` as the observed no-findings form, not malformed code-review data.
2. Keep running/stale security state pending within the existing timeout and report security incompleteness explicitly on expiry. Do not raise the timeout solely from the historical lag: the maximum current service delay is UNVERIFIED.
3. In the skill's CI-wait path, fetch and classify a fresh review snapshot before final clean; route new findings within the existing round budget, or report them when the budget is exhausted. Preserve head binding and existing no-response/max-round terminal rules.
4. Add regression cases for code complete/security running, security stale head, both complete with/without findings, security null finding count, missing legacy security half, a security root arriving after an earlier clean snapshot, and a finding arriving during the CI wait. Existing completed fixtures must retain their outcomes.
5. Include both marker halves in diagnostic poll evidence and update the detection contract and user guidance. This makes future early-clean reports diagnosable without relying on deleted session logs. No implementation, source edits or GitHub writes were performed in this task.

## Complexity and size

**Complexity: medium. Size: M.** The core change is local, but completion spans two asynchronous activities, head/time attribution, timeout behavior, CI-wait transitions, regression fixtures and protocol documentation. It needs more than a parser-only edit, not a new subsystem.

## Priority

**Priority: P1.** A false final clean result can conceal security findings and mislead a merge decision in every monitored PR using Codex security review. It blocks trusting the monitor's clean signal for those PRs; this is not evidence of an ongoing production compromise, so P0 is not justified.

## Dependencies

- **Needs:** no hard prerequisite issue verified. The shared Codex integration from merged PR #337 is already present.
- **Blocks:** no numbered issue dependency verified. Functionally, it blocks reliable final reviewer clearance when Codex security review is enabled.
- Related conflict/draft/marker fixes are integration context, not prerequisites. Formal issue dependency and full timeline events are UNVERIFIED under the permitted GitHub commands.

## Related issues

| Issue | Current state from GitHub | Relationship |
|---|---|---|
| #381 | CLOSED | Augment late-inline-comment classification, same classifier family but a different cause. |
| #382 | CLOSED | Unreadable Augment marker, addressed by PR #499, not this Codex gate. |
| #456 | CLOSED | Missing-brace variant of the Augment marker problem, addressed by PR #499. |
| #361 | CLOSED | Late conflict synchronization in the same CI-wait phase, implemented in PR #424. |
| #305 | CLOSED | Parent conflict-resolution work mentioned by #361. |
| #375 | CLOSED | Draft merge guard implemented in PR #428; a guard around fixes does not wait for security completion. |
| #330 | Historical context; current state UNVERIFIED | Ponytail installation work whose PRs #358/#360 supplied the original timing evidence. |

Links use https://github.com/IronbellyOrg/IronClaude/issues/<number>.

## Related PRs

All rows below were read live with the allowed `gh pr view` command and are MERGED. None is a verified implementation of #421.

| PR | Purpose and relevance | Merge commit |
|---|---|---|
| #337 | Original shared Codex reviewer integration; current completion gate derives from it. | `d4ac8a3d906883bd40337149eebc0d6cc932d096` |
| #358 | Ponytail installation; original separate Codex security review evidence. | `9b9497e64b830f735aac2765ebb74ed658d183f1` |
| #360 | Ponytail pin; two code/security cycles provide the issue's main evidence. | `c83e3d78da4367bd44f61f65d1490fb3dd7119af` |
| #367 | Committed follow-up notes explicitly include the premature Codex clean gap; documentation, not a fix. | `35d6ab9cc62b24e5685f41fe921effc140e876d7` |
| #368 | Orca worker-contract changes; corroborates separate later Codex security reviews, not monitor remediation. | `f3c1ef06296086a2c4d341ef807c871ddd6b1baf` |
| #369 | Fixes the installer issues left by #360, not reviewer completion. | `7632090d7389977dc0648054ccff34ddb972421d` |
| #424 | Late CI-wait conflict synchronization, related orchestration surface. | `ec1babd9b6c9a7bb9efc45643d4c8075353c6eca` |
| #428 | Draft merge guard during fixes, unrelated to waiting for both Codex activities. | `0b8a5801d75f159bcbca7087b99507c2a50d8dba` |
| #499 | Augment malformed-marker handling; leaves the Codex parser code-only. | `4ab620d1fad0588b145ac99a3f934881e10e31fc` |

Links use https://github.com/IronbellyOrg/IronClaude/pull/<number>.

## Verification limits and negative evidence

- Read issue #421's body, its one comment, current state/project metadata, creation/update timestamps and closing-PR references. Created 2026-11-07T05:40:25Z; updated 2026-11-17T07:12:08Z. **Full issue timeline events and marker edit histories: UNVERIFIED.** The brief permits only issue/PR view/list, which do not expose the full issue event stream or historical comment edits; no `gh api`, browser workaround or outward write was used. The review is therefore bounded, not a claim to have reconstructed every event.
- Historical monitor log timestamps, original inline comment contents, all historical marker edit states and the claimed 1.5-7.6 minute delay range are **UNVERIFIED independently** in this task. The durable issue body records them; live formal PR review timestamps corroborate only the separate later submissions. No removed worktree logs were available as inputs.
- Search `gh pr list --state all --search '421 in:body'` returned no PR. A separate all-state search for `Codex security in:title,body` returned historical/context PRs, including #367 and #499, but no verified fix for this gate. This is negative search evidence, not proof that no private branch exists.
- Source grep for `security_review` in the Python monitor package returned no matches; in the protocol it returned the explicit ignore rule. In the test tree the matches were fixture data, not a named security-half regression. Directly inspected existing Codex tests cover completed fixtures, running code review, wrong head, malformed JSON, timestamps and watermark behavior. No claim of full test execution is made.
- `/sc:analyze src/superclaude/pr_submit --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g1/421/analyze` was invoked through Skill at the top level. See the analysis report and its return contract in this task directory. Graph readiness was stale due to one pending report-file modification elsewhere in the shared worktree; native source reads/searches were used instead.
- No tests, builds, live monitor run, source modifications, staging, commit, push or GitHub mutations. Latest remote master and an active unpushed implementation remain UNVERIFIED. A freshness hook initially rejected an edit to the new stub until a tracked Read was performed; the retry used Edit normally, without bypassing the hook.
