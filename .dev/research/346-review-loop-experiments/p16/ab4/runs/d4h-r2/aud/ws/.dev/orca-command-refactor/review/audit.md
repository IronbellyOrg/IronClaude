review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (labelled whole-document audit, first review)

| Item | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| Candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (286 lines) |
| Candidate SHA-256 | `24e411dcd5b98e3947b103fd3ff76a76e2a8ddec93e2c6e4f42c03d1f20513c9` |
| Baseline / prior | none: neither `--re-review` nor `--baseline` was given, so this is a first review of the whole document (`baseline: missing` is not noted because neither flag was given) |
| Reviewer model | Sonnet 5.5 (`claude-sonnet-5-5`) |
| Date | 2026-11-10 |
| Prompt followed | FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (file read in full before reviewing) |
| Brief clauses overridden | none |
| Improve step | skipped: the brief says to edit nothing but this file, and the candidate is not modified |
| Citation shorthand | `spec:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md` |

## Coverage
- Read in full: `README.md`, the candidate (sections 1-9, Decisions, UNVERIFIED), all three inventory files.
- Checked: every `INV-A:`, `INV-B:` and `CAPS:` pointer in the candidate that I sampled (about 90) lands on the row or bullet the spec says it does; the 10 / 27 / 6 split reconciles with the inventories (`INV-A:73`, `INV-B:278`) and with the rows of spec section 3 (10 + 27 rows) and section 4 (6 rows); the phase lists in `spec:159-162` account for all 37 non-coordinator commands once each (15 + 15 + 4 + 3).
- Run: one shell test of the `grep -E '^-[^-]'` pattern used by AC-C5 and AC-0.3 (finding M3).
- UNVERIFIED (not checkable in this sandbox): every citation into `src/`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `.dev/evals/.../EVIDENCE.md`, `.dev/codegraph-migration/...`, and the claims of the grep in E5 (`spec:25`) and the 11 re-read locations (`spec:11`). Those lines are accepted only as far as the inventories quote them.
- Not covered: whether the plan can actually be implemented against the live repo; whether any command exists that neither inventory lists (N6).

## Summary
No blocking finding. The decision (Orca on top, commands as units of work) follows from the evidence the spec cites, the rejected alternative is rejected on checkable grounds (`spec:31-37`, `CAPS:97-103`, `CAPS:147-150`), the evidence-strength gaps are stated plainly (`spec:41-45`), and the counts, phase lists and inventory pointers reconcile. Nine Medium findings and eleven minor notes remain; they are listed under follow-up candidates. Each Medium finding needs the implementer to pick between readings the text allows, or is a requirement the document never states.

=== REQUIREMENTS ANALYSIS ===

Experts in order: Wiegers, Adzic, Cockburn (requirements focus), then the architecture and adversarial experts below.

**Wiegers (requirements quality).** The requirements WC-1 to WC-12 each have an owner, evidence and mostly a check in section 7. Weak points are requirements whose scope term is undefined or whose precondition is not available for every command they bind:
- WC-4 binds every command to `<output-dir>/return-contract.yaml` where `<output-dir>` is what the coordinator passed with `--output` / `--output-dir` (`spec:62`). Eight section 3 rows add a contract but no output flag, so the precondition does not hold for them (M1).
- WC-9 turns off "a paid external run" without defining the term (`spec:67`), while research, tdd and review-translation search the web by default (M6).
- WC-10 limits "a single tool call" to 5 minutes while WC-7 leaves Agent-tool fan-out as it is (`spec:65,68`), and an Agent-tool wave is a single tool call (M7).
- WC-4 says commands that already write a contract "keep their fields", and also requires `status` to be one of four values (`spec:62`); the spec does not say what happens where an existing `status` uses other words (M5).

**Adzic (examples and testability).** Section 7 is concrete: exact commands, pass conditions, and a worked flag example for D1 (`spec:228`). Checks that cannot do their job as written:
- AC-C5 and AC-0.3 use `grep -E '^-[^-]'` to prove edits are additive; that pattern never prints a deleted markdown bullet (M3).
- AC-0.4 compares the worker's `--outcome` with "that report's status under WC-5" for reports that have no four-value `status` today (M5).
- AC-1.1 and AC-1.2 select commands by "section 3 phase is P1", but six commands that section 6 puts in P1 carry no P1 tag in section 3 (M8).
- AC-C1 can fail on the spec's own P0 deliverable (M4).

