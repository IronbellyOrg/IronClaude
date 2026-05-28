# Critique 1 — Architect Position

## Architect Position (Steelman)

The strongest version of variant-1-architect.md treats the orchestration as a
**dependency-ordered DAG with file-mediated handoffs**, not a narrative. Every
phase declares its inputs as file paths that MUST exist on disk, produces its
outputs as file paths the next phase can name without ambiguity, and routes
the user's slogan ("task-builder is authoritative") through a single
operational artifact — `conflict-register.md` — that downstream phases read,
write, and reconcile against panel feedback.

Three structural choices make this robust:

1. **Sequential MCP → persisted proposals.** The variant inserts an explicit
   Step 3.2 that converts Sequential thinking into discrete `proposals/proposal-NN-<slug>.md`
   files PLUS an `INDEX.md` manifest that becomes the literal `--compare`
   argument for Phase 4. The adversarial command requires 2–10 explicit file
   paths; the source prompt handwaves "Write each proposal as its own markdown
   file" without an enumeration step.

2. **Precedence enforcement is a file, not a slogan.** The
   `conflict-register.md` ledger is appended in Phase 3, consulted in Phase 5
   reflection, cited in Phase 6 exclusions, and used to filter Phase 7 panel
   revisions. The source's "task-builder takes precedence" rule appears five
   times as prose with no concrete enforcement surface.

3. **Phase 7 omits `--downstream roadmap`.** Per `spec-panel.md` Step 6b, the
   `--downstream roadmap` flag injects roadmap-oriented frontmatter that the
   downstream consumer (Phase 8 is the **prd** skill, not /sc:roadmap) does not
   read. The source's flag choice introduces dead frontmatter and risks the
   panel scoping the spec for the wrong consumer. Removing the flag is a
   defensible deletion, not flag invention.

## Critique of Source (Baseline)

Structural defects identified in `source-prompt.md`:

- **D1 — Phase 3 → Phase 4 handoff is implicit.** Source line 73–74 says
  "Write each proposal as its own markdown file under
  .dev/releases/current/task-builder-merge/proposals/." Sequential MCP is a
  reasoning tool; it does not write files. There is no explicit Write step,
  no file naming convention, and no enumeration manifest. Phase 4's
  `--compare <proposal-1.md,proposal-2.md,...>` will be ambiguous at invocation
  time. (Cite: source-prompt.md lines 50–74 vs lines 80–86; adversarial.md
  lines 36–37 require explicit file paths.)

- **D2 — "Task-builder precedence" is unenforced.** The rule appears at
  source-prompt.md lines 4–6, 67–69, 95, 107–108, and 122–123 but has no
  operational artifact. Phase 5 says "flag for revision" without naming where
  flags live; Phase 7 says "defend it with FINAL-REPORT evidence" without a
  decision log. The slogan cannot survive a multi-phase orchestration without
  a persistent ledger.

- **D3 — Phase 5 reflect inputs unspecified.** Source-prompt.md lines 91–95
  invoke `/sc:reflect --type task --analyze --validate` without telling
  reflect what to read. Reflect (`commands/reflect.md`) examines session state
  and produces analysis; in this orchestration its only meaningful scope is
  "verify the adversarial merge respects precedence", which requires explicit
  references to `adversarial/merge-log.md` and the precedence rule. The
  `--type task` choice is acceptable (mid-stream validation, not closeout) but
  the prompt does not articulate why.

- **D4 — Phase 6 inputs are implicit.** Source-prompt.md lines 99–111 describe
  the release spec sections but never state that Phase 6 must read the
  adversarial merge output and the reflection output before writing.
  Freshness-pre-edit hooks will pass (writes are first-creation) but the
  resulting spec risks drifting from the adversarially-validated portfolio if
  the author works from memory instead of files.

- **D5 — Phase 7 `--downstream roadmap` is incorrect for the actual downstream.**
  Source-prompt.md line 119 sets `--downstream roadmap` but Phase 8 (lines
  126–142) invokes the prd skill. Per `commands/spec-panel.md` lines 33–34,
  the `--downstream roadmap` switch populates roadmap-oriented frontmatter
  (`spec_type`, `complexity_score`, `target_release`, `feature_id`) intended
  for /sc:roadmap consumption. PRD does not consume this frontmatter. The
  flag should be omitted.

- **D6 — Phase 1 buckets overlap and miss the PRD template.** Bucket A
  (sc-tasklist-protocol skill) and Bucket B (tasklist command + cli) are
  artificially split; the CLI is a coupled implementation of the command, so
  treating them as one bucket reduces cross-bucket reference noise. Bucket F
  reads the release-spec template but not the PRD template, even though
  Phase 8 invokes the prd skill — Phase 1 should pre-load both schemas.

