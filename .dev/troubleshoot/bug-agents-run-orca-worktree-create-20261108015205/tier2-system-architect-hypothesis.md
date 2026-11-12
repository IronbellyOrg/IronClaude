# Hypothesis: The empty tab comes from the project rule that requires a bare Orca create (CLAUDE.md:307-308), so the fix belongs in that rule (option A), not in Orca, the installed core file, or orca_worktree.py

<!-- Returned by troubleshoot-analyst (lens system-architect), persisted by parent on receipt 2026-11-08T02:06Z -->

**Agent**: troubleshoot-analyst (lens: system-architect)
**Tier**: 2
**Timestamp**: 2026-11-08T02:06Z
**Cause class**: Other: an instruction that causes the tab says nothing about it. Orca behaves as its help text says.
**Claim class**: `mixed` (`doc_contract`: which instruction owns the step; `runtime_behavior`: Orca opens the tab)
**Evidence class**: `log_evidence`
**Verdict direction**: `AFFIRM`
**Consistency with docs**: aligned
runs-in=CLAUDE.md:308 @ local host (SAME-ENV: yes)

## Claim
The project rule at CLAUDE.md:307-308 requires `orca worktree create`, and that command opens a plain first terminal (P1). The rule that brings the tab into existence should also say what to do with it. Orca cannot own the fix alone: its CLI has no option that skips the first terminal, and a new one would still need an instruction. The installed "Orca session launches" text (B) covers starting new Claude sessions, but most empty tabs come from agents that make a checkout and `cd` into it themselves (11 of 17), which is not a session launch.

## Evidence
- P1 / behaviour-definition: row 1. `IronOrca/src/main/runtime/runtime-local-worktree-terminal-startup.ts:202-210` — `shouldSeedWorktreePrimaryTerminal({ hasPrimarySurface: startupPaneHeld, callerProvidesSurface: callerProvidesInitialSurface(args) })` then `await ports.createTerminal(...)`. Only an agent on the create (`promisedAgentChat` / `createdWithAgent`, :264-265) or a running startup terminal (:147-148) skips the seed.
- Option C has no existing skip: `setupOnly` skips the shell only when a setup hook exists (`runtime-worktree-terminal-provisioning.ts:189`, :203), only on the provisioning path, and only via RPC (`rpc/methods/worktree-create-args.ts:87`). No `setupOnly`/`setup-only` in `IronOrca/src/cli`; N2 lists no such flag.
- `CLAUDE.md:307-310` is the rule; `:312` forbids `git worktree add`; `:320` bare example. `src/superclaude/core/CLAUDE.md:45-53` covers only new Claude sessions. N1: 11 of 17 bare creates followed by `cd` into the checkout. N8: 7 of 7 checked bare-created worktrees have a `hasCommand=false` row.
- No test pins CLAUDE.md:303-325. B carries 12 pinned phrases in two copies, and the installed copy on this host is stale.

## Proposed Fix
Option A only: project `CLAUDE.md`, one file, 2 edits. Add a bullet after :310:
"- A create without `--agent` also opens a plain first terminal. If you will work in the checkout from your own session, close that terminal right after the create, before anything is started there: `orca terminal close --worktree path:<path> --all`. If the checkout is for a new Claude session, put `--agent claude` on the create instead (see "Orca session launches"). `/sc:issue` and supervised workers keep their own launch steps."
Then add the close line to the example block at :318-324.
- Test (new): in `tests/core/`, assert the project CLAUDE.md worktree section contains `orca terminal close --worktree`.
- Live check (pending): V-CLOSE.

## Confidence
Self-reported: 0.66 (runtime part capped at 0.65; log evidence only)
- Evidence grounding: 1.0 — Orca branches and CLAUDE.md lines read this session.
- Runtime check: 0.5 — mixed claim, log evidence; V-CLOSE pending.
- Symptom coverage: 0.5 — covers IronClaude cases; creates in other repos (68fc8b81 in Coder) not covered.
- Reproducibility fit: 0.5 — installed build vs checkout unproven.
- Fix directness: 0.5 — edits the causing rule, depends on agents following it.
- Domain coherence: 1.0 — one file; respects D2, FO-18, WC-13; pinned phrases untouched.

## Risks
- `--all` stops every terminal in that worktree; after an agent launch there it kills that agent. "before anything is started there" is the only guard.
- Only IronClaude sessions on a branch containing the fix see it.

## If I'm wrong, it's probably because...
Many own-use creates happen outside IronClaude; then the owner is B plus a reinstall, or an Orca flag (C).

## Falsification standard
Wrong if a bare `orca worktree create --json`, then `orca terminal close --worktree path:<p> --all` and `orca terminal list --worktree path:<p> --json`, still shows a terminal or the worktree disappears from `orca worktree list` (V-CLOSE fails).

## Evidence classification
- **Claim class**: mixed — instruction ownership plus Orca seeding.
- **Evidence class**: log_evidence — N1, N8 captured by parent; Orca source read.
- **Runtime check performed?**: no — a create changes state.
- **If REFUTE verdict, coverage statement**: Not applicable — AFFIRM.
- Producer citation: P1 (surviving=yes).

## Alternatives considered
- (B) installed core rule plus README copy: rejected for now (subject is session launches; two copies and pinned phrases; does not reach agents here without reinstall).
- (C) new Orca flag: rejected as sole fix (another repo; still needs an instruction); reasonable follow-up.
- (D) `orca_worktree.py`: rejected (none of the observed tabs came from it, N10, N11).

## Grounding gaps
- Diagnosability verdict: partial.
- Repo of most N1 own-use creates not recorded by the worker (parent resolves in N12).
- V-CLOSE and V-JSON pending; compared IronOrca checkout HEAD dc57b3d6e8, not installed 1.4.245-aidev02.
- auggie unavailable.
