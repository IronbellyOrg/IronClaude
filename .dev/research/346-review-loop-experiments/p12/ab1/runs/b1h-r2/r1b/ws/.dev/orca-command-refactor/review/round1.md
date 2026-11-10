review: 1 of 3

# Spec-panel critique: orca-worker-contract-spec.md (round 1)

## Report header

- Command: `/sc:spec-panel` critique mode, focus `requirements,architecture`, FIRST-REVIEW prompt from `~/.claude/rules/prompts/document_review_loop_prompts.md` (sandbox copy at `home/.claude/rules/prompts/document_review_loop_prompts.md`).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (repo-relative; 286 lines), sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`.
- Baseline: none (first review; no `--re-review`, no `--baseline`).
- Reviewer model: claude-haiku-5-5. This is one reviewer. The three first reviews and the MERGE rule are the coordinator's step and were not run here.
- Panel: Wiegers (lead), Adzic, Cockburn (requirements); Fowler (lead), Newman, Hohpe, Nygard (architecture); Whittaker (active in every panel review). Crispin completes the Guard table, as the mandatory-artifact rules require.
- Pipeline Dimensional Analysis: not triggered. The spec describes no multi-stage data flow whose counts change.
- Coverage: read in full: `command.md` (sandbox copy of the `/sc:spec-panel` definition), `.dev/orca-command-refactor/README.md`, the FIRST-REVIEW prompt, the candidate, `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`. Not present in the sandbox and therefore UNVERIFIED: every `src/superclaude/...`, `tests/...`, `pyproject.toml`, `Makefile`, `plugins/...`, `CLAUDE.md:*` citation, and every `.dev/evals/...`, `.dev/codegraph-migration/...`, `.dev/research/...` citation. Those are marked as such below. I ran read-only grep tests in the sandbox (see B2).
- Ask-the-user step: the command asks the user once per loop whether to open issues for the Medium and minor follow-up candidates. A worker cannot ask a person here, so the list is recorded below and the question is left to the coordinator. No issue was created.

## Summary

The core decision in section 1 (Orca coordinates; commands stay units of work; no command calls Orca) is well argued and its citations to the inventories check out. The worker contract in section 2 and the acceptance checks in section 7 are where the defects are. Two rules contradict each other on who may authorize an outward action (B1). One acceptance check can never fail (B2). The outcome rule reports `succeeded` for an empty or unreadable contract (B3). Two acceptance checks cannot pass as written (B4, B5). Five findings are blocking. Medium findings are listed as follow-up candidates.

## Blocking findings

### B1. CRITICAL. WC-3 lets a coordinator answer add a flag; WC-9 says only the brief can turn on an outward action

- **Issue.** WC-3 says that after an ask the command is re-invoked "with the answer as a flag" (`spec:61`). WC-9 says an outward action "turns on only through the command's own explicit flag written in the brief" (`spec:67`). D4 says the coordinator may authorize outward actions only with the user's own instruction quoted in the brief (`spec:245-247`). The first two texts allow a flag that is not in the brief. The third forbids it.
- **Grading sentence.** An implementer who follows WC-3 on the post-release gate (`spec:113`, blocked on outward confirmations) re-invokes the command with an ask reply supplied as the push flag, and the outward push runs although no such flag is in the brief, which WC-9 (`spec:67`) forbids.
- **Expert.** Wiegers (contradictory requirements). Whittaker, FR-2.3 Sentinel Collision: a reply carries a value that an outward gate reads as authorization.
- **Recommendation.** Limit WC-3 answers to gate values that are not outward. Any outward flag comes only from the brief, as D4 says. Put that rule in WC-3 and WC-9 with the same wording.
- **Priority.** High. **Quality impact.** High: a safety-boundary risk.

### B2. CRITICAL. The AC-C1 grep cannot fail, so SA-2 and WC-8 have no working gate

- **Issue.** AC-C1 (`spec:172`) uses `\|` inside `grep -E`. In an extended regex `\|` is a literal bar, not alternation. I ran the pattern as written against a violating line, `orca orchestration check --json`, and it printed nothing (exit 1). The same pattern with plain `|` matched (exit 0). AC-C1 therefore passes on any command that calls Orca.
- **Grading sentence.** An implementer who adds `orca orchestration check` to a command and runs AC-C1 as written gets empty output and records SA-2 (`spec:147`) and WC-8 (`spec:66`) as passed.
- **Expert.** Wiegers (acceptance check). Crispin (completeness of the check).
- **Recommendation.** Use plain `|` inside the group. Add a positive control: the check must match a planted line in a scratch file. Re-run it before P0 is accepted.
- **Priority.** High. **Quality impact.** High: the hard boundary in section 5 has no working check.

### B3. MAJOR. WC-5 reports `succeeded` for a contract that is empty, unreadable or has an unknown status

- **Issue.** WC-5 sends `--outcome failed` only when the report says `failed` or `blocked`, or when no report exists. It sends `succeeded` "otherwise" (`spec:63`). A file that exists but is 0 bytes, is unparseable, or carries a status outside the four values matches neither failed trigger. Section 7.2 step 4 (`spec:183`) would catch it, but WC-5 does not.
- **Grading sentence.** An implementer who follows WC-5 with a zero-byte `return-contract.yaml` sends `--outcome succeeded`, since the file exists and its status is neither failed nor blocked.
- **Expert.** Whittaker, FR-2.1 Zero/Empty Attack. Nygard (guard boundary; see the table).
- **Recommendation.** Send `failed` when the contract is empty, unparseable, or has a status outside `succeeded|partial|failed|blocked`. Write that into WC-5 itself.
- **Priority.** High. **Quality impact.** High: a failed run reaches the coordinator as success, and dependents may start on it (M3).

### B4. CRITICAL. AC-1.1 cannot pass for `/sc:load`

- **Issue.** AC-1.1 (`spec:195`) requires every command in sections 3.1 and 3.2 to have a `## Unattended mode` section that names `return-contract.yaml`. The `load` row (`spec:112`) says the report is "none (see note)" and the Decisions table (`spec:265`) says a report file for load "would be an unrequested addition". Both texts are explicit.
- **Grading sentence.** An implementer who follows the load row writes no contract, so AC-1.1 fails on `load`, and the criterion cannot pass as written.
- **Expert.** Wiegers (traceability between decision and check).
- **Recommendation.** Exempt `load` from AC-1.1 by name, and say in P1 (`spec:159`) that load gets the flag as a usage-line fix only.
- **Priority.** High. **Quality impact.** Medium-high: an implementer stops at a failing gate or edits the check.

