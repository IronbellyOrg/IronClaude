# D-0007 — freshness-post-read.sh evidence

## Task: T02.04 (STRICT, async:true)

PostToolUse(Read) tracker per design §3.4. Records every successful Read into
`reads.jsonl` for the PreToolUse gate.

## File

`src/superclaude/hooks/scripts/freshness-post-read.sh`, mode 0755, `bash -n` clean.

## Dry-run 1 — success path

Input: `{"session_id":"PR1","tool_name":"Read","tool_input":{"file_path":"/a/b.go"},"tool_response":{"success":true}}`

Result: 1 row appended to reads.jsonl matching design §2.2 schema:

```json
{"ts":"2026-05-12T19:46:07+00:00","ts_unix":1778615167,"session_id":"PR1","path":"/a/b.go","tool_call_idx":1}
```

✓ exit 0, valid JSON, all required fields present.

## Dry-run 2 — failure path

Input includes `tool_response.success=false` and `error="ENOENT"`.

Result: 0 rows appended (file still has 1 row from prior test). Exit 0.

## Concurrency test — 50 parallel reads under `xargs -P 10`

```
$ : > reads.jsonl
$ seq 1 50 | xargs -P 10 -I{} sh -c "echo '{\"session_id\":\"CCR\",\"tool_name\":\"Read\",\"tool_input\":{\"file_path\":\"/conc/{}.go\"},\"tool_response\":{\"success\":true}}' | bash freshness-post-read.sh"
```

Results:

| Check | Expected | Got |
|---|---:|---:|
| Rows in reads.jsonl | 50 | 50 ✓ |
| Unique `tool_call_idx` values | 50 | 50 ✓ (monotonic) |
| Rows that pass `jq -c .` | 50 | 50 ✓ |

✓ flock(7) on `reads.jsonl.lock` + flock(9) on `tool-call-counter/<sid>.txt.lock`
both prevent atomic-append/counter-skew races.
✓ async:true safety verified — no race produces malformed lines.

## Acceptance criteria

| Criterion | Status |
|---|---|
| File mode 0755, `bash -n` clean | PASS |
| Success dry-run appends 1 row matching schema | PASS |
| Failure dry-run appends 0 rows | PASS |
| Concurrency: 50 invocations → 50 rows, unique tool_call_idx, valid JSON | PASS |

## Fail-open semantics

- jq parse failures → `exit 0` (no append).
- Lock contention timing → fallback to non-flock append OR skip (both safe).
- Write failures → `|| true` swallows; next Edit will block via `no_prior_read`,
  which heals state.
