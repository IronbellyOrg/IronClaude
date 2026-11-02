<!-- Provenance: This document was produced by /sc:adversarial, Step 5 (merge execution) -->
<!-- Base: Variant 1 (variant-1-original.md, option a, keep depth 1; combined score 0.827) -->
<!-- Plan: refactor-plan.md (19 Planned Changes, auto-approved 2026-11-02, after one rf-analyst review) -->
<!-- Merge date: 2026-11-02T18:12:51Z -->
<!-- "Change N" in this document means Change N of refactor-plan.md. "MN" means section MN of this document. -->

# D5 option (a): keep Orca's nesting depth at 1

## M1. Position

<!-- Source: Base (original), V1:3 -->
Position: workers may not start workers. Fan-out stays inside a command (Agent-tool subagents) or is split into separate Tasks by the coordinator (`SPEC:352`; `SPEC:42`). This is the spec's current recommendation.

<!-- Source: Base (original, modified): V1:5 citation key extended with the keys refactor-plan.md uses (plan Overview, citation key line) -->
Citation key: `SPEC:N` = spec line, `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `CR-01:N` = `.dev/orca-command-refactor/changes/CR-01-feature-worktree-hierarchy.md:N`; `V1:N` / `V2:N` = line of `variant-1-original.md` / `variant-2-original.md`; `R1-V1`, `R1-V2`, `R2-V1`, `R2-V2` = round files `rounds/r1-variant-1.md`, `rounds/r1-variant-2.md`, `rounds/r2-variant-1.md`, `rounds/r2-variant-2.md`; `DA` = `diff-analysis.md` (diff point IDs such as A-001, C-004, X-003); `INV-NNN` = `invariant-probe.md`; `AR-N` = accepted-risk or open entry in M11. All files without a directory are in `.dev/orca-command-refactor/decisions/D5/debate/adversarial/`.

## M2. Precondition

<!-- Source: refactor-plan.md Change 1 (invariant-probe.md INV-001, HIGH; CAPS:97, CAPS:101, CAPS:103; fixed constraint CR-01:15, CR-01:16, 22) -->
- Option (a) works only if the coordinator is depth 0. The coordinator must be a session the person opened (depth 0), in the feature's top-level worktree (`CR-01:15`); it must never be started with `worker-start`.
- Why: Orca counts root coordinators as depth 0 and the first generation of workers as depth 1 (`CAPS:97`). A coordinator that was itself started by `worker-start` is depth 1, so under a maximum of 1 its own `worker-start` calls are refused (presumed, `CAPS:103`), and opening a new Run does not help, because a new Run does not reset depth (`CAPS:101`).
- CR-01 child worktrees are created by that coordinator with `worker-start --worktree new-child`, so every worker in a child is still depth 1; "child worktree" is placement, not nesting (`CR-01:16, 22`).
- How Orca assigns depth to a session a person opens is not traced; depth 0 is presumed from `CAPS:97` (UNVERIFIED). AC-0.7 (Change 15, M9) traces it; until then it is open under AR-1 (M11).

## M3. Safety

<!-- Source: Base (original, modified): V1:8 "its fence against runaway fan-out" replaced per Change 3 (DA A-001 CONTRADICTED, C-001; INV-007); base quotes of CAPS:97, CAPS:99, CAPS:100, CAPS:101 kept as confirmed in the plan's citation audit -->
- Depth 1 is Orca's default and the tightest setting: it allows one generation of workers. "1 means a coordinator dispatches workers and those workers may not dispatch further" (`CAPS:97`). A raise to 2 allows one more generation; the refusal still fires at the new maximum ("not permitted at depth ${childDepth} (max ${maxDepth})", `CAPS:99`) and bad values fall back to 1: a malformed setting "falls back to the default rather than disabling the fence" (`CAPS:99-100`). A new Run does not reset depth (`CAPS:101`). Orca's advice at the limit is "Do the work in this terminal" (`CAPS:99`).
- Depth does not limit how many workers one generation has. At depth 1 Orca puts no cap on how many workers the coordinator starts; the only numeric cap in the spec is the contract's fan-in limit of 10 merge inputs (`SPEC:87`), which limits only the inputs to one merge Task. D5 does not change width under either option (INV-007).

<!-- Source: Base (original, modified): V1:8 refusal presented as enforced; sentence appended per Change 4 (V2:16; DA U-007; CAPS:103; SPEC:387; INV-004, HIGH) -->
- Which Orca calls check the depth was not traced: `worker-start` and `dispatch` are presumed, `task-create` from a depth-1 worker is unknown (`CAPS:103`). AC-0.7 (Change 15) traces them. A read-only grep by the orchestrator on 2026-11-02 found three files that raise or name the refusal (`out/shared/nested-worker-depth.js`, `out/cli/bundled-skill-guides.js`, and the minified `out/main/chunks/orcad-migration-source-retention-BKoqlqOo.js`); which verbs reach the check was not traced (UNVERIFIED).

<!-- Source: Base (original, modified): V1:9 "machine-wide, not per run" made per-profile per Change 7 (DA A-004; INV-009); base citation of orca-data.json:1 and CAPS:98 kept -->
- The setting is per Orca profile and applies to every run under that profile; `local-default` is the only profile on this machine, so today a raise affects every Orca run here. The value lives in the profile file (`/home/coder/.config/orca/profiles/local-default/orca-data.json:1`, `"nestedWorkerMaxDepth":1`, `CAPS:98`). No per-run override was found (inferred, not proven).

<!-- Source: refactor-plan.md Change 17 (INV-017, HIGH; DA A-003; R2-V1 A-003; R2-V2 A-003): the unproven "mechanical backstop" reason is dropped -->
- The guard on worker fan-out under (a) is WC-13 (Change 13: the worker session never starts Orca work) and the 7.2 step 5 transcript check (Change 18), plus Orca's refusal for each call AC-0.7 confirms. Depth 1 alone is not proof that a worker cannot start Orca work: INV-017 lists eight routes, and six were open or unverified when the probe ran; Change 14 closes route (c) and Change 13 closes route (h), and the rest are open under AR-1 to AR-3 (M11).
- The asymmetry between the options is kept only as "presumed": at depth 1 Orca is presumed to refuse direct dispatch from any worker of any run; under (b) only IronClaude briefs would carry a restraint.

## M4. Reliability

<!-- Source: Base (original, modified): V1:12 last sentence replaced per Change 5 to restore the dropped UNVERIFIED caveat of CAPS:155 (DA spot-check 4; R1-V1 concession 2; R2-V1 item 4; DA C-011) -->
- Nothing in the spec needs depth 2: commands never call Orca (WC-8, SA-2 at `SPEC:72`, `SPEC:170`), and the coordinator gets per-unit Task records by splitting work into Tasks (`SPEC:42`). Agent-tool subagents are not Orca workers, so the depth fence does not count them; that Orca never limits them is UNVERIFIED (`CAPS:155`). Orca shows them only as sidebar child rows, not Tasks (`CAPS:157`).

<!-- Source: Base (original), V1:13 -->
- The rejected design that depth 2 would enable fails for reasons depth does not fix: standalone use breaks without Orca (R2), a command cannot own `worker_done` (R3), the executable name differs by platform (R4), and a second orchestrator competes with the coordinator (R5) (`SPEC:37-40`).

### What option (a) gives up

<!-- Source: Variant 2, "Strongest case for it" (V2:7-8), merged per Change 6 (DA U-005, S-001, X-002; R1-V1 concession 3; R2-V1 item 11); liveness corrected per DA C-004, R2-V1 item 6, INV-016 (CAPS:64, SPEC:74) -->
Two costs are real:

1. Fan-out that stays inside one command run (for example troubleshoot Tier 2) has no Orca Task, Dispatch, liveness or independent retry, and WC-10's heartbeat gap stays accepted (`SPEC:74`).
2. A split a worker discovers at run time is planned by the coordinator after it reads the result, which costs one extra coordinator round trip.

D5 does not change cost 1 under either option, because depth cannot reach a command's Agent-tool fan-out (DA C-005, X-003). A worker blocked in `check --wait` is live (`CAPS:64`), so the heartbeat gap does not move to a parent.

## M5. How a person works day to day

<!-- Source: Base (original), V1:16 -->
- No change. The coordinator plans fan-out as Tasks (for example N troubleshoot workers then one adversarial merge, `SPEC:87`).

<!-- Source: refactor-plan.md Change 1 (INV-001; CR-01:15, CR-01:16, 22): the M2 precondition as a working habit -->
- The person opens the coordinator session themselves, in the feature's top-level worktree, and never starts it with `worker-start` (M2). Child worktrees are where that coordinator places workers, not a deeper level of workers.

## M6. Implementation cost

<!-- Source: Base (original, modified): V1:19 "Raising depth later is one desktop setting" replaced per Change 2 (DA C-008, A-006; R1-V1 concession 5; R2-V1 item 10; R2-V2 item 13); the V1:19 revisit trigger removed per Change 10 and moved, rewritten, to M8 -->
- Zero for the setting itself. Raising the value is one desktop setting (`CAPS:99`). Lowering it again while deeper workers are running is UNVERIFIED, so a raise is made only on the evidence in M8.
- The spec changes in M9 (Changes 10, 12-16, 18 and 19) add requirements or checks to the spec; the plan rates them Medium risk and leaves them to the next consolidated spec revision (`CR-01:3`).

## M7. If (b) is ever chosen

<!-- Source: refactor-plan.md Change 8 (R1-V2 Position summary; R2-V1 and R2-V2 Overall recommendation; DA A-002; INV-008) -->
If (b) is ever chosen, it is not section 1.3's design (commands calling Orca). Both advocates agree it would take this scoped form: depth exactly 2; only a worker's top-level session starts sub-workers; only when its brief carries `Sub-workers: allowed, max N`; no command file changes, so SA-2 and WC-8 hold. This route avoids R2-R4 (`CAPS:148`, `CAPS:150`, `CAPS:145`; R2-V1 item 8). A maximum of 2 admits depth-2 children and refuses depth 3 (`CAPS:97`, `CAPS:99`; INV-008).

<!-- Source: Variant 2 (V2:19, V2:22) and the rebuttals, merged per Change 9 (DA U-006, U-008, C-007, C-009; R2-V1 New evidence 1-4; R2-V2 New evidence 1) -->
The setting is trivial; using it is not. The costs of (b):

- **A new brief type.** The brief carries "the exact command line" (`SPEC:79`), so a worker that plans its own fan-out is a new composite brief type with contract text and tests.
- **The parent inherits the coordinator loop.** It starts each sub-worker (`CAPS:92`), makes one release-or-retain decision per settled sub-worker (`CAPS:107`), may not end its turn while any is `reclaimable` (`CAPS:113`), and is subject to the three-failure circuit breaker (`CAPS:116`). It becomes a second orchestrator (R5, `SPEC:40`).
- **Questions probably go to the coordinator.** A question from an active Dispatch defaults to its owning Run mailbox (`CAPS:59`), and a Run is the coordinator's inbox (`CAPS:92`), so sub-worker questions would probably reach the coordinator, not the parent; delivery to the parent is UNVERIFIED (R2-V2 New evidence 1; DA C-004 evidence).
- **The restraint is narrower than the setting.** The brief line restrains only IronClaude workers, while the raised value applies to every run under the profile (R2-V1 New evidence 4).
- **WC-13 would have to be relaxed** for briefs carrying the `Sub-workers:` line (Change 13).
- **The saving is small:** one coordinator wake, read and `task-create` per run-time split (R2-V1 New evidence 3; R2-V2 item 7).

<!-- Source: Variant 2 Round 2, merged per Change 11 (R2-V2 Overall recommendation item 4; R2-V2 New evidence 1; R2-V1 critique (iv); CAPS:59, CAPS:103; SPEC:387) -->
Before any raise:

1. The refusal call sites and `task-create` at depth 1 are traced. AC-0.7 (Change 15) does this anyway under (a).
2. Which mailbox receives a depth-2 worker's questions and `worker_done` is established, because the parent's fan-in depends on it and the sources suggest it is the coordinator's Run mailbox (`CAPS:59`).

## M8. Revisit trigger

<!-- Source: refactor-plan.md Change 10 (R1-V2 W3; R2-V1 item 3; R2-V2 New evidence 2 and Overall item 3; INV-010, INV-011; SPEC:83, SPEC:181); replaces the trigger removed from V1:19 -->
Revisit D5 only when both conditions hold together:

1. A composite brief type is defined in this spec. With the one-command brief no worker session has fan-out to start (INV-011).
2. The coordinator's run notes (section 2.3) record a real run whose split was knowable only at run time and whose extra round trip was material.

The base's old trigger, "if P0 smoke runs (`SPEC:181`) show coordinator-side splitting is inadequate", could not fire: the P0 smoke runs are three single-command workers with no run-time split. Today nothing records such a split either: the run notes record only partial-usability judgements (`SPEC:83`), so the evidence set would stay empty (INV-010). M9 edit 5 adds the run-notes line that collects this evidence.

## M9. Spec changes this decision needs

<!-- Source: refactor-plan.md "Corrected D5 Wording", list "Other spec edits this decision needs" (items 1-10), with the full text of Changes 10, 12, 13, 14, 15, 16, 18 and 19 -->
These edits go into `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` in the next consolidated spec revision (`CR-01:3`). D5 itself (`SPEC:350-354`) is replaced in full by M10. Table rows below are shown in `text` blocks so their pipes and backticks are exact; commands are in `sh` blocks copied from the plan.

### Edit 1: E4 (`SPEC:27`)

<!-- Source: refactor-plan.md Change 12 (R2-V2 New evidence 3; INV-012; DA spot-check 4) -->
Replace "are not counted by Orca's nesting limit." with "are not counted by Orca's nesting limit; that Orca never limits them is UNVERIFIED."

### Edit 2: R1 (`SPEC:36`)

<!-- Source: refactor-plan.md Change 12 -->
Replace "The two designs exclude each other unless the user raises the depth setting." with "Raising the depth would not make this design viable: R2-R5 still apply, and depth cannot reach a command's Agent-tool fan-out (D5)."

### Edit 3: Non-goal 2 (`SPEC:315`)

<!-- Source: refactor-plan.md Change 12 and Change 1 -->
Replace "Nesting depth stays 1 unless the user decides otherwise (D5)" with "Nesting depth stays 1 unless the user decides otherwise, and the coordinator is a session the person opened, never one started by `worker-start` (D5)".

### Edit 4: Section 2.2 new row WC-13; section 2.1 contract-file list

<!-- Source: refactor-plan.md Change 13 (INV-005, INV-013, INV-017 route (h); SPEC:72, SPEC:170, SPEC:67-76; CAPS:101, CAPS:139) -->
New row after WC-12 (`SPEC:76`):

```text
WC-13 | **No Orca fan-out from the worker session.** The worker's top-level session never calls `worker-start`, `dispatch` or `task-create`, Orca's low-level dispatch, or `orca-cli` `worktree create --agent` or `agent launch`, at any depth setting. Work it finds that needs another worker is stated in its `worker_done` body; the coordinator decides (section 2.3). | Worker session | `CAPS:97-103`, `CAPS:139`; INV-005
```

Add WC-13 to the worker-session duties named in the section 2.1 contract-file list (`SPEC:58`). Because AC-0.1's test asserts that the contract file states each rule section 2.1 assigns to it (`SPEC:251`), that test then asserts WC-13 too; no separate AC-0.1 edit is needed beyond the list.

### Edit 5: Section 2.3 run-notes line and coordinator Task-ownership bullet

<!-- Source: refactor-plan.md Change 10 (run-notes line; SPEC:83) and Change 14 (INV-014, INV-017 route (c); CAPS:86, CAPS:92, CAPS:103; SPEC:81-85, SPEC:387) -->
Add to the section 2.3 run notes:

> In its run notes the coordinator also records each follow-up Task it created because a worker's result showed work that could not be planned before dispatch, with the extra time that cost. This is the evidence D5's revisit trigger reads.

Add a bullet to section 2.3 "Reading a result before anything depends on it":

> The coordinator starts only Tasks it created itself. A ready Task it did not create is not started; it is reported to the person with its spec text.

### Edit 6: Section 7.1, AC-C1 widened and new AC-C6

<!-- Source: refactor-plan.md Change 19 (INV-006; SPEC:202, SPEC:205-211) -->
**AC-C1.** Replace the AC-C1 description at `SPEC:205` so it names the seven scanned directories and says the match ignores case. (The plan gives the content of this description, not its exact words.) Replace the block at `SPEC:206-211` with:

```sh
grep -rniE '\borca(-ide)?[[:space:]]+(orchestration|worktree|terminal|agent)\b' \
  src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core \
  src/superclaude/hooks src/superclaude/templates plugins/superclaude \
  | grep -v '^src/superclaude/skills/ccsession-tag/' \
  | grep -v '^src/superclaude/core/WORKER-CONTRACT\.md:' \
  | grep -v '^src/superclaude/core/HOW-WE-WORK\.md:' \
  | grep -v '^plugins/superclaude/core/WORKER-CONTRACT\.md:' \
  | grep -v '^plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK\.md:'
