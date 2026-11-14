# Diff Analysis: Design Proposal Comparison (C05, who decides whether a finding blocks)

## Metadata
- Generated: 2026-11-14 (orchestrator: debate-orchestrator, Mode A)
- Variants compared: 2
  - Variant A = `adversarial/variant-1-original.md` (copy of `proposal-a.md`): Option A of C05, single-reviewer veto with hardened inputs.
  - Variant B = `adversarial/variant-2-original.md` (copy of `proposal-b.md`): Option D of C05, blind grader after clustering.
- Total differences found: 54 listed items (structural 8, content 15, contradictions 7, unique 17, shared assumptions 7)
- Categories: structural (8), content (15), contradictions (7), unique (17), shared assumptions (7; 3 UNSTATED promoted, 4 STATED not promoted)
- Debate points (denominator for convergence: S + C + X + promoted A): 33
- Focus areas for the debate: correctness, risk, test-coverage
- Source of requirements for scoring: the C05 block of `synthesis/synth-04-options-conflicts.md` (lines 292-383) plus the shared proposal template (Design, How it works, Evidence, Correctness argument, Risks and mitigations, Test coverage needed, Cost)

## Method and verification notes
- Both variants were read in full. Facts that both variants cite and that bear on a contradiction were re-read by the orchestrator at HEAD `792cf8c52` and at the E2 commit `4a22d74`:
  - `ledger.py:187` sets a new row's `blocking` from `any(m["blocking"])`; `ledger.py:213-218` lets the current round's members set a re-found row, OR-combined only across several clusters of the same round; `ledger.py:274` gives FAIL while the brief list is non-empty. Both variants describe this correctly.
  - `cluster.py:375` sets `blocking_any = any(blocking)`. Correct in both.
  - `contract.py:295-296` (single-reviewer-fallback trigger) and `contract.py:377-381` (regression and drift counts halt). Correct in both.
  - `test_review_ledger.py:296-298`, `:468-472` and `test_review_cli.py:328-348` assert a one-reviewer round-1 PASS. Variant A's claim about them is correct; Variant B does not list them (B keeps the `flag` default, so they stay green until the default flips).
  - `COMBO-REPORT.md:291` (E2 commit): "Over 71 rows the judge counts 65 'blocking' catches but only 38 are real blocking defects", with `gt_covered_blocking` defined as a defect matched by a blocking-flagged ledger row "which can include defects that are not blocking_in_implement". The same paragraph lists silent merge drops (49 blocking findings lost, four FAIL-to-PASS flips) and 83 chained rows. Both variants quote it faithfully; they differ on what it shows (X-002, X-003).
  - `COMBO-REPORT.md:298`: only one wrong-blocker result survived the audit statistics, the `2x luna + 2x ember` panel (2.75-3.25 more wrong blockers, permutation p 0.005-0.03).
  - `finding-grader.md` exists under `~/.claude/agents/` only; `src/superclaude/agents/` has no grader. Variant B states this correctly (G6) and budgets the promotion.
- IDs: S = structural, C = content, X = contradiction, U = unique contribution, A = shared assumption. Taxonomy levels (L1 surface, L2 structural, L3 state-mechanics) are assigned in the Debate Point Register at the end of this file by signal terms with priority L3 over L2 over L1.

## Structural Differences

Both variants share the same seven H2 sections in the same order (Design, How it works, Evidence, Correctness argument, Risks and mitigations, Test coverage needed, Cost). Variant A has 0 H3 headings (165 lines, 5351 words); Variant B has 19 H3 headings (307 lines, 7097 words).

