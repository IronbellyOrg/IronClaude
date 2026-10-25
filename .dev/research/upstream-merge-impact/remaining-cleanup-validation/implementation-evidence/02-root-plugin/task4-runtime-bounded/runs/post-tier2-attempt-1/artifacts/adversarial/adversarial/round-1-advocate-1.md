<!-- Round 1 advocate for Variant 1 (analyzer). Task worker: general-purpose, requested model opus; agentId aa7f516d55a38acc3. Persisted verbatim by the protocol driver. -->
**Advocate brief: Variant 1 (analyzer card), Round 1**

## Position summary
Variant 1 reaches the same verdict as Variant 2: no deviations in any of the four classes, R-001 and R-002 adherent on a static reading, R-003 unresolved, so `partial` + `needs_human_decision`. Variant 1 is better on the points that decide whether the verdict can be trusted. It separates its grounding gaps by how each one gets resolved. It is more careful about what a selected-input snapshot can prove. Its confidence is split by scope. It also avoids a probable technical error in Variant 2's import-path remediation. Variant 1 loses on schema conformance and on two classification boundaries (X-001, X-003), and I concede both below.

## Steelman of Variant 2
At its strongest, Variant 2 is the acceptance-oriented card: an empty ledger is not sign-off. Its opening verdict (V2:11) and its "ledger-true and acceptance-false" challenge (V2:43) make that hard to misread. What it gets right:
- **Grounding-gaps format.** It uses the taxonomy's byte-exact grounding-gaps schema (V2:49-62 against `deviation-taxonomy.md:140-147`), including `decision_needed_by_user`.
- **Precedence walk.** It walks precedence explicitly (V2:19) and sets `regression_present: false` with stated reasons (V2:72). This matches `deviation-taxonomy.md:103`, where only Regression-mapped rows set that flag.
- **Drift boundary.** It reads Drift correctly. Drift needs "Diff hunk does NOT map to any tasklist item" (`deviation-taxonomy.md:62`), and T-103 is a task without a hunk, not a hunk without a task (V2:64).
- **Sibling-gap rule.** It reads the correctness-gap channel correctly. That channel needs two sibling symbols that disagree (`deviation-taxonomy.md:161,167`), and `greet` has no sibling (V2:81,84).
- **Coverage table.** F-001..F-004 gives a citation chain of spec, task, diff and source for each requirement (V2:25-28).
- **Body range.** Its patch body range `changes.patch:6-9` is exact: line 5 is `@@ -0,0 +1,4 @@` (`changes.patch:5`).

## Strengths claimed (Variant 1)
1. **The gaps are split by how they get resolved (C-001).**
   - GG-1 is provenance: T-103 is claimed at `completed.md:8` but has no hunk (`task-to-diff-map.md:11,19`). It is closed by widening the diff scope or by a task log.
   - GG-2 is execution: no verification run (`task-to-diff-map.md:31-33`). It is closed by a pytest exit code.
   - These two can be resolved independently and owe different evidence. Variant 2's first row (V2:50-55) merges them into one `hunk_ref`. A pytest exit 0 would then "close it" (V2:52) while provenance stays open, so one row ends up half-resolved.
   - Variant 2's second row (V2:56-61) is close to a verbatim copy of T1's second gap (`t1-card.md:42-47`). It adds no independent analysis. V1 already records "No task log was supplied" inside GG-1 (V1:22).
2. **Evidence calibration on file absence (X-002, U-002).**
   - V1:32-36 notes that the snapshot holds selected inputs only. The glob confirms exactly 8 files: the 5 core files plus 3 `__run_evidence__` files.
   - So the absence of `src/__init__.py`, conftest or pyproject is true of the snapshot and unknown for the live project. "Grounded for file absence" (`t1-card.md:58`) overreaches.
   - Variant 2 tags the missing config files as "Grounded … (snapshot file list)" (V2:80). It then uses that absence to predict a live collection failure (V2:45, :80, rec 3 at :90). That is an inference built on an absence the snapshot cannot establish for the live root.
