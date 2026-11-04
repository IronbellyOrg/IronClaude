# Diff Analysis: D2 Ruling-provenance position papers (3 variants)

## Metadata
- Generated: 2026-11-02T15:37:07Z
- Decision: D2 of `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` section 9 (lines 333-337): when `/sc:implement` halts for a Ruling inside an Orca worker, who may give the Ruling?
- Variants compared: 3
  - V1 = `variant-1-original.md`, option (a): keep the rule; the person resumes in their own session
  - V2 = `variant-2-original.md`, option (b): the coordinator relays the person's words through Orca `ask`
  - V3 = `variant-3-original.md`, option (c): the person writes the Ruling line into the ledger; the coordinator dispatches a resume worker
- Total differences found: 22 (structural 6 + content 12 + contradictions 4)
- Categories: structural (6), content (12), contradictions (4), unique (10), shared assumptions (12, of which 5 UNSTATED promoted to [SHARED-ASSUMPTION])
- Citation spot-check: 6 citations, 3 CONFIRMED, 2 OVERSTATED, 1 WRONG
- Citation key used below: `SPEC:N` = spec line; `QA:N`, `LEDGER:N`, `RETRY:N` = `src/superclaude/skills/sc-implement-protocol/refs/{qa,ledger,retry}.md:N`; `SKILL:N` = `src/superclaude/skills/sc-implement-protocol/SKILL.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `IMPL:N` = `src/superclaude/commands/implement.md:N`.
- Taxonomy (column "Level"): L1 surface (wording, layout), L2 structural (process shape, ownership, cost), L3 state-mechanics (ledger rows, eligibility, session and Task state). Priority L3 > L2 > L1; default L2.

## Structural Differences

| # | Area | V1 (a) | V2 (b) | V3 (c) | Severity | Level |
|---|------|--------|--------|--------|----------|-------|
| S-001 | Section set | Position, citation key, drift note, Safety, Reliability, Day to day, Implementation cost | Adds "Strongest case for it" before Safety | Adds "Why this works with no protocol change" before Safety | Low | L1 |
| S-002 | Citation scope | SPEC, QA, LEDGER, IMPL; declares RETRY in its key but never cites it | SPEC, QA, CAPS only; no LEDGER or RETRY citation, so its resume and ledger claims have no anchor | SPEC, QA, LEDGER, RETRY, IMPL; the only variant that cites the Ruling eligibility rule | Medium | L2 |
| S-003 | Source-currency check | Opens with a "citation drift" note (spec cites `qa.md:232,238`; rule now at `QA:254`) | None | None | Low | L1 |
| S-004 | Self-criticism | Cost stated only as "one context switch per halt" | Its own Safety section argues against the option (two risk bullets, no mitigation) | One labelled "Weakness" bullet (no scoped explanation; three fields to hand-write) | Medium | L2 |
| S-005 | Relation between options | Exclusive alternative to (b) | Exclusive alternative to (a) | Defined as a superset of (a): "or by running `/sc:implement` in their own session as in (a)" (V3 lines 3, 20). The choice is therefore (a), (a)+(c) or (b), not three disjoint options | High | L2 |
| S-006 | Testability placement | Cites existing AC-4.1 in Reliability | Lists AC-4.1 (b) only as an edit target under cost | Proposes a concrete AC-4.1 extension in Reliability | Low | L2 |

## Content Differences

| # | Topic | V1 (a) | V2 (b) | V3 (c) | Severity | Level |
|---|-------|--------|--------|--------|----------|-------|
| C-001 | Provenance of the Ruling | The person's confirmation is typed in the person's own conversation with the executor (`QA:254`: "clear user confirmation in the current conversation") | The person's words reach the worker as an Orca `reply` from the coordinator (`CAPS:62`); the worker "cannot tell the person's words from the coordinator's" (V2 line 13) | The person's own keystrokes in the ledger file, or V1's route. No agent message carries it (V3 line 13) | High | L3 |
| C-002 | Who writes the ledger line | The executor, in the person's session, per `QA:256` | The executor in the worker, quoting the relayed text "verbatim" | The person writes it by hand; a coordinator-written line is named "executor-invented approval" (`QA:249`) | High | L3 |
| C-003 | Executor's scoped explanation before acceptance (`QA:254`: "explain the task id, unmet AC/finding and current outcome, proposed acceptance, reason and cost-if-wrong") | Kept: the executor explains in the person's session (V1 line 18) | Diluted: the person sees "the coordinator's rendering of that explanation, not the executor's" (V2 line 14) | Skipped: the person relies on the halt message (`QA:247`: ledger path, Ti, verdict, missing citations) and writes all three fields alone; V3 calls this its weakness (line 21) | High | L2 |
| C-004 | Continuity of the remaining plan | The remaining tasks run attended in the person's session; "the remaining tasks of that plan leave Orca" (V1 line 19) | The remaining tasks keep running in the same worker after one answer | A new resume Task runs the remaining tasks unattended; "The rest of the plan stays in Orca" (V3 line 20) | Medium | L2 |
| C-005 | Resume mechanics (ledger rows R and H) | Not described beyond "resumes from the ledger". With a `halt` record and no Ruling, resume hits row H (`LEDGER:156`): a fresh operator review of the tree, then on non-compliant a `blocked` + `halt ... reason=operator-review` and STOP `E-HALT-QA`, after which the executor explains, asks and records. V1 omits this extra review | No resume: claims the worker "keeps its session, its ledger position and its retry state". Unaddressed: any `halt` is terminal (`RETRY:488`), the command has already stopped, and WC-3's re-invoke route needs an answer that fits an existing argument or flag (`SPEC:67`); implement has none for a Ruling | Row R (`LEDGER:154`) precedes P and H, so an eligible hand-written Ruling gets the post-ruling `complete` with no review; `--resume` is implicit (`IMPL:57`) | High | L3 |
| C-006 | Human wait time inside a worker | None: the worker ends `failed` at once | The worker session is held in `ask` for as long as the person takes; no heartbeat needed (`CAPS:64`); a timeout resumes the same message ID (`CAPS:60`); a late answer needs a new Task (`SPEC:67`) | None inside a worker: the wait sits between Tasks, until the person tells the coordinator "Ruling written" | Medium | L3 |
| C-007 | Protocol change cost | Zero protocol, zero spec change (WC-3 and the implement row already carry the exception) | Edits `QA:254`'s rule, WC-3, the implement row and AC-4.1 (b); non-goal 6 (`SPEC:319`). Not counted by V2: a mid-command `ask` sits against SA-2 (`SPEC:170`, no command runs an `orca` command) unless the re-invoke route is redesigned | Zero protocol change; one spec sentence in D2/WC-3, a rule that a coordinator-written line is invalid, and one AC-4.1 extension | Medium | L2 |
| C-008 | Testability | Existing AC-4.1 (D2 a): no `question` message, no Ruling in the ledger (`SPEC:274`) | AC-4.1 (b): the Ruling quotes the person verbatim. Relay fidelity itself cannot be checked by the worker or by a grep | Extended AC-4.1: add a hand-written line, dispatch a resume Task, expect `complete` with the unchanged verdict (`QA:248`); deterministic table row | Medium | L2 |
| C-009 | Single writer of the ledger | Not addressed; implicitly safe if the person resumes after the worker ends | Single writer by construction (same worker) | Explicit: no lock (`LEDGER:145`); the person writes only after the worker has settled, per WC-6 (`SPEC:70`) | Medium | L3 |
| C-010 | Malformed input handling | n/a (the executor formats the line) | n/a (the executor formats the line) | Claims a malformed line "is ignored and the resume halts again (`LEDGER:156`)". The appended line is the ledger's last line, and an unparseable last line is `E-LEDGER-CORRUPT` (`LEDGER:123`, `SKILL:36`); see spot-check 4 | Medium | L3 |
| C-011 | Frequency argument | Halts are rare by design (`QA:274`, `QA:288`, `QA:280`), so the per-halt cost is small | Silent | Silent | Low | L2 |
| C-012 | Reversibility | Easy to relax later; hard to restore trust after a bad relayed Ruling | Reversing means editing the protocol again | (a) stays available unchanged if hand-writing proves awkward | Low | L2 |

## Contradictions

| # | Point of Conflict | V1 (a) | V2 (b) | V3 (c) | Impact | Level |
|---|-------------------|--------|--------|--------|--------|-------|
| X-001 | Is a coordinator-relayed Ruling compatible with `QA:254`? Falsified by reading `QA:254` | "An Orca coordinator is another agent (`SPEC:334`). Keeping the rule keeps the one human checkpoint" (line 10) | "It contradicts the rule as written" (line 13), yet "The person still decides" (line 9) | "no agent ever relays a Ruling" (line 3) | High | L3 |
| X-002 | Does keeping the rule force the rest of the plan out of Orca? Falsified by whether a resume Task can consume a person-given Ruling | "the remaining tasks of that plan leave Orca" (line 19) | (not a party) | "The rest of the plan stays in Orca" under the same unchanged rule (line 20), via row R and a resume Task | Medium | L3 |
| X-003 | Is WC-3's `ask the coordinator` route structurally open to a Ruling halt? Falsified by `SPEC:67` | WC-3 carries a Ruling exception; WC-3's route is not a Ruling route (line 22) | "It matches how the spec treats other gates, which may go to the coordinator under `On a blocked gate: ask the coordinator`" (line 10) | Worker "reports the halt as `blocked` and ends `failed`" (line 3) | High | L3 |
| X-004 | V2 internal: who decides? Falsified by whether the worker can verify origin | (not a party) | "The person still decides. The words recorded are the person's, quoted verbatim" (line 9) vs "provenance rests on trusting the coordinator to relay faithfully" and "an 'executor-invented approval' the worker cannot detect" (line 13) | (not a party) | High | L3 |

Notes on falsification:
- X-001: `QA:254` lists "another agent's message" as not acceptance; `CAPS:62` shows the answer arrives as the coordinator's `reply`. V2's own line 13 concedes the conflict, so (b) needs the rule edited, not reinterpreted.
- X-003: `SPEC:67` limits the ask route to "a gate that fires before the command has written any output except its blocked contract and whose answer fits an existing argument or flag". A Ruling halt fires after the ledger has records, and `/sc:implement` has no Ruling flag (its flags are `--resume`, `--ledger`, `--skip-final-review`, `IMPL:6`). V2's "matches" claim fails on both conditions.

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | V1 | Detects citation drift: the spec's `qa.md:232,238` now points at the Family probe section; the rule is at `QA:254`, the Halt rows at `QA:247-249` (cause: commit 80f934de). Applies whatever option wins | High |
| U-002 | V1 | Frequency argument: minors and notes never halt (`QA:274`, `QA:288`); `E-HALT-QA` needs a confirmed blocker a repair could not close (`QA:280`), so per-halt cost is rare | Medium |
| U-003 | V1 | Asymmetric reversibility: relaxing later is cheap; restoring trust after a bad relayed Ruling is not | Medium |
| U-004 | V2 | Orca `ask` facts: durable on timeout, resume by message ID (`CAPS:60`), no heartbeat while blocked (`CAPS:64`), late answer needs a new Task | Medium |
| U-005 | V2 | Names the undetectable failure: the worker cannot tell the person's words from the coordinator's (`CAPS:62`), so a paraphrase is invisible "executor-invented approval" | High |
| U-006 | V2 | Scope-check dilution: the person sees the coordinator's rendering of the `QA:254` explanation, not the executor's | Medium |
| U-007 | V3 | A third path that keeps the rule and still returns the plan to Orca: a hand-written Ruling consumed by ledger row R in a resume Task (`LEDGER:154`, `RETRY:498`, `IMPL:57`) | High |
| U-008 | V3 | Single-writer precondition: no ledger lock (`LEDGER:145`), so the person writes only after the worker has settled (WC-6, `SPEC:70`) | High |
| U-009 | V3 | Requires the spec to state that a coordinator-written Ruling line is "executor-invented approval" (`QA:249`) | Medium |
| U-010 | V3 | Concrete live check: extend AC-4.1 with a hand-written line and a resume Task, expect `complete` with the unchanged verdict | Medium |

## Shared Assumptions

| # | Assumption | V1 | V2 | V3 | Class | Level |
|---|-----------|----|----|----|-------|-------|
| A-001 | A coordinator reply is "another agent's message" under `QA:254` | agrees (line 10) | concedes (line 13) | agrees (line 13) | STATED | L2 |
| A-002 | The accepted outcome stays non-compliant: the Ruling leads to a `complete` with the unchanged verdict, never `compliant` (`QA:248`, `LEDGER:82`) | implied | implied | stated (line 17) | STATED | L3 |
| A-003 | The ledger plus git is enough state to resume deterministically (`LEDGER:137`, `LEDGER:149`) | stated (line 14) | not used | stated (line 17) | STATED | L3 |
| A-004 | Only `E-HALT-QA` and `E-NO-RULING` need a person's decision inside a worker | stated (line 3) | implied | stated (line 3) | STATED | L2 |
| A-005 | The coordinator is an LLM agent that can paraphrase or answer from its own plan | stated (line 10) | stated (line 13) | implied (line 13) | STATED | L2 |
| A-006 | Halts are rare enough that per-halt handling cost is acceptable | stated (line 15) | not stated | not stated | STATED (V1 only) | L2 |
| A-007 | Orca's `reply` arrives in the worker's conversation attributed to the coordinator (`CAPS:62`) | relies on it | stated | relies on it | STATED | L3 |
| A-008 | [SHARED-ASSUMPTION] The person learns of the halt. None says who tells the person or how: V1 and V3 say "the person reads the halt", V2 says "the coordinator asks the person". The contract carries `blocked_question` (`SPEC:66`), but no variant says the coordinator must surface it | unstated | unstated | unstated | UNSTATED | L2 |
| A-009 | [SHARED-ASSUMPTION] The person can reach the worker's ledger file. V1 resumes from it and V3 edits it; both assume the person's session sees the same worktree. Workers share the current worktree by default (`CAPS:115`), but the brief may place them elsewhere, and remote workers exist (`SPEC:322`, non-goal 9) | unstated | n/a | unstated | UNSTATED | L3 |
| A-010 | [SHARED-ASSUMPTION] Keystrokes in the person's session or in the ledger file are the person's. The eligibility rule is positional only (`RETRY:498`) and cannot tell who wrote a line; any agent with file access could append one. V3 forbids a coordinator-written line by spec text only (line 13); V1 does not raise it | unstated | n/a | partly stated (policy only) | UNSTATED | L3 |
| A-011 | [SHARED-ASSUMPTION] The `dispute` halt (`QA:281`: "a disputed AC is a user decision") is out of scope. It also writes a `halt` record, so a Ruling after it is eligible under `RETRY:498` clause (a), and it is a person-decision halt inside a worker. No variant mentions it | unstated | unstated | unstated | UNSTATED | L3 |
| A-012 | [SHARED-ASSUMPTION] After any Ruling halt in a worker, a later Ruling is eligible. Not always true: a Ruling after a transient stop with no `halt` record following the latest `blocked` is ignored (`RETRY:500`); a task with `retry` records but no `halt` matches neither clause of `RETRY:498`. V3's hand-written line and V1's resumed session both depend on a `halt` record being present | unstated | unstated | partly stated ("A Ruling written after the halt is eligible") | UNSTATED | L3 |

Promoted [SHARED-ASSUMPTION] points for the debate: A-008, A-009, A-010, A-011, A-012.

## Citation spot-check

Each citation was re-read in this run.

| # | Citation (cited by) | What the source says | Verdict |
|---|---------------------|----------------------|---------|
| 1 | `QA:254` (V1, V2, V3): the relay rule and the explanation before asking | "A clear user confirmation in the current conversation is sufficient; the user need not hand-write a ledger record. Before asking, explain the task id, unmet AC/finding and current outcome, proposed acceptance, reason and cost-if-wrong. ... another agent's message ... not acceptance." | CONFIRMED. The explanation is a precondition of the asking path only. Halt-table row `QA:248` gives "valid existing operator Ruling" as an alternative that carries no explanation step, and "need not hand-write" implies hand-writing is allowed. So V3's "skips the executor's scoped explanation" is accurate and is a weakness, not a protocol violation; V2's "the protocol requires the executor to explain" is accurate for the asking path |
| 2 | `QA:256` and `LEDGER:195` (V3): "An operator-written Ruling is already valid" | `QA:256`: "Existing operator-written records remain valid." `LEDGER:195`: "The earlier operator-written form (...) remains valid." But `LEDGER:62` heads the section "user-authorized, executor-recorded" and `LEDGER:68` says "the executor MUST automatically append this line" | OVERSTATED. Mechanically valid: eligibility is positional (`RETRY:498`), the regex accepts the line (`LEDGER:71`), and `LEDGER:110` allows "operator `Ruling:` lines" after a halt. As policy, "existing" and "earlier" read as a backward-compatibility clause; no line explicitly endorses a newly hand-written line as the intended route. `QA:254` "need not hand-write" is the strongest support |
| 3 | `LEDGER:149-154` and `RETRY:498` (V3): row R runs first and a Ruling after the halt is eligible | Row R: "An eligible Ruling with no `complete` after it → Append the post-ruling `complete` ... with no review, then row 1", listed after row 1 and before P, H. `RETRY:498`: eligible iff "(a) a `halt` record follows the task's latest `blocked` line, the Ruling comes after that `halt`, and no verdict line lies between" or (b) no `retry` and no `halt` and the Ruling follows the latest `blocked` | CONFIRMED for an `E-HALT-QA` ladder halt, which writes a `halt` record: a hand-written line after it is eligible and resume completes the task with no review. Caveat (A-012): after a transient stop with no `halt` record the line is ignored (`RETRY:500`). Contrast for V1: with no Ruling, resume falls to row H (`LEDGER:156`), which runs a fresh operator review and re-halts before the executor can ask |
| 4 | `LEDGER:156` (V3): "A malformed line is ignored and the resume halts again" | `LEDGER:156` is row H and says nothing about malformed lines. `LEDGER:123`: "if last line does not match header\|start\|verdict\|ruling\|retry\|halt\|FINAL regex → E-LEDGER-CORRUPT"; `SKILL:36`: "`E-LEDGER-CORRUPT` \| Last ledger line truncated/unparseable \| No further". The Ruling regex requires em dashes (`LEDGER:71`: `Ruling: .+ — .+ — .+$`) | WRONG on mechanism. A hand-appended line is the last line, so a malformed one (for example hyphens typed for em dashes) stops resume with `E-LEDGER-CORRUPT`, not row H. The outcome is still a safe stop, but recovery needs a hand edit of the ledger, and V3 does not say so |
| 5 | `SPEC:334` (V1): the spec cites `qa.md:232,238` but the rule moved | `QA:232` and `QA:238` are Family probe bullets; the rule is at `QA:254`; halt rows at `QA:247-249` | CONFIRMED. The same stale anchors also appear at `SPEC:67` (WC-3 cites `qa.md:238`), `SPEC:132` (implement row cites `qa.md:231-238`) and `SPEC:319` (non-goal 6 cites `qa.md:238`); V1 names only `SPEC:334` |
| 6 | `CAPS:60-64` and `SPEC:67` (V2): `ask` is durable, no heartbeat, and the relay "matches how the spec treats other gates" | `CAPS:60`: "Timeout leaves the question pending; resume with the original message ID." `CAPS:64`: heartbeats skipped "while blocked inside `ask`". `SPEC:67`: the ask route applies only "at a gate that fires before the command has written any output except its blocked contract and whose answer fits an existing argument or flag" | OVERSTATED. The `CAPS` facts are confirmed. The "matches other gates" claim fails: a Ruling halt fires after output exists and its answer fits no `/sc:implement` flag, so (b) needs a new route, not the existing one (see X-003) |

Answers to the two required checks:
- Is an operator-hand-written Ruling line eligible on resume? Yes, after an `E-HALT-QA` that wrote a `halt` record: row R (`LEDGER:154`) runs before row H (`LEDGER:156`) and `RETRY:498` clause (a) makes the line eligible, so the task completes with the unchanged verdict and no review. Not after a transient stop with no `halt` record (`RETRY:500`). A malformed hand-written last line gives `E-LEDGER-CORRUPT` (`LEDGER:123`).
- Does `qa.md` require the executor's scoped explanation in a way a hand-written line skips? The explanation is required before the executor asks for confirmation (`QA:254`). A hand-written line uses the other branch of row `QA:248` ("valid existing operator Ruling"), which has no explanation step. The line skips the explanation without breaking the protocol; whether a new hand-written line counts as "existing" is the open wording question in spot-check 2.

## Summary
- Total structural differences: 6 (High 1, Medium 2, Low 3)
- Total content differences: 12 (High 4, Medium 6, Low 2)
- Total contradictions: 4 (High 3, Medium 1)
- Total unique contributions: 10 (High 4, Medium 6)
- Total shared assumptions: 12 (STATED 7, UNSTATED 5, CONTRADICTED 0); promoted [SHARED-ASSUMPTION]: A-008, A-009, A-010, A-011, A-012
- Taxonomy of S/C/X/A points (34): L1 2, L2 15, L3 17
- Highest-severity items: S-005 (V3 is a superset of V1, so the options are not disjoint), C-001 (provenance), C-002 (who writes the line), C-003 (scoped explanation), C-005 (resume mechanics: row R vs row H; V2 has no resume path), X-001 (relay vs `QA:254`), X-003 (WC-3's ask route does not fit a Ruling halt), X-004 (V2 internal provenance conflict); spot-check 4 WRONG (malformed hand-written line gives `E-LEDGER-CORRUPT`, not row H)
- Similarity check: 18 comparable items (6 structural areas + 12 content topics), all 18 differ across the variants (100%). Total differences are far above 10% of comparable items; the variants are not near-identical and the debate should proceed.
