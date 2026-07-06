# Reviewer B — Governance Conformance + Internal Consistency

**Scope**: Commit `09f7d487` (`feat(cli-eval)`). Lens: does the `/sc:cli-eval` package hang together
internally, and does it conform to the SuperClaude Developer Guide + the worktree CLAUDE.md?

**Files reviewed**: `commands/cli-eval.md`; `skills/sc-cli-eval-protocol/{SKILL.md, refs/*, templates/*}`;
`agents/{eval-docs-loader, eval-suite-author, eval-run-reporter}.md`; cross-checked against
`commands/{adversarial,spec-panel,document}.md`, `skills/sc-adversarial-protocol`,
`skills/sc-cli-portify-protocol`, `skills/sc-roadmap-protocol`, `cli/eval/*`, the Developer Guide, and CLAUDE.md.

**Verdict**: structurally sound and governance-clean on the high-risk axes (no `.claude/` staging, no new
`superclaude eval` flags, correct `.dev/eval-workspaces/` sink, exit-code/schema/contract claims all match
source). Real defects found are consistency-of-convention issues, the sharpest being an undeclared
divergence from the sibling `sc-cli-portify` "no inter-skill command invocation" decision.

---

## Findings

### B1 — MED — Direct `Skill sc:spec-panel` / `Skill sc:document` invocation contradicts the sibling cli-portify "no inter-skill command invocation" decision (undeclared)

- **Where**:
  - `skills/sc-cli-eval-protocol/SKILL.md:81` (`Invoke: Skill sc:spec-panel ...`),
    `SKILL.md:108` (`via Skill sc:document`), `SKILL.md:174` & `:177` (Delegation Pattern table rows).
  - `refs/create-pipeline.md:23` (`Skill sc:spec-panel ...`), `:54` (`Skill sc:document`).
  - `refs/integration-map.md:9-12, 44-47` (the `Skill sc:spec-panel` / `Skill sc:document` invocation blocks).
  - **Other side**: `skills/sc-cli-portify-protocol/decisions.yaml:58` —
    *"No inter-skill command invocation. Embed sc:brainstorm and sc:spec-panel behavioral patterns inline
    ... rather than invoking them as commands."* and `sc-cli-portify-protocol/SKILL.md:242` —
    *"embeds spec-panel behavioral patterns directly rather than invoking the `sc:spec-panel` command
    (Constraint 1: no inter-skill command invocation)."*
- **What's inconsistent**: Two sibling skills built on the same eval/CLI-portify surface take opposite
  stances on reusing `sc:spec-panel`. cli-portify deliberately embeds the *pattern* inline citing
  "Constraint 1: no inter-skill command invocation"; cli-eval instead invokes `Skill sc:spec-panel` and
  `Skill sc:document` directly. Both can't be the house rule. The new skill never acknowledges or
  rebuts the cli-portify constraint, so a maintainer reading the two will not know which is canonical.
- **is_real**: YES (real internal-consistency divergence). Severity is MED not HIGH because:
  (a) `sc:spec-panel` and `sc:document` ARE exposed as invocable skills by the install layer (they appear
  in the live available-skills registry), so the call is not guaranteed to dangle; and
  (b) the adversarial reuse on the same axis IS well-precedented (see B2), so the reuse *philosophy* is
  not novel — only the spec-panel/document command-as-skill leg conflicts with cli-portify's explicit
  decision.
