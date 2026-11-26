# Hook decision: what `run-create` gives a PostToolUse hook

## Authority
The owner's brief to this agent orders this test in these words: "first test what such a hook actually receives from run-create". The plan (Task 8) quotes that sentence as its authority for creating exactly one scratch Run.

## Scratch Runs created
Number of scratch Runs created: 1 (id `run_e97be8837462`, objective "scratch Run for the run-ledger hook payload test, safe to ignore", created 2026-11-26T18:38:33Z). Orca has no Run delete, so this Run stays in Orca for good. No Run was deleted and `orca orchestration reset` was not run. `run-list` had 64 Runs before and 65 after.

## Captured output of `orca orchestration run-create ... --json`
Saved byte for byte as `tests/run_ledger/fixtures/run_create_stdout.json`. Exit code 0, stderr empty. The stdout is one JSON object `{"id", "ok": true, "result": {"run": {"id": "run_e97be8837462", ...}, "mutation": {...}}, "_meta": {...}}`.

A `run_[0-9a-f]{12}` id IS in the output (`result.run.id`, and nowhere else in the object).

## Side effect seen
`orca orchestration run-current` printed "No Run is bound to this terminal." before the call and `run_e97be8837462 scratch Run for the run-ledger hook payload test, safe to ignore` after it: `run-create` binds the calling terminal to the new Run. (The sweep acceptance run of Task 11 must therefore use a terminal where the binding lookup fails.)

## Payload shape source
Claude Code hooks reference, https://code.claude.com/docs/en/hooks (read 2026-11-26): a PostToolUse command hook gets JSON on stdin with `session_id`, `transcript_path`, `cwd`, `permission_mode`, `hook_event_name: "PostToolUse"`, `tool_name`, `tool_input` (for Bash: `command`, `description`, ...), `tool_response` and `tool_use_id`. The page documents the Bash result keys as `stdout`, `stderr`, `interrupted` and `isImage` (in the PostToolUse decision-control section, as the shape of `updatedToolOutput`). The page has no full Bash PostToolUse input example (its only PostToolUse input example is for the Write tool), so the exact `tool_response` of a real Bash call was not captured from a live hook: `tests/run_ledger/fixtures/posttooluse_run_create.json` is built from the documented keys, wrapping the real captured stdout in `tool_response.stdout`. Status of the wrapper shape: documented keys, not live-captured. The hook script must also accept a `tool_response` that is a plain string or an object (the plan's Task 9 already requires that).

## Decision
The captured output holds a Run id, so the hook is delivered.

Decision: deliver
