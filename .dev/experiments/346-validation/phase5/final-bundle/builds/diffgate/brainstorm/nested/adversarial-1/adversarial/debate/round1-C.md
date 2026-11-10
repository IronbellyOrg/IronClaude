## Position summary

Variant C is the strongest acceptance-safety foundation because it checks both review anchors and preapproved repair footprints, preserves genuine fix-induced blockers, and stops rather than converting a twice-invalid report into a successful review (C sections 3-5). It is not ready unchanged: adopt A's regression-test integration and all-discovered primary metric, add A's independent blindness audit, and treat B's conservative forecast as better supported than C's optimistic forecast (A sections 8.6 and 9; B section 9; diff-analysis X-008, X-012 and X-017).

Citation key: A means `variant-1-opus-architect.md`, B means `variant-2-sonnet-refactorer.md`, C means `variant-3-haiku-qa.md`, and DA means `diff-analysis.md`, all in the supplied adversarial directory. These are proposal claims, not executed results. DA's Fact check says the experiment evidence is outside this working tree and its figures are unverified here; I therefore use the reported F22/N5/N12 sequence as a design example, not independently established causal evidence. Repository checks below are limited to the specific source excerpts read during this debate.

## Steelman of Variant A

A attacks the actual granularity problem rather than merely renaming scope rules. Its section 3.1 says S1 uses approximately 240-byte paragraph lines, and its section 3.5 computes changed tokens within changed lines. That is a persuasive way to prevent a one-word correction from reopening an entire paragraph, with a concrete test oracle in section 8.4: "One changed word in a 300-character line" produces a changed span containing that word.

A also has the most complete integration reconnaissance. Section 8.6 identifies the shipped-command inventory and unattended-section set checks, and DA's Fact check confirms both. Its section 9 counts deferred and demoted labels in the primary proxy and requires a fresh final-document blindness audit. Those choices directly test whether apparent convergence is just suppressed reporting. Section 4.4's replay of accepted reports is a useful consistency check, although not a security boundary against an owner able to replace every artifact.

The strongest case for A is therefore a small reviewer-facing change with precise eligibility and measurable blindness, not a claim that token matching proves semantic correctness. A itself admits anchor gaming, id gaming, and false PASS from demotion in section 10.

## Steelman of Variant B

B provides the best skeptical account of the proposed causal mechanism. Its section 1 replay says the last review's five items become two while "blocking 1 to 1" stays unchanged. Unlike an optimistic surface-size argument, this explicitly distinguishes removing noise from fixing the defect-generation rate. Its section 9 F1 asks whether high remaining counts on mapped fix hunks show that scope is the wrong lever.

B's explicit sidecar fix map is clearer and less intrusive than A's implicit mapping through document ids or deleted quotes (B section 5.2; A V2). B also anticipates wrong-directory resets with `--expect-round`, records fix chains, and proposes independently revertible inert and experiment stages (sections 2, 5.3 and 8). These are strong operational and regression-risk choices. B section 12 honestly identifies worker permissions as an experiment-blocking uncertainty and admits that the worse replicate's finding composition has not been read.

The strongest case for B is a cheaper, observable experiment that may correctly fail its success bar. Its cautious forecast and explicit alternatives to the scope hypothesis are strengths, not lack of advocacy (B sections 1 and 9).

## Key strengths claimed

1. **C distinguishes invalid evidence from a valid negative review.** Section 4 says, "A second reject marks the run invalid," preserves diagnostics, and prohibits another fix cycle. Section 3 explicitly separates operation success from the review verdict. P0 state tests then require that persistence failures and invalid drafts never produce PASS (section 13). This is a testable acceptance property, not simply the word "fail-closed."

2. **C checks where a repair may occur, not merely which id it claims.** Section 3 requires each actual edit group to have exactly one open blocking owner and fit a footprint approved before editing. Coupled sites must be listed beforehand. Section 13 tests undeclared sibling edits, minor-owned spelling corrections, boundary insertions, and merged adjacent fixes. A valid id on an unrelated distant change is insufficient under C, whereas A V2 and B F1 lack this coordinate-containment requirement. C section 5 correctly concedes that a semantically unrelated change inside an approved footprint can still pass mechanical checks.