3. **Metric blind spot (U-001).** V1:30 points out that `S_dev_density = 0/1` (`task-to-diff-map.md:25`) counts only hunks that exist. It therefore cannot see T-103, the one place a deviation could hide. Variant 2 says acceptance is not 100% (V2:73) but never explains why the metric is structurally blind.
4. **Scoped confidence (C-006).** V1:74 gives 0.8 for `src/greeting.py` and about 0.5 for the whole change. The two levels of evidence really are different: patch/disk identity is grounded, while R-003 has no execution or provenance. Variant 2's single 0.76 blends them and sits above T1's 0.72 (`t1-card.md:74`) despite the same gaps.
5. **No incorrect remediation claim (C-004).** V1's recommendation (V1:65) is the minimal, correct one: run both invocations and read the exit codes against `deviation-taxonomy.md:107-113`. See Weakness 1 for why Variant 2's extra claim is probably wrong.
6. **Citations for R-001/R-002 are exact.** `changes.patch:7-9` (V1:50) covers the guard (`:7-8`) and the return (`:9`), the same as `task-to-diff-map.md:17-18`.

## Weaknesses identified in Variant 2
1. **The rejection of T1 recommendation 3 is probably technically wrong (C-004, U-004, which the diff-analysis rated High value).**
   - V2:45 says `tests/__init__.py` "does not put the project root on `sys.path`."
   - Under pytest's default `prepend` import mode, a test module inside a package causes pytest to insert the first ancestor directory without `__init__.py` into `sys.path`. With `tests/__init__.py` present, that directory is the project root, so `from src.greeting import greet` (`tests/test_greeting.py:1`) resolves, with `src` as a namespace package.
   - Without it, pytest inserts `tests/`, and the import fails. So T1 recommendation 3 (`t1-card.md:69`) is a valid fix, and Variant 2's "Do not treat `tests/__init__.py` as that fix" (V2:90) is likely wrong.
   - Caveat: this rests on documented pytest behaviour, not on anything in the snapshot. Tag it [INFERRED]. Variant 2's `pythonpath = .` alternative is also valid, but only on pytest 7+.
2. **A falsified factual claim.** "`changes.patch` is 10 lines" (V2:44). A Read of the snapshot shows 9 lines (`changes.patch:1-9`). The card uses this claim to correct T1, so a correction carries a new error.
3. **An over-strong grounding tag** (V2:80). See Strength 2.
4. **Merged gap row** (V2:50-55). See Strength 1. It mixes two evidence needs with different owners and verifiers into one `decision_needed_by_user: true` row.
5. **Confidence is not scoped** (V2:102). See Strength 4.

## Concessions
- **Schema (S-002).** V1's gaps table omits `decision_needed_by_user`, which is required by `deviation-taxonomy.md:146`. Variant 2 conforms; V1 does not.
- **Drift boundary (X-001).** V1's "could be an unmapped change (Drift)" (V1:22, :57) is wrong as stated.
  - If the scope were widened and a hunk for `tests/test_greeting.py` appeared, it would map to T-103 and so would not be Drift (`deviation-taxonomy.md:62,96`).
  - The only Drift route left for T-103 is pytest exit 5 "Drift / coverage" (`:109`), which both cards already list.
  - V1's instinct really belongs under A-001 (other unmapped out-of-scope hunks), not under T-103.
- **Sibling disagreement (X-003).** V1's correctness gap #1 labels guard-vs-f-string *within one function* as a "Sibling disagreement" (V1:44). The advisory channel needs two sibling symbols (`deviation-taxonomy.md:161,167`). The observation is valid; it belongs under Risks, which is where Variant 2 puts it.
- **Citation range (C-002).** V1's `changes.patch:5-9` (V1:16) includes the `@@` header. It is defensible as a hunk reference, since the orchestrator map uses the same range (`task-to-diff-map.md:9`). But `:6-9` is the precise body range.
- **Precedence and coverage (U-003, U-007).** Variant 2's explicit precedence walk, `regression_present`, and F-table are real additions.

## Per-point positions

