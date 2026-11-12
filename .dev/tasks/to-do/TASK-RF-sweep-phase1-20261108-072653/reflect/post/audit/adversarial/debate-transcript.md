# Adversarial Debate Transcript
## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel, Round 2 sequential) plus Round 2.5 invariant probe (see invariant-probe.md); sections for Round 2 are appended below as they complete
- Convergence threshold: 80%
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 3 (sonnet, haiku, opus general-purpose agents; read-only)
- Total diff points: 29 (S 3 + C 18 + X 5 + promoted A 3)
- Note: advocate output is condensed by the orchestrator (nothing dropped from position tables, shared-assumption responses or concessions).

## Round 1: Advocate Statements

### Variant 1 Advocate (reviewer 1, analyzer, sonnet; agent ac4ebbeb613e7ed2c)
**position_summary.** V1's classifications are the best calibrated: no blocking item; its Authorized label for Rule 5 rests on the owner decision at FINAL-GATE-halt-resolution-decision.md:17-19. V1 is incomplete (missed ledger head read, NFR-007 test stop, fsmonitor/FIFO). The merge should keep V1's classes and add V2's and V3's unique findings at the calibrated Drift severity, with no blocking item.
**steelman (V2).** FR-006 (SPEC :100) was never amended; the owner approved a DESIGN edit, and DESIGN section 13 was left unchanged (decision :23), so the deviation is not a closed documented one. V2 got right: 33 of 33 citations, the stale banner (R2-F1), the NFR-007 mismatch (`test_probes_allowlist.py:1144`, `:1169`), the ledger head (R2-F5). Weakness: three blocking labels, all overstated; R2-F6 names the owner decision as its own authorization_source.
**steelman (V3).** SPEC :286 is an explicit mechanism (Popen, chunked reads, kill past 8 MiB); code does none of it and DESIGN is silent; under "explicit constraint" a Regression is defensible. V3 has the widest risk surface; R3-F1, R3-F2, R3-F5 supported; `checked_clean` is useful. Weakness: ledger labelled Regression while admitting low practical risk.
**strengths.** (1) R1-F1 grounded: FINAL-GATE :18 edits DESIGN :491 and :760, :17 records "All 3 approved", :23 leaves section 13 unchanged. (2) R1-F3 (dispatchId guard hole) is unique and supported. (3) R1-F4 drift medium matches the calibrated outcome for R3-F3; task :2992 note (13) records the departure but SPEC/DESIGN/owner do not approve it. (4) R1-F2 necessary: omission documented inline (`probes.py:432-434`, `1.0a-facts.md:35`). (5) Grounding gaps listed honestly.
**weaknesses (own).** Missed the ledger head read (task :2992 note (12) states it); did not verify NFR-007; did not examine fsmonitor, FIFO, sanitizer, stale text, FIN-F7, full suite; never read note (13); DC-1 citation `:18-19` for open item 6 is off; R1-F8 overstated (aligned); R1-F7 partly overstated; R1-F1 should carry a residual footnote Drift (FIN-F15).
**concessions.** V2 and V3 cover about twice V1's surface; V3's Regression label for Popen is textually defensible but held at Drift; drop R1-F8; add residual Drift note to R1-F1.
**shared assumptions.** A-001 QUALIFY (DESIGN 15.2 covers REPORT only; an explicit owner decision overrides for Rule 5 only). A-002 QUALIFY (Regression needs a contradicted criterion, constraint or invariant; a test-only gap is Drift). A-004 ACCEPT (task notes are run logs, not SPEC/DESIGN approval).
**point positions.** X-001/C-001 Authorized minor (+ residual footnote Drift minor); X-002/C-002 Drift medium; X-003/C-003 Drift medium; X-004 Authorized minor; X-005/C-012 Drift medium; C-004 Drift medium; C-005 Drift minor; C-006, C-007 Drift medium; C-008 Drift minor; C-009 Drift medium; C-010 Authorized; C-011 Necessary; C-013, C-014 Authorized minor; C-015 Drift medium; C-016, C-017 Drift minor; C-018 Aligned (drop).

