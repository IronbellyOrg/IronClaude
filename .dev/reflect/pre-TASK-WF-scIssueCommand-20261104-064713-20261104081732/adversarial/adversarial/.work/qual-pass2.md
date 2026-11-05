# Qualitative Scoring, Pass 2 (reverse order: V3, V2, V1)

Rubric: 30-criterion additive binary, Claim-Evidence-Verdict. No partial credit; no evidence = NOT MET.
Inputs: variant-3-original.md (V3), variant-2-original.md (V2), variant-1-original.md (V1); debate .work/round1-*.md, round2-*.md; diff-analysis.md; .work/evidence-sheet.md.
Interpretation: "requirements" = spec/plan points a reviewer should audit; "risks" = findings about failure modes; "sections" = YAML keys.
Debate outcome applied: C-001 (V1 A-1) survives as top-priority minor; V3 S-1/S-2 minor and S-2 "resume cannot work" conceded false; V2 PASS won X-001 but V2 missed C-001; A-002..A-007 missed by all cards.

Each cell: CLAIM is the criterion text applied to the variant; EVIDENCE quotes the card or the debate; VERDICT M (MET) / N (NOT MET).

## 1. Completeness

| Criterion | V3 | V3 evidence | V2 | V2 evidence | V1 | V1 evidence |
|---|---|---|---|---|---|---|
| 1 Covers all explicit requirements (no material miss) | N | Missed C-001 (live item-4 run; round2-v3.md:14 "That is a coverage miss in the safety focus area") and spec AC 5 first half / AC 8 offline half (A-002, A-003; diff-analysis "missed by all") | N | Missed C-001 and all eight shared-assumption items (round1-v2.md:35-36 "My card missed C-001 entirely"; "every calibrator missed_by_card item") | N | Caught C-001 (A-1) but missed AC 5 first half, AC 8 offline half, gh api `repos/<R>/` rule (A-002..A-004; round1-v1.md:78-84 "V1 missed ... AC 5's first half and AC 8's offline half") |
| 2 Edge cases / failure scenarios | M | S-8 "inventory 'every file in refs/, templates/, scripts/' fails on scripts/__pycache__"; S-7 tier member model vs picker ID | N | No evidence found: searched Q-1..Q-4 for edge, fail, empty, invalid; Q-1..Q-3 are deviation notes, Q-4 is posture | M | A-3 "first run 'assigned' cannot hold if the test task already lists the user"; A-6 invalid CLICKUP_MAX_PAGES |
| 3 Dependencies / prerequisites | M | S-3 "Task 17 depends on Task 14 only but cites Task 15 and Task 16 evidence"; S-9 interim reds until Task 9 | N | No evidence found: searched "depend", "prerequisite", "after Task", "before" in V2 card | M | A-2 "prerequisite says after Task 13 though it depends on Task 14"; A-1 rec "Read the implemented SKILL.md first"; round1_fix_check |
| 4 Success / completion criteria | M | S-2 on Task 15's stop/pending exit; S-7 "no transcript or log path named" for the AC evidence | M | Q-4 "Section 20 ACs 1, 2, 3, 6, 8 may end pending, so core end-to-end behaviour may ship unverified" | M | A-2 category ambiguous-ac "two incompatible exits"; A-3 'assigned' AC cannot hold |
| 5 Out-of-scope items | N | No evidence found: searched "out-of-scope", "defer", "pr-submit", "scope" in V3 card | M | Q-1 "Spec section 17 item 5 ... is only an out-of-scope note in Constraints" | N | No evidence found: searched "out-of-scope", "defer", "pr-submit", "scope" in V1 card |

## 2. Correctness

| Criterion | V3 | V3 evidence | V2 | V2 evidence | V1 | V1 evidence |
|---|---|---|---|---|---|---|
| 1 No factual errors or hallucinated claims | N | S-2 "resume cannot work" conceded false (round2-v3.md:24-25 "a false statement inside a blocking finding"); S-11 premise wrong, withdrawn (round2-v3.md:15-16) | N | self_audit "ACs observable" conceded false (round2-v2.md:13 "Conceded"); "audited sections 4, 7 ..." overstated (round2-v2.md:11) | N | A-1 "posts public comments on someone else's repo" overstated (round1-v1.md:71-72 concession); A-2 second half conceded wrong (round2-v1.md:25) |
| 2 Feasible recommendations | M | Every rec is an implementable plan edit, e.g. S-3 "Depends on: Task 14, Task 15, Task 16."; S-6 `test -n "${CLICKUP_API_TOKEN:-}"` | M | Q-1 "end Task 17's acceptance record with the exact /sc:pr-submit command"; Q-4 closing line asking for pre-approval | M | A-1 non-existent repo URL (amended to non-existent N, round2-v1.md:48 and endorsed by V2/V3); A-4 "delenv all four CLICKUP_* variables" |
| 3 Terminology and categories accurate and consistent | N | S-1 category "cross-task-contradiction"/blocking conceded "not a contradiction" and minor (round2-v3.md:26); S-2 blocking conceded minor | N | Q-2/Q-3 labelled deviation/weakened-test-scope though round-1-sanctioned; "Conceded on the label" (round2-v2.md:17-19) | N | A-1 "blocking"/"safety-risk" conceded to minor (round2-v1.md:3, :31) |
| 4 No internal contradictions | N | S-2 cites refs/ledger.md:161 Row S, which supports resume: "V3 even cites ledger.md:161 in its own evidence ... which supports the opposite" (round1-v2.md:28) | M | Verdict PASS, all four findings minor, self_audit consistent with findings; no conflicting statements found | M | FAIL verdict, self_audit "blocking A-1 introduced by the revision", and findings agree; no conflicting statements found |
| 5 Claims supported by citations | M | Every finding has an evidence list, e.g. S-5 [plan:56, src/superclaude/agents/evidence-validator.md:8]; S-7 tagged [INFERRED] | M | Every finding has evidence, e.g. Q-2 [source.md:149, plan:92] | M | Every finding has evidence, e.g. A-1 [plan:26, plan:254, plan:259, source.md:143 ...] |

