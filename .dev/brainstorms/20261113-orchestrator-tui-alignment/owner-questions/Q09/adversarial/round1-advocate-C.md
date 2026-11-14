# Round 1 advocate statement: Proposal C (variant-3, "neither, as a standing rule")

Debate: Q9 (keep the sweep JSON?), sc:adversarial Mode A, depth quick, Round 1.
Evidence read 2026-11-14. ROOT = `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode`. MR = `merged-requirements.md`; ADJ = `alignment-findings-adjudicated.md`; DES = `docs/designs/orchestrator-mode.md`.

## 1. Position summary

C says the sweep's JSON is a one-time reply to its caller and is never stored, and closes SW-11 as "will not do". Its real merit is that no reader exists today, so nobody pays for a store or keeps a deferred item open. Its weak spot is that the word "never" goes further than the evidence: the adjudicated review still names two possible future readers.

## 2. Steelman of each opposing variant

**A (not now; caller capture first; a stored file only if needed).** A is the spec's own recommended answer, word for word (MR:536, ADJ:779). It changes no code and no test. It keeps PR #539 exactly as reviewed (A-004: "Add no JSON keys and no files inside #539", ADJ:210). It also respects the adjudicated finding that the sweep JSON is "a candidate carrier only for v2 and for a Coder#477 status record", with the instruction "v2 names its field list first" (ADJ:361, 78 percent). A leaves the choice to the first real reader, and that reader can define fields, retention and file mode, which V2-04 requires anyway: "named store, owner, reader set, retention and file mode" (MR:401). Its order (stdout capture first, a stored file only if that fails) is the cheapest path that stays reversible. The stdout object already carries `report_path` (`report.py:694`), so a caller can pair what it saved with the report.

**B (embed the JSON as a fenced block in the dated report).** B is the only variant that persists machine facts without touching NFR-001. The run still adds one file (DES:331: "1 report file + 1 JSON object on stdout"), so the two pinned tests (`test_readonly.py:300`, `test_cli_contract.py:1474`) should still pass. Storage rules come from the sweep itself rather than from each caller, so two callers cannot store it differently. Reports already go in one known, gitignored folder (`.gitignore:256` `.dev/sweeps/`; DES:63 GQ-106). The JSON is built from `SweepResult` only and is "sanitized ... but never cut" (DES:563; `report.py:613-694`). So the content already exists, and serialising it a second time is a small change.

## 3. Strengths claimed (C)

1. **No reader exists today, and the spec says so.** "Consumer today: the coordinator or a person; no observer consumer" (MR:221). The coordinator gets the JSON on stdout when it runs the sweep and needs nothing stored. C fits the present facts exactly.
2. **It removes a store that would have no owner.** V2-04 requires "named store, owner, reader set, retention and file mode" (MR:401). Report retention is out of scope: "the person deletes old reports by hand" (DES:35, SP-22). A store with no reader, no owner and retention by hand deletion is the kind of thing C prevents.
3. **It keeps the observer and the sweep separate.** ADJ E-03 says the two programs "never mention each other" (ADJ:129). X-017 keeps two readers, and persistence "survives only for an optional later panel" (ADJ:360). Q17 is recommended "No, not now" (MR:544). C turns that separation into a rule, so nobody builds an observer reader against a sweep file.
4. **NFR-001 becomes settled rather than provisional.** K-NFR001 lists SW-11 as the only thing that may change it, "by owner decision Q9" (MR:618). Under C nothing can relax it, so the design line (DES:128) and the two tests are never touched.
5. **Less open work.** SW-11 is listed as DEFERRED with a "later" location (MR:200). ADJ A-005 says "Nobody defends 'Phase 2 and #534 will absorb the deferred items': only a reading list exists" (ADJ:348). Closing one deferred item is honest about that.
6. **It respects the rule against refetching.** "Consumers never run another sweep merely to fetch status" (MR:221), and WC-16 limits sweeps to once per 5 minutes. With no stored copy, a later reader cannot quietly depend on sweep output. It has to name its own status source, and for status that is the observer snapshot (ADJ:346: "the first status record is the observer snapshot").

## 4. Weaknesses identified in the others

1. **B adds a second copy of the facts and has no reader for it.** B admits this: "with no named reader today" and "It answers a question the spec deliberately left for the first real reader to shape" (variant-2). ADJ A-001 tells the reader to name its field list first (ADJ:361). B fixes the field list to the stdout object, so a later v2 inherits that shape or has to change it, which is churn on `ROW_KEYS`-pinned data (MR:617; ADJ:210).
2. **B's store is not durable.** Reports sit in the gitignored `.dev/sweeps/` folder of one checkout (`.gitignore:256`), and they are deleted by hand (DES:35). The "every past sweep becomes machine-readable" benefit lasts only as long as a person keeps the files. A Coder#477 status record on another host could not read them (see A-002 below).
3. **B makes the report harder for people to read, and sanitising has to be checked again.** The report is the human artefact. The JSON is sanitized for stdout (DES:563), but B itself says it is UNVERIFIED whether that sanitizing is safe inside a Markdown fenced block (variant-2). `render` (`report.py:608`) currently emits no JSON block, so B is new format work on a tool that has only just merged or is about to.
4. **A pushes storage rules onto each caller.** A concedes that "two callers could store it differently" (variant-1). Caller capture also gives any later reader no single contract to rely on.
5. **A keeps the question open with no clock.** SW-11 is "DEFERRED ... later" (MR:200), wave W5 is "not scheduled by the spec" (question.md, MR:865), and A-005 shows that deferred items have no owner (ADJ:348). A's trigger is sound, but nothing guarantees that anyone watches for it.

