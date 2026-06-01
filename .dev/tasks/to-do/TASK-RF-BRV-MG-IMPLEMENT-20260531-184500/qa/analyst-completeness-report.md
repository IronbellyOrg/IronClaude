# Research Completeness Verification — BRV-MG task-builder track

**Date:** 2026-05-31
**Files analyzed:** 2 research files (R1, R2)
**Analysis type:** completeness-verification
**Analyst scope:** 01-sibling-skill-template-and-reflect-cmd.md, 02-workflow-evalworkspace-refs.md

---

## Critical Spot-Check: Flat command-file path claim

**R1 §0 claim:** Source-of-truth commands directory at IronClaude is **flat** at `src/superclaude/commands/`; the `sc/` subdir only exists in synced `.claude/commands/sc/`.

**Verification (Bash `ls`):**
- `/config/workspace/IronClaude/src/superclaude/commands/` — exists, **flat**, contains 40 `.md` files including `reflect.md` and `auggie-review.md` at top level.
- `/config/workspace/IronClaude/src/superclaude/commands/sc/` — **does NOT exist** (`ls: cannot access ...: No such file or directory`).

**Verdict: R1's claim is CORRECT.** The task brief's `commands/sc/reflect.md` and `commands/sc/auggie-review.md` paths are wrong for source-of-truth edits. Executor MUST edit:
- `/config/workspace/IronClaude/src/superclaude/commands/reflect.md`
- `/config/workspace/IronClaude/src/superclaude/commands/auggie-review.md` (template only, read)
- New: `/config/workspace/IronClaude/src/superclaude/commands/pr-bot-validate.md`

Then `make sync-dev` copies to `.claude/commands/sc/`.

**Implication:** If a research-notes.md exists referencing `commands/sc/...` paths, it needs correction. (No research-notes.md found in the research/ directory — see Gap G-1 below.)

---

## 9-Item Checklist Results

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Source files identified with paths and exports | PASS | R1 §0/§1/§3/§4 cite SKILL.md:1-12, :47-61, :62-73, :355-366, :487-576; commands/reflect.md:258-265; commands/auggie-review.md:1-9, 11, 13, 23, 33, 44, 57, 66-71, 73, 80, 90, 141, 163. R2 §1 cites publish-pypi.yml:21-22,28,110; pull-sync-framework.yml:3-6,10,11; readme-quality-check.yml:3-10,12-15,21; Makefile:1, 493-505. |
| 2 | Output paths and formats clear | PASS | All target paths are absolute: skill at `/config/workspace/IronClaude/src/superclaude/skills/sc-pr-bot-validate-protocol/SKILL.md`; refs at `refs/bot-review-sources.yaml`; command at `commands/pr-bot-validate.md`; workflow at `.github/workflows/pr-bot-validate.yml`; eval workspace at `.dev/eval-workspaces/sc-pr-bot-validate/`; falsifier at `cases/falsifier-suite/pr-bot-validation-mixed-buckets.yaml`. |
| 3 | Logical breakdown of phases | PASS | R1 §6 lays out Phases 2-4 (skill dir + SKILL.md → command file → reflect.md edit); R2 §2-7 covers Phase 5 (workflow, eval workspace, ref file, Makefile, falsifier). Phase 1 (preflight) handed to executor; phases align with merged proposal Change list. |
| 4 | Patterns + conventions documented | PASS | R1: 2-block frontmatter pattern (YAML + HTML comment); wave anatomy (Preconditions/Steps/Exit-criteria); error-handling 3-column table; activation-block pattern. R2: workflow permissions idiom; GITHUB_TOKEN auto-injection; grader COPY+extend pattern; ref-file YAML header convention; `.PHONY` update at Makefile:1. |
| 5 | MDTM template notes present | PARTIAL | R1 §6 supplies per-step Edit operation blueprints (Step 2.1/2.2, Step 3.1, Step 4.1 with verbatim old_string/new_string at §3.3); R2 supplies recipe sketches. **However, neither file references the MDTM frontmatter schema (status, branch, complexity_tier, etc.) the task-builder will need.** See Gap G-2. |
| 6 | Granularity sufficient for per-file checklist items | PASS | Per-file work is decomposed: SKILL.md skeleton enumerates 16 section-level items (§6 Phase 2 lines 374-389); command file mirrors 12 sections (§4.2); reflect.md edit is a single-bullet insertion with verbatim text (§3.3); workflow YAML is fully drafted (§2); ref file is fully drafted (§6); falsifier YAML is fully drafted (§5); Makefile recipe is fully drafted (§7). Executor can checklist each. |
| 7 | Doc-sourced claims tagged with verification status | PARTIAL | All structural claims are CODE-VERIFIED via line citations from real files at `/config/workspace/IronClaude/`. No claim relies on stale documentation. **However, neither file uses explicit `[CODE-VERIFIED]` / `[UNVERIFIED]` tags.** Tagging is implicit through line citations rather than explicit. Acceptable for this depth tier but worth noting. See Gap G-3. |
| 8 | Solution research evaluated approaches | PASS | R1 §5.1 evaluates `__init__.py` parity (mixed pattern, no convention required — recommends omit, with rationale). R2 §4 evaluates grader strategy (COPY+extend vs import; chose COPY with 3-point rationale). R2 §7 evaluates Makefile param refactor vs copy-rename (chose copy). R1 §3.3 evaluates insertion-point alternatives (after `/sc:troubleshoot` vs end-append). |
| 9 | Unresolved ambiguities documented; §16 content drift resolved | PASS | R1 §0 + §3.4 explicitly resolve the proposal's "§16 Related Commands" content-drift: SKILL.md §16 = "Refs" (line 1387); actual `## Related Commands` lives in command file at `commands/reflect.md:258`. R2 §2 + §8 flag two pre-implementation blockers: (a) claude CLI install on runner, (b) ANTHROPIC_API_KEY repo secret. R2 §6 leaves `sync_source` value as `<spec-path> §<X>` placeholder pending §-number resolution by executor. |

