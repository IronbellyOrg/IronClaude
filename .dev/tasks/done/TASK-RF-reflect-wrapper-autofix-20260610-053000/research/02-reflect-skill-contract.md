# R2 Research — sc-reflect-protocol SKILL contract + refs (FR-8 / FR-9 deltas)

**Status: Complete**
**Researcher:** R2
**Topic:** What the wrapper consumes from the reflect SKILL contract, and the FR-8/FR-9 skill deltas the tasklist must include.
**Base read:** worktree `wrapper-onto-master`, `src/superclaude/skills/sc-reflect-protocol/`
**Driving docs:** `.dev/brainstorms/20260610-053000-reflect-wrapper-autofix/merged-requirements.md`, `.dev/handoffs/reflect-wrapper-contract.md`
**Evidence rule:** every claim cites `file:line` from the `wrapper-onto-master` worktree. Path prefix below abbreviated as `SKILL.md` = `.../skills/sc-reflect-protocol/SKILL.md`; refs under `.../sc-reflect-protocol/refs/`.

---

## 1. The EXACT current §9.1 `return-contract.yaml` field list — and the FR-8 gap

§9.1 "Stable contract" is the YAML block at `SKILL.md:651-789`, header literally **`### 9.1 Stable contract (contract_version: 1.3.0)`** (`SKILL.md:651`); first line of the block is `contract_version: "1.3.0"` (`SKILL.md:654`); closing prose re-states "Contract version is `v1.3.0`." (`SKILL.md:791`). §9.3 says the stable contract "has 60+ fields" (`SKILL.md:840`).

**The exact fields the wrapper's carve-out / FR-4 classifier reads (all present today, contract 1.3.0):**

| Field | `file:line` | Type / values |
|---|---|---|
| `contract_version` | `SKILL.md:654` | `"1.3.0"` (string) |
| `status` | `SKILL.md:655` | `success \| partial \| failed \| dry-run` |
| `mode` | `SKILL.md:656` | `pre \| post` |
| `tier_reached` | `SKILL.md:657` | `1 \| 2 \| 3` |
| `report_path` | `SKILL.md:658` | `<abs path to REPORT.md>` |
| `tasklist_completion_pct` | `SKILL.md:678` | `<float 0.0-1.0> \| null` |
| `deviation_count_by_class:` | `SKILL.md:679-683` | map with sub-keys `authorized`, `necessary`, `drift`, `regression` (each `<int>`) |
| `deviation_register_path` | `SKILL.md:684` | `<abs path> \| null` |
| `grounding_gaps_path` | `SKILL.md:685` | `<abs path> \| null` (parallel artifact for evidence-insufficient findings) |
| `t2_model_class_diversity` | `SKILL.md:736` | `full \| degraded` |
| `t2_vendor_diversity` | `SKILL.md:737` | `multi \| single` (warn-only in v1.0) |
| `t2_effective_diversity` | `SKILL.md:738` | `full \| model-only \| vendor-only \| none` (derived) |
| `remediation_offered` | `SKILL.md:742` | `bool` |
| `remediation_accepted` | `SKILL.md:743` | `bool \| null` |
| `task_file_path` | `SKILL.md:744` | `<path> \| null` |
| `regression_present` | `SKILL.md:749` | `bool` (FR-4: verified-sourced from §6.1 step-5.5 exit-code taxonomy) |
| `unauthorized_deviation_present` | `SKILL.md:750` | `bool` |
| `user_decision_required` | `SKILL.md:753` | `bool` (convergence < threshold AND no auto-route applies) |
| `needs_human_decision` | `SKILL.md:754` | `bool` (grounding-gaps.yaml non-empty) |

Supporting fields in the same block the wrapper may also consult: `handoff_memory_key` (`SKILL.md:745`), `cannot_validate_without_user_input` (`SKILL.md:748`), `spec_is_wrong` (`SKILL.md:752`), and the whole Promotion block `promotion_action`/`promotion_adapter`/… (`SKILL.md:776-788`).

### FR-8 gap — CONFIRMED: `remediation_task_path` does NOT exist today

I read the entire §9.1 block (`SKILL.md:651-789`). The Tier-3 sub-block is exactly four fields (`SKILL.md:741-745`):

