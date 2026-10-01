# Variant 2 (refactorer): switch Wave 2 to template 00, keep one source of truth for the rules

Stance: the 8 rules and the 3 fields already exist in one place (template 00). Copying them into the
protocol would create a second copy that drifts. The smallest *safe* change is to point Wave 2 at
template 00, swap the 03 heading gate for a 00 shape gate, and put the fill rules next to the schema.
Three source files change plus their plugin mirrors and one guard test. Nothing else changes.

## Decision

1. **Render template 00 instead of the 03 body.** Rationale: the 03 body (`### Phase N` + `- **Goal**:` bullets,
   `03_project_plan_template.md:30-52`) has zero enumerable items for `/sc:implement`, so the whole plan runs as T1
   (`sc-implement-protocol/SKILL.md:53,67`). Template 00 is already shaped for enumeration (`## Task N`,
   `Acceptance criteria:`, `00_mdtm_template_simple_task.md:32-47`) and its comment says it is "For /sc:workflow to
   fill in" (`00:9`), so the rules come with it without being copied. The 03 heading gate (`refs/quality-gates.md:13`)
   is replaced, not reconciled. 03 stays in place because `rf-team-lead.md:463` still uses it.
2. **Fill rules:** `created_date` = run date in UTC; `version` = `"1"`; `priority` = the source's explicit priority
   if it states one, else `Medium`. No new flag. Rationale: runs overwrite the same slug in place with no resume
   (`refs/input-parse.md:13`), so the plan is always revision 1. The command's flag table (`commands/workflow.md:36-42`)
   stays as it is, which follows the brief's "no new flags" constraint.
3. **Require the new keys at schema-min and bump `schema` to `workflow-plan/1.1`.** Rationale: the values are
   deterministic and cheap to check, so quick runs should not be exempt (`quality-gates.md:15-19`). The body shape
   changes from 03 to 00, which is a schema change. A grep of the repo (excluding `.dev/`, `.claude/`, `.venv/`) finds
   no reader of `workflow-plan/1.0` other than `quality-gates.md:6` and its plugin mirror, so the bump breaks nothing.
4. **Leave `return-contract.yaml` unchanged at 1.0.** Rationale: the contract describes the run, not the plan
   (`refs/return-contract.md:5-15`). The new fields are in `plan_path`'s frontmatter, and echoing them would
   duplicate data and force a contract version bump.

## File edits

### `src/superclaude/skills/sc-workflow-protocol/SKILL.md`

Current (line 42):

```
Write `<run>/plan.md` using headings from `src/superclaude/templates/workflow/03_project_plan_template.md` (`## Project Goal`, `## Project Context`, `## Phases`). Do not copy MDTM 00–02.
```

New:

```
Write `<run>/plan.md` from `src/superclaude/templates/workflow/00_mdtm_template_simple_task.md`. Follow every rule in its HTML comment, then delete the comment and every unused placeholder. Frontmatter = the template's `version` / `priority` / `created_date` (fill rules: `refs/quality-gates.md`) plus the gate keys.

Render each Wave 1 phase as `## Phase N: <goal>` followed by its `## Task N:` headings. Task numbers are global across phases (Task 1..N, never restart). Phase deps/Inputs → `Depends on: Task K` on the first task of the phase; Outputs → task body; Checkpoint → the last task's `Acceptance criteria:`. Do not use 03 or MDTM 01–02.
```

Line 44 (`If source was an inline prompt, ...`) is unchanged.

### `src/superclaude/skills/sc-workflow-protocol/refs/quality-gates.md`

Current (lines 3-19):

````
`plan.md` frontmatter MUST include:

```yaml
schema: workflow-plan/1.0
source: <path>
strategy: systematic|agile|enterprise
depth: quick|standard|deep
slug: <slug>
```

Body MUST have headings: `## Project Goal`, `## Project Context`, `## Phases` (same names as `03_project_plan_template.md`). Each phase: Goal, Inputs, Outputs, Checkpoint, deps.

## Schema-min (quick)

- frontmatter keys present
- ≥1 phase
- no MDTM checklist dialect (`- [ ]` task items as the phase body)
````

New:

````
`plan.md` frontmatter MUST include:

```yaml
schema: workflow-plan/1.1
source: <path>
strategy: systematic|agile|enterprise
depth: quick|standard|deep
slug: <slug>
version: "1"
priority: High|Medium|Low
created_date: YYYY-MM-DD
```

