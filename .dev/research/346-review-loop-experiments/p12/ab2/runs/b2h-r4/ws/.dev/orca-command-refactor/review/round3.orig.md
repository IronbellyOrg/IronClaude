review: 3 of 3
> verification (coordinator, VERIFY step VF3): pending. This reviewer did not run VERIFY. The VERIFY prompt runs in a fresh context on the candidate and the N-6 finding list only, before any escalation. Its reply is recorded by the coordinator.

# Spec-panel critique, re-review: orca-worker-contract-spec (focus: requirements, architecture)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `87c84d9ca9169f943376688b64d421baec2513be9fe5034504496a4473d86140`
- baseline: `.dev/orca-command-refactor/specs/history/spec-v2.md`, sha256 `97f56a6e69838dc9f80dfae9d1e8e0aa95413656b2559e687870566b2996ca6a`
- prior: `.dev/orca-command-refactor/review/round2.md`, sha256 `075cbff06003a5c391ba57ebb09f452ab06d1345712f1ba7af25f3eaa73b5088` (prior header `review: 2 of 3`, so this report is review 3 of 3)
- reviewer model: claude-haiku-5-5
- prompt: RE-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md`, read in full (sandbox home copy). The re-review core (roles, Step 1, review number, self-check) was applied first.
- rf-qa.md: neither `.claude/agents/rf-qa.md` nor `~/.claude/agents/rf-qa.md` exists in the sandbox. The review-loop step 5 rules in `command.md:262` therefore stand alone.
- round2 header note: round2 records candidate sha `97f56a69...`, which is the sha of `specs/history/spec-v2.md`. The text round2 reviewed is therefore this run's baseline, and the diff below isolates the revision made after round2 (the N-1 fix).
- citation key: `spec:N` = candidate line N; `baseline:N` = spec-v2 line N; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `round2:N` = `review/round2.md` line N. Repo-relative paths are under `.dev/orca-command-refactor/`.
- panel: Wiegers, Adzic, Cockburn (requirements); Fowler, Newman, Hohpe, Nygard (architecture); Whittaker (active in every panel review, `command.md:83`).

## Decisions

| Decision | Options considered | Rationale |
|---|---|---|
| Baseline | `spec-v2.md` (named in the brief) or `spec-v1.md` (round2's baseline) | The brief names `spec-v2.md`. Round2's candidate hash equals spec-v2, so this diff isolates the post-round2 revision. |
| Changed-line set | `diff -w` of the whole file | Step 1 requires `diff -w`. Two hunks changed, at spec:63 and spec:182. Removing those two lines from both files leaves them identical (`cmp`), which confirms no other line changed. |
| Prior blocking set | B-1, B-3, B-5 (`round1.md:2`); N-1 (`verify-2.md`, round2 `Reviser brief`) | `round2:157-158` records B-1, B-3 and B-5 as resolved and N-1 as the new blocking finding; `verify-2.md` confirmed N-1. |
| B-2 and B-4 | re-grade, or carry as noted | Rejected at VF1 and kept as noted (`round1.md:2`). Not re-graded, as round2 did. |
| Re-grade scope | every round2 Medium, or only prior blockers and changed lines | `command.md:261` item 5 and the RE-REVIEW prompt: prior blockers plus changed lines. Unchanged Medium items are carried. Two carried Medium items sit on changed line spec:63 and are re-graded below (M-2, M-3). |

## Coverage

Read in full: `README.md`, the candidate spec (285 lines), the baseline `history/spec-v2.md`, `round2.md`, `round1.md:1-2`, `verify-2.md`, `command.md` and the RE-REVIEW prompt file.

Checked against the inventories and README (the only evidence in the sandbox): `CAPS:73` (`worker_done requires --outcome succeeded or --outcome failed`; `[G]` lines 88-90, "Never encode failure only in prose"), `CAPS:76-77` (worker_done from the dispatched pane; settles the Task), `CAPS:79` (the report path is a pointer; whether Orca reads it is UNVERIFIED), and `INV-A:35` (adversarial: "the skill names no filename; real runs wrote `<output>/adversarial/return-contract.yaml`").

Unchanged dependency text read for the changed lines: spec:62, spec:73, spec:79, spec:83, spec:91, spec:92, spec:105, spec:114, spec:158, spec:182, spec:194, spec:200, spec:201, spec:262.

Not checkable here (UNVERIFIED): every `sk/`, `cmd/` and `src/superclaude/` cite (for example `sk/sc-adversarial-protocol/SKILL.md:427-429`), `WORKER-CONTRACT.md` (not in the sandbox), and the PR #329 run. These cites sit on unchanged lines and were not re-checked here.

## Step 1: evidence block (`diff -w BASELINE CANDIDATE`)

Roles: BASELINE = `specs/history/spec-v2.md`, CANDIDATE = `specs/orca-worker-contract-spec.md`. Lines starting `<` are `BEFORE (baseline)`; lines starting `>` are `AFTER (candidate)`. Changed hunks: baseline lines 63 and 182 (candidate lines 63 and 182).

```text
63c63
< | WC-5 | **Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. `--outcome failed` when the report says `failed` or `blocked`, or when the contract is missing, zero bytes, truncated, unparseable, lacks `status`, or has a `status` outside the four values (B-5: the default is `failed`); `--outcome succeeded` only when the parsed `status` is `succeeded` or `partial`, including an audit whose verdict is FAIL (the audit itself succeeded). The first sentence of the body states the report's status and verdict. | Worker session | `CAPS:73` (`[G]` lines 88-90, "Never encode failure only in prose"); `CAPS:76-77` |
---
> | WC-5 | **Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. `--outcome failed` when the report says `failed` or `blocked`; in P0, when the named report is missing or zero bytes (N-1); from P1, when the contract is missing, zero bytes, truncated, unparseable, lacks `status`, or has a `status` outside the four values (B-5: the default is `failed`); `--outcome succeeded` only when the parsed `status` is `succeeded` or `partial`, including an audit whose verdict is FAIL (the audit itself succeeded). The first sentence of the body states the report's status and verdict. | Worker session | `CAPS:73` (`[G]` lines 88-90, "Never encode failure only in prose"); `CAPS:76-77` |
182c182
< 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path.
---
> 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5 (from P1) or the named report under WC-5 (P0, N-1); its report path is the WC-4 contract path (from P1) or the command's named report file (P0, N-1).
```

Self-check: each AFTER line was found exactly once in the candidate and each BEFORE line exactly once in the baseline (`grep -nF`, run on this file's quoted text). Roles are confirmed. No prior blocking finding is marked resolved on a stale reading.

## Prior blocking findings

| id | status | evidence (AFTER text only) |
|---|---|---|
| B-1 | resolved | `spec:79` is unchanged from baseline: every ready-today command "also gets the P1 `--unattended` flag and its `## Unattended mode` section, a no-op where the command has no gate (B-1)". No regression. |
| B-3 | resolved | `spec:62`, `spec:73`, `spec:76`, `spec:83`, `spec:87`, `spec:90`, `spec:92` and `spec:198` are unchanged from baseline, so the path rules and rows round2 checked still hold. No regression. |
| B-5 | resolved | The P1 clause of `spec:63` ("from P1, when the contract is missing, zero bytes, truncated, unparseable, lacks `status`, or has a `status` outside the four values (B-5: the default is `failed`)") is unchanged in substance, and `spec:200` (AC-2.2 fixtures) is unchanged. The new P0 clause adds no fallback that sends `succeeded` for a missing or empty report. The P0 success gap is N-6 below, not a regression of B-5. |
| N-1 | resolved as to the defect stated | `spec:63` now sends `failed` in P0 when the named report is missing or zero bytes, so a clean run that leaves a complete `REPORT.md` (`spec:91`, `spec:79`) is no longer reported as failed. The success half of the P0 outcome is still missing, which is a new blocking finding, N-6. |

