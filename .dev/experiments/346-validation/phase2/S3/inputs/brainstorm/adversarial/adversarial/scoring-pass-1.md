# Scoring pass 1: launch-level hook design specs (issue #394)

Order of evaluation: A = Variant 1 (architect), B = Variant 2 (refactorer), C = Variant 3 (QA).
Sources read: the three variants, `diff-analysis.md`, `seed-brief.md`, `enrichment/research-light.md`, the 8 acceptance criteria of issue #394.
Repository facts I re-checked myself: `_FRESHNESS_SCRIPTS` is defined only in `src/superclaude/cli/install_hooks.py` (the Makefile imports it at lines 309 to 325); `hooks.json` already uses regex alternation matchers (`Edit|Write`, `startup|resume`); `pyproject.toml` sets `--strict-markers` and no `manual` marker is registered.

## 1. Quantitative layer

| Metric | A: Variant 1 | B: Variant 2 | C: Variant 3 |
|---|---|---|---|
| RC requirement_coverage | 13/13 = 1.000 | 13/13 = 1.000 | 13/13 = 1.000 |
| IC internal_consistency | 1 - 1/56 = 0.982 | 1 - 1/49 = 0.980 | 1 - 3/56 = 0.946 |
| SR specificity_ratio | 59/61 = 0.967 | 57/59 = 0.966 | 52/53 = 0.981 |
| DC dependency_completeness | 97/98 = 0.990 | 98/98 = 1.000 | 108/112 = 0.964 |
| SC section_coverage | 16/16 = 1.000 | 16/16 = 1.000 | 16/16 = 1.000 |
| quant_score | 0.989 | 0.990 | 0.978 |

quant_score = 0.30*RC + 0.25*IC + 0.15*SR + 0.15*DC + 0.15*SC.
- A: 0.300 + 0.2455 + 0.1451 + 0.1485 + 0.150 = 0.9891
- B: 0.300 + 0.2449 + 0.1449 + 0.150 + 0.150 = 0.9898
- C: 0.300 + 0.2366 + 0.1472 + 0.1446 + 0.150 = 0.9784

### Counts used

**RC.** All 13 requirements are matched in all three variants. A requirement counts as matched when a section or named test addresses it concretely. Matching says nothing about whether the design is right; correctness defects are charged under IC and the qualitative layer.
- AC-1 to AC-8: each variant has a section 13 acceptance criteria map plus a decision table and test cases (A sections 5, 6, 12, 13; B sections 5, 6, 12, 13; C sections 5, 6, 12, 13).
- SC-1 (every AC maps to a table row and a named test): the section 13 map in each variant.
- SC-2 (block message says what, why, what a human can do): section 11 in each variant. Note C's MSG-SELF has no next step.
- SC-3 (ordinary session pays one cheap check, never blocked): A fast paths 1 and 2 and `test_ordinary_session_never_blocked`; B section 10 plus `test_ordinary_never_blocked`; C section 10 plus T-ISO-1. C's own tamper rule contradicts it (see IC).
- SC-4 (test plan names the ten case families): A section 12 groups; B section 12 AC rows; C section 12 T-* ids. All name levels, approval, isolation, subagents, nested subagents, missing or unreadable state, tamper, rename, re-claim, wrappers and speed.
- SC-5 (residual risks and owner decisions): section 2 and section 15 in each variant.
- Known weak matches that I did not subtract: C on AC-5 (fails open when `jq` is missing, settings edit not blocked) and AC-6 (`git push origin HEAD` from `master` and `--all` pass at full with submit).

**IC.** Claims sampled = decision table rows + Bash rules + fail-closed and speed rows + test cases or groups + binding and approval rules.
- A, 56 claims = 20 table rows + 7 section 8 steps + 10 section 10 rows + 9 section 12 groups + 5 section 4 binding steps + 5 section 6 rules. 1 contradiction: section 10 fast path 1 ("if `sessions/` and `pending/` are empty, exit 0") fires before the section 4 step 4 rule that a marked prompt with no record still creates a degraded session. The two cannot both hold unless fast path 1 is scoped to PreToolUse, which the text does not say.
- B, 49 claims = 16 table rows + 9 section 8 items + 7 section 10 rows + 8 section 12 AC rows + 5 section 6 rules + 4 section 4 binding rules. 1 contradiction: section 10 fast path keys on "No `sessions/` files at all" and exits 0 without `jq`, so the first launch on a machine (no session file yet, only a pending file) never reaches the section 4 bind step. Section 10's speed paragraph says "no governed files", which is looser, so this one is the weaker of the three counted.
- C, 56 claims = 16 table rows + 8 section 8 steps + 8 section 10 items + 12 section 12 case families + 4 section 6 rules + 5 section 4 rules + 3 section 7 rules. 3 contradictions: X-005 (tamper rule "in every session" against "ordinary sessions never blocked" and T-ISO-1), X-007 ("No level allows a push to master or main" against `git push origin HEAD` allowed at full with submit and no check of `--all` or the current branch), and X-006 (section 2 says settings edits "reduce to the script-file residual" but no rule blocks an Edit of `~/.claude/settings.json`). X-004 is also a flaw in C but I charged it as a factual error (K1, E5), not here.

