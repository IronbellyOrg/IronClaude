# Track 4 Research — T4 Real-Card Extraction + Template 01 + Makefile/Pre-commit Conventions

**Researcher:** Track 4 / Researcher 3 (t4-cards-and-template)
**Status:** Complete
**Topic:** Locate T4 hypothesis-card source for Fixtures 7-9; document MDTM Template 01 fit, Makefile sync targets, pre-commit hooks, and Change B precedent for a wholly-new refs file.
**Output file:** `.dev/tasks/to-do/TASK-RF-track-4-change-e-eval-cases-corpus-20260527-044000/research/03-t4-cards-and-template.md`

---

## Section 1 (PRIORITY): T4 Real-Card Directory Hunt

### 1.1 Search results (verbatim find output)

**Command (a):** `find /config/workspace/IronClaude -maxdepth 8 -type d -name "*t4*" 2>/dev/null`

```
/config/workspace/IronClaude/.dev/test-fixtures/results/test4-spec
/config/workspace/IronClaude/.venv/lib/python3.12/site-packages/jsonschema_specifications/schemas/draft4
/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2/.dev/test-fixtures/results/test4-spec
/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.dev/test-fixtures/results/test4-spec
/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/.dev/test-fixtures/results/test4-spec
```

NO `t4-pane-title-*` match. `test4-spec` directories are unrelated (CLI fixture test outputs).

**Command (b):** `find /config/workspace/IronClaude -maxdepth 8 -type d -name "*pane-title*" 2>/dev/null`

```
(empty)
```

NO `pane-title` directory exists anywhere in the searched tree.

**Command (c):** `find /config/workspace/IronClaude -maxdepth 8 -name "tier2-h*.md" 2>/dev/null | head -20`

```
(empty)
```

NO files named `tier2-h1-*.md`, `tier2-h2-*.md`, or `tier2-h3-*.md` exist at any depth in the searched tree. (Note: existing tier2 calibrations use agent-role naming like `tier2-quality-engineer-hypothesis.md`, not `tier2-h{N}-*.md`.)

**Command (d) — wider search with 10-depth + `*20260526-101500*` pattern:**

```
(empty)
```

No directory with the 20260526-101500 timestamp at depth up to 10.

### 1.2 Conclusive finding

**The directory `t4-pane-title-20260526-101500` referenced in the Change E proposal for the source of Real-card Replay Fixtures 7-9 DOES NOT EXIST in this worktree's filesystem at any of the searched paths (max depth 10, including the main checkout, all sibling worktrees, and `.dev/` subtrees).**

Hypotheses for the mismatch (not load-bearing for the task; document for future investigation only):

1. The proposal author was referencing a transient/local directory on a different host or session that was never committed.
2. The directory may have existed on a now-purged path inside another worktree that was removed.
3. The proposal author may have used a placeholder name reflecting an intended-but-not-actualized run.

### 1.3 Closest analog found (recommended fallback source)

The directory `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/` exists and contains the SAME artifact pattern referenced by the proposal:

**Directory listing (verbatim `ls -la`):**

```
tier1-hypothesis.md                              7970 bytes
tier2-quality-engineer-calibration.md            2697 bytes
tier2-quality-engineer-hypothesis.md            18432 bytes
tier2-refactoring-expert-hypothesis.md          10415 bytes
tier2-root-cause-analyst-calibration.md          2569 bytes
tier2-root-cause-analyst-hypothesis.md           9596 bytes
```

This is a Tier-1 + 3×Tier-2 hypothesis-card sweep with calibration reports for two of the three Tier-2 cards. Timestamp is `20260526100600` (2026-05-26 10:06:00) — close to the proposal's referenced `20260526-101500` (2026-05-26 10:15:00), strongly suggesting this IS the run the proposal author intended to reference (off by ~9 minutes, perhaps a copy-paste from a sibling run record).

**This analog directory's contents are sufficient to extract the actual card properties needed for Fixtures 7-9.** Specifically:

#### Fixture 9 analog source (H1 / Tier 1)

