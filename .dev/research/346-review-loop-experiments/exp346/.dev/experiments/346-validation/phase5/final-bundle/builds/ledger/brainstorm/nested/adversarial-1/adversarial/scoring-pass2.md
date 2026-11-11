# Scoring Pass 2 (reverse order: C, B, A)

Step 3, hybrid scoring, qualitative part only. Pass 2 evaluated the variants in reverse order, independent of pass 1 (`scoring-pass1.md` not read).

- C = `variant-3-haiku-backend.md`, B = `variant-2-sonnet-analyzer.md`, A = `variant-1-opus-architect.md`.
- Requirements: `seed-brief.md` sections Constraints and Success Criteria, plus the 12 required spec sections. Context: `diff-analysis.md` (DA), `invariant-probe.md` (INV).
- Method: Claim, Evidence, Verdict. MET = 1 needs a quote or section; no evidence means NOT MET = 0. Section numbers are each variant's own.
- Repo citation checks (files read under `bs346-ledger/` in this pass):
  - C: `test_review_severity_rule.py:215-219` (cap text at 215, at-cap clauses at 216), `spec-panel.md:261` (cap bullet), `install_skill.py:35-53` (`copytree` at 52), `managed-workspace.md:54,64`, `rf-qa.md:386-416`, `qa.md:186` and `:311`, `spec-panel-review-loop.md:143,162-164`. All accurate.
  - B: `install_commands.py:38-41,59-61` (glob at 40, `copy2` at 61), `install_skills.py:40-59,88-98` (`_has_corresponding_command`, skip and delete stale copy), `pyproject.toml:85-87` (force-include `src`), `sc-bare-review/SKILL.md:3`, `test_workflow_archive.py:22-28`, `test_worker_contract.py:831-839`, `reflect SKILL.md:587`, `rf-qa.md:401`. All accurate.
  - A: `install_commands.py:11,40`, `install_skill.py:52`, `test_cli_install.py:111-121,187,501-505`, `test_routing_plugin_parity.py:41-47` (four mirrored commands), `rf-qa.md:387,391,401`, `test_review_severity_rule.py:181-182,320-325`, `qa.md:137,141,143,166`. All accurate. `reflect SKILL.md:42` is the hallucination contract, not the gate line (35 or 587), a minor imprecision.
  - Feasibility check for A: `tests/skills/test_worker_contract.py:20,831-839` asserts that the set of `src/superclaude/commands/*.md` files with a `## Unattended mode` heading equals `UNATTENDED_COMMANDS`. A's command is "Byte-identical to `spec-panel.md` except" frontmatter, usage line 1 and `## Review Loop`, so it keeps `## Unattended mode` (`spec-panel.md:451`) and would fail that test. A does not list that test or an edit to it.

## Qualitative

### Completeness

| Criterion | C verdict | C evidence | B verdict | B evidence | A verdict | A evidence |
|---|---|---|---|---|---|---|
| Covers all explicit requirements | MET | All 12 sections present; ledger format, location and transitions (s3); computed rule with PASS, CONTINUE, ESCALATE (s4); 427 difference (s5); adoption (s7); recommendation (s8); forecast and failure test (s9); cap literal retained verbatim (s4); installed path lookup `~/.claude/skills/review-ledger/SKILL.md` (s6) | MET | All 12 sections; T1 to T11 table and JSONL format (s3); `close` pseudocode (s4); duty table vs 427 (s5); adoption table (s7); recommendation (s8); P3, P3s predictions and five failure conditions (s9); cap literal cited to `test_review_severity_rule.py:215` (s4) | MET | All 12 sections; layout, JSON example and transition table (s3); `decision(k)` (s4); 427 comparison table (s5); adoption table (s7); recommendation (s8); prediction table and "What would mean the idea failed" (s9); cap bullet verbatim (s4) |
| Edge cases and failure scenarios | MET | s3 "A missing/ambiguous anchor cannot become verified"; s6 "Transaction, crash and rerun contract"; s2 overflow above 200 changed lines yields ESCALATE | MET | s11 "Ways the ledger could make the loop worse" items 1 to 8 (refusal stalls, moved sections, tamper hash on reformat, unattended coordinator meets exit 11) | MET | s2 `W-NO-ANSWERS` when the reviser never ran `answer`; s11 risks 3, 4, 6 (anchor brittleness, hand edits, moved paragraphs) |
| Dependencies and prerequisites | MET | s6 "A script must ship in the skill payload: installation copies the whole skill directory"; "Plugin packaging parity ... UNVERIFIED"; s11 local filesystem only | MET | s6 install mechanics with naming trap; "Experiment install (not a repo change)"; s12 q10 "that every worker environment has `uv`" UNVERIFIED | MET | s6 command reaches `~/.claude/commands/sc/` via `install_commands.py:11,40`, script via `install_skill.py:52`; s2 `<skill base>` "given by the Skill tool" |
| Success or completion criteria | MET | s9 "Apply the fixed bars <=3 and <=44.4%, effect larger than the larger within-arm spread, and every treatment replicate better than every control replicate" | MET | s9 "Bar (set now, same shape as D10 and D11)" items (a) to (c) | MET | s9 bar column in prediction table and failure list citing "the D11 rule, `DECISIONS.md:64`" |
| Explicit out of scope | MET | s6 "Leave `src/superclaude/commands/spec-panel.md`, its plugin copy, severity pins and routing defaults unchanged"; s8 "Skip a durable reviewer-session manager, database server"; s11 "skip cross-run dedup services, signatures, auto-waivers" | MET | s6 "Edited files: none in the original loop"; s7 "Two things the first version does NOT do" (several files, concurrent writers) | MET | s6 "Not changed" row; s7 "No adopter is changed by this design; each is a later, separate change" |

