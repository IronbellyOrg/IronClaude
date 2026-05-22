# D-0082 — Evidence

## Cross-references verified

| Source | Path | Verified content |
|---|---|---|
| Hook manifest | `src/superclaude/hooks/hooks.json` | 6 hook events × 8 hook scripts × 4 matcher groups enumerated (verified 2026-05-20) |
| OQ-2 statement | `.dev/releases/current/cliEval/extraction.md:274` | "Concrete content of E3–E15 manifest entries (only E1 and E2 parameterize are shown in §5; spec defers full eval-body design)." |
| OQ-2 owner / target | `.dev/releases/current/cliEval/roadmap.md:110` | "RyanW \| before M1 exit (schema), before M5 entry (bodies)" |
| Roadmap rows R-086 … R-098 | `.dev/releases/current/cliEval/roadmap.md:293-305` | 13 rows confirm "body per OQ-2 resolution" + "content frozen post-OQ-2" + "deterministic AC". |
| Design-spec named cases | `.dev/releases/current/cliEval/design-spec.md:521` | E15: hook timeout fail-open (preserved verbatim in proposal). |
| D-4 callback escape | `.dev/releases/current/cliEval/decisions.md:130-135` | YAML `callback:` field example for E14 use confirmed. |
| D-5 coverage gate | `.dev/releases/current/cliEval/decisions.md:148-174` | Hook-matcher coverage gate falsifiable definition — proposal satisfies it by construction. |
| Phase-5 unblocked tasks | `.dev/releases/current/cliEval/phase-5-tasklist.md:301-1050` | T05.07–T05.21 each cite "Load OQ-2 resolution from T05.01 decision artifact." |

## Independent re-verification (zero-trust)

- Hook event count = 6 (`SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `SubagentStart`, `SubagentStop`) — confirmed by direct read of `src/superclaude/hooks/hooks.json:1-95`.
- PreToolUse matcher pattern = `Edit|Write|mcp__serena__replace_content|mcp__serena__replace_symbol_body|mcp__serena__insert_after_symbol|mcp__serena__insert_before_symbol` — line 37; covered by E6 (Edit), E7 (Write), E8 (serena, single matcher).
- PostToolUse matchers = 2 groups: `Read` (line 49) and `mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*` (line 60); E9 covers the first; E1/E2.1–3 cover the second.
- Capability-tag rollup `kept_plus_skipped_equals_n_prime`: under `--no-mcp`, 5 evals skip (E1, E2.1, E2.2, E2.3, E8), 12 run, parameterize expansion totals 17 — invariant preserved.

## Files created by this task

- `artifacts/D-0082/spec.md` — frozen body shapes (this proposal).
- `artifacts/D-0082/notes.md` — design decisions and alternatives.
- `artifacts/D-0082/evidence.md` — this file.
- `evidence/T05.01/oq-2-resolution-summary.md` — concise summary linking back to spec.md.

## Decisions.md update (on sign-off)

Upon sign-off, append the OQ-2 resolution block to `decisions.md` per the format used by D-9 (OPS-001) and D-10 (DOC-OQ4):
- Status: RESOLVED — 2026-05-20.
- Owner: RyanW.
- Impacts: T05.07 … T05.21 (13 tasks).
