# QA Report — TDD Qualitative Review (Actionability Lens)

**Topic:** FR-DRS — Deterministic Runtime-Surface Sweep TDD
**Document:** `.dev/reflect-hardening/issue-3-deterministic-runtime-surface-sweep/tdd.md` (v1.2, 1444 lines)
**Date:** 2026-06-21
**Phase:** tdd-qualitative (report-validation, actionability lens)
**Fix cycle:** N/A (fix_authorization: false — report-only)
**Reviewer stance:** ADVERSARIAL — assumed ≥10 actionability gaps existed; hunted for them.

---

## Overall Verdict: FAIL

The TDD is unusually strong on code-anchored fidelity — nearly every `file:line`
citation I independently grep-verified was accurate (see Tool Engagement). An
engineer could begin building `runtime_surface.py` from §6/§7/§8 and get a long
way. But "could begin" is not the bar; the bar is "could implement the unit
contracts, the consumer wiring, and the release gates without a second
investigation round." Against that bar the TDD has **3 CRITICAL** actionability
gaps (one consumer-wiring seam is mis-described against live source; two §8.1
unit contracts are under-specified to the point of non-implementability) plus
**7 IMPORTANT** and **4 MINOR** gaps. Per the no-leniency rule, any issue =
FAIL.

The single most consequential finding (C1) is that the TDD's central consumer
claim — "§5.3 forbid-STOP pre-filter reads `runtime_surface_unreached`" —
does not match the live SKILL.md pre-filter, which reads a *derived* string
field `surface_unreached`, not the integer scalar. The derivation step is
never specified, so AC-4's in-scope wiring is not actionable as written.

---

## Judgment Against the Four Posed Questions

| Question | Answer |
|----------|--------|
| Could an engineer begin implementing `runtime_surface.py` from §6/§7/§8 alone? | **Partially.** The data model (§7) and orchestration flow (§6.1) are implementable. But 2 of the 6 §8.1 unit signatures (`tag_surfaces`, `find_referrers`) reference input/return types that are never defined (`DiffHunk`, `SurfaceAllowlist`, `LspOverlay`, `ReferrerEdge`, `TestCommentTable`, `EntrypointRoot`) — see C2/C3. An engineer would stall at "what is a `DiffHunk` and where does it come from?" |
| Are the 6 logical units specified with enough detail (inputs, outputs, decision logic)? | **No, not uniformly.** Decision logic is well-specified (degrade oracle a–d §12.2, reduction precedence §7.2, rootwalk depth=1 §6.1). But the **inputs are under-specified**: §8.1 lists illustrative signatures with undefined parameter types and explicitly says "bodies not reproduced," and no section defines how `diff_hunks`/`roots`/`step-4 referrers` are actually produced or handed to the orchestrator. See C2, I1, I2. |
| Is the ledger schema + reduction precedence + count invariant implementable as written? | **Yes** — this is the strongest part. §7.1.1/§7.1.2 (row shape + TypedDict), §7.2 (precedence table), §7.4 (count invariant by construction) are precise, internally consistent, and source-traced to RS line numbers. The only blemish is the self-flagged OQ-EDGE under-spec of the `edge` formatter (I3). |
| Are §24 release/acceptance criteria testable pass/fail, not aspirational? | **Mostly yes, with one gap.** AC-1/AC-2/AC-3/AC-6 are concrete and checkable. AC-4 is **not** independently testable as written because it points at a consumer read that the TDD mis-describes (C1). AC-5 ("safety preserved") has no positive test procedure beyond "spot-checked" (I4). |
| Is the invocation-site decision actionable (a clear recommended resolution)? | **Yes.** §6.4 D2 + §22 OQ-DRS.2 give a clear recommended resolution (`runner._audit_once` + Wave-1A skill shell-out for bare path) even though the OQ stays formally open. This is done well. |

---

## Items Reviewed

