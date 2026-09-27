---
template_name: "Component Authoring"
template_version: "1.0.0"
sections: 6
placeholder_prefix: "RF_PLACEHOLDER"
# --- Modularization fields (template-side, per map §0(d) as ratified) ---
spec_id: ""
# ^ infra template created at the D10 ratification (2026-06-10); SPEC assignment lands at the T0.INFRA leaves
externalize_status: "SHARED"
component_type: "template"
consumers:
- "track-0-family-task-files"
- "skill-creator"
- "agent-creator"
# ^ every Track-0 component-authoring task copies this scaffold; Track-3 generators consume it when emitting new components
---

# Component Authoring Template

**Origin:** created 2026-06-10 at the D10 ratification. Authoritative sources: `.dev/plans/RATIFICATION-component-template-20260610.md` (frontmatter schema section 2; skeleton amendments section 5a) and the skeleton-validation synthesis (`.dev/tasks/to-do/skills-modularization-20260608/skeleton-validation/SKELETON-VALIDATION-SYNTHESIS.md`). Where this file and the extraction map's §0 differ, THIS FILE wins (the map §0 is the historical proposal; this is the ratified operative scaffold).

**What this is:** the scaffold every IronFlow COMPONENT file follows. Copy PART 2, fill it, and obey PART 1 while filling. Components are READ (process/instruction content consumed by reference or baked); if you are producing a scaffold that gets FILLED to create artifacts, you are writing a TEMPLATE, not a component: stop and use the template-side convention instead (ratification spec section 6).

<!--
################################################################################
##  PART 1: AUTHORING INSTRUCTIONS (for the component author; never copied   ##
##  into the output component file)                                          ##
################################################################################

A. AUTHOR FROM LIVE LINES (ratified amendment 6; Track-0 acceptance criterion).
   The extraction map's §2 record gives you ROUTING: which units contribute,
   their live line ranges, the consumer set, the SPEC id. Its prose summaries
   of CONTENT are hints only: multiple glosses were verified CODE-CONTRADICTED.
   Re-read every contributing instance at its LIVE line range before writing a
   single line of the Universal Core. Never transcribe map glosses.

B. BEST-OF-BEST SYNTHESIS (map §0(c), ratified unchanged).
   1. Read EVERY contributing instance in full first.
   2. Enumerate all distinct rules/steps/principles across instances.
   3. Per rule: take the clearest most complete phrasing; merge where two
      phrasings each add something.
   4. Include everything: a rule present in only one instance still enters the
      core unless provably consumer-specific (then it is a Named Option, never
      dropped).
   5. Record what was merged/taken/excluded in Provenance > Synthesis notes.

C. LOSSLESS GATE (run before marking the component complete).
   Every contributing instance is either CAPTURED (with location) or EXCLUDED
   (with reason: TRULY-UNIQUE stays at <path>:<lines>, or duplicate of an
   already-captured instance). Any EXCLUDED instance without a reason = FAIL.
   Re-read the live source range when adjudicating each instance. The lossless
   record and the per-consumer source line ranges are recorded in the REGISTRY
   entry (`components[<slug>].consumers[].source` plus the entry `notes`), not in
   an in-component table.

