review: 2 of 3

# Spec panel review, round 2 (re-review): Orca worker contract spec

| Header field | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md` |
| Review number | 2 of 3. The prior report's header is `review: 1 of 3` (`round1.md:1`), so N = 1 + 1. The prior report is not at `review: 3`, so the halt check does not apply. |
| CANDIDATE | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 57873 bytes, SHA-256 `92073bce9aa934458a66ff79344ce2e439141e3c08d2246944949c626f472a09` |
| BASELINE | `.dev/orca-command-refactor/specs/history/spec-v1.md`, 57763 bytes, SHA-256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`. This is the hash the prior report recorded for the candidate it reviewed (`round1.md:9`), so the baseline is the reviewed text. |
| PRIOR | `.dev/orca-command-refactor/review/round1.md`, SHA-256 `49b39a99ceb424b01faf7de460436402c205226bea718064bf3673422845bc72` |
| Reviser output read | `.dev/orca-command-refactor/review/revise1.md` (its claims were checked against the diff, not trusted) |
| Reviewer model actually used | Sonnet 5.5 (`claude-sonnet-5-5`) |
| Prompt followed | RE-REVIEW prompt and re-review core, `~/.claude/rules/prompts/document_review_loop_prompts.md:34-47` (`~` resolves to the sandbox `home/`), read in full before any finding. Roles: CANDIDATE is the `@file`, BASELINE is `--baseline`, PRIOR is `--re-review`. |
| Panel | Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard, Newman, Hohpe (architecture); Whittaker (adversarial). Crispin, Gregory, Hightower not engaged (outside the requested focus). |

