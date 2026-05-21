# Adjudication: F-10 — NDJSON extraction silently swallows errors and falls back to raw blob

## Evidence re-verification (load-bearing, performed before persona analysis)

- `src/superclaude/cli/prd/executor.py:99-130` — `_extract_text_from_stream_json(raw: str) -> str` is the function under audit. The body matches the finding verbatim:
  - Line 111: `for line in raw.splitlines():`
  - Line 117-118: `except (json.JSONDecodeError, ValueError): continue` — confirmed silent swallow #1 (malformed line dropped, no log).
  - Line 120-123: `message = obj.get("message") or {}; content = message.get("content"); if not isinstance(content, list): continue` — confirmed silent swallow #2 (every non-assistant envelope — `type:"user"`, `type:"system"`, `type:"result"`, `tool_use`-only assistant messages — falls through with no signal).
  - Line 124-128: `if isinstance(block, dict) and block.get("type") == "text":` — only `text` blocks are collected; `tool_use`, `tool_result`, `thinking`, and any unknown block types are silently discarded.
  - Line 130: `return "\n".join(texts) if texts else raw` — **confirmed the fallback-to-raw branch**: when the parser collects zero text blocks, it returns the entire raw NDJSON stream verbatim.
- **Malformed JSON trace** (re-derived from the source): a line that fails `json.loads` enters the `except` at 117-118, hits `continue` at 118, and contributes nothing to `texts`. If *every* line is malformed and `texts` ends up empty, line 130 returns `raw` — the malformed stream is handed verbatim to gate evaluation. No exception escapes, no diagnostic is emitted, no counter is incremented.
- **Stream with no `type:"text"` blocks trace**: each NDJSON line parses (skipping 117-118), `message.content` may be a list (passing 122-123), but the per-block check at 125 finds no `type=="text"` entry. `texts` remains `[]`. Line 130 returns `raw` — the full NDJSON envelope text.
- `src/superclaude/cli/prd/executor.py:511-518` — only caller of `_extract_text_from_stream_json`. `raw_output = output_file.read_text(...)` at 514, then `output_text = _extract_text_from_stream_json(raw_output) if raw_output else ""` at 518. `output_text` is the post-extraction string.
- `src/superclaude/cli/prd/executor.py:520-524` — `output_text` is then passed as the *third* argument (`ndjson_text`) to `_resolve_step_content(step_id, self._config.task_dir, output_text)`, which binds the result to `gate_content`.
- `src/superclaude/cli/prd/executor.py:254-293` — `_resolve_step_content` performs the dispatch-table check at 267-269 (`if not artifact_name: return ndjson_text`). When the step is missing from `_STEP_ARTIFACT_FILES` (the F-01/F-04 condition), `gate_content` is whatever `_extract_text_from_stream_json` returned — including the raw fallback if no text blocks were found.
- `src/superclaude/cli/prd/executor.py:530-540` — `gate_content` is the input to `_evaluate_gate`; on STRICT failure status is promoted to `PrdStepStatus.HALT`.
- `src/superclaude/cli/prd/executor.py:587-599` — `_evaluate_gate` does `line_count = len(content.splitlines())` at 597. When `content` is the raw NDJSON blob, every envelope line becomes one "line" — the exact mechanism that turns "30 tool_use envelopes" into "Min lines: 30/400".
- **Sentinel detection consequence**: `output_text` is *also* passed to `_determine_status(exit_code, output_text, step_id)` at executor.py:527 → `_detect_sentinel` at line 75-91. When `output_text` is the raw NDJSON blob, sentinel regex `^EXIT_RECOMMENDATION:` runs against JSON-escaped strings; if the subprocess emitted an `EXIT_RECOMMENDATION:` token inside `text`-block content of an `assistant` message, it would be JSON-escaped (e.g. inside `"text":"...EXIT_RECOMMENDATION: HALT..."`) and the anchored `^` regex would not match it at the start of a line. The fallback path therefore also defeats sentinel detection silently.
- Negative claim "no log, no diagnostic": confirmed — there is no `self._logger`, `self._diagnostics`, `print`, `warnings.warn`, or any other emission inside the function body (executor.py:99-130). The function is pure-return, fully silent on every error path.
- Second NDJSON parser at `src/superclaude/cli/prd/monitor.py:69-98` shares the same swallow pattern (cross-reference for F-33), but per F-11 monitor is dead code, so it does not currently contribute to the F-10 incident chain.

