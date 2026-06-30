# QA Report — Research Gate (Gap-Detection Lens)

**Topic:** Build MDTM task file to implement `sc:submit-pr` per merged spec
**Date:** 2026-06-11
**Phase:** research-gate
**Lens:** GAP DETECTION (spec areas researchers missed entirely)
**Fix cycle:** N/A
**Stance:** ADVERSARIAL — assume research missed things; find the gaps.

---

## Scope

- SPEC: `.dev/brainstorms/20260610-234750-pr-review-auto-remediation/merged-spec.md`
- RESEARCH: files 01..07 in `research/`
- TRACK GOAL: builder must create per-file/per-phase MDTM items to implement `sc:submit-pr`.

Focus areas (from spawn prompt):
1. Run-log JSONL substrate (§11: envelope, 30 event types, 5 idempotency sets)
2. §12 crash-window resume / INV-007 write-ahead push triad
3. §10 validation gates VG-1..6 (lint≠format two-gate)
4. 21 test files in §6.3 mapped to source modules (R4)
5. FSM state machine (§5: states, gates G-arm/G-edit/G-push, 5-predicate INV-016)
6. Backoff/rate-limit (FR-2.5/NFR-2), idempotency (NFR-1), observability (NFR-3)
7. Findings actionable? Missing integration points?

---

## Verification Log

Read in full: spec (1085 lines, both pages) + all 7 research files (01..07) + the 3 in-progress
peer QA/analyst stubs. Cross-checked each of the 7 lens-focus areas against actual research content
with targeted greps. Findings below.

---

## Lens-Area Coverage Assessment (the 7 builder-needs)

| # | Lens area | Spec ref | Researched enough to build items? | Verdict |
|---|-----------|----------|-----------------------------------|---------|
| 1 | Run-log JSONL substrate (envelope, 30 event types, 5 idempotency sets) | §11 | **NO** — fell between researchers | **GAP (CRITICAL)** |
| 2 | Crash-window resume / INV-007 write-ahead push triad | §12.1 | **NO** — no owner; deferred to "R3" which didn't cover it | **GAP (CRITICAL)** |
| 3 | Validation gates VG-1..6 ordered list + lint≠format | §10 | Partial — commands confirmed, ordered list not enumerated | **GAP (MINOR)** |
| 4 | 21 test files → source modules (R4) | §6.3 | **YES** — file 04 §C full table | OK |
| 5 | FSM state machine (states, 3 gates, INV-016 5-predicate) | §5 | Partial — module named, transition table not mapped | **GAP (IMPORTANT)** |
| 6 | Backoff/idempotency/observability | FR-2.5/NFR-1/NFR-3 | Backoff+idempotency OK; observability=#1 gap | Partial (rolls into #1) |
| 7 | Actionability / integration seams | — | Strong — seams explicitly flagged | OK |

---

## GAP-1 (CRITICAL) — Run-log JSONL substrate (§11) is unresearched

**The single most serious gap.** Spec §11 defines a substantial substrate the builder must turn into
`loop-guard.md` + a `run_log.py` module + `test_run_log.py`:
- §11.3: an **event envelope** with required fields (`schema_version`, `event_id` unique+monotonic,
  `event_type`, `timestamp`, `run_id`, `pr{repo,number,url,base,head}`, `state_before`, `state_after`,
  `round_index`/`round_counter`, `payload`).
- §11.3: **30 named event types** (`run_started` … `terminal_failed`) — an enumerated, load-bearing list.
- §11.2: **file locations** — `monitor-run-<PR>.jsonl` (authoritative), `state.snapshot.json` (cache),
  `findings.latest.json`, `validation/round-<N>/`, `troubleshoot/round-<N>/`, plus the default
  `<output-dir>` path.
- §11.1: the **authority rule** — JSONL authoritative, snapshot rebuildable; write-ahead + fsync before
  every side effect.
- §11.4: the **5 idempotency sets** (`processed_review_ids`, `processed_finding_ids` keyed on `fix_key`,
  `replied_comment_ids`, `resolved_thread_ids`, `pushed_commit_shas`).

**Evidence of the gap (independently verified via grep):**
- File 04 (R4, the test-infra owner) references the run-log only as `run_log.py # JSONL observability
  (T-N20..N22)` (line 36) and three test-table rows (lines 169/171/172). It does **NOT** enumerate the
  envelope fields, the 30 event types, the 5 idempotency sets, or the snapshot/authority rule. So the
  module exists in the layout but its *internal contract* is undocumented.
