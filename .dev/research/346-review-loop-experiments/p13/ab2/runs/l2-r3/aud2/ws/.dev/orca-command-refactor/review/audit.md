review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (labelled whole-document audit, first review; no `--re-review`/`--baseline` given)
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines), sha256 `032a73216d9fa2a2e58b2be6fa0c2ed6374df75cb60076a9b7d7f4bd03d07a67`
- baseline: not applicable (first review)
- reviewer model used: claude-sonnet-5-5
- citation key: `SPEC:N` = the candidate; `CAPS:N`, `INV-A:N`, `INV-B:N` = `.dev/orca-command-refactor/inventory/{orca-capabilities,commands-a,commands-b}.md` line N. Only those three files and the README are checkable in this sandbox. Any `src/`, `CLAUDE.md`, `EVIDENCE.md`, `pyproject.toml`, `Makefile` or Orca-binary citation that is not quoted in an inventory is UNVERIFIED here.
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`. Grading by consequence (`command.md:259`).

## Coverage
Read in full: the candidate, `.dev/orca-command-refactor/README.md`, the review-loop prompts file and the command definition. Spot-checked every `CAPS:` line the requirement tables cite (about 40 lines) and the `INV-A`/`INV-B` lines cited for the counts, the workflow, tasklist, reflect and adversarial rows. Not checked (UNVERIFIED): all `sk/`, `cmd/`, `src/superclaude/cli/`, `CLAUDE.md`, `EVIDENCE.md` and `.dev/codegraph-migration/` line citations. The spec's own claims of a re-read of 11 locations and a 340-citation check (`SPEC:11`, `SPEC:285`) cannot be confirmed here. The focus areas are requirements (Wiegers, Adzic, Cockburn) and architecture (Fowler, Newman, Hohpe, Nygard). Whittaker is always active. Counting check: 3.1 has 10 rows, 3.2 has 27, section 4 has 6, total 43, matching `SPEC:76`. The phase lists P1 to P4 partition the 37 worker-capable commands consistently with the `Phase` column.

## Findings

### Blocking

**B1 (CRITICAL, Wiegers, Fowler): the P1 scope and acceptance test contradict the P4 deferral and the D3 recommendation.**
Grading sentence: an implementer who follows the stated text as written builds an `## Unattended mode` section and `--unattended` flag for `/sc:implement`, `/sc:post-release` and `/sc:pr-submit` in Phase 1, and that is wrong because those sections must "list only [the command's] own gate resolutions" (`SPEC:52`) and those resolutions are exactly what open decisions D2, D3 and D4 have not yet settled.
- `SPEC:154` says "Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4", and `SPEC:162` assigns implement, post-release and pr-submit to P4.
- `SPEC:159` says P1 adds `--unattended` to "every command in sections 3.1 and 3.2 except /sc:load". Those sections include all three P4 commands (`SPEC:109`, `SPEC:113`, `SPEC:114`).
- `SPEC:195` (AC-1.1) requires "every command in sections 3.1-3.2 except /sc:load" to carry the section naming `return-contract.yaml`. P1 therefore cannot pass for pr-submit unless it is edited, yet D3(a), the recommendation, says "no pr-submit changes in Phase 4" (`SPEC:240`) and `SPEC:139` says pr-submit "stays a worker candidate only if the user accepts D3". Under D3(a) the test demands a section the decision says should not exist.
- Concrete trace: user picks D3(a) and D2(a). P1 runs AC-1.1. If pr-submit is edited to pass the test, the spec's own D3(a) outcome is violated. If it is left alone, AC-1.1 fails and "later phases do not start until the earlier phase's checks pass" (`SPEC:154`) blocks P2.
- Minimum repair: scope P1 and AC-1.1 to the P1 to P3 commands, or state that the P4 commands get only the bare flag and a stub section in P1 (and say what the stub contains).

**B2 (MAJOR, graded blocking, Cockburn, Nygard): the workflow report path is not known before dispatch and has no location for pre-creation stops.**
Grading sentence: an implementer who follows the stated text as written builds a `/sc:workflow` that writes its contract at `.dev/tasks/to-do/<id>/return-contract.yaml` (`SPEC:92`) and must also write it for "pre-creation STOPs" (`SPEC:92`, AC-1.4 at `SPEC:198`), and that is wrong because no `<id>` or package directory exists at a pre-creation stop, so no contract path is specified for the very case being added.
- WC-4's heading requires the report file "known before dispatch" and says it sits in the `<output-dir>` the coordinator passed (`SPEC:62`). The workflow row passes only `--handoff none` (`SPEC:92`), so the coordinator cannot name the path and cannot set `--report-path` at dispatch or check step 3 of `SPEC:182`.
- Evidence of the gap: `INV-B:270-271` says the contract is "Not written for pre-creation STOPs" and the path is id-based.
- Minimum repair: give workflow an output-directory flag or a fixed pre-creation fallback path, and say which one a pre-creation stop uses.

