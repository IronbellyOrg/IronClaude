# Scoring Reconciliation: position-bias disagreements (Step 3)

- Step: 3 (hybrid scoring, qualitative layer), reconciliation of `scoring-pass-1.md` (input order) and `scoring-pass-2.md` (reverse order) for the /sc:adversarial git-ownership debate.
- Evaluator: independent reconciler, not an advocate. Date: 2026-11-02. Verdicts here are FINAL for the 15 disputed criterion-variant pairs.
- Inputs re-read: both passes; `variant-1-original.md` .. `variant-5-original.md` (`V<n>:L` = line L); for correctness, `round2-advocate-a.md:60` (N3), `debate-transcript.md` (N3 at 1221, C4/C10), `invariant-probe.md`.
- Rule: binary, no partial credit. MET needs a specific citation from the variant; otherwise NOT MET.

## Tests applied (one test per criterion, used for every variant)

- **Completeness 1 (R1-R7):** every requirement must be addressed in the text (a dedicated section is not required; that is Structure 5). R3 names two crash cases, "a worker or the git owner", so both must be addressed unless the variant makes them the same actor.
- **Completeness 4 (success/completion criteria):** needs an explicit statement of done-ness: when an action, or the design, counts as complete or successful. An output record (a SHA in a contract, a `worker_done` event, a PR link shown to the person) is a record, not a criterion. This is the test pass 1 itself used to fail V1.
- **Completeness 5 (out of scope):** an explicit statement that some action or case is not handled by the proposal and is handed elsewhere. V4's agreed MET ("outward actions fall back to A", V4:17) sets the bar.
- **Correctness 1 (factual errors):** a claim the debate showed false counts against every variant that makes it. N3 (`round2-advocate-a.md:60`) shows `/sc:implement` workers write refs, a private index and the working tree via `git restore`; so "workers make no git call / leave no git state" is false as a factual claim.
- **Clarity 1 (unambiguous language):** the wording has one reading. A design that is parameterized by the brief, with the options enumerated, is not ambiguous wording.
- **Risk 4 (external dependencies and their failure scenarios):** names a dependency outside the proposal's own control (Orca, GitHub/pr-submit, Agent tool, `/sc:git`, #326 K3) AND states what happens to the design when that dependency fails, is unavailable, or misbehaves. "Not yet delivered, with a stated consequence" counts as unavailable.
- **Invariant 1 (collection boundaries):** needs the empty case (no grant, no contract, nothing to commit) plus at least one of single or maximum. The single-writer case appears in every variant, so it alone does not show boundary analysis.
- **Invariant 3 (guard condition gaps):** names a specific guard or precondition and a case where it does not hold, is unchecked, or is unverified.

## Rulings

