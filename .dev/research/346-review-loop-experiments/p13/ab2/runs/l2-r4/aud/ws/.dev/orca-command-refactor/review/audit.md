review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (critique, requirements + architecture)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `64ace65d5ab1437b097ef30b7325e413a6e90e0ea575952d431a0fa4c73ce23e`
- baseline: none given (first review of the whole document, labelled whole-document audit)
- reviewer model: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`
- shared context read first: `.dev/orca-command-refactor/README.md:1-39`

Citation convention: `S:N` = line N of the candidate spec. `INV-A:N`, `INV-B:N`, `CAPS:N` = `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. Candidate lines were read in this sandbox. Source lines under `src/superclaude/...`, `~/.claude/...`, Orca's installed files and `CLAUDE.md` are not in the sandbox. I checked them only through what the inventories quote, and I mark each one UNVERIFIED where I rely on it.

## Coverage

Read in full: the spec (S:1-285), all three inventories, and the README. Covered by the experts in sequence: Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard, Whittaker, Newman, Hohpe (architecture and attack); Crispin and Gregory (acceptance checks); Hightower (operations). Cross-checked:
- every `INV-*` and `CAPS:*` citation in sections 1, 2 and 4 against the inventory line it names (all found as cited);
- the 10 / 27 / 6 verdict split against `INV-A:73` and `INV-B:278`;
- the phase assignments in S:99-125 and S:156-162 against the section 3 tables;
- the acceptance checks in S:166-210 against the requirements they test.

Not covered: the correctness of the inventories' own `src/` citations, and Orca's compiled behaviour. Neither is readable here.

## Panel notes (short)

- Wiegers: the WC table is testable and traceable, and each row carries evidence. Two stated texts disagree on where the report lives (F-1), and one acceptance check cannot pass for commands the phases never touch (F-2).
- Adzic: the 7.2 live check reads like an executable scenario. Its step 3 and step 4 contradict the section 3.1 report paths for adversarial and workflow.
- Cockburn: the actors (coordinator, worker session, command, person) are clear, and section 4 keeps the person's goals intact.
- Fowler: the layering (Orca on top, commands as units) is sound and the rejected alternative is argued with evidence (S:28-39). A shared contract file is the right single point of change.
- Nygard: failure paths are mostly specified (blocked, partial, fenced). The retry path (WC-6) leaves the output directory ambiguous (M-2).
- Whittaker: see the attack list under `=== ARCHITECTURE ANALYSIS ===`.
- Newman and Hohpe: the report file is a clear integration contract. Its location and schema are not uniform across commands (F-1, F-2).
- Crispin and Gregory: per-phase checks exist and have pass conditions. The phase scope gaps in F-2 mean some checks cannot pass.
- Hightower: operations are covered (heartbeat, release, reclaimable workers). WC-1 has an owner but no deliverable (m-3).

## Guard Condition Boundary Table

