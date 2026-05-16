# /sc:analyze --focus architecture --depth deep — Advisory Report

**Target:** `RELEASE-SPEC-merged.md` (v3.75 RigorflowMerger / task-unified-v3)
**Reviewer:** architect persona, Read-based pass
**Date:** 2026-05-14

## 0. Methodology note

`/sc:analyze` is a code-quality tool that depends on AST extraction, lint
adapters, and dependency graphs. The target is a markdown release spec
with no executable AST; programmatic invocation would emit thin,
non-actionable structural metrics (heading count, link density). Per the
release plan's explicit caveat, I fall back to a Read-based architectural
pass evaluating coherence, surface stability, coupling/cohesion, test
strategy, release-split sanity, risk completeness, semver, and effort
realism. This advisory should be cited in the final spec's validation
history.

## 1. Findings by category

### Coherence
The spec tells a single, internally consistent story. §1.2 verdict table
(18 candidates) flows cleanly into §2 surface contract, §3 protocol
edits, §5 test mapping, §7 release split, §8 question resolution, and §9
acceptance criteria. Cross-references are explicit (e.g., Q5/Q6 → §3.5;
Q11 → §3.7; A-005 → §8.2 gating Q1/Q2). One minor friction: §1.5 says
"R1 ⊥ R2 (siblings; can ship in parallel)" while §7.1 frames both as
"this release" with combined effort. The intent — parallel work streams
inside one release window — is correct, but a casual reader could mistake
R1/R2 as two distinct releases. Recommend clarifying wording.

### Surface stability
`/sc:task` canonical preservation is honored throughout (§2.1, §4.1,
§10). Flag count remains 8; no new flags this release (§2.1, §6.1). The
carry-over artifacts (`<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` sentinel
and `--caller task-unified`) are correctly preserved verbatim and the
DEFER lock is encoded via the canonical-form-agnostic preservation tests
in §5.2.5. This pattern is architecturally sound — tests assert
existence and structure without hardcoding the literal substring, so R3
rename remains a constant-only change. The `BLOCKED` TIER enum addition
is purely additive.

### Coupling/cohesion
The ADOPT items are largely separable. Cleanest seams: TU-003 (NFR text
addition), SE-004/SE-005 (enum additions), TUI P-02/P-03/P-05/P-07
(localized rendering fixes). Hidden coupling worth flagging:

- **TU-001 ↔ TU-004 ↔ audit.py.** All three converge on
  `audit.py` as a shared write path. The spec acknowledges this (§3.7)
  and adds the per-task write lock (INV-005), but a missed PR-ordering
  detail: `audit.py` must land before TU-001's `CriticalFailCondition`
  dataclass (which §3.3 says lives *in* `audit.py`). Recommend explicit
  PR sequence in §7.
- **TU-007 ↔ TU-001.** TU-007's completion checklist condition #5 cites
  "Adversarial verification (STRICT) returned a non-FAIL verdict" which
  composes with TU-001's CRITICAL FAIL semantics. The placeholder list is
  internally consistent but the LW-source verification could produce a
  condition that conflicts with TU-001's STRICT-only scope.
- **SE-002 ↔ SE-003.** Correctly paired (§1.2, §5.2). Good.

### Test strategy
Generally sound. P-01 mandatory test (`test_monitor_reset_between_tasks
.py`) is load-bearing and well-specified (§5.4). The 921 passed / 57
failed baseline is realistic for an existing sprint suite — it makes new
failures attributable rather than hidden. The canonical-form-agnostic
test pattern (§5.2.5) is the strongest architectural decision in the
spec: it survives the eventual rename without coupling CI to today's
literal strings.

**Gap:** §5.6 cites "+3 Wave-4 parser tests" as mandatory but does not
name them. If they don't yet exist, they must be authored as part of
SE-002+SE-003; if they exist, cite paths.

### Release split
The 4-release plan is defensible. R1+R2 as parallel siblings within v3.75
is justified by different reviewer pools and blast radii (§7.2). R3
deferral is correctly gated on A-005 and Q3 — both named, owned (§8.2),
with soft target windows. R4 deferral for SE-006 is justified by
RK-OOS-3. One mild risk: R3 packages TU-002 + TU-005 + TU-006 + Q1 + Q2
as a single release. That is a large bundle (B's effort estimate of 5-7
days underestimates if A-005 surfaces a hidden consumer). Recommend R3
be re-evaluated against sc-release-split-protocol when scheduled.

### Risk register completeness
§6.3 RK-NEW-1..5 + §6.4 inherited risks cover the surface. Missed risks:

- **No risk entry for audit.py I/O failure modes** beyond perf
  (RK-NEW-4). What happens if the audit directory is unwritable? Does
  TU-001/TU-004 hard-fail or degrade?
- **No risk for BLOCKED state interacting with `--force-strict`.** §3.5
  says force-strict bypasses BLOCKED, but doesn't address a low-
  confidence task that user *also* flags critical — audit semantics here
  are unclear.
- **TU-007 KNOWN GAP is a pre-merge blocker (§8.2) but not in §6.3.**
  Treat as RK-NEW-6.

### Backward-compat (semver)
2.0.0 → 2.2.0 minor bump is **defensible but borderline**. Under strict
semver, TU-001 (STRICT tasks that previously soft-passed now hard-fail),
TU-004 (auto-classify replaced with BLOCKED halt), TU-007 (new gate),
and SE-001 (sprint fail-closed) are behavioral breaks — these usually
warrant a major bump. The spec's argument (§1.1) is that breaks are
"migration-guide-addressable runways" and a major bump belongs with R3.
That is consistent with the "minor bump signals behavioral changes
gated by runway" convention some teams use, but it deviates from semver
strict semantics. Acceptable if release notes are loud; flag if external
consumers depend on semver guarantees.

### Effort realism
P-01 at LOW-MED in §1.2 versus its HIGH coupling rating and mandatory
test rig is inconsistent — the test plus the OutputMonitor wiring is at
least M, not S. R1's "1×M + 3×S" (§7.1) likely understates TU-007
because its pre-merge LW investigation is unbounded work. R2 at 7-10
days appears reasonable. R3 at 5-7 days is optimistic given TU-002 +
TU-005 + TU-006 + 2 renames; expect 8-12.

## 2. Severity-ranked issues

**Sev 1 (block):** none. The spec is internally coherent, hard
constraints preserved, gating investigations named and owned.

**Sev 2 (fix in release):**
- S2-a: §3.3 places `CriticalFailCondition` inside `audit.py` but §7
  doesn't sequence `audit.py` before TU-001. Add explicit PR ordering.
- S2-b: §6.3 missing risk row for audit.py I/O failure mode and a row
  for TU-007 LW-verification slip. Add RK-NEW-6, RK-NEW-7.
- S2-c: §5.6 "+3 Wave-4 parser tests" unnamed. Cite paths or mark as
  to-author with owner.
- S2-d: §1.1 semver justification needs one sentence noting external
  consumers won't see strict-semver guarantees this release.

**Sev 3 (follow-on):**
- S3-a: §1.5/§7.1 R1/R2 framing — clarify "siblings within one release"
  to avoid reader confusion.
- S3-b: §7.1 R3 effort 5-7 days likely understated; re-estimate when
  scheduled.
- S3-c: §3.5 `--force-strict` interaction with BLOCKED — add audit-log
  expected entry shape.
- S3-d: P-01 effort label inconsistent with its coupling; reclassify M.

## 3. Specific recommendations for RELEASE-SPEC.md (Wave 4)

1. Add a "PR ordering" subsection to §7.1: `audit.py` → TU-001 →
   TU-004 → TU-007; SE-001 → SE-004 → SE-005 → SE-002+SE-003 → TUI
   (P-05 → P-02 → P-03+P-07 → P-01 last).
2. Append RK-NEW-6 (audit I/O failure) and RK-NEW-7 (TU-007 LW
   verification slip blocks release) to §6.3.
3. In §5.6, replace "+3 Wave-4 parser tests" with explicit test paths
   or a TBD with owner.
4. Add one sentence to §1.1 clarifying semver convention deviation and
   that release notes will be explicit about behavioral breaks.
5. In §3.5, add `--force-strict` × BLOCKED interaction matrix and the
   audit log entry shape.
6. In §1.5 / §7.1, replace "R1+R2 (this release)" with "R1 and R2 are
   parallel work streams within v3.75."
7. Reclassify P-01 effort to M in §1.2.
8. Record this advisory in the validation-history section: "Wave-3
   /sc:analyze fallback to Read-based architectural pass per release
   plan caveat; see `artifacts/analyze-report.md`."

## 4. Verdict

**APPROVE WITH NOTES.** The spec is architecturally sound, internally
coherent, and preserves all hard constraints from v3.7. No Sev-1
blockers. Address Sev-2 items (S2-a..d) before promotion to canonical;
Sev-3 items can be tracked as follow-ons. Rework threshold: would only
be triggered if (a) TU-007 LW verification surfaces a canonical list
incompatible with TU-001 STRICT semantics, or (b) A-005 investigation
reveals a hidden consumer that breaks the carry-over preservation
assumption — neither is in scope for this review.
