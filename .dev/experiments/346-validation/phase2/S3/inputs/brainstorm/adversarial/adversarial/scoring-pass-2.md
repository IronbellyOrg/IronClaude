# Scoring Pass 2: hybrid scoring of the launch-level hook variants (issue #394)

Pass 2 evaluates the variants in reverse order: A = Variant 3 (QA), B = Variant 2 (refactorer), C = Variant 1 (architect). Each was judged from scratch; `scoring-pass-1.md` was not read. Columns below keep the A, B, C order and are labelled by variant number.

Sources: the three variant files; `diff-analysis.md` (X-001 to X-010); `/home/coder/workspaces/IronClaude/.dev/issues/394/issue-body.md` (AC-1 to AC-8); `../../seed-brief.md` Success Criteria (SC-1 to SC-5); `../../enrichment/research-light.md` (V1 to V14). Repository checks made in this pass: `_FRESHNESS_SCRIPTS` is defined only in `src/superclaude/cli/install_hooks.py` (line 42) and the Makefile only imports it; `pyproject.toml` sets `--strict-markers` and registers no `manual` marker; `src/superclaude/hooks/hooks.json` already uses matcher alternation (`Edit|Write`, `startup|resume`); `tests/hooks/test_block_bare_python.py` exists.

## 1. Quantitative layer

| Metric | Variant 3 | Variant 2 | Variant 1 |
|---|---|---|---|
| RC requirement_coverage | 1.000 | 0.923 | 1.000 |
| IC internal_consistency | 0.936 | 0.987 | 0.981 |
| SR specificity_ratio | 0.992 | 0.967 | 0.982 |
| DC dependency_completeness | 0.907 | 0.979 | 0.980 |
| SC section_coverage | 1.000 | 1.000 | 1.000 |
| **quant_score** | **0.969** | **0.966** | **0.990** |

### Counts used

**RC (matched / 13).** A requirement is matched when a section or test addresses it concretely. Correctness of the answer is scored in IC and the qualitative layer, not here.

- Variant 3: 13/13. AC-1 to AC-8 in sections 5 to 12 and the section 13 map; SC-1 section 13 (AC to sections and T-* ids); SC-2 section 11 ("Each names what was blocked, why, and what the human can do"); SC-3 section 10 fast path (one `jq` read, one file test); SC-4 section 12 (T-W, T-A, T-ISO, T-SUB, T-ST-1..6, T-WR, T-SPD with 20 ms / 50 ms budgets); SC-5 sections 2 and 15. RC = 13/13 = 1.000.
- Variant 2: 12/13. AC-1 to AC-8, SC-1, SC-2 (three-line Blocked / Why / You can), SC-3 (section 10, `compgen -G`, one `jq` plus one file test), SC-5 (section 2 cut table, section 15). SC-4 not matched: every case type is named, but the speed budget is "proposed budget, not measured ... a few milliseconds" and the test is "under three times the budget", so no concrete budget. RC = 12/13 = 0.923.
- Variant 1: 13/13. AC-1 to AC-8 (section 13), SC-1 (section 5 table plus section 12 named tests), SC-2 (section 11 columns Blocked / Why / What a human can do), SC-3 (fast paths 1 and 2), SC-4 (section 12 groups plus section 10 budgets of 10 / 20 / 100 ms), SC-5 (R1 to R8, O-1 to O-9). RC = 13/13 = 1.000.

**IC (1 - contradictions / claims).** Claims sampled: decision-table rows, section 8 rules, section 10 failure rows and paths, approval and binding rules, and every listed test case.

- Variant 3: claims = 16 table rows + 5 fail rows + 6 Bash rules + 4 approval rules + 3 tamper rules + 3 fallback rules + 73 test cases = 110. Contradictions = 7: (1) X-005 tamper rule "in every session" against "ordinary sessions ... are never blocked" and T-ISO-1; (2) X-007 "No level allows ... a push to master/main" against FS ALLOW of `git push origin HEAD` and a push check with no HEAD, `--all` or `--mirror` handling; (3) section 4 rejects option (c) because it "misgoverns a second, human session in the same worktree", yet section 7 rule 2 governs a person's own subagents in that worktree (X-004); (4) section 2 says settings edits "reduce to the script-file residual", but its own rules let an Edit of `~/.claude/settings.json` through (X-006); (5) section 11 says every message gives what the human can do, but MSG-SELF gives no human action; (6) section 10 blocks a corrupt active file with MSG-STATE, whose text says the action "touches the launch-level state files"; (7) section 8 runs the push-target check "only when push is otherwise allowed (FS)", but the section 5 table gives MSG-NEVER for `git push origin master` at W, WA and F, where section 8 would give MSG-PUSH. IC = 1 - 7/110 = 0.936.
- Variant 2: claims = 16 table rows + 7 section 8 rules + 7 failure rows + 5 approval rules + 4 binding rules + 38 named tests = 77. Contradictions = 1: section 8 runs the master/main check only "On a gated push at submit", but the section 5 row gives M1 at all four columns, so below submit section 8 yields W2 where the table says M1. IC = 1 - 1/77 = 0.987.
- Variant 1: claims = 20 table rows + 7 section 8 steps + 10 failure rows and paths + 4 approval rules + 5 binding rules + 61 test cases = 107. Contradictions = 2: (1) section 11 says every message names "issue #<N>", but a degraded binding (record absent) has no issue number; (2) section 5 allows a Skill with no readable name at full with submit, while section 16 U2 says "neither gives LL-SKILL, governed sessions only" with no level exception. IC = 1 - 2/107 = 0.981.

