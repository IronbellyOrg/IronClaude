# Merge Execution Log

## Metadata
- Base: Variant 1 (OURS), /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG3/adversarial/adversarial/variant-1-original.md
- Executor: merge-executor agent
- Changes applied: 8 of 8 (Change 5 applied in part: fact 10 added, the fact 6 sub-edit skipped, see Change 5)
- Status: partial (one sub-edit of Change 5 skipped, nothing else failed)
- Timestamp: 2026-11-20
- Output: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG3/adversarial/merged-output.md

## Changes Applied

### Change 1: Stage the default-on claim behind a key that ships false
- Status: Applied
- Source: Variant 2 (CLAY), Claim and Mechanism step 2; C-001, C-005, U-008, U-009
- Target: Claim, OA-28a paragraph (replace)
- Before: "OA-28a: a new repo that passes `first_run`'s six checks switches itself on. ... A staging key may hold it off until the single throwaway run has proved the chain, but after that one owner go the default for every later repo is on, with no per-repo go."
- After: "OA-28a: staged default-on. The `auto_enable` defaults key ships false, so no config is switched on before the S17 throwaway run. After S17 passes, the owner turns the key on once in the defaults file (one recorded chat go). From then on a new repo that passes `first_run`'s six checks switches itself on with no per-repo go. The end state is on because the owner's recorded line (REQ R17, R18) is that nothing in setup is manual."
- Provenance tag: Source: Variant 2 (CLAY), Claim and Mechanism step 2 - merged per Change #1; zero-setup rationale from Base (original)
- Validation: Plan's required elements all present (key ships false, nothing on before S17, one flip with one recorded chat go, no per-repo go afterwards, R17/R18 rationale kept). Base's R18 citation widened to "R17, R18" as the plan states.

### Change 2: Define what "passed" means for the S17 run
- Status: Applied
- Source: Shared assumption A-001
- Target: Mechanism, new step 6 (insert after step 5)
- Before: Mechanism ended at step 5.
- After: Step 6 "S17 passes when the six `first_run` checks are green on the throwaway repo, a `run-all --dry-run` shadow run has generated nothing and written nothing, the X-001 live check has been run, and the owner has said go in chat; this list is a proposal, not a recorded owner rule (UNVERIFIED)."
- Provenance tag: Source: Variant 2 (CLAY), shared assumption A-001 - merged per Change #2
- Validation: Text copied as planned; UNVERIFIED and proposal labels kept.

### Change 3: Make the label write consistent with the owner's go (resolves X-002)
- Status: Applied
- Source: Variant 2 (CLAY), Claim OA-28b and fact 1; X-002, C-006
- Target: Claim OA-28b paragraph and Costs bullet 1 (replace)
- Before (Claim): "NG-2 ... governs the poll cycle (`issue-watch once`). Per-repo init may create the trigger label once and `hold:backlog` once, behind the owner's chat OK before the first real run. Setup is not the poll."
- After (Claim): "NG-2 (...) covers the poll cycle only (`issue-watch once`). Init creates the trigger label once, and only after the owner's go that turns `auto_enable` on. Setup is not the poll."
- Before (Costs bullet 1): "... a label is created on GitHub without a fresh chat go."
- After (Costs bullet 1): "... a label is created on GitHub without a per-repo chat go, under the class-level go given when the key is turned on."
- Provenance tag: Source: Variant 2 (CLAY), Claim OA-28b and fact 1 - merged per Change #3 (both places)
- Validation: The plan's kept phrase lists only the trigger label, so the base's "and `hold:backlog` once" was not carried into the Claim; this matches Change 8 (hold:backlog is outside this decision). Contradiction X-002 resolved, see Post-Merge Validation.

### Change 4: Label step is read-only while the key is false
- Status: Applied
- Source: Variant 2 (CLAY), Mechanism step 3; C-006
- Target: Mechanism step 4 (append)
- Before: Step 4 ended "... so the code already splits cycle from init."
- After: Appended "With the key false the label step only calls `trigger_label_state` and reports `would_create`; it neither creates the label nor fails the check. With the key true it calls `ensure_trigger_label`. The `would_create` result is a design proposal, not existing code (UNVERIFIED against code)."
- Provenance tag: Source: Base (original, modified) - appended per Change #4; Variant 2 (CLAY), Mechanism step 3
- Validation: Proposal label present; no code claim added.

### Change 5: Add the widened NG-2 test as fact 10; fix fact 6
- Status: Applied in part
- Source: Debate transcript, Advocate 2 concession X-003; `tests/issue_watch/test_security_invariants.py:1059-1079`
- Target: Cited facts, new fact 10 (append); fact 6 second sentence (replace)
- Before: Facts ended at 9.
- After: Fact 10 added as planned ("The planb test `test_only_complete_and_repo_init_may_write_to_github` already permits ... The owner's own tests already read NG-2 as 'the cycle writes nothing'.").
- Skipped sub-edit: the "fix fact 6's second sentence (replace)" part. The plan names no replacement text and says fact 6's mention of lines 652 and 683 stays, so there was nothing specified to write. Fact 6 is left as in the base. The orchestrator may supply replacement text if one was intended.
- Provenance tag: Source: Variant 2 (CLAY) debate evidence, concession X-003 - merged per Change #5
- Validation: Fact numbers 1 to 9 unchanged; fact 10 follows 9 with no gap.

