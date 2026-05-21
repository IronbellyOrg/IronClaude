# Patch Checklist

Generated: 2026-05-19
Total edits: 26 across 4 files (phase-1, phase-2, phase-3, phase-5)

## File-by-file edit checklist

- `phase-1-tasklist.md`
  - [ ] T01.01 add OQ-8 gating step + Notes line (from M1)
  - [ ] T01.02 replace `Draft 2020-12` with documented-dialect language (from L1)
  - [ ] T01.07 add `T01.14` to Dependencies (from M2)
  - [ ] T01.10 demote determinism AC to Notes (from L2)
  - [ ] T01.11 rephrase OQ-5 timing in Notes (from L3)
  - [ ] T01.13 replace `coverage_missing:<binary>` with generic phrasing (from L4)
  - [ ] T01.14 add synthetic-EvalContext exercise AC (from M3)
  - [ ] T01.15 remove ValueError AC; soften to_dict() determinism (from M4, L5)
  - [ ] T01.16 remove hash AC; add `one entry per failing Expect` AC (from L6)
  - [ ] T01.20 remove CLAUDE.md doc AC (from M5)
  - [ ] T01.23 add exit-code-2 AC; broaden parameterize-expansion wording (from M6)
  - [ ] T01.26 remove "stubs for run" parenthetical (from L7)

- `phase-2-tasklist.md`
  - [ ] T02.14 add error-tag + verbatim-hooks.json ACs (from M7)

- `phase-3-tasklist.md`
  - [ ] T03.03 replace "14 fields" with "15 fields" in Deliverables + AC (from M8)
  - [ ] T03.13 add `T03.14` to Dependencies (from L8)
  - [ ] T03.15 replace `parallel=0 clamps to 1` with `parallel < 1 rejected` (from L9)
  - [ ] T03.19 promote `0 disables` from Notes to AC (from L10)
  - [ ] T03.22 specify ruff `flake8-tidy-imports.banned-api` configuration (from L11)

- `phase-5-tasklist.md`
  - [ ] T05.02 fix MCP Requirements cell + name `auggie` server (from M9)
  - [ ] T05.03 fix MCP Requirements cell + name `auggie` server + soft-skip language (from M9, L12)
  - [ ] T05.04 fix MCP Requirements cell + name `auggie-mcp` server + soft-skip language (from M9, L12)
  - [ ] T05.05 fix MCP Requirements cell + name `airis-mcp-gateway` server (from M9)
  - [ ] T05.07-T05.13 add M3-dependency Notes line on each (from L13)
  - [ ] T05.14-T05.21 add clean-per-eval-HOME isolation AC on each (from L14)
  - [ ] T05.23 name `MCP_FLAKY_TAG` explicitly in first AC bullet (from L15)
  - [ ] T05.26 remove or demote `skip_flag_triggered` AC (from L16)
  - [ ] T05.27 add `coverage-map: <link>` per-batch AC bullet (from M10)

## Cross-file consistency sweep

- [ ] Audit ALL phase files for any other `| Field | A | B |` 3-cell rows under metadata tables (escape internal pipes with `\|` or use `;`).
- [ ] Re-check Phase Files tier distribution counts in `tasklist-index.md` (current index claims Phase 1: STRICT 7 / STANDARD 13 / EXEMPT 2 / LIGHT 5; actual file has STRICT 5 / STANDARD 15 / EXEMPT 2 / LIGHT 5 — update or note as advisory).
- [ ] Verify no other tasks reference `coverage_missing:<binary>` outside of T04.14's `coverage_missing:<pattern>`.

---

## Precise diff plan

Suggested execution order: highest-impact files first (phase-1 has the most edits, then phase-5, phase-3, phase-2).

### 1) `phase-1-tasklist.md`

#### M1 — T01.01 add OQ-8 gating

**Current**: T01.01 Steps 1-6 do not mention OQ-8; Notes only say "Default scratch roots align with AC12 allowlist landing in T01.19."
**Change**: Insert OQ-8 consideration into Steps and Notes.
**Diff intent**:
```
Steps (insert between current step 2 and step 3):
2.5. **[PLANNING]** Confirm OQ-8 resolution status (DOC-OQ8 T06.03) or record deferral in `TASKLIST_ROOT/artifacts/D-0001/spec.md`.

Notes (add line):
- OQ-8 (`CLAUDE_FAKE_TIME_OFFSET` consumption) must resolve before COMP-005 close or be deferred via T06.03 decision.
```

#### L1 — T01.02 dialect

**Current AC bullet**: `File `src/superclaude/cli/eval/suites/suite.schema.json` exists and is jsonschema-valid against `Draft 2020-12`.`
**Change**: Replace dialect.
**Diff intent**:
```
File ... is jsonschema-valid against a documented JSON Schema dialect (decision recorded in `TASKLIST_ROOT/artifacts/D-0002/spec.md`).
```

#### M2 — T01.07 dependency

**Current**: `**Dependencies:** T01.04, T01.05`
**Change**: Add `T01.14`.
**Diff intent**: `**Dependencies:** T01.04, T01.05, T01.14`

