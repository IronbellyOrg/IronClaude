review: 1 of 3

# /sc:spec-panel critique, round 1

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (matches the hash in `review/lint-1.md:1`)
- baseline: missing (first review; no `--re-review`/`--baseline`)
- reviewer model: claude-sonnet-5-5
- mode: critique; focus: requirements, architecture; first review of the full document, one reviewer (the two-review merge of the loop prompt is not run in this sandbox)
- lint evidence: `review/lint-1.md:3-5` reports Checks REF, Findings 0. No lint id to address. Nothing in it fails or passes the review.
- evidence checked: `README.md`, `inventory/orca-capabilities.md` (CAPS), `inventory/commands-a.md` (INV-A), `inventory/commands-b.md` (INV-B). Every `src/`, `sk/`, `cmd/`, `CLAUDE.md`, `pyproject.toml`, `Makefile` and `orca-ide` guide citation that is not quoted in those inventories is UNVERIFIED here. A claim that rests on the inventories alone is marked as such.
- coverage: whole spec; requirements WC-1..WC-12, SA-1..SA-6, sections 3-4 and 6, every acceptance criterion in section 7 (AC-C1..C5, 7.2 steps 1-7, AC-0.1..0.4, AC-1.1..1.4, AC-2.1..2.5, AC-3.1..3.4, AC-4.1..4.3) and the open decisions.

## Panel summary (critique order: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower)

The architecture decision (Orca on top, commands stay units of work) is argued with evidence and the rejected alternative is stated with reasons (`spec:13-39`). The weaknesses are in the testability of the section 7 criteria: several cannot pass for every command or phase they cover, and a few depend on two spec texts that disagree about where the report file lives or which commands carry the change.

No guard-condition table is produced: the spec is a requirements document, not a stateful design with numeric guard conditions. The panel states "No guard conditions identified". The acceptance criteria were examined one by one instead (table below).

## Blocking findings

### B1 [CRITICAL-in-effect, expert: Crispin / Wiegers] AC-0.4 cannot pass: live-check step 3 demands a WC-4 contract that does not exist in Phase 0

- Stated text A: step 3 pass condition "exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path" (`spec:182`).
- Stated text B: AC-0.4 "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1" (`spec:194`); P0 makes no command edits (`spec:158`).
- An implementer who follows the stated text as written builds P0 smoke runs of `/sc:troubleshoot` (report `REPORT.md`, `spec:91`) and `/sc:adversarial` (contract filename "not fixed", `spec:83`) and then checks step 3. Step 3 requires the report path to be the WC-4 `return-contract.yaml` and the outcome to match its `status`; neither exists before P1, so step 3 cannot pass, and AC-0.4 exempts only step 4. The gate for P0 ("a failure here reopens section 1", `spec:194`) therefore fails for a reason unrelated to the decision it is meant to test.
- Recommendation: state in step 3 that, in P0, the report path is the command's existing report file and the outcome is judged from its own status; or exempt step 3's contract clauses in AC-0.4 as well.

### B2 [MAJOR, blocking, expert: Wiegers / Cockburn] AC-1.1 and AC-1.2 require a contract and an `## Unattended mode` section from `/sc:load`, which the spec says gets neither

- Stated text A: AC-1.1 "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`" (`spec:195`). `/sc:load` is a row of section 3.2 (`spec:112`).
- Stated text B: the `load` row gives Report "none (see note)", "use it as a step inside another worker's brief, not as its own Task" (`spec:112`); Decisions: "a report file would be an unrequested addition" (`spec:265`). P1 lists `load (usage line only)` (`spec:159`) but also says the P1 scope is "the WC-4 contract in unattended mode" for the section 3 commands (`spec:159`).
- An implementer who follows the text builds, for `load`, a usage-line fix only (rows 112, 159, 265). AC-1.1 then fails for `load` because no section naming `return-contract.yaml` exists, and AC-1.2 ("7.2 live check on each P1 command with `--unattended --output <dir>`", `spec:196`) fails at steps 3-4 (no `worker_done` contract path, `test -s <contract>` on a file that is never written). If the implementer instead adds the section and contract, the Decision at `spec:265` is violated.
- Recommendation: exclude `load` from AC-1.1/AC-1.2, or reverse the Decision.

