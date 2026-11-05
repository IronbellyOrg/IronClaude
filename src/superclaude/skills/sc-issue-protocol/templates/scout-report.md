# Scout report

- Mode: <claim | create>
- Repo: <owner/repo>
- Written by: issue-worker-t3

<!-- Fill the section for this mode and delete the other one. Write "Not known yet" where nothing is known. -->

## Claim

- Issue: #<N>
- url: <the url field returned by the issue lookup>
- is_pull_request: <true when url contains /pull/, else false>
- State: <OPEN | CLOSED>
- Assignees: <logins, or "none">
- Current login: <login>
- Earlier claim comment ID: <id, or "none">
- Earlier accuracy-check comment ID: <id, or "none">
- Created at: <createdAt>

### Merged pull requests since creation

- Result truncated at the 200 limit: <yes | no>

| PR | Title | Merged at | Changed files |
|---|---|---|---|
| #<number> | <title> | <mergedAt> | <paths> |

### Commits on the default branch since creation

| Commit | Changed files |
|---|---|
| <sha> | <paths> |

### First guesses

- Complexity: <simple | medium | complex>: <one-line reason>
- Type: <feature | bug>: <one-line reason>

## Create

### Repo labels

<label names, one per line>

### Possible duplicates

| Issue | Title | State | URL |
|---|---|---|---|
| #<number> | <title> | <state> | <url> |
