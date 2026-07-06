# Reflect REPORT — UC-1 Pre-Execution Audit

- **Mode:** pre (UC-1 coverage + plan-soundness audit)
- **Tier reached:** 1 (grounded single-agent pass)
- **Subject:** `.dev/tasks/to-do/TASK-RF-20260525-194356/TASK-RF-20260525-194356.md` — "Implement superclaude init-lite --context-optimized"
- **Spec surface:** task's 5 Key Objectives + Safety Invariants (self-contained MDTM task)
- **Date:** 2026-06-03
- **Calibrated confidence:** 0.88
- **Coverage:** 5/5 objectives mapped (coverage_pct = 1.00)
- **Best-practice grade:** 3/5 (well-structured plan; one high-impact change is unguarded + a validation gap)
- **Citations:** 9 grounded / 0 dropped / 1 [INFERRED]

> **Relationship to prior QA.** The 2026-05-27 `qa/qa-task-validation-report.md` was a *structural* task-integrity review (MDTM template conformance, citation-resolves, producer→consumer ordering). It passed 16/16 and remains valid. **This audit is complementary**: it checks whether the *plan is sound and complete against its objectives* — a different axis. The headline finding below was out of scope for the structural QA.

---

## Headline Finding (HIGH / regression risk) — F1

**The installer-mapping fix (Objective 3 / Step 2.3) has an unacknowledged blast radius across all 16 existing protocol skills and risks bricking every `/sc:*` command for end-user `superclaude install`.**

### Evidence chain (all Grounded, re-verified 2026-06-03)

1. The current matcher strips only the `sc-` prefix:
   `src/superclaude/cli/install_skills.py:27` → `cmd_name = skill_name[3:]`.
   So `sc-roadmap-protocol` → `commands/roadmap-protocol.md` (absent) → `_has_corresponding_command` returns **False** → the skill **is currently installed standalone**.
