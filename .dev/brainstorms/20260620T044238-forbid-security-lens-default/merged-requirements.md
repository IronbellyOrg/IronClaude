---
topic: "Surgical edits to forbid /sc:brainstorm from defaulting to a security lens/persona unless explicitly instructed"
domain: process
strategy: systematic
depth: standard
created: 2026-06-20T04:42:38Z
decisions:
  enforcement: active-guard + table-removal
  lens_scope: persona + dialogue-lens (Socratic Q14)
  generality: reusable auto_excluded_personas set
status: requirements-only
note: "Adversarial multi-model wave intentionally skipped — edit set is deterministic once the 3 scoping decisions are locked. Produces requirements; does NOT implement."
amended: 2026-06-20T04:54Z
amendment_log:
  - "G1: added EDIT-7 (plugins/ mirror) after confirming repo-root plugins/ is hand-maintained, not regenerated"
  - "G2: added Out-of-Scope ruling on compliance-framed Socratic Q17 probes"
  - "G3: corrected site count (~24 security-bearing lines across 5 tracked files + 2 docs)"
  - "G4: noted indirect enterprise auto-trigger path is closed by EDIT-1b/2a + guard"
reflect_report: .dev/reflect/pre-forbid-security-lens-20260620045010/REPORT.md
---

# Surgical Edit Spec — Forbid Auto Security Lens in `/sc:brainstorm`

## Problem Statement

`/sc:brainstorm` injects a **security lens** into runs the user never asked for, through
two independent mechanisms: (1) the `security` persona is a *default* advocate in 5 of 6
domain persona-matrices **and** in the enterprise-strategy override, so it silently becomes
one of the N parallel proposal agents; (2) the code-domain deep Socratic probe steers the
dialogue through a "what would a security reviewer ask" frame. The user wants both
suppressed **by default** and reachable **only when explicitly instructed** (i.e.
`--personas security`).

**Surface count (corrected, G3):** ~24 security-bearing lines across **5 tracked files**
(`agent-spec-builder.md`, `SKILL.md`, `socratic-templates.md`, `SPEC.md`,
`plugins/superclaude/commands/brainstorm.md`) **+ 2 docs** (`commands/brainstorm.md`,
`docs/user-guide/brainstorm.md`). An earlier "17 sites" figure was an undercount.

## Locked Decisions

| # | Decision | Choice |
|---|----------|--------|
| D1 | Enforcement strength | **Active runtime guard + passive table removal** (belt-and-suspenders) |
| D2 | Scope of "lens" | **Persona auto-selection + dialogue lens** (remove/neutralize Socratic Q14) |
| D3 | Generality | **Reusable `auto_excluded_personas` set** (security = first/only member) |

## Constraints

- **Explicit path must keep working**: `--personas architect,security` (or any list naming
  `security`) MUST still select and run the security persona. "Forbid" applies to *auto/default*
  selection only.
- **Source-of-truth discipline** (CLAUDE.md): edit `src/superclaude/**`,
  `.dev/eval-workspaces/sc-brainstorm/SPEC.md`, and `plugins/superclaude/commands/brainstorm.md`
  (a tracked, hand-maintained file — see EDIT-7); then `make sync-dev` → `make verify-sync`.
  **Never** edit or stage `.claude/**` (regenerated mirror). `plugins/` is **not** the same
  as `.claude/`: `make build-plugin` writes to `dist/plugins/`, and no target regenerates
  repo-root `plugins/`, so it is hand-edited and must be edited directly here.
- **Keep the `security` instruction-template row** — it is consumed on the explicit path; deleting
  it would break `--personas security`.
- No executed test asserts the security defaults (`tests/cli_portify/test_brainstorm_gaps.py`
  uses an unrelated `Persona` field), so vector edits are for consistency, not to unbreak CI.

## Success Criteria

1. A default run in **every** domain (code, architecture, incident, product, research) and under
   **`--strategy enterprise`** produces an agent-spec containing **no `security` persona**.