---

## Coverage Audit

| Required artifact (per task brief) | Covered by | Status |
|---|---|---|
| Sibling skill `sc-pr-bot-validate-protocol/SKILL.md` template | R1 §1 (auggie template) + §2 (reflect §9 contract pattern) + §6 (skeleton enumeration) | COVERED |
| New ref file `refs/bot-review-sources.yaml` | R2 §6 (verbatim YAML, 6 bots) | COVERED |
| New slash command `commands/pr-bot-validate.md` | R1 §4 (auggie-review.md template, 12-section mirror) | COVERED |
| New GitHub workflow `pr-bot-validate.yml` | R2 §1 (closest pattern) + §2 (verbatim draft) | COVERED |
| New eval workspace `.dev/eval-workspaces/sc-pr-bot-validate/` | R2 §3 (layout) + §4 (grader strategy) + §5 (falsifier YAML) | COVERED |
| 1 active falsifier `pr-bot-validation-mixed-buckets.yaml` | R2 §5 (verbatim YAML, adapted from T2-judge-class-collision.yaml) | COVERED |
| One-line edit to reflect command file Related-Commands section | R1 §3.3 (verbatim Edit operation blueprint) | COVERED |
| Makefile targets (`pr-bot-validate-eval`, `-quick`) | R2 §7 (recipe sketch + `.PHONY` update) | COVERED |
| Sync discipline (`make sync-dev` + `make verify-sync`) | R1 §3.4 + §6 Phase 5 | COVERED |

**All 9 task-brief artifacts covered.** No scope items missing.

---

## Evidence Quality

| Research File | Evidenced Claims | Unsupported Claims | Quality Rating |
|---|---|---|---|
| 01-sibling-skill-template-and-reflect-cmd.md | ~40 (line-cited file refs, verbatim YAML blocks, exact section headers with line numbers) | 0 | Strong |
| 02-workflow-evalworkspace-refs.md | ~35 (grep-verified greenfield claim, workflow-table line citations, grader self-description quotes) | 0 | Strong |

---

## Documentation Staleness

No doc-sourced claims requiring `[CODE-VERIFIED]` / `[CODE-CONTRADICTED]` tags. All claims sourced from live code/config files at known paths. The single content-drift between the merged proposal text ("§16 Related Commands") and reality (`commands/reflect.md:258 ## Related Commands`) is explicitly identified and resolved by R1.

---

## Completeness

| Research File | Status | Summary | Gaps Section | Key Takeaways | Rating |
|---|---|---|---|---|---|
| 01-sibling-skill-template-and-reflect-cmd.md | Complete | Y (§7) | N (subsumed into Summary "Blockers: None") | Y (§7 5-item list) | Complete |
| 02-workflow-evalworkspace-refs.md | Complete | Y (Summary) | Y (Blocker section in §2 + §8) | Y (Summary bullets) | Complete |

---

