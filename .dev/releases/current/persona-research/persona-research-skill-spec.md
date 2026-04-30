---
name: sc-persona-research-protocol
description: Research-driven persona builder for real public figures. Spawns parallel research agents per named person, compiles a public-surface dossier, extracts patterns, and produces BMAD-roster-ready persona descriptions calibrated against observable public posture. Modeled-on, never impersonating.
spec_type: skill-requirements
target_consumer: skill-creator
review_panel: [wiegers, adzic, cockburn, fowler, nygard, whittaker, newman, crispin, hightower]
review_mode: critique
created: 2026-04-29
status: draft-for-skill-creator
---

# Specification — `sc-persona-research-protocol`

## 0. Provenance & Background

Built from `/sc:spec-panel` review of a board-prep workflow. The triggering need: stress-test a board presentation (Neon Machine CEO transition) against the actual likely posture of three named investor-side decision-makers (Polychain partner, Griffin Gaming partner, Gala executive) by spawning each as a real-as-possible BMAD party-mode subagent.

A parallel deep-research agent confirmed that **no end-to-end open-source tool exists** for the "named real person → research → LLM persona" pipeline. The closest building blocks are `langchain-ai/people-researcher` (archived) for the research half and `microsoft/TinyTroupe` for the runtime half, but TinyTroupe is explicitly archetype-only and forbids real-person impersonation in its Responsible AI FAQ. This skill fills the gap, with TinyTroupe's ethics framing adopted as the floor.

### Where the skill lives (SuperClaude src/.claude pattern)

This skill is part of the SuperClaude framework and follows its source-of-truth convention from the global `CLAUDE.md`:

- **Canonical source:** `/config/workspace/IronClaude/src/superclaude/skills/sc-persona-research-protocol/`
- **Dev/runtime copy:** `.claude/skills/sc-persona-research-protocol/` (synced from `src/` via `make sync-dev`)

The skill carries a per-skill `personas/` subdirectory used as a **persistent archetype store** (see vocabulary note §5.5). Two layers:

| Layer | Path | Role | Writable by skill at runtime? |
|---|---|---|---|
| Canonical baseline | `<skill_root>/personas/` (in `src/superclaude/skills/...`, synced to `.claude/skills/...`) | Ships with the skill; bootstrap + promoted-archetypes-of-record | **No** — read-only |
| Working-project local store | `./.claude/skills/sc-persona-research-protocol/personas/` (in the current working project) | Where new archetypes accumulate from real research runs | **Yes** — runtime writes (with user approval) land here |

**Promotion workflow** (manual, deliberate): high-quality archetypes that have been validated across multiple subjects in a working project are **rolled back to `src/`** by the user — making them part of the skill's canonical baseline for future installs. The skill itself does not auto-promote; it surfaces promotion candidates in run summaries (§9).

This spec is the input to `skill-creator`, which is invoked from `/config/workspace/IronClaude` and writes the skill to the canonical `src/` path.

---

## 1. Purpose & Audience (Cockburn)

**Primary actor:** A user preparing a high-stakes communication (board pitch, investor update, customer call, regulatory hearing) who wants to stress-test their material against the likely viewpoints of named decision-makers.

**Goal:** Produce one or more BMAD-compatible persona descriptions (TOML-ready) for `_bmad/custom/config.toml`, each modeled on the public posture of a named real person, suitable for spawning in `bmad-party-mode` for adversarial roundtables.

**Success in the user's words:** "When I run party mode and the modeled persona spawns, it surfaces objections I wouldn't have anticipated, in language and framing consistent with how the real person speaks publicly — and I never see a fabricated quote attributed to them."

**Out of scope:** Replacing the real person's judgment, generating quotes attributed to them, or speaking on private matters. This is a stress-test instrument, not a digital twin.

---

## 2. User Stories (Cockburn / Adzic)

**US-1 — Single named person, no context.**
> As a board-prep user, I name **Josh Rosenthal at Polychain Capital** so that I get back an evidence dossier, a TOML-ready persona description, and a three-questions test I can use to validate fidelity.

**US-2 — Multiple named persons, in parallel, with context.**
> As a board-prep user, I name **three investors** and attach my draft deck, so that each persona is researched in parallel with the deck-context overlay folded into their description.

**US-3 — Audit trail.**
> As a governance-conscious user, I see every claim in the dossier sourced to a URL with retrieval date, so that I can defend the persona's grounding to an outside reviewer.

**US-4 — Halt on ambiguity.**
> As a user who provided an under-specified name, I'm asked to disambiguate before any research budget is spent, so that I don't get a confident persona of the wrong human.

**US-5 — Refuse on unsuitable subject.**
> As a user who accidentally named a private individual or deceased person, I'm refused with an explanation, so that I don't produce an inappropriate or legally exposed artifact.

**US-6 — Reuse archetype across subjects (the learning loop).**
> As a user researching my second crypto-VC partner, I get archetype matching against my prior runs so that the source recipe, slot schema, and stable-trait scaffolding for "crypto-native venture investor" is reused — and the per-subject worker focuses its budget on what's actually new about *this* subject.

**US-7 — Build a new archetype on a novel subject.**
> As a user researching the first member of a class I haven't researched before (e.g., a state-affiliated content-platform exec), I see the skill detect "no archetype matches" and propose a new archetype derived from this subject's research — which then becomes available for all future runs across all my projects.

**US-8 — Refine an existing archetype.**
> As a user whose archetype library has a `crypto_native_vc` archetype derived from one prior subject, when I research a second member of that class the skill folds the new evidence back into the archetype (new sources discovered, new stable-trait patterns) so the archetype gets sharper over time without me managing it.

---

## 3. Inputs & Outputs (Adzic — Specification by Example)

### Inputs

