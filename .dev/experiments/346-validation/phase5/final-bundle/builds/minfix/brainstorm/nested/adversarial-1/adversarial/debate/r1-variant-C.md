# Round 1 — Variant C

## Position summary

**Prefer C's transaction contract:** exact reconstruction, pinned inputs, one budget owner and externally granted exceptions make admission reproducible rather than a reviser's assertion (C §2, lines 43–49, 62, 88–98, 122). C is not experiment-ready as written: its coordinator-dispatch gap is real, and its forecast of one remaining critical/major finding per replicate is unsupported; borrow A's actor placement and B's experimental discipline before implementing it (A:37–42; B:362,397–409; C:126,313,352).

## Steelman of A

A's strongest argument is operational fit. “The coordinator gets no new duty” (A §2, line 37), because the reviewer saves the baseline and the report tells the reviser exactly what to run (A:42–62). That is genuinely better than assuming a command loaded by a review worker can instruct its parent coordinator. The existing command assigns the coordinator only count/prior-report/saved-copy duties (P:261), so A minimizes a real delivery problem rather than just reducing file count.

A also identifies a concrete mechanism worth testing: the non-blocking F22 → N5 → N12 chain (A §1, lines 28–30), and limits condition words because new guards produce further boundary-table work (A:80,129). The chain itself is corroborated: D1:37,39 records F22 applied despite being non-blocking; R2:48 names its new defective check; R3:35,84–89 traces N12 to the N5 fix. Its direct checker rerun and explicit carried-versus-new diagnostic are good controls against trusting a reviser's claimed resolution (A:66–68,305).

## Steelman of B

B's strongest argument is that **smaller is not necessarily more correct**. Its evidence section separates non-blocking edits, universal claims, executable checks, unused deletion options and flawed recommendations (B §1.3–1.5, lines 40–87). It explicitly says “Size and normative-word count do not separate the groups” (B:87). R2:27–38 independently supports its contract-shape, path-root and overly broad claim examples; R3:35 shows a fix resolving its parent while introducing another blocker. A size-only success claim would miss exactly these cases.

B also gives the clearest calibration sensitivity: at a 60-word MAJOR cap 13/17 historical fixes exceed it, at 80 words 11/17 do (B:89–98). These are B's measurements, not independently reproduced here, but its method and uncertainty are more inspectable than C's uncalibrated constants. Its source-matched experiment build (B:362), machine-derived child links (B:111,384) and reviewer blindness to ledger explanations (B:111,477) are sound. Atomic whole-finding restoration is an honest attempt to make the retry terminate without another model complying (B:210–211); my objection below is its input attribution and dependency assumptions, not that operational goal.

## Strengths claimed

### Citation key and evidence boundary

A/B/C are design proposals, not implemented checkers. All four comparison inputs were read fully in chunks of at most 120 lines. Ground-truth citations below are independent file reads, not quotations accepted solely from a variant. No checker, measurement script, experiment or installation was run for this debate; historical per-finding word estimates remain the proposing author's estimates.

- **A**: `/home/coder/workspaces/worktrees/IronClaude/bs346-minfix/.dev/brainstorms/346-minfix/nested/adversarial-1/adversarial/variant-1-opus-architect.md`.
- **B**: `/home/coder/workspaces/worktrees/IronClaude/bs346-minfix/.dev/brainstorms/346-minfix/nested/adversarial-1/adversarial/variant-2-sonnet-analyzer.md`.
- **C**: `/home/coder/workspaces/worktrees/IronClaude/bs346-minfix/.dev/brainstorms/346-minfix/nested/adversarial-1/adversarial/variant-3-haiku-backend.md`.
- **P**: `/home/coder/workspaces/worktrees/IronClaude/bs346-minfix/src/superclaude/commands/spec-panel.md`.
- **AB**: `/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase4/AB-REPORT.md`.
- **ARM**: `/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase4/ARMB-REPORT.md`.
- **D1**: `/home/coder/workspaces/worktrees/IronClaude/exp346-ab-flg-r2/.dev/orca-command-refactor/review/disposition.md`.
- **D2**: `/home/coder/workspaces/worktrees/IronClaude/exp346-ab-flg-r2/.dev/orca-command-refactor/review/disposition-round2.md`.
- **R1**: `/home/coder/workspaces/worktrees/IronClaude/exp346-ab-flg-r2/.dev/orca-command-refactor/review/spec-panel.md`.
- **R2**: `/home/coder/workspaces/worktrees/IronClaude/exp346-ab-flg-r2/.dev/orca-command-refactor/review/spec-panel-round2.md`.
- **R3**: `/home/coder/workspaces/worktrees/IronClaude/exp346-ab-flg-r2/.dev/orca-command-refactor/review/spec-panel-round3.md`.
- **Q3**: `/home/coder/workspaces/worktrees/IronClaude/exp346-ab-flg-r1/.dev/orca-command-refactor/review/spec-panel-round3.md`.

