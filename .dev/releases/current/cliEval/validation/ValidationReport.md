# Validation Report

Generated: 2026-05-19
Roadmap: `/config/workspace/IronClaude/.dev/releases/current/cliEval/roadmap.md`
Phases validated: 6
Agents spawned: 12
Total findings: 26 (High: 0, Medium: 10, Low: 16)

## Findings

### High Severity

(none)

### Medium Severity

#### M1. T01.01 EvalConfig OQ-8 gating omission

- **Severity**: Medium
- **Affects**: phase-1-tasklist.md / T01.01
- **Problem**: Roadmap M1 Open Questions table lists OQ-8 (`CLAUDE_FAKE_TIME_OFFSET` consumption) with resolution target "before COMP-005 close". T01.01 does not gate on OQ-8 nor mention `time_offset` in EvalConfig.
- **Roadmap evidence**: `roadmap.md` Open Questions M1 table — `OQ-8 | How CLAUDE_FAKE_TIME_OFFSET is consumed or validated | ... | before COMP-005 close`.
- **Tasklist evidence**: phase-1-tasklist.md T01.01 Steps mention only EvalConfig fields; Notes say "Default scratch roots align with AC12".
- **Exact fix**: Add Step 2.5 "Confirm OQ-8 resolution status (DOC-OQ8 T06.03) or record deferral in spec.md". Add Notes line: "OQ-8 (CLAUDE_FAKE_TIME_OFFSET) resolution required before close; deferral acceptable per T06.03 decision."

#### M2. T01.07 SuiteLoader missing COMP-010 dependency

- **Severity**: Medium
- **Affects**: phase-1-tasklist.md / T01.07
- **Problem**: Roadmap COMP-002 lists `Deps | FR-SCH2, COMP-010`. T01.07 Dependencies declares only `T01.04, T01.05`, omitting T01.14 (COMP-010 DSL interface).
- **Roadmap evidence**: `roadmap.md` M1 table — `COMP-002 SuiteLoader | ... | Deps | FR-SCH2,COMP-010`.
- **Tasklist evidence**: phase-1-tasklist.md T01.07 — `Dependencies: T01.04, T01.05`.
- **Exact fix**: Change `Dependencies: T01.04, T01.05` to `Dependencies: T01.04, T01.05, T01.14`.

#### M3. T01.14 COMP-010 missing synthetic-EvalContext exercise

- **Severity**: Medium
- **Affects**: phase-1-tasklist.md / T01.14
- **Problem**: M1 Exit criteria require DSL interface "importable AND exercised by unit tests against synthetic `EvalContext`". T01.14 AC only requires stubs returning `NotImplementedError("M4")`; no synthetic-EvalContext exercise.
- **Roadmap evidence**: `roadmap.md` M1 Exit line — "DSL interface (COMP-010) is importable and exercised by unit tests against synthetic `EvalContext`".
- **Tasklist evidence**: phase-1-tasklist.md T01.14 AC — "Each method returns an `ExpectCallable` stub raising `NotImplementedError("M4")`".
- **Exact fix**: Add AC bullet: "Unit tests instantiate `Expect` and exercise each method against a synthetic `EvalContext` fixture, asserting the stub `NotImplementedError("M4")` is raised consistently (per M1 exit criterion)."

#### M4. T01.15 ExpectResult invented ValueError invariant

- **Severity**: Medium
- **Affects**: phase-1-tasklist.md / T01.15
- **Problem**: T01.15 AC requires constructing with `passed=False, failure=None` to raise `ValueError`. Roadmap DM-009 declares `failure:Optional[ExpectFailure]` with no required-when-failed clause.
- **Roadmap evidence**: `roadmap.md` M1 table — `DM-009 ExpectResult record | ... | fields:name,passed:bool,message,details,duration_sec,failure:Optional[ExpectFailure];serializable`.
- **Tasklist evidence**: phase-1-tasklist.md T01.15 AC bullet 3 — "Constructing with `passed=False` and `failure=None` raises `ValueError` (failure detail required on failure)."
- **Exact fix**: Remove the ValueError AC bullet. Replace with: "Construction with valid field types succeeds; `failure` is Optional per DM-009 (no required-when-failed coupling)."

