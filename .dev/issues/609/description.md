# Description given to /sc:issue --create

Command Jev Preflight

Flags given: --mode feature (default depth quick; no --type, so a worker chooses the area).

Extra instruction given by the owner in the same message: create the issue and put all of the context, the asks and as much relevant research as was found into the body of the issue. Then create 2 sub-issues, one for each recommended step, and a 3rd sub-issue that depends on the 2nd and is about showing that Jev beats the keyword table. (The orchestrator creates the three sub-issues after this issue exists; this issue's body lists them under "Related Issues/PRs" once they exist.)

## Context supplied from the session that produced this request (2026-11-17)

Source: an `/sc:analyze` + short `/sc:research` pass on `/sc:troubleshoot`, run in this repository's checkout on 2026-11-17. Nothing below was run against the live Jev API.

### The original ask (owner)

Evaluate the value of having Jev (TypeSafe's System One model) read the prompt that follows `/sc:troubleshoot` and choose the flags and options. Example: `/sc:troubleshoot "ccsession is taking too long to load"` -> a pre-flight stage, before the troubleshoot protocol is invoked, would decide `--type performance` and any other relevant flag. Ideally Jev gets enough context to judge ALL available options, which may need a slightly different preflight per command. Finally, decide whether a Jev preflight should be a standalone component called ahead of time, or run through the LiteLLM gateway before the prompt reaches the model, so that the user types the command and a prompt and the preflight turns it into the full syntax with every option completed.

### What `/sc:troubleshoot` does today (verified by reading the files)

- Command file: `~/.claude/commands/sc/troubleshoot.md` (source copy under `src/superclaude/commands/`). Flags: `--type bug|build|performance|deployment|security|test`, `--depth quick|standard|deep`, `--scope`, `--no-escalate`, `--fix`, `--models`, `--output-dir`, `--no-doc-discovery`, `--no-mcp`, `--context`, `--caller`, `--unattended`, `--report-dir`.
- Protocol skill: `~/.claude/skills/sc-troubleshoot-protocol/SKILL.md`. Wave 0 (lines 145-183) auto-detects `--type` from a keyword table (lines 152-159): stack trace or exception name -> bug; "tsc", "lint", "build", `make`, CI log -> build; "slow", "latency", "p99", "memory", "leak", profiler output -> performance; "production", "deploy", "container", "env var", "service won't start" -> deployment; "auth", "token", "leak", "exposed", "CVE", "vulnerab" -> security; "pytest", "jest", "flake", "intermittent", "passing locally" -> test. On ambiguity the type is left unset.
- The example prompt "ccsession is taking too long to load" matches none of the performance keywords, so today its type stays unset. "leak" is listed under both performance and security.
- What `--type` changes: it picks the Tier 2 specialist agents (SKILL.md lines 380-389, one row per type) and raises the escalation bar for security (`escalation-rubric.md`: `--type security` and confidence below 0.95 escalates; the default gate is 0.85). A wrong type is mostly harmless except for security.
- The model that runs Wave 0 already reads the prompt, so Jev adds no new reasoning there. What it can add: repeatable answers (same prompt, same flags), calibrated probabilities that can be thresholded, an audit trail, and a measurable accuracy number.

### Which flags a preflight may and may not decide

- Safe for Jev: `--type` (one Choice over the 6 types plus a companion Noul asking whether any type fits), `--depth` (a Score, or small Noul questions: intermittent? multi-component? security-sensitive?), `--scope` (code extracts candidate paths and symbols from the prompt; Jev picks among them).
- Never inferred by a preflight: `--fix` (authorizes remediation), `--unattended`, `--report-dir`, `--output-dir`, `--caller`, `--context`, `--models`, `--no-mcp`, `--no-doc-discovery`, `--no-escalate`. They describe the operator's intent or environment, not the symptom.

### What Jev is (TypeSafe docs, read 2026-11-17)

- TypeSafe Jev 1.14 (`jev-1.14.0`, alias `jev-latest`), a "System One" model: it answers typed questions about supplied state. Question types: Choice (pick one option), Score (position on described levels), Noul (probability that a statement is true), Box (image location). Endpoint `POST https://api.typesafe.ai/v1/systemone`.
- Price: $0.042 per million input tokens; output is free. A call of about 1,000 tokens costs roughly $0.00004. Context: 64k per request and 32k per question. Questions in one request run in parallel and share the state, so many questions per request is the intended pattern (the parallel-questions cookbook reports 13 batched questions as 12.2x cheaper and 11.8x faster than 13 separate calls, with answers unchanged).
- Design guidance from TypeSafe: Jev makes the judgments, code makes the decisions. Ask one concrete judgment per question; pair a Choice with a companion Noul that asks whether any option fits; start Noul thresholds at 0.7 (yes) and 0.3 (no) with the band between as "not settled"; do not gate on `confidence`; keep all question wording in one module; when a call fails, surface an error, never treat it as "no".
- The function-calling cookbook (https://docs.typesafe.ai/cookbooks/function_calling.md) is the closest pattern: a per-function spec file holds one question per argument, one line per option, an optional "was this stated at all?" Noul, and a Choice that picks the function; arguments that are not closed sets (numbers, free text) get no question and keep their defaults.
- Data handling: Jev is not trained on customer requests; zero data retention is an enterprise option. The prompt text is sent to TypeSafe. IronClaude is a public repository and the owner lifted the earlier data-sharing hold on 2026-11-16; private repositories and the open data-sharing question OD3 in #552 are NOT covered.
- Related local issues that already use Jev: #574 (fast-jev compaction), #575 (jev-pruner), #553 (install the TypeSafe Jev plugin by default), #576 (local inference node for Jev, RTX 3090/4090). Live Jev runs so far were limited to public fixtures and a $50 budget (one cap for Jev credits and Claude usage); the API key is never printed or stored.
- Jev latency per call and accuracy on flag-choice questions are UNVERIFIED: no absolute latency figure was found in the docs read, and no live call was made.

### Where a preflight could run (verified in docs and code)

- Claude Code hooks: `UserPromptSubmit` and `UserPromptExpansion` can block a prompt or add `additionalContext`; they cannot rewrite the prompt or the command arguments (hooks reference, https://code.claude.com/docs/en/hooks). So a hook can inject "preflight says type=performance (p=0.93)" as context but cannot turn the typed command into the full syntax.
- LiteLLM gateway: `async_pre_call_hook` can modify the request before it is sent to the model (https://docs.litellm.ai/docs/proxy/call_hooks). But Claude Code expands `/sc:...` itself, so the gateway only sees the expanded command text with an "ARGUMENTS:" line, not what the user typed. A gateway rewrite would have to pattern-match that text, would fire on every request of the tool loop, would apply only to gateway sessions, and the user could not see what was rewritten. ccsession already routes through a LiteLLM `/cli` passthrough with a local alias proxy (`src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py`).
- Standalone component: a small command (for example `superclaude preflight troubleshoot "<prompt>"`) that returns JSON with each flag, its probability and whether it abstained. The command's Wave 0 calls it with Bash; optionally a `UserPromptExpansion` hook injects the same JSON as context.

### Recommendation from the session

Standalone, advisory, measured; not the gateway. Rules for the design: the user's explicit flags always win; a Noul probability between 0.3 and 0.7 leaves the flag unset (what the protocol does on ambiguity today); the `SC:TROUBLESHOOT:TARGET` audit header records `type: performance (preflight p=0.93)`; with no `TYPESAFE_API_KEY` or no network it fails open to the keyword table, which stays as the floor; one spec file per command, shared runner.

Recommended steps, in order:
1. Add the missing performance phrases to the keyword table ("too long to load", "takes forever", "hangs"). One edit; sends no data out.
2. Run a one-off comparison: take about 30 past `/sc:troubleshoot` prompts, label their types by hand, and compare Jev's `--type` answers with the keyword table. Needs the owner's yes on sending those prompts to TypeSafe, a budget (under $1 is enough) and use of `TYPESAFE_API_KEY`.
3. Only if Jev clearly beats the table in step 2: build the standalone preflight command for `/sc:troubleshoot`. Do not start with `--depth` or `--scope`, and do not touch the gateway.

Sub-issues requested by the owner: one for step 1, one for step 2, and one for step 3 that is blocked by step 2 and only starts if step 2 shows Jev beating the table.

### Sources

- https://docs.typesafe.ai/go/models.md
- https://docs.typesafe.ai/go/primitives.md
- https://docs.typesafe.ai/patterns/intent-routing.md
- https://docs.typesafe.ai/patterns/companion-noul.md
- https://docs.typesafe.ai/cookbooks/function_calling.md
- https://docs.typesafe.ai/cookbooks/parallel_questions.md
- https://code.claude.com/docs/en/hooks
- https://docs.litellm.ai/docs/proxy/call_hooks