**SR.** Counted over the section 5 decision table (with its trailing paragraph), section 8, section 10 and section 12.
- A: section 5 = 22 concrete (20 rows + 2 precedence sentences); section 8 = 11 concrete; section 10 = 13 concrete, 1 vague ("with a CI margin"); section 12 = 13 concrete. Row "MCP tool ... BLOCK (class id)" does not name the id, counted vague. Total 59 concrete, 2 vague.
- B: section 5 = 18 concrete; section 8 = 14 concrete; section 10 = 11 concrete, 2 vague ("a few milliseconds", "three times the budget" where the budget is unquantified); section 12 = 14 concrete. Total 57 concrete, 2 vague.
- C: section 5 = 18 concrete; section 8 = 10 concrete; section 10 = 12 concrete; section 12 = 12 concrete, 1 vague ("exit 0 ... except where section 10 says closed"). Total 52 concrete, 1 vague.

**DC.** Internal references = section references, message ids, test ids, U, N, O, R and OB ids. References to the research file (V1 to V14), the seed brief (A2, A10, A12, D1 to D7) and WORKER-CONTRACT are external and excluded.
- A, 98 references = 13 message ids + 18 section refs + 12 test-group refs + 25 U ids + 13 OB ids + 5 O ids + 12 R ids. 1 unresolved: "BLOCK (class id)" on the MCP row. The R1 to R8 residual ids are reused as claim interface R1 to R3 (sections 4 and 14); I treated those as resolved by context and charged the clash under K3.
- B, 98 references = 20 message ids + 30 section refs + 13 U ids + 7 N ids + 24 OB ids + 3 O ids + 1 C-id range. 0 unresolved (the T1 clash is charged under K3).
- C, 112 references = 22 message ids + 25 section refs + 40 test ids + 3 O ids + 12 U ids + 2 R ids + 8 OB ids. 4 unresolved: `T-WR-gh-repo` (section 15 O-1) is not in section 12; section 16 U2 points to "T-MSG cases" but T-MSG-1..8 only check message text; section 16 U4 points to `T-A-4`, which is the post-approval commit case, not a `!cmd` case; section 16 U6 points to `T-WR-escape`, which is not a distinct id.

**SC.** `grep -c '^## '` gives 16 for each variant. Maximum is 16, so each scores 1.000.

## 2. Qualitative layer (Claim-Evidence-Verdict)

Each cell is `verdict: evidence`. MET needs a quote or section reference; otherwise NOT MET.

