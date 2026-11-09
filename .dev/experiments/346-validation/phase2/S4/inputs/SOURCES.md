# inputs/SOURCES.md: where each input came from

Verify the files: `cd inputs && sha256sum -c MANIFEST.sha256`.

Path keys: `TD` = `/home/coder/workspaces/worktrees/Coder/bmad-ponytail-global/.dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901` (original task folder, final state); `FH` = `/home/coder/.claude/file-history/189f8649-3921-4435-bc6b-a15182a20399`; `BM` = main session log `/home/coder/.claude/projects/-home-coder-workspaces-worktrees-Coder-bmad-ponytail-global/189f8649-3921-4435-bc6b-a15182a20399.jsonl`; `SA` = its `subagents/` folder. All sources were copied read-only; nothing under `~/.claude` or in the Coder worktree was changed.

"EXACT" = byte-identical to the file as it stood at that time (proved by a stored copy). "REPLAY" = rebuilt by `tools/reconstruct.py` from the logged Write/Edit/heredoc calls; "confirmed" says what stored object it equals.

| File in `inputs/` | Origin | Status |
|---|---|---|
| `task-file/TASK-RESEARCH-bmad-first-use-20261107-075901.md.v2-at-2026-11-07T15-38-37Z` | `FH/32d05845d5285d52@v2` (backup taken 15:38:37Z; includes the pre-start Gate 4 sentence fix, its log entry is on line 535) | EXACT. This is the task file the executor read |
| `task-file/...md.v1-before-this-session` | `FH/32d05845d5285d52@v1` (13:25Z, before the Gate 4 sentence fix and the status change) | EXACT, for reference only |
| `task-file/BUILD-REQUEST.md` | `TD/BUILD-REQUEST.md` (mtime 08:04Z on 2026-11-07, before the run; no edits in the logs) | EXACT |
| `skills/tech-research_skill-text_as-loaded_L142.md` | `BM` L142 (the text the `tech-research` skill expanded to, 121,689 bytes) | EXACT |
| `skills/task_skill-text_as-loaded_L158.md` | `BM` L158 (the `task` skill text, 63,508 bytes) | EXACT |
| `common/research/01..05, web-01, web-02, research-notes.md`, `common/gaps-and-questions.md` | `TD/research/*`, `TD/gaps-and-questions.md` (final files; no edit after 18:11:58Z, so these are also the Gate 2 and Gate 3 starting states) | EXACT: each hashes to a git object in the Coder repo and to the replay of its logged edits |
| `gate1-start/research/01..05` | REPLAY of all logged calls up to 15:52:20Z (start of the Gate 1 reviewers, `BM` L676) | REPLAY, no stored copy; the chain end equals the file on disk |
| `gate1-start/research/research-notes.md` | final file on disk with the 10 edits of one Gate 1 fix agent (`SA/agent-a06234f4b582724ab.jsonl`, 16:07 to 16:11Z) reversed (`tools/reverse_notes.py`) | confirmed: a git object with this hash exists in the Coder repo |
| `gate2-start/synthesis/synth-01..04` | REPLAY up to 18:11:58Z (`BM` L1899) | REPLAY, no stored copy; chain end equals the file on disk |
| `gate3-start/synthesis/synth-01..04` | REPLAY up to 19:00:30Z; equals `TD/synthesis/*` (no edit after 18:57Z) | EXACT, each hashes to a git object in the Coder repo |
| `gate3-start/RESEARCH-REPORT-bmad-first-use.md` | REPLAY: stub Write (`SA/agent-a9c6678fe08ab2dda.jsonl` L44) + the assembler's five `sed -n ... >> report` / heredoc commands (L64, 77, 90, 116, 124) re-run on `gate3-start/synthesis` + its edits to 19:00:30Z (1,785 lines, `BM` L2844) | REPLAY; the same chain continued to 19:56Z equals `FH/ca7857aee503d1e6@v1` byte for byte |
| `gate4-start/RESEARCH-REPORT-bmad-first-use.md` | same replay up to 20:15:23Z (after the Gate 3 exception edits) | REPLAY |
| `gate5-start/RESEARCH-REPORT-bmad-first-use.md` | same replay up to 20:37:58Z | REPLAY |
| `repo-untracked/.dev/issues/478/*` (12 files) | `/home/coder/workspaces/worktrees/Coder/bmad-ponytail-global/.dev/issues/478/` (mtime 07:21 to 07:27Z, before the run); files created later (`spec.md`, `spec-stage1.md`) were not copied | EXACT as of now; UNVERIFIED that unchanged since the run |
| `repo-untracked/.dev/troubleshoot/untyped-bmad-and-ponytail-are-only-20261107072723/` | the same worktree (mtime 07:34 to 07:55Z) | EXACT as of now; UNVERIFIED that unchanged since the run |

Not in `inputs/` because they are not files: the Coder repo at commit `f1ac0c93ad5a64b03f0ed49866d3adfe140c28b1` (`BM` L23, L868), the installed skills and agents dated 2026-11-05 13:13 (`~/.claude/skills/{tech-research,task}`, `~/.claude/agents/rf-*.md`), `/opt/uv/tools/superclaude`, `/opt/nvm/.../bmad-method` and `~/.claude` as read by the research agents.

Results of the original run (not inputs) are in `../evidence/baseline-qa-outputs/` and must not be shown to a replay session.
