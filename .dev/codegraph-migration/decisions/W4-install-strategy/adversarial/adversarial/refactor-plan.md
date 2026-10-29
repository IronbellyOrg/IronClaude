# Refactoring Plan

## Overview
- Base variant: Variant 3 (Option C, original), combined score 0.879
- Incorporated variants: Variant 1 (Option A), many mechanisms; Variant 2 (Option B), two test and safety ideas
- Planned changes: 12
- Rejected alternatives: 5
- Overall risk: Medium. The base's "fail or fallback" becomes "always fallback", which changes its behaviour on non-Coder machines.
- Target artifact: `.dev/codegraph-migration/decisions/W4-install-strategy/adversarial/W4-install-strategy-merged.md`, a decision record. It must stay a planning document: no source, test or doc edits.

## Planned Changes

### Change 1: The verified download becomes the required fallback, not an option
- Source: V1 "What it does" bullets 2-3, from the pinned URL through the extract and links into `~/.codegraph/versions/v1.6.2/` and `~/.local/bin/codegraph`.
- Target: base "What it does" bullet 2, replacing "fails with a clear message, or falls back to Option A's verified download (if both are built)".
- Rationale: C-001 (unanimous combo, 95%), C-010 (V1 93%), and all three advocates' recommended combination.
- Approach: replace.
- Risk: Medium.

### Change 2: One pin and one hash table, both owned by IronClaude
- Source: V1 "Version bumps = edit pin + hashes in one place, tested by unit tests", and V1 Strengths "one place to bump".
- Target: base bullet 3, "Version bumps require an image rebuild plus an IronClaude pin bump, kept in sync".
- Rationale: C-008 (V1 80%), X-002 (V1 82%). C's advocate conceded the two-repo cost.
- Approach: replace. The Coder Dockerfile bakes the same pin and hash, copied from the IronClaude values. A rebuild is a speed-up, not a dependency. A stale image is detected (version mismatch) and repaired by the fallback.
- Risk: Low.

### Change 3: Exact gate, then register the absolute path of the binary that passed it
- Source: debate A-003 (unanimous, V3 plus absolute path, 90%).
- Target: base bullet 2, the registration clause.
- Rationale: a bare `"command":"codegraph"` depends on PATH order when both a baked copy and a user copy exist. On Coder the baked copy is in `/usr/local/bin`; otherwise the user copy is in `~/.local/bin`.
- Approach: modify. Candidate order: (1) `/usr/local/bin/codegraph` (or whatever `which codegraph` resolves to), (2) `~/.local/bin/codegraph`. The first whose `--version` equals the pin wins and its realpath is registered.
- Risk: Low.

### Change 4: MCP `env` turns off telemetry and the update check
- Source: V1 bullet 4 JSON `"env":{"CODEGRAPH_TELEMETRY":"0","CODEGRAPH_NO_UPDATE_CHECK":"1"}`.
- Target: the base registration command, plus the image env.
- Rationale: C-006 (V1 93%). The V2 advocate showed that a root-owned install which keeps prompting for upgrades is a defect.
- Approach: modify.
- Risk: Low.

### Change 5: No prompt hook, and never run upstream installers
- Source: V1 bullet 5 ("Does not install the `UserPromptSubmit` prompt hook") and bullet 6 ("Never runs `codegraph install`").
- Target: a new "Explicitly not done" list.
- Rationale: C-005 (V1 93%), X-001 (V1 95%, conceded by B), eval §5.9 (41-symbol payload).
- Approach: insert.
- Risk: Low.

### Change 6: Guidance and permission owned by IronClaude
- Source: V1 bullet 5 (`src/superclaude/core/CLAUDE.md` plus `mcp__codegraph__*` through IronClaude settings handling).
- Target: base bullet 2 ("relies on `src/superclaude/core/CLAUDE.md` for guidance"), extended with the permission.
- Rationale: C-004 (95%), `install_core.py:62-71`.
- Approach: modify.
- Risk: Low.

### Change 7: Receipt and removal for the user copy only
- Source: V1 bullet 6 (receipt plus removal reuse the `install_codebase_memory.py` pattern).
- Target: a new bullet.
- Rationale: C-011 (V1 72%). The baked copy is image-owned and IronClaude never removes or writes `/usr/local/bin`.
- Approach: insert.
- Risk: Low.