## Contradictions Found

None between R1 and R2. They cover disjoint scopes that compose cleanly:
- R1: skill structure, command file, reflect.md edit, parity audit.
- R2: workflow, eval workspace, grader, ref file shape, Makefile.
- Overlap point — `refs/` directory existence: R1 §5.2 says "mandatory for new sibling; R2 will detail." R2 §6 supplies the file. Consistent.
- Overlap point — `evals/` subdir: R1 §5.3 says skill does NOT need an `evals/` subdir for v1.0 because falsifier lives under `.dev/eval-workspaces/`. R2 §3 confirms the falsifier lives at `.dev/eval-workspaces/sc-pr-bot-validate/cases/falsifier-suite/`. Consistent.

---

## Compiled Gaps

### Critical Gaps (block synthesis) — 0

None.

### Important Gaps (affect quality) — 3

- **G-1: research-notes.md absent.** Task brief said "Also read parent research-notes.md" but no such file exists in `/config/workspace/Coder/.dev/tasks/to-do/TASK-RF-BRV-MG-IMPLEMENT-20260531-184500/research/`. Only R1, R2, and (per ls output) `qa-research-gate-report.md`... but the qa file also does NOT exist on `grep` (ENOENT). Directory contains only R1 + R2. **Source:** task brief + actual `ls`. **Impact:** A claimed scope-discovery/ambiguities document is missing. The §16 content-drift resolution lives instead inside R1 §0 + §3.4 — substantively present, just not in the expected meta-file. **Fix:** task-builder should either (a) create a research-notes.md that consolidates AMBIGUITIES and EXISTING_FILES from R1+R2, or (b) confirm the per-file resolution in R1 §0 is the authoritative source and skip the meta-file.
- **G-2: MDTM frontmatter schema not enumerated.** Neither R1 nor R2 documents the MDTM task-file frontmatter fields (status, branch, complexity_tier, related_skill, etc.) that task-builder will need to populate. **Source:** absence in R1/R2. **Impact:** task-builder must rely on its own template knowledge rather than research-supplied schema. Acceptable but worth flagging. **Fix:** task-builder reads its own MDTM template at skill-load time; no research action required.
- **G-3: Verification tags implicit, not explicit.** R1/R2 cite line numbers but do not annotate claims with `[CODE-VERIFIED]` tags. **Impact:** Low — line citations are functionally equivalent and traceable. **Fix:** None needed for this depth tier.

### Minor Gaps — 2

- **M-1: `sync_source` `<spec-path> §<X>` placeholder in R2 §6.** The bot-sources YAML header references a spec section number that isn't resolved. Task-builder/executor must fill in the actual spec section when authoring the file.
- **M-2: Two pre-implementation blockers flagged by R2 require user/executor action.** (a) claude CLI install step on Actions runner (not in any existing workflow); (b) `ANTHROPIC_API_KEY` repo secret must be configured. Both are correctly surfaced; neither is a research gap, but the task file's pre-flight checklist must include them.

---

## Depth Assessment

**Expected depth:** Standard-to-Deep (implementation-ready research for a multi-artifact task).
**Actual depth achieved:** Deep. Both files include verbatim source quotations, exact line numbers, alternative-approach evaluations with rationale, and ready-to-execute Edit/Write blueprints.
**Missing depth elements:** None.

---

## Recommendations

1. **Proceed to synthesis/task-builder phase.** Both research files are implementation-ready.
2. **task-builder should incorporate the path correction from R1 §0** — all source-of-truth edits target flat `src/superclaude/commands/` paths, not `commands/sc/`.
3. **task-builder should embed R2 §2 blocker resolution as a Phase-1 pre-flight checklist item** — verify `claude` CLI install strategy AND `ANTHROPIC_API_KEY` secret presence before any workflow file is committed.
4. **task-builder should resolve the §-number placeholder in R2 §6** (`sync_source: ".dev/<spec-path> §<X>"`) by reading the merged proposal and substituting the actual section reference.
5. **Optional:** create a `research-notes.md` consolidating EXISTING_FILES and AMBIGUITIES_FOR_USER for downstream agents that expect that meta-file. Not blocking.

---

## VERDICT: **PASS** (with 3 important gaps, all non-blocking)

Research is sufficient for task-builder to proceed. The flat-command-file-path claim is verified correct. The §16 content-drift is explicitly resolved. All 9 scope artifacts have implementation-ready evidence. The 3 important gaps are advisory, not blocking.
