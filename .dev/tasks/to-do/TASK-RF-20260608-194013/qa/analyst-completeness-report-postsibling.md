# rf-analyst Completeness-Verification Report — POST-SIBLING REFRESH

- **Analysis type:** completeness-verification (refresh against a changed baseline)
- **Gate:** pre-Phase-2 re-gate (operator-authorized; see task Deviations from Process)
- **Track:** single-track `--reflect <none|0|1|2|auto>` POST-gate dial refactor
- **Spec:** `.dev/brainstorms/20260608-191030-reflect-flag-post-gate/merged-requirements.md` (986 lines; FR-1..FR-13, NFR-1..NFR-8)
- **Scope (claimed):** EXACTLY 2 files — `src/superclaude/skills/task-builder/SKILL.md` + `src/superclaude/agents/rf-qa.md`
- **Baseline change:** sibling `TASK-RF-20260608-185553` landed as HEAD `015e7285` (SKILL.md 2308→2344 lines; `POST_REFLECT_MODE: halt|wrapper` is now LIVE; the single POST item is now a 2-arm `wrapper|halt` branch)
- **Prior report:** `qa/analyst-completeness-report.md` — VERDICT PASS on 2026-06-08 against the PRE-sibling baseline
- **Date:** 2026-06-09
- **Stance:** ADVERSARIAL + ZERO-TRUST — find coverage gaps NEWLY created by the sibling landing; re-verify spec→plan completeness against live source at HEAD. Prior claims trusted only after independent re-read.