```yaml
# Tier 3
remediation_offered: bool
remediation_accepted: bool | null
task_file_path: <path> | null
handoff_memory_key: <serena-memory-name> | null   # FR-3 (reflect/handoff-{slug}-{timestamp}; null when no Tier 3)
```

There is **`task_file_path`** (`SKILL.md:744`) but **NO `remediation_task_path`**. A grep of the whole SKILL.md for `remediation_task_path` returns zero hits (verified — the only `remediation_*` contract keys are `remediation_offered` / `remediation_accepted`). **This is the FR-8 gap: the wrapper's `merged-requirements.md` FR-8 (line 146-152) requires `remediation_task_path: <abs>|null`; reflect today emits only `task_file_path`.**

> **Note for tasklist authors (potential ambiguity):** the existing `task_file_path` (`SKILL.md:744`) is described as `<path> | null` with no comment, and the remediation-handoff ref says an MDTM task file "will be written under .dev/tasks/to-do/" (`refs/remediation-handoff.md:108`). FR-8 explicitly names a NEW field `remediation_task_path` rather than reusing `task_file_path` — the contract artifact (`reflect-wrapper-contract.md:133-134`) and merged-requirements FR-8 (`merged-requirements.md:146-152`) both name `remediation_task_path` as the additive field. The tasklist should decide: add a new `remediation_task_path` key (matches both driving docs verbatim — additive 1.4.0 minor bump, see §6 below) vs. repurpose `task_file_path`. **Recommendation: add the new key** to match the contract artifact's load-bearing field name byte-for-byte; `task_file_path`'s current semantics (generic Tier-3 file path) are unspecified enough to be ambiguous, and the contract version map (§9.3) keys consumer rows by exact field name.

---

## 2. §Will-Not — reflect never auto-executes Tier 3 (wrapper-owns-fix justification)

Section header **`### Will Not`** at `SKILL.md:1686`. The load-bearing line:

> "**Auto-execute a Tier 3 remediation task — task-builder produces a file, the user runs `/task <path>`.**" — `SKILL.md:1691`

Adjacent reinforcing lines: "Auto-commit after Tier 3." (`SKILL.md:1692`); "**Auto-promote a `status: partial` or `status: failed` run** without `--promote-anyway`…" (`SKILL.md:1699`).

**Implication for the wrapper design (NFR-1 thinness, D1):** reflect authoring-but-never-running the corrective MDTM file is a hard SKILL invariant. The wrapper is therefore the sole mutator-orchestrator (it runs `/task <remediation_task_path>`); reflect stays read-only. FR-9 does NOT relax `SKILL.md:1691` — reflect still never runs `/task`. FR-9 only removes the **human accept prompt** for *authoring* the file under headless `--print` (see §3 below). The "user runs `/task`" clause is preserved; the wrapper IS that runner.

---

## 3. Wave 6 / `--remediate` flow — where the path is known, and the interactive accept step FR-9 must kill

### 3.1 `--remediate` flag definition
`--remediate` is defined at `SKILL.md:78`: "`--remediate` (offer Tier 3)". It is an opt-in enable-flag (other flags are "Modeled on `--remediate` (enable-flag for default-off behavior)" — `SKILL.md:80-81`).

### 3.2 Wave 6 placement in the wave plan
Wave 6 = "Tier 3 — Remediation Handoff (conditional, opt-in)" (`SKILL.md:158`). Waves 0-6 are read-only outside `<output>/`; Wave 7 is the sole mutation wave (`SKILL.md:159,161,176`). Detailed Wave-6 spec is §4.6 at `SKILL.md:333-347`.

### 3.3 How the corrective file is authored (the BUILD_REQUEST)
`SKILL.md:618` cross-skill table: "`task-builder` | Wave 6 (T3 only) | Generate corrective MDTM task file from reflection findings; gated on user opt-in." §4.6 step 6.0 writes a warm-start handoff BEFORE the task-builder spawn (`SKILL.md:337-344`), then "invoke task-builder with the handoff key" (`SKILL.md:343`).

