# D-0111 — Notes

## Design notes

1. **Why a closure section appended to the ADR log, not a new D-N ADR.**
   SC4 is a documentation ratification of effort already spent, not an
   architectural decision about how to build the next thing. The
   architectural decisions whose enforcement caused the harness overrun
   (D-5..D-8) are already canonical in `decisions.md`; SC4 reads those
   ADRs as the cost drivers, it does not re-decide them. Following the
   convention established by AC1/AC2/DOC-OQ6/DOC-OQ8/DOC-OQ9 closures
   (R6-R10), this lands as a `## SC4 Closure` section appended to the
   ADR log rather than a new D-N entry. R11 is the corresponding
   revision-log line.

2. **Why the SC4 axes are "harness" + "eval bodies" and not a single
   combined number.** The design-spec §17 phase budget already factored
   the v1 work into a harness budget (Phases 1-4, ~1,340 LOC of Python)
   and an eval-bodies budget (Phase 5, ~3,000-4,500 LOC of YAML). A
   combined single number would obscure the asymmetric delta — the
   harness +701% / eval bodies -57% / combined +143% — which is the
   most operationally important fact in this section. Per-axis
   reporting matches the source-of-record (`design-spec.md:834-840`)
   and preserves the signal that the two axes diverged for opposite
   reasons.

3. **Why exclude `cli/eval/suites/` from the harness count and exclude
   the vendored ptytest fork from both counts.** Three reasons:
   - The design-spec §17 phase budget puts `suites/` content under
     Phase 5 (eval bodies), not Phase 1-4 (harness). Conflating them
     would let an under-budget YAML axis mask an over-budget Python
     axis, which is exactly what SC4 exists to prevent.
   - The vendored ptytest fork is third-party code per D-10 attribution.
     Counting its LOC against the SC4 harness estimate would let
     external code mask harness cost growth (or, conversely, get
     credit for harness cost discipline that is not the project's to
     claim).
   - `cli/eval/schemas/__init__.py` (44 LOC) is excluded too — schema
     files are configuration, not harness logic, and the estimate did
     not name them.

4. **Why include tests as an informational row but exclude them from
   the SC4 estimate band.** Tests (28,831 LOC) are ~2.7x production
   LOC, which is informative but not part of the SC4 contract. The
   design-spec §17 phase budget is production code only (Phase 5
   names "evals" but means YAML manifests, not the pytest harness).
   Adding tests to the +/-15% comparison would either (a) require
   retroactively inventing a test-LOC estimate, which would be
   fabrication, or (b) widen the band arbitrarily, which would dilute
   SC4's value as a delta-detection contract. The informational row
   exists so future readers can see the absolute size without thinking
   it was held to the estimate envelope.

5. **Why the harness justification is binned into five categories and
   not file-by-file.** Five categories matches the design-spec §17
   structure (Phase 1-4 phase boundaries + R2 supplement). A per-file
   walk would be longer than the source of the overrun is worth and
   would force future maintainers to re-derive the same five categories
   each time. The categories are: (1) D-5..D-8 production fidelity,
   (2) error/retry/signal handling, (3) CLI ergonomics, (4) PTY
   adapter layers, (5) reporter/artifact-layout split. Each category
   names the LOC contribution and the architectural cause; the
   per-file LOC log lives in `evidence/T06.08/loc-harness-py.log` for
   anyone who wants to walk the trees.

6. **Why the eval-bodies underrun justification is four causes and not
   one.** The natural reading would be "D-4 declarative YAML is
   denser than estimated, done." But three of the four causes
   (OQ-2 frozen body shapes, DOC-OQ6 `quick.yaml` deferral, no
   XFAIL/XPASS scaffolding) are *deferrals or scope decisions* that
   each independently contributed to the underrun and each is a
   separate audit pointer. Folding them into "D-4 architecture" would
   hide three distinct project decisions behind one ADR's name.

7. **Why no remediation action accompanies SC4 closure.** Three
   options were considered:
   - **(a) Acknowledge and ship** — chosen. SC4 contract says the
     deltas must be recorded and justified; it does not say they
     trigger a re-plan. The implementation is complete (T01..T05
     closed), tested (28,831 LOC of tests, all pass), and ADR-aligned
     (D-1..D-10 + D-0110/0111). Halting M6 closure for an effort-
     accounting delta would be expensive and would yield no product
     improvement.
   - **(b) Retroactively amend the estimate to fit the actual** —
     rejected. Faking the estimate to look honest is the exact failure
     mode SC4 exists to prevent. The whole point of the +/-15% band is
     that delta means something only if the original estimate is
     immutable.
   - **(c) De-scope harness features to fit the estimate** — rejected.
     Every overrun line traces to a design-spec / roadmap / ADR
     requirement. Removing them would create new gaps (D-5 hook-
     matcher coverage, D-7 path traversal hardening, AC1 platform
     refusal, etc.) that would themselves require new ADR closures.

