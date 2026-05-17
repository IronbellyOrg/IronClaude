# TDD §8 — Inter-Agent Contract APIs (synth-05)

**Status:** In Progress
**Date:** 2026-05-14
**Component:** task-builder convergence release (FR-CONV.1 .. FR-CONV.6)
**Adaptation note:** This component exposes **no HTTP API**. §8 is adapted to
document the **inter-agent contract APIs** — the spawn-prompt and report
artifacts exchanged between `task-builder` (skill orchestrator) and the
`rf-*` subagent family. Schemas are cited from PRD §25.N. SC-1..SC-8 from
`/qa/research-gate-consolidated.md` are applied; SC-3 (Five Adversarial Axes
canonicalization) is discharged in §8.5.

---

## §8.1 Inter-Agent Contract Overview

The task-builder convergence release introduces or modifies **five distinct
contract artifacts** carried between the skill orchestrator (`task-builder`
skill, executing inside the main Claude Code session) and its rf-* subagents.
Each contract is an in-memory spawn-prompt fragment OR an on-disk markdown
artifact under `.dev/tasks/to-do/TASK-*/`. None are HTTP endpoints; none
involve network transport. The table below replaces the conventional HTTP
endpoint table:

| Producer | Consumer | Contract Artifact | FR Introducing It |
|----------|----------|-------------------|-------------------|
| task-builder skill (orchestrator) | rf-task-builder | `BUILD_REQUEST` Skill-tool prompt | (existing, unchanged transport; payload extended) |
| rf-task-builder | rf-qa (task-integrity phase) | MDTM task file `.dev/tasks/to-do/TASK-*/TASK-*.md` containing a new `## Execution Context` block after frontmatter | **FR-CONV.2** (Execution-Context header addition) |
| rf-qa (task-integrity) | rf-qa-qualitative (task-qualitative) | `## Inherited Structural Verdict` block injected verbatim into the rf-qa-qualitative spawn prompt at SKILL.md §A.10.5 | **FR-CONV.3** |
| Any partition agent (rf-qa, rf-analyst, or rf-qa-qualitative partition instance) | task-builder skill orchestrator (gate-result merger at SKILL.md §A.8 / §A.10) | `synthetic-dnsp` HIGH-severity finding (5 fixed fields + 2 dedup-control fields) emitted in the agent's output stream | **FR-CONV.6** |
| rf-task-builder fix-loop | itself (next-cycle decision) | Halt-message strings: `[HALT-MONOTONICITY] \|F\|=<n>` OR verbatim regression message | **FR-CONV.5** |
| All-partition-agents-fail | rf-team-lead (existing) | Escalation per `rf-team-lead.md:417` (3 fix cycles per phase, HALT-and-ask-user) | (existing — explicitly **preserved** by FR-CONV.6 Negative Criterion) |

**Direction of flow:** All contracts are unidirectional. There is no
request/response handshake — the producer emits, the consumer reads.
Reinjection on retry (INV-002) is achieved by the orchestrator re-reading the
producer's on-disk artifact on every cycle, **not** by a callback.

**Persistent vs. ephemeral:**

- **On-disk (persistent under `.dev/tasks/to-do/TASK-*/`):** the MDTM task
  file itself, all `qa/qa-*.md` reports, all `research/*.md` files. These
  satisfy OPEN-INV-018 (persistent-artifact invariant) and are auditable
  post-hoc.
- **In-memory (ephemeral to one orchestrator turn):** the spawn-prompt
  payloads (`## Inherited Structural Verdict` block, `BUILD_REQUEST` body).
  These are reconstructed every cycle from the on-disk producer artifacts,
  which enforces INV-002 freshness without any cache layer.

---

## §8.2 Contract Details

### Contract 1: BUILD_REQUEST → MDTM Task File (FR-CONV.2 modifies output)

**Producer:** task-builder skill (orchestrator)
**Consumer:** rf-task-builder subagent
**Transport:** Skill-tool prompt (unchanged); generated artifact is the
on-disk MDTM task file.
**Schema:** existing `BUILD_REQUEST` per `SKILL.md:1409-1485`, plus an
optional new signal `EXECUTION_CONTEXT_REQUIREMENTS` that FR-CONV.2 *may*
add to the BUILD_REQUEST surface. The generated MDTM file MUST contain a
`## Execution Context` block placed **at the top of the file, immediately
after the YAML frontmatter and before Phase 1**. The block schema is PRD
**§25.1** — three labeled lines:

```yaml
"## Execution Context":
  References:        # BUILD_REQUEST refs (GOAL, WHY, related-doc IDs)
    - "R-###: <ref-line>"
  Source areas:      # named modules/packages — NEVER specific file paths
    - "<package-or-module-name>"
  Key constraints:   # top 1-3 invariants from BUILD_REQUEST
    - "<invariant statement>"
```

**Emission rules:**

- When BUILD_REQUEST is fully populated (GOAL + WHY + source-area hints
  present), the generated `## Execution Context` block contains exactly
  **three labeled lines** (`References`, `Source areas`, `Key constraints`).
- When BUILD_REQUEST is minimal (no WHY, no source-area hints), the block
  **degrades to References-only** — `Source areas` and `Key constraints`
  are omitted, not left blank (PR-01 failure-mode #2; PRD §25.1 degradation
  rule). This is the maximal-vs-degraded distinction noted as drift D-2 in
  research file 15: §25.1's YAML shows the maximal form; FR-CONV.2 governs
  the degradation.
- **Hidden-input determinism guard:** the block MUST NOT contain specific
  file paths or `file:line` citations. Verification:
  `grep -E "src/|/.*:[0-9]+"` run against the header block's line range
  returns **zero hits**. `Source areas` carries module/package names only.

**Error behavior:** If the orchestrator cannot derive even `References`
(BUILD_REQUEST has no GOAL), the task file generation is itself a MALFORMED
return — rf-task-builder's MALFORMED retry counter (max 2) governs, not a
new path.

### Contract 2: rf-qa task-integrity → rf-qa-qualitative task-qualitative (FR-CONV.3)

**Producer:** rf-qa, running the **task-integrity** QA phase
(`rf-qa.md:259-289`).
**Consumer:** rf-qa-qualitative, running the **task-qualitative** QA phase
(`rf-qa-qualitative.md:508-603`).
**Transport:** orchestrator-mediated spawn-prompt injection at task-builder
`SKILL.md §A.10.5` (verified range `SKILL.md:923-1000`).
**Schema:** PRD **§25.5 Phase Contract** (verbatim from research file 15):

```yaml
phase_contract:
  producer: rf-qa
  consumer: rf-qa-qualitative
  artifact: "## Inherited Structural Verdict block in spawn prompt"
  schema_version: "1.0.0"
  delivery_semantics: "at-most-once-per-cycle"
  freshness_rule: "On fix-cycle re-run, orchestrator re-injects NEW verdict; stale verdicts forbidden (INV-002)"
  enumeration_rule: "Checklist enumeration is dynamic — auto-picks up TB-Add catalogue from FR-CONV.1 (INV-010)"
  consumer_obligation: "Self-Audit listing relied-on PASS items AND ≥1 semantic check (INV-019)"
  anti_inflation: "Mechanical re-checking SKIPPED for PASS items; semantic verification STILL REQUIRED (rf-qa-qualitative.md:766-775)"
  failure_mode: "If rf-qa fails to emit a verdict, rf-qa-qualitative MUST NOT spawn — gate halts at A.10 before A.10.5"
```

The injected block itself follows PRD **§25.2**: `rf_qa_table_verbatim`
(byte-exact copy of rf-qa's `## Items Reviewed` table + `## Overall Verdict`
line + `## Summary` counts), a fixed `prompt_directive`, and a fixed
`reinjection_rule`.

**Emission rules:**

- rf-qa emits its verdict table verbatim in its report at
  `.dev/tasks/to-do/TASK-*/qa/qa-task-integrity*.md`.
- The orchestrator (SKILL.md §A.10.5) reads that report, extracts the
  `## Items Reviewed` table contiguously, and splices it **verbatim** into
  the rf-qa-qualitative spawn prompt under the heading
  `## Inherited Structural Verdict`. No paraphrase, no reformatting, no
  field-renaming. Insertion point is inside the §A.10.5 spawn-prompt fenced
  block, after the `TARGET FILES` enumeration and before `INSTRUCTIONS:`.
- The block includes the fixed `prompt_directive` (PRD §25.2, verbatim):
  *"PASS items machine-verified — skip structural re-checking; FAIL items
  machine-verified defects — flag HIGH. Focus on semantic quality."*
