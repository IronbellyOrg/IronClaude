# F-22 Adjudication: `EXEMPT`/`LIGHT` enforcement tiers not recognized by PRD `_evaluate_gate`

**Mode**: B (analyzer / refactorer / architect)
**Source finding**: `.dev/eval-workspaces/prd-cli-audit/findings/F-22-exempt-light-enforcement-not-recognized.md`

---

## Re-verification (read-only, cited)

### 1. `enforcement_tier` declarations of EXEMPT/LIGHT

Four entries in `GATE_CRITERIA` declare a non-STRICT/non-STANDARD tier (`src/superclaude/cli/prd/gates.py`):

| Step | Line | Tier | `min_lines` | `semantic_checks` |
|---|---|---|---|---|
| `check-existing` | `gates.py:300` | `EXEMPT` | (entry not shown in 300-504 window; declared above 300, with `min_lines=0` per finding) | none |
| `template-triage` | `gates.py:356` | `EXEMPT` | `0` (`gates.py:355`) | none |
| `preparation` | `gates.py:404` | `LIGHT` | `0` (`gates.py:403`) | none |
| `present-complete` | `gates.py:504` | `LIGHT` | `0` (`gates.py:503`) | none |

All four declare empty `required_frontmatter_fields=[]` and no `semantic_checks`. Consequence: under today's configuration, `_evaluate_gate` returns `True` for all four because both check blocks short-circuit (`executor.py:596` requires `min_lines > 0`; `executor.py:612` requires `semantic_checks` to be truthy). The label is decorative *today* but functionally a no-op.

### 2. Executor only branches on `STRICT`

`src/superclaude/cli/prd/executor.py:531-540`:

```python
if gate and status.is_success:
    gate_passed = self._evaluate_gate(step_id, gate, gate_content)
    if not gate_passed:
        if gate.enforcement_tier == "STRICT":
            status = PrdStepStatus.HALT
        else:
            status = PrdStepStatus.VALIDATION_FAIL
```

Confirmed via `grep -n "EXEMPT\|LIGHT" src/superclaude/cli/prd/executor.py` returning zero hits. The PRD executor recognizes exactly one tier name (`STRICT`); every other value — `EXEMPT`, `LIGHT`, `STANDARD`, or any typo — falls through the `else` branch and converts a gate-evaluator `False` into `PrdStepStatus.VALIDATION_FAIL`.

### 3. EXEMPT gates still run min_lines + semantic checks

Confirmed. `_evaluate_gate` (`executor.py:587-624`) does not look at `gate.enforcement_tier` at all. It unconditionally:

1. Runs `min_lines` if `gate.min_lines > 0` (`executor.py:596-609`).
2. Iterates `gate.semantic_checks` if non-empty (`executor.py:612-621`).

There is no "EXEMPT → return True" early-exit, no "LIGHT → file-exists-only" branch. This contrasts directly with the generic `src/superclaude/cli/pipeline/gates.py:28-65`, whose docstring (`pipeline/gates.py:4-7`) documents the intended ladder — `EXEMPT` always passes, `LIGHT` file-exists+non-empty, `STANDARD` adds line count and frontmatter, `STRICT` adds semantic checks — and whose body honors it (`pipeline/gates.py:29-65`).

### 4. Downstream impact of `VALIDATION_FAIL` for non-STRICT tiers

`PrdStepStatus.VALIDATION_FAIL` is in both `is_failure` and `is_terminal` sets (`src/superclaude/cli/prd/models.py:132, 152`). What that means concretely on the PRD path:

- **Stage A loop** (`executor.py:381-389`) only halts when `is_failure` *and* `gate.enforcement_tier == "STRICT"`. So an EXEMPT/LIGHT step that fails the bespoke evaluator does *not* halt Stage A; the loop continues to the next step.
- **Diagnostics** classify `VALIDATION_FAIL` as `PrdFailureCategory.GATE_FAIL` (`diagnostics.py:163-164`). The step appears as a hard failure in reports.
- **TUI** renders it as `[red]GATE FAIL[/]` (`tui.py:59`).
- **Stage B/post-loop gates** (e.g. `assembly` at `executor.py:684-687`) explicitly halt on `is_failure` for STRICT — but the wider question, "should a LIGHT/EXEMPT failure ever surface as `GATE_FAIL`?", is answered "no" by the documented contract.

