# A.10 Consolidated Task Validation Findings (cycle 1)

Sources: `qa-task-validation-b2-report.md` (B2 lens, VERDICT: FAIL) and `qa-task-validation-structure-report.md` (phase-structure lens, VERDICT: FAIL).

## Items Reviewed

| # | Lens | Check | Result |
|---|------|-------|--------|
| B2-1 | b2 | Every item has 5 B2 components | FAIL |
| B2-2 | b2 | No reliance on prior item context | FAIL |
| B2-3 | b2 | Agent-spawning items embed full prompt | FAIL |
| B2-4 | b2 | File paths specific | PASS |
| B2-5 | b2 | Verification measurable | FAIL |
| B2-6 | b2 | No batch items | FAIL |
| B2-7 | b2 | No items on CODE-CONTRADICTED/UNVERIFIED findings | PASS |
| B2-8 | b2 | Safety constraints in every command-running item | FAIL |
| S-1 | structure | YAML frontmatter | PASS |
| S-2 | structure | Mandatory template sections | PASS |
| S-3 | structure | Phase dependencies logical | FAIL |
| S-4 | structure | Phase ordering | FAIL |
| S-5 | structure | Completion items in final phase | FAIL |
| S-6 | structure | Task Log at bottom | PASS |
| S-7 | structure | Item count reasonable | PASS |
| S-8 | structure | Open Questions documented | PASS |
| S-9 | structure | QA gates M3/M4 and counts | FAIL |
| TB-Add-1 | structure | Placeholder scan | PASS |
| TB-Add-3 | structure | Clarification adjacency | PASS (inactive) |
| TB-Add-4 | structure | DAG | PASS |
| TB-Add-5 | structure | Granularity / XL splitting | FAIL (minor) |
| TB-Add-6 | structure | Verify/Acceptance format | PASS |
| TB-Add-7 | structure | Execution Context source areas | PASS |
| TB-Add-8 | structure | Per-item file:line evidence | FAIL (minor) |

## Blocking Findings (to fix)

| ID | Source | Severity | Location | Fix |
|----|--------|----------|----------|-----|
| C1 | B2#1 + S#5 | CRITICAL | Step 6.2 lens items (7) | Inline the full header (with a concrete N=5), lens-specific instructions, output format and full SAFETY block into each of the 7 items; remove the false "embeds in full" sentence. |
| C2 | B2#2 | IMPORTANT | Step 6.7 item 2 | Write out anti-omission-agent-2's full prompt. |
| C3 | B2#3 | IMPORTANT | Step 3.2 fix item | Forbid nested agent spawns; the fix agent does gap research itself under the full SAFETY block. |
| C4 | B2#4, #5, #6 | IMPORTANT | All gate/verifier/fix/synthesis prompts and the Step 7.2 runner prompt | Add the full four-part SAFETY block (no source edits; uv only; post nothing; experiments only in a `mktemp -d` /tmp repo with a local bare remote, never push to a real remote, clean up) to every agent prompt; put the "only this task package" scope inside the 7.2 prompt. |
| C5 | B2#7 | IMPORTANT | Step 2.2 | Forbid running launch-level-guard.sh; static reading of its regexes only (or run with HOME under mktemp -d and say an ungoverned session exits 0). Prefer static reading only. |
| C6 | B2#8 | IMPORTANT | Step 3.2 verify; Post-Completion item 5 | Use whole-tree `git status --porcelain` and require every changed path to be under `.dev/tasks/to-do/TASK-RESEARCH-pre-push-guard-20261108-095046/` (or pre-existing untracked paths recorded at Step 1.x baseline). |
| C7 | B2#9 + S#4 | IMPORTANT | Step 5.5; verification-pair items (3.3, 5.7, 6.4, 6.6, 6.8); Step 6.9 | One item per agent; split 6.9 into validate item(s) and a conditional fix item. Keep "spawn in ONE message" in the step preamble. |
| C8 | B2#10 | IMPORTANT | Steps 5.3/5.4 | Run 5.4 (and 5.3's reads of synth-01/02) after 5.1-5.3 complete, or remove those cross-file reads. |
| C9 | S#1 | IMPORTANT | Step 7.3/7.4 vs Post-Completion | Move Post-Completion checks before Task Summary and Done; Done is the last item and checks no Blocked was set. |
| C10 | S#2 | IMPORTANT | Step 7.1 vs 7.2 | User summary after the reflect gate and after safety checks. |
| C11 | S#3 | IMPORTANT | Phase 6 preamble, item 312 | Add a final lens re-check (template-conformance, internal-consistency, evidence-quality) scoped to sections changed after Gate 3 PASS, OR reword the final-state claim and log the deviation. |
| C12 | S#6 | IMPORTANT | Gate consolidation/verification filenames | Cycle-suffixed filenames and per-cycle PASS sets recorded in Phase Gate Findings. |

