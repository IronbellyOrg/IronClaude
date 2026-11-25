# Issue 597 closeout check (2026-11-25)

## Verdict: every criterion PASS on the merged rule; no rule change needed, so no new branch was made. Evidence is small (one session per case).

## Setup
- Merged rule = rule 11 in `src/superclaude/core/CLAUDE.md` at `origin/integration` d3a1059f0 (PR 828 included). The "before" arm is the same file with only rule 11 removed.
- Tests on that commit: `uv run pytest tests/core -q` 99 passed; `make lint` passed. Output: /home/coder/workspaces/worktrees/IronClaude/issue-597/.dev/issues/597/closeout-replay/tests-lint.txt
- 6 real sessions, model `claude-sonnet-5-5` only (no Opus). Total cost $1.48, cap $1 per session. A second model name, `claude-gw-tier2[1m]`, appears only in the session that used WebFetch (the gateway's page-summarizing step, as in the earlier round).
- A "claude-code-guide" agent with only Glob, Grep, Read, WebFetch, WebSearch (no Context7/Tavily) was defined in the G sessions. It is my reconstruction of the host's agent, not the original.
- Harness and raw transcripts: /home/coder/workspaces/worktrees/IronClaude/issue-597/.dev/issues/597/closeout-replay/run.py, /home/coder/workspaces/worktrees/IronClaude/issue-597/.dev/issues/597/closeout-replay/<case>/stream.jsonl (+ prompt.txt, attempt.json, stderr.txt).

## First tool call per session (from the transcripts)
| Session | Question | Rule | First tool call | Later calls | Delegated? |
|---|---|---|---|---|---|
| D1-docs-after-r1 | Next.js 15 streaming route handler | with | context7-resolve-library-id | context7-query-docs | no |
| T1-current-after-r1 | latest Playwright release | with | context7-resolve-library-id | Tavily search, then 3 Tavily extracts | no |
| G1-natural-guide-before-r1 | Claude Code PreToolUse hook | without | context7-resolve-library-id | context7-query-docs | no |
| G1-natural-guide-after-r1 | same | with | context7-resolve-library-id | context7-query-docs | no |
| G2-subagent-guide-before-r1 | hide thinking/tool details, "use a subagent if you can" | without | **Agent -> claude-code-guide** | guide made 7 WebFetch, 6 Grep, 1 Read; no Context7/Tavily | **yes (the bug)** |
| G2-subagent-guide-after-r1 | same | with | context7-resolve-library-id | 2 context7-query-docs | **no**; the answer says it ran the lookup itself because the guide agent has no context7 tools |

No session with the rule made any native WebFetch/WebSearch call.

## Criteria of issue 597
1. Docs questions default to Context7: **PASS** (D1, G1 both arms, G2 after: Context7 first).
2. Current-information questions default to Tavily: **PASS, with a caveat.** Tavily ran second, not first: the first call was a Context7 library lookup (Playwright is also a library), then Tavily search and extract, and no native web call. A strict reading of "first call is Tavily" is not met by this one sample. The earlier replay (/home/coder/workspaces/worktrees/IronClaude/issue-597/.dev/issues/597/delegation-replay/REPORT.md) saw Tavily first for the same question.
3. Native tools remain valid fallbacks: **PASS**, from the earlier replay (research server disconnected, native fallback worked). Not rerun now.
4. Delegation goes to an agent with the research tools, or the orchestrator looks it up itself: **PASS.** Without the rule the model delegated to the native-only guide; with it, it did the Context7 lookup itself (G2 pair).
5. Testing note (first call Context7/Tavily, delegated lookup checked): **PASS**, per the table. The G2 pair is the delegated-lookup check.

## Limits
- One session per case, no statistics. Order not randomized. Answer correctness not audited.
- G1 (natural question) did not delegate in either arm, so only G2 (explicit "use a subagent") shows the delegation effect.
- The rule was not tested on a native-only agent other than the reconstructed guide.

## Rule change
None required. No branch, no commit, nothing pushed. This run left the original branch `ironbelly/issue-597` as it was (I briefly detached to origin/integration to run the tests and returned).

## Recommendation
Close issue 597 as done. The only soft spot is criterion 2 order (Context7 before Tavily on a library-release question); the owner may accept it or ask for a wording tweak.
