# Round 2 rebuttal: Advocate for Variant 1 (reviewer-1, analyzer)

"plan" = `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-021737/TASK-WF-brainstormFixBri-20261106-021737.md`; "brief" = `source.md` in the same folder. Everything cited below was Read or run this round unless marked otherwise.

## Response to criticisms

Criticisms of V1 raised by Advocate 2 (A2) and Advocate 3 (A3) in Round 1, each answered.

| # | Criticism (who) | Answer | Verdict |
|---|---|---|---|
| 1 | A-2 filed P2 INFERRED although `analyze.md:97-98` was on disk; should be Grounded (A2, A3) | Conceded for the text conflict. I Read `analyze.md:97-98`: the contract "is written on every outcome" once a usable report directory exists; an unusable one is "refusal printed in chat only". The conflict between plan:38 and plan:128 is therefore Grounded. The failure is still INFERRED: it needs a worker that lists a file it did not write, and WC-4 (`WORKER-CONTRACT.md:32`) defines `artifacts` as "every other file written". So the honest tag is "Grounded conflict, INFERRED failure". My tag was wrong on the first half. | Concede tag; keep P2 |
| 2 | A-2 left at P2 although plan:133 says "no known false FAIL" and a P2 author will trust it (A3) | Partly conceded. plan:133 is false as written because plan:128 itself says the timeout "can stop `/sc:analyze` before it writes". But plan:133 copies brief:237 word for word. Severity stays P2: see "Updated assessment (a)" for likelihood. | Concede that I should have named plan:133; keep P2 |
| 3 | V1 missed R3-3 (`domain` and `enrichment_used` in the wrong contract) (A3) | Conceded that I missed it. But A3 calls it a false FAIL "on the ordinary route" and "on a correct worker". That is wrong. `WORKER-CONTRACT.md:192` ("`/sc:brainstorm` ... `--output <dir>`") and spec line 142 (brainstorm row: `--output <dir>`, contract at `<output>/return-contract.yaml`) say a conforming brief passes `--output`, and with `--output` the worker fields are added to brainstorm's own contract (`brainstorm.md:154`). Under a conforming brief `domain` and `enrichment_used` ARE in the step 4 contract. R3-3 bites only a non-conforming brief that passes `--report-dir`. Real, but a P3 note. | Concede miss; reject "ordinary route" |
| 4 | F-16 called a "nit"; V1 never asks where the AC check equivalent to the verifier is (brief:34) (A2) | Partly conceded. I did not ask the brief:34 question. Answer to it: there is none, and the verifier is literal ("Constraints contains the quoted line", brief:201). But `/sc:implement` judges task ACs through a closed template (`qa.md:318`). The only Constraints hook is `quoted-constraint-breach` (`qa.md:52`), which needs a diff that violates a Constraints item; no diff can violate a sentence about when edits reach a live plan. So it cannot block execution: a recording gap, not P1. | Concede the gap; keep P2/note |
| 5 | My R1 claim that the brief's "commits and merges" is "weaker/less accurate" than the plan's wording (implied by A2, A3 agreeing only on substance) | I overstated. Spec 7.2 (line 282) describes the P1 case: commit to a feature or scratch branch. For a P2 author on another branch the edits must be on THAT worktree's base branch, which in practice means merged. The brief's sentence is not wrong; the plan's "a branch the live-check worktree is built from" is equivalent in effect but not the quoted line. | Concede: "plan's wording is the correct one" was too strong |
| 6 | A-1: Task 5's half is overstated; the AC says "prints 0", so `grep -c` exit 1 is irrelevant (A2) | Conceded. Task 5 uses the full path (plan:111), so `git show` works and the count is a real 0. Withdrawn. | Concede, withdraw Task 5 half |
| 7 | A-1: Task 4's half is narrower than presented, because "the same command" can be read as the same full path (A2) | Partly conceded. I ran both forms just now: `git show HEAD:refs/handoff-routing.md 2>&1 \| grep -c ...` prints 0, and the full-path form also prints 0. So the log cannot tell a missing file from a missing phrase. The vacuity is real only if the executor shortens the path; a careful reading of "the same command" avoids it. Narrowed to a P3 hardening note (add `git show` exit status or a positive control). Still the only reproduced mechanical weakness. | Concede scope; keep as note |
| 8 | A-4 "false as written" is soft because plan:21 calls the `.claude/` rewrite "output, not edits" (A3) | Partly conceded. plan:21 is about "edit only these six files". The Task 7 sentence says "it writes only ... under `./artifacts/`" while the same task runs `make sync-dev`, which writes `.claude/`. The word "only" is inaccurate, but the brief's own F-13 sentence (brief:169) has the same flaw. So the falseness is brief-owned and a nit. | Concede to nit |
| 9 | A-3 (no exit codes) overstated (my own R1 weakness; A2 and A3 call it low) | Stand by the narrow part only: the format-check observation (`pyproject.toml:50-54`, CI runs `ruff format --check`) is valid; the exit-code part is weak because `make` prints `Error N` on failure. | Concede exit-code part |
| 10 | S-002: V1 better calibrated (A2, A3 agree) | Not a criticism; accepted with the caveat in row 1. | n/a |