| # | Area | Variant A | Variant B | Severity |
|---|------|-----------|-----------|----------|
| S-001 | H2 section ordering | Seven H2 sections in template order | The same seven H2 sections in the same order | Low |
| S-002 | Hierarchy depth | H1 + H2 only; sub-structure by bold lead-ins ("The decision.", "Asymmetric verdict...") | H1 + H2 + H3 (19): "What the core does", "The grader and its rubric", "What each consumer does", "Rollout", data-flow and contract-field subsections | Low |
| S-003 | Evidence organization | Numbered claims E-1 to E-17; each carries its own argument and counter-reading inline | Lettered tables A-E (V1-V9, G1-G8, K1-K6, F1-F5, X1-X10) with a Source column; argument is deferred to Correctness P1-P5 | Medium |
| S-004 | Risk register format | Eight numbered prose paragraphs, each with an italic *Mitigation* | Table R1-R11 with Risk, Mitigation and Residual columns | Low |
| S-005 | Staging or rollout section | None. One gate only: run the benchmark before the unified core is declared done (Risk 1, Test item 9) | Dedicated "Rollout" with four ordered steps (shadow, replay gate, flip `--decide` default, reflect authority only with a contract bump) | Medium |
| S-006 | Test-coverage organization | Nine numbered items: pins that stay green, tests changed by prerequisites, tests changed by the `degraded` marker, then new tests 4-8, then a benchmark | A table of existing tests that change (8 rows) followed by 16 numbered new-test groups, the last being the replay gate | Medium |
| S-007 | Evidence provenance tags | `[CODE]` (re-read at HEAD `792cf8c52`), `[E2@4a22d74]`, `[DOC]`, `[external]` | `[READ]`, `[VIA Rnn]`, `[E2 4a22d74]`, `[DOC-SOURCED]`; "[READ by grep]" used in places | Low |
| S-008 | Placement of the weakest point | Correctness step 8 ("what this argument does not establish") plus Risks item 1 | A dedicated "Weakest point" subsection under Correctness plus row R1 | Low |

## Content Differences

Both variants keep the any-reviewer set as the wide candidate list, keep the reflect debate and contract 1.8.0 (C11), and reject quorum and calibrator weighting on the same evidence. The differences below are where they part.

