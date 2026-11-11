review: 1 of 3

# /sc:spec-panel critique, round 1

- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- Candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Baseline: missing (first review; no `--baseline` given)
- Mode: critique. Focus: requirements, architecture. Format: structured.
- Reviewer model: claude-haiku-5-5
- Prompt: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full).
- Scope of this file: one reviewer's report. The FIRST-REVIEW prompt asks for three fresh-context reviewers and a coordinator MERGE. This worker has no way to start fresh-context reviewers, so the coordinator must run two more reviews and the MERGE. The verdict below is this reviewer's verdict only, not a merged verdict.
- Evidence limits: `.dev/orca-command-refactor/inventory/*.md` and the workspace README are the only files checked. Citations to `src/superclaude/...`, `.dev/evals/...`, `.dev/codegraph-migration/...`, `~/.claude/...` and the external docs are UNVERIFIED here. Spec line numbers are of the candidate as read; `INV-A:n`, `INV-B:n`, `CAPS:n` are lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`.

## Summary

Blocking findings: 3 (RQ-1, RQ-2, AR-1). Medium findings: 20 (follow-up candidates). Minor notes: 4.
The spec's inventory citations I could check resolve to the cited content (for example `INV-A:66`, `INV-A:107`, `INV-B:179`, `CAPS:34`, `CAPS:52`, `CAPS:68`, `CAPS:73`, `CAPS:79`, `CAPS:80`, `CAPS:115`, `CAPS:125-126`, `CAPS:130`, `CAPS:155`, `CAPS:161`, `CAPS:188`). The exception is M-6, where a claim is cited to a line the inventory itself marks UNVERIFIED.

=== REQUIREMENTS ANALYSIS ===

### RQ-1 (BLOCKING). WC-3 lets a coordinator's reply become a gate answer, which contradicts the implement Ruling rule (D2) and the outward-action rule (D4)
- Severity: MAJOR, graded blocking because two stated texts contradict.
- Expert: Karl Wiegers (lead), Gojko Adzic, Alistair Cockburn.
- Text: WC-3 says that when "a gate would resolve as blocked ... the session may instead ask the coordinator once ... then re-invoke or resume the command with the answer as a flag" (`spec:61`). It has no exception for the implement Ruling or for outward flags.
- Conflicts: the implement row says the Ruling rule "is unchanged" and that the halt ends in a blocked contract (`spec:109`). D2 option (a) recommends that a person gives the Ruling and the worker ends `failed` (`spec:234-236`). AC-4.1 expects that "the ledger records no Ruling unless D2 allows a relayed one" (`spec:208`). The rule behind D2 is that "another agent's message ... [is] not acceptance" (`INV-A:66`, quoting `refs/qa.md:238`). D4 option (a) requires that the user's own instruction, quoted, authorizes each outward flag (`spec:245-246`).
- Grading sentence: an implementer who follows WC-3 (`spec:61`) as written may send the implement Ruling question to the coordinator; nothing in the candidate stops the coordinator's reply from being recorded as the Ruling, and `qa.md:238` forbids exactly that. A second case: the coordinator answers "yes" to the auggie-review posting offer, the worker re-runs with `--post-pr` (WC-9 is met, since the flag is on the command line, `spec:67`), and D4(a) is broken because no user instruction was quoted.
- Recommendation: add an exclusion to WC-3: a gate that guards a Ruling, an outward action, or a safety boundary may never be answered by a coordinator reply. Such a gate resolves as blocked. Make the implement row and D2 cite WC-3 by name.
- Priority: High. Quality impact: high on the safety boundary of `/sc:implement` and on outward actions.

### RQ-2 (BLOCKING). The P0 phase cannot run the live check it is gated on
- Severity: MAJOR, graded blocking because two stated texts contradict.
- Expert: Karl Wiegers (lead), Gojko Adzic.
- Text A: P0 is "no command edits" and only adds the contract, the routing guide and a test file (`spec:158`). `--unattended` is first added in P1 (`spec:159`).
- Text B: the live check's step 1 must use "the brief per section 2.3" (`spec:180`). Section 2.3 says the brief carries "the exact command line including `--unattended`" (`spec:73`).
- Text C: the ready commands' "Brief must pass" column lists no `--unattended` (`spec:83-92`), and section 3.1 says they "run as workers now if the brief uses the stated flags" (`spec:79`).
- AC-0.4 then requires steps 1-3 and 5-7 to pass for `/sc:troubleshoot`, `/sc:workflow` and `/sc:adversarial` (`spec:194`).
- Grading sentence: an implementer who follows `spec:180` for P0 puts `--unattended` on the `/sc:troubleshoot` line. P0 adds no such flag (`spec:158`), so the run is not unattended, and AC-0.4 passes a decision test that never exercised the WC-2 and WC-4 behaviour that the decision depends on.
- Recommendation: state the P0 brief for ready commands without `--unattended` and say that the P0 run tests only the default path. Or move the P0 live check to after the first P1 command. Make `spec:73` and `spec:79` say the same thing.
- Priority: High. Quality impact: high on phase gating (the decision in section 1 is tested by this run).

### M-1 (Medium). WC-4 says the report path is known before dispatch, but some report paths are generated at run time
- Expert: Wiegers.
- Text: "the report path is known before dispatch (WC-4)" (`spec:73`); the contract is `<output-dir>/return-contract.yaml` (`spec:62`).
- Workflow writes to `.dev/tasks/to-do/<id>/return-contract.yaml` (`INV-B:52`, `INV-B:272`) and its brief passes only `--handoff none` (`spec:92`). The `<id>` is created by the command. Research writes a timestamped file (`spec:116`, `INV-B:132`). Adversarial's contract location is inconsistent on disk (`INV-A:60`), and `spec:83` admits that the filename is "not fixed".
- Grading: needs a guess that the `<id>` and timestamp are not coordinator-supplied; the candidate does not say whether they are.
- Recommendation: state, for each command in 3.1 and 3.2, whether the contract path is fixed, passed by a flag, or returned by the run. For run-generated paths, require the worker to report the path with `status` in the contract, and make the coordinator read it from there.
- Priority: Medium. Quality impact: medium (the coordinator cannot check the report before dispatch).

### M-2 (Medium). WC-2 has no requirement about tool-permission prompts
- Expert: Wiegers.
- Text: WC-2 says "No person-blocking step in unattended mode" (`spec:60`). The candidate contains no mention of "permission" (checked by grep of the candidate). A worker that runs Bash, Write or Edit may hit a tool-permission dialog, which only a person can answer. That dialog is a person-blocking step that WC-2's list does not cover.
- Grading: needs an assumption about the worker's permission mode, which the candidate does not state.
- Recommendation: add a requirement and a brief field for the worker's permission mode (or the allow-list it relies on), and a §7.2 check that no permission dialog appears (the `agentWait` check at `spec:181` may catch it, but the spec does not say so).
- Priority: High. Quality impact: medium to high (silent stall).

### M-5 (Medium). WC-10 cannot be met for Agent-tool calls
- Expert: Adzic (measurability), Fowler.
- Text: WC-10 says a step that "blocks a single tool call for longer than 5 minutes ... must be split into waits of at most 4 minutes" (`spec:68`). An Agent-tool fan-out is a tool call that a command cannot split. The ready and near-ready commands with long Agent waves are adversarial, tdd and cleanup-audit (`INV-B:221`, `INV-A:42`).
- Recommendation: state what WC-10 requires for Agent-tool calls (for example, a bounded fan-out or a split into several calls), or state that heartbeats cannot be sent during them and what the coordinator should do.
- Priority: Medium. Quality impact: medium.

### M-7 (Medium). WC-9 uses undefined terms
- Expert: Wiegers.
- Text: "pushes, opens a PR, posts to GitHub, installs, provisions or calls a paid external run" (`spec:67`). "Paid external run" is undefined. Research's web calls (`INV-B:38`) and cli-eval's model runs (`spec:104`) are the test cases, and the candidate does not say which is in scope.
- Recommendation: define "paid external run" by a list of commands and flags, or by the cost-bearing call type.
- Priority: Medium. Quality impact: medium.

### M-8 (Medium). WC-7 has no check, and AC-0.4 claims one
- Expert: Cockburn (acceptance criteria).
- Text: AC-0.4 says "each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript)" (`spec:194`). Step 5 passes when no `AskUserQuestion` appears in the transcript (`spec:184`). It does not test for a subagent wrapper.
- Recommendation: add a transcript check for the top-level invocation (for example, the first tool call is the command's Skill or Bash call in the top-level session). Or remove the "verified in the step-5 transcript" claim.
- Priority: Medium. Quality impact: medium.

### M-9 (Medium). The SA-2 grep in AC-C1 has gaps
- Expert: Cockburn.
- Text: AC-C1 (`spec:172`) checks `commands`, `skills`, `agents` and `core`, and matches `orca(-ide)? (orchestration|worktree|terminal|agent)` in lower case. The candidate itself lists the plugin mirror `plugins/superclaude/commands/` as unresolved (`spec:279`, UNVERIFIED item 8), and AC-C1 does not cover it. The guides use upper-case `ORCA orchestration ...` (`CAPS:63`), and the match is case-sensitive, so an upper-case call passes the check. `orca-cli` and other subcommands (`status`, `check`, `send`) are not matched.
- Recommendation: add case-insensitive matching, the plugin mirror path, and the `orca-cli`, `ORCA_TERMINAL_HANDLE` and `orca status|check|send` forms.
- Priority: Medium. Quality impact: medium (SA-2 could be violated while AC-C1 passes).

### M-10 (Medium). SA-1 and the roadmap and save rows can be read two ways
- Expert: Wiegers.
- Text: SA-1 says that without `--unattended`, "every prompt ... stays as it is today" (`spec:146`). The roadmap row says the "Resume? [Y/n]" prompt "is replaced by the explicit resume flag" (`spec:118`), and the save row says "write only the per-session keys" (`spec:119`). Both sit in the column headed "Unattended-mode gate resolution (WC-2)" (`spec:97`), so they probably apply only under `--unattended`. The row text does not say so. A plain session reading the row could drop the prompt.
- Recommendation: put "under `--unattended`" in both rows.
- Priority: Medium. Quality impact: medium (a standalone prompt could disappear).

### M-13 (Medium). WC-1's fallback bound is not measurable
- Expert: Wiegers.
- Text: "fall back on its own well inside the readiness limit (default 60 s)" (`spec:59`). The evidence in the candidate (`spec:59`, citing `EVIDENCE.md:45,56`, quoted at `CAPS:49`) says a fallback at about 45 s fails again. The band between about 45 s and 60 s has no stated rule, and "well inside" is undefined.
- Recommendation: state a numeric fallback (for example 30 s, the value the evidence passed with) and a maximum.
- Priority: Medium. Quality impact: medium.

### M-14 (Medium). WC-2 has no rule for a gate that is in no section 3 row
- Expert: Wiegers.
- Text: "Each gate resolves one of three ways, listed per command in section 3" (`spec:60`). Section 3 lists gates per command, but nothing says what an unlisted gate does in unattended mode. Inventory A notes that several commands have gates whose behaviour is unverified (`INV-A:113`).
- Recommendation: add a default for unlisted gates: "blocked".
- Priority: Medium. Quality impact: medium.

### M-15 (Medium). `/sc:cli-eval run` has no rule for an unknown suite name
- Expert: Cockburn.
- Text: `run` "requires `--suite` and the safety flags in the brief, else blocked" (`spec:104`). A `--suite` with a name that does not exist is not covered. The gate in `INV-A:44` (suite menu) would resolve as a stop in standalone mode, but the unattended rule is not stated.
- Priority: Low to medium. Quality impact: low.

### M-16 (Medium). Spec-panel's `target_release` source is inconsistent
- Expert: Cockburn.
- Text: spec-panel requires `target_release` "as a flag for TDD inputs, else blocked" (`spec:120`). Inventory B says the command asks for it when the TDD's frontmatter is empty (`INV-B:179`). The case in which frontmatter has a value and no flag is given is not stated. The command file itself is outside the candidate's evidence (UNVERIFIED).
- Priority: Medium. Quality impact: low to medium.

### M-18 (Medium). WC-6 does not say how a retry avoids overwriting a non-resumable command's output
- Expert: Wiegers.
- Text: WC-6 requires that "a command either resumes ... or ... writes each run into a fresh output directory" (`spec:64`). Section 2.3 (`spec:73`) gives the coordinator no rule for a retry, so a retry brief may reuse the first `--output`. For brainstorm, reflect and adversarial the contract is fixed inside `--output` (`spec:84`, `spec:88`, `spec:83`), so a reused directory overwrites the first attempt.
- Recommendation: add a rule to section 2.3: a retry of a non-resumable command gets a new `--output`.
- Priority: Medium. Quality impact: medium.

### M-19 (Medium). The coordinator-only count changes if D3 is recommended
- Expert: Cockburn (consistency).
- Text: the split is "10 ready, 27 needing a change and 6 coordinator-only" (`spec:75`). Pr-submit stays in 3.2 (`spec:114`), and section 4 says only that it "stays a worker candidate only if ... D3" is accepted (`spec:139`). D3's recommended option (a) puts pr-submit with the coordinator (`spec:240`). Under that recommendation the split is 10/26/7, which section 4 does not show.
- Recommendation: state both counts, or move pr-submit to section 4 under the recommendation.
- Priority: Low to medium. Quality impact: low.

=== ARCHITECTURE ANALYSIS ===

### AR-1 (BLOCKING). Two ready verdicts keep fixed output paths, which breaks WC-11 in the default shared worktree
- Severity: MAJOR, graded blocking because two stated texts contradict.
- Expert: Martin Fowler (lead), Sam Newman.
- Text: WC-11 says "Two workers in one worktree must never write the same file. Default output paths carry a timestamp or the slug the coordinator passes" (`spec:69`). The brief places workers in the current worktree by default (`CAPS:115`). Section 3.1 nonetheless marks cleanup-audit "ready" with a fixed output directory (`spec:85`, `INV-A:42`, and the verdict basis at `INV-A:107`: fixed `.claude-audit/pass1-summary.md`), and index-repo "ready" with `PROJECT_INDEX.md` at a location that is itself UNVERIFIED (`spec:86`, `INV-A:53`). Cleanup-audit's `progress.json` is also fixed (`INV-A:42`). The row's note "one audit per worktree at a time (WC-11)" (`spec:85`) is not a rule in section 2.3 (`spec:73`) or in the brief template.
- Grading sentence: an implementer who follows `spec:85` and `spec:86` dispatches two cleanup-audit or index-repo workers into the default shared worktree, and both write the same `.claude-audit/pass1-summary.md` or `PROJECT_INDEX.md`, which WC-11 says must never happen. Neither the brief template nor any check stops the second dispatch.
- Recommendation: move both rows to "needs change" until the output path takes a per-run slug, or add a coordinator rule (one such Task per worktree at a time) to section 2.3 and to AC-C1 or a new check.
- Priority: High. Quality impact: high (silent clobbering of shared state).

### M-3 (Medium). A silent stall and a blocked-retry loop have no coordinator rule
- Expert: Michael Nygard (failure modes).
- Text: section 7.2 step 3 waits on `check --wait` "until worker_done arrives" (`spec:182`), with no timeout rule. A worker that ends its turn with no `worker_done` is the most likely failure (`spec:44`, "silent stall"). Orca's guidance says the wait ends only on positive proof, including "a transcript whose final agent turn sent no worker_done" (`CAPS:126`). The spec does not adopt that rule. Orca's circuit breaker counts `worker-start` failures, but "a worker's own failed report does not" count (`CAPS:80`, `CAPS:116`). WC-5 maps `blocked` to `failed` (`spec:63`), so a coordinator that retries a blocked worker gets no breaker, and the spec does not forbid that retry.
- Recommendation: add to section 2.3: a silent end of turn is a stall; the coordinator reads `worker-show`, then escalates or releases with the proof `CAPS:126` names. Add: a `blocked` outcome is not retried automatically.
- Priority: Medium. Quality impact: medium to high (indefinite waits, unbounded retries).

### M-4 (Medium). Dependents of a `partial` or FAIL-verdict worker can start with no gating rule
- Expert: Hohpe (message semantics), Nygard.
- Text: `partial` and an audit with verdict FAIL both map to `succeeded` (`spec:63`), and the decision row says so (`spec:263`). Orca's ready view is built from Task status, and Orca does not start Tasks by itself (`CAPS:34`), so once a worker is settled as succeeded its dependents become startable. Section 2.3 asks the coordinator to open the report (`spec:73`) but does not tie the next start to the report's status.
- Recommendation: state that a dependent Task starts only when the contract status is `succeeded`, and say how a `partial` is handled.
- Priority: Medium. Quality impact: medium.

### M-6 (Medium). Nested reflect inside tasklist is cited to an inventory line that marks it UNVERIFIED
- Expert: Fowler.
- Text: the tasklist row says the reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`" (`spec:122`). `INV-A:14` is the documentation statement that nesting is allowed up to three layers. Inventory B says that whether reflect inside subagents works is UNVERIFIED (`INV-B:210`), and lists it as open item 1 (`INV-B:314`) and item 8 (`INV-B:322`). The spec's UNVERIFIED list (`spec:272-285`) does not include it.
- Recommendation: mark the tasklist fan-out UNVERIFIED in section 3.2 and the UNVERIFIED list, and add a P2 check for it.
- Priority: Medium. Quality impact: medium (the verdict depends on it).

