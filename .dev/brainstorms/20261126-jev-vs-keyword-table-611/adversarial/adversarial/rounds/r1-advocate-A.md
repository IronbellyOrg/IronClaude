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
