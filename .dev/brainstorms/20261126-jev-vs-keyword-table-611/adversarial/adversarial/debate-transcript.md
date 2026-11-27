# Adversarial Debate Transcript

## Metadata

- Depth: standard
- Rounds completed: 2 (Round 1 parallel statements, Round 2 sequential rebuttals) plus Round 2.5 invariant probe
- Convergence achieved on diff points: 100% (20 of 20 points have an agreed winner after Round 2; 10 of them are MERGE)
- Convergence threshold: 75%
- Convergence status: BLOCKED_BY_INVARIANTS (6 HIGH-severity UNADDRESSED invariants, see `invariant-probe.md`)
- Blind mode: on (advocates saw variants as A, B, C with no model names)
- Advocate count: 3
- New evidence between rounds: a decision rule was proposed by another session after Round 1 (status PROPOSED, not AGREED); it is recorded in `.dev/issues/611/issue-summary.md` and was given to all Round 2 advocates.

## Round 1: Advocate Statements

### Variant A advocate

# Round 1 advocate: variant A (analyzer)

## 1. Position summary

A targets the root causes most likely to fake a result on 30 prompts: keyword-copied labels, a table already shaped by known prompts, and failures or slow calls dropped from the numbers. Each is bound to a requirement and a test; B and C supply A's missing ordering, traceability and spend detail.

## 2. Steelman of B, then of C

B: the cleanest pipeline. Tests cite their FR or NFR (T-01 to T-13), the gate requires table answers stored before any Jev call (gate step 4), the scorer fails on a corpus gap (FR-002), and owner-shaped choices live in a dated rule file with no default (FR-011, FR-012): the strictest reading of "fixed before the run".

C: the strongest audit trail. A dated event log ties every step to evidence (FR-009), the gate blocks unitless or contradictory owner input, and spending stops when price cannot be bounded.

## 3. Strengths claimed for A

1. Leakage cut at source: label basis from the problem's nature, blind labeller, blind table applier recording cues and rows per prompt (FR-003, FR-004, FR-011; C-001, U-004).
2. Contamination: the table was repaired in #871 against known observations and tests; prompts seen there are flagged and scored both ways (FR-005; U-001). Only A sees this.
3. Paired breakdown shows how many prompts a margin rests on (FR-020; U-002).
4. Latency median over all attempted calls, failures at timeout time (FR-019, section 4; C-003), so dropping slow failures cannot help Jev.
5. Errors stay in the denominator as not correct (FR-015, FR-018, T-04); the confirmed restatement fixes unit, denominator and ties (section 4 item 6; C-010).

## 4. Weaknesses identified in B and C

1. B records labeller and date but no labelling basis, so labels may restate keywords (FR-001; C-001).
2. B's latency basis is unstated (C-003); C defers it entirely.
3. B FR-018 rescoring under another rule file invites rule shopping unless marked non-decisional (U-007).
4. Neither flags table-seen prompts (U-001); B records no per-prompt table cues, C only "enough execution evidence" (C FR-004).
5. C's tests lack IDs and FR links (S-003); its "defensible upper bound" is undefined (C-007).

## 5. Concessions about A

- Test traceability trails B (S-003).
- FR-016 fixes a retry policy, then bans retries, charging transient outages to Jev (X-001).
- FR-018 settles what the seed left open (X-002).
- No table-before-Jev ordering (U-005), corpus check (U-006), event log (U-008) or whole-run spend check (C-007).
- Risks are bullets, not a table (S-002).
- No command collects tests under `.dev/` (A-005).

## 6. SCORING TABLE

