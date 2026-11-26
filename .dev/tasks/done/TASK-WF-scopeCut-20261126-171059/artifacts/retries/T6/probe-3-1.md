d3882935c4821173ac0f11327bd180eb9bb2e1bb
family page-refused-bug-overclaim
defect form: the page says a whole class of script output is a bug or an error of one kind, when the script produces it on purpose for some inputs
command: grep -n -i -E "bug|report it|allowlist" docs/developer-guide/branch-protection-multi-repo.md
before:
106:- `refused: <text>` with some other text means the script's own allowlist blocked a call. That is a bug in the scrip
132:Dropped from the first plan to keep this small, to be decided and built later if they are wanted: a persistent file of target repos with a status per repo and one workflow ... (the word "allowlist" names a dropped follow-up; not a defect)
coupled sites: line 106 only.
family page-refusal-cause-imprecise
defect form: a table row lists a cause that never produces that text
command: grep -n -E "is empty|an empty|branch not supported" docs/developer-guide/branch-protection-multi-repo.md
before:
40:   Read the exit status of each ... "not an empty list" (prose, not a cause list; not a defect)
93:| `branch not supported: not a plain branch name: '<name>'` | The default branch name is empty, contains `*` or `~`, ...
105:- Usage mistakes exit 64 ... `--org: <reason>` (an empty name, or the upstream organization) ...
coupled sites: line 93 (the row), line 90 (`repo has no default branch`, the cause that an empty name reaches first), line 105 (reasons of usage errors).
family page-usage-reason-incomplete
defect form: a list of reasons for one message is shorter than the script's conditions
command: grep -n -i -E "usage|--org:|exactly one|an empty name" docs/developer-guide/branch-protection-multi-repo.md
before:
105:- Usage mistakes exit 64 with `usage error:` and one of `--repo takes exactly one repo name`, `--org: <reason>` (an empty name, or the upstream organization) ...
coupled sites: line 105 only.
after:
--- fam3
106:- `refused: <text>` with some other text means the script's allowlist refused a call. The usual cause is a default b
132:Dropped from the first plan to keep this small, to be decided and built later if they are wanted: a persistent file 
--- fam4
40:   Read the exit status of each. A command that failed (for example HTTP 403 or 404) means **unknown**, never "0": a 
93:| `branch not supported: not a plain branch name: '<name>'` | The default branch name contains `*` or `~`, or starts 
105:- Usage mistakes exit 64 with `usage error:` and one of `--repo takes exactly one repo name` (also for `.`, `..` and
--- fam5
105:- Usage mistakes exit 64 with `usage error:` and one of `--repo takes exactly one repo name` (also for `.`, `..` and