8. **Why the resolution names "+/-15%" explicitly and quotes the
   bands in the spec.** Future readers will not have the SC4 row
   committed to memory. Naming the band in the closure section makes
   the comparison self-contained; quoting the per-axis bands in
   `artifacts/D-0111/spec.md` makes the spec independently auditable
   without a cross-fetch. The `roadmap.md` source is still cited so
   the original commitment is reachable.

## Edge cases considered

- **A future eval is added to `real.yaml`.** New YAML LOC lands inside
  the eval-bodies axis. Whether the new total exceeds the original
  3,000-4,500 estimate depends on the new eval's verbosity; even a
  large addition is unlikely to push past the upper estimate band
  (it would take ~1,400 LOC of new YAML to reach 3,000 from 1,618).
  No remediation triggers unless a future SC4 row is opened against a
  v2 estimate.

- **A future ADR (e.g., D-11 cleanup phase) lands new harness code.**
  This SC4 row stays frozen as the v1 attestation. If a v2 SC4 row is
  opened, it gets its own estimate-vs-actual ledger and its own
  delta justification; the original 2026-05-20 row is preserved per
  the Reject/revise rule.

- **The vendored ptytest fork is replaced or upstreamed.** D-10
  attribution still excludes the fork from the harness LOC count; the
  exclusion rule is "third-party code", not "code that lives at this
  path". If the fork is upstreamed and removed, the harness LOC
  number does not change because the fork was never part of it.

- **Test LOC ratio (2.7x) drifts up or down.** Informational only.
  The ratio is tracked here for context; it does not block any
  acceptance criterion. A future SC entry could be opened against a
  test-LOC budget if the project chose to, but v1 does not have one.

- **A grep-counter discrepancy between this section and the evidence
  logs.** Possible if `find` is rerun after a code edit. The evidence
  logs (`evidence/T06.08/loc-*.log`) carry the exact `find | xargs wc
  -l` output captured on 2026-05-20; the LOC numbers in this section
  are taken from those logs. Any future drift between the section and
  the tree is resolved by reading the logs as the snapshot-of-record
  and (if warranted) opening a v2 SC4 row.

- **`design-spec.md:827` line moves due to upstream edit.** The
  citation here is the line number as of 2026-05-20. A drift-detector
  (grep for the R1 checkbox text) is the correct response, not a
  line-number chase. The `design-spec.md` content is canonical; this
  section quotes the relevant clause inline so a line shift does not
  invalidate the citation.

## Validation steps performed

1. Confirmed `decisions.md` §"SC4 Closure" landed at line 930 and
   contains all required subsections (Context, Decision table, Delta
   justification — harness, Delta justification — eval bodies,
   Combined delta interpretation, Closure of SC4, Cross-references,
   Consequences).
2. Confirmed the R11 revision-log line landed at line 17 with the
   2026-05-20 date and full SC4 closure summary.
3. Confirmed top-of-file status line names "R6-R11 closures land
   DOC-OQ9, DOC-OQ8, DOC-OQ6, AC2, AC1, SC4 in M6".
4. Re-ran `find src/superclaude/cli/eval -name '*.py' -not -path
   '*/suites/*' -not -path '*/schemas/*' -not -path '*/pty/*' | xargs
   wc -l` and confirmed the harness total (10,731 LOC) matches the
   logged value in `evidence/T06.08/loc-harness-py.log`.
5. Re-ran `find src/superclaude/cli/eval/suites -type f | xargs wc
   -l` and confirmed `real.yaml` is 1,618 LOC.
6. Re-ran `find tests/cli/eval -name '*.py' | xargs wc -l` and
   confirmed the test total (28,831 LOC).
7. Confirmed `artifacts/D-0111/spec.md` carries the estimate-vs-
   actual ledger table, the per-axis delta justifications mirroring
   `decisions.md`, the LOC measurement methodology section, and the
   acceptance-criteria site map.
8. Confirmed the cross-reference list in `decisions.md` §"SC4
   Closure" §"Cross-references" names SC1, SC2, SC3, SC5, D-5..D-8,
   DOC-OQ7, DOC-OQ6, OQ-2, the design-spec source line, and T06.16
   (the M6 exit checkpoint consumer).