## Updated assessment

### (a) The listed-contract conflict (C-001 / X-001)

What the files say:
- plan:38 (copied from brief:229): "The nested contract is listed in `artifacts`, also when the call failed."
- plan:128 (copied from brief:217): "every `nested/analyze-` path listed in `artifacts` exists and holds its own `return-contract.yaml`" with no carve-out in that clause. The carve-outs ("`skipped`", "did not refuse that directory") attach only to the later "required only when" clause. The same sentence admits the per-source timeout "can stop `/sc:analyze` before it writes".
- `analyze.md:97-98`: contract written on every outcome once the directory is usable; unusable directory is refused, chat only, no contract.
- WC-4 (`WORKER-CONTRACT.md:31-32`): `artifacts` = "every other file written".
- `SKILL.md:388`: `artifacts` includes "the nested contracts". `handoff-routing.md:77`: timeout records `quality_tier: skipped`.

Is it a real false FAIL? Yes, on one narrow path. Reachability of each trigger:
- Refusal. The nested directory sits under the report directory that brainstorm already validated against the same rule set (`brainstorm.md:153` vs `analyze.md:97`). A refusal of `nested/analyze-<n>/` needs a creation or write failure. Effectively unreachable.
- Timeout. Wave 2A runs sources in parallel Task agents with a 120 s limit (`handoff-routing.md:77`). A `/sc:analyze` that is cut off before it writes is reachable. Then the skill says to list the nested contract ("also when the call failed"). A worker following WC-4 lists only what exists. A worker following the skill's "unconditionally" sentence lists the path. Check: FAIL on a run the spec calls correct (skip and record).
- Frequency evidence: the only real run on record (`lc10-result.md`, line 13) made no `/sc:analyze` call at all.

Severity: P2 (high end). It needs (analyze route taken) AND (timeout before write) AND (worker lists an unwritten file). It cannot block `/sc:implement` (it is text in a spec), and it is a false FAIL in a future live check, which the owner can see and overrule. The only P1-flavoured argument is that plan:133 states "no known false FAIL", and the plan itself holds the counter-fact (plan:128). That makes plan:133 untrue in the plan's own voice. I keep P2 and I keep that plan:133 is wrong.

### (b) Who owns the defect: the plan or the brief?

The brief owns the wording. Part 4 says "copy exactly, do not paraphrase" (brief:213). plan:38 equals brief:229; plan:128 equals brief:217. Brief:225 ("keep the nested contract listed in `artifacts` unconditionally, a failed call's included") and brief:237 ("no known false FAIL") are the brief's own claims. So the plan is faithful and the brief is internally inconsistent.

The plan owns two smaller things:
1. It repeated "no known false FAIL" (plan:133) while its own plan:128 sentence contains the counter-fact. Part 4 asks the plan to record the four residual risks; it does not forbid recording a fifth in the opposite direction. The plan records one deviation openly (plan:131), so it could have recorded this.
2. Nobody flagged the conflict to the owner. A plan-level reviewer's remedy is an owner decision on Part 4, not a unilateral reword by the plan (V3's proposal would itself be an unrecorded departure from Part 4).

### (c) Other disputed facts, checked this round

