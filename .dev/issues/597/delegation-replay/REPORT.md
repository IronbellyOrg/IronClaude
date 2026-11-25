# Delegation, Tavily and Fallback Replay Report

Adapted from the cli-eval run-report template for eight direct live CLI sessions, not the null eval executor.

## Verdict
**On this sample, the changed rule moved first-action routing from native web to the research servers in both cases where the servers were connected; the delegation branch itself was never triggered.** Same model (`claude-sonnet-5-5`), same prompts, same tools; the only difference was rule 11.

| Case | Before (no rule) | After (rule 11) |
|---|---|---|
| A, guide agent available, docs question, 2 repeats | 0 of 2 passed: both went straight to native WebFetch (4 WebFetch calls each, plus 1 and 2 Grep), never Context7 | 2 of 2 passed: Context7 resolve then query, 2 calls each, no native web |
| B, current information, 1 pair | FAIL: WebFetch first, then Tavily search, then WebFetch | PASS: Tavily search, then Tavily extract twice; no native web |
| C, research server disconnected, 1 pair | PASS: native fallback worked, 5 native calls | PASS: native fallback worked, 3 native calls |

Counts are tiny (2 + 1 + 1 per arm) and cannot show a statistical difference. They do show that the baseline failure is not rare in this setup, and that the one added line reversed it every time it was tried.

**What this does not show:** no session delegated to the guide agent, so the clause "check the delegate's tools, else look up directly" was never exercised. The before-arm bypass here was the parent itself choosing native WebFetch, which is the other half of the original symptom. The historical failure (delegating a docs question to a native-only guide) still did not reproduce in any arm.

## Counts / totals
| Session | Pass/fail | First research action | All tool calls in order (Grep is local search, not research) | Turns | Cost USD | Wall sec |
|---|---|---|---|---|---|---|
| A-before-r1 | FAIL | WebFetch | WebFetch, WebFetch, Grep, WebFetch, WebFetch | 6 | 0.3933 | 39.1 |
| A-before-r2 | FAIL | WebFetch | WebFetch, WebFetch, Grep, WebFetch, Grep, WebFetch | 7 | 0.3130 | 40.9 |
| A-after-r1 | PASS | Context7 resolve | Context7 resolve, Context7 query | 3 | 0.1167 | 13.6 |
| A-after-r2 | PASS | Context7 resolve | Context7 resolve, Context7 query | 3 | 0.0266 | 13.1 |
| B-before-r1 | FAIL | WebFetch | WebFetch, Tavily search, WebFetch | 4 | 0.1697 | 54.5 |
| B-after-r1 | PASS | Tavily search | Tavily search, Tavily extract, Tavily extract | 4 | 0.1633 | 21.8 |
| C-before-r1 | PASS | WebFetch (valid fallback) | WebFetch, WebFetch, Grep, WebFetch, WebFetch | 6 | 0.3621 | 38.6 |
| C-after-r1 | PASS | WebFetch (valid fallback) | WebFetch, WebSearch, WebFetch | 4 | 0.2656 | 22.6 |

All 8 exited 0 with `success`, no tool errors, no permission denials, none timed out. Total reported API cost **$1.8103** (list price, not an invoice; MCP service charges not itemized). The authorized ceiling was 8 sessions at $1 each.

## Per-eval
- **A (guide agent present):** the init roster listed `claude-code-guide` and the `Task` delegation tool in all four sessions, so delegation was possible. Nobody used it. The before arm answered by fetching documentation pages natively; the after arm used Context7 and finished in 3 turns.
- **B (Tavily):** the after arm followed the rule's page-confirmation wording: one search, then extracts of candidate pages, with no further search. This is recorded as an observation, not a pass condition.
- **C (fallback):** with no research server connected, both arms completed using native tools and neither errored or refused. The rule's "native tools stay valid when a server is missing" clause held; it did not make the model stall. Neither answer said the research servers were unavailable, so fallback disclosure was not observed in either arm (this rule does not ask for it).

## Forensics
All files are under `.dev/issues/597/delegation-replay/`:
- `criteria.json`: pass and fail rules, written before any session ran.
- `run.py`: launcher. It asserts that removing exactly rule 11 from the working copy gives `git show HEAD:src/superclaude/core/CLAUDE.md`, pins `claude-sonnet-5-5` (and asserts the name contains no "opus"), refuses to run twice (`started.json` is created exclusively), and killed nothing (no timeouts).
- One folder per session (`A-before-r1`, and so on) with raw `stream.jsonl`, scrubbed `attempt.json`, `core-context.md`, `prompt.txt` and `stderr.txt`. `stderr.txt` is empty in A-after-r1, A-after-r2 and B-after-r1. In the other five it holds one 98-byte warning line, `[claude-code:unrecognized_model]` naming `claude-gw-tier2[1m]`, discussed below.
- `changed-rule.txt`: the single differing line.

**Second model key.** Every session that used native WebFetch also lists `claude-gw-tier2[1m]` under served models; sessions that did not use WebFetch list only Sonnet 5.5 (A-after, B-after). The five sessions that list it each wrote one `stderr.txt` warning naming the step that used it: `query_source` is `web_fetch_apply` in A-before-r1, A-before-r2, B-before-r1 and C-before-r1, and `web_search_tool` in C-after-r1 (the only session that called WebSearch). So the trace itself shows that **native WebFetch and WebSearch each route a helper call to this second model**. That the second model sits in the gateway's small-model slot is an **inference** from the environment (`ANTHROPIC_DEFAULT_HAIKU_MODEL` is `claude-gw-tier2[1m]`, read in this session's environment, not recorded by the run). It is not the Opus slot (`ANTHROPIC_DEFAULT_OPUS_MODEL` is `claude-gw-tier1a[1m]`). Every `model` value in every stream is `claude-sonnet-5-5`; no Opus model appears in any session.

The guide agent in cases A is my **reconstruction**: the host's advertised description with tools limited to Glob, Grep, Read, WebFetch and WebSearch, model pinned to Sonnet 5.5. It is not the host's own definition.

## Surfaced issues
- Very small samples; arm order alternated (A: before, after, after, before; B: after, before; C: before, after), not randomized. Cache warmth, backend drift and sampling noise were not controlled.
- The delegation clause is untested. A prompt that pushes the model toward delegation (for example naming the guide agent) would be needed to exercise it; none was run, and none is authorized.
- Case A's before arm differs from the earlier matched replay, where the before arm used Context7 without a guide agent in the roster. The guide agent being present is the only setup difference, so its presence may have changed baseline behavior; with so few runs this is a hypothesis, not a finding.
- Inline and built-in plugins still loaded in every session; this was not plugin-free.
- Answer correctness was not audited.
- No commit, push, install or settings change occurred. The rule and its three static tests remain uncommitted.
