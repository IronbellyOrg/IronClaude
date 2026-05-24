# Adversarial Validation Report — Option C (orphaned commits)

**Topic**: Should we open a follow-up PR from `fix/prd-build-task-file-glob`
containing the 3 orphaned commits (`1550ea5f`, `fcd28bfa`, `e1c458bd`)?

**Mode**: Adversarial debate, 2 positions, standard depth.
**Convergence**: 100% (both advocates aligned on HYBRID synthesis in Round 2).
**Date**: 2026-05-21T19:25:00Z

---

## TL;DR — Verdict

**Recommendation**: **Option C-MODIFIED** (HYBRID synthesis between the two
original positions). Specifically:

1. **Cherry-pick `1550ea5f`** (cliEval F401 + mix_stderr + dead skeleton) —
   safe, conflict-free, fixes active CI regression.
2. **Cherry-pick `e1c458bd`** (freshness hook anti-avoidance framing) —
   safe, conflict-free, additive defense-in-depth.
3. **Extract `.markdownlint.json` hunk from `fcd28bfa` as a NEW commit** —
   net-new content (9 LOC), no overlap with PR #70.
4. **ABANDON the rest of `fcd28bfa`** (skill, agents, commands troubleshoot.md
   SoT-restore content) — superseded by PR #70 + `9316d2ee` with newer
   `test_is_wrong` contract additions.

**Confidence**: 0.92.

---

## Why Option-C-as-stated has negative outcomes

The original Option C proposed cherry-picking all 3 commits as a bulk PR.
The decisive failure mode is **`fcd28bfa`** specifically:

| Empirical measurement | Result | Interpretation |
|---|---|---|
| `git diff fcd28bfa HEAD -- src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md \| wc -l` | **273 lines** | The skill file has diverged substantially between fcd28bfa and HEAD |
| `git show fcd28bfa:src/.../SKILL.md \| grep -c test_is_wrong` | **0** | fcd28bfa's version lacks the new contract field |
| `git show HEAD:src/.../SKILL.md \| grep -c test_is_wrong` | **4** | HEAD has 4 references to the new field (commit `9316d2ee`) |

A naive cherry-pick of `fcd28bfa` would:
- **Either** conflict on every file in the skill package (10 files, ~2700 lines
  of merge resolution surface), AND on `src/superclaude/agents/{confidence-calibrator,evidence-validator}.md`,
  AND on `src/superclaude/commands/troubleshoot.md`
- **Or** silently overwrite the user's newer `test_is_wrong` contract work
  (4 lines, structural impact on downstream automation)

Both outcomes are negative. The conflict resolution path is error-prone at
this scope; the silent-overwrite path destroys post-fcd28bfa improvements.

## Why Option-C-as-stated has positive outcomes for the other 2 commits

The same empirical measurement reveals `1550ea5f` and `e1c458bd` are safe:

| Empirical measurement | Result | Interpretation |
|---|---|---|
| `git log 1550ea5f..HEAD -- src/superclaude/cli/eval/commands.py tests/cli/eval/test_eval_group.py` | **empty** | Zero intervening commits touched these files |
| `git log e1c458bd..HEAD -- src/superclaude/hooks/scripts/freshness-pre-edit.sh` | **empty** | Zero intervening commits touched this file |

Cherry-picks of these specific commits produce the exact intended diff with
no merge work. Both fix real problems:

- `1550ea5f`: active CI regression at `tests/cli/eval/test_eval_group.py:114`
  (Click 8.3.2 `TypeError: CliRunner.__init__() got an unexpected keyword
  argument 'mix_stderr'`) + 3 F401 imports at `src/superclaude/cli/eval/commands.py:31,34,75`
- `e1c458bd`: defense-in-depth complement to the B7 memory record
  (`feedback_no_strategy_pivot_to_avoid_hooks.md`), enforces the
  no-mdformat-pivot lesson at the hook layer

## Top 3 risks of the recommended HYBRID approach

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|------------|--------|------------|
| 1 | Cherry-pick of `1550ea5f` could touch files that were renamed/moved by an unrelated commit not picked up by the file-path log | LOW | MEDIUM | Review the cherry-pick diff before pushing; revert if surprises |
| 2 | The new `.markdownlint.json` config could trigger pre-commit failures on OTHER markdown files in the repo (e.g., a doc file with a 250-char line) | MEDIUM | LOW | Run `uv run pre-commit run markdownlint --all-files` after applying; address fallout in a separate commit |
| 3 | The freshness hook strengthening might conflict with future hook-related work the user has planned | LOW | LOW | Hook is additive (only changes error messages); easy to re-roll if needed |

## Confidence breakdown

- **0.92** overall confidence in the HYBRID recommendation
- **0.95** confidence that `1550ea5f` cherry-pick is safe (empty intervening log)
- **0.95** confidence that `e1c458bd` cherry-pick is safe (empty intervening log)
- **0.98** confidence that `fcd28bfa` cherry-pick is UNSAFE (273-line divergence is decisive)
- **0.85** confidence that the `.markdownlint.json` extraction is genuinely free of overlap (could in principle conflict with a hypothetical future markdownlint config the user has planned)

## Recommendation execution plan (paste-ready, single-line per memory rule)

Three operations, in order:

```
git cherry-pick 1550ea5f
```

```
git cherry-pick e1c458bd
```

```
git show fcd28bfa -- .markdownlint.json | git apply && git add .markdownlint.json && git commit -m "chore: add .markdownlint.json with line_length 160 (extracted from orphaned fcd28bfa)"
```

(The third command extracts only the `.markdownlint.json` hunk from
`fcd28bfa` as a fresh commit. Adjust the commit message to taste.)

After all three, run:
- `make verify-sync` (expect ✅)
- `uv run pre-commit run markdownlint --all-files` (audit fallout from the new config)
- `uv run pytest tests/cli/eval/` (verify the regression is fixed)

## Alternatives considered and rejected

| Alternative | Rejected because |
|-------------|------------------|
| (a) Original Option C — cherry-pick all 3 commits as bulk PR | fcd28bfa would destroy or conflict with 4 `test_is_wrong` refs in HEAD; ~2700-line conflict resolution surface |
| (c) Drop all 3 commits entirely | Loses active regression fix (`mix_stderr` TypeError) + freshness hook strengthening + `.markdownlint.json` policy — all genuinely valuable work |
| (d) Re-apply all 3 commits as fresh commits (no cherry-pick) | Adds unnecessary work for the 2 commits where cherry-pick is empirically safe; loses commit-message rationale unnecessarily |

## Process artifacts

- `adversarial/variant-1-pro-c.md` — PRO-Option-C position
- `adversarial/variant-2-anti-c.md` — ANTI-Option-C position
- `adversarial/diff-analysis.md` — structured comparison, 5 diff points
- `adversarial/debate-transcript.md` — 2 rounds + invariant probe
- `adversarial/invariant-probe.md` — Round 2.5 fault-finder findings (6 invariants probed, 0 UNADDRESSED, gate-clean)

## Return contract

```yaml
return_contract:
  merged_output_path: ".dev/reviews/2026-05-21-orphaned-commits-debate/REPORT.md"
  convergence_score: 1.00
  artifacts_dir: ".dev/reviews/2026-05-21-orphaned-commits-debate/adversarial/"
  status: "success"
  base_variant: "ANTI-C (Variant 2)"
  unresolved_conflicts: 0
  fallback_mode: false
  failure_stage: null
  invocation_method: "skill-direct"
  unaddressed_invariants: []
```
