# Scoring Pass 1 (forward order: V1, V2, V3, V4)

## Metadata
- Step: /sc:adversarial Step 3 (Hybrid Scoring and Base Selection), evaluator pass 1, variants evaluated in INPUT ORDER.
- Variants: V1 = `adversarial/variant-1-original.md` (release line, story branches, local merges); V2 = `variant-2-original.md` (trunk on `integration`, dark landing); V3 = `variant-3-original.md` (release train, PR-gated batch); V4 = `variant-4-original.md` (GFxAI approach adapted).
- Source requirements: the nine numbered questions plus the thirteen hard facts and constraints in `CONTEXT.md` (22 requirements, listed in 1.1).
- Not done here, by instruction: no combined ranking, no base choice, no tiebreaker. Pass 2 was not read.
- Dash rule: no em dashes; hyphens only.

## 1. Quantitative layer (counts shown)

Counting commands were read-only `grep`, `sed` (stdout only) and `wc` over each variant file. Body text = the variant minus headings, table separator rows and the Sources section.

### 1.1 RC, Requirement Coverage

CONTEXT.md has no formal requirement IDs, so the edge-case rule applies: topic matching on the nine questions plus the listed facts and constraints. A requirement counts as matched when the variant names it (ID, keyword, or 3 or more consecutive words of the requirement) and engages it. Matching is deliberately by presence, not by quality; quality is scored in the qualitative layer.

| ID | Requirement (CONTEXT.md) | V1 | V2 | V3 | V4 |
|----|--------------------------|----|----|----|----|
| Q1 | Names: release and story branch names | Y (sec 2, Q1) | Y | Y | Y (rule 1) |
| Q2 | Where and how story work merges, conflicts, collisions | Y | Y | Y | Y |
| Q3 | Keeping the line current with master and integration | Y | Y (Q3: no long line, story branches merge integration) | Y | Y |
| Q4 | How the release lands | Y | Y | Y | Y |
| Q5 | Flags, trunk-based, long-lived branches justified | Y | Y | Y | Y |
| Q6 | Hotfixes and bug fixes during a release | Y | Y | Y | Y |
| Q7 | Clean-up and records kept | Y | Y | Y | Y |
| Q8 | Fit with integration and Clay | Y | Y | Y | Y |
| Q9 | Failure and rollback | Y | Y | Y | Y |
| F1 | `dash1.3` and `dash1.3/story1` cannot coexist (ref conflict) | Y (leaf rule) | Y (flat names) | Y | Y (different folders) |
| F2 | Orca `ironbelly/` prefix | Y | Y | Y | Y |
| F3 | Conflict is stopped and reported, never resolved automatically (worker contract) | Y ("never resolves automatically (worker contract)") | N (says the coordinator "never has to stop on a conflict"; no worker-contract rule named) | Y | Y |
| F4 | Two parallel stories, disjoint paths, serial merges | Y | Y | Y | Y |
| F5 | `/sc:pr-submit --monitor 3` only path, never rewrites a published branch, `--base` | Y | Y | Y | Y |
| F6 | CI only for PRs into master and integration | Y ("no CI ... per story", `test.yml`) | Y | Y | Y (closing section) |
| F7 | Owner merges every PR; nothing merged by an agent | Y | Y | Y | Y |
| F8 | `worker-start` has no `--branch`; use `orca worktree create --branch` | Y (names both) | Y (gives the command) | N (only "when `--branch` is given"; no command, no worker-start note) | Y (names the command) |
| F9 | No commit on master; never touch upstream SuperClaude-Org | N | N | N | N |
| F10 | `.dev/` records and ledger on the release branch; planning of n+1 from master | Y (Q7, step 1) | Y (Q7, as a mismatch) | Y (Q7, Q8) | Y (`.dev/` records only, Q7) |
| F11 | Release numbers are dashboard numbers (1.1, 1.105 ...), not package versions | Y (sort note, 1.105) | Y (Q6) | Y (Q6) | Y (tag note, "package is 6.1.0") |
| F12 | Scale: bursts of 15 to 60 AI PRs | N | Y (sec 5) | Y (Q3, "AI speed") | N |
| F13 | `integration` exists; Clay branches from it | Y | Y | Y | Y |
| | **Matched / 22** | **20** | **20** | **20** | **20** |
| | **RC** | **0.9091** | **0.9091** | **0.9091** | **0.9091** |