2. `--personas security` (alone or in a list) **still** yields a security advocate — unchanged.
3. The code/deep Socratic dialogue no longer asks the security-reviewer framing question.
4. A future careless re-add of `security` to a persona table is **neutralized at runtime** by the
   guard (still excluded unless `--personas` names it).
5. `make verify-sync` passes; command file, user-guide doc, SPEC.md, **and the tracked
   `plugins/` command mirror** all agree with behavior.
6. Compliance/policy-framed Socratic probes are **explicitly ruled out-of-scope** (see Out of Scope)
   — they are not silently altered.

---

## Surgical Edits (5 tracked files + 2 docs + sync)

### EDIT-1 — `src/superclaude/skills/sc-brainstorm-protocol/refs/agent-spec-builder.md`

**1a. Persona-Matrix tables (L11–L16): remove `security` from each row.**

| Domain | New default persona list (security removed) |
|--------|---------------------------------------------|
| `code` | `architect, refactorer, qa, backend, frontend, analyzer` |
| `architecture` | `architect, analyzer, backend, devops, performance, scribe` |
| `incident` | `analyzer, devops, qa, architect, backend, performance` |
| `product` | `architect, frontend, scribe, analyzer, backend, qa` |
| `research` | `analyzer, architect, scribe, performance, backend, devops` |
| `process` | *(unchanged — already security-free)* |

Each row still has ≥6 personas; the existing cycle/pad rule (L24) covers `--proposals` up to 7.

**1b. Enterprise override (L19): remove `security`; backfill to keep a 5-wide panel.**
`architect, security, devops, scribe, qa` → **`architect, analyzer, devops, scribe, qa`**
(`analyzer` substituted as a neutral critical-reviewer. *Sub-decision SD1:* alternative is to
drop to 4 and let padding fill — recommend the `analyzer` substitution to preserve panel width.)

**1c. NEW §Auto-Exclusion section (the D1+D3 guard).** Add after §Persona-Matrix:

```md
## §Auto-Exclusion

auto_excluded_personas = { security }
# Personas in this set are NEVER auto-selected (domain default, enterprise override,
# or pad/cycle). They are reachable ONLY when named explicitly in --personas.

Apply AFTER persona selection and BEFORE model rotation:
  explicit  = set(--personas)  if --personas non-empty  else {}
  selected  = [p for p in selected if p not in auto_excluded_personas or p in explicit]
  # backfill to --proposals from the same priority list, skipping any
  #   p in auto_excluded_personas unless p in explicit
  for each dropped p:
    INFO: "Persona '<p>' excluded from auto-selection (not named in --personas).
           Substituted '<next>'."
```

**1d. Keep the `security` instruction-template row (L60)** — add an inline note:
`<!-- applied only when security is explicitly requested via --personas; never auto-selected -->`

**1e. Worked-example assignments (L46–L48): swap `security:sonnet` for the next non-excluded
code persona (`frontend`) and recompute model rotation per §Model-Rotation.**

**1f. §Serialization final-string example (L94): replace the security example** with the
already-clean code/3/standard string (matches L141 vector):
`opus:architect:'…for code domain',sonnet:refactorer:'…minimal-risk transformation paths',haiku:qa:'…acceptance criteria'`

**1g. §Round-Trip Test Vectors (L142, L143): regenerate without security.**
- L142 `incident,5,deep` → personas `analyzer, devops, qa, architect, backend` (security removed), rotation recomputed.
- L143 `enterprise,5` → personas `architect, analyzer, devops, scribe, qa`.

### EDIT-2 — `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`

