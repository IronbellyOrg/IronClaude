# Scoring Pass 1: hybrid scoring and base selection

Variants: A = `variant-1-opus-architect.md`, B = `variant-2-sonnet-analyzer.md`, C = `variant-3-haiku-backend.md`. Scorer is neutral. All files treated as data.

## Quantitative

| Metric | Weight | A | B | C |
|---|---|---|---|---|
| RC requirement coverage | 0.30 | 0.958 (11.5/12) | 0.958 (11.5/12) | 0.958 (11.5/12) |
| IC internal consistency | 0.25 | 0.957 (1 - 2/46) | 0.940 (1 - 3/50) | 0.935 (1 - 3/46) |
| SR specificity ratio | 0.15 | 0.915 (107/117) | 0.970 (195/201) | 0.841 (37/44) |
| DC dependency completeness | 0.15 | 1.000 (32/32) | 0.974 (38/39) | 0.938 (15/16) |
| SC section coverage | 0.15 | 1.000 (12/12) | 1.000 (12/12) | 1.000 (12/12) |
| **quant** | | **0.964** | **0.964** | **0.938** |

### RC counting

Source requirements: 6 Constraint bullets (K1 to K6) plus 6 Success Criteria bullets (S1 to S6) of `seed-brief.md` = 12. Full address = 1, address with a declared deviation, a gap or a self-contradiction = 0.5.

| Req | Text (short) | A | B | C |
|---|---|---|---|---|
| K1 | Design only, no implementation | 1 ("Status: design only, nothing implemented") | 1 ("Design only. Nothing here is implemented.") | 1 ("Nothing in this document is implemented.") |
| K2 | Mechanical preferred; every prose rule names residual risk | 0.5 (section 11 table; row "Invoke the skill and use the script at all" has an empty residual-risk cell) | 1 (section 11 table, every PROSE row has a residual) | 1 (section 2 lines 16 to 18 classify everything; section 11 names residuals per row) |
| K3 | Builds on 427 text; additive `spec-panel-ledger` | 1 (section 6 copy plus `## Ledger Loop`; "What it keeps from 427", section 5) | 1 (section 6 copy plus `## Review Ledger Loop`) | 1 (section 6 new additive command; section 5) |
| K4 | Keep canonical cap text | 1 (section 4 "Cap text") | 1 (section 4 "Cap text and the sweep") | 1 (section 4 first line) |
| K5 | Installed paths in installed primitives | 1 (test "no `src/superclaude` inside the section") | 1 (dual lookup `~/.claude/skills/sc-review-ledger` first; test pins it) | 1 ("Never put source-tree paths in installed command instructions") |
| K6 | S1 measurement, same briefs and metrics, one-line substitution | 1 (section 9: name plus `--ledger` in three review briefs, no added session) | 0.5 (section 9 adds a sixth sweep dispatch, stated as a deviation) | 0.5 (section 9 claims one-line substitution, but X-018: coordinator must run mutations and a fourth reviewer session is added) |
| S1 | Parseable ledger format, location, per-actor transitions | 1 | 1 | 1 |
| S2 | Computed termination rule: PASS, FAIL-continue, ESCALATE | 1 | 1 | 1 |
| S3 | Difference from 427 `--re-review` | 1 | 1 | 1 |
| S4 | Adoption path reflect, rf-qa, implement final review | 1 | 1 | 1 |
| S5 | Stateful session vs file ledger recommendation | 1 | 1 | 1 |
| S6 | Predicted S1 R3 critical+major and growth, plus falsification | 1 (2.5, 18%, failure list) | 1 (P3 3.0, P3s 5.5, 23%, failure list) | 1 (1.5, 22.5%, fail conditions) |
| **Total** | | **11.5** | **11.5** | **11.5** |

### IC counting

Contradictions: diff-analysis intra-variant items plus ones found in this pass.

- A: X-020 (r2-coordinate spans compared with r3-coordinate hunks) + 1 found: section 8 says "About 4 extra script calls per review (section 11)" while section 11 says review 1 about +4 and reviews 2 and 3 about +5 each. Total 2.
- B: X-016 (FR-8/FR-9 blocking with no field to carry it), X-017 (`disputed` treated as a From state in T8 though it is not a status) + 1 found: T11 gives sweep rows status `open` and the U formula counts every blocking `open` row, so late rows enter both U and Lt. Total 3.
- C: X-018 (one-line brief change versus coordinator-run mutations and a fourth reviewer session), X-019 (random `run-id` default that no session can re-derive) + 1 found: section 3 line 106 "No automatic blocking deferral" versus line 115 "all final-sweep rows, even blockers, are deferred". Total 3.