### M-11 (Medium). `--unattended` carries several meanings and the coordinator must know each command's flags
- Expert: Fowler (interface segregation), Newman (contracts).
- Text: one flag stands for no prompts, no outward defaults, a fixed report and gate resolutions (`spec:51`, `spec:60`, `spec:146`). Section 2.3 has the coordinator write each command's full flag list into the brief (`spec:73`), and section 3 is the only catalogue (`spec:75`). There is no machine-readable catalogue, and P0's test checks only that the section exists (`spec:195`).
- Recommendation: either a per-command flag catalogue in a file the test reads, or per-concern flags. State which.
- Priority: Medium. Quality impact: medium (coordinator drift).

### M-12 (Medium). The scope of reflect's auto-accept under `--unattended` is not stated
- Expert: Newman (service boundary), Fowler.
- Text: the reflect row says "under `--unattended`, make `--remediate` follow the existing headless auto-accept rule" (`spec:88`). SA-6 says the rule is reused (`spec:151`). The candidate does not say which remediations are auto-accepted, and inventory B describes the rule as keyed to `claude --print` (`INV-B:109`).
- Recommendation: name the auto-accepted register classes and state that an Orca worker is not headless.
- Priority: Medium. Quality impact: medium (automatic code changes without a person).

### M-17 (Medium). WC-4 has no fallback when `<output-dir>` cannot be created or written
- Expert: Nygard.
- Text: the contract is written "on every outcome ... including stops before any other output exists" (`spec:62`). If the directory cannot be created, the contract cannot be written, and the candidate has no rule for this. WC-5 treats "no report exists" as failed (`spec:63`), so the outcome is still stated, but the coordinator has no path to read.
- Priority: Low to medium. Quality impact: low.