3. **C does not confuse an outcome string with confirmed harm.** Section 4 requires a coordinator-confirmed concrete wrong implementer outcome: "A nonempty outcome string is necessary but not sufficient." Section 3 pins confirmation to the draft and surface digests. The manual semantic cases in section 13 contrast a real changed-rule dependency with an unrelated complaint quoting the same changed line. This does not automate semantics; it makes responsibility and observed acceptance evidence explicit.

4. **C has the strongest deletion and context boundary oracles.** Section 3 gives deletions an exact old-side quote and a current insertion-boundary repair footprint. Section 13 tests both a genuine lost-rule finding and a deleted line falsely claimed as current. It separately rejects unchanged context inside an otherwise valid hunk. Those cases directly cover boundary errors that a broad hunk-membership check can miss.

5. **C preserves the hard case rather than purchasing convergence with a severity ceiling.** Section 5 states that new defects introduced by authorized fixes "are not capped to minor" and that the cap guarantees termination, not correctness. Section 13's complete stubbed chain ends with an R3 child still open, followed by refusal of a fourth review or third fix. This is a concrete regression test for the very failure the proposal must not hide.

6. **C makes release criteria and operational failures inspectable.** Sections 13-14 cover strict JSON duplicate keys, zero findings, stale ids, all-anchor validation, report-copy hashes, isolated HOME installation, original-command preservation, lock contention, crash recovery, and resource limits. Section 8 also removes the copied package-only template lookup, unlike A's and B's copy-preservation promises. The source excerpt at `/home/coder/workspaces/worktrees/IronClaude/bs346-diffgate/src/superclaude/commands/spec-panel.md`, under `## Tool Coordination`, confirms that lookup exists.

7. **C limits what a successful experiment may mean.** Sections 6 and 9 say scoped PASS is not permission to ship, call historical controls historical, require the effect to exceed observed spread, and carry early-PASS bytes forward without an extra repair. Section 10 prices coordinator Read-backs and rejected reports rather than describing helper runtime as the whole cost. The metric ambiguity discussed below must be fixed before these safeguards support a valid comparison.

## Weaknesses identified in Variant A

1. **Demotion can turn an evidence failure into a misleading scoped PASS.** A section 4.3 sends twice-invalid new findings to `deferred: unanchored`; section 10 explicitly names "False PASS from demotion." Counting demotions in the experiment proxy is useful but does not repair the operational acceptance signal. C section 4's invalid termination is safer for the seed's demand that enforcement be mechanical, with a measured cost for unusable output.

2. **A's fix gate authorizes labels, not bounded repairs.** V2 accepts a hunk if added text carries a blocking id or removed words overlap a finding quote. Section 10 acknowledges that "A valid id pasted onto an unrelated edit passes the gate." The fact that the next reviewer sees it once does not prevent unnecessary growth or fix-induced defects. C's preapproved footprints reduce this concrete escape without claiming semantic minimality (C sections 3 and 5).

3. **Report replay is not independent confirmation.** A section 4.4 recomputes syntax, anchor membership and arithmetic from the recorded report. A section 7 still leaves the truth of the outcome and resolution to reviewer judgment. C sections 3-4 add a separate coordinator decision and test its exact draft binding. That separation costs more, but it checks a different failure mode than replaying the same formal inputs.

4. **A's copy rule contradicts its own portability test.** Section 8.1 promises a byte copy with only the enumerated changes and "Nothing else changes," while section 8.5 forbids the package-source string. DA X-015 identifies the existing template lookup; the source excerpt read here confirms it. C section 8 explicitly removes it. A's strongest integration work does not excuse this independently failing acceptance condition.

5. **Token precision is not enough evidence for the forecast.** A section 9 scales fix rows and predicts mean proxy 2.0, while section 5 admits missed defects on closed fix text will not reopen. DA A-002 and A-006 identify unmeasured density and replicate-composition assumptions. Keep A's token-level experiment and blindness audit, but do not treat its probability estimates or smaller surface as demonstrated quality improvement.

## Weaknesses identified in Variant B

1. **"Degrades fail-safe" is safe against one error direction, not all of them.** B section 4 tier 3 moves malformed finding-level claims to deferred and returns exit 0. That prevents unanchored blockers, but can remove a real changed-line blocker from acceptance. B's own section 12 question 7 acknowledges the trade. C stops invalid instead, preserving the distinction between malformed evidence and no blocker.

