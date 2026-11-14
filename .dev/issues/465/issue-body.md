<!-- /sc:issue bug template (simple). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. -->

## Bug Summary

**Suggested title:** Verifier report delivery failure leaves implementation blocked without bounded recovery

A native Agent qualitative verifier returned its assessment in chat while its required report remained incomplete, then declined to write it; a fresh retry also refused. The implementation task correctly stopped rather than accepting missing evidence, but the observed workflow had no automatic bounded recovery from this delivery incompatibility.

## Environment (OS, version)

- OS: Linux 6.8.0-147-generic, as supplied by the incident environment.
- Version: IronClaude branch `ironbelly/issue-339-orchestrator-mode`, task package `TASK-RF-sweep-phase1-20261108-072653`; exact deployed agent runtime and injected instruction versions are not known yet.

## Current Behavior

### Contract and incident timeline

The original item 6.17 (`.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1095-1100`) requires a native Agent `rf-qa-qualitative` spawn, `mode: bypassPermissions`, `fix_authorization: false`, in parallel with the independent `rf-qa` verifier for 6.16. Its verbatim preamble requires rechecking all BLOCKING/MAJOR findings and every earlier PASS check, a `## Checks` table with each `<report name>:C<n>` and PASS/FAIL, new blocking findings, `Verdict: PASS` or `Verdict: FAIL`, and `Blocking count: <n>`. The output must be `qa/r5/verify-cycle1-rf-qa-qualitative.md` under the task package. It must classify every F0 finding RESOLVED or OPEN with evidence, and the report must be written before completion. Two failed attempts require recording the blocker and stopping.

1. On 2026-11-09 at 00:23:11 UTC the qualitative agent was launched. At 00:36:50 it returned an assessment in its completion notification, including 128 PASS and seven FAIL of 135 earlier PASS predicates, R5-F1 resolved, no new blocking finding, overall `Verdict: PASS`, `Blocking count: 0`.
2. The parent read the requested file and found only 59 displayed lines, ending `(Checks table follows.)`; no Checks table or closing verdict. The independent structural verifier's report was complete (`qa/r5/verify-cycle1-rf-qa.md:49-51,253-263`), but it cannot replace the qualitative review.
3. At 00:37:08 the parent resumed the original agent and asked it to persist the existing results without changing the seven FAILs. At 00:37:23 it refused, saying its session was restricted to returning findings directly. One fresh retry was launched at 00:37:55; it reported a higher-priority prohibition and performed no verification or tool calls. No tool denial proves filesystem or hook enforcement.
4. At 00:38:03 the task execution log recorded delivery failure after the two attempts; frontmatter is Blocked with a delivery-specific `blocker_reason` (`task file:7,63,2802-2806,2874-2878`). At the 00:39:07.270Z main-session stop, 122 of 355 tasks were reported complete. The ledger has T123 start only, while T122 completed (`.dev/implement/task-rf-sweep-phase1-202-c7ea3265/progress.md:244-246`). Item 6.17 is unticked, its independent Q3 compliance review has not happened, and 6.18 has not started. No R5 gate outcome was accepted.
5. At 02:26:57.498Z the owner, Ryan Wiancko, authorized report writing and, if necessary, parent-write fallback. The stop-to-owner-resume interval was **1:47:50.228**, not an observed infinite execution. The owner did not waive failed baseline checks, and a user message cannot override a genuine higher-priority restriction. The parent asked the original agent to write only if its governing instructions permitted, otherwise return the complete body and parent-write instructions.
6. The incident handoff reports a delayed 02:35:22 notification in which the original agent still declined writing and returned the complete report plus parent-write instructions, with zero tool calls and no file changes on that continuation. The bounded main-session extraction for this draft directly confirmed the earlier notification, owner message and resend, but did not independently locate that final notification or the exact retry text in timestamped records; verify these against the original session before treating their timing or content as independently established.

The qualitative result's overall PASS concerns blocking/major findings; it is **not** a pass of the cycle transition. Item 6.18 (`task file:1102-1106`) requires HALT on any earlier-PASS check now FAIL in either verifier, before monotonicity or cap, even if the underlying findings are minor. The seven reported FAILs would require that regression handling once complete evidence is delivered and checked; they were not accepted as on-disk evidence at the stop. Preserve both the verdict and every predicate; do not turn FAILs into PASS or infer an owner waiver.

### Evidence limits and cause

