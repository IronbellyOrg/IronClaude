# Phase 1 Context — Should `/sc:reflect` (or its agents) be wired into `/sc:auggie-review` and/or `/sc:cleanup-audit`?

**Date:** 2026-06-04
**Mode:** READ-ONLY investigation. No skill/protocol file was edited.
**Method:** Three parallel `audit-analyzer` subagents (Grep + Read for exact line numbers) + direct orchestrator re-Read of decision-critical citations + two prior-art reads.

> **Citation-freshness note.** `sc-reflect-protocol/SKILL.md` was modified 2026-06-04 00:25. The first subagent pass cited the reflect reusable-agent table at `:415`; an orchestrator re-grep showed `:415` is actually `### 5.5 Why these thresholds` and the table row is at **`:561`** (~146 lines of drift). **All `sc-reflect-protocol/SKILL.md` line numbers below are the re-verified values**, not the subagent's first-pass numbers. The auggie-review and cleanup-audit citations were spot-checked and held.

---

## 0. The central tension (the only question that matters here)

Both target protocols **already contain an independent verification mechanism**:

- **`sc:auggie-review`** runs the **`auggie-reviewer` agent BLIND** in `--depth deep` — a Claude-side review pass that never sees Auggie's findings before returning its own, so cross-source agreement is real signal, not anchoring (`src/superclaude/agents/auggie-reviewer.md:20`; spawned at `sc-auggie-review-protocol/SKILL.md:181`).
- **`sc:cleanup-audit`** runs the **`audit-validator` agent** — a 10% stratified spot-check that re-tests every sampled claim from scratch (`src/superclaude/agents/audit-validator.md:14,18`; spawned at `sc-cleanup-audit-protocol/SKILL.md:69`).

So the question is **NOT** "is independent review valuable" (both already buy it). The real question is:

> **Does `/sc:reflect` — or one specific reflect agent — add something the EXISTING mechanism lacks, net of the overlap cost (tokens, latency, a new cross-skill dependency, and double-validation)?**

The single sharpest overlap fact: **reflect itself already reuses `audit-validator`** (`sc-reflect-protocol/SKILL.md:561`, also `:1043`). So "drop reflect into cleanup-audit for independent validation" risks wiring a skill *whose validator is the exact agent cleanup-audit already runs* — a circular overlap. Conversely reflect's *distinctive* assets — the heterogeneous-reviewer ensemble, blind `confidence-calibrator`, and the mandatory `evidence-validator` gate — are the parts that could add genuinely new coverage.

---

## 1. `sc:auggie-review` — ground truth

### 1.1 Wave structure (5 waves)
Five waves with explicit entry/exit criteria; refs loaded per-wave (`SKILL.md:62,64`).

| Wave | Purpose | Anchor |
|---|---|---|
| Wave 0 | Resolve & validate target (mode classify, env prereqs `command -v auggie` / `git rev-parse` / `gh auth status`, slug, target header) | `SKILL.md:67,76,82–92,106` |
| Wave 1 | Collect inputs (diff body, file list, PR metadata, chunking strategy; thresholds: ≤1500 lines or ≤15 files single-shot; 1500–5000/16–30 directory-chunk; STOP >5000 unless `--force`) | `SKILL.md:68,110–130` |
| Wave 2 | Auggie deep pass (`--print --output-format json --ask --workspace-root`, depth-scaled `--max-turns`; prompt grounds every finding in real `file:line`; `--ask` = retrieval/non-editing only) | `SKILL.md:69,134–155,143,145,183` |
| Wave 3 | Validate & synthesize (parse JSON → **file:line validation pass** → dedupe → severity remap → persona cross-check → compose `REVIEW.md`) | `SKILL.md:70,196–214,281` |
| Wave 4 | Post & handoff (post comment-only PR review — never `--approve`/`--request-changes`; offer remediation; return contract) | `SKILL.md:71,295–330,313` |

### 1.2 The `auggie-reviewer` agent — the EXISTING independent verifier
- "Independent code-review specialist" running a Claude-side pass alongside Auggie's retrieval pass, **deep mode only** (`auggie-reviewer.md:2–3`; spawn at `SKILL.md:181`).
- **Runs blind:** depth is always `deep`; works "without seeing Auggie's findings"; "any agreement is real signal, not anchoring" (`auggie-reviewer.md:20,31,104`).
- Targets what indexed retrieval misses: subtle invariants, intent-vs-implementation gaps, comment/code contradictions (`auggie-reviewer.md:18`).
- Wave 3 marks each finding `source: auggie-only | claude-only | both` (`SKILL.md:212–213`); the severity rubric gives a deep-mode cross-source agreement bonus — both-source findings get no downgrade; single-source drop one tier unless a category floor holds (`refs/severity-rubric.md:97–99`).

