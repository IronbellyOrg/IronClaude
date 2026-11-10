# QA Report — Research Gate Fix Verification (Qualitative, research-depth lens)

**Topic:** Git pre-push hook semantics for the L2 pre-push guard (issue 441)
**Date:** 2026-11-08
**Phase:** research-gate, fix-cycle verification (qualitative, research-depth lens)
**Fix cycle:** 1 (verifies the Gate 1 cycle 0 fixes)
**Fix authorization:** false (report only; no research file was modified)

**Inputs read:**
- `qa/qa-consolidated-findings-phase3-cycle0.md` (blocking findings B1-B4, notes N1-N24)
- `qa/qa-research-fix-log.md` (cycle 0: FIXED 4, NOT FIXED 0; FIX_SANDBOX_PATH none)
- `research/01-identity-selector-ancestry.md`
- `research/02-l1-guard-push-bypass-coverage.md`
- `research/03-design-and-claim-code-crossvalidation.md`
- `research/04-empirical-git-prepush-experiments.md`
- `research/research-notes.md` (web-01 scope line, because the B2 fix edited it)
- `src/superclaude/hooks/scripts/launch-job-identity.sh` (read only, to check the B4 claims)

---

## Overall Verdict: PASS

## Items Reviewed — Per-fix verification (blocking findings B1-B4)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| B1 | 04 has a Key Takeaways section, and it is substantive, not padding | PASS | 04 lines 2233-2245: new `## Key Takeaways` with 9 bullets. Every bullet cites at least one experiment ID (E3-E31, F1, F2, F4), and line 2235 says no new experiment was run, so nothing is presented as new evidence. The bullets draw design-usable conclusions rather than restating headings. Examples: an exact compare of field 3 against `refs/heads/main`/`master` is enough (E6/E20/E21/E11/E3-E5); empty stdin is a real input (E12/E23b/E27a); an installer must use `--git-path hooks/pre-push` (E30, F2); a per-worktree `core.hooksPath` is a bypass (E31). Spot-checked against the recorded experiments: E26 (lines 1372-1421, `--atomic` with a hook exit of 1 refuses both refs), E28c (PATH `/usr/lib/git-core:/usr/bin:/bin`, `UV-ABSENT`), E29 (fails open), E30 (lines 1584-1658, the worktree-private hook is ignored), E31 (lines 1660-1699, `--git-path` printed otherhooks). All match. |
| B2 | Sub-question (b) "other tools" is either tested or routed, with honest tags | PASS | 04 line 2265: "ROUTE web-01: (b) other tools", with per-library sub-bullets for pygit2/libgit2, dulwich, GitPython and JGit at lines 2266-2269. Each names a concrete documentation or source location and the exact question to answer: does it run `hooks/pre-push`, and from which directory. Every library is marked [UNVERIFIED], and line 2270 says no location was fetched. Line 2268 keeps the GitPython "runs the git binary" premise [UNVERIFIED] instead of asserting it. Option (a), local testing, was correctly not possible: my own `uv pip list` check matched none of dulwich, pygit2 or GitPython, which matches the fix log. 02 Gap 6 (line 264) points to the route, and 02 line 190 keeps its [UNVERIFIED] scope tag. `research-notes.md` line 73 includes (b) in the web-01 scope. 04 line 2270 cites "02 §7 (line 187, PARTIAL)", and 02 line 187 is that PARTIAL row. The fix adds a real routing decision for Phase 4, not filler. |
| B3 | 03 no longer says the line-487 corpus is absent, and the correction rests on fresh evidence | PASS | 03 line 22 is a correction paragraph that cites 48 .md files (25 in the corpus, 23 in the sibling), 27 git-tracked files and commit `4f7e3e7e`. My own batch check reproduced each figure: the corpus .md counts were 25 and 23, `git ls-files` gave 27 for the corpus and 0 for `20261106-l2-prepush-decisions/`, and `git log` gave `4f7e3e7e`. 03 line 24 re-checks the D19 rows and finds none that rests on the corpus. Its quotes of `merged-requirements.md:1384`, `refactor-plan.md:1158` and `variant-1-opus-architect.md:135` matched the files exactly in my check. Gaps (line 301), Stale Documentation (lines 318-319, including a new "Not stale" line) and the Summary (line 328) were all updated together. No stale "absent" wording remains: the Grep for `20261105-170229` in the research files finds only the corrected lines. |
| B4 | 01 states the human-without-uv consequence, and 04's "absolute uv path" remedy is corrected | PASS | 01 lines 195-196 add two sub-bullets under item 5. They cite script lines 19-25, 52-53 and 566, and I confirmed each against `launch-job-identity.sh`: the no-store exit applies only to `$# == 0` or `hook`; `command -v uv` is at line 25; the "UV is required" message and `exit 2` are at lines 52-53; `exec uv run --no-project python -I -c ...` is at line 566. The reasoning holds. An absolute path in the hook does not reach the script's own two PATH lookups. Option (i), a fixed PATH, covers both lookups. Option (ii), a no-store short-circuit, does not help a human on a machine that also runs governed sessions, and 01 says so. A new Key Takeaway is at 01 line 203. 04 line 1530 (E28 uv bullet), line 2244 (Key Takeaway) and line 2259 (open question) carry the correction and point back to 01 §4 item 5. 01 line 195 correctly labels the behaviour as inferred from reading the script, not observed by running it. |

