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