**Cockburn (stakeholders and goals).** Actors and goals are clear: the coordinator (plans, briefs, reads the report), the worker session (sends lifecycle messages), the command (does the work), the person (standalone use, SA-1). Goal-level gap: the spec states the person's interest (SA-1 to SA-6) and the coordinator's (section 2.3) but does not say who owns the outcome when an `ask` is answered and a command is re-run (N10).

=== ARCHITECTURE ANALYSIS ===

**Fowler (boundaries).** The boundary is clean: Orca calls live only in the worker session and the coordinator, the shared rules are in one core file, and SA-2 plus AC-C1 enforce "no Orca in commands" (`spec:147,172`). Two seams are soft:
- Section 1.1 says what changes in commands "is limited to" the three contract items (`spec:16`), but section 3 and SA-4 add interface-drift fixes, an added `Write` tool for explain, a frontmatter move and a usage-line fix (`spec:108,112,102,149`) (N1).
- `tasklist` now depends on a flag of `reflect` (`--unattended` passed down, `spec:122`) while `reflect` has its own gate change (`spec:88`); both are P2, so the dependency is satisfied by phase, but the divergence from the inventory advice is not recorded (M9).

**Nygard (failure modes).** Failure handling is a strength: every outcome writes a contract (WC-4), the outcome mapping is fail-closed for absent, empty or unparseable reports (WC-5), a blocked worker is not silent (WC-2, WC-3), and the 60-second readiness case is separated from the later silent-stall case (`spec:44`). Gaps: a worker that dies before writing the contract is covered only by WC-5's "absent" branch, which relies on a `worker_done` that a dead worker never sends (the coordinator-side handling is Orca's, `CAPS:125-126`, and the spec does not restate it); and WC-10 does not cover Agent-tool waves (M7).

**Newman (evolution and compatibility).** SA-1 to SA-6 and the additive-edit rule (SA-4) are the compatibility contract; AC-C5 is its only mechanical check and it is blind to deleted bullets (M3). The spec names the plugin-mirror question as UNVERIFIED item 8 (`spec:279`) and tells each phase to resolve it first; `make verify-sync` (AC-C2) does not cover `plugins/superclaude/commands/`.

**Hohpe (message flow).** The message flow (`task-create`, `worker-start`, `worker_done`, `check`, `reply`, `ask`) matches the capabilities inventory (`CAPS:58-67,70-80`). Ordering rules are stated: one `worker_done`, resume the same message ID on `ask` timeout, `check` before `worker_done`, stop on `consumer_fenced` (WC-3, WC-5, WC-12). The sequence "ask, answer, re-invoke the command" has no stated rule for where the second run writes (N10).

=== ADVERSARIAL ANALYSIS (Whittaker) ===

Severity uses the panel labels; the graded result (blocking or Medium) follows the Review Loop grading rule.

1. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 / spec:62 and section 2.3 / spec:73** fails when **a command is run with `--unattended` and the coordinator has no output flag to pass**. Concrete attack: `/sc:research "topic" --unattended` (row `spec:116`, no output flag added). Before: no `--output`, `<output-dir>` undefined. After: the command must write `<output-dir>/return-contract.yaml`, and AC-2.3 step 4 (`spec:183`) runs `test -s <contract>` on a path the brief could not name. Same for review-translation, recommend, save, task, implement, cli-portify, cli-eval (rows `spec:117,115,119,121,109,105,104`). MAJOR, graded Medium: the implementer must choose a location or add a flag (M1).

2. I can break this specification by **Divergence Attack**. The invariant at **spec:159 (P1 scope) versus spec:160 and spec:60 (WC-2)** fails when **a command has a gate but no outward default**. Concrete attack: after P1, `/sc:cleanup <dir> --unattended` is "accepted" (P1 text: every command in 3.1 and 3.2 "that has no outward default"), but its approval gate is converted only in P2 (`spec:103,160`). State: flag accepted, gate unchanged, so the command prompts under `--unattended`, which WC-2 forbids. MAJOR, graded Medium (M2).

3. I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-4/WC-5 and Decisions / spec:62,63,262** fails when **an existing contract's `status` uses its own vocabulary**. Concrete attack: workflow already writes a contract with a `status` field "including `failed`" (`INV-B:272`); the 7.2 step 4 test asserts `d['status'] in {'succeeded','partial','failed','blocked'}` (`spec:183`) and WC-5 maps any other value to `--outcome failed` (`spec:63`). If the existing word is not one of the four, a good run is reported failed. Whether it is one of the four is UNVERIFIED (`sk/sc-workflow-protocol/refs/return-contract.md` is not in the workspace). MAJOR, graded Medium (M5).