S-001 | B | 60 | numbered IDs plus grouping; C uses bare bullets
S-002 | B | 60 | B's risk table cites FR/NFR; A uses bullets
S-003 | B | 80 | B tests cite the FR they check
C-001 | A | 80 | FR-003 basis plus FR-004 blindness stop keyword-copied labels
C-002 | A | 60 | RUN_INVALID covers changed files and missing provenance
C-003 | A | 75 | only A states the latency median's basis
C-004 | MERGE | 70 | A timestamps, B table-first ordering, C persisted result
C-005 | MERGE | 65 | A's conservative default written into B's rule file
C-006 | B | 60 | default none, optional pre-written policy, counted against cap
C-007 | MERGE | 70 | B whole-run check, A per-call check, C unbounded-price stop
C-008 | MERGE | 65 | A write refusal plus B post-run folder scan
C-009 | A | 50 | both names unverified against `.dev/` layout
C-010 | MERGE | 70 | A unit/denominator/tie restatement plus C blocking unitless input
X-001 | B | 60 | transient outages should not silently count against Jev
X-002 | MERGE | 65 | default in rule file, owner may change before freeze
A-001 | C | 60 | C FR-001 requires explaining any shortfall from 30
A-002 | C | 65 | C FR-005, FR-007 treat service fields as unverified
A-003 | B | 60 | only B asks whether a second labeller checks
A-004 | MERGE | 55 | nobody states it; report must name the limitation
A-005 | B | 75 | B gives the test path and raises collection

U-001 | yes | prompts known to the table can inflate its score
U-002 | yes | shows how few prompts decide the margin
U-003 | yes | merge with B's run-incomplete as one state with reason
U-004 | yes | stops manual application drifting toward labels
U-005 | yes | Jev output cannot shape table answers
U-006 | yes | cheap mechanical coverage check before the run
U-007 | yes | only if rescores are marked non-decisional
U-008 | yes | proves ordering without trusting a later narrative
U-009 | yes | cheap; keeps local timing apart from remote calls

## 7. SHARED ASSUMPTIONS

A-001 | QUALIFY | require reporting achieved count and coverage gaps, never synthetic padding
A-002 | QUALIFY | a missing field becomes error (FR-015); cost may be marked estimate
A-003 | QUALIFY | acceptable at 30 prompts if basis and blindness are recorded
A-004 | QUALIFY | record network location and state it as a limitation
A-005 | REJECT | spec must name the test command and record a passing run before the gate

### Variant B advocate

# Round 1 advocate: variant B (architect)

## 1. Position summary

B is the only spec built as a small, re-readable system. One job per file, one loader, rule-driven scorer, append-only runs and offline rescoring mean the experiment can be re-judged and extended. A and C hold stronger experiment-hygiene ideas, which should be merged into B's frame.

## 2. Steelman

**A.** A closes the validity holes that decide whether 30 prompts mean anything. FR-003/FR-004 stop labels from mirroring the table. FR-005 `seen-by-table` splits the score. FR-011 makes the table applier blind and records cues per row. FR-020 shows how many prompts a gap rests on. The gate restatement (item 6) catches unit and tie ambiguity, and RUN_INVALID keeps a bad run from driving issue 612. A fixes the latency basis (FR-019) where B is silent.

**C.** C treats the decision as evidence for an auditor. FR-009 is a dated event log that proves ordering without trusting a later narrative. Its spend guard (NFR cost) reserves outstanding liability and refuses unbounded requests. It keeps owner wording beside a machine reading and blocks the gate on unitless input. It also keeps local table cost apart from remote measurements.

## 3. Strengths of B

1. Question wording is never in code: FR-005, plus FR-006 rejecting aliases and T-13.
2. Rule-driven scorer: FR-011/FR-012 take Noul bounds and error treatment from the rule file with no built-in default (X-002). The owner can change policy without code edits.
3. Gate runs before the environment read (FR-014, gate order, T-04). This is the strongest key-secrecy structure of the three.
4. Table answers are stored before any Jev call (FR-009, gate step 4, U-005). It is mechanical anti-contamination.
5. Corpus check in the scorer (FR-002/FR-003, T-01, U-006) turns coverage and provenance into code.
6. Append-only run ids, offline rescore under a new rule file, README (NFR-008, FR-018, T-12, U-007). Rerunning never overwrites, which supports later review.
7. One-job-per-file folder and a single loader (NFR-010/NFR-011, section 5). A reader can re-judge from the folder alone.
8. Traceable tests: T-01 to T-13 each cite their FR (S-003). A has no cross-links on some tests and C has none.
9. Layered secrecy: redaction before storage plus a folder scan (NFR-005, T-10, C-008).

## 4. Weaknesses in A and C

