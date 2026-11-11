review: 2 of 3

# Gate-loop re-review: orca-worker-contract-spec.md (`/sc:spec-panel --mode critique --focus requirements,architecture --re-review`)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `0962971bc5e9e3d54fa29ae20237450890eefb0d54ec5b262606d398c0bb57e2`
- baseline: `.dev/orca-command-refactor/specs/history/spec-g.md`, sha256 `e40e99ee4052bc08befc7a5c553a10250f30eed258a771b80b4e6936f8bf5bff` (equals the candidate hash recorded in the prior report, `review/gate.md:6`)
- prior: `.dev/orca-command-refactor/review/gate.md`, sha256 `dfe9a92abc3664eaf302b476724f02d7197ba557b08a2a3ba9b41d1a5933f6b1`; its header is `review: 1 of 3` (`gate.md:1`), so N = 2. It is the gate review (`gate.md:8`), so this is the gate loop's one re-review (`document_review_loop_prompts.md:57-64`); the loop's own review count is not continued here.
- prompt followed: RE-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md`, read in full first; roles fixed by its table (CANDIDATE = `@file`, BASELINE = `--baseline`, PRIOR = `--re-review`)
- reviewer model actually used: claude-sonnet-5-5 (Sonnet 5.5)
- panel: Wiegers, Adzic, Cockburn (requirements); Fowler, Newman, Hohpe, Nygard (architecture); Whittaker (always active)
- citation key: `S:N` = line N of the candidate; `B:N` = line N of the baseline; `G:N` = line N of the prior report; `CAPS:N` = `inventory/orca-capabilities.md`
- Citation status: lines of the spec, the baseline, the prior report and the inventories were opened in this sandbox. References to `src/`, `CLAUDE.md`, `EVIDENCE.md`, `~/.claude/commands|skills|agents` are UNVERIFIED (not in the workspace).

## Step 1: evidence block

`diff -w BASELINE CANDIDATE` yields exactly one changed line, line 194 in both files (AC-0.4 row of section 7.3). No other line differs.

BEFORE (baseline, `<`):

```text
< | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
```

AFTER (candidate, `>`):

```text
> | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass, read as follows because no contract or `--unattended` flag exists in P0 (GF-01): the brief omits `--unattended`; in step 3 `--report-path` is the command's existing report file and `--outcome` matches that report, not a contract `status`; step 4 is skipped. Record the results in the phase report; a failure here reopens section 1 |
```

Self-check (run): `grep -nF` of the AFTER pass-condition text in the candidate hits S:194 only; `grep -nF` of the BEFORE clause "step 4 uses the command's existing" in the baseline hits B:194 only. Roles are not swapped. The edit matches the revise report (`review/revise-gate.md:23`, line 194, single edit, +176 bytes net; candidate size 59481 bytes agrees with `revise-gate.md:11`).

## Prior blocking findings

| id | prior status | now | basis |
|---|---|---|---|
| GF-01 | blocking (MAJOR), `G:25-30`, `G:109` | **resolved** | See below. |

Check of GF-01 against the AFTER text only. The defect (`G:28`) was that AC-0.4 required 7.2 step 3 to pass, and step 3 (S:182) demands an `--outcome` that matches the contract's `status` and a report path equal to the WC-4 contract path, while P0 has no contract (S:79, S:158) and S:73 demands `--unattended` that no unmodified command accepts until P1/P2 (S:159-160). The AFTER cell now states three things that remove each demand for P0 only: the brief omits `--unattended` (removes the S:73 demand), `--report-path` is the command's existing report file (removes the "WC-4 contract path" demand of S:182), `--outcome` matches that report and not a contract `status` (removes the WC-5 contract-status demand of S:182), and step 4 (S:183, contract existence and YAML) is skipped, which also covers the contract assertions. The text also gives its reason (no contract or flag in P0), so an implementer building P0 from S:158 (no command edits) can pass AC-0.4 without a contract. Steps 1, 2, 5, 6, 7 (S:181, 184-187) carry no contract or `--unattended` dependency, so "steps 1-3 and 5-7 pass" is consistent with every requirement that depends on the changed line. S:154 (later phases wait for section 7 checks) is therefore satisfiable by P0. Not regressed.

## Findings on changed lines

=== REQUIREMENTS ANALYSIS ===

No blocking finding. No Medium finding on the changed line.

- N-1 (minor, `origin=changed`, Wiegers): S:73 still says the brief carries "the exact command line including `--unattended`" with no P0 exception, and S:79 says ready commands "run as workers now if the brief uses the stated flags". AC-0.4 (S:194) is the only place that exempts P0, and it names its reason and the finding, so the two texts do not contradict in a way that yields a wrong build. Note only: a one-clause cross-reference at S:73 would remove the need to read S:194 to see the exemption. Not blocking, not a revision trigger.
- N-2 (minor, `origin=changed`, Adzic): the pass condition says `--outcome` "matches that report" but does not give a concrete example mapping for the three P0 commands (for example adversarial's `--output <dir>` report file). It is the same level of detail the baseline gave ("the command's existing report file", B:194). Note only.

=== ARCHITECTURE ANALYSIS ===

No finding. The change is a pass-condition reading in an acceptance table; it adds no interface, flag or file (Fowler, Newman). It leaves the P0 content (S:158), SA-1..SA-6 (S:146-151) and standalone behaviour unchanged. The Orca facts the check relies on (worker_done bound to the dispatched pane, CAPS:76 and CAPS:150) are unaffected. Pipeline Dimensional Analysis (FR-17): not triggered, no filter/aggregate stage on the changed line; no Quantity Flow Diagram required.

=== ADVERSARIAL ANALYSIS ===

- **Sequence attack:** on AC-0.4, running steps 1-7 out of order is not affected by the edit; step 4 is simply skipped. No break.
- **Zero/Empty attack:** if a P0 command writes no report at all, "`--report-path` is the command's existing report file" has nothing to name. S:79 says the worker "reports the named file", and the P0 command list was chosen from commands that have one; the case is old and not made worse by the edit. Not recorded as a finding (`origin=unchanged`, minor).
- **Sentinel collision / Divergence / Accumulation:** no sentinel, branch or counter on the changed line.

## Guard Condition Boundary Table (changed lines only)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| contract exists (AC-0.4 step 3/4) | S:194 | Zero/Empty | no contract (P0 case) | true | step 4 skipped; `--report-path` and `--outcome` use the existing report | OK |
| contract exists (AC-0.4 step 3/4) | S:194 | Typical | contract present (P1 onward) | false | AC-0.4 is a P0 row; P1+ rows use 7.2 unchanged (S:195-196) | OK |
| `--unattended` in brief (AC-0.4) | S:194 | Zero/Empty | flag omitted | true | allowed for P0 only | OK |
| `--unattended` in brief (AC-0.4) | S:194 | Typical | flag present | n/a | not applicable to P0 (commands do not accept it before P1/P2, S:159-160) | OK |

Classes left out: One/Minimal, Maximum/Overflow, Sentinel Value Match and Legitimate Edge Case: the changed line contains no count, size, sentinel or boundary value. FR-8/FR-9: no GAP; FR-10: table complete.

## Follow-up candidates

The Medium findings GM-01 to GM-17 and the minor notes MN-1 to MN-5 of the prior report (`G:32-105`) were not on the changed line, were not part of the reviser's brief (`G:111`), and are unchanged in the candidate; they remain follow-up candidates and are not re-graded here. Their status is not a prior blocking finding, so they are not in the table above. New notes from this review: N-1, N-2 (minor). The question whether to open an issue for the follow-up candidates is left to the session that owns the loop: this run had no user to ask and created no issue.

## What was covered

Step 1 diff (one changed line), self-check greps, the resolution of GF-01 against the AFTER text, the dependency check of the changed line against S:73, S:79, S:154, S:158, S:159-160, S:181-187, S:194-196 and the baseline lines B:194, panel passes (requirements, architecture, adversarial) and the guard table for the changed line. The reviser's byte accounting was checked against the file size (59481 bytes). Not covered: whole-document assurance (that was the gate review itself), and any source file outside the workspace (UNVERIFIED). No edit was made to the candidate.

coverage: scoped PASS: changed lines + prior blockers

Reviser brief: none; no blocking finding is open.

verdict: PASS