### B5. CRITICAL. AC-0.4 step 4 cannot pass for `/sc:troubleshoot` as written

- **Issue.** AC-0.4 (`spec:194`) says step 4 "uses the command's existing report file", because the contract arrives in P1. Step 4 (`spec:183`) asserts that the file is YAML with `status` in the four-value set and a `command` key. Troubleshoot's report is `REPORT.md` (`commands-b.md:49`, `:242`). Its `return-contract.yaml` appears only with `--caller task-unified` (`commands-b.md:242`). Workflow's `return-contract.yaml` does have a `status` (`commands-b.md:272`), but its values are not listed in the inventory (UNVERIFIED).
- **Grading sentence.** An implementer who runs step 4 on the troubleshoot `REPORT.md` gets a YAML or missing-key error, so AC-0.4 cannot pass for that command.
- **Expert.** Adzic (example check that does not match its own data). Wiegers (acceptance criteria).
- **Recommendation.** Limit step 4 in P0 to commands whose existing report is YAML with the four-value status, or check file presence only for the rest. Name which commands use which form.
- **Priority.** High. **Quality impact.** Medium-high: the P0 phase gate cannot close.

## Guard Condition Boundary Table (mandatory artifact)

Triggered: the spec contains conditional logic, threshold checks and gate resolutions (WC-2, WC-3, WC-4, WC-5, WC-6, WC-9, WC-10, WC-11, WC-12). Focus is not `correctness`, so the State Variable Registry is not required. FR-8 and FR-9 grading is applied to each GAP row. The table is complete under FR-10: each guard that carries conditional logic has at least one row. Input classes left out, with reasons: Maximum/Overflow for WC-5 (no numeric input) and WC-12 (no capacity input). WC-1, WC-7 and WC-8 carry no run-time guard.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome | `spec:63` | Zero/Empty | contract present, 0 bytes | not failed, not blocked | `succeeded` by the word "otherwise" | GAP, blocking (B3) |
| WC-5 outcome | `spec:63` | One/Minimal | `status: partial` | `succeeded` | defined (`spec:263` decision) | OK |
| WC-5 outcome | `spec:63` | Typical | `status: succeeded` / `failed` / `blocked` | `succeeded` / `failed` / `failed` | defined | OK |
| WC-5 outcome | `spec:63` | Sentinel Value Match | `status: "complete"` (outside the four values) | unspecified | unspecified | GAP, blocking (B3, same defect) |
| WC-5 outcome | `spec:63` | Legitimate Edge | `status: blocked`, `blocked_question` empty | `failed` | `failed`; empty question has no rule (`spec:62` requires the field) | GAP, Medium (M19) |
| WC-5 outcome | `spec:63` | Legitimate Edge | no report file | `failed` | defined | OK |
| WC-2 gate (b) | `spec:60` | Zero/Empty | `--output` absent under `--unattended` | no contract path | unspecified (WC-4 presumes it) | GAP, Medium (M19) |
| WC-2 gate (b) | `spec:60` | Invalid | malformed flag value, for example `--target-release` | unspecified | unspecified | GAP, Medium (M19) |
| WC-3 ask | `spec:61` | Maximum (no bound) | coordinator never answers | resume the same message ID, indefinitely | no maximum, no give-up path | GAP, Medium (M6) |
| WC-3 / WC-9 | `spec:61`, `spec:67` | Sentinel Value Match | reply carries an outward flag | WC-3 re-invokes with it; WC-9 requires the brief | the two rules conflict | GAP, blocking (B1) |
| WC-6 retry | `spec:64` | Legitimate Edge | retry with the same `--output` | fresh directory vs the passed directory | who creates the fresh directory is not stated | GAP, Medium (M5) |
| WC-11 | `spec:69` | Legitimate Edge | two workers on a fixed path (`spec:85`, `spec:86`) | "must never" write the same file | serialization by the coordinator is not a stated rule | GAP, Medium (M4) |
| WC-10 | `spec:68` | Boundary | one blocking tool call of 4 to 5 minutes | neither split nor forbidden | heartbeat cadence 5 minutes (`orca-capabilities.md:130`) | GAP, note (N1) |
| WC-12 | `spec:70` | Typical | `check` returns `consumer_fenced` | stop, no `worker_done` | defined | OK |
| WC-12 | `spec:70` | Zero/Empty | `check` returns no rows | no change | defined by Orca (`orca-capabilities.md:67`) | OK |

