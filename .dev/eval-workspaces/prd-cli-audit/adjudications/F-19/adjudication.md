# F-19 Adjudication: Sentinel-vs-Gate Source Mismatch

**Input finding**: `.dev/eval-workspaces/prd-cli-audit/findings/F-19-sentinel-vs-gate-source-mismatch.md`
**File under review**: `src/superclaude/cli/prd/executor.py:518-553`
**Preliminary severity (Stage 2)**: MEDIUM
**Mode**: /sc:adversarial Mode B — three personas, then converge.

---

## Re-verification of finding claims

Verified against current source on `feature/sc-auggie-review-protocol` (HEAD = 2219545).

1. **Two-source structure confirmed** (executor.py:518-532):
   - L518: `output_text = _extract_text_from_stream_json(raw_output)` — NDJSON stream → assistant-text concatenation.
   - L522-524: `gate_content = _resolve_step_content(step_id, self._config.task_dir, output_text)` — for the four step_ids in `_STEP_ARTIFACT_FILES` (`parse-request`, `scope-discovery`, `research-notes`, `sufficiency-review`), `_resolve_step_content` (L254-293) `rglob`s `task_dir` and its parent for the canonical filename, picks the **largest** match, and only falls back to `ndjson_text` if no disk match has non-whitespace content (L293).
   - L527: `status = self._determine_status(exit_code, output_text, step_id)` — sentinel detection (`_detect_sentinel`, L75-91) reads only `output_text` (NDJSON-derived).
   - L532: `gate_passed = self._evaluate_gate(step_id, gate, gate_content)` — gate logic (L587-624) reads `gate_content` (potentially disk-derived).

2. **Sources can legitimately diverge.** When a step in `_STEP_ARTIFACT_FILES` writes a multi-hundred-line artifact via Write/Edit but its NDJSON stdout only carries a short narration, `output_text` ≠ `gate_content`. This is by design — `_resolve_step_content`'s docstring (L257-265) explicitly states the NDJSON "only captures the assistant's commentary," and disk preference is the whole point of the helper.

3. **Critical sequencing constraint the finding under-states.** Gate evaluation is **guarded** by `if gate and status.is_success` (L531). Per `PrdStepStatus.is_success` (`models.py:135-142`), only `PASS`, `PASS_NO_SIGNAL`, and `PASS_NO_REPORT` qualify — `HALT` does **not**. Therefore the two evaluators do not run as peers that can publish competing verdicts; sentinel detection short-circuits gate evaluation. The finding's own "Trace" paragraph notes this ("the gate code never runs because `status.is_success` is False"), but the title and severity framing ("two sources of truth … unpredictable halts") suggest a symmetric race that the code does not actually permit.

4. **What the bug actually is.** The real defect is asymmetric: **sentinel HALT in narration vetoes a passing disk artifact** (sentinel-wins-over-disk), but a sentinel-CONTINUE or absent-sentinel still subjects the disk artifact to gate checks. Inverse asymmetry — sentinel CONTINUE in narration overriding a failing disk artifact — cannot occur, because the gate still runs. So the only realistic divergence scenario is: subprocess writes a quality artifact to disk, emits hortative "EXIT_RECOMMENDATION: HALT" in narration (e.g. recommending the *user* halt for a non-blocking reason), pipeline halts despite passing artifact.

---

## Persona analyses

### Analyzer — reproducibility

**Scenario**: A `research-notes` step subprocess writes a 420-line `research-notes.md` that satisfies `GATE_CRITERIA["research-notes"]` (`min_lines`, semantic checks). Its NDJSON narration includes a recommendation paragraph ending with a line `EXIT_RECOMMENDATION: HALT` outside any fenced code block — perhaps the subprocess is recommending the operator halt to clarify scope before downstream steps.

**Executor behavior**:
- L518: `output_text` = ~30 lines of narration including the bare sentinel line.
- L522: `_resolve_step_content` finds `research-notes.md` on disk (420 lines > 0), returns disk content.
- L527: `_determine_status` calls `_detect_sentinel(output_text)` → matches "HALT" → returns `PrdStepStatus.HALT`.
- L531: `status.is_success` is False → gate block skipped entirely; `_evaluate_gate` never runs against the 420-line artifact.
- L545: `if exit_code == 0 and gate_content.strip()` — artifact **is still persisted** via `_persist_step_artifact` (L546), so downstream steps would have the data — but the pipeline halts in the caller because the returned status is HALT.

**Reproducibility verdict**: Deterministic given the input. The race-condition framing in the finding is inaccurate — there is no race; the order of evaluation is fixed and the outcome is predictable from the inputs. **Reproducible: yes.** Practical likelihood depends on prompt discipline (whether `_EXIT_SENTINEL_PATTERN` is plausibly emitted as commentary). The four affected `_STEP_ARTIFACT_FILES` steps use prompt builders documented to ask for sentinels, so the trigger surface is non-trivial.

### Refactorer — blast radius

**Is "two sources for one verdict" a pattern elsewhere?**

