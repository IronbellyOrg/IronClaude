# Qualitative scoring, pass 1 (order V1, V2, V3)

Files: variant-1-original.md, variant-2-original.md, variant-3-original.md. Seed brief used as the requirement source. No debate folder or diff-analysis read.

Arithmetic rechecked: V1 time and gain totals reproduce. V2 critical path (8+1+19+1) gives 129-151, not the stated 128-150. V3 coverage sums recompute to 3.50-6.05 (CRS) and 3.40-5.95 (BLV), not 3.6-6.6 and 3.3-6.2.

| criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| CO1 covers all seed requirements | MET | Sec 1 theory mapping; (a)-(i) per redesign; sections 5-6 | MET | Sec 4 "Theories answered" row; (a)-(i) per redesign | NOT MET | No redesign-to-theory mapping; idle-time reallocation not assigned |
| CO2 edge cases and failure scenarios | MET | REQ-11 fallback; abort on missing source; NONE FOUND | MET | Empty sheet equals baseline; pre-pass kill at 15 s | MET | Reverse-dependency flood cap 12; verifier kill marks unverified |
| CO3 dependencies and prerequisites | MET | H1-H4 prerequisites; plan sha check flagged UNVERIFIED | MET | H3 is a precondition (R-04); sha comparison first | MET | "Both redesigns depend on harness fixes H1 to H4" |
| CO4 success/completion criteria | MET | Pre-registered gates G1-G7 | MET | Decision rule D1-D6 with outcomes table | MET | Section 4 decision rule, five checks |
| CO5 out of scope stated | MET | Claims-only exchange "out of scope for the first test" | MET | "Out of scope" line; messaging not used; docs set not gated | NOT MET | No out-of-scope statement anywhere |
| CR1 no factual errors (arithmetic) | MET | Recomputed 402, 474, 393, 453, 3.4-6.1, 2.8-5.5 correct | NOT MET | Stated 128-150 s; table sums to 129-151; 24 vs 25 assignments | NOT MET | Coverage sums 3.6-6.6 recompute to 3.5-6.05; +6% vs +21% |
| CR2 feasible within +35% | MET | Expected +15%/+13%; timeout D; fallback on failure | MET | Expected +23-28%; tightest 128 s vs cap 135 s, mitigation given | NOT MET | +18 s for 60 items vs +30% tokens; timeout 165+6+3 exceeds cap |
| CR3 terminology consistent | NOT MET | Hold-out H2/H5 collide with harness H1-H4; arm A3 tests Redesign B | NOT MET | Hold-out H5/H2 vs fixes H1-H4; step S1 vs extractor S | NOT MET | "H4" names two fixes; GT, I and B labels mixed |
| CR4 no internal contradictions | MET | None found; worst-case overrun of D acknowledged | NOT MET | R-12 caps critical-path model at 6 items; primary luna gets 8 | NOT MET | Per-package +6% vs aggregate +21% from same table |
| CR5 claims supported | MET | Theory tables cite PAT, DS, AC sections with counts | MET | Theory rows cite PAT sec 1, DS sec 2c counts | MET | Theory table cites investigation sections with run counts |
| ST1 logical section ordering | MET | 3.0 scaffolding precedes both redesigns | MET | Shared brief changes precede both redesigns | MET | Order follows seed; shared 3.3 placed after redesigns |
| ST2 consistent hierarchy depth | MET | Identical (a)-(i) headings in 3.1 and 3.2 | MET | Identical bold (a)-(i) in both redesigns | MET | Identical (a)-(i) in 3.1 and 3.2 |
| ST3 separation of concerns | MET | Shared scaffolding 3.0 separate from redesigns | MET | Shared brief changes separate from redesigns | MET | Harness fixes 3.3 separate from A and B |
| ST4 navigation aids | MET | Conventions block; REQ-nn and section cross-references | MET | Conventions block; R-04, R-14, D2 references resolve | NOT MET | No conventions block; "validation run (section 5)" points at requirements |
| ST5 six-section artifact conventions | MET | Six numbered sections matching the seed | MET | Six sections including comparison section 4 | MET | All six parts present; comparison nested as 3.4 |
| CL1 unambiguous language | MET | Exact item JSON, ledger row syntax, testable REQs | MET | Ledger line syntax and numeric caps stated | NOT MET | "Every reviewer answers all" vs "ember takes mechanical items" |
| CL2 concrete not abstract | MET | Quoted CB1-CB4 and eight recipe texts | MET | Quoted recipes R-C1 to R-C8 | MET | Quoted brief and per-class item templates |
| CL3 one purpose per section | MET | Each of six sections has one purpose | MET | Each of six sections has one purpose | MET | Sections 1-5 each single purpose |
| CL4 terms defined on first use | MET | Conventions defines BR, EVAL, HO2, IG, RE, DS, AC, PAT | MET | Conventions defines EVAL, BR, GEN, EXT, DS, AC, PAT | NOT MET | GT, "DE runs", "terra" never defined |
| CL5 actionable next steps | MET | Sec 4 recommendation; build 3.0 first; outcomes list | MET | Outcomes table with adopt, stop, report actions | MET | Adopt CRS if difference under 0.3 |
| RK1 at least 3 risks with probability and impact | MET | Kill rate 5% or less; luna files 31% surface blockers | MET | Rubber-stamp 41% non-defects; compliance 91.4%; 2.75-3.25 wrong blockers | NOT MET | Only false-positive growth quantified (+2 to +4); no likelihoods |
| RK2 mitigation for each risk | MET | Every failure-table row has a mitigation | MET | Every failure row has a control | MET | Every failure bullet has a mitigation |
| RK3 failure modes and recovery | MET | Graceful degradation to isolated panel; fallback recorded | MET | Pre-pass kill falls back; re-ask only if time fits | NOT MET | Killed CRS reviewer lost; helper failure unhandled |
| RK4 external dependencies and failure | MET | REQ-35 judge API error audited per batch | MET | Block-randomised order cancels gateway load drift | NOT MET | No judge, gateway or API failure handling |
| RK5 monitoring or validation mechanism | MET | Per-class yield telemetry; REQ-33 displacement and wrong blockers | MET | R-10 meta fields; ledger audit metrics | MET | Coverage audit counts unchecked; req 20 wrong blockers |
| IV1 collection boundaries | MET | NONE FOUND for empty check; cap 12 items | MET | Empty sheet; 12-item cap; R-17 | MET | 200-sentence fixture capped at 60; 12 hits per path |
| IV2 cross-boundary state interactions | MET | Ledger quote vs 200-char anchor; promotion via anchor_text | MET | Ledger outside block; R-03 merge unchanged | MET | Coverage block ignored by merge; req 7 |
| IV3 guard-condition gaps | MET | Unknown-key acceptance and plan sha flagged UNVERIFIED | MET | Plan sha equality UNVERIFIED, must be checked first | MET | BLOCK_OK checks fence opener only; parse gap noted |
| IV4 count divergence | MET | D=floor(1.35b); run counts 120, 96, 48 reproduce | NOT MET | 128 vs 129 critical path; 25 vs 24 item assignments | NOT MET | Coverage sums off by 0.1 to 0.55 |
| IV5 combined-component interactions | MET | Harness overlap may double-count 0.1; displacement | MET | H and redesign shares never summed; placebo arm | MET | "Shares are not additive" |

## Subtotals per dimension

| dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness (CO, /5) | 5 | 5 | 3 |
| Correctness (CR, /5) | 4 | 2 | 1 |
| Structure (ST, /5) | 5 | 5 | 4 |
| Clarity (CL, /5) | 5 | 5 | 3 |
| Risk coverage (RK, /5) | 5 | 5 | 2 |
| Invariant and edge cases (IV, /5) | 5 | 4 | 4 |
| **Total (/30)** | **29** | **26** | **17** |
