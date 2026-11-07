# Round 2 rebuttal: Advocate for Variant 2 (reviewer-2, qa)

"plan" = `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-021737/TASK-WF-brainstormFixBri-20261106-021737.md`; "brief" = `source.md` in the same folder. Everything cited was Read or run this round.

## Response to criticisms

| # | Criticism of V2 (who) | Answer | Verdict |
|---|---|---|---|
| 1 | R2-1 (F-16 line) is P1 but overstated: the plan's wording matches spec 7.2 (`spec:282`: commit to "the feature branch or a scratch branch with the user's authorization", no merge) (A1 R1, A3 R1) | Read `spec:282`: confirmed, no merge step. The plan wording ("committed to a branch the live-check worktree is built from", plan:25) states the spec's own requirement and still covers a P2 author on another branch. The brief's "commits and merges" is a simplification. A1's R2 retraction ("equivalent in effect, not the quoted line") is the right middle: same effect, not the verifier's literal line. I concede P1. | Concede severity (P1 to note/P3). Keep: verifier literal and departure unrecorded. |
| 2 | Constraints carry no AC; `/sc:implement` judges ACs through a closed template, so F-16 cannot block (A3 R1, A1 R2) | Read `qa.md:318`: the template is closed, seven slots, "may not add, remove or reword any criterion". True for per-task reviews. But the managed FINAL (`qa.md:310`) also reads "the plan's `## Constraints`" and returns `issues` when "a plan `## Constraints` item is violated"; per-task Q4 (`qa.md:339`) is "quoted-constraint-breach" against a diff. Both need a diff that breaches a Constraints item. A line about when edits reach a live plan cannot be breached by a diff, except by committing, which both wordings forbid ("this plan does not commit"). So neither wording can block execution. Conceded. | Concede: not an execution blocker. It stays a brief-fidelity finding for this audit. |
| 3 | R2-1 "drops the motivating scenario" (my own claim) | Withdrawn. Plan:25 names "a branch the live-check worktree is built from", which is exactly the scenario (`spec:282`). Only the word "merges" is lost, and the spec does not require it. | Withdrawn |
| 4 | R2-3 is tagged Grounded but is an inference about executor writes; unsized (A1 R1, A3 R1, A1 R2) | Conceded on tag: it is INFERRED. On size I now have evidence against my own claim. `implement.md:58`: a managed package always uses the sibling `progress.md` ledger; retries go to `<pkg>/artifacts/retries/` (`managed-workspace.md`). `git status --porcelain` today shows `.dev/reflect/pre-...001016/` and `pre-...021737/` as collapsed `??` directory lines. New files inside an already-untracked directory do not create a new line, so only a new top-level untracked path outside the package would trip bullet 3. `.dev/reflect/` is not gitignored (`git check-ignore` returns nothing), so a brand-new `.dev/reflect/<new>/` would be a new line, but `/sc:implement` has no step that creates one. Exposure is small. | Concede: INFERRED, small. R2-3 drops to a note. |
| 5 | V2 missed C-001/X-001 and C-005 (A2 R1 (mine), A3 R1, A1 R2) | True. I read plan:38 and plan:128 as separate edits and did not set them side by side. A QA card should have. No excuse. | Concede |
| 6 | V2 missed R3-3 (C-007) (A3 R1) | True; see below, C-007 is also lower than A3 claims. | Concede miss |
| 7 | S-002: V2 tags every finding Grounded (A1 R1) | Fair for R2-3 only. R2-1, R2-2, R2-4, R2-5 each quote both sides (brief line vs plan line). | Concede for R2-3 only |
| 8 | R2-2 (F-13 sentence) says "necessary deviation" but offers no fix (my own R1 weakness) | Fix: record it beside plan:131 ("the sentence names the status snapshot because F-2 adds it; `make sync-dev` also rewrites `.claude/`"), or write the brief's literal sentence and accept the F-2 conflict. Brief:169 itself says "writes only the logs", so the "only" flaw is brief-owned. | Concede; supply fix |
| 9 | C-012/C-013 are cosmetic (A3, A1) | Agreed. C-012: the plan satisfies the unsampled spans. C-013: spec:286 begins "4. Check the contract". | Concede (low) |
| 10 | V2's 0.87 self-confidence is unearned (A3 R1) | Agreed in effect: the blind calibration for V1 was 0.73 with 7 findings; V2's five findings missed the highest-severity defect. | Concede |

