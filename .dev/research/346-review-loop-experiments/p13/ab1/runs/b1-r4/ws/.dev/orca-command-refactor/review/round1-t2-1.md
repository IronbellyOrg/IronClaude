review: 1 of 3

# /sc:spec-panel critique: orca-worker-contract-spec.md (round 1)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: missing (first review; no `--re-review`, no `--baseline`)
- focus: requirements, architecture (critique mode, FIRST-REVIEW prompt from `~/.claude/rules/prompts/document_review_loop_prompts.md`)
- reviewer model: claude-haiku-5-5, single reviewer. `superclaude review panel resolve` is not installed in this sandbox, so one reviewer ran and this is the loop summary (per the prompt's fallback).
- verdict basis: 5 blocking findings open (F1-F5).

Citation keys: `spec:N` = candidate line N. `INV-A:N` = `.dev/orca-command-refactor/inventory/commands-a.md` line N. `INV-B:N` = `inventory/commands-b.md` line N. `CAPS:N` = `inventory/orca-capabilities.md` line N. `README:N` = `.dev/orca-command-refactor/README.md` line N. Any repo file the spec cites that is not in this workspace (src/, .dev/evals, .dev/codegraph-migration, CLAUDE.md, pyproject.toml, install_core.py, qa.md, SKILL.md files) is UNVERIFIED-direct. Where an inventory quotes it, I checked the quotation in the inventory only.

Coverage: read the whole candidate, `README.md`, all three inventories, the FIRST-REVIEW prompt and command.md. I did not open `specs/history/` (not part of this brief). I did not touch any path outside the workspace.

Grading rule applied: a finding is blocking only if the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y." holds with no further assumption. Undefined states and unstated requirements are Medium, even when labelled MAJOR.

---

## Findings summary

| id | expert | severity | blocking | category | location |
|---|---|---|---|---|---|
| F1 | Cockburn, Whittaker | CRITICAL | yes | safety | spec:61, spec:109 |
| F2 | Fowler, Newman | MAJOR | yes | contradiction | spec:62, spec:83, spec:90, spec:92 |
| F3 | Crispin, Fowler | MAJOR | yes | unpassable-check | spec:79, spec:85-92, spec:201 |
| F4 | Wiegers | MAJOR | yes | unpassable-check | spec:159, spec:195 |
| F5 | Wiegers, Adzic | MAJOR | yes | unpassable-check | spec:172, spec:173-176 |
| F6 | Hohpe | MAJOR | no | other | spec:63, spec:263 |
| F7 | Nygard | MAJOR | no | missing-requirement | spec:64, spec:73 |
| F8 | Nygard, Whittaker | MAJOR | no | missing-requirement | spec:63 |
| F9 | Fowler | MAJOR | no | other | spec:22 |
| F10 | Crispin | MAJOR | no | unpassable-check | spec:184, spec:194 |
| F11 | Newman | MAJOR | no | missing-requirement | spec:91, spec:228 |
| F12 | Nygard, Hohpe | MAJOR | no | missing-requirement | spec:68 |
| F13 | Newman | MAJOR | no | missing-requirement | spec:105, spec:160 |
| F14 | Wiegers | MINOR | no | other | spec:158 |
| F15 | Nygard | MINOR | no | missing-requirement | spec:61 |

---

=== REQUIREMENTS ANALYSIS ===

### F1. Worker may turn a coordinator answer into an implement Ruling (blocking)

- **Issue.** WC-3 says that when a gate would resolve as blocked, the worker "may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag" (`spec:61`). The implement row says the halt stays blocked and "the Ruling rule itself is unchanged (see open decision D2)" (`spec:109`). D2 is still open, and the Ruling rule says "another agent's message ... [is] not acceptance" (`INV-A:66`, quoting `sk/sc-implement-protocol/refs/qa.md:238`). The coordinator is an agent (`INV-A:66`). So WC-3 lets the rule be bypassed before the user has decided D2.
- **Expert.** Cockburn (actor and goal of the gate), Whittaker (attack below).
- **Blocking sentence.** An implementer who follows WC-3 as written re-invokes `/sc:implement` with the coordinator's answer as the Ruling, and that is wrong because the qa.md:238 rule exists to stop an agent approving its own work.
- **Recommendation.** Exempt `E-HALT-QA` and `E-NO-RULING` (and any other safety-boundary gate) from WC-3. Or state that WC-3 relay is allowed only where a decision in section 9 has been recorded. Name the exemption in the implement row.
- **Priority.** High. **Quality impact.** Safety rule (Clarity 4, Consistency 3).

### F2. The WC-4 contract path is not a fixed, pre-dispatch directory for several section 3.1 commands (blocking)

- **Issue.** WC-4 says the command writes `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed" (`spec:62`). Section 2.3 relies on this, so the path is "known before dispatch" (`spec:73`). The section 3.1 rows contradict it:
  - adversarial: "Fix the contract filename to `<output>/adversarial/return-contract.yaml`" (`spec:83`). That is a subdirectory, not `<output-dir>/return-contract.yaml`.
  - tdd: `--output` takes a file ("TDD file at `--output`", `spec:90`; `INV-B:47`). A file cannot be the directory WC-4 names.
  - workflow: the contract is `.dev/tasks/to-do/<id>/return-contract.yaml` (`spec:92`; `INV-B:52`). The `<id>` is made per run ("Fresh package each run", `spec:92`), so it is not known before dispatch.
  - init-lite: `--output <file>` (`spec:87`; `INV-A:55`).
- **Expert.** Fowler (interface contract), Newman (uniform contract across services).
- **Blocking sentence.** An implementer who follows WC-4 as written writes the workflow or tdd contract at a path the brief cannot name in advance, and the coordinator's "known before dispatch" check (`spec:73`) then has no path to open; that is wrong because the spec promises a path known before dispatch.
- **Recommendation.** Define the contract location per command in one table (the directory the brief passes, or a named derived path). Make WC-4 cover file-valued `--output` and per-run ids, for example by requiring the brief to pass a directory. Use one path rule for adversarial as well.
- **Priority.** High. **Quality impact.** Interface integrity (Clarity 5, Consistency 3).

### F3. Phase acceptance requires contracts that no phase adds (blocking)

- **Issue.** Section 3.1 opens: "the worker reports the named file until Phase 1 adds the contract" (`spec:79`). P1 covers analyze, build, business-panel, design, document, explain, index, test, load, plus fixes to adversarial, cleanup-audit, index-repo and workflow (`spec:159`). None of P1's rows adds a contract to cleanup-audit or index-repo; they get only a named filename or an output-location fix (`spec:85`, `spec:86`). troubleshoot, tdd and release-split get only gate fixes in P2 (`spec:89-91`, `spec:160`). init-lite's fix column says "None" and no phase lists it (`spec:87`). load's row says "none (see note)" (`spec:112`). AC-2.3 requires every P2 command to pass step 4 of 7.2, which requires a contract with a `status` (`spec:201`, `spec:183`).
- **Expert.** Crispin (acceptance completeness), Fowler (phase boundaries).
- **Blocking sentence.** An implementer who follows the phase table builds the P2 troubleshoot, tdd and release-split workers without any contract, so AC-2.3 (`spec:201`) fails on step 4 for them, and that is wrong because the table claims those commands pass.
- **Recommendation.** Add each contract to the phase that tests it, or move the command out of the acceptance criteria. State explicitly what init-lite, cleanup-audit and index-repo write for WC-4.
- **Priority.** High. **Quality impact.** Testability (Clarity 6, Testability 3).

### F4. AC-1.1 cannot pass at the end of P1 (blocking)

- **Issue.** AC-1.1 asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md` (`spec:195`). P1 is said to add the flag to "every command in sections 3.1 and 3.2 (a no-op where a command has no gate)" (`spec:159`). The P1 command column lists about 13 commands, and P2-P4 are not yet edited. The 3.2 rows for load, validate-roadmap and validate-tests say "none", "n/a" or "n/a" for the contract (`spec:112`, `spec:124`, `spec:125`), so the required filename cannot be present.
- **Expert.** Wiegers (requirement and test consistency).
- **Blocking sentence.** An implementer who builds P1 as the phase table lists it runs AC-1.1 and gets a failure for the 24 commands that P2-P4 have not yet edited and for the three commands with no contract, and that is wrong because the spec says P1 passes when AC-1.1 passes.
- **Recommendation.** Scope AC-1.1 per phase (each command assertion is tied to the phase that edits it), and state which commands have no contract and why.
- **Priority.** High. **Quality impact.** Testability (Clarity 6, Testability 3).

### F5. The AC-C1 grep matches nothing as written, and its exclusions are incomplete (blocking)

- **Issue.** AC-C1 uses `(orchestration\|worktree\|terminal\|agent)` inside an ERE (`spec:172`). In grep -E, `\|` is a literal pipe, not alternation. I ran the pattern in the sandbox against a file containing `orca worktree create` and `orca-ide terminal x`: the escaped form printed nothing (exit 1), and the same pattern with plain `|` matched both lines (exit 0). So the common check passes for any SA-2 violation (`spec:147`). Its only exclusion is `ccsession-tag` (`spec:172`). SA-2 allows an Orca mention in the contract file (`spec:147`), and P0 adds an Orca section to HOW-WE-WORK.md under `src/superclaude/core` (`spec:158`). The check does not say whether those are exempt.
- **Expert.** Wiegers (criterion must be checkable), Adzic (concrete example that exposes the failure).
- **Blocking sentence.** An implementer who runs AC-C1 as written sees no output for a command that calls `orca orchestration`, and that is wrong because SA-2 is the boundary that check is meant to enforce.
- **Recommendation.** Write the alternation with plain `|`, and name the exempt paths (the contract file and the P0 HOW-WE-WORK section) in the exclusions. Add a positive control to the check, a fixture that must match.
- **Priority.** High. **Quality impact.** Testability (Clarity 7, Testability 2).

### F6. partial maps to succeeded (follow-up, Medium)

- **Issue.** WC-5: `--outcome succeeded` "otherwise, including `partial`" (`spec:63`). The decision table justifies this (`spec:263`). A dependent Task becomes ready when the parent settles (`CAPS:85-86`), and the coordinator starts ready Tasks itself (`CAPS:92`).
- **Expert.** Hohpe (message semantics for downstream consumers).
- **Why Medium.** Harm needs an assumption: that the coordinator starts dependents without reading the contract. Section 2.3 says it opens the report (`spec:73`), so the spec does not prescribe the harm.
- **Recommendation.** State in WC-5 or 2.3 that a `partial` status blocks dependent starts until the coordinator has read it.

### F7. Retry and re-run output directories are unspecified (follow-up, Medium)

- **Issue.** WC-6 says a command with no resume flag writes "each run into a fresh output directory" (`spec:64`). Section 2.3 says the report path is known before dispatch (`spec:73`). A `worker-start --retry-of` (`CAPS:116`) needs a new directory, and the spec has no rule for choosing it or for finding the first attempt's contract.
- **Expert.** Nygard (retry and failure handling).
- **Recommendation.** Define the retry brief's directory rule (for example, `<output>/attempt-N`), and say which contract the coordinator reads after a retry.

### F8. A missing or unknown status falls into the success branch (follow-up, Medium)

- **Issue.** WC-5 maps "no report exists" to failed and everything else to succeeded (`spec:63`). A contract that exists but has no `status` key, or an unknown value, reaches "otherwise" and becomes succeeded. The spec does not define the state.
- **Expert.** Nygard (failure modes), Whittaker (attack below).
- **Whittaker attack.** I can break this specification by **Zero/Empty Attack**. The invariant at **spec:63** fails when **a worker crashes mid-write and leaves a non-empty contract without `status`**. Concrete attack: the command writes `return-contract.yaml` partially and stops. The step-4 check in 7.2 (`spec:183`) uses `test -s`, which passes for any non-empty file. WC-5's "otherwise" then sends `--outcome succeeded`. Before: no valid status. After: Orca settles the Task as succeeded.
- **Recommendation.** Map any contract whose status is absent or outside the four values to `failed`, and have the coordinator run the parse in 7.2 step 4 before trusting it.

### F9. E2 claims tool parity that the evidence does not show (follow-up, Medium)

- **Issue.** E2 says "a command run by a worker has the same tools as a command a person runs" (`spec:22`). The cited source, `CAPS:161`, only says the worker is a top-level Claude session. No inventory line shows tool parity. Tool availability in nested agents is itself UNVERIFIED (`INV-A:112`).
- **Recommendation.** Reword E2 to "is a top-level Claude session; tool parity not yet tested", and add tool parity to AC-0.4.

### F10. AC-0.4 claims a check that step 5 does not perform (follow-up, Medium)

- **Issue.** AC-0.4 requires each run to be "directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript)" (`spec:194`). Step 5 searches only for `AskUserQuestion` (`spec:184`). Nothing in 7.2 checks for an Agent-tool wrapper.
- **Recommendation.** Add an explicit transcript check for an Agent-tool call wrapping the command, or drop the claim.

### F11. The D1 example needs an output flag that section 3.1 does not give troubleshoot (follow-up, Medium)

- **Issue.** The D1 example runs `/sc:troubleshoot "login fails" --unattended --output .dev/troubleshoot/login/` (`spec:228`). The 3.1 row for troubleshoot lists only "no `--fix`" as its brief flags (`spec:91`). The inventory gives only a default output folder (`INV-B:242`, `cmd/troubleshoot.md:56`). So the spec does not show that troubleshoot takes `--output`.
- **Recommendation.** Confirm the flag exists (or name what the command accepts) and add it to the troubleshoot row.

### F12. The heartbeat boundary is not covered at exactly 5 minutes (follow-up, Medium)

- **Issue.** WC-10 splits waits "longer than 5 minutes" and says the worker "sends a heartbeat every 5 minutes" (`spec:68`). A single call of exactly 300 s is not split, and the heartbeat cadence (`CAPS:130`) is not enforced. Whether Orca uses heartbeat age for liveness is UNVERIFIED (`CAPS:130`).
- **Recommendation.** Use "5 minutes or longer" for the split, and state the heartbeat is advisory until the liveness question is tested.

### F13. cli-portify's hardcoded template path is not in any phase (follow-up, Medium)

- **Issue.** Section 3.2 lists "dispatch only inside an IronClaude checkout (hardcoded template path)" as a required change (`spec:105`; `INV-A:45`, `INV-A:68`). P2's scope covers gates and wait splitting only (`spec:160`), so the change is not scheduled.
- **Recommendation.** Add it to P2 or P3, or record it as deferred.

### F14. The P0 mirror count is ambiguous (minor)

- **Issue.** P0 says the Orca section goes into HOW-WE-WORK.md "and its two mirrored copies" (`spec:158`). AC-0.2 compares only one plugin copy and "the level-table test" (`spec:192`). The count of mirrors is not stated.
- **Recommendation.** List the two copies by path.

### F15. The ask default timeout is UNVERIFIED and not bounded (minor)

- **Issue.** WC-3 says a timeout "resumes the same message ID" (`spec:61`). The default `--timeout-ms` when omitted is UNVERIFIED (`CAPS:68`), and the spec does not set one in the brief.
- **Recommendation.** Put an explicit `--timeout-ms` in the brief template (2.3).

---

=== ARCHITECTURE ANALYSIS ===

Architecture findings are F2, F3, F5, F7, F9, F11, F12 and F13, grouped above by expert. The main architectural points I checked:

- The core decision (Orca coordinates, commands stay units of work, no Orca call in commands) is consistent with the cited depth limit (`CAPS:97-101`) and the top-level rule (`CAPS:161`). The depth-1 argument in R1 (`spec:33`) rests on an enforcement point the spec itself marks UNVERIFIED (`CAPS:103`). That is flagged honestly and I do not count it as a defect.
- The shared core file `~/.claude/WORKER-CONTRACT.md` follows the installed-path rule, so no `src/superclaude` path reaches an installed command. I did not verify `KNOWN_CORE_FILES` (`spec:52`, UNVERIFIED-direct).
- The 10 / 27 / 6 split matches the counts in the inventories (`INV-A:73`, `INV-B:278`), with 5 + 5 ready, 13 + 14 needs-change and 3 + 3 coordinator-only. The spec's section 3 header (`spec:75`) is correct.
- The contract vocabulary (four statuses mapped to two Orca outcomes, `CAPS:73`) is clear, but its mapping has the gaps in F6 and F8.

---

=== ADVERSARIAL ANALYSIS (Whittaker, always active) ===

- I can break this specification by **Sequence Attack (FR-2.4)**. The invariant at **WC-3 (spec:61)** fails when **the worker is in an `ask` that times out and then re-invokes the command with the answer**. Concrete attack: the worker asks the coordinator at the implement halt (`spec:109`). The coordinator, an agent, answers "proceed". The worker re-invokes `/sc:implement` with that answer as a flag. Before: the Ruling rule is in force and the ledger records a halt. After: the ledger records the coordinator's words as a Ruling, and the run completes. This is F1.
- I can break this specification by **Zero/Empty Attack (FR-2.1)**. The invariant at **WC-5 (spec:63)** fails when **the contract has no status**. Concrete attack in F8.
- I can break this specification by **Divergence Attack (FR-2.2)**. The invariant at **WC-5 (spec:63)** fails when **the status is `partial` and `blocked_question` is also set**. Concrete attack: the contract reads `status: partial` with an open question. The mapping sends succeeded, and the open question is not carried into the Orca outcome. This is F6.
- Sentinel and accumulation attacks did not produce a new finding; the blocked and failed values map consistently (`spec:63`).

---

=== GUARD CONDITION BOUNDARY TABLE ===

Trigger: the spec contains conditional logic (WC-2 gate resolutions, WC-5 mapping, WC-10 threshold, WC-4 path rule). The table is produced, not skipped. Pipeline Dimensional Analysis is not triggered: the spec has no multi-stage data flow whose item count changes (Task fan-out is a dependency graph, not a count transformation).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome | spec:63 | Zero/Empty (no report, no contract) | none | failed | "no report exists" maps to failed | OK |
| WC-5 outcome | spec:63 | One/Minimal (contract present, status absent or unknown) | status missing | otherwise branch | succeeded, undefined state (F8) | GAP (Medium) |
| WC-5 outcome | spec:63 | Typical (partial) | `partial` | succeeded | stated, harm assumes dependents start (F6) | GAP (Medium) |
| WC-5 outcome | spec:63 | Sentinel value (blocked) | `blocked` | failed | stated | OK |
| WC-5 outcome | spec:63 | Maximum/Overflow | not applicable: the status set is closed; out-of-set values are the row-2 case | n/a | n/a | OK (left out, reason given) |
| WC-4 path | spec:62 | Legitimate edge (file-valued `--output`, tdd and init-lite) | `--output <file>` | directory undefined | no path rule | GAP (blocking, F2) |
| WC-3 gate | spec:61 with spec:109 | Sentinel (coordinator answer relayed into halt) | answer text | re-invoke with answer as flag | implement row says Ruling unchanged | GAP (blocking, F1) |
| WC-3 ask | spec:61 | Zero/Empty (`--timeout-ms` omitted) | none | timeout unknown | resume by message ID | GAP (minor, F15) |
| WC-6 retry | spec:64 | Legitimate edge (`--retry-of` reuses output dir) | same dir | fresh dir required but no path rule | not stated | GAP (Medium, F7) |
| WC-10 wait | spec:68 | Boundary (wait exactly 5 min) | 300 s | not split; heartbeat not enforced | "longer than 5 minutes" | GAP (Medium, F12) |
| SA-1 flag | spec:146 | Zero/Empty (no `--unattended`) | none | today's behaviour | stated | OK |

---

=== SCORES (0-10, advisory) ===

Clarity 6, Completeness 6, Testability 4, Consistency 5. Testability is lowest because of F3, F4, F5 and F10.

---

## Follow-up candidates (Medium and minor, not blocking)

These are listed for the coordinator. The session that ran the review asks the user once per loop whether to open issues; none were created here.

- F6 partial maps to succeeded (spec:63, spec:263)
- F7 retry output directory rule (spec:64, spec:73)
- F8 missing or unknown status maps to succeeded (spec:63)
- F9 E2 tool parity overstated (spec:22)
- F10 AC-0.4 wrapper check not performed by step 5 (spec:184, spec:194)
- F11 troubleshoot output flag not in 3.1 row (spec:91, spec:228)
- F12 WC-10 boundary at 5 minutes (spec:68)
- F13 cli-portify template path not scheduled (spec:105, spec:160)
- F14 two mirrored copies not named (spec:158)
- F15 ask default timeout not set in brief (spec:61)

---

## Reviser brief

Blocking findings in this report: F1, F2, F3, F4, F5.

Restated rule (bullet 6 of the review loop): revise only text a blocking finding names. Add no rule, mechanism or section no blocking finding calls for. Each added paragraph or table cites its finding id. Prefer deleting or narrowing to adding. Report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings are not in this brief and are not to be edited.

---

## Findings block

```findings-v1
{"id": "F1", "severity": "CRITICAL", "blocking": true, "category": "safety", "anchor": "the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag", "anchor2": "the Ruling rule itself is unchanged (see open decision D2)", "refs": ["WC-3", "3.2 implement row", "D2", "INV-A:66"], "claim": "An implementer who follows WC-3 as written re-invokes /sc:implement with the coordinator's answer as the Ruling, which the qa.md:238 rule forbids while D2 is open."}
{"id": "F2", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "where `<output-dir>` is the directory the coordinator passed", "anchor2": "Fix the contract filename to `<output>/adversarial/return-contract.yaml`", "refs": ["WC-4", "2.3", "3.1 adversarial", "3.1 tdd", "3.1 workflow", "3.1 init-lite"], "claim": "An implementer who follows WC-4 as written cannot name a pre-dispatch contract path for tdd (file output), workflow (per-run id) or adversarial (subdirectory), which the 2.3 rule requires."}
{"id": "F3", "severity": "MAJOR", "blocking": true, "category": "unpassable-check", "anchor": "the worker reports the named file until Phase 1 adds the contract", "anchor2": "7.2 passes with `--outcome succeeded`", "refs": ["3.1 intro", "P1", "P2", "AC-2.3", "AC-1.2"], "claim": "An implementer who follows the phase table builds troubleshoot, tdd and release-split workers with no contract, so AC-2.3 fails on 7.2 step 4 for them."}
{"id": "F4", "severity": "MAJOR", "blocking": true, "category": "unpassable-check", "anchor": "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`", "anchor2": "the `--unattended` flag accepted by every command in sections 3.1 and 3.2", "refs": ["AC-1.1", "P1", "3.2 load", "3.2 validate-roadmap", "3.2 validate-tests"], "claim": "An implementer who runs AC-1.1 at the end of P1 gets failures for commands P2-P4 have not yet edited and for the three commands that have no contract."}
{"id": "F5", "severity": "MAJOR", "blocking": true, "category": "unpassable-check", "anchor": "(orchestration\\|worktree\\|terminal\\|agent)", "anchor2": "grep -v '^src/superclaude/skills/ccsession-tag/'", "refs": ["AC-C1", "SA-2", "WC-8", "P0"], "claim": "An implementer who runs AC-C1 as written sees no output for a real orca orchestration call, because the escaped pipes are literal in grep -E, so the SA-2 check passes falsely."}
{"id": "F6", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "`--outcome succeeded` otherwise, including `partial`", "anchor2": "A partial run left a usable deliverable", "refs": ["WC-5", "decision: partial maps to succeeded", "CAPS:85-86", "CAPS:92"], "claim": "A partial deliverable can settle as succeeded and make its dependents ready, which harms only if the coordinator skips the contract."}
{"id": "F7", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "A command either resumes from its on-disk state when given its resume flag, or, if it has none, writes each run into a fresh output directory so a re-run starts clean", "anchor2": "so the report path is known before dispatch (WC-4)", "refs": ["WC-6", "2.3", "CAPS:116"], "claim": "The spec gives no rule for choosing the fresh directory on a retry, so the pre-dispatch report path cannot be known for a retry."}
{"id": "F8", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "`--outcome failed` when the report says `failed` or `blocked`, or no report exists", "anchor2": "`--outcome succeeded` otherwise, including `partial`", "refs": ["WC-5", "7.2 step 4"], "claim": "A contract with a missing or unknown status falls into the success branch, which the spec leaves undefined."}
{"id": "F9", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "so a command run by a worker has the same tools as a command a person runs", "anchor2": "`CAPS:161` (`[H:worker-start]` line 38, `--agent claude`)", "refs": ["E2", "CAPS:161", "INV-A:112"], "claim": "E2 asserts tool parity that the cited evidence (top-level session only) does not show."}
{"id": "F10", "severity": "MAJOR", "blocking": false, "category": "unpassable-check", "anchor": "each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript)", "anchor2": "search the transcript for `AskUserQuestion`", "refs": ["AC-0.4", "7.2 step 5"], "claim": "AC-0.4 says step 5 verifies the absence of an Agent-tool wrapper, but step 5 only searches for AskUserQuestion."}
{"id": "F11", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "--unattended --output .dev/troubleshoot/login/", "anchor2": "| troubleshoot | no `--fix` |", "refs": ["D1", "3.1 troubleshoot", "INV-B:242"], "claim": "The D1 example passes --output to troubleshoot, but section 3.1 lists no output flag for it and the inventory names only a default folder."}
{"id": "F12", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "A command step that blocks a single tool call for longer than 5 minutes", "anchor2": "The worker sends a heartbeat every 5 minutes while working.", "refs": ["WC-10", "CAPS:130"], "claim": "A single tool call of exactly 300 s is neither split nor covered by a heartbeat, so the 5-minute cadence has a gap at the boundary."}
{"id": "F13", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "dispatch only inside an IronClaude checkout (hardcoded template path)", "anchor2": "Each default-on gate resolves per its section 3 row; WC-10 wait splitting for cli-eval.", "refs": ["3.2 cli-portify", "P2", "INV-A:45", "INV-A:68"], "claim": "The hardcoded template path is a required change that no phase schedules."}
{"id": "F14", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "add an Orca section to `HOW-WE-WORK.md` and its two mirrored copies", "anchor2": "AC-0.2", "refs": ["P0", "AC-0.2"], "claim": "The two mirrored copies are not named by path, so AC-0.2 checks one of them."}
{"id": "F15", "severity": "MINOR", "blocking": false, "category": "missing-requirement", "anchor": "On an `ask` timeout it resumes the same message ID and never creates a duplicate", "anchor2": "CAPS:68", "refs": ["WC-3", "CAPS:68"], "claim": "The default ask timeout is UNVERIFIED and the brief template does not set one."}
```

Verdict is FAIL: F1-F5 are open and blocking.

verdict: FAIL
