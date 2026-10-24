# codecov/codecov-action v4: input and token rules (Task 2)

## Sources

- Primary: README of codecov/codecov-action at the `v4` tag, https://github.com/codecov/codecov-action/blob/v4/README.md
  (tag `v4` resolves to commit b9fd7d16f6d7d1b5d2bec1a2887e65ceed900238; fetched from https://raw.githubusercontent.com/codecov/codecov-action/v4/README.md, 163 lines; line numbers below are lines of that file).
- Secondary: Context7 library ID `/codecov/codecov-action` (indexes the README on the main branch, which is v5 and later, not v4). Used only for the v5 deprecation notice in question 1.

## Question 1: is the `file` input deprecated in favor of `files`?

At the v4 tag: no. Both inputs are listed as valid, neither carries a deprecation note.

- v4 README line 94: "| `file` | Path to coverage file to upload | Optional"
- v4 README line 95: "| `files` | Comma-separated list of files to upload | Optional"
- v4 README usage example (lines 40-45) uses the plural form: "files: ./coverage1.xml,./coverage2.xml # optional"

The deprecation exists only from v5 on (Context7 `/codecov/codecov-action`, source https://github.com/codecov/codecov-action/blob/main/README.md, "v5 Release > Migration Guide"):

- "`file` (this has been deprecated in favor of `files`)"

Consequence: `file` works at v4 but is the name v5 removes; `files` is valid at v4 and stays valid after a later bump to v5.

## Question 2: is a token required for an upload from a push to master?

Yes. v4 dropped tokenless uploads; the only exception is a pull request from a fork.

- v4 README line 84: "| `token` | Repository Codecov token. Used to authorize report uploads | *Required"
- v4 README line 12: "Tokenless uploading is unsupported. However, PRs made from forks to the upstream public repos will support tokenless (e.g. contributors to OSS projects do not need the upstream repo's Codecov token)."
- v4 README usage example line 45: "token: ${{ secrets.CODECOV_TOKEN }} # required"

Events covered by the tokenless exception: pull requests from forks into a public upstream repository only. A push to master (and a pull request from a branch of the same repository) is not covered, so the token is needed for this workflow's push and pull_request runs.

## Question 3: are `flags`, `name` and `fail_ci_if_error` still valid v4 inputs?

Yes, all three are listed at the v4 tag.

- v4 README line 93: "| `fail_ci_if_error` | Specify whether or not CI build should fail if Codecov runs into an error during upload | Optional"
- v4 README line 96: "| `flags` | Flag upload to group coverage metrics (e.g. unittests \| integration \| ui,chrome) | Optional"
- v4 README line 99: "| `name` | User defined upload name. Visible in Codecov UI | Optional"

Decision: input name files; token: ${{ secrets.CODECOV_TOKEN }} is added.