### B3 [MAJOR, blocking, expert: Fowler / Cockburn] AC-1.1 and the P1 scope require an unattended section on `pr-submit`, `implement` and `post-release`, but the recommended decisions D2-D4 and Phase 4 say those commands are not changed or are not workers

- Stated text A: AC-1.1 covers "every command in sections 3.1-3.2" (`spec:195`); P1 scope "the `--unattended` flag accepted by every command in sections 3.1 and 3.2" (`spec:159`). `pr-submit`, `implement`, `post-release` are rows of section 3.2 (`spec:109,113,114`).
- Stated text B: Phase 4 owns them and "waits for answers to D2-D4" (`spec:154,162`); D3 recommendation (a) "Coordinator or person only ... no pr-submit changes in Phase 4" (`spec:240-242`); section 4 says `pr-submit` "stays a worker candidate only if the user accepts open decision D3" (`spec:139`); the same section gives coordinator-only commands "no `--unattended` mode" (`spec:128`).
- An implementer who follows the text builds, for the recommended D3(a), no pr-submit change in P4, but AC-1.1 in P1 requires a `## Unattended mode` section in `pr-submit.md`. Both cannot hold: either P1 gives pr-submit a worker mode before the user has decided (contradicting "Phase 4 waits"), or AC-1.1 fails. The same holds for `implement` (D2) and `post-release` (D4) whenever P1 requires the flag but the gate resolution (`spec:109,113`) arrives only in P4.
- Recommendation: restrict P1/AC-1.1 to the commands whose phase is P1-P3, or move the flag acceptance for the P4 commands into P4.

### B4 [MAJOR, blocking, expert: Hohpe / Wiegers] WC-4's report location contradicts section 3 rows, so the section 7.2 steps 3-4 and AC-1.2 cannot pass for adversarial, workflow, cleanup-audit and index-repo

- Stated text A: WC-4 "the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed", "known before dispatch" (`spec:62`); 7.2 step 3-4 check that path (`spec:182-183`); AC-1.2 runs every P1 command "with `--unattended --output <dir>`" (`spec:196`), and P1 includes fixes to adversarial, cleanup-audit, index-repo, workflow (`spec:159`).
- Stated text B (section 3.1):
  - adversarial: fix the contract to `<output>/adversarial/return-contract.yaml` (`spec:83`), a subdirectory, not `<output-dir>/return-contract.yaml`. AC-1.4 only asks that "adversarial names one fixed path" (`spec:198`), so it does not choose between the two.
  - workflow: brief passes only `--handoff none`; the contract is at `.dev/tasks/to-do/<id>/return-contract.yaml` (`spec:92`; INV-B workflow entry, `commands-b.md` line 52 of the table and the `/sc:workflow` (d) note: id is generated by the command, and the contract is "Not written for pre-creation STOPs"). The path is not known before dispatch, no output directory is passed, and for a pre-creation STOP no `<id>` directory exists, so the "write the contract for pre-creation STOPs too" fix (`spec:92`, AC-1.4) has no stated location.
  - cleanup-audit: "output dir is fixed" `.claude-audit/` (`spec:85`), so no `--output <dir>` exists to pass.
  - index-repo: brief passes "none", location only implied, and the P1 fix is "State the output location" (`spec:86`); no output flag is added although P1 says "output flags for commands that lack one" (`spec:159`).