Net: the finding's reproduction sketch ("step ... surfaces as a pipeline failure") slightly overstates the today-blast-radius — the run does *continue* past a LIGHT/EXEMPT failure in Stage A — but the artifact and report carry a `GATE_FAIL`/`VALIDATION_FAIL` stamp that the declared contract says should never appear for those tiers. The semantic violation stands; the operational severity is one notch below "halts the run."

### 5. Cross-reference with F-08

F-08 (adjudicated UPHELD, HIGH) and F-22 share a root cause. `GateCriteria` (`pipeline/models.py:67-82`) declares four fields and the PRD bespoke evaluator (`executor.py:587-624`) honors only two of them:

| `GateCriteria` field | PRD `_evaluate_gate` honors? | Finding |
|---|---|---|
| `required_frontmatter_fields` | No | **F-08** |
| `min_lines` | Yes | — |
| `enforcement_tier` | Partial (only `STRICT` branched on; `EXEMPT`/`LIGHT` ignored) | **F-22** |
| `semantic_checks` | Yes | — |

F-08's recommended fix (delegate to `pipeline.gates.gate_passed()`) co-fixes F-22 in the same diff. The two findings should be bundled.

---

## Persona analysis

### Analyzer (reproducibility)

**What does the executor do for an EXEMPT gate?**

Today: it runs `min_lines` (skipped because `min_lines=0`) and `semantic_checks` (skipped because list is empty), returns `True`, and the gate passes incidentally. Not because EXEMPT is recognized — because the two enforced fields happen to be inert.

Tomorrow, if any contributor adds even a single semantic check to `check-existing`, `template-triage`, `preparation`, or `present-complete` — or sets `min_lines` non-zero — the gate begins to enforce as STANDARD/STRICT-equivalent. The "EXEMPT" label gives no protection. Worse: a contributor reading `enforcement_tier="EXEMPT"` would reasonably believe they could add a check freely as documentation, only to discover it now blocks the pipeline.

**Reproduction (deterministic).** Add `min_lines=10` to the `preparation` entry (`gates.py:401-405`). Run a heavyweight PRD pipeline. The step produces 5 lines of output. `_evaluate_gate` returns `False`. `executor.py:534` checks tier — not "STRICT" — falls through to `executor.py:537`, sets status to `VALIDATION_FAIL`. Diagnostics record `GATE_FAIL`. TUI renders `GATE FAIL` red. The Stage A loop continues (the LIGHT tier saves us from `outcome = "halt"`), but the artifact is stamped failed in every report. The declared contract for LIGHT — "report-only" per `pipeline/gates.py:5` — is violated.

**Caveat the finding undersells.** The finding says "surfaces as a pipeline failure." More precisely: surfaces as a step-level failure that does not halt the run today (because the loop at `executor.py:381-389` only halts on STRICT). The user-visible symptom is therefore "report says LIGHT step failed even though I declared it informational," not "pipeline aborted." This is a narrower defect than the finding implies, and a hair lighter than F-08 in operational consequence.

**Reproducibility score.** Mechanical and deterministic; no timing or environment dependence. Confidence 0.95.

### Refactorer (blast radius)

**Same shape as F-08?** Yes — these are two manifestations of one defect class: the PRD pipeline maintains a bespoke `_evaluate_gate` (`executor.py:587-624`) that has drifted from the shared `GateCriteria` dataclass (`pipeline/models.py:67-82`) and the shared `pipeline.gates.gate_passed()` (`pipeline/gates.py:20-65`). Of four dataclass fields, two are honored, one is partial, one is ignored.

**Bundle recommendation.** Yes, bundle with F-08. Single co-fix: replace the body of `_evaluate_gate` with a delegation to `pipeline.gates.gate_passed()`, retaining the PRD-specific diagnostics/logging wiring (`_diagnostics.record_gate_failure`, `_logger.log_gate_result`). Estimated diff: ~30 lines, one function, one file. The roadmap path (`roadmap/validate_gates.py:12`) already imports the generic helper, proving its viability.

**Future-proofing.** Bundling closes both findings *and* prevents the same drift recurring whenever a new field is added to `GateCriteria`. Without the delegation refactor, a future field addition (say, `max_lines`) will silently no-op on the PRD path until someone files F-NN.