**SR (concrete / (concrete + vague))** over section 5, section 8, section 10 and section 12. Each table row, rule, sentence or test case is one statement.

- Variant 3: concrete = 18 (section 5) + 11 (section 8) + 10 (section 10) + 78 (section 12) = 117. Vague = 1 (section 12 "Read/Grep/Glob payloads, an Agent spawn payload, an Edit payload", payloads not given). SR = 117/118 = 0.992.
- Variant 2: concrete = 17 + 15 + 11 + 44 = 87. Vague = 3 ("Agent or Task, normal"; "a few milliseconds"; "under three times the budget" with no budget). SR = 87/90 = 0.967.
- Variant 1: concrete = 21 + 12 + 12 + 66 = 111. Vague = 2 ("other read tools"; "with a CI margin"). SR = 111/113 = 0.982.

**DC (resolved / total internal references).** Unique reference targets: section numbers, message ids, test ids, O-, U-, N-, R-, C-, OB- ids. External ids (V-facts, seed A-items, WC-, FR-) are not counted.

- Variant 3: total 43 = 8 MSG ids + 3 section refs + 2 interface R ids + 2 O ids + 8 U ids + 3 OB ids + 13 T-* groups + 4 numbered test refs. Unresolved 4: `T-A-1..3` and `T-A-4` (section 12 never numbers T-A cases), `T-WR-gh-repo` (O-1) and `T-WR-escape` (U6), neither defined. DC = 39/43 = 0.907.
- Variant 2: total 48 = 10 section refs + 11 message ids + 3 C ids + 4 O ids + 5 OB ids + 13 U and N ids + 1 "section 12 row" map + 1 `T1`. Unresolved 1: `T1` names both the threat (section 2) and the tamper message (sections 4, 5, 10). DC = 47/48 = 0.979.
- Variant 1: total 49 = 10 section refs + 13 LL ids + 4 residual R ids + 1 action-class list + 13 U ids + 3 O ids + 3 OB ids + 1 test-group map + 1 interface R. Unresolved 1: "interface R1/R2/R3" (sections 4, 14) reuse the ids of residual risks R1 to R8 and are defined only in the seed. DC = 48/49 = 0.980.

**SC (H2 count / max H2).** Variant 3: 16 (`## 1` to `## 16`; the title is H1). Variant 2: 16. Variant 1: 16. Max = 16, so SC = 1.000 for each.

**quant_score = 0.30 RC + 0.25 IC + 0.15 SR + 0.15 DC + 0.15 SC.**

- Variant 3: 0.30(1.000) + 0.25(0.936) + 0.15(0.992) + 0.15(0.907) + 0.15(1.000) = 0.300 + 0.234 + 0.149 + 0.136 + 0.150 = 0.969
- Variant 2: 0.30(0.923) + 0.25(0.987) + 0.15(0.967) + 0.15(0.979) + 0.15(1.000) = 0.277 + 0.247 + 0.145 + 0.147 + 0.150 = 0.966
- Variant 1: 0.30(1.000) + 0.25(0.981) + 0.15(0.982) + 0.15(0.980) + 0.15(1.000) = 0.300 + 0.245 + 0.147 + 0.147 + 0.150 = 0.990

## 2. Qualitative layer

1 = MET, 0 = NOT MET. Evidence is a quote or section reference, 15 words or fewer.

