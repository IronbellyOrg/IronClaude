review: 2 of 3

# Spec-panel critique, round 2 (re-review): orca-worker-contract-spec.md

## Header
- Command run: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md` (acted out from `command.md`; no slash command in the sandbox).
- Prompt followed: RE-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full; `~` = the sandbox `home` directory). Hard gate satisfied.
- Roles (fixed by the table, not by reading order): CANDIDATE = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; BASELINE = `.dev/orca-command-refactor/specs/history/spec-v1.md`; PRIOR = `.dev/orca-command-refactor/review/round1.md`.
- candidate sha256: `21fdbd31168a1ef40b1a05d12ef2b15a3e9d6f6fb4d8afb6da439fffe555cae8` (58141 bytes)
- baseline sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (57763 bytes). It equals the candidate hash recorded in PRIOR (`review/round1.md:9`), so the baseline is the text round 1 reviewed.
- prior sha256: `064b6616beb1d729680b59409d56897882501f6886816ad033dcfe0518287d78`
- review number: PRIOR header `review: 1 of 3` (`review/round1.md:1`), so N = 2.
- reviewer model actually used: claude-sonnet-5-5
- Not `--unattended`, not `--improve`: no revised specification is written; the candidate is untouched. `--iterations` is ignored in a re-review.
- Binding context read first: `.dev/orca-command-refactor/README.md:1-38`.
- Brief clauses overridden: none. The brief neither widens scope nor regrades a minor finding.

## Step 1: evidence block
Command run: `diff -w specs/history/spec-v1.md specs/orca-worker-contract-spec.md` (exit 1, three changed lines: 159, 195, 196; same numbering both sides).

BEFORE (baseline), lines starting `<`:
```text
< | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
< | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
```

AFTER (candidate), lines starting `>`:
```text
> | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by the eight section 3.2 commands listed in the next column (analyze, build, business-panel, design, document, explain, index, test); each later phase adds the flag and the section to its own commands together with their gate rows (F2); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that each of the eight section 3.2 commands with phase P1 other than `load` (analyze, build, business-panel, design, document, explain, index, test) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command, no `load`, and no command of phase P2-P4 has one yet (F1, F2) | passes |
> | P1 | AC-1.2 | 7.2 live check on each command named in AC-1.1 (not `load`, which writes no contract; F1) with `--unattended --output <dir>` | all steps pass |
```

Self-check (commands could be run): each AFTER line (without `>`) was found exactly once with `grep -cxF` in CANDIDATE (3 of 3); each BEFORE line (without `<`) was found exactly once in BASELINE (3 of 3). No role swap. Result: roles confirmed.

## Coverage
- Read in full: PRIOR (130 lines), the diff, README, and the candidate lines 1-285 (sections 1-9, Decisions, UNVERIFIED items) to follow the dependencies of the three changed lines: section 2.1 (`:41-43`), section 2.3 (`:73`), section 3 intro (`:76`), 3.1 (`:81-92`), 3.2 (`:97-125`), section 4 (`:127-139`), section 6 (`:153-164`), section 7 (`:166-210`), Decisions (`:254-266`).
- Citation check: `inventory/*.md` are the only checkable evidence. I did not re-run the round 1 resolution of `INV-A`/`INV-B`/`CAPS` references because no cited line changed. The three changed lines add no new citation, only the finding ids `F1`, `F2`.
- UNVERIFIED (outside the sandbox): every `src/superclaude/...`, `CLAUDE.md:N`, `HOW-WE-WORK.md:N`, `EVIDENCE.md` and `.dev/codegraph-migration/...` citation, as in round 1. Nothing on a changed line depends on one.
- Not covered: correctness focus (not requested); whole-document assurance (this is a scoped re-review; see the coverage line below).

## Prior blocking findings

| Id | Prior status | Re-review status | Basis (AFTER text only) |
|---|---|---|---|
| F1 | blocking, open | **resolved** | AC-1.1 (`specs/orca-worker-contract-spec.md:195`) now names the eight section 3.2 P1 commands "other than `load`" and says `no load` has the section; AC-1.2 (`:196`) runs on "each command named in AC-1.1 (not `load`, which writes no contract; F1)". The `load` row (`:112`: report "none (see note)", "P1 (usage line only)") and the Decisions row (`:265`: "a report file would be an unrequested addition") no longer contradict an acceptance check. The prior defect, AC-1.1 and AC-1.2 requiring a contract that `load` must not write, is gone. |
| F2 | blocking, open | **resolved** | P1 scope (`:159`) no longer says the flag is accepted "by every command in sections 3.1 and 3.2"; it names the eight commands whose 3.2 row has phase P1 and adds "each later phase adds the flag and the section to its own commands together with their gate rows". AC-1.1 (`:195`) asserts the section on those eight only, and that no P2-P4 command has it yet. So the P1 state no longer yields an accepted `--unattended` flag with the gate rows (`:100` auggie-review `--no-post-pr`, `:109` implement, `:113` post-release, `:114` pr-submit) still to come, which was the unsafe intermediate state of `review/round1.md:42-53`. Recounted: section 3.2 phase P1 rows are analyze, build, business-panel, design, document, explain, index, load, test = 9 (`:99,101,102,106,107,108,111,112,123`); minus `load` = 8, matching the AFTER text and the revise note's count. |

No prior blocking finding is open or regressed. No finding was deferred or withdrawn by the reviser (`review/revise1.md:19-22`: both "Applied").

## Findings on changed lines (against the baseline, whitespace ignored)

No blocking finding. Two Medium findings, both on changed lines, listed under follow-up candidates.

=== REQUIREMENTS ANALYSIS ===
No blocking requirements finding on changed lines. The AFTER text is consistent with the requirements that depend on it: WC-2/WC-9 (`:60`, `:67`) now apply to a flag that is accepted only where its gate rows land; SA-1 and SA-3 (`:146`, `:148`) are untouched; section 6's rule "Phases 1-3 need no user decision; Phase 4 waits for D2-D4" (`:154`) agrees with P1 no longer covering the P4 commands.

=== ARCHITECTURE ANALYSIS ===
No blocking architecture finding. The phase boundary (`:159-162`) is now the single place that decides when a command gains the flag, which is a cleaner interface than the baseline's "every command" sentence.

## Follow-up candidates (Medium and minor; not in the Reviser brief)
This worker was told to reply with a path only, so the one question per loop ("open an issue for these?") is left to the coordinator; no issue was created.

Medium:
- M11 (origin=changed; MAJOR label, Medium; Wiegers/Cockburn). AC-1.1 (`:195`) says `load` has no `## Unattended mode` section, while the unchanged sentence at `:76` says "Every changed command also gains the `## Unattended mode` section (section 2.1)" and section 2.1 (`:43`) says "Each changed command adds a short `## Unattended mode` section". `load` is a changed command (usage-line fix, `:112`). The load row (`:112`) and the Decisions row (`:265`) point to the AC-1.1 reading, so the reader must pick the specific row over the general sentence; Medium because that reading needs one guess, not zero. A one-clause exception at `:76` would close it.
- M12 (origin=changed; Medium; Crispin/Whittaker). The negative clause "no command of phase P2-P4 has one yet" in AC-1.1 (`:195`) is a permanent assertion in `tests/skills/test_worker_contract.py` if the test is written as stated. When Phase 2 adds the sections, that assertion fails, while AC-C3 (`:174`) requires that no test that passed in the baseline fails and AC-2.1 (`:199`) says the file "gains one assertion" per gate, not "relaxes one". The word "yet" signals a time-bound check, so an implementer can scope it to the P1 state; that is the guess that keeps this Medium. Separate, UNVERIFIED point on the same clause: the definition of `/sc:spec-panel` supplied to this run already contains a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md` (`command.md:455-465`), and spec-panel is a P2 row (`:120`); whether the repository's own copy has it cannot be checked in the sandbox, and if it does, the clause fails on its first run.

Round 1 Medium findings M1-M10 and the three minor notes were not touched by the revision (the diff has no line outside 159, 195, 196) and stay as listed in `review/round1.md:59-77`. They are not re-graded here and do not affect the verdict. Of them, only the round 1 minor note on section 2.3 (`:73`, "every brief includes `--unattended`") interacts with the changed line 159: after the revision, a brief that adds `--unattended` to a P2-P4 command before its phase carries a flag that command does not yet define. The spec names no behaviour for that case. It is a Medium-at-most reading of the unchanged line and does not change the verdict (origin=unchanged; the changed line it depends on is the P1 cell at `:159`).

Minor notes:
- The inline finding tags "(F1, F2)", "(F2)" and "(F1)" now appear inside the spec text (`:159`, `:195`, `:196`). They cite the review ids as the reviser contract requires, but they will outlive the review loop; a reader of the final spec gets ids that point to a report that is not part of it. Note only.

## Guard Condition Boundary Table (guards on changed lines only)
Trigger: the changed lines change the scope of the `--unattended` acceptance guard (`:159`) and the set an acceptance test iterates over (`:195-196`). Classes that cannot occur for these guards are left out with the reason on the last row.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `--unattended` accepted | P1 scope, `:159` | Zero/Empty | command is a P2-P4 command in P1 state | false (not accepted yet) | "each later phase adds the flag and the section ... with their gate rows" (`:159`) | OK |
| `--unattended` accepted | P1 scope, `:159` | Typical | one of the eight P1 commands | true | section + contract per `:195-196` | OK |
| `--unattended` accepted | P1 scope, `:159` vs `:73` | Legitimate Edge Case | brief includes `--unattended` for a P2-P4 command in P1 state | undefined | command behaviour on an unknown flag not stated | GAP (Medium, see the unchanged-line note above) |
| AC-1.1 command set | `:195` | Zero/Empty | `load` (no report by design) | excluded | "no `load` ... has one" | OK (F1 resolved; tension with `:76` is M11) |
| AC-1.1 command set | `:195` | One/Minimal | exactly the eight named commands | iterated | asserts section + both names | OK |
| AC-1.1 command set | `:195` | Legitimate Edge Case | P2-P4 command after its own phase starts | assertion "has none yet" | fails once Phase 2 lands unless relaxed | GAP (M12, Medium) |
| AC-1.2 live check set | `:196` | Typical | the eight commands, `--unattended --output <dir>` | iterated | 7.2 all steps | OK |
| Zero/Maximum for counts | n/a | n/a | n/a | n/a | the only counts on changed lines are the "eight" and the phase membership, reconciled in the prior-findings table | left out: no counter or collection beyond that |

FR-8/FR-9 grading: neither GAP names a concrete wrong outcome that follows from the stated text with no further assumption, nor a security, data-loss or safety-boundary risk, so both are Medium (follow-up candidates). The table is complete, so FR-10 does not block the verdict.

## Quantity Flow Diagram (changed counts only)
```text
[section 3.2: 27 needs-change commands]
   --> phase P1: 9 rows (analyze, build, business-panel, design, document, explain, index, load, test)
        --> AC-1.1 / AC-1.2 consumer: 9 - 1 (load, no contract) = 8 commands   (matches :159, :195, :196)
   --> phase P2: 11, P3: 4, P4: 3 (not covered by AC-1.1; gain flag + section in their own phase)   9+11+4+3 = 27
[section 3.1: 10 ready]  --> P1 fixes: adversarial, cleanup-audit, index-repo, workflow (4; no section asserted by AC-1.1)
```
No count is lost or double-counted; the baseline mismatch (AC-1.1 assuming 37 commands, `review/round1.md:107`) is gone.

## Whittaker attacks (reported where a finding resulted)
- I can break this specification by **Sequence Attack**. The invariant at **AC-1.1 (`:195`) with AC-C3 (`:174`)** fails when **Phase 2 lands after Phase 1 shipped the test**. Concrete attack: P1 passes with the assertion "no P2-P4 command has the section"; P2 adds the section to `task`; the P1 assertion now fails and AC-C3 forbids a baseline-passing test to fail. Mitigated by the word "yet"; graded Medium (M12).
- Attack on F2's resolution by **Divergence Attack**: P1 ends with 8 commands accepting the flag and 19 with none. A coordinator that follows `:73` and adds `--unattended` everywhere gets an undefined result on the 19. Not a state the changed text creates (unchanged `:73`), so a note only.
- Attacks by **Zero/Empty**, **Sentinel Collision** and **Accumulation** found nothing on changed lines.

## Auto-suggestion
No new numeric thresholds on changed lines; the round 1 advisory to re-run with `--focus correctness` stands and remains advisory only.

scoped PASS: changed lines + prior blockers

## Reviser brief
Blocking finding ids: none. Nothing for a reviser to repair. (Rules restated from the command's Review Loop bullet 6: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; cite the finding id on each addition; prefer deleting or narrowing; report bytes before and after and bytes added and deleted per finding id. Medium findings M1-M12 and minor notes are not to be edited.)

verdict: PASS