| # | Topic | Variant A approach | Variant B approach | Severity |
|---|-------|--------------------|--------------------|----------|
| C-001 | Decision authority and independence of the decider | Reviewers decide, each for its own findings, under a per-lens predicate; the core ORs the effective flags; no second agent (Design "The decision") | Reviewers propose, a separate blind grader decides per candidate cluster under a frozen rubric; the reviewer flag is kept as an input and baseline, not the decision (Design "Position") | High |
| C-002 | PASS rule and reviewer-count guard | FAIL on any open blocking row; a would-be PASS with fewer than two valid reviewer blocks is returned `degraded: true` and is not a certified PASS (Design "Asymmetric verdict") | PASS needs every candidate decided not-blocking; an undecided or unconfirmed candidate gives `PENDING` (exit 12), never PASS. No rule about how many reviewers were valid | High |
| C-003 | Candidate set and promotion | Only a finding whose effective flag is true can block; unflagged findings never block; advisory and grounding-gap never block | Candidates are `channel == defect` clusters with a blocking flag or severity MAJOR or CRITICAL; the grader can promote a cluster no reviewer flagged (`promoted` relation) | High |
| C-004 | Singleton handling | Add `singleton_blockers` (blocking clusters whose blocking members come from one reviewer) to cluster output and telemetry; nothing routes on it; a filter on singletons is the named fallback if the benchmark fails | Singletons are candidates and are graded like any other; `overruled` and `promoted` relations recorded per cluster | Medium |
| C-005 | Precision mechanism and panel-size policy | Harden the veto's inputs (evidence gate, per-lens predicate, partial reviewers abstain, complete-link clustering) and cap the panel at three finders | Make the chance of a wrong block per candidate a property of the grader (g), independent of reviewer count n; no cap argued for | High |
| C-006 | Re-found row and clearing across rounds | Unchanged: a re-found row takes the current round's flag (`ledger.py:213-218`), so one non-blocking re-report can clear it; made safe by D2 (invalid or partial reviewer never clears) and by C13 | Decision stored once with rubric and reply hashes; a re-found row keeps its decision unless its cited text changed; `grade apply` refuses a batch already graded | High |
| C-007 | Evidence gate behavior | Finding kept and flagged (`anchor_status: missing`); it cannot be effective-blocking until a deterministic re-read confirms it | `verify-citations` plus evidence-validator; a cluster that loses all citations is not graded and is recorded `dropped-unfounded`; surviving cites are re-read by the script and shown to the grader tagged `[verified]` or `[unverified]` | Medium |
| C-008 | Per-lens predicate or rubric | Predicate as data (C16): the reviewer's flag after the consequence-sentence check for spec; `deviation_class` and `channel` for reflect-post; the core records `blocking_effective` next to the reviewer's `blocking` | One frozen rubric file per lens with sha256 recorded in the ledger: `spec-v1` (stoprule B1-B3 verbatim), `reflect-pre-v1`, `reflect-post-v1` (mirrors the halting set; the grader proposes the class, code maps class to blocking); a change is a new version | High |
| C-009 | Fail-closed behavior and failure handling | A decider-less rule has no model failure mode; handles reviewer-level failure: rejected lines persisted, the reviewer is `partial` and abstains, a partial reviewer never clears a row | Canary claims; batch rejected on malformed line, missing or repeated `cid`, or wrong canary; one rerun, then `unconfirmed`; `unconfirmed` or undecided never yields PASS; but the rubric default for a case undecidable from the batch is "not blocking" (R5) | High |
| C-010 | Verdict vocabulary, CLI surface and contract fields | No new subcommand or required flag; adds `singleton_blockers`, `degraded`, `blocking_effective`, `anchor_status`, `rejected_lines[]`, `partial`; verdict word and exit code for degraded left to C19 | New `review grade prep|apply|status`, `review merge --decide flag|grader`, new `review-decisions/1` schema, `PENDING` and exit 12; existing 0/10/11 unchanged | Medium |
| C-011 | Reflect integration and contract constraint | Debate stays the merger; panel `blocking_any` stays shadow telemetry; contract 1.8.0, `merge_method` values and lint untouched; `singleton_blockers` in nested `telemetry:` | Grade stage runs after the debate and writes to `telemetry:`; authority passes only with a new `merge_method` value, a contract bump and a paired legacy-versus-panel run | Medium |
| C-012 | Reading of the E2 evidence | The 65-versus-38 gap is 27 real ground-truth defects graded blocking that did not block implement (severity over-grades); E2's rows were contaminated by D1 (49 dropped blocking findings), D5 (null spans) and D6 (83 chained rows); attribution was never measured | The 65-versus-38 and the 2.75-3.25 extra wrong blockers are the veto's measured failure; the merge code is faithful (0 violations in 264 merges) so the wrong blockers are a policy outcome, not a code bug | High |
| C-013 | Rollout, acceptance gate and measurement plan | Rerun the three E2 packages with the hardened core; pass condition is an owner-set tolerance on control-package wrong blockers (pre-fix baseline 0.83 for the default panel); fallback is a filter on singleton blockers | Pre-registered paired comparison on the same candidate sets: grader wrong blockers on control below the veto's, no loss of real-blocking recall, true-negative rate reported; canary and benchmark sets disjoint; bias battery; inconclusive result keeps D in shadow | High |
| C-014 | Test-coverage plan | Keeps `test_review_ledger.py:128-129`, `:279-300`, `:518-544` and `test_review_cluster.py:514-550` green; three tests gain a `degraded` assertion (`:296-298`, `:468-472`, `test_review_cli.py:328-348`); new: rule parity, monotonicity, effective flag, `singleton_blockers`, reflect isolation, benchmark | Default `--decide flag` keeps existing tests green until the default flips; 16 new groups: blindness, determinism, canaries and reruns, reply parser, candidate selection, verdict table, frozen decisions, relations, CLI round trip, reflect-post parity, reflect shadow, grader selection, data files, agent file, bias battery, replay gate | High |
| C-015 | Cost, new components and latency | Code S (the `degraded` marker, `singleton_blockers`, optionally one shared `any(...)` function); zero model calls beyond the finders; prerequisites C02, C12, C15, C16 are not charged to A | Effort L: `grade.py` (300-400 lines), `grade_cmd.py` (~150), `ledger.py` edits (40-60), three rubrics and three canary files, `finding-grader` promoted into `src/`; one grader call per batch of at most 6 candidates plus 2 canaries (25% overhead); one extra serial step per round; no grader token count measured | Medium |

## Contradictions

Each row cites text from both sides. Rows X-005 and X-006 are intra-variant (two passages of one variant disagree); the others are cross-variant. A contradiction is a falsifiable disagreement, not a difference of taste.