Fill: `version` = `"1"` (same-slug runs overwrite, no resume). `priority` = the source's explicit priority (frontmatter `priority:` or a `Priority:` line), else `Medium`; never inferred. `created_date` = run date, UTC.

Body = `00_mdtm_template_simple_task.md` shape: `# <title>`, `Source:`, `Goal:`, optional `## Constraints`, `## Phase N:` group headings, `## Task N:` items each with `Acceptance criteria:`.

## Schema-min (quick)

- frontmatter keys present; `priority` in enum; `created_date` matches `YYYY-MM-DD`; `version` non-empty
- ≥1 `## Phase N:` and ≥1 `## Task N:`; Task numbers unique
- no checkbox (`- [ ]`, `- [x]`, `* [ ]`) or numbered-list (`1.`, `1)`) lines anywhere in the body
- template comment and `[...]` placeholders removed
````

Current (lines 23-28, Full section bullets):

```
- every phase has Inputs and Checkpoint
- deps acyclic
- phase count within depth cap
- output paths not under `.claude/skills|agents|commands`
```

New:

```
- every Task has `Acceptance criteria:` with ≥1 bullet
- every `Depends on: Task K` names an earlier Task (acyclic by construction)
- phase count within depth cap
- no plan-wide `Outputs` / `Success Criteria` / `Verification` section
- output paths not under `.claude/skills|agents|commands`
```

Line 30 (`Fail any check → STOP E-GATE ...`) is unchanged.

### `tests/commands/test_workflow_command.py`

Append after line 38:

```python
def test_plan_renders_template_00_with_new_frontmatter():
    skill = (_SKILL / "SKILL.md").read_text(encoding="utf-8")
    gates = (_SKILL / "refs" / "quality-gates.md").read_text(encoding="utf-8")
    assert "00_mdtm_template_simple_task.md" in skill
    assert "03_project_plan_template.md" not in skill + gates
    tpl = _REPO / "src" / "superclaude" / "templates" / "workflow" / "00_mdtm_template_simple_task.md"
    assert tpl.is_file()
    for key in ("schema: workflow-plan/1.1", "version:", "priority:", "created_date:"):
        assert key in gates, key
    plugin = _REPO / "plugins" / "superclaude" / "skills" / "sc-workflow-protocol"
    for rel in ("SKILL.md", "refs/quality-gates.md"):
        assert (plugin / rel).read_bytes() == (_SKILL / rel).read_bytes(), rel
```

The last loop checks that the plugin mirror matches `src/` for the two edited files. The seed brief says the mirror
must stay byte-identical, and `Makefile` has no target for `plugins/superclaude/` (only `sync-dev` at line 109 and
`verify-sync` at line 166, both for `.claude/`). Without this check, drift would go unnoticed.

### `plugins/superclaude/skills/sc-workflow-protocol/SKILL.md` and `.../refs/quality-gates.md`

Copy the two `src/` files over byte-for-byte (`cp`). Today `diff -r` shows the whole skill dir plus
`commands/workflow.md` identical to `src/`. After the copy, run `make sync-dev` for `.claude/` and do not stage `.claude/`.

## Files unchanged

- `src/superclaude/commands/workflow.md` (+ plugin mirror): it owns no plan format (`:48`). The `plan.md` wording (`:12,67`) and the `/sc:implement @plan.md` next step (`:82`) are still true, and more useful now.
- `src/superclaude/templates/workflow/00_mdtm_template_simple_task.md`: already carries the fields and rules (`:1-5`, `:9-21`), so it is used as-is. There is no plugin copy (`plugins/superclaude/templates/` holds only `roadmaps`).
- `src/superclaude/templates/workflow/03_project_plan_template.md`: still used by `agents/rf-team-lead.md:463`.
- `refs/phase-templates.md`: Wave 1 still produces phases with Goal/Inputs/Outputs/Checkpoint/deps (`:3`). The mapping onto 00 lives in the SKILL Wave 2 paragraph above.
- `refs/input-parse.md`: `E-GATE | Wave 3 schema/heading fail` (`:26`) still describes the gate.
- `refs/return-contract.md`: Decision 4.
- `refs/overlap-routing.md`: handoff `implement` passes `plan.md` unchanged (`:5`).
- `sc-implement-protocol/SKILL.md`: the plan now fits its existing grammar, so it needs no change.

## Fill rules

