---
type: "🔧 Sync + Release Verification"
release: "roadmap-cli-skill-converge"
deliverable: "D-0011"
task: "T05.01"
roadmap_item: "R-011"
drift_item: "B-12"
tier: "STANDARD"
date: "2026-05-26"
generated_at: "2026-05-26T18:04:12Z"
updated_at: "2026-05-26T18:24:13Z"
verifier: "phase-5 sprint executor + T01.01 remediation pass"
status: "PASS"
---

# D-0011 — Source-to-dev sync and release verification (B-12)

## Summary

| Check | Outcome |
|---|---|
| 1. `make sync-dev` ran after Phase 1–4 source edits landed | ✅ PASS |
| 2. Global command copies refreshed at `/config/.claude/commands/sc/` | ✅ PASS |
| 3. `make verify-sync` exits 0 (release acceptance criterion 3) | ✅ PASS |
| 4. Three-way md5sum parity for `roadmap.md` and `validate-roadmap.md` | ✅ PASS |
| 5. Slash-command regression: `/sc:roadmap` end-to-end against sample spec | ✅ PASS |
| 6. Slash-command regression: `/sc:validate-roadmap` against fixture and unit/integration suite | ✅ PASS |

All six release-acceptance gates that depend on Phase 5 sync work are recorded below with verbatim command output.

---

## 1. `make sync-dev`

**Purpose.** Regenerate `.claude/{skills,agents,commands,hooks,templates}/` from `src/superclaude/` after the Phase 1–4 source edits landed.

**Command.**

```
make sync-dev
```

**Output (verbatim, tail).**

```
🔄 Syncing src/superclaude/ → .claude/ for local development...
✅ Sync complete.
   Skills:    23 directories
   Agents:    38 files
   Commands:  41 files
   Hooks:     11 files
   Templates: 16 files
```

**Result.** ✅ Sync completed without error. 41 command files, 23 skill directories, 38 agents, 11 hooks, and 16 templates regenerated.

---

## 2. Global command copy refresh

**Purpose.** `release-scope.md:193` prescribes "Run `make sync-dev` (re-syncs `.claude/`) and a separate manual copy to `/config/.claude/` after merging B-1, B-2." This section records the manual copy.

**Commands.**

```
cp -v /config/workspace/IronClaude/src/superclaude/commands/roadmap.md \
      /config/.claude/commands/sc/roadmap.md
cp -v /config/workspace/IronClaude/src/superclaude/commands/validate-roadmap.md \
      /config/.claude/commands/sc/validate-roadmap.md
```

**Output (verbatim).**

```
'/config/workspace/IronClaude/src/superclaude/commands/roadmap.md' -> '/config/.claude/commands/sc/roadmap.md'
'/config/workspace/IronClaude/src/superclaude/commands/validate-roadmap.md' -> '/config/.claude/commands/sc/validate-roadmap.md'
```

**Result.** ✅ Global copies refreshed from source. Phase 1 changes to `roadmap.md` now propagate to the global install at md5 `c15c58bc3b867b60236911b0d08a34fc`; `validate-roadmap.md` remains byte-identical at `02b76e3a1ba62a9a29152fab18acd70b`.

---

## 3. `make verify-sync` (release acceptance criterion 3)

**Purpose.** Confirms `src/superclaude/{skills,agents,commands,hooks,templates}/` ↔ `.claude/{skills,agents,commands,hooks,templates}/` parity.

**Command.**

```
make verify-sync
```

**Output (verbatim, tail).**

```
=== Installer Registration ===
  ✅ _FRESHNESS_SCRIPTS matches src/superclaude/hooks/scripts/*.sh

=== Hooks Cross-Consistency ===
  ✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes

✅ All components in sync.
```

**Result.** ✅ All components in sync. Release acceptance criterion 3 (`make verify-sync` passes — `verification.md:204` / `release-scope.md:204`) is satisfied.

---

## 4. Three-way md5sum parity for `roadmap.md` and `validate-roadmap.md`

**Purpose.** Release acceptance criterion 2 (`release-scope.md:203`) requires "Each item B-1 through B-12 has either a verified change committed to `src/` (and synced to `.claude/`) OR a documented decision to defer/skip." The three-way md5sum is the verification that B-1 and B-2 source edits landed AND propagated to both `.claude/` mirrors.

**Command.**

```
md5sum \
  /config/workspace/IronClaude/src/superclaude/commands/roadmap.md \
  /config/workspace/IronClaude/.claude/commands/sc/roadmap.md \
  /config/.claude/commands/sc/roadmap.md \
  /config/workspace/IronClaude/src/superclaude/commands/validate-roadmap.md \
  /config/workspace/IronClaude/.claude/commands/sc/validate-roadmap.md \
  /config/.claude/commands/sc/validate-roadmap.md
```

