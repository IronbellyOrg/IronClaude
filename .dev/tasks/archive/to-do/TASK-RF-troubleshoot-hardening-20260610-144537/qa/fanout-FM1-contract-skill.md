# Fanout FM1 — OUTPUT CONTRACT + verdict invariant + SKILL.md mapping

**Partition:** spec changes (CS-1, CS-2, CS-2b, CS-3, CS-4, CS-7, m1) affecting the §6.2 output contract, the C2/M2 verdict invariants, the §6.1 trigger→gate map, and the SKILL.md build items that encode them.

**Inputs read (fully):**

- Refactored spec: `troubleshoot-pipeline-hardening-spec.md` §6.1 (T1–T9 trigger→gate map), §6.2 (13-field contract + status/path rule M7 + verdict invariant C2 + off-path→verdict M2 + no-advisory C3 + defaults M4), §7-H0, §7-H5, §10 acceptance 11–15.
- Change-set: `spec-critique-adjudication.md` CS-1, CS-2, CS-2b, CS-3, CS-3b, CS-4, CS-7, m1.
- Current tasklist: `TASK-RF-troubleshoot-hardening-20260610-144537.md` (456 lines, all items read).

**Headline finding:** the tasklist was authored against the PRE-adjudication spec. It hard-codes the now-obsolete shape in TWO load-bearing ways that are repeated across ~15 items:

1. **"8-field output-contract table"** — the spec is now a **13-field** table (the 4 path fields each gained a sibling `*_status` enum, plus `gate_na_rationale` was added, plus a defaults column). Every "8-field" reference is stale.
2. **The full verdict enum `pass | blocked | advisory | not_applicable` "per GF-5"** — the adjudication (CS-3 / C1+C3) **REMOVES `advisory`**. The enum is now exactly `{pass, blocked, not_applicable}`. The tasklist's Open Question #2 (GF-5) is now factually inverted: it directs the executor to ADD advisory; it must instead direct removal.

These two errors are woven verbatim into the embedded prompts of build items AND QA-lens items, so they propagate into the produced artifacts AND into the gates that would have caught them. Both must be corrected at the source (build items) and in every QA/fidelity prompt that re-asserts them.

A third, larger gap: **the per-gate `status` field, the `gate_na_rationale` map, the defaults column, the C2 verdict invariant, the M2 off-path→verdict rule, and the §6.1 T1–T9 trigger→gate map have NO representation anywhere in the tasklist.** These are net-new spec surfaces (CS-7, CS-2, CS-2b, CS-1, CS-4, m1) that require either heavy edits to existing items or new items.

---

## Per-item analysis

### CS-7 (per-gate status field `{PASS|FAIL|NA|NOT_PROVEN}` distinct from card_path) + CS-4 (defaults) + m1 (known_escapes_caught pattern)

#### Step 2.8 — Append output-contract fields to SKILL.md `## Output Contract` table

- **Current intent (1 line):** Append **8** rows after `diagnosability_hard_stop`: `pipeline_hardening_applicable` (bool), `pipeline_hardening_verdict` (string, FULL enum incl. advisory), 4 `*_card_path` (string|null), `off_path_review_decision` (enum), `known_escapes_caught` (list[string]). 3-column `| Field | Type | Description |`.
- **REQUIRED CHANGE (specific):**
  - Change "**8 new rows**" → "**13 new rows**" (spec §6.2 now has 13 contract fields).
  - **Add a 4th column `Default`** to match the spec §6.2 table (Field/Type/Default/Meaning). If house style must keep 3 columns, fold the default into the Description text per field — but the default values are mandatory content (CS-4): `pipeline_hardening_verdict→not_applicable`, every `*_card_path→null`, every `*_status→NA`, `off_path_review_decision→not_required`, `known_escapes_caught→[]`, `gate_na_rationale→{}`, and `pipeline_hardening_applicable→` "(none — H0 MUST write it before any read)".
  - **Add the 4 missing `*_status` enum rows** (CS-7 — the enabler): `runtime_entrypoint_status`, `contract_ledger_status`, `unmask_sweep_status`, `effective_input_status`, each enum `PASS | FAIL | NA | NOT_PROVEN`, default `NA`. These are DISTINCT from the `*_card_path` rows.
  - **Add the `gate_na_rationale` row:** type `map[gate→string]`, default `{}`, meaning "Required rationale for EVERY gate whose status is `NA`; a `NA` without a rationale entry is invalid and MUST be treated as `NOT_PROVEN`."
  - **`pipeline_hardening_verdict` enum:** change `pass | blocked | advisory | not_applicable` → **`pass | blocked | not_applicable`** (CS-3 — drop advisory).
  - **`known_escapes_caught` type:** change bare `list[string]` → "list[string]; each item MUST match `^E\\d+$` or `^E\\d+\\+$`" (m1 / CS-m1).
  - **Add the status/path rule (M7)** as a note under the table: `*_card_path = null` permitted ONLY when `*_status ∈ {NA, NOT_PROVEN}`; a `PASS`/`FAIL` status MUST carry a non-null path; a gate that ran but produced no artifact is `NOT_PROVEN`, never silent `null`.
