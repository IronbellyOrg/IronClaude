---
name: sc-persona-research-protocol
description: "Generate public-surface persona dossiers and BMAD-roster-ready TOML persona blocks for named real public figures, modeled on observable public posture only — no first-person attributed quotes, no impersonation. Pipeline: identity verification → archetype resolution → parallel research workers → aggregator → approval gate → optional validator. Use this skill when you need to stress-test pitch material against the likely posture of named investor-side decision-makers (e.g., crypto-VC partners, gaming-VC partners, strategic-corporate execs), build modeled board personas, or research a named public figure for board-prep workflows. Trigger on phrases like 'research a persona for [name]', 'build modeled persona for [name]', 'stress-test against [investor name]', 'persona dossier for [name] at [firm]', 'model board persona on [name]', '/sc:persona-research', or 'create personas for [list of names]'."
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Task, WebFetch, WebSearch]
---

# Persona Research Protocol

A skill for generating evidence-based, public-surface persona dossiers and BMAD-roster-ready TOML persona blocks for **named real public figures**, modeled on observable public posture only. This skill uses Rigorflow's MDTM task file system for persistent progress tracking — every phase and step is encoded as checklist items in a task file that survives context compression and session restarts.

**How it works:** The skill performs identity verification on the named subject(s) FIRST (a hard sequential gate — research workers do not start until identity is confirmed), then runs archetype resolution (matching the subject to a domain-specific archetype like crypto-VC, gaming-VC, or strategic-corporate-exec), then spawns parallel research workers (one archetype-driven per subject, plus optional discovery workers for off-archetype angles), then routes findings through an aggregator with adversarial probes, then halts at a mandatory approval gate before producing any persona TOML or dossier output, and finally — if the user approves — optionally runs a validator pass. The skill produces a public-surface dossier markdown file, optional BMAD-roster persona TOML blocks, an archetype YAML stub, and a run summary including the §B quantity-flow diagram and §A guard-condition boundary tables.

This skill operates strictly on the **public surface** — observable public posture from interviews, talks, blog posts, podcasts, public filings, and on-chain data. It does NOT impersonate, does NOT generate first-person attributed quotes, and does NOT proceed without identity verification + user approval at the gate. The §10 ethics disclaimer is mandatory and verbatim on every dossier produced.

## Why This Process Works

Persona research fails when it relies on first-person quote fabrication, identity confusion, archetype contamination, or auto-writing personas to configuration without user approval. This skill forces every claim through public-source verification — workers cite specific URLs, dates, and source types; the §5.2 worker JSON contract enforces structured output with provenance; the aggregator runs adversarial probes (would this still be true if the persona were anonymized? Would a different archetype fit better? Are any quotes verbatim from the subject?); the approval gate halts the pipeline before any persona writes; and the §10 ethics disclaimer accompanies every output.

The MDTM task file provides three critical guarantees:
1. **Progress survives context compression** — The task file on disk is the source of truth, not conversation context. Every completed step is a checked box that persists across sessions.
2. **No steps get skipped** — The task file encodes every phase and step as a mandatory checklist item. The execution loop processes items sequentially, never jumping ahead.
3. **Resumability** — On restart, the skill reads the task file, finds the first unchecked `- [ ]` item, and picks up exactly where it left off.

The pipeline structure (identity verification → archetype resolution → **parallel research workers** → aggregator with adversarial probes → **approval gate** → optional validator) prevents five common failure modes:
- **Fabricated first-person quotes** — Workers operate under the §5.2 JSON contract that disallows verbatim subject quotes; only paraphrase with source citation is permitted. The aggregator's adversarial probe explicitly searches for any first-person attributed text and fails the dossier if found (FR-7, NO_FIRST_PERSON_ATTRIBUTION).
- **Identity confusion** — The identity-verify-first sequential gate (FR-2, IDENTITY_VERIFIED_BEFORE_RESEARCH) confirms the subject's name + affiliation + public footprint before any research worker starts. Common-name disambiguation is required at this gate.
- **Insufficient public footprint** — Subjects with no public posture (private individuals, witnesses in active litigation, minors, or others enumerated in §10.2) trigger an unsuitable-subject refusal at the identity gate, NOT silent low-quality output.
- **Archetype contamination** — The §22 archetype generic purity linter (FR-22, ARCHETYPE_GENERIC_PURITY) ensures archetype YAML files contain ONLY generic posture descriptors, never subject-specific content. Subject-specific content lives in the dossier; archetype content lives in the YAML.
- **Auto-write of configuration without approval** — The skill HALTS at the approval gate before any persona TOML is written or any BMAD-roster file is modified. The user must explicitly approve before output writes. The §10 ethics disclaimer + the §A guard tables + the §B quantity-flow diagram are all rendered for user inspection at the gate.

The research artifacts persist in the task folder under `.dev/tasks/to-do/` so findings survive context compression, can be re-verified later, and feed directly into downstream BMAD-roster ingestion or future re-research.

### Variable Reference

Every invocation creates a self-contained folder. All paths below are relative to this folder:

```
TASK_ID:     TASK-PERSONARES-YYYYMMDD-HHMMSS
TASK_DIR:    .dev/tasks/to-do/${TASK_ID}/
TASK_FILE:   ${TASK_DIR}${TASK_ID}.md
RESEARCH:    ${TASK_DIR}research/        # per-subject worker output (one file per worker per subject)
SYNTHESIS:   ${TASK_DIR}synthesis/       # aggregator output (cross-subject findings, adversarial probes)
QA:          ${TASK_DIR}qa/              # in-phase QA reports (lens reports, fix cycles, verifications)
REVIEWS:     ${TASK_DIR}reviews/         # phase-gate QA reports
DOSSIERS:    ${TASK_DIR}dossiers/        # final public-surface dossier markdown per subject
PERSONAS:    ${TASK_DIR}personas/        # BMAD-roster-ready persona TOML blocks per subject (post-approval only)
ARCHETYPES:  ${TASK_DIR}archetype-proposals/      # archetype YAML stubs (generic posture only, no subject-specific content)
APPROVALS:   ${TASK_DIR}approvals/       # approval gate artifacts (rendered disclosures, user decisions)
```

The DOSSIERS, PERSONAS, ARCHETYPES, and APPROVALS subfolders are domain-specific to this skill and are created during Phase 1 setup alongside the standard RESEARCH/SYNTHESIS/QA/REVIEWS folders.

---

## Input

The skill consumes a structured YAML input with **seven top-level keys** (per spec §3, lines 80-156). The `subjects` key is mandatory; the other six have spec-defined defaults but should be passed explicitly when the user wants non-default behavior.

```yaml
# 1. subjects (REQUIRED — list of 1+ entries; rejected if empty per FR-1)
subjects:
  - name: "Josh Rosenthal"            # required string
    affiliation: "Polychain Capital"  # required string
    role: "Partner"                   # optional but strongly recommended
    aliases: []                       # optional disambiguation hints
    archetype_hint: null              # optional archetype_id override (Guard G4 sentinel → match_path: USER_FORCED)

# 2. context_artifact (OPTIONAL — path string, used by Validator for three-questions probe)
context_artifact: "@/path/to/pitch-deck.md"

# 3. output_target (REQUIRED — where dossiers and config diffs land)
output_target:
  dossier_dir: "_bmad-output/planning-artifacts/persona-research/"
  config_diff: "_bmad/custom/config.toml"   # PROPOSED diff; never auto-written (FR-8)

# 4. archetype_store (REQUIRED — two-layer store with merge policy)
archetype_store:
  canonical_path: "<skill_root>/personas/"                                    # READ-ONLY at runtime; skill never writes here
  local_path: "./.claude/skills/sc-persona-research-protocol/personas/"      # RUNTIME-WRITABLE; new + refined archetypes land here
  merge_policy: "local_overrides_canonical"
  match_threshold: 0.7                # min similarity for archetype reuse (Guard G4)
  ambiguity_band: 0.10                # if top-2 archetypes within band → halt with AMBIGUOUS
  refinement_mode: "auto"             # "auto" | "propose" | "off"
  promotion_candidates: true          # surface promotion candidates in run summary

# 5. naming (REQUIRED — code prefix and archetype companion behavior)
naming:
  code_prefix: "board-"               # used for `[agents.<code_prefix><id>]` in TOML
  archetype_companion: true           # also keep generic archetype alongside named persona (§10.4)

# 6. research_budget (REQUIRED — soft caps per subject and per discovery)
research_budget:
  per_subject_minutes: 12             # soft cap per subject; exceeding → status: INCOMPLETE
  archetype_discovery_minutes: 18     # extra budget when no archetype matches (FR-18)

# 7. ethics (REQUIRED — gates the entire pipeline)
ethics:
  attestation_required: true          # default true; user must confirm verbatim §10.3 prompt before any worker runs
```

**Hard input rules:**
- `subjects` empty → reject with clear error (FR-1).
- `subjects` length > 10 → warn; > 25 → hard-cap unless `--force-large-batch` (FR-2.5 / §7).
- `subjects[].name + affiliation` together must clear Guard G1 (`identity_verified == true`). A bare name without affiliation is under-specified and triggers a clarification halt.
- `archetype_hint` provided → bypasses scoring; matched archetype emits `match_path: "USER_FORCED"` and is flagged in the run summary.
- `ethics.attestation_required: true` (default) → the verbatim §10.3 attestation prompt is shown to the user once per invocation BEFORE any research worker spawns.

### Effective Prompt Examples

**Strong — full triple-subject board-prep request (canonical worked example, spec App D):**
> /sc:persona-research subjects: [{name: "Josh Rosenthal", affiliation: "Polychain Capital", role: "Partner"}, {name: "Pierre Planche", affiliation: "Griffin Gaming Partners", role: "Partner"}, {name: "Thomas Larrison", affiliation: "Gala", role: "Executive"}]. Use these to stress-test the Neon Machine board pitch deck at `_bmad-output/pitch/neon-machine-deck.md`. Output dossiers to `_bmad-output/planning-artifacts/persona-research/` and a proposed config.toml diff at `_bmad/custom/config.toml`. Apply default archetype store, code_prefix `board-`, and the standard 12-minute per-subject budget.

**Strong — single subject with archetype_hint forcing path:**
> Research a persona for Mary Meeker (BOND Capital, General Partner). Force archetype `crypto_native_vc` via archetype_hint to test off-archetype mismatch behavior. Context artifact: `@docs/pitch-decks/series-c-deck.md`. Output to `personas/mary-meeker-dossier.md`.

**Strong — model board persona on a strategic-corporate-exec for early-stage gaming pitch:**
> Build modeled persona for Robert Iger (The Walt Disney Company, former CEO) to stress-test our entertainment-IP licensing pitch. Single subject, default archetype store, 12-minute budget, attestation required. Output to `_bmad-output/planning-artifacts/persona-research/disney-exec-dossier.md` and emit a proposed roster diff.

**Strong — multi-subject crypto-VC cohort with archetype refinement:**
> Create personas for [Olaf Carlson-Wee at Polychain, Katie Haun at Haun Ventures, Garry Tan at YC]. We want to refine the `crypto_native_vc` archetype based on three real partners. Output dossiers and propose archetype refinement deltas. Use refinement_mode: auto.

**Weak — bare name without affiliation (will trigger clarification halt at Guard G1):**
> Research a persona for John Smith.

**Weak — unsuitable subject (will trigger §10.2 refusal at identity gate):**
> Build a modeled persona for Steve Jobs to stress-test our consumer-electronics pitch.
> *(Refused: subject is deceased per §10.2 / FR-9.)*

### What to Do If the Prompt Is Incomplete

If the user provides only a list of names without affiliation, an ambiguous subject identifier, or omits the ethics attestation context, **do NOT proceed immediately**. Ask the user to clarify using this template:

> I can build modeled personas for [subject list] for you. To make the pipeline pass identity verification (Guard G1) and the ethics gate (§10.3), can you help me with:
>
> 1. **Affiliation for each subject** — for each name, what firm, fund, or organization is the subject currently or most-recently affiliated with? (Required to disambiguate common names per FR-1 / FR-10. A bare name without affiliation cannot clear identity verification.)
> 2. **Role (strongly recommended)** — what role does the subject hold (Partner, Executive, Director)? Improves archetype match scoring.
> 3. **archetype_hint (optional override)** — if you already know the archetype this subject should be matched to (e.g., `crypto_native_vc`, `gaming_vc`, `strategic_corporate_exec`), pass it as `archetype_hint`. Otherwise the Archetype Manager will score against the existing store.
> 4. **Context artifact (optional)** — path to the pitch deck, board memo, or fixture you want the personas stress-tested against. Required only if you also want a Validator pass with three-questions probe.
> 5. **Ethics attestation** — `ethics.attestation_required: true` is the default. You will be prompted with the verbatim §10.3 attestation string before any research worker spawns. Confirm you understand these personas are for internal stress-testing only.

Proceed once items #1 and #5 are clearly answered. Items #2-4 improve quality but aren't blockers. **Reject the request immediately** if any subject is in an unsuitable category per §10.2 (deceased, minor, private individual, witness in active litigation) — explain the refusal, do NOT silently produce low-quality output.

---

## Depth Tiers

Select a tier based on subject count and budget. **Default to Standard** for typical board-prep cohorts (3-10 named subjects).

| Tier | When to Use | Subject Count | Per-Subject Budget | Archetype Behavior | Worker Mode |
|------|------------|---------------|---------------------|---------------------|-------------|
| **Quick** | Single subject or tight cohort with strong existing archetype match | 1–3 subjects | 12-min soft cap | Reuse matched archetype only; no discovery | 1 archetype-driven worker per subject; no discovery workers |
| **Standard** | Typical board-prep cohort spanning 1-2 archetypes | 4–10 subjects | 25-min soft cap (per_subject_minutes + buffer) | Reuse matched + propose refinement deltas | Parallel archetype-driven workers; discovery worker only on NO_MATCH |
| **Deep** | Cohort that spans new domains (gaming-VC, strategic-corp) where existing store is sparse | 10–25 subjects (hard-cap at 25 per FR-2.5) | 40-min soft cap (per_subject_minutes + archetype_discovery_minutes) | Full archetype discovery; new archetype proposals expected | Parallel archetype-driven + parallel discovery workers; archetype proposal stage active |

**Tier selection rules:**
- If unsure, pick Standard.
- If cohort > 10 subjects → warn user, default to Deep, hard-cap at 25 unless user passes `--force-large-batch`.
- If any subject in cohort returns NO_MATCH from Archetype Manager → escalate that subject to discovery worker (Deep behavior on a per-subject basis, even within a Quick/Standard run).
- Quick tier never includes a Validator pass; Standard runs Validator only when `--validate` is passed; Deep recommends Validator by default.

---

## Output Locations

All persistent artifacts go to the task folder `${TASK_DIR}` (see Variable Reference above) plus the user-specified `output_target.dossier_dir`. The skill never writes to the canonical archetype store at runtime — only to `local_path` and the task folder.