The BUILD_REQUEST template that reflect constructs and feeds to `rf-task-builder` lives in `refs/remediation-handoff.md:7-90`. It spawns `subagent_type: "rf-task-builder"`, `mode: "bypassPermissions"` (`refs/remediation-handoff.md:13-14`), `TASK_ID_PREFIX: TASK-RF` (`refs/remediation-handoff.md:28`), and writes the MDTM file "under .dev/tasks/to-do/" (`refs/remediation-handoff.md:108`). **The path of the authored file is therefore known to reflect at the moment task-builder returns** — this is exactly what FR-8 surfaces as `remediation_task_path`.

### 3.4 THE INTERACTIVE ACCEPT STEP — what FR-9 must make non-interactive

This is the FR-9 gap, confirmed by direct citation:

- §4.6: "Wave 6 runs ONLY when `--remediate` **is accepted** (Tier 3)." (`SKILL.md:335`) and again "when `--remediate` is NOT accepted (no Tier 3), Step 6.0 never runs" (`SKILL.md:345`). The word "accepted" presupposes a human accept gate.
- The §Will-Not line (`SKILL.md:1691`) is grounded in this opt-in posture.
- The verbatim accept prompt is in `refs/remediation-handoff.md` under **"## Opt-in prompt"** (`refs/remediation-handoff.md:92-111`):
  > "Wave 6 presents this verbatim **before** invoking `task-builder` (**no auto-execute — §17 Will Not**). The user answers **yes/no**; ambiguous responses are treated as 'no'…" (`refs/remediation-handoff.md:94`)
  - The literal prompt body ends "Spawn task-builder to author a remediation MDTM task?  [yes / no]" (`refs/remediation-handoff.md:106`).

**FR-9 delta (per `merged-requirements.md:154-159`):** under wrapper (`claude --print`) headless mode there is no human to answer yes/no. `--remediate` under `--print` MUST author the file **non-interactively** (skip the `refs/remediation-handoff.md:92-111` opt-in prompt) and set `remediation_task_path`. Crucially, FR-9 carves out HUMAN-REQUIRED: when the deviation set is HUMAN-REQUIRED, reflect still authors nothing *auto-runnable* — the BUILD_REQUEST carries `needs_human_decision: true` which (per `refs/remediation-handoff.md:142` and the §9.3 consumer row `SKILL.md:849`) makes the "BUILD_REQUEST template prompts for user resolution before task is built." So the auto-author path is for AUTO-FIXABLE (Drift/Necessary-only) registers; HUMAN-REQUIRED still halts.

**Tasklist implications (skill-side edits):**
1. Add a headless-aware branch in §4.6 / `refs/remediation-handoff.md` "Opt-in prompt": when running under `--print` (no TTY / wrapper marker), treat `--remediate` as auto-accept for AUTO-FIXABLE registers (skip the yes/no), but still honor the Drift-vs-Regression default-remediation table (`refs/remediation-handoff.md:113-124`) so HUMAN-REQUIRED registers do not auto-author a runnable file.
2. After task-builder returns, capture the written MDTM path and emit it as `remediation_task_path` (FR-8).
3. This must NOT touch `SKILL.md:1691` (still never auto-*executes* `/task`) — only the authoring accept gate changes.

> **Degenerate-no-op preserved:** `refs/remediation-handoff.md:124` — register with only Authorized/Necessary items short-circuits ("No Tier 3 remediation warranted"). `SKILL.md:345` — when not accepted, `handoff_memory_key: null`. FR-8's `remediation_task_path` must be `null` in exactly these no-author cases.

---

## 4. promotion-adapters.md — EXACTLY two adapters, NO per-phase adapter (grounds D5)

`refs/promotion-adapters.md:7`: "**Two registered adapters in v1.0.** Adapter selection is deterministic from the resolved input path; if both apply or neither applies, promotion is suppressed."

The adapter table (`refs/promotion-adapters.md:9-12`) — **CONFIRMED exactly two:**

| Adapter | Source path glob | Destination | `file:line` |
|---|---|---|---|
| `task` | `.dev/tasks/to-do/TASK-*` | `.dev/tasks/done/TASK-*` | `refs/promotion-adapters.md:11` |
| `sprint-release` | `.dev/releases/current/<release>/` | `.dev/releases/complete/<release>/` | `refs/promotion-adapters.md:12` |

