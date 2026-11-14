# Adversarial Debate Transcript

## Metadata
- Depth: standard (Round 1 parallel, Round 2 sequential, Round 2.5 invariant probe; Round 3 not run at this depth)
- Rounds completed: 2 (Round 1 parallel, Round 2 sequential) plus Round 2.5 (invariant probe)
- Convergence achieved: 90.9% (30 of 33 points with a determinate agreed outcome), BLOCKED_BY_INVARIANTS (11 HIGH UNADDRESSED invariants); see the Convergence Assessment at the end
- Convergence threshold: 80% (default)
- Focus areas: correctness, risk, test-coverage
- Advocate count: 2 (Variant A advocate, Variant B advocate; one agent per round per variant, spawned with the Agent tool, `subagent_type: general-purpose`)
- Fallback mode: false (agents were spawned as separate agents, not simulated)
- Debate points: 33 (S-001..S-008, C-001..C-015, X-001..X-007, promoted A-001, A-003, A-007); taxonomy L1 = 5, L2 = 18, L3 = 10
- Variant A = Option A of C05 (single-reviewer veto, inputs hardened). Variant B = Option D of C05 (blind grader after clustering).
- Agents in this run: Round 1 advocates were named `c05-advocate-A-r1` and `c05-advocate-B-r1` (two agents in one message, parallel). Round 2 advocates (A first, then B, sequential, B seeing A's rebuttal) and the Round 2.5 fault-finder were spawned unnamed, each a separate general-purpose agent. Names such as `advocate-A-r1` that appear in the session's agent list belong to another debate and were not used or contacted.

## Delivery note
The two Round 1 advocates were spawned in ONE message with the Agent tool (parallel). Because they were spawned as named agents, their final text was written to their own agent transcripts and not returned inline. The orchestrator extracted the first complete statement of each from its transcript verbatim (jq on the agent JSONL) and pasted it below without edits. Both agents later answered an orchestrator wrap-up nudge with near-identical repeats; the repeats are not used. The text below, including the closing status table the advocate added, is the advocate's own output.

## Round 1: Advocate Statements

### Variant A Advocate (agent c05-advocate-A-r1, general-purpose, default model, focus: correctness, risk, test-coverage)

### Position
Keep the veto as the decision rule that is live today, and run B's blind grader in shadow beside it behind its replay gate. That is A's rule plus B's measurement. On present evidence the grader's accuracy is unmeasured. A, as written, has errors in direction and scope, which I list below.

### Steelman of Variant B
B points at the only measured failure, the 65 catches against 38 real ones, and at its mechanism: the veto's wrong-block chance grows with reviewer count, while a grader's does not. It separates the finder from the decider, which is the pattern in the Cloudflare and LinkedIn posts. It stores each decision once, so one reviewer's non-blocking re-report cannot clear a row (`ledger.py:213-218` [VERIFIED]). It keeps the veto as a recorded baseline on every cluster. It stays in shadow until a pre-registered paired replay passes. It can also promote unflagged MAJOR clusters, which is the only mechanism in either variant that could add recall beyond the veto. B is right on C-006, C-007, C-013, X-001 and X-007.

### Per-point stances
| Point | Stance | Conf | Evidence |
|---|---|---|---|
| S-001 | EQUAL | 90 | Both use the same seven H2 sections in template order. |
| S-002 | EQUAL | 75 | B's H3 headings and A's bold lead-ins are presentation only. |
| S-003 | B | 55 | B's source-column tables separate evidence from argument. A's inline counter-readings are useful, but B carries more `[VIA Rnn]` items it did not re-read. |
| S-004 | B | 60 | R1-R11 with a Residual column is easier to audit than prose. |
| S-005 | B | 75 | B has a staged rollout with shadow, replay and a default flip. A has one benchmark gate (Risk 1) and no staging. |
| S-006 | HYBRID | 60 | Take B's blindness, determinism and verdict-table tests and A's rule-parity and monotonicity tests. B keeps two `any(...)` copies with no parity test. |
| S-007 | EQUAL | 80 | Both tag provenance. A's tags are slightly more exact. B has "[READ by grep]". |
| S-008 | EQUAL | 75 | Both name the weakest point (A step 8 and Risk 1, B "Weakest point" and R1). |
| C-001 | HYBRID | 65 | The veto decides now (`ledger.py:187,274`). B's grader runs in shadow with the veto recorded, which is B's own rollout steps 1-2. Nothing measures the grader. |
| C-002 | HYBRID | 65 | A's guard has precedent (`contract.py:295-296`), but it is under-specified. Default re-review is one reviewer (`document_review_loop_prompts.md:70` [VERIFIED]), so a PASS is routinely thin. B's PENDING covers undecided candidates, not thin panels. |
| C-003 | A | 60 | Promotion adds blockers with no precision data (R8 admits it). MAJOR with `blocking:false` is legal in the spec lens (`findings_v2.py:107-108`). Promote only if shadow `promoted` precision is measured. |
| C-004 | EQUAL | 60 | `singleton_blockers` is derivable from B's per-cluster `reviewers[]`. B's relations record more. |
| C-005 | HYBRID | 60 | B's per-candidate claim is structural but g is unmeasured. A's cap is cheap but weak: replicated n=3 panels average 2.37 wrong blockers against 1.67 for n=2, and `research/11` §12 says 2 is as good as 3 (table, [VERIFIED]). |
| C-006 | B | 65 | A concedes that one non-blocking re-report clears a row (Risk 3, pinned at `test_review_ledger.py:518-544` [VERIFIED]). A relies on D2 and C13, which A does not own. |
| C-007 | B | 60 | A's gate says "until a deterministic re-read confirms", but the re-read has already failed and no resolver is named. `verify_cmd.py:1-13` calls a quote-not-found "advisory, not proof". B tags `[unverified]` and still grades. |
| C-008 | HYBRID | 70 | Reflect-post already has a code path: `findings_v2.py:161-162` forces `blocking == (severity != MINOR)` when `reflect_category` is set, and `contract.py:377-381` halts by class. A grader that proposes the class adds a model where code exists. For the spec lens, B's frozen, hashed rubric beats reviewer self-grading. |
| C-009 | HYBRID | 70 | The two cover different layers. A handles reviewer-level failure (partial abstains). B handles reply-level failure (canaries, hashes, rerun, `unconfirmed`). Both are needed. |
| C-010 | A | 60 | `EXIT_BY_DECISION = {PASS:0, REVISE:10, ESCALATE:11}` (`ledger_cmd.py:13` [VERIFIED]). B adds exit 12, so every caller needs new handling. A also leaves its degraded vocabulary to C19. |
| C-011 | EQUAL | 70 | Both keep contract 1.8.0 and write panel-only data to nested `telemetry:`. B adds a path to a contract bump. |
| C-012 | HYBRID | 65 | A is right on the definition of the 27 extra catches (`COMBO-REPORT.md:291` [VERIFIED]). B is right that the excess is not explained by merge defects: D1 and D6 push toward fewer blocking rows (see Errors in A, item 1). |
| C-013 | B | 70 | B pre-registers a paired comparison on the same candidate sets, keeps canary and benchmark sets disjoint, and keeps D in shadow if the result is inconclusive. A compares unpaired to a pre-fix baseline, and the input fixes change row counts. |
| C-014 | HYBRID | 65 | A's line pins are precise but incomplete (see Errors in A, item 3). B's new-test groups are more complete and its `--decide flag` default keeps pins green. |
| C-015 | A | 70 | A adds zero model calls and is effort S. A's defensibility needs C02, C12, C15 and C16, but B needs the same fixes. B's cost is L, plus an unbudgeted v1-to-v2 adapter (see Weaknesses in B, item 3). |
| X-001 | B | 85 | A's "a decider can only remove blockers" is false for B as designed. B admits unflagged MAJOR or CRITICAL clusters and a `promoted` relation. |
| X-002 | HYBRID | 60 | Audit D: 49 blocking findings were silently dropped and 4 verdicts flipped FAIL to PASS. B's "merge is faithful" (V7) omits that; audit D's own check X5 says "0 violations ... apart from the dropped-finding effect". But D1 and D6 understate blockers, so A's contamination excuse points the wrong way. |
| X-003 | A | 65 | `COMBO-REPORT.md:291`: the judge's blocking catch can include defects "not blocking_in_implement". The 27 are over-grades on real defects. B's grader would address them, so this does not favour keeping the veto. |
| X-004 | HYBRID | 60 | Replicated-panel means rise with n (1.67, 2.37, 4.75, 3.25 for n=2 to 5) but are confounded, and only one comparison survived audit (`COMBO-REPORT.md:298`). B overstates "E2 measured that direction". A is right that n=2 spans 0.25 to 2.75. |
| X-005 | OPEN | 65 | Decided by C19's verdict word and by whether the rule applies per round. Measure how the spec-panel loop treats `degraded`. If it halts, the one-reviewer fallback breaks. If it ships, `degraded` is cosmetic. |
| X-006 | A | 70 | B's P4 says "fail-closed by construction", but R5 admits an undecidable case is graded not blocking. The agent file agrees: "Otherwise it is not blocking" (`finding-grader.md:17` [VERIFIED]). It is fail-closed only on transport, not on meaning. |
| X-007 | B | 85 | A's "only option that leaves every pin alone" fails against A's own Test item 3. The exact-dict equality at `test_review_ledger.py:299-304` also breaks if `verdict()` gains a key. B's `--decide flag` default leaves the pins green. |
| A-001 | A; QUALIFY | 60 | Holds only for the tasklist and spec lens. E1 shadow runs have no ground truth (`research/05` line 195). A's reflect-post code predicate needs no transfer. B's new `reflect-pre-v1` and `reflect-post-v1` graders do. |
| A-003 | B; QUALIFY | 55 | Absence findings survive only if the anchor quotes the requirement text and a failed locate routes to a re-read, not to suppression. In E2, 46 rows had null spans and 13 of them blocked (audit D, X2). Luna's anchors were verbatim only 91.4% of the time (`COMBO-REPORT.md:294`). |
| A-007 | A; QUALIFY | 60 | A recomputes the flag from the current members each round, so a wrong match mislabels history. B's frozen decision lets a wrongly matched row inherit "not blocking" for a different finding. Holds only if `same_defect` is tightened (audit D, X1 chaining). |

### Strengths claimed for Variant A
1. **It is the only rule with replay evidence, and it needs no model call.** Audit D X5 found 0 row or verdict violations in 264 merges. The caveat is the dropped-finding effect. The cited lines are `ledger.py:187,213-218,274` and `cluster.py:375` [VERIFIED].
2. **Every FAIL is traceable and monotone.** `_brief_ids` and the FAIL rule read the rows directly (`ledger.py:99-104,274` [VERIFIED]). Adding a valid reviewer cannot turn FAIL into PASS.
3. **The error costs are asymmetric.** A false FAIL becomes REVISE or ESCALATE (`ledger.py:93-96` [VERIFIED]). The one blocking tasklist gate defaults its deviation counts to zero (`ensemble.py:779-785` [VERIFIED]). The `degraded` PASS rule mirrors `contract.py:295-296,317-326`.
4. **Reflect-post needs no grader.** `findings_v2.py:161-162` and `contract.py:377-381` already decide by label and class.
5. **A costs nothing that B does not also need.** B's evidence pre-checks and clustering are A's input fixes. A is B minus the grader, so shadowing B later wastes nothing.
6. **It leaves the contract alone.** `LEGAL_MERGE_METHODS` and `CONTRACT_VERSION` are untouched (`panel_lint.py:184-185` [VERIFIED]).
7. **A states its weakest point and a falsifiable test:** rerun the three E2 packages and compare control-package wrong blockers.

### Weaknesses identified in Variant B
1. **V7 overstates faithfulness.** "Merge code is faithful" omits D1: 49 blocking findings dropped and 4 FAIL-to-PASS flips (audit D, [VERIFIED]). B's evidence tables never list D1.
2. **P1 overstates "E2 measured that direction".** Only one pairwise result survived audit (`COMBO-REPORT.md:298`). The trend in the table means is descriptive and confounded.
3. **The document-loop wiring mismatches the code.** `ledger.py` imports `findings` (v1: anchors of 200 characters or fewer, no `channel`, no citation list [VERIFIED]). B's candidate rule needs `channel`. `verify-citations` reads findings-v2 cards only (`verify_cmd.py:1`). B's R1 admits the E2 reports are v1 and "not verified" usable. The replay gate may need an adapter, which B does not cost.
4. **P4's "fail-closed by construction" is contradicted by R5.**
5. **"PENDING mirrors stoprule" is only approximate.** Stoprule reports unconfirmed claims as FAIL `incomplete` (`stoprule.py:1185-1189` [VERIFIED]), not as a new exit code.
6. **Promotion is the one place B loses A's subset guarantee.** It has no precision evidence (R8).
7. **Canaries do not catch leniency on real items.** `evaluate_reply` rejects a batch only on a wrong canary answer (`stoprule.py:819-830` [VERIFIED]). B says so. Validators are agreeable (true-negative rate below 25% in one external study).
8. **The shipped agent pins `model: sonnet` (`finding-grader.md:5` [VERIFIED]).** E2's revised panel includes sonnet. Independence needs the generalised file B plans.
9. **No grader token or accuracy figure exists.** A B1-B3 rubric also excludes "gaps inferable from nearby text", and E2 ground truth comes from implement runs, not from that rubric. Recall loss is unmeasured.

### Errors you found in your own Variant A
1. **The contamination argument runs the wrong way.** D1 (49 dropped blocking findings) and D6 (a mega-row counts as one blocking row) lower the counted blockers. Fixing them likely raises wrong blockers, so "hardening lowers wrong blockers" lacks support. Only D5 (13 null-span blocking rows) pushes the other way. Steps 2 and 6 and Risk 1 should say so.
2. **The Design step 6 and How it works step 6 claim `row.blocking = cluster.blocking_any (ledger.py:187)` is wrong.** `ledger.py:187` runs `any(...)` over v1 groups from `fnd.cluster`. It does not read `cluster.py` output. These are two copies on two schema versions.
3. **"Only option that leaves every pin alone" (step 7) contradicts Test item 3.** A did not check the exact-dict equality at `test_review_ledger.py:299-304`, which breaks if `verdict()` gains `degraded`. A also missed one-reviewer PASS paths at `:307-315` and `:396-403`. `test_review_cli.py:348` asserts exit 0 and decision PASS.
4. **The degrade rule is not scoped to a round.** The table says "on round 1", but the design says any would-be PASS. With one-reviewer re-reviews as the default, every final PASS could be degraded.
5. **Step 1 "recall ceiling" fails against B's promotion.** X-001 is false as stated for B's design.
6. **E-7's cap is weakly evidenced.** `research/11` §12 supports 2 as well, and n=3 panels still show 1.8-3.2 wrong blockers.

### Concessions
- E2 precision is bad, and A's fix is a prediction (Risk 1).
- In the spec lens a reviewer still grades its own findings. The 27 over-grades came from that.
- A's evidence gate suppresses without naming a resolver. One reviewer can still clear a row until D2 and C13 land.
- A's `degraded` rule is under-specified and touches more tests than A claims.
- B's staged rollout and paired baseline are a better measurement design. A only wins on what runs today.

| Status | Result |
|---|---|
| DONE | Round 1 statement for Variant A; 33 stances; code lines, test lines and E2 table rows re-read. |
| NEXT | None from me; the lead scores the points. |

### Variant B Advocate (agent c05-advocate-B-r1, general-purpose, default model, focus: correctness, risk, test-coverage)

### Position
Variant B is the better design, but only as a staged, shadow-first change. The veto stays the live rule until a paired replay on the E2 packages shows the grader gives fewer wrong blockers without losing real-blocking recall. Variant A is cheaper and safer to ship today, but it leaves the same reviewer flagging and deciding, and its precision claim is unmeasured, as A itself says.

### Steelman of Variant A
A's strongest case has four parts.

- **The veto is a ceiling.** Any decider layered on the any-reviewer candidate list can only shrink the FAIL set. Measured real-blocking recall is already 0.17-1.20 of 8 per run (`COMBO-REPORT.md` rows 315-333 [VERIFIED]), so there is little recall to spend.
- **B's grader is unmeasured.** B's own evidence shows validators are agreeable (X2), and B concedes this in its weakest-point section. A grader that rubber-stamps would be the veto plus one model call.
- **The 27 over-grades are real defects.** The 65-versus-38 gap is 27 real ground-truth defects that were flagged blocking but did not block implementation. A reads this correctly from the report's definition of `gt_covered_blocking` [VERIFIED, "FINAL RESULTS" item 1].
- **A's mechanics are sound.**
  - The asymmetric verdict agrees with `contract.py:295-296`.
  - A's cost is S, with zero extra model calls.
  - Its fallback, a verification filter on singletons only, reuses everything A builds.

### Per-point stances

| Point | Stance | Conf. | Evidence |
|---|---|---|---|
| S-001 | EQUAL | 95 | Same seven H2 sections in the same order. |
| S-002 | EQUAL | 70 | Hierarchy is presentation only. |
| S-003 | EQUAL | 60 | B's source column and A's inline counter-readings each add something. B tags unread facts `[VIA]` honestly. |
| S-004 | B | 60 | B's R1-R11 table has a Residual column that forces a statement of what remains. |
| S-005 | B | 80 | B has four ordered rollout steps with `--decide flag` as the default. A has one benchmark gate (Risk 1, Test item 9) and no staging. |
| S-006 | HYBRID | 65 | Take B's 16 new-test groups. Add A's accounting of the three one-reviewer PASS pins (`test_review_ledger.py:296-298`, `:468-472`; `test_review_cli.py:328-348`) [VERIFIED]. Also add A's rule-parity and monotonicity tests. |
| S-007 | EQUAL | 70 | Both tag provenance. A's "[CODE] re-read" is stronger, B's "[VIA]" is more candid. |
| S-008 | EQUAL | 65 | Both put the weakest point where a reader will see it. |
| C-001 | B | 60 | Today each reviewer grades its own findings (research 05 line 289 [VERIFIED]). 26 of 42 MAJOR findings were `blocking:false` (05:186-189 [VERIFIED]), so the flag reflects labelling habit. B's gain depends on the replay. |
| C-002 | HYBRID | 80 | B has no reviewer-count guard, so one reviewer plus an approving grader yields PASS. A's degrade rule (`contract.py:295-296`) should sit on top of B's `PENDING`. |
| C-003 | HYBRID | 65 | Promotion is the only path either variant has to add recall (26 non-blocking MAJOR in shadow runs). It also risks over-blocking follow-ups (B R8). Run `promoted` as counted-only until the replay measures it. |
| C-004 | B | 60 | B grades singletons. A only counts them, and its own named fallback is B restricted to singletons. |
| C-005 | OPEN | 70 | Neither mechanism is evidenced. On the control package, wrong blockers do not rise with panel size: 5 reviewers give 0.25, and 2 reviewers give 1.25-1.50 (rows 315-333 [VERIFIED]). A paired replay with the veto as baseline would decide it. |
| C-006 | B | 72 | `ledger.py:213-218` lets one non-blocking re-report clear a row. The `:518-544` test pins that. A admits this in Risk 3 and covers only the invalid-reviewer case. B's frozen decision closes it, with a re-grade when the cited text changes. |
| C-007 | A | 65 | A's gate is hard. B's grader treats `unverified` evidence as true-but-noted (`finding-grader.md:19` [VERIFIED]), so B can block on an unconfirmed quote when some citations survive. |
| C-008 | HYBRID | 70 | For reflect-post, a code predicate on `deviation_class` (A) is enough, since `contract.py:377-381` is deterministic. For spec and tasklist, B's hash-frozen rubric (`rubric.md:1`). |
| C-009 | HYBRID | 65 | A's partial-reviewer abstention and B's canary and rerun logic (`stoprule.py:819-830`, `:1176-1189` [VERIFIED]) cover different layers. B needs its layer only because it adds a decider. |
| C-010 | HYBRID | 60 | A is the smaller surface. But `EXIT_BY_DECISION = {"PASS": 0, ...}` (`ledger_cmd.py:13` [VERIFIED]) means A's `degraded` PASS exits 0 unless C19 changes it. Adopt B's explicit exit 12 style for A's marker. |
| C-011 | EQUAL | 70 | Both keep the debate and contract 1.8.0, and both write only to nested `telemetry:`. |
| C-012 | OPEN | 70 | A's D1 point does not explain wrong blockers. Dropped findings only remove blockers (four FAIL-to-PASS flips). D5 and D6 could inflate them. B's V7 (merge code faithful) does not prove policy either. Rerun with D5 and D6 fixed, veto and grader on the same candidates. |
| C-013 | B | 72 | B's gate is paired, on the same candidate sets, with canary and benchmark sets disjoint and an inconclusive result staying in shadow. A compares against a pre-fix baseline from different runs, using an "owner-set tolerance" that has no number. |
| C-014 | HYBRID | 65 | B's default flag keeps existing tests green. A found the strict dict equality at `test_review_ledger.py:299-304` [VERIFIED] but contradicts itself on `:279-300` (see A weaknesses). |
| C-015 | A | 90 | Cost S against L, with zero extra model calls against one grader call per batch. |
| X-001 | B | 75 | A's universal ("none can add recall") is false for B as designed. B's `promoted` relation and its MAJOR-or-CRITICAL candidate rule add blockers. The risk of that is real (R8). |
| X-002 | OPEN | 70 | See C-012. |
| X-003 | HYBRID | 65 | A is right about what the 27 are. B is right that they are false blockers for a gate meant to predict implement-blocking. At loop level, `ledger.py:93-96` turns a persistent FAIL into REVISE and then ESCALATE even after the real blockers are fixed. |
| X-004 | A | 75 | The data does not show a size effect. Only one panel (4.75 wrong blockers) survives the audit. Replicated panels show p 0.54-1.0, and the 5-reviewer panel has 0.25 control wrong blockers [VERIFIED]. |
| X-005 | HYBRID | 65 | The tension in A is real. "Usable fallback" holds only if consumers accept an uncertified PASS, and the CLI currently exits 0 for it (`ledger_cmd.py:13`). |
| X-006 | HYBRID | 80 | "Fail-closed" (P4) is true for transport and format failures. For judgment, `finding-grader.md:17` returns "not blocking" when B1-B3 are not met [VERIFIED], so B fails open there (R5). |
| X-007 | B | 70 | A's own Test item 3 changes three existing tests, and the `degraded` key breaks the strict dict at `:299-304`. B's default-flag path changes none until the flip. |
| A-001 | B; QUALIFY | 60 | Transfer holds only for the spec and tasklist lenses (E2 ran the spec brief). Reflect-post is code-decided and reflect-pre has no ground truth. B's per-lens gates handle this. A's single benchmark does not. |
| A-003 | B; QUALIFY | 60 | The parser requires an anchor or citations (`findings_v2.py:124-125` [VERIFIED]). B's rubric tells the reviewer to quote the incomplete requirement for an omission (`rubric.md:4` [VERIFIED]). It holds only if absence findings anchor to existing text, which A's gate does not specify. |
| A-007 | A; QUALIFY | 60 | `fp` is a hash of section and refs, and `same_defect` needs non-empty refs (`findings.py:340-379` [VERIFIED]). A wrong match under A self-corrects next round. Under B it inherits a frozen decision, so B's "cited text changed" guard must actually be implemented. |

### Strengths claimed for Variant B
1. **It is the only design where the flagger is not the judge.** Reviewers self-grade (research 05 line 289 [VERIFIED]), and 27 of 65 judge-blocking catches were not real blockers (E2 "FINAL RESULTS" item 1 [VERIFIED]). B moves the call to a fresh context that cannot see reviewer ids, severity or labels.
2. **It removes the single-report un-block path.** `ledger.py:216-218` takes the current round's flag, and the test at `test_review_ledger.py:518-544` pins that [VERIFIED]. B stores the decision once, with the rubric hash, and re-grades only if the cited text changes.
3. **It is safer to ship.** The default `--decide flag` keeps current behaviour. Shadow mode writes only to `telemetry:`. It also records `overruled` and `promoted` counts, which A's `singleton_blockers` cannot give (it counts singletons but never measures their precision).
4. **Its gate design is stronger.** The replay is paired on identical candidates and pre-registered. Canary and benchmark sets are disjoint. An inconclusive result keeps D in shadow. A's pass condition is "an owner-set tolerance" on unpaired runs.
5. **It reuses tested machinery.** `stoprule.py` already has `build_batches` (657), `render_batch` (721), canary-checked reply validation (819-830) and "silence never passes" (1176-1189) [VERIFIED]. `canaries.json` holds 8 entries.
6. **Blindness is enforced by construction.** The renderer never receives the fields the E2 judge leaked. A test pins that.
7. **Policy is versioned.** The rubric's sha256 is stored in the ledger, and a change becomes a new version, as `rubric.md:1` already says.

### Weaknesses identified in Variant A
1. **The subset claim fails for B.** A's E-4 and Correctness step 1 say no other decider "can add recall". B's candidate rule and `promoted` relation do add blockers.
2. **A's D1 argument misattributes the wrong blockers.** D1 silently dropped 49 blocking findings and flipped four FAIL to PASS ("FINAL RESULTS" item 2 [VERIFIED]). That depresses recall and cannot inflate wrong blockers. Only D5 and D6 could.
3. **The cap of three finders is not supported by the control column.** A cites ember+sonnet at 0.25 wrong blockers, which is the defect-rich column. Its control wrong blockers are 1.25 (row 315 [VERIFIED]). The 2-reviewer panels at 1.25-1.50 are worse than the 3-reviewer default at 0.83. The 5-reviewer panel is at 0.25.
4. **"FAIL is the right verdict on a defect-rich plan" (step 2) is a snapshot argument.** A veto keeps FAIL after the real blockers are fixed. `ledger.py:93-96` then converts that to REVISE and finally ESCALATE.
5. **The certification safeguard is undefined.** A's `degraded` PASS would exit 0 (`ledger_cmd.py:13`) unless C19 changes it. Exit-code consumers would see an ordinary PASS.
6. **A's test accounting is inconsistent.**
   - Item 1 lists `:279-300` as staying green. Item 3 changes `:296-298`, which is inside that range.
   - The strict dict equality at `:299-304` would also break if `degraded` is added to `verdict()` [VERIFIED].
   - Correctness step 7 ("only option that leaves every pin alone") contradicts item 3.
7. **A depends on D2, which is not implemented.** `ledger.py:254-258` moves a `resolved_check` row to `resolved` whenever it is absent from `members_by_lid`. It never checks `block_ok` [VERIFIED]. This is a prerequisite problem, and B's status clearing shares it.
8. **Self-grading remains in the spec lens.** A's own Risk 2 admits it, and it is the regime that produced the 27 over-grades.

### Errors you found in your own Variant B
1. **P1 overreaches.** "E2 measured that direction" rests only on the defect-rich wrong-blocker column, which E2 calls an upper bound. On control, the trend is absent (5 reviewers 0.25; 2 reviewers 1.25-1.50) [VERIFIED]. The formula 1-(1-q)^n is a model, not an E2 finding.
2. **K1 overstates the grader inputs.**
   - findings-v2 has no `outcome` field. `grep` finds none in `src/superclaude/cli/review` besides telemetry [VERIFIED].
   - The stoprule claim record requires an `outcome` of at least 8 words (`stoprule.py:321`).
   - B2 ("concrete wrong outcome") must therefore be judged from the 300-character claim, and nothing enforces that the claim states a consequence.
3. **V7 does not support its conclusion.** "Merge code faithful" excludes merge bugs only. It does not exclude input defects D5 and D6. B also omits D1.
4. **P4 "fail-closed by construction" is true only for procedure.** R5 and `finding-grader.md:17` show a fail-open default for undecidable cases.
5. **The grader agent pins `model: sonnet`** (`finding-grader.md:5` [VERIFIED]). Sonnet is also an E2 reviewer. The class-disjoint selection needs the model to be overridable, and B does not say so.
6. **B1 trust is weaker than A's gate.** The grader accepts `unverified` evidence as true (`finding-grader.md:19`).
7. **Two pre-flip inaccuracies are carried over.**
   - The promotion claim "agent exists only under `~/.claude/`" is correct. `ls src/superclaude/agents` shows no grader [VERIFIED].
   - R1 notes the replay may lack anchors in the E2 reports and says this was not verified. I did not verify it either.

### Concessions
- No evidence exists that the grader is accurate. Validators confirm too readily (X2). A lenient grader would be the veto plus cost.
- B costs L and adds one serial step per round. Canaries add 25% overhead per batch. No token cost was measured.
- A's degrade rule (U-001) has no counterpart in B, and B should adopt it.
- A's `singleton_blockers` counter is cheap, and B should add it.
- A is right that the 65-versus-38 gap is about severity on real defects. It is not about invented defects.
- The replay has low power. The control package has 2 non-blocking defects and n of 4-6 per panel. B's own R1 residual admits an inconclusive replay is likely.
- A single grader is a single point of error. A second vendor-disjoint grader is not built in round one (R4).
- The E2 evidence is thin for both variants. Neither can claim measured precision.

### Round 1 per-point tracking (orchestrator, derived mechanically from the two stance tables above)

Agreement rule used throughout: two advocates agree on a point only when their stances are identical (A with A, B with B, EQUAL with EQUAL, HYBRID with HYBRID where the named components are compatible, OPEN with OPEN). For the shared assumptions A-001, A-003, A-007 the compared item is the ACCEPT/REJECT/QUALIFY response. A mismatch such as EQUAL versus B or HYBRID versus A is not agreement even when the substance is close; Round 2 is the place to close it.

| Point | Level | Advocate A | Advocate B | Agreed | Agreed outcome |
|-------|-------|------------|------------|--------|----------------|
| S-001 | L1 | EQUAL (90) | EQUAL (95) | yes | EQUAL |
| S-002 | L1 | EQUAL (75) | EQUAL (70) | yes | EQUAL |
| S-003 | L2 | B (55) | EQUAL (60) | no | |
| S-004 | L1 | B (60) | B (60) | yes | B |
| S-005 | L2 | B (75) | B (80) | yes | B |
| S-006 | L2 | HYBRID (60) | HYBRID (65) | yes | HYBRID (B's tests plus A's parity and monotonicity tests) |
| S-007 | L1 | EQUAL (80) | EQUAL (70) | yes | EQUAL |
| S-008 | L1 | EQUAL (75) | EQUAL (65) | yes | EQUAL |
| C-001 | L2 | HYBRID (65) | B (60) | no | |
| C-002 | L3 | HYBRID (65) | HYBRID (80) | yes | HYBRID (A's degrade rule on top of B's PENDING) |
| C-003 | L3 | A (60) | HYBRID (65) | no | |
| C-004 | L2 | EQUAL (60) | B (60) | no | |
| C-005 | L2 | HYBRID (60) | OPEN (70) | no | |
| C-006 | L3 | B (65) | B (72) | yes | B |
| C-007 | L3 | B (60) | A (65) | no | |
| C-008 | L2 | HYBRID (70) | HYBRID (70) | yes | HYBRID (code predicate for reflect-post; frozen rubric for spec) |
| C-009 | L3 | HYBRID (70) | HYBRID (65) | yes | HYBRID (both layers needed) |
| C-010 | L2 | A (60) | HYBRID (60) | no | |
| C-011 | L2 | EQUAL (70) | EQUAL (70) | yes | EQUAL |
| C-012 | L2 | HYBRID (65) | OPEN (70) | no | |
| C-013 | L2 | B (70) | B (72) | yes | B |
| C-014 | L2 | HYBRID (65) | HYBRID (65) | yes | HYBRID |
| C-015 | L2 | A (70) | A (90) | yes | A |
| X-001 | L3 | B (85) | B (75) | yes | B's side (A's subset claim is false for B as designed) |
| X-002 | L2 | HYBRID (60) | OPEN (70) | no | |
| X-003 | L2 | A (65) | HYBRID (65) | no | |
| X-004 | L2 | HYBRID (60) | A (75) | no | |
| X-005 | L3 | OPEN (65) | HYBRID (65) | no | |
| X-006 | L3 | A (70) | HYBRID (80) | no | |
| X-007 | L2 | B (85) | B (70) | yes | B's side (A's "only option" claim fails) |
| A-001 | L2 | QUALIFY (60) | QUALIFY (60) | yes | QUALIFY (holds for the tasklist and spec lens only) |
| A-003 | L3 | QUALIFY (55) | QUALIFY (60) | yes | QUALIFY (holds only if absence findings anchor to existing text and a failed locate routes to re-read, not suppression) |
| A-007 | L3 | QUALIFY (60) | QUALIFY (60) | yes | QUALIFY (needs `same_defect` tightened and an implemented cited-text-changed guard) |