Abbreviations: `SPEC:N` = line N of the candidate; `BASE:N` = line N of the baseline; `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `R1:N` = `round1.md` line N; `REV:N` = `revise1.md` line N.

## Step 1: evidence block

Command run: `diff -w specs/history/spec-v1.md specs/orca-worker-contract-spec.md`. Result: one hunk, `195c195`; exit code 1 (files differ). No other line differs, ignoring whitespace.

BEFORE (baseline), `BASE:195`:

```text
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
```

AFTER (candidate), `SPEC:195`:

```text
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command named in the P1 row of section 6, except `load` (usage-line fix only, no report file, section 3.2 and the Decisions table; F-01), has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
```

Net text change: the words `in sections 3.1-3.2` (19 bytes) were replaced by `named in the P1 row of section 6, except `load` (usage-line fix only, no report file, section 3.2 and the Decisions table; F-01),` (129 bytes). That is +110 bytes, which matches the byte accounting at `REV:12-17` (57763 to 57873). The reviser touched no other line, so the claim at `REV:18` holds.

Self-check run before the verdict (`grep -nF` with each quoted line, prefix removed):

| Check | Result |
|---|---|
| AFTER line found in CANDIDATE | found at `SPEC:195` |
| BEFORE line found in BASELINE | found at `BASE:195` |
| BEFORE line found in CANDIDATE (must be absent) | not found |
| AFTER line found in BASELINE (must be absent) | not found |

Roles are therefore not swapped.

## What I covered

- Read in full: the review-loop prompts file, `command.md`, `README.md`, `round1.md`, `revise1.md`, the candidate, and the diff above. Read in the inventories: the lines the spec cites for `load`, `brainstorm`, `init-lite` (`INV-B:31`, `INV-B:57-65`, `INV-A:39`, `INV-A:55`).
- Re-checked the one prior blocking finding (F-01) against the AFTER text only, then checked the AFTER line against every requirement that depends on it: the P1 row (`SPEC:159`), the phase gate (`SPEC:154`), AC-1.2 to AC-1.4 (`SPEC:196-198`), the `load` rows (`SPEC:112`, `SPEC:265`), the section-3 intro (`SPEC:76`), the section-4 list (`SPEC:132-137`) and D3 (`SPEC:240`).
- Counted the P1 set from the cells themselves: 9 listed commands (analyze, build, business-panel, design, document, explain, index, test, load) plus 4 fixed commands (adversarial, cleanup-audit, index-repo, workflow) = 13 (`SPEC:159`); 12 once `load` is excepted. The 9 section-3.2 rows with phase P1 (`SPEC:99`, `101`, `102`, `106`, `107`, `108`, `111`, `112`, `123`) match the 9 listed.
- Scope limit (Review Loop bullets 5 and 7): findings are limited to changed lines and the prior blocking findings. FR-8 to FR-10 and the Guard Condition Boundary Table cover guards on the changed line only. Everything else is `origin=unchanged`.
- Not covered, and UNVERIFIED in this sandbox: the project or home `rf-qa.md` agent file that Review Loop bullet 5 names for the re-check steps is not in the workspace (`find` over the sandbox found no `rf-qa*`), so the re-check below follows the rules in the Review Loop section and the prompts file, which the command says stand alone. Every `cmd/`, `sk/`, `ag/` citation not quoted by an inventory, `CLAUDE.md:*`, `src/superclaude/cli/install_core.py:*`, `Makefile:*` and `.dev/codegraph-migration/*` citation is UNVERIFIED; I did not need any of them to decide the changed line. The Pipeline and Guard analysis below does not re-review the 11 Medium and 6 minor findings of round 1; they are carried forward unchanged and unre-graded.

## Prior blocking findings: status table

| Id | Prior status | Status now | Basis |
|---|---|---|---|
| F-01 (AC-1.1 cannot pass as written, `R1:86-98`) | open, blocking | **resolved** | See the check against each of its four parts below. |

Check of F-01 against the AFTER text (`SPEC:195`) only:

| F-01 part (`R1:92-95`) | Defect | AFTER text | Result |
|---|---|---|---|
| 1. The test iterated 37 commands, P1 edits 13 | AC-1.1 asserted all of sections 3.1-3.2 | AC-1.1 asserts the commands named in the P1 row, `load` excepted: 12 commands, all of which P1 does edit (`SPEC:159`, and each carries phase P1 in `SPEC:83`, `85`, `86`, `92`, `99`, `101`, `102`, `106`-`108`, `111`, `123`) | resolved: assertion set is a subset of what P1 edits |
| 2. `load` has no report file (`SPEC:112`, `SPEC:265`; `INV-B:31`, `INV-B:65`) but AC-1.1 demanded a section naming `return-contract.yaml` | contradiction | `load` is excepted and the exception cites the same two places | resolved |
| 3. brainstorm (`SPEC:84`) and init-lite (`SPEC:87`) are in no phase list | AC-1.1 demanded a section from commands no phase edits | AC-1.1 no longer reaches them | resolved as to AC-1.1; the coverage gap this leaves is a separate Medium finding, M-13 |
| 4. pr-submit (`SPEC:114`) demanded at P1 while D3(a) makes no pr-submit change (`SPEC:240`) | contradiction | pr-submit is not in the P1 row, so AC-1.1 does not assert it | resolved |

Trace of Whittaker's round-1 attack (`R1:96`) on the new text: P1 is done as `SPEC:159` lists it; the test iterates the 12 named commands; each has the section; the test passes; the gate at `SPEC:154` does not block P2 to P4 for this reason. The attack no longer succeeds.

No prior blocking finding is open or regressed.

## Findings on changed lines (diff -w, `SPEC:195` only)

All of these have `origin=changed`, unless stated.

### Guard Condition Boundary Table (changed line only)

Trigger: `SPEC:195` is a set-membership guard ("every command named in the P1 row ... except `load`"; "no section-4 command"). Constructed before synthesis (FR-10). Nygard builds, Crispin's completeness check is folded in, Whittaker attacks the entries.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `ac11_scope` | SPEC:195 | Zero/Empty | a command named in the P1 row that has no `## Unattended mode` section | assertion fails | test fails, as intended (`SPEC:195`) | OK |
| `ac11_scope` | SPEC:195 | One/Minimal | `adversarial` (a fixed command, named in the P1 row after the semicolon, `SPEC:159`) | true, asserted | section must exist and name the contract (`SPEC:195`) | OK |
| `ac11_scope` | SPEC:195 | Typical | `analyze` | true, asserted | section must exist (`SPEC:195`) | OK |
| `ac11_scope` | SPEC:195 | Sentinel Value Match | `load` (the excepted name) | false, exempt | exempt; reason and places cited (`SPEC:195`, `SPEC:112`, `SPEC:265`) | OK |
| `ac11_scope` | SPEC:195, SPEC:159 | Legitimate Edge Case | `brainstorm`, `init-lite`: in sections 3.1-3.2 but in no phase Commands cell (`SPEC:84`, `SPEC:87`, `SPEC:158-162`) | not asserted | AC-1.1 says nothing; no other check asserts a section or the flag for them | GAP (M-13) |
| `ac11_scope` | SPEC:195, SPEC:159 | Legitimate Edge Case | wording "named in the P1 row": the row's Scope cell cites "every command in sections 3.1 and 3.2" by range, its Commands cell lists names | ambiguous | which cell "names" the commands is not stated | GAP (M-12) |
| `ac11_scope` | SPEC:195, SPEC:132-137 | Legitimate Edge Case | a section-4 command (agent, git, help, pm, spawn, swarm-wizard) | no section allowed | "no section-4 command has one" (`SPEC:195`) | OK |

Classes left out, one line each: Maximum/Overflow, because the set has a fixed size of 12 and no capacity; Zero/Empty for an empty P1 row, because the row lists 13 names (`SPEC:159`) and a P1 row without commands would make P1 meaningless, which no change on the changed line can cause.

Table status: complete, so synthesis may proceed (FR-10). Two GAP rows, graded below: M-12 and M-13 (both Medium).

### Quantity Flow Diagram (changed line only)

Trigger: the changed line shrinks the asserted set between stages, so counts differ across consumers (Fowler identifies, Whittaker attacks).

```text
[Source: 37 worker-capable commands, sections 3.1+3.2 (SPEC:76)]
  --> [Stage 1: P1 row Commands cell (SPEC:159)]
        13 = 9 listed + 4 fixed (analyze, build, business-panel, design, document, explain, index, test, load; adversarial, cleanup-audit, index-repo, workflow)
  --> [Stage 2: AC-1.1 exception (SPEC:195)]
        12 asserted (13 minus load)
  --> [Consumer A: AC-1.1 (SPEC:195) expects 12]                     match
  --> [Consumer B: P1 scope sentence (SPEC:159) "flag accepted by every command in sections 3.1 and 3.2" expects 37]   <-- MISMATCH 37 vs 12
  --> [Consumer C: AC-1.2 (SPEC:196) "each P1 command" expects 13 incl. load, which has no report file (SPEC:112)]       <-- MISMATCH 13 vs 12 (origin=unchanged, N-07)
  --> [Consumer D: phase table Commands cells (SPEC:158-162) assign 35 of 37]  unassigned: brainstorm, init-lite   <-- MISMATCH (origin=unchanged, same as round 1)
```

Grading decision: FR-19 labels any dimensional mismatch CRITICAL, but the Review Loop (bullet 2) grades by consequence and says CRITICAL is blocking. I follow round 1 (`R1:82`) and grade each mismatch by the wrong outcome it causes: M-13 (changed-line effect), N-07 and the unchanged Consumer D (notes). None of them makes the changed line contradict a stated text with no further assumption.

## === REQUIREMENTS ANALYSIS ===

### M-12 (Medium, origin=changed) "named in the P1 row" can be read two ways

- Expert: Wiegers (SMART, unambiguous scope), Adzic.
- Where: `SPEC:195` against `SPEC:159`.
- Why Medium: the P1 row has two cells that mention commands. The Scope cell says the flag is "accepted by every command in sections 3.1 and 3.2" (`SPEC:159`). The Commands cell lists 13 names (`SPEC:159`). "Named" fits the Commands cell, which is the natural reading and the one that fixes F-01. A reader who takes the Scope cell as the row's naming gets 36 commands (37 minus `load`), which restores the original F-01 defect minus one command. The text allows both readings, so the harm needs a guess, and it is Medium.
- Recommendation (follow-up only): write "the 12 commands in the Commands cell of the P1 row" or list them. Not requested for this loop.
- Priority: Low. Quality impact: removes the one reading that restores F-01.

### M-13 (Medium, origin=changed) brainstorm and init-lite are now covered by no check

- Expert: Wiegers (traceability), Cockburn.
- Where: `SPEC:195` (the narrowed assertion) with `SPEC:84`, `SPEC:87` (both fix "None"), `SPEC:76` ("Every changed command also gains the `## Unattended mode` section"), `SPEC:73` (the brief carries `--unattended` for every worker), `SPEC:158-162` (neither is in any Commands cell); disclosed by the reviser at `REV:31`.
- Why Medium: before the revision these two were asserted but no phase gave them the section, so the assertion was one of F-01's contradictions. After it, nothing asserts them. The row for each says what the brief must pass and omits `--unattended` (`SPEC:84`, `SPEC:87`), while section 2.3 says the brief carries it for every Task (`SPEC:73`). Whether P1 gives them the flag depends on the Scope cell (yes, `SPEC:159`) versus the Commands cell (no); that is a choice between two stated texts, not a stated text that does harm. It is a requirement the document never states: which phase edits them.
- Recommendation (follow-up only): add them to a Commands cell, or say they need no change because they are unaffected. Do not widen this loop's revision to do it.
- Priority: Medium.

## === ARCHITECTURE ANALYSIS ===

No finding on the changed line. Fowler, Newman and Hohpe note that the narrowed assertion keeps the layering decision intact: the shared rules still live in one installed file, `~/.claude/WORKER-CONTRACT.md`, which the assertion still requires every contract-bearing command to name (`SPEC:52`, `SPEC:195`). Narrowing the test does not touch the section-4 rule, which stays asserted (`SPEC:195`, `SPEC:132-137`).

## Adversarial analysis (Whittaker, changed line only)

1. I can break this specification by **Divergence Attack**. The invariant at **AC-1.1 (SPEC:195)** fails when **"named in the P1 row" is read through the Scope cell (`SPEC:159`) instead of the Commands cell**. Concrete attack: the test is written to iterate the 36 commands of sections 3.1-3.2 other than `load`; 24 of them are edited in P2 to P4 and carry no section; the test fails and the gate at `SPEC:154` blocks later phases. The same attack needs the less natural reading, so it is Medium (M-12).
2. I can break this specification by **Sentinel Collision Attack**. The invariant at **the `load` exception (SPEC:195)** fails when **`load` is also named in a later check as a P1 command**. Concrete attack: AC-1.2 (`SPEC:196`) runs the live check on "each P1 command"; for `load` step 3 requires a report path that is the contract path and step 4 runs `test -s <contract>`, but `load` writes none (`SPEC:112`, `INV-B:31`, `INV-B:65`). The exception sits in AC-1.1 only. This line is unchanged, so it is a minor note (N-07), not a finding on the revision.
3. I can break this specification by **Zero/Empty Attack**. The invariant at **AC-1.1 coverage (SPEC:195)** fails when **a command is in sections 3.1-3.2 but in no Commands cell**. Concrete attack: `brainstorm` receives `--unattended` from a brief built per `SPEC:73`; no phase edits it, no check asserts it; the outcome depends on how the command treats an unknown flag, which the spec does not say. Medium (M-13).
4. I can break this specification by **Sequence Attack**. The invariant at **the P1 to P4 order (SPEC:154)** is unaffected: the narrowed AC-1.1 passes in P1 without the P2 to P4 sections existing, which is the intended behaviour. No finding.
5. Accumulation Attack: the asserted count changes from 37 to 12 and is stated by reference, not by a number, so it cannot drift from the row. No finding.

## Findings with origin=unchanged (notes only)

An `origin=unchanged` finding is a minor note unless it quotes the changed line that depends on it (Review Loop bullet 5). The first note below quotes the changed line and is still kept as a note, for the reason given.

- **N-07 (minor note, origin=unchanged)**: AC-1.2 (`SPEC:196`) runs the 7.2 live check "on each P1 command", and the P1 Commands cell includes `load` (`SPEC:159`). The changed line states that `load` has "no report file" (`SPEC:195`), and 7.2 steps 3 and 4 require a contract (`SPEC:182-183`). I considered whether this restores F-01's consequence (a P1 check that cannot pass). It needs a guess that an implementer runs `load` as its own Task, which section 3.2 tells them not to do ("not as its own Task", `SPEC:112`; `SPEC:265`), so I do not grade it blocking. It came from the original text, not from the revision. A one-word fix ("each P1 command except `load`") is available to whoever opens the follow-up.
- **N-08 (minor note, origin=changed)**: `SPEC:195` carries a review finding id ("F-01") in normative text; an implementer reading the spec cannot resolve it. The Reviser contract asks the reviser to cite the id on additions (Review Loop bullet 6), so this follows the rule; it is noted so the id can be dropped when the loop closes.
- The unassigned `brainstorm` and `init-lite` in the phase table (Consumer D above) and the P1 Scope sentence's reach over P2 to P4 commands (`SPEC:159`; round-1 notes N-05 and the F-01 part 3 text) are unchanged since round 1. They stay as noted there.

## Self-check before the verdict

- Every prior blocking finding has an id in the table (F-01). No other finding id is cited as prior.
- Every id cited in this report appears in a table or heading above: F-01, M-12, M-13, N-07, N-08.
- The AFTER text is consistent with every requirement that depends on it that I could check: `SPEC:159`, `SPEC:154`, `SPEC:112`, `SPEC:265`, `SPEC:132-137`, `SPEC:240`. The one dependent check that is not (`SPEC:196`, N-07) is unchanged text and graded a note.
- The `grep -nF` role self-check passed (see Step 1).

## Follow-up candidates (Medium and minor; none triggers a revision)

Medium, new this round: M-12 (reading of "named in the P1 row"), M-13 (brainstorm and init-lite covered by no check).

Minor notes, new this round: N-07 (AC-1.2 still counts `load`), N-08 (finding id in normative text).

Carried forward from round 1 and not re-reviewed or re-graded here (the changed line does not touch them): M-01 to M-11 and N-01 to N-06 (`R1:205-216`).

Issue offer: the Review Loop (bullet 3) says the session that ran the review asks the user once per loop whether to open an issue for these candidates, and creates none without an answer. This worker was told to reply with a single `DONE` line, so it asked nothing and created nothing. The coordinator should ask.

## Brief clauses overridden

None. The brief (the command line and the "Re-review per the RE-REVIEW prompt" instruction) stayed inside the changed lines and the prior blocking finding, did not ask for any minor or Medium finding to fail the review, and did not say "apply all findings".

## Coverage

scoped PASS: changed lines + prior blockers

This is not whole-document assurance. A separate, labelled first review would be needed for that, and its blockers would be escalated and would not start a fourth review.

## Reviser brief

None. No blocking finding is open, so no revision is requested. (Restating the Reviser contract for completeness: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; cite the finding id on every addition; prefer deleting or narrowing to adding; report bytes added and deleted per finding id. Medium and minor findings are not revised in this loop.)

verdict: PASS


## Findings block

```findings-v1
{"prior": "L1", "status": "resolved"}
```
