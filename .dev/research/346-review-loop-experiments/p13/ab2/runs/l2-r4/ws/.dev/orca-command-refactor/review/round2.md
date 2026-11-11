review: 2 of 3

# Spec-panel re-review: orca-worker-contract-spec.md

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md`
- CANDIDATE: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `64ace65d5ab1437b097ef30b7325e413a6e90e0ea575952d431a0fa4c73ce23e` (matches `review/lint-2.md:1`)
- BASELINE: `.dev/orca-command-refactor/specs/history/spec-v1.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (equals the candidate hash recorded in `review/round1.md:6`, so the baseline is the text round 1 reviewed)
- PRIOR: `.dev/orca-command-refactor/review/round1.md`, sha256 `d4a2e4b82dae0425f55bc9811e5078ee40f947ef841afa947ab6c7b6ca0e2d1c`, header `review: 1 of 3`, final line `verdict: FAIL` (`round1.md:1,96`). So N = 2.
- Lint: `.dev/orca-command-refactor/review/lint-2.md`, sha256 `c17ee81ea0d25cef3f7fbf6c68b8f1cf0c8f97fec4e530fc6b8365c2ff5d6693`
- Reviser model used: claude-sonnet-5-5
- Prompt followed: RE-REVIEW prompt and re-review core, `~/.claude/rules/prompts/document_review_loop_prompts.md:35-49` (read in full), and the command's Review Loop bullets 1-7. The re-check of prior blockers also follows the Fix Cycle steps of `rf-qa.md`; that file is not present in the sandbox (UNVERIFIED), so the Review Loop bullet 5 rules stand alone, as that bullet allows.
- Coverage: scoped PASS: changed lines + prior blockers. I read README, round1.md, lint-2.md, revise1.md, spec lines 20-30 and 55-204, and checked the load citation `INV-B:65` (`inventory/commands-b.md:65`). Source-tree citations (`cmd/...`, `sk/...`, `CLAUDE.md:N`) are UNVERIFIED in this sandbox, as in round 1. This is not whole-document assurance.

## Step 1: evidence block (`diff -w BASELINE CANDIDATE`)

Four changed lines, 147, 159, 172, 195 (the diff is non-empty).

BEFORE (baseline), lines starting `<`:

```text
< | SA-2 | No command, skill or agent file runs an `orca` or `orca-ide` command, and none requires Orca to be installed or running. The only allowed mention of Orca in a changed command is as an example of a caller's question channel inside the contract file. | Commands run in other projects (`CLAUDE.md:74`); without Orca the calls fail with `runtime_unavailable` (`CAPS:147`). | `CAPS:145-149`; today's baseline: only `sk/ccsession-tag/` mentions Orca (section 1.2, E5) |
< | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
< | AC-C1 | `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core \| grep -v '^src/superclaude/skills/ccsession-tag/'` | prints nothing (SA-2, WC-8) |
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
```

AFTER (candidate), lines starting `>`:

```text
> | SA-2 | No command, skill or agent file runs an `orca` or `orca-ide` command, and none requires Orca to be installed or running. The only allowed mention of Orca in a changed command is as an example of a caller's question channel inside the contract file. Core files (the contract file, the Orca section of `HOW-WE-WORK.md`) may carry Orca command text; AC-C1 searches commands, skills and agents only [F-2]. | Commands run in other projects (`CLAUDE.md:74`); without Orca the calls fail with `runtime_unavailable` (`CAPS:147`). | `CAPS:145-149`; today's baseline: only `sk/ccsession-tag/` mentions Orca (section 1.2, E5) |
> | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by each command listed in this row except load (a no-op where a command has no gate; load writes no report and has no gate, `INV-B:65`; P2-P4 commands get the flag in their own phase; pr-submit gets none under D3(a)) [F-1]; output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
> | AC-C1 | `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents \| grep -v '^src/superclaude/skills/ccsession-tag/'` | prints nothing (SA-2, WC-8); core files are not searched, because the contract file and the Orca section of `HOW-WE-WORK.md` carry Orca command text [F-2] |
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that each command in the P1 row of section 6 except load has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
```

Self-check: each AFTER line (without `>`) was found with `grep -nF` in the candidate (count 1 each), and each BEFORE line (without `<`) in the baseline (count 1 each). Roles are not swapped.