### Medium (warnings, follow-up candidates, not blocking)

**M1 (Fowler): `/sc:tasklist` Stage 10.5 resolution relies on a headless rule the spec itself assumes does not apply.** `SPEC:122` says `--unattended` passes `--unattended` to each reflect "so the headless rule applies", and `SPEC:88` makes `--remediate` follow that rule. `SPEC:280` (UNVERIFIED item 9) and `INV-B:310` say an Orca worker is not `claude --print`, so the rule is assumed not to fire. `INV-B:215` recommends dropping `--remediate` in Stage 10.5 instead, and `INV-B:46` says Stage 10.5 passes `--remediate` today. With auto-accept, reflect would proceed into remediation handoff (`INV-B:109`) in a worker that never asked for it. Only a guess that the worse reading is implemented makes this wrong, so it is Medium. Prefer the inventory's option (drop `--remediate` under `--unattended`).

**M2 (Adzic): an `ask` and the live-check contradict.** WC-3 lets a worker `ask` the coordinator once instead of ending blocked (`SPEC:61`). AC-2.2 and step 2 of `SPEC:181` require `agentWait` never to be non-null and the outcome to be `failed` with a `blocked` contract (`SPEC:200`). Whether `agentWait` is set during an `ask` is not stated (`CAPS:52`, `CAPS:129` only describe prompts a person answers). The test passes only if the worker picks the contract path.

**M3 (Crispin): SA-2 and AC-C1 can collide with the contract file.** SA-2 allows an Orca mention "inside the contract file" (`SPEC:147`), and the contract file is `src/superclaude/core/WORKER-CONTRACT.md` (`SPEC:52`), which AC-C1's grep covers (`SPEC:172`). The text `orca orchestration ask` would make AC-C1 print a line. `SPEC:51` also says unattended mode "names no Orca command" while WC-3 names the preamble's `ask`. State whether the contract file may contain the literal command, and exclude it in AC-C1 if so.

**M4 (Wiegers): unattended with no output directory is unspecified.** WC-4 assumes the coordinator passed the directory (`SPEC:62`); many 3.2 rows add an optional `--output` (`SPEC:99-111`). If `--unattended` is passed without it, there is no stated behaviour (default path, or `blocked`). This is a missing restriction, not a stated text that does harm.

**M5 (Adzic): AC-C5 vs adding a flag to a Usage line.** AC-C5 passes only if no existing command line is removed or changed (`SPEC:176`). Adding `--unattended` to a one-line Usage block or to an `argument-hint` frontmatter value changes an existing line, unless a new line is added as `cmd/spec-panel.md` does with a second usage line. The spec does not say which form to use (SA-4, `SPEC:149`).

**M6 (Cockburn): pr-submit is counted as worker-capable though the recommended decision makes it coordinator-side.** `SPEC:76` counts it among the 27 and `SPEC:139` conditions it on D3, while D3 recommends (a) (`SPEC:240`). The 27/6 split is therefore 26/7 under the recommendation. State the count under the recommended answers.

**M7 (Nygard): evidence for the decision is stated inconsistently.** E3 cites `invocation_method: "skill-direct"` as proof the approach worked (`SPEC:23`), and `INV-A:13` and `INV-A:35` call the adversarial run "proven as a direct Orca-worker skill call". Section 1.4 then says only the nested (Agent-tool subagent) route was shown (`SPEC:43`, `CAPS:156`). The spec should say what `skill-direct` meant and drop it from E3 if it does not show a direct run. This does not change the recommendation, because P0 tests it (`SPEC:158`).

**M8 (Crispin): `gh api ... --jq length` in AC-2.4 is capped by default pagination** (`SPEC:202`), so a count may be unchanged when a 31st comment is added. Use `--paginate` or compare ids. Not verifiable against the Orca or gh docs here, so UNVERIFIED as a defect.

**M9 (Wiegers): undefined labels F-1, F-2 and SA-1 reference.** `SPEC:62`, `SPEC:76`, `SPEC:159` use "(F-1)" and "(F-2)" without defining them; they look like earlier review finding ids. A reader of the final spec cannot resolve them. `SPEC:122` uses "(SA-1)" correctly.

