# Spec Part 1 Analysis — FRs, Architecture, Guards, Schemas

**Investigation type:** Spec Partition Analysis
**Scope:** /config/workspace/IronClaude/.dev/releases/current/persona-research/persona-research-skill-spec.md, lines 1-360 plus orchestrator-assigned Appendix A (lines 554-605) and Appendix B (lines 606-655)
**Status:** Complete
**Date:** 2026-04-29

---

## 1. Functional Requirements Table (§4, lines 160-188)

| FR-ID | Title | Verbatim Requirement | Verbatim Acceptance Criteria | Architecture Component(s) Touched |
|-------|-------|----------------------|------------------------------|-----------------------------------|
| **FR-1** (L164) | Multi-subject input | Skill SHALL accept 1–N subjects per invocation. | Reject `len(subjects) == 0` with a clear error; warn when N > 10. | Orchestrator (input parsing) |
| **FR-2** (L165) | Identity-first ordering | Skill SHALL run identity verification BEFORE deep research for every subject. | `identity_verified` must be `true` before the research subagent for that subject is spawned. See guard table §A. | Identity Verifier (sequential, pre-research) |
| **FR-3** (L166) | Parallel research workers | Skill SHALL spawn one research subagent per verified subject, in parallel. | Subagents launched in a single message; no sequential waiting between subjects. | Research Worker / Discovery Worker (orchestrator dispatch) |
| **FR-4** (L167) | Three artifacts per worker | Each research subagent SHALL produce three artifacts: dossier, persona description, three-questions test. | Output validated against JSON schema in §5.2; missing fields = subject marked `INCOMPLETE` and surfaced in summary. | Research Worker, Worker contract §5.2 |
| **FR-5** (L168) | Source-cited claims | Every claim in a dossier SHALL be source-cited with URL and retrieval date. | Reviewer can spot-check any claim by clicking through; no orphan claims allowed. | Research Worker (dossier_markdown + sources array) |
| **FR-6** (L169) | Verbatim disclaimer | Persona descriptions SHALL include the "modeled on" disclaimer verbatim (§10). | String-equality check before the description is written to disk. | Aggregator / Approval Gate; references §10 (in Part 3) |
| **FR-7** (L170) | No first-person quote fabrication | Persona descriptions SHALL NOT contain first-person quotes attributed to the real person. | Static check: no quoted strings preceded by `<Name> said` or `<Name>:` patterns. Dynamic check: validation pass §8. | Aggregator (static check), Validator (§8 in Part 2) |
| **FR-8** (L171) | Diff, never auto-write | Skill SHALL produce a unified diff against `_bmad/custom/config.toml` but SHALL NOT auto-write it. | User must explicitly approve before any modification of the config file. | Aggregator → Approval Gate |
| **FR-9** (L172) | Refuse unsuitable subjects | Skill SHALL detect and refuse subjects who are deceased, minors, or non-public private individuals. | Identity verification step includes these checks; refuses with explanation. | Identity Verifier; guard G2 |
| **FR-10** (L173) | Halt on ambiguous identity | Skill SHALL halt on ambiguous identity (multiple plausible matches) and ask the user to disambiguate. | No silent disambiguation. | Identity Verifier; guard G1 |
| **FR-11** (L174) | INSUFFICIENT_PUBLIC_DATA sentinel | When the public footprint is below the threshold (§A), skill SHALL return `INSUFFICIENT_PUBLIC_DATA` for that subject and SHALL NOT fabricate to fill the gap. | Sentinel return; surfaced in summary; user can choose to proceed with a thin persona or skip. | Research Worker; guard G3 |
| **FR-12** (L175) | Quantity Flow Diagram emitted | Skill SHALL emit a Pipeline Quantity Flow Diagram (§B) showing how N input subjects became M output personas, with reasons for any divergence. | Always emitted, even when N == M. | Aggregator (emits §B diagram) |
| **FR-13** (L176) | Dossier caching | Skill SHALL cache dossiers by `{name|affiliation|isodate}` so re-runs within the same day reuse research. | TTL 24 hours, configurable. Invalidate on context_artifact change. | Research Worker (cache layer) |
| **FR-14** (L177) | --validate spawns persona | When `--validate` passed, skill SHALL spawn each produced persona once with its own three-questions test and report fidelity. | Fidelity score 0–10; <7 marks the persona as `NEEDS_REFINEMENT` in the summary. | Validator (§8 lives in Part 2) |
| **FR-15** (L178) | Companion archetype default | Skill SHALL preserve the original generic archetype personas alongside named-modeled ones (default: `archetype_companion: true`). | Both `board-polly` (generic) and `board-rosenthal-mod` (named) coexist in the roster. | Aggregator; references §10.4 in Part 3 |
| **FR-16** (L179) | Archetype resolution gate | Before any subject-specific research, skill SHALL resolve each subject against the global archetype store (`archetype_store.path`) and select the best-matching archetype, if any. | Match score computed per §F matching algorithm; result is one of `MATCH`, `AMBIGUOUS`, `NO_MATCH`. See guard G4 §A. | Archetype Manager; references §F (Part 3) |
| **FR-17** (L180) | Archetype-driven worker invocation | When `MATCH`, skill SHALL load the matched archetype's `source_recipe`, `slot_schema`, `persona_description_template`, and `three_questions_template` and use them to drive the per-subject worker. | Worker invocation includes `archetype_id` field; worker output references it. | Archetype Manager → Research Worker; references §E schema (Part 3) |
| **FR-18** (L181) | NO_MATCH discovery worker | When `NO_MATCH`, skill SHALL spawn a generic discovery worker (broader source sweep, longer budget per `archetype_discovery_minutes`) AND SHALL produce a proposed new archetype derived from that subject's research. | Discovery worker emits both: (a) a normal subject dossier, and (b) a proposed `archetype.yaml` for the global store. | Discovery Worker; references §E schema (Part 3) |
| **FR-19** (L182) | Archetype refinement on MATCH | When `MATCH` and `refinement_mode == auto`, skill SHALL fold new evidence (newly discovered sources, newly observed stable-trait patterns) back into the matched archetype with a version bump. | Archetype version increments; `refinement_log` appended; old versions retained as `archetype_id.v<N>.yaml` for rollback. | Aggregator (refinement assembly); Archetype Manager (write) |
| **FR-20** (L183) | Halt on AMBIGUOUS archetype | When `AMBIGUOUS`, skill SHALL halt and surface the top-K matching archetypes with their scores; user disambiguates. | No silent selection in the ambiguity band. | Archetype Manager; guard G4 |
| **FR-21** (L184) | No auto-save to global store | New or refined archetypes SHALL NOT be auto-saved to the global store without user approval. | Saving is gated by an explicit user confirmation; default behavior is "propose, await approval." | Approval Gate |
| **FR-22** (L185) | Generic archetypes (no person/firm names) | Archetypes SHALL be generic — they SHALL NOT contain person names, company names, or fund names in their core fields. Subject-specific bindings live exclusively in the slot schema's filled values at instantiation time. | Static check: archetype `identity_signals.affiliation_keywords` is allowed (it's an *example list* for matching), but archetype `display_name`, `persona_description_template`, and `stable_traits` MUST NOT mention any specific firm/person. Linter rule. | Archetype Manager (linter); references §E schema (Part 3) |
| **FR-23** (L186) | Portable store format | The archetype store SHALL be portable: a single directory of YAML files with no external dependencies, importable/exportable across machines and shareable across users. | One file per archetype. No SQLite, no proprietary index. A README.md in the store directory documents the schema. | Archetype Manager (filesystem only); §E schema (Part 3) |

