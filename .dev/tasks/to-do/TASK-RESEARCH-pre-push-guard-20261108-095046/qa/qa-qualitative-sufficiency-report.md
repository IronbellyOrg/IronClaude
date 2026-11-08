# QA Report — Task Qualitative Review (lens: qa-gate-sufficiency)

**Topic:** pre-push guard research task (issue 441)
**Date:** 2026-11-08
**Phase:** task-qualitative
**Fix cycle:** N/A
**Fix authorization:** false (report only)

---

## Overall Verdict: FAIL

One IMPORTANT (blocking) finding: no QA gate checks the final report against the six GOAL sub-questions (a)-(f). Four MINOR notes.

Drift baseline (AX-1), BUILD-REQUEST.md line 12, verbatim: "Conduct a technical investigation on the exact semantics of git's pre-push hook (stdin records for every push form, arguments, empty stdin; bypass paths; hook lookup in linked worktrees incl. core.hooksPath, rev-parse --git-path, extensions.worktreeConfig; hook process ancestry and environment; Linux no-replace atomic publication and the executable bit; the git version that introduced each behaviour and the installed git 2.47.3) as they bear on an L2 guard that refuses a governed AI agent's push to refs/heads/main or refs/heads/master, and produce a structured research report with findings, gap analysis, options, and implementation recommendations."

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | none | PASS | Gate commands are read-only (`git status --porcelain` whole tree, `git remote -v`, Glob, grep), and their preconditions exist: research/ and qa/ dirs, the `BASELINE-PORCELAIN:` record written in Phase 1, `SANDBOX_PATH:` written at Step 2.4 (L182). Step 7.3 (L311) runs after every producer. |
| 2 | Project convention compliance | none | PASS | No source edits anywhere; every spawn item carries SAFETY (46/46 per verify-cycle1 C4, which I did not recount). Experiments use `mktemp -d /tmp` plus a local bare repo (L182, L185). uv only. Nothing is posted. |
| 3 | Intra-phase execution order | none | PASS | Gate 1 (L192-194) runs after Step 2.5 (L184-185). Web (L213/L216) runs after Step 3.4 routing (L206). Gate 3 (L259-274), then Gate 4 (L277-285), then Gate 5 (L288-296), then validation (L299-300), then 7.1 reflect (L305), 7.2 re-check (L308), 7.3 safety (L311), summary (L314), post-completion (L321-325). Done is last (L325). |
| 4 | Gate agent counts vs expected (adapted from "signature verification") | none | PASS | Gate 1 = 3, Gate 2 = 3 (L235-237), Gate 3 = 7 (L259-265), Gate 4 = 2 rf-qa (L277-278), Gate 5 = 2 rf-analyst (L288-289). These match BUILD-REQUEST L39-43 and the standard row of tech-research SKILL.md (L397-415). The Phase Gate Findings table (L388-394) agrees. |
| 5 | Module context: Gate 3 lens distinctness | none | PASS | The 7 lenses are different: template-conformance, internal-consistency and evidence-quality (rf-qa, L259-261); actionability, domain-accuracy, crossref-chain and finding-reproducibility (rf-qa-qualitative, L262-265). Each has its own checklist and output file; no two lenses check the same question. |
| 6 | Downstream consumer: fidelity sources | none | PASS | Gate 4 checks the report against the real sources: agent-1 (L277) against launch-job-identity.sh, launch-level-guard.sh and research/04 (the /tmp git evidence); agent-2 (L278) against design §19 L489-578, orca_worktree.py, install_hooks.py and web-01/web-02. I confirmed the cited anchors exist (see Self-Audit (b)). |
| 7 | Test validity (verifier substance) | none | PASS | Verifiers are independent of the fixer: Gate 4 uses rf-qa (L283) plus rf-qa-qualitative (L284); Gate 5 uses rf-analyst (L294) plus structural rf-qa (L295, S4/S8/S9/S10 and TOC). Fixers are told not to spawn agents. MINOR note M4 (validation fix self-verified). |
| 8 | Coverage of the primary use case (anti-omission covers sub-questions and every finding) | none | PASS (part) | Every finding: yes. Gate 5 partitions all 10 inputs (L288: 01, 02, 03, synth-01, synth-02; L289: 04, web-01, web-02, gaps-and-questions, synth-03, synth-04), judges by meaning, enumerates exhaustively, and requires RECOVER/JUSTIFIED for each omission (L292). The sub-question part fails and is recorded under #11. |
| 9 | Error path coverage (fix-cycle bounds) | none | PASS | Each gate decision item writes a `PASS set / FAIL set / |F|` line, then checks for regression, then the monotonicity HALT, then the hard cap of 2 cycles, with its own counter (e.g. L285, L296). Consolidation and verification files are `-cycle<n>` suffixed. One fix agent per cycle. |
| 10 | Runtime path trace (Step 2.5 and web evidence) | none | PASS (notes) | Step 2.5 output goes into research/04 (L185), which Gate 1 reads in full (L192), and Gate 1 item 5 cross-checks 03 against 04. The web files are checked by Gate 2 analyst #3/#10 (L235), Gate 3 evidence-quality (L261) and domain-accuracy (L263), Gate 4 agent-2 (L278) and Gate 5 agent-2 (L289). See MINOR notes M1 and M2. |
| 11 | Completion scope honesty (final report answers the GOAL) | AX-3 | FAIL | No gate maps the report to sub-questions (a)-(f) of the Overview (L66). Gate 1 item 1 (L192) covers a-d only ("e and f are mainly web topics for Phase 4"), and no later gate picks up e and f. Gates 2-5 check output against the research files, so a sub-question that no file answers passes every gate. Step 6.9 (L299) only checks that the "Problem Statement references the original question". See Issue 1. |
| 12 | Ambient dependency completeness (QA_GATE / VALIDATION / TESTING as items) | none | PASS | QA_GATE PER_PHASE: Gates 1-5 are explicit `- [ ]` items. VALIDATION (TEMPLATE_COMPLIANCE, EVIDENCE_TRAIL, CROSS_VALIDATION) is Step 6.9 (L299). TESTING N/A is recorded as an item (L322). |
| 13 | Sequencing red flags (deferred actions completed) | none | PASS | Step 7.2 (L308) reads the fix logs that L281-285, L292-296 and L300 write. The reflect remediations from 7.1 (L305) come before 7.2. The `reflect_post` frontmatter value is filled at 7.1 and checked at Done (L325). |
| 14 | Existence claims verified | none | PASS | Sources the task cites exist: `def publish` at launch-job-identity.sh:164, `O_EXCL|O_NOFOLLOW` at :166, `fchmod(...0o400)` at :171, `os.link(...follow_symlinks=False)` at :172; design §19 starts at L489 (file is 578 lines); `def l2_status` at orca_worktree.py:1012, W-L2-ABSENT at 50/789/1312, IR-7 at 794/1307. |
| 15 | Template cross-references (M3, M4, I16, I17) | none | PASS | M3 lens QA (template L640, L1369), M4 fidelity (L640, L764), I16 fix cycles (L653-677) and I17 post-completion (L679-688) exist and say what the task relies on. I17.5 (final-state lens QA) is met by Gate 3 plus Step 7.2 (L308); see MINOR note M3 on the wording at L323. |

