# Merge Log

## Metadata
- Base: Variant 3 (Option C, original), `variant-3-original.md`, combined score 0.879
- Incorporated: Variant 1 (Option A), Variant 2 (Option B, advocate ideas only), debate points A-001..A-005
- Plan: `refactor-plan.md` (12 changes, auto-approved 2026-10-29T16:35:00Z)
- Executor: merge-executor (sc:adversarial Mode A, depth quick)
- Output: `../W4-install-strategy-merged.md`
- Changes applied: 12 of 12
- Status: COMPLETE
- Timestamp: 2026-10-29T16:40:00Z

## Structural changes made outside the 12 changes (required by the brief, no new content)
- Title extended to name the merged decision. Tag: "Base (original, modified)".
- New "Decision" summary section at the top, built only from the 12 changes and their cited debate points.
- Base "What it does" bullets split into subsections (a)-(d) so each change has one home. The base's H2 order (What it does, Strengths, Weaknesses) is kept.
- "Rejected alternatives" and "Debate summary" sections added from the plan's "Changes NOT Being Made" and the transcript/base-selection scores.

## Changes

### Change 1: verified download becomes the required fallback
- Status: applied
- Before: "If missing (non-Coder machine), it fails with a clear message, or falls back to Option A's verified download (if both are built)."
- After: step (b)3, the fallback runs whenever no candidate passes the gate, with the pinned URL, 4-platform hash table, `~/.codegraph/versions/v1.6.2/`, `~/.local/bin/codegraph` and `~/.codegraph/current`, plus a stale-image warning on Coder.
- Provenance tag: "Variant 1 (Option A), What it does bullets 2-3 — merged per Change 1"
- Validation: the "fail with a message" path is gone everywhere; the base Weakness "Non-Coder installs still need an install path" was removed as resolved.

### Change 2: one pin and one hash table owned by IronClaude
- Status: applied
- Before: "Version bumps require an image rebuild plus an IronClaude pin bump, kept in sync."
- After: (d) "One place in IronClaude: the pin plus the 4 hashes, covered by unit tests"; (a) the image copies the IronClaude values and baking is an optimization, not a dependency.
- Provenance tag: "Base (original, modified) — two-repo sync replaced by single IronClaude bump point; merged per Changes 2 and 10" and on (a)
- Validation: the base Weakness "Two repos must agree" was rewritten as "the image still has to copy the pin and hash; a missed copy costs speed, not correctness".

### Change 3: exact gate, then register the absolute path of the winner
- Status: applied
- Before: "checks `codegraph --version` equals the IronClaude-expected version; if present, only registers the MCP server" with a bare command.
- After: step (b)2, ordered candidates (`/usr/local/bin/codegraph` or the PATH-resolved one, then `~/.local/bin/codegraph`), first exact match wins; step (b)5 registers its realpath and re-registers when the winner changes.
- Provenance tag: "Base (original, modified) plus debate A-003 — merged per Change 3"
- Validation: the JSON uses `"command":"<abs path>"`, never a bare `codegraph`.

### Change 4: MCP `env` turns off telemetry and the update check
- Status: applied
- Before: image env set only `CODEGRAPH_TELEMETRY=0`; the registration had no env.
- After: image env sets both `CODEGRAPH_TELEMETRY=0` and `CODEGRAPH_NO_UPDATE_CHECK=1`; the `add-json` JSON carries both in `env`.
- Provenance tag: "Variant 1 (Option A), bullet 4 JSON — merged per Changes 3 and 4"
- Validation: JSON is the exact string from the brief with only the `command` placeholder.

### Change 5: no prompt hook, never run upstream installers
- Status: applied
- Before: base was silent.
- After: new "Explicitly not done" list: no `codegraph install`, no `install.sh`, no `UserPromptSubmit` hook.
- Provenance tag: "Variant 1 (Option A), bullets 5-6, plus Variant 2 advocate weakness #1 — merged per Changes 5, 11, 12"
- Validation: cites eval §5.9 in the Decision section (reason 2).

### Change 6: guidance and permission owned by IronClaude
- Status: applied
- Before: "relies on `src/superclaude/core/CLAUDE.md` for guidance".
- After: step (b)6, guidance in `src/superclaude/core/CLAUDE.md` plus `mcp__codegraph__*` through IronClaude settings handling.
- Provenance tag: "Base (original, modified) plus Variant 1 (Option A), bullet 5 — merged per Change 6"
- Validation: `install_core.py:62-71` cited in the Decision section.

### Change 7: receipt and removal for the user copy only
- Status: applied
- Before: base was silent on removal.
- After: step (b)7, reuses the `install_codebase_memory.py` pattern, covers only `~/.codegraph` and `~/.local/bin/codegraph`.
- Provenance tag: "Variant 1 (Option A), bullet 6 — merged per Change 7"
- Validation: consistent with "No writes to `/usr/local/bin` or `/opt/codegraph`" in "Explicitly not done".

### Change 8: running daemons when the user copy is swapped
- Status: applied
- Before: base was silent.
- After: step (b)4, new `versions/<tag>/` dir, symlink flip, previous dir kept until next run, never delete in the same run, warn about the 300 s idle timeout (eval §5.7).
- Provenance tag: "debate A-004 plus Variant 2 advocate (install.sh prune hazard) — merged per Change 8"
- Validation: carried as an untested condition under A-004 in "Conditions and risks".

### Change 9: Claude CLI readiness guard
- Status: applied
- Before: base was silent.
- After: step (b)1, reuse the readiness check that `install_codebase_memory.py:614` leaves to its caller.
- Provenance tag: "debate A-002 — merged per Change 9"
- Validation: the plan says "before registration"; the brief orders it first in the phase. First satisfies both. Note: the docstring sentence "The caller must check Claude CLI readiness" is at line 613 of `install_codebase_memory.py`; line 614 (as cited by the debate and plan) is the next docstring line, so the reference resolves to the right docstring but is off by one.