---

## 2. Architecture Component Table (§5, lines 190-356)

| Component | Role | Inputs | Outputs | Dependencies |
|-----------|------|--------|---------|--------------|
| **Orchestrator** (L196 — outer skill `sc-persona-research-protocol`) | Entry point; sequences the pipeline; dispatches workers; emits §B diagram | YAML inputs (subjects, context_artifact, output_target, archetype_store, naming, research_budget, ethics) per §3 (L84-113) | Aggregated outputs per §3 Outputs (L117-124) | All sub-components |
| **Identity Verifier** (L198-201) | Runs FIRST, sequentially per subject; gates all downstream work | Per-subject `{name, affiliation, role, aliases, archetype_hint}` | `identity_verified: bool`, `canonical_url`, `alternates_considered[]` (per worker contract L253-258) | None (sequential gate) |
| **Archetype Manager** (L203-211, L329-356) | Reads two-layer store (local first, canonical fallback); scores match per archetype; returns MATCH/AMBIGUOUS/NO_MATCH; sole reader of canonical store | Verified subject; `canonical_path` (`<skill_root>/personas/`); `local_path` (`./.claude/skills/sc-persona-research-protocol/personas/`); `match_threshold` (0.7); `ambiguity_band` (0.10); `merge_policy: local_overrides_canonical` | Resolution decision: `MATCH(archetype_id)` or `AMBIGUOUS` (with top-K scores) or `NO_MATCH`; merged runtime archetype roster | Filesystem (canonical + local YAML files); §F matching algorithm (Part 3) |
| **Research Worker** (archetype-driven) (L213-219) | Runs in parallel per MATCH subject; uses archetype's `source_recipe`; fills slot_schema | Subject input + matched archetype (recipe, slot_schema, templates) + research budget | JSON contract per §5.2 (L249-292): subject_input, identity_verification, archetype_resolution, slot_bindings, footprint_score, dossier_markdown, sources[], stable_traits, context_specific_lens, three_questions, persona_toml_block, archetype_refinement_proposal, warnings, status | Source catalog (§5.3); cache layer (FR-13) |
| **Discovery Worker** (generic broad sweep) (L213, L217-221) | Runs in parallel per NO_MATCH subject; longer budget (`archetype_discovery_minutes`); emits both dossier AND proposed archetype | Subject input + bootstrap `generic_public_figure` archetype + extended budget | All Research Worker JSON contract fields PLUS `discovered_archetype_proposal` (L294-305: archetype_id, display_name, rationale, full_archetype_yaml) | Bootstrap archetype `generic_public_figure` (L310); 9-tier source catalog (§5.3 L313-324) |
| **Aggregator** (L224-231) | Merges per-subject outputs; emits 2-tier Quantity Flow Diagram (matched vs new); generates proposed config.toml diff; if `refinement_mode==auto` prepares archetype version bumps; assembles archetype-store proposed write set | All worker JSON contracts; `refinement_mode` setting | Merged persona blocks; unified config.toml diff; archetype proposal write set; §B Quantity Flow Diagram | Worker outputs only — does not re-run worker reasoning (L332) |
| **Approval Gate** (user-facing) (L234-239) | Shows persona diffs + new/refined archetype proposals; user approves each independently; approved archetypes written to local store; approved persona blocks staged in config.toml diff | Aggregator's proposed write set | Approved writes to `local_path` (L356: skill never writes to canonical); finalized config.toml diff | User input; filesystem (local store only) |
| **Validator** (optional) (L242-243) | If `--validate` passed, spawns each persona once and runs three-Qs test; deterministic / idempotent (L333) | Approved persona TOML blocks; persona's three_questions | Per-persona fidelity score 0-10; flags `NEEDS_REFINEMENT` if <7 (FR-14) | §8 in Part 2 (validation methodology) |

