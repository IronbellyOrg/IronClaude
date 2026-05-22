# D-0112 — SC5 OQ-1..OQ-10 resolution ledger spec

**Task:** T06.09 (Phase 6, Roadmap SC5 / R-111)
**Tier:** EXEMPT (Section 5.3 — documentation / ADR closure; no code change)
**Status:** Implemented 2026-05-20
**Signed off by:** RyanW
**Signed off date:** 2026-05-20

## SC5 contract

Roadmap row 355 (SC5 / R-111) requires:

1. Every OQ-xxx (OQ-1..OQ-10) has a `resolution:` field in `decisions.md`.
2. Every OQ-xxx is signed off by RyanW.
3. The success criterion lands at the M6 exit gate.

The phase-6 task acceptance criterion (T06.09) sharpens this into:

- All 10 OQ-xxx entries (OQ-1..OQ-10) are listed in `decisions.md` with
  `resolution` and `signed_off_by` fields populated.
- All entries show `status: resolved`.
- `grep -c "status: resolved" decisions.md` returns >= 10.
- `artifacts/D-0112/spec.md` records the ledger summary.

This document is that ledger summary.

## Authoritative satisfaction sites

- **ADR ledger:** `.dev/releases/current/cliEval/decisions.md` §"SC5 OQ
  resolution ledger (T06.09)" — the canonical 10-row table with
  `status: resolved` / `resolution:` / `signed_off_by:` /
  `signed_off_date:` fields for each OQ.
- **Per-OQ closure evidence:** the individual closure sections already in
  `decisions.md` (D-10 for OQ-4, DOC-OQ7 / DOC-OQ8 / DOC-OQ6 / DOC-OQ9
  closures, OQ-2 frozen-bodies section, OPS-001 §B table) carry the
  decision bodies; the SC5 ledger lifts the `status` / `resolution` /
  `signed_off_by` fields out of each closure into a single sweep table.
- **Verification log:** `evidence/T06.09/grep-status-resolved.log` records
  the `grep -c "status: resolved" decisions.md` count post-ledger landing.

## OQ → resolution map (one row per OQ)

