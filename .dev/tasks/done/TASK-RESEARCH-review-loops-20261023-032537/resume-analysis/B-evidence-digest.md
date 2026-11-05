# B — Evidence Digest (review-loop investigation)

**Status:** Complete (read-only digest of existing research; no new log analysis)
**Date:** 2026-10-23
**Workspace root** (relative paths below): `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/`
**Sources read in full:** research/research-notes.md, research/session-manifest.txt, research/scope-rules.md, research/historical-review-rules.json, research/01..06-session-*.md, research/evidence-deck.md, gaps-and-questions.md, BUILD-REQUEST.md. Also read: qa/qa-consolidated-findings-phase3.md, qa/phase3-fix-log.md, qa/phase3-fix-verification.md (for section 3).

**Anchor convention:** "raw N" = physical line N of the original session JSONL, as the case analysts reported it. This digest did NOT re-open the session JSONLs; every raw anchor is **UNVERIFIED by this digest** (it was verified by the case analysts and, for six items, by the Phase-3 QA gate). Protocol file paths and line ranges in section 4 WERE re-checked directly by this digest.

**Counting rules** (evidence-deck.md:11-13): a session, an incident, a failed review and a transition are different counts. The population is 30 frozen logs; manifest index 03 is this investigation and is excluded. Seven of the 30 are synthetic, several never invoke the target command, and the six selected cases are **not** a prevalence rate (evidence-deck.md:53, :173).

---

## 1. The six cases

Short names for the causal classes: **FIR** = regression caused by a fix; **PMD** = defect that already existed but was found later; **UB** = blocker that stayed unchanged, or a prior finding not actually fixed; **RC** = review rule changed mid-run; **INV** = invalid or unsupported finding; **OTH** = other.

