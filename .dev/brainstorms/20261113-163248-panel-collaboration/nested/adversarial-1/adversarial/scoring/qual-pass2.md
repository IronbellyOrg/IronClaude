# Qualitative scoring, pass 2 (reverse order)

Evaluation order: V5, V4, V3, V2, V1. Strictness notes: RK1 needs at least 3 risks that each carry a probability and an impact; RK2 needs a mitigation on every listed failure mode (a per-failure "Action"/"Fix" column or equivalent); CP5 is accepted when the document states explicit exclusions or deferrals (no variant has a dedicated out-of-scope heading).

## V5

| Criterion | Verdict | Evidence |
|---|---|---|
| CP1 | MET | Sections 2.1-2.5 each have (b) schedule, (c) transport, (d) time table, (e) safeguards, (f) gain by issue (design 2 table B5, I1, I5, B1, B2, I4, B6, B8, I6, I7); Section 1 three theories; Section 4 first experiment. |
| CP2 | MET | Each design has (h) Failure modes, e.g. "ember posts after luna's call 6 and no one receives it: the harness logs 'no delivery' and the run counts as isolated". |
| CP3 | MET | "Spikes first (about half a day, no scoring)" and "Known unverified items (resolve before relying on any number above)"; H-1..H-6 harness preconditions. |
| CP4 | MET | Section 4 "Decision rule (set before running). Adopt arm X only if all hold..." five numbered conditions; E-4. |
| CP5 | MET | B-1 "No cross-session messaging, Orca mail or A2A in the first experiment"; "Designs 1 and 5 are deferred"; "grok is excluded: 790 s median". Weak: no dedicated heading. |
| CR1 | MET | Baselines 348/715/821 s match brief; per-package 116/238/274 s stated as divided by 3; c-sum 1.04 recomputes (0.05+0.05+0.125+0.075+0.2+0.185+0.215+0.14); "ember 81 of 209 = 39%" and "luna 49 of 222 = 22%" check; design 1 gain 0.21 recomputes. |
| CR2 | MET | "Hooks run in `-p` sessions unless `--bare`"; "`--max-turns`... not listed, so turn caps must come from a hook counter and `timeout`"; reviewers stay read-only. |
| CR3 | MET | Move codes G1-G8, arms A0-A5, EL2/HL2/SL2 used uniformly throughout. |
| CR4 | MET | Time arithmetic consistent ("116 + 27.0 = 143 s ... +23.3%"; "116 + 33.4 = 149.4 s ... +28.8%"); effort figures reconcile (130 shared + 40 = about 170). |
| CR5 | MET | Each gain gives its assumption chain ("a = 0.7", "q = 0.6 for 3 turns or fewer") and 2.0.6 lists five labelled assumptions. |
| ST1 | MET | Order: theories, shared substrate, designs, comparison, experiment, requirements. |
| ST2 | MET | Each design uses identical (a)-(h) sub-structure; no orphan sections. |
| ST3 | MET | Harness-fix share (2.0.6 table) separated from collaboration; requirements split into H, B, S, C, D, E groups. |
| ST4 | MET | Evidence-path short-name table (CR, HO2, INV-DS...), requirement IDs H-1, C-3, D4-1, theory-to-issue table. |
| ST5 | MET | Section 5 tables "ID / Requirement / Test" with thresholds (H-1 "at least 98% of runs"). |
| CL1 | MET | Quantified caps and schemas ("Nothing is injected ... before its 6th tool call"; size caps in S-2). |
| CL2 | MET | Concrete JSON schema v1, hook behaviour, arm run counts (12/6/12), cost 540 reviewer runs. |
| CL3 | MET | "Lens" line, 2.0.x substrate items and "Reading the table" give each section a clear purpose. |
| CL4 | MET | "Issue labels follow CR:401-417. DS = designSpec package..., AL..., DE..."; "hard ten" defined; "What c means" defined. |
| CL5 | MET | Spikes list, arms, interim look; "If no exchange arm passes but A2 beats A1 by at least 0.25 on hard credits, adopt A2 alone". |
| RK1 | NOT MET | Failure modes carry few numbers ("luna ignores the wrapper (a about 0.3 chance)", ember skips source.md 39%); no systematic probability and impact for 3+ risks, only Low/Medium ratings. |
| RK2 | NOT MET | Mitigations only for some: "the hook adds a one-line reminder at call 6", "guard with `timeout 95`"; design 1 and design 4 (h) lists ("The model omits or mangles the `moves:` line", "A non-Claude model ignores the block reason") have none. |
| RK3 | MET | "Results can arrive after the requester has finished: counted as lost, not retried"; "any run with an API error is quarantined and re-run once"; late phase-2 work dropped. |
| RK4 | MET | "hooks inheriting the board path, additionalContext reaching gateway models, Stop-hook blocks in -p mode, and --resume with gateway ids are untested"; spikes 1-3. |
| RK5 | MET | Convergence alarm (Jaccard 0.70, echo rate 30%, easy-issue share), C-4 `convergence-alarm.py`, interim look at 6 runs. |
| IV1 | MET | Index "up to 12 entries"; "no delivery" path; "baseline hard credits are 0 in 30 runs; with 12 runs, 4 or more ... Fisher p about 0.04"; caps in S-2/S-3. |
| IV2 | MET | "session storage is tied to the working directory (/tmp/evalsb/repo)"; `stop_hook_active` guard; resume requires dropping `--no-session-persistence`; board log "never given to the judge". |
| IV3 | MET | S-1 "drops and logs any that fail it or whose `note` contains a verdict word"; "model omits or mangles the `moves:` line"; B-3 jq validation. |
| IV4 | MET | "per-package figures are the three-package figures ... divided by 3, so confirm"; "A 15 s wait would add 15 s and break the cap (48.4 s = +41.7%)"; /14 vs control /2 split ("Nine are in the 14 defect-rich issues"). |
| IV5 | MET | Harness vs prompting vs collaboration shares (E-5); A2 static kit control; "design 1's value is mostly in A2 plus A4". |