## Updated assessment

Steelman first: V1 reproduced a mechanical check weakness; V3 found the only plan-text defect that contradicts a claim the plan makes in its own voice (plan:133) and a second fragility (R3-3); A1 and A3 both held V2 to the right standard on severity, since a Constraints line cannot block the executor. My R1 P1 does not survive.

### (a) V1's proposed fix for the listed-contract conflict

V1 replaces, in the live-check sentence, "exists and holds its own `return-contract.yaml`, and every" with the same text plus "(not checked for a call whose `codebase` entry is `skipped` or whose directory `/sc:analyze` refused), and every".

Correct? Mostly yes.
- It moves into the first clause the two carve-outs that already sit in the "required only when" clause (plan:128). Both clauses then agree.
- A crash recorded as anything other than `skipped` still has to leave a contract: `analyze.md:98` says the contract "is written on every outcome" once the directory is usable. A missing file there is a true FAIL, which is the intent of brief:225.
- `skipped` is checkable from the contract itself (`SKILL.md:371-373`: `quality_tier: primary | fallback_1 | skipped`; `handoff-routing.md:77` records `skipped` on timeout).

Keeps brief:225 intact? Yes. It does not touch plan:38 (the Task 1 tail "listed in `artifacts`, also when the call failed" stays byte for byte) and it keeps the listing unconditional. The carve-out is on the check, not on the listing.

Testable? Partly. The `skipped` branch is testable from the contract. The "refused" branch is not observable from files: `analyze.md:97` says a refusal is "printed in chat only", so it needs the session file, and the existing last clause already says the session file may be "not verifiable". Where it is not verifiable, the refused carve-out cannot be invoked and the first clause fails exactly as today. That is the same edge V1 itself calls "effectively unreachable". Acceptable, but the sentence should say so or accept it.

Does it need a matching plan change? Yes, three:
1. Plan:128 must carry the parenthesis. But plan:128 is brief Part 4's sentence, "copy exactly, do not paraphrase" (brief:213). The F-1 verifier (brief:45) requires Task 6 to carry the sentence "byte for byte as in replacement_wording". So V1's fix is itself an unrecorded departure from the brief's highest-priority (P1) verifier unless the owner amends Part 4 first, or the plan records it next to plan:131 as a Necessary deviation. V1 downplays unrecorded departures elsewhere; here its own fix creates one.
2. Plan:133 ("no known false FAIL") is true only after that change. Without it, plan:133 must be narrowed.
3. The Task 6 AC (plan:143) pins three substrings (`lc10`, `a source: codebase entry`, `neither quality_tier nor source records`). None is touched, so no AC edit is needed. AC 144 (two lines changed) is unaffected. There is also no AC that checks "byte for byte", so the plan's ACs cannot detect either the brief's wording or V1's. That gap exists today (F-1's verifier asks for byte equality; AC 143 gives three substrings).

Alternative that needs no sentence change: keep Part 4 byte for byte and, in the plan only, replace plan:133's "no known false FAIL" with an honest statement and add a fifth residual risk in the false-FAIL direction ("a `/sc:analyze` call cut off by the per-source timeout can leave a listed path with no contract; the first clause then fails a correct run"). This is cheaper, makes no unrecorded change to brief wording, and surfaces the problem to the owner. My recommendation: do the alternative now, and ask the owner to approve V1's parenthesis as a Part 4 amendment.

### (b) Does `/sc:implement` judge the brief's verifiers? (qa.md:318)

