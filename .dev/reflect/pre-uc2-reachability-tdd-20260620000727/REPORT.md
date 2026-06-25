# Reflect REPORT — UC-1 (pre-execution) coverage/best-practice audit

**Mode:** UC-1 (pre) · **Tier reached:** 2 (`--depth deep` hard-override) · **Calibrated confidence:** 0.91
**Spec (source of truth):** `.dev/reflect-hardening/issue-1-uc2-reachability/spec.md`
**Artifact under review (the "tasklist/strategy"):** `.dev/reflect-hardening/issue-1-uc2-reachability/tdd.md`
**Ensemble:** 3 heterogeneous reviewers (analyzer/sonnet, qa/haiku, architect/opus) + adversarial merge · convergence 0.88

> The TDD was authored in this same session by the orchestrator, so single-agent self-review would be
> structurally biased (the exact failure mode §1 of the protocol exists to prevent). This audit was therefore
> run through 3 independent reviewers on different model classes, each grounding directly in the on-disk files.

---

## Verdict

**PASS / status: success.** The TDD faithfully covers its driving spec (coverage **0.93**, 42/45 requirements;
no MISSING items, 3 minor PARTIAL traceability gaps) and **all 7 load-bearing invariants are carried verbatim**,
including the two the prompt singled out. Citations are accurate — the architect reviewer independently re-Read
every `SKILL.md:NNN` / `grader.py:NNN` / `reviewer-spec.md:NN` / `pyproject.toml` reference against the real
files and **zero resolved falsely**.

**Headline finding (highest value):** the two apparent TDD↔spec discrepancies are cases where **the TDD is *more
correct* than the spec** — it silently fixes two internal contradictions in `spec.md` itself. That is good
engineering but should be *annotated* for traceability, and the **spec defects should be fixed too**.

---

## Coverage matrix summary (Wave 1B)

| Bucket | Covered | Notes |
|--------|---------|-------|
| FR-RSR.1 … FR-RSR.10 | 10/10 COVERED | all sub-acceptance-criteria represented (FR-map §5.1 + detailed §6.4/§7/§11/§12/§15) |
| NFR-RSR.1 … NFR-RSR.6 | 6/6 COVERED | §5.2 table + §17 budgets + §12.3 + §13.2 |
| Key Design Decisions (spec §2.1) | 10/11 (1 PARTIAL) | D1–D10 map 1:1; spec's "downstream rollback coupling (Newman)" decision covered as OQ-RSR.5/§3.3/risk, not as a decision-table row |
| Contract fields + ledger schema (spec §4.5) | 7/7 COVERED | all 6 fields + `RuntimeSurfaceLedgerRow` + `contract_version 1.6.0` in §7.1 |
| Open Questions OQ-RSR.1–5 | 5/5 COVERED | §22 |
| Worked scenarios (spec §2.3) | 2/2 COVERED | §11.1 / §11.2 Gherkin |
| New/modified file inventory (spec §4.1/§4.2) | PARTIAL ×2 | see F4/F5 below |
| **Total** | **42/45 = 0.93** | above the 0.90 floor; 0 MISSING |

---

## Findings (deviation register)

### F1 — MED — TDD corrects the spec's `runtime_surface_unreached` count semantics without flagging the override

- **Evidence:** TDD §7.1 (`tdd.md:443`, `:476–479`) + glossary (`tdd.md:1059`) define `runtime_surface_unreached`
  as a count of **SYMBOLS** (reduced per-symbol verdict). The driving spec's §4.5 code-comment
  (`spec.md:613`) says **"count of UNREACHED edges"**. **Verified by re-Read.**