| # | Criterion | A: Variant 1 | B: Variant 2 | C: Variant 3 |
|---|---|---|---|---|
| C1 | Covers all explicit requirements | MET: section 13 maps AC-1 to AC-8 to sections and test groups | MET: sections 12 and 13 map every AC to named cases | MET: section 13 maps AC-1 to AC-8 to T-* test ids |
| C2 | Edge cases and failure scenarios | MET: section 10 failure table, degraded binding for missing or stale record | MET: section 10 table covers jq missing, bad JSON, unreadable state, timeout | MET: section 10 table, T-FO fail-open cases, T-SUB-4 no match |
| C3 | Dependencies and prerequisites | MET: section 3 files, claim interface R1/R2/R3, section 14 step 7 handoff | MET: C1 to C3 claim interface, claim script refuses launch without jq | MET: section 3 interface R1 to R4 owed by claim feature, install list |
| C4 | Success or completion criteria | MET: section 14 step 8, full and submit stay off real issues until OB-H3 | MET: section 14 step 5, OB-H2 and OB-H3 pass before any real full launch | MET: section 16 closing line makes OB-H2 mandatory; section 13 AC map |
| C5 | Explicit out of scope | MET: section 2 T3 out of scope; O-1 leaves source edits to #322 | MET: section 1 item 6 Cut list; T3 not designed against | MET: section 2 Not covered list; section 3 claim interface is requests only |
| K1 | No factual errors or hallucinated claims | NOT MET: section 3 says Makefile holds `_FRESHNESS_SCRIPTS`; it lives only in install_hooks.py | MET: `_FRESHNESS_SCRIPTS` and `hooks.json` alternation matcher both match the repository | NOT MET: wrong Makefile claim, unregistered `manual` marker, V4 and V11 misapplied (X-004, X-006) |
| K2 | Feasible within constraints | MET: bash builtins fast paths, ERR/EXIT traps, one subprocess only for governed pushes | MET: one jq call, string replacement, git call bounded by 1 s timeout | NOT MET: always-on cwd fallback and tamper block in every session break the ordinary-session constraint |
| K3 | Terminology consistent and accurate | NOT MET: R1 to R8 residual ids reused as claim interface R1, R2 (section 14) | NOT MET: T1 names both the honest-agent threat and the tamper message | MET: W, WA, F, FS and MSG-* ids used consistently; MSG-STATE reuse minor |
| K4 | No internal contradictions | NOT MET: fast path 1 (empty store) exits before degraded binding of a marked prompt | NOT MET: fast path tests only `sessions/`, so first launch never reaches binding | NOT MET: X-005 tamper block everywhere, X-007 push HEAD from master allowed |
| K5 | Claims supported by evidence or rationale | MET: every decision has a Why or Rejected line with V-tagged facts | MET: each position states rationale and rejects options, e.g. section 8 awk cost | NOT MET: fail-open rests on V8 and the fallback safety on V4; neither says that |
| T1 | Logical section ordering | MET: 16 sections run position, threats, identity, table, approval, tests, order | MET: same 16-section order, decisions D1 to D7 in seed order | MET: same order; section 14 builds a provably harmless skeleton first |
| T2 | Consistent hierarchy | MET: H1 title, 16 H2 sections, bold sub-labels used uniformly | MET: 16 H2 sections used uniformly, though no H1 title | MET: H1 plus 16 H2 sections; section 12 uses prose per AC |
| T3 | Clear separation of concerns | MET: ll_classify_shell, ll_decide, ll_message separate classify, policy, wording | MET: one section per decision; messages and tests in their own sections | MET: table, approval, Bash, tools, fail-closed, messages in separate sections |
| T4 | Navigation aids | MET: section 13 AC map, LL-* ids, U/OB/O/R ids, decision grid | MET: section 13 map, message ids W1 to F3, OB-H and N ids | MET: section 13 map, T-* and MSG-* ids; T-WR-gh-repo dangling |
| T5 | Design spec conventions | MET: summary, threat model, components, interfaces, tests, open decisions | MET: same elements; position summary stands in for an overview | MET: same elements with title and persona line |
| L1 | Unambiguous language | MET: closed class list and ordered message precedence leave little room | MET: exact regex `\[sc-launch:v1:([0-9a-f]{32})\]` and token rules in sections 4, 8 | NOT MET: "never blocked" (section 1) against "blocked in every session" (section 4) |
| L2 | Concrete rather than abstract | MET: literal word lists, delimiters, millisecond budgets in sections 8 and 10 | MET: regexes, token lists, timeouts in section 8 | MET: literal JSON payload per case in section 12 |
| L3 | Each section has a clear purpose | MET: headings name the decision, e.g. "Session identity (D1)" | MET: headings name the decision, e.g. "Bash and git wrappers (D4)" | MET: headings name the decision, e.g. "Fail-closed rules and speed (D6)" |
| L4 | Terms defined on first use | MET: "governed" defined in section 1, T1 to T3 in section 2, classes in section 3 | NOT MET: "governed" used in section 4, defined only in section 10 | MET: W, WA, F, FS defined at section 5 top; "bound" defined in section 4 |
| L5 | Actionable next steps or decisions | MET: section 14 eight ordered steps; section 15 nine decisions with recommendations | MET: section 14 five steps; section 15 seven decisions with defaults | MET: section 14 six steps; section 15 six decisions with defaults |
| R1 | At least 3 risks with probability and impact | NOT MET: R1 to R8 have reasons, no probability or impact rating | NOT MET: ten cuts listed; only "likeliest workaround" hints at probability | NOT MET: six residual bullets, no probability or impact rating |
| R2 | Mitigation for each risk | MET: each R row has "Why accepted"; section 16 gives a tolerance per unknown | MET: cut table states what stays open; section 16 tolerance per item | MET: each bullet gives its reason; section 16 tolerance per unknown |
| R3 | Failure modes and recovery | MET: section 10 table; LL-BROKEN and LL-TAMPER name a release step | MET: F1 to F3 messages say release as in T1, or claim again | MET: section 10 table; release by `rm` of the active file (R4) |
| R4 | External dependency failure scenarios | MET: jq missing, symbolic-ref timeout, hook timeout, missing record (section 10) | MET: jq missing, invalid JSON, 1 s git timeout, hook timeout (section 10) | MET: jq missing row; U8 harness failure voids binding (section 16) |
| R5 | Monitoring or validation mechanism | MET: OB-H1 to OB-H3 observed checks, LL-STATE note on degraded state | MET: OB-H1 to OB-H5 including live wording check and real-machine timing | MET: OB-H1 to OB-H3 plus T-FO and T-SPD regression guards |
| E1 | Collection boundaries | MET: empty store fast path, other-sessions speed test, missing Monitor field | MET: no sessions at all, empty state file, 100 KB command test | MET: empty `tool_input` and unknown tool cases, 256 KB stdin cap |
| E2 | State-variable interactions across components | MET: approval kept in a separate file; degraded session still accepts approval | MET: `.ok` written only at worktree level; prompts with `agent_id` ignored | MET: approval lives in active JSON; invalid file resets `approved` to false |
| E3 | Guard-condition gaps | MET: bare push on main, detached HEAD, symbolic-ref failure all LL-PROTECTED | MET: symbolic-ref printing master, main or nothing, plus `--all` and `--mirror` | NOT MET: `git push origin HEAD` and `--all` pass at full with submit (X-007) |
| E4 | Count divergence | MET: stale record "over 30 minutes"; nonce binds at most one session | MET: nonce regex `{32}`, single-use `mv`, 100 KB command speed test | NOT MET: four-word lookahead and 256 KB cap have no overflow behaviour or test |
| E5 | Interaction effects when features combine | MET: several-class precedence order; wrapper plus protected push in tests | MET: `test_wrappers_at_every_level`; `\/` token form; store name split in source | NOT MET: cwd fallback meets a human's own subagent and misgoverns it (X-004) |