4. I can break this specification by **Sentinel Collision Attack** (term). The invariant at **WC-9 / spec:67** fails when **a default is neither a push, PR, post or install but is "a paid external run"**. Concrete attack: `/sc:research` with Tavily search (`INV-B:134`), `/sc:review-translation` evidence search (`INV-B:144`), `/sc:tdd` with 0-4 web agents (`INV-B:221`): under `--unattended` each is either "off" (the command loses its function) or "on" (WC-9 broken), and the text does not say which. MAJOR, graded Medium (M6).

5. I can break this specification by **Sequence Attack**. The invariant at **WC-3 / spec:61 with WC-6 / spec:64** fails when **a worker asks, receives an answer and re-invokes a "fresh dir" command into the same `<output-dir>`**. Concrete attack: run 1 ends `status: blocked` and writes `<output-dir>/return-contract.yaml` plus partial files; run 2 (same directory, answer passed as a flag) overwrites the contract and may mix its files with run 1's. WC-6's fresh-directory rule is stated for retry workers, not for in-session re-runs. MINOR (N10): the final contract is rewritten on every outcome, so the last state is still readable.

6. I can break this specification by **Accumulation Attack**. The invariant at **WC-10 / spec:68** fails when **one tool call accumulates more than 5 minutes of work**. Concrete attack: `/sc:cleanup-audit` runs waves of 7-8 concurrent Task agents (`INV-A:42`); each wave is one blocking Agent-tool call. The session cannot heartbeat during it, and the spec splits only Bash waits (examples: poll, eval). Whether Orca uses heartbeat age at all is UNVERIFIED (`CAPS:130`, `CAPS:182` item 7), which is why this stays Medium (M7).

7. I can break this specification by **Accumulation Attack** (check). The invariant at **AC-2.4 / spec:202** fails when **the PR has more than one page of reviews or comments**. Concrete attack: `gh api repos/IronbellyOrg/IronClaude/pulls/<PR>/reviews --jq length` without `--paginate` counts only the first page (default 30 items); a posted review on page 2 leaves the count unchanged and WC-9 appears to hold. MINOR (N3): the scratch fork PR is likely small.

8. **Zero/Empty and Divergence on the regex guard.** I can break this specification by **Divergence Attack**. The invariant at **AC-C5 / spec:176 and AC-0.3 / spec:193** fails when **the diff deletes a markdown bullet**. Concrete attack: delete the line `- Will Not: Modify specifications without explicit user consent`; `git diff -U0` shows `-- Will Not: ...`; the pattern `^-[^-]` excludes it because the second character is `-`. Verified in this sandbox with `diff -U0 ... | grep -E '^-[^-]'`, which printed nothing for a removed `- Will Not: modify specs` line and for a removed `---` line. Result: "prints nothing: edits are additive" passes while SA-4 and SA-1 are violated (M3).

=== GUARD CONDITION BOUNDARY TABLE ===