- **INV-002 cycle-N+1 reinjection:** on every fix-cycle re-run the
  orchestrator re-reads the *current* rf-qa task-integrity report and
  re-injects the **NEW** cycle-N verdict. A stale cycle-(N-1) verdict is
  forbidden from governing current-cycle decisions. The orchestrator MUST
  NOT memoize a prior cycle's read.
- **INV-010 dynamic checklist enumeration:** the rf-qa task-integrity
  checklist is not fixed-length — it enumerates over the TB-Add catalogue
  (TB-Add-1 .. TB-Add-N). When FR-CONV.1 grows the catalogue, the verdict
  table FR-CONV.3 injects grows automatically; the extraction logic is
  row-agnostic (verbatim copy). **This is why FR-CONV.1 must land 1st and
  FR-CONV.3 must land 3rd** — landing in reverse order would ship a
  half-empty verdict table.
- **INV-019 Self-Audit mandate:** rf-qa-qualitative's output MUST contain a
  `## Self-Audit` section that (a) lists every rf-qa PASS item it relied on
  (structural re-check skipped) AND (b) lists **≥1 semantic check** where
  rf-qa PASS is insufficient and the agent verified independently. A run
  with 0 entries in category (b) is a violation, not a clean run. The
  Self-Audit is operationalized by the existing mandatory Self-Audit block
  repeated in every rf-qa-qualitative phase
  (`rf-qa-qualitative.md:183-187` pattern).