## 3. Dimension subtotals and qual_score

| Dimension | Items | A: Variant 1 | B: Variant 2 | C: Variant 3 |
|---|---|---|---|---|
| Completeness C1 to C5 | 5 | 5 | 5 | 5 |
| Correctness K1 to K5 | 5 | 2 | 3 | 1 |
| Structure T1 to T5 | 5 | 5 | 5 | 5 |
| Clarity L1 to L5 | 5 | 5 | 4 | 4 |
| Risk coverage R1 to R5 | 5 | 4 | 4 | 4 |
| Invariant and edge cases E1 to E5 | 5 | 5 | 5 | 2 |
| **Criteria met** | 30 | **26** | **26** | **21** |
| **qual_score** | | **0.867** | **0.867** | **0.700** |

## 4. Edge-case floor

Rule: a variant scoring under 1 of 5 on E1 to E5 is ineligible as base.
- A: 5 of 5. Eligible.
- B: 5 of 5. Eligible.
- C: 2 of 5 (E1 and E2 met; E3, E4, E5 not met). Passes the floor as written, but with the weakest edge-case result: its three misses are state-mechanics defects (push from `master` via `HEAD`, fallback governing a human's subagents, unbounded lookahead).

## 5. Combined score

combined = 0.5 * quant_score + 0.5 * qual_score.

| Variant | quant_score | qual_score | Combined |
|---|---|---|---|
| A: Variant 1 (architect) | 0.9891 | 0.8667 | **0.9279** |
| B: Variant 2 (refactorer) | 0.9898 | 0.8667 | **0.9282** |
| C: Variant 3 (QA) | 0.9784 | 0.7000 | **0.8392** |

Notes for the reader of this pass:
- The quantitative layer barely separates the variants (0.978 to 0.990) because all three share one skeleton and match all 13 requirements. The qualitative layer carries the spread.
- A and B are within 0.0003 of each other. A leads on defensive state handling (marker always governs, remote and repo checks, MCP coverage, trap-to-exit-2); B leads on repository accuracy (K1) and the smallest claim interface. Their one-line contradictions (fast path against binding) are both fixable by scoping the fast path to PreToolUse or checking `pending/` too.
- C trails mainly on correctness (K1, K2, K5) and edge cases (E3 to E5), all traceable to X-002, X-004, X-005, X-006 and X-007 in `diff-analysis.md`.
- R1 is NOT MET for all three: none rates a risk by probability and impact.