Responsibility: Nygard (construction), Crispin (completeness), Whittaker (attack). Guards are the conditional, threshold, boolean and sentinel checks in the spec. One row per applicable input class; omitted classes are listed under the table with a one-line reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `--unattended` switch | spec:16,51,228 | Zero/Empty | flag absent | false | SA-1: behavior and defaults unchanged (`spec:146`) | OK |
| `--unattended` switch | spec:51,60,62 | One/Minimal | flag present, no output flag in the command line | true | WC-4 needs `<output-dir>`; none defined for 8 rows (research, review-translation, recommend, save, task, implement, cli-portify, cli-eval) | GAP |
| `--unattended` switch | spec:159 | Typical | flag on a command with no gate and no outward default | true | no-op plus contract (`spec:159`) | OK |
| `--unattended` switch | spec:159-160 | Legitimate Edge Case | flag on a command with a P2 gate and no outward default (cleanup, improve, tdd, troubleshoot...) after P1 only | true | P1 says "accepted"; gate conversion is P2; WC-2 forbids prompts | GAP |
| `--unattended` switch | spec:159 | Legitimate Edge Case | flag on auggie-review, task, cli-eval, pr-submit, post-release before their phase | true | rejected (M15 text) | OK |
| `--unattended` switch | spec:51,228 | Sentinel Value Match | the string `--unattended` inside quoted free text (a prompt or topic) | ambiguous | spec says "caller passes `--unattended`"; D1(a) does not say token versus substring | GAP |
| Refused-flag guards (`--interactive`, `--watch`, `--mode socratic`, `--format interactive`, `--monitor 1`) | spec:102,103,108,110,114,123 | Legitimate Edge Case | refused flag plus `--unattended` | true | refuse; whether the refusal also writes a contract is covered by WC-4 "every outcome", but the output directory may not exist | OK |
| WC-5 outcome mapping | spec:63 | Zero/Empty | report absent or empty | true | `--outcome failed` | OK |
| WC-5 outcome mapping | spec:63 | One/Minimal | `status: partial` | true | `--outcome succeeded`, body states `partial` | OK |
| WC-5 outcome mapping | spec:63 | Typical | `status: succeeded` | true | `--outcome succeeded` | OK |
| WC-5 outcome mapping | spec:63 | Sentinel Value Match | `status: blocked` | true | `--outcome failed` | OK |
| WC-5 outcome mapping | spec:62,63,183 | Legitimate Edge Case | existing contract with its own `status` words, or markdown report with no `status` (troubleshoot `REPORT.md`, `INV-B:242`) | unknown | "outside the four values" gives failed; "keep their fields" gives conflict; not reconciled | GAP |
| WC-5 outcome mapping | spec:63 | Legitimate Edge Case | audit whose verdict is FAIL | true | `succeeded` (M19 text) | OK |
| WC-10 wait limit | spec:68 | Zero/Empty | step with no wait | false | no splitting needed | OK |
| WC-10 wait limit | spec:68,182 | Typical | Bash wait of 4 minutes | false | allowed; `check --wait` uses 240000 ms | OK |
| WC-10 wait limit | spec:68 | Sentinel Value Match | wait of exactly 5 minutes | false ("longer than 5") | allowed by "longer than 5" but the same text caps waits at 4 minutes; 4 governs | OK |
| WC-10 wait limit | spec:65,68 | Maximum/Overflow | one Agent-tool call lasting more than 5 minutes (cleanup-audit wave, tdd, reflect Tier 2) | true | not addressed; WC-7 leaves fan-out unchanged | GAP |
| Nesting depth fence | spec:33,66 | One/Minimal | worker at depth 1 calls `worker-start` | true | refused; WC-8 forbids it | OK |
| Nesting depth fence | spec:249-252 | Legitimate Edge Case | user raises depth (D5 b) | false | WC-8 still forbids commands calling Orca | OK |
| Readiness limit (WC-1) | spec:59 | Typical | launch-path prompt with 30 s fallback | false | passes (`EVIDENCE.md:45` via `CAPS:49`) | OK |
| Readiness limit (WC-1) | spec:59 | Legitimate Edge Case | fallback "well inside" the limit | unknown | no number given; evidence says about 45 s fails (a 45 s start timeout) | GAP |
| Confidence gate (task) | spec:121 | Typical | confidence below 0.70 | true | blocked | OK |
| Confidence gate (task) | spec:121 | Legitimate Edge Case | confidence exactly 0.70 or 0.70-0.89 | false | the row speaks only of "below 0.70"; INV-B:199 gives the same threshold | OK |
| `ask` once (WC-3) | spec:61 | Legitimate Edge Case | a second gate after the first answer | true | "ask the coordinator once"; second gate not stated (resolves as blocked by WC-2 (c), by inference) | GAP |
| WC-9 outward default | spec:67 | Sentinel Value Match | default that is a "paid external run" (web search, real-model eval) | unknown | term undefined; rows for research, tdd, review-translation say nothing | GAP |
| WC-9 outward default | spec:67,100 | Typical | auggie-review PR posting | true | off; returns only with explicit `--post-pr` | OK |
| AC-C5 / AC-0.3 additive check | spec:176,193 | Zero/Empty | no deleted lines | false | prints nothing, pass | OK |
| AC-C5 / AC-0.3 additive check | spec:176,193 | Sentinel Value Match | deleted line that starts with `- ` or `---` | false (pattern misses it) | "prints nothing" although a line was deleted | GAP |
| AC-1.1 / AC-1.2 command set | spec:195-196 | Legitimate Edge Case | P1-scope command with no P1 tag in section 3 (brainstorm, init-lite, adversarial, cleanup-audit, index-repo, workflow) | unknown | not clearly in or out of the tested set | GAP |
| AC-C1 grep | spec:172 | Legitimate Edge Case | the new Orca section in `HOW-WE-WORK.md` names an `orca` command | true | the grep excludes only WORKER-CONTRACT.md, so it would fail P0 | GAP |

