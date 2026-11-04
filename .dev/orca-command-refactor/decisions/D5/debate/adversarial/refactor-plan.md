# Refactoring Plan: Merge into Base (Variant 1)

## Overview
- Base: Variant 1, `variant-1-original.md` (option a, keep depth 1); combined score 0.827 against 0.694 (`base-selection.md`)
- Incorporating strengths from: Variant 2 (`variant-2-original.md`, option b), the Round 1-2 concessions and refinements of both advocates (`debate-transcript.md`), and the Round 2.5 invariant probe (`invariant-probe.md`)
- Merged output: one D5 position for option (a) with corrected reasons, the stated precondition, the scoped form (b) would take, a revisit trigger that can fire, and the spec changes and P0 checks the decision needs. The corrected D5 text for the spec is given in full under "Corrected D5 Wording".
- Planned changes: 19 (Changes 1-19). Six correct OVERSTATED citations or claims in the base (Changes 2, 3, 4, 5, 7, 10). Eight address the HIGH UNADDRESSED invariants (Changes 1, 4, 13, 14, 15, 16, 17, 18; Change 4 is in both groups), and three accepted-risk / open entries cover what those changes cannot close (see "Invariant Coverage")
- Convergence status carried in: 95.2%, BLOCKED_BY_INVARIANTS (INV-001, INV-004, INV-005, INV-017)
- Risk level: Medium overall. Most changes are wording in the D5 position (Low). The spec-side changes (a new worker-session rule, a coordinator Task-ownership rule, a P0 check) add requirements and acceptance checks to `orca-worker-contract-spec.md` and therefore touch sections other than D5 (Medium).
- Citation key: `V1:N` / `V2:N` = variant line; `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `R1-V1` ... `R2-V2` = round files; `DA` = `diff-analysis.md`; `INV-NNN` = `invariant-probe.md`. All `SPEC` and `CAPS` lines cited below were re-read by the orchestrator on 2026-11-02 (`SPEC:20-89, 165-259, 295-394`; `CAPS:56-169, 170-181`).

### Citation audit of the base
Every citation in Variant 1 was checked against the source. None is WRONG (the cited lines say what V1 quotes); six uses are OVERSTATED, each corrected by the change named.

| Base line | Citation | Problem | Verdict | Fixed by |
|---|---|---|---|---|
| V1:12 | `CAPS:155` | Drops the source's "UNVERIFIED that Orca never limits them" (DA spot-check 4; conceded R1-V1 concession 2). | OVERSTATED | Change 5 |
| V1:8 | `CAPS:97`, `CAPS:100-101` | Calls depth 1 "its fence against runaway fan-out", implying a raise removes the fence; `CAPS:99-100` show the refusal fires at any maximum (DA A-001 CONTRADICTED; R1-V1 concession 1). Depth also bounds generations, not width (INV-007). | OVERSTATED | Change 3 |
| V1:8 | `CAPS:97`, `CAPS:99` | Presents the refusal as enforced; `CAPS:103` says the call sites are presumed and `task-create` at depth 1 is unknown (INV-004). | OVERSTATED | Change 4 |
| V1:9 | `CAPS:98`, `orca-data.json:1` | "machine-wide, not per run": the setting is per profile and is machine-wide only because `local-default` is the only profile; no per-run override is inferred, not proven (DA A-004; INV-009). | OVERSTATED (minor) | Change 7 |
| V1:19 | `SPEC:181` | The P0 smoke runs are three single-command workers, so they cannot show "coordinator-side splitting is inadequate" (R1-V2 W3; conceded R2-V1 item 3). The citation is accurate; the inference is not. | OVERSTATED use | Change 10 |
| V1:19 | `CAPS:99` | "Raising depth later is one desktop setting" is presented as a cheap revisit; lowering it again with live nested workers is UNVERIFIED (DA C-008; R1-V1 concession 5). | OVERSTATED (one-directional) | Change 2 |

Confirmed and kept as is: `SPEC:352`, `SPEC:42`, `SPEC:72`, `SPEC:170`, `SPEC:37-40`, `SPEC:87`, `CAPS:97` quote, `CAPS:99` advice quote, `CAPS:100` fallback quote, `CAPS:101`, `orca-data.json:1` value (DA spot-check rows 1-3; orchestrator re-read).

## Planned Changes

Target structure of the merged D5 position (`merged-output.md`), so each change names where it lands: (M1) Position; (M2) Precondition; (M3) Safety; (M4) Reliability, with a subsection "What option (a) gives up"; (M5) How a person works day to day; (M6) Implementation cost; (M7) If (b) is ever chosen; (M8) Revisit trigger; (M9) Spec changes this decision needs; (M10) Corrected D5 wording; (M11) Accepted risks. M1, M3, M4, M5 and M6 are the base's sections (V1:3, V1:7, V1:11, V1:15, V1:18); the rest are new.

Fixed constraints applied by the orchestrator (team lead, 2026-11-02), not debate evidence: worktrees are created by Orca at its default paths, never under `.dev/worktrees/` (`changes/CR-01-feature-worktree-hierarchy.md:41`); SuperClaude upstream is never touched (CR-01:45); merged PR #343 (commit `80f934de`: only blocking findings fail a review, at most 2 fix cycles); CR-01 (child worktrees are placement chosen by the coordinator, CR-01:16, 22). Where one of these shapes a change's text, the change says so.

### Change 1: State the root-coordinator precondition (from the invariant probe)
- **Source**: `invariant-probe.md` INV-001 (HIGH, UNADDRESSED); `CAPS:97` ("Root coordinators are depth 0; the first generation of workers is depth 1"), `CAPS:101` (a new Run does not reset depth), `CAPS:151` (sessions in this project do run as dispatched workers). Fixed constraint CR-01:15 (the coordinator runs in the feature's top-level worktree) and CR-01:16, 22 (children are placement).
- **Target**: merged M2 (new) and M5; spec D5 option (a) (`SPEC:352`) and non-goal 2 (`SPEC:315`) via M10 (insert).
- **Rationale**: Option (a) works only if the coordinator is depth 0. A coordinator that was itself started by `worker-start` is depth 1, so under a maximum of 1 its own `worker-start` calls are refused (presumed, `CAPS:103`) and opening a new Run does not help (`CAPS:101`). Neither advocate, section 2.3 (`SPEC:79-87`) nor the 7.2 check (`SPEC:236`) states this.
- **Integration point**: M2 states: the coordinator must be a session the person opened (depth 0), in the feature's top-level worktree; it must never be started with `worker-start`. CR-01 child worktrees are created by that coordinator with `worker-start --worktree new-child`, so every worker in a child is still depth 1; "child worktree" is placement, not nesting. How Orca assigns depth to a session a person opens is not traced; depth 0 is presumed from `CAPS:97` (UNVERIFIED).
- **Risk**: Low. Adds a stated precondition; no behaviour changes.

### Change 2: Make the "cheap to revisit" claim one-directional (base weakness)
- **Source**: DA C-008, A-006; R1-V1 concession 5; R2-V1 item 10; R2-V2 item 13 (C-008: V1, 90%).
- **Target**: merged M6, base V1:19 (replace the sentence "Raising depth later is one desktop setting").
- **Rationale**: Raising is one setting (`CAPS:99`), but lowering it again while depth-2 workers are live is UNVERIFIED in the sources. Both advocates agreed this argues for raising only on evidence.
- **Integration point**: "Raising the value is one desktop setting (`CAPS:99`). Lowering it again while deeper workers are running is UNVERIFIED, so a raise is made only on the evidence in M8."
- **Risk**: Low.

### Change 3: "Widens, does not remove"; depth bounds generations, not width (base weakness)
- **Source**: DA A-001 (CONTRADICTED), C-001; R1-V1 concession 1; R1-V2 A-001; INV-007 (MEDIUM); `CAPS:99-100`; `SPEC:87`.
- **Target**: merged M3, base V1:8 (replace "its fence against runaway fan-out").
- **Rationale**: The refusal fires at any configured maximum ("not permitted at depth ${childDepth} (max ${maxDepth})", `CAPS:99`) and a malformed value falls back to 1 (`CAPS:100`), so a raise to 2 admits one more generation and keeps a fence. Depth limits generations only: at depth 1 Orca puts no cap on how many workers the coordinator starts; the only numeric cap in the spec is the contract's fan-in limit of 10 merge inputs (`SPEC:87`).
- **Integration point**: Replace the V1:8 framing with: "Depth 1 is Orca's default and the tightest setting: it allows one generation of workers. A raise to 2 allows one more generation; the refusal still fires at the new maximum and bad values fall back to 1 (`CAPS:99-100`). Depth does not limit how many workers one generation has."
- **Risk**: Low.

### Change 4: Say the refusal is presumed, not traced (base weakness; also HIGH INV-004)
- **Source**: V2:16 ("Which call sites enforce the depth check is UNVERIFIED"); DA U-007; `CAPS:103`; `SPEC:387` (UNVERIFIED item 5); INV-004 (HIGH).
- **Target**: merged M3 (modify V1:8) and M10.
- **Rationale**: V1:8 presents the refusal as enforced. `CAPS:103` says the enforcing call sites were not traced (`worker-start` and `dispatch` presumed) and whether a depth-1 worker may call `task-create` is unknown. Orchestrator check, 2026-11-02: a read-only `grep -rlE 'nested_worker_depth_exceeded|NESTED_WORKER_DEPTH_EXCEEDED_CODE' /opt/Orca/resources/app.asar.unpacked/out/` lists three files (`out/shared/nested-worker-depth.js`, `out/cli/bundled-skill-guides.js`, the minified `out/main/chunks/orcad-migration-source-retention-BKoqlqOo.js`); which verbs reach the check was not traced (UNVERIFIED).
- **Integration point**: Append to M3: "Which Orca calls check the depth was not traced: `worker-start` and `dispatch` are presumed, `task-create` from a depth-1 worker is unknown (`CAPS:103`). AC-0.7 (Change 15) traces them."
- **Risk**: Low.

### Change 5: Restore the dropped UNVERIFIED caveat on Agent-tool subagents (base weakness)
- **Source**: DA spot-check 4 (OVERSTATED); R1-V1 concession 2; R2-V1 item 4; C-011 (equal, 90%); `CAPS:155`.
- **Target**: merged M4, base V1:12 (modify).
- **Rationale**: `CAPS:155` says subagents are not counted by the depth fence and adds "UNVERIFIED that Orca never limits them". V1:12 kept only the first half.
- **Integration point**: "Agent-tool subagents are not Orca workers, so the depth fence does not count them; that Orca never limits them is UNVERIFIED (`CAPS:155`). Orca shows them only as sidebar child rows, not Tasks (`CAPS:157`)."
- **Risk**: Low.

### Change 6: State what option (a) gives up (from Variant 2)
- **Source**: Variant 2, "Strongest case for it" (V2:7-8); DA U-005; S-001 (V2, 95%); X-002 (V2, 94%); R1-V1 concession 3; R2-V1 item 11. Liveness correction: C-004 (V2, 94%), R2-V1 item 6, INV-016 (ADDRESSED); `CAPS:64`, `SPEC:74`.
- **Target**: merged M4, new subsection "What option (a) gives up" (insert after V1:13).
- **Rationale**: The three points Variant 2 won (S-001, X-002, C-004) all concern what the base left out or got wrong about (a)'s costs and liveness. Two costs are real: (i) fan-out that stays inside one command run (for example troubleshoot Tier 2) has no Orca Task, Dispatch, liveness or independent retry, and WC-10's heartbeat gap stays accepted (`SPEC:74`); (ii) a split a worker discovers at run time is planned by the coordinator after it reads the result, which costs one extra coordinator round trip. D5 does not change (i) under either option, because depth cannot reach a command's Agent-tool fan-out (C-005, X-003), and a worker blocked in `check --wait` is live (`CAPS:64`), so the heartbeat gap does not move to a parent.
- **Integration point**: Insert as a subsection of M4 with the two costs, then the sentence that neither option closes (i).
- **Risk**: Low.

### Change 7: Per-profile precision for "machine-wide" (base weakness)
- **Source**: DA A-004 (STATED; "absence of an override is inferred, not proven"); INV-009 (LOW); `CAPS:98`.
- **Target**: merged M3, base V1:9 (modify).
- **Rationale**: The value lives in one Orca profile file (`orca-data.json:1`, `"nestedWorkerMaxDepth":1`; re-read by the orchestrator 2026-11-02, output `"nestedWorkerMaxDepth":1`, and `local-default` is the only directory under `~/.config/orca/profiles/`). It is machine-wide only because that is the only profile. No per-run override is known; that none exists is inferred, not proven.
- **Integration point**: "The setting is per Orca profile and applies to every run under that profile; `local-default` is the only profile on this machine, so today a raise affects every Orca run here. No per-run override was found (inferred, not proven)."
- **Risk**: Low.

### Change 8: Record the scoped form (b) would take (from both advocates' Round 2)
- **Source**: R1-V2 Position summary; R2-V1 Overall recommendation; R2-V2 Overall recommendation item 2; A-002 (equal, 88%); INV-008 (ADDRESSED: a maximum of 2 admits depth-2 children and refuses depth 3, `CAPS:97`, `CAPS:99`).
- **Target**: merged M7 (new); M10 option (b).
- **Rationale**: Both advocates agree that if (b) is ever chosen it is not section 1.3's design (commands calling Orca) but: depth exactly 2; only a worker's top-level session starts sub-workers; only when its brief carries `Sub-workers: allowed, max N`; no command file changes, so SA-2 and WC-8 hold. This route avoids R2-R4 (`CAPS:148`, `CAPS:150`, `CAPS:145`; R2-V1 item 8).
- **Integration point**: First paragraph of M7.
- **Risk**: Low.

### Change 9: Locate (b)'s real cost and residual faults (from Variant 2 and the rebuttals)
- **Source**: V2:19, V2:22; DA U-006, U-008; C-007 (V1, 95%); C-009 (V1, 97%); R2-V1 New evidence 1-4; R2-V2 New evidence 1; `SPEC:40` (R5), `SPEC:79`; `CAPS:59`, `CAPS:92`, `CAPS:107`, `CAPS:113`, `CAPS:116`.
- **Target**: merged M7 (second paragraph); M10 option (b).
- **Rationale**: The setting is trivial; using it is not. The brief carries "the exact command line" (`SPEC:79`), so a worker that plans its own fan-out is a new composite brief type with contract text and tests. The parent inherits the coordinator loop: start each sub-worker (`CAPS:92`), one release-or-retain decision per settled sub-worker (`CAPS:107`), no turn end while any is `reclaimable` (`CAPS:113`), the three-failure circuit breaker (`CAPS:116`). It becomes a second orchestrator (R5, `SPEC:40`). Sub-worker questions would probably go to the coordinator's inbox: a question from an active Dispatch defaults to its owning Run mailbox (`CAPS:59`) and a Run is the coordinator's inbox (`CAPS:92`); delivery to the parent is UNVERIFIED (R2-V2 NE1; C-004 evidence). The brief line restrains only IronClaude workers while the raised value applies to every run under the profile (R2-V1 NE4). WC-13 (Change 13) would have to be relaxed for briefs carrying the `Sub-workers:` line. The saving is one coordinator wake, read and `task-create` (R2-V1 NE3; R2-V2 item 7).
- **Integration point**: Second paragraph of M7, as a list of costs.
- **Risk**: Low.

### Change 10: Replace the revisit trigger with one that can fire (base weakness)
- **Source**: R1-V2 W3 (the P0 smoke runs are single-command workers, `SPEC:181`); R2-V1 item 3 (trigger revised); R2-V2 New evidence 2 and Overall item 3 (second condition); INV-010 (LOW), INV-011 (MEDIUM); `SPEC:83`.
- **Target**: merged M6 (remove the V1:19 trigger) and M8 (new); spec section 2.3 run notes (insert, via M9).
- **Rationale**: V1:19's trigger cannot fire: P0 smoke runs have no run-time split. The revised trigger needs both conditions together (a defined composite brief type, and a real coordinator run whose split was knowable only at run time and whose extra round trip was material), because with the one-command brief no worker session has fan-out to start (INV-011). Nothing records such a split today: the run notes record only partial-usability judgements (`SPEC:83`), so the evidence set would stay empty (INV-010).
- **Integration point**: M8 states the two-condition trigger. M9 adds to section 2.3: "In its run notes the coordinator also records each follow-up Task it created because a worker's result showed work that could not be planned before dispatch, with the extra time that cost. This is the evidence D5's revisit trigger reads."
- **Risk**: Medium. Adds one coordinator duty to section 2.3.

### Change 11: Checks before any raise (from Variant 2's Round 2)
- **Source**: R2-V2 Overall recommendation item 4; R2-V2 New evidence 1; R2-V1 critique (iv); `CAPS:59`, `CAPS:103`; `SPEC:387`.
- **Target**: merged M7 (third paragraph) and M10.
- **Rationale**: Before any raise: the refusal call sites and `task-create` at depth 1 are traced (AC-0.7 does this anyway under (a)); and which mailbox receives a depth-2 worker's questions and `worker_done` is established, because the parent's fan-in depends on it and the sources suggest it is the coordinator's Run mailbox.
- **Integration point**: Third paragraph of M7; one sentence in M10.
- **Risk**: Low.

### Change 12: Correct the spec text around D5 (from Variant 2's Round 2 and the probe)
- **Source**: R2-V2 New evidence 3; INV-012 (MEDIUM); `SPEC:27` (E4), `SPEC:36` (R1), `SPEC:315` (non-goal 2), `SPEC:350`, `SPEC:353`; DA spot-check 4.
- **Target**: spec E4, R1, non-goal 2 and D5 (replace), all via M9 and M10.
- **Rationale**: `SPEC:350` asks whether to raise depth "so commands could start their own Orca workers", the route both advocates reject; `SPEC:353` says (b) would "break R1's protection against runaway fan-out", against `CAPS:99-100`; `SPEC:36` says the designs "exclude each other unless the user raises the depth setting", which implies a raise makes section 1.3 viable, against agreed point 1 (`invariant-probe.md` consensus 1); E4 (`SPEC:27`) drops the `CAPS:155` caveat.
- **Integration point**: M9 lists the exact replacements for E4, R1's last sentence and non-goal 2; M10 is the full D5 replacement.
- **Risk**: Medium. Touches four places outside D5; each edit narrows a claim and changes no rule.

### Change 13: A worker-session rule against Orca fan-out (new WC-13, from the invariant probe)
- **Source**: INV-005 (HIGH), INV-013 (MEDIUM), INV-017 route (h) (HIGH); `SPEC:72` (WC-8, owner "Command"), `SPEC:170` (SA-2 binds command, skill and agent files), `SPEC:67-76` (no worker-session ban); `CAPS:101` (`[G:topology]` "never use it [low-level dispatch] to route around the nested-depth limit"), `CAPS:139` (`worktree create --agent`, `agent launch`).
- **Target**: spec section 2.2, new row WC-13 after WC-12 (`SPEC:76`); section 2.1 contract-file list (`SPEC:58`), worker-session duties (insert), via M9.
- **Rationale**: The debate established that a worker's top-level session is bound by neither WC-8 nor SA-2 (A-002). Under (a) the unverified Orca refusal is therefore the only guard on that session. A written rule makes the contract, not a presumed refusal, the primary guard, and it covers the routes the depth fence may not cover.
- **Integration point**: New row: "WC-13 | **No Orca fan-out from the worker session.** The worker's top-level session never calls `worker-start`, `dispatch` or `task-create`, Orca's low-level dispatch, or `orca-cli` `worktree create --agent` or `agent launch`, at any depth setting. Work it finds that needs another worker is stated in its `worker_done` body; the coordinator decides (section 2.3). | Worker session | `CAPS:97-103`, `CAPS:139`; INV-005". Add WC-13 to the worker-session duties named at `SPEC:58`. Because AC-0.1's test asserts that the contract file states each rule section 2.1 assigns to it (`SPEC:251`), that test then asserts WC-13 too; no separate AC-0.1 edit is needed beyond the list.
- **Risk**: Medium. New requirement; it restates what depth 1 is presumed to enforce, so no current behaviour changes.

### Change 14: The coordinator starts only Tasks it created (from the invariant probe)
- **Source**: INV-014 (MEDIUM), INV-017 route (c) (HIGH); `CAPS:86` (ready view as "external memory"), `CAPS:92` (coordinator starts each ready Task); `CAPS:103`, `SPEC:387` (`task-create` at depth 1 UNVERIFIED); `SPEC:81-85` (no ownership check).
- **Target**: spec section 2.3 "Reading a result before anything depends on it" (insert a bullet), via M9.
- **Rationale**: If a depth-1 worker can `task-create`, its Task enters the ready view; the coordinator's ready scan would start it at depth 1, with no refusal anywhere. A rule on the coordinator closes that route without knowing the `task-create` answer.
- **Integration point**: New bullet: "The coordinator starts only Tasks it created itself. A ready Task it did not create is not started; it is reported to the person with its spec text."
- **Risk**: Medium. New coordinator rule; WC-13 makes such Tasks a contract breach, so the rule should never fire in normal runs.

### Change 15: A read-only P0 trace of the depth check (new AC-0.7, from the invariant probe)
- **Source**: INV-004 (HIGH), INV-013 (MEDIUM), INV-017 routes (a), (b), (c), (f) (HIGH); `CAPS:103`, `CAPS:180` (inventory UNVERIFIED item 5), `CAPS:171` (live failure-path probes ruled out); `SPEC:387`.
- **Target**: spec section 7.3, new P0 row AC-0.7 after AC-0.6 (`SPEC:256`); UNVERIFIED item 5 (`SPEC:387`) gains "Resolve: AC-0.7", via M9.
- **Rationale**: A live probe is unsafe: if the refusal is not enforced, the probe creates a real nested worker (INV-004). Reading Orca's installed code is read-only and gives `path:line` evidence. The trace's starting points are the three files the orchestrator's grep found (Change 4). The trace also covers how Orca assigns a depth to a session the person opens, which is the open half of INV-001 (Change 1).
- **Integration point**: New table row (no command in the cell, because a table cell cannot hold a `grep -E` pipe, `SPEC:202`): "P0 | AC-0.7 | Read-only trace in Orca's installed code, starting from the AC-0.7 block below the table, of (1) which calls check nesting depth: `worker-start`, `dispatch`, `task-create`, low-level dispatch, `worktree create --agent`, `agent launch`; and (2) what depth Orca gives a session the person opens (expected 0, `CAPS:97`). No live probe. | The phase report lists each call as checked, not checked, or not found, and the depth of a person-opened session, each with `path:line`. Any call not checked is recorded as covered only by WC-13 and 7.2 step 5." Add to the "Command blocks used by the table above" fence (`SPEC:278-286`):
  ```sh
  # AC-0.7 starting points: files that raise or name the depth refusal (read-only)
  grep -rlE 'nested_worker_depth_exceeded|NESTED_WORKER_DEPTH_EXCEEDED_CODE' /opt/Orca/resources/app.asar.unpacked/out/
  ```
  Run 2026-11-02, it lists `out/shared/nested-worker-depth.js`, `out/cli/bundled-skill-guides.js` and `out/main/chunks/orcad-migration-source-retention-BKoqlqOo.js`.
- **Risk**: Medium. New P0 check; read-only, but the main chunk is minified, so the trace may end "not found" for some calls (that is a valid recorded result).

### Change 16: Re-read the live depth value at every phase (new AC-C6, from the invariant probe)
- **Source**: INV-002 (MEDIUM), INV-017 route (g) (HIGH); `CAPS:98-99`; `SPEC:315` (non-goal 2 has no check in `SPEC:251-256`).
- **Target**: spec section 7.1, new common check AC-C6 after AC-C5 (`SPEC:229-232`), via M9.
- **Rationale**: The value is editable by the person, or for another project, at any time, and nothing in the spec re-reads it. A common check runs at P0 and again at every later phase, which a one-time P0 read would not.
- **Integration point**: New common check in section 7.1, in the fenced style of AC-C1 to AC-C5:
  "**AC-C6** (D5, non-goal 2). Pass: prints exactly one line per Orca profile and every line is `"nestedWorkerMaxDepth":1`. A profile whose file has no such key prints nothing for it; the phase report then records that profile as using Orca's default (1, `CAPS:97`), which is presumed, not read. Any other value fails the phase until the person confirms D5 was changed. Whether the running app re-reads the file is UNVERIFIED.
  ```sh
  grep -ho '"nestedWorkerMaxDepth":[0-9]*' "${ORCA_RUNTIME_SOURCE_PROFILE_PATH:-$HOME/.config/orca}"/profiles/*/orca-data.json
  ```"
  (`ORCA_RUNTIME_SOURCE_PROFILE_PATH` is `/home/coder/.config/orca` here, `CAPS:98`; `-h` drops file-name prefixes when there are several profiles.)
- **Risk**: Medium. A new common check. The exact command above was run on 2026-11-02 and printed `"nestedWorkerMaxDepth":1`, exit 0.

### Change 17: Drop the unproven "mechanical backstop" reason (from the invariant probe)
- **Source**: INV-017 (HIGH); A-003 (V1, 90%, held at the floor because the call sites are UNVERIFIED); R2-V1 A-003; R2-V2 A-003.
- **Target**: merged M3 and the recommendation line of M10 (replace).
- **Rationale**: The debate decided A-003 on "at depth 1 a mechanical refusal backs the contract on every run". INV-017 lists eight routes; six are open or unverified. The honest reason for (a) is cost, R5 and scope, not a proven fence.
- **Integration point**: M3 and M10 state the guard as: WC-13 (Change 13) and the 7.2 transcript check (Change 18), plus Orca's refusal for each call AC-0.7 confirms. The A-003 asymmetry is kept only as "presumed": at depth 1 Orca is presumed to refuse direct dispatch from any worker of any run; under (b) only IronClaude briefs would carry a restraint.
- **Risk**: Low. Wording; removes a claim.

### Change 18: Check WC-13 in every live worker check (from the invariant probe)
- **Source**: INV-005 (HIGH), INV-006 (MEDIUM: AC-C1 "cannot see worker-session behaviour at all"); `SPEC:244` (7.2 step 5), `SPEC:299-300` (traceability).
- **Target**: spec 7.2 step 5 (append) and 7.4 (insert a row), via M9.
- **Rationale**: AC-C1 scans files; WC-13 binds a session, so only the transcript can show a breach.
- **Integration point**: Append to 7.2 step 5's Pass list: "the worker session made no `worker-start`, `dispatch` or `task-create` call and no `orca-cli` `worktree create --agent` or `agent launch` call (WC-13)." New 7.4 row: "WC-13 no Orca fan-out from the worker session | 7.2 step 5; AC-0.7".
- **Risk**: Medium. Extends every live check by one transcript search; depends on AC-0.6 (tool calls named in the transcript), with the same `--source terminal` fallback 7.2 step 5 already has.

### Change 19: Widen AC-C1's scan (from the invariant probe)
- **Source**: INV-006 (MEDIUM); `SPEC:202` (`ORCA` placeholder), `SPEC:205-211` (AC-C1 scans commands, skills, agents and core only, case-sensitive).
- **Target**: spec 7.1 AC-C1 (replace the command block), via M9.
- **Rationale**: AC-C1 is the only check for WC-8 and SA-2. It is case-sensitive, so it misses `ORCA orchestration`, and it skips `src/superclaude/hooks`, `src/superclaude/templates` and the `plugins/superclaude` mirror, all of which exist (orchestrator `ls`, 2026-11-02). The widened grep, run by the orchestrator on 2026-11-02 over all seven directories, printed nothing, so the change does not fail today's tree.
- **Integration point**: Replace the AC-C1 description at `SPEC:205` so it names the seven scanned directories and says the match ignores case, and replace the block at `SPEC:206-211` with:
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
  The two added exclusions cover the mirrored routing guide, which gains the Orca section in P0 (`SPEC:181`, `SPEC:252`), and a future plugin copy of the contract file (`plugins/superclaude/core/` holds copies of some core files; whether `WORKER-CONTRACT.md` will be copied there is UNVERIFIED). Executable names held in variables stay out of reach of any grep; that residual is recorded under AR-2.
- **Risk**: Medium. A wider scan can catch prose that names Orca verbs; the contract file and both routing-guide copies are excluded by name.

## Invariant Coverage (HIGH UNADDRESSED items)

Every HIGH UNADDRESSED item from the convergence gate has a planned change, and what the changes cannot close is an explicit accepted-risk or open entry. MEDIUM and LOW items are mapped too.

| INV | Severity | Planned by | What stays open | Entry |
|---|---|---|---|---|
| INV-001 root coordinator | HIGH | Changes 1, 15 | How Orca assigns depth to a session a person opens is not traced (depth 0 presumed from `CAPS:97`); AC-0.7 traces it. A coordinator wrongly started at depth 1 fails at its first `worker-start` only if the refusal is enforced; if it is not, its workers start silently at depth 2. | AR-1 |
| INV-004 refusal untraced | HIGH | Changes 4, 15 | Until AC-0.7 runs, the refusal stays presumed. | AR-1 |
| INV-005 no worker-session rule | HIGH | Changes 13, 18 | WC-13 is a written rule a model follows; 7.2 step 5 finds a breach only after it happened. | AR-1 |
| INV-017 backstop not demonstrated | HIGH | Changes 13, 14, 15, 16, 17 | Routes (a), (b), (f) depend on AC-0.7; route (g) on AC-C6 and the person; (c) closed by Change 14; (h) closed by Change 13. | AR-1, AR-2, AR-3 |
| INV-002 depth value can change | MEDIUM | Change 16 | AC-C6 reads the file at phase checks only; runtime caching UNVERIFIED. | AR-3 |
| INV-006 AC-C1 gaps | MEDIUM | Changes 18, 19 | Variable-held executable names. | AR-2 |
| INV-007 width not bounded | MEDIUM | Change 3 | Orca puts no cap on how many workers one generation has; width is whatever the coordinator plans. The fan-in cap of 10 (`SPEC:87`) limits only the inputs to one merge Task. Change 3 states this; no further control is proposed, because D5 does not change width under either option. | closed in text |
| INV-011 triggers disagree | MEDIUM | Change 10 | None. | closed in text |
| INV-012 spec text around D5 | MEDIUM | Change 12 | None. | closed in text |
| INV-013 routes outside orchestration | MEDIUM | Changes 13, 15 | Whether the fence covers them depends on AC-0.7. | AR-2 |
| INV-014 worker-created Tasks | MEDIUM | Change 14 | None. | closed in text |
| INV-009 multi-profile | LOW | Change 7, Change 16 (glob over all profiles) | None. | closed in text |
| INV-010 trigger has no evidence | LOW | Change 10 (run-notes line) | None. | closed in text |

**Accepted-risk and open entries** (the three entries the Overview counts):
- **AR-1 (open until P0 AC-0.7).** Until the trace runs, Orca's refusal of `worker-start`, `dispatch` and `task-create` from a depth-1 worker is presumed, and so is depth 0 for a session the person opens (INV-001). The demonstrated guards are WC-13 (a contract rule) and the 7.2 step 5 transcript check (after the fact), plus the stated precondition that the coordinator is a session the person opened (Change 1). If AC-0.7 finds a call that is not checked, that call stays covered only by those guards, and the phase report says so. Owner: P0.
- **AR-2 (open until P0 AC-0.7).** Orca's low-level dispatch and `orca-cli` `worktree create --agent` / `agent launch` may not be depth-fenced: the guide only warns against routing around the limit (`CAPS:101`, `CAPS:139`). WC-13 names them; AC-C1 cannot see sessions or executable names held in variables. Owner: P0.
- **AR-3 (accepted risk).** The depth value is a per-profile setting the person can change at any time, for this or another project (`CAPS:98-99`). AC-C6 catches a change only at a phase check, and whether the running app re-reads the file is UNVERIFIED. Accepted because changing it is the person's decision (non-goal 2, `SPEC:315`), and Changes 13 and 18 do not depend on the value.

## Corrected D5 Wording (target text)

Replaces `SPEC:350-354` in full. Changes applied: 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 17. Spec IDs WC-13, AC-0.7 and AC-C6 are the new items from Changes 13, 15 and 16.

> **D5. Should Orca's nesting depth be raised so that a worker could start its own Orca workers?**
> - Today the maximum is 1: the coordinator (depth 0) starts workers (depth 1), and Orca is presumed to refuse `worker-start` and `dispatch` from a worker; which calls check the depth, and whether a worker may `task-create`, is not traced (`CAPS:97-99`, `CAPS:103`; AC-0.7 traces it). The value is per Orca profile and applies to every run under that profile; `local-default` is the only profile on this machine (`CAPS:98`). Raising it is one desktop setting (`CAPS:99`); lowering it again while deeper workers are running is UNVERIFIED.
> - Depth cannot reach a command's Agent-tool fan-out, and commands still may not call Orca (SA-2, WC-8), so no setting revives section 1.3. The only use of a raise would be a worker's top-level session starting sub-workers.
> - (a) **Keep depth 1 (recommended).** Fan-out stays inside a command (Agent-tool subagents) or is split into Tasks by the coordinator (sections 1.3 and 2.3). It requires the coordinator to be a root session: one the person opens in the feature's top-level worktree, never one started with `worker-start`, because at depth 1 its own `worker-start` calls would be refused (presumed, `CAPS:103`) and a new Run does not reset depth (`CAPS:97`, `CAPS:101`). Child worktrees (CR-01) are placement chosen by that coordinator, not nested workers. What (a) gives up: Orca Task, liveness and retry records for fan-out that stays inside one command run (WC-10's heartbeat gap stays accepted, under either option), and one extra coordinator round trip when a worker's result shows work that could not be planned before dispatch.
> - (b) **Raise to exactly 2, scoped.** A worker's top-level session may start sub-workers only when its brief says `Sub-workers: allowed, max N`; no command file changes. Orca's fence stays, one generation wider: the refusal fires at the new maximum and bad values fall back to 1 (`CAPS:99-100`). Costs: a composite brief type this spec does not define (the brief carries one command line, section 2.3); the parent becomes a second orchestrator (R5) running the full coordinator loop (`CAPS:92`, `CAPS:107`, `CAPS:113`, `CAPS:116`); sub-worker questions would probably go to the coordinator's Run mailbox, not the parent (`CAPS:59`, `CAPS:92`; UNVERIFIED); WC-13 would have to be relaxed for briefs carrying the `Sub-workers:` line; the brief line restrains only IronClaude workers while the value applies to every run under the profile. It saves one coordinator wake, read and `task-create` per run-time split.
> - Revisit only when both hold: a composite brief type is defined in this spec, and the coordinator's run notes (section 2.3) record a real run whose split was knowable only at run time and whose extra round trip was material. Before any raise: AC-0.7's trace is done, and the mailbox that receives a depth-2 worker's questions and `worker_done` is established.
> - Recommendation: (a). The guard on worker fan-out is WC-13 (the worker session never starts Orca work) with the 7.2 step 5 transcript check, plus Orca's refusal for each call AC-0.7 confirms; depth 1 alone is not proof that a worker cannot start Orca work.

Other spec edits this decision needs (Changes 10, 12, 13, 14, 15, 16, 18, 19), each given in full in its Planned Change entry:
1. E4 (`SPEC:27`): replace "are not counted by Orca's nesting limit." with "are not counted by Orca's nesting limit; that Orca never limits them is UNVERIFIED."
2. R1 (`SPEC:36`): replace "The two designs exclude each other unless the user raises the depth setting." with "Raising the depth would not make this design viable: R2-R5 still apply, and depth cannot reach a command's Agent-tool fan-out (D5)."
3. Non-goal 2 (`SPEC:315`): replace "Nesting depth stays 1 unless the user decides otherwise (D5)" with "Nesting depth stays 1 unless the user decides otherwise, and the coordinator is a session the person opened, never one started by `worker-start` (D5)".
4. Section 2.2: new row WC-13 (Change 13); section 2.1 contract-file list gains WC-13 among the worker-session duties (`SPEC:58`).
5. Section 2.3: run-notes line (Change 10) and the coordinator Task-ownership bullet (Change 14).
6. Section 7.1: AC-C1 widened (Change 19); new AC-C6 (Change 16).
7. Section 7.2 step 5: WC-13 transcript item (Change 18).
8. Section 7.3: new P0 row AC-0.7 (Change 15).
9. Section 7.4: new row WC-13 (Change 18).
10. UNVERIFIED item 5 (`SPEC:387`): append "Resolve: AC-0.7; WC-13 and the coordinator's Task-ownership rule forbid or ignore it either way."

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|---|---|---|
| S-002, C-005 | Frame the decision on section 1.3's design, commands starting Orca workers (V2:3) | Depth fixes only R1; R2-R5 remain (`SPEC:37-40`). Both advocates reject that route (`invariant-probe.md` consensus 1). V1 won S-002 (95%) and C-005 (96%). |
| X-003, C-003 | "Depth 2 would give each sub-unit its own Task and Dispatch" (V2:8) | Depth cannot reach a command's Agent-tool fan-out (R1-V2 concession 2; R2-V2 item 1). V1 won X-003 (97%). C-003 stays unresolved, but both advocates' readings reject a raise for it (debate-transcript Convergence Assessment). |
| X-001, C-010 | "Orca's provenance rule prefers it" (V2:9) | `CAPS:158` routes Orca-tracked fan-out to the coordinator. V2 withdrew it (R1-V2 concession 1). V1 won both at 98%. |
| A-001, C-001 | "Removes Orca's fence" (V2:13) | Contradicted by `CAPS:99-100`. Replaced by Change 3's "widens by one generation" wording, not by V2's text. |
| C-007 | Treat "one setting" as the cost (V2:10) | The real cost is a new composite brief type with contract text and tests (R2-V1 NE1; R2-V2 item 8). V1 won C-007 (95%); Change 9 records the real cost. |
| A-002 | Define the scoped worker-session route now (R1-V2 position) | No use under the one-command brief (`SPEC:79`; R2-V2 item 6); keeps R5 and the shared Run inbox. Recorded only as the form (b) would take (Change 8). |
| (none) | Define the composite brief type now, so the trigger can fire sooner | Not asked for and not needed by any phase (ladder rung 1); R2-V2 item 8 shows it would be the whole of (b)'s benefit. The trigger names it as a precondition instead (Change 10). |
| C-004 | Keep V1's R1 rebuttal "the heartbeat gap moves to the parent" | Withdrawn by the V1 advocate (R2-V1 item 6); `check --wait` is a liveness signal (`CAPS:64`). Not carried; Change 6 states the correction. |
| C-002 | A per-run depth override | None is known (`CAPS:98`; DA A-004: inferred, not proven). Change 7 records the inference. |
| (none) | A live probe of the refusal from a depth-1 worker | Unsafe: if the refusal is not enforced, the probe creates a real nested worker (INV-004); the inventory ruled out live failure-path probes (`CAPS:171`). Change 15 uses a read-only trace instead. |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| 1 | Low | A person starts the coordinator with `worker-start` and every worker start is refused (presumed) | Remove M2 and the sentence in M10; behaviour is unchanged |
| 2 | Low | Revisit looks cheaper than it is | Restore V1:19 sentence |
| 3 | Low | Readers again treat depth as a total-count cap | Restore V1:8 framing |
| 4 | Low | Readers treat the refusal as proven | Remove the appended sentence |
| 5 | Low | Caveat lost again | Restore V1:12 text |
| 6 | Low | Cost of (a) unstated | Remove the M4 subsection |
| 7 | Low | Multi-profile case misread | Restore V1:9 text |
| 8 | Low | A later raise uses section 1.3's form | Remove M7 paragraph 1 |
| 9 | Low | A later raise underestimates its cost | Remove M7 paragraph 2 |
| 10 | Medium | Coordinator gains a run-notes duty that nobody reads; trigger never fires | Remove the 2.3 sentence; trigger reverts to "never" in practice |
| 11 | Low | A raise happens before the mailbox question is answered | Remove M7 paragraph 3 |
| 12 | Medium | Four spec places change; a wrong replacement could narrow a true claim | Revert each line to `SPEC:27`, `SPEC:36`, `SPEC:315`, `SPEC:350-354` |
| 13 | Medium | A new worker-session rule; a worker that breaks it is caught only after the fact | Remove the WC-13 row and its `SPEC:58` mention; the presumed refusal is the only guard again |
| 14 | Medium | A legitimate Task the person created by hand would not be started by the coordinator | Remove the 2.3 bullet; or narrow it to Tasks created by workers |
| 15 | Medium | The trace ends "not found" for some calls (minified code) | The row's pass condition already accepts a recorded "not found"; remove the row to roll back |
| 16 | Medium | A second profile with another value fails every phase until the person answers | Remove AC-C6 |
| 17 | Low | The recommendation loses its strongest-sounding reason | Restore the A-003 wording |
| 18 | Medium | Transcript search misses a call if AC-0.6 finds tool calls are not named | Falls back to `--source terminal` as 7.2 step 5 already does; remove the item to roll back |
| 19 | Medium | Wider scan flags prose that names Orca verbs | Add a named exclusion, or restore the `SPEC:206-211` block |

Overall Medium: Changes 1-9, 11 and 17 are wording in the D5 position; Changes 10, 12-16, 18 and 19 add requirements or checks to the spec, which the next consolidated spec revision applies (CR-01:3 names the same round).

## Review Status
- [x] Auto-approved (default; `--interactive` was not set)
- [ ] User-approved (--interactive)
- Approved by: auto
- Analytical review (Step 4 "analytical agent reviews"): one fresh `rf-analyst` pass, 2026-11-02. First verdict FAIL with 3 blocking findings: (B1) the AC-0.7 grep sat in a table cell, against `SPEC:202`, and named no path; (B2) the AC-C6 command was written with escaped quotes and failed when copied; (B3) INV-001's open half had no accepted-risk entry. All three fixed: AC-0.7's command moved to a fenced block with its path (Change 15), AC-C6 given as a fenced command that was re-run and exits 0 (Change 16), INV-001 moved under AR-1 and AC-0.7 widened to trace a person-opened session's depth. Its 12 minor findings were also applied (Agent-tool wording in R1 and D5; "presumed" in D5 (a); mailbox hedged; WC-13 relaxation listed as a (b) cost; INV-007 cap wording; Change 6 win list; E4 punctuation; non-goal 2 wording; AC-C6 edge cases; AC-C1 prose and plugin-core exclusion; AC-0.1 ripple noted in Change 13; R2-V2 item 8 citation). Its zero-defect self-audit re-read more than 40 cited lines and found none wrong.
- Re-review of B1-B3 (fix cycle 1 of at most 2, per PR #343): **PASS** from the same reviewer, received after Step 5 had run on the fixed plan. B1: AC-0.7's grep is in the fence with its path, run verbatim, same 3 files, exit 0. B2: AC-C6 run verbatim with the variable set and unset, both print `"nestedWorkerMaxDepth":1`, exit 0. B3: the INV-001 row points to AR-1 and Changes 1 and 15; still three AR entries. No new blocking problem. One minor note, recorded and not fixed (PR #343: minor findings never start a fix pass): with `-h`, AC-C6 cannot show which profile is silent when a file lacks the key, so the phase report should compare the line count with the number of profile files.
- Approval timestamp: 2026-11-02 (after the review fixes)