2. The repo has **16** `sc-*-protocol` skill dirs, and **every one** has a matching `commands/<command>.md` (verified by enumerating `src/superclaude/skills/sc-*-protocol` against `src/superclaude/commands/`). None of the 16 is currently detected as command-backed (per #1).
3. Step 2.3's fix generalizes the match to `sc-<command>-protocol` → `commands/<command>.md`. Applied to the 16 skills, every one now matches → each is appended to `served_by_command` and its standalone install is removed via `shutil.rmtree` (`install_skills.py:60-68`, `:94-98` — "skills served by /sc: commands (not installed as skills)").
4. Every `/sc:*` command activates its skill **by name**: `commands/reflect.md:125` → `> Skill sc:reflect-protocol`; `commands/roadmap.md:85` → `> Skill sc:roadmap-protocol`.
5. **[INFERRED, high-confidence]** For a pipx/`superclaude install` end user, removing the standalone install of `sc-<command>-protocol` means the `Skill sc:<command>-protocol` activation can no longer resolve → the slash command breaks. (Grounded portion: the fix removes the installs. Inferred portion: that Claude Code cannot resolve a skill that was never installed — true under the documented install model; the dev `.claude/` mirror is populated by `make sync-dev` independently, which is why this is invisible in this repo.)

### Why the task missed it

Both the task and `research-notes.md:20` framed the installer's job as mapping `sc-<command>` (bare) → `commands/<command>.md`. In reality **there are zero bare `sc-<command>` skills** — all 16 real skills are `sc-<command>-protocol`. So Step 2.3's guard *"ensuring existing `sc-<command>` mapping behavior remains unchanged"* protects a set that does not exist, while the change's actual effect lands on the 16 protocol skills that the task never enumerates.

### Unresolved decision the task must answer first

Whether command-backed protocol skills **should** be installed standalone is genuinely ambiguous: the `install_skills.py:7-10` docstring says the *intent* is to NOT double-install them, but the live system depends on them being installed for `Skill` activation. The task does not resolve this. Either way it is under-specified:
- If they SHOULD stay installed → the fix must be scoped so it does **not** sweep the 16 (e.g., gate on the command file declaring a backing protocol skill, or only skip when no standalone invocation contract exists).
- If they SHOULD become command-only → the task must additionally (a) acknowledge the 16-skill migration, (b) verify `/sc:*` activation still works without standalone installs, and (c) handle removal of 16 currently-installed copies.

---

## Coverage Matrix (objectives → checklist)

| # | Key Objective | Covered by | Verdict |
|---|---------------|-----------|---------|
| 1 | Safe CLI `init-lite --context-optimized` + flags | 2.1, 2.2, 3.1, 3.2, 4.1 | ✅ Covered |
| 2 | Thin `/sc:init-lite` command + `sc-init-lite-protocol` skill | 2.4, 2.5 | ✅ Covered |
| 3 | Installer mapping fix for `sc-<command>-protocol` | 2.3, 3.3, 4.2 | ⚠️ Covered but **unsound/untested** (see F1, F2) |
| 4 | Protect target projects (no mutation; dry-run writes nothing) | 2.1, 3.1 | ✅ Covered (byte-preservation pinned by 3.1) |
| 5 | Validate with tests + sync checks | 4.1–4.6 | ⚠️ Covered but **incomplete** (see F3) |

**coverage_pct = 1.00** — every objective is mapped. The risk is not missing coverage; it is *soundness* on Obj 3 and *completeness* on Obj 5.

---

## Gap Registry

| ID | Sev | Finding | Evidence | Recommendation |
|----|-----|---------|----------|----------------|
| **F1** | HIGH | Installer fix sweeps all 16 `sc-*-protocol` skills; end-user-install regression risk; underlying "should they be installed?" decision unresolved | `install_skills.py:19-30,58-68,94-98`; 16/16 command matches; `commands/reflect.md:125`, `commands/roadmap.md:85` | Resolve the install-vs-served decision **before execution**; scope the fix so it does not silently reclassify the 16; add explicit migration handling if intended |
| **F2** | HIGH | No test guards the 16-skill interaction. `tests/unit/test_cli_install.py` has **no** `served_by_command`/protocol coverage (grep empty). Step 3.3 tests only `sc-init-lite-protocol` + a non-existent `sc-<command>` bare set | grep `served_by_command` in `tests/unit/test_cli_install.py` → 0 hits | Add a Step-3.3 test asserting each existing `sc-<command>-protocol` whose command exists is handled per the **chosen** policy, and that `/sc:*` activation contract is preserved |
| **F3** | MED | Step 4.5 runs only `make lint` (`ruff check .`). CI separately runs `ruff format --check src/ tests/` (`quick-check.yml:41`, `test.yml:100`). New `init_lite.py` can pass `make lint` yet fail CI format | `Makefile:48-50`; `.github/workflows/test.yml:98-100` | Add `uv run ruff format --check src/ tests/` (or `make format`) to Step 4.5 so green local validation ⇒ green CI |
| **F4** | LOW | `--force` semantics under-specified — what it overrides (regenerate marked report? overwrite scaffold?) is not crisply stated in any item; only its no-mutation safety is pinned (3.1 byte-preservation across force mode) | task §Obj1, Step 2.1, Step 3.1 | Add one sentence to Step 2.1 defining exactly what `--force` overwrites (must stay within `.dev/superclaude/`) |
| **F5** | LOW | Step 4.6 bundles assess + conditional remediation in one item (session-rollover risk) | concurs with prior QA advisory (qa report §Recommendations) | Optional split into assess / remediate; non-blocking |

---

## Recommendation

**Do not execute as-is.** Coverage is complete, but **Objective 3 is the single most impactful change and it is both unsound-by-default and untested** (F1+F2). Resolve the install-vs-served-by-command policy and add the interaction test *before* `/task`. F3 is a cheap, high-value add to the validation step. F4/F5 are polish.

This is a pre-execution audit: ~spend now (one decision + one test + one validation line) to avoid an end-user-install regression discovered only after merge.

---

## Inferred-claim ledger

- **[INFERRED]** (F1, step 5): that an uninstalled skill cannot be resolved by `Skill sc:<command>-protocol` for pipx end users. Load-bearing for the *severity* of F1, not for the *existence* of the behavior change (the rmtree of 16 installs is Grounded). Confirm by checking whether `superclaude install`'s command path installs skills by any route other than `install_all_skills` (grep showed none in `src/superclaude/cli/`).