Round 1 result: 20 of 33 points agreed = 60.6%. Not agreed (13): S-003, C-001, C-003, C-004, C-005, C-007, C-010, C-012, X-002, X-003, X-004, X-005, X-006.

Taxonomy coverage after Round 1: L1 points debated 5 of 5, L2 points debated 18 of 18, L3 points debated 10 of 10. No level has zero coverage, so no forced round is triggered.

Both advocates volunteered corrections to their own variant that matter for the later steps (the Round 2 briefs repeat them as the disputed facts): A-adv found that A's contamination argument runs the wrong way for D1 and D6 (they depress blockers; only D5 inflates), that `ledger.py:187` runs on findings v1 groups (not on `cluster.py` v2 output), and that A's test accounting is incomplete (`test_review_ledger.py:299-304` exact dict, `:307-315`, `:396-403`, `test_review_cli.py:348`). B-adv found that B's P1 overreaches ("E2 measured that direction"), that findings-v2 has no `outcome` field although the stoprule claim record needs one, that B's grader file pins `model: sonnet`, and that the grader accepts `unverified` evidence as true. Both found that X-001 and X-007 go against A, and that P4 "fail-closed" versus R5 (X-006) is a real tension in B.

## Round 2: Rebuttals

Round 2 is sequential: Advocate A answers first (it sees both Round 1 statements); Advocate B answers second (it sees both Round 1 statements and A's rebuttal). Round 2 agents were spawned unnamed, so their text came back inline and is pasted verbatim.

### Variant A Rebuttal (agent general-purpose, Round 2)

### Response to criticisms

1. **Subset claim fails for B (B1, X-001). CONCEDE.** My "no decider can add recall" holds only for filters. The merged text should say the veto's FAIL set is the base. A decider may demote clusters, and may promote only in shadow, as a counted `promoted` relation that cannot raise a FAIL until its precision is measured. That is C-003 as HYBRID.
2. **D1 cuts the other way (B2). CONCEDE, and it is worse than Round 1 said.** The E2 audit lists a control-package FAIL→PASS flip caused by a dropped blocker (n5-sonnet-ember, COMBO-REPORT "FINAL RESULTS" item 2). Fixing D1 therefore likely raises control wrong blockers. Only D5 (13 null-span blocking rows) pushes down. "Hardening lowers wrong blockers" has no support, so A's precision claim is a bare prediction. The replay must fix D1 before either arm runs, or the baseline is not clean. B needs the same fix.
3. **Cap of three (B3). CONCEDE the cap as a precision lever.** Control wrong blockers (column 8 of the table at COMBO-REPORT:304; the E2 report is cited below as CR) by panel size:

   | Panel size | Rows (CR line: control wrong blockers) | Control wrong blockers |
   |---|---|---|
   | 2 | 315: 1.25; 317: 1.50; 336: 1.25 | mean 1.33 |
   | 3 | 331: 0.83; 320: 1.00; 333: 1.20; 323: 1.40; 319: 1.60 | mean 1.21 |
   | 4 | 332 | 1.50 |
   | 5 | 316: 1.75; 318: 0.25 | 1.75 and 0.25 |

   There is no size effect on control. B's "5 reviewers give 0.25" is the best of two 5-reviewer rows; the other is 1.75. I also cited the wrong column: `ember + sonnet` 0.25 is the defect-rich figure (row 315), and its control figure is 1.25. Keep the cap only as a cost cap, since tokens are the one difference that survived the E2 statistics (p 0.002-0.009).
4. **"FAIL is right on a defect-rich plan" is a snapshot argument (B4). CONCEDE in part, REFUTE the escalation claim.** The control FAIL rate is the right metric, and my step 2 should go. But `ledger.py:93-96` only turns a persistent FAIL into ESCALATE if the review re-finds the row. The default re-review is one reviewer (`document_review_loop_prompts.md:70`), and a revised wrong blocker usually becomes `resolved_check` and clears (`ledger.py:254-257`). The real cost of a false FAIL is a wasted revision and the reviser's edits to text that was fine. That cost is smaller than ESCALATE but not zero.
5. **A degraded PASS exits 0 (B5). CONCEDE.** `ledger_cmd.py:13` maps PASS to exit 0, and `ledger_cmd.py:109` exits by decision word. The fix is to keep PASS and exit 0 for existing callers, because test_review_cli.py:348 asserts exactly that. Put `degraded` on the `merge_round` result and round record, and add a pre-`verdict:` line to the merged report. Say in the spec-panel coordinator prompt that a degraded PASS is reported to the user as uncertified. Add B's exit 12 only for `PENDING` under `--decide grader`.
6. **Test accounting is inconsistent (B6). CONCEDE the wording, REFUTE the damage.** See F2. Exactly one assertion breaks, and only if `verdict()` itself gains a key. Placing the key elsewhere avoids even that. I also missed `defer()` (see New evidence).
7. **A depends on D2, which is not coded (B7). CONCEDE the dependency, REFUTE the severity.** See F6. `block_ok` already exists, so the fix is about three lines. It can only misfire in rounds with two or more reviewers, which is not the default re-review. B's status clearing shares the gap.
8. **Self-grading stays in the spec lens (B8). CONCEDE.** One caution for the replay: the grader's rubric (B1-B3) asks whether a reader produces a wrong outcome. E2's "real blocking" is `blocking_in_implement`. Nobody has shown the grader closes the 27 over-grades, so the replay must score both arms against `blocking_in_implement`.

**B's self-corrections that bear on A:**
- B's P1 overreach is a point for A (see X-004).
- B's "no `outcome` field" (K1) is a point for A (see F4).
- B's V7 omission of D1 is a point for A.
- B's admission that the grader pins `model: sonnet` is mostly neutralised: the Agent tool's `model` parameter overrides the frontmatter pin. Whether it can reach non-Anthropic classes is UNVERIFIED.
- B's R5 supports A on X-006.
- B's "B1 trust weaker than A's gate" (`finding-grader.md:19`) is a point for A on C-007.

### Updated assessment of Variant B

B is better than I credited on three points:
- The frozen-decision store closes the path where a flag flips non-blocking on re-report (`ledger.py:216-218`, pinned at test_review_ledger.py:518-544).
- Shadow-first with a paired replay is the right measurement design.
- Blindness by construction answers a real E2 leak.

B is worse than B admits on two points:
- It routes the document loop through `merge_round` (variant-2:70). That function uses the v1 `findings` module, which has zero mentions of `channel`, `citations` or `deviation_class`. B's candidate rule (`channel == defect`) and its K1 inputs do not exist on that path, and `verify-citations` reads v2 cards only (`verify_cmd.py:1`). B needs an adapter and has not costed it.
- It makes "undecidable means not blocking" the grader default (F5).

My view is that B is the right destination and A the right interim. A is not "B minus the grader" until D1, D2 and the degrade scope are fixed.

### New evidence

- **`defer()` recomputes PASS without reviewer count.** `ledger.py:356-360` sets verdict and decision to PASS when the brief empties, so a human deferral on a one-reviewer loop would yield a certified PASS. A's `degraded` must be recomputed there. Neither variant noticed.
- **D2 is pinned by an existing test.** test_review_ledger.py:376-385 asserts `resolved` with one invalid reviewer. The docstring at `ledger.py:112` says an invalid reviewer is "skipped for clearing", but the code does not do that.
- **A's gate has a v1 signal.** A missing anchor gives `span is None` on the live path (test_review_ledger.py:408-417), so A's evidence gate is cheap there. B's citation pre-check is not available on that path.
- **Anchor limit.** The 200-character anchor limit (`findings.py:104`) drives D1 for both variants.

### Facts verified this round

- **F1 VERIFIED.**
  - `ledger.py:15` imports v1 `findings`, and `ledger.py:165` calls `fnd.cluster`.
  - `merge_cmd.py:109` calls `led.merge_round`.
  - `cluster.py:64-65` imports only `refs_norm` and `_check_citation`.
  - So `row.blocking` at `ledger.py:187` is not `cluster.blocking_any` (`cluster.py:375`); they are two copies.
  - B's "those two lines read the stored decision" also describes two copies, and B must edit both.
  - Consequence: the parity test must span both, and B's adapter cost stands.
- **F2 VERIFIED.**
  - `test_review_ledger.py:299-304` is exact dict equality on `verdict()`. It breaks only if `verdict()` gains a key.
  - `:296-298` is a tuple compare and `:307-315` is a key access. `:396-403` accesses keys on `verdict()` after `defer`. `:468-472` asserts `splitlines()[-1] == "verdict: PASS"`, so a degraded note must go before that line.
  - `test_review_cli.py:348` asserts exit 0 and `decision == "PASS"`.
  - Nothing else breaks provided decision words, exit codes and last report line stay as they are.
  - Consequence: A's claim "three tests change" overstates the damage, and "only option that leaves every pin alone" is wrong by one assertion. B's `--decide flag` default also makes B literally zero-touch.
- **F3 VERIFIED**, with the table above.
  - 2-reviewer panels (1.25-1.50 on control) are worse than the default 3-panel (0.83), but not worse than the other 3-panels (1.00-1.60).
  - `ember + sonnet` 0.25 is the defect-rich column.
  - The consequence is that both A's cap and B's P1 lack support on control.
- **F4 VERIFIED.**
  - Findings-v2 has no `outcome` field. Grep of `src/superclaude/cli/review` finds it only as a telemetry record kind (`telemetry.py:256`).
  - Stoprule's claim record requires `outcome` of at least 8 words (`stoprule.py:321`). `SKILL.md:41` requires a "named reader, implementer or test".
  - A finding's `claim` is at most 300 characters (`findings_v2.py:111`; `findings.py:118`). The brief says it names the wrong outcome (loop prompts :60) but nothing enforces a named reader.
  - So B2 is graded from the claim, with no enforced consequence statement. Consequence: B needs a claim-shape check or an `outcome` field before the grader's B2 means anything.
- **F5 VERIFIED.**
  - `finding-grader.md:5` pins `model: sonnet`.
  - `:17` says "Otherwise it is not blocking".
  - `:19` says to grade unverified evidence "as if that evidence were true".
  - Consequence: fail-open on meaning, and trust in unverified citations. The merged text needs an affirmative-demotion rule (see X-006).
- **F6 VERIFIED.**
  - `ledger.py:254-257` moves a `resolved_check` row to `resolved` when it is absent from `members_by_lid`, and never reads `block_ok`.
  - The "partial reviewer" concept does not exist. Grep finds no `partial`, `abstain` or `degraded` in `cli/review`.
  - A round with no valid block is refused (`:150-157`), so the gap only bites when two or more reviewers ran and one was invalid. That is not the default re-review.
- **F7 VERIFIED.**
  - Line 70 of `document_review_loop_prompts.md` gives "a panel for a first review, one reviewer for a re-review by default".
  - A's table scopes the PASS rule to round 1. But Design step 6, the `degraded` field definition ("fewer than two reviewers had a valid block") and Risk 7 are not scoped.
  - Read literally, every PASS reached after a revise would be degraded, because the final round has one reviewer. The merged text must scope certification to round 1 of the loop and let later rounds inherit it.

### Updated stances

| Point | Stance | Conf | Recommended merged-proposal position |
|---|---|---|---|
| S-003 | EQUAL (was B) | 60 | Use B's source-column tables plus a counter-reading column, and tag every unread fact `[VIA]`. |
| C-001 | HYBRID | 65 | The veto is live now and the grader runs in shadow. The grader decides per lens only after the paired replay passes, as B's own rollout says. |
| C-003 | HYBRID (was A) | 65 | Run `promoted` as a counted relation in shadow. It never raises a FAIL until its precision is measured. |
| C-004 | HYBRID (was EQUAL) | 62 | Record `singleton_blockers` from per-cluster `reviewers[]`. Singletons are the first population the grader goes live on. |
| C-005 | OPEN (was HYBRID) | 70 | Drop the cap as a precision lever and keep it as a cost cap. The replay reports wrong blockers by n. |
| C-007 | HYBRID (was B) | 62 | An unresolved citation cannot be effective-blocking (A's gate). A named resolver re-reads it and routes absence findings to the quoted requirement text. The grader never treats `unverified` as sole support. |
| C-010 | HYBRID (was A) | 62 | Keep decision words and exits 0/10/11. Add `degraded` as a field and a report line. Add exit 12 for `PENDING` only under `--decide grader`. |
| C-012 | OPEN (was HYBRID) | 70 | Rerun with D1, D5 and D6 fixed. Run veto and grader on the same candidates, scored on `blocking_in_implement`. |
| X-002 | OPEN (was HYBRID) | 68 | V7 must list D1, and E-5 must state that D1 pushes wrong blockers down. Attribution is unmeasured. |
| X-003 | HYBRID (was A) | 65 | The 27 are real defects over-graded. A gate meant to predict implement-blocking is scored against that, and a persistent FAIL escalates only if the reviewer re-finds the row. |
| X-004 | A | 65 | Delete both "E2 measured that direction" and the cap argument. Defect-rich means rise with n (1.67, 2.37, 4.75, 3.25) but are confounded. Control is flat. |
| X-005 | HYBRID (was OPEN) | 68 | Certification is a loop property set at round 1 (two or more valid blocks) and inherited later. `defer()` recomputes it. Exits stay 0. |
| X-006 | HYBRID (was A) | 75 | A grader may demote only with an affirmative "not blocking". On doubt it keeps the reviewer's flag, or goes to `PENDING`. |

**Previously agreed points whose stance I change:** none. Confidence changes only. X-007 stays B at 70, because A's break is one assertion and B's default flag is zero-touch. C-014 stays HYBRID, with F2's accounting replacing both variants' lists.

### Remaining disagreement

**What B still gets wrong:**
- It claims "fail-closed by construction" while the rubric default fails open.
- It never costs the v1-to-v2 adapter.
- It treats an inconclusive replay as unlikely when its own R1 says it is likely: the control package has two non-blocking defects and n is 4-6.
- It offers no evidence the grader closes the 27 over-grades.
- It takes `unverified` evidence as true.

**What I got wrong:**
- The contamination argument had the wrong sign.
- The cap rested on the wrong column.
- The `degraded` rule was unscoped.
- I missed `defer()`.
- I missed that D2 and the abstain rule are not code yet.
- "Only option that leaves every pin alone" was false.
- "Recall ceiling" was wrong once promotion is allowed.

The honest summary is that A is a safe interim with an unmeasured precision claim, and that B's measurement design should be adopted whole.

### Variant B Rebuttal (agent general-purpose, Round 2)

### Response to criticisms

1. **V7 omits D1 (A's B-weakness 1). CONCEDE.** `COMBO-REPORT.md` lines 291-292 list silent drops of 49 blocking findings and four FAIL-to-PASS flips. Fix: the merged text names D1, D5 and D6 as replay prerequisites for both arms, and says D1 pushes counted wrong blockers down.

2. **P1 "E2 measured that direction" (weakness 2). CONCEDE, and the data is worse for P1 than A showed.** I summed the full AS SCORED table (rows 306-337), weighted by run count. Control wrong blockers by panel size:

   | Panel size | Control wrong blockers per run |
   |---|---|
   | 1 | 1.00 |
   | 2 | 1.27 |
   | 3 | 1.05 |
   | 4 | 1.33 |
   | 5 | 0.89 |

   The audit-clean subset is equally flat (1.00, 1.46, 1.06, 1.17, 1.00). On the defect-rich packages the single-reviewer rows have the highest wrong-blocker counts (sol 3.00, terra 4.00), which cuts against 1-(1-q)^n. Fix: P1 becomes "g is independent of n by construction; E2 neither supports nor refutes any size effect".

3. **The document loop is on v1 (weakness 3). CONCEDE the claim, REFUTE the cost.**
   - Findings-v1 has `id, severity, blocking, category, anchor (12-200 chars), anchor2, refs, claim (<=300)` (`findings.py:90-121`). It has no `channel`, citations, `deviation_class` or `outcome`.
   - B's K1, candidate rule and `verify-citations` step are v2-only.
   - The adapter is small, not a v1-to-v2 conversion:
     - candidate = `blocking or severity in {MAJOR, CRITICAL}` with no channel test, since v1 findings are all defects;
     - evidence pre-check = `anchor_status == "missing"` (`findings.py:350`, `span is None` on the row);
     - the renderer reads the row's `claim`, `anchor` and the document text at `span`.
   - My estimate is 50-100 lines plus a second renderer and a parity test across both paths. That is unmeasured.
   - B must state this and cost it.

4. **"Fail-closed by construction" versus the rubric default (weakness 4). CONCEDE.** `finding-grader.md:17` says "Otherwise it is not blocking". B is fail-closed on procedure only. Fix: the generalised grader replies `true`, `false` or `undecidable`, and `false` must name the failed criterion (B1, B2 or B3). `undecidable` on a reviewer-flagged cluster keeps the reviewer's flag, or goes to PENDING. On an unflagged candidate it means no promotion. This needs `spec-v2`, because `rubric.md:1` says a rubric change is a new version.

5. **"PENDING mirrors stoprule" (weakness 5). CONCEDE as approximate.** I did not re-read `stoprule.py:1185-1189`. I accept A's merged position: keep decision words and exits 0/10/11, and use exit 12 only for PENDING under `--decide grader`. Exit 12 also needs an `EXIT_BY_DECISION` entry (see G2).

6. **Promotion has no precision data (weakness 6). CONCEDE.** `promoted` is counted in shadow and cannot raise a FAIL until its precision is measured on the replay.

7. **Canaries do not catch leniency (weakness 7). CONCEDE, partly REFUTE.** B said this itself. A's veto has no check at all. Fix: the replay adds the known E2 wrong blockers as a leniency probe, and the report states the grader's true-negative rate.

8. **The grader pins `model: sonnet` (weakness 8). CONCEDE in part; see G5.** The stoprule dispatch passes no model, so the frontmatter pin governs. The override reaches Anthropic aliases only.

9. **No accuracy figure, and B1-B3 versus `blocking_in_implement` (weakness 9). CONCEDE.** Fix: the replay scores both arms against `blocking_in_implement`, as A asks. It also reports where grader-blocking and implement-blocking disagree.

**A's Round 2 claims that cut against B:**

- **Missing `outcome` field. CONCEDE.** I confirmed v1 has none. I did not grep v2. Fix: the reviewer brief and the claim-shape check must require a named reader and wrong result in the claim, or the schema gains an `outcome` field. Otherwise B2 is ungradable and the item is `undecidable`.
- **`unverified` evidence graded as true. CONCEDE.** Fix: adopt stoprule's seal rule (G5). A claim whose cited text is not found is never graded as blocking.
- **Replay power. PARTLY REFUTE.** Per-panel n=4-6 is weak. But the gate pools all 71 valid-era control row-packages, about 1.2 wrong blockers each, paired on identical candidates. Recall is a paired comparison over the 38 real catches. What remains is unbudgeted: re-running the E2 judge to match grader-blocking rows to ground truth, and whether v1 anchors are usable (B's R1 already says unverified).
- **A's escalation refutation of B4.** A says a revised wrong blocker "usually clears" (`ledger.py:254-257`). Clearing happens only if the row is not re-found. A re-find sets `regressed` (`ledger.py:235`). No re-find rate has been measured, so A's refutation is not established either.

### Updated assessment of Variant A

A's concessions are accurate, and A's Round 2 is mostly an honest correction of its Round 1. A is a safe interim, not "B minus the grader". A still lacks:
- a named resolver for gated findings;
- the D2 fix, which is three lines but unmade;
- a degrade rule scoped to round 1 and recomputed in `defer()`.

A's precision claim is a bare prediction. So is B's. A's strongest remaining point is X-006: B's grader default is fail-open on meaning. I have conceded it.

### New evidence

- `defer()` bypasses B's PENDING (G2). A found `defer()` for the degraded rule. Neither variant saw it for PENDING.
- `ledger_cmd.py:13` indexes `EXIT_BY_DECISION[v["decision"]]`, so a `PENDING` decision raises KeyError until the dict gains it.
- My narrowing of C-006: a revision that touches the span flips the row to `regressed` on any re-find (`ledger.py:235`). B already re-grades changed text. So the frozen decision only matters for rows whose text did not change (reviser rejected, `named_not_touched`, never revised) and are re-reported non-blocking. The gain is real but narrower than B's R1 implied.
- Stoprule already demotes failed evidence before grading (G5).
- Full-table control flatness and the n=1 defect-rich result (G4).

### Facts verified this round

- **G1 VERIFIED.**
  - `ledger.py:15` imports v1 `findings`. `ledger.py:165` calls `fnd.cluster`, and `ledger.py:187` is `any(...)` over v1 groups.
  - `merge_cmd.py:10,109` goes ledger, then `merge_round`, so the v1 path.
  - `cluster_cmd.py:24-25,136` uses `cluster.py` and `findings_v2`. `verify_cmd.py:22-23` imports `cluster_cmd` and `findings_v2`.
  - `cluster.py:64-65` imports only `refs_norm` and `_check_citation`. `blocking_any` is at `cluster.py:375`, a second copy of the rule.
  - A grep of `findings.py` for `channel|citations|deviation_class|outcome` matches only imports.
  - Consequence: `review grade` needs two input adapters, ledger rows (v1) and `clusters_kept.json` (v2). B's candidate rule and `verify-citations` exist today only on the v2 path. B must edit both blocking copies, and the parity test must span both.
- **G2 VERIFIED.** `ledger.py:356-360` sets PASS when the brief empties, with no reviewer-count check.
  - For B, undecided rows have `blocking: None`, so they are not in `_brief_ids` (`ledger.py:99-104`). A PENDING round can have an empty brief, so any `defer` yields PASS.
  - Test `test_review_ledger.py:396-403` pins defer to PASS.
  - Fix: `defer` recomputes PENDING, and the degraded flag, from rows.
- **G3 VERIFIED.** `ledger.py:254-257` clears `resolved_check` to `resolved` when the row is absent from the round, and never reads `block_ok`. `test_review_ledger.py:376-385` pins `resolved` with one invalid reviewer. B depends on it equally, because clearing is absence-based whatever the decision source. It does not bite on the default one-reviewer re-review, since `ledger.py:150-157` refuses a round with no valid block.
- **G4 VERIFIED for A's arithmetic, FALSIFIED as a basis for any size claim.**
  - A's rows are correct: 315, 317 and 336 average 1.33; the five 3-panels average 1.21; n=4 is 1.50; n=5 is 1.75 and 0.25 (mean 1.00).
  - The sample was selective. The full-table figures are in the response to criticism 2.
  - Consequence: control data supports no panel-size claim in either direction. The cap is only a cost cap, and P1 is only a model.
- **G5 VERIFIED, with one gap.**
  - `finding-grader.md:5` pins `model: sonnet`, `:17` says "Otherwise it is not blocking", and `:19` says to grade unverified evidence as true.
  - In stoprule, `check_evidence` returns `(False, None)` for `live` evidence (`stoprule.py:264-265`). A failed path/line re-read is an issue (`:283-284`). Any seal issue forces a repair pass, and after the second seal the claim is `minor-form` (`SKILL.md:22`; `stoprule.py:541-553,590`). So only `live` evidence reaches the grader as `unverified`.
  - B's text (Design line 85) ported the batch logic but not this seal rule, so B grades quote-not-found items. That is a B defect.
  - `SKILL.md:24` dispatches with `subagent_type: finding-grader` only. `--grader-model` defaults to the label `"sonnet"` (`stoprule.py:2002`). The Agent tool's `model` parameter (enum sonnet, opus, haiku, fable) overrides the frontmatter, so independence from a sonnet reviewer is achievable among Anthropic aliases.
  - Non-Anthropic classes are UNVERIFIED. `merged-requirements.md:124` also lists whether the Agent tool honours `model:` in a worker as UNVERIFIED.
- **G6 UNVERIFIED (negative).** I found no scoring of the grader, or any blind per-claim grader, against ground truth. A grep of `phase5/` for canary, accuracy and ground-truth terms, and of `FINAL-REPORT.md` for grader terms, found none. `FINAL-REPORT.md:217` says no winning fix or valid repeated effect is established. `merged-requirements.md:351` lists "the grader is wrong in a patterned way", that canaries test only easy cases, and that no demotion is audited on a FAIL path. The search was not exhaustive. I did not re-read `FINAL-REPORT.md:106,162`, which B cited. Consequence: neither variant has measured precision, and the replay is the only planned measurement.

### Updated stances

| Point | Stance | Conf | Recommended merged-proposal position | Accept A's R2 position? |
|---|---|---|---|---|
| S-003 | EQUAL | 65 | Source-column evidence tables plus a counter-reading column; tag unread facts `[VIA]`. | yes |
| C-001 | HYBRID | 70 | The veto is live; the grader runs in shadow, then goes live per lens after the paired replay, starting with singletons. | yes |
| C-003 | HYBRID | 70 | Promotion is counted in shadow only and cannot raise a FAIL until measured precision exists. | yes |
| C-004 | HYBRID | 65 | Record `singleton_blockers` from per-cluster `reviewers[]`; singletons are the first population graded. | yes |
| C-005 | OPEN | 75 | Drop the cap as a precision lever and keep it as a cost cap; the replay reports wrong blockers by n. | yes |
| C-007 | HYBRID | 70 | A cluster with an unresolved citation is never graded blocking (stoprule's seal rule). A named resolver re-reads it. Absence findings are routed to the quoted requirement. `unverified` is never sole support. | yes |
| C-010 | HYBRID | 68 | Keep words and exits 0/10/11, add `degraded` as a field and a report line, and add exit 12 plus an `EXIT_BY_DECISION` entry for PENDING under `--decide grader`. | yes |
| C-012 | OPEN | 72 | Fix D1, D5 and D6 first; run veto and grader on the same candidates, scored on `blocking_in_implement`. | yes |
| X-002 | OPEN | 70 | V7 must list D1; attribution stays unmeasured. | yes |
| X-003 | HYBRID | 68 | The 27 are real defects over-graded; the gate is scored against implement-blocking. | yes |
| X-004 | A | 75 | Delete "E2 measured that direction" and the cap argument; control is flat, and the n=1 defect-rich rows are worst. | yes |
| X-005 | HYBRID | 70 | Certification is set at round 1 (two or more valid blocks) and inherited; `defer()` recomputes it and PENDING. | yes |
| X-006 | HYBRID | 80 | The grader may demote only with a named failed criterion; on doubt it keeps the reviewer's flag or goes to PENDING. | yes |

**Previously agreed points whose stance I change:** none. Confidence changes only:
- C-006 stays B but falls to about 60, narrowed to unchanged-text re-finds.
- X-007 stays B at 70.
- C-013 stays B; its power rests on pooling.
- C-014 stays HYBRID, with F2's accounting and the defer and exit-code tests added.

### Remaining disagreement

**What A still gets wrong:**
- "A is the right interim" understates its prerequisites: D1, D2 and the gate's resolver are unbuilt, so "runs today" means the unhardened veto.
- A's refutation of the escalation argument rests on an unmeasured re-find rate.
- A treats the replay as underpowered per panel and ignores the pooled paired design.

**What I got wrong:**
- P1's "E2 measured that direction" is unsupported.
- K1 described v2 fields as if the document loop had them.
- I ported the grader batch without stoprule's seal rule.
- I overstated what the frozen decision buys (C-006).
- I treated the replay as feasible without costing the judge re-run.
- "Fail-closed by construction" was wrong.

Files read this round include `src/superclaude/cli/review/{ledger.py,merge_cmd.py,cluster_cmd.py,ledger_cmd.py,findings.py}`, `tests/review/test_review_ledger.py`, `/home/coder/.claude/agents/finding-grader.md`, and the stoprule SKILL, script and rubric. The control-package arithmetic used `git show 4a22d74213f93837d00c2c314075dd967b9a98e3:.dev/eval-workspaces/tasklist-review-panel/20261111-a1/COMBO-REPORT.md`.

### Round 2 per-point tracking (orchestrator)

Same agreement rule as Round 1. "Determinate" means the agreed stance names a superior approach, an equivalence or a QUALIFY condition; "agreed-open" means both advocates say the point cannot be decided on present evidence.

| Point | Level | Advocate A (R2) | Advocate B (R2) | Agreed | Outcome |
|-------|-------|-----------------|-----------------|--------|---------|
| S-001 | L1 | EQUAL | EQUAL | yes | EQUAL |
| S-002 | L1 | EQUAL | EQUAL | yes | EQUAL |
| S-003 | L2 | EQUAL (was B) | EQUAL (was EQUAL) | yes (new) | EQUAL: B's source-column tables plus a counter-reading column; tag unread facts [VIA] |
| S-004 | L1 | B | B | yes | B (risk table with Residual column) |
| S-005 | L2 | B | B | yes | B (staged rollout) |
| S-006 | L2 | HYBRID | HYBRID | yes | HYBRID (tests of both, with the F2 accounting) |
| S-007 | L1 | EQUAL | EQUAL | yes | EQUAL |
| S-008 | L1 | EQUAL | EQUAL | yes | EQUAL |
| C-001 | L2 | HYBRID | HYBRID (was B) | yes (new) | HYBRID: veto live now, grader shadow, then live per lens after the paired replay |
| C-002 | L3 | HYBRID | HYBRID | yes | HYBRID: A's degrade rule on top of B's PENDING, certification set at round 1 and inherited |
| C-003 | L3 | HYBRID (was A) | HYBRID | yes (new) | HYBRID: `promoted` counted in shadow only; cannot raise a FAIL until measured |
| C-004 | L2 | HYBRID (was EQUAL) | HYBRID (was B) | yes (new) | HYBRID: `singleton_blockers` from `reviewers[]`; singletons are the first population graded |
| C-005 | L2 | OPEN (was HYBRID) | OPEN | yes (agreed-open) | OPEN: cap kept as a cost cap only; replay reports wrong blockers by n |
| C-006 | L3 | B | B | yes | B, narrowed to rows whose text did not change |
| C-007 | L3 | HYBRID (was B) | HYBRID (was A) | yes (new) | HYBRID: unresolved citation never blocking; named resolver; absence findings routed to quoted requirement; `unverified` never sole support |
| C-008 | L2 | HYBRID | HYBRID | yes | HYBRID |
| C-009 | L3 | HYBRID | HYBRID | yes | HYBRID |
| C-010 | L2 | HYBRID (was A) | HYBRID (was HYBRID) | yes (new) | HYBRID: exits 0/10/11 kept; `degraded` field and report line; exit 12 plus `EXIT_BY_DECISION` entry for PENDING |
| C-011 | L2 | EQUAL | EQUAL | yes | EQUAL |
| C-012 | L2 | OPEN (was HYBRID) | OPEN | yes (agreed-open) | OPEN: fix D1, D5, D6 first; same candidates; score on `blocking_in_implement` |
| C-013 | L2 | B | B | yes | B (paired, pre-registered, pooled replay) |
| C-014 | L2 | HYBRID | HYBRID | yes | HYBRID |
| C-015 | L2 | A | A | yes | A (S versus L), with B's v1-adapter cost added |
| X-001 | L3 | B | B | yes | B's side |
| X-002 | L2 | OPEN (was HYBRID) | OPEN | yes (agreed-open) | OPEN: attribution unmeasured; D1 pushes wrong blockers down |
| X-003 | L2 | HYBRID (was A) | HYBRID | yes (new) | HYBRID |
| X-004 | L2 | A (was HYBRID) | A | yes (new) | A's side: no size effect on control; drop P1's "measured that direction" and A's cap-as-precision claim |
| X-005 | L3 | HYBRID (was OPEN) | HYBRID | yes (new) | HYBRID: certification is a loop property set at round 1; `defer()` recomputes |
| X-006 | L3 | HYBRID (was A) | HYBRID | yes (new) | HYBRID: grader may demote only with a named failed criterion; on doubt keep reviewer's flag or PENDING |
| X-007 | L2 | B | B | yes | B's side |
| A-001 | L2 | QUALIFY | QUALIFY | yes | QUALIFY |
| A-003 | L3 | QUALIFY | QUALIFY | yes | QUALIFY |
| A-007 | L3 | QUALIFY | QUALIFY | yes | QUALIFY |

### Convergence assessment (before the invariant probe)
- Points with identical advocate stances: 33 of 33.
- Points with a determinate agreed outcome (not agreed-open): 30 of 33. Agreed-open points: C-005, C-012, X-002.
- Convergence on the superior approach, counting agreed-open points as NOT converged: 30 / 33 = 90.9% (threshold 80%).
- Taxonomy coverage gate: L1 5 of 5 covered, L2 18 of 18, L3 10 of 10, so the gate is satisfied.
- Trajectory: Round 1 60.6%, Round 2 90.9% (determinate) or 100% (identical stances). The 13 disputed points moved because both advocates verified source facts and conceded errors (see "Facts verified"), not because of a score threshold.
- Caution recorded by the orchestrator: both advocates converged on the same merged shape (veto live, grader in shadow behind a paired replay) and both conceded most of their own variant's numeric claims. Fast agreement is exactly where the protocol's Round 2.5 probe is aimed, so the invariant probe runs against the emerging consensus, not against either variant. The invariant-probe gate (HIGH and UNADDRESSED) can still block convergence even though the score is above the threshold.

## Round 2.5: Invariant Probe (summary; full findings in `invariant-probe.md`)

A single independent fault-finder agent (general-purpose, not an advocate) probed the emerging consensus M1-M12 across the six categories, including the always-on `sufficiency_challenge` category. It returned 25 findings: 2 ADDRESSED (both LOW) and 23 UNADDRESSED (11 HIGH, 10 MEDIUM, 2 LOW). The orchestrator spot-checked the code-fact claims behind the findings it could check cheaply and found them accurate; one line reference (`research/05:311`, INV-019) was not borne out and is flagged in the probe file.

HIGH and UNADDRESSED (the gate-blocking set): INV-001 (frozen decisions do not exist under the live veto, so one non-blocking re-report still clears a row until the flip), INV-004 (a PASS decided by a one-reviewer re-review is labelled certified by inheritance), INV-005 (an unresolved-anchor row leaves the brief, so the round can PASS before any resolver runs), INV-011 (one representative claim per cluster is graded and then frozen for every member), INV-014 (the D1 fix and the M3 locate gate can cancel each other, and a lone reviewer's rejected blocking finding is lost while two other valid blocks certify), INV-019 (the replay pass criterion can be met by a grader that demotes everything), INV-020 (the E2 replay never runs the rounds-2-and-3 code where C-006 lives), INV-021 (B2 is ungradable on v1 claims without an `outcome`), INV-023 (shadow counts measure disagreement, not who is right, and production has no ground truth), INV-024 (the degrade flag is enforced by prose only; the exit code stays 0), INV-025 (the evidence gate suppresses the population that fails it, and the v1 path has no resolver).

Invariant probe gate result: `count(HIGH + UNADDRESSED) = 11 > 0`. CONVERGENCE BLOCKED regardless of the diff-point score. MEDIUM items (10) are logged as warnings. At depth standard there is no Round 3, so no further debate round was run on these; they are carried into the return contract (`unaddressed_invariants`) and into the merged proposal as open items.

## Scoring Matrix

Winner and confidence per diff point. Rule used: the winner is the outcome both advocates stated in Round 2 (the advocates' stance tables above); confidence is the mean of the two advocates' last stated confidences, rounded; no extra boost is applied because those numbers already include each side's concessions. "B's side" or "A's side" on an X-point means that side's claim was found correct. HYBRID names the merged position in the Round 2 tracking table. OPEN means both advocates agreed it cannot be decided on present evidence. QUALIFY is the agreed response to a shared assumption.

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|------------|-------|--------|------------|-----------------|
| S-001 | L1 | EQUAL | 93% | Same seven H2 sections in the same order |
| S-002 | L1 | EQUAL | 73% | Heading depth is presentation only |
| S-003 | L2 | EQUAL | 63% | Source-column tables plus a counter-reading column; tag unread facts [VIA] |
| S-004 | L1 | Variant B | 60% | Risk table with a Residual column is easier to audit |
| S-005 | L2 | Variant B | 78% | B has four staged rollout steps; A has one benchmark gate |
| S-006 | L2 | HYBRID | 63% | B's 16 test groups plus A's parity and monotonicity tests, with the F2 accounting |
| S-007 | L1 | EQUAL | 75% | Both tag provenance; A's tags slightly more exact, B's more candid |
| S-008 | L1 | EQUAL | 70% | Both state the weakest point where a reader sees it |
| C-001 | L2 | HYBRID | 68% | Veto live now; grader in shadow, live per lens after the paired replay |
| C-002 | L3 | HYBRID | 73% | A's degrade rule over B's PENDING; certification set at round 1 (see INV-004) |
| C-003 | L3 | HYBRID | 68% | `promoted` counted in shadow only; cannot raise a FAIL until measured |
| C-004 | L2 | HYBRID | 64% | `singleton_blockers` from `reviewers[]`; singletons are the first population graded |
| C-005 | L2 | OPEN | 73% | Cap kept as a cost cap only; control wrong blockers are flat by panel size |
| C-006 | L3 | Variant B | 63% | Frozen decision closes the un-block path, but only for rows whose text did not change, and only after the flip (INV-001) |
| C-007 | L3 | HYBRID | 66% | Unresolved citation never blocking; named resolver; absence findings routed to quoted requirement; `unverified` never sole support |
| C-008 | L2 | HYBRID | 70% | Code predicate for reflect-post; frozen rubric for spec and tasklist |
| C-009 | L3 | HYBRID | 68% | Reviewer-level abstain and grader-level canaries are different layers; both needed |
| C-010 | L2 | HYBRID | 65% | Exits 0/10/11 kept; `degraded` as field and report line; exit 12 and `EXIT_BY_DECISION` entry for PENDING only |
| C-011 | L2 | EQUAL | 70% | Both keep contract 1.8.0 and nested `telemetry:` |
| C-012 | L2 | OPEN | 71% | Fix D1, D5, D6 first; same candidates; score on `blocking_in_implement`; attribution unmeasured |
| C-013 | L2 | Variant B | 71% | Paired, pre-registered, pooled replay with disjoint canary and benchmark sets (power limits in INV-019, INV-022) |
| C-014 | L2 | HYBRID | 65% | Tests of both, plus `defer`, exit-code and exact-dict `verdict()` tests |
| C-015 | L2 | Variant A | 80% | Effort S against L; B's v1 adapter (50-100 lines, estimate) is added to B's cost |
| X-001 | L3 | Variant B's side | 80% | A's "no decider can add recall" is false for B's promotion path |
| X-002 | L2 | OPEN | 69% | V7 omits D1; D1 pushes counted wrong blockers down; attribution unmeasured |
| X-003 | L2 | HYBRID | 67% | The 27 are real defects over-graded; the gate is scored against implement-blocking |
| X-004 | L2 | Variant A's side | 70% | No size effect on control; B's "E2 measured that direction" and A's cap-as-precision are both unsupported |
| X-005 | L3 | HYBRID | 69% | Certification is a loop property set at round 1; `defer()` recomputes it |
| X-006 | L3 | HYBRID | 78% | Grader may demote only with a named failed criterion; on doubt keep the reviewer's flag or PENDING |
| X-007 | L2 | Variant B's side | 70% | A's "only option that leaves every pin alone" is wrong; B's `--decide flag` default is zero-touch |
| A-001 | L2 | QUALIFY | 60% | Holds for the spec and tasklist lens only |
| A-003 | L3 | QUALIFY | 58% | Holds only if absence findings anchor to existing text and a failed locate routes to re-read (but see INV-006, INV-025) |
| A-007 | L3 | QUALIFY | 60% | Holds only if `same_defect` is tightened and a cited-text-changed guard exists (but see INV-011) |

Points won (debate performance for the Step 3 tiebreaker): Variant B 6 (S-004, S-005, C-006, C-013, X-001, X-007); Variant A 2 (C-015, X-004); HYBRID 13; EQUAL 6; OPEN 3; QUALIFY 3. Total 33.

## Convergence Assessment
- Points resolved (determinate agreed outcome): 30 of 33
- Alignment: 90.9% (30 / 33). Identical advocate stances: 33 of 33, of which 3 are agreed-open (C-005, C-012, X-002) and are counted as not converged
- Threshold: 80%
- Taxonomy coverage gate: satisfied (L1 5/5, L2 18/18, L3 10/10)
- Invariant probe gate: NOT satisfied, 11 HIGH-severity UNADDRESSED invariants (INV-001, 004, 005, 011, 014, 019, 020, 021, 023, 024, 025)
- Status: BLOCKED_BY_INVARIANTS (agreement is at or above the threshold and the taxonomy is covered, but HIGH-severity UNADDRESSED invariants exist). Because the gate is not met and depth standard has no Round 3, the debate ends without convergence; per the error-handling matrix the base is force-selected by score, non-convergence is documented, and the run is flagged for user review (status partial).
- Unresolved points: C-005, C-012, X-002 (agreed-open), plus the unaddressed invariants above
- Rounds completed: 2 debate rounds plus Round 2.5 (invariant probe)

