# D-0117 — Evidence

## Direct verification commands

```bash
# 1) Confirm MIG-003 Closure section header exists in decisions.md
grep -nE '^## MIG-003 Closure' .dev/releases/current/cliEval/decisions.md

# 2) Confirm R13 revision log entry recorded
grep -nE '^- R13 \(2026-05-20\): MIG-003 closure' .dev/releases/current/cliEval/decisions.md

# 3) Confirm MIG-003 status flip to RESOLVED on 2026-05-20
grep -nE 'MIG-003 status flips OPEN → RESOLVED|Resolution status: RESOLVED — 2026-05-20' .dev/releases/current/cliEval/decisions.md | grep -v 'AC2\|AC1\|DOC-OQ9\|DOC-OQ8\|DOC-OQ6\|DOC-OQ4\|DOC-OQ7'

# 4) Confirm v2 follow-up consolidation document exists
test -f docs/eval/v2-followups.md && echo "EXISTS"

# 5) Confirm consolidation document records macOS axis (§2.1) and CI axis (§2.2)
grep -nE '^### 2\.1 macOS support|^### 2\.2 CI integration' docs/eval/v2-followups.md

# 6) Confirm owner = RyanW and target window 2026-Q3 / 2026-07-01 / 2026-09-30 in both axes
grep -cE 'RyanW' docs/eval/v2-followups.md   # >= 2 (one per axis owner row, plus sign-off)
grep -nE '2026-Q3|2026-07-01|2026-09-30' docs/eval/v2-followups.md

# 7) Confirm v1-blocking-work negative check (§6 five rows)
grep -nE '^\| Does this document' docs/eval/v2-followups.md   # exactly 5 rows

# 8) Confirm AC1 / AC2 / DOC-OQ9 cross-references in consolidation document and in §MIG-003 Closure
grep -nE 'AC1.*R-?109|AC1.*Linux-only|DOC-OQ9.*R-?105|AC2.*R-?108' docs/eval/v2-followups.md
grep -nE 'AC1.*R-?109|AC1.*R10|DOC-OQ9.*R6|AC2.*R9' .dev/releases/current/cliEval/decisions.md | grep -A 0 'MIG-003 Closure\|R13'

# 9) Confirm Windows non-goal preservation (design-spec.md:812)
grep -nE 'Windows.*non-goal|design-spec.md:812' docs/eval/v2-followups.md .dev/releases/current/cliEval/decisions.md
```

Expected: each command above returns at least one match (commands 4 and 7 return exact-count matches as noted).

## Per-AC verification

| AC bullet (T06.15) | Verification step | Result |
|--------------------|-------------------|--------|
| A follow-up roadmap entry (in decisions.md or `docs/eval/v2-followups.md`) records macOS + CI as deferred scope. | Confirm `docs/eval/v2-followups.md` §2.1 (macOS) + §2.2 (CI) both record deferred scope tables, and `decisions.md §MIG-003 Closure` Decision summary table cites both upstream closures. | PASS — `docs/eval/v2-followups.md` exists with both §2.1 + §2.2; `decisions.md §MIG-003 Closure` cites R6 (DOC-OQ9) + R9 (AC2). |
| macOS non-goal and CI non-goal are preserved (referenced from AC1 + AC2). | Confirm `v2-followups.md` §1 cross-reference table cites AC1 + AC2 + DOC-OQ9 closures; `decisions.md §MIG-003 Closure` "Cross-references preserved" table cites the same four closures. | PASS — `v2-followups.md` §1 lists all three upstream closures; `§MIG-003 Closure` Cross-references table records the four-way graph. |
| No new v1-blocking work is added (verified by reading the follow-up entry). | Read `v2-followups.md` §6 five-row negative verification: (i) no new code change required for v1 ship, (ii) no v1 ADR re-opened, (iii) no task added to Phase 1-5, (iv) no `roadmap.md` row 360 AC modification, (v) no `--ci` / Darwin / harness change. | PASS — all five rows answer NO; no v1-blocking work added. |
| `TASKLIST_ROOT/artifacts/D-0117/spec.md` records the follow-up summary. | Confirm file exists with §"Follow-up summary" + §"MIG-003 resolution" + §"Cross-reference graph" + §"Acceptance-criteria → site map". | PASS — `artifacts/D-0117/spec.md` written this commit. |

## MIG-003 resolution evidence

`decisions.md` §"MIG-003 Closure" §"Closure of MIG-003":

> - **Question:** How is the deferred scope for macOS support and CI
>   integration consolidated into a v2 follow-up roadmap entry that
>   preserves the v1 non-goals and adds no v1-blocking work?
> - **Resolution:** Consolidated at `docs/eval/v2-followups.md`. The
>   document inherits owner RyanW and target window 2026-Q3 from
>   DOC-OQ9 (R6) + AC2 (R9), preserves the AC1 Linux-only platform
>   commitment (R10), and explicitly verifies (via §6 five-row
>   negative check) that no v1-blocking work is added. Windows
>   remains a non-goal beyond v2. No new code lands.
> - **Resolution status:** RESOLVED — 2026-05-20.

