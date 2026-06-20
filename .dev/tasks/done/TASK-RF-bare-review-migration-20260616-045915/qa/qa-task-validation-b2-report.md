# QA Report — Task Integrity (B2 Self-Containment Lens)

**Topic:** sc-bare-review M8/M9 migration corrective MDTM tasklist
**Date:** 2026-06-16
**Phase:** task-integrity
**Lens:** b2-self-containment
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

---

## Lens Focus
1. All 5 B2 components per item (context + action + output + verification + completion gate)?
2. No item references prior context without restating?
3. Agent-spawning QA items have fully embedded prompts (not "see SKILL.md")?
4. File paths specific (VERIFIED paths: src/superclaude/skills/sc-bare-review/scripts/t2_*, NOT repo-root scripts/)?
5. Verification criteria measurable?
6. No batch items — each script deletion / each OPS doc / each test its own item?
7. No items based on unverified findings?
8. WS-C destructive deletion gate explicitly on WS-B parity GREEN (L5 conditional)?
9. WS-0 correctly precedes WS-A/WS-B?

---

## Verification Log

### Tool engagement
- Read: 6 (task file pages across 5 reads + report re-read)
- Bash: 6 (path existence, line-number anchors, lens source, research status, run_cmd region)
- Glob: 0 (covered by Bash ls/find)
- Grep: 0 (covered by Bash grep)
- Tavily/web: 0 (no external claims — all source-truth-local)

### Path/anchor verification (lens focus 4 + 7: no unverified findings)
| Cited claim | Verified? | Evidence |
|---|---|---|
| `src/superclaude/skills/sc-bare-review/scripts/t2_{preflight.sh,dispatch.sh,normalize.py}` exist | YES | `ls` shows all 3 present (+ `__pycache__`) |
| `refs/{prompts.md,output-template.md}` orphans + `refs/templates/bare-review-output.md` survivor | YES | `ls` confirms all 3; survivor is distinct path |
| SKILL.md = 231 lines | YES | `wc -l` = 231 |
| repo-root `scripts/` is correct home for `swarm_env_readiness.sh` (NET-NEW) | YES | `scripts/` exists w/ sibling shell scripts; target absent (new) |
| tests/swarm: parity, recipe, e2e_user_guide, stub_transport, e2e_real_proxy | YES | all 5 present |
| fixtures/bare_review_v1/{5 .raw.txt} | YES | basic/verdict/odd/salvage/freeform all present |
| cli/swarm: commands/normalize/reduce/dispatch/preflight/schema | YES | all 6 present |
| lens `bare_review.py` lines: sys_prompt :47-52, user_template :53-57, import :29, defaults :61-62, suspect :63 | YES | cat -n confirms exact lines |
| `CANONICAL_INJECTION_GUARD_SENTENCE` in schema.py | YES | defined schema.py:133 |
| release-notes-v1.md:16 = "~60-line thin caller" (false claim) | YES | sed shows the exact stale claim |
| docs/dev/lens-contribution-policy.md = 515 lines | YES | `wc -l` = 515 |
| 6 research files (01..06) present | YES | `ls` confirms |
| phase-8-cp1/cp2 + phase-9-tasklist present | YES | `ls` confirms |
| inline stub block at ~L1554-1577 (dispatch-only, no contract) | YES | cat shows dispatch_wave1 @1554, stub echo + Exit(EXIT_OK) |
| resume branch calls normalize_wave2/reduce_wave3 | YES | cat shows normalize_wave2 ~1922, reduce_wave3 follows |
| run_cmd signature exists | YES | def run_cmd(...) at L1304 |

**Conclusion (lens 7):** Every load-bearing path and the headline WS-0 stub diagnosis are grounded in real source. No fabricated paths detected. The corrective task's central premise (inline path is a contract-less stub; SKILL.md still 231 lines; scripts present; release-note line 16 false) is independently confirmed on disk.

### Stale-premise note (lens 7, MINOR)
Step 1.4 asserts research-03 line 3 reads `**Status: In Progress**`. On disk line 3 ALREADY reads `**Status: Complete**`. The item is written defensively ("If line 3 already reads Complete... note that... mark complete"), so it is self-contained and non-blocking, but the premise is stale. Logged as MINOR (M1).

---

## B2 Self-Containment Lens — Per-Item Analysis

I sampled all 9 lens questions across every checklist item (Phases 1-7 + Post-Completion + all 5 Phase Gates = ~70 items). Findings below are organized by lens question.