```

The two added exclusions cover the mirrored routing guide, which gains the Orca section in P0 (`SPEC:181`, `SPEC:252`), and a future plugin copy of the contract file (`plugins/superclaude/core/` holds copies of some core files; whether `WORKER-CONTRACT.md` will be copied there is UNVERIFIED). Executable names held in variables stay out of reach of any grep; that residual is recorded under AR-2. The widened grep, run by the orchestrator on 2026-11-02 over all seven directories, printed nothing, so the change does not fail today's tree.

<!-- Source: refactor-plan.md Change 16 (INV-002, INV-017 route (g); CAPS:98-99; SPEC:315, SPEC:229-232, SPEC:251-256) -->
**AC-C6.** New common check after AC-C5 (`SPEC:229-232`), in the fenced style of AC-C1 to AC-C5:

> **AC-C6** (D5, non-goal 2). Pass: prints exactly one line per Orca profile and every line is `"nestedWorkerMaxDepth":1`. A profile whose file has no such key prints nothing for it; the phase report then records that profile as using Orca's default (1, `CAPS:97`), which is presumed, not read. Any other value fails the phase until the person confirms D5 was changed. Whether the running app re-reads the file is UNVERIFIED.

```sh
grep -ho '"nestedWorkerMaxDepth":[0-9]*' "${ORCA_RUNTIME_SOURCE_PROFILE_PATH:-$HOME/.config/orca}"/profiles/*/orca-data.json
```

(`ORCA_RUNTIME_SOURCE_PROFILE_PATH` is `/home/coder/.config/orca` here, `CAPS:98`; `-h` drops file-name prefixes when there are several profiles.) The exact command was run on 2026-11-02 and printed `"nestedWorkerMaxDepth":1`, exit 0.

### Edit 7: Section 7.2 step 5, WC-13 transcript item

<!-- Source: refactor-plan.md Change 18 (INV-005, INV-006; SPEC:244) -->
Append to 7.2 step 5's Pass list:

> the worker session made no `worker-start`, `dispatch` or `task-create` call and no `orca-cli` `worktree create --agent` or `agent launch` call (WC-13).

This depends on AC-0.6 (tool calls named in the transcript), with the same `--source terminal` fallback 7.2 step 5 already has.

### Edit 8: Section 7.3, new P0 row AC-0.7

<!-- Source: refactor-plan.md Change 15 (INV-004, INV-013, INV-017 routes (a), (b), (c), (f); CAPS:103, CAPS:171, CAPS:180; SPEC:202, SPEC:256, SPEC:278-286, SPEC:387) -->
New row after AC-0.6 (`SPEC:256`). The cell holds no command, because a table cell cannot hold a `grep -E` pipe (`SPEC:202`):

```text
P0 | AC-0.7 | Read-only trace in Orca's installed code, starting from the AC-0.7 block below the table, of (1) which calls check nesting depth: `worker-start`, `dispatch`, `task-create`, low-level dispatch, `worktree create --agent`, `agent launch`; and (2) what depth Orca gives a session the person opens (expected 0, `CAPS:97`). No live probe. | The phase report lists each call as checked, not checked, or not found, and the depth of a person-opened session, each with `path:line`. Any call not checked is recorded as covered only by WC-13 and 7.2 step 5.
```

Add to the "Command blocks used by the table above" fence (`SPEC:278-286`):

```sh
# AC-0.7 starting points: files that raise or name the depth refusal (read-only)
grep -rlE 'nested_worker_depth_exceeded|NESTED_WORKER_DEPTH_EXCEEDED_CODE' /opt/Orca/resources/app.asar.unpacked/out/
```

Run 2026-11-02, it lists `out/shared/nested-worker-depth.js`, `out/cli/bundled-skill-guides.js` and `out/main/chunks/orcad-migration-source-retention-BKoqlqOo.js`. A live probe is not used: if the refusal is not enforced, the probe creates a real nested worker (INV-004), and the inventory ruled out live failure-path probes (`CAPS:171`). The main chunk is minified, so the trace may end "not found" for some calls; that is a valid recorded result.

### Edit 9: Section 7.4, new row WC-13

<!-- Source: refactor-plan.md Change 18 (SPEC:299-300) -->

```text
WC-13 no Orca fan-out from the worker session | 7.2 step 5; AC-0.7
```

### Edit 10: UNVERIFIED item 5 (`SPEC:387`)

<!-- Source: refactor-plan.md "Other spec edits" item 10 and Change 15 (item 10 is the fuller form of Change 15's "Resolve: AC-0.7") -->
Append: "Resolve: AC-0.7; WC-13 and the coordinator's Task-ownership rule forbid or ignore it either way."

## M10. Corrected D5 wording

<!-- Source: refactor-plan.md "Corrected D5 Wording (target text)", copied verbatim; carries Changes 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 17 -->
Replaces `SPEC:350-354` in full. Changes applied: 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 17. Spec IDs WC-13, AC-0.7 and AC-C6 are the new items from Changes 13, 15 and 16.

> **D5. Should Orca's nesting depth be raised so that a worker could start its own Orca workers?**
> - Today the maximum is 1: the coordinator (depth 0) starts workers (depth 1), and Orca is presumed to refuse `worker-start` and `dispatch` from a worker; which calls check the depth, and whether a worker may `task-create`, is not traced (`CAPS:97-99`, `CAPS:103`; AC-0.7 traces it). The value is per Orca profile and applies to every run under that profile; `local-default` is the only profile on this machine (`CAPS:98`). Raising it is one desktop setting (`CAPS:99`); lowering it again while deeper workers are running is UNVERIFIED.
> - Depth cannot reach a command's Agent-tool fan-out, and commands still may not call Orca (SA-2, WC-8), so no setting revives section 1.3. The only use of a raise would be a worker's top-level session starting sub-workers.
> - (a) **Keep depth 1 (recommended).** Fan-out stays inside a command (Agent-tool subagents) or is split into Tasks by the coordinator (sections 1.3 and 2.3). It requires the coordinator to be a root session: one the person opens in the feature's top-level worktree, never one started with `worker-start`, because at depth 1 its own `worker-start` calls would be refused (presumed, `CAPS:103`) and a new Run does not reset depth (`CAPS:97`, `CAPS:101`). Child worktrees (CR-01) are placement chosen by that coordinator, not nested workers. What (a) gives up: Orca Task, liveness and retry records for fan-out that stays inside one command run (WC-10's heartbeat gap stays accepted, under either option), and one extra coordinator round trip when a worker's result shows work that could not be planned before dispatch.
> - (b) **Raise to exactly 2, scoped.** A worker's top-level session may start sub-workers only when its brief says `Sub-workers: allowed, max N`; no command file changes. Orca's fence stays, one generation wider: the refusal fires at the new maximum and bad values fall back to 1 (`CAPS:99-100`). Costs: a composite brief type this spec does not define (the brief carries one command line, section 2.3); the parent becomes a second orchestrator (R5) running the full coordinator loop (`CAPS:92`, `CAPS:107`, `CAPS:113`, `CAPS:116`); sub-worker questions would probably go to the coordinator's Run mailbox, not the parent (`CAPS:59`, `CAPS:92`; UNVERIFIED); WC-13 would have to be relaxed for briefs carrying the `Sub-workers:` line; the brief line restrains only IronClaude workers while the value applies to every run under the profile. It saves one coordinator wake, read and `task-create` per run-time split.
> - Revisit only when both hold: a composite brief type is defined in this spec, and the coordinator's run notes (section 2.3) record a real run whose split was knowable only at run time and whose extra round trip was material. Before any raise: AC-0.7's trace is done, and the mailbox that receives a depth-2 worker's questions and `worker_done` is established.
> - Recommendation: (a). The guard on worker fan-out is WC-13 (the worker session never starts Orca work) with the 7.2 step 5 transcript check, plus Orca's refusal for each call AC-0.7 confirms; depth 1 alone is not proof that a worker cannot start Orca work.

## M11. Accepted risks

<!-- Source: refactor-plan.md "Invariant Coverage (HIGH UNADDRESSED items)", HIGH rows copied verbatim -->
The four HIGH invariants that blocked convergence (INV-001, INV-004, INV-005, INV-017) map to planned changes and to the entries below:

| INV | Severity | Planned by | What stays open | Entry |
|---|---|---|---|---|
| INV-001 root coordinator | HIGH | Changes 1, 15 | How Orca assigns depth to a session a person opens is not traced (depth 0 presumed from `CAPS:97`); AC-0.7 traces it. A coordinator wrongly started at depth 1 fails at its first `worker-start` only if the refusal is enforced; if it is not, its workers start silently at depth 2. | AR-1 |
| INV-004 refusal untraced | HIGH | Changes 4, 15 | Until AC-0.7 runs, the refusal stays presumed. | AR-1 |
| INV-005 no worker-session rule | HIGH | Changes 13, 18 | WC-13 is a written rule a model follows; 7.2 step 5 finds a breach only after it happened. | AR-1 |
| INV-017 backstop not demonstrated | HIGH | Changes 13, 14, 15, 16, 17 | Routes (a), (b), (f) depend on AC-0.7; route (g) on AC-C6 and the person; (c) closed by Change 14; (h) closed by Change 13. | AR-1, AR-2, AR-3 |

<!-- Source: refactor-plan.md "Accepted-risk and open entries" AR-1, AR-2, AR-3, copied verbatim -->
- **AR-1 (open until P0 AC-0.7).** Until the trace runs, Orca's refusal of `worker-start`, `dispatch` and `task-create` from a depth-1 worker is presumed, and so is depth 0 for a session the person opens (INV-001). The demonstrated guards are WC-13 (a contract rule) and the 7.2 step 5 transcript check (after the fact), plus the stated precondition that the coordinator is a session the person opened (Change 1). If AC-0.7 finds a call that is not checked, that call stays covered only by those guards, and the phase report says so. Owner: P0.
- **AR-2 (open until P0 AC-0.7).** Orca's low-level dispatch and `orca-cli` `worktree create --agent` / `agent launch` may not be depth-fenced: the guide only warns against routing around the limit (`CAPS:101`, `CAPS:139`). WC-13 names them; AC-C1 cannot see sessions or executable names held in variables. Owner: P0.
- **AR-3 (accepted risk).** The depth value is a per-profile setting the person can change at any time, for this or another project (`CAPS:98-99`). AC-C6 catches a change only at a phase check, and whether the running app re-reads the file is UNVERIFIED. Accepted because changing it is the person's decision (non-goal 2, `SPEC:315`), and Changes 13 and 18 do not depend on the value.