Note: all four tie on RC. On the nine questions alone each is 9/9. The metric does not separate the variants.

### 1.2 IC, Internal Consistency

Total scorable claims = sentence terminators counted in the body text (an upper-bound proxy; hedged and UNVERIFIED sentences are included). Contradictions = opposing claims about one subject inside one variant, read by me.

| Variant | Total claims (proxy) | Contradictions found | IC |
|---------|----------------------|----------------------|----|
| V1 | 126 | 0 | 1.0000 |
| V2 | 118 | 0 | 1.0000 |
| V3 | 126 | 0 | 1.0000 |
| V4 | 86 | 2 | 0.9767 |

Contradictions in V4 (both also logged as X-003 and X-008 in `adversarial/diff-analysis.md`):
1. Opposing claims on `integration`: Q4 "Not through `integration`" and Q8 "a dashboard release does not pass through it" versus Q3 "merge, never rebase, `master` and `integration` into `release/dash1.3`" and Q8 "`integration` is merged into `release/dash1.3` before the release pull request (question 3)".
2. Opposing claims on when CI and reviewers run: Q4 "CI and the two reviewers run once, at that point" versus Q2 story pull requests "with the tests for that level and at least one review" and the closing section "add `release/**` to its pull-request branch list" for CI.

I looked for self-contradictions in V1, V2, V3 and found none. Sensitivity (not used in the score above): if an unresolved self-declared clash with a stated constraint is counted as a requirement-constraint conflict, V2 gets 1 (Q7 and sec 5: "The ledger-on-the-release-branch convention does not fit") and V3 gets 1 (Q2 and Open decision A: the standing "owner merges every pull request" rule). IC would then be V2 0.9915, V3 0.9921.

### 1.3 SR, Specificity Ratio

Formula as written in the protocol: SR = concrete_count / (concrete_count + vague_count), counted as indicator occurrences in the body text. Concrete = numbers, backticked identifiers (branch names, commands, files), named entities (Orca, GitHub, DORA, Fowler, Driessen, Augment, Codex, Clay, BMAD, Microsoft, Mozilla, Chrome, PostHog, Faros, Unleash, GFxAI, Makefile). Vague = the protocol lexicon (appropriate, as needed, properly, adequate, should consider, might, various, etc., best practices, industry standard).

| Variant | Numbers | Backticked | Named entities | Concrete total | Vague (lexicon) | SR |
|---------|---------|------------|----------------|----------------|-----------------|----|
| V1 | 104 | 99 | 23 | 226 | 0 | 1.0000 |
| V2 | 103 | 86 | 29 | 218 | 0 | 1.0000 |
| V3 | 102 | 110 | 26 | 238 | 0 | 1.0000 |
| V4 | 65 | 80 | 11 | 156 | 0 | 1.0000 |

The lexicon found no hits in any variant, so SR is 1.0 for all four and does not separate them. Sensitivity with soft hedges added to the vague count (probably, mostly, roughly, may, could, usually, often, likely, largely): hedge counts V1 2, V2 5, V3 4, V4 1, giving SR 0.9912, 0.9776, 0.9835, 0.9936. Explicit gap labels are counted separately and are not vague: UNVERIFIED V1 6, V2 7, V3 6, V4 1; UNSPECIFIED V4 7.

### 1.4 DC, Dependency Completeness

Internal references only (section and question cross-references, "Open decision" references, "below" references). Evidence IDs (S1 and so on), `CONTEXT.md` line numbers and `research-notes.md` are external and excluded. Cross-proposal references ("Proposal 3", "of the three proposals") point to other documents and are excluded; see the sensitivity line.