| Key | Set by | Source | Default | Format |
|-----|--------|--------|---------|--------|
| `version` | Wave 2 writer | constant (overwrite-in-place, `input-parse.md:13`) | `"1"` | quoted string |
| `priority` | Wave 2 writer | explicit priority in the source (frontmatter `priority:` or a `Priority:` line); inline prompt → default | `Medium` | `High` \| `Medium` \| `Low` (no brackets) |
| `created_date` | Wave 2 writer | run date, UTC | none (always set) | `YYYY-MM-DD` |

Never guess priority from tone. That would break template 00's "DO NOT invent" rule (`00:14`).
Existing keys (`schema/source/strategy/depth/slug`) keep their current sources. Only `schema` changes, to `1.1`.

## Gate changes

- **Schema-min (quick):** checks all 8 keys, validates `priority`, `created_date` and `version`, requires ≥1 Phase and
  ≥1 Task heading with unique Task numbers, bans checkbox and numbered-list lines anywhere in the body (not only
  "as the phase body" as at `quality-gates.md:19`), and requires the template comment and placeholders to be removed.
- **Full (standard/deep):** schema-min plus: every Task has an `Acceptance criteria:` bullet, `Depends on` only points
  backward, phase count is within the depth cap, there is no plan-wide Outputs/Success/Verification section, and the
  `.claude/` path ban stays.
- **Dropped:** "every phase has Inputs and Checkpoint" (`quality-gates.md:25`). Inputs become `Depends on`, and
  Checkpoint becomes the last task's acceptance criteria, so the Task-level checks replace it.
- **Rules not gated:** coverage, no fabrication, self-contained, no read-only or bulk tasks, and enumerate-items
  are not mechanical checks. The writer follows them from the template comment (Wave 2).
- **STOP:** unchanged. Any failure → `E-GATE` (`quality-gates.md:30`), and the contract gets `status: failed`
  (`return-contract.md:19`).

## /sc:implement compatibility

- `## Task N:` headings match enumerable rule 3 (`sc-implement-protocol/SKILL.md:65`). `Task 3:` normalizes to `T3`
  (`:61`). Global numbering keeps ids unique across phases.
- `## Phase N:` headings have Task children, so they are group headings, not tasks (`:65`).
- `Acceptance criteria:` blocks are AC QUALIFY match 1 (`:75`), and `## Constraints` feeds the global constraints (`:83`).
- The gate bans `- [ ]` and `1.` lines in the body, which rules out enumerable rules 1 and 2 (`:63-64`). Mixed
  document order therefore cannot split a Task into extra tasks (`:61,67`). Template 00 states the same rule (`00:12`).
- `Depends on:` is plain text. `/sc:implement` runs sequentially by default (`:87`), so it causes no parallelism.
- Net effect: `/sc:implement @plan.md` goes from 1 whole-document task (`:67`) to N reviewed tasks.

## Risks

1. **Hidden consumer of the 03-shaped plan or of `workflow-plan/1.0`.** Mitigation: the grep outside `.dev/`,
   `.claude/` and `.venv/` found only `quality-gates.md` and its mirror. The schema bump makes any future reader
   fail loudly instead of misparsing.
2. **The writer leaves numbered steps inside a Task body** (natural for "do X, then Y"), so `/sc:implement`
   splits the Task. Mitigation: the schema-min gate bans numbered and checkbox lines anywhere in the body and
   STOPs with `E-GATE`. Template 00 says "plain bullets" (`00:12`).
3. **Plugin mirror drift**: there is no make target for `plugins/superclaude/`. Mitigation: the byte-equality
   assert in the new test.
4. **Installed-path mismatch**: SKILL cites a `src/superclaude/templates/...` path. This convention already exists
   at `SKILL.md:42`, and this change keeps it. Mitigation: out of scope here (see below). Because the template's
   rules are the writer's instructions, if the template is unreadable the writer should fail visibly rather than
   improvise. Add "Template unreadable → STOP `E-GATE`" only if this is seen in practice.
5. **Losing Checkpoint as a first-class field** may make phases less clear to human readers. Mitigation: the
   Checkpoint is kept as the last task's acceptance criteria, where `/sc:implement` actually QAs it.

## Out of scope

- A `--priority` flag, or a version counter across runs (no resume exists).
- Echoing new fields in `return-contract.yaml`, or bumping it past 1.0.
- Mechanical gating of the 5 judgment rules (coverage, fabrication, self-contained, read-only/bulk, enumeration).
- Editing template 00, template 03, `phase-templates.md`, `input-parse.md`, `overlap-routing.md`, or `/sc:implement`.
- Fixing the `src/`-relative template path for installed copies.
- Any Python runtime or `.claude/` staging.
