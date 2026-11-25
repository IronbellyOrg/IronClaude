# Step 3 Scoring, Pass 2 (reverse order: V4, V3, V2, V1)

Evaluator: adv-scorer pass 2 (independent of pass 1). Date: 2026-11-23.
Status: COMPLETE (all sections filled). Result: V4 quant 0.8500, qual 0.7000 (21/30); V3 quant 0.9609, qual 0.8333 (25/30); V2 quant 0.9442, qual 0.8000 (24/30); V1 quant 0.9312, qual 0.9000 (27/30). All four pass the Invariant and Edge Case floor.

Scope: quantitative layer (RC, IC, SR, DC, SC and quant_score), qualitative layer (30 criteria, CEV, six dimension subtotals, qual_score), Invariant and Edge Case floor check. No combined ranking and no base choice (the reconciler does that).

## 0. Method and counting rules

Read for this pass: `SKILL.md` Step 3 (lines 1595-1860), `refs/scoring-protocol.md`, the four variants (order 4, 3, 2, 1), `CONTEXT.md`, `diff-analysis.md` (all), `debate-transcript.md` lines 1-280 and 440-654. Not read: `scoring-pass-1.md` (by instruction) and `debate-transcript.md` lines 281-439 (round 2 rebuttals of advocates 1 to 3). The debate was used only to corroborate contradictions (A-017, X-003, X-008); no verdict below rests on a debate claim alone.

