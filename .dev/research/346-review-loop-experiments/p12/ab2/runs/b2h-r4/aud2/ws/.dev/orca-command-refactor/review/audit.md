review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (labelled whole-document audit of the final spec; a first review, no `--re-review` or `--baseline`)
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `87c84d9ca9169f943376688b64d421baec2513be9fe5034504496a4473d86140`
- Baseline: none given (first review of the full document)
- Reviewer model actually used: claude-sonnet-5-5
- Prompt followed: FIRST-REVIEW in `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full)
- Panel (fixed order): Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard (architecture); Whittaker (always active); Newman, Hohpe (architecture). Crispin, Gregory and Hightower are not part of the requested focus; Crispin only completed the guard table.
- Coverage: the whole candidate (286 lines) was read. README `.dev/orca-command-refactor/README.md:1-39` was read first. Checked against the three inventories: the command tables and verdict counts in `inventory/commands-a.md` and `inventory/commands-b.md`, and the Orca facts in `inventory/orca-capabilities.md` lines 44-188 (spot checks). Citations to files outside `.dev/orca-command-refactor/` (`cmd/`, `sk/`, `CLAUDE.md`, `/opt/Orca/...`, `.dev/evals/...`, `.dev/codegraph-migration/...`) cannot be opened in this sandbox and are UNVERIFIED here except where an inventory line quotes them. Not covered: any live run, and the "about 340 citations re-read" claim at spec:285.

## Result in one paragraph
The decision (Orca on top, commands stay units of work) is well supported by the evidence the inventories quote, the 10 / 27 / 6 split matches the inventories (A: 5 ready + 13 change + 3 coordinator-only = 21; B: 5 + 14 + 3 = 22; sum 10 / 27 / 6 = 43), and the 27 rows of 3.2 and 10 rows of 3.1 are all present. One stated text contradicts an acceptance criterion (F-01) and blocks. Eight Medium findings and four notes are listed under follow-up candidates.

## Verification of counts (Pipeline Dimensional Analysis check)
The only count-changing flow in the spec is the command classification. Source 43 commands -> 10 ready (spec:78-92) + 27 needs-change (spec:94-125) + 6 coordinator-only (spec:127-137) = 43; spec:76 states the same. INV-A:3 says 21 and INV-B:3 says 22. No mismatch.

```text
[43 cmd/*.md] --> [INV-A 21 + INV-B 22] --> [10 ready (3.1)] + [27 change (3.2)] + [6 coordinator-only (4)] = 43   (no divergence)
```

## === REQUIREMENTS ANALYSIS ===

### F-01 (CRITICAL by label, blocking) `/sc:load` is required to have a contract and is required not to (Wiegers, Adzic)
- Grading sentence: an implementer who follows the stated text as written builds a P1 `test_worker_contract.py` and a `/sc:load` that satisfy AC-1.1 and AC-1.2, and X is wrong because the same document says `/sc:load` has no report file and must not get one, so one stated text or the other fails.
- Stated texts:
  - spec:76 "Every changed command also gains the `## Unattended mode` section"; spec:79 / spec:62 (WC-4) contract "written on every outcome".
  - spec:112 `load`: report "none (see note)", resume "n/a", change "use it as a step inside another worker's brief, not as its own Task", phase "P1 (usage line only)"; spec:265 (Decisions): "a report file would be an unrequested addition".
  - spec:159 lists `load (usage line only)` in the P1 scope.
  - spec:195 AC-1.1: the test asserts that "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`". `load` is in 3.2 (spec:112).
  - spec:196 AC-1.2: a 7.2 live check "on each P1 command with `--unattended --output <dir>`"; 7.2 step 4 (spec:183) requires `test -s <contract>` with `status` and `command`. `load` is a P1 command (spec:159) and has no contract.
- Concrete trace: P1 test run -> `load.md` has no `## Unattended mode` section, as spec:112 asks -> AC-1.1 fails. Adding the section with a contract creates the "unrequested" report that spec:265 forbids. The same holds for AC-1.2 step 4.
- Recommendation: state `load` as an explicit exception in AC-1.1 and AC-1.2 (and in spec:76), or give it a contract and delete the spec:112 / spec:265 position. Pick one.
- Priority High. Quality impact: Testability / Consistency.

## === ARCHITECTURE ANALYSIS ===
No blocking architecture finding. The core decision, the rejected alternative and the depth-1 reasoning are consistent with `CAPS:97-103` and `CAPS:145-161` (quoted lines read above). The Medium items below are listed under follow-up candidates.

## Guard Condition Boundary Table (Nygard lead, Crispin completeness, Whittaker attack)
Classes left out are noted per guard (one line each). Spec behavior is quoted from the spec lines given.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| Contract `status` check | WC-5 spec:63 | Zero/Empty | contract file missing or 0 bytes | fails | `--outcome failed` (P1 on), P0 uses the named report (N-1) | OK |
| Contract `status` check | WC-5 spec:63 | Sentinel Value Match | `status: Succeeded`, or a value outside the four | fails | `failed` by default (B-5; the id is not defined, see M-03) | OK |
| Contract `status` check | WC-5 spec:63 | Legitimate Edge Case | workflow's own `status` vocabulary (INV-B:272), existing contract fields kept (spec:62) | unknown | not specified which of the two vocabularies wins (M-06) | GAP |
| Nesting depth | WC-8 spec:66, R1 spec:33 | Maximum/Overflow | worker calls `worker-start` at depth 1 | refused (`CAPS:97-99`) | WC-8 forbids the call; whether `task-create` is allowed is UNVERIFIED (spec:276) | OK |
| Readiness limit | WC-1 spec:59 | Maximum/Overflow | prompt above ~45 s | fails | owner is "launch setup"; no acceptance check in section 7 (M-08) | GAP |
| Confidence gate | task row spec:121 | Typical | confidence < 0.70 | true | blocked | OK |
| Confidence gate | task row spec:121 | Legitimate Edge Case | blocked question needs an answer re-supplied "as a flag" (WC-3 spec:61) | n/a | no such flag exists for this gate (M-04) | GAP |
| Wait size | WC-10 spec:68 | Maximum/Overflow | single tool call > 5 min | heartbeat missed | split into waits <= 4 min | OK |
| Wait size | WC-10 spec:68 | Legitimate Edge Case | pr-submit poll script runtime | unknown | UNVERIFIED (spec:283) | GAP |
| Output kind | WC-4 spec:62 | Zero/Empty | row says "add a report path" without file or directory (spec:99, 101, 106-108, 111, 123) | n/a | contract path cannot be derived (M-02) | GAP |
| Output collision | WC-4 spec:62 vs WC-11 spec:69 | One/Minimal | two tdd workers, `--output a/x.md` and `a/y.md` | same file `a/tdd-return-contract.yaml` | overwritten; WC-11 says it must never happen (M-01) | GAP |
| Unattended switch | D1 spec:227-230 | Zero/Empty | flag absent | false | SA-1: behaviour unchanged | OK |
| Circuit breaker | WC-6 spec:64 | Maximum/Overflow | three failed starts | trips (`CAPS:80,116`) | worker's own `failed` report does not count (spec:263) | OK |
| Resume flag | WC-6 spec:64 | Zero/Empty | no resume flag and no state | fresh dir | stated per command | OK |

Classes not given a row: Zero/Empty for the nesting depth and the confidence gate cannot occur (depth floors at the default, `CAPS:100`; confidence is a ratio). The six GAP rows above name no wrong outcome that needs no further assumption (each needs a reader to pick the worse of two allowed readings, or is an unstated edge), so they are Medium and appear below as M-01, M-02, M-04, M-06, M-08; the pr-submit poll-runtime row is already an UNVERIFIED item at spec:283. F-01 is outside this table.

## Whittaker attack findings
- **Sequence attack (WC-3 vs WC-2/WC-5, spec:60-63).** Trace: command hits gate -> writes `status: blocked` -> stops (WC-2) -> worker `ask`s, then re-invokes the command with the answer -> contract is overwritten (WC-4 "written on every outcome") -> worker sends `worker_done` once (WC-5). Invariant "report reflects last run" holds; but nothing says the first blocked contract is kept or that the re-invocation is a resume. Medium (inside M-04).
- **Divergence attack (WC-4 directory vs file rule, spec:62).** `--output <dir>` and `--output <file>` give different names; rows with an unspecified kind leave both possible: M-02.
- **Sentinel collision (status vocabulary, spec:62, 262).** Existing contracts carry their own `status` (INV-B:272); the fixed four values collide with them: M-06.
- **Zero/Empty (WC-5).** Handled well (zero bytes, truncated, unparseable) at spec:63 and AC-2.2 spec:200.
- **Accumulation (heartbeats, WC-10).** Handled by the 4-minute rule; the poll runtime stays UNVERIFIED (spec:283).

## Follow-up candidates (Medium and minor; none blocks, none enters the Reviser brief)

Medium:
- **M-01** WC-4's file rule (`<file's directory>/<command>-return-contract.yaml`, spec:62; tdd at spec:90, init-lite at spec:87, spec-panel at spec:120) collides with WC-11 (spec:69). Two parallel workers of the same command writing different files in one directory share one contract file. Needs the guess that the coordinator picks the same directory, so Medium. (Nygard, Whittaker)
- **M-02** Many 3.2 rows say "add a report path" or "add `--output`" without saying file or directory (spec:99, 101, 106, 107, 108, 111, 123), but WC-4 derives the contract path from that kind and says the path is "known before dispatch". (Wiegers)
- **M-03** The ids B-1, B-3, B-5 and N-1 are used as authority in spec:62, 63, 76, 79, 92, 182, 194, 198, 200 but are not defined in the spec, in the README or in the inventories (`grep` over `.dev/orca-command-refactor` finds them only in the spec). The rules themselves are restated inline, so an implementer can still act; a reader cannot trace the source. (Wiegers)
- **M-04** WC-3 (spec:61) says the worker re-invokes "with the answer as a flag", but several blocked gates have no flag that carries an answer: task confidence below 0.70 and TFEP (spec:121), implement Ruling (spec:109, D2), pr-submit HALTs (spec:114), cli-eval W0 confirm (spec:104). Also unstated: whether the re-invocation resumes or restarts. (Adzic, Cockburn)
- **M-05** tasklist and reflect (spec:88, 122): under `--unattended`, Stage 10.5 passes `--unattended` to reflect so reflect's headless auto-accept rule applies. That rule "auto-accepts for auto-fixable registers" (INV-B:109), i.e. a `--remediate` run goes on to hand off to `sc:workflow` / `task-builder` without a person. INV-B:215 recommended dropping `--remediate` in 10.5 instead. The spec chooses the other option without stating why, WC-9 does not cover it (remediation is not an outward action, but it is unrequested work), and the `needs_human_decision` HALT at INV-B:209 is not addressed. Spec:280 item 9 also says reflect probably does not treat a worker as headless, which is the case this row repairs. (Fowler, Nygard)
- **M-06** WC-4 says commands with an existing contract "keep their fields and add the missing ones" (spec:62) while WC-5 and the Decisions fix a four-value `status` set (spec:63, 262). Workflow's existing `status` values are not listed in the inventory (INV-B:272), so whether they already match is UNVERIFIED; a mismatch maps to `failed` through B-5. (Whittaker)
- **M-07** AC-C1 (spec:172) scans `src/superclaude/core`, where the new `WORKER-CONTRACT.md` lives (spec:52), for `orca orchestration ...` text; WC-3 and the brief template (spec:158) need to name the preamble's `ask` command. SA-2 (spec:147) allows an Orca mention "as an example of a caller's question channel" but does not say it may use the `orca orchestration` form, so the contract file can fail the common check. (Fowler)
- **M-08** WC-1 (spec:59) is owned by "launch setup, not commands" yet has no acceptance check in section 7, and no phase scope item delivers it (spec:156-162). (Crispin)

Minor notes:
- **N-01** spec:43 says "Phase 0 therefore starts with live smoke runs", but spec:158 puts the smoke runs after the file edits ("Then run").
- **N-02** The claim at spec:285 (about 340 citations re-read, 9 defects fixed) and the E5 grep results (spec:25) cannot be checked in this sandbox: UNVERIFIED.
- **N-03** Tasklist's row (spec:122) rests on nesting being allowed (INV-A:14) while INV-B:210 and INV-B:312 mark subagent-to-agent nesting UNVERIFIED; the spec cites only the first.
- **N-04** AC-C5 (spec:176) checks command files only; the skill edits in P2 and P3 (reflect, roadmap, validate-roadmap) have no additive-edit check.

Issue question: per the command's Review Loop bullet 3, the session that ran this review asks the user once whether to open an issue for the follow-up candidates and creates none without an answer. This run cannot ask; no issue was created. This is recorded for the coordinator.

## Reviser brief
Blocking finding ids: F-01 only.
Rules for the reviser (restating Review Loop bullet 6 and the REVISE prompt): revise only text that F-01 names (spec:76, 112, 159, 195, 196, 265); add no rule, mechanism or section that F-01 does not call for; cite the finding id on every added paragraph or table row; prefer deleting or narrowing to adding (for example one sentence in AC-1.1 and AC-1.2 naming `load` as the exception); report the byte size before and after, and the bytes added and deleted per finding id; leave Medium (M-01 to M-08) and minor (N-01 to N-04) findings alone; return the candidate once and do not award yourself a PASS.

verdict: FAIL
