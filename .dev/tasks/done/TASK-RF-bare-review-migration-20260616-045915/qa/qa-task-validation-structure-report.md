# QA Report — Task Integrity (Structure + Phase Ordering Lens)

**Topic:** sc-bare-review M8/M9 migration corrective MDTM tasklist
**Date:** 2026-06-16
**Phase:** task-integrity
**Lens:** phase-structure
**Fix cycle:** N/A
**Fix authorization:** false (report-only)
**Task file:** /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-bare-review-migration-20260616-045915/TASK-RF-bare-review-migration-20260616-045915.md
**Template:** 02

---

## Overall Verdict: FAIL

Structural review of the 109-item, 7-phase + 6 phase-gate + 6-item post-completion
task file found the spine of the WS-0→WS-A→WS-B→WS-C sequence and the parity-green
deletion gating to be CORRECT and well-formed, but identified **6 structural defects**
(2 HIGH, 3 IMPORTANT, 1 MINOR) against the phase-structure lens. Any defect = FAIL.

---

## Items Reviewed

| # | Lens check | Result | Evidence |
|---|------------|--------|----------|
| 1 | YAML frontmatter complete/well-formed (spec_path, start_commit, executor_model_class, reflect_pre/post) | PASS | All mandatory fields present + non-empty; `start_commit` 02582ca0 resolves via `git cat-file -t` = commit; `spec_path`, `template_schema_doc`, research dir, related_docs all exist on disk; `reflect_pre` block + `reflect_post: ""` present per template L24-32 |
| 2 | All mandatory template-02 sections present | PASS | Task Overview, Key Objectives, Prerequisites & Dependencies, Execution Context (References/Source Areas/Key Constraints/Handoff/Frontmatter Protocol), Detailed Task Instructions, Post-Completion Actions, Task Log / Notes (Summary, Execution Log, per-phase Findings, Phase Gate Findings, Follow-Up, Deviations) all present |
| 3 | Phase dependencies logical, no cycles; WS-0→WS-A→WS-B; WS-C gated on WS-B parity GREEN | PASS | Phase order 1→2(WS-0)→PG2→3(WS-A)→PG3→4(WS-B)→PG4→5(WS-C)→PG5→6(WS-D)→PG6→7(WS-E). Each phase header declares its dependency; PG4.6 writes `parity-gate-status.md PARITY_GREEN`, Step 5.1 L5 gate-check reads it before ANY deletion; every WS-C deletion item (5.2-5.7) re-reads `ws-c-authorization.md` and proceeds ONLY if AUTHORIZED. Acyclic. |
| 4 | Build before test; capture-golden BEFORE script deletion | PASS | Step 4.1 captures + freezes the legacy golden (while `t2_normalize.py` still exists) and Step 4.2 verifies it; WS-C deletion (Phase 5) is downstream of PG4 parity-green. Golden-freeze-before-delete ordering is explicit and gated. |
| 5 | Task completion items inside a final phase (anti-orphaning) | PARTIAL/PASS | Status→Done (PC.6) lives in `## Post-Completion Actions`, the terminal section, with PC.6 as the last item. Acceptable but see Finding F2 (PC.4 not penultimate). |
| 6 | POST reflect penultimate + FLAT wrapper shell-out form (`reflect run … --depth deep --fix --promote` under SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE skip guard, consuming exit code) | **FAIL** | See Findings **F1** (wrapper form) + **F2** (not penultimate) |
| 7 | Task Log section at bottom | PASS | `## Task Log / Notes 📋` at L593, last section, with all sub-blocks + templates |
| 8 | PER_PHASE QA gates present, min 6 agents, lens-focused | PASS | Phase Gates 2-6 each spawn 3 rf-qa structural + 3 rf-qa-qualitative content (6) + PG6 adds 2 M4 fidelity agents (8). All lens-named, adversarial-framed, `fix_authorization: false` for report-only, ONE serialized fix agent per I20, max-3-cycle HALT. PC.3 post-completion is also 6-agent. |
| 9 | TB-Add: no TBD/TODO/FIXME; blocked items ref Open Qs; DAG; XL split; uniform Verify; Exec-Context source areas reappear + no file:line in block; per-item Context file:line/evidence-absence | **PARTIAL FAIL** | No TBD/TODO/FIXME in body (PASS). DAG holds (PASS). But Source Areas block carries file:line refs — see Finding **F3**. |
| 10 | I17 disk-verification items present | PASS | Step 3.3 (wc -l<=80 + grep t2_ disk-verify), Step 4.2 (golden inventory), Step 5.10 (scripts/refs absent disk-verify), Step PC.1 (final deliverable on-disk verification), PC.2 (final regression) — all derive verdicts from real `ls`/`wc`/`grep`/`find` output, explicitly anti-attestation. |