FR-8 count: 10 GAP rows. Blocking: 3 rows (two WC-5 rows, both B3, and the WC-3/WC-9 row, B1). Medium: 6 rows (M4, M5, M6, and M19 for the blocked-with-empty-question, missing-output and invalid-value rows). Note: 1 row (N1). FR-9 (blank Specified Behavior): no blank cells; the "unspecified" entries are graded under the GAP rows above.

## Medium findings (follow-up candidates, not blocking)

- **M1. Requirement with no owner and no check: WC-1.** WC-1 (`spec:59`) names "Launch setup, not commands" as its owner. No phase (`spec:158-162`) and no acceptance check (`spec:191-210`) covers it. Experts: Wiegers, Fowler. Recommendation: name the file that owns the launch path, and add an AC that plants a startup question and expects readiness within the limit (`orca-capabilities.md:44-46`).
- **M2. Session-start behavior in worker sessions is not addressed.** The inventory says `/sc:pm` "runs automatically at every session start" (`commands-b.md:70`), and the session-init banner prints at every session start, "Orca workers included" (`commands-a.md:69`). The spec classifies pm as coordinator-only (`spec:135`) but never says how a worker session avoids the always-on behavior. Experts: Nygard, Newman. UNVERIFIED: whether either runs as a hook (`cmd/pm.md` and `session-init.sh` are not in the sandbox).
- **M3. A partial result can release dependents before the contract is read.** WC-5 sends `succeeded` for `partial` (`spec:63`, decision `spec:263`). Orca keeps dependents blocked only after a failed or cancelled Task (`orca-capabilities.md:90`). A succeeded Task therefore lets its dependents become startable (an inference from `orca-capabilities.md:86, 88-90`). Section 2.3 says the coordinator opens the report "then releases or reuses the worker" (`spec:73`). It does not require the report to be read before a ready dependent starts. Experts: Hohpe, Nygard. Recommendation: hold dependents on a partial outcome until the contract is read, or add a gate.
- **M4. WC-11 is not met by the fixed default paths.** WC-11 says default paths "carry a timestamp or the slug the coordinator passes" (`spec:69`). `cleanup-audit` keeps `.claude-audit/` fixed and says "one audit per worktree at a time" (`spec:85`). `index-repo` writes fixed `PROJECT_INDEX.md` (`spec:86`). "One at a time" is a coordinator rule, not a WC-11 rule, so two workers can still write the same file. Experts: Fowler, Whittaker.
- **M5. Retry directory rule is missing.** WC-6 says a re-run writes "into a fresh output directory" (`spec:64`). WC-4 puts the contract in the directory the coordinator passed (`spec:62`). The brief rules (`spec:73`) do not say a retry gets a new `--output`. Expert: Fowler.
- **M6. WC-3 has no bound and no order.** The ask waits and resumes by message ID (`spec:61`). The spec gives no maximum wait and no give-up path. The default ask timeout is UNVERIFIED (`orca-capabilities.md:68`; `spec:281`). If the coordinator never answers, the worker stays parked with no outcome. The spec also does not order the ask against `worker_done`. Whittaker, FR-2.4 Sequence: if `worker_done --outcome failed` is sent first, the dispatch settles and the worker idles (`orca-capabilities.md:77-78`), so the ask cannot follow. Experts: Nygard, Whittaker.
- **M7. WC-7 has no mechanical check, and AC-0.4 claims one.** AC-0.4 says "no Agent-tool wrapper, verified in the step-5 transcript" (`spec:194`). Step 5 (`spec:184`) searches only for `AskUserQuestion`. WC-7 (`spec:65`) has no acceptance check. Expert: Wiegers.
- **M8. P0 builds before it tests.** Section 1.4 says Phase 0 "starts with live smoke runs" (`spec:43`), and the Decisions row says "Phase 0 tests the decision first ... before anything is built on it" (`spec:269`). P0 (`spec:158`) writes the contract, the `KNOWN_CORE_FILES` entry, the routing-guide edit and a test file, and then runs the smoke tests ("Then run"). AC-0.4 says a failure "reopens section 1" (`spec:194`), which would strand those edits. Expert: Fowler.
- **M9. SA-2 contradicts AC-C1 about mentioning Orca.** SA-2 says "the only allowed mention of Orca in a changed command is ... inside the contract file" (`spec:147`). A command cannot mention Orca "inside the contract file". AC-C1 (`spec:172`) and the Unattended-mode text (`spec:52`) do not settle whether a command may name Orca at all. Expert: Wiegers. Recommendation: state that commands never name Orca and only the contract file may.
- **M10. The status vocabulary and contract version are not reconciled.** WC-4 fixes four status values (`spec:62`). Commands that already write a contract keep their own fields (`spec:62`). Workflow's contract is "contract 1.1" with a `status` (`commands-b.md:272`), and its values are not in the inventory (UNVERIFIED). WC-4 has no version field. AC-1.4 (`spec:198`) checks file names, not values. Expert: Newman.
- **M11. P1 wording suggests the contract is skipped for gate-free commands.** P1 says the flag is "a no-op where a command has no gate" (`spec:159`). WC-4 requires the contract in unattended mode for every command (`spec:62`), and AC-1.2 checks it (`spec:196`). Gate-free rows (`spec:99`, `spec:101`) could be read as no contract. Expert: Wiegers.
- **M12. The headless trigger under `--unattended` is undefined.** SA-6 says `--unattended` "reuses" the headless rule (`spec:151`). P2 says that under `--unattended`, `--remediate` "follows the existing headless auto-accept rule" (`spec:88`). The inventory says that rule keys on `claude --print` without a TTY (`commands-b.md:109`; decision at `commands-b.md:310`). The spec never says `--unattended` sets that condition. The flag therefore acts as a control signal that auto-accepts a remediation offer the spec never names. Expert: Whittaker, FR-2.3.
- **M13. An unverified premise is stated as fact in the tasklist row.** The row says no change is needed because reflect "runs one layer below the worker, inside Claude Code's nesting limit" (`spec:122`, citing INV-A:14). Commands-b marks nested spawning and answering the remediation offer as UNVERIFIED (`commands-b.md:314`, `:322`). Expert: Nygard.
- **M14. Plugin mirror not covered.** UNVERIFIED item 8 leaves the update rule for `plugins/superclaude/commands/` open (`spec:279`). AC-C2 checks only `make verify-sync` (`spec:173`). Command edits can leave the plugin copies stale. Experts: Fowler, Wiegers.
- **M15. Dependence on an installed core file with no fallback.** Unattended commands point to `~/.claude/WORKER-CONTRACT.md` (`spec:52`). An older install lacks it. No detection or fallback is specified, and AC-1.1 checks only that the path is named. Expert: Newman.
- **M16. "Exactly once" has no idempotency key.** WC-5 requires exactly one `worker_done` (`spec:63`). Orca mutations accept `--retry-request` (`orca-capabilities.md:117`), and the spec does not require it for `worker_done`. A retried send after a lost response could duplicate it. Expert: Hohpe.
- **M17. Traceability from requirements to checks is incomplete.** WC-1 (`spec:59`), WC-6 (`spec:64`), WC-7 (`spec:65`), WC-11 (`spec:69`) and WC-12 (`spec:70`) have no check in sections 7.1 to 7.3 that covers all the commands they name. WC-10 is checked only for pr-submit (`spec:210`), not for cli-eval, which section 3.2 also changes (`spec:104`). Expert: Wiegers.
- **M18. Only two designs are compared.** Section 1.3 rejects one alternative (commands call Orca). The existing Orca-aware launcher, `ccsession-tag` (E5, `spec:25`), is never evaluated as a possible bridge for unattended launches. Expert: Fowler.
- **M19. Unattended gate inputs with no defined behavior.** A missing `--output` under `--unattended` and a malformed gate value (for example `--target-release`) have no specified outcome (`spec:60`, `spec:62`). This is the GAP group in the table above. Expert: Crispin.

## Notes (minor)

- **N1.** WC-10 (`spec:68`) splits only calls "longer than 5 minutes". A blocking call of 4 to 5 minutes is neither split nor limited, and the heartbeat cadence is 5 minutes (`orca-capabilities.md:130`). Expert: Whittaker, FR-2.2.
- **N2.** E2 (`spec:22`) says a worker "has the same tools as a command a person runs". Subagent tool availability is UNVERIFIED (`orca-capabilities.md:159-160`; `commands-a.md:112`). Soften the wording.
- **N3.** Non-goal 3 (`spec:215`) cites `CAPS:12-13` for Orca's coordinator guide. Those lines are the source-key table (`orca-capabilities.md:12-13`), not guide text.
- **N4.** AC-1.3 (`spec:197`) uses `claude -p`. That is print mode, the condition reflect's headless rule keys on (`commands-b.md:109`). Use an interactive invocation for the plain-session check.
- **N5.** E4 (`spec:24`) says Agent-tool subagents "are not counted by Orca's nesting limit". The inventory supports this only as an inference from the depth code's scope (`orca-capabilities.md:155`).
- **N6. Advisory.** The spec has numeric thresholds and several guards (`spec:61`, `spec:68`, `spec:183`). The command's advisory auto-suggestion for `--focus correctness` may apply. This is a recommendation only.

