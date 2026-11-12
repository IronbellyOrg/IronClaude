# Round 1 Advocate: Variant 2 (opus, analyzer)

- Variant defended: V2 = `variant-2-opus-analyzer.md`
- Lens: root-cause analysis and evidence-based reasoning for architecture
- Date: 2026-11-08 (from session context)
- Inputs read: `diff-analysis.md`, the three variants, `../../seed-brief.md`. No file under `qa/`, no REPORT, GAPS or code file was read in this round, so claims about those sources are the variants' claims (UNVERIFIED).
- Citation form: `V2:150` = line 150 of variant 2; `Seed:63` = line 63 of the seed brief.

## 1. Position summary

V2 contributes the evidence chain behind each safety claim: why no lock is taken (a real-git control experiment, NFR-002 at V2:98), why `.dev/tasks/` stays tracked (a negative `git check-ignore` AC, V2:93), why the report does not observe itself (R8, V2:262-265), and which signal produced each class (`rule` plus `evidence`, V2:139-141). Those parts should survive any merge.

V2 also has real defects, and this file concedes them plainly. The worst is X-002: V2 rule 2 (V2:150) lets an exited row with unknown fencing (`consumer_fenced is None`) become stalled (proved). That breaks Seed:56 and V2's own FR-009 (V2:70), and V1 and V3 are right. V2 also loses on idle reachability (X-007), the binary name (X-009), the recommendation sentence (X-003) and same-second collisions (X-019).

The count over the 75 S/C/X points: 30 go to V2 (V2 alone, or V2 where V1 says the same), 31 are conceded to V1, V3 or V1+V3, and 14 are merges that keep a V2 part (section 10).

## 2. Steelman of V1 (architect)

At its strongest, V1 is a spec built so the design cannot drift:

- **The rule table is total by construction.** Idle is rule 7 and an explicit `fallback` is rule 8 (V1:145-156). Rule order is pinned by name (`[r.name for r in RULES]`, V1:90), so a later edit cannot silently reorder precedence.
- **Unknown inputs are never promoted to a firmer class.** Rule 2 needs `fenced_evidence == "absent"`, and `unreadable` gives could not determine (V1:148, V1:59). A live blocked row whose gate policy is unreadable also gives could not determine (V1:147, U-008).
- **Writes are kept out by structure, not habit.** Dependencies run one way, `commands -> {probes, classify, report} -> models`, pinned by an AST import test (V1:114). The sweep package never holds a write verb, and a static test checks `ALLOWED_ORCA` against a fixed forbidden list (V1:71, V1:116). Phase 2 must get its own seam and must re-collect its data.
- **The JSON schema stays stable.** Changes within `schema_version: 1` are additive only, checked by a golden key-set test (V1:89).
- **Rollback is conservative.** The `.gitignore` line stays until existing reports are dealt with (V1:330).
- **Later phases name their extension point** (V1:35-41, V1:120-127), so Phases 2 to 5 need not reopen Phase 1 modules.

Read this way, V1 is the variant most likely to still be correct after three later phases have been built on it.

## 3. Steelman of V3 (backend)

At its strongest, V3 treats the report as a published artifact with an integrity contract, not as a log line:

- **Re-runs are idempotent.** Each run reserves its path exclusively, adds a collision suffix, never overwrites, prints no success JSON after a failed write, and ends with a "Report complete" footer (V3:179-187, U-022). V1 and V2 never say what happens when two sweeps run in the same second.
- **Resources are bounded beyond call counts.** Byte limits apply: 1 MiB for contracts and ledgers, 256 KiB for transcript tails, 8 MiB for subprocess output (V3:137). Reports are owner-only (V3:143). Unknown totals are shown as lower bounds that must reconcile (V3:114, V3:309).
- **Rule 2 is strict.** "Unreadable fencing/completion evidence defeats this rule" (V3:222).
- **Waits are never aged out.** Open Tasks, explicit waits and unread-report candidates are exempt from the activity window (V3:93, V3:237), so a person-wait never drops into Historical.
- **The sweep never recommends an action**, and fixtures must contain none (V3:105, V3:335).
- **It is honest about its own evidence.** It says no code was inspected (V3:32-34) and keeps runtime non-consumption UNVERIFIED (V3:403).

