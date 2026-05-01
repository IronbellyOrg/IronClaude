# Merge Log — Step 5 execution log

## Metadata

| Field | Value |
|---|---|
| Pipeline | `/sc:adversarial` (asymmetric A/B compare mode) |
| Pipeline depth | 3 rounds + invariant probe |
| Rounds executed | R1 (parallel advocates) → R2 (rebuttals) → R2.5 (invariant probe) → R3 (final positions) |
| Convergence achieved | YES — R3, average 0.825 (impl 0.85 / spec 0.80) |
| Convergence threshold | 0.80 (passed) |
| HIGH UNADDRESSED at convergence | 0 (INV-004 + INV-025 → ADDRESSED-R3 via P-006 + P-007) |
| Fallback used | No |
| Failure stage | None |
| Invocation method | skill-direct (`/sc:adversarial` invoked from `sc-adversarial-protocol`) |
| Base frame selected | B-as-base (spec-frame) — see `base-selection.md` §3-§4 |
| Tiebreaker invoked | Threshold case (5.0% margin); user-stated-goal alignment used |

---

## §1 Per-diff-point synthesis (which side won, with confidence)

Sourced from `debate-transcript.md` Scoring Matrix. Compact summary table.

| Bucket | Count | Notes |
|---|---|---|
| Impl-advocate clear wins (point retained as-is) | 14 | U-017, U-018, U-019, U-020, U-022, U-025, U-026, U-028, U-029, U-030, U-036, U-037, U-038, X-002, X-003, X-005 (consolidated; some bundled) |
| Spec-advocate concessions accepted by impl (lands R3) | 9 | U-007, U-024, U-035, X-004, X-006, INV-004, INV-009, INV-014, INV-019 |
| Draw / split (compromise resolution) | 7 | U-021 (Makefile + PR-comment split), U-023 (optional BEAT_2_BACKLOG.md appendix), U-031 (Makefile + release-eng), U-032 (3-of-8 + PR-comment for rest), U-033/U-034 (PR-description link), U-014 (benign 8th commit), X-001 (chronology vs framing) |
| NEW findings from probe (no advocate side) | 8 | INV-005 (deferred), INV-011 (clamped in P-009), INV-015 (T-015), INV-023 (T-016), INV-024 (deferred), INV-026 (deferred), INV-028 (deferred), INV-030 (deferred) |

### §1.1 Per-point evidence summary (per-row)

| Diff ID | Winner | Conf | Evidence one-liner | Refactor target |
|---|---|---|---|---|
| U-007 | spec | 100% | `wait()` direct attr, `terminate()` getattr → init in `__init__` | P-011 |
| X-004 | spec | 100% | `prompt_via=stdin` literal absent from log | P-012 |
| X-006 | spec | 95% | T-011 conditional → mock-injected unconditional | P-013 |
| U-024 | spec | 95% | 15 DEFER items unsurfaced → BEAT_2_BACKLOG.md | P-014 |
| U-035 | spec | 95% | D-NNN traceability → TRACEABILITY.md | P-015 |
| INV-004 | spec | 100% | PRD terminate missing 4-line block | P-006 |
| INV-025 | spec | 100% | PRD terminate test gap | P-007 |
| INV-009 | spec | 100% | Env-var int() crash | P-009 |
| INV-014 | spec | 90% | n=0 silent break observability | T-012 |
| INV-019 | spec | 95% | NUL-byte round-trip not pinned | T-013 |
| INV-002 | spec | 100% | `_stdin_error` not in `__init__` | P-011 (paired with U-007) |
| W-L9 | spec (R2-impl-conceded) | 95% | NUL-byte test | T-013 |
| W-L10 | spec (R2-impl-conceded) | 95% | finally-close mutation-kill | T-014 |
| U-021 | DRAW | 80% | Cross-host repro split | P-016 + D-FOLLOW-001 |
| U-031 | impl | 75% | Operational not code | P-016 |
| U-032 | DRAW | 85% | 3-of-8 in tree, rest in PR-comment | (PR description amendment) |
| (others) | impl-mostly | 70-100% | See debate-transcript §"Scoring matrix" | (no fix, kept as-is) |