Classes left out: Maximum/Overflow for the `--unattended` switch, WC-5, the depth fence, the confidence gate and AC-C1 (the guards are boolean or categorical, no capacity applies); Zero/Empty for the depth fence and the confidence gate (depth 0 is the coordinator and confidence 0 falls under "below 0.70"); One/Minimal for WC-10 and the readiness limit (a one-second wait is inside every limit).

Completion gates: FR-10 satisfied (all cells filled, guards listed, omitted classes given a reason). FR-8: every GAP row maps to a Medium finding below (M1 to M8, N10, N11), none blocking, because each needs the implementer to choose between readings the text allows or concerns a requirement the document never states. FR-9: no blank Specified Behavior cell; the cells that read "not addressed" or "not stated" are the GAP rows.

=== QUANTITY FLOW DIAGRAM (Pipeline Dimensional Analysis, Fowler and Whittaker) ===

Trigger: the spec partitions a command set into groups and phases, and later artifacts consume each group. Counts as stated in the document:

```text
[Source: 43 commands in cmd/ (INV-A:3 = 21, INV-B:3 = 22)]  (completeness of 43: UNVERIFIED, N6)
   --> [Split by verdict: spec:76]
         6 coordinator-only (spec:130-137)            --> no phase, no AC (consistent)
         37 worker-capable = 10 ready (spec:81-92) + 27 need change (spec:97-125)
   --> [Phase assignment: spec:158-162]
         P0: 0 command edits, 3 smoke runs (troubleshoot, workflow, adversarial)
         P1: 15 (analyze, build, business-panel, brainstorm, design, document, explain, index,
                 init-lite, test, load[usage line only]; adversarial, cleanup-audit, index-repo, workflow)
         P2: 15 (auggie-review, cleanup, improve, cli-eval, cli-portify, recommend, research,
                 review-translation, spec-panel, task, tasklist, reflect, release-split, tdd, troubleshoot)
         P3: 4   P4: 3                                  15 + 15 + 4 + 3 = 37  (conserved)
   --> [Consumers of the P1 set]
         P1 scope text (spec:159):            15
         AC-1.1 command set (spec:195):       commands with a section-3 "P1" tag, minus load
                                              = analyze, build, business-panel, design, document,
                                                explain, index, test = 8     <-- MISMATCH (15 vs 8)
         AC-1.2 live check (spec:196):        same selector as AC-1.1 = 8      <-- MISMATCH
```

Divergence point: P1 scope 15 versus AC-1.1 / AC-1.2 coverage 8 (the other 7 are adversarial, cleanup-audit, index-repo, workflow, brainstorm, init-lite, and load, which is excluded on purpose). FR-19 labels a dimensional mismatch CRITICAL; the Review Loop section requires grading by consequence, and the consequence here is that the P1 checks do not cover six edited commands, not that an implementer builds a wrong command. Graded Medium (M8).

=== FINDINGS ===

Findings table. No finding is blocking.

| Id | Panel label | Graded | Expert | Location |
|---|---|---|---|---|
| M1 | MAJOR | Medium | Wiegers, Whittaker | spec:62,73,183 vs rows spec:104,105,109,115,116,117,119,121 |
| M2 | MAJOR | Medium | Whittaker | spec:159-160 vs spec:60 |
| M3 | MAJOR | Medium | Adzic, Newman, Whittaker | spec:176,193 |
| M4 | MAJOR | Medium | Adzic | spec:172 vs spec:150,158 |
| M5 | MAJOR | Medium | Wiegers, Whittaker | spec:62,63,183,194,262 |
| M6 | MAJOR | Medium | Wiegers, Whittaker | spec:67 |
| M7 | MAJOR | Medium | Nygard, Whittaker | spec:65,68 |
| M8 | MAJOR | Medium | Adzic, Fowler | spec:159,195-196 |
| M9 | MINOR-to-MAJOR | Medium | Fowler | spec:122 |
| N1-N11 | MINOR | minor | various | below |

### Medium findings (warnings; listed under follow-up candidates)

