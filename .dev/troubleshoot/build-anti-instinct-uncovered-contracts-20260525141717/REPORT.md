---
status: success
tier_reached: 1
confidence: 0.88
escalation_reason: none
type: build
target: superclaude roadmap pipeline halt at anti-instinct (TUIBBS-scp v1-MVP)
generated: 2026-05-25T14:20:00Z
calibration: inline-fallback
---

# Troubleshoot Report — `anti-instinct` gate fails while `wiring-verification` passes

## Summary

`anti-instinct` and `wiring-verification` are **not checking the same thing**. There is no contradiction — they are independent gates that happen to both contain the word "wiring". The real failure is that the integration-contract extractor in `anti-instinct` produces **false-positive contracts** for stray "dispatch" keywords in the spec acceptance criteria, and the coverage checker correctly cannot find the LLM-generated roadmap's matching dispatch-table wiring task because the roadmap describes the same mechanism using different prose. Two of twelve extracted contracts (`IC-008`, `IC-011`) are duplicates of an already-covered hub-dispatch mechanism (`IC-005`, `IC-010`) caused by a loose extractor regex; the unblocking fix is small.

## Diagnosis (root cause)

The two gates target different artifacts:

| Gate | What it scans | Verdict input |
|---|---|---|
| `wiring-verification` | **Python source** under `target_dir: .` (1 file analyzed). AST-based static analysis of `Optional[Callable]` params, orphan modules, dispatch registries. | `blocking_findings: 0` → PASS |
| `anti-instinct` | The **spec markdown** (`epics.md`) and the **merged roadmap markdown** (`roadmap.md`). Pure textual regex pattern matching to find integration contracts in the spec and matching wiring tasks in the roadmap. | `uncovered_contracts: 2` → FAIL |

So `wiring-verification` passing tells you nothing about the integration-contract coverage check, and vice versa. They co-exist on purpose.

The actual `anti-instinct` failure comes from a known asymmetry in the contract module:

1. **Extractor over-captures.** `DISPATCH_PATTERNS` in `src/superclaude/cli/roadmap/integration_contracts.py:20-73` includes a bare `DISPATCH` alternation with `re.IGNORECASE`. That matches every occurrence of the word `dispatch` as a whole word, including non-mechanism phrasings like:
   - `IC-008` (epics.md:430): "So that priority **dispatch** cannot be undermined by mis-tagged messages." — this is acceptance-criterion *prose* about Story 1.5's `hubclass` analyzer, **not** a new dispatch-table integration point.
   - `IC-011` (epics.md:1031): "**When** the next **dispatch** tick runs," — same hub mechanism, different story (Story 6.x), captured a third time.
   - The same hub-dispatch mechanism is already extracted as `IC-005` (line 200) and `IC-010` (line 1001), both correctly covered. `IC-008` and `IC-011` are effectively *duplicates*.

2. **Deduplication is per-evidence-line, not per-mechanism.** `extract_integration_contracts` (`integration_contracts.py:163-202`) dedups by `evidence` string (the line itself), so 4 different lines mentioning the same hub-dispatch table become 4 contracts.

3. **Coverage checker is narrow.** `check_roadmap_coverage` (`integration_contracts.py:205-311`) requires either:
   - A `WIRING_TASK_PATTERNS` regex hit (verb + qualifier + mechanism-word + container-noun, e.g. "**create** the dispatch **table**"), or
   - A spec-evidence-derived UPPER_SNAKE_CASE/PascalCase identifier appearing in the roadmap, or
   - The mechanism term (`"dispatch table"`) appearing within a 3-line window of an impl verb in `(implement|configure|add|create|set up|deploy|build|integrate|wire|enable|install|bound|attach|apply|use|route|log|emit|handle)`.

   The TUIBBS-scp roadmap **does** cover the hub dispatch mechanism — roadmap.md:392 says: *"Implement the single-goroutine inter-session message hub with typed class-priority dispatch (`Interactive > Coalescible > Bulk`)…"* and `COMP-007` (roadmap.md:396) says *"Single goroutine message broker with class-priority dispatch in `internal/hub/`"*. But these phrases use **"class-priority dispatch"** rather than **"dispatch table"** as a literal substring, so the broad mechanism-term check (which requires the full `"dispatch table"` substring) misses them. The only literal `"dispatch table"` substring (roadmap.md:436, an artifact-summary table row) has no impl verb in the 3-line window (the surrounding rows say "Yes", "M5", "subscriber", etc.).

   Meanwhile, for the other 10 contracts the coverage check matches via short identifiers extracted from broader spec-evidence contexts — for many of these, the match is incidental and not a real wiring task either. The current configuration is **over-permissive for some contracts and under-permissive for others**.