Scorable claims (transition table rows + termination formula lines + CLI rows + rule-classification rows):

| Variant | Transition rows | Formula lines | CLI rows | Rule rows | Total |
|---|---|---|---|---|---|
| A | 10 | 6 (B(k), 4 decision branches, verdict line) | 9 (8 subcommands + exit-code list) | 21 | 46 |
| B | 11 (T1 to T11) | 10 (n, U, unmarked refusal, PASS, CONTINUE, ESCALATE, Lt, final, footer, last line) | 12 | 17 | 50 |
| C | 11 | 8 (B_r, X_r, I, 4 decision lines, S and delivery) | 10 (9 subcommands + exit-code line) | 17 | 46 |

### SR counting

Sample: first 40 substantive sentences per variant, 14 from section 2, 13 from section 4, 13 from section 11 (a table row counts as one sentence; code blocks, headers and table header rows skipped; minimum 25 characters). Concrete indicators: backticked tokens, numbers, file names, error or exit codes. Vague indicators: hedge words (about, roughly, may, might, could, should, likely, probably, some, typically, estimate, UNVERIFIED, plausible, often and similar). Counted mechanically.

| Variant | Section 2 (sent, conc, vague) | Section 4 | Section 11 | Concrete | Vague | SR |
|---|---|---|---|---|---|---|
| A | 14, 39, 0 | 13, 43, 1 | 13, 25, 9 | 107 | 10 | 0.915 |
| B | 14, 100, 0 | 13, 54, 0 | 13, 41, 6 | 195 | 6 | 0.970 |
| C | 14, 9, 0 | 13, 21, 0 | 13, 7, 7 | 37 | 7 | 0.841 |

### DC counting

Internal references: section references, row ids, error codes and defined symbols used elsewhere. Resolved = the target exists in the same variant and says what the reference claims. External references (other files, other themes, brief ids T05 to T09) excluded.

- A: 7 section refs (lines 48, 149 twice, 209, 237, 290, 333), all resolved; 20 codes (19 `E-*` defined in the section 6 exit-code list, `W-NO-ANSWERS` defined in context in section 2), all resolved; 1 "bullet 9" ref, resolved; 4 symbols (`B(k)`, `CAP_REVIEWS`, `PROFILES`, `dup_of`), resolved. 32/32.
- B: 15 section or open-question refs, all resolved; 14 T-id refs outside the table (T10 at line 51 used before its definition at line 66, still resolved), all resolved; 6 codes (`FROZEN_FIELD`, `LEDGER_TAMPERED`, `UNMARKED_ROWS`, `HUNKS_LARGE`, `UNCLAIMED`, `ILLEGAL`), resolved; 3 symbols (n, U, Lt), resolved; 1 status reference `disputed` in T8, unresolved (not a defined status). 38/39.
- C: 2 section refs (lines 18, 342), resolved; 3 id families (F001, C001, S001), resolved; 2 codes (`E_TRANSITION`, `E_IDEMPOTENCY`), resolved; 6 symbols (B_r, X_r, I, S, U3, W), resolved; `--op` and `--expect-seq`, resolved; "supporting context" (transition `verified -> verified`), never defined, unresolved. 15/16.

### SC counting

H2 count per variant (`grep '^## '`): A 12, B 12, C 12. Max 12. SC = 1.0 each.

### quant arithmetic

- A: 0.9583 x 0.30 + 0.9565 x 0.25 + 0.915 x 0.15 + 1.000 x 0.15 + 1.000 x 0.15 = 0.2875 + 0.2391 + 0.1373 + 0.1500 + 0.1500 = 0.964
- B: 0.9583 x 0.30 + 0.9400 x 0.25 + 0.970 x 0.15 + 0.974 x 0.15 + 1.000 x 0.15 = 0.2875 + 0.2350 + 0.1455 + 0.1462 + 0.1500 = 0.964
- C: 0.9583 x 0.30 + 0.9348 x 0.25 + 0.841 x 0.15 + 0.938 x 0.15 + 1.000 x 0.15 = 0.2875 + 0.2337 + 0.1262 + 0.1406 + 0.1500 = 0.938