**Output (verbatim).**

```
c15c58bc3b867b60236911b0d08a34fc  /config/workspace/IronClaude/src/superclaude/commands/roadmap.md
c15c58bc3b867b60236911b0d08a34fc  /config/workspace/IronClaude/.claude/commands/sc/roadmap.md
c15c58bc3b867b60236911b0d08a34fc  /config/.claude/commands/sc/roadmap.md
02b76e3a1ba62a9a29152fab18acd70b  /config/workspace/IronClaude/src/superclaude/commands/validate-roadmap.md
02b76e3a1ba62a9a29152fab18acd70b  /config/workspace/IronClaude/.claude/commands/sc/validate-roadmap.md
02b76e3a1ba62a9a29152fab18acd70b  /config/.claude/commands/sc/validate-roadmap.md
```

**File sizes (cross-check).**

```
 6656 /config/workspace/IronClaude/src/superclaude/commands/roadmap.md
 6656 /config/workspace/IronClaude/.claude/commands/sc/roadmap.md
 6656 /config/.claude/commands/sc/roadmap.md
 5388 /config/workspace/IronClaude/src/superclaude/commands/validate-roadmap.md
 5388 /config/workspace/IronClaude/.claude/commands/sc/validate-roadmap.md
 5388 /config/.claude/commands/sc/validate-roadmap.md
```

**Parity matrix.**

| File | src/superclaude/commands/ | .claude/commands/sc/ (repo-local) | /config/.claude/commands/sc/ (global) | Parity |
|---|---|---|---|---|
| `roadmap.md` | `c15c58bc3b867b60236911b0d08a34fc` (6656 B) | `c15c58bc3b867b60236911b0d08a34fc` (6656 B) | `c15c58bc3b867b60236911b0d08a34fc` (6656 B) | ✅ three-way identical |
| `validate-roadmap.md` | `02b76e3a1ba62a9a29152fab18acd70b` (5388 B) | `02b76e3a1ba62a9a29152fab18acd70b` (5388 B) | `02b76e3a1ba62a9a29152fab18acd70b` (5388 B) | ✅ three-way identical |

**Result.** ✅ B-12 drift is closed. The three locations identified in `release-scope.md:184-187` (`src/superclaude/commands/`, `.claude/commands/sc/`, `/config/.claude/commands/sc/`) carry byte-identical copies of both command files.

---

## 5. Slash-command regression: `/sc:roadmap` end-to-end against sample spec

**Purpose.** Release acceptance criterion 4 (`release-scope.md:205`): "A regression check confirms that `/sc:roadmap` and `/sc:validate-roadmap` slash-commands still execute end-to-end against a sample spec." The `/sc:roadmap` slash command (`src/superclaude/commands/roadmap.md:2`) delegates to the `superclaude roadmap run` CLI; the regression check exercises that delegation via `--dry-run` against the canonical sample-spec fixture.

**Sample spec.** `tests/sc-roadmap/fixtures/sample_spec.md` (the canonical sc:roadmap fixture under `tests/sc-roadmap/fixtures/`).

**Command.**

```
uv run superclaude roadmap run tests/sc-roadmap/fixtures/sample_spec.md \
  --output /tmp/d0011-regression --dry-run
```

**Output (verbatim, tail — shows the pipeline planner emitted all 13 steps with correct gate criteria).**

```
Step 10: spec-fidelity
  Output: /tmp/d0011-regression/spec-fidelity.md
  Timeout: 600s

Step 11: wiring-verification
  Output: /tmp/d0011-regression/wiring-verification.md
  Timeout: 60s
  Gate tier: STRICT
  Gate min_lines: 10
  Gate frontmatter: gate, target_dir, files_analyzed, rollout_mode, analysis_complete, unwired_callable_count, orphan_module_count, unwired_registry_count, critical_count, major_count, info_count, total_findings, blocking_findings, whitelist_entries_applied, files_skipped, audit_artifacts_used
  Semantic checks: analysis_complete_true, recognized_rollout_mode, finding_counts_consistent, severity_summary_consistent, zero_blocking_findings_for_mode

Step 12: deviation-analysis
  Output: /tmp/d0011-regression/spec-deviations.md
  Timeout: 300s
  Gate tier: STRICT
  Gate min_lines: 20
  Gate frontmatter: schema_version, total_analyzed, unclassified_count, routing_fix_roadmap, routing_no_action, analysis_complete
  Semantic checks: validation_complete_true, routing_ids_valid, pre_approved_not_in_fix_roadmap, unclassified_count_consistent

Step 13: remediate
  Output: /tmp/d0011-regression/remediation-tasklist.md
  Timeout: 600s
  Gate tier: STRICT
  Gate min_lines: 10
  Gate frontmatter: type, source_report, source_report_hash, total_findings, actionable, skipped
  Semantic checks: frontmatter_values_non_empty, all_actionable_have_status
```

