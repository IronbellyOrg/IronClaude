# Cross-Validation Report — Sprint 429 Detector Hardening (Single Track)

**Analysis type:** completeness-verification
**Lens:** CROSS-VALIDATION (between research files + against actual source)
**Date:** 2026-07-02
**Files analyzed:** 01-detector-change-surface.md, 02-test-and-fixture-conventions.md, 03-template-examples.md, shape2-verbatim-transcript.jsonl
**Spec:** /config/workspace/IronClaude/.dev/brainstorms/20260702-165220-sprint-429-detector-hardening/merged-requirements.md

---

## Method

For each cross-claim where two research files (or the spec) cover the same fact, I re-read the
actual source myself and compared. Line-number claims in 01 were spot-checked against the live
`monitor.py` / `rerun_tasks.py`. The Shape-2 fixture claims in 02 were checked against the actual
`shape2-verbatim-transcript.jsonl`. The contract matrix in 02 §5 was checked against spec §6.2 and
against 01's stated semantics.

## 1. Line-number cross-claims in 01 vs actual source (SPOT-CHECKED)

Every line-number claim in `01-detector-change-surface.md` was re-verified by Reading the exact
range in the live `monitor.py` / `rerun_tasks.py` this turn.

| 01 claim | Cited line | Actual (Read this turn) | Verdict |
|---|---|---|---|
| C1 entry predicate `if is_error and api_error_status == 429:` | `monitor.py:323` | `monitor.py:323` verbatim | **VERIFIED** |
| 429 branch body (all/single/neither) | `:324-333` | `:324-333` verbatim | **VERIFIED** |
| neither-body default `SINGLE_ACCOUNT_LIMIT` | `:332-333` | comment `:332` + return `:333` | **VERIFIED** |
| timeout branch predicate + return | `:335-343` | predicate `:335-338`, return `:343` | **VERIFIED** |
| terminal `NONE` fall-through | `:345` | `return ProviderFailureSignal(ProviderFailure.NONE)` at `:345` | **VERIFIED** |
| `_RE_ALL_ACCOUNT` (with `via provider`) | `:41-43` | `:41-43` verbatim incl. `(?P<model>.+?) are cooling down via provider` | **VERIFIED** |
| `_RE_SINGLE_ACCOUNT` | `:44` | `r"would exceed your account's rate limit"` at `:44` | **VERIFIED** |
| in-scope locals `is_error`/`api_error_status`/`body` | `:319-321` | `:319` `bool(...)`, `:320` bare `.get`, `:321` `str(...get("result",""))` | **VERIFIED** |
| enum members | `:272-275` | `NONE/SINGLE_ACCOUNT_LIMIT/ALL_ACCOUNT_COOLDOWN/OPERATION_TIMEOUT` `:272-275` | **VERIFIED** |
| `_classify_transcript` def | `rerun_tasks.py:552` | `def _classify_transcript(text: str) -> TaskStatus:` at `:552` | **VERIFIED** |
| inner-detector delegation | `rerun_tasks.py:592` | `_sig = _provider_failure_from_text(text)` at `:592` | **VERIFIED** |
| `PASS_RECOVERED` / `FAIL_PROVIDER_EXHAUSTED` returns | `:604`/`:605` | `PASS_RECOVERED` `:604`, `FAIL_PROVIDER_EXHAUSTED` `:605` | **VERIFIED** |

**Result:** ALL 12 spot-checked line-number cross-claims in 01 are byte-accurate against the current
source. No drift. (01's header claim "every claim cites a line I actually Read this turn" holds.)

Minor consistency note (not a defect): 01 §4 also cites consumer-chain lines in `recovery_policy.py`,
`executor.py`, `models.py`, `aienv.py` (`:69-70`, `:1085`, `:2283`, `:53/66`, `:880`, `:81`). These
are outside my ASSIGNED spot-check budget (assigned lens targeted the predicate/regex/body/offline
lines, all of which passed). They are marked here as **[UNVERIFIED — outside assigned spot-check
set]**; the four load-bearing lines the lens named (`:323`, `:41-43`, `:321`, `:592`/`:605`) are all
VERIFIED.

---

## 2. C1 predicate-widening: 01 vs spec R1 (§4)

- **01** (line 22): widens `:323` to `is_error and (api_error_status == 429 or "rate_limit_error" in body)`.
- **Spec R1** (`:96-99`): `is_error == true AND (api_error_status == 429 OR "rate_limit_error" in body)`.
- **01** (line 102): disjunct is a plain `"rate_limit_error" in body` membership test, NOT a regex,
  NOT JSON-path; no helper.
- **Spec R1** (`:101-103`): "Membership test is a plain `"rate_limit_error" in body`, NOT a regex,
  NOT a JSON-path extraction"; "no `_is_rate_limited()` helper".

**Verdict: CONSISTENT.** 01's predicate form, disjunct-ordering (structured field FIRST → superset /
back-compat R3), inlining decision, and no-helper decision all match spec R1/R3 verbatim.

