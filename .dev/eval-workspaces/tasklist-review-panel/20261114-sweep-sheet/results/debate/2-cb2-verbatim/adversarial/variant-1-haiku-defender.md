# 1. Position

Retain CB-2 verbatim in every non-raw arm and retain the heading count: the clause creates a plausible, disclosed weakness, not an established blocking defect; I propose no replacement wording.

Paths used below:
- **SW** = `/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet`
- **RL** = `/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger`
- **MR** = `/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md`

# 2. Evidence

1. **The default follows an explicit requirement.** MR:201 puts the edits in every non-raw arm; MR:209 supplies this exact clause; MR:1124 requires verbatim CB text. MR:1152 separately requires empty-sheet equality with Z0. Equality alone does not require the ledger wording, but verbatim compliance does.
2. **The clause is not a command to create a ledger.** SW/briefs/cb2.txt:1 says “including every ledger row you marked PROBLEM”; its governing instruction is to list every confirmed defect. With no marked rows, that inclusion adds no work. Actual ledger creation, heading, format and item instructions appear separately in SW/briefs/ledger-rule.txt:1 and SW/briefs/sheet-block.txt:1. This is a defensible reading, not proof that models always follow it.
3. **Treatment construction is explicit.** SW/DESIGN.md:433-441 gives Z0 the common parts, K the added checklist paragraph, and SS the ledger and sheet additions; empty-sheet SS returns to Z0. MR:1034-1037 defines the corresponding comparisons, including K without ledger machinery. The common clause is not secretly assigned only to controls.
4. **The diagnostic has a narrow, real implementation.** SW/analysis/analyze.py:1010-1028 counts accepted Z0/K reports containing an exact stripped `## Ledger` line, preferring raw reviews to normalised reports. SW/TESTING.md:187 requires per-arm reporting and an owner decision above zero. It does not establish that zero headings means zero confusion.
5. **Verbatim and equality checks are substantive contracts.** SW/tests/test_briefs.py:64-79 checks quoted MR bytes; :134-160 checks empty-sheet and fallback equality; :207-218 checks calculated hashes. These are inspected assertions, not test results from this debate.
6. **The clause also serves the treatment.** SW/DESIGN.md:511-523 promotes an unwritten PROBLEM finding only as MINOR and non-blocking. Removing the inclusion instruction could therefore affect how SS expresses genuine blocking discoveries, not merely clean up controls.
7. **The sibling shares the decision.** RL/briefs/cb2.txt:1 contains the same wording; RL/DESIGN.md:87-91 describes byte-identical control briefs and adopts DD-7. SW/DESIGN.md:66 and :801 explicitly disclose the dangling-clause risk and recommend the default.

# 3. Strongest case against my own position

Identical words need not produce identical burdens. SS supplies a ledger and explains it; Z0 and K do not. A control reviewer could search for missing instructions, invent a table, waste review time, or suppress findings while trying to reconcile the clause. Conversely, invented ledger work could improve control recall. Either direction could change finding counts and the checklist comparison.

The heading diagnostic misses alternative headings, bare tables, silent hesitation and reports excluded by its accepted-status filter. It cannot isolate the clause's causal effect without a clause-free comparison. Therefore, it would be misleading to advertise zero headings as proof of an uncontaminated baseline.

Nevertheless, the stated comparison is between complete review configurations containing shared brief edits, not an identified causal effect of the sheet alone. MR:1070-1074 measures actual findings and consistency. A possible prompt interaction does not make those outcomes unmeasurable. Nor does a reference to existing marked rows necessarily violate K's absence of ledger machinery. The opponent needs more than the possibility of a worse reading to establish that this default makes the experiment unfair.

# 4. Size of the harm

**UNVERIFIED:** My best qualitative estimate is a small rather than dominant average effect, assuming reviewers treat the clause as conditional and prioritise the explicit findings instructions. I cannot defensibly assign a numerical rate or upper bound. Rare severe confusion could still move a close decision. The heading count measures visible spillover only; neither a nonzero count nor its absence determines finding-count bias.

# 5. What would have to change if the default were replaced

An authorised override would need SW/briefs/cb2.txt, DD-7, section 15.1, and the decision record updated. SW/tests/test_briefs.py:64-79 would need an explicit exception to the immutable MR quotation, not a weakened silent check. Empty-sheet/fallback equality should remain intact.

Part and rendered hashes would change; the freeze must reflect the replacement (SW/bin/freeze.sh:37-45). SW/results/copy-briefs.py:29-36, :66-68 would otherwise restore the old wording. RL requires a separately authorised coordinated change before its controls can be treated as identical; neither RL nor MR may be edited here.

# 6. Blocking?

**NO.** The default preserves the stated verbatim requirement and measurable configuration comparisons; the incomplete diagnostic leaves a disclosed uncertainty, not established unfairness or a licence to claim that confusion is absent.