## 3. Structure

| Criterion | V3 | V3 evidence | V2 | V2 evidence | V1 | V1 evidence |
|---|---|---|---|---|---|---|
| 1 Logical ordering | M | Blocking S-1, S-2 first, then minors S-3..S-12 | N | Q-1..Q-4 all minor, evidence source.md:408, 149, 391, 467 and plan:25, 92, 129, 15: neither spec, plan nor severity order | M | Blocking A-1 first, then minors A-2..A-6 |
| 2 Consistent hierarchy / schema | N | Mixed block style (S-1, S-2) and flow maps (S-3..S-12) (diff-analysis S-001) | M | "every finding is an inline flow map" (diff-analysis S-001) | M | "block-style findings with recommendation" throughout (diff-analysis S-001) |
| 3 Separation of concerns (one topic per finding) | N | S-6 joins two topics: "key-path comparison has no method; no safe presence check"; S-2 joins two alternative failure claims ("... cannot work ... or the executor writes 'pending'") | M | Q-1..Q-4 each one topic (PR deferral, --limit 200, source-only check, pending posture) | N | A-2 joins exits and dependency text (split across C-002 and C-007); A-3 joins four topics (method, status JSON, curl -v ban, 'assigned') |
| 4 Navigation aids (finding IDs) | M | IDs S-1..S-12 | M | IDs Q-1..Q-4 | M | IDs A-1..A-6 |
| 5 Follows reviewer-card conventions | M | reviewer, persona, model_class, verdict, findings{id, severity, category, claim, evidence, recommendation}, self_reported_confidence, self_audit | M | Same keys plus resolved_model and attempt (retry note) | M | Same keys plus round1_fix_check |

## 4. Clarity

| Criterion | V3 | V3 evidence | V2 | V2 evidence | V1 | V1 evidence |
|---|---|---|---|---|---|---|
| 1 Unambiguous language | N | S-2 states two alternative outcomes ("cannot work ... or the executor writes 'pending'"); S-7 hedged "[INFERRED]" "may show" | M | Plain single claims, e.g. Q-2 "Task 5 adds --limit 200 to the spec's verbatim merged-PR query." | M | Direct claims, e.g. A-4 "Tests clear only the token and workspace variables" |
| 2 Concrete | M | S-12 exact heading "### `/sc:issue` - GitHub Issue Claim and Create."; S-6 exact shell test | M | Q-1 names the exact command /sc:pr-submit --monitor 3 | M | A-1 example URL "https://github.com/IronbellyOrg/issue302-no-such-repo/issues/1" |
| 3 Each finding summarisable in one sentence | M | Longest (S-2) reduces to "Task 15's stop-and-resume does not fit /sc:implement's semantics"; flow-map minors are already one sentence | M | Each Q-n claim is one sentence | N | A-3 holds four separate claims (no method; status JSON only; curl -v/-i/--trace not banned; 'assigned' cannot hold) that one sentence cannot carry |
| 4 Terms / acronyms defined on first use | N | "D26 sentence", "picker ID", "tier member model", "AC" never defined | N | "ACs", "STOP codes" undefined | N | "Wave 0 guard", "E-FOREIGN-REPO", "AC" undefined |
| 5 Actionable next steps | M | Every finding has a recommendation, e.g. S-5 "Task 3: no permissionMode: plan; test asserts it." | M | Q-1 and Q-4 give concrete steps; Q-2/Q-3 explicit "leave as is"/"Keep" | M | Every finding has a recommendation, e.g. A-6 "falls back to 20 ... and exits 0" |

## 5. Risk Coverage

