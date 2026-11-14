# Round 1 advocate statement: Variant 2 (Coder template update)

Advocate persona: architect (structure, dependencies, long-term impact). Facts re-checked read-only on 2026-11-14.

## Position summary

Variant 2 is the only route that keeps one delivery path and one reviewed, pinned provenance for the CLI on every workspace, which is the architecture the owner stated on 2026-11-12. As written it is incomplete: on this host it changes nothing the coordinator runs until the shadowing user-level install is removed, so the right answer is Variant 2 plus one owner-approved removal of that install, timed after the workspace update, with `workflow_dispatch` used to cut the monitor's wait.

## Steelman of Variant 1

Variant 1 is the only proposal that makes SWEEP-RUNNABLE true within minutes of SW-05 with certainty on this host as it stands. The user-level install already wins on `PATH` (verified: `which -a superclaude` lists `/home/coder/.local/bin/superclaude` first; the running Claude process 9543 has `~/.local/bin` before `/usr/local/bin`), so replacing it is the one action that changes what the coordinator runs. The in-place rule is already breached on this host by an unknown actor (receipt at `~/.local/share/uv/tools/superclaude/uv-receipt.toml`, rev `d2d8a2d1...`, links dated Nov 12 22:12), so replacing one user-level install with another adds no new kind of drift. It pins the merge commit, never a branch (variant-1 line 23, diff-analysis U-001), and it records the divergence in the ledger (variant-1 line 11). XC-04 records "the executable revision" (`merged-requirements.md:452`), so a single-host revision is fully auditable. The owner has also shown dislike for "wait for Coder" gates: the memory's How to apply says an IronClaude PR that does not touch `ccsession-models.json` "needs no 'wait for Coder' merge gate".

## Steelman of Variant 3

Variant 3 takes no host action and grants no exception, so it cannot break anything, and it matches the spec's own default (`question.md` line 15). Q29 is a W3 item asked "when the item is next" (`question.md` line 22), so deciding before the merge risks deciding on stale facts: the Coder pin, the host's installs and even the coordinator's environment may all change by then. The daily monitor (`ironclaude-upstream-monitor.yml` lines 9-12, cron `0 6 * * *`) may deliver the sweep with no decision at all (U-003), and the coordinator still has Orca read verbs for status meanwhile (variant-3 line 10).

## Key strengths claimed

1. One delivery path. The owner memory says "nobody updates IronClaude in place; updates reach workspaces only through the Coder template and workspace updates" (`ironclaude-updates-only-via-coder.md`, body line 1). Variant 2 is the only option that delivers the sweep through that path (variant-2 lines 5, 16-17).
2. Reviewed provenance. The template route carries an install proof and a recommended contract build before merge: the monitor PR body prints the `uv tool install ... @${UPSTREAM_SHA}` proof result and tells reviewers to require `coder-ci-aidev02-contract.yml` (`ironclaude-upstream-monitor.yml`, around lines 330-336). A hand reinstall skips both.
3. Fleet consistency. Every workspace runs the same pinned CLI (variant-2 line 16), so the XC-04 join result measures the CLI other coordinators will actually run, not a one-host build.
4. The wait is shorter than it looks. The workflow declares `workflow_dispatch` (line 12), so the owner can open the bump PR right after SW-05 (variant-2 line 9, U-002).
5. Honest about its own gap. Variant 2 is the only proposal that states, in its own risk section, that the template alone fails on this host while the user-level install shadows it (variant-2 line 23). That is the correct dependency analysis, and it points to the fix.

## Weaknesses identified in Variant 1

1. It needs an explicit exception to the owner's stated rule (variant-1 line 21; X-001). An exception granted for convenience sets a precedent the rule was written to prevent.
2. It entrenches the shadow. After a `--force` reinstall, the user-level copy keeps hiding every future template update, and Variant 1 leaves "when to remove the user-level install" unresolved (variant-1 line 27). `/home/coder` is a separate block device (`/dev/sdb`) while `/` is an overlay (`df`, 2026-11-14), so the shadow very likely survives image rebuilds (persistence across a rebuild itself is UNVERIFIED). The long-term cost is that this host silently stops following the fleet.
3. It skips the monitor's install proof and the contract build (strength 2 above).
4. It depends entirely on A-001 (the coordinator resolving `~/.local/bin` first). If the coordinator runs inside an IronClaude checkout with its `.venv/bin` first on `PATH`, the reinstall changes nothing (see A-001 below).

## Weaknesses identified in Variant 3

