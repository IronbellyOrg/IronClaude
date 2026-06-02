# Research: SKILL.md + reflect.md Inventory
**Topic type:** File Inventory + Patterns & Conventions
**Scope:** sc-reflect-protocol SKILL.md, reflect command, refs/
**Status:** Complete
**Date:** 2026-05-31
---

## A. File Inventory & Drift Findings (BLOCKER for task-builder)

### A.1 Target SKILL.md (single live copy)
- **Path:** `/config/.claude/skills/sc-reflect-protocol/SKILL.md`
- **Size:** 140,853 bytes, 1,586 lines
- **sha256:** `0aaef85fc8172c36ba8a2257b607018a8ed2c48718fb50b99881d35ec4d333ea`

### A.2 SOURCE-OF-TRUTH MIRROR DOES NOT EXIST — DRIFT BLOCKER
- **Expected per user brief:** `/config/workspace/Coder/src/superclaude/skills/sc-reflect-protocol/SKILL.md`
- **Actual:** `/config/workspace/Coder/src/` directory **does not exist** in the Coder repo.
- **Verified:** `find /config/workspace/Coder -maxdepth 4 -type d -name "src"` returns nothing. `find -name "superclaude"` returns nothing.
- **Verified:** `/config/workspace/Coder/` top-level dirs are: `.agents, _bmad, _bmad-output, catalogue, .claude, .dev, docs, .github, .opencode, openspec, postmortem, scripts, .serena, templates`. No `src/`.
- **Implication for task-builder:** The user-stated "mirror" rule (edit `src/`, then `make sync-dev`) **does NOT apply to this repo**. The Coder repo lacks the SuperClaude development structure described in the global `CLAUDE.md`. There is only ONE live copy of `SKILL.md` at `/config/.claude/skills/sc-reflect-protocol/SKILL.md`. The Edit operations must target this file directly. There is no `make sync-dev` to run.
- **Note:** SKILL.md §17.5 internally references `src/superclaude/skills/sc-reflect-protocol/SKILL.md` for the "Edit src/ then sync-dev" rule (line 1467). This reference is **stale relative to the Coder repo state**. The amendments themselves do NOT need to alter §17.5, but the executor must know there is no `src/` to sync from.

### A.3 reflect command file (single live copy)
- **Path:** `/config/.claude/commands/sc/reflect.md`
- **Size:** ~266 lines
- **version:** 2.0.0 (frontmatter line 8)

### A.4 refs/ directory listing (so new file doesn't collide)
- **Path:** `/config/.claude/skills/sc-reflect-protocol/refs/`
- **Existing files (11):**
  - `cost-profile.yaml` (3,170 bytes)
  - `coverage-mapping.md` (7,250)
  - `deviation-taxonomy.md` (7,995)
  - `grader-extensions.md` (16,301)
  - `input-resolution.md` (8,104)
  - `ops-integration.md` (17,097)
  - `promotion-adapters.md` (16,340)
  - `reflection-rubric.md` (9,150)
  - `remediation-handoff.md` (7,340)
  - `report-template.md` (10,949)
  - `reviewer-spec.md` (7,008)
- **NEW file the OVM proposal mandates:** `refs/claim-extraction-patterns.yaml` — **no collision** with existing names.

### A.5 Eval-workspace falsifier targets (covered by R3, listed here for completeness)
- `.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/outcome-verification-docker-cli-miss.yaml` (NEW per MERGED §7.1, line 503)
- `.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/outcome-verification-deferred-runtime-config.yaml` (NEW per MERGED §7.2, line 569)

---

## B. Amendment Inventory — verbatim current text + verbatim replacement text

The MERGED-PROPOSAL.md §3 enumerates 7 concrete protocol-text amendment buckets (§3.1-§3.7), plus supporting changes in §§4-7. Below: **15 amendments** total. Numbered Edit operations follow.

---

### Amendment 1: Frontmatter `allowed-tools` — add WebFetch, WebSearch
- **Merged proposal source:** §3.6 (lines 268-276 of MERGED-PROPOSAL.md)
- **SKILL.md target:** frontmatter line 5 (the `allowed-tools:` key)
- **Operation:** replacement of the `allowed-tools` value (insertion of two tokens within the comma-separated list)
- **Current text (verbatim with context):**
  ```
  description: "Tiered reflection protocol grounded in real code and real citations. UC-1 (pre-execution) validates a proposed strategy/tasklist against its driving spec/PRD for coverage and best-practice compliance. UC-2 (post-execution) audits completed work for 100% adherence and classifies every divergence under a 4-category deviation taxonomy (Authorized expansion / Necessary deviation / Drift / Regression). Tier 1 is a fast single-agent grounded pass; Tier 2 fans out 2-3 heterogeneous reviewer agents on different model classes and merges via sc-adversarial-protocol Mode A; Tier 3 hands off to task-builder for a corrective MDTM remediation. Structural mechanisms — heterogeneous reviewers, blind calibration, mandatory evidence-validator gate — exist specifically to neutralise the representational bias that makes single-agent self-review unreliable."
  version: 1.0.0
  allowed-tools: Read, Grep, Glob, Bash, TodoWrite, Task, Write, Edit, Skill, mcp__auggie__codebase-retrieval, mcp__serena__find_symbol, mcp__serena__find_referencing_symbols, mcp__serena__get_symbols_overview, mcp__serena__get_diagnostics_for_file, mcp__serena__read_memory, mcp__serena__write_memory, mcp__serena__list_memories, mcp__serena__search_for_pattern, mcp__serena__activate_project, mcp__context7__resolve-library-id, mcp__context7__query-docs, mcp__tavily__tavily-search, mcp__sequential-thinking__sequentialthinking
  ---
  ```
- **Replace with (verbatim resulting line):**
  ```
  allowed-tools: Read, Grep, Glob, Bash, TodoWrite, Task, Write, Edit, Skill, WebFetch, WebSearch, mcp__auggie__codebase-retrieval, mcp__serena__find_symbol, mcp__serena__find_referencing_symbols, mcp__serena__get_symbols_overview, mcp__serena__get_diagnostics_for_file, mcp__serena__read_memory, mcp__serena__write_memory, mcp__serena__list_memories, mcp__serena__search_for_pattern, mcp__serena__activate_project, mcp__context7__resolve-library-id, mcp__context7__query-docs, mcp__tavily__tavily-search, mcp__sequential-thinking__sequentialthinking
  ```