Subtotals: CP 5/5, CR 5/5, ST 5/5, CL 5/5, RK 3/5, IV 5/5, total 28/30

## V4

| Criterion | Verdict | Evidence |
|---|---|---|
| CP1 | MET | Five redesigns each (a)-(h) with schedule, transport, time table, safeguards, gain table per issue; Section 1 three theories; Section 4 first experiment. |
| CP2 | MET | Per-design "Failure modes and runbook" tables, e.g. "Digest empty (ember produced only surface findings) | challenges = 0 | Logged; the package behaves as isolated". |
| CP3 | MET | "Gate 0 (must pass before any arm runs)" spikes S0/S2/S3; 5.1 harness preconditions R-01..R-05. |
| CP4 | MET | "Pre-registered decision rule" five criteria plus Outcomes table; R-24 SLO. |
| CP5 | MET | "Grok is used in no design"; "Transports rejected for every design"; Redesigns 1, 4, 5 "deferred"; closing "Not checked in this specification". Weak: no dedicated heading. |
| CR1 | MET | Baselines 116/100/225/238 s match CR/3 and 348/715; sums recompute (Redesign 1 low 0.20 / high 0.88; Redesign 3 0.23 / 0.94); overhead % recompute (144/116 = +24%, 253/225 = +12%). |
| CR2 | MET | Hooks via `--settings`, helpers write only under `$BOARD`, `--disallowedTools Edit Write NotebookEdit` unchanged (R-09). |
| CR3 | MET | M1-M10, `panel-msg/1`, "seal", A0-A3, R-xx used consistently. |
| CR4 | MET | Catches its own overrun: "45 s timeout guaranteeing at most 161 s (+39%)... The overrun guard is therefore a hard 35 s" and R-15 matches (35 s luna, 45 s ember). |
| CR5 | MET | Gain models state chains ("P = P(a peer anchors the right sentence) x ... 0.5-0.6 x 0.3-0.6") with file:line sources. |
| ST1 | MET | Theories, building blocks, designs, comparison, experiment, requirements. |
| ST2 | MET | Uniform (a)-(h) per redesign; sections 5.1-5.6 grouped. |
| ST3 | MET | Shared 2.0 blocks and H-share separated from per-design material. |
| ST4 | MET | Path abbreviations (EVAL, BS, CR, HO2), move IDs, R-01..R-30, spike IDs S0/S2/S3. |
| ST5 | MET | Section 5 tables with Id / Requirement / Verification. |
| CL1 | MET | Fixed caps ("at most 600 bytes", "no delivery after t = 125 s"); explicit forbidden fields. |
| CL2 | MET | Full JSON schema, per-reviewer arithmetic, "4 replicates per arm x 3 packages = 48 package-runs". |
| CL3 | MET | Devops-framing list (target, kill switch, audit trail, alarms, runbook) gives each section a purpose. |
| CL4 | MET | Path abbreviations defined; "found /14" vs "control /2" defined; S07/S13/S14/S24 mapped to panels in the baseline table. |
| CL5 | MET | Outcomes table: "Both A2 and A3 pass 1-5 | Run a 6-run confirmation...", abort rule, Gate 0. |
| RK1 | NOT MET | Failure tables give detection and action but no probability/impact; closing "Risks:" lists two items without probability. |
| RK2 | MET | Every failure row has an Action column ("Fresh-session fallback (logged `resume_fallback`)"). |
| RK3 | MET | "Phase-1 lines are immutable by construction"; "On timeout the phase-1 report is the final report"; kill switch `PANEL_COLLAB=0`. |
| RK4 | MET | Hook firing on gateway models, `--resume` on gateway, hook timeout UNVERIFIED with spikes; "Project hooks in the sandbox's tracked `.claude/settings.json` also fire". |
| RK5 | MET | R-23 `collab.json` fields, R-25 alarms CONVERGENCE/ECHO/SEAL, R-24 SLO_BREACH. |
| IV1 | MET | "Digest empty ... challenges = 0"; "cards_sent = 0"; caps "at most 4 facts", "luna 2, ember 3"; `seal_missing` when no seal by call 10. |
| IV2 | MET | Seal-before-delivery, "Two blocks in one report (parser uses the last)", session storage growth, resume cwd `/tmp/evalsb/repo`. |
| IV3 | MET | R-06 "claim, severity, blocking and category ... rejected"; R-02 lists anchor 12-200, claim over 300, id over 16; R-22 hooks never fail the reviewer. |
| IV4 | MET | "Critical path 148 s: +28%, with the 45 s timeout guaranteeing at most 161 s (+39%)"; R-24 "1.35 x ... exceeding 1.5x raises SLO_BREACH"; /14 vs control /2 split. |
| IV5 | MET | "Moves M4 and M6 only pay off once H1 and H3 hold"; "H4 lowers measured I7 for sonnet panels"; A1 catalogue-only arm separates prompting from collaboration. |

