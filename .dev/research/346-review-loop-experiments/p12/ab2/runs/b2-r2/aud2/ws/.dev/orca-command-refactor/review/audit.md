review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (critique, focus requirements,architecture)

- Label: whole-document audit of the final spec, a first review of the whole document (not a re-review). Prompt followed: FIRST-REVIEW in `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`.
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- candidate sha256: `68ce70455b6b30e6a44dbd6460d0688443a0dcdfe80ef873cfa87d79d9501aee`
- baseline: not applicable (first review; neither `--re-review` nor `--baseline` given)
- reviewer model used: claude-sonnet-5-5 (Sonnet 5.5)
- Citation convention: `S:N` = line N of the candidate; `CAPS:N`, `INV-A:N`, `INV-B:N` = the three inventory files; `README:N` = `.dev/orca-command-refactor/README.md`.
- Coverage: I read all 285 lines of the candidate, README (38 lines), all of `orca-capabilities.md` lines cited by the candidate, and the `commands-a.md` / `commands-b.md` lines it cites (spot-checked about 60 lines). I did NOT have access to `src/superclaude/**`, `CLAUDE.md`, `EVIDENCE.md`, `pyproject.toml`, `Makefile` or `.dev/codegraph-migration/**`; every candidate citation into those files is UNVERIFIED by me and is graded only by internal consistency. Counts were checked: the 43 commands split 10 + 27 + 6 (S:76; rows S:83-92, S:99-125, S:132-137) and the per-phase command lists (S:159-162) add up to the 27 section-3.2 rows. No count-diverging pipeline exists, so no Quantity Flow Diagram is produced.

## Summary

One blocking finding (F-01: the P1 acceptance check cannot pass without doing P3/P4 work that the spec defers to later phases and to user decisions). Five Medium warnings and five minor notes follow. The central decision (Orca coordinates, commands stay workers) is consistently argued and its evidence gaps are honestly stated (S:41-45); I found no contradiction in section 1.

## === REQUIREMENTS ANALYSIS ===

### F-01 (blocking, MAJOR) — AC-1.1 requires P1 to deliver work the spec assigns to P3/P4 and to undecided D2-D4
- Experts: Wiegers (traceability), Adzic (example), Crispin (acceptance).
- Grading sentence: an implementer who follows the stated text as written builds, in Phase 1, a `## Unattended mode` section in every command of sections 3.1-3.2 except `load` (including implement, post-release, pr-submit, roadmap, save, validate-roadmap, validate-tests), because AC-1.1 asserts exactly that (S:195) and "Later phases do not start until the earlier phase's checks in section 7 pass" (S:154); and that is wrong because the same spec says the P1 command list is nine commands plus three fixes (S:159), the gate resolutions of those other commands are defined by phases P2-P4 (S:160-162), "Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4" (S:154, S:225), and under the recommended D3(a) "no pr-submit changes in Phase 4" (S:240). So P1 either fails AC-1.1 (the P4 commands and the 3.1 commands not in the S:159 list lack the section) or ships implement/post-release/pr-submit gate text before D2-D4 are answered. Section 2.1 makes this worse: each section "lists only its own gate resolutions" (S:52), so a P1 section for `implement` must already contain the D2 outcome.
- Also in conflict: S:159 says the flag is "accepted by every command in sections 3.1 and 3.2 except `load`" while its Commands column lists only analyze, build, business-panel, design, document, explain, index, test, load plus three fixes; S:128 says section-4 commands get no mode, but D3(a) leaves pr-submit with none either (S:139, S:240), so AC-1.1 cannot assert both.
- Recommendation (narrowing, no new rule): scope AC-1.1 and the S:159 flag sentence to the commands listed in the P1 row; let each later phase's own check (AC-2.1, AC-3.x, AC-4.x) cover the `## Unattended mode` section of the commands it converts; state that pr-submit has no section unless D3(b) is chosen.
- Priority High. Quality impact: removes a phase-gate that no implementer can pass as written.

### M-01 (Medium) — WC-4 "path known before dispatch" has rows that do not meet it
- S:62 sets the default `<output-dir>/return-contract.yaml` with "four" exceptions "whose section 3.1 row fixes another path (B-1)". Section 3.1 rows for tdd and init-lite (S:87, S:90) do not give `<file>.return-contract.yaml`; only WC-4 does. Rows with other contract locations are not in the four: implement "beside the ledger `progress.md`" (S:109, ledger location not stated in the spec), pr-submit "beside `monitor-run-<PR>.jsonl`" (S:114), research "naming the generated `claudedocs/research_*.md` path" (S:116, contract location not stated), cli-portify "file location unnamed" (S:105), cleanup-audit fixed `.claude-audit/` (S:85). The coordinator then cannot know the report path before dispatch, which WC-4 and section 2.3 (S:73) require and 7.2 step 3 checks (S:182).
- Not blocking: an implementer must guess a location, which needs an assumption. Recommendation: one column "Contract path" in sections 3.1-3.2 stating the path or "workflow-generated, learned from `worker_done`". `B-1` is an undefined label (see N-02).