1. **An admission contract, not a fuzzy attribution score.** C §2 Step 3 says “Compare the reconstruction with the supplied candidate byte-for-byte” and “even formatting churn fails” (C:90). A instead allows substring matching in either direction and splits words among matching ids (A:208–210); B uses normalized old quotes and a ten-word new-text prefix (B:159,164–166). C therefore has a concrete, testable invariant: accepted candidate bytes equal baseline bytes plus exactly the registered edits. It does not establish that the owner finding actually warrants the edit; C explicitly reserves semantic adequacy for review (C:88,128,334).

2. **The reviewer bounds the write scope before the reviser acts.** Exact unique quotes become baseline byte ranges at freeze time (C:45–47); every edit must stay inside its owner's target (C:90). The report identity includes its raw hash, not merely a reusable F1 label (C:43). This matters because the real revisions propagate findings into many statements, including extra related fixes (D2:13,19–24). C distinguishes an intended propagation from a reviser silently broadening the target; it may reject necessary propagation, but cannot quietly authorize it through a loose match.

3. **Replay and retry preserve evidence.** “Existing state with exactly the same inputs is an idempotent success; different contents are a conflict” (C §2 Step 1, line 47). A cut-down reconstructs from the same baseline, not the failed candidate (C:96); identical inputs produce byte-identical results, and checks do not mutate review counts or source files (C §4, line 271). This is a better recovery contract than turning an altered baseline into a new starting point. Hashes detect changes only relative to the independent pin; they are not proof against a coordinator controlling all inputs (C:49).

4. **No multiplying allowance by multiple labels.** C assigns each edit one owner; links can show that it answers another finding but cannot pool budget (C:62,88). A divides a site's words among k ids (A:210), and B allows two ids with equal splitting (B:159). C's rule gives a shared F2/F3/F4 mechanism one chargeable owner instead of extra room merely because it answers three findings; the real run explicitly chose one shared mechanism (D1:77).

5. **Authorization is separate from editing.** “The reviser can request but cannot grant an override” (C §2 Step 5, line 102). The grant is tied to the exact edit digest and cannot change scope, grade, minor status or cycle cap (C:122). That is a meaningful contract boundary beyond B's reviser-authored reason of ten words (B:178). The truth of the approval remains trusted coordinator behavior, not cryptographic proof of user consent (C:122,339).

6. **Failed accounting does not consume scarce semantic reviews.** Only a current exit 0 admits re-review; missing or stale inputs stop rather than degrade (C:126). This directly respects the scarce three-review limit in P:261. It is stricter than A's continue-without-checker path (A:109,174) and B's stale/missing-receipt continuation (B:110). Semantic review still independently checks the wrong outcome: “budget_ok is not semantic PASS” (C:128).

7. **Growth has an actual byte bound.** With two cycle caps of 6,144 gross added bytes, maximum accepted net addition is 12,288 bytes, about 21.3% of the 57,763-byte starting document (C:62,317; AB:6). Unlike word-to-byte estimates, this directly bounds the byte-growth metric. It is not convergence evidence: AB:19–25 already shows 29.7% growth without meeting the proxy bar; ARM:20–26 repeats that separation.

