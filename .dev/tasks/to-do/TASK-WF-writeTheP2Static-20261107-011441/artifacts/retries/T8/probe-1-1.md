8f58b757f409945b93ce1e58f55ad922f6e33d5e
family: report-dir-both-flags
defect form: the section lets --output and --report-dir coexist.
command: grep -n -F -e 'both' -e 'same directory' -e 'never both' -- src/superclaude/commands/release-split.md
before-output:
62:| `--report-dir` | | No | - | With `--unattended`: the report directory, the same directory `--output` names (see `##
115:- **Report directory.** `--output <dir>` (or `-o`) or `--report-dir <dir>`; `--report-dir` follows the same path rul
coupled sites: the Options-table --report-dir row; the Report directory bullet; the UNATTENDED_EXPECT phrases of release-split.
after:
62:| `--report-dir` | | No | - | With `--unattended`: the report directory, instead of `--output`, never both (see `## U
115:- **Report directory.** Exactly one of `--output <dir>` (short form `-o`) or `--report-dir <dir>`; both, or neither,
