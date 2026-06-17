---
title: "TFEP forensic→troubleshoot Migration — E2E Validation Suite (4 tests × 3 runs)"
source_seed: .dev/brainstorms/20260617-0148-tfep-e2e-validation/seed-brief.md
domain: process
strategy: systematic
adversarial_status: pass
convergence_score: 0.88
proposal_count: 3
models: [opus(claude-opus-4-8), sonnet(gpt-5.5), haiku(qwen3.6-plus)]
generated: 2026-06-17T01:55:00Z
---

# TFEP E2E Validation Suite — Merged Requirements

A delegable, reproducible, auditable validation suite that confirms the just-completed
**TFEP forensic→troubleshoot backend migration** achieves its desired outcome. **4 e2e tests**, each
**run 3× by independent subagents** (12 runs), each emitting a machine + human evidence artifact, rolled
up by an aggregator into a one-glance GREEN/RED gate under a **strict 12/12** policy.

Signature property (merged from all 3 proposals): **a PASS is positive proof, never absence of
evidence** — every test carries a falsification tripwire, and cross-run agreement is gated at the
*observation* level (normalized digest), not just the verdict level.

> NOTE: The migration is docs/skill PROSE (no pytest; `TESTING_REQUIREMENTS=NONE`). "e2e test" = a
> read-only behavioral validation scenario: deterministic shell probes (`rg`/`grep`/`make verify-sync`/
> `git status`) + bounded, anchor-cited protocol-trace reading. Nothing here mutates the 5 migrated files.

## 0. Conventions (bind all 4 tests)

- **Worktree root `$ROOT`**: `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend`
- **The 5 migrated files** (the ONLY in-scope surface):
  - `T1` = `src/superclaude/skills/sc-task-protocol/SKILL.md` (§4.5 TFEP consumer)
  - `T2` = `src/superclaude/commands/task.md`
  - `C1` = `src/superclaude/commands/troubleshoot.md`
  - `P1` = `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (producer)
  - `R1` = `src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md` (`## TFEP Consumer`)
- **7-field wire set** (canonical order): `status`, `test_is_wrong`, `recommended_escalation`, `tasklist_insertion_path`, `remediation_target`, `root_cause_summary`, `solution_summary`
- **Enums**: `recommended_escalation ∈ {none, retry, escalate_depth, halt}`; `remediation_target ∈ {test, code, docs, none}`
- **Freeze baseline file**: `.dev/tasks/to-do/TASK-RF-tfep-troubleshoot-migration-20260616-174519/phase-outputs/plans/freeze-block-preserved.md`
- **Explicit ignore-list (OUT of scope for all tests)**: bare `forensic` as generic vocabulary in unrelated skills (`cli-eval`, `sc-crash-recovery`, `sc-brainstorm-protocol`, `sc-reflect-protocol`, etc.). The bare-`forensic` sweep is scoped to `T1`+`T2` only; the `/sc:forensic` literal sweep is repo-wide over `src/`.
- **Determinism rule**: every probe is a shell command with captured exit code + stdout; run every `rg` with `LC_ALL=C` and `--sort path`. LLM judgment is permitted ONLY to (a) confirm a `diff`-backed byte-match, or (b) author human findings prose. Each acceptance criterion is labeled `DETERMINISTIC` or `JUDGMENT`; the suite holds **≤ 2 JUDGMENT criteria total**, each anchored to a quoted token.

### Coverage map (no gap, minimal deliberate overlap)

| Test | Outcome dimension | Surface | Owns |
|------|-------------------|---------|------|
| **E1** Residual + Sync | 1 — backend swap complete + clean | T1,T2,src/,.claude/ | removal |
| **E2** Contract round-trip | 2 — producer↔consumer adapter identity | T1,P1,R1 | cross-surface field identity |
| **E3** Chain trace | 3 — end-to-end protocol chain resolves | T1,P1,C1 | control-flow wiring |
| **E4** Safety invariants | 4 — freeze/`--fix`/asymmetric/neutral preserved | T1,R1,baseline | invariant preservation |

Deliberate overlap: "no live `--fix`" is checked in BOTH E3 (chain correctness) and E4 (safety invariant) — defense-in-depth on the single highest-cost regression.

