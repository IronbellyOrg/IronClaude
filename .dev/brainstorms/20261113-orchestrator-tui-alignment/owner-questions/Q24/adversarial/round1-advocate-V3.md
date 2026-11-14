# Round 1 advocate: Variant 3 (the 409 session runs the live reads)

Persona: analyzer (evidence quality, logical consistency). Depth quick, Round 1 only. No Orca command was run; every live fact below is quoted from a file, and anything not confirmed is marked UNVERIFIED.

## Position summary

The 409 session should run XC-03 (W1), OB-03 (W1, under its own row) and XC-04 (W3), each from a terminal that holds no Run. It is the only candidate with a recorded history of running exactly these kinds of live Orca probes safely, and the spec's own lane plan already assigns XC-03, OB-03 and OB-04 to one session. Variant 3's real weakness is that it has no fallback if the 409 session has ended. The fix is to add Variant 1 as the named fallback at XC-10 item (1), not to replace Variant 3.

## Steelman

**Variant 1 (a new master-based capture session).** At its strongest, V1 removes the one fact nobody can confirm today: whether the 409 session is alive (question.md line 31, UNVERIFIED). It never touches the `issue-409-mvp` worktree, which holds two unpushed commits and records that must survive until OB-01 (merged-requirements.md lines 234, 264). That makes the evidence-loss risk zero by construction. Its unique point U-001 is genuinely valuable and applies to every variant: whether `agent launch` binds a Run is unknown (D-A, merged-requirements.md line 128), so "holds no Run" must be read back with `run-current`, not assumed. A master-based worktree also gives XC-04 a clean provenance: the executable revision is the worktree's HEAD.

**Variant 2 (the owner by hand).** At its strongest, V2 removes delegated live-read authority entirely: a person makes every live Orca call, so no `GRANT(...)` row goes to an agent, and it depends on neither the 409 session nor D-A. It matches ADJ's own runner phrase for the seeded test, "owner or 409 session" (ADJ lines 192, 459, 470). The owner's terminal is also the most likely to be allowed to hold a Run legitimately.

## Strengths claimed

1. **Direct precedent with the same fences.** The observer's release-2 executor has already run the two hardest live steps this question gates. Q-1 (plan Task 16, 2026-11-11) was a refused read from "a plain Orca terminal that has a handle but holds no Run", and Orca replied "Nothing changed" (release-gates.md:43, :46). The Task 17 seeded sample created a throwaway Run "from a plain Orca terminal", seeded 5 questions and 2 status messages, and read twice (release-gates.md:45, :48). OB-03 is the same procedure, and ADJ cites that sample as its "safe precedent" (ADJ line 192; merged-requirements.md line 251). That the release-2 executor *is* the session that owns `issue-409-mvp` is likely but UNVERIFIED in the files I read.
2. **It matches the spec's lane plan; V1 does not.** W1 lane L-live is "session Q24 names; ADJ: the 409 session, from a terminal that holds no Run: XC-03, OB-03 then OB-04" (merged-requirements.md line 861). One runner for XC-03 and OB-03 is the planned shape. V1 splits them: OB-03 goes to "the owner or a session the owner names" (variant-1 line 5), which reopens Q24 for OB-03.
3. **Every source names it.** The spec's recommended answer (merged-requirements.md line 551), ADJ Part 7 (ADJ line 794), and the OB-03 row's runner column, "the `issue-409-mvp` worktree session or the owner" (merged-requirements.md line 251).
4. **Familiarity pays off on XC-03's content.** XC-03 records `projection.attention` values (D-8), checks whether `PER_CALL_TIMEOUT` holds (adapter.py:60-62, "UNVERIFIED until the first permitted live read measures it"), and records the build string (merged-requirements.md line 451). XC-04 compares the observer's `dispatchId` list with the sweep's `row_id` list, minus `orca:`, excluding duplicate-flagged rows (line 452). The session that wrote the observer's parser (observe/parse.py, adapter.py) is the least likely to misread those fields.
5. **Low owner time.** "Owner latency is the real schedule" (merged-requirements.md line 523). V3 asks the owner for permission rows only, not for three live sittings.
6. **It states the sitting split honestly.** XC-04 moved to W3 (merged-requirements.md line 861), so ADJ's "one sitting" no longer holds. V3 says so explicitly (variant-3 line 24).

## Weaknesses identified in other variants