## Summary

- Checks passed: 14 / 15
- Checks failed: 1 (#11, AX-3)
- Critical issues: 0
- Important issues: 1
- Minor issues: 4 (notes only, non-blocking)
- Issues fixed in-place: 0 (fix_authorization false)
- Inherited structural FAIL rows (B2-1, 2, 3, 5, 6, 8; S-3, S-4, S-5, S-9; TB-Add-5, TB-Add-8): closed per `qa/qa-task-validation-verify-cycle1.md` (C1-C12 yes, VERDICT PASS). I spot-confirmed the closure through the gate counts, the fixers' no-spawn rule, whole-tree porcelain, the cycle suffixes and the Step 7.2/7.3 order in the current file. Its line numbers are 3 lower than the current file because the RA alignment fix added lines.
- RA1-RA8 (alignment fix): each confirmed present by my own grep (RA1 L213, RA2 L182, RA3 L185, RA4 L229, RA5 L173, RA6 L179, RA7 frontmatter L22, RA8 L226/L232).

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | Task file L192 (Gate 1 item 1), L289 (Gate 5 agent-2), L299 (Step 6.9) | No gate checks that the final report answers each GOAL sub-question (a)-(f) listed in the Overview (L66). Gate 1 checks a-d and defers e/f to Phase 4, but nothing after Phase 4 checks them. Gates 2-5 compare outputs to the research files, so a sub-question (or sub-part, e.g. extensions.worktreeConfig, the introducing git version per behaviour vs 2.47.3, the executable bit) that no file answers passes every gate. This is a missing required deliverable check (AX-3). | Add a row to the Step 6.9 validation item (L299), or a numbered item to anti-omission-agent-2 (L289): "For each sub-question (a)-(f) listed in the Overview (line 66), name the report section(s) that answer it, sub-part by sub-part. Any unanswered sub-question or sub-part (for example extensions.worktreeConfig, the git version that introduced each behaviour compared with 2.47.3, the executable bit) is an IMPORTANT failure." Also add e and f to the Gate 1 item 1 coverage check, or state there that e/f are checked at Step 6.9. |
| M1 | MINOR | L278 (fidelity-agent-2), L261 (evidence-quality) | No agent checks the quotes and URLs in web-01/web-02 against the live pages. L278 treats the web files as the source for external claims, and L261 checks only that a citation is present. This matches the tech-research skill design (no web gate). | Optionally have fidelity-agent-2 spot-check at least 5 quoted sentences with `mcp__tavily__tavily_extract` (WebFetch fallback, logged). |
| M2 | MINOR | L192 (Gate 1 safety), L311 (Step 7.3), L216 (web-02) | `FOLLOWUP_SANDBOX_PATH` appears only at L185 (grep). The Gate 1 safety check and Step 7.3(a) check only the Phase 2 `SANDBOX_PATH`. The optional web-02 /tmp experiment records no exact path. L185 does have the executor verify the removal. | Name `FOLLOWUP_SANDBOX_PATH` in the L192 safety check and in Step 7.3(a); have web-02 write a `WEB02_SANDBOX_PATH:` line and check it at 7.3. |
| M3 | MINOR | L323, L308 | L323 says "Post-completion lens QA satisfied by Gate 3 ... together with the Step 7.2 final lens re-check", but Step 7.2 uses only the 3 structural lenses on late-changed sections. Content lenses on late fixes are covered only by the L284 and L295 verifiers. | Reword L323 to name the 3 lenses Step 7.2 runs, or add a domain-accuracy lens to L308. |
| M4 | MINOR | L300 | The Step 6.9 validation fix is done by one rf-qa, and the executor itself re-runs the failed checks; no independent verifier. Step 7.2 re-checks those sections afterwards. | Optional: have the 7.2 rf-qa explicitly confirm each `## Fixes` entry. |

## Actions Taken

None. Report only (fix_authorization false). No file other than this report was edited.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- Relied on rf-qa PASS for B2-4
- Relied on rf-qa PASS for B2-7
- Relied on rf-qa PASS for S-1
- Relied on rf-qa PASS for S-2
- Relied on rf-qa PASS for S-6
- Relied on rf-qa PASS for S-7
- Relied on rf-qa PASS for S-8
- Relied on rf-qa PASS for TB-Add-1, TB-Add-3, TB-Add-4, TB-Add-6, TB-Add-7

**(b) Independent semantic checks (≥1 required, INV-019):**
- GOAL sub-question coverage across gates: verified by Grep on the task file. "e and f are mainly web" appears only at L192, and "Problem Statement references" only at L299. No gate item maps the report to (a)-(f). This produced Issue 1, which rf-qa PASS could not catch.
- Sandbox record coverage: verified by Grep. `FOLLOWUP_SANDBOX_PATH` is at L185 only, and `WEB02_SANDBOX_PATH` has 0 hits (M2).
- Fidelity source anchors: verified by reading `src/superclaude/hooks/scripts/launch-job-identity.sh` 164-174 (publish, O_EXCL|O_NOFOLLOW 0o600, fchmod 0o400, os.link follow_symlinks=False), design doc §19 at L489 (lines 510-514, 520, 534 match), and by Grep on `orca_worktree.py` (l2_status 1012; W-L2-ABSENT 50/789/1312; IR-7 794/1307).
- Gate counts and lens types: verified by Grep for `subagent_type` and lens names on L259-265, L277-278, L288-289, against SKILL.md L397-415.
- RA1-RA8 presence: verified by my own Grep for each fix token.
- Template sections: verified by reading template L640-689 (M3/M4/I16/I17).

**Self-audit questions:**
1. Factual claims independently verified: about 30 (gate counts, lens names, line anchors in 3 source files and the design doc, 8 RA tokens, template sections, sandbox and sub-question greps).
2. Files read: the task file (in chunks, plus greps), BUILD-REQUEST.md, qa/qa-task-research-alignment-fix.md, qa/qa-task-validation-verify-cycle1.md, launch-job-identity.sh, launch-level-guard.sh (line count and regex section), docs/designs/sc-issue-launch-level-hook.md §19, orca_worktree.py (greps), install_hooks.py (existence), tech-research SKILL.md L23 and L394-415, MDTM template 02 L640-689, L764, L1369.
3. Not applicable: 1 IMPORTANT and 4 MINOR findings were recorded.
4. No web research was done, so Tavily was not used and there was no fallback.

**Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 11 | Grep: 14 | Glob: 1 | Bash: 12 (read-only, including /tmp mktemp batches under the batching policy)

## Recommendations

- Apply the Issue 1 fix (sub-question (a)-(f) coverage row at Step 6.9 or in anti-omission-agent-2), then re-run task validation before execution.
- The MINOR notes M1-M4 are optional and do not block.

## QA Complete

VERDICT: FAIL