Grep across `src/superclaude/cli/prd/`:
- `_determine_status` / `_evaluate_gate` are each called exactly once — at L527 and L532 of `_execute_step`.
- `_resolve_step_content` is called only at L522.
- QA fix cycle (L854) uses a single source (`qa_result.status.is_success`); no dual-source split there.
- `_STEP_ARTIFACT_FILES` enumerates only 4 step IDs; steps outside that map (e.g. `template-triage`, `build-task-file`, all Stage B steps) get `gate_content = output_text` (L268-269), so for them the two sources collapse to one — the divergence cannot occur.

**Blast radius**: Localized to one function (`_execute_step`) and four step IDs. **No fan-out.** No identical sentinel-vs-gate pattern in QA cycle, parallel-step handling, or Stage B. Fix touches a single call site.

### Architect — severity calibration

**Preliminary MEDIUM** rests on "inconsistent verdicts → unpredictable halts." After re-verification:

- **"Inconsistent verdicts" is mischaracterized.** Behavior is deterministic, not racy. The asymmetry (sentinel-wins-over-disk-pass) is a real defect, but it is *one-directional* and *predictable*, not a class of unpredictable disagreement.
- **Blast radius is small** — single call site, four step IDs.
- **Failure mode is fail-safe-ish.** A spurious HALT stops the pipeline, persists the artifact (L545-546), and writes resume state (per `_signal_handler`/checkpoint plumbing). User loses time and turn budget but doesn't get a silent wrong answer downstream. Compare against the inverse hypothetical (gate-FAIL silently overridden by sentinel-CONTINUE) — that cannot happen, because gate still runs when sentinel is CONTINUE/absent.
- **Frequency floor**: requires subprocess to emit an unfenced `EXIT_RECOMMENDATION: HALT` line that does not reflect artifact quality. Plausible (LLM hedging), but not high-frequency for disciplined prompts.
- **Mitigations already in tree**: `_CODE_BLOCK_PATTERN` excludes fenced sentinels (L86), reducing accidental matches in code samples.

**Calibration**: MEDIUM is **too high**. The bug is a one-directional spurious-halt risk on four step IDs with fail-safe semantics and a localized fix. **LOW-to-MEDIUM**, leaning LOW.

---

## Convergence

**Verdict**: **CONFIRMED with reframing.** Two-source structure exists and can produce divergent inputs to sentinel and gate evaluators. The finding's framing ("unpredictable halts," "independent verdicts," "irreversible halt") overstates the disorder — sentinel deterministically wins because gate evaluation is gated on `status.is_success` (L531). The real defect is the **one-directional, asymmetric veto**: a narrative HALT sentinel can spuriously fail a step whose on-disk artifact would have passed.

**Convergence score**: **0.85** — all three personas agree the source mismatch is real and reproducible; they agree the severity framing in the finding is inflated; they agree the fix is localized.

**Final severity**: **LOW** (downgrade from preliminary MEDIUM).
- Deterministic, not racy.
- One-directional (spurious HALT only; spurious PASS impossible because gate still runs when sentinel is non-HALT).
- Confined to 4 step IDs in `_STEP_ARTIFACT_FILES`.
- Fail-safe: halts conservatively, persists artifact, writes resume state — operator can resume.
- Bounded by prompt discipline (sentinels are documented contract).

**Fix difficulty**: **LOW (S, ~30-60 LOC).** Two viable approaches, both single-site:

1. **Unify the source.** Run `_detect_sentinel` on `gate_content` (or on both, with sentinel-on-disk taking precedence). Tradeoff: a sentinel buried in a 400-line markdown file is more likely to be inside content meant for the user, so add stricter anchoring (e.g. require sentinel to be on a line by itself at the end of the document).
2. **Order-swap with override.** Evaluate gate first; if gate PASS and sentinel HALT, log a warning and treat as PASS_WITH_HALT_WARNING (new status) — surfaces the disagreement to the operator without forcing a halt on disk evidence of success.

Either approach is one method-body change in `_execute_step` plus one new test in `tests/cli/prd/test_executor.py` exercising the "disk PASS + narrative HALT" case.

**Synthesis**:
- F-19 is a real but mis-severitized finding. Re-classify as LOW.
- The structural critique (two sources for one decision) is valid; the operational critique (race / unpredictable halts) is not — behavior is deterministic.
- Recommend fix path (1) — unify on `gate_content` for sentinel detection, with a stricter anchoring rule — because it preserves the single-decision invariant the original design appears to have intended.
- No fan-out remediation needed; pattern is localized.
- Cross-reference: this adjudication does not change the prelim severity of any other finding; the QA cycle (L854) and Stage B steps do not share the dual-source structure.

**Citations** (all `src/superclaude/cli/prd/executor.py` unless noted):
- L75-91 `_detect_sentinel` (anchored, code-block-aware regex over `output`)
- L99-130 `_extract_text_from_stream_json` (NDJSON → assistant-text)
- L246-251 `_STEP_ARTIFACT_FILES` (4 step IDs)
- L254-293 `_resolve_step_content` (disk-preferred, largest-match, NDJSON fallback)
- L518-553 `_execute_step` dual-source block (the finding's locus)
- L527 sentinel-on-NDJSON
- L531 `if gate and status.is_success` — the short-circuit that makes behavior deterministic
- L532 gate-on-resolved-content
- L545-546 artifact persisted even on HALT
- L854 QA cycle uses single source (no fan-out)
- `src/superclaude/cli/prd/models.py:135-142` `is_success` membership