Read this way, V3 is the variant that best protects the person from a misleading or half-written report.

## 4. V2 strengths, with evidence

1. **It is the only variant that tests the lock behaviour itself, not just the intent** (NFR-002, V2:98; U-011). All three variants rely on `--no-optional-locks` (A-002). A recorded-argv test proves only that the flag was passed, not that it stops the index rewrite on the git installed here. V3 says as much in its own risk list (V3:365). V2 runs real git in `tmp_path`. A control run without the flag shows the index rewritten, and the run with the flag shows it untouched. If the control run shows no rewrite, the test is skipped as inconclusive rather than passed. This is the only direct test of the seed's first safety item (Seed:52, GQ-103(1)).
2. **It gates on the git version** (V2:180, U-012). When git is too old for the flag, every git source is marked `unscanned: git too old`. Without the gate, an old git makes the safety flag silently do nothing.
3. **It proves `.dev/tasks/` stays tracked** (FR-026, V2:93, U-015). The `.dev/sweeps/` line in `.gitignore` (Seed:66) is Phase 1's only change to what git tracks. V2 alone has a negative `git check-ignore` AC proving `.dev/tasks/` is still tracked, which is an absolute rule in both CLAUDE.md files.
4. **It names the self-observation loop** (R8, V2:262-265, U-014). Without the ignore line, each sweep's previous report shows up as an untracked path, so the tree looks dirty because it was swept. This explains why Seed:66 matters, where the other variants only state it.
5. **Every class carries its evidence** (V2:139-141, C-037). Each row has a `rule` and an `evidence` field naming the field and its source. The stated reason (V2:141) is the success metric (Seed:47): a class with no reason sends the person back into the session.
6. **Could not determine is shown before working rows** (V2:211, U-016). An unknown row can hide a person-wait. Safety comes before completeness (Seed:27), so the person should see possible waits before confirmed work.
7. **Every git verb is an exact argv** (V2:197-203). The list is `status --porcelain --branch`, one `log --format=%H --max-count=1 <branch>..HEAD`, and `--version`. There is no `rev-parse`: `--root` is found by a plain path walk (V2:203), so there is one fewer git verb to justify. V3 leaves its exact argv to a later design gate (V3:282-285) and so cannot pass Seed:64.
8. **Unmerged commits are observed, not waved away** (FR-014, V2:75, U-017). One bounded `git log` per child worktree turns "removable" into a judgment backed by evidence. V1 skips this because removable is never yes (V1:202).
9. **Pagination has a test that fails if the design is wrong** (FR-005, V2:63). A 101-row fixture asserts exactly 2 list calls. V1 leaves the cursor UNVERIFIED (V1:187).
10. **The read-only snapshot covers the fixture `~/.claude/`** (NFR-001, V2:97). It records path, size, mtime_ns and sha256, so a write outside the repo, such as a ccsession cache, is caught too.
11. **Other evidence:** a two-part root cause (V2:11-22), failure-mode columns for "evidence it is real" and "test" (V2:237-247), a root-cause column in the GQ table (V2:271-285), and no new dependency (V2:105).

## 5. Critique of V1