Subtotal Completeness: C 5/5, B 5/5, A 5/5.

### Correctness

| Criterion | C verdict | C evidence | B verdict | B evidence | A verdict | A evidence |
|---|---|---|---|---|---|---|
| No factual errors or hallucinated claims (3 or more repo citations checked) | MET | 8 repo citations checked (see header list), all match the files, for example cap literal at `test_review_severity_rule.py:215` and `copytree` at `install_skill.py:52` | MET | 8 repo citations checked, all match, including the install naming trap at `install_skills.py:40-59,88-98` and the set-equality test at `test_worker_contract.py:831-839` | MET | 9 repo citations checked, all match (one slight line imprecision at `reflect SKILL.md:42`), for example four mirrored commands at `test_routing_plugin_parity.py:41-47` |
| Feasible with stated constraints | NOT MET | s9 claims "Only authored brief change: substitute `/sc:spec-panel` ... on its invocation line", but s2 requires "The coordinator alone runs ledger mutations" and s11 "four reviewer sessions including the sweep"; the S1 arm cannot run under the one-line constraint (DA X-018) | MET | Deviation is disclosed, not hidden: s9 "ONE added dispatch after review 3 ... The added sixth session is a stated deviation"; s6 omits `## Unattended mode` so `test_worker_contract.py:831-839` stays green; skill name avoids the install skip | NOT MET | s6 command "Byte-identical to `spec-panel.md` except" three blocks keeps `## Unattended mode`, which fails the set-equality assertion at `test_worker_contract.py:837`; A's keep-green list omits that test |
| Consistent terminology | MET | s2 and s4 use F, C, S rows, `loop_decision`, `delivery_outcome`, MECHANICAL and PROSE the same way throughout | MET | `sev` (blocking or minor) and `grade` (CRITICAL, MAJOR, MINOR) kept distinct in s3, s4, s9 ("Grade, not `sev`") | MET | statuses `open`, `deferred`, `fixed`, `verified`, `reopened` and `B(k)` used identically in s3, s4, s9 |
| No internal contradictions | NOT MET | One-line brief change (s9) versus coordinator-run mutations and an extra reviewer session (s2, s11), DA X-018; random `run-id` default versus "No missing-ledger fallback" (s2, s3), DA X-019 | NOT MET | s6 bullet 3 "CRITICAL and FR-8/FR-9 are blocking" but `add` rows carry no rule field (DA X-016); T4 keeps status yet T8 has `disputed` as a From state (DA X-017) | NOT MET | s3 hunks are "new-file line ranges" while `regressed` compares a stored `r2:` span with this round's hunks, mixing coordinates (DA X-020) |
| Claims supported by evidence | NOT MET | Most claims cite sources, but the headline forecast is bare: s9 "Forecast, not measured: headline proxy 1 and 2, mean 1.5" with no derivation, while its proxy counts more rows than A or B (DA X-011, X-012) | MET | s9 trace table per replicate and explicit growth arithmetic ("Gives 21.3% and 24.9%"); s5 line-by-line hunk check on ctl-r1 and N12 | MET | s9 "Basis:" paragraph ties the 2.5 forecast to Arm B R1 counts and flg-r2 R3 (`ARMB-REPORT.md:13,14,31`) and growth to the 9-of-15 minor rows (`disposition-round2.md:35`) |

Subtotal Correctness: C 2/5, B 4/5, A 3/5.

### Structure