1. A hard-codes error scoring and no-retry (FR-018, FR-016, X-001, X-002). It decides policy the owner has not accepted, and then lists acceptance as an open question.
2. A's 24 FRs mix policy into the spec, so the scorer cannot be re-run under a different rule. There is no rescore or run-id model (U-007 absent).
3. A has no stored-before-Jev ordering for table answers (U-005 absent), only a blind-applier rule.
4. C has no numbered tests and no FR links (S-003). Its seven bullets cannot be traced or ticked off.
5. C leaves the folder, verdict names and layout open (C-002, C-009) and defines no files. It is hard to implement from.
6. C's liability-reservation guard (C-007) is heavy for roughly 30 calls costing about 0.00004 dollars each, and it adds untestable machinery.
7. C does not state which scorer inputs exist, so "recomputable" depends on unspecified evidence formats.

## 5. Concessions about B

1. Latency basis is unstated (C-003). A's all-attempted-calls rule is better, and B's verdict can be gamed by dropping failed calls.
2. B has no label-basis rule (C-001), no seen-by-table flag (U-001), no blind table applier or cue record (U-004), no paired breakdown (U-002).
3. B has no unit and tie confirmation step (C-010) and no persisted event log (U-008).
4. Its whole-run worst-case check (NFR-002) is coarser than a per-call guard (C-007), though FR-015 adds a stop.
5. Storing raw bodies widens the leak surface. The tests-under-`.dev/` collection gap is only an open question.

## 6. SCORING TABLE

S-001 | B | 60 | Grouped NFRs with section 5 file table are easier to navigate
S-002 | MERGE | 60 | A and B tables beat C prose; no substantive gap
S-003 | B | 80 | T-01 to T-13 each cite their FR
C-001 | A | 80 | FR-003/FR-004 stop label leakage; B has only labeller and date
C-002 | A | 55 | RUN_INVALID covers more invalid cases than run-incomplete
C-003 | A | 85 | FR-019 states the basis; B leaves it open
C-004 | MERGE | 65 | A restatement, C persisted result, B pre-env-read order
C-005 | B | 60 | Rule-file policy with no scorer default; A's fix is unaccepted
C-006 | MERGE | 55 | B and C allow a declared retry; A has none
C-007 | C | 65 | Per-request liability beats whole-run estimate
C-008 | MERGE | 60 | B redaction and scan plus A refusal to write
C-009 | MERGE | 50 | Folder name is open in all three
C-010 | A | 75 | Item 6 confirmation catches unit and tie gaps
X-001 | B | 60 | No retry by default, optional pre-declared policy counted against cap
X-002 | B | 65 | Rule file decides; no built-in default (FR-011/FR-012)
A-001 | MERGE | 55 | No variant names a prompt source
A-002 | A | 60 | FR-012/FR-015 reject wrong model and malformed bodies
A-003 | MERGE | 55 | Only A's blind labeller and basis reduce single-labeller risk
A-004 | C | 55 | Separates local from remote measurements
A-005 | B | 65 | Tests beside data and open question 6 on collection

U-001 | incorporate yes | Cheap corpus flag, directly lowers inflated table score
U-002 | incorporate yes | Scorer output only, shows what the gap rests on
U-003 | incorporate yes | Fold into B's verdict set as a fourth state
U-004 | incorporate yes | Blind table arm with cue records is a core validity control
U-005 | incorporate yes | B's own; cheap and mechanical
U-006 | incorporate yes | B's own; keeps coverage in code
U-007 | incorporate yes | B's own; supports review and extension
U-008 | incorporate yes | Append-only events.jsonl fits B's run-id model
U-009 | incorporate no | Low value; keep only local-versus-remote cost labels

## 7. SHARED ASSUMPTIONS

