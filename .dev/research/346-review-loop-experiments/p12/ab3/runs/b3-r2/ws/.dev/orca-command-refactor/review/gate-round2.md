review: 2 of 3

# GATE-loop RE-REVIEW: orca-worker-contract-spec.md (/sc:spec-panel --mode critique --focus requirements,architecture --re-review --baseline)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines by `wc -l`, 59523 bytes)
- candidate sha256: `3df6411553609a3781774f54ed644139d6073eeb6265fab7bf239562e2658b99`
- baseline: `.dev/orca-command-refactor/specs/history/spec-g.md` (285 lines, 59339 bytes), sha256 `523f1629dc21eaacc3987537a70cf3e5944edf741f8b5368cdaad6f32cf68d9c`. This hash equals the candidate hash that `gate.md:6` records as the gate-reviewed text, so the roles are consistent: baseline = text the gate reviewed, candidate = the revision.
- prior: `.dev/orca-command-refactor/review/gate.md` (78 lines), sha256 `2cf05a9cfb4089fa0de50ba94622417bca1b58a10cd3bed47e249779b5d5eee4`; its header is `review: 1 of 3` (`gate.md:1`), so N = 2. The gate loop numbers its own reviews, so this is not a fourth review of the document.
- reviewer model used: claude-sonnet-5-5
- prompt followed: RE-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:38-51` (home resolves inside the sandbox); roles fixed by its table, not inferred.
- Evidence limits: per `README.md` only the three files under `.dev/orca-command-refactor/inventory/` are checkable. `SPEC` = candidate, `INV-A` = `inventory/commands-a.md`, `CAPS` = `inventory/orca-capabilities.md`. Any citation to `cmd/`, `sk/`, `EVIDENCE.md` or Orca source that is not quoted in an inventory file is UNVERIFIED.
- `.claude/agents/rf-qa.md` and `~/.claude/agents/rf-qa.md`: neither exists in the sandbox (`home/.claude` holds only `rules/`). The rules of the command's Review Loop section were applied alone, as the command says they stand alone.

## Step 1: evidence block (`diff -w BASELINE CANDIDATE`)

Exactly two changed lines; both are table rows in the candidate and sit at the same line numbers in the baseline.

Change at SPEC:105 (section 3.2 cli-portify row, column "unattended gate handling"):

BEFORE (baseline), `spec-g.md:105`:
`< | cli-portify | each of the three approval gates resolves as blocked with the artifact to review named in the contract | contract (fields already defined; file location unnamed) | add a `--resume <contract>` flag that uses the existing `resume_phase`/`resume_substep` fields | dispatch only inside an IronClaude checkout (hardcoded template path) | `sk/sc-cli-portify-protocol/SKILL.md:69,152,170,393,464-473,517-566,529`; `cmd/cli-portify.md:23,34`; `INV-A:45,68` | P2 |`

AFTER (candidate), `orca-worker-contract-spec.md:105`:
`> | cli-portify | each of the three approval gates resolves as blocked with the artifact to review named in the contract; no flag pre-approves a gate, so every unattended run ends `blocked` until a person approves (F-1) | contract (fields already defined; file location unnamed) | add a `--resume <contract>` flag that uses the existing `resume_phase`/`resume_substep` fields | dispatch only inside an IronClaude checkout (hardcoded template path) | `sk/sc-cli-portify-protocol/SKILL.md:69,152,170,393,464-473,517-566,529`; `cmd/cli-portify.md:23,34`; `INV-A:45,68` | P2 |`

Change at SPEC:201 (section 7.3 acceptance row AC-2.3):

BEFORE (baseline), `spec-g.md:201`:
`< | P2 | AC-2.3 | Happy-path run per P2 command with every required flag in the brief | 7.2 passes with `--outcome succeeded` |`

AFTER (candidate), `orca-worker-contract-spec.md:201`:
`> | P2 | AC-2.3 | Happy-path run per P2 command except cli-portify (F-1: it always ends `blocked`, so its acceptance is AC-2.2 only) with every required flag in the brief | 7.2 passes with `--outcome succeeded` |`

Self-check (run): `grep -nF` of the AFTER cell text found it at `orca-worker-contract-spec.md:105` and `:201` and not in the baseline for the new wording; `grep -nF` of the BEFORE text found the old wording at `spec-g.md:105` and `:201` (the old AC-2.3 wording "Happy-path run per P2 command with every" is absent from the candidate). No role swap.

Size accounting (reviser report is not in the workspace, so measured here): 59339 to 59523 bytes, +184 net, both additions cite F-1, none outside the two rows named by F-1 (the diff has no other hunk).

## Prior blocking findings

| id | prior status | now | evidence |
|---|---|---|---|
| F-1 | open (blocking, `gate.md:19`) | resolved | see below |

F-1 defect, restated from `gate.md:21`: cli-portify's three always-on gates resolve only as `blocked` (SPEC:105), WC-2 gives it only option (c) (SPEC:60), WC-5 maps `blocked` to `--outcome failed` (SPEC:63), yet AC-2.3 required a `--outcome succeeded` happy-path run for every P2 command including cli-portify (`spec-g.md:201`). Two stated texts contradicted each other.

Check against the AFTER text only:
- AFTER SPEC:201 removes cli-portify from the AC-2.3 set and says its acceptance is AC-2.2 only. The contradiction in `gate.md:21` (an acceptance criterion that cannot pass) is gone: no criterion now demands `succeeded` from cli-portify.
- AFTER SPEC:105 states the consequence explicitly ("every unattended run ends `blocked` until a person approves"), which matches WC-2(c) (SPEC:60), WC-5 (SPEC:63) and the inventory fact that the gates are always on (`inventory/commands-a.md:45`). This is the second of the two repairs `gate.md:24` offered, so it is an accepted fix.
- AC-2.2 (SPEC:200) still applies to cli-portify: a gate-trigger run expects `worker_done --outcome failed`, contract `status: blocked` with a non-empty `blocked_question`, and no `agentWait`. cli-portify's always-on gate satisfies exactly that, so its remaining acceptance path is passable. Dependent texts checked: P2 phase row (SPEC:160, lists cli-portify and says each gate "resolves per its section 3 row"), section 7.2 steps 1-7 (SPEC:178-186, no per-command success assumption beyond "its `--outcome` matches the contract's `status` under WC-5", which holds for `blocked`/`failed`), and the `--resume <contract>` flag in SPEC:105, which only says where to restart and is now explicitly not an approval. All consistent with the AFTER text.
- No regression: the edit adds no mechanism, flag or section; it narrows an acceptance row and adds a clause that agrees with existing rules.

## === REQUIREMENTS ANALYSIS ===

No new blocking finding on changed lines. Findings on lines changed against the baseline:

- N-1 [Medium / note, origin=changed] (Wiegers) SPEC:105 says every run ends `blocked` "until a person approves", but neither SPEC:105 nor WC-3 (SPEC:61) says how a person's approval is recorded, since no answer flag exists for these gates. This is not blocking: the text that is stated (blocked, AC-2.2 only) is internally consistent and an implementer builds nothing wrong from it; it is a requirement the document does not state, and it falls under the already open M-10 (`gate.md:64`, answer flag undefined for blocked gates). Listed under follow-up candidates, not a revision trigger.
- N-2 [minor, origin=changed] (Adzic) The new AC-2.3 cell inlines a finding id and a rationale into an acceptance row (SPEC:201). It is readable and matches the reviser-contract rule that additions cite the finding id; once the spec leaves the review loop the "(F-1: ...)" label points at a report, not a spec section. Note only.

## === ARCHITECTURE ANALYSIS ===

The two changed lines touch no boundary or interface: they narrow one acceptance criterion and annotate one gate-handling cell. R1-R5 (SPEC:31-37), SA-2 (SPEC:147) and the phase plan are untouched. Counts conserve: the diff changes no row count, so 10 + 27 + 6 = 43 (`gate.md:14`) still holds. No architecture finding.

## Guard Condition Boundary Table (changed lines only)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| cli-portify approval gates (3, always on) | SPEC:105 | Typical | gate reached under `--unattended` | true | Contract `status: blocked` with the artifact to review named; run ends `--outcome failed` (WC-2(c) SPEC:60, WC-5 SPEC:63); AC-2.2 is its acceptance (SPEC:200-201) | OK |
| cli-portify approval gates | SPEC:105 | Legitimate Edge Case | relaunch with `--resume <contract>` after a person's approval | gate fires again | Stated: no flag pre-approves, run ends `blocked` again; how a person's approval is recorded is not stated | OK for the guard (behavior stated); recording of approval is Medium N-1 |
| AC-2.3 happy-path set | SPEC:201 | Zero/Empty (cli-portify only, 0 happy paths) | P2 set minus cli-portify | n/a | cli-portify excluded, covered by AC-2.2 | OK |

Classes left out: Maximum/Overflow and Sentinel Value Match, because the changed lines carry no numeric threshold or sentinel; One/Minimal, because a gate has no size. Unchanged guards from `gate.md:35-46` are not re-graded (scope is changed lines plus prior blockers).

## Pipeline/Quantity check (changed lines only)

No count flow changes. The only quantity in the diff is the exclusion of one command (cli-portify) from the AC-2.3 happy-path set: P2 happy-path commands go from all P2 commands to all P2 commands minus 1; the P2 phase list (SPEC:160) and the 27-command phase distribution (`gate.md:14`) are unchanged because cli-portify stays in P2 for AC-2.1 and AC-2.2. No mismatch.

## Coverage
`scoped PASS: changed lines + prior blockers`. Covered: the full `diff -w`, the one prior blocking finding (F-1), the rows and rules that depend on the two changed lines (SPEC:60, 61, 63, 105, 160, 178-186, 200, 201; `inventory/commands-a.md:45`). Not covered: whole-document assurance (needs a separate labelled first review), and every `cmd/`, `sk/` and Orca guide citation outside the inventories (UNVERIFIED). This is a gate-loop re-review: a PASS ends the loop; no further review follows.

## Follow-up candidates (Medium and minor; never trigger a revision)
- Carried unchanged from `gate.md:55-64` and not re-graded here (origin=unchanged, none quotes a changed line): M-1 to M-10 and minor notes n-1 to n-5 (`gate.md:66-71`).
- New Medium: N-1 above (how a person's approval of cli-portify's gates is recorded). Related to M-10.
- New minor: N-2 above.

Issue offer: the session that ran this review asks the user once per loop whether to open an issue for M-1 to M-10, n-1 to n-5, N-1 and N-2. I created none and wrote no file other than this report.

## Reviser brief
None: no blocking finding is open (F-1 resolved). Nothing to revise. (Rules for any later reviser: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; cite the finding id on each addition; prefer deleting or narrowing; report byte size before and after and bytes added and deleted per finding id. Brief clauses overridden by this report: none.)

verdict: PASS
