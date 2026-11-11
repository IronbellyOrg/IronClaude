review: 2 of 3

# /sc:spec-panel critique, round 2 (re-review)

- Mode: critique, re-review (`--re-review .dev/orca-command-refactor/review/round1.md`, `--baseline .dev/orca-command-refactor/specs/history/spec-v1.md`). Focus: requirements, architecture (as briefed).
- CANDIDATE: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 57870 bytes, SHA-256 `9bf4886e4a47262c5cf9c862441589e93e25942e3132e8035b411d7bd0318c5f`
- BASELINE: `.dev/orca-command-refactor/specs/history/spec-v1.md`, 57763 bytes, SHA-256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- PRIOR: `.dev/orca-command-refactor/review/round1.md`, 17707 bytes, SHA-256 `5c62f17b267d58ff77cafb9ca758130edd90699d2f11346d7a7e9b2d0f156e6d`, header `review: 1 of 3`, `verdict: FAIL`, Reviser brief `B1`
- Review number: 1 + 1 = 2, so `review: 2 of 3`.
- Reviewer model: claude-haiku-5-5
- Rules read: `command.md` in full; `home/.claude/rules/prompts/document_review_loop_prompts.md` in full (RE-REVIEW prompt, Step 1, self-check). The Process of the Fix Cycle in `.claude/agents/rf-qa.md` (project) and `~/.claude/agents/rf-qa.md` could not be read: neither exists in this sandbox. Per the command's rule, the rules in the Review Loop section stand alone here.
- Evidence base: the candidate, the baseline, the prior report, `README.md`, and the three inventories under `.dev/orca-command-refactor/inventory/`. Paths outside the workspace are cited only where an inventory quotes them; otherwise they are UNVERIFIED.

Citation shorthand: `SPEC:N` = candidate line N. `BASE:N` = baseline line N. `R1:N` = `review/round1.md` line N. `INV-A:N`, `INV-B:N`, `CAPS:N` = the three inventories. `README:N` = `README.md`.

## Step 1. Evidence block

`diff -w BASELINE CANDIDATE` gives one hunk, at line 73 (`73c73`). Plain `diff` gives the same hunk. Changed lines verbatim:

```text
BEFORE (baseline), BASE:73:
< The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).

AFTER (candidate), SPEC:73:
> The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line, including `--unattended` from Phase 1 on (Phase 0 briefs omit it, because no command accepts the flag before P1; B1, SPEC:158-159) and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
```

Only SPEC:73 changed. Every other line matches the baseline, and the byte counts agree with the reviser's accounting (57870 - 57763 = +107).

Self-check, `grep -nF` run in the workspace:
- The AFTER line (without `>`) matches exactly once in the CANDIDATE (SPEC:73).
- The BEFORE line (without `<`) matches exactly once in the BASELINE (BASE:73).
- Roles are not swapped.

## Prior blocking findings

| Id | Status | Basis |
|---|---|---|
| B1 | resolved | The defect was that SPEC:73 required `--unattended` in every Task brief, while P0 has "no command edits" (SPEC:158) and P1 adds the flag (SPEC:159). The ready-today brief column lists no flag (SPEC:79, SPEC:81-92). SPEC:73 now says the flag is carried from Phase 1 on and that Phase 0 briefs omit it. That matches SPEC:158, SPEC:159 and SPEC:81-92. The two places that build briefs "per section 2.3" (SPEC:180 and SPEC:194) now agree with P0. The two rules no longer contradict each other, which is the fix R1:52-57 allowed. The residual point (a P0 run does not exercise the unattended contract) is the consequence the B1 recommendation accepted, not a contradiction. Not regressed: the new text restates no contradiction. |

No prior blocking finding is open, so none is regressed.

## Findings on changed lines (origin=changed)