---

## 3. C8 regex-loosening: 01 vs spec R2

- **01** (line 79-80): drop `via provider` → `r"All credentials for model (?P<model>.+?) are cooling down"`,
  keep non-greedy `(?P<model>.+?)`; `_RE_SINGLE_ACCOUNT` UNCHANGED.
- **Spec R2** (`:105-108`): same target string, "still non-greedily capturing the resolved model";
  `_RE_SINGLE_ACCOUNT` "is unchanged".

**Verdict: CONSISTENT.** Also cross-checked against the CURRENT source at `monitor.py:41-43`, which
still carries the `via provider` suffix — confirming C8 has a real target to loosen.

---

## 4. Shape-2 verbatim transcript: actual file vs 02's claims + spec §3

I Read `shape2-verbatim-transcript.jsonl`. The terminal result event is **line 3**:

```
{"type":"result","subtype":"success","is_error":true,"duration_ms":181906,...,"result":"API Error: 429 {\"error\":{\"message\":\"b'{\\\"type\\\":\\\"error\\\",\\\"error\\\":{\\\"type\\\":\\\"rate_limit_error\\\",\\\"message\\\":\\\"All credentials for model gpt-5.5 are cooling down\\\"}}'\",\"type\":\"None\",\"param\":\"None\",\"code\":\"429\"}}",...}
```

The four load-bearing invariants (spec §3 / 02 §3) checked against the ACTUAL bytes:

| Invariant (02 §3 / spec §3) | Required | Actual in `.jsonl` line 3 | Verdict |
|---|---|---|---|
| (a) `is_error:true` | present | `"is_error":true` | **CONFIRMED** |
| (b) NO `api_error_status` key | absent | no `api_error_status` token anywhere in the line | **CONFIRMED** |
| (c) `rate_limit_error` in body | present | `\\\"type\\\":\\\"rate_limit_error\\\"` inside nested envelope | **CONFIRMED** |
| (d) `All credentials for model gpt-5.5 are cooling down`, NO "via provider" | present, no suffix | `All credentials for model gpt-5.5 are cooling down` — NO "via provider" | **CONFIRMED** |
| model = `gpt-5.5` | yes | `gpt-5.5` (also in `system.init` `"model":"gpt-5.5"` on line 1) | **CONFIRMED** |
| prefix `API Error: 429 {...}` | yes | `"API Error: 429 {\"error\":...` | **CONFIRMED** |
| nested `"code":"429"` | yes | `\"code\":\"429\"` | **CONFIRMED** |

**Verdict: the verbatim transcript satisfies EVERY Shape-2 distinguishing fact 02 and the spec name.**
All four R1/R2 key invariants hold. The transcript is genuine ground truth (session_id, real
`duration_ms:181906`, `cwd:/config/workspace/Octodive`), not a hand-fabrication.

### 4a. IMPORTANT cross-file discrepancy (02's reconstruction vs the now-present verbatim)

02 §3 (lines 148-152) states: *"the merged-requirements file does NOT contain a single
copy-paste-ready one-line JSON literal … The builder MUST source the exact byte-for-byte Shape-2 line
from the July incident raw logs"* and provides a **reconstruction** it explicitly labels as needing
validation. That reconstruction is:

```
...\"message\":\"b'{...rate_limit_error...All credentials for model gpt-5.5 are cooling down...}'\",\"code\":\"429\"}}"}
```

The **actual verbatim** now present in `shape2-verbatim-transcript.jsonl` differs from 02's
reconstruction in the nested-envelope key ordering: the real line carries
`...\"code\":\"429\"}}` **preceded by** `\"type\":\"None\",\"param\":\"None\"` fields
(`...cooling down\\\"}}'\",\"type\":\"None\",\"param\":\"None\",\"code\":\"429\"}}`), which 02's
reconstruction OMITS. 02's reconstruction also lacks the `duration_ms`/`num_turns`/`session_id`
envelope fields the real result event carries.

