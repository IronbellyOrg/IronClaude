# Feature Characterization — Compliance Gating

**Task:** T02.03 — Characterize MCP declarations, persona activation, allowed-tools, compliance gating, triggering surface
**Roadmap Item:** R-006
**Donor Catalog Anchors:** D04 (orthogonal-dimensions Strategy × Compliance), D07 (Flag set including `--compliance`, `--skip-compliance`, `--force-strict`, `--no-escalation`), D10 (per-tier dispatch), D16 (verification routing table), D27 (MCP circuit breaker) — see `donor-feature-catalog.md` lines 50, 53, 56, 67, 78
**Side of Truth (R-RULE-10):** `src/superclaude/commands/task.md` and `src/superclaude/skills/sc-task-protocol/SKILL.md` (canonical) — byte-identical to `.claude/` mirrors
**Generated:** 2026-05-15

---

## 1. What It Is

**Compliance gating** is the umbrella behavior that turns the tier label produced by classification (feature D09) into *enforcement actions* across five distinct gating surfaces:

1. **Dispatch gate** — terminates the command inline (EXEMPT/LIGHT) vs. invokes the protocol skill (STANDARD/STRICT).
2. **Verification routing gate** — selects verification method, token budget, and timeout per tier.
3. **MCP circuit breaker** — blocks STRICT if required servers are unavailable; permits degradation otherwise.
4. **TFEP enforcement** — applies the Test Failure Escalation Protocol's VIOLATION-level rules to STRICT and STANDARD only.
5. **Override flag set** — `--compliance`, `--skip-compliance`, `--force-strict`, `--no-escalation` allow the user to bypass or pin the gating.

Compliance gating is **not a single mechanism** — it is the coordinated effect of five separate rule sets keyed on the same tier label. The unifying claim is that "compliance tier is the load-bearing dimension that drives every downstream safety decision in `/sc:task`."

## 2. How It Works (Mechanism + Entry/Exit Conditions + `file:line` Evidence)

**Gate 1 — Dispatch (post-classification routing, `src/superclaude/commands/task.md:93-101`, `src/`):**

```
- EXEMPT: Execute immediately — no Skill invocation needed.
- LIGHT: Execute the change directly. No Skill invocation needed.
- STANDARD / STRICT: > Skill sc:task-protocol
```

- **Entry condition:** classification header has been emitted; tier value ∈ `{STRICT, STANDARD, LIGHT, EXEMPT}` is known.
- **Mechanism:** four-way switch on tier; two tiers terminate inline, two invoke the skill.
- **Exit condition:** either the command turn ends (EXEMPT/LIGHT) or the `sc:task-protocol` skill is invoked (STANDARD/STRICT).

**Gate 2 — Verification routing (`src/superclaude/skills/sc-task-protocol/SKILL.md:110-119`, `src/`):**

```
| Tier     | Method                          | Cost    | Timeout |
| STRICT   | Sub-agent (quality-engineer)    | 3-5K    | 60s     |
| STANDARD | Direct test execution           | 300-500 | 30s     |
| LIGHT    | Skip verification               | 0       | 0s      |
| EXEMPT   | Skip verification               | 0       | 0s      |
```

- **Entry condition:** dispatch landed in the skill (STANDARD or STRICT); the skill has reached Verification Phase (`src/superclaude/skills/sc-task-protocol/SKILL.md:110-119`, `src/`).
- **Mechanism:** tier-keyed selection of verification handler with associated budget and timeout.
- **Override:** Critical Path Override (`src/superclaude/skills/sc-task-protocol/SKILL.md:121`, `src/`) forces CRITICAL verification on `auth/`, `security/`, `crypto/`, `models/`, `migrations/` regardless of tier. Trivial Path Override (`src/superclaude/skills/sc-task-protocol/SKILL.md:123`, `src/`) permits skipping verification on `*.md`, `docs/`, `*test*.py`.
- **Exit condition:** verification either passes (proceeds to Completion Phase), fails (enters TFEP), or is skipped (LIGHT/EXEMPT).

**Gate 3 — MCP circuit breaker (`src/superclaude/skills/sc-task-protocol/SKILL.md:253-263`, `src/`):**

```
- STRICT: Sequential, Serena (fallback not allowed)
- STANDARD: Sequential, Context7 (fallback allowed)
- LIGHT/EXEMPT: None required
- If required servers unavailable for STRICT tier, block task execution
```

- **Entry condition:** skill invoked (post-dispatch).
- **Mechanism:** per-tier required-server check; STRICT fails closed, lower tiers degrade.
- **Exit condition:** `proceed` | `degrade` | `block` (see `feature-mcp-declarations.md`).

**Gate 4 — TFEP enforcement (`src/superclaude/skills/sc-task-protocol/SKILL.md:129-142`, `src/`):**