| # | Point of Conflict | Variant A position | Variant B position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Can another decider add a blocker the veto would not have raised? (subset invariant) | Correctness step 1: "A decider that filters that list can only remove blockers: for the same inputs, its FAIL set is a subset of the veto's FAIL set." E-4: "Any other decider named in C05 is a filter on the veto's candidate list ... so none can add recall." | Design step 1: a cluster is a candidate when `channel` is `defect` "and at least one member is flagged blocking or has severity MAJOR or CRITICAL"; contract fields: "`promoted` means no reviewer flagged it and the grader did"; R8: the grader "may promote findings the brief tells reviewers to list as follow-ups" | High |
| X-002 | Cause of the veto's wrong blockers in E2: policy or contaminated inputs | E-5: "The E2 measurement of the veto is contaminated by defects that are fixed elsewhere" (D1 dropped 49 blocking findings, D5 null spans, D6 83 chained rows); "Attribution ... was not measured by anyone. This is the central gap of this proposal" | V7: "The merge code is faithful to its rules (0 invariant violations over 264 merges), so the wrong blockers are a policy outcome, not a code bug". B's evidence tables do not list D1 (silent drops), which `COMBO-REPORT.md:291` lists as audit defect 2 | High |
| X-003 | What the 65-versus-38 gap means | E-3: the 27 extra catches "are severity over-grades. ... It is not an invented defect"; Correctness step 2: a wrong-blocker row on a defect-rich plan "sits on a plan with 4 to 10 known defects, so the plan's FAIL is the right verdict"; harm "lands on the control package" | Position: "The single-reviewer veto produced 65 judge-blocking catches against 38 real ones" is "the only measured failure"; P1 defines a spurious cluster as one where "no real blocking defect sits behind it" and treats wrong blockers as the cost to remove. `COMBO-REPORT.md:291` supports A on the definition; the wrong-blocker counts (rows with no ground-truth match) are a separate measure that neither variant maps back to the 27 | Medium |
| X-004 | Is the wrong-blocker effect a panel-size effect? | E-6 and E-7: "The only wrong-blocker result that survived audit is the four-reviewer panel built from two doubled pairs"; the two-reviewer `ember + luna` panel sits at 2.00, so "the effect is not only a panel-size effect"; replicated panels are not distinguishable (p 0.54-1.0) | P1: with n reviewers each over-flagging with probability q "the chance it blocks is 1 - (1 - q)^n, which rises with n. E2 measured that direction"; under D the chance "is the grader's false-block rate g ... independent of n" (B itself says reviewer flags are not independent, X7) | Medium |
| X-005 | Intra-A: degraded PASS versus a usable one-reviewer fallback | Design: "Degrading, not refusing, keeps spec-panel's one-reviewer fallback usable"; also "a would-be PASS with fewer than two valid blocks is returned with `degraded: true` and is not a certified PASS"; Risk 7: such a round "can no longer return a certified PASS" | (not applicable; B has no reviewer-count rule for ledger consumers) | Medium |
| X-006 | Intra-B: fail-closed by construction versus a not-blocking default | P4: "Fail-closed and auditable by construction ... PASS requires every candidate decided" | R5: "A case that cannot be decided from the batch is graded not blocking by the rubric's default (`finding-grader.md:17`)"; residual: "This default can drop a real blocker" | High |
| X-007 | Is A the only option that leaves existing pins and the contract alone? | Correctness step 7: "It is the only option that leaves every pin and contract alone ... the existing veto pins stay green"; Test item 3: three one-reviewer PASS tests (`test_review_ledger.py:296-298`, `:468-472`, `test_review_cli.py:328-348`) "gain an assertion on `degraded: true`" | Test coverage: "The `--decide flag` default keeps today's behaviour, so most existing tests stay green until the default flips"; Rollout steps 1-3 write to `telemetry:` only, leaving contract 1.8.0 and the lint untouched | Medium |

## Unique Contributions