**M1. WC-4's output directory does not exist for eight rows.** Grading check: an implementer who follows WC-4 and the research row as written builds a research command that must write `<output-dir>/return-contract.yaml`, where `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)" (`spec:62`), but the research row adds no such flag (`spec:116`); the same holds for review-translation, recommend, save, task, implement, cli-portify and cli-eval. Graded Medium because the fix (add the flag, as the analyze row does at `spec:99`) is the obvious reading and the spec allows new flags (SA-4, `spec:149`), so an implementer picks between two sensible readings rather than builds a provably wrong command. Effect if unfixed: the coordinator cannot name the report path before dispatch (`spec:73`) and AC-2.3 step 4 (`spec:183`) has no path to test.

**M2. P1 accepts `--unattended` on commands whose gates convert in P2.** Grading check: `spec:159` says the flag is accepted by every command in 3.1 and 3.2 that has no outward default, "a no-op where a command has no gate"; `spec:160` and the rows (for example `spec:103`) convert gates in P2; WC-2 (`spec:60`) forbids any person-blocking step under `--unattended`. A P1-complete `/sc:cleanup --unattended` therefore accepts the flag and still prompts. Medium because the sequence is transitional and a reader can take "accepted" to mean "refused until its phase", as the sentence does for auggie-review, task, cli-eval, pr-submit and post-release.

**M3. AC-C5 and AC-0.3 cannot detect a deleted bullet.** Grading check: an implementer who runs `git diff -U0 ... | grep -E '^-[^-]'` (`spec:176,193`) gets an empty result for a diff that deletes a markdown bullet or a `---` line, because git shows such a line as `-- ...` or `----` and the pattern needs a non-`-` second character. Verified by running the pattern on a sample diff (printed nothing). The checks exist to prove SA-4 (additive edits) and SA-5 (no existing routing row changed). Graded Medium: the criterion under-detects; it does not make any stated text wrong. A pattern such as `grep -E '^-' | grep -vE '^---'` does not have this blind spot.

**M4. AC-C1 can fail on P0's own deliverable.** Grading check: AC-C1 (`spec:172`) must print nothing for `src/superclaude/core`, excluding only `WORKER-CONTRACT.md`; P0 adds an Orca section to `HOW-WE-WORK.md` (`spec:158`, SA-5 `spec:150`), which today has no `orca` mention (E5, `spec:25`). If that section names an `orca orchestration ...` command, P0 fails its own common check. Medium because the section's text is not specified, so the failure needs the guess that it quotes a command.

**M5. Status vocabulary: existing contracts versus the four-value set.** Grading check: WC-4 says commands with an existing contract "keep their fields" (`spec:62`); step 4 asserts `status` is one of four words (`spec:183`); WC-5 maps any other word to `failed` (`spec:63`). Workflow's contract already has a `status` (`INV-B:272`), and troubleshoot's report is a markdown file (`INV-B:242`). AC-0.4 requires the worker's `--outcome` to match "that report's status under WC-5" for these reports (`spec:194`), which is undefined if the report has no four-value `status`. Whether the existing words are in the set is UNVERIFIED here, so Medium. This also bears on the P0 gate, whose failure "reopens section 1".

**M6. "A paid external run" is undefined.** Grading check: WC-9 (`spec:67`) turns off any default that "calls a paid external run" under `--unattended`; research (`INV-B:134`), review-translation (`INV-B:144`) and tdd (`INV-B:221`) search the web by default, and cli-eval run executes model runs (`INV-A:44`). Whether they are "paid" is not stated, and the rows leave them unchanged. Medium: an implementer may disable web search in research (a wrong outcome for that command) or ignore the term.

**M7. WC-10 and Agent-tool waves.** Grading check: WC-10 (`spec:68`) says a step that blocks a single tool call longer than 5 minutes must be split into waits of at most 4 minutes; WC-7 (`spec:65`) leaves each command's Agent-tool fan-out as it is; a wave of 7-8 agents is one tool call (`INV-A:42`). No row splits such a call, and the heartbeat is lost while it runs. Medium because Orca's use of heartbeat age is UNVERIFIED (`CAPS:130`, `CAPS:182` item 7).