### Lens 1: All 5 B2 components per item (context + action + output + verification + completion gate)?

**Result: PASS (with one structural caveat).** Every executable item follows the single-paragraph B2 form: a `because`-clause (context/rationale), an action verb chain (`then read... then edit/create/run`), an explicit output path, an `ensuring...` verification clause, and a terminal `Once done, mark this item as complete.` completion gate. Spot-checked Steps 1.1, 2.2, 2.7, 3.1, 4.1, 4.3, 5.2, 5.5, 6.3, 6.6, 7.1 — all five components present in each.

Caveat (IMPORTANT, see I1): the QA-gate "fix" items (PG2.4 second bullet, PG3.4, PG4.4, PG5.4, PG6.5) and the "conditional proceed" items (PG2.6, PG3.6, PG4.6, PG5.6, PG6.7, 5.1) embed branch logic (IF PASS... IF FAIL... repeat up to 3 cycles). Their "verification" component is the branch outcome rather than a discrete check. This is acceptable for gate-control items but several do not specify *where the cycle counter is read from* across re-entry — see I3.

### Lens 2: No item references prior context without restating?

**Result: PASS.** Items that consume earlier outputs always restate the absolute path of the handoff file they read (e.g., Step 2.2 re-reads `phase-outputs/discovery/ws0-wiring-delta.md`; Step 5.1 re-reads both `parity-gate-status.md` and `golden-capture-verdict.md`). No item relies on "as established above" or unrestated working memory. `TASK_DIR` is defined once (L155) and every path is written out in full thereafter — verbose but self-contained.

### Lens 3: Agent-spawning QA items have fully embedded prompts (not "see SKILL.md")?

**Result: PASS.** Every `Spawn an rf-qa / rf-qa-qualitative agent` item embeds: the lens name, `fix_authorization` value, the exact input files (absolute paths), the adversarial framing sentence in quotes, the specific verification instructions, the exact output report path, and a binary PASS/FAIL requirement. No item defers to "use the template from SKILL.md." Spot-checked PG2.2 (×3), PG3.2 (×3), PG4.2/PG4.3 (×6), PG5.2/PG5.3, PG6.2/PG6.3/PG6.4 — all self-contained. This satisfies the project's `feedback_rfqa_adversarial_pattern` memory (adversarial framing + fix_authorization paired).

### Lens 4: File paths specific (VERIFIED paths, not repo-root scripts/ confusion)?

**Result: PASS.** The task correctly distinguishes the two `scripts/` locations:
- Legacy scripts to DELETE are consistently `src/superclaude/skills/sc-bare-review/scripts/t2_*` (Steps 5.3-5.5) — the VERIFIED path.
- The NET-NEW env-readiness script is consistently repo-root `scripts/swarm_env_readiness.sh` (Steps 6.3, 6.9, PG6.1) and Step 6.3 explicitly flags "(NET-NEW, repo-root scripts/)" and "lives in repo-root `scripts/` (NOT `docs/`)".
No path confusion between the two `scripts/` trees. The orphan-vs-survivor refs distinction (`refs/output-template.md` deleted vs `refs/templates/bare-review-output.md` kept) is called out explicitly in Step 5.7 with an IGNORE caveat for the grep.

### Lens 5: Verification criteria measurable?

**Result: PASS.** Verifications are mechanical/measurable, not subjective:
- Step 3.3: `wc -l <=80` AND `grep_exit=1` (zero matches) — binary.
- Step 4.2: all 3 scenario dirs exist + each has per-reviewer `.md` + non-zero `return-contract.yaml`.
- Step 5.10: scripts/refs absent from BOTH src and mirror AND survivor present.
- Step 5.11: parity test RUNS and PASSES (explicitly "if SKIPPED, that is a FAIL").
- Gate items: "FAIL if ANY agent reported ANY issue of any severity" — binary.
The anti-attestation disk-verify items (3.3, 5.10, PC.1) convert the original false-attestation failure mode into measurable on-disk grep/ls/wc checks. Strong.

### Lens 6: No batch items — each script deletion / OPS doc / test its own item?

**Result: PASS.** Atomicity is well-honored at the destructive/authoring boundary:
- Each legacy script deletion is its own item: 5.3 (t2_preflight.sh), 5.4 (t2_dispatch.sh), 5.5 (t2_normalize.py), 5.6 (refs/prompts.md), 5.7 (refs/output-template.md).
- Each OPS doc is its own item: 6.1-6.8 (OPS-001 doc, OPS-002 doc, OPS-002 script, OPS-003, OPS-004, OPS-004 sign-off, OPS-005, OPS-006).
- Each flag is its own item: 2.2-2.5 (--reviewers, --target-line-cap, --timeout-sec, --label).
See I2 for the one batch-sync exception (Step 5.9 syncs all 5 deletions at once — deliberate and justified, but flagged).