```yaml
subjects:                  # required, 1+ entries
  - name: "Josh Rosenthal"
    affiliation: "Polychain Capital"
    role: "Partner"        # optional but strongly recommended
    aliases: []            # optional disambiguation hints
    archetype_hint: null   # optional override: force a specific archetype_id
context_artifact: "@/path/to/deck.md"   # optional; folds project-specific overlay
output_target:
  dossier_dir: "_bmad-output/planning-artifacts/persona-research/"
  config_diff: "_bmad/custom/config.toml"   # PROPOSED diff; never auto-written
archetype_store:
  # Two-layer store. Both layers contain archetype YAML files with the same schema (§E).
  # Read order: local first, canonical fallback. Writes go to local only.
  canonical_path: "<skill_root>/personas/"               # baseline; ships with skill; READ-ONLY at runtime
  local_path: "./.claude/skills/sc-persona-research-protocol/personas/"   # working-project store; RUNTIME-WRITABLE
  merge_policy: "local_overrides_canonical"              # on archetype_id collision, local wins
  match_threshold: 0.7         # min similarity for archetype reuse
  ambiguity_band: 0.10         # if top-2 scores within this band → ask user
  refinement_mode: "auto"      # auto | propose | off — see §4 FR-19
  promotion_candidates: true   # if true, run summary surfaces archetypes ready for src/ promotion
naming:
  code_prefix: "board-"           # default
  archetype_companion: true        # also keep the original generic archetype, see §10
research_budget:
  per_subject_minutes: 12          # soft cap on research-agent runtime
  archetype_discovery_minutes: 18  # extra budget when no archetype matches (§4 FR-18)
ethics:
  attestation_required: true       # see §10
```

> **Note on source categories.** Source category coverage is no longer hardcoded as a flat list — it's read from the matched archetype's `source_recipe` field at runtime (§5.3). This is the central architectural shift in this revision of the spec.

### Outputs (per subject)

1. **Evidence dossier** — markdown, ~500 words, source-cited with retrieval date.
   `<dossier_dir>/<code>-dossier.md`
2. **Persona description** — TOML block, ready to paste into `[agents.<code>]`. Includes the modeled-on disclaimer (§10).
3. **Three-questions test** — three concrete questions the persona should ask any pitch in this domain. Used as the validation gate (§8).
4. **Aggregated proposed diff** — single unified diff against `_bmad/custom/config.toml` covering all subjects in this run. **Never auto-written.**
5. **Validation report** (if `--validate` passed) — for each persona, the spawned subagent's response to its own three-questions test, plus a fidelity score.

### Worked Example

**Input:**
```yaml
subjects:
  - { name: "Josh Rosenthal", affiliation: "Polychain Capital", role: "Partner" }
context_artifact: "@/config/workspace/shrapnel-gov/board-presentation-brief.md"
```

**Expected output sketch:**
```toml
[agents.board-rosenthal-mod]
module = "board"
team = "board-investor"
name = "Polly-R"
title = "Polychain-Modeled Investor"
icon = "🦅"
description = """
Modeled on the public posture of Josh Rosenthal, Partner at Polychain Capital.
Captures observable patterns from public statements, podcast appearances,
and disclosed deal history; does not generate first-person quotes attributed
to the real person. For internal pitch stress-testing only.

STABLE TRAITS (from research):
  [bullets derived from research]

CONTEXT-SPECIFIC LENS (Neon Machine board deck, 2026-04-29):
  [bullets derived from project overlay]
"""
```
Plus dossier file, three-questions file, and the proposed config.toml diff.

---

## 4. Functional Requirements (Wiegers)

| ID | Requirement | Acceptance Criteria |
|----|-------------|---------------------|
| **FR-1** | Skill SHALL accept 1–N subjects per invocation. | Reject `len(subjects) == 0` with a clear error; warn when N > 10. |
| **FR-2** | Skill SHALL run identity verification BEFORE deep research for every subject. | `identity_verified` must be `true` before the research subagent for that subject is spawned. See guard table §A. |
| **FR-3** | Skill SHALL spawn one research subagent per verified subject, in parallel. | Subagents launched in a single message; no sequential waiting between subjects. |
| **FR-4** | Each research subagent SHALL produce three artifacts: dossier, persona description, three-questions test. | Output validated against JSON schema in §5.2; missing fields = subject marked `INCOMPLETE` and surfaced in summary. |
| **FR-5** | Every claim in a dossier SHALL be source-cited with URL and retrieval date. | Reviewer can spot-check any claim by clicking through; no orphan claims allowed. |
| **FR-6** | Persona descriptions SHALL include the "modeled on" disclaimer verbatim (§10). | String-equality check before the description is written to disk. |
| **FR-7** | Persona descriptions SHALL NOT contain first-person quotes attributed to the real person. | Static check: no quoted strings preceded by `<Name> said` or `<Name>:` patterns. Dynamic check: validation pass §8. |
| **FR-8** | Skill SHALL produce a unified diff against `_bmad/custom/config.toml` but SHALL NOT auto-write it. | User must explicitly approve before any modification of the config file. |
| **FR-9** | Skill SHALL detect and refuse subjects who are deceased, minors, or non-public private individuals. | Identity verification step includes these checks; refuses with explanation. |
| **FR-10** | Skill SHALL halt on ambiguous identity (multiple plausible matches) and ask the user to disambiguate. | No silent disambiguation. |
| **FR-11** | When the public footprint is below the threshold (§A), skill SHALL return `INSUFFICIENT_PUBLIC_DATA` for that subject and SHALL NOT fabricate to fill the gap. | Sentinel return; surfaced in summary; user can choose to proceed with a thin persona or skip. |
| **FR-12** | Skill SHALL emit a Pipeline Quantity Flow Diagram (§B) showing how N input subjects became M output personas, with reasons for any divergence. | Always emitted, even when N == M. |
| **FR-13** | Skill SHALL cache dossiers by `{name|affiliation|isodate}` so re-runs within the same day reuse research. | TTL 24 hours, configurable. Invalidate on context_artifact change. |
| **FR-14** | When `--validate` passed, skill SHALL spawn each produced persona once with its own three-questions test and report fidelity. | Fidelity score 0–10; <7 marks the persona as `NEEDS_REFINEMENT` in the summary. |
| **FR-15** | Skill SHALL preserve the original generic archetype personas alongside named-modeled ones (default: `archetype_companion: true`). | Both `board-polly` (generic) and `board-rosenthal-mod` (named) coexist in the roster. |
| **FR-16** | Before any subject-specific research, skill SHALL resolve each subject against the global archetype store (`archetype_store.path`) and select the best-matching archetype, if any. | Match score computed per §F matching algorithm; result is one of `MATCH`, `AMBIGUOUS`, `NO_MATCH`. See guard G4 §A. |
| **FR-17** | When `MATCH`, skill SHALL load the matched archetype's `source_recipe`, `slot_schema`, `persona_description_template`, and `three_questions_template` and use them to drive the per-subject worker. | Worker invocation includes `archetype_id` field; worker output references it. |
| **FR-18** | When `NO_MATCH`, skill SHALL spawn a generic discovery worker (broader source sweep, longer budget per `archetype_discovery_minutes`) AND SHALL produce a proposed new archetype derived from that subject's research. | Discovery worker emits both: (a) a normal subject dossier, and (b) a proposed `archetype.yaml` for the global store. |
| **FR-19** | When `MATCH` and `refinement_mode == auto`, skill SHALL fold new evidence (newly discovered sources, newly observed stable-trait patterns) back into the matched archetype with a version bump. | Archetype version increments; `refinement_log` appended; old versions retained as `archetype_id.v<N>.yaml` for rollback. |
| **FR-20** | When `AMBIGUOUS`, skill SHALL halt and surface the top-K matching archetypes with their scores; user disambiguates. | No silent selection in the ambiguity band. |
| **FR-21** | New or refined archetypes SHALL NOT be auto-saved to the global store without user approval. | Saving is gated by an explicit user confirmation; default behavior is "propose, await approval." |
| **FR-22** | Archetypes SHALL be generic — they SHALL NOT contain person names, company names, or fund names in their core fields. Subject-specific bindings live exclusively in the slot schema's filled values at instantiation time. | Static check: archetype `identity_signals.affiliation_keywords` is allowed (it's an *example list* for matching), but archetype `display_name`, `persona_description_template`, and `stable_traits` MUST NOT mention any specific firm/person. Linter rule. |
| **FR-23** | The archetype store SHALL be portable: a single directory of YAML files with no external dependencies, importable/exportable across machines and shareable across users. | One file per archetype. No SQLite, no proprietary index. A README.md in the store directory documents the schema. |

