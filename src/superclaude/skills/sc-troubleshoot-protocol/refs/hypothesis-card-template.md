# Hypothesis Card Template

Used by every agent that produces a hypothesis — `root-cause-analyst` in Wave 1.7, and every Tier 2 agent in Wave 3.

A hypothesis card is **one** proposed cause-and-fix, not a list. If the agent has two equally strong candidates, it picks one and notes the other under "Alternatives considered" — Tier 2 fan-out exists precisely so that other agents can champion alternative hypotheses.

## Template

```markdown
# Hypothesis: <one-line claim, e.g. "eval_run.py never imports `Path`, so the NameError fires on line 142">

**Agent**: <agent-name>
**Tier**: <1|2>
**Timestamp**: <ISO 8601>
**Cause class**: <from triage-checklist.md, e.g. "Missing/wrong import">
**Claim class**: `static_defect` | `runtime_behavior` | `environment_dependent` | `config_value` | `doc_contract` | `mixed`
  — `static_defect`: source-reading alone is sufficient evidence (typos, missing imports, regex literals, syntax errors)
  — `runtime_behavior`: claim depends on dynamic control flow, side effects, executed semantics, or library call dispatch
  — `environment_dependent`: claim depends on OS / runtime / feature-flag / network / data state
  — `config_value`: claim depends on configuration / settings / env vars
  — `doc_contract`: claim depends on a documented contract (RFC, spec, README)
  — `mixed`: spans more than one class
**Evidence class**: `runtime_repro` | `runtime_trace` | `log_evidence` | `source_static` | `doc_static` | `none`
  — `runtime_repro`: executed reproducer with captured stdout/stderr
  — `runtime_trace`: live execution trace, debugger output, instrumentation log
  — `log_evidence`: post-hoc log excerpt from the failing run
  — `source_static`: source file Read + cited line (no execution)
  — `doc_static`: documentation citation (no execution, no source)
  — `none`: prose only / no evidence
**Verdict direction**: `AFFIRM` | `REFUTE` | `REJECT`
  — REFUTE/REJECT verdicts on `runtime_behavior` claims face a higher calibration bar (see escalation-rubric § Verdict-direction modifier).
**Consistency with docs**: <aligned | conflicts | not_applicable | no_docs_found>

## Claim

One paragraph (≤ 4 sentences) stating the proposed root cause in plain language. No hedging, no "this might be" — state the claim plainly. Confidence goes in its own section.

## Evidence

List 1–4 evidence items. **Each item must be either a `file:line` citation with a quoted snippet, or a command + actual output.** Speculation is not evidence.

- `path/to/file.py:142` — `result = Path(scratch_root) / "foo"` (uses `Path` but no `from pathlib import Path` in the file's imports — verified by reading lines 1–20)
- Command: `uv run python -c "from src.module import target"` → `NameError: name 'Path' is not defined`
- `path/to/test_file.py:88` — the failing test that exercises this code path

## Proposed Fix

Describe the change in one paragraph. Then list the files that would change:

- `path/to/file.py` — add `from pathlib import Path` to imports
- (any others)

Include a test that would prove the fix:

- Existing: `tests/path/to/test_file.py::test_eval_run` should pass once the import is added
- New (if needed): describe the new test

## Confidence

Self-reported confidence: <0.0–1.0>

The skill will re-grade this against the rubric. The agent's score is a signal, not the final number.

Per-dimension self-assessment:
- Evidence grounding: <0.0|0.5|1.0> — <one-line reason>
- Runtime check: <0.0|0.5|1.0> — <derived from (claim_class, evidence_class) cross-tab; cite the executed-reproducer command + captured output, OR cite a runtime-asserting test by name + its execution state. For claim_class=static_defect, mark "inherits Evidence grounding" with no further evidence required.>
- Symptom coverage: <0.0|0.5|1.0> — <one-line reason>
- Reproducibility fit: <0.0|0.5|1.0> — <one-line reason>
- Fix directness: <0.0|0.5|1.0> — <one-line reason>
- Domain coherence: <0.0|0.5|1.0> — <one-line reason>

## Risks

What breaks if this fix is wrong, or if the fix introduces a regression elsewhere. Be specific — name the file or behaviour at risk.

## If I'm wrong, it's probably because...

One sentence. The agent's best guess at the next-most-likely explanation if this hypothesis is wrong. This is what the Tier 2 fan-out uses to choose complementary agents.

## Falsification standard

One sentence. What concrete evidence — an executable command and expected output, a named test outcome, a log assertion, or a measurable observation — would prove this hypothesis WRONG? "Re-reading the source differently" is NOT a falsification standard. If you cannot name a falsification standard, the claim_class is `runtime_behavior` and Runtime check self-scores ≤ 0.5.

## Evidence classification [V2 merged]

- **Claim class**: <one of the seven above> — <one-line reason>
- **Evidence class**: <one of the six above> — <one-line reason>
- **Runtime check performed?**: yes | no — <if no, one-line reason why not>
- **If REFUTE verdict, coverage statement**: <which paths/files/conditions were inspected; explicitly name anything not inspected that could flip the verdict>

Filling rule: an empty or "Not applicable" value on `evidence_class` is a defect; cards with `claim_class: runtime_behavior` AND `evidence_class ∈ {source_static, doc_static, none}` MUST self-cap their confidence at 0.65 in the per-dimension self-assessment and state the cap in the rationale.

## Recommended evidence shape (v2.0 preview)

For new cards, the recommended evidence shape is a typed table that makes each item's evidence kind explicit:

| # | Kind | Source | Content |
|---|------|--------|---------|
| E1 | `source_citation` | `path/to/file.py:142` | (verified snippet) |
| E2 | `executed_reproducer` | `uv run python -c "..."` | (captured stdout/stderr) |
| E3 | `test_assertion` | `tests/.../test_x::test_y` | (execution state: fails / passes / not-run) |

Kinds: `source_citation`, `executed_reproducer`, `test_assertion`, `documentation`, `log_artifact`.

This shape is **OPTIONAL in v1.5** — the existing bulleted-list evidence shape remains valid. The typed table will become **MANDATORY in v2.0** (target: follow-up commit after pin-test corpus in `calibrator-eval-cases.md` confirms v1.5 stability).

## Alternatives considered

Bullet list of 0–3 other hypotheses the agent considered and rejected. For each, one line on why it was rejected. Empty list is fine if there were no plausible alternatives.

## Grounding gaps

What the agent could **not** verify (e.g. "could not run the failing test locally because UV is unavailable in the sandbox"). Explicit gaps protect the calibration step from over-counting evidence.
```