1. **No Shift Brief and no next action** (X-014, X-015). V1 says it copies the #409 header, Attention Ledger and Shift Brief (V1:208), but its section list has no Shift Brief (V1:223-230), and the Sessions row has no next-action column (V1:228). Seed:63 requires class, waiting-on and next action for every session, and Seed:44 and Seed:88 name the Shift Brief. V1 is the only variant that fails a stated success criterion on report content.
2. **Stalled (proved) can never appear on a live sweep, and V1 does not say so** (V1:134, V1:148). `fenced_evidence` is always `unreadable` on live rows in Phase 1, so rule 2 fires only in fixtures. That is safe, and it is the same outcome as the X-002 fix conceded below. But V1 never labels the class fixture-only, as V2 rule 3 does for fenced (V2:151). Nor does it require a live exited row to keep Orca's `exited` verdict in its could-not-determine note. The person loses the most useful signal Orca gives without being told. The merge should add both.
3. **Lock-freedom is proved only by intent** (V1:81-82). Every real subprocess entry point is patched to raise, so V1 can only check that the flag sits at argv index 1. It cannot catch a git where the flag has no effect, and V1 has no version gate. The patch rule is right for the rest of the suite; it just leaves the first safety item without a direct test.
4. **`rev-parse` is allowed but not needed** (V1:200, X-004). A plain path walk finds the top level without spawning git. Every extra git verb is one more argv to justify against WC-9.
5. **Archive-blocked does not block removal** (V1:164, X-006). A package in `to-do/` with a `FINAL:` line has not been archived. Since safety outranks completeness (Seed:27), the conservative reading blocks removal. V1's reasoning, that the work is done, holds only if the commits have reached the remote, which V1 does not observe (V1:202).
6. **The rollback is right but its reasoning is thin.** Keeping the `.gitignore` line (V1:330) is correct, and I concede it. But V1 has no AC that `.dev/tasks/` stays tracked, which is the bigger risk of the same edit.

## 6. Critique of V3

1. **The exact allowlist is deferred, so Seed:64 cannot be checked** (V3:279-286, X-004). V3 allows the `rev-parse`, `log` and `branch` families but leaves their exact arguments to "a pre-implementation design gate". Seed:64 asks for a test that every recorded argv is in an exact allowlist, and a list of families cannot be tested that way. This is V3's largest safety gap, because GQ-103(1) is the first safety item.
2. **GQ-101 depends on an argv V3 never picks** (V3:246, V3:284-285, X-005). The "differs from the fixed base reference" check needs a base-reading git call that is in no list. The single `status` call per worktree (Seed:64, GQ-110) already shows changed or untracked paths under a package folder, which is what "active" means. V3 adds a second read surface without saying why the first is not enough.
3. **It requires a live check, which Seed:54 forbids** (V3:403, V3:421, X-016). A "separately authorized disposable-Run check before release" conflicts with "no live Orca ... launch in tests or in this work" (Seed:54), if the release is part of this work. The doubt behind it, whether a read consumes anything, is real. It belongs in the risk register as UNVERIFIED and in a later phase, not as a release gate.
4. **WC-14 adds a timer duty and loses a pin** (V3:327, V3:334, X-008, X-017). "Keeps a periodic sweep scheduled" turns an allowed practice into a required one. "Never posted" does not match the pin phrase "it is never posted" that V1 and V2 share, and V3 defines no pin phrases at all (C-026), against Seed:67.
5. **`task-list` is missing but still needed** (V3:266-271, X-011). V3's closed list has no non-ready `task-list --run <id> --json`, yet its model needs the blocked-gate policy (V3:202). Rule 1 would depend on a value V3 cannot read.
6. **When Orca is down the person gets nothing** (V3:165-166, X-001). With Orca down and no `--run`, V3 exits 2 and writes no report. The disk state (worktrees, packages, transcripts) is scoped by `--root`, not by the Run, and can still be read safely. Exiting 2 gives up completeness and gains no safety.
7. **The model has no field types** (V3:189-215). So it cannot state the None, False and absent distinctions behind X-002 precisely. V3's rule 2 wording is right, but nothing in its model makes an implementation keep it.

## 7. Concessions (X-002 first)

