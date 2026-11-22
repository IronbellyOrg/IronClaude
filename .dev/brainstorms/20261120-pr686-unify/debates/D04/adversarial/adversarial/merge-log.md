# Merge Execution Log (D04 claim level and grants)

## Metadata
- Base variant: Variant A (OURS), `variant-1-original.md`
- Non-base variant: Variant B (CLAY), `variant-2-original.md`
- Refactoring plan: `refactor-plan.md` (9 changes, applied in order)
- Merge date: 2026-11-20
- Output: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D04/adversarial/merged-output.md`
- Sources used for facts and citations: the two variants, `debate-transcript.md`, `invariant-probe.md`, `base-selection.md`, `diff-analysis.md`, `refactor-plan.md`. No master snapshot or repository file was re-read, so every `D:N`, line number and PR or issue reference is copied as written in those files, not re-verified here.
- Form: the merged output is a unified position (the debate's resolved answer), not a third advocate paper, as the plan's Overview says. The base sections "Cited facts", "What it costs", "What it risks" and "What it gets right" are therefore not reproduced as such. Their surviving content sits in Claim, Mechanism, Grants, Flag semantics, Corrected facts and Conditions.

## Changes Applied

### Change 1: Live rule is a none-only claim
- Status: Applied
- Source: Variant B Claim and Cited fact 1; debate Round 2 (both advocates); C-001, C-004
- Target: Claim (replaced)
- Before (base): "The person who owns the issue decides, per issue, how far automation goes... The watcher reads it and the coordinator launches the claim at that level... The Pipeline field is the owner's only per-issue throttle..."
- After: the watcher or orchestrator claims only at `--pipeline none` and starts one supervised `worker-start` worker; the Pipeline field is not read while governed levels are not allowed; test is `PROMPT_PATTERN` (`launch.py:33`) and `commands/issue.md:48`. The Pipeline field stays named as the gate-open selector (R25, line 51), a later owner decision that amends R9 and the K4 test together.
- Provenance tag: `Base (original, modified): Claim replaced per Change 1`
- Validation: the new Claim does not contradict Flag semantics (the watcher always passes `--pipeline none`; other levels only after the gate opens). The base's "only per-issue throttle" sentence is gone (see Change 6, C-005).

### Change 2: One supervised route
- Status: Applied
- Source: Variant B Mechanism 1 and 2; Cited fact 3; C-002
- Target: Mechanism items 1 and 2 (new)
- Before: base Mechanism had no claim-then-`worker-start` item; the base Mechanism 1 mapped board values to flags.
- After: item 1 (wave 1 claim at none, D:544) and item 2 (`worker-start`, Run mailbox, one message handled once per id, K4 at D:1226 as a gate-independent reason). The base flag mapping moved to the "Flag semantics" section (Change 7).
- Provenance tag: `Base (original, modified): Mechanism rebuilt ... items 1 and 2 merged from Variant B Mechanism 1 and 2 per Change 2`
- Validation: item order is claim, route, controls, gate wording. C-002 (whether a second route is ever wanted) is left open and listed in Open points, as the plan requires. A sentence on C-002 inside Mechanism was cut for length; the point survives only in Open points.

### Change 3: Grants split, four standing and two per PR
- Status: Applied, with one deviation
- Source: Variant B Mechanism 3 (list); Variant A Cited fact 6 and Decision 8; Round 2 answers (c) and (d) of both advocates; C-006, C-007
- Target: Claim last sentence and base Mechanism 4 (replaced)
- Before: "Every outward write the coordinator makes for an issue needs that issue's own grant row" and Mechanism 4 (coordinator writes only under that issue's grant row, Decision 8, owner-answers line 130).
- After: a new "Grants" section. Four standing entries (`issue.assign`, `issue.comment`, `issue.body.append_plan_sections`, `issue.hold`); `pr.merge` and `issue.close` not standing, with contract lines 241, 245, 300, R10 (D:71), ADD1 (D:135) and Q38 (owner-answers line 187); release per PR and head sha by a chat-recorded go accepted by an `answer-check`-style verb with the owner identity as a parameter; key `merge_safety:<PR>:<head sha>` (D:598).
- Deviation: the plan asked for the grants sentence to sit at the end of Claim. A one-line pointer there was cut while trimming to the word target, so the grants split now appears only in the Grants section.
- Provenance tag: `Variant B Mechanism 3 (grants list) merged per Change 3, split using Variant A Cited fact 6 ...`
- Validation: "six entries" is now attributed to Clay's design (D:291, D:872) and "four standing" to this position, so it does not contradict the INV-006 count of 2 of 6. The per-issue file row written by the owner is dropped, in line with the owner's chat-only order of 2026-11-17 (A conceded in Round 2 (d)).

### Change 4: Controls adopted, scoped to what they cover
- Status: Applied
- Source: Variant B Mechanism 3, 4, 5; Cited fact 7; C-008
- Target: Mechanism item 3 (new)
- After: `answer-check` (D:688, N1 at D:758), `E-NO-GRANT` limited to the orchestrator's own verbs and at most 2 of 6 entries (D:696), closed "may do" list and `refuse(argv)` (5.9, D:736). States they limit the orchestrator, not the worker. The four conditions of Change 8 sit in their own section.
- Provenance tag: `... item 3 merged from Variant B Mechanism 3, 4, 5 per Change 4 and scoped to what the controls cover`
- Validation: the claim "E-NO-GRANT refuses a write outside the list" from Variant B is narrowed as D:696 requires. Variant B Cited fact 7's "one test row per pattern" detail (D:1111, D:1117) was cut for length except the `refuse(argv)` reference in INV-003.

### Change 5: Gate wording keyed to what master has
- Status: Applied
- Source: Round 2 answers (a) of both advocates; INV-001
- Target: Mechanism item 4 (replaced base Mechanism 5)
- Before: "`GOVERNED_LEVELS_ALLOWED = False` (`launch.py:48`, branch `ironbelly/issue-watcher-zero-setup-plan`; R33, requirements.md line 59). Only Pipeline None launches until a reviewed commit flips it."
- After: the orchestrator launches only through `worker-start`; the watcher prompt stays pinned to `--pipeline none` (`launch.py:33`); any governed level waits for the 12 skipped observations, open issue 442 and an owner decision; the spec must not key to `GOVERNED_LEVELS_ALLOWED` because master does not have it (INV-001).
- Source conflict, resolved: the base names branch `ironbelly/issue-watcher-zero-setup-plan` for `launch.py:48`; the probe (INV-001) says the constant exists only in the unpushed worktree `claim-handoff-planb`. I followed the probe and the plan, and dropped the branch name from the merged text. The two statements were not reconciled against the repository.
- Provenance tag: `item 4 replaces base Mechanism 5 per Change 5`
- Validation: Claim, Mechanism item 4 and INV-001 in Conditions say the same thing.

### Change 6: Corrections to base facts
- Status: Applied
- Source: Round 1 and 2 concessions (X-002, X-003, C-005)
- Target: base Cited facts 3 and 4, Costs bullets 2 and 5 (edited in place, then collected in "Corrected facts")
- After: X-002 "the only control that is built"; X-003 Q36 (owner-answers line 185) is approval latency, Decision 8 (line 130) is the grant row, "accepted for now" claim removed; C-005 other brakes (`enabled` D:278 and D:302, `max_in_flight` D:289, gate reasons D:582) exist but none is a per-issue stop after the claim; `hold:backlog` (D:445) stops only the claim wave.
- Note: Costs bullet 5 (grant row written as a file versus the chat-only rule) is handled through the Grants release rule, not through a separate correction line.
- Provenance tag: `Base (original, modified): Cited facts 3 and 4 and Costs bullets 2 and 5 corrected per Change 6`
- Validation: no remaining text calls the Pipeline field the only per-issue throttle or says "the control that exists today".

### Change 7: Flag semantics kept
- Status: Partial
- Source: base Mechanism 1 to 3; `docs/designs/sc-issue-claim-pipeline-flag.md` lines 69-89 (as cited by the plan)
- Target: new "Flag semantics of `/sc:issue --claim`" section
- Kept: board value to flag mapping (None, Worktree, Full, Full Submit), empty Pipeline means None (R25, line 51), `--submit` only with `--pipeline full`, STOP names `E-SUBMIT-NEEDS-FULL` and `E-CLAIM-ONLY-FLAG`, the watcher always passes `--pipeline none`, level state outside the worktree with `W-ENFORCEMENT-ABSENT`, the Full Submit push rule (Pipeline plus `Approved`), no level merges.
- Not applied: the `--plan` STOP row "from D:1065". The text of D:1065 is not quoted in any of the files I was given, so adding it would have been invention. Escalate to the orchestrator if it is required.
- Limits on the STOP names: `E-SUBMIT-NEEDS-FULL` and `E-CLAIM-ONLY-FLAG` come from the executor brief, not from the variants. The variants do not state what triggers `E-CLAIM-ONLY-FLAG`, so the merged text only names it and points to the flag design lines 69-89. Pairing `E-SUBMIT-NEEDS-FULL` with "`--submit` only with `--pipeline full`" is my reading of the brief and `base-selection.md` (Strengths to Preserve 1).
- Dropped for length: the references to PR 425 and PR 441 (built flags and L2 pre-push layer).
- Provenance tag: `Base (original): Mechanism 1 ... kept per Change 7`
- Validation: the section matches the base wording on the points kept.

### Change 8: Conditions from the invariant probe
- Status: Applied
- Source: invariant-probe.md
- Target: new section "Conditions the spec must state"
- After: HIGH items INV-001, INV-002, INV-003, INV-004, INV-012; MEDIUM warnings INV-005, INV-006, INV-009, INV-010. The plan listed INV-005, INV-009 and INV-010 but not INV-006; INV-006 was added because the brief names it.
- Provenance tag: `Variant B Cited fact 7 and Round 2.5 invariant probe ..., merged per Change 8 as a new section`
- Validation: each item keeps its probe citation (D:688, D:300, D:117, D:1117, D:135, D:588, D:696, D:598, D:582, `owner-answers.md:162`, D:694, D:1109, D:445, R36 `requirements.md:62`). The probe row INV-010 also cites D:575; that mention was cut for length.

### Change 9: Open points
- Status: Applied
- Source: debate-transcript.md (unresolved), diff-analysis.md (A-001, A-003)
- Target: new final section "Open points"
- After: C-001 and X-001 (one row), C-002, A-001, A-003 with who must decide, plus the R10 confirmation for `ironbelly`.
- Who-decides wording: C-001/X-001 "repository owner, probably D01", A-001 "topic D01", A-003 "owner, with D06 and D16" are taken from the transcript and diff-analysis. For C-002 the sources only say it is unresolved; "the owner, at the gate-open decision" is my wording based on Round 2 (B contest 3), not a source quote.
- Provenance tag: `Base (original, modified): new final section per Change 9`
- Validation: non-convergence (78.9%) is stated in the Status line.

## Post-Merge Validation

### Structural integrity: PASS
- One H1, seven H2 (Claim, Mechanism, Grants, Flag semantics of `/sc:issue --claim`, Corrected facts, Conditions the spec must state, Open points). No skipped heading levels (checked by listing every heading line).
- Three header comments present. Eight `<!-- Source: ... -->` tags, one per content block (title and status block plus seven sections). No stub marker left (grep count 0).
- No em or en dashes (grep count 0). No non-ASCII characters on the first check.
- Length: 1338 words by `wc -w` on the file with comment lines removed. That counts table separators, so it is a little over the "about 1300" target; I did not cut further.
- "Changes not made" is not in the merged document; it stays in `refactor-plan.md`.

### Internal references: PASS with two notes
- Every `INV-` id in the text (001, 002, 003, 004, 005, 006, 009, 010, 012) appears in Conditions; the cross-reference in Mechanism item 4 (INV-001) resolves. The "see Grants" pointer was removed in trimming, so no dangling pointer remains (grep for "see " is empty).
- Every diff-point id used (C-001, C-002, X-001, A-001, A-003 in Open points; C-005, X-002, X-003 in Corrected facts) is defined where it appears.
- Note 1: external citations (`D:N`, `owner-answers` lines, `requirements.md` lines, contract lines) were not re-opened. I checked only that each one appears in the source files given to me.
- Note 2: first-mention rule for numbers. Issue 442 and issue 394 each carry a few words saying what they are. PR 425 and PR 441 were removed. The `D01`, `D06`, `D16` ids are debate topic ids, labelled "topic".

### Contradiction re-scan: PASS, with items to watch
- Claim ("Pipeline not read now") against Flag semantics (levels run only after the gate opens): consistent.
- Grants ("six entries" in Clay's design, four standing here) against INV-006 ("2 of 6"): consistent after the wording fix above.
- Controls adopted (`answer-check`) against INV-002 (the list sits in a file the orchestrator can edit): consistent; one adopts, the other states the residual weakness.
- Mechanism item 2 (K4 is a gate-independent reason) against Claim (gate-open decision amends the K4 test): not a contradiction, but it is the same tension as open point C-002 and is left open on purpose.
- Mechanism item 4 (do not key to `GOVERNED_LEVELS_ALLOWED`) against Variant A Round 2 answer (a) (key to the gate): this is the resolution the plan chose (Change 5); a reader of the debate transcript will see A's earlier wording as superseded.
- No new contradiction found.

## Summary
- Changes applied: 8 (1, 2, 3, 4, 5, 6, 8, 9). Applied with a noted deviation: Change 3. Partial: Change 7 (the `--plan` STOP row from D:1065 was not added). Failed: 0. Skipped: 0.
- Items for the orchestrator: (1) D:1065 text needed for the `--plan` STOP row; (2) the branch-name conflict for `launch.py:48` between the base and INV-001; (3) the exact trigger text of `E-CLAIM-ONLY-FLAG`; (4) word count 1338 versus the "about 1300" target.
- Files written: `merged-output.md` (new) and this `merge-log.md` (filled).
