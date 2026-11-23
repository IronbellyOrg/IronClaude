# Gate 4 (source-document fidelity) consolidated findings, cycle 1

Reports: `qa-source-fidelity-report-1.md` (PASS, 0 blocking, 6 minor) and `qa-source-fidelity-report-2.md` (PASS, 0 blocking, 10 minor), in the same folder.

**Consolidated verdict: PASS with notes. F_1 (blocking findings) = 0.** No phantom finding, no distorted or inaccurate code behaviour and no aspirational claim was found by either agent; about 150 claims were re-checked or reproduced.

## Blocking findings

None.

## Minor findings (notes only, not fixed)

| # | Type | Report section | Finding | Originating agent |
|---|---|---|---|---|
| 1 | Inaccurate (citation) | 2.1 | `line`-class column names in `_columns` cited as `render.py:203-204`; they are at 199-202. | fidelity-1 |
| 2 | Inaccurate | 2.4 | 116 ledger row says "5 header lines"; capture has 4 plus the gap notice (also fidelity-2 F-4). | fidelity-1, fidelity-2 |
| 3 | Inaccurate (citation) | tests table | `:454` listed among `GAP_NOTICE in lines` checks; it is `not in`. | fidelity-1 |
| 4 | Tag drift | 5 vs 2-4, 8 | `safe_box` probe, 16-colour collapse and `rich.box.HEAVY`/`ASCII` tagged [UNVERIFIED] in Section 5, [CODE-VERIFIED] elsewhere; both agents reproduced them. | fidelity-1 |
| 5 | Design extension | 3.2, RB-01(c), 5.3 | Bold amber desk age is a design choice (user-approved), not mockup evidence: the decision-desk mockups show the age in base colour; the "verified from segment text" wording applies to the list rows only. | fidelity-1, fidelity-2 (F-10) |
| 6 | Inaccurate (citation) | source-guard test | `test_render.py` :396-404 cited with four different ranges. | fidelity-1 |
| 7 | Inaccurate | 2.x (80-column attention ledger) | "three plain question lines above the pane" are a focused card; Q01 to Q03 sit inside the SELECTED SIGNALS pane. | fidelity-2 F-1 |
| 8 | Missing detail | colour tables, RB-01(e) | Cyan frames (80-column SELECTED SIGNALS pane, 160 SIGNALS pane) and bold amber STALE are not in the colour tables; RB-01(e) "every secondary-pane border is slate" would disagree with the 80-column mockup. | fidelity-2 F-2 |
| 9 | Inaccurate | 3.2 | Badge written `SYNTHETIC / READ ONLY`; source has a middle dot. | fidelity-2 F-3 |
| 10 | Tag drift | 5, 9 | `send-keys` and `attach --create-background` and `run_interactive --fixture` tagged [UNVERIFIED] but present locally (local Zellij help; commands.py:165-166, :373). | fidelity-2 F-5 |
| 11 | Inaccurate (citation) | several | `render_current.py` is 93 lines; `snapshot_json` at export.py:219; test_commands :671-675 and :691; pexpect `>=4.9`. | fidelity-2 F-6 |
| 12 | Inaccurate | 7.2 | "export writes ids, times and counts": the record also writes each question's subject-based line text. | fidelity-2 F-7 |
| 13 | Omission (stated) | 4.5 | Record file name, state directory, 0600 atomic write, collector and retention constants, key decoder not in the report; excluded on purpose by 4.5. | fidelity-2 F-8 |
| 14 | Wording | 4.1 | "severity scale in the header" does not exist; M-01 to M-05 Critical in 4.1 vs High in 1.3 and 8.10. | fidelity-2 F-9 |

Items 8 and 12 are the most worth carrying into the redesign spec (the 80-column cyan frame and the record text), as follow-up notes.