**F-R2-1. Minor.** SPEC:73 cites the review-finding id `B1` inside normative spec text. `B1` is defined only in `R1:52`, so a reader of the spec alone cannot resolve it, and the citation goes stale once the review closes. `SPEC:158-159` also uses this review's citation scheme. The spec's own conventions (SPEC:7-11) define only `INV-A`, `INV-B`, `CAPS`, `cmd/` and `sk/`. Suggested fix: replace "B1, SPEC:158-159" with "section 6, P0 and P1 rows". Not blocking: the sentence still holds without it.

No blocking finding on the changed line. The statement "no command accepts the flag before P1" agrees with SPEC:158 (no command edits in P0) and SPEC:159 (flag added in P1).

## Findings on lines that depend on the changed line (origin=unchanged, quoting SPEC:73)

**F-R2-2. Minor.** AC-0.4 (SPEC:194) and the live check (SPEC:180-183) run P0 briefs without `--unattended`. Their passes (step 2 `agentWait` never non-null, step 3 exactly one `worker_done`, step 5 no `AskUserQuestion`) therefore rely on the standard-mode commands not stopping on a person. The inventories support this for the three AC-0.4 commands:
- `/sc:troubleshoot` without `--fix`: diagnosis never asks (`inventory/commands-b.md:49`, citing `sk/sc-troubleshoot-protocol/SKILL.md:209`). The `--depth deep` short-input STOP (`inventory/commands-b.md:239`, citing `SKILL.md:57`) needs a short input, and AC-0.4 uses "<real symptom>".
- `/sc:workflow --handoff none`: no prompts (`inventory/commands-b.md:267-275`, item (g)).
- `/sc:adversarial --output`: its only gate is `--interactive`, which the P0 brief excludes (SPEC:83).

The residual is that the spec does not state these inputs must avoid gates. Minor, because the inventories support the pass. The inventories were not run.

## Coverage of the scoped pass

- Guard Condition Boundary Table: no guard on the changed line (SPEC:73 is a content requirement, not a threshold, boolean or sentinel). FR-8 to FR-10 therefore produce no finding here.
- Pipeline Dimensional Analysis: not triggered.
- The changed line, the prior blocker B1, and the lines that depend on SPEC:73 (SPEC:73, 79, 81-92, 158, 159, 180-183, 194) were checked against the inventories where they cite them.
- Severe defects newly discovered outside this scope: none found in this pass. The rest of the candidate was not re-reviewed (scope rule, step 5).

## Round 1 Medium and minor findings

The revision edited only SPEC:73. The round 1 Medium findings (M1-M12) and minor notes (N1-N6) cite lines that are unchanged, so they stand as in `R1` and are not re-graded here.

## Follow-up candidates (Medium and minor; recorded, not acted on)

- Carried from round 1: Medium M1, M2, M3, M4, M5, M6, M7, M8, M9, M10, M11; Low M12; minor N1 to N6.
- New in this round: F-R2-1 (minor), F-R2-2 (minor).
- No issue has been opened. The run is not `--unattended`, so the session that ran the review asks the user once whether to open issues for these. That question is for the session, not this worker.

## Precedence and overrides

The brief's values (candidate, baseline, prior) match the RE-REVIEW prompt. No brief clause was narrowed or overridden. The brief's focus (`requirements,architecture`) was applied to the changed line only.

## Reviser brief

No blocking finding is open (B1 resolved). Nothing to revise.

Restated rule: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph cites its finding id; prefer deleting or narrowing; report byte size before and after with bytes added and deleted per finding id.

Blocking ids for revision: none.

## Items not checked

- Neither `rf-qa.md` file exists in this sandbox; its Process steps were not applied (see header).
- Citations to `src/`, `.dev/codegraph-migration/`, `.dev/evals/`, `CLAUDE.md`, `~/.claude/` and `/opt/Orca/` are UNVERIFIED unless an inventory quotes them.
- Nothing was run against Orca, GitHub or the repository. Commands run: `sha256sum`, `diff`, `diff -w`, `wc -c`, `grep -nF`, and `sed` on inventory lines.

verdict: PASS