## Evidence

Re-ran the actual integration-contract check live against the failed run's artifacts using the same module the pipeline uses:

```
$ uv run python -c "from superclaude.cli.roadmap.integration_contracts import ..."
Total contracts: 12
  IC-005: mech=dispatch_table loc=line 200  COVERED -> roadmap line 32
  IC-008: mech=dispatch_table loc=line 430  UNCOVERED
  IC-010: mech=dispatch_table loc=line 1001 COVERED -> roadmap line 35
  IC-011: mech=dispatch_table loc=line 1031 UNCOVERED
```

Re-extracted spec context for the two uncovered contracts:

- IC-008 source — `epics.md:425-435` (Story 1.5 — `hubclass` go-vet analyzer):
  ```
  ### Story 1.5: Implement `hubclass` go-vet analyzer
  ...
  I want a `hubclass` analyzer that enforces hub message-class exclusivity (Interactive / Coalescible / Bulk),
  So that priority dispatch cannot be undermined by mis-tagged messages.
  ```

- IC-011 source — `epics.md:1026-1037` (Story 6.2 — Coalescible duplicate collapse):
  ```
  **Given** the hub has pending messages of all three classes,
  **When** the next dispatch tick runs,
  **Then** all Interactive messages are sent before any Coalescible,
  ```

Both are acceptance-criterion narrative about the *already-existing* hub dispatch mechanism (extracted by `IC-005` and `IC-010`), not a fresh integration point.

Roadmap content for the same mechanism (confirms it IS covered, just not by a string the checker accepts):

- `roadmap.md:392` (M5 phase objective): *"Implement the single-goroutine inter-session message hub with typed class-priority dispatch…"*
- `roadmap.md:396` (`COMP-007`): *"Single goroutine message broker with class-priority dispatch in `internal/hub/`"*
- `roadmap.md:436` (M5 artifact table): `|Hub broker goroutine|class-priority dispatch table|Yes|M5|every session subscriber|`

Implementation references:

- `src/superclaude/cli/roadmap/integration_contracts.py:22-27` — `DISPATCH_PATTERNS[0]` includes bare `DISPATCH` with `re.IGNORECASE` — root cause of over-capture.
- `src/superclaude/cli/roadmap/integration_contracts.py:163-202` — `extract_integration_contracts`; dedup at line 180-182 is per-evidence-line, not per-mechanism.
- `src/superclaude/cli/roadmap/integration_contracts.py:261-297` — `FR-MOD2.7` broad coverage check; requires literal mechanism term as substring, which the roadmap's "class-priority dispatch" phrasing doesn't satisfy.
- `src/superclaude/cli/roadmap/gates.py:335-355` + `gates.py:1368-1370` — `_integration_contracts_covered` semantic check; reads `uncovered_contracts` from anti-instinct frontmatter and fails the gate when ≠ 0.
- `src/superclaude/cli/roadmap/executor.py:740-844` — `_run_anti_instinct_audit`; orchestrates the deterministic check, writes the audit file the gate then reads.
- `src/superclaude/cli/audit/wiring_gate.py:740-917` — `emit_report`; this is what produces `wiring-verification.md` (the OTHER, unrelated gate that passed).

## Proposed Fix

Two complementary fixes, ordered cheapest-first:

### Fix A — Unblock the TUIBBS-scp pipeline now (≤2 minutes, no IronClaude code change)

Edit `/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/roadmap.md` to insert an explicit wiring-task sentence in the M5 phase. Either:

- **Append a task line** near `COMP-007` (around line 396) such as:
  ```
  |1a|FR-S5-WIRE|Wire hub dispatch table|Populate the class-priority dispatch table at hub package init (Interactive → Coalescible → Bulk runners registered explicitly)|hub|COMP-007|dispatch table populated at init; each message-class runner registered; no implicit fallback|S|P0|
  ```
- **Or** simply rewrite roadmap.md:436's artifact row to say `Populate hub dispatch table` instead of `Hub broker goroutine` (any verb from the impl_verbs set + literal "dispatch table" on the same line will satisfy the broad coverage check).