A-001: QUALIFY. Add a sourcing plan or a fallback if too few real ambiguous or none-fit prompts exist.
A-002: ACCEPT. Needed, but state it as a response contract checked before any run (A's FR-015).
A-003: QUALIFY. One labeller is fine if label basis is recorded and the labeller is blind to arms.
A-004: QUALIFY. Record that latency is workspace-measured and not a pre-step estimate.
A-005: REJECT. Tests under `.dev/` can go uncollected; require a stated run command in the gate.

### Variant C advocate

## 1. Position summary

C offers the strongest audit-trail foundation: it states what evidence establishes ordering and justifies the decision. Merge A’s bias controls and B’s verification structure into C.

## 2. Steelman of A, then of B

**A:** A best protects measurement validity. Independent label bases, contamination splits, blinded table application, paired breakdowns, explicit error denominators, and attempted-call latency make results interpretable (A FR-003–005, FR-010–011, FR-018–020; C-001, C-003, U-001–004). T-01–T-10 give concrete verification targets.

**B:** B best serves later operators. Corpus validation, an ordered gate, append-only runs, deterministic scoring, and preserved rescoring outputs support independent review (B FR-002–004, FR-014, FR-018; NFR-008–011; S-003, U-006–007). T-04 and T-10 make secrecy controls observable.

## 3. Strengths claimed for C

1. **Gate scope:** C blocks comparison as well as live calls until owner inputs and the complete rule exist, matching the seed’s stronger constraint (C run gate; C-004).
2. **Chronology:** The first-request event references the exact pre-run manifest. Retained originals and identified amendments let reviewers establish ordering without trusting retrospective narrative (C FR-003, FR-009; U-008).
3. **Interpretation:** Owner quotations remain beside their confirmed interpretation; unclear units and contradictions block execution. Definitions must explain why they answer the build decision (C run gate; C-010).
4. **Honest records:** Candidates differ from final answers, unattempted cases from errors, and unmeasured local timing from zero. Issue text and resulting references are retained (C FR-007–010; U-009).
5. **Bounded spending:** Unbounded pricing or outstanding liability stops sending; estimates cannot masquerade as safeguards (C Cost cap; C-007).

## 4. Weaknesses identified in A and B

1. B allows table application before owner inputs; A’s hard gate addresses network access rather than all comparison. C preserves the seed’s required ordering (B gate step 4; A section 4; C-004, U-005).
2. A FR-024 ends at coordinator delivery, while the seed requires issue updates. C FR-010 includes retained publication evidence; A needs an explicit downstream completion obligation.
3. B freezes labels without requiring output blindness or non-keyword label bases. C FR-002 improves blindness, though A FR-003–005 remains strongest (C-001, U-001).
4. A fixes error scoring while asking owner acceptance. B permits alternative-rule rescoring without expressly separating exploratory conclusions from the original verdict. C requires separate replacement evidence after invalidation (X-002, U-007; A open questions; B FR-018; C run gate).

## 5. Concessions about C

C lacks numbered NFRs/tests and FR-to-test links (S-001, S-003). Its risk paragraph is harder to scan (S-002); the diff incorrectly calls A’s risk bullets a table. C lacks A’s contamination split and explicit denominator/latency defaults. Adopt A’s no-retry scored run. X-002 overstates C: pre-run policy need not exclude a spec-fixed policy.

## 6. SCORING TABLE

S-001 | B | 90 | Numbered requirements aid references.
S-002 | B | 90 | Risk table pairs causes and controls.
S-003 | B | 98 | T-01–T-13 link requirements and checks.
C-001 | A | 98 | FR-003 requires non-keyword label bases.
C-002 | MERGE | 90 | A’s enums; C’s inconclusive rationale.
C-003 | A | 95 | FR-019 separates attempted/successful latency.
C-004 | C | 99 | Blocks comparison; persists gate evidence.
C-005 | MERGE | 90 | Freeze explicit denominator pre-run.
C-006 | A | 95 | No retries preserves one-request design.
C-007 | C | 96 | Bounds liability and uncertainty.
C-008 | MERGE | 95 | C’s minimization; B’s redaction tests.
C-009 | C | 85 | Naming remains legitimately open.
C-010 | C | 96 | Ambiguous interpretations block execution.
X-001 | A | 95 | Scored retries weaken one-request design.
X-002 | MERGE | 94 | Resolve policy; remove apparent contradiction.
A-001 | MERGE | 95 | Provenance requirements cannot establish availability.
A-002 | C | 94 | FR-005 requires authorized service verification.
A-003 | MERGE | 90 | Difficult labels need review.
A-004 | C | 88 | FR-010 requires limitations.
A-005 | B | 95 | Explicit offline invocation and checks.
U-001 | incorporate yes | Exposes contamination.
U-002 | incorporate yes | Shows paired effects.
U-003 | incorporate yes | Makes invalidity explicit.
U-004 | incorporate yes | Preserves blinded reasoning.
U-005 | incorporate yes | After owner gate only.
U-006 | incorporate yes | Checks corpus completeness.
U-007 | incorporate yes | Mark rescoring exploratory.
U-008 | incorporate yes | Establishes evidence ordering.
U-009 | incorporate yes | Preserves publication evidence.

## 7. SHARED ASSUMPTIONS

A-001 QUALIFY — Verify public corpus availability before freeze.
A-002 QUALIFY — Validate actual response fields at authorized execution.
A-003 QUALIFY — Require instructions and difficult-case review.
A-004 QUALIFY — Limit conclusions to measured network conditions.
A-005 REJECT — Require recorded offline verification, not presumed collection.

## Round 2: Rebuttals

### Variant A advocate

# Round 2 rebuttal: advocate A (analyzer)

## 1. Responses to the strongest criticisms of A

- **A hard-codes policy (X-001, X-002).** Conceded on retries: the rule's one rerun per failed prompt contradicts A FR-016. Countered on content: a twice-failed prompt scores not right for Jev and stays in the denominator, which is A FR-018. B's no-default rule file is the container; A's text is its content.
- **No table-before-Jev ordering, no rescore model (U-005, U-007).** Conceded; adopt B's, with table answers stored after the gate (C's U-005 note).
- **A's gate covers network, not comparison (C-004).** Conceded; the seed blocks both.
- **FR-024 stops at coordinator delivery (C section 4.2).** Conceded; add issue updates and U-009.