**NO per-phase adapter exists (D5 confirmed).** Operator-added adapters are explicitly deferred to v1.1 with no v1.0 registration surface: "In v1.0 the adapter registry is hard-coded to the two adapters above; there is no operator-facing registration surface." (`refs/promotion-adapters.md:21`). Also cross-checked in SKILL.md §1 "Promote validated work-units … move `.dev/tasks/to-do/TASK-*` → `.dev/tasks/done/TASK-*` and `.dev/releases/current/<release>/` → `.dev/releases/complete/<release>/`" (`SKILL.md:1678`) — same two, no third.

**This is the mechanical justification for FR-5 (`merged-requirements.md:125-132`):** O2 (per-phase) gates MUST force `--no-promote` because no per-phase adapter exists; the `task` adapter only matches a `.dev/tasks/to-do/TASK-*` dir path, and a phase-file path would `skip_reason: no-adapter-match` (`refs/promotion-adapters.md:19`). Adding a per-phase adapter would thicken the wrapper / break reflect-as-promotion-SoT.

### `--promote-mode` / `--no-promote` flag semantics reflect ALREADY accepts

The wrapper does NOT need to add these — they exist today. From `SKILL.md:83-88` and `refs/promotion-adapters.md:27-43`:

| Flag | Default | Semantics | `file:line` |
|---|---|---|---|
| `--no-promote` | unset (promote is default-on) | "Suppress Wave 7 entirely. Emits `promotion_action: skipped`, `skip_reason: user-flag`. No gate eval, no mutation." | `SKILL.md:84`, `refs/promotion-adapters.md:29` |
| `--promote-anyway` | unset | Override gate condition 2 (`status: partial`) ONLY; conditions 1,3-9 still apply; no effect on `status: failed` | `SKILL.md:85`, `refs/promotion-adapters.md:30` |
| `--promote-dry-run` | unset | Print `mv` + gate eval; no mutation | `SKILL.md:86`, `refs/promotion-adapters.md:31` |
| `--promote-mode auto\|task\|sprint-release\|none` | `auto` | Force a specific adapter or disable selection; `none` ≡ suppress Wave 7 but emit structured `skip_reason: mode-none` | `SKILL.md:87`, `refs/promotion-adapters.md:32` |
| `--promote-resume <checkpoint>` | unset | Resume interrupted cross-fs promotion; mutually exclusive with the other three | `SKILL.md:88`, `refs/promotion-adapters.md:33` |

> Note: SKILL.md §1 (`SKILL.md:84`) states promotion is "Default-on, `--no-promote` to suppress" — this is reflect's default. The WRAPPER's `merged-requirements.md` FR-5 flips the **wrapper-CLI** `--promote` default to True (`merged-requirements.md:125`); that is a wrapper-flag-default decision, NOT a reflect-skill change. Reflect already defaults promote-on. The wrapper just stops passing `--no-promote` for O1 and forces it for O2.

---

## 5. deviation-taxonomy.md — 4 classes + default-remediation postures (grounds D4 safe-class carve-out)

`refs/deviation-taxonomy.md:5`: "The taxonomy is **4 categories** — `evidence-insufficient` findings route to a parallel artifact … not a 5th category." (Reinforced `refs/deviation-taxonomy.md:117`: "There is no `unknown` deviation class.")

**The 4 classes, default-remediation posture, and Tier-forcing behavior:**

| Class | Definition `file:line` | Default (no flag) | With `--remediate` | Forces Tier? |
|---|---|---|---|---|
| **Authorized** | `refs/deviation-taxonomy.md:26-38` | None — document in report; **no Tier 3** (`:38`) | No remediation task (`refs/remediation-handoff.md:119`) | No |
| **Necessary** | `refs/deviation-taxonomy.md:40-54` | `Documentation note`; **no Tier 3** unless `--remediate-docs` (`:54`) | only `--remediate-docs` → spec-update task (docs-only) (`refs/remediation-handoff.md:120`) | No |
| **Drift** | `refs/deviation-taxonomy.md:56-69` | Surface "Authorize-or-revert decision required"; no auto-fix (`:69`) | Tier-3 backfill-or-revert task (`:69`, `refs/remediation-handoff.md:121`) | No (escalation depends on other rules) |
| **Regression** | `refs/deviation-taxonomy.md:71-83` | Surface as STOP-class finding (`refs/remediation-handoff.md:122`) | **Unconditionally** offer Tier 3 (`:83`) | **YES — unconditionally forces Tier-2 escalation** (`:83`) |

