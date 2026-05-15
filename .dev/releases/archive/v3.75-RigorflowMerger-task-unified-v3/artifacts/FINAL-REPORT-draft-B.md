# FINAL REPORT — Draft B (Decision-Ready)

> Synthesizer S-B. Optimized for scan-and-decide. Capability matrix + risks + open questions dominate. Brevity over exhaustiveness.

Status legend: ✅ adopted (already in `/sc:task`) | ⚠ partial (present but incomplete) | ❌ missing (worth merging) | 🛑 blocked (depends on a prior decision)

Effort labels: **S** ≤½ day | **M** 1-3 days | **L** >3 days

---

## 1. Scope

**TL;DR.** Merge the historically-distinctive strengths of `/sc:task-unified` into canonical `/sc:task` without regressing the v3.7 canonicalization (which already removed `/sc:task-unified` as a live command). The merge surface is small: tier classification rigor (CRITICAL FAIL conditions, output-type-specific gates, six universal quality principles, anti-sycophancy as a gate, mandatory completion checklist, deterministic low-confidence BLOCKED state). Sprint-executor adoptables (per-item UID, batch immutability, three-mode resume, fail-closed verdict) are in scope because the sprint executor consumes `/sc:task` and shares its tier vocabulary.

**Non-goals.**
- Reintroducing `/sc:task-unified` as a live command name (regresses v3.7 — see §9).
- Wholesale adoption of LW/Rigorflow's bash orchestrator or its multi-backup versioning strategy (R1).
- Replacing the keyword-scoring classifier with semantic NLP (out of scope; tracked as longstanding limitation).
- Rewriting TFEP or the diagnostic chain.
- Migrating away from Python supervisor model for sprint executor.

---

## 2. Source index

| ID | File | Role |
|----|------|------|
| R1 | `artifacts/wave1-extracts.md` §R1 | comparison-sprint-executor |
| R2 | `artifacts/wave1-extracts.md` §R2 | comparison-task-unified-tier |
| R3 | `artifacts/wave1-extracts.md` §R3 | improve-sprint-executor |
| R4 | `artifacts/wave1-extracts.md` §R4 | improve-task-unified-tier |
| R5 | `artifacts/wave1-extracts.md` §R5 | strategy-ic-sprint-executor |
| R6 | `artifacts/wave1-extracts.md` §R6 | strategy-ic-task-unified |
| R7 | `artifacts/context-task-current-state.md` | `/sc:task` current state |
| R8 | `artifacts/context-task-unified-current-state.md` | `/sc:task-unified` historical state + prior art |

---

## 3. `/sc:task-unified` inventory — historical strengths worth preserving

> Scoped to merge-relevant capabilities, not full surface. `/sc:task-unified` no longer exists as a live command (R8 §1); these are the qualities the merger must consolidate into `/sc:task`.

| # | Historical strength | Source | Status today |
|---|---------------------|--------|--------------|
| H1 | CRITICAL FAIL conditions (Sequential/Serena unavailable, output absent, classification header absent → unconditional FAIL) | R4 (TU-001), R8 §4 | ⚠ partial — only MCP unavailability blocks (R7 §3 SKILL.md:253-263) |
| H2 | Output-type-specific gates (code / analysis / documentation / opinion) | R4 (TU-002), R2 | ❌ missing (R7 §5 issue 6) |
| H3 | Six universal quality principles as NFR baseline (Verifiability, Completeness, Correctness, Consistency, Clarity, Anti-Sycophancy) | R4 (TU-003), R2 | ❌ missing |
| H4 | Anti-sycophancy as a universal gate principle | R2 | ❌ missing |
| H5 | Mandatory task completion checklist (six conditions before "complete") | R2 | ❌ missing |
| H6 | Deterministic low-confidence BLOCKED state (with computed tier + competing tier + split keywords) | R4 (TU-004) | ⚠ partial — currently "prompt user" (R7 §2 task.md:91) |
| H7 | Three-tier severity model (Sev 1 block / Sev 2 cycle / Sev 3 advisory) | R2, R3 | ❌ missing as named taxonomy |
| H8 | Original orthogonal `--strategy` × `--compliance` design | R6, R8 §4 v2.0 spec | ✅ already canonical (R7 §1) |
| H9 | Automatic tier classification with confidence scoring | R6 | ✅ adopted (R7 §2 ORCHESTRATOR.md:151-213) |
| H10 | Critical path filesystem override (`auth/`, `security/`, `crypto/`, `models/`, `migrations/`) | R6 | ✅ adopted (R7 §2 SKILL.md:120-123) |