## Lint evidence (`lint-2.md`)

- LINT-REF-1 (spec:147, "F-2 is referenced but never defined", `lint-2.md:5-10`): dismissed. The tag `[F-2]` cites round 1's finding id, defined at `round1.md:33`. The reviser contract requires each addition to cite its finding id (Review Loop bullet 6; REVISE prompt, `document_review_loop_prompts.md:53`). The spec is not meant to define review ids, so this is not a defect.
- LINT-REF-2 (spec:159, "F-1 is referenced but never defined", `lint-2.md:12-17`): dismissed for the same reason (`round1.md:22`).
- Neither lint id is a finding, and neither touches a blocking issue.

## Prior blocking findings

| Prior id | Status | Basis |
|---|---|---|
| F-1 (AC-1.1 cannot pass against the stated phase scope, `round1.md:22-31`) | resolved | Compared with the AFTER text only. AC-1.1 (spec:195) now covers "each command in the P1 row of section 6 except load". The P1 row (spec:159) lists analyze, build, business-panel, design, document, explain, index, test, load, and fixes to adversarial, cleanup-audit, index-repo, workflow. No P4 command (implement, post-release, pr-submit) is in that row, so the three contradictions named in round 1 are gone. They were pr-submit untouched under D3(a) (spec:240), implement and post-release in P4 (spec:109, 113, 162), and `/sc:load` writing no report (spec:112, spec:265). The row also states the load exemption (`INV-B:65` = `inventory/commands-b.md:65`: "writes no file, so a worker has nothing to report"), that P2-P4 commands get the flag in their own phase, and that pr-submit gets none under D3(a). The clause "no section-4 command has one" is kept and agrees with spec:128. Every command AC-1.1 now names is changed in P1, and spec:76 says each changed command gains the section, so the test can pass. |
| F-2 (AC-C1 forbids text that SA-2 and P0 require, `round1.md:33-38`) | resolved | Compared with the AFTER text only. AC-C1 (spec:172) no longer searches `src/superclaude/core`, and SA-2 (spec:147) says core files may carry Orca command text and that AC-C1 covers commands, skills and agents only. The contract file and the Orca section of `HOW-WE-WORK.md` (spec:52, 150, 158) can now carry `orca orchestration ask` and the like without failing AC-C1. No other check scans core for Orca: AC-0.3 (spec:193) only checks that no existing routing row changed, and the E5 grep (spec:25) is a dated baseline observation. The remaining scope (commands, skills, agents) still enforces SA-2 and WC-8 where they apply. |

Prior blocking findings carried: F-1 resolved, F-2 resolved. Open: none. Regressed: none.

## Findings on lines changed against the baseline

No blocking finding. The four changed lines (147, 159, 172, 195) are consistent with the requirements that depend on them, apart from the two Medium items below.

### === REQUIREMENTS ANALYSIS ===

**M-10 | Medium (warning) | Wiegers | origin=unchanged, quotes changed line 159 | AC-1.2 still says "each P1 command" and includes load**
- Changed line 159 now says "load writes no report and has no gate, `INV-B:65`" and exempts load from the flag. AC-1.2 (spec:196, unchanged) says "7.2 live check on each P1 command with `--unattended --output <dir>`", and its pass step 4 (spec:183) needs `test -s <contract>`. The P1 row lists load as a P1 command.
- Grading sentence: an implementer who reads "each P1 command" to include load runs a load worker that has no `--unattended` flag and writes no contract, so step 4 fails. That needs a guess that the implementer picks the worse of two readings. Spec:112 and spec:139 say load is "a step inside another worker's brief, not its own Task", which supports the better reading, so the finding is Medium and not blocking.
- Recommendation: AC-1.2 says "each P1 command except load", matching AC-1.1. Low effort.

**M-11 | Medium (warning) | Wiegers | origin=unchanged, quotes changed line 159 | spec:76 still says every changed command gains the section**
- Spec:76: "Every changed command also gains the `## Unattended mode` section". Load is a changed command (usage line, spec:112, 159) and the changed AC-1.1 and spec:159 exempt it.
- Grading sentence: an implementer may add the section to load, which writes no report, contradicting line 159. AC-1.1 does not forbid the section for load, so no acceptance criterion fails. This needs a guess about which text wins, so it is Medium.
- Recommendation: add "except load" to spec:76.

