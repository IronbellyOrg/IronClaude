# T06.09 — SC5 OQ-1..OQ-10 resolution ledger — Evidence summary

**Task:** T06.09 (Phase 6, SC5 / R-111)
**Deliverable:** D-0112
**Date:** 2026-05-20
**Owner sign-off:** RyanW

## Status

PASS — SC5 acceptance criteria satisfied.

## Acceptance criteria

| AC bullet (phase-6-tasklist.md / SC5 row 355) | Status | Evidence |
|---|---|---|
| All 10 OQ-xxx entries (OQ-1..OQ-10) listed in `decisions.md` | PASS | `oq-enumeration.log` — each OQ-N has exactly one `#### OQ-N` ledger heading |
| Each entry has a `resolution:` field | PASS | `decisions.md` §"SC5 OQ resolution ledger (T06.09)" — 10 rows, each with `resolution:` one-liner |
| Each entry has a `signed_off_by` field populated with RyanW | PASS | `signed-off-by.log` — 10 ledger rows carry `signed_off_by: RyanW` (lines 1108..1189) |
| All entries show status `resolved` | PASS | `grep-status-resolved.log` — 10 ledger rows carry `status: resolved` (lines 1106..1187) |
| `grep -c "status: resolved" decisions.md` returns >= 10 | PASS | `grep-status-resolved.log` — count is 16 (10 canonical rows + 6 prose mentions in R12 entry / Purpose / Verification block) |
| `artifacts/D-0112/spec.md` records the ledger summary | PASS | `.dev/releases/current/cliEval/artifacts/D-0112/spec.md` (SC5 contract restatement + OQ→resolution map) |
| Evidence saved under `evidence/T06.09/` | PASS | this directory |

## Verification commands and outputs

### 1. `grep -c "status: resolved" decisions.md`

```
$ grep -c "status: resolved" .dev/releases/current/cliEval/decisions.md
16
```

Full log: [`grep-status-resolved.log`](./grep-status-resolved.log)

Of the 16 matches, lines 1106 / 1115 / 1124 / 1133 / 1142 / 1151 / 1160 /
1169 / 1178 / 1187 are the 10 canonical ledger rows (one per OQ). The
remaining 6 are prose mentions of the literal field name in the R12
revision-log entry (line 18), the SC5 ledger Purpose paragraph (line
1088), the Verification fenced block (lines 1094, 1098, 1197), and the
Consequences section (line 1210). These prose mentions document the
gate itself and do not invent new OQ closures.

### 2. OQ-1..OQ-10 ledger heading enumeration

```
OQ-1: 1 ledger heading occurrence(s); 21 total mentions in file
OQ-2: 1 ledger heading occurrence(s); 19 total mentions in file
OQ-3: 1 ledger heading occurrence(s); 13 total mentions in file
OQ-4: 1 ledger heading occurrence(s); 9 total mentions in file
OQ-5: 1 ledger heading occurrence(s); 4 total mentions in file
OQ-6: 1 ledger heading occurrence(s); 9 total mentions in file
OQ-7: 1 ledger heading occurrence(s); 12 total mentions in file
OQ-8: 1 ledger heading occurrence(s); 20 total mentions in file
OQ-9: 1 ledger heading occurrence(s); 6 total mentions in file
OQ-10: 1 ledger heading occurrence(s); 22 total mentions in file
```

Full log: [`oq-enumeration.log`](./oq-enumeration.log)

Each of OQ-1..OQ-10 has exactly one `#### OQ-N` ledger heading. No OQ
is missing from the ledger; no OQ is doubly-listed.

### 3. `signed_off_by: RyanW` count

```
$ grep -c "signed_off_by: RyanW" .dev/releases/current/cliEval/decisions.md
15
```

Full log: [`signed-off-by.log`](./signed-off-by.log)