---

## 4. `/sc:task` inventory — strengths + gaps relevant to merge

### Strengths to preserve (do not regress)

| Capability | Source | Why it matters for merge |
|------------|--------|--------------------------|
| Automatic tier classification with confidence + compound-phrase overrides | R7 §2 task.md:69-91, ORCHESTRATOR.md:151-213 | Eliminates manual gate selection — strictly stronger than LW's manual model (R2) |
| Priority resolution `STRICT > EXEMPT > LIGHT > STANDARD` | R7 §2 | Deterministic; fail-safe-upward |
| STRICT MCP block (Sequential + Serena, no fallback) | R7 §3 SKILL.md:253-263 | Already a safety decision LW has no equivalent for (R2 L79) |
| Per-tier execution recipes (STRICT 11-step, STANDARD 5-step, LIGHT 4-step, EXEMPT 2-step) | R7 §2 SKILL.md:76-123 | Concrete; programmatic — must remain after merge |
| Sprint CLI prompt builder emits canonical `/sc:task` | R7 §3 `cli/sprint/process.py:123-183` | v3.7 wiring — must not break |
| TFEP gates + forensic invocation chain | R7 §2 SKILL.md:125-244 | Out of scope to alter; merge must compose with it |
| Critical path override (auth/security/crypto/models/migrations/) | R7 §2 SKILL.md:120-123 | Semantic safety backstop beyond keyword matching |
| Classification header gate (HTML-comment block, first output) | R7 §2 task.md:50-67 | Hook into telemetry; merge candidate H6 should populate fields here |

### Gaps relevant to the merge

| # | Gap | Source | Touches merge candidate(s) |
|---|-----|--------|---------------------------|
| G1 | Only one CRITICAL condition (MCP unavailable). No output-absent or header-absent enforcement | R7 §5 issue 5 | H1 |
| G2 | No output-type axis — STRICT/STANDARD/LIGHT/EXEMPT applied uniformly to code, docs, analysis | R7 §5 issue 6 | H2 |
| G3 | Low-confidence "prompt" not deterministic — no blocked state with structured reason | R7 §5 issue 7 | H6 |
| G4 | No quality-principles NFR doc — verification agent has no shared check framework | R8 §4 TU-003 | H3, H4 |
| G5 | No mandatory completion checklist | R2 | H5 |
| G6 | Classification logic duplicated across command / skill / tasklist / orchestrator with keyword drift (`password, credential, secret, jwt, transaction, query` only in tasklist rules) | R7 §5 issue 4, R8 §6 issue 4 | All — sync risk amplifies any keyword change |
| G7 | Skill references nonexistent `config/` files (`tier-keywords.yaml` etc.) | R7 §5 issue 2 | Any keyword-table change must reconcile |
| G8 | Naming artifacts (`SC:TASK-UNIFIED:CLASSIFICATION` sentinel; `--caller task-unified`) — possibly telemetry compat | R7 §5 issue 1, R8 §6 issue 2 | Decide before formalizing classification header schema |
| G9 | Sprint executor: no intra-phase checkpoint; TurnLedger not persisted; coarse phase-level restart | R1, R3, R5 | Sprint-executor adoptables |

---

## 5. Overlap matrix — pivot capability × status × decision