1. **X-002 / C-003: conceded to V1, using V3's wording.** V2 rule 2 (V2:150) requires `worker_done_observed is False`, a positive observation, but for fencing it only checks `consumer_fenced is not True`, so `None` (unknown) passes. The root cause is a None check applied to one input and not the other. V2's own note on rule 2 (V2:158) states the right principle, "must be a positive observation; `None` falls to rule 7", but applies it to `worker_done` and not to fencing. Rule 3's "fenced evidence not readable" path comes after rule 2, so it never sees the row. As written, V2 would label a live exited row stalled (proved) with no proof that fencing is absent. That breaks Seed:56, WC-10 and V2's own FR-009 property test (V2:70). The fix: rule 2 requires `consumer_fenced is False`, and None goes to could not determine with the note "Orca: exited; fencing not readable". V1's `fenced_evidence == "absent"` (V1:148) is the cleaner model.
2. **X-007 / C-001: conceded to V1.** In V2, idle comes after rule 7, "anything else" (V2:155-156), and the first matching rule wins (V2:145). Idle can never be reached, yet FR-003's AC expects it (V2:58). V1's order, idle as rule 7 and an explicit fallback as rule 8, pinned by name (V1:90), is correct.
3. **X-003 / C-024: conceded to V1 and V3.** V2's WC-14 sentence (V2:228) and FR-022 (V2:86) recommend stop-and-cancel, removal and a new Task. Seed:52 and Seed:88 ("no action controls") point the other way, and V2 already has the right sentence ready at V2:231. Use V3's wording, "recommends no stop, retry, release, merge or removal" (V3:335), with V1's pins. V2's "what to check next" column survives, limited to inspection steps (C-038).
4. **X-009: conceded to V1 and V3.** V2 writes `orca` in the argv (V2:175) but `orca-ide` in FR-020 (V2:84), so it contradicts itself. Use `orca-ide`; which name is actually correct is UNVERIFIED here.
5. **X-019 / C-019 / C-020: conceded to V3.** V2's "the dated path and nothing else" (V2:79) leaves a same-second overwrite undefined. V3's exclusive reservation and suffix (V3:181-187) fix it.
6. **X-018 / C-004: conceded to V3, with V1.** V2 marks a row finished, with note "partial", when `read_ok` is false (V2:154). That labels a row finished on evidence V2 could not read. V3's "unreadable contract: unknown evidence, not finished" (V3:352) is right.
7. **X-012 and X-013: conceded to V1.** The JSON key should be `class`, not `cls`, because the schema serves people and tools, not Python. On rollback, the `.gitignore` line stays until the reports are dealt with. V2 removes the line (V2:310) while keeping the reports (V2:311), which turns them into untracked noise.
8. **Also conceded:**
   - C-002, to V1 (U-008, V1:147).
   - C-030, to V1: V2 removes LF instead of folding it to a space, which joins words (V2:83 against V1:66).
   - C-036: V2 leaves out the ten #409 dimensions.
   - C-035 and C-040, to V3: its window exemptions and its symlink-safe `--output`.
   - C-023 / X-008, to V1: "allowed, not required" is more explicit than V2's wake-only.

## 8. Per-point positions

Tag key: OWN = V2 preferred, including where V1 says the same thing; CONCEDE = V1, V3 or V1+V3 preferred; MERGE = a merge that keeps a V2 part.

### Structural

| Point | Preferred | Conf | Tag | Evidence |
|---|---|---|---|---|
| S-001 | V1 | 55 | CONCEDE | V1's field table carries emphasis and date (V1:3-10); V3 has no date |
| S-002 | V2 | 65 | OWN | Separate root-cause and out-of-scope sections (V2:11, V2:35); V3 has no architecture section |
| S-003 | V1 | 55 | CONCEDE | ID / requirement / AC tables (V1:49-75) trace more easily than inline bullets |
| S-004 | V1 | 50 | CONCEDE | FR-001 = CLI in V1 and V2; V1's 13 NFRs make the larger base for renumbering |
| S-005 | merge V1+V2 | 70 | MERGE | V1's B1-B5 and extension table (V1:112-127) plus V2's data flow and rejected placements (V2:107-129) |
| S-006 | merge V1+V2 | 55 | MERGE | V1's typed frozen dataclasses (V1:133-141) inside V2's 7.1/7.2/7.3 split (V2:131-168) |
| S-007 | V2 | 70 | OWN | "Evidence it is real" and "Test" columns (V2:237-247) make every failure mode checkable |
| S-008 | V2 | 60 | OWN | Likelihood and impact rated separately (V2:253-263); V3's risks are unrated (V3:362-372) |
| S-009 | V2 | 60 | OWN | Root-cause column per gap (V2:271-285) |
| S-010 | V2 | 65 | OWN | OQ-1..OQ-8 IDs can be cited by later rounds (V2:289-298) |
| S-011 | V3 | 60 | CONCEDE | Separate verification checklist (V3:414-423) |
| S-012 | V2 | 70 | OWN | Exact line ranges plus host `git --version` (V2:9); V3 inspected no code (V3:32-34) |
| S-013 | V2 | 55 | OWN | Fenced block with heading (V2:225-229) is the exact text the contract pins test |