#### L2 — T01.10 demote determinism

**Current AC bullet**: `\`to_json()\` output is deterministic byte-for-byte for identical inputs (verified by hashing two serializations).`
**Change**: Move to Notes.
**Diff intent**: Replace with `\`to_json()\` produces a serializable mapping (DM-008 contract).` and append Notes line: `Determinism is a derived requirement for doctor snapshot tests, not in DM-008.`

#### L3 — T01.11 OQ-5 timing

**Current Notes**: `OQ-5 (mcp_server_reachable semantics) must be resolved before this lands per M2 entry blocker.`
**Change**: Correct phrasing.
**Diff intent**: `OQ-5 must be resolved before COMP-009 close (M2 target) per roadmap Open Questions table.`

#### L4 — T01.13 artifact name

**Current AC bullet**: `Doctor fails closed (exit 2) when any HARD capability is missing; emits \`coverage_missing:<binary>\` artifact.`
**Change**: Remove the `coverage_missing:` artifact name.
**Diff intent**: `Doctor fails closed (exit 2) when any HARD capability is missing; emits a HARD-failure artifact identifying the missing capability.`

#### M3 — T01.14 synthetic EvalContext exercise

**Current**: T01.14 AC bullets cover interface + stubs; no synthetic-EvalContext exercise.
**Change**: Append AC bullet.
**Diff intent**: Add as fifth AC line `Unit tests instantiate \`Expect\` and exercise each method against a synthetic `EvalContext` fixture, asserting the stub `NotImplementedError("M4")` is raised consistently (per M1 exit criterion).`

#### M4 — T01.15 remove ValueError invariant

**Current AC bullet**: `Constructing with \`passed=False\` and \`failure=None\` raises \`ValueError\` (failure detail required on failure).`
**Change**: Replace with roadmap-faithful wording.
**Diff intent**: `Construction with valid field types succeeds; \`failure\` is Optional per DM-009 (no required-when-failed coupling).`

#### L5 — T01.15 soften to_dict() determinism

**Current AC bullet**: `\`to_dict()\` is deterministic across two calls with the same instance.`
**Change**: Soften.
**Diff intent**: `\`ExpectResult\` is JSON-serializable via \`dataclasses.asdict()\` per DM-009 "serializable" requirement.`

#### L6 — T01.16 fix hash + add per-Expect entry

**Current AC bullet**: `A reference failure instance hashes consistently across two constructions.`
**Change**: Remove hash; add per-Expect entry.
**Diff intent**: Replace with `Reporter produces exactly one ExpectFailure entry per failing Expect (verified by integration test in which 2 failing Expects in a single eval produce 2 ExpectFailure entries).`

#### M5 — T01.20 remove CLAUDE.md doc

**Current AC bullet**: `Documentation in \`CLAUDE.md\` references the gate.`
**Change**: Remove.
**Diff intent**: Delete that AC bullet entirely; renumber remaining bullets.

#### M6 — T01.23 add exit-code AC + broaden parameterize

**Current**: AC mentions preflight ordering + parameterized-unsafe rejection; no exit-code-2 assertion.
**Change**: Add AC bullet + rephrase parameterize scope.
**Diff intent**:
```
+ Tests assert process exit code 2 on schema-violation and unsafe-id rejection paths.
- File ... contains tests for schema-violation rejection, unsafe id rejection, parameterized-unsafe rejection, and pre-flight ordering (no FS writes before rejection).
+ File ... contains tests for schema-violation rejection, unsafe id rejection, parameterize expansion validated post-expansion (both safe and unsafe expansion cases), and pre-flight ordering (no FS writes before rejection).
```

#### L7 — T01.26 remove run stub mention

**Current AC bullet**: `\`superclaude eval --help\` lists \`list\`,\`describe\`,\`doctor\` (plus stubs for run added in M4).`
**Change**: Remove parenthetical.
**Diff intent**: `\`superclaude eval --help\` lists the M1 subcommands (\`list\`, \`describe\`, \`doctor\`); additional subcommands land per their milestones (\`run\` per FR-CLI1 in M4).`

### 2) `phase-2-tasklist.md`

#### M7 — T02.14 add error-tag + verbatim hooks.json

**Current AC**: 4 bullets (signature, idempotency, no-real-HOME, spec record).
**Change**: Append 2 AC bullets.
**Diff intent**:
```
+ Adapter raises `HookDeployFailed` with an `error_tag` propagated to `EvalRunner.outcome.artifacts` on `install_hooks` failure.
+ `<home_path>/.claude/hooks.json` is byte-identical to `src/superclaude/hooks/hooks.json` (SHA256 equality assertion in adapter test).
```

### 3) `phase-3-tasklist.md`

#### M8 — T03.03 field count 14 -> 15

**Current**: "with the 14 fields from DM-010" (Deliverables); "exposes the 14 fields named in DM-010" (AC).
**Change**: Replace 14 with 15 in both occurrences.
**Diff intent**: `replace_all` `the 14 fields` -> `the 15 fields` in T03.03 only.

#### L8 — T03.13 missing dependency

