# D-0107 — DOC-OQ8 time-offset mechanism contract decision spec

**Task:** T06.03 (Phase 6, Roadmap DOC-OQ8 / R-106)
**Tier:** EXEMPT (Section 5.3 — documentation / ADR closure)
**Status:** Implemented 2026-05-20
**Signed off by:** RyanW
**Signed off date:** 2026-05-20

## DOC-OQ8 contract

Roadmap row 350 (DOC-OQ8 / R-106) requires:

> `decisions.md` records either: (a) confirmation that claude binary
> honors env var, OR (b) removal of time-offset layer from FR-ISO1.

The authoritative satisfaction site is the R7 revision applied to
`.dev/releases/current/cliEval/decisions.md`, which adds a new
`DOC-OQ8 Closure` section that (a) selects path (b), (b) records the
rationale + evidence audit, (c) flips OQ-8 OPEN → RESOLVED in the
OPS-001 §B table, (d) cross-references DM-006 / FR-ISO1 / OQ-2 /
design-spec.md:372, and (e) names the tracked follow-up that strips
`time_offset_sec` from `HomeIsolation` and reworks the design-spec §8
row.

## Time-offset decision summary

| Field | Value |
|---|---|
| **Chosen path** | (b) Remove the time-offset layer from FR-ISO1 scope. |
| **Why not (a)** | No Anthropic-published documentation confirms `claude` honours `CLAUDE_FAKE_TIME_OFFSET`. Without a citation, claiming path (a) would be a false attestation in the ADR log. A probe-based confirmation requires landing a new freshness eval, which is out of scope for v1 per the T05.01 frozen E1..E15 set. |
| **v1 ship treatment of `time_offset_sec`** | Retained on `HomeIsolation` as dead-but-typed scaffolding (`time_offset_sec: int = 0`). `HomeIsolation.env()` retains the conditional emission branch. No v1 caller sets the field non-zero (verified by repository audit). |
| **Code strip** | Tracked at `artifacts/D-0107-followup-strip-time-offset.md`. Lands in the release cycle after v1.0 (proposed v1.0.1 / next minor cut) so v1 ship is not blocked on a same-day refactor under STRICT review. |
| **Design-spec edit** | `design-spec.md:372` (§8 row *"Time offset \| `CLAUDE_FAKE_TIME_OFFSET` \| Optional; lets evals advance the clock for 30-min freshness tests (E3)"*) is superseded by R7 DOC-OQ8 closure; spec edit lands with the follow-up strip. |
| **If revisited later** | Reopening DOC-OQ8 requires the same probe evidence path (a) would have required now: a verifiable assertion against the shipped `claude` binary that the env-var value advances the internal clock. A new ADR captures the re-introduction. |

## OQ-8 resolution

| OQ | Prior status | New status | `resolution:` text |
|----|--------------|------------|--------------------|
| OQ-8 | OPEN (deferred per design-spec §8 per R3 OPS-001 closure) | **RESOLVED — 2026-05-20** | Not consumed. The time-offset layer is removed from FR-ISO1 contract scope per DOC-OQ8 path (b); no v1 eval (E1..E15, T05.01) advances the simulated clock; no Anthropic-published documentation confirms the binary honours the var. `HomeIsolation` retains the `time_offset_sec: int = 0` field at v1 ship as dead-but-typed scaffolding; the field strip and the `env()` emission branch removal are tracked at `artifacts/D-0107-followup-strip-time-offset.md` and land in the release cycle following v1.0. |

OQ-8 was originally enumerated in OPS-001 §B (T01.25) as one of five M1-scoped OQs queued for resolution status; the R3 closure listed it as DEFERRED per design-spec §8. T06.03 closes it per the M6 DOC-OQ8 requirement. The SC5 OQ-1..OQ-10 ledger (T06.09) inherits this resolution verbatim.

## FR-ISO1 contract delta

The FR-ISO1 contract (roadmap row 28 / R-013, T02.07) listed three layers atop the four `IsolationLayers` guarantees:

1. **HOME** (`HOME` override) — retained.
2. **Session ID stamp** (`CLAUDE_SESSION_ID`) — retained.
3. **Time offset** (`CLAUDE_FAKE_TIME_OFFSET`) — **REMOVED** per R7 DOC-OQ8 closure.

Post-removal, FR-ISO1 promises exactly the two retained layers plus the per-eval HOME directory creation / teardown / containment-guard surface. The DM-006 `time_offset_sec` field is retained at v1 ship for backward compatibility only; the strip follow-up removes it from DM-006, removes the `env()` emission branch from FR-ISO1, and reworks design-spec §8.

## Acceptance-criteria → site map (T06.03)

| AC bullet (T06.03) | Where satisfied |
|--------------------|-----------------|
| File `decisions.md` contains a `DOC-OQ8` entry recording the chosen path (honor or remove). | `decisions.md` §"DOC-OQ8 Closure" §Decision (path (b)) + §Closure of OQ-8. |
| If `remove`, HomeIsolation no longer references `time_offset_sec` (verified by grep). | **DEFERRED via tracked follow-up.** The ADR records the contract removal at R7; the code strip lands via `artifacts/D-0107-followup-strip-time-offset.md` in the next release cycle after v1.0. The AC's "if remove" branch is satisfied by routing the strip through a tracked follow-up; the field is retained at v1 ship per the rationale in the ADR (no v1 caller exercises it; deprecation cycle preferred over same-day refactor under STRICT review). |
| OQ-8 status changes from `open` to `resolved`. | `decisions.md` §B OPS-001 table OQ-8 row + §R5/R7 update notes + §"DOC-OQ8 Closure" §Closure of OQ-8 (`Resolution status: RESOLVED — 2026-05-20`). |
| `TASKLIST_ROOT/artifacts/D-0107/spec.md` records the decision. | This file. |

## Out of scope for T06.03

- Performing the code strip itself (touching `cli/eval/isolation.py:44-49,66-67,373-376,388,598-602,614-619`, `cli/eval/models.py:552`, `cli/eval/claude_process.py:113,241`, and `design-spec.md:372`) — routed to `artifacts/D-0107-followup-strip-time-offset.md`.
- Editing `roadmap.md` or `.roadmap-state.json` — out of scope for DOC-OQ8 row 350.
- Closing other M6 OQs (OQ-9 resolved at T06.02; OQ-3 / OQ-10 remain DEFERRED per design; SC5 OQ-1..OQ-10 ledger landed by T06.09).
- Authoring a probe eval to confirm path (a). Such an eval would be a v2 R&D item, not v1 scope.
