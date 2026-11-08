# QA Report — Task File Qualitative Review (operational lens)

**Topic:** git pre-push hook semantics for the L2 launch-level guard (issue #441)
**Date:** 2026-11-08
**Phase:** task-qualitative
**Lens:** operational (will each item actually succeed if executed)
**Fix cycle:** N/A
**fix_authorization:** false (report only)
**Task file:** .dev/tasks/to-do/TASK-RESEARCH-pre-push-guard-20261108-095046/TASK-RESEARCH-pre-push-guard-20261108-095046.md

**Drift baseline (BUILD_REQUEST.GOAL verbatim, BUILD-REQUEST.md line 12):**
> Conduct a technical investigation on the exact semantics of git's pre-push hook (stdin records for every push form, arguments, empty stdin; bypass paths; hook lookup in linked worktrees incl. core.hooksPath, rev-parse --git-path, extensions.worktreeConfig; hook process ancestry and environment; Linux no-replace atomic publication and the executable bit; the git version that introduced each behaviour and the installed git 2.47.3) as they bear on an L2 guard that refuses a governed AI agent's push to refs/heads/main or refs/heads/master, and produce a structured research report with findings, gap analysis, options, and implementation recommendations. The report will be written to `.dev/tasks/to-do/TASK-RESEARCH-pre-push-guard-20261108-095046/RESEARCH-REPORT-pre-push-guard.md`.

---

(Findings appended incrementally below.)

## Overall Verdict: FAIL

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | AX-3 | FAIL | Step 7.1 (L305) computes `BASE = git merge-base HEAD master`. Dry-run in this worktree: `git merge-base HEAD master` = `80f361804b15...`, `git rev-parse HEAD` = `5dc29d23...`, `git rev-parse origin/master` = `5dc29d23...` (local `master` is 28 commits stale). `git diff --stat 80f3618..HEAD` = "3518 files changed, 471748 insertions(+), 536 deletions(-)", all of it unrelated merged history (#404..#451). The task package is never committed (the task forbids committing). `git add .dev/tasks` only puts it in the index, and `git diff A..B` does not read the index. The reflect run therefore audits 3518 unrelated files and sees none of the deliverables. See Issue 1. The other gates dry-run clean: the `wc -l` counts (747/566), `git --version` = 2.47.3, `git status --porcelain` (3 untracked dirs, recordable as the baseline), `ls -d` of the Q-artifact dir (absent, as Step 2.3 expects), `ps`/`jq`/`timeout` present, and the sandbox probe below. |
| 2 | Project convention compliance | none | PASS | No item edits `src/` or `.claude/`. Every agent prompt carries the SAFETY block. Step 7.1 stages only `.dev/tasks` and says "never stage any `.claude/` path", which matches the CLAUDE.md `.dev/tasks` always-staged rule. No PR, push or gh call appears anywhere. Python goes through `uv run` only. |
| 3 | Intra-phase execution order | none | PASS | Step 1.2 records BASELINE-PORCELAIN before the first porcelain comparison (Step 3.2). Step 2.5 runs after 2.3 and 2.4 (L170) and consumes 2.3's `UNVERIFIED-GIT D19-n` lines (L179/L185). Step 3.4 consumes the Step 2.5 `ROUTE web-01:` lines. Phase 4 waits for Gate 1 PASS (L210). Step 5.4 runs after 5.1-5.3. The subfolders `qa/ research/ reviews/ synthesis/` already exist (`ls -la` of the task dir). |
| 4 | Value/signature verification (doc adaptation) | none | PASS | Every cited value Read or grepped against source. launch-job-identity.sh: 566 lines; `store()` L102; `publish` L164, temp name `'.' + uuid` L165, `fchmod 0o400` L171, `os.link` no-replace L172; `proc` L202 (sid = field 3 of `/proc/<pid>/stat`); `identify` L215, FileNotFoundError -> ordinary L224; `supervise` L291, `os.setsid()` L292; early exit 0 at L20-24; wrapper exits 2 without uv (L25-53). launch-level-guard.sh: 747 lines; LL-PROTECTED refusal text L58-61; push regex L528; hookspath/alias/pushurl/insteadof regex L532; canonical push regex L661. Design doc: §19 L489-578 (file ends at 578); 19.2 install/no-replace L512; L524; L534; 19.6 L536-545; Q paths L540-543. orca_worktree.py: REMEDY L778, `W-L2-ABSENT` L789, `L2_ABSENT_WHY` L796, `l2_status` L1012-1029 (`rev-parse --git-path hooks/pre-push`), use L1312. seed-brief.md L73 is the owner decision on unknown identity. |
| 5 | Module context analysis | none | PASS | Read `identify` -> `proc` -> `store`/`subdir`/`read_file`. The selector keys on the kernel session id of the PID it is given, and `supervise` calls `setsid()` (L292). So "what PID would a hook pass and what is its sid" is the right question, and Step 2.1 and Step 2.4 (the `ps -o pid,ppid,sid` log) both ask it. `publish` writes a 0o400 file, so the RA5 question in Step 2.1 (can it be reused for an executable hook) is grounded in the real module. No sibling disagreement on the input shape: `l2_status` and the design both resolve through `rev-parse --git-path`. |
| 6 | Downstream consumer analysis | none | PASS | Producer/consumer paths match. Gate 1: `qa-research-fix-log.md` and `qa-research-fix-verification[-qualitative]-cycle<n>.md`. Gate 2: `qa-synthesis-fix-log.md`. Gate 3: `qa-fix-log.md` and `qa-fix-verification[-qualitative]-cycle<n>.md`. Gate 4: `qa-fidelity-fix-log.md`. Gate 5: `qa-anti-omission-fix-log.md`. Step 7.2 reads exactly the Gate 4 and Gate 5 logs, validation `## Fixes` and the reflect remediations. `gaps-and-questions.md` (Step 3.4) is consumed by Phase 4 and the anti-omission-2 partition. |
| 7 | Verification-step validity | AX-2 | FAIL | The safety acceptance criterion "no push targeted origin or a network URL" (L182, L185) and the Gate 1 rule "any sign of a push to origin ... is CRITICAL" (L193) contradict the commands the same items prescribe: `git -C $SANDBOX/wt push origin`, `remote.origin.push`, `origin/main`, `git push origin feature:refs/heads/side HEAD:main` (L176, L182). The sandbox probe confirmed that `git clone <bare>` names the local bare remote `origin` (`origin /tmp/qa-op-probe.Zt6h79b6/r.git`). Read literally, the criterion always fails. Read loosely, it is a rubber stamp. See Issue 2. |
| 8 | Coverage of the primary use case | none | PASS | Sub-questions a-f each have an owning item with an acceptance criterion: a/b/c/d in Step 2.4 (stdin forms, SHA-256, bypasses, hook lookup, ancestry, env); identity in Step 2.1; L1 coverage in Step 2.2; e/f in web-01 and web-02 (Phase 4). The report sections are mapped S1-S10 across synth-01..04. |
| 9 | Error-path coverage | none | PASS | Every spawn item has a "log the blocker in Phase N Findings" fallback. Gates have the monotonicity/regression HALT and the 2-cycle cap. Step 7.1 has MALFORMED re-spawn x2 then Blocked. Step 7.2 has a FAIL -> Blocked stop. Step 7.3 has violation -> Blocked, never revert. |
| 10 | Runtime failure-path trace | AX-3 | FAIL | Path: research (Ph2) -> Gate 1 -> web (Ph4) -> synth + Gate 2 -> assembly + Gates 3/4/5 + validation -> reflect (7.1) -> lens re-check (7.2) -> safety (7.3) -> summary (7.4) -> Done. It breaks at 7.1, the reflect input diff (Issue 1). The Tier-2 expectation itself holds: sc-reflect-protocol SKILL.md §5.1 L365 says "`--depth deep` | ALWAYS escalate to T2", and no `--budget-remaining` is passed, so the "tier below Tier 2 is MALFORMED" rule is reachable and is not a defect. |
| 11 | Completion-scope honesty | none | PASS | The absent Q artifacts are handled honestly: Step 2.3 Globs them and tags the dependent claims `[UNVERIFIED: source artifact absent from checkout]`, and `ls -d` confirms the directory is absent. The unknown-identity decision is recorded as DECIDED (seed-brief L73) rather than left open. Design git claims stay UNVERIFIED until 2.4, 2.5 or web-01 settle them. |
| 12 | Ambient dependency completeness | none | PASS | Every recorded value has a consumer: SANDBOX_PATH, FOLLOWUP_SANDBOX_PATH, BASELINE-PORCELAIN, the gate PASS/FAIL sets, `reflect_post`, completion_date and status. Note only (MINOR, Issue 3): Step 7.3(a) re-checks only `SANDBOX_PATH`, not `FOLLOWUP_SANDBOX_PATH` or a sandbox created by a Gate 1 fix agent. Step 2.5 verifies its own path is gone, so this is not blocking. |
| 13 | Dependent-edit sequencing | none | PASS | Values are produced before they are consumed: SANDBOX_PATH (2.4) before 7.3; BASELINE (1.2) before 3.2/5.x/6.x/7.3; the Gate 3 PASS boundary before the 7.2 change list; `reflect_post` (7.1) before 7.2 reads its remediations. Status: Doing (1.1) -> Done (last Post-Completion item). |
| 14 | Existence claims verified | none | PASS | "install_hooks.py has no git-hook path": grep for `pre-push|hooksPath|core.hooks|.git/hooks` returned NO_MATCH, consistent with U28 being an open install-place question. "Q artifacts absent": confirmed. "research/ holds only research-notes.md": confirmed (`Status: Complete` L7, depth Standard L5). `ps` is `/usr/bin/ps`. `uv` is `/usr/local/bin/uv`, so the PATH built from `dirname $(command -v git)` (`/usr/bin`) plus `/usr/bin:/bin` really removes uv: the probe printed `UV-ABSENT`. |
| 15 | Template cross-references | none | PASS | tech-research SKILL.md has: Lens-Specific QA Agent Prompt Template L1042; Report Structure L1311 (S1 "Problem Statement" onward); Synthesis Mapping Table L1491; Validation Checklist L1548; QA Intensity Adaptation "standard" row L641-646 (Gate 3 = 3 rf-qa + 3 rf-qa-qualitative + finding-reproducibility = 7; intermediate gates 3; fidelity 2; max 2 cycles). These match L115, L256-265, L276-285 and BUILD-REQUEST L39-43. |

**Sandbox probe (this review):** `mktemp -d /tmp/qa-op-probe.XXXXXXXX` -> `/tmp/qa-op-probe.Zt6h79b6`. With `HOME=$S/home GIT_CONFIG_NOSYSTEM=1`, `git init --bare` + `git clone` + an empty commit gave `git branch --show-current` = `master` (not `main`) and `git remote -v` = `origin /tmp/qa-op-probe.Zt6h79b6/r.git`. `env -i PATH=/usr/bin:/usr/bin:/bin sh -c 'command -v uv || echo UV-ABSENT'` printed `UV-ABSENT`. No push was run. The directory was removed by the trap, and `ls -d` reported "No such file or directory".

## Summary

- Checks passed: 12 / 15
- Checks failed: 3 (#1, #7, #10; #1 and #10 are the same root defect)
- Critical issues: 1
- Important issues: 1
- Minor issues (notes): 4
- Issues fixed in-place: 0 (fix_authorization: false)
- Drift axis: active (the GOAL is quoted verbatim above). The task matches the GOAL's scope: every GOAL clause maps to an item, and no item narrows a GOAL verb.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | Step 7.1, L305 (`BASE` = `git merge-base HEAD master`; `--diff {BASE}..HEAD`; "run `git add .dev/tasks` first so the task package ... is visible to the diff") | **The reflect gate audits the wrong change set and never sees the deliverables.** (a) The local `master` is stale: merge-base = `80f36180`, while HEAD = origin/master = `5dc29d23`. So `BASE..HEAD` spans 28 merged unrelated commits: "3518 files changed, 471748 insertions(+)". (b) The task package is never committed, and a `A..B` commit range ignores the index, so staging does not make it "visible to the diff". If `master` were up to date, `BASE..HEAD` would be empty instead. Either way, the deviation audit of the research output (reflect `S_scope`, hunk mapping, Regression/Drift classification) runs on the wrong input. The run is likely to be costly or to time out, and any verdict it records is meaningless for this task. | Replace the ref-range input with a diff file of the staged package. After `git add .dev/tasks`, run `git -C /home/coder/workspaces/worktrees/IronClaude/issue-441 diff --cached HEAD -- .dev/tasks/to-do/TASK-RESEARCH-pre-push-guard-20261108-095046/ ':(exclude).dev/tasks/to-do/TASK-RESEARCH-pre-push-guard-20261108-095046/reflect/' > /home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-RESEARCH-pre-push-guard-20261108-095046/reflect/post-input.diff` (mkdir -p `reflect/` first). Pass `--diff <that absolute path>` (sc-reflect-protocol SKILL.md L80: "`--diff <ref-or-path>` — git ref ... or path to a diff file"). Drop the `BASE` computation, or, if a ref is still wanted, use `git merge-base HEAD origin/master`. Add an acceptance check that the diff file is non-empty and names only package paths. |
| 2 | IMPORTANT | L114 (Key Constraints "never `git push` to origin"); Step 2.4 L182 acceptance criteria and Step 2.5 L185 ("no push targeted origin or a network URL"); Gate 1 rf-qa prompt L193 ("any sign of a push to origin ... is CRITICAL") | **Contradiction between the safety criterion and the prescribed experiments.** The same items order `git -C $SANDBOX/wt push origin`, `remote.origin.push ...`, `--set-upstream-to=origin/main` and `git push origin feature:refs/heads/side HEAD:main` (L176, L182). In the sandbox clone, `origin` is the local bare repo (probe: `origin /tmp/qa-op-probe.Zt6h79b6/r.git`). An executor or the Gate 1 rf-qa reading literally must FAIL a correct file 04 as CRITICAL, which can burn the Gate 1 fix cycles or trip `[HALT-MONOTONICITY]`. Reading loosely makes the safety check unobservable. | Reword all four places to name the real thing being forbidden: "never push to the IronClaude repository's remote (`git -C /home/coder/workspaces/worktrees/IronClaude/issue-441 remote get-url origin`, IronbellyOrg/IronClaude) or to any network URL. In the sandbox, a remote named `origin` is allowed only when `git -C $SANDBOX/clone remote -v` shows its URL is the local bare path under the recorded SANDBOX_PATH." Make the L193 CRITICAL rule "any push whose recorded remote URL is not a path under the recorded sandbox". |
| 3 | MINOR | Step 7.3(a), L311 | Only `SANDBOX_PATH:` is re-checked at the end. `FOLLOWUP_SANDBOX_PATH:` (Step 2.5) and any sandbox a Gate 1 fix agent creates (L198 lets it run experiments) are not. Step 2.5 already verifies its own path is gone, so the residual risk is the fix-agent sandbox only. | Extend (a) to every `*SANDBOX_PATH:` line in Phase 2/3 Findings and in `qa/qa-research-fix-log.md`, using the same exact-path `ls -d` and `/tmp/` prefix guard. |
| 4 | MINOR | Step 2.4, L182 ("a clone with an initial commit on main") | Under the prescribed isolated `HOME` + `GIT_CONFIG_NOSYSTEM=1`, git 2.47.3 names the first branch `master` (probe). That makes every `HEAD:main` / `origin/main` form depend on the agent noticing and creating `main` itself. | Say "`git -c init.defaultBranch=main init --bare ...` and `git -C $SANDBOX/clone switch -c main` before the initial commit, then `git push origin main` so `origin/main` exists". |
| 5 | MINOR | L125 (handoff layout: `reviews/` "reserved (unused unless a gate needs a scratch review)") vs Step 7.4, L314 (writes `reviews/user-summary.md`) | Wording inconsistency. The folder exists, so execution is unaffected. | Change L125 to "holds `user-summary.md` (Step 7.4); otherwise reserved". |
| 6 | MINOR | Step 5.4 synth-04 Evidence Trail ("every file under qa/ at the time of writing") | S10 goes stale once Gates 2-5, validation and reflect add QA files. No later item refreshes S10's QA list. | Let Step 6.9 or Step 7.2 append the final qa/ inventory to S10, or reword S10 to "QA reports: see qa/ (final list in Task Log)". |

Additional MINOR note, which is not a task defect: the Step 2.1 L173 `git status --porcelain` baseline shows the untracked directories `.dev/brainstorms/20261108-094705-l2-pre-push-guard/`, `.dev/issues/441/` and the task package as single lines each. A stray file written inside one of them would therefore not change the porcelain output. Using `git status --porcelain --untracked-files=all` for both the baseline and the Step 7.3 comparison would make the check line-exact.

Issue 2 traces back to its upstream source. BUILD-REQUEST.md L26 says "Never run git push against any real remote (no origin, no network URL)". There "origin" means the real checkout's remote, because the same line limits experiments to "a local bare repository as the remote". The task copied the parenthetical but dropped its qualifier "real", and that is how the contradiction arises.

## Actions Taken

- None. fix_authorization is false, so this review only reports. No file except this report was edited. The only experiment was the sandbox probe described above: it used a `mktemp -d` directory under /tmp, made no push, and the directory was removed afterwards.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)

- Inherited FAIL rows (B2-1, B2-2, B2-3, B2-5, B2-6, B2-8, S-3, S-4, S-5, S-9, TB-Add-5, TB-Add-8) are reported as fixed and verified. I spot-checked their effects in the current task file: Step 2.1 L173 has the baseline, sandbox and clean-up text, and the Phase 6 gate items carry their embedded prompts. None of these rows reopened as a structural defect. Issue 1 is a new operational defect in Step 7.1, which is not one of the inherited rows.
- RA1-RA8 were inherited as fixed but not re-verified. I confirmed each one is present:
  - RA1 at L213 ("Pushes via other tools").
  - RA2, RA5 and RA8 at Step 2.1 L173.
  - RA3 at L179 and L182 (push.default=upstream, non-fast-forward, UNVERIFIED-GIT D19-).
  - RA4 at L229 ("Design 19.2 compliance").
  - RA6 at L179 ("source artifact absent").
  - RA7 at frontmatter L22 (the depth comment).
  - The fix log `qa/qa-task-research-alignment-fix.md` exists.
  - All eight are closed.
- Relied on rf-qa PASS for B2-4, B2-7, S-1, S-2, S-6, S-7, S-8, TB-Add-1, TB-Add-3, TB-Add-4, TB-Add-6 and TB-Add-7. For each one I checked its meaning rather than repeating the structural check (see Self-Audit (b)).

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- Relied on rf-qa PASS for B2-4, B2-7 (item self-containment and embedded prompts).
- Relied on rf-qa PASS for S-1, S-2, S-6, S-7, S-8 (structure, frontmatter, phase layout).
- Relied on rf-qa PASS for TB-Add-1, TB-Add-3, TB-Add-4, TB-Add-6, TB-Add-7 (task-builder structural additions).
- Relied on rf-qa for the fixed-and-verified FAIL rows B2-1, B2-2, B2-3, B2-5, B2-6, B2-8, S-3, S-4, S-5, S-9, TB-Add-5 and TB-Add-8. I spot-checked these but did not repeat the structural checks.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Step 7.1 reflect input dry-run:
  - `git merge-base HEAD master` printed `80f36180`; HEAD and origin/master are both `5dc29d23`.
  - `git diff --stat 80f36180..HEAD | tail -1` printed "3518 files changed, 471748 insertions(+), 536 deletions(-)".
  - `git status --porcelain` showed the task package as untracked, so a commit range cannot include it.
  - rf-qa's structural PASS on Phase 7 could not detect this. It produced Issue 1.
- Sandbox probe under /tmp, with isolated HOME and GIT_CONFIG_NOSYSTEM=1, on git 2.47.3:
  - `git init --bare` followed by a clone set the clone's `origin` to the local bare path, and the default branch was `master`.
  - The probe made no push and was cleaned up.
  - It produced Issue 2 and MINOR 4.
- Reflect tier semantics: sc-reflect-protocol SKILL.md §5.1 L365 says `--depth deep` always escalates to T2, so the task's Tier 2 requirement holds. I checked this and found no defect.
- `--diff` input contract: sc-reflect-protocol SKILL.md L80 accepts a git ref or a diff-file path. This confirms that the fix for Issue 1 can be carried out.
- Citation reads against the target files:
  - launch-job-identity.sh: publish L164-172 (O_EXCL tmp, fchmod 0o400, os.link), proc L202, identify L215/L224, supervise L291-292, the uv-absent path L25-53.
  - launch-level-guard.sh: L58-61, L528, L532, L661.
  - orca_worktree.py: REMEDY L778, W-L2-ABSENT L789, L2_ABSENT_WHY L796, l2_status L1012-1029, the cmd_launch use at L1312.
  - install_hooks.py: no pre-push or hooksPath match.
  - Design doc §19: L489-578, with subsections 19.1-19.8 at the cited lines.
  - All of these match what the task items claim.
- Owner decisions: seed-brief.md L73-L77 (unknown identity, B-CTX scope, IR-7 default off) match the task's constraints, so the task contains no contrary instruction.
- Gate counts: the task's gate structure (3/3/7/2/2 agents, each capped at 2 fix cycles) matches BUILD-REQUEST L39-43 and the tech-research SKILL.md QA Intensity standard row (L641-646).

**Self-audit questions:**
1. Claims verified independently against source: about 45 (file:line citations, git state, git default behaviour, reflect contract lines, gate counts, RA1-RA8 presence).
2. Files read:
   - The task file, BUILD-REQUEST.md, seed-brief.md and research-notes.md.
   - The design doc §19, launch-job-identity.sh, launch-level-guard.sh, orca_worktree.py and install_hooks.py.
   - tech-research SKILL.md, sc-reflect-protocol SKILL.md and qa/qa-task-research-alignment-fix.md.
3. The review found 1 CRITICAL issue, 1 IMPORTANT issue and 4 MINOR notes, not zero. Each finding has command or line evidence above.
4. No web research was performed, so Tavily was not used and nothing fell back to another tool.

**Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 15 | Grep: 3 | Glob: 3 | Bash: 8 (rg EACCES on the guard script fell back to bounded sed output inside the batch script; tavily: 0 attempts, not needed)

## Recommendations

1. Before the task runs, fix Issue 1 (CRITICAL): make Step 7.1 feed reflect a `--diff` file built from `git diff --cached HEAD -- <task package> ':(exclude)<task package>/reflect/'`, and add a check that the file is non-empty and scoped to the package. Otherwise the final deviation audit is either meaningless or impossible to run.
2. Fix Issue 2 (IMPORTANT): reword L114, L182, L185 and L193 so the forbidden target is the real checkout's IronbellyOrg/IronClaude remote or any network URL. A sandbox `origin` must be allowed when its URL is a path inside the recorded sandbox. This stops Gate 1 from failing a correct file 04.
3. Optional: apply MINOR 3-6 and the porcelain note (`--untracked-files=all`) in the same edit pass. None of them blocks execution.
4. Re-run this operational review after the fixes. That is fix cycle 1 of 2.

## QA Complete

VERDICT: FAIL