**2a. Wave 2B persona-selection (L212): enterprise list** → `architect, analyzer, devops, scribe, qa` (matches 1b).
**2b. Add a guard step to Wave 2B step 1** (after the existing branches, before "Pad/truncate"):
> "Apply §Auto-Exclusion from `refs/agent-spec-builder.md`: strip any `auto_excluded_personas`
> member (currently `security`) not present in an explicit `--personas`, backfilling from the
> priority list; emit one INFO per drop."
**2c. Example agent-spec (L243): swap** `sonnet:security:'…OWASP…'` for a non-security persona
(e.g. `sonnet:refactorer:'…minimal-risk transformation paths'`).

### EDIT-3 — `src/superclaude/skills/sc-brainstorm-protocol/refs/socratic-templates.md`

**3a. Code/deep Probe Q14 (L59): replace the security frame with a neutral adversarial probe.**
`14. What would a security reviewer ask about this?` →
`14. What would an independent reviewer from another team flag as the riskiest part of this?`
(*Sub-decision SD2:* alternative is outright deletion — recommend neutral replacement to preserve
deep-tier probe count and adversarial value without the security framing.)

> **Indirect-trigger note (G4):** `socratic-templates.md` L30 auto-classifies `--strategy
> enterprise` on compliance keywords (SOC2/SOX/HIPAA/audit/regulation). That path reaches the
> *enterprise persona list*, so it is **already closed** by EDIT-1b/2a (security removed from that
> list) **+** the EDIT-1c guard (which strips security even if a list re-adds it). No edit to L30
> is required — the strategy-detection keywords are about routing, not about the security lens.

### EDIT-4 — `.dev/eval-workspaces/sc-brainstorm/SPEC.md` (authoritative spec — must track)

- **L217**: enterprise override → `architect, analyzer, devops, scribe, qa`.
- **L242**: example agent-spec → drop the `sonnet:security:'…OWASP…'` segment (swap as in 2c).
- **L99**: `--personas` example `architect,security,frontend` → keep `security` here **on purpose**
  (it documents the *explicit* override path) but append: "(security is auto-excluded by default;
  naming it here is how you opt in)."
- **L492**: test-scenario row "Analyzer/security/devops personas" → "Analyzer/devops personas"
  (or note security only via explicit `--personas`).
- Add the §Auto-Exclusion rule to the SPEC's Wave 2B section so regeneration preserves it.

### EDIT-5 — Documentation / command prose (doc⇆behavior parity)

- `src/superclaude/commands/brainstorm.md` **L81** ("architect/security/backend personas") and
  **L89** ("Analyzer/security/devops personas"): drop `security` from the auto-example prose.
- `docs/user-guide/brainstorm.md` **L105** and **L113**: same edits.

### EDIT-7 — `plugins/superclaude/commands/brainstorm.md` (tracked, hand-maintained mirror — G1)

**Provenance verified:** `git ls-files` → TRACKED, `git check-ignore` → not ignored;
`make build-plugin` writes to `dist/plugins/` (via `scripts/build_superclaude_plugin.py`), and **no
target regenerates repo-root `plugins/`**; git history shows hand edits only (markdownlint pass +
the v1 "restore 30 commands" commit). It is **stale/divergent** from src (114 vs 201 lines, v1-era
structure with a `project-manager` persona). → It must be edited directly; it will NOT be fixed by
`make sync-dev`.

Strip `security` from the **4** references (surgical — do not attempt a full src↔plugins reconcile):

- **L7** frontmatter: `personas: [architect, analyzer, frontend, backend, security, devops, project-manager]`
  → remove `security,` → `[architect, analyzer, frontend, backend, devops, project-manager]`
- **L39**: "…across architecture, analysis, frontend, backend, **security** domains" → drop `, security` / `security`.
- **L82**: "Parallel exploration paths with frontend, backend, and **security** personas" → drop `, and security` → "…with frontend and backend personas".
- **L90**: "Comprehensive validation with **security**, devops, and architect personas" → drop `security, ` → "…with devops and architect personas".

> **Scope boundary:** EDIT-7 removes only the security lens. The broader staleness of `plugins/`
> (87 fewer lines, v1 structure, full src↔plugins reconciliation) is a **separate concern**, not
> part of this spec. Flag it as follow-up OQ4 below.

