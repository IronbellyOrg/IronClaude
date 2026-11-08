# QA Report: Research Qualitative (research-gate, research-depth lens)

**Topic:** git pre-push hook semantics for the L2 launch-level guard (issue #441)
**Date:** 2026-11-08
**Phase:** report-qualitative, adapted to research files (research-gate)
**Fix cycle:** N/A (first review; fix authorization false, report only)
**Files reviewed:** research/01-identity-selector-ancestry.md, research/02-l1-guard-push-bypass-coverage.md, research/03-design-and-claim-code-crossvalidation.md, research/04-empirical-git-prepush-experiments.md; research-notes.md for the planned scope
**Inherited Structural Verdict:** none supplied, so this is a standalone review

---

## Overall Verdict: FAIL

One IMPORTANT finding (F1) blocks the gate. The other findings are MINOR notes.

## Items Reviewed

| # | Check (adapted to research files) | Result | Evidence |
|---|---|---|---|
| 1 | Problem statement matches findings: do the four files answer the planned sub-questions (research-notes.md lines 9, 66-70)? | PASS | Each sub-question has an answer. (a) stdin and argv for every push form: 04 E1-E11, E20-E26; the Summary is at line 2259. Empty stdin: E12/E12b. Dry run: E13/E13b. (b) What skips the hook: E14 `--no-verify`, E15/E16 `-c core.hooksPath`, E17a-c send-pack (E17c rewrote main with no hook run), E29 non-executable hook. (c) Linked-worktree lookup: E30 (the common-dir hook runs and the private-dir copy is ignored), E31 worktreeConfig. (d) Ancestry and environment: E18 (same SID, GIT_DIR set only from the worktree), E28. 01 covers identify, setsid and the PID to pass. 02 covers L1 coverage. 03 covers the design claims. Sub-questions (e) and (f) are planned for web-01/web-02, which are outside this gate. |
| 2 | Current state is current: are the code paths described those that exist now? | PASS | Re-read: launch-job-identity.sh lines 20-25 (the hook-mode early exit, then `command -v uv`), 102-122 (store, the 0o022 check at line 109), 164-174 (publish), 202-207 (proc), 215-239 (identify), 291-293 (setsid), 525-566 (main and `exec uv`). orca_worktree.py lines 789-799 and 1012-1029 (l2_status), plus line 1311 (the call site). launch-level-guard.sh lines 528, 532, 661-667 and 706. Every citation checked in 01, 02 and 03 matches. |
| 3 | Options are genuinely distinct (placement and publication) | PASS | 01 (lines 220-258) contrasts link(2) no-replace publication with rename(2), which replaces. 04 E30/E31 separates three placements: the common-dir hook, a per-process hooksPath and a per-worktree hooksPath. 04 line 2245 offers pure shell or uv. These are distinct mechanisms, not variations of one. |
| 4 | Conclusions follow from the analysis | FAIL (F1) | 01 section 4 item 3 (line 192) maps "no verdict" (uv absent, exit 2) to unknown, which refuses main/master. Item 5 (line 194), however, omits humans without uv on PATH from the human side effects. 04 line 1530 and line 2245 propose "call uv by absolute path" as the fail-closed remedy. That remedy cannot work as written: the identity script itself resolves uv through PATH (launch-job-identity.sh line 25 `command -v uv`, line 566 `exec uv run ...`). |
| 5 | Findings are actionable for a spec | PASS with F1 caveat | A spec can cite: exact field-3 comparison against `refs/heads/main`/`master` (04 line 2259); one nonzero exit aborts the whole push (E19); bypasses that need install-integrity checks (lines 2244 and 2259); which PID to pass to identify and the setsid residual (01 lines 119-129 and 193); the no-replace install pattern (01 lines 220-258). The one gap that is not actionable is the uv/PATH failure mode (F1). |
| 6 | Gaps are honest | PASS with MINOR notes | 02 is labelled static only (line 8), and its gaps are tagged UNVERIFIED (lines 264-271). 04 Gaps (lines 2233-2250) tag their items. 01 tags the container/PID namespace as UNVERIFIED (lines 210-212) and the PID-reuse case as inferred (line 165). Notes: 04 lines 2241-2242 are stale against line 2248 (F3), and 02 Gap 9 (line 267) says "probably", although a local check was possible (F7). |
| 7 | External research is relevant (adapted: are doc citations traceable?) | PASS with MINOR note | 02 line 141 cites the git-push docs as "fetched 2026-11-08" but names no tool or URL (F7). The claim is corroborated empirically by 04 E20. The other git-behaviour claims rest on sandbox commands with their output shown. |
| 8 | Scale claims are substantiated (adapted: are performance and volume assumptions about the hook tested?) | PASS (after my own check) | No file tested a hook that exits without reading stdin, while many refs are pushed (a possible SIGPIPE concern for a guard that exits early). I ran this check myself (see Self-Audit): on git 2.47.3, 3000 refs pushed with a hook that never reads stdin gave push exit 0 and 3001 remote branches. Recorded as MINOR note F8, so the spec can cite it. |
| 9 | Risk assessment is complete | FAIL (F1) | Install-integrity risks are covered: chmod -x fail-open (E29, plus 02 lines 156-160, where L1 allows it), worktreeConfig (E31), send-pack (E17). Human-impact risk is incomplete: 01 line 194 omits humans whose PATH lacks uv (F1). |
| 10 | Evidence trail is complete | PASS with MINOR notes | Experiments show their commands and outputs, and both sandbox removals are recorded (04 lines 1701-1712 and 2217-2229). Two cross-references are wrong: 04 line 1530 cites "(E9-E11)" for refusal, but E9-E11 are --all/--tags/--mirror (line 551) and refusal is E19 (line 1029); 04 line 1699 cites "E7/E8 (per-process `-c core.hooksPath`)", but E7/E8 are refspec experiments (line 453) and hooksPath is E15/E16 (line 855) (F4). 01 line 142 names uv 0.11.8 with no command shown (F6). |
| 11 | No circular reasoning | PASS | 04 Step 2.5 (lines 1773-1797) checks 03's 16 UNVERIFIED-GIT claims against new sandbox runs F1-F4; it does not cite 03 as evidence for itself. 01's verdict logic cites source lines, not other research files. |
| 12 | Conclusions are proportionate | PASS with MINOR note | 04 Summary (line 2259) stays inside git 2.47.3 and the local file transport (line 2238). One labelling inconsistency: line 2254 says "None contradicted ... §19.5 line 534" held, while line 2247 tags D19-47 (design line 534) as CODE-CONTRADICTED. Line 2247 explains that the tag applies to 03's paraphrase and that the design sentence is incomplete, so the meaning is reconciled in prose, but the two labels read as contradictory at a glance (F5). |

## Summary

- Checks passed: 10 / 12 (items 4 and 9 fail on the same root finding, F1)
- Checks failed: 2
- Critical issues: 0
- Important issues: 1 (F1)
- Minor issues: 7 (F2-F8)
- Issues fixed in-place: 0 (fix authorization false)

## Issues Found

| # | Severity | File | Finding | Proposed fix |
|---|---|---|---|---|
| F1 | IMPORTANT (blocking) | 01 section 4 item 5 (line 194); 04 lines 1530 and 2245 | **A spec-relevant failure mode is missing, and the proposed remedy does not work.** 01 item 3 (line 192) requires the hook to treat "no verdict" (identify exit 2 because uv is absent, line 53) as `unknown`, which refuses main/master. 04 E28c shows that uv can be absent from the hook's PATH. A human whose push runs with a PATH that lacks uv therefore gets exit 2 and a refused push to main, even when no launch-level store exists. Examples are an IDE or GUI git client, cron, or uv installed only in `~/.local/bin`. The "missing ordinary state needs no uv" early exit (launch-job-identity.sh lines 19-24) applies only to `$# == 0` or `hook`, not to `identify`; line 25 then requires uv. Item 5 lists only HOME unset/relative, a 0775 home and a stale record, so a spec built from it understates the narrowing of the design invariant (design line 493). 04 then offers "call uv by absolute path recorded at install time" as the fail-closed answer (lines 1530 and 2245). That answer is incomplete: the identity script resolves uv itself through PATH (line 25 `command -v uv`, line 566 `exec uv run --no-project python -I ...`), so an absolute path in the hook does not reach the script's own lookup unless the hook also sets PATH. | In 01 item 5, add: "a human whose PATH lacks uv (exit 2, treated as unknown) cannot push to main/master." State the hook-side options a spec can choose from: (i) the hook sets a fixed PATH containing the uv directory recorded at install time before it calls the script; (ii) the hook first applies the same no-store early exit as lines 20-24 (no `$HOME/.claude/state/launch-level` gives ordinary, with no uv needed); (iii) a pure-shell hook. In 04 lines 1530 and 2245, correct the remedy to say that an absolute uv path alone is insufficient because of script lines 25 and 566. Optionally confirm (i) or (ii) with one sandbox run that pushes with `PATH=/usr/bin:/bin` and no store. |
| F2 | MINOR | 01 line 246 | "on the path git will actually run (`git rev-parse --git-path hooks/pre-push`, with `core.hooksPath` unset)" is ambiguous. It can be read as "run rev-parse with hooksPath unset", which would check the wrong file whenever hooksPath is set, since E31 shows git then runs a different file. It can also be read as "this applies when hooksPath is unset". | Reword: "the path `git -C <worktree> rev-parse --git-path hooks/pre-push` prints, which already follows any effective `core.hooksPath`; when hooksPath is set, report it rather than installing." |
| F3 | MINOR | 04 lines 2241-2242 vs 2248 | Two Gaps bullets are stale. They say `refs/heads/ma` was not pushed and worktree removal was not exercised, but line 2248 says Step 2.5 resolved both (F3a, F2). The reader meets UNVERIFIED tags for facts that are verified six lines later. | Delete the two bullets or retag them as RESOLVED with a pointer to F3a and F2. Keep only "Orca's removal path remains untested". |
| F4 | MINOR | 04 lines 1530 and 1699 | Wrong cross-references. Line 1530 cites "(E9-E11)" for "a nonzero exit refuses", but E9-E11 are `--all`/`--tags`/`--mirror` (line 551) and the refusal experiment is E19 (line 1029). Line 1699 cites "E7/E8 (per-process `-c core.hooksPath`)", but E7/E8 are refspec experiments (line 453) and hooksPath is E15/E16 (line 855). | Change "(E9-E11)" to "(E19)" and "E7/E8" to "E15/E16". |
| F5 | MINOR | 04 lines 2246-2247 vs 2254 | Labelling inconsistency. Stale Documentation says "None contradicted ... §19.5 line 534" held, while Gaps tags D19-47 (design line 534) as [CODE-CONTRADICTED]. The prose reconciles them: the tag applies to 03's paraphrase, and the design sentence is incomplete, not wrong. This is graded MINOR rather than as an unresolved contradiction because the meaning is resolved in the file; only the labels clash. | In line 2247, attach the tag to "file 03 paraphrase of D19-47". In line 2254, add "(line 534 is incomplete; see next bullet)". |
| F6 | MINOR | 01 lines 140-142 | Sections are numbered out of order (section 7 placed before sections 4-6, with a note). The uv version "0.11.8" is stated with no command shown, unlike the git version, which research-notes line 16 backs with `git --version`. | Record `uv --version` output in the setup line. Optionally renumber the sections. |
| F7 | MINOR | 02 line 141; 02 line 267 (Gap 9) | The git-push documentation is cited as "fetched 2026-11-08" with no URL or tool. Gap 9 leaves "git probably rejects `refs//heads/main`" speculative, although 02 is static-only by design and 04 could have settled it locally, as F3 did for space and tab names. | Add the URL and tool to line 141. Route Gap 9 to a one-line sandbox check (`git push origin HEAD:refs//heads/main` against a local bare remote), or mark it explicitly as deferred to 04. |
| F8 | MINOR (informational) | 04 (all experiments) | No experiment covers a hook that exits without reading all of stdin when many refs are pushed. This matters for a guard that refuses or allows early, because git could see EPIPE/SIGPIPE while writing records. My own sandbox run (Self-Audit b1) shows that on git 2.47.3 the push succeeds (exit 0, 3001 remote branches). | Record this as an observed fact the spec can cite, or tell the hook to drain stdin before it exits for robustness across git versions. |

## Actions Taken

None. Fix authorization was false. No research or source file was modified; this report is the only file written.

## Confidence

- **Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Every checklist item was checked with tool evidence: Read of all four research files (04 read in full, 2261 lines), research-notes.md, and the cited source lines in launch-job-identity.sh, orca_worktree.py and launch-level-guard.sh; Grep for experiment headings and cross-references; one sandbox Bash experiment.
- Unverifiable items: none at this gate. Web citations (02 line 141) were judged for traceability only, not re-fetched; the claim they support is corroborated by 04 E20.
- **Tool engagement:** Read: 26 | Grep: 11 | Glob: 0 | Bash: 3 | Web: 0 (no external lookup was needed, so Tavily was not called and no fallback occurred)
- The tool-engagement minimum is met: Read + Grep + Glob = 37, which exceeds the 12 checklist items.

## Self-Audit

**(a) Reliance list (rf-qa PASS items skipped for the structural re-check):**
- None. No Inherited Structural Verdict was supplied, so this review ran standalone. It relied on nothing beyond its own re-reading of the research files and source.

**(b) Independent semantic checks (at least one required, INV-019):**
- b1. **Hook that never reads stdin, under a large push.** In `mktemp -d` sandbox `/tmp/qa-prepush.vLbqTW9t`, with HOME inside the sandbox, a local bare remote as the only remote, and 3000 branches created via `git update-ref --stdin`, the hook was `#!/bin/sh` / `exit 0`. `git push -q origin 'refs/heads/*:refs/heads/*'` gave push exit=0 and the remote listed 3001 branches (git 2.47.3). The cleanup trap printed "cleanup ok"; no real remote was touched. This fills a gap none of the four files covered (F8).
- b2. **The uv/PATH failure mode for humans (F1).** Read launch-job-identity.sh lines 16-27 and 566: the early exit at lines 20-24 is gated on `$# == 0` or `hook`; line 25 `command -v uv` then applies to `identify`; line 566 `exec uv run ...` resolves uv through PATH. Compared with 01 line 192 (no verdict maps to unknown) and line 194 (the human side-effect list), the missing case and the flaw in 04's absolute-path remedy (lines 1530 and 2245) follow directly.
- b3. **The 0o022 home check cited in 01 line 194.** Re-read launch-job-identity.sh line 109 in store(): it rejects a group- or other-writable HOME, which confirms the "0775 home" human side effect is real code behaviour, not an inference.
- b4. **Cross-reference audit of 04.** Grep of 04's experiment headings (lines 453, 551, 855, 1029) proved that the references at lines 1530 and 1699 point at the wrong experiments (F4).
- b5. **Gaps freshness.** Read 04 lines 2233-2255: lines 2241-2242 conflict with line 2248 (F3), and line 2254 conflicts in labels with line 2247 (F5).

**Answers to the mandatory self-audit questions:**
1. Claims independently verified against source: about 30 (the citations in item 2, every PID, setsid and publish claim in 01, the regexes and tamper tokens in 02, l2_status and the call site at orca_worktree.py line 1311 for 03, plus the uv lookup lines).
2. Files read: the four research files, research-notes.md, launch-job-identity.sh, orca_worktree.py, launch-level-guard.sh, and tests/skills/test_issue_orca_worktree.py (Grep for the `present-unverified` expectations).
3. Not applicable as a zero-findings defence: eight findings were recorded, one of them blocking.
4. No web research was performed; this is recorded under Tool engagement.

## Recommendations

- Resolve F1 before synthesis: amend 01 item 5 and 04 lines 1530 and 2245 as proposed. Synthesis must then carry the "human without uv on PATH" narrowing, and one of the hook-side options (fixed PATH, no-store early exit, or pure shell), into the spec input.
- Apply MINOR fixes F3 and F4 in the same pass; they are one-line edits and prevent stale or misdirected citations from reaching synthesis.
- F2, F5, F6, F7 and F8 can be handled during synthesis wording; they do not block.
- Re-run this qualitative gate (fix cycle 1) only on F1.

## QA Complete

