# QA Report — task-qualitative (operational-correctness lens)

**Topic:** TASK-RF-submit-pr-20260611-030241 — sc:submit-pr PR review auto-remediation
**Date:** 2026-06-11
**Phase:** task-qualitative
**Fix cycle:** N/A (fix_authorization: false)
**Lens:** operational-correctness — will each item actually succeed when executed?
**Inherited Structural Verdict:** A.10 PASSED (B2 lens). Structure NOT re-verified; semantic operational checks only.

---

## Overall Verdict: PASS (8/8 operational checks PASS)

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Coverage arg `--cov=superclaude.submit_pr` valid | none | PASS | pyproject.toml — `[tool.coverage.run] source=["src/superclaude"]`; `superclaude.submit_pr` is a valid Python dotted id (verified), hyphenated target invalid (verified) |
| 2 | Markers add-4 necessary + `--strict-markers` | none | PASS | pyproject.toml L111 `--strict-markers`; L114-140 markers — none of `loop_guard`/`autonomy`/`recovery`/`p0` registered → add-4 item correct & necessary |
| 3 | Hook edit feasibility + src-only discipline | none | PASS | offer-pr-review.sh fail-open (`exit 0` everywhere, additive stdout); task L78/L119 mandate src-only + `make sync-dev`, never `git add .claude/hooks` |
| 4 | Make targets exist + lint≠format split | none | PASS | Makefile: `sync-dev:` L109, `verify-sync:` L166, `lint:` L48 (`uv run ruff check .` only); task keeps format as separate `uv run ruff format --check src/ tests/` gate (L80/L137/L457) |
| 5 | Dispatch flags never `--depth quick --fix` | none | PASS | task L135/L270/L276/L279/L285: Medium→`--fix`, High/Critical→`--depth deep --fix`, NEVER `--depth quick --fix`; tests assert no such emission |
| 6 | R1 DET probe HALT (needs_human_decision) | none | PASS | task Step 2.0 (L196-197): `needs_human_decision` HALT, writes PENDING, ships `locked:false`, never auto-locks/hard-guesses login, downstream proceeds on synthetic fixtures |
| 7 | POST-reflect item correctness | none | PASS | task L463: `<BASE>=git merge-base HEAD origin/master` (symbolic default master), `git add -A` FIRST, SINGLE ref vs working tree (not range), SELF-RUN subagent, penultimate before Done-flip (L465) |
| 8 | gh `--repo` pin + origin push | none | PASS | task L130/L197/L292/L314/L317/L320: every gh/gh api pins `--repo IronbellyOrg/IronClaude`; push target `origin` never `upstream`/`master` (L130/L323); T-104 static-grep test enforces it |

---

## Check-by-check findings

### Check 1 — Coverage arg `--cov=superclaude.submit_pr` valid — PASS
- `pyproject.toml` `[tool.hatch.build.targets.wheel] packages = ["src/superclaude"]` and `[tool.coverage.run] source = ["src/superclaude"]` (L142-143). The deterministic core lives at `src/superclaude/submit_pr/`, so it imports as `superclaude.submit_pr` and is on the coverage source path.
- Verified `all(p.isidentifier() for p in "superclaude.submit_pr".split("."))` → True; `"superclaude.skills.sc-submit-pr-protocol"` → False (hyphens are illegal Python identifiers). The task's SPEC CORRECTION #2 (L132) correctly replaces the unresolvable spec line-1025 target with `--cov=superclaude.submit_pr`. **Operationally correct.**

### Check 2 — Markers + `--strict-markers` — PASS
- `[tool.pytest.ini_options].addopts` includes `--strict-markers` (L111) → an unregistered marker raises a hard error, so the add-4-markers item is genuinely necessary (tests using `@pytest.mark.loop_guard/autonomy/recovery/p0` would error-collect otherwise).
- Read the full `markers` list (L114-140): `loop_guard`, `autonomy`, `recovery`, `p0` are all ABSENT. SPEC CORRECTION #3 (L133) registers exactly these 4 and correctly drops the 5th `loop` (R4 over-count). **Item correct and necessary.**

### Check 3 — Hook edit feasibility + src-only — PASS
- Read `src/superclaude/hooks/scripts/offer-pr-review.sh`: it is a PostToolUse(Bash) fail-open hook — every exit path is `exit 0` (lines 21,25,28,35,39,74) and it only emits additive stdout context. Adding a `sc:submit-pr --monitor` mention to the offer block (the `cat <<EOF`) is fully achievable without changing the fail-open contract.
- Task encodes src-only discipline: L78 ("`src/`-only"), L119 ("`make sync-dev` mirrors it to `.claude/hooks/`"), L129 SoT rule. No item stages `.claude/hooks`. **Feasible + disciplined.**

### Check 4 — Make targets + lint≠format split — PASS
- Makefile greps: `sync-dev:` (L109), `verify-sync:` (L166), `lint:` (L48). The `lint` body is `uv run ruff check .` ONLY (L50) — it does NOT run `ruff format --check`.
- Task keeps the two gates separate (VG-3≠VG-4): `make lint` AND a distinct `uv run ruff format --check src/ tests/` appear as separate gates (L80, L137, L457), with T-511 as the regression test. This matches the documented gotcha (memory `make_lint_vs_ci_ruff_format`). **Correct split.**