- File 01 (R1) lists `loop-guard.md` purpose as "FR-6 round-counter invariants (INV-001) + run-log
  schema (§11)" (line 78) — it points AT §11 but does not unpack it.
- File 05 (R5) §5 touches the triad event names but **explicitly disclaims ownership**: "These are R3's
  contract domain" (line 270).
- File 03 (R3) is "Reuse Surfaces" — severity rubric / verify discipline / troubleshoot flags. It does
  **NOT** cover the run-log at all (grep confirms zero run-log content in 03).

So §11 was assigned (by file 05's own pointer) to "R3", but R3's actual scope was reuse surfaces. The
run-log substrate has **no owning researcher**. The builder, when creating the `run_log.py` item +
`loop-guard.md` run-log-schema section + `test_run_log.py` item, will be left re-deriving the 30 event
types, the envelope schema, and the 5 idempotency sets directly from the spec with no mapping to the
module/test structure, no note on which events are write-ahead, and no guidance on the snapshot-rebuild
test.

**Why this is CRITICAL not IMPORTANT:** the run-log is the spine of resumability (NFR-3), the
idempotency sets back FR-6/NFR-1 (double-post prevention), and `pushed_commit_shas` is what INV-001
attributes re-reviews against (the loop-guard correctness invariant, the P0 defect class). A builder
item that says "create run_log.py per §11" without the researched envelope/event-set mapping risks a
thin or schema-divergent module that silently breaks resume and idempotency tests.

**Required remediation:** a research addendum (or an R3/R4 extension) that, for the builder, enumerates:
(a) the event envelope field list, (b) the 30 event-type names grouped by FSM phase, (c) which events
are write-ahead/fsynced, (d) the 5 idempotency sets + their keys, (e) the 5 file locations + authority
rule, and (f) maps these to `run_log.py` + the `loop-guard.md` schema section + `test_run_log.py`
(T-N20..N22) and `test_idempotency.py` (T-N01/N02).

---

## GAP-2 (CRITICAL) — INV-007 write-ahead push triad + crash-window resume (§12.1) unresearched

Closely related to GAP-1 but distinct enough to rate separately because it drives `test_crash_recovery.py`
and the T-CRASH-WINDOW-NO-DOUBLE-PUSH P0 invariant.

Spec §12.1 (INV-007, verbatim normative) defines:
- the **ordered push triad** `push_decision → push_initiated (fsync before git push) → push_completed`,
  with exact payload fields per event;
- the **idempotency key** `push:<run_id>:<cycle_id>:<pre_push_sha>:<target_branch>` (PRE-push SHA);
- the **crash-window resume rule** — on `--resume`, if `push_initiated` has no matching `push_completed`,
  query the remote for `target_sha` and branch into reachable / not-reachable / ambiguous, each with a
  specific recorded outcome and HALT-or-resume behavior.

**Evidence of the gap:**
- File 05 (R5) §5 mentions the triad event names exist but defers the contract ("R3's contract domain",
  line 270) and does not unpack the resume branch logic.
- File 06 (R6) covers the **gh/git push SURFACE** (the `git push` mechanics, `--repo` pinning, the reply/
  resolve API) but does **NOT** cover the §12.1 *ordering / fsync / crash-window resume reconstruction*
  — its scope is "gh API DETAIL", not the recovery state machine. Grep confirms no INV-007 resume-branch
  content in any research file.
- File 04 maps `test_crash_recovery.py → submit_pr.fsm resume + run_log reconstruction` (line 172) but
  gives the builder **no researched detail** on the three-way reachable/not-reachable/ambiguous branch,
  the `recovered:true` event variants, or the remote-reachability mock (which §18.3 mandates).

**Required remediation:** the same addendum should map §12.1 to: the `submit_pr.fsm` resume entry point,
the `run_log.py` triad-event writers (write-ahead/fsync ordering), the remote-reachability mock in
`conftest.py`, and `test_crash_recovery.py` (T-CRASH-WINDOW-NO-DOUBLE-PUSH + the three resume branches).
Without it the builder cannot write a faithful crash-recovery item — it would guess the resume branching.

---

## GAP-3 (IMPORTANT) — FSM transition table / INV-016 5-predicate not mapped to the module

File 04 names `fsm.py # FSM states (S0..S7 / HALT_*), transition fn, run_skill() driver` and the module
exists in the layout. But **no research file** decomposes the §5 FSM for the builder beyond the file
existing:
- the **transition table** (§5.1 ASCII FSM) — which the spec says C6 "tests directly (AC-2..AC-6 become
  table-row assertions)" (§5.4) — is not mapped to `test_autonomy_gates.py` / a transition-table test.