- **Notes:** Also bump `version: 1.0.0` -> `version: 1.1.0` (per MERGED §3.3 "additive — minor bump 1.0 -> 1.1" and §6 "minor 1.0 -> 1.1"). Recommend keeping description unchanged; add `version` bump as a second small Edit (Amendment 2).

---

### Amendment 2: Version bump 1.0.0 -> 1.1.0
- **Merged proposal source:** §3.3 line 177 ("additive — minor bump 1.0 -> 1.1") + §6 line 450 ("**Version bump:** **minor 1.0 -> 1.1** per `§9.4`")
- **SKILL.md target:** frontmatter line 4
- **Operation:** replacement
- **Current text:**
  ```
  version: 1.0.0
  ```
- **Replace with:**
  ```
  version: 1.1.0
  ```
- **Notes:** Per §9.4 (line 644): "**Minor (1.x.0):** purely additive change — new top-level field(s) added, no existing field renamed/removed/retyped". OVM is strictly additive, so minor bump is correct.

---

### Amendment 3: NEW Wave 1 sub-step 1B.4 — Outcome-claim extraction
- **Merged proposal source:** §3.1 lines 101-140 of MERGED-PROPOSAL.md
- **SKILL.md target:** §4.1 (lines 227-241 of SKILL.md) — insertion AFTER existing `Step 1B.3` block, BEFORE the `### 4.3 Wave 3 — Detailed step addition` heading at line 243.
- **Operation:** insertion (new sub-step after 1B.3)
- **Current text (verbatim with context — last lines of 1B.3 block + section break):**
  ```
  5. Each risk becomes a synthetic invariant probe entry tagged `category: cross_task` (in addition to the existing 6 categories — see §11.2). Severity scales with the symbol's call-site count: HIGH if >5 referencing call sites, MEDIUM if 2-5, LOW if 1.

  Emit `interaction_effects_scanned: true` in the contract when this step runs; `interaction_effects_scanned: false` when skipped (tasklist < 3 tasks OR mode == UC-1). This is the differentiating value of end-of-tasklist reflect — single-scope review misses interaction effects, and this is where reflect catches them.

  ### 4.3 Wave 3 — Detailed step addition
  ```