## Items Reviewed — Cross-cutting quality checks

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| Q1 | The fixes deepen the findings and make them actionable, and are not padding | PASS | Each fix changes what a spec author would do. B4 replaces a remedy that does not work (an absolute uv path) with three named options and their coverage limits (01 line 196). B2 gives web-01 a per-library question plus source locations (04 lines 2265-2269). B3 removes a false [STALE DOC] that would have sent a reader looking for a missing corpus (03 lines 22-24, 318-319). B1's takeaways compress 31 experiments into 9 design-relevant conclusions (04 lines 2237-2245). No fix adds generic prose without a cited source. |
| Q2 | No contradiction introduced between files | PASS | uv/PATH story: 01 item 3 (line 192), item 5 (lines 195-196), Key Takeaways (line 203) and Summary (line 305) agree with 04 lines 1528-1530, 2244 and 2259. Both say exit 2 maps to `unknown`, a refusal only for `main`/`master`, and a fixed PATH or no uv. Other-tools routing: 02 line 190 [UNVERIFIED, L2 hook research], 02 Gap 6 (line 264), 04 line 2265 and research-notes line 73 all route to web-01. Corpus: 03 lines 22, 301, 319 and 328 consistently say "present". No other research file says "absent" (Grep for `20261105-170229`). The 01 §8 wording is in mild tension with the new option (i); see N-1 below. It is not a contradiction, because §8 describes today's default and option (i) is a proposed hook change. |
| Q3 | Git-behaviour claims added by the fixes carry a command, an experiment ID or a tag | PASS | Every git-behaviour sentence added in 04's Key Takeaways cites E-/F-IDs (lines 2237-2245). The uv correction cites script line numbers and E28c (04 line 1530; 01 line 195). The B2 route is tagged [UNVERIFIED] for every library (04 lines 2265-2268). The B3 correction cites `git ls-files`, `git log -1` and Glob results (03 line 22). The new 01 text says it was inferred from Read, not run (01 line 195). No untagged git-behaviour assertion was introduced. |
| Q4 | The fix log is honest and matches the files | PASS | Fix log rows B1-B4 (`qa-research-fix-log.md` lines 14-17) name the exact sections edited; each was found at the location stated. The claims "No new experiment" and FIX_SANDBOX_PATH none are consistent with 04 line 2235 and the absence of any new E-ID after E31. The claim that MINOR notes were not applied is consistent with the remaining N21 miscite at 04 line 1530 ("E9-E11"). |
| Q5 | Fix scope stayed on the blocking findings, with no scope creep | PASS | The edits are confined to the B1-B4 locations plus their necessary echoes in Gaps, Summary and Stale Documentation. No new section unrelated to B1-B4 appeared in 01-04. |

## Summary
- Checks passed: 9 / 9 (B1-B4, Q1-Q5)
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- New MINOR notes: 4 (N-1 to N-4 below; none blocking)
- Issues fixed in-place: 0 (fix authorization false)
- Previously blocking findings now passing: B1, B2, B3, B4. Still failing: none.
- Issue count trend: cycle 0 had 4 blocking findings; this cycle has 0. No systemic regression.

## Issues Found (new, introduced or left incomplete by the fixes)

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| N-1 | MINOR | `research/01-identity-selector-ancestry.md` §8, line 275 | The text says the hook calls `identify` "with the hook's inherited `HOME` and `PATH`". The new item 5 option (i) (line 196) proposes that the hook set a fixed PATH. This describes the default rather than contradicting it, but a reader may take line 275 as settled. | Add "(unless the spec adopts §4 item 5 option (i), a fixed PATH)" after "inherited `HOME` and `PATH`". |
| N-2 | MINOR | `research/01-identity-selector-ancestry.md` Gaps item 4 (line 289) and Summary (line 305) | Gaps item 4 lists the humans restricted by `unknown` (HOME unset/relative, group-writable home, stale records) but omits the new no-uv human case that B4 added to item 5. The Summary mentions "a PATH without uv yields exit 2" but not that this restricts humans. This is internal incompleteness, not a false claim; item 5 and the Key Takeaway (line 203) state it. | Append "a human whose PATH lacks uv (§4 item 5)" to Gaps item 4, and add "including humans whose PATH lacks uv" to the Summary sentence. |
| N-3 | MINOR | `research/04-empirical-git-prepush-experiments.md` E28 uv bullet, line 1530 | The superseded sentence "has to call uv by absolute path or not depend on uv at all" is kept and followed by "Correction ...". This reads as two remedies in one bullet. The existing N21 miscite "(E9-E11)" (the nonzero-exit refusal is E19/E24/E26) also remains, as expected, since MINOR notes were not applied. | Replace the superseded sentence with the corrected remedy, rather than appending; optionally fix the E-ID per N21. |
| N-4 | MINOR | `research/04-empirical-git-prepush-experiments.md` Key Takeaways, line 2243 | The heading "The environment passes through unchanged" sits next to "PATH (with `/usr/lib/git-core` prepended)", so "unchanged" is slightly inaccurate for PATH. The same wording is at line 1528. | Change it to "passes through, with only `/usr/lib/git-core` prepended to PATH" (or "almost unchanged"). |