### M-20 (Medium). Stated evidence in section 1.2 overreaches
- Expert: Fowler.
- Text: E2 says a command run by a worker "has the same tools as a command a person runs" (`spec:22`). The cited evidence (`CAPS:161`, and `--agent claude` at `spec:22`) shows the worker is a top-level Claude session. It does not show tool parity, and no permission setting is cited (see M-2).
- Priority: Low to medium. Quality impact: low.

=== MINOR NOTES ===

- N-1. `spec:83` says the adversarial contract filename is "not fixed", but `spec:83` also calls adversarial "ready today" with a brief that does not name the file. These two are consistent only if P1 fixes the name before any run. P0 is the first run (`spec:158`), so the ready verdict and the P0 use are in tension. (See also RQ-2.)
- N-2. Index-repo is "ready" with an UNVERIFIED output location (`spec:86`, `INV-A:53`). Keep the verdict only after the location is checked.
- N-3. WC-12 says checks happen "at natural checkpoints" (`spec:70`). A single long tool call has none, so the worker cannot run `check` during it. Name the call's maximum length or the checkpoint between calls.
- N-4. The spec's claims about its own citation checks (`spec:11`, `spec:285`, `INV-B:320`, `INV-A:106`) cannot be checked from the workspace. Marked UNVERIFIED here.

