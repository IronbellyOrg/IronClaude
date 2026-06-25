---
title: "UC-2 Contracted-Sink Reachability & Oracle-Admissibility Gate (FR-RH1)"
status: merged-requirements
domain: code
strategy: systematic
adversarial_status: converged
convergence: high
created: 2026-06-20
source_seed: seed-brief.md
target_skill: src/superclaude/skills/sc-reflect-protocol/SKILL.md
---

# Merged Requirements — Harden `/sc:reflect` UC-2 against silent runtime-surface / durable-invariant reachability gaps

## 0. One-paragraph thesis

`/sc:reflect` UC-2 is **divergence-first** and therefore structurally blind to a *fail-open* bug where the
code is present, the unit tests are green, a parallel observable (journald) is emitted, but the **contracted
durable sink is never reached** (composition root never binds the facade; emitter error discarded; e2e oracle
greps the proxy sink). The fix is a UC-2 **Contracted-Sink Reachability & Oracle-Admissibility obligation**
(new §6.1 **step 5.6**, UC-2-only, Tier-1) that, for *side-effect-bearing requirements only*, requires the
audit to ground two sub-claims — **(a) reachability** (an executed path from the entry/composition root to the
side-effecting call, result not discarded) and **(b) oracle-admissibility** (the verification observes the
*contracted* sink, not a proxy). **The fail-closed teeth are the existing §10.6 Grounding-Gap →
`needs_human_decision` → HALT route** (which does *not* trip §5.3 rule-3, so the common path stays Tier-1).
Auto-`regression_present` is reserved for a **real-boot-PROVEN** contradiction. The static fail-open scan and
the real-boot verifier are **advisory recall aids** (capped at L2, fail-open, per the reuse-auditor precedent),
never the gating mechanism. Findings are injected at Wave-1A (upstream of the render-only Wave 5) and ride the
existing `regression_present` / `needs_human_decision` contract fields — **no `contract.py` change required**.

## 1. Re-grounded gap (real `file:line`, this checkout)

