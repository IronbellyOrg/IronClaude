# Research: GF-2 what CHANGELOG.md:170, commands.md:619 and commands.md:620 each say
**Investigation type:** Doc Analyst
**Scope:** research/03-sweep-classifier-joins.md (s8.1 point 3, s8 Takeaways, Gaps item 4); /home/coder/.cache/ic-snap-20261120/master/docs/user-guide/commands.md (600-630); /home/coder/.cache/ic-snap-20261120/master/CHANGELOG.md (160-180)
**Status:** Complete
**Date:** 2026-11-20
---

## 1. What each line says (snapshot origin/master 61ac2c2e6, read in full this pass)

All paths below are under /home/coder/.cache/ic-snap-20261120/master.

| Line | Exact statement | Gives a reason? | Covers |
|---|---|---|---|
| `CHANGELOG.md:170` | "The classes `stalled (proved)` and `fenced` are never observed, and `working` is never produced, because the live `agentWait` names were never captured (design open item 6). Healthy workers read `could not determine`." | Yes: one "because" clause, grammatically spanning all three classes | stalled (proved), fenced, working |
| `docs/user-guide/commands.md:619` | "The classes `stalled (proved)` and `fenced` are never observed in Phase 1, so a zero there means nothing. The counts carry the mark `(not observed in Phase 1)`." | No. States the limit and a reading rule only | stalled (proved), fenced |
| `docs/user-guide/commands.md:620` | "The class `working` is never produced yet, because the live names of Orca's `agentWait` field were never captured. Healthy workers read `could not determine`, and a waiting-on-a-person row from an agent wait cannot match on live data. Rows waiting because of a blocked contract or a frozen plan still work." | Yes, but only for `working` (and the agent-wait waiting row) | working, waiting (a) |

**[CODE-VERIFIED]** by the Read of both ranges (commands.md:600-630, CHANGELOG.md:160-180).

## 2. Which parts are stale, and why

Code facts used (all read this pass):
- Rule 5 exists and is active: `src/superclaude/cli/sweep/classify.py:251-269` (`_rule_working`) returns `C_WORKING` when `liveness_verdict == "live"`, `outcome == "in_progress"`, `agent_wait_present is True` and `agent_wait is None`. Its comment (`:252-256`) says the names were captured from a running worker on 2026-11-16.
- Parser: `probes.py:458-468` (`_agent_wait`) docstring "Captured 2026-11-16 (a running worker): the key is present with value null in both places. A non-null value was never captured".
- Test: `tests/sweep/test_cli_contract.py:1133-1140` `test_a_captured_running_worker_is_reported_as_working` asserts class and rule `working` and `counts["working"] == 1`.
- Design: `docs/designs/orchestrator-mode.md:1003` (open item 6) "Resolved 2026-11-16 for a running worker ... Rule 5 is active. Still UNVERIFIED: what a non-null `agentWait` looks like and means"; `:877` (SP-24) "Rule 5 restored with the captured names on 2026-11-16".

Per line:
- `commands.md:619`: **not stale and gives no reason.** `stalled (proved)` and `fenced` are still never observed on live rows (`models.py:108-109` defaults `worker_done_seen` None and `fenced_evidence` "unreadable"; `classify.py:219-223` `_rule_fenced` needs "present"). It cannot carry the "wrong reason" charge.
- `commands.md:620`: **stale in its first clause only** ("`working` is never produced yet" and "Healthy workers read `could not determine`"): `working` is produced since 2026-11-16 (evidence above). Its "because the live names of Orca's `agentWait` field were never captured" explained `working`, and that explanation is also outdated for the names that Rule 5 uses (captured). The remaining clause "a waiting-on-a-person row from an agent wait cannot match on live data" is **[UNVERIFIED]**, not contradicted: `models.py:98-100` says a non-null `agentWait` was never captured; `models.py:111-112` and `probes.py:481` say `agent_wait_since` is never set. The last sentence (blocked contract or frozen plan still work) matches `classify.py:237-244`.
- `CHANGELOG.md:170`: **stale for `working` and "Healthy workers read could not determine"** (same evidence). For `stalled (proved)` and `fenced` the "never observed" half is still true; the stated reason ("because the live `agentWait` names were never captured (design open item 6)") is the only public wording in these three lines that gives that reason for those two classes, and it is out of line with the SPEC reason (`worker_done_seen` None "because no named live source establishes its absence", SPEC:232 per research file 03 s8.1) and with design open item 6, which is about `agentWait`/`liveness.verdict`/`status` names and is resolved for a running worker (`orchestrator-mode.md:1003`). Docs-internal inconsistency: CHANGELOG:170 cites open item 6 as a current reason while `:1003` marks it resolved.

