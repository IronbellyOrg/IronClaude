# QA Report — Research Gate (Evidence-Quality Lens)

**Topic:** Implement the reflect Tier-2 fallback model ladder per revised design.md
**Date:** 2026-07-06
**Phase:** research-gate
**Lens:** evidence-quality
**Fix cycle:** N/A
**Fix authorization:** false

---

## Scope

Assigned files (5):
- 01-reflect-seam-inventory.md
- 02-swarm-transport-slot-inventory.md
- 03-patterns-conventions.md
- 04-test-surface.md
- 05-template-and-examples.md

Lens focus: EVIDENCE QUALITY — verify cited file:line references against actual source.

**Partition note:** Sole QA instance for the 5 assigned files. Cross-file checks
(contradictions) applied across the assigned subset only.

---

## Citation Spot-Checks Performed (against ACTUAL source, this turn)

Far exceeds the 20% mandate — ~35 distinct file:line citations re-Read in source.

| # | Research claim | Source verified | Result |
|---|---|---|---|
| 1 | F01: seam stamp L216 / normalize L217-225 / succeeded_final_paths L226-230; insert between 225/226 | ensemble.py:210-230 | EXACT |
| 2 | F01/F03: `build_reflect_contract` def L553-569; 3 L2 kwargs reviewer_isolation(564)/audit_tree_dirty(565)/reviewer_grounding_root(566) | ensemble.py:553-569 | EXACT |
| 3 | F01: return dict L599-638; reviewer_isolation(635)/audit_tree_dirty(636)/reviewer_grounding_root(637); diversity calls L615/L616 | ensemble.py:599-638 | EXACT |
| 4 | F01: call site L308-340; swarm_status(316), reviewer_isolation(331-333), audit_tree_dirty(334), reviewer_grounding_root(335-339) | ensemble.py:308-340 | EXACT |
| 5 | F01: succeeded(579), reviewer_count(580), return None(581-582), tier_reached(584), merge_method(585) | ensemble.py:579-585 | EXACT |
| 6 | F01: compute_model_class_diversity def L641-648; compute_vendor_diversity L651-669; _vendor_from_model_id L672 | ensemble.py:641-672 | EXACT |
| 7 | F01: `_degraded_reason` def L256; T6 degraded-tier1 L271-272 BEFORE T10 single-reviewer-fallback L288-289; T7/T8/T9/T11/T11a match | contract.py:256-300 | EXACT |
| 8 | F01: `_LOAD_BEARING_BOOL_FIELDS` L48-58, exactly 7 fields, none are diversity/merge_method | contract.py:48-58 | EXACT |
| 9 | F01/F03: ReflectConfig field-order comment L82-83; base_override/fix/max_fix_iterations 84-86; reachability L109 = last defaulted; contract_path property L111-114 | reflect/models.py:82-114 | EXACT |
| 10 | F01: reflect commands.py run cmd L216; reachability opt L236; isolate_reviewers L312; def run L320; params 336/337; forwards 368/369; _build_inner_command L459, no-reachability L485, isolate L489 | reflect/commands.py | EXACT (±1) |
| 11 | F02: transport_for_slot(slot_index) L454; tasks over range(workers_requested) L464-472 (L471); rekey loop L485; _make_callable L444 | dispatch.py:444-489 | EXACT |
| 12 | F02: openai_compat import block L98-103 = exactly 4 T2 constants | openai_compat.py:98-103 | EXACT |
| 13 | F02/F03: `_collect_t2_models` L178-185 body (1-based dense loop) | swarm/config.py:178-185 | EXACT |
| 14 | F02: swarm config constants T2_PROXY_URL_ENV(51)/T2_PROXY_KEY_ENV(52)/T2_MODEL_ENV_PREFIX="T2Model0"(57)/T2_MODEL_MAX_SLOTS=9(63); @dataclass(frozen=True) L66 | swarm/config.py | EXACT |
| 15 | F02: ModelPoolTooSmallError L589-609; _resolve_run_transport_factory L612-618; read_env L680, pool L681, guard L687-688, _factory L691, pool[slot_index % len] L692 | swarm/commands.py:589-703 | EXACT |
| 16 | F02: WorkerStatus Literal L69 (4 values); ResultStatus L68; WorkerResult class L1020; fields index(1110)/final_path(1114)/model_id(1115)/status(1118); __post_init__ L1123 | swarm/models.py | EXACT |
| 17 | F03: ensemble consts REFLECT_REVIEW_RECIPE L66, SWARM_SUBRUN_DIR L67, TransportFactory L106, stub_model_id L116, resolve_t2_transport_factory L140 | ensemble.py | EXACT |
| 18 | F04: tests/cli/swarm/ does NOT exist | `ls` | CONFIRMED absent |
| 19 | F04: tests/cli/reflect/test_contract.py does NOT exist | `ls` | CONFIRMED absent |
| 20 | F04: tests/swarm/{test_config,test_openai_compat}.py exist | `ls` | CONFIRMED present |
| 21 | F04: greenfield — zero hits for t2_fallback/read_env_for_pool/make_fallback_slot_factory/T1Model/t1_models | grep tests/ src/cli | CONFIRMED zero |
| 22 | F04 Finding A: "design §9 instructs swarm tests under tests/cli/swarm/" | design.md:620-646 + revision_note L9 | **WRONG — design says the OPPOSITE** |
| 23 | F04 Finding B: "design §9 labels test_contract.py '(existing)'" | design.md:626-638 | **WRONG — design says it does NOT exist** |
| 24 | F04 §3: WorkerResult __post_init__ at "models.py:1010-1012 region" | swarm/models.py:1123 | **WRONG line (1010 is a different dataclass)** |

