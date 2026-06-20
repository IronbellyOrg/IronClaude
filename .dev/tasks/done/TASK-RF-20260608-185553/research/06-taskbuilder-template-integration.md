# Research: Task-builder Template Integration (POST_REFLECT_MODE)
**Status:** Complete
**Date:** 2026-06-08
---

## Scope

`src/superclaude/skills/task-builder/SKILL.md` (2308 lines, the ONLY file in `src/superclaude/skills/task-builder/`). No separate template files exist under `task-builder/`; the MDTM templates live at `.claude/templates/workflow/0[1|2]_mdtm_template_*.md` (referenced via `template_schema_doc` frontmatter at SKILL.md:1930), but the inline-embedded task template that the builder emits lives entirely inside SKILL.md. SoT discipline (NFR-6): edit `src/superclaude/skills/...` then `make sync-dev`; NEVER edit `.claude/` directly.

---

## (a) Phase-N POST reflect HALT item — EXISTS TODAY  [CODE-VERIFIED]

`src/superclaude/skills/task-builder/SKILL.md:1992-2006` — verbatim. The item is `N.{X-1}`, penultimate, immediately before `N.X — Update task status to Done`:

```
## Phase N: [Final Phase — includes completion items]

- [ ] **N.{X-1} — Independent post-execution reflection gate (fresh session, HALT)**
  - **Context**: All implementation/test/QA items above are complete. The inline rf-qa gates ran in THIS executor's frame and cannot perform an executor-disjoint audit. Per project memory `feedback_sc_reflect_vs_inline_rfqa`, an independent `/sc:reflect --mode post` ensemble catches spec-literal-token, invariant-arithmetic, and integration/orphan blindspots that same-frame QA misses.
  - **Action**: Do NOT run reflect inside this session. Write `reflect_post: PENDING` to this file's frontmatter, then STOP and surface this paste-ready command for the operator to run in a NEW session: `/sc:reflect --mode post --remediate --diff <BASE>..HEAD --tasklist {TASK_FILE} [--spec {SPEC_PATH}] --depth {DEPTH} --executor-model {EXECUTOR_CLASS}` — where `<BASE>` is the commit recorded at task start (frontmatter `start_commit`, or `git merge-base HEAD <integration>` if unset), `{DEPTH}` is floored at `standard` per O4 (the POST gate NEVER runs `--depth quick`), and the spawned reflect agent uses the default subagent model. The gate command uses `/sc:reflect` and never the `sc:task` execution command.
  - **Output**: Frontmatter `reflect_post: PENDING`; paste-ready `/sc:reflect --mode post` command surfaced for a fresh session.
  - **Verification**: `reflect_post` is PENDING and the operator has the exact `/sc:reflect` command. The item does NOT self-resolve.
  - **Completion gate**: Operator has run `/sc:reflect --mode post` in a fresh session and recorded its verdict (`reflect_post: {verdict, run_id, report}`) in frontmatter. Only THEN may the Update-status-to-Done item proceed (HALT per `feedback_human_decision_items_must_halt`).
```

**Key observations for the wrapper branch:**
- The current item's command uses `/sc:reflect` (a slash-command in a fresh Claude session), NOT `superclaude reflect run`. The wrapper branch must SWAP the `**Action**` to shell `superclaude reflect run {TASK_FILE}` (Bash) per spec §7.7 / Open Q7.
- `<BASE>` resolution prose ("frontmatter `start_commit`, or `git merge-base HEAD <integration>` if unset") matches FR-3 exactly — the wrapper inherits this same derivation logic. [CODE-VERIFIED] consistent with spec FR-3 (merged-requirements.md:23).
- `{DEPTH}` "floored at `standard` per O4" matches FR-3 "TCS floored at `standard`". [CODE-VERIFIED]
- The current item explicitly says "the spawned reflect agent uses the default subagent model" — i.e. the manual `/sc:reflect` path runs IN-session as a subagent. The wrapper path replaces this with a top-level `claude -p` subprocess (escaping the nesting limit per spec). NFR-7: the swapped Action shells Bash, never Agent/Task.