**Anti-inflation invariant (FR-CONV.3 Negative Criterion):** the Prohibited
Behaviors block at `rf-qa-qualitative.md:766-775` — in particular line 770,
*"NEVER mark an item VERIFIED if you only read about it in another report —
that is RELIANCE, not VERIFICATION"* — MUST NOT be weakened, removed, or
rephrased. FR-CONV.3 layers a *deliberately-permitted RELIANCE channel* on
top of this rule: the inherited verdict permits skipping **structural**
re-checks (rf-qa's machine-verified domain) but does **not** permit marking
**semantic** items VERIFIED without an independent tool call. The K-003
audit (first 5 real runs after FR-CONV.3 lands) verifies operational
compliance.

**Failure mode:** If rf-qa fails to emit a task-integrity verdict at all,
rf-qa-qualitative MUST NOT spawn — the gate halts at §A.10 before §A.10.5
(PRD §25.5 `failure_mode`).

### Contract 3: Partition Agent → Orchestrator (FR-CONV.6 synthetic-dnsp emission)

**Producer:** any partition instance — rf-qa partition, rf-analyst
partition, or rf-qa-qualitative partition (all three carry the identical
emission contract in their partition-protocol sections).
**Consumer:** task-builder skill orchestrator, in the gate-result merge
step at `SKILL.md §A.8` (Research Quality Gate) and `§A.10` (Task File
Validation).
**Transport:** the synthetic finding is emitted as a structured block in
the partition agent's **normal output stream** — no separate channel. The
orchestrator's existing merge logic consumes it identically to a real
finding.
**Schema:** PRD **§25.3** (verbatim from research file 15):

```yaml
synthetic_dnsp_finding:
  severity: HIGH                                # fixed
  source: "synthetic-dnsp"                      # fixed
  affected_range: "<agent's assigned_files slice>"
  evidence: "<spawn-log path, OR stub citing log absence>"
  recommendation: "Manual review required — partition agent failed twice"
  dedup_key: "(assigned_files_range, escalation_ladder_exhaust_point)"
  found_n_times: <int, default 1>               # increments on dedup collapse
```

**Emission rules:**

- A partition agent emits **one** HIGH-severity synthetic finding with all
  7 fields (5 fixed + `dedup_key` + `found_n_times`) when its escalation
  ladder (initial → retry-1 → retry-2, the default twice-retry exhaust)
  exhausts and gap-fill has not recovered the partition's report.
- **Cardinality is per-partition-instance.** If 4 partition agents spawn
  and 1 exhausts, exactly 1 synthetic finding emits. If 2 exhaust with
  distinct `assigned_files`, 2 synthetic findings emit (different
  `dedup_key`s).
- **Dedup collapse (within-cycle):** two synthetic findings with identical
  `dedup_key = (assigned_files_range, escalation_ladder_exhaust_point)`
  collapse to one finding in the orchestrator's merge step, with
  `found_n_times` incremented (`1 → 2`).
- **INV-021 within-agent-instance emission:** the cohort does **not**
  serialize on one partition's exhaust. The DNSP synthetic is generated
  locally inside the exhausted agent's reply; N-1 partitions continue to
  run concurrently to completion while the exhausted partition synthesises
  its finding. This preserves the parallel-research invariant
  (NFR-CONV.10). Spawn-log inspection verifies: N partition agents run
  concurrently; on one agent's exhaust, N-1 continue before DNSP
  synthesises.
- **HIGH severity is non-overridable** — it guarantees gate-level
  visibility so a synthetic finding cannot mask, or be masked by, real
  findings. Synthetic findings emit *alongside* (not in place of) the real
  findings from partitions that did succeed.

**All-agents-fail precedence (FR-CONV.6 Negative Criterion):** if **zero**
partition agents succeeded AND the whole cohort exhausted, the orchestrator
MUST **NOT** emit any synthetic finding. Instead it activates the existing
escalation at `rf-team-lead.md:417` (3 fix cycles per phase, then
HALT-and-ask-user). Rationale: with zero successful partitions there is no
merged report to attach findings to; synthetic emission would mask the
all-agents-fail condition by producing N HIGH findings that look like
ordinary fixable issues. This satisfies SC-2: the "partial-exhaust" path
(emit synthetic) and the "all-fail" path (escalate, no synthetic) are
**mutually exclusive**.

| Condition | Action |
|---|---|
| ≥1 partition succeeded AND ≥1 partition's ladder exhausted | Emit synthetic-dnsp per exhausted partition (one each) |
| Zero partitions succeeded (all exhausted) | DO NOT emit synthetic; escalate per `rf-team-lead.md:417` |
| All partitions succeeded | No synthetic emission — normal gate flow |

### Contract 4: Fix-Loop Halt Signals (FR-CONV.5)

**Producer:** rf-task-builder fix-loop (and the rf-qa fix-cycle protocol
that feeds it verdict counts).
**Consumer:** itself — the next-cycle decision logic.
**Transport:** halt-message strings emitted into the fix-loop's verdict
stream; on emission, the fix-cycle loop exits and control returns to the
caller as a halt verdict (no further cycle attempted, no further QA gate
invoked under that fix-cycle counter).
**Schema:** two verbatim halt-message string formats.

**Halt messages (verbatim — fixtures depend on character-for-character match):**

- **Monotonicity halt** — emitted when the FAIL-set fails to shrink, i.e.
  `|F_{n+1}| >= |F_n|`:

  ```
  [HALT-MONOTONICITY] |F|=<n>
  ```

  where `<n>` is the cardinality of `F_{n+1}` (the stagnant or growing
  count).

- **Regression halt** — emitted when any item held verdict PASS at cycle N
  and flips to FAIL at cycle N+1:

  ```
  Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.
  ```

  Substitutions: `X.Y` → the item identifier in the task file's checklist
  numbering; `N` → the cycle index at which that item last held PASS.

**Ordering / precedence (per cycle transition n → n+1):**

1. **First** — regression check: compute `R = { item | verdict(item,n)=PASS ∧ verdict(item,n+1)=FAIL }`. If `R ≠ ∅`, emit the regression halt and exit. **Regression detection has STRICT PRECEDENCE over the monotonicity guard** — it runs first, and halts even if `|F_{n+1}| < |F_n|`.
2. **Second** — monotonicity check: if `|F_{n+1}| >= |F_n|`, emit `[HALT-MONOTONICITY] |F|=|F_{n+1}|` and exit.
3. **Third** — existing 3-cycle hard cap (`rf-team-lead.md:417`, `rf-task-builder.md` per-gate table) if neither new halt fired.
4. **Fourth** — otherwise proceed to fix cycle n+2.

**F-set definition:** `F_n` is the set of FAIL-verdict items at the end of
fix cycle n, where **item identity is its dedup-key**, not its checklist
position or surface text. `|F_n|` is the cardinality after dedup-key
deduplication. This dedup-key identity is what makes INV-012 composition
with FR-CONV.6 work.

**Negative criteria:** there is **no "shrinks too slowly" threshold** —
`|F| = 10, 9, 8` is valid and must not be halted (X-003 was REJECTED in the
PRD). The 4+ separate retry counters (RESEARCH_NEEDED max 2, MALFORMED
max 2, and the per-gate fix-cycle counters) MUST NOT be collapsed into a
shared monotonicity state — monotonicity is tracked **per fix-cycle
counter**, not globally. The monotonicity check is only consulted when
`|F_n| > 0`; gate-PASS termination (`|F_n| = 0`) precedes it so
`[HALT-MONOTONICITY] |F|=0` is never falsely emitted.

**INV-012 composition with synthetic-dnsp (Contract 3):** synthetic-dnsp
findings **count as failures** for `|F_n|` cardinality — they are
first-class members of `F`. **BUT** a synthetic finding with an identical
`dedup_key` across consecutive cycles is a **dedup case, NOT a regression**
— its prior-cycle verdict was already FAIL (synthetic emission = FAIL), not
PASS, so the PASS→FAIL regression trigger does not fire. It does still
contribute `1` (not `2`) to `|F_{n+1}|`, and if it persists with nothing
else changing it WILL trip the monotonicity guard on the next cycle — which
is the intended behavior (a partition exhaust the team cannot dislodge is
exactly the runaway condition the halt protects against). This dedup
mechanism is what lets FR-CONV.6 (per-partition exhaust) and FR-CONV.5
(monotonicity) compose cleanly.

---

## §8.3 Error Response Format

This component has no HTTP error responses. The analogous concept is the
**synthetic-dnsp finding** — the structured block a partition agent emits
into the gate-result stream when its own escalation ladder exhausts, so
that the partition's failure is surfaced as a first-class HIGH finding
rather than silently aborting the gate. The schema below is canonical for
all three partition-capable agents (rf-qa, rf-analyst, rf-qa-qualitative):

```yaml
synthetic_dnsp_finding:   # FR-CONV.6 output on partition exhaust
  severity: HIGH
  source: synthetic-dnsp
  affected_range: "<agent assigned_files slice>"
  evidence: "<spawn-log path OR stub citing log absence>"
  recommendation: "Manual review required — partition agent failed twice"
  dedup_key: ["<assigned_files_range>", "<escalation_ladder_exhaust_point>"]
  found_n_times: 1   # increments on dedup collapse within a cycle
```

**Field semantics (also see PRD §25.3):**

- `severity: HIGH` is fixed and non-overridable — guarantees gate-level
  visibility so the synthetic finding cannot be masked.
- `source: "synthetic-dnsp"` is a fixed literal sentinel string —
  grep-able for operator inspection and for the acceptance assertion
  `grep -n "synthetic-dnsp" src/superclaude/agents/{rf-qa,rf-analyst,rf-qa-qualitative}.md`
  (returns ≥1 hit per file once FR-CONV.6 lands; current grep returns
  zero hits — greenfield, as expected for a BASE FR).
- `affected_range` is the partition's `assigned_files` slice copied
  verbatim from the spawn prompt — free-form range descriptor.
- `evidence` is either a spawn-log path (canonical recommended location
  `${TASK_DIR}qa/spawn-log-<agent_role>-<partition_id>.txt`) **or** an
  explicit stub of the form `"no-spawn-log: <reason>"` citing log absence
  — never blank.
- `recommendation` is the fixed literal `"Manual review required —
  partition agent failed twice"`.
- `dedup_key` is the 2-tuple `(assigned_files_range,
  escalation_ladder_exhaust_point)`. Canonical wire format MUST be a
  YAML list `["<range>", "<exhaust_point>"]` to avoid the
  string-vs-tuple ambiguity flagged in research file 15 §8.3.
  `escalation_ladder_exhaust_point` is a closed-vocabulary token from
  `{"retry-1", "retry-2", "gap-fill-round-1", "gap-fill-round-2",
  "gap-fill-round-3"}` — free-form descriptions are forbidden so
  dedup-key equality is deterministic.
- `found_n_times` defaults to 1; increments on dedup collapse within the
  same cycle.

**Non-error paths:**

- A partition agent that completes successfully emits its normal report;
  no synthetic block.
- A partition agent that returns FAIL with real findings emits those
  findings normally; no synthetic block.
- A partition agent whose ladder exhausts emits exactly **one**
  synthetic-dnsp block, replacing the missing real report.
- All-cohort exhaust routes to `rf-team-lead.md:417` escalation — no
  synthetic emitted at all (see §8.2 Contract 3 precedence table).

---

## §8.4 API Governance & Versioning

**Versioning strategy.** The inter-agent contracts are versioned via a
`schema_version` field on the Phase Contract (PRD §25.5,
`schema_version: "1.0.0"`, semver). The Phase Contract is the *meta-schema*
that governs the producer/consumer relationship between rf-qa and
rf-qa-qualitative; the other artifacts (Execution Context header, Synthetic
DNSP Finding, Inherited Structural Verdict block) are versioned implicitly
under the same `1.0.0` umbrella for this release. A future change requiring
a wire-incompatible adjustment to any artifact bumps `schema_version`.

**Compatibility contract.** Governance is bound by **A-002 (strictly
additive landings)** — for the v3.9 convergence release, every FR-CONV
landing may only *add* fields/sections; it may not remove or rename
existing ones.

| Change Type | Example | Allowed Without Version Bump? |
|-------------|---------|-------------------------------|
| Add optional field to Phase Contract | New `audit_trail` field | **Yes** — additive, permitted by A-002 |
| Add optional field to Synthetic DNSP Finding | New `tags` array | **Yes** — additive |
| Add optional line to Execution Context header | New `Risk notes` label | **Yes** — additive (degradation rules unchanged) |
| Remove an existing field | Drop `recommendation` from Synthetic DNSP Finding | **No** — breaking; A-002 forbids |
| Rename a field | `dedup_key` → `fingerprint` | **No** — breaking; consumers + fixtures pinned to the name |
| Change Inherited Verdict `prompt_directive` text | Modify the directive wording | **No** — affects the anti-inflation guarantee; the directive is a fixed-value field (PRD §25.2) |
| Change a halt message format | Alter `[HALT-MONOTONICITY]` text or the regression message | **No** — FR-CONV.5 fixtures depend on verbatim character-for-character match |
| Change `escalation_ladder_exhaust_point` vocabulary | Add a new token | Additive **Yes**; removing/renaming a token **No** (breaks dedup-key equality) |

**Deprecation policy.** N/A for v3.9 — A-002 mandates strictly-additive
landings, so no field is deprecated in this release. Any future field
deprecation requires a net-new `schema_version` plus a documented
bridge-period during which both old and new fields are accepted by the
consumer. The `prompt_directive`, the two halt-message strings, and the
fixed-value fields of §25.2/§25.3 are explicitly **frozen surfaces** —
treat them as part of the wire ABI.

**Drift caveat (carries SC-1).** PRD §25.4 (Per-Item Checklist Schema)
declares the 5-field schema `{Description, Context, Acceptance, Confidence,
Verification}` is "preserved unchanged" at `SKILL.md:1452-1457`, but the
current SKILL.md at that range holds a different phase-template
`{Context, Action, Output, Verification, Completion gate}` and `grep` for
`Acceptance`/`TB-Add-8` returns zero hits. §25.4 is **not** an inter-agent
*contract* surface (it is the per-item structure inside the MDTM file), so
it is out of §8's primary scope — but because FR-CONV.1/TB-Add-8 may have
to *land* this schema (which would itself be a non-additive change,
conflicting with A-002), it is recorded here as a governance risk and is
elevated to a TDD §22 Open Question per SC-1. Resolution requires
Engineering Lead input.

---

## §8.5 SC-3: Five Adversarial Axes — Canonical Definitions

Per SC-3 in `/qa/research-gate-consolidated.md`, the Five Adversarial Axes
introduced by **FR-CONV.4** are referenced by the rf-qa-qualitative
task-qualitative phase but are **not defined anywhere in
`rf-qa-qualitative.md`**. Canonicalizing them is the TDD's responsibility.
FR-CONV.4 adds a "Five Adversarial Axes" header *before* the immutable
15-item task-qualitative checklist (`rf-qa-qualitative.md:527-562`) and adds
an `Axis` column to the `## Items Reviewed` table
(`rf-qa-qualitative.md:689-693`), transforming it from
`# | Check | Result | Evidence` to `# | Check | Axis | Result | Evidence`.

**The five axes (canonical definitions):**

| Axis | Name | Definition | What a finding on this axis looks like |
|------|------|------------|----------------------------------------|
| AX-1 | **Drift** | A cited fact (file path, line number, signature, count, config value) no longer matches the current source. | "Item 4.2 cites `foo()` at `src/x.py:88`; actual location is `:91` — stale citation." |
| AX-2 | **Contradictions** | Two artifacts (or two sections of one artifact) assert mutually incompatible facts about the same subject. | "Phase 3 says the function returns a dict; Phase 5's verification greps for a list return." |
| AX-3 | **Omissions** | A required touchpoint, consumer, dependency, or step is absent from the plan. | "Item adds a new kwarg but no item updates the function signature to accept it." |
| AX-4 | **Weakened criteria** | An acceptance/verification condition has been softened to something unobservable or trivially satisfiable. | "Verification reads `# Test` into a file and asserts on the 6-char placeholder — does not exercise the feature." |
| AX-5 | **Invented content** | The artifact introduces a requirement, feature, or capability not present in its upstream source. | "TDD adds a caching layer the PRD never specified." |

**Annotation rules (canonical):**

- Every row in the `## Items Reviewed` table for the task-qualitative phase
  MUST carry exactly one `Axis` value from `{AX-1, AX-2, AX-3, AX-4, AX-5}`
  OR the literal `none`.
- `Axis: none` is used when the check passed and the axis lens surfaced
  nothing — it is **not** an N/A escape (the Ban-N/A rule at
  `rf-qa-qualitative.md:93` still applies; `none` means "examined, clean").
- `Axis: drift-axis-inactive` is the single permitted exception: used only
  when the artifact under review has **no citations at all** to drift
  against (rare for task files; possible for skeletal stubs). It records
  that AX-1 was consciously evaluated and found inapplicable, satisfying
  Ban-N/A without forcing a false `none`.
- The five axes **multiply lenses, not checks** — the task-qualitative
  TOTAL stays at **15** items. Each axis labels groups of checks; it does
  not add checks. The Tool Engagement Minimum
  (`rf-qa-qualitative.md:774-775`) floor remains `tool calls ≥ 15`, NOT
  `≥ 15 × 5`.
- The `Axis` column is **task-qualitative-only**. The shared Output Format
  block (`rf-qa-qualitative.md:675-714`) is used by all 8 phases; for the
  non-task phases the `Axis` column is omitted entirely rather than filled
  with `none` — this avoids forcing a meaningless column onto phases the
  axes were not designed for, and sidesteps the Ban-N/A tension.

**Composition with FR-CONV.3 (INV-013):** the five axes apply to items
**not** covered by the inherited structural PASS. An item whose structural
correctness rf-qa already machine-verified is off the table for AX-1/AX-2
structural-drift re-checking; the axes focus rf-qa-qualitative's effort on
the semantic surface. Composition is clean — FR-CONV.4 (4th) layers on
FR-CONV.3 (3rd) without conflict.

---

## §8.6 Cross-Section Notes for TDD Assembly

- **SC-2 discharged** in §8.2 Contract 3 — partial-exhaust vs all-fail
  trigger semantics documented as mutually-exclusive paths.
- **SC-3 discharged** in §8.5 — five axes canonically defined with
  `none` / `drift-axis-inactive` annotation rules.
- **SC-4** (per-gate fix-cycle limits live in `rf-task-builder.md` I16:
  research-gate 3 / synthesis-gate 2 / report-validation 3 /
  task-integrity 2 / qualitative 3, NOT in `rf-qa.md`) is referenced by
  §8.2 Contract 4 and is primarily synth-03's (Architecture) and
  synth-06's (Testing) surface — noted here for the halt-precedence
  ordering only.
- **SC-1** is recorded as a governance risk in §8.4 and must appear as a
  TDD §22 Open Question.
- **SC-6 corrected FR landing order** applied throughout: FR-CONV.1 (1st)
  → FR-CONV.2 (2nd) → FR-CONV.3 (3rd) → FR-CONV.4 (4th) → FR-CONV.5 (5th)
  → FR-CONV.6 (6th).
- **SC-8** applied: zero-trust verdict definitions cited at
  `rf-qa.md:141-142`, not `:144-146`.
- All line citations in this section were taken from the research files
  read this turn (03, 04, 10, 12, 13, 15, research-gate-consolidated) and
  carry those files' drift caveats; TDD assembly should re-verify against
  current source at authoring time.

---

**Status:** Complete





