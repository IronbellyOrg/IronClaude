# Round 1 advocate statement: Variant 3 (Proposal C, no coordinator yet)

Persona: qa (edge cases, failure scenarios, risk). Depth: quick. Read-only; this file is the only write.

## Position summary

Variant 3 is the lowest-risk answer at W0: it is the spec's own default, the W0 exit row explicitly accepts it ("XC-09 open, or held on Q26's default", `merged-requirements.md:860`), and it makes no irreversible move while the three facts that decide the home (Orca reachability, whether an `--agent` launch is person-opened, whether the docs branch is finished) are still open. Its honest cost is that it defers rather than answers, so I argue it as the right answer for now, with a hard re-ask trigger, not as the long-term home.

## Steelman of Variant 1

Strongest version: the coordinator home must be isolated, and only a dedicated worktree gives isolation by construction. The ledger package is always staged (project `CLAUDE.md:35`), and staged files live in the checkout's index, so the safest place for them is a checkout that only the coordinator ever uses and that never changes branch. V1 gives exactly that: a new branch from `origin/master` that holds nothing but program files, so a later "commit the ledger" is clean (V1 "What it unlocks"). It uses the exact creation form the spec itself prescribes for top-level agents (`orca worktree create --name <name> --base-branch origin/master --agent claude --prompt "<task>"`, `merged-requirements.md:954`), and the project rules expect humans to create worktrees with agents ("A worktree a human creates needs an agent too", project `CLAUDE.md:312`). It leaves the main checkout and its 21 untracked entries untouched (V1 step 4). What it genuinely gets right: it is the only variant that solves A-001 and A-002 structurally rather than by owner discipline, and it is honest about its own weak point (V1 "What it costs or risks", first bullet, marks person-opened UNVERIFIED).

## Steelman of Variant 2

Strongest version: the coordinator must be person-opened (XC-09 (1), `merged-requirements.md:457`), and V2 is the only variant where that is certain, because the owner opens the session by hand (V2 step 3). It is the spec's recommended answer (`question.md:11`), it uses the only existing home the invariant probe found rule-conforming (`invariant-probe.md:10`), and its first step is git only, so it does not wait on Orca to put the ledger on disk; XC-01 can be kept before XC-09 exists (`merged-requirements.md:457`, blocks column). It comes with measured evidence that the docs branch is already safe to leave: 0 unpushed commits, no modified tracked files, no PR (`question.md:32`; V2 step 1). What it genuinely gets right: it removes the one UNVERIFIED premise V1 rests on, and it keeps the grant table on disk where agents can read it, which V3 does not.

## Key strengths claimed

1. **It is the sanctioned default, and the wave plan accepts it.** The default text is verbatim in the spec (`question.md:15`), and the W0 exit criteria read "XC-09 open, or held on Q26's default" (`merged-requirements.md:860`). V3 needs no rule bent to be valid.
2. **No action is taken on unverified premises.** V1 rests on an `--agent` launch counting as person-opened, which no source confirms (`question.md:34`; `refactor-plan.md:90`, `:618`). The spec's own vocabulary makes this worse for V1: XC-09 (3) and 6.2 call an agent started by `orca worktree create --agent` "a top-level agent" (`merged-requirements.md:457`, `:951`), while XC-09 (1) requires "A person opens it". V3 does not stake the program on that reading.
3. **The coordinator cannot start anyway until Orca answers.** Edge 118 requires ORCA-AVAILABLE before XC-09 (`question.md:19`), and the probe found Orca unreachable on 2026-11-13 (`merged-requirements.md:604`; current state UNVERIFIED). So V1 and V2 buy no dispatch progress today that V3 forgoes; they only pre-commit a home.
4. **It avoids V2's always-staged leak entirely.** In V2 the ledger sits staged in the index of the owner's general working checkout. Any plain `git commit` there commits everything staged, so the ledger rides into the owner's next unrelated commit, on the program branch or after a switch back (standard git behaviour; A-001). That breaks "committed only when the owner asks" (`merged-requirements.md:449`, `:976`) silently. V3 has no staged ledger to leak.
5. **The deferral is short and bounded by a concrete trigger.** V3 step 4 re-asks Q26 when the first worker-dispatched item (edge 119) is next, with the then-current Orca and checkout state. Those items sit in W1 (WA-01, WA-03, XC-05, V2-05, `merged-requirements.md:861`), so the re-ask lands at W1 entry, not "someday".
6. **Grant authorship is the owner's in every variant.** 6.8 says of each grant row: "Each row is itself the owner's approval; no agent writes one" (`merged-requirements.md:1047`). Keeping rows in the owner's own notes does not change who writes them; it changes only who can read them (see Concessions).
7. **The work that does not need a coordinator keeps moving.** SW-01's ruling never waits for the ledger (`question.md:36`; `refactor-plan.md:91`); SW-03 and SW-06 in W0 are run by the #539 author and on GitHub, not dispatched (`merged-requirements.md:860`).