### === ARCHITECTURE ANALYSIS ===

Nothing new. The SA-2 narrowing means core files and the contract file are the only places that may hold Orca command text. The same-baseline concerns already recorded stay as follow-ups (M-1 to M-9 in `round1.md:73-81`). None of the revised lines touches them.

### Guard Condition Boundary Table (changed lines only)

Guards on the changed lines: the P1 flag scope (spec:159), the AC-C1 search scope (spec:172) and the AC-1.1 assertion scope (spec:195).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `--unattended` accepted ("each command in this row except load") | spec:159 | Zero/Empty (command with no gate) | analyze, build, design... | accepted | "a no-op where a command has no gate" | OK |
| same | spec:159 | Sentinel Value Match (load) | load | excluded | No flag, no report (`INV-B:65`) | OK |
| same | spec:159 | Legitimate Edge Case (the "fixes to" commands: adversarial, cleanup-audit, index-repo, workflow) | listed as fixes, not "commands" | accepted | Read as accepted, since spec:76 gives every changed command the section; not stated in the row | OK (see M-11 for the related spec:76 point) |
| AC-C1 search scope | spec:172 | Legitimate Edge Case (Orca text in core) | `WORKER-CONTRACT.md` with `orca orchestration ask` | not searched | Passes by design, with the reason stated | OK |
| AC-C1 search scope | spec:172 | Legitimate Edge Case (the `plugins/superclaude/` mirror of `HOW-WE-WORK.md`) | mirror copy | not searched | Not stated; it carries the same Orca section as core (spec:158), so it cannot trip the check | OK |
| AC-1.1 assertion | spec:195 | Sentinel Value Match (load) | load | not asserted | "except load" | OK |
| AC-1.1 assertion | spec:195 | Zero/Empty (section-4 command) | any of the six | asserted absent | "no section-4 command has one" | OK |

Omitted classes: "One/Minimal" and "Maximum/Overflow" cannot occur for these scope guards, because the inputs are finite named lists, not counts. No FR-8 or FR-9 finding arises on the changed lines.

### Whittaker adversarial probe (changed lines only)

- Divergence Attack on AC-C1: could the narrower scope hide an Orca call in an installed primitive? The three searched paths cover commands, skills and agents, the same files SA-2 forbids. Core files are not primitives that run an agent, and the contract file is the only core file named to hold Orca text. The residual risk, a stray Orca call in some other core file such as `CLAUDE.md`, is unspecified. It is a requirement the document never states, so it is Medium at most, and not worth a separate id here.
- Sequence Attack on F-1's fix: a P1 implementer adds `--unattended` to the "fixes to" commands (adversarial and the rest) because spec:76 says so, and AC-1.1 then asserts the section for them (spec:195). Consistent. No break.
- Sentinel Collision on `[F-1]` and `[F-2]` tags inside the spec: they are review-loop ids, and a later implementer could read them as requirement ids. Minor, and recorded as a note (N-5).

## Follow-up candidates (Medium findings, no revision triggered)

- M-10 and M-11 above (new).
- M-1 to M-9 from `round1.md:73-81` are unchanged by the revision and stay open as follow-ups (all Medium; M-9 evidence is UNVERIFIED here for the same reason).
- Under the Review Loop, the session that ran this review asks the user once whether to open an issue for these follow-ups and creates none without an answer. An `--unattended` run only records them. This run was not given `--unattended`, but it has no user to ask in this sandbox, so it records the list only.

## Notes (MINOR, never fail the review)

- N-5 The `[F-1]` and `[F-2]` tags added at spec:147, 159, 172 are review ids with no definition inside the spec; they are required by the reviser contract. Consider removing them from the final published spec.
- N-1 to N-4 from `round1.md:85-88` are unchanged.

## Reviser brief

Blocking finding ids: none. No revision is called for. Medium and minor findings (M-1 to M-11, N-1 to N-5) must not be edited under this brief. Revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after and the bytes added and deleted per finding id. Brief clauses overridden: none.

verdict: PASS