Key Takeaways
- Only `CHANGELOG.md:170` attaches the agentWait-capture reason to `stalled (proved)` and `fenced`. `commands.md:619` attaches no reason; `commands.md:620` attaches it to `working` only.
- `commands.md:620` first clause and `CHANGELOG.md:170` `working` clause are stale (working produced since 2026-11-16). `commands.md:619` is current.

## 3. Replacement paragraph for synthesis (use verbatim)

> Three public lines describe the sweep's Phase 1 class limits, and they do not say the same thing. `CHANGELOG.md:170` says `stalled (proved)` and `fenced` are never observed and `working` is never produced, "because the live `agentWait` names were never captured (design open item 6)", and that healthy workers read `could not determine`; it is the only one of the three that gives the agentWait capture gap as the reason for `stalled (proved)` and `fenced`. That reason differs from the SPEC's reason (`worker_done_seen` is None on live rows because no named live source establishes its absence, SPEC line 232) and from design open item 6, which `docs/designs/orchestrator-mode.md:1003` marks resolved on 2026-11-16 for a running worker. `docs/user-guide/commands.md:619` says only that `stalled (proved)` and `fenced` are never observed in Phase 1 and that the counts carry the mark `(not observed in Phase 1)`; it gives no reason and is current. `docs/user-guide/commands.md:620` says `working` is never produced yet because the live names of Orca's `agentWait` field were never captured; that applies to `working` only, and it is stale because `working` has been produced since 2026-11-16 (`classify.py:251-269`, pinned by `tests/sweep/test_cli_contract.py:1133-1140`). The same stale `working` claim is in `CHANGELOG.md:170`. What stays unverified in both lines is what a non-null `agentWait` looks like and means; until that is captured, the "waiting on a person from an agent wait" row cannot be shown to match on live data (`models.py:98-100`, `:111-112`, `probes.py:481`).

## Gaps and Questions
- **[UNVERIFIED]** Meaning of a non-null `agentWait` (never captured; `models.py:98-100`).
- Whether CHANGELOG.md:170 gives its reason for all three classes or for `working` only is a grammar question: one "because" after a compound subject. This file reads it as covering all three, as research file 03 did; the QA report (F-2) agrees.
- No remediation task created (read-only brief); the stale lines are flagged for the owner.

## Stale Documentation Found
| Doc | Line | Stale statement | Current code | Marker |
|---|---|---|---|---|
| `CHANGELOG.md` | 170 | `working` never produced; healthy workers read `could not determine` | `classify.py:251-269`; `test_cli_contract.py:1133-1140` | **[STALE DOC]** **[CODE-CONTRADICTED]** |
| `CHANGELOG.md` | 170 | reason for stalled/fenced is the agentWait capture gap (design open item 6) | open item 6 resolved (`orchestrator-mode.md:1003`); SPEC:232 gives a different reason | **[STALE DOC]** (reason) |
| `docs/user-guide/commands.md` | 620 | `working` never produced yet; healthy workers read `could not determine` | same as above | **[STALE DOC]** (first clause only) |
| `docs/user-guide/commands.md` | 619 | none | `models.py:108-109`, `classify.py:219-223` | current |

## Summary
`commands.md:619` gives no reason and is current; `commands.md:620` gives the agentWait reason for `working` only and is stale because `working` is produced since 2026-11-16; `CHANGELOG.md:170` alone gives the agentWait reason for stalled/fenced and is stale for `working`. A verbatim replacement paragraph is in section 3.