- An implementer who follows the stated text builds, for these four, a contract at the place section 3 names. WC-4, step 3 ("report path is the WC-4 contract path"), step 4 (`test -s <contract>`) and AC-1.2 then point at a path that is not where the file is, or at an `--output` flag that the command does not accept. The criteria cannot pass as written for those four commands, and the adversarial rows contradict WC-4 directly.
- Recommendation: add to WC-4 the exception list (path per command, coordinator-known), or fix each command's contract to `<output-dir>/return-contract.yaml` and give workflow, cleanup-audit and index-repo an output flag.

### B5 [MAJOR, blocking, expert: Crispin / Adzic] AC-2.2 requires every P2 command to end `blocked` with a `blocked_question`; several P2 commands have no blocking path

- Stated text A: AC-2.2 "Gate-trigger run per P2 command ... `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`" (`spec:200`). P2 lists auggie-review, cleanup, improve, cli-eval, cli-portify, recommend, research, review-translation, spec-panel, task, tasklist, reflect, release-split, tdd, troubleshoot (`spec:160`).
- Stated text B: the gate resolution of several of these is not "blocked":
  - research: `--unattended` "pins `--strategy planning`" (`spec:116`);
  - tasklist: Stage 10.5 "passes `--unattended` to each reflect so the headless rule applies" (`spec:122`);
  - auggie-review: implies `--no-post-pr` and `--no-remediation-offer` (`spec:100`);
  - cleanup and improve: apply only items outside "Approval Required", list the rest (`spec:103,110`);
  - reflect: follows "the existing headless auto-accept rule" (`spec:88`).
- An implementer who follows the text builds those commands to complete with a default; no input makes them write `status: blocked`. AC-2.2 therefore cannot pass for them as written, and AC-2.1 ("one assertion per gate listed in the section 3 row") and AC-2.3 are the only checks that can. The example inputs in AC-2.2 (`tdd "auth"`, `cli-eval run` without `--suite`) fit only the blocked-type commands.
- Recommendation: restrict AC-2.2 to the commands whose row says "blocked", and give the default-resolution commands a check of their own (the default applied, no `agentWait`).

## Follow-up candidates (Medium, never fail the review, not in the Reviser brief)

- M-a (AC-C1, `spec:172`): the grep covers `src/superclaude/core`, where P0 adds `WORKER-CONTRACT.md` and an Orca section in `HOW-WE-WORK.md` (`spec:158`). SA-2 allows an Orca mention in the contract file "as an example of a caller's question channel" (`spec:147`). Whether that text will contain the string `orca orchestration ask` (which the grep matches) is a choice the spec does not make, so AC-C1 may fail on the spec's own P0 output. UNVERIFIED which wording the files will use. Medium: needs a guess.
- M-b (AC-C5 / SA-4, `spec:176,149`): additive-only edits. Section 3 asks for new flags on commands (`--output`, `--unattended`), and if those are documented by editing the existing Usage line, `git diff -U0 | grep '^-[^-]'` prints that line. The spec does not say whether flags are added as new lines. Medium: needs a guess.
- M-c (AC-C3, `spec:174`): baseline and re-run cover `tests/skills/` only, while P2/P3 edit commands and skills that other test directories may pin (CLAUDE.md names `tests/skills/test_primitive_dual_surface_lookup.py`; the wider suite is UNVERIFIED here). A regression outside `tests/skills/` is not caught.
- M-d (AC-1.3 `spec:197`, AC-4.3 `spec:210`, 7.2 `spec:180`): "a scratch worktree" / "scratch fork PR". The repo rule quoted in the task context (CLAUDE.md, Orca worktree rule; UNVERIFIED in this sandbox) says worktrees are created only through Orca with an agent. The criterion does not say how the scratch worktree is made.
- M-e (AC-1.4, `spec:198`): the check is a `grep -n` whose pass condition ("adversarial names one fixed path", "workflow states ... pre-creation STOPs") needs a human reading; it is not a mechanical pass/fail. See also B4.
- M-f (AC-2.2 vs WC-3, `spec:200,61`): WC-3 lets the worker `ask` the coordinator instead of ending `blocked`. A gate-trigger run in which the worker asks produces a `question`, not `worker_done --outcome failed`. The criterion should say the brief forbids `ask`.
- M-g (7.2 step 5 and AC-3.2, `spec:184,205`): a text search of the transcript for `AskUserQuestion` or `[Y/n]` can hit the command's own text (the Unattended-mode section says "never calls `AskUserQuestion`", `spec:60`). The pass wording "no `AskUserQuestion` call" is workable, but "no `[Y/n]` in the transcript" is not.
- M-h (7.2 step 4, `spec:183`): `import yaml` relies on "PyYAML is a declared dependency, `pyproject.toml:38`"; that line is UNVERIFIED here.
- M-i (E2, `spec:22`): cites `CAPS:161` for `[H:worker-start]` line 38 / `--agent claude`; `CAPS:161` is the pr-submit top-level rule (`orca-capabilities.md:161`). The `--agent claude` fact is not at that line. Citation defect; the claim itself is not shown wrong.
- M-j (phases): `brainstorm` and `init-lite` are "None" in the small-fix column (`spec:84,87`) and appear in no phase list (`spec:158-162`), but P1 says every 3.1 command accepts `--unattended` (`spec:159`). Who adds the flag to them is not stated.
- M-k (AC-2.4, `spec:202`): `gh api .../reviews --jq length` returns at most one page (default 30); counts above that would be truncated. Low risk on a scratch PR.