| # | Dimension | Criterion | Variant | Pass 1 | Pass 1 evidence (short) | Pass 2 | Pass 2 evidence (short) | Final | Reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Completeness | 1. Covers R1-R7 | V4 (D) | MET | Lock/HEAD (V4:14,20,23), auth hop and audit (V4:18-19), Recovery (V4:26), Context, PR, Day to day, Cost | NOT MET | Recovery covers subagent and coordinator crash only (V4:26); no worker crash | NOT MET | V4:26 covers the git owner (subagent, coordinator) only. R3 names "a worker" crash too, and V4 never states what a worker crash leaves behind; "recovery as A" in V4:26 is attached to the coordinator crash, not the worker. Safety/audit is covered (V4:18-19), so that is not the reason. In V2 the worker is the git owner, so its one case covers both. |
| 2 | Completeness | 4. Success criteria | V2 (B) | MET | "the worker's contract lists the commit SHA" (V2:22); SHA field (V2:38) | NOT MET | Searched all sections; no criterion | NOT MET | A SHA in the contract is an audit record (V2:22 is under "Audit trail"), not a statement of when a commit or the design is done. Same test that fails V1 (agreed NOT MET). |
| 3 | Completeness | 4. Success criteria | V3 (C) | MET | Own Task, Dispatch, `worker_done`, outcome per action (V3:11); git result contract shape (V3:46) | NOT MET | Contract shape is an output shape | NOT MET | V3:11 explicitly calls the per-action Task/outcome "the per-action audit record"; V3:46 is an implementation item. Neither defines success. |
| 4 | Completeness | 4. Success criteria | V4 (D) | MET | Subagent ends with "report the SHA" (V4:8) | NOT MET | "report the SHA" is an output | NOT MET | V4:8 is the subagent's role instruction; it names an output, not a done condition. |
| 5 | Completeness | 4. Success criteria | V5 (E) | MET | Worker "lists each SHA in its contract's `artifacts`" (V5:13) | NOT MET | Contract SHAs are a record | NOT MET | V5:13 is a condition on the worker row and V5:25 repeats it as the audit trail. Record, not criterion. |
| 6 | Completeness | 5. Out of scope | V2 (B) | MET | Coordinator "still owns merging branches back ... (so B still needs A for merges)" (V2:29); "B is never complete on its own" (V2:44) | NOT MET | Names gaps, declares nothing out of scope | MET | V2:29 hands merges out of B's worker scope to the coordinator, the same form as V4's agreed MET "outward actions fall back to A" (V4:17). V2:20 also excludes `/sc:git` as the tool ("`/sc:git` cannot be the tool ... Workers would run plain `git`"). |
| 7 | Correctness | 1. No factual errors | V3 (C) | MET | Orca mechanics verified; Round 2 C4, C10 are judgement concessions | NOT MET | "Other workers never run mutating git" (V3:8) false per N3 | NOT MET | V3:34 "Worker crash: no git state to repair, as in A" is the same factual claim that failed V1 (V1:24, agreed NOT MET): N3 shows `/sc:implement` workers write and delete refs and restore files (`round2-advocate-a.md:60`). The SPEC:156 omission alone would not fail it. |
| 8 | Clarity | 1. Unambiguous language | V2 (B) | NOT MET | Brief picks among levels; B never says which level it proposes (V2:8) | MET | Allowed actions enumerated (V2:8) | MET | V2:8 says the brief states the allowed level, enumerates the three levels, and ties the choice to the quoted user instruction (D4 (a)). That is a parameterized rule with one reading, not vague wording. The "for example" triggers are labelled examples. |
| 9 | Risk | 4. External dependencies and failure scenarios | V1 (A) | NOT MET | Orca durability relied on, no Orca/GitHub failure scenario (V1:25,28) | MET | Orca message queueing during pr-submit waits (V1:28); Run state durable (V1:25) | MET | V1:14: dependency on #326 K3, and while it is absent "A cannot honour ... commit after each task". V1:28: pr-submit's attended loop blocks up to 600 s per wait budget, so the coordinator does not react to workers, with Orca's durable queue as the mitigation. Both name a dependency and its unavailable or misbehaving case. |
| 10 | Risk | 4. External dependencies and failure scenarios | V2 (B) | NOT MET | No Orca, GitHub or pr-submit failure scenario (V2:17-32) | MET | `/sc:git` has no unattended mode, so workers run plain git (V2:20); K3 needed (V2:19) | MET | V2:20 names `/sc:git`'s missing unattended mode and the consequence (workers run plain `git`); V2:19 names K3 as a prerequisite protocol change for implement-side commits. |
| 11 | Risk | 4. External dependencies and failure scenarios | V5 (E) | NOT MET | No Orca, GitHub or pr-submit failure scenario (V5:22-35) | MET | K3 absent: "until it exists a worker commits only through steps its brief adds after the command finishes" (V5:41) | MET | V5:41 names the #326 K3 dependency and the explicit fallback while it is unavailable. |
| 12 | Invariant | 1. Collection boundaries | V2 (B) | MET | One worker per worktree vs two committers (V2:11,14) | NOT MET | Single case only; no empty case | NOT MET | V2 states single vs two writers (V2:11,14) but never the empty case: no grant, no SHA, nothing to commit, or an absent contract. |
| 13 | Invariant | 1. Collection boundaries | V3 (C) | MET | Maximum one active Dispatch per terminal (V3:12) | NOT MET | No empty case | NOT MET | V3:12 gives a maximum. No empty case found; "no git state to repair, as in A" (V3:34) is a cross-reference to a crash claim (and a false one, #7), not an empty-collection analysis. |
| 14 | Invariant | 1. Collection boundaries | V4 (D) | MET | "one subagent at a time"; two subagents collide (V4:14,20) | NOT MET | Single and two-writer only | NOT MET | V4:14,20 give single and two-writer cases; no empty case anywhere (V4:7-43). |
| 15 | Invariant | 3. Guard condition gaps | V1 (A) | NOT MET | Guards stated, no gap; quiescence detection not discussed | MET | Orca ownership guard: coordinator "is doing owner work unless the user's plan names it as owner" (V1:42) | MET | V1:42 names Orca's guard (a review-only `worker_done` "authorizes synthesis of findings, not coordinator file edits"; PR preparation stays with the named owner, `[G:cl] 62-65`) and the case where A falls outside it: the plan does not name the coordinator as owner. That is a stated guard gap, the same kind as V2's missing stale-lock step (agreed MET). |

## Consistency notes (agreed verdicts not changed, listed only)

1. **Completeness 1, V2 (agreed MET).** Under my R3 test V2 passes because its worker is the git owner (V2:24-26). But V2:29 also makes the coordinator a git actor (merges), and V2 never addresses a coordinator crash mid-merge. A stricter reading ("every git actor") would fail V2. Borderline; left as agreed.
2. **Completeness 4, V1 (agreed NOT MET).** Now consistent: all five variants are NOT MET on success criteria, which matches pass 2's note that no variant met it.
3. **Correctness 1, V4 (agreed NOT MET).** Agreed for X-005 in pass 1; under my test V4:8 ("Workers never run mutating git") would also fail it. Consistent; no change in verdict.
4. **Risk 4, V3 and V4 (agreed MET).** Consistent with my test; all five variants are now MET on Risk 4.
5. **Risk 5, V2 (agreed NOT MET) vs V5 (agreed MET).** Consistent with ruling #2: a SHA in a contract is a record. V5 passes Risk 5 only because it adds a checker ("the coordinator's later review", V5:45); V2 names no checker.
6. **Invariant 1, V1 and V5 (agreed MET).** Consistent with the empty-plus-one test: V1:24 (contract "or its absence") with V1:11 (single writer); V5:38 ("Without that instruction nothing is committed") with V5:13 (only writer).
7. **Invariant 3 (all five MET after ruling #15).** Consistent; each names a guard and an unheld or unverified case.

No agreed verdict was found that contradicts a ruling outright; note 1 is the only one a stricter test would flip.

## Final totals

Final = agreed MET count + MET rulings above.

| Variant | Agreed MET | MET rulings (#) | Final /30 |
|---|---|---|---|
| V1 (A) coordinator main chat | 23 | 2 (#9, #15) | **25** |
| V2 (B) workers own git | 20 | 3 (#6, #8, #10) | **23** |
| V3 (C) dedicated git session | 23 | 0 | **23** |
| V4 (D) coordinator subagent | 19 | 0 | **19** |
| V5 (E) hybrid | 24 | 1 (#11) | **25** |

V1 and V5 tie at 25/30 on the qualitative layer; the tie is for the quantitative layer and debate matrix to settle. Edge-case floor (Invariant dimension) after reconciliation: V1 5/5, V2 4/5, V3 4/5, V4 3/5, V5 5/5; no variant falls to 0.