D. FROZEN SPANS (ratified amendment 4).
   Byte-exact wire/protocol strings (halt strings, verdict line formats) are
   wrapped in FROZEN markers inside the Universal Core. Synthesis must NOT
   rephrase them. If live instances diverge byte-wise, pick ONE canonical
   sequence, and log every divergent variant in Provenance. (Precedent: the
   regression-halt string's canonical form is the comma variant.)

E. PLACEHOLDER DISCIPLINE (gate rider R1 as amended).
   Every {{RF_PLACEHOLDER:*}} remaining in the finished file MUST have a
   Value Params row WITH a Binding. bake-time = task-builder resolves it when
   baking; runtime = the executing agent fills it live (single-brace spawn-fill
   slots and runtime selectors are runtime). A placeholder with no row is an
   unfinished authoring slot: FAIL. Runtime-SELECTED structures (tier tables,
   lens libraries) are Universal Core content, never Named Options.

F. SCOPE RULES.
   - KEEP-UNIQUE records get NO component file: register in components/INDEX.md
     with a pointer to the consumer unit + line range (ratified amendment 5).
   - One component file per SPEC id. Prompt variants with their own SPEC ids
     are separate files; relate them to the umbrella via depends_on (amendment 7).
   - The core must be safe verbatim for EVERY consumer listed. Anything that
     applies to some-but-not-all consumers is a Named Option.

G. INCREMENTAL WRITING (mandatory, zero tolerance).
   Write the file with frontmatter + H1 only; append each section ONE AT A TIME
   via Edit (core, params, options one at a time, usage, consumers, provenance);
   run the lossless gate; update the gate table via Edit. Never accumulate the
   whole file in context for one Write.

H. CONSISTENCY (gate rider R2).
   frontmatter `consumers:` == the consumer set in the component's
   `registry.json` entry (same set, same status); the registry-coverage check
   replaces the in-component lossless gate. The reference-integrity CI also
   requires every referenced component to exist; keep slugs exact.

I. IRONFLOW NAMING (born-at-build; CHANGE-SPEC-ironflow-rename-20260624.md section 3).
   Every component you author is born IronFlow. In the OUTPUT component file:
   - reference agents as `if-<agent>` (never `rf-<agent>`): e.g. consumers/depends_on
     list `if-qa`, `if-task-builder`, not `rf-qa`, `rf-task-builder`;
   - reference skills/commands as `/if:<skill>` (never `/rf:*` or `/sc:*`);
   - write the prose brand as "IronFlow" (never "RF-harness"/"Rigorflow"/"superclaude");
   - write plugin self-paths as `ironflow/` (never `rf-harness/`).
   Apply the section-3 rename table to ANY rf-/sc- name you encounter in the live
   source or the extraction map: it maps to its IronFlow equivalent IN YOUR OUTPUT.
   The live source and the map are NOT edited (author-from-live is read-only); only
   your authored output carries IronFlow names.
   The single tracked exception is `/sc:reflect`: if a component records a gate that
   invokes it, leave it as `/sc:reflect` (its rename is deferred). No other rf-/sc-
   name may appear in a finished component.

J. EMIT A REGISTRY ENTRY (replaces the retired in-component Consumers table).
   The component BODY carries no consumer-skill names; each consumer's per-skill
   bindings live in the registry at `ironflow/registry/registry.json`. Before
   marking the component complete, append one `components[]` object to the
   registry, shaped exactly like the existing entries in that file:
   - `component` (the slug), `spec_id`, `family`, `externalize_status`, `notes`,
     and (when applicable) `provisional` / `open_question`;
   - a `consumers[]` array with one object per consumer: `skill`, `status`
     (confirmed | provisional | indirect), `source` (`<skill>:<start>-<end>`
     live line range), `options_selected[]`, and `params{}` (record a param only
     when the consumer OVERRIDES the component-level default);
   - `option_values{}` on a consumer ONLY where a Named Option carries a
     per-consumer value table.
   Use the schema of the objects already in `ironflow/registry/registry.json` as
   the shape to emit. After appending, regenerate the two MD views
   (`ironflow/registry/by-component.md` and `ironflow/registry/by-skill.md`) from
   the JSON so all three stay in sync. The frontmatter `consumers:` list MUST
   equal the registry entry's consumer set (same slugs, same status): this is the
   registry-coverage check that replaces the old rider-R2 body-table sync.
################################################################################
-->

---

## PART 2: THE COMPONENT FILE SCAFFOLD (copy everything below this line)

```yaml
---
# --- Identity (MDTM-standard) ---
id: "COMP-SPEC-NNN"
title: "<component-slug>"
description: "<One sentence: what this component provides to consumers.>"
version: "1.0.0"
# status options (component lifecycle): "active" | "draft" | "deprecated" | "superseded"
status: "active"
type: "🧱 Component"
# priority options: "🔥 Highest" | "🔼 High" | "▶️ Medium" | "🔽 Low" | "🧊 Lowest"
priority: "▶️ Medium"
created_date: "YYYY-MM-DD"
updated_date: "YYYY-MM-DD"
# --- Authoring provenance (MDTM-standard) ---
assigned_to: "<authoring agent>"
autogen: true
autogen_method: "<Track-0 component-authoring task>"
coordinator: "<orchestrator>"
parent_doc: "components/INDEX.md"
parent_task: "<the MDTM task ID that created this file>"
depends_on: []
# ^ other component slugs this component requires (umbrella links live here)
spec_path: "<map §2 record citation; plus any change-spec that amends this component>"
related_docs:
- path: ".dev/tasks/to-do/TASK-RESEARCH-skills-modularization-20260608-155631/COMPONENT-EXTRACTION-MAP.md"
  description: "Extraction map; the §2 record this component implements"
related_prd: ""
related_tdd: ""
tags:
- "<family-tag>"
- "<domain-tag>"
template_schema_doc: ".claude/templates/workflow/03_component_authoring_template.md"
ai_model: "<authoring model id>"
model_settings: "<effort or notable settings>"
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
# --- Modularization fields ---
spec_id: "SPEC-NNN"
family: "<A|B|C|D>"
component_type: "component"
externalize_status: "<SHARED|ANTICIPATORY>"
# ^ KEEP-UNIQUE never produces a component file (INDEX record only)
consumers:
- "<skill-or-agent-slug-1>"   # status: confirmed
- "<skill-or-agent-slug-2>"   # status: confirmed | provisional | indirect
# ^ minimum 2 confirmed for SHARED; ANTICIPATORY lists provisional consumers
registry: "ironflow/registry/registry.json"
# ^ the ledger this component's per-consumer bindings live in; emit a components[]
#   entry there (see PART-1 step J) rather than an in-component Consumers table
---
```

```markdown
# <component-slug>

## Universal Core

<!-- GUIDANCE: The single canonical version ALL consumers get verbatim.
     - Parameterize ONLY via {{RF_PLACEHOLDER:<param_name>}} slots.
     - No consumer-specific wording; some-but-not-all content goes to Named Options.
     - Runtime-SELECTED structures (tier tables, lens libraries) stay HERE in full.
     - Byte-exact wire strings are wrapped in FROZEN marker comments and never
       rephrased. Marker syntax (write as two HTML comments around the span,
       shown here without angle brackets to avoid nesting): FROZEN:START
       reason="wire string" ... FROZEN:END
     - Best-of-best synthesis from LIVE source lines; lossless; no padding. -->

{{RF_PLACEHOLDER:universal_core_content}}

---

## Value Params

<!-- GUIDANCE: Every placeholder used in the core gets a row. Binding (ratified):
     bake-time = resolved by /task-builder when baking; runtime = filled live by
     the executing agent (single-brace spawn-fill slots, runtime selectors).
     Default "REQUIRED" when the consumer must supply it. This table declares each
     param's binding, default, and meaning ONCE; the per-consumer example values
     (what each consumer actually binds a param to) live in the registry entry
     (`components[<slug>].consumers[].params` and `.option_values`), not in the
     component body. If no params, write:
     "None - this component has no value params; the Universal Core is used
     verbatim by all consumers." -->

| Param name | Binding | Default | Description |
|---|---|---|---|
| `{{RF_PLACEHOLDER:param_name}}` | `bake-time` | `REQUIRED` | What this param controls and what values are valid. |

---

## Named Options

<!-- GUIDANCE: Per-consumer/per-flavor variations. Core stays clean.
     Metadata per option (ratified composition semantics):
     - Interaction: appends | replaces <target heading/span> | inserts-at <anchor>
     - Mutually exclusive with: <option names | none>  (consumers MAY select
       multiple non-exclusive options via a selected_options list)
     - Embed form: full | summary-bullet
     - Description: one sentence.
     If none, write: "None - all consumers use the Universal Core without
     variation." -->

### Option: {{RF_PLACEHOLDER:option_name}}

- **Interaction:** {{RF_PLACEHOLDER:option_interaction}}
- **Mutually exclusive with:** {{RF_PLACEHOLDER:option_mutex}}
- **Embed form:** {{RF_PLACEHOLDER:option_embed_form}}
- **Description:** {{RF_PLACEHOLDER:option_description}}

{{RF_PLACEHOLDER:option_content}}

---

## Usage and Reference

### Reference syntax (reference-with-mandate)

```text
<!-- RF-COMPONENT: {{RF_PLACEHOLDER:component_slug}}
     Path: ${CLAUDE_PLUGIN_ROOT}/components/{{RF_PLACEHOLDER:component_slug}}.md
     Resolution: ${CLAUDE_PLUGIN_ROOT} when installed as a plugin; the repo root
       components/ directory when the variable is unset (in-repo development).
     Mandate: {{RF_PLACEHOLDER:mandate_instruction}} -->
```

### Param binding and option selection (consumer-side)

```text
<!-- RF-COMPONENT-PARAMS
     selected_options: [<option-name>, <option-name>]   # list; may be empty
     <param_name>: <value>                              # bake-time params only
     -->
```

### Task-builder baking rule

When `/task-builder` generates a task file consuming this component, it reads
this file and bakes the Universal Core into the task file inline: bake-time
params resolved, runtime params left as live slots, each selected option
applied per its Interaction mode (append, replace its target, or insert at its
anchor) and Embed form. The generated task file is self-contained; executing
agents do not follow the reference path. Skill files keep the reference; task
files carry the baked content.

---

## Provenance

### Synthesis notes

{{RF_PLACEHOLDER:synthesis_notes}}

<!-- Include here: what was merged/taken verbatim/classified core-vs-option, and
     for every FROZEN span: the canonical byte sequence chosen and each divergent
     live variant found (unit + line + the difference). The per-consumer source
     line ranges and the lossless-capture record are recorded in the registry
     entry, not in an in-component table. -->
```

