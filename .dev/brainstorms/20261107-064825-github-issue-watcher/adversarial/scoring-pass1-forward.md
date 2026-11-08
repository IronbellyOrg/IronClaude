# Base Selection Report, Scoring Pass 1 (forward order A, B, C, D, E)

- Source: `seed-brief.md` (constraints, success criteria, fixed decisions D1 option A, D2 claim-only, D3 integer-only prompt)
- Inputs: `adversarial/blind/variant-A.md` .. `variant-E.md`; `adversarial/diff-analysis.md` (contradictions X-001..X-008); `adversarial/rounds/round2-tally.md` (debate leads)
- Formulas: quant = 0.30 RC + 0.25 IC + 0.15 SR + 0.15 DC + 0.15 SC; qual = criteria met / 30; final = 0.5 quant + 0.5 qual
- Counts: Bash grep/wc/awk over the variant files only (no interpreter, no state change)

## Quantitative Scoring (50% weight)

Method notes:

- **RC** (no formal IDs in the seed): 40 topic items extracted from the seed (5 definitions, D1-D3, repo pin, no-secrets, UV/`src/`, never-as-worker, 5-minute cadence, own login, record-before-launch, six states, re-read, `considered` map, caps, `--retry-launch`, launch argv, marker check, audit line, read:project, truncation `-L 100`, rate limits, label creation, allow-list, routing, same-login, permission mode, live test, Coder cron, `$HOME` persistence, Coder#477, B/C alternatives, revisit conditions, design doc, mock tests, CLI registration, scoring of B and C). Keyword hit per item; item 40 (scoring table for alternatives) is only in C section 2.
- **IC** = 1 - internal contradictions / substantive claim lines. Contradictions are requirement-vs-requirement or requirement-vs-fixed-constraint conflicts inside one variant (cross-checked with diff-analysis X-001..X-008).
- **SR** = concrete lines / (concrete + vague) over substantive lines (non-heading, non-blank, non-table-rule); concrete = contains a number, code span, or named system; vague-term hits were 0 in every variant, so non-concrete lines count as vague.
- **DC** = resolved internal references / internal references. Every FR/NFR/OD/O/R/T/NG/F/FU/C/RC ID referenced is defined in the same file; `Section n` references all resolve to existing H2/H3 sections. External keys (RD-Fn, RF-n, RQ-n, Qn, research F1/F2/B1/B2) excluded.
- **SC** = H2 sections / max H2 (12).

| Metric | Weight | Variant A | Variant B | Variant C | Variant D | Variant E |
|---|---|---|---|---|---|---|
| requirement_coverage | 0.30 | 0.975 (39/40; no B/C scoring table) | 0.975 (39/40) | 1.000 (40/40) | 0.975 (39/40) | 0.975 (39/40) |
| internal_consistency | 0.25 | 0.988 (2/170: OD-5 `off` Project mode vs section 3; lost-reply `pending`->`failed`->fresh launch vs NFR-004) | 0.985 (2/132: FR-022 label-only drops two section 3 definitions; NFR-010 empty reload vs NFR-005) | 1.000 (0/122) | 1.000 (0/165) | 0.967 (4/121: FR-014 `<agent>` vs seed `claude`; FR-010 vs FR-017 claimed condition; NFR-013 pruning vs section 7 `reset`-only exit from `abandoned`; section 2 "every `gh` call names --repo" vs FR-001 `gh api user`) |
| specificity_ratio | 0.15 | 0.959 (163/170) | 0.985 (130/132) | 0.828 (101/122) | 0.982 (162/165) | 0.959 (116/121) |
| dependency_completeness | 0.15 | 1.000 (61/61 IDs; 10 section refs) | 1.000 (88/88 IDs; F10 is external RD-F10; 7 section refs) | 1.000 (22/22 IDs; 2 section refs) | 1.000 (76/76 IDs; 6 section refs) | 1.000 (52/52 internal IDs; F1/F2 external; 8 section refs) |
| section_coverage | 0.15 | 1.000 (12/12) | 1.000 (12/12) | 1.000 (12/12) | 1.000 (12/12) | 1.000 (12/12) |
| **quant_score** | | **0.983** | **0.987** | **0.974** | **0.990** | **0.978** |

## Qualitative Scoring (50% weight), additive binary rubric, 30 criteria

Criteria (5 per dimension; dimension 6 is the protocol's Invariant and Edge Case dimension, not in the template):

- **Completeness:** Q1 all five predicates plus "eligible" defined; Q2 dispatch record with all six states and transitions; Q3 deliverables: modules, CLI verbs, tests, design doc, setup instructions; Q4 follow-ups name live slash-command test, Coder cron, permission mode; Q5 open decisions with recommended defaults (routing, same-login, allow-list, labels, caps).
- **Correctness:** Q6 D2 respected: no post-claim work, no GitHub write by poller; Q7 prompt builder rejects bool/str/float/out-of-range and returns exact `/sc:issue --claim N` (D3); Q8 launch argv matches the seed contract (`--agent claude`, `path:<abs>`, `--surface terminal`, `--json`); Q9 no fresh launch after an ambiguous outcome (lost reply, `unknown`, `launched`); Q10 no internal contradiction.
- **Structure:** Q11 the 12 required sections in order; Q12 unique requirement IDs; Q13 every FR has a testable acceptance criterion; Q14 traceability table to sources; Q15 risks carry ID, likelihood/impact and mitigation.
- **Clarity:** Q16 [PROPOSAL]/ASSUMPTION convention stated and used; Q17 exit codes enumerated with meanings; Q18 exact discovery command given; Q19 audit line fields enumerated; Q20 configuration surface (options or config keys) concrete.
- **Risk coverage:** Q21 residual session injection (claim reads public text) stated; Q22 launched-session permission mode risk with a decision; Q23 missing `read:project` with mitigation; Q24 same-login multi-workspace double claim; Q25 rate-limit signal detected and handled.
- **Invariant and edge case:** Q26 discovery returning exactly the limit fails closed; Q27 bot actor explicitly excluded from approval; Q28 crash between record write and reply handled; Q29 pre-launch re-read plus overlapping-cycle lock; Q30 remove-and-re-add or later `unlabeled` handled.

### Variant A (CEV)

| # | Verdict | Evidence |
|---|---|---|
| Q1 | MET | §3 defines Tagged, Approved, In a Project, Backlog, Intended owner, Eligible as `gh` JSON predicates |
| Q2 | MET | §7 States table (six) plus Transitions table |
| Q3 | MET | §8 module table, verbs `once/status/check-config`, `tests/issue_watch/` list, design doc, setup |
| Q4 | MET | §9 F-1 cron, F-2 live prompt test, F-3 permission mode |
| Q5 | MET | §10 OD-1..OD-9 with defaults and reasons |
| Q6 | MET | §2 D2; FR-020 no `gh issue edit/comment/label`, non-GET |
| Q7 | MET | FR-011 rejects `"12"`, `True`, `0`, `12.0`, `1000000000`; returns `/sc:issue --claim 331` |
| Q8 | MET | FR-012 argv `--agent claude --worktree path:<abs> --surface terminal ... --json` |
| Q9 | NOT MET | §7: lease-expired `pending` with no reply goes `failed` (`lost_reply`), then fresh launch allowed |
| Q10 | NOT MET | OD-5 `off` Project mode vs §3 definition; lost-reply path vs NFR-004 |
| Q11 | MET | 12 numbered H2 sections in required order |
| Q12 | MET | FR-001..020, NFR-001..011, OD, R, F, NG IDs |
| Q13 | MET | §4 every FR has a Given/then line |
| Q14 | MET | §12 requirement-to-source table |
| Q15 | MET | §11 table: ID, Likelihood / impact, Mitigation |
| Q16 | MET | Header convention; caps marked [PROPOSAL] §7 |
| Q17 | MET | §8 exit codes 0-7 with meanings |
| Q18 | MET | FR-003 full `gh issue list ... -L 100` argv |
| Q19 | MET | FR-017 fields `ts, login, cycle_id, outcome, ...` |
| Q20 | MET | OD-9 JSON config path; §8 verbs with `--config`, `--dry-run` |
| Q21 | MET | §6 Launched session row: injection via text the claim reads |
| Q22 | MET | OD-6 `ccsession-orca` default pending F-2, F-3 |
| Q23 | MET | R-3 exit 4 visible; F-4; option D fallback |
| Q24 | MET | R-2 and OD-2 `enabled` default false, one workspace per login |
| Q25 | MET | NFR-006 rate limit / 403 / 429 ends cycle, exit 5 |
| Q26 | MET | FR-003 exactly 100 items: nothing launches, exit 4 |
| Q27 | MET | §3 Approved (b) excludes `type` `Bot` or `[bot]` login |
| Q28 | MET | §7 row "pending (found at cycle start, lease expired)" handled (unsafe direction, scored at Q9) |
| Q29 | MET | FR-010 pre-launch re-read; FR-018 non-blocking lock |
| Q30 | MET | §3 Approved (c) no later `unlabeled` event |
| **Total** | **28/30** | |

### Variant B (CEV)

| # | Verdict | Evidence |
|---|---|---|
| Q1 | MET | §3 table: five terms plus Eligible, each with fail-closed column |
| Q2 | MET | §7.3 transitions cover pending, launched, unknown, failed, claimed, abandoned |
| Q3 | MET | §8.1 modules, §8.2 `once` verb, §8.3 tests, §8.4 design doc and setup |
| Q4 | MET | §9 F1 cron, F3 live test incl. Q6 permission mode, F7 |
| Q5 | MET | §10 OD-1..OD-10 with defaults |
| Q6 | MET | NG1 no GitHub write; NFR-001 bans edit/comment/`--add-assignee` |
| Q7 | MET | FR-013 rejects `0, -1, True, 3.0, None, "331"`; returns `/sc:issue --claim 331` |
| Q8 | MET | FR-012 exact argv with `--agent claude`, `--surface terminal`, `--json` |
| Q9 | NOT MET | §7.3: `launched`, `failed` with lease expired and no marker get a new launch (X-001) |
| Q10 | NOT MET | FR-022 label-only drops two §3 definitions; NFR-010 empty reload vs NFR-005 |
| Q11 | MET | 12 H2 sections in order (plus H3 subsections) |
| Q12 | MET | FR-001..022, NFR-001..013, T1..T11, OD, R IDs |
| Q13 | MET | §4 table Given/When/Then column for every FR |
| Q14 | MET | §12 table with RD/RR/SB keys |
| Q15 | MET | §11 table: Likelihood / impact, Mitigation |
| Q16 | MET | Header "Marking" line; §7.4 [PROPOSAL] values |
| Q17 | MET | FR-021 exit 0-3 with meanings |
| Q18 | MET | FR-022 full label-only argv; FR-004 Project query `-L 100` |
| Q19 | MET | FR-020 keys `ts, mode, own_login, issue, decision, ...` |
| Q20 | MET | §8.2 full option list for `once` |
| Q21 | MET | T4 "Open and material": integer protects prompt, not session |
| Q22 | MET | T5; OD-8 do not enable F1 before Q6 |
| Q23 | MET | R2 `gh auth refresh -s read:project` |
| Q24 | MET | R5 and OD-2 one poller per login |
| Q25 | NOT MET | R9 "Rate-limit replies not handled specially" |
| Q26 | MET | FR-005 exactly 100 items: exit 2, `E-GH-TRUNCATED` |
| Q27 | NOT MET | §3 approval checks allow-list only; no bot-type exclusion |
| Q28 | MET | §7.3 `pending` at cycle start treated as `launched` |
| Q29 | MET | FR-011 changed second snapshot aborts; FR-019 held lock |
| Q30 | MET | FR-007 labeled, unlabeled, labeled(non-approver) rejected |
| **Total** | **26/30** | |

### Variant C (CEV)

| # | Verdict | Evidence |
|---|---|---|
| Q1 | MET | §3 defines all five terms plus Eligible issue by node/field IDs |
| Q2 | MET | §7 six-state table with permitted transitions |
| Q3 | MET | §8 modules, `once/status/init-state`, `tests/issue_watch/`, design doc with setup topics |
| Q4 | MET | §9 owner-run prompt test, `coder_script` schedule, session permission policy |
| Q5 | MET | §10 ten decisions with recommended defaults |
| Q6 | MET | §2 D2; FR-013 GitHub mutation count zero |
| Q7 | MET | FR-009 rejects booleans, strings, fractional, out-of-range; fixed command plus digits |
| Q8 | NOT MET | FR-010 gives only `path:<absolute-path>`; no `--agent claude`, `--surface`, `--json` |
| Q9 | MET | §7 lost reply allows only `--retry-launch`, "never a new ordinary launch" |
| Q10 | MET | No internal contradiction found |
| Q11 | MET | 12 numbered H2 sections in order |
| Q12 | MET | FR-001..013, NFR-001..009 |
| Q13 | MET | Each FR has an Acceptance Given/when/then |
| Q14 | MET | §12 requirement-to-source table |
| Q15 | NOT MET | §11 is prose; no IDs, likelihood/impact or per-risk mitigation |
| Q16 | MET | §7 values marked [PROPOSAL]; §1 ASSUMPTION stated |
| Q17 | MET | §8 exit codes 0, 2-6 with meanings |
| Q18 | NOT MET | No discovery command or argv anywhere |
| Q19 | MET | NFR-005 lists repository, issue, cycle ID, decision, reason, transition, elapsed, exit |
| Q20 | NOT MET | No option list or config keys; "configured" values unnamed |
| Q21 | MET | §6 "Claim later reads public issue text"; activation blocked |
| Q22 | MET | §6 and §10 block activation pending verified session policy |
| Q23 | MET | FR-006 fail closed; §9 host validation of Project-read scope |
| Q24 | MET | §7 multiple workspaces per login unsupported; §10 one authority |
| Q25 | MET | NFR-004 persist next-permitted time, no busy retry |
| Q26 | MET | FR-006 incomplete pagination blocks; §8 tests full-page ambiguity |
| Q27 | MET | §3 approval requires non-bot account type |
| Q28 | MET | §7 crash between commit and submission suppresses, accepted |
| Q29 | MET | FR-008 pre-launch refresh; §7 exclusive cycle lock |
| Q30 | MET | FR-005 removal then unauthorized reapplication fails |
| **Total** | **26/30** | |

### Variant D (CEV)

| # | Verdict | Evidence |
|---|---|---|
| Q1 | MET | §3 Own login, Tagged, Approved, In a Project, Backlog, Intended owner, Claimed, Eligible |
| Q2 | MET | §7 schema lists six states; transitions table with "Launch allowed" |
| Q3 | MET | §8 modules, `once` options, `status` (FR-021), tests, design doc with runbook |
| Q4 | MET | §9 FU-1 live test, FU-2 Coder cron, FU-6 session permissions |
| Q5 | MET | §10 OD-1..OD-9 with defaults |
| Q6 | MET | NG-2 GET only; NFR-002 read-only argv test |
| Q7 | MET | FR-012 rejects `"9"`, `True`, `0`, `-1`, `10**9`, `9.0` |
| Q8 | MET | FR-013 exact 12-element argv with `--agent claude` |
| Q9 | MET | §7 `pending_orphan` and `unknown_expired` go `abandoned`; `launches < max_launches` |
| Q10 | MET | No internal contradiction found |
| Q11 | MET | 12 numbered H2 sections in order |
| Q12 | MET | FR-001..021, NFR-001..013, T1..T12, OD, R, FU IDs |
| Q13 | MET | Every FR carries a GWT line |
| Q14 | MET | §12 requirement-to-source table |
| Q15 | MET | §11 table: Likelihood / impact, Mitigation |
| Q16 | MET | Header convention; [PROPOSAL] on every unfixed number |
| Q17 | MET | §8 exit-code table with operator action |
| Q18 | MET | FR-003 exact `gh issue list` argv |
| Q19 | MET | NFR-006 lists `ts, cycle_id, host, login, exit_code, ...` |
| Q20 | MET | §8 `once` options with defaults |
| Q21 | MET | T1 residual: claim reads text live in PUBLIC repo |
| Q22 | MET | T10; OD-7 default interactive, never bypass |
| Q23 | MET | R2 runbook pre-flight `gh auth refresh -s read:project` |
| Q24 | MET | T7; OD-8 one workspace per login |
| Q25 | MET | NFR-9 rate-limit reply ends cycle, exit 3 |
| Q26 | MET | FR-004 exactly 100 fails closed, exit 4 |
| Q27 | MET | §3 Approved (d) `actor.type` is `User`; T3 |
| Q28 | MET | §7 `pending` found at start becomes `abandoned` `pending_orphan` |
| Q29 | MET | FR-011 pre-launch re-read; FR-017 `fcntl.flock` |
| Q30 | MET | FR-006 approver-labeled, outsider-unlabeled, outsider-labeled skipped |
| **Total** | **30/30** | |

### Variant E (CEV)

| # | Verdict | Evidence |
|---|---|---|
| Q1 | MET | §3 own login, tagged, approved, in a Project, Backlog, intended owner, eligible |
| Q2 | MET | §7 six-state table plus Transitions paragraph |
| Q3 | MET | §8 modules, `once/status/check-config/reset`, tests, design doc with setup |
| Q4 | MET | §9 cron entry, owner-run live launch test, permission-mode decision |
| Q5 | MET | §10 O-1..O-8 with defaults and reasons |
| Q6 | MET | FR-021 no GitHub write; §2 D2 |
| Q7 | MET | FR-013 rejects `"12"`, `12.0`, `True`, `0`, `-3`, `10**9` |
| Q8 | NOT MET | FR-014 `--agent <agent>` instead of fixed `claude` (X-008) |
| Q9 | MET | §7 lease-expired `pending` resolves to `unknown`; no id goes `abandoned` |
| Q10 | NOT MET | FR-010 vs FR-017 claimed condition; NFR-013 pruning vs §7 `reset`; §2 vs FR-001 |
| Q11 | MET | 12 numbered H2 sections in order |
| Q12 | MET | FR-001..023, NFR-001..014, O, R IDs |
| Q13 | MET | Every FR has an AC with Given/Then |
| Q14 | MET | §12 table with RF/RQ/SB keys |
| Q15 | NOT MET | §11 bullet list; no likelihood/impact; R-2, R-3, R-7 lack mitigations |
| Q16 | MET | Front matter `tags_used`; §7 parameters [PROPOSAL] |
| Q17 | MET | FR-023 exit codes 0, 2-8 |
| Q18 | MET | FR-002 exact `gh issue list` flags |
| Q19 | MET | NFR-007 audit keys listed |
| Q20 | MET | §3 named config values; §7 parameters; `check-config` verb |
| Q21 | MET | §6 Launched session: "Stated, not solved" |
| Q22 | MET | O-6 no override; live test before cron |
| Q23 | MET | FR-009 fail closed exit 3; O-3 option D before label-only |
| Q24 | MET | §6 Duplicate claim row; O-4 one poller per login |
| Q25 | MET | NFR-006 403/429 stops calls, exit 8 |
| Q26 | MET | FR-003 exactly 100 items fails closed, exit 4 |
| Q27 | MET | FR-007 `type=Bot` rejected |
| Q28 | MET | NFR-004 fault injection between FR-011 and FR-015 |
| Q29 | MET | FR-012 pre-launch re-read; FR-019 exclusive lock |
| Q30 | MET | FR-006 labeled then unlabeled is not approved |
| **Total** | **27/30** | |

## Qualitative Summary

| Variant | Completeness /5 | Correctness /5 | Structure /5 | Clarity /5 | Risk /5 | Edge cases /5 | Met /30 | qual |
|---|---|---|---|---|---|---|---|---|
| A | 5 | 3 | 5 | 5 | 5 | 5 | 28 | .933 |
| B | 5 | 3 | 5 | 5 | 4 | 4 | 26 | .867 |
| C | 5 | 4 | 4 | 3 | 5 | 5 | 26 | .867 |
| D | 5 | 5 | 5 | 5 | 5 | 5 | 30 | 1.000 |
| E | 5 | 3 | 4 | 5 | 5 | 5 | 27 | .900 |

## Edge-case floor check

Floor is 1/5 on dimension 6 (Q26 to Q30). A 5, B 4, C 5, D 5, E 5. All five are eligible.

## Position-Bias note

This is pass 1 (forward order A, B, C, D, E). The pass-2 (reverse) verdicts were not consulted. The orchestrator reconciles the two passes and re-evaluates any criterion where they disagree.

## Combined Scoring

final = .5 quant + .5 qual

| Variant | quant | qual | final | Rank |
|---|---|---|---|---|
| A | .983 | .933 | .958 | 2 |
| B | .987 | .867 | .927 | 4 |
| C | .974 | .867 | .920 | 5 |
| D | .990 | 1.000 | .995 | 1 |
| E | .978 | .900 | .939 | 3 |

## Margin and tiebreaker

- Top two: D .995, A .958. Margin .037, under the 5% threshold, so the tiebreaker applies.
- Level 1, debate wins (single-letter winners in `round2-tally.md`): D 6 (C-017, C-018, X-001, X-002, X-003 open, X-005 open), C 2 (C-011, X-004), A 1 (C-021), B 1 (S-007), E 1 (C-003). D wins at level 1; levels 2 and 3 are not needed.

## Selected Base: Variant D

Rationale: highest combined score (.995), the only variant with 30/30, the only variant meeting both Q9 (no relaunch after an ambiguous or lost launch) and Q10 (no internal contradiction) alongside the exact launch argv (Q8), and the most debate wins.

Strengths to preserve from D:
- operator runbook in the design doc (§8)
- at-most-once `launches < max_launches` counter (§7)
- `pending_orphan` and `unknown_expired` resolving to `abandoned` (§7)
- kill switch and disabled-by-default activation (OD-2, OD-7)
- exit-code table with operator action (§8)
- SLO and audit signals (NFR-006)

Strengths to incorporate from other variants:
- C: node-ID and account-ID identity in definitions (§3); alternatives scoring table (§2)
- E: per-issue `projectItems` query to avoid the 100-item Project limit (FR-008, §5); daily launch cap (FR-018)
- A: `check-config` verb and stage seams (§8)
- B: `orca-cli` probe (FR-014); `origin` remote check (FR-002); root-cause table (§1.1)
