# Research: FX7 reflect contract

Status: Complete
Date: 2026-07-03
Researcher: R3 (Integration Points + Data Flow for FX7 honest-degrade accounting)
Scope: `src/superclaude/cli/reflect/*.py` (+ frontmatter writer/validator location; + additive-safety consumer sweep)

Worktree root (all paths below are relative to it):
`/config/workspace/IronClaude/.dev/worktrees/pr209-harden`

---

## 0. Executive orientation — TWO distinct "contracts", do not conflate

There are two artifacts named "contract" in the reflect wrapper. FX7 touches
BOTH, at different files:

1. **`return-contract.yaml`** — the machine artifact the wrapper reads to derive
   a verdict. It has TWO producers:
   - **Primary (skill path):** the `/sc:reflect` child (skill
     `sc-reflect-protocol`) authors it. Schema lives in
     `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (§ ~700-950). This is
     R7's territory but is cited below where it bears on FX7.
   - **Wrapper/ensemble path (IN SCOPE):** when the wrapper runs the Tier-2
     swarm itself (FR-RH2), it SYNTHESIZES the contract dict from swarm worker
     facts in `build_reflect_contract` (`ensemble.py:492`) and writes it via
     `_emit_reflect_contract(config.contract_path, contract)` (`ensemble.py:328`).
     **This is the FX7 "return-contract builder" inside cli/reflect.**
2. **`reflect_post:` frontmatter block** — written back into the tasklist by the
   wrapper after deriving a verdict. Builder = `_build_reflect_post_value`
   (`runner.py:93`); writer = `write_reflect_post` (`runner.py:120`); reader =
   `_read_existing_reflect_post` (`runner.py:298`). **This is the FX7
   "reflect_post frontmatter validator/writer".**

The **verdict derivation** (consumer of #1, feeds #2) lives in
`contract.py:derive_verdict` (`contract.py:130`) + `_degraded_reason`
(`contract.py:249`). FX7's degrade rules (verification_ran:false => degraded,
reviewer_count<requested => degraded_components) are ALREADY partly enforced
here — the gap is that the ensemble BUILDER emits a **vacuously-exempt** contract
that dodges the existing degrade triggers. See §3 for the exact leak.

---

## 1. The return-contract model — fields, types, defaults (Deliverable 1)

**IMPORTANT:** `return-contract.yaml` is parsed as a **plain `dict`** (PyYAML
`safe_load`), NOT a dataclass. See `parse_contract` (`contract.py:65-82`) which
returns `dict | None`. There is no dataclass schema for the return-contract; the
field set is defined implicitly by (a) the builder `build_reflect_contract`
(`ensemble.py:536-568`) and (b) the reader keys in `contract.py`.

### 1a. The DERIVED result dataclass — `ReflectResult` (`models.py:117-157`)

This is the wrapper's internal verdict object (built from the parsed contract),
NOT the on-disk contract. Fields (all `models.py`):

| Field | Type | Default | Line |
|---|---|---|---|
| `verdict` | `Verdict` | (required) | 126 |
| `status` | `str \| None` | (required) | 127 |
| `tier_reached` | `int \| None` | (required) | 128 |
| `reason` | `str` | (required) | 129 |
| `report_path` | `str \| None` | (required) | 130 |
| `contract_path` | `str \| None` | (required) | 131 |
| `deviations` | `dict[str, int]` | `{}` (field factory) | 132 |
| `child_exit_code` | `int \| None` | `None` | 133 |
| `write_status` | `str` | `""` | 134 |
| `fix_iterations` | `int` | `0` | 137 |
| `fix_converged` | `bool` | `False` | 138 |
| `remediation_task_path` | `str \| None` | `None` | 139 |
| `reviewer_isolation` | `str` | `"disabled"` | 150 |
| `audit_tree_dirty` | `bool` | `False` | 151 |
| `reviewer_grounding_root` | `str \| None` | `None` | 152 |

Note: `ReflectResult` has **no** `reviewer_count`, no `verification_ran`, no
`degraded_components`, and no `*_verified` field today. **FX7 must ADD any
new degrade-accounting fields it wants surfaced through the verdict object here**
(strictly appended after existing fields, all defaulted, to keep the 5 hand-built
construction sites valid — see the "Defaulted so all 5 hand-built construction
sites stay valid" comment at `models.py:135-136`).

### 1b. The `Verdict` enum — the `status`-analogue value set (`models.py:26-54`)

`Verdict(str, Enum)` values (`models.py:33-36`):
`PASS = "pass"`, `HALTED = "halted"`, `DEGRADED = "degraded"`, `BLOCKED = "blocked"`.
Exit-code map (`models.py:44-49`): pass→0, halted→10, degraded→11, blocked→2.
`PASS` is the ONLY promotable / exit-0 verdict (`models.py:52-54`).

### 1c. The on-disk `status` field value set (contract, NOT verdict)

`status` on the return-contract is a SEPARATE string from `Verdict`. Its literal
value set, grepped from the builder + readers + skill:
- Builder hardcodes `status: "success"` (`ensemble.py:538`).
- `contract.py` reads `status == "success"` (`contract.py:235`), `== "failed"`
  (`contract.py:311`), `== "partial"` (`contract.py:313`).
- Skill schema (`SKILL.md:702`): `status: success | partial | failed | dry-run`;
  (`SKILL.md:837`): `success | partial | failed`; report-template
  (`refs/report-template.md:15`): `success | partial | needs_human_decision`.

So the recognized `status` literal set the wrapper acts on is
**`success` / `failed` / `partial`** (others fall through to `tier-mismatch`
HALTED). **FX7's "set status:degraded" is a NEW value not currently in this set**
— see §3.4 additive-safety warning.

### 1d. Full field set of the ensemble-built contract (`ensemble.py:536-568`)

`contract_version` (`"1.0"`), `status` (`"success"` hardcoded, :538),
`mode` (`"post"`), `tier_reached` (int, :540), `reviewer_count` (int =
`len(succeeded)`, :541), `report_path`, `audit_log_path` (None),
`deviation_count_by_class` (4-key int dict), `t2_model_class_diversity`,
`t2_vendor_diversity`, `adversarial_unavailable` (bool),
`merge_method`, `adversarial_convergence_score`,
**`verification_ran` (hardcoded `False`, :550)**,
**`verification_skip_reason` (hardcoded `"tool-unavailable"`, :551)**,
`citations_dropped` (0), `citations_dropped_extrapolated` (0),
`input_drift_detected` (False), `regression_present` (bool),
`unauthorized_deviation_present` (bool), `needs_human_decision` (bool),
`user_decision_required` (False), `serena_summary_corroboration`
(`"unavailable"`), **`degraded_components` (hardcoded `[]`, :560)**,
`reviewer_isolation`, `audit_tree_dirty`, `reviewer_grounding_root`.

---

## 2. The builder(s) FX7 must modify (Deliverable 2)

### 2a. `build_reflect_contract` — `ensemble.py:492-568` (PRIMARY FX7 TARGET)

Signature `ensemble.py:492-506`. Key lines FX7 changes:

- `reviewer_count = len(succeeded)` (`ensemble.py:517`) — **SUCCEEDED count only.**
  The **requested** count (`config.reviewers`, default 3) is NOT a parameter of
  this function. To implement "when reviewer_count<requested => populate
  `degraded_components`", FX7 must **thread `requested`/`reviewers` into
  `build_reflect_contract`** (it is available at the call site: `reviewers =
  int(config.reviewers)` at `ensemble.py:191`, and `run_tier2` calls the builder
  at `ensemble.py:302-327` where `config` is in scope). Add a keyword param
  e.g. `reviewers_requested: int | None = None` (defaulted → additive-safe for
  the direct-call/test sites, e.g. `test_ensemble_unit.py`).
- `tier_reached` (:521), `merge_method` (:522: `"single-reviewer-fallback"` when
  `reviewer_count < 2`).
- **`"verification_ran": False` (`ensemble.py:550`)** paired with
  **`"verification_skip_reason": "tool-unavailable"` (`ensemble.py:551`)**. The
  skip reason is a member of `_VERIFICATION_SKIP_EXEMPTIONS`
  (`contract.py:36-38`), so this contract is **EXEMPT from the
  verification-skipped degrade** (Trigger 12). This is the F1-F4 vacuous-clean
  leak (see §3). FX7's "verification_ran:false => degraded + regression:unknown"
  is exactly the honest-accounting fix for this line.
- **`"degraded_components": []` (`ensemble.py:560`)** — hardcoded empty. FX7's
  "reviewer_count<requested => populate degraded_components" writes here.

The dict is emitted to disk at `ensemble.py:328`:
`_emit_reflect_contract(config.contract_path, contract)`.

### 2b. `_build_reflect_post_value` — `runner.py:93-117` (frontmatter builder)

Returns the fixed-order `reflect_post` mapping written into the tasklist
frontmatter. Current keys (`runner.py:101-117`): `verdict`, `status`, `run_id`,
`tier_reached`, `report`, `contract`, `reason`, `deviations` (4-key), `head`,
`reviewed_at`. It reads from the `ReflectResult` (`result.status`,
`result.verdict.value`, `result.deviations`, etc.). **If FX7 wants the honest
degrade fields (e.g. `verification_verified`, `reviewers_verified`,
`degraded_components`) surfaced into the tasklist frontmatter, it appends new
keys here** (append at the END to preserve field order; the writeback test
`test_writeback.py:80-91` asserts the existing 10 keys are PRESENT, not that the
set is exact — additive keys are safe against that test).

### 2c. Verdict derivation — `contract.py:derive_verdict` (:130) + `_degraded_reason` (:249)

Not a "builder" but the consumer that turns the contract into a `ReflectResult`.
Relevant to FX7 because:
- `_degraded_reason` already has **Trigger 12** (`contract.py:288-291`):
  `verification_ran is False` AND `verification_skip_reason NOT in
  _VERIFICATION_SKIP_EXEMPTIONS` → `"verification-skipped"` degrade.
- `_make_result` (`contract.py:104-127`) is where `ReflectResult` is
  constructed; if FX7 adds new fields to `ReflectResult` (§1a) they must be
  populated here (defensively, reading `c.get(...)`).

FX7 has a **design choice**: fix the LEAK at the builder (stop emitting the
exempt skip reason / honestly mark degraded) vs. tighten the CONSUMER (remove
`tool-unavailable` from `_VERIFICATION_SKIP_EXEMPTIONS`). The task spec ("builder
+ validator changes … STRICTLY ADDITIVE") points at the **builder** (`ensemble.py`)
+ **new visibility fields**, NOT repurposing the consumer exemption set (which
would be a behavior change, not additive). See §3.4.

---

## 3. Where `verification_ran`/reviewer-count are set, and the leak (Deliverable 3)

### 3a. `verification_ran` — actual field name CONFIRMED: `verification_ran`

- Set FALSE (hardcoded) at `ensemble.py:550` in the ensemble builder.
- Consumed at `contract.py:288` (`_degraded_reason` Trigger 12).
- Exemption set `_VERIFICATION_SKIP_EXEMPTIONS = {"read-only-project",
  "tool-unavailable", "--no-verify"}` (`contract.py:36-38`).
- Also a member of `_LOAD_BEARING_BOOL_FIELDS` (`contract.py:47-57`) → a present
  non-bool value routes BLOCKED `malformed-contract-boolean` (`contract.py:200-209`).
- Skill schema declares it at `SKILL.md:743` (`verification_ran: <bool>`).

### 3b. reviewer count vs requested — the two numbers

- **Requested:** `config.reviewers` (`models.py:93`, default 3, clamped [2,4]
  except 1). In `run_tier2`: `reviewers = int(config.reviewers)` (`ensemble.py:191`).
- **Succeeded/actual:** `reviewer_count = len(succeeded)` where
  `succeeded = [w for w in workers if w.status == "success"]`
  (`ensemble.py:516-517`). The ensemble driver header documents the gap:
  "`reviewer_count`: M (succeeded workers)" vs N requested (`ensemble.py:19`).
- **The requested vs succeeded delta is NOT currently recorded in the contract.**
  `build_reflect_contract` never sees `reviewers_requested`. FX7's
  "reviewer_count<requested => populate degraded_components" requires threading
  it in (see §2a).

### 3c. THE LEAK (F1-F4 root cause) — vacuously clean → PASS

The ensemble contract hardcodes `status:"success"` (:538),
`verification_ran:False` (:550) **with the exempt skip reason** `tool-unavailable`
(:551), `degraded_components:[]` (:560), `regression_present` defaults False.
Run it through `derive_verdict`:
- Trigger 12 exempt (skip reason is in the exemption set) → no verification degrade.
- No degraded_components → no degrade.
- status success + tier reached → **PASS / exit 0** (`contract.py:235-238`).

So an ensemble run where verification NEVER ran, and where fewer reviewers
succeeded than requested (as long as ≥2 survive so tier stays 2), still emits a
**vacuously clean PASS**. The `regression:0` and `status:success` are true-by-
default, not true-by-evidence. This is exactly the FX7 target: add `*_verified`
flags so these vacuous fields are visible, and honestly degrade when
verification didn't run / reviewers came up short.

Existing test `test_r2f2_build_reflect_contract_emits_honest_verification_fields`
(`tests/cli/reflect/test_ensemble_unit.py:342-364`) DOCUMENTS this state: it
asserts `verification_ran is False` with skip reason `tool-unavailable` and notes
the prior hardcoded `verification_ran=True` "was factually false." FX7 evolves
this honesty one step further (from "honest that it didn't run" → "degrade-visible
that it didn't run").

### 3d. `*_verified` flags — none exist today

Grep confirms no `*_verified` boolean on the contract or `ReflectResult`. FX7
introduces them as NEW keys (e.g. `verification_verified: false`,
`reviewers_verified: false`, `regression_verified: false`) in
`build_reflect_contract` (§2a) and optionally surfaced through `_make_result` →
`ReflectResult` → `_build_reflect_post_value`.

---

## 4. reflect_post frontmatter writer/validator (Deliverable 4)

All in `runner.py`:

- **Builder:** `_build_reflect_post_value` (`runner.py:93-117`) — §2b. Fixed key
  order; append-only for FX7.
- **Writer:** `write_reflect_post` (`runner.py:120-188`). String-splices ONLY the
  `reflect_post:` block into the frontmatter (regex `_REFLECT_POST_KEY_RE`,
  `runner.py:49`), preserves all other bytes, uses `_IndentDumper`
  (yamllint-conformant, `runner.py:59-68`), applies a compare-before-write race
  guard (`runner.py:184-185` → returns `"frontmatter-stale"`), atomic write
  (`runner.py:187`). Returns `"frontmatter-missing"` / `"frontmatter-stale"` /
  `"written"`.
- **Reader/validator:** `_read_existing_reflect_post` (`runner.py:298-334`).
  Parses the existing `reflect_post` block directly (NOT via `extract_frontmatter`,
  which drops the nested `deviations` mapping). Returns the mapping or `None`
  (e.g. when value is `PENDING` / not a mapping). This is the **skip-if-clean /
  `--skip-if-pass` gate reader** (used at `runner.py:586`).

**How a validator could enforce the new degrade fields:** `_read_existing_reflect_post`
is the natural hook for a "was this a real pass or a vacuous one" check — the
`--skip-if-pass` path at `runner.py:586` (`prior = _read_existing_reflect_post(...)`)
currently trusts a prior `verdict == pass`. FX7 could make that gate ALSO require
`prior.get("verification_verified") is True` (and/or no `degraded_components`)
before honoring the skip — otherwise a vacuous prior pass would wrongly suppress a
fresh audit. This is additive (new field absent on old blocks → treat as
unverified → do NOT skip → fail-closed).

Sidecar (`write_sidecar`, `runner.py:191-244`) is the always-written
`wrapper-result.yaml`; FX7's new fields should also flow here for the dual-gate
signal (append to the `data` dict, `runner.py:207-232`).

**Frontmatter TEMPLATE / seeding sites** (context, not FX7 edits — R6 owns
templates): `templates/workflow/01_mdtm_template_generic_task.md:32` and
`02_...:32` seed `reflect_post: ""`. The tasklist/task-builder skills
(`skills/sc-tasklist-protocol/SKILL.md:112,929,1213`;
`skills/task-builder/SKILL.md:2157,2168,2204-2207,2322`) instruct NOT to
hand-author `reflect_post` — the wrapper writes it.

---

## 5. Additive-safety: existing consumers of `status`/`regression` (Deliverable 5)

New fields must not break these existing readers. Evidence that FX7's additive
fields are safe, and where NOT to repurpose:

**Consumers of contract `status`:**
- `contract.py:235` (`== "success"` → PASS gate), `:311` (`== "failed"`),
  `:313` (`== "partial"`). — These key off the STRING literals. **If FX7 sets
  `status:"degraded"` on the ensemble contract, it falls through PASS/HALTED and
  lands at `tier-mismatch` HALTED (exit 10), NOT degraded (exit 11).** ⚠️ This
  means "set status:degraded" alone would MISROUTE. To route DEGRADED, FX7 must
  populate `degraded_components` (or another `_degraded_reason` trigger), NOT
  rely on the `status` string. Prefer keeping `status` in the existing literal
  set and adding a NEW `verification_verified:false`/`degraded_components`
  signal that `_degraded_reason` reads. (See §3.4 residual-risk note.)
- `_make_result` reads `c.get("status")` → `ReflectResult.status` (`contract.py:116`).
- `_build_reflect_post_value` copies `result.status` into frontmatter
  (`runner.py:103`); `write_sidecar` copies it (`runner.py:209`).

**Consumers of `regression` / `regression_present`:**
- `_halted_reason`: `contract.py:315` (`regression_present is True`), `:324`
  (`deviations["regression"] > 0`). — key off `is True` / `> 0`.
- `classify_fix`: `contract.py:357` (`regression_present is True`), `:361`
  (`deviations.get("regression",0) > 0`) → `human-required`.
- `_extract_deviations` (`contract.py:90-101`) builds the 4-key int dict
  (`_DEVIATION_KEYS`, `contract.py:40`).
- Frontmatter/sidecar copy `deviations["regression"]`
  (`runner.py:113`, `runner.py:218`).

**Additive-safety verdict:** All existing consumers read specific KEYS
(`status`, `regression_present`, `deviation_count_by_class`, `verification_ran`,
`degraded_components`). New keys (`*_verified`, or a populated
`degraded_components` LIST that was already read) are IGNORED by
`parse_contract` (NFR-8 read-and-ignore, `contract.py:66-71`) and by
`extract_frontmatter`. The ONE hazard: **`regression:unknown`** — the FX7 spec's
"regression:unknown" would break `_extract_deviations` if written into
`deviation_count_by_class.regression` (int coercion at `contract.py:98` catches
it → coerces to 0, so it degrades to 0 silently, NOT a crash — but ALSO not
honest). Recommend `regression:unknown` be a SEPARATE new field
(e.g. `regression_verified: false`), NOT a value inside the existing int-typed
`deviation_count_by_class` (residual risk §3.4).

### 3.4 residual-risk (STRICTLY ADDITIVE constraint — the load-bearing warning)

- Do NOT change `status` string semantics (existing `success`/`failed`/`partial`
  branches). Adding `"degraded"` as a `status` value routes to `tier-mismatch`
  HALTED, not degraded — a MISROUTE. Route degrade via `degraded_components`
  (already a `_degraded_reason` trigger, `contract.py:259-260`) or a NEW trigger.
- Do NOT put `unknown` into `deviation_count_by_class.regression` (int-typed;
  coerced to 0). Use a new sibling boolean.
- Do NOT remove `tool-unavailable` from `_VERIFICATION_SKIP_EXEMPTIONS`
  (`contract.py:37`) — that is a behavior change (would flip existing
  read-only/tool-unavailable ensemble runs to degrade globally). If FX7 wants the
  ensemble path to stop self-exempting, change what the BUILDER emits
  (`ensemble.py:551`) for the ensemble case specifically, keeping the consumer
  exemption set intact so genuine read-only-project skips still exempt.
- `_LOAD_BEARING_BOOL_FIELDS` (`contract.py:47-57`): any NEW `*_verified` bool
  FX7 wants strict-typed against malformed-truthy leakage should be ADDED to this
  frozenset — but only if a present non-bool should BLOCK. Adding it is additive
  (absent field flows normally, `contract.py:201`).

---

## 6. Test insertion points for FX7 (Deliverable 6)

Unit tests EXIST for both the builder and the derivation. FX7 inserts here:

- **Builder (`build_reflect_contract`):** `tests/cli/reflect/test_ensemble_unit.py`.
  - `test_u5_...` (:162) model-class diversity, `test_u11_...threads_regression_fields`
    (:299), and **`test_r2f2_build_reflect_contract_emits_honest_verification_fields`
    (:342-364)** — the DIRECT precedent for FX7's verification-honesty assertions.
    Add new tests here: (a) `reviewer_count<requested` populates
    `degraded_components`; (b) `verification_verified:false` present; (c) the
    ensemble contract no longer routes a vacuous PASS.
- **Verdict derivation (`derive_verdict`/`_degraded_reason`):**
  `tests/cli/reflect/test_verdict_mapping.py`. Precedents:
  `test_verification_skip_exemption_not_degraded` (:154),
  `test_verification_not_run_unexempted_is_degraded` (:166-177),
  `test_benign_degraded_component_does_not_over_halt` (:190),
  `test_malformed_truthy_load_bearing_boolean_blocks` (:228). Add: a degraded
  route when `reviewers_verified`/`degraded_components` reflect a reviewer
  shortfall, WITHOUT breaking the existing exemption test.
- **Frontmatter writeback (`_build_reflect_post_value`/`write_reflect_post`):**
  `tests/cli/reflect/test_writeback.py`. Field-presence assertion at :78-92
  (asserts the 10 existing keys PRESENT — additive keys safe). Add: new
  `*_verified` keys appear in the written block.
- **Integration:** `tests/cli/reflect/test_ensemble_stub_integration.py` (full
  stub-transport ensemble run → contract on disk → verdict) is the end-to-end
  regression seat for the "no more vacuous PASS" behavior.
- **CLI/status:** `tests/cli/reflect/test_contract_status_cli.py`,
  `test_cli_smoke.py` for exit-code surfacing.

Fixture contracts for verdict tests live under
`tests/cli/reflect/fixtures/` (e.g. `pass.yaml`, `halted_regression.yaml`,
`degraded_serena.yaml`, `degraded_single_vendor.yaml`, `degraded_tier1.yaml` —
referenced via `_load(...)` in test_verdict_mapping.py). FX7 likely adds a
`degraded_reviewer_shortfall.yaml` / `vacuous_no_verify.yaml` fixture.

---

## 7. Summary — FX7 concrete edit map (all cli/reflect, strictly additive)

| FX7 requirement | File:line to modify | Nature |
|---|---|---|
| verification didn't run ⇒ degrade-visible | `ensemble.py:550-551` (builder) + read at `contract.py:288` (already a trigger) | Stop self-exempting in the ENSEMBLE builder; keep consumer exemption set intact |
| reviewer_count<requested ⇒ populate `degraded_components` | `ensemble.py:516-517,560`; thread `reviewers_requested` from `ensemble.py:191/302` | Add kwarg (defaulted), compute shortfall, append token to the (already-consumed) `degraded_components` list |
| add `*_verified` flags | NEW keys in `build_reflect_contract` `ensemble.py:536-568`; optionally `ReflectResult` `models.py:152+` + `_make_result` `contract.py:114-127` + `_build_reflect_post_value` `runner.py:101-117` + `write_sidecar` `runner.py:207-232` | Append-only; absent-on-old = unverified (fail-closed) |
| `regression:unknown` | NEW sibling field (e.g. `regression_verified:false`), NOT inside int-typed `deviation_count_by_class` | Additive; avoids int-coercion silent-zero |
| validator enforcement | `_read_existing_reflect_post` `runner.py:298`; skip-if-pass gate `runner.py:586` | Require `verification_verified is True` before honoring a prior-pass skip |
| Do NOT | change `status` literal semantics `contract.py:235/311/313`; remove `tool-unavailable` from `_VERIFICATION_SKIP_EXEMPTIONS` `contract.py:37` | Behavior change / misroute — forbidden by additive constraint |

**Unverified / out-of-scope-but-flagged:** The SKILL-path producer of
`return-contract.yaml` (`sc-reflect-protocol` skill, `SKILL.md` §700-950) is the
OTHER emitter of these same fields; for the wrapper-vs-skill contract to stay
consistent, the skill's schema for the new `*_verified` fields must be updated in
parallel (R7 doc-crossval / R4 briefs territory). I did not audit the skill's
authoring logic (out of my cli/reflect scope) — marked Unverified whether the
skill emits `degraded_components` on reviewer shortfall today.