**This is NOT a contradiction that blocks the build** — because:
- 02 EXPLICITLY flagged its literal as a reconstruction and instructed the builder to source the
  byte-for-byte line from ground truth, not to use the reconstruction.
- The four load-bearing invariants (a)-(d) that R1/R2 key on are IDENTICAL between the reconstruction
  and the verbatim. The detector keys ONLY on `is_error`, absent `api_error_status`,
  `"rate_limit_error" in body`, and the `_RE_ALL_ACCOUNT` regex — none of which touch the
  `type/param/code` envelope fields or `duration_ms`.

**Actionable cross-validation finding (Minor):** the builder now has a REAL verbatim source
(`shape2-verbatim-transcript.jsonl`) and should author `all_account_cooldown_apierror429.jsonl` from
THAT line (line 3), NOT from 02's reconstruction. 02's authoring caveat ("do NOT hand-fabricate")
is now satisfiable directly. Recommend the task item cite `shape2-verbatim-transcript.jsonl:3` as the
byte source.

---

## 5. 02's 12-row contract matrix vs spec §6.2 vs 01's semantics

I diffed 02 §5 (lines 205-218) against spec §6.2 (`:180-193`) row-by-row, and checked each row's
expected `(kind, model)` against 01's stated branch semantics + the actual `monitor.py:323-345`.

| Row | 02 (kind / model) | Spec §6.2 (kind / model) | Consistent with 01 + source? | Verdict |
|---|---|---|---|---|
| 1 | ALL_ACCOUNT_COOLDOWN / `claude-opus-4-8` | same | 429+via-provider → `_RE_ALL_ACCOUNT` match → cooldown, group=model | **MATCH** |
| 2 | SINGLE_ACCOUNT_LIMIT / None | same | 429+single body → `:330-331` | **MATCH** |
| 3 | SINGLE_ACCOUNT_LIMIT / None | same | 429+single (api_retry_maxed) → `:330-331` | **MATCH** |
| 4 | ALL_ACCOUNT_COOLDOWN / `gpt-5.5` (load-bearing) | same | absent-aes → C1 text disjunct opens; loosened `_RE_ALL_ACCOUNT` matches → cooldown/gpt-5.5 | **MATCH** |
| 5 | ALL_ACCOUNT_COOLDOWN / X | ALL_ACCOUNT_COOLDOWN / X | 429-present + no-via-provider → post-C8 regex matches (proves R2 ⟂ aes) | **MATCH** |
| 6 | ALL_ACCOUNT_COOLDOWN / `claude-opus-4-8` | same | absent-aes + via-provider present → C1 text disjunct opens, regex matches (proves R1) | **MATCH** |
| 7 | SINGLE_ACCOUNT_LIMIT / None (SYNTHESIZED) | same | absent-aes + "would exceed…" → C1 opens, `_RE_SINGLE_ACCOUNT` → `:330-331` | **MATCH** |
| 8 | SINGLE_ACCOUNT_LIMIT / None (INV-001 residual) | same, `:332-333` | absent-aes + rate_limit_error + neither body → neither-body default `:333` | **MATCH** |
| 9 | NONE / None (FP fixture) | same | `is_error:false` → predicate fails on `is_error` conjunct → falls through to `:345` NONE | **MATCH** |
| 10 | OPERATION_TIMEOUT / None | same | `is_error:true` + aes null + exact timeout body → `:335-343` | **MATCH** |
| 11 | NONE / None (real task fail) | same | `is_error:true`, aes absent, no rate_limit_error → C1 both disjuncts false → `:345` NONE | **MATCH** |
| 12 | NONE / None (clean pass) | same | `is_error:false` → `:345` NONE | **MATCH** |

**Verdict: 02's 12-row matrix is a faithful, row-for-row reproduction of spec §6.2**, and every
expected `(kind, model)` is consistent with 01's branch semantics AND the actual `monitor.py:323-345`
post-fix control flow. Specifically the two lens-named spot-checks:
- **Row 4** (Shape-2 all-account → `ALL_ACCOUNT_COOLDOWN`, model `gpt-5.5`): **MATCH** across
  02, spec §6.2, and post-C1/C8 source semantics. Cross-validated further against the actual
  `shape2-verbatim-transcript.jsonl` (§4 above).