**Inputs read (this session):** sibling diff (`git show 015e7285 -- SKILL.md` + `--stat`); full spec (986 lines, both pages); prior completeness report (full); the task file (all 340 lines: steps Phase 1–6, Open Questions, the orchestrator's Phase-1 drift map); live `SKILL.md` POST surfaces (:41, :201, :853-858, :1425, :1960, :2014-2035, :2085, :2142, :2150-2188, INV-010 :1336-1347); live `rf-qa.md` (:138/:184/:298 count headers, :330 region heading, TB-Add-1..8 :334-378); grep over `rf-task-builder.md` for POST tokens.

---

## VERDICT: PASS (plan is complete + correctly scoped against the post-sibling baseline)

**0 builder-blocking gaps. 3 step-reframings REQUIRED (all already captured in the task's Phase-1 drift map + Open Questions — none is an uncovered gap). 2 advisories.**

The sibling landing reverses one load-bearing premise (INV-005 "no live collision" → there IS now a live `POST_REFLECT_MODE` field to retire) and restructures the single POST item into a 2-arm branch. **Every consequence of that reversal is already accounted for** in the task file: the orchestrator's Phase-1 Findings drift map (task lines 261–311) caught it, surfaced it to the operator, and the operator authorized this exact re-gate. The four step-reframings the drift map enumerates (Steps 2.2/2.3, 3.2, 3.5) are correct and sufficient. The spec direction is unchanged (the §5 alias map `wrapper→2`, `halt→halt` was always designed to consume `POST_REFLECT_MODE`; it now consumes a present field instead of an absent one). The V15 byte-anchor survived the sibling byte-for-byte. The 2-file scope still holds — the sibling touched only SKILL.md among the agent surfaces, and `rf-task-builder.md` carries no POST-item body.

---

## 1. SPEC→PLAN COVERAGE MATRIX (refreshed against live HEAD)

Each FR/NFR is mapped to the implementing task STEP and the **live** target surface that step edits. Status: **covered** (step + live surface align as written) / **needs-reframe** (step targets a surface the sibling changed; the task already records the reframe) / **gap** (no step, or a surface that vanished).

### Functional Requirements (13)

| Req | Implementing step | Live target (verified at HEAD) | Status |
|---|---|---|---|
| FR-1 — one dial `{none,0,1,2,auto}`, default 2, MALFORMED on unknown | 2.1 (Input doc) + 2.4 (A.9 producer, unknown-token STOP) | `SKILL.md:41` (`--spec` Input doc adjacency, intact); A.9 `### A.9` region | covered |
| FR-2 — `none\|0` disables; no item; `reflect_post:` omitted | 3.1 (mode-conditional sentinel) + 3.2 (§6.1 no-item arm) | frontmatter `reflect_post: ""` now `:1960` (was :1942); POST item branch `:2014-2033` | covered |
| FR-3 — Mode 1 inline `/sc:reflect --depth standard`, no remediate/Agent | 3.2 (§6.2 arm) + 3.5 (Rule 19 mode-conditioning — the FR-3 fix) | POST item branch `:2014-2033`; Rule 19 `:2142` (sibling-rewritten) | **needs-reframe** (Rule 19) |
| FR-4 — Mode 2 Bash `superclaude reflect run {TASK_FILE}` | 3.2 (§6.3 arm) | live **wrapper arm** `:2026-2033` is the Mode-2 basis | **needs-reframe** (build ON the wrapper arm, not net-new) |
| FR-5 — `auto` resolves 1/2 deterministically (§4 FER) | 2.4 (A.9 predicate) | A.9 region; TCS signals S5 `:2162` / S6 `:2163` / formula `:2168±` | covered |
| FR-6 — `--reflect` subsumes legacy fields (§5 total map) | 2.3 (retire schema fields) + 2.4 (§5 map in producer) | `POST_REFLECT_GATE` `:853` **AND** live `POST_REFLECT_MODE` `:857` | **needs-reframe** (retire TWO live fields, not one) |
| FR-7 — every non-`none` item HALTs + writes `reflect_post` back | 3.2 (all arms) | POST item branch `:2014-2033` (both live arms already HALT + write-back) | covered |
| FR-8 — `--remediate` scope mode-fixed; Tier-3 → Open Questions | 3.2 (§6.2 audit-only / §6.3 wrapper-remediate) | wrapper arm `:2030-2033` (delegates remediate to wrapper) | covered |
| FR-9 — single producer at A.9; MODE-MATCH oracle | 2.4 (resolve once) + 4.1 (MODE-MATCH in TB-Add-9) | A.9 region; `rf-qa.md` Structural Gate region `:330+` | covered |
| FR-10 — Mode-2 wrapper-availability probe + frozen fallback (§8) | 2.4 (W probe + ladder) | A.9 region (probe is build-time, additive) | covered |
| FR-11 — Mode-1 nesting-boundary guard (runtime PRIMARY) | 3.2 (§6.2 Verification branch) | POST item branch `:2014-2033` | covered |
| FR-12 — `--spec` threading across modes | 2.1/2.2 (`SPEC_PATH`) + 3.2 (Mode-1 `--spec`) | `SPEC_PATH` A.2 `:201` (intact); `spec_path:` frontmatter | covered |
| FR-13 — advisory WARNING on under-rigorous fixed-1 | 2.4 (§10.4 WARNING in producer) | A.9 region | covered |

### Non-Functional Requirements (8)

| Req | Implementing step | Live target | Status |
|---|---|---|---|
| NFR-1 — no reflect-logic duplication | 2.4 + 3.3 (depth note is doc-only) | A.9 + TCS section `:2150` | covered |
| NFR-2 — byte-for-byte reversibility (V15) | 1.1 (V15 snapshot) + 3.2 (§6.4 halt arm) + 5.4 (byte diff) | live halt arm `:2017-2024` (sibling preserved it byte-identical) | covered |
| NFR-3 — single SoT field `reflect_post_mode` | 3.1 (frontmatter field) + 2.4 (single write) | frontmatter near `:1960` | covered |
| NFR-4 — extensibility (one new row) | 4.1 (TB-Add-9 reuses fixed bodies) | `rf-qa.md` TB-Add-9 | covered |
| NFR-5 — determinism (TCS + W boolean) | 2.4 (pure-arithmetic predicate) | TCS `:2150-2188` | covered |
| NFR-6 — SoT discipline (`src/`→`make sync-dev`) | 5.1 (sync + verify-sync) | Makefile targets | covered |
| NFR-7 — no-nesting guard testable | 3.2 (Mode 2 = Bash) + 4.1 (V8) + 5.5 (test) | wrapper arm `:2026-2033`; TB-Add-9 | covered |
| NFR-8 — fail-closed posture | 2.4 (degrade→manual-HALT, never silent Mode 1) | A.9 ladder | covered |

**No FR/NFR has zero coverage. Three FRs (FR-3 via Rule 19, FR-4, FR-6) carry a `needs-reframe` flag — all three are because their target surface SHAPE changed under the sibling, and all three reframes are already enumerated in the task's Phase-1 "Steps needing target-shape adjustment" block (task lines 297–307). None is an uncovered gap.**

---

## 2. SCOPE RE-CONFIRMATION — still EXACTLY 2 files

### 2a. The sibling commit's file list (did it introduce a THIRD-file surface?)

`git show --stat 015e7285` — the sibling modified, among the in-scope agent/skill surfaces, **only** `src/superclaude/skills/task-builder/SKILL.md` (+31/−1). Its other 22 changed files are the NEW wrapper package (`src/superclaude/cli/reflect/*`, `tests/cli/reflect/*`, +4 lines in `cli/main.py`) — all OUT OF SCOPE for this task (the wrapper is the sibling's deliverable; this task is a hard non-goal on it per spec §11).

**Critically: the sibling did NOT touch `src/superclaude/agents/rf-qa.md` and did NOT touch `src/superclaude/agents/rf-task-builder.md`.** So neither agent file's state changed since the prior completeness gate. No third in-scope file surface was introduced.

### 2b. `rf-task-builder.md` carries NO POST-item body (re-confirmed by grep at HEAD)

```text
$ grep -nE "POST_REFLECT|REFLECT_POST|reflect_post|MODE-MATCH|post-execution refl|penultimate|1994|wrapper arm" \
    src/superclaude/agents/rf-task-builder.md
(zero matches)
```

The emitted POST-item BODIES (the halt arm, the wrapper arm, the per-mode templates) and the Output-Structure frontmatter template all live in **`SKILL.md`**, not in `rf-task-builder.md`. The rf-task-builder agent carries no competing copy the task would need to edit. This re-confirms OQ-3 and the prior report's down-rating of file-01's 3-file over-statement. **The 2-file scope holds.**

### 2c. `rf-qa.md` POST surfaces (the second in-scope file — unchanged by the sibling)

```text
$ grep -nE "Checklist \([0-9]+ items\)|TB-Add-1 through|Structural Gate Additions" src/superclaude/agents/rf-qa.md
298:#### Checklist (28 items)
330:#### Structural Gate Additions (TB-Add-1 through TB-Add-7, imported from sc:tasklist 17-point gate …)
```

`rf-qa.md` is at TB-Add-1..8 (checklist item 28); there is **no** `MODE-MATCH`, no `reflect_post`, no `TB-Add-9` yet — exactly the pre-sibling state the prior report and research-03 recorded. Step 4.1 (insert TB-Add-9 as item 29, inside the bounded region, matching the INV-010 regex `^[0-9]+\. \*\*TB-Add-([0-9]+):`) and Step 4.2 (bump `(28 items)`→`(29 items)`; fix the `TB-Add-1 through TB-Add-7`→`…-9` heading) remain exactly correct. The pre-existing `7`-vs-`8` heading drift (heading says "through TB-Add-7" but TB-Add-8 already exists) is unchanged and is correctly folded into Step 4.2.

**SCOPE VERDICT: EXACTLY 2 files (`SKILL.md` + `rf-qa.md`) — re-confirmed at HEAD with grep evidence. No third-file surface introduced by the sibling.**

---

## 3. NEW GAPS FROM THE SIBLING — coverage NOT in the pre-sibling research

The research (01–06) and the prior completeness gate were written when `POST_REFLECT_MODE` was ABSENT from live source (prior report Advisory-1/GAP-4: *"grep over live SKILL.md returns NOTHING for either token — sibling NOT merged, no live collision"*). That premise is now FALSE. Below is each sibling-introduced surface, with a verdict on whether an EXISTING step covers it.

| # | Sibling-introduced live surface | Verified location | Covered by | Verdict |
|---|---|---|---|---|
| N1 | `POST_REFLECT_MODE: <halt\|wrapper>` schema sub-field | `SKILL.md:857` | **Step 2.3** (drift-map reframe: "retire BOTH `POST_REFLECT_GATE:853` AND the now-live `POST_REFLECT_MODE:857`") | COVERED (reframed) |
| N2 | `POST_REFLECT_MODE` component doc (full prose block) | `SKILL.md:1874-1886` (grep-confirmed `:1874`) | **Step 2.2/2.3** (drift-map: "the sibling's `POST_REFLECT_MODE` component doc … must also be reconciled (retire/redirect to `REFLECT_POST_MODE`)") | COVERED (reframed) |
| N3 | 2-arm `wrapper\|halt` POST branch (replaces single item) | `SKILL.md:2014-2033` (halt arm :2017-2024; wrapper arm :2026-2033) | **Step 3.2** (drift-map: "must replace the 2-arm `wrapper\|halt` branch, not a single fixed POST item. The wrapper arm is the basis for Mode 2; the halt arm → halt/2-degraded-halt") | COVERED (reframed) |
| N4 | Rule 19 ALREADY rewritten to reference `POST_REFLECT_MODE: halt\|wrapper` | `SKILL.md:2142` | **Step 3.5** (drift-map: "Rule 19 was already rewritten by the sibling … the dial rewrite reconciles against THAT version, not the pre-sibling version research 01 Surface 8 captured") | COVERED (reframed) |
| N5 | `start_commit` capture comment + Critical Rule #20 (audit F3) | `SKILL.md:2008` comment; Rule 20 `:2144` | Step 1.1 already records `start_commit`; Step 3.x edits don't conflict with Rule 20 (additive, `POST_REFLECT_GATE: ENABLED`-conditioned) | COVERED (no edit needed — orthogonal) |
| N6 | `EXECUTOR_CLASS` schema sub-field (audit F3) | `SKILL.md:858` | Not a dial concern; Step 2.3 retains the surrounding sub-fields. The dial retires `POST_REFLECT_GATE`/`POST_REFLECT_MODE` but `SPEC_PATH`/`TASK_FILE`/`EXECUTOR_CLASS` are preserved (spec §10.2) | COVERED (preserved, not retired) |

### 3a. The one substantive NEW consideration the research did not pre-author (ADVISORY, not a gap)

The sibling's **wrapper arm** (`:2026-2033`) is a near-exact realization of the spec's §6.3 Mode-2 template — it already does `superclaude reflect run {TASK_FILE} --depth {DEPTH}` as a Bash shell-out, writes the structured `reflect_post:` block back, and dual-gates on exit-code + `reflect_post.verdict == pass`. **This is a net POSITIVE for the task, not a gap:** Step 3.2's Mode-2 arm can be derived from (or recognized as already-matching) the live wrapper arm rather than authored from scratch. Two spec-vs-live deltas the executor must reconcile when folding the wrapper arm into Mode 2 (both MINOR, both inside Step 3.2's remit):

1. **Command form.** Live wrapper arm: `superclaude reflect run {TASK_FILE} --depth {DEPTH}` (passes `--depth` explicitly). Spec §6.3 FR-4/AT-FR4 testable: `superclaude reflect run {TASK_FILE}` (wrapper derives depth itself). The spec's §6.3 prose says *"the wrapper derives … `--depth {DEPTH}`"* — i.e., spec intends the wrapper to own depth. The live arm passing `--depth {DEPTH}` is a benign superset (the builder bakes the TCS passthrough, spec FR-4 *"The builder bakes the TCS-derived `--depth` … as passthrough"*). **These are reconcilable — the spec FR-4 text explicitly endorses baked-depth passthrough.** rf-qa V7 asserts the Bash `superclaude reflect run {TASK_FILE}` substring is present, which both forms satisfy. Executor should keep the `--depth {DEPTH}` passthrough (matches FR-4) and ensure V7's substring check tolerates the trailing `--depth` flag.
2. **Title string.** Live wrapper-arm title: *"Independent post-execution reflection gate (automated wrapper, fail-closed)"* (grep `:2028`). Spec §6.3 title: *"Independent post-execution reflect gate (wrapper subprocess, HALT)"*. The §6.3.1 unified diff is the authoritative byte-delta; the executor should emit the §6.3 title for Mode 2 (the spec is authoritative for the dial's templates). NOT a blocker — Step 3.2 already cites §6.3/§6.3.1 as the literal source.

This is an ADVISORY for the executor (fold the live wrapper arm INTO Mode 2 rather than ignore it), not a coverage gap — Step 3.2 already targets the §6.3 template and the 2-arm branch is the documented replace-target.

---

## 4. OQ-1 (8-value oracle) RE-CONFIRM against the post-sibling baseline

OQ-1 is a SPEC-INTERNAL inconsistency, not a code-state fact — the sibling landing does NOT touch it (the sibling added no `reflect_post_mode` value-set surface). I re-verified the spec citations:

- **§10.3 (`merged-requirements.md:848`)** enumerates **7** values: `none | 1 | 2 | auto-resolved-1 | auto-resolved-2 | halt | 2-degraded-halt`.
- **§8.2 fallback ladder (`:678`)** REQUIRES `auto-resolved-2-degraded-halt` (row `auto / 2 / false`).
- **§9.1 V16 (`:739`)** and **§9.2 active map (`:749`)** and **§9.3 MODE-MATCH (`:766`)** all reference `auto-resolved-2-degraded-halt` in the halt/degraded row.

So the 8th value (`auto-resolved-2-degraded-halt`) is REQUIRED by §8.2/§9.1/§9.2/§9.3 but OMITTED by §10.3's enumeration. The **8-value union is the only internally-consistent oracle** — without it, a degraded `auto→2` (wrapper-absent) case cannot be validated by V16/MODE-MATCH. The task's resolution (Steps 3.1, 4.1, 5.3, OQ-1) — **use the 8-value union, flag the upstream §10.3 correction as out-of-scope** — is still correct and still the right call. **Unaffected by the sibling. PASS.**

One refinement worth noting: the prior report (Advisory-1) and OQ-1 both frame this as "spec lists 7, use 8." That framing is unchanged and correct. The sibling does not add or remove any `reflect_post_mode` value (it uses the disjoint `POST_REFLECT_MODE: halt|wrapper` 2-value field, which the dial RETIRES — it is not a `reflect_post_mode` value). No collision between the sibling's 2-value `POST_REFLECT_MODE` and the dial's 8-value `reflect_post_mode`: the former is a deprecated INPUT alias, the latter is the resolved OUTPUT oracle (spec §5/§10.1). Re-confirmed consistent.

---

## 5. TESTABILITY (research 06) — bounded surface unaffected by the sibling

Research 06's verification surface rests on two facts, both re-verified unaffected:

1. **No `build_tasklist()` entry point exists** — the builder is an LLM-driven markdown emitter, so ~7-8 of the §13 ATs have a builder-runtime `(c)` core with no Python harness. The sibling added a `superclaude reflect run` CLI (`src/superclaude/cli/reflect/`) with 35 tests, but **that is the WRAPPER's test surface, not the task-builder's** — it does NOT introduce a `build_tasklist()` entry point and does NOT change the task-builder's "LLM markdown emitter, fixture-based content assertions only" testability profile. Step 5.5's bounded approach (fixture `.md` + content-marker + V-rule re-impl, modeled on `tests/audit/test_evidence_bound_tb_add_8.py` and `tests/skills/test_task_builder_merge.py`) is unchanged and still correct.
2. **The CI gates that fire** (markdownlint on the two `src/` files, `make verify-sync`, full `pytest`) are unchanged. The sibling's new `tests/cli/reflect/` suite is additive and orthogonal — it does not gate this task's two-file edit.

`TESTING_REQUIREMENTS: UNIT (scoped)` remains the correct value. The Step-5.5 test (`tests/skills/test_reflect_mode_validation.py`) targeting AT-VALIDATION-1 / AT-MISMATCH-1 / AT-MODE-MATCH / AT-PLUMBING-1 + the 8-value content marker is unaffected. **PASS.**

> Note (advisory): Step 5.5's fixture tasklists must use a POST item shaped per the NEW dial templates (Mode-1/Mode-2/halt arms), NOT the live 2-arm `wrapper|halt` sibling branch. This is inherent to the test's purpose (validate the dial) and already implied by Step 5.5's spec references; no reframe needed, just flagged so the executor authors dial-shaped fixtures.

---

## 6. CONTRADICTION / STALENESS audit (prior report vs live HEAD)

| Prior-report claim | Live-HEAD reality | Resolution |
|---|---|---|
| Advisory-1 / GAP-4: *"grep over live SKILL.md returns NOTHING for `POST_REFLECT_MODE`/`REFLECT_POST_MODE` — sibling NOT merged, no live collision; reconciliation is forward-looking (INV-005)"* | `POST_REFLECT_MODE` is **LIVE** at `:857` (schema), `:1874-1886` (doc), `:2014-2033` (2-arm branch), `:2142` (Rule 19) | **STALE — correctly superseded.** Task Phase-1 Findings (lines 261–311) caught this reversal, surfaced it to the operator, and drives this re-gate. The reconciliation is now a LIVE retirement, not forward-looking. Direction unchanged; §5 alias map still applies. NOT a contradiction in the PLAN — the plan's drift map already corrected it. |
| Advisory-2: *"`rf-task-builder.md` carries no POST-item body; 2-file scope holds"* | grep at HEAD: zero POST tokens in `rf-task-builder.md` | **STILL TRUE.** Re-confirmed (§2b). |
| Advisory-4 / OQ-6: *"spec `:2094` citation for MODE-MATCH is Critical Rule 12, not a check surface"* | unaffected by sibling; MODE-MATCH lands in rf-qa.md TB-Add-9 | **STILL TRUE.** Unchanged. |
| V15 byte-anchor at `:1994-1999` | sibling relocated it to `:2017-2024` under a `**Halt arm**` subheading, byte-for-byte preserved | **STALE LINE NUMBER, INTACT CONTENT.** Step 1.1 already captured the V15 snapshot from live HEAD and confirmed byte-identity. Drift map records the relocation. NOT a gap. |

No contradiction remains unresolved in the PLAN. Every staleness the prior report carried is explicitly corrected by the task's Phase-1 drift map.

---

## 7. ADVISORIES (non-blocking)

1. **A.9 producer prose region — confirm seam before Step 2.4.** The `### A.9` region absorbed the sibling's +29-line shift below line ~856. Step 2.4 authors the resolution producer prose into A.9; the executor should re-locate the exact A.9 insertion seam at runtime (Step 2.4 already instructs reading `:785-:856` — that range is the schema-block area; confirm the producer-prose insertion point lands AFTER the schema block and the sibling's `EXECUTOR_CLASS`/`POST_REFLECT_MODE` lines, near `:858`). Mechanical; Step 2.4's "read the A.9 seam" instruction covers it.

2. **Minor line-number drift in the task's Phase-1 drift map.** The drift map's live anchors are accurate on SHAPE but a few are off by a small offset from this session's grep (e.g., drift map lists validation-checklist bullet at `:2080`, live grep = `:2085`; Rule 19 at `:2137`, live grep = `:2142`; PRE cross-ref `:1424`, live = `:1425`). This is benign — every Step re-reads its anchor by CONTENT before editing (each step says "read … to confirm"), so the small numeric drift self-corrects at execution time. Flagged for honesty; not a blocker.

---

## VERDICT: PASS

**The task's spec→implementation plan is COMPLETE and CORRECTLY SCOPED against the post-sibling baseline at HEAD `015e7285`.**

- **0 builder-blocking gaps.** Every FR-1..FR-13 and NFR-1..NFR-8 has an implementing step targeting a live, verifiable surface.
- **Scope re-confirmed EXACTLY 2 files** (`SKILL.md` + `rf-qa.md`) with grep evidence; the sibling introduced no third in-scope surface (it touched only SKILL.md among agent/skill files; rf-qa.md and rf-task-builder.md are untouched; rf-task-builder.md carries no POST-item body).
- **The sibling's load-bearing reversal is fully absorbed by the plan.** The 6 sibling-introduced surfaces (N1–N6) are all covered by existing steps; the 3 `needs-reframe` items (Steps 2.3, 3.2, 3.5) are already enumerated verbatim in the task's Phase-1 drift map (task lines 297–307) as operator-surfaced reframings. No NEW step is required.
- **OQ-1 8-value oracle, V15 byte-anchor, and the bounded test surface are all unaffected by the sibling.** Re-confirmed consistent.

**Step reframings the executor MUST apply (already in the task's drift map — re-affirmed here):**
- **Step 2.3** — retire BOTH `POST_REFLECT_GATE` (`:853`) AND the now-LIVE `POST_REFLECT_MODE` (`:857`) into the single `REFLECT_POST_MODE` field (not "replace one line + comment about a hypothetical alias").
- **Step 2.2/2.3** — also reconcile the sibling's `POST_REFLECT_MODE` COMPONENT DOC at `:1874-1886` (retire/redirect to `REFLECT_POST_MODE`).
- **Step 3.2** — replace the live 2-arm `wrapper|halt` branch (`:2014-2033`); the wrapper arm (`:2026-2033`) is the basis for Mode 2; the halt arm (`:2017-2024`) → `halt`/`2-degraded-halt`; Mode 1, `none`, `auto` are net-new. Emit the spec §6.3 title (not the live "automated wrapper, fail-closed" title) and keep the FR-4-endorsed `--depth {DEPTH}` passthrough.
- **Step 3.5** — Critical Rule 19 (`:2142`) is ALREADY sibling-rewritten to reference `POST_REFLECT_MODE: halt|wrapper`; the dial rewrite reconciles against THAT live version, not the pre-sibling version research-01 Surface 8 captured.

**Advisory (no reframe, just confirm at runtime):** Step 2.4 A.9 producer-prose insertion seam now sits after the sibling's `:857-858` schema lines; Step 5.5 fixtures must be dial-shaped, not sibling-2-arm-shaped. Both are inherent to the steps as written.

The re-gate confirms the prior PASS still holds **after correcting its one stale premise (INV-005)** — which the task's own Phase-1 drift map already corrected. The executor may proceed to Phase 2 with the rebased anchors and the four affirmed reframings.