### 1.3 Wave 3 finding-validation — INLINE Read, NOT a dedicated agent
- "**File:line validation pass** (non-negotiable): For each finding, `Read` the cited file at the cited line range. Confirm the line exists and (where possible) confirm the cited snippet actually appears" (`SKILL.md:204–205`). *(Orchestrator-re-verified.)*
- PR/diff mode also checks the line is within diff hunks; else downgrade/drop (`SKILL.md:206`).
- `needs-grounding` findings (missing file/line) are grounded via `mcp__auggie__codebase-retrieval` or `Grep`, promoted if found, else dropped + logged (`SKILL.md:203,207`).
- **This is an inline orchestrator pass — there is no separate validator agent for citations.** The `auggie-reviewer` agent is a *content* cross-check (does an independent reviewer find the same issues), not a *citation* re-Read.

**Severity rubric** (`refs/severity-rubric.md`): Critical (blocks merge: exploitable security, data-integrity, crash-on-default-path, compliance — `:13–20`); High (fix before merge: latent security, non-default-path correctness, leaks, API breaks, concurrency, arch drift — `:24–33`); Medium (`:37–45`); Low (`:47–53`); Nit (never inline-commented, never blocks — `:55–61`). Remap algorithm: Auggie hint → category override → confidence adj → diff-locality adj → deep-mode cross-source bonus (`:63–99`); Auggie severity is a hint, not authoritative (`:3`, `SKILL.md:211`).

### 1.4 The remediation chain ALREADY invokes `/sc:reflect` (orchestrator-verified)
Wave 4 remediation offer fires only if `--remediation-offer` AND `critical + high > 0` (`SKILL.md:318`). On accept:
- Phase A → `/sc:design` (`SKILL.md:322`)
- Phase B → `task-builder` (`SKILL.md:323`)
- **Phase C → `/sc:reflect --type task --analyze`** against the new task file (`SKILL.md:324`, re-verified); flagged issues surfaced to user (`:325`)
- Phase D → user-driven `/task` execution (`SKILL.md:326`)
- **Phase E → `/sc:reflect --type task --validate`** before commit; **block on validation failures** (`SKILL.md:327`, re-verified)

Mirrored in `refs/remediation-handoff.md:30–31,35–36,102–107,144–159`. **Key fact: auggie-review is already a reflect *consumer* — but only in the post-review remediation tasklist, NOT in the review-finding validation itself (Wave 3).**

---

## 2. `sc:cleanup-audit` — ground truth

### 2.1 3-pass structure + agents
| Pass | Purpose | Agent | Anchor |
|---|---|---|---|
| Pass 1 Surface | Classify every file DELETE/REVIEW/KEEP; obvious waste | `audit-scanner` | `SKILL.md:68,113`; `rules/pass1-surface-scan.md:5`; `audit-scanner.md:14` |
| Pass 2 Structural | Mandatory 8-field profiles; placement, staleness, broken refs (KEEP/REVIEW only, excludes Pass-1 DELETEs) | `audit-analyzer` | `SKILL.md:121`; `rules/pass2-structural-audit.md:5`; `audit-analyzer.md:24,30` |
| Pass 3 Cross-cutting | Duplication matrix w/ overlap %, sprawl, cross-dir broken refs | `audit-comparator` | `SKILL.md:129`; `rules/pass3-cross-cutting.md:5`; `audit-comparator.md:14` |
| Fan-in | Merge batch reports → pass summaries → final report (`--pass all`) | `audit-consolidator` | `SKILL.md:70,137`; `audit-consolidator.md:14` |

### 2.2 The `audit-validator` agent — the EXISTING independent verifier
- Spawned in the Validate step for **10% spot-check (5 findings per 50 files)** + grep-claim verification (`SKILL.md:69,94`).
- **Independence:** "Do NOT assume the prior agent was correct. Verify everything from scratch" (`audit-validator.md:18`); "re-test claims from scratch" (`:14`).
- **Stratified sample:** ≥1 DELETE (if any), ≥1 KEEP, ≥1 FLAG/REVIEW (if any), remainder random (`audit-validator.md:34,36–39`).
- **4-check methodology:** (1) Grep Claim Verification `:45`; (2) File Content Verification `:52`; (3) Classification Accuracy `:59`; (4) Evidence Completeness `:67`.
- **Pass/fail:** PASS <20% discrepancy; FAIL ≥20% → re-audit batches; critical-fail on false-negative DELETEs / wiring false-negatives (`audit-validator.md:140–145`).