## Qualitative

Citation check (Correctness 1). Repo files opened read-only in `bs346-ledger`:
- A: `spec-panel.md:256-264` (Review Loop, grading at 259, reviser at 263), `spec-panel.md:22` (usage line), `install_commands.py:11,40` (`_EXCLUDE_FILES = {"README.md"}`, `glob("*.md")`), `install_skill.py:52` (`copytree`), `test_review_severity_rule.py:215-219` (cap constants), `rf-qa.md:401` (monotonicity), `spec-panel-review-loop.md:143,154,162`, `test_routing_plugin_parity.py:41-47` (four mirrored commands), `test_cli_install.py:111-121,501-505`. All accurate.
- B: `install_skills.py:40-59` (sc- prefix strip and activation check), `test_worker_contract.py:831-839` (set equality on `## Unattended mode`), `spec-panel.md:451-461` (`## Unattended mode`), `pyproject.toml:85-87` (force-include `src`), `test_workflow_archive.py:22-28` (importlib load), `sc-reflect-protocol/SKILL.md:587` ("Non-negotiable final gate"), `test_cli_install.py:399-404`. All accurate.
- C: `install_skill.py:35-53` (copytree at 52), `spec-panel.md:261` (cap text), `test_review_severity_rule.py:215-219`, `qa.md:184-196` ("may raise a new blocker ... anywhere in task-owned text"), `qa.md:309-311` (fresh FINAL per archive attempt), `rf-qa.md:386-416`, `sc-reflect-protocol/SKILL.md:148-167`. All accurate.

Verified consequence used below: `tests/skills/test_worker_contract.py:20` sets `COMMANDS_DIR = src/superclaude/commands`, and `:831-839` asserts the set of command files with `## Unattended mode` equals `UNATTENDED_COMMANDS`. A's command is "Byte-identical to `spec-panel.md` except" three blocks, so it keeps `## Unattended mode` (`spec-panel.md:451`) and would fail that test unless `UNATTENDED_COMMANDS` is edited; A's file-by-file list names no such edit.

### Completeness

| Criterion | A verdict | A evidence | B verdict | B evidence | C verdict | C evidence |
|---|---|---|---|---|---|---|
| Covers all explicit requirements | MET | All 12 addressed (RC table) | MET | All 12 addressed, K6 with declared deviation (RC table) | MET | All 12 addressed, K6 self-contradicted (RC table) |
| Edge cases and failure scenarios | MET | Section 11 "Ways it could make the loop worse" 1 to 7; `deleted: true`; `W-NO-ANSWERS` (section 2) | MET | Section 11 risks 1 to 8; section 10 five-point self-attack | MET | Section 6 "Transaction, crash and rerun contract"; tombstones and `anchor_state` missing or ambiguous (section 3) |
| Dependencies and prerequisites | NOT MET | Lists install paths and `<skill base>` (section 6), but omits the `UNATTENDED_COMMANDS` edit its byte-identical copy requires (verified, see above) | MET | Install naming trap (`install_skills.py:40-59`); "No `UNATTENDED_COMMANDS` edit is needed because the variant omits `## Unattended mode`"; `uv` listed UNVERIFIED (q10) | MET | "A script must ship in the skill payload" (section 6); lookup order; Linux local filesystem lock (q9) |
| Success and completion criteria | MET | Test list (section 6 "Tests"); "What would mean the idea failed" (section 9); V1-ledger | MET | Bar (a) to (c) and five failure conditions (section 9) | MET | "Fail the idea for S1 if either bar, spread test or per-replicate ordering fails" (section 9); test list (section 6) |
| Explicit out of scope | MET | "Not changed" row (section 6); "No adopter is changed by this design" (section 7) | MET | "Edited files: none in the original loop"; "Two things the first version does NOT do" (section 7) | MET | "Skip a durable reviewer-session manager, database server" (section 8); "skip cross-run dedup services, signatures, auto-waivers" (section 11) |

Subtotals: A 4/5, B 5/5, C 5/5.

### Correctness