---

## TEST E1 — Residual-Integrity & Sync-Parity  (dimension 1)

**Scope IN:** residual token sweep over `T1`+`T2`; repo-wide `/sc:forensic` over `src/`; `make verify-sync` exit+output; `git status` filtered to `.claude/`. **OUT:** bare `forensic` outside `T1`/`T2`; content correctness (E2–E4).

**Probes** (each captured with exit code; `LC_ALL=C`):
1. `LC_ALL=C rg -n --sort path "/sc:forensic|\bforensic\b|--tier|--intent|rca-verdict|solution-verdict" T1 T2` → **0 lines, exit 1**
2. `LC_ALL=C rg -n --sort path "/sc:forensic" src/` → **0 lines, exit 1**
3. `make verify-sync` → **exit 0**, stdout contains `All components in sync`, NO `DIFFERS`/`MISSING`
4. `git status --porcelain | grep '\.claude/'` → **0 lines** (only `.claude/settings.json` ever exempt)
5. **Falsification (sweep-liveness):** `LC_ALL=C rg -n "troubleshoot" T1 | head -1` → **≥1 line, exit 0**
6. **Falsification (backend present):** `LC_ALL=C rg -c "/sc:troubleshoot" T1` → **≥1**

**Acceptance (PASS iff ALL; class in brackets):**
- AC1.1 [DET] probe 1 → exit 1, hit_count 0.
- AC1.2 [DET] probe 2 → exit 1, hit_count 0.
- AC1.3 [DET] probe 3 → exit 0, contains in-sync confirmation, NO `DIFFERS`/`MISSING`.
- AC1.4 [DET] probe 4 → 0 lines.
- AC1.5 [DET] **(falsification)** probe 5 → ≥1 line. *If empty, the test FAILS even if AC1.1/1.2 "passed" — a clean sweep is only trustworthy when the same tool on the same file proves it CAN find a present token.*
- AC1.6 [DET] **(falsification)** probe 6 → ≥1 (the replacement backend IS wired, so AC1.1's 0-hits isn't from an empty/missing file).

---

## TEST E2 — Adapter Contract Round-Trip (Producer ↔ Consumer)  (dimension 2)

**Scope IN:** presence of all 7 wire fields in `T1`,`P1`,`R1`; the 2 enum literals on `P1`+`R1`; `contract_version 1.1.0`; the 5 adapter rows; no field leak in the `## TFEP Consumer` block. **OUT:** control flow (E3); runtime values.

**Probes** (`LC_ALL=C`):
1. 7-field × 3-surface count loop: `for f in <7 fields>: rg -c "$f" T1 ; rg -c "$f" P1 ; rg -c "$f" R1` → every cell **≥1** (21 non-zero cells).
2. `rg -c "TFEP adapter field \(contract v1.1.0" P1` → **exactly 5**.
3. `rg -n "Output-contract semver, default .1\.1\.0" P1` → **≥1, exit 0**.
4. `rg -n "none\|retry\|escalate_depth\|halt" P1 R1` → **≥1 hit in EACH**.
5. `rg -n "test\|code\|docs\|none" P1 R1` → **≥1 hit in EACH**.
6. `rg -n "Diagnostic backend.*troubleshoot" T1` → **exactly 1**.
7. **Falsification (no field leak):** extract the `## TFEP Consumer` yaml block from `R1` (`sed -n '/## TFEP Consumer/,/^## /p' R1`) and `rg "tier_reached|confidence:|escalation_reason"` → **0 hits**.

**Acceptance (PASS iff ALL):**
- AC2.1 [DET] all 21 cells ≥1.
- AC2.2 [DET] adapter-row count in `P1` == **exactly 5** (not ≥5).
- AC2.3 [DET] `contract_version 1.1.0` present in `P1`.
- AC2.4 [DET] `recommended_escalation` enum verbatim in BOTH `P1` and `R1`.
- AC2.5 [DET] `remediation_target` enum verbatim in BOTH `P1` and `R1`.
- AC2.6 [DET] exactly one `**Diagnostic backend:** troubleshoot` declaration in `T1`.
- AC2.7 [DET] **(falsification)** the `## TFEP Consumer` block exposes ZERO producer-internal fields (`tier_reached`/`confidence:`/`escalation_reason`). *Proves the wire set is exactly 7, not ≥7.*