| Variant | Internal references found | Resolved | DC |
|---------|---------------------------|----------|----|
| V1 | 10: "(section 4, Q2)", "(Q7)", "(Q8)" in step 6, "See section 2", "(Q9)", "(Q8)" in Q3, "(Q8)" in Q7, "(Q3)" in Q8, "see Q4 and Q5" (2) | 10 | 1.0000 |
| V2 | 3: "See section 2", "(Q9)", "see Q3 note" | 3 | 1.0000 |
| V3 | 6: "See section 2", "Open decision A below" (to sec 8), "(Q9)", "(Q6)", "cadence rule (below)" (resolves to the Q5 time box by substance, not by name), "(Open decision A)" in sec 5 | 6 | 1.0000 |
| V4 | 3: "(question 3)", "(question 4)" in Q8, "question 4" in Q9 | 3 | 1.0000 |

Sensitivity if cross-proposal references were counted as unresolved: V1 about 2 (Q5 "switch to Proposal 3", sec 5 "of the three proposals"), V2 about 3 ("of the three" in Q2, sec 5, Q9), V3 about 9 (Proposal 1 and Proposal 2 in the Summary, Q4, Q5, sec 5, risks, Open decision A), V4 0. That would read V1 10/12, V2 3/6, V3 6/15, V4 3/3. It is not used because the protocol excludes other documents, but it shows that V1, V2 and V3 are written as members of a set and V4 is self-contained.

### 1.5 SC, Section Coverage

Top-level (H2) headings counted with `grep -c '^## '`.

| Variant | H2 sections | H3 | SC (H2 / 9) |
|---------|-------------|----|-------------|
| V1 | 8 | 0 | 0.8889 |
| V2 | 8 | 0 | 0.8889 |
| V3 | 9 (max) | 0 | 1.0000 |
| V4 | 3 | 9 | 0.3333 |

V4 puts its nine answers at H3 under one H2, so by the protocol's H2-only rule it scores low on a formatting choice, not on missing content. If the nine H3 answers were counted it would be 12 of 12 and SC would be 1.0 (not used).

### 1.6 Quant score

quant_score = 0.30 RC + 0.25 IC + 0.15 SR + 0.15 DC + 0.15 SC

| Variant | 0.30 RC | 0.25 IC | 0.15 SR | 0.15 DC | 0.15 SC | **quant_score** |
|---------|---------|---------|---------|---------|---------|-----------------|
| V1 | 0.2727 | 0.2500 | 0.1500 | 0.1500 | 0.1333 | **0.9561** |
| V2 | 0.2727 | 0.2500 | 0.1500 | 0.1500 | 0.1333 | **0.9561** |
| V3 | 0.2727 | 0.2500 | 0.1500 | 0.1500 | 0.1500 | **0.9727** |
| V4 | 0.2727 | 0.2442 | 0.1500 | 0.1500 | 0.0500 | **0.8669** |

The quant layer separates V4 (low SC, two contradictions) from the rest, and separates V3 from V1 and V2 only by one extra H2 section.

## 2. Qualitative layer: 30-criterion binary rubric with Claim-Evidence-Verdict

Format note: in every cell the CLAIM is the row's criterion text applied to that variant ("[criterion] is met in Vn"); the cell gives the VERDICT first (MET = 1, NOT MET = 0) and then the EVIDENCE (quote or section; "none found" lists what was searched). No partial credit. A MET with no citable evidence would be NOT MET. Sections are cited as in the variant files ("sec 4" = H2 section 4; "Q2" = the bold Q2 paragraph; "rule 2" = V4's H3). Evaluated in order V1, V2, V3, V4 for each criterion.

### 2.1 Completeness (5)

