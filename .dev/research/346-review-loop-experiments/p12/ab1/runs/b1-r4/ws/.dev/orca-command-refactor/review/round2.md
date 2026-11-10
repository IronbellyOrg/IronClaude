review: 2 of 3

# Re-review 2 (critique mode, focus requirements,architecture)

- candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 ecccef2cd605be2429bee0a2ca58d7ed10decc68e84a2d03445f68dc64843d1c (58352 bytes)
- baseline: .dev/orca-command-refactor/specs/history/spec-v1.md sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d (57763 bytes). This hash equals the candidate hash recorded in the prior report (round1.md:5), so the baseline is the text round 1 reviewed.
- prior: .dev/orca-command-refactor/review/round1.md sha256 7e64c67802ad3c06e7ab423b74a818febc81b7badfa1769befe83efdce83d499 (header `review: 1 of 3`, round1.md:1; N = 1 + 1 = 2)
- reviewer model: claude-sonnet-5-5 (Sonnet 5.5)
- binding context read: .dev/orca-command-refactor/README.md. Review-loop prompt read in full: ~/.claude/rules/prompts/document_review_loop_prompts.md (RE-REVIEW prompt followed). The re-check follows the Fix Cycle steps of `rf-qa.md`, which is not in the sandbox (UNVERIFIED); the rules of the command's Review Loop section were applied on their own.
- Inventories (`inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`) were not re-read. Every inventory or `cmd/`/`sk/` citation below is carried from the spec and is UNVERIFIED here; only spec-internal consistency was checked.
- Brief clauses overridden: none.

## Step 1: evidence block

Roles: CANDIDATE = specs/orca-worker-contract-spec.md; BASELINE = specs/history/spec-v1.md; PRIOR = review/round1.md. Command run: `diff -w BASELINE CANDIDATE`. It prints five changed spans, at lines 62, 76, 159, 194 and 195 (the same line numbers on both sides). Every other line is identical ignoring whitespace.

BEFORE (baseline), verbatim from the diff:

```
< WC-4 row, line 62: "...where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern ..."
< line 76: "...Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6."
< line 159 (P1 Scope cell): "The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands."
< line 194 (AC-0.4 pass cell): "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1"
< line 195 (AC-1.1): "...the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one"
```

AFTER (candidate), verbatim from the diff, shortened to the changed words:

```
> line 62 (WC-4): "...(`--output` / `--output-dir`); when `--output` is a file, `<output-dir>` is that file's parent directory; a command with a fixed output location writes the contract there, and adversarial uses `<output>/adversarial/` (section 3.1) (M3). ..."
> line 76: "Every changed command except `/sc:load` also gains the `## Unattended mode` section (section 2.1), in the phase of its own row (M1, M4, M5)."
> line 159 (P1 Scope): "The WC-4 contract in unattended mode; the `--unattended` flag and section on the commands listed in this row plus brainstorm and init-lite (no gate, a no-op), and on no other command yet (M4, M5); `/sc:load` gets neither (M1); output flags for commands that lack one; the small fixes to ready commands."
> line 194 (AC-0.4): "steps 1-2 and 5-7 pass; in steps 3 and 4 the command's existing report file stands in for the contract, since the contract arrives in P1: step 3 compares `--outcome` with that report's result under WC-5 and takes that file as the report path, and step 4 is only `test -s` on it (M2). Record the results ..."
> line 195 (AC-1.1): "...the test asserts that every command in the P1 scope (section 6, P1 row) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that `/sc:load`, every P2-P4 command and every section-4 command has none (M1, M4, M5)"
```

Self-check (run before the verdict): each AFTER line, with its `>` removed, was found by `grep -nF` in the candidate at its own line (62, 76, 159, 194, 195), and each BEFORE line, with its `<` removed, was found by `grep -nF` in the baseline at the same five line numbers. No role swap. The candidate hash matches the hash of the file read.

Net change: +589 bytes (57763 to 58352), which agrees with the figure in review/revise1.md. This is the revise report's own claim, not independently verified beyond the two `wc -c` values taken here.

## Prior blocking findings: table

| id | prior defect (round1.md) | status | AFTER text compared | reason |
|---|---|---|---|---|
| M1 | AC-1.1 required a contract-naming section on `/sc:load` (spec:112, 265 say no report) | resolved | candidate:76, 159, 195 | AC-1.1 now says `/sc:load` has none (195). The P1 Scope cell says "`/sc:load` gets neither" (159). Line 76 says "except `/sc:load`". These agree with the load row ("none (see note)", "P1 (usage line only)", candidate:112) and with the Decision at candidate:265. The contradiction is gone. A residual wording issue is under follow-up candidate F1. |
| M2 | AC-0.4 step 3 could not pass in P0 (no contract, no `status`) | resolved | candidate:194 | Step 3 now compares `--outcome` with the existing report's result and takes that file as the report path. The relaxation now covers steps 3 and 4. The 7.2 text (candidate:182-183) is unchanged, so P1-P4 still use the contract. The step 3 stand-in is still loose for troubleshoot and adversarial (follow-up candidate F2). |
| M3 | WC-4 gave no contract path when `--output` is a file; adversarial's sub-directory was an unstated exception | resolved | candidate:62 | Rule: a file-valued `--output` means the file's parent directory; a fixed output location holds the contract; adversarial's exception is named (`<output>/adversarial/`) and matches the adversarial row (candidate:83). `test -s <contract>` in 7.2 step 4 now has a path to test for tdd and init-lite (candidate:87, 90, 200). New side effects are follow-up candidate F3. |
| M4 | P1 made `--unattended` accepted by commands whose gates convert in P2 or P4 | resolved | candidate:76, 159, 195 | Flag and section now arrive in each command's own phase. P1 covers only the P1 row plus brainstorm and init-lite. AC-1.1 asserts that P2-P4 commands have none. `/sc:auggie-review <PR> --unattended`, `/sc:post-release --unattended`, and the pr-submit and implement variants no longer exist before their gates are converted (candidate:100, 160, 162). |
| M5 | AC-1.1 contradicted D3(a), the P4 deferral and "Phases 1-3 need no user decision" | resolved | candidate:159, 195 | pr-submit, implement and post-release are P4 rows (candidate:109, 113, 114, 162), and AC-1.1 requires them to have no section after P1. D3(a) ("no pr-submit changes in Phase 4", candidate:240) and "Phases 1-3 need no user decision" (candidate:154) no longer conflict with a P1 check. |

No finding regressed. The round1.md header lists M5 under a "follow-up candidates" heading (round1.md:130), but round1.md:158 and :12 list it as confirmed and blocking. I treated it as blocking.

## Findings on changed lines (new)

All five changed spans were checked against the spans that depend on them. No finding names a concrete wrong outcome an implementer would build from the stated text with no further assumption. The items below are Medium or minor and go under follow-up candidates.

## === REQUIREMENTS ANALYSIS ===

Experts: Wiegers (traceability), Adzic (testability), Cockburn (actor).

- F1 (Medium, origin=changed; Wiegers / Adzic): AC-1.1 at candidate:195 tests "every command in the P1 scope (section 6, P1 row)", and the P1 row's Commands cell (candidate:159) lists `load (usage line only)`. Read literally, `/sc:load` is both in the scope of the first assertion and the subject of the second ("`/sc:load` ... has none"). The same row's Scope cell (candidate:159) says "`/sc:load` gets neither", so the intent is clear. Graded Medium, not blocking, because the same row settles the reading with no guess about which text wins. Likewise, `AC-1.2` ("each P1 command", candidate:196, unchanged line, depends on the changed row at 159) could be read to include `/sc:load`, which has no contract (candidate:112), so its 7.2 step 4 would fail. Suggested narrowing: write "every P1 command except `/sc:load`" in AC-1.1 and AC-1.2. Priority Low.
- F2 (Medium, origin=changed; Adzic): AC-0.4 step 3 (candidate:194) says "compares `--outcome` with that report's result under WC-5". WC-5 maps a contract `status` to an outcome (candidate:63). `REPORT.md` (troubleshoot, candidate:91) has no defined status field, and adversarial's contract filename is "not fixed" until P1 (candidate:83). The P0 pass condition therefore relies on the worker's judgment of what "result" means. The P0 gate (candidate:194) is still passable by reading the report, so this is not a wrong build. Suggested narrowing: say "the worker states in the phase report which result it compared". Priority Low.
- F6 (minor, origin=unchanged; note): AC-0.4 says "the contract arrives in P1" for all three smoke commands. Under the M4 scoping, troubleshoot's section and flag arrive in P2 (candidate:91, 160). The stand-in rule still holds, so this is only a wrong phase number in a rationale. Also candidate:79 ("until Phase 1 adds the contract") has the same imprecision for reflect, release-split and tdd (P2). Cites the changed lines 76 and 159.

## === ARCHITECTURE ANALYSIS ===

Experts: Fowler (boundary), Newman (interface evolution), Hohpe (hand-off), Nygard (failure modes).

No blocking architecture finding. The M3 rule keeps the single hand-off (one contract file the worker names in `--report-path`, WC-4 at candidate:62) and adds no flag, mechanism or section. The M4 scoping makes `--unattended` additive per phase, which fits SA-4 (candidate:149). The core decision (commands stay units of work, Orca coordinates) is unchanged and is not touched by the diff.

- F3 (Medium, origin=changed; Fowler / Nygard): the "file's parent directory" rule at candidate:62 puts `return-contract.yaml` beside the deliverable. Two workers whose `--output` files share a parent directory (for example two `/sc:tdd ... --output .dev/x/a.md` and `.dev/x/b.md`) write the same `.dev/x/return-contract.yaml`, and a bare `--output a.md` puts it in the repository root. Concrete attack (Whittaker, Divergence Attack on candidate:62): before, no contract; worker A writes it, worker B overwrites it, and A's coordinator reads B's status. The spec has a one-run-per-directory idea for cleanup-audit (WC-11, candidate:85) but does not state one for file-valued `--output`. Graded Medium: it needs a coordinator that reuses a directory, which the spec does not require or forbid. Suggested narrowing: add one sentence that parallel workers use distinct `--output` parents (no new mechanism). Priority Medium.
- F4 (minor, origin=changed; Newman): AC-1.1's negative assertion "every P2-P4 command has none" (candidate:195) is true at the end of P1 only. `test_worker_contract.py` is one persistent file (candidate:158, 199) and AC-2.1 adds assertions to it, so the P1 negative assertion must be dropped or phase-gated when P2 lands. The spec does not say so. A note, not a wrong outcome from the stated text.
- F5 (minor, origin=unchanged; Hohpe): the spec-panel row says "add `--output`" (candidate:120) with no statement of whether it is a file or a directory. The M3 rule now yields a defined contract path in either case, so the round 1 concern is covered. The sandbox `command.md:22-23,460` already defines `--output <file>`, `--report-dir` and an `--unattended` section for spec-panel. The spec cites `cmd/spec-panel.md:22,34-35,222,451,455` (UNVERIFIED, file not in the sandbox), so the row may describe an older command text.

## === ADVERSARIAL ANALYSIS (Whittaker) ===

Only changed lines were attacked (re-review scope).

- Divergence Attack on candidate:62 (file versus directory): `--output .dev/x/auth-tdd.md` now gives `<output-dir>` = `.dev/x/`, so `test -s .dev/x/return-contract.yaml` has a defined target. Holds. Collision case = F3 (Medium).
- Sequence Attack on candidate:159 versus 160-162 (phase order): run P1 then check the P2-P4 commands. The flag and section are absent on auggie-review, task, post-release, pr-submit and implement, so the P1 outward-action path described in M4 cannot occur. Holds.
- Sentinel Collision Attack on candidate:62 (`status` vocabulary versus a command's own `status` values): carried from round 1 as minor and not worsened by the diff. UNVERIFIED (the workflow contract reference is not in the sandbox).
- Zero/Empty Attack on candidate:62 (no `--output` for post-release): still a Medium follow-up from round 1 (M3 in the round 1 numbering of follow-ups), not changed by the diff.
- Accumulation and other attacks: none found that name a concrete wrong outcome.

## === GUARD CONDITION BOUNDARY TABLE === (guards on changed lines only)

Guards on changed lines: G-A (WC-4 `--output` is a file versus a directory, candidate:62), G-B (P1 flag scope, candidate:159), G-C (AC-0.4 stand-in for steps 3 and 4, candidate:194). Classes left out: Sentinel and Maximum/Overflow for G-A, G-B, G-C cannot occur (presence or enum tests, no numeric threshold or reserved value).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G-A `--output` file or dir | candidate:62 | Zero/Empty | no `--output` | false | fixed-location commands write there; post-release "else blocked" (candidate:113), where its blocked contract goes is unstated | OK for fixed-location commands; GAP (Medium, carried from round 1) for post-release |
| G-A | candidate:62 | One/Minimal | `--output a.md` (bare file) | file | contract in the file's parent directory (current directory) | OK |
| G-A | candidate:62 | Typical | `--output <dir>` | directory | `<dir>/return-contract.yaml` | OK |
| G-A | candidate:62 | Legitimate Edge Case | two file outputs share a parent | file | same contract path for both | GAP (Medium, F3) |
| G-B P1 flag scope | candidate:159 | Typical | analyze, build, brainstorm, init-lite | in scope | flag and section added | OK |
| G-B | candidate:159, 195 | Legitimate Edge Case | `/sc:load`, a P1 command by the Commands cell | excluded by name | "gets neither" | OK (wording note F1, Medium) |
| G-B | candidate:159, 160-162 | Legitimate Edge Case | any P2-P4 command | out of scope | flag and section absent until its phase | OK |
| G-C AC-0.4 stand-in | candidate:194 | Typical | troubleshoot `REPORT.md` | stand-in | `--outcome` compared with "that report's result" | GAP (Medium, F2) |
| G-C | candidate:194 | Legitimate Edge Case | adversarial contract name not fixed (candidate:83) | stand-in | "that file" is whichever contract the run wrote | GAP (Medium, F2) |

Table complete (FR-10): every guard on a changed line is enumerated, every cell is filled, omitted classes carry their reason. The GAP rows are all Medium under FR-8 and FR-9 because none names a concrete wrong outcome an implementer would produce from the stated text with no further assumption, and none is a security, data-loss or safety-boundary risk. Pipeline Dimensional Analysis: not triggered. `--focus correctness` is not active.

## Follow-up candidates (Medium and minor; never trigger a revision)

Medium: F1 (AC-1.1/AC-1.2 wording for `/sc:load`), F2 (AC-0.4 stand-in for troubleshoot and adversarial), F3 (contract collision when file outputs share a parent directory). Carried from round 1 and untouched: the sources listed at round1.md:154 (round1-a.md, round1-b.md, round1-c.md).
Minor: F4 (the P1 negative assertions are phase-bound), F5 (spec-panel row versus the sandbox command text, UNVERIFIED), F6 (phase number in the "arrives in P1" rationale).

The session that ran this review would ask the user once whether to open an issue for these. No answer is available in this sandbox, so none is asked and none is created.

## Coverage

scoped PASS: changed lines + prior blockers

Covered: the five diff spans (candidate:62, 76, 159, 194, 195); the five prior blocking findings M1-M5; the spans that depend on them (candidate:79, 83, 87, 90, 91, 100, 109, 112-114, 149, 154, 158, 160-162, 196, 199, 240, 265); a grep of the candidate for "every command", "no-op" and "accepted by", which found no remaining unscoped "every command" claim about the flag. Not covered: unchanged text of the candidate and all inventory and source citations (UNVERIFIED here); whole-document assurance needs a separate, labelled first review.

## Reviser brief

None. No blocking finding is open, so no revision is requested and none may be made for F1-F6.

verdict: PASS
