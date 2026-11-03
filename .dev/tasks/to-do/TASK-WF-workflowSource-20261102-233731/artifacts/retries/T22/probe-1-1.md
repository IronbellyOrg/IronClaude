cf84f99d0fcbf743ef204e55965452ac464dcb53
family=output-default-first-input
defect form: --output default described as the spec file's folder; code uses the first positional input's folder (commands.py:331)
command: grep -n -i -e "parent dir" -e "parent directory" -e "parent of" -e "spec's parent" -- docs/guides/roadmap-cli-tools-release-guide.md
before:
134:| `--output` | Path | Parent dir of the spec file | Output directory for all pipeline artifacts. Created automatically if it doesn't exist. |
363:All artifacts are written to the output directory (default: parent directory of the spec file).
1226:Runs the full 11-step pipeline with default agents (`opus:architect` + `sonnet:architect`) and standard depth (2 debate rounds). Artifacts written to the spec's parent directory.
coupled sites: src/superclaude/cli/roadmap/commands.py:331; guide line 127 (inputs in any order); guide line 1226 example text (single spec input, so its folder is the first input's folder; true as written)
after:
134:| `--output` | Path | Parent dir of the first input file | Output directory for all pipeline artifacts. Created automatically if it doesn't exist. The default is the folder of the first file you list, whatever its type (`--help` calls it the spec file). |
363:All artifacts are written to the output directory (default: parent directory of the first input file).
1226:Runs the full 11-step pipeline with default agents (`opus:architect` + `sonnet:architect`) and standard depth (2 debate rounds). Artifacts written to the spec's parent directory.