- **Replace with (insertion between the `interaction_effects_scanned` paragraph and the `### 4.3` heading):**

  Insert this block immediately before `### 4.3 Wave 3 — Detailed step addition`:

      **Step 1B.4 (outcome-claim extraction, UC-2; also UC-1 in coverage-claim mode).** Inserted immediately after Step 1B.3 (cross-task interaction-effects scan) and before Wave 1C reflection. Behavior:

      1. Parse **three claim sources**, in priority order:
         - **Spec acceptance criteria** (`§10` gold-standard reference) — every "MUST", "WILL", "EXPECTS", or bulleted success-criterion statement becomes a candidate claim.
         - **Tasklist success criteria / task description body** — every "verifies that …" or "expected to …" statement.
         - **Diff's implicit upstream-artifact claims** — for every line matching the patterns `apt-get install`, `apt install`, `pip install`, `npm install`, `gem install`, `cargo add`, `go get`, `gh api`, `aws <service>`, `terraform apply -target=<resource_type>.<name>`, a single implicit claim "<package/api/resource> provides <required-symbol-or-endpoint>" is extracted. The pattern list is **regenerable from `refs/claim-extraction-patterns.yaml`** (new ref); operators add patterns without editing SKILL.md.

         **Claim granularity (INV-003):** One implicit claim per `(package, install-line)` pair. Example: `apt-get install -y --no-install-recommends docker.io git curl` emits 3 separate claims (one per package). Multi-line installs across `\` continuations are concatenated first.

      2. Each candidate claim is tagged with a `verification_seat` per a small classifier rubric (also in `refs/claim-extraction-patterns.yaml`):
         - Spec/tasklist claim mentioning files, symbols, configs in-repo -> `in-repo`
         - Claim mentioning a third-party package, API, or external schema -> `external-spec`
         - Claim mentioning live processes, kernel state, deployed behavior, latency, error rate -> `runtime`
         - Claim mentioning a named downstream service or cross-process invariant -> `cross-system`
         - Claim that depends on second-order reasoning the audit declines to perform at the current tier (e.g., "rebuild changes install-list outcome") -> `V-Deferred-Logical`
         - Ambiguous -> tag as `runtime` (most-conservative; runtime is the seat reflect cannot verify, so over-tagging here surfaces honest deferrals rather than false-pass)

         **Multi-mode precedence (INV-005):** when a claim satisfies multiple modes, apply this order: `V-Deferred-Logical > runtime > cross-system > external-spec > in-repo`. Rationale: `V-Deferred-Logical` signals tier-escalation; if Tier 2 resolves the logical question, the claim collapses to a stricter mode.

      3. Write `<output>/outcome-claims.yaml` with required fields (YAML body uses fenced block per the same convention as §9.1):

         claim_id, claim_text, source (`spec_section:<id> | tasklist_item:<id> | diff_hunk_implicit:<file>:<line>`), verification_seat (`in-repo | external-spec | runtime | cross-system | V-Deferred-Logical`), verification_status (pending initially; filled in Wave 5), verifier_tool, evidence_ref, deferral_runbook (null initially; filled in Wave 5 for runtime/cross-system/V-Deferred-Logical seats).

      4. Token cost: **~400-1200 tokens per run** depending on diff size and spec density. Within the ≤2k T1 envelope from §15 constraint.

- **Notes:** Watch for nested code-fence escaping. The verbatim MERGED-PROPOSAL text contains a YAML code fence inside item 3; if the executor wants byte-identical transplant, indent the new section with 4 leading spaces so the inner ```yaml fences render correctly, OR rewrite item 3 in prose (as shown above) to avoid the nesting issue. **Preferred: prose form for item 3 to keep the markdown clean** — the schema is already authoritatively defined in §9.1 OVM additive fields (Amendment 6). The "Change 11" / "Change 12" markers from MERGED-PROPOSAL are stripped; only "INV-003" / "INV-005" anchors retained to match SKILL.md convention (lines 132-135 already use Change # AND INV-NNN).

---

### Amendment 4: NEW Wave 5 sub-step 5.OVM — Outcome-verification pass
- **Merged proposal source:** §3.2 lines 141-176 of MERGED-PROPOSAL.md
- **SKILL.md target:** §4.5 (lines 249-258 of SKILL.md) — insertion AFTER existing Step 5.0 block, BEFORE the `---` separator at line 259.
- **Operation:** insertion (new sub-step after Step 5.0)
- **Current text (verbatim with context — Step 5.0 block + section break):**
  ```
  ### 4.5 Wave 5 — Detailed step addition

  **Step 5.0 (sc-adversarial pre-invocation probe and F1/F2/F3 fallback).** Before calling `Skill sc-adversarial-protocol`, probe its existence via `mcp__serena__list_memories` for the skill's existence indicator OR a no-op `Skill('sc-adversarial-protocol', args='--help')`. If the probe returns `skill not found`:

  - **F1**: retry the probe once after a short backoff.
  - **F2**: on second probe failure, use the highest-calibrated single Tier 2 reviewer verdict as the fallback merged result; mark `merge_method: single-reviewer-fallback`.
  - **F3**: route to Tier 3 only if user explicitly opts in (`--remediate`); otherwise surface `adversarial_unavailable: true` and `status: partial`.

  The fallback path is **loud, never silent**: every F-step writes to audit.log; the return contract carries `adversarial_unavailable: true`.

  ---
  ```
- **Replace with (insertion BEFORE the `---` line at end of §4.5):**

  Insert this block between "The fallback path is **loud, never silent**:..." and the `---` separator:

      **Step 5.OVM (outcome-verification pass).** Inserted between Step 5.0 and the existing synthesis substeps. Behavior:

      1. **For every `in-repo` claim:** verify using the existing Serena symbol-chain from §6.1 plus the citation re-Read window from §11.5. Drop on failure per §11.2.

      2. **For every `external-spec` claim:** verify using the external-spec toolkit:
         - `apt-cache show <pkg>` / `dpkg -L <pkg>` for Debian/Ubuntu packages.
         - `pip show <pkg>` / `npm view <pkg>` for Python/Node packages.
         - `gh api <endpoint>` for GitHub-resident schemas.
         - `WebFetch <upstream-doc-url>` for vendor docs (URL derived from `claim_text` by a small template, e.g., `packages.debian.org/<dist>/<pkg>` for the debian case).
         - `Skill context7` / `Skill tavily` for library/framework references.
         - Cache fetched content + content-sha + timestamp in `<output>/external-spec-cache/`. Treat cached fetches >24h old as stale; re-fetch.
         - On verification failure (claim contradicted by upstream artifact): record `verification_status: failed`, set `evidence_ref` to the cached fetch path, and **route the failed claim into `deviation-ledger.yaml` as a §10.4 Regression** with `gold_standard: external-spec` and a new `evidence_source: outcome-verification-pass` field. This reuses the existing Regression-handling path (forces §5.3 rule 3 escalation, blocks §14.5.2 condition 4).

         **Parser scope for `--no-install-recommends` detection (INV-002):** The orchestrator detects `--no-install-recommends` by literal-substring match on the install command line. Variants handled: `--no-install-recommends`, `--no-install-suggests`. Variants currently NOT handled (listed as known limitations): `-o APT::Install-Recommends=false`, `Dpkg::Options::='--force-confdef'` overrides. Multi-line continuation: parser concatenates lines ending in `\` before flag detection.

      3. **For every `runtime` or `cross-system` claim:** synthesize a `deferral_runbook` with **all four required fields** (`next_actor`, `next_command`, `success_criterion`, `fail_criterion`). Schema validation enforced by `evidence-validator` (see §11.2 OVM extensions). Status: `deferred`. Write the runbook to both `outcome-claims.yaml` and a per-claim file at `<output>/deferred-outcomes/<claim_id>.yaml` so a downstream consumer (or fresh agent) can pick up a single runbook by ID.

      4. **For every `V-Deferred-Logical` claim:** at Tier 1, emit a tier-escalation signal (the claim is logged with `verification_status: deferred` and `verifier_tool: tier-2-reescalate`). At Tier 2 (when adversarial debate is already complete), the claim is materialized as a runbook for the operator OR a Wave 6 remediation candidate, with the same four required runbook fields.

      5. Token cost: ~500-1500 tokens when external-spec claims exist; near-zero otherwise.

- **Notes:** Preserve the trailing `---` separator on line 259. The phrase "§3.4 below" in the merged proposal is rewritten to "§11.2 OVM extensions" because the §3.4 numbering is internal to the merged proposal, not SKILL.md.

---

### Amendment 5: Wave-architecture diagram — add 1B.4 + 5.OVM rows
- **Merged proposal source:** §3.1 lines 101-107, §3.2 lines 141-147 (Wave-step naming)
- **SKILL.md target:** §4 wave diagram, lines 126-168 (the fenced code block listing Wave 0 through Wave 7 steps)
- **Operation:** insertion of two new step rows inside the existing diagram (TWO sub-edits in the same fenced code block)
- **Current text — Wave 1 block (verbatim):**
  ```
  Wave 1:   Tier 1 — Grounded Single-Agent Reflection
              1A. Real-code grounding (auggie + serena symbolic chain)
              1B. Mode-specific evidence gathering (UC-1: coverage map; UC-2: tasklist-vs-diff map)
                  — zero-task guard (Change #12); coverage_undefined route (Change #11)
              1C. Single-agent reflection (root-cause-analyst OR self-review)
              1D. Blind calibration (confidence-calibrator) on the Tier 1 card
  ```
- **Replace with (insert "1B.4" line between "1B" continuation and "1C"):**
  ```
  Wave 1:   Tier 1 — Grounded Single-Agent Reflection
              1A. Real-code grounding (auggie + serena symbolic chain)
              1B. Mode-specific evidence gathering (UC-1: coverage map; UC-2: tasklist-vs-diff map)
                  — zero-task guard (Change #12); coverage_undefined route (Change #11)
              1B.4 Outcome-claim extraction -> outcome-claims.yaml (OVM §4.1)
              1C. Single-agent reflection (root-cause-analyst OR self-review)
              1D. Blind calibration (confidence-calibrator) on the Tier 1 card
  ```
- **Current text — Wave 5/6 block (verbatim):**
  ```
  Wave 5:   Synthesis + Evidence-Validator Gate + Report
              5.0 Pre-invocation probe of sc-adversarial (F1/F2/F3 fallback — Change #15)
              5.x Re-read input + verify input_sha256 matches snapshot (Change #10 drift guard)
  Wave 6:   Tier 3 — Remediation Handoff (conditional, opt-in)
  ```
- **Replace with (insert "5.OVM" line between "5.x" and "Wave 6"):**
  ```
  Wave 5:   Synthesis + Evidence-Validator Gate + Report
              5.0 Pre-invocation probe of sc-adversarial (F1/F2/F3 fallback — Change #15)
              5.x Re-read input + verify input_sha256 matches snapshot (Change #10 drift guard)
              5.OVM Outcome-verification pass (in-repo / external-spec / runbook synthesis)
  Wave 6:   Tier 3 — Remediation Handoff (conditional, opt-in)
  ```
- **Notes:** Two separate Edit ops within the same fenced code block. Indentation uses spaces (12 columns) for the leaf bullets. Preserve the rest of the code block exactly.

---

### Amendment 6: §9.1 contract — add OVM additive fields (minor bump)
- **Merged proposal source:** §3.3 lines 177-213 of MERGED-PROPOSAL.md
- **SKILL.md target:** §9.1 stable contract YAML block — end at line 596-597 (`promotion_pending: bool ...`), then closing triple-backticks at line 597, then the paragraph "Each flag has a one-line semantics description in `refs/report-template.md`. Contract version is `v1.0`." at line 599.
- **Operation:** insertion (append new fields BEFORE the closing triple-backticks of the §9.1 YAML)
- **Current text (verbatim with context — last YAML lines + close + next paragraph):**
  ```
  promotion_cross_fs: bool                       # true when source and destination on different filesystems
  promotion_pending: bool                        # true between pre-write (7.3.6) and finalization (7.6); only true in a crashed-mid-run log entry
  ```

  Each flag has a one-line semantics description in `refs/report-template.md`. Contract version is `v1.0`.
- **Replace with (insert before the closing ``` of the YAML block; then update the "Contract version is" line from v1.0 to v1.1):**
  ```
  promotion_cross_fs: bool                       # true when source and destination on different filesystems
  promotion_pending: bool                        # true between pre-write (7.3.6) and finalization (7.6); only true in a crashed-mid-run log entry

  # Outcome verification (additive — minor bump 1.1)
  outcome_claims_path: <abs path> | null
  outcome_claims_total: <int>
  outcome_claims_by_seat:
    in_repo: <int>
    external_spec: <int>
    runtime: <int>
    cross_system: <int>
    v_deferred_logical: <int>
  outcome_claims_verified: <int>
  outcome_claims_deferred: <int>      # all have valid runbooks
  outcome_claims_failed: <int>        # >0 forces status: partial AND becomes §10.4 Regression
  outcome_verification_complete: <bool>   # true ONLY when deferred==0 AND failed==0
  outcome_verification_summary_path: <abs path> | null

  # Derived single-axis convenience field
  outcome_verified: <bool>            # derived: true iff every actionable finding is in-repo OR (external-spec AND no contradiction)
  deferred_outcomes_runbook_present: <bool>   # true iff every deferred row has a complete runbook (next_actor, next_command, success_criterion, fail_criterion)

  # Promotion-gate companion (additive — does NOT change existing promotion_action enum)
  promotion_deferred_outcomes_count: <int>     # surfaced separately to keep promotion_action enum stable
  promotion_deferred_runbook_paths: [<list>]   # one path per deferred runbook moved alongside the work-unit
  ```

  Each flag has a one-line semantics description in `refs/report-template.md`. Contract version is `v1.1`.
- **Notes:** The closing `Contract version is v1.0` line must change to `v1.1`. Also update `contract_version: "1.0"` at line 494 -> `contract_version: "1.1"` (separate Edit; Amendment 7).

---

### Amendment 7: §9.1 — bump `contract_version` literal
- **Merged proposal source:** §3.3 line 177 + §6 line 450
- **SKILL.md target:** SKILL.md line 494
- **Operation:** replacement
- **Current text (with context for unique match):**
  ```
  contract_version: "1.0"
  status: success | partial | failed | dry-run
  mode: pre | post
  ```
- **Replace with:**
  ```
  contract_version: "1.1"
  status: success | partial | failed | dry-run
  mode: pre | post
  ```
- **Notes:** `contract_version: "1.0"` appears exactly once in the file body (verified via Read). Eval-asserted value in §17.6 testability map (line 1503) reads `contract_version == "1.0"` and is updated by Amendment 14b below.

---

### Amendment 7b (sub-Edit of Amendment 7): §17.6 testability-map assertion target
- **Merged proposal source:** consequence of contract_version bump per §3.3 line 177 + §6 line 450
- **SKILL.md target:** SKILL.md line 1503
- **Operation:** replacement
- **Current text (with context):**
  ```
  | §9.1 versioned return contract stability | `yaml_field` | `return-contract.yaml contract_version == "1.0"` |
  ```
- **Replace with:**
  ```
  | §9.1 versioned return contract stability | `yaml_field` | `return-contract.yaml contract_version == "1.1"` |
  ```
- **Notes:** Mandatory companion to Amendment 7 — if contract_version bumps but the eval-asserted value isn't bumped in lockstep, every eval iteration fails. Builder should bundle 7+7b as a single checklist item OR add 7b as a dependent next-item.

---

### Amendment 8: §11.2 — evidence-validator gains 2 new responsibilities
- **Merged proposal source:** §3.4 lines 215-236 of MERGED-PROPOSAL.md
- **SKILL.md target:** §11.2 (lines 786-797 of SKILL.md) — append after the existing four-bullet validator-output interpretation and the `--no-evidence-validator` paragraph, BEFORE the `### 11.3` heading
- **Operation:** insertion (append at end of §11.2)
- **Current text (verbatim with context — last lines of §11.2 + section break):**
  ```
  - Validator subprocess crash -> fall back to inline citation re-Read, mark `evidence_validator_ran: false`, force `status: partial`.

  The `--no-evidence-validator` flag exists for debugging only; using it forces `status: partial` and emits a loud WARN in chat.

  ### 11.3 Blind calibration (anti-anchoring) — disjoint-set rule
  ```
  (Note: SKILL.md actually uses the unicode "→" arrow in line 795; the bullet reads "Validator subprocess crash → fall back to inline citation re-Read...". Treat arrow as `→` not `->`.)
- **Replace with (insertion between the `--no-evidence-validator` paragraph and the `### 11.3` heading):**
  ```
  - Validator subprocess crash → fall back to inline citation re-Read, mark `evidence_validator_ran: false`, force `status: partial`.

  The `--no-evidence-validator` flag exists for debugging only; using it forces `status: partial` and emits a loud WARN in chat.

  **OVM validator extensions (added with v1.1).** `evidence-validator` gains two additional responsibilities, policed by the same drop-not-downgrade rule as citations:

  1. **Runbook schema validation.** For every row in `outcome-claims.yaml` with `verification_status: deferred`, the validator checks that `deferral_runbook` has all four required non-empty fields (`next_actor`, `next_command`, `success_criterion`, `fail_criterion`) and that `next_command` is a single, executable command (not a paragraph). Runbooks failing schema validation are **dropped** the same way unfounded citations are dropped — and force `status: partial`.

  2. **Finding-row presence check.** Every actionable finding from REPORT.md MUST correspond to exactly one row in `outcome-claims.yaml`. Findings without a row are dropped per §11.1's third-bucket rule. The validator does **not** re-resolve upstream lookups (too expensive); it asserts presence and shape, not freshness.

  This is the structural reason runbook quality and claim-coverage cannot rot.

  ### 11.3 Blind calibration (anti-anchoring) — disjoint-set rule
  ```
- **Notes:** Preserve the blank line before the `### 11.3` heading. Use unicode arrow `→` (not ASCII `->`) — SKILL.md line 795 uses the unicode form.

---

### Amendment 9: §14.5.2 — add new promotion-gate condition 10
- **Merged proposal source:** §3.5 lines 237-266 of MERGED-PROPOSAL.md
- **SKILL.md target:** §14.5.2 (lines 1108-1112 of SKILL.md) — append after condition 9, edit the "When all 9 hold..." wrap-up sentence
- **Operation:** insertion of condition 10 + replacement of two numeric anchors in the wrap-up paragraph
- **Current text (verbatim with context — end of cond 9 + wrap-up):**
  ```
  9. **`convergence_score` not null when Tier 2 ran** — if `tier_reached == 2` AND `adversarial_unavailable == true` (F3 path, `convergence_score: null`), promotion is blocked regardless of other conditions. Tier-1-only runs satisfy this vacuously (`convergence_score` is null by construction at T1, but `tier_reached == 1` means the gate's adversarial-result clause does not apply). Equivalently: a Tier 2 run with no merged adversarial verdict MUST NOT promote. *(maps to `gate_evaluation.adversarial_result_present`)*

  When all 9 hold and `--no-promote` is unset, Wave 7 executes. When conditions 1, 3-9 hold but `status == partial`, `--promote-anyway` can override condition 2 only (conditions 1, 3-9 still apply unmodified).
  ```
- **Replace with:**
  ```
  9. **`convergence_score` not null when Tier 2 ran** — if `tier_reached == 2` AND `adversarial_unavailable == true` (F3 path, `convergence_score: null`), promotion is blocked regardless of other conditions. Tier-1-only runs satisfy this vacuously (`convergence_score` is null by construction at T1, but `tier_reached == 1` means the gate's adversarial-result clause does not apply). Equivalently: a Tier 2 run with no merged adversarial verdict MUST NOT promote. *(maps to `gate_evaluation.adversarial_result_present`)*
  10. **`outcome_claims_failed == 0 AND (outcome_verified == true OR deferred_outcomes_runbook_present == true)`** — added with v1.1. Combines the strict-on-failure floor (`outcome_claims_failed == 0`) with the permissive-on-deferred-with-runbook clause (`outcome_verified == true OR deferred_outcomes_runbook_present == true`). Neither alone is sufficient: the former would allow promotion of unverified-but-not-failed claims with no runbook; the latter would allow promotion of failed claims that happen to have a runbook. The merge is strictly safer than either: it blocks promotion only when either formulation alone would also have blocked. When `outcome_claims_deferred > 0` AND condition 10 passes alongside the other 9: promotion fires (`promotion_action: moved`), the per-claim files under `<output>/deferred-outcomes/` are **moved alongside the work-unit** to the destination, and `promotion_deferred_outcomes_count` is non-zero in the contract. A `V-Deferred-Outcome` or `V-Deferred-Logical` row with no runbook is the structural equivalent of `needs_human_decision: true` and forces `status: partial`. *(maps to `gate_evaluation.outcome_claims_failed_zero_AND_verified_or_runbook_present`)*

  When all 10 hold and `--no-promote` is unset, Wave 7 executes. When conditions 1, 3-10 hold but `status == partial`, `--promote-anyway` can override condition 2 only (conditions 1, 3-10 still apply unmodified).
  ```
- **Notes:** Numbering changes "all 9" -> "all 10" and "1, 3-9" -> "1, 3-10" (TWO replacements within the wrap-up paragraph). Preserves the bold + italic + monospace conventions used by conds 1-9.

---

### Amendment 10: §14.5.6 — extend `gate_evaluation` map in promotion-log.yaml
- **Merged proposal source:** §3.5 line 255-256 ("The condition is tagged `gate_evaluation.outcome_claims_failed_zero_AND_verified_or_runbook_present`")
- **SKILL.md target:** §14.5.6 promotion-log.yaml schema (lines 1213-1225 of SKILL.md) — extend the `gate_evaluation:` map and the inline header comment
- **Operation:** insertion of a new map entry + comment text edit
- **Current text (verbatim — gate_evaluation block):**
  ```
  gate_evaluation:                       # 11 atomic fields, 1:1 with the 9 numbered conditions in §14.5.2 (conditions 5 and 6 each have a/b sub-conditions per the structural split)
    mode_post: pass | fail                            # cond 1
    status_success: pass | fail                       # cond 2
    tasklist_completion_pct_1_0: pass | fail          # cond 3
    no_drift_no_regression: pass | fail               # cond 4
    frontmatter_present: pass | fail                  # cond 5a
    frontmatter_status_matches: pass | fail           # cond 5b
    no_citations_dropped: pass | fail                 # cond 6a
    no_grounding_gaps: pass | fail                    # cond 6b
    no_input_drift: pass | fail                       # cond 7
    no_user_decision_pending: pass | fail             # cond 8
    adversarial_result_present: pass | fail | n/a     # cond 9; "n/a" when tier_reached == 1
  ```
- **Replace with:**
  ```
  gate_evaluation:                       # 12 atomic fields, 1:1 with the 10 numbered conditions in §14.5.2 (conditions 5 and 6 each have a/b sub-conditions per the structural split; cond 10 added with v1.1 OVM)
    mode_post: pass | fail                            # cond 1
    status_success: pass | fail                       # cond 2
    tasklist_completion_pct_1_0: pass | fail          # cond 3
    no_drift_no_regression: pass | fail               # cond 4
    frontmatter_present: pass | fail                  # cond 5a
    frontmatter_status_matches: pass | fail           # cond 5b
    no_citations_dropped: pass | fail                 # cond 6a
    no_grounding_gaps: pass | fail                    # cond 6b
    no_input_drift: pass | fail                       # cond 7
    no_user_decision_pending: pass | fail             # cond 8
    adversarial_result_present: pass | fail | n/a     # cond 9; "n/a" when tier_reached == 1
    outcome_claims_failed_zero_AND_verified_or_runbook_present: pass | fail   # cond 10 (v1.1)
  ```
- **Notes:** Header inline-comment changes "11 atomic fields, 1:1 with the 9" -> "12 atomic fields, 1:1 with the 10". Keep YAML formatting + 2-space indent.

---

### Amendment 11: §16 Refs table — add the new ref entry
- **Merged proposal source:** §3.1 line 111 (`refs/claim-extraction-patterns.yaml` (new ref))
- **SKILL.md target:** §16 Refs table (lines 1389-1402 of SKILL.md)
- **Operation:** insertion (new table row)
- **Current text (verbatim — last existing row + closing paragraph):**
  ```
  | `refs/cost-profile.yaml` | (pre-invocation) | **(P7)** Static, machine-readable mirror of the §15 Token Cost Profile table. Callers (sprint TurnLedger, CI) read this BEFORE invoking reflect to pre-flight budget. Reflect itself never reads this at runtime — the file is for caller-side discovery only. Updated in lockstep with §15 by a `make sync-cost-profile` target (see `refs/ops-integration.md`). |

  Refs loaded by the wave that needs them; never pre-loaded. Session-start footprint: SKILL.md only (~50 tokens via Claude Code skill loader).
  ```
- **Replace with (insert a new row after `cost-profile.yaml`, BEFORE the closing paragraph):**
  ```
  | `refs/cost-profile.yaml` | (pre-invocation) | **(P7)** Static, machine-readable mirror of the §15 Token Cost Profile table. Callers (sprint TurnLedger, CI) read this BEFORE invoking reflect to pre-flight budget. Reflect itself never reads this at runtime — the file is for caller-side discovery only. Updated in lockstep with §15 by a `make sync-cost-profile` target (see `refs/ops-integration.md`). |
  | `refs/claim-extraction-patterns.yaml` | Wave 1B.4 | **(v1.1 OVM)** Regenerable pattern list for diff-implicit outcome-claim extraction (`apt-get install`, `pip install`, `npm install`, `gh api`, etc.) plus the verification-seat classifier rubric. Operators add patterns without editing SKILL.md. |

  Refs loaded by the wave that needs them; never pre-loaded. Session-start footprint: SKILL.md only (~50 tokens via Claude Code skill loader).
  ```
- **Notes:** Pipe-character alignment is approximate in markdown tables; renderers reflow. Preserve trailing pipe on each row.

---

### Amendment 12: §17 (Will) — add OVM commitment bullets
- **Merged proposal source:** §3.1 + §3.2 + §3.7 (the user-visible commitment surface)
- **SKILL.md target:** §17 "Will" list (lines 1411-1430 of SKILL.md) — append at end of "Will" bullets, BEFORE the `### Will Not` heading
- **Operation:** insertion (append bullets at end of "Will" block)
- **Current text (verbatim with context — last 2 bullets + heading break):**
  ```
  - **Honor caller-side budget hints** (P5) via `--budget-remaining` and auto-degrade tier per §4.0 step 0.9.
  - **Publish a static cost-profile ref** (P7) at `refs/cost-profile.yaml` so callers can pre-flight check before invoking.

  ### Will Not
  ```
- **Replace with:**
  ```
  - **Honor caller-side budget hints** (P5) via `--budget-remaining` and auto-degrade tier per §4.0 step 0.9.
  - **Publish a static cost-profile ref** (P7) at `refs/cost-profile.yaml` so callers can pre-flight check before invoking.
  - **Extract outcome claims** (v1.1 OVM, §4.1 Step 1B.4) for every UC-2 audit run from spec acceptance criteria, tasklist success criteria, and diff-implicit upstream-artifact patterns (one claim per `(package, install-line)` pair); write to `<output>/outcome-claims.yaml`.
  - **Verify outcome claims by seat** (v1.1 OVM, §4.5 Step 5.OVM): `in-repo` via the existing Serena chain; `external-spec` via `apt-cache`/`pip`/`npm`/`gh api`/`WebFetch`/`context7`/`tavily` with 24h cache; `runtime`/`cross-system`/`V-Deferred-Logical` via a 4-field deferred runbook moved alongside the work-unit at promotion time.
  - **Route failed external-spec verifications into the §10.4 Regression path** with `gold_standard: external-spec` and `evidence_source: outcome-verification-pass`; force §14.5.2 condition 10 fail and block promotion.
  - **Block promotion on outcome-verification failure** via §14.5.2 condition 10: `outcome_claims_failed == 0 AND (outcome_verified == true OR deferred_outcomes_runbook_present == true)`.

  ### Will Not
  ```
- **Notes:** Watch blank line before `### Will Not`. The new bullets reference §4.1 Step 1B.4 and §4.5 Step 5.OVM (introduced by amendments 3 and 4).

---

### Amendment 13: §17.7 Kill-List item 6 — clarification note
- **Merged proposal source:** §8 line 651-657 ("Revisiting §17.7 Kill-List item 6 (5th deviation category) — OVM routes around this kill")
- **SKILL.md target:** §17.7 item 6 (line 1530 of SKILL.md)
- **Operation:** append clarification clause to item 6
- **Current text (verbatim):**
  ```
  6. **5th `unknown` deviation category in deviation-ledger** — Rejected because structural cleanliness requires the 4-category ledger to remain pure; insufficient-evidence findings route to a *separate* artifact (`grounding-gaps.yaml`) with required-field rigor. *Replaces with:* §10.6 Grounding Gaps parallel artifact.
  ```
- **Replace with:**
  ```
  6. **5th `unknown` deviation category in deviation-ledger** — Rejected because structural cleanliness requires the 4-category ledger to remain pure; insufficient-evidence findings route to a *separate* artifact (`grounding-gaps.yaml`) with required-field rigor. *Replaces with:* §10.6 Grounding Gaps parallel artifact. **v1.1 OVM note:** The new `V-Deferred-Logical` (§4.1 Step 1B.4) is a 5th *verification mode*, not a 5th deviation category — failed external-spec verifications still become §10.4 Regressions via the existing 4-class taxonomy. The Kill is respected.
  ```
- **Notes:** Single-bullet append; preserves item numbering and the existing `*Replaces with:*` clause.

---

### Amendment 14: §19.2 INV-023 — note OVM integration
- **Merged proposal source:** §6 lines 485-492 ("v1.1 deferred-hardening integration (Change 7, incorporated from Proposal B §6). OVM folds naturally into §19.2's INV-023 path...")
- **SKILL.md target:** §19.2 INV-023 (lines 1552-1561 of SKILL.md) — append paragraph after the "Why deferred:" paragraph, BEFORE the `### 19.3` heading
- **Operation:** insertion (append paragraph)
- **Current text (verbatim with context — end of §19.2 + section break):**
  ```
  - If the case fails ≥20% of runs: tighten the §11.3 disjoint-set rule from "degrade to non-disjoint" to "BLOCK at Wave 4" when calibrator class cannot be disjoint from reviewer classes.

  **Why deferred:** v1 ships the falsifier eval case (operationalises the claim); v1.1 hardens based on the empirical record. Shipping unconditional sufficiency language in v1 without empirical evidence would be exactly the kind of self-confirming claim this protocol exists to prevent.

  ### 19.3 Auto-rollback of successful promotion (carryover from §14.5)
  ```
- **Replace with:**
  ```
  - If the case fails ≥20% of runs: tighten the §11.3 disjoint-set rule from "degrade to non-disjoint" to "BLOCK at Wave 4" when calibrator class cannot be disjoint from reviewer classes.

  **Why deferred:** v1 ships the falsifier eval case (operationalises the claim); v1.1 hardens based on the empirical record. Shipping unconditional sufficiency language in v1 without empirical evidence would be exactly the kind of self-confirming claim this protocol exists to prevent.

  **OVM integration note (v1.1).** OVM folds naturally into the INV-023 path: iteration-2 evidence for the `T2-converges-on-wrong-answer` case can now include outcome-verification classification accuracy as a sub-criterion, and the v1.1 tightening from "conditional" to "demonstrated" gains a broader sufficiency surface. The post-OVM sufficiency claim covers implementation fidelity *and* upstream-resolvable outcome fidelity, with deferred outcomes explicitly named. This is a tightening, not a loosening.

  ### 19.3 Auto-rollback of successful promotion (carryover from §14.5)
  ```
- **Notes:** Preserves blank lines around the new paragraph.

---

### Amendment 15: §17.6 Testability Map — add OVM rows
- **Merged proposal source:** §3.1 + §3.2 + §3.5 + §7.1 + §7.2 (every new mechanism needs a testability anchor per the §17.6 manifest rule)
- **SKILL.md target:** §17.6 Testability Map (lines 1481-1510 of SKILL.md) — insert new rows at end of table, BEFORE the closing paragraph
- **Operation:** insertion of multiple table rows
- **Current text (verbatim — last few rows + closing paragraph):**
  ```
  | Citation grounding (final report) | `citation_resolves` | `REPORT.md` |
  | Recommendation actionability | `yaml_list_contains` | `recommendation-scrutiny.yaml decision` |
  | Memory write optionality | `yaml_substring` | `telemetry memory_status` |

  A protocol step that cannot map to at least one row here should be simplified or removed. The Testability Map is the manifest the eval workspace consumes; every row references a real protocol decision in §3-§14.5 (no orphan rows, no orphan decisions).
  ```
- **Replace with:**
  ```
  | Citation grounding (final report) | `citation_resolves` | `REPORT.md` |
  | Recommendation actionability | `yaml_list_contains` | `recommendation-scrutiny.yaml decision` |
  | Memory write optionality | `yaml_substring` | `telemetry memory_status` |
  | §4.1 Step 1B.4 outcome-claim extraction | `file_exists` + `yaml_field` | `outcome-claims.yaml outcome_claims_total ≥ 1` |
  | §4.1 Step 1B.4 per-package claim granularity (INV-003) | `yaml_list_contains` | `outcome-claims.yaml` (one row per `(package, install-line)` pair) |
  | §4.5 Step 5.OVM external-spec verification fail -> Regression | `yaml_list_contains` | `deviation-ledger.yaml deviation_class contains regression AND evidence_source == outcome-verification-pass` |
  | §4.5 Step 5.OVM deferred runbook schema (4 required fields) | `yaml_field` | `deferred-outcomes/<claim_id>.yaml next_actor AND next_command AND success_criterion AND fail_criterion` |
  | §14.5.2 cond 10 outcome-verification gate | `yaml_field` | `promotion-log.yaml gate_evaluation.outcome_claims_failed_zero_AND_verified_or_runbook_present` |
  | §7.1 (MERGED) falsifier outcome-verification-docker-cli-miss | `falsifier_skeleton_present` | `cases/falsifier-suite/outcome-verification-docker-cli-miss.yaml` |
  | §7.2 (MERGED) falsifier outcome-verification-deferred-runtime-config | `falsifier_skeleton_present` | `cases/falsifier-suite/outcome-verification-deferred-runtime-config.yaml` |

  A protocol step that cannot map to at least one row here should be simplified or removed. The Testability Map is the manifest the eval workspace consumes; every row references a real protocol decision in §3-§14.5 (no orphan rows, no orphan decisions).
  ```
- **Notes:** The grader assertion `falsifier_skeleton_present` already exists per §12.4 (line 902) — no new grader type required for these rows. The `§7.1` / `§7.2` references are to MERGED-PROPOSAL.md sections (NOT to SKILL.md §7 which is the Agent Delegation Map) — labels clarified above with "(MERGED)".

---

## C. reflect.md command — surface-change inventory

### C.1 Does reflect.md need amendment?

**Decision: NO mandatory surface change required.** The MERGED-PROPOSAL.md contains no §3.X amendment targeting the command file. Specifically:

1. **No new user-facing CLI flags.** OVM operates on every UC-2 run by default; no `--ovm`, `--no-ovm`, or similar flag is introduced. The behavior is invisible to the caller until an outcome-claim fails (which then surfaces via existing `status: partial` + the deviation register).
2. **`allowed-tools` is a frontmatter field on SKILL.md (not the command).** The reflect.md command file does not list tools in its frontmatter — its frontmatter uses `mcp-servers: [auggie, serena, context7, tavily, sequential]` (line 6) which already covers context7/tavily. Adding WebFetch/WebSearch to SKILL.md frontmatter (Amendment 1) is sufficient.
3. **`Tool Coordination` section (lines 138-149)** lists tools used. It could optionally add `WebFetch`, `WebSearch` for parity with SKILL.md, but this is a documentation nicety, not a requirement.
4. **Behavioral Summary / Boundaries / Examples** make no claim that contradicts OVM; the existing copy continues to read correctly.

### C.2 OPTIONAL Amendment 16: reflect.md Tool Coordination parity (LOW PRIORITY)
- **Target:** `/config/.claude/commands/sc/reflect.md` line 147
- **Operation:** insertion of `WebFetch`/`WebSearch` in the Tool Coordination bullet list
- **Current text (verbatim with context — lines 144-149):**
  ```
  - **`mcp__context7__resolve-library-id` / `query-docs`**: external library grounding (Tier 2)
  - **`mcp__tavily__tavily-search`**: targeted web search (Tier 2, rate-limited)
  - **`Task`**: spawn `root-cause-analyst`, `self-review`, `requirements-analyst`, `confidence-calibrator`, `rf-qa`, `rf-qa-qualitative`, `audit-validator`, `evidence-validator`, `socratic-mentor`
  - **`Skill`**: invoke `sc:adversarial-protocol` (Wave 4 merge debate), `task-builder` (Wave 6 remediation), `confidence-check` / `tech-research` (auxiliary)
  - **`Read` / `Grep` / `Glob`**: native fallback when MCPs are unavailable; file:line re-Read for evidence-validator
  - **`Bash`**: diff resolution, git ref expansion, output-dir creation
  ```
- **Replace with (insert a new bullet between `mcp__tavily__tavily-search` and `Task`):**
  ```
  - **`mcp__context7__resolve-library-id` / `query-docs`**: external library grounding (Tier 2); also used by Wave 5.OVM external-spec verification (v1.1)
  - **`mcp__tavily__tavily-search`**: targeted web search (Tier 2, rate-limited); also used by Wave 5.OVM external-spec verification (v1.1)
  - **`WebFetch` / `WebSearch`**: Wave 5.OVM external-spec verification (v1.1) — vendor docs, package registries, upstream changelogs; 24h cache under `<output>/external-spec-cache/`
  - **`Task`**: spawn `root-cause-analyst`, `self-review`, `requirements-analyst`, `confidence-calibrator`, `rf-qa`, `rf-qa-qualitative`, `audit-validator`, `evidence-validator`, `socratic-mentor`
  ```
- **Notes:** OPTIONAL — task-builder may skip if scope discipline argues against expanding the diff. Builder can mark this checklist item with `priority: optional`.

### C.3 reflect.md version bump (NOT recommended)
- The command file is at `version: 2.0.0` (line 8); SKILL.md is at `version: 1.0.0`. They are independent. OVM is a SKILL.md amendment, not a command-surface amendment, so the command-file version need not bump. **Recommendation: leave reflect.md version unchanged.**

---

## D. Summary

- **File-touch count:** 1 mandatory (`/config/.claude/skills/sc-reflect-protocol/SKILL.md`), 1 new file (`/config/.claude/skills/sc-reflect-protocol/refs/claim-extraction-patterns.yaml`), 2 new falsifier YAMLs in `.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/` (R3 owns). Optionally 1 more (`/config/.claude/commands/sc/reflect.md` Tool Coordination parity).
- **Mandatory amendment count to SKILL.md:** **15** (Amendments 1-15, with 7b a coupled sub-Edit of 7). Counting 7b independently: 16 atomic Edit operations.
- **Optional amendment count to reflect.md:** **1** (Amendment 16; reflect.md version bump explicitly NOT recommended).
- **Drift / concerns flagged:**
  1. **HARD DRIFT (BLOCKER for task-builder):** `/config/workspace/Coder/src/superclaude/skills/sc-reflect-protocol/SKILL.md` does NOT exist in this repo. The user's framing assumes the SuperClaude project layout, but the Coder repo lacks `src/superclaude/`. The single live copy of SKILL.md is at `/config/.claude/skills/sc-reflect-protocol/SKILL.md` and Edit operations must target it directly. **No `make sync-dev` to run.** Builder must NOT add any "edit src/ then sync" checklist steps.
  2. SKILL.md §17.5 (line 1467) internally references the `src/superclaude/skills/sc-reflect-protocol/SKILL.md` path as the canonical edit target. This text is stale relative to the Coder repo state but is NOT in scope for this OVM amendment — leave it alone.
  3. Existing in-skill style uses "Change #10" / "INV-NNN" anchor names for Wave 0 step labels (lines 132-135). The MERGED-PROPOSAL.md uses "Change 11" / "Change 12" — when transplanting text, strip the bare "Change N" markers and preserve only the INV-NNN tags (INV-002, INV-003, INV-005) where present, to match in-skill convention.
  4. Amendments 7 and 7b are coupled — if contract_version bumps but the eval-asserted value in §17.6 isn't bumped in lockstep, every eval iteration fails. Builder should bundle 7+7b as a single checklist item OR explicitly mark 7b as dependent.
  5. Amendment 9 (cond 10) and Amendment 10 (gate_evaluation map) are coupled — both must apply or neither, to keep §14.5.2 <-> §14.5.6 in 1:1 sync.
  6. Amendment 8 must use unicode `→` arrow (matching SKILL.md line 795), NOT ASCII `->`.
  7. Amendment 3 contains an embedded YAML fence in the MERGED-PROPOSAL source; preferred transplant rewrites item 3 as prose to avoid nested fence escaping (schema authoritatively defined by Amendment 6 in §9.1).
- **All 15 SKILL.md amendments are pure additive or in-place text inserts.** No deletions. No symbol renames. Backward-compat per §9.4 minor-bump rules holds.
