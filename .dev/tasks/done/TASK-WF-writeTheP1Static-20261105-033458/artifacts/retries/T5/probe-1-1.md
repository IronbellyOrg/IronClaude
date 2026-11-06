a07be8dcd1c742234d8e0c070804fdb5de05329d
family: ac-grep-visibility (F1.1)
defect form: an AC-named grep does not display a required item because the literal flag is absent on that line
search: grep -n -e '--report-dir' -- src/superclaude/skills/sc-impact-protocol/SKILL.md
before:
21:| Flag | Default | Validation | STOP → `status: blocked` (contract still written when
31:| `--unattended` | `false` | standalone argument token outside any quoted argument; nee
32:| `--report-dir` | unset | only with `--unattended`; same rules as `--output-dir` | ins
51:| 10 | Write outputs | Write `<output-dir>/impact.md` (section 6), then `<output-dir>/r
101:| `artifacts` | list[string] | other files written: `[]` with `--output-dir`; `impact.
coupled sites: the Will Not write-scope bullet (line 190); any other sentence in src/superclaude/skills/sc-impact-protocol/SKILL.md that names the report directory as <report-dir> without the literal flag
after:
21:| Flag | Default | Validation | STOP → `status: blocked` (contract still written when
31:| `--unattended` | `false` | standalone argument token outside any quoted argument; nee
32:| `--report-dir` | unset | only with `--unattended`; same rules as `--output-dir` | ins
51:| 10 | Write outputs | Write `<output-dir>/impact.md` (section 6), then `<output-dir>/r
101:| `artifacts` | list[string] | other files written: `[]` with `--output-dir`; `impact.
190:- Edit code, run tests, or build, sync or remove an index (Write and Edit touch only `