#### M5. T01.20 AC11 invented CLAUDE.md documentation requirement

- **Severity**: Medium
- **Affects**: phase-1-tasklist.md / T01.20
- **Problem**: AC adds "Documentation in CLAUDE.md references the gate." Roadmap AC11 requires only `make verify-sync passes; pre-commit hook rejects edits to .claude/ without sync-back`.
- **Roadmap evidence**: `roadmap.md` M1 table — `AC11 ... make verify-sync passes; pre-commit hook rejects edits to .claude/ without sync-back`.
- **Tasklist evidence**: phase-1-tasklist.md T01.20 AC bullet 3 — "Documentation in `CLAUDE.md` references the gate."
- **Exact fix**: Remove the CLAUDE.md AC bullet, or relocate to **Notes** as a non-binding suggestion.

#### M6. T01.23 TEST-001 omits exit-code-2 + parameterize expansion explicit

- **Severity**: Medium
- **Affects**: phase-1-tasklist.md / T01.23
- **Problem**: Roadmap TEST-001 AC names "invalid schema exits 2; unsafe id exits 2; parameterize expansion tested". T01.23 ACs mention preflight ordering and the cases at a generic level but do not require explicit exit-code-2 assertions, and "parameterize expansion" is narrowed to "parameterized-unsafe rejection".
- **Roadmap evidence**: `roadmap.md` M1 table — `TEST-001 | ... | invalid schema exits 2; unsafe id exits 2; no FS writes before rejection; parameterize expansion tested; cross-links NFR-SEC1`.
- **Tasklist evidence**: phase-1-tasklist.md T01.23 ACs cover schema-violation/unsafe-id/parameterized-unsafe/pre-flight ordering but do not require explicit exit-2 assertion or generic parameterize-expansion coverage.
- **Exact fix**: Add AC bullet: "Tests assert process exit code 2 on schema-violation and unsafe-id rejection paths." Replace "parameterized-unsafe rejection" wording with "parameterize expansion validated post-expansion (both safe and unsafe expansion cases)."

#### M7. T02.14 COMP-014 omits error-tag + verbatim hooks.json ACs

- **Severity**: Medium
- **Affects**: phase-2-tasklist.md / T02.14
- **Problem**: Roadmap COMP-014 AC mandates `errors tagged; hooks.json deployed verbatim into per-eval HOME`. T02.14 AC omits both (a) error-tag propagation and (b) byte-identical hooks.json assertion.
- **Roadmap evidence**: `roadmap.md` M2 table — `COMP-014 | ... | adapter signature matches install_hooks; targets per-eval HOME path; idempotent; no direct real-HOME writes; errors tagged; hooks.json deployed verbatim into per-eval HOME`.
- **Tasklist evidence**: phase-2-tasklist.md T02.14 ACs cover signature, idempotency, no-real-HOME writes — omit errors-tagged and verbatim-hooks.json.
- **Exact fix**: Append two AC bullets: (a) "Adapter raises `HookDeployFailed` with an `error_tag` propagated to `EvalRunner.outcome.artifacts` on `install_hooks` failure." (b) "`<home_path>/.claude/hooks.json` is byte-identical to `src/superclaude/hooks/hooks.json` (SHA256 equality assertion in adapter test)."

#### M8. T03.03 EvalContext field count off-by-one (14 vs 15)