**Blast surface of F-22 alone (without F-08).** Bounded: four entries (`check-existing`, `template-triage`, `preparation`, `present-complete`) — 4/18 of the PRD gate table. Operational impact today: nil (all four are inert). Operational impact under any future config change to those four entries: spurious `GATE_FAIL` reports, no Stage A halt, but `assembly`-style post-loop halt logic *would* fire if a non-STRICT tier got `is_failure` and the halt check inspected only `is_failure` (which `executor.py:684-687` does — though `assembly` itself is STRICT, so the immediate risk is narrow). Any future post-loop halt block written by analogy could be more permissive.

**Refactor risk.** Low. The generic helper is already exercised on roadmap and sprint paths. The behavior change is "EXEMPT/LIGHT now correctly short-circuit" — a strict relaxation, not a tightening — which means the refactor cannot introduce new false-positive failures relative to today's behavior. (It may surface latent contract drift in tests that assert today's incorrect behavior; check `tests/cli/prd/` for fixtures.)

### Architect (severity calibration)

**Preliminary severity: MEDIUM.** Argument for keeping MEDIUM:

1. **No live symptom today.** All four EXEMPT/LIGHT entries are inert (`min_lines=0`, no `semantic_checks`). The defect is armed for future config edits, not exploding now. Per the F-08 architect calibration's framing: "live today" vs "armed for later" — F-22 is the latter.
2. **Stage A continuation.** Even when armed and triggered, the bug produces a misclassified step report rather than a halted pipeline. The loop at `executor.py:381-389` saves us by halting only on STRICT.
3. **Bounded surface.** 4 of 18 gate entries are affected, all in inert configuration.

**Counter-arguments to bump higher (and why MEDIUM still holds):**

- *Defense-in-depth gap.* True — the relaxation contract documented in `pipeline/gates.py:4-7` is silently not delivered on the PRD path. But this is a P7 (architectural-contract) gap, not an active-corruption gap. Severity for unenforced relaxation contracts is meaningfully lower than unenforced *strengthening* contracts (F-08, where missing frontmatter would ship malformed artifacts to humans).
- *Surface area equal to F-08.* Comparable count of affected gates, but the *kind* of failure differs: F-08 lets bad artifacts through; F-22 lets falsely-flagged "failures" through on inert gates that don't have anything to evaluate today.
- *Risk of contributor confusion.* Real — a future contributor adding a check to `preparation` would mis-predict the outcome. Mitigation: same refactor closes it.

**Calibration vs F-08.** F-08 is HIGH because (a) failure manifests immediately for any artifact missing a declared field, no config change needed, and (b) `assembly` has no semantic-check overlap to mask the gap — bad artifacts ship today. F-22 is MEDIUM because (a) failure requires a future config edit to manifest, and (b) even when it does, the operational consequence is a misclassified report rather than a shipped bad artifact.

**Final calibrated severity: MEDIUM.** No change from preliminary. The qualifier: if the F-08/F-22 bundle is *not* fixed together, F-22 should be re-evaluated upward when (not if) someone adds a check to one of the four entries.

---

## Convergence

| Field | Value |
|---|---|
| **Verdict** | UPHELD — finding is accurate; mechanism verified at file:line. The "surfaces as a pipeline failure" phrasing is slightly stronger than today's actual behavior (Stage A continues; only reports/diagnostics are stamped failed), but the underlying contract violation is real and mechanically reproducible. |
| **Convergence score** | 0.92 — all three personas agree the defect is real, reproducible, structurally identical to F-08, and bundle-fixable. Minor calibration disagreement on whether to nudge severity slightly downward from MEDIUM given the inert-today posture; architect retains MEDIUM on contributor-confusion / contract-violation grounds. |
| **Final severity** | **MEDIUM** (unchanged from Stage 2 preliminary). |
| **Fix difficulty** | **LOW** — co-fix with F-08. Replace `_evaluate_gate` body (`executor.py:587-624`) with a delegation to `pipeline.gates.gate_passed()`, preserving the diagnostics/logging wiring. Estimated effort: 30-60 lines, one function, plus test updates for any fixture that asserts today's incorrect behavior. |
| **Recommended fix** | Bundle with F-08. Single delegation refactor closes both. Add explicit regression tests: (a) `preparation` with `min_lines=10` and 5-line output → gate passes (LIGHT relaxation honored); (b) `check-existing` with `min_lines=10` and 0-line output → gate passes (EXEMPT honored); (c) `parse-request` (STRICT) with empty content → gate still halts. |

### Synthesis

