# Fix 2: Add the step to both installed copies and the project rule, but close only the one seeded tab by handle, never `--all`

Source card: tier2-quality-engineer-hypothesis.md

## Problem statement
Same diagnosis as Fix 1 (bare create seeds a plain first terminal; no instruction says what to do with it; tier1-observation.md N1, N2, N8). The closing step itself must not be able to kill a running setup script (setup/default-tab provisioning is fire-and-forget, IronOrca runtime-local-worktree-terminal-startup.ts:187-201), a reused worktree's live sessions, or the agent's own shell. `--all` "stops every terminal process owned by that workspace" (N3).

## Proposed change
1. Replace/insert in "Orca session launches" in `src/superclaude/core/CLAUDE.md` (45-53) and `src/superclaude/skills/ccsession-tag/README.md` (228-237):
   "A `worktree create` without `--agent` and without a setup script also opens one plain first terminal; right after that create, before any `agent launch`, run `orca terminal list --worktree path:<path> --json` and, if it shows exactly one terminal, close it with `orca terminal close --terminal <handle>`. Never use `--all`, and never close terminals in a worktree you did not just create."
2. Project `CLAUDE.md`: one bullet after line 310 pointing to that sentence.
3. `make sync-dev`, `make verify-sync`.
4. Leave `orca_worktree.py` unchanged; file a separate issue (its bare create + agent launch likely leaves the same tab; unobserved, N11; changing it breaks pinned `test_fo18_exact_commands_and_no_forbidden_flag`).

## Evidence
IronOrca runtime-local-worktree-terminal-startup.ts:187-214; N3, N7, N8, N11; tests/core/test_orca_session_launch_guidance.py:14-31; tests/skills/test_issue_orca_worktree.py:794-820.

## Risks
- If the daemon registers the seed after the create reply, `terminal list` may show zero and the tab survives (harmless, incomplete).
- "Exactly one terminal" could match a setup terminal if the agent misjudges whether setup ran.
- Longer instruction: list + judgment + close.

## Test plan
- Add phrases "`orca terminal close --terminal`" and "before any `agent launch`" plus `assert "--all" not in section` to tests/core/test_orca_session_launch_guidance.py for both copies.
- `uv run pytest tests/core/test_orca_session_launch_guidance.py tests/core/test_claude_md_routing_block.py tests/skills/test_issue_orca_worktree.py -v`.
- Live V-JSON then V-CLOSE with `--terminal` (pending).

## Documented constraints to honor
(verbatim from doc-context.md)

### Restrictions / decisions that constrain the fix

- `CLAUDE.md:307` (worktree creation) — "every project worktree is created through Orca"
- `CLAUDE.md:312` (worktree creation) — "Never create a project worktree with raw `git worktree add` ..."
- `CLAUDE.md:314` / `:54` (link flags) — never pass `--issue`, `--pr` or other Orca link flags for this repo
- `src/superclaude/core/CLAUDE.md:47-52` (session launch) — new Claude session = Claude (CLI) / `worktree create --agent` / `agent launch`; `worker-start` stays authoritative for supervised workers
- `src/superclaude/core/WORKER-CONTRACT.md:62` (workers) — workers never call `worktree create --agent` or `agent launch`
- `src/superclaude/skills/sc-issue-protocol/SKILL.md:176` and tests/skills/test_issue_orca_worktree.py:264-279 — `--agent` is forbidden on /sc:issue's create step
- tests/core/test_orca_session_launch_guidance.py:10-31 — 12 phrases pinned in both copies of "Orca session launches" (core/CLAUDE.md and ccsession-tag/README.md)

### Re-frame signals

- The empty tab is Orca's documented default ("By default this creates the worktree and its first terminal", `orca worktree create --help`, tier1-observation.md N2), and the repo rule tells agents to run exactly that bare create. The defect is the missing instruction for what to do with that first terminal, not a code deviation.
- Adding `--agent` is the wrong fix for most observed cases: 11 of 17 bare creates were followed by the same session cd-ing into the checkout (tier1-observation.md N1), and `--agent` is forbidden for /sc:issue's create step and for supervised workers.
- No doc tells an agent to close or reuse the seeded terminal; that gap is where a fix fits.