| OQ | Topic | Status | Resolution summary | Closure section |
|----|-------|--------|--------------------|-----------------|
| OQ-1  | Remaining `decisions.md` open-question items (SC5 driver)    | resolved | RyanW signed off D-1..D-8 and D-10 in R5 (`decisions.md` Sign-off table); OPS-001 D-5..D-8 queue cleared. | §Sign-off (R5) + §"OPS-001 Closure §B" |
| OQ-2  | Concrete content of E3..E15 manifest entries                 | resolved | T05.01 froze E3..E15 body shapes; signed off at T06.09 in the SC5 sweep below. | §"OQ-2 Resolution" + §"SC5 OQ resolution ledger (T06.09)" |
| OQ-3  | Which eval categories are excluded by `--no-pty`             | resolved | DOC-OQ3 (T04.16): exclusion set written to `suites/real.yaml` as the `no_pty:skip` per-eval tag; `--no-pty` implementation honours the tag; `eval describe` surfaces it. | §"OPS-001 Closure §B" (OQ-3 row) + roadmap row 254 (DOC-OQ3) |
| OQ-4  | NOTICE/LICENSE attribution mechanism for vendored ptytest    | resolved | D-10 (R4, 2026-05-20) — top-level `NOTICE` references `src/superclaude/cli/eval/pty/LICENSE`; verbatim upstream MIT terms retained at the vendored path; PROVENANCE.md records fork SHA + diffs. | §"D-10" |
| OQ-5  | Exact MCP server reachability check semantics                | resolved | M1 implementation (`src/superclaude/cli/eval/capabilities.py:292-313`) ships PATH-presence as the reachability signal for the default MCP roster (`auggie`, `auggie-mcp`, `airis-mcp-gateway`); SOFT-SKIP failure mode covers the M2 follow-up surface via the `mcp_probe` injection hook so a future handshake / SSE probe drops in without API change. | §"SC5 OQ resolution ledger (T06.09)" (OQ-5 row) |
| OQ-6  | Suite filename convention beyond `real.yaml`                 | resolved | DOC-OQ6 (R8, T06.04) — naming convention ratified in `src/superclaude/cli/eval/suites/README.md`; `quick.yaml` recorded as a deferred follow-up with shape + trigger conditions. | §"DOC-OQ6 Closure" |
| OQ-7  | Whether `--junit` flag is supported in CLI                   | resolved | DOC-OQ7 (T04.15, R-076) — `--junit` is wired into FR-CLI1; spec §4 flag table updated to list 12 flags; `Reporter.to_junit()` + `emit_junit` gate already on disk. | §"DOC-OQ7 Closure" |
| OQ-8  | How `CLAUDE_FAKE_TIME_OFFSET` is consumed or validated       | resolved | DOC-OQ8 (R7, T06.03) — path (b): time-offset layer REMOVED from FR-ISO1 scope; `HomeIsolation.time_offset_sec` retained at v1 ship as dead-but-typed scaffolding; strip tracked at `artifacts/D-0107-followup-strip-time-offset.md`. | §"DOC-OQ8 Closure" |
| OQ-9  | macOS support timeline and scope                             | resolved | DOC-OQ9 (R6, T06.02) — macOS deferred to v2 (target 2026-Q3); v1 ships Linux-only per AC1; `eval doctor` refuses non-Linux platforms. | §"DOC-OQ9 Closure" |
| OQ-10 | Exact MCP-flaky failure taxonomy permitting retry-once       | resolved | Empirical resolution accepted per debate convergence (roadmap row 114). v1 ships NFR-REL2 default no-retry path; `R3-mit` (MCP retry-once) deferred to a P1 follow-up post-v1 against the `mcp_server_flaky` outcome tag. Resolution is the deferral itself (the question is closed by recording the v1 retry posture in the ledger). | §"SC5 OQ resolution ledger (T06.09)" (OQ-10 row) |

## Acceptance criteria → site map

| AC bullet (T06.09)                                                                                | Where satisfied |
|---------------------------------------------------------------------------------------------------|-----------------|
| All 10 OQ-xxx entries listed with `resolution` and `signed_off_by` fields populated.              | `decisions.md` §"SC5 OQ resolution ledger (T06.09)" (10 entries) |
| All entries show status `resolved`.                                                               | Same section — each row carries an explicit `status: resolved` line. |
| `grep -c "status: resolved" decisions.md` returns >= 10.                                          | `evidence/T06.09/grep-status-resolved.log` (count == 10 + ledger header references). |
| `artifacts/D-0112/spec.md` records the ledger summary.                                            | This file. |

## Out of scope for T06.09

- Re-opening any of the underlying decisions. Each OQ row points back to
  its canonical closure section in `decisions.md`; the SC5 ledger lifts
  fields out of those sections, it does not re-litigate them.
- Editing `roadmap.md` or `.roadmap-state.json` — the ledger is a
  `decisions.md` artifact only.
- Implementation work for the M2 follow-up MCP probe (OQ-5) or the v1.0.1
  `time_offset_sec` strip (OQ-8) — both are tracked as deferred follow-ups
  in their respective closure sections / artifacts.

## Cross-references

- **SC1 (T06.01, R-104):** the ADR sign-off infrastructure SC5 depends on
  (same `signed_off_by` / `signed_off_date` field pattern).
- **SC4 (T06.08, R-110):** the production-code attestation that the v1
  implementation matches the design-spec contract within recorded variance;
  reads each OQ closure as a cost-shape driver.
- **T06.16 (M6 exit checkpoint):** consumes this ledger as the SC5
  attestation; `grep -c "status: resolved" decisions.md` is a checkpoint
  verification line.
- **`evidence/T06.09/`:** the grep verification log + the SC5 sweep
  summary.