**M8. The P1 test set differs from the P1 scope.** Grading check: `spec:159` puts 15 commands in P1; AC-1.1 and AC-1.2 (`spec:195-196`) test "every command whose section 3 phase is P1, except load". Section 3.2 tags 9 commands P1; the 3.1 rows for adversarial, cleanup-audit, index-repo and workflow tag only their fix (`spec:83,85,86,92`); brainstorm and init-lite (`spec:84,87`) have no tag. The tests cover 8 of the 14 non-load commands. Medium because the implementer's work is clear from `spec:159`; only the test selection is ambiguous.

**M9. The tasklist row departs from the inventory advice without a recorded decision.** Grading check: `INV-B:215` recommends calling reflect without `--remediate` in Stage 10.5; `spec:122` instead passes `--unattended` to each reflect so its headless rule applies (`spec:88`), which auto-accepts remediation for auto-fixable registers (`INV-B:109`). The Decisions table (`spec:258-269`) has no entry. The row also states the reflect fan-out is "inside Claude Code's nesting limit" (`INV-A:14`), where `INV-B:210` and `INV-B:322` leave nested spawning UNVERIFIED. Medium: the consequence (unattended tasklist runs remediation hand-offs the brief did not ask for) needs the guess that auto-accept is unwanted; WC-9 covers only outward actions.

### Minor notes

- **N1.** Section 1.1 says command changes are "limited to" the three contract items (`spec:16`); section 3 and SA-4 add drift fixes, a Write tool, a frontmatter move and a usage-line fix (`spec:108,112,102,149`), and non-goal 8 limits fixes to defects that stop a command working as a worker (`spec:220`), which a usage line does not.
- **N2.** E3 cites `invocation_method: "skill-direct"` as support (`spec:23`) while 1.4 (1) says that run proves only the nested route (`spec:43`); `INV-A:13` reads the same field as direct proof. State which reading the spec takes.
- **N3.** AC-2.4 counts reviews and comments with `--jq length` and no `--paginate` (`spec:202`); only the first page of 30 is counted.
- **N4.** SA-3 says contract and report files are written "only in unattended mode or when the caller passes the new output flag" (`spec:148`); WC-4 says "in unattended mode" (`spec:62`).
- **N5.** 7.2 step 5 checks that "the command's skill is the first tool call" (`spec:184`); 13 of the 21 inventory-A commands have no skill (`INV-A:70`), and the preamble may call `check` or `heartbeat` first. The pass condition (no `AskUserQuestion`, no Agent or Task call before the command) is clear; the descriptive clause is not.
- **N6.** "The 43 commands in `cmd/`" (`spec:76`) rests on the two scope lists (`INV-A:3`, `INV-B:3`); neither inventory records a directory listing, so completeness is UNVERIFIED.
- **N7.** D4 says it affects auggie-review `--post-pr` and task `commit`/`push` (`spec:244`), both P2 rows, while section 6 says Phases 1-3 need no user decision (`spec:154`). The rows turn the actions off, so the behavior holds under either D4 answer; the sentence should say so.
- **N8.** The research row pins `--strategy planning` (`spec:116`) but does not carry `INV-B:128,316`: whether the frontmatter persona loads `deep-research-agent.md` is UNVERIFIED, and the command states no default strategy (`INV-B:129`).
- **N9.** The `/sc:spec-panel` definition used for this audit already lists `--output <file>`, `--report-dir`, a `## Unattended mode` section, and `<report-dir>/return-contract.yaml` (`command.md:23-24,455-465`), while the spec's row says "add `--output`; contract" (`spec:120`) from `INV-B:43,182` ("no `--output` flag exists"). The two snapshots differ; which is newer is UNVERIFIED. The flag name `--report-dir` also differs from WC-4's `--output` / `--output-dir`.
- **N10.** WC-3 and WC-6 do not say where a re-run after an answered `ask` writes (Whittaker item 5).
- **N11.** WC-1 says a launch prompt must fall back "well inside" the readiness limit (`spec:59`) without a number; the cited evidence gives 30 s passing and about 45 s failing (`CAPS:49`).

## Follow-up candidates
Medium: M1, M2, M3, M4, M5, M6, M7, M8, M9. Minor: N1 to N11. Medium and minor findings never trigger a revision and never fail a review. The session that ran this review asks the user once per loop whether to open an issue for them; this run was a subagent that replies only `DONE <path>`, so the question was not asked here and no issue was created. The coordinator asks it.

## Reviser brief
No blocking finding is open, so no revision is requested and no finding id is listed. For any later revision the contract is: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Medium and minor findings are not part of any reviser brief and a brief cannot make them blocking.

verdict: PASS