2. **Merged hunk ranges permit unrelated unchanged anchors.** B section 3 merges candidate hunks separated by up to two lines; C6 then checks whether the cited range lies inside the reviewable hunk range. A gap line inside that merged range can therefore become eligible even though it did not change. C section 3 explicitly says context lines never become eligible merely by sharing a hunk, and section 13 tests that condition. B's pure-deletion policy, which permits neighboring current lines, also needs C's explicit old-side loss evidence to avoid confusing absence with current text.

3. **The `via` quota bounds discovery rather than harm.** B C11 accepts at most two dependency findings through unchanged text, and section 12 admits that number is a guess. If three real changed-rule regressions exist, the third should not cease blocking because it is third. C section 7 keeps the changed cause as the primary anchor and requires dependency confirmation without a discovery quota. That still permits unchanged context to explain the consequence.

4. **A sidecar map without containment still permits id laundering.** B F1-F3 validate ownership labels and coverage, and section 10 R5 concedes that an unrelated edit can map to a blocker. The 1,500-byte advisory warning cannot reject that edit and is explicitly uncalibrated (sections 5.2 and 12). C's footprints are the stronger mechanical check; B's warning can remain optional observability, not a substitute for authorization.

5. **The claimed minimal transformation has two confirmed integration holes.** B section 8.4 refuses routing-test edits, but DA X-012 and the read shipped-command equality show that adding the command requires inventory accommodation. B section 8.1 preserves all untouched sections while section 8.3 prohibits package-source references; DA X-016 and the copied template lookup make both promises incompatible. B's drift guard is valuable after the legitimate exception is explicitly specified.

6. **The worked replay is useful but internally overprecise.** B section 1 assigns the line carrying both N1 and N11 to the minor group, yet F1 permits its blocking N1 owner. DA X-018 correctly points out that the claimed 13 allowed lines becomes 14 under B's stated rule. The replay supports a qualitative noise reduction hypothesis, not the exact line ratio used in the forecast.

## Concessions (genuine weaknesses of Variant C)

1. **C cannot meet its own regression promise without changing existing tests.** Section 8 forbids edits to the routing and worker-contract surfaces, while sections 13-14 require their regression checks to pass. The read excerpts at `/home/coder/workspaces/worktrees/IronClaude/bs346-diffgate/tests/recommend/test_routing_refresh.py` show shipped commands must match the active inventory after enumerated exclusions. The read `/home/coder/workspaces/worktrees/IronClaude/bs346-diffgate/tests/skills/test_worker_contract.py` helper requires exact equality of unattended-section names. A new command with that heading violates both expectations. Accept A's explicit variant registration approach, but adapt its unattended assertions to C's intentionally changed failure semantics rather than requiring byte identity (DA X-012 and X-017; A section 8.6; C section 8).

2. **C's bar metric is ambiguous and must lose to A+B's definition.** C section 9 says it retains the original proxy rule, but labels the bar "Open CRITICAL+MAJOR proxy" and separates deferred claims into another count. DA X-008 identifies a real ambiguity, not a wording preference. Pre-register all-discovered critical+major, including deferred and rejected/demoted proposed labels as applicable, as the comparison metric; report scoped effective blocking separately. Do not claim an early clean PASS solely because severe discovered claims were moved out of scope (A section 9; B section 9).

3. **C lacks an independent blindness audit.** Raw drafts and ancestry cannot reveal a defect no reviewer recorded. A section 9's fresh final-document review, classified into original and fix-written text, is superior for that failure. Add it as an out-of-loop observation, with no automatic new fix cycle; C section 13's semantic fixtures do not replace it.

4. **C's optimistic forecast has weak support.** The proposed 1 and 2 proxies in section 9 are expressly "hypotheses, not calibrated estimates." Neither the unexamined worse replicate nor the possibility of denser findings on fewer lines supports that precision (DA A-002 and A-006). B's lower-confidence forecast and wrong-lever condition are better choices until composition and actual runs are examined. All historical experimental counts remain unverified in this checkout (DA Fact check).

