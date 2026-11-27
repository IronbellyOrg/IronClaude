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