## Filling the card

- **Length cap**: ≤ 1 page in plain rendering (~ 60 lines). Longer cards mean the agent is over-reaching.
- **No `TODO`s, no placeholders.** If a field is genuinely not applicable, write "Not applicable — <reason>". An empty section is a defect.
- **One claim, one fix.** This is non-negotiable. Multi-claim cards defeat the fan-out math.
- **Cite real files.** The validation pass in Wave 5 will drop any unfounded citations. Cards that lose their citations lose credibility.

## Worked example (illustrative — not a real card)

```markdown
# Hypothesis: eval_run.py uses Path without importing it

**Agent**: root-cause-analyst
**Tier**: 1
**Timestamp**: 2026-05-21T05:14:30Z
**Cause class**: Missing/wrong import

## Claim

`eval_run.py` references `Path(...)` on lines 142 and 156 but never imports `Path` from `pathlib`. The `NameError` reported in the user's stack trace fires at line 142 because the symbol is undefined at module load.

## Evidence

- `src/superclaude/cli/eval_run.py:142` — `scratch = Path(args.scratch_root) / ...` (no `Path` import in lines 1–20)
- Stack trace from user: `NameError: name 'Path' is not defined` at `eval_run.py:142`
- `git log -p src/superclaude/cli/eval_run.py` — the `Path(...)` call was introduced in commit 5a65c62, but the matching import was not added

## Proposed Fix

Add `from pathlib import Path` to the imports section of `src/superclaude/cli/eval_run.py`. Single-line addition.

## Confidence

0.92

[per-dimension breakdown ...]
```