---

## §2 Convergence trajectory

```
Round    Impl   Spec   Spread   Status
-------  -----  -----  ------   -----------------------------------------
R1       0.65   0.55   0.10     wide; impl over-confident on 22-unique-to-B
R2       0.78   0.70   0.08     mediums acknowledged; reframing accepted
R2.5     0.72   0.68   0.04     probe surfaces 2 HIGH; both scores reduce
R3       0.85   0.80   0.05     HIGH ADDRESSED; converged

Average R3: 0.825
Threshold:   0.80 (PASSED)
```

### §2.1 Why R3 converged (and not earlier)

R2 was close to convergence (spread 0.08) but neither advocate had visibility into the PRD subclass gap — R2-impl cited F-strict-review's MEDIUM-1 in passing but did not propose to fix it; R2-spec did not name PrdClaudeProcess as a HIGH issue. The invariant probe (R2.5) was the unblocker: by directly reading `prd/process.py:239-279` and confirming the subclass override predates P-004, it forced the issue onto both advocates' R3 surfaces.

Both R3 advocates accept the 4-line patch (P-006) + new test file (P-007) as the resolution; spec-advocate adds parametric subclass coverage (P-008) and §4 P-004 spec amendment (P-010) as same-PR follow-ups.

### §2.2 Why didn't we go to R4?

Per protocol, R4 escalation triggers only if convergence < 0.80 OR HIGH UNADDRESSED > 0 after R3. After R3:
- Average 0.825 ≥ 0.80 ✓
- HIGH UNADDRESSED = 0 (both INV-004 and INV-025 ADDRESSED via R3 concessions with named file:line, owner, acceptance criteria) ✓

R4 not triggered. Convergence finalised at R3.

---

## §3 Items "merged" into the final verdict

From each variant, what survived into the merged output:

### From Variant A (implementation diff)

- **All 5 patches retained as-shipped** (P-001 through P-005; commits `526a606`, `c42139b`, `be46520`, `5a8e5e7`, `01cf2ef`). Mechanical correctness verified by F-strict-review and invariant probe.
- **All 11 T-NNN tests retained** (test_process_stdin.py L201-597). T-011 modified by P-013 (mock-injection); rest unchanged.
- **A's 4 spec corrections retained**:
  - X-005 — A's `_process.poll()` (correcting B's `proc.poll()` typo).
  - X-002 — A's 18s SIGTERM budget (defended over B's 16s; mathematically conservative for `start()` prelude).
  - X-003 — A's `< 4 * 1024` ceiling (strict subset of B's `≤ 4 KB`).
  - U-008, U-009 — A's positive boundary test + tool_write_mode_false negative companion (more rigorous than B).
- **A's narrative comment** (U-003 in `cli_portify/process.py`) — useful historical context; positive drift.
- **A's `# pragma: no cover` annotations** (U-001, U-002) — coverage hygiene.
- **A's defensive `if n <= 0: break`** (U-005) — augmented by T-012 to capture as `_stdin_error`.

### From Variant B (RECONCILED_DESIGN.md spec)

- **§4 P-001..P-005 acceptance criteria** retained as the contract surface that A was measured against.
- **§5 T-001..T-011 mocking strategy + pass/fail criteria** retained as the test contract.
- **§3.2 SUPERSEDED + DEFER ledgers** retained as historical record (and the DEFER list lands as `BEAT_2_BACKLOG.md` per P-014).
- **§7 R-1..R-6 risk register** retained as risk-coverage map; R-1/R-2/R-3 marked resolved, R-4/R-5/R-6 marked deferred-with-tracking.
- **§9.2 deployment runbook** retained as a `make ship-coder` target (P-016) + release-engineer post-merge action.
- **§10 acceptance checklist** retained, satisfied 3-of-8 in-tree, 5 routed to PR-comment / PR-description / cross-doc / on-Coder.
- **§11 provenance appendix** retained, mirrored in `TRACEABILITY.md` (P-015).