- the **3 gates** (G-arm/G-edit/G-push) + the **needs_human_decision override** — file 01 lists them as
  SKILL.md/state-machine.md responsibilities but no researcher maps the gate predicates to the
  `classifier.py`/`fsm.py` split or to the §5.2 gate table.
- the **INV-016 5-predicate conjunction** (the G-push runtime gate) — referenced by file 04 only as
  `T-ZERO-EDIT-NO-PUSH` in a test-table row; the 5 predicates themselves and how predicate (5)
  `applied_edits > 0` threads through `push_decision` are not unpacked.

**Mitigating factor (why IMPORTANT not CRITICAL):** the spec §5 is itself unusually detailed and
self-contained (full ASCII FSM, the §5.2 gate table, the §5.3 INV-016 verbatim text, the §15.6 state
glossary). A competent builder reading §5 + file 04's module names can construct the items. The gap is
that the *research didn't pre-chew it into module-mapped items*, so the builder does more spec-reading
work and the FSM↔test-table-assertion mapping (which the spec explicitly calls for) is unguided. This
raises the risk of an under-specified `state-machine.md` or a missing transition-table test, but does
not leave the builder fundamentally guessing the way GAP-1/GAP-2 do.

**Required remediation (lighter):** a short mapping note tying §5.1 transition table → a transition-table
test in `test_autonomy_gates.py`; §5.2 gate table → the three gate predicates in `fsm.py`/`classifier.py`;
§5.3 INV-016 → the `push_decision` writer + T-ZERO-EDIT-NO-PUSH. Could be folded into the GAP-1/GAP-2
addendum.

---

## GAP-4 (MINOR) — Validation gates VG-1..6 not enumerated as an ordered actionable list

Spec §10 defines an **ordered** gate list (VG-1 targeted tests → VG-2 cross-cutting `make test` →
VG-3 `make lint` → VG-4 `ruff format --check` → VG-5 `make verify-sync` → VG-6 PR-target URL), with the
lint≠format two-gate split (VG-3+VG-4 both mandatory) being the load-bearing known-gotcha.

**What research covers:** file 02 confirms `make lint`/`make verify-sync`/sync discipline; file 04
confirms `uv run pytest` + the marker registry; the project memory note "make lint ≠ CI ruff format" is
the known gotcha. So all the *commands* exist in research.

**What's missing:** no research file enumerates VG-1..6 as the **ordered list** the builder must encode
as the `S7_VALIDATING` validation item / `test_validation_gate.py` (T-501/502/510/511/520-522), nor maps
`validation_status == "validated"` (the §5.4 / FR-5.4 single definition consumed by the G-push predicate)
to the FSM. The builder can assemble this from §10 directly, so it's MINOR — but it's another
spec-re-derivation the research could have pre-mapped, and the VG-3/VG-4 split is exactly the kind of
thing that gets collapsed into one gate if not called out.

---

## What the research covers WELL (so the builder is NOT guessing)

