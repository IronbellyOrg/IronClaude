# Qualitative scoring, pass 1 (input order A, B, C)

Rubric: `scoring-protocol.md` section A.2 (30 binary criteria, CEV protocol). MET = 1, NOT MET = 0, no partial credit; MET needs a quoted citation (variant:line).
Variants: A = `variant-1-opus-architect.md`, B = `variant-2-sonnet-analyzer.md`, C = `variant-3-haiku-backend.md`. Source requirements: `seed-brief.md`.
Ground truth checked read-only: `src/superclaude/commands/spec-panel.md` (486 lines; `## Review Loop` at line 256; line 220 cites `src/superclaude/examples/release-spec-template.md`), `tests/skills/test_spec_panel_review_loop.py` (pins only the two `spec-panel.md` copies), `tests/skills/test_worker_contract.py:831-839`, `src/superclaude/cli/install_skills.py:40-59`, phase4 `AB-REPORT.md` and `ARMB-REPORT.md`.

## Variant A

| Dimension | # | Criterion | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|---|---|
| Completeness | 1 | Covers all explicit requirements | Not met: the variant is an installed primitive that keeps a `src/superclaude/` citation, against the seed constraint "Installed primitives never cite `src/superclaude/` paths" | A:157 "with exactly these regions changed, and byte-identical elsewhere (pinned by test 5)"; the five regions (A:159-163) do not include Tool Coordination, and ground truth `spec-panel.md:220` reads "`src/superclaude/examples/release-spec-template.md`". A:249 checks only "no `src/superclaude` in the section". All other constraints are covered (7 bullets A:163, override A:50, escalate A:61, cap A:69) | NOT MET (0) |
| Completeness | 2 | Edge cases and failure scenarios | Met | A:347-355 section 7.2 "Ways the mechanism could make the loop worse" (under-fixing, cross-site inconsistency, gaming, false positives, missing reviewer line); A:105-110 exit-code table incl. "1 \| the checker crashed" | MET (1) |
| Completeness | 3 | Dependencies and prerequisites | Met | A:278 "That base has neither file and does not need them ... `uv run --no-project python` runs it with no project, no package and no dependency"; A:185 "stdlib only: `argparse`, `difflib`, `json`, `re`, `pathlib`, `sys`" | MET (1) |
| Completeness | 4 | Success/completion criteria | Met | A:322 "Seed-brief criteria: R3 proxy mean 3 or fewer with every replicate better than every control ... and growth 44.4% or less"; A:107 "exit 0 ... reviser stops" | MET (1) |
| Completeness | 5 | Explicit out of scope | Met | A:140 "`spec-panel.md`, its plugin copy, `HOW-WE-WORK.md`, `pragmatic.md` and the 427 pin tests are not touched"; A:256 "Later adopters (assessment, not part of this change)"; A:261 "That is a second unitiser, out of scope" | MET (1) |
| Correctness | 1 | No factual errors | Met (spot-checked claims match ground truth) | A:9 "6.0 / 5.5 / 3.5" and "63.5% ... 29.7% ... 30.0%" match ARMB-REPORT.md:20; A:151 "`install_skills.py:40-59` removes an `sc-<x>` skill when `commands/<x>.md` exists and does not activate it" matches `_has_corresponding_command`; A:162 `test_worker_contract.py:831-839` matches `_check_no_unattended_sections`; A:157 "486 lines" matches | MET (1) |
| Correctness | 2 | Feasible with stated constraints | Met: all steps run inside the review and revise workers, so only the command name changes in briefs | A:37 "The coordinator gets no new duty, so the S1 briefs change only by the command name"; A:286 "The revise briefs need no change: the reviser reads the report" | MET (1) |
| Correctness | 3 | Terminology consistent | Met | Classes `C`/`B`/`L` defined at A:50 and used identically in A:73-78 table, A:168 bullet 2 and A:189-191 `CLASSES`; "site" defined A:80 and used throughout | MET (1) |
| Correctness | 4 | No internal contradictions | Met: budget numbers have one source and limits, retries and exit codes agree across sections | A:183 "Budget numbers are deliberately not in the command: the checker prints them ... so the command cannot drift from the script"; A:62 "At most 3 checker runs after editing" agrees with A:180 bullet 6 retry sequence | MET (1) |
| Correctness | 5 | Claims supported by evidence/rationale | Met | A:82 "Calibration: 62-79% of 427-arm per-finding additions already fit 40 words (section 1)"; A:26 per-finding medians; A:29-31 traced chains with file:line | MET (1) |
| Structure | 1 | Logical ordering | Met | A:35 "## 2. Mechanism (each loop step, in order)" with 2.1 Review N, 2.2 Fix cycle, 2.3 Review N+1; problem (A:5) before mechanism before file changes (A:138) before measurement (A:292) | MET (1) |
| Structure | 2 | Consistent hierarchy | Met | `##` 1-8 with `###` 2.1-2.6, 4.1-4.5, 7.1-7.3; no orphan levels (A:39, A:52, A:155, A:334) | MET (1) |
| Structure | 3 | Separation of concerns | Met | A:121 "## 3. Causes removed and causes left" (effect) separate from A:138 "## 4. Exact changes" (files) and A:332 "## 7. Risks" | MET (1) |
| Structure | 4 | Navigation aids | Met (cross-references) | A:144-148 "(section 4.1)", "(section 4.3)", "(section 4.2)"; A:125 "(section 7, gaming)"; A:370 "Falsification criteria are fixed in section 6" | MET (1) |
| Structure | 5 | Artifact-type conventions | Met: follows the 8-heading design-proposal layout | A:5 "## 1. Problem and evidence" ... A:372 "## 8. Open questions", same headings as the requested proposal shape | MET (1) |
| Clarity | 1 | Unambiguous language | Met: search for "should consider", "might", "as appropriate", "should" found no hits; rules are stated as commands | A:61 "An escalated finding gets no edit and stays open. Escalate, never expand." | MET (1) |
| Clarity | 2 | Concrete | Met | A:45-48 literal `reviewed-copy:`, `fix-budget:`, `check:` lines; A:73-78 numeric class table | MET (1) |
| Clarity | 3 | Section purpose | Met | A:7 "**Problem in one sentence.**"; A:37 "Three parts, nothing else"; A:136 "Net claim: ..." | MET (1) |
| Clarity | 4 | Acronyms/terms defined on first use | Not met | A:151 "(D9; ...)", A:276 "(V6 as in D10)", A:298 "D5 M1-M5" and "FR-8/FR-9" (A:50) are used without definition | NOT MET (0) |
| Clarity | 5 | Actionable next steps | Met | A:271-273 literal install commands; A:353 "a dry run of the checker on one real cycle (flg-r2 cycle 2 ...) ... (planned, not done)"; A:324-330 pre-registered failure readings | MET (1) |
| Risk Coverage | 1 | >=3 risks with probability and impact | Not met: risks have impact but no per-risk probability; only two get qualitative wording | A:349 "This is the main trade"; A:350 "This is the likeliest way minfix raises a count"; risks 3-7 (A:351-355) carry no probability. Searched 7.1-7.3 | NOT MET (0) |
| Risk Coverage | 2 | Mitigation per risk | Met | A:349 "Mitigations: class `C` (3 sites), the rename rule, one `L` per report"; A:350 "Mitigation: narrow the rule instead of rewriting dependents"; A:352 "Escalation needs a reason naming the smallest fix found; M8 counts escalations" | MET (1) |
| Risk Coverage | 3 | Failure modes and recovery | Met | A:62 "restore each breaching finding's sites to `revert_to` ... this always reaches exit 0"; A:109 "reviser edits nothing further and reports; re-review records `fixcheck: input-error <message>` and continues without it" | MET (1) |
| Risk Coverage | 4 | External dependencies and failure | Met | A:180 "(if that script is absent, use the project `.claude/skills/fix-budget/scripts/fixcheck.py`)"; A:110 "the checker crashed (Python traceback) \| treated as exit 3"; A:151 package reinstall dependency rejected | MET (1) |
| Risk Coverage | 5 | Monitoring/validation for risk detection | Met | A:308 "V-M1 ... V-M2 ... V-M3 ... A replicate that fails one is 'variant not honoured' and is re-run"; A:302-306 M6-M10 | MET (1) |
| Invariant & Edge | 1 | Collection boundaries (empty, single, max) | Met | A:233 "no edits, valid report \| exit 0"; A:201 "missing file = no entries"; A:193 "MAX_L = 1" and A:242 "two `L` ... exit 3"; A:244 "S1-sized input (generated 1,500 units) \| finishes under 5 s" | MET (1) |
| Invariant & Edge | 2 | State interactions across components | Met | A:42 "427's coordinator copy for `--baseline` stays as it is; the two should be equal"; A:66 "This run is authoritative: it does not matter whether the reviser ran the checker" | MET (1) |
| Invariant & Edge | 3 | Guard condition gaps | Met | A:50 "The checker rejects (exit 3) an override line whose id is not `L`, an `L` without an override line, and a second `L`"; A:99 `ledger_errors` "old-not-in-baseline\|new-not-in-revised\|bad-json\|unknown-id\|add-without-reason" | MET (1) |
| Invariant & Edge | 4 | Count divergence (off-by-one, ranges) | Met | A:237 "`B` fix with 3 sites; same fix as a 3-site rename \| exit 2 / exit 0" (limit 2, A:76); A:11 "byte counts read as text, so they differ from `wc -c` by a few bytes"; A:209 "a site matched by k ids splits its words evenly" | MET (1) |
| Invariant & Edge | 5 | Interaction effects | Met | A:350 "Cross-site inconsistency ... review 2 flags it as an `origin=unchanged` finding that quotes the changed line"; A:379 "Composition with the other themes ... minfix plus stoprule" | MET (1) |