| Criterion | V3 | V3 evidence | V2 | V2 evidence | V1 | V1 evidence |
|---|---|---|---|---|---|---|
| 1 At least 3 risks with impact | M | S-5 "would ... block worker writes"; S-1 fork-safety test fails; S-8 inventory fails; S-2 "scheduled smoke spawn never happens" | N | Only Q-4 states an impact ("core end-to-end behaviour may ship unverified"); Q-1..Q-3 are deviation notes with "Acceptable"/"Keep" | M | A-1 "post public comments on someone else's repo"; A-4 variables "reach tests that pin page cap"; A-5 "false-positives on prose" |
| 2 A mitigation for each | M | All 12 findings carry a recommendation | M | Its one risk (Q-4) has a mitigation: "closing line asking the user to pre-approve one scratch test issue" | M | All 6 findings carry a recommendation |
| 3 Failure modes and recovery | M | S-2 "a stop goes to review/retry/halt and a re-run gives operator review" (recovery path addressed, though wrong per debate); S-9 interim reds "expected to fail until Task 9" | N | No evidence found: searched "fail", "stop", "resume", "retry", "recover" in V2 card | M | A-1 failure mode (guard wrong -> public writes) with containment "so any escaped write 404s"; A-2 "asks the user to restart" |
| 4 External dependencies (GitHub, ClickUp, gateway, executor) and their failures | M | GitHub S-1 (gh --repo); ClickUp S-4, S-6; gateway S-7 "tier proxy rewrites the alias"; executor S-2 sc-implement SKILL.md/ledger | N | Only self_audit "ClickUp posture satisfies section 12"; no failure of any dependency analysed | N | GitHub A-1, ClickUp A-3/A-4/A-6, executor A-2 (sc-implement SKILL.md:135); gateway: no evidence found, searched "gateway", "tier", "proxy", "model" |
| 5 Validation / monitoring mechanism | M | S-5 "test asserts it"; S-8 bounded inventory globs; S-6 presence check | M | Q-4 pre-approved scratch issue "so those items can run live" | M | A-1 "confirm E-FOREIGN-REPO precedes the first gh call and spawn"; A-4 delenv in every test |

## 6. Invariant and Edge Case Coverage

| Criterion | V3 | V3 evidence | V2 | V2 evidence | V1 | V1 evidence |
|---|---|---|---|---|---|---|
| 1 Collection boundaries (empty, single, max) | N | No evidence found: S-8 is membership (__pycache__), not empty/single/max; searched "empty", "max", "limit", "single" | N | Q-2 notes `--limit 200` but only as a disclosed addition; no boundary behaviour analysed; searched "empty", "max", "beyond" | M | A-6 "invalid CLICKUP_MAX_PAGES behaviour without bounding it ... falls back to 20" |
| 2 State interactions across components | M | S-1 Task 6 content vs Task 7 test; S-5 agent frontmatter permissionMode vs worker writes | N | No evidence found: searched "interaction", "across", "session", "state" in V2 card | M | A-1 Wave 0 guard vs later waves' writes; A-4 exported shell state leaking into tests |
| 3 Guard-condition gaps | M | S-6 "no safe presence check for the variables" (guard for the pending branch) | N | No evidence found: searched "guard", "STOP", "check" findings; self_audit only confirms STOP codes are present | M | A-1 "if the implemented Wave 0 guard is wrong ... the only protection is the code under test" |
| 4 Count divergence / off-by-one | N | No evidence found: S-3 is a dependency-set mismatch, S-9 names failing inventory tests without a count; searched "of the", "count", "only" | M | self_audit "all nine STOP codes in Task 6"; "section 15/16 inventories map one-to-one" | M | A-4 tests clear two of four CLICKUP_* variables ("only the token and workspace variables"; "an exported CLICKUP_MAX_PAGES or CLICKUP_LIST_IDS still reaches tests") |
| 5 Interaction effects of combined features | M | S-1 error table x fork-safety scan; S-4 secrets constraint x `env -u` | N | No evidence found: searched "combined", "conflict", "vs", "interaction" in V2 card | M | A-5 fork-safety line scan x spec prose copied into SKILL.md; A-1 approval carve-out x untested guard |

## Summary

| Dimension | V3 | V2 | V1 |
|---|---|---|---|
| Completeness | 3/5 | 2/5 | 3/5 |
| Correctness | 2/5 | 3/5 | 3/5 |
| Structure | 3/5 | 4/5 | 4/5 |
| Clarity | 3/5 | 4/5 | 3/5 |
| Risk Coverage | 5/5 | 2/5 | 4/5 |
| Invariant and Edge Case | 3/5 | 1/5 | 5/5 |
| **Total** | **19/30** | **16/30** | **22/30** |

Notes: Completeness 1, Correctness 1, Correctness 3 and Clarity 4 are NOT MET for all three cards (the shared-assumption misses, the conceded errors and severity labels, and undefined terms). V1 leads on invariant coverage and on carrying C-001; V3 leads on risk surface; V2 leads on structure and clarity but has the thinnest risk and invariant coverage.