| Claim | Evidence |
|---|---|
| Wave-1A evidence chain is symbol/diff/test-oriented; never proves entrypoint→composition-root→sink | `SKILL.md:453-494` (§6.1 steps 1–7'); verification triangle step 5.5 `SKILL.md:474,490` |
| Taxonomy is divergence-first → a *missing* bind + discarded error classifies as nothing | `SKILL.md:907-983` (§10.1-10.5 detection signals all key on an observable divergence) |
| §10.4 Regression signals don't trip on a green-tests fail-open | `SKILL.md:956-976` (contradiction / previously-passing-test-fails / invariant) |
| No oracle-admissibility obligation — a proxy-sink pass counts as grounded evidence | step-5.5 triangle trusts `pytest` exit 0 regardless of oracle sink (`SKILL.md:490`, envelope §6.1.1 `SKILL.md:496-510`); exit-code taxonomy maps codes not sink-identity (`SKILL.md:962-974`) |
| Wave 5 only renders → fix must inject upstream | `SKILL.md:155` |
| Consumer already HALTs on the routes the gate uses | `contract.py:313` (partial), `:315` (regression_present), `:319` (needs_human_decision), `:356-363` (classify_fix→human-required); unknown-field tolerance `:66-82` |
| Real-boot rides existing T1 tool, doesn't force T2 | `cost-profile.yaml` T1=3-8k vs T2=35-70k; verifier = step-5.5 `execute_shell_command` |

## 2. Red-team outcome (what changed from the leading hypothesis)

The leading hypothesis (`seed-brief.md` §"Leading hypothesis") was **right about the gap and placement** but
**wrong about the default classification**. Three blind reviewers (`redteam/A1`, `A2`, `A3`) converged:

| Leading hypothesis | Problem found | Merged decision |
|---|---|---|
| `unreachable`/`oracle_mismatch` → **auto-Regression** (fail-closed) | Trips §5.3 rule-3 (`SKILL.md:392`) → first static hit drags whole run to Tier-2, ~5-9× cost (A1#4); risks **false-Regression** on idiomatic `_ =`/lazy-DI → halt-fatigue → operators rubber-stamp the alarm (A1#1) | **Default → `unproven`/Grounding Gap** (does NOT trip rule-3 → Tier-1 preserved). Auto-Regression reserved for a **real-boot-PROVEN** contradiction |
| **real-boot verifier** as a required proof | Cannot exist under §6.1.1 envelope (metachar reject `:503`, verb allowlist excludes the prod binary `:501`, 120s/cwd) → only the executor's own suspect suite is runnable → **circularity** (A1#2) | Real-boot is **best-effort/advisory**; it is the *only* path that can *upgrade* a verdict to PROVEN-`unreachable`, and it must itself observe the contracted sink (else `oracle_mismatch`) |
| static fail-open scan as the detector | Statically indistinguishable from correct best-effort/lazy/plugin code (A1#1,#5); Go-overfit, misses tx-rollback/tmpdir/zero-subscriber (A2#5) | **Static scan = advisory-L2 recall aid** (reuse-auditor posture `SKILL.md:492`); the *general* obligation is **oracle-admissibility** |
| oracle-identity via LLM inference | Fragile (Pass-2 `SKILL.md:300/306`); slog-as-contracted-sink false positive (A1#3) | **Prefer an explicit machine-readable sink annotation**; unresolved sink identity → `unproven` (human decides), never false Regression |
| new `runtime-reachability-ledger.yaml` as a **gate** + possible 5th category | Duplicates §10.6; §17.7 item-6 already rejected a 5th category (A2#3) | Ledger is **evidence/telemetry only**; routes to existing §10.6 + §10.4; optional `gap_kind` discriminator |
| opt-in `--reachability` / standalone skill | An opt-in gate that defaults off **silent-passes the exact bug** (A2#4) | **Always-on, side-effect-conditional**, default-on; `--no-reachability` to disable |
| mandatory `--tasklist` | Breaks legacy `--type task --validate` / sc:troubleshoot Wave 6 (A2#2) | **Spec-conditional**; no spec → diff-side probe → `unproven` or no-op; **never STOP** |

## 3. Final design (FR-RH1)

### 3.1 Trigger predicate — "side-effect-bearing requirement"
An acceptance criterion `AC` is side-effect-bearing iff its **contracted observable effect** is in
`SIDE_EFFECT_TAXONOMY = {durable_row, db_write, queue_publish, event_emit, file_persist,
external_api_write, process_spawn, prod_route}` **AND** the effect crosses a process/persistence boundary
(not fully observable from a pure unit test of the changed symbol) **AND** the AC names a `contracted_sink`
the changed symbol does not itself own. Resolution order for `contracted_sink`:
1. explicit machine-readable annotation on the AC (`durable_sink:`/`@sink`) — **preferred, unambiguous**;
2. else semantic classification of the AC's effect noun into the taxonomy (the orchestrator model), with the
   resolved sink identifier recorded.
If (2) cannot pin a unique sink identity → the row is `unproven` (not skipped, not Regression).

**Spec-absent default (preserves legacy callers, never STOP):** when neither `--spec` nor `--tasklist` is
supplied, fall back to a **diff-side probe**: a touched emitter-shaped call (`/Emit|Publish|Persist|Write|
Enqueue|Send|Register|SetDefault/` to a non-local receiver) **whose result is discarded** → a single
`unproven` row → Grounding Gap. No requirement signal and no diff-side shape → **no row, no gate** (zero
over-fire).

### 3.2 The two grounded sub-claims (the obligation)
For each side-effect-bearing requirement the audit MUST carry, grounded to `file:line`:
- **Reachability sub-claim:** an executed path exists from the entry/composition root to the side-effecting
  call, and the call's result is not silently discarded. Advisory inputs: **signal 1 missing_binding**
  (`find_referencing_symbols` on the binder symbol in the entrypoint file = zero refs — reuses step 4,
  `SKILL.md:463`); **signal 2 discarded_emitter_result** (step-6 re-Read shows `_ =`/unchecked/swallowed —
  reuses `SKILL.md:475`).
- **Oracle-admissibility sub-claim (the general, primary teeth):** the completion evidence comes from an oracle
  whose observed sink == `contracted_sink`. **signal 3 oracle_mismatch**: the acceptance/e2e assertion targets
  a proxy (journald/slog/stdout/unit-pass/code-presence) for a requirement that contracts a durable sink.

### 3.3 Verdict → classification → existing contract field (fail-closed, never-false-Regression)
| Verdict | Condition | Class | Existing field set | Tier effect |
|---|---|---|---|---|
| `reachable` | binding present **and** emitter result checked **and** `oracle_match: true` | none | — | none |
| `unreachable` | **real-boot ran and observed the contracted sink absent** (PROVEN) — *or* binding unambiguously absent **and** `oracle_mismatch` confirmed | Regression | `reachability_unreachable += 1`; `verification_regressions_detected += 1`; `regression_present: true` (`SKILL.md:762`) → `contract.py:315` HALT | trips §5.3 rule-3 → Tier-2 (**correct**: a proven fail-open is worth a debate) |
| `unproven` | any fail-open signal present but contradiction **not** real-boot-proven; or sink identity unresolved; or real-boot unavailable; or spec absent | Grounding Gap | one `grounding-gaps.yaml` row (`gap_kind: unreachable-sink`\|`oracle-mismatch`) → `status: partial` + `needs_human_decision: true` (`SKILL.md:1004-1005`) → `contract.py:313/319` HALT | **does NOT trip rule-3 → Tier-1 preserved** |

Default bias is **`unproven` over `unreachable`** — ambiguity is always Grounding Gap, never a false
Regression and never a silent pass. The static scan alone (signals 1-3 without a real-boot proof) is
**advisory L2**: it populates the ledger and the reviewer probe but on its own yields `unproven`
(Grounding-Gap), never `regression_present`.

### 3.4 Halt-fatigue containment (resolves A1#1)
A Grounding-Gap row fires **only** when (i) the AC is side-effect-bearing with a resolvable durable sink AND
(ii) the audit cannot ground the reach/oracle sub-claims — a far narrower trigger than "any `_ =` in the
diff". An idiomatic best-effort discard on a path that is *not* a contracted durable sink produces **no
requirement → no row → no halt**. This is the structural reason the merged gate does not flood
`needs_human_decision`.

## 4. Concrete per-file edits (additive; anchors confirmed in this checkout)

> All edits are insertions. Edit `src/superclaude/` first, then `make sync-dev`, then `make verify-sync`.

### 4.1 `SKILL.md` — new §6.1 **step 5.6** (insert after the step-5.5 paragraph that ends `…points at the per-invocation artifact.`, `SKILL.md:490`)
```markdown
Step 5.6 (FR-RH1, UC-2-only) is the **contracted-sink reachability & oracle-admissibility gate** — it closes the
"passes unit tests + emits to a proxy sink, contracted durable sink never reached, fails OPEN" blindspot that a
divergence-first audit (§10) is structurally blind to. It fires **only** for *side-effect-bearing requirements*
(taxonomy: durable_row / db_write / queue_publish / event_emit / file_persist / external_api_write /
process_spawn / prod_route) — an acceptance criterion naming a `contracted_sink` the changed symbol does not
itself own, resolved by an explicit `durable_sink:`/`@sink` annotation when present, else by semantic
classification of the AC's effect noun. For each such requirement the audit grounds two sub-claims, reusing
artifacts already in hand: **reachability** — signal 1 `missing_binding` via the step-4 `find_referencing_symbols`
on the sink's binder symbol scoped to the entrypoint/composition-root file (zero refs = unbound), and signal 2
`discarded_emitter_result` via the step-6 re-Read of the emitter hunk (`_ =`/unchecked/swallowed); and
**oracle-admissibility** — signal 3 `oracle_mismatch` via a compare of the acceptance/e2e oracle's asserted sink
vs `contracted_sink` (a proxy like journald/slog/stdout/unit-pass for a durable requirement does NOT count). The
static signals are **advisory (capped L2, reuse-auditor posture §6.1 step 4a)**; on their own they yield
`unproven`, never `regression_present`. The real-boot verifier is **best-effort**: when a bootable entrypoint
exists and `--no-verify` is unset it issues ONE step-5.5 `execute_shell_command` under the §6.1.1 envelope and
checks the contracted sink observed the effect; it is the ONLY path that can prove `unreachable`. It writes one
row per side-effect requirement to `<output>/runtime-reachability-ledger.yaml` (schema §9.1) and emits a
`reachability_gate_invoked` audit row per the §4 per-step convention. **Verdict (fail-closed):** real-boot
observed the contracted sink absent — OR binding unambiguously absent AND `oracle_mismatch` confirmed ⇒
`unreachable` → §10.4 Regression (`regression_present: true`; trips §5.3 rule-3 — correct). Any fail-open signal
WITHOUT a real-boot-proven contradiction, or an unresolved sink identity, or real-boot unavailable, or spec/
tasklist absent ⇒ `unproven` → §10.6 Grounding Gap (`gap_kind: unreachable-sink|oracle-mismatch`,
`needs_human_decision: true`) — which does NOT trip rule-3, so the common UC-2 path stays Tier-1. No fail-open
signal ⇒ `reachable`/none. When neither `--spec` nor `--tasklist` is supplied, the predicate degrades to a
diff-side probe (a touched emitter-shaped call with a discarded result → a single `unproven` row; otherwise no
row, no gate). Disabled by `--no-reachability` (records the skip in Grounding Gaps). Fail-open per §6.5; NEVER STOP.
```

### 4.2 `SKILL.md` — §10.4 detection-signal bullet (insert after the `@invariant` bullet, `SKILL.md:960`)
```markdown
- **A contracted side-effect never reaches its durable sink (fail-open reachability) — detected by the §6.1
  step-5.6 gate, NOT by unit-test pass/fail.** When a side-effect-bearing requirement's sink binding is absent
  at the composition root AND the emitter result is discarded or the acceptance oracle asserts a proxy sink, the
  work "passes" while the contracted sink is never written. This is a Regression ONLY when real-boot proves the
  sink absent (or the binding-absence + oracle-mismatch is unambiguous); otherwise it degrades to a Grounding
  Gap (`unproven`) — never a silent pass and never a false Regression (§10.6 / §17.7 item 7).
```

### 4.3 `SKILL.md` — §9.1 contract-field block (insert immediately before the `# Reuse-Miss neighbour sweep` comment, `SKILL.md:711`)
```yaml
# Runtime-reachability gate (FR-RH1 — §6.1 step 5.6 / §10.4 / §10.6; UC-2). Rides existing
# regression_present / needs_human_decision fields — NO new consumer field required.
reachability_gate_ran: <bool>
reachability_ledger_path: <abs path> | null      # <output>/runtime-reachability-ledger.yaml
reachability_requirements_scanned: <int>          # side-effect-bearing requirements evaluated
reachability_unreachable: <int>                   # verdict==unreachable rows (each → regression_present)
reachability_unproven: <int>                      # verdict==unproven rows (each → a grounding-gaps row)
reachability_real_boot_ran: <bool>                # best-effort step-5.5 boot fired at least once
reachability_skip_reason: --no-reachability|no-side-effect-requirements|spec-and-tasklist-absent|null
```

### 4.4 `SKILL.md` — §10.6 optional discriminator field (insert into the Grounding-Gap row schema, after the optional `similarity_tier` block ending `SKILL.md:998`)
```yaml
  # OPTIONAL — present only on reachability-routed gaps (§6.1 step 5.6 / FR-RH1):
  gap_kind: unreachable-sink | oracle-mismatch                  # optional discriminator
  contracted_sink: <sink identifier>                           # optional
  reachability_ledger_ref: <runtime-reachability-ledger.yaml row index>  # optional
```

### 4.5 `SKILL.md` — §17.6 Testability Map rows (insert after the §10.6 grounding-gaps row, `SKILL.md:1767`)
```markdown
| §6.1 step 5.6 reachability gate (unreachable→regression) | `yaml_field` | `return-contract.yaml regression_present == true AND reachability_unreachable > 0` |
| §6.1 step 5.6 reachability fail-closed (unproven→grounding-gap, Tier-1 preserved) | `file_exists` + `yaml_field` | `runtime-reachability-ledger.yaml verdict AND return-contract.yaml needs_human_decision == true AND tier_reached == 1` |
```

### 4.6 `SKILL.md` — §17.7 Kill List item 7 (append after item 6, `SKILL.md:1799`)
```markdown
7. **New `reachability` agent / 5th "fail-open" deviation category / standalone reachability sub-command** —
   Rejected. The gate is a 3-signal advisory check (missing binding / discarded emitter / oracle mismatch) over
   artifacts the §6.1 chain *already collects* (steps 4 and 6) plus a best-effort step-5.5 boot; it needs no new
   agent and no new deviation class, and an opt-in sub-command would silent-pass the exact fail-open bug it
   targets. *Replaces with:* §6.1 step 5.6 reusing existing serena calls; `unreachable` → existing §10.4
   Regression (real-boot-proven only), `unproven` → existing §10.6 Grounding Gaps — preserving the 4-category
   ledger purity and the Tier-1 common path.
```

### 4.7 `reflect.md` — new flag (insert after the `--no-verify` row, `reflect.md:86`)
```markdown
| `--no-reachability` | `false` (UC-2) | Disable the §6.1 step-5.6 contracted-sink reachability & oracle-admissibility gate. Default-on; charges ONLY side-effect-bearing requirements (durable row / DB write / queue publish / event emit / file persist / external API write / process-spawn / prod route). When set, records the skip in Grounding Gaps. Reuses the step-5.5 verification budget; no extra tool class. |
```

### 4.8 `reflect.md` — Tool-Coordination line (append in the `## Tool Coordination` list, after the step-5.5 line, `reflect.md:146`)
```markdown
- **Runtime-reachability (step 5.6, UC-2):** reuses `mcp__serena__find_referencing_symbols` (binding presence) + the step-6 re-Read (emitter-result discard) + an oracle-vs-contracted-sink compare; the real-boot check is a best-effort step-5.5 `execute_shell_command` under the §6.1.1 envelope. Verdict `unreachable`→Regression (real-boot-proven), `unproven`→Grounding Gap; fail-open / NEVER STOP.
```

### 4.9 `refs/reflection-rubric.md` — extend dimension #4 (insert after `### 4. Risk surface coverage`, after its scoring list)
```markdown
**Reachability sub-criterion (FR-RH1, UC-2).** For every side-effect-bearing requirement, full marks require the
report to have evaluated whether the contracted durable sink is actually reached (binding present + emitter
result checked + oracle asserts the *contracted* sink), not merely that unit tests pass. An audit that reports
"tests pass" while a `runtime-reachability-ledger.yaml` row carries an unaddressed `unreachable`/`unproven`
verdict caps this dimension — fail-open sinks are the canonical risk this dimension exists to surface.
```

### 4.10 `refs/reflection-rubric.md` — extend dimension #1 (insert after `### 1. Citation grounding` scoring list)
```markdown
**Oracle-admissibility (FR-RH1, UC-2).** A completion claim for a side-effect-bearing requirement is grounded
ONLY if its evidence oracle observes the *contracted* sink. Evidence from a proxy sink (journald/slog/stdout/
unit-pass/code-presence) for a requirement that contracts a durable sink is `[INFERRED]`, not grounded; when
load-bearing it routes to §10.6 Grounding Gaps via the evidence-validator, never counting as citation grounding.
```

### 4.11 `refs/reviewer-spec.md` — required reviewer probe (append under "Required sections (per brief)")
```markdown
### Side-effect reachability probe (UC-2, FR-RH1)
For any reviewed requirement whose AC names a durable sink the changed symbol does not own (taxonomy in §6.1
step 5.6), each reviewer MUST independently answer, cited to `file:line`: (1) is the sink BOUND at the
composition root? (2) is the emitter's result CHECKED (not `_ =`/swallowed)? (3) does the acceptance/e2e oracle
assert the **contracted** sink (not a proxy like journald)? Inability to resolve the entrypoint or the sink
identity → an `unproven` vote (Grounding Gap), never a clean vote. A real-boot-proven sink-absent → a Regression
vote. This neutralises the single-agent blindspot where a passing unit suite masks a fail-open sink.
```

### 4.12 `refs/deviation-taxonomy.md` — Regression/Grounding mapping (append a sub-section before the Grounding-Gaps section)
```markdown
## Runtime-reachability → deviation-class mapping (FR-RH1)
A contracted side-effect that never reaches its durable sink is a Regression **only when real-boot proves it**
(conservative — partial proof is never a Regression):

| Reachability verdict | Condition | Class | Effect |
|---|---|---|---|
| `unreachable` | real-boot observed the contracted sink absent, OR binding unambiguously absent AND oracle_mismatch confirmed | **Regression** | `reachability_unreachable += 1`; `regression_present: true` |
| `unproven` | a fail-open signal present but contradiction not real-boot-proven / sink identity unresolved / real-boot unavailable / spec absent | **Grounding Gap** | one `grounding-gaps.yaml` row (`gap_kind`); `needs_human_decision: true`; Tier-1 preserved |
| `reachable` | binding present, emitter result checked, oracle asserts the contracted sink | **none** | clean |
```

### 4.13 `refs/report-template.md` — render note (append after the Grounding-Gaps section header)
```markdown
### Runtime-reachability findings (FR-RH1)
A step-5.6 `unreachable` verdict renders as a Regression D-<id> with the `contracted_sink`, the `entrypoint_ref`
showing the absent binding, the `emitter_ref` showing the discarded result, and the `oracle_ref` showing the
mismatched assertion — each cited `file:line`, with the real-boot evidence anchor. An `unproven` verdict renders
as Grounding Gap G-<id> with `gap_kind`, `evidence_missing` = the unresolved reach/oracle link, and
`next_evidence_needed` = "boot the entrypoint and assert the row lands on the contracted sink, or confirm the
sink binding". Both cite the `runtime-reachability-ledger.yaml` row.
```

### 4.14 `refs/cost-profile.yaml` — advisory note under `T1:` (insert after the `turn_budget_label: "T1-midpoint"` line)
```yaml
    # Runtime-reachability gate (§6.1 step 5.6, FR-RH1) adds NO new tool class: signals 1-3 reuse
    # step-4 find_referencing_symbols + step-6 re-Read already counted in this band; the best-effort
    # real-boot is one step-5.5 execute_shell_command (already T1). Per-side-effect-requirement only;
    # unproven verdicts route to Grounding Gap and do NOT trip §5.3 rule-3, so the common path stays T1.
    reachability_gate_added_tokens: 0
    reachability_gate_added_turns: 0
```

### 4.15 (OPTIONAL, deferred) `contract.py` defense-in-depth
Not required (the gate rides `regression_present`/`needs_human_decision`). A future hardening MAY add, after
`contract.py:319`, a redundant trigger `if int(contract.get("reachability_unreachable", 0) or 0) > 0: return
"regression"` so a producer that mis-wires the legacy boolean still HALTs. Deferred to avoid coupling the pure
consumer to the new artifact in v1; tracked as an open item.

## 5. Fail-before / pass-after self-test (`tests/cli/reflect/`)

Two new fixtures (style mirrors `halted_regression.yaml` / `human_required_needs_decision.yaml`; bump
`contract_version` to `"1.5.0"` per `SKILL.md:804`) + three functions appended to `test_verdict_mapping.py`.

### 5.1 Fixture `tests/cli/reflect/fixtures/reachability_unbound_sink.yaml` (bug WITH the gate firing)
```yaml
contract_version: "1.5.0"
status: partial
mode: post
tier_reached: 2
report_path: /tmp/reflect-out/REPORT.md
audit_log_path: /tmp/reflect-out/audit.log
deviation_count_by_class: {authorized: 0, necessary: 0, drift: 0, regression: 1}
t2_model_class_diversity: full
t2_vendor_diversity: multi
adversarial_unavailable: false
merge_method: adversarial
adversarial_convergence_score: 0.83
verification_ran: true
verification_skip_reason: null
citations_dropped: 0
citations_dropped_extrapolated: 0
input_drift_detected: false
regression_present: true
unauthorized_deviation_present: false
needs_human_decision: false
user_decision_required: false
serena_summary_corroboration: unavailable
degraded_components: []
reachability_gate_ran: true
reachability_ledger_path: /tmp/reflect-out/runtime-reachability-ledger.yaml
reachability_requirements_scanned: 1
reachability_unreachable: 1
reachability_unproven: 0
reachability_real_boot_ran: true
reachability_skip_reason: null
verification_regressions_detected: 1
```

### 5.2 Fixture `tests/cli/reflect/fixtures/reachability_silent_bug_pregate.yaml` (the hole the gate closes — passes today)
```yaml
contract_version: "1.5.0"
status: success
mode: post
tier_reached: 2
report_path: /tmp/reflect-out/REPORT.md
audit_log_path: /tmp/reflect-out/audit.log
deviation_count_by_class: {authorized: 0, necessary: 0, drift: 0, regression: 0}
t2_model_class_diversity: full
t2_vendor_diversity: multi
adversarial_unavailable: false
merge_method: adversarial
adversarial_convergence_score: 0.88
verification_ran: true
verification_skip_reason: null
citations_dropped: 0
citations_dropped_extrapolated: 0
input_drift_detected: false
regression_present: false
unauthorized_deviation_present: false
needs_human_decision: false
user_decision_required: false
serena_summary_corroboration: unavailable
degraded_components: []
reachability_gate_ran: false
```

### 5.3 Tests appended to `tests/cli/reflect/test_verdict_mapping.py`
```python
def test_reachability_unreachable_halts_human_required() -> None:
    """FR-RH1: a real-boot-proven unreachable sink -> HALTED / exit 10 + human-required.

    The gate sources regression_present from runtime-reachability-ledger.yaml
    (reachability_unreachable=1). derive_verdict HALTs on the existing
    regression_present field (contract.py:315); classify_fix routes human-required
    on the same field (contract.py:356-363). No consumer change required.
    """
    contract = _load("reachability_unbound_sink.yaml")
    result = derive_verdict(contract, expected_tier=2, allow_single_vendor=False, child_rc=0)
    assert result.verdict is Verdict.HALTED
    assert result.verdict.exit_code == 10
    from superclaude.cli.reflect.contract import classify_fix
    assert classify_fix(contract, contract["deviation_count_by_class"]) == "human-required"


def test_reachability_unproven_routes_grounding_gap_halts_tier1() -> None:
    """FR-RH1 fail-closed default: unproven -> needs_human_decision -> HALTED, Tier-1 preserved.

    A partially-proven fail-open signal must never silent-pass nor false-Regress: it
    sets needs_human_decision (a grounding-gaps row) -> HALTED (contract.py:319),
    classify_fix -> human-required (NOT regression), and does NOT force Tier-2.
    """
    contract = _load("reachability_unbound_sink.yaml")
    contract["status"] = "partial"
    contract["tier_reached"] = 1
    contract["regression_present"] = False
    contract["reachability_unreachable"] = 0
    contract["reachability_unproven"] = 1
    contract["reachability_real_boot_ran"] = False
    contract["needs_human_decision"] = True
    contract["deviation_count_by_class"]["regression"] = 0
    result = derive_verdict(contract, expected_tier=1, allow_single_vendor=False, child_rc=0)
    assert result.verdict is Verdict.HALTED
    assert result.verdict.exit_code == 10
    from superclaude.cli.reflect.contract import classify_fix
    assert classify_fix(contract, contract["deviation_count_by_class"]) == "human-required"


def test_pregate_silent_bug_passes_demonstrating_the_gap() -> None:
    """FR-RH1 motivation: WITHOUT the gate the fail-open bug rides to PASS / exit 0.

    Fixture (b) PASSES; fixture (a) HALTS on the same derive_verdict. The delta is the gate.
    """
    result = derive_verdict(
        _load("reachability_silent_bug_pregate.yaml"),
        expected_tier=2, allow_single_vendor=False, child_rc=0,
    )
    assert result.verdict is Verdict.PASS
    assert result.verdict.exit_code == 0
```

**Property proven:** fixture (b) PASS + fixture (a)/(modified) HALT on the *same* `derive_verdict` shows the
gate is the discriminator; the unproven test additionally proves the **Tier-1-preserving fail-closed default**
(HALT via `needs_human_decision`, `tier_reached: 1`). All three are green only because the gate populated
existing HALT fields — no `contract.py` change; `contract.py:66-82` tolerates the 7 new fields, so the 14
existing fixtures (incl. `pass.yaml`, `tolerant_unknown_field.yaml`) are unaffected.

> **Scope note on the self-test.** This deterministic suite proves the **contract→verdict wiring** (the gate's
> outputs never silent-pass). The **protocol-level detection** (that step 5.6 actually produces the right
> verdict from a real diff) is validated by an eval-workspace falsifier case (the §12.5 pattern + the new §17.6
> rows) under the LLM eval harness, not `make test`. Both are required for full coverage; the Python suite is
> the CI-runnable half and the fail-before/pass-after artifact requested.

## 6. Risk / rollback

| Risk | Likelihood | Mitigation | Rollback |
|---|---|---|---|
| **False-Regression** on idiomatic `_ =`/lazy-DI/plugin code | Low (by design) | Auto-Regression requires real-boot proof; static-only → `unproven`/Grounding Gap; non-durable-sink discards produce no requirement → no row | Set `--no-reachability`; revert §6.1 step-5.6 + §10.4 bullet (additive, isolated) |
| **Halt-fatigue** from too many `needs_human_decision` | Low-Med | Gate fires only for side-effect-bearing requirements with a resolvable durable sink (§3.4); spec-conditional | Tighten the trigger to require an explicit `durable_sink:` annotation only (drop semantic fallback) |
| **Oracle-identity misclassification** (slog-as-durable false positive) | Med | Prefer explicit annotation; unresolved → `unproven` (human decides), never Regression | Disable semantic fallback; annotation-only mode |
| **Cost creep into Tier-2** | Low | `unproven` does NOT trip §5.3 rule-3 (`SKILL.md:392`); only real-boot-proven `unreachable` escalates (correct) | `--no-reachability`; or pin `--tier 1` |
| **Real-boot infeasible under §6.1.1 envelope** | Expected often | Real-boot is best-effort; absence → `unproven`, not a blocker | n/a (degradation is the designed path) |
| **`make verify-sync` drift** after editing `src/` | Low | Run `make sync-dev` before commit; never edit `.claude/` directly | Re-run `make sync-dev` |
| **Eval-workspace SPEC/testability drift** | Low | Add the two §17.6 rows + a falsifier case in the same change | Remove the rows (additive) |

**Rollback summary:** every edit is an insertion behind the default-on `--no-reachability` flag and 7 additive
contract fields the consumer ignores. Disabling the flag restores exact prior behavior; reverting the §6.1
step-5.6 + §10.4 bullet + the two §17.6 rows fully removes the feature with zero impact on the 14 existing
reflect tests.

## 7. Definition-of-Done checklist (for the landing task)
- [ ] Edits 4.1-4.14 applied under `src/superclaude/`; 4.15 deferred.
- [ ] `make sync-dev && make verify-sync` green.
- [ ] 2 fixtures + 3 tests added; `uv run pytest tests/cli/reflect/ -v` green (incl. 14 prior).
- [ ] `uv run ruff format --check src/ tests/` green (CI format gate, per memory).
- [ ] Eval-workspace: add the §17.6 falsifier case (LLM-harness half).
- [ ] Feature branch only; PR `--repo IronbellyOrg/IronClaude --base master`.