Every class that applies is listed. Left out, with the one-line reason in the last row of each guard.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `--unattended` switch | S:51, S:228 | Zero/Empty (flag absent) | no flag | false | today's behaviour, SA-1 (S:146) | OK |
| `--unattended` switch | S:51 | Sentinel Value Match (flag passed by a person) | person types it | true | D1(a) says "a person never types it" (S:228) but nothing says what happens if one does | GAP (Medium, M-7) |
| `--unattended` switch | S:132-137, S:76 | Legitimate Edge Case (command in section 4) | `/sc:git --unattended` | true | section 4 says "get no `--unattended` mode"; refusal behaviour is not stated | GAP (Medium, M-7) |
| report status (WC-5) | S:63 | Typical | `partial` | maps to succeeded | specified, S:63, S:263 | OK |
| report status (WC-5) | S:63 | Legitimate Edge Case | no report exists | failed | specified | OK |
| report status (WC-5) | S:63 | Sentinel Value Match | `status` outside the four-value set from an existing contract (adversarial, reflect, workflow) | undefined | S:62 says existing contracts "keep their fields and add the missing ones"; mapping an old status value into the set is not stated | GAP (F-2 covers the scheduling side) |
| wait size (WC-10) | S:68 | Typical | 240 s | within | specified | OK |
| wait size (WC-10) | S:68 | Maximum/Overflow | exactly 5 min and a single tool call over 4 min | split required | specified ("longer than 5 minutes ... split into at most 4") | OK, but the 4-5 minute band has no rule (m-2) |
| wait size (WC-10) | S:68, S:114 | Divergence | pr-submit poll runtime | unknown | marked UNVERIFIED, S:114, S:283 | GAP (Medium, M-6) |
| nesting depth | S:33, S:66 | Typical | depth 1 | worker may not start workers | specified (WC-8) | OK |
| nesting depth | S:249-253 | Maximum/Overflow | user raises depth | rejected alternative | D5(a) keeps depth 1 | OK |
| fresh-dir resume (WC-6) | S:64 | One/Minimal (retry with same brief) | same `--output` | undefined | "fresh output directory" does not say who picks it | GAP (Medium, M-2) |
| circuit breaker | S:263 | Typical | 3 failures | Task failed | `CAPS:80`: a worker's own failed report does not count | OK |
| confidence < 0.70 (task) | S:121 | Maximum/Edge | exactly 0.70 | not stated here | the row says "below 0.70"; the boundary is the command's own | OK (inherited, INV-B:199) |

Not applicable: Zero/Empty for WC-10 and for the depth guard cannot occur.

## Quantity flow (pipeline dimensional analysis)

```
[cmd/ commands: 43] --> [verdict split] --> [ready 10] --> P0 smoke 3; P1 fixes 4 (adversarial, cleanup-audit, index-repo, workflow); P2 fixes 4 (reflect, release-split, tdd, troubleshoot); no phase: 2 (brainstorm, init-lite)
                                       --> [needs change 27] --> P1 9, P2 11, P3 4, P4 3  (sum 27, matches S:159-162)
                                       --> [coordinator-only 6]
```

Counts are conserved: 43 = 10 + 27 + 6, and the 27 re-sum across phases. One mismatch: two ready commands (brainstorm, init-lite) are in no phase, yet S:73 requires `--unattended` and the WC-4 contract for every worker (F-2).

=== REQUIREMENTS ANALYSIS ===

### F-1 [MAJOR, blocking] (Wiegers, Adzic) The report path rule contradicts section 3.1 for adversarial and workflow

- WC-4 states: the command "writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed" (S:62).
- Section 3.1 states adversarial's small fix is the filename `<output>/adversarial/return-contract.yaml` (S:83). AC-1.4 checks only that "adversarial names one fixed path" (S:198).
- Section 3.1 states workflow reports `.dev/tasks/to-do/<id>/return-contract.yaml` (S:92). Nothing in section 3 says workflow takes an output directory.
- Grading sentence: an implementer who follows the stated text builds, for `/sc:adversarial --output D`, a contract at `D/adversarial/return-contract.yaml` (S:83) or at `D/return-contract.yaml` (S:62), and those two stated texts name different files. The coordinator brief (S:73) promises a path "known before dispatch (WC-4)". For workflow, `<id>` is generated by the run (INV-B:272), so the promise cannot hold. 7.2 step 3 requires the `worker_done` report path to be "the WC-4 contract path" (S:182), which fails for workflow and, on the other reading, for adversarial.
- Evidence the contradiction is real in the inventories: adversarial runs wrote the contract in two different places (INV-A:60). Workflow's path is `<id>`-based (INV-B:272).
- Recommendation: state one rule. Either WC-4 gains an explicit exception for these two (adversarial: `<output>/adversarial/`; workflow: the package path, reported by the worker in `worker_done --report-path` and not known before dispatch), or both are changed to write at `<output-dir>/return-contract.yaml`. Narrow, do not add a mechanism.
- Priority: High. Quality impact: removes a check that cannot pass (AC-1.2, 7.2 step 3 for two P1 commands).