**How each variant absorbs the rule.** A: the sign test's b and c are A's paired breakdown (U-002), now the decision statistic; the rule's validity conditions are A's RUN_INVALID list (U-003); "unset is right for both arms" needs a table no-answer rule, which only A has (U-004). A must edit FR-016 and FR-019. B: its rule file takes the rule without code edits, but lacks a latency basis and no-answer rule. C: its frozen rule document takes it, but lacks the b/c breakdown.

**A gap the rule leaves.** Its median is over "the final answered attempt of each prompt"; a prompt failing twice has none. A FR-019 (count it at the 10-second timeout) closes that gap.

## 2. Changed positions

C-002 | MERGE | 65 | rule has two verdicts; keep A's invalid reason as a field under "not clearly"
C-003 | MERGE | 70 | rule now supplies the basis; A adds timeout value for twice-failed prompts
C-005 | MERGE | 75 | rule adopts A's not-right-in-denominator; B's rule file holds it
X-001 | B | 80 | rule permits one logged rerun counted against the cap
X-002 | MERGE | 75 | rule is PROPOSED and may change, so no-default rule file carrying A's text

## 3. Unresolved points

C-006 | MERGE | 80 | B's pre-written retry policy plus C's separately visible attempts; drop A FR-016
C-009 | B | 65 | `.dev/README.md` lines 23 and 38 put decision-informing analysis under `research/`; `experiments/` is undocumented
C-010 | MERGE | 80 | proposal's 8-2 example contradicted its formula (p 0.0547); A's restate-and-return loop caught it, C's block keeps the gate shut while PROPOSED

## 4. Round 1 majorities

Accepted: S-001 to S-003 B; C-001 A; C-004, C-005, C-008 MERGE; C-007 C; X-001 B; X-002 MERGE; A-001, A-003 MERGE; A-002, A-004 C; A-005 B. C-004's merge must use C's comparison-scope gate. Disputed, against my own variant: C-002 and C-003 should be MERGE, since the rule now supplies that content.

### Variant B advocate

# Round 2 rebuttal: advocate B (architect)

## 1. Responses to the strongest criticisms of B

- **Latency basis unstated (C-003).** Conceded. The rule now states it, but only for answered attempts. A's gap is real: a prompt that fails twice has no final answered attempt. Count it at the 10-second timeout in the median too (A FR-019).
- **Table applied before owner inputs (C section 4.1; C-004).** Conceded. B gate step 4 stores table answers before the first Jev call, but the seed blocks the comparison itself. Keep U-005 ordering, but run it only after the gate is AGREED.
- **Rescoring under another rule file is not marked exploratory (C section 4.4; U-007).** Conceded. A rescore is labelled non-decisional and never replaces the original verdict.
- **No label basis, no seen-by-table flag, no cue record (C-001, U-001, U-004).** Conceded; take A's.
- **Unit and tie handling is "whatever the owner's words say" (C-010).** Conceded, and the new rule proves the point. See section 3.
- **A hard-codes policy (X-001, X-002).** A conceded; stands.

