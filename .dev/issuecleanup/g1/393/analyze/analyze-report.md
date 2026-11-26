# Retry adviser architecture analysis

Template: ../../362/report-template.md, Analysis template.

## Scope and grounding
Command: `/sc:analyze src/superclaude/skills/sc-implement-protocol/refs --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g1/393/analyze`.

The target is the narrowest common directory covering retry selection and its saved ledger. Four Markdown reference files were discovered; this pass examines the model-selection parts of retry.md and ledger.md, not unrelated revert or review internals. Supporting reads cover the adviser definition, three test files, the plugin retry mirror and launcher alias exports.

Codegraph: index_state=fresh, checked_at=2026-11-23T23:07:22Z; degraded: graph:empty.

Access: mcp. Worktree root: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup. The graph returned no files for the Markdown-only target, which the guide says is not indexed; evidence therefore uses Glob, Grep and Read. No index mutation was performed.

## Architecture and metrics
This is an instruction-driven retry process, not a Python adviser dispatcher. The parent obtains two advisers' answers before reverting and saves them verbatim: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-implement-protocol/refs/retry.md:58-75. The adviser is read-only, with Read/Grep/Glob and high effort but no fixed model: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/agents/implement-retry-adviser.md:1-6.

Selection has four primary environment-variable rungs and three alias fallback rungs. Nonempty primary variables activate that ladder without a stated spawn-capability check: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-implement-protocol/refs/retry.md:162-185. The ledger records the executor's rung, not a launchable adviser argument: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-implement-protocol/refs/ledger.md:94-112. This session's Agent tool accepts only opus, sonnet, haiku and fable as its model argument, not arbitrary environment model IDs.

Scope metrics: 4 reference files discovered; 2 issue-relevant reference files inspected; 1 adviser definition and 3 supporting test files inspected. These are scope counts, not whole-package quality or coverage metrics.

## Severity-rated findings
1. **Medium: selected adviser models lack a verified launch mapping.** The primary ladder is enabled by variable presence, but the specified Agent model argument cannot carry its arbitrary model IDs; the file explicitly says no GPT spawn path is verified. Adviser B has a strongest-reachable fallback, but no corresponding general mapping is specified for adviser A, the critique adviser or the top-rung advisers in escalation 2. This keeps #393 valid without proving every execution crashes. Evidence: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-implement-protocol/refs/retry.md:162-185. The plugin mirror carries the same rules: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/plugins/superclaude/skills/sc-implement-protocol/refs/retry.md:162-185.
2. **Medium: inspected tests do not establish launchability.** The model-policy test pins exported names, archive tests accept rung tokens, and family tests use local dictionaries and pin the absence of a verified GPT path. Those checks neither call Agent nor validate every selected argument against its accepted aliases. Evidence: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/skills/test_model_alias_policy.py:217-228; /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/skills/test_workflow_archive.py:798-830; /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/skills/test_implement_adviser_family.py:14-48,58-85.

No security or performance conclusion is claimed by this architecture-only pass.

## Recommendations and roadmap
Keep #393 open. Prefer the smallest complete correction: explicitly select only supported Agent aliases for every adviser role and state that gateway routing does not prove a particular underlying model family. Do not restore misspelled unset variable names merely to disable the primary ladder by accident.

Update the retry model policy and plugin mirror, check the ledger's executor-rung meaning, and add cases for populated primary variables, missing variables, unavailable other-family models, adviser A/B, critique and escalation 2. Verify actual launch arguments before claiming named-model fidelity. Preserve readability of existing ledger rung tokens; avoid a grammar migration without a demonstrated need.

## Verification limits
Static quick analysis only: no tests, live helper launch, proxy call, environment-defaults read, source change or GitHub write. Current underlying gateway model and model-family fidelity are UNVERIFIED. The model schema is observed from this session's Agent tool, not a new runtime probe. The whole reference directory was not audited. Augment's first request failed because its default main branch does not exist; retrying explicitly on master succeeded. Graph lookup found no Markdown files, so no no-callers claim is made. Initial report edits were blocked by the freshness hook; reading the stubs resolved that restriction before population.
