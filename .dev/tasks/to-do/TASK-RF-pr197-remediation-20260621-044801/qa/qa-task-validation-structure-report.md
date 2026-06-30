# QA Report — Task Integrity Check (PR-197 Remediation)

**Topic:** PR-197 remediation tasklist structural validation
**Date:** 2026-06-20
**Phase:** task-integrity
**Lens:** b2-self-containment + phase-structure + spec-alignment
**Fix authorization:** false (report-only)

---

## Overall Verdict: PASS (with 1 IMPORTANT + 2 MINOR advisory findings; none merge-blocking)

The task file is structurally sound, B2-self-contained, correctly phased, faithfully
spec-aligned, and HD-1-compliant. All 8 MUST-HOLD invariants from the spawn prompt hold.
The one IMPORTANT finding (R1 acceptance-grep false positives) is a defect inherited
verbatim from the authoritative spec, not introduced by the task; it is flagged here as an
execution-time risk with a concrete mitigation, but it does not invalidate the task structure.

---

## Verification Methodology

I verified the task against the PR branch it actually targets (`origin/feat/rf-harness-sync`,
head `a3f3f0cb` per spec) using `git show origin/feat/rf-harness-sync:<path>`, NOT the working
tree (`master`/`feat/recommend-minstar`), because the spec and every line citation are written
against the PR-branch blobs. Reading the working tree would have produced false "already fixed"
verdicts (the working tree already carries the hyphen form). This branch-discipline is the same
care the REVIEW.md author exercised (see its review-environment note).

---

## MUST-HOLD Invariant Results

### Invariant 1 — R1 granularity + correctness: PASS (with IMPORTANT advisory, see Issue #1)
- Exactly one revert item per rf-* agent: Steps 2.1 (rf-analyst), 2.2 (rf-assembler),
  2.3 (rf-qa), 2.4 (rf-qa-qualitative), 2.5 (rf-task-builder), 2.6 (rf-task-executor),
  2.7 (rf-task-researcher), 2.8 (rf-team-lead) = 8 items, one per file. VERIFIED via phase-item map.
- Direction is CORRECT: every item replaces `tavily_search`->`tavily-search` and
  `_extract`->`-extract` (underscore->HYPHEN). VERIFIED: PR branch rf-analyst.md:13-14 carries the
  underscore form (`mcp__tavily__tavily_search`/`_extract`); the canonical hyphen form is at
  `deep-research.md:6-7` (`mcp__tavily__tavily-search`/`-extract`, Read directly). The revert
  direction matches REVIEW.md H1 + spec R1. Not inverted.
- Cross-file acceptance check present: Step 2.9 runs
  `git -C ... grep -nE 'tavily_(search|extract)' src/superclaude/agents/` and requires ZERO matches,
  plus a hyphen-presence check and a `deep-research.md` zero-diff check. VERIFIED at line 228.
- `deep-research.md` correctly marked do-not-touch (Steps 1.4, 2.x, 2.9 diff-stat guard). VERIFIED.

### Invariant 2 — HD-1 halt (CRITICAL): PASS
- Step 4.3 is a `needs_human_decision`-style HALT item. Its first sentence: "This is a
  `needs_human_decision` gate — it MUST NOT auto-select a resolution, MUST NOT flip the `--cli`
  default, and MUST NOT edit O4 depth floors." VERIFIED at line 254.
- It writes a PENDING record (`STATUS: PENDING — awaiting RyanW`) to
  `phase-outputs/plans/HD-1-default-mode-decision.md`, records the three options verbatim, asserts
  no default flipped / no O4 floor edited, and ends "do NOT proceed to edit any default." It does
  NOT silently apply a default. VERIFIED.
- R2a (Steps 4.1 + 4.2) is applied UNCONDITIONALLY and is SEPARATE from R2b: phase intro line 245
  states "R2a is applied UNCONDITIONALLY" while R2b is the HALT gate. 4.1 adds the in-SKILL
  disclosure at both the Rule-20 default arm and the `#6 --cli` input definition; 4.2 softens the
  "confirmed" wording. VERIFIED at lines 245, 247-251.
- The Post-Completion Done item (line 286) explicitly notes HD-1 PENDING is NOT a blocker to Done
  (correct: the halt is the terminal state for that item, the rest of the work proceeds).

### Invariant 3 — Source-of-truth discipline: PASS
- Every editing item targets `src/superclaude/...` paths (resolved against the worktree root) and
  is followed by `make sync-dev` + `make verify-sync`: VERIFIED in Steps 2.1-2.8, 3.1, 3.2, 4.1,
  4.2, 5.1, 5.2.
- No item stages or commits any `.claude/` path. All `.claude/` mentions (lines 158, 178, 274, 286)
  are NEVER-stage rules or the settings.json carve-out. Step 6.x and Post-Completion explicitly
  verify no `.claude/` path is staged. VERIFIED.
