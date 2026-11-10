# QA Report - Gate 5 Anti-Omission Content Verification (Fix Cycle 2, agent 2 of 2)

**Status:** Complete
**Date:** 2026-11-08
**Phase:** report-qualitative (anti-omission recovery check), fix cycle 2 of 3 (last), fix_authorization: false
**Report under review:** `RESEARCH-REPORT-bmad-first-use.md` (1804 lines); inputs: consolidated findings cycle 2 (BLOCKING_COUNT 3: I-1, I-2, I-3), fix log cycle 2.

---

## Check results

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | I-1 (step 5.3 case (d), l.1542): `bmad-os-x` fixture no longer asserted byte-identical | PASS on the contradiction; new defect N-1 below | l.1542 now reads "(c), (e) and the `bmad-x` fixture of (d) leave P byte-identical"; the `bmad-os-x` fixture "is a first use ... P changes"; agrees with step 3.2 condition 3 (l.1465), Section 9 row 20(b) (l.1718), l.292, l.298. |
| 2 | I-2 (`--output-folder` wording, l.406, 681, 910) | PASS | Grep of `output-folder` and `every (first-use )?command` over the report: l.121, 406, 568, 681, 910, 1021, 1438, 1464 all limit the rule to commands that pass `--user-name`; l.68, 192, 1056 only quote the manual command (no rule). No unqualified rule left. |
| 3 | I-3 (W01-18 l.867, step 4D.4 l.1526) | PASS | Compared with `research/web-01-claude-code-user-skills-hooks-and-live-reload.md` l.127 (project skill hooks register "including in a `-p` run in a folder you haven't trusted"), l.155 (`-p`/SDK treats the folder as trusted), l.156 ("no hook-based option escapes it", settings-file hooks), l.157 (skills not gated the same way). The report now says only that skill-frontmatter hooks run in untrusted `-p` folders where `-p` already trusts the folder; the rest is labelled `[synthesis inference: ...]` and UNVERIFIED - doc-only, and unverified for a user-level stub. Faithful. |
| 4 | Correction text vs `ui.js` 800-869 | PASS | Read `/opt/nvm/versions/node/v24.22.2/lib/node_modules/bmad-method/tools/installer/ui.js` 796-873: partial-seed branch l.807 (any of 4 flags), the install.sh:42 flag set writes only `user_name` and `output_folder` (l.809-824); default branch l.838-861, empty-config test l.843, five keys l.851-859. Report l.1464 and row 20 cite 807-837 / 838-861 / 843 correctly. |
| 5 | `bmad-os-*` citations behind case (d) | PASS | `_config-driven.js:789-790` (cleanup skips `bmad-os-`), `:499-516` (cleanup removal set), `installed-skills.js:45` (`isBmadOwnedEntry` false for `bmad-os-`): all read. |
| 6 | Nothing contradicts Section 9 row 20 (stricter glob) | PASS | l.292, 298, 1465, 1542, 1718 agree: plan default counts `bmad-*` except `bmad-os-*`; the stricter glob stays an open implementer or owner choice. |
| 7 | Q1, Q2, Feasibility statement intact | PASS | Section 9 rows 1 and 2 (l.1698-1699 region) still marked "(unanswered)" with no owner answer invented; l.1695 says nothing is answered; Feasibility statement l.1327-1331 and restated row 4 (l.1702, "stop condition is not triggered") unchanged. |
| 8 | Inference labels intact | PASS | `[synthesis inference: ...]` present at l.867 and l.1526 (new, with UNVERIFIED - doc-only); older labels at l.1351, 1480, 1700 still present. |
| 9 | (a) Placement and consistency with Sections 6 to 9 | PASS | Recoveries sit where a reader looks: W01-18 in Section 5.1, the rule in 2.5 / 4.2 / 5.2 / 3.1, the fixture in step 5.3. None changes an option's feasibility, effort or risk (text-level corrections); Section 6 to 9 statements about hold-back (l.975, 984, 985, 1141, 1491, 1713) agree with the corrected W01-18. |
| 10 | (b) Scannability | PASS with MINOR notes | Recovered text is inside bullets and table cells, not free prose. Notes only: l.867 is 1,690 characters and the step 5.3 cell (l.1542) is 3,496 characters. |
| 11 | (c) Recovered plan steps actionable | FAIL | Step 5.3 case (d): see N-1. |
| 12 | STOP-AND-RE-SCOPE branch | Not triggered (adapted) | Grep for `STOP-AND-RE-SCOPE` / `RE-SCOPE PROPOSAL` found none; Section 7 says feasible, so the normal checks (a) to (c) were applied. |

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| N-1 | IMPORTANT | Section 8, step 5.3, case (d), `bmad-os-x` fixture (l.1542) | The fix tells the test to "assert the same creation as in (a) (`_bmad/_config/manifest.yaml`, `_bmad/config.toml`, the `bmad-*` skill count)". The (a) skill-count assertion is "the number of `P/.claude/skills/bmad-*` directories equals the `<N>` of the installer's `Claude Code configured: <N> skills` line". In the `bmad-os-x` fixture the user's own `bmad-os-x` directory also matches `bmad-*`, so the count is N+1 and the test fails on its own fixture, the same kind of defect as I-1. The installer's N counts only the skills it wrote (it preserves `bmad-os-*`, `_config-driven.js:789-790`). | State that for this fixture the count excludes `bmad-os-*` entries (count `bmad-*` directories other than `bmad-os-*`, equal to N) and that the user's `bmad-os-x` entry is still present. |