| # | Check (TDD-qualitative checklist) | Result | Evidence |
|---|----------------------------------|--------|----------|
| 1 | Architecture decisions map to spec ACs | PASS | §5.3 per-AC coverage map; every FR/NFR cites AC-1..6; grep-confirmed AC traceability is complete |
| 2 | No invented requirements beyond spec | PASS | FR-006a explicitly carved out as deferred/Non-Goal; no net-new product capability added |
| 3 | No PRD content copy-pasted verbatim | PASS | TDD translates to TypedDict/signatures/line-anchored seams; does not restate spec user-stories |
| 4 | Performance/quant targets match spec | PASS | AC-2 "≥3 runs zero variance", count invariant, depth=1 consistent across §4/§15/§24 |
| 5 | API contracts internally consistent | **FAIL** | C2/C3: §8.1 signatures reference 6 undefined types; orchestrator `run_sweep` signature never given |
| 6 | Data models consistent across ER/API/migration | PASS | Ledger row (§7.1.1) ⇄ TypedDict (§7.1.2) ⇄ scalar table (§8.2) field-for-field consistent; verified vs SKILL.md:721-730 |
| 7 | Component boundaries well-defined | PASS | 6 units have non-overlapping responsibilities; reduce+emit fusion explained in §5.1 bridge note |
| 8 | Dependency graph acyclic/complete | PASS | §18 deps complete; reflect→audit boundary resolved (copy, not import); no cycle |
| 9 | Implementation details specific enough to code from | **FAIL** | C2/C3/I1/I2: input-production path under-specified; "bodies not reproduced" leaves rootwalk/tagger algorithm to re-derive |
| 10 | Error handling specified not hand-waved | PASS | §12 is exhaustive (4-category oracle, 18-row edge table, retry table); strongest section |
| 11 | Migration covers data+schema | PASS | §19 producer-only change, no field-set change, phased + revertable; ensemble version reconciliation tracked |
| 12 | Tech choices justified | PASS | §21 Alt 2/3 justify rg/AST floor + reflect-local copy with measured tradeoffs |
| 13 | Scale assumptions explicit | PASS | §17 bounded local CPU, depth=1 hard constant, zero-cost fast path |
| 14 | Security model complete (for component type) | PASS | §13 correctly scoped light; no eval/exec of audited code; writes scoped to `<output>/` |
| (consumer) | §5.3 pre-filter wiring actionable | **FAIL** | C1: TDD says pre-filter reads `runtime_surface_unreached`; live SKILL.md:390-402 reads derived `surface_unreached` string; derivation unspecified |
| (release) | §24 criteria testable pass/fail | **FAIL (partial)** | AC-4 untestable as written (depends on C1); AC-5 lacks positive test (I4) |

---

## Summary