### Variant 2 Advocate (reviewer 2, qa, haiku; agent a00cbe54fbc6c80c4)
**position_summary.** V2 separates incomplete acceptance evidence from an unqualified completion claim. Withdraws all three blocking ratings, accepts the owner-authorized Rule 5 limitation, retains a minor Regression for the ledger reader as a contradiction of an explicit read constraint.
**steelman (V1).** Separates an observed limitation from an unauthorized implementation choice; R1-F1 correct on owner approval (O:18), R1-F4 correct on buffering before the size check (P:257-270, :308-315). Weakness: treats "no acceptance criterion fails" as sufficient to avoid Regression though SPEC :286 requires chunked reads and a kill independent of final output.
**steelman (V3).** Mechanics matter when the SPEC pins safety constraints; R3-F3 correctly contrasts S:286 with P:257-270; R3-F4 correctly finds the missing head read. Its ledger severity is too high given D:62 searches only the tail; "tasklist is not approval" needs room for task records carrying explicit owner decisions.
**strengths.** R2-F6 keeps the S:100 mismatch visible even when Authorized; R2-F5 is an exact departure (D:62, S:295 vs P:563-565); R2-F2 distinguishes continuation from repair (O:17); R2-F4 asks the right evidence question (S:136 requires publication, not rendering).
**weaknesses (own).** R2-F6's Regression/blocking label is wrong (O:18 authorizes) - agrees with Authorized/medium; R2-F5 blocking unsupported; R2-F4 blocking overstates; objective 3 "fail" disproportionate; confidence too strong for a sampled pass.
**concessions.** All three blocking ratings overstated. Accept R2-F6 Authorized medium and R2-F4 Drift medium. Keep R2-F5 Regression minor. Prefers R3-F3 Regression medium over the calibrators' Drift.
**shared assumptions.** A-001 REJECT (D:925 gives DESIGN precedence over REPORT only; Rule 5 has specific owner authorization). A-002 QUALIFY (Regression can contradict an explicit constraint like S:286 without a demonstrated output failure; missing publication-test evidence alone proves no runtime failure). A-004 QUALIFY (a tasklist alone does not amend requirements, an explicit owner decision can).
**point positions.** C-001 Authorized medium; C-002 Regression minor; C-003 Regression medium; C-012 Drift medium; X-001 Authorized medium; X-002 Regression minor; X-003 Regression medium; X-004 Authorized minor; X-005 Drift medium.

