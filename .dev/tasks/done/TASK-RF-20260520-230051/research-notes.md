---
name: research-notes
status: Complete
date: 2026-05-20
---

# Research Notes: PR #64 Top-3 Medium Remediation

**Scenario:** A (explicit — all 3 fixes pre-specified with exact content from PR #64 REVIEW.md)
**Depth Tier:** Quick (genuinely small scope; <5 files, no discovery needed)
**Track Count:** 1
**Template:** 02 (per user instruction — three coordinated edits across two file types qualifies as multi-step with validation phase)
**Parent spec:** `/config/workspace/IronClaude/.dev/reviews/pr-64-20260520211916/REVIEW.md`

---

## EXISTING_FILES

Three source-of-truth files in scope (each verified to exist at the line ranges
the BUILD_REQUEST cites):

1. **`src/superclaude/hooks/scripts/offer-pr-review.sh`** (70 lines, bash)
   - Hook contract: PostToolUse(Bash); reads JSON from stdin; emits XML offer
     block on stdout when `gh pr create` succeeds.
   - Current hot path: `INPUT="$(cat ...)"` at L17 → `jq -r '.tool_name'` at
     L20 → tool-name gate at L21 → `jq -r '.tool_input.command'` at L23 →
     regex match at L29.
   - Fix 1 insertion point: between L17 and L20 (after INPUT capture, before
     first jq invocation).

2. **`src/superclaude/skills/sc-auggie-review-protocol/SKILL.md`** (362 lines,
   markdown)
   - Target block: lines 163-170 (within the "Common pitfalls" callout block).
   - Line 166 is the offending bullet (JSON wrapping bullet that omits the
     `tail -n +2` and `jq -r '.result'` steps).
   - Line 167 is the `--max-turns preamble` bullet that DOES document the
     full pipeline — but as a forward reference from L166.
   - Fix 2 rewrites L163-170 so the JSON-wrapping bullet is complete and inline.

3. **`src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json`**
   (29 lines, JSON)
   - Three eval scenarios (id 1/2/3): pr-by-number-merged, local-diff-vs-master,
     snapshot-cli-module.
   - All three have `"assertions": []` at lines 10, 18, 26.
   - Each scenario produces a REVIEW.md at the eval's `--output-dir`.

**Sync mechanics (verified from CLAUDE.md):**

- Source of truth is `src/superclaude/`. `make sync-dev` copies to `.claude/`.
- `.claude/` is gitignored except `settings.json` (see memory:
  feedback_claude_dir_gitignored). Never stage `.claude/*.md`.
- Pre-commit hook runs `make verify-sync` to fail if src/ and .claude/ drift.

---

## PATTERNS_AND_CONVENTIONS

**Bash style (offer-pr-review.sh):**

- `set -u` only (no `-e`, no `-o pipefail`) — hook is intentionally fail-open
  per its own contract (L7: "we do NOT want exit 2 here").
- Inline `case "$VAR" in PATTERN) ;; *) exit 0;; esac` is the idiomatic
  pure-shell guard pattern in this codebase (matches the existing exit-0
  short-circuits at L21, L24, L30, L35).
- Comments use `# ...` single-line style; section dividers use `# Section`.

**Markdown style (SKILL.md "Common pitfalls" block, lines 161-176):**

- Blockquote callout with `>` prefix on every line including blanks.
- Bulleted items use `> - **Term**: explanation. Recipe: \`code block\` or
  equivalent.`
- Code spans use single backticks; multi-line shell snippets are inline
  (no fenced code blocks inside the callout).

**JSON style (evals.json):**

- 2-space indent.
- Each eval object has: `id` (int), `name` (kebab), `prompt` (multi-line
  string), `expected_output` (paragraph), `files` (array — currently empty),
  `assertions` (array — currently empty, target of Fix 3).
- No existing assertion DSL anywhere in the repo (verified: only one
  evals.json exists). Fix 3 will DEFINE the assertion JSON shape and
  document it so the harness implementer can wire it up later.

---

## GAPS_AND_QUESTIONS

**Resolved during scope discovery:**

- ✓ Existing assertion DSL? — NONE. Single `evals.json` in the repo, all
  three `assertions: []`. Fix 3 defines the shape; recommend
  `{"type": "...", ...}` discriminated-union form (skill-evals harness
  convention from prior Anthropic skill-creator template).
- ✓ Sync model? — `make sync-dev` (src → .claude), `make verify-sync` (CI
  gate). `.claude/` gitignored except settings.json.
- ✓ Current line numbers verified — offer-pr-review.sh L17/L20 and SKILL.md
  L163-170 match BUILD_REQUEST.
- ✓ Hook contract for fail-open prefilter — `exit 0` is correct (matches
  existing pattern at L21, L24, L30, L35).

**Genuinely open (low risk):**

- The substring `*'"command"'*'gh'*'pr'*'create'*` pattern has a known
  false-positive: a Bash command like `echo '"command" gh foo pr create'`
  would match. Accepted because (a) downstream regex at L29 is precise,
  (b) the prefilter's job is to skip the ~99% of Bash calls that aren't
  `gh pr` at all, not to be a tight gate. Documented as an Open Question
  in the generated task.

---

## RECOMMENDED_OUTPUTS

The generated MDTM task file should structure work into 5 phases:

| Phase | Purpose | Items |
|-------|---------|-------|
| 1 | Pre-flight checks (verify branch, clean baseline, read targets) | 3-4 |
| 2 | Fix 1 — offer-pr-review.sh prefilter | 2-3 |
| 3 | Fix 2 — SKILL.md L163-170 rewrite | 2-3 |
| 4 | Fix 3 — evals.json assertions populated | 3-4 |
| 5 | Sync, validate, completion (sync-dev, verify-sync, lint, completion gate) | 3-4 |

Each fix phase should have: read-current-content item → apply-edit item →
verify-edit item. Phase 5 wraps with task-completion items per anti-orphaning
rule.

NO commit/push items in the generated task — those are post-execution
steps the user runs after `/sc:reflect --type task --validate` signs off.

---

## SUGGESTED_PHASES

Three researchers, one per concern, parallel spawn:

1. **researcher-01 — File Inventory + Patterns**
   - Scope: All 3 target files in detail
   - Output: `research/01-target-files-inventory.md`
   - What other researchers cover: template/eval-harness conventions (R02),
     verification/sync mechanics (R03)

2. **researcher-02 — Template & Examples + Eval-Harness Convention**
   - Scope: `.claude/templates/workflow/02_mdtm_template_complex_task.md` PART 1,
     existing `.dev/tasks/done/` examples for similar small-fix tasks, skill-creator
     eval-harness assertion DSL convention research (web)
   - Output: `research/02-template-and-eval-dsl.md`
   - Note: This researcher MAY do limited web search (skill-creator eval
     conventions) — Quick tier normally has 0 web agents, but this one
     researcher needs it to design Fix 3's assertion DSL.

3. **researcher-03 — Test & Verification (Sync + Lint + Gates)**
   - Scope: `make sync-dev`, `make verify-sync`, pre-commit config, how to
     verify each fix landed correctly (jq lint for evals.json, bash -n for
     hook script, markdown render check for SKILL.md)
   - Output: `research/03-verification-and-sync.md`

---

## TEMPLATE_NOTES

**Template 02 selection:** Multi-file (3 files), multi-phase (Fix → Verify per
fix), and includes a validation phase (sync + verify-sync + lint). Even though
each individual fix is small, the coordination structure across files and the
mandatory validation gate per CLAUDE.md ("sc:reflect --type task --validate
should be run before changes are committed") warrants template 02.

**Tier selection — Quick (3 researchers, 0-1 web):** Genuine narrow request,
all 3 fixes pre-specified, no codebase discovery needed, no architecture
decisions. Quick is correct; promoting to Standard would add ceremony
without uncovering more facts.

**MDTM features to use:**

- Per-item `Context / Action / Output / Verification / Completion gate` (5-field schema)
- Phase-level dependencies (Phase 2/3/4 are independent; Phase 5 depends on all three)
- Open Questions section for the prefilter false-positive note
- No agent-spawning items needed (executor handles everything directly with Edit/Bash/Read)
- `## Execution Context` block: AUTO per BUILD_REQUEST default. Inferred source
  areas ≥3 ("offer-pr-review hook", "sc-auggie-review-protocol SKILL.md",
  "sc-auggie-review-protocol evals harness") → block SHOULD emit (full form).

**BUILD_REQUEST fields to pass to rf-task-builder:**

- `QA_GATE_REQUIREMENTS: FINAL_ONLY` — single validation phase at end is correct
  for this scope; per-phase QA would be ceremony.
- `VALIDATION_REQUIREMENTS: "make sync-dev succeeds; make verify-sync passes;
  jq . on evals.json parses; bash -n on offer-pr-review.sh parses;
  shell-check on offer-pr-review.sh produces no NEW warnings vs baseline"`
- `TESTING_REQUIREMENTS: NONE` — this fix is itself test-coverage
  infrastructure (Fix 3 adds the test assertions). No existing harness to run.
- `EXECUTION_CONTEXT_REQUIREMENTS: AUTO`

---

## AMBIGUITIES_FOR_USER

None — intent is fully unambiguous:

- All 3 fixes have verbatim content specified in BUILD_REQUEST
- Insertion points have line numbers
- Source-of-truth path discipline is established
- Post-build chain is explicit (analyze → execute → validate → sync-dev →
  commit → push)
- Out-of-scope is explicit (no scope creep, no refactor of unrelated code)

The one minor design choice — assertion DSL shape for Fix 3 — is delegated to
the builder with guidance to use the natural `{"type": "...", ...}` JSON form
and document it inline so the future harness implementer can wire it up. This
is a sensible deferral, not an ambiguity requiring user input.