### Check 5 — Never `--depth quick --fix` — PASS
- Constraint L135 (SPEC CORRECTION #5): `--depth quick`+`--fix` is an explicit STOP/conflict; routes Medium→`/sc:troubleshoot --fix` (defaults standard), High/Critical→`--depth deep --fix`.
- Build items enforce it: severity_router (L270) "routing NEVER emits `--depth quick --fix`"; troubleshoot-dispatch ref (L276) "EXPLICITLY note `--depth quick --fix` is a STOP/conflict that must NEVER be emitted"; tests T-301/302/310/311/312 (L279) and T-320/330/331 (L285) assert no `--depth quick --fix`. Edit-application owned by FSM `S3_FIXING` (not troubleshoot auto-apply). **No conflicting flag emission anywhere.**

### Check 6 — R1 DET probe HALT — PASS
- Step 2.0 (L196-197) is a `needs_human_decision` operator item that: writes a `needs_human_decision: PENDING` Task-Log entry, ships `detection-contract.md` with `locked: false`, NEVER auto-locks, NEVER hard-guesses `augment_bot_login` (stays `<PROBE-LOCKED>`, see L200), and explicitly does NOT block remaining internal-pure phases (synthetic fixtures per §18.4). T-210 mechanically blocks arming until an operator flips `locked:true`. Matches memory `feedback_human_decision_items_must_halt` (HALT, never auto-default). **Correct HALT semantics.**

### Check 7 — POST-reflect item — PASS
- L463 computes `<BASE> = git merge-base HEAD origin/master` (notes repo default branch = master), runs `cd /config/workspace/IronClaude && git add -A` FIRST so new files enter the diff surface, passes `<BASE>` as a **SINGLE ref against the working tree — NOT a `start..HEAD` range** (matches memory `task-builder` POST-reflect --diff convention / commit #153), names `/sc:reflect` (never `/sc:task`), `--depth deep`, `--spec` the merged spec.
- It is a **SELF-RUN subagent gate, explicitly "NOT a human HALT"**, records `reflect_post`, and is the **penultimate** item — immediately followed by the Done-flip at L465 (which gates on `reflect_post` being populated). **All 5 sub-criteria satisfied.**

### Check 8 — gh `--repo` pin + origin push — PASS
- Constraint L130: `--repo IronbellyOrg/IronClaude` pin on every gh/gh api; push target `origin`, never `upstream`; PR-target the fork.
- Enforced in items: runbook (L197), augment-poll ref (L292 "all `--repo IronbellyOrg/IronClaude`-pinned"), poll script (L314 "EVERY gh/gh api call pins `--repo`"), thread-reply ref (L317), reply-resolve script (L320). Push discipline L323: "`git push origin <target_sha>:<target_branch>` (never `upstream`, never `master`)". T-104 static-grep test (L379) asserts no bare `gh ` without `--repo` in skill+hook sources. Matches CLAUDE.md fork-only PR rule + memory `feedback_pr_target_fork_only`. **Disciplined throughout.**

---

## Summary
- Checks passed: 8 / 8
- Checks failed: 0
- Critical issues: 0 | Important: 0 | Minor: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found
None. All 8 high-value operational checks PASS.

## Confidence
Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100% (of the 8-check scoped subset)
**Scope caveat:** This was an 8-check targeted operational subset per the spawn prompt, NOT the full 15-item task-qualitative checklist. The 8 cover the highest-risk operational seams (coverage/marker/make-target reality, hook+gh+SoT discipline, troubleshoot-flag conflict, HALT semantics, POST-reflect diff mechanics). Cross-phase data-flow traces (items 6,10) and exhaustive function-signature verification of the ~9 Python modules were OUT OF SCOPE for this pass.

## Tool engagement
Read: 4 (report, task file [2 pages], pyproject.toml, offer-pr-review.sh) | Grep: 5 (Makefile targets, identifier-validity checks, 4 task-file greps) | Glob: 0 | Bash: 5
- Tool calls (≥9) ≥ 8 scoped checks: engagement floor satisfied.
- No web research performed (all verification local-file-bound) — Tavily-first N/A this run.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)
- Relied on A.10 (B2-lens) structural PASS for: item shape, frontmatter schema, section numbering, phase-reference correctness → did NOT re-verify these.
- Independent semantic checks requiring my own tool engagement (reliance ≠ verification):
  - Coverage-arg *resolvability* (Check 1): A.10 confirms the arg string is present/well-formed; I independently verified via Python identifier analysis that `superclaude.submit_pr` actually resolves and the hyphenated form does NOT — a semantic correctness fact A.10's structural pass does not establish.
  - Marker *necessity* (Check 2): I read live pyproject.toml to confirm the 4 markers are genuinely unregistered AND `--strict-markers` is active, proving the add-4 item is operationally required (not just structurally well-formed).
  - `make lint` *body* (Check 4): I read the actual Makefile `lint:` recipe (`ruff check .` only) to confirm the lint≠format split is real at the source, not merely asserted in task prose.

## VERDICT: PASS
