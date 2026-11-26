## Verdict
still-relevant. Issue [678](https://github.com/IronbellyOrg/IronClaude/issues/678) is OPEN with no comments as checked on 2026-11-24. Its body records that the owner parked it on 2026-11-19, not that the defect was fixed or rejected permanently. Recommend retaining that parked disposition, not closing as completed or marking not-planned on the owner's behalf.

The narrow-source analysis ran through the Skill tool and completed: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g4/678/analyze/analyze-report.md. Current /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/scripts/launch-level-guard.sh:456-468 still records executable and flag indicators separately; :510 classifies a Claude launch as ESCAPE only when both are set. This leaves the reported bare-prompt form outside that escape classification. The design at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/designs/sc-issue-launch-level-hook.md:176 also still describes the flag requirement.

Historical evidence is real but narrower than the issue title: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/tasks/done/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/ob-logs/logs/h1.jsonl:74-80 records the parent command, child SessionStart, child prompt, child Stop with the requested word, and returned output. /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issues/442/observation-results.md:263-316 records item 8 as FAIL. PR 677 merged that archive at ccf3c461800523921a36bd096f2a35a6f40861a9; PR 685 merged the runbook/results at cba6ef2145b0aabedda0f66653dadba7671c93fe. Neither is a classifier fix.

UNVERIFIED: that the child actually performs unrestricted tool calls in a real governed launch today. The isolated observation's /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issues/442/scripts/setup.sh:125-139 registers only the logging probe at PreToolUse. Code permits no-marker prompts without a binding at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/scripts/launch-level-guard.sh:367-368 and unbound tool calls at :391-395, but that reasoning is not a live governed-child test. No new live launch or unit test ran in this review.

## Complexity and size
complexity medium; size S. The likely repair is confined to the shared classifier, design and regression cases, but proving child identity/tool enforcement and repeating the live observation needs a disposable governed session; this is not just a one-line verified fix.

## Priority
P3. Preserve the owner's explicit low-urgency parking: the classifier gap is a launch-limit risk, but current unrestricted-child impact is UNVERIFIED and item 8 is not a required ship-gate item. /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issues/442/observation-runbook.md:718-726 requires items 1 and 5, OB-H2 and OB-H3; /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/hooks/test_launch_level_observations.py:79-87 defines the same four required gate items. This is not a claim that governed launches are otherwise safe or enabled.

## Concrete next steps
No implementation is in progress in this review; leave the issue parked unless the owner separately reopens work. If they do:
1. Reproduce with a disposable governed parent and child, recording each session's binding and one harmless tool decision. Do not use the earlier log-only setup as proof of unrestricted governed behavior.
2. Fix the shared Bash/Monitor escape classifier to cover the bare executable-plus-prompt forms for both executable names, then add regression cases for the bare form, path/wrapper forms and all governed levels. Update the matching design text. /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/hooks/test_launch_level_guard.py:3129-3167 shows the current flagged-launch cases and the explicit allowed-version expectation; changing to an executable-wide block must deliberately update that expectation to match the issue's acceptance rule.
3. In that separately authorized implementation run, execute the regression tests and repeat live observation item 8 before recording completion. Do not mark the historical failure PASS by editing its record.
These are conditional follow-up steps, not authorization to launch a session, install anything or change GitHub.

## Dependencies
- Related to issue [442](https://github.com/IronbellyOrg/IronClaude/issues/442), the OPEN live-observation task, because it owns item 8's result. It does not require 678 to be fixed to pass its four-item ship gate. The live 442 comment dated 2026-11-23 explicitly keeps item 8 parked and accounted for separately.
- No prerequisite issue number or other blocking edge was verified for 678. A future live rerun requires the owner's separate authorization and a disposable governed environment, not completion of another identified issue. GitHub's full dependency/timeline data was not available through the permitted issue/PR view and list reads: UNVERIFIED beyond these explicit references.

## Related issues
- [442](https://github.com/IronbellyOrg/IronClaude/issues/442): OPEN, parent live-observation work; its comments distinguish parked item 8 from the required gate observations. Its older no-observations wording does not override the archived child-turn evidence.
- No additional issue relationship was independently established in this narrow review.

## Related PRs
- [432](https://github.com/IronbellyOrg/IronClaude/pull/432): MERGED, 3b344dd4e0481a9063d4ac22abb24a9e589614a6, original launch-level guard. Its body explicitly calls the guard text-layer checks, not universal prevention; it is not evidence of a bare-prompt repair.
- [677](https://github.com/IronbellyOrg/IronClaude/pull/677): MERGED, ccf3c461800523921a36bd096f2a35a6f40861a9, archived observation logs and plan; its body records item 8 FAIL.
- [685](https://github.com/IronbellyOrg/IronClaude/pull/685): MERGED, cba6ef2145b0aabedda0f66653dadba7671c93fe, observation runbook/scripts/results; explicitly records item 8 FAIL and references 678. Its changed-file listing is observation material, not a production classifier fix.
- Read-only PR searches for 678, including the quoted-number search with limit 30, returned only 685. No open completion PR was returned by those searches; exhaustive absence of differently worded work is UNVERIFIED. A broader bare/Claude search was too noisy to support an absence claim and was not treated as proof.

Review limits: static source and historical records only; no uv, pip, test execution, new child session, source change, staging, commit or GitHub write. The optional graph returned no indexed Bash target and analysis fell back to source reads. Findings were populated from the brief's seven-heading structure; the analysis uses the command's required scope/findings/metrics/recommendation structure.