| Criterion | A verdict | A evidence | B verdict | B evidence | C verdict | C evidence |
|---|---|---|---|---|---|---|
| No factual errors or hallucinated claims | MET | 9 repo citations checked, all accurate (list above) | MET | 7 repo citations checked, all accurate | MET | 7 repo citations checked, all accurate |
| Feasible with stated constraints | MET | Runs on S1 with the one-line brief change and "Sessions: none added" (section 11); the missing test edit is scored under Completeness | NOT MET | Needs "ONE added dispatch after review 3", against the one-line substitution constraint (section 9) | NOT MET | "The coordinator alone runs ledger mutations" (section 2) and "four reviewer sessions including the sweep" (section 11) need a changed coordinator, against "Only authored brief change" (section 9), X-018 |
| Consistent terminology | MET | Five statuses `open, deferred, fixed, verified, reopened` used the same way in sections 3, 4, 9; `B(k)` defined once | NOT MET | `disputed` used as a From state in T8 though the statuses are open, deferred, fixed, verified, reopened (X-017) | NOT MET | "deferred" means both a note and a blocking sweep row; section 3 line 106 vs line 115 |
| No internal contradictions | NOT MET | X-020 | NOT MET | X-016, X-017, plus U and Lt double count via T11 | NOT MET | X-018, X-019, plus deferral wording conflict |
| Claims supported by evidence | MET | File:line on every evidence claim (section 1); prediction basis cites `ARMB-REPORT.md:13,14,31` (section 9) | MET | Alias citations with lines; traced F22 to N5 to N12 chain (section 1); line-by-line anchor check of ctl-r1 (section 5) | MET | Absolute experiment paths with lines (sections 1, 9); secondary claims flagged as "not independently re-read" (section 10) |

Subtotals: A 4/5, B 2/5, C 2/5.

### Structure

| Criterion | A verdict | A evidence | B verdict | B evidence | C verdict | C evidence |
|---|---|---|---|---|---|---|
| Logical ordering | MET | Sections 1 to 12 in brief order (S-001) | MET | Same order (S-001) | MET | Same order (S-001) |
| Consistent hierarchy | MET | H1 title, 12 H2, bold run-in heads | MET | H1, 12 H2, bold run-in heads | MET | H1, 12 H2, H3 subsections in sections 3 and 6 |
| Separation of concerns | MET | Kernel, contract, adapter table (section 2) | MET | "the script knows no spec-panel words" (section 7) | MET | "The only authoritative state is `ledger.json`. Reports and packets are disposable projections" (section 3) |
| Navigation aids or cross-references | MET | 7 internal section refs, for example "(section 9)", "(section 12)" | MET | Citation alias list up front; 15 internal refs | NOT MET | 2 internal refs in 387 lines; sections 4 and 9 use `X_r`, packets and sweep rules without pointing to their defining section |
| Follows design-spec conventions | MET | Status line, problem, mechanism, file changes, risks, open questions | MET | Same, plus UNVERIFIED marking | MET | Same, plus closing statement |

Subtotals: A 5/5, B 5/5, C 4/5.

### Clarity

| Criterion | A verdict | A evidence | B verdict | B evidence | C verdict | C evidence |
|---|---|---|---|---|---|---|
| Unambiguous language | MET | Exact `decision(k)` pseudocode and per-transition refusal codes (sections 3, 4) | MET | Decision table plus worked example on flg-r2 counts (section 4) | NOT MET | "supporting context" (section 3) and "unresolved sweep uncertainty" in S (section 4) are never pinned down |
| Concrete | MET | SR 0.915; named codes, paths, thresholds | MET | SR 0.970; byte counts, line numbers, arithmetic | MET | SR 0.841; closed field lists, exit codes, limits (section 6) |
| Each section one clear purpose | MET | Section 11 splits costs, risks and a rule table under separate heads | MET | Section 10 holds causes, bound and self-attack, all on "what it removes and leaves" | NOT MET | Section 11 table mixes rule classification with costs (S-012); MECHANICAL and PROSE labels repeated in every section |
| Terms defined on first use | MET | "Below, `L` is the ledger directory and `D` the document" (section 2); `B(k)` defined in the formula | MET | Aliases and `LEDGER`, `DOC`, `L` defined before use | NOT MET | "regression observation" used in section 2 before `X_r` defines it in section 4; "supporting context" never defined |
| Actionable next steps | MET | File-by-file table, test list, 8 open questions with options | MET | File table, experiment install steps, recommended answers in open questions | MET | File table, test list, open questions with preflight actions |

Subtotals: A 5/5, B 5/5, C 2/5.

### Risk coverage

