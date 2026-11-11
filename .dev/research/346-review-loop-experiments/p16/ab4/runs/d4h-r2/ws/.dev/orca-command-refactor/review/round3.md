review: 3 of 3
# Re-review of the orca-worker-contract spec (coordinator RE-REVIEW prompt, reviewer: claude-haiku-5-5)

candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 24e411dcd5b98e3947b103fd3ff76a76e2a8ddec93e2c6e4f42c03d1f20513c9
baseline: .dev/orca-command-refactor/specs/history/spec-v2.md sha256 54648b506bfdcd80743a1d2154ba8247546181fddf2026636e6e105d2c2bbbc5
prior: .dev/orca-command-refactor/review/round2.md sha256 24da95f6e4192e142802118240bd7cbe080ff1ac56a7d8f5acbdd6d096d62b23 (review: 2 of 3)
lint: .dev/orca-command-refactor/review/lint-3.md sha256 c541a2870a261c97a143036cc8d3649ec4fff050fbdca77bfa9bcb6e26a4a8aa (Checks: REF; Findings: 0)
reviewer model: claude-haiku-5-5

Header notes for the coordinator: round2.md:6 records the candidate as sha256 54648b...; that hash is the sha of spec-v2.md, which is this run's baseline (verified by sha256sum). round2.md:7-8 names spec-v1.md as the baseline; this run's brief names spec-v2.md, and this review uses spec-v2.md. The current candidate (24e411...) is the text after round2.md; the round2 verification shows it was written after round2 (lint-3.md:1 records its hash).

Coverage: scoped PASS scope = the 3 changed hunks of the candidate (6 lines: :92, :198, :209) plus the prior blocking ids M16 and N1. Not a whole-document review. Focus applied: requirements and architecture, on the changed lines only. The rf-qa.md "Process of the Fix Cycle" could not be read: no `.claude/agents/rf-qa.md` exists in the workspace or in the sandbox home, so the Review Loop rules in command.md (section "Review Loop", bullets 1-7) were applied alone. Lint: lint-3.md:3 "Checks: REF. Findings: 0." and lint-3.md:5 "No findings." No lint id needs an address. The Improve step was not run and no spec was edited.

## Step 1: evidence block

Roles are fixed: BASELINE = specs/history/spec-v2.md, CANDIDATE = specs/orca-worker-contract-spec.md. Command run: `diff -w BASELINE CANDIDATE` (exit 1, three hunks, 92c92, 198c198, 209c209). Both files have 285 lines.

```text
92c92
< | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Add `--output-dir <dir>`; the pre-creation STOP contract goes to `<output-dir>/return-contract.yaml`, since no package id exists before creation, and the post-creation contract stays at its package path (WC-4 "every outcome"; M12) (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
---
> | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Add `--output-dir <dir>`; the worker's contract is `<output-dir>/return-contract.yaml` on every outcome, pre-creation STOP and post-creation alike, since no package id exists before creation (WC-4 "every outcome"; M12). After creation it lists the package contract `.dev/tasks/to-do/<id>/return-contract.yaml` under `artifacts`, and WC-5 reads only the `<output-dir>` file (N1) (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
198c198
< | P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs |
---
> | P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path; workflow states that `<output-dir>/return-contract.yaml` is written on every outcome and names the package contract as an artifact (N1) |
209c209
< | P4 | AC-4.2 | `/sc:post-release <version> --unattended --output <dir>` with no authorization flags | no install, VM, commit or PR: `git log -1` unchanged and no new PR from `gh pr list --repo IronbellyOrg/IronClaude --author @me`; the contract lists each outward step as `skipped`, and a process audit (`ps -ef` before and after, for installer or VM processes) shows none started (M16) |
---
> | P4 | AC-4.2 | `/sc:post-release <version> --unattended --output <dir>` with no authorization flags | no commit or PR: `git log -1` unchanged and no new PR from `gh pr list --repo IronbellyOrg/IronClaude --author @me`; the contract lists each outward step as `skipped`; and no install into the audited locations: a listing of each install target the install step uses (the throwaway venv, the `pipx` home, and the container and VM lists, `sk/sc-post-release-protocol/SKILL.md:129-131`, UNVERIFIED here) is unchanged before and after. The pass covers those locations only, so an install elsewhere is not shown by this check, and the `skipped` entries are the primary evidence (M16) |
```