Noted, not re-graded (per `round1.md:2`): B-2 (AC-0.4 step 4 parses `REPORT.md`; `spec:194` unchanged) and B-4 (reflect remediation auto-accept under `--unattended`; `spec:88` and `spec:122` unchanged).

## Findings on changed lines

### N-6 (BLOCKING, new, origin=changed): WC-5 gives a clean P0 run no permitted outcome, so the AC-0.4 outcome check cannot pass

- Changed text: `spec:63` WC-5, "`--outcome failed` when the report says `failed` or `blocked`; in P0, when the named report is missing or zero bytes (N-1); ... `--outcome succeeded` only when the parsed `status` is `succeeded` or `partial`". Changed text: `spec:182` (7.2 step 3), "its `--outcome` matches the contract's `status` under WC-5 (from P1) or the named report under WC-5 (P0, N-1)".
- Dependent text: `spec:79` ("the worker reports the named file until Phase 1 adds the contract"); `spec:91` (`troubleshoot`: `REPORT.md`, `report_path`); `spec:194` (AC-0.4: "steps 1-3 and 5-7 pass"); `spec:158` (P0 smoke runs carry no contract).
- Sentence: "An implementer who follows `spec:63` as written in P0 for `/sc:troubleshoot`, whose named `REPORT.md` is complete (`spec:91`, `spec:79`), finds that the failed branch does not apply, since the report is neither missing nor zero bytes, and that the succeeded branch requires a parsed `status`, which P0 does not produce. So `spec:63` permits no outcome for that run. That is wrong because `spec:63` also requires exactly one `worker_done`, and AC-0.4 step 3 (`spec:182`, `spec:194`) requires the outcome to match."
- Why it is blocking: two stated texts contradict for the same clean P0 run (`spec:63` against `spec:182` and `spec:194`), and an acceptance criterion cannot pass as written. The grading rule names both cases. `spec:201` (AC-2.3) shows that `--outcome succeeded` is the intended clean-run outcome, but only in P2 with a contract, so it does not cover P0.
- Attack (Whittaker, FR-2.2 Divergence): "I can break this specification by **Divergence Attack**. The invariant at **WC-5 (spec:63)** fails when **the P0 named report is present and non-empty**. Concrete attack: the P0 smoke run of `/sc:troubleshoot "<symptom>"` writes a complete `REPORT.md` and no contract; the failed branch does not fire; the succeeded branch needs a parsed status that P0 does not produce; the worker sends no outcome, or sends one the text forbids. Trace: before the N-1 revision = `failed` (wrong); after = no permitted outcome (wrong)."
- Origin: the revision after round2. It added a P0 failed clause to `spec:63` and no P0 success clause.
- Experts: Nygard (settlement and failure reporting), Adzic (testability of AC-0.4), Hohpe (exactly-once `worker_done`), Whittaker (above).
- Recommendation: narrow `spec:63` by adding one P0 success clause that names its condition, for example "in P0, `--outcome succeeded` when the named report is present and non-empty; from P1, `--outcome succeeded` only when the parsed `status` is `succeeded` or `partial`". Cite N-6 on the added words. Adds no mechanism.
- Priority: High. Quality impact: high. Every P0 smoke run would have no defined pass outcome, so the P0 gate at `spec:158` cannot be passed.

