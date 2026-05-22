# F-18 Adjudication: Verdict literal matching brittle

**Mode**: B (single-finding, three-persona convergence)
**Finding**: `.dev/eval-workspaces/prd-cli-audit/findings/F-18-verdict-literal-matching-brittle.md`
**Re-verified against**: `src/superclaude/cli/prd/executor.py:577-585`, `src/superclaude/cli/prd/gates.py:36-53, 239-241`, `src/superclaude/cli/prd/monitor.py:32-36`, `src/superclaude/cli/prd/models.py:120-160`, `src/superclaude/cli/prd/prompts.py:297, 439`

---

## Re-verification

### Executor literal matcher (the brittle one)

```python
# src/superclaude/cli/prd/executor.py:577-585
# QA steps: check for verdict
if "qa" in step_id or "review" in step_id:
    if '"verdict": "FAIL"' in output or "verdict: FAIL" in output:
        return PrdStepStatus.QA_FAIL
    if '"verdict": "PASS"' in output or "verdict: PASS" in output:
        return PrdStepStatus.PASS

# No sentinel found -- pass with caveat
return PrdStepStatus.PASS_NO_SIGNAL
```

This is a Python `in` substring test on two literal strings. Every char (quote glyph, single space, colon-space spacing, casing of `PASS`/`FAIL`, `verdict` lower-case) must match exactly. **It accepts only:**

1. `"verdict": "FAIL"` (JSON with a single space after the colon, double-quoted, lowercase key)
2. `verdict: FAIL` (markdown style, single space, lowercase key, ALLCAPS verdict)

### Gate regex (the tolerant one)

```python
# src/superclaude/cli/prd/gates.py:36-53
def _check_verdict_field(content: str) -> bool | str:
    # JSON format
    json_match = re.search(r'"verdict"\s*:\s*"(PASS|FAIL)"', content)
    if json_match:
        return True
    # Markdown format (case-insensitive key, case-sensitive value)
    md_match = re.search(
        r"(?:^|\n)\s*\*{0,2}[Vv]erdict\*{0,2}\s*:\s*(PASS|FAIL)",
        content,
    )
    if md_match:
        return True
    return "No verdict field found ..."
```

Tolerant to whitespace via `\s*`, but unanchored (`re.search`) and `_check_qa_verdict` (`gates.py:239-241`) is a thin wrapper that returns this verbatim. **Calling-site contract:** `_check_verdict_field` answers "does a verdict field exist?" not "what is the final verdict?" — it returns True as long as *any* `"verdict": "PASS"` or `"verdict": "FAIL"` substring appears anywhere in the document.

### Cascade confirmation

`PrdStepStatus.is_success` (`models.py:120-130`) returns True for both `PASS` *and* `PASS_NO_SIGNAL`. `_run_qa_fix_cycle` (`executor.py:854`) exits the fix-cycle loop on `qa_result.status.is_success`. Therefore:

**A missed QA FAIL in `executor.py:579` → falls through to `PASS_NO_SIGNAL` (line 585) → `is_success == True` → fix cycle terminates after the first QA pass that wasn't actually a pass.**

This is the cascade the finding describes; it is real.

---

## Analyzer persona — reproducibility

**Formats the executor matcher REJECTS (each of these silently demotes a real QA FAIL to `PASS_NO_SIGNAL`):**

| Input emitted by QA subprocess | Matched? | Why |
|---|---|---|
| `{"verdict": "FAIL"}` | Yes | canonical |
| `{"verdict":"FAIL"}` (compact JSON, no space after colon) | **No** | requires one space |
| `{"verdict":  "FAIL"}` (two spaces, pretty-printer) | **No** | requires exactly one space |
| `{"verdict" : "FAIL"}` (space before colon) | **No** | matcher requires `"verdict":` |
| `{'verdict': 'FAIL'}` (single quotes, e.g. Python repr) | **No** | matcher uses double quotes |
| `{"Verdict": "FAIL"}` (capitalised key) | **No** | matcher is case-sensitive on key |
| `{"verdict": "fail"}` (lowercase verdict value) | **No** | matcher requires `FAIL` upper |
| `**Verdict**: FAIL` (markdown bold) | **No** | matcher has no `**` allowance |
| `verdict:FAIL` (no space) | **No** | matcher requires `verdict: FAIL` with space |
| `Verdict: FAIL` (capitalised md key) | **No** | matcher is case-sensitive |
| `"final_verdict": "FAIL"` (different key name) | **No** | matcher hardcodes key |

