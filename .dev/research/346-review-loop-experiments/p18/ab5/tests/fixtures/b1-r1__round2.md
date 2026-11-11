review: 2 of 3
> verification (coordinator, VERIFY step VF2; verifier reply .dev/orca-command-refactor/review/verify-2.md): confirmed blocking ids: R2-1. Rejected, kept as noted, unactioned and not prior blocking findings for the next re-review: none. The Reviser brief below is narrowed to the confirmed ids.

# Re-review (critique mode, focus requirements,architecture)

- candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 4608dec8f5f47699675938e131fc3f4f5f3fbb7915dd6eb492ed6df1a5933d83
- baseline: .dev/orca-command-refactor/specs/history/spec-v1.md sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d
- prior: .dev/orca-command-refactor/review/round1.md sha256 98e676f52cf0f7e37acc29a60a57662c4a52425fbc14470839b64afa55a7adb6 (header `review: 1 of 3`, `verdict: FAIL`)
- reviewer model: claude-sonnet-5-5
- baseline: present. Review loop prompt file read in full: home/.claude/rules/prompts/document_review_loop_prompts.md (RE-REVIEW prompt followed).
- `.claude/agents/rf-qa.md` and `~/.claude/agents/rf-qa.md` do not exist in the sandbox (home/.claude holds only rules/), so the rf-qa Fix Cycle steps 1-5 could not be read; the Review Loop section 5 rules were applied standing alone.
- Citation note: inventory citations (`INV-A`, `INV-B`, `CAPS`, `cmd/`, `sk/`) point to files outside the sandbox evidence set except the three inventory files; I did not re-check them and mark any I rely on UNVERIFIED. Line numbers below are candidate line numbers (the diff changes no line count, so they equal baseline line numbers).

## Step 1. Evidence block (`diff -w BASELINE CANDIDATE`, 11 hunks)

BEFORE (baseline, lines starting `<`), abbreviated to the changed passage only; the full lines are in the baseline at the same line numbers:
- 61 (WC-3): "When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once"
- 62 (WC-4): "the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)."
- 73: "the output directory, so the report path is known before dispatch (WC-4)"
- 76: "\"Contract\" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1)."
- 79: "the worker reports the named file until Phase 1 adds the contract."
- 83: "Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1)"
- 92: "Write the contract for pre-creation STOPs too (WC-4 \"every outcome\") (P1)"
- 95: "\"Blocked\" means the WC-2 (c) resolution: write the contract with `status: blocked` and the question, then stop."
- 148 (SA-3): "...or when the caller passes the new output flag."
- 154: "...Phase 4 waits for answers to D2-D4."
- 159 (P1): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 ... analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow"
- 182: "its report path is the WC-4 contract path."
- 195-197 (AC-1.1 to AC-1.3): "every command in sections 3.1-3.2 has a `## Unattended mode` section ..."; "`--unattended --output <dir>`"; "no `--unattended` and no new output flag"
- 200 (AC-2.2): "`/sc:tdd \"auth\" --unattended --output <file>` with a bare topic"
- 208 (AC-4.1): "`/sc:implement <plan> --unattended` on a plan with one acceptance criterion that cannot be met"

AFTER (candidate, lines starting `>`), the changed text at the same lines:
- 61 (WC-3): "When a gate would resolve as blocked, the worker session holds a preamble and the brief says `on a blocked gate: ask`, the session may instead ask the coordinator once ... Without that line the session sends no `ask` and follows WC-5."
- 62 (WC-4): "the command writes `<report-dir>/return-contract.yaml`, where `--report-dir <dir>` is a directory-valued flag the brief always passes. It is separate from `--output`, which may be a file (tdd, init-lite) or a directory, so the path never depends on a run-time id (workflow's package id included)." and "in unattended mode they also write it to `<report-dir>`, and a standalone run keeps today's location (SA-3)."
- 73: "the `--report-dir` directory, so the contract path is known before dispatch (WC-4); the blocked-gate line, `on a blocked gate: stop and report` (the default when absent) or `on a blocked gate: ask` (WC-3)"
- 76: "\"Contract\" means the WC-4 file `<report-dir>/return-contract.yaml`. Every changed command also gains the `--report-dir` flag and the `## Unattended mode` section (section 2.1), in the phase its row names; `load` gains neither."
- 79: "...until its phase adds the contract (P1: adversarial, brainstorm, cleanup-audit, index-repo, init-lite, workflow; P2: reflect, release-split, tdd, troubleshoot). Every brief also passes `--unattended --report-dir <dir>` (WC-4, section 2.3)."
- 83: "Name the contract location: `<report-dir>/return-contract.yaml` in unattended mode, today's place standalone (P1)"
- 92: "...to `<report-dir>` so a STOP with no id has a location (P1)"
- 95: "...then stop. Every brief also passes `--report-dir <dir>` (WC-4)."
- 148 (SA-3): "...or when the caller passes `--report-dir` or the new output flag."
- 154: "Each command gains its flags and section only in the phase its row names, so P1 does not touch implement, post-release or pr-submit."
- 159 (P1): "the `--unattended` and `--report-dir` flags and the `## Unattended mode` section for the commands in this row's Commands cell, `load` excepted ... analyze, build, business-panel, design, document, explain, index, test, brainstorm, init-lite, adversarial, cleanup-audit, index-repo, workflow; load (usage line only, no section)"
- 182: "its report path is `<report-dir>/return-contract.yaml` (WC-4)."
- 195-197: "every command in the section 6 P1 Commands cell except `load` has a `## Unattended mode` section ... and that no section-4 command and not `load` has one"; "`--unattended --report-dir <dir>` (plus `--output` where section 3 requires it)"; "no `--unattended`, no `--report-dir` and no new output flag"
- 200 (AC-2.2): "`/sc:tdd \"auth\" --unattended --output <file> --report-dir <dir>` with a bare topic and the brief line `on a blocked gate: stop and report`, as in every AC-2.2 run"
- 208 (AC-4.1): "`/sc:implement <plan> --unattended` with the brief line `on a blocked gate: stop and report`, on a plan ..."