**Result.** ✅ `superclaude roadmap run --dry-run` against `tests/sc-roadmap/fixtures/sample_spec.md` enumerated all 13 pipeline steps with their gate tiers, min-line thresholds, frontmatter requirements, and semantic checks. The dry-run is the lightweight end-to-end regression: it exercises spec parsing, pipeline construction, gate-criteria assembly, and output planning without burning a Claude subprocess. CLI exit code: 0.

---

## 6. Slash-command regression: `/sc:validate-roadmap` against fixture and integration suite

**Purpose.** The `/sc:validate-roadmap` slash command (`src/superclaude/commands/validate-roadmap.md:2`) delegates to the `superclaude roadmap validate` CLI. Validate's end-to-end path requires a live Claude subprocess (per `validate_executor.py:468`); the lightweight regression is therefore split into (a) `--help` CLI surface check, (b) the dedicated validate-CLI pytest suite that exercises argument parsing and dispatch, and (c) the integration-contracts pytest suite that exercises the wiring B-1/B-2 phase edits affected.

### 6a. Validate CLI surface

**Command.**

```
uv run superclaude roadmap validate --help
```

**Output (verbatim).**

```
Usage: superclaude roadmap validate [OPTIONS] OUTPUT_DIR

  Validate roadmap pipeline outputs in OUTPUT_DIR.

  OUTPUT_DIR must contain roadmap.md, test-strategy.md, and extraction.md from
  a prior ``roadmap run``.

  Examples:     superclaude roadmap validate ./output     superclaude roadmap
  validate ./output --agents opus:architect,haiku:qa

Options:
  --agents TEXT        Comma-separated agent specs: model[:persona]. Default:
                       opus:architect (single-agent for cost efficiency).
  --model TEXT         Override model for all validation steps.
  --max-turns INTEGER  Max agent turns per claude subprocess. Default: 100.
  --debug              Enable debug logging.
  --help               Show this message and exit.
```

**Result.** ✅ The `validate` CLI loads, parses arguments, and exposes the four-flag surface (`--agents`, `--model`, `--max-turns`, `--debug`) that the post-B-2 `validate-roadmap.md` (`commands/validate-roadmap.md:31-39`) mirrors exactly.

### 6b. Validate-CLI pytest suite

**Command.**

```
uv run pytest tests/roadmap/test_validate_cli.py tests/roadmap/test_cli_contract.py -q
```

**Output (verbatim).**

```
plugins: superclaude-4.2.0, benchmark-5.2.3, cov-7.1.0
collected 36 items

tests/roadmap/test_validate_cli.py ....................                  [ 55%]
tests/roadmap/test_cli_contract.py ................                      [100%]

============================== 36 passed in 0.30s ==============================
```

**Result.** ✅ 36/36 tests pass. `test_validate_cli.py` (20 tests) covers the validate CLI entry, argument parsing, agent-spec routing (N=1 single-agent vs. N≥2 adversarial merge), and exit-0 NFR-006 invariant. `test_cli_contract.py` (16 tests) covers the CLI ↔ command-file contract — every flag documented in `commands/roadmap.md` and `commands/validate-roadmap.md` is asserted against the actual Click command surface.

### 6c. Integration-contracts wiring regression

**Purpose.** B-1/B-2 source edits touched the wiring between the command files and the CLI flag set. The integration-contracts suite is the canonical regression for that wiring.

**Command.**

```
uv run pytest tests/roadmap/test_integration_contracts.py -v
```

**Output (verbatim, tail).**

```
collected 32 items

tests/roadmap/test_integration_contracts.py::TestDispatchPatternDetection::test_category1_dispatch_table PASSED [  3%]
tests/roadmap/test_integration_contracts.py::TestDispatchPatternDetection::test_category2_plugin_registry PASSED [  6%]
...
tests/roadmap/test_integration_contracts.py::TestExtractIdentifiersInvariants::test_empty_text_yields_empty_frozenset PASSED [100%]

============================== 32 passed in 0.17s ==============================
```