Read: `qa.md:318` is a closed template; the orchestrator "fills only the seven slots" and "may not add, remove or reword any criterion". The slots include `{global_constraints}` and `{task_brief}`, and Q4 is "quoted-constraint-breach: does the diff violate a quoted plan constraint ... or an explicit task instruction". So V1 is right: brief verifiers are not judged. Only plan text is.

Consequences:
- C-002 (F-16): the Constraints line cannot be breached by a diff (only by committing), so it cannot block. Severity: note/P3. Fidelity finding only.
- C-003 (F-13): the sentence is task body text, i.e. an "explicit task instruction" (Q4), and Q3 asks about mutation "outside the task's declared outputs". A strict reviewer could mark Task 7's "writes only logs and snapshot" false (Q2 false-claim: "a recipe ... followed as written" does not do what the text says, because `make sync-dev` rewrites `.claude/`). But plan:21 labels those writes "output, not edits", the `.claude/` copies are gitignored so they never reach the diff or the status snapshot, and Task 7 produces no delivered text. The realistic chance of a blocking finding is low but not zero. So C-003 is P3, with a one-clause fix ("and the gitignored `.claude/` copies").
- The managed FINAL (`qa.md:310`) reads Constraints and returns `issues` for "a plan `## Constraints` item is violated". That also needs a breach.
So V2's A-002 point survives only as "fidelity, not blocker".

### (c) C-007 and the live-check "the contract"

V1 is right for a conforming brief. Read: spec line 142 (3.1 brainstorm row, column "Brief must pass"): `--output <dir>`; `WORKER-CONTRACT.md:192`: same; `brainstorm.md:154`: "With `--output` the worker fields are added to the command's own `<output>/return-contract.yaml`"; `SKILL.md:369-371`: `domain` and `enrichment_used` are fields of that own contract. So under a conforming brief, `<contract>` in 7.2 step 4 (`spec:286`) holds `domain`, `enrichment_used` and the worker fields together. R3-3 bites only a brief that passes `--report-dir`, which `brainstorm.md:153` allows but the spec's brief table does not. Two caveats keep it from being nothing: the Task 6 sentence does not say "with `--output`", so a P2 author who passes `--report-dir` gets a false FAIL on the `source: codebase` entry; and the `nested/analyze-` paths in the sentence are relative to the report dir either way. Verdict: V3 found a real fragility, V1 is right that it is a note (P3), not an "ordinary-route" false FAIL as A3 argued.

### Other variants, adversarial view
- V1: best on mechanical probes; A-2 tag wrong in the text-conflict half; fix proposal (a) is good but creates its own Part 4 departure; its A-5 "executor outputs stay in the package" is better evidence than my R2-3.
- V3: best evidence on C-001; R3-2 false today (index shows 001016 staged); R3-7 does not bite (`sc-implement-protocol/SKILL.md:97`: "Default sequential in source order"); R3-3 overstated; R3-4 to R3-6 are brief-mandated wording the plan cannot change without a recorded deviation.
- V2 (mine): the only card to hold the plan to the brief's literal verifiers; but missed C-001, and overrated severity.

## New evidence

1. `qa.md:310,318,339`: FINAL reads Constraints and fails only on a violated item; per-task Q4 needs a diff breach. Neither can fire on the F-16 line.
2. `git status --porcelain` today (this round): `001016` is `A`; `.dev/reflect/pre-...001016/` and `pre-...021737/` are collapsed `??` directory lines; `.dev/reflect/` is not gitignored. New files inside an existing untracked directory add no line; this shrinks X-005.
3. Ran `git show HEAD:refs/handoff-routing.md ... | grep -c ...`: prints 0; the full-path form also prints 0 and `git show` exits 0 on the full path. Confirms C-005 (Task 4 routing half only).
4. `sc-implement-protocol/SKILL.md:97` exists ("Default sequential in source order"), which shrinks C-011.
5. V1's fix applied to plan:128 would break the byte-for-byte verifier of F-1 (brief:45); AC 143 cannot detect it either way.
6. `brainstorm.md:154` vs `153`: `--output` and `--report-dir` are both legal in the command, but only `--output` is in the spec's brief table (`spec:142`, `WORKER-CONTRACT.md:192`).