### 5.3 Source Catalog (lines 313-324) — 9 tiers

1. **Regulatory & legal filings** (SEC EDGAR, PACER, state courts, bankruptcy estates, class actions)
2. **Deal-history databases** (Crunchbase, PitchBook, RootData, CryptoRank, Messari, Tracxn, Dealroom)
3. **On-chain forensics** (block explorers, Nansen, Arkham, wallet entity tags) — *typically only relevant for crypto archetypes*
4. **Long-form publications** (Substack, Mirror, Medium, fund-website memos) — *with personal vs firm-attributed split*
5. **Audio/video appearances** (YouTube, podcast circuit, conference archives)
6. **Real-time social** (Farcaster, X, Threads, Bluesky, LinkedIn engagement)
7. **Adjacency leakage** (portfolio-CEO podcasts, co-investor commentary, ex-partner interviews, LP-disclosure documents)
8. **Trade press** (per-domain: crypto, gaming, blockchain-gaming, traditional VC, enterprise SaaS, biotech, etc.)
9. **Hostile/adversarial coverage** (investigative journalism, bankruptcy filings naming the subject, class actions)

### 5.4 Service-Boundary Rules (Newman) (lines 329-334)

- Workers do not share state. Cross-subject inference happens only in the Aggregator.
- The orchestrator does not re-do worker reasoning; it consumes the JSON contract and surfaces it.
- The Validator is optional and idempotent. Re-running it on the same persona produces the same fidelity score (deterministic test set).
- The Archetype Manager is the **only** component that reads the canonical store. All other components read archetypes through the Manager's resolution output (the matched archetype, fully merged) — they never touch the store directly.