### Folded from F-strict-review

- F's MEDIUM-1 (PRD subclass) elevated to HIGH by probe → P-006 / P-007 R3.
- F's MEDIUM-2 (env-var crash) confirmed by both advocates → P-009 R3.
- F's LOW-1 (`_stdin_error` not in `__init__`) folded into U-007 fix → P-011.
- F's LOW-2 (`n=0` silent break) elevated to MEDIUM by probe → T-012 R3.
- F's NIT-1, NIT-2, NIT-3 captured as D-FOLLOW-007/008 deferrals.

### Folded from invariant probe (NEW vs F)

- INV-005, INV-024, INV-026, INV-028, INV-030 → deferred via D-FOLLOW-004/006/007/009/010 (LOW; maintainer-post-merge).
- INV-011 → folded into P-009 helper if helper clamps; otherwise D-FOLLOW-005.
- INV-015 → T-015 LOW.
- INV-019 → T-013 (NUL-byte round-trip; lands R3).
- INV-023 → T-016 LOW.

---

## §4 Items "rejected" (considered and dropped)

The merge synthesizer considered and rejected the following on the basis of evidence-driven evaluation:

| Considered | Rejected because | Round |
|---|---|---|
| Spec-advocate W-L1 (X-002 18s vs 16s SIGTERM) | A's 18s budget allows for `start()` prelude (file open + Popen fork) before SIGTERM+SIGKILL window; B's 16s ignored prelude. R3-spec withdrew. | R3 |
| Spec-advocate W-L2 (X-003 `<` vs `≤`) | A is strict subset of B; cannot fail when B passes. R3-spec withdrew. | R3 |
| Spec-advocate W-M4 (X-001 commit-order rationale) | `git log --oneline` is newest-first; `526a606` IS oldest = step 1. R3-spec withdrew. | R3 |
| Spec-advocate W-M11 (U-014 8th commit `db8cffe`) | Imports F-strict-review.md into design package; benign. R3-spec withdrew. | R3 |
| Spec-advocate W-M5 (S-002 supersession cross-link) | `fde1431` adds the banner; verified. R2-impl reframed; not contested in R3. | R2 |
| Spec-advocate W-M7 (U-029 pre-merge tests) | CI artefact, not diff artefact; PR-comment with `make test` output sufficient. R2-impl reframed. | R2 |
| Spec-advocate W-M8 (U-017 D-067 CI integration) | Existing `.github/workflows/test.yml` discovers new tests; no new CI step needed. R2-impl reject-in-part. | R2 |
| Spec-advocate W-M9 (U-026 R-4 empty-prompt tracking) | T-006 IS the contract test; tracking via test, not TODO. R2-impl reframed. | R2 |
| Spec-advocate W-M12 (U-018/U-020 PR-creation) | Outside `git diff` scope; human-in-loop `gh pr create` after sign-off. R2-impl reframed. | R2 |
| Spec-advocate W-M13 (A-002 blocking-FD assertion) | R2-impl proposed `assert os.get_blocking(fd)` defensively; nice-to-have but no defect. R3 routes to D-FOLLOW (LOW). | R2 |
| Impl-advocate "U-021 is a category error" | Spec-advocate showed 338 KB Coder repro is the original-bug-validation; impl-advocate conceded R2 and R3. | R2 |
| Impl-advocate "U-024 DEFER tracking is spec's responsibility" | R2-impl conceded with BEAT_2_BACKLOG.md proposal (which lands R3). | R2 |
| Impl-advocate's R3 narrow PRD-only test | Spec-advocate argued for parametric subclass test; routed to P-008 same-PR follow-up commit. Compromise. | R3 |