5. **Strictness adds real failure modes and under-fixing risk.** C section 10 admits adjacent legitimate fixes can merge into a rejected mixed-owner group and valid structural repairs can expand the surface. Sections 3 and 10 add more state, coordinator confirmations and roughly 5-13 minutes of estimated overhead. Footprint rejection must be measured alongside unresolved priors, not congratulated as scope control when a correct repair cannot be expressed (C section 12 question 3; DA A-003).

6. **C's line-level policy leaves large paragraph surface and whitespace blindness.** A section 3.1's one-paragraph-per-line observation challenges C's precision. C section 10 explicitly says ignoring spaces and tabs can hide indentation, shell-argument and Markdown changes. C's raw-edit ownership is stronger than silently ignoring those edits, but it does not make them eligible blockers. Test semantic whitespace fixtures and report that limitation, rather than claiming general document correctness (C sections 3, 10 and 13).

7. **C overstates the plugin rationale and mixes two acceptance layers.** DA's Fact check contradicts C's description of existing plugin drift as one word, and DA confirms parity is not mandatory for every new command. A+B's source-only experimental delivery is smaller unless plugin runtime is explicitly in scope. Also C section 14 calls implementation acceptance separate from experiment success but includes the S1 screen as criterion 15; split those gates clearly. C section 8's removal of the source-only lookup remains necessary regardless of whether mirrors ship.

8. **No actor-placement choice creates an unskippable harness.** C section 7 admits the coordinator may omit the helper, while A section 2 and B section 2 admit wrong-directory resets. C's confirmation file checks presence, not truth (section 3). Require transcript evidence, wrong-directory and nonzero-exit recovery probes, and disclose invalid runs and costs rather than claiming a sandbox. B section 12's worker-permission smoke preflight should also be retained.

## Shared assumptions

A-001: QUALIFY: Recovery compliance is an acceptance condition to observe, not a property conferred by exit codes; exercise nonzero exits, stale state and attempted directory resets, then require matching transcript and ledger evidence (C sections 4 and 13; DA A-001).
A-002: REJECT: Smaller scope does not logically imply fewer real findings; record findings per eligible line or token alongside distinct defects, deferred counts and the independent blindness audit before attributing a gain to narrowing (A section 9; B section 1; DA A-002).
A-003: QUALIFY: Blocking-only ownership can reduce gratuitous edits but also prevent valid coupled repairs; count unresolved priors, legitimate footprint/map rejections and stalls as harms, not just prevented growth (C sections 10 and 12 question 3; B F2; DA A-003).
A-004: REJECT: Added scope instructions can change behavior without enforcement, so historical comparisons identify only the combined treatment; a briefs-only arm is needed to isolate the script's contribution (C section 8 calls the step lines treatment; DA A-004).
A-005: QUALIFY: Full-document eligibility in R1 does not mean unchanged elicitation when JSON, footprints and confirmation are new; compare R1 counts, labels and formatting failure rates before using Arm B as an interchangeable baseline (C sections 3 and 9; DA A-005).
A-006: REJECT: One best replicate's ancestry cannot establish the worse replicate's composition; inspect both before defending the forecast, or label it an unsupported extrapolation as B section 12 question 12 does (DA A-006 and Fact check).

## Per-point positions

