# F-33: Duplicated NDJSON parser between executor.py and monitor.py with divergent behavior

**Final severity (Stage 2 preliminary)**: LOW
**Pattern tags**: P1
**Identified by**: D-10
**File:line**: `src/superclaude/cli/prd/executor.py:99-130` and `src/superclaude/cli/prd/monitor.py:69-98`

## Evidence

Both files parse NDJSON line-by-line, both call `json.loads`, both silently swallow `JSONDecodeError`. The executor variant extracts `message.content[].text` to feed gates; the monitor variant extracts `step_id`/`agent_type`/`artifact`/`verdict`/`fix_cycle` for state.

## Trace

- Two parsers, two failure modes, two places to update when the stream-json schema evolves.
- Given F-11 (monitor unused), this is currently low-impact, but if monitor is ever wired up, the two parsers will drift.
- A schema change in the claude CLI (e.g. moving `text` from `message.content[].text` to `delta.text`) requires touching both files independently.

## Reproduction sketch

Schema change to claude's stream-json output. Executor breaks first; monitor breaks differently (or silently degrades).

## Confidence (aggregated)

0.65 -- Agent D identified the duplication. Low severity because monitor is currently dead code.

## Cross-agent corroboration

- **Agent D** identified the two NDJSON parsers and noted the divergence risk if monitor is ever wired up, compounding the maintenance surface.
