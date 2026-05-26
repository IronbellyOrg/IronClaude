# Git Synthesis — Anti-Instinct integration_contracts Refactor (Fix B Merged)

**Generated:** 2026-05-25 (read-only inspection, no git mutations performed)
**Working dir:** `/config/workspace/IronClaude`
**Branch:** `fix/integration-contracts-mechanism-signature`

---

## A. Branch State

- **Name:** `fix/integration-contracts-mechanism-signature`
- **Base:** `master` (created off master earlier this session)
- **Tracking:** No upstream — local-only branch (not in `git branch -vv` upstream list)
- **Commits ahead of master:** **0** — `git log master..HEAD` returned empty
- **HEAD SHA:** `bb16c25a` (identical to `master` HEAD)
- **Implication:** All session work is **uncommitted in the working tree**. Nothing has been staged or committed on this branch yet.

---

## B. Tracked File Changes vs Master

`git diff master --shortstat`: **265 files changed, 4400 insertions(+), 1775 deletions(-)**

This count is **misleading** for the session's scope. The 265-file delta is the **pre-existing dirty working tree** that was already present when the branch was created off master. Only **3 files** are the substantive output of this session's anti-instinct refactor work:

| File | Role | +/− |
|---|---|---|
| `src/superclaude/cli/roadmap/integration_contracts.py` | Core implementation: `mechanism_signature` field, `_signature_subsumed`, 3-layer FR-MOD2.7 coverage with identifier-overlap guard | +148 / −41 |
| `tests/roadmap/test_integration_contracts.py` | New `TestHubDispatchRegression` class (t1-t7) + 2 synthetic TUIBBS-shaped fixtures (`TUIBBS_HUB_SPEC`, `TUIBBS_HUB_ROADMAP`) | +112 / 0 |
| `KNOWLEDGE.md` | New section: "Fix B Merged — Anti-Instinct Gate Mechanism-Signature Refactor (2026-05-25)" — load-bearing details, deviations, and limitation log | +53 / 0 |

The remaining **262 modified files** (entire `.claude/` mirror, `src/superclaude/cli/eval/*`, `src/superclaude/cli/prd/*`, all tests under `tests/audit/` + `tests/cli/eval/`, `scripts/`, `.dev/eval-workspaces/`, etc.) are **inherited dirty state** that was already modified vs master before this session started. They are unrelated to this session's refactor.

---

## C. Per-File Diff Highlights

### `src/superclaude/cli/roadmap/integration_contracts.py`