**How B absorbs the proposed rule.**
- C-005, C-006, X-001: FR-011 and FR-012 hold error treatment and a pre-written retry policy. The rule fills both slots: one rerun per failed prompt, every attempt counted against the cap, a twice-failed prompt scored not right for Jev. No code edit.
- C-003: the 2 s and 5 s limits are rule-file parameters. The measurement basis needs A's text.
- C-006 and the cap: B's whole-run worst-case check (NFR-002) must count the reruns. I concede it is coarser than C's per-request guard (C-007).
- X-002: the no-default stance fits because the rule is PROPOSED and may change.
- **Gap B does not close by configuration.** A sign test is code, not a parameter, so B's scorer needs a new, integer-arithmetic test type. This agent's own rule fixes the formula, so a rule file cannot just choose it.
- "Unset is right for both arms" on an ambiguous or none-fit label needs a table no-answer rule. Only A has one (U-004).
- C-002: two verdicts plus a reason field.

## 2. Changed positions

C-003 | MERGE | 75 | rule gives the basis, A adds the timeout value for twice-failed prompts
C-005 | MERGE | 75 | no-default rule file holds A's not-right-in-denominator
C-007 | C | 70 | reruns make whole-run estimates weaker still
X-001 | B | 80 | rule is a pre-written retry policy counted against the cap
X-002 | MERGE | 75 | rule file carries A's text while the rule is PROPOSED
C-010 | MERGE | 80 | see section 3

## 3. Final positions on unresolved points

C-006 | MERGE | 80 | B's pre-written retry policy (rule file), C's separately visible attempts; drop A FR-016
C-009 | B | 70 | `.dev/README.md` line 23 lists `research/` for analysis that informs design decisions, line 38 for decision memos; `experiments/` appears in neither line
C-010 | MERGE | 80 | the proposal's 8-2 example contradicts its own formula (p 0.0547); only A's restate-and-return loop catches that, and C's block keeps the gate shut while the rule is PROPOSED

## 4. Round 1 majorities

I accept all of them: S-001 to S-003 B; C-001 A; C-004, C-005, C-008 MERGE; C-007 C; X-001 B; X-002 MERGE; A-001, A-003 MERGE; A-002, A-004 C; A-005 B. Two conditions: C-004's merge uses C's comparison-scope gate, and C-002 and C-003 become MERGE, since the rule supplies that content.

### Variant C advocate

# Round 2: advocate C

## Rebuttal and new evidence

Conceded: C's unnumbered checks and unspecified files weaken implementation and independent scoring (S-001–003; B R1 §4). Adopt B's linked tests, loader and layout; A's label bases, contamination split, blind table cues and paired counts (C-001; U-001–004). Audit chronology cannot replace measurement controls.

On C-007, A rightly calls the request upper bound undefined: require a verified bound and refusal test. Cheap estimated calls do not bound liability. B now concedes C's per-request advantage. Sequential calls need no concurrent-request machinery. Both rebuttals accept C's stronger gate: comparison itself must wait (C-004; U-008).

**A accommodates the proposal** through paired counts and failure scoring, but must replace FR-016's no-retry rule and revise FR-019's latency basis (C-003, C-005–006; X-001–002). Its no-cue rule supports symmetric unset scoring.

**B accommodates it** through its frozen rule file and declared retry policy. However, B R2 correctly retracts configuration-only sufficiency: integer sign-test logic needs implementation. Store latency limits, charged attempts, final failure treatment and symmetric unset scoring explicitly.

**C accommodates it** through frozen interpretation, visible attempts and the event log. Add explicit scorer inputs, paired counts and linked tests. Its gate prevents proposal becoming approval (C-010). The corrected 8–2 example supports merging A's confirmation loop with C's contradiction block.

I withdraw my no-retry endorsement: one rerun per failed prompt fits accountable scoring. Every attempt counts against the cap; twice-failed prompts are not right. Unset is right for both arms on ambiguous/none-fit labels. Median ≤2 seconds uses final answered attempts; slowest ≤5 seconds covers all attempts. A/B identify missing median treatment for twice-failed prompts, but imputing 10 seconds to quick errors is another proposal, not agreed wording. Clarify before freezing. Status remains PROPOSED; the comparison gate stays closed.

