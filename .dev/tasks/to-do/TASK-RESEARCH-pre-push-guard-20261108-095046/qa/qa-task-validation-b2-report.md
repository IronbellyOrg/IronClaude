# QA Report — Task Integrity (Lens: B2 Self-Containment)

**Topic:** git pre-push hook semantics for the L2 launch-level guard (issue #441)
**Date:** 2026-11-08
**Phase:** task-integrity
**Lens:** b2-self-containment
**Fix cycle:** N/A
**Fix authorization:** false (report only; task file not edited)
**Task file:** /home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-RESEARCH-pre-push-guard-20261108-095046/TASK-RESEARCH-pre-push-guard-20261108-095046.md

---

## Overall Verdict: FAIL

Scope read: the full task file (409 lines, 60 `- [ ]` items), BUILD-REQUEST.md safety lines 24-28, and the cited source lines in `launch-job-identity.sh`, `launch-level-guard.sh`, `orca_worktree.py` and the design doc.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Every item has context + action + output + verification + completion gate | FAIL | Most items carry all five parts (for example Steps 1.1, 2.1-2.4, 4.1, 4.2, 5.1-5.4, 6.1, 6.5). The seven Step 6.2 items (lines 252-258) and Step 6.7 item 2 (line 280) do not hold their own full action, the prompt. See issues 1 and 2. |
| 2 | No item relies on a prior item's context without restating it | FAIL | Lines 252-258 say "passing it the Step 6.2 header ... then the Step 6.2 output format". Line 280 says "passing it the same complete prompt as anti-omission-agent-1 with only these values changed". Every item points to "the templated format in the ### Phase N Findings section", but that template exists only as a comment under ### Phase 1 Findings (lines 347-360). |
| 3 | Agent-spawning items embed the full prompt | FAIL | Step 6.2 (7 items) and Step 6.7 item 2 do not, as above. The Step 3.2 fix item (line 195) lets the fix agent spawn rf-task-researcher agents with a prompt it writes itself; that nested prompt is not embedded and is not required to carry the SAFETY block. Line 250 says "Each item below embeds that header ... in full", which the items do not do. |
| 4 | File paths are specific | PASS | Every output path is a full `.dev/tasks/to-do/TASK-RESEARCH-pre-push-guard-20261108-095046/...` path. The cited source files exist with the claimed sizes (566 / 747 / 578 / 611 lines). `~/.claude/skills/tech-research/SKILL.md`, the template 02 file and the research, synthesis, qa and reviews subfolders exist. Step 7.1's `phase-outputs/` path is a minor inconsistency (issue 13). |
| 5 | Verification criteria are measurable | FAIL | Most are measurable (Status: Complete, named sections, `Blocking count: <n>`, `ls -d ... \|\| echo NONE`). Exceptions: `git status --porcelain -- src docs` (lines 195 and 314) is used to prove that no source file was edited, but it misses `tests/`, `scripts/`, `plugins/`, `Makefile`, `pyproject.toml`, `.claude/settings.json` and the root `CLAUDE.md` (issue 8). Several "only the report and fix log changed" gates give no way to check it (issue 14). |
| 6 | No batch items: each file or component has its own item | FAIL | Step 5.5 (line 231) spawns 3 agents with 3 output files in one item, although Step 3.1 splits the same pattern into 3 items. Step 6.9 (line 289) runs three validations, a conditional fix agent and a re-run in one item. The verifier items in 3.3, 5.7, 6.4, 6.6 and 6.8 each spawn 2 agents. See issues 9 and 11. |
| 7 | No item is built on a [CODE-CONTRADICTED] or [UNVERIFIED] finding | PASS | Cited facts match the code. In launch-job-identity.sh: `publish` at 164 (O_EXCL at 166, `os.link` at 172), `proc` at 202, `identify` at 215, `os.setsid()` at 292. In launch-level-guard.sh: the push regexes at 528, 532 and 661, and the main/master refusal text at 59; Grep for `\.git/hooks` found nothing, which confirms the "no hooks token" claim. In orca_worktree.py: `"W-L2-ABSENT"` at 789, `L2_ABSENT_WHY` at 796, `l2_status` at 1012 and its call at 1311. The design doc's section 19 heading is at 489. The version hints in Step 4.1 are labelled unconfirmed and are not used as fact. |
| 8 | Safety constraints are written into every item that runs commands | FAIL | BUILD-REQUEST.md line 24 requires the safety block in every relevant item. The full four-part block is in 2.1-2.4, the 3.2 fix item, 4.1 and 4.2. It is missing from every gate and verifier prompt given to a Bash-capable agent (3.1 x3, 3.3, 5.5 x3, 5.7, 6.2 x7, 6.4, 6.6, 6.7 x2, 6.8). It is partial in the Phase 5 synthesis prompts and the 5.6, 6.3, 6.5, 6.6, 6.8 and 6.9 fix prompts. It is absent from the Step 7.2 runner prompt (issues 4-7). |

## Summary

- Checks passed: 2 / 8
- Checks failed: 6
- Critical issues: 1
- Important issues: 9
- Minor issues: 6
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | Step 6.2, all 7 lens items (lines 252-258); claim at line 250 | The items say "passing it the Step 6.2 header ... then the Step 6.2 output format", but the header and output format are defined only in the prose paragraph at line 250, outside every item. Line 250 claims each item embeds them "in full"; none does. An executor working one item at a time gets a prompt with no header and no output format. | Copy the full header text, the lens-specific instructions, the output format and the SAFETY block into each of the 7 items. Remove the false "embeds ... in full" claim or make it true. |
| 2 | IMPORTANT | Step 6.7 item 2 (line 280) | anti-omission-agent-2 is given "the same complete prompt as anti-omission-agent-1 with only these values changed". The item depends on the previous one. | Write out agent-2's complete prompt in its own item. |
| 3 | IMPORTANT | Step 3.2 fix item (line 195) | The fix agent may spawn nested rf-task-researcher agents that rerun sandbox experiments. Their prompt is not embedded, and nothing requires it to carry the SAFETY block. Only the fix agent itself gets the constraints. | Embed the nested researcher prompt with the full SAFETY block, or forbid nested spawns and make the fix agent do the gap research itself under its own SAFETY block. |
| 4 | IMPORTANT | Steps 3.1 (x3), 3.3, 5.5 (x3), 5.7, 6.2 (x7), 6.4, 6.6, 6.7 (x2), 6.8 gate and verifier prompts | These agents (rf-qa, rf-analyst, rf-qa-qualitative) can run Bash, but their prompts carry no safety constraints. The Step 3.1 rf-qa prompt says "Zero tolerance: if you cannot verify it, it fails", which invites rerunning git experiments with no sandbox, push or uv rule. This breaks BUILD-REQUEST.md line 24 ("embed in every relevant item"). | Add the full four-part SAFETY block to every gate and verifier prompt: no source edits; uv only; post nothing; experiments only in a `mktemp -d` /tmp repo with a local bare remote, never a push to a real remote, cleaned up afterwards. |
| 5 | IMPORTANT | Phase 5 synthesis items 5.1-5.4; fix prompts in 5.6, 6.3, 6.6, 6.8, 6.9; fidelity-2 in 6.5 | The safety text is partial: "no source edit, post nothing" only. The uv-only rule and the no-push / /tmp-only rule are dropped. | Replace the partial text with the full four-part SAFETY block. |
| 6 | IMPORTANT | Step 7.2 reflect runner | The verbatim prompt runs `--remediate` in a general-purpose agent with bypassPermissions, but it contains no safety constraints. The "only this task package" scope is written outside the prompt, so the agent never sees it. | Put the scope limit and the full SAFETY block inside the verbatim prompt. |
| 7 | IMPORTANT | Step 2.2 (line 176) | The item lets the agent run the real `launch-level-guard.sh` on literal strings without isolating HOME. The guard reads and writes its store under `$HOME` (`LL_STORE` at line 23; the prompt branch at lines 285-297 creates directories, renames and links files there). In an ungoverned session it exits 0 (line 281), so every string would classify as ALLOWED. The result would be misleading, and the run can change real state. | Require `HOME="$SANDBOX/home"` under a `mktemp -d` directory and a governed test session for each guard run, or forbid running the guard and allow static reading of its regexes only. |
| 8 | IMPORTANT | Step 3.2 verification and Post-Completion item 5 (line 314) | `git status --porcelain -- src docs` is used to prove that "no source or documentation file was edited", but it does not cover `tests/`, `scripts/`, `plugins/`, `Makefile`, `pyproject.toml`, `.claude/settings.json` or the root `CLAUDE.md`. The check proves less than the gate claims. | Use `git status --porcelain` on the whole tree and require that every changed path is under `.dev/tasks/to-do/TASK-RESEARCH-pre-push-guard-20261108-095046/`. |
| 9 | IMPORTANT | Step 5.5 (line 231); Step 6.9 (line 289) | Batch items. 5.5 spawns 3 agents with 3 outputs in one item, although Step 3.1 shows the one-item-per-agent pattern. 6.9 bundles three validations, a conditional fix agent and a re-run. A partial failure cannot be recorded against a single checkbox. | Split 5.5 into 3 items, one per agent and output. Split 6.9 into one item per validation, plus a separate conditional fix item and a re-run item. |
| 10 | IMPORTANT | Step 5.4 and Step 5.3 dependency ordering | 5.4 is spawned in parallel with 5.1-5.3, but its prompt requires listing synth-01..04 and checking with Glob that each exists. Its gate "every listed file exists" cannot hold at spawn time. 5.3 reads synth-01 and synth-02 "if they exist"; with parallel spawning they will not exist yet. | Run 5.4 (and the part of 5.3 that reads synth-01/02) after 5.1-5.3 complete, or remove those cross-file reads from the parallel items. |
| 11 | MINOR | Verifier items 3.3, 5.7, 6.4, 6.6, 6.8; Step 2.4 | The verifier items each spawn 2 agents. Step 2.4 has one agent run about 25 experiments into one file; it has one output and follows the tech-research pattern. | Optionally split the verifier items into one item per agent. |
| 12 | MINOR | Every Phase 2-7 item; Task Log lines 347-372 | Items say "use the templated format in the ### Phase N Findings section", but the template appears only as a comment under Phase 1 Findings (lines 347-360). | Name the Phase 1 template location in each item, or repeat the template in each Phase Findings section. |
| 13 | MINOR | Step 7.1 | It writes `phase-outputs/reports/user-summary.md`, but line 120 says the task uses the tech-research layout "instead of a generic phase-outputs/ tree", and Step 1.2 does not create that folder. | Write the summary inside the task folder's existing layout (for example `reviews/` or the task root). |
| 14 | MINOR | Steps 5.6, 6.3, 6.6, 6.8 verification | "Only the report and fix log changed" gives no way to check it. | Name the check (for example, `git status --porcelain` limited to the task folder, compared before and after). |
| 15 | MINOR | Step 2.4 and Post-Completion leftover check | The glob `/tmp/prepush-research.*` could match sandbox folders from other sessions, which could produce false leftovers or invite deleting another session's directory. | Record the exact `mktemp -d` path in the research file and check that path only. |
| 16 | MINOR | Step 7.2; Step 6.9; Step 2.3; repeat instructions | 7.2 passes the Agent tool's `mode: bypassPermissions` parameter, which is deprecated and ignored. 6.9 says "sampled exhaustively", which contradicts itself. 2.3 cites line 1311 for the `L2_ABSENT_WHY` use, which is at 1312 (the `l2_status` call is at 1311). The repeat instructions ("repeat Steps 3.2-3.3 by unchecking") refer to items by step number only. | Drop the ignored parameter; choose "sampled" or "exhaustive"; cite 1311-1312; name the items to uncheck. |

## Actions Taken

None. fix_authorization is false, and the task file was not edited.

## Confidence

- **Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 11 | Grep: 9 | Glob: 1 | Bash: 3 (no web research)
- No unchecked or unverifiable items.

## Recommendations

- Fix issues 1-10 in the task file before execution. Start with the Step 6.2 prompts and the SAFETY coverage (issues 1 and 4-7); without those, an agent may push to a real remote or change the guard's real store.
- Rerun this B2 lens after the fixes. This was review 1 of at most 3.

## QA Complete

VERDICT: FAIL
