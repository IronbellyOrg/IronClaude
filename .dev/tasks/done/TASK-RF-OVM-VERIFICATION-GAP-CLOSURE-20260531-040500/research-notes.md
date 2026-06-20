# Research Notes: Implement OVM (Outcome-Verification Manifest) — sc-reflect protocol amendments

**Date:** 2026-05-31
**Scenario:** A (explicit — merged brainstorm proposal at MERGED-PROPOSAL.md is concrete BUILD_REQUEST)
**Depth Tier:** Standard
**Track Count:** 1

---

## EXISTING_FILES

- `/config/.claude/skills/sc-reflect-protocol/SKILL.md` — current v1.0 protocol (~1700 lines). Sections to amend (per merged proposal §3.1-3.7): frontmatter (allowed-tools), §3 (mode selection), §4.1 (Wave 1 — add Step 1B.4), §4.5 (Wave 5 — add outcome-verification pass), §6.1 (Serena chain — orthogonal extension), §7.1 (reviewer composition — no change needed), §9.1 (stable contract — add ~10 new fields + derived boolean), §10 (deviation taxonomy — preserves 4-category; routes failed external-spec as §10.4 Regression), §10.6 (grounding-gaps pattern — referenced but unchanged), §11.2 (evidence-validator — add schema + presence checks), §14.5.2 (promotion gate — add cond 10), §17.7 (Kill List — add explanation of route-around for 5th-category kill), §19.2 (deferred hardening — append INV-023 integration note).
- `/config/.claude/skills/sc-reflect-protocol/refs/` — existing refs directory. New file required: `claim-extraction-patterns.yaml` (per merged §3.1 / §3.7).
- `/config/.claude/commands/sc/reflect.md` — command file. Likely needs minor update for new contract fields visibility + the new step in mode-selection logic (TBD per builder).
- `/config/workspace/IronClaude/.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/` — does NOT currently exist; must be created. Per merged §7: 2 new YAML falsifier cases:
  - `outcome-verification-docker-cli-miss.yaml` (active iteration-1 fixture; the docker case)
  - `outcome-verification-deferred-runtime-config.yaml` (V-Deferred-Outcome sibling)