Self-check: every AFTER line (17) found once by `grep -cF` in the candidate and every BEFORE line (17) found once in the baseline. Roles are not swapped.

## Prior blocking findings (from round1.md)

| id | status | basis (AFTER text only) |
|---|---|---|
| M1 | resolved | WC-4 (62) now fixes one location, `<report-dir>/return-contract.yaml`, from a directory-valued flag separate from file-valued `--output`. The adversarial row (83) and workflow row (92) cite the same path, workflow's pre-creation STOP gets a location (92), and acceptance step 3 (182) compares against the same path. The three formerly incompatible definitions no longer exist. |
| M2 | resolved | P1 Commands cell (159) now lists exactly the commands that P1 touches, `load` excepted; AC-1.1 (195) tests that cell, not "every command in 3.1-3.2"; 154 states implement, post-release and pr-submit are not touched in P1, consistent with P4 (162) and D3. Cross-check: the P1 cell's 14 commands equal the 3.1 rows marked P1 (83, 84, 85, 86, 87, 92 = adversarial, brainstorm, cleanup-audit, index-repo, init-lite, workflow) plus the 3.2 rows marked P1 (analyze, build, business-panel, design, document, explain, index, test); `load` is in the cell as "usage line only, no section". |
| M3 | resolved | Same edit as M2; AC-1.1 excludes `load` and asserts `load` has no section, matching the `load` row (112) and the decision "a report file would be an unrequested addition". The init-lite sub-note is also closed: init-lite is now an explicit member of the P1 cell and 79 says its section arrives in P1. |
| M4 | resolved | WC-3 (61) now makes `ask` conditional on the brief line `on a blocked gate: ask`; without it the session follows WC-5. Section 2.3 (73) makes the brief carry the line, defaulting to stop and report. AC-2.2 (200) and AC-4.1 (208) name the stop-and-report line. A worker that follows WC-3 on the AC-2.2 input sends `worker_done --outcome failed`. |
| M5 | resolved | `--report-dir` is directory-valued and separate from file-valued `--output` (62); tdd (90) and init-lite (87) keep `--output <file>`, spec-panel (120) adds `--output`, and the contract goes to `<report-dir>`; AC-2.2 (200) passes both flags, and step 4 (183) tests `<contract>` at that path. |

No finding was deferred or withdrawn by the reviser.

## Findings on changed lines