### N-7 (Medium, new, origin=changed): the P0 "named report" is not named per command, so one smoke command has no file to test

- Changed text: `spec:63` and `spec:182` both rely on "the named report" in P0. `spec:83` (adversarial) names no file: "contract, but filename not fixed". `INV-A:35` says the skill names no filename, and real runs wrote `<output>/adversarial/return-contract.yaml`.
- Dependent text: `spec:194` lists `/sc:adversarial --compare ... --output <dir>` as a P0 smoke run. `spec:91` (troubleshoot, `REPORT.md`) and `spec:92` (workflow, package contract) name their files.
- Sentence: "An implementer who follows `spec:63` in P0 for `/sc:adversarial --output <dir>` cannot tell which file is the named report. So the implementer cannot tell whether it is missing or zero bytes, and the match test of `spec:182` has no file to compare. Choosing a file is a guess."
- Why Medium: the requirement is one the document never states (an undefined file), not a stated text that does harm. The grading rule puts that at Medium.
- Recommendation: name the P0 report for each command in section 3.1, as round2's N-1 recommendation asked and the candidate did not do. For adversarial, name the file `INV-A:35` records (`<output>/adversarial/return-contract.yaml`) or record the choice under `## Decisions`.

### Carried Medium items on changed line spec:63 (re-graded here)

- M-2 (partial maps to succeeded, `spec:63`, `spec:262`): re-graded **Medium**. The mapping is stated ("mapped to Orca's two outcomes in WC-5", `spec:262`), so an implementer does not guess it. The open question is whether `partial` should fail, which the document does not decide.
- M-3 (write-then-send order, `spec:62` and `spec:63`): re-graded **Medium**. `spec:62` says the contract is written on every outcome and `spec:63` says `worker_done` is sent exactly once. The order between the two is still not stated, and the change at `spec:63` does not alter it.

### Minor note on a changed line

- N-5 (minor, origin=unchanged, quotes changed line): `spec:182` now names the P0 report, but its P1 wording "its report path is the WC-4 contract path" still omits the workflow exception (`spec:73`, `spec:92`). Minor note.

## Carried follow-up candidates (not re-graded; unchanged lines, carried from round2 and not re-read this run)