| # | Capability | `/sc:task` (today) | Historical `/sc:task-unified` strength | Decision needed |
|---|-----------|--------------------|---------------------------------------|-----------------|
| C1 | Auto tier classification | ✅ | ✅ | None — already merged |
| C2 | Confidence threshold (0.70) | ⚠ prompts | ❌ historic (TU-004 proposes BLOCKED) | Adopt explicit BLOCKED state? |
| C3 | CRITICAL FAIL — MCP unavail | ✅ | ⚠ instructional only | None |
| C4 | CRITICAL FAIL — output absent | ❌ | ❌ proposed (TU-001) | Add as programmatic check? |
| C5 | CRITICAL FAIL — header absent | ❌ | ❌ proposed (TU-001) | Add as programmatic check? |
| C6 | Output-type axis (code/analysis/doc/opinion) | ❌ | ❌ proposed (TU-002) | Adopt; if so, does it modify tier routing or add a parallel axis? |
| C7 | Six quality principles NFR | ❌ | ❌ proposed (TU-003) | Adopt as quality-engineer agent check framework? |
| C8 | Anti-sycophancy gate | ❌ | ❌ proposed | Adopt as cross-cutting principle vs. STRICT-only? |
| C9 | Mandatory completion checklist | ❌ | ❌ proposed | Adopt; integrate with `think_about_whether_you_are_done`? |
| C10 | Sev 1/2/3 severity model | ❌ | ❌ proposed | Adopt as named taxonomy or fold into existing TFEP triggers? |
| C11 | Critical path FS override | ✅ | ✅ | None |
| C12 | Strategy × Compliance orthogonality | ✅ | ✅ | None — already canonical |
| C13 | STRICT MCP no-fallback block | ✅ | ⚠ behavioral | None |
| C14 | Sprint per-item UID tracking | ❌ | n/a (R1/R3 adoptable from LW) | Adopt for sprint executor? |
| C15 | Sprint sub-phase resume | ❌ | n/a | Adopt? Depends on C14 |
| C16 | Sprint three-mode execution (NORMAL/INCOMPLETE_RESUME/CORRECTION) | ❌ | n/a | Adopt? |
| C17 | Sprint fail-closed verdict (empty output ≠ PASS) | ⚠ unclear | n/a | Confirm or harden |
| C18 | Auto-diagnostic threshold (consecutive failures) | ❌ | n/a | Adopt? |
| C19 | TurnLedger persistence | ❌ | n/a | Adopt? Largest sprint-side risk (R1, R5) |
| C20 | Naming artifacts cleanup (`SC:TASK-UNIFIED:CLASSIFICATION`, `--caller task-unified`) | ⚠ carry-over | n/a | Keep for telemetry, or rename? |
| C21 | Classification logic deduplication (single source of truth) | ❌ drift across 4 locations | n/a | Adopt config/yaml extraction? Blocked on G7 |

---

## 6. Best-of-breed candidates — recommendations

> Every candidate has an explicit verdict. **ADOPT** = include in this release. **DEFER** = next release. **REJECT** = do not pursue.

### Tier-rigor candidates (from `/sc:task-unified` history)