## Acceptance criteria and live-check steps, one by one

Pass-as-written column: Y = can pass for every command and phase it covers; N = cannot (a finding above); Y* = can pass, with a Medium note.

| Criterion | Pass as written? | Reason |
|---|---|---|
| AC-C1 (`spec:172`) | Y* | M-a; the SA-2 exception wording is not tied to the grep pattern. |
| AC-C2 `make verify-sync` (`spec:173`) | Y | Mechanical; Makefile target UNVERIFIED here (`CLAUDE.md` names it). |
| AC-C3 (`spec:174`) | Y* | M-c. |
| AC-C4 (`spec:175`) | Y | Mechanical. |
| AC-C5 (`spec:176`) | Y* | M-b. Also uses `master...HEAD`, so it is cumulative across phases (fine for additive edits). |
| 7.2 step 1 (`spec:180`) | Y | Flags match CAPS:46,84; exit 0 and `state: ready`. |
| 7.2 step 2 (`spec:181`) | Y* | `agentWait` is quoted at CAPS:129. For a gate-trigger run in which the worker uses `ask`, see M-f. |
| 7.2 step 3 (`spec:182`) | N | B1 (P0), B4 (adversarial/workflow/cleanup-audit/index-repo), B2 (load). |
| 7.2 step 4 (`spec:183`) | N | B4 and B2: no contract at the stated path for those commands; M-h. |
| 7.2 step 5 (`spec:184`) | Y* | `worker-read --source transcript` is supported (CAPS:131,140); M-g. |
| 7.2 step 6 (`spec:185`) | Y* | "Documented artifacts" covers `.claude-audit/`, `PROJECT_INDEX.md`, `claudedocs/`; only if the brief lists them. |
| 7.2 step 7 (`spec:186`) | Y | CAPS:113 quotes the `worker-list --terminal-state reclaimable` rule. |
| AC-0.1 (`spec:191`) | Y | Mechanical once the name is added (`install_core.py` UNVERIFIED here). |
| AC-0.2 (`spec:192`) | Y* | Level-table test name not given; UNVERIFIED. |
| AC-0.3 (`spec:193`) | Y | Mechanical. |
| AC-0.4 (`spec:194`) | N | B1. |
| AC-1.1 (`spec:195`) | N | B2 (load), B3 (pr-submit, implement, post-release). |
| AC-1.2 (`spec:196`) | N | B2, B4 (index-repo and cleanup-audit take no `--output <dir>`; workflow path generated). |
| AC-1.3 (`spec:197`) | Y* | M-d. |
| AC-1.4 (`spec:198`) | N/Y* | M-e; its adversarial half depends on B4 (path undecided). |
| AC-2.1 (`spec:199`) | Y | Per-row string assertions. |
| AC-2.2 (`spec:200`) | N | B5; M-f. |
| AC-2.3 (`spec:201`) | Y | Happy-path with required flags. |
| AC-2.4 (`spec:202`) | Y* | M-k. |
| AC-2.5 (`spec:203`) | Y* | Manual check; no mechanical oracle. |
| AC-3.1 (`spec:204`) | Y | Assertion on filenames/flags, provided the roadmap and validate-roadmap files are fixed as row 118/124 say. |
| AC-3.2 (`spec:205`) | Y* | M-g. |
| AC-3.3 (`spec:206`) | Y | Depends on the validate-tests default-target fix (`spec:125`). |
| AC-3.4 (`spec:207`) | Y | Per-session files vs single-owner hashes. |
| AC-4.1 (`spec:208`) | Y | Consistent with D2(a); D2(b) branch stated. |
| AC-4.2 (`spec:209`) | Y | |
| AC-4.3 (`spec:210`) | Y* | Applies only if D3(b); M-d. |

