# Wave 1B — Spec→Tasklist Coverage Matrix (UC-1)

Spec: SYNTHESIS §6 (H1–H6) + §7 (M2–M7, L1–L5) + Stage 0–3 roadmap.
Tasklist: TASK-RF-20260603-024610 (69 items, 6 phases). Tag-mention counts from grep; item mapping from build + rf-qa task-integrity report.

| Requirement | Covering items | Tag hits | Coverage |
|---|---|---|---|
| H1 per-path isolation merge | 2.1 (setup_isolation scope + probe re-pin), 2.2 (Path A keep WORK_DIR + add 2), 2.3 (_task_env), 2.4 (Path B full set) | 10 | ✅ |
| H2 corrected Stage-0 gate | 2.8/2.9 (serial smoke), PG0 (concurrent-spawn repro) | 7 | ✅ |
| H3 task_complete ↔ task_rerun_complete | 3.5 (mirror + discriminator) | 7 | ✅ |
| H4 frozen HandoffRecord schema | 3.1 (schema_version=1, TaskResult-derived + 2 deltas), 3.2 round-trip | 8 | ✅ |
| H5 resume predicate+key+CLI | 4.1 (validated-success), 4.2 (skip-before-debit), 4.3 (--resume), 4.4 (resume_command reconcile) | 16 | ✅ |
| H6 shared-state inventory+seam+dep reuse | 5.1 (inventory), 2.5 (_env_capture seam), 5.5 (scheduler reuse walk_dependencies + topo wrapper) | 15 | ✅ |
| M2 _jsonl concurrency (covers Stage0/1 writer) | 5.2 (lock _jsonl) — sequenced before 5.7 parallelism | 10 | ✅ |
| M3 per-task prompt composition | 3.x (build_task_context wiring) | 7 | ✅ |
| M4 --task-parallelism/--handoff/store plumbing | 3.x (--handoff), 5.6 (--task-parallelism), config fields | 12 | ✅ |
| M5 in-flight-sprint migration/back-compat | 4.5 (missing handoff/ degrades), 4.8 (test), 3.x (--handoff=off legacy) | 11 | ✅ |
| M6 heading-regex warn-only global-routing | 3.x (warn-only probe, _TASK_HEADING_RE untouched) | 7 | ✅ |
| M7 versioned/migration-safe schema gate | 3.1/3.2 (schema_version + migration test) | 8 | ✅ |
| L1 T02.06 turn-count reconcile | 2.7 (supersedes T02.06) | 1 (T02.06: 5) | ✅ |
| L2 Stage-4 rollback reword | 6.x (reword + teardown stub) | 6 | ✅ |
| L3 crash-consistency test | 4.7 (handoff-file authoritative) | 9 | ✅ |
| L4 benchmark/DAG-resume/mail-failover tests | 5.8 (race), 5.9 (TOCTOU), 5.10 (wall-clock + DAG/resume gap) | 6 | ✅ (mail-failover deferred w/ Stage 4) |
| L5 docs tasks | 3.x + 5.11 (flag docs) | 8 | ✅ |
| T02.05 isolation API pin stays green | 2.1 (probe re-pin), 2.11/PG0.2/5.12 (probe in test runs) | 0 (by file ref) | ✅ traceability nit (no T02.05 tag) |

**Coverage_pct (requirement axis): 18/18 = 1.00** — every §6/§7 finding + the T02.05 constraint has ≥1 concrete covering item. Reviewer ensemble audits *correctness* of the mapping (does the item implement the finding, not just name it) and *latent* gaps the tag-grep can't see (call-site ripple, sequencing, over-coverage).
