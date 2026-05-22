# F-10: NDJSON extraction silently swallows errors and falls back to raw blob

**Final severity (Stage 2 preliminary)**: HIGH
**Pattern tags**: P4, P8
**Identified by**: A-10, D-4
**File:line**: `src/superclaude/cli/prd/executor.py:99-130`

## Evidence

```python
# executor.py:111-130
for line in raw.splitlines():
    line = line.strip()
    if not line:
        continue
    try:
        obj = json.loads(line)
    except (json.JSONDecodeError, ValueError):
        continue                          # silent swallow

    message = obj.get("message") or {}
    content = message.get("content")
    if not isinstance(content, list):
        continue                          # silent swallow
    for block in content:
        if isinstance(block, dict) and block.get("type") == "text":
            text = block.get("text", "")
            if text:
                texts.append(text)

return "\n".join(texts) if texts else raw   # silent fallback to raw NDJSON
```

## Trace

Three independent silent-swallow conditions, each capable of feeding the gate semantically wrong content:

1. **Malformed JSON** -> skipped, no log, no diagnostic. Partial-buffer truncated lines under load lose content with zero visibility.
2. **No text blocks** -> if output is mostly `tool_use` events (e.g., the subprocess used Write tool heavily), zero text blocks are extracted.
3. **Final fallback** -> if zero text blocks were extracted, returns the entire raw NDJSON blob. `splitlines()` then counts NDJSON envelope lines (one per event) as "content lines" -- exactly the failure mode that produced "30 lines" at build-task-file.

The fallback at line 130 is the most dangerous: the gate's `splitlines()` counts NDJSON envelope lines as content, inflating or deflating line counts unpredictably. A subprocess that emits 30 `tool_use` NDJSON envelopes and zero `text` blocks produces 30 "lines" of raw NDJSON, which is the exact production failure.

## Reproduction sketch

A subprocess emits 30 valid NDJSON envelopes with `type: "tool_use"` and zero `type: "text"` blocks. `_extract_text_from_stream_json` returns the entire raw NDJSON. `splitlines()` counts 30. Gate `min_lines=400` fails with the exact "30/400" message observed in production.

## Confidence (aggregated)

0.90 -- Both agents independently identified the fallback-to-raw branch as the mechanism behind the observed failure. Agent A traced the downstream gate consequence; Agent D traced the parser behavior in detail.

## Cross-agent corroboration

- **Agent A** identified the fallback behavior and its interaction with F-01: when there is no on-disk artifact AND the assistant emitted only tool_use blocks, gate evaluation runs against raw NDJSON, producing false line counts.
- **Agent D** traced the three silent-swallow conditions in detail and confirmed this is the exact failure-mode mapping to the "30 lines" production incident.