## Cycle 1 outcome

Fix report `qa-task-validation-fix-cycle1.md` VERDICT: PASS; verification `qa-task-validation-verify-cycle1.md` VERDICT: PASS. C1-C12 closed.

## A.10.25 Research-Alignment Blocking Findings (from qa-task-research-alignment-report.md, VERDICT: FAIL)

| ID | Severity | Location | Fix |
|----|----------|----------|-----|
| RA1 | IMPORTANT | Sub-question (b), no item | Add coverage (in an existing Phase 2 or Phase 4 item, or a new item) of pushes via other tools: git libraries (libgit2/pygit2, JGit, isomorphic-git), `gh api` / REST ref updates, curl to the git smart-HTTP endpoint; verify the design claim at §19.3 (design line 520) with doc citations; no real-remote push and nothing posted. |
| RA2 | IMPORTANT | Step 2.1 / Step 2.4 | Record the hook's full relevant environment (HOME, PATH, and the presence of `uv` on PATH) not only `GIT_*`; Step 2.1 must analyse that `identify()` returns `ordinary` when the store under HOME is missing (launch-job-identity.sh 102-106, 220-225) and needs uv on PATH (25-53), i.e. what happens to identification when the hook runs under an agent's HOME/PATH. |
| RA3 | IMPORTANT | Step 2.3 handoff to 2.4 | Remove the impossible handoff, and add explicit experiments in Step 2.4 (or a new follow-up item after 2.3/2.4) for: a configured refspec (`remote.<n>.push`) mapping onto main; a sha256 repo (`git init --object-format=sha256`, oid length 64); a rejected non-fast-forward push (does the hook still run?); a mixed push with the protected ref last; look-alike names `mainline`, `feature/main`, `refs/heads/main2`; plus (minor) `--atomic` and `--force-with-lease`. |
| RA4 | IMPORTANT | Step 5.3 | Make the option list honour design §19.2 (design line 512) placement limits: mark `core.hooksPath`-directory and `extensions.worktreeConfig` options as ruled out by §19.2, or state explicitly why they are being reconsidered. |

Minor (optional): RA5 publish() 0o400 reuse question in Step 2.1; RA6 tag claims that depend on missing §19.6 / earlier brainstorm results; RA7 frontmatter depth vs notes "Standard" (fix to standard); RA8 seed brief line 73 owner decision on `unknown` cited in Step 2.1 instead of asked open.

RA1-RA8 fixed: qa-task-research-alignment-fix.md VERDICT: PASS.

## A.10.5 Qualitative Blocking Findings (operational + sufficiency, both VERDICT: FAIL)

| ID | Source | Severity | Fix |
|----|--------|----------|-----|
| Q1 | operational #1 | CRITICAL | Step 7.1 reflect input: replace `--diff {BASE}..HEAD` with a diff file of the staged package (`git diff --cached HEAD -- <package> ':(exclude)<package>/reflect/' > <package>/reflect/post-input.diff`, mkdir -p first), pass its absolute path; drop BASE; acceptance: diff file non-empty and names only package paths. |
| Q2 | operational #2 | IMPORTANT | Reword the "no push to origin" criterion everywhere (Key Constraints, Steps 2.4/2.5 acceptance, Gate 1 rf-qa prompt): forbidden = push to the IronClaude repo's remote or any network URL; a sandbox remote named origin is allowed only if its URL is the local bare path under the recorded sandbox path. |
| Q3 | sufficiency #1 | IMPORTANT | Add a sub-question (a)-(f) coverage check, sub-part by sub-part, to Step 6.9 validation (or anti-omission-agent-2); add e/f to the Gate 1 coverage note or point to the Step 6.9 check. |

Minor to apply (cheap): operational #3 + sufficiency M2 (check every `*SANDBOX_PATH:` line incl. FOLLOWUP and web-02 at Step 7.3), operational #4 (`init.defaultBranch=main`), operational #5 (reviews/ wording), operational #6 (S10 QA list wording), `--untracked-files=all` for the git status baseline/compare, sufficiency M3 (reword final-state lens claim to name the 3 lenses).

## Minor Findings (notes, not required)

B2#11-16 and S#7-14: phase-outputs/ path for user summary (fix with C10 if convenient: write to `reviews/user-summary.md`), Phase N Findings template location, unverifiable "only report changed" checks, /tmp glob breadth (record exact mktemp path), deprecated bypassPermissions parameter, line 1311 vs 1312 citation, `tracks` frontmatter, web files gate, XL item justification, file:line in items 189/190/195/269, `--diff` vs staged files, unchecking rule.
