# D-0099 — Design rationale notes

**Deliverable ID:** D-0099
**Task ID:** T05.21 (Phase 5)
**Date:** 2026-05-20

## Why E15 is the timeout twin of E13

The hook lifecycle (E3-E15) is divided into three regions: happy-path
event-fire (E3-E11), deployment idempotency (E12), and error-path
fail-open (E13, E15). E13 and E15 form a matched pair — both pin the
fail-open contract, but discriminated by the failure mode:

| Eval | Failure trigger | Fixture script (deferred) | Ledger discriminator | Unique expects |
|---|---|---|---|---|
| E13 | hook exits non-zero with stderr | `tests/fixtures/hooks/failing-post-read.sh` | `"type":"hook_error"` | `stderr.contains("failing-post-read.sh")` |
| E15 | hook sleeps past `timeout:` field | `tests/fixtures/hooks/slow-post-read.sh` | `"type":"hook_timeout"` | (strict) `duration.less_than(hook_timeout + 2.0)` |

The two evals share three of four scaffolding gaps (fixture script,
hooks.json-variant deployment, structured ledger emission). The fourth
gap is unique per eval: E13 needs no additional primitive (stderr is
already a first-class Expect.* primitive), while E15 needs the
Expect.duration primitive that doesn't exist today.

## Scaffolding-gap inheritance vs T05.07..T05.20

This is the **final** post-OQ-2 body to land. The inheritance stack from
T05.07 (D-0087) through T05.20 (D-0098) has built up the following
consolidated follow-up roster, ordered by how many evals each gap blocks:

| Scaffolding gap | Blocks evals | First identified | Follow-up class |
|---|---|---|---|
| Hook scripts don't emit `{"type":"session_init"}` rows to `logs/session-events.jsonl` | E3 (T05.07), E14 (T05.20) | T05.07 | hook-script wiring |
| `logs/freshness.jsonl` per-matcher row emission | E4-E11 | T05.08..T05.16 | hook-script wiring |
| `hooks.json` variant deployment path (`isolation.hooks_variant:` field) | **E13 (T05.19), E15 (T05.21)** | T05.19 | schema bump + setup-wrapper |
| Structured `logs/hook-errors.jsonl` emission | **E13 (T05.19), E15 (T05.21)** | T05.19 | harness extension |
| YAML `callback:` schema field + loader + runner wiring | E14 (T05.20) | T05.20 | schema bump + loader + runner |
| `tests/fixtures/hooks/failing-post-read.sh` fixture | E13 (T05.19) | T05.19 | fixture creation |
| `tests/fixtures/hooks/slow-post-read.sh` fixture | E15 (T05.21) | T05.21 | fixture creation |
| Expect.duration primitive | **E15 (T05.21) only** | T05.21 | Expect.* extension |

T05.21 inherits **4 scaffolding gaps** (3 shared with E13 + 1 unique
duration primitive). This is one less than T05.20 (5 gaps) because T05.21
reuses E13's hooks.json-variant + ledger-emission tracks rather than
introducing a fresh dependency (E14's callback-escape-hatch was novel).

## Why a body-verbatim proxy posture (not a downsized body)

The OQ-2 contract is a stable target for the post-Phase-5 harness work
to converge on. Landing a downsized body (e.g. omitting the
`type:"hook_timeout"` discriminator row to "make the proxy pass today")
would (a) make the body diverge from the OQ-2 contract, requiring an
edit when the harness scaffolding lands, and (b) lose the auditability
of the deferral — a future contributor reading `real.yaml` would not
see what the strict form requires.

The body-verbatim + proxy-substring posture solves both: the body
mirrors the OQ-2 expects shape one-for-one (4 rows, conjunctive
substring filter over the same JSONL file), and the strict form lands
when the scaffolding closes — no body edit needed, only Expect.duration
addition for the orthogonal wall-clock axis.

## Why two-substring conjunction over the same file

The OQ-2 contract names `jsonl.contains_event(..., type=hook_timeout,
disposition=fail_open)` as a single keyword-arg-filtered predicate.
Declarative YAML cannot express keyword-arg predicates against
Expect.jsonl (which routes to a Python callable per `expect.py:269-369`
for predicate dispatch). The Expect.file primitive's `contains:` field
takes a single substring per row.

The proxy decomposes the conjunction into two rows: one substring per
discriminator, both against the same `logs/hook-errors.jsonl` file.
This mirrors the E13 (T05.19) precedent and the E6/E7/E8 sibling pattern
(two-substring `{type, matcher}` conjunction). The limitation: the two
substrings need not appear on the SAME row of the JSONL file — a
pathological harness that emitted them on different rows would still
pass the proxy. This is captured in spec.md §8.2 ("concurrent hook
timeouts garble ledger rows").

## Why /quit is the third input

`exit_code.equals: 0` pins the PTY teardown contract, NOT the
timeout-reap status of the slow hook. This decouples two assertions
that the fail-open contract makes orthogonal: the hook timeouts, the
harness reaps + logs, the tool call completes, and the session exits
0 on `/quit` regardless. A naive harness that propagated the hook
timeout to the session exit code would surface as `exit_code` ≠ 0,
which would FAIL this expect — so `/quit` provides a discriminator
between fail-open (exit 0) and fail-closed (non-zero exit propagated).

## Why no `expect_tool_call` on inputs[2]

The `/quit` input is a session-control command, not a Read/Write/Edit
tool invocation; it doesn't fire a tool-call hook. The
`expect_tool_call: Read` annotation on inputs[1] pins the Read tool as
the trigger for the slow PostToolUse hook (the OQ-2 contract names
"inject prompt triggering a Read"). Matches the E13/T05.19 pattern
exactly.

## Final-body retrospective

T05.21 is the seventeenth and last evalbody to land under the OQ-2
resolution. The 17-eval roster is now schema-complete: E1, E2.1-2.3,
E3-E15. SC2 (T05.22) will verify manifest schema compliance over the
complete suite; SC1 (T05.23) will roll up the deferral roster into a
follow-up gating list before Phase 5 exit.