Subtotals: CP 5/5, CR 5/5, ST 5/5, CL 5/5, RK 4/5, IV 5/5, total 29/30

## V3

| Criterion | Verdict | Evidence |
|---|---|---|
| CP1 | MET | R1-R5 each (a)-(h) with schedule, transport, time, contamination, gain targets ("Targets: I7 (M2), B8 (M3), I5 (M5), B5 (M1), I4 (M4)"); Section 1 theories; Section 4 experiment. Gain is one low-high number per design, not per issue. |
| CP2 | MET | (h) Failure modes per design, e.g. "Ember exits before the challenge arrives". |
| CP3 | MET | "Pre-condition (not optional). Apply the harness fixes first"; UNVERIFIED flags on resume and hook env. |
| CP4 | MET | Section 4 decision rule: Adopt/Extend/Reject; requirement 20. |
| CP5 | MET | "R3, R4 and R5 are deferred"; "Haiku ... and grok alone break the +35% cap. Glm and Qwen are excluded"; "Harness fixes (separate from all five designs, not collaboration)". Weak. |
| CR1 | MET | Legend counts match brief (B3 68, I8 56, I2 52, I7 9, I1 3, I4 4, B8 1); 116 s = 348/3; R1 "102 + 14 + 3 + 30 = 149 s ... +28%" recomputes. |
| CR2 | MET | `--disallowedTools` kept; R3 truncation acknowledged ("130 s cap truncates most sonnet runs"). |
| CR3 | MET | R1-R5, M1-M6, A0-A2 consistent. |
| CR4 | MET | No clear contradiction; slight tension between R1 "complete replacement findings-v1 block" and requirement 6 "separate section outside the fenced block", reconcilable. |
| CR5 | MET | Gains carry "Assumptions: P(move run) 0.6 to 0.9; P(issue found | move run) 0.15 to 0.4" and T1/T2 evidence quotes; thin but present. |
| ST1 | MET | Theories, designs, comparison, experiment, requirements. |
| ST2 | MET | Uniform (a)-(h); numbered requirements 1-21. |
| ST3 | MET | Harness fixes separated from the five designs; legend separate from theories. |
| ST4 | MET | Legend table with IDs, M1-M6, R1-R5, A0-A2, numbered requirements, source line references. |
| ST5 | MET | Section 5 "Numbered, testable requirements" each with "Test:". |
| CL1 | NOT MET | Baseline basis left ambiguous: "If the 348 s figure is a per-package figure instead, every budget here is conservative"; tokens reported "per panel run" next to per-package seconds. |
| CL2 | MET | Concrete JSON `{"from":"ember","move":"M2","scope":"repo_wide","status":"ran"}`, line caps, run counts 10/10/10. |
| CL3 | MET | Section headings and "Legend (plain meaning of each defect...)" give purpose. |
| CL4 | NOT MET | "GT10", "GT5", "DE runs", "COMBO-REPORT R14", "HANDOFF D1" used undefined (e.g. "16 findings anchored the GT10 CHANGELOG-adjacent Task 2 grep sentence"). |
| CL5 | MET | Decision rule with Extend to 20 runs; hold-out package before adoption (requirement 21). |
| RK1 | NOT MET | Failure modes listed without probabilities or impacts; only Low/Medium/High reliability labels in Section 3. |
| RK2 | NOT MET | (h) lists failures only ("Resume fails for gateway ids (UNVERIFIED), so phase 2 silently becomes no-op"); no mitigation per failure. |
| RK3 | NOT MET | Failure modes named but no recovery path for R1, R2, R3, R5; only requirement 16 excludes fallback runs. |
| RK4 | MET | "UNVERIFIED: resume with gateway model ids"; "held messages expire after 5 minutes"; "`ListAgents` shows every local session". |
| RK5 | MET | Requirement 11 leak check "hard failure", requirement 12 convergence alarm, double-scored sample. |
| IV1 | MET | "the board is silently empty"; "Injection arrives after the last tool call"; max messages 4 / 3; power at 10 runs per arm. |
| IV2 | MET | "Seal before release ... timestamp earlier than the first peer line"; "Session expiry between phases"; unique names for ListAgents. |
| IV3 | MET | Requirement 7 "any other field is rejected"; requirement 8 caps "rejected, not truncated"; 12-character leak substring check. |
| IV4 | NOT MET | Count basis mismatch unresolved (116 s per package vs 63.6k tokens "per panel run"; "if the 348 s figure is a per-package figure instead"); no inclusive/exclusive or rounding handling. |
| IV5 | MET | "Overlap with collaboration assumed at 20%" between harness fixes and collaboration; A0 fixed-harness arm. |

