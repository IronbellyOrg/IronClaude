<!-- /sc:issue feature template (simple). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. -->

## Feature Summary

Add an advisory Jev preflight for `/sc:troubleshoot`: TypeSafe's Jev (System One) model reads the user's prompt and recommends the `--type` flag (and, later, `--depth`/`--scope`), behind a measured, standalone component rather than a gateway rewrite. The first two steps are a keyword-table fix and a Jev-vs-table accuracy comparison; the standalone preflight is built only if Jev clearly beats the table.

## Problem Statement

Today `/sc:troubleshoot` auto-detects `--type` in Wave 0 of `~/.claude/skills/sc-troubleshoot-protocol/SKILL.md` from a keyword table (SKILL.md lines 152-159): stack trace or exception name -> `bug`; "tsc", "lint", "build", `make`, CI log -> `build`; "slow", "latency", "p99", "memory", "leak", profiler output -> `performance`; "production", "deploy", "container", "env var", "service won't start" -> `deployment`; "auth", "token", "leak", "exposed", "CVE", "vulnerab" -> `security`; "pytest", "jest", "flake", "intermittent", "passing locally" -> `test`. On ambiguity the type is left unset.

The gap: a prompt like `/sc:troubleshoot "ccsession is taking too long to load"` matches none of the performance keywords, so its type stays unset even though a human immediately reads it as a performance issue. "leak" is also listed under both performance and security, so it is ambiguous by construction.

What `--type` changes: it picks the Tier 2 specialist agents (SKILL.md lines 380-389, one row per type) and raises the escalation bar for security (`refs/escalation-rubric.md`: `--type security` and confidence below 0.95 escalates; the default gate is 0.85). A wrong type is mostly harmless except for security.

The model that runs Wave 0 already reads the prompt, so Jev adds no new reasoning there. What it can add: repeatable answers (same prompt, same flags), calibrated probabilities that can be thresholded, an audit trail, and a measurable accuracy number.

## User Story

As a user of `/sc:troubleshoot`, I want the command's flags (starting with `--type`) to be chosen accurately from my plain-English prompt, so that the right specialist agents and escalation rules apply without me memorizing the flag syntax.

## Proposed Solution

**Recommendation from the analysis session (2026-11-17, repository checkout; nothing was run against the live Jev API): standalone, advisory, measured; not the gateway.**

Which flags a preflight may and may not decide:

- Safe for Jev: `--type` (one Choice over the 6 types plus a companion Noul asking whether any type fits), `--depth` (a Score, or small Noul questions: intermittent? multi-component? security-sensitive?), `--scope` (code extracts candidate paths and symbols from the prompt; Jev picks among them).
- Never inferred by a preflight: `--fix` (authorizes remediation), `--unattended`, `--report-dir`, `--output-dir`, `--caller`, `--context`, `--models`, `--no-mcp`, `--no-doc-discovery`, `--no-escalate`. They describe the operator's intent or environment, not the symptom.

What Jev is (TypeSafe docs, read 2026-11-17):

