# D-0075 — design notes

## Why `re.search` and not `re.fullmatch`

Hook matchers are written as partial-anchored regexes (e.g.
`mcp__auggie__.*`) — `re.search` matches the documented usage. Forcing
`fullmatch` would either require every matcher to be re-anchored or
break compatibility with the live `settings.json`.

## Why `expect_tool_call` is the registry signal

Two candidates were considered:

1. Reuse `inputs[].expect_tool_call`. This field already exists on
   every eval that asserts an MCP tool invocation. The gate gets the
   coverage signal for free.
2. Introduce a new `provides: [<tool-name>, ...]` field on `EvalSpec`.
   Cleaner separation between "what this eval calls" and "what this
   eval asserts," but a parallel registry that can silently drift.

Choice: option 1 for v1. T05.25 may add option 2 as a complement once a
concrete drift case appears.

## Why an unreadable settings.json passes the gate

A fresh dev host doesn't ship a `settings.json`. Making the gate fail
on that host would block `superclaude eval doctor` for any user who has
not yet installed the SuperClaude hook bundle — not the intent. The
gate degrades to "no matchers → no obligations → pass" in that case.
The doctor still reports `coverage_gate.status = "passed"` in JSON so
the operator can see the matcher set was empty (it isn't a silent
skip).

## Why the artifact JSON includes `settings_source`

When triaging a failed run later, the operator needs to know which
`settings.json` the matchers came from. The artifact pins the absolute
path so a postmortem doesn't need to re-derive it from the failed
command line.

## Why the default filter is a function, not a tuple

Callers that need to extend the v1 scope compose their own predicate
(e.g. `lambda p: default_matcher_filter(p) or "mcp__newfamily__" in p`).
Exposing only the function — not the tuple — keeps the v1 contract
crisp: the module owns the v1 set, callers own anything beyond it.
