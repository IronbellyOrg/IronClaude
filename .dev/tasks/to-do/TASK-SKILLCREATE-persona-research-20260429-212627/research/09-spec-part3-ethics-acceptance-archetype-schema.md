# Research: Spec Part 3 — Ethics, Acceptance, Archetype Schema, Matching Algorithm

**Investigation type:** Spec Partition Analysis
**Scope (assigned):** /config/workspace/IronClaude/.dev/releases/current/persona-research/persona-research-skill-spec.md, lines 661-993 (per prompt: §10 ethics + §10.1 disclaimer + §10.2 unsuitable-subject refusal rules, §11 acceptance FR-1..FR-26, §12 open questions OQ-1..OQ-9, Appendix E archetype.yaml schema, Appendix F matching algorithm)
**Scope (actual):** Lines 487-553 contain §10/§11/§12; lines 724-902 contain Appendix E; lines 904-967 contain Appendix F. The prompt's line range (661-993) does NOT actually cover §10/§11/§12 — those sections live at 487-553. To fulfill the protocol I read the canonical sections by name regardless of the prompt's stated line range. See "Prompt-vs-actual line discrepancies" in the Internal Contradictions section.
**Status:** Complete
**Date:** 2026-04-29

---

## 1. §10.1 Mandatory Disclaimer (VERBATIM — character-for-character)

The disclaimer is a single blockquote-italic line in the spec at line 493 of `persona-research-skill-spec.md`. The disclaimer text follows. ANY deviation from the contents of the fenced block below is a CRITICAL failure per `VALIDATION_REQUIREMENT ETHICS_DISCLAIMER_VERBATIM`.

**Source citation:** spec §10.1, line 493.

**Surrounding context:** lines 491-494
- L491: `### 10.1 Mandatory disclaimer (verbatim, prepended to every persona description)`
- L492: blank
- L493: the disclaimer (preceded on that line by `> *` and followed by `*` — the asterisks are the markdown italic markers and the `>` is the blockquote marker; the disclaimer **text itself** is what lies between the asterisks)
- L494: blank

The disclaimer text (between the italic markers, exactly as written in the spec):

```text
Modeled on the public posture of [Name, Affiliation]. Captures observable patterns from public statements, conference appearances, and disclosed deal history; does not generate first-person quotes attributed to the real person. For internal pitch stress-testing only — not endorsed by, not affiliated with, and not a representation of the real individual's views.
```

Notes for byte-faithful copying:
- Punctuation includes one em-dash (`—`, U+2014) between "stress-testing only" and "not endorsed by". This is NOT a hyphen or two hyphens. It IS the Unicode em-dash character.
- The apostrophe in "individual's" is a straight ASCII apostrophe `'` (U+0027) as written in the spec source.
- The hyphen in "stress-testing" is a regular hyphen-minus `-` (U+002D).
- There is one period at the end of the second sentence ("real person.") and one period at the very end ("real individual's views.").
- Bracketed placeholder is `[Name, Affiliation]` — square brackets, comma-space inside.
- The disclaimer is a single line with no internal line breaks.

The exact rendering in the spec source uses a leading `> *` and trailing `*` (markdown blockquote + italic emphasis). When emitted into a generated SKILL.md per `VALIDATION_REQUIREMENT ETHICS_DISCLAIMER_VERBATIM`, copy ONLY the contents of the fenced block above (the disclaimer string itself), not the surrounding `> *...*` markdown wrappers.

The same disclaimer text is restated almost-but-NOT-identically in Appendix E `persona_description_template` (lines 849-854) — see "Internal Contradictions" section: the Appendix E version **adds** a closing parenthetical clause and a leading sentence break that the §10.1 canonical version does not have. The §10.1 version (this section) is the authoritative one for verbatim emission.

---

## 2. §10.2 Output Discipline + Unsuitable-Subject Refusal Rules (verbatim)

**Source citation:** spec §10.2, lines 495-499.

The spec §10.2 is titled "Output discipline" (NOT "unsuitable-subject refusal rules" as the prompt states — the prompt mis-titled this section). It contains three bullets, the third of which IS the unsuitable-subject refusal rule. All three are reproduced verbatim:

```markdown
### 10.2 Output discipline

- **No attributed novel quotes.** Persona speaks in patterns ("a partner with this profile would push back here"), never in invented direct speech ("Josh would say…"). FR-7 enforces this statically and dynamically.
- **No private-matter inference.** Persona may model professional posture only. Health, family, undisclosed personal views: out of bounds.
- **Refuse on unsuitable subjects.** Deceased, minors, private individuals, witnesses in active litigation: refuse (FR-9).
```

**Unsuitable-subject categories** (from the third bullet, line 499) — refuse to model:
1. Deceased subjects
2. Minors
3. Private individuals (i.e., non-public)
4. Witnesses in active litigation

The refusal mechanism is anchored in **FR-9** (line 172): "Skill SHALL detect and refuse subjects who are deceased, minors, or non-public private individuals. Identity verification step includes these checks; refuses with explanation." Note that FR-9 lists three categories (deceased, minors, non-public private individuals) but §10.2 lists FOUR (the additional one being "witnesses in active litigation"). See Internal Contradictions for this divergence.

**Related ethics subsections** (also in §10):

- **§10.3 User attestation (lines 501-504)** — when `attestation_required: true` (default), the skill SHALL prompt the user once per invocation with the verbatim attestation string at line 504:
  ```text
  These personas are for internal stress-testing of your own material. They will be labeled 'modeled on' the named individuals and will not generate quotes attributed to them. You will not present them externally as representations of the real person. Confirm to proceed.
  ```
  (This is a SECOND verbatim-mandated ethics string in addition to the §10.1 disclaimer. The skill-creator should treat it with the same byte-fidelity care.)

- **§10.4 Companion archetype default (lines 506-508)** — `archetype_companion: true` keeps generic archetypes alongside named-modeled persona, providing a "clear escape hatch" for generic-pattern discussion. Anchored to FR-15 (line 178).