### MALFORMED-output enforcement rule for the POST item  [CODE-VERIFIED]

`SKILL.md:2108-2109` (Critical Rule #19) and validation checklist `SKILL.md:2051`:
- Rule #19 (L2108): "When the BUILD_REQUEST specifies `POST_REFLECT_GATE: ENABLED`, the builder MUST emit, as the penultimate item of the final phase ... a fresh-session reflect handoff item. ... The handoff command uses `/sc:reflect` for the gate and `/task` (never `/sc:task`) for any re-execution. A generated task file that omits the POST reflect item when `POST_REFLECT_GATE: ENABLED` is a MALFORMED output."
- Checklist L2051: "POST reflect item present and positioned penultimate (immediately before Update-status-to-Done) when POST_REFLECT_GATE is ENABLED — MALFORMED if omitted".

These two enforcement points hardcode "the handoff command uses `/sc:reflect`". A `POST_REFLECT_MODE: wrapper` branch must AMEND Rule #19 + the checklist so the wrapper variant (Bash `superclaude reflect run`) is also accepted, not flagged MALFORMED.

---

## (b) "Reflect Depth (Deterministic TCS)" section — EXISTS TODAY  [CODE-VERIFIED]

`SKILL.md:2114-2156`. Header at L2114: `## Reflect Depth (Deterministic TCS)`.

**Depth computation (L2116):** TCS is "a pure-arithmetic score computed from observable signals on the finished MDTM file + BUILD_REQUEST + spec." Six signals S1-S6 with frozen extraction rules (L2118-2129).

**The formula (L2133-2134):**
```text
TCS = 3·S1 + 4·S2 + 2·S3 + 2·S4 + 5·S5 + 4·S6
```

**Threshold table (L2141-2145):**
| TCS range | `--depth` | tier |
|---|---|---|
| TCS ≤ 12 | `quick` | Tier 1 only |
| 13 ≤ TCS ≤ 34 | `standard` | T1, escalate-by-rubric |
| TCS ≥ 35 | `deep` | Tier 2 (forced) |

**Hard overrides (L2147-2152), the "floored at standard" rule:**
- O1 (L2149): any `S5 > 0` (human-decision item) ⇒ floor `--depth standard`.
- O2 (L2150): `S6 = 1` (file-level refactor/remediation `type:`) ⇒ force `--depth deep`.
- O3 (L2151): item-count cap > 40 (single-track > 50) ⇒ floor `--depth standard`.
- **O4 (L2152) — POST-gate depth floor (HARD RULE, no exceptions):** "the POST gate depth ∈ {`standard`, `deep`} — it may NEVER be `quick`. ... When the band yields `quick`, the POST command is emitted with `--depth standard` (the PRE call may still use `quick`, since no diff exists pre-execution)."

O4 IS the "POST never runs quick" rule the spec FR-3 references. [CODE-VERIFIED] matches merged-requirements.md:23 ("`--depth` from TCS floored at `standard` (POST never runs `quick`)").

**Single-TCS-producer / passthrough (spec FR-3, V1 R-6):** Today the builder bakes the resolved POST `--depth` via BUILD_REQUEST field `DEPTH: <max(tcs-derived depth, standard)>` at `SKILL.md:855` (see (c)). The wrapper is to treat this as PASSTHROUGH. The `±4` boundary-inference rule is at L2154.

---

## (c) Does the builder already bake `--depth`/`<BASE>` into the item command? — PARTIALLY  [CODE-VERIFIED]

**`--depth` (DEPTH): ALREADY baked.**  `SKILL.md:853-856` — the `POST_REFLECT_GATE` block in the BUILD_REQUEST template:
```
    POST_REFLECT_GATE: ENABLED
      SPEC_PATH: <spec_path or NONE>
      DEPTH: <max(tcs-derived depth, standard)>   # POST floor per O4 — never quick
      TASK_FILE: ${TASK_FILE}
```
So `DEPTH` (the POST-floored TCS depth) and `SPEC_PATH` and `TASK_FILE` are already passed to the builder, and the emitted item's command substitutes `{DEPTH}` / `{SPEC_PATH}` / `{TASK_FILE}` (item Action at L1996). This satisfies FR-3's "single TCS producer: the builder bakes the resolved `--depth` ... the wrapper treats them as passthrough." **No NEW depth-baking work needed** — the wrapper just reads the baked value.

**`<BASE>` (start_commit): NOT baked as a frontmatter field by the template; resolved at item-runtime.**  The emitted POST item's Action (L1996) tells the EXECUTOR to resolve `<BASE>` from "frontmatter `start_commit`, or `git merge-base HEAD <integration>` if unset" at the time the operator runs reflect. The frontmatter template (L1925-1949, see (e)) does NOT contain a `start_commit:` field. So `<BASE>` is resolved at gate time, not baked at build time. **This is the gap the wrapper closes:** `superclaude reflect run` performs the same `<BASE>` derivation (FR-3) in Python at launch. Whether the builder should ALSO write a `start_commit:` frontmatter field at build time is NEW work to decide (the example tasklist below DID carry `start_commit:` — see (e)).

---

## (d) BUILD_REQUEST field list — where POST_REFLECT_MODE would be added  [CODE-VERIFIED]

Two places define BUILD_REQUEST fields:

1. **The embedded template (A.9), `SKILL.md:789-866`** — the actual prompt text. The `POST_REFLECT_GATE: ENABLED` sub-block is at **L853-856**. This is where a `POST_REFLECT_MODE: wrapper|halt` line would be added (most naturally as a 4th line inside the `POST_REFLECT_GATE` block, e.g. `MODE: <halt (default) | wrapper>`).

2. **The field-list documentation (A.x), `SKILL.md:1811-1858`** — "Required BUILD_REQUEST fields" (L1813-1825) and "Optional BUILD_REQUEST signals (strictly-additive, M1-frozen schema preserved)" (L1827+). `POST_REFLECT_MODE` belongs under **Optional signals** (L1827), mirroring how `EXECUTION_CONTEXT_REQUIREMENTS` (L1829) is documented as strictly-additive with an "Omission implies <default>" rule. Default `halt` → byte-identical to current behavior when unset (NFR-3, Open Q7).

The BUILD_REQUEST "Required fields" list (L1813-1825) is the M1-frozen 15-field schema; `POST_REFLECT_MODE` must be OPTIONAL/additive to preserve that freeze (the same discipline the `EXECUTION_CONTEXT_REQUIREMENTS` signal follows at L846-848: "Strictly additive — when absent or AUTO, the M1-frozen ... BUILD_REQUEST behavior is preserved byte-identical").

---

## (e) `reflect_post: PENDING` write + frontmatter fields  [CODE-VERIFIED]

### Frontmatter template (what the builder emits) — `SKILL.md:1925-1949`

```yaml
type: "🔧 Refactor"  # or 📝 Documentation, ✨ Feature, etc.
priority: "🔼 High"
created_date: "YYYY-MM-DD"
updated_date: "YYYY-MM-DD"
assigned_to: "orchestrator"
template_schema_doc: ".claude/templates/workflow/0[1|2]_mdtm_template_[generic|complex]_task.md"
estimation: "[estimated duration]"
task_type: static
spec_path: "[driving spec/PRD/TDD path resolved at A.2, or empty if none]"
reflect_pre:
  verdict: pass | fail | skipped
  coverage_pct: <float | null>
  depth: quick | standard | deep
  tcs: <int>
  run_id: "[reflect run id]"
  report: "[TASK_DIR]reflect/pre/report.md"
  reviewed_at: "YYYY-MM-DDTHH:MM:SSZ"
reflect_post: ""   # PENDING sentinel set by the final-phase POST reflect item; operator records {verdict, run_id, report} in a fresh session
related_docs:
...
```

**Where `reflect_post: PENDING` is WRITTEN:** NOT at build time. The template seeds `reflect_post: ""` (empty sentinel, L1942). The Phase-N POST item's **Action** (L1996) is what writes `reflect_post: PENDING` at gate time, and the **Completion gate** (L1999) records the final `reflect_post: {verdict, run_id, report}`. So the lifecycle is: build → `reflect_post: ""`; gate reached → `reflect_post: PENDING`; reflect run + operator records → structured block. **The wrapper (`superclaude reflect run`) replaces the operator-records step** with an atomic frontmatter write-back (spec FR-6).

**Important template gap [CODE-CONTRADICTED vs the generated example]:** the frontmatter TEMPLATE at L1925-1949 does **NOT** contain a `start_commit:` field. But the wrapper needs `start_commit` (FR-3: `<BASE>` = frontmatter `start_commit`). See the example below — real generated tasklists DO carry `start_commit:`. So either (i) the template is stale and `start_commit` was added downstream, or (ii) `start_commit` is written by the executor/sprint at task-start, not by the builder. The wrapper's `<BASE>` fallback (`git merge-base HEAD <integration>`) covers the "unset" case (FR-3).

### Real generated-tasklist examples  [CODE-VERIFIED]

`.dev/tasks/to-do/TASK-RF-20260604-042055/TASK-RF-20260604-042055.md:48-55` — a real generated tasklist (the dogfood task that built THIS feature's predecessor). Its frontmatter carries all three fields the wrapper needs:

```yaml
spec_path: ".dev/proposals/reflect-in-task-builder.md"     # L48
reflect_pre: ""                                             # L49
reflect_post:                                              # L50  (post-run, structured)
  verdict: pass                                             # L51
  run_id: "post-TASK-RF-20260604-042055-20260604T120400"   # L52
  report: ".dev/reflect/post-.../REPORT.md"                # L53
  reviewed_at: "2026-06-04T15:48:00Z"                       # L54
start_commit: "2ea470c15ec110719fe6636cd184fa4defecce75"   # L55
```

This confirms the three frontmatter fields the wrapper reads (FR-3):
- `spec_path:` (L48) → `--spec` when it resolves to one absolute file.
- `start_commit:` (L55, a 40-char SHA) → `<BASE>` for `--diff <BASE>..HEAD`.
- `reflect_post:` (L50-54) → the block the wrapper REPLACES with the §6 structured verdict (FR-6).

Note this example uses `reflect_pre: ""` (empty string) and a FLAT `start_commit:` SHA, slightly different shape from the current SKILL.md template's structured `reflect_pre:` block — confirms drift between the template and real output, and that `start_commit` flows from somewhere other than the L1925-1949 template.

**`EXECUTOR_MODEL_CLASS` / executor model class:** NOT present as a frontmatter field in the template (L1925-1949) nor in the example tasklist's frontmatter (grep of the example returned no executor-model field). The current POST item (L1996) takes `{EXECUTOR_CLASS}` as a placeholder substituted from the BUILD_REQUEST, and FR-3 says `--executor-model` comes "from frontmatter/`EXECUTOR_MODEL_CLASS`" (merged-requirements.md:23) — i.e. an env/frontmatter source. **[CODE-CONTRADICTED / partial]:** there is currently NO `executor_model_class:` frontmatter field emitted by the template. If the wrapper is to read it from frontmatter, the builder must ADD that field (NEW work), OR the wrapper reads it from the `EXECUTOR_MODEL_CLASS` env var (FR-3 "frontmatter/env"). This is a gap the contract researcher (R02) / frontmatter researcher (R05) should reconcile.

---

## Minimal reversible edit (NFR-3, Open Q7)

The smallest reversible change is an **opt-in config flag `POST_REFLECT_MODE: wrapper|halt` (default `halt`)** added as an Optional BUILD_REQUEST signal, gating a single item-Action swap. Exact edit surface:

1. **BUILD_REQUEST template (A.9), `SKILL.md:853-856`** — add a `MODE:` line to the `POST_REFLECT_GATE` block, e.g.:
   `POST_REFLECT_MODE: <halt (default) | wrapper>` (omission ⇒ `halt`).
2. **Optional-signals doc, `SKILL.md:1827+`** — document `POST_REFLECT_MODE` as strictly-additive (mirror `EXECUTION_CONTEXT_REQUIREMENTS` at L1829-1851), with "Omission implies `halt`; when `halt` the M1-frozen byte-identical HALT item is preserved."
3. **The emitted item, `SKILL.md:1994-1999`** — add a BRANCH. When `POST_REFLECT_MODE` is unset/`halt`: emit the current L1994-1999 item BYTE-IDENTICAL (NFR-3 reversibility). When `wrapper`: emit a variant whose **Action** is a Bash shell-out `superclaude reflect run {TASK_FILE}` (NFR-7 — Bash, never Agent/Task), with Output/Verification/Completion-gate keyed off the wrapper's exit code + written-back `reflect_post.verdict == pass` (FR-7 dual-gate).
4. **Enforcement amendments, `SKILL.md:2051` (checklist) and `SKILL.md:2108-2109` (Rule #19)** — broaden "the handoff command uses `/sc:reflect`" to accept the `superclaude reflect run` Bash form under `POST_REFLECT_MODE: wrapper`, so the wrapper variant is not flagged MALFORMED.

**Reversibility proof:** because the branch defaults to `halt` and the `halt` arm reproduces L1994-1999 verbatim, a build with no `POST_REFLECT_MODE` (or `=halt`) yields a byte-identical tasklist to today (NFR-3). Only when `POST_REFLECT_MODE: wrapper` is explicitly set does the Action change.

**SoT note (NFR-6):** all four edits are in `src/superclaude/skills/task-builder/SKILL.md` → requires `make sync-dev` after editing; NEVER edit `.claude/skills/task-builder/SKILL.md` directly.

---

## Cross-researcher boundary notes
- R05 covers frontmatter WRITE mechanics (atomic/race-safe per FR-6); THIS file covers the tasklist-template SIDE — which fields tasklists carry (`spec_path`, `start_commit`, `reflect_post`) and the HALT item text. The `executor_model_class` frontmatter gap (see (e)) is a shared seam between R02 (contract), R05 (frontmatter), and this track.
- R08 covers reflect flags; the baked `--depth`/`--spec`/`--executor-model` values this file documents are the INPUTS the wrapper passes through to those flags.

---

## Summary & Staleness Tag Tally

**Findings:**
- (a) Phase-N POST HALT item EXISTS at `SKILL.md:1992-2006`; quoted verbatim. Uses `/sc:reflect` (not the wrapper); penultimate, HALTs, writes `reflect_post: PENDING`. Enforced MALFORMED by Rule #19 (L2108) + checklist (L2051).
- (b) "Reflect Depth (Deterministic TCS)" section EXISTS at `SKILL.md:2114-2156`. Formula `3·S1+4·S2+2·S3+2·S4+5·S5+4·S6`; bands quick≤12 / standard 13-34 / deep≥35; O4 (L2152) = the "POST never quick, floor standard" rule.
- (c) `--depth` (as `DEPTH:`) is ALREADY baked via BUILD_REQUEST L855 → no new depth work; `<BASE>`/`start_commit` is resolved at gate-runtime, NOT baked by the template → wrapper closes that.
- (d) `POST_REFLECT_MODE` goes in the `POST_REFLECT_GATE` block (L853-856) + Optional-signals doc (L1827+), strictly-additive, default `halt`.
- (e) `reflect_post: ""` seeded at L1942; PENDING written by the item Action (L1996); real example `TASK-RF-20260604-042055.md:48-55` carries `spec_path`/`start_commit`/`reflect_post`. `start_commit` and `executor_model_class` are NOT in the SKILL template frontmatter (drift / gap).
- Minimal reversible edit = 4 in-SKILL edits, all in `src/superclaude/skills/task-builder/SKILL.md`, default `halt` byte-identical (NFR-3), requires `make sync-dev` (NFR-6).

**Staleness tag tally:**
- [CODE-VERIFIED]: 11 (items a, b, c, d, e core claims + DEPTH bake + TCS formula + O4 + example frontmatter + HALT item + MALFORMED rules)
- [CODE-CONTRADICTED]: 2 (template frontmatter lacks `start_commit:` despite real tasklists carrying it; template lacks `executor_model_class:` field despite FR-3 expecting frontmatter source)
- [UNVERIFIED]: 0

**Status:** Complete