```
These rules apply to ALL compliance tiers that run tests (STRICT, STANDARD)
1. VIOLATION: must not fix code without TFEP completion.
2. VIOLATION: must not modify test expectations without adversarial validation.
3. VIOLATION: ad-hoc patches derived from test output are PROHIBITED.
```

- **Entry condition:** a test failure has occurred in Verification Phase on a STRICT or STANDARD tier task.
- **Mechanism:** Three VIOLATION-level prohibitions plus a six-row escalation gradient at `src/superclaude/skills/sc-task-protocol/SKILL.md:155-168` (`src/`).
- **Override:** `--no-escalation` flag (`src/superclaude/commands/task.md:48`, `src/`) bypasses TFEP triggers but voids TFEP protection.

**Gate 5 — Override flag set (`src/superclaude/commands/task.md:44-48`, `src/`):**

```
--compliance       Force tier (strict|standard|light|exempt|auto)
--skip-compliance  Bypass compliance entirely (escape hatch)
--force-strict     Force STRICT tier
--no-escalation    Bypass TFEP triggers
```

- **Entry condition:** parsed at command-invocation time (`src/superclaude/commands/task.md:69`, `src/`: "check `--compliance` override first").
- **Mechanism:** flags override the inferred tier or bypass an entire gate.
- **Exit condition:** if `--compliance` is present, classification is short-circuited and the explicit tier is used; if `--skip-compliance` is present, gates 2-4 are all bypassed; `--force-strict` pins to STRICT regardless of prompt content; `--no-escalation` disables Gate 4 only.

**Inter-gate sequencing:** Gates fire in this order during one `/sc:task` turn:

```
Override-parse (Gate 5) → Classification (D09) → Dispatch (Gate 1) →
  (if STANDARD/STRICT) Skill enters → MCP circuit-breaker (Gate 3) →
  Verification routing (Gate 2) → (on test failure) TFEP (Gate 4)
```

## 3. What It Produces

- **Five gate decisions per turn**, in order: override applied (yes/no), tier (which), dispatch (inline/skill), MCP outcome (proceed/degrade/block), verification verdict (pass/fail/skip), and if applicable, TFEP outcome (triage/escalate/full-stop).
- **One observable artifact:** the classification header (D08) — which records `OVERRIDE: true|false` capturing only Gate 5's effect on tier choice. Gates 2-4 produce *no* visible sentinel; their effects must be inferred from the command's downstream behavior (e.g., "did a sub-agent spawn?" indicates Gate 2 picked STRICT).
- **One on-disk side effect on TFEP path:** when Gate 4 fires, the TFEP execution flow at `src/superclaude/skills/sc-task-protocol/SKILL.md:170-218` (`src/`) writes a `context.yaml` (per `feature-tfep.md`), invokes `/sc:forensic`, consumes a `return-contract.yaml`, and inserts a remediation tasklist block. A `tfep-incident-report.md` is committed alongside.

## 4. What Invokes It

- **Gate 5 (overrides):** invoked at the very start of `/sc:task` parsing — before classification (`src/superclaude/commands/task.md:69`, `src/`).
- **Gate 1 (dispatch):** invoked immediately after classification header emission (`src/superclaude/commands/task.md:93-101`, `src/`).
- **Gate 3 (MCP circuit breaker):** invoked at the start of `sc:task-protocol` skill execution (`src/superclaude/skills/sc-task-protocol/SKILL.md:253`, `src/`).
- **Gate 2 (verification routing):** invoked at the Verification Phase boundary inside the skill (`src/superclaude/skills/sc-task-protocol/SKILL.md:110`, `src/`).
- **Gate 4 (TFEP):** invoked reactively when a test failure occurs in the Verification Phase (`src/superclaude/skills/sc-task-protocol/SKILL.md:125-127`, `src/`).
- **Common invariant:** every gate is invoked by *prose discipline* inside the command/skill body; none are invoked by procedural code in this repo. The `/sc:task` command is a markdown file describing what the LLM should do, not an executable.

## 5. What It Depends On