---

## 5. Architecture & Orchestration (Fowler / Newman)

### 5.1 Component model

```
┌──────────────────────────────────────────────────────────────────────┐
│  sc-persona-research-protocol (orchestrator skill)                          │
│                                                                      │
│  ┌────────────────────┐                                              │
│  │ Identity Verifier  │  ← runs FIRST, sequentially per subject      │
│  └─────────┬──────────┘                                              │
│            ↓ verified subjects                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │ Archetype Manager  (NEW)                                       │  │
│  │  - reads two-layer store: local first, canonical fallback     │  │
│  │    local:     ./.claude/skills/.../personas/                   │  │
│  │    canonical: <skill_root>/personas/  (read-only baseline)     │  │
│  │  - per subject: scores match against every archetype           │  │
│  │  - returns: MATCH(archetype_id) | AMBIGUOUS | NO_MATCH         │  │
│  │  - on AMBIGUOUS → halt, ask user                               │  │
│  │  - on NO_MATCH → spawn discovery worker (next stage)           │  │
│  └─────────┬───────────────────────────────────────┬──────────────┘  │
│            ↓ MATCH path                            ↓ NO_MATCH path   │
│  ┌────────────────────────┐         ┌──────────────────────────────┐ │
│  │ Research Worker        │         │ Discovery Worker             │ │
│  │ (archetype-driven)     │         │ (generic broad sweep)        │ │
│  │  - uses archetype's    │         │  - emits subject dossier     │ │
│  │    source_recipe       │         │  - ALSO emits proposed       │ │
│  │  - fills slot_schema   │         │    archetype.yaml            │ │
│  │  - runs in parallel    │         │  - longer budget             │ │
│  │    with peers          │         │                              │ │
│  └─────────┬──────────────┘         └──────────────┬───────────────┘ │
│            ↓ dossier + slot bindings              ↓ dossier +        │
│            ↓                                       proposed archetype │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │ Aggregator                                                     │  │
│  │  - merges per-subject outputs                                  │  │
│  │  - emits Quantity Flow Diagram (now 2-tier: matched vs new)    │  │
│  │  - generates proposed config.toml diff                         │  │
│  │  - if refinement_mode==auto: prepares archetype version bumps  │  │
│  │  - assembles archetype-store proposed write set (FR-21)        │  │
│  └─────────┬──────────────────────────────────────────────────────┘  │
│            ↓                                                         │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │ Approval Gate (user-facing)                                    │  │
│  │  - shows: persona diffs + new/refined archetype proposals      │  │
│  │  - user approves each independently                            │  │
│  │  - approved archetypes written to global store                 │  │
│  │  - approved persona blocks written to local config.toml diff   │  │
│  └─────────┬──────────────────────────────────────────────────────┘  │
│            ↓ (if --validate)                                         │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │ Validator (spawns each persona, runs three-Qs test)            │  │
│  └────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

### 5.2 Worker contract (the strict interface)

Each research worker returns a single JSON object with this shape — non-conformance is a hard failure:

```json
{
  "subject_input": { "name": "...", "affiliation": "...", "role": "..." },
  "identity_verification": {
    "verified": true,
    "canonical_url": "https://...",
    "alternates_considered": ["..."]
  },
  "archetype_resolution": {
    "matched_archetype_id": "crypto_native_vc",
    "match_score": 0.82,
    "match_path": "MATCH | DISCOVERED | USER_FORCED",
    "alternates_considered": [
      { "id": "traditional_growth_vc", "score": 0.41 }
    ]
  },
  "slot_bindings": {
    "firm_name": "Polychain Capital",
    "firm_blog_url": "https://polychain.capital/blog",
    "mirror_handle": "@polychain",
    "...": "..."
  },
  "footprint_score": 0-10,
  "dossier_markdown": "...",
  "sources": [
    { "url": "...", "category": "deal_history|...", "retrieved": "2026-04-29", "claim_ids": ["C1","C2"], "from_archetype_recipe": true }
  ],
  "stable_traits": ["..."],
  "context_specific_lens": ["..."],
  "three_questions": ["...", "...", "..."],
  "persona_toml_block": "...",
  "archetype_refinement_proposal": {
    "applies_to_archetype_id": "crypto_native_vc",
    "deltas": [
      { "type": "add_source", "tier": "tier_5_adjacency", "value": "3AC_bankruptcy_estate_filings" },
      { "type": "add_stable_trait_pattern", "value": "..." }
    ]
  },
  "warnings": ["..."],
  "status": "OK|INCOMPLETE|INSUFFICIENT_PUBLIC_DATA|REFUSED"
}
```

When the worker is the **discovery worker** (NO_MATCH path), the contract additionally requires:

```json
{
  "discovered_archetype_proposal": {
    "archetype_id": "state_affiliated_content_platform_exec",
    "display_name": "State-Affiliated Content Platform Executive",
    "rationale": "Subject's role/affiliation/source-availability profile did not match any existing archetype. Proposed archetype derived from this subject's research; will become available for future runs across all projects after user approval.",
    "full_archetype_yaml": "..."   // see §E schema
  }
}
```

### 5.3 Source category coverage — archetype-driven

Source coverage is **no longer a fixed flat list**. Each archetype carries a `source_recipe` field (see §E schema) that names which sources to prioritize and in what order, with template variables filled from the subject's slot bindings. The worker reads the matched archetype's recipe and executes it.

The skill ships with a **bootstrap archetype** named `generic_public_figure` whose recipe covers the broadest 9-tier source catalog so a discovery worker has something to start from. After the first few runs across diverse subjects, the global store accumulates specialized archetypes (e.g., `crypto_native_vc`, `gaming_specialist_vc`, `strategic_corporate_exec`, `state_affiliated_executive`, `traditional_growth_vc`) that the matching algorithm chooses between.

The 9 source-category tiers an archetype recipe can reference:

1. **Regulatory & legal filings** (SEC EDGAR, PACER, state courts, bankruptcy estates, class actions)
2. **Deal-history databases** (Crunchbase, PitchBook, RootData, CryptoRank, Messari, Tracxn, Dealroom)
3. **On-chain forensics** (block explorers, Nansen, Arkham, wallet entity tags) — *typically only relevant for crypto archetypes*
4. **Long-form publications** (Substack, Mirror, Medium, fund-website memos) — *with personal vs firm-attributed split*
5. **Audio/video appearances** (YouTube, podcast circuit, conference archives)
6. **Real-time social** (Farcaster, X, Threads, Bluesky, LinkedIn engagement)
7. **Adjacency leakage** (portfolio-CEO podcasts, co-investor commentary, ex-partner interviews, LP-disclosure documents)
8. **Trade press** (per-domain: crypto, gaming, blockchain-gaming, traditional VC, enterprise SaaS, biotech, etc.)
9. **Hostile/adversarial coverage** (investigative journalism, bankruptcy filings naming the subject, class actions)

An archetype's `source_recipe` references these tiers selectively and weights them — e.g., `crypto_native_vc` weights tiers 3 and 4 (specifically Mirror) high; `gaming_specialist_vc` weights tier 8 (Naavik, GamesIndustry.biz) high and tier 3 to zero.

A worker MUST report per-tier coverage in the `sources` array with `from_archetype_recipe: true|false` so the Aggregator can detect when a worker discovered novel sources outside the matched archetype's recipe — these become candidate refinements (FR-19).

### 5.4 Service-boundary rules (Newman)

- Workers do not share state. Cross-subject inference happens only in the Aggregator.
- The orchestrator does not re-do worker reasoning; it consumes the JSON contract and surfaces it.
- The Validator is optional and idempotent. Re-running it on the same persona produces the same fidelity score (deterministic test set).
- The Archetype Manager is the **only** component that reads the canonical store. All other components read archetypes through the Manager's resolution output (the matched archetype, fully merged) — they never touch the store directly.

### 5.5 Vocabulary note — "personas" vs "archetypes"

The user-facing directory name is `personas/` (their preferred term). The technical schema (§E) is `archetype.yaml`. This is not a contradiction:

- **Archetype** (technical term in this spec) = the *generic, reusable template* — what's stored in `personas/`.
- **Persona** (user-facing term) = colloquially, both the archetype templates and the instantiated subject-specific outputs the skill produces.

The skill MUST treat the directory name as fixed (`personas/`) per user contract, but internally and in this spec the file format and matching algorithm refer to "archetypes" for precision. Documentation written for end-users should use "personas" consistently to avoid confusion.

### 5.6 Two-layer store merge & write rules

On startup, the Archetype Manager:
1. Enumerates all `*.yaml` files in `canonical_path` and loads them as the baseline set.
2. Enumerates all `*.yaml` files in `local_path` and loads them as the local set.
3. Builds the runtime archetype roster:
   - For each `archetype_id`, if both layers contain it: **local wins** per `merge_policy: local_overrides_canonical`.
   - Local-only archetypes are added to the roster.
   - Canonical-only archetypes are added to the roster.
4. The Manager surfaces in the run summary which archetypes came from which layer (and which were locally-overridden).

Writes — new archetypes from discovery workers, and refinements to matched archetypes — are written exclusively to `local_path`. The skill **never** writes to `canonical_path` at runtime. Promotion of local archetypes into canonical is a manual user action, out of scope for the skill but documented in §9.

---

## 6. Failure Modes (Nygard)

| Failure | Detection | Behavior |
|---------|-----------|----------|
| Identity ambiguous (multiple plausible humans) | Identity verifier finds >1 match above confidence threshold | Halt; ask user to disambiguate via aliases |
| Subject is deceased / minor / non-public | Identity verifier check | Refuse; explain |
| Subject has zero/near-zero public footprint | `footprint_score < 3` | Return `INSUFFICIENT_PUBLIC_DATA`; do not fabricate |
| Source paywall (PitchBook, Bloomberg) | HTTP 401/402 or known-paywall URL | Flag as gap in dossier; continue |
| Source rate-limit (Twitter, LinkedIn) | HTTP 429 | Backoff once; if persistent, mark category as "rate-limited"; continue |
| Network failure on a single source | Exception during fetch | Retry once; on second failure, mark source as `unavailable`; continue |
| Worker exceeds budget (`per_subject_minutes`) | Wall-clock > budget | Worker returns partial with `status: INCOMPLETE` and the warnings field populated |
| Aggregator gets back 0/N successful workers | All workers `INCOMPLETE`/`REFUSED` | Halt; surface per-subject reasons; do not emit a config diff |
| Context overflow on heavily documented subject | Worker exceeds context window | Worker returns tiered output: full source list + summary dossier + "deep dive available" marker |
| Cache hit on stale dossier | Dossier `> 90 days` old | Use cached but flag `STALE` in summary; recommend refresh |
| Canonical store missing | Skill not properly installed; `<skill_root>/personas/` absent | Hard error: skill installation is broken; refuse to run |
| Local store missing | First run in a working project | Auto-create `./.claude/skills/sc-persona-research-protocol/personas/` (empty); warn user; proceed using canonical only |
| Both stores empty | Fresh install with no canonical bootstrap shipped | Use built-in `generic_public_figure` defined in code (failsafe); warn user |
| Archetype store corruption (malformed YAML) | Schema validation fails on load | Skip the corrupt file, continue with remaining archetypes; surface as `STORE_INTEGRITY_WARNING` (note which layer) |
| Local-overrides-canonical with same `archetype_id` but divergent `archetype_version` | Local was forked from older canonical; canonical has since been updated upstream | Use local per merge_policy; surface as `STORE_DIVERGENCE_WARNING`; suggest user rebase local against new canonical |
| Two archetypes match in ambiguity band | Top-2 match scores within `ambiguity_band` of each other | Halt; show user both with scores; user picks or forces a third |
| Archetype matched but slot_schema has new required slots | Archetype version drift | Worker fills what it can; missing slots reported as `SLOT_GAPS` for archetype-refinement consideration |
| Refinement proposal contradicts archetype's existing stable traits | Aggregator detects conflict | Surface to user; do not auto-apply; offer manual reconciliation |
| Discovery worker proposes near-duplicate of existing archetype | New proposal's identity_signals overlap >0.85 with existing | Reject the new proposal; recommend refinement of the existing archetype instead |
| Archetype store grows unboundedly | >100 archetypes (operational concern) | Warn at 50, 100; recommend manual consolidation pass; never auto-delete |

---

## 7. Adversarial Probes (Whittaker)

Applied against the skill's own pipeline before shipping.

**FR-2.1 Zero/Empty Attack.** Subject with empty name, empty affiliation, zero sources returned, zero stable_traits extracted. Skill MUST NOT proceed past identity-verify with empty inputs; MUST NOT emit a persona with zero traits.

**FR-2.2 Divergence Attack.** Subject name resolves to two real public figures with overlapping affiliation history (e.g., "John Smith" who worked at both Goldman *and* Polychain). Identity verifier MUST surface both; orchestrator MUST halt.

**FR-2.3 Sentinel Collision Attack.** Subject whose entire public posture is "no comment" or who systematically declines to articulate views (e.g., a fund partner with a sealed-lips reputation). Worker MUST NOT confuse public silence with the user's `INSUFFICIENT_PUBLIC_DATA` sentinel; the dossier should explicitly note "deliberate public reticence" as a stable trait.

**FR-2.4 Sequence Attack.** Research worker runs before identity verification completes. MUST be impossible by construction — verify is a sequential blocker per FR-2.

**FR-2.5 Accumulation Attack.** Invocation with 50+ subjects. Skill SHOULD warn at N>10, hard-cap at N=25 unless `--force-large-batch` passed. Aggregator output for large batches MUST be paginated to avoid context overflow downstream.

---

## 8. Validation & Testing (Crispin)

### 8.1 Acceptance gate per persona — Three-Questions Test

For each produced persona, the worker writes three concrete questions the persona should ask any pitch in their domain. The Validator (when `--validate` is passed):
1. Spawns the persona as a subagent with no other context.
2. Presents it with the user's `context_artifact` (or a default board-pitch fixture).
3. Records the persona's first three questions.
4. Scores 0–10 on overlap with the worker-authored three-questions. Threshold: ≥7 = `OK`; <7 = `NEEDS_REFINEMENT`.

### 8.2 Cross-cohort consistency

Spawn the same persona against two different topics (the user's pitch + an unrelated control fixture). The persona's vocabulary, frameworks, and pet-issues should remain stable across topics. Drift signals an over-specified context overlay leaking into the stable traits.

### 8.3 Regression / reproducibility

Re-running the skill on the same subject within the cache TTL MUST return the same dossier and persona description (cache hit). Re-running after cache expiry MAY produce a new dossier; diff is reported in the summary.

### 8.4 Fabrication probe (the hard test)

Validator presents the persona with a leading question like "what did you say about X in 2024?" where X is something the dossier does NOT cover. A faithful persona responds with hedging or "I haven't taken a public position on that." A fabricating persona invents content — that's a failure.

---

## 9. Operational Concerns (Hightower)

- **Caching.** Per FR-13, dossiers cached at `<dossier_dir>/.cache/<sha>/`. SHA over `{name|affiliation|context_hash|isodate}`.
- **Source rate limits.** Worker MUST honor robots.txt; MUST backoff on 429; MUST NOT scrape behind paywalls.
- **Source freshness.** Dossiers older than 90 days flagged `STALE`. Consider auto-refresh on next invocation.
- **Observability.** Each invocation writes `<dossier_dir>/<isodate>-run-summary.json` capturing: subjects, footprint scores, source counts, validation results, total wall-clock, *model token spend per tier* (see §9.2), *promotion candidates* (see §9.1). Useful for "are my personas getting better over time."
- **Idempotency.** Re-running on the same inputs within cache TTL is a no-op (returns cached outputs). Useful for CI-style runs in long-running prep work.

### 9.1 Promotion workflow (local → canonical)

The skill does NOT auto-promote local archetypes into the canonical store. Promotion is a deliberate human action because canonical archetypes ship with the skill and affect every future install.

The skill DOES surface **promotion candidates** in the run summary when `promotion_candidates: true`:

> A local archetype is a promotion candidate when ALL of the following hold:
> 1. It has been refined from ≥3 distinct subjects (`refined_from_subject_count >= 3`)
> 2. It has been stable (no refinement deltas) for ≥30 days
> 3. Its `archetype_version` >= 2 (proves at least one refinement cycle happened)
> 4. No corresponding `archetype_id` exists in the canonical store, OR the local version is materially newer than canonical

When the user decides to promote, the workflow is the standard SuperClaude src/.claude pattern:
1. User copies the local archetype YAML from `./.claude/skills/sc-persona-research-protocol/personas/<id>.yaml` to `<IronClaude>/src/superclaude/skills/sc-persona-research-protocol/personas/<id>.yaml`
2. User runs `make sync-dev` (per global CLAUDE.md) so all `.claude/` install copies pick it up
3. User commits the change to the IronClaude repo
4. On next invocation in any project, the archetype is now resolved from canonical

The skill's run summary SHOULD print the suggested copy command for each candidate. It does not execute the copy.

### 9.2 Model selection & tool routing — tiered for cost/speed

Per user spec: small/fast model for volume work, Opus reserved for synthesis-heavy stages.

| Stage | Recommended model | Rationale |
|---|---|---|
| Identity Verification | `claude-haiku-4-5-20251001` (Haiku) | Single-shot disambiguation; cheap and fast |
| Archetype Manager (matching) | Deterministic Python (no LLM) | §F algorithm is keyword-weighted; no model call needed |
| Per-source web search & extraction | **Tavily MCP** (preferred) → results processed by `claude-haiku-4-5-20251001` (Haiku) | High-volume, parallel; per-source extraction is mechanical pattern-matching against the archetype's source recipe |
| Per-source fact extraction & dossier-fragment writing | `claude-haiku-4-5-20251001` (Haiku) | One Haiku call per source; runs in parallel within a worker |
| Discovery worker — broad sweep | `claude-haiku-4-5-20251001` (Haiku) | Same volume profile as archetype-driven worker, just wider |
| **Cross-source consolidation per subject** | `claude-opus-4-7` (Opus) | Synthesis across many Haiku-extracted fragments into a coherent dossier requires Opus reasoning |
| **Persona description generation** | `claude-opus-4-7` (Opus) | The "modeled on" persona description is the highest-stakes output; voice fidelity matters |
| **Archetype proposal / refinement synthesis** | `claude-opus-4-7` (Opus) | Inferring the right generic-template structure from a subject's research is synthesis work |
| Validator (three-questions test spawn) | Same model as production party-mode usage | Validator must mirror runtime conditions for fidelity score to be meaningful |

**Hard rules:**
- **FR-24:** Workers MUST NOT call Opus for per-source processing. Static check: budget allocator caps Opus token spend per worker at the consolidation step only.
- **FR-25:** Web searches MUST route through Tavily MCP when Tavily is configured. Fallback to direct fetch only when Tavily is unavailable or for sources Tavily can't reach (e.g., authenticated PACER queries, on-chain block explorers via their own APIs).
- **FR-26:** The run summary MUST report token spend per model tier so the user can see Opus is being reserved appropriately (target: <15% of total tokens spent on Opus).

**Tavily MCP usage pattern** (per worker):
1. For each source in the matched archetype's `source_recipe`, the worker constructs the query from the slot bindings (e.g., `tavily_search(query="Polychain Capital Form D site:sec.gov")`).
2. Tavily returns ranked results with snippets.
3. Haiku processes each result against an extraction template ("from this snippet, extract: deal date, amount, lead/follow signal, attributed quotes if any, source URL").
4. Extracted fragments accumulate per source category.
5. After all sources processed, **Opus** consolidates the per-source fragments into the dossier markdown, stable_traits list, and three_questions.

This separation means a typical 12-minute per-subject worker runs ~50–100 Haiku calls (Tavily + extraction) and 1–2 Opus calls (consolidation, persona description).

---

## 10. Ethics, Legal & Output Discipline

This is the policy layer the OSS research flagged as the unsolved problem. Adopting TinyTroupe's framing as the floor.

### 10.1 Mandatory disclaimer (verbatim, prepended to every persona description)

> *Modeled on the public posture of [Name, Affiliation]. Captures observable patterns from public statements, conference appearances, and disclosed deal history; does not generate first-person quotes attributed to the real person. For internal pitch stress-testing only — not endorsed by, not affiliated with, and not a representation of the real individual's views.*

### 10.2 Output discipline

- **No attributed novel quotes.** Persona speaks in patterns ("a partner with this profile would push back here"), never in invented direct speech ("Josh would say…"). FR-7 enforces this statically and dynamically.
- **No private-matter inference.** Persona may model professional posture only. Health, family, undisclosed personal views: out of bounds.
- **Refuse on unsuitable subjects.** Deceased, minors, private individuals, witnesses in active litigation: refuse (FR-9).

### 10.3 User attestation

When `attestation_required: true` (default), the skill SHALL prompt the user once per invocation:
> "These personas are for internal stress-testing of your own material. They will be labeled 'modeled on' the named individuals and will not generate quotes attributed to them. You will not present them externally as representations of the real person. Confirm to proceed."

### 10.4 Companion archetype default

`archetype_companion: true` keeps generic archetypes (e.g., the original `board-polly`) in the roster alongside the named-modeled persona. This gives users a clear escape hatch when they want to discuss patterns generically without invoking a real name.

---

## 11. Acceptance Criteria (Wiegers)

The skill is **DONE** when:

1. ✅ FR-1 through FR-23 all pass (per-FR acceptance criteria above).
2. ✅ All five Whittaker probes (§7) verified by red-team test cases in the skill's own test suite.
3. ✅ The mandatory disclaimer (§10.1) appears verbatim in every produced persona description.
4. ✅ Validator achieves ≥7/10 fidelity on a held-out test subject (e.g., a well-documented public figure not in the original use case).
5. ✅ Three-subjects-in-parallel test completes within `3 × per_subject_minutes` ceiling (proves parallel orchestration is real).
6. ✅ Skill refuses on a deceased-subject test fixture and a minor-subject test fixture.
7. ✅ Skill emits a non-empty Quantity Flow Diagram and Guard Boundary Table on every run.
8. ✅ **Archetype lifecycle test:** First-ever run on a novel subject produces both a dossier and a proposed archetype; second run on a matching subject reuses the archetype with refinement deltas; third run on the same subject is a cache hit.
9. ✅ **Archetype generic-purity test:** A linter check rejects any archetype containing person names, fund names, or company names in core fields (FR-22).
10. ✅ **Archetype portability test:** Copying the entire archetype-store directory to a fresh machine and running the skill there produces identical match scores against the same subjects (no hidden state).
11. ✅ **Approval-gate test:** Skill never modifies the local archetype store or the project's roster file without explicit user approval; canonical store is never written by the skill at runtime.
12. ✅ **Model-tiering test:** Per FR-24/FR-26, Opus token spend in a typical per-subject worker run is <15% of total tokens. Test fixture: research a moderately-documented subject end-to-end; assert the per-tier spend report.
13. ✅ **Tavily routing test:** Per FR-25, when Tavily MCP is configured, all general web searches route through Tavily. Test fixture: stub Tavily; assert worker invokes `tavily_search` rather than direct fetch for non-API sources.
14. ✅ **Two-layer store test:** Canonical store contains archetype `crypto_native_vc.v1`. Local store contains `crypto_native_vc.v3`. Match returns local v3; run summary notes the override.
15. ✅ **Promotion-candidate test:** Local archetype refined from 3 subjects, stable >30 days, version >= 2 — appears in run summary's promotion-candidates list with the suggested copy command.

---

## 12. Open Questions (defer to skill-creator dialogue)

### Resolved (kept for traceability)
- ~~**OQ-3 Validator model selection.**~~ Resolved: Validator uses the same model as production party-mode/business-panel usage; mirrors runtime conditions (§9.2).
- ~~**OQ-7 Archetype-store path convention.**~~ Resolved: two-layer store, canonical at `<skill_root>/personas/`, local at `./.claude/skills/sc-persona-research-protocol/personas/` (§0, §3).

### Open

1. **Naming convention for modeled personas.** Proposed: `<prefix>-<lastname>-mod` (e.g., `board-rosenthal-mod`). Alternative: `<prefix>-<firstname>-r` (cleaner but loses surname). Resolve before implementation.
2. **PitchBook / Crunchbase API budget.** Real deal-history needs paid sources. Skill needs a configurable "premium-source provider" interface or it will be limited to free-tier signal. Tavily covers a lot but not these.
3. **Multi-language posture.** Some investors speak primarily in non-English channels (esp. the China-side counterparts). v1 = English-only; flag in scope.
4. **Archetype matching algorithm.** §F proposes a weighted keyword-overlap scorer for v1 (deterministic, explainable). v2 candidates: embedding-based similarity, LLM-as-judge (Haiku tier per §9.2). Decide v1 algorithm with skill-creator.
5. **Archetype versioning conflict resolution.** When two parallel runs propose conflicting refinements to the same archetype, what's the merge strategy? v1 proposal: serialize approvals (last-approver wins, prior version retained). v2 candidates: three-way merge tooling.
6. **Bootstrap archetypes shipped in canonical `<skill_root>/personas/`.** Should v1 ship with only `generic_public_figure`, or pre-author 3–4 common archetypes (`crypto_native_vc`, `gaming_specialist_vc`, `traditional_growth_vc`, `strategic_corporate_exec`)? Tradeoff: faster cold start vs forcing users to discover archetypes themselves (richer learning loop, better evidence for what the archetype should look like).
7. **Archetype deprecation.** When an archetype no longer matches anyone (e.g., the VC class it described has dissolved), how is it deprecated? v1: never auto-delete; flag at >50/100 archetypes; manual consolidation pass.
8. **Consumer-agnostic persona output format.** Original use case targets BMAD `_bmad/custom/config.toml`. SC has its own `sc:business-panel` for similar roundtables. Should the persona-output stage be a pluggable "emitter" with adapters for `bmad-party-mode`, `sc:business-panel`, and a generic JSON for downstream consumers? v1 ships BMAD adapter; v2 adds others.
9. **Tavily-MCP availability fallback.** Per FR-25, fallback to direct fetch when Tavily is unavailable. What's the threshold for declaring "unavailable" — first 429, repeated 5xx, MCP disconnect? Define operational policy.

---

## Appendix A — Guard Condition Boundary Table

Per spec-panel methodology. Three guards drive correctness in this skill.

### Guard G1: `identity_verified`

| Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-----------------|----------------|--------------|--------------------|--------|
| Zero/Empty | `name=""` | `false` | Halt; error: "name required" | OK |
| One/Minimal | `name="John Smith"`, no affiliation | `false` (under-specified) | Halt; ask user for affiliation | OK |
| Typical | `name="Josh Rosenthal", affiliation="Polychain"` | `true` (single match) | Proceed to research worker | OK |
| Maximum/Overflow | Name matches 5+ public figures | `false` | Halt; ask user to disambiguate | OK |
| Sentinel Value Match | Name is a placeholder like "TBD" or "John Doe" | `false` | Refuse with explanation | OK |
| Legitimate Edge Case | Name with non-Latin characters | `true` if resolvable | Proceed; flag transliteration variants in dossier | OK |

### Guard G2: `subject_is_living_adult_public_figure`

| Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-----------------|----------------|--------------|--------------------|--------|
| Zero/Empty | (subsumed by G1) | n/a | n/a | OK |
| One/Minimal | Subject is a public figure (verified) | `true` | Proceed | OK |
| Typical | Public investor with conference talks | `true` | Proceed | OK |
| Maximum/Overflow | Subject is a head-of-state (extreme public profile) | `true`, but flag for elevated caution | Proceed; verbose disclaimer | OK |
| Sentinel Value Match | Subject is deceased | `false` | Refuse; explanation | OK |
| Legitimate Edge Case | Subject is a private individual recently named in news | `false` | Refuse; explain "private individual exception" | OK |

### Guard G3: `public_footprint_above_threshold`

| Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-----------------|----------------|--------------|--------------------|--------|
| Zero/Empty | `footprint_score == 0` | `false` | Return `INSUFFICIENT_PUBLIC_DATA`; do not fabricate | OK |
| One/Minimal | `footprint_score == 3` (minimum threshold) | `true` (just clears) | Proceed; flag thin dossier | OK |
| Typical | `footprint_score == 7` | `true` | Proceed normally | OK |
| Maximum/Overflow | `footprint_score == 10` (saturated) | `true` | Proceed; worker may need tiered output (Nygard §6) | OK |
| Sentinel Value Match | Subject's posture is deliberate public silence | `true` if score >= 3 from non-statement signal (deal history) | Proceed; mark "deliberate reticence" as a stable trait | OK |
| Legitimate Edge Case | Subject changed public posture recently (post-departure) | `true` | Proceed; flag temporal split in dossier | OK |

### Guard G4: `archetype_match_resolution`

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

## Appendix B — Pipeline Quantity Flow Diagram

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

## Appendix C — Three-Questions Test Template

Per persona, the worker writes three questions in this format:

```
Three-Questions Test for [Persona Code]
========================================

