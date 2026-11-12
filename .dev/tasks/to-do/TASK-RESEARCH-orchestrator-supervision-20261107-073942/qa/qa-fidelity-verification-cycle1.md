# QA Report — Source-document fidelity gate, fix-cycle verification (cycle 1, third and last review)

**Topic:** Orchestrator mode Phase 1 (issue #339) research report
**Date:** 2026-11-07
**Phase:** fix-cycle
**Fix cycle:** 2 (verifies the cycle-1 fix pass; third review of this gate)
**Fix authorization:** false (report only; no file edited except this one)
**Inputs:** `qa/qa-fidelity-consolidated-findings-cycle1.md` (C1-01 to C1-04, |F_0'| = 4 for this pass), `qa/qa-fidelity-fix-log-cycle1.md`
**Report:** `RESEARCH-REPORT-orchestrator-mode.md`

---

## Findings (written incrementally)

Source-version note: `src/superclaude/core/WORKER-CONTRACT.md` is cited by the report at HEAD of this worktree, not at `495eb96d`. `git diff 495eb96d HEAD` on that file adds one line at `:33` (WC-4 `artifacts` rule), so every WC-3/WC-5/freeze line sits one line lower at HEAD than at `495eb96d` (WC-3 Ruling halt: `495eb96d` `:55`, HEAD `:56`). WC-3 text is byte-identical in both. The report's numbers (`:30`, `:45`, `:54-56`, `:58`, `:60`, `:108`, `:125`, `:129`, `:133-136`) all match HEAD. #409 file `data-dictionary.md` checked via `git show 495eb96d:` (`:12` Request, `:27` policy frozen / not frozen): match.

### C1-01 (IMPORTANT) — RESOLVED

Required: the `ask the coordinator` skip must cover 4a's and 4b-contract's contract halves; GQ-96 sentence and step 1.8 fixtures conditional; `:113`, diagram rule 1 and rule 4 aligned.

| Spot (current line) | Check | Result |
|---|---|---|
| §2 precedence `:113` | Rule 1 states the condition (settled / `report blocked` / Ruling halt); says the same condition gates 4a and 4b-contract; names the source conflict with `research-notes.md:192`, `:196` and GQ-96 | PASS |
| §2 rule 4 `:116` | "A blocked contract counts under 4a or 4b-contract only when rule 1's condition holds" | PASS |
| §3.1 diagram `:371-385` | Rule 1 carries the condition and the fall-through note; rule 4 carries "(a blocked contract counts here only when rule 1's condition holds)" | PASS |
| §3.1 policy bullet `:406` | GQ-96 sentence conditional; skipped case gets no class from 1/4a/4b-contract and policy "could not determine", never "not frozen" | PASS |
| GQ-02 row `:525`, GQ-96 row `:579`, gap-to-step GQ-96 `:1358` | All conditional on rule 1's condition | PASS |
| §7 precedence diagram `:957-961` | Rule 1 conditional; rule 4(a) lists only `agentWait` | PASS |
| Step 1.3 `:1224` | Rule 1 condition defined once as "rule 1's condition"; 4a contract half "when rule 1's condition holds" with the WC-2 `:30` reason; 4b-contract blocked case "and rule 1's condition holds (otherwise policy could not determine)"; GQ-96 sentence conditional | PASS |
| Step 1.8 `:1234` | 4a fixture on a settled row; GQ-96 fixture on settled row or `report blocked`; live `ask the coordinator` implement contract asserts no class from 1/4a/4b-contract and policy could not determine; rule-1 ask fixture asserts "not (a) or frozen under rule 4". The rule-1 and 4a fixtures no longer assert opposite results for one input | PASS |
| Step 1.9 `:1235` | "blocked contract with Orca outcome `failed` -> waiting on a person": a settled row, so it meets the condition | PASS |

Sources re-read: `WORKER-CONTRACT.md` HEAD `:52-57` (WC-3), `:30` (WC-2 `blocked_question` in every blocked contract), `:32` (WC-4 `reason` carries the STOP code for `/sc:implement` when blocked), `:133` (freeze on latest blocked implement contract); `research/research-notes.md:190-202` (rule 1 `:192`, 4a `:196`, 4b `:197`, unconditional as the report says); `gaps-and-questions.md:119` (GQ-96, unconditional as the report says).

**Unrequested addition (Ruling-halt case), checked against source:** PASS. WC-3 (HEAD `:56`, `495eb96d` `:55`): "A Ruling halt is never asked: an `/sc:implement` halt for a Ruling (`E-HALT-QA`, `E-NO-RULING`) is reported blocked whatever the policy line says". So a blocked implement contract with one of those codes cannot be replaced by an ask-and-re-run, and rule 1 applying to it on a live `ask the coordinator` row is faithful. The report detects it by `reason`, which WC-4 (`:32`) says carries the STOP code when `/sc:implement` is blocked. Both codes exist in `~/.claude/skills/sc-implement-protocol/refs/qa.md:247` (`E-HALT-QA`, "No, unless operator Ruling") and `:249` (`E-NO-RULING`). The step 1.8 fixture "`E-HALT-QA` on a live row under `ask the coordinator` -> class (a), policy frozen" matches WC-3 `:56` plus the freeze rule `:133`. The `:56` citation is correct for HEAD.

### C1-02 (IMPORTANT) — RESOLVED

- §8.2 row now at `:1414`: label "S9 rows 8, 9, 30, 51, 53"; owner decisions list GQ-61, GQ-63, GQ-10, GQ-11, GQ-35 only; adds "Person-started sessions (G6, GQ-09, S9 row 7) are not an owner decision: the sources settle that they are reported (Section 3.1 G6)"; "step 1.0b asks for all five"; Blocks column "WC-14 rule id, default window, report directory, layout pin, report format (GQ-63)" with no "G6 wording".
- Cross-check: step 1.0b `:1216` names the same five (GQ-10, GQ-11, GQ-35, GQ-61, GQ-63) and says GQ-09 "is not asked". Grep of the report for "S9 rows 7, 8", "G6 wording", "report person-started sessions": 0 hits. "all six" has one hit, `:1288` "`src/superclaude/cli/sweep/` (all six modules)", which is the module count, not the decision count.

### C1-03 (IMPORTANT) — RESOLVED

- Step 1.8 `:1234` adds `patch_git` fixtures: `git status --branch --porcelain` for a branch with no upstream and one ahead of upstream; `git status --porcelain -- .dev/tasks` with an untracked and an unstaged path; a `_git` raising `subprocess.CalledProcessError`.
- Step 1.9 `:1235` adds one safe-to-close case per fixture, built through the step 1.4 git probe, each "worktree removable: no" with the condition named, plus the failed-git case (`unpushed` / `dev_tasks_unsaved` is `None`, "worktree removable: could not determine").
- SC-4 `:458` "How it is checked" names these tests.
- Supporting definitions exist: step 1.2 `:1223` `WorktreeState.unpushed: bool | None` and `dev_tasks_unsaved: bool | None`; step 1.4 `:1225` git allowlist includes `status`, and the probe functions catch `(OSError, subprocess.SubprocessError)` and map to could not determine, so the failed-git expectation is consistent.
- Source: `seed-brief.md:60` ("`.dev/tasks/` content is never classed as disposable") and `:68` (mock-based tests for "git cleanliness, unpushed commits, unfinished ledgers"): cited correctly.

### C1-04 (IMPORTANT) — RESOLVED

- Rollback "Four registries" row `:1292` now reverts the step 1.21(b) "Orca coordination" edits (the coordinator-runs-`/sc:sweep` bullet and `/sc:sweep` in the "Some commands are never workers" bullet `:403`) and re-copies the plugin byte copy after both the "Other commands" and the "Orca coordination" reverts, including the follow-up-PR case. Rationale `:1284` extends the "removed command" argument to those bullets.
- Matches step 1.21 `:1263` part (b) (adds the bullet, extends the `:403` bullet) and step 1.23 `:1265` (copy again if part (b) moves).
- Source: `src/superclaude/core/HOW-WE-WORK.md:396` "## Orca coordination", `:403` "**Some commands are never workers.**": both line numbers correct.
- Coverage check: every Phase 1 step that edits a file (1.2-1.24b) maps to a rollback row (`:1288-1293`).

## New findings introduced by the fixes

No new blocking finding. Adversarial search covered: every report line that links a blocked contract to "waiting on a person" or names `blocked_question` (grep, 17 lines); every place GQ-96, "ask the coordinator", "Ruling halt" and "rule 1's condition" appear (grep, 40 hits); all WORKER-CONTRACT line citations against HEAD; the decision-count wording; the rollback row against the step list; regression markers (NB-4: 23 hits, CONTRADICTION: 6 hits, the same counts the fix log records; `git status --short src/` empty, so no source was edited).

MINOR notes (do not fail the gate, not to be rechecked):

| # | Location | Note |
|---|---|---|
| M1 | Step 1.3 `:1224`, §2 `:113` | A row that skips rule 1 is said to get "working (rule 5) or could not determine (rule 7)". Rules 2, 3 and the `agentWait` half of 4a can still match such a row. Whether a worker blocked in Orca `ask` shows a non-null `agentWait` is not established (`research/scope-02-orca-recovery.md:70` describes `agentWait` as hook / prompt-text / title evidence; `:106` says `ask` has no read path). If it does, rule 4a labels a worker that is asking the coordinator as waiting on a person. Wording: say "falls through to rules 2-7" and keep the step 1.8 fixture's `agentWait` null. |
| M2 | Step 1.2 `:1223`, step 1.3 `:1224` | Carried from `qa-fidelity-verification.md:153`: rule 1's condition reads the brief's policy line "from the Task spec", but neither `SessionRow`/`OrcaObservation` nor the `classify(row, contract, now)` signature carries it, and step 1.4 names no probe that reads a running Task's spec. The fallback ("when it cannot be read ... could not determine") keeps behaviour safe, but the step 1.8 fixture "live row whose brief says `report blocked` -> (a)" needs a field to express. |
| M3 | Step 1.2 `:1223` vs step 1.3 `:1224` | `policy` is listed as "frozen / not frozen" defaulting to `UNKNOWN` ("unknown"), while step 1.3 prints policy "could not determine" (also used before this fix for the ledger case). Name the third value in step 1.2. |
| M4 | §2 `:113` | The rule still opens with "`worker_status: blocked` means waiting on a person" before stating the condition; reads as unconditional on a skim. |
| M5 | Gap-to-step G-B `:1318`, S9 row 2 `:1520` | Summary rows still say questions come from `blocked_question` without "when rule 1's condition holds"; the full rule is in `:525` and step 1.3. |

## Items that PASS

C1-01, C1-02, C1-03, C1-04; the unrequested Ruling-halt case of C1-01 (source-faithful to WC-3 `WORKER-CONTRACT.md:56`); regression check (no previously resolved finding reopened; NB-4 record and both [CONTRADICTION] markers intact).

## Gate arithmetic

- Previously open blocking: |F_0| = 4 (C1-01 to C1-04)
- Resolved: 4. Still open: 0. New blocking: 0.
- **|F_1| = 0**
- Regression check (step 1): no item that passed earlier now fails. Monotonicity (step 2): 0 < 4, no halt. Hard cap (step 3): this is the third and last review; nothing is left to escalate.

## Confidence Gate

- **Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
  (items: C1-01, C1-02, C1-03, C1-04, Ruling-halt addition, regression check, new-blocking scan)
- **Tool engagement:** Read: 10 | Grep: 5 | Glob: 0 | Bash: 21 (all read-only: `git show`, `git diff`, `sed -n`, `grep`). No web research.
- Unchecked items: none. Unverifiable items: none (M1's `agentWait`-under-`ask` question is unverified in the sources, which is why it is recorded as a note, not a finding).

## Verdict: PASS

