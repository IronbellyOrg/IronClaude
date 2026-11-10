# Sources for inputs/ (S1 / incident I1)

Every file below was copied (never moved) out of `~/.claude/file-history`, git objects or the tracked tree; nothing under `~/.claude` was edited. `MANIFEST.sha256` lists the sha256 of every file in this folder, including this one (check from inside `inputs/`: `sha256sum -c MANIFEST.sha256`).

`FH` = `/home/coder/.claude/file-history`. `PJ` = `/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-OrcaCLICommandRefactor-Specs`. `WT` = this worktree's tracked tree (`.dev/orca-command-refactor/`, committed by f3c1ef06/#368 and ce642492/969c7709 on the branch).

## Starting document and shared inputs (`repo-overlay/`, drop into the replay worktree root)

| File in `inputs/` | Original path / log line | Identity check |
|---|---|---|
| `repo-overlay/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (57,763 B, 285 lines) | **Starting document v1.** `FH/3bb70411-6b34-4a6c-b0de-81ffdbae7944/2d815cfd5e9a74d2@v1`, the pre-edit backup Claude Code made when Task 6 (revise 1) first edited the spec; the same file is named in `PJ/aff19d65-a1f0-4494-8e6a-9ece95738d29.jsonl` L140 as the pre-revision backup. Written originally by Task 4 (`PJ/1b14f80b...jsonl` L95-629, Write + 26 Edits, worker_done L652) | `cmp` equal to `WT/specs/history/spec-v1-draft.md`; sha256 equal; size equals the 57,763 bytes the R1 review cites |
| `repo-overlay/.dev/orca-command-refactor/README.md` (2,755 B) | `WT/README.md`; existed before all sessions (`PJ/9f0fb721...jsonl` L36); no Write/Edit in any session of `PJ` touched it | sha256 equal to the bytes Task 4 `Read` (`PJ/1b14f80b...jsonl` L54 call, L56 result) |
| `repo-overlay/.dev/orca-command-refactor/inventory/commands-a.md` (34,322 B) | `WT/inventory/commands-a.md`; created by Task 1 (`PJ/9f0fb721...jsonl` L56 Write plus Edits to 03:36Z); no edit after 03:43Z in any session | sha256 equal to the bytes Task 4 read (`PJ/1b14f80b...jsonl` L70 call, L72 result) |
| `repo-overlay/.dev/orca-command-refactor/inventory/commands-b.md` (53,889 B) | `WT/inventory/commands-b.md`; Task 2 (`PJ/a1c4ed4e...jsonl` L65 Write plus Edits to 03:42Z) | sha256 equal to the bytes Task 4 read (L81 call, L83 result) |
| `repo-overlay/.dev/orca-command-refactor/inventory/orca-capabilities.md` (44,524 B) | `WT/inventory/orca-capabilities.md`; Task 3 (`PJ/f7191a1f...jsonl` L69 Write plus Edits) | sha256 equal to the bytes Task 4 read (L58 call, L60 result) |

## Reference snapshots of the document after each baseline revision (for M4 and diffs; not inputs to the loop)

| File | Original path | Size |
|---|---|---|
| `reference-snapshots/spec-v2-after-round1.md` | `FH/66468bab-54d0-4268-a016-46cd22c264ab/2d815cfd5e9a74d2@v1` (pre-edit backup of Task 8) = state the R2 reviewer saw | 82,643 B, 402 lines |
| `reference-snapshots/spec-v3-after-round2.md` | `FH/458bdc00-e815-4098-a449-4dfaef7826fd/2d815cfd5e9a74d2@v1` (Task 10) = state the R3 reviewer saw | 92,194 B, 414 lines |
| `reference-snapshots/spec-v4-after-round3.md` | `FH/eadb62ac-2f33-4997-9dc3-0925e98f9aa5/2d815cfd5e9a74d2@v1` (Task 12) = after Task 10 | 89,089 B, 405 lines |

All three are `cmp`-equal to `WT/specs/history/spec-v2-after-round1.md`, `spec-v3-after-round2.md`, `spec-v4-after-round3.md`.

## Tool text (the command under test)

| File | Original | Notes |
|---|---|---|
| `tool-text/spec-panel-pre427-ec1babd9.md` (32,717 B, 462 lines) | `git show ec1babd9:src/superclaude/commands/spec-panel.md` | Byte-identical to `git show 2cb683f5:src/superclaude/commands/spec-panel.md` (the original repo base) and to the installed `~/.claude/commands/sc/spec-panel.md` on this machine (read-only `cmp`). This is the text R2/R3 read (`1-462`, `BO/spec-panel-round2.md:16`, `-round3.md:17`) and, minus the front matter plus a trailing `ARGUMENTS:` line, the text R1's Skill call loaded (`PJ/699ae853...jsonl` L58) |
| `tool-text/spec-panel-post427-95f2c6e4.md` (35,853 B, 472 lines) | `git show 95f2c6e4:src/superclaude/commands/spec-panel.md` | The text PR 427 installs |
| `tool-text/spec-panel-427.diff` | `git diff ec1babd9 95f2c6e4 -- src/superclaude/commands/spec-panel.md` | Applies cleanly to the `2cb683f5` file and reproduces the `95f2c6e4` file byte for byte (checked with `patch --dry-run` and `cmp`). Use it for the pinned-evidence arm |

## Inputs that are NOT copied here, and how to get them

| Needed | Where | Note |
|---|---|---|
| Repo state the reviewers checked citations against | git commit `2cb683f5c1f0dfbd3c5f169a8b64a432931f718e` (original base for rounds 1-3; branch created from it 2026-10-30, fast-forwarded to `c118b5a5` at 2026-11-02T15:25:37Z) | Reflog: `git reflog show --date=iso ironbelly/OrcaCLICommandRefactor-Specs`. The original working tree had only `.dev/` untracked content (R3's `git status` listing, `BO/spec-panel-round3.md:21`) |
| README's evidence files (`.dev/codegraph-migration/orchestration/README.md`, `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md`, `.dev/research/recovered-command-evaluation-20261027/`) | git, identical blobs at `2cb683f5` and `95f2c6e4` for the first two | |
| Orca CLI `1.4.237-aidev02.0e4491a95e92` help output | live tool; cannot be frozen | The inventory `orca-capabilities.md` quotes the parts the spec cites |
| Original reports and dispositions (for comparing a re-run) | `../baseline-outputs/` (copies of `.dev/orca-command-refactor/review/*`; checksums in `../baseline-outputs/SHA256SUMS`) | Outputs of the original run, deliberately outside `inputs/`: never give them to replay workers |
