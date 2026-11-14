<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant B (Option D, blind grader) -->
<!-- Merge date: 2026-11-14T01:18:57Z -->

<!-- Source: Base (original, modified) - title extended with the merged scope, Change 20 -->
# Proposal (merged): who decides whether a finding blocks (C05, `who-judges-blocking`)

<!-- Source: Debate record - status banner, Change 20 -->
> **Status: PARTIAL. This is the result of a debate, not a settled design.**
>
> - Alignment 90.9% (30 of 33 debate points have a determinate agreed outcome). Convergence was NOT achieved: it was blocked by invariants. The invariant probe found 11 HIGH-severity UNADDRESSED invariants (assumptions the probe tried to break and the debate did not resolve), 10 MEDIUM and 2 LOW UNADDRESSED, and 2 ADDRESSED. Three points are agreed-open: C-005 (does panel size move precision), C-012 (what caused the veto's wrong blockers) and X-002 (V7 and the contamination reading disagree on attribution).
> - Round 3 was not run (depth standard). Nothing in this document states that any invariant is resolved. The full list is in "Unaddressed invariants".
> - Base: Variant B (Option D, blind grader after clustering). Variant A (Option A, hardened single-reviewer veto) led on combined score (A 0.9091, B 0.8810, margin 0.0281, inside the 5% band), so the Step 3 tiebreaker applied: debate points won B 6, A 2. This says nothing about whether the grader is accurate; nobody has measured that.
> - What runs today is the existing, unhardened veto. Everything else here is a proposal, a target, or a measurement plan. Nothing in this document has been built.

<!-- Source: Debate record - Decision summary, merged per Change 1 (Overview decision list) -->
## Decision summary

**The shape the debate agreed on.** Reviewers propose. What runs today is the existing, UNHARDENED veto: a finding group (a ledger row or a cluster) blocks when any one member is flagged blocking, and the verdict is FAIL while one blocking row is open (`ledger.py:187,274`, `cluster.py:375`). The hardened veto is the interim TARGET; it becomes available only once four prerequisites are built: D1 (stop silent drops of findings over the length limits), D2 (a partial or invalid reviewer must not clear a row), the named resolver (a named step that re-reads a citation that did not resolve) and the degrade scope (the certification rule applies at round 1 and later rounds inherit it). None of the four is built. A blind grader (a separate agent that cannot see who found a finding, how many found it or what label they gave it) is built behind the veto and runs in shadow: it records its grade and nothing reads it for the verdict. It goes live per lens only after a pre-registered paired replay passes, starting with singleton blockers.

**What is agreed.** Each item carries the invariants that qualify it. None of them is settled.

| # | Agreed by both advocates after verifying source | Qualified by (all UNADDRESSED unless marked) |
|---|---|---|
| 1 | What runs today is the existing, unhardened veto (`ledger.py:187,274`, `cluster.py:375`). The hardened veto is the interim target once D1, D2, the named resolver and the degrade scope land; none is built. The grader is built behind the veto in shadow and goes live per lens only after the paired replay, starting with singleton blockers | INV-019, INV-020, INV-022, INV-023, INV-015 |
| 2 | `promoted` (a cluster no reviewer flagged that the grader would block) is counted only and cannot raise a FAIL in shadow (C-003) | INV-023 |
| 3 | Certification is set at round 1 and inherited by later rounds; `defer()` recomputes it (C-002, X-005) | INV-004, INV-007, INV-024 (INV-003 is ADDRESSED) |
| 4 | The grader may demote only with a named failed criterion; on doubt the reviewer's flag stands or the row goes to PENDING (X-006). The named criterion is checked by format only, not for truth | INV-008, INV-021 |
| 5 | D1, D5 and D6 are fixed first, for both arms of the replay (C-012) | INV-014 ("D1 fixed" is undefined and the fix can cancel the evidence gate) |
| 6 | The panel cap of three finders is a cost cap only; its effect on precision is OPEN (C-005) | none recorded |
| 7 | Reflect keeps the debate and contract 1.8.0; reflect-post decides by a code predicate and not by a grader (C-008, C-011); the E2 evidence transfers only to the spec and tasklist lens (A-001) | INV-016 |

**What is agreed to be open.** C-005 (does panel size move precision), C-012 (what caused the veto's wrong blockers) and X-002 (V7 and the contamination reading disagree on attribution). See "Unresolved conflicts".

**What blocks convergence.** 11 HIGH + UNADDRESSED invariants (INV-001, 004, 005, 011, 014, 019, 020, 021, 023, 024, 025), plus 10 MEDIUM and 2 LOW UNADDRESSED. The debate did not resolve them. See "Unaddressed invariants".

**Not decided here.** Whether the grader is accurate; whether the veto's false-block rate is what E2 shows or an artifact of its inputs; which reflect-post predicate applies; any numeric pass threshold for the replay. The Owner decisions section lists what the owner must set.

<!-- Source: Base (original, modified) - glossary added so that every term is defined on first use, Change 19 -->
### Terms used in this document

| Term | Meaning |
|---|---|
| veto | The rule that a ledger row or a cluster blocks when any one member's `blocking` flag is true. "Hardened veto": the same rule with its inputs repaired (see "Interim rule") |
| candidate | A cluster (v2 path) or ledger row (v1 path) that the grader is asked about, chosen by a code rule (see "Candidates, promotion and singletons") |
| shadow | The grader runs and records its grade; nothing reads the grade for the verdict, the exit code or the merged report |
| `grade` | The grader's outcome for one candidate: `blocking`, `not_blocking`, `undecidable` or `unconfirmed` |
| `decision` | The ledger routing word: PASS, REVISE or ESCALATE (and PENDING under `--decide grader`). It is never the grader's outcome |
| `model_class` | The class of the model that ran an agent (used for class-disjoint selection). `deviation_class` keeps its own meaning: the reflect deviation class (authorized, necessary, drift, regression, none) |
| E2 | The tasklist-review panel evaluation at git commit `4a22d74`, under `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/`: three packages, 16 ground-truth defects, 4 to 6 runs per panel, reports `COMBO-REPORT.md` and `PILOT-REPORT.md` |
| D1 to D6 | Defects found by E2's audit D of the merge code and its inputs. D1: findings over the length limits (anchor over 200 characters, claim over 300) are silently dropped (49 blocking findings; four FAIL-to-PASS flips). D2: a partial or invalid reviewer can clear a row it did not re-report (`ledger.py:254-257`). D3: one valid reviewer is enough for a round to count. D5: a blocking row whose anchor is not found (null span) is kept and can block. D6: over-merged rows (83 rows with eight or more members or four or more sections). D4 is not used in this document |
| UC-1, UC-2 | Reflect use cases: UC-1 is the pre-execution audit of a plan against its spec; UC-2 is the post-execution deviation audit |
| B1 to B3 | The frozen stoprule rubric: B1 a verbatim quote, B2 a concrete wrong outcome, B3 a blocking kind (`rubric.md`) |
| INV-nnn | A finding of the invariant probe (see "Unaddressed invariants") |
| U-nnn | A unique contribution of one variant, numbered in `adversarial/diff-analysis.md` (A: U-001 to U-008; B: U-009 to U-017) |
| S4 | `synthesis/synth-04-options-conflicts.md` under `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/` |
| S-nnn, C-nnn, X-nnn, A-nnn | Debate points (structural, content, contradiction, promoted shared assumption). Each of the 33 is defined by topic in the table in "Debate record and provenance". The ones used in this Decision summary: C-002 PASS rule and reviewer-count guard; C-003 candidate set and promotion; C-005 panel-size policy; C-008 per-lens predicate or rubric; C-011 reflect integration and contract constraint; C-012 reading of the E2 evidence; X-002 cause of the veto's wrong blockers; X-005 degraded PASS versus the one-reviewer fallback; X-006 "fail-closed" versus the not-blocking default; A-001 transfer of the E2 result to other lenses |

Synthesis conflicts cited (numbers without a hyphen; each is a separate conflict in S4):

| ID | One line |
|---|---|
| C02 | Anchor handling at merge: persist every rejected line, flag a missing anchor instead of letting it block silently (decided) |
| C03 | Model and tier configuration, gateway versus anthropic-only; its own debate chose anthropic-only class launch values and left O-2 open |
| C04 | Distinctness: declared per-slot policy with recorded intended replicas (decided) |
| C05 | This conflict: who decides blocking (veto, quorum, calibrator, blind grader or debate); undecided by evidence |
| C07 | How runs are recorded: one manifest per run, telemetry groups (decided) |
| C11 | Reflect merge path and contract bump: keep the debate and contract 1.8.0 (decided) |
| C12 | Clustering algorithm: complete-link admission on the v2 location model (decided) |
| C13 | Ledger model: re-find and cluster versus find-once, verify-only later rounds (undecided) |
| C14 | Panel size versus cost: fix the rubric first, cap at three (resolved by its own debate, partial) |
| C15 | Bad-line policy: keep valid lines, mark the reviewer partial, persist every rejection (decided) |
| C16 | Blocking predicate per lens, held as data; reviewer flag kept as input (decided) |
| C17 | Fate of the code-driven Tier 2 engine behind the tasklist post gate: fix in place first (decided) |
| C19 | One verdict contract and exit-code vocabulary (decided) |
| C20 | Rollout and evaluation: shadow for safety, ground-truth benchmark for quality (decided) |

Debate point IDs (with a hyphen: S-nnn structural, C-nnn content, X-nnn contradiction, A-nnn shared assumption) are listed with a topic and the agreed outcome in "Debate record and provenance". Open items named in the base and cited here: G-03 (does MINOR drift halt), G-04 (who sets `unauthorized_deviation_present`), G-05 (is static unreachability a Regression), G-57 (a paired legacy-versus-panel reflect run), G-59 (owner for the benchmark port), O-2 (the environment the central panel serves).

<!-- Source: Base (original, modified) - Design section; Position restructured to the staged-decider shape, Change 1 -->
## Design

<!-- Source: Base (original, modified) - Position rewritten: the unhardened veto runs today, the hardened veto is a target, the grader is shadow then per-lens; Variant A "The decision" folded in - Change 1 -->
### Position

**Reviewers propose; the existing, unhardened veto is the rule that runs today; the hardened veto is the interim target once its prerequisites land; a blind grader runs in shadow and takes over, one lens at a time, only after a pre-registered paired replay passes.**

- **Today.** A cluster or ledger row blocks when any member's `blocking` flag is true, a re-found row takes the current round's flag, and the verdict is FAIL while the Reviser brief (the blocking open or regressed rows) is non-empty (`ledger.py:187,213-218,99-104,274`; at cluster level `cluster.py:375`). Nothing about this is hardened: D1, D2, the named resolver and the degrade scope are not built.
- **Interim target.** The same rule with its inputs repaired (see "Interim rule: the hardened veto"). It is a target, not a description of the live system.
- **Grader, in shadow.** A separate agent grades each candidate against a frozen per-lens rubric without seeing reviewer ids, model names, severity, the `blocking` flag, support or overlap. In shadow its grade is recorded next to the veto's decision and nothing reads it for the verdict.
- **Grader, live.** Per lens, after the replay gate (see "Rollout"), starting with singleton blockers. In the destination state a candidate blocks only when the grader grades it `blocking`; the reviewer's flag stays in the record as an input and as the measurement baseline.

**Why a grader is on the table at all.** E2 measured the veto at 65 judge-blocking catches against 38 real blocking defects over 71 valid-era rows, and a four-reviewer panel (`2x luna + 2x ember`) carried 2.75 to 3.25 more wrong blockers than every comparator (Evidence rows V2 and V3). Two readings of that result survive the debate. The grader reading: the flagger is also the judge, so the decision belongs to a separate context. The veto reading: the 27 extra catches are real ground-truth defects that were graded blocking and did not block implementation (a severity over-grade, EC3), and E2's rows were produced under input defects D1, D5 and D6. The debate did not decide between them: the cause of the wrong blockers is agreed-open (C-012, X-002). A grader is the only candidate in either variant that changes who makes the call in the spec lens, and nobody has measured whether it closes the over-grades.

**Not claimed.** This document does not claim that the grader is accurate, that a replay on the E2 packages is enough to choose between the veto and the grader (INV-019, INV-020, INV-022), or that the shadow counts show which decider is right (INV-023).

<!-- Source: Variant A, Design "The decision" and "What changes is the input to the veto" - merged per Change 2; corrected by Round 2 A concessions 2 and 7 and facts F1, F6 -->
### Interim rule: the hardened veto (a target; the unhardened veto is what runs today)

The rule: `blocking = any(effective flags of the members)`, and the verdict is FAIL while one blocking row is open. No second agent, score threshold, vote count or debate sits between the flags and the verdict. Both advocates agreed the hardened veto is the right interim and that it is not "the grader design minus the grader" until its four prerequisites are built. Each prerequisite acts on what enters the veto; none is a decider.

| # | Prerequisite | What the debate added | Still open |
|---|---|---|---|
| 1 | **Evidence gate before blocking** (C02, D5): a finding whose anchor or citation does not resolve is kept and flagged, and cannot be effective-blocking until a named resolver re-reads it | The gate needs a named resolver (C-007); the A-003 condition applies (see "Evidence gate and named resolver") | INV-005, INV-006, INV-014, INV-025 |
| 2 | **Per-lens predicate as data** (C16): the reviewer's flag is an input; the core records an effective flag (`blocking_effective`) next to it; `channel: advisory` and `grounding-gap` never block; reflect-post uses a code predicate (see "Reflect-post: code predicate") | The two rules a "predicate" could mean differ (INV-016) | INV-016 |
| 3 | **Partial reviewers abstain** (C15, D2): a reviewer with rejected lines is `partial`, never clears a row and never counts as "found nothing" | D2 is a code change at `ledger.py:254-257` (the clearing step never reads `block_ok`) that inverts the existing pin at `test_review_ledger.py:376-385`; the "partial" concept does not exist in the code today [VIA transcript Round 2 F6] | INV-013, INV-009, INV-014 |
| 4 | **Complete-link clustering** (C12): one blocking member must not turn a 19-member chained row into one mega blocker | A C12 dependency, not built here; E2 had 83 chained rows (D6) | INV-011 |

**Two copies of the rule.** `ledger.py:187` runs `any(...)` over v1 groups produced by the v1 `findings` module (the document loop), and `cluster.py:375` runs it over v2 clusters. They are two implementations on two schema versions, not one rule read from two places (see "Adapters and the two copies of the rule"; C-015, A-007).

**Dropped.** Variant A's claim about the veto's FAIL set bounding every decider is dropped (X-001): the debate found it false for the promotion path and neither advocate re-asserted it. Variant A's panel cap of three finders is kept only as a cost cap (see "Cost"; C-005).

<!-- Source: Variant A, Design "Asymmetric verdict" (U-001) combined with Base (original) Verdict logic and CLI table (PENDING) - merged per Change 3; scoped by Round 2 A fact F7 and B finding G2 -->
### Certification and verdict vocabulary

C-002 ended HYBRID (73%): Variant A's degrade rule on top of Variant B's PENDING. X-005 ended HYBRID (69%): certification is a loop property, set at round 1 and inherited. One reviewer may fail a plan; two reviewers with a valid block are needed to certify a PASS. This matches reflect's own rule that a single-reviewer merge is degraded (`contract.py:295-296`; also `:317-326` for convergence below 0.80). Everything below is proposed; none of it is built.

1. **Certification at round 1.** A first review in which fewer than two reviewers hold a valid block (a reviewer whose block parsed without a rejected line) and which would otherwise PASS returns PASS with `degraded: true`. The flag is set at round 1 and inherited by later rounds. Decision words and exit codes 0, 10 and 11 are unchanged. The flag is written to the round record and to a report line placed before the final `verdict:` line (the last line is pinned: `test_review_ledger.py:468-472`). `verdict()` keeps its key set (it is compared as an exact dict at `test_review_ledger.py:299-304`), so the flag is stored elsewhere.
2. **`defer()` recomputes.** `defer()` (`ledger.py:356-360`) sets PASS when the brief empties, with no reviewer-count check, so a human deferral on a one-reviewer loop would otherwise yield a certified PASS. It recomputes `degraded` from `rounds[0].reviewers[].block_ok` and, under `--decide grader`, recomputes PENDING (undecided rows carry `blocking: None`, which keeps them out of the brief, so without this a PENDING round could be deferred into PASS).
3. **PENDING and exit 12 exist only under `--decide grader`**, with an entry in `EXIT_BY_DECISION` (`ledger_cmd.py:13`, used at `:109`); without the entry a PENDING decision raises a `KeyError`.

**Open points, not fixed by this design.**
- INV-004 (HIGH): the PASS that ends a loop after a REVISE is decided by a re-review, and the default re-review is one reviewer (`document_review_loop_prompts.md:70`; one valid block suffices, `ledger.py:150-157`). Under "certify at round 1, inherit later" that single-reviewer PASS is labelled certified by inheritance, and the flag is sticky. A guard for a thin deciding round is missing.
- INV-007 (MEDIUM): `_decision` has no PENDING mapping at the review cap (`ledger.py:93-96`); a PENDING round does not consume a review; after the rerun a batch is `unconfirmed` for good, so the loop has no exit except a human.
- INV-024 (HIGH): exit codes stay 0/10/11 and `test_review_cli.py:348` asserts exit 0 and PASS; the in-repo consumers read prose, not the flag, so nothing in code enforces "uncertified". Whether any caller must treat `degraded` as uncertified in code is an owner decision (see "Owner decisions", C19).
- INV-009 (MEDIUM): "two valid blocks" is not "two independent looks" (see Risks R17).
- Addressed in the debate: INV-003 (ADDRESSED, LOW): `defer()` can recompute the flag because `block_ok` is stored per round.

<!-- Source: Base (original, modified) - "What the core does" steps 1, 4, 5 split into Candidate rule, Promotion and singletons, Recording; Variant A "Record who and how many" merged - Change 4 -->
### Candidates, promotion and singletons

The core is `src/superclaude/cli/review/`. The proposal adds one stage between clustering and verdict and changes nothing before it.

<!-- Source: Base (original, modified) - "What the core does" step 1; the v1 form was added - Change 4 -->
#### Candidate rule

1. **v2 path (clusters).** A cluster is a candidate when its `channel` is `defect` and at least one member is flagged blocking or has severity MAJOR or CRITICAL. Clusters whose members are all MINOR cannot block under the parser (`findings_v2.py:107-108`), so excluding them loses nothing. Clusters on the `advisory` or `grounding-gap` channel never block (the rule `research/05` section 13.1 proposes; grounding gaps route through `needs_human_decision`). Singletons are candidates, not dropped: the evidence that most confirmed defects are found by one reviewer rules out a quorum filter (X5, V6).
2. **v1 path (ledger rows, the document loop).** The same rule has no channel test, because v1 findings are all defects: `blocking or severity in {MAJOR, CRITICAL}` (see "Adapters and the two copies of the rule").

<!-- Source: Base (original, modified) + Variant A Design item 1 - evidence gate, named resolver, seal rule - merged per Change 6; conditions from C-007 (HYBRID 66%) and A-003 (QUALIFY 58%) -->
#### Evidence gate and named resolver

C-007 ended HYBRID (66%). The agreed rule: a finding with an unresolved citation or anchor is never effective-blocking until a named resolver re-reads it; absence findings are routed to the quoted requirement text; the grader never treats `unverified` evidence as sole support. Variant B's own advocate proposed adopting stoprule's seal rule; that is B's proposal for how to meet the rule, not an agreed mechanism.

- **A-003 condition, verbatim.** Absence findings survive the gate only if the anchor quotes the requirement text that is incomplete, and a failed locate routes to a re-read, not to suppression.
- **v2 path.** The pre-check is `superclaude review verify-citations` (`verify_cmd.py:1-13`; it flags missing files, out-of-range lines and quotes not found in the cited lines, with no model call). The resolver is the existing evidence-validator step, which keeps or drops citations; `review cluster --kept` re-clusters the survivors (`cluster_cmd.py:119-125,165-170`). A cluster that loses all its citations is not graded and is recorded as `dropped-unfounded`.
- **v1 path.** The signal is `anchor_status == "missing"` (`span is None` on the row; pinned by `test_review_ledger.py:408-417`). There is no re-read resolver on this path today.
- **What stoprule does and the v1 loop does not.** In stoprule a failed re-read forces a repair pass, and after the second seal the claim becomes `minor-form` (`stoprule.py:264-265,283-284,541-553,590`). The v1 document loop has no repair pass and no resolver, so porting the rule there means suppression unless a resolver is built.

Open, not solved: INV-005 (HIGH): with the live veto a gated row leaves the brief (`ledger.py:99-104,274`), so the round can PASS before the resolver runs, and v1 members carry no anchor status. INV-006 (MEDIUM): a located anchor proves where the reviewer pointed, not that something is absent, and a fix that inserts text elsewhere leaves the row `named_not_touched`, so the loop ends in ESCALATE. INV-025 (HIGH): the population that fails the gate is the population it must not suppress (D5's 13 null-span blocking rows [VIA audit-D], D1's recovered long anchors). INV-014 (HIGH): the D1 fix and this gate can cancel each other.

<!-- Source: Variant A, "Record who and how many" (singleton_blockers) merged with Base (original) R8 - per Change 4 (C-003, C-004, X-001) -->
#### Promotion and `singleton_blockers`

- `promoted` (no reviewer flagged the cluster and the grader would block it) is counted only. In shadow it cannot raise a FAIL (C-003, HYBRID 68%). Its precision is unmeasured: Variant B's R8 admits it, and the shadow runs hold 26 non-blocking MAJOR findings among 42 MAJOR (V8). Variant A's claim about the veto's FAIL set bounding every decider is dropped (X-001).
- `singleton_blockers` is the count of blocking clusters whose blocking members all come from one reviewer. It is added to the cluster output and to the telemetry, and read by no verdict rule (C-004, HYBRID 64%; derived from `reviewers[]`). Singletons are the first population the grader goes live on.
- **What the shadow counts measure.** `overruled` (a reviewer flagged the cluster blocking and the grader did not), `promoted` and `singleton_blockers` measure disagreement. They do not measure who is right: production loops have no ground truth (INV-023, HIGH). Wherever this document says the paired record helps compare the deciders, read it as a disagreement record plus whatever weak label exists (the reviser's applied or rejected fix map, `ledger.py:330-342`, which the consensus did not name as a label and nobody has checked as one).

<!-- Source: Base (original) - "What the core does" step 5 -->
#### Recording

`blocking_any`, `blocking_all`, `support`, `disputed` and `reviewers` stay on the cluster (`cluster.py:323-378`) next to the grade. Every run therefore carries a paired veto-versus-grader record at no extra model cost. The core adds no numeric threshold, no quorum and no calibrator to the decision. Support and overlap are recorded and used for measurement and for ordering batches, not for deciding.

<!-- Source: Base (original, modified) - grader section; "fail-closed by construction" replaced, tri-state reply presented as B's proposal, rubric versioning added - Change 5; rubric inventory per Change 7 -->
### The grader and its rubric

- **Agent.** `finding-grader` is promoted from `~/.claude/agents/` into `src/superclaude/agents/` and generalised: lens-neutral wording, the rubric arrives in the batch, reply keys come from the rubric header. It stays read-restricted (`tools: Read`, `permissionMode: plan`, "do not read any file", `finding-grader.md:4-12`). The shipped file pins `model: sonnet` (`finding-grader.md:5`); the Agent tool's `model` parameter overrides the pin among the Anthropic aliases, but whether it reaches non-Anthropic model classes is UNVERIFIED (Round 2 B fact G5), and E2's reviewer set includes sonnet, so independence from a sonnet reviewer needs the override.
- **Independence.** The grader is class-disjoint from every reviewer in the panel (its `model_class` differs from theirs) and, where the environment allows, vendor-disjoint. When the disjoint set is empty (the anthropic-only case, `research/05` section 12) the run records `grader_diversity: degraded`. This applies class-disjointness to the decider and not to the finders, as the C04 resolution recommends (S4 C04). Same-vendor models judge alike (X7), so "degraded" is a recorded weakness, not a fix.
- **Rubrics as data.** One frozen rubric file per lens under `src/superclaude/cli/review/data/rubrics/` (the directory that already holds the panel JSON files). The file's sha256 is recorded in the ledger at round 1 and later rounds refuse a different hash, as stoprule does ("a change is a new version and starts a new loop", `rubric.md:1`). A rubric change, including a change of the reply format, is therefore a new version.

| Lens | Rubric | What it decides | Notes |
|---|---|---|---|
| `spec` (document loop, tasklist review) | `spec-v2`, new: stoprule B1-B3 plus the reply rule below and the claim-shape precondition. The live stoprule rubric is `spec-v1` (B1-B3 verbatim); it stays as it is | `grade` (`blocking`, `not_blocking`, `undecidable`); agreement and lateness are never reasons (`rubric.md:13-14`) | The v2 categories `contradiction`, `unpassable-check`, `data-loss` and `safety` already map to B3 kinds (a), (c), (e) (`findings.py:15-22`); kinds (b) and (d) have no category and the grader judges them from the claim. Shadow data collected under `spec-v1` measures a rubric that will not ship (INV-015) |
| `reflect-post` | none: a code predicate decides (see "Reflect-post: code predicate") | the deviation class is proposed by reviewers and read by code | Reflect-post already has a code path (`findings_v2.py:161-162`, `contract.py:377-381`); no grader proposes the class there |
| `reflect-pre` | not decided: whether a rubric ships, and who authors it, is an owner decision | n/a | reflect-pre has no ground truth; the contract's deviation counts are UC-2 only (`SKILL.md:753-759`, `research/05` section 13.1) |
| future (PR review, rf-qa replacement) | one file each | per the consumer's tier or definition | No core change; each declares a lens, a rubric and a gate strength |

**Rubric inventory after this merge.** Only `spec-v2` and its canary file ship in the first build. `reflect-post-v1` is dropped. Whether `reflect-pre-v1` ships is NOT decided by the debate.

<!-- Source: Base (original, modified) - the X-006 outcome replaces "fail-closed by construction"; the tri-state reply is Advocate B's proposal; INV-008 and INV-021 printed - Change 5 -->
#### Reply contract: what was agreed, what is proposed, what is open

- **Agreed (X-006, HYBRID 78%).** The grader may demote only with a named failed criterion (B1, B2 or B3). On doubt the reviewer's flag stands or the row goes to PENDING. "Fail-closed by construction", the base's claim, is replaced by **fail-closed on procedure only**: a missing, malformed or rejected reply never yields PASS, but on meaning the shipped agent fails open (`finding-grader.md:17`: "Otherwise it is not blocking"), and the rubric default in Risks R5 says so.
- **Proposed by Advocate B, not agreed as a contract (Round 2 concession 4).** A tri-state reply: `blocking` true, false or `undecidable`; `false` names the failed criterion; `undecidable` on a reviewer-flagged cluster keeps the reviewer's flag or goes to PENDING; on an unflagged candidate it means no promotion. It needs a new rubric version (`spec-v2`).
- **Open (the probe found these and the debate did not resolve them).**
  - INV-008 (MEDIUM): a tri-state reply is a schema change, not a rubric edit. `parse_grader_reply` and `evaluate_reply` require a boolean (`stoprule.py:808-830`), `finding-grader.md:29-35` states the boolean schema, and "name B1/B2/B3" must fit inside the 25-word `why`. These files serve the live stoprule command, so a tri-state reply is a fork of them. The selector for `undecidable` (reviewer flag stands, or PENDING) is not agreed.
  - INV-021 (HIGH): the named criterion is checked by format only (a `why` of at most 25 words, `stoprule.py:813`), not for truth. B2 is ungradable on v1 inputs unless a claim names a reader and a wrong result, or the finding gains an `outcome` field (v1 findings have no `outcome`; findings-v2 has none either; `findings_v2.py:111` and `findings.py:118` allow a 300-character claim with no enforced named reader). Variant B's advocate conceded the precondition; it is not in the consensus list. Without it the grader arm collapses toward the veto.

<!-- Source: Base (original, modified) - "What each consumer does" with the v1 correction, reflect-post code predicate and rubric inventory - Change 7 -->
### What each consumer does

- **Document review loop (spec-panel, ledger).** `review merge` gains a mode `--decide flag|grader` (default `flag` until the gate passes). In `grader` mode `merge_round` stores candidate rows with `blocking: null` and returns verdict PENDING; `grade prep` and `grade apply` fill the grades; `ledger verdict` prints the final verdict. Today `merge_round` sets row blocking from member flags at `ledger.py:187` and `ledger.py:213-218`; in `grader` mode those two lines read the stored grade instead. The base said `_brief_ids` (`ledger.py:99-104`) and the verdict line (`ledger.py:274`) need no change because they read the row's `blocking`; the debate corrected this: an undecided row has `blocking: None`, so it is absent from `_brief_ids`, and `defer()` can turn a PENDING round into PASS unless it recomputes PENDING (Round 2 B fact G2; see "Certification").
- **Tasklist review.** Uses the `spec` lens, because the E2 tasklist study ran the spec review brief as shipped (S4 C16 table, E2 row). A tasklist rubric is added only if the benchmark shows `spec-v2` needs it. The E2 evidence transfers only to this lens (A-001).
- **Reflect Tier 2.** Contract 1.8.0 is frozen and the debate stays the merge (C11). Reflect-post decides by a code predicate (see "Reflect-post: code predicate"); the grade stage, for the spec and tasklist lens only, runs after the debate on `clusters_kept` and writes its grades to the nested `telemetry:` block, which the lint does not inspect (`research/07` section 2.3, line 113). The panel `blocking_any` stays shadow telemetry that "never routes anything" (`SKILL.md:345`). The verdict is still derived from the contract as today. Authority passes to the grader only through a new `merge_method` value and a contract bump, after C05 selects it and a paired legacy-versus-panel run exists (G-57).
- **Code-driven Tier 2 engine behind the tasklist post gate (`ensemble.py`).** Where the grade stage plugs in depends on C17 and is not decided here. The engine sets `merge_method` from the reviewer count and defaults its deviation flags to clean (`research/07` section 8a, line 410). Variant A's reading is that this blocking gate cannot currently fail on drift or regression because no producer fills the counts (`ensemble.py:442-471,779-785`) [VIA research/09 and 13]; the debate did not verify it.

<!-- Source: Base (original, modified) - Rollout; step 0 prerequisites added, the replay gate written with Advocate A's concessions and the probe's limits kept visible - Change 15 (C-013, B at 71%; C-012, OPEN at 71%; S-005, B) -->
### Rollout

The grader is staged, and the veto stays the live rule until a lens passes the gate. Both advocates agreed on this shape (C-001, S-005). The replay below is the only measurement the proposal plans, and it does not suffice to decide: see "What the gate does not settle".

0. **Prerequisites, before any shadow data counts.**
   - D1, D5 and D6 are fixed first, for both arms of the replay (C-012). "D1 fixed" is not defined yet. If it means persisting `rejected_lines[]` and marking the reviewer partial, a lone reviewer's rejected blocking finding is lost while two other valid blocks still certify. If it means raising the 200-character limit, the recovered findings (mostly from the models with the weakest verbatim fidelity, `CR:292`, `CR:294`) fail the locate gate and are suppressed there. Unless shown otherwise the two cancel (INV-014).
   - The claim-shape fix (a claim names a reader and a wrong result, or the finding gains an `outcome` field) and `spec-v2` land before shadow starts. Shadow data collected earlier measures a rubric that will not ship (INV-015), and B2 is ungradable without the claim shape (INV-021).
1. **Shadow.** Promote the agent, the `spec-v2` rubric and its canaries; run the grade stage with grades recorded and the veto still deciding. Shadow data stays out of the merged report and out of the exit code (INV-018).
2. **Replay (the gate).** See below.
3. **Flip `--decide grader` per lens**, starting with singleton blockers (the first population graded, C-004), only for a lens whose replay passed. The default stays `flag` otherwise.
4. **Reflect authority** only with the contract bump and a paired legacy-versus-panel run (G-57).

**The replay gate (C-013, B at 71%).** A paired, pre-registered, pooled replay on the E2 packages:
- Veto and grader run on the same candidate sets, with D1, D5 and D6 fixed first for both arms. Both arms are scored against `blocking_in_implement` (Advocate A's condition: the grader's rubric asks whether a reader gets a wrong outcome, and nobody has shown it closes the 27 over-graded catches, EC3). Where grader-blocking and implement-blocking disagree is reported.
- The pass condition is written before the run: the grader's wrong blockers on the control package are below the veto's on the same candidate sets, at no loss of real-blocking recall on the defect-rich packages. "Pooled" means the 71 valid-era rows are compared together and recall is a paired comparison over the 38 real catches.
- The known E2 wrong blockers are added as a leniency probe, and the grader's true-negative rate on them is reported. Canary sets and benchmark sets are disjoint.
- An inconclusive result keeps the grader in shadow and the veto live.
- "Same candidate sets" breaks wherever D1 changes the set (INV-014, INV-022).

**What the gate does not settle (all UNADDRESSED).**
1. No numeric pass threshold exists in either variant or in the debate. A grader that always demotes meets the criterion above: the control package has no known blocking defect, so any demotion lowers its wrong-blocker count, and the recall side lives on a floor of 0.17 to 1.20 of 8 per run that cannot show a loss (INV-019). The threshold is an owner decision.
2. Power is low. The control package is one document with two defects and n of 4 to 6 per panel; the 71 pooled rows are not independent; some rows were merged from stale or replaced reports, so the replay population shrinks below 71. Advocate B's own R1 residual predicts an inconclusive result, which keeps the veto live indefinitely (INV-022).
3. The replay never runs `apply_revision`, `defer`, the re-found and regressed paths or the clear step, which is where C-006 lives. It cannot validate certification, frozen grades or clearing (INV-020).
4. Shadow counts measure disagreement and not correctness: production loops have no ground truth (INV-023).
5. Shadow data collected before `spec-v2` and the claim-shape fix measures a rubric that will not ship (INV-015).
6. The E2 reports are findings-v1; whether their anchors are usable by the renderer is unverified, and re-running the E2 judge to match grader-blocking rows to ground truth is not costed.

<!-- Source: Base (original, modified) - How it works; two data-flow variants and the adapter subsection added - Change 8 -->
## How it works

Items marked (new) do not exist today. Everything else is existing code read for this proposal; the `[READ]` tags in "Evidence" are inherited from the variant authors, and the Round 2 facts F1 to F7 and G1 to G6 in the debate transcript are the debate's re-verification.

<!-- Source: Base (original, modified) - the v2 flow is the base's; the v1 flow was added - Change 8 -->
### Data flow (one round)

The document loop runs on the v1 `findings` module (`ledger.py:15,165,187`, `merge_cmd.py:109`); the v2 path runs on `cluster.py` (`cluster.py:375`). Variant B's candidate rule and `verify-citations` exist only on v2. Both advocates verified this in Round 2 (F1, G1). Two variants of the flow follow.

**v2 path (clusters; reflect and any v2 consumer).**

```
reviewer cards (findings-v2)
  -> superclaude review cluster <cards> --snapshot <input-snapshot.yaml> [--calibration ...] --out <out>   -> panel/clusters.json
  -> superclaude review verify-citations --cards ... --snapshot ... --root <repo> --out <out>             -> panel/precheck.json
  -> evidence-validator (existing agent; the named resolver)                                              -> kept finding ids
  -> superclaude review cluster ... --kept <ids> --out <out>                                              -> panel/clusters_kept.json
  -> superclaude review grade prep   --clusters panel/clusters_kept.json --precheck panel/precheck.json     (new)
        --lens <spec> --rubric <path> --canaries <path> --root <repo> --out <out>
        prints one block per batch (=== BATCH Bn === ... === END BATCH Bn ===)
  -> one finding-grader Agent call per batch, all in one message (parallel)
  -> superclaude review grade apply  --out <out> --batch Bn --reply <file>                                  (new)   -> panel/decisions.json
  -> verdict from the grades (reflect: telemetry block only; the contract verdict is unchanged)
```

Steps 1-4 are existing commands (`cluster_cmd.py:96-197`, `verify_cmd.py:76`).

**v1 path (ledger rows; the document loop).**

```
reviewer reports (findings-v1 blocks)
  -> superclaude review merge [--decide flag|grader]    (merge_cmd.py:21-70; new flag)
        merge_round -> fnd.cluster -> ledger rows {claim, anchor, span, blocking, members[]}
  -> superclaude review grade prep    (new; v1 adapter: reads ledger rows instead of clusters_kept.json)
        candidate = blocking or severity in {MAJOR, CRITICAL}     (no channel test)
        pre-check = anchor_status == "missing"  (span is None)
  -> one finding-grader Agent call per batch, all in one message (parallel)
  -> superclaude review grade apply                                   (new)  -> row["grade"], row["blocking"]
  -> superclaude review ledger verdict
```

In `--decide grader` mode `merge_round` stores candidate rows with `blocking: null`; in `--decide flag` mode (the default) nothing changes.

<!-- Source: Variant A Design step 6 and Round 2 A F1, Variant B G1 - merged per Change 8; adapter estimate is an advocate estimate -->
### Adapters and the two copies of the rule

The grade stage needs two input adapters, ledger rows (v1) and `clusters_kept.json` (v2). Advocate B conceded the adapter and estimated it at **50 to 100 lines plus a second renderer plus a parity test across both paths `[estimate; Advocate B, not measured]`** (C-015, A-007).

- **Candidate rule, v1:** `blocking or severity in {MAJOR, CRITICAL}`, no channel test.
- **Pre-check, v1:** `anchor_status == "missing"` (`span is None`).
- **Renderer, v1:** reads the row's `claim`, its `anchor` and the document text at `span`. It must be blind in the same way as the v2 renderer: it never receives reviewer ids, model names, severity or the `blocking` flag.
- **Two copies of the rule to edit.** `row.blocking` at `ledger.py:187` (v1) and `blocking_any` at `cluster.py:375` (v2). Under `--decide grader` both must read the stored grade. A parity test must span both copies.
- **More copies outside the core (INV-017, MEDIUM).** `diffgate.py:796` (`verdict = "FAIL" if open_blocking else "PASS"`, in the installed `sc-diffgate` skill) and the claim-level FAIL rule in `stoprule.py:1179-1191`. `review_ledger.py` in `sc-review-ledger` exists; its rule was not confirmed. Whether those commands are in scope for the unified core is not decided (see "Owner decisions"); if they are out of scope, the parity test cannot cover them.
- **INV-011 (HIGH), kept visible.** One `representative` claim per v2 cluster is graded (`cluster.py:338-344,373-374`); a v1 row takes the claim of `group[0]`, which depends on reviewer order (`ledger.py:182-199`). `same_defect` merges by a shared fingerprint (`findings.py:367-372`) even when the claims differ, so a `false` on the representative demotes every member, including a distinct defect, and a frozen grade then keeps it. "Tighten `same_defect`" has no mechanism, no test and no acceptance number. The D6 fix covers the 83 chained rows only (A-007).

<!-- Source: Base (original, modified) - the unverified-evidence rule (Change 6), the v1 renderer and an owner-decision pointer (Changes 8 and 18) were added -->
### What the grader sees and does not see

Modelled on `render_batch` (`stoprule.py:721-766`), which gives the grader the rubric and, per claim, the quote, span, outcome and evidence, and never the reviewer's grade label.

| Shown to the grader | Never shown |
|---|---|
| the frozen rubric text for the lens | reviewer ids, model names, `model_class`, vendors |
| per item: opaque id `Cn`, the claim (at most 300 characters, `findings_v2.py:111`), each cited location and the text the script re-read there, evidence tagged `[verified]` or `[unverified]` | the reviewer's severity, `blocking` flag or `deviation_class` |
| in a re-review: the baseline text of the changed hunk (`stoprule.py:708-718`) | `support`, `reviewers`, overlap, `disputed`, panel or run names, file paths that encode a combo |
| two canary items (one blocking, one minor), shuffled in | anything outside the batch: the agent is told not to read files (`finding-grader.md:12`) |

The right-hand column carries a lesson from E2: its judge was blind to reviewer ids but not to the panel name, because the judge schema contained the combo name (`research/11` section 2, `judge-one.sh:21`). Blindness is enforced by construction (the renderer never receives those fields) and checked by a test, for BOTH the v1 and the v2 renderer.

The script, not the reviewer, re-reads the cited lines, so the grader judges the text itself and B1 ("a verbatim quote") is checked mechanically: a quote that `verify-citations` could not find in the cited lines (`verify_cmd.py:68-72`) is tagged `[unverified]`. An item whose only support is `[unverified]` evidence is never graded `blocking`; the grader must say in `why` which evidence it relied on (`finding-grader.md:18-19` says the shipped agent grades unverified evidence as if it were true, which is the base's defect, C-007). How many lines of cited text are shown per citation, and the cap on citations per item, are owner decisions (see "Owner decisions").

<!-- Source: Base (original, modified) - the reflect-post `class` key was removed (Change 7); the canary caveats from INV-010 were added (Change 5) -->
### Reply, validation and failure handling

- **Reply.** Exactly one JSON line per item, `{"cid","blocking","q2","why"}` with `why` at most 25 words (`finding-grader.md:26-35`, `stoprule.py:789-816`). The core maps the reply to the item's `grade`. Under Advocate B's proposal `blocking` gains the third value `undecidable` (a schema change, INV-008; see "The grader and its rubric"). The accepted key set comes from the rubric header; any other key set rejects the batch.
- **Batch rejection.** A batch is rejected as a whole when a line is malformed, a `cid` is missing or repeated, or either canary is graded wrongly (`stoprule.py:819-830`). The first rejection asks for one rerun; the second leaves the batch's items `unconfirmed` (`stoprule.py:872-880`). The raw reply and its sha256 are stored with the attempt either way (`stoprule.py:849-871`).
- **What the canaries do and do not test.** They catch a grader that ignores the rubric on an easy item. They do not catch a grader that is merely lenient on real items. `build_batches` adds exactly two canaries per batch whatever its size, and the canary choice is seeded per batch (`stoprule.py:665-692`), so a rerun likely meets the same canaries, and one wrong canary rejects every real claim in the batch (`:826-829`), which two rejections turn into `unconfirmed` for the whole batch (INV-010, MEDIUM).
- `unconfirmed` and not-yet-graded candidates both keep the verdict away from PASS. `grade apply` refuses a batch that is already graded, so a grade is written once.

<!-- Source: Base (original, modified) merged with Variant A contract-fields table; `decision` renamed `grade`, `class` renamed `model_class` - Change 9 (C-010), Change 19 -->
### Contract fields

`panel/decisions.json` (schema id `review-decisions/1`, new; the file and schema names keep the base's word "decisions", and the outcome in each entry is a `grade`, never a ledger `decision`). Fields from Variant B, with the grader outcome renamed `grade` and the model class renamed `model_class`:

| Field | Meaning |
|---|---|
| `lens`, `rubric_id`, `rubric_sha256` | which frozen rubric produced the grade |
| `grader` | `{agent, model_requested, model_served, model_class, vendor, diversity: full or degraded}`; the served model is recorded because all three efforts hit served-model drift (`research/11` section 11, Key Takeaways) |
| `batches[]` | `{id, attempt, state: graded, rejected or unconfirmed, reply_sha256, reason}` |
| `clusters{cid}` | `{candidate_reasons[], grade: blocking, not_blocking, undecidable or unconfirmed, q2, why, veto: {blocking_any, blocking_all}, support, disputed, reviewers[], relation: agreed, overruled or promoted}` |
| `summary` | `{candidates, graded, unconfirmed, blocking, overruled, promoted, dropped_unfounded, singleton_blockers}` |

`overruled` means a reviewer flagged the cluster blocking and the grader did not; `promoted` means no reviewer flagged it and the grader did. Both are counted, never silent (the "no silent blocking rejection" check that C07 already asks for). Both measure disagreement and not correctness (INV-023).

Fields from Variant A and the interim path:

| Field | Where | Status |
|---|---|---|
| `blocking` (reviewer's flag) | finding | unchanged |
| `blocking_effective` | finding, written by the core | new (C16); recorded next to the reviewer's flag, so the disagreement rate can be reported |
| `anchor_status`, `rejected_lines[]`, `partial` | finding, reviewer | from C02 and C15 |
| `blocking_any`, `blocking_all`, `reviewers`, `support`, `disputed`, `chained`, `uncalibrated` | cluster | existing, unchanged |
| `singleton_blockers` | cluster summary and telemetry | new, one integer, read by no verdict rule |
| `degraded` | merge result, round record, report line before `verdict:` | new boolean: true when fewer than two reviewers had a valid block at round 1; inherited (see "Certification") |
| `confidence: overlap/single` | ledger row | existing, display only |
| `contract_version`, `merge_method`, every stable reflect key | reflect `return-contract.yaml` | unchanged (1.8.0); panel-only values live in the nested `telemetry:` block that lint rule L2 does not inspect |

**In a ledger.** Each graded row stores `row["grade"]` (frozen together with the rubric hash) and `row["blocking"] = (grade == "blocking")`. A re-found row keeps its grade unless its cited text changed (C-006, B at 63%, narrowed to rows whose text did not change: a revision that touches the span flips the row to `regressed` on any re-find, `ledger.py:235`). Under the live veto a re-found row still takes the current round's flag (`ledger.py:210-218`; pinned at `test_review_ledger.py:518-544`), so the frozen grade helps only after the flip (INV-001, HIGH).

**Open points on these fields.**
- INV-002 (MEDIUM): the ledger schema string `review-ledger/1` (`ledger.py:17`, `load` at `:47`) accepts any ledger; loops in flight at rollout have rows with no grade and rounds with no flag; `degraded` can be derived from `block_ok`, but grades and the rubric hash cannot; "later rounds refuse a different hash" would strand a loop that started in shadow when `spec-v2` ships. No default for a row without a grade and no ledger version bump is specified (Owner decisions).
- INV-018 (LOW): the merged report is read by the next reviewer and the reviser (`ledger.py:408-411`), so shadow data must stay out of `render_merged_report` and out of the exit code. No rule says so yet.

<!-- Source: Base (original, modified) - grade replaces decision; the undecidable line and the v1 reference were added - Changes 3, 5 and 19 -->
### Verdict logic

In the order a unit test would pin it. This is the `--decide grader` form; under `--decide flag` the verdict is today's.

```
candidates = candidate rule for the path (v2: channel == defect and (blocking_any or max severity in {MAJOR, CRITICAL}); v1: see Adapters)
if any candidate has no grade or grade == unconfirmed:  verdict PENDING   (decision word PENDING, exit 12, never PASS)
elif any candidate has grade == blocking:               verdict FAIL      (decision REVISE, or ESCALATE at the cap)
else:                                                   verdict PASS      (with degraded: true when certification failed at round 1)
# grade == undecidable: the selector is not agreed (reviewer's flag stands, or PENDING); see Owner decisions
```

`PENDING` with exit 12 is the optional state C19 allows and the experiment ledger already uses (`review_ledger.py:63` per `research/02` section 6.1). `ledger_cmd.py:13` today maps PASS, REVISE and ESCALATE to 0, 10 and 11. Stoprule reports unconfirmed or pending claims as FAIL `incomplete` (`stoprule.py:1185-1189`), not as a new exit code, so "PENDING mirrors stoprule" is only approximate; it also means a waiting state advances a stoprule loop and does not advance this one (INV-007).

<!-- Source: Base (original, modified) - "Reflect-post: from decision to contract" replaced by a code predicate and the two-rule note - Change 7; INV-016 -->
### Reflect-post: code predicate

No grader proposes the deviation class in reflect-post: reflect-post already has a code path. Two different rules are both called "the predicate" in the sources, and they must not be treated as one:

| Rule | Where | Blocks when | Notes |
|---|---|---|---|
| Label rule | `findings_v2.py:155-162` | every MAJOR or CRITICAL finding that carries a `reflect_category` is blocking, whatever its `deviation_class` | `reflect_category` is optional (`findings_v2.py:155-156`), so the predicate needs a fallback |
| Halting rule | `contract.py:377-381` | halts only on regression or drift counts; authorized and necessary deviations never halt | the contract reads `deviation_count_by_class` from the debate and defaults it to 0 when absent (`contract.py:90-101`, `ensemble.py:779-785`) |

A MAJOR authorized finding is blocking under the first rule and passes the second. Which rule applies is an owner decision (INV-016, MEDIUM; see "Owner decisions"). Two further owner decisions sit inside the halting rule: whether MINOR drift halts (`contract.py:380-381` against `findings_v2.py:107-108`; G-03), and who produces `unauthorized_deviation_present` (no producer rule exists, `SKILL.md:854`, `research/05` section 2.3; G-04). Evidence-sourced facts reach the contract through the existing deterministic path: a Regression is set by the exit-code taxonomy and real-boot evidence, not by assignment (`SKILL.md:1117`, `research/05` section 2.1).

<!-- Source: Base (original, modified) - exit 12 with the EXIT_BY_DECISION entry, `degraded` as a field and report line - Change 9 (C-010) -->
### CLI surface (summary)

| Command | Status |
|---|---|
| `review cluster`, `review verify-citations`, `review merge`, `review ledger verdict` | existing |
| `review merge --decide flag\|grader` (default `flag` until the gate passes) | new flag |
| `review grade prep`, `review grade apply`, `review grade status` | new |
| `review ledger verdict` exit codes | existing 0, 10, 11 unchanged. New values: `degraded` (a field and a report line, no new exit code) and `PENDING` (exit 12, only under `--decide grader`). Both places must change for PENDING: the `EXIT_BY_DECISION` entry (`ledger_cmd.py:13`) and the exit call (`ledger_cmd.py:109`) |

<!-- Source: Base (original, modified) - Evidence tables A-E kept with their source columns; a Counter-reading column added to every table from Variant A E-1 to E-17 and from the debate; tags extended - Change 10 (S-003, EQUAL) -->
## Evidence

**Key.** `R01`-`R13` are files under `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/research/` (R05 = `05-blocking-calibration.md`, R02 = `02-ledger-merge-verdict.md`, R07 = `07-reflect-merge-contract.md`, R10 = `10-future-consumers.md`, R11 = `11-evaluation-evidence.md`, R12 = `12-test-pins-regression.md`); `web-01` and `web-03` are the web research files in the same folder; S4 is `synthesis/synth-04-options-conflicts.md`. Code paths are relative to the repository root. The research-file tags `R01`-`R13` (two digits) are not the risk rows R1-R22 of "Risks and mitigations". `CR` is `COMBO-REPORT.md`, `PR` is `PILOT-REPORT.md` and `AD` is `analysis/audits/audit-D/summary.md`, all under the E2 folder.

**Tags.** **[READ]**: the variant author read the cited lines; this merge did not re-read them (the debate re-verified the items its Round 2 "Facts verified" lists). **[VIA Rnn]**, **[VIA audit-D]**, **[VIA research/09 and 13]**: the fact comes from that file and nobody re-read the underlying source. **[E2 4a22d74]**: read with `git show 4a22d74213f93837d00c2c314075dd967b9a98e3:.dev/eval-workspaces/tasklist-review-panel/20261111-a1/<file>`. **[external]**: outside the repository, with a URL. **[advocate-computed, not re-aggregated]**: a number one debate advocate computed from `COMBO-REPORT.md` rows; the orchestrator did not re-aggregate it. **[estimate]**: a size or cost the author did not measure.

**Counter-reading column.** Variant A argued each fact inline (its items E-1 to E-17). The merged text keeps the source column and moves that argument here, so a reader sees the claim, where it came from, and the other reading of the same fact. A counter-reading marked "debate" is a correction both advocates agreed. None of the counter-readings changes the fact in the row.

<!-- Source: Base (original, modified) - Counter-reading column added from Variant A E-1 to E-14; V7 corrected; V10 and V11 added from Variant A - Change 10 -->
### A. The veto and its measured failure

| # | Claim | Source | Counter-reading |
|---|---|---|---|
| V1 | A new row blocks when any member blocks (`ledger.py:187`); a re-found row takes the current report's classification, so one non-blocking re-report un-blocks it (`ledger.py:213-218`); the Reviser brief is the blocking open or regressed rows (`ledger.py:99-104`); the verdict is FAIL while the brief is non-empty (`ledger.py:274`); `_confidence` ("overlap" or "single", `ledger.py:86-90`) is computed but `_decision` (`ledger.py:93-96`) never reads it. At cluster level `blocking_any` is the veto (`cluster.py:46-47`, `cluster.py:375-376`) and `disputed` routes nothing | [READ] | Variant A E-1: the veto is what master and `cluster_v2` do, and it does it faithfully: the merge replayed over 264 E2 merges had 0 row or verdict inconsistencies (AD:9, AD:33). Debate: `ledger.py:187` runs on v1 groups and `cluster.py:375` on v2 clusters; they are two copies (Adapters) |
| V2 | Over 71 valid-era rows the judge counted 65 blocking catches and only 38 were real blocking defects; "ember + 2x luna 1.00 judge-blocking is 0.17 real" | `CR:291` [E2 4a22d74] | Variant A E-3: the 27 extra catches are real ground-truth defects that a blocking-flagged row matched and that did not block implementation (`gt_covered_blocking` "can include defects that are not blocking_in_implement", CR:291), a severity over-grade, not an invented defect. Rows with no ground-truth match are counted separately as wrong blockers. The judge was told the panel name and had no `source.md` (`research/11` section 2 on `judge-one.sh:12-21`) [VIA R11]. Scoring also counts a novel real finding as a wrong blocker (`PR` "Stated limits"; CR:63). Debate X-003: see EC3 |
| V3 | `2x luna + 2x ember` had 2.75-3.25 more wrong blockers than every comparator (permutation p 0.005-0.03); the same panel's table row shows 1.75 of 14 found, 0.25 real blocking and 4.75 wrong blockers; runs are n=4-6 per panel over three packages | `CR:298` and the "AS SCORED" table [E2 4a22d74] | Variant A E-2 and E-6: replicated panels of two to five reviewers range from 0.25 to 4.75 wrong blockers per run on the two defect-rich packages, most between 1.8 and 3.5, and from 0.25 to 1.75 on the control package (CR:315-333); `ember + luna` (two reviewers) sits at 2.00 (CR:317), so it is not only a panel-size effect; between replicated panels no difference in found, real blocking, wrong blockers or control (p 0.54-1.0), only tokens differ (p 0.002-0.009, CR:381). The four-reviewer panel is the only wrong-blocker result that survived audit. Debate X-004: see EC2 |
| V4 | Caveats stated by E2: ground truth scores novel real finds as wrong blockers, so wrong-blocker counts on defect-rich packages are an upper bound; the control package is the cleaner signal | `CR:63`, `:75`; `PR:79` [E2 4a22d74] | Applies to every reading of V2 and V3. The control package has two defects and no blocking defect, so it is also a small sample (INV-019, INV-022) |
| V5 | The veto gives no recall guarantee: all three pilot arms had 0 of 8 real blocking recall and "Single-reviewer Arm A passed both defect-rich packages" | `PR:71` [E2 4a22d74] | Variant A E-4: recall is already the binding constraint: replicated panels found 0.17 to 1.20 of the 8 real blocking defects per run (CR:315-333); single-run rows that reached 2 or 3 of 8 were never replicated (CR:306-314, CR:370). An earlier section (CR:60) says five combinations returned PASS on `designSpec`; CR:289 says the final section supersedes earlier tables, so CR:60 is direction only. Variant A's further step, that no other decider can add recall, is dropped (X-001) |
| V6 | A few defects carry most catches: B3 in 95 of 106 runs, I8 in 76, I2 in 71 | `CR:502` [E2 4a22d74] | Variant A E-9: a quorum can therefore remove real singletons (S4 line 326) [VIA S4]. Same direction as the row |
| V7 (corrected, see EC1) | The merge code is faithful to its rules (0 invariant violations over 264 merges), so a merge bug is excluded. That does not exclude the input defects D1, D5 and D6, and it does not establish that the wrong blockers are a policy outcome. Audit D's own check lists "0 violations ... apart from the dropped-finding effect" (D1) | `research/05` section 11, citing `research/scope/01-other-branch-study.md:128` [VIA R05; DOC-SOURCED]; D1 in `CR:291-292` [E2 4a22d74] | Variant A E-5: E2's rows were produced under D1, D5, D6 and source blindness (156 of 665 valid-era runs never referenced `source.md`, CR:373; CR:293 says 161 and is corrected by CR:373). Debate X-002 (agreed-open): D1 pushes counted wrong blockers down; D5 and D6 may push them either way (the direction was not agreed); attribution was not measured by anyone |
| V8 | In 13 shadow runs (modification times 2026-11-12 22:22 to 2026-11-13 02:42 UTC): 142 findings, 16 reviewer-blocking, 42 MAJOR of which 26 were `blocking: false`; a blind calibrator's number was higher on blocking findings (mean 0.80 against 0.66) but with no ground truth that is an association | `research/05` section 5.3 [VIA R05, run files] | Variant A E-8: no decider other than the veto has any ground truth: "No ground truth exists for quorum, calibrated weighting, the grader or the debate" (S4 line 372) [VIA S4]. The 0.80 versus 0.66 comparison is n=16 versus 126 |
| V9 | Three blocking rules coexist: each reviewer applies the consequence rule to its own findings (`spec-panel.md:259`, `document_review_loop_prompts.md:31`), the label rule in code applies only with `reflect_category` (`findings_v2.py:161-162` [READ]), and reflect halts by deviation class (`contract.py:377-381` [READ]). The parser enforces only that a MINOR finding cannot block (`findings_v2.py:107-108` [READ]) | `research/05` sections 10 and 13 [VIA R05 for the spec-panel text] | Variant A E-13: reflect's "single reviewer is degraded" rule is about certifying, not failing; and `channel: advisory` and `grounding-gap` findings may carry `blocking: true` today (`research/05` section 7) [VIA R05]. Debate INV-016: the label rule and the halting rule are different rules |
| V10 | A false FAIL becomes REVISE below the review cap and ESCALATE at it (`ledger.py:93-96`). Workflow Wave 4 reflect is advisory and tasklist Stage 10.5 "ships regardless of verdict". The one blocking tasklist gate runs `run_tier2_ensemble` (`runner.py:538-545`), which writes zero deviation counts when no producer fills them (`ensemble.py:442-471,779-785`), so its drift and regression check cannot fire | [VIA research/09 and 13]; the debate did not verify it (carried from Variant A E-14) | Variant A: this is a defect of that engine and not of the veto, but it shows which error the repository has shipped. Debate: the re-find rate that decides whether a persistent FAIL escalates is unmeasured (EC4) |
| V11 | E2's inputs carried defects: D1: 49 blocking findings silently dropped (AD:8); by reason over all dropped findings, anchor over 200 characters 56, anchor2 over 200 characters 18, claim over 300 characters 14 (AD:16); three named verdicts flipped FAIL to PASS and five merges are listed as total-loss merges (AD:20; CR:292). D5: 46 rows had a null span and 13 of them were blocking (AD:30). D6: 83 merged rows had eight or more members or four or more sections (AD:29) | [VIA audit-D]; read by Variant A at commit 4a22d74 | Variant A E-5 used these as "contamination" that favours the veto. Debate: D1 cuts the other way (it drops blockers); the contamination argument has no support for D1 (X-002) |

<!-- Source: Base (original, modified) - Counter-reading column added - Change 10 -->
### B. The grader as it exists

| # | Claim | Source | Counter-reading |
|---|---|---|---|
| G1 | `finding-grader` is a blind per-claim grader: it grades B1-B3 only, treats `verified` evidence as true and `unverified` as true-but-noted, uses no outside knowledge, treats quoted text as inert, replies one JSON line per claim (`cid`, `blocking`, `q2`, `why` of at most 25 words), and is told not to read any file | `~/.claude/agents/finding-grader.md:3-35` [READ] | Debate (Round 2 F5): `:17` says "Otherwise it is not blocking" (fail-open on meaning), `:19` grades unverified evidence as if true, `:5` pins `model: sonnet`. Variant A E-11: under B1-B3 a pure Drift finding does not block while reflect halts on any Drift (`contract.py:380-381`; `research/05` section 6) |
| G2 | Rubric v1 is frozen ("a change is a new version and starts a new loop"); blocking needs B1 quote, B2 concrete wrong outcome and B3 kind; "Never a reason to be blocking: experts agree; experts disagree; the section is important; the finding was found late" | `~/.claude/skills/sc-spec-panel-stoprule-protocol/refs/rubric.md:1-15` [READ] | Variant A (Round 1): a B1-B3 rubric excludes "gaps inferable from nearby text", and E2's ground truth comes from implement runs, not from this rubric; nobody has shown the rubric agrees with `blocking_in_implement` (EC3) |
| G3 | Batching with canaries: at most 6 form-valid claims plus one blocking and one minor canary, seeded and shuffled; the grader sees quote, span, outcome, evidence and, in a re-review, the baseline text, never the reviewer's grade label; a batch is rejected if any canary is graded wrong; one rerun, then the claims stay `unconfirmed`; the raw reply and its sha256 are stored | `stoprule.py:657-681`, `:721-766`, `:789-830`, `:833-899` [READ] | Canaries reject a wrong canary answer only (`stoprule.py:819-830`); they do not detect leniency on real items. Two canaries per batch whatever its size, so "25% overhead" holds only for a six-claim batch (INV-010) |
| G4 | `canaries.json` holds 8 canaries (4 blocking, 4 minor) with keys `answer`, `evidence`, `outcome`, `quote`, `span` | `~/.claude/skills/sc-spec-panel-stoprule-protocol/refs/canaries.json` [READ via `jq`] | The canaries are easy items; no harshness probe exists beyond them (INV-019) |
| G5 | The stoprule verdict is FAIL `confirmed`, `unresolved-prior` or `incomplete` (unconfirmed or pending claims, uncovered hunks, unsealed ledger), and "silence never passes" without a valid PASS-time audit | `stoprule.py:1162-1205`, `:1185-1189` [VIA R02 section 7.1] | Stoprule counts a waiting claim as FAIL `incomplete`, which advances its loop; PENDING under `--decide grader` does not advance this one (INV-007) |
| G6 | The grader, stoprule and rubric are installed only under `~/.claude/` and in the phase-5 bundle, not under `src/` | R05 section 6; R02 section 7 and its Stale Documentation note [VIA R05, R02] | Variant A E-11: same fact, cited as a cost of Option D; this proposal budgets the promotion (Cost) |
| G7 | In the one live stoprule trial, review 1 sealed 8 claims and the grader classed 6 blocking and 2 minor; the trial was then invalidated because the transcript-integrity verifier could not read asynchronous grader replies, which the report calls "a transport/provenance failure, not evidence for or against reduced defects" | `.dev/experiments/346-validation/phase5/FINAL-REPORT.md:106`, `:162` [READ; E3, 2026-11-08/09] | Debate (Round 2 G6, search not exhaustive): no scoring of the grader, or of any blind per-claim grader, against ground truth was found; the trial carries no accuracy information |
| G8 | The same report: "None of the completed, measured loops reached a clean PASS. None of the five proposed variants has a valid, repeated convergence result"; and one final review had "six MAJOR labels but four blocking grades, demonstrating why the two measures must not be substituted for one another" | `FINAL-REPORT.md:75`, `:109` [READ; E3] | Same direction as the claim: the six-versus-four gap shows a label and a grade differ; it does not show which is right |

<!-- Source: Base (original, modified) - Counter-reading column added - Change 10 -->
### C. Fit with today's code

| # | Claim | Source | Counter-reading |
|---|---|---|---|
| K1 | findings-v2 already carries what a grader batch needs: `claim` of at most 300 characters, 1-8 citations with optional quotes, `channel` (defect, grounding-gap, advisory), `deviation_class`, and categories `contradiction`, `unpassable-check`, `data-loss`, `safety`, `missing-requirement`, `other` | `findings_v2.py:111`, `:128`, `:140-153`, `:184-186`; `findings.py:15-22` [READ] | Debate (Round 2 B G1, F4): this describes v2. The document loop's v1 findings have `id, severity, blocking, category, anchor (12-200 chars), anchor2, refs, claim (<=300)` and no `channel`, citations, `deviation_class` or `outcome` (`findings.py:90-121`). Neither version has an `outcome` field, so B2 is graded from a 300-character claim with no enforced named reader (INV-021) |
| K2 | `verify-citations` is a model-free pre-check that flags missing-file, out-of-range and quote-not-found and writes a re-read set | `verify_cmd.py:1-13`, `:42-73` [READ] | It reads v2 cards only (`verify_cmd.py:1`); the v1 loop has no equivalent resolver (INV-005, INV-025). `verify_cmd.py:1-13` calls a quote-not-found "advisory, not proof" (Variant A Round 1) |
| K3 | `review cluster` writes `panel/clusters.json` or, with `--kept`, `panel/clusters_kept.json`, each cluster with `reviewers`, `support`, `disputed`, `blocking_any`, `blocking_all`, `chained`, `representative`, `claim` | `cluster_cmd.py:96-197`; `cluster.py:323-378` [READ] | One `representative` claim per cluster is what a grader would see and a frozen grade would then cover for every member (INV-011) |
| K4 | `review merge` is a single call that merges and computes the verdict; `ledger verdict` exits 0, 10 or 11 | `merge_cmd.py:21-118`; `ledger_cmd.py:13`, `:94-109` [READ] | `ledger_cmd.py:13` indexes `EXIT_BY_DECISION[v["decision"]]`, so a PENDING decision raises a `KeyError` until the dict gains it (Round 2 B new evidence) |
| K5 | The evidence-validator is a mandatory gate on the reflect report and re-reads every `file:line` citation; unfounded items are dropped, not downgraded | `SKILL.md:35`, `:635` [READ by grep] | It is a reflect gate, not a step of the v1 document loop, which has no re-read resolver (INV-005) |
| K6 | The experiment ledger already computes blocking from a profile predicate (`PROFILES`, one entry), freezes decided fields, and refuses a fourth review; it has no multi-reviewer merge | `review_ledger.py:41-59`, `:1592-1606`, `:1300-1311` [VIA R02 section 6.1] | It is one more place where a blocking rule lives; whether its rule is in scope for a unified core is undecided (INV-017) |

<!-- Source: Base (original, modified) - Counter-reading column added from Variant A E-13, E-16 - Change 10 -->
### D. Constraints from reflect

| # | Claim | Source | Counter-reading |
|---|---|---|---|
| F1 | Reflect treats a single-reviewer merge as DEGRADED, degrades a T2 convergence score below 0.80, and halts on any regression or drift count | `contract.py:295-296`, `:317-326`, `:377-381` [READ] | Variant A E-13: the degrade rule is about certifying, not failing; it is the precedent for the asymmetric verdict (Certification) |
| F2 | Contract 1.8.0 forbids reflect from synthesising its own merge (`SKILL.md:837`); `panel_lint` treats a new `merge_method` value or top-level key as a bump; `merge_method: panel` and contract 1.9.0 are pinned as failing; a major bump blocks the wrapper; the nested `telemetry:` block is not inspected by the lint | R07 sections 1.6, 2.3 (line 113), 3, 4.2 (`test_f2_merge_method_panel_fails`, `test_f3_f4_contract_version`) [VIA R07] | Variant A E-16: the legal `merge_method` values are exactly `adversarial` and `single-reviewer-fallback`, the lint is 1.8.0-only and a new stable key or value trips lint rules L2, L3 and bump rule B (`panel_lint.py:184-185`); the interim hardened veto needs no new stable field |
| F3 | A third merge path, `ensemble.py`, sets `merge_method` from the reviewer count and defaults deviation flags to clean | R07 section 8a, line 410 [VIA R07] | See V10: the post gate cannot currently fail on drift (carried from Variant A, not verified) |
| F4 | The calibrator cannot be the decider as built: `confidence-calibrator.md` implements six troubleshoot dimensions with a gated-minimum formula against reflect's five-dimension mean, returns one number per card, produced 0 of 689 per-finding numbers in legacy runs and 142 of 142 in shadow runs once the brief asked for them; calibrated `C` routes tiers, not findings | R05 sections 2.4, 4, 5 [VIA R05] | Variant A E-10: same direction; under `anthropic-only` the class-disjoint calibrator is always `degraded` (R05 section 12); verbalized confidence separates right from wrong answers weakly (AUROC about 62.7% for GPT-4) and is top-skewed, so no threshold is portable [external; via `research/web-03` sections 5.1 and 5.5] |
| F5 | Debate evidence: convergence was 1.0 in 9 of 14 recorded runs, 6 of 14 merges were judged inline by the orchestrator, and shadow09 had no debate artifacts | R07 section 7; S4 C05 evidence (line 375) [VIA R07] | Variant A E-12: under any option the debate is untouched for reflect (C11); this proposal depends on it neither way |

<!-- Source: Base (original, modified) - Counter-reading column added; X11 added from Variant A E-9 - Change 10 -->
### E. External sources (outside the repository)

Every item is external. None of them tested the project's current model set, and none studied defect-finding panels for specifications or plans (`web-03` section 6.5; `web-01` lines 132-133).

| # | Claim | URL and reliability | Counter-reading |
|---|---|---|---|
| X1 | Union voting reached 82.7% recall at 85.0% false-positive rate against 37.7% recall for weighted voting (vulnerability detection, direction transfers, magnitude does not) | https://arxiv.org/html/2602.17875v1 (preprint; figures taken from a search snippet per `web-01` line 21) | Variant A E-15: weighted voting is 37.7% recall at 35.3% false-positive rate; the source treats the false-positive rate as the main deployment constraint for CI gating, so it supports the recall side of the veto and the precision side of its critics |
| X2 | LLM validators confirm far more than they reject (true-positive rate above 96%, true-negative rate typically below 25%); a minority veto tuned on human labels was the best rule | https://arxiv.org/html/2510.11822v2 (preprint; Python feedback validity, not review) | Variant A E-11: a missing vote must not default to an answer. The "minority veto was best" result is the one external point that favours keeping a veto-type rule |
| X3 | Debate amplified judge biases after the first round; a meta-judge was more resistant | https://arxiv.org/html/2505.19477v3 (EMNLP 2025 Findings; snippets, bias not accuracy) | Variant A E-12: same point; under every option the reflect debate is untouched |
| X4 | Production review systems separate finders from a coordinator that deduplicates, verifies against source and applies a severity rubric before anything blocks | https://blog.cloudflare.com/ai-code-review and https://www.linkedin.com/blog/engineering/ai/high-signal-ai-code-review-that-adapts-to-your-codebase-at-scale (vendor blogs, no error rates) | Variant A E-15: Cloudflare's coordinator, not the reviewers, applies the rubric and states a bias toward approval. That argues against the veto and is listed for that reason |
| X5 | 56.8% of confirmed defects were found by exactly one of fifteen model versions, so a hard quorum would drop real defects; LinkedIn verifies singletons rather than dropping them | https://zenodo.org/records/21328807 (self-published, not peer reviewed; abstract only) and the LinkedIn post above | Variant A E-9: 167 of 294 defects; coverage rose from about 47% with one reviewer to about 72% with a second (single-organization corpus, reliability low to medium). Singleton handling is where external sources disagree: Cursor drops them, LinkedIn verifies them |
| X6 | Self-preference and label effects: models favour their own output via self-recognition; a 2026 reanalysis attributes about 89.6% of measured self-preference to judge uncertainty on hard items; author labels and filenames shift scores | https://proceedings.neurips.cc/paper_files/paper/2024/file/7f1f0218e45f5414c79c0679633e47bc-Paper-Conference.pdf (peer reviewed, 2023-era models); https://arxiv.org/abs/2601.22548 (preprint, summary figures); https://arxiv.org/html/2611.01829v1 (single-author preprint, Nov 2026) | Variant A Risk 2: in the spec lens each reviewer grades its own finding, the regime that produced the 27 over-graded catches; nothing shows a grader would not carry its own bias |
| X7 | Anthropic models' judgments are highly correlated and cross-provider ensembles calibrate better, so vendor diversity is a stronger guarantee than `model_class` diversity | https://www.apolloresearch.ai/monitoring/evaluating-llm-calibration-for-coding-agent-monitoring (vendor research blog; date not shown) | Variant A Risk 5: extra reviewers may add correlated wrong blockers, so the veto does not get independent votes from a larger panel |
| X8 | Verbalized numeric confidence is overconfident and weakly discriminative; a model is up to 26% more confident in an answer presented as its own | https://arxiv.org/abs/2306.13063 (ICLR 2024); https://arxiv.org/abs/2603.29559 (preprint); https://arxiv.org/abs/2606.03437 (preprint, open-weight models only) | Variant A E-10: AUROC about 62.7% for GPT-4 and top-skewed confidence, so no threshold is portable |
| X9 | Rubric option and criterion order shifts scores in a model-specific direction; a few random permutations remove most of it | https://arxiv.org/abs/2602.02219 (preprint, abstract read) | none recorded by Variant A or the debate |
| X10 | A panel of three diverse smaller judges beat one large judge on agreement with humans (answer-correctness scoring) | https://arxiv.org/abs/2404.18796 (preprint, 2024 models); this counts against a single grader, see Risks R4 | none recorded by Variant A or the debate |
| X11 | Nine judges behaved like about two independent votes and the best single judge matched or beat the panel | https://arxiv.org/html/2605.29800v1 (preprint, natural-language-inference tasks, not code review) [external; via `research/web-01` section 2.2] | Variant A E-9: a 2-of-3 quorum buys less independence than it appears to; the same point limits any panel's votes, the veto's included |

<!-- Source: Debate record - corrections both advocates conceded (X-002, X-003, X-004, C-005, C-012, C-006), Round 2 A concessions 2-4 and B concessions 1-2 - Change 10 -->
### Evidence corrections

Both advocates conceded the claims below. Each correction is applied to the rows above and to the Correctness argument.

| # | Correction | What it replaces | Status |
|---|---|---|---|
| EC1 (X-002, C-012) | V7 names D1 (49 dropped blocking findings, four FAIL-to-PASS flips, `CR:291-292` [E2 4a22d74]). D1 pushes counted wrong blockers down. D5 (13 null-span blocking rows `[VIA audit-D]`) and D6 (83 chained rows) may push them either way. Attribution of the wrong blockers to the veto versus these defects is unmeasured | The base's V7, which omitted D1 and read "faithful merge" as "policy outcome, not a code bug" | Agreed-open (X-002, C-012) |
| EC2 (X-004, C-005) | P1 becomes: the grader's false-block rate PER CANDIDATE is independent of reviewer count by construction (a larger panel can still produce more candidates); E2 neither supports nor refutes a size effect. Variant A's cap as a precision lever is dropped. The cap is written once, as "cost cap only; precision effect open (C-005)" | "E2 measured that direction" (P1) and Variant A's E-7 cap | Agreed (X-004 to Variant A's side); C-005 agreed-open |
| EC3 (X-003) | The 27 extra catches are real ground-truth defects graded blocking that did not block implementation (the definition at `CR:291`). Wrong blockers (rows with no ground-truth match) are a different measure; nobody mapped one onto the other. The gate is judged against implement-blocking, and where grader-blocking and implement-blocking disagree is reported | The reading that the 65-versus-38 gap is the veto inventing defects, and Variant A's step that "FAIL is the right verdict" on a defect-rich plan | HYBRID (67%) |
| EC4 (C-006) | Frozen grades matter only for rows whose cited text did not change. Whether a persistent FAIL escalates depends on how often a reviewer re-finds the row (a re-find sets `regressed`, `ledger.py:235`; a revised wrong blocker clears only if not re-found, `ledger.py:254-257`). That re-find rate was measured by nobody | Variant A's refutation of the escalation argument; B's R1 reading of the frozen grade | Agreed (B at 63%, narrowed) |
| EC5 (U-004) | The error-cost facts in V10 are carried as `[VIA research/09 and 13]`, not as read facts | Variant A's `[CODE]`/`[DOC]` mix for E-14 | Kept, unverified |
| EC6 | Judge limits: the E2 judge saw the panel name and had no `source.md` [VIA R11]; novel real finds count as wrong blockers (V4). Wrong-blocker counts on defect-rich packages are upper bounds | n/a (made explicit) | Agreed |

**Control-package wrong blockers per run, by panel size.** Both tables are `[advocate-computed, not re-aggregated]` from `COMBO-REPORT.md` rows 306-337 and were not re-aggregated by the orchestrator; they disagree in detail and agree that there is no size effect on the control package.

| Panel size | Advocate B, full table, weighted by run count | Advocate B, audit-clean subset | Advocate A, selected rows |
|---|---|---|---|
| 1 | 1.00 | 1.00 | not given |
| 2 | 1.27 | 1.46 | 1.33 (rows 315: 1.25, 317: 1.50, 336: 1.25) |
| 3 | 1.05 | 1.06 | 1.21 (rows 331: 0.83, 320: 1.00, 333: 1.20, 323: 1.40, 319: 1.60) |
| 4 | 1.33 | 1.17 | 1.50 (row 332) |
| 5 | 0.89 | 1.00 | 1.75 (row 316) and 0.25 (row 318); the mean 1.00 is Advocate B's computation |

Further advocate-computed points: on the defect-rich packages the single-reviewer rows have the highest wrong-blocker counts (sol 3.00, terra 4.00) `[advocate-computed, not re-aggregated]`; `ember + sonnet` 0.25 is the defect-rich figure and its control figure is 1.25 (CR:315); the default panel `ember + luna + luna` shows 0.17 real blocking, 1.83 wrong blockers on the defect-rich packages and 0.83 on the control (n=6, CR:331 [E2 4a22d74]).

<!-- Source: Base (original, modified) - Correctness argument; P1 and P4 rewritten, P5 narrowed; Variant A steps 3-5 and 8 folded in; A steps 1 and 2 deleted - Change 11 -->
## Correctness argument

The argument is structural plus the E2 measurements. It is not a measured win for the grader, and it says so where it matters. Each step names the evidence it rests on and a falsifier; "What this argument does not establish" lists the open invariants that the argument runs into.

**P1. The grader's per-candidate false-block rate does not depend on reviewer count, by construction.** Call a cluster spurious when no real blocking defect sits behind it. Under the veto, a spurious cluster blocks when any member is flagged, so with n reviewers that each over-flag it with probability q the chance it blocks is 1 - (1 - q)^n, which rises with n. Under a grader the chance that a spurious candidate blocks is the grader's false-block rate g, fixed by the rubric and the batch and independent of n. More reviewers add candidates (cost) and can still produce more candidates; they do not raise the per-candidate chance of a wrong block. The formula is a model and not an E2 finding: reviewer flags are not independent in practice (X7, X11), and **E2 neither supports nor refutes a size effect** (EC2: control wrong blockers are flat by panel size). Assumptions: the grader's output depends only on the rendered batch (true by construction, checked by a test), and batch position effects are controlled by seeded shuffling (X9). What would falsify P1: on the E2 control package the grader's wrong-blocker count is not lower than the veto's on the same candidate sets. That falsifier is necessary and not sufficient: a grader that demotes everything meets it (INV-019).

**P2. Recall is the union's recall, minus the grader's misses.** The candidate rule admits every flagged cluster and every MAJOR or CRITICAL cluster, singletons included (X5, V6). The veto's claim to maximum recall is a property of candidate generation, and the grader keeps that generator unchanged. A grader cannot find a defect no reviewer reported, and does not claim to: the pilot's 0 of 8 real blocking recall under the veto (V5) is a candidate-generation question that C14 leaves open. The grader's recall risk is a false negative, which the canaries do not measure (they reject a grader that ignores the rubric on an easy item) and the replay can measure only within the limits in "Rollout". Real-blocking recall is already low (0.17 to 1.20 of 8 per run for replicated panels), so a floor that low cannot show a loss.

**P3. The decider is not the finder.** Today each reviewer applies the consequence rule to its own findings (V9), and the merge takes the union of those self-grades. Separating the roles is the production pattern (X4), and the self-preference literature gives a mechanism for why self-grading inflates (X6, X8). The grader runs in a fresh context, sees the finding as external input, is class-disjoint and vendor-disjoint where the environment allows, and has no access to who or how many found it. That transfer from the literature to these models is extrapolation: the studies use 2023-2026 models and none tested a defect-finding panel (`web-03` section 6.5).

**P4. Fail-closed on procedure only, and auditable.** These properties are code, not model behaviour, and each has a unit test:
- PASS requires every candidate graded; a rejected or missing reply leaves the verdict at PENDING under `--decide grader` (approximately mirrors `stoprule.py:1174-1189`, which reports FAIL `incomplete` instead of a new exit code).
- Each grade is stored once with the rubric hash and the reply hash. A re-found row keeps its grade when its cited text did not change (EC4). That closes the "one non-blocking re-report clears a row" path (V1) only after the flip: under the live veto a re-found row still takes the current round's flag (`ledger.py:210-218`), so one non-blocking re-report still clears it (INV-001).
- A grader that ignores the rubric on a canary rejects the batch (G3). Canaries do not catch leniency on real items (INV-010).
- The veto is recorded on every cluster next to the grade, so every run yields a paired veto-versus-grader record and `overruled` and `promoted` counts. That is a record of disagreement; it does not show which decider is right, because production loops have no ground truth (INV-023).

On meaning the design is not fail-closed: the shipped agent grades "not blocking" when it cannot decide (`finding-grader.md:17`) and grades unverified evidence as if true (`:19`). The agreed fix is the demotion rule (X-006) plus the evidence gate (C-007), whose open points are INV-008, INV-021, INV-005, INV-006 and INV-025.

**P5. Policy consistency with reflect.** Reflect-post decides by a code predicate, and the grader never overrides evidence-sourced regressions; under contract 1.8.0 the grader writes only to the nested `telemetry:` block while the debate stays the merge (F2). The existing degrade rules for a single-reviewer merge and for convergence below 0.80 (F1) keep applying. Adopting the grader cannot weaken reflect's gate without a deliberate contract bump. Which of the two "predicates" applies in reflect-post is not decided (INV-016).

**P6. The costs of the two errors are unequal in this repository (Variant A step 4).** A false FAIL becomes REVISE below the review cap and ESCALATE at it (`ledger.py:93-96`), and two of the three tasklist review points are advisory (V10). A false PASS ships a plan, and the single-reviewer pilot arm did exactly that on both defect-rich packages (V5). The one blocking tasklist gate in production cannot currently fail on drift or regression (V10 `[VIA research/09 and 13]`, unverified). The limit of this step: whether a persistent FAIL escalates depends on how often a reviewer re-finds the row, and that rate is unmeasured (EC4, Advocate B Round 2).

<!-- Source: Variant A, Correctness steps 3 and 5 - merged per Change 11; step 3 limited by INV-001 -->
### Properties of the interim rule (Variant A steps 3 and 5)

- Within one round, adding a reviewer with a valid block can only add blocking rows, and every FAIL traces to a named finding with a quote and a span, because the Reviser brief is the list of those rows (`ledger.py:99-104`, `:274`); the merge replayed over 264 E2 merges showed 0 inconsistencies (V1). Across rounds this does not hold under the live rule: a re-found row takes the current round's flag, and one reviewer's non-blocking re-report removes it (V1, INV-001).
- The PASS side is corroborated. A single-reviewer merge is degraded, never a certified PASS (`contract.py:295-296`), and so is a convergence score below 0.80 (`contract.py:317-326`). Variant A's asymmetric verdict agrees with both: one reviewer may fail a plan, two valid reviewers are needed to certify one (see "Certification"). INV-004 and INV-024 limit what "certified" means.

<!-- Source: Base (original, modified) - "Why D over the other deciders" with Variant A E-9 to E-12 evidence and the EC1 correction on the veto row - Change 11 -->
### Why a staged grader over the other deciders

| Option | Why not it as the live rule, on the evidence |
|---|---|
| A veto (hardened) | Measured failure, with a cause that is not established (EC1: the merge code is faithful, which excludes a merge bug and not the input defects D1, D5 and D6; V2, V3, V5). The veto stays as candidate generator, as control, and as the rule that runs until a lens passes the gate. Its precision claim is a prediction (see below) |
| B quorum | The stoprule rubric states that agreement is never a reason to block (G2); most confirmed defects are found by one reviewer (X5, V6), so a hard quorum removes real singletons; a 2-of-3 quorum buys less independence than it appears to (X11); no ground truth exists for any k (`research/05` section 14) |
| C calibrator-weighted | Its formula keeps the reviewer flag as a necessary condition and adds a threshold with no evidence; the agent is a six-dimension troubleshoot grader with no reflect rubric override, produced 0 of 689 legacy numbers, and numeric verbalized confidence is weakly discriminative (F4, X8, V8) |
| E debate | Convergence carried no information beyond the cluster number in recorded runs and 6 of 14 merges were inline (F5); debate amplified judge bias in the one external study (X3); it does not serve ledger consumers (S4 C05 Option E). In reflect it stays as the merge and the grader composes with it |

<!-- Source: Variant A, Correctness step 8 and Base (original) "Weakest point", with INV-001, INV-006, INV-019, INV-020 added - merged per Change 11 -->
### What this argument does not establish

This is Variant A's step 8, stated for both options.

**For the hardened veto.** It does not show that the veto's precision is acceptable. E2 is the only ground-truth evidence on any decider and it is unfavourable on precision. The claim that hardening the inputs lowers wrong blockers enough is a prediction: D1 pushes counted wrong blockers down, so fixing it likely raises them (EC1); only D5 could push them the other way, and nobody measured either. It is falsifiable with data the repository owns (rerun the three E2 packages with the hardened core); the pass condition needs an owner-set number (Owner decisions).

**For the grader.** Nothing measures the grader's accuracy. The case rests on the veto's measured failure (whose cause is open, EC1) and on the structure of the alternative. The external evidence says LLM validators are agreeable (true-negative rate below 25% in one study, X2), and a grader that rubber-stamps would turn the design into the veto plus a model call and a false sense of independence. Canaries catch a grader that ignores the rubric; they do not catch a grader that is lenient on real items. The one live stoprule trial that ran the grader (6 of 8 claims graded blocking, G7) was invalidated for a transport reason and carries no accuracy information; the only loop-level report shows no variant reached a clean PASS (G8). The grader is therefore adopted behind a gate, not on trust.

**What the probe found that this argument runs into** (all UNADDRESSED):
- INV-001 (HIGH): under the live veto a re-found row still takes the current round's flag (`ledger.py:210-218`), so the frozen grade helps only after the flip.
- INV-006 (MEDIUM): an absence defect fixed elsewhere leaves the row `named_not_touched` (`ledger.py:330-339`), and a frozen grade then ends the loop in ESCALATE.
- INV-019 (HIGH): a grader that always demotes would pass the replay's control-package criterion.
- INV-020 (HIGH): the replay never runs the rounds-2-and-3 code (`apply_revision`, `defer`, re-found and regressed paths, the clear step) where C-006 lives.
- INV-011 (HIGH): one representative claim per cluster is graded and then frozen for every member.
- INV-021 (HIGH) and INV-023 (HIGH): the named criterion is checked by format only and B2 may be ungradable; shadow counts measure disagreement, not correctness.

<!-- Source: Base (original, modified) - Risks table R1-R11 kept, columns Likelihood basis and Consequence added, Variant A risks 1-8 carried in as R12-R18, debate risks R19-R22 added - Change 12 (S-004) -->
## Risks and mitigations

A row counts as a risk with a likelihood basis when it gives a measured rate, count, frequency or rating plus its consequence. Where nobody recorded one, the cell says "no basis recorded". Risks R1 to R11 come from Variant B, R12 to R18 from Variant A, R19 to R22 from the debate.

| # | Risk | Likelihood basis | Consequence | Mitigation | Residual |
|---|---|---|---|---|---|
| R1 | **Grader accuracy is unmeasured and validators are agreeable** (X2) | External: validator true-negative rate typically below 25% (X2); the one live trial carries no accuracy information (G7); no measurement in the repository | A lenient grader equals the veto at higher cost, with a false sense of independence | Gate authority on a paired, pre-registered replay (see "Rollout" for the gate and what it does not settle). Pre-register the pass condition before running, as the E3 fixed screen did (`research/11` section 11). Keep canary and benchmark sets disjoint. Run a small bias battery (swap item order, pad claims, rename paths) before trusting it (`web-03` Recommendation 4) | The E2 replay has 3 packages and 16 defects with n=4-6 per panel (V3), so it can fail to separate the two; an inconclusive result keeps the grader in shadow and the veto live (INV-022); a grader that always demotes meets the control criterion (INV-019); the replay never runs rounds 2 and 3 (INV-020). Whether the E2 reviewer reports carry anchors the renderer can use (they are findings-v1) is not verified |
| R2 | **Rubric mismatch**: B1-B3 is spec-specific; under B1-B3 a pure Drift finding does not block while reflect halts on any Drift (`research/05` section 6) | 1 rubric, 1 lens that E2 covered (A-001); no basis recorded for a rate | A rubric used on the wrong lens misclassifies; policy could change silently | One rubric per lens that ships (`spec-v2` only in the first build); reflect-post uses a code predicate, so the mismatch does not arise there; policy changes are new rubric versions | Two different rules are both called "the predicate" (INV-016); two owner decisions remain (G-03 MINOR drift; G-04 `unauthorized_deviation_present`); `SKILL.md:1196` and `deviation-taxonomy.md:123` disagree on whether static unreachability is a Regression (`research/05` section 3.2; G-05) |
| R3 | **Independence is weakest where C03 is undecided**: in the anthropic-only environment the class-disjoint set is empty (`research/05` section 12) and same-vendor models judge alike (X7) | no basis recorded: no source quantifies the cost for blocking decisions | The grader shares a vendor with the reviewers | Record `grader_diversity: degraded` per run; resolve the grader with `--hard-exclude-class` so a disjoint grader is used whenever one exists; report the shadow gate per environment, since E2 ran on one gateway | The cost of degraded diversity is unmeasured |
| R4 | **One grader per batch** (X10, X2) | External only: three diverse small judges beat one large judge on one task (X10); no basis recorded in the repository | A single decider is a single point of error | Not in the first build. If the replay shows a true-negative problem, add a second vendor-disjoint grader and block only on agreement, at double grader cost | Until then, a single point of error |
| R5 | **The grader is blind to context**: B3's "a requirement the spec calls core" and many consequence calls need more than a quote | no basis recorded | A case that cannot be decided from the batch is graded not blocking by the shipped default (`finding-grader.md:17`), which can drop a real blocker | The script re-reads the cited lines; evidence entries may carry the requirement text; the demotion rule (X-006) turns "cannot decide" into `undecidable`, which keeps the reviewer's flag or goes to PENDING | The selector for `undecidable` is not agreed (INV-008); B2 may be ungradable on v1 claims (INV-021); the named criterion is checked by format only |
| R6 | **Transport and provenance fragility**: the only live trial was invalidated because a transcript verifier could not read asynchronous grader replies (G7) | 1 live trial, invalidated | An invalidated grading run | `grade apply` works on the reply text in a file and records its sha256 and attempt; it does not parse transcripts. Failure is `unconfirmed`, never PASS | A reply file written by the orchestrator is self-attested (the same weakness as EV-1, `research/07` section 7.5); canaries raise the cost of fabrication but do not prevent it |
| R7 | **Extra serial step and cost per round** | 42 MAJOR findings in 13 shadow runs, about 3 per run before clustering (V8), which is usually one batch; no grader token count measured anywhere (G7) | One more model round-trip per round; collateral rejection when a canary fails (INV-010) | At most 6 candidates plus 2 canaries per batch; batches run in parallel in one message; MINOR-only clusters are not sent | Cost per round is unmeasured (see "Cost"); a singleton-first batch is 1 claim plus 2 canaries (INV-010) |
| R8 | **Candidates the reviewers marked "Medium" (MAJOR, `blocking: false`) now reach the grader**, so the grader may grade as blocking findings the brief tells reviewers to list as follow-ups | 26 of 42 MAJOR findings in 13 shadow runs were `blocking: false` (V8) | Promotions are new blockers with no precision data | `promoted` is counted only and cannot raise a FAIL in shadow (C-003); `spec-v2` applies the same consequence test as the brief | Promotion precision is part of the replay measurement, which has the limits in R1 and INV-023 |
| R9 | **Reflect needs a contract bump to give the grader authority** (F2), rated XL in S4 (C11 Option B) | S4 effort rating XL | Until the bump, the reflect decider is unchanged | This proposal stops short of it: reflect gets telemetry-only grading under 1.8.0 until a paired legacy-versus-panel run exists (G-57) | The grader is advisory in reflect until the bump |
| R10 | **Quoted text is attacker-controlled input** (a reviewed document can contain instructions) | no basis recorded | A document could steer the grader | The grader's instructions mark quotes inert (`finding-grader.md:21`), tools are restricted, replies are schema-checked | The restriction is prose plus plan mode; whether an empty tool list is supported by the agent format was not checked |
| R11 | **Rubric presentation order biases scores** (X9) | External preprint only (X9) | Scores shift in a model-specific direction | Freeze the rubric content and permute the order of criteria per batch with the seeded generator; a test pins that content is identical | The effect on a conjunction rubric (B1 and B2 and B3) is unmeasured; an extrapolation from a preprint |
| R12 | **The spec lens still lets the reviewer grade its own findings** (Variant A Risk 2) | 27 of the 65 judge-blocking catches were over-graded real defects (V2, EC3) | The over-grade regime continues until a grader goes live | Record `blocking` (reviewer) next to `blocking_effective` (core) per finding and report their disagreement rate in telemetry; keep the brief's "write the consequence sentence" requirement (`document_review_loop_prompts.md:31`) | Nobody has shown a grader closes the 27 |
| R13 | **One reviewer can also clear a row** (Variant A Risk 3) | Pinned behaviour: `ledger.py:213-218` with `test_review_ledger.py:518-544`; the default re-review is one reviewer (`document_review_loop_prompts.md:70`); the rate at which this happens was measured by nobody | A real blocker is cleared by one non-blocking re-report on the live path | D2 (an invalid or partial reviewer never clears a row) is a prerequisite; whether later rounds re-find or only verify is C13; the frozen grade closes it only after the flip | INV-001 (HIGH): the pre-flip live path keeps the hole |
| R14 | **Promotion of the veto or the grader into reflect's verdict would halt on any one reviewer's Drift** (Variant A Risk 4) | `contract.py:377-381` halts on any Drift or Regression count | A single reviewer's drift finding would halt if the debate were replaced | Nothing is promoted: the debate stays (C11), the panel stays shadow telemetry, authority waits for the replay and a contract bump | Two owner decisions are open (G-03, G-04); the reflect-authority bump needs its own decision |
| R15 | **A panel of different models is not a panel of independent votes** (Variant A Risk 5) | External: nine judges behave like about two independent votes (X11) | Extra reviewers may add correlated wrong blockers | Cap at three finders as a cost cap only (C-005), declare replicas (C04), and report each reviewer's blockers that no other reviewer shares | The cap's precision effect is open (C-005) |
| R16 | **The evidence is thin on both sides** (Variant A Risk 6) | 3 packages, 16 ground-truth defects, n of 4 to 6 per panel, one gateway on 2026-11-11 to 2026-11-13, one judge pass per row whose variance was not measured, a judge that saw the panel name | Every claim in this document, the ones favouring either variant included, rests on a small sample | C20's portable benchmark with panel-blind labels and a source-aware judge brief | Not built; owner for the benchmark port is open (G-59) |
| R17 | **The PASS rule adds degraded outcomes** (Variant A Risk 7) | 80 reviewer-level invalid-block cases in E2 under the v1 rule (`CR:292`); three existing tests assert a one-reviewer round-1 PASS (see Test coverage) | A round with fewer than two valid blocks can no longer return a certified PASS | C15's per-line policy keeps valid lines, so a reviewer with one bad line still has a valid block; the outcome is marked degraded and can be re-run; the one-reviewer fallback keeps working | INV-009 (MEDIUM): `block_ok` is false on any bad line, and two same-model reviewers count as two blocks because dedup is by id only (`ledger.py:119-121`); the replay is not told to report the degrade rate. INV-004 and INV-024 are open |
| R18 | **Chained clusters could carry a blocker** (Variant A Risk 8) | 83 merged rows with eight or more members or four or more sections in E2 (D6) | One blocking member colours a large cluster | `chained` is reported; C12's complete-link admission and its acceptance metric cover it | INV-011 (HIGH): the grader sees one representative claim per cluster |
| R19 | **The v1 adapter is uncosted in the base** | `[estimate]` 50 to 100 lines plus a second renderer plus a parity test (Advocate B; not measured) | The document loop cannot use the grade stage without it | Cost it (see "Cost"); a parity test spans the v1 and v2 copies of the rule | The estimate is unmeasured; at least two more copies exist outside the core (INV-017) |
| R20 | **`defer()` and PENDING**: undecided rows carry `blocking: None`, so they are absent from the brief and `defer()` turns a PENDING round into PASS (`ledger.py:356-360`); `ledger_cmd.py:13` raises `KeyError` for a PENDING decision | Code facts verified by Advocate B (Round 2 B fact G2) and by the probe | A round with undecided candidates could pass | `defer()` recomputes PENDING and `degraded`; an `EXIT_BY_DECISION` entry for PENDING | INV-007 (MEDIUM): PENDING has no mapping at the review cap |
| R21 | **The shipped grader agent pins `model: sonnet`** (`finding-grader.md:5`) and E2's reviewer set includes sonnet | Code fact (Round 2 B fact G5; also row G1) | Independence from a sonnet reviewer is lost unless overridden | The Agent tool's `model` parameter overrides the pin among Anthropic aliases | Whether the override reaches non-Anthropic classes is UNVERIFIED (also whether the Agent tool honours `model:` inside a worker) |
| R22 | **The replay can be passed by an always-demoting grader** | The control package has 0 known blocking defects, so any demotion lowers its wrong-blocker count (INV-019); no numeric pass threshold exists | The gate could pass a grader that never blocks | A negative-control test with an always-demote grader and a leniency probe (the known E2 wrong blockers) are proposed (not agreed in the debate) | INV-019 (HIGH) is unaddressed; the numeric threshold is an owner decision |

<!-- Source: Base (original, modified) - existing-tests table corrected with Variant A's accounting (Round 2 A F2) and 16 new-test groups extended; Variant A items 4-8 folded in - Change 13 (C-014 and S-006, HYBRID) -->
## Test coverage needed

C-014 ended HYBRID (65%) and S-006 HYBRID (63%): the new-test groups of Variant B plus Variant A's rule-parity and monotonicity tests, with the accounting corrected in Round 2 (F2). Line numbers below are the ones the variants and the plan cite; this merge did not re-read the test files.

<!-- Source: Base (original, modified) with Variant A items 1-3 and the Round 2 accounting (F2) - Change 13 -->
### Existing tests that change or stay

The `--decide flag` default keeps today's behaviour, so most existing tests stay green until the default flips (Rollout step 3). Variant A's list kept `:279-300` green while also changing `:296-298`, which lies inside that range; the table below replaces both variants' lists.

| Test | What it pins | Change |
|---|---|---|
| `tests/review/test_review_ledger.py:128-129` (`brief_ids == ["L1","L2","L4"]`), `:518-544` (`test_refound_as_nonblocking_stops_failing_the_review`) | blocking rows come from member flags; one non-blocking re-report un-blocks a row (`research/12` line 317) | stay green under `--decide flag`; add a `grader`-mode twin whose blocking rows come from stored grades and a test with the opposite outcome for a re-found row whose cited text did not change |
| `test_review_ledger.py:376-385` and `:408-417` | D2/D3 (invalid reviewer, one valid block) and D5 (a missing anchor stays blocking; `:417` asserts `blocking is True`) | change under the prerequisites: `:376-385` last assertion becomes `resolved_check` (D2); `:417` becomes effective-blocking false until verified (evidence gate) |
| `test_review_ledger.py:299-304` | exact dict equality on `verdict()` | breaks only if `verdict()` gains a key, so the `degraded` key goes elsewhere (round record and report line) |
| `test_review_ledger.py:296-298`, `:307-315`, `:396-403`, `:468-472` | one-reviewer round-1 PASS and `defer` pins (`:296-298` tuple compare, `:307-315` key access, `:396-403` keys on `verdict()` after `defer`); `:468-472` asserts `splitlines()[-1] == "verdict: PASS"` | gain a `degraded` assertion; the degraded note goes before the last line; `defer` also recomputes PENDING under `--decide grader` |
| `tests/review/test_review_cli.py:328-348` | round trip, exit codes; `:348` asserts exit 0 and `decision == "PASS"` | assertions unchanged; add an assertion on `degraded`; add `--decide` and exit 12 |
| `tests/review/test_review_cluster.py:514-550` (`test_blocking_any_all_and_disputed`) | `blocking_any`, `blocking_all`, `disputed` | unchanged: the grade stage adds keys and removes none. Not checked: whether any test compares a whole cluster dict |
| `tests/cli/reflect/test_panel_contract_lint.py`, `test_shadow_skill_contract.py` | contract 1.8.0, `merge_method`, no new top-level key (`research/07` section 4) | unchanged in Rollout steps 1-3 because grades go in `telemetry:`. At the authority bump: rewrite `test_f2_merge_method_panel_fails` (`:184-190`), `test_f3_f4_contract_version` (`:193-201`), the byte-identical block test (`test_shadow_skill_contract.py:42-49`) and the `"1.8.0"` constants in `reflect_shadow_exit.py` and `reflect_verdict_replay.py` (`research/07` section 6) |
| `tests/skills/test_primitive_dual_surface_lookup.py` and the `grep -rn 'src/superclaude'` rule in `CLAUDE.md` | installed primitives must not name `src/superclaude/` paths | the promoted agent file must pass; whether an agent-inventory test exists was not checked |
| `tests/review/test_review_rules_text.py` | pins rules text (not read) | only if `document_review_loop_prompts.md:31` is edited so the reviewer's grading line says its flag is an input; not needed while the default is `flag` |

<!-- Source: Base (original, modified) tests 1-16; Variant A tests 4-8 as 17-23; invariant probe tests 24-27 (not agreed in the debate) - Change 13 -->
### New tests

Variant B's groups 1-16 with two adjustments (the blindness test covers BOTH the v1 and the v2 renderer; the reflect-post parity group becomes a test of the code predicate in "Reflect-post: code predicate"; the grader-selection and data-file groups cover `spec-v2` only), then the additions.

1. **Blindness.** Render a batch, v1 and v2, from inputs that plant reviewer ids, model names, severity words, `blocking` values, `support`, `reviewers` and a combo-style path; assert none appears in the output (the E2 judge leak, `research/11` section 2).
2. **Determinism.** The same seed gives the same batches and canary positions; a different review number or seal gives different ones.
3. **Canaries and reruns.** A wrong canary rejects the batch; the first rejection allows one rerun; the second leaves items `unconfirmed`; `unconfirmed` never yields PASS.
4. **Reply parser.** Exact key set from the rubric header; duplicate, missing and unknown `cid`; `why` over 25 words.
5. **Candidate selection.** MINOR-only excluded; unflagged MAJOR included; advisory and grounding-gap excluded; singleton included; a cluster that loses every citation is `dropped-unfounded`; v1 form (no channel test) tested separately.
6. **Verdict table.** PENDING (exit 12) when any candidate is undecided or unconfirmed; FAIL when any candidate blocks; PASS only when all are graded not blocking.
7. **Frozen grades.** A re-found row keeps its grade; changed cited text triggers re-grading; a different rubric hash is refused; `grade apply` on a graded batch is refused.
8. **Relations.** `agreed`, `overruled` and `promoted` counts match a hand-built case.
9. **CLI round trip.** `merge --decide grader`, `grade prep`, a canned reply file, `grade apply`, `ledger verdict`, exit codes.
10. **Reflect-post predicate.** For each class in `findings_v2.DEVIATION_CLASSES`, build a contract and assert the chosen predicate (once the owner picks one of the two rules) agrees with `contract._halted_reason` where the owner decides they must agree; assert the other rule's disagreement cases explicitly (a MAJOR authorized finding).
11. **Reflect shadow.** Grades appear only inside `telemetry:`; `panel_lint` passes with them present; no new top-level key.
12. **Grader selection.** With a non-empty disjoint set the chosen `model_class` is outside the reviewers' classes; with an empty set the run records `grader_diversity: degraded`.
13. **Data files.** The `spec-v2` rubric and its canary file load, carry at least one blocking and one minor canary, and their hashes are recorded.
14. **Agent file.** Frontmatter and body pass the dual-surface lookup rule.
15. **Bias battery** on a fixed set (swap order, pad, rename) with an assertion that grades are unchanged; slow or manual marker.
16. **Replay gate** (not a unit test): the pre-registered comparison in "Rollout". It needs the portable benchmark of C20; until it exists, a script-driven replay is the interim, and the gate cannot pass without it.

Additions from Variant A and the debate (agreed):

17. **Rule parity across both copies.** A property test over generated member flags and lens predicates: ledger row `blocking` (`ledger.py:187`), cluster `blocking_any` (`cluster.py:375`) and `any(effective flags)` agree, and the ledger verdict is FAIL iff one such row is open. This is the test that stops the copies from drifting apart.
18. **Monotonicity.** Adding a valid reviewer to a first review never turns FAIL into PASS; adding a reviewer whose block is invalid or partial never clears a row (D2).
19. **Effective flag** (shared with C16). `channel: advisory` and `grounding-gap` with `blocking: true` give an effective false; a missing anchor gives an effective false until verified, with a warning that names the finding id; two-word deviation-class labels are normalised before the predicate runs (`card_convert.py:203`).
20. **`singleton_blockers`.** One reviewer flags a cluster: count 1. Two distinct reviewers flag the same cluster: count 0. A partial reviewer's valid line counts. The value appears in `review cluster` and `review merge` output and in telemetry, and no code path reads it.
21. **`defer` recomputation.** `defer` on a one-reviewer round-1 loop returns PASS with `degraded: true`; under `--decide grader` a round with undecided rows stays PENDING after `defer`.
22. **`EXIT_BY_DECISION` with PENDING.** `ledger verdict` exits 12 for PENDING under `--decide grader` and raises no `KeyError`.
23. **Reflect isolation.** A shadow run that adds `singleton_blockers` and grades to the nested `telemetry:` block passes `lint_panel_contract` (rules L1-L6, bump rule B) and leaves `merge_method`, `contract_version` and every stable key untouched.

Additions the probe showed are missing. **Not agreed in the debate; they are proposals from the invariant probe:**

24. A replay that exercises rounds 2 and 3 (`apply_revision`, `defer`, re-found and regressed paths, the clear step) (INV-020).
25. An always-demote grader as a negative control for the replay (INV-019).
26. A tri-state reply test and a canary-count test (a one-claim batch carries two canaries) (INV-008, INV-010).
27. An anchor-missing-after-D1 test: a recovered long anchor that fails the locate gate (INV-014).

<!-- Source: Base (original, modified) - Cost; interim and destination cost lines, v1 adapter, one rubric, corrected canary overhead formula, "cost of being wrong" from Variant A; the Owner-decisions paragraph moved out of this section - Change 14 (C-015, A at 80%) -->
## Cost

S4 rates the blind grader at effort L, risk Medium, reuse Medium (S4 C05 Option D). C-015 ended in Variant A's favour at 80% on effort: S against L, with zero extra model calls against one grader call per batch, and B's v1 adapter added to B's cost. Line counts below are estimates, not measurements.

**Interim (the hardened veto): effort S, zero extra model calls beyond the finders.** The decision rule needs no change. Net new code: the `degraded` marker in `merge_round`, the `singleton_blockers` count, and optionally one shared function so `ledger.py` and `cluster.py` stop carrying two copies of `any(...)`. The D2 fix is about three lines `[estimate; Advocate A]`. Tests: three changed for the marker, two changed for prerequisites, new tests 17-23. The prerequisites (C02, C12, C15, C16) are costed in their own conflicts and needed under every option, so they are not charged here.

**Destination (the grader): effort L.**
- `grade.py`: a port of `stoprule.py:657-899` (about 240 lines) plus candidate selection, the grade schema and relation counts: roughly 300 to 400 lines `[estimate]`.
- `grade_cmd.py` about 150 lines `[estimate]`; edits to `ledger.py` (`merge_round` blocking source, row `grade`, rubric-hash check, `defer()` recomputation) about 40 to 60 lines `[estimate]`; small edits to `merge_cmd.py` and `ledger_cmd.py` (`--decide`, exit 12, the `EXIT_BY_DECISION` entry).
- **The v1 adapter, which the base did not cost:** 50 to 100 lines plus a second renderer plus a parity test across both paths `[estimate; Advocate B, not measured]`.
- Promote and generalise `finding-grader` into `src/superclaude/agents/`, then `make sync-dev` (the `.claude/` copy is never staged; project `CLAUDE.md`).
- **One rubric (`spec-v2`) and its canary file in the first build, not three.** The installed canary set has 8 canaries, 4 blocking and 4 minor (G4); the new lens file needs its own, written to be separable from the benchmark's ground truth. Whether a `reflect-pre` rubric ships is an owner decision.
- Grader selection uses `review panel resolve --hard-exclude-class` with a one-slot template; no panel schema change (`research/05` section 12). Making the decider a first-class slot is the additive schema change C04 already recommends.
- Tests: the 27 groups above. Documentation: reflect `SKILL.md` shadow steps (a telemetry line), `document_review_loop_prompts.md` when the default flips.

**Reused as is.** `cluster_v2`, `verify-citations`, the evidence-validator, the stoprule batch and canary logic, the rubric text, the `PROFILES` idea (blocking predicate as data), the E2 ground-truth packages as the benchmark.

**Run cost per round.** One grader call per batch of at most 6 candidates plus 2 canaries. Input per item is bounded by the claim limit of 300 characters (`findings_v2.py:111`) plus the re-read cited text, whose size is an owner decision (Owner decisions). **Canary overhead, one formula:** overhead = canaries / (claims + canaries) per batch, with two canaries per batch whatever its size (`stoprule.py:669-673`). So 25% holds only for a six-claim batch. A singleton-first batch of 1 claim plus 2 canaries has 67% of its items as canaries, or 200% relative to the one real claim (INV-010). No grader token count has been measured anywhere: the one live trial recorded none (G7), and E2's judge numbers (`research/11`, about 115,000 output tokens per package-arm in the pilot) are for a full-document ground-truth judge and are not comparable. The shadow data suggest one batch per run (V8). Candidate counts per E2 run were not computed.

**Latency.** One extra model round-trip per review round, parallel across batches. For the document loop this adds a step before the verdict; for reflect it adds a post-debate step that is off the critical path while grading is telemetry-only.

**Benchmark cost.** One replicate of the default panel over the three packages is 63,644 reviewer output tokens (`CR:331`), so six replicates are about 380,000 REVIEWER OUTPUT tokens, 6 x 63,644 `[advocate-computed, not re-aggregated]`. Judge passes and the judge re-run (matching grader-blocking rows to ground truth) are not costed.

**Cost of being wrong.** If the replay fails or stays inconclusive, the follow-up filter on singleton blockers (effort M to L, over a smaller input) reuses the evidence gate, the effective flag, the abstention rule and `singleton_blockers` that the interim adds, so nothing built for the interim is thrown away.

**Cost of keeping the veto alone.** The veto costs XS and is correct as code on the 264 replayed merges (V1, V7), but E2 measured one panel (the four-reviewer `2x luna + 2x ember`) with 2.75 to 3.25 more wrong blockers than every comparator (V3), found no size effect on the control package (EC2), and the veto gives no recall guarantee (V5); the cause of the wrong blockers is open (EC1). The grader buys a different decider at the price of one new stage, one new agent, a v1 adapter and a gate that has to be run before it is trusted; whether it buys better decisions is unmeasured.

The decisions the owner must take are listed in "Owner decisions".


<!-- Source: Debate record - Unresolved conflicts, Round 2 tracking rows C-005, C-012, X-002 and the QUALIFY rows A-001, A-003, A-007 - Change 16 -->
## Unresolved conflicts

These are the points the advocates agreed cannot be decided on present evidence (agreed-open), and the three assumptions both advocates qualified. They stay visible: nothing here is decided, and "the measurement the debate named" is a measurement that may not decide.

<!-- Source: Debate record - Round 2 tracking rows C-005, C-012, X-002 - Change 16 -->
### Agreed-open points

| ID | Agreed-open position | The measurement the debate named; it may not decide | Limits |
|---|---|---|---|
| **C-005** (precision mechanism and panel-size policy; OPEN 73%) | Neither mechanism is evidenced. The panel cap of three finders is kept as a cost cap only; the effect of panel size on precision is open. On the control package wrong blockers are flat by panel size (EC2) | The replay reports wrong blockers by panel size | Per-panel n is 4 to 6, so power by panel size is low; the control package has two defects and no blocking defect; the same limits as INV-019 and INV-022 apply |
| **C-012** (reading of the E2 evidence, the cause of the veto's wrong blockers; OPEN 71%) | Fix D1, D5 and D6 first; run veto and grader on the same candidates; score both on `blocking_in_implement`. Whether the wrong blockers come from the veto, from input defects, or from both is not known | The paired replay | INV-019 (an always-demoting grader meets the criterion), INV-020 (the replay never runs rounds 2 and 3), INV-022 (power; "same candidate sets" breaks where D1 changes the set) |
| **X-002** (V7 and Variant A's E-5 disagree on attribution; OPEN 69%) | V7 must list D1; attribution of the wrong blockers is unmeasured. D1 pushes counted wrong blockers down. D5 (13 null-span blocking rows `[VIA audit-D]`) and D6 (83 chained rows) may push them either way; the direction was not agreed (Advocate A said in Round 1 that D6 depresses blockers; Advocate B said D5 and D6 could inflate them) | The same replay, with D1, D5 and D6 fixed first | The same limits as C-012. The replay measures the combined effect of the fixes and does not attribute it to a defect |

<!-- Source: Debate record - QUALIFY rows A-001, A-003, A-007 with the conditions and confidences of Change 16 -->
### Qualified assumptions (QUALIFY, shared by both variants)

| ID | Assumption | Agreed condition under which it holds | Confidence | Attached invariants |
|---|---|---|---|---|
| **A-001** | The E2 result (one lens: tasklist and spec review, three packages, 16 defects, n of 4 to 6) transfers to the other lenses the core will serve | Holds only for the spec and tasklist lens, because E2 ran the spec brief, reflect-post is code-decided and reflect-pre has no ground truth | 60% | INV-016 |
| **A-003** | Absence findings (category `missing-requirement`, "the plan has no X") survive the evidence gate | Holds only if absence findings anchor to the quoted requirement text that is incomplete, and a failed locate routes to a re-read, not to suppression | 58% | INV-006, INV-025 |
| **A-007** | A finding keeps a stable identity across rounds (`fp`), so a re-found row inherits the right flag or the right frozen grade | Holds only if `same_defect` is tightened and a cited-text-changed guard is actually implemented | 60% | INV-011 |

For A-007 the debate left open how `same_defect` is tightened, with what test and what number (INV-011); see "Owner decisions".

<!-- Source: Debate record - Unaddressed invariants, all 25 findings of invariant-probe.md (Round 2.5 fault-finder) - Change 17 -->
## Unaddressed invariants

**This section is the debate's list of what it did not resolve. It is not a to-do list that the merge has completed.** The invariant probe (Round 2.5, an independent fault-finder, six categories including the always-on sufficiency challenge) tried to break the emerging consensus and returned 25 findings: 23 UNADDRESSED (11 HIGH, 10 MEDIUM, 2 LOW) and 2 ADDRESSED (both LOW). Because 11 HIGH findings are UNADDRESSED, convergence is blocked regardless of the 90.9% agreement. At depth standard there is no Round 3 in which to resolve them. The debate did not resolve any of the 23, and this document does not state that any of them is resolved. Severity and status are exactly as the probe set them: HIGH items first, then MEDIUM, then LOW, then the two ADDRESSED ones. The labels M1 to M12 in the "Assumption" column are the probe's names for the consensus items it was given; they are defined in the notes below the table.

Orchestrator verification noted in the probe: code-fact claims behind INV-001, 003, 005, 008, 009, 010, 012, 016 and 017 were spot-checked and accurate; INV-002, 004, 006, 007, 011, 013, 014, 015, 018 and 020 to 025 rest on source lines and E2 report rows that the fault-finder read and the orchestrator did not re-read.

| ID | Category | Assumption | Status | Severity | Evidence (one line, as in the probe) | Used in this document |
|----|----------|------------|--------|----------|----------|----------|
| INV-001 | state_variables | M5 frozen decisions close the "one non-blocking re-report clears a row" hole while M1 keeps the veto live | UNADDRESSED | HIGH | Under the live veto a re-found row takes the current round's flag (`ledger.py:210-218`, pinned by `test_review_ledger.py:518-544`); default re-review is one reviewer; the freeze exists only after the flip | Contract fields; Correctness; R13 (Changes 9, 11, 12) |
| INV-004 | guard_conditions | M2's "certify at round 1, later rounds inherit" keeps PASS meaning "two valid reviewers looked" | UNADDRESSED | HIGH | The PASS-deciding round after a REVISE is a one-reviewer re-review (`document_review_loop_prompts.md:70`; one valid block suffices, `ledger.py:150-157`); the flag is sticky, no guard for a thin deciding round | Decision summary; Certification (Changes 1, 3) |
| INV-005 | guard_conditions | M3's "unresolved anchor is never effective-blocking until a named resolver re-reads it" fits the verdict | UNADDRESSED | HIGH | With the live veto the gated row leaves the brief (`ledger.py:99-104,274`) so the round can PASS before the resolver runs; v1 members carry no anchor status; no resolver on the v1 path | Evidence gate; Interim rule (Changes 2, 6) |
| INV-011 | collection_boundaries | Grading one claim per cluster and freezing it (M5) is safe once D6 and `same_defect` are "tightened" | UNADDRESSED | HIGH | One `representative` claim per v2 cluster (`cluster.py:338-344`), v1 row takes `group[0]` claim (`ledger.py:182-199`); `same_defect` merges by shared fp (`findings.py:367-372`); a `false` demotes every member and M5 freezes it; no mechanism, test or number for "tightened" | Adapters; R18; A-007 (Changes 8, 16) |
| INV-014 | interaction_effects | D1, D5, M3 evidence gate, M9 partial abstain and M2 degrade compose | UNADDRESSED | HIGH | (a) a lone reviewer's rejected blocking finding is lost while two other valid blocks still certify; (b) if D1 is fixed by raising the 200-character limit, the recovered luna and ember findings fail the M3 locate gate (`findings.py:276-304`): the D1 fix and the gate cancel | Rollout step 0; Evidence gate; Interim rule; test 27 (Changes 6, 13, 15) |
| INV-019 | sufficiency_challenge | M12: fix D1, D5, D6 plus the paired replay alone decides between veto and grader | UNADDRESSED | HIGH | A grader that always says `false` passes the control wrong-blocker test (control has no blocking defects, see the note below the table), cannot lose measured recall on a 0.17-1.20 of 8 floor, meets only easy canaries, and no numeric pass threshold exists | Rollout; Correctness; R22; C-012; Owner decisions (Changes 11, 12, 15, 16, 18) |
| INV-020 | sufficiency_challenge | The E2 replay can validate M2, M5 and M9 (certification, frozen decisions, clearing) | UNADDRESSED | HIGH | E2 merged each package once; the replay never runs `apply_revision`, `defer`, re-found or regressed paths, or the clear step (`ledger.py:207-238,254-258,301-360`), which is where C-006 lives | Rollout; Correctness; test 24 (Changes 11, 13, 15, 16) |
| INV-021 | sufficiency_challenge | M4 affirmative demotion alone fixes the fail-open grader | UNADDRESSED | HIGH | B2 is ungradable on the replay inputs: v1 has no `outcome` field, claims are at most 300 characters with no enforced named reader (`findings.py:118`); the grader arm collapses toward the veto; the claim-shape fix is not in M1-M12 | Grader and rubric; Rollout step 0; Owner decisions (Changes 5, 18) |
| INV-023 | sufficiency_challenge | Shadow counts (`overruled`, `promoted`, `singleton_blockers`) make the choice checkable after rollout | UNADDRESSED | HIGH | Production loops have no ground truth (`research/05:195`); `overruled` measures disagreement not who is right; `promoted` precision needs labels nothing produces; the reviser's applied/rejected fix map (`ledger.py:330-342`) is the only weak label and is not named | Promotion; Rollout; Correctness P4 (Changes 1, 4, 15) |
| INV-024 | sufficiency_challenge | M2 degrade rule alone resolves "PASS certified on a thin panel" | UNADDRESSED | HIGH | Exit codes stay 0/10/11 and `test_review_cli.py:348` asserts exit 0 and PASS; in-repo consumers are `ledger.py`, `merge_cmd.py` and the prompt prose; only prose is asked to report "uncertified", so no code enforces the flag | Certification; Owner decisions (Changes 1, 3, 18) |
| INV-025 | sufficiency_challenge | M3 evidence gate alone resolves wrong blockers without losing real ones | UNADDRESSED | HIGH | The gate's target inputs are the population that fails it: D5's 13 null-span blocking rows [VIA audit-D] fail the locate step, D1's recovered long anchors likely fail it, the v1 path has no re-read resolver; the gate suppresses real blockers and no input is shown to pass it | Evidence gate; A-003 (Changes 6, 16) |
| INV-002 | state_variables | New persistent state (degraded, rubric hash, frozen and shadow decisions) fits the existing ledger schema | UNADDRESSED | MEDIUM | `SCHEMA = "review-ledger/1"` (`ledger.py:17`, `load` at `:47`); mid-flight loops have no decision field; rubric-hash refusal strands a loop when `spec-v2` ships | Contract fields; Owner decisions (Change 9) |
| INV-006 | guard_conditions | Routing absence findings to the quoted requirement text lets the gate and the grader handle them | UNADDRESSED | MEDIUM | A located anchor proves where the reviewer pointed, not that something is absent; grader cannot read the document (`finding-grader.md:12`); a fix elsewhere leaves the row `named_not_touched` and the loop ends in ESCALATE | Evidence gate; Correctness; A-003 (Changes 6, 11, 16) |
| INV-007 | guard_conditions | PENDING under `--decide grader` (exit 12) fits the review loop | UNADDRESSED | MEDIUM | `_decision` has no PENDING mapping (`ledger.py:93-96`); stoprule counts waiting claims as FAIL `incomplete`; undecided rows have `blocking: None` so `defer()` can turn the round into PASS | Certification; R20 (Changes 1, 3) |
| INV-008 | guard_conditions | M4's true/false/undecidable reply is a rubric change (`spec-v2`) | UNADDRESSED | MEDIUM | It is a schema change: `parse_grader_reply` and `evaluate_reply` require a boolean (`stoprule.py:808-830`); "name B1/B2/B3" must fit 25 words; the files serve the live stoprule command | Grader and rubric; test 26 (Changes 5, 13) |
| INV-009 | count_divergence | "At least two reviewers with a valid block" measures two independent looks | UNADDRESSED | MEDIUM | `block_ok` is false on any bad line; E2 audit D found 80 reviewer-level drops; dedup is by id only (`ledger.py:119-121`) so two same-model reviewers count as two; replay does not report the degrade rate | Certification; R17 (Change 12) |
| INV-010 | count_divergence | Canaries cost "25% overhead" and a rerun is an independent second chance | UNADDRESSED | MEDIUM | Two canaries per batch whatever its size (`stoprule.py:669-673`): 200% for a one-claim batch; rerun likely meets the same canaries; a wrong canary rejects every real claim in the batch | Reply handling; Cost; test 26 (Changes 13, 14) |
| INV-015 | interaction_effects | Shadow can start now and `spec-v2` follow later | UNADDRESSED | MEDIUM | `spec-v1` has the fail-open default and trusts unverified evidence (`finding-grader.md:17,19`); shadow counts collected before `spec-v2` measure a rubric that will not ship; the claim-shape fix (named reader and outcome) must precede shadow | Rubric table; Rollout (Changes 1, 15) |
| INV-016 | interaction_effects | M8's code predicate on `deviation_class` / `reflect_category` is one rule | UNADDRESSED | MEDIUM | `findings_v2.py:155-162` makes every MAJOR or CRITICAL finding with a `reflect_category` blocking whatever its class; `contract.py:377-381` halts only on regression or drift; `reflect_category` is optional; counts default to 0 when absent | Reflect-post: code predicate; Owner decisions (Changes 7, 18) |
| INV-017 | interaction_effects | M10: two copies of the blocking rule need adapters and a parity test | UNADDRESSED | MEDIUM | At least two more copies: `diffgate.py:796` and the claim-level rule in `stoprule.py:1179-1191`; scope of the unified core over those commands is not stated | Adapters; Owner decisions (Changes 8, 18) |
| INV-022 | sufficiency_challenge | The pooled paired replay has power | UNADDRESSED | MEDIUM | The 71 pooled rows are not independent (control is one document with 2 defects); some rows were merged from stale or replaced reports; "same candidate sets" breaks where D1 changes the set; B's own R1 residual predicts an inconclusive result, which keeps the veto live forever | Rollout; C-012 (Changes 1, 15, 16) |
| INV-013 | collection_boundaries | D2 ("an invalid reviewer never clears a row") is a three-line fix with no side effects | UNADDRESSED | LOW | `ledger.py:254-257` never reads `block_ok`; the fix inverts the pin at `test_review_ledger.py:376-385`; a reviewer whose block is always invalid would stop rows clearing and end in ESCALATE | Interim rule; Test coverage (Change 2) |
| INV-018 | interaction_effects | A shadow grader "routes nothing" while the veto stays unchanged | UNADDRESSED | LOW | The merged report is read by the next reviewer and the reviser (`ledger.py:408-411`); a shadow annotation in it would anchor them; no rule keeps shadow data out of the report or out of the exit code | Contract fields; Rollout step 1 (Change 9) |
| INV-003 | state_variables | `defer()` can recompute the certification flag | ADDRESSED | LOW | `ledger.py:356-360`; named in M2 and in the Round 2 new evidence; flag derivable from `block_ok` per round | Certification (Change 3) |
| INV-012 | collection_boundaries | Empty inputs (zero valid reviewers, zero candidates) are safe | ADDRESSED | LOW | A round with no valid block is refused (`ledger.py:150-157`; `test_review_ledger.py:345-373`); zero candidates give no batch (`stoprule.py:669`) | not referenced in the body (no change needed) |

**Notes.**
- The invariant labels M1 to M12 in the "Assumption" column are the probe's names for the consensus items it was given: M1 veto live and grader in shadow; M2 certification and PENDING; M3 evidence gate; M4 true/false/undecidable reply; M5 frozen decisions; M6 cap as a cost cap; M7 D1, D5, D6 fixed first and a paired replay; M8 reflect-post code predicate; M9 partial or invalid reviewers abstain; M10 two copies of the rule; M11 evidence transfers only to the spec and tasklist lens; M12 the sufficiency claim "fixing D1, D5, D6 and running the paired replay is enough to decide, and shadow counts make the choice checkable". The probe tested M12 as a claim; this document does not make it.
- Wording in the probe rows: the probe says "decision" and "frozen decisions" where this document says `grade` and frozen grades; the rows are kept as the probe wrote them. Its "class" in INV-016 means `deviation_class`.
- INV-019 citation note: the probe cites `research/05-blocking-calibration.md:311` for "the control package has 0 known blocking defects". The orchestrator's spot check found that lines 309-313 of that file do not state it. The fact (control: 2 defects, 0 blocking in ground truth) is stated in Variant B R1 and in `research/11` section 5 as B cites it, so the finding stands on that source; the line reference is flagged.
- Counts: 25 rows; HIGH UNADDRESSED 11; MEDIUM UNADDRESSED 10; LOW UNADDRESSED 2; ADDRESSED 2.

<!-- Source: Variant A Cost "Owner decisions" merged with Base (original) Cost "Decisions this proposal needs from the owner", plus the decisions the debate and probe added; open phrases of both variants replaced by entries here - Change 18 -->
## Owner decisions

Nothing below has been decided. Each entry is a number, a policy or an ownership the debate left to the owner. Entries 1, 15 and 16 replace phrases that the two variants left open ("owner-set tolerance", "design parameters to fix at build time", "to be tightened"). Open points of the invariant probe that have no entry here (for example INV-004, INV-007, INV-009, INV-020) are listed in "Unaddressed invariants" and are not owner decisions in the plan this merge executed.

| # | Decision the owner must take | Why it is open | Attached |
|---|---|---|---|
| 1 | The control-package wrong-blocker tolerance and a numeric pass threshold for the replay | Neither variant gives a number; a grader that always demotes meets the qualitative criterion | INV-019 |
| 2 | Which reflect-post predicate applies: the label rule at `findings_v2.py:155-162` or the halting rule at `contract.py:377-381` | The two are different rules; a MAJOR authorized finding blocks under one and passes the other | INV-016 |
| 3 | Who authors the `reflect-pre` rubric, and whether one ships | reflect-pre has no ground truth; the debate did not decide | Rubric inventory |
| 4 | Whether MINOR drift halts (G-03) | `contract.py:380-381` against `findings_v2.py:107-108` | INV-016 |
| 5 | Who sets `unauthorized_deviation_present` (G-04) | No producer rule exists (`SKILL.md:854`) | INV-016 |
| 6 | The static-unreachability rule: is it a Regression (G-05) | `SKILL.md:1196` and `deviation-taxonomy.md:123` disagree (`research/05` section 3.2) | R2 |
| 7 | The environment the central panel serves (C03, O-2) | It sets how often the grader can be vendor-disjoint | R3 |
| 8 | The owner of the benchmark port (G-59) | The replay needs the portable benchmark of C20 | R16 |
| 9 | Who authors the rubrics (`spec-v2` and any other) | The grader's quality rests on a rubric nobody has measured against ground truth | R1 |
| 10 | The verdict vocabulary for a degraded PASS (C19), and whether any caller must treat it as uncertified in code | Exit codes stay 0/10/11; only prose is asked to report "uncertified" | INV-024 |
| 11 | Whether the `diffgate` and `stoprule` copies of the blocking rule are in scope for the unified core | At least two more copies exist (`diffgate.py:796`, `stoprule.py:1179-1191`) | INV-017 |
| 12 | The selector for an `undecidable` grade: the reviewer's flag stands, or the row goes to PENDING | The debate agreed "or"; no selector exists | INV-008 |
| 13 | The claim-shape fix (a claim names a reader and a wrong result) or an `outcome` field, and whether it must precede shadow | B2 is ungradable without it | INV-021, INV-015 |
| 14 | A ledger schema bump, and the default for a row without a grade in a loop in flight at rollout | `review-ledger/1` accepts any ledger | INV-002 |
| 15 | How many lines of cited text the renderer shows per citation, and the cap on citations per item | Left as "design parameters to fix at build time" in the base; no value exists | Grader inputs |
| 16 | How `same_defect` is tightened: the mechanism, the test and the acceptance number | "To be tightened" has no mechanism, test or number; the D6 fix covers only the 83 chained rows | INV-011, A-007 |

<!-- Source: Debate record - Debate record and provenance; the 33-point table is the Round 2 tracking table of debate-transcript.md - Change 20 -->
## Debate record and provenance

**Status.** Partial. Alignment 90.9% (30 of 33 points with a determinate agreed outcome); convergence was blocked by invariants (11 HIGH-severity UNADDRESSED); 3 agreed-open points (C-005, C-012, X-002). Threshold 80%. Taxonomy coverage gate satisfied (L1 5 of 5, L2 18 of 18, L3 10 of 10). Rounds: 2 debate rounds (Round 1 parallel, Round 2 sequential) plus Round 2.5 (invariant probe); Round 3 not run at depth standard. Trajectory: Round 1 60.6%, Round 2 90.9% determinate (33 of 33 identical stances, 3 of them agreed-open). Both advocates moved because they verified source facts and conceded errors, not because of a score threshold; fast agreement is where the probe is aimed, and it found what the table below cannot show.

**Points won (Step 3 tiebreaker).** Variant B 6 (S-004, S-005, C-006, C-013, X-001, X-007); Variant A 2 (C-015, X-004); HYBRID 13; EQUAL 6; OPEN 3; QUALIFY 3; total 33. The tiebreak rests on a small count: only 8 points produced a one-sided winner.

<!-- Source: Debate record - Round 2 per-point tracking table of debate-transcript.md, topics from diff-analysis.md - Change 20 -->
### The 33 debate points

Level: L1 surface (naming, wording, presentation), L2 structure (components, interfaces), L3 state mechanics (guards, boundaries, transitions). "Agreed outcome" is the outcome both advocates stated in Round 2; HYBRID names the merged position; "agreed-open" means both said the point cannot be decided on present evidence.

| ID | Level | Topic | Agreed outcome |
|---|---|---|---|
| S-001 | L1 | Section ordering | EQUAL |
| S-002 | L1 | Hierarchy depth | EQUAL |
| S-003 | L2 | Evidence organization | EQUAL: source-column tables plus a counter-reading column; tag unread facts `[VIA]` |
| S-004 | L1 | Risk register format | B (risk table with a Residual column) |
| S-005 | L2 | Staging or rollout section | B (staged rollout) |
| S-006 | L2 | Test-coverage organization | HYBRID (tests of both, with the Round 2 accounting) |
| S-007 | L1 | Evidence provenance tags | EQUAL |
| S-008 | L1 | Placement of the weakest point | EQUAL |
| C-001 | L2 | Decision authority and independence of the decider | HYBRID: veto live now, grader in shadow, then live per lens after the paired replay |
| C-002 | L3 | PASS rule and reviewer-count guard | HYBRID: A's degrade rule on top of B's PENDING; certification set at round 1 and inherited |
| C-003 | L3 | Candidate set and promotion | HYBRID: `promoted` counted in shadow only; cannot raise a FAIL until measured |
| C-004 | L2 | Singleton handling | HYBRID: `singleton_blockers` from `reviewers[]`; singletons are the first population graded |
| C-005 | L2 | Precision mechanism and panel-size policy | OPEN (agreed-open): cap kept as a cost cap only; replay reports wrong blockers by n |
| C-006 | L3 | Re-found row and clearing across rounds | B, narrowed to rows whose text did not change |
| C-007 | L3 | Evidence gate behaviour | HYBRID: unresolved citation never blocking; named resolver; absence findings routed to the quoted requirement; `unverified` never sole support |
| C-008 | L2 | Per-lens predicate or rubric | HYBRID: code predicate for reflect-post; frozen rubric for spec |
| C-009 | L3 | Fail-closed behaviour and failure handling | HYBRID: both layers needed (reviewer-level abstain, grader-level canaries) |
| C-010 | L2 | Verdict vocabulary, CLI surface, contract fields | HYBRID: exits 0/10/11 kept; `degraded` field and report line; exit 12 plus an `EXIT_BY_DECISION` entry for PENDING |
| C-011 | L2 | Reflect integration and contract constraint | EQUAL |
| C-012 | L2 | Reading of the E2 evidence | OPEN (agreed-open): fix D1, D5, D6 first; same candidates; score on `blocking_in_implement` |
| C-013 | L2 | Rollout, acceptance gate, measurement plan | B (paired, pre-registered, pooled replay) |
| C-014 | L2 | Test-coverage plan | HYBRID |
| C-015 | L2 | Cost, new components and latency | A (S versus L), with B's v1-adapter cost added |
| X-001 | L3 | Can another decider add a blocker the veto would not have raised | B's side (A's claim is false for B as designed; dropped) |
| X-002 | L2 | Cause of the veto's wrong blockers in E2 | OPEN (agreed-open): attribution unmeasured; D1 pushes wrong blockers down |
| X-003 | L2 | What the 65-versus-38 gap means | HYBRID |
| X-004 | L2 | Is the wrong-blocker effect a panel-size effect | A's side: no size effect on control; drop P1's "measured that direction" and the cap-as-precision claim |
| X-005 | L3 | Degraded PASS versus a usable one-reviewer fallback | HYBRID: certification is a loop property set at round 1; `defer()` recomputes |
| X-006 | L3 | Fail-closed by construction versus a not-blocking default | HYBRID: the grader may demote only with a named failed criterion; on doubt keep the reviewer's flag or PENDING |
| X-007 | L2 | Is A the only option that leaves pins and contract alone | B's side (A's claim fails) |
| A-001 | L2 | E2's one-lens result transfers to other lenses | QUALIFY |
| A-003 | L3 | Absence findings survive the evidence gate | QUALIFY |
| A-007 | L3 | Finding identity is stable across rounds | QUALIFY |

<!-- Source: Debate record - unique contributions U-001 to U-017 of diff-analysis.md and base-selection.md - Change 20 -->
### Where each contribution went

- **Variant A (non-base):** asymmetric verdict (U-001) to "Certification and verdict vocabulary"; `singleton_blockers` (U-002) to "Promotion and `singleton_blockers`"; the four input fixes (U-003) to "Interim rule"; error-cost asymmetry (U-004) to Correctness P6 and Evidence V10; the panel cap (U-005) kept as a cost cap only; rule-parity and monotonicity tests (U-006) to tests 17 and 18; the reading of the 65-versus-38 gap (U-007) to EC3 and the V2 counter-reading; "cost of being wrong" (U-008) to Cost.
- **Variant B (base):** candidate rule (U-009), blindness by construction (U-010), canaries and batch rejection (U-011), frozen rubric as data (U-012), relation counts (U-014), staged rollout (U-015), grader independence and served-model recording (U-016) and the transport lessons and bias battery (U-017) are preserved. U-013 (`reflect-post-v1` rubric mirroring the halting set) is overridden by the code predicate; U-011 and U-012 are modified by the demotion rule and `spec-v2`; U-014 is qualified by INV-023.
- **Unchanged claims of the base that the debate showed wrong** were rewritten: P1, V7, P4 ("fail-closed by construction"), the K1 wiring and the claim that `_brief_ids` needs no change.

<!-- Source: Debate record - artifact pointers - Change 20 -->
### Artifacts

All paths are relative to the folder that holds this document.

| File | What it is |
|---|---|
| `adversarial/variant-1-original.md`, `adversarial/variant-2-original.md` | Variant A (hardened veto) and Variant B (blind grader, the base), normalized copies; the originals are `proposal-a.md` and `proposal-b.md` |
| `adversarial/diff-analysis.md` | 54 listed differences, the 33 debate points and their taxonomy levels, the shared assumptions |
| `adversarial/debate-transcript.md` | Both rounds verbatim, per-point outcomes, the scoring matrix, the convergence assessment |
| `adversarial/invariant-probe.md` | The 25 findings INV-001 to INV-025 and the fault-finder output |
| `adversarial/base-selection.md` | Quantitative and qualitative scoring, position-bias mitigation, the tiebreaker, strengths to preserve and weaknesses to fix |
| `adversarial/refactor-plan.md` | The 20 changes this merge applied, independently reviewed (22 findings, all accepted) |
| `adversarial/merge-log.md` | Per-change execution log and the post-merge validation |
| `adversarial/return-contract.yaml` | The run's return contract (not edited by the merge) |

**Provenance and verification.** Provenance comments (`<!-- Source: ... -->`) precede each section; they are invisible in rendered Markdown. The `[READ]` and `[E2 4a22d74]` tags are the variant authors' own; the merge did not re-read the code or the E2 reports. The debate's own re-verification is in the Round 2 "Facts verified" lists, and the orchestrator's spot check is in the invariant probe. Numbers that debate advocates computed, and sizes nobody measured, carry `[advocate-computed, not re-aggregated]` or `[estimate]`.
