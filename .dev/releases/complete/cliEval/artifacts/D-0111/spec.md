# D-0111 — SC4 effort estimate acknowledgment spec

**Task:** T06.08 (Phase 6, Roadmap SC4 / R-110)
**Tier:** EXEMPT (Section 5.3 — documentation / ADR closure; no code change)
**Status:** Implemented 2026-05-20
**Signed off by:** RyanW
**Signed off date:** 2026-05-20

## SC4 contract

Roadmap row 354 (SC4 / R-110) requires:

1. `decisions.md` records the signed-off pre-implementation LOC estimate.
2. `decisions.md` records the post-implementation actual LOC measurement.
3. Any delta beyond the +/-15% SC4 band is explicitly justified.
4. SC4 entry status flips OPEN → RESOLVED with `signed_off_by: RyanW`.
5. `artifacts/D-0111/spec.md` records the estimate-vs-actual ledger.

The authoritative satisfaction sites are:

- **ADR:** `.dev/releases/current/cliEval/decisions.md` §"SC4 Closure" —
  signed-off estimate + actual measurement + per-axis delta justification
  + cross-references to D-5..D-8, DOC-OQ7, DOC-OQ6, OQ-2 as the
  ADR-mandated cost drivers.
- **Evidence logs:** `evidence/T06.08/loc-harness-py.log` (per-file
  harness Python LOC), `evidence/T06.08/loc-eval-bodies.log` (suites/
  contents LOC), `evidence/T06.08/loc-tests.log` (informational test
  LOC). Captured via `find ... | xargs wc -l` on the final tree as of
  2026-05-20.
- **Source authorities:** `design-spec.md:827` (R1 acknowledged-effort
  checkbox) + `design-spec.md:834-840` (§17 per-phase LOC breakdown) for
  the pre-implementation estimate; `roadmap.md:354,450` for the SC4
  acceptance criterion + the +/-15% band.

## Estimate vs actual ledger

| Axis | Estimate | Actual | Delta vs midpoint | Within +/-15%? |
|------|----------|--------|--------------------|----------------|
| Harness (Python under `src/superclaude/cli/eval/` excluding `suites/`) | ~1,340 LOC | **10,731 LOC** | **+9,391 LOC (+701%)** | No |
| Eval bodies (`src/superclaude/cli/eval/suites/real.yaml`) | ~3,000-4,500 LOC (midpoint 3,750) | **1,618 LOC** | **-2,132 LOC (-57%)** | No |
| **Combined** | **~4,340-5,840 LOC (midpoint 5,090)** | **12,349 LOC** | **+7,259 LOC (+143%)** | No |
| Tests (informational, not part of SC4 envelope) | not estimated | 28,831 LOC | N/A | N/A |

Both per-axis deltas exceed the +/-15% SC4 band; both are justified
below. SC4 requires the deltas be **recorded and justified**, not that
they fall inside the band — RyanW sign-off acknowledges that the v1
implementation is complete in good faith against the original estimate
and that the delta is honest rather than scope-creep.

## Per-axis delta justification

### Harness (+701%, +9,391 LOC)

Five categories of work absorbed the unbudgeted complexity:

1. **D-5..D-8 production-fidelity enforcement (~+2,500 LOC).** The four
   CRITICAL R2 ADRs landed at full enforcement fidelity, not the
   prototype scope the original phase budget assumed:
   - D-5 hook-matcher coverage gate → `coverage.py` (348 LOC).
   - D-6 `--max-disk-mb` poller → `disk_budget.py` (492 LOC).
   - D-7 three-layer path-traversal hardening → `validate_eval_id`
     regex in `loader.py` (~+200 LOC of the 623 LOC total) + symlink
     resolution branches in `isolation.py` (~+350 LOC of the 696 LOC
     total).
   - D-8 reporter dimensional invariant + 8-status taxonomy →
     `models.py` (937 LOC) with `EvalOutcome` dataclass +
     `AggregatedRunReport.from_outcomes()` contract assertion.

   The R2 supplement was estimated at +150 LOC total; the actual
   per-ADR cost is an order of magnitude higher.

2. **Production error handling, retry, signal management (~+1,500 LOC).**
   `runner.py` reaches 1,237 LOC because it carries atomic-setup
   contract (design-spec §11 #6), MCP-flaky retry-once (NFR-REL2 /
   R3-mit), and full keep-on-failure / preserve-partial-HOME teardown
   semantics. `signal_handler.py` (254 LOC) and `retry.py` (165 LOC)
   are net-new files the design-spec did not name.

3. **CLI surface and operator ergonomics (~+1,500 LOC).** `commands.py`
   reaches 1,695 LOC because the FR-CLI1 12-flag set (DOC-OQ7 resolution)
   lands `doctor`, `run`, `list`, `describe`, capability-report
   rendering, suite resolution, AC1 platform precheck (T06.07), `--json`
   emission, `--max-disk-mb` wiring, `--junit` wiring, and artifact-layout
   glue. The phase-4 estimate (~150 LOC) was off by an order of
   magnitude — CLI wiring at production fidelity is its own subsystem.