Every load-bearing claim in the finding matches what is on disk at this revision. No discrepancies. Two additional consequences worth recording: (a) sentinel detection is also defeated when the fallback fires, and (b) the swallowed conditions are not just unlogged but uncounted — there is no instrumentation at all on the parser.

---

## Persona 1 — Analyzer (opus, depth=standard) — focus: reproducibility

**Is the production incident genuinely a reproduction of F-10, or merely consistent with it?**

The production incident — "30 NDJSON lines counted as 30 content lines, gate `min_lines=400` fails" — is *not just* consistent with F-10, it is the *only* mechanism in the source that can produce that exact symptom. The chain is mechanically deterministic:

1. Subprocess emits stream-only NDJSON (the `claude` CLI default with `--output-format stream-json` per `process.py`). Confirmed at executor.py:514 — output_file is the captured stream, no separate text channel.
2. `_extract_text_from_stream_json` runs on that stream. The subprocess at step 7 (`build-task-file`) performs its work via `Write` tool calls (per prompts.py:381 "Write the task file to: …"). The corresponding NDJSON envelopes are `tool_use` blocks, not `type:"text"` blocks. Per the trace above, `texts` ends empty.
3. Line 130 returns `raw` — the full NDJSON envelope text, line count ≈ number of NDJSON events (~30 for a typical Write-heavy step).
4. `_resolve_step_content` falls through (F-01 dispatch miss) and returns the same NDJSON-as-text to `gate_content`.
5. `_evaluate_gate` splits on newlines and gets ~30. `min_lines=400`. STRICT. HALT.

The "30/400" is not arithmetic coincidence — it is *literally* the count of NDJSON envelopes emitted by a Write-heavy assistant turn, which is the prompted behavior. There is no other code path in the executor that produces a string whose `splitlines()` length matches the NDJSON event count: every other source (disk file, extracted text blocks) would either contain markdown lines or be empty.

**Independent reproduction without F-01:**

If F-01 is fixed (dispatch entry added) but the disk-file search at executor.py:280-291 finds nothing — for example, if the subprocess wrote to a path outside `task_dir` and `task_dir.parent`, or if the `Write` tool failed silently — then `_resolve_step_content` at line 293 also falls back to `ndjson_text`, which is whatever F-10 returned. So F-10 has at least one independent trigger condition: any disk-search miss in a step that is in the dispatch table.

**Conditions for the malformed-JSON arm to fire:**