Self-check (run before the verdict): each of the 3 quoted BEFORE lines (without `<`) matched exactly once, as a whole line, in BASELINE (grep -cxF), and each of the 3 quoted AFTER lines (without `>`) matched exactly once in CANDIDATE. Roles confirmed; no swap.

## Prior blocking findings (from round2.md)

Round2 confirmed two blocking ids, M16 and N1 (verify-2.md:16; round2.md:2). Rejected ids M1, M9 and N2 are not prior blocking findings for this review (see "Noted, unactioned"). Other round-2 table entries marked resolved are not re-opened here because none of their cited text sits on a changed line, except M12, checked below.

| id | status | evidence (candidate line) |
|---|---|---|
| M16 | resolved | :209 no longer relies on a `ps` snapshot. The install check is now a before-and-after listing of each install location the install step uses, so an installer that writes to a listed location and exits before the second snapshot now changes the listing and fails the check. The residual transient-install case is F3 below (Medium). |
| N1 | resolved | :92 and :198 now name the same file. `<output-dir>/return-contract.yaml` is the worker's contract on every outcome (WC-4, `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:62`), and the package contract is listed under `artifacts`, which WC-4 defines as "every other file written" (:62). WC-5 (:63) reads only the `<output-dir>` file. No contradicting text remains. |
| M12 | resolved, not regressed | M12 (round2.md:82) concerned the workflow row's subdirectory rule. Row :92 now writes directly to `<output-dir>` and names no subdirectory, so the WC-4 subdirectory exception (:62) is not invoked. The post-creation half is covered by N1. |

Regressed: none. No prior report marked a finding resolved that now fails.

## Noted, unactioned (rejected by VERIFY step VF2; not prior blocking findings)

- M1: verify-2.md:10 rejected it (the P0 override at :194 governs step 3 of P0). Text unchanged (:182, :194). Note only.
- M9: verify-2.md:11 rejected it (:194 defers step 4 to P1; the phrase it quotes is not in the candidate). Text unchanged. Note only.
- N2: verify-2.md:14 rejected it (AC-1.1 at :195 is scoped by "section 3 phase", which section 3.1 does not assign to brainstorm or init-lite). Text unchanged (:78-87, :159, :195). Note only.

Coordinator note (process, not a verdict input): round2.md:133 still lists M1, M9, M16, N1 and N2 in its Reviser brief, although round2.md:2 says the brief "is narrowed to the confirmed ids". Per the Review Loop rule that a rejected id is a note, this review treats M1, M9 and N2 as notes and does not use round2.md:133.

## Findings on changed lines (origin=changed)

No blocking finding. Four Medium findings (F3 to F6) are listed under follow-up candidates. Each was graded by the grading check: each needs an assumption or an unnamed choice to produce a wrong outcome, so none is blocking.

### :92 (workflow row): no finding

Checked: WC-4 (:62) "written on every outcome" and its artifacts field; WC-5 (:63) absent-report rule; AC-0.4 (:194) still reads the package path in P0, which is correct before P1 changes the contract. The "Report today" column (:81) names the package path as today's state; it is not a conflict. The inventory agrees with the pre-change state: `INV-B:52` (the workflow row, `inventory/commands-b.md:52`) names `.dev/tasks/to-do/<id>/return-contract.yaml`, and `INV-B:267-275` (`inventory/commands-b.md:272`) says the package contract is written on every post-creation outcome and not for pre-creation STOPs. The cited `sk/sc-workflow-protocol/SKILL.md:58,66,72` and `refs/return-contract.md:3-19,39,41` are not in the workspace: UNVERIFIED here.

### :198 (AC-1.4): F6 (Medium)

An implementer who follows row :92 and adds the output-dir contract only to the command, and not to the workflow return-contract ref, fails AC-1.4 at its pass condition ("workflow states that `<output-dir>/return-contract.yaml` ..."). Row :92's "Other required change" text (:92) names no edit to the ref, and section 3's own rule (SA-4, :149) lists the ref only as a named defect fix. This fails closed; it does not pass a wrong result. The grep check also names "the workflow return-contract ref" with no path (:198). Medium.

### :209 (AC-4.2)

F3 (Medium): transient install. Grading sentence: "An implementer who follows AC-4.2 as written runs an install step that creates its throwaway venv, installs into it, and removes the venv; the before and after listings match, the AC passes, and an install ran." Whether the install step removes its venv is an assumption about `sk/sc-post-release-protocol/SKILL.md:129-131`, which is not in the workspace (UNVERIFIED here). `inventory/commands-b.md:82` summarises that line as "throwaway venv, container, `pipx install .`, VM per runbook" and gives no cleanup behaviour. The text itself discloses that "an install elsewhere is not shown by this check", but it does not disclose the transient case. Because the wrong outcome needs the venv-removal assumption, this is Medium. If the protocol is confirmed to remove its venv, the coordinator should treat F3 as the reason to re-open the item; see the escalation note below.