### Change 8: Running daemons when the user copy is swapped
- Source: debate A-004 (V1 plus daemon handling, 68%, majority). From the V2 advocate: `install.sh` prunes old `versions/*`. From the V3 advocate: a newer client talking to an older running daemon is untested.
- Target: a new bullet under the fallback.
- Approach: insert. Install into `versions/<tag>/`, flip the symlink, leave the previous version directory until the next run, and warn that open sessions keep the old daemon until the 300 s idle timeout (eval §5.7). Never delete a version directory in the same run that flips the symlink.
- Risk: Medium. Untested; carried as a condition.

### Change 9: Claude CLI readiness guard
- Source: debate A-002 (88%). `install_codebase_memory.py:614` already leaves Claude CLI readiness to its caller.
- Target: before registration.
- Approach: insert.
- Risk: Low.

### Change 10: Drift check against upstream config shape, test-time only
- Source: the V2 advocate's recommended combination (`codegraph install --print-config claude` writes nothing, eval §5.9).
- Target: a new "Tests" bullet.
- Approach: insert. A recorded fixture of the `--print-config` output is refreshed on each pin bump. A unit test compares IronClaude's `add-json` entry with it, ignoring IronClaude's added `env`. It never runs during `superclaude install`.
- Risk: Low.

### Change 11: `codegraph upgrade` is unsupported and detected
- Source: the V2 advocate's weakness #1 against A, conceded by the V1 advocate.
- Target: a new "Explicitly not done" bullet plus a doctor check.
- Approach: insert. Documentation says not to run `codegraph upgrade` or `codegraph install`. `superclaude doctor` (run by `./update.sh`) flags a codegraph version that differs from the pin, a `CODEGRAPH_START` block in `~/.claude/CLAUDE.md`, or a `codegraph prompt-hook` entry in `~/.claude/settings.json`.
- Risk: Low.

### Change 12: Conditions and out of scope
- Source: debate A-001 (unanimous gap, 90%), A-005, and the concessions from all advocates.
- Target: a new "Conditions and risks" section.
- Approach: append. Per-worktree `codegraph init` needs a separate owner and decision. Also list: maintaining 4 hashes per release, the single-maintainer upstream, image growth of about 286 MB, GitHub availability for fallback machines, and `gh attestation verify` as optional and non-blocking.
- Risk: Low.

## Changes NOT Being Made
| Diff Point | Non-base approach | Rationale |
|---|---|---|
| C-001 / C-002 | B: delegate acquisition to upstream `install.sh` | It has no checksum step (`install.sh:71-82`, eval §1), and B conceded this. A hash check in advance cannot cover bytes from a separate download. |
| X-001 / C-003 | B: `codegraph install --target=claude --location=global --yes` | It edits `~/.claude.json`, `settings.json` and `CLAUDE.md`, and `--force` erases the block (`install_core.py:62-71`). B conceded. |
| C-005 | B: install the `UserPromptSubmit` prompt hook | It adds context nobody chose (eval §5.9). It can be revisited as an explicit opt-in later. |
| C-007 | A: user-writable `~/.local/bin` everywhere, Coder included | The V3 advocate's attack-surface argument holds: an `alwaysLoad` binary runs every session. On Coder the root-owned baked copy is preferred whenever its version matches. |
| U-001 | A: `gh attestation verify` as part of the check | It needs GitHub auth and writes a sigstore cache under `$HOME` (eval §5.1). Kept optional and non-blocking only. |

## Risk Summary
| Change | Risk | Impact | Rollback |
|---|---|---|---|
| 1 | Medium | Non-Coder and stale-image machines download 63 MB and write 286 MB | Revert to C's fail-with-message |
| 2 | Low | The image must copy the IronClaude pin and hash | Image keeps its own pin; the gate still detects a mismatch |
| 3 | Low | Absolute path must be re-registered when the winning binary changes | Bare command |
| 8 | Medium | A daemon can run an older version for up to 300 s | Document "restart sessions after update" |
| others | Low | — | Remove the bullet |

## Review Status
- Approval: auto-approved (non-interactive)
- Timestamp: 2026-10-29T16:35:00Z
