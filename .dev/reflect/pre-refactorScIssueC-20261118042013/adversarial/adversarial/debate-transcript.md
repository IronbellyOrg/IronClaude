# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 plus the Round 2.5 invariant probe
- Convergence achieved: 100% (15 of 15 points)
- Convergence threshold: 80%
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 3 (advocates are the three reviewers that wrote the cards; they kept their own context)

## Round 1: Advocate Statements

### Variant 1 Advocate (reviewer 1, analyzer, sonnet)
- Position: card stands (pass-with-findings). Three real defects, none blocking: the bare --submit rule change, the stale launch text at claim.md:142, missed sites. V3's evidence on the --submit rule is stronger; treat it as an owner answer needed before Task 3.
- Steelman V2: claim.md:142 tells the person to "run the printed implement command ... to let it continue" for every launched agent; at default full the agent already implements, so the user is told a wrong next action. V2 is also right that Task 5 has no test of the new --submit behaviour (plan:50 vs plan:70). Steelman V3: the design record already requires the stop (flag.md:85: "`--submit` with a value, or with `--pipeline worktree` or `--pipeline none` or no `--pipeline`: STOP"), so Task 3 reverses a recorded decision; V3 also found the architecture reference (:1557, :1635), design-record lines 66/78/85/87 and worker-brief.txt:17-19.
- Claims: every claim tied to a re-read line; only card to raise the stricter gate for a bare claim (F3); checked launch.py/test_launch.py (F4). Zero blocking is right: wording and scope, not a safety boundary.
- Weaknesses of others: V2's blocking grade is arguable (redundant instruction; plan tests do not pin it). V3 rejects F3 because the gate names both levels, but a bare claim moves from the worktree gate to the stricter full gate (U1, issue.md:16). V2 accepts the --submit relaxation although the design record forbids it.
- Concessions: F1 should have cited flag.md:85; missed the architecture reference; F5 vague.
- Shared assumptions: A-001 ACCEPT. A-002 QUALIFY (no code parses --pipeline; `--level` required not confirmed by its grep; tests should pin the Markdown, which Tasks 5 and 6 do). A-003 ACCEPT (launch.py:33,:92; test_launch.py:932-939; WORKER-CONTRACT.md:293). A-004 QUALIFY (in src/superclaude the only bare caller is documentation; docs/, plugins/, README not searched; check before Task 3).

### Variant 2 Advocate (reviewer 2, qa, haiku)
- Position: keeps the missing-submit-test finding; withdraws the unconditional blocking grade for the launch message (evidence shows ambiguity, not an observed incorrect launch).
- Steelman V1: changing the default need not remove explicit authorization for submission; the design rejects submit without pipeline (flag.md:85). Steelman V3: distinguishes existing ambiguous wording from a newly introduced failure ("For full" could replace rather than append, claim.md:142).
- Claim: the planned test (plan:70) checks flag names and an error message only; it cannot tell accepting omitted --pipeline from rejecting it.
- Weakness of V1: the ship gate already covers both worktree and full (claim.md:133); its operational status is unverified.
- Concessions: did not substantiate coverage of Tasks 7-10 (plan:88-122); accepted the submit-policy change too readily; its authorization must be resolved before choosing the test expectation.
- Shared assumptions: A-001 ACCEPT. A-002 QUALIFY (the helper requires an explicit level, orca_worktree.py:1873-1883; no proof of repository-wide absence of other default resolution). A-003 QUALIFY (explicit none and tests justify preserving the watcher, not that it is the sole guard). A-004 REJECT: a documented owner-run launch passes a bare claim prompt (docs/designs/issue-watcher-setup.md:616-619; orchestrator re-read: those rows give `<orca> agent launch ... --prompt '/sc:issue --claim <test issue>'` for fixture capture in the owner-run live test).