### Content

| Point | Preferred | Conf | Tag | Evidence |
|---|---|---|---|---|
| C-001 | V1 | 90 | CONCEDE | Idle as rule 7, explicit fallback rule 8 (V1:145-156); V2's idle is unreachable (V2:155-156) |
| C-002 | V1 | 80 | CONCEDE | Unknown gate policy on a live row gives could not determine (V1:147); V2 leaves it open (V2:149) |
| C-003 | merge V1+V3 | 95 | CONCEDE | V1's `fenced_evidence == "absent"` (V1:148) plus V3's wording (V3:222); V2's `is not True` lets None through (V2:150) |
| C-004 | V3 | 70 | CONCEDE | "Finished never means admitted" (V3:228-229); V2's note on unreadable rows is X-018 |
| C-005 | V3 | 60 | CONCEDE | "Never label them definitively foreign" (V3:226); V2's "foreign" (V2:152) claims ownership it cannot see |
| C-006 | merge V1+V2 | 75 | MERGE | V1's `unknown` state for an unreadable ledger (V1:167) plus V2's blocking of states 1-4 (V2:168) |
| C-007 | V2 (= V1) | 85 | OWN | One status call shows changed paths under the package (V2:73, V1:199); V3 needs an unchosen argv (V3:284-285) |
| C-008 | V1 | 75 | CONCEDE | Same six templates as V2 with `orca-ide` (V1:175); V2's `orca` contradicts V2:84 |
| C-009 | V2 | 70 | OWN | Exact `status`, `log`, `--version` argv (V2:197-203); V3 defers argv (V3:282); V1's rev-parse is unneeded |
| C-010 | V2 | 80 | OWN | Flag and env variable plus a version gate (V2:176-180); V3 drops the env variable (V3:279) |
| C-011 | merge V2+V1 | 75 | MERGE | V2's real-git control experiment in its own marked test (V2:98) plus V1's argv-index-1 check (V1:82) |
| C-012 | V2 | 70 | OWN | Path walk, no git call (V2:203); V3's method is unstated (V3:154) |
| C-013 | V2 | 65 | OWN | One bounded `git log` per child (V2:75); V1 skips it (V1:202); V3's argv is deferred (V3:282) |
| C-014 | merge V2+V3 | 60 | MERGE | V2's 101-row two-call AC (V2:63) plus V3's dedupe and partial coverage (V3:63, V3:274); cursor field UNVERIFIED (V1:187) |
| C-015 | V2 (= V1) | 55 | OWN | Disk state is scoped by `--root`, so exit 0 with a banner keeps completeness at no safety cost (V2:57); deviates from Seed:63, owner sign-off needed |
| C-016 | V3 | 60 | CONCEDE | "Exit 0 means the report was successfully published" (V3:161-164) |
| C-017 | merge V1+V2 | 70 | MERGE | V1's `class` key, additive-only rule and golden test (V1:89, V1:234) plus V2's `evidence` and `notes` (V2:81) |
| C-018 | merge V2+V3 | 75 | MERGE | V2's order with could not determine before working rows (V2:207-217) plus V3's source coverage and footer (V3:297-307) |
| C-019 | V3 | 80 | CONCEDE | Exclusive reservation and collision suffix (V3:181-187) |
| C-020 | V3 | 80 | CONCEDE | Explicit re-run section (V3:179-187); V2 only notes the loop (V2:262-265) |
| C-021 | V2 | 70 | OWN | "Apart from the header timestamp" with a fixed `now` (V2:102) is the only form that can be tested |
| C-022 | V2 | 55 | OWN | "As shown by the Run's own task list" (V2:228) names the evidence for "settled" |
| C-023 | V1 | 60 | CONCEDE | "Allowed, not required" (V1:245) states the scheduled case; V2 only says on wake |
| C-024 | merge V1+V3 | 85 | CONCEDE | "Recommends no stop, retry, release, merge or removal" (V3:335) with V1's pins (V1:248); V2:228 recommends actions |
| C-025 | merge V2+V3 | 60 | MERGE | V2's lock-free sentence (V2:228) plus V3's "a missing heartbeat is absence, never death" (V3:329) |
| C-026 | V2 (= V1) | 65 | OWN | Same three pins, checked against `_check_rule` (V2:231); V3 defines no pins (V3:334) |
| C-027 | merge V1+V2+V3 | 75 | MERGE | Union: V1's output dir not writable (V1:256-267), V2's symlink and old git (V2:239-247), V3's input change and killed process (V3:347-358) |
| C-028 | merge V2+V1 | 70 | MERGE | V2's sha256 snapshot including `~/.claude/` (V2:97) plus V1's patched `Popen` / `os.system` outside the control test (V1:81) |
| C-029 | merge V1+V3 | 65 | CONCEDE | V1's injected `Budget` (V1:178) plus V3's remaining-time limit and byte limits (V3:124-125, V3:137) |
| C-030 | merge V1+V3 | 75 | CONCEDE | V1 folds LF to a space (V1:66); V2 removes it and joins words (V2:83); V3 neutralizes HTML (V3:317-318) |
| C-031 | V1 | 70 | CONCEDE | Keep the `.gitignore` line until reports are handled (V1:330); V2:310 orphans the reports |
| C-032 | V2 | 60 | OWN | Worst-case design, so the capture only confirms two flag forms (V2:291) |
| C-033 | V2 (= V1) | 60 | OWN | Copy the sections and cite `495eb96d` (V2:296, V1:311) |
| C-034 | V2 | 55 | OWN | After #422, otherwise a follow-up PR (V2:295) gives a concrete fallback |
| C-035 | V3 | 70 | CONCEDE | Unknown timestamps never idle; waits exempt from the window (V3:93, V3:234-237) |
| C-036 | V1 | 70 | CONCEDE | Ten dimensions, default `unknown` (V1:136); V2 leaves them out |
| C-037 | V2 | 70 | OWN | `rule` plus `evidence` naming the field and source (V2:139-141) |
| C-038 | merge V3+V2 | 70 | MERGE | V3's "next inspection" in Sessions (V3:303) plus V2's ledger column (V2:210), inspection steps only |
| C-039 | merge V1+V2 | 65 | MERGE | V1's static forbidden list (V1:71) plus V2's negative `worker-read` test (V2:99) |
| C-040 | V3 | 75 | CONCEDE | Symlink-safe `--output` with no overlap with input dirs (V3:156-157) |
| C-041 | merge V2+V3 | 65 | MERGE | V2's `resolve()` check and never `ccsession --list` (V2:64) plus V3's escaping-symlink rejection (V3:288-292) |
| C-042 | V2 (= V1) | 50 | OWN | Carry the citations without editing REPORT (V2:285); V3's label adds nothing testable |
| C-043 | V1 | 65 | CONCEDE | REPORT citations plus an extension-point column (V1:35-41); V1 includes all of V2's content here |