## Weaknesses identified in Variant 1

1. **The person-opened premise is unverified, and the spec's words lean against it.** V1 admits it (V1 "What it costs or risks"); the spec labels `--agent` agents "top-level agent" (`merged-requirements.md:457`, `:951`). If the owner or a reviewer later rules that this is not a coordinator, every dispatch it made sits on uncertain authority, including who may run `worker-start`. Failure scenario: XC-11's independent gate (`merged-requirements.md:459`) checks "the honest built and unbuilt status" and flags the coordinator as not person-opened.
2. **First step needs Orca, which was down.** The worktree cannot be created without Orca (V1 risk bullet 2; `merged-requirements.md:604`). Picking V1 today produces the same state as V3 until Orca answers, plus a recorded commitment.
3. **A prompt-launched coordinator can start with the wrong brief.** A launch receipt is not proof that the brief loaded (V1 risk bullet 4; owner memory `orca-worker-resume-verify-screen.md`). A coordinator that runs without the spec, ADJ and worker contract loaded is a top-level agent with worktree powers and no rules. The mitigation (the person reads the first screen) is manual.
4. **Resume behaviour is unverified.** If the Orca-launched coordinator ends and resumes, it needs `run-use` to rebind (owner memory `orca-coordinator-rebind-after-resume.md`); whether an `--agent` session can hold a coordinator Run binding at all is UNVERIFIED.
5. **Host load.** One more worktree on a host with 19 (V1 risk bullet 3; `invariant-probe.md:10`). Low.

## Weaknesses identified in Variant 2

1. **Always-staged ledger in a shared index.** Covered in strength 4: any plain `git commit` in the main checkout, on any branch, takes the ledger with it. V2 notes only the narrower `git add .dev` risk (V2 risk bullet 1, U-004); the wider risk is that the ledger is already staged, so no `git add` is needed at all.
2. **Branch switch carries staged state (A-001).** If the owner later switches the main checkout back to a docs branch, the staged ledger travels with the index and can be committed there, the exact outcome Q26's wording warns against (`question.md:7`).
3. **Concurrency in the owner's general workspace (A-002).** Spec 6.2: "one worktree never holds two live agents" (`merged-requirements.md:951`). V2 makes the owner's everyday checkout the coordinator's for weeks (V2 risk bullet 1). Any second session the owner opens there breaks 6.2. I checked one candidate collision: the 409 session runs in `issue-409-mvp`, not the main checkout (`merged-requirements.md:898`), so the risk is the owner's own ad hoc sessions; whether any is live now is UNVERIFIED.
4. **It does not follow the rule it cites literally.** The project line says "Session A: Open the main checkout (current branch)" (project `CLAUDE.md:336`). V2 switches the branch first, so it follows the place but not the "(current branch)" part. The line sits in a "Usage" list of examples, so its force as a rule is itself unsettled (V1 "What stays unresolved").
5. **Switch edge case.** `git switch` refuses when an untracked file in the working tree would be overwritten by a tracked file on the target branch. The 21 untracked entries are under `.claude-audit/` and `.dev/` (`question.md:32`); whether `origin/master` tracks any of those exact paths is UNVERIFIED. V2's own text says only that tracked changes would be refused (V2 risk bullet 2).

## Concessions