Unique contributions feed the refactoring plan (Step 4). They are not debate points and do not enter the convergence denominator.

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | Asymmetric verdict: one valid reviewer may fail a plan, two valid reviewer blocks are needed to certify a PASS; a thinner PASS is marked `degraded` (agrees with `contract.py:295-296,317-326`) | High |
| U-002 | A | `singleton_blockers` count in cluster output and telemetry, read by no decision, plus a pre-agreed next step (a verification filter on singleton blockers only) | Medium |
| U-003 | A | States plainly that the veto is only defensible together with four input fixes decided in other conflicts (C02 evidence gate, C16 predicate, C15 abstain, C12 complete-link) and that they act on what enters the veto | High |
| U-004 | A | Error-cost asymmetry: a false FAIL becomes REVISE or ESCALATE (`ledger.py:93-96`), two of three tasklist review points are advisory, and the one blocking tasklist gate cannot currently fail on drift or regression | High |
| U-005 | A | Cap the panel at three finders (E-7), citing the only wrong-blocker result that survived audit | Medium |
| U-006 | A | Rule-parity property test (ledger row, cluster `blocking_any`, effective flags agree) and a monotonicity test (adding a valid reviewer never turns FAIL into PASS; an invalid or partial one never clears a row) | Medium |
| U-007 | A | Reads the 65-versus-38 gap against its definition (`COMBO-REPORT.md:291`) and notes the E2 judge saw the panel name | Medium |
| U-008 | A | "Cost of being wrong": the follow-up filter reuses the evidence gate, effective flag, abstention rule and `singleton_blockers` that A adds, so nothing is thrown away | Medium |
| U-009 | B | Split of candidate from decision with a deterministic candidate rule (defect channel; flagged or MAJOR/CRITICAL; advisory and grounding-gap excluded; MINOR-only excluded because the parser forbids blocking MINOR) | High |
| U-010 | B | Blindness enforced by construction (the renderer never receives reviewer ids, severity, `blocking`, `support`, combo-style paths) and pinned by a test, learning from the E2 judge's panel-name leak | High |
| U-011 | B | Canary claims, whole-batch rejection, one rerun, then `unconfirmed`; `unconfirmed` and undecided give `PENDING` (exit 12) and never PASS | High |
| U-012 | B | Frozen rubric per lens as data with its sha256 recorded in the ledger; later rounds refuse a different hash; option order permuted per batch | Medium |
| U-013 | B | `reflect-post-v1` mirrors the `contract.py:377-381` halting set with a parity test; the grader never overrides evidence-sourced regressions | Medium |
| U-014 | B | `agreed` / `overruled` / `promoted` relation counts: every run yields a paired veto-versus-decider record, so the choice can be checked after rollout | High |
| U-015 | B | Staged rollout with `--decide flag` as the default until a pre-registered replay gate passes; inconclusive result keeps D in shadow | High |
| U-016 | B | Grader independence recorded per run (`grader_diversity: degraded` when no disjoint class exists), served-model recorded against drift | Medium |
| U-017 | B | Failure lessons from the one live stoprule trial (transport invalidation), reply-file hashing, bias battery (swap order, pad claims, rename paths) | Medium |

## Shared Assumptions

Agreement points scanned: (1) both keep the any-reviewer set as the wide candidate list; (2) both cluster before deciding; (3) both gate blocking on a deterministic evidence re-read; (4) both reject quorum and calibrator weighting on the same evidence (X5, E-9); (5) both keep the reflect debate and contract 1.8.0; (6) both treat E2 as the only ground-truth evidence and call it thin; (7) both keep a re-round ledger with row matching. For each, the preconditions that must hold are listed. Only UNSTATED ones are promoted to debate points (A-NNN).

| # | Agreement source | Assumption (precondition) | Classification | Promoted |
|---|------------------|---------------------------|----------------|----------|
| A-001 | (6) E2 as the only evidence | The E2 result (one lens: tasklist and spec review, three packages, 16 defects, n of 4-6) transfers to the other lenses the core will serve (reflect-pre, reflect-post, future PR review and rf-qa replacement). Neither variant measured any of those lenses | UNSTATED | Yes |
| A-002 | (2) cluster before deciding | A cluster is a coherent unit of decision: complete-link clustering (C12) removes the chained rows (83 in E2) before the decider acts | STATED (A item 4 and Risk 8; B relies on "changes nothing before it" and reads one `representative` claim per cluster) | No |
| A-003 | (3) evidence re-read before blocking | Findings of absence (category `missing-requirement`, "the plan has no X") can carry a quote or anchor that a re-read will confirm, so the evidence gate does not suppress them or send them to `dropped-unfounded` | UNSTATED | Yes |
| A-004 | (1) any-reviewer candidate list | Candidate recall (what reviewers find at all) is decided elsewhere (C14) and is adequate, so the decider can be judged on precision | STATED (A Correctness step 1; B P2) | No |
| A-005 | (6) E2 as evidence | E2's figures (one gateway, 2026-11-11 to 11-13) transfer to the models and served versions in use when the core ships | STATED (A Risk 6; B R3 and served-model recording) | No |
| A-006 | (4) rejecting filters that drop singletons | A false FAIL is the cheaper error (REVISE below the review cap, ESCALATE at it) and a false PASS ships | STATED in A (E-14); implicit in B, and in tension with B's not-blocking default (X-006) | No |
| A-007 | (7) ledger row matching | A finding keeps a stable identity across rounds (the `fp` fingerprint matches the same finding after the reviser edits the document, and does not merge two different findings), so a re-found row inherits the right flag (A) or the right frozen decision (B) | UNSTATED | Yes |