8. **Operational failures are first-class results.** C separately defines malformed input, stale pins, failed output writes and unexpected failure; a report-write failure cannot emit usable acceptance (C:259–271). Its proposed tests include interrupted freeze/retry, output aliasing, duplicate JSON keys, UTF-8 boundaries and stale receipts (C:275). These are appropriate boundary tests for the proposed file protocol, not claims of tests already passing. C also requires a fresh worker to execute valid and invalid fixtures, not merely read a command (C:289); AB:45–47 independently explains why personal installation delivery must be tested on this machine.

## Weaknesses in A

1. **A detects breaches but does not consistently deny admission.** Its re-review continues on input error or crash (A:109,174); unattributed sites are reviewed normally rather than treated as blocking process failures (A:67). Its own enforcement table concedes “one review spent on an over-budget fix” (A:365). That is not a complete mechanical admission gate under the three-review constraint (P:261). C's fail-closed rule is the stronger API contract (C:126,262–267).

2. **Its trust anchor is editable and its attribution can dilute a charge.** A admits “nothing hashes” the report and that altering its class line is a residual risk (A:351); its matcher divides words between matching ids (A:208–212). Neither guarantees that a site's full cost stays with one authorized obligation. C's pinned report/state and single-owner accounting directly address those weaknesses (C:43–49,62,90). This is a correctness advantage even for accidental edits; no hostile reviser need be assumed.

3. **The 40-word calibration is not settled.** A's median 38 words for flg-r2 cycle 1 and 44–77% unattributed upper-bound estimate (A:26) coexist with B's 13 blocking fixes all at least 58 words and 260 untagged words (B:24–29). Those methods cannot be treated as the same per-finding measurement. I have verified disposition coverage (D1:16–39), not independently recounted its spans. A's 40-word cap and claim that 62–79% fit therefore need a common counting/replay method before being accepted as calibrated. C's 60 is uncalibrated too; declaring that is more honest, not evidence that 60 is optimal (C:62).

4. **Word ceilings do not prove a byte-growth ceiling.** A's approximate 16% ceiling uses added words divided by starting words while labeling the growth metric bytes (A:314). Very long identifiers or multibyte words need not retain the historical bytes-per-word ratio. C measures gross UTF-8 insertion bytes directly (C:210,317). A's estimate remains a useful forecast, not a hard byte guarantee.

## Weaknesses in B

1. **Its minor-edit allowance contradicts a strict minimal-fix contract.** B permits 12 words per minor, 36 per cycle (B:176–178), while telling disposition rows to say “budget 0” (B:133,284). The real loop's F22 was explicitly non-blocking (R1:63–65), was edited (D1:37), and spawned a new check defect (R2:48). B's bounded correction might avoid that particular chain (B:233), but that counterfactual is not observed evidence. Zero edits is a simpler rule and matches P:259's “minor findings are notes and never trigger a revision.”

2. **Self-granted exceptions weaken the very budget being tested.** Up to two reviser-written override reasons double limits; reviewer `large` flags provide further doubled limits without using those overrides (B:128,178). The syntax is mechanically checkable, but the reviser can expand its own allowance by describing the work as a contradiction. C separates request from authorization and pins the exact edits (C:102,122). A's reviewer-only grant is also better than self-authorization (A:78).

3. **Automatic rollback acts on approximate matching.** B normalizes emphasis/whitespace, accepts a unique 40-character fragment and new-text prefix, and treats moved units as free (B:159,164–166). It then reconstructs an in-place result by reverting failing hunks (B:211). Atomic replacement prevents a torn file, but does not prove the right text was selected or the kept edits are independent. C never lets its checker rewrite the document and checks exact candidate reconstruction instead (C:90,94). Partial-admission semantic dependencies remain a concession for C too.

4. **B does not mechanically enforce named scope.** Its `named` flag is “Informational, never failing” (B:168). A reviser can accurately ledger an edit not actually named by the blocker, receive a warning, and still pass numerical accounting. C registers targets before dispatch and rejects out-of-target edits (C:45–47,90). This is a narrower and more testable interpretation of P:263.