The most likely real-world failure mode is **compact JSON**: `json.dumps(obj)` with no `indent=` argument emits `{"verdict":"FAIL"}` — zero spaces. Any QA subprocess that uses default `json.dumps` defeats the matcher.

**Reproduction is trivial:** any Python QA subprocess that does `print(json.dumps({"verdict": "FAIL", "reasons": [...]}))` (no `indent`) produces a string the executor cannot detect.

**Gate-layer (gates.py:43) bug is separate but real:** because `re.search` is unanchored and matches anywhere in the document, a QA report that *quotes* a prior `"verdict": "PASS"` in commentary or a fenced code block satisfies `_check_verdict_field` even if the actual final verdict is `**Final Verdict**: REJECTED`. The first match wins; first-document-order — not last — wins.

---

## Refactorer persona — blast radius

Sweep across `src/superclaude/cli/` for verdict matchers:

| Location | Pattern | Tolerant? | Notes |
|---|---|---|---|
| `prd/executor.py:579-581` | literal `in` | **Brittle** | The bug |
| `prd/gates.py:43, 47-50` | regex with `\s*` | Tolerant | But unanchored; first-match-wins |
| `prd/gates.py:239-241` | wraps `_check_verdict_field` | Inherits | Same unanchored issue |
| `prd/monitor.py:33-36` | regex with `\s*` | Tolerant | Correct pattern |
| `prd/prompts.py:297, 439` | prompt template | n/a | Instructs canonical `"verdict": "PASS" or "FAIL"` — *mitigation*, not enforcement |
| `prd/filtering.py:149, 170` | emits dict, not matches | n/a | producer side |

**Key finding:** the codebase already has a tolerant pattern (`monitor.py:33`, `gates.py:43`). The brittle matcher in `executor.py:579-581` is the **outlier** — it duplicates intent without reusing the existing regex. Three independent places define essentially the same regex; the one that diverges to literal substring is the one that decides the fix-cycle outcome.

**Mitigating factor:** `prompts.py:297, 439` instruct the QA model to emit `"verdict": "PASS" or "FAIL"` — the canonical-spaced format the executor accepts. So in the happy path the prompt and matcher are aligned. But:

1. Prompt compliance is not enforced; LLM output drift (compact JSON, alternate casing, markdown rendering) will defeat the matcher silently.
2. Any QA step that wraps the model output through a JSON serializer (e.g., a subprocess that re-emits a parsed dict via `json.dumps`) drops the space.
3. Future contributors writing new QA-style steps may not know the exact-spacing requirement.

**No additional brittle literal matchers found in `src/superclaude/cli/`** — the bug is localized to one ~5-line block in `executor.py`. Blast radius is bounded but the *single* affected matcher is in the critical fix-cycle decision path.

---

## Architect persona — severity calibration

**Preliminary: MEDIUM.** Calibration check:

Impact arguments for retaining or raising MEDIUM:
- The matcher gates the QA fix-cycle decision. A miss does not just lose telemetry — it terminates the cycle as if QA passed. Silent quality regressions ship.
- `PASS_NO_SIGNAL.is_success == True` (`models.py:125`) is the amplifier: there is no "I don't know" path. Ambiguity is resolved toward shipping.
- The trigger (compact JSON) is not hypothetical — it is the default behavior of `json.dumps`.
- Diagnostic categorization (`diagnostics.py:157-160`) only flags `QA_FAIL`, so the diagnostic layer cannot recover what the executor misclassified.

Impact arguments for lowering to LOW:
- The prompt explicitly specifies the canonical format the matcher requires (`prompts.py:297, 439`), so in the **expected** path matcher and producer agree.
- The brittle matcher is one block in one file; the rest of the verdict-handling code is tolerant.
- A correct QA FAIL does still get classified as `QA_FAIL` when the model complies with the prompt — i.e., this is a robustness gap, not a guaranteed misclassification.

**Calibration: keep MEDIUM.** It is not HIGH because (a) the prompt steers the LLM toward the matched format and (b) the blast radius is one file. It is not LOW because the failure mode is silent, the cascade lands on a critical control-flow decision (fix-cycle exit), and the trigger (compact JSON output) is plausible enough that any QA-tool refactor or subprocess change could expose it.

---

## Convergence

