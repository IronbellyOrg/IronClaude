# Draft notes

Leave a list empty (write "None") when there is nothing to report. "None" is the empty marker, never an item, and `- None` under both headings is the same state as empty notes. Items under New material cause no question: they are kept in the issue body and printed in the final output. One or more supported items under Contradictions cause exactly one question to the user.

## New material

<!-- Facts added to the issue body that the description did not contain, one per line, each with its source (path:line or command). List an assumption as `Assumption: <text>`. A contradiction line that lacks its category, the user's own words or its conflicting evidence belongs here instead. -->

Title: Handle empty descriptions in issue creation
- The crash was not reproduced in this static quick pass; exact error, affected environment and impact remain unknown.
- The specified expected STOP message is `--create needs a description` (src/superclaude/commands/issue.md:56).
- Reproduction suggestion: `/sc:issue --create ""` (derived from the reported empty-description input).
- The command defines validation before activation and then invokes the protocol skill (src/superclaude/commands/issue.md:51-56,108-114); the skill also specifies a pre-activation STOP (src/superclaude/skills/sc-issue-protocol/SKILL.md:156), and create prerequisites are in src/superclaude/skills/sc-issue-protocol/refs/create.md:11-16.
- Existing test checks the rule's presence in command text rather than executing the command (tests/commands/test_issue_command.py:183-191).
- Codegraph MCP and Auggie tools were unavailable; the quick pass used Glob, Grep and Read. The codegraph CLI exists but MCP access was unavailable.
- Repo and base branch are IronbellyOrg/IronClaude and integration, supplied in the task.
- Suggested workflow: `/sc:troubleshoot`, `/sc:implement`, `/sc:pr-submit --monitor 3`; first reproduce and locate the entry point, then implement and test the responsible component (src/superclaude/commands/issue.md:51-56; tests/commands/test_issue_command.py:183-191).
- Regression gate and review: `uv run pytest`, `make lint`, `make verify-sync`, plus a controlled empty-input check (project CLAUDE.md testing and sync guidance).
Assumption: The reported crash is reproducible, so the High priority trigger is a documented command failing.
Assumption: If validation fails in practice, fix the responsible command or protocol component to honor the existing STOP rule and add coverage in the appropriate test.
Assumption: Add an execution regression once the entry point is identified, checking the STOP message and that no issue is created.

## Contradictions

<!-- Only a supported contradiction of the user's own description, instruction or flag, one per line, in this form: category (reversed choice, dropped requirement, changed flag, or user-stated fact contradicted by verified code), the user's own words in quotes (or the flag as passed), and the conflicting evidence (draft text, or a path:line the worker read). A line missing any of the three parts belongs under New material. A worker's disagreement with a user-supplied flag is not a contradiction when the issue is filed with the user's flag. An addition that is the only evidence of a contradiction is listed here. Secrets rule: the worker never copies anything that looks like a secret (a key, token, password, credential, or a connection string with a password) or any text from ~/.env, environment variables or credential files into the issue body or these notes; if the draft would contain such material, list that here (the place, never the value) so the contradiction question is asked. -->

- user-stated fact contradicted by verified code: "crashes in `src/superclaude/skills/sc-issue-protocol/scripts/create_issue.py`"; Glob listing of `src/superclaude/skills/sc-issue-protocol/scripts/*` shows only `clickup_claim.py`, `origin_repo.py`, and `orca_worktree.py`, with no `create_issue.py` in this checkout. The command specifies a STOP before skill activation at `src/superclaude/commands/issue.md:51-56,108-114`; this does not by itself disprove an observed crash elsewhere.
  - Answer (contradiction question, asked once): "Keep my wording". The body states the user's path as the crash location; the "file is absent" notes were removed from the body.