Subtotals A: Completeness 4/5, Correctness 5/5, Structure 5/5, Clarity 4/5, Risk Coverage 4/5, Invariant & Edge Case 5/5.
**Total A: 27/30; qual_score = 27/30 = 0.900.**

## Variant B

| Dimension | # | Criterion | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|---|---|
| Completeness | 1 | Covers all explicit requirements | Not met: the variant copy keeps the `src/superclaude/` citation of the original (constraint "Installed primitives never cite `src/superclaude/` paths"), and it adds an eighth Review Loop bullet against "keep its 7 bullets" | B:331 "M2 faithful copy: after removing the frontmatter, the command-name substitution, bullet 8 and the `## Fix Budget` section, the file equals `src/superclaude/commands/spec-panel.md` line for line" (ground truth line 220 cites `src/superclaude/examples/...`); B:256 "The line to append after bullet 7" | NOT MET (0) |
| Completeness | 2 | Edge cases and failure scenarios | Met | B:444-456 table of 11 failures (under-fixing, residue, gaming, false positives, skipped checker, forged receipt) | MET (1) |
| Completeness | 3 | Dependencies and prerequisites | Met | B:104-106 "Step 0 — one-time setup and availability ... stops with `E-FIXCHECK-MISSING`"; B:360 "stdlib only and run as `uv run --no-project python "<path>"`, which needs no `pyproject.toml`" | MET (1) |
| Completeness | 4 | Success/completion criteria | Met | B:378 "Bar, fixed now and the same as D11: (a) ... (b) ... (c)"; B:202 "0 \| all hunks attributed ... \| proceed" | MET (1) |
| Completeness | 5 | Explicit out of scope | Met | B:246-247 "not changed" rows; B:340 "Later adopters (not part of this change)"; B:478 "it stays outside this theme's scope" | MET (1) |
| Correctness | 1 | No factual errors | Met (spot-checked claims match ground truth) | B:241 "486 lines in `src/` ... the `plugins/` copy still has the 472-line text" (both verified by `wc -l`); B:9 "control mean 6.0, arm A 5.5, Arm B 3.5 (r1 = 6, r2 = 1)" matches ARMB-REPORT.md:13,20; B:242 sc- strip rule matches `install_skills.py` | MET (1) |
| Correctness | 2 | Feasible with stated constraints | Met | B:364 "reviser briefs T06 and T08 stay verbatim (the reviser learns the budget from the report)"; B:370 "no brief mentions the checker, the ledger or the budget" | MET (1) |
| Correctness | 3 | Terminology consistent | Met | Budget classes `C`/`M`/`m` defined B:174-176 and identical in B:273-275 and `BUDGETS` B:296-298; `std\|large\|-` defined B:128 | MET (1) |
| Correctness | 4 | No internal contradictions | Not met: two pinned tests cannot both pass | B:331 M2 requires line-for-line equality with `spec-panel.md` outside the listed regions, while B:334 "M5 ... no `src/superclaude` in the command or the skill"; the original carries `src/superclaude/examples/release-spec-template.md` at line 220 | NOT MET (0) |
| Correctness | 5 | Claims supported by evidence/rationale | Met | B:89-98 replay of caps on flg-r2 ("80 (proposed) \| 11 \| 449"); B:407 explicit derivation "(3 x 0.9 + 3 x 0.6 + 2 x 0.5 + 3 x 0.3) / 13 = 0.49" with assumed rows labelled (B:404-405) | MET (1) |
| Structure | 1 | Logical ordering | Met | B:100 "## 2. Mechanism (each loop step, in order)" with Step 0 setup, Step 1 review, Step 2 reviser, Step 3 checker, Step 4 enforce, Step 5 next review | MET (1) |
| Structure | 2 | Consistent hierarchy | Met | `##` 1-8 with `###` 1.1-1.6, Steps 0-5, 4.1-4.6, 6.1-6.4, 7.1-7.4; no orphan levels | MET (1) |
| Structure | 3 | Separation of concerns | Met | B:216 "## 3. Causes removed and causes left" separate from B:235 "## 4. Exact changes" and B:372 "## 6. Measurement plan" | MET (1) |
| Structure | 4 | Navigation aids | Met (cross-references) | B:170 "derivation in section 1.6 and section 6"; B:222 "(section 6)"; B:233 "section 1.3" | MET (1) |
| Structure | 5 | Artifact-type conventions | Met | B:5 "## 1. Problem and evidence" ... B:469 "## 8. Open questions" | MET (1) |
| Clarity | 1 | Unambiguous language | Met: no "should consider", "might", "as appropriate"; one "should too" (B:362) is followed by the concrete decision | B:132 "A finding that none of these can answer inside its budget is listed `escalated`, never expanded." | MET (1) |
| Clarity | 2 | Concrete | Met | B:284-289 literal Reviser brief with five numbered steps and exact commands | MET (1) |
| Clarity | 3 | Section purpose | Met | B:102 "Shape in one paragraph: ..."; B:218 "Target (constraint 1): ..." | MET (1) |
| Clarity | 4 | Acronyms/terms defined on first use | Not met | B:9 "D10/D11/D12" and "FR-8 / FR-9" (B:128) used without definition; "V1-V6" (B:378) undefined | NOT MET (0) |
| Clarity | 5 | Actionable next steps | Met | B:479 "First implementation task: replay harness. Run the finished script over the six recorded loops"; B:353-355 install commands | MET (1) |
| Risk Coverage | 1 | >=3 risks with probability and impact | Not met: the risk table has cause, detection, mitigation and residual columns, no probability | B:444 header "\| # \| failure \| why it can happen (evidence) \| detection \| mitigation \| residual \|"; probabilities exist only for outcomes (B:409), not risks. Searched 7.1-7.4 | NOT MET (0) |
| Risk Coverage | 2 | Mitigation per risk | Met | B:446-456 mitigation column filled on every row, e.g. B:446 "`large` and 2 overrides per cycle; one pre-registered retry at 100/60" | MET (1) |
| Risk Coverage | 3 | Failure modes and recovery | Met | B:211 "`enforce` ... restores the baseline text for every hunk of every finding that fails ... writes the file atomically"; B:160 "`enforce` is the termination guarantee, so the loop cannot spin" | MET (1) |
| Risk Coverage | 4 | External dependencies and failure | Met | B:106 "stops with `E-FIXCHECK-MISSING` ... It never falls back to plain 427 behaviour silently"; B:479 "decide whether `uv run --no-project` is acceptable offline (UNVERIFIED)" | MET (1) |
| Risk Coverage | 5 | Monitoring/validation for risk detection | Met | B:381 "V7 (mechanism honoured): `.fixcheck/receipt-1.json` and `receipt-2.json` exist ... next review's header says `fixcheck: OK`"; B:318 `verify` re-runs `check` | MET (1) |
| Invariant & Edge | 1 | Collection boundaries (empty, single, max) | Met | B:211 "It refuses to run without a ledger that has at least one entry (exit 1)"; B:327 test 10 "override accepted once and twice, refused third (exit 4)"; test 11 "a fifth flag among four blocking ids is ignored" | MET (1) |
| Invariant & Edge | 2 | State interactions across components | Met | B:131 "refuses (exit 1, `STALE-BASE`) if its sha256 differs from `reviewed_sha256` ... This copy is also the saved copy the coordinator needs for the next `--baseline`" | MET (1) |
| Invariant & Edge | 3 | Guard condition gaps | Met | B:166 "The checker also derives the real `op` of the hunk ... and refuses a mislabelled entry"; B:453 "`snapshot` and `check` validate that every id of the block appears in the report body" | MET (1) |
| Invariant & Edge | 4 | Count divergence (off-by-one, ranges) | Met | B:327 test 2 "MAJOR fix of 81 added words: exit 2" (cap 80) and test 4 "minor fix of 13 words, or of 12 words with net +1"; B:450 "renumbering or inserting a numbered item creates 'new ids' (AC-1.4 becomes AC-1.5)" | MET (1) |
| Invariant & Edge | 5 | Interaction effects | Met | B:48 "N3 ... cross-fix interaction"; B:71 class E "two fixes interacted"; B:447 "the ctl-r1 residue findings are what propagation prevents, and the flg-r2 N3/N6 findings are what propagation causes" | MET (1) |