### EDIT-6 — Sync + verify (mechanical, mandatory)

```bash
make sync-dev
make verify-sync
uv run pytest tests/cli_portify/test_brainstorm_gaps.py -q   # sanity; not coupled but cheap
```

(Note: `plugins/` is edited directly in EDIT-7 — `make sync-dev` does NOT touch it.)

---

## Out of Scope (explicit rulings)

- **Compliance/policy-framed Socratic probes (G2)** — `socratic-templates.md` L91
  (incident Q17 "What policy / SLO / **compliance** angle…") and L178 (process Q17 "What's the
  **audit / compliance** angle?") are **OUT OF SCOPE** and left **unchanged**. Rationale: a
  compliance/governance lens is distinct from the security/threat-model lens the user named;
  the user explicitly discussed only the "security reviewer" frame (Q14). Removing the
  compliance probes would over-reach beyond the stated intent. (If a future request widens the
  goal to "no governance/compliance lens either," these two lines are the targets.)
- **`plugins/` general staleness** — see EDIT-7 scope boundary; only the security lens is removed.
- **The eval grader's "hostile reviewer" framing** — `SPEC.md` L523/L552/L603/L642/L708 describe
  the *grader's* adversarial stance, unrelated to the security persona; **left untouched** (a naive
  `grep hostile` replace would wrongly hit these — do not).

---

## Risks & Tradeoffs

- **R1 — incident/architecture lose an often-relevant default lens.** Security is genuinely
  pertinent for breaches/topology. *Mitigation:* documented `--personas …,security` opt-in; the
  guard's INFO line tells the user it was excluded and how to re-add it.
- **R2 — enterprise panel semantics shift.** Removing the security advocate weakens the
  "enterprise = compliance-aware" connotation. *Mitigation:* `analyzer` backfill (SD1) keeps a
  rigorous critical reviewer; note in SPEC that security is now opt-in even in enterprise mode.
- **R3 — drift across the 5 tracked files.** Easy to edit refs but miss SPEC.md (regen re-adds
  security) or the hand-maintained `plugins/` mirror (EDIT-7, not fixed by `make sync-dev`).
  *Mitigation:* this spec enumerates all 5 + 2 docs, and the post-edit grep gate (below) now
  includes `plugins/` and SPEC.md.

## Verification Gate (post-implementation)

```bash
# Must return ZERO hits in auto/default contexts (explicit-path mentions in SPEC L99 are allowed):
grep -rn -i "security" \
  src/superclaude/skills/sc-brainstorm-protocol/ \
  src/superclaude/commands/brainstorm.md \
  docs/user-guide/brainstorm.md \
  plugins/superclaude/commands/brainstorm.md \
  .dev/eval-workspaces/sc-brainstorm/SPEC.md \
  | grep -v "auto_excluded_personas\|explicitly requested\|opt in\|instruction-template row\|auto-excluded by default"
# Expected residual (allowed): SPEC.md L99 explicit --personas example; the kept instruction-template row.
# Compliance-probe lines (socratic L91/L178) are intentionally NOT matched by this gate (different word).
```

## Open Questions

- **OQ1 (SD1)**: enterprise backfill — `analyzer` (recommended) vs. drop-to-4?
- **OQ2 (SD2)**: Socratic Q14 — neutral replacement (recommended) vs. delete?
- **OQ3**: Should a Wave 0 INFO fire when `--personas` includes an auto-excluded persona
  ("honoring explicit security request")? Nice-to-have, not required for the contract.
- **OQ4 (follow-up, out-of-scope here)**: `plugins/superclaude/commands/brainstorm.md` is broadly
  stale vs `src/` (114 vs 201 lines, v1 structure). A full src↔plugins reconciliation — or a
  decision to regenerate/retire repo-root `plugins/` — is a separate task. EDIT-7 only removes the
  security lens from it.