### Contradictions

| Point | Preferred | Conf | Tag | Evidence |
|---|---|---|---|---|
| X-001 | V2 (= V1) | 55 | OWN | Named exception (V2:57): disk sweep is safe and still useful; V3's exit 2 (V3:165-166) follows Seed:63 literally, so the owner must decide |
| X-002 | V1 (V3 wording) | 95 | CONCEDE | V2 rule 2 `consumer_fenced is not True` (V2:150) lets unknown through, against Seed:56 and V2's own FR-009 (V2:70) |
| X-003 | merge V1+V3 | 85 | CONCEDE | Seed:52 and Seed:88 forbid action output; V2's own V2:231 alternative already agrees |
| X-004 | V2 | 65 | OWN | Path walk removes the need for rev-parse; `log` is needed for C-013; V3's families cannot be tested against Seed:64 |
| X-005 | V2 (= V1) | 80 | OWN | One status call per worktree answers GQ-101 (V2:73); V3's base comparison has no argv (V3:284-285) |
| X-006 | V2 | 60 | OWN | Archive-blocked is unarchived work; block removal (V2:168); safety comes first (Seed:27) |
| X-007 | V1 | 90 | CONCEDE | V2's idle sits after "anything else" (V2:155-156): impossible as written |
| X-008 | V1 | 60 | CONCEDE | "Allowed, not required" (V1:245); V3's required schedule adds a duty Seed:36 does not ask for |
| X-009 | V1 / V3 | 70 | CONCEDE | `orca-ide` (V1:175, V3:267); V2 contradicts itself (V2:175 against V2:84); correct name UNVERIFIED |
| X-010 | V2 | 70 | OWN | Only a real-git run proves the lock is not taken (V2:98); V3:365 admits argv tests prove intent; isolate it as one marked test |
| X-011 | V2 (= V1) | 85 | OWN | Non-ready `task-list` is needed for gate policy (V2:189); V3 needs it but omits it (V3:202 against V3:266-271) |
| X-012 | V1 | 70 | CONCEDE | `class` (V1:234) is the schema-facing name; `cls` is a Python workaround |
| X-013 | V1 | 70 | CONCEDE | Keep the line (V1:330); V2 removes it while keeping the reports (V2:310-311) |
| X-014 | V2 (= V3) | 85 | OWN | Shift Brief present (V2:217); V1 claims it (V1:208) but omits it (V1:223-230) |
| X-015 | merge V3+V2 | 70 | MERGE | Seed:63 needs a next action per session: V3's Sessions column (V3:303) plus V2's ledger column (V2:210) |
| X-016 | V2 (= V1) | 75 | OWN | Seed:54 forbids live Orca in this work; record V3's concern (V3:403) as an UNVERIFIED risk for a later phase |
| X-017 | V2 (= V1) | 85 | OWN | "It is never posted" pin present (V2:228); V3 lacks it (V3:334) |
| X-018 | V3 (with V1) | 75 | CONCEDE | "Unreadable contract: unknown evidence, not finished" (V3:352); V2:154 labels unread rows finished |
| X-019 | V3 | 80 | CONCEDE | Suffix or a clean failure (V3:134, V3:181); V2:79 leaves an overwrite undefined |

