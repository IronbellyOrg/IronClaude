# Managed workspace (workflow task packages)

Loaded **only** when Wave 0 detects a managed plan. Everything here is additive: legacy sources (specs, notes, prompts, `workflow-plan/1.1` plans) keep the path-hashed ledger and every rule in SKILL.md unchanged. The closed per-task verdict grammar and `refs/qa.md` apply as-is.

## Detection (before Wave 0 step 3 slug resolution)

A source file `P` is **managed** iff `P` has front matter `schema: workflow-plan/1.2`. Then **all** must hold, else STOP `E-MANAGED-INVALID` (no ledger, no writes):

1. `slug` matches `^TASK-WF-[a-z][A-Za-z0-9]{0,15}-[0-9]{8}-[0-9]{6}(-[2-9])?$` (subject: lower camelCase, max 16, no hyphens), equals the name of `P`'s parent directory, **and `P`'s basename is exactly `<slug>.md`** (a managed plan named `plan.md` or any other name → `E-MANAGED-INVALID`; never fall back to `plan.md`). Below, `<plan>` means `<slug>.md`.
2. Sibling `return-contract.yaml` has `contract_version: "1.1"`, the same `slug`, and `status: success` or `partial` (a `failed` contract is never executable).
3. `P` resolves (realpath, no symlinked component below the checkout) to `<checkout>/.dev/tasks/to-do/<slug>/<slug>.md` or `<checkout>/.dev/tasks/done/<slug>/<slug>.md`, where `<checkout>` is the current git top-level. A copied plan or a plan from another checkout fails here.
4. Sibling `source.md` exists as a regular file.

Any other schema → legacy path. Do not "upgrade" or rewrite a plan.

## Location resolution (first, before ledger dispatch)

`<pkg>` = `.dev/tasks/to-do/<slug>`, `<done>` = `.dev/tasks/done/<slug>`. Use `test -e || test -L` so dangling symlinks count.

This runs **before** the missing-file check on the invoked path (SKILL.md "Managed path-shape pre-check"): an invocation naming `to-do/<slug>/<slug>.md` after the package was archived has no file at that path, yet resolves here by its immutable slug. Neither location exists → `E-SOURCE-MISSING`.

| State | Action |
|-------|--------|
| both exist | STOP `E-MANAGED-CONFLICT`. Never merge, move, or delete |
| only `<done>` exists (invoked by either path) | run the helper (below) in archive mode: it validates the archived identity and answers `already-archived` with the actual path → print `already archived: <actual done path>`; run no tasks. Helper error → STOP with its code |
| `<pkg>/.archiving` exists | STOP `E-ARCHIVE-MARKER`: never reclaim, never infer the owner is dead (see Recovery) |
| only `<pkg>` exists | continue |

## Ledger, artifacts, pins

