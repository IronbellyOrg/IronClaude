# Round 2 rebuttal: Advocate for Variant 3 (reviewer-3, refactorer, opus)

"plan" = `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-021737/TASK-WF-brainstormFixBri-20261106-021737.md`; "brief" = `source.md` in the same folder; "spec" = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Every file:line below was Read or grepped this round. Index facts come from `diff-analysis.md:19` (the orchestrator's check), because I cannot run git here.

## Response to criticisms

Steelman first. Advocates 1 and 2 are right on the main point. V3 found the strongest evidence for C-001, but it priced the finding too high and aimed the fix at the wrong document. Each criticism of V3 is answered below.

| # | Criticism (who) | Answer | Verdict |
|---|---|---|---|
| 1 | R3-1 is P2, not P1: narrow edge, brief-owned, never observed (A1 R1/R2, A2 R2) | **They are right.** (a) The wording is the brief's own: plan:38 = brief:229, plan:128 = brief:217, plan:133 = brief:237, and all of it sits under "copy exactly, do not paraphrase" (brief:213). (b) The failure needs three things at once: the analyze route is taken, the call is cut off or refused before it writes, and the worker lists a file it did not write. (c) The only real run made no nested `/sc:analyze` call (`lc10-result.md:13`, re-grepped this round). (d) It cannot block `/sc:implement`: it is spec text, not a task AC. What I keep: plan:133 says "no known false FAIL" in the plan's own voice, and plan:128 holds the counter-fact ("can stop `/sc:analyze` before it writes"). So plan:133 is false as written. | **Concede P1 to P2 (high). Keep that plan:133 is false.** |
| 2 | R3-1 is over-tagged Grounded (A1, A2, A3-R1) | Conceded. The text conflict is Grounded: `analyze.md:97-98` and plan:38 against plan:128. The false FAIL is INFERRED. WC-4 defines `artifacts` as "every other file written" (`WORKER-CONTRACT.md:32`), so a worker that puts WC-4 ahead of its skill never lists an unwritten contract. Steelman of my side: the skill's own contract template lists "the nested contracts" without condition (`SKILL.md:388`), and Task 1 adds "also when the call failed". A worker reads its skill before the shared contract, so listing an unwritten file is plausible. Plausible is still not observed. | **Concede: Grounded conflict, INFERRED failure.** |
| 3 | R3-1's remedy (reword the skill sentence to "listed when it was written") is itself an unrecorded Part 4 departure (A1 R1/R2, A2 R1) | Conceded, and it is worse than that. The reword breaks brief:225 ("keeps the nested contract listed in `artifacts` unconditionally, a failed call's included, never 'only for a command that ran'"). "When it was written" is a condition. It also breaks Task 1's AC (plan:45), which requires the paragraph to end with the exact sentence. | **Withdraw my reword.** The fix belongs in the check sentence, not in the listing rule (see the C-001 section). |
| 4 | R3-2 rests on a false premise (A1, A2) | `diff-analysis.md:19`: the earlier package `...001016` is staged (`A`), and only this package is `??`, which plan:157 exempts. The premise is false today. | **Withdraw.** At most a note that depends on A-003. |
| 5 | R3-3 is not an "ordinary route" false FAIL; conforming briefs pass `--output` (A1 R2, A2 R2) | **They are right.** Spec:142 (brainstorm row, "Brief must pass") says `--output <dir>`, and `WORKER-CONTRACT.md:192` says the same. With `--output`, the worker fields go into the command's own `<output>/return-contract.yaml` (`brainstorm.md:154`), which also holds `domain` and `enrichment_used` (`SKILL.md:369-373`). So under a conforming brief the step-4 contract holds every field the sentence reads. "Ordinary route" was my Round 1 advocate's overstatement. A residue is real: the sentence does not say "with `--output`", and `brainstorm.md:153` still allows `--report-dir`. | **Downgrade to a P3 note.** |
| 6 | R3-4, R3-5 and R3-6 are notes about text the brief mandates (A1, A2) | **They are right on ownership.** R3-4's companion sentence is brief:221, R3-5's routing bullet is brief:230, and R3-6's residual risk is brief:239. The facts still hold: `handoff-routing.md:77` records `skipped` on a timeout, not "this tier's `quality_tier`", and spec:60 and spec:62 already name "the Skill tool or the Agent tool". These are brief-level notes for the owner, not plan defects. The plan copied the text faithfully, as R3-8 itself confirms. R3-4 is weaker still (see New evidence 3). | **Concede: brief-owned notes.** |
| 7 | R3-7 does not bite under the executor (A1 R2, A2 R2) | `sc-implement-protocol/SKILL.md:97` (grepped): "Default sequential in source order". Task 1 always runs first. | **Withdraw to nit.** It matters only for a manual out-of-order run. |
| 8 | V3 missed the F-13 and F-16 literal-verifier departures, the `git show` vacuity and the step-4 anchor (A1, A2) | True. For a card whose focus was deviation classification, missing both unrecorded departures (plan:25 against brief:199; plan:152 against brief:169) is the bigger miss. | **Concede.** |
| 9 | V3 is inconsistent about brief fidelity: it ignores F-13 and F-16 yet proposes its own departure (A2 R1) | Fair. Point 3 withdraws the departure. | **Concede.** |

## Updated assessment

Adversarial view of each variant, mine first.

- **V3 (mine).** It found the best evidence for the one plan sentence the plan's own text refutes (plan:133 against plan:128). Its secondary false-FAIL path (R3-3) shrinks to a note once the brief table is read. Two of its eight findings are withdrawn (R3-2, R3-7). Three are re-owned to the brief (R3-4, R3-5, R3-6). The one P1 becomes a high P2, and its proposed fix was wrong. V3's net value is C-001's evidence and R3-8's byte-for-byte confirmation. The blind calibration should land below its 0.74 self-confidence.
- **V1.** It has the best mechanical probe (C-005, narrowed to Task 4's routing half). It got the index right on C-004 and proposed the right fix shape for C-001. Weakness: its parenthesis carries a refusal exception that no file can show without the session file, and V1 did not say what happens when the session file is missing (handled in the C-001 section).
- **V2.** It is the only card that held the plan to the brief's literal verifiers (C-002, C-003). It missed C-001, and its P1 did not survive (its own R2 concedes this). Its option (b) is cheap, but it fixes the wrong reader (below).

Severity outcome: **no P1 survives on any card.** The plan is executable as written. Before `/sc:implement`, one owner decision is worth taking: C-001. After execution, the same spec line would need a second edit, and F-1's byte-for-byte rule (brief:45) would then point at stale text.

## New evidence

1. **A refusal is not covered by the existing `skipped` exception.** A timeout records `skipped` (`handoff-routing.md:77`). But no file maps a refused or failed `/sc:analyze` call to `skipped`. The brief forbids stating any tier for any `/sc:analyze` outcome (brief:225). Tier 2 activates "if Tier 1 returns error OR empty result" (`handoff-routing.md:31`), so a refused call can end up recorded as `fallback_1` or `primary`. So the refusal exception in any fix is load-bearing, and it cannot be dropped in favour of a `skipped`-only exception.
2. **The refusal exception can only be judged from the session file.** `analyze.md:97` prints a refusal "in chat only". The existing required-folder clause already relies on the session file and ends "when the session file is not verifiable, this last clause is recorded `not verifiable`, never PASS" (plan:128). Under V1's parenthesis alone, a listed path that is missing, with a non-`skipped` entry and no readable session file, can only be judged FAIL. On a correct run, that is a false FAIL. It is near-unreachable, because the nested directory sits under a parent that brainstorm already validated against the same refusal list (`brainstorm.md:153` against `analyze.md:97`). But it keeps plan:133 literally false. Spec:300 shows the intended handling for unreadable evidence: `not verifiable`, never PASS, owner accepts in writing.
3. **R3-4's "twin drift" already exists.** Spec:62 says the step must be gate-free "per its section 3 row"; the installed twin `WORKER-CONTRACT.md:24` has no such words. The two texts were never byte-identical, so the companion sentence adds drift of the same kind. That makes R3-4 an even weaker owner note.
4. `lc10-result.md:13`: "no nested `/sc:analyze` call was made". The C-001 path has never been observed.
5. A grep of `tests/` for `orca-worker-contract-spec` finds no match. No test reads the spec, so a Part 4 amendment changes no test pin.
6. Spec:142 brainstorm row: `--output <dir>`. This confirms that R3-3 applies only to a non-conforming brief.

## Recommended resolution of C-001

**Pick: (a) the owner amends brief Part 4. Use V1's parenthesis plus one clause in the sentence's tail, and the plan mirrors the change.**

Option (b) is rejected as the resolution. A live-plan author reads only the spec's 7.2 step 4 sentence. The plan's residual-risk notes (plan:133-137) stay in this package, Task 6 leaves "everything else in the spec as it is" (plan:139), and the package is archived to `.dev/tasks/done/`. Under (b), the false FAIL stays in the one sentence the P2 author uses, and only the plan becomes honest about it. Option (b) is acceptable only as a fallback if the owner declines (a). In that case, plan:133 must be narrowed and a fifth risk added, exactly as Advocate 2 wrote.

My own option (c), changing Task 1's listing sentence, is rejected. It breaks brief:225 and the AC at plan:45 (see Response 3).

**Exact replacement text** (apply in brief Part 4 "Task 6 live-check sentence", brief:217, and identically in plan:128):

Edit 1. Replace

```text
every `nested/analyze-` path listed in `artifacts` exists and holds its own `return-contract.yaml`, and every
```

with

```text
every `nested/analyze-` path listed in `artifacts` exists and holds its own `return-contract.yaml` (not checked for a call whose `codebase` entry is `skipped` or whose directory `/sc:analyze` refused), and every
```

Edit 2. Replace

```text
when the session file is not verifiable, this last clause is recorded `not verifiable`, never PASS
```

with

```text
when the session file is not verifiable, this last clause, and a listed path that is missing while the `codebase` entry is not `skipped`, are recorded `not verifiable`, never PASS
```

Edit 3. Change residual risk 4 (brief:241 and plan:137). Replace "The required-folder clause depends on the session file" with "The required-folder clause and the refusal exception depend on the session file". The rest of the bullet stays.

Checks against the constraints:

- **brief:225 (listing stays unconditional).** Held. Task 1's tail "The nested contract is listed in `artifacts`, also when the call failed." (plan:38) is untouched. The exception is on the check, not on the listing.
- **True FAILs are kept.** A call with a usable directory that failed must still have written its contract ("written on every outcome", `analyze.md:98`). Its listed path is still checked, so a missing file there is still a FAIL.
- **What the live-plan author reads.** The final spec sentence now carries both exceptions in the clause they apply to. Edit 2 routes the one unjudgeable case to the spec's existing `not verifiable` handling (spec:300) instead of a FAIL. The author needs no plan note to avoid a false FAIL.
- **plan:133 ("no known false FAIL")** becomes true. The only new leniency is that a missing path with an unreadable session file is recorded `not verifiable` instead of FAIL. That still blocks PASS until the owner accepts the gap in writing, which residual risk 4 already covers (Edit 3).

ACs and pins that change: **none.**

- Task 6 ACs (plan:142-144) still find `lc10`, ``a `source: codebase` entry`` and ``neither `quality_tier` nor `source` records``, and the edit is still one changed line in step 4.
- Task 1's AC (plan:45) is unchanged.
- No test reads the spec (New evidence 5).
- What must change: the plan text itself (plan:128 and plan:137) must match the amended Part 4, because F-1's verifier compares Task 6 byte for byte with the replacement wording (brief:45). Do this before `/sc:implement`, by owner amendment and a regenerate or a two-line plan edit. Otherwise Task 6 writes the old sentence into the spec.
- Known gap, not caused by this fix: no Task 6 AC checks byte equality (Advocate 2, R2 point 3).

## Final diff-point positions

| Point | Final superior position | Changed since Round 1? | One-line evidence |
|---|---|---|---|
| S-001 | none | no | No P1 survives on any card; counts measure bias, not merit |
| S-002 | V1 | no | V3's R3-1 failure is INFERRED (`WORKER-CONTRACT.md:32`); V2 tagged R2-3 Grounded wrongly |
| C-001 | split (V3 evidence; V1 severity P2 and fix shape) | yes | plan:38 vs plan:128 vs `analyze.md:97-98`; brief-owned (brief:213,217,229,237); fix = Part 4 amendment above |
| C-002 | split (V2 recording, V1 severity) | no | plan:25 vs brief:199 unrecorded; not blockable by a Constraints line (`qa.md:318`, per A1/A2); P3 |
| C-003 | V2 | no | Widening forced by F-2's status-after.txt (plan:152); unrecorded; "only" flaw is brief-owned (brief:169) |
| C-004 | V1 | no | `diff-analysis.md:19`: earlier package `A`, this package `??` exempted at plan:157 |
| C-005 | V1 | no | plan:95 "the same command" for the routing ref; short path fails and still prints 0; narrowed to Task 4 routing half |
| C-006 | V1 | no | Only raiser; format-check point valid, exit-code point weak; low |
| C-007 | split (V3 found it, V1 set severity P3) | yes | spec:142 and `WORKER-CONTRACT.md:192` require `--output`; `brainstorm.md:154` puts all fields in one contract then |
| C-008 | V3 (out-of-scope owner note) | no | Brief-mandated (brief:221); spec:62 and `WORKER-CONTRACT.md:24` already differ; fix needs a seventh file (plan:21) |
| C-009 | V3 (brief-owned note) | no | `handoff-routing.md:77` records `skipped` on timeout; text is brief:230 |
| C-010 | V3 (brief-owned note) | no | spec:60,62 name the Skill and Agent tools; text is brief:239 |
| C-011 | none | no | `sc-implement-protocol/SKILL.md:97` "Default sequential in source order" |
| C-012 | V2 | no | Matrix completeness only; plan satisfies the unsampled spans |
| C-013 | split (V1, V2) | no | spec:286 begins "4. Check the contract"; cosmetic |
| C-014 | none (all three agree) | no | plan:38,54,69,122,128 equal brief:229,230,231,221,217 |
| X-001 | V3 on evidence, P2 | yes | Real conflict, unobserved (`lc10-result.md:13`), not blockable; plan:133 false until Part 4 is amended |
| X-002 | V1 | no | `diff-analysis.md:19`: earlier package staged; R3-2 withdrawn |
| X-003 | split (V1 severity, V2 recording) | yes | spec:282 supports the plan's wording; departure from brief:199 still unrecorded; not P1 |
| X-004 | V2 | no | Necessary deviation forced by F-2, unrecorded; "only" overstatement shared with brief:169 |
| X-005 | V1 | yes | Ledger is the sibling progress.md (`implement.md:58`, per A1/A2); V2 conceded its exposure is small and INFERRED |
| A-001 | QUALIFY | no | Holds for a usable directory (`analyze.md:98`); fails for a caller timeout (`handoff-routing.md:77`); a refusal writes nothing and maps to no fixed tier (`handoff-routing.md:31`, brief:225) |
| A-002 | QUALIFY | no | Task ACs are judged literally; brief verifiers and the Constraints line are not ACs, so C-002 and C-003 are fidelity notes |
| A-003 | QUALIFY | yes | Before/after snapshot (plan:33,157) absorbs the baseline; only mid-run changes or an unstage of `...001016` break it |
| A-004 | ACCEPT | no | Exact-substring pins mandated (brief:232-233); each new phrase occurs once |
| A-005 | QUALIFY | no | Not a brief rule, but brief:34,42 and plan:131 make an unrecorded departure a note-level gap |
