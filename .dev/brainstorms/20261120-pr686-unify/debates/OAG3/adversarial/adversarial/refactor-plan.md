# Refactoring Plan: Merge into Base (Variant 1, OURS)

Base file: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG3/adversarial/adversarial/variant-1-original.md`
Other variant: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG3/adversarial/adversarial/variant-2-original.md`
Section references below use the base's H2 headings: Claim, Mechanism, Cited facts (numbered 1-9), Costs, Risks, What it gets right.

## Overview
- Base: Variant 1 (OURS)
- Incorporating strengths from: Variant 2 (CLAY)
- Planned changes: 8
- Risk level: Medium overall (changes 1 and 3 alter the base's headline claim; the rest are additive)
- Output rule: the merged file must keep the base's section list and may not add a fact that has no source in either variant, in the debate transcript or in the code reads recorded there.

## Planned Changes

### Change 1: Stage the default-on claim behind a key that ships false (from Variant 2)
- **Source**: Variant 2, Claim and Mechanism step 2; diff points C-001, C-005, U-008, U-009
- **Target**: Base, Claim (OA-28a paragraph) (replace)
- **Rationale**: C-001 landed on HYBRID at 60% in both advocates' tables; C-005 resolves under it. `first_run.py` has no key today (`_enable` runs unconditionally on a pass), MR line 416 says no config is switched on before S17, MR line 353 lists the key as NOT BUILT.
- **Integration point**: Replace the OA-28a sentence with: the `auto_enable` defaults key ships false; no config is switched on before the S17 throwaway run; after S17 passes, the owner turns the key on once in the defaults file (one recorded chat go); from then on a repo that passes the six checks switches itself on with no per-repo go. Keep the base's zero-setup rationale (R17, R18) as the reason the end state is on.
- **Risk**: Medium - it changes the paper's headline from "default-on" to "staged default-on", which is the debate's HYBRID.

### Change 2: Define what "passed" means for the S17 run (from both advocates)
- **Source**: Shared assumption A-001 (both advocates QUALIFY)
- **Target**: Base, Mechanism, new step 6 (insert)
- **Rationale**: A-001 HYBRID at 70%: neither paper defines pass criteria. Advocate 1 proposed: the six first-run checks green, the X-001 live check, a recorded owner go. Advocate 2 proposed: six checks, one shadow `run-all --dry-run`, at least one real poll cycle with a recorded owner go. The plan merges them as the union and marks the list as a proposal.
- **Integration point**: New Mechanism step: "S17 passes when the six `first_run` checks are green on the throwaway repo, a `run-all --dry-run` shadow run has generated nothing and written nothing, the X-001 live check has been run, and the owner has said go in chat; this list is a proposal, not a recorded owner rule (UNVERIFIED)."
- **Risk**: Low - additive.

### Change 3: Make the label write consistent with the owner's go (resolves X-002) (from Variant 2)
- **Source**: Variant 2, Claim OA-28b and fact 1; diff points X-002 (V2 wins at 85%), C-006 (V2 wins at 62%)
- **Target**: Base, Claim (OA-28b paragraph) and Costs (first bullet) (replace)
- **Rationale**: Both advocates agree the Claim ("behind the owner's chat OK before the first real run") contradicts the Costs ("without a fresh chat go"). MR lines 91 and 361 require the owner's chat OK for the label write. The consistent reading: the owner's go at the S17 flip is a class-level go for the label creation of later repos; before that go, with the key false, `first_run` does not create the label.
- **Integration point**: Claim OA-28b: keep "NG-2 covers the poll cycle only; init creates the trigger label once" and add "and only after the owner's go that turns `auto_enable` on". Costs bullet 1: replace "without a fresh chat go" with "without a per-repo chat go, under the class-level go given when the key is turned on".
- **Risk**: Medium - touches the base's two key sentences; keeps its position.

### Change 4: Label step is read-only while the key is false (from Variant 2)
- **Source**: Variant 2, Mechanism step 3; diff point C-006; Advocate 2's concession that a read-only label step stays red until the label exists
- **Target**: Base, Mechanism step 4 (append)
- **Rationale**: C-006 V2 at 62%. To avoid the red-check problem, the read-only label step must report `would_create` as a non-failing result while the key is false; the repo still stays off because the key is false.
- **Integration point**: Append to step 4: "With the key false the label step only calls `trigger_label_state` and reports `would_create`; it neither creates the label nor fails the check. With the key true it calls `ensure_trigger_label`." Mark the `would_create` result as a design proposal, not existing code (UNVERIFIED against code).
- **Risk**: Low - additive, no existing code claim.

### Change 5: Add the widened NG-2 test as fact 6's evidence (from the debate)
- **Source**: Debate transcript, Advocate 2 strength and concession X-003; orchestrator verified `tests/issue_watch/test_security_invariants.py:1059-1079` in planb (`_WRITER_MODULES = {"complete.py", "repo_init.py"}`, `_WRITE_SIGN` includes `"label", "create"`, `github.py` and `cycle.py` must stay clean)
- **Target**: Base, Cited facts, new fact 10 (append); also fix fact 6's second sentence (replace)
- **Rationale**: C-002 V1 at 82%; X-003 V1 at 88%. This is the strongest single piece of evidence for OA-28b and the base does not cite it. Fact 6's mention of lines 652 and 683 stays, because those scan the cycle.
- **Integration point**: New fact 10: "The planb test `test_only_complete_and_repo_init_may_write_to_github` already permits `complete.py` and `repo_init.py` as the only writers and keeps `github.py` and `cycle.py` read-only (`test_security_invariants.py:1059-1079`). The owner's own tests already read NG-2 as 'the cycle writes nothing'."
- **Risk**: Low - additive and verified.

### Change 6: Add the unrun live check and the unproved claim route as preconditions (from Variant 2)
- **Source**: Variant 2, facts 6-8; U-007, X-001, C-003
- **Target**: Base, Risks (second bullet) (append)
- **Rationale**: Both advocates accept that INV-025 and the unrun X-001 check are real residual risk. C-003 and X-001 stay unresolved but lean V1; the plan keeps the base's layered-brake claim and adds the caveat.
- **Integration point**: Append: "The layered brake is not proved until S17: the X-001 live check (claim agents share one `Coordinator` worktree) has not been run, and INV-025 means the guard reads command text only. So the staged key in Change 1 stays false until S17."
- **Risk**: Low - additive.

### Change 7: Owner-visible report of self-enabled repos (from both advocates)
- **Source**: Shared assumption A-004 (both QUALIFY)
- **Target**: Base, Mechanism, new step 7 (insert)
- **Rationale**: A-004 HYBRID at 62%: reversal is cheap only if the owner sees which repos switched themselves on; `first-run.txt` is written either way but nobody is told.
- **Integration point**: New step: "When the key is on, each repo that switches itself on is listed in the owner's session report (proposal; the mechanism for telling the owner is not built and not part of this decision)."
- **Risk**: Low - additive, labelled as a proposal.

### Change 8: State that `hold:backlog` creation is not part of this decision, and cite symbols (from both advocates)
- **Source**: C-004 (unresolved, leans V2 or HYBRID at 55%); A-005 (HYBRID at 72%)
- **Target**: Base, Costs (third bullet) (replace) and Mechanism (new closing note) (append)
- **Rationale**: Planb creates only the trigger label (`first_run.py:193`); `hold:backlog` creation is not built (U-005); Clay's design creates it by hand (D:445). Line numbers from planb will drift after the rebase (MR line 501).
- **Integration point**: Costs bullet 3: "`hold:backlog` creation is not built in planb; it stays by hand (Clay design D:445) until the owner asks for it, and is outside this decision." Closing note under Mechanism: "Line numbers cite the planb head d0a0a433b; after the rebase cite the symbols (`ensure_config`, `first_run`, `ensure_trigger_label`, `trigger_label_state`) and re-verify."
- **Risk**: Low - clarifying.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| C-001 (per-repo go forever) | A recorded owner go for every repo, permanently | The debate landed on a HYBRID: key false until S17, then one flip. A permanent per-repo go breaks R17 and R18 after repo 1 (C-007, V1 at 68%; Advocate 2's own Risks section says zero setup becomes "not zero") |
| C-002 (strict NG-2) | No GitHub write anywhere in setup; labels by hand | Advocate 2 conceded: the planb NG-2 test already permits `repo_init.py` (`test_security_invariants.py:1059-1079`) and the read/write split exists in `repo_init.py:93-117`; V1 at 82% |
| C-004 (labels by hand) | `first_run` only checks labels; the owner creates them | Unresolved. Not adopted for the trigger label, because the owner's R17 says nothing manual and the creation is idempotent and reversible; adopted for `hold:backlog` only by omission (Change 8) |
| X-003 (tests encode flat NG-2) | Pinned tests make a setup write a breach | Refuted: those tests scan the cycle; V2 conceded (88%) |
| X-004 (D:1125 as a switch-on rule) | Clay's "name each repo" rule applies to production switch-on | Refuted: the sentence governs live tests of PR B in throwaway repos; V2 conceded (88%) |
| S-003 (evidence organization) | Evidence grounded in requirement rows | Unresolved, leans V1 (55%); the base's code-grounded facts stay, requirement-row facts are cited where Change 1 uses them |
| A-003 (registration signals intent) | Registration alone does not signal intent | Unresolved, leans V1 (62%); the owner filter and generation filters stay as the bound, no change made |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Medium | The headline claim misstates the debate result | Restore the original Claim paragraph from the base |
| 2 | Low | A proposed pass list is mistaken for an owner rule | Delete the inserted step |
| 3 | Medium | Claim and Costs become inconsistent again | Restore the two original sentences |
| 4 | Low | A design proposal is mistaken for code | Delete the appended sentence |
| 5 | Low | A wrong test citation | Delete fact 10 |
| 6 | Low | None; additive caveat | Delete the appended sentence |
| 7 | Low | A proposal is mistaken for a built feature | Delete the inserted step |
| 8 | Low | None; clarifying | Restore the original Costs bullet |

## Review Status
- [x] Auto-approved (default; `--interactive` not set, `--unattended` refuses person-mode flags)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-20
