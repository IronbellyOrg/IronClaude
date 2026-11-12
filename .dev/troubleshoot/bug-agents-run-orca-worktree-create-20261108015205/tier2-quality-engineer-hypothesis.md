# Hypothesis: The Tier 1 fix is right that a step is missing, but `--all` is unsafe as the closing step. Close only the one seeded tab, by its handle, and only when the create ran no setup.

<!-- Returned by troubleshoot-analyst (lens quality-engineer), persisted by parent on receipt 2026-11-08T02:06Z -->

**Agent**: troubleshoot-analyst (lens: quality-engineer)
**Tier**: 2
**Timestamp**: 2026-11-08T02:06Z
**Cause class**: Other: the instructions leave out a step. The proposed step has an unsafe scope.
**Claim class**: `mixed` (`doc_contract` plus `runtime_behavior`)
**Evidence class**: `source_static`
**Verdict direction**: `AFFIRM`
**Consistency with docs**: aligned
runs-in=CLAUDE.md:308 @ local host (SAME-ENV: yes)

## Claim
P1 opens a plain first tab after a create with no agent, and nothing in the rules says to close it. The Tier 1 wording is the problem: `orca terminal close --worktree path:<p> --all` "stops every terminal process owned by that workspace" (N3). P1's seed runs only when the create starts no setup and opens no default tabs; otherwise Orca opens those tabs in the background, so `--all` right after the create could kill a running setup script. Reused on an existing worktree, `--all` kills live sessions, including the agent's own shell if it runs there. Closing the single seeded tab by handle avoids all three.

## Evidence
- behaviour-definition: row 1; `IronOrca/src/main/runtime/runtime-local-worktree-terminal-startup.ts:187-201` — `else if (ports.canSpawn && (setup || defaultTabs || didSpawnStartup)) { const provisioning = ports.provision({...}) ... void provisioning`. The seed at `:202-214` is the `else` of that branch.
- N3: "With --worktree <selector> --all, stops every terminal process owned by that workspace and durably removes its terminal tabs, layouts, and resume records." N7: `fix-flaky-parallel-thread-test` has two empty-titled tabs (term_9fe9e46e, term_ee0007a6).
- Tests: `tests/core/test_orca_session_launch_guidance.py:14-31` checks 12 phrases between `### Orca session launches` and the next `\n## ` in both copies. `tests/core/test_claude_md_routing_block.py:21-50` checks only the level-table block and its tail; the Orca section (`core/CLAUDE.md:45-53`) is outside it. The two copies already differ (`core/CLAUDE.md:51` vs `README.md:234-235`); no test requires them to match. No `plugins/superclaude/**` mirror exists. No test pins project `CLAUDE.md:303-325`.
- `/sc:issue`: `orca_worktree.py:594-610` creates with no `--agent`, `--setup` or `--activate`, so by P1 it seeds a plain tab, and `agent launch` opens a separate one (N4, N8 pattern); unobserved here (N11). `tests/skills/test_issue_orca_worktree.py:794-820` pins the exact call list of the `worktree` subcommand (`test_fo18_exact_commands_and_no_forbidden_flag`); `:1035-1071` pin `launch` calls.

## Proposed Fix
Keep Tier 1 placement; replace the sentence in both copies with:
"A `worktree create` without `--agent` and without a setup script also opens one plain first terminal; right after that create, before any `agent launch`, run `orca terminal list --worktree path:<path> --json` and, if it shows exactly one terminal, close it with `orca terminal close --terminal <handle>`. Never use `--all`, and never close terminals in a worktree you did not just create."
Add the project `CLAUDE.md` bullet after `:310`. Leave `orca_worktree.py` alone (predicted, unobserved; pinned tests); record a separate issue naming `test_fo18...`.
- Files: `src/superclaude/core/CLAUDE.md` (45-53), `src/superclaude/skills/ccsession-tag/README.md` (228-237), `CLAUDE.md` (after 310). Run `make sync-dev`, `make verify-sync`.
- Test: in `tests/core/test_orca_session_launch_guidance.py` add phrases "`orca terminal close --terminal`" and "before any `agent launch`", plus `assert "--all" not in section` for both copies. Run `uv run pytest tests/core/test_orca_session_launch_guidance.py tests/core/test_claude_md_routing_block.py tests/skills/test_issue_orca_worktree.py -v` (last file unchanged and passing).
- Live check (pending): V-JSON, then V-CLOSE with `--terminal`.

## Confidence
Self-reported: 0.72
- Evidence grounding: 1.0 — Orca branch structure, tests and copy rules read directly.
- Runtime check: 0.5 — source only; setup race and seed timing not observed.
- Symptom coverage: 1.0 — own use and hand-off.
- Reproducibility fit: 0.5 — installed 1.4.245 vs checkout unproven.
- Fix directness: 0.5 — wording; depends on agents following it.
- Domain coherence: 0.5 — docs and a test.

## Risks
- If the daemon registers the seeded tab 2-3 s after the create returns (N8 timing), `terminal list` may show zero terminals and the tab survives; harmless but incomplete. V-JSON decides.
- "Exactly one terminal" can match a setup terminal if the agent misjudges whether setup ran.

## If I'm wrong, it's probably because...
The bare `--json` create already returns the seeded tab's handle (N5's tail was cut off), so `--terminal <handle-from-create>` is simpler.

## Falsification standard
Wrong if V-CLOSE shows `orca terminal close --terminal <seeded handle>` failing or leaving the tab, or if a bare create with a setup script still produces a `hasCommand=false` row.

## Evidence classification
- **Claim class**: mixed — omitted doc step plus Orca branching.
- **Evidence class**: source_static — Orca source and tests read, no execution.
- **Runtime check performed?**: no — a create is a mutation.
- **If REFUTE verdict, coverage statement**: Not applicable — AFFIRM.
- Producer citation: P1 (surviving=yes), `runtime-local-worktree-terminal-startup.ts:202`.

## Alternatives considered
- Keep `--all` with "before any launch": rejected (does not protect a setup terminal, a reused worktree or the agent's own shell).
- Fix `orca_worktree.py` in the same change: rejected for now (unobserved, N11; breaks pinned call lists at `test_issue_orca_worktree.py:800-820`).

## Grounding gaps
- Diagnosability verdict: partial. V-JSON and V-CLOSE pending. Create-with-existing-name behaviour not checked. `provisionArgs` (`:236`) and how `defaultTabs` is set not read. auggie unavailable.
