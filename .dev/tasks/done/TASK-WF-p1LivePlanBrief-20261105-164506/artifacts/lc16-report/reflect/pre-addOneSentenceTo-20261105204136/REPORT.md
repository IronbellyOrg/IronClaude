```yaml
contract_version: 1.8.0
status: success            # evidence-validator ran: 20 of 20 verified, 0 dropped (zero-drop flag set in audit.log)
mode: pre
tier_reached: 2
confidence_calibrated: 0.73
citations_total: 20
citations_revalidated: 20
citations_dropped: 0
citations_inferred: 3
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

# Reflect report: pre-execution audit of TASK-WF-addOneSentenceTo-20261105-204034

Spec: `.dev/tasks/to-do/TASK-WF-addOneSentenceTo-20261105-204034/source.md`. Plan: `.dev/tasks/to-do/TASK-WF-addOneSentenceTo-20261105-204034/TASK-WF-addOneSentenceTo-20261105-204034.md`. Advisory and read-only: this report never edits the plan.

## Verdict

The plan is executable as written, with three fixable gaps. Merged verdict: `sound-with-notes` (`.dev/reflect/pre-addOneSentenceTo-20261105204136/adversarial/merged-verdict.yaml`, merge method `adversarial`, base variant sonnet:analyzer).

- The sentence the spec asks for is inaccurate in both directions (F-1).
- Acceptance criterion 2 is weak (F-2).
- The debate's own replacement for criterion 2 fails on a correct run and must not be adopted (F-2).

Tier 2 ran because the spec is a single unlabeled sentence, so every requirement is inferred and the parse-density guard forbids a Tier 1 stop (`.dev/reflect/pre-addOneSentenceTo-20261105204136/artifacts/tier_decision.yaml`). Convergence: 8 of 8 diff points agreed, status BLOCKED_BY_INVARIANTS because two HIGH-severity invariants (INV-003, INV-012) stayed open at standard depth; the recommended text below addresses them but no debate round tested it.

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation | Match result |
|--------|----------------|----------|--------------|
| INF-001 | "Add one sentence to the Installation section of README.md stating that superclaude install --force overwrites files that already exist in ~/.claude" | `.dev/tasks/to-do/TASK-WF-addOneSentenceTo-20261105-204034/source.md:1` | Task 1 (covered) |

Coverage: `coverage_pct` null (no parsed rows); `coverage_pct_union` 1.0; `unmapped_requirements_union` empty.

## Findings

Every finding is a plan gap or a confirmation, not a deviation from executed work (nothing has been executed). Severity is minor for all five; none blocks the plan as written.

### F-1: The requested sentence is inaccurate in both directions (class: gap)

- **Plan location:** `.dev/tasks/to-do/TASK-WF-addOneSentenceTo-20261105-204034/TASK-WF-addOneSentenceTo-20261105-204034.md:26`
- **Evidence (overstates):** a seed data file is deployed only when absent and is never overwritten even with `--force` (`src/superclaude/cli/install_hooks.py:89-95`), and `--force` is not forwarded to the codegraph phase (`src/superclaude/cli/main.py:52`).
- **Evidence (understates):** with `--force`, core files are copied over existing ones (`src/superclaude/cli/install_core.py:69`), each shipped skill folder is deleted and re-copied (`src/superclaude/cli/install_skill.py:47-48`), and the install guide warns that no backup is kept and files a user added inside a shipped skill folder are lost (`docs/getting-started/installation.md:593`).
- **Classification rationale:** both advocates that claimed user files are left alone (V1 "never touched", V3 "leaves user-created files alone") conceded the claim false in Round 2. The spec supplies the broad wording, so this is a spec-accuracy gap, not plan drift.
- **Default remediation:** use the recommended sentence in R-001.

### F-2: Acceptance criterion 2 is weak, and the debate's replacement fails (class: gap)

- **Plan location:** `.dev/tasks/to-do/TASK-WF-addOneSentenceTo-20261105-204034/TASK-WF-addOneSentenceTo-20261105-204034.md:30`
- **Evidence:** plain `git diff --stat` cannot see staged or untracked changes, so it can pass when another file changed. [INFERRED] It can also list `.dev/tasks` files after `/sc:implement` stages and then edits the package, because that command must stage `.dev/tasks/` (`src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:36`).
- **V3's Round 2 replacement** (record `git status --porcelain` and `git diff --cached --name-only` before, require both unchanged except ` M README.md` after) fails on a correct run for the same staging reason (INV-003) and does not say where the baseline is kept (INV-001). Do not adopt it.
- **Default remediation:** use the criterion text in R-002. That text is orchestrator-derived from INV-003's fix and was not debated.

### F-3: "Framework files" does not tell readers their own CLAUDE.md is replaced (class: gap)

- **Evidence:** the core installer copies every `core/*.md` when `--force` is set (`src/superclaude/cli/install_core.py:57`), which includes `CLAUDE.md` and `RULES.md`; the install guide names both (`docs/getting-started/installation.md:593`). Raised by the fault-finder (INV-010), not by any card.
- **Default remediation:** name both files in the sentence (R-001).

### F-4: Placement and fallout are fine (class: none)

- `README.md:64` is the single-line paragraph under "Install the current package/CLI" (`README.md:55`). The Upgrading block (`README.md:66-75`) is left alone and already uses the same "framework files" term (`README.md:75`).
- No other doc needs a change: `docs/getting-started/installation.md:283` and `docs/getting-started/upgrading.md:56-60` already agree. The only test that reads the repo-root README checks links to retired docs (`tests/docs/test_retired_docs_absent.py:37-49`); a link-free sentence cannot trip it, and no test can catch a factually wrong sentence.

### F-5: The plan covers the whole spec sentence (class: none)

- INF-001 maps to Task 1 (`.dev/tasks/to-do/TASK-WF-addOneSentenceTo-20261105-204034/TASK-WF-addOneSentenceTo-20261105-204034.md:19-30`). Coverage and factual accuracy (F-1) are separate judgments.

## Inferred-claim audit

- `citations_inferred: 3`
- Inferred-fraction: `3 / 20` = 0.15
- Evidence check: an independent validator re-Read all 20 ranges and verified every one. A zero-drop pass is a flag, not a clean bill; its notes: the cited lines for `install_hooks.py:89-95` and `main.py:52` are a comment and a docstring (the behavior is in `install_hooks.py:554-556` and `main.py:240-246`, which it also read), and `install_core.py:69` is the skip guard (the copy is at line 74).
- The three inferred items: the staging side effect in F-2, the orchestrator-derived criterion text in R-002, and the statement that no test can catch a wrong sentence in F-4.

## Recommendations

### Recommendation R-001: Replace the spec sentence with an accurate one

- **File:** `.dev/tasks/to-do/TASK-WF-addOneSentenceTo-20261105-204034/TASK-WF-addOneSentenceTo-20261105-204034.md` (title line 12, Goal line 15, Task 1 line 26, acceptance criterion 1 line 29)
- **Change:** the claim is worded differently in four places (title line 12 "overwrites existing files in ~/.claude"; Goal line 15 and Task 1 line 26 "overwrites files that already exist in `~/.claude`"; criterion 1 line 29 "overwrites files that already exist there"), so a literal find-and-replace would miss some. Rewrite each to this final wording: "Running `superclaude install --force` overwrites the framework files it ships that already exist in `~/.claude` (including `CLAUDE.md` and `RULES.md`) without keeping a backup, and deletes and re-copies each shipped skill folder, so any file you added inside one is lost." Shorter alternative: "`superclaude install --force` overwrites the framework files it ships that already exist in `~/.claude`." The title, Goal and criterion 1 must carry the same wording. This changes the spec's own words, so the plan owner decides.
- **Verifier:** the README sentence names `superclaude install --force` and `~/.claude`, says "overwrites" and "already exist", and agrees with `docs/getting-started/installation.md:593` and `src/superclaude/cli/install_hooks.py:89-95`.
- **Linked findings:** F-1, F-3
- **Priority:** P1

### Recommendation R-002: Replace acceptance criterion 2

- **File:** `.dev/tasks/to-do/TASK-WF-addOneSentenceTo-20261105-204034/TASK-WF-addOneSentenceTo-20261105-204034.md` (line 30)
- **Change:** replace it with: "`git status --porcelain -- . ':!.dev/tasks' ':!.dev/reflect'` prints exactly one line, for README.md, and `git diff --word-diff HEAD -- README.md` shows one hunk whose only change is the added sentence {+...+} at the end of the paragraph that starts 'This installs the package', with no [-...-] deletions."
- **Verifier:** after a correct run, run both commands and confirm one status line (README.md) and one word-diff hunk containing only {+...+}. The status command printed nothing on the clean tree before the edit; the full check has not been run on an executed plan.
- **Linked findings:** F-2
- **Priority:** P1

### Recommendation R-003: Run the docs tests after the edit

- **File:** `tests/docs/test_retired_docs_absent.py`
- **Change:** none to the file; run it after the README edit.
- **Verifier:** `uv run pytest tests/docs` passes.
- **Linked findings:** F-4
- **Priority:** P2

## Artifacts

- Merged verdict: `.dev/reflect/pre-addOneSentenceTo-20261105204136/adversarial/merged-verdict.yaml`
- Debate record: `.dev/reflect/pre-addOneSentenceTo-20261105204136/adversarial/adversarial/` (diff-analysis, debate-transcript, invariant-probe, base-selection, refactor-plan, merge-log, return-contract)
- Reviewer cards and calibrations: `.dev/reflect/pre-addOneSentenceTo-20261105204136/reviewer-cards/`, `.dev/reflect/pre-addOneSentenceTo-20261105204136/artifacts/`
- Calibrated confidence (blind, opus, calibrator diversity degraded): Tier 1 card 0.76; reviewer cards V1 0.82, V2 0.59, V3 0.78 (mean 0.73)
