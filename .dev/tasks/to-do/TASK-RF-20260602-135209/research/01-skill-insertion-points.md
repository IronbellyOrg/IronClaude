# Research: SKILL.md Insertion Points
**Topic type:** File Inventory
**Scope:** src/superclaude/skills/sc-reflect-protocol/SKILL.md
**Status:** Complete
**Date:** 2026-06-02
**File total length:** 1585 lines (verified `wc -l`)
---

## Point 1 — Frontmatter `allowed-tools` (FR-6.3)

- **Line range:** SKILL.md:4-5 (`version: 1.0.0` on line 4; `allowed-tools:` on line 5).
- **Anchor (verbatim, line 5):**
  > `allowed-tools: Read, Grep, Glob, Bash, TodoWrite, Task, Write, Edit, Skill, mcp__auggie__codebase-retrieval, mcp__serena__find_symbol, mcp__serena__find_referencing_symbols, mcp__serena__get_symbols_overview, mcp__serena__get_diagnostics_for_file, mcp__serena__read_memory, mcp__serena__write_memory, mcp__serena__list_memories, mcp__serena__search_for_pattern, mcp__serena__activate_project, mcp__context7__resolve-library-id, mcp__context7__query-docs, mcp__tavily__tavily-search, mcp__sequential-thinking__sequentialthinking`
- **FR:** FR-6.3 (and the declared-surface enabler for FR-1/2/4/5/7/8).
- **Current Serena tools present:** `find_symbol, find_referencing_symbols, get_symbols_overview, get_diagnostics_for_file, read_memory, write_memory, list_memories, search_for_pattern, activate_project` (9).
- **7 tools to ADD** — ALL verified ABSENT via grep (each returned no hits): `mcp__serena__find_implementations` (FR-1), `mcp__serena__find_declaration` (FR-2), `mcp__serena__get_current_config` (FR-7), `mcp__serena__summarize_changes` (FR-5), `mcp__serena__delete_memory` (FR-8), `mcp__serena__rename_memory` (FR-8), `mcp__serena__edit_memory` (FR-8).
- **`check_onboarding_performed` (FR-6.3) confirmation:** ABSENT — `grep -n "check_onboarding"` and `grep -n "onboarding"` both return ZERO hits anywhere in the file. Must STAY absent. FR-6 derives onboarding status from `activate_project`/`get_current_config` output, NOT by adding `check_onboarding_performed` to the surface.
- **Edit shape:** Single in-place Edit on line 5. House style: tools are clustered by server (`mcp__serena__*` group runs contiguous from `find_symbol`→`activate_project`). Append the 7 new tokens INSIDE the serena cluster — insert after `mcp__serena__activate_project,` and before `mcp__context7__resolve-library-id`. Anchor substring for surgical Edit: `mcp__serena__activate_project, mcp__context7__resolve-library-id`.
- **Builder caveat:** `think_about_*` tools are deliberately NOT in allowed-tools (SKILL.md:395 — "**They are NOT listed in frontmatter `allowed-tools`**"). Different rationale; the 7 new tools ARE protocol surface and DO belong.

---

## Point 2 — §4.0 Wave 0: step 0.5 (env alias) & step 0.7 (activate+hydrate) + insert points for 0.5c (FR-7) and 0.7 onboarding parse (FR-6)

**Wave 0 outline block (the ASCII step list):** SKILL.md:127-135.
- Line 132 (verbatim): `            0.5 Resolve env-var aliases + apply 0/1/2/3+ alias routing table (Change #13/#14)`
- Line 134 (verbatim): `            0.7 Activate Serena project + memory hydrate`
- Line 133 is `0.6 Inspect vendor heterogeneity`; line 135 is `0.8 Open audit log`.

**§4.0 Detailed step additions block:** SKILL.md:172-225. IMPORTANT FINDING: this block contains detailed prose ONLY for steps **0.4 (172-195), 0.5 (197-211), 0.6 (213), 0.9 (215-225)**. There is **NO detailed prose block for step 0.7** anywhere in §4.0 — 0.7 exists only as the one-line outline entry at line 134. There is also NO existing 0.5b/0.5c detailed block (0.5b is only *mentioned* inline at line 426 in §7.1, "a new sub-step inserted between alias resolution and reviewer composition" — it has no §4.0 prose home either).