| Criterion | C verdict | C evidence | B verdict | B evidence | A verdict | A evidence |
|---|---|---|---|---|---|---|
| Logical ordering | MET | s1 to s12 in the required order, mechanism before file format before termination | MET | s1 to s12 in the required order; step table precedes per-step explanations (s2) | MET | s1 to s12 in the required order; components table precedes per-step blocks (s2) |
| Consistent hierarchy | MET | `##` numbered sections with `###` subsections ("Storage and schema", "Row transitions", "Transaction, crash and rerun contract") | MET | `##` numbered sections with bold labelled paragraphs ("Format", "Location", "Frozen after `add`") used uniformly | MET | `##` numbered sections with bold labelled paragraphs ("Location", "Layout", "Format", "Computed fields") used uniformly |
| Separation of concerns | NOT MET | s11 table header "Rule or cost" mixes rules and costs in one table (DA S-012); test cases listed inside the transaction subsection of s6 (DA S-009) | MET | Costs, worsening risks and rule classification are three separate labelled blocks in s11; CLI and tests separate in s6 | MET | s2 "Three components, each with one job": kernel, contract, adapter (DA U-001) |
| Navigation aids or cross-references | MET | s2 "section 11 names them individually"; s5 and s9 refer back to s2 and s4 | MET | Preamble citation alias list (`SP`, `DES`, `QA` ...); in-text "(section 10)", "(section 6)" | MET | In-text "(section 9)", "(section 12)", "(section 11)" pointers from s4 and s8 |
| Follows design spec conventions | MET | Problem, mechanism, data schema with example, interface CLI, tests, risks, open questions; status line "Design proposal ... Nothing in this document is implemented" | MET | Status line "Design only. Nothing here is implemented."; schema example, CLI table, test plan, risks, open questions | MET | Status line "design only, nothing implemented"; schema example, CLI table, tests, risks, open questions |

Subtotal Structure: C 4/5, B 5/5, A 5/5.

### Clarity

| Criterion | C verdict | C evidence | B verdict | B evidence | A verdict | A evidence |
|---|---|---|---|---|---|---|
| Unambiguous language | NOT MET | Core rule outcome is undeterminable: s3 "Script carries it only when its mapped text and supporting context are unchanged"; "supporting context" is never defined (DA A-011) | NOT MET | Transition table is ambiguous: T4 "(stays; `claim.action=disputed`)" yet T8 starts from `disputed` as if it were a status (DA X-017) | NOT MET | s3 `verified` needs "`broke_sentence` given" but no consequence of `broke_sentence: true` is stated (DA X-015) |
| Concrete | MET | s3 full JSON example; s6 exit codes "0 ... 2 for CONTINUE, 3 for ESCALATE; 4 invalid ..."; closed per-phase input fields | MET | s3 JSONL example built on F10, F22, N12 shapes; s6 subcommand table with exit codes | MET | s3 JSON example with N5, N12, N9; s6 subcommand table and named error codes |
| Each section one clear purpose | MET | Each `##` section matches its required topic; s10 is only the causes table and net claim | MET | Each section matches its topic; s5 is only the 427 duty table and its limit | MET | Each section matches its topic; s8 is only the comparison table and recommendation |
| Terms defined on first use | MET | s2 "Let `D` be the existing working specification; `L` an explicit absolute ledger path; `P` the selected skill directory"; s4 defines `B_r`, `X_r`, `I`, `S`; s9 defines `U3`, `W` | MET | Preamble defines every alias; s2 "Names used below" defines `LEDGER`, `DOC`, `L`, actors; s9 defines P3, P3s, H | MET | s2 "Below, `L` is the ledger directory and `D` the document"; s4 defines `B(k)`; s3 defines profile and computed fields |
| Actionable next steps | MET | s12 q2 "Preflight on saved copies before preregistering a run"; s6 file table with exact responsibilities | MET | s6 "Run `uv run pytest tests/skills/test_review_severity_rule.py` first"; s12 recommendations per question ("Recommendation: only by the user") | MET | s6 file table with exact changes and named test cases per file |

Subtotal Clarity: C 4/5, B 4/5, A 4/5.

### Risk coverage

