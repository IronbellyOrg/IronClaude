# Research Completeness Verification

**Topic:** Sprint 429 provider-failure detector hardening (task-builder single track)
**Date:** 2026-07-02
**Lens:** BREADTH (completeness)
**Track goal:** Harden `src/superclaude/cli/sprint/monitor.py` (2 hunks) + Shape-2 fixtures + parametrized detection-contract test + live/offline parity tests
**Spec:** `.dev/brainstorms/20260702-165220-sprint-429-detector-hardening/merged-requirements.md`

**Files analyzed:**
- 01-detector-change-surface.md
- 02-test-and-fixture-conventions.md
- 03-template-examples.md
- shape2-verbatim-transcript.jsonl

---

## Independent source verification (this analyst re-checked, not just trusted the research)

Before assessing coverage, I re-Read the current source for every load-bearing citation so the breadth verdict rests on facts, not on the research files' self-report:

| Claim (from research) | Independently verified | Result |
|---|---|---|
| C1 predicate at `monitor.py:323` = `if is_error and api_error_status == 429:` | `sed -n 319,333p` | CONFIRMED verbatim |
| Locals `is_error`/`api_error_status`/`body` in scope at `:319-321` | same read | CONFIRMED (`body = str(result_event.get("result", ""))` at :321) |
| Neither-body default (INV-001 residual) at `:332-333` | same read | CONFIRMED |
| C8 `_RE_ALL_ACCOUNT` at `:41-43` requires `via provider` suffix | `sed -n 41,44p` | CONFIRMED; `_RE_SINGLE_ACCOUNT` at :44 unchanged, no capture group |
| 6 existing Shape-1 fixtures, exact filenames | `ls fixtures/exhaustion/` | CONFIRMED all 6 present, names match research-02 exactly |
| `_classify_transcript` at `rerun_tasks.py:552` | `grep -n` | CONFIRMED |
| 3 test files exist | `ls` | CONFIRMED (test_monitor / test_rerun_tasks / test_recovery_policy) |

**Anti-fabrication (byte-exact Shape-2 source):** the assigned `shape2-verbatim-transcript.jsonl` was independently grep-checked and satisfies ALL FOUR load-bearing invariants R1+R2 key on:
- `rate_limit_error` substring present (grep count 2 — in both the assistant event and the terminal result event)
- `All credentials for model gpt-5.5 are cooling down` present
- `via provider` **absent** (grep count 0) — the C8 gap
- `api_error_status` **absent** (grep count 0) — the C1/G1 breaker

The ground-truth file `.dev/troubleshoot/429-signature-ground-truth.md` also exists (5820 bytes). A byte-exact, non-fabricated Shape-2 source therefore EXISTS and is captured in the research bundle itself. This closes the single biggest incident-recurrence risk (the original incident was caused by fabricating the expected shape).

---

## Coverage Audit — the 5 breadth areas the spawn mandated

| # | Required area | Covered by | Status |
|---|---|---|---|
| 1 | Exact `monitor.py` change-surface with line numbers | 01 §1 (predicate `:323`, branch `:324-333`), §2 (regex `:41-43`), §3 (locals `:319-321`) | COVERED — all line-pinned + independently re-verified |
| 2 | Read-only consumer / offline-mirror confirmation (what stays untouched) | 01 §4 (8-row consumer table a–h, each `file:line` + "untouched"), §4 offline-mirror paragraph, §5 | COVERED — exhaustive, each consumer confirmed byte-unchanged |
| 3 | test_monitor.py conventions + fixture format + ~12-row matrix + 4 parity asserts + offline `_classify_transcript` import/call form | 02 §1 (conventions), §2 (6 fixtures verbatim), §3 (3 new fixtures), §4 (`_classify_transcript(text: str)` call form + seam), §5 (12-row matrix parametrize-ready), §4 (4 parity asserts mapped) | COVERED — all sub-parts present |
| 4 | MDTM template-02 rules incl. QA gate encoding + POST reflect wrapper item + Execution Context | 03 §1 (frontmatter+sections), §2 (A3/B2 granularity), §3 (M3/M4/I19/I22 QA floors), §4 (POST reflect flat wrapper), §5 (Execution Context + TB-Add-7/8) | COVERED |
| 5 | Byte-exact Shape-2 fixture source exists (anti-fabrication) | `shape2-verbatim-transcript.jsonl` (assigned) + 02 §3 caveat + independent grep above | COVERED — verbatim source captured, invariants verified |

All 5 mandated breadth areas are covered.

---

## Deliverable-by-deliverable buildability (can a builder create each per-file-granular from the research?)

The BUILD-REQUEST names **3 new fixtures + 9 deliverables**. Each must be creatable per-file-granular from the research alone.

**3 new fixtures:**