---

## Summary
- Lens checks passed: 7 / 10 (checks 1,2,3,4,7,8,10)
- Lens checks failed: 3 (checks 5-partial, 6, 9-partial)
- Issues found: 6 (HIGH: 2, IMPORTANT: 3, MINOR: 1)
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| F1 | HIGH | Step PC.4 (L583) | POST reflect gate uses the PLAIN form `superclaude reflect run --mode post --task <file> --depth deep` — it is MISSING the lens-required FLAT wrapper shell-out shape: no `--fix`, no `--promote`, and no `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` skip-guard wrapping (confirmed: `grep -c SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` = 0, `grep -c -- --fix` = 0, `grep -c -- --promote` = 0). Without the skip guard, a reflect wrapper that itself shells back into this task can recurse; without `--fix --promote` the gate observes but does not remediate/promote per the lens contract. | Rewrite PC.4 to the FLAT wrapper form: invoke `superclaude reflect run … --depth deep --fix --promote` guarded by `if [ -z "$SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE" ]; then …; fi` (skip when already inside a wrapper), and consume/branch on the exit code (judging PASS by `return-contract.yaml` status/regression, treating "degraded (single-reviewer-fallback)" exit 11 as a possible content PASS per the project memory). |
| F2 | HIGH | Steps PC.4 → PC.5 → PC.6 (L581-591) | The POST reflect item (PC.4) is NOT penultimate. Two items follow it: PC.5 (Write Task Summary) and PC.6 (Close out frontmatter → status Done). The lens requires reflect to sit IMMEDIATELY before the Update-status-to-Done item, so the independent anti-bias audit is the last gate before completion is asserted. As written, the Task Summary is authored AFTER the reflect audit (so reflect cannot review it) and there is an item between reflect and Done. | Reorder so the reflect gate is penultimate: move PC.5 (Task Summary) to BEFORE PC.4, making the tail `… → Write Task Summary → POST reflect gate → Update status to Done`. Alternatively fold the summary write into PC.3/earlier and keep reflect (PC.4) immediately before PC.6. |
| F3 | IMPORTANT | `### Source Areas` block, L110-118 | The Execution Context Source Areas block embeds numerous specific `path:NN` / `path:L1304-1578` citations (`bare_review.py … :61 :62 :63 :47-52`; `commands.py … ~L1304-1578, L1554-1577, L1714-1977, L728-868`; `normalize.py … :482-483`; `reduce.py … :369`). Per lens item 9 / TB-Add-7 consumer-side spot check (`grep -cE "src/|/.*:[0-9]+"` over the block range must be 0) and the producer-side hidden-input guard (R-039), the header block MUST NOT carry file:line references — those belong only in per-item Context fields (TB-Add-8 enforces the item side). The block is the header summary, not an evidence venue. | Strip the `:NN` / `Lnnnn` anchors from the Source Areas bullets (keep the file/dir names and the prose role: "WS-0 wires the inline path + adds 4 flags"). The precise anchors already appear in the per-item Context fields (Steps 2.1-2.7), which is the correct venue. |
| F4 | IMPORTANT | Overview L87 vs Phase 6/7 structure (L469, L553) | The Prerequisites section states "WS-D and WS-E are independent and may run in parallel," but the task file serializes them as Phase 6 (WS-D) then Phase 7 (WS-E), and the F1 execution loop processes phases strictly in order with no parallel-spawn marker on these phases. WS-E (Step 7.1/7.2) also reads the WS-A disk verdict and WS-C verdicts, so it genuinely DEPENDS on WS-A/WS-C completion — meaning the "WS-D and WS-E … parallel" prose is both unactionable (no parallel marker) and partially contradicted by WS-E's actual cross-references. | Reconcile the prose with the structure: either (a) drop the "may run in parallel" claim and state WS-D/WS-E run sequentially after the WS-0→WS-C chain, or (b) if true parallelism is intended, add an explicit parallel-execution marker to the Phase 6/7 headers. Note WS-E's real dependency on WS-A/WS-C verdicts so the executor doesn't start WS-E before those land. |
| F5 | IMPORTANT | Step 2.4 (`--timeout-sec`, L195) vs Step 2.7 (L205) | Step 2.4 adds `--timeout-sec` whose threading into `dispatch_wave1(worker_spec=...)` "depends on Step 2.7 wiring the worker_spec" — a FORWARD reference to a later item in the same phase. Per lens item 11 (intra-phase dependency ordering), an item that depends on another item's output should come AFTER it. As written, 2.4's flag cannot be fully validated until 2.7 runs, and 2.4's own gate is only a path-scoped ruff (no functional test), so the dependency is deferred but not ordered. | Partially mitigated: the item explicitly NOTES the dependency, 2.7 does the worker_spec wiring, and the WS-0 STRICT gate (Step 2.10) functionally validates the whole pipeline at phase end. Acceptable IF the note is retained, but cleaner to either (a) move the timeout-threading assertion into Step 2.7, or (b) reorder so worker_spec wiring (2.6/2.7) precedes the timeout flag item. Flagged IMPORTANT, not blocking, because the end-of-phase gate covers it. |
| F6 | MINOR | Handoff convention L138 vs Step 1.2 L167 | The Handoff File Convention lists 5 subdirs (`discovery/`, `test-results/`, `reviews/`, `plans/`, `reports/`) but `reviews/` is never written to by any item (QA reports go to `qa/`, which Step 1.2 creates separately). Harmless unused directory, but a minor inconsistency between the declared convention and actual item usage. | Either remove `reviews/` from the convention list or repoint the QA-report writes; cosmetic only. |

---

## Confidence Gate

- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 8 | Grep: 0 (grep run within Bash) | Glob: 0 | Bash: 4 (item-count + placeholder + reflect-form scan; frontmatter-field check; Execution-Context file:line scan + start_commit/spec_path existence; phase-ordering + per-item-evidence scan)
- No web research performed (all claims are local-source-truth).
- No UNCHECKED items. Every lens criterion was verified against the actual file with cited tool output.

Tool-engagement note: the lens has 10 criteria; total Read+Bash calls (12) exceed
the criterion count, so the engagement minimum is satisfied.

---

## Recommendations (before this task file is executed)

1. **F1 + F2 (HIGH) must be fixed** — the POST reflect gate is the project's mandatory
   independent anti-bias check (see memory `feedback_sc_reflect_vs_inline_rfqa`). Both
   its form (FLAT wrapper + `--fix --promote` + skip guard + exit-code consumption) and
   its position (penultimate, immediately before status→Done) are load-bearing. Fix both.
2. **F3 (IMPORTANT)** — strip file:line anchors from the Source Areas header block; they
   already live in the per-item Context fields where they belong (TB-Add-7/R-039).
3. **F4 (IMPORTANT)** — reconcile the "WS-D/WS-E may run in parallel" prose with the
   serial Phase 6→7 structure and WS-E's real dependency on WS-A/WS-C verdicts.
4. **F5 (IMPORTANT)** — tighten the Step 2.4↔2.7 intra-phase forward dependency (or rely
   on the documented note + Step 2.10 end-of-phase functional gate).
5. **F6 (MINOR)** — drop the unused `reviews/` subdir or wire it up.

The WS-0-prerequisite discovery, the parity-green deletion gate, the golden-freeze-before-delete
ordering, the disk-verification anti-attestation items, and the 6-agent lens gates are all
structurally sound and should be preserved as-is.

## QA Complete