---

## §5 Validation

### §5.1 Structural integrity

- All 6 artifacts created at their specified paths.
- `merged-output.md` is the headline deliverable; sized in §6.
- All artifacts cross-reference each other: `merged-output.md` → `refactor-plan.md` (P-006..P-016) → `debate-transcript.md` (R-NNN) → `diff-analysis.md` (S/C/X/U/A) → `invariant-probe.md` (INV-NNN) → `F-strict-review.md` (NEW vs F).

### §5.2 Internal references

| From | To | Verified? |
|---|---|---|
| `merged-output.md` §4 (real drift) | `refactor-plan.md` P-NNN | ✓ |
| `merged-output.md` §6 (newly surfaced risks) | `invariant-probe.md` INV-NNN | ✓ |
| `merged-output.md` §8 (vs F) | `F-strict-review.md` MEDIUM/LOW/NIT IDs | ✓ |
| `refactor-plan.md` provenance fields | `diff-analysis.md` S/C/X/U/A IDs + `invariant-probe.md` INV-NNN | ✓ |
| `base-selection.md` coverage-quant | `diff-analysis.md` U-NNN counts | ✓ |
| `base-selection.md` test mutation-kill | `invariant-probe.md` ADDRESSED/UNADDRESSED ratios | ✓ |
| `debate-transcript.md` per-round trajectory | `r1/r2/r3-impl/spec-advocate.md` files | ✓ (section refs) |

### §5.3 Contradiction re-scan

After merge, scanned for residual contradictions in the synthesized output:

- **None found.** All 7 X-NNN contradictions are resolved (3 fixed in R3 via P-NNN; 4 dispute-equivalent or A-corrects-B and retained).
- **U-007 self-contradiction within A** (asymmetric `_stdin_error` defensive read) closed by P-011 (init in `__init__`).
- **Spec self-contradiction (`proc.poll()` typo at §5 row 5)** closed by accepting A's correction (X-005); R3-spec did not contest.

### §5.4 Open conflicts after R3 (unresolved_conflicts count)

Per refactor-plan §"Remaining Disagreements" reconciled:

| Disagreement | Resolution |
|---|---|
| W-H1 enforcement mechanism (CODEOWNERS vs honor-system) | DEFER to repo admin; refactor plan suggests required-status-check post-PR. **Not blocking.** |
| W-M10 telemetry coverage scope (`prompt_bytes` vs `prompt_encode_peak_bytes`) | Routed to D-FOLLOW (Beat-2 telemetry). **Not blocking.** |
| Subclass-test scope (narrow PRD vs parametric) | Both land R3 (P-007 narrow + P-008 parametric). **Resolved.** |
| §4 P-004 spec amendment scope (this-PR vs follow-up) | Same-PR commit per R3-spec demand (P-010). **Resolved.** |
| U-033/U-034 verification | PR-description amendment (D-FOLLOW-003). **Not blocking; pre-merge action.** |

**Final unresolved-after-R3 count: 0** (all open items have a named owner and resolution path; nothing blocks merge except pre-merge actions explicitly listed in `merged-output.md` §9).

---

## §6 Output sizing

| File | Approx size | Key metric |
|---|---|---|
| `base-selection.md` | ~12 KB | Frame: B-as-base; combined score 0.884 vs 0.840 |
| `refactor-plan.md` | ~17 KB | 18 planned changes; P-006..P-016 + T-012..T-016 |
| `merge-log.md` | ~15 KB | (this file) Convergence 0.825; 0 unresolved |
| `merged-output.md` | ~22 KB (target) | Headline deliverable; status YELLOW (merge-ready with 5 in-PR fixes) |
| `return-contract.yaml` | ~1 KB | Contract fields per protocol |
| `debate-transcript.md` | ~18 KB | 3-round transcript with section refs |
| **Total** | **~85 KB** | within target band 80-150 KB |

---

**End of merge-log.md**