| Fixture | Supported by | Buildable? |
|---|---|---|
| `all_account_cooldown_apierror429.jsonl` (load-bearing, Shape-2 all-account, `gpt-5.5`) | 02 §3 (4 invariants + reconstruction) + `shape2-verbatim-transcript.jsonl` verbatim source | YES — verbatim byte source exists; expected `(ALL_ACCOUNT_COOLDOWN, "gpt-5.5")` stated |
| `provider_429_incidental_ratelimit_text.jsonl` (FP guard, `is_error:false`) | 02 §3 item 2 + row 9; expected `NONE` | YES — content spec + expected verdict given |
| `single_account_apierror429_SYNTHESIZED.jsonl` (OQ2 breakpoint) | 02 §3 item 3 + row 7; naming rule + assumed phrasing + loud-failure comment | YES — explicitly flagged as synthesized with in-test comment requirement |

**9 deliverables (the implementer scope from spec §11 + §2):**

| # | Deliverable | Supported by | Buildable? |
|---|---|---|---|
| 1 | `monitor.py` hunk 1: widen predicate `:323` | 01 §1a (exact current line + exact target expression) | YES |
| 2 | `monitor.py` hunk 2: loosen `_RE_ALL_ACCOUNT` `:41-43` | 01 §2 (exact current regex + exact target regex) | YES |
| 3 | Fixture: all_account_cooldown_apierror429 | above | YES |
| 4 | Fixture: provider_429_incidental_ratelimit_text | above | YES |
| 5 | Fixture: single_account_apierror429_SYNTHESIZED | above | YES |
| 6 | ~12-row parametrized detection-contract table test | 02 §5 (full matrix w/ per-row source/kind/model + parametrize skeleton + xfail rule) | YES |
| 7 | 4 live/offline parity assertions | 02 §4 (each mapped to exact surface + existing template `test_monitor.py:336-343` / `test_rerun_tasks.py` seam) | YES |
| 8 | F5 timeout-unreachability guard test | 01 §1c (timeout branch `:335-343` + "guard test only") + spec §6.4 | PARTIAL — see Finding F1 |
| 9 | Regression: all 6 fixtures + policy truth table pass unchanged (R3) | 02 §2 (6 fixtures verbatim) + §6 (policy table byte-unchanged) | YES |

---

## Findings

### Finding F1 (MINOR) — F5 timeout-unreachability guard test: assertable but the exact assertion form is under-specified

**What:** Deliverable 8 (the F5 guard test, spec §6.4 / AC-adjacent) is described in prose as "assert a 429 body never reaches the timeout branch — every `is_error` 429 returns inside the 429 block before `:335`." Research-01 §1c pins the timeout branch to `:335-343` and confirms it stays untouched. But neither research file provides a concrete, copy-mirrorable assertion *shape* for F5 the way §4/§5 do for the contract table and the 4 parity asserts.

**Why it is only MINOR, not a gap that blocks the builder:** the builder CAN derive the test from what is present — the timeout fixture (`operation_timeout.jsonl`, row 10) exists, the branch semantics are pinned, and the assertion is straightforward ("a Shape-2 429 transcript classifies to `ALL_ACCOUNT_COOLDOWN`, never `OPERATION_TIMEOUT`"). It is per-file-granular buildable. It simply lacks a mirror-ready snippet, unlike every other test deliverable. A builder following the template's B2 self-contained-item rule will still produce it correctly.

**Recommendation:** In the task file's F5 item, state the assertion explicitly as "assert `detect_provider_failure(shape2_fixture).kind is ProviderFailure.ALL_ACCOUNT_COOLDOWN` (proving the 429 block returns before the `:335` timeout predicate)" so the builder does not have to infer it.

### Finding F2 (MINOR) — Contract-table "model X" placeholder on synthetic row 5

**What:** In both the spec §6.2 matrix and research-02 §5, row 5 (429-present, all-account body *without* "via provider") lists expected model as "model X" / "X" rather than a concrete string. This is a synthetic inline row the builder authors.

**Why MINOR:** row 5's purpose (prove R2 regex loosening is independent of `api_error_status`) is clear, and the builder controls the inline transcript, so they choose the model token and assert it. The `(?P<model>.+?)` non-greedy capture is documented. No external source needed.

**Recommendation:** builder picks any concrete model string for the row-5 inline transcript (e.g. `"claude-opus-4-8"` or `"gpt-5.5"`) and asserts that exact string; note it as builder-chosen in the row comment.

### Finding F3 (INFORMATIONAL, not a gap) — Shape-2 verbatim source location clarified by the assigned bundle file

**What:** Research-02 §3 carries a strong caveat that the merged spec does NOT contain a copy-paste-ready Shape-2 one-liner and that the builder MUST pull it byte-for-byte from the July incident raw logs / ground-truth file, providing a "faithful reconstruction" that must be validated by running the test. This is exactly the right anti-fabrication posture.