| # | Session id | Project path | Original log path | Workflow / Implement | Loop shape | Classes found |
|---|---|---|---|---|---|---|
| 1 | `ac2cd1fd-60f6-4b7c-942c-93026ea8edce` (manifest 20) | `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking` | `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-orca-upstream-tracking/ac2cd1fd-60f6-4b7c-942c-93026ea8edce.jsonl` | **Workflow** (plan + advisory `reflect pre`) | v1 → full review 16 findings `partial` (raw499) → v2 whole-file Write (raw544) → full review 20 items `partial` (raw821) → v3 (raw841) → targeted 1-reviewer `PARTIAL` (raw874) → 15 Edits = v4 (raw906-934) → "NOT CHECKED: v4 has had no review since this edit" (raw946) | FIR, PMD, UB, INV, OTH (contradictory source) |
| 2 | `a9b88895-5374-4cae-8ebb-cac03a97aff1` (manifest 27) | `/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate` | `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-auggie-claim-gate/a9b88895-5374-4cae-8ebb-cac03a97aff1.jsonl` | **Implement** per-task QA (Task 12, managed package TASK-WF-designV2-20261020-132032) | FAIL 4 findings (raw291) → repair limited to findings 1-3, frozen fixture excluded (raw383) → FAIL, 3 confirmed fixed, #4 kept (raw450) → operator authorizes fixture fix (raw521) → one boolean + hash + assertion → PASS (raw668) | PMD (3, repaired), UB (frozen fixture). No FIR, no INV |
| 3 | `6f744b87-6508-4d3e-9e71-c1193fd2162d` (manifest 01) | `/config/workspace/Coder/.claude/worktrees/issue-358-litellm-key-env` | `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/6f744b87-6508-4d3e-9e71-c1193fd2162d.jsonl` | **Implement** per-task QA + managed FINAL (TASK-WF-issue358FollowUp-20261022-210638) | Task 6: `cannot-verify` (raw430) → evidence-only patch, "No text change was needed" (raw443) → `cannot-verify (unchanged)` (raw450) → halt `head-moved` because the q0-head file was never written (raw485-486) → user says "t7" by mistake (raw498), executor refuses (raw503), user "accept t6" (raw506) → FINAL pass that keeps the unmet clause (raw527) → archived (raw531). Task 2 (control): `extra` (raw204) → diff narrowed → `compliant` (raw234) | UB (environment: `man` is a notice script); INV (Task 2 wrong baseline); OTH (false `head-moved` halt) |
| 4 | `43582de1-c41b-4b6a-806c-f19f1488095c` (manifest 04) | `/config/workspace/IronClaude/.dev/worktrees/ci-followup` (worktree of IronClaude) | `/config/.claude/projects/-config-workspace-IronClaude/43582de1-c41b-4b6a-806c-f19f1488095c.jsonl` | **Workflow** (plan + `reflect pre`; user-authorized regeneration) | Review #1: 18 merged concerns, 10 medium / 8 low (raw623) → user "refactor" (raw627) → feedback appended to source, new package (raw651-670) → review #2: final `not_ready`, 5 medium / 11 low / 0 high, status `partial` from 2 dropped citations (raw1036-1084, supplement at 04:02:04Z) → user decision pending; no implementation | FIR (dependency-graph ancestry); UB (tooling exemption on status but not hash; rename handling); PMD (search filters unchecked, overstrict "required" ban, stub confinement, half-edit header); INV (overclaimed allowlist severity, wrong rename-order advice, rejected literal-warning claim, matrix bookkeeping) |
| 5 | `e002bed2-7877-42c1-8665-8cb8595587b6` (manifest 05) | `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking` | `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-orca-upstream-tracking/e002bed2-7877-42c1-8665-8cb8595587b6.jsonl` | **Implement** per-task QA (Task 12, the same Orca plan as case 1) | One invocation. 7 verdicts (6 non-compliant, 1 compliant), 5 repair passes, 4 operator `fix` replies, no ladder/adviser/revert records. 640-line workflow (raw585) → `missing` (raw697) → fix → `missing` (raw804) → halt (raw817) → fix → `compliant` (raw849) → protocol changed mid-run, migration row P forces a fresh review (raw874-902) → `missing` ×3 (raw906, 1021, 1143) → `misunderstood` (raw1240), halt (raw1247). Later: human "accept these defects and proceed" (raw1250) → complete with the SAME `misunderstood` verdict (raw1260-1261) | PMD (most), FIR (one proven: stdout error-trap pollutes `P=$(...)`), UB (summary obligation found again on different boundaries), RC (mid-run protocol migration), OTH (reviewer prompt "any defect of any severity"; findings outside the plan's acceptance criteria) |
| 6 | `0690ee9f-c2f6-40ef-96be-1a0913a37866` (manifest 15) | `/config/workspace/Coder/.claude/worktrees/issue-358-litellm-key-env` | `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866.jsonl` | **Implement** managed FINAL (archive gate) | Package A (control, issue358InTempla-151058): FINAL issues (raw390) → evidence-only fix → FINAL pass (raw435). Package B (issue358FollowUp-193837, 17 tasks): FINAL #1 issues (nested a9c0…:135) → user "accept and fix" (raw1938) → FINAL #2 issues on a blank-line Task 10 citation (nested acf0…:116) → more evidence fixes (raw2015) → rubric changes on disk → FINAL #3 pass + archive (raw2036). Delivery digest unchanged throughout. FINAL #2 is missing from the ledger | PMD (Task 10 blank citation, wrong from creation at raw1425); UB/incomplete fix (Task 7 range 45-56 misses row 57); RC (qa.md changed between FINAL #2 and #3); OTH (task QA relaxed a literal criterion without the user's consent; durable proof lost) |

### Per-case notes (only what the table cannot hold)

- **Case 1.** The second review's "13 fixed / 3 partial" is wrong; its own detailed checklist shows **14 fixed / 2 partial** (M-04, M-09) (01-session-ac2cd1fd.md:90-97, :392-396). The 20 items are not 20 defects: N-02 is a duplicate and N-16 is labelled "a note, not a defect" (01:99-103). The input-snapshot source hash is the same in both reviews, so the extra findings were not caused by a changed spec (01:338). The loop stopped because the user reduced review scope, not because the plan converged (01:303-313).
- **Case 2.** Tests stayed green while reviews failed (67/78 → 74/85 → 74/85). Tests checked labels and counts, not meaning (02:220-246). A later archive refusal (raw824) was caused by a missing operator archive ruling. It was not a QA failure.
- **Case 3.** `/usr/bin/man` is a six-line minimized-image notice script; the first check threw away stdout and kept only rc=0 (03:70-88). The retry scripts (raw99/188/237) never wrote `artifacts/retries/T6/q0-head`, so the halt was labelled `head-moved` without proof that HEAD moved (03:158-169).
- **Case 4.** "16 fixed, 2 partial, 4 new medium" was an early, provisional count; debate later qualified it (04:149-201). The orchestrator said every note was applied (raw791) before the calibrator noted the 18 findings had not been checked one by one (raw801) (04:234).
- **Case 5.** Task 12's acceptance criteria were structural; behavior tests were deferred to Task 14, so reviewers built their own counterexamples (05:50-71). Controls in the same session: Task 10 and Task 11 each converged after one repair (05:246-257).
- **Case 6.** The third FINAL passed after BOTH the evidence fixes AND a rubric change, so the effect of each cannot be separated (06:232-258). A narrow Task 2 manpage omission survived the pass (06:260-273).

---

## 2. Strongest evidence items (with anchors)

| # | Claim | Anchor(s) | Strength |
|---|---|---|---|
| E1 | A fix to a plan introduced new plan defects, proven by before/after text: early four-asset check, old lock-digest source swap, inventory test before registration, renderer boundary, wrong `origin` remote | Case 1 raw544 (v2 Write) vs raw841; 01-session-ac2cd1fd.md:110-192; merged-verdict v2 :57-83, :120-128, :201-209 | Strong (plan level, not runtime) |
| E2 | One proven implementation regression caused by a fix: an inherited ERR trap writes `::error::` to stdout, which is captured into `P=$(...)` | Case 5 raw759-762 (introduced), raw1240 (reproduced); 05-session-e002bed2.md:162, :185-202 | Strong |
| E3 | Most later implementation findings already existed in the first artifact | Case 5 raw585 (640-line original) vs raw804/906/1021/1143; 05:109-165 | Strong |
| E4 | A retained frozen fixture forced a second failure that could be predicted; the repair boundary forbade the fix | Case 2 raw383 (exclusion), raw450 (retained), raw521 (authorization), raw668 (PASS); artifacts/t12-held-back-before-authorization.json:563-628; 02:182-218 | Strong |
| E5 | A re-review with unchanged source and unchanged environment cannot change its verdict | Case 3 raw443 ("No text change was needed"), raw450; t6-fix-evidence.log:1-3 | Strong |
| E6 | The review rubric changed on disk mid-run: the same installed path, two different byte versions | historical-review-rules.json: before sha `0b5337…` (nested acf0…:18, 20:26:30.085Z), after sha `faff03…` (nested a4bfff…:18, 20:32:19.277Z). **Re-verified by this digest:** current `src/.../refs/qa.md` sha256 = `faff03b7b94ca2b70f9b25c35dcefd52636b7df8f7bf9a110c0a956a78d2e7d5` = the "after" version | Strong (who made the change: UNVERIFIED) |
| E7 | A mid-run protocol migration turned a compliant check into a fresh review | Case 5 raw849 (compliant), raw874 (ledger Resume row P), raw893/902 | Strong |
| E8 | Task QA knowingly relaxed a written criterion without the user's consent; the FINAL review reapplied it | Case 6 raw1215 (DIFFERENCE FOUND), raw1230 (log reworded), nested a6d8…:61; plan :30, :96 | Strong |
| E9 | A FINAL missed an evidence defect that already existed, which caused the next FINAL failure | Case 6 raw1425 (bad `:10` pointer created), nested acf0…:116, raw2012 `T10: BLANK` | Strong (why it was missed: unknown) |
| E10 | Coverage was credited by text containment without the required state wiring | Case 1 first coverage-matrix.yaml:1749-1757 (ratio 0.714) | Medium (one row shown) |
| E11 | A repair that repointed dependencies removed required graph ancestors | Case 4 regenerated plan lines 31, 138, 153, 172 vs source :82; 04:203-224 | Strong (plan graph; sequential executor prevents runtime harm) |
| E12 | A wrong baseline produced a false `extra` verdict | Case 3 raw188, raw204, raw234; git trees f60d2c3 / 3c5fdfa / 00d8f4a; 03:190-258 | Strong |
| E13 | The ledger undercounts failed reviews | Case 6 package B progress.md:37-43 has no second `FINAL: issues`; Case 5 ledger through line 34 records 5 blocked lines against 7 verdicts | Strong |

**Counter-evidence that must stay with the claims above** (evidence-deck.md:164-173): repairs often work (case 2, three fixes; case 5 Tasks 10/11). A defect that becomes reachable later is not a defect the fix introduced (case 5, size limits after file transport). A PASS does not prove every literal instruction was met (cases 3 and 6). No case shows that context exhaustion, model weakness or reviewer count was the cause.

---

## 3. Corrections applied after QA

**Phase-3 research gate:** 15 independent reports, 9 PASS / 6 FAIL, merged into 6 issues (qa/qa-consolidated-findings-phase3.md). The main session applied them as appended `<!-- phase3-correction: ... -->` blocks, with SHA256 before/after recorded in qa/phase3-fix-log.md. Fresh verification found **6/6 RESOLVED and 0 new issues** (qa/phase3-fix-verification.md).

| # | Correction | Where it was applied |
|---|---|---|
| C1 | All 16 original Orca plan repairs traced one by one; closure is 14 fixed / 2 partial; "fixed" means the plan amendment was accepted, not that it was tested at runtime | 01-session-ac2cd1fd.md:357 onward (`orca-plan-original-repair-ledger`) |
| C2 | Raw150 edit was blocked (raw151); the retry at raw163 succeeded (raw164). The blocked attempt is not counted as a change | 01:398-409 |
| C3 | All 8 CI second-reviewer entries given dispositions; the completed final review recorded separately (04:02:04Z): `not_ready`, 5M/11L/0H, `partial` | 04-session-43582de1.md:263 onward (`ci-final-outcome-and-reviewer-dispositions`) |
| C4 | Monitor content cutoff is raws 1-1247 ending 03:31:57.433Z, NOT the manifest selection time 03:25:59Z. The later human acceptance (raw1250/1261) closes Task 12 with the same `misunderstood` verdict; there is no eighth review. Task 13 is separate | 05-session-e002bed2.md:288 onward (`monitor-boundary-and-accepted-completion`) |
| C5 | Earlier misses with no observed mechanism are labelled "unknown" (monitor blank notes/CR/rename; credential blank pointer) | 05:405-407; 06-session-0690ee9f.md:318 onward |
| C6 | Credential nested Task 10 reviewer record 16 timestamp corrected to 19:57:18.777Z | 06:208 |

Also recorded: evidence-deck.md:192 (`consolidated-accounting`) and gaps-and-questions.md:38 (`supplemented-endpoints`).

**Process corrections recorded in gaps-and-questions.md:15-27:** the main session overwrote scope-01.md and scope-03.md with skeletons by mistake; they were recovered into `scope-0{1,3}-recovered.md`, and scope-01 still has 4 historical placeholders. 5 of 15 parallel spawns failed on a lock and were retried one at a time. Analyst handoffs were text-only and were transcribed by the main session (stated in each case file's header). Source logs kept growing after first observation, so later evidence is kept as separately timed supplements.

**Corrections to analysts' own reviewer claims** (not QA fixes, but needed before reusing any count): case 1 N-02/N-16 and the withdrawn "pin==current forbidden" subclaim; case 4 allowlist severity lowered, rename order corrected to new-then-old, literal-warning claim rejected; case 3 Task 2 `extra` was a false attribution.

---

## 4. Current protocol files the findings implicate

All paths below are under `/config/workspace/IronClaude/src/superclaude/skills/`. **Existence, line counts and the cited ranges were re-checked by this digest.** Each source file has the same SHA-256 prefix as its `/config/.claude/skills/` installed copy.

| File (exists?) | Lines | Cited rule (re-checked) | Implicated by |
|---|---|---|---|
| `sc-workflow-protocol/SKILL.md` — EXISTS | 72 | :48-58 Wave 3 gate, then Wave 4 reflect: advisory and read-only, never regenerates the plan from findings | Cases 1, 4: the loop is user-driven revise→re-reflect with no rule that a revised plan must be checked against prior findings; v4 shipped unreviewed |
| `sc-workflow-protocol/refs/quality-gates.md` — EXISTS | 41 | :24-39 schema-min / full checks; "every source requirement is covered by at least one task" is a check the agent performs, not a semantic proof | Cases 1, 4: the gate passed all plan versions while semantic, ordering and dependency defects remained (E1, E10, E11) |
| `sc-implement-protocol/SKILL.md` — EXISTS | 175 | :65 resume per ledger; :101 inline vs subagent review rule; operator reviews always use a fresh subagent | Case 5 (fresh reviewers each round find new paths) |
| `sc-implement-protocol/refs/qa.md` — EXISTS | 90 | :9-17 input limited to brief, criteria, constraints and diff; :56-68 halt table and scoped-acceptance Ruling; :80-82 managed FINAL ("moved line number alone is never `issues`"); :84-90 subagent rule and forbidden retry-folder reads. **Current bytes = the "after" rubric** (sha `faff03…`) | Cases 2, 3, 5 (per-task loop); case 6 (FINAL rubric changed mid-run, E6); case 6 Task 6 relaxation (E8) |
| `sc-implement-protocol/refs/retry.md` — EXISTS | 451 | :27 q0-head must be written at Q0 before `start`; :38-43 ladder checks, "a missing file … counts as moved" → `halt review=2 reason=head-moved`; :142-146 cost and caps | Case 3 Task 6 and case 5 Task 13: false `head-moved` halt from a missing q0-head; case 5 Task 12 never ran the ladder (no retry records) |
| `sc-implement-protocol/refs/ledger.md` — EXISTS | 242 | :61-81 Ruling line and post-ruling complete with unchanged verdict; :142 single-writer precondition, no lock; :148-158 resume rows (row P = one fresh operator review of a blocked task with no retry/halt records) | Case 5 (row P migration reopened a compliant task, E7); cases 3, 5, 6 (acceptance closes the task with the verdict unchanged); E13 (ledger undercounts) |
| `sc-implement-protocol/refs/managed-workspace.md` — EXISTS | 85 | :42 plan/source pinned after first `start`; :46-60 archive gate (join writers, state, fresh FINAL, re-state, discard if changed); :80-85 enforcement table: `./artifacts/*` and unlisted delivery files are NOT covered by the state digest | Case 6 (evidence-only FINAL failures with an unchanged digest); case 2 (frozen fixture cannot be silently rewritten) |
| `sc-reflect-protocol/` (SKILL.md + refs/, e.g. `coverage-mapping.md`, `reviewer-spec.md`) — EXISTS (outside the two requested folders) | — | Content NOT re-read by this digest — **UNVERIFIED** which rule applies | Cases 1, 4: the multi-agent `reflect pre` review produced the findings, coverage matrix and counts |

**Caveat:** today's bytes do not show which bytes a historical run loaded. The only proven historical version is the qa.md before/after pair in historical-review-rules.json. Whether cases 1, 2, 3, 4 and 5 ran today's workflow/retry/ledger text is **UNVERIFIED** (gaps-and-questions.md:13). Case 5 shows the protocol changed during the run (raw42/58 load the one-fix rule; raw874/884 show the updated ledger/retry rules).

---

## 5. Remaining open questions

1. **Which rule bytes did each historical run load?** Proven only for case 6 FINAL #2 vs #3. For the others it is UNVERIFIED (gaps-and-questions.md:13).
2. **Who changed the installed qa.md** between 20:26:30Z and 20:32:19Z on 2026-10-22, and would the unrepaired package have passed under the new rubric alone? Unknown (06:258, :296).
3. **Why earlier reviewers missed preexisting defects** (case 5 blank notes/CR/rename; case 6 blank pointer; case 4 search filters; case 1 remaining test-strength gaps). Recorded as unknown; no cognitive cause has been shown (evidence-deck.md:147).
4. **Historical reconstruction gaps:** can every fix diff and frozen fixture be rebuilt from history? gaps-and-questions.md:12 is still "Open". Case 2 has no pre-authorization full oracle snapshot (02:267, :291).
5. **Runtime behavior not established:** GitHub runner, permissions, cancellation, timeouts (case 5); manpage rendering (case 3); no implementation for cases 1 and 4.
6. **Specification contradictions still unresolved** in the Orca source (Noop vs up-to-date state; fetch before self-check; follow tag URL vs check before use) (gaps-and-questions.md:33-35; 01:294-299).
7. **Endpoints still open:** case 4 waits for a user decision with no later refactor seen; case 5 continued into Task 13/14 with no Task 14 review outcome observed.
8. **Generalization:** six cases in a few repos, chosen by mtime, with no controlled old-vs-new protocol comparison. Fleet-wide causation is not established (evidence-deck.md:173).
9. **Pipeline state:** the evidence deck still says "In Progress" and notes that the five-hypothesis adversarial ranking was pending when it was written. Files under synthesis/ and reviews/adversarial/ and the RESEARCH-REPORT exist but were **not read by this digest**. Whether they are complete is UNVERIFIED.
10. **Task 6 render (case 3):** was it ever rendered later, for example in CI? Not established (03:300).

---

## 6. Verification status of this digest

- **Verified directly by this digest:** the six protocol paths in section 4 exist; their line counts; the cited line ranges (workflow SKILL :48-58; quality-gates :24-41; qa :9-17, :56-68, :80-90; retry :27, :36-45, :140-150; ledger :61-64, :81, :140-158; managed-workspace :40-60, :80-85; implement SKILL :65, :101); source and installed hashes match; current qa.md sha256 equals the historical "after" rubric.
- **Taken from research files, not re-checked against raw logs:** every raw/JSONL anchor, every artifact line citation in the Coder and claim-gate worktrees, and every hash in sections 1-2. Their verification status is the case analysts' plus the Phase-3 QA gate's, not this digest's.
- **Line-count note:** scope-rules.md reports workflow SKILL.md as 72 lines (Read showed 73). `wc -l` gives 72; the difference is the trailing newline, not different content.
