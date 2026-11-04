# Execution locus
PRINT-SITE: hook exit status of src/superclaude/hooks/scripts/block-bare-python.sh, read by Claude Code (PR #359 review comments 4469161162, 4469111833, 4469111829)
RUN-SITE: src/superclaude/hooks/scripts/block-bare-python.sh:275 (exit 0 when the scanner prints no word) and :279 (exit 2) @ local bash + awk (mawk/gawk via LC_ALL=C awk), this worktree
SAME-ENV: yes
OBSERVE-VIA: same-shell
re-run permitted: yes (read-only probe of the hook, already run this session by the pr-submit verify wave)