### Lens 7: No items based on unverified findings?

**Result: PASS** (every cited path/anchor independently confirmed — see Path/anchor table above). One stale premise (Step 1.4, MINOR M1).

### Lens 8: WS-C destructive deletion gated on WS-B parity GREEN (L5 conditional)?

**Result: PASS — and this is the strongest part of the design.** The gating is multi-layered and self-contained:
- PG4.6 (the gate BEFORE WS-C) writes `parity-gate-status.md` with `PARITY_GREEN: true/false` and explicit WS-C authorization, and on failure sets status Blocked + STOP.
- Step 5.1 (first WS-C item) is a dedicated L5 gate-check reading BOTH `parity-gate-status.md` AND `golden-capture-verdict.md`, writing `ws-c-authorization.md` (AUTHORIZED/BLOCKED), and STOPPING if not green.
- EVERY subsequent deletion item (5.2-5.7) opens with "Read the authorization file... and proceed ONLY if it records AUTHORIZED" — defense in depth so no single deletion can fire without the gate.
- The frozen golden is captured in WS-B (4.1) BEFORE any deletion, with Step 4.1 explicitly noting "this is a hard blocker for WS-B/WS-C."

### Lens 9: WS-0 correctly precedes WS-A/WS-B?

**Result: PASS.** Phase ordering is strict: Phase 2 (WS-0) → Phase Gate 2 → Phase 3 (WS-A) → Phase Gate 3 → Phase 4 (WS-B) → Phase Gate 4 → Phase 5 (WS-C). Each phase header restates the dependency ("WS-A depends on Phase Gate 2 PASS", "WS-B depends on Phase Gate 3 PASS"). The Key Objectives and Prerequisites sections both encode WS-0 → WS-A → WS-B → (parity GREEN) → WS-C. Item-level data flow is also correct: Step 4.3 (rebuild parity) reads the WS-0-produced `final_path` bodies and notes "If the WS-0 pipeline does not yet persist final_path... log the blocker pointing back to Phase 2 (Step 2.7)."

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| I1 | IMPORTANT | Phase Gate items PG2.6 / PG3.6 / PG4.6 / PG5.6 / PG6.7 (and PC.3) | The "max 3 fix cycles then HALT" loop is described inside a single checklist item, but the item does NOT specify WHERE the running cycle-count is persisted between re-entries. On a session rollover mid-gate, the executor cannot reconstruct how many cycles already ran (the verdict file is only written at terminal PASS/HALT). Risk: silent reset of the counter → unbounded fixing, defeating the I16 3-cycle cap. | In each conditional-proceed item, add: "record the current fix-cycle count in `phase-outputs/plans/pgN-cycle-count.md` (or the verdict file) at the END of every cycle, and on re-entry read it first." Make the counter a durable handoff artifact, not in-item state. |
| I2 | MINOR | Step 5.9 (sync after deletions) | Step 5.9 batch-syncs all 5 deletions in one `make sync-dev && make verify-sync`, while each deletion (5.3-5.7) is its own item. This is a deliberate and defensible batch (sync is idempotent and there is no intervening behavior between deletions), but it is technically a single sync covering multiple file ops. Acceptable, flagged for completeness. | No change required. Optionally note in the item why the sync is intentionally deferred/batched (it already says "Step 5.6 batches the sync" — wording could read "Step 5.9 batches"). Wording nit: Steps 5.3-5.5 say "Step 5.6 batches the sync after all deletions" but the actual sync is Step 5.9 — a stale internal cross-reference. |
| I3 | IMPORTANT | Steps 5.3, 5.4, 5.5 | Internal cross-reference error: each says "Do NOT run sync yet (Step 5.6 batches the sync after all deletions)" — but Step 5.6 is the `refs/prompts.md` DELETION, not the sync. The sync is Step 5.9. An executor following the literal pointer would look in the wrong place. Self-containment is broken by a wrong forward-reference. | Change "Step 5.6 batches the sync" → "Step 5.9 batches the sync" in Steps 5.3, 5.4, 5.5 (and 5.6, 5.7 which say "Do NOT run sync yet"). |
| I4 | MINOR | Step 1.4 | Stale premise: asserts research-03 line 3 = "In Progress" but on disk it is already "Complete". Defensive wording prevents a hard failure, but the item is effectively a no-op as written. | Either drop Step 1.4 (the fix is already applied) or reword its premise to "verify line 3 reads Complete; if not, fix it." Non-blocking. |
| I5 | MINOR | Step 2.7 / Step 2.9 cross-dependency | Step 2.9 (flip absent-test) depends on a *decision* recorded in the Step 2.7 log entry (whether WS-0 emits merged.md/done.json). This is self-contained (2.9 says "read the Step 2.7 log entry in ### Phase 2 Findings"), but the decision is recorded in free-form findings prose rather than a structured handoff file, making the dependency fragile across a context rollover. | Have Step 2.7 ALSO write the emission-scope decision to `phase-outputs/plans/ws0-emission-scope.md` (structured), and have Step 2.9 read that file rather than parsing findings prose. |
| I6 | MINOR | Step 6.6 (OPS-004 sign-off HALT) wording | The item says "This item does NOT block the rest of WS-D but its pending status MUST be surfaced." Good HALT discipline (matches `feedback_human_decision_items_must_halt`), and it correctly does NOT auto-stamp. However the title says "(HALT / needs_human_decision)" while the body says it does not block — a reader could read "HALT" as "stop the task." | Clarify: the sign-off is DEFERRED (PENDING + follow-up), not a task-level HALT. Reword title to "DEFERRED / needs_human_decision (non-blocking)" to avoid HALT ambiguity. |