**Verdict: VALID — confirmed both layers, but only the executor literal matcher (`executor.py:579-581`) is high-impact; the gate-layer unanchored-search issue (`gates.py:43`) is a real secondary concern but lower severity (gate semantic checks are advisory; executor classification is decisional).**

**Convergence score: 0.92.** All three personas independently confirm:
1. The executor literal matcher silently misclassifies (Analyzer).
2. No other brittle matchers in `cli/`; the bug is a single outlier diverging from existing tolerant patterns (Refactorer).
3. The cascade through `PASS_NO_SIGNAL.is_success == True` makes the silent miss decisional, not advisory (Architect).

Slight divergence: whether prompt-steering (`prompts.py:297, 439`) is sufficient mitigation. Architect treats it as a mitigation that prevents HIGH; Analyzer treats it as an unenforced contract that does not justify lowering severity. Convergence resolves at MEDIUM.

**Final severity: MEDIUM** (confirmed from preliminary).

**Fix difficulty: LOW** — replace the literal `in` substring test in `executor.py:579-581` with the existing tolerant regex (`monitor.py:33-36` is already a drop-in or can be lifted into a shared helper). For the gate layer, change `re.search` to scan-and-take-last-match or anchor to a "Final Verdict" section header. Estimated 10-30 lines + tests.

**Synthesis:**

The finding is reproducible: any QA subprocess emitting compact JSON (`json.dumps` without `indent=`) silently demotes `QA_FAIL` to `PASS_NO_SIGNAL`, and because `PASS_NO_SIGNAL.is_success == True` (`models.py:125`), the fix-cycle loop in `executor.py:854` exits without spawning gap-fillers. The gate-layer regex in `gates.py:43` is unanchored and first-match-wins, so a report quoting a prior `"verdict": "PASS"` in commentary passes the semantic check regardless of the final verdict.

Blast radius is **one file (executor.py) for the high-impact matcher, plus one helper (gates._check_verdict_field) for the secondary issue**. Three other call-sites (`monitor.py:33`, the markdown branch in `gates.py:47`) already use the tolerant pattern, so the fix is to consolidate to the existing tolerant form, not invent new parsing.

Severity is MEDIUM because the prompt template (`prompts.py:297, 439`) steers the LLM toward the matched format — this is the only thing keeping the bug latent. It will not stay latent: any refactor that re-serializes QA output through `json.dumps`, any prompt-template drift, or any new QA-style step author who doesn't know the exact-spacing requirement reactivates the silent-miss cascade.

**Recommended remediation (informational, READ-ONLY adjudication):**
1. Extract `_QA_VERDICT_JSON_PATTERN` / `_QA_VERDICT_MD_PATTERN` from `monitor.py:33-36` into a shared module (e.g., `prd/verdict.py`) with a function `extract_final_verdict(output: str) -> Literal["PASS", "FAIL"] | None` that scans for the *last* verdict occurrence (rfind semantics) and returns `None` when nothing matches.
2. Replace the literal block in `executor.py:579-581` with the shared extractor.
3. Replace `gates._check_verdict_field` to use the same extractor (and to scan for the last verdict, not the first).
4. Add unit tests covering: compact JSON, pretty-printed JSON with 2-space and 4-space indent, single-quoted Python repr, `**Verdict**: FAIL` markdown, lowercase `fail`, capitalised key, and a report that *quotes* a prior verdict followed by a contradicting final verdict.

---

## Citations

- `src/superclaude/cli/prd/executor.py:577-585` — brittle literal matcher and `PASS_NO_SIGNAL` fall-through
- `src/superclaude/cli/prd/executor.py:854` — fix-cycle exit on `is_success`
- `src/superclaude/cli/prd/gates.py:36-53` — `_check_verdict_field` (tolerant regex but unanchored)
- `src/superclaude/cli/prd/gates.py:239-241` — `_check_qa_verdict` wrapper
- `src/superclaude/cli/prd/models.py:120-130` — `PrdStepStatus.is_success` includes `PASS_NO_SIGNAL`
- `src/superclaude/cli/prd/monitor.py:32-36` — existing tolerant regex (the consolidation target)
- `src/superclaude/cli/prd/prompts.py:297, 439` — prompt-side canonical-format instruction (mitigation, not enforcement)
- `src/superclaude/cli/prd/diagnostics.py:157-160` — diagnostic categorization only flags explicit `QA_FAIL`, cannot recover misclassification