=== GUARD CONDITION BOUNDARY TABLE (mandatory artifact, triggered) ===

Trigger: the candidate contains threshold checks (60 s, 4 and 5 min, 0.70, 3 failures), boolean guards (`--unattended` refusals, `--suite`, `target_release`) and sentinel-like values (`partial`, `consumer_fenced`). Guards enumerated: those in `spec:59-70`, `spec:73`, `spec:102`, `spec:104`, `spec:109`, `spec:114`, `spec:120-121`, `spec:146`. This table was built by one reviewer covering the Nygard, Crispin and Whittaker roles; the candidate's focus set does not include Crispin or Whittaker, so there is no independent check of its completeness (FR-10 limit).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-1 readiness fallback | `spec:59` | Zero/Empty | no launch prompt | n/a | nothing to wait on | OK |
| WC-1 readiness fallback | `spec:59` | Maximum | fallback 45-60 s | true (fails above about 45 s, `CAPS:49`) | "well inside" undefined | GAP (M-13) |
| WC-2 gate resolution | `spec:60` | Typical | gate with documented default | resolves (a) | per section 3 row | OK |
| WC-2 gate resolution | `spec:60` | Legitimate Edge | gate in no section 3 row | unknown | no rule | GAP (M-14) |
| WC-3 ask coordinator | `spec:61` | Sentinel Value Match | implement Ruling question | may ask; reply used as flag | contradicts `spec:109`, `spec:234-236`, `spec:208` | GAP (RQ-1) |
| WC-4 contract written | `spec:62` | Zero/Empty | output dir cannot be created | contract cannot be written | no fallback | GAP (M-17) |
| WC-5 outcome mapping | `spec:63` | Zero/Empty | no report file | failed | stated | OK |
| WC-5 outcome mapping | `spec:63` | Typical | `partial` | succeeded | no dependent-start rule | GAP (M-4) |
| WC-5 outcome mapping | `spec:63` | Legitimate Edge | audit verdict FAIL, worker completed | succeeded | stated | OK (see M-4) |
| WC-6 retry | `spec:64` | Legitimate Edge | retry with same `--output`, non-resumable | output overwritten | no coordinator rule | GAP (M-18) |
| WC-7 top level | `spec:65` | Typical | command wrapped in subagent | must not happen | no check | GAP (M-8) |
| WC-9 outward flag | `spec:67` | Sentinel Value Match | flag supplied by a coordinator reply | true | D4(a) needs quoted user instruction | GAP (RQ-1) |
| WC-9 outward flag | `spec:67` | Maximum | "paid external run" | undefined | no list | GAP (M-7) |
| WC-10 heartbeat wait | `spec:68` | Maximum | single Agent-tool call over 5 min | must split | cannot split | GAP (M-5) |
| cli-eval `run` gate | `spec:104` | Zero/Empty | no `--suite` | blocked | stated | OK |
| cli-eval `run` gate | `spec:104` | Legitimate Edge | unknown suite name | unknown | not stated | GAP (M-15) |
| task confidence | `spec:121` | Maximum | 0.70 exactly | not below, proceed | "below 0.70" stated | OK |
| target_release | `spec:120` | Zero/Empty | flag absent | blocked | stated | OK |
| target_release | `spec:120` | Legitimate Edge | frontmatter set, flag absent | unknown | not stated | GAP (M-16) |
| circuit breaker | `spec:63`, `CAPS:80` | Maximum | 3 consecutive `blocked` | breaker not tripped | no retry rule | GAP (M-3) |
| SA-1 standalone | `spec:146` | Typical | no `--unattended` | unchanged | roadmap and save rows ambiguous | GAP (M-10) |
| `--mode socratic` | `spec:102` | Sentinel Value Match | socratic + `--unattended` | refused | stated | OK |
| `--monitor 1` | `spec:114` | Typical | `--monitor 1` + `--unattended` | refused | stated | OK |

Pipeline Dimensional Analysis: not triggered. The candidate's flows are control messages and one contract file per worker; no multi-stage data flow changes counts (`spec:62`, `spec:73`). Quantity Flow Diagram: not produced for that reason. State Variable Registry and the correctness-focus tables: not triggered (focus is requirements, architecture). Advisory: the candidate's numeric thresholds meet the `--focus correctness` auto-suggestion condition (guard conditions with numeric thresholds, per the command's Focus Areas section). A later review may use `--focus correctness`.

=== REVISER BRIEF ===

Blocking finding ids: RQ-1, RQ-2, AR-1.

Restated bullet (command step 6): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report byte size before and after, and bytes added and deleted per finding id. Medium and minor findings are not revised and never appear here.

=== FOLLOW-UP CANDIDATES (Medium and minor; not blocking; the session asks the user once whether to open an issue) ===

M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9, M-10, M-11, M-12, M-13, M-14, M-15, M-16, M-17, M-18, M-19, M-20; minor notes N-1 to N-4.

=== COVERAGE ===

Read in full: `~/.claude/rules/prompts/document_review_loop_prompts.md` (sandbox home), the candidate `spec/orca-worker-contract-spec.md`, `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`, and the workspace README. Command definition read in full. Checked: the candidate's internal citations to `INV-A`, `INV-B` and `CAPS` lines (for example `spec:22`, `spec:44`, `spec:52`, `spec:73`, `spec:79`, `spec:83-92`, `spec:97`, `spec:114`, `spec:122`, `spec:139`, `spec:146-151`, `spec:158-162`, `spec:172-186`, `spec:194-196`, `spec:208`, `spec:228-253`, `spec:272-285`); each resolves to the content cited, apart from M-6. Not checked: any citation to `src/`, `.dev/evals`, `.dev/codegraph-migration`, `~/.claude`, `CLAUDE.md`, `plugins/` or external URLs (UNVERIFIED). Not run: fresh-context reviewers, the MERGE, the VERIFY prompt (coordinator steps). No file other than this report was written.

verdict: FAIL