- **Severity**: Medium
- **Affects**: phase-3-tasklist.md / T03.03
- **Problem**: Roadmap DM-010 enumerates 15 fields. T03.03 Deliverables and AC say "14 fields".
- **Roadmap evidence**: `roadmap.md` M3 table — `DM-010 EvalContext runtime record | ... | fields:eval_spec,home,home_path,artifacts_dir,run_dir,env,stdout_path,stderr_path,transcript_path,jsonl_paths,exit_code,stdout,stderr,duration_sec,artifacts;immutable view` (15 fields).
- **Tasklist evidence**: phase-3-tasklist.md T03.03 — Deliverables: "with the 14 fields from DM-010"; AC: "exposes the 14 fields named in DM-010".
- **Exact fix**: Replace "14 fields" with "15 fields" in T03.03 Deliverables and Acceptance Criteria (both occurrences).

#### M9. T05.02-T05.05 MCP Requirements field malformed + missing real MCP server names

- **Severity**: Medium
- **Affects**: phase-5-tasklist.md / T05.02, T05.03, T05.04, T05.05
- **Problem**: (a) MCP Requirements cell uses literal pipe `None | Preferred: Sequential, Context7` which breaks 2-column markdown table parsing; (b) the value does NOT name the real MCP server each task invokes (E1 needs `mcp__auggie__`; E2.1 same; E2.2 needs `mcp__auggie-mcp__`; E2.3 needs `mcp__airis-mcp-gateway__`), contradicting the task body.
- **Roadmap evidence**: `roadmap.md` M5 — `R-082 ... inputs invoke real mcp__auggie__codebase-retrieval`; `R-083 ... real mcp__auggie__codebase-retrieval invocation`; `R-084 ... real mcp__auggie-mcp__ask_question invocation`; `R-085 ... real mcp__airis-mcp-gateway__auggie_search invocation`.
- **Tasklist evidence**: phase-5-tasklist.md `MCP Requirements | None | Preferred: Sequential, Context7 |` for T05.02-T05.05.
- **Exact fix**: For each of T05.02-T05.05, replace the malformed row with a single-pipe-cell value naming the required MCP server:
  - T05.02: `| MCP Requirements | Required: auggie (mcp__auggie__codebase-retrieval); Preferred: Sequential, Context7 |`
  - T05.03: same as T05.02 (E2.1 invokes same tool)
  - T05.04: `| MCP Requirements | Required: auggie-mcp (mcp__auggie-mcp__ask_question); Preferred: Sequential, Context7 |`
  - T05.05: `| MCP Requirements | Required: airis-mcp-gateway (mcp__airis-mcp-gateway__auggie_search); Preferred: Sequential, Context7 |`

#### M10. T05.27 MIG-002 omits eval-PR coverage-map reference AC

- **Severity**: Medium
- **Affects**: phase-5-tasklist.md / T05.27
- **Problem**: Roadmap MIG-002 AC requires `eval PRs reference coverage map`. T05.27 step 4 mentions adding "coverage-map reference per batch" but the Acceptance Criteria do not assert it as a load-bearing requirement.
- **Roadmap evidence**: `roadmap.md` M5 table — `MIG-002 | ... | 15 eval IDs tracked; batches of 3–5 defined; harness PR separable; eval PRs reference coverage map`.
- **Tasklist evidence**: phase-5-tasklist.md T05.27 AC bullets list batches/DoD/PR-1 naming but no `coverage-map: <link>` per-batch entry assertion.
- **Exact fix**: Add AC bullet: "Each batch entry in `docs/eval/mig-002-batch-plan.md` includes a `coverage-map: <link>` field that the corresponding eval PR description cites verbatim."

### Low Severity

#### L1. T01.02 invented JSON Schema dialect (Draft 2020-12)

- **Affects**: phase-1-tasklist.md / T01.02
- **Problem**: AC fixes dialect to "Draft 2020-12"; roadmap is silent on the dialect.
- **Roadmap evidence**: `roadmap.md` M1 table — `DM-011 ... fields:name,version,description,defaults,required_binaries,optional_capabilities,evals[]; parameterize accepted; unknown required fields rejected; jsonschema-valid`.
- **Tasklist evidence**: phase-1-tasklist.md T01.02 AC bullet 1 — "jsonschema-valid against `Draft 2020-12`".
- **Exact fix**: Replace "Draft 2020-12" with "a documented JSON Schema dialect (decision recorded in `TASKLIST_ROOT/artifacts/D-0002/spec.md`)".