- File: `tier1-hypothesis.md` (7970 bytes)
- Calibration: NO separate `tier1-calibration.md` in THIS directory (the agent's calibration was inline in the audit log).
- Cause class: documentary defect (PR review issue — "wrong contract for hub dispatch")
- Self-reported confidence: NOT directly extracted from this analog; use the proposal's stated 0.82 CONFIRM.

#### Fixture 8 analog source (H2 / Tier 2 — WebFetch/GitHub URL evidence)

- File: `tier2-quality-engineer-hypothesis.md` (18432 bytes)
- Calibration: `tier2-quality-engineer-calibration.md` exists, captured below.
- Calibration findings (verbatim from `tier2-quality-engineer-calibration.md`):
  - Self-reported: **0.88**
  - Calibrated: **0.60**
  - Delta: **-0.28** — drag from fix-directness (broad change surface) and unverifiable PR-sha citations.
  - Per-dimension: evidence-grounding 0.5, symptom-coverage 1.0, reproducibility 1.0, fix-directness 0.5, domain-coherence 1.0.
  - Notable rubric note: "Per-card grounding limitation same as the other two Tier 2 calibrations" — PR-sha-specific citations could not be spot-checked without Bash; **PR-sha citations are the source-vs-runtime evidence-gap signature that motivates Change A's evidence_grounding cap.**

#### Fixture 7 analog source (H3 / Tier 2 — options-subcommand style)

- The closest H3 analog in this directory is `tier2-root-cause-analyst-hypothesis.md` (9596 bytes) with calibration `tier2-root-cause-analyst-calibration.md`.
- Calibration findings (verbatim):
  - Self-reported: **0.88**
  - Calibrated: **0.90**
  - Delta: **+0.02** — calibrator rewards mechanical strength + discipline of splitting off F2/F4.
  - Per-dimension: evidence-grounding 0.5, symptom-coverage 1.0, reproducibility 1.0, fix-directness 1.0, domain-coherence 1.0.
  - Verdict: STOP (Tier 2; calibrated 0.90 ≥ 0.85).

### 1.4 Recommended fallback strategy (for the task file)

Given Section 1.2 (T4 source not found) and Section 1.3 (close analog directory found), the task file should ship Fixtures 7-9 with the **proposal-described properties** (claim_class / evidence_class / verdict_direction / scores per proposal L334-344) embedded INLINE in `calibrator-eval-cases.md` as structured fixture sections, **WITHOUT** path-references to the original card files. Rationale:

1. **Path-references would be broken in CI / portable across environments** (the analog directory `pr86-integration-contracts-20260526100600` exists in this worktree but may not exist in clean checkouts; using its path would make the corpus non-portable). The proposal's L298-370 already provides the structured fixture content as inline prose — preserve that pattern.
2. **Inline content is reproducible** — anyone reading the corpus can verify the expected calibrated scores against the stated card properties without needing access to the source cards.
3. **A follow-up commit can backfill source paths IF the original T4 directory is later located** — leave a brief footnote in the corpus's "Real-card Replay Fixtures" section noting that the original H1/H2/H3 cards were drawn from a sc-troubleshoot run on 2026-05-26 (no specific path), and the inline content reflects the OBSERVED calibration deltas for those cards.

**Concrete recommendation for the task file's Phase 3 (Real-card fixtures):** use the inline prose pattern from the proposal verbatim. Do not introduce path references. Do not block the task on locating the T4 source.

---

## Section 2: Template 01 Fit for New-File Creation

**Template path (verified):** `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.claude/templates/workflow/01_mdtm_template_generic_task.md` (sync-dev mirror of `src/superclaude/templates/workflow/01_mdtm_template_generic_task.md` — verified present).

### 2.1 Selection rationale

Template 01 (Generic) IS the appropriate template for Change E. Confirmed by:

1. **Change B (PR-#89 precedent) used Template 01** — frontmatter line 31: `template_schema_doc: "src/superclaude/templates/workflow/01_mdtm_template_generic_task.md"`. Change E has the same structural shape (single file, deterministic content fully specified in proposal, no discovery for the bulk of the file).
2. **Template 01's Part 1 Section B (Self-contained checklist items)** matches Change E's needs — every checklist item embeds context + action + output + integrated verification + completion gate.
3. **Template 01's Section I3 (Incremental file modification)** explicitly mandates the "DO NOT attempt to complete entire files at once" pattern — matches the Section 7 recommendation here.

### 2.2 Difference from Change B

| Aspect | Change B (existing file edit) | Change E (new file create) |
|---|---|---|
| Primary tool | Edit (5 insertion blocks into existing 108-line file) | Write (initial header + frontmatter) + Edit (append each section incrementally) |
| Baseline read | Required (target file state already captured by researcher) | Not required for target file (doesn't exist); STILL required for refs/ directory siblings to confirm header conventions |
| Anchor strings | Three precise anchor points for surgical insertion | N/A (creating from scratch) |
| Lint risk | Low (additive content matches existing style) | Higher (new file must lint cleanly on first pass; existing siblings provide style template) |

### 2.3 Discovery scope for Change E

Section 1 of THIS research file is the ONLY discovery component — once the fallback strategy (inline content, no path references) is decided, the file content is fully specified by the proposal L298-370. No further discovery is needed in the task's Phase 2+.

---

## Section 3: Sync-Dev + Verify-Sync Workflow

**File:** `/config/workspace/IronClaude/Makefile`

### 3.1 sync-dev target (L108-163)

**Anchor line:** `Makefile:L108`: `# Sync src/superclaude/{skills,agents} → .claude/{skills,agents} for local dev`
**Target declaration:** `Makefile:L109`: `sync-dev:`

**Skill subtree handling (L112-125):**

```makefile
@for skill_dir in src/superclaude/skills/*/; do \
    skill_name=$$(basename "$$skill_dir"); \
    case "$$skill_name" in __*) continue;; esac; \
    if [ -f "$$skill_dir/SKILL.md" ] || [ -f "$$skill_dir/skill.md" ]; then \
        mkdir -p ".claude/skills/$$skill_name"; \
        find "$$skill_dir" -type f ! -name '__init__.py' ! -path '*/__pycache__/*' -exec sh -c ' \
            src="$$1"; skill_dir="$$2"; target_base="$$3"; \
            rel=$${src#$$skill_dir}; \
            target_dir="$$target_base/$$(dirname "$$rel")"; \
            mkdir -p "$$target_dir"; \
            cp "$$src" "$$target_dir/" \
        ' _ {} "$$skill_dir" ".claude/skills/$$skill_name" \; ; \
    fi; \
done
```

**Critical for Change E:** the `find ... -type f` recursion at L117 will copy `src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` to `.claude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md`. The `refs/` subdirectory structure IS preserved (line `target_dir="$$target_base/$$(dirname "$$rel")"` computes the relative path; `rel=refs/calibrator-eval-cases.md` → `target_dir=.claude/skills/sc-troubleshoot-protocol/refs`).

**Success path:** L158 prints `✅ Sync complete.` and L159-163 print counts. Exit code 0.

**Failure modes:** if the source SKILL.md is missing OR a `cp` fails (e.g., permission denied), exits non-zero with stderr from the shell loop.

### 3.2 verify-sync target (L165 onwards)

**Anchor line:** `Makefile:L165`: `# Verify src/superclaude/ and .claude/ are in sync (CI-friendly, exits 1 on drift)`
**Target declaration:** `Makefile:L166`: `verify-sync:`

**Skills drift check (L171-187):**

```makefile
for skill_dir in src/superclaude/skills/*/; do \
    name=$$(basename "$$skill_dir"); \
    case "$$name" in __*) continue;; esac; \
    if [ ! -d ".claude/skills/$$name" ]; then \
        echo "  ❌ MISSING in .claude/skills/: $$name"; \
        drift=1; \
    else \
        changes=$$(diff -rq --exclude='__init__.py' --exclude='__pycache__' "$$skill_dir" ".claude/skills/$$name" 2>/dev/null); \
        if [ -n "$$changes" ]; then \
            echo "  ⚠️  DIFFERS: $$name"; \
            echo "$$changes" | sed 's/^/      /'; \
            drift=1; \
        else \
            echo "  ✅ $$name"; \
        fi; \
    fi; \
done
```

**Exit semantics:** if `drift=1` was set anywhere, the target exits 1. CI-friendly per the comment.

**Reverse check (L188-200):** also verifies that `.claude/skills/*/` entries have a source in `src/superclaude/skills/*/`. If a skill exists in `.claude/` but not in `src/`, prints `❌ MISSING in src/superclaude/skills/: $name (not distributable!)` and sets drift=1.

**For Change E:** the new file lives inside the already-mirrored `sc-troubleshoot-protocol` skill subtree; verify-sync will run `diff -rq` between `src/superclaude/skills/sc-troubleshoot-protocol/` and `.claude/skills/sc-troubleshoot-protocol/`, which after sync-dev should show no differences. If sync-dev was NOT run after the new file lands in src/, verify-sync will print `⚠️ DIFFERS: sc-troubleshoot-protocol` with the file in the diff output.

### 3.3 Recovery paths

| Failure | Cause | Recovery |
|---|---|---|
| `verify-sync` reports `DIFFERS: sc-troubleshoot-protocol` after new-file create | Forgot to run `make sync-dev` after creating the file in src/ | Run `make sync-dev` then `make verify-sync` |
| `sync-dev` succeeds but file content differs in .claude/ | Stale .claude/ from a prior partial sync | Delete `.claude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md`, re-run `make sync-dev` |
| `verify-sync` reports `MISSING in src/` for an existing .claude/ file | New file accidentally edited in .claude/ first | NEVER edit .claude/ directly. Copy file content from .claude/ to src/, delete from .claude/, then sync-dev |

---

## Section 4: Markdownlint Hook

**File:** `/config/workspace/IronClaude/.pre-commit-config.yaml`

### 4.1 Hook definition (L70-82)

**Verbatim content:**

```yaml
  # Markdown linting
  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.38.0
    hooks:
      - id: markdownlint
        args: ['--fix']
        exclude: |
          (?x)^(
            CHANGELOG\.md|
            .*node_modules.*|
            .*\.min\.md$|
            \.dev/.*
          )$
```

| Field | Value |
|---|---|
| `repo` | `https://github.com/igorshubovych/markdownlint-cli` |
| `rev` | `v0.38.0` |
| `id` | `markdownlint` |
| `args` | `['--fix']` (autoFix mode — hook MAY modify the file in-place) |
| Exclude patterns | `CHANGELOG.md`, any `node_modules`, any `*.min.md`, anything under `.dev/` |

### 4.2 Does the new file get linted?

**YES.** The new file at `src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` is NOT in any exclude pattern:

- Not `CHANGELOG.md` (different filename)
- Not `node_modules` (not in that path)
- Not `*.min.md` (different suffix)
- Not under `.dev/` (it's under `src/`)

Therefore: the pre-commit markdownlint hook WILL lint this file on commit. After sync-dev, the mirror at `.claude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` is blocked from being staged separately (see Section 5), but if it ever appears in a commit it WOULD also be linted by the same rule (no path-based exclude for the `.claude/` mirror itself).

### 4.3 Lint risks for the new file

The `--fix` flag means markdownlint may auto-modify the file (e.g., fix trailing whitespace, normalize list markers, collapse blank lines). If this happens AFTER sync-dev, the source file in `src/` and the mirror in `.claude/` will drift. **Mitigation:** run pre-commit markdownlint on the source file BEFORE running sync-dev, OR re-run sync-dev after markdownlint reports auto-fixes.

Common autoFix triggers for new markdown files:

- MD009 (trailing whitespace)
- MD012 (multiple consecutive blank lines)
- MD030 (spaces after list markers)
- MD047 (file should end with single newline)

---

## Section 5: block-claude-generated-mirrors Hook + Source-of-Truth Rule

**File:** `/config/workspace/IronClaude/.pre-commit-config.yaml`

### 5.1 Hook definition (L98-109)

**Verbatim content:**

```yaml
  # AC11 / R-017 / T01.20 — source-of-truth discipline gate
  # Rejects generated `.claude/` mirrors on the commit path. Full mirror drift
  # remains available via `make verify-sync`, but pre-commit must not require
  # staging generated mirrors when this repository edits its own src/ sources.
  - repo: local
    hooks:
      - id: block-claude-generated-mirrors
        name: Block generated .claude mirror commits (AC11)
        entry: scripts/precommit_block_claude_mirrors.sh
        language: script
        pass_filenames: false
        files: '^\.claude/(skills|agents|commands|hooks|templates)/'
```

| Field | Value |
|---|---|
| `id` | `block-claude-generated-mirrors` |
| `entry` | `scripts/precommit_block_claude_mirrors.sh` |
| `files` regex | `^\.claude/(skills\|agents\|commands\|hooks\|templates)/` |
| Effect | If a staged file matches the regex (i.e., lives in `.claude/skills/`, `.claude/agents/`, `.claude/commands/`, `.claude/hooks/`, or `.claude/templates/`), the commit is REJECTED |

### 5.2 Source-of-truth rule (verbatim from project context)

From `/config/.claude/CLAUDE.md`:
> Source of truth is `src/superclaude/`. Always edit there first, then `make sync-dev`.

From memory `feedback_hooks_source_of_truth.md`:
> Never edit `~/.claude/` or `<project>/.claude/` directly; edit `src/superclaude/` then `make sync-dev`.

### 5.3 Consequence for Change E

- The new file MUST be created at `src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md`.
- `make sync-dev` will mirror it to `.claude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md`.
- The `.claude/` copy MUST NOT be staged for commit (the block hook will reject it).
- If the task accidentally creates the file in `.claude/` first, recovery is: copy content to `src/`, delete `.claude/` version, re-sync.

---

## Section 6: Known Gotchas for New-File Creation

(a) **sync-dev order:** ALWAYS create in `src/` first, then sync, then verify. NEVER edit `.claude/` directly. (See Section 5.)

(b) **markdownlint `--fix` may modify the file:** if the hook auto-fixes (e.g., adds trailing newline, normalizes list markers), the source `src/` file changes but the `.claude/` mirror is now stale. **Mitigation:** after running markdownlint, re-run `make sync-dev` and re-run `make verify-sync` to confirm zero drift.

(c) **block-claude-generated-mirrors rejects `.claude/` paths:** committing `.claude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` directly will fail the pre-commit hook. The intended commit surface is `src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` ONLY.

(d) **pre-commit install via uv pip install:** if pre-commit hooks have not been installed in the current environment, the lint gate is silently skipped. Verify with `pre-commit --version` and `pre-commit install` if not already installed. Use `uv run pre-commit run markdownlint --files <path>` to run the markdownlint hook against a specific file without committing.

(e) **NEW (Track-4-specific): H1 collision risk:** the new file's H1 `# Calibrator Eval Cases` should be unique within the skill's refs/ directory. Other researchers (refs-conventions) confirm existing siblings (`escalation-rubric.md`, `hypothesis-card-template.md`, `triage-checklist.md`) have distinct H1s. **No collision expected; verify in task Phase 1 baseline check.**

(f) **NEW (Track-4-specific): broken-link risk if Fixtures 7-9 reference real cards via path:** as established in Section 1.4, the original T4 directory does NOT exist in this worktree. If the corpus references the analog `pr86-integration-contracts-20260526100600` directory by path, the resulting markdown will render with broken links in any environment where `.dev/troubleshoot/` is gitignored or not present (note: `.dev/` IS excluded from markdownlint per the exclude pattern, so the link itself won't fail lint, but consumers reading the corpus would hit a missing path). **Recommendation: use inline content per Section 1.4.**

(g) **First-pass lint cleanliness:** because the file is new, every markdown rule must pass on first creation (no incremental drift forgiveness). Verify these rules pass during task Phase 2 by inspecting the staged file structure: (i) single H1 at top, (ii) blank line after H1, (iii) consistent list marker (proposal uses `-`), (iv) code fences with language tags, (v) no trailing whitespace, (vi) file ends with single newline.

---

## Section 7: Change B Precedent for New-File Creation

**Source task file:** `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.dev/tasks/done/TASK-RF-20260527-022700-change-b-hypothesis-card-schema/TASK-RF-20260527-022700-change-b-hypothesis-card-schema.md`

### 7.1 Scope comparison

| Aspect | Change B | Change E |
|---|---|---|
| Target | Edit existing 108-line file → ~138-153 lines | Create new ~70-line file |
| Insertion blocks | 5 paste-ready blocks (3 frontmatter, 1 row, 1+ sections) | 1 wholly-new file with ~9 fixtures + 5 property tests + suite-integrity + implementation-hook note |
| Tool pattern | Edit (Read first; surgical Edit with unique anchors) | Write (initial header) + Edit (append sections incrementally) |
| Validation | `make sync-dev` + `make verify-sync` + markdownlint on file | Same |
| QA gate | FINAL_ONLY (executor-performed structural check) | Same (per research-notes.md QA_GATE_REQUIREMENTS) |

### 7.2 Workflow transfer (what Change E inherits from Change B)

1. **Template 01 selection** — confirmed in Change B frontmatter L31; same in Change E.
2. **Tier Standard (4 researchers)** — Change E uses 4 researchers per research-notes.md.
3. **Two-phase execution: edit → sync-and-verify** — same shape; Phase 2 in Change E becomes "create file with sections appended incrementally."
4. **Lint integration:** Change B's Phase 2 ran `pre-commit run markdownlint --files <target>` after edits; Change E does the same on the new file.
5. **Frontmatter discipline:** status `🟠 Doing` at start, `🟢 Done` at completion, start_date and completion_date updated.
6. **Post-Completion Actions section** — verifies all outputs, task summary, frontmatter update.

### 7.3 Workflow divergence (what Change E adds)

1. **Initial Write call** for the file header + frontmatter (Change B started with Read of an existing file).
2. **Incremental section appends via Edit** — see Section 8 below for recommended phase structure.
3. **Section-1 Real-card resolution decision** is encoded in Phase 1 OR Phase 3 (the "inline-vs-reference" choice is now PRE-DECIDED per Section 1.4 of this research file — inline content, no path references).
4. **No code-fence boundary integrity check needed** (Change B had to preserve the existing template's open/close fence at L9 and L70; Change E has no pre-existing fences to preserve).

### 7.4 Single-shot Write vs. incremental Write + Edit

For a ~70-line file, a single-shot Write is technically feasible from a token-output perspective. However, **the incremental writing protocol from Template 01 Section I3 still applies**: "Require agents to add content incrementally as they progress" + "Explicitly state 'DO NOT attempt to complete entire files at once'" + "Include save points after major sections". Recommendation: initial Write for header + frontmatter, then Edit for each subsequent ## section. This preserves the surgical-Edit property and the freshness-pre-edit hook's safety guarantees.

---

## Section 8: Recommended Task Structure for Track 4

Based on Sections 1-7, the Change E task file should have the following phase structure:

### Phase 1: Status update + baseline checks

- **Step 1.1 (status):** Update frontmatter status to `🟠 Doing`, set start_date, log to Execution Log.
- **Step 1.2 (baseline):** Read research files (01-spec-extraction, 02-refs-conventions, 03-t4-cards-and-template — this file). Verify the target path `src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` does NOT yet exist (using Glob or Bash `test -f`). Verify refs/ directory exists.
- **Step 1.3 (sibling-style read):** Read the closest sibling refs file (e.g., `hypothesis-card-template.md` post-PR-#89) to confirm header conventions before writing the new file.

### Phase 2: Create file with header + frontmatter (Write)

- **Step 2.1 (Write header):** Create the new file with H1 `# Calibrator Eval Cases (Pin-Test Corpus)` (or proposal-specified title), one-paragraph intro, and any required frontmatter (NOTE: refs/ markdown files in this skill do NOT use YAML frontmatter — verify via sibling read in Step 1.3; if no frontmatter is the convention, skip it).

### Phase 3: Append each ## section incrementally (Edit)

- **Step 3.1 (Synthetic Fixtures 1-6):** Edit-append the first H2 section with Fixtures 1-6 (six synthetic fixtures per proposal L298-330).
- **Step 3.2 (Real-card Replay Fixtures 7-9):** Edit-append the second H2 section with Fixtures 7-9, using **inline content per Section 1.4** (no path references). Embed the proposal's L334-344 properties directly (claim_class, evidence_class, verdict_direction, calibrated score, M3a-cap activation if applicable).
- **Step 3.3 (Property Tests P1-P5):** Edit-append the H2 section with the 5 property tests verbatim from proposal L346-355.
- **Step 3.4 (Suite Integrity rules):** Edit-append the H2 section with file-change trigger rules from proposal L357-365.
- **Step 3.5 (Implementation Hook note):** Edit-append the final H2 section with the deferred-pytest-harness note from proposal L367-370.

### Phase 4: Sync + verify + lint

- **Step 4.1 (sync-dev):** Run `make sync-dev`; expect `✅ Sync complete.` and the new file mirrored to `.claude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md`.
- **Step 4.2 (verify-sync):** Run `make verify-sync`; expect exit 0 and `✅ sc-troubleshoot-protocol` line in output.
- **Step 4.3 (markdownlint):** Run `uv run pre-commit run markdownlint --files src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md`; expect Passed. If `--fix` modifies the file, re-run sync-dev + verify-sync.

### Phase 5: Final structural verification (FINAL_ONLY QA per Change B precedent)

- **Step 5.1 (post-completion validation):** Glob to confirm both `src/` and `.claude/` copies exist. Verify file has all 9 fixtures, all 5 property tests, suite-integrity section, and implementation-hook note (per VALIDATION_REQUIREMENTS in research-notes.md).
- **Step 5.2 (task summary):** Populate Task Summary in Task Log / Notes.
- **Step 5.3 (frontmatter complete):** Update status to `🟢 Done`, set completion_date, log to Execution Log.

### 8.1 Notes on parallelism with Tracks A/C/F

Per the proposal L488-495 dependency order (A → B → C → F → E), Change E is LAST. The task file CAN be BUILT in parallel with A/C/F (since the corpus markdown is deterministic from the proposal), but its **expected scores are only verifiable** once A (rubric formula), C (calibrator scoring), and F (audit gate) have shipped. Document this prerequisite in the task overview but do not block task build.

---

## Status: Complete

## Summary

1. **T4 directory `t4-pane-title-20260526-101500` confirmed NOT to exist** anywhere in `/config/workspace/IronClaude/` (find at depth 10 returns no matches). Closest analog found: `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/` (9 minutes earlier timestamp, same artifact pattern). Recommendation: **ship Fixtures 7-9 with proposal-described properties INLINE, no path references**, to maintain corpus portability.
2. **Template 01 confirmed appropriate** for Change E (single-file create with deterministic content; Change B used the same template).
3. **Makefile sync-dev (L109) and verify-sync (L166) documented verbatim** — sync-dev's `find ... -exec cp` recursion correctly handles the `refs/` subdirectory; verify-sync uses `diff -rq` for drift detection.
4. **Markdownlint hook (L70-82) confirmed to lint the new file** (no exclude pattern matches `src/superclaude/skills/.../refs/*.md`). `--fix` flag means file may be auto-modified, requiring re-sync.
5. **block-claude-generated-mirrors hook (L102-109)** confirms `.claude/` paths are blocked from commit — only the `src/` source is the commit surface.
6. **Change B precedent (TASK-RF-20260527-022700-change-b-hypothesis-card-schema) confirmed as a direct template** for the sync/lint/structural-check workflow; the only divergence is Write-then-Edit instead of pure Edit.
7. **Recommended 5-phase task structure** documented in Section 8 with explicit Phase 3 incremental Edit-append pattern for each ## section.

**Key gotchas surfaced:** (a) sync-dev order; (b) markdownlint --fix may modify file → re-sync required; (c) block-claude-generated-mirrors rejects .claude/ commits; (d) pre-commit may not be installed in fresh checkout; (e) NEW — H1 collision risk (low; verified in Phase 1); (f) NEW — broken-link risk if real-card paths used → mitigated by inline content recommendation; (g) NEW — first-pass lint cleanliness required (no incremental forgiveness for new files).

**Output file path:** `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.dev/tasks/to-do/TASK-RF-track-4-change-e-eval-cases-corpus-20260527-044000/research/03-t4-cards-and-template.md`
