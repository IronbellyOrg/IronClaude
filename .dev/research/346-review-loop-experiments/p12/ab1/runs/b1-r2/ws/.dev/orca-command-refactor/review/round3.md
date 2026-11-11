review: 3 of 3

# Re-review (critique mode, focus requirements,architecture)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` sha256 `e867c6d99ac7d3695eb8d12653c0adb84cc8683d98189276c8b5f83a5fe17627`
- baseline: `.dev/orca-command-refactor/specs/history/spec-v2.md` sha256 `9d73c078966cd5e27ccbfd4e244c2f43fce5d76c7c7f2bcbc9c574c5b6690ea6` (given, not missing; equals the candidate hash recorded in `round2.md`)
- prior: `.dev/orca-command-refactor/review/round2.md` sha256 `e49446ddf5435de5758513555c6db62f0c30bc949d61cb57313b253204f7cfe1`, header `review: 2 of 3`, so N = 3
- reviewer model: claude-sonnet-5-5
- review-loop prompts file read in full: `~/.claude/rules/prompts/document_review_loop_prompts.md` (RE-REVIEW prompt followed). The prior's verdict is FAIL at `review: 2`, not 3, so the cap check (HALT at a prior `review: 3` with FAIL) does not apply. `rf-qa.md` (project `.claude/agents/` or `~/.claude/agents/`) does not exist in the sandbox: UNVERIFIED, so the Review Loop rules stand alone.
- citation key: `spec:N` = candidate line N; `base:N` = baseline line N; `R2:` = `round2.md`; `INV-A`/`INV-B` = `.dev/orca-command-refactor/inventory/commands-a.md` / `commands-b.md`. Citations to `src/`, `cmd/`, `sk/` are UNVERIFIED (not in the sandbox) unless a `commands-*.md` line is given.
- `--iterations` is ignored in a re-review, the Improve step is skipped, and no revised spec is written.

## Step 1. Evidence block (`diff -w BASELINE CANDIDATE`)

One hunk (line 196). Changed lines, verbatim:

BEFORE (baseline, lines starting <)

    | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |

AFTER (candidate, lines starting >)

    | P1 | AC-1.2 | 7.2 live check on each P1 command except `load`, with `--unattended --output <dir>` (`load` writes no contract, section 3.2) | all steps pass |

Self-check (run): the AFTER line (without `>`) is found with `grep -nF` at `spec:196`; the BEFORE line (without `<`) is found at `base:196`. Roles are not swapped. The diff is not empty. Net change: the reviser's edit is exactly the one clause that R2's N1 recommended; no other line changed.

## Prior blocking findings

| id | status | evidence (AFTER text only) |
|---|---|---|
| N1 (AC-1.2 requires a live `--unattended --output <dir>` contract check on every P1 command, but `load`, a P1 command, takes neither) | resolved | `spec:196` now reads "each P1 command except `load`" and states "`load` writes no contract, section 3.2". This agrees with `spec:112` (`load` gets no `## Unattended mode` section, Report "none", "not as its own Task"), with `spec:159` (flag and section "in every command in sections 3.1 and 3.2 except load"; `load` listed "(usage line only)"), with `spec:195` (AC-1.1 excludes `load` and asserts it has no section) and with `spec:265` (Decisions: `load` gets no report file). The cross-reference "section 3.2" is correct: the `load` row is at `spec:112`, inside "3.2 Needs a change" (`spec:94`). Step 3 and step 4 of 7.2 (`spec:182-183`) are therefore never run against a command with no contract, so the P1 gate at `spec:167` ("every check in its block ... passes") is passable. |

No other prior blocking finding exists: R2 recorded M1-M5 as resolved and N1 as its only open blocker (R2 table and Reviser brief), and the VF2 verification block in R2 confirmed only N1.

## Findings on lines changed against the baseline

None blocking. One changed line (`spec:196`), checked against its dependents:

- `spec:195` (AC-1.1), `spec:159` (P1 row), `spec:112` (`load` row), `spec:265` (Decisions), `spec:167` (gate rule), `spec:182-183` (7.2 steps 3-4): all consistent with the AFTER text, see the N1 row above.
- Guard "except `load`" on the changed line (Guard Condition Boundary Table, changed lines only; Maximum/Overflow and Sentinel Value Match omitted, since no counts or reserved values exist for this guard):

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `except load` | `spec:196` | Zero/Empty | no P1 command other than `load` | n/a | cannot occur: `spec:159` lists nine commands plus three fixes | OK |
| `except load` | `spec:196` | One/Minimal | `load` | true | excluded from the live check; AC-1.1 asserts it has no section (`spec:195`) | OK |
| `except load` | `spec:196` | Typical | `analyze` | false | live check with `--unattended --output <dir>` runs through 7.2 | OK |
| `except load` | `spec:196` | Legitimate Edge Case | P1 "fixes to adversarial, cleanup-audit, index-repo" (`spec:159`) | not stated whether these count as "P1 command" for the live check | see F2 below | GAP (Medium) |

- origin=changed; no wrong outcome is named that an implementer builds from the stated text alone, so the GAP row is Medium (F2).

## Follow-up candidates (Medium and minor; none triggers a revision and none fails the review)

These are the R2 follow-ups, carried by reference, plus one new Medium. R2's F1-F6 were not re-verified line by line in this review (they are not prior blocking findings and `origin=unchanged` per the empty diff elsewhere), and the single changed line does not touch them; each is still open:

- F1 (Medium, R2, `spec:182` vs `spec:194`): AC-0.4 steps 1-3 in P0 need a contract path that does not exist yet; `spec:194` shows the intent ("the contract arrives in P1"). Suggest: step 3 "in P0, the command's existing report file".
- F2 (Medium, new in wording, `spec:196` with `spec:159`): "each P1 command" is ambiguous between the nine commands in the Commands cell and the three commands that only get fixes (adversarial, cleanup-audit, index-repo). The wrong outcome needs a guess about which reading an implementer picks, so it is Medium. Inherited from the unchanged `spec:159` wording; the changed line `spec:196` does not worsen it.
- R2 F2 (Medium, `spec:62`): cleanup-audit (`.claude-audit/`, no output flag) and index-repo have no coordinator-passed `<output-dir>` for the WC-4 default.
- R2 F3 (Medium, `spec:62`): file-valued `--output` puts the contract in the file's directory, so two workers writing files into one directory collide (WC-11, `spec:69`, covers default paths only).
- R2 F4 (Medium, `spec:159` vs `spec:154`): P1 gives the flag and section to commands whose gates and contracts arrive in P2-P4; "a no-op where a command has no gate" leaves gated commands unspecified.
- R2 F5 (minor, `spec:149`): SA-4 still lists "adversarial and workflow contract gaps" although the workflow row now says "None" (`spec:92`).
- R2 F6 (minor, `spec:62`): a workflow pre-creation STOP writes no contract, so a blocked question there goes only in the `worker_done` body; workflow has no stated gate (INV-B:267-275), so no wrong outcome follows.

Medium and minor findings never trigger a revision. The session that ran this review asks the user once per loop whether to open an issue for them and creates none without the user's answer; this run asked nothing and created nothing (no user channel in this sandbox).

## Coverage

Covered: the single changed line (`spec:196`), prior blocking finding N1, and the dependencies of the changed line (`spec:94`, `112`, `159`, `167`, `182-183`, `195`, `265`). Coverage line: `scoped PASS: changed lines + prior blockers`. Not covered: the unchanged remainder of the document (whole-document assurance needs a separate, labelled first review whose blockers are escalated and never start a fourth review); the `src/`, `sk/` and `cmd/` files, which are UNVERIFIED in this sandbox. The brief did not widen scope and did not grade a minor finding as blocking, so no brief clause was overridden. No Reviser brief is written: there is no open blocking finding, and at `review: 3` the run would escalate rather than revise.

verdict: PASS