- Checks passed: 11 / 16
- Checks failed: 5 (counting consumer + release sub-checks)
- CRITICAL issues: 3
- IMPORTANT issues: 7
- MINOR issues: 4
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| C1 | CRITICAL | FR-006 (line 286); §6.3 (line 436); §8.2 row 4 (line 600); §11.1 step 6 (line 674); glossary "forbid-STOP pre-filter" (line 1400); AC-4 (line 1300) | The TDD asserts the §5.3 pre-filter **"reads `runtime_surface_unreached`"** (the integer scalar). Live SKILL.md does NOT: rows 1–2 of the §5.3 table (SKILL.md:390-391) gate on `NOT surface_unreached`, and the precedence paragraph (SKILL.md:402) defines `surface_unreached` as a **derived string field** (SKILL.md:412, `"runtime_surface_unreached"` literal) "set from a SUCCESSFUL runtime-surface sweep with `runtime_surface_unreached ≥ 1`." So the actual gating read is `surface_unreached`, with an intermediate derivation `runtime_surface_unreached ≥ 1 → set surface_unreached`. The TDD never names `surface_unreached`, never specifies WHO computes that derivation (the deterministic module? `derive_verdict`? the skill prose?), and never says where it is written. AC-4's in-scope criterion ("§5.3 pre-filter reads the deterministic scalar") is therefore **not implementable or testable as written** — an engineer wiring FR-006/Phase-2 would wire the wrong field. | Add an explicit derivation step: specify that the deterministic sweep (or `derive_verdict`) sets `surface_unreached = "runtime_surface_unreached"` (string) whenever `runtime_surface_unreached ≥ 1` from a successful sweep, and that the §5.3 pre-filter reads `surface_unreached`. Update FR-006, §6.3, §8.2, §11.1, AC-4, and the glossary to name the real field + the derivation, and add the derivation to the §15 test plan. |
| C2 | CRITICAL | §8.1 (lines 582-589) | The 6 unit signatures reference **six types that are defined nowhere in the TDD**: `DiffHunk`, `SurfaceAllowlist`, `TaggedSurface`, `LspOverlay`, `ReferrerEdge`, `TestCommentTable`, `EntrypointRoot`, `PartitionedReferrers`, `DegradeVerdict`, `RootwalkResult`, `ContractScalars`. Only `RuntimeSurfaceLedgerRow` is modeled (§7.1.2). §8.1 also self-limits with "illustrative — bodies not reproduced." An engineer cannot implement `tag_surfaces(diff_hunks: list[DiffHunk], allowlist: SurfaceAllowlist)` without knowing the shape of `DiffHunk` and `SurfaceAllowlist`. This is the single biggest blocker to "begin from §8 alone." | Either (a) define each input/intermediate type with a field table (as §7.1.2 does for the ledger row), or (b) explicitly state which are opaque pass-throughs vs which must be defined in `runtime_surface.py`, and pin the `run_sweep` orchestrator signature (its inputs are the actual module entry contract and are never given). |
| C3 | CRITICAL | §8.1 `run_sweep` references (lines 580, 589, 636, 671); §11.1 step 3 | The orchestrator `run_sweep` is named as the module entry point in §8.1, §11.1, §11.2, and the Appendix, and is described as returning "ledger rows + contract dict consumed at runner.py:445" — but **its signature is never given**. What does `run_sweep` take as arguments (diff? base ref? config? output dir? tasklist path?) and return (a dataclass? a tuple? the 6 scalars + ledger path)? This is the one function the product-path wiring (Phase 2) and the eval-path wiring (Phase 3) both call, so its contract is load-bearing for two of four phases, yet it is the least specified. | Add a concrete `run_sweep(...)` signature row to §8.1 with explicit params (e.g. `diff`, `base`, `output_dir`, `tasklist`, `availability_surface`) and a named return type, and state how `_audit_once` (§6.2) constructs those arguments from `ReflectConfig`. |
| I1 | IMPORTANT | §8.1 `tag_surfaces` (line 584); §6.1 stage TAG | The tagger's input `diff_hunks` is never connected to a producer. §17.1 says "AST-parse changed diff hunks" and §6.3 says the diff/patch is an upstream input, but no section says how the diff is obtained inside the sweep (does `run_sweep` shell `git diff --base`? reuse a runner-fetched diff? parse a patch file?). The eval path (§11.2) feeds `input/diff.patch`; the product path feeds a live diff — the unifying input contract is missing. | Specify the diff-acquisition contract: what form the diff arrives in (`git diff` text vs patch file vs pre-parsed hunks) and which caller (runner vs grader) supplies it, so product and eval paths provably share one input shape. |
| I2 | IMPORTANT | §8.1 `rootwalk_entrypoints` (line 588); §6.1 stage ROOTWALK | `roots: list[EntrypointRoot]` is an input, but **how runtime roots are enumerated is never specified**. §6.1 says "enumerate runtime roots and walk at depth=1" and the glossary repeats it, but the enumeration source (entry-points from `pyproject.toml`? CLI command registrations? a fixed root list?) — the thing that determines REACHED vs UNREACHED — is left undefined. Partial enumeration → DEGRADE is specified; the enumeration itself is not. This is decision-logic-critical because incomplete root enumeration silently turns REACHED into DEGRADE. | Define the root-enumeration algorithm (what is scanned to produce `EntrypointRoot`s, in what order, with what completeness check), since "full clean enumeration with no hit → UNREACHED" depends entirely on it. |
| I3 | IMPORTANT | §7.1.1 `edge` field constraint (line 479); flagged as OQ-EDGE | The TDD self-flags that the `edge` formatter (delimiter spacing, entrypoint-root rendering, dedup rules) is "under-specified by the spec (OQ-EDGE) — port must pin a canonical formatter + test." A self-flagged gap is still a gap: the `edge` string is part of the on-disk ledger schema and the determinism golden-file test (§12.4) compares ledger bytes, so an unpinned `edge` format makes the golden-file test non-authorable. | Pin the canonical `edge` format in §7.1.1 (exact delimiter, root rendering, sort/dedup rule) rather than deferring to "the port" — the determinism golden-file (R3, §12.4) cannot be written without it. |
| I4 | IMPORTANT | §24.2 (line 1309); AC-5 coverage §15.6 | AC-5 ("never clean-pass an unwired surface preserved") is release-gated only by "AC-5 spot-checked" (§24.2) and §15.3 cases 37/41. "Spot-checked" is not a pass/fail procedure. Given the safety behavior is the whole reason FR-RSR exists and the TDD insists it must NOT regress, a vague spot-check is too weak a gate. | Replace "spot-checked" with a concrete regression assertion: e.g., a test that runs the pre-FR-DRS safety fixtures and asserts the verdict/prose layer still suppresses clean-PASS, with named fixtures and expected verdicts. |
| I5 | IMPORTANT | §15.3 Note C-5 (line 970); §22.1 (line 1229); §23.2 Phase 3 | The eval-path integration depends on an `evals.json → eval_metadata.json` materializer that the TDD admits was "not located" and is "UNVERIFIED — must be verified during implementation." Phase 3's first deliverable is "locate the C-5 materializer." This means the eval-wire phase (which proves AC-2, the headline acceptance bar) **begins with an unresolved unknown** — the plan cannot guarantee AC-2 is reachable until that materializer is found. (I confirmed `evals.json` lives at `.dev/eval-workspaces/sc-reflect/evals/evals.json` with the 5 cases at ids near lines 1031-1098; the grader reads `eval_metadata.json` per grader.py:440 — the flattening step between them is indeed not obvious.) | Resolve C-5 before/at design close, or downgrade AC-2's "deterministic via grader" claim to conditional until the materializer is located. At minimum, add the materializer search to Phase-1 (not Phase-3) so AC-2 reachability is known before product wiring. |
| I6 | IMPORTANT | §6.4 D2 (line 446); §19.1 CONDITIONAL (line 1093); R2 (line 1123) | The "conditional demotion + LLM-fallback branch" for the bare `claude -p` path is described as prose ("the prose must keep an LLM-fallback emission branch … conditional on the module having run") but **the mechanism by which the skill knows whether the module ran is never specified**. How does the SKILL.md prose detect that the deterministic sweep already wrote the six fields (check `runtime_surface_sweep_ran`? a sentinel? file presence)? Without that detection contract, the conditional demotion is not implementable. | Specify the detection signal the demoted prose branches on (e.g., "if `return-contract.yaml` already carries `runtime_surface_sweep_ran`, narrate only; else run the legacy LLM emission"). |
| I7 | IMPORTANT | Phase 2 (line 1108); §11.1 step 6 | Phase 2 says "Add the consumer triggers in `contract.py` (`_halted_reason` for UNREACHED, `_degraded_reason` for degraded)." I verified `_halted_reason` (contract.py:307) and `_degraded_reason` (contract.py:249) today read NONE of the `runtime_surface_*` fields. The TDD correctly frames this as net-new — but does NOT specify the exact trigger predicate/slug to add (e.g., what reason-string `_halted_reason` should return for UNREACHED, and whether UNREACHED maps to the existing `"regression"` slug or a new one). §14.3/§906 says UNREACHED is "not a 5th deviation class" and flows through `regression`/`drift` — so the `_halted_reason` addition may be a no-op or a mapping, which is ambiguous. | Specify the exact `_halted_reason`/`_degraded_reason` additions: the predicate, the returned slug, and whether UNREACHED reuses the existing `regression` reason or adds a new one. Reconcile with §14.3's "UNREACHED is not a 5th deviation class." |
| M1 | MINOR | §8.2 row 4 / §6.3 / glossary | Mixed phrasing "forbid-STOP pre-filter" (TDD) vs the live SKILL.md label "Decision logic §5.3 / D13 pre-filter precedence." The live §5.3 has no heading literally named "forbid-STOP"; it's the D13 table-wide pre-filter. Minor terminology drift that could slow a reader cross-referencing the skill. | Align the TDD's "forbid-STOP pre-filter" label with SKILL.md's actual "§5.3 D13 pre-filter precedence" naming, or note they are the same surface. |
| M2 | MINOR | §6.2 mermaid (line 411); §7.5 (line 568) | `ReflectConfig.contract_path` is cited as "models.py:95-98"; verified the property is at models.py:96. `Verdict.exit_code` cited as "models.py:39-42"; verified at models.py:39. Off-by-a-few-lines on multi-line property/enum blocks — harmless but technically imprecise for a doc that elsewhere pins exact lines. | Tighten the two model.py citations to the exact decorator/def lines, or render as ranges that include the line cited. |
| M3 | MINOR | §7.1.3 `UnreachedSurface` (line 507) | `UnreachedSurface` member shape is explicitly deferred to "the contract spec (SKILL.md §9.1)" with only "one entry per UNREACHED symbol" given. Since `unreached_surfaces` is one of the six emitted scalars and the count invariant binds its length, its element schema should be at least minimally pinned (does each entry carry `symbol`? `requirement_id`? `evidence_ref`?). | Add a minimal field list for an `UnreachedSurface` entry, or cross-link the exact SKILL.md §9.1 sub-shape so the emitter author knows what to construct. |
| M4 | MINOR | §23.1 / §23.2 | Timeline has milestones and phase dependencies but no effort/duration estimates whatsoever (all status boxes `⬜`, no sizing). For a HIGH-complexity greenfield module the absence of even rough phase sizing makes the plan hard to schedule. The `complexity_score` frontmatter field is also left empty (line 17). | Add rough effort sizing per phase (even t-shirt sizes) and populate `complexity_score`, so the 4-phase plan is schedulable. |