### F-2 [MAJOR, blocking] (Wiegers, Crispin) The WC-4 contract and `--unattended` flag are required of ready commands that no phase gives them to

- S:73 says the brief states "the exact command line including `--unattended`". S:79 says ready commands report their named file "until Phase 1 adds the contract". WC-4 requires the contract with `status` in the four-value set and `command` (S:62).
- But S:159 limits the P1 contract work to the P1 row. S:160 limits P2 to "each default-on gate resolves per its section 3 row". The P2 rows for reflect, release-split, tdd and troubleshoot name only gate resolutions (S:88-91). The rows for brainstorm and init-lite name no change (S:84, S:87), and neither is in any phase (Quantity flow above).
- Troubleshoot writes `return-contract.yaml` only with `--caller task-unified` (INV-B:242), tdd writes the TDD file only (INV-B:222), and release-split writes a markdown report (INV-B:122). None has a contract file in unattended mode.
- Grading sentence: an implementer who follows the stated phase scope builds P2 for `/sc:troubleshoot` with a gate resolution and no contract file, and that is wrong because AC-2.3 requires "7.2 passes with `--outcome succeeded`" (S:201), and 7.2 step 4 asserts `test -s <contract>` and a parsed `status` and `command` (S:183). The same holds for AC-1.2 on adversarial, cleanup-audit, index-repo and workflow (S:196), whose fixes in S:83, S:85, S:86, S:92 add no `status` or `command` fields.
- Recommendation: either list "write the WC-4 contract in unattended mode" in the P1/P2 scope for the named ready commands and add brainstorm and init-lite to a phase, or narrow AC-2.3 and AC-1.2 step 4 to the commands whose scope includes the contract.
- Priority: High. Quality impact: closes a phase-exit check that cannot pass as written.

=== ARCHITECTURE ANALYSIS ===

No blocking architecture finding. The decision (S:13-45), the rejected alternative (S:28-39) and the coordinator-only list (S:127-139) hold against the evidence in `CAPS:97-103,145-161` and `INV-A:90`, `INV-B:285-287`.

Whittaker attacks (all graded below blocking):

1. Sequence Attack on retry (WC-6, S:64). Setup: a P2 command with "fresh dir" is blocked at a gate, the coordinator retries with `worker-start --retry-of` and the same brief. Step trace: before, `<output-dir>` holds `return-contract.yaml` with `status: blocked`; after, the second run writes to the same directory, and the first attempt's file is overwritten or mixed. The text "writes each run into a fresh output directory" does not say who picks the directory. See M-2.
2. Divergence Attack on tasklist (S:122). The spec resolves Stage 10.5 by passing `--unattended` to reflect so the headless auto-accept rule applies. The inventory recommended dropping `--remediate` (INV-B:215). Auto-accept starts a remediation chain with no person, and no acceptance check covers it. See M-3.
3. Sentinel Collision on `--unattended` (guard table). A person typing the flag gets unattended behaviour with no way to answer a gate. See M-7.
4. Accumulation Attack on shared paths (WC-11, S:69). Two workers in one worktree: cleanup-audit's output directory is fixed (S:85), and index-repo writes `PROJECT_INDEX.md` at the root (S:86). WC-11 says default paths carry a timestamp or slug, yet both are "ready today". See M-5.

## Follow-up candidates (Medium and minor; none triggers a revision)

Medium (warnings):