| ID | Candidate | Verdict | Effort | Rationale |
|----|-----------|---------|--------|-----------|
| B1 | TU-001: CRITICAL FAIL dataclass + 3 conditions (MCP, output absent, header absent) | **ADOPT** | M | Closes G1; existing MCP block is foundation; additive — low blast radius (R4 risk Low). |
| B2 | TU-002: output-type-specific gate tables (code/analysis/documentation/opinion) | **ADOPT** | M | Closes G2; precision win over uniform tier overhead (R2 L71). Detection rules are deterministic (extension + deliverable). |
| B3 | TU-003: Six quality principles NFR section in skill | **ADOPT** | S | Closes G4; pure documentation addition consumed by quality-engineer agent (R4 risk Low). |
| B4 | Anti-sycophancy as universal gate | **ADOPT** | S | Subset of B3 but worth calling out — applies to LIGHT/STANDARD reviews too. |
| B5 | TU-004: deterministic BLOCKED state on confidence <0.70 | **ADOPT** | S | Closes G3; current "prompt" is non-deterministic. Block message includes tier/competing tier/split keywords. |
| B6 | Mandatory completion checklist (six conditions) | **ADOPT** | S | Closes G5; integrates with existing `think_about_whether_you_are_done`. |
| B7 | Sev 1/2/3 severity model (named taxonomy) | **ADOPT** | S | Closes part of G6 chain; aligns gate failures with TFEP triggers (R3 L109). |
| B8 | Reintroduce `/sc:task-unified` as live command | **REJECT** | — | Regresses v3.7 canonicalization (R8 §5 prior-art constraint). |
| B9 | Replace keyword classifier with NLP | **REJECT** | L | Out of scope; longstanding limitation (R6 L99); not a merge concern. |
| B10 | Extract tier keywords/weights to `config/*.yaml` (single source of truth) | **DEFER** | M | Closes G6/G7 but is its own release; touches 4 locations + sync pipeline. Worth a dedicated release. |
| B11 | Rename `SC:TASK-UNIFIED:CLASSIFICATION` sentinel + `--caller task-unified` | **DEFER** | S | Naming artifact only; functional. Touch alongside B10 to avoid telemetry break. |

### Sprint-executor candidates (R1/R3/R5 — consumer of `/sc:task`)

| ID | Candidate | Verdict | Effort | Rationale |
|----|-----------|---------|--------|-----------|
| B12 | Per-item UID on task records (`{phase_id}-{task_index:04d}`) | **ADOPT** | M | Closes G9 partially; stable identifier; LW pattern but as a Python field, not bash kvstore (R3 L44). |
| B13 | Sub-phase resume on `--start N` (resume at first non-DONE task) | **ADOPT** | M | Direct value to current pain: Phase 3/task 14 failure re-runs all 15 (R1 L66, R5 L77). Depends on B12. |
| B14 | Three-mode execution enum (NORMAL / INCOMPLETE_RESUME / CORRECTION) | **ADOPT** | S | Cleaner than implicit modes; needed by B13. |
| B15 | Fail-closed verdict on empty output file | **ADOPT** | S | Tightening — risk Low (R3 L34). |
| B16 | TurnLedger persistence to disk per state transition | **ADOPT** | M | Closes G9; largest sprint-side reliability gap (R1 L66, R5 L75). |
| B17 | `--auto-diagnostic-threshold N` (default 3 consecutive gate failures) | **DEFER** | M | New invocation path for diagnostic chain — wider blast radius (R3 L96). Defer until B12-B16 land. |
| B18 | `GateFailureSeverity` enum mapping to B7 Sev 1/2/3 | **ADOPT** | S | Couples cleanly with B7; deterministic default mapping per tier (R3 L109). |
| B19 | Adopt LW bash orchestrator / multi-backup strategy | **REJECT** | — | Explicit anti-pattern (R1 L64, L88). |
| B20 | Adopt LW Python-from-bash subprocess pattern | **REJECT** | — | Explicit anti-pattern (R1 L88). |

---

## 7. Risks

Prioritized by severity × likelihood.