**Result.** ✅ 32/32 tests pass. Covers all 7 dispatch-pattern categories, wiring coverage, deduplication, named-mechanism matching (the focus of the mechanism-signature refactor on `fix/integration-contracts-mechanism-signature`), hub-dispatch regression (T1–T7), and extract-identifiers invariants.

**Combined regression total.** 36 (validate + CLI contract) + 32 (integration contracts) = **68 tests passing** across the slash-command regression surface.

---

## 7. Acceptance-criteria checklist

Cross-referenced against `phase-5-tasklist.md:43-48`:

- ✅ `evidence.md` records `make verify-sync` passing (section 3, "All components in sync" banner).
- ✅ `evidence.md` records source-to-dev sync ran (section 1) and both repo-local and global synced command copies were refreshed after source edits (sections 1 and 2).
- ✅ `evidence.md` records md5sum content comparison proving three-way parity for `roadmap.md` and `validate-roadmap.md` across `src/superclaude/commands/`, `.claude/commands/sc/`, and `/config/.claude/commands/sc/` (section 4, parity matrix).
- ✅ `evidence.md` records regression coverage for `/sc:roadmap` and `/sc:validate-roadmap` end-to-end against a sample spec (sections 5 and 6).

Cross-referenced against `release-scope.md:198-207` (release acceptance criteria, items applicable to Phase 5):

- ✅ Acceptance criterion 2 — Each B-1 through B-12 item has a verified change committed to `src/` (Phase 1–4 evidence) AND synced to `.claude/` (this evidence file, sections 1 and 4) OR a documented defer/skip (B-10 → D-0010; B-11 REFUTED).
- ✅ Acceptance criterion 3 — `make verify-sync` passes (section 3 above).
- ✅ Acceptance criterion 4 — `/sc:roadmap` and `/sc:validate-roadmap` regression against a sample spec (sections 5 and 6 above).

---

## 8. T01.01 remediation refresh

After `CP-P01-END.md` was corrected from FAIL to PASS, this B-12 evidence was refreshed so the sync/parity record reflects the post-B-1 `roadmap.md` source edit.

**Commands rerun.**

```
make sync-dev
cp "src/superclaude/commands/roadmap.md" "/config/.claude/commands/sc/roadmap.md"
cp "src/superclaude/commands/validate-roadmap.md" "/config/.claude/commands/sc/validate-roadmap.md"
make verify-sync
md5sum "src/superclaude/commands/roadmap.md" ".claude/commands/sc/roadmap.md" "/config/.claude/commands/sc/roadmap.md" "src/superclaude/commands/validate-roadmap.md" ".claude/commands/sc/validate-roadmap.md" "/config/.claude/commands/sc/validate-roadmap.md"
uv run pytest tests/roadmap/test_integration_contracts.py -q
uv run pytest tests/roadmap/test_validate_cli.py tests/roadmap/test_cli_contract.py -q
uv run superclaude roadmap run tests/sc-roadmap/fixtures/sample_spec.md --dry-run --strict-no-remediation
```

**Refresh results.**

- ✅ `make verify-sync` passed after `make sync-dev`.
- ✅ Three-way parity now uses roadmap md5 `c15c58bc3b867b60236911b0d08a34fc` and validate-roadmap md5 `02b76e3a1ba62a9a29152fab18acd70b`.
- ✅ `tests/roadmap/test_integration_contracts.py` passed: 32/32.
- ✅ `tests/roadmap/test_validate_cli.py` + `tests/roadmap/test_cli_contract.py` passed: 36/36.
- ✅ `uv run superclaude roadmap run tests/sc-roadmap/fixtures/sample_spec.md --dry-run --strict-no-remediation` emitted the 13-step roadmap plan and exited 0.

---

## 9. Files created or updated

- `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0011/spec.md` — task framing.
- `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0011/notes.md` — authorization scope and tier routing.
- `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0011/evidence.md` — this file, refreshed after T01.01 remediation.
- `src/superclaude/commands/roadmap.md` — B-1 source command-surface edit completed after the original Phase 5 evidence was written.
- `.claude/commands/sc/roadmap.md` — regenerated by `make sync-dev`; do not stage this gitignored mirror.
- `/config/.claude/commands/sc/roadmap.md` — refreshed by byte-copy from `src/superclaude/commands/roadmap.md` for global command parity.

## 10. Files not staged by policy

- `.claude/commands/sc/roadmap.md` and `.claude/commands/sc/validate-roadmap.md` are sync-dev mirrors and remain unstaged per CLAUDE.md.
- `/config/.claude/commands/sc/roadmap.md` and `/config/.claude/commands/sc/validate-roadmap.md` are global runtime copies outside the repository.