**Which class unconditionally forces escalation — the D4 anchor:**

> "**Regression is the only class that *unconditionally* triggers a Tier 3 remediation offer in Wave 6 when `--remediate` is set. It also **unconditionally forces escalation to Tier 2** per §5.3 rule 3 — the regression is debated by ≥2 reviewers before the report ships. No other deviation class carries an unconditional escalation…**" — `refs/deviation-taxonomy.md:83`

Classification precedence (`refs/deviation-taxonomy.md:85-97`): **Regression > Drift > Necessary > Authorized**. `regression_present` is set **by evidence, not by assignment** — only verification exits that the exit-code map (`refs/deviation-taxonomy.md:99-113`) classifies as Regression set it (`refs/deviation-taxonomy.md:101`).

**Grounding-gaps → `needs_human_decision`:** when `grounding-gaps.yaml` is non-empty, `status: partial` is forced AND `needs_human_decision: true` is emitted (`refs/deviation-taxonomy.md:132-135`; mirrored at `SKILL.md:754`).

**D4 carve-out mapping (this directly grounds `merged-requirements.md` FR-4 / §3 verdict table):**
- **AUTO-FIXABLE** = HALTED caused solely by `drift>0` and/or `necessary`-class items, with `regression_present` false, `needs_human_decision` false, `user_decision_required` false, `unauthorized_deviation_present` false, grounding-gaps empty. Justified because Drift/Necessary carry NO unconditional Tier-3/Tier-2 forcing (`refs/deviation-taxonomy.md:54,69`) — they are the mechanically-safe classes.
- **HUMAN-REQUIRED (terminal HALT)** = any of `regression_present` / `needs_human_decision` / `user_decision_required` / `unauthorized_deviation_present` / non-empty grounding-gaps / degraded-or-blocked. Regression is the load-bearing unconditional-escalation class (`refs/deviation-taxonomy.md:83`).

---

## 6. contract_version bump policy — grounds FR-8's 1.3.0 → 1.4.0

§9.4 "Contract Evolution" at `SKILL.md:856-881`. Versioning is `contract_version: "<major>.<minor>.<patch>"` (`SKILL.md:858`).

**Versioning rule (`SKILL.md:860-864`):**
- **Patch (1.0.x):** doc-only field-description change, no shape change (`SKILL.md:862`).
- **Minor (1.x.0):** "**purely additive change — new top-level field(s) added, no existing field renamed/removed/retyped, no semantic change to existing fields.** Forward-compatible: consumers MUST tolerate unknown top-level fields (read-and-ignore)." (`SKILL.md:863`)
- **Major (X.0.0):** any field rename, removal, retype, or semantic change. Breaking. (`SKILL.md:864`)

Reinforced in §9.3: "**Adding a field to a consumer's load-bearing row requires a contract version bump**" (`SKILL.md:840`) and "Additions are minor-version bumps." (`SKILL.md:854`).

**FR-8 conclusion:** adding `remediation_task_path` is a **purely additive new top-level field** → **MINOR bump 1.3.0 → 1.4.0** (matches `merged-requirements.md:152` "a `1.3.0 → 1.4.0` minor bump" and the contract artifact `reflect-wrapper-contract.md:11,133`). The wrapper, as a new consumer reading this field, is covered by the §9.4 unknown-field-tolerance forward-compat guarantee (`SKILL.md:881`) — older callers ignore it; the wrapper opts in by reading it explicitly (`SKILL.md:863`).

**Sites that hard-assert the version string `1.3.0` and MUST be bumped to `1.4.0` together (found by grep):**
- `SKILL.md:651` — §9.1 header `### 9.1 Stable contract (contract_version: 1.3.0)`
- `SKILL.md:654` — `contract_version: "1.3.0"` (the emitted field)
- `SKILL.md:791` — closing prose "Contract version is `v1.3.0`."
- `SKILL.md:1627` — §15.1 example `runs.jsonl` row `"skill_version": "1.3.0"`
- `SKILL.md:1758` — §18 grader assertion `return-contract.yaml contract_version == "1.3.0"` (THIS IS A TEST/GRADER ASSERTION — bumping the contract without updating this line breaks the falsifier eval. Tasklist MUST update it to `1.4.0`.)

