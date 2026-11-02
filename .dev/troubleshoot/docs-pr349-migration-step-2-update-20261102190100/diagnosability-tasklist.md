# Diagnosability Tasklist
**Issue**: release notes migration step 2 uses `superclaude update`, which skips the codegraph phase and the retire step
**Verdict**: partial  **Complexity**: trivial  **failing_component**: docs/releases/v5.0.0.md  **Round**: 0 of 3  **re-run permitted**: unknown  **discriminator-required**: no  **capability-verdict**: n/a
**branch**: ironbelly/release-v5.0.0  **repro-venue-id**: superclaude update on a pre-codegraph install

## Emitter search
emitter-search: n/a (no single-expression predicate; the defect is documentation text)
emitters-found: 2 (src/superclaude/cli/doctor.py:164 detail "no codegraph registration; run `superclaude install`"; src/superclaude/cli/install_mcp.py codegraph_ready_line via doctor.py:208)
already-read-files: 6
usable-capture-routes: 2 (`superclaude doctor --verbose` prints doctor.py:164; `superclaude install --list` prints the codegraph block) — both are invocation-site reads, no production-source change

## Discriminator rows
core-rows=1, pack-rows=0, total-rows=1
- M1 (core). Claim: following migration step 2 (`pipx install --force ...` then `superclaude update`) leaves codegraph unregistered on a pre-codegraph install. Observable: `superclaude doctor --verbose` codegraph detail lines, or `claude mcp get codegraph`. Probe: in a throwaway HOME with a pre-codegraph install, run step 2, then the observable. value-if-claim-true: "no codegraph registration; run `superclaude install`" / registration absent | value-if-false: a registered codegraph command line. Outcome mapping: true-value → consistent; false-value → refuted; empty/error → unobserved. Provenance: static reading of main.py:340-429, :407. State: pending — not run (would need a throwaway install environment; re-run permitted: unknown).

## Fix candidate
Docs-only: replace `superclaude update` with `superclaude install --force` in migration step 2 (and :3, :69, :150), and change step 4 to check `superclaude doctor --verbose` / `superclaude install --list` for a registered codegraph. Paired verification: M1 under the new instructions should show a registered codegraph. Applied by sc:pr-submit (fix authorized), not by this skill.

## Hard Constraints
- INVOCATION SITES only; ADDITIVE only; each task is annotated `# Diagnosability-tasklist instrumentation: revert after defect closed.`

## Implementation tasks
### Task 1: Verify the upgrade with verbose doctor output (task type 1, env/flag override at the invocation site)
- Invocation site: docs/releases/v5.0.0.md migration step 4 (the documented verification command).
- Current: "`superclaude doctor` passes".
- Change: run `superclaude doctor --verbose` and require a codegraph registration line. # Diagnosability-tasklist instrumentation: revert after defect closed. (Here the change is permanent documentation; no revert needed once the notes are fixed.)
- Linked measurement: M1. Rationale: answers the "why" W (doctor.py:164 is verbose-only).
- Verification: the step names a command whose default output distinguishes registered vs missing codegraph. Rollback: restore the previous step text.

## Verification
M1 pending; the docs fix is verified by re-reading the notes against main.py:242-267 and :407.
## Rollback
Revert the docs commit.
## Patch-round counter
discriminator-required: no; counter not incremented (store .dev/troubleshoot/diagnosability-rounds.json untouched).
