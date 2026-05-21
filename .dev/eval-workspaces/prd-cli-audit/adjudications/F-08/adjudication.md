# F-08 Adjudication: `required_frontmatter_fields` declared but never checked in PRD `_evaluate_gate`

**Mode**: B (analyzer / refactorer / architect)
**Source finding**: `.dev/eval-workspaces/prd-cli-audit/findings/F-08-frontmatter-fields-declared-never-checked.md`

---

## Re-verification (read-only, cited)

### 1. PRD `_evaluate_gate` body — what is actually checked

`src/superclaude/cli/prd/executor.py:587-624` defines the only gate evaluator used by the PRD pipeline. The function checks exactly two attributes of the `gate` argument:

- `gate.min_lines` — line-count floor (`executor.py:596-609`)
- `gate.semantic_checks` — iterable of `SemanticCheck` callables (`executor.py:612-621`)

No other attribute of `gate` is read inside `_evaluate_gate`. A bytewise grep confirms:

```
$ grep -n "required_frontmatter_fields\|frontmatter" src/superclaude/cli/prd/executor.py
(zero matches)
```

The string `"frontmatter"` appears nowhere in `prd/executor.py`. The PRD executor consumes `GATE_CRITERIA` at four call sites (`executor.py:382, 530, 685, 864`) and routes all of them through `_evaluate_gate` — the only evaluator on the PRD path.

### 2. Field declarations — `prd/gates.py`

`GATE_CRITERIA` declares 18 entries (`prd/gates.py:295-505`). Of those, **four** populate `required_frontmatter_fields` with non-empty lists, and **fourteen** declare it as `[]`:

| Step | Line | Fields declared |
|---|---|---|
| `research-notes` | `prd/gates.py:323` | `["Date", "Scenario", "Tier"]` |
| `build-task-file` | `prd/gates.py:360-366` | `["id", "title", "status", "complexity", "created_date"]` |
| `assembly` | `prd/gates.py:452-458` | `["id", "title", "status", "created_date", "tags"]` |
| `present-complete` | `prd/gates.py:502` | `[]` (declared but empty — included in finding's line list) |

The other declarations on lines 298, 304, 317, 341, 354, 389, 402, 408, 414, 427, 433, 439, 476, 489, 502 all pass `required_frontmatter_fields=[]`. The dead-code claim narrows to the **three non-empty entries** — the empty ones are noise but confirm the field is part of the declared contract for every step.

> Note: the finding's File:line list says "388, 402…475, 488, 502" matching empty entries. The line numbers in the current source are 389, 402, 408, 414, 427, 433, 439, 476, 489, 502 — a one-line drift, not a substantive disagreement.

### 3. Is the generic `pipeline/gates.py` evaluator reachable from PRD?

Yes, **the dataclass is shared** — `prd/gates.py:29` imports `GateCriteria` from `superclaude.cli.pipeline.models`. And the generic `pipeline/gates.gate_passed()` at `pipeline/gates.py:20-58` *does* consume the field correctly (`pipeline/gates.py:53-56` calls `_check_frontmatter`).

**But the PRD executor never calls it.** `executor.py:40` imports only `GATE_CRITERIA` from `.gates`; it does not import `gate_passed` from `pipeline.gates`. Every gate evaluation in the PRD path goes through the bespoke `_evaluate_gate` at `executor.py:587-624`. The generic evaluator is dead with respect to PRD.

A sibling consumer, `roadmap/validate_gates.py:12`, *does* import the generic helper (`_frontmatter_values_non_empty`), so the contract is honored on the roadmap path. The PRD path is the lone defector.

### 4. Dead-code claim — confirmed

For the three non-empty entries (`research-notes`, `build-task-file`, `assembly`), the declared frontmatter contract has no enforcement on the PRD path. The fields are documentation-only.

---

## Persona analysis

### Analyzer (reproducibility)

**User-visible symptom.** A heavyweight PRD run produces a task file or assembly artifact whose frontmatter is missing one or more of the declared required keys (e.g. `created_date`, `tags`, `Tier`). `_evaluate_gate` passes the artifact provided it clears `min_lines` and any `semantic_checks`. Status flows on as `PASS`, and the next pipeline stage (or any downstream consumer that does `frontmatter["created_date"]`) crashes with `KeyError` — or, worse, silently misroutes because a missing `status` key looks like "in-progress" by default.

**Worst-case bad output that can ship.** A `build-task-file` artifact missing `status` and `complexity` is the most plausible foot-gun: downstream tier classification (`sc:task` compliance tier) keys off `complexity`, and a missing field would either crash the consumer or silently default to the lowest tier. The Bug-1 scenario quoted in the finding (30-line NDJSON commentary read as a task file) would have failed *both* `min_lines` and the frontmatter check — the latter was the defense-in-depth layer that was never wired, so when `min_lines` caught it, that was the only signal.

**Reproducibility.** Mechanical and deterministic: write a step output with valid line count + passing semantic checks but missing one declared frontmatter key, run `_evaluate_gate`, observe `True`. No timing or environment dependence. The finding's confidence of 0.97 is well-founded.

**Caveat — does the symptom manifest today?** Today, `research-notes` and `build-task-file` happen to also have semantic checks that overlap partially with the frontmatter contract (`research_notes_sections`, structural checks on the task file). Those semantic checks may catch *some* missing-frontmatter cases by accident. But `assembly` (`prd/gates.py:452-465`) has only one semantic check (`prd_sections`) which validates section headings, not frontmatter — so a malformed `assembly` artifact is the cleanest reproduction path.

### Refactorer (blast radius)

**Same shape as F-22?** Yes — and that is the key insight. F-22 (`enforcement_tier` values `EXEMPT`/`LIGHT` not recognized by `_evaluate_gate`) and F-08 are **two instances of the same class of bug**: the `GateCriteria` dataclass has four fields, and the PRD's bespoke evaluator silently honors only two of them.

`pipeline/models.py:67-82` defines `GateCriteria` with four fields:

| Field | Honored by PRD `_evaluate_gate`? |
|---|---|
| `required_frontmatter_fields` | **No** (F-08) |
| `min_lines` | Yes (`executor.py:596`) |
| `enforcement_tier` | Partially — F-22: only `STRICT` branches; `EXEMPT`/`LIGHT` ignored (`executor.py:531-540`) |
| `semantic_checks` | Yes (`executor.py:612`) |

So **two of the four declared contract fields are under-enforced on the PRD path.** The generic `pipeline/gates.gate_passed()` honors all four. The blast radius is the entire PRD pipeline (18 gate entries), but the *correctness impact* concentrates on the three steps with non-empty `required_frontmatter_fields` (and on any future step that populates the field expecting enforcement).

**Other silently-ignored dataclass fields?** The check above enumerates the full surface of `GateCriteria`. No other fields exist on the dataclass, so this exhausts the pattern within `GateCriteria` itself. However, the pattern (bespoke PRD evaluator divergent from generic shared evaluator) is a structural smell — future field additions to `GateCriteria` are likely to repeat the bug unless the PRD path is refactored to call `pipeline.gates.gate_passed()` directly.

**Refactor sketch.** Replace `_evaluate_gate` body (executor.py:587-624) with a delegation to `pipeline.gates.gate_passed()` plus the PRD-specific diagnostics/logging wiring. This collapses F-08, F-22, and any future drift into a single shared implementation. Estimated diff: ~30 lines, touching one function. Risk: low — the generic helper has been exercised by the roadmap and sprint paths.

### Architect (severity calibration)

**Preliminary severity** (declared contract not enforced): HIGH.

**Calibration factors.**

1. **Downstream tolerance.** The PRD pipeline does not appear to do strict `frontmatter[key]` lookups inside the executor itself — most downstream reads happen in human review or in adjacent tools (sc:task tier classification, the assembly renderer). A missing `created_date` in a `build-task-file` artifact will probably not crash the *pipeline*, but will degrade artifacts that ship to humans or to the next CLI command. Severity moderates from HIGH-crash toward HIGH-silent-corruption.

2. **Overlapping coverage by semantic checks.** As noted in the Analyzer section, `research-notes` and `build-task-file` have semantic checks that partially overlap the frontmatter contract. This reduces the *realized* defect rate today but is fragile — it is implicit, undocumented overlap that future contributors will not preserve.

3. **Defense-in-depth gap.** The finding correctly notes that Bug 1 (NDJSON-as-task-file) would have been caught by the frontmatter check as a second mechanism. The single layer that did catch it (`min_lines`) is the same single layer for every step. This is a P7 (control-loop) pattern: the architecture *declares* defense in depth and only delivers one layer.

4. **Surface area.** Three non-empty entries × ~2 fields each = 13 frontmatter keys whose declared contract is unenforced. The risk is bounded but real.

5. **Calibration vs F-22.** F-22 is MEDIUM because the latent failure (EXEMPT/LIGHT mistreated as STANDARD) requires a future config change to manifest — today no step triggers it. F-08 is **worse**: the latent failure manifests immediately for any artifact that omits a declared field, with no config change required. F-08 should remain HIGH, F-22 stays MEDIUM, and the difference is "live today" vs "armed for later."

**Final calibrated severity: HIGH.** Recommend not downgrading to MEDIUM despite the incidental semantic-check overlap, because (a) the `assembly` step has no such overlap, and (b) the architectural pattern (bespoke evaluator silently dropping contract fields) is itself the primary risk.

---

## Convergence

| Field | Value |
|---|---|
| **Verdict** | UPHELD — finding is accurate, mechanism is exactly as described, dead-code claim verified at file:line. |
| **Convergence score** | 0.95 — all three personas agree the bug is real, reproducible, and exhibits the same root cause as F-22 (under-enforcement of `GateCriteria` by the PRD bespoke evaluator). Minor disagreement is only about whether incidental semantic-check overlap should soften severity; architect's calibration resolves this in favor of HIGH because `assembly` lacks the overlap. |
| **Final severity** | **HIGH** (unchanged from Stage 2 preliminary) |
| **Fix difficulty** | **LOW** — two viable fixes: (a) add a frontmatter check block to `_evaluate_gate` (executor.py:587-624) mirroring `pipeline/gates.py:53-58`; or (b) refactor `_evaluate_gate` to delegate to `pipeline.gates.gate_passed()`. Option (b) also closes F-22 in the same diff. Estimated effort: 30-60 lines, one file, plus tests for each of the three non-empty entries. |
| **Recommended fix** | Option (b) — delegate. Co-fix with F-22. Rationale: collapses the divergence between PRD and generic evaluators, prevents the same class of bug from recurring when new fields are added to `GateCriteria`. |

### Synthesis

F-08 is a real, mechanically-verifiable, HIGH-severity gap: `prd/gates.py` declares `required_frontmatter_fields` on 18 entries (3 non-empty) and `prd/executor.py:_evaluate_gate` (executor.py:587-624) reads only `min_lines` and `semantic_checks`. The shared `GateCriteria` dataclass (`pipeline/models.py:67-82`) is honored fully by the generic `pipeline/gates.gate_passed()` (`pipeline/gates.py:53-56`) and by the roadmap path, but the PRD bespoke evaluator silently ignores the contract.

The defect is structurally identical to F-22 (`enforcement_tier` partially ignored): both stem from the PRD pipeline maintaining a separate evaluator that has drifted from the shared dataclass. Of the four fields on `GateCriteria`, the PRD evaluator honors two fully, one partially, and one not at all. The recommended remediation is to converge the PRD evaluator onto `pipeline.gates.gate_passed()`, closing F-08 and F-22 together and pre-empting future drift.

Severity stays HIGH because (a) the `assembly` step has no semantic-check overlap to mask the gap, (b) the failure manifests on any artifact missing a declared field — no config change required — and (c) the architecture documents defense-in-depth that the implementation does not deliver.

---

## Evidence ledger

- `src/superclaude/cli/prd/executor.py:587-624` — `_evaluate_gate` body; only reads `gate.min_lines` and `gate.semantic_checks`.
- `src/superclaude/cli/prd/executor.py:40` — imports only `GATE_CRITERIA`, not the generic evaluator.
- `src/superclaude/cli/prd/executor.py:382, 530, 685, 864` — all `GATE_CRITERIA.get(...)` call sites; all flow through `_evaluate_gate`.
- `src/superclaude/cli/prd/gates.py:295-505` — `GATE_CRITERIA` table, 18 entries.
- `src/superclaude/cli/prd/gates.py:323, 360-366, 452-458` — three entries with non-empty `required_frontmatter_fields`.
- `src/superclaude/cli/pipeline/models.py:67-82` — `GateCriteria` dataclass, four fields.
- `src/superclaude/cli/pipeline/gates.py:20-58` — generic `gate_passed()`; honors `required_frontmatter_fields` at lines 53-56.
- `src/superclaude/cli/roadmap/validate_gates.py:12` — sibling path that imports the generic helper, confirming the contract is honored elsewhere.
- Grep: `grep -n "required_frontmatter_fields\|frontmatter" src/superclaude/cli/prd/executor.py` returns zero matches.
