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
runs-in=<RUN-SITE label from <output-dir>/execution-locus.md>
runs-in=unknown

## Claim

One paragraph (≤ 4 sentences) stating the proposed root cause in plain language. No hedging, no "this might be" — state the claim plainly. Confidence goes in its own section.

## Evidence

List 1–4 evidence items. **Each item must be either a `file:line` citation with a quoted snippet, or a command + actual output.** Speculation is not evidence.

- `path/to/file.py:142` — `result = Path(scratch_root) / "foo"` (uses `Path` but no `from pathlib import Path` in the file's imports — verified by reading lines 1–20)
- Command: `uv run python -c "from src.module import target"` → `NameError: name 'Path' is not defined`
- `path/to/test_file.py:88` — the failing test that exercises this code path
- behaviour-definition: row 1 — required when the mechanism sentence asserts what a primitive does (shared procedure in Wave 3 step 1 accepts a producer assertion or received card; write the row to `<output-dir>/behaviour-definitions.md` before fetching, reuse a matching row, and bind its citation after card receipt but before calibration in either tier); a missing row or empty Status caps calibrated confidence at 0.5 (`behaviour-cite: missing`, C8)

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

When two mechanisms are in dispute for the same observable (Wave 3 step 4.5, or S1.6.4 rows), embed this form here instead of the one sentence — at most two arms, one form per pair. The card still advances one claim and one fix; the second arm is its comparator, not a second card claim:

# Discriminator: <symptom or token>
Hypothesis A: <one sentence naming the runtime property that differs>
Hypothesis B: <one sentence>
Observable that differs: <one boolean; where it is emitted — file:line, log key, metric name, or column>
Exact probe: <one read-only command or query; complete successful capture reduces to true|false; missing/empty/incomplete/error capture is unobserved, never false>
Primitive under dispute, fetched verbatim: <locator + pasted text of the thing the two mechanisms disagree about: a function body, a library doc section, a config schema, an RFC/spec paragraph. NOT the observed output.>
Reference-context value: <true|false|n/a — what the observable reads in a known-good context (passing run, passing test, passing environment, known-good input). n/a only on the first instrumented run.>
Pre-registered outcome table (written before the probe runs):
| Probe result | A | B |
|---|---|---|
| true  | <consistent\|refuted\|inconclusive — reason> | <consistent\|refuted\|inconclusive — reason> |
| false | <consistent\|refuted\|inconclusive — reason> | <consistent\|refuted\|inconclusive — reason> |
Falsifier sentence: "If <observable>=<value> on the next run, <A|B> is false" only when the preregistered mapping supports refutation; otherwise `No discriminating falsifier established — <reason and missing evidence>`. Never invent a differing outcome to fill the form.
Self-consistency: compare a literal Reference-context value with an actually observed reference-arm value on ANY run, including the first; mismatch marks THIS PROBE `suspect` under Grounding Gaps and skips its outcome table. Record run/arm/command provenance. A failing-arm difference is not a reference mismatch. Skip comparison for an evidenced first-run `n/a` or an unobserved reference cell; neither establishes a passing control. Apply the binary table only to a complete observed boolean, never unobserved. Equal predictions are non-discriminating; unknown predictions require a reason, not fabricated values. `consistent` is compatibility, not confirmation; a both-consistent result cannot select a cause or populate root_cause_summary without independent discriminating evidence.

Worked example (I/O; illustrative adaptation, NOT verified runtime evidence): historical incident pointers are unverified context aliases, not a resolvable evidence archive supplied by this template. Assume for this example that `procUptime.go Open()` sets `nonSeekable=true` and bash `read.def` uses `lseek … ESPIPE → zread(fd,&c,1)`. A: under the matched failing-arm conditions, this path prevents obtaining a digit-leading `up` value. This is a value claim, NOT a claim about `read`'s exit status: an unterminated input can yield `up=123` with read status 1 and regex success. The regex below tests only the narrowed value claim; read-status or causal claims require separate evidence. B: the workload's `mktemp` site is unwritable. Observable: `uptime-regex` (`IFS=' ' read -r up _ < /proc/uptime; [[ $up =~ ^[0-9] ]]`). Literal reference expectation: `true`; reference-arm capture is unobserved. Preregistered table: true → A refuted / B consistent; false → A consistent / B consistent. Falsifier: "If uptime-regex=true on the failing arm, A is false." Suppose a complete failing-arm capture gave `uptime-regex=false`, `bulk=true`, and `tmp-writable=true` at the same site/credentials/time as the claimed failure. This is consistent with A and refutes that narrowly scoped B, but does not exclude other mechanisms or confirm A; retain UNDETERMINED and empty root_cause_summary without further causal evidence. Companion `started-line`: expected reference `true`, hypothetical failing-arm `false` beside `cloned`, reference arm unobserved ⇒ not suspect merely for that difference. If an actual reference-arm capture instead returned `false`, mark that probe suspect and skip its table, even on a first run with a literal reference expectation. Real use must supply run/arm/command spans; these assumed values are not observations.

Worked example 2 (non-I/O; queue consumer ordering, hypothetical): Symptom: duplicate invoice emails. A: a crash after the side-effect but before ack causes redelivery of the message that produced the duplicate. B: HTTP retry causes two publications. Assume an illustrative broker contract, NOT a verified vendor quotation: every redelivery has `redelivered=true`. Probe the specific duplicate's message ID, publish ID and delivery IDs, correlating both side-effects; require complete delivery coverage and captured flag values before reducing to a boolean. Observable: whether the duplicate-producing message was redelivered. Reference expectation: `false`; reference observation must be separately captured or marked unobserved. Table: true → A consistent / B consistent (redelivery and double publication can coexist); false → A refuted / B consistent, ONLY under the stated completeness and assumed-contract conditions. Empty/incomplete/error results stay unobserved and skip the table. Falsifier: "If complete captures show no redelivery of the duplicate-producing message under this contract, A is false." An invoice-wide bool_or does not identify the duplicate's mechanism; independently examine publication identities to test B. These two arms are not an exhaustive causal model and neither consistent outcome alone proves the diagnosis.

## Evidence classification

- **Claim class**: <one of the six above> — <one-line reason>
- **Evidence class**: <one of the six above> — <one-line reason>
- **Runtime check performed?**: yes | no — <if no, one-line reason why not>
- **If REFUTE verdict, coverage statement**: <which paths/files/conditions were inspected; explicitly name anything not inspected that could flip the verdict>

Filling rule: an empty or "Not applicable" value on `evidence_class` is a defect; cards with `claim_class: runtime_behavior` AND `evidence_class ∈ {source_static, doc_static, none}` MUST self-cap their confidence at 0.65 in the per-dimension self-assessment and state the cap in the rationale. When an existing producer menu has at least one `surviving=yes` row, a card whose claim names an enum token (a categorical value the symptom reports) MUST cite the `producers.md` row id(s) with `surviving=yes` for that token; excluding a token requires the `file:line` of its exit statement (calibrator C2: `unproven_exclusion:<token>`, Runtime check := 0.0). With a missing, header-only or empty surviving menu, record the producer-citation check as skipped with its reason, require ordinary grounded `file:line` or captured-output citations, and continue behaviour binding and independent calibration. No bypass relaxes documentation, locus, evidence or confidence guards; enumeration's zero-survivor recovery remains mandatory when enumeration ran.

## Recommended evidence shape (typed table)

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

If Wave 1.6 emitted a Diagnosability Context Card with `verdict ∈ {partial, insufficient}`, reference it here (e.g., "Diagnosability verdict: partial — see <card-path>; coverage of 'why' is missing, so this hypothesis cannot be falsified at runtime without the proposed instrumentation").
```

## Filling the card

- **Length cap**: ≤ 1 page in plain rendering (~ 60 lines). Longer cards mean the agent is over-reaching.
- **No `TODO`s, no placeholders.** If a field is genuinely not applicable, write "Not applicable — <reason>". An empty section is a defect.
- **One claim, one fix.** This is non-negotiable. Multi-claim cards defeat the fan-out math.
- **Cite real files.** The validation pass in Wave 5 will drop any unfounded citations. Cards that lose their citations lose credibility.
- `runs-in=`: mandatory whenever the execution-locus card derives `SAME-ENV ≠ yes`; a card without it is returned unread (same rule as `consistency_with_docs`). `unknown` is legal — the calibrator then caps Runtime check ≤ 0.5 (`locus_unknown`). Written as a plain `runs-in=<label>` line, not bold, so the mechanical check (`^runs-in[=:]`) matches.
- `environment-property:`: include the line ONLY when the claim names an environment property (typically `claim_class: environment_dependent`); omit it otherwise. A card that carries it must cite a 2x2 row (`## Discriminator rows` of the tasklist or the refs/primitive-differential.md differential) or the calibrator caps calibrated confidence at 0.5 (`uncited`, C7). Plain line, not bold (`^environment-property:` is the check).

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
