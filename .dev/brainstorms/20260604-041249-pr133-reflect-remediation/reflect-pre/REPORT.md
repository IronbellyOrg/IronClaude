# /sc:reflect --mode pre — UC-1 Coverage/Gap Audit

**Subject:** PR #133 review-critique remediation plan
**Spec:** `../remediation-spec.md`  **Tasklist:** `../remediation-tasklist.md`
**Mode:** pre (UC-1)  **Tier reached:** 1  **Status:** success (with 2 must-fix refinements + 1 human decision)
**Coverage:** 6/6 requirements mapped (coverage_pct = 1.00)  **Calibrated confidence:** 0.90

---

## 1. Coverage matrix (spec requirement → tasklist task)

| Req | Acceptance criteria | Covered by | Verdict |
|-----|---------------------|------------|---------|
| R1  | AC-R1.1 flags.md `--tasklist` row | T-001 | ✅ |
|     | AC-R1.2 reflect.md:73 | T-002 | ✅ |
|     | AC-R1.3 SKILL.md:68 | T-003 | ✅ |
|     | AC-R1.4 no example mutated for wording | T-001/2/3 (wording-only; no example edits) | ✅ |
| R2  | AC-R2.1/R2.2 legacy post note + Wave 6 source | T-004 | ✅ |
| R3  | AC-R3.1 `--task-log` row | T-005 | ✅ |
| R4  | AC-R4.1 three PR-headlined flags | T-006 | ✅ |
|     | AC-R4.2 curation pointer | T-006 | ✅ (see G4 wording) |
| R5  | AC-R5.1 plugins/ copy → v2 | T-007 | ✅ |
|     | AC-R5.2 orphan flagged, not patched | T-008 | ✅ (human decision) |
| R6  | AC-R6.1 sync-dev + verify-sync | T-009 | ✅ |
|     | AC-R6.2 never stage `.claude/` | T-011 (constraint) | ✅ |
|     | AC-R6.3 markdownlint | T-010 | ✅ |
|     | AC-R6.4 PR to fork | T-011 | ✅ |

**No unmapped requirements.** Coverage floor (0.90) cleared.

---

## 2. Gap registry (best-practice + risk findings)

### MUST-FIX before execution

**G-ANCHOR (critical) — wording downgrade must be surgical (tasklist row only).**
`"required for UC-2"` appears on **two adjacent rows** in both source files:
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md:68` (`--tasklist` — the target) **and `:69`** (`--diff` — genuinely required, MUST NOT change).
- `src/superclaude/commands/reflect.md:73` (`--tasklist`) **and `:74`** (`--diff … Required for UC-2 unless --task-log`).
A blanket find/replace of `"required for UC-2"` would falsely weaken the real `--diff` requirement and corrupt the hard-STOP contract.
→ **Refine T-002/T-003:** target the `--tasklist` row literally; leave every `--diff` row untouched. Verify post-edit that `--diff … required for UC-2` survives.

**G3 (high) — branch base is not in the working tree.**
The current working tree is on `fix/roadmap-resume-spec-guard`, **6 commits behind `origin/master`**; PR #133 (`b9724e49`) content is absent here. Every line number in the tasklist is `origin/master`-relative.
→ **Add gating T-000:** `git fetch origin && git checkout -b docs/pr133-reflect-critique-remediation origin/master`, then re-confirm each anchor (`grep -n`) before editing. Executing against the current tree would mis-target every edit.

### ADVISORY

- **G1 (scope) — single-purpose PR spans 4 distributable surfaces.** Edits touch `docs/`, `src/superclaude/commands/`, `src/superclaude/skills/`, and `plugins/`. PR #133's own guideline is "~200 lines, single purpose." This is cohesive under the theme *"reflect surface fidelity,"* but if a reviewer enforces single-purpose strictly, split docs-only (R1 flags/commands + R2-R4) from the skill/plugin sync (R1 SKILL.md + R5). Recommend keeping as one themed PR with a clear title.
- **G4 (wording) — curation pointer target.** AC-R4.2 points users at `src/superclaude/commands/reflect.md` (a source path). For a user-facing doc, prefer pointing at the rendered reflect section of `commands.md` or "run `/sc:reflect --help`." Minor.
- **G5 (fidelity) — T-007 is the highest-risk edit (already MEDIUM-flagged).** Manually porting the 100-line v1 plugins copy to the v2 surface invites drift. Recommend a `/sc:reflect --mode post --diff` (or a diff review) on the resulting change before PR.
- **G6 (sync) — `make sync-dev` covers skills + agents only, not `commands/` or `plugins/`.** T-002 (command file) and T-007 (plugins copy) won't be propagated by sync-dev; that's expected (they're install-time / hand-maintained, not verify-sync-gated). No defect — just don't expect `verify-sync` to validate them.

### HUMAN DECISION (needs_human_decision = true)

**T-008 — orphan `commands/sc-reflect.md` disposition.** Not install-resolved, carries `/sc:sc:sc:reflect` corruption. Recommended action: `git rm` as separate cleanup rather than hand-patch a dead snapshot. **Halts pending your approval** (delete vs keep-and-fix vs leave).

---

## 3. Verdict

The remediation plan is **complete (1.00 coverage) and evidence-grounded**. It is **execution-ready after two surgical refinements** (G-ANCHOR + G3 gating T-000) and **one human decision** (T-008). No requirement is unaddressed; no critique is left without a mapped fix; the C1 wording direction is verified against the skill's actual STOP enforcement.

**Recommended pre-execution edits to the tasklist:**
1. Insert **T-000** (branch off `origin/master` + re-anchor) as the first, gating task.
2. Annotate **T-002/T-003** with "tasklist row only — do NOT touch the adjacent `--diff` row."
3. Resolve **T-008** (orphan delete vs keep) before the PR is opened.
