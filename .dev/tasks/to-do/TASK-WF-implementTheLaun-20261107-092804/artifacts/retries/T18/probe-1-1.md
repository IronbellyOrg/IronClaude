2972aa6ec7b94a4518c3976bb881929401428f0b
family matcher-coverage
defect form: a probe list or check that is shorter than the set the design says the registration must fire for
command: grep -nE 'GOVERNED_TOOLS|process_interface_gaps|LINUX_FILES' src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py
before-output:
GOVERNED_TOOLS held the 13 plain tool names; LINUX_FILES held two /proc paths; the mcp__ branch and the pidfd and subreaper interfaces were not probed
coupled sites: SKILL.md and refs/claim.md describe the preflight in words (no list of names); test_ir4_non_linux_host_is_refused asserted the old reason text (updated)
after:
724:GOVERNED_TOOLS = (
745:LINUX_FILES = ("/proc/self/stat", "/proc/sys/kernel/random/boot_id")
749:def process_interface_gaps() -> list[str]:
