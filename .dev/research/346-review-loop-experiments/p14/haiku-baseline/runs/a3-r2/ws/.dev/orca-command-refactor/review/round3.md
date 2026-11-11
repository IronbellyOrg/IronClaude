review: 3 of 3

# Spec-panel re-review: orca-worker-contract-spec.md (review 3 of 3)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (288 lines)
- candidate sha256: `284cc6b74e9164675f12bdb0a33d7d0c5edf49544b271cb956ec89ae5853237e`
- baseline (`--baseline`): `.dev/orca-command-refactor/specs/history/spec-v2.md` (288 lines)
- baseline sha256: `a6bb2fd31d271c13717322860b98be5dce7608e4f442926d61851162c5d899b7`
- prior report (`--re-review`): `.dev/orca-command-refactor/review/round2.md` (`review: 2 of 3`, `verdict: FAIL`)
- prior report sha256: `369b370eca164fd395ae14ee98c4407801e71adc646ce7491fb2dc589fe171ae`
- reviewer model: claude-haiku-5-5 (Haiku 5.5)
- mode: critique; focus: requirements, architecture; prompt: RE-REVIEW from `~/.claude/rules/prompts/document_review_loop_prompts.md` (sandbox home copy); N = prior 2 + 1 = 3
- Citation convention: `:N` alone is a line of the candidate; `spec-v2.md:N` is a line of the baseline.
- Provenance note: round2.md's header records candidate sha256 `a6bb2fd3...`, which is the sha256 of `specs/history/spec-v2.md` (the baseline here). Round2 therefore reviewed the text now saved as spec-v2.md. The brief's baseline is used as given.

## Coverage and evidence limits

- Read in full: `review/round2.md`, `specs/history/spec-v2.md` (baseline), `specs/orca-worker-contract-spec.md` (candidate), `README.md`, `command.md`, the RE-REVIEW prompt file `home/.claude/rules/prompts/document_review_loop_prompts.md`.
- Rule file for the fix cycle: `.claude/agents/rf-qa.md` (project) and `~/.claude/agents/rf-qa.md` are not in the sandbox. Review Loop bullet 5 applies: steps 1-5 of the rf-qa Fix Cycle were not run, and the rules in `command.md` Review Loop stand alone.
- No `--unattended` flag is in this run, so `~/.claude/WORKER-CONTRACT.md` was not needed and was not read.
- `diff -w` between baseline and candidate shows one changed line pair (hunk `73c73`). Every other line of the candidate is identical to the baseline, so round2's findings on the other lines carry over unchanged.
- `inventory/*.md` and `inventory/orca-capabilities.md` were not opened in this loop. Citations to `CAPS:`, `cmd/`, `sk/`, `src/`, `INV-A`, `INV-B` were not re-checked and stay UNVERIFIED, including `CAPS:115`, `CAPS:116` and `CAPS:107-113` cited on changed line 73.
- Git was not used. Only `review/round3.md` was written.

## Re-review guard table (guards on changed lines only)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| unattended non-empty `--output` refusal | `:73` | Zero/Empty: new per-attempt directory | empty directory | proceeds | writes contract (WC-4, `:62`) | OK |
| unattended non-empty `--output` refusal | `:73` | Typical: unattended run into a non-empty directory, no resume flag | non-empty directory | refuses | writes no contract; `worker_done` body states refusal | OK (AC-1.5, `:199`) |
| unattended non-empty `--output` refusal | `:73` | Legitimate edge: unattended run that passes a resume flag | non-empty directory | not refused by `:73` (the refusal applies only to a command with no resume flag) | resumes | OK |
| unattended non-empty `--output` refusal | `:73` | Sentinel: first attempt in the same directory wrote only a contract | non-empty directory | refuses | first attempt's contract stays on disk | GAP, Medium (M-09) |
| standalone non-empty `--output` (no `--unattended`) | `:73` | Typical: plain run into a non-empty directory | non-empty directory | not refused | writes to `--output` as today | OK (SA-1, `:146`) |

## Step 1, evidence block

Roles are fixed: BASELINE is `specs/history/spec-v2.md`, CANDIDATE is `specs/orca-worker-contract-spec.md`. Command run: `diff -w BASELINE CANDIDATE`. Output (verbatim):

```text
BEFORE (baseline), lines starting "<":
< The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). For a retry (`worker-start --retry-of`, `CAPS:116`) the coordinator passes a new `--output` for each attempt, for example `<dir>/attempt-2/`. A command with no resume flag refuses a non-empty `--output` directory: it stops before writing into it, writes no contract there (the one outcome without a contract under WC-4), and states the refusal in the `worker_done` body (F-05). Until a command has a per-run output path (the `--slug` flag added in P1), the coordinator runs at most one worker of that command per worktree (WC-11, F-06). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).

AFTER (candidate), lines starting ">":
> The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). For a retry (`worker-start --retry-of`, `CAPS:116`) the coordinator passes a new `--output` for each attempt, for example `<dir>/attempt-2/`. In unattended mode, a command with no resume flag refuses a non-empty `--output` directory: it stops before writing into it, writes no contract there (the one outcome without a contract under WC-4), and states the refusal in the `worker_done` body (F-05). Without `--unattended` this refusal does not apply and the command writes to `--output` as it does today (SA-1, F-08). Until a command has a per-run output path (the `--slug` flag added in P1), the coordinator runs at most one worker of that command per worktree (WC-11, F-06). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
```