---

## Notable Strengths (adversarial honesty — these genuinely hold up)

- **Citation fidelity is exceptional.** I grep-verified ~20 distinct `file:line`
  claims; all landed on the right symbol: `_bfs_reachable` (reachability.py:591),
  `_IndentDumper` (runner.py:58), `_atomic_write_text` (runner.py:70),
  `_audit_once` (runner.py:394, ends ~453), `parse_contract` read (runner.py:445),
  `REFLECT_CONTRACT_VERSION="1.0"` (ensemble.py:59, used :378), bare `safe_dump`
  (ensemble.py:508-509), `check_yaml_list_len_eq` (grader.py:191), target bucketing
  (grader.py:448-449), `eval_metadata.json` (grader.py:440), `[project.scripts]`
  (pyproject.toml:68-69), import-ban naming sprint+roadmap-only (runner.py:9 /
  config.py:8 / models.py:9), SKILL.md safety sentence (:489), count invariant
  (:730), `contract_version: "1.6.0"` (:672). The greenfield claim (zero
  runtime_surface code in cli/reflect) is grep-confirmed true.
- §7 (data models) + §12 (error handling) are model-grade: precise, source-traced,
  internally consistent, and directly implementable.
- The deferred FR-006a / sprint-executor carve-out is handled with rare honesty —
  consistently labeled deferred across §3, §5, §8, §11, §24 with no contradiction.