Observed: a partial artifact, chat-only output, explicit refusals, and a blocked task. A plausible instruction/capability mismatch exists: both canonical and installed `rf-qa-qualitative.md` list Write/Edit and require a report and incremental writes, while their `fix_authorization: false` section says not to modify any files (`:822-825`); that text may itself be ambiguous about the report exception. A different higher-priority instruction or injection could also explain refusal. The actual instruction origin, precedence, effective agent session, and enforcement mechanism remain **unverified**. Listing tools or `bypassPermissions` does not establish permission; no claim is made that the owner's message lifted a system/developer instruction.

## Expected Behavior

A reviewer with compatible authority delivers a complete, verifiable artifact, or explicitly reports a bounded, actionable delivery failure. The parent validates artifact contents before independent Q3 and gate progression, preserves failed predicates and provenance, and escalates after a finite number of attempts. A genuinely restricted agent must obey its actual higher-priority instructions; an authorized parent may write only when its own governing permissions permit, without treating a relabeling as a bypass. A valid long-running review must not be declared failed merely for being slow.

## Steps to Reproduce

1. Use a deterministic local test harness with a temporary task package, a small F0 set, prior PASS IDs and a fake native-agent transport; no live Orca, network or private transcript is needed.
2. Simulate a verifier that writes a 59-line-style stub ending `(Checks table follows.)`, then returns a complete in-band result with a mix of PASS and FAIL plus `Verdict: PASS` and zero blocking findings. Deliver a completion notification. Assert the parent reads the file, detects missing required rows/verdict and does not mark the item complete.
3. Simulate the same agent refusing the continuation and a fresh retry returning a higher-priority report-write restriction without tool calls. Assert bounded retry then explicit blocked/escalated state, no independent Q3 falsely recorded and no cycle decision.
4. Simulate authorized parent-side persistence of the exact complete result when independently permitted. Validate all IDs, findings and closing fields; then run a separate Q3 review. Assert the regression gate HALTs for a previously PASS ID now FAIL, despite zero blocking findings. Separately test a real policy prohibiting the parent write: remain blocked, do not rename or bypass.

## Impact Assessment (Severity, Blast Radius)

- Severity: **high** for this workflow: 233 of 355 tasks were still pending when a required independent verification delivery blocked progress; silent acceptance could also defeat a regression gate.
- Blast Radius: native Agent tasks requiring file-based reviews and their parents, any dependent implementation steps and operators awaiting an actionable stop. This incident is not evidence that supervised Orca worker heartbeat or `worker_done` is broken.

### Risks to address

- **Authority versus capability:** Write/Edit availability and permissive tool mode do not override policy. Surface a real incompatibility; never claim user identity or naming a report an input changes an actual higher-priority prohibition.
- **Parent fallback:** only with authority for that parent and path; preserve original bytes and attribution, make clear transport is not independent verification, then obtain separate Q3. Do not silently manufacture or rewrite a verdict.
- **Partial, empty, truncated or stale output:** existence/nonempty and receipt notifications are insufficient. Check expected IDs, duplicates, findings, verdict/count, completeness and current run/cycle; prevent stale data from satisfying the new run.
- **Clobber and concurrency:** preserve partial evidence; prevent overwriting a newer writer or a changed target, constrain paths and symlinks, and use safe atomic publication only when supported. Fail closed on conflict.
- **Notification loss / false completion:** reconcile completion with validated artifact or explicit failure, not delivery receipt alone; distinguish lost notification from a still-running review.
- **Time and cost:** finite escalation deadlines must allow genuinely long work and observable progress; timeout is not proof of failure. Bound retry count and token cost, avoid duplicate live agents and late-result overwrite.
- **Resume and compaction:** recover run identity, prior attempt, artifact and Q0 snapshot from durable records; do not duplicate start, complete or cycle-ledger rows. Handle delayed results and repeated wakeups idempotently.
- **Privacy:** transcripts can contain sensitive material. Use synthetic fixtures, minimal redacted evidence and restricted storage; do not attach raw session logs or private paths to public issues.
- **Gate semantics:** minor-only findings need not fail a review, but a FAIL on an earlier PASS predicate still triggers the task's regression HALT; preserve the distinction.

## Error Messages

```text
I cannot persist the report because this verifier session is restricted to returning findings directly, without writing report files. No further file changes were made.
FAILURE: A higher-priority instruction explicitly prohibits writing or editing report Markdown files.
```

The first quote is in the timestamped 00:37:23 notification. The second is supplied in the incident handoff and is consistent with the task log's summary, but its exact text was not independently recovered in this bounded extraction.

## Codebase Context (from `/sc:analyze`)

Scoped quick static pass over agent definition, implement protocol and incident artifacts; codegraph and auggie tools were unavailable, so Glob, Grep and Read were used. No tests or live agents were run.