Subtotals: CP 5/5, CR 5/5, ST 5/5, CL 3/5, RK 2/5, IV 4/5, total 24/30

## V2

| Criterion | Verdict | Evidence |
|---|---|---|
| CP1 | MET | D1-D5 each (a)-(h) incl. per-issue gain tables (D1 I5, B8, B6, I7; D2 I5, B1, I4, B5...); Section 1 Theories A, B, C; Section 4 first experiment. |
| CP2 | MET | Per-design (h) failure modes, e.g. D1 "The hook does not receive the board path: no delivery, and the run behaves as isolated (fails closed)". |
| CP3 | MET | "Harness fixes (prerequisites, H)"; "Spike S0 (gate for A3 and A4...)". |
| CP4 | MET | Section 4 pre-registered decision rule 1-5 with Fisher test ("4/6 vs 0/6 gives p = 0.030"). |
| CP5 | MET | "D3-D5 are deferred"; "No Opus or sonnet reviewer takes part"; closing "Not checked by this variant". Weak. |
| CR1 | MET | Baselines 116/238/274/225 s match CR/3; "ember 81/209 = 39%"; Fisher 4/6 vs 0/6 = 15/495 = 0.030 correct; overhead % recompute (150/116 = +29%, 300/274 = +10%). |
| CR2 | MET | Reviewers keep read-only and hooks fail closed (R-22); D3 transport flagged UNVERIFIED and ranked "Low-medium". |
| CR3 | MET | M1-M9, `panel-msg/1`, D1-D5, A0-A4, H/C shares used consistently. |
| CR4 | MET | Only a trivial mismatch ("claim ... to 297 characters" in H2 vs "at most 300" in R-2), compatible. |
| CR5 | MET | Gain rows give path chains with probabilities ("ember M6 finds CHANGELOG.md:166 (0.3-0.6), luna or ember reports it (0.3-0.5)") and "Weakens it" counter-evidence in the theories. |
| ST1 | MET | Theories, building blocks, designs, comparison, experiment, requirements. |
| ST2 | MET | Uniform (a)-(h) design blocks; Section 1 subsections 1.0-1.4. |
| ST3 | MET | Harness (H) vs collaboration (C) kept in separate columns; requirement groups by design. |
| ST4 | MET | R-1..R-28, M1-M9, D1-D5, "Gate A/B/C" table, ENR source sections. One wrong cross-ref (D1 says "requirement R-20" for the spike, but R-20 is the Stop-hook rule). |
| ST5 | MET | Section 5 bold R-n requirements each with "*Test:*". |
| CL1 | MET | Formulas make rules exact ("min(2, floor((150 - t_stop - 12) / 11)) locators"; R-20 tests at 100/125/140 s). |
| CL2 | MET | Catalog sentences quoted verbatim; schema field table; exact arm run counts (6/6/6/6/4). |
| CL3 | MET | Section 1.0 method (exposure, question, survival gates) explains the structure of the theories. |
| CL4 | MET | Header defines EVAL/ENR/CR, "Found /14", GT mapping; CI and claim echo defined in the common alarm paragraph; "Natural seal" defined. |
| CL5 | MET | "If only A2 passes 1-3 against A1, adopt the static catalog and stop"; "X goes to a 12-run confirmation on at least two new packages". |
| RK1 | NOT MET | Failure modes without probability and impact; only a few numbers ("ember skipped source.md in 39% of runs"). |
| RK2 | NOT MET | D3 (h) lists "Gateway models misname peers or never send ... No durable log. ... haiku overruns the cap." with no mitigation; D4, D5 similar. |
| RK3 | MET | R-15 "on timeout, an invalid block or a missing findings-v1 block, the phase-1 report is used"; R-21 fallback to last assistant message; fail-closed hooks (R-22). |
| RK4 | MET | "UNVERIFIED: whether the hooks receive the board path, and whether a Stop block in `-p` mode yields a reissued full report"; `--resume` with gateway ids; Spike S0. |
| RK5 | MET | R-24 CI and claim echo vs A1 reproducing 0.25; R-23 board-access audit; alarm firing "in at most 1 of 6 runs". |
| IV1 | MET | "a luna that stops at 135 s or later gets none"; R-20 tests 100/125/140 s giving 2/1/0 locators; "no board, no seal or an invalid line" delivers nothing. |
| IV2 | MET | R-11 seal timestamp precedes first delivery; R-12 session persistence; "resumed session re-runs the /sc:spec-panel skill prompt: the phase-2 prompt must not start with a slash command". |
| IV3 | MET | R-8/R-9 validator (quote verbatim in candidate/source, path exists), forbidden keys, R-16 id-loss check. |
| IV4 | MET | Stop-time guard floor arithmetic; "p = 0.030" check; "+29% expected with worst +34%" kept under 35%; "(H2) claim ... to 297 characters". |
| IV5 | MET | R-28 "Gains are reported as H (A1 - A0), catalog content (A2 - A1), communication (A3 or A4 minus A2)"; "D5 depends on H1" and shares D1 infrastructure. |