| Point | Superior approach (A, B, C, or "A+B" style merge, or "tie") | One-line reason |
|---|---|---|
| S-001 | C | Separate test and acceptance sections make review obligations easier to inspect, though criterion 15 must move to the experiment gate (C sections 13-14). |
| S-002 | C | P0 eligibility, edit ownership and crash/state oracles exceed the compact case lists, with explicit negative cases (C section 13; A 8.4; B 8.3). |
| S-003 | C | Numbered implementation criteria expose omissions independently of an optimistic forecast (C section 14). |
| S-004 | A+C | A's verbatim replacement bullets reduce implementation ambiguity; preserve C's stricter acceptance ownership within that format (A 8.1; C section 8). |
| S-005 | A+B | Named functions and a bounded outline are more actionable than C's prose outline; estimates are budgets, not proof (A 8.3; B 8.2; C section 8). |
| S-006 | A+B | Shared exit tables with an actor column are easier to test and act on than C's inline sentence (A 3.3; B section 3; C section 3). |
| S-007 | B+C | Preserve B's explicit unverified tags and C's PROPOSED labels; dense citations cannot verify absent experiment evidence (B section 1; C section 1; DA Fact check). |
| S-008 | A | Bullet-by-bullet mapping with residual risk gives the clearest trace from the existing contract to enforcement (A section 7). |
| S-009 | C | Cost envelope plus guard-and-residual table makes semantic and operational limits explicit (C section 10). |
| S-010 | B+C | B identifies setup blockers; C defines initial defaults so open questions do not silently select runtime behavior (B section 12; C section 12). |
| C-001 | C | Independent coordinator acceptance adds semantic confirmation that worker-owned script calls alone cannot provide (C sections 2-4; B section 3). |
| C-002 | C | Explicit protocol activation and complete-directory lookup reduce mixed-install risk; all three names can install (C section 3; DA Fact check). |
| C-003 | B | Four subcommands keep the user interface smaller; command count alone does not justify weakening C's confirmation semantics (B section 3; C section 3). |
| C-004 | C | Structured stdout, explanatory stderr and separate execution/verdict fields support unambiguous automation (C section 3). |
| C-005 | B+C | B's actor-action table is clearer; retain C's explicit valid-FAIL-versus-helper-failure distinction (B section 3; C section 3). |
| C-006 | C | Strict JSON, duplicate-key rejection and digest-bound confirmation avoid a second authoritative Markdown interpretation (C sections 3-4). |
| C-007 | C | Per-round artifacts, generation checks and locking support precise crash and concurrency tests despite added storage (C sections 3 and 13). |
| C-008 | A+C | A's changed-token precision targets long paragraphs; C's exact old/new eligibility and context exclusion are necessary safety constraints (A 3.5; C section 3). |
| C-009 | C | Round, content and coordinate-bound ids reject stale identical-looking hunks without relying on caller memory (C section 3). |
| C-010 | C | Checking every claimed anchor and the exact confirmation digest closes partial-validity shortcuts (C section 4 step 4; section 13). |
| C-011 | C | Twice-invalid evidence stops invalid rather than becoming a potentially false scoped PASS through deferral (C section 4; A 4.3; B section 4). |
| C-012 | C | Explicit deferred placement plus rejection of an unanchored claimed finding best matches the seed's scripted rejection criterion (C section 4; seed Success Criteria). |
| C-013 | C | Anchor the changed cause and confirm the dependency; do not hide a third genuine regression behind B's quota (C section 7; B C11). |
| C-014 | C | Preapproved coordinate footprints prevent distant unrelated changes from passing on a valid ownership label alone (C sections 3 and 5). |
| C-015 | C | Approved repair area is a defensible authorization boundary; an uncalibrated advisory byte threshold is only observability (C section 5; B 5.2). |
| C-016 | tie | All reject severity ceilings that would hide genuine last-round fix-induced defects (A section 5; B 5.4; C section 5). |
| C-017 | C | Invalid termination also discloses deferred candidates, with explicit unverified locations and scoped-PASS limits (C section 6). |
| C-018 | C | Rendering accepted records and verdict together eliminates reviewer verdict reconciliation and append-order mistakes (C section 4 step 8). |
| C-019 | C | A coordinator-confirmed wrong outcome is stronger than a nonempty or 25-character string (C section 4; A 4.1; B C12). |
| C-020 | C | Immutable outcome/grade plus footprint-intersecting regression evidence makes identity drift explicitly testable (C sections 3-4). |
| C-021 | tie | Each design excludes minor ids from repair authorization; C adds raw-edit containment as a separate advantage (A V3; B F1; C section 5). |
| C-022 | C | Preserve physical changes rather than assuming reflow is semantically inert, and require ownership even for ignored raw whitespace (C section 3). |
| C-023 | B | The conservative estimate and acknowledged surviving mapped blocker are better grounded than C's mean 1.5 forecast (B section 9; C section 9). |
| C-024 | B+C | B gives explicit assumptions and C labels forecasts uncalibrated; no proposal has measured treatment growth (B section 9; C section 9). |
| C-025 | A+B+C | Combine A's blindness failure, B's wrong-lever diagnosis and C's integrity/spread checks without metric substitution (all section 9). |
| C-026 | A+B | Count deferred severity labels in the primary proxy; keep C's scoped blocking count secondary (A section 9; B section 9; DA X-008). |
| C-027 | C | Explicitly budgeting parent Read-backs, writes and repair overhead is more complete than helper runtime alone (C section 10). |
| C-028 | B+C | Keep B's expected-round defense and C's mandatory state, installed hashes and observed Skill invocation (B section 2; C section 8). |
| C-029 | C | Supplied predecessor paths must match pinned history rather than being ignored or silently stripped (C sections 3 and 8). |
| C-030 | A+C | C supplies richer behavior/install tests; A supplies the existing inventory and unattended registration changes C missed (C section 13; A 8.6; DA X-012/X-017). |
| C-031 | C | A helper failure must not publish an unchecked report as successful unattended execution (C section 8). |
| C-032 | A+B | Source-only experimental delivery and a separate design note are smaller; DA's Fact check does not establish a universal mirror requirement (A 8.8; B 8.4). |
| C-033 | A | A mandatory fresh blindness audit detects defects absent from all drafts; C's ancestry inspection cannot (A section 9; C section 9). |
| C-034 | C | Explicitly preserve full FINAL and rf-qa stop rules rather than presenting scoped repair review as equivalent assurance (C section 11). |
| C-035 | C | Exclusive locking, generation checks and crash tests address races that atomic replacement alone does not (C sections 3, 10 and 13; B R11). |
| X-001 | C | Coordinator acceptance is worthwhile separation of judgment, but it remains cooperative enforcement rather than an unskippable harness (C sections 2 and 7). |
| X-002 | C | Stop invalid after one repair; do not silently relabel malformed evidence to keep the loop moving (C section 4; A 4.3; B section 4). |
| X-003 | C | Physical reflow may change Markdown structure, so conservative visible eligibility is safer than unconditional token-equivalence filtering (C sections 3 and 10). |
| X-004 | C | An unchanged observation has a legal deferred array; calling it an accepted finding first must trigger a repair, not soft acceptance (C section 4 step 5). |
| X-005 | A+C | Anchor the changed cause with unchanged context as evidence; B's two-item escape cap can suppress a real third consequence (A section 10; C section 7; B C11). |
| X-006 | C | Only the generated accepted report owns the verdict, avoiding B's redundant reviewer verdict requirement (C section 4; B C1). |
| X-007 | B | An admitted likely bar failure is more credible than an optimistic extrapolation from unverified best-run ancestry (B section 9; DA A-006). |
| X-008 | A+B | All-discovered primary counts prevent a narrower verdict definition from winning the historical comparison by deferral (A section 9; B section 9; C section 9 ambiguity). |
| X-009 | C | Ignoring a raw whitespace edit for eligibility does not justify authorizing that edit without a blocker owner (C section 3; A 3.5; B section 3). |
| X-010 | C | Verify retained predecessor flags and reject mismatches instead of discarding potentially useful integrity evidence (C sections 3 and 8). |
| X-011 | A+B | No general mirror requirement is established; test the selected source-install surface before adding plugin delivery scope (DA Fact check; A 8.8; B 8.4). |
| X-012 | A | A explicitly accommodates shipped-command inventory equality; B omits it and C incorrectly forbids the needed change (A 8.6; DA Fact check). |
| X-013 | C | Preapproved footprint containment avoids an arbitrary advisory threshold without imposing a hard size limit that prevents valid repairs (C sections 3 and 5; B 5.2). |
| X-014 | C | Explicit Skill activation and isolated discovery testing make loading observable; installer facts do not require A's naming choice (C section 8; DA Fact check). |
| X-015 | C | Remove the copied package-only template read rather than promise both byte preservation and no package-source lookup (C section 8; A 8.1/8.5; DA X-015). |
| X-016 | C | Declare the portability fix as an allowed drift-guard exception; B's untouched-copy and no-source-string requirements conflict (C section 8; B 8.1/8.3; DA X-016). |
| X-017 | A+C | Register the new unattended command as A proposes, but test C's stricter failure contract rather than demanding unchanged section bytes (A 8.6; C section 8; DA X-017). |
| X-018 | A+C | C's recomputed exact edit groups avoid B's replay accounting shortcut; B's own F1 admits the line with blocking N1 ownership (C section 3; B section 1 and F1; DA X-018). |