| # | Criterion | V1 | V2 | V3 | V4 |
|---|-----------|----|----|----|----|
| 1 | Covers all explicit requirements from source input | MET. All nine questions answered in sec 4 (Q1 to Q9); ledger on the release branch kept: Q7 "`sprint-status.yaml` are committed on the release branch and land on `master` with it". | MET. Q1 to Q9 answered; the ledger fact is engaged in Q7 ("This is a real mismatch"), though not satisfied. | MET. Q1 to Q9 answered; ledger kept (Q7) and planning base addressed (Q8 "planning must start from `integration`"). | NOT MET. Nine rules answered, but the release branch's base is never stated (rules 1 to 4 silent; rule 4 only "straight into `master`"), and the ledger home and planning base of release n+1 are absent (rule 7 mentions only ".dev/ records committed on the release branch"). |
| 2 | Addresses edge cases and failure scenarios | MET. Q9 rollback of a bad story and a failed release; Q2 "If it would conflict, stop"; sec 7 lists six risks. | MET. Q9 "revert pull request for that one squash commit, or switch its flag off"; risk 3 "`integration` can go red". | MET. Q9 three layers (story out of train, train out of `integration`, promotion out of `master`). | MET. Rule 9 "revert its single squash commit on the release branch"; "revert the release's merge commit on `master`". |
| 3 | Includes dependencies and prerequisites | MET. Q2(b) "shared files ... belong to exactly one story or to a first 'foundation' story that merges before the others start". | MET. Q2 "Dependent slices are not stacked ... The dependent slice starts after its predecessor merged"; shared files go "in their own first slice". | MET. Sec 5 "One change to `.github/workflows/test.yml` ... and a branch-protection or ruleset entry for `train/*`"; sec 8 Open decisions A to C. | MET. Closing section "What this proposal needs that the source does not give": "a CI trigger for pull requests into `release/**` ... a rule for who may merge into the release branch; the tag scheme". |
| 4 | Defines success/completion criteria | MET. Sec 3 step 3 "Story is 'settled': ... trial merge ... full local test suite ... record the merge and the result in the ledger"; step 5 release readiness. | MET. Sec 3 step 5 "When the switch-on slice has merged and the owner decides to ship". | MET. Sec 1 "The train departs when its planned stories are in, or at a set time"; step 6. | MET. Rule 4 "full test tiers, two approvals and sign-off, then a tag"; rule 7 delete "once its squash commit is in the release branch and recorded in the ledger". |
| 5 | Specifies what is explicitly out of scope | NOT MET. None found; searched sec 1, Q5, sec 5, sec 7. Exclusions appear only as design choices ("Flags are not used"). | NOT MET. None found; searched sec 1, Q3, Q5, sec 5. ("this proposal does not depend on it" is a design note on merge queues, not a scope statement.) | NOT MET. None found; searched sec 1, Q5, sec 5, sec 8. ("native GitHub stacked pull requests feature is not assumed available" is an assumption.) | NOT MET. None found; searched the paragraph, rules 1 to 9, closing section. UNSPECIFIED marks gaps in the source, not scope limits of this proposal. |

### 2.2 Correctness (5)