| Criterion | A verdict | A evidence | B verdict | B evidence | C verdict | C evidence |
|---|---|---|---|---|---|---|
| At least 3 risks with probability and impact | NOT MET | Seven risks with impact, no probability on any | NOT MET | Impact stated; only risk 1 carries a rating ("Residual: MEDIUM") | NOT MET | Impact per row, no probability |
| Mitigation per risk | NOT MET | Risks 1 to 4 have "Mitigation"; risks 5, 6, 7 have none | NOT MET | Risks 4 and 7 have no mitigation | MET | Every section 11 row has an Enforcement column naming the control |
| Failure modes and recovery | MET | Atomic refusals, re-runnable `answer`, `E-TAMPERED` stop (sections 2, 3) | MET | Temp file plus `os.replace`; `revert-unclaimed`; `reseal` (sections 3, 6, 12) | MET | Crash before and after publication, resume rules (section 6) |
| External dependency failures | NOT MET | No statement on missing `uv`, missing skill folder or install failure | MET | "a host with neither copy fails at the first call, loudly" (section 11); `uv` UNVERIFIED (q10) | MET | "no inline fallback if helper is missing" (section 6); unsupported filesystems refused |
| Monitoring or validation mechanism | MET | V1-ledger check and refusal covariate (section 9) | MET | Baseline sweeps, hidden-defect share H, `minor_touched` (section 9) | MET | Record command, skill and script hashes; live D vs snapshot mismatch surfaced (section 9) |

Subtotals: A 2/5, B 3/5, C 4/5.

### Invariant and edge case coverage

| Criterion | A verdict | A evidence | B verdict | B evidence | C verdict | C evidence |
|---|---|---|---|---|---|---|
| Collection boundaries (empty, single, max) | MET | Review-1 PASS with zero blocking rows; anchor at least 12 characters; "an empty new-row list is always accepted" | MET | Row "1, 0, PASS, sweep"; `HUNKS_LARGE` above 40% | MET | 200 initial rows, 10 MiB, 4 KiB, 200 changed lines; "No diff means no new fixed states" |
| State interactions across components | MET | `E-REPORT-EDITED` ties the report tail to ledger decisions (section 2) | MET | T9 resets `verified` when a later hunk overlaps the claim span | MET | Packets bind round, document hash and ledger sequence (section 2) |
| Guard condition gaps | MET | "text added inside an attributed hunk is invisible to the check" (section 11) | MET | "a small quote inside a large hunk claims the whole hunk" (section 11) | MET | "detects unclaimed edits, not unrelated mechanisms hidden inside a claimed span" (section 3) |
| Count divergence (off-by-one, inclusive/exclusive) | NOT MET | No range convention; span vs hunk coordinate mismatch left open (X-020) | MET | Counter "incremented only by `open`"; `close` never CONTINUE at n = 3; worked count trace (section 4) | MET | "1-based half-open line ranges; zero-width ranges denote insertion/deletion boundaries" (section 6) |
| Interaction effects | MET | No-progress branch changes what R3 counts (sections 4, 12); moved paragraphs widen hunks (risk 6) | MET | Interaction defect N15 rejected unless `depends_on` (section 10 item 2) | MET | "Reviewer may omit the dependent sentence that proves a regression" (section 11) |

Subtotals: A 4/5, B 5/5, C 5/5. Edge-case floor (at least 1 of 5): all three eligible.

### Qualitative totals

| Dimension | A | B | C |
|---|---|---|---|
| Completeness | 4 | 5 | 5 |
| Correctness | 4 | 2 | 2 |
| Structure | 5 | 5 | 4 |
| Clarity | 5 | 5 | 2 |
| Risk coverage | 2 | 3 | 4 |
| Invariant and edge case | 4 | 5 | 5 |
| **Met / 30** | **24** | **25** | **22** |

## Scores

| Variant | quant | qual | combined = 0.5 x quant + 0.5 x qual | Base-eligible |
|---|---|---|---|---|
| A (`variant-1-opus-architect.md`) | 0.964 | 0.800 | 0.882 | yes |
| B (`variant-2-sonnet-analyzer.md`) | 0.964 | 0.833 | 0.899 | yes |
| C (`variant-3-haiku-backend.md`) | 0.938 | 0.733 | 0.836 | yes |

Pass 1 ranking: B (0.899), A (0.882), C (0.836). The A to B margin is 0.017, so a single qualitative verdict flip changes the order.