- Ledger is always `<pkg>/progress.md`. Any `--ledger` naming another path → STOP `E-LEDGER-PATH`. Header source token is `./<slug>.md`.
- Q0 git pins use the stable id: `refs/superclaude/implement/<slug>/T<id>`. No lookup hashes a plan path (the package moves).
- Task-owned evidence and delegate output live under `<pkg>/artifacts/` and are cited as `./artifacts/<file>:<line>` in `evidence=`. Delivery paths in `files=` and `evidence=` are repo-relative and canonical.
- Optional delegates (e.g. `sc:adversarial`, `sc:reflect`) get an explicit root below `<pkg>/artifacts/<name>/`; consume only returned paths whose realpath is inside `<pkg>/artifacts/`, else treat them as missing. `sc:adversarial` writes its own `<root>/adversarial/` child (use its returned `artifacts_dir`). Invoke `sc:reflect` only with `--no-promote`: `/sc:implement` is the sole mover. Give `sc:reflect` a fresh dedicated per-run `--output` directory, e.g. `<pkg>/artifacts/reflect/<mode>-<runid>/`: never `<pkg>`, `<pkg>/artifacts`, or a directory holding a report you pass as input (a prior run's folder). Reflect's own input-snapshot exclusion and overlap guard (sc-reflect-protocol `SKILL.md` §4.0 Step 0.4 `REFLECT_OUTPUT_ROOT`) govern; do not restate or reimplement them here. No mandatory heavy review.
- Run task checks so they leave no stray byproducts (e.g. `PYTHONDONTWRITEBYTECODE=1`); remove caches/temp files a check created before Q2, because Q0 snapshots sweep all non-ignored untracked files.
- At ledger creation append, right after the header:

```
PLAN: sha256=<planhash> source_sha256=<sourcehash>
```

  hashes are lowercase hex SHA-256 of the bytes of `<slug>.md` and `source.md`. Every invocation recomputes them. **Before the first `T<id>: start` line** a differing hash is re-pinned by appending a new `PLAN:` line (append-only; never edit). The first `T<id>: start` line is the immutability boundary: afterwards any plan/source hash differing from the latest `PLAN:` line → STOP `E-PLAN-CHANGED`; no repair, no new pin.

## Completion: fresh FINAL, then archive

Dispatch (replaces the legacy "already complete" stop for managed packages): when every task is `complete` and the package is still in `to-do/`, you are **active all-complete** → run the archive gate below. Report `archive-blocked: <reason>` if it cannot finish. Never print `already complete` for an unarchived package.

Archive gate, **every attempt** (N=1, resume, retry; an earlier FINAL never counts):

1. Join every delegated writer / background task. Nothing may still be writing the package or delivery files.
2. `--skip-final-review` → no FINAL and no archive: STOP `E-ARCHIVE-BLOCKED` (`--skip-final-review` prevents archiving a managed package).
3. State: `uv run --no-project python "<skill base>/scripts/archive_workspace.py" --root "<checkout>" --package "<checkout>/.dev/tasks/to-do/<slug>" --print-state` → JSON `{"status": "state", "state": "<sha256>", "files": [...]}` (the plan/source/delivery-file digest; `files` = every repo-relative path named in a ledger `files=` field, so list every delivery file there). Failure → STOP `E-ARCHIVE-BLOCKED` with the helper's code.
4. One independent reviewer (always a Task subagent, even N=1; `refs/qa.md` isolation rules) gets the current full plan, the full ledger, and the current contents of each listed delivery file. Pass absolute paths or inline contents; the reviewer must read the real current files. It verifies every task's AC against the real files and returns `pass` or `issues` with `path:line` evidence. Missing or unverifiable evidence → `issues`.
5. Re-run step 3. If `state` changed during the review, discard the result and repeat from step 1. Otherwise append (after all task lines and the latest `PLAN:` pin):

```
FINAL: <pass|issues> evidence=<ev-list> state=<sha256>
```

6. `pass` → run the helper in archive mode (no extra flag). It appends its own `ARCHIVE: start id=<id> token=<hex>` line after FINAL and moves the package; there is no later "complete" record (location is the archive state). `issues` → STOP `E-ARCHIVE-BLOCKED`; the package stays in `to-do/`; do not reopen completed tasks unless the operator says.

`<skill base>` is the base directory the loaded skill announces (the directory holding this skill's `SKILL.md`); never hardcode a repository `src/` path. A FINAL pass is not a commit, PR, merge, release or human approval.

### Operator archive Ruling

Tasks completed through an operator task Ruling need, before archiving, an operator-written line:

```
ARCHIVE: Ruling: <what, naming each waived task id e.g. T2,T3> — <why> — <cost-if-wrong>
```

The executor MUST NOT write it, and it never waives FINAL or evidence of current outcomes. The helper checks every non-compliant task is named. Any later ledger record makes a FINAL stale, so the Ruling must already be on the ledger before the fresh FINAL of the attempt it covers.

### Helper, sole movement path

The helper is the **only** way a package moves. Never `mv`, `cp`, `rename`, or `mkdir` a destination. It uses Linux `renameat2(RENAME_NOREPLACE)`; unsupported platform/libc/filesystem, EINVAL, ENOSYS, EXDEV and any existing destination fail closed with the package untouched. It prints `{"status":"archived","path":"<actual done path>"}` — report that path. Non-zero exit: print stderr, the package stays in `to-do/`, no retry loops; the next attempt starts again at step 1.

### Recovery (explicit, never automatic)

An existing `.archiving` marker always stops. If a run was killed mid-archive the marker (and the evidence in `progress.md`) stays. Only after the operator confirms the original run has stopped: read the token in `<package>/.archiving/owner`, then run the helper with `--root <checkout root> --package <that package path> --clear-marker <token>` (`--root` defaults to the current directory). The helper never moves anything in that mode, and an empty token is rejected (never treated as archive mode). Owner-less marker: if `<package>/.archiving` is an empty directory with no `owner` file (a crash between creating the marker and writing its token), the helper cannot clear it. Only after the operator confirms the original run has stopped, remove exactly that directory with the non-recursive `rmdir <package>/.archiving` (it fails if anything is inside; never `rm -r`), then retry. Never do this to a marker that has an `owner` file or content. Ledger `ARCHIVE:` lines are never proof the owner is dead.

## Enforcement map

| Rule | Enforced by |
|------|-------------|
| detection, location resolution, ledger path, pin/re-pin, delegate roots, joins, `--no-promote`, fresh reviewer, "active all-complete" dispatch | **protocol** (this Markdown; static tests only prove the wording) |
| real direct package under to-do/done, no symlink escape, schema/slug/contract, pins vs disk, every task complete (Ruling + named archive Ruling), FINAL pass last and bound to the current state digest, no existing marker, no-replace move, recovery token | **executable** (`scripts/archive_workspace.py`, tested in `tests/skills/test_workflow_archive.py`) |
| concurrent writers on one package, non-cooperating checkout writers | unsupported; not claimed |
| delivery files missing from every ledger `files=` field, and `./artifacts/*` content | not covered by the state digest; only the FINAL reviewer (protocol) can notice stale evidence |