- **suggested_fix**: Add one sentence to `refs/integration-map.md` reconciling with cli-portify's
  Constraint 1 — either "cli-eval intentionally invokes these as skills because the install layer
  registers commands as skill aliases (unlike cli-portify's inline-embed choice), and here is why that's
  safe" OR fall back to the cli-portify inline-embed pattern for spec-panel/document. Pick one house rule
  and cite it. (Note also B5: the loud-fallback probe that reflect uses for `sc-adversarial-protocol` is
  entirely absent here.)

### B2 — NONE (verified clean) — `Skill sc:adversarial-protocol` naming + reuse is correct and precedented

- **Where**: `SKILL.md:87, 176`; `refs/create-pipeline.md:29`; `refs/integration-map.md:24-26, 34-37`.
- **Checked**: The skill dir is `skills/sc-adversarial-protocol/` with frontmatter `name: sc:adversarial-protocol`,
  and `commands/adversarial.md:146` hands off via `> Skill sc:adversarial-protocol`. Precedent
  `sc-roadmap-protocol/SKILL.md:204,251,264` and `sc-reflect-protocol/SKILL.md:325` both invoke
  `Skill sc:adversarial-protocol` with the identical colon+`-protocol` form and the same
  `--compare` / `--source --generate --agents` surface. **No defect** — the name resolves, the flag
  surface matches `commands/adversarial.md` (Mode A `--compare`, Mode B `--source/--generate/--agents`),
  and the `--agents model[:persona]` spec is consistent.

### B3 — LOW — Mixed delegation-naming convention in the Delegation Pattern table

- **Where**: `SKILL.md:174-177` Delegation Pattern table — rows read `Skill sc:spec-panel`,
  `Skill sc:adversarial-protocol`, `Skill sc:document`.
- **What's inconsistent**: One row carries the `-protocol` suffix (`sc:adversarial-protocol`) while the
  other two are bare command names (`sc:spec-panel`, `sc:document`). This is correct *mechanically*
  (adversarial has a backing protocol skill; spec-panel/document are command-only and only resolve as
  skills via the install-layer alias), but the table gives no hint why the suffix appears on one and not
  the others, which reads like a typo to a reviewer.
- **is_real**: YES (cosmetic/clarity). **suggested_fix**: add a one-word qualifier per row
  (e.g. "(skill)" vs "(command-as-skill)") or a footnote, so the asymmetry is obviously intentional.

### B4 — LOW — Command uses `## Behavioral Summary`, but the Guide's command section table mandates `## Behavioral Flow`

- **Where**: `commands/cli-eval.md:41` (`## Behavioral Summary`).
  - **Other side**: Developer Guide line 282 — `| `## Behavioral Flow` | Step-by-step protocol | **Yes** |`.
- **What's non-conformant**: The guide lists `## Behavioral Flow` as a *required* command section;
  cli-eval.md (like the thin precedent) titles it `## Behavioral Summary`.
- **is_real**: YES but **near-zero risk** — the precedent thin command `commands/adversarial.md:74` ALSO
  uses `## Behavioral Summary`, so cli-eval is consistent with the established thin-command archetype and
  the divergence is the guide-vs-precedent gap, not a cli-eval-specific defect. The thin-command archetype
  legitimately summarizes rather than enumerates a protocol it hands off.
- **suggested_fix**: Optional — rename to `## Behavioral Flow` to satisfy the literal guide table, or
  (better) leave as-is and update the guide to bless `## Behavioral Summary` for the thin/Activation
  archetype. No change required for correctness.

### B5 — LOW — No degraded-mode/probe fallback for the reused skills (reflect has one; cli-eval doesn't)

- **Where**: `SKILL.md` Error Handling table (`:201`) — `/sc:spec-panel` or `/sc:adversarial` errors →
  "Retry once with reduced payload / Proceed with the un-merged best design". `refs/integration-map.md:59-64`
  notes the subagent-nesting limitation but only as a caveat.
  - **Other side**: `sc-reflect-protocol/SKILL.md:325-331` defines a Step-5.0 pre-invocation **probe**
    (`Skill('sc-adversarial-protocol', args='--help')`) with explicit F1/F2/F3 loud-fallback and an
    `adversarial_unavailable: true` return field.
- **What's inconsistent**: A sibling skill that reuses adversarial added a structured "is the skill even
  installed" probe + loud fallback; cli-eval reuses three components but has only a generic
  "retry once, then proceed" row and no probe / no `*_unavailable` return field. Given B1's open question
  about whether `sc:spec-panel`/`sc:document` resolve as skills in every install, the absence of a probe
  is a real robustness gap.
- **is_real**: YES (robustness/consistency). **suggested_fix**: mirror reflect's pre-invocation probe for
  at least the spec-panel/document legs, and add a `reuse_degraded` / `*_unavailable` boolean to the
  Return Contract so a degraded run is machine-detectable rather than silently "proceeded".

---

## Where I found NOTHING wrong (explicitly verified clean)

- **Activation pattern (cli-eval.md:67-73)** — present, verbatim per Guide lines 64-72:
  `**MANDATORY**: ... > Skill sc:cli-eval-protocol` + the "Do NOT proceed ... full behavioral
  specification is in the protocol skill" lines. CLEAN.
- **Naming triad** — command `cli-eval` (bare) / skill `name: sc:cli-eval-protocol` (colon) / dir
  `sc-cli-eval-protocol` — matches the adversarial precedent exactly (command `adversarial`,
  skill `name: sc:adversarial-protocol`, dir `sc-adversarial-protocol`). CLEAN.
- **Command frontmatter** — `name, description, category, complexity, mcp-servers, personas` all present
  and well-formed (Guide §3.1 required set). `allowed-tools` is a *skill* field, not required on commands;
  its omission on the command is conformant (adversarial.md adds it only as an optional extra). CLEAN.
- **Skill frontmatter** — `name: sc:cli-eval-protocol` (colon form ✓), `description` ✓,
  `allowed-tools` present and scoped (`Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill,
  AskUserQuestion`), `argument-hint` ✓; extended-metadata HTML comment matches Guide §5.3. CLEAN.
- **Command ⇄ skill metadata parity** — `category: testing`, `complexity: advanced`,
  `mcp-servers: [sequential, context7, serena]`, `personas: [architect, analyzer, qa, scribe]` are
  byte-identical across `cli-eval.md:4-7` and `SKILL.md:9-12`. CLEAN.
- **Options/argument-hint parity** — command Options table (`cli-eval.md:32-39`:
  `create|run`, `--name`, `--from`, `--agents`, `--suite`, `--eval`) exactly matches the skill
  `argument-hint` (`SKILL.md:5`) and Input Contract (`SKILL.md:39-44`). `--agents` default
  `opus,sonnet,haiku` is identical in command, hint, and Input Contract. CLEAN.
- **Agent name resolution** — Delegation Pattern table's `eval-docs-loader` / `eval-suite-author` /
  `eval-run-reporter` (`SKILL.md:173,176,179`) match the three agent files' `name:` fields exactly. CLEAN.
- **Agent frontmatter** — all three carry `name`, `description`, `category`, `tools`, `model`
  (loader=sonnet, author=opus, reporter=sonnet). Well-formed per Guide §4.1. CLEAN.
- **Every "Read" ref / template exists** — `refs/{eval-contracts,create-pipeline,run-pipeline,
  integration-map}.md` and `templates/{run-report.md,suite-manifest.yaml}` all present on disk; SKILL.md's
  per-wave "Refs Loaded" declarations point only at files that exist. CLEAN.
- **All cited source files exist** — loader's canonical sources (`cli/eval/{loader,runner,models,
  run_report,commands,artifact_layout,exit_codes}.py`, `suite.schema.json`, the two exemplar manifests
  `eval_smoke.yaml`/`installer_sync_drift.yaml`, `docs/eval/{suites-guide,runtime,validation-commands,
  retry,scratch-roots}.md`) all resolve. No dangling citation. CLEAN.
- **Contract-claim accuracy (high value)** — every contract value the package asserts matches source:
  exit codes `0/1/2/3` = `exit_codes.py:21-24` (incl. FR-G5→`USAGE_ERROR=2`); `eval list --json` →
  `{name,version,eval_count}` = `commands.py:757,929`; schema top-level required + `additionalProperties:false`
  = `suite.schema.json:7,16,127`; status enum + per-eval keys match `models`/`run_report`. CLEAN.
- **The `--json` suppresses-the-null-executor-warning claim** — asserted in `SKILL.md:162`,
  `refs/run-pipeline.md:63`, `templates/run-report.md:12`, and `agents/eval-run-reporter.md:27,60`.
  Verified against `commands.py:1879`: `if getattr(executor_factory, "produces_null_executor", False)
  and not as_json:` — the `results MUST NOT be treated as authoritative` warning is indeed suppressed by
  `--json`. The package's authoritativeness narrative is factually correct. CLEAN.
- **CLAUDE.md — `.claude/` staging** — NO instruction anywhere to stage/commit `.claude/`. SKILL.md "Will
  Not Do" (`:220`) and `agents/eval-suite-author.md:63` both correctly state "Edit `.claude/` ... source of
  truth is `src/superclaude/`; sync via `make sync-dev`." CLEAN / actively compliant.
- **CLAUDE.md — no new `superclaude eval` CLI flags** — asserted ≥6× (command Usage note, Boundaries,
  SKILL.md Purpose/Will-Not, both refs) and consistent with the run pipeline being pure orchestration. CLEAN.
- **CLAUDE.md — workspace sink override** — all generated artifacts route to
  `.dev/eval-workspaces/cli-eval/{design,runs}/`, never `.claude/skills/*-workspace/`. Matches the
  project's skill-creator destination override exactly. CLEAN.
- **Reuse-surface claims** — `--mode critique` verified in `commands/spec-panel.md:22`;
  `--compare`/`--source`/`--generate`/`--agents` verified in `commands/adversarial.md:15-17`;
  `--type guide` verified in `commands/document.md:22`. integration-map's invocation surface is accurate. CLEAN.

---

## Summary

- **HIGH: 0**
- **MED: 1** — B1: direct `Skill sc:spec-panel`/`sc:document` invocation contradicts cli-portify's
  explicit "no inter-skill command invocation" (Constraint 1) decision, undeclared/unreconciled.
- **LOW: 3** — B3: mixed `-protocol`-suffix vs bare naming in the Delegation table reads like a typo;
  B4: command uses `## Behavioral Summary` vs the guide's mandated `## Behavioral Flow` (but matches the
  thin-command precedent); B5: no degraded-mode probe/fallback for reused skills (reflect has one).
- **Clean & verified**: B2 (adversarial reuse correct + precedented) plus 18 explicitly-checked
  conformance points — Activation verbatim, naming triad, both frontmatter sets, command⇄skill parity,
  agent-name resolution, every ref/template/cited-source exists, exit-code/schema/`--json`-suppression
  contract accuracy, and all three CLAUDE.md governance axes (no `.claude/` staging, no new eval flags,
  correct `.dev/` sink).

The package hangs together. No dangling agent names, no missing refs, no invented contract values, no
governance violation. The one substantive issue is a philosophical inconsistency with the sibling
cli-portify skill over command-as-skill reuse (B1) that should be reconciled in prose, not a broken link.