The malformed-JSON arm (silent swallow #1) requires either (a) partial-buffer truncation under load — possible with non-line-buffered NDJSON pipes; not currently tested — or (b) the subprocess emitting non-JSON debug lines (some `claude` CLI versions emit a banner before NDJSON starts). Not the production trigger here, but a latent path that would produce the same fallback-to-raw symptom with even worse diagnosability.

**Reproducibility verdict**: 1.0 for the no-text-blocks arm (the production trigger). The chain is fully deterministic given the prompted Write-heavy subprocess behavior. The malformed-JSON arm is reproducible in principle but not exercised by the production incident. Confidence: **HIGH**.

---

## Persona 2 — Refactorer (opus, depth=standard) — focus: blast radius

**What is the shape of this defect, and what other code paths share it?**

The shape is: *defensive parser with three independent silent-failure modes whose worst case (no extractable content) emits a fallback that looks structurally similar to the expected output (a multi-line string) but is semantically garbage (the raw envelope stream).* This is the classic "looks like a duck, isn't a duck" anti-pattern: downstream consumers cannot distinguish a successful extraction from a degenerate fallback because both return a `str`.

**Relationship to sibling findings:**

- **F-01 interaction**: F-10's fallback is *required* for F-01's failure mode. If `_extract_text_from_stream_json` instead raised on "no text blocks found", F-01's `gate_content = ndjson_text` path would have crashed loudly at step 7 the first time it was exercised — and the dispatch-table omission would have been caught at the first standard-tier dry run. F-10 is the *concealment mechanism* that allowed F-01 to ship.
- **F-04 interaction**: F-04 is the systemic version of F-01 (13 Write-emitting steps missing from `_STEP_ARTIFACT_FILES`). Every one of those 13 steps depends on F-10's silent fallback to manifest as "wrong gate count" rather than "no content". Without F-10, all 13 would loudly fail at first run; with F-10, the "lucky pass" cases (per F-04 trace: `investigation-{N}` min_lines=50 vs ~50-line NDJSON commentary, `web-research-{N}` min_lines=30 vs ~30-line commentary) silently produce false PASS verdicts on garbage content. **F-10 turns F-04 from a loud-fail-on-first-run defect into a silent-corruption defect.**
- **F-33 interaction**: The duplicated parser in `monitor.py:69-98` shares the swallow pattern but is currently dead per F-11; if monitor were wired up, the same silent-swallow class would extend to state tracking.

**Other code paths that fall back to raw NDJSON:**

I traced every caller of `_extract_text_from_stream_json` (single caller at executor.py:518) and every consumer of its return value:

1. `gate_content` via `_resolve_step_content` (executor.py:522-524) — analyzed above.
2. `output_text` for status detection via `_determine_status` (executor.py:527) — passes through to `_detect_sentinel` (executor.py:571) and to QA verdict scanning (executor.py:578-582). All three operate on raw-NDJSON text when the fallback fires. Sentinel match likelihood drops to ~zero (JSON-escaped text against `^EXIT_RECOMMENDATION:` anchored regex); QA verdict scan at 579 (`'"verdict": "FAIL"' in output`) would *match* the substring inside a raw NDJSON envelope, producing spurious QA_FAIL verdicts on any step that emits a `verdict` token in any other context.
3. `len(raw_output.encode(...))` at executor.py:551 — used only for telemetry, not behavior.

So the blast radius from a single fallback firing is: (a) wrong line count for `min_lines`, (b) defeated sentinel detection (CONTINUE/HALT never recognized), and (c) potentially spurious verdict matching on QA steps. All three failures are *silent at the parser* and *visible only as downstream gate misbehavior*, which is exactly the symptom profile of the production incident.

**Latent variants in adjacent code:**

The `_resolve_step_content` function at executor.py:293 has its own fallback-to-ndjson on disk-search miss. That fallback consumes whatever F-10 returned, so the two fallbacks chain: F-10 fallback → `_resolve_step_content` fallback → gate sees raw NDJSON. Removing F-10's silent fallback (e.g., raising on no-text-blocks) would force the caller to also stop pretending an empty extraction is "extracted text", which would surface as a clean status code at the gate layer.

**Class-of-defect verdict:** The defect is the *combination* of three silent-swallow conditions plus a fallback that produces a structurally-valid-but-semantically-wrong result. Fixing only the fallback (return `""` instead of `raw`) is a partial fix that still loses the diagnostic for "malformed under load" and "no text blocks" cases — but is the highest-leverage single change because it converts the F-04 silent-corruption profile back into a loud-fail profile, making the next dispatch-miss visible.

Blast radius: **HIGH** as the *concealment layer* for the entire F-01/F-04 family. Standalone blast radius is **MEDIUM** (one parser, one caller). Combined effective severity is dominated by the concealment role. Confidence: **HIGH**.

---

## Persona 3 — Architect (sonnet, depth=standard) — focus: severity calibration

**Preliminary severity: HIGH. Is that right? Should it match F-01's CRITICAL?**

The calibration question is whether F-10 is "the actual mechanism of the production halt" co-equal with F-01, or a contributing factor one rung below.

**Mechanism analysis:** The production halt requires *both* F-01 (dispatch table miss) *and* F-10 (silent fallback emitting raw NDJSON). Either fix alone changes the symptom:

- Fix F-01 only → `_resolve_step_content` reads the on-disk task file via the rglob search → gate sees real content → passes. F-10's fallback never fires for `build-task-file`. The pipeline runs to completion. The production halt does not recur.
- Fix F-10 only (return `""` instead of `raw`) → `_resolve_step_content` still falls through on dispatch miss → `gate_content = ""` → gate fails with "Min lines: 0/400" instead of "30/400". The pipeline still halts at step 7, but the error message now plainly says "no content extracted" instead of fingerprinting NDJSON envelope counts. The halt is *louder and faster to diagnose* but still a halt.

So F-01 is the *necessary* defect; F-10 is the *concealment* defect. Without F-01 the user sees no halt; without F-10 the user sees a halt with a much more informative error. This means F-01 is the genuine release-blocker for the headline functionality, and F-10 is the genuine release-blocker for *the next dispatch miss to be loud*.

**Severity ladder mapping:**

- CRITICAL = default path of primary feature halts, no workaround. → F-01 fits.
- HIGH = default path breaks but a workaround/diagnosis exists, OR breakage is confined to a non-primary feature, OR the defect *enables* CRITICAL defects to ship undetected.

F-10 fits the third HIGH criterion squarely: it is the mechanism that allowed F-01 to escape pre-release testing. The e2e test fixture at `test_e2e.py:245-247` writes raw markdown into the stream file; F-10's `raw`-fallback returns that markdown verbatim, satisfying the gate. The test passes. F-01 ships. F-10 is the *test-defeating* mechanism, which is structurally CRITICAL for the test suite's integrity but not directly for the user-visible artifact.

**Should it move to CRITICAL alongside F-01?**

Argument for: F-10 enables every F-04 step to silently mis-evaluate; the concealment scope across the 13 steps is arguably greater than the single F-01 halt. Argument against: standalone, with F-01/F-04 fixed, F-10 reduces to "parser swallows errors silently, fix to add logging" — clearly HIGH, not CRITICAL. The defect is dependent on a co-defect to cause user-visible harm.

The principled call: **HIGH confirmed**, with explicit note that F-10's *severity is contingent* — it would be CRITICAL if F-01/F-04 were not separately tracked, because in that counterfactual it would be the proximate cause of silent corruption across 13 steps. Since the audit *does* track F-01 and F-04 separately at CRITICAL, F-10 sits at HIGH as the concealment layer.

**Fix difficulty:** XS (≤30 min). Replace `return "\n".join(texts) if texts else raw` at executor.py:130 with: (i) return `"\n".join(texts)` unconditionally (let empty extractions be empty), (ii) emit a diagnostic when `texts` is empty AND `raw` was non-empty (record "no text blocks extracted from N NDJSON events" — actionable telemetry), and (iii) optionally promote `json.JSONDecodeError` and "no content list" cases to counters so silent swallows become observable. Tests: add a fixture where stream contains only `tool_use` blocks and assert the extracted text is empty (not the raw blob); add a fixture with malformed line and assert it is logged.

**Severity verdict: HIGH confirmed.** No upgrade to CRITICAL — F-01/F-04 already capture the user-visible halt severity; F-10 captures the concealment-mechanism severity, which is correctly one rung below the proximate cause it concealed.

---

## Convergence

- **Verdict**: REAL
- **Convergence score**: 0.95 — All three personas independently confirmed the defect and its role in the production incident. Analyzer confirmed mechanical reproducibility of the no-text-blocks arm as the unique source of the "30/400" symptom. Refactorer confirmed F-10 is the concealment layer that allowed F-01/F-04 to ship and that the fallback also defeats sentinel detection and warps QA verdict scanning. Architect confirmed HIGH severity is correctly calibrated relative to F-01/F-04 (CRITICAL) rather than co-equal — F-10 is a *necessary contributor* but not the *proximate cause*. The only split is the Architect's calibration debate, which resolved to HIGH with explicit conditional reasoning (would be CRITICAL absent F-01/F-04).
- **Final severity (post-adjudication)**: HIGH
- **Fix difficulty**: XS (≤30 min) for the surface fix: change executor.py:130 to return `"\n".join(texts)` unconditionally (no raw fallback), plus add a diagnostic emission when extraction yields zero text blocks from a non-empty stream. Realistically S (≤2h) once regression tests are added covering (a) tool_use-only stream → empty extraction, (b) malformed line → logged not swallowed, (c) all-malformed stream → empty extraction with diagnostic. Pair with F-01/F-04 fixes; the three together restore loud-fail semantics across the dispatch chain.

**Synthesis:** All three personas agree F-10 is a real defect that materially contributed to the production halt and that its primary harm is *concealment* of the F-01/F-04 dispatch-coherence defects. Evidence re-verification at executor.py:99-130 confirmed all three silent-swallow conditions and the fallback-to-raw return path verbatim. The production "30 NDJSON lines / 400 minimum" symptom is mechanically derivable only from this fallback firing — no other code path produces a string whose `splitlines()` length matches the NDJSON event count. Blast radius extends beyond gate evaluation to sentinel detection (executor.py:571, defeated when raw NDJSON is fed to anchored `^EXIT_RECOMMENDATION:` regex against JSON-escaped text) and QA verdict scanning (executor.py:578-582, which would substring-match `"verdict"` tokens inside raw envelopes). The e2e test fixture at `tests/cli/prd/test_e2e.py:245-247` is defeated by the same fallback — raw markdown written into the stream file is returned verbatim by F-10 because no line parses as JSON, so the gate passes against bypass content and the entire F-01/F-04 class is invisible to the test suite. Severity calibrates to HIGH rather than CRITICAL because F-01 is the proximate cause of the user-visible halt and F-10 is the concealment mechanism — fixing F-01 alone stops the halt; fixing F-10 alone makes the next halt loud. Both should be fixed together; the minimum F-10 fix (drop the `else raw` fallback, add a diagnostic on empty-extraction-from-nonempty-stream) is XS and converts the entire F-04 family from silent corruption back to loud failure.