### Minor notes
- `SPEC:11` says the section-3 source lines were re-read and found "as cited", but `sk/sc-pr-submit-protocol/SKILL.md:37-39` (also `INV-B:90`) differs from the installed-copy lines `:47-49` in `CAPS:161`. Different copies, so probably consistent, but the spec does not say which file it cites. UNVERIFIED.
- `SPEC:285` item 14 (citation-check outcome) is process narration in a spec; harmless.
- `SPEC:59` WC-1 says a prompt must fall back "well inside" 60 s; the evidence tested a 45 s limit (`CAPS:49`). Consistent but the margin is not quantified.

## Guard Condition Boundary Table
Guards in the spec: the `--unattended` switch, the heartbeat and wait bounds (WC-10), the nesting depth (R1/D5), the circuit breaker at 3 failures (`CAPS:80`, `CAPS:116`), and task confidence below 0.70 (`SPEC:121`). Classes that cannot occur for a guard are omitted with one line.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `--unattended` set | WC-2, SPEC:60 | Zero/Empty (set, no output dir) | `--unattended` without `--output` | true | not stated (M4) | GAP (Medium) |
| `--unattended` set | WC-2, SPEC:60 | Typical | flag plus `--output <dir>` | true | gates resolve per section 3; contract written | OK |
| `--unattended` set | WC-2, SPEC:60 | Sentinel Value Match | a command whose own argument is the string `--unattended` (quoted content) | true or false | not stated (`command.md:459` handles it for spec-panel only) | GAP (Medium) |
| `--unattended` set | SA-1, SPEC:146 | Legitimate Edge Case | person passes it by hand in a plain session | true | behaves as unattended; SA-1 only covers its absence | OK |
| report path known before dispatch | WC-4, SPEC:62 | Zero/Empty (path has no id yet) | workflow pre-creation stop | n/a | no path (B2) | GAP (blocking) |
| wait of at most 4 min | WC-10, SPEC:68 | Maximum/Overflow | poll script longer than 4 min | false | confirm per iteration; poll runtime UNVERIFIED (`SPEC:283`) | GAP (Medium, carried as UNVERIFIED) |
| nesting depth 1 | R1, SPEC:33 | Maximum/Overflow | worker calls `worker-start` | refused | `nested_worker_depth_exceeded` (`CAPS:99`) | OK |
| circuit breaker | WC-6, SPEC:64 | One/Minimal and Maximum | 3 failed starts for one Task | true at 3 | Task failed (`CAPS:80`); a worker `failed` report does not count | OK |
| confidence below 0.70 | task row, SPEC:121 | Sentinel Value Match | exactly 0.70 | false | not stated in the spec (it inherits the command's boundary, UNVERIFIED) | GAP (Medium) |
Classes left out: Zero/Empty for the depth and breaker guards (a depth of 0 is the coordinator, `CAPS:97`, and a count of 0 failures needs no behaviour).

Pipeline Dimensional Analysis: not triggered. The spec describes a coordinator-to-worker task flow, not a multi-stage data flow whose item counts diverge. State Variable Registry: not required (`--focus correctness` not active).

## Expert panel notes (critique mode)
=== REQUIREMENTS ANALYSIS ===
- Wiegers: requirements are numbered, owned and evidenced (WC-1 to WC-12), and testable by the 7.2 live check. Gaps: B1, M4, M9.
- Adzic: each gate has a concrete example in 7.2 and 7.3; M2 and the missing `--unattended`-without-output example are the exceptions.
- Cockburn: the primary actors (coordinator, worker session, command, person) are separated cleanly in `SPEC:55-70`; B2 breaks the "known before dispatch" goal for one command.
=== ARCHITECTURE ANALYSIS ===
- Fowler: Orca-on-top with commands as units has no internal Orca call (SA-2) and one shared contract file, a clean boundary; B1 and M3 are the places the boundary text contradicts itself.
- Nygard: failure outcomes (blocked, partial, failed) map to the two Orca outcomes (WC-5); M1 is the one place a failure path may continue into more work.
- Newman and Hohpe: the report-file hand-off is a pull contract; Orca does not verify the file (`CAPS:79`), and the spec correctly makes the coordinator open it (`SPEC:62`).
- Whittaker: sequence attack on workflow (B2) and sentinel attack on `--unattended` (guard table) are the two real breaks found; the rest of the spec's guards hold.

## Follow-up candidates
M1, M2, M3, M4, M5, M6, M7, M8, M9 and the minor notes above. Question for the user (not asked, since this sandbox has no user): open an issue for these follow-up candidates? No issue was created and nothing was edited except this file.

## Reviser brief
Blocking finding ids: B1, B2. Revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Leave Medium and minor findings alone.

verdict: FAIL
