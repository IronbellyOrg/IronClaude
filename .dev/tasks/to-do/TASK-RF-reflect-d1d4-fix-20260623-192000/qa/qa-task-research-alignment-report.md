# QA Report — Task ⇆ Research Alignment

**QA_MODE:** task-integrity
**LENS:** task-research-alignment
**Adversarial stance:** Assume the builder dropped or misrepresented research findings.
**Date:** 2026-06-23
**Task file:** `TASK-RF-reflect-d1d4-fix-20260623-192000.md`
**Research:** `research/01-d1-d4-evidence.md`, `research-notes.md`

---

## Scope of checks

1. Every finding D1/D2/D3/D4 has corresponding task items that act on it per the research.
2. The exact CODE-VERIFIED anchors appear in the relevant item Context/Action fields and are not corrupted/fabricated — re-verified against live source.
3. D1 design (a) vs (b) both captured; no item silently picks one.
4. D4 correctly encoded as NO-code-fix / verification-only.
5. D3 replacement-citation targets actually exist on disk.

---

## Check 1 — Every finding D1–D4 has corresponding task items

| Finding | Research action | Task item(s) | Aligned? |
|---|---|---|---|
| D1 (load-bearing) | HALT design (a)/(b) → impl → falsifier test → sync | Phase 2 (2.1 HALT record, 2.2 HALT gate), Phase 3 (3.1 falsifier test, 3.2 impl, 3.3 SKILL.md+sync, 3.4 verify) | YES |
| D2 (NON-BLOCKING) | Reconciliation/doc note, out-of-tree, do not edit sibling | Step 5.1 — produces note, explicitly NON-BLOCKING, MUST NOT edit sibling | YES |
| D3 (LOW) | Rewrite `:133` citation to resolvable sources + sync | Step 4.1 (rewrite + on-disk verify), 4.2 (sync) | YES — but see Check 5 (premise defect) |
| D4 (NON-BLOCKING) | NO code fix; verify EXEMPT label; follow-up only | Step 5.2 — verify-only, explicit "MUST NOT modify test" | YES |

All four findings are acted on by dedicated task items. No finding was dropped. **PASS (coverage).**

## Check 2 — CODE-VERIFIED anchors: re-verified against live source

Every anchor the QA brief named was re-grepped against the live tree (worktree `reflect-reviewer-guard`):

| Anchor (research) | Live grep result | Match? |
|---|---|---|
| `ensemble.py:218` `"target": str(config.tasklist_path)` | `218:            "target": str(config.tasklist_path),` | EXACT |
| `ensemble.py:315-316` `"snapshot" if … else "disabled"` | `316:            "snapshot" if config.reviewer_grounding_root else "disabled"` (ternary spans 315-316) | EXACT |
| `ensemble.py:433-441` `_load_review_target()` reads `tasklist_path` | `433:def _load_review_target`, `438`/`441` read `config.tasklist_path` | EXACT |
| `ensemble.py:366` adversarial scorer `cwd=config.reviewer_grounding_root` | `366:        cwd=config.reviewer_grounding_root,` | EXACT |
| `ensemble.py:415` `build_worker_prompt()` | `415:def build_worker_prompt(config: ReflectConfig) -> str:` | EXACT |
| `runner.py:441-461` Tier-1 audit child grounding | `cwd=config.reviewer_grounding_root` at `:461`; `ClaudeProcess(...)` opens at `:441`. Range brackets the construction correctly. | OK (range, not single line) |
| `SKILL.md:268` Step 0.5e item 4 "receive review targets derived from `<snapshot>`" | `268:` matches verbatim incl. swarm-worker clause | EXACT |
| `reflect-reviewer.md:133` cites `pr199-reflect-hardening-proposal-2026-06-22.md` as primary source | `133:` matches; cites that proposal + demotes round-2 findings | EXACT |

The anchors in the task's Context/Action fields are NOT corrupted or fabricated; they reproduce live source faithfully. **PASS (anchor fidelity).**

Note: the task does NOT hardcode line numbers into edit items — Step 1.3 re-confirms anchors live and writes `anchor-confirmation.md`; Step 3.2 reads that file for current line numbers. Correct line-drift hygiene (no stale `:NNN` baked into an Edit instruction).

## Check 3 — D1 design (a) vs (b) both captured; no silent pick

- Research records BOTH (a) full grounding redirect and (b) telemetry-honesty narrowing, with (b) a non-binding recommendation.
- Task Step 2.1 mandates recording **both** designs verbatim with exact edit sites + three-site classification + explicit "recommendation does NOT authorize adoption" + empty `OPERATOR DECISION:` block.
- Task Step 2.2 is a hard HALT gate: if `Chosen design:` empty or `status: PENDING`, set `⚪ Blocked` and STOP; "under no circumstances is a design auto-selected by the executor."
- Phase 3 items branch on the chosen design, executing ONLY that design's edit sites.

No task item silently picks a design. Faithfully matches memory `feedback_human_decision_items_must_halt`. **PASS.**

## Check 4 — D4 encoded as NO-code-fix / verification-only

- Research: D4 reclassified Drift→Authorized; "Fix: NONE required"; EXEMPT label sanctioned by parent Key Constraint.
- Task Step 5.2: verification-only, "YOU MUST NOT modify `test_reviewer_finding_parity.py`"; records EXEMPT-label text + PASS/FAIL + Follow-Up as OPTIONAL.
- Live source confirms the EXEMPT label is present and correctly worded (`test_reviewer_finding_parity.py` docstring 13-17: "falsifier-EXEMPT … reachability INVARIANT over the seeded fixtures, not a layer-landing guard").
- Task did NOT invent any code change to the parity test.

**PASS — no fabricated code change.**

