# Qualitative scoring, pass 2 (evaluated in order V3, V2, V1; columns shown V1, V2, V3)

| criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| CO1 | MET | Theory mapping table 1; 8 recipes quoted; all seed parts present | MET | Section 4 "Theories answered"; 8 recipes quoted; all six sections | NOT MET | No redesign-to-theory mapping; only 5 of 8 class templates quoted |
| CO2 | MET | 3.1(i)/3.2(i) failure tables: over-extract, probe timeout, kills | MET | Failure tables: rubber-stamp, extractor miss, slow pre-pass, leak path | MET | 3.1(i): FP growth, flood, haiku ignores list, verifier rejects |
| CO3 | MET | H1-H4 shared scaffolding; REQ-03 base commit; unknown-keys test | MET | R-04 "H3 is a precondition"; pre-pass reads sandbox | MET | "Both redesigns depend on harness fixes H1 to H4" |
| CO4 | MET | Gates G1-G7 and outcomes list in section 5 | MET | Decision rule D1-D6 plus outcome table | MET | Five-check pre-registered decision rule, section 4 |
| CO5 | MET | Claims-only exchange "out of scope for the first test"; no messaging | MET | "Out of scope for this file"; messaging not used; I7 excluded from sums | NOT MET | No out-of-scope statement anywhere |
| CR1 | MET | Recomputed: matrix sums 1.70/3.70, 1.05/3.10; +14.8%, +34.4% correct | MET | Recomputed: 1.63/3.55, 1.25/3.10, 254 runs, +23%, +18% correct | NOT MET | Matrix sums stated 3.6-6.6 and 3.3-6.2; actual 3.5-6.05, 3.4-5.95 |
| CR2 | MET | Expected +15%/+13%; worst +36% kill-limited, disclosed | MET | Primary +23-28% and +18-22%, within cap 135-165 | NOT MET | BLV critical path 148 s exceeds 135 s cap for 100 s package |
| CR3 | MET | Class IDs C1-C8, cards, probe, lens used consistently | MET | Conventions block; C1-C8, ledger, sheet used consistently | NOT MET | Wrong section refs ("validation run (section 5)"); H4 used for two fixes |
| CR4 | NOT MET | Luna +1.5k tokens at 48 tok/s conflicts with stated +12 s | NOT MET | "C2, C4 duplicated" fails sonnet panel; "at most 6 items" vs luna 8 | NOT MET | "Every member answers full list" vs ember mechanical, luna reading split |
| CR5 | MET | Evidence tables with PAT/DS/AC section cites | MET | Evidence column with counts and source sections | MET | Theory table numbers cited to investigation files |
| ST1 | MET | Order: theories, classes, redesigns, comparison, validation, requirements | MET | Same order, shared brief changes before redesigns | MET | Sections 1-5 in seed order; fixes in 3.3 |
| ST2 | MET | Both redesigns use #### (a)-(i) identically | MET | Both redesigns use bold (a)-(i) identically | MET | 3.1 and 3.2 share (a)-(i) layout |
| ST3 | MET | 3.0 scaffolding separate from 3.1/3.2; comparison section 4 | MET | Shared brief, two redesigns, comparison, experiment separated | MET | Harness fixes 3.3 and comparison 3.4 separate |
| ST4 | MET | Conventions block (BR, EVAL, HO2, IG); REQ-01..37 ids | MET | Conventions paragraph; R-01..R-32; D1-D6 | NOT MET | No conventions block; cross-refs point to wrong sections |
| ST5 | MET | All six seed sections present | MET | All six seed sections present | MET | All six seed sections present |
| CL1 | MET | Exact ledger format, caps, time limit D = floor(1.35 x b) | MET | Exact ledger line format; 12-item cap; 15 s kill | NOT MET | "Both luna members get the full list" contradicts role split |
| CL2 | MET | Quoted recipes, question templates, line counts | MET | Eight quoted recipes, exact ledger syntax | MET | Quoted brief wording, templates, 60-item/10 KB caps |
| CL3 | MET | Each numbered section has one purpose | MET | Each numbered section has one purpose | MET | Each numbered section has one purpose |
| CL4 | MET | Conventions define abbreviations; E1-E7, CB1-CB4 defined | MET | Conventions define GEN, EXT, DS, AC, PAT; CB-1 defined | NOT MET | "DE runs", "terra", "grok" never defined |
| CL5 | MET | Outcomes: both pass, one passes, neither passes | MET | Outcome table: neither, one, both, placebo | MET | Adopt CRS if difference below 0.3; neither: harness only |
| RK1 | NOT MET | Failure tables list effect, no probability per risk | NOT MET | Failure tables list effect, no probability per risk | NOT MET | Failure modes give magnitudes only, no probability |
| RK2 | MET | Mitigation column for every failure row | MET | Control column for every failure row | MET | Mitigation line on every failure mode |
| RK3 | MET | "Graceful degradation" falls back to isolated panel | MET | Pre-pass kill falls back; re-ask rule; ledger_missing | MET | Verifier timeout leaves claims unverified, listed in follow-up |
| RK4 | MET | REQ-35 judge API error audited; git recovery must be checked | NOT MET | Only gateway-load randomisation; no dependency failure handling | NOT MET | No external dependency failure handled |
| RK5 | MET | Per-class yield telemetry; kill rate and wrong-blocker gates | MET | Clean twins, OK-rate audit, ledger-check script | MET | Coverage audit counts unchecked; wrong blockers counted separately |
| IV1 | MET | Cap 12 items; NONE FOUND row; 250-char anchor fixture | MET | Empty sheet equals baseline; 12-item cap; R-17 test | MET | 200-sentence fixture capped at 60; exact 12/200 anchor fixture |
| IV2 | MET | Quote check demotes unsupported rows; class/probe keys via merge | MET | Ledger DEFECT must appear in findings; re-ask time condition | MET | Defect verdict needs matching finding; coverage ignored by merge |
| IV3 | MET | REQ-10 verifies unknown keys accepted before reliance | MET | Quote exact-substring check; sha check flagged UNVERIFIED | MET | BLOCK_OK checks only fence opener; parser required |
| IV4 | MET | I7 kept separate from /14; sums and run totals recompute | MET | I7 excluded from sums; 254-run total recomputes | NOT MET | Sum errors; "eight hold-out and derivation packages" is six |
| IV5 | MET | Harness and redesign overlap "may double-count about 0.1" | MET | H share and redesign share never summed in headline | MET | "Shares are not additive"; luna overlap is cross-check |

## Subtotals by dimension

| dimension | max | V1 | V2 | V3 |
|---|---|---|---|---|
| Completeness (CO1-CO5) | 5 | 5 | 5 | 3 |
| Correctness (CR1-CR5) | 5 | 4 | 4 | 1 |
| Structure (ST1-ST5) | 5 | 5 | 5 | 4 |
| Clarity (CL1-CL5) | 5 | 5 | 5 | 3 |
| Risk coverage (RK1-RK5) | 5 | 4 | 3 | 3 |
| Invariant and edge case (IV1-IV5) | 5 | 5 | 5 | 4 |
| **Total** | **30** | **28** | **27** | **18** |
