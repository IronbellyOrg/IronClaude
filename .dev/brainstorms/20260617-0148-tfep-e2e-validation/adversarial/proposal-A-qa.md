# Proposal A — QA Architect: Exhaustive E2E Validation Suite with Binary Acceptance + Falsification

**Lens**: Every test PASS must mean "we proved the desired outcome held", not "we ran some greps and found nothing alarming." Each test carries at least one **falsification check** — a probe whose non-zero/non-empty result FAILS the test — so a green verdict is positive evidence, not absence of evidence. All numeric thresholds are pinned to the seed-brief enrichment surface and re-verified against the live files at design time (residual sweep = 0 hits / exit 1; adapter rows = 5; one `**Diagnostic backend:**` declaration; freeze block byte-identical to the recorded baseline).

---

## 0. Conventions binding all four tests

- **Worktree root** (`$ROOT`): `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend`
- **The 5 migrated files** (the ONLY in-scope surface):
  - `src/superclaude/skills/sc-task-protocol/SKILL.md` (§4.5 TFEP consumer) — `T1`
  - `src/superclaude/commands/task.md` — `T2`
  - `src/superclaude/commands/troubleshoot.md` — `C1`
  - `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (producer) — `P1`
  - `src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md` (`## TFEP Consumer`) — `R1`
- **The 7-field wire set**: `status`, `test_is_wrong`, `recommended_escalation`, `tasklist_insertion_path`, `remediation_target`, `root_cause_summary`, `solution_summary`
- **Enum literals**: `recommended_escalation ∈ {none, retry, escalate_depth, halt}`; `remediation_target ∈ {test, code, docs, none}`
- **Freeze baseline file**: `.dev/tasks/to-do/TASK-RF-tfep-troubleshoot-migration-20260616-174519/phase-outputs/plans/freeze-block-preserved.md`
- **Out of scope for ALL tests** (explicit ignore-list): bare `forensic` as generic vocabulary in `cli-eval`, `sc-crash-recovery`, `sc-brainstorm-protocol`, `sc-reflect-protocol`, and any other non-migrated skill. Tests NEVER sweep the whole repo for bare `forensic`; the residual sweep is scoped to `T1` + `T2` only (where the backend token was actually removed), and the `/sc:forensic` literal sweep is repo-wide because that EXACT literal must be zero everywhere in `src/`.
- **Determinism rule**: every probe is a shell command with a captured exit code and captured stdout. LLM judgment is permitted ONLY to (a) confirm a quoted block is byte-identical to a quoted baseline (mechanically backed by `diff`), and (b) author the human-findings prose. No acceptance criterion depends on un-grounded LLM opinion.

**Coverage map (no gap, minimal overlap):**

| Test | Outcome dimension (seed §"desired outcome") | Primary surface |
|------|----------------------------------------------|-----------------|
| **E1** | Dimension 1 — Backend swap complete + clean (residual + sync parity) | T1, T2, src/, .claude/ |
| **E2** | Dimension 2 — Adapter contract integrity (producer↔consumer round-trip) | T1, P1, R1 |
| **E3** | Dimension 3 — End-to-end protocol chain resolves (trigger→freeze→dispatch→return→branch→resume) | T1, P1, C1 |
| **E4** | Dimension 4 — Safety invariants preserved (freeze byte-identity, no `--fix`, asymmetric gates, backend-neutral prose) | T1, baseline file |

E1 owns *removal*; E2 owns *cross-surface field identity*; E3 owns *control-flow wiring*; E4 owns *invariant preservation*. The only deliberate overlap is the "no live `--fix` in dispatch" check (touched by E3's chain trace AND E4's safety lens) — E3 checks it as a chain-correctness property, E4 checks it as a safety invariant with the prohibition-vs-live disambiguation; this redundancy is intentional defense-in-depth on the single highest-cost regression.

---

## TEST E1 — Residual-Integrity & Sync-Parity

**ID**: `E1-residual-sync`
**Validates**: Dimension 1 — the `/sc:forensic` backend and its vocabulary (`forensic`, `--tier`, `--intent`, `rca-verdict`, `solution-verdict`) are fully removed from the two task-protocol files; `src/` has zero `/sc:forensic`; src↔.claude parity holds (verify-sync EXIT 0); nothing under `.claude/` is staged.