Pre-existing notes not re-checked as blocking, per the fix-cycle rule: N4 (04 Stale Documentation line 2274 "None contradicted" vs the [CODE-CONTRADICTED] D19-47 tag at line 2261), N21 and N22 (01 section order) are still present and remain MINOR.

## Actions Taken
- None. Fix authorization is false. No research or source file was modified. The only file written is this report.

## Confidence Gate

- [x] B1 verified: Read 04 lines 2231-2276 and the E26/E28/E29/E30/E31 sections.
- [x] B2 verified: Read 04 lines 2265-2270, 02 lines 187/190/264, research-notes line 73; ran `uv pip list` (no match).
- [x] B3 verified: Glob of the corpus, a Bash batch (`git ls-files`, `git log -1`, quote matches), and Read of 03 lines 22-24, 301, 318-319, 328.
- [x] B4 verified: Read `launch-job-identity.sh` lines 1-60, line 566 in a batch, 01 lines 192-203, and 04 lines 1528-1530, 2244, 2259.
- [x] Q1-Q5 verified: Read of the edited sections above, plus a Grep across `research/` for the corpus and library names.

**Confidence:** Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 16 | Grep: 4 | Glob: 2 | Bash: 2. The counts span this review, including its earlier part before a context compaction; the earlier counts were reconstructed, not logged, so treat them as approximate lower bounds. Bash was used only for a read-only batch (corpus counts, `git ls-files`, `git log -1`, quote matching, the script's line 566, `uv pip list`). No git push, no network fetch, no web research. Tavily was not needed, so no fallback was used.

## Self-Audit

**(a) Reliance list — items accepted without structural re-check:**
- Relied on the consolidated findings file (`qa-consolidated-findings-phase3-cycle0.md`) for the definitions of B1-B4 and N1-N24. They were not re-derived from the original phase 3 QA reports.
- Relied on 04's recorded experiment transcripts (E0-E31, F1-F4) as faithful records of git 2.47.3 runs. No experiment was re-run, because the fix made no new git claim needing a fresh run, and the safety rules allow git experiments only in a `/tmp` sandbox, which this check did not need.
- No `## Inherited Structural Verdict` block was supplied in the spawn prompt, so no rf-qa PASS items were inherited; structural points (section presence, line locations) were checked directly.

**(b) Independent semantic checks (≥1 required, INV-019):**
- B4 reasoning, checked against the source: read `src/superclaude/hooks/scripts/launch-job-identity.sh` lines 19-25 and 52-53, and found line 566 in the batch. This confirms that the no-store exit does not cover `identify`, that uv is resolved through PATH twice, and therefore that an absolute uv path inside the hook cannot fix it. Option (ii)'s stated limit (it does not help when a store exists) follows from lines 20-24.
- B3 correction, checked against the filesystem and git: corpus .md counts of 25 and 23, 27 git-tracked files, 0 tracked under `20261106-l2-prepush-decisions/`, commit `4f7e3e7e`, and the three quoted corpus lines matching exactly. Every figure in 03 line 22 was reproduced.
- B2 "not testable locally", checked: `uv pip list` matched none of dulwich, pygit2 or GitPython.
- Cross-file consistency, checked by meaning: compared the uv/PATH statements in 01 (lines 192, 195-196, 203, 275, 289, 305) with 04 (lines 1528-1530, 2243-2244, 2259). This found N-1 and N-2, which a structural check would not catch.

**Why trust a 0-blocking result:** every B-fix was checked against a primary source (script lines, git output, file counts) rather than against the fix log, and the review still found four new MINOR defects. That shows the files were read closely, not skimmed.

## Recommendations
- Proceed past Gate 1: no open CRITICAL or IMPORTANT findings.
- Optional cleanup, non-blocking: apply N-1 to N-4 (and the earlier N4/N21) when 01 and 04 are next edited, so that the synthesis step does not copy the superseded "absolute uv path" sentence from 04 line 1530.

## QA Complete