## 5. Concessions (C's real weaknesses)

1. **"Never" contradicts the adjudicated finding.** ADJ A-001 (78 percent) keeps the sweep JSON as a candidate carrier for v2 and for a Coder#477 status record (ADJ:361). V2-04 depends on SW-11 "if v2 reads stored sweep facts" (MR:401). C closes a door that the evidence deliberately left open, and the cost of closing it is only a ledger line.
2. **C has nothing A lacks today.** Under both A and C the code, NFR-001 and the tests do not change now. C only adds that this will never change later, and the only evidence for that is the absence of a reader today, which is weak evidence about the future.
3. **"Never stored by callers" cannot be enforced.** The sweep cannot stop a caller from redirecting stdout (variant-3 admits this). The rule is a sentence, not a guard.
4. **Reopening costs more than deferring.** If v2 needs sweep facts, C requires "a new owner question, not a revival of SW-11" (variant-3), and the closure has to be explained. A's trigger does the same job with less friction.
5. **The fallback is weak.** C sends past readers to Markdown, which "is not a stable machine format" (variant-3). A shares this fallback, so it does not separate them.
6. **C pre-answers Q17.** Q17 effectively becomes "no" for good (variant-3). The spec keeps Q17 open and says "if yes later, Q9 becomes a real requirement" (MR:544).

## 6. Shared assumptions

- **A-001 (reports last long enough to be a record): QUALIFY.** The assumption is false as a durability claim. Reports are gitignored (`.gitignore:256`) and deleted by hand (DES:35). It does not hold for B, whose whole benefit rests on it. For A and C it is acceptable only as a best-effort route for a person to look back, not as a machine record. C's position barely depends on it, because C promises no stored machine facts. The diff-analysis wording "all three" is fair only in the sense that A and C also name the Markdown report as the fallback.
- **A-002 (readers share the sweep's host and checkout): ACCEPT for today, QUALIFY for the future.** It is true now: the consumer is the coordinator or a person (MR:221), and V2-04's first release "reads only what the same OS user on the same host can read" (MR:401). It breaks for a Coder#477 status record on another host, which none of the three variants serves. This favours A, because A lets that reader define its own transport and does not lock in a same-host store (B) or rule one out (C).

## 7. Per-point positions

| Point | Better variant | Confidence | Reason |
|---|---|---|---|
| S-001 (section set) | Tie (A) | 50% | Same five sections. No difference on the merits. |
| C-001 (is the JSON kept?) | A | 75% | "Not now" fits "no reader today" (MR:221) and keeps the named candidate readers (ADJ:361). C's "never" and B's "yes now" both go further than the evidence. |
| C-002 (NFR-001) | A | 65% | All three keep it now. A keeps the owner's lever that K-NFR001 reserves for Q9 (MR:618). C's permanence gives up that lever for no gain today. |
| C-003 (SW-11) | A | 70% | Deferred with a named trigger matches MR:200 and V2-04's conditional dependency (MR:401). C's closure is tidier but hides a live dependency. |
| C-004 (who owns storage rules) | B | 55% | B is the only one with a single owner (the sweep). A's per-caller rules can diverge, and C has no rules because there is nothing to rule. B's owner still has no retention policy (DES:35). |
| C-005 (later readers) | A | 75% | A leaves the first reader to shape the fields, as ADJ A-001 requires (ADJ:361). B pre-shapes them, and C forces a new question. |
| X-001 (keep anything before a named reader?) | A, with C agreeing | 80% | A and C both say no. A's "until a named reader" is the evidenced form. C's "and not later" is not evidenced. |
| X-002 (does keeping need NFR-001 relaxed?) | B | 70% | B is correct that embedding keeps one file (DES:331). A is correct that a separate file would need relaxing it. B made the sharper point. |
| A-001 (reports last as a record) | C | 60% | C relies on it least. B relies on it most, and it is false for durability (`.gitignore:256`; DES:35). |
| A-002 (same host and checkout) | A | 65% | A alone leaves a remote reader (Coder#477) free to choose its own transport. |

## 8. Overall verdict

The owner should pick **A** (the spec default), with one element borrowed from C: record now in the XC-05 contract note that sweep report JSON v1 is a stdout-only reply and has no stored form until a named reader triggers SW-11. Confidence is 75 percent. A matches every present fact that C relies on (no reader today, NFR-001 unchanged, no work in #539), and it does not shut out v2 and the Coder#477 status record, which the adjudicated review keeps as candidate readers (ADJ:361, MR:401). My own variant's "never" does exactly that, and nothing in the evidence supports it.