Files 01, 02, 03 citations: verified essentially flawless (every spot-checked
line exact or ±1). Defects concentrate in File 04 and File 05 (below).

---

## Findings

### ISSUE 1 — CRITICAL (evidence-quality): File 04's two "BLOCKING PATH FINDINGS" misrepresent the CURRENT (revised) design; their cited design lines say the OPPOSITE

File 04 opens with "⚠️ TWO BLOCKING PATH FINDINGS FOR THE BUILDER" asserting the
design is defective. Both are false against the ACTUAL current design.md:

- **Finding A** (F04 lines 12-28) claims: *"The design §9 (design.md:623-624,
  635-636) instructs writing swarm tests under `tests/cli/swarm/`. That directory
  does not exist. … The design's §9 F7 'corrected to tests/cli' note over-corrected
  the swarm rows."*
  - ACTUAL design.md:624 reads: *"but swarm tests live under **`tests/swarm/`**
    (NOT `tests/cli/swarm/`, which does not exist…)"*. The design table rows
    (design.md:640-641) already cite `tests/swarm/test_config.py` and
    `tests/swarm/test_openai_compat.py`.
  - `grep "tests/cli/swarm" design.md` → the ONLY hit is the negation on line 624.
    The design NEVER instructs `tests/cli/swarm/`.
  - design.md:9 `revision_note` explicitly lists **"F7: tests/cli paths"** among
    findings already **CLOSED**. File 04 re-litigates a resolved finding and brands
    the corrected design as "over-corrected."

- **Finding B** (F04 lines 30-48) claims: *"Design §9 row (design.md:633) cites
  `tests/cli/reflect/test_contract.py (existing)` … Design labels it 'existing'."*
  - ACTUAL design.md:633 is the **classify** test row (`test_fallback_classify.py`),
    not test_contract.py. `grep test_contract.py design.md` → the only hit is
    design.md:626: *"`tests/cli/reflect/test_contract.py` does NOT currently exist —
    the verdict-unchanged regression assertions are added to the existing
    `test_verdict_mapping.py`."* The design AGREES with file 04's conclusion and
    NEVER labels test_contract.py "existing."