**Resolution (this analyst):** the assigned `shape2-verbatim-transcript.jsonl` in the research bundle IS the byte-exact source — its terminal result event is a real captured transcript (`cwd: Octodive`, real `session_id`, `duration_ms:181906`) and it satisfies all four invariants (verified by grep above). So the builder does NOT need to go hunting external logs — the verbatim line is already in the research directory. This is a strengthening, not a gap. The task file should point the load-bearing-fixture item at `research/shape2-verbatim-transcript.jsonl` as the byte source rather than at "the July incident raw logs," which is more precise and eliminates the one residual "go find it" step.

### Completeness check (per-file)

| Research File | Status | Summary | Gaps/Caveats surfaced | Line-cited evidence | Rating |
|---|---|---|---|---|---|
| 01-detector-change-surface.md | Complete | Yes (§Summary) | Yes (timeout-branch untouched note; superset/back-compat) | Every claim `file:line`, independently re-verified | Strong |
| 02-test-and-fixture-conventions.md | Complete | Yes (§Summary) | Yes (explicit anti-fabrication caveat §3; row-5 "X"; xfail rule) | Every claim `file:line`; fixtures reproduced verbatim | Strong |
| 03-template-examples.md | Complete | Yes (§Summary) | Yes (M4 include-only-if-derived judgment call flagged) | template:line + SKILL.md:line + example:line throughout | Strong |
| shape2-verbatim-transcript.jsonl | N/A (data) | — | — | Real captured transcript; 4 invariants verified | Strong (byte-exact source) |

### Contradiction detection

No contradictions between files. Cross-checks that AGREE:
- Both spec §6.2 and research-02 §5 use the identical 12-row matrix with identical per-row `(kind, model)` — no drift.
- Research-01's line numbers (`:323`, `:41-43`, `:332-333`, `:552`) match research-02's citations of the same surfaces and match current source (independently verified).
- The Shape-2 invariants in spec §3, research-02 §3, and the verbatim transcript file all agree (absent `api_error_status`, no `via provider`, `rate_limit_error` present, `gpt-5.5`).

### Compiled gaps

**Critical (block a builder):** NONE.

**Important (affect quality):** NONE.

**Minor (should be addressed in the task file but do not block per-file-granular build):**
- F1 — give the F5 guard test a concrete assertion shape in its item.
- F2 — row-5 model is builder-chosen; state it in the row comment.
- F3 (strengthening) — point the load-bearing-fixture item at `research/shape2-verbatim-transcript.jsonl` as the byte source instead of "July incident raw logs."

### Depth assessment

**Expected depth:** Deep (spec `depth: deep`; verification surface MEDIUM). Expect exact change-surface, full consumer-chain trace, fixture-level detail, parametrize-ready matrix, template-rule citations.

**Actual depth achieved:** Meets Deep. The research provides: (a) exact two-hunk change-surface with surrounding block quoted; (b) an 8-row untouched-consumer table each `file:line`-confirmed; (c) all 6 fixtures reproduced verbatim + 3 new fixtures spec'd + expected verdicts; (d) a parametrize-ready 12-row contract table + 4 parity asserts mapped to exact existing test templates; (e) full template-02 authoring rules (granularity, QA floors, POST-reflect flat wrapper, Execution Context TB-Add-7/8). RED→GREEN discipline is called out. The offline seam (`_classify_transcript`) — the currently untested path — is explicitly identified.

**Missing depth elements:** none blocking; only the two MINOR snippet-level under-specifications (F1, F2).

---

## VERDICT: PASS

All 5 mandated breadth areas are covered, all 3 new fixtures and all 9 deliverables are supported such that a builder can create each per-file-granular from the research bundle alone, and the anti-fabrication requirement is satisfied by a real byte-exact Shape-2 transcript captured IN the research directory (`shape2-verbatim-transcript.jsonl`), whose four load-bearing invariants I independently grep-verified. Every load-bearing source citation was independently re-Read against current source and confirmed. No contradictions. No critical or important gaps.

Three MINOR polish items (F1, F2, F3) are recommended for the task-file items but none blocks a per-file-granular build. The builder is cleared to proceed.

### Gap list (MINOR only — advisory, non-blocking)
1. **F1** — F5 timeout-unreachability guard test lacks a mirror-ready assertion snippet (has semantics + fixture). Fix: state `assert detect_provider_failure(shape2_fixture).kind is ProviderFailure.ALL_ACCOUNT_COOLDOWN` in the item.
2. **F2** — Contract-table row 5 expected model is placeholder "X" (builder-chosen inline). Fix: pick a concrete string, assert it, note builder-chosen in the row comment.
3. **F3** — Load-bearing Shape-2 fixture source should cite `research/shape2-verbatim-transcript.jsonl` (byte-exact, in-bundle) rather than "the July incident raw logs." Strengthening, not a defect.