| # | Criterion | V1 | V2 | V3 | V4 |
|---|-----------|----|----|----|----|
| 1 | No factual errors or hallucinated claims | MET. Claims I could check hold: sec 2 ref-conflict rule (verified in a scratch repo, CONTEXT line 8); Q3 "Merging `integration` in would make the release pull request carry Clay's unreleased work" (confirmed in the debate by a scratch `git diff --stat master...release/dash1.3`); unverified items are labelled (6 UNVERIFIED marks). | MET. Q2 "CI only runs for pull requests into `master` and `integration`" matches CONTEXT line 11; flat names cannot collide (matches the scratch test); 7 UNVERIFIED marks on unchecked items. External S-ID claims not checked by me. | MET. Q2 / sec 3 step 3 "CI does not run on a pull request whose base is a story branch under the present workflow" matches the `test.yml` filter reported in the debate; 6 UNVERIFIED marks. External S-ID claims not checked by me. | MET. Rule 1 "`release/dash1.3` and `dash1.3/story/01-...` are in different folders, so git accepts both" matches the debate's scratch test. GFxAI figures (PR #147, 1,384 files) are not checkable by me; no claim contradicts CONTEXT.md. |
| 2 | Technical approaches are feasible with stated constraints | MET. Fits every constraint: pr-submit once at the end, local coordinator merges per the worker contract, sec 6 "no change to CI or repository settings". | NOT MET. Sec 5 "The ledger-on-the-release-branch convention does not fit." and Q7 "a real mismatch and the biggest process cost"; Q5 dark landing "UNVERIFIED". As written it cannot meet CONTEXT line 14. | MET. Works inside the constraints once decisions A and C are answered; the fallback is written ("No: use Proposal 1 or accept the owner as the merge lane"); ledger kept (Q7). Borderline: depends on owner decisions. | NOT MET. Rule 4 "CI and the two reviewers run once, at that point" cannot hold together with rule 2 per-story pull requests that need CI on `release/**`, which `test.yml` does not trigger (closing section); the release base is unstated. |
| 3 | Terminology used consistently and accurately | MET. "release branch" = `<release>/release`, "story branch" and "settled" (step 3) used consistently. | MET. "slice", "promotion pull request", "dark" defined in sec 1 and step 1 and used consistently. | MET. "train", "story", "sync branch", "departure" used consistently. | MET. Four provenance marks defined once and applied to each rule; "feature branch" versus "story branch" difference flagged in rule 1. |
| 4 | No internal contradictions (cross-validated with IC) | MET. IC 1.0000; checked Q2 versus sec 3, Q3 versus Q8 (integration never merged in; merge not rebase throughout). | MET. IC 1.0000; squash per slice (Q2, step 4) and merge commit for the promotion (Q4) do not conflict. | MET. IC 1.0000; merge commit used in Summary, step 4, Q2, Q4. | NOT MET. Two contradictions in 1.2: the `integration` path (rules 3, 4, 8) and when CI runs (rules 2, 4, closing section). |
| 5 | Claims supported by evidence or rationale | MET. Q2 "One merge commit per story means one `git revert -m 1` removes the whole story later (Q9)"; evidence IDs S1 to S21. | MET. Q5 "trunk-based branches last about two days (S1); DORA calls a batch over a week too big and says small batches are the countermeasure (S6)". | MET. Q5 "The scope floats, the time does not ... Chrome moved from four weeks to two, S22". | MET. Rule 3 "Reason: stories branch from the release branch, and `/sc:pr-submit` never rewrites a published branch"; rule 7 "Why add a rule: FROM PRACTICE GFxAI left 6 `backup/...` branches". |

### 2.3 Structure (5)

| # | Criterion | V1 | V2 | V3 | V4 |
|---|-----------|----|----|----|----|
| 1 | Logical section ordering | MET. Summary, names (sec 2), merge flow (sec 3), nine questions, costs, favours, risks, sources; names come before the flow that uses them. | MET. Same order as V1. | MET. Same order plus "Open decisions" (sec 8) after risks and before sources. | MET. "In one paragraph", then rules 1 to 9 in CONTEXT's question order, then the needs list. |
| 2 | Consistent hierarchy depth, no orphaned subsections | MET. 8 H2, 0 H3; questions are uniform bold paragraphs. | MET. 8 H2, 0 H3. | MET. 9 H2, 0 H3. | MET. 3 H2, 9 H3, all H3 under "The rules, in order of the nine questions"; no level skipped. |
| 3 | Clear separation of concerns between sections | MET. Names (sec 2), flow (sec 3), answers (sec 4), costs (sec 5), beneficiaries (sec 6), risks (sec 7) are separate. | MET. Same split. | MET. Same split plus decisions (sec 8). | MET. Source versus adaptation separated by the provenance tags; gaps in their own closing section. Costs and risks are absent (scored under criterion 5). |
| 4 | Navigation aids present | MET. Numbered sections and cross-references: "(section 4, Q2)", "See section 2", "see Q4 and Q5". | MET. "See section 2", "(see Q3 note)". | MET. "See section 2", "Open decision A below". | MET. Rules numbered 1 to 9 to match CONTEXT's questions; "(question 3)", "(question 4)" cross-references; Marks legend at the top. |
| 5 | Follows conventions of the artifact type | MET. Summary, design, costs, beneficiaries, risks, sources: a complete decision proposal. | MET. Same layout. | MET. Same layout plus open decisions. | NOT MET. No costs, beneficiaries, risks or sources section (diff-analysis S-005: "None; only the list of what the source does not give"). |

### 2.4 Clarity (5)

