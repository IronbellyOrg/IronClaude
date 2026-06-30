---
contract_version: "1.2.0"
status: partial
mode: pre
tier_reached: 1
confidence_calibrated: 0.92
coverage_pct: 1.0
best_practice_grade: 3
needs_human_decision: true
---

# Reflect (UC-1, pre-execution) — TASK-RF-20260604045025

**Spec (driving doc):** `.dev/troubleshoot/test-audit-canonical-brainstorm-ci-20260604043148/REPORT.md` (resolved from the task's `related_docs`; no `--spec` was passed).
**Verdict:** Coverage is complete (4/4 objectives mapped). **Two best-practice defects found** — one HIGH that would halt the fix mid-execution, one MEDIUM that could block branch creation. Both reproduced empirically. Recommend fixing the task file before `/task`.

## Coverage matrix (spec → tasklist) — 100%

| Spec requirement (REPORT Proposed Fix) | Task item | Status |
|---|---|---|
| Fix A: `.gitignore` negation after `*.log` | Step 2.1 | ✅ mapped |
| Fix A: commit 6 fixtures, no `-f`, no `.claude/` | Step 2.2 | ✅ mapped |
| Fix A: 27 parity tests green | Step 3.1 | ✅ mapped |
| Fix B: hermetic rewrite + companion present-case test | Step 2.3 | ✅ mapped |
| Fix B: brainstorm `-k skill` green | Step 3.2 | ✅ mapped |
| Constraint: ruff check + format --check separately | Step 3.3 | ✅ mapped |
| Constraint: no `.claude/` staged / no `-f` | Steps 2.2, 3.4, PG.2, PC | ✅ mapped (defense-in-depth) |
| Risk: branch off master | Step 1.3 | ⚠️ mapped but defective (Finding 2) |

No unmapped requirements. No scope drift (task stays within the 8 WHERE files).

## Findings

### 🔴 HIGH — F1: Step 2.1's `git check-ignore -v` assertion is inverted → executor will halt staging on a correct negation

Step 2.1 instructs (line 137): run `git check-ignore -v <6 paths>` and *"confirm the command prints NOTHING and exits non-zero for all 6 (un-ignored)"*, and the item's halt clause says *"if any `git check-ignore` result contradicts the expected un-ignore/stay-ignored split, DO NOT proceed to staging."*

**That assertion is backwards for the `-v` form.** Reproduced live (negation appended transiently, then reverted):

```
$ git check-ignore -v .dev/.../D-0060/fixture-slow-shrink-F-5-4.log
.gitignore:242:!.dev/releases/**/artifacts/**/fixture-*.log	.dev/.../fixture-slow-shrink-F-5-4.log
exit=0
```

With `-v`, a file un-ignored by a `!` negation **prints the negation line and exits 0** — the opposite of "prints nothing, exits non-zero." (The "prints nothing, exit 1" behavior is the *non-`-v`* form: `git check-ignore <path>`.) An executor following the instruction literally will see output + exit 0, conclude the result "contradicts the expected split," trigger the halt clause, and **the fix never lands** — a clean false-negative that blocks the whole task.

This is why the inline rf-qa task-integrity gate passed it: rf-qa verified the *fix* is correct against repo state; it did not simulate the executor running the `-v` command and matching its output against the prose assertion.

**Recommended fix (pick one):**
- **(a) boolean form** — replace with `git check-ignore -q <path>` per fixture; **exit 1 = un-ignored (PASS)**, exit 0 = still ignored (FAIL). Cleanest for a pass/fail gate.
- **(b) keep `-v`, fix the assertion** — expect each of the 6 to **print a line whose rule begins with `!`** (the negation is winning) and exit 0; for the "stay ignored" probe, expect the printed rule to be `*.log`. More informative, but string-matching.

### 🟠 MEDIUM — F2: Step 1.3 branches off `origin/master` from a dirty tree with diverging tracked files → checkout may abort

Step 1.3 runs `git checkout -b fix/ci-canonical-brainstorm-hermetic origin/master`. The current working tree has **modified tracked files** under `.dev/releases/current/MultiModelSwarm/` that **diverge from `origin/master`** (reproduced: 10+ files report `DIVERGES`). `git checkout -b <new> origin/master` tries to carry uncommitted changes forward; when a locally-modified file's content differs at the target ref, git aborts with *"Your local changes would be overwritten by checkout."*

Step 1.3's fallback only covers *"origin/master cannot be fetched or the branch already exists"* — it does **not** cover a checkout abort from local modifications, so the executor hits an unhandled failure at the very first mutating step.

(The 6 target fixtures are untracked and carry across any checkout fine — they are not the problem. The modified *tracked* `MultiModelSwarm/` files are.)

**Recommended fix (pick one):**
- Add a pre-step: `git stash push -u -- <unrelated paths>` or a full `git stash`, branch, then `git stash pop` after — but the unrelated changes belong to the `docs/pr133` branch, so simpler:
- **Use a worktree:** `git worktree add ../IronClaude-cifix -b fix/ci-canonical-brainstorm-hermetic origin/master` (clean tree, no interaction with the dirty `docs/pr133` working copy; the untracked fixtures must then be copied/regenerated there — so worktree is heavier here).
- **Simplest:** widen Step 1.3's fallback to detect the abort and instruct `git stash --include-untracked` is **wrong** (would hide the fixtures); instead stash only tracked modifications: `git stash push -- .dev/releases/current/MultiModelSwarm/` (or the diverging set), then branch, leaving untracked fixtures in place. Document the stash-pop as a cleanup step.

## Best-practice compliance (grade 3/5)

**Strong:** explicit `.claude/`-staging guards at 4 points; `-f` forbidden; atomic-commit framing; the 12-vs-6 over-match documented as known side-effect (from the rf-qa pass); production code explicitly out-of-scope; ruff check + format-check run separately; regression/monotonicity halt ordering in the QA gate.

**Deductions:** F1 (a verification step that asserts the wrong command behavior is worse than no check — it actively blocks success); F2 (first mutating step has an uncovered failure mode).

## Grounding gaps / human decision

`needs_human_decision: true` — F1 and F2 each need a one-line decision on which remediation to apply. Neither changes the *fix* (the diagnosis and the two diffs are correct); both are about the *executor harness* in the task file. The task is safe to run **only after** F1 is corrected (without it, Step 2.1 halts).

## Next step

Fix F1 (required) and F2 (recommended) in the task file, then execute. Paste-ready:

```
Apply reflect findings F1 (fix the git check-ignore -v assertion in Step 2.1) and F2 (handle dirty-tree checkout in Step 1.3) to the task file, then I'll run /task
```

Or, if you'd rather I just correct the two steps and proceed:

```
Patch Step 2.1 to use `git check-ignore -q` (exit 1 = un-ignored) and Step 1.3 to stash tracked MultiModelSwarm changes before branching, then run /task
```