- **Step 0.5 detailed anchor (verbatim, line 197):**
  > `**Step 0.5 (env-var alias resolution + 0/1/2/3+ alias routing).** Resolve the three ANTHROPIC_DEFAULT_*_MODEL env vars into an alias-set. Apply this routing table to decide Tier 2 reviewer count:`
  Step 0.5 prose spans 197-211 (table 199-205, grader note 207, STOP rationale 209, ref pointer 211).

- **FR-7 (get_current_config → step 0.5c):** INSERT a new detailed `**Step 0.5c ...**` prose block. Two coordinated edits:
  1. Outline edit: add `0.5c get_current_config probe ...` line after line 132 (and after wherever 0.5b lands) in the 127-135 block.
  2. Detailed-prose edit: `insert_after` the end of step 0.5 prose (after line 211, before the `**Step 0.6 ...**` line at 213). New label: **`Step 0.5c (active-project config probe)`**. (Builder: confirm with R6 whether 0.5b prose must also be authored or stays inline-only at :426.)

- **FR-6 (onboarding-status parse → augments 0.7):** Because step 0.7 has NO detailed prose block, FR-6 must CREATE one. Two coordinated edits:
  1. Outline edit on line 134: extend to `0.7 Activate Serena project + memory hydrate + parse onboarding status`.
  2. Detailed-prose edit: author a new `**Step 0.7 (activate project + memory hydrate + onboarding-status parse)**` block. Cleanest `insert_after` anchor is the end of step 0.6 prose (line 213) OR after the new 0.5c block — i.e., insert in the 213→215 gap so detailed steps stay in numeric order (0.4, 0.5, 0.5c, 0.6, 0.7, 0.9). New label: **`Step 0.7`**.

---

## Point 3 — §4.1 Wave 1B.3 cross-task scan; find_declaration pre-step (FR-2)

- **§4.1 heading:** SKILL.md:227 (`### 4.1 Wave 1 — Detailed step additions`).
- **Step 1B.3 block:** SKILL.md:233-241.
- **Anchor (verbatim, line 233):**
  > `**Step 1B.3 (cross-task interaction-effects scan, UC-2 tasklist-scope only).** When mode is UC-2 AND the tasklist contains ≥3 completed tasks, run the symbol-overlap scan:`
- The numbered sub-steps are lines 235-239 (1. find_symbol on diff hunks; 2. build overlap graph; 3. find_referencing_symbols; 4. cross-citation check; 5. synthetic invariant probe). Emit line is 241.
- **FR-2 insert (find_declaration pre-step):** Insert a new sub-step into the 235-239 numbered list. The natural slot is BEFORE current step 1 (line 235, `find_symbol against diff hunks`) — a `find_declaration` pass to resolve the canonical declaration site before symbol-overlap. New label: renumber as **step "1." `find_declaration` pre-step**, pushing existing 1→2 etc.; OR (lower-churn) insert as **"1a."** between the intro (233) and current step 1 (235). Recommend the **1a.** form to avoid renumbering the 5-item list and its downstream "(see §11.2)" reference. Edit target: `insert_after` line 233 (the intro sentence) or `replace_content` on the `1. For each task in the tasklist, derive its touched symbols via mcp__serena__find_symbol` line (235) to prepend the find_declaration step.

---

## Point 4 — §6.1 mandatory evidence chain (steps 1-6); inserts for 2a/3b/include_info/7/7' (FR-1/2/3/4/5)

- **§6.1 heading:** SKILL.md:354 (`### 6.1 Mandatory evidence-gathering chain (Wave 1A)`).
- **The fenced chain block:** SKILL.md:358-365 (opening ``` at 358, closing ``` at 365). The numbered steps:
  - Line 359: `1. mcp__serena__activate_project (once, idempotent at Wave 0)`
  - Line 360: `2. mcp__serena__get_symbols_overview <file>            # structural map`
  - Line 361: `3. mcp__serena__find_symbol <relevant-symbol>          # symbol body`
  - Line 362: `4. mcp__serena__find_referencing_symbols <symbol>      # downstream impact`
  - Line 363: `5. mcp__serena__get_diagnostics_for_file <file>        # LSP-level issues`
  - Line 364: `6. Re-Read each cited file:line range before quoting    # citation-grounding`