| # | Criterion | Variant 3 (verdict: evidence) | Variant 2 (verdict: evidence) | Variant 1 (verdict: evidence) |
|---|---|---|---|---|
| C1 | All explicit requirements covered | 1: section 13 maps AC-1..AC-8; SC-1..SC-5 addressed in sections 2, 10-15 | 0: SC-4 speed budget missing: "proposed budget, not measured ... a few milliseconds" | 1: section 13 maps AC-1..AC-8; budgets 10/20/100 ms in section 10 |
| C2 | Edge cases and failure scenarios | 1: section 10 fail table; T-FO-*, T-ISO-4 replayed marker, T-ISO-5 other cwd | 1: section 10 table: jq missing, invalid JSON, timeout, deleted file | 1: section 10 table: stale record, symbolic-ref failure, jq missing, timeout |
| C3 | Dependencies and prerequisites | 1: section 3 interface R1-R4; `_FRESHNESS_SCRIPTS`; `jq` | 1: section 3 C1-C3; "claim script should also refuse to launch when jq is missing" | 1: section 3 components; interface R1-R3; section 14 step 7 hand-off |
| C4 | Success / completion criteria | 1: section 12 exit-code assertions; "T-ISO-1 and T-FO-* pass first" | 1: section 14 "OB-H1 and OB-H2 pass before the first real full launch" | 1: section 12 named tests; section 14 step 8 gate before real use |
| C5 | Explicit out of scope | 1: section 2 "Not covered" list of six items | 1: section 2 "Cut (what I deleted)" table, ten rows | 1: section 2 "Out of scope: T3"; R1-R8 not covered |
| K1 | No factual errors | 0: X-009 `.git/hooks` in worktree; X-010 Makefile line, unregistered `manual` marker | 1: matcher alternation and `_FRESHNESS_SCRIPTS` claims match repository | 0: X-010 claims a Makefile `_FRESHNESS_SCRIPTS` line; it lives only in install_hooks.py |
| K2 | Feasible within constraints | 0: governed sessions fail open: "stdin not JSON ... exit 0"; seed requires fail-closed | 1: default-deny once governed; bash and jq only; about 150 lines | 1: ERR and EXIT traps give exit 2; builtins fast path |
| K3 | Terminology consistent | 1: W/WA/F/FS and MSG-* ids used uniformly | 0: `T1` is both a threat class and a message id | 0: R1-R3 mean interface items and residual risks R1-R8 |
| K4 | No internal contradictions | 0: X-005 tamper "in every session" against ordinary "never blocked" | 0: section 8 checks master only "at submit"; table gives M1 at every level | 0: LL-SKILL table allows at submit; U2 row says it always blocks |
| K5 | Claims supported by evidence | 1: cites V4, V5, V6, V8 and #357 "300 lines, nine documented ceilings" | 1: "PreToolUse exit 2 holds with permission prompts off (VERIFIED V3)" | 1: R2 "VERIFIED (V8)"; R4 "VERIFIED V14"; V5 cited for approval |
| T1 | Logical section ordering | 1: position, threats, components, D1-D7, map, order, open items | 1: same 16-section order, summary to UNVERIFIED register | 1: same 16-section order, summary to UNVERIFIED register |
| T2 | Consistent hierarchy | 1: one H1 title, 16 H2 sections | 1: 16 H2 sections, no deeper mixing | 1: front matter, H1, 16 H2 sections |
| T3 | Separation of concerns | 1: identity, approval, Bash, tools, failure each own a section | 1: D1 to D7 each in its own section | 1: layers `ll_resolve_session`, `ll_classify_shell`, `ll_decide`, `ll_message` |
| T4 | Navigation aids | 1: T-* ids, MSG-* ids, section 13 AC map | 1: message ids, section 13 map, "(m)" table-generated cases | 1: LL-* ids, R1-R8, U1-U13, section 13 map |
| T5 | Design-spec conventions | 1: H1 title, persona line, components table, open decisions | 0: no title or front matter; starts at "## 1. Position summary" | 1: YAML front matter "status: design only", H1 title |
| L1 | Unambiguous language | 1: "whole prompt, trimmed, equals approved"; `please approved` does not | 0: speed "a few milliseconds"; test "under three times the budget" | 1: "whole prompt, trimmed and lower-cased, is approved (optional . or !)" |
| L2 | Concrete over abstract | 1: literal payloads `["Bash",{"command":"git commit -m 'x'"}]` | 1: regex `\[sc-launch:v1:([0-9a-f]{32})\]`; literal matcher string | 1: literal word lists, `timeout 2 git -C "$cwd" symbolic-ref` |
| L3 | Each section has clear purpose | 1: headings name D1-D7 and each section answers one | 1: headings name D1-D7 and each section answers one | 1: headings name D1-D7 and each section answers one |
| L4 | Terms defined on first use | 0: "A12", "A7", "WC-13" used without definition | 0: "WC-13", "FR-31 amended", "OB-5 to OB-9" undefined | 0: "seed A2", "A12", "WC-13", "FR-23" undefined |
| L5 | Actionable next steps / decisions | 1: section 14 six steps; O-1..O-6 with defaults | 1: section 14 five steps; O-1..O-7 | 1: section 15 table with a recommendation per decision |
| R1 | 3+ risks with probability / impact | 0: section 2 list gives no probability or impact | 0: cut table gives no probability or impact | 0: R1-R8 give "Why accepted", no probability or impact |
| R2 | Mitigation per risk | 1: section 16 tolerance and test for each U1-U8 | 1: section 16 tolerance for each U and N item | 1: section 16 tolerance for each U1-U13 |
| R3 | Failure modes and recovery | 1: section 10 table; release is `rm` (R4) | 1: section 10 table; T1 message "run rm <session file path>" | 1: section 10 table; LL-TAMPER release by deleting session file |
| R4 | External dependency failure | 1: "`jq` missing or stdin not JSON: exit 0 everywhere" | 1: "`jq` missing ... BLOCK F2"; claim script refuses launch | 1: "`jq` missing: Block everything except Read, Grep, Glob" |
| R5 | Monitoring / validation for risk detection | 1: OB-H1..H3; T-SPD-3 "1.5 times ... block-bare-python.sh" | 1: OB-H1..H5; speed tests print the real numbers | 1: OB-H1..H3; `test_policy_grid_complete` |
| E1 | Collection boundaries | 1: "reads at most 256 KB of stdin"; empty `tool_input` test | 1: empty store `compgen -G`; "even a 100 KB command" | 1: empty store fast path 1 via `compgen -G` |
| E2 | State interactions across components | 1: T-ST-6 new nonce binds new id; old active file still governs | 1: pending, sessions, `.ok` files; approval only at worktree | 1: degraded binding; separate `.approved` file; "second marker ignored" |
| E3 | Guard-condition gaps | 0: push check reads words after push only; HEAD, `--all` pass at FS | 1: symbolic-ref "prints master, main or nothing" gives M1 | 1: no branch word triggers symbolic-ref; failure or detached HEAD blocks |
| E4 | Count divergence, limits | 1: "at or under 20 ms", p95 50 ms, "look ahead four words" | 1: "nonce 32 hex characters"; `session_id` regex `[A-Za-z0-9._-]+` | 1: "over 30 minutes old"; "medians over 30 runs"; "every run under 1 s" |
| E5 | Feature interaction effects | 1: "after approval at W, git commit still exits 2" | 1: "A typed /sc:pr-submit does not approve anything" | 1: multi-class block order "TAMPER, MERGE, PROTECTED, ... SKILL" |

