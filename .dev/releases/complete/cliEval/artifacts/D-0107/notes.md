# D-0107 — Notes

## Design notes

1. **Why path (b) over path (a).** DOC-OQ8 names two acceptable
   outcomes; the choice between them is forced by what evidence is
   available at M6 exit. Path (a) requires citing Anthropic-published
   documentation that the `claude` binary advances its internal clock
   when `CLAUDE_FAKE_TIME_OFFSET` is set, or landing a probe eval that
   demonstrates the behaviour. A repository-wide audit (see
   `artifacts/D-0107/evidence.md` §"Repository audit") finds the var
   named only in harness-side comments and prior `decisions.md` rows;
   no Anthropic source has been cited. Probe-eval R&D is out of v1
   scope per the T05.01 frozen E1..E15 set. Without evidence, path (a)
   would be a false attestation; path (b) is the only honest closure.

2. **Why retain `time_offset_sec` at v1 ship instead of stripping it
   immediately.** Three options were considered:
   (a) immediate strip — touch isolation.py / models.py / claude_process.py /
       design-spec in the same commit as the ADR closure;
   (b) deferred strip via tracked follow-up — record the contract
       removal at R7 and land the code change in v1.0.1 / next minor
       cut after v1;
   (c) leave the field indefinitely as documented-deprecated.
   Option (a) was rejected because T06.03 is EXEMPT-tier; the code
   strip touches T02.07 (FR-ISO1) which lands under STRICT-tier review
   (Section 5.3.2). Refactoring isolation.py at the M6 exit gate would
   require a Phase-6 re-checkpoint and risks delaying M6 close.
   Option (c) was rejected because deferring forever leaks a
   dead-by-design env-var contract into v1 release notes. Option (b)
   is the minimal-disruption path: the ADR records the contract
   removal at R7 (sufficient for SC5 / T06.09 to read OQ-8 as
   RESOLVED), and the code strip lands in v1.0.1 under its own STRICT
   review. Step 4 of T06.03 explicitly authorises this routing
   (*"If removed, file follow-up task to strip time_offset_sec from
   HomeIsolation"*).

3. **Why the follow-up artifact lives at
   `artifacts/D-0107-followup-strip-time-offset.md` and not under
   `.dev/tasks/to-do/`.** This release cycle's convention (see
   `artifacts/D-0099-followup-k003-runs.md`) is to file follow-ups as
   sibling artifacts under the parent deliverable's release directory,
   not as RF-task files. The convention keeps the follow-up grep-able
   from the ADR ("see `artifacts/D-0107-followup-...md`") without
   demanding a new RF task ID at M6 exit. When the v1.0.1 cut is
   planned, the follow-up artifact is consumed by a new RF task at
   that time.

4. **Repository audit methodology.** The audit underpinning path (b)
   is a `grep -rn "CLAUDE_FAKE_TIME_OFFSET\|time_offset_sec\|time_offset"`
   over `src/superclaude/cli/eval/` plus a separate sweep of
   `.dev/releases/current/cliEval/` for spec / ADR / OQ references.
   Every hit was classified as either (i) harness-side comment /
   docstring, (ii) `HomeIsolation` field declaration, (iii) `env()`
   emission branch, (iv) spec / ADR row, or (v) callsite. Zero
   callsites set `time_offset_sec` to a non-zero value. Zero
   external Anthropic sources document the env var. Full audit log in
   `artifacts/D-0107/evidence.md`.

5. **What changes if Anthropic later documents the var.** Path (a)
   becomes available retroactively. The ADR closure here is amended
   with an `Outcome:` line citing the new documentation; the strip
   follow-up is either (i) cancelled if discovered before it lands or
   (ii) followed by an immediate re-introduction ADR if discovered
   after. Either way, the cost of removing the layer now is the cost
   of re-adding it later (~30 LOC), so the decision is reversible.

6. **What changes if a future v2 freshness eval needs time mocking.**
   Same outcome — a new ADR records the re-introduction with the
   probe evidence path (a) would have required. The v2 R&D item is
   tracked separately at MIG-003 / DOC-OQ9 follow-up scope (macOS +
   CI), not at this ADR.

## Edge cases considered

- **What if v1 ships before the follow-up strip lands.** The
  retention of `time_offset_sec: int = 0` at v1 ship is intentional;
  v1 callers do not set the field, so the dead branch in
  `HomeIsolation.env()` is unreachable in practice. The follow-up
  artifact records that the v1 release notes name OQ-8 as RESOLVED
  with the env-var contract removed (in spirit, via this ADR) and
  flag the code strip as a v1.0.1 deprecation item.
- **What if a downstream consumer constructs `HomeIsolation(...,
  time_offset_sec=N)` positionally before v1.0.1 lands.** They get
  the historic behaviour (env var emitted on non-zero). The
  follow-up strip plan notes the positional-arg risk and routes
  through a deprecation warning in v1.0.1 before the field removal in
  v1.1 (see `artifacts/D-0107-followup-strip-time-offset.md`).
- **What if the design-spec §8 row is read by a maintainer before the
  follow-up strip edits it.** The R7 ADR is the canonical authority;
  any drift between `decisions.md` §"DOC-OQ8 Closure" and
  `design-spec.md:372` is resolved in favour of the ADR until the
  follow-up strip aligns them. The SC5 OQ-ledger sweep (T06.09) is
  the integrity check.
- **What if RyanW (the named architect for the OPS-001 §B OQ-8 row)
  later prefers path (a).** Reject/revise rule applies: a new
  revision log entry records the reversal; the original R7
  `Resolution:` line stays for audit. Reversal requires the same
  probe evidence path (a) needed originally.

## Validation steps performed

1. Audited every reference to `CLAUDE_FAKE_TIME_OFFSET`,
   `time_offset_sec`, and `time_offset` across `src/superclaude/cli/eval/`
   and confirmed zero non-zero callsites and zero Anthropic-published
   sources (see `artifacts/D-0107/evidence.md` §"Repository audit").
2. Read `decisions.md` §"OQ-2 Resolution" and confirmed the verbatim
   statement *"None of E3 … E15 requires `CLAUDE_FAKE_TIME_OFFSET`."*
3. Confirmed the §B OPS-001 OQ-8 row flipped OPEN → RESOLVED with the
   correct `resolution:` text shape (matching OQ-1 / OQ-7 / OQ-9
   precedents).
4. Confirmed the R5 / R7 update notes correctly enumerate which OQs
   remain DEFERRED (OQ-3, OQ-10) vs RESOLVED (OQ-1, OQ-7, OQ-8, OQ-9).
5. Confirmed the §"DOC-OQ8 Closure" section follows the structural
   template of §"DOC-OQ7 Closure" and §"DOC-OQ9 Closure" (Context →
   Options → Decision → Rationale → Closure → Cross-references →
   Consequences).
6. Confirmed the follow-up artifact path is grep-able from the ADR
   and from the OPS-001 §B OQ-8 row.