1. On this host the gate will most likely never pass on its own: the template update changes `/usr/local/bin/superclaude`, which `~/.local/bin/superclaude` shadows (variant-3 line 22). "Re-check after the pin bump" (variant-3 line 11) therefore re-asks the same question later with the same options (variant-3 line 23).
2. It leaves WC-16 indefinitely not runnable and XC-04 and everything after it held (variant-3 line 21), with no mechanism that ends the hold.
3. It resolves nothing Q29 asks (variant-3 line 27). Deferring is only safe if something will change, and the shadow analysis says nothing will.

## Concessions

1. Variant 2 as written does not reach SWEEP-RUNNABLE on this host (X-002). The removal of the user-level install is a required step, not an open question, and Variant 2 lists it only under "unresolved" (variant-2 line 27).
2. It is slower: a bump PR, its review, an image build, a template push and a workspace update (variant-2 line 21), even with `workflow_dispatch`.
3. A workspace update may restart the workspace and end the coordinator and Orca sessions (variant-2 line 22); this is UNVERIFIED and is a real operational risk Variant 1 does not carry.
4. Removing the user-level install drops this host from `d2d8a2d16` (2026-11-12) back to the image's `4ab620d1` (2026-11-11) if done before the workspace update. Ordering matters (see A-002).

## Shared assumption responses

| ID | Response | Reason |
|----|----------|--------|
| A-001 | QUALIFY | Verified for the sampled sessions: `which -a superclaude` and the `PATH` of Claude process 9543 put `~/.local/bin` before `/usr/local/bin`. But processes started inside an IronClaude worktree with its venv active (python 1204205/1204206 under `eval-tasklist-review-panel`) have `<worktree>/.venv/bin` first, and this worktree has `.venv/bin/superclaude` (Nov 12 22:09). A coordinator in such an environment would run the checkout's CLI, and none of the three variants would change it; whether that venv install is editable, and whether the coordinator runs with it, is UNVERIFIED. SWEEP-RUNNABLE is rightly defined "in the coordinator's own environment" (`merged-requirements.md:601`); every variant should check `which -a superclaude` there, not in a worker shell. |
| A-002 | QUALIFY | The image install provides the same two entry points, `ic` and `superclaude` (verified `/opt/uv/tools/superclaude/uv-receipt.toml`; `/usr/local/bin/ic` exists), so removal leaves both commands resolvable. But it falls back one revision (`d2d8a2d16` to `4ab620d1`); whether anything here depends on the difference is UNVERIFIED. For Variant 2 the removal should run after the workspace update lands the new pin, so it is a move forward, not a regression. |
| A-003 | ACCEPT | Stated in `merged-requirements.md:1154`: neither `superclaude install` nor `make sync-dev` upgrades the CLI. |
| A-004 | ACCEPT | `sc-sweep-protocol/SKILL.md:24` falls back to `uv run` "only when step 1 fails with 'command not found'"; the observed output is Click's "No such command 'sweep'", which is not the shell's message. |

## Per-point verdicts

| Point | Superior variant | One-line reason |
|-------|------------------|-----------------|
| S-001 | Tie | All three have the same five sections and four steps; structure decides nothing. |
| C-001 | V2 | The only route through the owner's stated delivery path, provided it adds the one removal step. |
| C-002 | V1 | Minutes versus a PR, build and update; `workflow_dispatch` narrows but does not close the gap. |
| C-003 | V2 | Every workspace gets the same reviewed pin; V1 creates host drift and V3 delivers nothing. |
| C-004 | V1 | A user-level reinstall ends no sessions; V2 carries an unverified restart risk. |
| X-001 | V2 | Follows the owner rule and actually delivers; V3 follows it only by not acting. |
| X-002 | V1 | As written, only V1 changes what the coordinator runs on this host; V2 names the gap but leaves its fix unresolved. |
| X-003 | V2 | Install proof plus contract build plus pinned image beats a hand-picked commit on one host. |
| A-001 | V2 | Once the shadow is removed only one global install remains, so V2 stops depending on `PATH` order between two installs (the venv case still applies to all). |
| A-002 | V1 | Replacing keeps a newer revision in place with no fallback window; V2 must order the removal after the update to avoid a regression. |

## Overall pick

Variant 2, amended: trigger the Coder monitor with `workflow_dispatch` after SW-05, update the workspace, then make one owner-approved removal of the shadowing `~/.local` install and confirm SWEEP-RUNNABLE with `which -a superclaude` and `superclaude sweep --help` in the coordinator's own environment.
