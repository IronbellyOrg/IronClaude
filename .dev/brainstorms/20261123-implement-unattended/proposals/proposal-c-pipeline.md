# Proposal C: coordinator and pipeline integration for `/sc:implement --unattended`

Read: seed-brief, IRONCLAUDE-SIDE (G1, B4, O3, O5, 10.2), installed WORKER-CONTRACT sections 4 and 5, implement.md, the skill, refs, installed launch-level-guard.sh. NOT read (UNVERIFIED): HOW-WE-WORK.md, user-guide docs, `launch.py`, `brief.py`. NEW = my proposal.

## 1. Command line

```text
Command: /sc:implement <abs plan path> --unattended --report-dir <D>/pre-1 --plan-only          (NEW)
Command: /sc:implement <abs plan path> --unattended --report-dir <D>/impl-1 [--approve-plan <sha256>]  (NEW token)
```

`--report-dir` holds only `return-contract.yaml` (WC-4); the ledger stays where the protocol puts it. The brief never passes `--ledger`, `--skip-final-review` (blocks archiving) or `--force`; `--resume` stays implicit. A resume is a new Task (WC-6) with a fresh report dir, the same plan path and the same token.

## 2. Plan approval (O3), both answers

Token = SHA-256 of the plan file bytes: for a managed plan the `PLAN: sha256=` value the protocol already computes; legacy file the same; a prompt hashes `source.md`. I do not reuse `issue-pipeline plan-hash` (same algorithm: UNVERIFIED).

- `--plan-only`: runs Wave 0 and every STOP that can fire before an edit (E-NO-AC for all tasks, E-MANAGED-REVIEW-FAIL, path and ledger checks). No ledger, no `start` line, no product write. Contract `succeeded` with `plan_sha256`, `tasks_total`, or the STOP. The owner approves a plan known to be runnable, and the hash comes from the executor.
- `--approve-plan`: before the first `start` line a mismatch gives `blocked`, reason `E-PLAN-NOT-APPROVED` (NEW), no edits. After the first `start`, `E-PLAN-CHANGED` guards the pin; the token is a no-op.
- **O3 = yes:** `--plan-only`, the owner sees path, task count and hash, approves in chat, the coordinator records it in run notes and creates the Task with the token. **O3 = no:** one Task, no token, brief line `Plan approval: not required (policy O3)`. One code path serves both; an absent token is legal, so the O3 = yes duty sits in the coordinator text (section 5).

## 3. Contract and next step

Worker keys per WC-4; `report_path` is the ledger; `reason` carries the STOP code; `blocked_question` carries the halt text and asks no one. Implement keys under `implement:` (NEW; how other commands carry extras is UNVERIFIED): `ledger_path`, `plan_path` (the `done/` path after archive), `plan_sha256`, `tasks_total`, `tasks_complete`, `halted_task`, `halt_reason`, `final` (pass, issues, not-run), `archive` (archived, already-archived, blocked, n/a), `followups` (notes paths, minor count, safety-scan result), `mode`.

| Status | Cases | Coordinator next step |
|---|---|---|
| succeeded | all tasks complete; managed archived or already-archived; legacy FINAL pass or N=1 | Check the ledger agrees (last line parses, counts match); stage `.dev/tasks`; commit under the owner's instruction; next story |
| partial | E-ARCHIVE-BLOCKED; legacy FINAL issues | Read report, record usability; freeze (section 5) |
| blocked | E-HALT-QA (any halt reason; resume rows P and H never run an operator review, they block with `halt_reason: operator-review`), E-NO-RULING | Freeze; show the person the halt text; Ruling in chat; resume by the D2 check |
| blocked | E-PLAN-NOT-APPROVED | Not a freeze (no task record). Get approval, new Task with token |
| blocked | E-MANAGED-REVIEW-FAIL, E-PLAN-CHANGED | Freeze; plan fixed by a workflow Task; person decides |
| failed | E-RESUME-NEEDED | One re-run as a new Task, same worktree, only if no freeze; a second escalates |
| failed | other STOPs (E-NO-SOURCE, -SOURCE-MISSING, -NO-TASKS, -NO-AC, -LEGACY, -LEDGER-*, -MANAGED-INVALID, -MANAGED-CONFLICT, -ARCHIVE-MARKER) | Freeze; brief or plan defect; person |

## 4. Launch levels, LL-IMPL, ship gate

The guard governs only sessions with a record in its store (installed script); launched issue agents have one, so a coordinator-started worker is probably ungoverned (UNVERIFIED that `worker-start` writes none). The mode changes nothing in the guard.

- **none** (Mode C, level-none claim): the only path.
- **worktree:** a Skill start of implement stays denied until a person types `/sc:implement` as the first prompt line; a brief is not a typed prompt. LL-IMPL text stays. No bypass.
- **full, full submit:** the guard allows implement, but `GOVERNED_LEVELS_ALLOWED = False` blocks every governed launch. Launch prompts do not gain `--unattended`; that is a later owner decision. A full-submit push goes through `/sc:pr-submit`, never implement (WC-9).
- **Issue pipeline (B8, later):** one closed `brief.py` row (plan path from the claim folder, `--unattended`, `--report-dir`, token from the `--plan-only` contract). Needs O3 and an open ship gate; this mode does not depend on it.

## 5. File changes

- **WORKER-CONTRACT section 5:** a P4 sentence (implement accepts `--unattended` under the two-copy test; joins the default set after a live check; until then only when the owner's instruction names it, question 2); one table row: `/sc:implement | <abs plan path>; --report-dir <dir>; --plan-only first when O3 = yes, then --approve-plan <sha256>; never --ledger, --skip-final-review, --force`; update the "13 rows" and "10 commands" counts; one flag-effect bullet (no commit, push or staging; a halt is never asked).
- **Section 4, "After an `/sc:implement` stop":** freeze also on `partial` with a STOP code; exempt E-PLAN-NOT-APPROVED; the resume Task keeps every token of the original `Command:` line; checks 2 and 6 read `ledger_path` and `halted_task` from the contract. "Reading a result" gains: the contract is a claim, the ledger is the proof.
- **HOW-WE-WORK and docs (UNVERIFIED):** drop "no `--unattended` exists" for implement (IRONCLAUDE-SIDE 10.2 says it); one user-guide sentence. Edit `src/` implement.md (`## Unattended mode`, argument-hint) and skill, then `make sync-dev` and the plugins mirror; flip the three `deferred:P4` lines in `tests/skills/test_worker_contract.py`.

## 6. Open questions for the owner

1. O3 yes or no? Both work; I recommend yes for medium and complex stories.
2. Does O5 count as the instruction naming `/sc:implement` for the brief?
3. Force sequential tasks under `--unattended` (batches get no retry ladder)? I say yes.
4. Ship `--plan-only` in the first release, or only the token?
5. Legacy FINAL `issues`: `partial` (my choice) or `succeeded` with `final: issues`?
6. One automatic E-RESUME-NEEDED re-run, or none?