---

## TEST E3 — Protocol-Chain Resolution (Trigger→Freeze→Dispatch→Return→Branch→Resume)  (dimension 3)

**Scope IN:** presence + linkage of each chain hop as a clause in `T1`/`P1`/`C1`; depth mapping; the Step 4 branch ladder; loop discipline. Static chain trace (not live execution). **OUT:** freeze byte-identity (E4); residual (E1); field matrix (E2).

**Probes** (`LC_ALL=C`, anchored to exact clauses):
1. H1 `rg -n "Write context to .\{output_dir\}/context\.yaml" T1` (context bound to `{context_path}`) → exit 0.
2. H2 `rg -n "sc:troubleshoot --caller task-unified --context \{context_path\} --output-dir \{output_dir\} --depth \{depth\}" T1` → exit 0.
3. H3 dispatch carries `Pass NO .--fix` prohibition → exit 0.
4. H4 `rg -n "When .caller=task-unified., mark Wave 5 to emit .return-contract\.yaml" P1` (Wave 0 ingest) → exit 0.
5. H5 `rg -n "Emit TFEP return-contract|return-contract\.yaml` is written and its path returned" P1` (Wave 5 step 4.5) → exit 0.
6. H6 branch ladder: `rg -n "first match wins|test_is_wrong == true|remediation_target == .docs.|status == .success.|recommended_escalation == .(none|retry|escalate_depth|halt)." T1` → all branch keys + precedence note.
7. H7 loop discipline: `rg -n "increment .escalation_count.|FULL STOP" T1` → exit 0.
8. H8 depth map: `rg -n "1st TFEP trigger|2nd TFEP trigger|systemic failure OR ≥3 new failing tests|3rd TFEP trigger|--depth standard|--depth deep" T1` → exit 0.
9. H9 **Falsification (no live `--fix`):** `TOTAL=$(rg -c -- "--fix" T1); PROHIB=$(rg -c "NO .--fix|Pass NO .--fix|with NO --fix" T1); [ "$TOTAL" = "$PROHIB" ]`.
10. H10 **Falsification (old flags gone):** `rg -c -- "--tier|--intent" T1 T2 C1 P1 R1` → **0**.

