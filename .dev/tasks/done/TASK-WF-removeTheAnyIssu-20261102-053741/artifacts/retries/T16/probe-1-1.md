768902a72df6987ea226fa70bafdc22e8422ac21
family max-convergence-help-truth
defect form: --max-convergence help text claims where the value is used; nothing reads config.max_convergence.
command: git grep -n -F -e "max-convergence" -- src/superclaude/cli/cli_portify/commands.py
before:
src/superclaude/cli/cli_portify/commands.py:98:    "--max-convergence",
coupled sites: CHANGELOG.md:16 (states only the default; true)
after:
src/superclaude/cli/cli_portify/commands.py:98:    "--max-convergence",
    help=(
        "Maximum convergence iterations for panel-review "
        "(default: 1; follows the 2-fix-cycle cap). "
        "The value is stored in the run config, but nothing reads it yet: "
        "the review loop always runs 1 iteration."
    ),