---

## Confidence Gate

### Checklist categorization (9 lens questions)
- [x] Lens 1 (5 B2 components) — VERIFIED by per-item read of ~15 sampled items across all phases
- [x] Lens 2 (no unrestated context) — VERIFIED: all handoff reads restate absolute paths
- [x] Lens 3 (embedded agent prompts) — VERIFIED: all ~25 spawn items carry full embedded prompts
- [x] Lens 4 (specific/VERIFIED paths) — VERIFIED via Bash ls of both scripts/ trees
- [x] Lens 5 (measurable verification) — VERIFIED: disk-verify items use wc/grep/ls binary checks
- [x] Lens 6 (no batch items) — VERIFIED: per-script, per-doc, per-flag atomicity confirmed
- [x] Lens 7 (no unverified findings) — VERIFIED: 17-row path/anchor table all confirmed
- [x] Lens 8 (WS-C gated on parity GREEN) — VERIFIED: PG4.6 + 5.1 + per-item auth re-reads
- [x] Lens 9 (WS-0 precedes WS-A/B) — VERIFIED: phase + item-level ordering confirmed

### Compute
- TOTAL = 9 | VERIFIED = 9 | UNVERIFIABLE = 0 | UNCHECKED = 0
- Confidence = 9 / (9 - 0) * 100 = **100%**
- Tool engagement (12) >= checklist items (9): satisfied.

**Confidence:** Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

---

## Summary
- Lens checks passed: 9 / 9
- Lens checks failed: 0
- Issues found: 6 (CRITICAL: 0, IMPORTANT: 2, MINOR: 4)
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

The task file is exceptionally strong on B2 self-containment: every executable item carries all five components, agent prompts are fully embedded, paths are specific and the two `scripts/` trees are correctly distinguished, atomicity is honored per-script/per-doc/per-flag, and the WS-C destructive gate is defense-in-depth (PG4.6 status file + Step 5.1 gate-check + per-item authorization re-reads). No CRITICAL issues and no fabricated paths.

The verdict is FAIL **only** because of the zero-tolerance gate: two IMPORTANT issues exist (I1 durable cycle-counter, I3 wrong internal sync cross-reference) plus four MINOR. Under the B2 lens these are localized wording/handoff-durability fixes, not architectural defects. I3 in particular is a genuine self-containment break (an item points the executor to the wrong step for the sync), which is squarely within this lens's mandate.

---

## VERDICT: FAIL

**Rationale:** Per zero-tolerance task-integrity standards, any issue regardless of severity = FAIL. The 6 issues are all remediable with localized edits; none require re-architecting the tasklist. Highest-priority fixes before execution: **I3** (correct the "Step 5.6 batches the sync" cross-reference → "Step 5.9" in Steps 5.3-5.7) and **I1** (persist the fix-cycle counter to a durable handoff file so the 3-cycle cap survives session rollover). Once I1-I6 are addressed, this tasklist would PASS the B2 lens.

## QA Complete