| Artifact | Location |
|----------|----------|
| **MDTM Task File** | `${TASK_DIR}TASK-PERSONARES-YYYYMMDD-HHMMSS.md` |
| Research notes | `${TASK_DIR}research/research-notes.md` |
| Per-subject worker output (one file per worker per subject) | `${TASK_DIR}research/[NN]-subject-<code>.md` |
| Aggregator synthesis (cross-subject findings + adversarial probes) | `${TASK_DIR}synthesis/synth-aggregator-report.md` |
| Quantity Flow Diagram (per FR-12, mandatory emission) | `${TASK_DIR}synthesis/quantity-flow-diagram.md` |
| Guard Boundary Tables (App A, mandatory emission) | `${TASK_DIR}synthesis/guard-boundary-tables.md` |
| Final dossier markdown (per subject, ~500 words, source-cited) | `${TASK_DIR}dossiers/<code>-dossier.md` (mirrored to user's `dossier_dir/<code>-dossier.md` post-approval) |
| BMAD-roster persona TOML block (per subject, post-approval only) | `${TASK_DIR}personas/<code>.toml` (staged in `output_target.config_diff` post-approval) |
| Archetype YAML stub (new from discovery, refinement deltas from match) | `${TASK_DIR}archetype-proposals/<archetype_id>.yaml` (mirrored to `archetype_store.local_path/<archetype_id>.yaml` post-approval; canonical_path NEVER written) |
| Proposed unified config.toml diff | `${TASK_DIR}approvals/proposed-config.toml.diff` (rendered for user inspection; NEVER auto-applied per FR-8) |
| §10.1 Ethics disclaimer attestation record | `${TASK_DIR}approvals/ethics-attestation.md` |
| Approval gate render (disclosures + decisions) | `${TASK_DIR}approvals/gate-render-[timestamp].md` |
| Validator fidelity report (optional, per FR-23 with `--validate`) | `${TASK_DIR}qa/validator-fidelity-report.md` |
| Phase-gate QA reports (Gates 1-3) | `${TASK_DIR}qa/qa-gate-[N]-report.md` |

**File numbering convention:** Per-subject research files use zero-padded sequential numbers (`01-`, `02-`, ...) keyed to subject input order. The dossier filename `<code>` is the `code_prefix + slug(subject.name)` — e.g., `board-josh-rosenthal-dossier.md`.

Check for existing task folders in `.dev/tasks/to-do/` before creating new ones — if prior persona research exists for the same subject roster (matching `TASK-PERSONARES-*/`), read it first and offer cache-hit reuse per FR-13 (90-day TTL with `STALE` flag).

---

## Execution Overview

The skill operates in two stages:

**Stage A — Scope Discovery & Task File Creation (before the task file exists):**
1. Parse the user's input YAML and triage (Scenario A vs B)
2. Perform scope discovery (depth adjusted by tier and archetype-store state)
3. Write scope discovery results to a structured research notes file
4. Review research sufficiency (mandatory gate)
5. Triage template selection
6. Spawn the task builder to create the MDTM task file
7. Verify the task file

**Stage B — Task File Execution (after the task file exists):**
8. Execute the seven-phase persona research pipeline using the READ → IDENTIFY → EXECUTE → UPDATE → REPEAT loop
9. Each checklist item is a self-contained prompt — no prior context needed

**The Stage B pipeline has seven phases** (per spec §5.1 architecture, lines 196-243; mapped to MDTM L-levels):

| Phase | Name | L-level | Concurrency | Purpose |
|-------|------|---------|-------------|---------|
| **Phase 1** | Preparation & Ethics Attestation | L0 (setup) | sequential | Create task folder, render verbatim §10.3 attestation, capture user confirmation |
| **Phase 2** | Identity Verification (HARD GATE) | L1 (discovery, but sequential per FR-2) | sequential per subject | Verify each subject clears Guards G1+G2+G3; halt on AMBIGUOUS, deceased, minor, private, or insufficient footprint |
| **Phase 3** | Archetype Resolution | L1 (matching) | parallel per subject | Score each verified subject against archetype store; route to MATCH (archetype-driven worker) or NO_MATCH (discovery worker); halt on AMBIGUOUS within ambiguity_band |
| **Phase 4** | Parallel Research Workers | L4 (parallel research) | parallel batch (FR-3) | Spawn one worker per verified subject in a single message; archetype-driven workers use matched recipe + Tavily + Haiku per-source; discovery workers do broad sweep with extra budget |
| **Phase 5** | Aggregation & Adversarial Probes | L2 (build-from-discovery) | sequential | Collect M worker outputs; run §7 adversarial probes; consolidate per-subject Opus call; emit unified config.toml diff + archetype proposals |
| **Phase 6** | Approval Gate (HARD HALT) | L0 (gate) | sequential | Render proposed diff + archetype proposals + Quantity Flow Diagram + Guard Boundary Tables + ethics disclaimer; halt for user decision; per FR-21, never auto-write |
| **Phase 7** | Optional Validator | L4 (parallel validation) | parallel per persona | Only if `--validate` passed: spawn each persona as subagent, run three-questions probe (§8), score 0-10; <7 → mark NEEDS_REFINEMENT |

**QA gate placement** (per RF 3-gate QA architecture):
- **Gate 1** (between Phase 4 and Phase 5): Worker output schema-conformance + ethics-disclaimer-verbatim check on each worker JSON output (§5.2 contract validation).
- **Gate 2** (between Phase 5 and Phase 6): Aggregator structural review — adversarial probes ran, no first-person quotes (FR-7 static check), archetype generic-purity linter on proposals (FR-22), Quantity Flow Diagram emitted with actual counts (FR-12).
- **Gate 3** (after Phase 6 approval, before any writes): Final byte-fidelity check on §10.1 disclaimer in every persona TOML block; verify only `local_path` writes (FR-21); verify config.toml diff is rendered, not applied (FR-8).

**Per FR-12 (mandatory emission):** Every run MUST emit the App B Quantity Flow Diagram with actual N → N' → P+Q → M → K counts populated, and the App A Guard Boundary Tables for each guard that fired. These appear in the run summary regardless of pipeline outcome (success, halt, refuse).

If a task file already exists for this subject roster (from a previous session), skip Stage A and resume Stage B from the first unchecked item.

---

## Stage A: Scope Discovery & Task File Creation

### A.1: Check for Existing Task File

Before creating a new task file, check if one already exists:

1. Look in `.dev/tasks/to-do/` for any `TASK-PERSONARES-*/` folder related to this subject roster
2. If found, read the task file inside it (`${TASK_DIR}TASK-PERSONARES-*.md`) and check for unchecked `- [ ]` items
3. If unchecked items exist → skip to Stage B (resume execution)
4. If all items are checked → inform user that the persona research run is already complete, offer to re-run, refresh stale dossiers (per FR-13 90-day TTL), or build on existing dossiers
5. Check for existing task folder matching `TASK-PERSONARES-*/` in `.dev/tasks/to-do/`:
   a. If `${TASK_DIR}research/research-notes.md` exists with `Status: Complete` → skip to A.5 (review sufficiency, then build task file)
   b. If `${TASK_DIR}research/research-notes.md` exists with `Status: In Progress` → read it, resume A.3 scope discovery from where it left off, then continue to A.4 to update the file
   c. If task folder exists but no `research-notes.md` → continue with A.3 but use the existing folder
6. If no task folder exists → continue with A.2

### A.2: Parse & Triage the Input

Break the user's persona research request into structured components:

- **SUBJECTS[]**: Parsed list of `{name, affiliation, role, aliases, archetype_hint}` per spec §3 input schema. Reject if empty (FR-1). Warn if > 10 (FR-2.5). Hard-cap at 25 unless `--force-large-batch`.
- **CONTEXT_ARTIFACT**: Optional path string (`@/path/to/file`) to the pitch deck or fixture the personas will be stress-tested against. Required only if `--validate` is passed.
- **OUTPUT_TARGET**: dossier_dir + config_diff paths. Defaults from spec §3 lines 93-94.
- **ARCHETYPE_STORE_STATE**: Snapshot of canonical_path + local_path archetype YAMLs at run start. Used by Phase 3 matching.
- **ETHICS_ATTESTATION_REQUIRED**: Default `true`. If true, the verbatim §10.3 attestation prompt must be rendered to the user BEFORE any Phase 4 worker spawns.
- **ARCHETYPE_HINT_FORCING**: Per-subject, the presence of `archetype_hint` is a Guard G4 sentinel that bypasses scoring and emits `match_path: USER_FORCED`. Flagged in run summary.
- **ROSTER_SLUG**: A kebab-case identifier for the task folder, derived from the subject roster (e.g., `board-prep-rosenthal-planche-larrison`, `single-mary-meeker`). Used in TASK_ID.

**Unsuitable-subject screening (mandatory before scope discovery proceeds):**

For each subject in the input list, run a fast initial screen against the §10.2 unsuitable-subject categories:
1. **Deceased** — if any subject is known-deceased (e.g., Steve Jobs, John McCain), refuse with an explanation citing §10.2 / FR-9. Do NOT silently produce low-quality output.
2. **Minors** — if any subject is under 18, refuse.
3. **Private individuals** — if a subject has no public posture (no public conference appearances, talks, blog posts, podcasts, public filings, on-chain history), refuse.
4. **Witnesses in active litigation** — if a subject is currently named as a witness in a pending case, refuse.

If even one subject in the input list falls into an unsuitable category, the ENTIRE invocation halts. The skill does NOT proceed with the remaining subjects. The user must remove the unsuitable subject from the list and re-invoke.

**Ethics attestation rendering (verbatim from spec §10.3):**

Before proceeding to A.3, render this attestation prompt to the user character-for-character:

```text
These personas are for internal stress-testing of your own material. They will be labeled 'modeled on' the named individuals and will not generate quotes attributed to them. You will not present them externally as representations of the real person. Confirm to proceed.
```

Capture the user's confirmation and write it to `${TASK_DIR}approvals/ethics-attestation.md` with timestamp. Do NOT proceed if the user declines.

**Triage into Scenario A or B:**

**Scenario A — Explicit request:** User provided most of: subjects with affiliations, output_target, optional context_artifact, archetype_hint where applicable.
Example: full triple-subject board-prep request from the worked example (Rosenthal/Planche/Larrison with affiliations and dossier_dir).
→ Scope discovery confirms archetype-store state, identifies which subjects will hit MATCH vs NO_MATCH. Lighter exploration.

**Scenario B — Vague request:** User provided subject names but few specifics.
Example: "Build personas for [list of names]" without affiliation or archetype hints.
→ Scope discovery does broader work: cross-checks affiliation candidates, surveys archetype store, identifies which subjects need discovery workers.

**Do NOT interrogate the user with a list of questions.** Proceed with what you have AFTER the unsuitable-subject screen and ethics attestation. Only ask the user (via `AskUserQuestion`) if there's a genuine ambiguity about **identity** (Guard G1 fail) or **archetype intent** (Guard G4 AMBIGUOUS) that cannot be inferred from the inputs.

### A.3: Perform Scope Discovery

Use Glob, Grep, and codebase-retrieval to map the archetype store and locate the subjects' public surface. This must happen BEFORE building the task file so the builder can enumerate specific worker assignments.

**Adjust depth by scenario and tier:**
- **Scenario A + Quick/Standard**: Focused discovery — enumerate canonical_path + local_path archetype YAMLs, run a fast match-score preview per subject, identify which subjects will need discovery workers.
- **Scenario B + Deep**: Broad discovery — enumerate archetype store, do a per-subject identity-footprint scan to estimate footprint_score, flag subjects with `footprint_score < 3` for INSUFFICIENT_PUBLIC_DATA per Guard G3.

Discover:
- All YAML files in `archetype_store.canonical_path` (READ-ONLY) and `archetype_store.local_path`
- Existing dossiers from prior runs (cache hit candidates per FR-13)
- Per-subject public footprint sketch (quick Tavily probe to estimate footprint_score)
- Source category coverage per subject (interviews, talks, blog posts, podcasts, public filings, on-chain data, mirror handles, conference appearances, deal history) — the 9-tier source catalog from spec §5.3
- Archetype match score preview per subject

Based on the discovery:
- Select tier (Quick / Standard / Deep — default: Standard for 4-10 subjects)
- Plan worker assignments — one archetype-driven worker per matched subject, one discovery worker per NO_MATCH subject
- Plan archetype proposals (which subjects will produce new archetype YAMLs)
- Determine the synthesis file mapping (per-subject worker output → aggregator → dossiers)

**Agent type roster** (six distinct agent types — use as the topic requires):

| Agent Type | Purpose | What the Agent Does | Spec Anchor |
|------------|---------|---------------------|-------------|
| **Identity Verifier** | Confirm subject identity before research | Resolve name + affiliation against public records; check Guards G1+G2+G3; halt on AMBIGUOUS/deceased/minor/private/insufficient | §5.1 L198-199; FR-2; FR-9; FR-10 |
| **Archetype-Driven Worker** | Research a verified subject using a matched archetype's recipe | Use matched archetype's `source_recipe` + Tavily + Haiku per-source; emit §5.2 worker JSON; one Opus call for cross-source consolidation | §5.1 L201; §5.2 worker contract; §9.2 model tiering; FR-3, FR-17, FR-24, FR-25 |
| **Discovery Worker** | Research a NO_MATCH subject and propose a new archetype | Broad sweep across all 9 source tiers; emit §5.2 worker JSON + `discovered_archetype_proposal` with full archetype YAML | §5.1 L202; §5.2 L294-305; FR-18 |
| **Aggregator** | Consolidate worker outputs into personas, diffs, archetype proposals | Cross-subject §7 adversarial probes; emit M persona blocks + 1 unified config.toml diff + K archetype proposals | §5.1 L210-218; §7 probes |
| **Archetype Matcher** | Resolve subject → archetype prior to research worker spawn | Deterministic Python tool (no LLM); enumerates canonical+local archetype YAMLs, computes keyword-weighted similarity, returns MATCH/NO_MATCH/USER_FORCED/AMBIGUOUS per Guard G4 | §9.2 row 2; §F matching algorithm; FR-16, FR-20 |
| **Validator** | Optional fidelity check via three-questions probe | Spawn each persona as subagent with no other context; present context_artifact; record first 3 questions; score 0-10 | §8.1; FR-14, FR-23 |

The **Approval Gate** is a phase boundary (Phase 6, HARD HALT), not a spawned agent — it is render-and-halt logic executed by the orchestrator, not via Task-tool subagent spawn.

**9-tier source catalog** (per spec §5.3, used by archetype-driven and discovery workers):

1. Public conference talks and panels
2. Recorded interviews and podcasts
3. Blog posts and Substack/Mirror/Medium long-form
4. Public filings (SEC, court records, regulatory disclosures)
5. On-chain activity (wallet history, governance votes, public smart-contract deployments)
6. Disclosed deal history (Crunchbase, PitchBook public profile, firm portfolio pages)
7. Social-media public posts (Twitter/X, LinkedIn — public only)
8. Press coverage (TechCrunch, The Information, Bloomberg public articles)
9. Firm/company official biographies and statements

**Worker service-boundary rule (§5.4):** Workers do NOT share state. Each worker reads only its input + the matched archetype YAML; it writes ONLY its §5.2 JSON output. Cross-subject reasoning happens in the Aggregator, never in workers.

Create the task folder: `.dev/tasks/to-do/TASK-PERSONARES-YYYYMMDD-HHMMSS/` with subfolders `research/`, `synthesis/`, `qa/`, `reviews/`, `dossiers/`, `personas/`, `archetype-proposals/`, `approvals/`.

**Optional — spawn rf-task-researcher for complex scope discovery:** If the cohort is large (>10 subjects) or the archetype store has many candidates needing match-score preview, spawn an `rf-task-researcher` subagent to write the per-subject footprint and archetype-match-preview to a research notes file.

### A.4: Write Research Notes File (MANDATORY)

Write the scope discovery results to a structured research notes file at `${TASK_DIR}research/research-notes.md`. This file is what the builder reads — NOT inline content in the BUILD_REQUEST.

The file MUST be organized into these mandatory categories (include all, mark as "N/A" if empty):

```markdown
# Research Notes: Persona Research — [ROSTER_SLUG]

**Date:** [today]
**Scenario:** [A or B]
**Depth Tier:** [Quick / Standard / Deep]
**Subject Count:** [N]

---

## SUBJECT_ROSTER
[All N subjects from input. Per-subject detail: name, affiliation, role, aliases, archetype_hint (if any). Cite the input YAML as source. Note any subjects flagged for unsuitable-subject screen — if any present, the run halts and this file should record the refusal.]

## ARCHETYPE_STORE_INVENTORY
[Snapshot of canonical_path + local_path archetype YAML files. For each: archetype_id, version, layer (canonical/local), display_name, applies_to summary. Note any STORE_DIVERGENCE_WARNING (canonical+local differ on same archetype_id). Note any STORE_INTEGRITY_WARNING (malformed YAML).]

## ARCHETYPE_RESOLUTION_STRATEGY
[For each subject, the planned match path: MATCH (with archetype_id), NO_MATCH (route to discovery), USER_FORCED (archetype_hint provided), or DEFER (Phase 3 will compute). Per-subject preview match score where possible. Identify subjects expected to produce archetype refinement deltas vs new archetype proposals.]

## ETHICS_ATTESTATION_PLAN
[Confirmation that the verbatim §10.3 attestation prompt will be rendered before Phase 4. Confirmation that §10.1 disclaimer will be byte-fidelity-checked into every persona TOML block. Note attestation_required: true (default) vs false (rare override). Record the unsuitable-subject screen result.]

## SOURCE_BUDGET_PLAN
[Per-subject budget allocation: per_subject_minutes (default 12), archetype_discovery_minutes (default 18, applied to discovery workers only). Total expected wall-clock ceiling per FR-3 (parallel: max(per-subject) not sum). Tavily routing assumption (FR-25). Opus token-spend cap target (<15% per FR-26).]

## RECOMMENDED_OUTPUTS
[Planned output files: per-subject worker JSON files in research/, aggregator synthesis file, Quantity Flow Diagram, Guard Boundary Tables, dossier markdown per subject, persona TOML block per subject, archetype YAML stubs, proposed config.toml diff, approval gate render. Full paths and purposes.]

## SUGGESTED_PHASES
[Planned 7-phase pipeline breakdown. Per-phase detail:
- Phase 1: setup steps and ethics attestation render
- Phase 2: per-subject identity verifier spawns (sequential)
- Phase 3: archetype resolution per subject (parallel matching)
- Phase 4: per-worker assignments — one item per worker (archetype-driven or discovery), output paths, embedded §5.2 JSON contract
- Phase 5: aggregator assignment with §7 adversarial probes list
- Phase 6: approval gate render + halt
- Phase 7: optional Validator if --validate]

## TEMPLATE_NOTES
[Notes about which MDTM template to use and why. Almost always Template 02 for persona-research because the pipeline involves discovery (Phase 3 archetype resolution), parallel agents (Phase 4 workers), aggregation (Phase 5), gates (Phase 6), and conditional flows (Phase 7 only if --validate).]

## AMBIGUITIES_FOR_USER
[Genuine ambiguities about identity (Guard G1 fail), archetype intent (Guard G4 AMBIGUOUS), or ethics that cannot be resolved from the inputs. If none, write "None — inputs are clear and all guards have a deterministic path."]
```

### A.5: Review Research Sufficiency (MANDATORY GATE)

**You MUST review the research notes before spawning the builder.** This is a quality gate — do NOT skip it.

Read `${TASK_DIR}research/research-notes.md` and evaluate:

1. Are all N subjects from the input listed in SUBJECT_ROSTER with affiliation and role?
2. Has the unsuitable-subject screen been performed and recorded? (If any subject is unsuitable, the run should already have halted.)
3. Is the archetype-resolution strategy per-subject specific enough for the builder to create one Phase 4 worker checklist item per subject?
4. Is the synthesis mapping clear (which worker outputs feed which dossier and persona block)?
5. Has the §10.3 ethics attestation been confirmed and recorded in `${TASK_DIR}approvals/ethics-attestation.md`?
6. Are there unresolved ambiguities (Guard G1 or G4) that would block the builder?
7. Is the source-budget plan consistent with the selected tier's per_subject_minutes ceiling?

**If sufficient** → proceed to A.6 (template triage).

**If insufficient** → either:
- Do additional scope discovery yourself and update the research notes file, OR
- Spawn an rf-task-researcher subagent with specific feedback about what's missing, then re-review

**Maximum 2 gap-fill rounds.** After 2 rounds, proceed with what's available and note remaining gaps in the AMBIGUITIES_FOR_USER section.

Do NOT proceed to the builder with incomplete research notes. The builder cannot explore the archetype store effectively — it relies on what you provide.

### A.6: Template Triage

Determine which MDTM template the task builder should use:

**Use Template 02 (Complex Task) when the work involves:**
- Discovery before building (investigating unknown areas)
- Parallel subagent spawning
- Multiple phases with different activities (research, synthesis, assembly)
- Review/validation steps
- Conditional flows based on findings

**Use Template 01 (Generic Task) when the work involves:**
- Simple, sequential file creation
- Straightforward execution with no discovery
- Single-pass operations

**For persona-research, the answer is almost always Template 02** — the skill inherently involves discovery (Phase 3 archetype resolution), parallel agents (Phase 4 workers), synthesis (Phase 5 aggregator), gates (Phase 6 approval), and conditional flows (Phase 7 optional Validator).

### A.7: Build the Task File

Spawn the `rf-task-builder` subagent. The builder reads the research notes file and the MDTM template, then creates the task file. It also reads the SKILL.md itself for phase requirements and agent prompt templates.

**BUILD_REQUEST format for the subagent prompt:**

```
BUILD_REQUEST:
==============
GOAL: Conduct a persona research run on the [N]-subject roster [ROSTER_SLUG] and produce M public-surface dossiers + M BMAD-roster-ready persona TOML blocks + 1 unified config.toml diff (PROPOSED, never auto-applied) + K archetype YAML proposals (new + refined). Render the §10.1 disclaimer verbatim in every persona description, the App B Quantity Flow Diagram with actual counts, and the App A Guard Boundary Tables. Halt at the Phase 6 Approval Gate before any writes.

WHY: [WHY — what the user is stress-testing (e.g., "the Neon Machine board pitch deck") and what the personas will be used for]

TEMPLATE: 02

DOCUMENTATION STALENESS WARNINGS:
[None expected for persona-research scope discovery; archetype store snapshot in research notes is current. Phase 3 will re-verify archetype YAMLs at runtime.]

TEMPLATE 02 PATTERN MAPPING FOR THIS SKILL:
- Phase 1 (Preparation & Ethics Attestation): L0 Setup — create task folders, render verbatim §10.3 attestation, capture user confirmation in approvals/ethics-attestation.md
- Phase 2 (Identity Verification): L1 Discovery, sequential per subject (HARD GATE per FR-2) — one Identity Verifier per subject; halt on AMBIGUOUS, deceased, minor, private, or footprint_score < 3
- Phase 3 (Archetype Resolution): L1 Matching, parallel per verified subject — score against archetype store; route to MATCH or NO_MATCH; halt on AMBIGUOUS within ambiguity_band
- Phase 4 (Parallel Research Workers): L4 Parallel Research, single-message spawn per FR-3 — one archetype-driven worker per MATCH subject + one discovery worker per NO_MATCH subject; each worker emits §5.2 JSON; Tavily-routed per FR-25; Haiku per-source + Opus per-consolidation per FR-24
- **Gate 1 (between Phase 4 and Phase 5):** Schema-conformance + ethics-disclaimer-verbatim check on every worker JSON output
- Phase 5 (Aggregation & Adversarial Probes): L2 Build-from-Discovery, sequential — collect M outputs; run §7 probes (Zero/Empty, Divergence, Sentinel Collision, Sequence, Accumulation); emit M persona blocks + 1 config.toml diff + K archetype proposals; emit Quantity Flow Diagram + Guard Boundary Tables (FR-12 mandatory)
- **Gate 2 (between Phase 5 and Phase 6):** Adversarial probes ran, FR-7 no-quote static check, FR-22 archetype generic-purity linter, FR-12 emission verified
- Phase 6 (Approval Gate): L0 Gate, HARD HALT — render proposed diff + archetype proposals + Quantity Flow Diagram + Guard Boundary Tables + §10.1 disclaimer; halt for user decision; per FR-21, never auto-write
- **Gate 3 (after Phase 6 approval, before any writes):** Final byte-fidelity check on §10.1 disclaimer; verify only `local_path` writes; verify config.toml diff is rendered, not applied
- Phase 7 (Optional Validator): L4 Parallel Validation — only if --validate; spawn each persona as subagent; three-questions probe; score 0-10; <7 → NEEDS_REFINEMENT

RESEARCH NOTES FILE:
${TASK_DIR}research/research-notes.md
Read this file FIRST for full detailed findings including: SUBJECT_ROSTER, ARCHETYPE_STORE_INVENTORY, ARCHETYPE_RESOLUTION_STRATEGY, ETHICS_ATTESTATION_PLAN, SOURCE_BUDGET_PLAN, SUGGESTED_PHASES, and synthesis mapping.

SKILL CONTEXT FILE:
.claude/skills/sc-persona-research-protocol/SKILL.md
Read the "Agent Prompt Templates" section (S20) for: Identity Verifier prompt, Archetype-Driven Research Worker prompt (Tavily-routed, Haiku-per-source, Opus-per-consolidation), Discovery Worker prompt, Aggregator prompt with §7 adversarial probes list, Validator prompt with three-questions probe.
Read the "Output Structure" section (S21) for the per-subject artifact schema (dossier markdown + persona TOML + archetype YAML stub + config.toml diff fragment).
Read the "Synthesis Mapping Table" section (S22) for the worker-output → dossier + persona-block + archetype-proposal mapping.
Read the "Synthesis Quality Review Checklist" section (S23) for the post-aggregator checklist (disclaimer verbatim, no first-person quotes, source citations valid, archetype generic-purity).
Read the "Assembly Process" section (S24) for the Phase 5/6 assembly steps (Quantity Flow Diagram emission, config.toml diff generation, approval gate render).
Read the "Validation Checklist" section (S25) for Phase 6 + Gate 3 validation criteria including byte-fidelity check on §10.1 disclaimer.
Read the "Content Rules" (S26) and "Critical Rules" (S27) sections for non-negotiable writing standards (FR-7 no quotes, FR-6 disclaimer verbatim, FR-22 archetype generic-purity, FR-21 no auto-write, FR-24 Opus discipline, FR-25 Tavily routing).

WORKER JSON CONTRACT (§5.2 — strict output schema, non-conformance = hard failure):
Every Phase 4 worker checklist item MUST embed the full §5.2 JSON contract from S20. Required fields: subject_input, identity_verification (verified, canonical_url, alternates_considered), archetype_resolution (matched_archetype_id, match_score, match_path, alternates_considered), slot_bindings, footprint_score, dossier_markdown, sources[] (with category, retrieved date, claim_ids[]), stable_traits, context_specific_lens, three_questions, persona_toml_block, archetype_refinement_proposal, warnings[], status. Discovery workers ALSO emit discovered_archetype_proposal with full archetype YAML.

MODEL TIERING RULES (per FR-24/25/26 — embedded in every Phase 4 worker prompt):
- Workers MUST NOT call Opus for per-source processing (FR-24).
- Per-source web search routes through Tavily MCP when configured (FR-25).
- Per-source extraction uses Haiku (claude-haiku-4-5-20251001).
- Cross-source consolidation per subject uses Opus (claude-opus-4-7) — exactly one consolidation call per worker.
- Persona description generation uses Opus.
- Run summary MUST report token spend per model tier; target <15% Opus (FR-26).

ETHICS ATTESTATION GATE (Phase 1, mandatory before Phase 4):
The verbatim §10.3 attestation prompt MUST be rendered to the user character-for-character before any worker spawns. The user's confirmation is captured in approvals/ethics-attestation.md with timestamp. If the user declines, the run halts.

CRITICAL — GRANULARITY REQUIREMENT:
Per MDTM template rules A3 (Complete Granular Breakdown) and A4 (Iterative Process Structure), you MUST create individual checklist items for EVERY subject's identity verification, EVERY archetype resolution, EVERY worker spawn, EVERY synthesis step, and EVERY validation step. Do NOT create batch items like "verify all subjects" or "spawn all workers" — each subject gets its own checklist item per phase. The research notes SUGGESTED_PHASES section contains per-subject detail specifically to enable this granularity.

ESCALATION:
Since you are running as a subagent, return the task file path as your final output. Do NOT broadcast TASK_READY or use TaskCreate.

TASK FILE LOCATION: .dev/tasks/to-do/TASK-PERSONARES-YYYYMMDD-HHMMSS/TASK-PERSONARES-YYYYMMDD-HHMMSS.md

STEPS:
1. Read the research notes file specified above (MANDATORY)
2. Read the SKILL.md file specified above for agent prompts, JSON contract, validation checklist, and content rules (MANDATORY)
3. Read the MDTM template specified in TEMPLATE field above (MANDATORY): .claude/templates/workflow/02_mdtm_template_complex_task.md
4. Follow PART 1 instructions in the template completely (A3 granularity, B2 self-contained items, E1-E4 flat structure)
5. Encode the 7 phases with Gates 1, 2, 3 placed as specified above
6. If anything is missing, note it in the Task Log section — the skill will review
7. Create the task file at .dev/tasks/to-do/TASK-PERSONARES-YYYYMMDD-HHMMSS/TASK-PERSONARES-YYYYMMDD-HHMMSS.md using PART 2 structure
8. Return the task file path
```

**Spawning the builder:**

Use the Agent tool with `subagent_type: "rf-task-builder"` and `mode: "bypassPermissions"`. Pass the full BUILD_REQUEST as the prompt.

### A.8: Receive & Verify the Task File

The builder subagent returns the path to the created task file. Read the file and verify:
- Frontmatter is properly populated (`id`, `title`, `status`, `created`, `type`, `template`, `tracks`)
- All planned phases are present as checklist items (Phases 1-7 per the persona-research pipeline)
- Checklist items follow the B2 self-contained pattern (single paragraph: context + action + output + verification)
- No nested checkboxes, no standalone context-reading items
- Agent prompts are FULLY embedded in each subagent-spawning item (not references to "see above")
- Phase 1 includes the §10.3 ethics-attestation render step before any worker spawn (FR-2 sequencing)
- Phase 2 items are ordered for sequential per-subject identity verification (FR-2 hard gate)
- Phase 4 items embed the full §5.2 worker JSON contract verbatim per worker (Identity Verifier output, Archetype-Driven Worker output, Discovery Worker output) — no "see SKILL.md" references
- Phases 3, 4, and 7 items include explicit parallel spawning instructions (single-message multi-Agent calls)
- Phase 6 is a HARD HALT approval gate (renders Quantity Flow Diagram + Guard Boundary Tables + §10.1 disclaimer + proposed diff; never auto-writes)
- The §10.1 disclaimer string appears byte-verbatim where required (S25.1, S26.1, S27 Rule 23) and the verification checks reference S25.4 byte-fidelity spot checks

If the task file is malformed or missing critical elements, re-run the builder with specific corrections. Otherwise, proceed to Stage B.

---

## Stage B: Task File Execution

### Execution Loop (F1)

Execute the task file using the five-step execution pattern from the MDTM template (Section F1):

```
READ → IDENTIFY → EXECUTE → UPDATE → REPEAT
```

1. **READ**: Read the task file from disk (always — never work from memory of previous state)
2. **IDENTIFY**: Find the FIRST unchecked `- [ ]` item
3. **EXECUTE**: Complete ONLY that single identified item:
   - If the item says to spawn a subagent → use the Agent tool with the prompt embedded in the item
   - If the item says to read files and produce output → do it directly
   - If the item says to present to the user → output the required information
   - If the item says to update frontmatter → edit the task file's frontmatter
4. **UPDATE**: Mark ONLY that item as `- [x]` in the task file on disk
5. **REPEAT**: Return to step 1

### Prohibited Actions (F2)

These actions are NEVER permitted during task file execution:

- **Working from memory** — You MUST re-read the task file before each action. Never assume you know the current state.
- **Executing multiple items simultaneously** — One item at a time, marked complete before moving to the next. Exception: parallel agent spawning (see below).
- **Skipping items** — Items MUST be completed in exact sequential order. No reordering, no "I'll come back to this."
- **Assuming completion** — An item is only complete when you have evidence of completion (file written, output produced, command succeeded) AND have marked it `- [x]` on disk.
- **Modifying source code** — Persona research agents READ public sources, they do not modify production code. The skill produces dossiers, persona TOML blocks, and a proposed config diff — never auto-written.
- **Inventing file paths** — Only reference files you have verified exist via Glob/Read.

### Parallel Agent Spawning (MANDATORY for Phases 3, 4, 7)

When multiple consecutive items each spawn independent subagents, you MUST spawn them in parallel using multiple Agent tool calls in a single response. This applies to: Phase 4 archetype-driven research workers (one per subject, after identity verification has completed for all subjects), Phase 5 lens QA gates. This is not optional — it is how the skill achieves depth and minimizes wall-clock time.

Rules for parallel spawning:
1. Read the task file and find the first unchecked `- [ ]` item
2. Identify the **batch**: starting from that item, read forward through all consecutive unchecked items that are independent subagent spawns within the same phase. All of these form a single parallel batch.
3. Spawn ALL agents in the batch using parallel Agent tool calls in a single message
4. As each agent returns, mark its corresponding item `- [x]` immediately — do not wait for all to finish before checking any off. This ensures progress is captured even if the session ends mid-batch.
5. After ALL agents in the batch return, read the task file again before proceeding to the next phase

**Identity-first sequencing exception (FR-2):** Phase 2 Identity Verification runs sequentially per subject — research workers (Phase 4) MUST NOT spawn until identity verification has completed for ALL subjects. The "single message" parallel spawn rule (FR-3) applies WITHIN Phase 4 (workers fan out), not across the verification → research boundary.

**On resumption after a mid-batch failure:** If some items in a batch are `- [x]` and others are `- [ ]`, spawn only the unchecked ones. The checked agents' output files already exist on disk — do not re-run them.

### Task File Modification Restrictions (F4)

During execution, you MAY ONLY modify the task file to:
- Check off completed items (`- [ ]` → `- [x]`)
- Update frontmatter fields (status, updated_date, start_date, completion_date)
- Add entries to the Task Log / Notes section
- Add items within DYNAMIC CONTENT MARKER sections (if the template includes them)

You MUST NOT:
- Rewrite or rephrase existing checklist items
- Add new checklist items outside of DYNAMIC CONTENT MARKER sections
- Delete or reorder existing items
- Modify the Task Overview or Key Objectives sections

### Frontmatter Update Protocol (F5)

Update frontmatter at these specific points:

| Event | Fields to Update |
|-------|-----------------|
| **Task start** | `status: "🟠 Doing"`, `start_date: [today]`, `updated_date: [today]` |
| **After each work session** | `updated_date: [today]` |
| **Task blocked** | `status: "⚪ Blocked"`, `blocker_reason: [description]`, `updated_date: [today]` |
| **Task completion** | `status: "🟢 Done"`, `completion_date: [today]`, `updated_date: [today]` |

### Error Handling

If an item cannot be completed:
1. Log the blocker in the Task Log / Notes section with: timestamp, item reference, error description, attempted resolution
2. If the error is recoverable (e.g., agent returned partial results), complete what you can and note the gap
3. If the error is unrecoverable, mark the item `- [x]` with a note in Task Log, continue to next item
4. If ALL remaining items are blocked by the same issue (e.g., FR-10 ambiguous identity for all subjects, or §10.2 unsuitable-subject refusal), update frontmatter to "⚪ Blocked" with reason

### Session Resumption

If the session restarts or context compresses mid-execution:

1. Check `.dev/tasks/to-do/` for `TASK-PERSONARES-*/` folders related to the current subjects
2. Read the task file inside the folder (`${TASK_DIR}TASK-PERSONARES-*.md`)
3. Find the first unchecked `- [ ]` item
4. Resume the execution loop from that item
5. Do NOT re-execute any `- [x]` items — they are complete

The task folder `${TASK_DIR}` contains all intermediate artifacts in typed subfolders (`research/`, `qa/`, `dossiers/`, `archetype-proposals/`). Read existing research files to understand what has been completed before resuming.

---

## Agent Prompt Templates

These templates are provided to the task builder (in the BUILD_REQUEST) so it can embed them in the task file's self-contained checklist items. The builder MUST customize each instance with the specific subject(s), file paths, archetype_store paths, and ethics disclaimer. Workers do not share state (§5.4 service-boundary rule) — every input must be inlined into each prompt.

The agent prompts below are organized into three groups:

1. **Domain agent prompts (6)** — execute the persona-research pipeline (Identity Verifier, Archetype Matcher, Archetype-Driven Research Worker, Discovery Worker, Aggregator, Validator).
2. **Lens QA prompts (6)** — Phase 5 Gate 2 quality lenses (template-conformance, internal-consistency, evidence-quality, actionability, domain-accuracy, section-classification-accuracy).
3. **Source-fidelity prompts (3)** — Phase 5 Gate 2.5 fidelity audits (reference-skill semantic coverage, spec FR coverage, domain-noun leakage).

### Prompt: Identity Verifier (Domain Agent 1 of 6)

**subagent_type:** `rf-task-researcher`
**Sequencing:** Phase 2 — runs BEFORE any research worker spawns (FR-2 sequential gate). One Identity Verifier per subject; verifications run sequentially per subject (§5.1 component diagram L198-199).
**Model:** Haiku (`claude-haiku-4-5-20251001`) per §9.2 row 1 — single-shot disambiguation; cheap and fast.
**Input:** `subject = {name, affiliation, role, aliases}` from §3 input schema; `archetype_hint` (optional).
**Output path:** `${TASK_DIR}research/[NN]-identity-<subject_code>.md`

```
Verify the canonical public identity of the named subject and write findings to [output-path].

Subject: {name: "[name]", affiliation: "[affiliation]", role: "[role]", aliases: [list]}
Archetype hint (if forced): [archetype_hint or "none"]

Your job is to confirm — BEFORE any deep research begins — that this subject:
1. Is uniquely identifiable from public sources (not ambiguous with another person)
2. Is suitable for persona research per the ethics floor (§10.2): not deceased, not a minor, not a private individual, not an active witness in litigation
3. Has at least one canonical public URL (firm bio, fund page, official profile, verified social handle)

CRITICAL — Incremental File Writing Protocol:
You MUST follow this protocol exactly. Violation results in data loss.

1. FIRST ACTION: Create your output file immediately with this header:
   ```markdown
   # Identity Verification: [Subject Name]

   **Subject research type:** identity-verification
   **Status:** In Progress
   **Date:** [today]

   ---
   ```

2. As you investigate each disambiguation signal, IMMEDIATELY append your findings to the output file using Edit. Do NOT accumulate findings in your context window.

3. After each append, your output file grows. This is correct behavior. Never rewrite the file from scratch.

4. When finished, update the Status line from "In Progress" to "Complete" and append the identity_verification JSON block.

CRITICAL — Documentation Staleness Protocol:
Documentation describes intent or historical state. Public sources frequently lag the present (firm pages, LinkedIn bios, conference panel listings). For EVERY identity-disambiguation claim, mark it with one of:
- **[SPEC-VERIFIED]** — confirmed by at least 2 independent sources retrieved within the past 12 months
- **[SOURCE-CONTRADICTED]** — sources disagree on a key field (name spelling, current affiliation, role)
- **[UNVERIFIED]** — could not find corroborating source; treat as ambiguous

ADVERSARIAL STANCE:
Assume the name is ambiguous until proven otherwise. Search for at least 3 distinct people who could match the {name, affiliation} pair. If you find more than one plausible match in the same affiliation tier (e.g., two partners named "John Smith" at different funds), the verification FAILS with `verified: false` and the run HALTS per FR-10.

Output the identity_verification JSON block at the end of your file:

```json
{
  "verified": true | false,
  "canonical_url": "https://...",
  "alternates_considered": ["string", ...],
  "ethics_screen": {
    "deceased": false,
    "minor": false,
    "private_individual": false,
    "active_witness_in_litigation": false
  }
}
```

VERDICTS:
- PASS: `verified: true` AND ethics_screen all false → research worker may proceed
- FAIL — AMBIGUOUS: multiple candidates in tier; halt and surface to user (FR-10, FR-20)
- FAIL — UNSUITABLE: any ethics_screen field true; refuse per §10.2
- FAIL — INSUFFICIENT_PUBLIC_DATA: no canonical URL found; downstream worker emits `status: INSUFFICIENT_PUBLIC_DATA`

Be adversarial. Be specific. Verification is the FIRST gate — if you let through an ambiguous identity, the entire downstream pipeline is wrong.
```

### Prompt: Archetype Matcher (Domain Agent 2 of 6)

**subagent_type:** None — invoked as a deterministic Python tool, NOT via the Task tool.
**Per §9.2 row 2 (verbatim):** "Archetype Manager (matching) | Deterministic Python (no LLM) | §F algorithm is keyword-weighted; no model call needed." Per OQ-9 v1 default, no LLM is used at the matching step.
**Input:** Verified `subject` block, `slot_bindings` (firm_name, mirror_handle, etc. extracted by Identity Verifier output), `archetype_store.canonical_path`, `archetype_store.local_path`, `archetype_store.match_threshold` (default 0.7), `archetype_store.ambiguity_band` (default 0.10).
**Output:** Returns archetype_resolution JSON block to caller (Aggregator or task orchestrator). Does NOT write a research file.

```
TOOL CALL (deterministic Python — not an LLM agent):

Inputs:
- subject: {name, affiliation, role}
- slot_bindings: {firm_name, mirror_handle, fund_size, ...}
- archetype_store.canonical_path: <skill_root>/personas/  (READ-ONLY)
- archetype_store.local_path: ./.claude/skills/sc-persona-research-protocol/personas/  (RUNTIME-WRITABLE)
- match_threshold: 0.7
- ambiguity_band: 0.10
- archetype_hint: [optional override — forces match_path=USER_FORCED]

Algorithm (§F matching, summarized):
1. Enumerate all *.yaml in canonical_path and local_path
2. Apply local_overrides_canonical merge policy (§5.6)
3. For each archetype, compute keyword-weighted similarity score against subject's slot_bindings
4. Rank archetypes by score
5. Apply guard G4 sentinel logic:
   - archetype_hint set → MATCH(forced), match_path=USER_FORCED
   - top score < match_threshold → NO_MATCH (triggers Discovery Worker)
   - top-2 scores within ambiguity_band → AMBIGUOUS (HALT per FR-20)
   - top score ≥ match_threshold → MATCH, match_path=MATCH
   - store empty (first run) → NO_MATCH → bootstrap with `generic_public_figure` recipe

Output: archetype_resolution block (returned to caller, conforms to §5.2 worker contract):

  archetype_resolution.matched_archetype_id: string
  archetype_resolution.match_score: float
  archetype_resolution.match_path: enum: MATCH | DISCOVERED | USER_FORCED
  archetype_resolution.alternates_considered: list of {id, score}

NOTES:
- Per FR-22, the matched archetype's core fields (slot_taxonomy, decision_axes, persona_description_template, stable_traits) MUST remain GENERIC — no firm/person/fund names. Matcher returns the archetype as-is; the Worker fills slot_bindings with subject-specific values WITHOUT mutating the archetype.
- Per §5.4 service-boundary, the Matcher MUST NOT call any worker or LLM. It is a pure read-and-rank function.
```

### Prompt: Archetype-Driven Research Worker (Domain Agent 3 of 6)

**subagent_type:** `rf-task-researcher`
**Sequencing:** Phase 4 — spawned in parallel after ALL identity verifications complete and archetype matcher has returned a non-NO_MATCH path. One worker per subject. (FR-3 single-message parallel spawn.)
**Model tiering (§9.2, FR-24/25/26):** Haiku for per-source web search and extraction (Tavily-routed per FR-25); Opus reserved for cross-source consolidation, persona description generation, and archetype refinement synthesis. Static check: Opus token spend per worker capped at <15% of total tokens (FR-26 target / Acceptance #12 assertion threshold).
**Tavily routing (FR-25):** Web searches MUST route through Tavily MCP when configured. Fallback to direct fetch only when Tavily is unavailable or for sources Tavily can't reach (e.g., authenticated PACER queries, on-chain block explorers via their own APIs).
**Input:** Verified `subject`, matched archetype (`source_recipe`, `slot_schema`, `persona_description_template`, `three_questions_template`), `slot_bindings`, `research_budget.per_subject_minutes` (default 12), `${ETHICS_DISCLAIMER_VERBATIM}` (the §10.1 disclaimer string).
**Output path:** `${TASK_DIR}research/[NN]-subject-<subject_code>.md` containing the full §5.2 worker contract JSON block at the end.

```
Research the named subject using the matched archetype's source recipe and write a strict JSON dossier to [output-path].

Subject: {name, affiliation, role}
Matched archetype: {archetype_id, source_recipe, slot_schema, persona_description_template, three_questions_template}
slot_bindings (from Matcher): {firm_name, mirror_handle, ...}
Research budget: [per_subject_minutes] minutes (soft cap; tier output if exceeded)
Ethics disclaimer (verbatim, must appear in persona_toml_block):
[${ETHICS_DISCLAIMER_VERBATIM}]

CRITICAL — Incremental File Writing Protocol:
You MUST follow this protocol exactly. Violation results in data loss.

1. FIRST ACTION: Create your output file immediately with this header:
   ```markdown
   # Research: [Subject Name]

   **Subject research type:** archetype-driven-research-worker
   **Archetype:** [archetype_id]
   **Status:** In Progress
   **Date:** [today]

   ---
   ```

2. As you investigate each source from the archetype's source_recipe, IMMEDIATELY append your findings to the output file using Edit. Do NOT accumulate findings in your context window.

3. After each append, your output file grows. This is correct behavior. Never rewrite the file from scratch.

4. When finished, update the Status line from "In Progress" to "Complete" and append the §5.2 worker contract JSON block.

Research Protocol:
1. Walk the matched archetype's source_recipe (tier_1_regulatory → tier_2_deal_history → tier_3_thought_leadership → ... per §5.3 9-tier source catalog)
2. For each source category, route the search through Tavily MCP (FR-25). Fallback to direct fetch only on Tavily unavailability.
3. For each source result, run a Haiku extraction call (per §9.2 row 4): "from this snippet, extract: deal date, amount, lead/follow signal, attributed quotes if any, source URL"
4. Append each per-source fragment to the output file IMMEDIATELY (incremental writing)
5. After ALL sources processed, run ONE Opus call to consolidate fragments into: dossier_markdown, stable_traits list, three_questions
6. Run ONE Opus call to generate persona_toml_block (the "modeled on" persona description per §10.1; voice fidelity matters)
7. If the matched archetype's source_recipe could be improved by what you learned, propose deltas in archetype_refinement_proposal — but do NOT mutate the canonical archetype YAML.

CRITICAL — Documentation Staleness Protocol:
Documentation describes intent or historical state. Public sources frequently lag the present.
For EVERY claim sourced from a webpage, blog post, or doc, you MUST cross-validate:

1. Firm/role described in source: Verify the firm bio page, fund site, or official profile is current (retrieved within the past 12 months). If a doc says "Partner at [Firm X]" but the firm's About page lists someone else, the source is STALE.

2. Deal-history claims: A "led Series A in [Company]" claim must match at least 2 of: PitchBook entry, firm portfolio page, founder confirmation, press release. Single-source deal claims are STALE-PRONE.

3. Quotes: Per FR-7, the worker MUST NOT copy verbatim quotes longer than ~10 words from any source. Paraphrase always. Static check: dossier_markdown contains no `"..."` substrings exceeding 10 words.

4. Thesis statements: A "investment thesis" claim must trace to at least 2 sources (firm site + interview/podcast/blog). Single-source thesis statements are inferences, not facts.

For EVERY source-derived claim, mark it with one of:
- **[SPEC-VERIFIED]** — confirmed by 2+ independent sources retrieved within the past 12 months
- **[SOURCE-CONTRADICTED]** — sources disagree (describe the conflict)
- **[UNVERIFIED]** — only one source; flag as inferential

Claims marked [UNVERIFIED] or [SOURCE-CONTRADICTED] MUST appear in the warnings[] field.

ADVERSARIAL STANCE:
Assume the persona will be wrong until proven right by sources. The "modeled on" disclaimer is non-negotiable. Quotes are non-negotiable (no verbatim). Source citations are non-negotiable (every claim has a sources[] entry with a URL and retrieved date). If your footprint_score is below 5, the subject likely has insufficient public data — emit `status: INSUFFICIENT_PUBLIC_DATA` rather than fabricate.

Output the §5.2 worker contract JSON block at the end of your file:

```json
{
  "subject_input": {"name": "...", "affiliation": "...", "role": "..."},
  "identity_verification": {
    "verified": true,
    "canonical_url": "https://...",
    "alternates_considered": ["..."],
    "ethics_screen": {
      "deceased": false,
      "minor": false,
      "private_individual": false,
      "active_witness_in_litigation": false
    }
  },
  "archetype_resolution": {
    "matched_archetype_id": "...",
    "match_score": 0.83,
    "match_path": "MATCH | DISCOVERED | USER_FORCED",
    "alternates_considered": [{"id": "...", "score": 0.41}]
  },
  "slot_bindings": {
    "firm_name": "...",
    "firm_blog_url": "...",
    "mirror_handle": "..."
  },
  "footprint_score": 7,
  "dossier_markdown": "...",
  "sources": [
    {"url": "...", "category": "tier_1_regulatory", "retrieved": "YYYY-MM-DD", "claim_ids": ["c1","c2"], "from_archetype_recipe": true}
  ],
  "stable_traits": ["..."],
  "context_specific_lens": ["..."],
  "three_questions": ["...", "...", "..."],
  "persona_toml_block": "...",
  "archetype_refinement_proposal": {
    "applies_to_archetype_id": "...",
    "deltas": [
      {"type": "add_source", "...": "..."},
      {"type": "add_stable_trait_pattern", "...": "..."}
    ]
  },
  "warnings": ["..."],
  "status": "OK | INCOMPLETE | INSUFFICIENT_PUBLIC_DATA | REFUSED"
}
```

VERDICTS:
- PASS — `status: OK`: dossier complete, footprint_score ≥ 5, all claims source-cited, persona_toml_block contains disclaimer verbatim → ready for Aggregator
- PASS — `status: INCOMPLETE`: partial dossier (some source categories empty); aggregator decides whether to gap-fill or proceed
- FAIL — `status: INSUFFICIENT_PUBLIC_DATA`: footprint_score < 5; surface to user, do not fabricate
- FAIL — `status: REFUSED`: ethics-floor violation surfaced mid-research; halt and route to user

Be thorough. Be specific. Source-cite every claim. Never paraphrase the §10.1 disclaimer — it must appear byte-identical in persona_toml_block.
```

### Prompt: Discovery Worker (Domain Agent 4 of 6)

**subagent_type:** `rf-task-researcher`
**Sequencing:** Phase 4 — variant of Archetype-Driven Research Worker, spawned ONLY when Matcher returned `match_path: NO_MATCH` (top archetype score < match_threshold). Per guard G4 zero/empty row, also runs on first invocation when local_path is empty using the bootstrap `generic_public_figure` recipe.
**Model tiering:** Same as Archetype-Driven Worker — Haiku per-source, Opus for cross-source consolidation. Per §9.2 row 5 (verbatim): "Discovery worker — broad sweep | claude-haiku-4-5-20251001 (Haiku) | Same volume profile as archetype-driven worker, just wider."
**Budget:** Uses `research_budget.archetype_discovery_minutes` (default 18 — extended budget per FR-18) instead of the 12-minute per-subject budget.
**Input:** Verified `subject`, bootstrap `generic_public_figure` recipe (or last-best-fit archetype as starting heuristic), `${ETHICS_DISCLAIMER_VERBATIM}`.
**Output path:** `${TASK_DIR}research/[NN]-subject-<subject_code>.md` (same as archetype-driven worker) PLUS `${TASK_DIR}archetype-proposals/[NN]-<proposed_id>.yaml` for the discovered archetype.

```
Research the named subject WITHOUT a pre-existing matched archetype, and propose a NEW generic archetype to add to the local store. Write findings to [output-path] and the proposed archetype YAML to [archetype-proposal-path].

Subject: {name, affiliation, role}
Bootstrap recipe: generic_public_figure (or [last-best-fit archetype as broad starting point])
Research budget: [archetype_discovery_minutes] minutes (extended budget per FR-18)
Ethics disclaimer (verbatim, must appear in persona_toml_block):
[${ETHICS_DISCLAIMER_VERBATIM}]

CRITICAL — Incremental File Writing Protocol:
You MUST follow this protocol exactly. Violation results in data loss.

1. FIRST ACTION: Create your output file immediately with this header:
   ```markdown
   # Research: [Subject Name] (Discovery Mode)

   **Subject research type:** discovery-worker
   **Bootstrap archetype:** generic_public_figure
   **Status:** In Progress
   **Date:** [today]

   ---
   ```

2. As you sweep across source categories using the broad bootstrap recipe, IMMEDIATELY append your findings to the output file using Edit. Do NOT accumulate findings in your context window.

3. After each append, your output file grows. This is correct behavior. Never rewrite the file from scratch.

4. When finished, update the Status line from "In Progress" to "Complete" and append BOTH the §5.2 worker contract JSON block AND the discovered_archetype_proposal block.

Discovery Protocol:
1. Run the broad source sweep using the bootstrap recipe (wider than archetype-driven; longer budget)
2. Route searches through Tavily MCP per FR-25; Haiku per-source extraction
3. As patterns emerge across sources, identify candidate generic structure: slot_taxonomy (what slots are subject-specific?), decision_axes (what decision criteria recur?), source_recipe (which source tiers were most productive?), persona_description_template (generic skeleton with named slot placeholders, NOT firm/person names), three_questions_template (parameterized by slot bindings)
4. Run ONE Opus call to synthesize the proposed archetype YAML per §E schema
5. Run ONE Opus call to consolidate the subject's dossier_markdown, stable_traits, three_questions
6. Run ONE Opus call to generate persona_toml_block

CRITICAL — Documentation Staleness Protocol:
Same rules as Archetype-Driven Worker. Mark every source-derived claim with [SPEC-VERIFIED], [SOURCE-CONTRADICTED], or [UNVERIFIED]. Place all UNVERIFIED claims in warnings[].

CRITICAL — Generic-Purity Guarantee (FR-22):
The proposed `archetype.yaml` MUST be GENERIC. Static check on the YAML:
- `display_name`: a generic role label ("Crypto-native VC", "Family Office Allocator") — NEVER a person's name
- `slot_taxonomy`: parameterized slots (`firm_name`, `mirror_handle`, `fund_size`) — slot KEYS, not values
- `decision_axes`: generic decision dimensions ("technical-depth-vs-narrative", "lead-vs-follow") — NOT subject-specific picks
- `persona_description_template`: contains placeholder syntax like `{{firm_name}}`, `{{mirror_handle}}` — NOT literal names
- `stable_traits`: generic patterns ("references on-chain data in pitches") — NOT "[Subject] references Etherscan in their tweets"

Linter check (mandatory): Grep the proposed YAML for any of:
  - The verified subject's name
  - The verified subject's firm name (full string match)
  - The verified subject's fund name
  - Any URL containing the firm domain
If ANY of these appear in the core archetype fields (`display_name`, `slot_taxonomy`, `decision_axes`, `persona_description_template`, `stable_traits`), the discovery FAILS — clean the YAML or refuse with status REFUSED.

ADVERSARIAL STANCE:
Assume the proposed archetype will leak subject-specific identifiers until proven generic. Read your own YAML through the linter perspective: would another researcher use this template for a DIFFERENT subject without finding the original subject's fingerprint? If not, generalize harder.

Output BOTH the §5.2 worker contract JSON block (as in Archetype-Driven Worker) AND the discovery extension (per §5.2 L294-305):

```json
{
  "...": "(all §5.2 fields as in Archetype-Driven Worker — subject_input, identity_verification, archetype_resolution {match_path: \"DISCOVERED\"}, slot_bindings, footprint_score, dossier_markdown, sources, stable_traits, context_specific_lens, three_questions, persona_toml_block, archetype_refinement_proposal, warnings, status)",
  "discovered_archetype_proposal": {
    "archetype_id": "proposed_archetype_id_lowercase_underscored",
    "display_name": "Generic Role Label (no names)",
    "rationale": "1-3 sentences explaining why this archetype is distinct from existing ones",
    "full_archetype_yaml": "(the full YAML per §E schema as a string)"
  }
}
```

Also write the proposed YAML to [archetype-proposal-path] as a real `.yaml` file (the Aggregator + Approval Gate will route it to local_path on user approval). Per §5.6 and FR-21, this skill NEVER writes directly to canonical_path and NEVER auto-saves to local_path — the user reviews the proposal at the approval gate first.

VERDICTS:
- PASS — `status: OK`: dossier complete, archetype proposal passes generic-purity linter → Aggregator + Approval Gate
- FAIL — generic-purity linter trips: clean the YAML and re-emit, or surface as REFUSED with rationale
- FAIL — `status: INSUFFICIENT_PUBLIC_DATA`: discovery sweep found no usable archetype-pattern; surface to user

Be thorough. Be specific. Generic-purity is non-negotiable — a leaked name in a "generic" archetype poisons the whole local store.
```

### Prompt: Aggregator (Domain Agent 5 of 6)

**subagent_type:** `rf-task-researcher`
**Sequencing:** Phase 5 — runs AFTER all Phase 4 workers (Archetype-Driven + Discovery) have returned. Single instance. Hands off to Phase 6 Approval Gate.
**Model:** Opus for adversarial probe synthesis and unified diff generation; Haiku for routine table assembly.
**Input:** All §5.2 worker JSON blocks from Phase 4 outputs, archetype proposals (if any), `output_target.config_diff` path, `output_target.dossier_dir`.
**Output paths:**
- `${TASK_DIR}synthesis/aggregator-persona-blocks.md` (the assembled persona TOML blocks + dossier links + archetype proposals + Quantity Flow Diagram)
- `${TASK_DIR}synthesis/aggregator-proposed-config-diff.patch` (the unified diff against `_bmad/custom/config.toml` — NEVER auto-applied per FR-8)

```
Aggregate all worker outputs into a single review package and write to [output-path]. Hand off to the Approval Gate.

Worker JSON blocks: [list of paths to ${TASK_DIR}research/[NN]-subject-*.md files]
Archetype proposals (if any): [list of paths to ${TASK_DIR}archetype-proposals/*.yaml]
Existing config: _bmad/custom/config.toml
Output dossier dir: [output_target.dossier_dir]

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file with header { "# Aggregation Report", "Status: In Progress", "Date" }
2. As each worker JSON is parsed and validated, IMMEDIATELY append findings
3. After all workers processed, append the Quantity Flow Diagram (App B), the unified config diff, and the adversarial probes section
4. Mark Status: Complete

Aggregation Protocol:
1. Validate every worker JSON against the §5.2 strict schema. Hard failure on non-conformance.
2. For each subject, write the dossier_markdown to [output_target.dossier_dir]/<code>-dossier.md
3. Assemble persona_toml_block entries into a single proposed-config-diff.patch (unified diff against _bmad/custom/config.toml). Per FR-8, this diff is NEVER auto-written — it is a proposal for the user.
4. Per FR-12, emit the Quantity Flow Diagram (Appendix B) with ACTUAL counts:
   - N subjects in
   - P verified-and-MATCH, Q verified-and-DISCOVERED, R AMBIGUOUS-or-REFUSED
   - dossiers produced, persona TOML blocks produced, archetype proposals produced
5. For each archetype proposal, route the YAML to [archetype-proposals dir]. Per §5.6 the skill NEVER writes to canonical_path; per FR-21 the skill NEVER auto-saves to local_path — the Approval Gate writes after user confirms.

CRITICAL — Documentation Staleness Protocol:
The persona TOML blocks that workers produced are themselves a form of documentation about subjects. Cross-validate before passing to approval:
- Every persona_toml_block contains the §10.1 disclaimer byte-identical (em-dash U+2014, ASCII apostrophe U+0027 per spec lines 30-32)
- Every claim in dossier_markdown traces to a sources[] entry
- No verbatim quotes longer than 10 words anywhere in dossier_markdown (FR-7)

Adversarial Probe Section (mandatory):
For each persona, answer these probes IN WRITING in the aggregation report:
1. Would this persona still hold if the subject's name were removed and only the slot_bindings remained? (If no → archetype too thin or footprint too low.)
2. Would this subject fit a DIFFERENT archetype better? (Score the top 2 alternates from archetype_resolution.alternates_considered against the dossier; flag if an alternate fits better than the matched one.)
3. Are any direct quotes verbatim (>10 words)? Run grep over dossier_markdown for `"..."` substrings. (If yes → FR-7 violation; refuse aggregation.)
4. Does footprint_score ≥ 5 hold? (If no → status should be INSUFFICIENT_PUBLIC_DATA, not OK.)
5. Generic-purity (for archetype proposals): does the proposed YAML pass the linter? (If no → reject the proposal.)

ADVERSARIAL STANCE:
Assume every persona is wrong until proven right by the probes. The Aggregator is the LAST gate before user review — surface every doubt explicitly. The probe answers go INTO the aggregation report so the user sees them.

Hand-off to Approval Gate:
Output the aggregation report (with Quantity Flow Diagram + adversarial probes) and the proposed-config-diff.patch. The next phase is the user-facing approval gate (Phase 6) — present:
- The Quantity Flow Diagram
- The dossier paths
- The proposed config diff
- The adversarial probe answers
- Each archetype proposal with rationale and "approve / reject / edit" prompt

VERDICTS:
- PASS — all workers conformant, all probes answered, diff prepared → Approval Gate
- FAIL — schema non-conformance: surface the offending worker output to user; halt
- FAIL — FR-7 verbatim-quote violation: refuse aggregation, route worker back for paraphrase
- FAIL — generic-purity linter on archetype proposal: refuse the proposal, surface to user

Be adversarial. Be specific. The aggregation report is the artifact the user reviews — every probe answered honestly here saves a wrong-direction approval.
```

### Prompt: Validator (Domain Agent 6 of 6, OPTIONAL)

**subagent_type:** `rf-task-researcher`
**Sequencing:** Phase 7 — runs ONLY when `--validate` flag passed. After user approves the personas at Phase 6, Validator spawns each persona in a sandboxed subagent and runs the three-questions test (FR-23) against a context_artifact (e.g., a pitch deck).
**Model (§9.2 row 9):** "Validator (three-questions test spawn) | Same model as production party-mode usage | Validator must mirror runtime conditions for fidelity score to be meaningful."
**Input:** Approved persona_toml_blocks (one per subject), `context_artifact` path (e.g., a pitch deck markdown), `three_questions` (one set per subject from §5.2 worker contract).
**Output path:** `${TASK_DIR}validation/<code>-validation.md` (one per subject), and `${TASK_DIR}validation/fidelity-summary.md` (aggregated).

```
Validate that the approved persona, when spawned and given the context_artifact, would respond with answers consistent with its three_questions. Write findings to [output-path].

Persona TOML block: [persona_toml_block]
Three questions: [three_questions list of 3]
Context artifact: [context_artifact path — e.g., a pitch deck markdown]
Subject code: [code]

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create [output-path] with { "# Validation: [Subject Code]", "Status: In Progress", "Date" }
2. After each of the 3 question runs, append the persona's predicted answer
3. After all 3 questions, append the fidelity score and rationale
4. Mark Status: Complete

Validation Protocol:
1. Spawn a subagent with the persona_toml_block (mirror production party-mode invocation per §9.2 row 9)
2. For each of the three_questions, prompt the persona-spawned subagent: "Read [context_artifact]. Answer this question as the modeled persona: [question]"
3. Capture each predicted answer
4. Score fidelity:
   - Did the persona's answer reference the slot_bindings (firm-relevant signals)?
   - Did the persona's answer match the stable_traits patterns?
   - Did the persona maintain the §10.1 disclaimer framing (no first-person identity claim)?
5. Compute fidelity score 0-10 per Acceptance Criterion #4 (target ≥ 7/10)

CRITICAL — Documentation Staleness Protocol:
The context_artifact may itself be stale (a pitch deck from a prior fundraise). Note retrieval/version date in the validation report. Do NOT score fidelity against a context_artifact whose date is unknown — flag as INSUFFICIENT_TEST_FIXTURE.

ADVERSARIAL STANCE:
Assume the persona will sound plausible but miss the slot_bindings until proven otherwise. A fidelity score is meaningful only if the persona references SPECIFIC details traceable to the dossier — not generic VC platitudes. If predicted answers are generic, fidelity score is LOW regardless of fluency.

User-Review Gate:
After predicting answers, OUTPUT THEM TO THE USER for review. The Validator does NOT auto-pass — the user inspects predicted answers and confirms whether they match the modeled persona's expected behavior. Per FR-23, the Validator is a SUGGESTION tool, not an autopass.

Output the validation report:

```markdown
## Validation: [Subject Code]

**Persona archetype:** [archetype_id]
**Context artifact:** [path] (retrieved [date])
**Fidelity score:** [0-10]

### Question 1: [question]
**Predicted answer:** [answer]
**Score reasoning:** [why this scores N/10 — references to slot_bindings, stable_traits]

### Question 2: ...
### Question 3: ...

**Aggregate fidelity:** [score]/10
**User decision required:** approve / reject / re-run with adjusted persona
```

VERDICTS:
- PASS — fidelity ≥ 7/10 across all 3 questions: persona is approved
- WARN — fidelity 5-6: surface to user for manual review
- FAIL — fidelity < 5: persona is too generic; re-spawn with stronger slot_bindings or refuse

Be honest. Be specific. The Validator is OPTIONAL but when invoked must give the user enough information to trust (or reject) the persona, not paper over weak fidelity.
```

---

### Lens QA Prompts (Phase 5 Gate 2 — Build-Time Skill Authoring Only)

**Note:** These six lens prompts run during **skill authoring** (Phase 5 of skill-creator generation when this SKILL.md was being produced or is being extended), **NOT during runtime persona-research execution**. Runtime QA for persona-research artifacts is handled by Aggregator + the user-facing Approval Gate (the worker prompts above) and the optional Validator. The vocabulary in these lens prompts (BUILD_REQUEST, section classification, COPY/SUBSTITUTE/GENERATE) is skill-creator authoring vocabulary and does not apply to runtime persona-research worker outputs.

The six lens QA prompts below are spawned in parallel after Aggregation produces the review package and before the user-facing Approval Gate. Each lens has a narrow, non-overlapping scope. All six must PASS before the Approval Gate engages; any FAIL returns the offending artifact to the responsible upstream worker.

### Prompt: Template-Conformance Lens (Lens QA 1 of 6)

**subagent_type:** `rf-qa`
**Scope:** Structural conformance — verifies the produced SKILL.md (when this skill is being used to generate another skill) or the produced persona artifacts conform to template structure.
**Output path:** `${TASK_DIR}qa/lens-template-conformance.md`

```
Verify that the produced artifacts conform to the canonical template structure.

Artifacts to inspect: [list of paths — SKILL.md scaffolds, persona TOML blocks, archetype YAMLs]
Reference template: [reference path — e.g., the 29-section structure from /config/workspace/IronClaude/.dev/releases/current/skill-creator/]

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create [output-path] with header "Status: In Progress"
2. As each artifact is checked, IMMEDIATELY append findings
3. Mark Status: Complete

Checklist:
1. 29-section structure present (S1-S29) — every section header matches the canonical names
2. Frontmatter validity — `name`, `description`, `allowed-tools` keys present and well-formed
3. COPY-classified sections byte-match their reference source (verify via diff against tech-research lines indicated in section classification)
4. SUBSTITUTE-classified sections preserve reference structure with only domain-variable substitutions
5. GENERATE-classified sections present and non-empty

CRITICAL — Documentation Staleness Protocol:
The reference templates themselves can drift. Use the LATEST committed version from `.claude/skills/`. If a section header in the reference has a different name than what the artifact uses, log it — do not assume the reference is wrong without verifying.

ADVERSARIAL STANCE:
Assume the artifact has structural drift until proven otherwise. Sample 5 random sections and verify both header text AND ordering against the reference.

VERDICTS:
- PASS: all 5 checklist items pass
- FAIL: any item fails — list the offending section(s) and remediation

Be specific. Cite line numbers. Do not gloss over partial matches.
```

### Prompt: Internal-Consistency Lens (Lens QA 2 of 6)

**subagent_type:** `rf-qa`
**Scope:** Cross-section consistency — no contradictions between S18 BUILD_REQUEST and S20 worker contract; agent prompts in S20 reference fields that exist in §5.2.
**Output path:** `${TASK_DIR}qa/lens-internal-consistency.md`

```
Verify that internal references between sections are consistent.

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create [output-path]; status In Progress
2. Append findings per cross-section pair checked
3. Status: Complete on finish

Checklist:
1. S18 BUILD_REQUEST refers to worker contract — verify the schema described matches the §5.2 schema verbatim in S20
2. S25 Validation Checklist references FR-1..FR-26 — verify each FR is mentioned at least once across S2-S24
3. S27 Critical Rules referencing FR-numbers — verify each FR cited actually exists in the spec
4. S6 examples referencing TASK_ID prefix — verify the prefix matches S4 Variable Reference
5. Worker contract field names in S20 (identity_verification, archetype_resolution, slot_bindings, footprint_score, dossier_markdown, sources, stable_traits, three_questions, persona_toml_block, archetype_refinement_proposal, discovered_archetype_proposal) — verify each is referenced in at least one other section that orchestrates them (S18, S22, S24, S25)

CRITICAL — Documentation Staleness Protocol:
This skill's own SKILL.md is the documentation under test. If a section references "see §X" and §X was renumbered, flag it.

ADVERSARIAL STANCE:
Assume cross-references are stale until verified. Manually trace 5 random "see §X" or "per FR-N" references end-to-end.

VERDICTS:
- PASS: all 5 checks pass
- FAIL: list each broken cross-reference with section IDs and proposed fix
```

### Prompt: Evidence-Quality Lens (Lens QA 3 of 6)

**subagent_type:** `rf-qa`
**Scope:** Every claim in dossier_markdown traces to a sources[] entry; every FR cited has a spec line number reference.
**Output path:** `${TASK_DIR}qa/lens-evidence-quality.md`

```
Verify that every factual claim is backed by a source line citation.

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create [output-path]; In Progress
2. Append per-claim verdicts as you sample
3. Status: Complete

Checklist:
1. Sample 10 random claims from dossier_markdown across all subjects; for each, verify a sources[] entry covers it (claim_ids cross-reference)
2. Sample 5 random FR citations in S25 / S27 / S20 prompts; for each, verify the FR exists at the cited line in the spec
3. Verify §10.1 disclaimer appears verbatim in every persona_toml_block (byte-fidelity check — em-dash U+2014, ASCII apostrophe U+0027)
4. Verify no `"..."` substring exceeding 10 words exists in any dossier_markdown (FR-7 no-quote rule)
5. Verify each sources[] entry has {url, category, retrieved} fully populated

CRITICAL — Documentation Staleness Protocol:
A claim's source URL must be retrievable today. Spot-check 2 source URLs are reachable; if any 404, mark the claim [SOURCE-CONTRADICTED] (now defunct) and surface as a warning.

ADVERSARIAL STANCE:
Every unsourced claim is a fabrication risk. Be ruthless on the 10-claim sample — if even ONE claim has no traceable source entry, the lens FAILS.

VERDICTS:
- PASS: all 5 checks pass
- FAIL: list unsourced claims, broken disclaimers, FR citations that don't trace
```

### Prompt: Actionability Lens (Lens QA 4 of 6)

**subagent_type:** `rf-qa-qualitative`
**Scope:** Agent prompts in S20 are runnable end-to-end without reading SKILL.md; every checklist item is self-contained.
**Output path:** `${TASK_DIR}qa/lens-actionability.md`

```
Verify that each agent prompt and checklist item is self-contained and immediately runnable.

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create [output-path]; In Progress
2. Append per-prompt verdicts
3. Status: Complete

Checklist:
1. Sample 3 random S20 prompts; for each, verify all needed inputs (paths, schemas, disclaimers) are inlined in the prompt itself — the agent should NOT need to read SKILL.md
2. Verify each prompt names its subagent_type explicitly
3. Verify each prompt names its output path explicitly
4. Verify each prompt embeds at least the Incremental File Writing Protocol verbatim (≥1 occurrence in research/QA prompts)
5. Verify the §5.2 worker contract JSON schema appears EXACTLY ONCE verbatim across S20 (not duplicated across multiple prompts; not paraphrased)

CRITICAL — Documentation Staleness Protocol:
If a prompt references `${TASK_ID_PREFIX}` or `${DOMAIN_NAME}` placeholders that should have been substituted, flag them — the BUILD_REQUEST or skill-author missed the substitution step.

ADVERSARIAL STANCE:
Assume each prompt is missing at least one input. If you find a sampled prompt that references a path or variable that is not also defined in the prompt, the lens FAILS.

VERDICTS:
- PASS: all 5 checks pass
- FAIL: list non-runnable prompts and missing inputs
```

### Prompt: Domain-Accuracy Lens (Lens QA 5 of 6)

**subagent_type:** `rf-qa-qualitative`
**Scope:** Domain-specific accuracy — FR mapping correctness, ethics §10.1 disclaimer verbatim presence, archetype generic-purity rules present.
**Output path:** `${TASK_DIR}qa/lens-domain-accuracy.md`

```
Verify that domain-specific rules and FR mappings are accurate.

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create [output-path]; In Progress
2. Append per-rule verdicts
3. Status: Complete

Checklist:
1. §10.1 disclaimer is byte-identical wherever it appears (em-dash U+2014, ASCII apostrophe U+0027)
2. FR-22 generic-purity linter rules are present in S20 Discovery Worker prompt (no firm/person/fund names in display_name, slot_taxonomy, decision_axes, persona_description_template, stable_traits)
3. FR-24 model tiering rule is present in S20 Archetype-Driven Worker prompt (no Opus per-source; Opus only at consolidation)
4. FR-25 Tavily routing is present in S20 worker prompts (web searches MUST route through Tavily MCP when configured)
5. FR-7 no-quote rule referenced in S20 + S25 (no verbatim quotes >10 words)
6. FR-8 + FR-21 no-auto-write rules referenced in Aggregator prompt (config diff never auto-applied; archetype proposals never auto-saved to local_path)
7. §10.2 unsuitable-subject categories referenced in Identity Verifier (deceased/minors/private/witnesses-in-litigation)

CRITICAL — Documentation Staleness Protocol:
Spec FRs evolve. If the produced skill cites FR-X at line N but spec has FR-X at line M, flag the line-number drift but accept the citation if the FR text matches.

ADVERSARIAL STANCE:
Assume one FR rule is missing. Run the checklist exhaustively; do not stop at the first PASS.

VERDICTS:
- PASS: all 7 checks pass
- FAIL: list missing rules and proposed insertion points
```

### Prompt: Section-Classification-Accuracy Lens (Lens QA 6 of 6)

**subagent_type:** `rf-qa-qualitative`
**Scope:** Verifies COPY/SUBSTITUTE/GENERATE classifications applied per section match the section classification file (`research/12-section-classification.md`).
**Output path:** `${TASK_DIR}qa/lens-classification-accuracy.md`

```
Verify each section's content matches its declared COPY/SUBSTITUTE/GENERATE classification.

Reference: ${TASK_DIR}research/12-section-classification.md

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create [output-path]; In Progress
2. Append per-section verdicts
3. Status: Complete

Checklist:
1. For each COPY section (S11, S17, S19): byte-diff against the cited reference source — flag any divergence beyond domain-variable substitution
2. For each SUBSTITUTE section: structure preserved? Only domain variables changed? No new content added beyond what variables replace?
3. For each GENERATE section: content is domain-specific (not boilerplate from a reference template)
4. Sample 3 random sections from each classification — verify the chosen classification is the LEAST disruptive (a section that could have been SUBSTITUTE should not be GENERATE)
5. Verify the section classification file's reasoning is consistent with what was actually produced

CRITICAL — Documentation Staleness Protocol:
The classification file is itself a planning artifact — it can be wrong. If you find a section labeled COPY but the reference has changed since classification was authored, flag the drift.

ADVERSARIAL STANCE:
Assume one section is misclassified. Look hardest at SUBSTITUTE-vs-GENERATE boundaries — a section that paraphrases a reference but changes structure may be miscategorized as SUBSTITUTE when it should be GENERATE.

VERDICTS:
- PASS: all classifications accurate
- FAIL: list misclassified sections with proposed correction
```

---

### Source-Fidelity Prompts (Phase 5 Gate 2.5)

The three prompts below run AFTER the six lens gates pass. They specifically probe whether the generated SKILL.md preserves semantic intent from the reference skills and the source spec.

### Prompt: Reference-Skill Semantic Coverage (Source-Fidelity 1 of 3)

**subagent_type:** `rf-qa`
**Scope:** Verifies the produced SKILL.md preserves structural patterns from the 5 reference skills (tech-research, skill-creator, task-builder, prd, tdd).
**Output path:** `${TASK_DIR}qa/fidelity-reference-skill-coverage.md`

```
Verify that the produced SKILL.md preserves structural patterns from the 5 reference skills.

Reference skills:
- /config/workspace/IronClaude/.claude/skills/tech-research/SKILL.md
- /config/workspace/IronClaude/.claude/skills/skill-creator/SKILL.md
- /config/workspace/IronClaude/.claude/skills/task-builder/SKILL.md
- /config/workspace/IronClaude/.claude/skills/prd/SKILL.md
- /config/workspace/IronClaude/.claude/skills/tdd/SKILL.md

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create [output-path]; In Progress
2. Append per-pattern verdicts
3. Status: Complete

Checklist (sampling):
1. Two-stage A/B execution pattern (Stage A: scope discovery; Stage B: task file execution) — present in produced skill?
2. F1 execution loop (READ → IDENTIFY → EXECUTE → UPDATE → REPEAT) — present?
3. Parallel agent spawning protocol — present in S19?
4. Incremental File Writing Protocol — embedded in research/QA prompts in S20?
5. Documentation Staleness Protocol — embedded in research/QA prompts in S20?

CRITICAL — Documentation Staleness Protocol:
The reference skills evolve. Use the latest committed version. If a reference's pattern shifted between commits, prefer the most-recently-edited reference.

ADVERSARIAL STANCE:
Assume one pattern is missing. Sample patterns 1-5 above explicitly — do not infer presence from "looks similar."

VERDICTS:
- PASS: all 5 patterns present
- FAIL: list missing patterns and proposed insertion section
```

### Prompt: Spec FR Coverage (Source-Fidelity 2 of 3)

**subagent_type:** `rf-qa`
**Scope:** Every FR-1..FR-26 referenced; every §11 acceptance criterion mapped to S25 validation checklist.
**Output path:** `${TASK_DIR}qa/fidelity-spec-fr-coverage.md`

```
Verify that every FR and every §11 acceptance criterion has a referent in the produced SKILL.md.

Spec: /config/workspace/IronClaude/.dev/releases/current/persona-research/persona-research-skill-spec.md
Spec partition files (for line numbers):
- ${TASK_DIR}research/07-spec-part1-frs-architecture.md (FR-1..FR-23)
- ${TASK_DIR}research/08-spec-part2-failures-validation-ops.md (FR-24/25/26 + §11 acceptance + §6 failure modes)
- ${TASK_DIR}research/09-spec-part3-ethics-acceptance-archetype-schema.md (§10 ethics + §E archetype schema)

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create [output-path]; In Progress
2. Append per-FR coverage verdicts
3. Status: Complete

Checklist:
1. FR-1..FR-26: each referenced at least once across S2..S29 of the produced skill
2. §11 acceptance criteria (15 items): each maps to a row in S25 Validation Checklist
3. §6 failure modes: each has a referent in S3 (Why This Process Works) or S20 worker prompts (warnings[] / status enum)
4. §10.1 disclaimer: appears byte-identical wherever cited (em-dash U+2014, ASCII apostrophe U+0027)
5. §10.2 unsuitable-subject categories (deceased/minor/private/witness): referenced in S13 (Parse & Triage) and S20 Identity Verifier prompt
6. §10.3 ethics attestation: referenced in S13

CRITICAL — Documentation Staleness Protocol:
The spec is the source of truth, but spec line numbers drift across edits. Use the partition files (07/08/09) as the canonical FR-to-line mapping.

ADVERSARIAL STANCE:
Assume one FR is missing a referent. Cross-reference the FR table from spec part 1 §4 exhaustively.

VERDICTS:
- PASS: all FRs and acceptance criteria covered
- FAIL: list uncovered FRs / acceptance items with proposed insertion section
```

### Prompt: Domain-Noun Leakage (Source-Fidelity 3 of 3)

**subagent_type:** `rf-qa-qualitative`
**Scope:** No `tech-research` / `prd` / `tdd` / `skill-creator` / `task-builder` domain phrases leaked into SUBSTITUTE/GENERATE sections.
**Output path:** `${TASK_DIR}qa/fidelity-domain-noun-leakage.md`

```
Verify that no reference-skill domain nouns leaked into the produced SKILL.md's domain-specific sections.

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create [output-path]; In Progress
2. Append findings per leaked phrase found
3. Status: Complete

Checklist (grep-based):
1. Run `grep -n "tech-research\|tech research\|technical research"` against produced SKILL.md — every hit must be in a COPY section that explicitly cites tech-research as the source (e.g., S19 protocol blocks). Hits in SUBSTITUTE/GENERATE sections are leakage.
2. Run `grep -n "PRD\|prd"` — every hit must reference PRDs as a comparison/example, not as the produced skill's own domain
3. Run `grep -n "TDD\|tdd"` — same rule
4. Run `grep -n "skill-creator"` — only allowed where explicitly framed as a reference-skill citation
5. Run `grep -n "task-builder"` — same rule
6. Run `grep -n '\${DOMAIN_NAME}\|\${TASK_ID_PREFIX}'` — must return ZERO hits (all template placeholders should have been substituted)

CRITICAL — Documentation Staleness Protocol:
A reference to "tech-research" inside a citation like "Reference: /config/workspace/.../tech-research/SKILL.md" is intentional — only flag bare nouns in body prose.

ADVERSARIAL STANCE:
Assume there is at least one leaked noun. Run all 6 greps; do not stop at the first one that returns expected hits only.

VERDICTS:
- PASS: all 6 greps clean (only intentional citations remain)
- FAIL: list each leaked phrase with line number and proposed replacement
```



---

## Output Structure

This skill produces output at TWO levels: (a) the SKILL.md document itself (29-section RF schema, written incrementally during skill generation), and (b) the runtime artifacts produced when the skill executes a persona-research run.

### 21.1 SKILL.md schema (this document, 29 sections in order)

When this SKILL is generated by skill-creator, it follows the canonical 29-section RF structure. Each section is COPIED verbatim from tech-research, SUBSTITUTED with persona-research domain nouns, or GENERATED net-new from spec evidence.

The 29 sections below are the canonical logical structure; in this document they appear as plain `##` headers per the tech-research convention rather than numbered `## N.` headers.

```markdown
# Skill: sc-persona-research-protocol

[S1  Frontmatter + Title — name, description, allowed-tools, plus the H1 title line]

## S2  Overview + How it works
## S3  Why This Process Works
## S4  Variable Reference
## S5  Input
## S6  Effective Prompt Examples
## S7  What to Do If Prompt Is Incomplete
## S8  Depth Tiers
## S9  Output Locations
## S10 Execution Overview
## S11 Stage A header
## S12 A.1 Check for Existing Task File
## S13 A.2 Parse & Triage
## S14 A.3 Perform Scope Discovery
## S15 A.4 Write Research Notes File
## S16 A.5 Review Research Sufficiency
## S17 A.6 Template Triage
## S18 A.7 Build the Task File / A.8 Receive & Verify
## S19 Stage B Task File Execution (inline F1 execution loop per §10; the skill is NOT consulted during execution)
## S20 Agent Prompt Templates
## S21 Output Structure
## S22 Synthesis Mapping Table
## S23 Synthesis Quality Review Checklist
## S24 Assembly Process
## S25 Validation Checklist
## S26 Content Rules (Non-Negotiable)
## S27 Critical Rules (Non-Negotiable)
## S28 Session Management
## S29 Research Quality Signals
```

This logical S1-S29 mapping is the authoritative reference (cross-checked against `${TASK_DIR}research/12-section-classification.md`). In this document the corresponding live `## ` headers use plain descriptive names per the tech-research convention (e.g., `## Input`, `## Depth Tiers`, `## Stage B: Task File Execution`) rather than `## SN` numeric prefixes.

### 21.2 Runtime artifacts produced by a persona-research run

When the skill executes, each invocation produces the following files. Paths are relative to the working project unless prefixed with the skill root.

| Artifact | Path Pattern | Per-subject? | Source FR / Spec § |
|----------|--------------|--------------|--------------------|
| Evidence dossier (markdown, ~500 words, source-cited) | `<dossier_dir>/<code>-dossier.md` (default `_bmad-output/planning-artifacts/persona-research/`) | One per subject | FR-4 + FR-5 + spec §3 Outputs L119-120 |
| Persona TOML block (ready to paste into `[agents.<code>]`) | embedded in unified config diff | One per subject | FR-4 + FR-6 + spec §3 Outputs L121 |
| Three-questions test file | `<dossier_dir>/<code>-three-questions.md` | One per subject | FR-4 + spec §3 Outputs L122 + Appendix C |
| Unified config.toml diff (NEVER auto-written) | proposed against `_bmad/custom/config.toml` | One per run, all subjects merged | FR-8 + spec §3 Outputs L123 |
| Archetype proposal (new YAML for global store, NEVER auto-written) | proposed against `archetype_store.local_path` | One per `NO_MATCH` subject (discovery worker) | FR-18 + FR-21 + Appendix E schema |
| Archetype refinement deltas (version bump, NEVER auto-written) | proposed against existing `<id>.yaml`, prior versions retained as `<id>.v<N>.yaml` | One per `MATCH` + `refinement_mode==auto` subject | FR-19 + FR-21 + Appendix E |
| Pipeline Quantity Flow Diagram (Appendix B) | embedded in run summary stdout | One per run | FR-12 + Appendix B |
| Guard Boundary Tables (G1-G4, Appendix A) | embedded in run summary stdout | One per run | Appendix A guards |
| Run summary (counts, model-tier spend, promotion candidates) | stdout + `<dossier_dir>/run-summary.md` | One per run | FR-26 + spec §9.1 promotion |
| Validation report (only if `--validate` passed) | `<dossier_dir>/validation-report.md` | One per run | FR-14 + spec §8 |

### 21.3 Output emission rules

- **NEVER auto-write** to `_bmad/custom/config.toml`, the canonical archetype store, or the local archetype store. All writes are PROPOSED via diffs / write-set descriptors that the user explicitly approves at the Approval Gate (FR-8, FR-21).
- **ALWAYS emit** the Pipeline Quantity Flow Diagram and Guard Boundary Tables on every run, even when N==M (no divergence) — per FR-12 and Appendix A/B.
- **ALWAYS prepend** the §10.1 disclaimer to every persona description, with byte-equality enforced before the description is written to disk (FR-6).
- **NEVER emit** a persona description containing first-person quotes attributed to the real subject (FR-7).
- The Approval Gate writes (when approved) go EXCLUSIVELY to `archetype_store.local_path`. The skill NEVER writes to `archetype_store.canonical_path` at runtime — promotion to canonical is a manual user action documented in §9.1.

---

## Synthesis Mapping Table

This skill uses **incremental Edit assembly** rather than the synth-files pattern from tech-research. There is no `synth-NN-*.md` intermediary set — Phase 4 writes directly to the output SKILL.md (during skill-generation) and the runtime aggregator writes directly to the persona/archetype output artifacts (during a persona-research run).

This section provides two reference mappings:

### 22.1 Skill-generation mapping (research file → SKILL.md section)

Used during Phase 4 sub-phases when this very SKILL.md was being assembled by skill-creator. For traceability only.

| SKILL.md Section | Source Research File(s) | Assembly Pattern |
|------------------|-------------------------|------------------|
| Frontmatter + S1 Skill Overview | `02-reference-tech-research.md`, spec §1-§2 (file 06) | SUBSTITUTE (domain-noun replace) |
| S2 When to Use / S3 When NOT to Use | `02-reference-tech-research.md`, research-notes.md TRIGGER_PATTERNS | SUBSTITUTE |
| S4 Skill Triggers | research-notes.md TRIGGER_PATTERNS | GENERATE |
| S5 Input | spec §3 Inputs L84-113 (file 07) | GENERATE (domain-specific YAML schema) |
| S6 Depth Tiers | tech-research S6 boilerplate | SUBSTITUTE |
| S7 Output Locations | spec §3 Outputs L117-124 (file 07) | SUBSTITUTE (distributed pattern) |
| S8 Variable Reference | tech-research S8 boilerplate | SUBSTITUTE (TASK-PERSONARES prefix) |
| S9 Execution Overview | research-notes.md SUGGESTED_PHASES + spec §5 architecture (file 07) | GENERATE |
| S10-S17 Stage A (A.1-A.7) | tech-research S10-S17 + skill-creator A.7 BUILD_REQUEST template | SUBSTITUTE + GENERATE (A.7 customized) |
| S18 Stage A Output | tech-research S18 boilerplate | COPY |
| S19 Stage B | tech-research S19 boilerplate | COPY (verbatim protocol blocks) |
| S20 Agent Prompt Templates | spec §5 architecture + §9.2 model-tiering + §5.2 worker contract (files 07, 08) | GENERATE (6 domain agents + 6 lens QA + 3 source-fidelity) |
| S21 Output Structure | spec §3 Outputs + Appendix B (files 07, 08) | SUBSTITUTE |
| S22 Synthesis Mapping Table (this section) | meta-mapping | GENERATE |
| S23 Synthesis Quality Review Checklist | spec §11 acceptance + §10 ethics + §6 failure modes (files 08, 09) | SUBSTITUTE |
| S24 Assembly Process | research-notes.md Phase 4 sub-phase plan | GENERATE |
| S25 Validation Checklist | spec §11 (file 09) + BUILD-REQUEST.md VALIDATION_REQUIREMENTS + all FRs (files 07, 08, 09) | GENERATE |
| S26 Content Rules | tech-research S26 + spec §10 ethics + FR-7/FR-22 (file 09) | SUBSTITUTE |
| S27 Critical Rules | tech-research S27 + skill-creator critical rules + spec §10 disclaimer + FR-2/6/7/22/24/25/26 | GENERATE |
| S28 Session Management | tech-research S28 boilerplate | SUBSTITUTE (TASK-PERSONARES) |
| S29 Research Quality Signals | tech-research S29 + spec §6/§7/§11 quality signals | SUBSTITUTE |

### 22.2 Runtime mapping (worker JSON output → output artifacts)

Used during a persona-research RUN by the Aggregator component. Worker emits a single §5.2 JSON contract; Aggregator splits its fields across the output artifacts.

| Worker JSON Field (per §5.2 L247-292) | Output Artifact | Notes |
|---------------------------------------|-----------------|-------|
| `subject_input` (name, affiliation, role) | dossier markdown header | Echoed for traceability |
| `identity_verification.{verified, canonical_url, alternates_considered}` | dossier markdown identity block + Guard G1 row of run summary | FR-2 |
| `archetype_resolution.{matched_archetype_id, match_score, match_path, alternates_considered}` | dossier markdown archetype block + Guard G4 row of run summary | FR-16, FR-17, FR-20 |
| `slot_bindings` (firm_name, firm_blog_url, mirror_handle, etc.) | persona TOML block (slot substitution) + dossier metadata | Per matched archetype's slot_schema |
| `footprint_score` (0-10) | dossier markdown header + Guard G3 row of run summary | FR-11 |
| `dossier_markdown` | dossier `.md` file body | FR-4, FR-5 |
| `sources[]` ({url, category, retrieved, claim_ids[], from_archetype_recipe}) | dossier "Sources" appendix | FR-5 (every claim source-cited) |
| `stable_traits` (list of strings) | persona TOML block STABLE TRAITS + archetype refinement candidate | Used by Aggregator to detect refinement deltas |
| `context_specific_lens` | persona TOML block CONTEXT-SPECIFIC LENS | Per-run overlay |
| `three_questions` (length 3) | three-questions test file | FR-14 + Appendix C template |
| `persona_toml_block` | unified config.toml diff (one block per subject) | FR-6 disclaimer prepended; FR-7 no first-person quotes |
| `archetype_refinement_proposal.{applies_to_archetype_id, deltas[]}` | archetype refinement write-set descriptor | FR-19, FR-21 (NEVER auto-write) |
| `discovered_archetype_proposal.{archetype_id, display_name, rationale, full_archetype_yaml}` (discovery-worker only) | new archetype YAML write-set descriptor | FR-18, FR-21, FR-22 (no firm/person names in core fields) |
| `warnings[]` | run summary "Warnings" section | FR-26 spend report; §6 failure-mode warnings |
| `status` (`OK`/`INCOMPLETE`/`INSUFFICIENT_PUBLIC_DATA`/`REFUSED`) | Pipeline Quantity Flow Diagram divergence counts (Stage 4) + run summary | FR-11, FR-12, §6 |

The Aggregator does NOT re-run worker reasoning (per §5.4 Service-Boundary Rules). It only consumes worker JSON and routes its fields to the appropriate output artifact.

---

## Synthesis Quality Review Checklist

These quality criteria are applied by rf-analyst and rf-qa agents during Phase 5 (Lens-Based Structural + Qualitative QA Gate) and Gate 2.5 (Source-Fidelity). They are FR-driven — each criterion ties back to a specific functional requirement or VALIDATION_REQUIREMENT.

The 12 quality criteria:

1. **§10.1 disclaimer string-equality (FR-6 / VALIDATION_REQUIREMENT ETHICS_DISCLAIMER_VERBATIM).** Every produced persona description begins with the §10.1 disclaimer text byte-verbatim. Reviewer runs string-equality check (NOT substring or fuzzy match). Em-dash must be U+2014, apostrophe U+0027.
2. **FR-7 no-first-person-quote static check (NO_FIRST_PERSON_ATTRIBUTION).** Persona descriptions and dossiers contain no quoted strings matching attribution patterns. Static regex check (`grep -nE '\b[A-Z][a-z]+ (said\|stated\|wrote\|tweeted)\s+["“]'` and `grep -nE '^[A-Z][a-z]+:\s*"'`) + dynamic §8.4 fabrication probe.
3. **FR-22 archetype generic-purity linter (ARCHETYPE_GENERIC_PURITY).** Proposed archetype YAML's `display_name`, `persona_description_template`, and `stable_traits` fields contain NO person names, firm names, or fund names. Only `identity_signals.affiliation_keywords` is permitted to contain firm names (as match examples, not as the archetype identity).
4. **FR-5 source-citation completeness.** Every dossier claim cites a source URL + retrieval ISO date. No orphan claims. Reviewer can spot-check any claim by clicking through.
5. **FR-2 identity-first sequencing (IDENTITY_VERIFIED_BEFORE_RESEARCH).** Worker JSON contracts show `identity_verification.verified == true` before any source-fetch evidence appears in the dossier. No research worker spawned for a subject whose `identity_verified` is false.
6. **FR-12 Quantity Flow Diagram emission (PIPELINE_QUANTITY_FLOW_DIAGRAM_PRESENT).** Run summary contains the Appendix B diagram with actual N/N'/P/Q/M/K counts populated. Diagram present even when N==M.
7. **Guard Boundary Tables emission (GUARD_BOUNDARY_TABLE_PRESENT).** Run summary contains G1 (`identity_verified`), G2 (`subject_is_living_adult_public_figure`), G3 (`public_footprint_above_threshold`), G4 (`archetype_match_resolution`) tables with each subject's row populated.
8. **§5.2 worker JSON contract conformance (WORKER_JSON_CONTRACT_CONFORMANCE).** Every worker output validates against the §5.2 JSON schema. Missing required fields → subject marked `INCOMPLETE` and surfaced in run summary; never silently dropped.
9. **FR-9 unsuitable-subject refusal coverage.** Test fixtures for deceased, minor, and non-public-private-individual subjects all return `REFUSED` status with explanation. (Note: §10.2 also lists "witnesses in active litigation" as a refusal category — flag if this fourth category is uncovered.)
10. **FR-21 + FR-8 propose-only discipline.** Skill never auto-writes to `_bmad/custom/config.toml`, the canonical archetype store, or (without explicit user approval) the local archetype store. All writes pass through the Approval Gate.
11. **FR-24/FR-25/FR-26 model-tiering compliance.** Per-source extraction uses Haiku only (no Opus). Web searches route through Tavily MCP when configured. Run summary reports per-tier token spend with Opus <15% target.
12. **No doc-only architectural claims.** Same as tech-research's rule: any claim about a pipeline, service, or component without code-traced evidence is flagged `[UNVERIFIED — doc-only]` or removed. (Note: for this skill, the spec is forward-looking — claims sourced from spec text are tagged `[SPEC-AUTHORITATIVE]` rather than `[UNVERIFIED]`.)

The rf-qa agent's QA Gate also enforces section completeness, hallucinated-file-path detection, and content-rules compliance from S26.

---

## Assembly Process

This skill has TWO assembly contexts: (a) **skill-generation assembly** — how the SKILL.md document itself was incrementally constructed by skill-creator in Phase 4; and (b) **runtime assembly** — how the Aggregator combines per-worker outputs into the final per-run artifacts. Both follow the same incremental-Edit discipline (skill-creator Critical Rule 9 / tech-research Critical Rule 2): NEVER one-shot a large Write; always Write-then-append-via-Edit.

### 24.1 Skill-generation assembly (Phase 4, completed during this skill's birth)

Sequential 4-sub-phase incremental Edit pattern, NO one-shot Writes. Each sub-phase opens with a Write (creating or extending the file with frontmatter/header) and then uses repeated Edit calls to append section by section.

| Sub-phase | Sections | Operation | Verification |
|-----------|----------|-----------|--------------|
| 4.1 | Frontmatter + S1-S4 | Write (create file with frontmatter), then Edit-append S1, S2, S3, S4 individually | `wc -l` matches expected; no leftover `${DOMAIN_NAME}` template placeholders; YAML frontmatter parses |
| 4.2 | S5-S18 (Input through Stage A Output) | Edit-append S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, S16, S17, S18 individually | Each section header present; A.7 BUILD_REQUEST template is customized for persona-research (not the tech-research generic template) |
| 4.3 | S19-S20 (Stage B + Agent Prompt Templates) | Edit-append S19 (verbatim protocol blocks copied from tech-research) + S20 (6 domain agents + 6 lens QA + 3 source-fidelity prompts) | Incremental File Writing Protocol, Documentation Staleness Protocol, ADVERSARIAL STANCE, VERDICTS blocks present byte-verbatim from tech-research |
| 4.4 | S21-S29 (Output Structure through Quality Signals) | Edit-append S21, S22, S23, S24, S25, S26, S27, S28, S29 individually | §10.1 disclaimer present byte-verbatim ≥3 times across S25/S26/S27; FR-1 through FR-26 all referenced in S25; Rules 1-28 present in S27; section count exactly 29 |

After Sub-phase 4.4, the SKILL.md file is final-ready and Phase 5 lens-based QA gates are applied.

### 24.2 Runtime assembly (executed every time the skill runs)

When the skill is invoked on N subjects, the Aggregator component (per spec §5.1) runs after all workers complete and produces the final run output through the following ordered steps:

1. **Collect worker JSON contracts.** Read all per-subject worker outputs (one §5.2 JSON object per subject from archetype-driven workers; one §5.2 JSON + `discovered_archetype_proposal` from each discovery worker). Validate against the §5.2 schema. Subjects with missing required fields → marked `INCOMPLETE`.
2. **Compute Pipeline Quantity Flow counts.** Walk the §B stage diagram with actual numbers: N input → N' identity-verified → split P matched + Q no-match → P+Q workers run → M complete → K archetype proposals. Stage 1, 2, 4, 5, 7 divergence reasons populated from worker `status` and `warnings` fields.
3. **Emit Quantity Flow Diagram (FR-12 mandatory, ALWAYS emitted).** Render the Appendix B diagram with the computed counts. Even when N==M (no divergence), the diagram is emitted with all stages showing equal counts. This is non-negotiable — `[ ]` for emission would be a failure.
4. **Render Guard Boundary Tables (G1-G4 from Appendix A).** One row per subject per guard. G1 identity_verified, G2 subject_is_living_adult_public_figure, G3 public_footprint_above_threshold, G4 archetype_match_resolution.
5. **Aggregate per-subject persona TOML blocks.** For each subject with `status == OK`, take the worker's `persona_toml_block`, verify the §10.1 disclaimer is byte-prepended (FR-6 string-equality check, fail-closed if missing), verify no first-person attributed quotes (FR-7 static check), and stage the block in the unified config.toml diff.
6. **Generate unified config.toml diff (NEVER auto-written, FR-8).** One unified diff against `_bmad/custom/config.toml` covering all approved persona blocks. Diff is staged for the Approval Gate; the Aggregator NEVER writes it directly.
7. **Prepare archetype-store proposal write set (NEVER auto-written, FR-21).** For each `MATCH` + `refinement_mode==auto`, build a refinement descriptor (target archetype, version bump to N+1, deltas, retain old as `<id>.v<N>.yaml`). For each `NO_MATCH`, take the worker's `discovered_archetype_proposal` and validate FR-22 generic-purity (no firm/person/fund names in `display_name`/`persona_description_template`/`stable_traits`). All proposals target `archetype_store.local_path` ONLY — never the canonical store.
8. **Surface promotion candidates per §9.1.** Scan the local archetype store for candidates meeting the four criteria (`refined_from_subject_count >= 3`, no deltas for ≥30 days, `archetype_version >= 2`, not in canonical or materially newer). Emit each candidate's suggested copy command in the run summary.
9. **Compose run summary.** Includes: Quantity Flow Diagram, Guard Boundary Tables, per-subject persona summary, unified config.toml diff path, archetype proposal write set, promotion candidates, per-tier token spend report (FR-26, target Opus <15%), warnings list.
10. **Stage at Approval Gate.** Aggregator hands the staged write set to the user. NOTHING IS WRITTEN until the user explicitly approves each item. Approved persona blocks → unified diff. Approved archetype proposals → `local_path` only. Promotion to canonical is documented but never auto-executed (§9.1 manual workflow).
11. **(Optional) Trigger Validator if `--validate` passed.** Spawn each approved persona once with its three-questions test, score 0-10 fidelity, mark <7 as `NEEDS_REFINEMENT` (FR-14, §8.1).

The Aggregator follows the §5.4 Service-Boundary Rule: **it does not re-run worker reasoning**. It only consumes worker JSON and routes fields to artifacts. Cross-subject inference happens here (and only here), but it is mechanical aggregation, not model re-call.

---

## Validation Checklist

Before presenting a persona-research run output to the user (or, during skill-generation, before declaring the SKILL.md final), validate against this comprehensive checklist. Each item ties to a specific FR-N or to one of the 11 VALIDATION_REQUIREMENTS from BUILD-REQUEST.md.

This checklist is encoded into the task file's QA gates and applied by lens-based agents in Phase 5 + Phase 6.

### 25.1 §10.1 Ethics Disclaimer — VERBATIM (VALIDATION_REQUIREMENT ETHICS_DISCLAIMER_VERBATIM, FR-6)

The following string MUST appear byte-verbatim, prepended to every persona description, with no edits permitted. Em-dash MUST be U+2014 (`—`), NOT a hyphen-minus (`-`) or two hyphens (`--`). Apostrophe MUST be U+0027 (`'`), NOT U+2019 (`’`).

> Modeled on the public posture of [Name, Affiliation]. Captures observable patterns from public statements, conference appearances, and disclosed deal history; does not generate first-person quotes attributed to the real person. For internal pitch stress-testing only — not endorsed by, not affiliated with, and not a representation of the real individual's views.

The bracketed `[Name, Affiliation]` is a runtime placeholder substituted with the resolved subject's name and affiliation; all other characters are byte-immutable.

### 25.2 Per-FR Validation Items (FR-1 through FR-26)

- [ ] **FR-1** (multi-subject input): Skill rejects `len(subjects) == 0` with clear error; warns when N>10. Tested against zero-subject and 11-subject fixtures.
- [ ] **FR-2** (identity-first ordering): `identity_verified == true` for every subject before any research worker spawns for that subject. Sequential gate enforced by orchestrator.
- [ ] **FR-3** (parallel research workers): Three-subjects-in-parallel test completes within `3 × per_subject_minutes` ceiling. Workers launched in single message.
- [ ] **FR-4** (three artifacts per worker): Each worker emits dossier_markdown + persona_toml_block + three_questions. Output validated against §5.2 JSON schema; missing fields → `INCOMPLETE`.
- [ ] **FR-5** (source-cited claims): Every dossier claim has URL + retrieval ISO date. Reviewer can spot-check; no orphan claims.
- [ ] **FR-6** (verbatim disclaimer): String-equality check on the §25.1 disclaimer text passes for every persona description before write to disk.
- [ ] **FR-7** (no first-person quote fabrication): Static regex `grep -nE '\b[A-Z][a-z]+ (said\|stated\|wrote\|tweeted)\s+["“]'` finds no quoted strings preceded by attribution patterns; also `grep -nE '^[A-Z][a-z]+:\s*"'` finds no name-colon-quote patterns. Dynamic §8.4 fabrication probe passes.
- [ ] **FR-8** (diff, never auto-write): Skill produces unified diff against `_bmad/custom/config.toml`; never auto-writes. User explicitly approves before any modification.
- [ ] **FR-9** (refuse unsuitable subjects): Skill returns `REFUSED` for deceased, minor, and non-public-private-individual test fixtures. (Note: §10.2 also lists witnesses-in-active-litigation; flag if uncovered.)
- [ ] **FR-10** (halt on ambiguous identity): Subject with multiple plausible matches → halt with disambiguation prompt; no silent disambiguation.
- [ ] **FR-11** (INSUFFICIENT_PUBLIC_DATA sentinel): Subject with `footprint_score < 3` → returns sentinel; surfaced in summary; nothing fabricated to fill the gap.
- [ ] **FR-12** (Quantity Flow Diagram emitted): Run summary contains Appendix B diagram with actual N/N'/P/Q/M/K counts. Always emitted, even when N==M. (VALIDATION_REQUIREMENT PIPELINE_QUANTITY_FLOW_DIAGRAM_PRESENT)
- [ ] **FR-13** (dossier caching): Re-run within 24h uses cached dossier. Cache invalidated on context_artifact change. Stale cache (>90 days) flagged.
- [ ] **FR-14** (--validate spawns persona): With `--validate` flag, each persona run through three-questions test; fidelity 0-10 reported; <7 marked `NEEDS_REFINEMENT`.
- [ ] **FR-15** (companion archetype default): Both generic archetype persona (`board-polly`) and named-modeled persona (`board-rosenthal-mod`) coexist in roster when `archetype_companion: true`.
- [ ] **FR-16** (archetype resolution gate): Every subject scored against canonical+local archetype roster before research; result one of `MATCH`/`AMBIGUOUS`/`NO_MATCH` per §F algorithm.
- [ ] **FR-17** (archetype-driven worker invocation): On `MATCH`, worker invocation includes `archetype_id`, uses matched archetype's `source_recipe` + `slot_schema` + `persona_description_template` + `three_questions_template`. Worker output references the archetype.
- [ ] **FR-18** (NO_MATCH discovery worker): On `NO_MATCH`, discovery worker spawned with longer budget (`archetype_discovery_minutes`). Emits BOTH dossier AND proposed archetype.yaml.
- [ ] **FR-19** (archetype refinement on MATCH): On `MATCH` + `refinement_mode==auto`, archetype version increments; `refinement_log` appended; old version retained as `<id>.v<N>.yaml`.
- [ ] **FR-20** (halt on AMBIGUOUS archetype): Top-K matches surfaced with scores; user disambiguates; no silent selection in ambiguity band.
- [ ] **FR-21** (no auto-save to global store): All new/refined archetypes await explicit user approval. Default behavior is propose-then-approve.
- [ ] **FR-22** (generic archetypes — no person/firm names): Static linter rejects any archetype whose `display_name`, `persona_description_template`, or `stable_traits` contains a specific firm/person/fund name. `affiliation_keywords` is the SOLE allowed exception. (VALIDATION_REQUIREMENT ARCHETYPE_GENERIC_PURITY)
- [ ] **FR-23** (portable store format): Archetype store is a directory of YAML files only. No SQLite, no proprietary index. Copy-to-fresh-machine test produces identical match scores.
- [ ] **FR-24** (no Opus per-source): Static check confirms budget allocator caps Opus token spend at consolidation step ONLY; per-source extraction uses Haiku.
- [ ] **FR-25** (Tavily MCP routing): When Tavily is configured, every general web search invokes `tavily_search` rather than direct fetch. Fallback only on Tavily unavailable or sources Tavily can't reach (PACER, on-chain via own APIs).
- [ ] **FR-26** (token-spend reporting): Run summary reports per-tier token spend; Opus <15% target. Per-subject worker shape: ~50–100 Haiku calls + 1–2 Opus calls per 12-min subject.

### 25.3 VALIDATION_REQUIREMENTS Coverage (11 items per BUILD-REQUEST.md)

- [ ] **TEMPLATE_COMPLIANCE**: All 29 canonical sections present in correct ordering (per tech-research/SKILL.md as canonical reference). All sections (S1-S29) use plain descriptive `## ` headers per the tech-research convention — no `## N.` numbered prefixes appear in the live document body. The 29-section logical mapping is canonical in §21.1 (inside a fenced code block as a reference schema). Section count check: `grep -cE '^## [0-9]+\. ' SKILL.md` should return 0 in the live document body (the §21.1 fenced schema lists numbered logical sections but those are inside a code fence and are not live headers); `grep -c '^## ' SKILL.md` should return ≥29 for live `## ` headers (which include §-prefixed canonical sections plus any descriptive subheaders).
- [ ] **EVIDENCE_TRAIL**: Every section in this SKILL.md cites the spec FR / section it satisfies or the domain-model field it depends on. Reviewer can trace every claim.
- [ ] **CROSS_VALIDATION**: COPY-classified sections byte-match tech-research's equivalents. SUBSTITUTE-classified sections contain no leftover tech-research / skill-creator / prd / tdd domain nouns.
- [ ] **ETHICS_DISCLAIMER_VERBATIM**: §10.1 disclaimer string (see §25.1 above) appears byte-verbatim at exactly these locations in this SKILL.md (≥3 occurrences enforced): §25.1 (around line 1616), §26.1 (around line 1710), §27 Rule 23 (around line 1782). Verification: `grep -nF "Modeled on the public posture of [Name, Affiliation]" SKILL.md` should return ≥3 matches with byte-identical text. The runtime FR-6 string-equality check enforces the same disclaimer in every produced persona description.
- [ ] **NO_FIRST_PERSON_ATTRIBUTION**: SKILL.md describes both static checks (regex `grep -nE '\b[A-Z][a-z]+ (said\|stated\|wrote\|tweeted)\s+["“]'` and `grep -nE '^[A-Z][a-z]+:\s*"'`) and dynamic checks (§8.4 fabrication probe) enforcing FR-7. S20 worker prompts include the prohibition.
- [ ] **ARCHETYPE_GENERIC_PURITY**: SKILL.md describes the FR-22 linter check covering `display_name`, `persona_description_template`, and `stable_traits` fields. `identity_signals.affiliation_keywords` is named as the SOLE exception. The runnable grep rule list is encoded in the Discovery Worker prompt (S20, "CRITICAL — Generic-Purity Guarantee (FR-22)" block, including the four mandatory grep targets: subject's name, subject's firm name full string, subject's fund name, any URL containing the firm domain) — see S20 Discovery Worker prompt lines covering the linter check.
- [ ] **IDENTITY_VERIFIED_BEFORE_RESEARCH**: SKILL.md encodes FR-2's sequential gate. S20 orchestrator prompt + the Identity Verifier agent prompt both state: research worker SHALL NOT spawn until `identity_verified == true` for that subject.
- [ ] **WORKER_JSON_CONTRACT_CONFORMANCE**: S20 Agent Prompt Templates include the exact §5.2 JSON contract structure for both archetype-driven and discovery worker outputs. Worker output validated against schema before Aggregator consumes.
- [ ] **PIPELINE_QUANTITY_FLOW_DIAGRAM_PRESENT**: SKILL.md instructs runtime emission of Appendix B diagram on every run per FR-12 (S21, S24). Always emitted, even when N==M.
- [ ] **GUARD_BOUNDARY_TABLE_PRESENT**: SKILL.md instructs runtime emission of Appendix A guard tables (G1-G4) on every run.
- [ ] **SECTION_COUNT_29**: This SKILL.md follows the canonical 29-section RF schema (S1-S29). All sections (S1-S29) use plain descriptive `## ` headers per the tech-research convention (e.g., `## Input`, `## Depth Tiers`, `## Output Structure`, `## Validation Checklist`, `## Critical Rules`). No `## N.` numbered prefixes appear as live headers. The 29-section logical structure is the authoritative mapping in §21.1 of this document (inside a fenced code block as a reference schema, not as live headers) and in `${TASK_DIR}research/12-section-classification.md`. Section count check: `grep -c '^## ' SKILL.md` should return ≥29 live `## ` headers; cross-reference each header against the §21.1 logical schema and the section classification table. Numbered-prefix check: `grep -cE '^## [0-9]+\. ' SKILL.md` should return 0 in the live document body (the §21.1 fenced code block contains numbered logical-section labels, but those are inside a fenced block and represent the logical mapping, not live headers — note that grep does not honor code fences, so any non-zero count must be inspected to confirm matches are inside the §21.1 fence).

### 25.4 Byte-Fidelity Spot Check on the Disclaimer

- [ ] **Em-dash byte check**: Hex-dump the disclaimer line and confirm the dash between "stress-testing only" and "not endorsed by" is `0xE2 0x80 0x94` (U+2014 UTF-8). NOT `0x2D` (hyphen-minus) and NOT `0x2D 0x2D` (double hyphen).
- [ ] **Apostrophe byte check**: Hex-dump the disclaimer's "individual's" — the apostrophe MUST be `0x27` (ASCII straight, U+0027), NOT `0xE2 0x80 0x99` (U+2019 right single quotation mark).
- [ ] **Hyphen in "stress-testing"**: ASCII hyphen-minus `0x2D` (U+002D) — NOT em-dash, NOT en-dash.
- [ ] **Sentence terminators**: Two periods total — one after "real person." and one after "real individual's views.".
- [ ] **No internal line breaks** in the disclaimer (it is a single logical line; markdown line-wrapping for display is allowed but the source string contains no `\n`).

### 25.5 Spec §11 Acceptance Criteria (15 items, traceability)

- [ ] §11 #1: FR-1 through FR-23 all pass (bundled — see per-FR items in §25.2).
- [ ] §11 #2: All five Whittaker probes (§7) verified by red-team test cases.
- [ ] §11 #3: §10.1 disclaimer appears verbatim in every produced persona description (covered by FR-6 and §25.1).
- [ ] §11 #4: Validator achieves ≥7/10 fidelity on a held-out test subject.
- [ ] §11 #5: Three-subjects-in-parallel test completes within `3 × per_subject_minutes` (covered by FR-3).
- [ ] §11 #6: Skill refuses on deceased-subject and minor-subject test fixtures (covered by FR-9).
- [ ] §11 #7: Skill emits non-empty Quantity Flow Diagram and Guard Boundary Table on every run.
- [ ] §11 #8: Archetype lifecycle test — first run produces dossier + proposed archetype; second run on matching subject reuses with refinement; third run is cache hit.
- [ ] §11 #9: Archetype generic-purity linter rejects person/fund/company names in core fields (covered by FR-22).
- [ ] §11 #10: Archetype portability test — copy store directory to fresh machine, identical match scores (covered by FR-23).
- [ ] §11 #11: Approval-gate test — skill never modifies local store or roster file without explicit approval; canonical store never written at runtime.
- [ ] §11 #12: Model-tiering test — Opus <15% of total tokens in typical per-subject worker run (covered by FR-24/FR-26).
- [ ] §11 #13: Tavily routing test — `tavily_search` invoked rather than direct fetch when configured (covered by FR-25).
- [ ] §11 #14: Two-layer store test — local v3 overrides canonical v1; run summary notes the override.
- [ ] §11 #15: Promotion-candidate test — local archetype refined from 3 subjects, stable >30 days, version >= 2 → appears in run summary's promotion-candidates list with suggested copy command.

---

## Content Rules (Non-Negotiable)

These rules govern how content is written within research files, dossiers, persona TOML blocks, archetype YAML proposals, and the run summary. They prevent bloat, ensure consistency, and — for this skill specifically — enforce the spec §10 ethics floor and FR-7/FR-22 guardrails.

| # | Rule | Do | Don't |
|---|------|-----|-------|
| 1 | **Source code** | Summarize behavior in tables and prose with key signatures | Reproduce full function bodies, interfaces, config files, or YAML blocks |
| 2 | **Architecture** | Use tables and ASCII diagrams | Multi-paragraph prose for what could be a table row |
| 3 | **Comparisons** | Use comparison tables with clear criteria | Prose-based side-by-side descriptions |
| 4 | **Evidence** | Inline citations: `file.md:123`, source URLs, retrieval ISO dates, archetype IDs | "The dossier says X" without pointing to where |
| 5 | **Tags for claim provenance** | Tag every claim as `[CODE-VERIFIED]`, `[SPEC-AUTHORITATIVE]`, or `[UNVERIFIED — doc-only]`. **Exception:** an inline parenthetical citation of the form `(FR-N)` or `(per FR-N)` already conveys `[SPEC-AUTHORITATIVE]` provenance for that FR-derived claim and does NOT require a redundant `[SPEC-FR-N]` tag. Tags remain mandatory for claims sourced from non-spec docs. | Present uncertain findings as verified facts |
| 6 | **Don't fabricate** | Mark gaps explicitly: `INSUFFICIENT_PUBLIC_DATA`, `NEEDS_REFINEMENT`, `[UNVERIFIED]` | Invent details to fill gaps. Speculation is a hard fail. |
| 7 | **No first-person attributed quotes (FR-7)** | Speak in patterns: "a partner with this profile would push back here" | Generate invented direct speech: "Josh would say…" or `<Name>: "..."`. Static check + dynamic §8.4 fabrication probe enforces this. |
| 8 | **Source-cite every dossier claim (FR-5)** | Every claim has URL + retrieval ISO date | Orphan claims with no source. Reviewer must be able to spot-check by clicking through. |
| 9 | **Archetype generic-purity (FR-22)** | Archetype `display_name`, `persona_description_template`, and `stable_traits` are abstract patterns ("Crypto-Native Venture Investor", "reads pitches through token-economics lens") | Mention any specific firm/person/fund name in those fields. `identity_signals.affiliation_keywords` is the SOLE allowed location for firm names (as match examples, not as the archetype identity). |
| 10 | **§10.1 disclaimer byte-verbatim, no edits permitted (FR-6)** | Prepend the EXACT disclaimer string below to every persona description; em-dash U+2014, apostrophe U+0027 | Edit, paraphrase, abbreviate, or "fix typos" in the disclaimer. The string-equality check fails the run if a single byte drifts. |

### 26.1 The §10.1 disclaimer (verbatim, must appear prepended to every persona description)

> Modeled on the public posture of [Name, Affiliation]. Captures observable patterns from public statements, conference appearances, and disclosed deal history; does not generate first-person quotes attributed to the real person. For internal pitch stress-testing only — not endorsed by, not affiliated with, and not a representation of the real individual's views.

The bracketed `[Name, Affiliation]` is substituted at runtime with the resolved subject's name and affiliation; all other characters MUST remain byte-immutable. A single drifted character (em-dash → hyphen, straight apostrophe → curly apostrophe, missing comma) fails the FR-6 string-equality check and aborts the write to disk.

### 26.2 Refusal language for unsuitable subjects (§10.2)

When the skill refuses a subject (deceased, minor, non-public private individual, witness in active litigation), the refusal message MUST:
- Name which guard tripped (G2 subject_is_living_adult_public_figure)
- Cite the §10.2 category that applies
- NOT include speculation about why the subject might fall in that category
- NOT proceed to research stages even if the user attempts to override (no `--force` for ethics refusals)

### 26.3 General content principles

- Tables over prose whenever presenting multi-item data (subjects, FRs, archetypes, sources, guards).
- Conciseness over comprehensiveness — the report should be scannable, not exhaustive prose.
- Every claim needs evidence — if you can't cite a file path, URL, or spec FR, it belongs in Open Questions or `[UNVERIFIED]`.
- Prefer ASCII diagrams (Appendix B Quantity Flow style) for visual relationships over paragraph descriptions.
- For persona TOML blocks: stable traits go in patterns, not in invented dialogue. The persona is a *posture model*, not a ventriloquized voice.

---

## Critical Rules

These rules apply across ALL phases of skill execution and ALL phases of skill generation. Violations compromise output quality, ethical compliance, or both. Rules 1-9 are universal protocol (boilerplate from tech-research / skill-creator); Rules 10-22 are persona-research runtime template-discipline rules covering execution loop, QA gates, incremental writing, contract enforcement, and audit-trail emission; Rules 23-28 are persona-research domain rules.

**Rule 1 — Task file is the source of truth.** Never work from memory of prior state. Always read the task file before acting. Progress is tracked by checked/unchecked items on disk.

**Rule 2 — Incremental writing is mandatory — ZERO TOLERANCE.** Every agent's FIRST ACTION must be creating its output file on disk using Write (frontmatter/header only). All subsequent content is appended using Edit, one section at a time. NEVER accumulate content in context and attempt a single large Write — this is the #1 failure mode across all agents. The procedure is: Write (create file with header) → Edit (append section 1) → Edit (append section 2) → ... → Edit (update Status to Complete).

**Rule 3 — Maximize parallelism (MANDATORY).** For Phases 3, 4, and 7, you MUST spawn all independent agents in each batch in parallel using multiple Agent tool calls in a single message (Phase 3 archetype resolution per subject, Phase 4 research workers per subject, Phase 7 Validator per persona). The only sequential requirements in this skill are: Phase 2 Identity Verification (sequential per subject — FR-2 hard gate before any Phase 4 worker spawns); Phase 5 Aggregator (single-instance, runs after all Phase 4 workers complete); Phase 6 Approval Gate (HARD HALT for user decision, never parallelizable); QA fix-cycles (each cycle waits for predecessor's report). Otherwise, parallel-by-default.

**Rule 4 — Codebase / spec is source of truth.** Web research supplements but never overrides spec or verified code findings. For this skill, the persona-research-skill-spec.md is forward-looking specification — it IS authoritative for what to build, even when no code exists yet. Internal documentation about non-spec topics is treated with the same skepticism as external sources unless code-verified.

**Rule 5 — Evidence-based claims only.** Every finding must cite spec line numbers, FR-IDs, or actual file paths. No assumptions, no inferences, no guessing. If you can't verify it, mark it as `[UNVERIFIED — needs confirmation]`.

**Rule 6 — Default to Deep tier for skill-generation.** This skill was generated at Deep tier; runtime persona-research can run at Quick/Standard/Deep per user choice but Deep is the recommended default for any pitch-stakes use case.

**Rule 7 — No one-shotting reports or skills.** Agents must write incrementally as they discover information. The orchestrator must write the final SKILL.md or run summary section by section. This is non-negotiable.

**Rule 8 — Use dedicated tools.** Use Glob for file search, Grep for content search, Read for file reading, codebase-retrieval for semantic code search. Do NOT use bash `find`, `grep`, `cat`, `head`, `tail`, `rg`, or `awk` commands for these operations. (Bash for `wc -l` and other non-search operations is fine.)

**Rule 9 — Preserve research artifacts.** Research files, synthesis files, dossiers, archetype proposals, and gap logs persist after assembly. They serve as the evidence trail for all claims and enable future re-investigation without starting from scratch. Do NOT delete artifacts.

**Rule 10 — Template fidelity.** When a section is classified COPY, byte-match the source (tech-research SKILL.md). When classified SUBSTITUTE, replace ONLY domain nouns with persona-research equivalents — preserve all structural scaffolding. When classified GENERATE, the section is net-new from spec evidence; cite the spec FR or section it satisfies.

**Rule 11 — Skill is not consulted during Stage B execution.** The skill (sc-persona-research-protocol) is consulted ONLY during Stage A (task file generation). Once the MDTM task file is built, every checklist item in the task file is self-contained: agents executing the task file MUST NOT read SKILL.md. All required context (full §5.2 worker contract JSON schema, full §10.1 disclaimer text, full FR list, refusal language, archetype generic-purity rules) is embedded directly in each item's prompt per Rule 20. Reading SKILL.md mid-execution is a violation — it indicates an under-specified task item that must be regenerated rather than papered over at runtime.

**Rule 12 — Phase boundaries are mandatory QA checkpoints.** After completing all items in a phase, phase-gate QA MUST run and PASS before the first item of the next phase is executed. The 7-phase structure (1 Identity Verify → 2 Sequential Identity Gate → 3 Archetype Resolve → 4 Parallel Workers → 5 Aggregator → 6 Approval Gate → 7 Optional Validator) is a sequence of hard gates, not a continuous flow. A phase that fails its gate cannot be bypassed; the orchestrator must spawn fix-cycle agents (max 3 cycles per gate) and only proceed when the gate verdict is PASS.

**Rule 13 — Incremental File Writing Protocol applies to ALL file creations.** Every file produced by this skill (research analyses, dossiers, archetype proposals, synthesis files, persona TOML blocks, approval records, run summary, SKILL.md itself during authoring) MUST follow the protocol: Write header/frontmatter first, append sections via Edit, mark Status: Complete only at the end. Never accumulate full content in context for a single large Write call — this is the #1 failure mode (token-output ceiling, context rot, fabrication). Rule 2 states this for agent outputs; Rule 13 extends it without exception to every file in the persona-research output directory.

**Rule 14 — Frontmatter is YAML-valid.** The skill's frontmatter (`name`, `description`, `allowed-tools`) must parse as valid YAML. No leftover `${DOMAIN_NAME}` template placeholders.

**Rule 15 — Variable Reference uses TASK_ID_PREFIX consistently.** All `.dev/tasks/` paths in this skill use `TASK-PERSONARES` as the prefix. No leakage of `TASK-RESEARCH`, `TASK-SKILLCREATE`, etc., from copied templates.

**Rule 16 — §5.2 worker contract is the load-bearing schema.** Every research worker (Identity Verifier, Archetype Discovery/Match worker, per-subject Research Worker) MUST emit output conforming to the §5.2 Worker JSON Contract with all 14 required fields populated. Use `null` for non-applicable fields (e.g., `archetype_resolution.proposed_archetype_path: null` when `match_path == MATCH`); never omit a field. Aggregator (Phase 5) rejects any worker output missing a required key with `status: SCHEMA_VIOLATION` and either re-spawns the worker (cycle ≤2) or marks the subject `INCOMPLETE` in the run summary's per-subject table. Schema enforcement runs both at worker emission and at Aggregator ingestion (defense in depth).

**Rule 17 — §A guard-condition boundary tables (G1-G4) MUST be emitted on every run.** The four guard tables (G1 identity_verified, G2 subject_is_living_adult_public_figure, G3 archetype_match_quality, G4 footprint_score_threshold) are the audit trail for every refusal-vs-continue decision. They are emitted regardless of outcome — runs that proceed cleanly still produce all four tables (with all rows showing `pass`). Empty or omitted guard tables are an FR-12 audit-trail violation. The run summary's "Guard Boundary Tables" section is non-optional, even on `--quick` tier.

**Rule 18 — §B Quantity Flow Diagram MUST be emitted on every run, even when N==M.** The Quantity Flow Diagram (per FR-12) reports N (subjects requested) → N' (post-G1 identity-verified) → P (post-G2 ethics-passed) → Q (post-G3 archetype-resolved) → M (workers spawned) → K (dossiers complete). It is required even when no losses occur (N == N' == P == Q == M == K). A run that omits the diagram on grounds of "nothing to report" is an FR-12 violation; the diagram with all-equal counts is itself the affirmative audit signal that no subject was silently dropped.

**Rule 19 — Cross-reference findings.** When one agent's findings reference another agent's domain, note the cross-reference explicitly. Spec analyst Part 1 references Part 3 ethics; cross-references are tracked in each research file's "Cross-Slice References" section.

**Rule 20 — Implementation plans must be actionable.** S20 Agent Prompt Templates include enough detail (full §5.2 JSON schema, full §10.1 disclaimer text, full FR list) that downstream sub-agents can be invoked from a single prompt without out-of-band context.

**Rule 21 — Report all uncertainty.** Open Questions OQ-1 through OQ-9 from spec §12 are surfaced in the run summary or the SKILL.md's "Future Work" notes. Don't silently pick one interpretation and present it as fact.

**Rule 22 — Documentation is not verification (in general).** Internal documentation (design docs, integration guides, READMEs) describes intent or planned state — NOT necessarily current state. For the persona-research skill, the spec is forward-looking, so spec text is `[SPEC-AUTHORITATIVE]` rather than `[CODE-VERIFIED]`. But once code is written, the same trust hierarchy applies: code > spec > docs.

**Rule 23 — Ethics disclaimer §10.1 is non-negotiable and byte-verbatim (FR-6).** The following string is prepended to every persona description; the FR-6 string-equality check fails the run if a single byte drifts.

> Modeled on the public posture of [Name, Affiliation]. Captures observable patterns from public statements, conference appearances, and disclosed deal history; does not generate first-person quotes attributed to the real person. For internal pitch stress-testing only — not endorsed by, not affiliated with, and not a representation of the real individual's views.

Em-dash MUST be U+2014. Apostrophe MUST be U+0027. The bracketed `[Name, Affiliation]` is the only runtime substitution. All other characters are byte-immutable.

**Rule 24 — Identity verification is a sequential gate (FR-2).** No research worker may spawn for a subject before the Identity Verifier completes for that subject and emits `identity_verified == true`. The orchestrator MUST enforce this structurally: identity verification runs FIRST for every subject (sequential per subject), and only after all subjects are verified does the parallel worker batch launch in a single message. Guard G1 enforces this. Violations are §7 FR-2.4 Sequence Attack failures.

**Rule 25 — No first-person attributed quotes (FR-7) — static check on every worker output.** Worker dossiers and persona descriptions MUST NOT contain quoted strings preceded by attribution patterns. Aggregator runs the concrete static regex `grep -nE '\b[A-Z][a-z]+ (said\|stated\|wrote\|tweeted)\s+["“]'` (catching `Josh said "..."`, `Rosenthal stated "..."`, etc.) and `grep -nE '^[A-Z][a-z]+:\s*"'` (catching `Josh: "..."` patterns) before persona TOML blocks are staged in the unified diff. Dynamic enforcement: §8.4 fabrication probe (Validator presents a leading question about an undocumented topic; faithful persona hedges, fabricating persona invents — fabrication = failure).

**Rule 26 — Archetype generic-purity (FR-22) — proposed archetype.yaml core fields contain NO person/firm/fund names.** The static linter rejects any archetype whose `display_name`, `persona_description_template`, or `stable_traits` mentions any specific firm/person/fund. The `identity_signals.affiliation_keywords` field is the SOLE allowed exception (it's an example list for the matcher, not the archetype's identity). Discovery worker output that would propose `display_name: "Polychain-style VC"` is rejected; correct form is `display_name: "Crypto-Native Venture Investor"` with `affiliation_keywords: [polychain, paradigm, ...]`.

**Rule 27 — Tavily-routing mandate (FR-25).** All public-source web searches go through Tavily MCP when configured. Direct fetch is fallback only — for sources Tavily can't reach (PACER queries, on-chain block explorers via own APIs) or when Tavily is unavailable. Per-source Haiku extraction processes Tavily results; Opus is reserved for cross-source consolidation.

**Rule 28 — Opus-spend cap via model tiering (FR-24 + FR-26).** Per-source extraction MUST use Haiku (`claude-haiku-4-5-20251001`); Opus (`claude-opus-4-7`) is reserved for cross-source consolidation, persona description generation, and archetype proposal/refinement synthesis. Run summary reports per-tier token spend; target Opus <15% of total. Static check: budget allocator caps Opus token spend per worker at the consolidation step ONLY. Per-worker shape: ~50-100 Haiku calls + 1-2 Opus calls per 12-min subject.

---

### Generation-Time Invariants (informational, not runtime rules)

The following invariants describe how this SKILL.md was BUILT (via skill-creator authoring), NOT how it executes at runtime. They are preserved here for traceability and for future re-authoring or extension of this skill, but they do NOT govern runtime persona-research execution. A runtime persona-research run does not consult these invariants.

**Generation-Invariant G-11 — COPY/SUBSTITUTE/GENERATE discipline (skill-creator authoring).** Every section in this SKILL.md was authored under a documented COPY/SUBSTITUTE/GENERATE classification (see `${TASK_DIR}research/12-section-classification.md` produced by skill-creator's Phase 2d). A section presented as COPY but with non-trivial content drift was treated as a violation during authoring. A SUBSTITUTE section with leftover tech-research / prd / tdd domain nouns was treated as a violation during authoring.

**Generation-Invariant G-12 — Canonical 29-section schema (skill-creator authoring).** The canonical RF skill schema has 29 logical sections (S1-S29). The skill-creator validator rejects skipped, merged, or duplicated logical sections. Cross-reference `${TASK_DIR}research/12-section-classification.md` and §21.1 above for the canonical mapping.

**Generation-Invariant G-13 — Reference skill paths existed at authoring time (skill-creator authoring).** When this SKILL.md was generated, `tech-research/SKILL.md`, `skill-creator/SKILL.md`, `task-builder/SKILL.md`, `prd/SKILL.md`, and `tdd/SKILL.md` were present in `.dev/releases/current/`. If you re-author this skill and any reference is missing, halt and surface the gap before spawning agents.

**Generation-Invariant G-16 — Verbatim protocol blocks at authoring time (skill-creator authoring).** During authoring, S19 Stage B was required to contain the Incremental File Writing Protocol, Documentation Staleness Protocol, ADVERSARIAL STANCE, and VERDICTS blocks byte-verbatim from tech-research. These blocks have been hardened across many runs; do not edit them when re-authoring.

**Generation-Invariant G-17 — A.7 BUILD_REQUEST template was domain-customized at authoring time (skill-creator authoring).** S18 (A.7) embeds a BUILD_REQUEST template. The skill-creator generic template's phase mapping was replaced during authoring with the persona-research-specific 7-phase structure (identity verify → archetype resolve → parallel workers → aggregator → approval gate → optional validator → run summary).

**Generation-Invariant G-18 — Spec partitioning during authoring (skill-creator authoring).** When this SKILL.md was authored, the persona-research-skill-spec.md (993 lines) combined with the 2088-line developer guide exceeded skill-creator's partitioning threshold; skill-creator's Phase 2b spawned 3 spec analyst agents (Part 1, Part 2, Part 3) and Phase 2c spawned 2 guide analyst agents. Single-agent reads of >1000 lines cause context rot and fabrication during authoring; this invariant applies to re-authoring or extending this skill, not to runtime persona-research execution.

---

## Session Management

This work may span multiple sessions. The task file and persona-research output directory serve as the persistent record.

**At session start:**
1. Check for existing task folder in `.dev/tasks/to-do/TASK-PERSONARES-*/`
2. If found, read the task file inside it and resume from the first unchecked `- [ ]` item
3. Read existing research, qa, dossiers, archetype-proposals, and reviews subfolders for context
4. Read the gaps-and-questions file if it exists
5. Read any partial run summary, dossier, or archetype proposal
6. Do not re-research completed subjects — cache layer (FR-13) handles within-TTL re-runs; explicit `--force` bypasses cache

**At session end:**
- All research files should have Status: Complete
- The task file should reflect exactly which items are checked and unchecked
- If aggregation is in progress, note which dossiers are complete and which archetype proposals are staged
- The user should know the current state (which phase, which step, which subjects pending Approval Gate)

**Subfolders within `.dev/tasks/to-do/TASK-PERSONARES-<slug>/`:**
- `research/` — per-spec-partition analysis files (Part 1, Part 2, Part 3) + reference-skill analyses
- `qa/` — lens-based QA reports (template-conformance, internal-consistency, evidence-quality, actionability, domain-accuracy, section-classification-accuracy)
- `dossiers/` — per-subject evidence dossiers (markdown, ~500 words each, source-cited)
- `archetype-proposals/` — proposed new archetype YAMLs (from discovery workers) + proposed refinement deltas (from MATCH + auto refinement_mode)
- `synthesis/` — Aggregator (Phase 5) cross-subject synthesis: unified diff, archetype-proposal manifest, contradiction tables, run summary draft
- `personas/` — Per-subject persona TOML blocks (with §10.1 disclaimer prepended) staged for Approval Gate (Phase 6)
- `approvals/` — Approval Gate (Phase 6) decision records: user choices on each archetype proposal/refinement, write-target paths, post-approval staging artifacts
- `reviews/` — three-questions test files + validation reports (when `--validate` passed)

---

## Research Quality Signals

### Strong Investigation Signals

- Every dossier claim has URL + retrieval ISO date (FR-5 satisfied)
- Archetype proposal core fields contain NO firm names, person names, or fund names (FR-22 satisfied — `display_name: "Crypto-Native Venture Investor"`, NOT `display_name: "Polychain-style VC"`)
- `footprint_score >= 0.7` (or scaled equivalent ≥ 7 on 0-10 scale) indicates substantive public surface
- ≥3 source diversity per subject — at minimum: interviews (audio/video), conference talks, regulatory filings, on-chain or deal-history (when archetype calls for it)
- §10.1 disclaimer byte-verbatim prepended to every persona description (FR-6 string-equality passes)
- No first-person attributed quotes — static check + §8.4 fabrication probe both pass (FR-7)
- Worker JSON contracts validate against §5.2 schema with no missing required fields (every subject `OK`, no `INCOMPLETE`)
- Archetype-driven workers cite `from_archetype_recipe: true` for sources discovered via the matched archetype's recipe (proves recipe-driven research is happening)
- Quantity Flow Diagram populated with actual N/N'/P/Q/M/K counts; Guard tables G1-G4 have a row per subject

### Weak Investigation Signals (Redo)

- `stable_traits` listed without source citations or evidence anchors (claims without citation = orphan claims)
- Subject claim with no source URL or retrieval date (FR-5 violation)
- Archetype proposal containing 'Polychain', 'Paradigm', 'a16z', or any other firm/person/fund name in `display_name`, `persona_description_template`, or `stable_traits` (FR-22 violation)
- Persona description containing patterns like `Josh said "..."` or `Rosenthal: "..."` (FR-7 violation — first-person attribution)
- Em-dash drift in disclaimer (`-` or `--` instead of `—`) — FR-6 byte-equality fails
- Footprint score high but dossier sourced from <3 source categories (single-source bias)
- Worker output with `status: OK` but missing `identity_verification.canonical_url` or `archetype_resolution.match_path` (schema violation)
- Discovery worker proposing an archetype near-duplicate of existing (`identity_signals` overlap >0.85 with existing — should refine instead, per §6 row 382)
- `[UNVERIFIED]` claims with no follow-up plan (left as orphan in run summary)

### When to Spawn Additional Agents

- **Spawn additional Discovery Worker** when `footprint_score < 0.5` (or <5 on 0-10 scale) for a subject — the initial worker found insufficient public surface; broaden source sweep with longer budget per `archetype_discovery_minutes`
- **Spawn additional Archetype Discovery** when no existing archetype's `slot_binding` match score > 0.6 against the subject — none of the canonical or local archetypes are a good fit; need a new archetype proposal
- **Spawn second Identity Verifier** when initial verification returns >1 plausible match in the ambiguity band — not a halt-on-AMBIGUOUS case necessarily, but a sanity check before proceeding
- **Spawn Validator on a held-out test subject** when fidelity scores on the production subjects look suspiciously high (validator must mirror runtime conditions per §9.2; held-out test ensures the score isn't gameable)
- **Spawn a fresh research run after >90 days** even on cache-hit subjects — dossiers older than 90 days are flagged `STALE` per §6 row 373; user can force a refresh
- **Spawn a tie-breaker investigation** when two agents' findings contradict each other (e.g., one analyst says the subject is crypto-VC, another says traditional VC) — need a third opinion
- **Spawn additional spec re-read** when a generated section's classification (COPY/SUBSTITUTE/GENERATE) is contested — the Section Classifier agent re-reads with the contested context

The skill is designed to fail-loud (refuse, halt, surface) rather than fail-silent. If a quality signal is weak and not addressed via an additional agent spawn or explicit `[UNVERIFIED]` tag, it is a Critical Rule 5 violation (evidence-based claims only).
