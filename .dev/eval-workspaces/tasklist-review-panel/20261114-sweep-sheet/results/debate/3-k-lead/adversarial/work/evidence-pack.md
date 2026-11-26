# Evidence pack for the K-arm lead-in debate (written by the orchestrator; every fact was read from disk in this session)

SW = /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet
RL = /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger  (sibling Redesign 2 workspace; READ ONLY)
MR = /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md (READ ONLY)
OUT = SW/results/debate/3-k-lead/adversarial

## The decision under debate
DESIGN.md DD-14 (SW/DESIGN.md line 73) and 15.1 row 4 (line 802): the paragraph of arm K is generated from a fixed lead-in (`SW/briefs/k-lead.txt`) plus the eight class-card `definition` fields. The owner is asked to approve the lead-in as drafted. Default under test: APPROVE k-lead.txt unchanged.

## F1. The text (SW/briefs/k-lead.txt, 2 lines; line 1 is a comment that is not sent)
Line 1: `# DRAFT, awaiting owner approval (DD-14). Lines that start with "# " are comments: they are not sent to the reviewer.`
Line 2 (the lead-in, 151 chars, 33 words): "Eight kinds of defect to look for in your own review of the plan. Each one says what to look for. A plan may have none of them, one of them or several."
Byte-identical copy at RL/briefs/k-lead.txt (checked with cmp). RL DESIGN.md line 91 (DR-16): "Adopted from SWD DD-14 ... one shared decision of both builds."

## F2. The whole K paragraph as sent (SW/scaffold/briefs.py `k_paragraph` lines 90-107; rendered by OUT/work/render_k.py, output in OUT/work/render_k.out)
1224 chars, 226 words, one paragraph with no line breaks: the lead-in, then "(1) <definition C1> (2) <C2> ... (8) <C8>" in card order. The eight definitions (SW/cards/C1..C8.json field `definition`, 92 to 182 chars each):
(1) A criterion asks for a complete or exhaustive result over a set with no bounded method or stopping rule, or the criterion's scope differs from the scope of the instruction it checks.
(2) A rule stated in the driving document is not carried into the plan's task text or criterion.
(3) A value, field or state is read, mapped or required by one component and no row, task or step writes it for that case.
(4) A criterion embeds a command, pattern or test selector whose literal form cannot match or cannot pass against the text or state the same plan orders.
(5) After a change, a count, claim or copy in a second location is left stale because no task enumerates that location.
(6) A sentence says "all", "only", "never" or "outside X nothing", and an inventory, the plan's other tasks or the scope of the enforcing test contradict it.
(7) Verbatim text the plan dictates omits a clause of a constraint stated elsewhere, or contradicts the plan's own criterion.
(8) A plan edits files or behavior that a test elsewhere pins, with no task that updates or runs that test.

## F3. Where K sits in the brief (SW/scaffold/briefs.py `part_names` lines 110-121; DESIGN.md 8.1 lines 424-441)
Z0 = base, CB-1 (only with a source), CB-2, CB-3, CB-4, CB-5. K = Z0 parts + K paragraph (LAST, after CB-5). SS = Z0 parts + ledger rule + sheet block + heading + sheet text. Rendered lengths (OUT/work/render_k.out, with a source and a 1-item dummy sheet): Z0 2921 chars; K 4147 (+1226); SS 4633 with one dummy item (+1712; the real sheet text is added on top: sheets may be up to 16,000 chars, DESIGN 6.3).
So the K paragraph is shorter than the SS addition by an amount that grows with the sheet. MR 934 lists "Prompt length hurts small models" as a risk (Medium) for the recipe arm.