## Final diff-point positions

| Point | Final superior position | Changed since Round 1? | One-line evidence |
|---|---|---|---|
| S-001 | none | no | Counts reflect depth and bias; V2's P1 and V3's R3-2 P1 do not survive |
| S-002 | V1 | yes (was split) | V1 tags A-3/A-5 INFERRED; V2 tagged R2-3 Grounded wrongly; V3 tagged R3-1 failure Grounded (WC-4 `artifacts` = files written) |
| C-001 | V3 (on evidence), P2 | no | plan:38 vs plan:128 vs `analyze.md:97-98`; real on timeout; wording brief-owned (brief:217,229,237) |
| C-002 | split (V2 on recording, V1 on severity) | no | verifier literal (brief:201) and unrecorded; plan wording matches `spec:282`; not blockable (`qa.md:310,318,339`); P3 |
| C-003 | V2 (classification), V1 for the "only" point | no | forced by F-2 (status-after.txt), unrecorded; "only" is brief-owned (brief:169); P3 |
| C-004 | V1 | no | `git status` today: `001016` is `A`; only this package `??`, exempted at plan:157 |
| C-005 | V1 | no | Run this round: short and full path both print 0; narrow to Task 4 routing half (plan:95) |
| C-006 | V1 | no | Only raiser; format-check point valid, exit-code point weak; low |
| C-007 | split (V3 found it, V1 sets severity P3) | yes (was V3) | `spec:142`, `WORKER-CONTRACT.md:192`, `brainstorm.md:154`: conforming briefs pass `--output`; bites only `--report-dir` briefs |
| C-008 | V3 (as an out-of-scope note) | no | Twin `WORKER-CONTRACT.md:24` unedited; a fix needs a seventh file (plan:21) |
| C-009 | V3 | no | `handoff-routing.md:77` records `skipped` on timeout; wording brief-mandated (brief:230) |
| C-010 | V3 | no | `spec:60,62` already name Skill and Agent; only Task inferred |
| C-011 | none | yes (was V3) | `sc-implement-protocol/SKILL.md:97` sequential in source order; Task 1 runs first |
| C-012 | V2 | no | Only V2 checked matrix coverage; plan satisfies the spans; low |
| C-013 | none | yes (was split) | All three agree, cosmetic: `spec:286` begins "4. Check the contract" |
| C-014 | none | no | All three confirm pins, slices and Part 4 copy |
| X-001 | V3 (P2) | no | Conflict real; failure only on timeout; unobserved in practice; fix is a Part 4 amendment (V1's parenthesis) or a narrowed plan:133 |
| X-002 | V1 | no | Index today: earlier package `A` |
| X-003 | split (V1 on severity, V2 on recording) | no | Not P1; `spec:282` supports the plan; departure still unrecorded |
| X-004 | V2 | no | Necessary deviation (F-2), unrecorded; "only" flaw brief-owned |
| X-005 | V1 | yes (was split) | `implement.md:58` ledger is the sibling `progress.md`; collapsed `??` lines; V2's exposure is small and INFERRED |
| A-001 | QUALIFY | no | `analyze.md:97-98` holds for a usable directory; not for a caller timeout (`handoff-routing.md:77`, plan:128) |
| A-002 | QUALIFY | no | `qa.md:318`: task ACs/constraints judged, brief verifiers not; C-002/C-003 are fidelity notes, C-003 carries a small Q2 risk |
| A-003 | QUALIFY | no | Before/after snapshot (plan:33,157) absorbs baseline; only mid-run changes matter |
| A-004 | ACCEPT | no | Brief mandates exact pins (brief:232-233); slices supply placement |
| A-005 | QUALIFY | no | Not a brief rule; brief:34 and plan:131 make silence a note-level gap |