- Trailing prose (line 367): "The chain replaces 'think_about_collected_information' ...".
- **All five FR inserts land INSIDE this fenced block (358-365)** via a single `replace_content`/`replace_symbol_body`-style rewrite of lines 359-364 (the fence is plain markdown, so use `replace_content` on the chain interior). New step labels per spec:
  - **FR-2 → step 2a:** `2a. mcp__serena__find_declaration <symbol>` — insert between line 360 (get_symbols_overview) and 361 (find_symbol). Label: **2a**.
  - **FR-1 → step 3b:** `3b. mcp__serena__find_implementations <symbol>` — insert after line 361 (find_symbol). Label: **3b**.
  - **FR-3 → include_info:true on step 4:** modify line 362 in place — append `include_info: true` param to the `find_referencing_symbols` call (e.g. `4. mcp__serena__find_referencing_symbols <symbol> include_info:true   # downstream impact + signatures`). Label: existing **4** (param add, not new step).
  - **FR-4 → step 7 (search_deps):** append a new `7. <third-party / dependency search>` step AFTER line 364 (the re-Read step 6). Label: **7**.
  - **FR-5 → step 7' (summarize_changes, UC-2):** append `7'. mcp__serena__summarize_changes` (UC-2-only) after the new step 7. Label: **7'** (prime, matching spec's UC-2 corroboration framing).
- **Edit mechanics note:** because steps are renumbered/inserted mid-list, the lowest-risk approach is one `replace_content` over the whole interior (lines 359-364) emitting the full new 1→7' sequence, rather than 5 separate fragile fence edits.

---

## Point 5 — §6.3 memory pattern; retention-sweep block (FR-8)

- **§6.3 heading:** SKILL.md:373 (`### 6.3 Memory pattern (per-project, expiring)`).
- **Fenced memory-ops block:** SKILL.md:375-381 (read_memory/write_memory/list_memories calls).
- **Retention rule line (verbatim, line 383):**
  > `Retention rule: keep last 20 entries per key; expire >90 days. Project slug derived from pwd basename.`
- **FR-8 (retention-sweep block using delete_memory / rename_memory / edit_memory):** INSERT a new prose/fenced block. Best `insert_after` anchor is line 383 (the retention-rule line) — the sweep block operationalizes that rule. Builder authors a `**Retention sweep (Wave 5/0)**` paragraph + a small fenced block listing `mcp__serena__list_memories` → `mcp__serena__delete_memory` (expired/over-cap) → `mcp__serena__rename_memory` (slug migration) → `mcp__serena__edit_memory` (merge dedupe). New label: **"Retention sweep"** appended to §6.3, after line 383, before the §6.4 heading (line 385). Section §6.3 currently ends at 383; §6.4 begins at 385 (blank line 384 between).

---

## Point 6 — §6.5 fail-open policy (envelope all new calls inherit)

- **§6.5 heading:** SKILL.md:397 (`### 6.5 Fail-open policy`).
- **Body:** SKILL.md:399 (single paragraph):
  > `Every Serena call is fail-open per sc-validate-roadmap-protocol convention. Missing Serena → fall back to Grep/Glob with degraded: true in the audit. The protocol must never abort because Serena is unavailable.`
- Section spans 397-399, then `---` separator at line 401 (§7 starts 403).
- **Relevance to FRs:** This is the inherited envelope — ALL 7 new Serena tool calls (find_implementations, find_declaration, get_current_config, summarize_changes, delete/rename/edit_memory) are automatically covered by this fail-open clause; no edit strictly required here. Builder MAY add a one-line note confirming the new tools inherit fail-open (optional; insert at line 399 end). If R2 finds the spec mandates explicit per-tool fallback rows, that augmentation lands at line 399.

---

## Point 7 — §9.1 Stable contract block; contract_version + UC-1/UC-2 fields + bump to 1.1.0 (FR-1/2/4/5)

