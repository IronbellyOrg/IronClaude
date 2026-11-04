# Wave 1.5 Branch B (round 3), returned by troubleshoot-analyst, persisted on receipt; currency finalized by parent
| doc_path | verdict | summary |
|---|---|---|
| src/superclaude/hooks/scripts/block-bare-python.sh (header 1-62) | current (parent: the code file itself, edited this session) | line 27 claims redirections are tracked; line 29 covers the `function` keyword only; ceilings 45-58 list neither defect; the generic false-positive note (59-60) uses a heredoc example |
| CHANGELOG.md (#357 entry 7-16) | current (parent: written this session) | names only process-substitution redirect targets; nothing on function definitions or {fd}; no false positive recorded |
| CLAUDE.md | unknown | UV-only rule only |
| KNOWLEDGE.md | unknown | nothing on the hook |
| docs/ | unknown | nothing on the hook |
degraded: false. Defect 1 = unlisted false positive; defect 2 = unlisted miss.