| Criterion | C verdict | C evidence | B verdict | B evidence | A verdict | A evidence |
|---|---|---|---|---|---|---|
| At least 3 risks with probability and impact | NOT MET | s11 table gives impact ("Locks in bad first-pass grading") but no probability for any risk | NOT MET | Only one risk carries a level (risk 1 "Residual: MEDIUM"); the other seven have impact only | NOT MET | s11 risks 1 to 7 state impact only; no probability or likelihood given |
| Mitigation per risk | NOT MET | Several rows give no mitigation, for example "Frozen severity, MECHANICAL, Locks in bad first-pass grading" and "Correct phase dispatch ... logs must show actual calls" | NOT MET | Risk 4 "S1 cannot show this" and risk 7 "Experiment confounds" have no mitigation | NOT MET | Risk 5 (no-progress branch escalates early) and risk 6 (moved paragraphs widen hunks) have no mitigation |
| Failure modes and recovery | MET | s6 "Crash before ledger publication leaves the previous valid state ...; crash after publication resumes from the committed event and regenerates missing reports" | MET | s3 "All writes are all-or-nothing (temp file, then `os.replace`)"; s11 risk 1 recovery via candidate lines, `--at`, `revert-unclaimed` | MET | s3 "Refusals are atomic: exit 2 ... ledger untouched"; s2 `answer` re-runnable; s11 risk 3 "`deleted: true`, the uniqueness error names a longer quote" |
| External dependency failures | MET | s11 "Unsupported filesystems or host/storage failure may violate durability"; s6 "no inline fallback if helper is missing"; plugin discovery UNVERIFIED | MET | s11 rule table "a host with neither copy fails at the first call, loudly"; s12 q10 `uv` availability UNVERIFIED; s6 owner's `superclaude` binary not testable | NOT MET | No statement of what happens if `uv`, the installed skill or the script is missing; s11 only says "Invoke the skill and use the script at all, PROSE, detected at the next step" |
| Monitoring or validation mechanism | MET | s9 "Future experiment setup must record variant command, skill and script hashes and actual loaded paths"; "measure both live D and the accepted snapshot" | MET | s9 baseline sweeps on six finals, hidden-defect share H, `minor_touched`, unclaimed bytes | MET | s9 "V1-ledger" validity check and refusal count covariate; `status --json` metrics |

Subtotal Risk coverage: C 3/5, B 3/5, A 2/5.

### Invariant and edge case coverage

| Criterion | C verdict | C evidence | B verdict | B evidence | A verdict | A evidence |
|---|---|---|---|---|---|---|
| Collection boundaries (empty, single, max) | MET | s3 "200 initial rows and 10 MiB per document are explicit refusal limits"; s2 "at most one new finding C001" and 200 changed lines; s6 "No diff means no new fixed states" | MET | Empty: s4 table row "1, 0, PASS, sweep"; max: s11 risk 3 `HUNKS_LARGE` above 40% changed lines; s3 "An unanswered blocking row ... stays `open`" | NOT MET | Empty cases covered (`W-NO-ANSWERS`, PASS at review 1) but no maximum on rows, hunks or document size; only a 12-character minimum anchor |
| State interactions across components | MET | s2 "packets bind response schema, round, document hash and ledger sequence"; s3 verified to fixed when "Reviser changes its mapped sentence again"; s6 reviser crash leaves `D` partly edited | MET | s3 T9 "a hunk of this revision overlaps the row's claim span"; s2 sweep rows classified `in_claimed_span`, `in_unclaimed_hunk`, `outside_hunks` | MET | s2 `begin` checks "the prior report's last line equals the recorded verdict (`E-REPORT-EDITED`)"; s3 `E-NOT-CHANGED`; s11 risk 7 report prose vs ledger |
| Guard condition gaps | MET | s3 "A syntactically nonempty false claim can still block"; s3 "this detects unclaimed edits, not unrelated mechanisms hidden inside a claimed span" | MET | s11 rule table residuals, for example "a small quote inside a large hunk claims the whole hunk (lenient overlap)" and "honesty of `depends_on`" | MET | s11 rule table residuals, for example "text added inside an attributed hunk is invisible to the check" and "the last report could be edited after `close` without detection" |
| Count divergence (off-by-one, inclusive or exclusive) | MET | s6 "A span is `{old_start,old_end,new_start,new_end}` using 1-based half-open line ranges; zero-width ranges denote insertion/deletion boundaries"; s4 "initialization, packet generation and crash retries are not reviews" | MET | s2 "the review counter is a field in `L`, incremented only by `open`"; s9 P3 counts by grade "so that MAJOR rows 427 relabels as minor are counted exactly as the proxy counted them", `U` reported beside it | NOT MET | Spans stored as `"r2:220-220"` with no inclusive or half-open rule and compared against new-file hunks of a later round (DA X-020, INV-014) |
| Interaction effects | MET | s4 delivery outcome combines loop result and sweep count `S`; s6 bullet 5 "Treat any caller phrase making minor findings fail as overridden" | MET | s1 F22 to N5 to N12 chain from a brief overriding the command; s10 item 2 interaction defect N15 rejected unless `depends_on` is found | MET | s4 no-progress branch "changes what 'R3' means in the measurement (section 9)"; s9 sweep duplicates counted with frozen severity of the matched row |

Subtotal Invariant and edge case coverage: C 5/5, B 5/5, A 3/5.

## Totals

| Dimension | C | B | A |
|---|---|---|---|
| Completeness | 5 | 5 | 5 |
| Correctness | 2 | 4 | 3 |
| Structure | 4 | 5 | 5 |
| Clarity | 4 | 4 | 4 |
| Risk coverage | 3 | 3 | 2 |
| Invariant and edge case coverage | 5 | 5 | 3 |
| **Total met/30** | **23/30** | **26/30** | **22/30** |