- **Why the TDD is right, not wrong:** the spec is *internally contradictory* — its own FR-RSR.2 prose and
  acceptance criteria (`spec.md:296–301`, `:312–313`) state "counts **symbols**… never an edge count" and make
  `len(unreached_surfaces) == runtime_surface_unreached` an invariant. The TDD aligned with the authoritative
  prose. (`spec.md:614`'s `runtime_surface_degraded` comment has the same "≥1 edge" wording — same latent defect.)
- **Classification:** Necessary deviation (the TDD had to pick one reading; it picked the correct, invariant-preserving one).
- **Recommendation:** (a) add a one-line note in TDD §7.1 — *"corrects spec §4.5 comment (edges→symbols) per FR-RSR.2 prose"*;
  (b) **fix the spec** — `spec.md:613` (and the §4.5 narrative) should read "count of UNREACHED **symbols**".

### F2 — LOW — `requirement_id` nullability tightens the spec, unflagged

- **Evidence:** TDD makes `UnreachedSurface.requirement_id` and `RuntimeSurfaceLedgerRow.requirement_id`
  `str | None` (`tdd.md:448`, `:459`); spec §4.5 (`spec.md:618`, `:633`) types them `str`.
- **Why the TDD is right:** the symbol-anchored invariant (FR-RSR.1, `spec.md:254–262`) *mandates* a
  `requirement_id: null` path. The spec's TypedDict is again inconsistent with its own prose.
- **Recommendation:** annotate the override in TDD §7.1; fix the spec TypedDicts to `str | None`.

### F3 — LOW — Key-Design-Decision traceability gap

- The spec §2.1 decision "Downstream rollback coupling (Newman)" (`spec.md:145`) is covered in the TDD only as
  OQ-RSR.5 (§22) + §3.3 + the §20 risk table, not as a §6.4 decision row. Substance is present; the 1:1
  decision-table mapping is not. **Recommendation:** add a D12 row mirroring the spec decision (accept the
  rollback coupling) for clean traceability.

### F4 — LOW — runtime ledger artifact missing from the file inventory

- TDD §18.2 "new files" omits `<output>/artifacts/runtime-surface-ledger.yaml` (spec §4.1 lists it). It is fully
  covered as a data model in §7.1/§7.3, so this is inventory-completeness only. **Recommendation:** add a row
  (marked "runtime artifact, per-run") to §18.2 for implementer checklist completeness.

### F5 — LOW — falsifier-suite modified-file row absent from §18.2

- Spec §4.2 lists a `.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/…` modification (promote/author the
  active companion). TDD §18.2 lists `grader.py` but not that row; FR-RSR.10/§15.2 cover the *behavior*
  (existing skeletons stay green, companions in MAIN `evals/`). **Recommendation:** add the row, or a one-line
  note clarifying the spec's headline-promotion lands in `evals/` per FR-RSR.10's "main cases primary".

### F6 — LOW (cosmetic) — line-count citation

- TDD states "SKILL.md (1855 lines)" (`tdd.md:72`); `wc -l` reports 1854 (the Read tool reports 1855 — the
  difference is a trailing-newline artifact). Cosmetic; every line-number citation still resolves. **Recommendation:**
  soften to "~1855 lines" or drop the count.

---

## What the audit explicitly confirmed (the load-bearing invariants — all PASS)

1. **Symbol-anchored tagger (NOT requirement-anchored)** — `tdd.md:147–149`, `:292–300` carry it as the #1
   non-negotiable invariant, incl. `requirement_id: null` + Drift mapping. No contradiction anywhere. ✅
2. **Degrade oracle defaults dynamic/registry/decorator/reflection/`[project.scripts]` → DEGRADE → §10.6
   Grounding Gap, never Regression** — `tdd.md:150–153`, `:302–307`, D5, §12.3, risk table, both Gherkins. ✅
3. **Per-edge ledger / per-symbol counts / `DEGRADE > UNREACHED > REACHED` reduction / count invariant** —
   `tdd.md:467–479`. ✅
4. **Regression-counter hygiene** (increment only `deviation_count_by_class.regression`, never
   `verification_regressions_detected`) — D8 `tdd.md:419`. ✅
5. **Degrade-only runs do NOT force Tier 2** (trigger is `runtime_surface_unreached ≥ 1`) — D11 `tdd.md:422`. ✅
6. **Eval falsifiability** (active headline w/ real fixtures, FAIL-pre/PASS-post; 4 MAIN companions; skeletons
   green) — `tdd.md:743–758`; grader assertion types `regex_absent`/`yaml_field`/`falsifier_skeleton_present`
   confirmed present in `grader.py`. ✅
7. **Mandatory entrypoint-rootwalk before any UNREACHED; partial enumeration → DEGRADE** — D4 `tdd.md:415`,
   `:634`, `:646`. ✅

---

## Recommended next move (audit-first — no edits made)

This was an audit (`--remediate` not set); no files were changed. The findings are small and the TDD is
ship-quality as-is. The single highest-value action is to **fix the spec's two internal defects** (F1/F2) so the
spec and TDD agree, then annotate the TDD overrides. Paste-ready remediation prompt:

```
Apply reflect findings F1–F5 to .dev/reflect-hardening/issue-1-uc2-reachability/ :
1. Fix spec.md:613 + :614 §4.5 comments: "UNREACHED edges"→"UNREACHED symbols (reduced per-symbol verdict)" and align the degraded comment; fix spec §4.5 TypedDict requirement_id: str → str | None (both UnreachedSurface and RuntimeSurfaceLedgerRow), per the spec's own FR-RSR.2/FR-RSR.1 prose.
2. In tdd.md §7.1, add a one-line note on each override ("corrects spec §4.5 comment per FR-RSR.2/.1 prose").
3. Add tdd.md §6.4 decision row D12 mirroring spec's "downstream rollback coupling (Newman)" decision.
4. Add the runtime-surface-ledger.yaml (runtime artifact) and falsifier-suite promotion rows to tdd.md §18.2.
5. Soften the "1855 lines" count in tdd.md:72.
Edit src/superclaude only is N/A here (these are .dev/ design docs); UV only if any script runs.
```

**Caveat (evidence-validator note, §11.2):** this run is a zero-citation-drop pass, which the protocol treats as
a *flag, not a clean bill*. The mitigation here is that drops are genuinely zero because the architect reviewer
re-Read every citation against the real source — and the audit still surfaced 6 findings (one MED), so it did not
rubber-stamp.
