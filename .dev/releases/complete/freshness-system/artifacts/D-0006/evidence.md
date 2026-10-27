# D-0006 — freshness-pre-edit.sh evidence

## Task: T02.03 (STRICT, Critical Path Override)

The enforcement layer. PreToolUse(Edit-class) freshness gate per design §3.3.

## File

`src/superclaude/hooks/scripts/freshness-pre-edit.sh`, mode 0755, `bash -n` clean.

## Dry-run table (4 branches)

| # | Scenario | Setup | Expected | Got | Stderr |
|---|---|---|---|---:|---|
| 1 | `no_prior_read` | empty reads.jsonl, Edit /x/y/z.go | exit 2 | exit 2 | ✓ "You have not Read \`/x/y/z.go\` in this session. Read it before editing." |
| 2 | `read_too_old` | Read 3600s ago | exit 2 | exit 2 | ✓ "You last Read \`/x/y/old.go\` 3600s ago, beyond the 30-minute freshness horizon. Re-Read before editing." |
| 3 | `recent_read` (ALLOW) | Read 60s ago, no changes | exit 0 | exit 0 | (none) |
| 4 | `external_change` | Read 120s ago + change 30s ago | exit 2 | exit 2 | ✓ "\`/x/y/c.go\` was modified after your last Read (mtime change detected). Re-Read before editing." |

## Telemetry rows (FR-6 schema)

All 4 rows parse with `jq -c .` and conform to design §2.2 schema:

```jsonl
{"ts":"2026-05-12T19:45:49+00:00","event":"PreToolUse","tool":"Edit","path":"/x/y/z.go","session_id":"SE1","tool_call_idx":1,"recent_read_age_sec":null,"external_change_seen":false,"decision":"block","reason":"no_prior_read"}
{"ts":"2026-05-12T19:45:49+00:00","event":"PreToolUse","tool":"Edit","path":"/x/y/old.go","session_id":"SE2","tool_call_idx":1,"recent_read_age_sec":3600,"external_change_seen":false,"decision":"block","reason":"read_too_old"}
{"ts":"2026-05-12T19:45:49+00:00","event":"PreToolUse","tool":"Edit","path":"/x/y/r.go","session_id":"SE3","tool_call_idx":1,"recent_read_age_sec":60,"external_change_seen":false,"decision":"allow","reason":"recent_read"}
{"ts":"2026-05-12T19:45:49+00:00","event":"PreToolUse","tool":"Edit","path":"/x/y/c.go","session_id":"SE4","tool_call_idx":1,"recent_read_age_sec":120,"external_change_seen":true,"decision":"block","reason":"external_change"}
```

✓ All four `decision` and `reason` enum values exercised.
✓ `recent_read_age_sec` is `null` for `no_prior_read`, integer otherwise.
✓ `external_change_seen` boolean correctly tracks the `external_change` reason.

## Sub-agent verification points (per task spec)

| Item | Status |
|---|---|
| (a) Only exit 2 blocks | ✓ Source: exit 0 on allow, exit 2 on block, exit 0 on cannot-enforce variants. No exit 1 anywhere. |
| (b) Fail-open semantics | ✓ Missing reads.jsonl → branch handled (LAST_READ_TS_UNIX=0 → no_prior_read block, NOT silent allow). Missing changes.jsonl → branch skipped. cwd/relative_path absent → `exit 0` with warning to stderr. |
| (c) Factual stderr phrasing | ✓ Each branch's stderr message is factual ("You have not Read X", "You last Read X 3600s ago"), not imperative ("Always Re-Read"). Phrasing per Q3 resolution / CLAUDE.md guidance. |

## Acceptance criteria

| Criterion | Status |
|---|---|
| File mode 0755, `bash -n` clean | PASS |
| 4 dry-runs produce documented exit codes + stderr per design §3.3 | PASS |
| Telemetry rows match FR-6 schema (each `jq .` parses) | PASS |
| Critical Path Override: stricter verification applied | PASS |