**Scope**:
- IN: residual token sweep over `T1` + `T2` only; repo-wide `/sc:forensic` literal sweep over `src/`; `make verify-sync` exit code + output; `git status --porcelain` filtered to `.claude/`.
- OUT: bare `forensic` anywhere outside `T1`/`T2` (generic vocabulary — explicitly NOT a failure); any content correctness of the migration (that's E2–E4).

### Delegable subagent prompt (copy-paste to spawn)

```
You are an independent E2E validation subagent. Run READ-ONLY. Do NOT edit, stage, or
commit anything. Your job: validate that the TFEP forensic→troubleshoot backend swap is
residually clean and src↔.claude is in sync. Emit one evidence file; do not fix anything.

cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend

Run these probes verbatim, capturing each command's stdout AND exit code:

  P1: rg -n "/sc:forensic|\bforensic\b|--tier|--intent|rca-verdict|solution-verdict" \
        src/superclaude/skills/sc-task-protocol/SKILL.md src/superclaude/commands/task.md ; echo "EXIT=$?"
  P2: rg -n "/sc:forensic" src/ ; echo "EXIT=$?"
  P3: make verify-sync ; echo "EXIT=$?"
  P4: git status --porcelain | grep '\.claude/' ; echo "EXIT=$?"
  P5 (falsification probe — proves the sweep CAN detect a token, i.e. it isn't silently
      matching nothing due to a broken regex): rg -n "troubleshoot" \
        src/superclaude/skills/sc-task-protocol/SKILL.md | head -1 ; echo "EXIT=$?"

Apply the ACCEPTANCE CRITERIA below; PASS iff ALL hold. Write your evidence file to:
  <RUN_ARTIFACT_PATH>   (provided by the spawner; e.g.
  .dev/brainstorms/20260617-0148-tfep-e2e-validation/evidence/E1/run-<N>.md)
using the EVIDENCE SCHEMA below. Return the verdict (PASS/FAIL) and the artifact path.
```

### Ordered probe steps (deterministic)

1. `rg -n "/sc:forensic|\bforensic\b|--tier|--intent|rca-verdict|solution-verdict" src/superclaude/skills/sc-task-protocol/SKILL.md src/superclaude/commands/task.md` → expect **0 lines, exit 1**.
2. `rg -n "/sc:forensic" src/` → expect **0 lines, exit 1**.
3. `make verify-sync` → expect **exit 0** and output containing `All components in sync` (or equivalent), with NO `DIFFERS`/`MISSING`.
4. `git status --porcelain | grep '\.claude/'` → expect **0 lines** (grep exit 1).
5. **Falsification/sanity probe**: `rg -n "troubleshoot" src/superclaude/skills/sc-task-protocol/SKILL.md` → expect **≥1 line, exit 0**. (Proves the regex engine and file path are live; a 0-result here would mean P1's "0 hits" is a false negative from a broken probe, not a clean file.)

### Binary acceptance criteria (PASS iff ALL hold)

- **AC1.1** — P1 returns exit code 1 AND zero matching lines.
- **AC1.2** — P2 returns exit code 1 AND zero matching lines.
- **AC1.3** — P3 (`make verify-sync`) returns exit code 0 AND stdout contains an in-sync confirmation AND contains NO substring `DIFFERS` and NO substring `MISSING`.
- **AC1.4** — P4 returns zero lines (no `.claude/` path staged or modified-in-index).
- **AC1.5 (FALSIFICATION)** — P5 returns exit 0 with ≥1 line. **If P5 is empty, the test MUST FAIL** even if AC1.1/AC1.2 "passed" — a clean sweep is only trustworthy when the same tool on the same file is proven able to find a token that IS present.
- **AC1.6 (FALSIFICATION — token reappearance)** — If ANY of `/sc:forensic`, `--tier`, `--intent`, `rca-verdict`, `solution-verdict`, or word-boundary `forensic` reappears in `T1` or `T2` on a future run, AC1.1 fails and the test MUST FAIL. This criterion is the standing regression tripwire.

### Evidence-artifact schema (`evidence/E1/run-<N>.md`)

```yaml
---
test_id: E1-residual-sync
run: <N>
timestamp: <ISO-8601>
verdict: <PASS|FAIL>
criteria:
  AC1.1_residual_task_files: {pass: <bool>, exit: <int>, hit_count: <int>}
  AC1.2_forensic_literal_src: {pass: <bool>, exit: <int>, hit_count: <int>}
  AC1.3_verify_sync: {pass: <bool>, exit: <int>, differs: <bool>, missing: <bool>}
  AC1.4_claude_staged: {pass: <bool>, line_count: <int>}
  AC1.5_falsification_probe_live: {pass: <bool>, exit: <int>, hit_count: <int>}
  AC1.6_token_reappearance_tripwire: {pass: <bool>, reappeared_tokens: []}
---
```
Followed by `## Raw command outputs` (each command + verbatim stdout + `EXIT=<n>`) and `## Human findings` (2–4 sentences).

---

## TEST E2 — Adapter Contract Round-Trip (Producer ↔ Consumer)

**ID**: `E2-contract-roundtrip`
**Validates**: Dimension 2 — every one of the 7 wire-set fields the §4.5 consumer reads has a producer in BOTH the troubleshoot Output Contract (`P1`) AND the report-template `## TFEP Consumer` block (`R1`); the enum literals byte-match across surfaces; `contract_version` is `1.1.0`; the 5 TFEP adapter rows exist in `P1`.

**Scope**:
- IN: presence of all 7 tokens in `T1` (§4.5), `P1` (Output Contract), `R1` (`## TFEP Consumer`); the two enum literal sets; `contract_version` default; adapter-row count.
- OUT: control-flow / branch semantics (that's E3); whether the field VALUES are correct at runtime (un-testable statically — out of every test's scope).

### Delegable subagent prompt (copy-paste to spawn)

```
You are an independent E2E validation subagent. Run READ-ONLY. Do NOT edit/stage/commit.
Validate the TFEP adapter contract is identical across producer and consumer surfaces.

cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend

For each of the 7 wire fields, confirm presence in all three surfaces:

  FIELDS="status test_is_wrong recommended_escalation tasklist_insertion_path \
          remediation_target root_cause_summary solution_summary"
  for f in $FIELDS; do
    a=$(rg -c "$f" src/superclaude/skills/sc-task-protocol/SKILL.md)
    b=$(rg -c "$f" src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md)
    c=$(rg -c "$f" src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md)
    echo "$f T1=$a P1=$b R1=$c"
  done

  # Enum literals must appear verbatim in BOTH P1 (producer) and R1 (template):
  rg -n "none\|retry\|escalate_depth\|halt" \
     src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md \
     src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md ; echo "EXIT=$?"
  rg -n "test\|code\|docs\|none" \
     src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md \
     src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md ; echo "EXIT=$?"

  # Adapter rows + version stamp in P1:
  rg -c "TFEP adapter field \(contract v1.1.0" \
     src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md
  rg -n "contract_version.*1\.1\.0" \
     src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md ; echo "EXIT=$?"

  # FALSIFICATION: a field NOT in the wire set must NOT leak into the R1 TFEP Consumer
  # YAML block (e.g. 'tier_reached' is producer-internal, must not appear in the block).
  sed -n '/## TFEP Consumer/,/^## /p' \
     src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md \
     | rg -n "tier_reached|confidence:|escalation_reason" ; echo "NEG_EXIT=$?"

Apply ACCEPTANCE CRITERIA; PASS iff ALL hold. Write evidence to <RUN_ARTIFACT_PATH>
(.dev/brainstorms/20260617-0148-tfep-e2e-validation/evidence/E2/run-<N>.md). Return verdict + path.
```

### Ordered probe steps

1. 7-field × 3-surface presence loop → each field's `T1`, `P1`, `R1` count must be **≥1**.
2. `rg -n "none\|retry\|escalate_depth\|halt" P1 R1` → **≥1 hit in EACH file** (the `recommended_escalation` enum literal is present and byte-identical on both surfaces).
3. `rg -n "test\|code\|docs\|none" P1 R1` → **≥1 hit in EACH file** (the `remediation_target` enum literal).
4. `rg -c "TFEP adapter field \(contract v1.1.0" P1` → **exactly 5**.
5. `rg -n "contract_version.*1\.1\.0" P1` → **≥1 hit, exit 0**.
6. **Falsification (leak check)**: extract the `## TFEP Consumer` YAML block from `R1` and grep for producer-internal fields (`tier_reached`, `confidence:`, `escalation_reason`) → expect **0 hits** (the consumer block exposes ONLY the 7 wire fields).

### Binary acceptance criteria (PASS iff ALL hold)

- **AC2.1** — All 7 fields have count ≥1 in `T1` AND ≥1 in `P1` AND ≥1 in `R1` (21 non-zero cells). Any zero cell FAILS.
- **AC2.2** — `recommended_escalation` enum literal `none|retry|escalate_depth|halt` appears verbatim in BOTH `P1` and `R1`.
- **AC2.3** — `remediation_target` enum literal `test|code|docs|none` appears verbatim in BOTH `P1` and `R1`.
- **AC2.4** — Adapter-row count in `P1` is **exactly 5** (not ≥5, not 4 — exactly 5).
- **AC2.5** — `contract_version` `1.1.0` present in `P1`.
- **AC2.6 (FALSIFICATION — no field leak)** — The `## TFEP Consumer` YAML block in `R1` contains ZERO of {`tier_reached`, `confidence:`, `escalation_reason`}. **If any producer-internal field leaks into the wire block, the test MUST FAIL** — a contract that exposes 8+ fields is as wrong as one that exposes 6. This proves the wire set is *exactly* 7, not "at least 7."

### Evidence-artifact schema (`evidence/E2/run-<N>.md`)

```yaml
---
test_id: E2-contract-roundtrip
run: <N>
timestamp: <ISO-8601>
verdict: <PASS|FAIL>
criteria:
  AC2.1_seven_fields_three_surfaces:
    pass: <bool>
    matrix: {status: [<T1>,<P1>,<R1>], test_is_wrong: [...], recommended_escalation: [...],
             tasklist_insertion_path: [...], remediation_target: [...],
             root_cause_summary: [...], solution_summary: [...]}
  AC2.2_escalation_enum_both_surfaces: {pass: <bool>, P1: <bool>, R1: <bool>}
  AC2.3_remediation_enum_both_surfaces: {pass: <bool>, P1: <bool>, R1: <bool>}
  AC2.4_adapter_rows: {pass: <bool>, count: <int>}
  AC2.5_contract_version: {pass: <bool>, found: <bool>}
  AC2.6_no_field_leak: {pass: <bool>, leaked_fields: []}
---
```
Followed by `## Raw command outputs` and `## Human findings`.

---

## TEST E3 — Protocol-Chain Resolution (Trigger → Freeze → Dispatch → Return → Branch → Resume)

**ID**: `E3-chain-trace`
**Validates**: Dimension 3 — the full TFEP control flow is wired and terminating: trigger detection → Step 1 freeze → Step 2 `context.yaml` bound to `{context_path}` → Step 3 dispatch `/sc:troubleshoot --caller task-unified --context {context_path} --output-dir {output_dir} --depth {standard|deep}` with **NO `--fix`** → P1 Wave 0 step 6 ingests `--caller`/`--context` → P1 Wave 5 step 4.5 emits `return-contract.yaml` when `caller=task-unified` → Step 4 consumes + branches on the adapter enum (first-match-wins) → Step 5 composes + inserts → Step 6 resumes. Depth mapping consistent (1st→standard; escalation/systemic/≥3-new→deep; 3rd→FULL STOP).

**Scope**:
- IN: presence + linkage of each chain hop as a token/clause in `T1`/`P1`/`C1`; the depth-mapping clauses; the Step 4 branch ladder's six branch keys; loop discipline (increment `escalation_count`, halt/failed → immediate FULL STOP). This is a STATIC chain trace, not a live execution — each hop is verified by locating the clause that wires it.
- OUT: byte-identity of the freeze block (E4 owns that); residual cleanliness (E1); field-presence matrix (E2). E3 asserts the *edges of the graph exist and point correctly*, not the node internals.

### Delegable subagent prompt (copy-paste to spawn)

```
You are an independent E2E validation subagent. Run READ-ONLY. Do NOT edit/stage/commit.
Trace the TFEP protocol chain statically: confirm every hop's wiring clause exists and the
dispatch is diagnosis-only (no --fix). Emit one evidence file; fix nothing.

cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend
TASK=src/superclaude/skills/sc-task-protocol/SKILL.md
PROD=src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md

# H1 Step 2 context binding: context.yaml written to {output_dir}, IS the {context_path}
rg -n "context\.yaml" "$TASK" ; echo "EXIT=$?"
# H2 Step 3 dispatch (exact shape, NO --fix on the invocation line):
rg -n "sc:troubleshoot --caller task-unified --context \{context_path\} --output-dir \{output_dir\} --depth \{depth\}" "$TASK" ; echo "EXIT=$?"
# H3 dispatch line carries NO live --fix (the line must contain 'NO --fix' prohibition, and
# must NOT contain a bare '--fix ' as an argument). Extract the dispatch line(s) and inspect:
rg -n "sc:troubleshoot --caller task-unified" "$TASK"
# H4 producer ingests --caller/--context in Wave 0:
rg -n "If .--caller. is set|--context <path>. is set|caller=task-unified.*emit .return-contract" "$PROD" ; echo "EXIT=$?"
# H5 producer Wave 5 step 4.5 emits return-contract.yaml when caller=task-unified:
rg -n "Emit TFEP return-contract.*caller=task-unified|return-contract\.yaml" "$PROD" ; echo "EXIT=$?"
# H6 Step 4 branch ladder — all six branch keys, first-match-wins, asymmetric gates first:
rg -n "first match wins|test_is_wrong == true|remediation_target == .docs.|status == .success.|recommended_escalation == .none.|recommended_escalation == .retry.|recommended_escalation == .escalate_depth.|recommended_escalation == .halt." "$TASK" ; echo "EXIT=$?"
# H7 loop discipline: increment escalation_count; halt/failed -> immediate FULL STOP:
rg -n "increment .escalation_count.|FULL STOP" "$TASK" ; echo "EXIT=$?"
# H8 depth mapping consistency (standard for 1st; deep for systemic/>=3-new/2nd; 3rd FULL STOP):
rg -n "1st TFEP trigger|2nd TFEP trigger|3rd TFEP trigger|--depth standard|--depth deep" "$TASK" ; echo "EXIT=$?"

# FALSIFICATION H9: there must be NO live '--fix' token used as a troubleshoot ARGUMENT
# anywhere in $TASK. Every '--fix' occurrence must be inside a 'NO --fix' prohibition clause.
# Count total --fix vs --fix-inside-prohibition; they must be EQUAL.
TOTAL=$(rg -c -- "--fix" "$TASK"); PROHIB=$(rg -c "NO .--fix|Pass NO .--fix|with NO --fix" "$TASK")
echo "FIX_TOTAL=$TOTAL FIX_PROHIBITION=$PROHIB"

Apply ACCEPTANCE CRITERIA; PASS iff ALL hold. Write evidence to <RUN_ARTIFACT_PATH>
(.dev/brainstorms/20260617-0148-tfep-e2e-validation/evidence/E3/run-<N>.md). Return verdict + path.
```

### Ordered probe steps

1. **H1** Step 2 `context.yaml` binding present in `T1` → exit 0.
2. **H2** Step 3 dispatch line present with the exact `--caller task-unified --context {context_path} --output-dir {output_dir} --depth {depth}` shape → exit 0.
3. **H3** dispatch line read back: must contain the `NO --fix` prohibition clause; the invocation token sequence must not include `--fix` as an argument.
4. **H4** producer Wave 0 ingests `--caller`/`--context` → exit 0.
5. **H5** producer Wave 5 step 4.5 emits `return-contract.yaml` gated on `caller=task-unified` → exit 0.
6. **H6** Step 4 branch ladder: all six branch keys present + `first match wins` precedence note + asymmetric gates (`test_is_wrong`, `remediation_target == "docs"`) checked first → exit 0.
7. **H7** loop discipline clauses present (`increment escalation_count`; `FULL STOP` for halt/failed) → exit 0.
8. **H8** depth-mapping clauses present (1st→standard, 2nd/systemic/≥3-new→deep, 3rd→FULL STOP) → exit 0.
9. **H9 (falsification)**: `--fix` total count in `T1` EQUALS the count of `--fix` occurrences inside a `NO --fix` prohibition clause.

### Binary acceptance criteria (PASS iff ALL hold)

- **AC3.1** — H1 context-binding clause present (exit 0, ≥1 hit).
- **AC3.2** — H2 exact dispatch shape present (exit 0, ≥1 hit). A dispatch line missing `--caller task-unified` OR `--context` OR `--output-dir` OR `--depth` FAILS.
- **AC3.3** — H4 producer ingest clause present AND H5 return-contract emission clause present, both gated on `caller=task-unified`.
- **AC3.4** — H6 all six branch keys present (`test_is_wrong == true`, `remediation_target == "docs"`, `status == "success"`, and the four `recommended_escalation` enum branches) AND the first-match-wins/asymmetric-first precedence note present.
- **AC3.5** — H7 loop discipline present: `escalation_count` increment clause AND a `FULL STOP` clause for the `halt`/`failed` terminal.
- **AC3.6** — H8 depth mapping present for all three trigger ordinals.
- **AC3.7 (FALSIFICATION — no live `--fix`)** — `FIX_TOTAL == FIX_PROHIBITION` in `T1`. **If even one `--fix` appears outside a prohibition clause (i.e. as a live argument), the test MUST FAIL.** A diagnosis-only dispatch that silently regained `--fix` would auto-apply code fixes inside TFEP — the single most dangerous regression — so this criterion is non-negotiable and is checked here AND in E4.

### Evidence-artifact schema (`evidence/E3/run-<N>.md`)

```yaml
---
test_id: E3-chain-trace
run: <N>
timestamp: <ISO-8601>
verdict: <PASS|FAIL>
criteria:
  AC3.1_context_binding: {pass: <bool>, exit: <int>}
  AC3.2_dispatch_shape: {pass: <bool>, exit: <int>, has_caller: <bool>, has_context: <bool>,
                         has_output_dir: <bool>, has_depth: <bool>}
  AC3.3_producer_ingest_and_emit: {pass: <bool>, wave0_ingest: <bool>, wave5_emit: <bool>}
  AC3.4_branch_ladder: {pass: <bool>, keys_found: [...], first_match_note: <bool>}
  AC3.5_loop_discipline: {pass: <bool>, increment: <bool>, full_stop: <bool>}
  AC3.6_depth_mapping: {pass: <bool>, first: <bool>, second: <bool>, third_fullstop: <bool>}
  AC3.7_no_live_fix: {pass: <bool>, fix_total: <int>, fix_prohibition: <int>}
---
```
Followed by `## Raw command outputs` and `## Human findings`.

---

## TEST E4 — Safety-Invariant Preservation

**ID**: `E4-safety-invariants`
**Validates**: Dimension 4 — Step 1 freeze block is **byte-identical** to the recorded pre-migration baseline; the asymmetric-cost gates are present (`test_is_wrong` → present-for-review, `remediation_target == "docs"` → present-for-review, both "do not auto-apply"); the prose is backend-neutral (exactly one `**Diagnostic backend:** troubleshoot` declaration; a future swap touches only that declaration + invocation strings).

**Scope**:
- IN: `diff` of the live Step 1 freeze block against the baseline file's verbatim block; presence of both asymmetric gates with their "do NOT auto-fix / present to user" semantics; exactly-one `**Diagnostic backend:**` declaration; backend-neutral framing clause.
- OUT: chain wiring (E3); contract field matrix (E2); residual sweep (E1). E4 is the invariant lens — it asserts what must NOT have changed.

### Delegable subagent prompt (copy-paste to spawn)

```
You are an independent E2E validation subagent. Run READ-ONLY. Do NOT edit/stage/commit.
Validate TFEP safety invariants survived the migration byte-for-byte. Emit one evidence
file; fix nothing.

cd /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend
TASK=src/superclaude/skills/sc-task-protocol/SKILL.md
BASE=.dev/tasks/to-do/TASK-RF-tfep-troubleshoot-migration-20260616-174519/phase-outputs/plans/freeze-block-preserved.md

# I1 Freeze byte-identity: extract the live Step 1 freeze block (the two numbered lines)
# and diff against the baseline's recorded verbatim block.
printf '%s\n' '**Step 1: Halt and freeze**' '' \
  '1. **STOP** testing immediately.' \
  '2. **FREEZE** implementation — no further code changes permitted.' > /tmp/e4_expected.txt
# Pull the live block from the task SKILL (Step 1 header through the FREEZE line):
sed -n '/\*\*Step 1: Halt and freeze\*\*/,/FREEZE.*implementation/p' "$TASK" > /tmp/e4_live.txt
diff -u /tmp/e4_expected.txt /tmp/e4_live.txt ; echo "DIFF_EXIT=$?"
# Cross-check the baseline file actually contains the same verbatim block:
rg -n "STOP. testing immediately|FREEZE.*implementation .. no further code changes permitted" "$BASE" ; echo "EXIT=$?"

# I2 Asymmetric gates present with present-for-review semantics (NOT auto-fix):
rg -n "test_is_wrong == true.*Present to user|Do NOT auto-fix tests" "$TASK" ; echo "EXIT=$?"
rg -n "remediation_target == .docs.*present to user|Do NOT auto-insert" "$TASK" ; echo "EXIT=$?"

# I3 Backend-neutral: EXACTLY one Diagnostic backend declaration + neutral framing clause:
rg -c "\*\*Diagnostic backend:\*\*" "$TASK"        # expect 1
rg -n "backend-neutral|swapping the backend changes only this declaration" "$TASK" ; echo "EXIT=$?"

# FALSIFICATION I4: the freeze block must NOT contain backend vocabulary (forensic OR
# troubleshoot) — it is meant to be backend-agnostic. A backend token inside the freeze
# block is a regression.
rg -n "forensic|troubleshoot" /tmp/e4_live.txt ; echo "NEG_EXIT=$?"

Apply ACCEPTANCE CRITERIA; PASS iff ALL hold. Write evidence to <RUN_ARTIFACT_PATH>
(.dev/brainstorms/20260617-0148-tfep-e2e-validation/evidence/E4/run-<N>.md). Return verdict + path.
```

### Ordered probe steps

1. **I1** Build `/tmp/e4_expected.txt` from the baseline's verbatim block; extract live block to `/tmp/e4_live.txt`; `diff -u` → expect **DIFF_EXIT=0** (identical). Cross-check baseline file contains the block.
2. **I2** Asymmetric gate `test_is_wrong == true` → "Present to user / Do NOT auto-fix tests" clause present; `remediation_target == "docs"` → "present to user / Do NOT auto-insert" clause present.
3. **I3** `rg -c "\*\*Diagnostic backend:\*\*"` → **exactly 1**; backend-neutral framing clause present.
4. **I4 (falsification)** freeze block (`/tmp/e4_live.txt`) contains NEITHER `forensic` NOR `troubleshoot` → grep exit 1 (NEG_EXIT=1).

### Binary acceptance criteria (PASS iff ALL hold)

- **AC4.1 (byte-identity)** — `diff -u` between the baseline verbatim freeze block and the live Step 1 block returns **exit 0 (zero differences)**. Any single-character drift FAILS.
- **AC4.2** — Both asymmetric-cost gates present with present-for-review (non-auto-apply) semantics: `test_is_wrong==true` → present/do-not-auto-fix; `remediation_target=="docs"` → present/do-not-auto-insert.
- **AC4.3** — Exactly **one** `**Diagnostic backend:**` declaration in `T1` (not 0, not 2) AND the backend-neutral framing clause present.
- **AC4.4 (FALSIFICATION — no backend token in freeze block)** — The extracted live freeze block contains NEITHER `forensic` NOR `troubleshoot`. **If a backend token has leaked into the freeze invariant, the test MUST FAIL** — the freeze block is by-design backend-agnostic, and contamination would mean a future backend swap must touch the safety invariant (violating the migration's stated neutrality goal).
- **AC4.5 (FALSIFICATION — baseline self-consistency)** — The baseline file itself must contain the verbatim block (so AC4.1's "identical" can't be a vacuous match against an empty/missing baseline). If the baseline cross-check (`rg` on `$BASE`) returns 0 hits, the test MUST FAIL as "baseline unverifiable."

### Evidence-artifact schema (`evidence/E4/run-<N>.md`)

```yaml
---
test_id: E4-safety-invariants
run: <N>
timestamp: <ISO-8601>
verdict: <PASS|FAIL>
criteria:
  AC4.1_freeze_byte_identity: {pass: <bool>, diff_exit: <int>, diff_lines: <int>}
  AC4.2_asymmetric_gates: {pass: <bool>, test_is_wrong_gate: <bool>, docs_gate: <bool>}
  AC4.3_backend_neutral: {pass: <bool>, declaration_count: <int>, neutral_clause: <bool>}
  AC4.4_no_backend_token_in_freeze: {pass: <bool>, neg_exit: <int>}
  AC4.5_baseline_self_consistent: {pass: <bool>, baseline_hits: <int>}
---
```
Followed by `## Raw command outputs` (including the full `diff -u` output) and `## Human findings`.

---

## 1. The 3× execution + aggregation protocol (12 runs)

### 1.1 Independence

Each of the 4 tests is run **3 times**, each run in a **fresh subagent context** spawned from the embedded prompt above with a distinct `<RUN_ARTIFACT_PATH>`. The 12 spawns share NO mutable state: no run reads another run's artifact, no run reuses a cached probe result, and each subagent re-executes every shell command itself. The spawner (parent orchestrator) passes only `(test_id, run_index, RUN_ARTIFACT_PATH)`; the prompt is otherwise byte-identical across the 3 runs of a test. Because every acceptance criterion is shell-exit-coded, three independent runs of a deterministic file state MUST produce identical verdicts — divergence across runs is itself a signal (flaky probe or a file mutated mid-suite) and forces a manual halt.

### 1.2 Artifact layout

```
.dev/brainstorms/20260617-0148-tfep-e2e-validation/evidence/
├── E1/  run-1.md  run-2.md  run-3.md
├── E2/  run-1.md  run-2.md  run-3.md
├── E3/  run-1.md  run-2.md  run-3.md
├── E4/  run-1.md  run-2.md  run-3.md
└── AGGREGATE.md            ← written by the aggregator after all 12 land
```

### 1.3 Cross-run agreement computation

The aggregator reads all 12 run files' YAML front-matter `verdict` fields and builds a 4×3 verdict matrix. Per test it computes:
- `unanimous` = (run-1 == run-2 == run-3).
- `test_verdict` = PASS iff all 3 runs are PASS (strict — see 1.4).
- `divergence_flag` = true iff the 3 verdicts are not unanimous.

### 1.4 Final "migration validated" verdict (strict 12/12)

```
MIGRATION_VALIDATED  iff  all 4 tests are unanimous PASS  ==  12/12 green.
```

Rationale for **strict 12/12, not majority**: the suite is fully deterministic (shell-exit-coded), so a 2/3 split is not "noise to be voted out" — it is evidence that either a probe is non-deterministic or a file changed between runs, both of which invalidate the audit. A non-unanimous test ⇒ overall verdict `INDETERMINATE` (not FAIL, not PASS) with a mandatory `divergence_flag` and a human-halt instruction in `AGGREGATE.md`. Any test unanimously FAIL ⇒ overall `MIGRATION_NOT_VALIDATED` with the failing criteria enumerated.

### 1.5 `AGGREGATE.md` schema

```yaml
---
suite: tfep-e2e-validation
generated: <ISO-8601>
overall_verdict: <MIGRATION_VALIDATED | MIGRATION_NOT_VALIDATED | INDETERMINATE>
green_count: <0-12>
matrix:
  E1-residual-sync:       {runs: [<v>,<v>,<v>], unanimous: <bool>, test_verdict: <PASS|FAIL>}
  E2-contract-roundtrip:  {runs: [...], unanimous: <bool>, test_verdict: <...>}
  E3-chain-trace:         {runs: [...], unanimous: <bool>, test_verdict: <...>}
  E4-safety-invariants:   {runs: [...], unanimous: <bool>, test_verdict: <...>}
divergences: [<test_id: which criterion differed across runs>]
failing_criteria: [<AC ids that failed in any unanimously-FAIL test>]
---
```
Followed by a per-test 1-paragraph human synthesis and a final "what a reviewer should conclude" line.

---

## 2. Human-readable audit trail (end-to-end, re-derivation-free)

A reviewer reads, in order:
1. **`AGGREGATE.md`** — the 4×3 matrix + `overall_verdict` + `green_count`. One glance answers "did the migration validate?"
2. **Each `E*/run-N.md`** — the YAML criteria block gives per-criterion pass/fail with the actual exit codes and hit counts; the `## Raw command outputs` section reproduces the literal commands + stdout the subagent saw, so the reviewer can re-run any single command to spot-check; the `## Human findings` paragraph explains the verdict in prose.

The trail is **re-derivation-free** because every PASS is backed by a captured exit code + captured stdout in the same file — a reviewer never has to re-trace the protocol or re-grep; they only have to *trust or re-run* the verbatim command. And because each test carries a falsification criterion (AC1.5/1.6, AC2.6, AC3.7, AC4.4/4.5), a green run is positive evidence of "we proved presence/identity/absence", not the weaker "we looked and found nothing."

---

## Summary (distinctive emphasis)

This proposal's distinctive emphasis is **falsification-anchored binary acceptance**: every one of the four tests carries at least one negative/tripwire criterion (sweep-can-still-find-a-token, no-field-leak-beyond-the-7, no-live-`--fix`-outside-a-prohibition, no-backend-token-in-the-freeze-block) so a PASS is positive proof rather than absence of evidence, and every criterion is reduced to a captured shell exit code so three independent subagent runs are forced to agree under a **strict 12/12** verdict (any split is treated as audit-invalidating INDETERMINATE, not majority-voted away). The audit trail is re-derivation-free: each run-artifact embeds the literal command + stdout + exit code behind every criterion, so a human confirms the migration by trusting-or-re-running one command per claim, never by re-tracing the protocol.