### 2.3 Evidence-gating + quality gates
- Per-finding gate: "Every DELETE requires grep proof; every KEEP requires reference citation; every CONSOLIDATE requires overlap quantification" (`SKILL.md:75`).
- No DELETE without "grep proof of zero references" + dynamic-loading check (`SKILL.md:150–151`; `rules/dynamic-use-checklist.md:5,9,124–128`; `rules/verification-protocol.md:20–25,78,83`).
- Quality gates (`templates/pass-summary.md:79–89`): all batches complete · required sections present · mandatory profiles complete · spot-check validation · coverage threshold met. Failed reports regenerate (`SKILL.md:69`; `templates/finding-profile.md:5,28–32,54–58`).

---

## 3. `sc:reflect` reusable agents — which are truly standalone (corrected citations)

| Agent | Role (cite) | Tools | Standalone Task-spawnable by another protocol? |
|---|---|---|---|
| **confidence-calibrator** | Re-grades a hypothesis card vs a 5-dim rubric; returns calibrated confidence + escalation (`confidence-calibrator.md:3`) | `Read` (`:5`) | **YES** — "Delegable by any other skill that produces a hypothesis card + rubric pair" (`:16`); "always invoked via `Task` with explicit `card_path` and `rubric_path`" (`:17`); self-contained inputs (`:47–51`) |
| **evidence-validator** | Last-gate validator; re-Reads every file:line citation in a draft report, drops unfounded items (`evidence-validator.md:3`) | `Read, Grep, Glob` (`:5`) | **YES** — "designed to be reusable by any skill that produces an evidence-cited report" (`:3`); "Delegable by any other skill…" (`:16`); "always invoked via `Task` with an explicit `report_draft_path`" (`:17`); generic inputs (`:37–44`) |
| **audit-validator** | Spot-check validator; re-tests audit findings independently (`audit-validator.md:3,12–14`) | `Read, Grep, Glob` (`:4`) | **YES** (audit-finding workflows) — self-contained inputs (`:24–30`); read-only (`:20–22`). Caveat: no explicit "invoked via Task" line; conclusion from the generic contract |
| **root-cause-analyst** | Evidence-based root-cause investigation + hypothesis testing (`root-cause-analyst.md:3`) | No explicit `tools:` line in frontmatter (`:1–5`) | **CONDITIONAL** — conceptually portable for debugging (`:9–14,28–42`) but needs supplied problem context + runtime-granted tools |
| **self-review** | Post-implementation validation & reflexion partner (`self-review.md:3`) | No explicit `tools:` line (`:1–5`) | **CONDITIONAL** — needs caller-supplied task summary + diff + test evidence (`:22–25`) |
| **rf-qa** | Rigorflow intra-task QA (research/synthesis/report/task-integrity gates) (`rf-qa.md:3`) | Large set incl. Read/Write/Edit/Bash/Task/Skill (`:6–33`) | **CONDITIONAL** — needs caller-supplied phase + scope + criteria + `fix_authorization` (`:41–50,232–242`); supports parallel partitioning (`:52–68`) |

### 3.1 Reflect-internal reuse (the overlap signals) — corrected line numbers
- **Tier/Wave map** (`SKILL.md:142–155`): Wave 1 = Tier 1 grounded single-agent (`root-cause-analyst` OR `self-review`, `:140`-ish region) + blind `confidence-calibrator` (`:147`); Wave 3 = Tier 2 parallel heterogeneous reviewers (`:149`) + per-card blind calibration `×N` with disjoint-set rule (`:152`); Wave 4 = adversarial merge via sc-adversarial Mode A (`:154`); **Wave 5 = Synthesis + Evidence-Validator Gate + Report (`:155`)**.
- **Heterogeneous reviewer ensemble** — Tier 2 reviewers on different model classes "so per-model representational bias does not stack"; merge judge deliberately a different class than every debater (`SKILL.md:33`); reviewers heterogeneous by model class AND persona (`:570`).
- **Blind calibration** — `confidence-calibrator` re-grades each reviewer's findings without formation context; merged verdict weights calibrated, not self-reported, scores (`SKILL.md:34`); the "dominant anti-anchoring mechanism", calibrator-model ≠ reviewer-model (disjoint-set §11.3) (`:558`).
- **Mandatory evidence-validator gate** — every file:line in the merged report independently re-Read; unfounded citations *dropped, not downgraded*; "A report that ships with no dropped citations is treated as suspicious, not clean" (`SKILL.md:35`); "Non-negotiable final gate" (`:562`); skill-level dependency at Wave 5 (`:607`).
- **★ Reflect reuses `audit-validator` ★** — "`audit-validator` | 5 | UC-2 (large) | When Wave 5 produces ≥20 findings, 10% random spot-check before report ships (lighter alternative to full evidence-validator pass)" (`SKILL.md:561`); also a 10% audit-validator spot-check on the long-tail citations (`:1043`). **This is the circular-overlap signal with cleanup-audit.**