5. **B's failure table softens the actual experimental bar.** It calls means 3.5–4.5 promising and suggests more replicates (B:425), although ARM:23–26 says a mean of 3.5 was not proven. More data can be reasonable research; it is not this screen succeeding. B:426 also labels mean/each ≤3 plus growth and validity “Bar met” without rechecking the spread condition that B:378 itself requires. C explicitly retains all three comparisons in its falsifier (C:319,345).

6. **Its hard-gate handling needs correction.** B's final open question allows an FR-8/FR-9 GAP graded minor to receive minor budget (B:481). That reflects observed grader inconsistency, not the actual rule: P:259 says FR-8/FR-9 findings are blocking; R1:63 gives an observed contrary F22 grade. A checker should surface that disagreement rather than silently encode the inconsistent grade. C's structural rule requires a hard-gate finding to be blocking (C:43).

## Concessions

1. **C's coordinator gap is a blocking design defect for the proposed experiment.** C requires freeze before dispatch and coordinator check/promotion afterward (C:47–49,94,271), yet says unchanged briefs plus a review-command substitution deliver those duties (C:126,282–285,297). An instruction loaded by a dispatched reviewing worker does not itself dispatch work in the parent. P:261's existing coordinator responsibilities do not include this new contract. Prefer A's reviewer/reviser-local delivery for this point (A:37–42), or explicitly authorize and test new coordinator instructions; the latter is an additional treatment change, not a one-line-only experiment. C's claimed delivery must not be accepted on prose alone.

2. **Withdraw confidence in C's 1/1 proxy forecast.** C labels it UNVERIFIED but provides no derivation (C:309–319); it also calls smaller-text causation the main unanswered question (C:352). B supplies a counterweight: fix size did not separate child-producing fixes in its small sample (B:77–87). The defensible claim is that C should bound growth and expose rejected work; its chance of getting the proxy to ≤3 is unknown. B's assumed-probability derivation is a better sensitivity analysis, though not a validated prediction (B:403–409).

3. **C's strict machine contract can prevent useful fixes.** Unique quotes, UTF-8 byte offsets and exact equality avoid ambiguous matching but increase authoring errors (C:45,81,90,340). A 60-word/512-byte budget plus 120-word removal cap can reject a correct multi-site repair; C acknowledges under-fixing and destructive deletion (C:331,335,338). It has no replay-based false-breach measurement. Prefer B's common-method replay before fixing the initial constants (B:479), not informal assurances that most cuts will fit.

4. **Partial admission is not semantic atomicity.** C lets valid edits remain while other obligations escalate (C:96,98). A/B do something similar (A:62; B:211). R2:28,37 directly shows the F2 path rule interacting with F11 placement, so a whole-finding rollback need not preserve cross-finding consistency. C's single-owner links solve accounting, not a dependency graph. A selected design must either reject the whole coupled change set or have independent review check the retained combination; this is a required correction, not existing implemented behavior.

5. **C has a growth guarantee, not an obligation-preservation proof.** Its removal cap limits destructive rewrites but does not prove that deletion preserves required behavior (C:338). Reviewer targets can themselves be overbroad (C:334); a tiny wrong replacement can still create CRITICAL defects (C:134). Hashes establish input continuity, not truth, minimality, valid approval provenance or correct severity (C:139).

6. **The proxy can count notes that the budget intentionally leaves alone.** ARM:13–14 records six critical/major findings but four blockers in flg-r1 R3; ARM:37 explicitly attributes the difference to MAJOR findings graded minor. Zero edits must not be marketed as removing those findings from a severity-count metric. C records proxy and actual blocking separately (C:302), but does not justify assuming deferred MAJOR notes vanish. The primary tally must retain them when open/reported under the pre-registered counting rule, even if the review verdict permits minor notes.

7. **C expands the implementation and has packaging risks still to verify.** C adds mirrors, a design document, strict input checks and richer exit states (C:149–160,195–216,259–275), while A/B offer smaller file sets (A:140–149; B:239–248). Its current-command copy is a poorer controlled-experiment base than B's exact 427 text; ARM:6 confirms the historical 472-line command differs from the restored 486-line machine version. C's preserved Unattended section also needs the enumeration-test check A identifies (A:162); that test was not independently read here, so it is a reported integration risk, not a verified failure. C §4's table actually names nine files when both mirror rows are expanded (C:149–156); the diff summary's “7” is not an authoritative count.