| # | Criterion | V1 | V2 | V3 | V4 |
|---|-----------|----|----|----|----|
| 1 | Unambiguous language (no "should consider", "might", "as appropriate") | MET. 0 hits for the protocol lexicon (grep over body text); 2 soft hedges only. | MET. 0 lexicon hits; 5 soft hedges (for example "probably cannot use"). | MET. 0 lexicon hits; 4 soft hedges. | MET. 0 lexicon hits; 1 soft hedge. |
| 2 | Concrete rather than abstract | MET. Sec 2 gives "`orca worktree create --branch dash1.3/s04-token-usage-panel --base-branch dash1.3/release --parent-worktree <release worktree> --agent claude`"; `git merge-tree`; `git revert -m 1`. | MET. Step 2 "`orca worktree create --branch dash1.3-s04-p1-... --base-branch integration --agent claude`". | MET. Step 2 "`/sc:pr-submit --monitor 3 --base train/dash1.3`"; CI pattern `train/*`. | MET. Exact patterns and actions: `dash1.3/story/01-widget-grid`, "Squash merge to release", "Tag: `dash-1.3`". No commands, but actions are specific. |
| 3 | Each section has a clear purpose or one-sentence summary | MET. Titles state purpose ("What it costs", "Who it favours", "Risks"). | MET. Same. | MET. Same plus "Open decisions this proposal raises". | MET. "In one paragraph", "The rules, in order of the nine questions", "What this proposal needs that the source does not give". |
| 4 | Acronyms and domain terms defined on first use | NOT MET. "CI" (sec 1), "DORA" (Q4), "ledger", "coordinator", "Orca" used without definition; only UNVERIFIED and the S-IDs are explained in the header. | NOT MET. "dark" is defined (sec 1) but "CI", "DORA" (Q5), "PostHog", "ledger" are not. | NOT MET. "train" is defined (sec 1) but "CI", "DORA", "Mozilla and Chrome", "ledger" are not. | NOT MET. Marks are defined, but "CI", "UAT sign-off", "Tier 1 + Tier 2 + Tier 3" and "Interface-First design" are not. |
| 5 | Actionable next steps or decision points clearly identified | MET. Sec 3 steps 1 to 6; Q4 "split it if the branch is open longer than about a week"; Q5 "If they do not, switch to Proposal 3". | MET. Sec 3 steps 1 to 6; Q5 "the first thing to test on one story". | MET. Sec 8 Open decisions A (merge authority), B (time box), C (edit `test.yml`). | MET. Closing section lists five things the owner or coordinator must supply (CI trigger, merge rule, tag scheme, bug-fix and test-only naming, clean-up and rollback). |

### 2.5 Risk Coverage (5)