## Cross-reference preservation evidence

The four-way cross-reference graph wired by Phase 6 closures:

- **AC1 ↔ DOC-OQ9:** §AC1 Closure (R10) cites §DOC-OQ9 Closure (R6) as the reciprocal "what v1 is NOT" entry; §DOC-OQ9 Closure (R6) cites AC1 as the reciprocal "what v1 IS" entry.
- **AC1 ↔ AC2:** §AC1 Closure (R10) cites §AC2 Closure (R9) as the reciprocal execution-context restriction; §AC2 Closure (R9) cites AC1 as the reciprocal platform restriction.
- **DOC-OQ9 ↔ AC2 via MIG-003:** §MIG-003 Closure (R13) is the consolidation handle; `docs/eval/v2-followups.md` is the consolidation document.
- **AC1 ↔ MIG-003:** §MIG-003 Closure (R13) "Cross-references preserved" table cites AC1 as the v1 platform commitment that MIG-003 defers against; `docs/eval/v2-followups.md` §1 cross-reference table cites AC1.

## v1-blocking-work negative check evidence

`docs/eval/v2-followups.md` §6:

| Negative check | Result |
|---|---|
| Does this document introduce a new code change required for v1 ship? | No. All §2 items are explicitly v2-scoped. |
| Does this document re-open a v1 ADR that was previously RESOLVED? | No. DOC-OQ9 (R6), AC2 (R9), AC1 (R10), and DOC-OQ6 (R8) remain RESOLVED. |
| Does this document add a task to any Phase-1..Phase-5 tasklist? | No. All references are to existing Phase-6 tasks and v2 planning gate. |
| Does this document modify `roadmap.md` row 360 (R-116) AC? | No. Row 360 AC reads "macOS non-goal preserved; CI non-goal preserved; follow-up roadmap item created; no v1 blocking work added" — this document IS the follow-up roadmap item; it preserves both non-goals. |
| Does this document add a `--ci` flag, Darwin support code, or any harness change? | No. All harness behaviour is unchanged. |

All five rows: NO. No v1-blocking work added.

## MIG-003 acceptance crosscheck

Roadmap row 360 (MIG-003 / R-116) AC: *"macOS non-goal preserved; CI
non-goal preserved; follow-up roadmap item created; no v1 blocking
work added."*

| AC element | Satisfied at |
|---|---|
| "macOS non-goal preserved" | `docs/eval/v2-followups.md` §1 + §2.1 "v1 posture: NON-GOAL"; `decisions.md §MIG-003 Closure` Decision summary table → "Upstream macOS decision: DOC-OQ9 Closure (R6)". Reciprocal AC1 closure (R10) preserves the Linux-only platform restriction. |
| "CI non-goal preserved" | `docs/eval/v2-followups.md` §1 + §2.2 "v1 posture: NON-GOAL"; `decisions.md §MIG-003 Closure` Decision summary table → "Upstream CI decision: AC2 Closure (R9)". Reciprocal AC2 closure (R9) cited in `§MIG-003 Closure` Cross-references table. |
| "follow-up roadmap item created" | `docs/eval/v2-followups.md` exists (this task creates it); `decisions.md §MIG-003 Closure` cites it as the consolidation artifact. |
| "no v1 blocking work added" | `docs/eval/v2-followups.md` §6 five-row negative check — all five rows answer NO. |

All four AC elements satisfied.

## Cross-link

- Evidence summary: `.dev/releases/current/cliEval/evidence/T06.15/summary.md`
- ADR log: `.dev/releases/current/cliEval/decisions.md` (R13, §"MIG-003 Closure")
- Consolidation document: `docs/eval/v2-followups.md`
- Companion spec: `artifacts/D-0117/spec.md`
- Design rationale: `artifacts/D-0117/notes.md`
- Upstream decisions:
  - R6 / DOC-OQ9 Closure / T06.02 — macOS axis (`decisions.md` §DOC-OQ9 Closure)
  - R9 / AC2 Closure / T06.05 — CI axis (`decisions.md` §AC2 Closure)
  - R10 / AC1 Closure / T06.07 — Linux-only platform commitment (`decisions.md` §AC1 Closure)
- Downstream consumers:
  - T06.16 (M6 exit checkpoint) — consumes this section + `v2-followups.md` as the MIG-003 attestation in the SC1–SC5 set.
  - OPS-005 release-checklist §7.2 (T06.13) — already wired to point at MIG-003 (T06.15); now resolves to `docs/eval/v2-followups.md` via this closure section.
  - v2 release-lead (2026-07-01 planning gate) — reads `docs/eval/v2-followups.md` §3 as the four-step read-and-act list.
