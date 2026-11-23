# Gate 5 (anti-omission) consolidated findings, cycle 1

Reports: `qa-anti-omission-report-1.md` (FAIL: 28 omissions in 15 rows, 1 IMPORTANT and 27 MINOR; 1070 findings enumerated) and `qa-anti-omission-report-2.md` (FAIL: 9 MINOR omissions; 675 raw items, 634 distinct), both in this folder. Every omission is either recovered or explicitly justified below; none is silently dropped.

**Consolidated verdict: FAIL. F_1 (blocking) = 1** (the one IMPORTANT omission). The 36 MINOR omissions are handled as in the table below: 4 are cheaply recovered in the same edit, the rest are justified as out-of-scope low-level detail.

## Blocking finding

| # | Finding | Severity | Blocking | Affected report section | Originating agent | Proposed fix |
|---|---|---|---|---|---|---|
| 1 | The severity scale from synth-02 (Critical, Important, Minor, and what counts as a C8 defect) is missing from the report: Section 4.1 says "Severity follows the scale in the header" but no scale exists, so every severity label in the gap table (4.1) and the remediation needs (4.2) is undefined. The path of `FIND` (`/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/merged/FINDINGS.md`) is also never given although `FIND` and other abbreviations (`RR`, `R01` to `R05`, `W01`, `W02`, `GAPS row N`) are used. | IMPORTANT | yes | Section 4 header (4.1), and a short legend near the top of the report | anti-omission-1 | Add the severity scale (and the C8 definition) from synth-02 to the Section 4 header; add an abbreviation legend (`FIND`, `RR` = `rendering-rules.md`, `R01`-`R05`, `W01`/`W02`, `GAPS row N`) with the full paths after the Table of Contents or at the start of Section 10. Note that Gate 4 also found the same dangling "severity scale in the header" (fidelity-2 F-9) and that M-01 to M-05 are Critical in 4.1 and High in 1.3 and 8.10: add one sentence mapping High to Critical. |

## Minor omissions: disposition

| Group | Omission | Disposition |
|---|---|---|
| anti-omission-2 O1 to O4 | `render_current.py` mixes fixture-mode and live-mode data and does not capture NO_COLOR, `--ascii`, error states or heights other than 50; RR 17 header contract wording (`SYNTHETIC FIXTURE <variant>, not Orca data`); the full question text is untruncated in inspector and export paths (RR 26) but not in the Decision Desk; RR 21 key list contents and the absence of an `r` key | RECOVER with one or two sentences each (in Section 2 or the plan notes), in the same fix pass |
| anti-omission-2 O5 to O9 | `config.kdl` header purpose; remaining `zellij run` flags and `--max-panes`; command-pane exit code, Enter re-run, `start_suspended`, swap layouts; `console.py:805/955/964` citation; Makefile target inventory with line numbers | JUSTIFIED as out-of-scope low-level detail: the Zellij verdict (optional layout only, not a dependency) and the plan do not rely on them; the facts remain in research files 05, web-02 and `gaps-and-questions.md` |
| anti-omission-1 minor (27) | Inspector body and height overflow; `line` and `short` column widths; sanitize line/block modes; character-versus-cell arithmetic; gate-refusal and exit-code behaviour; commands.py constants; the loop's failure and exit handling; export file mechanics; test-helper inventory; a few test pins (the `>` truncation marker, `test_f04`); the rule that `release1_surface.py` imports only release-1 names; Rich `cell_len` handling of ZWJ and VS16, and `Text.from_ansi` | JUSTIFIED as out-of-scope low-level detail: none changes a decision, a phase or an acceptance check in the plan; the facts remain in research files 01, 02, 03 and web-01 (the report's Section 4.5 already names the collector, parse and key-map internals as intentionally excluded) |