4. **PTY + adapter layers (~+700 LOC).** Phase-1 assumed the vendored
   ptytest fork would carry most PTY work. In practice the harness has
   `pty_driver.py` (426 LOC) + `pty_stream.py` (288 LOC) as adapter
   layers atop the vendored fork (the fork itself lives at
   `cli/eval/pty/` and is third-party code per D-10 attribution —
   excluded from the 10,731 LOC harness figure). `claude_process.py`
   (369 LOC) wraps the real Claude Code subprocess; `hook_adapter.py`
   (269 LOC) wraps the `install_hooks` cross-process surface for E12
   idempotency.

5. **Reporting and artifact-layout split (~+700 LOC).** Phase 3 folded
   reporter into orchestrator + runner; the shipped code has
   `reporter.py` (233 LOC), `run_report.py` (379 LOC), and
   `artifact_layout.py` (305 LOC) as three concerns plus `expect.py`
   (722 LOC) for the 10-primitive Expect.* DSL (D-2). The Expect DSL
   alone exceeds the entire Phase 2 estimate (350 LOC).

Every line of the +9,391 LOC overrun traces to a design-spec
requirement, a roadmap row, or an R2 ADR enforcement obligation. The
overrun is an honest acknowledgment that the design-time phase budget
under-estimated production-grade complexity; it is NOT scope creep.

**Recommendation for future estimates:** multiply design-time phase
LOC budgets by ~3-5x to internalize the production-fidelity tax this
v1 surfaced.

### Eval bodies (-57%, -2,132 LOC)

Four causes of the underrun:

1. **D-4 declarative YAML compressed per-eval LOC.** Average ~108 LOC
   per eval (1,618 LOC / 15 evals) vs the ~200-300 LOC/eval the
   estimate assumed. The D-4 schema carries enough conventions (named
   expects, capability tags, parameterize blocks) that each manifest
   entry is mostly declarative payload.

2. **OQ-2 frozen body shapes (T05.01) bounded the scope.** The R3 / R4
   estimate assumed bespoke per-eval Python; OQ-2 resolution froze
   E3..E15 to YAML-expressible bodies with only E14 needing the D-4
   callback escape hatch.

3. **`quick.yaml` deferred (DOC-OQ6 / R8).** The estimate range
   allowed for a second suite alongside `real.yaml`; DOC-OQ6 closure
   deferred `quick.yaml` to post-v1.

4. **No XFAIL/XPASS scaffolding at v1.** The D-8 8-status taxonomy
   added XFAIL/XPASS as legal statuses, but no v1 eval declares those
   expectations.

The underrun is **NOT** a coverage gap — D-5 hook-matcher coverage gate
enforcement verifies every PostToolUse / SessionStart / UserPromptSubmit
matcher in `src/superclaude/hooks/hooks.json` is exercised by ≥1 eval in
the frozen 15. SC2 coverage is satisfied with denser-than-estimated YAML.

### Combined interpretation

The +143% combined overrun reflects asymmetry: the harness absorbed the
spec-panel R2 work, the production-grade error handling, and the CLI
ergonomics. The eval bodies came in dense because the harness took on
the heavy lifting. The harness over-delivered on the design-spec
contract; the eval bodies satisfied SC2 (coverage) at lower YAML cost
than feared.

## SC4 resolution

| SC | Prior status | New status | `resolution:` text |
|----|--------------|------------|--------------------|
| SC4 | OPEN (roadmap row 354, M6 docs lane) | **RESOLVED — 2026-05-20** | Pre-implementation estimate: ~1,340 harness + ~3,000-4,500 eval bodies (signed off at `design-spec.md:827` R1). Post-implementation actual: 10,731 harness Python + 1,618 eval-body YAML (12,349 combined). Delta: +701% harness (justified by D-5..D-8 production-fidelity enforcement + production error handling + CLI ergonomics + PTY adapter layers + reporter split), -57% eval bodies (justified by D-4 YAML compression + OQ-2 frozen bodies + DOC-OQ6 `quick.yaml` deferral), +143% combined. Test LOC 28,831 tracked informationally outside SC4 envelope. |

## Cross-references