8. **Costs are estimates, and C does not eliminate skipped execution.** C estimates roughly 10 calls normally, 18–22 with retries, and human escalation can wait indefinitely (C:325–327). Its coordinator can still skip the checker (C:137,342). A runtime receipt proves an invoked check on particular bytes, not an operating-system security barrier or a demonstrated convergence benefit. Keep the proposed valid/invalid fresh-worker probe and measured cost logging; do not claim tests, packaging or runtime performance have already passed (C:275,289,327).

## Per-point positions table

“Preferred” selects the best approach on that specific point, not an assertion that the entire selected variant works unchanged. Equal shared structure still receives the required explicit choice. There are 51 positions: seven structural, thirty content and fourteen contradictions.

| id | preferred | reason |
|---|---|---|
| S-001 | C | Same eight-section order; C leads with a concrete admission invariant rather than additional machinery (C:3–5,20,130,141,277,295,323,349). Structural tie, C's opening is clearer. |
| S-002 | C | C's steps and inline schemas give a compact contract organization (C:20–128); B's many subsections are more useful for evidence than operating instructions (B:100–214). |
| S-003 | B | Cap replay, chain classes and negative predictors make the evidence auditable, unlike C's report-level calibration (B:63–98; C:9–16,62). |
| S-004 | C | Freeze → budget → ledger → check → authorization → re-review exposes state transitions in operational order (C:22–128); its actor-delivery defect remains X-012. |
| S-005 | A | Per-artifact changes plus derivation pins make additive implementation scope easy to inspect, without C's extra mirrors/document (A:140–162,246–252; C:149–156). |
| S-006 | B | Separating growth arithmetic from proxy sensitivity shows what is measured versus assumed (B:387–409); C's proxy table has no derivation (C:313). |
| S-007 | B | Detection/mitigation/residual columns operationalize risks and expose ownership problems (B:444–456); C's two-column table is candid but less diagnostic (C:329–343). |
| C-001 | C | All findings and explicit severity/blocking/hard-gate fields permit structural validation; classes are derived rather than selected by the reviser (C:24–53). |
| C-002 | B | For the initial MAJOR word allowance, prefer replay-informed 80 over uncalibrated 60 or contested 40; 13/17 exceeded 60 in B's stated method (B:89–98; C:62). Still requires independent replay. |
| C-003 | C | C retains 120 gross words but also bounds bytes and removals, which better contains destructive or long-token rewrites (C:55–60,210). |
| C-004 | C | Explicit zero edits and one deferred disposition per non-blocker avoid B's 12-versus-0 ambiguity (C:57,88; B:133,176). |
| C-005 | C | A fixed gross word/byte cycle ceiling includes overrides and cannot be purchased by unrelated deletion (C:62); A has no independent cycle cap (A:73–82). |
| C-006 | A | The condition-word tripwire directly targets added guards and has a stated causal trace; retain its heuristic limitation rather than call it semantic proof (A:31,80,129). |
| C-007 | C | One strict JSON object binds every disposition and exact edit to frozen state; duplicate keys and absent coverage fail explicitly (C:68–90,195). |
| C-008 | C | Unique registered target ranges plus byte reconstruction avoid fuzzy substring matching and budget splitting (C:45,90; A:208–212; B:159,166). |
| C-009 | C | Exclusive idempotent freeze and an independently pinned state hash detect stale/tampered evidence instead of trusting an editable baseline (C:47–49). |
| C-010 | A | A's neutral `fix-budget` name makes command/helper distinction explicit and explains the installer concern (A:151). Installer behavior was not independently checked here; no claim that C's protocol suffix is actually swept. |
| C-011 | C | Two operations with explicit input paths and paired authorization pins are easier to bound than B's mutation-capable five-operation API (C:189–204; B:303–318). |
| C-012 | C | Stable JSON plus separate input/hash/output/internal failure states gives callers actionable errors without accidental acceptance (C:218,257–271). |
| C-013 | C | Rebuild one cut-down from the original baseline; on another failure retain the accepted document, not a script-mutated approximation (C:94–98). Partial-success semantic coupling still needs correction. |
| C-014 | C | One externally authorized grant bound to exact edits is more accountable than reviser-authored doubling (C:102–122; B:178). |
| C-015 | C | FR-8/FR-9 remain blocking but do not automatically earn larger edits; authorization needs a concrete necessity (C:43,53,102; P:259). |
| C-016 | C | Amend bullet 6 and append admission to bullet 5 while retaining seven bullets, rather than B's eighth bullet (C:164–182; B:252–259). |
| C-017 | C | External attribution avoids growing normative text; every changed byte still counts rather than making citation annotations free (C:90,210; B:165). |
| C-018 | B | Verify receipts by recomputation and expose only numerical/line-map evidence; keeping reasons out avoids unnecessary anchoring (B:111,318,477; R3:27). |
| C-019 | C | Missing/malformed/stale evidence halts admission, matching the no-silent-fallback principle already present in P:258 (C:126). |
| C-020 | C | A fresh-worker valid/invalid execution probe tests actual delivery, beyond logging copied hashes (C:287–291; AB:45–47). |
| C-021 | C | Literal invocation-token replacement is unambiguous about preserving flags and not rewriting similarly named commands (C:281–285); exact resulting briefs must still be inspected. |
| C-022 | A | Reviewer-local saving and reviser-local checks reach actors through the existing report channel; C's new parent duties have no demonstrated dispatch route (A:37–42; C:47,94,126). |
| C-023 | B | Use the exact historical 427 text for the installed experiment and current source only for the repository artifact (B:362); ARM:6 confirms these are different bases. |
| C-024 | B | Assumption-labeled transition sensitivity is preferable to C's unexplained 1/1 forecast (B:403–409; C:313,352), though neither establishes actual success probability. |
| C-025 | C | Its 21.3% bound follows directly from gross byte caps, unlike converting capped word growth into byte-growth ceilings (C:317; A:314; B:392). The 15% forecast remains unverified. |
| C-026 | C | Preserve proxy ≤3, every-control and spread conditions; no-growth/all-escalation outcomes cannot masquerade as convergence (C:319–321,345; ARM:23–26). |
| C-027 | B | The per-role tool-call table is the most inspectable cost breakdown, including cut-down work (B:434–440). All variants' timing remains estimated (C:325–327). |
| C-028 | C | Keep later adoption separate and do not inherit the three-review count or widen implementation criteria (C:293,356), rather than designing new adapter options now (B:342). |
| C-029 | B | Child-chain analysis and cap replay provide a stronger starting calibration than report-level growth or incompatible span-attribution estimates (B:22–98; A:26; C:62). Measurements need independent reproduction. |
| C-030 | C | Runtime integrity tests cover interrupted preparation, UTF-8, tampering and unsafe outputs, essential for C's proposed contract (C:275). Its full file set is larger than needed and should be bounded during planning (C:149–156). |
| X-001 | C | Zero edits is an unequivocal non-blocker rule; B's small allowance changes known minor text into new review surface (C:57,62; B:176–178; R2:48). |
| X-002 | C | Seven bullets are preserved with an explicit external-ledger amendment, not a contradictory additional bullet layered over old inline attribution (C:167–182; B:254–259; P:263). |
| X-003 | C | Put finding ownership in the external ledger without a free-word exemption for annotations (C:90,167,210); B excludes such tags (B:165). |
| X-004 | C | Define nonzero categories, canonical status and output-failure behavior so automation never mistakes a missing receipt for acceptance (C:257–271). Exact integer choices are conventions, not inherent quality. |
| X-005 | C | A checker should validate, not automatically overwrite candidate bytes selected through heuristic hunks (C:94,271; B:164–166,211). Keep the last accepted document recoverable. |
| X-006 | C | Separate authority from the reviser and invalidate approval if the edit changes (C:102,122), rather than accept a self-written override reason (B:178). |
| X-007 | C | A stale/missing physical input stops admission; degraded checking is not the promised mechanical gate (C:126; A:174; B:110). |
| X-008 | B | Keep ledger reasons out of the next review; actual wrong outcomes and computed spans suffice (B:111,477). Real R3 explicitly judged spec text rather than dispositions (R3:27). |
| X-009 | C | Bound removals because an unrestricted deletion can discard required behavior; the cap contains damage without proving semantic preservation (C:58–59,210,338). |
| X-010 | B | Prefer B's explicit whole-fix attribution and sensitivity table for calibration, not A's id-bearing-sentence lower coverage (B:24–29,89–98; A:26). Neither count was independently recomputed here. |
| X-011 | B | Negative predictor evidence defeats a confident size→convergence claim; smaller fixes can still follow a wrong recommendation (B:77–87; R2:36; C:352). |
| X-012 | A | A actually assigns new work to the command-loaded reviewer and report-reading reviser; C's convention alone cannot instruct the parent coordinator (A:37–42; C:126,285). |
| X-013 | C | A proxy mean above 3 fails this screen, even if further research might be worthwhile; retain the spread comparison too (C:319,345; B:425–426; ARM:23–26). |
| X-014 | B | Match the exact 472-line comparator for causal isolation, rather than C's current-command copy (B:362; C:149; ARM:6). |