---

## 4. Prior art (so we don't re-derive)

### 4.1 `.dev/brainstorms/sc-reflect-rebuild/integration-analysis.md`
Analyzed wiring reflect into **sprint / roadmap / task** (NOT review/audit). Key transferable framings:
- **Variant A (additive, lower risk)**: keep existing validators, ADD reflect as an extra step (`integration-analysis.md:283–301`).
- **Variant B (replacement, higher leverage)**: replace the bespoke validator block with a single `/sc:reflect --mode post` that subsumes it via the heterogeneous ensemble — flagged as "more rigorous… but the existing machinery already works, and reflect is new + unproven" (`:299`).
- Recommended **Variant A first, Variant B as follow-on once reflect proves out** (`:301`).
- **Open Question #6 (rf-qa vs reflect overlap)**: "doing both is 2-3× the token cost of doing one well" (`:357`) — the exact cost objection that applies here.
- Reflect Tier-2 cost cited at **35–70k Claude + 10–25k auggie tokens** (`:347`).

### 4.2 `.dev/releases/backlog/TaskQAComparison/adversarial/refactor-plan.md`
The "bolt reflect onto an existing QA surface for the disjoint-set property" argument, Change #9 (CRITICAL):
- INV-006 sufficiency-challenge (HIGH, **unaddressed across all 3 QA variants**) BLOCKED convergence — no variant had a structural self-confirmation-bias defense (`refactor-plan.md:83`).
- **Empirical anchor: R0 PR #112** — inline rf-qa's fix passed inline-rf-qa's surface signal but **missed the underlying defect `/sc:reflect --mode post` caught** (`:83`). This is the strongest *pro-integration* evidence in the repo.
- Integration approach: spawn `/sc:reflect --mode post --depth deep` against QA-resolved outputs, in a **different context window** than the verifier → the **calibrator-disjoint-set property** the inline verifier lacks (`:84`).
- Cost: **+10–30K tokens per STRICT-tier task**, new dependency on reflect availability; mitigated by tier-routing (fires only on STRICT) (`:85,139`).
- Corroborated by memory `feedback_sc_reflect_vs_inline_rfqa.md`: sc:reflect caught blindspots past clean inline rf-qa runs **twice** (R0/PR#112 and TASK-RF-20260602-135209).

---

## 5. Synthesis — what reflect adds vs. what already exists

| Property | auggie-review HAS | cleanup-audit HAS | reflect ADDS (net-new) |
|---|---|---|---|
| Independent content review | ✅ `auggie-reviewer` blind pass (deep) | ✅ `audit-validator` spot-check | Heterogeneous *multi-model* ensemble (2–3 classes) — neither target uses >1 model class |
| Citation re-Read gate | ✅ inline Wave-3 Read (orchestrator, same context) | partial (validator re-greps sampled findings) | `evidence-validator` as a **dedicated, disjoint-context** gate that drops-not-downgrades |
| Blind calibration | ❌ (severity remap is rubric-based, not blind-recalibrated) | ❌ | `confidence-calibrator` blind re-grade (anti-anchoring) |
| Disjoint-context verification | ⚠️ blind agent but same orchestrator drives synthesis | ⚠️ validator samples 10%, same run | Full out-of-context pass (the R0/PR#112 property) |
| Cost | low (1 extra agent in deep) | low (1 sampled validator) | **high: 35–70k + 10–25k auggie (Tier 2)** |
| Already depends on reflect? | ✅ YES — remediation Phases C/E | ❌ no | — |
| Shares an agent with reflect? | no | ✅ **`audit-validator`** (circular-overlap risk) | — |

**Decision-relevant asymmetries between the two targets:**
1. **auggie-review already consumes reflect** (remediation Phases C/E) but only *post-review on the fix tasklist*, not on the *review findings*. Its Wave-3 citation validation is a same-context inline Read — the one place a disjoint-context `evidence-validator` could add real value cheaply.
2. **cleanup-audit's validator IS the agent reflect reuses** (`audit-validator`). Wiring full `/sc:reflect` into cleanup-audit would partly re-invoke the agent cleanup-audit already runs — high circular-overlap, low marginal value. A *single* reflect agent (`evidence-validator`, which audit doesn't use) is the only non-circular add.
3. The strongest pro-integration evidence (R0/PR#112) is about **task-execution QA**, not read-only review/audit. Review/audit findings are *recommendations*, not *applied changes* — the "fix passed surface signal but missed the defect" failure mode is weaker when nothing was changed.

This sets up three mutually-exclusive proposals: **A** (additive single agent at the existing seam), **B** (replace the bespoke validator with `/sc:reflect --mode post`), **C** (reject — existing mechanisms suffice).