- X-002 / C-004 (earlier package untracked?). Run just now: `git status --porcelain -- .dev/tasks/to-do` shows the earlier package `...001016` as `A` (three files) and only `?? .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-021737/` untracked; `git ls-files` for the 021737 folder prints 0. R3-2's premise is false today. The `??`-to-`A` flip of this package is what plan:157 exempts. Unchanged.
- A-002 (does `/sc:implement` judge the brief's verifiers?). `qa.md:318`: a closed template filled with seven slots; the reviewer may not add, remove or reword any criterion. The plan's task ACs are what get judged. Brief verifiers for F-16 and F-13 are not ACs, and F-13's sentence is task body text. So C-002 and C-003 cannot block execution.
- C-011 (missing Depends-on). `sc-implement-protocol/SKILL.md:97`: "Default sequential in source order". Grep confirms the line exists. Task 1 runs first. R3-7 only bites a manual out-of-order run. I now side with A3: nit, no winner.
- C-007 (R3-3). See criticism row 3: brief table passes `--output`, so the sentence is right for conforming briefs.

### (d) F-16 and F-13 departure (C-002, C-003)

Classification: Necessary deviation (F-13, forced by F-2, which adds `status-after.txt` that is not a log) and benign Drift (F-16, a rewording that keeps the intent), both unrecorded. Neither blocks. Both are fidelity notes (P3/low P2) because the brief's own Part 3 says "Apply all of them" and each verifier is a literal quote. The cheapest repair is zero-cost: put the brief's literal F-16 line in Constraints (it is true and harmless), or add one sentence recording the departure next to plan:131. For F-13, record "the sentence names the status snapshot because F-2 adds it; `make sync-dev` also rewrites `.claude/`".

### Other variants, adversarial view

- V2: right that two literal verifiers are unmet and unrecorded; wrong at P1; R2-3 tagged Grounded though it is inference; blind to C-001 and C-005. Strongest on brief-fidelity discipline.
- V3: strongest evidence on C-001; R3-2 rests on a false premise; R3-3 overstated as "ordinary route"; R3-7 not reachable under the executor; blames the plan for brief-mandated text on R3-1, R3-4, R3-5, R3-6.
- V1: three real finds (C-005 narrowed, C-004, the reproduction), one mis-tag (A-2), one miss (R3-3), no P1 and no fix proposal.

## New evidence

1. `WORKER-CONTRACT.md:192` and spec line 142: a conforming `/sc:brainstorm` brief passes `--output <dir>`. This downgrades R3-3 / C-007 to a non-conforming-brief note.
2. `lc10-result.md:13`: the only real run made no nested `/sc:analyze` call. The C-001 path has not been observed.
3. Ran `git show HEAD:refs/handoff-routing.md ... | grep -c ...` and the full-path form: both print `0`. Confirms the log cannot tell "file missing" from "phrase missing" (C-005 narrowed to Task 4's routing half).
4. `qa.md:52`: `/sc:implement` does look at plan Constraints, but only for a diff that violates a Constraints item (`quoted-constraint-breach`). F-16's line is not diff-checkable.
5. Index today: earlier package `A`, this package `??` only.

## Proposed wording fix

Goal: remove the plan:38 / plan:128 conflict without touching the Task 1 tail, so the rule "keep the nested contract listed unconditionally, a failed call's included" (brief:225) is untouched.

Smallest change: one parenthesis inside the Part 4 live-check sentence (brief:217, copied to plan:128). Leave brief:229 and plan:38 as they are.

Replace, in the Part 4 "Task 6 live-check sentence":

```text
every `nested/analyze-` path listed in `artifacts` exists and holds its own `return-contract.yaml`, and every
```

with:

```text
every `nested/analyze-` path listed in `artifacts` exists and holds its own `return-contract.yaml` (not checked for a call whose `codebase` entry is `skipped` or whose directory `/sc:analyze` refused), and every
```

Why this works:
- It moves the two carve-outs that already exist in the "required only when" clause (`skipped`, "did not refuse that directory") forward to the "listed paths exist" clause, so both clauses agree.
- A call that crashes but is recorded `failed` still has to have written a contract (`analyze.md:98`, WC-4), so a missing file there is a true FAIL. This is the intent of the unconditional-listing rule.
- Task 1's tail "The nested contract is listed in `artifacts`, also when the call failed." and its AC (plan:45) stay byte for byte.
- No test pin changes. The Task 6 ACs (plan:142-143: `lc10`, `a source: codebase entry`, `neither quality_tier nor source records`) still hold.
- Matching edit in the plan: the same parenthesis in plan:128, and either keep plan:133 or add a fifth residual note: "A `/sc:analyze` call cut off by the per-source timeout may leave a listed path with no contract; the carve-out in the first clause covers it."

Not recommended: changing Task 1's tail to "listed whenever written". It is the brief's F-14 text, it would break the Task 1 AC (plan:45), and it reintroduces a condition that brief:225 forbids.

Optional hardening notes (not part of the fix): add the full repo path to Task 4's second `git show` command (plan:95) and require `git show` to exit 0; record the F-16 and F-13 departures in one sentence beside plan:131.

## Final diff-point positions

| Point | Final superior position | Changed since Round 1? | One-line evidence |
|---|---|---|---|
| S-001 | none | no | Counts reflect depth and bias, not correctness; V2's P1 and V3's second P1 do not survive checks |
| S-002 | V1 | no | V1 tags A-3, A-5 INFERRED correctly; caveat: its A-2 tag was wrong for the text conflict (`analyze.md:97-98` is on disk) |
| C-001 | V3 | no | plan:38 vs plan:128 vs `analyze.md:97-98`; real only on timeout; P2; wording is brief-owned (brief:217, 229, 237) |
| C-002 | split (V2 on recording, V1 on severity) | no | Verifier literal (brief:201) and unrecorded; no AC can judge it (`qa.md:318`); I withdraw "plan wording is more correct" |
| C-003 | V2 | yes | Widening forced by F-2 and unrecorded; "only" is also untrue due to sync-dev, but brief:169 has the same flaw |
| C-004 | V1 | no | Index run today: earlier package `A`, only this package `??`; exempted at plan:157 |
| C-005 | V1 | no | Reproduced: short and full path both print 0; narrowed to Task 4 routing half (Task 5 half withdrawn) |
| C-006 | V1 | no | Only raiser; format-check point valid (`pyproject.toml:50-54`), exit-code point weak; low |
| C-007 | V3 | no | `brainstorm.md:154`, `SKILL.md:369-381`; but briefs pass `--output` (`WORKER-CONTRACT.md:192`), so note-level only |
| C-008 | V3 | no | Only raiser; out-of-scope note, the fix needs a seventh file (plan:21) |
| C-009 | V3 | no | `handoff-routing.md:77` records `skipped` on timeout; brief-mandated wording (brief:230) |
| C-010 | V3 | no | Spec already names Skill and Agent tools (`spec:62`); only Task inferred (plan:135) |
| C-011 | none | yes | `sc-implement-protocol/SKILL.md:97` runs tasks in source order; Task 1 always first |
| C-012 | V2 | no | Only V2 checked matrix coverage; plan satisfies the spans; low |
| C-013 | none | no | All agree line 286 begins "4. Check the contract"; cosmetic |
| C-014 | none | no | All three confirm pins, slices and the byte-for-byte Part 4 copy |
| X-001 | V3 | no | Conflict real, fix belongs in brief Part 4; P2 (timeout path, unobserved in `lc10-result.md:13`), not P1 |
| X-002 | V1 | no | `git status` today: earlier package `A` |
| X-003 | split | no | Not P1 (Constraints line not an AC, `qa.md:318`); both V1 and V2 partly right; see C-002 |
| X-004 | V2 | yes | Necessary deviation (F-2), unrecorded; V1's extra point is brief-owned |
| X-005 | split (V1, V2) | no | Executor ledger stays in the package (`implement.md:58`); other `.dev/` writers unenumerated and unmeasured |
| A-001 | QUALIFY | no | Holds for a usable directory (`analyze.md:97-98`), not for a caller timeout (`handoff-routing.md:77`, plan:128) |
| A-002 | QUALIFY | no | `/sc:implement` judges task ACs through a closed template (`qa.md:318`); brief verifiers are not ACs |
| A-003 | QUALIFY | no | Tree matches today; before/after snapshot absorbs pre-Task-1 drift; only mid-run untracked paths matter |
| A-004 | ACCEPT | no | Brief mandates exact pins; slices supply placement |
| A-005 | QUALIFY | no | Reviewer convention; plan:131 sets the recording habit, so omission is a note, not a blocker |