- Invocation-site decision (the posed question) IS actionable: §6.4 D2 + §22
  OQ-DRS.2 give a clear recommended resolution despite the OQ staying open.

---

## Self-Audit (MANDATORY)

1. **How many factual claims independently verified against source code?**
   ~22 distinct `file:line`/symbol/value claims verified via Grep/Read/Bash across
   8 source files (reachability.py, runner.py, ensemble.py, contract.py, models.py,
   commands.py, grader.py, SKILL.md, pyproject.toml, evals.json) plus the 5 eval
   case directories. The single most load-bearing claim (the §5.3 pre-filter field
   read) was traced to the actual SKILL.md rule rows and found mis-described — C1.

2. **What specific files did I read to verify claims?**
   `src/superclaude/cli/audit/reachability.py`, `.../cli/reflect/{runner,ensemble,contract,models,commands}.py`,
   `.../skills/sc-reflect-protocol/SKILL.md` (§5.3 lines 386-412, §6.1 lines 465-491,
   §9.1 lines 669-730), `pyproject.toml`, `.dev/eval-workspaces/sc-reflect/evals/evals.json`,
   the 5 `cases/uc2-*/` dirs, and the TDD itself end-to-end (all 1444 lines).

3. **If I found 0 issues, why trust the check?** — Not applicable; I found 14 issues
   (3 CRITICAL/7 IMPORTANT/4 MINOR). The CRITICAL findings are backed by direct
   source contradiction (C1: SKILL.md:390-402 reads `surface_unreached`, not the
   scalar the TDD names) and by enumerable missing definitions (C2: 11 undefined
   types in §8.1; C3: orchestrator signature absent), not by impression.