1. [Question]
   Why: [What this question reveals about the persona's worldview / area of focus]
   Source signal: [Which dossier evidence anchors this question]

2. [...]
3. [...]
```

When run by the Validator, a faithful persona spawns and (without seeing this test) asks questions whose Jaccard similarity with the test set is ≥0.5 over question keywords/concepts.

---

## Appendix D — Worked Example (preview, not the deliverable)

For the Neon Machine board-prep use case, expected first-run inputs:

```yaml
subjects:
  - { name: "Josh Rosenthal",   affiliation: "Polychain Capital",       role: "Partner" }
  - { name: "Pierre Planche",   affiliation: "Griffin Gaming Partners", role: "Partner" }
  - { name: "Thomas Larrison",  affiliation: "Gala",                    role: "Executive" }
context_artifact: "@/config/workspace/shrapnel-gov/board-presentation-brief.md"
```

Expected outputs:
- 3 dossier files in `_bmad-output/planning-artifacts/persona-research/`
- 3 persona TOML blocks
- 1 unified diff against `_bmad/custom/config.toml` adding `board-rosenthal-mod`, `board-planche-mod`, `board-larrison-mod` while preserving the generic archetypes (`board-polly`, `board-greta`)
- Validation report (if `--validate` passed) with three fidelity scores

---

## Expert Panel Findings (consolidated)

| Expert | Key concern | Where addressed |
|--------|-------------|-----------------|
| **Wiegers** | Acceptance criteria for "complete profile" must be measurable | §4 FR table, §11 acceptance criteria |
| **Adzic** | Concrete examples of input → output | §3 worked example, §D appendix |
| **Cockburn** | Primary actor and goal must be explicit | §1 purpose, §2 user stories |
| **Fowler** | Component model and worker contract | §5.1 architecture, §5.2 JSON contract |
| **Nygard** | Failure modes must be enumerated, not implied | §6 failure-mode table |
| **Whittaker** | All five attack methodologies probed against the pipeline | §7 adversarial probes |
| **Newman** | Service boundaries: workers don't share state | §5.4 boundary rules |
| **Crispin** | Validation strategy with measurable fidelity gate | §8 validation, three-questions test |
| **Hightower** | Operational concerns: cache, rate limits, observability | §9 operational concerns |

**Consensus points:**
1. Identity verification is a hard sequential gate — non-negotiable.
2. The "modeled on" disclaimer is the legal/ethical floor — non-negotiable.
3. Parallel research is the architectural payoff — non-negotiable.
4. Auto-write to `config.toml` is forbidden — user approval required for every diff.
5. Caching and freshness handling matter operationally even for a v1.

**Disagreement worth surfacing:**
- Crispin and Whittaker disagree on validation severity. Crispin: fidelity score <7 is `NEEDS_REFINEMENT` (recoverable). Whittaker: any fabrication detected (§8.4 hard test) is a `FAIL` regardless of fidelity score. **Resolution adopted in spec:** both rules apply — fidelity score is the soft gate, fabrication probe is the hard gate.

---

---

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

---

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

---

## Next Step

Invoke from `/config/workspace/IronClaude` (the SuperClaude source-of-truth working directory):

```
cd /config/workspace/IronClaude
/skill-creator @/config/workspace/shrapnel-gov/_bmad-output/planning-artifacts/persona-research-skill-spec.md
```

skill-creator will produce `SKILL.md` (29-section RF format) under `src/superclaude/skills/sc-persona-research-protocol/`, then `make sync-dev` propagates it to `.claude/skills/sc-persona-research-protocol/`.

Recommend pairing with `agent-creator` for **two** worker subagent definitions:
1. **Archetype-driven research worker** (consumes a matched archetype's `source_recipe`; uses Haiku for per-source extraction, Opus for consolidation)
2. **Discovery worker** (broad sweep + emits proposed archetype YAML; same model tiering)

The per-worker contract (§5.2) is stable enough that both workers can share a base agent definition with a `mode: archetype_driven | discovery` parameter.

**Bootstrap content to include in canonical `src/superclaude/skills/sc-persona-research-protocol/personas/`** (per §12 OQ-6, default to shipping a useful baseline):
- `generic_public_figure.yaml` (always)
- `crypto_native_vc.yaml` (covers Polychain-archetype board-prep work)
- `gaming_specialist_vc.yaml` (covers Griffin-archetype work)
- `strategic_corporate_exec.yaml` (covers Gala-archetype work)

These four archetypes give the skill a useful cold-start; subsequent runs grow the local store with anything novel.