**Current**: `**Dependencies:** T03.10, T03.11`
**Change**: Add T03.14.
**Diff intent**: `**Dependencies:** T03.10, T03.11, T03.14`

#### L9 — T03.15 fix invented clamp behavior

**Current AC bullet**: `\`parallel=20\` clamps to 15; \`parallel=0\` clamps to 1.`
**Change**: Reword.
**Diff intent**: `\`parallel=20\` clamps to 15; \`parallel < 1\` rejected per clamp range \`[1,15]\`.`

#### L10 — T03.19 promote `0 disables` to AC

**Current Notes**: `--max-disk-mb 0 disables the budget per roadmap AC.`
**Change**: Promote to AC.
**Diff intent**: Add AC bullet `When \`--max-disk-mb 0\` is set, the poller is disabled and no breach is ever signaled (verified by a fixture that fills the run dir past 2 GB and asserts the run is not interrupted).` Keep Notes line.

#### L11 — T03.22 specify ruff configuration

**Current Steps 4**: `Add ruff invocation step asserting no \`anthropic\` import under \`src/superclaude/cli/eval/\`.`
**Current AC**: `\`uv run ruff check src/superclaude/cli/eval/\` exits 0 (no \`anthropic\` import).`
**Change**: Name the ruff rule configuration.
**Diff intent**:
```
Step 4 -> Configure `tool.ruff.lint.flake8-tidy-imports.banned-api` in `pyproject.toml` to reject `anthropic` imports under `src/superclaude/cli/eval/`. Inject a synthetic `import anthropic` and confirm `ruff check` exits non-zero.
AC -> `uv run ruff check src/superclaude/cli/eval/` exits 0 on the clean tree AND exits non-zero when a synthetic `import anthropic` is injected (verified by test in `tests/cli/eval/test_ban_import_rule.py`).
```

### 4) `phase-5-tasklist.md`

#### M9 — T05.02-T05.05 MCP Requirements row fix

**Current rows** (T05.02-T05.05):
```
| MCP Requirements | None | Preferred: Sequential, Context7 |
```
**Change**: Per-task replacements:
- T05.02: `| MCP Requirements | Required: auggie (mcp__auggie__codebase-retrieval); Preferred: Sequential, Context7 |`
- T05.03: `| MCP Requirements | Required: auggie (mcp__auggie__codebase-retrieval); Preferred: Sequential, Context7 |`
- T05.04: `| MCP Requirements | Required: auggie-mcp (mcp__auggie-mcp__ask_question); Preferred: Sequential, Context7 |`
- T05.05: `| MCP Requirements | Required: airis-mcp-gateway (mcp__airis-mcp-gateway__auggie_search); Preferred: Sequential, Context7 |`

#### L12 — T05.03/T05.04 soft-skip language

**Current Notes** (T05.03 and T05.04): `Skip under \`--no-mcp\`.`
**Change**: Replace.
**Diff intent**: `Soft-skip under \`--no-mcp\` per OQ-5; status \`SKIPPED\` with \`skip_reason\` populated.`

#### L13 — T05.07-T05.13 M3-dependency Notes

**Current Notes**: `Confidence 75% reflects OQ-2 dependency at task generation time.`
**Change**: Append M3-transitive-dependency line.
**Diff intent**: Add a new Notes line on each: `Determinism assertion assumes M3 EvalRunner + Reporter availability transitively via M4 exit.`

#### L14 — T05.14-T05.21 add clean-HOME AC

**Current AC bullets** (each): 4 bullets covering content, deterministic 3 runs, reproducibility, spec.
**Change**: Append fifth AC bullet on each.
**Diff intent**: `Eval body runs against a freshly-isolated per-eval HOME (per FR-ISO2) and does not read/write outside \`EvalContext.scratch_root\`.`

#### L15 — T05.23 name MCP_FLAKY_TAG

**Current first AC bullet**: `Tagged eval fails once on a stubbed MCP failure and retries exactly once; on persistent failure, status is FAIL with \`mcp_server_flaky\` artifact.`
**Change**: Name the tag constant.
**Diff intent**: `Eval carrying the \`MCP_FLAKY_TAG\` constant (and only that tag) triggers retry-once on stubbed MCP failure; on persistent failure, status \`FAIL\` with \`mcp_server_flaky\` artifact in \`outcome.artifacts\`.`

#### L16 — T05.26 demote skip_flag_triggered

**Current AC bullet**: `Test asserts skip_flag_triggered == \`--no-mcp\` per outcome.`
**Change**: Remove or move to Notes.
**Diff intent**: Delete the AC bullet. Append Notes line: `\`skip_flag_triggered\` is a DM-001 field; assertion is derived from FR-RPT1 reporting contract, not a TEST-014 requirement.`

#### M10 — T05.27 add coverage-map AC

**Current AC**: 4 bullets covering doc presence, batch entry DoD, PR ordering, spec.
**Change**: Append AC bullet.
**Diff intent**: `Each batch entry in \`docs/eval/mig-002-batch-plan.md\` includes a \`coverage-map: <link>\` field that the corresponding eval PR description cites verbatim (per roadmap MIG-002 AC "eval PRs reference coverage map").`