10 occurrences are the ledger rows (lines 1108..1189, one per OQ). 5
are prose mentions: the R12 revision-log entry (line 18), three
cross-references in DOC-OQ6 / DOC-OQ8 / DOC-OQ9 closures that pre-cite
T06.09 as the sign-off site (lines 621, 685, 751), and a reciprocal
mention in the SC4 closure of the SC1 sign-off pattern (line 998).

The SC1 ADRs (D-1..D-8 + D-10) carry their RyanW sign-offs in tabular
form rather than the literal `signed_off_by: RyanW` field; that is by
design — the literal field is an SC5 grep-gate convention.

### 4. closure_ref pointer resolution

```
OK   §"Sign-off" (R5 table) + §"OPS-001 Closure §B" (OQ-1 row, updated R5)
OK   §"OQ-2 Resolution" (with R12 sign-off flip)
OK   §"OPS-001 Closure §B" (OQ-3 row) + roadmap row 254 (DOC-OQ3)
OK   §"D-10: NOTICE/LICENSE attribution mechanism for vendored ptytest (OQ-4 closure)"
OK   this section (OQ-5 row) + `src/superclaude/cli/eval/capabilities.py:235-313` (OQ-5 deferral note + probe implementation)
OK   §"DOC-OQ6 Closure — suite naming convention + `quick.yaml` follow-up (T06.04)"
OK   §"DOC-OQ7 Closure — `--junit` flag wiring decision (T04.15)"
OK   §"DOC-OQ8 Closure — time-offset mechanism contract decision (T06.03)"
OK   §"DOC-OQ9 Closure — macOS support roadmap entry (T06.02)" (+ §"AC1 Closure" for the reciprocal Linux-only declaration)
OK   §"OPS-001 Closure §B" (OQ-10 row) + roadmap row 198 (NFR-REL2) + roadmap row 307 (R3-mit follow-up)
```

Full log: [`closure-ref-resolution.log`](./closure-ref-resolution.log)

All 10 ledger rows carry `closure_ref:` pointers that resolve to
existing sections in `decisions.md` (or, in OQ-5's case, point at the
ledger row itself plus the implementation file lines, since OQ-5's
closure is the ledger row + the harness implementation, not a prior
ADR section).

## Artifacts produced by T06.09

| Path | Purpose |
|---|---|
| `.dev/releases/current/cliEval/decisions.md` (R12 entry + OQ-2 sign-off flip + new §"SC5 OQ resolution ledger (T06.09)") | Authoritative ledger |
| `.dev/releases/current/cliEval/artifacts/D-0112/spec.md` | D-0112 spec: SC5 contract restatement, OQ→resolution map, AC site map, out-of-scope items |
| `.dev/releases/current/cliEval/artifacts/D-0112/notes.md` | Design rationale: separate-ledger vs in-place flips; field-name choice; deferred-OQ treatment; cross-reference discipline |
| `.dev/releases/current/cliEval/artifacts/D-0112/evidence.md` | Evidence specification (commands + expected outputs) |
| `.dev/releases/current/cliEval/evidence/T06.09/grep-status-resolved.log` | SC5 grep-gate output |
| `.dev/releases/current/cliEval/evidence/T06.09/oq-enumeration.log` | OQ-1..OQ-10 heading enumeration |
| `.dev/releases/current/cliEval/evidence/T06.09/signed-off-by.log` | Sign-off field count |
| `.dev/releases/current/cliEval/evidence/T06.09/closure-ref-resolution.log` | closure_ref pointer resolution |
| `.dev/releases/current/cliEval/evidence/T06.09/summary.md` | This file |

## Cross-references

- Phase tasklist: `.dev/releases/current/cliEval/phase-6-tasklist.md` (T06.09, lines 399-446)
- Roadmap: `.dev/releases/current/cliEval/roadmap.md` (SC5 row 355, R-111)
- Decisions: `.dev/releases/current/cliEval/decisions.md` (§"SC5 OQ resolution ledger (T06.09)" + R12 revision-log entry)
