# Architecture analysis for issue 672

Command: `/sc:analyze src/superclaude/hooks --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g4/672/analyze`

Report structure: the installed analyze command's Output and Behavioral Flow sections, read before authoring.

## Scope and grounding

Target: the startup instruction boundary under `src/superclaude/hooks`, the narrowest source directory containing both registered SubagentStart loaders. Read-only supporting inspection covers the style they load and the existing startup tests. No hooks or tests were executed.

Codegraph: index_state=fresh, checked_at=2026-11-24T13:41:04Z; degraded: graph:empty

Graph access: mcp; worktree root: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup`. Graph layout covers only two indexed files here; shell scripts, JSON registrations and Markdown policy were inspected directly. Empty callers/callees for the top-level `output` constant are not evidence that the hook is unused; its registration is explicit in hooks.json. All findings below are confirmed by source reads.

Live evidence: issue #672 is OPEN, with one comment dated 2026-11-19. The comment reports 30/30 exact-content handoffs and 6/6 read-and-author handoffs succeeded despite the alleged prohibition appearing in all 36 recorded system-prompt snapshots. The comment explicitly says refusal, provenance, historical root cause and a fix were not established, and further repetition is paused. Those counts are issue-reported evidence, not rerun or independently verified experimental results.

## Severity-rated findings

1. **Medium, unresolved investigation gap, not a proven hook defect:** the repository exposes two real startup instruction inputs, but neither loader identifies the origin of the historical report-writing prohibition. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/hooks.json:159-177` registers both; `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/scripts/pragmatic-subagent.js:7-18` reads the installed user style, removes frontmatter and emits all remaining text; `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/scripts/freshness-subagent-start.sh:29-33` injects the installed Bash policy. Runtime contents can therefore differ from checked-in inputs. A source-only scan cannot establish the entire effective instruction stack of an earlier agent.
2. **Informational, positive architectural evidence:** the current checked-in style explicitly requires saved handoffs, not a blanket prohibition, at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/output-styles/pragmatic.md:206-213`. This supports the issue's expected behavior, but does not prove which higher-priority instructions an affected runtime received or that any later change fixed it.

No concrete defect was established in either loader by this quick static pass. The alleged prohibition's source and causal link to refusals remain UNVERIFIED.

## Code quality metrics

- Two registered startup instruction loaders were traced directly: one JavaScript loader and one shell loader.
- The policy-injection test file contains five tests: injection/counter, missing policy, malformed input, bounded lock contention and registration. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/hooks/test_freshness_subagent_start_policy.py:39-115` does not exercise the historical model refusal or prove instruction provenance. Its helper runs the shell hook with a temporary HOME at lines 25-36.
- `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/commands/test_pragmatic_plain_english.py:1-5,50-74` checks style wording and wrap-up structure, not agent behavior.
- Executed tests: zero, as required by the brief's prohibition on uv and files outside this report directory. No application source, installed policy or configuration was changed.
- Exact/near-exact prohibition search (`Do NOT Write|report/summary/findings/analysis|Return findings directly|reply.only`) returned no matches under `src/superclaude`. That bounded textual result does not exclude other wording, provider prompts or historical inputs. A separate installed-Markdown search found a memory note in another project, not an authoritative injection source; its content was not read or used.

## Security and performance boundaries

No security vulnerability or performance defect was established by the scoped static inspection; neither property was dynamically tested. Reading complete historical prompts can expose private data, so future provenance work should retain minimal sanitized evidence and must not publish raw prompts. No policy override, renaming workaround or reply-only bypass is authorized by this analysis. Hook execution was deliberately omitted because the shell loader writes user-state files.

## Recommendations

1. Keep issue #672 open as a still-relevant investigation, not a verified hook bug and not an active fix. Follow its latest comment: compare one original refusal with one successful control before resuming synthetic repetitions.
2. Compare the effective model, original dispatch wording, user/project/agent instructions and actual emitted hook context with sanitized provenance for each input. The historical source and authority of the prohibition remain UNVERIFIED.
3. Select a fix boundary only after the comparison establishes one. Reuse the existing startup-policy test pattern if that boundary is a hook; use the actual coordinator refusal path if it is coordination. Do not assume that current successful writes, or the absence of an exact phrase in tracked source, resolve the historical incident.
4. Related issue #465 concerns a particular verifier delivery failure and recovery. Its live issue describes a distinct incident; neither duplicate status nor a hard dependency on it is established.

PR discovery: the issue body/comment mentions no numbered PR. Title/body searches for 672 returned unrelated numerical matches (#84, and a broader search also #197); no fix relationship was established. A dedicated title search for the exact phrase "report-writing prohibition" returned no PR. This is bounded negative evidence, not an exhaustive GitHub timeline or comment search.

Minor review follow-up candidates: none beyond the unresolved investigation above. No remediation or GitHub write was performed.