Medium:
- N-4 (round2, Medium): `spec:105` (cli-portify, "file location unnamed") and `spec:114` (pr-submit, "contract beside `monitor-run-<PR>.jsonl`") still give no file rule under WC-4.
- M-1 WC-1 has no owner or phase (`spec:59`); M-4 WC-3 answer path and ask timeout (`spec:61`); M-5 SA-2 check misses `orca-cli` and uppercase `ORCA` (`spec:172`); M-6 SA-4 versus section 3 edits (`spec:149`); M-7 nesting layers (`spec:122`); M-8 plugin mirror (`spec:279`); M-9 P0 smoke runs do not test WC-2 (`spec:79`, `spec:194`); M-10 4-minute rule (`spec:68`); M-11 WC-5 has no automated test (`spec:195`); M-12 checkpoints undefined (`spec:70`); M-13 missing `--output` in an unattended brief (`spec:62`), still open; M-14 WC-11 fixed output dirs (`spec:85`, `spec:119`); M-15 brief template owner and version (`spec:73`, `spec:158`).

Minor:
- N-2 (round2): adversarial contract location (`spec:83`) differs from the observed path in `INV-A:35`, and no `## Decisions` entry records the change.
- N-3 (round2): "changed command" is undefined (`spec:52`, `spec:76`, `spec:79`).
- Round2 carried minor notes (`round2:132`): `spec:215` cites `CAPS:12-13`; `spec:80` says "share the current worktree by default"; `spec:23` makes a PR #329 claim (`README:12`).

Noted (not re-graded): B-2 and B-4, see above.

## Guard Condition Boundary Table (changed guards only)

The re-review table covers guards on changed lines only (`command.md:261` item 5). Changed guards: WC-5 outcome mapping (`spec:63`, P0 and P1 clauses) and the 7.2 step 3 outcome check (`spec:182`).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome mapping (P0) | spec:63 | Zero/Empty | named report missing or zero bytes | `failed` | Stated (N-1 fix) | OK |
| WC-5 outcome mapping (P0) | spec:63 | Typical | named report present, non-empty and complete (`REPORT.md`, `spec:91`) | no permitted outcome | `failed` does not apply; `succeeded` needs a parsed `status` that P0 does not produce (`spec:79`) | GAP (N-6, blocking) |
| WC-5 outcome mapping (P0) | spec:63 | Legitimate Edge Case | named report present but truncated | not stated | Left out as a separate row, reason: a P0 markdown report has no parse step, so a truncated report falls under the same gap as the typical row (N-6) | row left out, reason given |
| WC-5 outcome mapping (P0) | spec:63 | Zero/Empty (no named file) | adversarial (`spec:83`, `INV-A:35`) | not stated | No file to test for missing or zero bytes | GAP (N-7, Medium) |
| WC-5 outcome mapping (P1) | spec:63 | Zero/Empty | contract exists, 0 bytes | `failed` | Stated (B-5), unchanged | OK |
| WC-5 outcome mapping (P1) | spec:63 | One/Minimal | `status: Succeeded` (case) | `failed` (outside the four values) | Stated (B-5), unchanged | OK |
| WC-5 outcome mapping (P1) | spec:63 | Sentinel Value Match | `status: partial` | `succeeded` | Stated mapping (`spec:262`); lossy, recorded as M-2 | OK as written; M-2 |
| 7.2 step 3 | spec:182 | Typical (P0) | named report complete | `--outcome` must match "the named report under WC-5" | WC-5 gives no outcome for this case (N-6) | GAP (N-6, blocking) |
| 7.2 step 3 | spec:182 | Zero/Empty (P0, adversarial) | no named file | match undefined | `spec:83` names no file (N-7) | GAP (N-7, Medium) |

FR-8: GAP rows are N-6 (blocking) and N-7 (Medium). FR-9 (blank behaviour): none blank; the `none` entries are explicit values graded under FR-8. FR-10: the table is complete for the changed guards; the one left-out input class has its reason in the table.

Pipeline Dimensional Analysis: not triggered by the changed lines. They change which report one worker reads and when `worker_done` is sent. No changed line alters a count along a data pipeline.

## Re-review result

- Prior blocking findings: B-1 resolved, B-3 resolved, B-5 resolved, N-1 resolved as to the stated defect.
- Regressed: none.
- New blocking finding: N-6.
- Coverage line: not `scoped PASS`, because a blocking finding is open.

## Escalation (review 3 of 3)

- This is the cap (`command.md:261`). No fourth review runs.
- The VERIFY prompt runs before escalation, in a fresh context with only the candidate and the N-6 finding. If it confirms N-6, the loop escalates to the user with N-6 as the open blocking finding. If it confirms none, the loop ends with no confirmed blocking finding, which counts as PASS, and the user gets the noted list (`document_review_loop_prompts.md`, VERIFY, "After the reply").
- The Reviser brief is omitted at review 3 (`command.md:263`). No revision is requested from this report.
- Brief clauses overridden: none, since this run had no brief beyond the command.

verdict: FAIL