### 5.5 Vocabulary Note (lines 336-343)

- **Archetype** = generic, reusable template stored in `personas/`.
- **Persona** = colloquially refers to both archetype templates and instantiated subject-specific outputs.
- The directory name MUST stay `personas/` per user contract; spec internals use "archetype" for precision.

### 5.6 Two-Layer Store Merge & Write Rules (lines 345-356)

On startup, Archetype Manager:
1. Enumerates `*.yaml` in `canonical_path` → baseline set.
2. Enumerates `*.yaml` in `local_path` → local set.
3. Builds runtime roster: on `archetype_id` collision **local wins** per `merge_policy: local_overrides_canonical`; local-only and canonical-only both added.
4. Surfaces in run summary which archetypes came from which layer (and which are locally-overridden).

**Writes** (new from discovery, refinements from MATCH) → exclusively `local_path`. Skill **never** writes to `canonical_path` at runtime. Promotion is manual user action.

---

## 3. Appendix A — Guard Tables (verbatim, lines 554-602)

### Guard G1: `identity_verified` (lines 558-567)

| Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-----------------|----------------|--------------|--------------------|--------|
| Zero/Empty | `name=""` | `false` | Halt; error: "name required" | OK |
| One/Minimal | `name="John Smith"`, no affiliation | `false` (under-specified) | Halt; ask user for affiliation | OK |
| Typical | `name="Josh Rosenthal", affiliation="Polychain"` | `true` (single match) | Proceed to research worker | OK |
| Maximum/Overflow | Name matches 5+ public figures | `false` | Halt; ask user to disambiguate | OK |
| Sentinel Value Match | Name is a placeholder like "TBD" or "John Doe" | `false` | Refuse with explanation | OK |
| Legitimate Edge Case | Name with non-Latin characters | `true` if resolvable | Proceed; flag transliteration variants in dossier | OK |

### Guard G2: `subject_is_living_adult_public_figure` (lines 569-578)

| Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-----------------|----------------|--------------|--------------------|--------|
| Zero/Empty | (subsumed by G1) | n/a | n/a | OK |
| One/Minimal | Subject is a public figure (verified) | `true` | Proceed | OK |
| Typical | Public investor with conference talks | `true` | Proceed | OK |
| Maximum/Overflow | Subject is a head-of-state (extreme public profile) | `true`, but flag for elevated caution | Proceed; verbose disclaimer | OK |
| Sentinel Value Match | Subject is deceased | `false` | Refuse; explanation | OK |
| Legitimate Edge Case | Subject is a private individual recently named in news | `false` | Refuse; explain "private individual exception" | OK |

### Guard G3: `public_footprint_above_threshold` (lines 580-589)

| Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-----------------|----------------|--------------|--------------------|--------|
| Zero/Empty | `footprint_score == 0` | `false` | Return `INSUFFICIENT_PUBLIC_DATA`; do not fabricate | OK |
| One/Minimal | `footprint_score == 3` (minimum threshold) | `true` (just clears) | Proceed; flag thin dossier | OK |
| Typical | `footprint_score == 7` | `true` | Proceed normally | OK |
| Maximum/Overflow | `footprint_score == 10` (saturated) | `true` | Proceed; worker may need tiered output (Nygard §6) | OK |
| Sentinel Value Match | Subject's posture is deliberate public silence | `true` if score >= 3 from non-statement signal (deal history) | Proceed; mark "deliberate reticence" as a stable trait | OK |
| Legitimate Edge Case | Subject changed public posture recently (post-departure) | `true` | Proceed; flag temporal split in dossier | OK |

### Guard G4: `archetype_match_resolution` (lines 591-602)

Determines which path the subject takes after Archetype Manager scoring.

| Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-----------------|----------------|--------------|--------------------|--------|
| Zero/Empty | Store is empty (first run) | `NO_MATCH` | Initialize with bootstrap archetype; route subject to discovery worker | OK |
| One/Minimal | Single archetype exists, score below threshold | `NO_MATCH` | Route subject to discovery worker | OK |
| Typical | One archetype scores above threshold; runner-up below `match_threshold - ambiguity_band` | `MATCH` | Route subject to archetype-driven worker | OK |
| Maximum/Overflow | Many archetypes score above threshold | Take highest if gap to runner-up > `ambiguity_band`; otherwise `AMBIGUOUS` | Halt on AMBIGUOUS; otherwise proceed | OK |
| Sentinel Value Match | `archetype_hint` provided in input | `MATCH(forced)` | Skip scoring; use forced archetype; flag `match_path: USER_FORCED` | OK |
| Legitimate Edge Case | Top score equals threshold exactly | `MATCH` (inclusive comparison) | Proceed; document threshold-edge case in dossier | OK |

