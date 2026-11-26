Title: Make superclaude install end with the number of skills copied
# Draft notes

Leave a list empty (write "None") when there is nothing to report. "None" is the empty marker, never an item, and `- None` under both headings is the same state as empty notes. Items under New material cause no question: they are kept in the issue body and printed in the final output. One or more supported items under Contradictions cause exactly one question to the user.

## New material

<!-- Facts added to the issue body that the description did not contain, one per line, each with its source (path:line or command). List an assumption as `Assumption: <text>`. A contradiction line that lacks its category, the user's own words or its conflicting evidence belongs here instead. -->

- Preserved mode bug, type cli, depth standard and complexity Medium, per the dispatch instructions; no reclassification is proposed. Retained the synthetic marker verbatim from description.md:3.
- Existing count output occurs during the skills phase, before later phases; the CLI has no final copied-skills summary (src/superclaude/cli/main.py:202-296).
- Batch installation tracks successful, skipped, failed and command-served skills but returns only a success/message pair; single-skill success follows copytree (src/superclaude/cli/install_skills.py:62-150; src/superclaude/cli/install_skill.py:46-55).
- The last current output varies with retirement outcomes; the empty-state line is `   No retired commands, skills or agents present.` (src/superclaude/cli/install_retired_files.py:269-305). This is static evidence, not captured runtime output.
- Orca skills are installed through a separate CLI and its completion/presence check is not a per-run copied count (src/superclaude/cli/install_user_setup.py:323-366).
- Proposed disposable-home reproduction and low severity/output-only blast radius based on the missing summary and unchanged install control flow; no affected OS, package version or error output was provided (description.md:3; src/superclaude/cli/main.py:202-296).
- Priority Low uses the Cosmetic, wording, or docs only trigger in refs/create.md:73-82; no higher-priority trigger is established by the request or code pass.
- Proposed structured count exposure with compatibility for existing callers, final print after retirement, and preserved aggregate exit behavior (src/superclaude/cli/install_skills.py:62-150; src/superclaude/cli/main.py:271-296). This is implementation guidance, not an existing API.
- Proposed ordered workflow, implementation and PR submission against IronbellyOrg/IronClaude, base integration, as directed by dispatch; the multi-source-file plan requirement is documented in src/superclaude/core/HOW-WE-WORK.md:17-19.
- Proposed unit and CliRunner regression tests, successful/zero/forced/skipped/failed copy cases, retirement output ordering, and unchanged list/update contracts. Existing relevant coverage is in tests/unit/test_cli_install.py:683-727 and tests/cli/test_install_retired_mcp.py:514-549. Proposed tests are not implemented or executed.
- Full-suite, lint and sync gates come from Makefile:12-15,47-50,108-109,165-166 and project workflow instructions; manual verification is isolated from the reviewer's real home.
- No duplicate links were added: scout.md:28-33 reports none found, not proof that none exist.
- Standard /sc:analyze behavior was followed without a depth flag using Glob, Grep and Read. Codegraph and Auggie MCP tools are absent from this session's tool list; the codegraph CLI reports Not initialized, version 1.6.2. Installed and project CODEGRAPH.md were missing, so the canonical in-checkout guide src/superclaude/core/CODEGRAPH.md was read. Installed HOW-WE-WORK.md was also missing, so its canonical in-checkout source was read. No codegraph initialization or indexing was performed.
- Codegraph: index_state=not_initialized, checked_at=2026-11-26T18:30:35Z; degraded: graph:not_initialized; access=cli; worktree_root=/tmp/createQuestionEv-scratch/clones/standard-flag-preserved. Readiness was checked once; all lookups used the file-tool fallback. The codegraph guide recommends `/sc:graph status` for this state; graph availability is not a blocker for this issue.
- Assumption: “skills it copied” means successfully copied SuperClaude batch skill directories during this invocation, including forced replacements, excluding existing skipped skills, command-served skills, failures, and separately delegated Orca skill installation.
- Assumption: use the final-line format `Skills copied: N`, including zero, on completed normal installation paths even when a handled phase fails; preserve failure status and leave `install --list` and `update` output contracts unchanged.
- Assumption: deterministic stubbed CLI tests are the primary verification so this output change does not require network downloads, real MCP registration changes or modifying the reviewer's home.

## Contradictions

<!-- Only a supported contradiction of the user's own description, instruction or flag, one per line, in this form: category (reversed choice, dropped requirement, changed flag, or user-stated fact contradicted by verified code), the user's own words in quotes (or the flag as passed), and the conflicting evidence (draft text, or a path:line the worker read). A line missing any of the three parts belongs under New material. A worker's disagreement with a user-supplied flag is not a contradiction when the issue is filed with the user's flag. An addition that is the only evidence of a contradiction is listed here. Secrets rule: the worker never copies anything that looks like a secret (a key, token, password, credential, or a connection string with a password) or any text from ~/.env, environment variables or credential files into the issue body or these notes; if the draft would contain such material, list that here (the place, never the value) so the contradiction question is asked. -->

None