| ID | Risk | Sev | Like | Blast radius | Owner | Mitigation |
|----|------|-----|------|--------------|-------|------------|
| R-1 | Regressing v3.7 canonicalization by reintroducing `/sc:task-unified` name in any new artifact | High | Med | Live command routing, telemetry, sprint CLI | Lead | Hard rule: `name: task` only. B8 REJECTED. Add CI grep for `/sc:task-unified` strings excluding documented carry-overs. |
| R-2 | Classification logic drift across 4 locations (command, skill, tasklist rules, orchestrator) — any keyword change risks divergence | High | High | All tier-routed tasks | Tier owner | B10 (config extraction) is the proper fix; until then, every keyword edit must touch all 4 files + run `make verify-sync`. |
| R-3 | Output-type axis (B2) modifies routing for documentation/analysis tasks — existing STRICT-tier doc tasks may re-evaluate to lower tier | Med | Med | Existing tasks classified STRICT | Tier owner | R4 L57. Stage rollout behind a flag; emit before/after tier in classification header. |
| R-4 | CRITICAL FAIL on "output absent" may false-positive on legitimate EXEMPT (no output expected) | Med | Med | EXEMPT tasks | Skill owner | Apply CRITICAL FAIL only to STRICT/STANDARD; EXEMPT exits before check. |
| R-5 | Naming artifacts (`SC:TASK-UNIFIED:CLASSIFICATION`, `--caller task-unified`) may be telemetry-load-bearing; renaming breaks dashboards | Med | Unknown | Telemetry/log parsers | DevOps | Inventory consumers before renaming. B11 DEFERRED until consumer audit complete. |
| R-6 | TurnLedger persistence (B16) introduces file I/O on hot path — may slow sprint execution | Low | Low | Sprint runtime | Sprint owner | Append-only JSON; benchmark before merge. |
| R-7 | Per-item UID + sub-phase resume (B12+B13) needs migration path for legacy result files lacking UIDs | Low | High | Resumed sprints | Sprint owner | R3 L55. Graceful fallback to full-phase restart when UIDs absent. |
| R-8 | Skill protocol references nonexistent `config/*.yaml` (G7) — drafting B10 may surface unexpected references | Low | High | Skill consistency | Skill owner | Audit refs in `SKILL.md:359-365`; either create files in B10 or remove dead references first. |
| R-9 | Six quality principles (B3) become checklist-theater if quality-engineer agent does not enforce | Med | Med | STRICT verification quality | Quality agent owner | Bind principles to specific verification steps; require evidence cite per principle. |
| R-10 | Auto-diagnostic threshold (B17 — deferred) when later adopted may flood diagnostic chain on flaky tests | Med | Med | Diagnostic chain | Sprint owner | Default threshold 3; cap diagnostic invocations per sprint. Out of scope for this release. |
| R-11 | Sequential + Serena hard requirement blocks STRICT tasks when servers degraded — could halt sprints | High | Low | All STRICT tasks during MCP outages | Ops | Already present in `/sc:task`; document operator escape via `--skip-compliance` (kept <12% target, R2 L27). |
| R-12 | `--skip-compliance` escape hatch can bypass newly added CRITICAL FAIL conditions (B1) — security hole if abused | High | Low | STRICT tasks | Lead | Require `--reason "..."` justification (already in COMMANDS.md:86-119); add audit log entry on use. |

---

## 8. Open questions — decision queue

