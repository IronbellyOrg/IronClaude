# Q-1 result (plan Task 16)

**Q-1: FAIL (consumer_fenced)**

Date: 2026-11-11 (22:3x UTC). Run read: probe Run A, `run_c1badaa6576b`, created by the gate research worker as a throwaway.

## What was run

A plain Orca terminal spawned by the owner for this test: it has a terminal handle (`ORCA_TERMINAL_HANDLE` is set) and holds no Run. From that terminal, once:

```
orca orchestration check --all --types question --run run_c1badaa6576b --json
```

(`orca`, not `orca-ide`: inside an Orca terminal `orca` is the Orca CLI.) No `--peek`, plain `check`, `--ack`, `run-use` or send was run against Run A. The other commands of this task ran only against the Run the executor created itself (see `t17-sample.md`).

## Observed (redacted shape)

Exit status 1; stdout one JSON envelope: `{"ok": false, "error": {"code": "consumer_fenced", "message": "This caller is not bound to Run run_c1badaa6576b, which is bound to <a terminal handle, redacted>. Nothing changed."}}`. No `result`, no rows.

## Meaning

- An observer terminal that has a handle but holds no Run cannot read a Run that is bound to another terminal. It is fenced, the same code the gate research saw for a caller bound to a different Run. So an observer must run in the terminal that holds the Run, or hold a Run of its own; there is no read-by-name from an unbound terminal. This is one case, one Run: Orca may behave differently for a Run that is bound to no terminal (not tested).
- Whether `check --all` ever consumes when the reader is not the owner: **not observed.** The only non-owner read was refused before any row was returned, and Orca's own message says "Nothing changed". The second step of the plan (read Run A once from the owning terminal and compare ids and count before and after) was not done: the owning terminal belongs to the research session and was not touched. This question stays UNVERIFIED, now narrowed: a non-owner read returns nothing at all.

## Commands run in this task (all of them)

1. `check --all --types question --run run_c1badaa6576b --json` from the plain terminal (above).