- **Lines 21-33** — `DISPATCH_PATTERNS[0]` expanded: added explicit `PROGRAMMATIC_RUNNERS` alternation (because `\bRUNNERS\b` doesn't match across `_`) and added compound dispatch-noun alternation (`class-priority|named-theme|role-keyed|theme|severity-keyed|module-tier|subprocess|gRPC`). Comment explicitly notes bare `priority` was removed.
- **Lines 128-134** — `IntegrationContract` gained `mechanism_signature: tuple[str, frozenset[str]] = field(default=(("", frozenset())))`.
- **Lines 174-217** — Extraction rewritten: per-evidence-line `seen_evidence: set[str]` replaced with `seen_signatures: dict[(str, frozenset[str]), int]`. Each match builds `signature = (mechanism, frozenset(_extract_identifiers(context)))`, then calls `_signature_subsumed`; loop now `break`s after one contract per line.
- **Lines 267-365** — `check_roadmap_coverage` FR-MOD2.7 block expanded from 1 to 3 layers: Layer 1 dispatch-family regex tolerance, Layer 2 same-line/window verb check (now includes `populate` verb), Layer 3 stem-fallback with **identifier-overlap guard** against `contract.mechanism_signature[1]` (defeats "Implement priority dispatch for logging" false-positive).
- **Lines 422-441** — New `_signature_subsumed` helper. Empty-identifier branch (`if not idents: return sig in seen`) preserves the existing `test_duplicate_lines_deduplicated` exact-match semantics — load-bearing detail.

### `tests/roadmap/test_integration_contracts.py`

- **Lines 129-173** — Two new synthetic fixtures (`TUIBBS_HUB_SPEC` ~26 lines, `TUIBBS_HUB_ROADMAP` ~11 lines) shaped like TUIBBS-scp `v1-MVP/{epics,roadmap}.md` hub block. `FR-S10-02` appears in every hub-dispatch context window so `_signature_subsumed` fires deterministically.
- **Lines 322-388** — New `TestHubDispatchRegression` class with 7 tests:
  - `t1_one_contract_per_hub_mechanism` — 4 epic lines → 1 contract
  - `t2_class_priority_dispatch_covers_hub` — roadmap covers via Layer 1
  - `t3_prose_dispatch_not_extracted_alone` — bare prose ≤1 contract
  - `t4_existing_dispatch_table_test_still_passes` — regression guard
  - `t5_cli_portify_regression_still_blocks` — SC-003 still uncovered
  - `t6_stem_fallback_with_ident_overlap_covers` — Layer 3 happy path
  - `t7_stem_fallback_without_ident_overlap_uncovers` — overlap-guard false-positive defense

### `KNOWLEDGE.md`

- **Lines 153-205** — New section logs: problem framing, key abstraction, load-bearing empty-identifier branch, two deviations from merged-output.md (PROGRAMMATIC_RUNNERS alternation + bare-priority removal) with rationale, documented limitation (single-PascalCase identifiers like `Interactive`/`Bulk` not captured by `_extract_identifiers`), end-to-end live-target result (`total=5 uncovered=0` against TUIBBS-scp v1-MVP).

---

## D. Untracked Artifacts

### Session-scoped (this session)

**Task folder** — `.dev/tasks/to-do/TASK-RF-20260525-150000/`
- `TASK-RF-20260525-150000.md` (100KB main task file)
- `research-notes.md`
- `research/` — `01-file-inventory.md`, `02-patterns-conventions.md`, `03-template-examples.md`, `04-gap-fill.md`
- `qa/` — `analyst-completeness-report.md`, `qa-phase-gate-independent.md`, `qa-phase-gate-independent-rerun.md`, `qa-qualitative-review.md`, `qa-research-gate-report.md`, `qa-task-validation-report.md`
- `phase-outputs/` — `discovery/`, `plans/`, `reports/`, `reviews/`, `test-results/`

**§7 Follow-up stub** — `.dev/tasks/to-do/TASK-RF-merge-prompt-wiring-directive-20260525-160000/`
- `TASK-RF-merge-prompt-wiring-directive-20260525-160000.md` (2.9KB, follow-up directive only)

**Troubleshoot folder** — `.dev/troubleshoot/build-anti-instinct-uncovered-contracts-20260525141717/`
- `REPORT.md`, `fix-b-opus.md`, `fix-b-sonnet.md`, `fix-a-retention-debate.md`, `fix-a-leave-vs-revert-debate.md`
- `adversarial/` — `base-selection.md`, `debate-transcript.md`, `diff-analysis.md`, `merged-output.md`, `merge-log.md`, `refactor-plan.md`, `variant-1-original.md`, `variant-2-original.md`
- (This `git-synthesis.md` will live alongside the above)

### Not session-scoped (pre-existing untracked clutter)

- `.dev/eval-workspaces/prd-bug-test/`
- `.dev/reviews/pr-71-20260521130522/`, `.dev/reviews/pr-79-20260524144323/`
- `.dev/tasks/to-do/TASK-RESEARCH-20260501-201321/`, `TASK-RF-20260521133223/`, `TASK-RF-20260525-025459/`, `TASK-STDIN-RECON-REMEDIATION-20260501/`

---

## E. `.claude/` Cleanliness Verdict

**Verdict: FAIL (but not a session-introduced violation)**

`git status -- .claude/` shows **133 modified files** under `.claude/` (agents, commands, skills, templates). This violates the absolute rule "`.claude/{skills,commands,agents,hooks,templates}/*` is gitignored sync-dev output."

**Evidence this pre-dates the session:**
- The branch was created off master at `bb16c25a` with this dirty state already present.
- A later master commit visible in `git log --all --since="2026-05-25"` is `942bbc49 chore(repo): untrack 137 drifted .claude/ mirrors to honor SoT discipline` — confirming the repo-wide cleanup is the open remediation path on master, not work for this session.
- Zero `.claude/` modifications in this session's diffs are session-introduced. The session touched only `src/superclaude/cli/roadmap/integration_contracts.py`, `tests/roadmap/test_integration_contracts.py`, and `KNOWLEDGE.md`.

**Action required:** Do **NOT** stage any `.claude/` paths. The CLAUDE.md absolute rule and the upstream `942bbc49` cleanup commit cover this; the pre-existing dirty state will reconcile when this branch rebases onto the post-untrack master.

---

## F. TUIBBS-scp Side (Fix A)

- **Repo:** `/config/workspace/TUIBBS-scp`
- **Branch:** `feat/prd-tuibbs-v1` (up to date with `origin/feat/prd-tuibbs-v1`)
- **Tracked-file modifications:** **None** — `git diff --stat` is empty.
- **roadmap.md status:** **Untracked** (`git ls-files --error-unmatch` errors: "did not match any file(s) known to git"). The file exists on disk (`108522 bytes`, mtime May 25 14:33) but has never been `git add`ed. The entire `.dev/releases/current/v1-MVP/` directory tree is untracked.
- **Implication for Fix A:** Whatever Fix A edited in `roadmap.md` is purely on-disk and not visible to git as a diff. The merged Fix B end-to-end success message in KNOWLEDGE.md says `total=5 uncovered=0` was achieved **before** the Fix A workaround would be reverted — confirming Fix B is sufficient and Fix A can be safely retired. Per the `fix-a-leave-vs-revert-debate.md` adversarial doc, the retention decision is pending; either outcome leaves the TUIBBS-scp repo in the same "no tracked modifications" state.

---

## G. Suggested Next Steps

### Ready to commit on `fix/integration-contracts-mechanism-signature`

Stage **only these 3 files**:
```
src/superclaude/cli/roadmap/integration_contracts.py
tests/roadmap/test_integration_contracts.py
KNOWLEDGE.md
```

### Do NOT stage under any circumstance
- Any `.claude/` path (133 modified — CLAUDE.md absolute-rule violation; covered by upstream `942bbc49`)
- `.dev/eval-workspaces/`, `.dev/research/`, `scripts/`, `src/superclaude/cli/eval/`, `src/superclaude/cli/prd/`, `tests/audit/`, `tests/cli/eval/`, `tests/cli/prd/`, `tests/hooks/`, `tests/pipeline/`, `tests/sprint/` (inherited dirty state, not session work)
- Anything under `.dev/tasks/to-do/` from older dates (`20260501-*`, `20260521-*`, `20260525-025459`)

### Review-worthy before committing
- Confirm the three deviations called out in `KNOWLEDGE.md` (PROGRAMMATIC_RUNNERS alternation, bare-priority removal, documented PascalCase-stem limitation) are acceptable — they are spec-vs-implementation departures from `merged-output.md`.
- Decide whether the `TASK-RF-20260525-150000/` task folder and `TASK-RF-merge-prompt-wiring-directive-20260525-160000/` stub should be committed alongside or land in a separate `chore(tasks): …` commit.

### Suggested commit split

**Option 1 (recommended — one focused fix commit + one task-artifacts commit):**

```
git checkout -b fix/integration-contracts-mechanism-signature  # already on this branch
git add src/superclaude/cli/roadmap/integration_contracts.py \
        tests/roadmap/test_integration_contracts.py \
        KNOWLEDGE.md
git commit -m "fix(roadmap): anti-instinct mechanism_signature refactor — collapse over-capture, widen coverage with overlap guard"

# Optional second commit for task artifacts:
git add .dev/tasks/to-do/TASK-RF-20260525-150000/ \
        .dev/tasks/to-do/TASK-RF-merge-prompt-wiring-directive-20260525-160000/ \
        .dev/troubleshoot/build-anti-instinct-uncovered-contracts-20260525141717/
git commit -m "chore(tasks): land Fix B task workspace + §7 follow-up stub + troubleshoot artifacts"
```

**Option 2 (single bundled commit):** Stage all session-scoped files (the 3 source files + 3 untracked task/troubleshoot dirs) under one `fix(roadmap): …` commit. Less clean, but acceptable if the task artifacts are considered load-bearing audit trail for the fix.

### TUIBBS-scp follow-up
- `fix-a-leave-vs-revert-debate.md` is unresolved on disk. Since roadmap.md is untracked anyway, no git action is required on the TUIBBS-scp side regardless of which way the debate resolves.