- TypeSafe Jev 1.14 (`jev-1.14.0`, alias `jev-latest`), a "System One" model: it answers typed questions about supplied state. Question types: Choice (pick one option), Score (position on described levels), Noul (probability that a statement is true), Box (image location). Endpoint `POST https://api.typesafe.ai/v1/systemone`.
- Price: $0.042 per million input tokens; output is free. A call of about 1,000 tokens costs roughly $0.00004. Context: 64k per request and 32k per question. Questions in one request run in parallel and share the state, so many questions per request is the intended pattern (the parallel-questions cookbook reports 13 batched questions as 12.2x cheaper and 11.8x faster than 13 separate calls, with answers unchanged).
- Design guidance from TypeSafe: Jev makes the judgments, code makes the decisions. Ask one concrete judgment per question; pair a Choice with a companion Noul that asks whether any option fits; start Noul thresholds at 0.7 (yes) and 0.3 (no) with the band between as "not settled"; do not gate on `confidence`; keep all question wording in one module; when a call fails, surface an error, never treat it as "no".
- The function-calling cookbook (https://docs.typesafe.ai/cookbooks/function_calling.md) is the closest pattern: a per-function spec file holds one question per argument, one line per option, an optional "was this stated at all?" Noul, and a Choice that picks the function; arguments that are not closed sets (numbers, free text) get no question and keep their defaults.
- Data handling: Jev is not trained on customer requests; zero data retention is an enterprise option. The prompt text is sent to TypeSafe. IronClaude is a public repository and the owner lifted the earlier data-sharing hold on 2026-11-16; private repositories and the open data-sharing question OD3 in #552 are NOT covered.
- Jev latency per call and accuracy on flag-choice questions are UNVERIFIED: no absolute latency figure was found in the docs read, and no live call was made.

Where a preflight could run (verified in docs and code):

- Claude Code hooks: `UserPromptSubmit` and `UserPromptExpansion` can block a prompt or add `additionalContext`; they cannot rewrite the prompt or the command arguments (hooks reference, https://code.claude.com/docs/en/hooks). So a hook can inject "preflight says type=performance (p=0.93)" as context but cannot turn the typed command into the full syntax.
- LiteLLM gateway: `async_pre_call_hook` can modify the request before it is sent to the model (https://docs.litellm.ai/docs/proxy/call_hooks). But Claude Code expands `/sc:...` itself, so the gateway only sees the expanded command text with an "ARGUMENTS:" line, not what the user typed. A gateway rewrite would have to pattern-match that text, would fire on every request of the tool loop, would apply only to gateway sessions, and the user could not see what was rewritten. ccsession already routes through a LiteLLM `/cli` passthrough with a local alias proxy (`src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py`).
- Standalone component (recommended): a small command (for example `superclaude preflight troubleshoot "<prompt>"`) that returns JSON with each flag, its probability and whether it abstained. The command's Wave 0 calls it with Bash; optionally a `UserPromptExpansion` hook injects the same JSON as context.

Rules for the design: the user's explicit flags always win; a Noul probability between 0.3 and 0.7 leaves the flag unset (what the protocol does on ambiguity today); the `SC:TROUBLESHOOT:TARGET` audit header records `type: performance (preflight p=0.93)`; with no `TYPESAFE_API_KEY` or no network it fails open to the keyword table, which stays as the floor; one spec file per command, shared runner.

Recommended steps, in order:

1. Add the missing performance phrases to the keyword table ("too long to load", "takes forever", "hangs"). One edit; sends no data out.
2. Run a one-off comparison: take about 30 past `/sc:troubleshoot` prompts, label their types by hand, and compare Jev's `--type` answers with the keyword table. Needs the owner's yes on sending those prompts to TypeSafe, a budget (under $1 is enough) and use of `TYPESAFE_API_KEY`.
3. Only if Jev clearly beats the table in step 2: build the standalone preflight command for `/sc:troubleshoot`. Do not start with `--depth` or `--scope`, and do not touch the gateway.

Three sub-issues: #610 (step 1, keyword table), #611 (step 2, Jev vs table comparison), #612 (step 3, standalone preflight, blocked by #611 and only if Jev beats the table).

## Acceptance Criteria

- [ ] Step 1: the keyword table in `sc-troubleshoot-protocol` includes "too long to load", "takes forever" and "hangs" under performance, and `/sc:troubleshoot "ccsession is taking too long to load"` auto-detects `--type performance` (sub-issue 1).
- [ ] Step 2: the Jev-vs-keyword-table comparison over about 30 hand-labelled past prompts is run and its accuracy numbers recorded (sub-issue 2).
- [ ] Decision rule applied and recorded: the standalone preflight (sub-issue 3) is built only if Jev clearly beats the keyword table in step 2; otherwise sub-issue 3 is closed as not-justified with the comparison attached.
- [ ] If built, the preflight is standalone and advisory: user-explicit flags always win, Noul probabilities between 0.3 and 0.7 leave the flag unset, the audit header records the preflight choice and probability, and with no `TYPESAFE_API_KEY` or no network it fails open to the keyword table.

## Out of Scope

- Any rewrite of the LiteLLM gateway request path (the gateway option was evaluated and rejected).
- `--depth` and `--scope` inference in the first build; the first preflight targets `--type` only.
- Flags a preflight must never infer: `--fix`, `--unattended`, `--report-dir`, `--output-dir`, `--caller`, `--context`, `--models`, `--no-mcp`, `--no-doc-discovery`, `--no-escalate`.
- Private-repository data: sending private repo prompts to TypeSafe is not covered (the 2026-11-16 hold lift covers this public repository only; open question OD3 in #552 remains open).

## Components Affected (from `/sc:analyze`)

Quick codebase pass on the troubleshoot command, its protocol skill and the ccsession gateway files (codegraph/auggie not used; Grep/Glob/Read only). All paths confirmed to exist in this checkout:

- `src/superclaude/commands/troubleshoot.md` (source copy of the command; installed to `~/.claude/commands/sc/troubleshoot.md`). Flags today: `--type bug|build|performance|deployment|security|test`, `--depth quick|standard|deep`, `--scope`, `--no-escalate`, `--fix`, `--models`, `--output-dir`, `--no-doc-discovery`, `--no-mcp`, `--context`, `--caller`, `--unattended`, `--report-dir`.
- `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (Wave 0 auto-detect at lines 145-183; keyword table at lines 152-159; Tier 2 agent table at lines 380-389).
- `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` (security gate 0.95 vs default 0.85).
- `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py` (existing LiteLLM `/cli` passthrough with a local alias proxy; relevant only to the rejected gateway option).
- A future `superclaude preflight` CLI entry under `src/superclaude/cli/` plus one spec file per command (new; does not exist yet).

## Related Issues/PRs

- #463: closed Jev/decision-model router research; nearest earlier ask in spirit.
- #553: install the TypeSafe Jev plugin by default (open); same Jev integration family.
- #574: fast-jev compaction, first local Jev evaluation (closed; live runs limited to public fixtures, $50 budget, key never printed or stored).
- #575: jev-pruner, second local Jev evaluation (closed; same limits as #574).
- #576: local inference node for Jev on RTX 3090/4090 (closed); alternative to the hosted API, not needed for step 2.
- #552: classification-blocker issue whose open data-sharing question OD3 is not covered by this issue.
- Sub-issues: #610 (step 1 keyword table), #611 (step 2 Jev vs table comparison), #612 (step 3 standalone preflight, blocked by #611 and only if Jev beats the table).

Sources:

- https://docs.typesafe.ai/go/models.md
- https://docs.typesafe.ai/go/primitives.md
- https://docs.typesafe.ai/patterns/intent-routing.md
- https://docs.typesafe.ai/patterns/companion-noul.md
- https://docs.typesafe.ai/cookbooks/function_calling.md
- https://docs.typesafe.ai/cookbooks/parallel_questions.md
- https://code.claude.com/docs/en/hooks
- https://docs.litellm.ai/docs/proxy/call_hooks

<!-- sc:issue:create template=issue-feature-simple -->
