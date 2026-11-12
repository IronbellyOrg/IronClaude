# Hypothesis: the #412 "Orca session launches" rule never reaches an orchestrator's loaded instructions, because `superclaude install` keeps an existing `~/.claude/CLAUDE.md` unchanged and the repo's own worktree text then steers toward a bare `orca worktree create`

(Returned by troubleshoot-analyst, persisted by the parent; HTML entities decoded, wording kept, some Evidence lines tightened by the parent.)

**Agent**: system-architect (Tier 2, instruction delivery and install flow)
**Tier**: 2
**Timestamp**: 2026-11-08T00:12:39Z (parent-stamped; the worker wrote a placeholder)
**Cause class**: Config / env drift (a stale installed instruction copy plus an instruction gap)
**Claim class**: `mixed`. The install behaviour is `static_defect`. Whether an LLM follows the rule once delivered is `runtime_behavior`.
**Evidence class**: `source_static`
**Verdict direction**: `AFFIRM`
**Consistency with docs**: aligned. This matches the doc-context.md re-frame signals.
runs-in=unknown

## Claim

`install_core_files` skips every core file that already exists unless `force` is set (`install_core.py:70-72`). A plain `superclaude install` therefore never replaces an existing `~/.claude/CLAUDE.md`, so the #412 rule (`src/superclaude/core/CLAUDE.md:45-53`) never reaches a host that already has one. The only instruction text on this host that covers worktree creation is repo-root `CLAUDE.md:308` and `:320`, which show a bare `orca worktree create` with no `--agent`. The orchestrator is steered to the Orca command that leaves one empty plain terminal.

Different from Tier 1: Tier 1 fixes the repo-root text. This card shows why the rule written for this problem is not delivered, and that a plain `install` does not fix it.

## Evidence

- `/home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/src/superclaude/cli/install_core.py:70-72`: `if dest_file.exists() and not force: skipped.append(...); continue`. No merge, no overwrite for `CLAUDE.md`, which is in `KNOWN_CORE_FILES` (line 19).
- `install_core.py:94-105`: this checkout adds a "kept file(s) differ ... NOT updated" warning; the file is still not updated. The pipx package built 2026-11-05 (O5) predates this checkout; whether the warning is in that package was not checked.
- `/home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/src/superclaude/cli/main.py:178` (`install`) calls `install_core_files(force=force)`, default false; `main.py:365` (`update`) calls it with `force=True`. Only `update` or `install --force` refreshes the file. No Python code outside `install_core.py` writes `CLAUDE.md`.
- The pipx package (built 2026-11-05) predates #415 (2026-11-06T22:19, O5), so `update` from it installs the old text too; the package must be reinstalled from the fork first.
- `~/.claude/CLAUDE.md` has no "Orca session launches" block (matches the parent's 0-match grep, O5).
- Q2/Q3: repo-root `CLAUDE.md:308` and `:320` have no `--agent`. `/home/coder/workspaces/IronClaude/CLAUDE.md` (the project file for a session started at that cwd) has `orca worktree create` at lines 308 and 320 with 0 hits for `--agent` or "Orca session launches". A coordinator started in `/home/coder/workspaces/IronClaude` gets two sources: `~/.claude/CLAUDE.md` without the rule, and the project file with the bare create example. Repo-root `CLAUDE.md` has no `@` import of `core/CLAUDE.md`. When both texts are present they do not contradict each other: the core rule says `worktree create --agent` for a new checkout that needs Claude; the project text only says how to create the worktree.
- Producers: P1 (surviving) is what the project text produces; P2 (surviving) is the plain-shell fallback the missing rule would warn against; P3 and P4 are not affected by instruction delivery.
- behaviour-definition: row 6 (behaviour-definitions.md).

## Proposed Fix

Change `install_core.py` so that, without `--force`, it upserts a marker-delimited block (the style already used by `<!-- SUPERCLAUDE_CODEGRAPH_BEGIN -->` in `core/CLAUDE.md`) into an existing `~/.claude/CLAUDE.md`. The block carries the Orca session-launch rule; the rest of the user's file is untouched.
- `src/superclaude/core/CLAUDE.md`: wrap lines 45-53 in `<!-- SUPERCLAUDE_ORCA_BEGIN -->` and `<!-- SUPERCLAUDE_ORCA_END -->`.
- `src/superclaude/cli/install_core.py`: add the upsert for `CLAUDE.md` when it is skipped.
- Test: a new test in the `install_core` tests: an existing `CLAUDE.md` without the block gains it on a plain install, user text is preserved, and a second run changes nothing.
- Operational stop-gap, not part of the fix: reinstall the package from the fork, then run `superclaude update` (overwrites the user's file).

## Confidence

Self-reported confidence: 0.40 (`mixed` with `source_static`, 0.65 cap, lowered: reporter's orchestrator never observed, `runs-in` unknown).
- Evidence grounding: 0.5 — install code and both CLAUDE.md files Read; reporter's run not seen.
- Runtime check: 0.0 — no executed reproducer; install behaviour follows from source, LLM behaviour does not.
- Symptom coverage: 0.5 — explains why the rule is absent, not the waiting orchestrator by itself.
- Reproducibility fit: 0.5 — delivery is deterministic; the empty terminal is not reproduced.
- Fix directness: 0.5 — delivers the rule; does not make the LLM obey it.
- Domain coherence: 1.0 — fits #412, #415, the O5 grep and the doc-context re-frame signals.

## Risks

- A new upsert path in `install_core.py` edits a file the user may have customised; the block must be strictly marker-bounded.
- If the rule is delivered and the orchestrator still starts bare terminals, the cause is elsewhere (P1 text, P2 or P4) and this fix changes nothing.
- The rule excludes supervised `worker-start`, so it has no effect on that path (`core/CLAUDE.md:52`).

## If I'm wrong, it's probably because...

The rule was delivered to the reporter's session (a different host or a fresh install), and the empty terminal comes from a bare `worktree create`, the UI shortcut or a failed `--agent claude` start (P1, P3 or P4).

## Falsification standard

Run `grep -c "Orca session launches" ~/.claude/CLAUDE.md` on the reporter's host: a count of 1 or more falsifies the delivery claim. Or take the failing orchestrator's transcript and check whether its `orca` calls ran after the rule was loaded.

## Evidence classification

- **Claim class**: `mixed` — install behaviour is static; LLM obedience is dynamic.
- **Evidence class**: `source_static` — source reading only; the parent's 0-match grep is secondary.
- **Runtime check performed?**: no — no shell, reporter's run not supplied.
- **If REFUTE verdict, coverage statement**: Not applicable (AFFIRM).

## Alternatives considered

- Tier 1's repo-root `--agent` wording: a reasonable second change, but it does not fix the missing core rule and is a separate edit.
- Reading `src/superclaude/core/CLAUDE.md` as a nested project file: believed to load lazily, not verified here; in any case the main checkout's copy has no rule.

## Grounding gaps

- `install_ccsession.py` and `install_skills.py` were not Read for the ccsession README; `install_skills.py` has `skill_target.exists() and not force` at line 102, the same skip-without-force pattern.
- How Claude Code orders `~/.claude/CLAUDE.md` against project `CLAUDE.md` when they differ was not checked.
- Whether the stale warning at `install_core.py:94-105` is on origin/master was not checked.
- No transcript of the reporter's run exists. Diagnosability is partial per the parent's card.