---

## 4. Appendix B — Pipeline Quantity Flow Diagram (verbatim, lines 606-652)

```
[Input: N subjects]
        |
        v
[Stage 1: Identity Verify]  -- N in, N' out where N' <= N
        |                       (failures: ambiguous, deceased, private)
        v
[Stage 2: Archetype Resolution]  -- N' in, splits into:
        |                            P = matched (route to archetype-driven worker)
        |                            Q = no-match (route to discovery worker)
        |                            R = ambiguous → user disambiguates → folds back to P or Q
        |                            P + Q == N' (after disambiguation)
        v
[Stage 3a: Archetype-Driven Workers]   [Stage 3b: Discovery Workers]
   P workers spawned in parallel          Q workers spawned in parallel
   (use matched archetype's recipe)       (broad sweep; longer budget)
        |                                       |
        ↓                                       ↓
[Stage 4: Per-worker output]  -- P+Q attempts → M complete (M <= P+Q)
        |                        (incomplete: budget exceeded, network failure)
        |                        (refused: INSUFFICIENT_PUBLIC_DATA)
        v
[Stage 5: Aggregator]  -- M personas in, outputs:
        |                      • M persona blocks
        |                      • 1 unified config.toml diff
        |                      • K archetype proposals (K = new archetypes from discovery + refinements)
        v
[Stage 6: Approval Gate]  -- user approves: persona diffs, archetype proposals
        |                     approved archetypes written to GLOBAL store
        |                     approved persona blocks staged in LOCAL config.toml diff
        v
[Stage 7 (optional): Validator]  -- M personas in, M fidelity scores out
        |                            (scores <7 marked NEEDS_REFINEMENT)
        v
[Output: M personas, 1 diff, K archetype updates, optional validation report]

DIVERGENCE POINTS:
  Stage 1: N → N'    (failed identity verification)
  Stage 2: N' → P+Q  (split by archetype match path)
  Stage 4: P+Q → M   (research failures or insufficient data)
  Stage 5: M → M + K (K archetype proposals derived from research)
  Stage 7: M → {OK_personas, NEEDS_REFINEMENT_personas}

The Quantity Flow Diagram MUST be emitted on every run with actual counts populated.
```

---

## 5. §3 Inputs & Outputs Schemas (lines 80-156)

### Inputs Schema (lines 84-113)

The full YAML input shape — note that the orchestrator's instruction asked for "the 6+ extra fields beyond GOAL/WHY/WHERE", but the spec's actual top-level keys are listed below. The spec does NOT use the GOAL/WHY/WHERE convention; it uses domain-specific keys:

| Key | Sub-fields | Required? | Default | Line |
|-----|-----------|-----------|---------|------|
| `subjects` | list of `{name, affiliation, role, aliases, archetype_hint}` | required, 1+ entries | none | L85-90 |
| `subjects[].name` | string | required | none | L86 |
| `subjects[].affiliation` | string | required | none | L87 |
| `subjects[].role` | string | optional but strongly recommended | none | L88 |
| `subjects[].aliases` | list | optional disambiguation hints | `[]` | L89 |
| `subjects[].archetype_hint` | string (archetype_id override) | optional | `null` | L90 |
| `context_artifact` | path string (`@/path/to/file`) | optional | none | L91 |
| `output_target.dossier_dir` | path | required | `_bmad-output/planning-artifacts/persona-research/` | L93 |
| `output_target.config_diff` | path | required | `_bmad/custom/config.toml` (PROPOSED diff; never auto-written) | L94 |
| `archetype_store.canonical_path` | path | required | `<skill_root>/personas/` (READ-ONLY at runtime) | L98 |
| `archetype_store.local_path` | path | required | `./.claude/skills/sc-persona-research-protocol/personas/` (RUNTIME-WRITABLE) | L99 |
| `archetype_store.merge_policy` | enum | required | `local_overrides_canonical` | L100 |
| `archetype_store.match_threshold` | float | required | `0.7` (min similarity for archetype reuse) | L101 |
| `archetype_store.ambiguity_band` | float | required | `0.10` (if top-2 within band → ask user) | L102 |
| `archetype_store.refinement_mode` | enum (`auto` \| `propose` \| `off`) | required | `auto` | L103 |
| `archetype_store.promotion_candidates` | bool | required | `true` (run summary surfaces promotion candidates) | L104 |
| `naming.code_prefix` | string | required | `board-` | L106 |
| `naming.archetype_companion` | bool | required | `true` (also keep generic archetype, see §10) | L107 |
| `research_budget.per_subject_minutes` | int | required | `12` (soft cap) | L109 |
| `research_budget.archetype_discovery_minutes` | int | required | `18` (extra budget when no archetype matches, FR-18) | L110 |
| `ethics.attestation_required` | bool | required | `true` (see §10) | L112 |