- **§9.1 heading:** SKILL.md:491 (`### 9.1 Stable contract (contract_version: 1.0)`).
- **Fenced YAML contract block:** OPENS at SKILL.md:493 (```yaml), CLOSES at SKILL.md:597 (```). The contract body is lines 494-596.
- **Current `contract_version` value (verbatim, line 494):** `contract_version: "1.0"` — also stated in heading (491) and trailing line 599 ("Contract version is `v1.0`.").
- **Bump to 1.1.0 (FR-1/2/4/5):** edit line 494 `contract_version: "1.0"` → `"1.1"` (note: spec says 1.1.0 — current style uses 2-segment `"1.0"`, so builder should match house style → likely `"1.1"`; confirm with R2/R6). ALSO update heading line 491 and trailer line 599 for consistency (3 coordinated edits).
- **Where new UC-1/UC-2 contract fields land:**
  - UC-1 block: lines 503-507 (`# UC-1 specific` comment at 503; fields coverage_pct 504, coverage_undefined 505, unmapped_requirements 506, best_practice_grade 507).
  - UC-2 block: lines 509-517 (`# UC-2 specific` comment at 509; tasklist_completion_pct 510, deviation_count_by_class 511-515, deviation_register_path 516, grounding_gaps_path 517).
  - FR-1/FR-2 (find_implementations/find_declaration evidence fields) → new keys appended to the UC-2 block (after line 517) OR to a new `# Serena symbolic evidence` sub-block; insert via `insert_after` line 517.
  - FR-4 (third_party_api_verified) → new boolean field; natural home is near the UC-2 / input-integrity region. Add after line 517 or in the asymmetric-cost flags block (555-562). R6/R3 own exact field names.
  - FR-5 (serena_summary_corroboration) → UC-2 field; append after line 517.
  - Builder note: `evidence_validator_ran` and citation fields are at 529-537; per-task verdicts 564-571; interaction-effects 573-575 — these are precedents for how new boolean/enum evidence fields are formatted (lowercase_snake, inline `# comment`).

---

## Point 8 — §9.2 Telemetry block; FR-6/7/8 telemetry fields

- **§9.2 heading:** SKILL.md:601 (`### 9.2 Telemetry (non-stable)`).
- **Fenced YAML telemetry block:** OPENS at SKILL.md:603 (```yaml), CLOSES at SKILL.md:618 (```). Body lines 604-617.
- **Current telemetry fields (anchors):** `wave_durations_ms` (604), `token_usage` (605), `reviewer_models/personas/vendors` (606-608), `serena_checkpoints_path` (609), `degraded_components` (610), `fallback_path` (611), `executor_class_source` (612), `executor_class_resolved` (613), `executor_exclusion_degraded` (614), `citations_dropped_extrapolated` (615), `memory_hits` (616), `memory_misses` (617).
- **Where FR-6/7/8 telemetry lands:** append new fields before the closing fence (line 618). `insert_after` anchor = line 617 (`memory_misses: <int>`), the last field.
  - FR-6 (onboarding status) → e.g. `onboarding_status: performed | not-performed | unknown` — append after 617.
  - FR-7 (get_current_config probe) → e.g. `active_project_config_probed: bool` — append after 617.
  - FR-8 (retention sweep) → memory-sweep counters; note `memory_hits`/`memory_misses` (616-617) are the existing memory-telemetry precedent — new sweep fields (e.g. `memory_entries_swept`, `memory_entries_expired`) cluster naturally right after them. Builder: insert immediately after line 617, before fence 618.

---

## Point 9 — §10.2 Necessary deviation + §10.3 Drift; classifier-input notes for FR-4/FR-5

- **§10.2 Necessary deviation:** heading SKILL.md:689; body 691-702. Detection-signals list 693-698; Gold-standard reference line 700; Default remediation line 702.
- **§10.3 Drift:** heading SKILL.md:704; body 706-716. Detection-signals 708-712; Gold-standard reference 714; Default remediation 716.
- **FR-4 (third_party_api_verified classifier input):** Note belongs in §10.2 Necessary deviation — a third-party-API-forced divergence is the archetypal "technical constraint discovered during execution." Add a detection-signal bullet to the 693-698 list (`insert_after` line 698, the last signal `- The deviation does NOT contradict any acceptance criterion in the spec.`) OR augment the Gold-standard reference (line 700) to cite `third_party_api_verified`. Recommend a new detection-signal bullet after line 698.
- **FR-5 (serena_summary_corroboration classifier input):** Relevant to BOTH §10.2 and §10.3 — `summarize_changes` corroboration distinguishes documented-necessary from silent-drift. Add a note: in §10.3 Drift detection-signals (708-712), a `serena_summary_corroboration: absent` signal reinforces "silent change" classification → `insert_after` line 712 (last drift signal). Optionally mirror in §10.2 where corroboration is `present`. Builder: keep edits to detection-signal bullet additions; do NOT restructure the 4-category taxonomy (precedence at §10.5:732-734 must stay intact).
- **Precedence guard:** §10.5 (732-734) — Regression > Drift > Necessary > Authorized — any new signal must not imply a 5th class (§10.6 grounding-gaps at 736+ owns evidence-insufficient).

---

## Point 10 — §4 per-step audit emit convention line

