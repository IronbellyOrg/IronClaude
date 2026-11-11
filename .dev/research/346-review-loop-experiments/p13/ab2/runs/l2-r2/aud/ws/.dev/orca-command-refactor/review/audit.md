review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- label: whole-document audit of the final spec, a first review of the whole document (FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md`, read in full)
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `0686b734a23ad02747840178fa995a98e02d1dad4e7ef5e12322d1cb7ce8879d`
- baseline: not given, not needed for a first review. No `--re-review`.
- reviewer model: claude-sonnet-5-5
- binding context read first: `.dev/orca-command-refactor/README.md` (38 lines)

Citation notation: `spec:N` is a line of the candidate. `INV-A:N`, `INV-B:N` and `CAPS:N` are lines of `inventory/commands-a.md`, `commands-b.md` and `orca-capabilities.md`. The candidate uses the same keys. Only the README and the three inventories exist in the workspace, so any citation to `src/`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `EVIDENCE.md`, `~/.claude/...` or Orca guide text is UNVERIFIED by me unless an inventory line quotes it.

## Coverage

- Read all 285 lines of the candidate.
- Cross-checked its inventory citations against the inventories:
  - The 43-command split (10 ready, 27 needs-change, 6 coordinator-only) holds. INV-A:73 gives 5/13/3 and INV-B:278 gives 5/14/3.
  - The ready set, the 27 section 3.2 rows, the phase assignments in section 6 and the six section 4 commands are mutually consistent.
  - The `INV-A:N`, `INV-B:N` and `CAPS:N` lines cited for E1-E6, R1-R5, WC-1..WC-12 and the UNVERIFIED list match their cited content.
- Not checkable here (UNVERIFIED): every `cmd/`, `sk/`, `src/superclaude/cli/install_core.py`, `CLAUDE.md`, `Makefile`, `pyproject.toml` and `EVIDENCE.md` line. The candidate says it re-read 11 of them and got a fresh-context check on about 340 (`spec:11`, `spec:285`). I did not re-verify that.
- Experts applied, per focus plus the always-on adversarial expert: Wiegers, Adzic, Cockburn (requirements); Fowler, Newman, Hohpe, Nygard (architecture); Whittaker.
- Not triggered:
  - Pipeline Dimensional Analysis: no multi-stage data pipeline with count divergence.
  - State Variable Registry: it needs `--focus correctness`.

## Findings (critique mode)

Grading follows the Grading check in the FIRST-REVIEW prompt. No finding below holds as a wrong outcome without an extra assumption, a guess between two readings, or a requirement the document never states. All findings are therefore Medium or minor and none is blocking.

=== REQUIREMENTS ANALYSIS ===

**A-01 (Medium, MAJOR label, Wiegers/Whittaker, priority High).** `--unattended` is required on every worker line, but six ready commands never get the flag.
- Texts:
  - `spec:73`: the brief carries "the exact command line including `--unattended`".
  - D1(a), `spec:228`: "The coordinator writes it into every worker's command line".
  - `spec:195-196`: AC-1.1 and AC-1.2 test only the P1 row.
- Commands affected: adversarial, brainstorm, cleanup-audit, index-repo, init-lite and workflow.
- Why: `spec:79-92` says these run as workers with only the listed flags (none lists `--unattended`), and no phase in `spec:158-162` adds `--unattended` or an `## Unattended mode` section to them. P1 adds only "fixes" for adversarial, cleanup-audit, index-repo and workflow; brainstorm and init-lite appear in no phase.
- Wrong outcome: a brief template that always appends `--unattended` passes a flag the command never defines. Whether that is ignored, taken as topic text or rejected is not stated.
- Why Medium: it needs a guess about how an undefined flag is handled.
- Recommendation: state that the flag is added only for commands whose section 3 row gives them the mode. Alternatively, add the six commands to a phase.
- Quality impact: removes a brief-template ambiguity.

**A-02 (Medium, Wiegers/Cockburn, priority High).** The report path "known before dispatch" (WC-4) is underdetermined for commands whose `--output` is a file.
- Texts:
  - `spec:62` puts `<output-dir>/return-contract.yaml` in the directory the coordinator passed.
  - `spec:73` has the coordinator pass "the output directory".
  - Rows give a file-valued `--output` for tdd (`spec:90`), init-lite (`spec:87`) and spec-panel (`spec:120`).
- Defect: no directory flag exists for those commands, so the contract path cannot be derived from the brief.
- Related conflict: WC-6 (`spec:64`) says commands without a resume flag "write each run into a fresh output directory", and many rows say "fresh dir". If the command creates that directory, the contract moves and WC-4 breaks. If the coordinator must pass a new directory per retry, `spec:73` never says so.
- Why Medium: two readings exist, and the worse one needs a guess.
- Recommendation: add one sentence on where the contract goes for a file-valued `--output`. Say who supplies the fresh directory on `--retry-of`.

**A-03 (Medium, Wiegers, priority Medium).** "Keep their fields" conflicts with a fixed four-value `status`.
- Texts: `spec:62` ("Commands that already write a contract keep their fields and add the missing ones") against the closed set `succeeded|partial|failed|blocked` (`spec:62`, `spec:262`), enforced by the check at `spec:183`.
- Defect: the existing status vocabularies of workflow, brainstorm, reflect and adversarial were not recorded. INV-B:272 shows only that workflow's contract carries `status` and `failed`. Which side wins is UNVERIFIED.
- Recommendation: record each existing status vocabulary. State the mapping or the winner.

**A-04 (Medium, Adzic, priority Medium).** AC-2.2 contradicts the permitted WC-3 path.
- Texts: WC-3 (`spec:61`) lets a worker with a preamble `ask` the coordinator and resume. AC-2.2 (`spec:200`) passes only on `worker_done --outcome failed` with `status: blocked`.
- Defect: a worker that follows WC-3 would fail a test written under WC-2(c).
- Why Medium: both readings are allowed.
- Recommendation: have the gate-trigger test brief forbid `ask`, or accept either path.

**A-05 (Medium, Whittaker/Adzic, priority Medium).** `spec:184` (7.2 step 5) searches the transcript for the string `AskUserQuestion`, but the pass condition is "no `AskUserQuestion` call".
- Defect: command and skill text read into the transcript, including allowed-tools lists, contains the string, so a text search gives false failures.
- Recommendation: say "tool call", not "string".

**A-06 (Medium, Wiegers, priority Medium).** WC-11 (`spec:69`: "Two workers in one worktree must never write the same file") is not met by several rows.
- index-repo: row `spec:86` fixes only the location statement, and its report is a fixed `PROJECT_INDEX.md` (INV-A:53).
- cleanup-audit: row `spec:85` notes the fixed `.claude-audit/` and gives no fix.
- init-lite: row `spec:87` says "None", and the default report is a single fixed file (INV-A:55).
- Recommendation: narrow WC-11 to say these are single-owner per worktree and the coordinator serializes them. Alternatively, require a brief-supplied path.

**A-07 (Medium, Fowler/Nygard, priority Medium).** The tasklist row departs from its inventory without a decision.
- Texts:
  - Inventory recommendation: drop `--remediate` at Stage 10.5 (INV-B:46, INV-B:295).
  - Spec (`spec:122`): pass `--unattended` to each reflect "so the headless rule applies".
- Why this is unsettled: the spec never says what that rule does. The inventory notes only that headless keys on `claude --print` (INV-B:310), and the spec's own UNVERIFIED item 9 (`spec:280`) assumes an Orca worker is not headless.
- Also unsettled: the claim that the reflect fan-out is "inside Claude Code's nesting limit" (`spec:122`) is stated as fact. INV-B:46 and INV-B:314 mark it UNVERIFIED.
- Recommendation: state whether the rule auto-accepts or declines remediation. Add the departure to the `## Decisions` table. Add an acceptance check for tasklist.

=== ARCHITECTURE ANALYSIS ===

**A-08 (Medium, Fowler/Newman, priority Medium).** AC-C1 (`spec:172`) scans `src/superclaude/core` and requires empty output.
- P0 (`spec:158`) adds the contract file to `core/` and an Orca section to `HOW-WE-WORK.md`. SA-2 (`spec:147`) allows Orca mentions in the contract file.
- Defect: any `orca orchestration ...` text in those files fails the check.
- Recommendation: exclude the two files, or forbid command syntax there.

**A-09 (Medium, Fowler, priority Medium).** AC-C5 (`spec:176`) requires `grep '^-[^-]'` on the diff to print nothing.
- Defect: adding a flag to an existing Usage line necessarily removes a line.
- Recommendation: say new flags go on a new Usage line, or exempt Usage lines.

**A-10 (Medium, Hohpe, priority Low).** The plugin mirror is unresolved.
- Text: `spec:279` leaves it to each phase's plan, while AC-C2 and SA-5 check only `.claude/`.
- Defect: no acceptance check covers `plugins/superclaude/commands/`.
- Recommendation: add the check, or a P0 step that resolves the sync rule.

**A-11 (Medium, Cockburn, priority Low).** Undefined labels F-1 and F-2.
- Where: `spec:76`, `spec:154`, `spec:159`, `spec:195-196`.
- Defect: they appear without a definition in the document. The rule they cover is restated inline, so no behavior is lost.
- Recommendation: replace the labels with the rule text.

## Minor notes

- `spec:159` titles P1 "no gate", yet business-panel, explain, test and index carry refusal or pin rows (`spec:102,108,111,123`).
- `spec:16` says changes are "limited to" the contract. Section 3 also includes drift reconciliation, the load usage line and the business-panel frontmatter move. Non-goal 8 (`spec:220`) restricts scope to worker-blocking defects, which load and business-panel do not meet.
- `spec:285` (item 14) is a verification note, not an UNVERIFIED item.
- SA-1 (`spec:142,146`) says output paths do not change, while AC-3.1 reconciles validate-roadmap's report filename. SA-4 (`spec:149`) carves out the exception.

## Guard Condition Boundary Table

Guards enumerated from the spec: the WC-10 wait split (`spec:68`), the nesting depth (`spec:33`), the WC-5 outcome mapping (`spec:63`) and the WC-2 confidence/gate resolution (`spec:60`, `spec:121`). Classes that cannot occur for a guard are left out with one line.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| single blocking wait > 5 min | WC-10 `spec:68` | Zero/Empty | wait of 0 s | false | none needed | OK |
| single blocking wait > 5 min | WC-10 `spec:68` | Typical | 600 s | true | split into waits of at most 4 min | OK |
| single blocking wait > 5 min | WC-10 `spec:68` | Legitimate Edge Case | pr-submit poll + sleep iteration near 240 s; poll script runtime | undetermined | marked UNVERIFIED (`spec:114`, `spec:283`) | GAP (Medium: no wrong outcome stated) |
| nesting depth fence | R1/WC-8 `spec:33`, `spec:66` | Maximum/Overflow | worker calls `worker-start` | true | refused `nested_worker_depth_exceeded`; which call sites enforce is UNVERIFIED | GAP (Medium) |
| outcome mapping | WC-5 `spec:63` | Typical | status `partial` | n/a | `--outcome succeeded` | OK |
| outcome mapping | WC-5 `spec:63` | Sentinel Value Match | status `blocked` | n/a | `--outcome failed` | OK |
| outcome mapping | WC-5 `spec:63` | Zero/Empty | no report file | true | `--outcome failed` | OK |
| confidence gate < 0.70 | task row `spec:121` | Legitimate Edge Case | exactly 0.70 | false | not stated (gate says "below 0.70") | OK (inferable) |

Classes left out: One/Minimal for every guard (no count semantics). Sentinel and Maximum for the wait and confidence guards (no sentinel; the maximum is covered by the Typical row).

The table is complete. The two GAP rows are Medium and fall under the follow-up candidates below.

## Follow-up candidates

Medium: A-01 through A-11, including the two GAP rows above. Minor: the four notes above.
- Per the Review Loop, the session that ran the review asks the user once whether to open an issue for these. This worker created none, and nothing was asked of anyone from here.

## Overrides

No brief clause was overridden. The brief asked for the FIRST-REVIEW prompt, which is what was applied.

## Reviser brief

None. There are no blocking finding ids, so no revision is requested.

verdict: PASS