### Change 6: Add the unrun live check and the unproved claim route as preconditions
- Status: Applied
- Source: Variant 2 (CLAY), facts 6-8; U-007, X-001, C-003
- Target: Risks, second bullet (append)
- Before: Second bullet (Coder issue 516) ended "... not an unsafe launch."
- After: Appended "The layered brake is not proved until S17: the X-001 live check (claim agents share one `Coordinator` worktree) has not been run, and INV-025 means the guard reads command text only. So the staged `auto_enable` key stays false until S17."
- Wording adaptation: the plan text says "the staged key in Change 1"; "Change 1" is a plan label that does not exist in the merged document, so it was written as "the staged `auto_enable` key" to avoid a dangling reference.
- Observation: the plan targets the second bullet (the 516 bullet) although INV-025 is first mentioned in the first bullet. Applied where the plan says.
- Provenance tag: Source: Base (original, modified) - appended per Change #6; Variant 2 (CLAY), facts 6-8, U-007, X-001, C-003
- Validation: Consistent with Claim (key false until S17).

### Change 7: Owner-visible report of self-enabled repos
- Status: Applied
- Source: Shared assumption A-004
- Target: Mechanism, new step 7 (insert after step 6)
- Before: No such step.
- After: Step 7 "When the key is on, each repo that switches itself on is listed in the owner's session report (proposal; the mechanism for telling the owner is not built and not part of this decision)."
- Provenance tag: Source: Variant 2 (CLAY), shared assumption A-004 - merged per Change #7
- Validation: Proposal label present.

### Change 8: hold:backlog out of this decision, and cite symbols
- Status: Applied
- Source: C-004, A-005
- Target: Costs bullet 3 (replace); Mechanism closing note (append)
- Before (Costs bullet 3): "`hold:backlog` creation is not built in planb: `ensure_trigger_label` creates only the trigger label (planb `first_run.py:193`). D09 rule 2 and K18 expect both, so a small addition is needed."
- After (Costs bullet 3): "`hold:backlog` creation is not built in planb; it stays by hand (Clay design D:445) until the owner asks for it, and is outside this decision."
- After (closing note): "Line numbers cite the planb head d0a0a433b; after the rebase cite the symbols (`ensure_config`, `first_run`, `ensure_trigger_label`, `trigger_label_state`) and re-verify."
- Provenance tag: Source: Variant 2 (CLAY), C-004 and A-005 - merged per Change #8 (both places)
- Validation: The `first_run.py:193` citation was removed by the replacement, as the plan's text specifies.

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: PASS. One H1, six H2 (Claim, Mechanism, Cited facts, Costs, Risks, What it gets right); no H3 and no gaps.
- Section ordering: PASS. Same order as the base.
- Document flow: PASS. Mechanism list runs 1 to 7 with the closing note after step 7; Cited facts run 1 to 10; provenance comments are the first three lines; every section and block carries a Source tag.
- Em dash check: PASS. No em or en dash in the merged file.

### Internal References
- Total: 0 in-body "fact N" or "step N" references (the only such wording is inside provenance comments and refers to Variant 2 sections, not to merged-file items).
- Resolved: 0 (none needed)
- Broken: 0. The one reference that would have broken ("Change 1" in Change 6 text) was reworded, see Change 6.
- Numbers, paths and line citations: every one appears in the base or the plan (for example `test_security_invariants.py:1059-1079`, "Clay design D:445", d0a0a433b, X-001, INV-025).

### Contradiction Re-Scan
- New contradictions introduced: none.
- X-002 (Claim vs Costs on the owner's chat go): resolved. Claim says init creates the label only after the owner's go that turns `auto_enable` on. Costs bullet 1 says the label is created without a per-repo go, under the class-level go given when the key is turned on. Mechanism step 4 says the label step is read-only while the key is false. Risks and step 6 agree the key stays false until S17. No sentence says the label write is made without the owner's go, and none says it needs a per-repo go.
- Residual note (not a contradiction): Mechanism step 3 and fact 4 describe planb as read (`enabled: true` is written when all six checks pass, with no key). The `auto_enable` key is the proposed change to that behaviour (the plan states `first_run.py` has no key today); the merged text does not say the key already exists.

## Summary
- Planned: 8
- Applied: 8 (Change 5 in part)
- Failed: 0
- Skipped: 1 sub-edit (Change 5, fact 6 sentence fix: the plan gives no replacement text)
- Post-merge validation: PASS