- **Change type:** **SPLIT.** This item now carries ~13 fields + a new column + a status/path rule + the no-advisory enum change. Split into: **(2.8a)** append the 5 non-gate rows (`applicable`, `verdict` [no advisory], `off_path_review_decision`, `known_escapes_caught` [pattern-constrained], `gate_na_rationale`) + defaults; **(2.8b)** append the 8 per-gate rows (4 `*_status` + 4 `*_path`) + the M7 status/path rule note. The single-item "8 rows additive" framing understates the work and omits half the fields.
- **Coverage note:** the embedded "mirror `diagnosability_verdict`'s never-silently-skipped enum" guidance is fine, but the executor MUST be told the per-gate `*_status` pattern has no existing analogue in the contract — it is genuinely new and must not be conflated with the `*_card_path` rows.

#### Step 2.1 — Hub ref `pipeline-hardening-closure.md` `## Output contract fields` section

- **Current intent:** Reproduce the §6.2 **8-field** table as a GFM pipe table (Field/Type/Meaning), using FULL enum incl. advisory.
- **REQUIRED CHANGE:** Same field-count + enum + defaults corrections as 2.8 — the hub ref's contract table must be the 13-field table with the `Default` column, drop advisory, add the 4 `*_status` rows + `gate_na_rationale`, add the M7 status/path rule note, and constrain `known_escapes_caught`. Also add the **C2 verdict invariant block** (see CS-2 below) and the **C3 no-advisory note** to this section since the hub ref is the authoritative narrative home of the contract.
- **Change type:** **EDIT (heavy).** Same content delta as 2.8 plus the invariant prose. Do not split — the hub ref legitimately holds the full narrative; just expand the embedded directive.

---

### CS-3 (verdict enum → `{pass, blocked, not_applicable}`; advisory REMOVED)

Every item that names the verdict enum or "advisory" must drop advisory. The literal string `pass | blocked | advisory | not_applicable` (and `{pass, advisory}`) appears in:

| Item | Where advisory appears | Required change |
|---|---|---|
| **Open Question #2 (GF-5), lines 151** | "use the FULL §6.2 enum `pass \| blocked \| advisory \| not_applicable`" and "additive reconciliation" | **INVERT.** Rewrite OQ#2 to state the enum is `{pass, blocked, not_applicable}`; advisory was removed (CS-3/C1+C3) as a dead surface with no emitter and no consumer; `not_applicable` is the legitimate value for a zero-trigger skip (so the skipped-run reconciliation OQ#2 worried about is satisfied by `not_applicable`, not advisory). |
| **Step 2.1 (hub ref)** | enum + `## Remediation gating` ("Tier 3 offer gated on `pipeline_hardening_verdict ∈ {pass, advisory}`") | enum → drop advisory; gating set → `{pass, not_applicable}` (per Step 2.11 which already uses `{pass, not_applicable}` for the Wave 6 precondition — reconcile both to the same set). |
| **Step 2.8 (SKILL Output Contract)** | enum | drop advisory (see CS-7 above). |
| **Step 2.9 (Wave 4.5)** | `Emit "Wave H… complete: verdict=<pass\|blocked\|advisory\|not_applicable>"` | drop advisory → `<pass\|blocked\|not_applicable>`. |
| **Step 2.12 (report-template inside fence)** | `Closure verdict: pass \| blocked \| advisory \| not applicable per GF-5` | drop advisory → `pass \| blocked \| not_applicable`. Note spec §8 uses `not_applicable` (underscore in §6.2; §8 acceptance #11 requires §6.2 and §8 IDENTICAL) — use `not_applicable`, and add the §6.2→§8 mapping note (C1/C3): the line renders `pipeline_hardening_verdict` verbatim, `not_applicable` only when `Applicability: not applicable`. |
| **Step 2.14 (remediation-handoff)** | precondition "`pipeline_hardening_verdict ∈ {pass, advisory}`" | → `{pass, not_applicable}` (reconcile with 2.11). |
| **Step 4.3 (internal-consistency QA lens)** | embedded: "enum is consistently the FULL `pass\|blocked\|advisory\|not_applicable` everywhere (GF-5)" | rewrite the lens assertion to verify enum is `{pass, blocked, not_applicable}` everywhere and that **no file contains the token `advisory`** as a verdict value. As written, this lens would FAIL any correct (advisory-free) output. |
| **Step 5.1 (fidelity agent 1)** | embedded: "full enum `pass\|blocked\|advisory\|not_applicable` per GF-5" | same inversion — fidelity agent must verify advisory is ABSENT, not present. |

- **Change type for all:** **EDIT.** No splits; each is a token/set substitution + (for the two QA prompts) a polarity inversion so the gate checks for the correct post-CS-3 state. **These two QA-prompt inversions (4.3, 5.1) are the highest-risk: if left unchanged, the gates actively enforce the WRONG enum and would reject correct work.**

---

### CS-2 (C2 verdict invariant — closes vacuous pass; absorbs M8 NOT_PROVEN⇒blocked) + CS-2b (M2 off-path→verdict)

The verdict invariant is the apex change and has **no representation in the tasklist** beyond a free-floating "Closure verdict: blocked when any gate NOT PROVEN" mention. The spec §6.2 now defines verdict as a **total function of gate statuses** plus the mandatory-gate-set logic. Affected items:

#### Step 2.11 — Wire failure-state blocking rules (calibration-gate block + Wave 6 precondition + Will Not Do)

- **Current intent:** Add a "pipeline-hardening completeness gate" (MUST NOT set verdict=pass / mark remediated unless H1–H4 cards exist on disk and pass); force `verdict=blocked`+`status: partial` when any required gate is NOT PROVEN/FAIL/N/A-without-rationale; tighten Wave 6 to require `verdict ∈ {pass, not_applicable}`; add a Will-Not-Do bullet.
- **REQUIRED CHANGE:** This item is the natural home for the C2 invariant. It MUST now encode the FULL invariant, not just the NOT_PROVEN clause:
  - `verdict = pass` **iff** `applicable=true (resolved)` ∧ **EVERY gate in the run's mandatory gate set** has `status=PASS` with a non-null path ∧ **ZERO** gates `NOT_PROVEN` ∧ `off_path_review_decision ∈ {performed, not_required, waived_with_rationale}`.
  - `verdict = blocked` whenever ANY mandatory gate is `FAIL`, ANY gate is `NOT_PROVEN`, a required `NA` lacks a rationale, OR `off_path_review_decision = required` ∧ ¬(performed ∨ waived_with_rationale). **(CS-2b / M2 — add the off-path→blocked clause explicitly.)**
  - `verdict = not_applicable` **iff** `applicable=false` (legal only under the zero-trigger skip rule).
  - Add the **vacuous-pass closure statement** (acceptance #12): an all-null/all-NA/`known_escapes_caught=[]` run with `applicable=true` is `blocked`, never `pass`.
  - The on-disk-verification step must check **per-gate status + non-null path coherence (M7)**, not just "cards exist."
  - Wave 6 precondition `{pass, not_applicable}` stays (already correct); add that a `blocked` verdict mechanically prevents the Tier 3 offer.
- **Change type:** **SPLIT.** Currently one item bundles (a) completeness gate, (b) Wave 6 precondition, (c) Will-Not-Do bullet. The C2 invariant + M2 off-path clause + mandatory-gate-set arithmetic is substantial new normative content. Recommend: **(2.11a)** encode the C2 verdict invariant + M2 off-path→blocked + vacuous-pass closure as a dedicated "Verdict invariant" block in SKILL.md (and ensure it matches the hub ref's invariant block from 2.1); **(2.11b)** the existing completeness-gate + Wave 6 precondition + Will-Not-Do wiring (referencing 2.11a's invariant).

#### Step 2.9 — Wave 4.5 mode section (CS-2b mandatory-gate-set + off-path)

- **Current intent:** Insert `### Wave 4.5` walking H0→H1→H2→H3→H4→H5; Emit verdict line; failure-handling table.
- **REQUIRED CHANGE:**
  - The H0 step must now **compute the mandatory gate set from the §6.1 trigger→gate map** (CS-1, see below) — not present a "9 triggers vs 5 mandatory" split.
  - The H5 step must encode **M2**: when any §7-H5 trigger holds, `off_path_review_decision = required`, H5 joins the mandatory gate set, and `required ∧ ¬(performed ∨ waived) ⇒ verdict = blocked`. H5 is **not optional/silently-skippable** — the current "H5 off-path-review decision" framing reads as advisory and must be made mandatory-on-trigger.
  - The Emit line drops advisory (CS-3, above).
- **Change type:** **EDIT (substantive).** No split needed but the H0 and H5 sub-steps gain hard normative content (mandatory-gate-set computation; off-path→blocked).

#### Step 2.12 + Step 2.13 (report-template §8 lines) — CS-2b co-location + status/path/rationale (CS-3b / M3)

- **Current intent (2.12):** Insert `## Pipeline Hardening Closure` section inside the four-backtick fence with the §8 bullet list (each gate line `PASS|FAIL|N/A — <path>`).
- **REQUIRED CHANGE (2.12):**
  - Each gate line status set must become **`PASS | FAIL | NA | NOT_PROVEN`** (add `NOT_PROVEN` — it is a first-class status now, M8/M3) and carry **`— rationale (required if NA): <…>`** (CS-3b / M3). A bare `NA` (no rationale) renders `NOT_PROVEN`.
  - Add the **off-path→verdict consequence co-located on the off-path line** (CS-2b / M2): "Off-path review decision: required | performed | waived_with_rationale | not_required — (if required and not performed/waived_with_rationale ⇒ verdict = blocked)".
  - Add the "Firing triggers / mandatory gate set: T… → H…" line (spec §8 now opens with it — CS-1).
  - `known_escapes_caught` line: note each must match `^E\\d+$` or `E\\d+\\+` (m1).
  - Closure verdict line: drop advisory (CS-3).
- **REQUIRED CHANGE (2.13 — the `## Pipeline Hardening Closure rule` after EOF):** Currently sets `Closure verdict: blocked` when any H1–H4 gate is NOT PROVEN. Must additionally state: (a) `NOT_PROVEN` is a **first-class gate status** (not prose), (b) a bare `NA` without adjacent rationale is invalid and rendered `NOT_PROVEN` (M3/M7), (c) `path=null` legal only for `NA`/`NOT_PROVEN` (M7), (d) the off-path→blocked clause (M2). The existing item is close but understates: it must reference the C2 invariant as the authority, not re-derive a narrower rule.
- **Change type:** **EDIT** both. 2.12 gains 3 new line-level requirements + status-set change; 2.13 gains the M7/M3/M2 clauses.

---

### CS-1 (M1 trigger→gate map, T1–T9) — SKILL.md Wave 4.5 / H0 trigger item

#### Step 2.9 (H0 portion) and Step 2.1 (hub ref `## Trigger` + `## Wave H0`)

- **Current intent (2.1 `## Trigger`):** Reproduce the §6.1 **bullet list** Trigger verbatim plus the skip rule. **Current intent (2.9 H0 step):** walk H0 applicability with `pipeline_hardening_applicable=false` skip path.
- **REQUIRED CHANGE:**
  - The §6.1 Trigger is **no longer a flat bullet list** — it is the **T1–T9 trigger→gate map TABLE** (`| ID | Trigger condition | Mandatory gate(s) it pins |`). Step 2.1's `## Trigger` section must reproduce that **table** (T1→H1,H2; T2→H1,H2; T3→H1,H3; T4→H1,H2,H3; T5→H2,H3; T6→H1,H2; T7→H1,H4; T8→H2,H3; T9→H3) plus the **mandatory-gate rule** ("every firing trigger pins ≥1 gate; the union is the run's mandatory gate set; the C2 invariant reads it; H5 additionally mandatory when its §7-H5 triggers hold").
  - The **skip rule** must be updated (CS-6 territory, but it lands in the same Trigger section): skippable ONLY when **zero** triggers fire; trigger overrides operator skip (non-overridable); `applicable=false` requires the boundary scan justifying "no trigger fired."
  - Step 2.9's H0 sub-step must reference the trigger→gate map (compute mandatory set from the map; **explicitly NOT a separate narrower "5-condition" list** — the old spec's 9-vs-5 split is gone, acceptance #13).
  - The hub ref's `## Wave H0` section (2.1) must state the pass criterion "the mandatory gate set is computed SOLELY from the §6.1 trigger→gate map — no separate narrower list."
- **Change type:** **EDIT (substantive).** The "Trigger bullet list verbatim" directive in 2.1 is now wrong (it's a table) and must also carry the trigger→gate map + mandatory-gate rule. No split, but the embedded directive must be rewritten from "bullet list" → "T1–T9 table + mandatory-gate rule + skip-rule-with-precedence."

---

## Coverage gaps — spec changes with NO corresponding tasklist item (NEW items needed)

| Spec change | Gap | New item needed |
|---|---|---|
| **CS-7 per-gate `*_status` (4 fields)** | No tasklist item creates the `*_status` rows; 2.8 only knows the 4 `*_path` rows. | Folded into split **2.8b** (above). If not split, a NEW item to add the 4 status rows + M7 rule. |
| **`gate_na_rationale` field + "bare NA ⇒ NOT_PROVEN" rule** | Absent everywhere. | Folded into **2.8a** + **2.12/2.13** (rationale on report lines). No standalone item, but MUST be added — currently zero coverage. |
| **CS-4 defaults column** | No item mentions defaults at all. | Folded into **2.8a/2.8b**; needs the `Default` column or per-field default text. Currently zero coverage. |
| **CS-2 C2 verdict invariant (total function + mandatory-gate-set arithmetic)** | Only a narrow NOT_PROVEN⇒blocked fragment exists (2.11/2.13). The full iff-invariant, the vacuous-pass closure (acceptance #12), and the mandatory-gate-set dependency are absent. | **NEW item 2.11a** (above) — dedicated verdict-invariant block in SKILL.md + matched in hub ref (2.1). |
| **CS-1 trigger→gate map (T1–T9 table + mandatory-gate rule)** | Tasklist assumes a flat §6.1 bullet "Trigger list." The T-IDs, the per-trigger gate pins, and "no separate 5-list" (acceptance #13) are absent. | Folded into **2.1** + **2.9** edits (above). High risk if missed — the H0 mandatory-set computation has no source without it. |
| **m1 `known_escapes_caught` regex pattern `^E\\d+$`/`E\\d+\\+`** | Item 2.8 says bare `list[string]`. | Folded into **2.8a**. |
| **M11 consumer-discovery manifest ⇒ H2 NOT_PROVEN** (spec §7-H2, acceptance #15) | The H2 ref item (Step 2.3) reproduces only the 9-row ledger + 3 blocking bullets. The spec §7-H2 now ALSO requires a **consumer-discovery manifest** (exact search terms + symbol/ref-search results) as evidence, with "absence ⇒ H2 NOT_PROVEN." **This is in §7-H2 which is NOT in this fanout's primary partition (FM1 = contract+SKILL), but it directly governs the H2 `contract_ledger_status` contract field** — flagging for the H2/gate-ref fanout owner. | Out of FM1's edit scope; **FLAG to the §7-gate-ref fanout**: Step 2.3 must add the manifest requirement + NOT_PROVEN-on-absence blocking bullet. |

(M5 H4 no-op/FAIL, M9 H3 fixpoint, M10 E3 fixture are §7-H3/H4 surfaces — outside FM1's contract+SKILL partition; noted only so the contract-side `effective_input_status`/`unmask_sweep_status` semantics stay consistent. Defer to the gate-ref fanout.)

---

## Mapping table

| CS-id | Tasklist item(s) | Change type | One-line directive |
|---|---|---|---|
| **CS-7** (per-gate status, distinct from path) | 2.8 → **split 2.8a/2.8b**; 2.1 (hub) | split + edit | Add 4 `*_status` enum rows `{PASS\|FAIL\|NA\|NOT_PROVEN}` distinct from the 4 `*_path` rows; add the M7 status/path rule (`path=null` only for NA/NOT_PROVEN; ran-but-no-artifact = NOT_PROVEN). |
| **CS-4** (defaults) + **m1** (escape pattern) | 2.8a; 2.1 | edit | Add a `Default` column (or per-field default text): verdict→not_applicable, paths→null, statuses→NA, off_path→not_required, escapes→[], gate_na_rationale→{}, applicable→H0-must-write; constrain `known_escapes_caught` to `^E\\d+$`/`^E\\d+\\+$`. |
| **CS-3** (drop advisory) | OQ#2/GF-5, 2.1, 2.8, 2.9, 2.12, 2.14, **4.3**, **5.1** | edit (incl. 2 prompt inversions) | Enum is exactly `{pass, blocked, not_applicable}` everywhere; delete `advisory`; **invert QA-lens 4.3 and fidelity-agent 5.1** to verify advisory is ABSENT (they currently mandate it); rewrite OQ#2 to say advisory was removed and `not_applicable` covers the skip case. |
| **CS-2** (C2 verdict invariant ⊇ M8) | 2.11 → **split 2.11a/2.11b**; 2.1 (hub); 2.13 | split + edit | Encode verdict as a total function of gate statuses (pass iff all mandatory gates PASS+non-null path ∧ zero NOT_PROVEN ∧ off-path satisfied; else blocked; not_applicable iff applicable=false); state vacuous-pass is `blocked` (acceptance #12). |
| **CS-2b** (M2 off-path→verdict + H5 mandatory) | 2.9 (H5 step); 2.11a; 2.12 (off-path line); 2.14 | edit | H5 is mandatory-on-trigger (not optional); `off_path_review_decision=required ∧ ¬(performed∨waived) ⇒ verdict=blocked`; co-locate this on the §8 off-path report line (2.12). |
| **CS-1** (M1 trigger→gate map T1–T9) | 2.1 (`## Trigger`+`## Wave H0`); 2.9 (H0 step); 2.12 (T→H line) | edit (substantive) | Replace the flat "§6.1 Trigger bullet list" with the **T1–T9 trigger→gate map table** + mandatory-gate rule; H0 computes the mandatory set SOLELY from the map (no separate 5-condition list — acceptance #13). |
| **m1** (escape regex) | 2.8a; 2.12 | edit | `known_escapes_caught` items match `^E\\d+$` or `^E\\d+\\+$` (so `E6+` valid). |
| **M11** (H2 manifest — OUT OF FM1 SCOPE) | 2.3 (H2 gate ref) | flag to gate-ref fanout | H2 ref must add the consumer-discovery manifest requirement; absence ⇒ `contract_ledger_status = NOT_PROVEN`. |