### Variant 3 Advocate (reviewer 3, refactorer, opus)
- Position: pass-with-findings stands; raises F6 (claim.md:142 text) from note to medium; keeps F1 (bare --submit) at medium as an owner decision.
- Steelman V1: right that claim.md:142 gives full a wrong instruction, right that the bare --submit change is drift; its F3 noticed a bare claim now runs under the full-level gate. Steelman V2: read literally, claim.md:142 prints "It stops at the plan boundary and waits; run the printed implement command" then the full sentence, so a person at the new default could start /sc:implement a second time; F2 right that no test pins the bare --submit behaviour.
- Claims: only card to find the architecture reference, worker-brief.txt:17-19, and flag.md:85.
- Weaknesses of others: V1 F3 changes no outcome: the gate already requires item 1 for a worktree claim (claim.md:133), so a bare claim needs the same preconditions under either default. V2's blocking grade: the defect already applies to every explicit `--pipeline full` claim today. V2 F2 accepts the looser rule without weighing flag.md:85.
- Concessions: C-2 rejection was shown without the comparison (the comparison holds); F5 and F6 should be tagged grounded; F6 should be medium, fix is one added scope edit in Task 4 so the "waits; run the printed implement command" sentence applies to worktree only.
- Shared assumptions: A-001 ACCEPT. A-002 ACCEPT (`--level` required, orca_worktree.py:1873,:1883; `--submit` refused unless full, :1900-1901). A-003 QUALIFY (code also rejects any prompt not of the `--pipeline none` form, launch.py:33; /sc:issue is never dispatched to workers, WORKER-CONTRACT.md:23). A-004 QUALIFY (in src/ and plugins/ the watcher is the only caller; docs not fully searched).

## Round 2: Rebuttals (sequential: V1, then V2, then V3; each saw the earlier answers)

### Variant 1 (reviewer 1)
- P1 claim.md:142: qualify (0.7). The text is ambiguous: the "For full" sentence follows the unconditional "It stops at the plan boundary and waits; run the printed implement command" and reads as an addition. Medium is right; Task 4 should make the "waits; run ..." sentence apply to worktree only.
- P2 bare --submit: agree (0.85). flag.md:85 lists "no --pipeline" as a STOP case; source.md:1 asks only for the default; narrower edit is to leave issue.md:57 as written. This also removes V2's test gap.
- P3 ship gate: WITHDRAWS F3 (0.8). issue.md:16 says "No governed claim (worktree or full) is used on a real issue until OB-H1 item 1, OB-H2 and OB-H3 have passed", so worktree is already under item 1; a bare claim faces the same gate before and after.
- P4 A-004: false as stated, small impact (0.75). issue-watcher-setup.md:616-619 shows four rows launching `/sc:issue --claim <test issue>` with no --pipeline (owner-run fixture capture); after the plan that launch starts at full, with no commit or push. Add --pipeline none to the rows or list them as out of scope.

### Variant 2 (reviewer 2)
- P1: downgrades blocking to medium (0.85). "For full" can reasonably replace the preceding message; restrict "waits; run..." to worktree; no observed failure supports blocking (claim.md:142).
- P2: WITHDRAWS its missing-test finding as written (0.95). If the rule stays, pin instead that a bare --submit stops and explicit full permits submission (issue.md:57); Task 7 wording must follow the preserved rule.
- P3: qualify (0.95). Tasks 7-9 have no wrong target line or dependency. Task 10 says "Stage only" the src/, tests/, docs/ and plugins/ side, which excludes the task package; CLAUDE.md:35-37 says .dev/tasks is always staged. Include task-package staging and an acceptance check.
- P4: qualify (0.9). The setup-doc rows are owner-run fixture capture, not another production caller, but they refute the universal assumption; record that their bare prompts inherit full, update them before reuse if capture must stay claim-only.