## 9. Shared assumptions

| Point | Answer | Reason |
|---|---|---|
| A-001 | ACCEPT | A1 with two seams and one write is the shape every variant and Seed:33 share; deferred registration is stated at Seed:89 |
| A-002 | QUALIFY | The flag covers only `_git`; A-101 (Orca's own git) stays open, and the flag needs the version gate (V2:180) and a real-git control test (V2:98) |
| A-003 | QUALIFY | `run-current` JSON form and child-process visibility (A-102) are UNVERIFIED; the exit-2 message must name `--run` as the fix |
| A-004 | QUALIFY | Correct as a rule, but A-103 has no named source, so in Phase 1 live exited rows become could not determine with Orca's verdict kept in the note |
| A-005 | ACCEPT | Result read, report read and open PR are not observable (V1:169, V2:74, V3:253) |
| A-006 | QUALIFY | Rests on A-104, A-105 and A-106, all UNVERIFIED; an unjoinable transcript must be could not determine, never idle |
| A-007 | ACCEPT | Bounds come from REPORT (Seed:41); over-bound rows are visible as could not determine and counted as lower bounds (V3:114) |
| A-008 | QUALIFY | The path pattern is fine, but uniqueness per second is false (X-019); add V3's suffix (V3:181-187) |
| A-009 | ACCEPT | 0 / 1 / 2 is consistent across variants; that Click usage errors exit 2 is UNVERIFIED here (V2:313) |
| A-010 | QUALIFY | Escaping the pipe is necessary, but A-108 (viewer renders `\|`) is UNVERIFIED; LF must fold to a space (V1:66), not be removed |
| A-011 | ACCEPT | No non-consuming question read exists (Seed:74), so "partial" coverage is the honest label |
| A-012 | ACCEPT | Placement and gating follow Seed:67 and Seed:78 |
| A-013 | ACCEPT | Carrying the stale citations without editing REPORT matches Seed:79 |
| A-014 | ACCEPT | 6 h is fixed by the topic (Seed:77); waits must be exempt from the window (V3:93) |
| A-015 | ACCEPT | GQ-110 (Seed:64); one call per worktree also answers GQ-101 (X-005) |
| A-016 | ACCEPT | No mechanical caller check is possible without a new security model (Seed:54) |
| A-017 | QUALIFY | Seam mocks prove intent, not lock behaviour; one isolated real-git test in `tmp_path` (V2:98) is needed and launches no Orca, ccsession or Claude, so it stays within Seed:54 |
| A-101 | REJECT | Assuming this is not justified: it is UNVERIFIED and, if false, defeats the first safety item. Record it as a named risk, keep it out of the lock-free claim in WC-14, and test it in a later phase |
| A-102 | QUALIFY | UNVERIFIED; if the binding is not visible to the child, the skill must pass `--run` explicitly instead of relying on `run-current` |
| A-103 | REJECT | No allowlisted read is named as the source of `worker_done`, so rule 2 must default to could not determine until a source is captured |
| A-104 | QUALIFY | UNVERIFIED; read the file directly (never `ccsession --list`, V2:64) and treat a parse failure as could not determine |
| A-105 | QUALIFY | UNVERIFIED; a derivation miss must show as an unscanned source, not as "no sessions" |
| A-106 | QUALIFY | mtime is a proxy only; when it is missing or in the future the row is could not determine, never idle (V3:234-237) |
| A-107 | QUALIFY | UNVERIFIED; the design must degrade visibly (lower bounds, omission counts) rather than assume the bound is rarely hit |
| A-108 | QUALIFY | UNVERIFIED; the escaping test must check the rendered column count, not just the escaped bytes |

## 10. Tally

| Category | OWN (V2) | CONCEDE (V1, V3 or V1+V3) | MERGE (keeps a V2 part) | Total |
|---|---|---|---|---|
| Structural | 7 | 4 | 2 | 13 |
| Content | 14 | 18 | 11 | 43 |
| Contradictions | 9 | 9 | 1 | 19 |
| **All S/C/X** | **30** | **31** | **14** | **75** |

- Of the 30 OWN points, 11 are positions V2 shares with another variant: C-007, C-015, C-026, C-033, C-042, X-001, X-005, X-011, X-016 and X-017 with V1, and X-014 with V3. So V2 alone wins 19 points.
- Shared assumptions: 10 ACCEPT, 13 QUALIFY, 2 REJECT (A-101, A-103).
- The two strongest critiques:
  1. **V3 defers its exact git argv** to a design gate (V3:279-286), and its GQ-101 check needs a base-reading argv it never picks (V3:284-285). Seed:64's exact-allowlist test cannot pass, and the first safety item (GQ-103(1)) has no testable boundary.
  2. **V1 drops the Shift Brief it says it copies** (V1:208 against V1:223-230) and has no next-action column (V1:228), so it fails Seed:63. It also proves lock-freedom only from recorded argv (V1:81-82), with no real-git test and no git version gate.