| Point | Preferred | Reason |
|---|---|---|
| S-001 | V2 | The explicit precedence walk documents the classification reasoning. |
| S-002 | V2 | Conforms to the taxonomy's byte-exact schema (`:140-147`). V1 omits a required field. |
| S-003 | V2 | The per-requirement F-table gives a spec→task→diff→source chain for each requirement. |
| S-004 | Neutral (slight V2) | Presentation only. V2's opening verdict blocks a clean-pass misreading. |
| S-005 | V2 | V1's advisory section misapplies the sibling-symbol criterion (`taxonomy:167`). |
| S-006 | V2 | Grounded/[INFERRED] tags on risks are better evidence hygiene. |
| C-001 | V1 (with V2 schema) | Gaps split by resolution path can be closed independently. V2's row 2 copies T1's. |
| C-002 | Mixed, lean V2 for body range | V2's `:6-9` is exact, but its "10 lines" claim is false. V1's `:5-9` is a valid hunk ref but imprecise as a body ref. |
| C-003 | V2 (concede) | Both are correct. "Ledger-true, acceptance-false" is the clearer framing. |
| C-004 | V1 | V2's rejection of `tests/__init__.py` probably contradicts pytest's prepend-mode rootdir insertion. |
| C-005 | V2 | Explicit `regression_present: false` matches `taxonomy:103`. |
| C-006 | V1 | Split confidence matches the evidence gradient. A single 0.76 overstates the change-level confidence. |
| X-001 | V2 (concede) | Drift needs a hunk with no task (`taxonomy:62`). A T-103 hunk would be mapped. |
| X-002 | V1 | Snapshot absence is not live-project absence. V2 then infers a live failure from it. |
| X-003 | V2 (concede) | `greet` has no sibling symbol, so the advisory correctness channel does not apply. |

## Shared-assumption responses
- **A-001: QUALIFY.** Nothing in the evidence supports it. The map records only that the patch has no tests hunk and that scope is `src` (`task-to-diff-map.md:11,19`, `t1-card.md:12`). Out-of-scope unmapped hunks would be genuine Drift candidates that neither card checked. V1's GG-1 `next_evidence_needed` (widen the diff scope) partly covers it. The merged card should state it as an explicit grounding gap, not leave it as an assumption.
- **A-002: ACCEPT.** `spec.md:6` gives the string unquoted, and the natural reading excludes the sentence-final period. `tests/test_greeting.py:5` asserts `"Hello, Ada!"` too, so spec, code and test agree. Low impact.
- **A-003: ACCEPT.** `deviation-taxonomy.md:105-113` is the governing table. One qualification: the flaky-retry rule (`:112`) and the default that any unmapped exit is a Grounding Gap (`:113`) must also apply. Neither card mentions them.
- **A-004: ACCEPT.** `deviation-taxonomy.md:149-152` says verbatim that `status: partial` is forced and `needs_human_decision: true` is emitted.
- **A-005: QUALIFY.** "Empty" (`spec.md:9`) clearly covers `""`, which `not ""` rejects (`src/greeting.py:2`). Rejecting `None` or `0` goes beyond R-002, but it sits inside the mapped T-102 hunk and contradicts nothing, so it is not a deviation. Whether whitespace counts as "empty" is still an open spec question; both cards recommend a spec amendment.
- **A-006: QUALIFY.** The snapshot is internally consistent: the patch body at `changes.patch:6-9` matches `src/greeting.py:1-4`. But I did not check `provenance-manifest.json` (it is outside my read boundary), and neither card did. Every "Grounded" tag is grounded *to the snapshot*. The merged report should say so.
- **A-007: QUALIFY (low).** It is unstated, but the failure mode is benign. On Python older than 3.6, `src/greeting.py:4` is a SyntaxError, which surfaces as pytest exit 2 at collection, a Grounding Gap (`taxonomy:108`), not a silent misclassification.
- **A-008: ACCEPT, scoped to the snapshot.** `task-to-diff-map.md:29-33` ("Not run … tool-unavailable", no task log) and `t1-card.md:4` ("Nothing was executed") support it. Results outside the snapshot cannot be excluded, given the boundary.

Files read: `variant-1-original.md`, `variant-2-original.md`, `diff-analysis.md` (under `.../artifacts/adversarial/adversarial/`); the 8 snapshot files under `.../artifacts/reviewer-snapshot/root/`; and `.../plugin/skills/sc-reflect-protocol/refs/deviation-taxonomy.md`. I wrote nothing.