## F4. The shared parts that surround K (SW/briefs/*.txt, quoted in MR 3.0.2, lines 196-221)
- base.txt (also in Z0): "... Report concrete wrong outcomes, not a minimum number of findings. Minor findings are notes and never fail the review ..."
- CB-1 (only with a source): "Driving document: {{SOURCE_ABS}}. Read it in full before you review the candidate. A rule it states that the candidate does not carry is a finding." MR line 203: "It is rendered only when a source file exists. Otherwise the harness logs `no_source` and C2 is not applicable for that document (INV-013)."
- CB-2: "Every defect you confirm must appear as a line in the findings block, including every ledger row you marked PROBLEM. ... Do not leave a defect out because it looks small." Purpose (MR 207): removes suppression, T3b. MR line 37: T3b = reporting filters suppressed findings (80 reviewer-level drops, 49 blocking findings lost).
- CB-3: "A tool line or a recipe step is a fact or a question about the text. It becomes a blocking finding only if you can write the sentence ..."
- CB-5: "The checks you were given do not replace your own review. Keep at least half of your time for your own review of the plan." (appears BEFORE the K paragraph in K.)
- The K lead-in says the eight kinds are things to look for "in your own review". CB-5 treats "the checks you were given" as separate from "your own review". The K paragraph never uses the word "check"; MR 1035 calls them "the eight checks".
- SS sheet block (sheet-block.txt, 1015 chars): "... Your job is to judge it. ... Do not skip an item. ... A sheet item is a question, not a finding. Most items are fine. Answer PROBLEM only when you can quote the two texts, or the search result, that prove it. ... Keep at least half of your time for your own review of the plan. The sheet does not replace it."
- SS ledger rule (ledger-rule.txt, 473 chars): final message must carry a `## Ledger` block with one line per assigned item.

## F5. What SS gives a reviewer per item, against what K gives (DESIGN.md 6.1 to 6.3, lines 346-383; cards)
SS item = class id (C1-C8, no name), location (task and lines), the literal trigger text, up to 5 tool-output lines (search hits, NO MATCH, etc.), and the class `question_template` (a one-step question, some with a method: C4 "Do not use the current file as evidence; it may already contain the finished work."; C6 "run one count or listing command over the tree"; C8 "Open the referencing file the plan never names."). It does NOT print the class `definition`. At most 12 items per document; only triggered classes appear. A forced one-line verdict per item (OK, PROBLEM, UNSURE).
K = the eight `definition` fields for every class, no location, no text, no tool output, no question, no forced verdict (MR 1035: "No recipes, no sheet, no ledger").
So the two carry different information by design: K names every class; SS names the places and runs the tools for some classes.

