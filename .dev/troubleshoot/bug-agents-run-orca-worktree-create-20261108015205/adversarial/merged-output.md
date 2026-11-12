<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 2 (fix-2) -->
<!-- Merge date: 2026-11-08T02:16Z -->

# Merged Fix: Close the plain first terminal after an own-use bare create; route hand-offs to --agent

Source card: tier2-quality-engineer-hypothesis.md

## Problem statement
<!-- Source: Base (Variant 2, original). "Fix 1" below refers to Variant 1 (variant-1-original.md). -->
Same diagnosis as Fix 1 (bare create seeds a plain first terminal; no instruction says what to do with it; tier1-observation.md N1, N2, N8). The closing step itself must not be able to kill a running setup script (setup/default-tab provisioning is fire-and-forget, IronOrca runtime-local-worktree-terminal-startup.ts:187-201), a reused worktree's live sessions, or the agent's own shell. `--all` "stops every terminal process owned by that workspace" (N3).

## Proposed change
<!-- Source: Base (Variant 2) structure; step 1 replaced from Variant 1 step 1 + Variant 3 bullet, guards from Variant 2 + Variant 3, hand-off routing and exemptions from Variant 1 + Variant 3 (plan Changes 1, 2, 3); step 2 replaced from Variant 3 (plan Change 5); step 3 appended from Variant 1 step 3 (plan Change 4); step 4 Base -->
1. Replace/insert in "Orca session launches" in `src/superclaude/core/CLAUDE.md` (45-53) and `src/superclaude/skills/ccsession-tag/README.md` (228-237):
   "A `worktree create` without `--agent` also opens a plain first terminal. If you will work in that new checkout from your current session, close it right after the create with `orca terminal close --worktree path:<path> --all`, only when you created it with no setup script (`--setup skip` or none configured) and have started nothing in it; never run this on a worktree you did not just create. To hand work to a new Claude session, use `worktree create --agent` instead of a bare create; `/sc:issue` and supervised workers keep their own launch steps."
2. Project `CLAUDE.md`: one bullet after line 310 with the same command and guards in short form:
   "- A create without `--agent` also opens a plain first terminal. If you will work in the checkout from your own session, close it right after the create with `orca terminal close --worktree path:<path> --all`, only with no setup script and before anything is started there; never on a worktree you did not just create. If the checkout is for a new Claude session, put `--agent` on the create instead (see "Orca session launches"). `/sc:issue` and supervised workers keep their own launch steps."
   Plus one comment line in the example block at :318-324 showing that close right after the create.
3. `make sync-dev`, `make verify-sync`. After the change is merged (or with an editable install), run `superclaude update`; plain `superclaude install` keeps the existing ~/.claude/CLAUDE.md (install_core.py:70-72).
4. Leave `orca_worktree.py` unchanged; file a separate issue (its bare create + agent launch likely leaves the same tab; unobserved, N11; changing it breaks pinned `test_fo18_exact_commands_and_no_forbidden_flag`).

## Evidence
<!-- Source: Base (Variant 2, original) -->
IronOrca runtime-local-worktree-terminal-startup.ts:187-214; N3, N7, N8, N11; tests/core/test_orca_session_launch_guidance.py:14-31; tests/skills/test_issue_orca_worktree.py:794-820.

## Risks
<!-- Source: Base (Variant 2) bullets 1-3, written for the base's list-and-handle close that the merge replaced (see dissent (d)); bullets (a)-(d) appended from all advocates, A-001/A-002 QUALIFY (plan Change 7) -->
- If the daemon registers the seed after the create reply, `terminal list` may show zero and the tab survives (harmless, incomplete).
- "Exactly one terminal" could match a setup terminal if the agent misjudges whether setup ran.
- Longer instruction: list + judgment + close.
- (a) Opening the worktree in the Orca UI re-seeds a shell (worktree-activation.ts:275). This is user-driven and acceptable.
- (b) Default tabs configured for a repo start in the background and would also be closed by `--all` (IronOrca runtime-local-worktree-terminal-startup.ts:187-201). The setup-script guard does not cover them.
- (c) Compliance is unproven (A-002): agents may still skip the step.
- (d) Variant 2 dissent: a single-handle close (`orca terminal close --terminal <handle>`) bounds the damage if the guards are misjudged.

## Test plan
<!-- Source: Variant 1 test (pinned phrase, live check) + Variant 3 test (project CLAUDE.md test) + Base run list (plan Change 6); the base's assertion that the section never mentions --all is dropped (X-003) -->
- In tests/core/test_orca_session_launch_guidance.py add pinned phrases "`orca terminal close --worktree`" and "worktree you did not just create" for both copies (core/CLAUDE.md and ccsession-tag/README.md); the 12 existing pinned phrases stay unchanged.
- New small test in tests/core/: assert the project CLAUDE.md worktree section contains `orca terminal close --worktree`.
- `uv run pytest tests/core/test_orca_session_launch_guidance.py tests/core/test_claude_md_routing_block.py tests/skills/test_issue_orca_worktree.py -v` (the last file is unchanged and must keep passing).
- Live V-CLOSE (pending; needs a create).

## Documented constraints to honor
<!-- Source: Base (Variant 2, original; verbatim, identical in all three variants) -->
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