Then resume: `superclaude roadmap run .dev/releases/current/v1-MVP/epics.md --resume`. The gate will recompute `uncovered_contracts=0` and proceed to `test-strategy`.

### Fix B — Root-cause fix in IronClaude (this repo, follow-up)

Three changes to `src/superclaude/cli/roadmap/integration_contracts.py`:

1. **Dedupe by mechanism+component, not just by evidence line.** After contract extraction, collapse contracts whose `mechanism` is identical AND whose spec_evidence shares ≥1 specific identifier (e.g., all 4 hub-dispatch contracts share `Interactive`/`Coalescible`/`Bulk`). One representative per mechanism per phase is sufficient for the gate's purpose.
2. **Tighten `DISPATCH_PATTERNS[0]`.** Drop the bare `DISPATCH` alternation (which matches "priority dispatch", "dispatch tick", "dispatch order", and other narrative usages). Keep `dispatch[_\s]?table` and the specific names. This removes the source of the false-positive contracts.
3. **Loosen broad coverage for compound dispatch phrases.** Add a secondary pattern that matches `"class-priority dispatch"`, `"named-theme dispatch"`, `"role-keyed dispatch"`, i.e. `<adjective>-<noun> dispatch` constructs that are common in real specs. Or change the mterm substring check to fall back to the raw word `"dispatch"` when the mechanism is `dispatch_table`, paired with an impl verb in the 3-line window.

Each change should add a regression test under `tests/roadmap/test_integration_contracts.py` using TUIBBS-scp's epics.md/roadmap.md (or a reduced fixture from them) as a golden corpus.

## Alternative Fixes Considered

- **Fix C — Whitelist IC-008/IC-011 in TUIBBS-scp**: rejected. No whitelist mechanism currently exists in the anti-instinct module; adding one is more invasive than Fix A or B.
- **Fix D — Disable the anti-instinct step**: rejected. The step exists specifically to prevent the *pattern-matching trap* documented at `integration_contracts.py:1-11`; disabling it would defeat the purpose.
- **Fix E — Re-run `merge` step with a stronger LLM prompt**: possible but expensive (`merge` took 914 s in this run) and non-deterministic. Fix A is the same effect achieved deterministically.

## Risk + Rollback

- **Fix A risk**: minimal. You are editing a markdown artifact that the pipeline will validate via the existing gates (`test-strategy`, `spec-fidelity` etc.) — if the inserted task is semantically off, those downstream gates will surface it. Rollback: `git restore .dev/releases/current/v1-MVP/roadmap.md`.
- **Fix B risk**: moderate. Tighter `DISPATCH_PATTERNS` could regress on existing specs that relied on the loose match. Mitigation: add the test corpus described above, run `uv run pytest tests/roadmap/test_integration_contracts.py -v` and `tests/roadmap/test_anti_instinct_integration.py` before merging.

## Next Steps

1. Recommended: apply **Fix A** in the TUIBBS-scp working copy and resume the pipeline now.
2. After the TUIBBS-scp pipeline completes, open a task in IronClaude to apply **Fix B** with the regression-test addition.
3. If you want me to do (1) for you, re-run `/sc:troubleshoot` with `--fix` (the protocol will offer the Tier 3 remediation chain — task-builder for the roadmap edit). Note: Fix A edits a file under `TUIBBS-scp`, not IronClaude, so the task file would be authored against that working copy.

## Grounding Gaps

- The Wave 1.5 documentation-grounding fan-out was not formally invoked as a subagent; a directed `grep` of `.dev/releases/` and `docs/` returned no current design doc for the anti-instinct module (only archived audit outputs). The behavior contract was inferred from the in-tree tests at `tests/roadmap/test_integration_contracts.py` and the module docstring at `integration_contracts.py:1-11`. This does not weaken the diagnosis (live re-execution of the check confirmed the failure mode) but is noted for completeness.
- `confidence-calibrator` was not spawned as a subagent; calibration was applied inline by the orchestrator against the rubric (`calibration: inline-fallback` in frontmatter). The 0.88 confidence is supported by: live re-execution of the exact gate logic matching the exact output (5 dims of the rubric all clear), single-domain, deterministic behavior.

## Audit footer

<!-- SC:TROUBLESHOOT:SUMMARY
status: success
tier_reached: 1
confidence: 0.88
escalation_reason: none
hypothesis_count: 1
adversarial_invoked: false
fix_authorized: false
duration_sec: ~120
-->