- **The tier label produced by classification (D09)** — the single shared input to Gates 1, 2, 3, 4. If classification is wrong, every downstream gate misroutes.
- **Override-flag parsing** — must run *before* classification so Gate 5 can preempt. Order is documented at `src/superclaude/commands/task.md:69` (`src/`).
- **An LLM that honors prose discipline** — none of the gates have automated enforcement in this repo. "Block STRICT" (Gate 3), "VIOLATION: must not fix" (Gate 4), the dispatch switch (Gate 1) all rely on the LLM following the markdown instructions.
- **The `/sc:forensic` command (for Gate 4 only)** — referenced at `src/superclaude/skills/sc-task-protocol/SKILL.md:170-218` (`src/`); its existence and the return-contract shape are external dependencies.
- **A writable tasklist (for Gate 4's remediation insert)** — depends on tasklist mutation being permissible, which the donor side allows.
- **Critical/Trivial Path Override globs** — Gate 2 references path-pattern overrides that themselves require knowing the affected files; if the file set is uncertain at gate time, the override may misfire.

## 6. Standalone Value Claim

**Claim:** Compliance gating is the load-bearing safety architecture of `/sc:task`. The collective value of the five gates is that they convert a single LLM classification into a *coordinated set of policy decisions* spanning dispatch, MCP requirements, verification depth, and failure-mode response — each scaled to risk.

Concretely:

- For a security-critical change (STRICT), all five gates align to maximum safety: invokes the skill (Gate 1), requires Sequential + Serena MCP with hard block on outage (Gate 3), spawns a quality-engineer sub-agent for verification with 3-5K-token budget and 60s timeout (Gate 2), enforces TFEP VIOLATION rules on test failure (Gate 4), and accepts `--force-strict` override but rejects `--skip-compliance` for security domain (Gate 5).
- For a doc-only change (EXEMPT/LIGHT), all five gates align to minimum overhead: terminates inline (Gate 1), no MCP requirement (Gate 3), skips verification (Gate 2), TFEP does not apply (Gate 4), the user can still override up to STRICT if they want (Gate 5).
- The escalation philosophy at `src/superclaude/commands/task.md:27` (`src/`) ("Better false positives than false negatives") makes the gating bias toward safety: when uncertain, classification + Gate 1 escalate, and `--force-strict` is always a valid override.

For an organization running a mixed task stream (some security, some trivial), the value is *proportional cost*: the system spends 0 tokens on doc updates and 5K tokens on auth migrations — the gating is what makes that proportionality real.

**Non-value condition (R-RULE-04, concrete, not boilerplate):**

The value claim does NOT hold under these specific conditions:

- **All five gates depend on the same upstream classification.** A misclassification at D09 propagates through every gate without correction. If the LLM classifies a 12-file refactor as LIGHT (because the prompt says "minor cleanup"), all five gates align to *zero* safety: dispatch terminates inline, no MCP check, no verification, no TFEP, no override prompt. The system fails closed on safety only if classification is right; otherwise, it fails open at every gate simultaneously. There is no per-gate independent re-check.
- **No gate has automated enforcement; all rely on LLM discipline.** "Block STRICT" (Gate 3) is prose, not code. The VIOLATION-level prohibitions in Gate 4 are prose. The dispatch switch in Gate 1 is prose. If the LLM decides — under context pressure, or after an `--skip-compliance` it has misinterpreted as `--skip-classification` — to bypass a gate, nothing in this repo intercepts. The value of the gating model is bounded by the LLM's compliance, not by mechanical safeguards.
- **The override flag set creates legitimate bypasses for *all* safety guarantees.** `--skip-compliance` (Gate 5) bypasses Gates 2-4 entirely. `--no-escalation` (`src/superclaude/commands/task.md:48`, `src/`) explicitly "voids TFEP protection." A user habituated to typing escape-hatch flags during quick iteration cycles will silently downgrade their own safety. Compare to a security model that requires re-authentication for risky overrides — here, the flag is just appended to the command. The value relies on user discipline to leave the flags alone.
- **The two-track dispatch (Gate 1) creates a knowledge bifurcation.** EXEMPT/LIGHT execute inline in the command; STANDARD/STRICT execute inside the skill. A reviewer reading only the command file sees only half of the gating; a reviewer reading only the skill sees only the other half. There is no consolidated "Compliance Gating Reference" that documents all five gates and their interaction order — it must be reconstructed from two files.

## 7. Coupling Cost Claim

**Claim:** Attaching compliance gating to `/task` requires the recipient to take on **all six** of the following concrete burdens. The set is uniquely large because compliance gating is itself the aggregation of five sub-features:

1. **A tier source — same prerequisite as everything else.** Gates 2, 3, 4 all branch on tier; Gate 1 *produces* dispatch *from* tier. `/task`'s frontmatter schema at `src/superclaude/skills/task/SKILL.md:69` (`src/`) has no `Tier:` slot. The recipient must extend the schema (or the upstream task-builder pipeline) before any gate can run. This is the same prerequisite called out by `feature-tier-classification.md` coupling cost #2 and `feature-mcp-declarations.md` coupling cost #2 — it is load-bearing for the entire gating model.

2. **A two-tier execution model inside the F1 loop.** Gate 1 routes EXEMPT/LIGHT to inline execution and STANDARD/STRICT to a deeper skill. `/task`'s F1 loop is single-track — every item runs through the same `READ → IDENTIFY → EXECUTE → UPDATE → REPEAT` sequence (`src/superclaude/skills/task/SKILL.md:83-98`, `src/`). Adding a per-tier dispatch inside the loop forces either (a) two different EXECUTE handlers selected by per-item tier (changes the loop's uniformity), (b) a pre-loop branch that selects one of two `/task` modes (changes the skill's entry shape), or (c) a sibling skill invocation for STRICT items only (introduces cross-skill coordination the recipient currently does not have). Each option meaningfully extends the loop's surface.

3. **A verification-routing layer compatible with `/task`'s existing Phase-Gate QA.** Gate 2 maps tier → (verification method, token cost, timeout). `/task` already has Phase-Gate QA at `src/superclaude/skills/task/SKILL.md:182-211` (`src/`), which spawns `rf-qa` adversarially with a 3-cycle fix loop — operationally complete but single-method. Adopting Gate 2 requires either (a) replacing `rf-qa` with `quality-engineer` for STRICT and direct Bash test execution for STANDARD (loses `rf-qa`'s adversarial-stance, fix-cycle, and "ensuring..." clause discipline), (b) layering Gate 2 *on top* of Phase-Gate QA (two verification systems coexist on STRICT, doubling token cost), or (c) making Gate 2 a precursor to Phase-Gate QA (introduces ordering). The recipient must choose without precedent.