## Check 5 — D3 replacement-citation targets exist on disk — DEFECT FOUND

On-disk reality (verified via `ls`/`find`/`git ls-files`):

| File | `reflect-reviewer-guard` worktree (where the tracked agent lives) | canonical root `/config/workspace/IronClaude` | git-tracked |
|---|---|---|---|
| `pr199-reflect-hardening-proposal-2026-06-22.md` (the "non-existent" cited proposal) | absent | **EXISTS (31 KB)** | untracked |
| `.dev/reflect-hardening/pr199-round2-findings/` (proposed replacement) | **absent** | **absent** (exists ONLY in sibling `ReflectHardening-3`) | untracked |
| `pr199-reflect-damage-report-20260622.md` (proposed replacement) | EXISTS | absent | **tracked** |
| `pr199-reflect-subagent-forensics-2026-06-22.md` (proposed replacement) | EXISTS | absent | **tracked** |
| BUILD_REQUEST-reflect-reviewer-guard (proposed replacement) | absent | EXISTS | untracked |

**GAP-1 (IMPORTANT) — Research D3 premise is factually wrong at the canonical root.** Both research files and the task description assert the cited proposal `.dev/analysis/pr199-reflect-hardening-proposal-2026-06-22.md` "DOES NOT EXIST." It DOES exist (31 KB) at the canonical repo root `/config/workspace/IronClaude`; it is merely untracked and absent from this worktree's checkout. The research/REPORT conflated "not resolvable from this worktree" with "does not exist." The agent file `reflect-reviewer.md:133` itself already states the correct nuance ("untracked working-tree artifacts at the canonical repo root … not resolvable from this tracked agent file's worktree"). The task inherited the research's overstatement.

**GAP-2 (IMPORTANT) — A prescribed D3 *replacement* target is non-resolvable, undercutting the fix.** Research/task instruct rewriting `:133` to cite `.dev/reflect-hardening/pr199-round2-findings/` as a resolvable source. That directory does NOT exist in this worktree NOR at the canonical root — only in sibling worktree `ReflectHardening-3`. Citing it reproduces the exact defect D3 targets: a citation that does not resolve from the tracked agent file. Of the proposed replacements, only TWO are robustly resolvable from every worktree: the git-tracked forensics docs `pr199-reflect-damage-report-20260622.md` and `pr199-reflect-subagent-forensics-2026-06-22.md`. The BUILD_REQUEST and the round2-findings dir are both untracked and absent from this worktree.

**Mitigating factor:** Step 4.1 DOES instruct an on-disk `ls`/`test -e` verification of replacement sources before editing, with "If a replacement source unexpectedly does not exist on the current tree, record the discrepancy and log the specific blocker." An executor following that clause literally would catch GAP-2 at runtime. BUT the same item's prescriptive clause pre-names `.dev/reflect-hardening/pr199-round2-findings/` as a source to cite — steering toward a non-resolvable path. The runtime check and the prescriptive citation list are in tension; the outcome (non-resolvable citation written, or blocker logged) depends on which clause the executor weights.

## Additional observations (adversarial sweep)

- **OBS-1 (MINOR) — runner.py `:441-461` is a 21-line range for one grounding line.** Actual `cwd=config.reviewer_grounding_root` at `:461`; `:441` opens the `ClaudeProcess(...)` ctor. Range is defensible (brackets the grounded-child construction) and is read-only reference for D1 — not corruption, just imprecise vs the single-line `ensemble.py:366` scorer anchor. No action.
- **OBS-2 (MINOR) — `reviewer_isolation` enum drift.** Research notes say `{disabled, snapshot, stopped-precondition}`; live `models.py:139-141` documents `disabled | snapshot` (default `"disabled"`, `str`, no hard enum). Step 1.3 instructs listing the CURRENT enum verbatim from live source, so this is self-correcting at runtime. No action.
- D1/D2/D4 anchors and encodings are otherwise faithful — no fabrication in the load-bearing D1 path, the D2 out-of-tree framing, or the D4 verify-only framing.

---

## VERDICT: FAIL

Strongly aligned on D1 (load-bearing), D2, and D4 — all anchors re-verified EXACT against live source, both D1 designs captured, the HALT genuinely encoded, D4 correctly kept as a no-code-fix verification, and no fabricated code changes. However the D3 strand carries two inherited research-misrepresentation defects that meet the adversarial bar:

- **GAP-1 (IMPORTANT):** Research/task assert the cited proposal "does not exist"; it DOES exist at the canonical repo root (untracked, worktree-absent). Premise overstated.
- **GAP-2 (IMPORTANT):** A prescribed D3 replacement citation (`.dev/reflect-hardening/pr199-round2-findings/`) is non-resolvable from this worktree and the canonical root (sibling-only), so the prescribed fix would re-introduce the unresolvable-citation defect D3 targets. Only the two git-tracked forensics docs are worktree-portable.

Plus 2 MINOR observations (OBS-1, OBS-2), both self-correcting via runtime re-verification items.

**Required corrections (D3 only):**
1. Correct the D3 premise (task + ideally research): the proposal is untracked-and-worktree-absent, not non-existent. The fix is still valid (the tracked agent file must cite worktree-resolvable sources) but on the right rationale.
2. Narrow Step 4.1's prescribed replacement citation to the TWO git-tracked, worktree-portable forensics docs (`pr199-reflect-damage-report-20260622.md`, `pr199-reflect-subagent-forensics-2026-06-22.md`). Drop, or explicitly mark canonical-root-only, the untracked `pr199-round2-findings/` dir and the BUILD_REQUEST, so the executor cannot write another non-resolvable citation.

The mitigating runtime `ls`/`test -e` check in Step 4.1 reduces but does not eliminate the risk, because the item's prescriptive citation list still names the non-resolvable path.