1. **V1's "master code" advantage is smaller than the diff (C-003) suggests.** XC-04 runs only after SWEEP-RUNNABLE, meaning "the CLI on this host has the sweep" (question.md line 20; merged-requirements.md line 452). So every variant runs the host's installed sweep, not worktree code. The sweep also takes `--root` and `--output` (sweep/commands.py:232-241), so the 409 session can point the report at a master checkout and write nothing into `issue-409-mvp`. V1 still has the cleaner provenance record, but this is not a blocker for V3.
2. **V1 inherits the D-A risk it names, plus a cold start.** A newly launched agent's terminal may be bound to a Run (variant-1 line 25). V1 also adds a worktree to create, track and remove (variant-1 lines 9, 13, 23). Its own text admits it "may misread observer output that the 409 session would know" (variant-1 line 24).
3. **V1 leaves OB-03 unresolved.** "Who runs OB-03; this answer only names the owner's default" (variant-1 line 31). OB-06 needs OB-03 (question.md line 22), so V1 either costs owner time or needs a second Q24-style answer.
4. **V2 costs the scarcest resource three times.** Three live sittings by the owner (variant-2 line 22) against "Owner latency is the real schedule" (merged-requirements.md line 523).
5. **V2 raises the risk of the one irreversible mistake.** A hand-typed `check` consumes messages (variant-2 line 23). Agents run argv from fixed templates. The observer's adapter refuses `check`, `run-use`, `run-create`, `send` and others by prefix before any call (adapter.py:34-50). Pasted output also cannot be re-run to check it (variant-2 line 24).
6. **V2 does not escape the binding question.** The owner's own terminal may hold a Run (35 of 53 Runs had consumer_generation 2 or more, ADJ line 459). The `run-current` before-and-after record is needed in every variant.

## Concessions

- **No fallback.** If XC-10 item (1) finds the 409 session gone, V3 as written records Q24's default, and XC-03, XC-04 and OB-03 do not run (variant-3 lines 9, 22; merged-requirements.md line 551). V1 does not have this failure mode. V3 should name V1 as its fallback.
- **The 409 session's terminal may already hold a Run.** The Task 17 sample used `run-create` from the executor's terminal (release-gates.md:45, :48). If that terminal still holds `run_86013b917868`, it fails "holds no Run", and the session must use a fresh plain terminal. UNVERIFIED.
- **Evidence-loss risk (C-004) is real.** Mitigation (read verbs only, `--root` elsewhere, no cleaning) lowers it but does not remove it. V1 and V2 do not have it.
- **One session holds three rows, one of them a write row.** The rows stay separate (merged-requirements.md line 575), but the concentration is real.

## Shared assumption responses (A-001)

**QUALIFY.** The assumption is too broad as the diff states it. Q-1's failure is about `orchestration check` (the mailbox read), not `worker-list`. The fence is "This caller is bound to Run <A>, not Run <B>" with code `consumer_fenced`, recorded for the `check --all --types question --run <id>` template (release-gates.md:40-43), and Q-1 refused "a plain Orca terminal that has a handle but holds no Run" reading another terminal's Run (release-gates.md:43; ADJ line 87).

For `worker-list`, the evidence points the other way:
- The sweep with `--run <id>` never binds. `bind_run` (run-current) is called only when no `--run` is given (sweep/commands.py:264-266; probes.py:365-375). It then calls `worker-list --run <run> --json` (probes.py:1047).
- The observer's template is an unscoped `worker-list --json --limit 100` with optional run pairs (adapter.py:29). A live unscoped read on this host returned `page.total` 513 across Runs (ADJ line 140, E-14; INV-017).

So XC-04's sweep side and observer side, and XC-03's `worker-list`-based attention values, are probably not blocked by Q-1. What stays UNVERIFIED:
- whether the E-14 read came from a terminal that held no Run;
- whether `worker-show` on another terminal's Run is fenced.

The remaining live risk is OB-03, which reads with `check` and only works because it reads the Run that its own terminal just created with `run-create` (merged-requirements.md line 251). XC-03 should record a `worker-list --run <id>` read from the Run-less terminal as its first step, so A-001 is settled before XC-04.

## Per-point verdicts

| Point | Superior | Reason |
|---|---|---|
| S-001 | tie | Same five-section layout in all three. |
| C-001 | V3 | It has run these probes before (release-gates.md:43, :45), the spec's L-live lane names it (line 861), and it costs little owner time. It needs a V1 fallback. |
| C-002 | V3 | It names a concrete OB-03 runner that the spec and ADJ endorse, with the Task 17 precedent. V1 punts to the owner, and V2 spends owner time. |
| C-003 | V1 | A master worktree gives a clean revision record. The gap is narrow, because SWEEP-RUNNABLE means the host CLI and `--root` avoids writes into the 409 worktree. |
| C-004 | tie (V1, V2) | Neither touches `issue-409-mvp`. V3 carries real, though mitigable, evidence-loss risk. |
| C-005 | tie (V1, V3) | Both keep live sittings off the owner. V2 needs three. |
| X-001 | V3 | Agents running fixed, guard-checked templates under per-item GRANT rows have a safe record (Task 16, 17) and avoid hand-typed `check` (adapter.py:34-50). V3 also avoids V1's cold start. |
| X-002 | V3 | XC-03 and XC-04 are about observer fields (attention, `dispatchId` join rules). Familiarity cuts misreads, and the clean-runner risk is mitigable by read-only work plus `--root`. |
| X-003 | tie | All three run two sittings. V3 only states it more plainly. |
| A-001 | tie | All three share it. QUALIFY: Q-1 fences `check`, not `worker-list --run`, but a Run-less `worker-list --run` read is still UNVERIFIED and should be XC-03's first recorded step. |

Overall: V3