| # | Question | Options | Recommendation | Blocking? |
|---|----------|---------|----------------|-----------|
| Q1 | Is output-type axis (B2) a **modifier** to tier routing, or a **parallel** dimension? | (a) modifier: tier → output-type-specific gate; (b) parallel: tier + output_type stored independently; (c) replace tier where applicable | **(a) modifier** — preserves existing tier surface; output_type detected after tier and selects which gate table to apply | **Y** |
| Q2 | Should anti-sycophancy (B4) apply at all tiers or only STRICT? | (a) all tiers; (b) STRICT+STANDARD; (c) STRICT only | **(a) all tiers** — R2 calls it "universal" gate principle | N |
| Q3 | Should naming artifacts (`SC:TASK-UNIFIED:CLASSIFICATION`, `--caller task-unified`) be renamed in this release? | (a) rename now; (b) keep + document; (c) defer to dedicated cleanup release | **(c) defer (B11)** — telemetry consumers unaudited; rename risk > benefit | **Y** — affects scope boundary |
| Q4 | Should tier keyword tables be extracted to `config/*.yaml` (B10) in this release or deferred? | (a) include in this release; (b) defer | **(b) defer** — own release; >4 locations; sync pipeline impact | **Y** — affects scope boundary |
| Q5 | Should CRITICAL FAIL "output absent" check apply to EXEMPT tasks? | (a) all tiers; (b) STRICT only; (c) STRICT+STANDARD | **(c) STRICT+STANDARD** — EXEMPT has no expected output | N |
| Q6 | When confidence <0.70 BLOCKED (B5), should `--skip-compliance` override BLOCK? | (a) yes (bypass everything); (b) no (BLOCK always wins); (c) yes but require `--reason` | **(c) yes with `--reason`** — preserves escape hatch; audits abuse | N |
| Q7 | Sev 1/2/3 model (B7) — should it replace existing TFEP escalation triggers or sit beside them? | (a) replace; (b) beside; (c) map TFEP → Sev | **(c) map** — TFEP unchanged operationally; Sev becomes the reporting taxonomy | N |
| Q8 | Sprint-executor adoptables (B12-B18) — same release as tier-rigor candidates, or a sibling release? | (a) same release; (b) split | **(b) split** — natural seam: tier rigor is `/sc:task` surface; sprint UID/resume is `cli/sprint/`. Different reviewers, different blast radius. Reference: `sc-release-split-protocol` | **Y** — affects release shape |
| Q9 | Six quality principles (B3) — encoded as agent prompt instructions or as a checklist artifact emitted by quality-engineer? | (a) prompt only; (b) checklist artifact only; (c) both | **(c) both** — prompt drives behavior; artifact provides audit trail | N |
| Q10 | Should mandatory completion checklist (B6) be enforced programmatically (block "complete") or via skill instructions? | (a) programmatic; (b) instructional | **(a) programmatic** — R4 L23 cites this as IC's edge over LW | N |

Blocking rows: **Q1, Q3, Q4, Q8** — these set scope boundaries; downstream candidate work cannot proceed without resolution.

---

## 9. Prior-art constraints from v3.7-task-unified-v2

> Source: R8 §5. Hard constraints inherited from the v3.7 canonicalization release. Violating any of these regresses prior work.

- **Canonical name is `/sc:task`.** `commands/task-unified.md` → `commands/task.md`; `skills/sc-task-unified-protocol/` → `skills/sc-task-protocol/`; old paths deleted. (`HANDOVER.md:51-60`)
- **Zero live `/sc:task-unified` references in `src/` or `.claude/`** (excluding documented carry-over strings). (`HANDOVER.md:64-71`)
- **`ClaudeProcess.build_prompt` must start with `/sc:task`.** (`TEST-SPEC.md:34-80`)
- **Sprint CLI prompt builder emits canonical `/sc:task`** (`cli/sprint/process.py:170`) — runtime integration already migrated; merge must not assume `/sc:task-unified` callsites exist.
- **Five cleanup_audit prompt builders also call `/sc:task`** (`cli/cleanup_audit/prompts.py:26, 47, 69, 92, 116`) — same constraint.
- **Documented carry-over strings (intentional, may be telemetry-load-bearing):**
  - `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` header sentinel (`task.md:58-67`)
  - `--caller task-unified` in TFEP forensic invocation (`SKILL.md:191-197`)
- **R1 ("Fix the Pipeline") / R2 ("Show the Pipeline") split** — R2 depended on R1; informs scope discipline (R8 §5 `release-split-report.md`, `boundary-rationale.md:55-65`).
- **R1 handoff criteria preserved**: `/sc:task` resolves correctly; zero remaining `sc:task-unified` references in `src/superclaude/` except listed historical artifacts.
- **CRITICAL constraint for this merger** (R8 §5): canonical surface must remain `/sc:task`; reintroducing `/sc:task-unified` as a separate live command would regress the v2/v3.7 collision fix unless explicitly designed as an alias or historical compatibility layer.
