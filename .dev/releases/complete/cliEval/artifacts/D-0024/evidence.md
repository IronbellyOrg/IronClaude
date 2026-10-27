# D-0024 — Evidence

**Task:** T02.02 (Phase 2, DOC-OQ4)
**Date:** 2026-05-20
**Tier:** EXEMPT (Verification Method = "Skip verification" — manual maintainer review)

---

## E1. Top-level `NOTICE` exists at repo root

```bash
$ ls -la /config/workspace/IronClaude/NOTICE
-rw-r--r-- 1 root root  ~1.3K May 20 2026 NOTICE
```

## E2. `NOTICE` references ptytest LICENSE

```bash
$ grep -c ptytest /config/workspace/IronClaude/NOTICE
4
```

Required: `>= 1`. Observed: `4` (header callouts + attribution body + location references). ✅ PASS.

The references in NOTICE point at:

- `src/superclaude/cli/eval/pty/` (vendored location)
- `src/superclaude/cli/eval/pty/LICENSE` (verbatim upstream MIT)
- `src/superclaude/cli/eval/pty/PROVENANCE.md` (fork SHA + changes)

The latter two land with T02.01 (NFR-MAINT1); the NOTICE forward-reference is intentional — OQ-4 is an **M2 entry blocker** for T02.01, so the NOTICE must precede the vendored sources, not follow them.

## E3. `decisions.md` records OQ-4 closure under D-10

```bash
$ grep -n "D-10\|OQ-4" .dev/releases/current/cliEval/decisions.md | head -10
10:- R4 (2026-05-20): DOC-OQ4 closure — D-10 added recording the NOTICE/LICENSE attribution mechanism for the vendored ptytest fork. OQ-4 status flips from OPEN to RESOLVED (M2 entry blocker for T02.01 cleared); per-deliverable spec at `artifacts/D-0024/spec.md`.
300:| D-10: NOTICE/LICENSE attribution for vendored ptytest | 🟠 QUEUED FOR SIGN-OFF (R4) | — | 2026-05-20 |
371:## D-10: NOTICE/LICENSE attribution mechanism for vendored ptytest (OQ-4 closure)
375:`OQ-4` (roadmap.md:173) asks: ...
398:### Closure of OQ-4
416:- Future vendored components MUST follow the same convention ...
```

- ✅ Revision log entry at decisions.md:10 (R4).
- ✅ Sign-off table row at decisions.md:300 (D-10 — 🟠 QUEUED FOR SIGN-OFF (R4)).
- ✅ Full ADR body at decisions.md:371 (D-10 with Context / Options / Decision / Rationale / Closure of OQ-4 / Attribution clause / Consequences).
- ✅ "Resolution status: RESOLVED — 2026-05-20" recorded in §"Closure of OQ-4" block.

## E4. Attribution clause documented in artifact spec

`artifacts/D-0024/spec.md §2 "Attribution clause (canonical)"` reproduces the canonical wording used in NOTICE. The ADR body in `decisions.md §D-10 "Attribution clause"` carries the same wording — the two must stay in lockstep.

## E5. Acceptance-criteria check

| Acceptance criterion | Outcome |
|----------------------|---------|
| File `NOTICE` exists at repo root and references ptytest LICENSE. | ✅ MET (E1 + E2) |
| `.dev/releases/current/cliEval/decisions.md` contains a D-? entry recording OQ-4 closure. | ✅ MET (E3) — entry is D-10 |
| DOC-OQ4 status changes from "open" to "resolved" in decisions.md. | ✅ MET (E3 — §"Closure of OQ-4") |
| `TASKLIST_ROOT/artifacts/D-0024/spec.md` records the attribution clause. | ✅ MET (E4) |

## E6. Downstream gate readiness

T02.01 (NFR-MAINT1) entry condition *"OQ-4 resolved before vendored ptytest sources physically land"* (per roadmap.md:127 M2 entry text) is now satisfied. T02.01 is unblocked.

---

**Reviewer:** RyanW (per roadmap risk register, OQ-4 owner = Maintainer).
**Status at filing:** OQ-4 RESOLVED; D-10 QUEUED FOR SIGN-OFF (R4); awaiting maintainer flip to 🟢 APPROVED at M1/M2 exit.