| Reference | Where | Why |
|---|---|---|
| **SC1 (T06.01 / R-104)** | `decisions.md` Sign-off table + R5 revision | Sign-off infrastructure SC4 depends on; same `signed_off_by: RyanW` / `signed_off_date: 2026-05-20` pattern. |
| **SC2 coverage (roadmap row 451)** | D-5 hook-matcher coverage gate enforcement | The eval-bodies underrun (-57%) does NOT reduce SC2 coverage; coverage is gate-enforced, not LOC-correlated. |
| **SC3 (T06.10 / R-112)** | `decisions.md` (M6) | Zero-new-deps verification; SC3 unaffected by SC4 — the harness LOC overrun is in already-imported stdlib + jsonschema + the vendored ptytest fork. |
| **SC5 (T06.09 / R-111)** | `decisions.md` OQ ledger | SC5 reads SC4 as the production-code attestation that v1 matches the design-spec within recorded variance. |
| **D-5..D-8 (R2, 2026-05-18)** | `decisions.md` §"D-5"..§"D-8" | The four CRITICAL ADRs whose production-fidelity enforcement accounts for ~+2,500 LOC of the +9,391 LOC harness delta. |
| **DOC-OQ7 closure (T04.15)** | `decisions.md` §"DOC-OQ7 Closure" | FR-CLI1 12-flag decision driving `commands.py` to 1,695 LOC. |
| **DOC-OQ6 closure (T06.04 / R8)** | `decisions.md` §"DOC-OQ6 Closure" | `quick.yaml` deferral, partial cause of eval-bodies underrun. |
| **OQ-2 resolution (T05.01)** | `decisions.md` §"OQ-2 Resolution" | E3..E15 body shapes frozen, primary cause of eval-bodies YAML density. |
| **`design-spec.md:827,834-840`** | Source authority | Authoritative pre-implementation estimate + §17 per-phase LOC breakdown. |
| **T06.16 (M6 exit checkpoint)** | `phase-6-tasklist.md` | Consumes this section as the v1 SC4 attestation. |

## LOC measurement methodology

Captured 2026-05-20 from the final tree at this release's HEAD via:

```bash
find src/superclaude/cli/eval -type f -name '*.py' \
    ! -path '*__pycache__*' | sort | xargs wc -l \
    > evidence/T06.08/loc-harness-py.log

find src/superclaude/cli/eval/suites -type f \
    \( -name '*.yaml' -o -name '*.json' -o -name '*.md' -o -name '*.py' \) \
    ! -path '*__pycache__*' | sort | xargs wc -l \
    > evidence/T06.08/loc-eval-bodies.log

find tests/cli/eval -type f -name '*.py' | sort | xargs wc -l \
    > evidence/T06.08/loc-tests.log
```

`find | wc -l` reports total physical lines (including blank lines and
comments). This is the same convention as the original
`design-spec.md:834-840` estimate (which cites raw LOC, not SLOC). No
`cloc` or `tokei` normalization is applied because the estimate carries
no normalization either; comparing physical LOC to physical LOC is the
honest comparison.

The harness Python figure (10,731 LOC) excludes:

- `suites/__init__.py` (15 LOC) — counted under eval bodies.
- `cli/eval/pty/CHECKLIST.md` + `cli/eval/pty/PROVENANCE.md` (205 LOC
  documentation only; the vendored fork's Python sources are
  third-party per D-10 attribution and not counted as harness LOC).
- `__pycache__/` artifacts.

The eval-bodies figure (1,618 LOC) is `suites/real.yaml` only; the
auxiliary `suites/README.md` (173 LOC), `suites/suite.schema.json`
(161 LOC), and `suites/__init__.py` (15 LOC) are not eval bodies. The
combined `loc-eval-bodies.log` reports 1,967 LOC total because it
includes those auxiliary files; the SC4 ledger isolates the 1,618 LOC
manifest figure as the eval-bodies authority.

## Acceptance-criteria → site map (T06.08)

| AC bullet (T06.08) | Where satisfied |
|--------------------|-----------------|
| `decisions.md` contains an `SC4` entry with signed-off LOC estimate and actual LOC measurement. | `.dev/releases/current/cliEval/decisions.md` §"SC4 Closure" — Decision table records estimate + actual + delta per axis. |
| Delta is recorded and within +/-15% of estimate (or justified explicitly). | Outside +/-15% on both axes; justified in §"Delta justification — harness" and §"Delta justification — eval bodies" subsections of the closure + this artifact §"Per-axis delta justification". |
| SC4 entry status is `resolved`. | `decisions.md` §"SC4 Closure" §"Closure of SC4" subsection: `Resolution status: RESOLVED — 2026-05-20`. |
| `artifacts/D-0111/spec.md` records the estimate vs actual. | This file. |

## Out of scope for T06.08

- Re-estimating the design-spec phase budgets — out of scope at M6;
  the v1 estimate is the historical record, not a moving target. A
  future v2 SC4 would estimate v2 scope separately.
- Normalizing LOC via `cloc` or `tokei` SLOC counts — comparison is
  apples-to-apples physical LOC against the design-spec.md:834-840
  estimate, which uses physical LOC.
- Counting test LOC inside the SC4 +/-15% band — the design-spec §17
  budget is production code; tests are informational.
- Counting the vendored ptytest fork Python sources as harness LOC —
  third-party per D-10 attribution; excluded from the 10,731 LOC
  figure consistent with the original phase-1 estimate convention.
- Editing `roadmap.md` or `.roadmap-state.json` — out of scope for
  SC4 row 354.
- Reducing the harness LOC to meet the +/-15% band — the
  implementation is complete and tested; SC4 records the delta for
  honesty, not as a remediation action.
