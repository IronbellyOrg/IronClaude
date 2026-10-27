# D-0024 — DOC-OQ4 NOTICE/LICENSE attribution for ptytest

**Task:** T02.02 (Phase 2)
**Roadmap row:** 132 (DOC-OQ4)
**ADR ID:** D-10 (decisions.md)
**Open Question:** OQ-4 — *"Does the repo require a top-level NOTICE file for ptytest attribution?"*
**Tier:** EXEMPT
**Date:** 2026-05-20

---

## 1. Why this deliverable exists

`OQ-4` is the **M2 entry blocker** per debate convergence (roadmap.md:166, roadmap.md:173). The vendored ptytest sources (T02.01 / NFR-MAINT1) cannot physically land under `src/superclaude/cli/eval/pty/` until the top-level NOTICE/LICENSE attribution mechanism is in place. Landing vendored MIT sources without the upstream copyright + permission notice in plain sight would breach the MIT attribution clause.

This deliverable closes OQ-4 by:

1. Creating a top-level `NOTICE` file referencing where the vendored ptytest LICENSE will live.
2. Recording the decision in `decisions.md` as ADR **D-10** with full ADR-lite structure (Context → Options → Decision → Consequences) and queuing it for maintainer sign-off in R4.
3. Documenting the canonical attribution clause so future edits to the NOTICE/ADR pair stay in lockstep.

## 2. Attribution clause (canonical)

The authoritative ptytest attribution text used in `NOTICE` is:

> **ptytest (vendored fork)** — Upstream: `https://github.com/brandon-fryslie/ptytest`; License: MIT; Location: `src/superclaude/cli/eval/pty/`. A fork of `brandon-fryslie/ptytest` is vendored under `src/superclaude/cli/eval/pty/` and used as the PTY/pexpect driver layer for the CLI evaluation harness. The upstream MIT LICENSE is retained verbatim at `src/superclaude/cli/eval/pty/LICENSE`, and `src/superclaude/cli/eval/pty/PROVENANCE.md` records the fork SHA, vendoring date, and the changes made relative to upstream.

`NOTICE` MAY add formatting and surrounding header text around this clause but MUST preserve the upstream URL, the license name (MIT), and the location pointer. Any future change to this clause MUST update both `NOTICE` and the D-10 ADR body (decisions.md §D-10 "Attribution clause").

## 3. Files touched

| Path | Change | Purpose |
|------|--------|---------|
| `NOTICE` | CREATED | Top-level attribution; references `src/superclaude/cli/eval/pty/LICENSE`. |
| `.dev/releases/current/cliEval/decisions.md` | EDITED | R4 revision-log entry; D-10 ADR section added (≈58 lines); Sign-off table row for D-10. |
| `.dev/releases/current/cliEval/artifacts/D-0024/spec.md` | CREATED | This file. |
| `.dev/releases/current/cliEval/artifacts/D-0024/notes.md` | CREATED | Implementation notes. |
| `.dev/releases/current/cliEval/artifacts/D-0024/evidence.md` | CREATED | Verification evidence pointers. |
| `.dev/releases/current/cliEval/evidence/T02.02/` | POPULATED | Evidence directory for the task. |

Files NOT touched in this task (deferred to T02.01 / NFR-MAINT1):

- `src/superclaude/cli/eval/pty/LICENSE` — created with the vendored sources.
- `src/superclaude/cli/eval/pty/PROVENANCE.md` — created with the vendored sources.

The forward references in `NOTICE` are intentional: the vendored path is the agreed location, and T02.01 fills it on entry to M2.

## 4. Acceptance criteria (per phase-2-tasklist.md §T02.02)

| Criterion | Status | Evidence |
|-----------|--------|----------|
| File `NOTICE` exists at repo root and references ptytest LICENSE. | ✅ MET | `NOTICE` created (this commit); contains the canonical attribution clause above pointing at `src/superclaude/cli/eval/pty/LICENSE`. |
| `.dev/releases/current/cliEval/decisions.md` contains a D-? entry recording OQ-4 closure. | ✅ MET | `decisions.md` §D-10 added with full ADR structure; revision log updated (R4); Sign-off table row added (🟠 QUEUED FOR SIGN-OFF (R4)). |
| DOC-OQ4 status changes from "open" to "resolved" in decisions.md. | ✅ MET | `decisions.md` §D-10 "Closure of OQ-4" block: *"Resolution status: RESOLVED — 2026-05-20."* |
| `TASKLIST_ROOT/artifacts/D-0024/spec.md` records the attribution clause. | ✅ MET | This file — §2 contains the canonical clause. |

## 5. Verification (per phase-2-tasklist.md §T02.02 Validation)

- `grep -c ptytest NOTICE` → expected `>= 1`. Logged in `evidence.md`.
- Manual review by maintainer: tier is EXEMPT (Verification Method = "Skip verification"); the verification check above is the maintainer's confirmation hook.

## 6. Dependencies and downstream gates unblocked

- **Depends on:** None.
- **Unblocks:** T02.01 (NFR-MAINT1) — M2 entry per roadmap.md:127 ("Entry: ... OQ-4 resolved (NOTICE/LICENSE attribution complete before vendored ptytest sources physically land)").
- **Inherited by:** T02.03 (AC10 fork SHA pin + drift policy) — the quarterly review must re-verify the attribution clause matches upstream LICENSE text after any resync.

## 7. Out of scope for T02.02

- Vendoring the ptytest sources themselves — that is T02.01.
- Authoring `src/superclaude/cli/eval/pty/LICENSE` or `PROVENANCE.md` — those land with the sources in T02.01.
- Flipping D-10 to 🟢 APPROVED — that is the maintainer sign-off pass at M1/M2 exit (cross-references SC1).
- Resolving any other open question (OQ-1/2/3/5/6/7/8/9/10) — out of scope; D-10 closes OQ-4 only.