Subtotals B: Completeness 4/5, Correctness 4/5, Structure 5/5, Clarity 4/5, Risk Coverage 4/5, Invariant & Edge Case 5/5.
**Total B: 26/30; qual_score = 26/30 = 0.867.**

## Variant C

| Dimension | # | Criterion | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|---|---|
| Completeness | 1 | Covers all explicit requirements | Met: keeps 7 bullets, cap, additive variant, override, escalation, UV/stdlib, and removes the inherited `src/` lookup | C:182 "This is the only added command contract, not an eighth Review Loop bullet"; C:160 "In the **new variant only**, replace that source-path lookup" (ground truth `spec-panel.md:220`); C:98 "A finding needing more space gets `escalate`, never an invented larger fix"; C:102 logged override | MET (1) |
| Completeness | 2 | Edge cases and failure scenarios | Met | C:329-343 failure-mode table (under-fixing, escalation replaces work, oversized anchors, concurrent change, skipped checker) | MET (1) |
| Completeness | 3 | Dependencies and prerequisites | Met | C:289 "A fresh worker at repository base `2cb683f5` needs no new repository code ... Run the helper through `uv run --no-project python`" | MET (1) |
| Completeness | 4 | Success/completion criteria | Met | C:313-314 bar column "at most 3; each replicate below both controls" / "at most 44.4%"; C:345 "Falsification: ..." | MET (1) |
| Completeness | 5 | Explicit out of scope | Met | C:158 "No CLI registration, package dependency, global rule, routing guide, `/sc:reflect`, rf-qa agent or `/sc:implement` change is part of this variant"; C:347 "Skip a package CLI, database, automatic patch engine ..." | MET (1) |
| Correctness | 1 | No factual errors | Met (spot-checked claims match ground truth) | C:12 "R3 proxy 6 and 1, mean 3.5; actual blocking 4 and 1; growth 27.8% and 32.1%" matches ARMB-REPORT.md:13-16; C:297 "R3 proxy 8 and 4 ... growth 57.7% and 69.3%" matches; C:160 Tool Coordination source-path lookup exists at `spec-panel.md:220` | MET (1) |
| Correctness | 2 | Feasible with stated constraints | Not met: the mechanism depends on coordinator actions and pins that no brief carries, against the success criterion "same briefs with the one-line name substitution" and Q9 "one extra Bash call per fix cycle", and requires the reviser to author baseline byte offsets | C:47 "Use the helper's `freeze` operation ... **before dispatching the reviser**"; C:49 "The coordinator keeps the state hash outside the reviser's allowed write set and passes it as a literal `--state-sha256`"; C:285 "Coordinator freeze/check work is an explicitly measured part of the treatment"; C:81 ledger `"start_byte": 120, "end_byte": 169`; C:325 "about four extra tool calls" per cycle | NOT MET (0) |
| Correctness | 3 | Terminology consistent | Met | "baseline", "candidate", "state", "receipt", "ledger" defined in C:47-49 and C:88-90 and used the same way in C:189-195 and C:259-267 | MET (1) |
| Correctness | 4 | No internal contradictions | Not met | C:88 "`fix` requires at least one real edit" then, in the same paragraph, "A finding answered only by another finding's edit may therefore have `fix` with an incoming `also_answers` link instead of its own edit"; C:195 restates the second form | NOT MET (0) |
| Correctness | 5 | Claims supported by evidence/rationale | Not met: the budget numbers and the headline prediction carry no derivation | C:62 "These are initial engineering choices, not empirically optimized limits"; C:313 "R3 open critical+major proxy ... 1 / 1 \| 1.0" with C:317 "These are deliberately testable forecasts", no derivation given. Searched sections 1, 2, 6 | NOT MET (0) |
| Structure | 1 | Logical ordering | Met | C:22 "Step 1 — review and freeze the input" through C:124 "Step 6 — re-review the accepted candidate"; problem (C:3) before mechanism before changes (C:141) | MET (1) |
| Structure | 2 | Consistent hierarchy | Met | `##` 1-8 with `###` Steps 1-6 and section-4 subsections (C:143, C:162, C:184, C:273); no orphan levels | MET (1) |
| Structure | 3 | Separation of concerns | Met | C:130 "## 3. Causes removed and causes left" separate from C:141 "## 4. Exact changes" and C:323 "## 7. Risks" | MET (1) |
| Structure | 4 | Navigation aids | Met (cross-references) | C:126 "beside the prior review report, `minfix-cycle-N/`"; C:151 "Operational contract from section 2"; C:285 "New gate paths use the convention in section 2" | MET (1) |
| Structure | 5 | Artifact-type conventions | Met | C:3 "## 1. Problem and evidence" ... C:349 "## 8. Open questions" | MET (1) |
| Clarity | 1 | Unambiguous language | Met: no "should consider", "might", "as appropriate"; three plain "should" uses (C:216, C:317, C:351) are bounded by explicit rules beside them | C:216 "Reject larger inputs as unsupported input, not partial success"; C:358 "No schema, exit code, retry limit, ownership rule or baseline behavior is intentionally left open" | MET (1) |
| Clarity | 2 | Concrete | Met | C:189-190 literal `freeze` and `check` invocations; C:209 exact token regex | MET (1) |
| Clarity | 3 | Section purpose | Met | C:5 "**Decision:** treat a revision as a bounded transaction against a saved document" | MET (1) |
| Clarity | 4 | Acronyms/terms defined on first use | Not met | C:16 "FR-8/FR-9" and C:297 "D10 controls", C:299 "D5 metrics" used without definition (D9 is explained at C:287, others are not) | NOT MET (0) |
| Clarity | 5 | Actionable next steps | Met | C:289 "Before a measured loop, show that a fresh worker loaded the new command and executed the installed checker on a tiny valid and invalid fixture"; C:358 "Implementation must follow a checked plan after this design is selected" | MET (1) |
| Risk Coverage | 1 | >=3 risks with probability and impact | Not met: the table gives "Consequence and containment", no probability | C:329 header "\| Failure mode \| Consequence and containment \|"; no per-risk likelihood in rows C:331-343. Searched section 7 | NOT MET (0) |
| Risk Coverage | 2 | Mitigation per risk | Met | C:331-343 each row carries containment, e.g. C:335 "One bounded, edit-hash-specific override is the release valve"; C:339 "One grant/cycle, hard maxima, no pooled budgets and digest binding restrict volume" | MET (1) |
| Risk Coverage | 3 | Failure modes and recovery | Met | C:96 "If the second check fails, admit nothing, retain the last accepted specification and escalate"; C:259-267 exit table with coordinator action per code | MET (1) |
| Risk Coverage | 4 | External dependencies and failure | Met | C:289 "If the helper is absent, halt rather than reinstalling from inside a worker"; C:342 "Checker or installation is skipped ... Receipt absence invalidates the treatment" | MET (1) |
| Risk Coverage | 5 | Monitoring/validation for risk detection | Met | C:307 "Show the SHA-linked evidence chain for every accepted cycle"; C:291 "Maintain an install watcher for all treatment files and the original command" | MET (1) |
| Invariant & Edge | 1 | Collection boundaries (empty, single, max) | Met | C:216 "at most 2 MiB per specification/report/JSON input, 256 findings and 256 edits"; C:275 "a zero-edit ledger with explicit escalations"; C:195 "It rejects empty files" | MET (1) |
| Invariant & Edge | 2 | State interactions across components | Met | C:47 "Existing state with exactly the same inputs is an idempotent success; different contents are a conflict"; C:49 "both hashes are checked again after revision and before the next review" | MET (1) |
| Invariant & Edge | 3 | Guard condition gaps | Met | C:195 "rejects duplicate JSON keys and unknown schema fields ... out-of-range or non-boundary byte offsets ... overlapping edits, no-op edits"; C:216 "Reject symlink input/output paths" | MET (1) |
| Invariant & Edge | 4 | Count divergence (off-by-one, ranges) | Met | C:90 "Offsets are zero-based half-open **baseline** byte ranges"; C:214 "Enforce limits at equality-inclusive boundaries"; C:275 "a valid 60-word boundary and 61-word rejection" | MET (1) |
| Invariant & Edge | 5 | Interaction effects | Met | C:62 "A shared edit has one owning finding id; optional `also_answers` links do not pool allowances"; C:335 "Coupled fixes ... Aggregated per-finding budgets may punish the correct fix" | MET (1) |

Subtotals C: Completeness 5/5, Correctness 2/5, Structure 5/5, Clarity 4/5, Risk Coverage 4/5, Invariant & Edge Case 5/5.
**Total C: 25/30; qual_score = 25/30 = 0.833.**

## Summary

| Variant | Completeness | Correctness | Structure | Clarity | Risk Coverage | Invariant & Edge Case (floor 1/5) | Total | qual_score |
|---|---|---|---|---|---|---|---|---|
| A (opus, architect) | 4 | 5 | 5 | 4 | 4 | 5/5 (eligible) | 27/30 | 0.900 |
| B (sonnet, analyzer) | 4 | 4 | 5 | 4 | 4 | 5/5 (eligible) | 26/30 | 0.867 |
| C (haiku, backend) | 5 | 2 | 5 | 4 | 4 | 5/5 (eligible) | 25/30 | 0.833 |

Shared misses: none of the three gives per-risk probability (Risk 1) or defines the experiment codes D5/D9/D10, V1-V6 or FR-8/FR-9 on first use (Clarity 4). A and B both inherit the `src/superclaude/examples/...` lookup at `spec-panel.md:220` into the installed variant; only C removes it. No variant falls below the edge-case floor.