F-22 is a real but latent defect: `prd/gates.py` declares `enforcement_tier="EXEMPT"` (twice) and `"LIGHT"` (twice), but `prd/executor.py:_evaluate_gate` (`executor.py:587-624`) ignores the tier and the dispatcher block at `executor.py:531-540` only branches on `"STRICT"`. Every non-STRICT tier name falls through the `else` and converts a failed evaluator into `PrdStepStatus.VALIDATION_FAIL`, which is `is_terminal`/`is_failure`. The shared `pipeline/gates.py:28-65` documents and implements the intended ladder (EXEMPT always passes, LIGHT file-exists+non-empty, etc.); the PRD bespoke evaluator silently does not.

Operationally, the bug is dormant today because all four EXEMPT/LIGHT entries declare `min_lines=0` and no `semantic_checks` — the two fields `_evaluate_gate` actually consults are both inert. Any future contributor adding even one check to those entries arms the bug: the gate now enforces as if STRICT-without-halt, surfacing as a misclassified `GATE_FAIL` in reports and diagnostics even though Stage A continues past it (the STRICT-only halt check at `executor.py:381-389` rescues the run from full abort).

F-22 is structurally identical to F-08: both stem from the PRD pipeline maintaining a separate evaluator that has drifted from the shared `GateCriteria` dataclass. Of four dataclass fields, the PRD evaluator honors two fully (`min_lines`, `semantic_checks`), one partially (`enforcement_tier` — only `STRICT` branched on), and one not at all (`required_frontmatter_fields` — F-08). Recommended remediation is to converge the PRD evaluator onto `pipeline.gates.gate_passed()`, closing F-08 and F-22 in one diff and pre-empting future drift.

Severity stays MEDIUM (one notch below F-08's HIGH) because (a) no live symptom today — all affected entries are inert; (b) when armed by future config, the operational impact is misclassified reports rather than shipped bad artifacts; (c) the failure mode is relaxation-not-honored, not strengthening-not-enforced. The defect is worth fixing primarily because it is free to fix alongside F-08, and the architectural pattern (bespoke evaluator silently dropping contract fields) is itself a latent risk multiplier.

---

## Evidence ledger

- `src/superclaude/cli/prd/gates.py:300` — `check-existing`, `enforcement_tier="EXEMPT"`.
- `src/superclaude/cli/prd/gates.py:356` — `template-triage`, `enforcement_tier="EXEMPT"` (entry at `gates.py:353-357`, `min_lines=0`).
- `src/superclaude/cli/prd/gates.py:404` — `preparation`, `enforcement_tier="LIGHT"` (entry at `gates.py:401-405`, `min_lines=0`).
- `src/superclaude/cli/prd/gates.py:504` — `present-complete`, `enforcement_tier="LIGHT"` (entry at `gates.py:501-505`, `min_lines=0`).
- `src/superclaude/cli/prd/executor.py:531-540` — gate dispatcher; branches only on `"STRICT"`, all other tiers fall to `VALIDATION_FAIL`.
- `src/superclaude/cli/prd/executor.py:587-624` — `_evaluate_gate` body; reads only `gate.min_lines` and `gate.semantic_checks`, never `enforcement_tier`.
- `src/superclaude/cli/prd/executor.py:381-389` — Stage A loop halt; halts only on `is_failure` *and* `enforcement_tier == "STRICT"`. Non-STRICT failures continue the loop.
- `src/superclaude/cli/prd/models.py:99-153` — `PrdStepStatus`; `VALIDATION_FAIL` is in `is_terminal` and `is_failure`.
- `src/superclaude/cli/prd/diagnostics.py:163-164` — `VALIDATION_FAIL` → `PrdFailureCategory.GATE_FAIL` classification.
- `src/superclaude/cli/prd/tui.py:59` — `VALIDATION_FAIL` rendered as `[red]GATE FAIL[/]`.
- `src/superclaude/cli/pipeline/gates.py:4-7, 28-65` — documented enforcement ladder and its correct implementation (EXEMPT/LIGHT/STANDARD/STRICT honored).
- `src/superclaude/cli/pipeline/models.py:67-82` — shared `GateCriteria` dataclass; four fields.
- `src/superclaude/cli/roadmap/validate_gates.py:12` — sibling path that imports the generic helper.
- `.dev/eval-workspaces/prd-cli-audit/adjudications/F-08/adjudication.md` — UPHELD/HIGH adjudication of the paired finding; recommends the same delegation refactor that co-fixes F-22.
- Grep: `grep -n "EXEMPT\|LIGHT" src/superclaude/cli/prd/executor.py` returns zero matches.