| # | Criterion | V1 | V2 | V3 | V4 |
|---|-----------|----|----|----|----|
| 1 | At least 3 risks with probability and impact assessment | NOT MET. Sec 7 lists six risks with no probability or impact rating; only a relative ranking in sec 5 ("Review-size risk is the highest of the three proposals"). | NOT MET. Sec 7 lists six risks; one likelihood phrase, in sec 5 ("most likely failure is a queue of ready slices waiting for the owner"); no ratings. | NOT MET. Sec 7 lists six risks, none rated. | NOT MET. No risk section; none found in rules 1 to 9 or the closing section. |
| 2 | Mitigation for each identified risk | NOT MET. Risks 1 to 3 are mitigated elsewhere (Q4 story-count cap, digest, one-week split; Q2 guards), but risks 4 (Orca prefix) and 6 (no early review) have none. | NOT MET. Risk 2 has "first thing to test on one story" and risk 6 "retire each flag"; risks 1, 3, 4, 5 (owner queue, red `integration`, Clay's work bundled, ledger) have none. | NOT MET. Risk 5 "Check by opening one test pull request first" and risk 1 via Open decision A; risks 2, 3, 4, 6 have none. | NOT MET. No risk list, so no mitigation per risk. |
| 3 | Failure modes and recovery procedures | MET. Q9 "`git revert -m 1 <story merge commit>` ... revert the release merge commit on `master` through a revert pull request". | MET. Q9 "revert pull request for that one squash commit, or switch its flag off ... or cherry-pick the fix into `release/dash1.3` and promote again". | MET. Q9 revert of a story merge into the train, of the train merge in `integration`, of the promotion on `master`. | MET. Rule 9 revert of one squash commit; revert of the release merge commit on `master`, then fix and a new pull request. |
| 4 | External dependencies and their failure scenarios | MET. Risk 4 "Orca prefix behaviour with `--branch` unverified; a prefix surprise could break the leaf rule"; Q4 merge-commit setting UNVERIFIED. | MET. Risk 3 "`integration` can go red because of someone else's merge, stalling all slices"; Q3 merge queue plan UNVERIFIED. | MET. Risk 5 "Wrong pattern in the CI filter ... leaves story pull requests with no CI while everyone assumes they have it"; risk 6 bot behaviour on `train/*` bases. | MET. Rule 1 "If `orca worktree create --branch` does not stop the prefix, every name gets `ironbelly/` in front; the rule still holds". Thinner than the others. |
| 5 | Monitoring or validation mechanism for risk detection | MET. Step 3 trial merge with `git merge-tree` and a full local suite after each merge; Q8 path-claim comparison against open `integration` pull requests. | MET. Q2 "CI on every slice runs against the real `integration`, so semantic collisions show as a red check"; Q5 test one story first. | MET. Risk 5 test pull request; per-story CI and both reviewers (Q2). | MET. Rule 2 "tests for that level and at least one review"; rule 4 full tiers; rule 6 "Beta freeze". |

### 2.6 Invariant and Edge Case Coverage (5)

| # | Criterion | V1 | V2 | V3 | V4 |
|---|-----------|----|----|----|----|
| 1 | Boundary conditions for collections (empty, single-element, maximum size) | MET. Q6 "A one-story release can skip the release branch" (single element); Q4 "treat the release as 'too big' and split it if the branch is open longer than about a week" (maximum). | MET. Sec 1 "one or more small pull requests" (single, several); Q4 "Release size is bounded by the slices". No empty case. | MET. Q6 "A one-story release skips the train ... (no train branch for a batch of one)"; Q5 time box as the maximum. | MET. Rule 4 "Size warning, FROM PRACTICE: ... #147 had 34 commits, 1,384 files, +242,976 lines" (maximum). |
| 2 | State variable interactions across component boundaries | MET. Q2(c) "the full local test run after each merge is the only thing that catches a semantic collision that merges cleanly". | MET. Q2 "CI on every slice runs against the real `integration`, so semantic collisions show as a red check". | MET. Q2 "a semantic collision shows as a red check on the next story's pull request, one story later at worst". | MET. Rule 3 merges "done by the coordinator between two story merges (never mid-merge)". |
| 3 | Guard condition gaps (missing validation, unguarded assumptions) | MET. Sec 3 step 3 trial merge before touching the release tip; "If it would conflict, stop". | MET. Q2 "two slices in parallel must declare disjoint paths; the coordinator sequences any pair that shares a file". | MET. Risk 5 names the gap "no CI while everyone assumes they have it" and gives the test-PR check. | MET. Rule 2 "the source has Interface-First design and mocks ... and nothing about file paths. MY ADAPTATION: ... disjoint paths". |
| 4 | Count divergence scenarios (off-by-one, inclusive/exclusive ranges) | MET. Sec 2 "`s01` to `s99`" and "a future `1.10` would sort wrongly, so do not use it" (names the 1.1 / 1.10 / 1.105 ordering divergence). | NOT MET. Sec 2 gives the range "`dash1.3-s01` to `dash1.3-s99`" only; no divergence case (no 1.10, no 100th story). Searched sec 2, Q1. | NOT MET. Sec 2 "story branches sort by release then story number"; no divergence case. Searched sec 2, Q1. | NOT MET. Rule 1 "two-digit story number (zero padded so they sort)"; no divergence case. Searched rule 1. |
| 5 | Interaction effects when features or components combine | MET. Q3 "Merging `integration` in would make the release pull request carry Clay's unreleased work into `master`". | MET. Q4 "the promotion carries Clay's merged work too. The dashboard release cannot be shipped without it". | MET. Risk 3 "A train branch cut from `integration` inherits whatever red or half-done work `integration` has at the cut". | MET. Rule 2 "It clashes with `/sc:pr-submit`, which never rewrites a published branch" (source rebase-only rule against the tool). It misses the `integration` merge interaction, which is charged under Correctness 4. |

## 3. Qualitative summary (pass 1)

| Dimension (5 each) | V1 | V2 | V3 | V4 |
|--------------------|----|----|----|----|
| Completeness | 4 | 4 | 4 | 3 |
| Correctness | 5 | 4 | 5 | 3 |
| Structure | 5 | 5 | 5 | 4 |
| Clarity | 4 | 4 | 4 | 4 |
| Risk Coverage | 3 | 3 | 3 | 3 |
| Invariant and Edge Case | 5 | 4 | 4 | 4 |
| **Total met / 30** | **26** | **24** | **25** | **21** |
| **qual_score** | **0.8667** | **0.8000** | **0.8333** | **0.7000** |

Where the verdicts move between variants (these are the rows a pass-2 comparison should look at):
- Completeness 1 (V4 only NOT MET): release base, ledger home and planning base missing.
- Correctness 2 (V2 and V4 NOT MET): V2 cannot satisfy the ledger convention; V4's CI statements cannot both be implemented. V3 is MET but borderline because it depends on owner decisions A and C.
- Correctness 4 (V4 only NOT MET): the two contradictions in 1.2.
- Structure 5 (V4 only NOT MET): no costs, risks or sources section.
- Invariant 4 (V1 only MET): the "1.10 would sort wrongly" case.
- Clarity 4, Risk 1, Risk 2, Completeness 5 are NOT MET for all four, so they do not separate the variants. If another evaluator reads "defined on first use" or "out of scope" more loosely, those rows can flip together for all four.

Correctness count for the tiebreaker rule, from this pass only: V1 5, V2 4, V3 5, V4 3 (pass-1 view; the reconciler decides whether it is needed).

## 4. Invariant and Edge Case floor check

Floor rule: below 1 of 5 on Invariant and Edge Case Coverage makes a variant ineligible as base.

| Variant | Invariant and Edge Case score | Eligible as base |
|---------|-------------------------------|------------------|
| V1 | 5 / 5 | Yes |
| V2 | 4 / 5 | Yes |
| V3 | 4 / 5 | Yes |
| V4 | 4 / 5 | Yes |

No variant is below the floor and the floor is not suspended (no variant scored 0).

## 5. Pass-1 results at a glance (no ranking, no base choice)

| Variant | quant_score | qual_score (met / 30) |
|---------|-------------|-----------------------|
| V1 | 0.9561 | 0.8667 (26 / 30) |
| V2 | 0.9561 | 0.8000 (24 / 30) |
| V3 | 0.9727 | 0.8333 (25 / 30) |
| V4 | 0.8669 | 0.7000 (21 / 30) |

## 6. What I could not count or verify

- IC claim totals are a sentence-terminator proxy (126, 118, 126, 86), not a hand-extracted list of falsifiable claims; the contradiction counts (0, 0, 0, 2) come from reading, and the sensitivity line shows the effect of counting unresolved self-declared constraint clashes.
- RC is presence matching; F3 for V2 and F8 for V3 are judgement calls (I scored both N). Flipping both would make RC 0.9545 for V2 and V3 and change quant_score by about +0.014 each.
- SR and DC are 1.0 for all four under the protocol's own lexicon and exclusion rules, so they carry no information in this pass; the sensitivity lines are the only signal and are not used in the scores.
- External evidence (S1 to S22 in `research-notes.md`, GFxAI numbers such as PR #147) was not opened or checked by me. Correctness 1 is judged only against `CONTEXT.md`, the variants, and verifications reported in `diff-analysis.md` and `debate-transcript.md`.
- `adversarial/invariant-probe.md` describes the consensus design rather than the four original variants, so I did not use it for any score.
- Pass 2 (reverse order) was not read.