> The §15.1 telemetry block also references `"skill_version": "<contract_version from §9.1>"` at `SKILL.md:1544` (template form, auto-derives — no literal to change there).

---

## 7. Cross-cutting summary & flags for the tasklist authors

**FR-8 (emit `remediation_task_path`) — skill edits required:**
1. Add field `remediation_task_path: <abs path>|null` to the §9.1 Tier-3 sub-block (`SKILL.md:741-745`), with a comment noting it is the path of the MDTM file `rf-task-builder` wrote in Wave 6, `null` when no remediation authored.
2. Populate it in §4.6 step 6.0 after the task-builder spawn returns (`SKILL.md:337-344`) — the path is already known there (`refs/remediation-handoff.md:108`).
3. Bump `contract_version` 1.3.0 → 1.4.0 at ALL five literal sites listed in §6 above, including the §18 grader assertion `SKILL.md:1758`.
4. (Optional but recommended) add a §9.3 consumer-map row for the wrapper reading `remediation_task_path` (the §9.3 map is at `SKILL.md:840-852`).

**FR-9 (headless `--remediate` auto-authoring) — skill edits required:**
1. In `refs/remediation-handoff.md` "## Opt-in prompt" (`refs/remediation-handoff.md:92-111`) and §4.6 (`SKILL.md:333-347`), add a headless branch: under `claude --print` (no TTY) with an AUTO-FIXABLE (Drift/Necessary-only) register, auto-accept `--remediate` (skip the yes/no prompt) and author the file.
2. Preserve `SKILL.md:1691` (never auto-*execute* `/task`) and the HUMAN-REQUIRED halt: Regression / `needs_human_decision` registers still author nothing auto-runnable (BUILD_REQUEST carries `needs_human_decision: true`, `refs/remediation-handoff.md:142`, `SKILL.md:849`).
3. Preserve the degenerate no-op: Authorized/Necessary-only registers short-circuit (`refs/remediation-handoff.md:124`); `remediation_task_path: null` in that case.

**What does NOT change on the skill side (NFR-1 thinness):**
- Wave/tier/4-taxonomy/promotion mechanics stay in reflect (per `merged-requirements.md:25-29`).
- The two promotion adapters are unchanged; no per-phase adapter is added (`refs/promotion-adapters.md:7,21`; `merged-requirements.md:131-132`).
- `--no-promote` / `--promote-mode` already exist (`SKILL.md:84,87`); the wrapper reuses them, adds none.
- The §Will-Not auto-execute invariant (`SKILL.md:1691`) is preserved — the wrapper, not reflect, runs `/task`.

**Unverified / open for tasklist authors:**
- *Unverified:* whether the existing `task_file_path` (`SKILL.md:744`) is currently populated with the Wave-6 MDTM path in practice (the §4.6 text does not explicitly wire `task_file_path` to the task-builder return; it wires `handoff_memory_key`). If `task_file_path` is already the authored MDTM path, FR-8 could in principle alias it — but both driving docs name a NEW `remediation_task_path` field, so the recommendation stands to add the new key. (See §1 ambiguity note.)
- *Unverified:* exact mechanism by which the wrapper/CLI detects "headless `--print`" inside the skill (TTY check vs. the `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` marker). The marker is the wrapper's recursion-breaker (`merged-requirements.md:95-103`) and exits the nested gate at exit 0 — it is NOT obviously the same signal as "suppress the accept prompt." The tasklist should specify which signal gates FR-9 auto-accept. This is an R1/R3 (CLI/process) boundary question; flagging for cross-team resolution.

---

**END R2 — all claims cite `wrapper-onto-master` worktree `file:line`. FR-8 gap (`remediation_task_path` absent, only `task_file_path` at `SKILL.md:744`) and FR-9 gap (interactive yes/no accept at `refs/remediation-handoff.md:92-111`, "accepted" gate at `SKILL.md:335`) both confirmed.**