Counts: CRITICAL 0, IMPORTANT 1 (blocking), MINOR notes 2 (scannability of l.867 and l.1542, not blocking, not rechecked).

## Self-Audit

- Files and lines read: task file l.469 (the prompt); `qa-anti-omission-consolidated-findings-cycle2.md` (all 25 lines); `qa-anti-omission-fix-log-cycle2.md` (all); report l.860-871, 975-986, 1455-1569, 1695-1718 plus targeted line extracts (l.121, 292, 298, 406, 681, 910, 1021, 1327-1331, 1438); `web-01-...md` l.127 and 155-158; `ui.js` 796-873; `_config-driven.js` 496-517 and 770-806; `installed-skills.js` 30-55.
- Searches run: `output-folder` / `every (first-use )?command` (all hits classified); `byte-identical`; `stricter`; `case (d)` / `bmad-os-x`; `escape`; `frontmatter`; `W01-18`; `STOP-AND-RE-SCOPE`; `Feasibility`; step-5.3 cell and bullet lengths measured with `wc -c`.
- Claims reproduced: the web-01 quotes at l.127/155/156/157, the `ui.js` branch lines (807, 838, 843, 851-859), the `bmad-os-` preservation lines. I did not run any installer or test; anything about install behaviour stays UNVERIFIED.
- Why the count is credible: the three cycle-2 blocking rows were each traced to the source and found fixed. The one new defect (N-1) came from walking the corrected case (d) against the (a) assertion it points to. I looked for similar regressions (other fixtures in 5.3, Section 9 row 20, W01-18 echoes, `--output-folder` echoes) and found none.
- Tool engagement: Read 8 | Grep 1 | Glob 0 | Bash 8 (read-only). Reads plus greps cover the checklist items; no padding calls.
- Confidence: Verified 11 / 11 applicable checks (check 12 not triggered) | Unverifiable 0 | Unchecked 0 | Confidence 100.0%. Verdict is FAIL because of N-1, not because of low confidence.

## Verdict

**FAIL** - 1 blocking issue: N-1 (Section 8, step 5.3 case (d), IMPORTANT). I-1, I-2 and I-3 are fixed. This was the last fix cycle, so under the pipeline rule the gate HALTS unless the orchestrator can still apply one text fix and re-verify.

**Status:** Complete

## QA Complete