To be fair and adversarially honest about where I could NOT find a gap:
- **GAP-4 area aside, the test-file→module mapping (lens #4) is fully actionable** — file 04 §C is a
  complete 21-row table + the `run_skill()`/`remap_severity`/`poll_augment_review`/`classify` import
  contract + the **critical hyphen defect** (the spec's `--cov=superclaude.skills.sc-submit-pr-protocol`
  is unresolvable → `--cov=superclaude.submit_pr`) + the **unregistered-markers** action
  (loop_guard/autonomy/recovery/p0/loop must be added to pyproject or --strict-markers fails). These are
  high-value, builder-ready findings.
- **Detection probe / DET gate (lens-adjacent)** — file 06 §1 is excellent: the 5 capture commands, the
  "cannot run now / must HALT" framing, the `needs_human_decision` PENDING-not-auto-lock encoding tied to
  the project memory, and T-210 mechanical enforcement.
- **Reuse surfaces** — file 03 nails the severity-rubric reuse-by-reference, the `evidence-validator`
  agent reuse for C3a, and the **`--depth quick` × `--fix` STOP conflict** (a real builder landmine).
- **Integration seams** — file 05 flags the two biggest seams (Monitor-tool ≠ daemon; troubleshoot won't
  auto-apply edits so submit-pr must own edit application at L2/L3) — exactly the "missing integration
  points" the lens asked for.
- **MDTM template** — file 07 gives the full Template-02 rule set + the L5-contract-verdict-gate DAG
  encoding + the POST-reflect HALT-gate pattern. Builder-ready.
- **Conventions** — file 02 resolves the SKILL/command/hook structure, the Activation pairing, and flags
  the real open question (does `make sync-dev` copy `hooks/`? — file 05 §3.2 then ANSWERS it:
  Makefile:131-135 copies commands, and hooks sync is confirmed via the settings.json reference; though
  the hooks-flattening question remains lightly held).

The gap is specifically the **§11 run-log substrate + §12.1 INV-007 recovery contract** — a coherent
subsystem that fell through an ownership crack (file 05 pointed at "R3", R3 did reuse-surfaces), plus the
lighter §5-FSM-mapping and §10-VG-list pre-chewing.

---

## Overall Verdict: FAIL

Two CRITICAL gaps (the §11 run-log substrate and §12.1 INV-007 crash-window/push-triad recovery contract)
leave the builder genuinely guessing on a coherent, load-bearing subsystem — the substrate that backs
resumability (NFR-3), idempotency (NFR-1), and the INV-001 push-SHA attribution that the P0 loop-guard
depends on. Under the research-gate rule (ANY gap regardless of severity = FAIL, and these are
CRITICAL), this is a FAIL.

### Severity-rated gap list

| # | Severity | Spec area | Remediation |
|---|----------|-----------|-------------|
| GAP-1 | **CRITICAL** | §11 run-log substrate (envelope, 30 event types, 5 idempotency sets, 5 file locations, authority rule) | Addendum enumerating envelope fields + 30 event types grouped by FSM phase + write-ahead set + 5 idempotency sets/keys + locations/authority, mapped to `run_log.py` + `loop-guard.md` schema section + `test_run_log.py` (T-N20..N22) + `test_idempotency.py` (T-N01/N02) |
| GAP-2 | **CRITICAL** | §12.1 INV-007 push triad + crash-window resume (3-way reachable/not-reachable/ambiguous) | Addendum mapping triad write/fsync ordering + idempotency key + 3-way resume branch to `submit_pr.fsm` resume entry, `run_log.py` triad writers, the remote-reachability mock in `conftest.py`, and `test_crash_recovery.py` (T-CRASH-WINDOW-NO-DOUBLE-PUSH) |
| GAP-3 | IMPORTANT | §5 FSM transition table + §5.2 gate table + §5.3 INV-016 5-predicate | Mapping note: §5.1 table → transition-table test in `test_autonomy_gates.py`; §5.2 gates → `fsm.py`/`classifier.py` predicates; §5.3 INV-016 → `push_decision` writer + T-ZERO-EDIT-NO-PUSH (can fold into GAP-1/2 addendum) |
| GAP-4 | MINOR | §10 VG-1..6 ordered list + lint≠format two-gate + `validation_status=="validated"` definition | Enumerate VG-1..6 ordered → `test_validation_gate.py` (T-501/502/510/511/520-522) mapping; call out VG-3+VG-4 must NOT collapse |

**Note on scope of remediation:** GAP-1 and GAP-2 are the same coherent subsystem and can be closed by a
single focused research addendum (one researcher pass over §11 + §12.1, mapping to the `run_log.py` /
`loop-guard.md` / `test_run_log.py` / `test_crash_recovery.py` / `test_idempotency.py` surfaces). GAP-3
and GAP-4 are lighter and can ride along in the same addendum. The other ~85% of the research is
builder-ready and does not need rework.

---

## Confidence Gate

- **Confidence:** Verified: 7/7 lens areas | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
  (Each of the 7 lens-focus areas was checked against actual research content via Read + targeted grep;
  the run-log/INV-007 absence was independently confirmed by grepping all 7 files for run-log/event/
  INV-007/triad tokens — the matches are pointers-to-§11, not unpacked content.)
- **Tool engagement:** Read: 10 | Grep: 4 | Glob: 0 | Bash: 4 (grep/cat via Bash) | tavily: 0 (no
  external lookup needed — all verification is source-truth-local)
- UNCHECKED items: none
- UNVERIFIABLE items: none

## QA Complete