- M-1 (Wiegers). S:73 requires `--unattended` in every brief, but S:79-92 and AC-0.4 (S:194) run ready commands without it before P1/P2 add the flag. The phase applicability is inferable, so it needs only a sentence. Evidence: S:73 vs S:79, S:194.
- M-2 (Nygard). WC-6 "fresh output directory" does not say who creates the directory, and 2.3 (S:73) does not make the coordinator pass a new one on retry (S:64). The guess is which reading the implementer picks. A command-made subfolder would also move the WC-4 path.
- M-3 (Fowler). Tasklist Stage 10.5 under `--unattended` auto-accepts remediation through reflect's headless rule (S:122), against the inventory's advice (INV-B:215). No check in section 7 exercises it. Not a stated contradiction, so Medium.
- M-4 (Crispin). SA-4 and AC-C5 constrain only `src/superclaude/commands/*.md` edits (S:149, S:176). Many P2 changes land in skills and refs (for example reflect's `remediation-handoff.md`, S:88; tasklist `SKILL.md`, S:122), which no check keeps additive. A requirement the document never states.
- M-5 (Nygard). WC-11 versus cleanup-audit's fixed `.claude-audit/` and index-repo's root file (S:85-86, S:69). Also, reflect writes the tracked file `docs/memory/reflect/deviation-patterns-<slug>.md` (INV-B:114), which section 3.1 does not mention for a worker that is told to write nothing outward (WC-9).
- M-6 (Hightower). The WC-10 / pr-submit reading that the 600 s is a "cumulative per-wait budget" of poll-then-sleep iterations (S:68, S:114) rests on `cmd/pr-submit.md:49` and `SKILL.md:46-64`. The inventory reads it as "600 s per wait, several rounds" (INV-B:95, INV-B:299), and the spec re-read list (S:11) does not include those lines. UNVERIFIED here; the spec itself marks poll runtime UNVERIFIED (S:283). AC-4.3 depends on it.
- M-7 (Whittaker). Behaviour of `--unattended` typed by a person, and of passing it to a section-4 command, is not stated (guard table).
- M-8 (Cockburn). S:154 says "Phases 1-3 need no user decision", but P1 depends on D1 and P2 touches D4 commands (auggie-review `--post-pr`, task `commit`/`push`, S:244). S:225 correctly says they proceed on the recommendations. Reword S:154.
- M-9 (Adzic). AC-1.1 and S:159 say the section applies to "each command in the P1 row except load". The row also names fixes to adversarial, cleanup-audit, index-repo and workflow, so it is unclear whether those four get a `## Unattended mode` section (S:195, S:159).

Minor notes:

- m-1. WC-9 and the git row cite `.dev/orca-command-refactor/README.md:31` (S:67, S:133). That README line is the rule for this planning run's workers (README:31), not a product rule for later workers.
- m-2. WC-10 has no rule for a tool call between 4 and 5 minutes.
- m-3. WC-1 is owned by "launch setup" (S:59), but no phase or check produces a deliverable for it.
- m-4. E3 cites `invocation_method: "skill-direct"` as evidence the direct route works (S:23), while section 1.4 says the PR #329 run proves only the nested route (S:43). The spec states both; reword E3 for consistency.
- m-5. AC-C1's grep is case-sensitive and covers only four verbs (S:172).
- m-6. UNVERIFIED in this sandbox: every `src/`, `~/.claude`, Orca-installed-file and `CLAUDE.md` citation, including the 11 "re-read" locations (S:11) and `pyproject.toml:38` (S:183). Only the inventory-quoted forms were checked.

Follow-up issue question: the review loop asks the user once whether to open an issue for these. This single-reply sandbox run could not ask. No issue was created, and the list above is the record.

## Reviser brief

Blocking finding ids: **F-1, F-2**.

Rules (restated from the command's Review Loop, bullet 6; the reviser reads this report, not the command):
- Revise only text a blocking finding names (F-1: S:62, S:83, S:92, S:182, S:198; F-2: S:73, S:79, S:159-160, S:201, S:196).
- Add no rule, mechanism or section that a blocking finding does not call for.
- Cite the finding id on each added paragraph or table.
- Prefer deleting or narrowing to adding.
- Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings alone. Return the candidate once; do not award yourself a PASS.

verdict: FAIL
