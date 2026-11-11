# Revise 1: Orca worker-contract spec (blocking findings F-1, F-2, F-3)

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, edited in place. Report: `.dev/orca-command-refactor/review/round1.md` (its Reviser brief, `round1.md:218-222`, lists F-1, F-2, F-3). Citation key: `spec:N` = line N of the candidate (line count unchanged at 285, so before and after line numbers match); `r1:N` = line N of `round1.md`; `INV-A:N`, `INV-B:N` = `inventory/commands-a.md`, `commands-b.md`. Medium and minor findings were left alone. No PASS is claimed.

## Byte accounting

| | bytes | sha256 |
|---|---|---|
| Before (`specs/history/spec-v1.md`, identical to the reviewed candidate, sha256 matches `r1:8`) | 57763 | d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d |
| After | 58573 | fd9020aeb88b0fd3aa673b34de70465e3d6d2d18a0ec0245de39c5d2383e536b |
| Net | +810 | |

Per finding id, byte-level (a byte-sequence diff of before against after; a replaced word counts as deleted plus added, so unchanged letters inside a replaced word are counted on both sides):

| Finding | Bytes added | Bytes deleted | Net |
|---|---|---|---|
| F-1 | 535 | 71 | +464 |
| F-2 | 116 | 30 | +86 |
| F-3 | 283 | 23 | +260 |
| Total | 934 | 124 | +810 |

The F-1 and F-3 edit to spec:73 is one sentence; its added bytes are split by the id cited in the inserted text (F-1: 52 bytes, F-3: 38 bytes). The spec grew because each fix names the narrowing it makes with its finding id; no section, table or rule that a listed finding does not call for was added. Not done: no additions elsewhere, no edit to a Medium or minor item.

## Dispositions

| Finding | Disposition | Where applied | What changed | Why this repairs it |
|---|---|---|---|---|
| F-1 | Applied | spec:73 (section 2.3), spec:76 (section 3 intro), spec:154 (section 6 intro), spec:159 (P1 row), spec:195 (AC-1.1). Bytes: +535 / -71. | (1) P1 no longer gives the flag to "every command in sections 3.1 and 3.2"; it gives it to "the P1 commands in the next column only" (spec:159, which lists analyze, build, business-panel, design, document, explain, index, test, load and the fixes to adversarial, cleanup-audit, index-repo, workflow). (2) A general rule in section 6 (spec:154): a command gains `--unattended` and its `## Unattended mode` section only in the phase that resolves all of its gates, that is the Phase column of its 3.2 row or the phase of its 3.1 small fix; brainstorm and init-lite (3.1 "Small fix: None", spec:84, 87) gain neither; a P4 command that D2-D4 leave unchanged (pr-submit under D3 (a), `spec:240`) gains neither. (3) Section 3 intro (spec:76) says the section arrives "in the phase its row names and not earlier". (4) Section 2.3 (spec:73) says the brief includes `--unattended` "from the phase in which the command gains it". (5) AC-1.1 (spec:195) now asserts the section for every command of the phases up to the one under test and its absence for later-phase and section-4 commands. | It removes the contradiction by narrowing, as the recommendation at `r1:69` asks: WC-2's guarantee (spec:60) is then true of every command that accepts the flag, because the flag exists only once that command's gates are resolved (P2 for 15 commands per spec:160, P3 for 4 per spec:161, P4 for implement, post-release, pr-submit per spec:162). spec:154 ("Phases 1-3 need no user decision; Phase 4 waits for D2-D4") stays true, since no P1 text writes a D2-D4 outcome. AC-1.1 can no longer be passed by a P1 command that still prompts, and it no longer demands a pr-submit section under D3 (a). The mechanical `gate-resolution` assertions stay in AC-2.1 (spec:199), unchanged. |
| F-2 | Applied | spec:176 (AC-C5), spec:193 (AC-0.3). Bytes: +116 / -30. | In both checks the filter `git diff -U0 master...HEAD -- <file> \| grep -E '^-[^-]'` is replaced by `git diff --numstat master...HEAD -- <file> \| awk '$2 != 0'`, with a short parenthetical citing F-2. Pass conditions ("prints nothing") are unchanged. | The old filter skipped any deleted line whose second character is `-`, such as the bullet `- Will Not: edit files`, which a diff shows as `-- Will Not: edit files` (`r1:131`). `--numstat` prints `added<TAB>deleted<TAB>path`, so the second column is the count of deleted lines whatever they start with, and a rewritten bullet counts as one deletion. This is the second option the recommendation offers (`r1:133`); it is a correction of the stated command, not a new mechanism. Checked in the sandbox: the old filter on a deleted-bullet diff printed nothing (exit 1); the new `awk` on numstat-format rows `1<TAB>1<TAB>path` printed the row, and on `12<TAB>0<TAB>path` printed nothing. These runs used printf-fed numstat-format rows, not a live `git diff --numstat` (no git repository is available in the sandbox), so the git side of the pipe is UNVERIFIED here; the numstat column order is git's documented format. |
| F-3 | Applied | spec:194 (AC-0.4), spec:73 (section 2.3, the "but not in the P0 smoke briefs (F-3)" clause). Bytes: +283 / -23. | AC-0.4 now reads steps 1-3 and 5-7 as follows because the flag and the contract arrive in P1: the step-1 brief omits `--unattended`; in step 3 the `--outcome` is compared with the status in the command's existing report (the "Report today" column of 3.1) and the report path is that file; step 4 is `test -s` on that file only. Section 2.3's "exact command line including `--unattended`" no longer applies to the P0 smoke briefs. | The three P0 commands (troubleshoot, workflow, adversarial; spec:158) are run before any command edit, so none accepts `--unattended` yet (spec:159), and troubleshoot writes `return-contract.yaml` only with `--caller task-unified` (`INV-B:242`) and a `REPORT.md` otherwise (spec:91), adversarial's contract filename is not fixed (spec:83; `INV-A:35`). The text now asks only for what P0 can produce, as the recommendation at `r1:76` says. Step 4's YAML assertion would have failed on `REPORT.md`, which is not YAML, so step 4 is narrowed to `test -s` for P0; that is the same defect (the check demanding the P1 contract) and the finding's step 3/4 evidence names it (`r1:73`). The rule that a failure "reopens section 1" (spec:194) is unchanged and is now a failure about Orca running commands, not about an absent flag. |

## Rejected findings

None. All three listed ids were accepted.

## Citations I could not check

- `sk/...`, `cmd/...`, `src/...`, `CLAUDE.md:` and `pyproject.toml:` lines inside the spec are not in the sandbox, so I did not re-verify them and did not change any. My own edits cite only spec lines, round1 lines and the two inventory lines above (`INV-B:242`, `INV-A:35`), which I read: `INV-B:242` quotes "return-contract.yaml only when --caller task-unified", and `INV-A:35` is the adversarial row. The remaining claim, that real `git diff --numstat` output has the deleted count in the second field, is from git's documented format and was not run here (UNVERIFIED).