Source requirements (CONTEXT.md has no formal IDs, so this is section-level topic matching, as the protocol's edge case says). 23 items: Q1-Q9 (the nine numbered questions) and 14 items from "What the branching has to serve": B1 integration, Clay and the Orca prefix; B2 the owner's model (release line, story sub-branches, release lands on the default branch); B3 the ref-conflict fact; B4 worker flow (worktree per story, coordinator merges, conflicts stopped and reported); B5 two parallel stories with disjoint paths and serial merges; B6 `/sc:pr-submit` facts (CI only for master and integration, two reviewers, owner merges); B7 exact-name creation (`worker-start` has no `--branch`, use `orca worktree create --branch`); B8a never rewrite a published or branched-from branch; B8b never touch the upstream repository; B8c `.dev/` records committed on the release branch; B9a ledger on the release branch; B9b BMAD planning of release n+1 starts from master; B10 dashboard release numbers are not package versions (6.1.0); B11 scale (bursts of 15 to 60 AI pull requests). A requirement is "matched" when the variant states a rule, a mechanism or a disclosed alternative for it (a reasoned departure counts as addressed; fit is judged in the qualitative layer, not here).

Deterministic counts for IC, SR, DC and SC come from one read-only script (run once with `uv run python -I` from a private `/tmp` directory, removed afterwards). It splits body text (no headings, code fences or table separators) into units: one sentence, or one table row. Concrete unit = contains a digit, a backticked token or a named entity (Orca, GitHub, DORA, Augment, Codex, BMAD and similar). Vague unit = matches the protocol vague list (appropriate, as needed, properly, adequate, should consider, might, various, etc., best practice(s), industry standard). Claim unit (scorable claim) = concrete and not vague. Contradiction rule: only opposing claims or requirement-constraint conflicts that the variant's own text states with no resolution path. A disclosed trade-off that offers a path or an owner decision is not counted (V2 ledger mismatch, V3 Open decision A and planning-base change: not counted).

## 1. Quantitative scoring (counts shown)

### 1.1 SC (section coverage)
H2 headings counted per the protocol (H3 not counted).

| Variant | H2 count | H3 count | SC = H2 / max(9) |
|---|---|---|---|
| V4 | 3 ("In one paragraph", "The rules, in order of the nine questions", "What this proposal needs that the source does not give") | 9 (the nine questions) | 3/9 = 0.3333 |
| V3 | 9 | 0 | 9/9 = 1.0000 |
| V2 | 8 | 0 | 8/9 = 0.8889 |
| V1 | 8 | 0 | 8/9 = 0.8889 |

Note: V4's low SC is mostly a heading-level choice (S-006 in diff-analysis): its nine answers sit at H3. Scored as the protocol prescribes.

### 1.2 RC (requirement coverage)
Y = matched, N = not matched (23 items). Notes: B7 for V3: only "when `--branch` is given" appears, no `orca worktree create` command, so N. B9a for V2: matched by the disclosed ledger mismatch in Q7. B11 for V3: matched weakly (cites CONTEXT line 16 for AI-speed merge-in cost, no 15-to-60 figure). B9b for V1: only "Commit the planning `.dev/` records" appears, no statement about where BMAD planning starts, so N.

| Item | V4 | V3 | V2 | V1 |
|---|---|---|---|---|
| Q1 to Q9 (nine rows, each answered with a rule by every variant) | 9 Y | 9 Y | 9 Y | 9 Y |
| B1 integration, Clay, Orca prefix | Y | Y | Y | Y |
| B2 owner's model | Y | Y | Y | Y |
| B3 ref-conflict fact | Y | Y | Y | Y |
| B4 worker flow, conflicts stopped and reported | Y | Y | Y | Y |
| B5 two stories, disjoint paths, serial merges | Y | Y | Y | Y |
| B6 `/sc:pr-submit`, CI scope, reviewers, owner merges | Y | Y | Y | Y |
| B7 exact-name creation command | Y | N | Y | Y |
| B8a no rewrite of published branch | Y | Y | Y | Y |
| B8b never touch upstream (searched "upstream", "SuperClaude-Org": 0 hits in all four) | N | N | N | N |
| B8c `.dev/` records | Y | Y | Y | Y |
| B9a ledger | Y | Y | Y | Y |
| B9b BMAD planning base | N | Y | N | N |
| B10 dashboard numbers not package version | Y | N | N | N |
| B11 scale 15 to 60 | N | Y | Y | N |
| Matched / 23 | 20 | 20 | 20 | 19 |
| RC | 0.8696 | 0.8696 | 0.8696 | 0.8261 |

### 1.3 IC (internal consistency)
IC = 1 - contradictions / scorable claims.

| Variant | Scorable claims (script count) | Contradictions | IC |
|---|---|---|---|
| V4 | 46 | 2 | 1 - 2/46 = 0.9565 |
| V3 | 98 | 0 | 1.0000 |
| V2 | 92 | 0 | 1.0000 |
| V1 | 94 | 0 | 1.0000 |

V4 contradiction 1 (requirement-constraint conflict): Q8 "a dashboard release does not pass through it; `integration` is merged into `release/dash1.3` before the release pull request" and Q4 "Not through `integration`" versus Q3 "merge, never rebase, `master` and `integration` into `release/dash1.3`". Merging `integration` into the release line puts its commits into the release PR (corroborated by diff-analysis X-003 and A-017). V4 never notices this.
V4 contradiction 2 (opposing claims): Q4 "CI and the two reviewers run once, at that point" (release PR) versus Q2 "By pull request from the story branch into `release/dash1.3`, with the tests for that level and at least one review" and the closing section's `release/**` CI trigger for story PRs (diff-analysis X-008).
V1, V2, V3: scanned Q2 vs Q3 vs Q4 vs Q9, the flow steps and the cost and risk sections for opposing claims; none found. Disclosed trade-offs not counted: V2 Q7 "This is a real mismatch" (ledger, two paths offered), V3 Q2 Open decision A (owner-merge fallback offered), V3 Q8 planning base moves to `integration` (stated as a change).

### 1.4 SR (specificity ratio)
SR = concrete units / (concrete units + vague units).

| Variant | Units | Concrete units | Vague units | SR |
|---|---|---|---|---|
| V4 | 90 | 46 | 0 | 1.0000 |
| V3 | 140 | 98 | 0 | 1.0000 |
| V2 | 128 | 92 | 0 | 1.0000 |
| V1 | 136 | 94 | 0 | 1.0000 |

The protocol vague list matched zero units in all four variants, so SR is 1.0 for all and does not separate them. Diagnostic only (not scored): share of units that are concrete: V4 51%, V3 70%, V2 72%, V1 69%; "UNVERIFIED" marks: V4 1 (plus 7 "UNSPECIFIED"), V3 6, V2 8, V1 6.

### 1.5 DC (dependency completeness)
DC = resolved internal references / internal references. External references excluded (S-IDs, CONTEXT lines, `research-notes.md`, `gfxai-fit.md`, other proposal files).

| Variant | Internal refs | Resolved | DC | References |
|---|---|---|---|---|
| V4 | 3 | 3 | 1.0000 | Q8: "(question 3)", "(question 4)"; Q9: "question 4" |
| V3 | 6 | 6 | 1.0000 | "section 2", "Open decision A" (x2), "(Q9)", "(Q6)", "cadence rule (below)" (resolves to the Q5 "Train rule") |
| V2 | 3 | 3 | 1.0000 | "section 2", "(Q9)", "Q3 note" |
| V1 | 11 | 11 | 1.0000 | "section 4", "Q2", "(Q7)", "(Q8)", "section 2", "(Q9)", "(Q8)", "(Q8)", "(Q3)", "Q4", "Q5" |

Excluded cross-document references ("Proposal N" points at another variant file): V3 10, V1 1, V2 0, V4 0. Sensitivity if the reconciler decides to count them as unresolved: V3 DC = 6/16 = 0.3750 (quant 0.8671), V1 DC = 11/12 = 0.9167 (quant 0.9187); V2 and V4 unchanged. The scores in 1.6 follow the protocol (excluded).

### 1.6 quant_score table
quant_score = 0.30 RC + 0.25 IC + 0.15 SR + 0.15 DC + 0.15 SC.

| Variant | RC (x0.30) | IC (x0.25) | SR (x0.15) | DC (x0.15) | SC (x0.15) | quant_score |
|---|---|---|---|---|---|---|
| V4 | 0.8696 (0.2609) | 0.9565 (0.2391) | 1.0000 (0.1500) | 1.0000 (0.1500) | 0.3333 (0.0500) | 0.8500 |
| V3 | 0.8696 (0.2609) | 1.0000 (0.2500) | 1.0000 (0.1500) | 1.0000 (0.1500) | 1.0000 (0.1500) | 0.9609 |
| V2 | 0.8696 (0.2609) | 1.0000 (0.2500) | 1.0000 (0.1500) | 1.0000 (0.1500) | 0.8889 (0.1333) | 0.9442 |
| V1 | 0.8261 (0.2478) | 1.0000 (0.2500) | 1.0000 (0.1500) | 1.0000 (0.1500) | 0.8889 (0.1333) | 0.9312 |

## 2. Qualitative scoring (30 criteria, CEV)

Reading of each row: CLAIM = "[criterion] is met in this variant"; EVIDENCE = quote or section, or "none found, searched ...". No evidence means NOT MET; no partial credit. Rules applied the same way to all four variants: C1 needs RC = 1.0 (every listed requirement matched), so it is NOT MET for all four; K2 needs the design to run under the CONTEXT constraints as written (no constraint has to be changed); R1 needs at least three risks that each carry a likelihood and an impact; R2 needs a mitigation for each listed risk; L1 is a scan of the protocol vague list (0 matches in all four variants, see 1.4).

### 2.1 Variant 4 (GFxAI approach adapted)

| ID | Criterion | Evidence | Verdict |
|---|---|---|---|
| C1 | Covers all explicit requirements | RC = 20/23. Searched all nine answers: no upstream rule (B8b), no statement of where BMAD planning starts (B9b), no burst scale (B11). | NOT MET |
| C2 | Edge cases and failure scenarios | Q9 "revert its single squash commit on the release branch with a new commit (no history rewrite)"; Q2 "a conflict is stopped and reported to the coordinator, never resolved automatically". | MET |
| C3 | Dependencies and prerequisites | Closing section: "a CI trigger for pull requests into `release/**` ... a rule for who may merge into the release branch; the tag scheme". | MET |
| C4 | Success and completion criteria | Q4 "full test tiers, two approvals and sign-off, then a tag and deploy"; Q7 delete "once its squash commit is in the release branch and recorded in the ledger". | MET |
| C5 | Explicit out of scope | Marks line "UNSPECIFIED = the source has no answer and I add none"; Q1 "the source's rule on size is not kept". | MET |
| K1 | No factual errors or hallucinated claims | No verifiable error found; ref-folder rule matches CONTEXT line 8. GFxAI figures (PR #147, #129, #131) were not independently checked by me; they are sourced to `gfxai-approach.md`. | MET |
| K2 | Feasible with stated constraints | Q2 puts a PR per story into `release/dash1.3` with the coordinator running the merge, and the closing section needs `release/**` added to `test.yml`; CONTEXT line 11 says CI runs only for master and integration and the owner merges every PR. Needs two constraints changed. | NOT MET |
| K3 | Terminology consistent | "release branch", "work branches", "story", and the four marks are used the same way throughout; Q1 flags the feature-versus-story difference explicitly. | MET |
| K4 | No internal contradictions | Two found (section 1.3): Q8 "does not pass through" `integration` while `integration` is merged into the release line; Q4 "CI and the two reviewers run once" versus Q2 per-story PR tests and review. | NOT MET |
| K5 | Claims supported by evidence or rationale | "FROM PRACTICE: GFxAI's long-lived branch `feat/OntRAG` took `master` in by merge twice (pull requests #129 on 2026-03-21 and #131 on 2026-03-23)"; Q3 gives a reason for merge-not-rebase. | MET |
| S1 | Logical section ordering | One paragraph, then Q1 to Q9 in order, then needs; Q8 refers back to "(question 3)" only after question 3. | MET |
| S2 | Consistent hierarchy depth | 3 H2, nine H3 all under "The rules, in order of the nine questions"; no orphaned subsection. | MET |
| S3 | Separation of concerns | Summary, rules (one question per H3), needs list are separate sections. | MET |
| S4 | Navigation aids | "(question 3)", "(question 4)", "needs the merge-commit landing in question 4". | MET |
| S5 | Artifact-type conventions | No branch table, no flow diagram, no step list (diff-analysis S-003, S-004: flow "spread across the nine rule answers"). Searched the whole file. | NOT MET |
| L1 | Unambiguous language | Vague-list scan: 0 matches. | MET |
| L2 | Concrete rather than abstract | `dash1.3/story/01-widget-grid`, `hotfix/<id>-<slug>`, tag `dash-1.3`. | MET |
| L3 | Each section has one clear purpose | Each of Q1 to Q9 answers one question; the paragraph and the needs list are one-sentence summarisable. | MET |
| L4 | Terms defined on first use | The four marks are defined in the intro line, but "Tier 1 + Tier 2 + Tier 3", "UAT sign-off", "Interface-First design" (Q2, Q4) and "Tech-Lead emergency override" (Q9) are used with no definition. | NOT MET |
| L5 | Actionable next steps or decisions | Closing list of what the proposal needs; Q1 "UNVERIFIED whether `--branch` keeps the name exact". | MET |
| R1 | At least 3 risks with probability and impact | No risk section. Only "Size warning, FROM PRACTICE: ... #147 ... 1,384 files, +242,976 lines" (impact, no likelihood). | NOT MET |
| R2 | Mitigation for each risk | No risk list; the size warning is answered only by "keep stories short-lived" (Q5). | NOT MET |
| R3 | Failure modes and recovery | Q9: revert the release merge commit on `master`, fix on the release branch, new PR. | MET |
| R4 | External dependencies and their failure | Q1 Orca `--branch` UNVERIFIED; closing section `test.yml` trigger; Q7 "because 'delete branch on merge' is off" (GFxAI left 6 `backup/...` branches). | MET |
| R5 | Monitoring or validation mechanism | Q4 full test tiers and sign-off; Q6 beta freeze. | MET |
| E1 | Collection boundaries (empty, one, max) | No rule at a boundary; only the size warning and "zero padded". Searched Q1, Q4, Q5, Q6. | NOT MET |
| E2 | State interactions across components | Q3 and Q8 handle `master` and `integration` state wrongly: merging `integration` into the release line pulls its commits into the release PR (A-017), unnoticed. | NOT MET |
| E3 | Guard condition gaps | Closing "a rule for who may merge into the release branch"; Q2 notes the rebase-only rule "clashes with `/sc:pr-submit`, which never rewrites a published branch". | MET |
| E4 | Count divergence | Q1 "two-digit story number (zero padded so they sort)". | MET |
| E5 | Interaction effects | Q2 "the two parallel stories name disjoint paths in their specs; the coordinator merges one story at a time". | MET |

### 2.2 Variant 3 (release train)

| ID | Criterion | Evidence | Verdict |
|---|---|---|---|
| C1 | Covers all explicit requirements | RC = 20/23. Missing: exact-name creation command (B7, only "when `--branch` is given"), upstream rule (B8b), dashboard-number note (B10). | NOT MET |
| C2 | Edge cases and failure scenarios | Q9 "a revert pull request of that story's merge commit into the train (`git revert -m 1`), or a fix story"; Q2 conflicts handled by the story worker; Q3 `dash1.3-sync<N>` when merge-in conflicts. | MET |
| C3 | Dependencies and prerequisites | Section 5: one change to `.github/workflows/test.yml` "needs the owner's approval", a merge-authority decision, planning base moves to `integration`. | MET |
| C4 | Success and completion criteria | Section 1 "The train departs when its planned stories are in, or at a set time with whatever is in"; Q4 owner merges with a merge commit, then marker. | MET |
| C5 | Explicit out of scope | Q5 "unfinished work is 'not in the train', not 'in but hidden'" (no flags); Section 5 "the native GitHub stacked pull requests feature is not assumed available". | MET |
| K1 | No factual errors | No verifiable error; "CI is turned on by the pattern `train/*` in the `branches` filter of the `pull_request` trigger" is how GitHub filters on the base branch; ref rule matches CONTEXT line 8. | MET |
| K2 | Feasible with stated constraints | Q2 "works best if the owner allows the coordinator to merge story pull requests into a `train/*` branch only" and Section 5 `test.yml` edit; both conflict with CONTEXT line 11 as written. Needs two constraints changed. | NOT MET |
| K3 | Terminology consistent | "train", "story", "roll-up", "departure" used consistently in Sections 1 to 4. | MET |
| K4 | No internal contradictions | Checked Q2 vs Q3 vs Q4 vs Q6 and flow steps 1 to 6: merge-not-rebase and merge-commit rules repeat without conflict. Summary "can be stacked" is narrowed (not reversed) by Section 3 step 3. | MET |
| K5 | Claims supported | Q2 "(S6: small batches; S19: reviewers choke on big diffs)"; Q5 Chrome and DORA references. | MET |
| S1 | Logical section ordering | Summary, names, flow, nine questions, costs, favours, risks, open decisions, sources. | MET |
| S2 | Consistent hierarchy depth | 9 H2, no H3. | MET |
| S3 | Separation of concerns | Costs (5), favours (6), risks (7), decisions (8), sources (9) are separate. | MET |
| S4 | Navigation aids | "See section 2", "(Open decision A below)", "(Q9)", "(Q6)". | MET |
| S5 | Artifact-type conventions | Branch table, ASCII merge diagram, six numbered steps. | MET |
| L1 | Unambiguous language | Vague-list scan: 0 matches. | MET |
| L2 | Concrete rather than abstract | `/sc:pr-submit --monitor 3 --base train/dash1.3`, `train/dash1.3`, `dash1.3-s04-token-usage-panel`. | MET |
| L3 | Each section has one clear purpose | Each H2 has one purpose. | MET |
| L4 | Terms defined on first use | "train" defined in Section 1 ("one batch branch `train/dash1.3`, cut from `integration`"), "departs", "roll-up", "sync branch" explained in place. | MET |
| L5 | Actionable next steps or decisions | Section 8 Open decisions A, B, C with the effect of each answer. | MET |
| R1 | At least 3 risks with probability and impact | Section 7 lists 6 risks, none with a likelihood (e.g. "1. Merge authority: if the owner insists on clicking every story merge, the train stalls"). | NOT MET |
| R2 | Mitigation for each risk | Section 7 risks 2, 3, 4 and 6 have no mitigation text; only risk 5 ("Check by opening one test pull request first") and risk 1 (Open decision A). | NOT MET |
| R3 | Failure modes and recovery | Q9 layered: story out of the train, train out of `integration`, promotion out of `master`; "prefer a fix train". | MET |
| R4 | External dependencies and their failure | Risk 5 wrong CI filter leaves story PRs with no CI; risk 6 "Reviewer behaviour on pull requests whose base is a `train/*` branch ... is UNVERIFIED". | MET |
| R5 | Monitoring or validation mechanism | CI plus both reviewers on every story PR; risk 5 "opening one test pull request first". | MET |
| E1 | Collection boundaries | Q6 "A one-story release skips the train ... (no train branch for a batch of one)"; Q5 time box: "stories that are not merged ride the next train". | MET |
| E2 | State interactions across components | Q3 merge-in of `integration`; Q6 "`master` into `integration` sync pull request, then the train merges `integration` in"; Q8 planning base moves to `integration`. | MET |
| E3 | Guard condition gaps | Risk 5 "leaves story pull requests with no CI while everyone assumes they have it". | MET |
| E4 | Count divergence | Only `s<NN>` numbering and "sort by release then story number"; no off-by-one or range scenario. Searched Section 2, Q1. | NOT MET |
| E5 | Interaction effects | Q2 "a semantic collision shows as a red check on the next story's pull request, one story later at worst". | MET |

### 2.3 Variant 2 (trunk, dark landing)

| ID | Criterion | Evidence | Verdict |
|---|---|---|---|
| C1 | Covers all explicit requirements | RC = 20/23. Missing: upstream rule (B8b), BMAD planning base (B9b, not stated), dashboard-number note (B10). | NOT MET |
| C2 | Edge cases and failure scenarios | Q9 "revert pull request for that one squash commit, or switch its flag off"; Section 7 six risks. | MET |
| C3 | Dependencies and prerequisites | Step 1 "Planning (BMAD) splits each story into slices that can each merge alone"; Q2 shared files "in their own first slice". | MET |
| C4 | Success and completion criteria | Step 5 "When the switch-on slice has merged and the owner decides to ship: cut `release/dash1.3`"; Step 6 tag, delete. | MET |
| C5 | Explicit out of scope | Q3 merge queue "so this proposal does not depend on it"; Q2 "Dependent slices are not stacked". | MET |
| K1 | No factual errors | No verifiable error; UNVERIFIED tags on auto-delete, queue plan, sync owner (8 marks). Flat-name leaf claim is correct git behaviour. | MET |
| K2 | Feasible with stated constraints | Q7 "CONTEXT says `sprint-status.yaml` is tracked on the release branch being executed ... Here there is no release branch ... This is a real mismatch"; CONTEXT line 14 cannot be met without changing it. | NOT MET |
| K3 | Terminology consistent | "slice", "dark", "switch-on", "release cut" defined in Section 1 and used the same way. | MET |
| K4 | No internal contradictions | Checked Q2 vs Q3 vs Q4 vs Q6 and steps 1 to 6; "never merged back into `integration`" (Q3) agrees with the cherry-pick-only rule in step 5. | MET |
| K5 | Claims supported | Q5 "trunk-based branches last about two days (S1); DORA calls a batch over a week too big ... (S6)". | MET |
| S1 | Logical section ordering | Same eight-section order as V1. | MET |
| S2 | Consistent hierarchy depth | 8 H2, no H3. | MET |
| S3 | Separation of concerns | Costs (5), favours (6), risks (7), sources (8). | MET |
| S4 | Navigation aids | "See section 2", "(Q9)", "see Q3 note". | MET |
| S5 | Artifact-type conventions | Branch table, ASCII flow, six steps. | MET |
| L1 | Unambiguous language | Vague-list scan: 0 matches. | MET |
| L2 | Concrete rather than abstract | `orca worktree create --branch dash1.3-s04-p1-... --base-branch integration --agent claude`. | MET |
| L3 | Each section has one clear purpose | Each H2 has one purpose. | MET |
| L4 | Terms defined on first use | Section 1: lands "dark: the code is in `integration` but nothing reaches it until the last story ... wires it in or flips a flag"; "slice" defined in step 1. | MET |
| L5 | Actionable next steps or decisions | Q5 "How practical flags are ... is UNVERIFIED and is the first thing to test on one story." | MET |
| R1 | At least 3 risks with probability and impact | Only risk 1 has a likelihood ("most likely failure is a queue of ready slices waiting for the owner"); risks 2 to 6 have none. | NOT MET |
| R2 | Mitigation for each risk | Risks 1, 3 and 4 have no mitigation (Section 7); only partial on 2 and 6. | NOT MET |
| R3 | Failure modes and recovery | Q9 "flag off for dark features, or revert the promotion merge commit through a revert pull request, or cherry-pick the fix into `release/dash1.3` and promote again". | MET |
| R4 | External dependencies and their failure | Q3 merge queue "private repositories need an Enterprise Cloud plan (S4); the plan is UNVERIFIED"; Section 5 reviewer saturation (S19). | MET |
| R5 | Monitoring or validation mechanism | Q2 "CI on every slice runs against the real `integration`, so semantic collisions show as a red check". | MET |
| E1 | Collection boundaries | No statement for an empty, one-item or maximum set (only "Release size is bounded by the slices"). Searched Q2, Q4, Q6. | NOT MET |
| E2 | State interactions across components | Q3 "a `master` into `integration` sync pull request after every promotion or emergency fix"; Q7 ledger state has no branch. | MET |
| E3 | Guard condition gaps | Q2 "a pull request whose base is another slice's branch gets no CI". | MET |
| E4 | Count divergence | `s01` to `s99` sort only; no off-by-one or range scenario. Searched Section 2 and Q1. | NOT MET |
| E5 | Interaction effects | Q4 "the promotion carries Clay's merged work too. The dashboard release cannot be shipped without it". | MET |

### 2.4 Variant 1 (release line, local merges)

| ID | Criterion | Evidence | Verdict |
|---|---|---|---|
| C1 | Covers all explicit requirements | RC = 19/23. Missing: upstream rule (B8b), BMAD planning base (B9b), dashboard-number note (B10), burst scale (B11). | NOT MET |
| C2 | Edge cases and failure scenarios | Q9 "`git revert -m 1 <story merge commit>` ... a new commit; published history is never rewritten"; Q2 conflicts "the coordinator stops and reports". | MET |
| C3 | Dependencies and prerequisites | Section 2 "Creating a story branch with an exact name (worker-start has no `--branch`): `orca worktree create --branch ...`"; Q2 foundation story for shared files. | MET |
| C4 | Success and completion criteria | Step 3 "Story is 'settled': ... trial merge ... full local test suite ... record the merge and the result in the ledger"; Q4 split "if the branch is open longer than about a week". | MET |
| C5 | Explicit out of scope | Q5 "Flags are not used."; Q3 "`integration`: not merged into the release branch." | MET |
| K1 | No factual errors | Ref rule "verified by the coordinator, CONTEXT.md line 8"; sort claim checks out (byte order: "/" 0x2F sorts before "0" 0x30, so `dash1.1/` precedes `dash1.105/`). | MET |
| K2 | Feasible with stated constraints | Q2 local coordinator merges, no per-story PR, CI only at the final PR: matches CONTEXT lines 9 and 11 and the CI scope as written; no constraint has to change. | MET |
| K3 | Terminology consistent | "release branch", "story", "settled", "coordinator", "foundation story" used the same way. | MET |
| K4 | No internal contradictions | Checked Q2 vs Q3 vs Q4 vs Q5 vs Q9 and steps 1 to 6; "never rebase" (Q3) matches Step 4 "a merge, never a rebase". | MET |
| K5 | Claims supported | Q5 "Driessen's own 2020 note says release branches fit software that is released as explicit versions (S3)"; Q2 "(S21: worktrees do not prevent semantic conflicts)". | MET |
| S1 | Logical section ordering | Summary, names, flow, questions, costs, favours, risks, sources. | MET |
| S2 | Consistent hierarchy depth | 8 H2, no H3. | MET |
| S3 | Separation of concerns | Costs (5), favours (6), risks (7), sources (8). | MET |
| S4 | Navigation aids | "(section 4, Q2)", "(Q7)", "(Q8)", "(Q3)", "Q4 and Q5". | MET |
| S5 | Artifact-type conventions | Branch table, ASCII flow, six numbered steps. | MET |
| L1 | Unambiguous language | Vague-list scan: 0 matches. | MET |
| L2 | Concrete rather than abstract | `dash1.3/release`, `dash1.3/s04-token-usage-panel`, `git merge-tree`, `git revert -m 1`. | MET |
| L3 | Each section has one clear purpose | Each H2 has one purpose. | MET |
| L4 | Terms defined on first use | Q2 "a first 'foundation' story that merges before the others start"; "settled" defined in Step 3; "leaf" defined in the ref-conflict rule. | MET |
| L5 | Actionable next steps or decisions | Six numbered steps; Q5 "If they do not, switch to Proposal 3." | MET |
| R1 | At least 3 risks with probability and impact | Section 7 lists 6 risks with no likelihood; Section 5 only ranks ("Review-size risk is the highest of the three proposals"). | NOT MET |
| R2 | Mitigation for each risk | Section 7 risk 6 "there is no pull request to review it in" and risk 4 have no mitigation; mitigations exist only for 1 to 3 and 5 (Q4, Q2, Q9). | NOT MET |
| R3 | Failure modes and recovery | Q9 release revert PR, "Prefer a bug-fix release", revert-then-redo caveat. | MET |
| R4 | External dependencies and their failure | Risk 4 "a prefix surprise could break the leaf rule if someone creates `dash1.3` by hand"; Q4 merge-commit setting UNVERIFIED. | MET |
| R5 | Monitoring or validation mechanism | Step 3 trial merge with `git merge-tree`, full local suite after each merge; Q8 path-claim comparison. | MET |
| E1 | Collection boundaries | Q6 "A one-story release can skip the release branch"; Q4 split "if the branch is open longer than about a week". | MET |
| E2 | State interactions across components | Q3 "Merging `integration` in would make the release pull request carry Clay's unreleased work into `master`." | MET |
| E3 | Guard condition gaps | Risk 4 (nothing stops someone creating the bare `dash1.3`); Q2 trial merge as the missing pre-merge guard. | MET |
| E4 | Count divergence | Section 2 "a future `1.10` would sort wrongly, so do not use it"; two-digit story numbers. | MET |
| E5 | Interaction effects | Q9 "If later stories depend on it, revert them in reverse order or fix forward."; Q2 (c) clean merges that still collide. | MET |

## 3. Qualitative summary (dimension subtotals, qual_score)

| Variant | Completeness (5) | Correctness (5) | Structure (5) | Clarity (5) | Risk Coverage (5) | Invariant and Edge Case (5) | Total met | qual_score (met / 30) |
|---|---|---|---|---|---|---|---|---|
| V4 | 4 | 3 | 4 | 4 | 3 | 3 | 21 | 0.7000 |
| V3 | 4 | 4 | 5 | 5 | 3 | 4 | 25 | 0.8333 |
| V2 | 4 | 4 | 5 | 5 | 3 | 3 | 24 | 0.8000 |
| V1 | 4 | 5 | 5 | 5 | 3 | 5 | 27 | 0.9000 |

Criteria that separate the variants: K2 (V1 only is feasible without changing a CONTEXT constraint), K4 (V4 only has contradictions), S5 and L4 (V4 only fails), E1 (V1 and V3 only), E2 (V4 only fails), E4 (V1 and V4 only). C1, R1 and R2 fail for all four under the uniform rules stated at the top of section 2, so they do not separate anyone.

For reference, correctness count (used by the tiebreaker level 2): V1 5, V2 4, V3 4, V4 3.

## 4. Invariant and Edge Case floor check

Floor rule: below 1 of 5 on the Invariant and Edge Case Coverage dimension makes a variant ineligible as base; the floor is suspended only if all variants score 0.

| Variant | E1 | E2 | E3 | E4 | E5 | Score | Eligible as base |
|---|---|---|---|---|---|---|---|
| V4 | NOT MET | NOT MET | MET | MET | MET | 3/5 | Yes |
| V3 | MET | MET | MET | NOT MET | MET | 4/5 | Yes |
| V2 | NOT MET | MET | MET | NOT MET | MET | 3/5 | Yes |
| V1 | MET | MET | MET | MET | MET | 5/5 | Yes |

No variant is below 1/5; no suspension warning is needed.

## 5. Items not counted or uncertain

1. SR is degenerate: the protocol vague list matched 0 units in all four variants, so SR = 1.0 for all. A wider hedge list would change this; none was applied because the protocol fixes the list.
2. DC is 1.0 for all four because the protocol excludes cross-document references. V3 has 10 "Proposal N" references and V1 has 1 that cannot be resolved inside their own file; if the reconciler counts them, V3 drops to 0.3750 (quant 0.8671) and V1 to 0.9167 (quant 0.9187). I did not apply this.
3. Scorable-claim counts (V4 46, V3 98, V2 92, V1 94) are a regex proxy (sentences or table rows with a digit, a backticked token or a named entity and no vague term), not an LLM reading of each claim. One contradiction changes IC by 1/46 (V4) or about 1/95 (others).
4. Requirement matching (RC) uses my 23-item list. Three judgement calls moved RC: B7 for V3 (N, no `orca worktree create` command), B9b for V1 (N, planning base never stated), B11 for V3 (Y, weak: cites CONTEXT line 16 only). Each flip moves that variant's quant_score by 0.013 (0.30 / 23).
5. Contradiction counting excluded disclosed trade-offs that offer a path (V2 ledger mismatch, V3 Open decision A, V3 planning-base change). If the reconciler counts V2's ledger mismatch, V2 IC = 0.9891 and quant = 0.9415; K4 for V2 would flip to NOT MET (qual 23/30 = 0.7667).
6. Strict rules (C1, K2, R1, R2) were applied the same way to all four. A looser reading of R1 (counting "most likely failure" in V2 risk 1 as enough) would still need three risks with likelihood and would not change V2. A looser C1 (nine questions answered) would add 1 point to every variant and change no ranking.
7. Not verified by me: V4's GFxAI facts (PR #147, #129, #131, "Pending team review"), V3's Chrome cycle and GitHub stacked-pull-request claims, V2's merge-queue plan limits. They are sourced to files or notes the variants name; none is contradicted by anything I read.
8. Debate lines 281-439 (round 2 rebuttals of advocates 1 to 3) were not read; the scoring matrix and the convergence section were read in full and agree with the contradictions counted here (X-003, X-008, A-017 for V4).
9. No ranking and no base selection is given here, as instructed.