## Whittaker attack notes (adversarial)

- I can break this specification by the **Sequence Attack**. The invariant at `spec:154` ("Phase 4 waits for answers to D2-D4") fails when P1 runs first as ordered and AC-1.1 (`spec:195`) demands the unattended section for `pr-submit`. Concrete attack: before D3 is answered, P1 must add the section; after D3(a) the section should not exist (`spec:240-242`). This is B3.
- I can break this specification by the **Sentinel Collision Attack**. The invariant at `spec:62` ("`<output-dir>/return-contract.yaml`") fails when a command's own fixed contract name sits in a subfolder (`<output>/adversarial/`, `spec:83`). This is B4.
- I can break this specification by the **Divergence Attack**. The invariant at `spec:200` (every P2 gate ends `blocked`) fails for commands whose gate resolves by default (`spec:116,122`). This is B5.

## Verification notes

- Facts I checked against inventory text: `worker_done` outcome vocabulary (CAPS:73), the heartbeat cadence being from the preamble (CAPS:130), worker-release and `reclaimable` rule (CAPS:107-113), `worker-read` sources (CAPS:131,140), workflow contract timing (INV-B workflow notes). They match the spec's use of them.
- The count 10 / 27 / 6 = 43 matches the rows in sections 3.1, 3.2 and 4 (10, 27, 6 rows).
- UNVERIFIED (not checkable in the sandbox): every `src/superclaude/...`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `HOW-WE-WORK.md` line citation; the spec's own claim that 11 locations were re-read and about 340 citations were validated (`spec:11,285`).

## Reviser brief

Applies to blocking ids B1, B2, B3, B4, B5 only. Rules: revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; cite the finding id on each added paragraph or table; prefer deleting or narrowing to adding; report the spec's byte size before and after and the bytes added and deleted per finding id; leave minor and Medium findings (the follow-up candidates) untouched.

- B1: `spec:182` (step 3) against `spec:194` (AC-0.4): P0 has no WC-4 contract, so step 3's contract clauses cannot pass in P0.
- B2: `spec:195` (AC-1.1) and `spec:196` (AC-1.2) against `spec:112` and `spec:265`: `load` gets no contract and no unattended section.
- B3: `spec:195` and `spec:159` against `spec:154,162,240-242,139`: P4 commands (pr-submit, implement, post-release) are required to carry the section in P1 although their change waits for D2-D4.
- B4: `spec:62,182-183,196` against `spec:83,85,86,92,159`: report location for adversarial, workflow, cleanup-audit and index-repo.
- B5: `spec:200` against `spec:88,100,103,110,116,122`: P2 commands without a blocked path.

verdict: FAIL