1. **V3 answers nothing.** It is a deferral; "Everything Q26 asks" stays open (V3 "What stays unresolved").
2. **The grant table off disk is a real risk.** W0 already needs grant rows: `GRANT(SW-03,push)`, `GRANT(SW-03,thread-resolve)`, `GRANT(SW-06,issue-write)` (`merged-requirements.md:860`). An edge "is satisfied only by a matching row" (`merged-requirements.md:607`). With the ledger in the owner's notes, the #539 author session cannot check a row from disk and must take it from chat, where wording can drift from the owner's notes. V1 and V2 are better here (X-003).
3. **"Ledger exists" is ambiguous under V3.** The W0 exit row also needs "ledger exists" (`merged-requirements.md:860`), and 6.4 rule 3 says "before W0 exits the owner names the coordinator's home" (`merged-requirements.md:976`). That rule and the W0 exit row's "or held on Q26's default" disagree; V3 depends on the W0 row winning and on a hand ledger counting as "the ledger". Both readings are UNVERIFIED.
4. **Most of W1 waits.** WA-01, WA-03, XC-05 and V2-05 are dispatched items (`question.md:20`; `merged-requirements.md:861`), so V3 stalls W1 until Q26 is re-asked and answered.
5. **The re-ask has no mechanical trigger.** Only the owner notices that the first dispatched item is next. If nobody notices, the program stalls without a visible blocker, which is the failure mode QA should fear most.
6. **If Orca answers at W0, V3 loses its main timing argument.** Strength 3 depends on ORCA-AVAILABLE being false; once it reads back, the deferral only costs time.
7. **It conflicts in spirit with the always-staged practice** for program state (V3 "What it costs or risks", bullet 3).

## Shared assumption responses

| id | response | reason |
|---|---|---|
| A-001 | REJECT (the assumption as stated) | "Staged on branch X" is not a stable fact in git: staged files live in the index and follow the checkout, so the claim holds only where the checkout never switches and nobody else commits there. That is true of V1 by construction and false of V2 (strength 4, V2 weaknesses 1 and 2). V3 avoids it by having nothing staged. The spec should say "staged in checkout X, which never changes branch" instead of "on branch X". |
| A-002 | QUALIFY | Holds for V1 by construction (a dedicated worktree, 6.2 `merged-requirements.md:951`). For V2 it holds only if the owner moves all other main-checkout work elsewhere for the program's life; the 409 session is not a collision (it is in `issue-409-mvp`, `merged-requirements.md:898`), but the owner's own sessions may be (UNVERIFIED). Moot for V3. |
| A-003 | ACCEPT | Stated and sourced: edge 118 and ORCA-AVAILABLE (`question.md:19`; `merged-requirements.md:604`). It applies to XC-09 in every variant, and to V1's first step as well; V2's branch switch and on-disk ledger do not need it. It is the main support for V3's timing argument and its main expiry condition. |

## Per-point verdicts

| point | superior variant | one-line reason |
|---|---|---|
| S-001 | none (tie) | All three use the same five sections with four steps; no structural difference to judge. |
| C-001 | V2 | The only home where the coordinator is certainly person-opened today; V1 rests on an unverified premise and V3 has no home. |
| C-002 | V1 | A dedicated branch in a checkout that never switches is the only place "staged on that branch" stays true (A-001). |
| C-003 | V2 | Its first action is git only, so it can put the ledger on disk while Orca is down; V1 needs Orca, V3 takes no step. |
| C-004 | V1 | Leaves the main checkout untouched like V3 while still making progress; V2 occupies the owner's general workspace for weeks. |
| X-001 | V2 | Person-opened is certain only when the owner opens the session by hand; the spec calls V1's agent "a top-level agent". |
| X-002 | V2 | It follows the project's named place for the orchestrator, though not its "(current branch)" wording, and the line may be only an example. |
| X-003 | V1 | Grant table on disk and isolated from other work; V2 also on disk but in a shared index; V3 off disk is weakest. |
| A-001 | V1 | Its checkout never switches, so the staged ledger cannot travel to another branch or ride into an unrelated commit. |
| A-002 | V1 | One coordinator per dedicated worktree by construction; V2 depends on owner discipline in a shared checkout. |

Overall QA reading: V3 is the safest answer for the moment Q26 is asked if Orca is still unreachable, provided the re-ask is recorded as an explicit ledger hold with a trigger at W1 entry. Once Orca answers, the risk balance favours V1 if person-opened is confirmed and V2 otherwise, with V2 needing a rule that the main checkout carries no other commits while the ledger is staged there.