F4 (Medium): the listing is not defined. "The container and VM lists" name no command, and "the `pipx` home" names no path. The inventory line (commands-b.md:82) names `pipx install .` but not a pipx home directory. An implementer chooses the listing, so the check's pass depends on that choice. Medium.

F5 (Medium): "the contract lists each outward step as `skipped`" names no field. WC-4 (:62) gives the fields `status`, `command`, `report_path`, `artifacts`, `blocked_question` ("at least"). The place for per-step `skipped` entries is not stated, so the check cannot be run exactly as written. This fails closed. Medium.

M16 is resolved (see table). The original defect, a `ps` snapshot that misses an installer which exits early, no longer applies to the stated process check, which was removed.

## Guard Condition Boundary Table (changed guards only; FR-8 to FR-10)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| package created before the contract is written | :92 | Zero/Empty (no package id before creation) | no package id | true (pre-creation) | `<output-dir>/return-contract.yaml` on every outcome (WC-4 :62) | OK |
| package created before the contract is written | :92 | Typical (creation succeeded) | package id present | false | `<output-dir>` contract, package contract listed under `artifacts` (:92, :62) | OK |
| package created before the contract is written | :92 | Legitimate Edge Case (a STOP after partial package write) | package id present, status blocked or failed | true | `<output-dir>` contract with status blocked or failed (WC-4, WC-5 :63) | OK |
| install step ran | :209 | Legitimate Edge Case (install in a throwaway venv that is removed) | listing unchanged, install ran | true | the listing check passes; no install is detected for that location | GAP (F3, Medium) |
| install step ran | :209 | Legitimate Edge Case (install in a location not on the list) | listing unchanged, install ran | true | stated: "an install elsewhere is not shown by this check" | OK (disclosed limit) |

Input classes left out: One/Minimal, Maximum/Overflow and Sentinel Value Match are not applicable to the creation-state or install guards on these lines (no numeric threshold and no sentinel value is compared). FR-8 applies to the GAP row only; it is graded Medium for the reason in F3.

## Medium follow-up candidates (not blocking; listed for the user, no issue opened)

- F1 (carried from round2.md:119, unchanged text :61): WC-3 names the implement Ruling as a safety-rule gate "such as" one example, so other safety gates (for example the WC-9 pr-submit and post-release authorizations) are not named. Needs a guess which gates are safety rules. Medium.
- F2 (carried from round2.md:120, UNVERIFIED; unchanged text :194): the step 3 outcome must match "that report's status under WC-5" for troubleshoot's `REPORT.md`. `inventory/commands-b.md:242` names `report_path` (REPORT.md) and `audit_log_path` in the output contract and no status field. Still UNVERIFIED.
- F3 (new, :209): transient install in a throwaway venv that is removed before the second listing, graded Medium; see above.
- F4 (new, :209): install-location listing has no named command or pipx home path; see above.
- F5 (new, :209): the `skipped` entries have no named field in WC-4 (:62); see above.
- F6 (new, :198): AC-1.4 requires text in the workflow return-contract ref, which row :92 does not name as an edit; see above.

## Escalation note (not a verdict input)

At review 3 the Reviser brief is omitted (Review Loop bullet 6). The verdict is PASS because no blocking finding is open. F3 is the one Medium that could change the outcome: if `sk/sc-post-release-protocol/SKILL.md:129-131` shows that the install step removes its venv, the transient install becomes a concrete wrong outcome, an FR-8 safety-boundary GAP, and the review would be FAIL. At review 3 a FAIL escalates to the user with the open blocking findings and does not start a fourth review.

## Lines checked and citations not verifiable

- Checked against the workspace: `inventory/commands-b.md:52`, `:82`, `:242`, `:267-275`; `specs/history/spec-v2.md` (diff); `review/round2.md:2,6-8,119-120,133`; `review/verify-2.md:10,11,14,16`; `review/lint-3.md:1,3,5`.
- UNVERIFIED (file not in the workspace): `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `sk/sc-post-release-protocol/SKILL.md:129-131`; `sk/sc-adversarial-protocol/SKILL.md` (AC-1.4); `.claude/agents/rf-qa.md`.

verdict: PASS