Subtotals: CP 5/5, CR 5/5, ST 5/5, CL 5/5, RK 3/5, IV 5/5, total 28/30

## V1

| Criterion | Verdict | Evidence |
|---|---|---|
| CP1 | MET | R1-R5 each (a)-(h) with schedule table, transport, time table, safeguards, per-issue gain tables; Section 1 three theories with issue-to-theory map; Section 4 first experiment. |
| CP2 | MET | (h) Failure modes per design, e.g. "ember's map is so late that the lunas have finished"; "Weaker models skip posting cards. Then there are no gaps and R1 behaves like the isolated panel." |
| CP3 | MET | "5.1 Preconditions (spikes; each must pass before arms A3 or A4 run)" REQ-S1..S3; REQ-H1..H6. |
| CP4 | MET | Section 4 decision-rule table with p-values and guard conditions; REQ-E1..E4. |
| CP5 | MET | "The grading-rule problem ... is held constant"; R1, R4, R5 not in first experiment; closing "What I skipped or did not check". Weak. |
| CR1 | MET | 116/238/274 s = CR/3; issue-found counts match brief ("B5 3, I1 3, I4 4, I5 0, I7 9 (7 clean)"); totals recompute (1.83 + 0.10 + 0.2 = 2.1; 233 + 2 + 46 = 281 = +18%; 274 + 56 = 330 = +20%). |
| CR2 | MET | Hooks via `--settings`; RR:48 `--no-session-persistence` must be dropped for resume; R3 hard guard "`1.35 x T1 - 2 s`" via `timeout`. |
| CR3 | MET | M1-M10, panel-msg/1, panel-card/1, A1-A4, REQ-* used consistently. |
| CR4 | MET | Minor dangling reference ("listed as follow-up work in section 4" while section 4 has no such list) but no real contradiction in numbers or design. |
| CR5 | MET | Every gain row states its assumption ("P(test file in haiku output) 0.45 (5/11); P(luna opens it when injected) 0.7") and source line refs (INV-PAT:43-45). |
| ST1 | MET | Theories, scaffolding, designs, comparison, experiment, requirements. |
| ST2 | MET | Consistent 2.1-2.5 (a)-(h) hierarchy; 5.1-5.7 requirement groups. |
| ST3 | MET | Shared scaffolding (2.0) separate from policies; harness share separated in each gain table. |
| ST4 | MET | Evidence-key table, REQ-S/H/C/X/B/M/A/E IDs, move IDs, file:line cites. |
| ST5 | MET | Section 5 tables "Id / Requirement / Test" with measurable pass conditions. |
| CL1 | MET | Exact formulas and caps ("PANEL_FINISH_AT = T0 + 1.20 x B"; "at most 3 cards"; 200 bytes). |
| CL2 | MET | Sample JSON envelope, effort tables by file with lines, arm counts "24 panel-runs, 216 reviewer runs and 72 blind judge calls". |
| CL3 | MET | Each section states role (e.g. 2.0 "built once; every design below is a policy on top of it"). |
| CL4 | MET | Header defines issue labels and GT mapping, "Found /14", `J`, H1-H4, S07/S24 tied to panels. |
| CL5 | MET | Decision table incl. "If A2 already matches A3 within 0.25, ship the static catalogue"; "Stop early" rule. |
| RK1 | NOT MET | Failure modes without probability and impact pairs; only reliability labels (Medium/Low) in the comparison table. |
| RK2 | NOT MET | R5 (h) lists "luna never sends", "Held messages expire after 5 minutes", "Session names collide", "It only works on one machine" with no mitigation; several R-design lists give none. |
| RK3 | MET | REQ-B7 "the hook prints nothing and exits 0 (the review continues isolated)"; "Phase 2 is killed at the cap ... phase-1 report stands"; fail-open noted. |
| RK4 | MET | REQ-S1..S3 spikes for resume, hook env, injection; "luna calls `SendMessage` correctly through the gateway" UNVERIFIED. |
| RK5 | MET | Convergence alarm J, echo rate, tunnelling alarm (REQ-B6), `board-audit.py` (REQ-A1). |
| IV1 | MET | "at least one card per reviewer is a gap card when any unanchored region exists" (REQ-X4); missing board directory (REQ-B7); "46 unanchored rows ... skip those findings". |
| IV2 | MET | "parser treats more than one block as invalid (HO2:336)" handled by `combine-blocks.sh`; resume keeps `expected_model`; "one board per package" so per-sandbox paths don't mix. |
| IV3 | MET | REQ-X3 schema validation of every card; REQ-B7 fault injection: corrupt line; REQ-A3 schema-invalid -> EXCLUDE. |
| IV4 | MET | "Total elapsed is therefore at most 1.35 x T1"; "finish signal 139 s plus at most 17 s ... 156 s or less"; "+34.5% hard; expected ~150 s = +29%". |
| IV5 | MET | Arm A2 isolates catalogue effect from exchange; "R2 and R3 ... share no transport parts, and can be tested as separate arms"; H4 effect on sonnet I7 credits. |

Subtotals: CP 5/5, CR 5/5, ST 5/5, CL 5/5, RK 3/5, IV 5/5, total 28/30

## Summary

| Variant | CP | CR | ST | CL | RK | IV | Total /30 |
|---|---|---|---|---|---|---|---|
| V5 | 5/5 | 5/5 | 5/5 | 5/5 | 3/5 | 5/5 | 28 |
| V4 | 5/5 | 5/5 | 5/5 | 5/5 | 4/5 | 5/5 | 29 |
| V3 | 5/5 | 5/5 | 5/5 | 3/5 | 2/5 | 4/5 | 24 |
| V2 | 5/5 | 5/5 | 5/5 | 5/5 | 3/5 | 5/5 | 28 |
| V1 | 5/5 | 5/5 | 5/5 | 5/5 | 3/5 | 5/5 | 28 |

Ranking by total: V4 (29), V5 = V2 = V1 (28), V3 (24). Main separators: V4 is the only variant with a per-failure action column (RK2); V3 loses on undefined shorthand (GT10, DE), the unresolved per-package vs per-panel baseline, and bare failure lists; no variant presents a probability-and-impact risk register (RK1 NOT MET for all five).