### Promoted shared assumptions (debate points)

| # | Assumption | Impact | Status |
|---|-----------|--------|--------|
| A-001 | E2's one-lens result transfers to reflect-pre, reflect-post and future lenses | High: it carries the case for both variants outside the tasklist lens | Open: debate with ACCEPT, REJECT or QUALIFY |
| A-003 | Absence findings survive the evidence gate | High: a gate that suppresses absence findings removes the defect class "missing requirement" from blocking under either variant | Open |
| A-007 | Finding identity is stable across rounds | Medium: a wrong match gives a wrong flag (A) or a stale frozen decision (B) | Open |

## Debate Point Register

Every debate point has exactly one taxonomy level. Level assignment follows the signal terms of the protocol with priority L3 over L2 over L1 (L3: state, guard, boundary, invariant, validation rule, transition; L2: architecture, interface, component, module, dependency, organization; L1: naming, formatting, wording, style, presentation). Promoted A-NNN points tag L3 only when they carry state, guard or boundary terms. Focus tags: c = correctness, r = risk, t = test-coverage.

| Point | Level | Signal terms | Focus | Severity |
|-------|-------|--------------|-------|----------|
| S-001 | L1 | ordering, presentation | c | Low |
| S-002 | L1 | presentation, formatting | c | Low |
| S-003 | L2 | organization | c,t | Medium |
| S-004 | L1 | formatting | r | Low |
| S-005 | L2 | organization, dependency | r | Medium |
| S-006 | L2 | organization | t | Medium |
| S-007 | L1 | style, labeling | c | Low |
| S-008 | L1 | presentation | r | Low |
| C-001 | L2 | interface, component | c,r | High |
| C-002 | L3 | guard, boundary, transition | c,r,t | High |
| C-003 | L3 | boundary, validation rule | c,r | High |
| C-004 | L2 | component | r | Medium |
| C-005 | L2 | architecture, dependency | c,r | High |
| C-006 | L3 | state, transition | c,t | High |
| C-007 | L3 | validation rule, guard | c,t | Medium |
| C-008 | L2 | module, interface | c | High |
| C-009 | L3 | guard, state | c,r,t | High |
| C-010 | L2 | API design, interface | t | Medium |
| C-011 | L2 | interface, dependency | r | Medium |
| C-012 | L2 | dependency, organization | c,r | High |
| C-013 | L2 | component, dependency | r,t | High |
| C-014 | L2 | component, organization | t | High |
| C-015 | L2 | component, dependency | r | Medium |
| X-001 | L3 | invariant | c | High |
| X-002 | L2 | dependency | c,r | High |
| X-003 | L2 | dependency | c | Medium |
| X-004 | L2 | architecture | c | Medium |
| X-005 | L3 | guard, state | c,r | Medium |
| X-006 | L3 | guard, invariant | c,r | High |
| X-007 | L2 | interface, dependency | t | Medium |
| A-001 | L2 | dependency | c,r | High |
| A-003 | L3 | guard, boundary | c,t | High |
| A-007 | L3 | state, transition | c,t | Medium |

Level counts: L1 = 5, L2 = 18, L3 = 10. Every level has more than zero points, so the taxonomy coverage gate can be satisfied only if the debate actually addresses at least one point of each level.

## Summary
- Total structural differences: 8
- Total content differences: 15
- Total contradictions: 7
- Total unique contributions: 17 (A: 8, B: 9)
- Total shared assumptions surfaced: 7 (UNSTATED: 3, STATED: 4, CONTRADICTED: 0)
- Debate points (convergence denominator = S + C + X + promoted A): 8 + 15 + 7 + 3 = 33
- Highest-severity items (High): C-001, C-002, C-003, C-005, C-006, C-008, C-009, C-012, C-013, C-014, X-001, X-002, X-006, A-001, A-003
- Similarity check: the variants differ on the decision rule itself, so the difference is far above the 10% threshold; debate is not skipped.
- Overlap worth noting before the debate: both variants agree on the candidate list, on clustering before deciding, on the evidence re-read, on keeping the reflect debate and contract 1.8.0, and on rejecting quorum and calibrator weighting. The live disagreements are C-001 to C-003, C-005, C-006, C-009, C-012 and C-013, and the contradictions X-001, X-002, X-006.