### M-02 (Medium) — "Keep their fields" versus the fixed four-value status set
- S:62 says commands that already write a contract "keep their fields and add the missing ones" while `status` must be one of succeeded/partial/failed/blocked; the Decisions row fixes that set (S:262). The existing contracts of workflow/brainstorm/reflect/adversarial (S:261) may use other `status` values; the candidate does not show them (`INV-B:272` names a `status` field without values). UNVERIFIED either way. 7.2 step 4 (S:183) asserts the four values, so an existing value outside the set fails the check. Recommendation: state the mapping from each existing vocabulary, or say the new field is separate.

### M-03 (Medium) — Missing handling for a blocked worker's answer and for a retry's output directory
- A blocked worker ends `failed` (S:63, S:200); a failed Task keeps dependents blocked until a `--retry-of` replacement succeeds (`CAPS:90`). WC-3 covers only the in-session `ask` route (S:61, optional "may"). The spec never says how the coordinator supplies the missing flag after a `blocked` outcome (a retry brief?) or that a "fresh dir" command (S:99-125, many rows) needs a different directory in the retry brief to satisfy WC-6 (S:64); section 2.3 (S:73) lists neither. AC-2.2 (S:200) also requires `worker_done --outcome failed`, which conflicts with the WC-3 "may ask instead" path (S:61) unless the test forbids `ask`. Recommendation: one sentence in 2.3 on the retry brief, and say AC-2.2 is run with the `ask` route unused.

### M-04 (Medium) — Edge: `--unattended` with no output flag, and an unreadable contract at outcome mapping
- See Guard table rows G-2 and G-3. Only post-release, cli-eval, spec-panel and a few others say what happens when a required value is missing (S:104, S:113, S:120); for analyze, build, design, document, explain, index, test, research, recommend and others the row says "add `--output`" (S:99-125) but not what `--unattended` does without it. WC-5 (S:63) maps "no report exists" to failed but is silent on a report that exists and is unparseable or has a `status` outside the set.

## === ARCHITECTURE ANALYSIS ===

### M-05 (Medium) — WC-10 threshold contradicts the 4-minute rule used elsewhere
- WC-10 requires splitting only a call that blocks "longer than 5 minutes" into waits of at most 4 (S:68). The pr-submit row requires each iteration "under 4 minutes" (S:114), AC-4.3 fails any call over 240 s (S:210), and the Decisions row justifies 4 minutes as the margin under 5 (S:266). A 270-second wait complies with WC-10 and fails AC-4.3. Because the pr-submit row and AC-4.3 apply only under D3(b), this stays Medium. Recommendation: state the rule once as "no single tool call over 4 minutes" in WC-10. WC-10's cli-eval application (S:104) has no acceptance check in section 7 (AC-4.3 is pr-submit only): a follow-up.

### M-06 (Medium) — AC-C1 can fail on text the spec itself requires in `core/`
- AC-C1 greps `src/superclaude/core` for `orca(-ide)? (orchestration|worktree|terminal|agent)` and requires no output (S:172). P0 adds `WORKER-CONTRACT.md` (a brief template) and an Orca section to `HOW-WE-WORK.md`, both in `core/` (S:158); SA-2 explicitly allows an Orca mention as "an example of a caller's question channel inside the contract file" (S:147). If any of these files writes `orca orchestration ask` in lower case, AC-C1 fails on P0's own deliverable. Needs the guess that the text uses that exact form, so Medium. Recommendation: scope AC-C1 to commands, skills and agents (which is what SA-2's first sentence says) or exclude the two P0 core files.

## === Minor notes ===
- N-01: E4 (S:24) states flatly that subagents "are not counted by Orca's nesting limit"; its own evidence line `CAPS:155` ends "UNVERIFIED that Orca never limits them", and S:45 says as much. Soften E4.
- N-02: dangling labels: `(B-1)` at S:62 and "ladder rung 2" at S:261 are defined nowhere in the candidate or README.
- N-03: line-number drift between two readings of the same rule: WC-7 cites `sk/sc-pr-submit-protocol/SKILL.md:37-39` (S:65) while `CAPS:161` cites the installed copy at lines 47-49 for the same "Top-level activation required" text. Source file not available to me; UNVERIFIED which is right, probably src versus installed copy.
- N-04: AC-0.4 (S:194) says "steps 1-3 and 5-7 pass; steps 3 and 4 use the command's existing report": step 3 appears in both halves. Reword.
- N-05: 7.2 step 2 (worker-show at least every 5 minutes, S:181) and step 3 (`check --wait --timeout-ms 900000`, S:182) read as concurrent; say step 3 is looped with shorter timeouts. Also SA-4's list of allowed in-place edits (S:149) looks closed, while AC-C5 (S:176) would flag any in-place line change in P2 rows such as reflect's `--remediate` prompt (S:88); say whether those are additive overrides inside `## Unattended mode`.