- `/config/.claude/templates/workflow/02_mdtm_template_complex_task.md` — MDTM template 02 (this builder's template).
- `/config/workspace/IronClaude/.dev/brainstorm/reflect-verification-gap-20260531/MERGED-PROPOSAL.md` — the authoritative input (5,303 words; 8 §7 sections; 14 numbered amendments).
- `/config/workspace/Coder/CLAUDE.md` — project conventions: "Validation should be done via the .github actions. One off validation scripts should be avoided." Source-of-truth = `src/superclaude/`, then `make sync-dev` → `.claude/`, then `make verify-sync`.

## PATTERNS_AND_CONVENTIONS

- **Source of truth = `src/superclaude/`.** Edit there first; mirror via `make sync-dev`; verify with `make verify-sync`. Never edit `.claude/` directly. Per project CLAUDE.md.
- **`.github actions` validation only.** No one-off validation scripts. Acceptance criteria should reference CI gates (e.g., `make reflect-eval-quick`, `make reflect-eval`, `make verify-sync`).
- **Eval-workspace location:** `.dev/eval-workspaces/sc-reflect/` per protocol §12. Falsifier cases per §12.5 schema.
- **MDTM template 02 patterns:** L1-L6 handoff patterns; per-phase QA gates; self-contained items (context + action + output + verification + completion gate); PER_PHASE QA when complex changes.
- **STRICT tier classification:** modifications to a protocol skill (sc-reflect-protocol) hit the STRICT tier per sc-task-protocol rules. Frontmatter must declare `compliance_tier: STRICT` (or equivalent — exact field per template 02).

## GAPS_AND_QUESTIONS

- Does `.claude/commands/sc/reflect.md` need amendments? Likely yes — `--no-doc-discovery`-like flags or new visibility for `outcome_verification_complete` field. Researcher 1 to verify and itemize.
- What MDTM frontmatter field encodes compliance tier? Researcher 2 to confirm from template 02.
- Existing falsifier files in `.dev/eval-workspaces/` — what shape do they take? Researcher 3 to scan.
- `make sync-dev` and `make verify-sync` targets — verify they exist and what they do. Researcher 2 to read the Makefile.
- Cross-skill propagation per merged §3.7: ref file is now single-skill, but sibling-skill awareness needs… nothing? Or a one-line note in each sibling skill (`sc:auggie-review`, `sc:cleanup-audit`, `sc:troubleshoot` Wave 6)? Per merged proposal §3.7 (Change 5 in refactor plan): sibling skills inherit by writing valid `outcome-claims.yaml`; NO sibling-skill edits required in this task. Confirmed by merged proposal.

## RECOMMENDED_OUTPUTS

The builder produces ONE MDTM task file at:
`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-OVM-VERIFICATION-GAP-CLOSURE-20260531-040500/TASK-RF-OVM-VERIFICATION-GAP-CLOSURE-20260531-040500.md`

The task file's checklist should drive the executor to produce these artifacts (in source-of-truth `src/superclaude/`, then synced to `.claude/`):
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md` — amended (12+ specific edits per merged §3.1-3.7 + frontmatter)
- `src/superclaude/skills/sc-reflect-protocol/refs/claim-extraction-patterns.yaml` — new ref file
- `src/superclaude/commands/sc/reflect.md` — amended if researcher 1 confirms surface changes
- `.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/outcome-verification-docker-cli-miss.yaml` — new
- `.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/outcome-verification-deferred-runtime-config.yaml` — new

After all edits: `make sync-dev` → `make verify-sync` → CI on PR.

## SUGGESTED_PHASES

Suggested 6-phase structure for the MDTM task:

1. **Preparation** — read MERGED-PROPOSAL.md; read current SKILL.md sections; verify scope.
2. **SKILL.md amendments** — apply 12+ ordered edits per merged §3.1-3.7 + frontmatter (`WebFetch`, `WebSearch`). One checklist item per amendment, citing merged section.
3. **New ref file** — create `refs/claim-extraction-patterns.yaml` per merged §3.1; populate with apt-get/pip/npm/gem/cargo/go get/gh api/aws/terraform patterns + classification rubric.
4. **Eval falsifier cases** — create 2 YAML falsifier cases per merged §7; active iteration-1 + sibling skeleton.
5. **Sync + verify** — `make sync-dev`; `make verify-sync`; `make lint`; commit on feature branch.
6. **Self-validation gate (eat dog food)** — invoke `Skill sc:reflect-protocol --mode post --diff <pre-task-ref>..HEAD --tasklist <this-task-file>` per merged §6.

Item-level granularity: per merged §3.1-§3.7 there are 7 mechanism subsections + ~5 contract field groupings + 4 supporting changes (taxonomy precedence, INV-002/003/005 mechanism additions, A-001/A-002 shared-assumption surfacings). Expect 18-30 distinct checklist items in Phase 2 alone. Total task file: ~40-55 items.

## TEMPLATE_NOTES

- **Template 02 (Complex Task)** — required. The task spans multiple phases with discovery (researcher 1 must verify edge cases like reflect.md surface), build (12+ SKILL.md edits + new files), test (CI gates), and self-validation (post-task reflect). PER_PHASE QA gates appropriate.
- **Compliance tier:** STRICT (protocol-text modification + multi-file + impact on §9.3 consumer-field-map consumers).
- **QA_GATE_REQUIREMENTS:** PER_PHASE (each phase ends with a `make verify-sync` or equivalent gate).
- **VALIDATION_REQUIREMENTS:** `make sync-dev`; `make verify-sync`; CI gates (`make reflect-eval-quick` if available, `make lint`).
- **TESTING_REQUIREMENTS:** Falsifier cases are the tests — eval workspace grader runs them. Active fixture must `expected: assertion holds` on the docker miss; skeleton fixture must satisfy `falsifier_skeleton_present` per merged §7 / §12.5.
- **EXECUTION_CONTEXT_REQUIREMENTS:** AUTO (rollup signal present — ≥3 named source areas: sc-reflect-protocol SKILL.md, refs/, eval-workspaces).

## AMBIGUITIES_FOR_USER

None blocking. All ambiguities are within research/builder scope (resolved by researchers 1-3 or by builder reading the merged proposal). The merged proposal is concrete enough to drive a fully-specified task file without further user input.