4. **An MCP circuit breaker with enforcement.** See `feature-mcp-declarations.md` coupling cost #3-4 — the recipient must implement a probe and a block path. This is sub-cost #4 here, not a standalone burden.

5. **TFEP integration with `/task`'s Error Handling.** Gate 4 enforces three VIOLATION rules on test failure. `/task`'s Error Handling at `src/superclaude/skills/task/SKILL.md:170-179` (`src/`) currently treats failures by logging blockers and continuing (`- [x]` with a note). The donor's TFEP halts, freezes, writes `context.yaml`, invokes `/sc:forensic`, consumes `return-contract.yaml`, inserts a remediation block (per `feature-tfep.md`). Integrating TFEP requires (a) deciding when `/task` should switch from "log and continue" to "halt and forensically triage" (probably per-item-tier), (b) verifying `/sc:forensic` exists in the repo (it does not; see TFEP characterization), (c) extending DYNAMIC CONTENT MARKER mutation to accept TFEP's remediation block format. Each is non-trivial.

6. **An override flag set on a skill that has no flags.** Gate 5's `--compliance`, `--skip-compliance`, `--force-strict`, `--no-escalation` are CLI-flag-shaped. `/task` is invoked via the Skill tool with a single argument (the task file path); it has no flag-parsing layer. The recipient must either (a) re-encode flags as task-file frontmatter (`--force-strict` becomes a `force_tier: strict` field — extends schema), (b) re-encode them as per-item annotations (every item carries a tier-override hint — extends item shape), or (c) introduce a "task-config" sidecar file (new artifact). The donor's CLI-flag affordance does not survive intact.

**Net coupling cost:** the recipient must extend the schema with a tier slot (1), bifurcate the F1 loop into a tier-routing branch (2), reconcile or replace Phase-Gate QA (3), implement MCP circuit-breaker enforcement (4), integrate TFEP with Error Handling (5), and re-encode CLI flags into a flagless skill model (6) — six distinct extensions across six separate `/task` surfaces. This is the largest coupling cost of any single feature in the donor catalog because compliance gating is structurally the aggregation of five gates.

---

## Cross-Reference

- D04, D07, D10, D16, D27 in `donor-feature-catalog.md` — sub-feature anchors.
- D09 in `donor-feature-catalog.md` (tier classification model) — shared upstream producer of the tier label; see `feature-tier-classification.md`.
- D19, D20, D21, D22, D23, D24, D25 in `donor-feature-catalog.md` (TFEP family) — sub-feature of Gate 4; see `feature-tfep.md`.
- `feature-per-tier-branching.md` — characterizes Gates 1 and 2 from the branch-mapping perspective; this file is the gating-mechanism perspective.
- `feature-mcp-declarations.md` — characterizes Gate 3 in isolation.
- Recipient row 1 (Task File Validation gate, `src/superclaude/skills/task/SKILL.md:64-73`, `src/`) — structural attach point for tier slot and pre-loop gate checks.
- Recipient row 10 (Phase-Gate QA Verification, `src/superclaude/skills/task/SKILL.md:182-211`, `src/`) — structural attach point for Gate 2 (verification routing).
- Recipient row 8 (Error Handling / blocker logging, `src/superclaude/skills/task/SKILL.md:170-179`, `src/`) — structural attach point for Gate 4 (TFEP integration).