## Changed positions

C-003 | MERGE | 90 | Freeze proposed basis; resolve missing answered attempts.
C-004 | MERGE | 96 | C gate/log, B ordering, A confirmation.
X-001 | B | 95 | Declared bounded reruns replace my no-retry preference.

## Final unresolved positions, all changed

C-006 | MERGE | 96 | B policy plus C's visible, charged attempts.
C-009 | B | 85 | Repository workspace guide supports research decision records.
C-010 | MERGE | 98 | A confirmation loop plus C blocking interpretation gate.

## Majority results

I accept every Round 1 majority except C-002 and C-003: both need MERGE. Preserve invalidity reasons under the proposed two-verdict scheme; reconcile latency rather than retain A unchanged.

## Scoring Matrix (final, after Round 2)

| Diff Point | Winner | Confidence | Evidence Summary |
|---|---|---|---|
| S-001 | B | 90% | Numbered ids plus grouped NFRs; unanimous |
| S-002 | B | 85% | Risk table pairs cause and control; 2 of 3 plus a MERGE vote |
| S-003 | B | 95% | Tests T-01 to T-13 each cite their FR; unanimous |
| C-001 | A | 90% | Label basis plus blind labeller; unanimous |
| C-002 | MERGE | 75% | Two verdicts plus an invalid-reason field; changed from A after the rule arrived |
| C-003 | MERGE | 80% | Rule supplies the latency basis; A adds the timeout value; median treatment of a twice-failed prompt still open |
| C-004 | MERGE | 85% | C's comparison-scope gate and event log, B's ordering, A's confirmation of the restatement |
| C-005 | MERGE | 75% | No-default rule file holds A's not-right-in-the-denominator text |
| C-006 | MERGE | 85% | Pre-written retry policy (one rerun per prompt), visible and charged attempts; A's no-retry dropped |
| C-007 | C | 75% | Per-request bound beats a whole-run estimate; undefined bound must be defined and tested |
| C-008 | MERGE | 75% | Refuse to write, redaction, folder scan, minimum transmission |
| C-009 | B | 75% | `.dev/README.md` lines 23 and 38 name `.dev/research/` for decision memos; `experiments/` is not listed (checked) |
| C-010 | MERGE | 85% | A's restate-and-confirm loop plus C's blocking of unclear input; the proposal's 8-2 example showed why |
| X-001 | B | 85% | Pre-declared, bounded, charged rerun |
| X-002 | MERGE | 75% | Rule file carries A's conservative default while the rule is PROPOSED |
| A-001 | MERGE | 65% | QUALIFY x3: verify corpus availability before freeze; report shortfall, never pad |
| A-002 | C | 70% | QUALIFY, ACCEPT, QUALIFY: validate the response contract at authorised execution |
| A-003 | MERGE | 70% | QUALIFY x3: one labeller acceptable only with a recorded basis and blindness |
| A-004 | C | 65% | QUALIFY x3: state that latency is measured from this workspace |
| A-005 | B | 80% | REJECT x3: name the test command and record a passing run before the gate |

Shared-assumption responses: all five A-NNN points were answered by all three advocates; no [OMISSION] flagged.

## Convergence Assessment

- Points resolved: 20 of 20
- Alignment: 100% on diff points; threshold 75%
- Taxonomy coverage: L1 (S-001, S-002, C-002, C-009), L2 (S-003, C-001, C-003, C-004, C-010, A-001, A-003, A-004, A-005) and L3 (C-005 to C-008, X-001, X-002, A-002) all debated; no forced round needed
- Invariant gate: BLOCKED. 6 HIGH UNADDRESSED: INV-001, INV-002, INV-003, INV-013, INV-014, INV-017. 10 MEDIUM UNADDRESSED (warnings).
- Status: BLOCKED_BY_INVARIANTS. Depth is standard, so no Round 3 runs. The six items are missing requirements, not disputes, so the refactor plan adds a requirement for each and the return contract lists them as unaddressed by debate.
- Unresolved points: none by vote. One open sub-item: median latency treatment of a prompt that fails twice (A and B count it at the 10-second timeout; C calls that a new proposal needing agreement).
