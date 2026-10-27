# D-0075 — FR-G5 hook-matcher coverage gate

**Task:** T04.14 (Phase 4, Roadmap FR-G5 / R-075)
**Module:** `src/superclaude/cli/eval/coverage.py`
**CLI surface:**
  * `superclaude eval doctor --check-coverage [--suite <name>]`
  * `superclaude eval run --suite <name> [...]` (gate runs implicitly at top-of-run)
**Status:** Implemented 2026-05-20

## Why the gate exists

Bug PR #49 silently regressed because a hook matcher pattern broke and
no eval issued a tool call that would have noticed. Design-spec §1.5
documents the falsifiable rule: for every matcher pattern `P` in
`~/.claude/settings.json`, at least one eval in the suite under test
MUST issue a real tool call whose name matches `P`. The gate enforces
that rule at the CLI boundary.

## Public surface

| Name | Kind | Purpose |
|---|---|---|
| `coverage_gate(settings_path, suite, *, output_dir, matcher_filter)` | function | CLI entry. Returns a `CoverageResult`. |
| `CoverageResult` | dataclass | Outcome record (`passed`, `matchers`, `covered`, `missing`, `artifacts`, `coverage_map`). |
| `CoverageMatcher` | dataclass | `(event, pattern)` pair from `settings.json`. |
| `eval_covers_pattern(spec, pattern)` | function | Tag-based registry rule (regex `.search` against `inputs[].expect_tool_call`). |
| `extract_hook_matchers(settings)` | function | Pure parser over a parsed `settings.json` mapping. |
| `default_matcher_filter(pattern)` | function | v1 scope predicate — accepts patterns mentioning one of the three known MCP tool prefixes. |
| `sanitize_pattern_for_filename(pattern)` | function | Replaces filesystem-unsafe characters with `_`. |
| `COVERAGE_GATE_FAILED_EXIT_CODE` | int | `2` — pins design-spec §4 harness-rejection contract. |
| `COVERAGE_MISSING_ARTIFACT_PREFIX` | str | `"coverage_missing:"` — filename prefix written on a breach. |

## Matcher → eval mapping rule (registry derivation)

The gate derives the matcher → covering-eval registry on the fly from
each eval's manifest. The rule:

> For each `CoverageMatcher(event, pattern)` and each `EvalSpec spec`
> in `suite`, `eval_covers_pattern(spec, pattern)` returns `True` iff
> `re.compile(pattern).search(tc)` returns a match for some
> `tc = row["expect_tool_call"]` where `row` is one of the entries in
> `spec.inputs`.

Rationale: `expect_tool_call` is already declared on every eval input
that asserts MCP tool invocation; reusing that field as the coverage
signal avoids a parallel `provides:` registry that would drift.

An unparseable matcher pattern is treated as `covered=False` for every
eval (rather than raising). The pattern still appears in `missing` so
the operator notices it.

## v1 scope (`default_matcher_filter`)

The v1 gate only checks matchers that mention one of:

* `mcp__auggie__`
* `mcp__auggie-mcp__`
* `mcp__airis-mcp-gateway__`

Other matchers (`Edit|Write`, `mcp__serena__replace_content...`) are
bookkeeping hooks that no eval needs to issue a tool call for; they are
out of scope for v1. T05.25 widens the predicate as additional MCP tool
families come online.

## Wiring

### `eval doctor --check-coverage`

* Reads `~/.claude/settings.json`. Missing/unreadable → empty matcher
  set → gate passes (the doctor stays green on a clean dev host).
* `--suite <name>` is optional. When supplied, the suite is loaded via
  `SuiteLoader` and the gate resolves covering evals; when omitted, the
  gate runs in matchers-only mode (every matcher reports as uncovered
  because there are no evals to map against).
* On `--json`, the `coverage_gate` marker in the payload carries the
  full `CoverageResult.to_dict()` payload under `result`. Status is one
  of `skipped` (not requested), `passed`, or `failed`.
* On failure: stderr roster + exit `COVERAGE_GATE_FAILED_EXIT_CODE` (2).

### `eval run`

* Runs at the TOP of the run, AFTER suite parse + post-expansion filter
  and BEFORE any worker dispatch. A breach short-circuits the run
  without touching a per-eval HOME.
* Artifacts (`coverage_missing:<sanitised-pattern>`) land inside the
  resolved `--output-dir` so the FR-G4 run directory contains the full
  forensic trail.

## Artifact contract

For every uncovered matcher pattern `P`, the gate writes a JSON file
named `coverage_missing:<sanitize_pattern_for_filename(P)>` to
`output_dir` with the payload:

```json
{
  "coverage_missing": true,
  "covered_by": [],
  "event": "<hook event name>",
  "pattern": "<matcher pattern, verbatim>",
  "settings_source": "<absolute path to settings.json>"
}
```

A `grep -l '^coverage_missing:' <run-dir>` surfaces every breach in
deterministic order.

## Exit codes

| Code | Cause |
|---|---|
| `0` | every checked matcher has a covering eval (or empty matcher set) |
| `2` | at least one matcher has no covering eval — `COVERAGE_GATE_FAILED_EXIT_CODE` |

Doctor maps the same `2` to HARD-failure semantics; `eval run` maps it
to "harness rejection" per design-spec §4.

## Validation (T04.14 AC)

* "Stub a settings.json with a 4th matcher and confirm gate fails" —
  covered by `test_coverage_gate_fails_when_fourth_matcher_added_without_eval`.
* CLI integration — covered by
  `test_cli_doctor_check_coverage_fails_when_uncovered_matcher_present`
  and `test_cli_doctor_check_coverage_json_payload_carries_missing_list`.
* Default filter scoping — covered by
  `test_coverage_gate_default_filter_skips_non_mcp_matchers`.
* Full coverage validation against the real `~/.claude/settings.json`
  is deferred to M5 T05.25 per the phase-4 tasklist note.

## Open M5 follow-ups (T05.25)

* Extend `default_matcher_filter` to cover additional MCP tool families
  as they ship.
* Run the gate against the real suite + the real settings.json in CI as
  a smoke test, not just synthetic stubs.
* Add a `provides:` field to `EvalSpec` as a complement to
  `expect_tool_call` for evals that prove tool-call coverage without
  asserting on the call result.