- Worktree isolation set up in Phase 1: Step 1.2 runs
  `git worktree add .dev/worktrees/pr197-remediation feat/rf-harness-sync`. VERIFIED at line 188.

### Invariant 4 — R3 completeness: PASS
- (a) Test item: Step 3.2 adds a `tests/cli/reflect/` test asserting the `_build_prompt()`
  directive is present, appears EXACTLY ONCE, and contains "INLINE", "Do NOT delegate", and
  "Wave 3"/"Wave 4". VERIFIED at line 238. The directive + those exact phrases exist on the PR
  branch at `runner.py:367-380` (`inline_directive`, "...INLINE...", "Do NOT delegate...",
  "Wave 3 ... Wave 4 (adversarial merge)"). VERIFIED via `git show`.
- (b) Comment item: Step 3.1 adds a one-line comment at the directive site noting EV-1 is the
  structural enforcement. VERIFIED at line 235.
- Python validation uses `uv run pytest` (Steps 3.3, 6.3) and `uv run ruff format --check src/ tests/`
  (Step 6.2). VERIFIED. (Matches the project rule that CI runs `ruff format --check` separately
  from `make lint`.)

### Invariant 5 — R4 + R5 present: PASS
- R4 (Step 5.1): Mode Bifurcation Table (columns Field/Rule · CLI · Skill-only · Justification)
  + key-presence rule (`reflect_post_mode: cli` => start_commit/executor_model_class MUST be
  present; `skill` => MUST be absent), referenced from §3.3. VERIFIED at line 261.
- R5 (Step 5.2): §4.2 dangling-ref fix + `spec_path` mode-qualifier. VERIFIED at line 264. The
  dangling "§4.2 clause 4" citation exists on the PR branch at `SKILL.md:2276`; clauses live in
  the unnumbered note at ~2244-2250 (VERIFIED via `git show`), matching REVIEW.md L1.

### Invariant 6 — R6 exclusion: PASS
- No work item touches `reflection-rubric.md` line citations. Every R6 reference (lines 80-81, 162,
  318, 365) is an explicit OUT-OF-SCOPE statement or a follow-up note. VERIFIED via grep.

### Invariant 7 — No POST reflect wrapper item: PASS
- No `superclaude reflect run` POST gate item exists. The two grep hits are: line 261 (R4 content
  referencing `reflect_post_mode: cli` as documentation, not a gate item) and line 268, which
  explicitly states "do NOT run any `superclaude reflect run` wrapper here." VERIFIED.
- Phase 6 is a FINAL_ONLY command-based validation gate (sync -> verify-sync -> ruff -> pytest),
  not a reflect wrapper. Consistent with POST_REFLECT_GATE DISABLED.

### Invariant 8 — B2 self-containment + anti-orphaning: PASS
- Every checklist item is a single self-contained paragraph carrying context + action + output +
  verification + completion gate ("Once done, mark this item as complete"). Spot-VERIFIED across
  Steps 1.2, 2.1, 3.2, 4.3, 5.1, 6.4.
- The "update status to Done" item (line 290) is the VERY LAST `- [ ]` item in the file.
  Anti-orphaning holds. VERIFIED via `grep -nE '^- \[ \]' | tail`.

---

## Structural Cross-Checks (task-integrity checklist subset)