### Outputs Schema, per subject (lines 118-124)

1. **Evidence dossier** — markdown, ~500 words, source-cited with retrieval date. Path: `<dossier_dir>/<code>-dossier.md` (L119-120).
2. **Persona description** — TOML block, ready to paste into `[agents.<code>]`. Includes the modeled-on disclaimer (§10) (L121).
3. **Three-questions test** — three concrete questions the persona should ask any pitch in this domain. Used as the validation gate (§8) (L122).
4. **Aggregated proposed diff** — single unified diff against `_bmad/custom/config.toml` covering all subjects. **Never auto-written** (L123).
5. **Validation report** (if `--validate` passed) — for each persona, the spawned subagent's response to its own three-questions test, plus a fidelity score (L124).

### Worker Contract Schema (§5.2, lines 247-305)

Strict JSON object emitted per worker (non-conformance = hard failure):

| Field | Type | Notes |
|-------|------|-------|
| `subject_input` | obj `{name, affiliation, role}` | L253 |
| `identity_verification.verified` | bool | L255 |
| `identity_verification.canonical_url` | string | L256 |
| `identity_verification.alternates_considered` | list[string] | L257 |
| `archetype_resolution.matched_archetype_id` | string | L260 |
| `archetype_resolution.match_score` | float | L261 |
| `archetype_resolution.match_path` | enum: `MATCH \| DISCOVERED \| USER_FORCED` | L262 |
| `archetype_resolution.alternates_considered` | list of `{id, score}` | L263-264 |
| `slot_bindings` | obj (subject-specific values like `firm_name`, `firm_blog_url`, `mirror_handle`) | L267-271 |
| `footprint_score` | int 0-10 | L273 |
| `dossier_markdown` | string | L274 |
| `sources[]` | list of `{url, category, retrieved, claim_ids[], from_archetype_recipe: bool}` | L275-277 |
| `stable_traits` | list[string] | L278 |
| `context_specific_lens` | list[string] | L279 |
| `three_questions` | list[string] of length 3 | L280 |
| `persona_toml_block` | string | L281 |
| `archetype_refinement_proposal` | obj `{applies_to_archetype_id, deltas[]}` where deltas are `{type: "add_source"|"add_stable_trait_pattern", ...}` | L282-288 |
| `warnings[]` | list[string] | L289 |
| `status` | enum: `OK \| INCOMPLETE \| INSUFFICIENT_PUBLIC_DATA \| REFUSED` | L290 |

**Discovery-worker additional field** (NO_MATCH path) (L294-305):
- `discovered_archetype_proposal.archetype_id` (string)
- `discovered_archetype_proposal.display_name` (string)
- `discovered_archetype_proposal.rationale` (string)
- `discovered_archetype_proposal.full_archetype_yaml` (string per §E schema, in Part 3)

---

## 6. Cross-Slice References (FRs in my slice that depend on Part 2 / Part 3 sections)

These references inside lines 1-360 point OUTSIDE my slice — the builder/coordinator should ensure Part 2/Part 3 analysts deliver the referenced sections:

| Source (in my slice) | References | Target Slice |
|----------------------|------------|--------------|
| FR-6 (L169) | "the 'modeled on' disclaimer verbatim (§10)" | Part 3 (§10 lives at lines 487+) |
| FR-7 (L170) | "Dynamic check: validation pass §8" | Part 2 (§8 at lines 403+) |
| FR-11 (L174) | "below the threshold (§A)" | Part 1 (§A in my slice — internal OK) |
| FR-14 (L177) | "When `--validate` passed... fidelity" | Part 2 (§8 validation methodology) |
| FR-15 (L178) | references "(§10)" via context (L107 archetype_companion) | Part 3 (§10.4 at L506) |
| FR-16 (L179) | "Match score computed per §F matching algorithm" | Part 3 (§F at L904+) |
| FR-17 (L180) | "matched archetype's `source_recipe`, `slot_schema`, `persona_description_template`, `three_questions_template`" → §E schema | Part 3 (§E at L724+) |
| FR-18 (L181) | "proposed `archetype.yaml`" → §E schema | Part 3 (§E archetype schema) |
| FR-19 (L182) | "version bump... `refinement_log` appended" | Part 3 (§E schema for refinement_log shape) |
| FR-22 (L185) | "archetype `display_name`, `persona_description_template`, and `stable_traits`" — these are §E schema fields | Part 3 (§E) |
| Architecture L242 | "Validator (spawns each persona, runs three-Qs test)" | Part 2 (§8 validation) and Appendix C three-Qs template (lines 656+, Part 3 territory) |
| Architecture L587 (G3 max overflow) | "worker may need tiered output (Nygard §6)" | Part 2 (§6 Failure Modes at L360+) |
| §3 Outputs L122 | "Used as the validation gate (§8)" | Part 2 |
| §3 Outputs L124 | "if `--validate` passed... fidelity score" | Part 2 (§8) |
| §3 Inputs L107 | "see §10" (archetype_companion behavior) | Part 3 |
| §3 Inputs L112 | "ethics... see §10" | Part 3 |
| L116 archetype source-recipe note | "archetype's `source_recipe` field at runtime (§5.3)" | Internal to my slice — OK |
| L335 Archetype Manager | "matched archetype, fully merged" — depends on §E merge semantics | Part 3 (§E) |

---

## 7. Internal Contradictions (within my slice, lines 1-360 + Appendices A, B)

### IC-1 — `personas/` directory location is described inconsistently across sections

- **Frontmatter §0 (L24-25):** "Canonical source: `/config/workspace/IronClaude/src/superclaude/skills/sc-persona-research-protocol/`" — implies the canonical store is under `src/`.
- **§3 Inputs (L98):** `canonical_path: "<skill_root>/personas/"` — implies it lives inside the skill root, but `<skill_root>` is undefined; it is unclear whether `<skill_root>` resolves to the `src/` location or the `.claude/` synced copy.
- **§5 component diagram (L205-206):** "local: `./.claude/skills/.../personas/`; canonical: `<skill_root>/personas/`" — same ambiguity.
- **Impact:** Readers cannot deterministically resolve `<skill_root>` from the spec alone. The spec is internally consistent in *naming* the layers but does not pin down the path resolution rule for `<skill_root>` in any FR or guard.

### IC-2 — `archetype_companion` default is named twice with `archetype_hint` semantics not fully closed

- **§3 Inputs (L90):** `archetype_hint: null   # optional override: force a specific archetype_id`
- **Guard G4 sentinel row (L601):** `archetype_hint` provided → "MATCH(forced)" with `match_path: USER_FORCED`.
- **Worker contract (L262):** `match_path: "MATCH | DISCOVERED | USER_FORCED"`.
- **§5.2 archetype_resolution example (L260-262):** `matched_archetype_id: "crypto_native_vc"` paired with `match_path: "MATCH | DISCOVERED | USER_FORCED"` — but the worker contract sample shows only one matched_archetype_id. If `match_path == DISCOVERED`, what is `matched_archetype_id`? The discovered archetype's new id? Or null until approval? The slice does not specify.
- **Impact:** Mild. Worker contract field semantics for `DISCOVERED` are under-specified within my slice.

### IC-3 — FR-3 "single message" for parallel spawn vs FR-2 "sequentially per subject"

- **FR-2 (L165):** identity verification BEFORE deep research, "for every subject."
- **FR-3 (L166) + acceptance criteria:** "Subagents launched in a single message; no sequential waiting between subjects."
- **§5.1 component diagram (L198-199):** "Identity Verifier ← runs FIRST, sequentially per subject."
- **Tension:** If identity verification runs sequentially per subject (L199), then research workers cannot all be spawned in a single message simultaneously with verification — research spawn waits for ALL verifications to complete. This is consistent if interpreted as "verify ALL sequentially, then spawn ALL research in one parallel batch", but the spec does not state this explicitly. A reader could misread "sequentially per subject" as interleaving verify→research per subject.
- **Impact:** Low. Likely just an under-specified phrasing; not a true contradiction.