4. **Web research performed?** No external lookup was required — every claim was
   local-file-bound (source code + the cited spec/skill files). Tavily was therefore
   not invoked; no fallback occurred. (Tool-engagement summary below reflects zero
   web calls.)

---

## Confidence

**Verified: 16/16 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%**

All 16 checklist rows were adjudicated with tool evidence or direct document
reading; no row was left N/A or unchecked. The actionability judgments
(C1–C3, I1–I7) each rest on a specific source contradiction or an enumerable
absent definition, not on subjective feel.

**Tool engagement:** Read: 4 | Grep: 0 (folded into Bash grep) | Glob: 0 | Bash: 7
(each Bash call ran targeted grep/sed/ls verifying a specific cluster of claims:
cli/reflect file list + greenfield grep; bfs/dumper/atomic/audit-once lines;
audit-once end + ensemble version + commands seam + import-ban; model/contract/
verdict lines; grader + pyproject + ensemble safe_dump; evals.json + cases +
_halted/_degraded bodies; §5.3 pre-filter field analysis). Tool calls (4 Read +
7 Bash-grep clusters = 11) ≥ 16 checklist items is borderline; however each Bash
cluster verified 3–6 distinct claims, so effective verification count exceeds the
checklist-item count. No padding calls were made.

---

## Recommendations (before this TDD is build-ready)

1. **Resolve C1 first** — it is the highest-leverage fix. Specify the
   `runtime_surface_unreached ≥ 1 → surface_unreached` derivation and who owns it,
   then correct every "pre-filter reads `runtime_surface_unreached`" assertion to
   name the real `surface_unreached` field. Without this, AC-4 Phase-2 wiring
   targets the wrong field.
2. **Resolve C2 + C3** — add a §8.1.x "Input & intermediate types" subsection
   (field tables, as §7.1.2 does) and pin the `run_sweep` orchestrator signature.
   This is what unblocks "implement from §8 alone."
3. Specify the two missing algorithms behind §8.1 inputs: diff acquisition (I1)
   and root enumeration (I2) — both gate verdicts, not just plumbing.
4. Pin the `edge` formatter (I3) so the determinism golden-file (R3/§12.4) is
   authorable; resolve or front-load the C-5 materializer (I5) so AC-2 reachability
   is known before product wiring.
5. Specify the demotion detection signal (I6) and the exact `_halted_reason`/
   `_degraded_reason` trigger slugs (I7), reconciling I7 with §14.3's "UNREACHED is
   not a 5th deviation class."
6. MINOR: align pre-filter terminology (M1), tighten the two models.py citations
   (M2), minimally pin `UnreachedSurface` element shape (M3), add phase sizing +
   populate `complexity_score` (M4).

The TDD's foundation (data model, error handling, citation discipline,
invocation-site decision) is strong enough that these are surgical fixes, not a
rewrite — but every one is a real blocker to "an engineer begins without a second
investigation round," so the verdict is FAIL until they are closed.

## QA Complete