### Change 10: drift check against upstream config shape, test-time only
- Status: applied
- Before: base was silent.
- After: (d) "Drift test, test-time only": recorded `--print-config claude` fixture refreshed per pin bump, unit test ignores IronClaude's `env`, never runs during install.
- Provenance tag: "Base (original, modified) — ... merged per Changes 2 and 10"
- Validation: does not conflict with "No `codegraph install`" because `--print-config` writes nothing (eval §5.9) and runs only when refreshing a test fixture; the "Explicitly not done" bullet is scoped to "at runtime".

### Change 11: `codegraph upgrade` unsupported and detected
- Status: applied
- Before: base Weakness "`codegraph upgrade` cannot update a root-owned install from a user shell".
- After: "Explicitly not done" bullet (unsupported, documented, detected) and (c) doctor checks for version drift, a `CODEGRAPH_START` block, and a `codegraph prompt-hook` entry.
- Provenance tag: "Base (original, modified) — update path; merged per Changes 2 and 11"
- Validation: `./update.sh` runs `superclaude install --force` (line 8) then `superclaude doctor` (line 10), verified by reading `update.sh`. The base weakness was removed as superseded.

### Change 12: conditions and out of scope
- Status: applied
- Before: base was silent.
- After: "Conditions and risks attached by the debate": A-001 owner as a separate decision, A-004 untested, 4 hashes per release at about 8 per quarter, single maintainer, about 286 MB image growth, GitHub availability, re-registration on winner change; `gh attestation verify` optional in "Explicitly not done".
- Provenance tag: "debate A-001, A-004, A-005 and advocate concessions — merged per Change 12"
- Validation: every item maps to the plan's Change 12 list or the brief's list.

## Post-Merge Validation

### 1. Structural integrity: PASS
- Heading sequence: H1, then H2 Decision, H2 What it does with H3 (a)-(d), then H2 Explicitly not done, Strengths, Weaknesses, Conditions and risks, Rejected alternatives, Debate summary.
- No level gaps (no H1 to H3 jumps). No orphaned subsections: all four H3s sit under "What it does".
- Every section and significant block has a preceding `<!-- Source: ... -->` comment; the three header provenance comments are present.
- Length: about 1,200 words of visible prose, about 1,560 including the required provenance comments. Within the "about 1,400 words" limit if comments are excluded; slightly over if they are counted.

### 2. Internal references: PASS (50 total, 50 resolved, 0 broken)
- Debate IDs: 28 occurrences of 18 distinct IDs (A-001..A-005, C-001, C-002, C-003, C-004, C-005, C-007, C-008, C-009, C-010, C-012, X-001, X-002, U-001). All 18 resolve in `debate-transcript.md` or `diff-analysis.md` (U-001 at `diff-analysis.md:52`).
- Eval section refs: 15 (§1, §2, §4, §5.1, §5.1-5.2, §5.2, §5.7, §5.9). All exist in `codegraph-evaluation.md`; each supports its claim (no checksum §1/§5.2, 63 MB §5.1, 286 MB §5.2, 300 s idle §5.7, 41-symbol payload and `--print-config` §5.9, worktree `init` §4, about 8 releases §1).
- File:line refs: 7 (`main.py:254-262`, `update.sh:8,10`, `install_core.py:62-71` x2, `install.sh:71-82` x2, `install_codebase_memory.py:614`). `main.py:254-262` and `update.sh:8,10` were re-read this run and match. `install_core.py:62-71` matches the copy loop. `install.sh:71-82` refers to upstream `docs/install.sh` as cited by eval §1. `install_codebase_memory.py:614` resolves with the off-by-one noted under Change 9.

### 3. Contradiction re-scan: PASS (0 new contradictions)
- **Gate vs fallback vs registration order.** (b) is numbered: readiness guard, gate, fallback only if no candidate passes, daemon handling, registration of the winner. The Decision sentence, (c) pin-bump flow and Conditions all describe the same order. Registration always follows either the gate or the fallback, and the fallback's binary becomes the winner. No clash.
- **Root-owned preference vs single-pin rule.** No conflict: the root-owned copy is preferred only when its version equals the single IronClaude pin; a mismatching baked copy never wins. The trade-off (a stale image makes the user-writable copy the registered binary) is stated as a Weakness and the fallback warns on Coder. The rejected-alternatives row for C-007 says "whenever its version matches", consistent with this.
- **Upstream layout vs "no `codegraph upgrade`".** Option A claimed the layout keeps `codegraph upgrade` working (base-selection's IC finding against A). The merge keeps the layout but does not repeat that claim, and states `upgrade` is unsupported and detected. Contradiction not carried over.
- **Drift test vs "no `codegraph install`".** Resolved by scoping: `--print-config` writes nothing and runs only at fixture-refresh time; the "not done" bullet says "at runtime".
- **Removal scope vs baked copy.** Removal covers only the user copy; IronClaude never writes `/usr/local/bin` or `/opt/codegraph`. Consistent.
- **Base Strengths after merge.** "Root-owned binary" was narrowed to "On Coder the registered binary is root-owned" so it does not contradict the stale-image weakness. "Works offline" was narrowed to "up-to-date Coder workspaces".

## Summary
| Planned | Applied | Failed | Skipped |
|---|---|---|---|
| 12 | 12 | 0 | 0 |

Issues for the orchestrator: none blocking. Two notes: the `install_codebase_memory.py:614` citation is off by one (the sentence is at 613), kept as cited by the plan; and the merged file is about 1,200 words of prose but about 1,560 with provenance comments.
