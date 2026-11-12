# Hypothesis: The installed "Orca session launches" guidance has no step for a bare create's plain first tab, and on this host even the existing guidance is not loaded

<!-- Returned by troubleshoot-analyst (lens root-cause-analyst), persisted by parent on receipt 2026-11-08T02:05Z -->

**Agent**: troubleshoot-analyst (lens: root-cause-analyst)
**Tier**: 2
**Timestamp**: 2026-11-08T02:05Z
**Cause class**: Other: the instructions leave out a step and the installed copy is out of date. Orca behaves as its help text says.
**Claim class**: `mixed` (`doc_contract` + `runtime_behavior`)
**Evidence class**: `log_evidence`
**Verdict direction**: `AFFIRM` (extends the Tier 1 card: fix location, exact command, V-JSON settled from source)
**Consistency with docs**: aligned
runs-in=CLAUDE.md:308 @ local host (SAME-ENV: yes)

## Claim
A bare `orca worktree create` always opens a plain shell as its first tab (P1, behaviour-definition: row 1). The `--json` reply never returns that tab's handle, so an agent cannot close just that one tab from the reply. Agents run the create from many repos (N1: IronOrca, Coder, IronClaude), so the missing step belongs in the installed `core/CLAUDE.md` "Orca session launches" section, not in the project CLAUDE.md. On this host the installed `~/.claude/CLAUDE.md` lacks that section, so agents never see even the existing "`worktree create --agent`" rule; that explains the hand-off cases (N1 44e7b6ec: bare create, then `terminal create`, then a prompt), which already break the current rule.

## Evidence
- `IronOrca/src/main/runtime/runtime-local-worktree-terminal-startup.ts:210` — `await ports.createTerminal(\`id:${worktree.id}\`, { surfaceOwner: false })`; the returned handle is discarded. The result (:223-233) returns only `startupTerminalHandle` (null without an agent). `workspace-creation.ts:239-268` returns only `setupReceipt.terminalHandle`, and only with `awaitTerminalProvisioning`. Settles V-JSON from checkout source: no seeded-tab handle in the reply.
- Race (source): with no setup and no default tabs the seed is awaited inside the create (`workspace-creation.ts:209`). With setup or default tabs and no `--activate`, provisioning is fire-and-forget (`runtime-local-worktree-terminal-startup.ts:196-197` `void provisioning`) and seeds later (`runtime-worktree-terminal-provisioning.ts:202-211`). The plain CLI create never sets `awaitTerminalProvisioning` (only `agent-launch-worktree-creation.ts:102`, `worker-worktree-creation.ts:80`, `federated-worker-agent-launch.ts:82`). A close right after the reply can miss a late seed.
- `src/superclaude/core/CLAUDE.md:45-53` covers launching a session but not the first tab. The `~/.claude/CLAUDE.md` loaded into this session has no "Orca session launches" section (session context; parent to re-verify on disk).
- Daemon log (N8): 5 of 5 hand-offs show a `hasCommand=false` seed then a separate `true` row; 2 own-use worktrees still have the empty tab (N7).

## Proposed Fix
Add one sentence to "Orca session launches" in `src/superclaude/core/CLAUDE.md` (after line 51, "...to use ccsession.") and its mirror `src/superclaude/skills/ccsession-tag/README.md`; then `make sync-dev` and `superclaude install`/`update` so `~/.claude/CLAUDE.md` gets the section:
"A `worktree create` without `--agent` also opens a plain shell tab; if you will work in the new checkout from your current session, close it right after the create with `orca terminal close --worktree path:<path> --all`; to hand work to a new Claude session, use `worktree create --agent` instead of a bare create."
The close is only for own use, where no other tab exists yet, so `--all` cannot kill an agent.
- No change to the project `CLAUDE.md` (it defers to installed rules; an IronClaude-only line misses other repos).
- Test: add 13th phrase "`orca terminal close`" to `tests/core/test_orca_session_launch_guidance.py:17-30`; both copies must pass.

## Confidence
Self-reported: 0.72
- Evidence grounding: 1.0 — Orca source read this run, plus daemon rows N8.
- Runtime check: 0.5 — log evidence only; no live create.
- Symptom coverage: 1.0 — own use (new step) and hand-off (stale install plus existing `--agent` rule).
- Reproducibility fit: 0.5 — installed 1.4.245 vs checkout unproven.
- Fix directness: 0.5 — depends on agents following text and on a reinstall.
- Domain coherence: 0.5 — docs plus a pinned-phrase test.

## Risks
- With setup hooks or default tabs the seed can land after the close; one empty tab survives. Probe: `orca terminal list --worktree path:<p> --json` 5 s after create plus close.
- Without `superclaude install` the fix never reaches agents.
- `--all` after `agent launch` kills that agent; the sentence limits it to own use.

## If I'm wrong, it's probably because...
The installed 1.4.245 binary returns the seed's handle or waits for provisioning, unlike checkout HEAD dc57b3d6e8.

## Falsification standard
Wrong if `orca worktree create --name t --no-parent --json` then `orca terminal close --worktree path:<p> --all` then, after 5 s, `orca terminal list --worktree path:<p> --json` lists any tab, with setup skipped and no default tabs.

## Evidence classification
- **Claim class**: mixed — instruction gap plus Orca seeding behaviour.
- **Evidence class**: log_evidence — N1, N7, N8 from the parent; Orca source read for the mechanism.
- **Runtime check performed?**: no — a create changes state.
- **If REFUTE verdict, coverage statement**: Not applicable — AFFIRM.
- Producer citation: P1 (surviving=yes), plus the provisioning seed at `runtime-worktree-terminal-provisioning.ts:202-211`.

## Alternatives considered
- Step only in the project CLAUDE.md: rejected (N1 creates in IronOrca and Coder too).
- List tabs and close one handle: rejected (no handle in the reply; picking a tab needs judgment).
- Fix `orca_worktree.py`: deferred, not rejected — by P1 its bare create (:594-610) then `agent launch` (:951-953) should leave the same tab; N11 shows it never ran here.

## Grounding gaps
- Installed binary not compared with the checkout; default tabs / setup hook config unknown (no `orca.yaml` in repo).
- Stale `~/.claude/CLAUDE.md` from session context, not re-read from disk.
- Diagnosability: partial; agents' reasons inferred from next commands.