#### L2. T01.10 invented determinism beyond "serializable"

- **Affects**: phase-1-tasklist.md / T01.10
- **Problem**: Roadmap DM-008 requires "serializable to JSON"; T01.10 AC adds byte-for-byte determinism not in roadmap.
- **Exact fix**: Demote determinism AC bullet to Notes: "Determinism is a derived requirement for doctor snapshot tests; not in DM-008."

#### L3. T01.11 wrong OQ-5 timing in Notes

- **Affects**: phase-1-tasklist.md / T01.11
- **Problem**: Notes say OQ-5 must resolve "before this lands per M2 entry blocker"; roadmap targets OQ-5 "before COMP-009 close (M2)".
- **Exact fix**: Rephrase Notes to: "OQ-5 must be resolved before COMP-009 close (M2 target) per roadmap Open Questions table."

#### L4. T01.13 invented `coverage_missing:<binary>` artifact name

- **Affects**: phase-1-tasklist.md / T01.13
- **Problem**: AC mentions "emits `coverage_missing:<binary>` artifact" on HARD fail; this artifact name is roadmap-introduced for hook matchers (FR-G5), not for missing binaries.
- **Exact fix**: Replace `coverage_missing:<binary>` with "a HARD-failure artifact identifying the missing capability". Leave FR-G5's `coverage_missing:<pattern>` only in T04.14.

#### L5. T01.15 invented `to_dict()` determinism

- **Affects**: phase-1-tasklist.md / T01.15
- **Problem**: AC adds `to_dict()` deterministic-serialization; roadmap says only "serializable".
- **Exact fix**: Soften to: "`ExpectResult` is serializable to JSON via `dataclasses.asdict()` (no `to_dict()` API mandated by DM-009)."

#### L6. T01.16 invented hash AC; omits "one entry per failing Expect"

- **Affects**: phase-1-tasklist.md / T01.16
- **Problem**: AC asserts hash consistency (not required and may fail for frozen dataclass with mutable details); roadmap DM-005 requires "one entry per failing Expect" which is absent.
- **Exact fix**: Remove hash AC. Add AC bullet: "Reporter produces exactly one ExpectFailure entry per failing Expect (verified by integration test with 2 failing Expects in a single eval producing 2 entries)."

#### L7. T01.26 invented "stubs for run" in --help

- **Affects**: phase-1-tasklist.md / T01.26
- **Problem**: AC line mentions "plus stubs for run added in M4". M1 only ships run/list/describe/doctor where run is registered without a body until M4.
- **Exact fix**: Replace "(plus stubs for run added in M4)" with "; additional subcommands land per their milestones (`run` lands in M4 per FR-CLI1)."

#### L8. T03.13 missing T03.14 dependency (COMP-015 probe)

- **Affects**: phase-3-tasklist.md / T03.13
- **Problem**: Roadmap COMP-008 lists `Deps | FR-RPT1, COMP-015`. T03.13 Dependencies declares only `T03.10, T03.11`.
- **Exact fix**: Change `Dependencies: T03.10, T03.11` to `Dependencies: T03.10, T03.11, T03.14`.

#### L9. T03.15 invented `parallel=0 clamps to 1`

- **Affects**: phase-3-tasklist.md / T03.15
- **Problem**: Roadmap specifies clamp range `[1,15]` but is silent on behavior when input is 0.
- **Exact fix**: Replace "`parallel=20` clamps to 15; `parallel=0` clamps to 1." with "`parallel=20` clamps to 15; `parallel < 1` rejected per clamp range `[1,15]`."

#### L10. T03.19 `0 disables` placed in Notes instead of AC

- **Affects**: phase-3-tasklist.md / T03.19
- **Problem**: Roadmap NFR-PERF4 AC explicitly: `0 disables`. T03.19 AC omits this; only Notes mention it.
- **Exact fix**: Add AC bullet: "When `--max-disk-mb 0` is set, the poller is disabled and no breach is ever signaled."

#### L11. T03.22 ban-import lint mechanism under-specified

- **Affects**: phase-3-tasklist.md / T03.22
- **Problem**: Roadmap names "ban-import lint rule (per COMP-013)". T03.22 uses `ruff check` without configuring an explicit rule that rejects `anthropic` imports.
- **Exact fix**: In Steps 4 and AC, name the ruff configuration: "Configure `tool.ruff.lint.flake8-tidy-imports.banned-api` in `pyproject.toml` to reject `anthropic` under `src/superclaude/cli/eval/`. Verify by injecting a synthetic `import anthropic` and confirming `ruff check` exits non-zero."

#### L12. T05.03/T05.04 plain skip vs soft-skip with skip_reason

- **Affects**: phase-5-tasklist.md / T05.03, T05.04
- **Problem**: T05.05 enforces soft-skip with `skip_reason`; T05.03/T05.04 say only "Skip under --no-mcp" (no `skip_reason`).
- **Exact fix**: Align Notes for T05.03 and T05.04 to: "Soft-skip under `--no-mcp` per OQ-5; status `SKIPPED` with `skip_reason` populated."

#### L13. T05.07-T05.13 M3-dependency advisory only

- **Affects**: phase-5-tasklist.md / T05.07-T05.13 (7 tasks)
- **Problem**: AC asserts "deterministic across 3 consecutive runs" relying on M3 EvalRunner/Reporter; deps list only T05.01 and T04.01..T04.08.
- **Exact fix**: Add Notes line to each (T05.07..T05.13): "Determinism assertion assumes M3 EvalRunner + Reporter availability transitively via M4 exit."

#### L14. T05.14-T05.21 missing clean-HOME isolation AC for E9-E15

- **Affects**: phase-5-tasklist.md / T05.14-T05.21 (8 tasks; E9-E15 inclusive)
- **Problem**: Roadmap E3 row says "passes deterministically on clean HOME"; E4-E15 reduce to "deterministic AC" but per-eval-HOME isolation is implicit. Tasklist asserts "3 runs identical" but not "clean per-eval HOME".
- **Exact fix**: Add AC bullet to each of T05.14-T05.21: "Eval body runs against a freshly-isolated per-eval HOME (per FR-ISO2) and does not read/write outside `EvalContext.scratch_root`."

#### L15. T05.23 R3-mit does not name MCP_FLAKY_TAG explicitly

- **Affects**: phase-5-tasklist.md / T05.23
- **Problem**: AC says "Tagged eval" generically; roadmap explicitly requires `MCP-flaky tag` honored.
- **Exact fix**: Rephrase first AC bullet to: "Eval carrying the `MCP_FLAKY_TAG` constant (and only that tag) triggers retry-once on stubbed MCP failure; on persistent failure, status `FAIL` with `mcp_server_flaky` artifact in `outcome.artifacts`."

#### L16. T05.26 invented `skip_flag_triggered` field assertion

- **Affects**: phase-5-tasklist.md / T05.26
- **Problem**: Roadmap TEST-014 AC is `MCP evals skipped; status SKIPPED; skip_reason set; counts kept_plus_skipped_equals_n_prime true`. T05.26 adds `skip_flag_triggered == --no-mcp` which is not in M5 row.
- **Exact fix**: Either remove the `skip_flag_triggered` AC bullet OR demote to Notes citing DM-001 (which defines the field but does not require this assertion in TEST-014).

## Verification Results

Verified: 2026-05-19
Findings resolved: 26/26