### R2-1. CRITICAL by consequence, BLOCKING, origin=changed. Line 79 says every 3.1 brief passes `--unattended --report-dir`, but P0 runs three 3.1 commands before those flags exist
- Experts: Wiegers (consistency of requirements), Fowler (phase boundary), Adzic (the AC-0.4 example).
- Texts: line 79 (changed): "Every brief also passes `--unattended --report-dir <dir>` (WC-4, section 2.3)." under "### 3.1 Ready today (10)", whose same paragraph says "the worker reports the named file until its phase adds the contract (P1: ...; P2: reflect, release-split, tdd, troubleshoot)". Line 62 (changed) also says the brief "always" passes `--report-dir`. Against it: line 158 (P0, "no command edits"; smoke runs `/sc:troubleshoot` (no `--fix`), `/sc:workflow --handoff none`, `/sc:adversarial --output <dir>`) and line 192 (AC-0.4), which runs those three commands with no `--unattended` and no `--report-dir`, and passes at "step 4 uses the command's existing report file, since the contract arrives in P1". Line 91: troubleshoot's `--unattended` handling is a P2 change; line 159 and 154 add `--report-dir` only in the phase a row names.
- Wrong outcome: An implementer who follows the stated text as written builds a P0 coordinator brief for the smoke runs that includes `--unattended --report-dir <dir>` on commands that, per line 158 ("no command edits") and line 154, do not yet accept either flag (troubleshoot not before P2), so the brief hands each command an unknown flag whose behaviour the spec does not define; an implementer who follows AC-0.4 as written omits both flags and so breaks the "every brief" rule of 79 and 62. The text cannot be followed both ways, and AC-0.4 cannot pass under line 79 without the P0 edits that line 158 forbids. The same contradiction applies to every 3.1 command between P0 and its phase (P2 commands troubleshoot, reflect, release-split, tdd are not edited until P2).
- This is introduced by the revision: the baseline sentence (79 before) said "if the brief uses the stated flags" and had no universal `--unattended --report-dir` rule.
- Recommendation: narrow 79 and the "always" in 62 to "from the phase that adds them (the Phase column of each row); a brief before that phase omits them and the worker reports the row's 'Report today' file". Delete rather than add.
- Priority: High.

## Medium findings (warnings, not blocking; listed under follow-up candidates)

- R2-M1, origin=unchanged, depends on changed line 61 (WC-3): line 114 (pr-submit row, unchanged) says "operator HALTs resolve as blocked (the worker may use `ask` or `escalation`)", while WC-3 now says "Without that line the session sends no `ask`". "May" is permissive and pr-submit is P4 behind D3 (240, "no pr-submit changes in Phase 4" as recommended), so a wrong build needs the implementer to pick the worse reading. Also line 235 (D2 option b) has the coordinator answering a worker's `ask`, which now presupposes the `on a blocked gate: ask` line.
- R2-M2, origin=unchanged, depends on changed WC-4: 7.2 step 6 (line 184) passes only if "only files under the brief's output directory (and the command's documented artifacts)" appear, but the contract now sits in `<report-dir>`, which WC-4 says is separate from `--output`. Whether `<report-dir>` is inside the "output directory" is unstated; a guess that it is outside makes step 6 fail on a correct run. Fix by naming `<report-dir>` in step 6.
- R2-M3, origin=changed: 3.2 rows for analyze, build, design, index, test and similar (rows 97-129) say "add a report path/output path; contract" while WC-4 now fixes the contract at `<report-dir>`; the rows still read as if the contract location follows the new output path. Line 76 ("Contract" means the `<report-dir>` file) covers it, so this is a clarity note only.
- R2-M4, origin=changed: `.claude`/command definition note. `/sc:spec-panel` as defined in command.md:460-461 already has `--report-dir` and `--output` (file-valued), while the spec row (120) says "add `--output`" and cites INV-B:177-185 (it had no output flag at inventory time). Not checked against evidence inside the sandbox beyond the inventory; the flag-name collision may be a duplicate addition. UNVERIFIED against the live repo.

## Minor notes (origin=unchanged unless stated)

- Line 195 AC-1.1 parses "the section 6 P1 Commands cell" including the parenthetical "load (usage line only, no section)"; the test must exclude the `load` token by name. A note, not a defect.
- Section 3.1 line 79 wording "P1: ... init-lite" makes init-lite, whose "Small fix" is "None" (87), a P1 member only for the flags and section; consistent with 159.

## Coverage

Covered: the 11 changed hunks (WC-3, WC-4, 2.3 brief, 3 intros, adversarial and workflow rows, SA-3, phase text, P1 row, 7.2 step 3, AC-1.1 to AC-1.3, AC-2.2, AC-4.1), the P0 row and AC-0.4 that depend on them, the 3.1 and 3.2 P1 membership cross-check, and the five prior blocking findings. Guard Condition Boundary Table: in a re-review it covers guards on changed lines only. The one changed guard is the WC-3 `ask` condition (brief line present / absent / both lines present). Present: stop-and-report or WC-5 (OK). Absent: default stop and report (OK, 73). Both lines present: unspecified (GAP, Medium, not blocking; no implementer gets a concrete wrong outcome without a guess). Not covered: unchanged sections 1, 4, 5, 8 beyond the lines above; inventory-line citations (`INV-*`, `CAPS:*`, `cmd/`, `sk/`) are UNVERIFIED here. This is a scoped review (changed lines plus prior blockers), not whole-document assurance.

## Follow-up candidates (Medium and minor; not in the Reviser brief)

R2-M1, R2-M2, R2-M3, R2-M4, and the two minor notes above. The session that ran the review asks the user once whether to open an issue for them; none is created here.

## Reviser brief

Blocking finding ids: R2-1.
Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names (lines 62 and 79); add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Leave Medium and minor findings alone.

verdict: FAIL