### IC-4 — Bootstrap archetype path is implicit

- **§5.3 (L310):** "The skill ships with a **bootstrap archetype** named `generic_public_figure`..."
- **Guard G4 zero/empty row (L597):** "Store is empty (first run) → `NO_MATCH` → Initialize with bootstrap archetype."
- **§5.6 (L348):** Manager enumerates `*.yaml` in canonical_path and local_path on startup.
- **Tension:** If "store is empty" triggers bootstrap initialization, where does the bootstrap archetype YAML live? It must be in `canonical_path` (since it ships with the skill), in which case the store cannot be "empty" — only `local_path` would be empty. The spec conflates "store is empty" (likely meaning local_path empty AND no matches) with "bootstrap initialization." 
- **Impact:** Low-medium. The bootstrap archetype must always be present in canonical, so guard G4's "Zero/Empty" row's "Store is empty (first run)" wording is misleading.

### IC-5 — Aggregator counts vs Quantity Flow Diagram counts on AMBIGUOUS

- **§B Stage 2 (L615-619):** "P + Q == N' (after disambiguation)" — implies AMBIGUOUS resolves to either P or Q via user input.
- **FR-20 (L183) + Guard G4 (L600):** "Halt and surface" / "Halt on AMBIGUOUS."
- **Tension:** If the skill HALTS on AMBIGUOUS (FR-20), the run does not continue past Stage 2 in the AMBIGUOUS case. The diagram's "R = ambiguous → user disambiguates → folds back to P or Q" implies a continuous flow with mid-pipeline user interaction. The spec does not specify whether HALT means full-pipeline restart or mid-run prompt. Internal ambiguity about pipeline resumability.
- **Impact:** Medium. Builder must clarify whether AMBIGUOUS is a runtime mid-pipeline prompt or a full halt requiring re-invocation.

### IC-6 — `archetype_resolution.alternates_considered` shape vs identity_verification.alternates_considered

- **L257 (identity_verification.alternates_considered):** `["..."]` — list of strings.
- **L263-264 (archetype_resolution.alternates_considered):** `[{ "id": "...", "score": 0.41 }]` — list of objects.
- **Tension:** Same field name, two different shapes in the same JSON contract. Not a true contradiction (different parent objects), but easy source of implementation confusion.
- **Impact:** Low. Naming inconsistency only.

---

## 8. Summary

This slice (lines 1-360 + Appendices A & B) defines the SPEC FOUNDATION for `sc-persona-research-protocol`:

- **23 FRs** (FR-1 … FR-23) covering input handling, identity verification, parallel research, archetype resolution, refinement, output discipline, store portability.
- **8 architectural components**: Orchestrator, Identity Verifier, Archetype Manager, Research Worker, Discovery Worker, Aggregator, Approval Gate, Validator.
- **4 guard tables (G1-G4)** at boundary points (identity, suitability, footprint, archetype match).
- **1 quantity-flow diagram** with 7 stages and 5 explicit divergence points.
- **2 schemas**: input YAML (~21 keys across 6 top-level groups) and worker JSON contract (16 fields plus discovery-worker extension).

**Cross-slice dependencies**: 17 references to sections in Parts 2 and 3 — most critical are §E archetype schema (Part 3, drives FR-17/18/19/22), §F matching algorithm (Part 3, drives FR-16), §8 validation (Part 2, drives FR-7/14), §10 ethics (Part 3, drives FR-6/15), and §6 failure modes (Part 2, referenced from G3 overflow row).

**6 internal contradictions/under-specifications** identified, none catastrophic; most are phrasing ambiguities (path resolution for `<skill_root>`, AMBIGUOUS halt semantics, bootstrap archetype location) that the builder should pin down before code generation.

**Critical takeaway for skill-creator**: The architecture is centered on the Archetype Manager as the only canonical-store reader and on a strict worker JSON contract. FR-22 (no person/firm names in archetype core fields) is a hard linter rule. FR-21 (no auto-save without user approval) and FR-8 (no auto-write of config.toml) jointly establish a "propose-only, never auto-mutate" discipline that the implementation must honor in every write path.