### Variant 3 (reviewer 3)
- P1: agree (0.85). Medium is the right common grade (the defect already affects every explicit full claim). Fix wording: in Task 4 make the "waits; run the printed implement command ..." sentence apply to worktree only; add one test that the full branch does not carry it.
- P2: CHANGED to a definite plan change (0.8). Keep the rule (flag.md:85). Task 3: drop the E-SUBMIT rewrite, keep issue.md:57 and the --submit row exactly, add "`--submit` still needs an explicit `--pipeline full`, even though `full` is the default." Task 4: leave SKILL.md:154 unchanged. Task 5: add a test that the rule text still says "without `--pipeline full`" and keeps the quoted message. Task 7: leave commands.md:371 unchanged.
- P3: agree (0.9). CLAUDE.md:37 ".dev/tasks/ is always staged"; plan Task 10 says "Stage only the src/, tests/, docs/ and plugins/ side", leaving the plan package out. Add .dev/tasks/.
- P4: qualify (0.8). Plan tasks: F2 (architecture reference :1557, :1635) into Task 7; F3 and F4 into Task 8 (name flag.md lines 66, 78, 87 and add a "superseded" line under the row at sc-issue-command.md:238, following :248). Recorded out of scope: F5 worker-brief.txt:17-19 (the spec names only refs/chains.md) and the owner test launch rows in issue-watcher-setup.md:616-619 (concedes its A-004 answer missed them).

## Round 2.5: Invariant probe
See invariant-probe.md. 10 findings, 0 HIGH unaddressed, 2 MEDIUM unaddressed (INV-002 coordinator-owned re-claim; INV-005 the kept E-SUBMIT wording becomes ambiguous once the default is stated). INV-005 corrects the Round 2 consensus: keeping the rule text verbatim is not enough.

## Scoring Matrix
| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| S-001 verdict spread | pass-with-findings before the probe; fail after (one blocking, grade by consequence) | 80% | V2 withdrew its blocking grade; the blocking finding is M1 (safety: commit, push, PR) |
| S-002 severity labels | common grade medium for claim.md:142 | 85% | V1 0.7, V2 0.85, V3 0.85 |
| C-001 claim.md:142 | restrict the sentence to worktree (V1, V3 wording) | 85% | three advocates agree |
| C-002 bare --submit | keep the rule and copy "or no --pipeline" (V3 plus probe INV-005) | 90% | flag.md:85; V1 0.85, V2 0.95, V3 0.8; INV-005 |
| C-003 ship gate | no finding (V3, V2) | 85% | V1 withdrew after re-reading issue.md:16 |
| C-004 missed sites | add to Tasks 7 and 8 (V3) | 80% | V1 conceded, V2 no objection |
| C-005 worker-brief | record out of scope (V3) | 75% | spec names only chains.md |
| C-006 test_launch.py | no edit (all) | 95% | already pinned (test_launch.py:932-939) |
| X-001 severity of claim.md:142 | medium | 85% | resolved |
| X-002 relaxation defect or consequence | defect, definite plan change (V3, V1) | 90% | resolved |
| X-003 ship gate attention | none | 85% | resolved |
| A-001 task order | ACCEPT | 90% | all three accept |
| A-002 Markdown-only default | ACCEPT with qualification | 85% | V3 accept; V1, V2 qualify; probe INV-004 confirms no code default |
| A-003 watcher guard | ACCEPT with qualification | 80% | V1 accept; V2, V3 qualify (code also rejects other prompts, launch.py:33) |
| A-004 no other bare caller | CONTRADICTED | 90% | issue-watcher-setup.md:616-619, confirmed by the orchestrator re-read; all three agree |

## Convergence Assessment
- Points resolved: 15 of 15
- Alignment: 100 percent (qualified on A-002 and A-003)
- Threshold: 80 percent
- Status: CONVERGED (taxonomy levels L1, L2, L3 all covered; no HIGH unaddressed invariant)
- Unresolved points: none
- Caution: two of the three advocates moved toward V3 after reading the same evidence; the move was driven by a checked line (flag.md:85) and not by repeated assertion, and the probe then found a flaw in the consensus (INV-005).
