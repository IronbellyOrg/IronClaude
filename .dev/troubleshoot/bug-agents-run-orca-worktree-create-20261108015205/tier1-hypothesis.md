# Hypothesis: The repo's worktree rule tells agents to run a bare `orca worktree create` but never says what to do with the plain first terminal that Orca opens, so that tab is left unused every time

<!-- Returned by troubleshoot-analyst (lens root-cause-analyst), persisted by parent on receipt 2026-11-08T02:00Z -->

**Agent**: troubleshoot-analyst (lens: root-cause-analyst)
**Tier**: 1
**Timestamp**: 2026-11-08T02:00Z
**Cause class**: Other: the instructions leave out a step. Orca behaves as documented and the code has no defect.
**Claim class**: `mixed` (`doc_contract`, because the rule leaves out a step, plus `runtime_behavior`, because Orca opens the tab)
**Evidence class**: `log_evidence`
**Verdict direction**: `AFFIRM`
**Consistency with docs**: aligned
runs-in=CLAUDE.md:308 @ local host (SAME-ENV: yes)

## Claim
When `orca worktree create` has no `--agent`, Orca opens a plain shell as the worktree's first terminal (P1, `IronOrca/src/main/runtime/runtime-local-worktree-terminal-startup.ts:202`). The repo rule tells agents to run exactly that bare create (`CLAUDE.md:308`, example at `:320`). Neither that rule nor the "Orca session launches" section says to use or close the first terminal. Agents then either `cd` into the checkout from their own session (11 of 17 creates) or start the work in a new tab (5 of 17), and both leave the first tab empty.

## Evidence
- P1 / behaviour-definition: row 1. `shouldSeedWorktreePrimaryTerminal(...)` returns true when `callerProvidesSurface` is false, then `ports.createTerminal(id:${worktree.id}, { surfaceOwner: false })` runs with no startup command (tier1-observation.md, Behaviour definitions, :202-214 and :259-269).
- `CLAUDE.md:308` — "Create it with `orca worktree create --name <name>`"; `:320` — `orca worktree create --name pm-agent --base-branch origin/master`. Nothing in 303-325 mentions `--agent`, the first terminal, or `terminal close`.
- Log evidence (tier1-observation.md N1, N8): 17 of 18 hand-typed creates had no `--agent`. In 7 of 7 checked bare-created worktrees a daemon `hasCommand=false` row appears 2-3 s after the create. In all 5 hand-off cases a separate `hasCommand=true` row follows, so the first tab is never reused. In 2 own-use worktrees the empty tab is still open (N7).
- `--agent` cannot be required everywhere: `docs/designs/sc-issue-claim-pipeline-flag.md:370` (D2) "no `--agent` on create", `:333` (FO-18) forbids it; `src/superclaude/core/WORKER-CONTRACT.md:62` (WC-13) workers never call `worktree create --agent`; `orca_worktree.py:594-610` creates bare then `orca agent launch ... --surface terminal` at `:951-953`.

## Proposed Fix
Add the missing step and keep everything that exists. Insert one sentence into "Orca session launches", after the line ending "`--surface terminal` when a CLI session is required.", in both copies, keeping all 12 pinned phrases:

"A `worktree create` without `--agent` also opens a plain first terminal; when you work in the checkout from your own session, or will start the agent with `agent launch`, close it right after the create with `orca terminal close --worktree path:<path> --all`, before any launch."

In the project `CLAUDE.md`, add one bullet after `:310` pointing to that step and saying to use `--agent` on the create when the point is a new Claude session (not for `/sc:issue` or supervised workers).
- `src/superclaude/core/CLAUDE.md` (47-53): add the sentence.
- `src/superclaude/skills/ccsession-tag/README.md` (230-237): add the same sentence.
- `CLAUDE.md` (project, after 310): add one bullet.
- Test: extend `tests/core/test_orca_session_launch_guidance.py` with a 13th pinned phrase "`orca terminal close`" for both copies; the 12 existing phrases must still pass.
- Live check (pending; needs a create): V-CLOSE in diagnosability-tasklist.md.

## Confidence
Self-reported: 0.70
- Evidence grounding: 1.0 — Orca source and daemon rows quoted for 7 instances.
- Runtime check: 0.5 — log evidence only, no live reproduction (re-run permitted: unknown).
- Symptom coverage: 1.0 — explains both own-use and hand-off cases.
- Reproducibility fit: 0.5 — checkout vs installed 1.4.245 equality not proven.
- Fix directness: 0.5 — instruction change; depends on agents following it; V-CLOSE unverified.
- Domain coherence: 1.0 — respects D2, FO-18, WC-13 and pinned phrases.

## Risks
- `--all` stops every terminal in the worktree; run after `agent launch` it kills that agent ("before any launch").
- If V-JSON shows a bare `--json` create returns the first terminal's handle, `--terminal <handle>` is safer.

## If I'm wrong, it's probably because...
`/sc:issue` creates leave no first terminal (control row M-CTRL); if so, something besides "no `--agent`" decides whether the tab opens.

## Falsification standard
Wrong if a bare `orca worktree create --json` followed at once by `orca terminal list --worktree path:<p> --json` returns zero terminals, with no `hasCommand=false` daemon row for that worktree.

## Evidence classification
- **Claim class**: mixed — instruction omission plus Orca runtime behaviour.
- **Evidence class**: log_evidence — transcripts and daemon.log captured by the parent (N1, N6, N8).
- **Runtime check performed?**: no — a create changes state; re-run not authorized.
- **If REFUTE verdict, coverage statement**: Not applicable — AFFIRM.
- Producer citation: P1 (surviving=yes), `runtime-local-worktree-terminal-startup.ts:202`.

## Alternatives considered
- "Agents should always pass `--agent`." Rejected: 11 of 17 own-use creates would start an unwanted session; D2/FO-18/WC-13 forbid it; `core/CLAUDE.md:49` already covers hand-offs.
- "Fix `orca_worktree.py` to close the first terminal." Rejected for now: M-CTRL shows no leftover tab on the issue-* worktrees; the complaint is about hand-typed creates.

## Grounding gaps
- Diagnosability verdict: partial (diagnosability-context.md). Agents' reasons are inferred from their next commands.
- M-CTRL creation commands not captured (CONTROL-PROOF: unknown); unresolved against P1 for `orca_worktree.py`'s own bare create.
- V-CLOSE and V-JSON pending. Installed build vs IronOrca checkout (HEAD dc57b3d6e8) equality not proven.
- auggie unavailable; sources Read directly.
