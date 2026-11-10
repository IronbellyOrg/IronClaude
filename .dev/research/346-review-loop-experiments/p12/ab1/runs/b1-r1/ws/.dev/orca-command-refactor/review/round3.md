review: 3 of 3

# Re-review (critique mode, focus requirements,architecture)

- candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 eb7a9219ddeed9546c90120ee7c914556a7d57ba7d99b5a503bf74f7881bf609
- baseline: .dev/orca-command-refactor/specs/history/spec-v2.md sha256 4608dec8f5f47699675938e131fc3f4f5f3fbb7915dd6eb492ed6df1a5933d83 (equals the candidate hash recorded in round2.md:6, so the baseline is the text round 2 reviewed)
- prior: .dev/orca-command-refactor/review/round2.md sha256 727568dc468342ed79630f504bedb91800a5b8900fedbdc9ebf2a045491e46aa (header `review: 2 of 3`, `verdict: FAIL`, round2.md:1,99)
- reviewer model: claude-sonnet-5-5
- baseline: present. Review loop prompt file read in full (home/.claude/rules/prompts/document_review_loop_prompts.md, RE-REVIEW prompt followed). README read (.dev/orca-command-refactor/README.md).
- `.claude/agents/rf-qa.md` and `~/.claude/agents/rf-qa.md` do not exist in the sandbox (home/.claude holds only rules/), so the rf-qa Fix Cycle steps 1-5 could not be read; the Review Loop section 5 rules were applied standing alone.
- Citation note: inventory citations in the spec (`INV-A`, `INV-B`, `CAPS`, `cmd/`, `sk/`) are mostly outside what I checked; none is relied on below. Line numbers are candidate line numbers (the diff changes no line count, so they equal baseline line numbers).
- Verification block from round2.md:2: confirmed blocking id R2-1 only; no rejected ids.

## Step 1. Evidence block (`diff -w BASELINE CANDIDATE`, 2 hunks: lines 62 and 79)

BEFORE (baseline, `<`):
- 62 (WC-4): "`--report-dir <dir>` is a directory-valued flag the brief always passes."
- 79: "Every brief also passes `--unattended --report-dir <dir>` (WC-4, section 2.3)."

AFTER (candidate, `>`):
- 62 (WC-4): "`--report-dir <dir>` is a directory-valued flag the brief passes from the phase that adds it (the Phase column of each row in section 3; before that phase the brief omits it and the worker reports the row's existing report file)."
- 79: "From the phase that adds them, the brief also passes `--unattended --report-dir <dir>` (WC-4, section 2.3); a brief before that phase omits them."

The rest of both lines is identical apart from whitespace.

Self-check: each AFTER quote found once by `grep -cF` in the candidate (count 1 each); each BEFORE quote found once in the baseline (count 1 each). Roles are not swapped.

## Prior blocking findings (from round2.md)

| id | status | basis (AFTER text only) |
|---|---|---|
| R2-1 | resolved | Line 79 now makes `--unattended --report-dir` a brief requirement only "from the phase that adds them" and says "a brief before that phase omits them"; line 62 says the same for `--report-dir` and tells the worker to report "the row's existing report file" before then. The two named contradictions are gone. P0 (line 158, "no command edits") and AC-0.4 (line 192, no `--unattended`, no `--report-dir`, step 4 uses the command's existing report file) now agree with 62 and 79: a P0 smoke brief omits both flags. Line 79 still lists P1 and P2 phase membership in its first sentence, so the phase is stated beside the rule. |

No finding was deferred or withdrawn by the reviser. Only round2 R2-1 was blocking; M1-M5 stay resolved and are not touched by the diff (the diff is two lines).

## Findings on changed lines

None blocking. Two changed lines, checked against the requirements that depend on them:

- Line 62 and the WC-4 contract path: `<report-dir>/return-contract.yaml` is unchanged; only the "always" is narrowed. Phase 3 rows (83, 92) and acceptance step 3 (182) still cite the same path. Consistent.
- Line 79 against line 154 ("Each command gains its flags and section only in the phase its row names") and 159 (P1 row): consistent; 3.1 commands gain `--report-dir` in P1 or P2 and are briefed with it only then.

### Residual text that still reads universal (origin=unchanged, depends on changed lines 62 and 79; Medium, not blocking)

- R3-M1. Line 95 (section 3.2 intro, unchanged): "Every brief also passes `--report-dir <dir>` (WC-4)." and line 73 (section 2.3, unchanged): the brief states "the exact command line including `--unattended`" and "the `--report-dir` directory". Read next to changed lines 62 and 79, these read as unconditional. Line 95 sits under 3.2, whose commands all gain the flag in the phase their row names (154), so a wrong build needs the implementer to apply 73's general sentence to a P0 smoke run and ignore 62 and 79, which say the contrary and are the specific text. That is a guess about the worse of two readings, so Medium. Suggested narrowing (optional): add "from the phase that adds them" to 73 and 95. Quotes: "Every brief also passes `--report-dir <dir>` (WC-4)." (line 95) and "the exact command line including `--unattended`" (line 73).

## Carried follow-up candidates (from round2.md, all origin=unchanged by this diff, none blocking)

- R2-M1: line 114 (pr-submit, unchanged) "the worker may use `ask` or `escalation`" against WC-3 (61) requiring the brief line `on a blocked gate: ask`; pr-submit is P4 behind D3. Still open, still Medium.
- R2-M2: acceptance step 6 (line 184) says "only files under the brief's output directory" while the contract sits in `<report-dir>`; name `<report-dir>` there. Not touched by this diff. Still Medium.
- R2-M3: 3.2 rows 97-129 say "add a report path/output path; contract"; line 76 covers it. Clarity note.
- R2-M4: spec-panel row (line 120) says "add `--output`"; the command definition I was given (command.md:460-461) already has `--report-dir` and a file-valued `--output`. The row cites `INV-B:43,177-185`, which I did not re-check against a live repo. UNVERIFIED.
- Minor: AC-1.1 (line 195) must exclude the `load` token by name; init-lite is a P1 member for flags and section only (87, 159).

## Guard Condition Boundary Table (changed guards only)

The only changed guard is the phase condition "from the phase that adds them" (62, 79).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| brief passes `--report-dir` | 62, 79 | Zero/Empty (phase not yet reached, e.g. P0) | no flag | false | brief omits flags; worker reports the row's existing report file (62); AC-0.4 step 4 uses it (192) | OK |
| brief passes `--report-dir` | 62, 79 | Typical (phase reached, e.g. P1 command) | flag present | true | contract at `<report-dir>/return-contract.yaml` (62) | OK |
| brief passes `--report-dir` | 62, 79 | Legitimate edge case (command's phase is P2 but run in P1) | no flag | false | row's existing report file (62, 79) | OK |

Classes left out: One/Minimal and Maximum/Overflow cannot occur for a boolean phase guard; Sentinel Value Match has no sentinel.

## Coverage

Covered: the two changed hunks (lines 62, 79), the prior blocker R2-1, and the lines that depend on them (73, 95, 154, 158, 159, 182, 192). Scoped PASS: changed lines + prior blockers. This is not whole-document assurance; whole-document assurance needs a separate, labelled first review whose blockers are escalated and never start a fourth review. Not covered: unchanged sections 1, 4, 5, 8 and every inventory citation (UNVERIFIED).

## Follow-up candidates (Medium and minor; not in any Reviser brief)

R3-M1, R2-M1, R2-M2, R2-M3, R2-M4 (UNVERIFIED), and the minor notes above. The session that ran the review asks the user once whether to open an issue for them; none is created here.

scoped PASS: changed lines + prior blockers

verdict: PASS
