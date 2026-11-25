# Merge Execution Log

## Metadata
- Base: Variant A (OURS), `variant-1-original.md`
- Executor: merge-executor agent
- Changes applied: 9 of 9
- Status: success
- Timestamp: 2026-11-20
- Output: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D06/adversarial/merged-output.md`
- Method: both outputs were created as stubs and filled section by section. The unchanged base content was filled first, then Changes 1 to 9 were applied as edits in plan order.

## Changes Applied

### Change 1: Merge procedure with a read-only gate
- **Status**: Applied
- **Source**: Variant B, "The mechanism" items 1 to 3, cited facts 1 and 9; Round 2 B hybrid gaps (go window, restart)
- **Target**: new H2 "Merge procedure" (intro) and H3 "Steps" (steps 1 to 6), after "The mechanism"
- **Before**: no merge procedure in the base; the base only said the person gives a go for each merge
- **After**: an intro that labels the gate "a requirement for a later build, not a present control" and "not shown to pass"; six steps: run the gate read-only, show the output, the person types a go, re-run the gate before the merge and refuse on any changed reason, thread, review, base or draft state, `gh pr merge ... --match-head-commit <sha>` (never `--auto`, `--admin`, `--delete-branch`; the pin covers only the head sha), read back PR state (read first after a restart). States that a passing gate never triggers a merge.
- **Provenance tag**: `<!-- Source: Variant B (CLAY), The mechanism items 1 to 3, Cited fact 1 and Cited fact 9 - merged per Change #1 -->` and `... items 1 to 3 - merged per Change #1 -->`
- **Validation**: structural integrity OK (H2 with H3 children, ordered after "The mechanism"); references OK ("The go: contents, expiry and reach" resolves); contradictions none (the person's go is step 3, before the merge call in step 5)

### Change 2: What a go is, how long it lives, what it may override
- **Status**: Applied (with one limit, see Note)
- **Source**: Round 2 A "Updated assessment", Round 2 B "Hybrid gaps", probe INV-002, INV-004, INV-006
- **Target**: new H3 subsections "The go: contents, expiry and reach", "Gate reasons and what a go may override", "Windows" under "Merge procedure"
- **Before**: nothing on the contents, expiry or reach of a go
- **After**: the go names repo, PR, full 40-character head sha, merge method (checked against `merge_method` or `release_merge_method`), the word "merge" and the gate output; typed in live chat after the gate output; recorded as an entry (repo, PR, sha, time); one-shot, not a grant; stated expiry whose number is marked "Owner DECISION" (no source gives it); void on any head change or new gate reason. One table of gate reasons with a "Go may override?" column: `head_moved`, `draft`, `not_mergeable`, `snapshot_incomplete`, `changes_requested` never; `merge_safety` and `checks_failing` only by a go carrying that reason's own question key; `review_stalled` and `review_none_present` not overridable. `changes_requested` hard refusal is stated as the recommended rule and marked "Owner DECISION". Windows: the 2-minute window runs gate-to-merge (second gate run), the 60-minute hold runs from the final head's checks finishing (default, UNVERIFIED, "Owner DECISION"), the loop's silence timeout is a different clock.
- **Provenance tag**: `<!-- Source: Variant B (CLAY), Round 2 rebuttal "Hybrid gaps" and Variant A Round 2 "Updated assessment", with probe INV-002, INV-004, INV-006 - merged per Change #2 -->` (and two more tags for the table and Windows)
- **Validation**: structural integrity OK; references OK; contradictions none
- **Note**: the plan asks for "the 13 gate reasons". The inputs name only nine (`checks_failing`, `review_stalled`, `changes_requested`, `merge_safety`, `head_moved` from Variant B; `draft`, `not_mergeable`, `snapshot_incomplete`, `review_none_present` from the plan). No source names the other four, and the rules forbid adding facts. The table therefore lists the nine named reasons plus one row for "the other four", which says each needs a row before the gate is built and none is overridable until then (this follows the plan's rollback line, "make every reason non-overridable except by its own key"). The owner or orchestrator may want to fill in the four names from D:578-583.

### Change 3: Merge-time reviewer hold with a final-head re-trigger
- **Status**: Applied
- **Source**: Variant B cited facts 2 to 4; Round 1 A-001; Round 2 A item 2; probe INV-005, INV-007, INV-008, INV-009, INV-012
- **Target**: new H2 "Silent reviewer"; the loop's skip rule stays as written in the base (mechanism item 4 unchanged)
- **Before**: no merge-time check; the base conceded "OURS has no separate merge-time check"
- **After**: states that `/sc:pr-submit` is unchanged and keeps its skip rule; explains why the loop's absent state is sticky and clock-based (`reviewers.py:390-391`, SKILL.md:31-32; one done plus one absent reads clean, :414-419); five explicit hold steps (read owner-set `reviewers` list, request a review of the final head from each listed reviewer because the loop never re-triggers, re-poll the final head, wait up to 60 minutes with the zero-checks fallback to the push time of the final head, raise `review_none_present` or `review_stalled`, neither overridable); rules for the list (write-protected on the owner's recorded word including `none`; an uninstalled reviewer stalls every PR and the gate names it; what `none` prints); residual falsifiers (INV-012) with "narrows, does not close"; whether Codex reviews on push marked UNVERIFIED; gate, re-trigger, 60 minutes and lists marked "not shown to pass".
- **Provenance tag**: `<!-- Source: Variant B (CLAY), Cited facts 2 to 4, with Round 1 shared assumption A-001, Round 2 Variant A item 2 and probe INV-005, INV-007, INV-008, INV-009 - merged per Change #3 -->`
- **Validation**: structural integrity OK; references OK; contradictions none (skip rule stays in the loop; the hold does not read the loop's state)
- **Note**: the sources do not define when `review_none_present` versus `review_stalled` is raised. The mapping written (no listed reviewer shows activity versus a listed reviewer does not finish) is an interpretation of Variant B fact 2 (`merge_wait` returns `no_response` when all listed reviewers are absent) and is worded as a requirement. The `none` output ("prints `reviewers: none`, raises neither reason") is written as a requirement because the probe says the design leaves it undefined.

### Change 4: `answer-check` as a stale-answer validator only
- **Status**: Applied
- **Source**: Variant B mechanism item 4 and cited fact 5; Round 2 A item 3; Round 2 B concession; probe INV-003, INV-013
- **Target**: "The mechanism" item 5 (modified); and the sentence "Approvals and goes are given in chat and are checked as such" in "The claim" (the phrase the plan quotes sits in the claim, so it was replaced there too)
- **Before**: item 5 "Approvals live in chat, not files or relayed text (...)"; claim "Approvals and goes are given in chat and are checked as such."
- **After**: item 5 keeps its original sentence and adds the validator wording (entry, question key, head sha, newer than the notice; D:694), "It does not prove who typed the answer" (`orca terminal send` into the same terminal, D:112; a script knows the sha), spoofed typing as a residual risk, harness marking of sent text UNVERIFIED, `answer-check` not built and not shown to pass. Claim now reads: "Approvals and goes are given in chat. A validator checks that a recorded answer is current and matches its question; it cannot prove who typed it (mechanism item 5)."
- **Provenance tag**: inline `<!-- Source: Variant B (CLAY), The mechanism item 4 and Cited fact 5 - merged per Change #4 -->` in item 5; section tags on "The claim" and "The mechanism" read "Base (original, modified)"
- **Validation**: structural integrity OK; references OK; contradictions none

### Change 5: One-shot go versus `E-NO-GRANT`
- **Status**: Applied
- **Source**: Variant B Round 2 "Remaining dispute" item 4; Variant B fact 5 (grants keys); probe INV-011
- **Target**: new H2 "Standing lists"
- **Before**: nothing on standing lists
- **After**: the verb refuses any GitHub write not on a list the owner recorded in chat; the list never holds `pr.merge` or `issue.close`; the merge go is a one-shot entry, not a grants row; a two-column table (action, how it is authorized) with rows for issue-pipeline duties (standing list, R17), Full Submit push and PR (per-issue go, R25, never a merge, force push or branch deletion), merge (per-PR go), issue close (never on a list; the person's instruction names it), any other write (refused). Requirement for INV-011: the merge goes through one verb that demands the go entry and refuses a raw `gh pr merge` outside it; the verb does not exist and is not shown to pass; the post-merge audit is the interim check.
- **Provenance tag**: `<!-- Source: Variant B (CLAY), Round 2 "Remaining dispute" item 4 and Cited fact 5 (grants keys), with probe INV-011 - merged per Change #5 -->`
- **Validation**: structural integrity OK; references OK ("Steps, step 7" resolves after Change 9); contradictions none

### Change 6: Script-started depth-0 coordinator and the contract lines to amend
- **Status**: Applied
- **Source**: Variant B cited fact 7; Round 2 A (c), (d); Variant A facts 7 and 8; probe INV-010
- **Target**: "The claim" (modified), "Cited facts" 7 and 8 (modified), new H2 "Contract amendments"
- **Before**: claim "(or started by the owner's installed watcher under an authorization the owner recorded in chat)"; fact 7 and fact 8 as in the base
- **After**: claim says the coordinator is person-opened or started at depth 0 (terminal plus `ccsession`, never `worker-start`) under an authorization the owner recorded in chat, and that a launch-prompt authorization is self-attested. Fact 7 adds that R25 is in a local unpushed plan, amends :245 and counts only after the owner approves it in chat. Fact 8 adopts Variant B's depth reading (D5's depth reason concerns `worker-start`), narrows fact 2 accordingly, keeps "person opened" (:70) as a separate authority rule needing amendment, and declares the launch prompt self-attested (INV-010), requiring that the prompt cite the owner's recorded authorization and list only the duties it names, not shown to pass. "Contract amendments": (1) :70 proposed sentence, (2) :245 sentence taken verbatim from Round 2 A, (3) :23 and :244 unchanged with a note; each marked as needing the owner's chat approval (Owner DECISION) and none applied. ADD1's worker route is stated as not adopted.
- **Provenance tag**: `<!-- Source: Variant B (CLAY), Cited fact 7, with Variant A Round 2 (c), (d) and probe INV-010 - merged per Change #6 -->` (Contract amendments); inline tags on facts 7 and 8
- **Validation**: structural integrity OK; references OK; contradictions: two were found and fixed inside this change. (a) The base "What it gets right" third bullet called R25 "owner-approved", which contradicts fact 7 as modified (R25 is unpushed and needs approval); the bullet was qualified and tagged. (b) Fact 2 ("person opened is a precondition that protects fan-out") would overread D5 after the depth-0 reading; fact 2 was left as written and fact 8 states that it narrows fact 2.

### Change 7: Nine-row "what reaches the person" list as a reasons inventory
- **Status**: Applied
- **Source**: Variant B cited fact 6; Round 2 B "Remaining dispute" item 5
- **Target**: new H2 "Reasons to reach the person" (three lines)
- **Before**: no such section
- **After**: line 1 states the design's nine-row table (D:664-696) and the rule "an unanswered question waits, no default" (D:692); line 2 adopts it only as an inventory for non-outward decisions and says every outward action still waits for the person's go; line 3 is flagged "Owner DECISION" (whether to adopt), benefit UNVERIFIED, remove the section if not adopted.
- **Provenance tag**: `<!-- Source: Variant B (CLAY), Cited fact 6 and Round 2 "Remaining dispute" item 5 - merged per Change #7 -->`
- **Validation**: structural integrity OK; references OK; contradictions none

### Change 8: Risk register with residual risks and the admin-side control
- **Status**: Applied
- **Source**: Variant B risk habit (K12, AU4a, AU7); shared assumption A-004; probe INV-003, INV-012, INV-013
- **Target**: "What it risks" (modified)
- **Before**: two bullets (person is a bottleneck; skipping a silent reviewer can finish a loop clean; "OURS has no separate merge-time check")
- **After**: both original bullets kept (the second updated to say a merge-time check now exists in "Silent reviewer", designed and not built, because the old wording would contradict Change 3); a table (risk or cost, mitigation, status) with ten rows covering the bottleneck, prose-only contract rules, state change with the sha unchanged, late reviewer, dead 60-minute wait, spoofed typing, self-attested launch prompt, go replay after a restart, raw `gh pr merge`, and unprotected `master`; status values are "designed", "accepted", "UNVERIFIED" and "Owner DECISION", and the text says no row is "built". Branch protection, a ruleset, required review or a merge queue is stated as a repo-admin action and an Owner DECISION, not a consensus item (A-004). A closing paragraph lists the INV-013 falsifiers and says "narrows, does not close".
- **Provenance tag**: `<!-- Source: Variant B (CLAY), risk habit (K12, AU4a, AU7) with shared assumption A-004 and probe INV-003, INV-012, INV-013 - merged per Change #8 -->`
- **Validation**: structural integrity OK; references OK; contradictions none
- **Note**: the plan says "replace the two bullet lists under 'What it costs' and 'What it risks' with the table plus the original bullets kept". I read it as: keep both original bullet lists and add the table (the table also carries the two "What it costs" items). "What it costs" is therefore unchanged.

### Change 9: Post-merge audit kept
- **Status**: Applied
- **Source**: Variant B Round 2 hybrid gap on AU4a and AU7 (D:812, D:601)
- **Target**: "Merge procedure", "Steps", last step (appended as step 7 after the read-back)
- **Before**: steps ended at the read-back (step 6)
- **After**: step 7: the audit after the merge (AU4a, AU7) is kept even when a person gave the go, because it can find a merge the gate did not make.
- **Provenance tag**: `<!-- Source: Variant B (CLAY), Round 2 hybrid gap on AU4a and AU7 (D:812, D:601) - merged per Change #9 -->`
- **Validation**: structural integrity OK; references OK (cited by "Standing lists" and the risk table); contradictions none

### Edits outside the nine planned changes
- The title was changed from "Position OURS (D06)" to "Recommended authority model (D06)" and the status line was reworded, with a conventions paragraph ("narrows" versus "closes", "not shown to pass", "Owner DECISION"). This frames the output as the plan's Overview requires ("the recommended authority model written as spec text") and adds no facts. Tagged "Base (original, modified)".
- The "What it gets right" third bullet and the "What it risks" second bullet were edited only to avoid contradictions introduced by Changes 6 and 3 (described above).

## Post-Merge Validation

Performed by reading the full merged file after the last edit, plus three mechanical greps.

### Structural Integrity
- **Heading hierarchy**: PASS. One H1 (title), twelve H2 sections, four H3 sections; no level is skipped. The four H3 ("Steps", "The go: contents, expiry and reach", "Gate reasons and what a go may override", "Windows") all sit under the H2 "Merge procedure", so none is an orphan.
- **Section ordering**: PASS. The claim, the mechanism, Merge procedure, Silent reviewer, Standing lists, Contract amendments, Reasons to reach the person, Cited facts, What it costs, What it risks, What it gets right. The base sections keep their original relative order; the five inserted sections sit between "The mechanism" and "Cited facts".
- **Document flow**: PASS. Procedure comes before the sections that refer to it; "Steps, step 7" exists before it is cited.
- **Other mechanical checks**: no `FILL:` marker remains; no em dash or en dash appears; the three provenance comment lines open the file; every section and every inserted or modified block carries a Source tag; "Owner DECISION" appears 13 times and covers the go expiry number, the `changes_requested` hard refusal, branch protection on the repository, adopting the nine-row list, the 60-minute default, and the contract amendments.

### Internal References
- **Total**: 23 (section-name, step and fact references such as "Contract amendments", "What it risks", "The go: contents, expiry and reach", "Steps, step 4", "Steps, step 7", "Standing lists", "Silent reviewer", "mechanism item 5", "fact 2", "Cited fact 6" via "memory note above")
- **Resolved**: 23
- **Broken**: 0

### Contradiction Re-Scan
- **New contradictions introduced**: 0 remaining. Two were introduced mid-merge and fixed (see Change 6 validation): the "owner-approved" wording of R25, and the reach of fact 2 after the depth-0 reading. One more inconsistency was found by the read-through and fixed: the `changes_requested` row said "No." and then asked whether a go may merge over it; it now reads "Recommended rule: no, a hard refusal. Owner DECISION ... Until the owner decides, treat it as a hard refusal."
- **The person's go is required for every merge, in every section**: PASS. The claim says "never merges on its own initiative"; Merge procedure says a passing gate never triggers a merge and the go is required for every merge in every section; Standing lists puts merge on a per-PR go and never on a standing list; Contract amendments says the Full Submit go "never covers a merge"; Reasons to reach the person says every outward action waits for the go. Cited facts 6 and 9 describe an autonomous miss and the design's conflicting flow as history and concession, not as adopted rules.
- **The pr-submit skip rule stays in the loop**: PASS. Claim, mechanism item 4 and the first paragraph of "Silent reviewer" all keep it; the hold step reads fresh state and does not change the loop.
- **pr-submit is never a worker**: PASS. Claim, mechanism item 3, Contract amendments item 3 (ADD1's worker route is stated as not adopted) and Cited facts 3 and 4.
- **Unbuilt or UNVERIFIED gates marked "not shown to pass"**: PASS for the merge gate, second gate run, `answer-check`, go expiry and recorded entry, re-trigger, 60-minute hold, reviewer lists, merge verb, launch-prompt authorization and the contract amendments. Claims are worded "narrows" where a gate lowers a risk.
- **Noted tension, not a new contradiction**: the `merge_safety` row lets a go clear the reason only when it carries that reason's own question key (as the plan specifies), while Variant B reads D:583 and D:593 as a hard hold. The document states this openly in the table row. The orchestrator may want the owner to confirm the plan's rule.
- **Noted tension carried from the base**: the claim lets a script-started depth-0 coordinator act while the contract at :70 still says "person opened"; the paper says the :70 amendment is needed and none is in force.

## Summary
- Planned: 9
- Applied: 9
- Failed: 0
- Skipped: 0
- Limits to report: Change 2 names nine of the thirteen gate reasons because the inputs name no more (the last table row covers the other four); Change 3 interprets which condition raises `review_none_present` versus `review_stalled`, as the sources do not define it.
- Validation: PASS

## Orchestrator addendum (after the merge-executor finished)
The orchestrator read `merged-output.md` in full and made three edits, all tagged in the file:
1. "Gate reasons and what a go may override": the four reason names the executor lacked (`checks_pending`, `review_pending`, `threads_open`, `worker_not_done`) were added from the closed set at `docs/designs/orchestrator.md:582` (master export), each as "No, wait or answer first", so all thirteen now have a row. This resolves the Change 2 note above.
2. `merge_safety` row: reworded to match D:593 (a merge-safety change is held until an explicit OK tied to that PR and head sha; a recorded OK for a failing check never clears it). This removes the "tension" noted in the post-merge validation: the design and the paper agree.
3. The sentence "The gate is a closed set of thirteen reasons (D:578-583)" now cites D:582 for the names.
The `changes_requested` row stays "recommended rule: no, hard refusal; Owner DECISION", as the executor wrote it. Status after the addendum: success; Validation: PASS.