## Citation check

- Checked against the inventories, with the spec's citation confirmed: `CAPS:44-46` (60 s readiness), `CAPS:52` (waiting worker healthy), `CAPS:58-61` (ask), `CAPS:67` (empty check), `CAPS:73` (outcome), `CAPS:76-78` (pane binding, settlement, idle), `CAPS:80` (circuit breaker), `CAPS:86`, `CAPS:88-90` (waves, dependents), `CAPS:97-101` (depth), `CAPS:107-113` (release), `CAPS:115-117` (placement, retry, `--retry-request`), `CAPS:130`, `CAPS:145-149`, `CAPS:155`, `CAPS:161`. Also `INV-A:14, 35, 38, 62, 69, 95, 96`; `INV-B:49, 70, 109, 242, 272, 310, 314, 322`. Spot-checked against the inventory text; each matched the spec's description.
- Not checkable in the sandbox, so UNVERIFIED: every `src/superclaude/...` path and line (E5, section 3 rows, `install_core.py`), `CLAUDE.md:*`, `pyproject.toml:38`, `plugins/...`, `tests/...`, and `.dev/evals/...`, `.dev/codegraph-migration/...`, `.dev/research/...`. The spec's own claim that its citations were re-checked on 2026-11-02 (`spec:11`, `spec:285`) cannot be verified here.

## Reviser brief

Blocking findings: B1, B2, B3, B4, B5 only. Medium and minor findings are excluded.

Restated rule (`command.md` Review Loop, bullet 6): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with bytes added and deleted per finding id. Precedence (bullet 7): this brief does not grade any Medium or minor finding as blocking, and it does not authorize editing one.

Next step: the VERIFY prompt, in a fresh context that sees only the candidate and the blocking list, before any revision.

verdict: FAIL