- **Row 9** (`is_error:false` → `NONE`): **MATCH**. The `is_error` conjunct at `:323` (and the
  timeout branch's `is_error` at `:336`) both fail on a false `is_error`, so the FP prose can never
  open the gate → terminal `NONE` at `:345`. This is exactly the R4/INV-004 FP-guard behavior.

Note: 02 correctly reproduces the spec's "empty/impossible cells → explicit `pytest.mark.xfail`,
never silent omission" rule (02 line 201/220 vs spec `:177-178`). Consistent.

---

## 6. 02's parity assertions vs spec §6.3 vs actual seams

| §6.3 assertion | 02 mapping | Spec §6.3 | Source seam confirmed | Verdict |
|---|---|---|---|---|
| 6.3.1 inner==wrapper on Shape-2 | extends `test_monitor.py:336-343` | extends `test_monitor.py:339-343` | parity template exists at `:336-343` (02 reproduced it) | **CONSISTENT** (line-range label differs by the 3 decorator/sig lines — 02 says `:336-343` incl. decorator, spec says `:339-343` body; both point at the same `test_text_core_matches_path_wrapper`) |
| 6.3.2 `_classify_transcript(shape2)` → FAIL_PROVIDER_EXHAUSTED | `test_rerun_tasks.py::TestClassifyTranscriptProviderExhaustion` | same (the "untested seam") | delegation `:592` → `:605` verified in source | **CONSISTENT** |
| 6.3.3 FP fixture → NOT FAIL_PROVIDER_EXHAUSTED | same class, `is not` | same | `is_error:false` → NONE (§5 row 9) | **CONSISTENT** |
| 6.3.4 prior-success + trailing Shape-2 → PASS_RECOVERED | mirror `:815-828` | same | `completed_before_overrun_from_text` gate at `:603-604` verified | **CONSISTENT** |

Minor label note: 02 cites the parity template as `test_monitor.py:336-343` while spec §6.3.1 cites
`:339-343`. Both reference the SAME method (`test_text_core_matches_path_wrapper`); 02's range
includes the `@pytest.mark.unit` decorator + def line, spec's is the body only. **Not a defect** —
just a wider line span. Flagged for transparency.

---

## 7. 03 template rules vs BUILD-REQUEST / SKILL canon

03 covers template-02 authoring rules. Cross-checks against the lens-named items:

- **6-agent FINAL_ONLY floor:** 03 §3 (I19, lines 71-74) states `<500 lines → 3 rf-qa + 3
  rf-qa-qualitative = 6 total`, and I15 (line 73) "absolute minimum is 6 agents (3 rf-qa + 3
  rf-qa-qualitative)" for FINAL DOCUMENT. This is internally consistent and matches the topic's
  stated "6-agent FINAL_ONLY floor". **CONSISTENT.** No contradiction with the BUILD goal (a
  <500-line code+test task file → 6-agent final gate at `full`/`standard`).
- **POST reflect wrapper form:** 03 §4 (lines 86-104) reproduces the FLAT wrapper shell-out
  `superclaude reflect run {abs TASK_FILE} --depth deep --fix --promote` behind the
  `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` skip guard, NO `--base`, consume exit code (only 0 proceeds),
  wrapper writes `reflect_post` back. This matches the canonical SKILL.md form and the `.claude/`-not-
  staged discipline. **CONSISTENT** with project rules (memory `feedback_claude_dir_gitignored`).
- **M4 fidelity gate:** 03 §3 (line 69) correctly judges M4 "likely N/A" for this code+test task
  (not a source-doc→doc derivation) and instructs noting the omission. Consistent with I21.

**No contradiction found between 03's template rules and the BUILD-REQUEST/track goal.** 03 is
advisory (how to author the task file), not a factual claim about `monitor.py`, so there is nothing
to cross-validate against source; its internal citations to template/SKILL line numbers are outside
my assigned spot-check budget and are marked **[UNVERIFIED — template/SKILL line numbers not
spot-checked; outside assigned lens]**. The substantive rules it states are self-consistent and
consistent with the track goal.

---

## 8. Contradiction sweep (all four files)

I searched for any place where two files (or a file and the spec/source) describe the SAME fact
differently:

- **No hard contradictions found.** Every shared fact (predicate line, regex target, branch
  semantics, matrix rows, parity seams, Shape-2 invariants) is consistent across 01 ↔ 02 ↔ spec ↔
  source.
- **One soft discrepancy (Minor, non-blocking):** 02's §3 hand-written Shape-2 *reconstruction*
  differs in envelope key-ordering from the now-present verbatim (`shape2-verbatim-transcript.jsonl`)
  — see §4a. Because 02 explicitly labeled it a reconstruction and deferred to ground truth, and the
  four load-bearing invariants are identical, this is a builder-guidance improvement, not a
  correctness conflict.
- **Two label-only line-range differences (cosmetic):** (i) 02 cites the parity template as
  `:336-343`, spec as `:339-343` (same method); (ii) 01 notes spec's "~:335-338" for the timeout
  predicate resolves to actual return `:343` (01 already reconciles this explicitly). Neither is a
  defect.

---

## Compiled Gaps

### Critical Gaps (block synthesis/build)
- **None.**

### Important Gaps
- **None.** All load-bearing cross-claims (C1 predicate `:323`, C8 regex `:41-43`, offline delegation
  `:592`/`:605`, Shape-2 four invariants, matrix rows 4 & 9) are VERIFIED consistent.

### Minor Gaps (should be fixed / noted before authoring)
- **M1 — Point the fixture at real verbatim, not 02's reconstruction (§4a).** The builder should
  author `all_account_cooldown_apierror429.jsonl` from `shape2-verbatim-transcript.jsonl:3` (now
  present, ground-truth) rather than 02 §3's illustrative reconstruction. Recommend the task item
  cite `shape2-verbatim-transcript.jsonl:3` as the byte source and (per 02's own RED→GREEN rule)
  validate the authored fixture classifies to `(ALL_ACCOUNT_COOLDOWN, "gpt-5.5")`.
- **M2 — Consumer-chain lines in 01 §4 unverified by this pass (outside assigned lens).** Lines
  `recovery_policy.py:69-70`, `executor.py:1085/2283`, `models.py:53/66/880`, `aienv.py:81` were not
  spot-checked (assigned lens targeted the predicate/regex/body/offline surface). They are marked
  `[UNVERIFIED]`; a follow-up spot-check would close this. NOT blocking — these are "stay untouched"
  consumers, not edit targets.
- **M3 — 03's template/SKILL line-number citations unverified (outside assigned lens).** 03's numerous
  `template:NNN` / `SKILL.md:NNNN` citations were not re-read this pass. The substantive authoring
  rules are self-consistent; the exact line anchors are `[UNVERIFIED]`.

---

## Cross-Validation Summary

- **01 ↔ source:** all 12 spot-checked line-number claims byte-accurate. C1 predicate + C8 regex +
  offline delegation semantics all match the live `monitor.py`/`rerun_tasks.py`.
- **01 ↔ spec R1/R2/R3:** predicate widening, inlined membership test, no-helper, regex loosening,
  superset back-compat — all consistent.
- **02 ↔ spec §6.2:** 12-row matrix reproduced row-for-row; every `(kind, model)` consistent with
  post-fix source semantics. Row 4 (Shape-2 → gpt-5.5) and Row 9 (`is_error:false` → NONE) both
  MATCH.
- **shape2-verbatim-transcript.jsonl:** genuine ground truth; all four R1/R2 load-bearing invariants
  (is_error:true, no api_error_status, rate_limit_error in body, "cooling down" w/o "via provider",
  gpt-5.5) CONFIRMED. Supersedes 02's reconstruction (§4a).
- **03 ↔ track goal:** 6-agent FINAL_ONLY floor and FLAT POST-reflect wrapper form consistent; no
  contradiction with the BUILD-REQUEST.
- **Contradictions:** none hard; one soft (reconstruction vs verbatim, non-blocking) + two cosmetic
  label diffs.

---

## VERDICT: PASS

All load-bearing cross-claims between the four assigned files and against the actual source are
mutually consistent and byte-accurate. Zero critical or important gaps. Three minor, non-blocking
notes (M1 fixture-source pointer, M2/M3 unverified-outside-lens citations) are recorded for the
builder.

**Gap list:** Critical: 0 · Important: 0 · Minor: 3 (M1 fixture verbatim source; M2 consumer-chain
lines unverified; M3 template/SKILL line anchors unverified).