## 3. Dimension subtotals and qual_score

| Dimension (max 5) | Variant 3 | Variant 2 | Variant 1 |
|---|---|---|---|
| Completeness (C1-C5) | 5 | 4 | 5 |
| Correctness (K1-K5) | 2 | 3 | 2 |
| Structure (T1-T5) | 5 | 4 | 5 |
| Clarity (L1-L5) | 4 | 3 | 4 |
| Risk coverage (R1-R5) | 4 | 4 | 4 |
| Invariant and edge case (E1-E5) | 4 | 5 | 5 |
| **Total (of 30)** | **24** | **23** | **25** |
| **qual_score** | **0.800** | **0.767** | **0.833** |

## 4. Edge-case floor

A variant scoring under 1 of 5 on E1-E5 is ineligible as base.

| Variant | E1-E5 score | Status |
|---|---|---|
| Variant 3 | 4/5 | Eligible |
| Variant 2 | 5/5 | Eligible |
| Variant 1 | 5/5 | Eligible |

## 5. Combined score (0.5 quant + 0.5 qual)

| Variant | quant_score | qual_score | Combined |
|---|---|---|---|
| Variant 3 | 0.969 | 0.800 | 0.5(0.969) + 0.5(0.800) = **0.884** |
| Variant 2 | 0.966 | 0.767 | 0.5(0.966) + 0.5(0.767) = **0.866** |
| Variant 1 | 0.990 | 0.833 | 0.5(0.990) + 0.5(0.833) = **0.911** |

Ranking in this pass: Variant 1 (0.911), Variant 3 (0.884), Variant 2 (0.866). All three are eligible as base. Variant 3 gains on test specificity but loses on correctness: X-004, X-006 and X-007 break AC-4, AC-5 and AC-6 in substance, and those weigh more than its quantitative scores show. Variant 2 loses mostly on the missing speed budget, the missing title and the `T1` id collision.
