# F-18: Verdict literal matching brittle in executor and gate layers

**Final severity (Stage 2 preliminary)**: MEDIUM
**Pattern tags**: P4, P3
**Identified by**: A-9, B-8
**File:line**: `src/superclaude/cli/prd/executor.py:577-583`; `src/superclaude/cli/prd/gates.py:36-53, 239-241`

## Evidence

```python
# executor.py:577-583 -- substring match on output text
if "qa" in step_id or "review" in step_id:
    if '"verdict": "FAIL"' in output or "verdict: FAIL" in output:
        return PrdStepStatus.QA_FAIL
    if '"verdict": "PASS"' in output or "verdict: PASS" in output:
        return PrdStepStatus.PASS

# gates.py:43 -- JSON path is unanchored substring
md_match = re.search(
    r"(?:^|\n)\s*\*{0,2}[Vv]erdict\*{0,2}\s*:\s*(PASS|FAIL)",
    content,
)
# JSON path at line 43:
re.search(r'"verdict"\s*:\s*"(PASS|FAIL)"', content)
```

## Trace

**Executor layer** (A-9):
- `'"verdict": "FAIL"'` requires exactly one space after the colon. Compact JSON (`{"verdict":"FAIL"}`), different quoting, or capitalised keys all miss.
- A miss demotes QA failures to PASS_NO_SIGNAL (`is_success` returns True), so the QA fix cycle exits without spawning gap-fillers.

**Gate layer** (B-8):
- The JSON path (`re.search`) is an unanchored substring match anywhere in the document. If a QA report quotes an earlier verdict inside a fenced code block, the regex finds the quoted verdict rather than the current one.
- A report quoting `"verdict": "PASS"` in commentary but writing `**Final Verdict**: REJECTED` scores PASS by the check.

## Reproduction sketch

QA subprocess emits `{"verdict":"FAIL","reasons":[...]}` (compact JSON, no spaces after colon). Executor classifies as PASS_NO_SIGNAL; fix cycle terminates without spawning gap-fillers.

## Confidence (aggregated)

0.85 -- Both agents independently identified the brittleness. Agent A traced the cascade to PASS_NO_SIGNAL; Agent B traced the unanchored regex match.

## Cross-agent corroboration

- **Agent A** identified the executor's literal substring match and traced how a miss cascades to PASS_NO_SIGNAL, silently treating a failing QA step as passing.
- **Agent B** identified the gate's unanchored regex that can match verdicts embedded in commentary or code blocks, producing spurious PASS/FAIL results.