## F6. Why K exists and how it is judged
- MR 1035: K = "Z0 plus one paragraph naming the eight checks in plain words. No recipes, no sheet, no ledger. Tests whether recipe or script machinery beats a plain checklist."
- MR 1091: gate D7 = "Gain over K at least 0.04 absolute on D2's metric, otherwise K wins." MR 1100: "K within 0.03 of RL: Report that recipe wording adds nothing over plain words, and adopt the cheaper form."
- Code (SW/analysis/analyze.py `_effect` 594-603, `gate_d7` 727-736, LIMITS 481-495): D7 passes when mean found fraction of SS minus K is at least 0.04. It is a point difference; no bootstrap bound is used for D7 (D2 uses the point difference >= 0.12 AND a 90% bootstrap lower bound > 0.04).
- Orchestrator arithmetic (DERIVED, not measured): if D2 passes (SS - Z0 >= 0.12) then D7 fails only if K - Z0 > 0.08. So D7 changes the adoption result only in the region where the K prompting share exceeds about 0.08.
- MR 120 (prior): "A checklist alone does no better than ad hoc reading in human inspections; a detection recipe per class is what helped (scenario reading about +35%, replication mixed)."
- MR 1000, 1106: the three study packages are never evidence for adoption; Stage 1 decision sets hold about 36-40 items, 5 runs per document, 4 documents; "A pass is evidence, not proof."
- K runs in Stage 1 only (MR 5.4 lines 1045-1056): 4 decision documents x 5 runs = 20 panel runs = 60 reviewer reports (RL's schedule would share them; SW/TESTING.md line 254 counts 3 arms x 4 documents x 5 = 60 panel runs in this build).
- K is paired with the same documents, judge and panel clock as Z0 and SS.

## F7. Leak surface
- The lead-in contains no document text, no class names, no hold-out detail; it discloses the number "eight".
- The eight definitions are the target-neutral `definition` fields of the cards (cards/README.md). They are the same words the card file holds for SS. Cards and briefs are frozen by git tag and sha256 BEFORE the hold-out ground truth is written (MR 1026, REQ-33; SW/bin/freeze.sh line 43 hashes `cards/*.json` and `briefs/*.txt`; IMPLEMENTATION.md step 14.3 decides the K lead-in, 14.5 freezes, 14.6 writes hold-out ground truth).
- The cards' `swap_test` records are still empty (filled at step 14.2 by a second author), so the definitions may still change before the freeze; approving the lead-in does not approve the definitions.
- The classes were derived from the three study packages (MR 1000). That is shared by K and SS.

## F8. Tests, files and copies that pin the lead-in
- tests/test_briefs.py::test_k_paragraph_from_the_eight_cards (lines 187-204) pins: the paragraph has no newline, holds "(n) <definition>" for the eight cards in order, ends the K brief, and `part("k").splitlines()[0]` starts with "# DRAFT" and contains "owner approval (DD-14)". It does NOT pin the lead-in sentence text. test_no_src_path_in_any_brief and test_sha256_of_every_part_and_brief read the file but store no hash of it. config/freeze.json does not exist yet (the freeze has not run).
- The draft marker (line 1) is pinned by that test; approval therefore does not remove it, and the frozen file would still say "DRAFT, awaiting owner approval".
- RL/briefs/k-lead.txt is byte-identical; RL/runs/rehearsal-K/briefs/*.txt hold fake-model rehearsal briefs that contain the lead-in text. A change to SW's k-lead.txt would split the shared control unless RL is edited; this task may not edit RL.
- results/copy-briefs.py does NOT touch k-lead.txt (its header: "briefs/k-lead.txt is a hand-written draft and is not touched here").

## F9. What is known about the real effect: nothing
No real-model run of any K brief exists. The RL rehearsals are fake-model runs. Every statement about how the wording moves K's found fraction, finding count, time, or format failures is UNVERIFIED. The compliance and timing spikes (DESIGN 14.2) never run K.
UNVERIFIED: whether the decision plans have a driving document (CB-1 absent means no_source; then K's definition (2) refers to a driving document that the brief never names, while SS produces no C2 item). The three derivation packages each have a source (config/packages.json); the hold-out list is not in this folder.

## F10. Rules of this debate (from the owner's order)
Advocates on Sonnet or Haiku only (never Opus). Nobody opens any file named ground-truth*.json or any score file. Nobody stages, commits or pushes. Nobody edits src/, tests/, .claude/, .dev/tasks/ or the brainstorm. Only the orchestrator may edit, and only after a FAIL: SW/briefs/k-lead.txt, SW/DESIGN.md (DD-14 and 15.1), SW/results/owner-decisions.md, and any test that pins the lead-in. Verdict rule: PASS = no blocking defect survived; a blocking defect = the default would make the experiment unfair, unmeasurable or misleading, or would break a stated requirement. FAIL = at least one did. Minor findings are notes.

## F11. The owner's attack questions (answer each, with evidence)
Q1 Is K a fair, strong control or a strawman (too weak makes SS look good; too strong makes SS lose for the wrong reason)?
Q2 Does the lead-in leak anything about the hold-out answers?
Q3 Does it differ in length or tone from the SS brief in a way that confounds?
Q4 Does "a plan may have none" discourage findings?
Q5 Is the generated paragraph (lead-in plus definitions) equivalent in information to what SS gives?