### Variant 3 Advocate (reviewer 3, refactorer, opus; agent aff5ffbfe33576791)
**position_summary.** V3 is the only card grading the risky code paths of probes.py (fsmonitor, FIFO, subprocess output cap, report_path sanitizer); keep those. Accepts calibration on R3-F4 (Drift minor). Holds R3-F3 as Regression medium under the explicit-constraint clause: neither tasklist nor DESIGN overrides SPEC :286 and the missing kill changes real behaviour.
**steelman (V1).** Traces the owner decision for inert Rule 5 most fully; alone finds U-001 (origin-guard hole: `classify.py:690-694`, `:759-762`); applies "Drift unless an acceptance criterion fails" consistently. Weaknesses: one off citation (`:18-19` vs quote at `:13`), R1-F7/R1-F8 overstated, no fsmonitor/FIFO/sanitizer.
**steelman (V2).** Reads acceptance criteria strictly: an unmet SPEC criterion stays unmet whatever DESIGN later says; checks the objectives against disk; catches stale approval text; finds the NFR-007 test gap. Weakness: three blocking labels with no behaviour failure; R2-F6 names its own authorization source.
**strengths.** (1) Unique risk surface U-004: `_git` has no `core.fsmonitor=false` (`probes.py:304-310`) against the module docstring and CHANGELOG "changes nothing"; FIFO reads (SPEC :291 untimed); `report_path` sanitizer; all supported by the calibrator at drift/medium. (2) R3-F3 grounded in SPEC :286, the task note (13) confirms the code does not do it. (3) The authority gap is exact: the tasklist item (task file :1452) chose `subprocess.run` "because the subprocess guard only catches calls made as subprocess.run", but DESIGN :753 and `tests/sweep/conftest.py:36-41` block `Popen` and `os.system` alike, so the departure was neither forced nor approved. (4) Best citation grounding (0.88) and a checked_clean list. (5) R3-F9, R3-F10 correctly Authorized.
**weaknesses (own).** R3-F4 overstated (head read has no observable effect: SPEC :295 and DESIGN :62 say the tail is searched) - Drift minor. Did not examine C-001, C-004, C-009, C-012 (coverage 0.70). Two citation errors (`probes.py:837`, `commands.py:219-221`). Low actionability (0.55).
**concessions.** R3-F4 Drift minor (covers the misnamed test too). R3-F3: partly disagrees with the calibrators; if A-002's narrow rule (only a failed acceptance criterion counts) is adopted it accepts Drift medium (SPEC :297 fixtures pass).
**shared assumptions.** A-001 QUALIFY (DESIGN :925 covers REPORT only; a SPEC difference counts as approved only if section 13 lists it or an owner decision names it; DESIGN is silent on Popen and agrees with SPEC on head+tail). A-002 QUALIFY (an explicit constraint counts; a gap only in tests or wording with identical behaviour is Drift). A-004 ACCEPT (the tasklist's premise is contradicted by DESIGN :753, so a plan item cannot authorize departing from SPEC :286).
**point positions.** C-001/X-001 Authorized medium (+ footnote Drift minor); C-002/X-002 Drift minor; C-003/X-003 Regression medium (fallback Drift medium under the narrow A-002 rule); X-004 Authorized minor; C-012/X-005 Drift medium; C-004 Drift medium; C-006, C-007, C-015 Drift medium; S-002 no blocking findings.

### Orchestrator check after Round 1 (grounding for Round 2)
- DESIGN :753 and `tests/sweep/conftest.py:4,36,41` confirm the autouse guard patches `subprocess.run`, `subprocess.Popen` and `os.system`, so the task item's stated reason for `subprocess.run` (task file :1452, quoting research/05) is false. The departure from SPEC :286 is therefore neither forced nor approved.
- `tests/sweep/test_probes_allowlist.py:1144-1147` and `:1169` confirm that the two "still publish" tests stop at `report.render` (orchestrator re-read).
- `test_probes_allowlist.py:1320-1331` confirm FINAL-at-start is "lost once only the tail is searched" (the test shows tail-only searching) and that the test named `..._read_as_head_and_tail` asserts only a tail-derived boolean.

## Round 2: Rebuttals (sequential: V1, V2, V3; agents a008c7c1a794e1294, a309807e0d898aebe, a2a480c5c08d797c6; condensed)

### Variant 1 Advocate
- Conceded: the task's reason for `subprocess.run` is false (orchestrator check), so the departure is unforced and unapproved, never Necessary/Authorized. Countered on class: Regression needs a broken acceptance criterion or invariant; SPEC :297 boundary fixtures feed finished outputs and `probes.py:270-273` returns `call_failed`, so they pass; `subprocess.run(timeout=...)` still kills a runaway child at 10 s. User-visible differences exist only for a runaway child: (i) output buffered until exit or timeout rather than stopped at 8 MiB; (ii) SPEC gives `call_failed` "output over 8 MiB" (`orca_available` stays true) while the code gives `unavailable` "timeout after N s" (`probes.py:264-265`), which per SPEC :287 stops further Orca calls.
- C-002: SPEC :295 says the tail is searched, so the unread head changes no result: accept Drift minor; the code comment (`probes.py:561-562`) states tail-only openly and `test_probes_allowlist.py:1320-1331` pins it.
- C-004: `_guard` only sees rows that survive the drop (`classify.py:730`, `:739`); a dropped row cannot be protected by `:739`; it masks the problem when another non-ready row survives; the all-rows-dropped case leaves `rows` empty, all four guard flags False, `_origin_unknown` (`:690-694`) reads only `listing.unscanned`, and the path can end in `person_started=True` (`:761-762`). Keep Drift medium (narrowed).
- C-001 Authorized minor + residual footnote Drift (SPEC :100 never amended, DESIGN section 13 unchanged).
- Adopts V3's C-006, C-007, C-015 and V2's C-009, C-010, C-013, C-014; drops C-018. Would accept Regression for C-003 only under the rule "any unapproved departure from an explicit SPEC mechanism is Regression", which it rejects because A-002 requires a failed criterion.
- Final: C-003 Drift medium; C-002 Drift minor; C-001 Authorized (+Drift footnote) minor; C-004 Drift medium; C-005 Drift minor; C-012 Drift medium; C-018 dropped.

### Variant 2 Advocate
- C-003: counter V1: S:286 expressly requires stopping reads and killing the child above 8 MiB; P:257-270 buffers before checking; a continuously emitting child can exceed the memory bound and reach the timeout branch returning `unavailable` instead of the specified output-limit failure: an observable safety-constraint breach, not only an unapproved mechanism choice; boundary fixtures do not exercise the running-child case.
- C-002: concede to V1 and V3 (no output difference); inconsistent to call it Regression. C-012: concede (Drift medium: missing publication evidence, no demonstrated failure). C-001: Authorized, keep medium impact (a named class is intentionally unavailable). C-009: Drift medium, reconcile before documentary completion, not a runtime-promotion veto. Objective labels: concede the conflation: objective 3 qualified pass, objective 6 not fully satisfied (literal all-green unmet, publication coverage incomplete), objective 7 pending (an audit cannot classify its own unfinished gate as a deviation).
- Final: C-003 Regression medium; C-002 Drift minor; C-012 Drift medium; C-001 Authorized medium; C-009 Drift medium.

### Variant 3 Advocate
- R3-F4 withdrawn to Drift minor (misnamed test belongs to the same minor Drift). C-003 kept Regression medium: the taxonomy lists "explicit constraint" as a separate route to Regression; SPEC :286 states the mechanism and SPEC :296 refers the 8 MiB case back to it; DESIGN :386 is silent; silence is not an amendment (DESIGN section 13 does not list it; DESIGN 15.2 gives DESIGN precedence over REPORT only); the task's stated reason is false; the final safety report's check C1 confirms only `subprocess.run` is used (`qa-readonly-safety-report.md:30`). Fallback Drift medium if the narrow A-002 rule is adopted. Accepts V2's qualification: an explicit owner decision recorded in a task file (FINAL-GATE :17-18) authorizes; a plan item alone, built on a false premise (task :1452), does not.
- Self-correction C-006/C-007: already recorded (task :3066 as a [Low] follow-up; `qa-readonly-safety-report.md:13-14`, `:55-56` MINOR follow-up candidates, verdict PASS at `:58`); `-c core.fsmonitor=false` would change the pinned NFR-002 argv (`design-base.md:343`) so it needs an owner note; on FIFO, SPEC :291 itself says disk reads are untimed: hardening follow-up / SPEC gap, Drift minor only if a class is forced. C-015 lowered to Drift minor (path is chosen by the tool under `<root>/.dev/sweeps/`; not re-read). R3-F10/DC-5 Authorized minor.
- Not re-verified: SPEC :286 line itself, DESIGN :717, the sanitizer code, whether a budget-cut timeout inside `_orca` becomes `call_failed` as SPEC requires (task note (2) says `_call` converts it).
- Adopts from V1: C-004 narrowed, the residual footnote Drift on C-001, dropping C-018. Adopts from V2: C-009, C-010, C-012 Drift medium, objective 6 not fully satisfied.

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|---|---|---|---|
| S-001 | all (no dispute) | 95% | sections differ in presentation only |
| S-002 | no blocking finding | 92% | all three advocates now agree; blockers withdrawn after calibration |
| S-003 | four-class vocabulary | 90% | taxonomy of the skill; "authorized" is the skill's class 1 |
| C-001 / X-001 | Authorized (+ residual footnote Drift) | 88% | FINAL-GATE-halt-resolution-decision.md:17-19; V2's own authorization_source |
| C-002 / X-002 | Drift minor | 85% | tail-only search has the same output (SPEC :295, DESIGN :62); V2 and V3 conceded |
| C-003 / X-003 | Regression medium (V2, V3) against Drift medium (V1, both calibrators) | 62% | SPEC :286 explicit mechanism not implemented, `unavailable` vs `call_failed` on a runaway child; no acceptance fixture fails; task's reason false; 2 of 3 |
| C-004 | Drift medium | 80% | `classify.py:690-694`, `:739`; all-rows-dropped case fails open |
| C-005 | Drift minor | 82% | `probes.py:316` vs SPEC :286; reason string collapsed at `:936-937` |
| C-006 | Drift minor, hardening follow-up (V3), medium (V1) | 66% | no `-c core.fsmonitor=false`; already filed as follow-up and a MINOR safety-gate note |
| C-007 | Drift minor, hardening follow-up | 66% | SPEC :291 says disk reads are untimed |
| C-008 | Drift minor | 80% | V1 and V3 agree |
| C-009 | Drift medium | 85% | DESIGN :5, task :3037-3043 |
| C-010 | Authorized | 85% | FINAL-GATE-FIN-F7-ruling.md:17 |
| C-011 | Necessary | 85% | environmental causes re-confirmed by the orchestrator |
| C-012 / X-005 | Drift medium | 88% | tests stop at `report.render` (orchestrator re-read) |
| C-013 / X-004 | Authorized minor | 80% | copies DESIGN :717 and :680 verbatim |
| C-014 | Authorized | 85% | DESIGN :1052 |
| C-015 | Drift minor (V3), medium (V1) | 62% | sanitize on JSON path; low practical impact |
| C-016, C-017 | Drift minor | 78% | V3 only, supported by calibration |
| C-018 | dropped (aligned) | 85% | DESIGN :346 plus :517 |
| A-001 | QUALIFY | 85% | DESIGN precedence covers REPORT, not SPEC; a SPEC difference is approved only where DESIGN section 13 lists it or an owner decision names it |
| A-002 | QUALIFY | 82% | Regression = contradicts a criterion, explicit constraint or invariant; a test-only or wording gap with identical behavior = Drift |
| A-004 | ACCEPT | 85% | a plan item is not authority; an owner decision recorded in the task is |

## Convergence Assessment
- Points resolved: 29 of 29 (28 by unanimity of final positions on class; C-003 by 2 of 3 majority; C-006 and C-015 agree on class and differ one step on severity)
- Alignment: 100% (threshold 80%)
- Status: CONVERGED on advocate positions, subject to the Round 2.5 invariant gate (see invariant-probe.md)
- Unresolved points: C-003 dissent (V1: Drift medium; both blind calibrators: Drift medium); recorded in the merged verdict as a contested classification