- **D7 — Output paths assume directories exist.** Source-prompt.md never
  declares the subdirectory structure under the output root (`proposals/`,
  `adversarial/`, etc.). Hook-compliant first writes need parent directories
  to exist; the source leaves this implicit. Combined with D1, this risks a
  Write failing because `proposals/` was never created.

- **D8 — Phase 1 bucket count + scope is large but not exhaustive.** Six
  buckets, but no bucket reads the existing release specs as shape references
  (Bucket F mixes template + samples). Splitting "schema" from "exemplars"
  would be cleaner; the variant collapses to schema-only since exemplars are
  not load-bearing for this orchestration.

## Acknowledged Weaknesses of My Variant

- **W1 — Conflict-register.md is a new artifact not in the user's stated
  outputs.** It adds one file to the deliverable set. The user could
  legitimately argue this is scope creep. Defense: the slogan in the source
  cannot be operationalized without some persistent precedence surface; a
  single ledger file is the minimum.

- **W2 — Phase 3 has more steps (3.1 → 3.4) than the source.** This adds
  ceremony to a brainstorm. Defense: the ceremony is the file-writing and
  enumeration that the source omits; the brainstorm itself is unchanged.

- **W3 — Removing `--downstream roadmap` is a behavioral deletion that some
  reviewers may flag as introducing a regression in the spec frontmatter.**
  Defense: the source's choice was wrong for the downstream consumer; either
  the source's frontmatter is dead, or it would mislead a future
  /sc:roadmap invocation against this spec.

- **W4 — Variant collapses Buckets A+B into a coupled-unit framing.** Some
  reviewers will see this as reducing the parallelism budget. Defense: the
  CLI is the implementation of the command; reading them apart inflates
  cross-references rather than gathering distinct context.

- **W5 — Adversarial pass-batching (Step 4.1) adds branching complexity for
  the >10-proposal case.** Source ignores the case entirely. Defense:
  adversarial.md Mode A caps at 10; batching is the only structural answer.

- **W6 — `--type task` for Phase 5 reflect is defensible but not maximally
  fitted.** `reflect --type completion` could be argued for end-of-portfolio
  validation. Defense: the orchestration is not yet complete (Phases 6–8
  remain), so `--type task` correctly characterizes mid-stream task adherence
  validation.

## Diff Points Raised

- **S-001 — Phase-3 proposal materialization.** Source: implicit / handwaved.
  Variant: explicit Write step (3.2) + INDEX.md manifest (3.4). Rationale: D1.

- **S-002 — Conflict-register.md as precedence enforcement surface.** Source:
  none. Variant: file created in Phase 1.0, appended in 3.3 / 5.3 / 7.3, read
  by 6.1 / 7.3 / 8.2. Rationale: D2.

- **S-003 — Phase-5 reflect scope made explicit.** Source: bare invocation.
  Variant: scoped prompt naming the merge-log and the precedence rule.
  Rationale: D3.

- **S-004 — Phase-6 explicit input read list.** Source: implicit. Variant:
  Step 6.1 enumerates the six input artifacts that must exist before drafting.
  Rationale: D4.

- **S-005 — Removed `--downstream roadmap` from Phase 7.** Source: present.
  Variant: omitted with documented rationale. Rationale: D5 (flag removal, not
  invention).

- **S-006 — Phase-1 bucket re-partition.** Source: 6 buckets with A/B split
  and F=template+samples. Variant: 6 buckets with A/B coupled (skill + cli
  treated as coupled unit by joining E to include the adversarial command file)
  and F = both PRD and release-spec schemas. Rationale: D6, D8.

- **S-007 — Subdirectory pre-creation as Phase 1 Step 0.** Source: implicit.
  Variant: explicit Step 1.0 creates `context-digests/`, `analysis/`,
  `proposals/`, `adversarial/`, `reflection/` plus touches
  `conflict-register.md`. Rationale: D7, hook compliance.

- **S-008 — Adversarial pass-batching for >10 proposals.** Source: silent.
  Variant: Step 4.1 defines pass-batching with pass-N subdirectories.
  Rationale: Mode A's 10-file cap.

- **S-009 — Structural Invariants block (Precondition 0).** Source: invariants
  scattered across "Global Constraints" at the end. Variant: hoisted to the
  top as I0–I3 so every phase reads them before executing. Rationale: phase
  ordering — invariants must precede the phases they constrain.

- **S-010 — Phase 8 supporting inputs handed to the prd skill.** Source: PRD
  receives only INPUT_SPEC. Variant: adds SUPPORTING_INPUTS listing
  conflict-register, merge-log, and reflect output so the PRD can trace
  decisions. Rationale: PRD skill consumes additional context per its WHERE
  semantics; explicit > implicit.