| Check | Result | Evidence |
|---|---|---|
| Checklist format `- [ ]` | PASS | All items use `- [ ]`; none malformed |
| Phase ordering / no gaps | PASS | Phases 1-6 sequential; P4 before P5 (both edit SKILL.md, correctly serialized — line 245/258) |
| Intra-phase dependency ordering | PASS | Step 1.4 writes canonical-form file; Steps 2.x read it. Step 3.1 (comment) before 3.2 (test) before 3.3 (run). Discovery before consumption holds |
| Output paths specified | PASS | Every file-producing item names a `phase-outputs/...` path |
| Verification durability (R3 test) | PASS | Step 3.2 adds a real pytest file under `tests/cli/reflect/`, not an inline `python -c`. CI-compatible |
| Completion-criteria honesty | PASS | Done item (286/290) gates on Phase 6 green; HD-1 PENDING explicitly carved out as non-blocking-by-design, not a hidden false-done |
| Item atomicity | PASS | Items are single-file, single-concern. The 8 R1 items are deliberately split per file (one agent each) — correct granularity |
| Phase header count claims | N/A | Headers carry no explicit "(N items)" claim, so no count to contradict |
| Frontmatter schema | PASS | id/title/status/created_date/type/template-equivalent fields present and non-empty (template 02) |
| spec_path frontmatter | PASS | `spec_path: ".dev/reviews/pr-197-20260620223934/remediation-spec.md"` set (line 18) |

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | Steps 1.3, 2.1-2.9 (R1 acceptance grep) | The acceptance command `git grep -nE 'tavily_(search\|extract)' src/superclaude/agents/` matches BOTH tool-ids AND unrelated PROSE report-label strings. On the PR branch these prose labels exist at `rf-qa.md:119` (`tavily_search: 1 attempt, fell back...`), `rf-qa.md:506` (`tavily_search: N \| tavily_extract: N`), `rf-qa-qualitative.md:127`, and the §12 reference at `rf-qa.md:538` (`mcp__tavily__tavily_search` inside a "Tavily-first" sentence). After the tool-id revert to hyphens, the regex `tavily_(search\|extract)` will STILL match the underscore in the prose label `tavily_search:` (a report field name, not a tool id). So the R1 acceptance criterion "returns ZERO matches" is UNSATISFIABLE without either (a) also rewriting those prose labels — which would be scope creep / a wrong mutation — or (b) tightening the grep. This is inherited verbatim from the spec (R1 acceptance #1) and REVIEW.md H1's recommendation, so it is a spec defect, not a task-builder defect — but the executor will hit it. | Tighten the acceptance grep to match the TOOL-ID form only, e.g. `git grep -nE 'mcp__tavily__tavily_(search\|extract)' src/superclaude/agents/` (require the `mcp__tavily__` prefix). This excludes the bare `tavily_search:` report labels. Apply in Steps 1.3, 2.1-2.8 (per-file) and 2.9 (cross-file). NOTE: the report-label strings like `tavily_search: N` are CORRECT as-is and MUST NOT be changed — they are field names in the QA report format, never tool ids. The task already says "pure hyphen-restoration with NO other line changed", which protects against the wrong mutation, but the verification grep as written will report a false FAIL. fix_authorization is false, so this is reported, not applied. |
| 2 | MINOR | Step 4.2 (line 250-251) | Step 4.2 asserts "three 'capability are confirmed' assertion sites (approximately lines 1668, 2218, and 2370)" and "ensuring all three sites are updated". On the PR branch the exact phrase "capability are confirmed" appears only TWICE (`SKILL.md:2218` and `:2370`, VERIFIED via `git show ... \| grep -ci`). Line 1668 carries a RELATED but differently-worded claim ("a subagent CAN invoke the Skill tool and that skill spawns its own ensemble, as the POST gate relies on") — not the literal "confirmed" phrase. The "all three sites" wording could cause the executor to hunt for a non-existent third literal match or to over-edit. Inherited from spec R2/REVIEW.md H2 (both cite 1668/2218/2370). | Reword to "the 'confirmed'/over-asserted capability sites (2 exact 'capability are confirmed' matches at ~2218/2370 plus the related provisional claim near ~1668)". The item already mitigates with "use Grep to confirm exact current locations since line numbers may have shifted", so impact is low — the executor will grep and find what exists. No structural failure. |
| 3 | MINOR | Step 4.2 acceptance phrasing | Spec R2a acceptance #1 is "no remaining bare 'capability are confirmed' assertion without softening or a cited validating run." Because only 2 literal sites exist, softening both satisfies the spec; the "three sites" expectation in the item is stricter than the spec and could read as an unmet sub-goal if the executor finds only 2. | Align the count to the spec's outcome-based criterion (no bare 'confirmed' assertion remains) rather than a hardcoded site count. Cosmetic; subsumed by Issue #2's fix. |

---

## Confidence Gate

- **Confidence:** Verified: 8/8 MUST-HOLD invariants + 10/10 structural cross-checks |
  Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 4 | git grep / Bash: 9 | Glob: 0 | Bash (non-grep): included above
  (No web research performed — all verification was source-truth-local against the PR-branch blobs.)
- Every UNCHECKED item: none.
- Every UNVERIFIABLE item: none.

Tool-engagement note: each invariant was verified by a targeted command whose output covered
multiple checklist rows (e.g. the single phase-item-map awk covered Invariants 1, 8 and several
structural cross-checks; one `git show` per file covered the PR-branch citation checks). No padding
calls were made; no invariant was marked VERIFIED on reliance rather than direct tool output.

---

## Recommendations Before Execution

1. **(IMPORTANT)** Fix the R1 acceptance grep to require the `mcp__tavily__` prefix before
   executing Phase 2, otherwise Step 2.9 will report a false FAIL and the executor may be tempted
   to wrongly mutate the `tavily_search:`/`tavily_extract:` REPORT-LABEL strings (which are correct
   field names). Recommend editing the spec's acceptance command and the inherited grep in Steps
   1.3 / 2.1-2.9 to `mcp__tavily__tavily_(search|extract)`.
2. **(MINOR)** Soften Step 4.2's "three sites" / "all three sites" to an outcome-based criterion
   matching spec R2a acceptance #1; the Grep-confirm mitigation already present makes this low-risk.
3. No changes required for HD-1, source-of-truth discipline, R4/R5/R6 scope, the POST-wrapper
   exclusion, or anti-orphaning — all verified clean.

## QA Complete