| Finding | Status | Notes |
|---------|--------|-------|
| M1 | RESOLVED | OQ-8 gating Step 3 added to T01.01; Notes line cites T06.03 deferral path |
| M2 | RESOLVED | T01.07 Dependencies now reads `T01.04, T01.05, T01.14` |
| M3 | RESOLVED | T01.14 AC added: "exercise each method against a synthetic `EvalContext` fixture..." |
| M4 | RESOLVED | T01.15 ValueError AC replaced with "`failure` is Optional per DM-009 (no required-when-failed coupling)" |
| M5 | RESOLVED | T01.20 CLAUDE.md AC replaced with positive-case pre-commit hook fixture |
| M6 | RESOLVED | T01.23 AC added "Tests assert process exit code 2 on schema-violation and unsafe-id rejection paths"; parameterize-expansion language broadened |
| M7 | RESOLVED | T02.14 AC adds `HookDeployFailed` error_tag propagation and SHA256 byte-identity assertion for hooks.json |
| M8 | RESOLVED | T03.03 Deliverables + AC now say "15 fields from DM-010" |
| M9 | RESOLVED | T05.02-T05.05 MCP Requirements row rewritten with semicolons and named MCP servers |
| M10 | RESOLVED | T05.27 AC adds `coverage-map: <link>` per-batch field requirement |
| L1 | RESOLVED | T01.02 Draft 2020-12 replaced with "documented JSON Schema dialect" |
| L2 | RESOLVED | T01.10 determinism AC softened to DM-008 "serializable" language; Notes flag determinism as derived |
| L3 | RESOLVED | T01.11 OQ-5 timing Notes rephrased to "before COMP-009 close (M2 target)" |
| L4 | RESOLVED | T01.13 `coverage_missing:<binary>` replaced with generic "HARD-failure artifact" wording |
| L5 | RESOLVED | T01.15 `to_dict()` determinism replaced with `dataclasses.asdict()` per DM-009 (verified at phase-1-tasklist.md:734) |
| L6 | RESOLVED | T01.16 hash AC removed; AC added: "exactly one ExpectFailure entry per failing Expect" |
| L7 | RESOLVED | T01.26 "stubs for run" parenthetical removed; replaced with milestone deferral language |
| L8 | RESOLVED | T03.13 Dependencies now reads `T03.10, T03.11, T03.14` |
| L9 | RESOLVED | T03.15 invented "`parallel=0 clamps to 1`" replaced with "`parallel < 1` rejected per clamp range `[1,15]`" |
| L10 | RESOLVED | T03.19 added AC: "When `--max-disk-mb 0` is set, the poller is disabled..." |
| L11 | RESOLVED | T03.22 Steps + AC now name `tool.ruff.lint.flake8-tidy-imports.banned-api` configuration per COMP-013 |
| L12 | RESOLVED | T05.03 + T05.04 Notes now say "Soft-skip under `--no-mcp` per OQ-5; status `SKIPPED` with `skip_reason` populated" |
| L13 | RESOLVED | All 13 E-tasks (T05.07-T05.21) Notes include M3-availability transitive dependency clause (T05.21 uses lowercase-d variant in concatenated Notes) |
| L14 | RESOLVED | All 13 E-tasks (T05.07-T05.21) AC include "freshly-isolated per-eval HOME (per FR-ISO2)" assertion (T05.08 combined into existing "Test asserts deterministic AC" bullet) |
| L15 | RESOLVED | T05.23 first AC bullet now names `MCP_FLAKY_TAG` constant explicitly |
| L16 | RESOLVED | T05.26 `skip_flag_triggered` AC bullet removed; demoted to Notes referencing DM-001 |

All 26 findings re-verified by grep against the patched phase files (2026-05-19). No regressions detected in surrounding context. Cross-file consistency sweep items from the PatchChecklist are tracked separately as informational and do not block release of the bundle.