## Mandatory output: Guard Condition Boundary Table
Triggered (the spec contains thresholds and boolean guards). Six classes are the menu; classes that cannot occur are omitted with the reason in the last paragraph. Nygard built, Crispin checked, Whittaker attacked (Whittaker attacks recorded below the table).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G-1 `--unattended` present | S:51, S:146 (SA-1) | Zero/Empty | flag absent | false | Today's behaviour unchanged, no new file (SA-1, SA-3) | OK |
| G-2 required output flag given | S:62, S:73, S:99-125 | Zero/Empty | `--unattended` with no `--output` (analyze, build, design, document, explain, index, test, research, recommend) | false | Not stated for these rows; only post-release/spec-panel-type rows say blocked (S:113, S:120) | GAP (Medium M-04) |
| G-3 report parse in WC-5 | S:63 | Zero/Empty | contract file empty or invalid YAML | n/a | Only "no report exists" is mapped to failed | GAP (Medium M-04) |
| G-4 status in set | S:62, S:183 | Sentinel Value Match | existing contract `status` outside the four values | false | Not stated (see M-02) | GAP (Medium M-02) |
| G-5 `blocked` collision | S:60-63 | Sentinel Value Match | a command's own report already uses the word "blocked" (for example a verdict) | ambiguous | WC-5 maps the contract `status`, not the verdict (S:63 first sentence states both) | OK |
| G-6 wait size (WC-10) | S:68 | Typical | single call 3 minutes | not split | No split needed | OK |
| G-7 wait size (WC-10) | S:68, S:114, S:210 | Legitimate Edge Case | single call 270 s | >5 min false, so no split required | WC-10 allows it; AC-4.3 and the pr-submit row reject it | GAP (Medium M-05) |
| G-8 depth limit | S:33, S:66 (WC-8) | Maximum/Overflow | worker calls `task-create` at depth 1 | UNVERIFIED (`CAPS:103`) | WC-8 forbids it regardless | OK |
| G-9 `consumer_fenced` | S:70 | Legitimate Edge Case | `check` returns `consumer_fenced` | true | Stop, no `worker_done` (WC-12) | OK |
| G-10 `--outcome` mapping | S:63 | One/Minimal | one-line report `status: partial` | true | `succeeded`, first sentence says partial | OK |
| G-11 retry directory | S:64, S:73 | Legitimate Edge Case | `--retry-of` re-run of a "fresh dir" command with the same brief | true | Brief must name a new dir, not stated | GAP (Medium M-03) |

Classes left out: Maximum/Overflow for G-1 to G-7 and G-9-G-11 (no capacity limit applies to these boolean or enumerated guards). "One/Minimal" omitted for guards G-2 to G-9 and G-11 because the minimal and typical inputs coincide.

Whittaker attacks (five methodologies against the invariants "path known before dispatch", "exactly one worker_done", "no outward action without brief"):
- Zero/Empty: I can break this specification by Zero/Empty Attack. The invariant at WC-4 (S:62) fails when a P1 command runs with `--unattended` and no output flag. Concrete attack: before, no `<output-dir>`; after, the command either writes into the working tree root or stops; the spec does not say which (M-04).
- Divergence: I can break this specification by Divergence Attack. The invariant at WC-10 (S:68) fails when a call lasts 270 s: compliant by S:68, non-compliant by S:210 (M-05).
- Sentinel Collision: I can break this specification by Sentinel Collision Attack. The invariant at WC-4 status set (S:62) fails when an existing contract already uses `status: complete` or similar; the "keep their fields" clause keeps it and 7.2 step 4 rejects it (M-02).
- Sequence: I can break this specification by Sequence Attack. The invariant at WC-5 "exactly once" (S:63) fails when the worker sends `worker_done` after `ask` returned and the command re-ran blocked a second time; the spec does not say whether a second blocked contract overwrites the first, nor how the coordinator answers after a `failed` blocked outcome (M-03).
- Accumulation: I can break this specification by Accumulation Attack. Orca's circuit breaker counts failed `worker-start` attempts, not a worker's own `failed` report (`CAPS:80`, `CAPS:116`), so repeated blocked/failed retries are unbounded by Orca; the spec sets no retry cap for the coordinator. Medium follow-up, folded into M-03.

## follow-up candidates (Medium and minor, no revision triggered)
M-01, M-02, M-03, M-04, M-05, M-06, N-01, N-02, N-03, N-04, N-05. Whether to open an issue for them is a question for the user, once per loop; this run is a worker in a sandbox and created none.

## Reviser brief
Blocking finding ids: F-01 only. Restated contract: revise only the text F-01 names (S:154, S:159, S:195, with S:139/S:240 only to state pr-submit's position); add no rule, mechanism or section that F-01 does not call for; each added paragraph or table cites F-01; prefer deleting or narrowing to adding; report the byte size before and after and the bytes added and deleted per finding id; leave Medium and minor findings alone; do not award yourself a PASS.

verdict: FAIL