Impact: The research's headline framing tells the builder the design is broken and
"over-corrected" when it is correct and already self-consistent. The specific
citations (design.md:623-624, 633) are wrong — they point at text stating the
opposite of the claim. Under the evidence-quality lens ("any citation that is
wrong/stale = flag"), this is the most serious defect: two load-bearing,
prominently-boxed findings rest on fabricated design conflicts. The *destinations*
file 04 recommends (tests/swarm/, fold into test_verdict_mapping.py) happen to match
the design, so a builder is not misrouted on path — but the assertion that the
design is defective is false and erodes trust in an already-correct spec.

Required fix: Rewrite File 04's §"TWO BLOCKING PATH FINDINGS" to reflect that the
CURRENT design (post-F7 revision, revision_note design.md:9) ALREADY specifies
`tests/swarm/` and ALREADY states test_contract.py does not exist. Demote from
"BLOCKING design defect" to "confirmation that the design's grounded paths are
correct." Re-cite design.md:624 and 626 accurately. Remove the "over-corrected"
claim.

### ISSUE 2 — IMPORTANT (evidence-quality + cross-file contradiction): File 04 §3 cites WorkerResult `__post_init__` at the wrong line; contradicts File 02

- File 04 §3 (line 160-161) states: *"`__post_init__` (models.py:1010-1012 region)
  raises `ValueError` on a status outside `WorkerStatus`."*
- ACTUAL: `WorkerResult.__post_init__` is at **swarm/models.py:1123**. Line 1010 is
  the `__post_init__` of a **different, preceding** dataclass (the WorkerResult
  class does not even begin until L1020).
- File 02 §5 (line 202) correctly cites *"`__post_init__` validates `status ∈
  WorkerStatus` — L1123-1129."* → File 02 and File 04 **contradict** each other on
  the same symbol; File 02 is correct, File 04 is wrong by ~113 lines and points at
  an unrelated dataclass.

Required fix: Correct File 04 §3 to `swarm/models.py:1123`.

### ISSUE 3 — MINOR (evidence-quality): File 04 §3 `WorkerResult.body` docstring citation is wrong

File 04 §3 (line 162) states the raw body attr is *"(models.py:1058-1071
docstring)."* Actual lines 1058-1071 are the WorkerResult docstring paragraphs
describing `final_path` / `model_id` / `model_label`, NOT the `body` attribute.
The `body` non-dataclass attr is documented elsewhere in the class docstring.

Required fix: Re-locate the `body` attr docstring citation, or drop the specific
line range.

### ISSUE 4 — MINOR: File 05 header Status says "In Progress" (checklist item 1 requires "Complete")

File 05 line 3 reads `**Status: In Progress**` while line 199 reads
`**Status: Complete**`. The authoritative top-of-file status field says In
Progress. The file inventory gate (research-gate checklist item 1) requires every
research file carry `Status: Complete`. Content is in fact complete, so this is a
stale header line, but it is an internal inconsistency that fails the literal
inventory check.

Required fix: Set File 05 line 3 to `Status: Complete`.

### ISSUE 5 — MINOR (evidence-quality): File 04 swarm-test line ranges run loose / start before the actual `def`

File 04 §1 cites *"empty slot skip (95-105)"* and *"max-slot ceiling (108-119)"*
for tests/swarm/test_config.py. Actual `def` lines are
`test_from_env_skips_empty_t2_model_slots` at **L98** and
`test_from_env_respects_max_slot_ceiling` at **L109** — File 04's ranges start
1-3 lines BEFORE the function definition (bracketing the prior test's tail). File
03 §3 cites the same tests as (100-106) and (109-117), which are accurate body
ranges. Minor imprecision in File 04 only; File 03 is correct.

Required fix: Tighten File 04 §1 ranges to the actual `def` boundaries (98-107,
109-124).

---

## Overall Verdict: FAIL

Rationale: Files 01, 02, 03 are exemplary — every one of ~25 spot-checked
citations across ensemble.py / contract.py / dispatch.py / openai_compat.py /
swarm-config.py / swarm-commands.py / reflect-commands.py / models.py verified
EXACT (or ±1). The F1 root-cause chain, the T6-before-T10 first-match ordering,
the additive-kwarg precedent, and the frozen/non-frozen dataclass distinctions
are all correctly grounded. However, the research-gate standard is zero-tolerance
("any gap regardless of severity = FAIL"), and File 04 carries a CRITICAL
evidence-quality defect: its two prominently-boxed "BLOCKING PATH FINDINGS" cite
design lines that state the OPPOSITE of the claim and brand an already-correct,
already-revised design as defective (F7 was explicitly closed per design.md:9).
Two further wrong citations (WorkerResult __post_init__ line; body docstring) and
a cross-file contradiction with File 02 compound it. File 05 has a stale
In-Progress header. These must be remediated before synthesis, because a synthesis
agent that trusts File 04's "design is broken" framing could propagate a false
defect narrative or mistrust the correct spec.

Note: none of the defects touch the *actionable engineering conclusions* (seam
location, symbol targets, test destinations, greenfield status) — those are
correct. The failures are in citation accuracy and the false design-conflict
framing, which is precisely the evidence-quality lens's remit.

## Items Reviewed (research-gate checklist)
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory (Status: Complete + Summary) | FAIL | F05 header line 3 = "In Progress" (Issue 4); F01-F04 Complete + Summary present |
| 2 | Evidence density | FAIL | ~30 citations verified EXACT in F01-F03; F04 has 3 wrong citations + 2 false-design findings (Issues 1-3,5) |
| 3 | Scope coverage vs research-notes EXISTING_FILES | UNVERIFIABLE | research-notes.md not in 5-file partition scope |
| 4 | Doc cross-validation ([CODE-VERIFIED] tags) | PASS (N/A) | Files are code-grounded, no doc-only claims requiring tags |
| 5 | Contradiction resolution | FAIL | F02 vs F04 contradict on WorkerResult __post_init__ line (Issue 2) |
| 6 | Gap severity | PASS | Gaps read; F04's "blocking gaps" are false alarms (Issue 1) — no genuine unresolved research gap |
| 7 | Depth appropriateness (data-flow trace) | PASS | F01 traces ensemble seam dispatch→stamp→normalize→contract end-to-end |
| 8 | Integration-point coverage | PASS | transport_for_slot / read_env / dispatch / resolve_config seams documented |
| 9 | Pattern documentation | PASS | F03 documents additive-kwarg, dataclass-ordering, frozen, test-seam patterns w/ line evidence |
| 10 | Incremental-writing compliance | PASS | Files show growing structure; F05 dual-status is a symptom of incremental authoring |

## Summary
- Checks passed: 6 / 10 (item 4 counted PASS-N/A)
- Checks failed: 3 (items 1, 2, 5)
- Unverifiable: 1 (item 3 — out of partition scope)
- Critical issues: 1 (Issue 1)
- Important issues: 1 (Issue 2)
- Minor issues: 3 (Issues 3, 4, 5)
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

## Confidence
- **Confidence:** Verified: 9/10 | Unverifiable: 1 | Unchecked: 0 | Confidence: 100.0%
  (VERIFIED/(TOTAL−UNVERIFIABLE) = 9/9. All findings backed by cited tool output;
  item 3 unverifiable because research-notes.md is outside the 5-file partition.)
- **Tool engagement:** Read: 13 | Grep: 4 (via Bash) | Glob: 0 | Bash: 4
  (No web research performed — all claims are source-truth-local; Tavily N/A.)
- **Unverifiable items:** Item 3 (scope coverage) — requires research-notes.md
  EXISTING_FILES list, which is not among the 5 assigned partition files.
- **Unchecked items:** none.

## Recommendations
1. Correct File 04's "TWO BLOCKING PATH FINDINGS" framing: the CURRENT revised
   design (design.md:9 revision_note closes F7; lines 624/626) ALREADY specifies
   tests/swarm/ and ALREADY states test_contract.py does not exist. Re-frame as
   confirmation, not a design defect. (Issue 1 — CRITICAL)
2. Fix File 04 §3 WorkerResult __post_init__ citation → swarm/models.py:1123;
   reconcile with File 02 (Issue 2 — IMPORTANT).
3. Fix File 04 §3 body-attr docstring citation (Issue 3) and §1 swarm-test line
   ranges (Issue 5).
4. Set File 05 line 3 Status → Complete (Issue 4).
5. After remediation, re-run this evidence-quality gate (fix-cycle) — the
   engineering substance is sound; only citation accuracy + F04 framing block PASS.

## QA Complete

