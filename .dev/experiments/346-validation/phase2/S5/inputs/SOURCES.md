# S5 inputs: where every file came from

Incident I5 = the four final reviews of package `TASK-WF-writeTheP0LivePl-20261103-215902` (4 Nov 2026, executor session `aaee1ebf-4ec9-494f-85e0-52f3697170b5`, repo checkout `/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs`, branch `ironbelly/OrcaCLICommandRefactor-Specs`, HEAD `8db29f11`).

`AA` = `/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-OrcaCLICommandRefactor-Specs/aaee1ebf-4ec9-494f-85e0-52f3697170b5.jsonl`.
`FH` = `/home/coder/.claude/file-history/aaee1ebf-4ec9-494f-85e0-52f3697170b5/` (read only; nothing there was changed).
Everything below was copied out; nothing here points back into `~/.claude`. The original checkout and `/tmp/ironclaude-p0live/` no longer exist.

## The starting document: `package-R1/TASK-WF-writeTheP0LivePl-20261103-215902/` (121 files)

The document under review is the whole task package (plan, source, ledger, 100+ evidence files), as it stood when review 1 was spawned (`AA` L2001, 2026-11-04T09:09:08.436Z).

| How it was built | Evidence it is right |
|---|---|
| Took the archived final package from git commit `b5c09e90` (identical to `f3c1ef06`, the squash merge #368), path `.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/` (121 files, 772,021 bytes). | `git archive b5c09e90 .dev/tasks/done/<id>`; the two commits give identical trees (`diff -r` clean). |
| Reversed the ten logged `Edit` calls that changed the package after review 1 (`AA` L2099, L2103, L2107, L2111, L2242, L2246, L2261, L2302, L2316, L2464) with `derivation-scripts/recon.py`: each `new_string` is swapped back to its `old_string`, newest first. Six files are touched: `artifacts/lc1-step5.md`, `lc2-result.md`, `lc2-step5.md`, `lc3-session-analysis.txt`, `lc3-step5.md`, `p0-phase-report.md`. | For all six files, the rebuilt content at the start of each review is byte-identical to a Claude Code file-history backup (table below). The fix text itself is the logged tool input, so the edits are verbatim. |
| Cut the ledger `progress.md` to its first 12 lines (the ledger had 12 lines before the first `FINAL:` line was appended at `AA` L2038). | The 13-, 14- and 16-line prefixes of the final ledger are byte-identical to `FH/2217edb430755e4e@v2`, `@v3`, `@v4` (7,219 / 7,430 / 8,156 bytes). The 12-line prefix is 7,040 bytes. |
| Everything else (115 files) is taken as it is in the final package. | No logged `Edit`, `Write` or Bash redirect changed any other package file between `AA` L2001 and L2559 (checked by scanning every mutating call in that range; only ledger appends and the ten edits exist). |

File-history match table (rebuilt state of the file at the start of the review equals this backup):

| File | R1 start | R2 start | R3 start | R4 start |
|---|---|---|---|---|
| `artifacts/lc1-step5.md` | `e6e0c5385eeb92e7@v2` | `@v3` | `@v3` | `@v3` |
| `artifacts/lc2-result.md` | `29b2f6ff40ae72c5@v2` | `@v3` | `@v3` | `@v3` |
| `artifacts/lc2-step5.md` | `f5dd5b308dc0a5b9@v2` | `@v3` | `@v3` | `@v3` |
| `artifacts/lc3-session-analysis.txt` | `599c62d748129d9e@v1` | `@v1` | `@v2` | `@v2` |
| `artifacts/lc3-step5.md` | `d31fc1104e11402f@v2` | `@v2` | `@v3` | `@v3` |
| `artifacts/p0-phase-report.md` | `38feb002f84e3014@v2` | `@v2` | `@v3` | none (no later turn; follows from the verified edit L2464) |

Known limit: the package digest the helper printed in the original `FINAL:` lines (`3ea431e2...` for round 1) cannot be reproduced. The digest includes each delivery file's permission bits, git stores only 644 or 755, and the original files had mixed bits (several were written under `umask 077`). The helper accepts the rebuilt package (`--print-state` prints status `state` and 57 delivery files, with both the 80f934de and the 95f2c6e4 versions of `archive_workspace.py`); a replay writes its own digests.

## Fix cycles and owner rulings: `round-deltas/`

| File | Source |
|---|---|
| `edits.json` | The ten `Edit` inputs, verbatim, in log order: `path`, `old_string`, `new_string`, log line. Cycle 1 = L2099 to L2111; cycle 2 = L2242 to L2316; cycle 3 = L2464. |
| `ledger-ruling-1.txt` | The `ARCHIVE: Ruling:` line appended at `AA` L2280 (line 15 of the final ledger). |
| `ledger-ruling-2.txt` | The `ARCHIVE: Ruling:` line appended at `AA` L2478 (line 17 of the final ledger); it replaces ruling 1. |

## Expected states: `expected-states/*.sha256`

`sha256sum` of every package file except `progress.md` at the start of each review (`R1-start` to `R4-start`) and after review 4 (`FINAL-after-R4`). Use them to check that `tools/apply_round.py` reproduced the original document state. `progress.md` is left out because a replay writes its own `FINAL:` lines.

## Protocol text the executor loaded: `evidence/protocol-as-loaded/`

`qa.md`, `ledger.md`, `managed-workspace.md` as read by the executor at `AA` L100, L96, L72 (line-number prefixes removed). They are byte-identical to `src/superclaude/skills/sc-implement-protocol/refs/<name>.md` at commit `80f934de`. The installed `qa.md` and `managed-workspace.md` on this machine are the same bytes; `ledger.md` and `retry.md` have since changed. The severity test and cap wording the reviewers applied come from this `qa.md` (sections "Severity model", "FINAL derived test", "Managed FINAL review").

## Repo files the reviewers read: `evidence/repo-snapshot-8db29f11/`

Copied with `git show 8db29f11:<path>` (the commit the original checkout was at). The reviewers read them as reference, and all four saw the OLD step-5 wording of the spec (checked: the old sentence appears in each reviewer log, the new one in none). Master at 95f2c6e4 has newer versions of five of them, so a replay must overlay this snapshot (REPLAY.md, setup step 4).

| File | Same on master 95f2c6e4? |
|---|---|
| `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` | NO (PR #368 rewrote 7.2 step 5) |
| `src/superclaude/core/WORKER-CONTRACT.md` | NO (later P1/P2 edits; WC-10 and WC-13 text unchanged) |
| `src/superclaude/commands/workflow.md`, `src/superclaude/commands/adversarial.md`, `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md` | NO |
| `src/superclaude/commands/troubleshoot.md`, `src/superclaude/skills/sc-adversarial-protocol/refs/artifact-templates.md`, `src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md`, `.dev/orca-command-refactor/decisions/D1/option-a.md`, `option-b.md`, `.dev/tasks/done/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/p0-static-report.md`, `.../t1-accepted-failures.md` | yes |

## Evidence the reviewers audited (tar.gz, unpack with `tar -xzf`)

| File | Source | Notes |
|---|---|---|
| `evidence/worker-sessions.tar.gz` | `~/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-p0-live-{troubleshoot,workflow,adversarial}/` (68, 70 and 25 files) | The three live-check worker sessions. Their last timestamps (06:51:58Z, 08:25:48Z, 09:03:41Z) precede the first review spawn (09:09:08Z), so the copies are complete as the reviewers saw them. |
| `evidence/executor-session-asof-R1.tar.gz` to `R4.tar.gz` | `AA` and its `subagents/` folder, cut by `tools/asof_cutoff.py` at the spawn time of each review: R1 2026-11-04T09:09:08.436Z (main log 2,001 lines), R2 12:11:17.569Z (2,157), R3 12:29:53.890Z (2,342), R4 12:56:21.546Z (2,499). | Reviews 2 to 4 audited the executor session tree, which by then contained the earlier reviewers' own tool calls (that is where round 3's finding came from). Each cut holds the earlier reviewers' logs and nothing later. Not copied: `tool-results/` (20 saved tool outputs) and `custom-title.json`. |

## Tools: `tools/`

`apply_round.py` (apply fix cycle k), `asof_cutoff.py` (how the executor cuts were made), `render_briefs.py` (swap machine paths in the verbatim briefs). Each was exercised once on a scratch copy: `apply_round.py` reproduced the `R2-start`, `R3-start` and `R4-start` hashes exactly; `render_briefs.py` left no original path in any brief. For the archive helper use `src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py` from the replay checkout (not shipped here).

## Checks on this folder

- Secret scan (API keys, tokens, private keys, bearer strings, `*_KEY=`/`SECRET=`/`PASSWORD=` assignments) over this folder, `briefs/`, `baseline-reference/` and the unpacked evidence: the only hits are task-name slugs that contain the letters `sk-` (for example `...-task-sk-rf-20260608-...`), no credentials.
- The session logs contain Orca terminal handles (`term_...`) and the user's home path. These are identifiers, not secrets; they stay because the reviewers' audit depends on those logs.