Roles confirmed: the AFTER line occurs in the candidate and the BEFORE line occurs in the baseline (see Self-check).

## Self-check

- `grep -nF` of the AFTER line (without its `>`) in the candidate: 1 of 1 found, at `:73`.
- `grep -nF` of the BEFORE line (without its `<`) in the baseline: 1 of 1 found, at `spec-v2.md:73`.
- No role swap occurred.

## Prior blocking findings (round2)

| Prior id | Status | Evidence (candidate) |
|---|---|---|
| F-08 | resolved | `:73` now scopes the refusal: "In unattended mode, a command with no resume flag refuses a non-empty `--output` directory" and "Without `--unattended` this refusal does not apply ... (SA-1, F-08)". Consistent with `:62` (WC-4, "except the non-empty-directory refusal in section 2.3"), `:141` (§5, hard requirement on every phase), `:146` (SA-1, without `--unattended` output paths stay as today), `:148` (SA-3, a standalone default run writes the same files), and `:199` (AC-1.5, runs with `--unattended`). The worker-run data-loss protection (F-05) is kept. |
| F-05 | resolved, not regressed | Retry overwrite protection still applies in unattended mode (`:73`, `attempt-2/` per attempt). The scoping change does not weaken it. |
| F-01 | resolved, not regressed | `:61` (WC-3 Ruling exemption). Line not in the diff; round2 status carried. |
| F-02 | resolved, not regressed | `:159` (P1, open gate writes `status: blocked`); `:200` (AC-1.6). Lines not in the diff. |
| F-03 | resolved, not regressed | `:147` (SA-2, no Orca mention permitted); `:61` (ask command only). Lines not in the diff. |
| F-04 | resolved, not regressed | `:83`, `:115`, `:125` (WC-4 paths). Lines not in the diff. |
| F-06 | resolved, not regressed | `:107`, `:110` (`--slug` rows); `:73` one-worker-per-worktree sentence unchanged in substance; `:201` (AC-1.7). |
| F-07 | resolved, not regressed | `:88` (tdd precise prompt); `:89` (troubleshoot excludes `--depth deep`). Lines not in the diff. |

No prior blocking finding is open.

## Findings on changed lines

No blocking finding.

Sentence test on `:73`: an implementer who follows the new text as written builds a command that refuses a non-empty `--output` only when it runs unattended and has no resume flag. This matches `:62`, `:146`, `:148` and `:199`. No two stated texts contradict each other on this point, so F-08 does not recur.

## Findings on lines quoting a changed line

### M-09 (Medium), origin unchanged, quotes changed line `:73`: a refused run can pass the live check

- Stated text: `:182` (§7.2 step 3) requires that the `worker_done` report path "is the WC-4 contract path". `:183` (§7.2 step 4) passes on `test -s <contract>` and the YAML schema check, with no check that the file was written by this run. Line `:73` says a refused run "writes no contract there".
- Sentence test: an implementer who follows `:183` as written, in a directory where a refused run left an earlier attempt's contract, builds a live check that passes on a file this run did not write, which is a wrong outcome.
- Why Medium, not blocking: the stale-file case needs a second run into the same directory. `:73` and `:64` say a retry gets a new `--output` per attempt (for example `attempt-2/`), so the case arises only when a person or coordinator reuses a directory. Nothing is lost and no safety boundary is crossed. Medium and minor findings never fail the review.
- Optional fix for a later revision (not required): in `:183`, require that the contract's mtime is after dispatch, or that the target directory is empty before dispatch.

## Changed lines checked with no finding

- `:73`, the new "Without `--unattended`" sentence: checked against `:141`, `:146`, `:148`. No finding.
- `:62` (WC-4): "except the non-empty-directory refusal in section 2.3" now matches the unattended-only refusal. No finding.
- `:199` (AC-1.5): runs with `--unattended`, so it tests the scoped refusal correctly. No finding.

## Follow-up candidates (Medium and minor; not blocking; none created)

These need the user's answer before any issue is opened. None is created.

- **M-09**: listed above.
- The other follow-up items in `.dev/orca-command-refactor/review/round2.md:151-159` sit on text that this diff does not change. They are not re-graded in this loop and stay as round2 recorded them.

## Notes (not graded)

- N-01: citations to `CAPS:`, `cmd/`, `sk/`, `src/`, `INV-A`, `INV-B` were not re-checked in this loop and stay UNVERIFIED.
- N-02: the provenance note in the header (round2's candidate hash equals the spec-v2 hash).
- N-03: this is a scoped review. Its coverage is changed line `:73` and the prior blocking findings only. It is not whole-document assurance. Whole-document assurance needs a separate, labelled first review; none is claimed here.
- N-04: within the dependencies of `:73` that were read (`:62`, `:64`, `:141`, `:146`, `:148`, `:182-183`, `:199`), no older severe defect was found.

Coverage: `scoped PASS: changed lines + prior blockers`

verdict: PASS