- `src/superclaude/agents/rf-qa-qualitative.md:5-9,41-51,822-825,905-920,981-983`: tools, output contract, false-authorization wording, completion readback and incremental-write instruction. Installed `~/.claude/agents/rf-qa-qualitative.md` has the same relevant passages; neither proves the effective runtime instruction stack.
- `src/superclaude/skills/sc-implement-protocol/SKILL.md:105-134` and `refs/qa.md:5-11,95-99`: ledger reread, independent Q3, parent-owned verdict and evidence rules. `refs/ledger.md:29-31,41-60` defines existing start reuse and completion grammar. `refs/retry.md:35-52,69-77` has bounded QA retries, a per-run budget, read-only adviser output saved by parent and validation; these are existing patterns, not proof they automatically govern nested item 6.17's delivery retry.
- Incident helpers `.dev/implement/task-rf-sweep-phase1-202-c7ea3265/mkv.sh:7-10` construct Q3 material from an on-disk report; `mkprompt.sh:8-25` saves review prompts; `done.sh:11-20` appends completion and ticks the task. They are run-specific scripts, not a safe general validator; notably the latter appends before the checkbox update.
- `src/superclaude/skills/sc-issue-protocol/SKILL.md:66-68,155` already specifies exact output paths and one retry for missing/empty files. This is a useful contract example, not a way to evade an actual report-write restriction or a complete semantic validator.
- Existing relevant test surfaces include `tests/skills/test_implement_retry_revert.py`, `test_implement_retry_citation.py`, `test_implement_saved_prompt_rule.py` and `test_implement_severity_replay.py`; inspect their actual coverage before extending or reusing them.

### Ordered refactor handoff

1. Trace the effective native Agent invocation and governing policy chain in a controlled, redacted reproduction. Resolve report-output versus `fix_authorization: false` ambiguity without asserting that capabilities confer authority. Clarify contract on both canonical and installed surfaces through the existing distribution process.
2. At the nested-verifier boundary, reuse existing report and Q3 contracts where appropriate; explicitly define complete, incomplete, policy-blocked, running and delivery-unknown states. Validate the exact F0 set and prior PASS IDs, verdict fields and current run before independent Q3. Investigate existing helpers before adding a new framework.
3. Define a permission-checked parent transport fallback that retains original result, attribution and current cycle identity; use safe no-clobber behavior, separately review the artifact and apply 6.18 unchanged. If transport is incomplete or authority unavailable, block with actionable reason.
4. Add bounded retry/escalation and progress-sensitive waiting for this native-Agent path, integrate with existing ledger/resume and budgets, and test late results and duplicate notifications. Select actual limits based on measured review duration and owner approval; do not treat Orca-specific controls as the proven fix.

## Related Issues

- #431 — quiet supervised workers and weak liveness signals; related symptom, different mechanism, not established duplicate.
- #339 — broader orchestrator work under which the blocked task was being performed.
- #322 — worktree write boundaries are relevant to safe fallback, not evidence of this incident's instruction origin.

## Testing Notes

Acceptance criteria, exercised with deterministic fake transport and temporary files:

- A complete current-run artifact with every expected finding, exactly one row per prior-PASS ID, verdict and blocking count reaches a separate Q3 only after successful validation; missing, empty, stub, duplicate-ID, truncated, wrong-cycle and stale artifacts never do.
- One initial delivery failure plus one fresh retry produces one recorded actionable block/escalation; test silent agent, explicit policy refusal, lost notification and successful but delayed report independently. Repeated polling or resume does not produce unbounded attempts or duplicate records; long-running activity is not a success receipt or automatic stall proof.
- A policy-constrained agent never writes; parent fallback happens only when parent authority and exact destination are allowed, preserves all bytes and origin, refuses symlinks, path escape, concurrent updates and stale overwrite, and preserves partial evidence. Denied parent fallback remains blocked.
- Transport a fixture with 128 PASS and seven FAIL, overall PASS and zero blocking; preserve every FAIL and assert regression HALT before monotonicity. Separately verify minor-only notes with all earlier checks PASS do not cause a new fix cycle. No operator permission to write is interpreted as waiver.
- Restart/compaction after each transition, duplicate notification, concurrent late response and interrupted publication leave one T123 start, at most one legitimate completion and one cycle entry, with the original snapshot reused. Test normal success and explicitly verify a separately attributed Q3 review.
- Keep fixtures synthetic and run offline; inspect existing test helpers before choosing implementation. No tests were run for this draft.

<!-- sc:issue:create template=issue-bug-simple -->