**Acceptance (PASS iff ALL):**
- AC3.1 [DET] H1 context-binding present.
- AC3.2 [DET] H2 exact dispatch shape present (missing any of `--caller task-unified`/`--context`/`--output-dir`/`--depth` FAILS).
- AC3.3 [DET] H4 ingest + H5 emit, both gated on `caller=task-unified`.
- AC3.4 [DET] H6 all six branch keys + first-match-wins/asymmetric-first precedence note.
- AC3.5 [DET] H7 `escalation_count` increment + `FULL STOP` for halt/failed.
- AC3.6 [DET] H8 depth mapping for all three trigger ordinals.
- AC3.7 [DET] **(falsification)** H9 `FIX_TOTAL == FIX_PROHIBITION` in `T1`. *Every `--fix` must be inside a "NO --fix" clause; one live `--fix` argument = the most dangerous regression (auto-applying fixes inside TFEP) → MUST FAIL.*
- AC3.8 [DET] **(falsification)** H10 zero `--tier`/`--intent` across all 5 files.
- AC3.9 [JUDGMENT, anchored] one bounded conclusion — the chain is continuous because every output a step requires has a later producer/ingester anchor; MUST cite only H2/H4/H5/H6 line anchors (no unstated protocol inference). *(1 of the suite's ≤2 judgment criteria.)*

---

## TEST E4 — Safety-Invariant Preservation  (dimension 4)

**Scope IN:** byte-`diff` of live Step 1 freeze block vs baseline; both asymmetric gates with "do-not-auto-apply" semantics; exactly-one backend declaration + neutral framing clause; incident-report rebind to troubleshoot artifacts; report-template asymmetric rendering rules. **OUT:** chain wiring (E3); field matrix (E2); residual (E1).

**Probes** (`LC_ALL=C`):
1. I1 freeze byte-identity: build expected block from baseline; extract live Step 1 block via `sed -n '/\*\*Step 1: Halt and freeze\*\*/,/FREEZE.*implementation/p' T1`; `diff -u expected live` → **exit 0**. Cross-check baseline file contains the verbatim block (else "unverifiable") via `rg -n "STOP.* testing immediately|FREEZE.*implementation.*no further code changes permitted" BASE` → ≥1. *(Regex tolerates the markdown bold `**STOP**` and the single-codepoint em-dash `—` per the v1 run's E4-I1b probe-artifact finding; `.*` spans them. AC4.1's `diff -u` already guarantees byte-identity — this cross-check only proves the baseline is non-empty.)*
2. I2 asymmetric gates: `rg -n "test_is_wrong == true.*Present to user|Do NOT auto-fix tests" T1` AND `rg -n "remediation_target == .docs.*present to user|Do NOT auto-insert" T1`.
3. I3 backend-neutral: `rg -c "\*\*Diagnostic backend:\*\*" T1` → **1**; `rg -n "backend-neutral|swapping the backend changes only this declaration" T1` → ≥1.
4. I4 incident rebind: `rg -n "Diagnostic artifacts.*report_path.*REPORT\.md.*audit_log_path" T1` → ≥1 (no `rca-verdict`/`solution-verdict`). *(Regex uses `.*` separators to tolerate the actual markdown punctuation `` `report_path` (REPORT.md) `` — backtick+space+paren — per the v1 run's E4-I4a probe-artifact finding.)*
5. I5 report-template asymmetric rules: `rg -n "Files that MUST NOT change|behavior_is_documented" R1` → ≥1.
6. I6 **Falsification (no backend token in freeze):** `rg -n "forensic|troubleshoot" <live freeze block>` → **0 hits (exit 1)**.

**Acceptance (PASS iff ALL):**
- AC4.1 [DET] freeze `diff -u` → exit 0 (any single-char drift FAILS).
- AC4.2 [DET] both asymmetric gates present with present-for-review (non-auto-apply) semantics.
- AC4.3 [DET] exactly one `**Diagnostic backend:**` declaration + neutral framing clause.
- AC4.4 [DET] incident-report `Diagnostic artifacts` sourced from `report_path`/`audit_log_path` (not forensic verdict files).
- AC4.5 [DET] report-template asymmetric rendering rules present.
- AC4.6 [DET] **(falsification)** freeze block contains NEITHER `forensic` NOR `troubleshoot` (freeze is backend-agnostic).
- AC4.7 [DET] **(falsification)** baseline self-consistency — the baseline file actually contains the block (so AC4.1's match can't be vacuous against an empty/missing baseline).

---

## 1. Per-run evidence artifacts (every run writes exactly two files)

Path: `.dev/brainstorms/20260617-0148-tfep-e2e-validation/evidence/<TEST>/run-<N>/{verdict.yaml,findings.md}`

### `verdict.yaml` (machine-readable, strict schema)
```yaml
schema_version: "1.0.0"
test_id: <E1|E2|E3|E4>
test_name: <string>
run_index: <1|2|3>
verdict: <PASS|FAIL>
verdict_reason: <null|first-failure description>
started_at_utc: <ISO-8601>            # volatile — excluded from digest
ended_at_utc: <ISO-8601>              # volatile — excluded from digest
worktree: /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend
commands:
  - id: <stable id>
    command: <exact string incl. LC_ALL=C>
    exit_code: <int>
    stdout_sha256: <hex>
    stderr_sha256: <hex>
criteria:
  - id: <AC id>
    class: <DETERMINISTIC|JUDGMENT>
    expected: <string>
    observed: <string>
    result: <PASS|FAIL>
    evidence_ref: <command id or file:line anchor>
normalized_observations:               # stable keys only — counts/booleans/exact tokens
  <per-test keys, e.g. residual_hit_count: 0, adapter_row_count: 5, freeze_diff_exit: 0, fix_total: N, fix_prohibition: N>
normalized_observation_digest: <sha256 of canonicalized normalized_observations>
```
Canonicalization: sort keys + unordered lists lexicographically; lowercase booleans; OMIT volatile fields (run_index, timestamps, durations, artifact_dir, agent_name). `verdict: PASS` only if every `criteria[*].result == PASS`.

**Digest determinism rule (v1 E3-digest fix):** `normalized_observations` MUST contain ONLY acceptance-bearing, canonically-derived values (exit codes, exact counts of a FIXED expected set, booleans, exact tokens). It MUST NOT contain raw `rg` *line-match counts* that vary with how an agent slices output (these are not acceptance inputs and drift across runs). Concretely, for E3 do NOT record `branch_keys_found_count` as a raw `rg` line count; either record `branch_keys_all_present: <bool>` (true iff all 6 canonical branch keys + the first-match-wins note are found) or omit the key entirely. This guarantees the 3 per-test digests are byte-identical when the underlying file state is unchanged.

### `findings.md` (human-readable, re-derivation-free)
Per probe: the exact command, verbatim stdout, `EXIT=<n>`; then a 2–4 sentence findings paragraph. A reviewer confirms any criterion by *trusting-or-re-running one command* — never by re-tracing the protocol.

## 2. 3× execution + aggregation protocol (12 runs)

**Orchestration:** 4 sequential batches (one per test) × 3 parallel runs each. Each batch spawns its 3
runs in a single parallel message (shared no state); orchestrator waits for all 3 before the next batch.
After all 12 land, spawn ONE **aggregator subagent**. Each run gets only `(test_id, run_index, run_dir)`;
the embedded prompt is otherwise byte-identical across a test's 3 runs; absolute paths pinned (no cwd drift);
each run re-executes every probe itself and never reads a sibling run's artifacts.

**Reproducibility gate (strict 12/12 + digest identity):** per test, the 3 runs must ALL be `PASS` AND
their 3 `normalized_observation_digest` values must be byte-identical. Mismatch → test status `DISAGREE`.

**Aggregator outputs** `evidence/roll-up.yaml` + `evidence/dashboard.md`:
```
overall_gate = GREEN  iff  ∀ test ∈ {E1,E2,E3,E4}: 3/3 PASS AND 3/3 identical digests   (12/12)
suite_failure_class ∈ {none, missing_artifact, schema_invalid, run_failed, cross_run_disagreement}
- any DISAGREE (split verdict or digest mismatch) → overall INDETERMINATE + mandatory human-halt (NOT silently RED)
- any unanimous FAIL → MIGRATION_NOT_VALIDATED with failing AC ids enumerated
```
`dashboard.md` renders the 4×3 PASS/FAIL matrix + cross-run column + the GREEN/RED/INDETERMINATE gate.

**Why strict 12/12, not majority:** the suite's purpose is to prove the migration validates
*reproducibly*; a 2/3 split is the exact defect class being hunted (non-deterministic probe or a file
mutated mid-suite), so it is surfaced (INDETERMINATE + halt), never averaged away.

**Idempotency / cost:** read-only probes only; evidence root is append-only (a re-run creates a new
timestamped root, never overwrites). ~2K tokens/run, ~27K total incl. aggregator; 5-min per-subagent
timeout (→ `verdict: FAIL, reason: timeout`); fail-fast within a run captures first-failure context.

## 3. Human audit trail (end-to-end)

A reviewer reads, in order: (1) `dashboard.md` — one glance answers "did the migration validate?";
(2) `roll-up.yaml` — machine verdict + per-test digests + failure class; (3) any `evidence/<TEST>/run-N/`
— the `verdict.yaml` criteria block (per-criterion result + exit codes + counts) and `findings.md`
(literal command + stdout behind every claim). The trail is **re-derivation-free** and every green is
**positive evidence** (each test's falsification criterion proves presence/identity/absence, not "found nothing").

## 4. Definition of done

`MIGRATION_VALIDATED` ⟺ `dashboard.md` shows GREEN ⟺ 4 tests × 3 runs = **12/12 PASS with 3/3 identical
per-test digests**, all 23 acceptance criteria (E1:6, E2:7, E3:9, E4:7 — minus the 1 shared `--fix`
overlap counted once operationally) satisfied, suite_failure_class `none`. Judgment criteria total = 1
(E3-AC3.9), anchored. Any other state → INDETERMINATE (halt) or MIGRATION_NOT_VALIDATED.
