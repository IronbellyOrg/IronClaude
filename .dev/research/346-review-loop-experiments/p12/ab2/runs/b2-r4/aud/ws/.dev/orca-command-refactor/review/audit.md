review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md (`/sc:spec-panel --mode critique --focus requirements,architecture`)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `c9e2ff995f731358d2c486eecbe202f9c810da58a248e59a7c693464e08d5a7b`
- baseline: missing (first review, no `--re-review`/`--baseline`); prior report: none
- reviewer model: claude-sonnet-5-5
- scope: first review of the whole document (labelled whole-document audit), FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`
- citation basis: only `.dev/orca-command-refactor/README.md` and `inventory/*.md` could be read. Every `cmd/…` and `sk/…` line the spec cites is UNVERIFIED here; I checked it only through what the inventories quote. Spec citations of the form `INV-A:n`, `INV-B:n`, `CAPS:n` were checked against the inventories where noted. `S:n` below = line n of the candidate.
- coverage: all 285 lines of the candidate; panel order Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower; requirements and architecture buckets expanded, other experts folded in. Not covered: the sandbox `command.md` internals beyond the report format; the ~340 source citations (UNVERIFIED).
- brief clauses overridden: none.

## Spot-check of the spec's own numbers
- 43 commands = 21 + 22 (`S:76`): `inventory/commands-a.md:1` ("21 SC commands"), `inventory/commands-b.md:1` ("22 SC commands"). Held.
- 10 ready / 27 needs-change / 6 coordinator-only (`S:76`): I counted section 3.1 (10 rows, `S:83-92`), section 3.2 (27 rows, `S:99-125`), section 4 (6 rows, `S:132-137`). It matches the inventories' split (A: 5 ready, 13 change, 3 coordinator at `commands-a.md:86-92`; B: 5 ready, 14 change, 3 coordinator at `commands-b.md:285-299`). Held.
- Phase rows cover 9+11+4+3 of the 27 (`S:158-162`). Held. See M-6 for the 3 ready commands no phase row lists.
- CAPS cites checked and held: `CAPS:44-45` (60 s readiness), `CAPS:52`/`129` (waiting is healthy), `CAPS:64`, `CAPS:73`, `CAPS:76`, `CAPS:80`, `CAPS:97-99,103` (depth 1; enforcement call sites UNVERIFIED, as the spec says), `CAPS:145`, `CAPS:147-151`, `CAPS:155,158-161`, `CAPS:178-188`.

## === REQUIREMENTS ANALYSIS ===

Blocking findings: none. Grading check applied to each finding below (`document_review_loop_prompts.md:31`): none yields a sentence of the form "an implementer who follows the stated text builds X, and X is wrong because Y" that holds with no further assumption. Each needs a guess about which reading an implementer picks, or is a requirement the document never states. All are Medium (follow-up candidates) even where the expert label would be MAJOR.

### M-1 (Medium; Wiegers/Crispin; High priority) Common check AC-C1 and the Orca text the spec itself asks for can contradict, and the check as written may pass vacuously
- AC-C1 (`S:172`) requires `grep … orca(-ide)? (orchestration|worktree|terminal|agent)` over `src/superclaude/core` to print nothing, excluding only `skills/ccsession-tag/`. SA-2 (`S:147`) allows "an example of a caller's question channel inside the contract file", and P0 adds `WORKER-CONTRACT.md` plus an Orca section in `HOW-WE-WORK.md`, both under `src/superclaude/core` (`S:158`, `S:150`). `S:25` records `HOW-WE-WORK.md` has 0 Orca mentions today (UNVERIFIED, not in the workspace).
- Wrong outcome if the implementer writes a lowercase `orca orchestration ask` example (the natural wording of a "question channel"): P0 can never pass its own common check. It needs the guess that the example is written in that form, so Medium.
- Separately, the table cell writes the pipes as `\|` (`S:172`). Copied literally into ERE, `\|` is a literal pipe, so the alternation matches nothing and the check passes on any content. Rendered Markdown hides this.
- Recommendation: state which Orca words the core files may contain (or exempt `WORKER-CONTRACT.md`/the Orca section from AC-C1), and put the command in a fenced block without table escapes. Quality impact: restores a mechanical SA-2/WC-8 gate.

### M-2 (Medium; Wiegers; Medium priority) Dangling finding ids F-1 and F-2
- `F-1` and `F-2` are used as the reason for exceptions at `S:52, 62, 73, 92, 159, 195, 196, 198` but defined nowhere in the candidate or the inventories (`grep -n "F-1\|F-2"` over `inventory/` returns nothing). The surrounding sentences state the behaviour (workflow mints its own `<id>`; `/sc:load` writes no contract), so an implementer can still act, but the ids point at a review artifact the reader cannot open (`review/disposition.md` is not in the workspace; UNVERIFIED).
- Recommendation: replace the ids with the stated rule or add a one-line legend.

### M-3 (Medium; Wiegers/Adzic; High priority) The contract path is not computable for several commands, which WC-4 and check 7.2 step 3 require
- WC-4 (`S:62`) says the path is "known before dispatch" and gives rules only for `--output`/`--output-dir` directories, `--output` files, and rows that name a path. Section 3 rows for build, test, cleanup, improve, design, index, document, business-panel, explain, analyze say only "add a report path" or "add an output path" (`S:99-111`), without a flag name; `/sc:cleanup-audit` and `/sc:index-repo` have fixed locations (`.claude-audit/…`, `PROJECT_INDEX.md`, `S:85-86`) and P1 only "names" the report, not a contract path. 7.2 step 3 (`S:182`) requires the worker's report path to equal "the WC-4 contract path".
- The implementer must invent the flag name and the contract path rule per command; two implementers can differ and the coordinator brief template (`S:73`) cannot be written. Requirement not stated, hence Medium.
- WC-11 (`S:69`) says default output paths carry a timestamp or slug, yet the same spec accepts fixed `.claude-audit` and `PROJECT_INDEX.md` with a note (`S:85-86`). The two texts do not reconcile for parallel workers in one worktree.
- Recommendation: one sentence per row naming the flag (`--output` everywhere) and, for the two fixed-location commands, the contract path.

### M-4 (Medium; Wiegers; Medium priority) WC-1 has no delivering phase and no acceptance check
- WC-1 (`S:59`) is owned by "Launch setup, not commands" and cites the 30 s fallback evidence (`EVIDENCE.md:45,56`, via spec; UNVERIFIED here). No phase in `S:158-162` delivers it and no AC in section 7 tests it beyond 7.2 step 1 `state: ready`. The readiness failure is the one outage the README names as evidence (`README.md:14`).
- Recommendation: assign it to P0 and add a check, or move it to non-goals as someone else's responsibility.

### M-5 (Medium; Adzic/Crispin; Medium priority) AC-2.2 asserts one outcome of a path WC-3 leaves optional
- WC-3 (`S:61`) lets the worker session `ask` the coordinator instead of finishing as blocked ("may"). AC-2.2 (`S:200`) passes only on `worker_done --outcome failed`, `status: blocked`. A conforming worker that asks and gets an answer fails the acceptance check.
- Recommendation: AC-2.2 should brief the worker not to `ask`, or accept an `ask` event followed by either outcome.

### M-6 (Medium; Cockburn; Low priority) Three ready commands belong to no phase
- brainstorm, init-lite and workflow have "None" in the small-fix column (`S:84, 87, 92`) and appear in none of the phase command lists (`S:158-162`), yet AC-1.1 (`S:195`) requires an `## Unattended mode` section for every command in 3.1 and 3.2 except load, and P1 scope says the flag is accepted by every such command (`S:159`). The phase table is therefore not the authority for who gets the section.
- Recommendation: add the three to the P1 list.

### M-7 (Medium; Whittaker; Medium priority) Authorization and mode-switch edge cases are unspecified
- Sentinel/collision: `--unattended` is a plain token; the spec says nothing about the token appearing inside quoted content, an input document, or a coordinator-only command (`S:128` says section 4 commands "get no `--unattended` mode" but not what they do when handed it). The installed `command.md:459` already adds the rule "standalone argument token outside any quoted argument" for spec-panel; the spec does not carry it into WC-2 (UNVERIFIED whether the spec should).
- WC-9 (`S:67`) and D4 (`S:245`) rest on a brief quoting the user's instruction, but no command can verify that; the flag alone is the authorization. That is an accepted trust model, but it is not stated as one.
- Recommendation: add one line each to WC-2/WC-9.

## === ARCHITECTURE ANALYSIS ===

### M-8 (Medium; Fowler/Nygard; Medium priority) Tasklist Stage 10.5 resolution rests on unstated semantics and contradicts the inventory's recommendation
- The tasklist row (`S:122`) has Stage 10.5 pass `--unattended` to each reflect so the "headless rule applies", and says the fan-out is "inside Claude Code's nesting limit, `INV-A:14`". The headless rule keys on `claude --print` (`commands-b.md:297`, decision row on reflect) and what it does to a `--remediate` offer (auto-accept, so remediation runs unattended inside subagents) is not stated. `commands-b.md:215` recommended running reflect without `--remediate` and at the worker's top level instead; `commands-b.md:209` records who answers the offer in a subagent as UNVERIFIED. The nesting claim is an inference from `commands-a.md:13` (three layers), not a measured depth.
- Wrong outcome needs a guess (whether auto-accept starts corrective workflow packages nobody asked for), so Medium.
- Recommendation: state what the headless path does on `--remediate`, or take the inventory's option of dropping `--remediate` under `--unattended`.

### Architecture notes that held
- The central decision (Orca on top, commands unchanged units) is consistent with README `:6`, with R1-R5 (`S:33-37`) and with `CAPS:97-103`; the spec correctly states its own evidence gap (`S:42-45`, direct-route run unobserved, `commands-b.md:323` equivalent text) and puts the live smoke runs first (`S:158`). No contradiction found between section 1, WC-7/WC-8 and section 8.
- WC-5 maps `partial` to `succeeded` and records the choice (`S:263`); consistent with `CAPS:73`.

## Guard Condition Boundary Table (triggered: the spec contains thresholds and boolean guards)
| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| unattended switch | WC-2 `S:60` | Zero/Empty (flag absent) | absent | false | standalone behaviour unchanged, SA-1 `S:146` | OK |
| unattended switch | WC-2 `S:60` | Sentinel Value Match (token inside quoted content or on a section-4 command) | `--unattended` as data | undefined | not specified | GAP (M-7, Medium) |
| heartbeat wait cap | WC-10 `S:68` | Typical | one wait of 3 min | true | allowed | OK |
| heartbeat wait cap | WC-10 `S:68` | Legitimate Edge Case | exactly 4 min / single tool call 5 min | boundary | "at most 4 minutes" split rule; a single un-splittable tool call is covered only for pr-submit (UNVERIFIED poll runtime, `S:114`) | OK |
| confidence gate | task row `S:121` | Legitimate Edge Case | exactly 0.70 | false | "below 0.70" blocks; 0.70 proceeds | OK |
| readiness limit | WC-1 `S:59` | Maximum/Overflow | prompt fallback above ~45 s | fails | stated as evidence only, no owner or check | GAP (M-4, Medium) |
| nesting depth | R1 `S:33` | Typical (depth 1) | worker calls worker-start | refused | WC-8 forbids; enforcement call sites UNVERIFIED (`CAPS:103`) | OK |
| status enum | WC-4 `S:62` | Zero/Empty (no report exists) | none | n/a | WC-5 maps to `failed` | OK |
| status enum | WC-4 `S:62` | Legitimate Edge Case (workflow stop before `<id>` exists) | no directory | n/a | no contract, `failed` under WC-5, `S:92` | OK |
| contract path | WC-4 `S:62` | Zero/Empty (command with no output flag or fixed dir) | no `--output` | undefined | "add a report path", flag unnamed | GAP (M-3, Medium) |
| circuit breaker | `CAPS:80` via WC-6 | Maximum/Overflow | 3 consecutive failures | Task failed | spec says a worker's own failed report does not trip it | OK |
Classes left out for the guards above: One/Minimal for the switch and status guards, because a boolean/enum has no distinct minimal case.

## follow-up candidates (Medium and minor; none blocking)
Medium: M-1 to M-8 above.
Minor notes:
- m-1: `S:65` cites `sk/sc-pr-submit-protocol/SKILL.md:37-39` while `CAPS:161` quotes the same rule at lines 47-49 of `/home/coder/.claude/skills/…/SKILL.md`, and `commands-a.md:13` cites 37-39 in the repo copy. Two copies, both plausible; UNVERIFIED which is current.
- m-2: AC-1.4 (`S:198`) is a `grep -n` whose pass condition ("names one fixed path") is a judgment, not an exit code.
- m-3: Section 3 header counts pr-submit, post-release and implement among the 27 needing change, but under the recommended D2/D3 (`S:234, 240`) pr-submit needs no change; the count is a classification, not a work list.
- m-4: The sandbox `command.md:460-461` already defines `--report-dir` and `<report-dir>/return-contract.yaml` for spec-panel, while the spec's spec-panel row says "add `--output`" (`S:120`); the spec's WC-4 path rule differs from that installed command. UNVERIFIED which governs.
- m-5: The sc-adversarial, cleanup, improve and other "rollback UNVERIFIED" notes (`S:103, 110`) are properly flagged; no action.

Open question for the user (asked once per loop): open an issue for the follow-up candidates above? No issue was created.

Reviser brief: none; no blocking finding is open.

verdict: PASS
