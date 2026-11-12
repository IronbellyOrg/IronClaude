# Round 1 Advocate Statement: Variant 1 (opus, architect)

- Debate: sc:adversarial, Orchestrator Mode Phase 1 (#339) requirements spec
- Round: 1 (opening, parallel)
- Advocate for: V1 = `variant-1-opus-architect.md` (emphasis: maintainability and extension scaffolding)
- Inputs read: `debate-protocol.md` lines 105-144; `diff-analysis.md` lines 1-235; V1 lines 1-333; V2 lines 1-313; V3 lines 1-431; `seed-brief.md` lines 50-70
- Citation form: `V1:148` = line 148 of variant 1; `Seed:63` = seed brief line 63; `D-A` = diff-analysis.md

## 1. Position summary

V1 should be the base document for the merge. It is the only variant whose classification table is total and reachable as written (idle is rule 7, an explicit `fallback` is rule 8, V1:153-156). Its stall rule agrees with the seed (V1:148, Seed:56). Its module boundaries, rule order, read/write split and JSON shape are each pinned by a named test (V1:84, V1:89, V1:90, V1:71, V1:114). Later phases read its `rows` (V1:234) and grow through named extension points (V1:37, V1:125-127), so the cheapest time to fix the read model's shape is now.

V1 is not complete. It drops the Shift Brief it says it copies (X-014), has no per-session next action the seed requires (X-015, Seed:63), writes to an exact path that can collide (X-019), has no symlink rule (C-041), and its WC-14 end condition never ends for a rejected result (C-022). On those points V3 or V2 is better and this statement says so. Recommended merge: V1's structure and safety rules as the base; V3's report section contract, re-run idempotency and inspection-only next steps; V2's real-git control experiment, per-row `evidence` field and failure-table format.

## 2. Steelman of the opposing variants

### V2 (opus, analyzer), strongest version

V2 treats the observer effect as the first design constraint, not a detail (V2:22): a naive sweep turns healthy workers into blocked ones through WC-9. Its answer is the only one that proves the lock-free property against real git instead of trusting the argv: NFR-002 pairs the argv test with a real-git control experiment (V2:98, V2:273, D-A U-011). That is a falsifiable test of the one failure in which the sweep harms a live worker (F7, V2:245). V2 gives every row an `evidence` tuple naming which field of which source decided the class (V2:139-141), so the person need not open a session to learn why a row says stalled. Its failure table pairs each failure with evidence it is real and the test that proves containment (V2:240-247). Its negative `git check-ignore` AC proves `.dev/tasks/` stays tracked (V2:93), and R8 names the self-observation loop the ignore line prevents (V2:262-265). It places could-not-determine rows before working rows because an unknown can hide a person-wait (V2:211). Its provenance header records the host git version (D-A S-012).

### V3 (haiku, backend), strongest version

V3 is the most defensive about what the sweep does not know. It alone has a re-run contract: dated base name plus collision suffix, exclusive reservation, never overwrite, and a "Report complete" footer to tell crash leftovers apart (V3:181-187). It bounds reads by size (V3:137), keeps reports owner-only (D-A U-024, V3:143), shows unknown totals as lower bounds that must reconcile (V3:114), and keeps the activity window from hiding unresolved work (FR-013, V3:92). It reads the seed literally on the Orca-down case: no Run and no reachable binding means scope is not established, so exit 2 (V3:166, Seed:63). Its report contract is the fullest: source coverage, both ledgers, Shift Brief and "What I could not determine" plus footer (V3:298-307). Its Sessions table has a "next inspection" column (V3:303) that meets the seed's "next action" criterion without recommending any action (V3:335). Its WC-14 end condition, "every result has been inspected and its admission or rejection recorded" (V3:324-325), terminates for rejected results, which V1's does not.

## 3. V1 strengths, with evidence

1. **Total, reachable precedence table.** Idle is rule 7 and a named `fallback` is rule 8 (V1:153-154), with the reason stated (V1:156). V2 lists idle after "anything else" under first-match-wins, so idle is unreachable (V2:145, V2:155-156) while V2's FR-003 AC expects idle (V2:58). V3 leaves the position unstated (V3:230-236). Only V1's table can be implemented as written.
2. **Stall rule matches the seed.** Rule 2 requires `fenced_evidence == "absent"`; `unreadable` or an unreadable transcript gives could not determine with a named note (V1:148). This keeps Seed:56. V3 agrees (V3:222); V2 does not (X-002).
3. **Unknown gate policy stays unknown.** Rule 1 returns could not determine when the gate policy cannot be read (V1:147, D-A U-008), and `gate_policy` is an explicit nullable field (V1:136).
4. **Rule order pinned by name.** NFR-010 asserts `[r.name for r in RULES]` equals the spec list (V1:90); every JSON row carries `class` and `rule` (V1:234). A later phase that inserts a rule must change a test, so precedence drift is visible in review (R4, V1:276).
5. **Enforced module boundaries.** The module table lists May import and Must not import per module (V1:101-108), and B1 pins the one-way edge `commands -> {probes, classify, report} -> models` with an AST import test (V1:114). V3 has no table (V3:19-22, D-A S-005).
6. **Read/write split for later phases.** FR-021 keeps every write verb out of the sweep package, with a static forbidden-verb test (V1:71). B3 gives Phase 2 its own package, seam and allowlist and makes it re-collect before acting (V1:116). This is the one safety property that must hold across phases (D-A U-004, rated High).
7. **Stable machine output.** `schema_version: 1`, every key always present, additive-only, golden key-set test (V1:89, V1:234).
8. **Smallest git surface.** `status --porcelain --branch` plus one `rev-parse` for the default root, and no `log`, `branch`, `stash` or `worktree list` (V1:197-202, V1:43). Unmerged commits are not observed, which is safe because removable is never `yes` (V1:202).
9. **WC-14 forbids recommendations.** "The sweep recommends none of these actions" (V1:315) keeps the classifier from becoming an actor (V1:244). V3 agrees (V3:335).
10. **Orca allowlist covers what the rules need.** V1 includes the non-ready `task-list --run` because rule 1 needs the gate policy line (V1:190). V3 omits it (V3:270) while still needing blocked-gate policy (V3:77, V3:202).
11. **Testable without globals.** `Budget` is passed into `collect` (V1:178); `SweepContext` with `now` and `window` is a parameter of `classify_all` (V1:57, V1:105, V1:133); the pure core has an AST import test (V1:84) and a determinism test (V1:85).
12. **Later phases mapped to extension points.** The out-of-scope table gives each later phase its blocker and the extension point it will use (V1:37, D-A U-001); the extension table says how each point grows (V1:125-127).
13. **Unknown package state.** An unreadable ledger is `unknown` and prints could not determine (V1:167); V2 has no state for it (V2:160-165).
14. **Self-maintaining contract test.** Renaming `test_never_as_worker_list_names_all_seven_commands` to a count-free name (V1:248) removes a forced rename from every future never-as-worker addition.

## 4. Critique of V2 and V3, with evidence

### V2

1. **Rule 2 can label a row stalled without proof (X-002, high).** Rule 2 fires on `consumer_fenced is not True` (V2:150), so `None` passes. Rule 3 only fires on `consumer_fenced is True` (V2:151), so its "fenced evidence not readable" text never catches `None`. V2's own root-cause note guards `worker_done_observed` against `None` but not `consumer_fenced` (V2:158). This breaks Seed:56 and V2's FR-009 property test, which allows stalled only where "no fenced evidence" exists (V2:70). V2's R2 rates a false stalled as high impact (V2:256), so the bug sits on V2's own worst risk.
2. **Idle is unreachable (X-007).** "First matching rule wins" (V2:145), rule 7 "anything else" (V2:155), then idle (V2:156). FR-003's AC expects `idle` (V2:58). The spec cannot pass its own test.
3. **The sweep recommends actions (X-003, high).** WC-14 lets the sweep recommend stop-and-cancel, removal and a new Task (V2:228, OQ-4 V2:294), and FR-022 lets the report print them as proposals (V2:86). A sweep that cannot observe open PRs or report reads (V2:74) should not propose removal; that is the risk the read-only constraint exists for (Seed:52). OQ-4 keeps the alternative sentence ready (V2:294), which concedes this half is contested.
4. **Real git weakens the no-subprocess guard (X-010).** NFR-004 lets `subprocess.run` accept `argv[0] == "git"` session-wide (V2:100), which weakens the read-only proof for every test, not only the control experiment. The experiment is valuable (C-011); its scope should be one isolated test.
5. **Binary name drift (X-009).** `_orca` runs `["orca", *args]` (V2:175) while FR-020 speaks of "a missing `orca-ide` binary" (V2:84). Which name is correct is UNVERIFIED, but V2 contradicts itself.
6. **Extra git verbs for little gain.** `git log` per child (V2:200) adds a verb and up to N calls to report "unmerged" (V2:138), a fact that can only add a `no` reason to a value that is never `yes` (V2:74). `git --version` (V2:201) guards a case that already fails safe: a git too old for the flag should fail the call, and a failed seam call marks the source unscanned. UNVERIFIED: the exact exit code git returns for an unknown global option.
7. **No `unknown` package state (C-006).** V2's five states (V2:160-165) have nowhere to put an unreadable ledger, so it falls into `unfinished` by default ("has no `FINAL:` line", V2:164).

### V3

1. **Git allowlist is not exact (X-004, high).** V3 permits "read families `rev-parse`, `log` and `branch`" (V3:281) and leaves the exact argv to a later gate (V3:272-273, V3:283-285). Seed:64 requires tests that every recorded argv is in the exact allowlist; a family with deferred arguments cannot be tested. V3 itself bans wildcards in the final allowlist (V3:275).
2. **GQ-101 needs an argv nobody chose (X-005).** Active-local evidence is a difference "from the fixed base reference" (V3:246), found by comparison "against a fixed base tree; select and verify any required base-reading argv" (V3:285). The one `status --porcelain --branch` call already lists changed and untracked paths under a package folder (V1:199, V2:73, V2:276). V3 adds an unspecified second mechanism to the safety-critical surface.
3. **Missing Orca read it needs (X-011).** V3's closed forms have only `task-list --ready` (V3:270), yet FR-008 and rule 1 depend on blocked-gate policy (V3:77, V3:202, V3:218-220). Either rule 1 never has its input or the allowlist grows after it was closed.
4. **Live check conflicts with the seed (X-016).** "Require a separately authorized disposable-Run check before release" (V3:403) conflicts with Seed:54 if release is part of this work. It is an owner decision, not a spec requirement.
5. **WC-14 requires a timer Phase 1 lacks (X-008).** "Keeps a periodic sweep scheduled while work remains" (V3:327), while V3 says Phase 1 does not implement the scheduler (V3:51). See C-023 in section 6 for where this advocate concedes on owner grounds.
6. **No pin phrases (C-026, X-017).** V3's AC says pins "name `/sc:sweep`" (V3:108) but lists no phrases, and its text says "Reports are dated local files, never posted" (V3:334), not the pinned "it is never posted". Seed:67 ("pinned by contract tests") has no concrete pin set.
7. **No module table or boundary test (S-005).** Modules are named in prose only (V3:19-22). Nothing stops `classify` importing `probes`.
8. **Removal blockers incomplete (X-006).** V3's list (V3:251) omits interrupted archive, although V3 says `.archiving` must not be cleared (V3:243).

## 5. Weaknesses in V1 this advocate concedes

1. **Shift Brief dropped (X-014).** V1:208 says the layout copies header, Attention Ledger and Shift Brief, but the section list has none (V1:223-230). V1 contradicts itself. Take V3's section list (V3:298-307).
2. **No next action per session (X-015, C-038).** Seed:63 requires class, waiting-on and next action for every session; V1's Sessions row has none (V1:228). V3's "next inspection" (V3:303) meets the seed and still recommends no action, so it fits V1's WC-14 closing sentence.
3. **No could-not-determine section.** V1 leaves those rows inside Sessions. V2 (V2:211) and V3 (V3:307) give them their own section; V2's reason (an unknown can hide a person-wait) is sound.
4. **Same-second collision (X-019, C-019).** V1's exact path (V1:210) leaves overwrite behaviour unspecified. V3's suffix plus exclusive reservation (V3:181-187) is correct; the AC should check the dated base name.
5. **No re-run contract (C-020).** V1 has determinism only (V1:85). V3's dedicated section (V3:148, V3:179-187) is better.
6. **WC-14 end condition does not terminate for rejected results (C-022).** "Settled and been admitted": a rejected result is never admitted, so the loop never ends. V3's "admission or rejection recorded" (V3:324-325) fixes it.
7. **No symlink rule (C-041).** A grep of V1 finds no symlink or `resolve()` rule for disk reads. V2 (F9, V2:247) and V3 (V3:291) have one.
8. **Lock-free proof trusts the argv only (C-011).** V1's recorded-argv test (V1:82) proves intent, not effect. V2's control experiment proves effect.
9. **Periodic sweep (C-023, X-008).** The owner memory index in this session's context records "keep a cron sweep" as an owner order for coordinators (memory file not read, UNVERIFIED). If that holds, V1's "allowed, not required" is weaker than V3's requirement.

## 6. Per-point positions (S, C, X)

Confidence is 0-100 that the named choice is right for the merged spec.

### Structural

| Point | Preferred | Conf. | Evidence |
|---|---|---|---|
| S-001 | V1 | 50 | V1's table records Emphasis and Date (V1:3-10); V3 has no date. Cosmetic. |
| S-002 | merge V1+V3 | 55 | V1's 14 numbered sections as base, plus V3's "CLI contract and re-run idempotency" section (V3:148), which no other variant has. |
| S-003 | V1 | 65 | ID / Requirement / AC tables (V1:49-75) make a missing AC visible at a glance; V3's two-line form does not. |
| S-004 | V1 | 60 | Any base forces renumbering; V1's FR-001 is the CLI like V2's, so fewer IDs move than with V3's (D-A S-004). |
| S-005 | V1 | 85 | Module table plus B1-B5 and extension table (V1:95-127); V3 has prose only (V3:19-22). |
| S-006 | V1 | 60 | Typed frozen dataclasses (V1:129-169); V2 is equally typed, V3 has no field types. |
| S-007 | V2 | 70 | Evidence and Test columns (V2:240-247) make every failure checkable; V1's Exit column can be added to it. |
| S-008 | V2 | 60 | Likelihood and impact split (V2:253-263) is more informative than V1's one rating. |
| S-009 | V2 | 55 | Root-cause column (V2:271-285) explains why each gap mattered. |
| S-010 | V2 | 65 | OQ-1..OQ-8 IDs (V2:289-298) can be cited in later rounds; V1 has none. |
| S-011 | merge V1+V3 | 50 | Keep V1's per-requirement ACs and add V3's verification checklist (V3:414-423) as a release gate. |
| S-012 | V2 | 60 | Exact line ranges plus host git version (V2:9) is the most auditable provenance. |
| S-013 | V2 | 60 | A fenced block with heading (V2:225-229) is copy-exact into `WORKER-CONTRACT.md`. |

### Content

| Point | Preferred | Conf. | Evidence |
|---|---|---|---|
| C-001 | V1 | 85 | Only V1's table is total and reachable (V1:153-156); V2's idle is dead (V2:155-156). |
| C-002 | V1 | 80 | Unknown policy on a live row gives could not determine (V1:147); V2 leaves it unspecified (V2:149). |
| C-003 | merge V1+V3 | 90 | Both require known-absent fencing (V1:148, V3:222); V2's `is not True` admits `None` (V2:150). |
| C-004 | merge V1+V3 | 70 | V1's partial note (V1:152) plus V3's "finished never means admitted" (V3:229). |
| C-005 | merge V1+V3 | 60 | V1's "creator: could not determine" plus V3's "ownership review" wording (V3:226); V2's "foreign" asserts what is unobserved. |
| C-006 | merge V1+V2 | 60 | Keep V1's six states incl. `unknown` (V1:158-167); adopt V2's rule that archive-blocked blocks removal (V2:168) as the conservative choice. |
| C-007 | V1 | 80 | One status call answers GQ-101 (V1:199); V3's base-tree comparison has no chosen argv (V3:285). |
| C-008 | V1 | 80 | Includes non-ready `task-list --run` for gate policy (V1:190); V3 lacks it (V3:270). |
| C-009 | merge V1+V2 | 70 | Status only: V1's no-log rule (V1:202) plus V2's plain-walk root (V2:203), so neither `log` nor `rev-parse` is needed. |
| C-010 | V1 | 70 | Seam builds the flag and env (V1:176); an old git fails the call and the source is unscanned, so V2's version gate adds a verb for a fail-safe case (UNVERIFIED exit code). |
| C-011 | merge V1+V2 | 70 | V1's argv and env test (V1:82) plus V2's real-git control experiment (V2:98), isolated to one test. |
| C-012 | V2 | 65 | Plain path walk (V2:203) removes the only `rev-parse` from V1's allowlist. |
| C-013 | V1 | 60 | Unmerged is unobservable without `git log`, and removable is never `yes` anyway (V1:202). |
| C-014 | merge V1+V3 | 70 | Cursor flag UNVERIFIED until capture (V1:187), and V3's partial-coverage and dedup rule (V3:63, V3:274); V2's flag is guessed. |
| C-015 | V1 | 55 | Disk-only exit 0 keeps person waits visible when Orca is down (V1:69); see X-001 for the seed-reading risk. |
| C-016 | merge V1+V3 | 60 | Same 0/1/2 meanings (V1:68) plus V3's "exit 0 means the report was published" (V3:161-164). |
| C-017 | merge V1+V2+V3 | 60 | Key `class` and additive-only (V1:89, V1:234); V2's per-row `evidence`, `notes`, `safe_to_close` (V2:81); V3's zero counts and ID-only `waiting` (V3:167-177). |
| C-018 | V3 | 70 | Fullest section contract incl. Shift Brief and could-not-determine (V3:298-307); V1 drops the Shift Brief (V1:223-230). |
| C-019 | V3 | 75 | Collision suffix, exclusive reservation, footer (V3:181-187); V1's exact path can collide. |
| C-020 | V3 | 75 | Dedicated re-run section (V3:179-187); V1 has determinism only (V1:85). |
| C-021 | V1 | 65 | Byte-identical report and JSON from injected `now` (V1:85); V2's "apart from the header timestamp" is weaker when `now` is injected. |
| C-022 | merge V2+V3 | 70 | V3's "admission or rejection recorded" (V3:324-325) terminates; V2's "shown by the Run's own task list" (V2:228) makes it observable. V1's never ends for a rejection. |
| C-023 | V3 | 55 | Owner order "keep a cron sweep" in this session's memory index (UNVERIFIED file content) favours V3:327; the timer itself stays out of Phase 1 (V3:51). |
| C-024 | merge V1+V3 | 85 | "Recommends none" (V1:315) with V3's explicit verb list (V3:335); V2's proposals fail V3's AC (D-A X-003). |
| C-025 | merge all three | 55 | Add V2's lock-free sentence (V2:228) and V3's "a missing heartbeat is absence, never death" (V3:328-329) to V1's text. |
| C-026 | V1 | 85 | Three pin phrases, `NEVER_AS_WORKER` to 9, count-free rename (V1:248); V3 has no phrases (V3:108). |
| C-027 | merge all three | 70 | Union: V1's unwritable output and unknown field, V2's symlink and old git, V3's input change, duplicate Dispatch, process killed. |
| C-028 | merge V1+V2 | 65 | V1's patched entry points and HOME/XDG in root (V1:81) plus V2's (path, size, mtime_ns, sha256) snapshot (V2:97). |
| C-029 | merge V1+V3 | 60 | Injected `Budget` (V1:178) plus V3's per-call remaining time and byte limits (V3:125, V3:137). |
| C-030 | merge V1+V3 | 70 | V1's fold-to-space keeps words apart (V1:66); add V3's HTML neutralizing and no active links (V3:317-318). |
| C-031 | merge V1+V3 | 70 | Revert as one unit and keep the ignore line until reports are dealt with (V1:330), plus V3's "never remove `.dev/tasks/`" (V3:425-431). |
| C-032 | V1 | 60 | Design for list plus show and capture before step 1.2 (V1:308) puts the capture before the code that depends on it. |
| C-033 | V1 | 65 | Copying sections and citing `495eb96d` (V1:311) makes the spec stand alone; V2 agrees. |
| C-034 | merge V1+V3 | 60 | V1's ordering (V1:313) plus V3's overlap check and "do not silently omit WC-14" (V3:406). |
| C-035 | merge V1+V3 | 70 | V1's join rule (V1:60) plus V3's exemptions for open Tasks and waits and "unknown timestamps never idle" (V3:92, V3:236). |
| C-036 | V1 | 70 | Ten dimensions on every row, default `unknown` (V1:136); V2 omits them. |
| C-037 | merge V1+V2 | 70 | V1's `rule` name plus V2's `evidence` tuple (V2:139-141). |
| C-038 | V3 | 75 | "Next inspection" (V3:303) meets Seed:63 without recommending; V1 has nothing (V1:228). |
| C-039 | merge V1+V2 | 65 | V1's static forbidden-verb test (V1:71) plus V2's negative `worker-read` test with zero subprocess calls (V2:99). |
| C-040 | V3 | 65 | Symlink-resolved check and no overlap with input dirs (V3:156-157) close cases V1:54 leaves open. |
| C-041 | merge V2+V3 | 75 | `resolve()` check (V2:247) and reject escaping symlinks (V3:291); V1 has no rule. |
| C-042 | V1 | 50 | "Carried, not fixed" (V1:302) is neutral; V3's "documentation debt" adds nothing testable. |
| C-043 | V1 | 70 | REPORT citations plus extension-point column (V1:35-41); V3 has no citations. |

### Contradictions

| Point | Preferred | Conf. | Evidence |
|---|---|---|---|
| X-001 | V1 | 55 | Seed:63 targets "no binding"; with Orca down the binding is unknown, not absent, and a disk-only read-only report still surfaces person waits (V1:69). V3's literal reading (V3:166) is defensible; owner may decide. |
| X-002 | merge V1+V3 | 95 | V2 rule 2 admits `None` fencing (V2:150-151) against Seed:56 and V2's own FR-009 AC (V2:70). |
| X-003 | merge V1+V3 | 85 | The sweep recommends nothing (V1:315, V3:335); V2's proposals (V2:228, V2:86) cut against Seed:52. |
| X-004 | merge V1+V2 | 70 | Status only (V1:202) with V2's root walk (V2:203) gives the smallest exact allowlist; V3's families (V3:281) cannot pass Seed:64. |
| X-005 | V1 | 80 | One status call lists changed paths under the package (V1:199, V2:73); V3's base-tree argv is unchosen (V3:285). |
| X-006 | merge V1+V2 | 60 | V1's states with V2's "archive-blocked blocks removal" (V2:168); V3 omits interrupted archive (V3:251). |
| X-007 | V1 | 85 | Idle as rule 7 before the fallback (V1:153-154); V2's idle is unreachable (V2:155-156). |
| X-008 | V3 | 55 | Owner "keep a cron sweep" order (memory index, UNVERIFIED) favours V3:327; concede. |
| X-009 | V1 | 60 | `orca-ide` (V1:175), shared by V3 (V3:270) and named by V2's own FR-020 (V2:84); correct name UNVERIFIED until capture. |
| X-010 | V2 | 65 | Real git only in one isolated `tmp_path` test is the only way to prove the lock claim; keep V1's raise-on-subprocess everywhere else. |
| X-011 | V1 | 80 | Gate policy needs non-ready `task-list --run` (V1:190); V3 needs the policy (V3:202) but lacks the read (V3:270). |
| X-012 | V1 | 60 | `class` (V1:234) is the plain word; `cls` is a Python-ism leaking into a schema. |
| X-013 | merge V1+V3 | 70 | Keep the ignore line until reports are dealt with (V1:330, V3:427); V2 removes it while keeping reports (V2:310-311), which dirties `git status`. |
| X-014 | V3 | 85 | Concede: V1 claims a Shift Brief (V1:208) and omits it (V1:223-230); V3 includes it (V3:306). |
| X-015 | V3 | 80 | Concede: Seed:63 needs next action per session; V3's "next inspection" (V3:303) supplies it. |
| X-016 | V1 | 75 | Seed:54 bars live Orca in this work; V3's disposable-Run check (V3:403) belongs to the owner, not the spec. |
| X-017 | V1 | 80 | V1 text and pins carry "it is never posted" (V1:248); V3 says "never posted" in other words (V3:334) and lists no pins (V3:108). |
| X-018 | V1 | 60 | A `guard refused:` body is positive Orca terminal evidence (V1:152); V3's "not finished" discards it, V2's "partial" mislabels it. |
| X-019 | V3 | 75 | Concede: suffix or clean failure (V3:181-187); V1's exact path leaves overwrite unspecified (V1:210). |

## 7. Shared assumptions (A)

| Point | Answer | Reason |
|---|---|---|
| A-001 | ACCEPT | Option A1 is stated in all three and the seed (Seed:89); no variant offers a better placement. |
| A-002 | QUALIFY | True for the sweep's own `_git`, but only if Orca's read verbs do not run lock-taking git themselves (A-101). |
| A-003 | QUALIFY | Right scope rule; the `run-current` JSON form is UNVERIFIED (V3:272) and its visibility to a child process is A-102. |
| A-004 | ACCEPT | WC-10 makes `exited` the only proof (Seed:45); the dissent is V2's rule 2 bug, not the assumption. |
| A-005 | ACCEPT | Result read, report read and open PR are unobservable in Phase 1 (V1:202, V2:74). |
| A-006 | QUALIFY | The join rule is sound, but rests on A-104, A-105 and A-106, all unverified. |
| A-007 | QUALIFY | The bounds are stated by REPORT; that a typical Run fits within them is unverified (A-107). |
| A-008 | QUALIFY | Path and ignore line yes; second-resolution uniqueness no, so add V3's collision suffix (X-019). |
| A-009 | ACCEPT | Click usage errors exit 2 is standard Click behaviour; V2 marks it as an assumption (V2:313), worth one test. |
| A-010 | QUALIFY | Correct on GitHub-flavoured Markdown; other viewers depend on A-108. |
| A-011 | ACCEPT | No non-consuming question read exists (Seed:74); "partial" coverage is the honest label. |
| A-012 | ACCEPT | WC-14 placement and gating on owner GQ-11 and PR #422 are stated (Seed:78). |
| A-013 | ACCEPT | Counts 113 / 88 / 25 come from GAPS line 138 (Seed:79); carrying, not editing, REPORT is right. |
| A-014 | ACCEPT | Default 6 h is fixed by the topic (Seed:77). |
| A-015 | ACCEPT | GQ-110 fixes one status call per worktree (Seed:64), and it is enough for GQ-101 (X-005). |
| A-016 | ACCEPT | A caller check cannot tell a worker from a coordinator in Phase 1; the contract rule is the available guard. |
| A-017 | QUALIFY | Mock both seams everywhere, plus one isolated real-git test for the lock claim (X-010). |
| A-101 | QUALIFY | UNVERIFIED and a real hole: `--no-optional-locks` on `_git` cannot cover Orca's own git. Record as a risk and probe in the step 1.0a capture. |
| A-102 | QUALIFY | UNVERIFIED; if false, every skill-run sweep exits 2 with a clear message, which is visible, not harmful. |
| A-103 | QUALIFY | UNVERIFIED; if no source exists, every exited row is could not determine, the safe direction. |
| A-104 | QUALIFY | UNVERIFIED; needs the capture. V3 notes the CLI can migrate names (V3:288), so pin the format in a fixture. |
| A-105 | QUALIFY | UNVERIFIED; needs the capture before the person-started join is coded. |
| A-106 | QUALIFY | A plain read changes atime, not mtime, so the sweep does not move the boundary; whether mtime tracks activity is UNVERIFIED. |
| A-107 | REJECT | The design must not assume 50 or fewer rows; bound-reached rows are already counted and reported (V1:263). |
| A-108 | QUALIFY | GitHub-flavoured Markdown honours `\|` in cells; other viewers UNVERIFIED. |

## 8. Tally

Over the 75 S, C and X points:

| Outcome | S | C | X | Total |
|---|---|---|---|---|
| Prefer V1 alone | 5 | 14 | 9 | 28 |
| Merge that includes V1 | 2 | 20 | 5 | 27 |
| Concede to V2 or V3 (no V1) | 6 | 9 | 5 | 20 |
| **All** | **13** | **43** | **19** | **75** |

Shared assumptions (25): ACCEPT 10, QUALIFY 14, REJECT 1.

Two strongest critiques:

1. V2 rule 2 lets unknown fencing produce stalled (proved) (X-002, V2:150-151), against Seed:56 and V2's own FR-009 AC; and V2's idle can never fire (X-007, V2:155-156).
2. V3's git read families with deferred arguments, plus an unchosen base-tree argv for GQ-101, cannot pass the exact-allowlist test Seed:64 requires (X-004, X-005, V3:281-285); V3 also lacks the `task-list --run` read its own rule 1 needs (X-011).
