<!-- Merged by merge-executor, 2026-10-29. Base: adversarial/variant-2-original.md (Option B). Changes: RP-1..RP-8 of adversarial/refactor-plan.md. -->
<!-- Source tags: V2 = Option B (base), V1 = Option A, V3 = Option C, R2 = debate Round 2, INV-n = invariant-probe.md. Log: adversarial/merge-log.md. -->
# P2 decision: IronClaude removes the Serena registration once codegraph is ready; Coder removes what IronClaude cannot

> **Amended by Phase 2 spec D22-D24 (§2.12), 2026-10-29.** Where this record differs, the spec wins: `env`/`headers` match when absent **or `{}`** (the live entry has `"env":{}`); entries are matched by shape (`start-mcp-server` in args) under any name except `serena-local`; `codegraph_ready()` is the read-only predicate in spec §2.12, ANDed with this run's phase result in `install()`; "never left with neither" is narrowed to "the current-pin Serena entry is never removed while codegraph is missing"; acceptance is the two `jq` checks in spec §2.12; Coder's migration lives in `T/scripts/startup.sh`.

Read `../context.md` first. Chosen: Option B, corrected in debate. Why: every known writer of the current-pin argv is IronClaude or a mirror of its pin, so once codegraph is in place the removal is a replacement, not a deletion.

## The rule (IronClaude, Phase 2) <!-- Source: V2 base; RP-2, RP-3, RP-4, RP-5 -->
- Who: IronClaude's Phase 1 retire step (`install_retired_mcp.py`). `superclaude install` runs it, so `./update.sh` and Coder's slug run it too.
- When: only if `codegraph_ready()` is true. That function is the codegraph phase's own pass check, run after that phase in the same run. `install --list` and `doctor` call the same function. A user-managed codegraph entry whose command resolves counts as ready (INV-010).
- What is removed: every user-scope `serena` launcher entry (argv contains `start-mcp-server`, stdio, no env or headers). Tier R rows are still removed with no condition. A `serena` entry with env or headers is kept and reported.
- Same condition: the kind-B `~/.local/bin/codebase-memory-mcp` registration is removed. Its binary and client companions stay; the upstream `uninstall` command is printed.
- Otherwise (codegraph not ready): nothing changes from Phase 1. Serena is kept and the Tier K line is printed, so the user is never left with neither server.
- Messages: each removal prints the removed argv. The re-register hint uses the name `serena-local`, so the rule never removes it again.

## What Coder must do, and when <!-- Source: RP-1, RP-6; migration from V1/V3, guarded per R2 -->
- Step 2 of Phase 2 §8 (before the IronClaude merge; gate for steps 3-4): the bundle stops registering, installing, warming and health-checking Serena. Tests change with it: test-57 (including `:602-603`), `spec2-health.sh:79`, manifest health, the test-startup-boot handshake proof.
- Also in step 2: `uv tool uninstall serena-agent`, markers, alias, and a guarded one-time migration in `startup.sh`. It runs only when a `codegraph` user entry exists whose command prints `1.6.2`. It then removes `serena` only if it equals the bundle argv, and the exact `/usr/local/bin/codebase-memory-mcp` entry.
- Step 5 (after the pin bump): the image drops `/usr/local/bin/codebase-memory-mcp`.
- Coder confirms which `superclaude` the slug runs, and what an outer `timeout 60` does to the retire step's process group.

## When "completely absent" holds
- Non-Coder machines: right after `./update.sh` (registrations).
- This Coder workspace: registrations right after `./update.sh`; they stay absent once the workspace runs the step-2 image (no re-add), which also removes the Serena programs; the codebase-memory binary goes with the step-5 image.

## Spec amendments in the same merge <!-- Source: RP-7 -->
- Phase 1: §2.3 row, §3.2 Tier K, §3.4 hint, §3.6 row, the sandbox expectation "Legacy Serena registration kept", D2.
- Handoff: §2.4 and §3.2. Phase 2: file table row, §2.1 "can leave neither", §8 steps 2 and 5.

## Acceptance checks <!-- Source: RP-8; tests from V3/R2, checks from V1 -->
- Unit tests: codegraph failed keeps Serena and exits 1; predicate table (owned pinned, user-managed resolving, user-managed not resolving, wrong version); near-miss shapes kept; `serena-local` never removed; idempotent; `install`, `--list` and `doctor` share one function; no registry change when codegraph matches; Tier R `/usr/local/bin` removal stays unconditional.
- Layer-2 sandbox: seed current-pin `serena` and kind-B codebase-memory, assert both gone; same seed with codegraph failing keeps Serena.
- Coder boot tests: step-2 image on the old pin; pin-bump boot; second boot unchanged.
- After every Claude session restarts: `jq -e '[(.mcpServers // {}), (.projects // {} | .[] | .mcpServers // {})] | map(has("serena") or has("codebase-memory-mcp")) | any | not' ~/.claude.json`.
- On Coder, as user coder, only when the image pin >= the merge SHA: `! command -v serena` and `! command -v codebase-memory-mcp`.

## Stated exceptions and escalations
- Kept by policy: `~/.serena`, `~/.cache/codebase-memory-mcp`, the uv cache, project `.serena/`. The acceptance text and CHANGELOG say so.
- Local-scope and `.mcp.json` entries: reported with the exact command, not removed.
- Off Coder, a user-installed Serena uv tool stays; the command to remove it is printed.
- Residual risk: if Coder's `timeout 60` kills a later codegraph remove-then-add after Serena is gone, neither server is registered until the next run (Phase 2 §2.9 leaves a matching entry untouched).
- ESCALATED to the coordinator as unmet: INV-001 (the baked root-owned Coder binary stays until the step-5 image) and INV-002 (the kind-B upstream binary and its client companions; removing them would reopen Phase 1 D2).

## How this was chosen
- Scores: B 0.898, C 0.853, A 0.835. Margin 0.045, so tiebreaker level 1 (debate points won) applied; B won.
- Convergence 18/18 (100%), all taxonomy levels. Invariant gate BLOCKED by INV-001 and INV-002 (escalated); base force-selected by score.
- Taken from A: the single `jq` check and the `command -v` checks; the exact-argv Coder migration. From C: the two-branch test matrix; the guarded migration.
- Rejected: C's provenance-file guard, A's "no IronClaude change", a removal marker file, an unguarded migration.
