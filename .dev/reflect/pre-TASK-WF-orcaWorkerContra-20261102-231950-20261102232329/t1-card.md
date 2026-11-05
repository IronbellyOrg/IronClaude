# Tier 1 reflection card (UC-1, pre-execution)

Spec: `.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md` (cited `SRC:N`). Tasklist: `.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md` (cited `TL:N`). Coverage matrix: `artifacts/coverage-matrix.yaml` (101 inferred rows, 0 parsed, 25 matched by containment, `coverage_pct_union` 0.2475, `S_dev_density` 0.7525, `coverage_degraded: parsed-sparse`).

## Coverage and acceptance (qa slice)
- Scope decision. The tasklist plans Phase P0 only and defers P1-P4 to their own plans (`TL:19`). The spec states "Each phase is one written plan" (`SRC:238`) and "Later phases do not start until the earlier phase's checks in section 7 pass" (`SRC:216`). Classification: Authorized scope limit, stated in the tasklist's Constraints with the source rule cited; the low union coverage is mostly P1-P4 rows the source itself assigns to later plans.
- P0 gap G1: AC-C5 (`SRC:271-274`) is never run or recorded; `SRC:241` says a phase passes only when every common check passes. In P0 no command file is edited, so the check is vacuous, but the tasklist does not record that.
- P0 gap G2: 7.2 step 5 requires each phase report to name at least one checked run longer than the heartbeat cadence (`SRC:291`); Task 8 (`TL:118-128`) does not require it.
- P0 gap G3: if AC-0.6 finds transcripts do not name tool calls, step 5 uses `--source terminal` instead (`SRC:291`, `SRC:303`); Task 8 does not carry that fallback.
- Ordering: AC-C1 and AC-C2 run only in Task 4 (`TL:77-79`), before Tasks 5-9 add or change files; they are not re-run at the end of the phase.

## Root cause and deviation (analyzer slice)
- Task 7 commits inside an `/sc:implement` task window (`TL:106-116`). The spec's WC-9 notes that a commit inside a task's window disables that task's retry ladder because implement's retry requires HEAD unchanged since the task started (`SRC:77`). The tasklist mitigates by making the commit the task's last action, but a QA retry of Task 7 after the commit would find HEAD moved.
- Task 7 depends on Tasks 4 and 6 but not on Task 3 (`TL:108`), yet its acceptance checks that the installed `~/.claude/WORKER-CONTRACT.md` exists, which needs Task 3's `KNOWN_CORE_FILES` change only for listing, not for copying (`SRC:59`). Dependency is incomplete but behaviour is inferable.
- Task 8 makes the `/sc:implement` executor session the Orca coordinator. D5 requires a session the person opened (`SRC:394`); an implement session the person started qualifies, but the tasklist does not say so explicitly.

## Structure and maintainability (refactorer slice)
- Tasks 1 and 2 restate spec content by label ("WC-2", "section 2.3 in full") rather than enumerating every rule; Task 5's test pins those rules. The containment matcher therefore under-counts coverage of sections 2.1-2.3; by meaning, those rows are covered.
- Task 6 (AC-0.9 audit) asks each git/gh write-verb hit to be classified, including "refused under `--unattended` by the phase that converts its command" (`TL:97`). At P0 nothing is refused yet, so every such hit must sit on the allowlist with a forward reference; the task wording allows that but does not say it.
- Task 3 leaves the plugin-mirror decision to the executor with recorded evidence (`TL:60`); the spec's UNVERIFIED item 8 (`SRC:432`) says the plugin mirror rule must be resolved before editing, which the task does.

## Self-assessed confidence
0.72 (uncalibrated). Main uncertainty: whether the deferral of P1-P4 should count against coverage.
