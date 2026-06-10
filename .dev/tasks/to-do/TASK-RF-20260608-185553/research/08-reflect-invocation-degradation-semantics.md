# Research: Reflect Invocation + Degradation Routing
**Status:** Complete
**Date:** 2026-06-08

---

## 0. Sources & scope

- Command file: `src/superclaude/commands/reflect.md` (NOT at `commands/sc/reflect.md` — there is no `commands/sc/` dir; the file is `commands/reflect.md`).
- Skill: `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (1840 lines).
- Refs: `refs/input-resolution.md` (94 lines), `refs/ops-integration.md` (275 lines).
- **Contract version is `1.3.0`** (SKILL.md:651, 654, 791). FR-5's `contract_version` gate must accept `1.x`, reject unknown major. Spec §10 mentions "1.3.0→future" — matches.

**Headline contradictions (detailed in §6 below):**
1. Spec §8 prompt flag **`--executor-model <class>` IS REAL** (SKILL.md:584) but is MISSING from the command file's Options table (`reflect.md:66-95`). CONFIRMED real via SKILL body; the command-file omission is a doc gap, not a blocker for the wrapper.
2. Spec FR-5/§6 routes on `status: stopped-precondition` (named in `reflect.md:30`), but that value is **NOT in the §9.1 stable `status` enum** (`success | partial | failed | dry-run`, SKILL.md:655). STOP conditions emit **no contract / no status** in many cases. Wrapper must treat "STOP → no parseable contract" as `blocked`, not look for a `stopped-precondition` status. See §5.
3. `degraded_components` lives in the **§9.2 telemetry (non-stable) block** (SKILL.md:793, 802), NOT the §9.1 stable contract. FR-11 reads it anyway — fine, but the wrapper must tolerate its absence (NFR-8 unknown-field tolerance) and not assume stable-contract guarantees for it.

---

## 1. Complete flag enumeration

Reflect accepts **20 flags** per `refs/input-resolution.md:7` (the ref's count) — but the command-file Options table (`reflect.md:66-95`) lists MORE (24+ rows, incl. `--no-doc-discovery`, `--no-verify`, `--onboard`, `--with-hierarchy`, `--budget-remaining`, the legacy `--type/--analyze/--validate`). The authoritative per-flag semantics for the wrapper are below; flag/value/default/meaning, with the SOURCE the wrapper should trust.

### 1.1 Flags the §8 wrapper prompt USES (confirm/contradict)

| Flag (spec §8) | Real? | Values | Default | Meaning | Anchor |
|---|---|---|---|---|---|
| `--mode post` | ✅ REAL | `pre` \| `post` | auto-detect via §3.2 6-rule | UC selector; non-`pre`/`post` value is a hard STOP | `reflect.md:68`; input-resolution.md:9; SKILL.md:656 |
| `--no-promote` | ✅ REAL | (boolean flag) | `false` (i.e. promotion **default-ON**) | Suppress Wave 7 promotion mutation. Spec FR-9 passes it as a HARD prompt flag so an upstream default flip can't enable promotion | `reflect.md:91`; input-resolution.md:25; SKILL.md:84 |
| `--diff <BASE>..HEAD` | ✅ REAL | git ref range, branch, or path to diff file | (none) | UC-2 diff source. **Required for UC-2** unless `--task-log` given | `reflect.md:74`; input-resolution.md:12 |
| `--tasklist <abs>` | ✅ REAL | path | (none) | Tasklist file. STRONGLY recommended for UC-2 but does NOT STOP if omitted (hard req is `--diff`/`--task-log`) | `reflect.md:73`; input-resolution.md:11 |
| `--spec <abs>` | ✅ REAL | path | (none) | Driving spec/PRD. Recommended for UC-2 | `reflect.md:72`; input-resolution.md:10 |
| `--depth <standard\|deep>` | ✅ REAL | `quick` \| `standard` \| `deep` | `standard` | Tier control; see §3 vocabulary | `reflect.md:78`; input-resolution.md:16; SKILL.md:361-362 |
| `--executor-model <class>` | ✅ REAL (**but absent from command Options table**) | model class string | (none); falls back to `EXECUTOR_MODEL_CLASS` env, then commit-author log heuristic | Anti-self-confirmation exclusion: removes executor's class from reviewer rotation (§7.1) | SKILL.md:584-586; **NOT in reflect.md:66-95** |
| `--output <abs-pinned-dir>` | ✅ REAL | dir path | `.dev/reflect/<mode>-<slug>-<YYYYMMDDHHMMSS>/` | Output dir. **STOP** if under `.claude/{skills,agents,commands}` | `reflect.md:81`; input-resolution.md:19; SKILL.md:111 |

**Verdict: every flag in the spec §8 prompt is a real accepted flag.** The only caveat is `--executor-model`, which is real in the SKILL body (the source of truth for behavior) but undocumented in the command-file Options table — flag this as a doc-completeness gap for whoever owns `reflect.md`, but it does NOT block the wrapper. The wrapper SHOULD still pass it.

### 1.2 Other flags the wrapper may need (`--tier`, `--reviewers`, `--timeout`, dry-run)

- **`--tier 1 | 2 | auto`** — explicit tier pin; `auto` default; overrides the rubric (input-resolution.md:17; SKILL.md:79). **Hard override** (SKILL.md:359-360). The spec §8 prompt does NOT set `--tier`; it relies on `--depth` instead. **`--tier` is the flag the zero-alias STOP keys on** (see §4). The wrapper does NOT pass `--tier 2`; it passes `--depth deep` to force T2, which avoids the zero-alias-`--tier 2` STOP (see §4 + §5).
- **`--reviewers N`** — 2-3; default 3; clamped by `--depth` (input-resolution.md:18; SKILL.md:80). Wrapper does not set it.
- **`--allow-single-vendor`** (spec §9 in-scope, FR-11) — **NOT a reflect flag.** It is a WRAPPER-side flag that suppresses the wrapper's own `t2_vendor_diversity == single` → degraded routing. Reflect treats single-vendor as warn-only (SKILL.md:1291; ops-integration.md:95). CONTRADICTION-ADJACENT: do not pass `--allow-single-vendor` to reflect; it would be an unknown flag. It modifies the wrapper's FR-11 checklist only.
- **`--timeout`** (spec NFR-5, §8) — **NOT a reflect flag.** It is a WRAPPER/`ClaudeProcess` parameter (`timeout_seconds=3600`); reflect has no `--timeout`. Reflect's own budget control is `--budget-remaining` (SKILL.md:90). Do NOT put `--timeout` in the slash prompt.
- **No `--dry-run` on reflect.** Reflect's dry-run-like flag is `--promote-dry-run` (promotion-only, SKILL.md:93). The wrapper's `--dry-run`/`--print-command` (FR-12) is wrapper-local — it never launches reflect, so reflect's flag set is irrelevant there.
- **Debug-only fail-open flags** (the wrapper must NEVER pass these — they would defeat the gate): `--no-mcp` (SKILL.md:83), `--no-evidence-validator` (forces `status: partial`, SKILL.md:84/1049), `--no-verify` (SKILL.md:86), `--no-doc-discovery` (SKILL.md:85). Passing any of these would inject exactly the degradation FR-11 is built to reject.

---

## 2. `--no-promote` semantics (FR-9 critical)

Promotion is **default-ON** in reflect: when the §14.5.2 strict 9-condition gate passes AND `--no-promote` is unset, Wave 7 moves the work-unit folder to its `done` destination (`reflect.md:91`; input-resolution.md:25; SKILL.md:84, 1365). This is a real filesystem mutation OUTSIDE `<output>/` (SKILL.md:1372-1394). FR-9's insistence that `--no-promote` be a HARD prompt flag (not merely omitted) is correct and load-bearing: omission = promotion-on. The wrapper's audit-only default MUST literally emit `--no-promote` in the prompt string.

`--promote` (the spec's opt-in) is NOT a reflect flag name — reflect's promotion is on-by-default; the wrapper's `--promote` simply DROPS the `--no-promote` flag from the prompt, letting reflect's own gated Wave 7 run. Related reflect flags if ever needed: `--promote-anyway` (override `status: partial` cond only), `--promote-dry-run`, `--promote-mode auto|task|sprint-release|none`, `--promote-resume` (SKILL.md:1396-1404).

---

## 3. Depth vocabulary + "POST never runs quick" rule

**Vocabulary CONFIRMED:** `quick` | `standard` | `deep` (`reflect.md:78`; input-resolution.md:16; SKILL.md:361-362).

- `--depth quick` → **STOP at Tier 1** (hard override, SKILL.md:361). Tier-1-only.
- `--depth standard` → Tier 1, escalate by the §5 rubric (default, `reflect.md:78`).
- `--depth deep` → **ALWAYS escalate to Tier 2** (hard override, SKILL.md:362).

**CRITICAL CLARIFICATION — "POST never runs quick" is a WRAPPER rule, NOT a reflect-internal rule.** Spec FR-3 says `--depth` is "TCS floored at `standard` (POST never runs `quick`)." I searched the SKILL for any reflect-internal rule that floors post-mode depth at `standard` — **NONE EXISTS** (grep for `never.*quick`/`post.*never`/`floor` returns nothing relevant). Reflect WOULD honor `--depth quick` in post mode and STOP at T1 (SKILL.md:361). Therefore the flooring is entirely the wrapper's/builder's responsibility (FR-3 "builder bakes the resolved `--depth` … floored at `standard`"). **The wrapper must NEVER emit `--depth quick` for a post gate** — if it did, reflect would cap at T1 and the wrapper's "expected-T2 but `tier_reached==1`" FR-11 check would then fire `degraded` (a self-inflicted degradation). This is consistent, not contradictory: the wrapper enforces the floor upstream; reflect enforces nothing here.

---

## 4. §4 Wave 0 alias-count → tier/diversity routing (drives FR-11 preflight)

Reflect resolves model aliases at Wave 0 step 0.5 from env: `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL` (input-resolution.md:66-72; SKILL.md:115-117). Alias count drives Tier 2 reviewer topology. **Exact 5-row routing table** (SKILL.md:219-224, identical at input-resolution.md:84-90):

| Aliases resolved | `--tier` flag | Routing | Telemetry emitted |
|---|---|---|---|
| 0 | (any except `--tier 2`) | T1-only; WARN "T2 requires ≥1 model class"; degraded | `degraded_components: ["env-aliases"]` |
| 0 | `--tier 2` explicit | **STOP**, `stop_reason: "zero-aliases-tier2-conflict"` | `degraded_components: ["env-aliases"]` |
| 1 | (any) | T1-only; WARN "T2 requires ≥2 model classes" | `t2_model_class_diversity: degraded` |
| 2 | (any) | T2 with 2 reviewers (degraded) | `t2_model_class_diversity: degraded` |
| ≥3 | (any) | T2 with 3 reviewers (FULL diversity) | `t2_model_class_diversity: full` |

**Mapping alias-count → full/degraded for the wrapper's FR-11 preflight:**
- **0 or 1 aliases** → reflect goes T1-ONLY. For a post gate that EXPECTS T2 (depth≥standard, medium/complex TCS), this means `tier_reached==1` while T2 was expected → wrapper routes **`degraded`** (FR-11 "expected-T2 but `tier_reached==1`"). The wrapper SHOULD catch this in PREFLIGHT (count `ANTHROPIC_DEFAULT_*` in the exact child env) and can fail early.
- **2 aliases** → T2 runs but `t2_model_class_diversity: degraded` → wrapper routes **`degraded`** (FR-11 "`t2_model_class_diversity != full`").
- **≥3 aliases (distinct classes)** → `t2_model_class_diversity: full` → the ONLY non-degraded model-diversity state. This is the wrapper's pass precondition for diversity.

So FR-11's "count `ANTHROPIC_DEFAULT_*` aliases" preflight maps to: **≥3 distinct classes required for a clean (`full`) T2**; 2 = degraded-but-ran; 0-1 = T1-only (degraded by expected-tier-miss).

**Vendor axis (orthogonal, step 0.6):** `t2_vendor_diversity: multi` (≥2 vendors) vs `single` (one vendor) (SKILL.md:263; ops-integration.md:90-97). Reflect treats `single` as **warn-only** (does not block, SKILL.md:1291). The wrapper's FR-11 escalates `single` to `degraded` UNLESS `--allow-single-vendor` (wrapper flag). So 3 aliases all from one vendor = `t2_model_class_diversity: full` BUT `t2_vendor_diversity: single` → wrapper still routes `degraded` absent the override.

---

## 5. STOP conditions + exact stop_reason slugs

**Hard STOP list** (§3.3, SKILL.md:105-111; mirrored input-resolution.md:54-62; error matrix SKILL.md:1271-1274):

1. Neither `--spec`, `--tasklist`, nor `--diff` provided.
2. `--mode pre` with no `--spec`.
3. `--mode post` with no `--diff` AND no `--task-log`.
4. `--depth deep` with under-specified input (1-line spec / empty tasklist) — error matrix: "≤10 words spec/diff" (SKILL.md:1301).
5. **`--output` resolves under `.claude/skills/`, `.claude/agents/`, or `.claude/commands/`** — CLAUDE.md ABSOLUTE RULE (SKILL.md:111, 1274; input-resolution.md:19, 60). This is **FR-4's STOP**: the wrapper must reject such an `--output` BEFORE launch.
6. **Zero aliases + `--tier 2` explicit** → STOP, `stop_reason: "zero-aliases-tier2-conflict"` (input-resolution.md:62, 87; SKILL.md:221). The exact STOP message: `"--tier 2 requires ≥1 alias resolved (zero aliases available — set ANTHROPIC_DEFAULT_*_MODEL env vars or omit --tier 2)"`.
7. Mixing legacy + new flags (`--type task --analyze --mode post`) is a STOP (reflect.md:106).
8. Mode-resolution rule-6 catch-all STOP: `"Reflect requires --mode pre|post OR a resolvable input combination."` (input-resolution.md:40, 50).
9. Output-dir collision `-N` cap at 99 → STOP (SKILL.md:1303).
10. `--budget-remaining N` with N<5 → STOP `"budget too low for reflect"`, `budget_forced_stop: true` (SKILL.md:1305).

**Only ONE confirmed `stop_reason` SLUG exists in the sources: `zero-aliases-tier2-conflict`** (SKILL.md:221; input-resolution.md:87). Other STOPs surface a message but I found no other `stop_reason:` slug field documented — mark **Unverified** that the other STOPs populate a structured `stop_reason`.

**STOP → contract behavior (load-bearing for FR-5 verdict map):**
- The §9.1 stable `status` enum is `success | partial | failed | dry-run` (SKILL.md:655). There is **NO `stopped` / `stopped-precondition` status value** in the contract.
- The command file (`reflect.md:30`) says STOP "aborts cleanly with a `status: stopped-precondition` contract" — this value is **NOT in the §9.1 enum** and is unverifiable as a real emitted contract field. **CONTRADICTION.** Treat `reflect.md:30`'s claim as unreliable; do NOT key the wrapper verdict on a `status: stopped-precondition` field.
- Most STOPs occur at **Wave 0** (parse/validate, before any artifact dir is reliably populated). The realistic wrapper expectation: on STOP, `<output>/return-contract.yaml` may NOT exist or may be incomplete. Therefore **STOP → "no usable contract" → wrapper `blocked` (exit 2)** per spec §6 row 1. The FR-4 `--output`-under-`.claude` STOP is caught by the wrapper's OWN preflight (before launch), also → `blocked`.
- NOTE the two STOPs that DO route to a real `status` because they happen mid-run AFTER the contract is being built: `input_drift` → `status: partial` (SKILL.md:1285), and `empty_input` zero-task UC-1 → `status: partial` (SKILL.md:1286). These are post-mode-irrelevant-ish but: `input_drift_detected: true` is its own FR-11 trigger (see §6).

---

## 6. FR-11 degradation ROUTING TABLE (the wrapper's fail-closed checklist)

For each FR-11 trigger, the **exact contract field + value** that fires `degraded`, with the producing anchor. Field block noted (§9.1 stable vs §9.2 telemetry) because telemetry fields are non-stable and may be absent (NFR-8 tolerate).

| # | FR-11 trigger | Contract field + degraded value | Block | Anchor |
|---|---|---|---|---|
| 1 | grounding loss: serena | `degraded_components` contains `"serena"` | §9.2 telem | SKILL.md:802, 1294 |
| 2 | grounding loss: auggie | `degraded_components` contains `"auggie"` | §9.2 telem | SKILL.md:802, 1293; note auggie-unavailable also emits `"neighbour-search:auggie_unavailable"` (SKILL.md:463, 484) and sets `neighbour_search_degraded: true` (§9.1, SKILL.md:707) |
| 3 | env-aliases lost | `degraded_components` contains `"env-aliases"` | §9.2 telem | SKILL.md:802, 1288-1289; input-resolution.md:72 |
| 4 | evidence-validator gate lost | `degraded_components` contains `"evidence-validator"`; ALSO `evidence_validator_ran: false` (§9.1, SKILL.md:727) and reflect forces `status: partial` (SKILL.md:1049, 1280) | mixed | SKILL.md:727, 802, 1049, 1280 |
| 5 | serena context-excluded chain-critical tool | `degraded_components` contains `"serena:context-excluded"` | §9.2 telem | SKILL.md:237 (exact token; up-weights `S_dev_density`) |
| 6 | expected-T2 but ran T1 | `tier_reached == 1` while wrapper expected 2 (depth≥standard) | §9.1 | SKILL.md:657; expected from §4 alias rows 0/1 → T1-only |
| 7 | model-class diversity not full | `t2_model_class_diversity != full` (i.e. `== degraded`) | §9.1 | SKILL.md:736; §4 alias rows 1/2 |
| 8 | vendor diversity single | `t2_vendor_diversity == single` **unless `--allow-single-vendor`** (wrapper flag) | §9.1 | SKILL.md:737; warn-only in reflect (SKILL.md:1291) so wrapper must escalate it itself |
| 9 | adversarial merge unavailable | `adversarial_unavailable == true` | §9.1 | SKILL.md:734, 1275; F3 path |
| 10 | single-reviewer fallback | `merge_method == single-reviewer-fallback` | §9.1 | SKILL.md:735, 1277; F2 path |
| 11 | null convergence at T2 | `adversarial_convergence_score == null` AND `tier_reached == 2` | §9.1 | SKILL.md:733, 638-642 |
| 12 | verification didn't run | `verification_ran == false` **unless exempted** (see exceptions) | §9.1 | SKILL.md:693, 1295 |
| 13 | citations dropped | `citations_dropped > 0` | §9.1 | SKILL.md:723; also forces reflect `status: partial` |
| 14 | input drift | `input_drift_detected == true` | §9.1 | SKILL.md:717, 1285 |

**Routing key precedence note:** for trigger 11, the contract MANDATES consumers route on `merge_method` FIRST: if `merge_method == single-reviewer-fallback`, treat `adversarial_convergence_score` as inapplicable and use the single reviewer's calibrated confidence instead of routing null as `<0.60` (SKILL.md:638-642). The wrapper hits this via trigger 10 already (single-reviewer-fallback → degraded), so it's consistent — but the wrapper must not double-count or mis-route null convergence as a "low score → halt"; it's `degraded` (F2/F3), not `halted`.

**Field name caveat (telemetry vs stable):** triggers 1-5 read `degraded_components`, which is in the **§9.2 telemetry (non-stable) block** (SKILL.md:793, 802) — NOT the §9.1 stable contract. R02 should confirm the field catalog; for routing, the wrapper must tolerate `degraded_components` being absent (treat absent as empty list, per NFR-8) rather than KeyError. Triggers 6-14 read STABLE §9.1 fields and are safe to require.

### 6.1 NOT-halt exceptions (must NOT route degraded/halt)

These look like degradation signals but are EXPECTED — the wrapper must explicitly exempt them:

- **`serena_summary_corroboration: unavailable`** — EXPECTED on any cross-session reflect (FR-5.4): the summarize-changes meta-tool is session-aware; a fresh subprocess session has nothing to summarize, so `unavailable` is the default no-signal state and the main verdict is unchanged (SKILL.md:478, 692, 932). Spec FR-11 calls this out (V2 FM-13). **`agree`/`partial`/`unavailable` do NOT boost Drift; only `disagree` does** (SKILL.md:932). Since the wrapper launches reflect in a FRESH subprocess (cross-session by construction), `unavailable` is the NORMAL value here — never treat it as degraded.
- **Verification exemptions** — `verification_ran == false` is NOT a degradation when `verification_skip_reason ∈ {read-only-project, tool-unavailable, --no-verify}` (§9.1 field, SKILL.md:697). Specifically:
  - `read-only-project` — Serena project config `read_only: true` (ops-integration.md:122-131).
  - `tool-unavailable` — `execute_shell_command` context-excluded (ops-integration.md:133-142).
  - `--no-verify` — operator opted out (but the wrapper must NEVER pass `--no-verify`, so this skip-reason should not appear in wrapper runs; if it does, it's a prompt-construction bug).
  The wrapper's FR-11 trigger-12 should read: route `degraded` on `verification_ran == false` ONLY when `verification_skip_reason` is null/empty (i.e., it ran-or-should-have but didn't). When skip_reason is a legit exemption, do not halt on this axis alone. NOTE the spec says "unless exempted" — `read-only-project`/`tool-unavailable` are the documented exemptions.
- **`onboarding_ran: false`** / `serena_summary_corroboration` aside — onboarding is opt-in (`--onboard`, default OFF); the wrapper never passes it, so `onboarding_ran: false` is normal, not degraded.
- **`t2_vendor_diversity: single` with `--allow-single-vendor`** — operator-acknowledged; exempt (wrapper flag).
- **Advisory-only telemetry that does NOT gate:** `citations_dropped_extrapolated > 0` is recording-only and explicitly does NOT gate (SKILL.md:724, 1092-1095). The wrapper must gate on `citations_dropped` (the sample count), NOT the extrapolated field. Likewise `reuse_miss_advisory`, `neighbour_search_sampled` are advisory.

---

## 7. The 9-condition promotion gate (§14.5.2) — grounding the §6 verdict map

The wrapper does NOT recompute this; it MIRRORS it by reading contract outputs (spec §6 "mirrors reflect's own 9-condition promotion gate by reading its outputs"). Promotion fires only when ALL 9 hold (SKILL.md:1345-1363):

1. `mode == post` — UC-1 has nothing to promote. → `gate_evaluation.mode_post`
2. `status == success` — `partial`/`failed` block; "Conditional-CONVERGED" is NOT eligible. → `status_success`
3. `tasklist_completion_pct == 1.0` — every item independently verified by reflect, not just frontmatter-declared. → `tasklist_completion_pct_1_0`
4. `deviation_count_by_class.drift == 0` AND `.regression == 0` — Authorized/Necessary are non-blocking; Drift/Regression block. Reuse-Miss at rung L3 increments drift/regression. → `no_drift_no_regression`
5. Frontmatter agreement: **5a** present+parseable (has `status` field) → `frontmatter_present`; **5b** `status: done` (or terminal) declared, any other value (in-progress/partial/blank) fails → `frontmatter_status_matches`.
6. `citations_dropped == 0` (sample-count, NOT extrapolated) AND grounding-gaps.yaml empty → `no_citations_dropped` + `no_grounding_gaps`.
7. `input_drift_detected == false` → `no_input_drift`.
8. `needs_human_decision == false` AND `user_decision_required == false` → `no_user_decision_pending`.
9. `convergence_score` not null when Tier 2 ran: if `tier_reached == 2` AND `adversarial_unavailable == true` (→ `convergence_score: null`), promotion blocked regardless. T1-only runs satisfy vacuously. → `adversarial_result_present` (SKILL.md:642, 1363).

**How this grounds spec §6 verdict map (first-match-wins):**
- **`blocked` (exit 2):** contract missing/unparseable / child crash / preflight STOP (incl. `--output` under `.claude`, FR-4) / rc==124 timeout / unknown `contract_version` major. Maps to "no usable contract."
- **`degraded` (exit 11):** any §6 FR-11 trigger above (gate cond 6/7/9 overlap the degradation set: `citations_dropped`, `input_drift`, `adversarial`/`convergence` map to BOTH a degraded-grounding signal AND a gate-fail). The wrapper routes these to `degraded` (chain-critical loss) per FR-8/FR-11 — STRICTER than reflect's own gate which would just `skip` promotion.
- **`halted` (exit 10):** `status: partial` OR `regression_present`/`unauthorized_deviation_present`/`needs_human_decision`/`user_decision_required`/`drift>0`/`regression>0` (gate conds 2,4,8 — the AUDIT-FOUND deviation signals, §9.1 fields SKILL.md:749-754, 679-683). These mean reflect ran cleanly (full Tier-2) but FOUND problems → human must decide.
- **`pass` (exit 0):** `status: success` AND none of degraded/halted AND expected tier reached (`tier_reached==2` for a T2-expected post gate) AND `t2_model_class_diversity==full` AND non-null adversarial merge AND `verification_ran` (or exempt). I.e. the 9-gate would pass AND no degradation. This is the ONLY exit-0 path (FR-8).

**Key distinction degraded vs halted:** `degraded` = reflect LOST the structural machinery (diversity/grounding/adversarial/verification) that makes the audit trustworthy → the audit itself is suspect. `halted` = the audit was TRUSTWORTHY (full Tier 2) and it FOUND real deviations/partials. Both HALT the Done item; only the reason and the operator's next move differ. `blocked` = couldn't even get a usable audit.

---

## 8. Contradictions / flags for the task author

1. **`status: stopped-precondition` does NOT exist** in the §9.1 contract enum (`success|partial|failed|dry-run`, SKILL.md:655). The command file claims it (`reflect.md:30`). The spec §6 verdict table does NOT route on it (it correctly routes STOP → `blocked` via "preflight STOP" / "contract missing"). **Resolution:** wrapper routes any STOP → `blocked` by absence-of-usable-contract, NOT by a status value. Do not author a wrapper branch that greps for `stopped-precondition`.
2. **`--executor-model` real but undocumented** in `reflect.md:66-95` Options table; real in SKILL.md:584. Wrapper SHOULD pass it (FR-3). Doc gap to flag for the reflect-command owner, non-blocking.
3. **`--allow-single-vendor`, `--timeout`, `--dry-run` are WRAPPER flags, NOT reflect flags.** Never put them in the `/sc:reflect …` prompt string. `--timeout` → `ClaudeProcess(timeout_seconds=…)`; `--allow-single-vendor` modifies FR-11 routing; `--dry-run` short-circuits before launch. Reflect's analogous flags are `--budget-remaining` (budget) and `--promote-dry-run` (promotion preview only).
4. **`--promote` is not a reflect flag** — opt-in promotion = DROP `--no-promote` from the prompt (reflect promotion is default-ON). Confirmed SKILL.md:84/1365.
5. **"POST never runs quick" is wrapper-enforced**, not reflect-enforced (§3 above). No reflect-internal floor exists. Wrapper must never emit `--depth quick` for a post gate.
6. **`degraded_components` is telemetry (non-stable)**, not stable contract (SKILL.md:793-802). FR-11 triggers 1-5 depend on it; wrapper must tolerate absence (treat as empty). Triggers 6-14 use stable §9.1 fields — prefer those where overlap exists (e.g. prefer stable `t2_model_class_diversity` over inferring from `degraded_components`).
7. **Spec FR-11 token `serena:context-excluded`** is confirmed real (SKILL.md:237). The spec's degraded_components set `{serena, auggie, env-aliases, evidence-validator, serena:context-excluded}` all map to real emitted tokens; additionally auggie path can emit `neighbour-search:auggie_unavailable` (SKILL.md:463/484) — the wrapper may want a prefix/substring match (`startswith("serena")`, `contains("auggie")`) rather than exact-equality to catch the qualified variants like `serena:pre-v1.5-no-rename-propagation` (SKILL.md:533) and `serena:onboarding-parse` (SKILL.md:271) — but NOTE those two are benign/expected, so exact-token matching against the spec's enumerated set is SAFER than broad substring. Recommend exact-set membership against `{serena, auggie, env-aliases, evidence-validator, serena:context-excluded}` per FR-11's literal list.

---

## 9. Wrapper invocation surface (synthesized, for FR-2/FR-3)

The single slash invocation the wrapper builds (all real flags, confirmed §1):
```
/sc:reflect --mode post --no-promote --diff <BASE>..HEAD --tasklist <abs> [--spec <abs>] --depth <standard|deep> --executor-model <class> --output <abs-pinned-dir>
```
- `--mode post` (REAL), `--no-promote` (REAL, hard flag), `--diff` (REAL), `--tasklist` (REAL), `--spec` (REAL, conditional), `--depth standard|deep` (REAL, never `quick`), `--executor-model` (REAL, undocumented in cmd table), `--output` (REAL, must not be under `.claude/{skills,agents,commands}`).
- NO `--tier` in the prompt → the zero-alias-`--tier 2` STOP (`zero-aliases-tier2-conflict`) is structurally unreachable from the wrapper; T2 is forced via `--depth deep`/rubric instead. Good — the wrapper can't trip that STOP.
- The `claude` argv (model/headless only) carries NONE of reflect's flags; reflect's flags all live in the stdin prompt (spec §8 corrects V3's argv bug — confirmed: `--output`/`--diff` are reflect flags, not `claude` flags).

---

## Complete

## Summary

**Every flag in the spec §8 prompt is a REAL accepted reflect flag** — `--mode post`, `--no-promote`, `--diff`, `--tasklist`, `--spec`, `--depth`, `--executor-model`, `--output` all confirmed (anchors in §1.1). The one caveat: `--executor-model` is real in the SKILL body (SKILL.md:584) but missing from the command-file Options table (reflect.md:66-95) — a doc gap, NOT a blocker; the wrapper should still pass it.

**Three real contradictions for the task author:**
1. `status: stopped-precondition` (claimed in reflect.md:30) is NOT in the §9.1 contract status enum (`success|partial|failed|dry-run`, SKILL.md:655). Wrapper must route STOP → `blocked` by absence-of-usable-contract, never by a status value.
2. `--allow-single-vendor`, `--timeout`, `--dry-run`, `--promote` are WRAPPER-side, NOT reflect flags — must never appear in the slash prompt. `--promote` = drop `--no-promote` (reflect promotion is default-ON).
3. "POST never runs quick" is WRAPPER-enforced (FR-3 floor); no reflect-internal post→standard floor exists (reflect would honor `--depth quick` → STOP at T1).

**Depth vocab confirmed:** `quick`(→T1 stop) / `standard`(default, rubric) / `deep`(→force T2) (SKILL.md:361-362).

**STOP conditions** (§5): the only confirmed structured `stop_reason` slug is `zero-aliases-tier2-conflict` (SKILL.md:221). The FR-4 `--output`-under-`.claude/{skills,agents,commands}` STOP is wrapper-preflight-caught → `blocked`. Because the wrapper forces T2 via `--depth deep` (not `--tier 2`), the zero-alias-`--tier 2` STOP is structurally unreachable.

**§4 Wave-0 alias routing** (the FR-11 preflight driver): 0-1 aliases → T1-only (expected-T2 miss → degraded); 2 → T2 `t2_model_class_diversity: degraded`; **≥3 distinct classes → `full`** (the only clean state). Vendor axis orthogonal: `single` is reflect-warn-only but wrapper escalates to `degraded` unless `--allow-single-vendor`.

**FR-11 routing table** (§6): mapped all 14 triggers to exact contract field+value+source. Critical caveat — `degraded_components` (triggers 1-5) is §9.2 **telemetry/non-stable** (SKILL.md:802), so the wrapper must tolerate its absence; triggers 6-14 use stable §9.1 fields. **NOT-halt exceptions** (§6.1): `serena_summary_corroboration: unavailable` is EXPECTED cross-session (the wrapper always runs a fresh subprocess, so this is normal — SKILL.md:478/932); `verification_ran: false` is exempt when `verification_skip_reason ∈ {read-only-project, tool-unavailable}` (SKILL.md:697); `citations_dropped_extrapolated` is advisory-only and must NOT gate (gate on `citations_dropped` sample-count, SKILL.md:1092-1095).

**9-condition promotion gate** (§7) summarized and mapped to the spec §6 4-state verdict. Key distinction: `degraded` = lost structural machinery (diversity/grounding/adversarial/verification → audit untrustworthy); `halted` = trustworthy full-T2 audit that FOUND deviations/partial; `blocked` = no usable audit at all. Contract version is **1.3.0** (gate FR-5 on `1.x` tolerant, unknown major → blocked).

**File:** `.dev/tasks/to-do/TASK-RF-20260608-185553/research/08-reflect-invocation-degradation-semantics.md`