- **Line:** SKILL.md:124.
- **Verbatim:**
  > `**Per-step audit emit convention.** Every numbered step within every wave emits one row to <output>/audit.log with shape: {wave: <N>, step: <M>, timestamp: <ISO-8601>, outcome: ok|warn|fail|skip, evidence_ref: <path-or-null>}. This is the audit-granularity unit that resolves the 9-wave vs 7-wave structural disagreement: each step (not each wave) is the audit row.`
- **Relevance:** Every NEW sub-step the FRs add (0.5c, 0.7-detail, 1B.3 find_declaration pre-step, chain steps 2a/3b/7/7') automatically inherits this emit obligation — each must emit an `audit.log` row with `{wave, step, outcome, evidence_ref}`. Builder should reference SKILL.md:124 as the convention each new step conforms to (no edit to line 124 itself required).

---

## Summary Table

| # | Insertion point | Line range (anchor) | FR | New label / edit |
|---|-----------------|---------------------|----|------------------|
| 1 | Frontmatter `allowed-tools` | :5 (whole list) | FR-6.3 | Append 7 serena tools after `activate_project,`; keep `check_onboarding_performed` ABSENT |
| 2a | Wave 0 outline | :127-135 (0.5=:132, 0.7=:134) | FR-6/FR-7 | Add `0.5c`, extend `0.7` outline lines |
| 2b | §4.0 step 0.5 detail | :197-211 | FR-7 | insert_after :211 → new **Step 0.5c** (get_current_config) |
| 2c | §4.0 (no 0.7 detail exists) | gap after :213 | FR-6 | author new **Step 0.7** detailed block (activate+hydrate+onboarding parse) |
| 3 | §4.1 Step 1B.3 sub-steps | :233-241 (intro :233, steps :235-239) | FR-2 | insert **1a.** find_declaration before :235 |
| 4 | §6.1 evidence chain fence | :358-365 (steps :359-364) | FR-1/2/3/4/5 | rewrite interior: **2a** find_declaration, **3b** find_implementations, **include_info:true** on step 4 (:362), **7** search_deps, **7'** summarize_changes |
| 5 | §6.3 retention rule | :383 ("keep last 20 / expire >90 days") | FR-8 | insert_after :383 → **Retention sweep** block (delete/rename/edit_memory) |
| 6 | §6.5 fail-open | :397-399 (body :399) | (envelope) | inherited by all new calls; optional 1-line note at :399 |
| 7 | §9.1 stable contract | fence :493-597; `contract_version:"1.0"` :494 (also :491,:599) | FR-1/2/4/5 | bump → "1.1"; new UC-2/symbolic-evidence fields insert_after :517 |
| 8 | §9.2 telemetry | fence :603-618; last field :617 | FR-6/7/8 | insert_after :617 (before fence :618) — onboarding_status, config_probed, memory-sweep counters |
| 9a | §10.2 Necessary deviation | heading :689; signals :693-698; gold-ref :700 | FR-4 | new detection-signal bullet after :698 (third_party_api_verified) |
| 9b | §10.3 Drift | heading :704; signals :708-712; gold-ref :714 | FR-5 | new detection-signal bullet after :712 (serena_summary_corroboration absent) |
| 10 | §4 audit emit convention | :124 | (all new steps) | reference-only; new steps inherit `{wave,step,outcome,evidence_ref}` |

### Key cross-cutting findings for the builder
1. **No §4.0 detailed prose exists for step 0.7** — detailed blocks cover only 0.4/0.5/0.6/0.9. FR-6 must CREATE the 0.7 detail block, not merely augment one.
2. **No §4.0 detailed prose exists for step 0.5b either** (only an inline mention at :426 in §7.1). If FR-7's 0.5c sits "after 0.5b," confirm with R6 whether 0.5b prose must be authored first.
3. **All 7 new tools + `check_onboarding_performed` confirmed ABSENT** by grep (zero hits each) — clean adds, no dedupe risk.
4. **§6.1 chain edits are best done as ONE `replace_content`** over interior lines 359-364, not 5 fragile per-line fence edits (renumbering 1→7' touches every line).
5. **contract_version bump touches 3 locations:** :491 (heading), :494 (yaml), :599 (trailer) — keep all three in sync. House style is 2-segment `"1.0"`; spec's "1.1.0" likely renders as `"1.1"`.
6. **Deviation-taxonomy edits (§10.2/10.3) must stay bullet-level** — do not disturb §10.5 precedence (:732-734) or imply a 5th class (§10.6 grounding-gaps owns evidence-insufficient).
