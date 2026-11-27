# Draft notes

Leave a list empty (write "None") when there is nothing to report. "None" is the empty marker, never an item, and `- None` under both headings is the same state as empty notes. Items under New material cause no question: they are kept in the issue body and printed in the final output. One or more supported items under Contradictions cause exactly one question to the user.

## New material

<!-- Facts added to the issue body that the description did not contain, one per line, each with its source (path:line or command). List an assumption as `Assumption: <text>`. A contradiction line that lacks its category, the user's own words or its conflicting evidence belongs here instead. -->

- Tooling: codegraph and auggie were not available to this worker; the `/sc:analyze --depth deep` pass ran on Grep, Glob and Read only (following `~/.claude/commands/sc/analyze.md`; no `--output` file was requested, so no analysis report was written).
- A-001 (adversarial/merged-flags.md, agreed qualification): the count must be the last line on every path, after the Step 10 retire step and also on the `sys.exit(1)` path (src/superclaude/cli/main.py:271-296). Kept in Expected Behavior.
- A-002 (adversarial/merged-flags.md, agreed qualification): "copied" = the installed bucket of `install_all_skills`; skipped, served-by-command and failed skills are not counted; the zero case still prints 0. Kept in Expected Behavior.
- Citation correction to A-002: merged-flags.md cites the zero case as install_skills.py:142-143; in the checked-out code the early returns are at src/superclaude/cli/install_skills.py:80-81 ("No skills available to install") and :144-145 ("No skills to install"). The body uses the verified lines. Not a contradiction of the user's words.
- Observation (out of scope, not filed as a fix): src/superclaude/cli/install_skills.py:144-145 returns `(True, "No skills to install")` when `installed`, `skipped` and `served_by_command` are all empty, even if `failed` is non-empty, which drops the failure messages built at :139-142 and reports success. Relevant only because the count line prints 0 on that path.
- Observation: `superclaude update` calls the same `install_all_skills` (src/superclaude/cli/main.py:402), `install --list` returns early (main.py:174); the body scopes the change to `install` only.
- Environment facts added to the body: package version 6.1.0 (pyproject.toml:7), branch `qev-run`, commit 862384852 (git rev-parse), OS Linux 6.8.0-149-generic (uname -sr). These describe the code checkout, not the reporter's machine.
- Related issues: none (scout.md: no results for `superclaude install skills count`).
- Test-landscape facts: tests stub `install_all_skills` with 2-tuples (tests/cli/test_update_command.py:16-25,74-96; tests/cli/test_install_retired_mcp.py:514-534); direct callers unpack `(bool, str)` (tests/unit/test_cli_doctor.py:78; tests/troubleshoot/test_diagnostic_worker_contract.py:419); no test asserts a skills total or the last line of `install` output (grep of tests/).
- Proposed Solution and Fix approach design (optional `counts` out-parameter on `install_all_skills`, one echo in `install()` after Step 10 and before the exit check) comes from the codebase pass; it is a proposal for whoever implements, not text from the description.
- Assumption: the exact wording of the line is `Skills copied: N` (the description gives no wording; "how many skills it copied" only).
- Assumption: the count line applies to `superclaude install` runs that reach the install steps only; `install --list` (returns at main.py:174) and `superclaude update` (main.py:356-461) are unchanged.
- Assumption: the return type `Tuple[bool, str]` of `install_all_skills` stays unchanged, because existing tests and callers unpack a 2-tuple and stub it with 2-tuples (see test-landscape fact above); a stub that does not fill the out-parameter yields a count of 0.
- Assumption: severity in Impact Assessment is "low" (output only); the reporter gave no severity.
- Assumption: Priority is Medium, because the information is obtainable another way (`install --list`, the `- <name>` lines of the Step 4 output), so the "degraded behaviour with a workaround" trigger applies and no High/Urgent trigger does.
- Assumption: `docs/getting-started/installation.md` ("What's Installed", line 337) may or may not describe the install output; the doc step is marked conditional in Fix approach because the worker did not read that section in full.
- Assumption: no `make sync-dev` is needed, because the fix touches only `src/superclaude/cli/` and `tests/`, not an installed primitive.
- Pushback note (not a contradiction, for the Wave 5 comment, not the body): the debate (adversarial/merged-flags.md) judged the request a feature, since no documented behaviour promises a final count line; the issue is filed as a bug with the user's `--mode bug`.

## Contradictions

<!-- Only a supported contradiction of the user's own description, instruction or flag, one per line, in this form: category (reversed choice, dropped requirement, changed flag, or user-stated fact contradicted by verified code), the user's own words in quotes (or the flag as passed), and the conflicting evidence (draft text, or a path:line the worker read). A line missing any of the three parts belongs under New material. A worker's disagreement with a user-supplied flag is not a contradiction when the issue is filed with the user's flag. An addition that is the only evidence of a contradiction is listed here. Secrets rule: the worker never copies anything that looks like a secret (a key, token, password, credential, or a connection string with a password) or any text from ~/.env, environment variables or credential files into the issue body or these notes; if the draft would contain such material, list that here (the place, never the value) so the contradiction question is asked. -->

- None