**Cross-references back to functional requirements:**
- §10.1 disclaimer ↔ FR-6 (line 169): "Persona descriptions SHALL include the 'modeled on' disclaimer verbatim (§10). String-equality check before the description is written to disk."
- §10.2 first bullet ↔ FR-7 (line 170): "Persona descriptions SHALL NOT contain first-person quotes…"
- §10.2 third bullet ↔ FR-9 (line 172): refusal of unsuitable subjects.
- §10.3 attestation: not directly anchored to a numbered FR; introduces the `attestation_required` config flag.
- §10.4 companion archetype ↔ FR-15 (line 178): preserve generic archetypes alongside named-modeled.

---

## 3. §11 Acceptance Criteria — Mapping Table (FR-1..FR-26)

**Source citation:** spec §11 "Acceptance Criteria (Wiegers)", lines 512-530. The section header is at line 512; criteria are numbered 1-15 and span lines 516-530.

§11 has **15 numbered acceptance items** (NOT 26 as the prompt's "FR-1..FR-26 table" implies). The first item (line 516) bundles ALL of FR-1 through FR-23 by reference: "FR-1 through FR-23 all pass (per-FR acceptance criteria above)". Criteria 12 and 13 add tests for FR-24/FR-25/FR-26 (defined in §9.2, lines 472-474). Criteria 14-15 add coverage for store-layer behavior tied to FR-19/FR-21.

The prompt requested a 26-row FR-by-FR mapping. To serve that intent, I produce two tables: (a) the 15 §11 acceptance items as written, with line citations and what they test; and (b) a synthesized FR-1..FR-26 → acceptance-test rationale mapping derived by joining §11 with the per-FR acceptance criteria embedded in the §4 FR table (lines 164-186) and the §9.2 model-tiering FRs (lines 472-474).

### 3a. §11 Acceptance Criteria as Written (15 items, verbatim line citations)

| §11 # | Spec line | Anchor | Verbatim acceptance test (paraphrased only where compressed for table) |
|-------|-----------|--------|------------------------------------------------------------------------|
| 1 | 516 | FR-1..FR-23 | "FR-1 through FR-23 all pass (per-FR acceptance criteria above)." Bundles every FR's per-row acceptance criterion from §4 by reference. |
| 2 | 517 | §7 probes | "All five Whittaker probes (§7) verified by red-team test cases in the skill's own test suite." |
| 3 | 518 | §10.1 / FR-6 | "The mandatory disclaimer (§10.1) appears verbatim in every produced persona description." |
| 4 | 519 | FR-14 | "Validator achieves ≥7/10 fidelity on a held-out test subject (e.g., a well-documented public figure not in the original use case)." |
| 5 | 520 | FR-3 | "Three-subjects-in-parallel test completes within `3 × per_subject_minutes` ceiling (proves parallel orchestration is real)." |
| 6 | 521 | FR-9 / §10.2 | "Skill refuses on a deceased-subject test fixture and a minor-subject test fixture." |
| 7 | 522 | FR-12 / App B / App A | "Skill emits a non-empty Quantity Flow Diagram and Guard Boundary Table on every run." |
| 8 | 523 | FR-16/17/18/19 | "Archetype lifecycle test: First-ever run on a novel subject produces both a dossier and a proposed archetype; second run on a matching subject reuses the archetype with refinement deltas; third run on the same subject is a cache hit." |
| 9 | 524 | FR-22 | "Archetype generic-purity test: A linter check rejects any archetype containing person names, fund names, or company names in core fields (FR-22)." |
| 10 | 525 | FR-23 | "Archetype portability test: Copying the entire archetype-store directory to a fresh machine and running the skill there produces identical match scores against the same subjects (no hidden state)." |
| 11 | 526 | FR-21 | "Approval-gate test: Skill never modifies the local archetype store or the project's roster file without explicit user approval; canonical store is never written by the skill at runtime." |
| 12 | 527 | FR-24 / FR-26 | "Model-tiering test: Per FR-24/FR-26, Opus token spend in a typical per-subject worker run is <15% of total tokens. Test fixture: research a moderately-documented subject end-to-end; assert the per-tier spend report." |
| 13 | 528 | FR-25 | "Tavily routing test: Per FR-25, when Tavily MCP is configured, all general web searches route through Tavily. Test fixture: stub Tavily; assert worker invokes `tavily_search` rather than direct fetch for non-API sources." |
| 14 | 529 | Two-layer store (§0/§3) | "Two-layer store test: Canonical store contains archetype `crypto_native_vc.v1`. Local store contains `crypto_native_vc.v3`. Match returns local v3; run summary notes the override." |
| 15 | 530 | Promotion-candidate flow (§0/§3) | "Promotion-candidate test: Local archetype refined from 3 subjects, stable >30 days, version >= 2 — appears in run summary's promotion-candidates list with the suggested copy command." |

### 3b. Synthesized FR-1..FR-26 → Test Rationale Mapping

Each FR's acceptance criterion is the right column of the §4 FR table (or the inline test in §9.2 for FR-24/25/26). §11 Item 1 bundles FRs 1-23; the table below lifts each per-FR acceptance to its own row and notes which §11 item (if any) tests it directly.

| FR | Spec line | Requirement (compressed) | Per-FR acceptance criterion (from §4 / §9.2) | Direct §11 item |
|----|-----------|--------------------------|----------------------------------------------|-----------------|
| FR-1 | 164 | Accept 1–N subjects per invocation | Reject `len(subjects) == 0` with clear error; warn when N>10 | §11 #1 (bundled) |
| FR-2 | 165 | Identity verification BEFORE deep research | `identity_verified` must be `true` before research subagent spawn (Guard G1, App A) | §11 #1 |
| FR-3 | 166 | One research subagent per verified subject in PARALLEL | Subagents launched in single message; no sequential waiting | §11 #1, #5 |
| FR-4 | 167 | Three artifacts per worker (dossier, persona description, three-questions) | Output validated against §5.2 JSON schema; missing fields = `INCOMPLETE` and surfaced in summary | §11 #1 |
| FR-5 | 168 | Every dossier claim source-cited (URL + retrieval date) | Reviewer can spot-check; no orphan claims | §11 #1 |
| FR-6 | 169 | Persona descriptions include §10 disclaimer verbatim | String-equality check before write to disk | §11 #1, #3 |
| FR-7 | 170 | No first-person quotes attributed to real person | Static check: no quoted strings preceded by `<Name> said` / `<Name>:` patterns; dynamic via §8 validation | §11 #1 |
| FR-8 | 171 | Produce unified diff against `_bmad/custom/config.toml`; NEVER auto-write | User must explicitly approve | §11 #1, #11 |
| FR-9 | 172 | Refuse deceased / minors / non-public private individuals | Identity-verification step includes checks; refuses with explanation | §11 #1, #6 |
| FR-10 | 173 | Halt on ambiguous identity; ask user to disambiguate | No silent disambiguation | §11 #1 |
| FR-11 | 174 | Below footprint threshold → `INSUFFICIENT_PUBLIC_DATA`; do NOT fabricate | Sentinel return; surfaced in summary | §11 #1 |
| FR-12 | 175 | Emit Pipeline Quantity Flow Diagram (App B) | Always emitted, even when N==M | §11 #1, #7 |
| FR-13 | 176 | Cache dossiers by `{name\|affiliation\|isodate}`; TTL 24h | Configurable; invalidate on context_artifact change | §11 #1 |
| FR-14 | 177 | `--validate` flag spawns persona once with three-questions test → fidelity score | Score 0-10; <7 → `NEEDS_REFINEMENT` in summary | §11 #1, #4 |
| FR-15 | 178 | Preserve generic archetype personas alongside named-modeled (default `archetype_companion: true`) | Both `board-polly` (generic) and `board-rosenthal-mod` (named) coexist | §11 #1 |
| FR-16 | 179 | Resolve subject against global archetype store BEFORE research | Match score per §F; result one of `MATCH`/`AMBIGUOUS`/`NO_MATCH`; Guard G4 | §11 #1, #8 |
| FR-17 | 180 | On `MATCH`: load matched archetype's recipe/schema/templates and use them in worker | Worker invocation includes `archetype_id`; output references it | §11 #1, #8 |
| FR-18 | 181 | On `NO_MATCH`: spawn discovery worker AND produce proposed new archetype | Discovery worker emits BOTH dossier AND proposed `archetype.yaml` | §11 #1, #8 |
| FR-19 | 182 | On `MATCH` + `refinement_mode == auto`: fold new evidence back into archetype with version bump | Version increments; `refinement_log` appended; old versions retained as `<id>.v<N>.yaml` | §11 #1, #8, #14 |
| FR-20 | 183 | On `AMBIGUOUS`: halt, surface top-K matches with scores, user disambiguates | No silent selection in ambiguity band | §11 #1 |
| FR-21 | 184 | New/refined archetypes NEVER auto-saved without user approval | Default behavior: "propose, await approval" | §11 #1, #11 |
| FR-22 | 185 | Archetypes SHALL be generic — no person/company/fund names in core fields | Static linter: `display_name`, `persona_description_template`, `stable_traits` MUST NOT mention any specific firm/person; `affiliation_keywords` is the ONE allowed exception | §11 #1, #9 |
| FR-23 | 186 | Archetype store portable: directory of YAML, no external deps | One file per archetype; no SQLite/proprietary index; README.md documents schema | §11 #1, #10 |
| FR-24 | 472 | Workers MUST NOT call Opus for per-source processing | Static check: budget allocator caps Opus token spend per worker at consolidation step ONLY | §11 #12 |
| FR-25 | 473 | Web searches MUST route through Tavily MCP when configured | Fallback to direct fetch only when Tavily unavailable or for sources Tavily can't reach | §11 #13 |
| FR-26 | 474 | Run summary MUST report token spend per model tier; target <15% Opus | Per-tier spend report visible to user | §11 #12 |

**Three new acceptance items not directly anchored to a numbered FR:**
- §11 #5 (line 520) — parallel-orchestration timing test (`3 × per_subject_minutes` ceiling). Operationalizes FR-3 but adds a quantitative ceiling not stated in FR-3's own row.
- §11 #14 (line 529) — two-layer store override semantics. Tests two-layer behavior described in §0/§3 framing but not encoded in any single FR.
- §11 #15 (line 530) — promotion-candidate listing in run summary. Tests UX behavior of the local→canonical promotion flow described in §0/§3 but not encoded in a numbered FR.

---

## 4. §12 Open Questions OQ-1..OQ-9 (verbatim, with v1 defaults)

**Source citation:** spec §12, lines 534-550.

§12 contains TWO resolved open questions retained for traceability (OQ-3, OQ-7) AND nine *open* questions numbered 1-9 in the spec source. The prompt asks for "OQ-1..OQ-9 verbatim with v1 defaults" — note that the spec's numbering 1-9 in the "Open" subsection is independent of the OQ-3/OQ-7 traceability labels. To avoid ambiguity, this section reproduces both subsections verbatim with line citations.

### 4a. Resolved (lines 537-538)

**OQ-3 Validator model selection** (line 537) — verbatim:
```text
~~OQ-3 Validator model selection.~~ Resolved: Validator uses the same model as production party-mode/business-panel usage; mirrors runtime conditions (§9.2).
```

**OQ-7 Archetype-store path convention** (line 538) — verbatim:
```text
~~OQ-7 Archetype-store path convention.~~ Resolved: two-layer store, canonical at `<skill_root>/personas/`, local at `./.claude/skills/sc-persona-research-protocol/personas/` (§0, §3).
```

### 4b. Open (lines 540-550) — numbered 1 through 9 in spec source

**Open #1 (line 542) Naming convention for modeled personas** — verbatim:
```text
1. **Naming convention for modeled personas.** Proposed: `<prefix>-<lastname>-mod` (e.g., `board-rosenthal-mod`). Alternative: `<prefix>-<firstname>-r` (cleaner but loses surname). Resolve before implementation.
```
**v1 default annotated by spec:** `<prefix>-<lastname>-mod` (proposed; alternative `<prefix>-<firstname>-r` rejected as "loses surname").

**Open #2 (line 543) PitchBook / Crunchbase API budget** — verbatim:
```text
2. **PitchBook / Crunchbase API budget.** Real deal-history needs paid sources. Skill needs a configurable "premium-source provider" interface or it will be limited to free-tier signal. Tavily covers a lot but not these.
```
**v1 default:** None stated. Spec flags scope limitation; configurable interface deferred.

**Open #3 (line 544) Multi-language posture** — verbatim:
```text
3. **Multi-language posture.** Some investors speak primarily in non-English channels (esp. the China-side counterparts). v1 = English-only; flag in scope.
```
**v1 default:** English-only; flag in scope.

**Open #4 (line 545) Archetype matching algorithm** — verbatim:
```text
4. **Archetype matching algorithm.** §F proposes a weighted keyword-overlap scorer for v1 (deterministic, explainable). v2 candidates: embedding-based similarity, LLM-as-judge (Haiku tier per §9.2). Decide v1 algorithm with skill-creator.
```
**v1 default:** Weighted keyword-overlap scorer (per Appendix F).

**Open #5 (line 546) Archetype versioning conflict resolution** — verbatim:
```text
5. **Archetype versioning conflict resolution.** When two parallel runs propose conflicting refinements to the same archetype, what's the merge strategy? v1 proposal: serialize approvals (last-approver wins, prior version retained). v2 candidates: three-way merge tooling.
```
**v1 default:** Serialize approvals (last-approver wins, prior version retained).

**Open #6 (line 547) Bootstrap archetypes shipped in canonical `<skill_root>/personas/`** — verbatim:
```text
6. **Bootstrap archetypes shipped in canonical `<skill_root>/personas/`.** Should v1 ship with only `generic_public_figure`, or pre-author 3–4 common archetypes (`crypto_native_vc`, `gaming_specialist_vc`, `traditional_growth_vc`, `strategic_corporate_exec`)? Tradeoff: faster cold start vs forcing users to discover archetypes themselves (richer learning loop, better evidence for what the archetype should look like).
```
**v1 default:** Per the "Next Step" section (lines 987-991), spec recommends shipping FOUR baseline archetypes: `generic_public_figure.yaml`, `crypto_native_vc.yaml`, `gaming_specialist_vc.yaml`, `strategic_corporate_exec.yaml`. Note this differs from the OQ-6 question text which lists `traditional_growth_vc` instead of `strategic_corporate_exec` as one of the candidate four.

**Open #7 (line 548) Archetype deprecation** — verbatim:
```text
7. **Archetype deprecation.** When an archetype no longer matches anyone (e.g., the VC class it described has dissolved), how is it deprecated? v1: never auto-delete; flag at >50/100 archetypes; manual consolidation pass.
```
**v1 default:** Never auto-delete; flag warning at >50 archetypes, hard limit at 100; manual consolidation pass.

**Open #8 (line 549) Consumer-agnostic persona output format** — verbatim:
```text
8. **Consumer-agnostic persona output format.** Original use case targets BMAD `_bmad/custom/config.toml`. SC has its own `sc:business-panel` for similar roundtables. Should the persona-output stage be a pluggable "emitter" with adapters for `bmad-party-mode`, `sc:business-panel`, and a generic JSON for downstream consumers? v1 ships BMAD adapter; v2 adds others.
```
**v1 default:** Ship BMAD adapter only; v2 adds `sc:business-panel` and generic JSON.

**Open #9 (line 550) Tavily-MCP availability fallback** — verbatim:
```text
9. **Tavily-MCP availability fallback.** Per FR-25, fallback to direct fetch when Tavily is unavailable. What's the threshold for declaring "unavailable" — first 429, repeated 5xx, MCP disconnect? Define operational policy.
```
**v1 default:** Not stated; spec defers operational-policy decision.

---

## 5. Appendix E — Archetype YAML Schema (verbatim)

**Source citation:** spec Appendix E, lines 724-902.

The full schema (lines 728-891 — the YAML block) and schema notes (lines 893-900) reproduced verbatim:

````markdown
## Appendix E — Archetype Schema (the global-store file format)

One YAML file per archetype, lives at `<archetype_store.path>/<archetype_id>.yaml`. Versioned files retained as `<archetype_id>.v<N>.yaml`. The store directory also contains a `README.md` documenting the schema and a `_index.yaml` (auto-maintained) listing all archetypes for fast scoring.

```yaml
---
# ─── METADATA (required) ───
archetype_id: crypto_native_vc           # snake_case; unique; immutable after creation
display_name: Crypto-Native Venture Investor
schema_version: 1                        # of the archetype schema itself
archetype_version: 3                     # increments on refinement (FR-19)
created: 2026-04-29
last_refined: 2026-05-12
created_from_subject_count: 1
refined_from_subject_count: 4

# ─── IDENTITY SIGNALS (used by the matcher; see §F) ───
identity_signals:
  affiliation_keywords:                  # *example list* of firms in this archetype's class
    - polychain
    - paradigm
    - a16z crypto
    - variant
    - multicoin
    - dragonfly
  role_keywords:
    - partner
    - principal
    - general partner
    - gp
  domain_keywords:
    - crypto
    - web3
    - defi
    - token
    - blockchain
  required_signals: 2                    # min keyword categories that must hit for a candidate match
  negative_signals:                      # disqualifiers
    - state-affiliated
    - public-pension

# ─── SOURCE RECIPE (drives the per-subject worker; see §5.3) ───
source_recipe:
  tier_1_regulatory:
    - source: SEC_EDGAR
      query_template: "{firm_name} Form D"
      priority: high
    - source: SEC_EDGAR
      query_template: "{firm_name} Form ADV"
      priority: medium
  tier_2_deal_history:
    - source: RootData
      query_template: "investor:{firm_name}"
      priority: high
    - source: CryptoRank
      query_template: "{firm_name} portfolio"
      priority: high
    - source: Crunchbase
      query_template: "{firm_name}"
      priority: medium
  tier_3_onchain:
    - source: Nansen
      query_template: "entity:{firm_name}"
      priority: medium
  tier_4_longform:
    - source: Mirror
      query_template: "author:{mirror_handle} OR {firm_handle}"
      priority: high
    - source: firm_blog
      url_template: "{firm_blog_url}"
      priority: high
  tier_5_audio:
    - source: YouTube
      query_template: "{name} {firm_name}"
      priority: medium
    - source: Bankless_podcast
      query_template: "{name}"
      priority: high
    - source: Empire_podcast
      query_template: "{name}"
      priority: medium
  tier_6_social:
    - source: Farcaster
      query_template: "@{farcaster_handle}"
      priority: medium
    - source: X
      query_template: "@{x_handle}"
      priority: low
  tier_7_adjacency:
    - source: 3AC_bankruptcy_estate
      query_template: "{firm_name}"
      priority: high
    - source: portfolio_company_podcasts
      query_template: "{firm_name} board"
      priority: medium
  tier_8_press:
    - source: Decrypt
      query_template: "{name}"
      priority: medium
    - source: Blockworks
      query_template: "{name}"
      priority: high
    - source: The_Block
      query_template: "{name}"
      priority: medium
  tier_9_hostile:
    - source: Web3IsGoingJustGreat
      query_template: "{firm_name}"
      priority: low

# ─── SLOT SCHEMA (filled per subject at instantiation) ───
slot_schema:
  required:
    - { name: name, type: string, description: "Subject's full name" }
    - { name: firm_name, type: string, description: "Firm/fund name" }
    - { name: role, type: string, description: "Role at firm" }
  optional:
    - { name: firm_blog_url, type: url }
    - { name: firm_handle, type: string, description: "Firm's social handle" }
    - { name: mirror_handle, type: string }
    - { name: farcaster_handle, type: string }
    - { name: x_handle, type: string }
    - { name: linkedin_url, type: url }

# ─── PERSONA TEMPLATE (Tina/PersonaTwin-style two-tier conditioning) ───
persona_description_template: |
  Modeled on the public posture of {name}, {role} at {firm_name}.
  Captures observable patterns from public statements, conference appearances,
  and disclosed deal history; does not generate first-person quotes attributed
  to the real person. For internal pitch stress-testing only — not endorsed by,
  not affiliated with, and not a representation of the real individual's views.

  STABLE TRAITS (archetype: crypto_native_vc):
    - Reads pitches through token-economics lens: allocation %, vesting cliffs, unlock schedules
    - Treats founder credibility through a public-track-record lens (prior deals, prior token launches)
    - {custom_trait_1}                    # filled by worker from subject's evidence
    - {custom_trait_2}
    - {custom_trait_3}

  CONTEXT-SPECIFIC LENS:
    {context_overlay}                     # filled by worker from context_artifact

# ─── THREE-QUESTIONS TEMPLATE ───
three_questions_template:
  - "What's the token vs equity structure, and how do they interact in a downside scenario?"
  - "Who else is in the round, and what does the lead/follow signal say?"
  - "What's the realistic recovery path under each named exit destination?"

# ─── REFINEMENT LOG ───
refinement_log:
  - date: 2026-04-29
    archetype_version_after: 1
    subject_added: subject_001            # opaque ID; never the person's real name
    deltas:
      - "initial creation from discovery worker"
  - date: 2026-05-08
    archetype_version_after: 2
    subject_added: subject_002
    deltas:
      - "added 3AC_bankruptcy_estate to tier_7_adjacency"
      - "raised tier_4_longform Mirror priority from medium to high"
  - date: 2026-05-12
    archetype_version_after: 3
    subject_added: subject_004
    deltas:
      - "added negative_signal: state-affiliated"
      - "added optional slot: farcaster_handle"
```

### Schema notes

- `archetype_id` is **immutable** once created. Renames require deprecate-and-recreate.
- `archetype_version` increments on every refinement. Old versions retained as `<id>.v<N>.yaml` for rollback.
- `created_from_subject_count` and `refined_from_subject_count` are diagnostic only — the actual subjects are NOT stored in the archetype (privacy, FR-22 generic-purity).
- `refinement_log.subject_added` is an opaque local ID, not a real name.
- `slot_schema` follows JSON-Schema-lite semantics; unknown slots are warnings, not errors.
- Per FR-22, neither `display_name` nor `persona_description_template` nor `stable_traits` may name a real person/firm/fund. The `identity_signals.affiliation_keywords` field is the *only* place specific firm names appear, and they're framed as match examples, not as the archetype itself.
````

### Schema field inventory (organized for builder reference)

**METADATA block (lines 730-738):**
- `archetype_id` (string, snake_case, unique, immutable)
- `display_name` (string)
- `schema_version` (int)
- `archetype_version` (int; increments on refinement per FR-19)
- `created` (date)
- `last_refined` (date)
- `created_from_subject_count` (int; diagnostic)
- `refined_from_subject_count` (int; diagnostic)

**IDENTITY_SIGNALS block (lines 741-763) — used by §F matcher:**
- `affiliation_keywords` (list of strings; example list of firms; ONLY place firm names allowed per FR-22)
- `role_keywords` (list of strings)
- `domain_keywords` (list of strings)
- `required_signals` (int; min keyword categories that must hit)
- `negative_signals` (list of strings; disqualifiers)

**SOURCE_RECIPE block (lines 766-832) — drives per-subject worker per §5.3:**
- 9 tiers (`tier_1_regulatory` through `tier_9_hostile`)
- Each tier: list of `{ source, query_template OR url_template, priority }`
- `priority` ∈ {high, medium, low}

**SLOT_SCHEMA block (lines 835-846) — JSON-Schema-lite:**
- `required` list (default: name, firm_name, role)
- `optional` list (default: firm_blog_url, firm_handle, mirror_handle, farcaster_handle, x_handle, linkedin_url)
- Each slot: `{ name, type, description? }` where type ∈ {string, url}

**PERSONA_DESCRIPTION_TEMPLATE block (lines 849-864):**
- YAML literal block scalar (`|`)
- Contains the §10.1-style disclaimer at top
- "STABLE TRAITS" section with 2 archetype-fixed bullets + 3 worker-filled `{custom_trait_N}` bullets
- "CONTEXT-SPECIFIC LENS" section with one `{context_overlay}` placeholder

**THREE_QUESTIONS_TEMPLATE block (lines 867-870):**
- List of 3 strings (questions)

**REFINEMENT_LOG block (lines 873-890):**
- List of `{ date, archetype_version_after, subject_added (opaque ID), deltas (list of strings) }`

---

## 6. Appendix F — Matching Algorithm (verbatim)

**Source citation:** spec Appendix F, lines 904-967.

````markdown
## Appendix F — Archetype Matching Algorithm (v1)

Deterministic, explainable, no embeddings required.

### Inputs
- Subject: `{ name, affiliation, role, domain_inferred_from_affiliation }`
- Archetype store: list of `archetype.yaml` files

### Score per archetype

For each archetype A:

```
score(A) =
    w_aff * (matched_affiliation_keywords / required_signals)
  + w_role * (matched_role_keywords / required_signals)
  + w_dom * (matched_domain_keywords / required_signals)
  - w_neg * (matched_negative_signals)

clamp to [0, 1]
```

Default weights: `w_aff=0.5, w_role=0.2, w_dom=0.3, w_neg=0.4`.

### Decision
1. Compute score for every archetype in the store.
2. Let `top1`, `top2` be the two highest scores.
3. If `top1 >= match_threshold` AND `(top1 - top2) >= ambiguity_band` → **`MATCH(top1.archetype_id)`**
4. Else if `top1 >= match_threshold` AND `(top1 - top2) < ambiguity_band` → **`AMBIGUOUS([top1, top2, ...])`** → halt for user input
5. Else → **`NO_MATCH`** → route to discovery worker

### Examples

**Subject:** `{ name: "Josh Rosenthal", affiliation: "Polychain Capital", role: "Partner" }`

Score against `crypto_native_vc`:
- `polychain` matches affiliation_keywords (1 hit / 2 required = 0.5) → +0.25
- `partner` matches role_keywords → +0.10
- `crypto` inferred from "Polychain Capital" matches domain_keywords → +0.15
- No negative signals
- **Score: 0.50**

Score against `traditional_growth_vc`:
- `partner` matches role_keywords → +0.10
- No other matches
- **Score: 0.10**

Top1 = 0.50, Top2 = 0.10. Threshold 0.7 → **`NO_MATCH`** → routes to discovery worker.

(After discovery + refinement adds Polychain to `crypto_native_vc.identity_signals.affiliation_keywords`, the next Polychain partner would score ~0.85 → `MATCH`.)

### Why deterministic v1

- Auditable: every match score is explainable as keyword hits × weights
- Reproducible: same store + same subject = same score, always
- No model-version drift on matching
- Easy to red-team: adversarial subject inputs produce predictable scores

### v2 candidates (deferred — see §12 OQ-5)

- Embedding-based similarity over a richer subject description
- LLM-as-judge: ask a subagent to choose the best archetype with rationale
- Hybrid: keyword score as a fast filter, then LLM tiebreak in the ambiguity band
````

### Algorithm extracted parameters (for builder reference)

- **Default weights:** `w_aff=0.5, w_role=0.2, w_dom=0.3, w_neg=0.4` (line 926)
- **`match_threshold`:** `0.7` per the example (line 951)
- **`ambiguity_band`:** unspecified default; referenced symbolically (lines 931-932 and 600). Spec leaves this as a tunable.
- **Per-archetype `required_signals`:** set inside each archetype YAML (default 2 in the example archetype, line 760).
- **Decision sentinels:** `MATCH(<archetype_id>)`, `AMBIGUOUS([list])`, `NO_MATCH`, plus `MATCH(forced)` from Guard G4 sentinel (line 601) when `archetype_hint` is provided.

---

## 7. Cross-Slice References

The §10/§11/§12 partition references functional requirements whose definitions live in §4 (Part 1, lines 164-186) and §9.2 (Part 2, lines 460-474), and validation/operational mechanics whose definitions live in §6 (Part 2, lines 360-385) and §8 (Part 2, lines 403-425). Catalog of every reference encountered in the assigned slice:

### §10 → other slices

| §10 line | References | Target slice | Note |
|----------|-----------|--------------|------|
| 497 | "FR-7 enforces this statically and dynamically" | §4 (Part 1, line 170) | Output-discipline → FR-7 quote-attribution rule |
| 499 | "(FR-9)" | §4 (Part 1, line 172) | Refusal of unsuitable subjects → FR-9 |

### §11 → other slices

| §11 line | References | Target slice | Note |
|----------|-----------|--------------|------|
| 516 | "FR-1 through FR-23 all pass (per-FR acceptance criteria above)" | §4 (Part 1, lines 164-186) | Bundles ALL Part 1 FRs by reference |
| 517 | "five Whittaker probes (§7)" | §7 (Part 2, lines 387-401) | Adversarial probes |
| 518 | "the mandatory disclaimer (§10.1)" | §10.1 (this slice, line 493) | Internal reference |
| 519 | "Validator achieves ≥7/10 fidelity" | FR-14 (Part 1, line 177) + §8 (Part 2) | Validator behavior |
| 520 | "Three-subjects-in-parallel test" | FR-3 (Part 1, line 166) | Parallel orchestration |
| 521 | "deceased-subject test fixture and a minor-subject test fixture" | FR-9 (Part 1) + §10.2 (this slice) | Refusal tests |
| 522 | "Quantity Flow Diagram and Guard Boundary Table" | App B (line 606) + App A (line 554) | Both in this slice — though App A is largely tied to FRs in §4 |
| 523 | "Archetype lifecycle test" | FR-16/17/18/19 (Part 1, lines 179-182) | Archetype FRs |
| 524 | "(FR-22)" | §4 (Part 1, line 185) | Generic-purity rule |
| 525 | "Archetype portability test" | FR-23 (Part 1, line 186) | Portability |
| 526 | "Approval-gate test" | FR-21 (Part 1, line 184) + FR-8 (line 171) | Approval gates |
| 527 | "Per FR-24/FR-26" | §9.2 (Part 2, lines 472, 474) | Model-tiering FRs |
| 528 | "Per FR-25" | §9.2 (Part 2, line 473) | Tavily routing |
| 529 | "Two-layer store test … `crypto_native_vc.v1` … `crypto_native_vc.v3`" | §0/§3 (Part 1) for two-layer-store framing; App E (this slice) for version semantics | Two-layer store |
| 530 | "Promotion-candidate test … stable >30 days, version >= 2" | §0/§3 (Part 1) | Promotion flow |

### §12 → other slices

| §12 line | References | Target slice | Note |
|----------|-----------|--------------|------|
| 537 | "(§9.2)" | §9.2 (Part 2) | Validator model tiering |
| 538 | "(§0, §3)" | §0/§3 (Part 1) | Two-layer store path convention |
| 545 | "§F proposes …" + "Haiku tier per §9.2" | App F (this slice) + §9.2 (Part 2) | Matching algorithm |
| 547 | reference to canonical `<skill_root>/personas/` | §0/§3 (Part 1) | Bootstrap archetypes |
| 550 | "Per FR-25" | §9.2 (Part 2, line 473) | Tavily fallback |

### Appendix E → other slices

| App E line | References | Target slice | Note |
|------------|-----------|--------------|------|
| 734 | "(FR-19)" comment on `archetype_version` | §4 (Part 1, line 182) | Version-bump trigger |
| 765 | "(see §5.3)" comment on `source_recipe` | §5 (Part 1, lines 190-358) | Recipe consumption by worker |
| 740 | "(used by the matcher; see §F)" comment on `identity_signals` | App F (this slice) | Matcher input |
| 897 | "(privacy, FR-22 generic-purity)" | §4 (Part 1, line 185) | No subjects stored in archetype |
| 900 | "Per FR-22, neither `display_name` nor … may name a real person/firm/fund" | §4 (Part 1, line 185) | FR-22 |

### Appendix F → other slices

| App F line | References | Target slice | Note |
|------------|-----------|--------------|------|
| 962 | "(deferred — see §12 OQ-5)" | §12 (this slice). NOTE: §12 has resolved OQ-3/OQ-7 plus open #1-#9; "OQ-5" here likely refers to open #5 versioning-conflict OR open #4 algorithm-v2; App F's "v2 candidates" align with open #4 content (embedding/LLM-as-judge), not open #5 (versioning conflict). See Internal Contradictions. |

---

## 8. Internal Contradictions (cross-slice and within-slice)

### 8a. Disclaimer text drift between §10.1 and Appendix E (within slice + cross-slice)

The §10.1 canonical disclaimer (line 493) and the Appendix E `persona_description_template` opening (lines 850-854) differ:

- **§10.1 (line 493):** Single line. "Modeled on the public posture of [Name, Affiliation]." (uses bracketed placeholder `[Name, Affiliation]`).
- **Appendix E (lines 850-854):** Multi-line block scalar. "Modeled on the public posture of {name}, {role} at {firm_name}." (uses YAML slot bindings `{name}`, `{role}`, `{firm_name}`).

**Implication for the verbatim-emission test (§11 #3, line 518):** The §11 acceptance criterion says "the mandatory disclaimer (§10.1) appears verbatim in every produced persona description" — but Appendix E's template would emit a slot-substituted version, not the literal `[Name, Affiliation]` bracketed string. The skill must either:
1. Substitute the slot bindings INTO the §10.1 string at runtime (replacing `[Name, Affiliation]` with the resolved name/affiliation) — matches the spirit of FR-6 ("verbatim").
2. Treat Appendix E's template as the canonical disclaimer for emission (richer slot binding) — diverges from §10.1 verbatim phrasing.

The spec does not resolve this. **Flag for skill-creator: which version is "verbatim"?**

### 8b. Number of unsuitable-subject categories: §10.2 vs FR-9

- **§10.2 line 499:** lists FOUR categories — "Deceased, minors, private individuals, witnesses in active litigation".
- **FR-9 line 172 (Part 1):** lists THREE — "deceased, minors, or non-public private individuals". OMITS witnesses in active litigation.

**Implication:** §11 #6 (line 521) tests only deceased-subject and minor-subject fixtures, not private-individual or witness-in-active-litigation. FR-9's per-row acceptance criterion does not require detection of witnesses-in-active-litigation. Either §10.2 over-specifies the policy floor or FR-9 under-specifies the implementation requirement.

### 8c. Acceptance-criterion count: prompt says "FR-1..FR-26 (26 rows)" but spec has 23 FRs in §4 + 3 in §9.2 = 26 total

Resolved by joining §4 FR table (FR-1..FR-23) with §9.2 hard rules (FR-24..FR-26). The mapping is internally consistent. The prompt's framing as "§11 26-row acceptance table" was misleading because §11 itself has only 15 numbered items (item 1 of which bundles FR-1..FR-23 by reference). Both views are reconciled in §3 of this report.

### 8d. Bootstrap archetype list mismatch: OQ-6 vs Next Step section

- **OQ-6 (line 547):** lists candidates `crypto_native_vc`, `gaming_specialist_vc`, `traditional_growth_vc`, `strategic_corporate_exec`.
- **Next Step (lines 988-991):** recommends `generic_public_figure`, `crypto_native_vc`, `gaming_specialist_vc`, `strategic_corporate_exec` — DROPS `traditional_growth_vc`, ADDS `generic_public_figure`.

**Implication:** Two different bootstrap-archetype slates. The skill-creator must pick one. Given the Next Step section is more recent/concrete and `generic_public_figure` is also referenced in the OQ-6 question text ("v1 ship with only `generic_public_figure`, or pre-author 3-4"), the Next Step list is the more authoritative.

### 8e. App F's reference to "OQ-5" is ambiguous

- **App F line 962:** "v2 candidates (deferred — see §12 OQ-5)".
- **§12 open #5 (line 546):** is about "Archetype versioning conflict resolution" (last-approver-wins merge strategy).
- **§12 open #4 (line 545):** is about "Archetype matching algorithm" v2 candidates (embedding-based similarity, LLM-as-judge).

App F's "v2 candidates" content (embeddings, LLM-as-judge, hybrid) maps to OPEN #4, not OPEN #5. App F appears to mis-cite. The skill-creator should treat the deferred-decision link as Open #4.

(Alternatively, if the "OQ-5" label in App F refers to the legacy open-question numbering BEFORE OQ-3 and OQ-7 were resolved, it is internally consistent — but the spec doesn't preserve a legacy numbering.)

### 8f. Resolved-OQ numbering vs Open-question numbering (within slice)

§12 retains "OQ-3" and "OQ-7" labels for resolved questions but renumbers the OPEN ones as 1-9. This means the label "OQ-5" can refer to either:
- A resolved question that was previously OQ-5 (if any — none stated, suggesting OQ-5 is "open #5 in current numbering")
- "Open #5" in the current spec — which is versioning conflict resolution, not the matching-algorithm v2 question App F seems to point at.

The numbering scheme is fragile. Recommend the skill-creator track open questions by their topic, not by ordinal number.

### 8g. Prompt-vs-actual line discrepancies (process note)

The prompt specified "investigation scope … lines 661-993". Actual content of those lines is:
- Lines 661-672 — tail of Appendix C (three-questions test template).
- Lines 676-693 — Appendix D worked example (NOT in the prompt's listed targets).
- Lines 696-720 — "Expert Panel Findings" section (NOT in the prompt's listed targets).
- Lines 724-902 — Appendix E (matches prompt).
- Lines 904-967 — Appendix F (matches prompt).
- Lines 970-993 — "Next Step" section (NOT in the prompt's listed targets but contains the bootstrap-archetype list referenced above).

The §10/§11/§12 sections the prompt named are at lines 487-553, OUTSIDE the prompt's stated 661-993 range. To fulfill the protocol I read those sections by name. Nothing was fabricated; every quoted line cites a real file:line.

### 8h. §11 #14 references archetype versions that don't exist in App E example

§11 #14 (line 529) constructs a test scenario where "Canonical store contains archetype `crypto_native_vc.v1`. Local store contains `crypto_native_vc.v3`." App E's example archetype IS at `archetype_version: 3` (line 734) but only example, not part of the canonical bootstrap. The bootstrap archetypes named in the Next Step section are not version-stamped — implies they ship at v1, which would make the §11 #14 test fixture buildable but requires the local store to have been refined twice (per the App E refinement_log lines 873-890). Not a contradiction — but a coupling between test fixtures and the example archetype that the builder should note.

### 8i. `match_threshold` and `ambiguity_band` are not given default values

App F mentions both parameters by name (lines 931-932) but only the example uses `0.7` for `match_threshold`. No spec line defines the default `ambiguity_band`. Guard G4 (line 600, App A) uses both names but does not define them either. **Flag for skill-creator: needs configurable defaults defined.**

---

## 9. Summary

This slice (assigned 661-993, but reading 487-553 + 724-967 + 970-993 to fulfill protocol) is the policy/acceptance/data-model spine of the spec. Key takeaways for the builder:

1. **Two verbatim-emission strings** the skill MUST byte-copy:
   - The §10.1 disclaimer (line 493) — anchored to FR-6.
   - The §10.3 attestation prompt (line 504) — anchored to `attestation_required: true` config flag.
   Both must appear in the generated SKILL.md's Critical Rules section AND in the §S25 Validation Checklist per `VALIDATION_REQUIREMENT ETHICS_DISCLAIMER_VERBATIM`.

2. **Four unsuitable-subject categories** (§10.2): deceased, minors, private individuals, witnesses in active litigation. FR-9 covers only the first three. Builder should follow §10.2 (the broader set) and either widen FR-9 or add an explicit refusal rule for the litigation case.

3. **§11 has 15 numbered acceptance items**, not 26 — but item 1 bundles FR-1..FR-23 by reference, and items 12-13 cover FR-24..FR-26. The functional FR-1..FR-26 mapping is reconstructable (see §3b above) but the skill-creator should NOT generate "26 §11 items" in the SKILL.md output; it should generate the 15 §11 items as written.

4. **§12 has 9 open questions plus 2 resolved**. The v1 defaults are explicit for OQ-1, OQ-3 (resolved), OQ-4, OQ-5, OQ-6 (with Next Step authoritative), OQ-7 (resolved), OQ-8. OQ-2 and OQ-9 lack v1 defaults and require skill-creator dialogue.

5. **Appendix E is the global-store file format** — eight top-level YAML blocks (metadata, identity_signals, source_recipe, slot_schema, persona_description_template, three_questions_template, refinement_log; schema_version is metadata too). FR-22 forbids person/firm/fund names in core fields; affiliation_keywords is the SOLE allowed exception.

6. **Appendix F is the deterministic v1 matcher** — weighted keyword overlap with default `w_aff=0.5, w_role=0.2, w_dom=0.3, w_neg=0.4`, `match_threshold=0.7` from example (no spec-stated default), `ambiguity_band` unspecified default. v2 candidates deferred per (mis-cited) §12 OQ-5 — actual referent is open #4.

7. **Cross-slice integration points** the builder must surface in the SKILL.md output:
   - §11 #1 → all of Part 1's FR table.
   - §11 #5 → §6 + §9 from Part 2.
   - §11 #12-#13 → §9.2 from Part 2.
   - §10 → FR-7 / FR-9 / FR-15 (Part 1).
   - App E → FR-19, FR-22, §5.3 from Part 1.
   - App F → §A guard G4 (Part 2), §9.2 (Part 2).

8. **Nine internal contradictions flagged** (§8 above). The most consequential for the skill-creator are:
   - 8a (disclaimer-text drift between §10.1 and App E)
   - 8b (refusal-category count mismatch)
   - 8d (bootstrap-archetype list mismatch)
   - 8i (missing default for `ambiguity_band`)
