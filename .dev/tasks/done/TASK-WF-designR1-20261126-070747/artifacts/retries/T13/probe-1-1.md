2641bb1a17f804be6b3dee862253d180d9622b18
## family: commands-file-completeness (from F1.1 of review r1-1)

- defect form: the commands file lists only the fenced blocks of Steps 2 to 6; commands the page writes inside table cells or prose are missing.
- search command (read-only): grep -n -E -e '^(gh|git|make|grep|uv|\./update|superclaude|/sc:)' ./artifacts/rehearsal-github-commands.sh.txt
- before-output: 36 lines match (the fenced commands only); no line has `gh run list`, `gh pr list`, `git remote -v`, `gh pr checks <m>` or `/sc:pr-submit`.
- coupled sites: the generator /tmp/t13-commands-826.py (outside the repository); the header comments of the commands file; `./artifacts/rehearsal-github.md` line 9 (describes the file as the commands of Steps 2 to 6); the page lines 66, 122, 129, 176 (docs/developer-guide/release-procedure.md).
after: 58 lines match the search; the commands now listed include gh run list (line 42), gh pr list, git remote -v (line 41), gh pr checks <m> (line 77) and /sc:pr-submit (line 31). Hit lines of the missing-command search: 7:# `git remote -v` and `git rev-parse --show-toplevel` are logged in the same shell call as the `git tag` and `git push`. 10:# The /sc 31:/sc 41:git remote -v 42:gh run list --repo <scratch-owner>/<scratch-repo> --workflow Tests --event push --branch master --commit <merge-sha> --json databaseId,status,conclusion 59:gh pr list --repo <scratch-owner>/<scratch-repo> --state open 77:gh pr checks <m> --repo <scratch-owner>/<scratch-repo> --watch 