## Shared assumption responses

| id | response | evidence and consequence |
|---|---|---|
| A-001 | QUALIFY | Reject an untested claim that regex sentence boundaries are reliable enough for enforcement. A splits after punctuation and B normalizes/splits cells and sentences (A:198–199; B:164), while the real second revision added 6,073 bytes with only one extra line (D2:57). C avoids that particular parser assumption through unique exact anchors and byte reconstruction (C:45,90), but transfers failure risk to quote uniqueness and reviser offsets (C:340). Accept sub-line accounting only with executable fixtures for tables, punctuation in code/paths, repeated quotes, Unicode boundaries and the real long-line documents; C:275 proposes several, not a proven false-breach rate. |
| A-002 | REJECT | Partial admission is not automatically safe. R2:28,37 directly ties the new relative-path defect to F2's table and F11's separate placement rule; B:48 independently identifies that interaction. Reverting a whole finding is not reverting all dependent semantics (B:211), and C's “Valid edits may remain” has the same gap (C:96). Before admitting a partially retained candidate, the contract must preserve coupled changes together or require an independent consistency check of the retained combination. Accounting links alone do not establish this. |
| A-003 | REJECT | A severity proxy cannot silently exclude a deferred non-blocking MAJOR. ARM:13–14,37 reports six critical/major versus four blocking findings in flg-r1 R3. R1:63–65 is a concrete MAJOR/non-blocking F22; P:260 permits minor notes in a semantic PASS but does not redefine a severity tally. Count severity and actual blocking separately as C:302 requires, preserve terminal obligations under C:321, and do not assume zero edits mechanically lowers the primary proxy. The exact pre-registered rule for carried/re-listed notes must be fixed before treatment results, not adjusted to make the budget win. |
| A-004 | REJECT | One cut-down is a cost/termination policy, not evidence that models usually meet a numerical cap after it. B's replay has 11/17 MAJOR fixes above even 80 words (B:98), yet predicts only 1–3 escalations (B:412); A predicts the same order (A:319). No reviewed ground-truth report demonstrates a budget-driven retry, so there is no observed retry-success rate. Keep the single-attempt bound (C:96), measure first/second-check outcomes and escalated obligations (C:307), and treat high escalation as failure to demonstrate convergence, not low-growth success (C:321,345). |

**Decision for the merge:** select C's exact, fail-closed accounting core, but do not authorize an experiment from C unchanged. Resolve the coordinator delivery gap using A's actor-local approach, use B's comparator-matched build and replay method, and withdraw the unsupported 1/1 forecast; those changes matter because the verified reports already show that low growth and resolved parent findings can coexist with a failed final proxy (ARM:13–26; R3:15,35).

**Scope and remaining risk:** only this debate file was created; no code, Git, installation or network work was performed. Runtime correctness, per-finding recounts, packaging behavior, checker cost and actual convergence remain untested.
