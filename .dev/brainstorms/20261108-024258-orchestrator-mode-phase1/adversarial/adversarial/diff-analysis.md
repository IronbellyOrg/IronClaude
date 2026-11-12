# Diff Analysis: Requirements Specification Comparison (Orchestrator Mode Phase 1, #339)

## Metadata
- Generated: 2026-11-08 (date from session context; clock time UNVERIFIED)
- Variants compared: 3
  - V1 = `variant-1-opus-architect.md` (333 lines, opus, architect)
  - V2 = `variant-2-opus-analyzer.md` (313 lines, opus, analyzer)
  - V3 = `variant-3-haiku-backend.md` (431 lines, haiku, backend)
  - Seed = `../../seed-brief.md` (90 lines), used as the constraint and success-criteria baseline
- Total differences found: 133 points (S 13, C 43, X 19, U 33, A 25)
- Categories: structural (13), content (43), contradictions (19), unique (33), shared assumptions (25, of which 8 are promoted [SHARED-ASSUMPTION] points)
- Citation form: `V1:148` means line 148 of variant 1; `Seed:63` means line 63 of the seed brief. Every cited line was read in this step.
- Taxonomy: each point carries one level. L3 = state mechanics (state, guard, boundary, invariant, concurrency, race, validation rule, transition); L2 = architecture, API, component, module, interface, dependency, organization; L1 = naming, formatting, wording, style. Highest matching level is used.
- Scope note: no file under `qa/` was read; no REPORT, GAPS or code file was read in this step, so any claim a variant makes about those sources is reported as the variant's claim, not checked here (UNVERIFIED).

## Structural Differences

| # | Area | V1 (architect) | V2 (analyzer) | V3 (backend) | Severity | Level |
|---|------|----------------|---------------|--------------|----------|-------|
| S-001 | Header block | Field/Value table with Variant, Model, Persona, Emphasis, Date, Status (V1:3-10) | Bullet list Variant, Model, Persona, Date, Status (V2:3-7) | Four plain lines, no date (V3:3-6) | Low | L1 |
| S-002 | Top-level section order | 14 numbered sections: problem/scope, out of scope, FR, NFR, architecture, data model, seams, report, WC-14, failure modes, risks, GQ, open questions, rollback | 15 numbered sections: adds a separate "Problem and Root Cause" (V2:11) and splits Scope (V2:24) from Out of Scope (V2:35) | 12 unnumbered headings; no architecture section; adds "CLI contract and re-run idempotency" (V3:148); merges verification and rollback (V3:412) | Medium | L2 |
| S-003 | Requirement format | Tables `ID / Requirement / Acceptance criterion` (V1:49-75) | Bold bullets with inline `*AC:*`, grouped under Entry, Discovery, Classification, Report, Command subheadings (V2:54-93) | Two lines per item, `FR-NNN.` statement then `Acceptance:` (V3:56-114) | Low | L1 |
| S-004 | Requirement ID numbering | FR-001..FR-025, NFR-001..NFR-013 | FR-001..FR-026, NFR-001..NFR-009 | FR-001..FR-020, NFR-001..NFR-010 | Medium (same ID means different things: FR-001 is the CLI in V1/V2 but the git-lock gate in V3; a merge must renumber) | L1 |
| S-005 | Architecture section | Module table with Role / May import / Must not import, plus boundary rules B1-B5 and an extension-point table (V1:95-127) | Module table Owns / May import / Must not, plus data flow and rejected placements (V2:107-129) | No module table; modules named in prose only (V3:18-23) | Medium | L2 |
| S-006 | Data model hierarchy | Flat bullet list of typed frozen dataclasses, then rule table and package-state table (V1:129-169) | Numbered subsections 7.1 records, 7.2 classes, 7.3 package states (V2:131-168) | Prose "model groups" without field types, then numbered rule list (V3:189-254) | Medium | L2 |
| S-007 | Failure-mode table columns | Mode / Detection / Behaviour / Exit (V1:254-267) | # / Failure / Evidence it is real / Containment / Test (V2:237-247) | Failure / Required behavior (V3:345-358) | Low | L2 |
| S-008 | Risk presentation | Table with Likelihood (V1:271-281) | Table with Likelihood / impact (V2:253-263) | Unrated bullet list (V3:362-372) | Low | L1 |
| S-009 | GQ resolution layout | Table GQ / Resolution / Where (V1:287-300) | Table Gap / Root cause / Resolution (V2:271-285) | Prose lines (V3:376-394) | Low | L1 |
| S-010 | Open-question layout | Table, 9 rows, no IDs (V1:306-316) | Table, OQ-1..OQ-8 (V2:289-298) | 10 bullets, no IDs (V3:398-410) | Low | L1 |
| S-011 | Verification placement | Per-requirement AC only | Per-requirement AC only | Per-requirement AC plus a separate verification checklist (V3:414-423) | Low | L2 |
| S-012 | Evidence provenance statement | Exact line ranges read (V1:12) | Exact line ranges read, plus host `git --version` (V2:9) | Generic source list; states no code implementation was inspected (V3:25-34) | Medium | L2 |
| S-013 | WC-14 text presentation | Blockquote paragraph (V1:240) | Fenced Markdown block with heading (V2:225-229) | Wrapped prose lines, heading given separately (V3:322-336) | Low | L1 |

## Content Differences

### Classification states and precedence

| # | Topic | V1 Approach | V2 Approach | V3 Approach | Severity | Level |
|---|-------|-------------|-------------|-------------|----------|-------|
| C-001 | Shape of the precedence table | 8 named rules in `classify.RULES`; idle placed as rule 7 and an explicit `fallback` as rule 8, so the table is total (V1:145-156) | Rules 1-7 with rule 7 "anything else"; idle listed as a row after rule 7 (V2:147-156) | Rules 1-7 with rule 7 "everything else"; idle described in prose after the list, position unstated (V3:218-236) | High | L3 |
| C-002 | Rule 1 with unknown gate policy on a live row | Returns could not determine with a note (V1:147) | Unspecified; only the `ask the coordinator` skip is defined (V2:149) | "unknown policy stays unknown" (V3:220) | Medium | L3 |
| C-003 | Rule 2 (stalled proved) fencing input | Requires `fenced_evidence == "absent"`; `unreadable` gives could not determine (V1:148) | Requires `consumer_fenced is not True`, so `None` passes (V2:150) | Requires "known absent fencing"; unreadable defeats the rule (V3:221-222) | High | L3 |
| C-004 | Rule 6 finished and partial results | `partial` contract status gives note "partial: usable not yet judged" (V1:152) | Note "partial" when `read_ok` is false (V2:154) | Partial stays usable-not-yet-judged; "finished never means admitted" (V3:228-229) | Medium | L3 |
| C-005 | Ready-Task wording | "a ready Task (creator: could not determine)" (V1:150) | "a frozen or foreign ready Task" (V2:152) | "never label them definitively foreign"; "ownership review" (V3:226) | Low | L1 |
| C-006 | Package states, precedence and removal blocking | Six states: conflict, interrupted-archive, archive-blocked, unfinished, archived, unknown; archive-blocked does not block removal by itself (V1:158-167) | Five states, no `unknown`; states 1-4 (incl. archive-blocked) block removal (V2:160-168) | Four report values normal, archive-blocked, interrupted archive, conflict; unfinished is a separate blocker (V3:240-245) | High | L3 |
| C-007 | GQ-101 "active package" evidence | Changed or untracked path inside the package folder in that worktree's single status call (V1:65, V1:199) | Same: own `git status --porcelain` lists a path under the package (V2:73) | Package folder or ledger "differs from the fixed base reference", by plain-read comparison against a base tree (V3:246, V3:284-285) | High | L3 |
| C-008 | Orca allowlist contents | 6 templates incl. `task-list --run <run> --json` for the gate policy line; binary `orca-ide` (V1:175, V1:184-191) | 6 templates incl. `task-list --run`; binary `orca` (V2:175, V2:184-191) | 5 forms, no non-ready `task-list`; binary `orca-ide` (V3:266-271) | Medium | L3 |
| C-009 | Git allowlist | `status --porcelain --branch` plus `rev-parse --show-toplevel`; no log, branch, stash, worktree list (V1:197-202) | `status`, `log --format=%H --max-count=1 <branch>..HEAD`, `--version`; no rev-parse (V2:197-203) | `status` plus read families `rev-parse`, `log`, `branch` with exact args deferred to a design gate (V3:280-283) | High | L3 |
| C-010 | `_git` seam construction | Seam builds `git --no-optional-locks -C <path>` and sets `GIT_OPTIONAL_LOCKS=0` (V1:176) | Same, plus a git version gate that marks git sources unscanned if too old (V2:176-180) | "Every Git form starts `git --no-optional-locks -C <root>`"; argv shape validated before spawn; no env variable (V3:260-263, V3:279) | Medium | L3 |
| C-011 | Proof that the sweep takes no index lock | Recorded-argv test with flag at index 1, plus env test (V1:82) | Recorded-argv test plus a real-git control experiment in `tmp_path` (V2:98) | Recorded-argv check; negative fixtures fail before subprocess (V3:57) | Medium | L3 |
| C-012 | Default `--root` discovery | One `rev-parse --show-toplevel` call (V1:200) | Walk up to the first `.git` with plain reads, no git call (V2:203) | "defaults to the current Git top-level", method unstated (V3:154) | Low | L2 |
| C-013 | Unmerged commits | Not observed in Phase 1; acceptable because removable is never yes (V1:202) | One `git log` per child against the feature branch; root worktree is could not determine (V2:75) | Listed as a removal blocker; argv deferred (V3:251, V3:282) | Medium | L3 |
| C-014 | `worker-list` pagination | Cursor flag UNVERIFIED, added as one template after step 1.0a (V1:187) | Paged on `page.nextCursor`; a 101-row fixture asserts 2 list calls (V2:63) | Do not guess continuation flags; show partial coverage; deduplicate rows (V3:63, V3:274) | Medium | L3 |

### Orca-down behaviour, exit codes, JSON

| # | Topic | V1 Approach | V2 Approach | V3 Approach | Severity | Level |
|---|-------|-------------|-------------|-------------|----------|-------|
| C-015 | Orca unavailable | Banner, one `_orca` call, disk-only sweep, exit 0, with or without `--run` (V1:69, V1:256) | Same, stated as an explicit exception to the no-binding exit 2 (V2:57, V2:84) | Local-only report only when a Run was selected; no Run plus Orca down exits 2 (V3:165-166, V3:347) | High | L3 |
| C-016 | Exit-code meanings | 0 completed, 1 internal error incl. allowlist miss, 2 usage (V1:68) | Same (V2:82) | Same, plus "exit 0 means the report was successfully published" (V3:161-164) | Low | L2 |
| C-017 | Stdout JSON | Schema v1, ten keys, row key `class` plus `rule`; additive-only within v1, golden key-set test (V1:89, V1:234) | Same ten keys; row key `cls`, plus `rule`, `evidence`, `notes`, `safe_to_close` (V2:81) | Same ten keys; `waiting` holds stable IDs only; printed only after successful publication; zero counts included (V3:167-177) | Medium | L2 |

### Report format, path, re-run behaviour

| # | Topic | V1 Approach | V2 Approach | V3 Approach | Severity | Level |
|---|-------|-------------|-------------|-------------|----------|-------|
| C-018 | Report sections and order | Header, Waiting (a), Waiting (b), Retained problems, Sessions, Worktrees, Historical; no Shift Brief and no could-not-determine section (V1:223-230) | Header, Waiting (Attention Ledger), Could not determine, Stalled, Working/finished/fenced/idle, Worktrees, Retained problems, Historical, Shift Brief (V2:207-217) | Header, Source coverage, Ledger (a), Ledger (b), Retained problems, Sessions, Worktrees, Historical, Shift Brief, What I could not determine plus footer (V3:297-307) | High | L2 |
| C-019 | Report path and collisions | `<output>/<YYYYMMDD-HHMMSS>-sweep.md` UTC (V1:67, V1:210) | Same path (V2:79, V2:207) | Same base name plus a collision suffix, exclusive reservation, never overwrite, "Report complete" footer (V3:181-187) | Medium | L3 |
| C-020 | Re-run behaviour and idempotency | No explicit rule; determinism only (V1:85) | No explicit rule; R8 notes the self-observation loop without the ignore line (V2:262-265) | Dedicated section: no lifecycle change, no cursor advance, new file every run (V3:179-187) | Medium | L3 |
| C-021 | Determinism | Byte-identical report and JSON for same input and context (V1:85) | Byte-identical "apart from the header timestamp", fixed `now` in the AC (V2:102) | Byte-identical classifications and rendered text (V3:122) | Low | L3 |

### WC-14

| # | Topic | V1 Approach | V2 Approach | V3 Approach | Severity | Level |
|---|-------|-------------|-------------|-------------|----------|-------|
| C-022 | End condition of the loop | "every Task it created has settled and been admitted" (V1:240) | "settled and admitted, as shown by the Run's own task list" (V2:228) | "settled and every result has been inspected and its admission or rejection recorded" (V3:324-325) | Medium | L3 |
| C-023 | Sweep cadence | On every wake; scheduled sweep allowed, not required (V1:240, V1:245) | On every wake only (V2:228) | On every wake plus "keeps a periodic sweep scheduled while work remains"; 5 min recommended (V3:326-328, V3:405) | Medium | L3 |
| C-024 | Closing sentence on recommendations | "The sweep recommends none of these actions" (V1:240, V1:244) | "The sweep only recommends the stop-and-cancel step ..., worktree removal and a new Task" (V2:228); alternative kept ready (V2:231) | "The sweep recommends no stop, retry, release, merge or removal" (V3:335) | High | L2 |
| C-025 | Extra sentences | None beyond the step 1.17 draft | Adds the lock-free observer guarantee (V2:228) | Adds "Phase 1 adds this duty, not a scheduler" and "A missing heartbeat is absence, never death" (V3:328-329) | Low | L1 |
| C-026 | Contract-test pins | Three pin phrases, `NEVER_AS_WORKER` grows to 9, test rename (V1:248) | Same three pins, checked against `_check_rule` (V2:231) | No pin phrases defined; text lacks "it is never posted" (V3:334) | Medium | L1 |

### Failure modes, tests, safety detail

| # | Topic | V1 Approach | V2 Approach | V3 Approach | Severity | Level |
|---|-------|-------------|-------------|-------------|----------|-------|
| C-027 | Failure-mode coverage | 12 modes incl. output dir not writable, unknown schema field (V1:256-267) | 9 modes F1-F9 incl. symlink escape and old git (V2:239-247) | 12 modes incl. input change during read, duplicate Dispatch, process killed, remote host (V3:347-358) | Medium | L2 |
| C-028 | Read-only snapshot test | One added file; HOME and XDG inside the root; `subprocess.run`, `Popen`, `os.system` patched to raise (V1:81) | (path, size, mtime_ns, sha256) snapshot incl. fixture `~/.claude/`; real `git` allowed (V2:97, V2:100) | Hashes and metadata under root, HOME and XDG; real subprocess blocked (V3:119, V3:420) | Medium | L3 |
| C-029 | Call and time bounds | `Budget` object 50 / 10 s / 90 s injected into `collect` (V1:70, V1:178) | Same bounds; fake-clock test (V2:85, V2:101) | Same bounds; remaining time limits each call; byte limits on reads (V3:124-125, V3:137) | Low | L3 |
| C-030 | `sanitize()` | Strip ESC/CSI/OSC, C0/C1, CR, bidi; fold newline to space; escape pipe (V1:66) | Same, but LF is removed, not folded (V2:83) | Same plus neutralize Markdown HTML and no active links (V3:317-318) | Low | L3 |
| C-031 | Rollback | Revert as one unit; keep `.gitignore` line until reports are dealt with (V1:320-333) | Delete and revert; remove the `.gitignore` line; re-run install (V2:302-313) | Revert ignore line only after deciding where reports go; never remove `.dev/tasks/` (V3:425-431) | Low | L2 |

### Open-question answers and remaining topics

| # | Topic | V1 Approach | V2 Approach | V3 Approach | Severity | Level |
|---|-------|-------------|-------------|-------------|----------|-------|
| C-032 | GQ-01 answer | Design list plus show now; capture before step 1.2 (V1:308) | Worst-case design; capture only confirms two flag forms (V2:291) | List plus show at 50; captured fixtures required before release (V3:398-399) | Low | L2 |
| C-033 | #409 layout answer | Copy sections and cite `495eb96d` (V1:311) | Same (V2:296) | Use this spec's section contract; #409 commit status UNVERIFIED (V3:372, V3:407) | Low | L1 |
| C-034 | PR #422 sequencing | New files first; contract edits after #422 (V1:313) | Same, else a follow-up PR (V2:295) | Verify overlap; "do not silently omit WC-14 from done" (V3:371, V3:406) | Low | L2 |
| C-035 | Person-started and Historical | Unjoined transcript; outside window goes to Historical (V1:60) | Same, last activity = transcript mtime (V2:65) | Same, readable required; unknown timestamps never idle; open Tasks and waits exempt from window (V3:93, V3:234-237) | Low | L3 |
| C-036 | Ten #409 dimensions | Ten dimensions on every row, default `unknown` (V1:136) | Not mentioned | Ten dimensions named and kept independent (V3:211-212) | Medium | L2 |
| C-037 | Per-row provenance | `rule` name in JSON and report (V1:139) | `rule` plus `evidence` naming field and source, shown in the ledger (V2:139-141) | Source identity, time and reason on every observation (V3:192) | Low | L2 |
| C-038 | "Next action" in the report | No next-action column; no action controls (V1:228, V1:232) | "what to check next" column plus proposals as text (V2:86, V2:210) | "next inspection" in Sessions; inspection-only steps (V3:303, V3:316) | Medium | L2 |
| C-039 | Forbidden-verb test | Static test against a fixed forbidden list (V1:71) | Negative test with `worker-read` (V2:99) | Negative fixtures, unknown verb is exit 1 (V3:263) | Low | L3 |
| C-040 | `--output` validation | Outside `<root>/.dev/` is a usage error (V1:54) | Same (V2:59) | Same, including through symlinks, and no overlap with input dirs (V3:156-157) | Low | L3 |
| C-041 | Disk discovery scope | Lists the read targets; no symlink rule (V1:204) | Fixed patterns, no recursive walk, `resolve()` check, never `ccsession --list` (V2:64) | Fixed patterns, reject escaping symlinks, ccsession files read directly (V3:288-292) | Low | L3 |
| C-042 | GQ-111 to GQ-113 framing | Stale citations carried, not fixed (V1:302) | Same (V2:285) | GQ-111/112 called "documentation debt" (V3:390-394) | Low | L1 |
| C-043 | Later-phase blockers | REPORT-line citations plus an extension-point column (V1:35-41) | REPORT-line citations (V2:39-46) | Generic blockers without REPORT citations, for example Phase 5 "explicit parent-child authority" (V3:38-44) | Low | L2 |

## Contradictions

Only falsifiable opposing claims, requirement-constraint conflicts and impossible sequences are listed.

| # | Point of Conflict | V1 Position | V2 Position | V3 Position | Impact | Level |
|---|-------------------|-------------|-------------|-------------|--------|-------|
| X-001 | Exit code when Orca is down and no `--run` is given | Exit 0, disk-only report; the test records exactly one `_orca` argv (V1:69, V1:256) | Exit 0, named exception to the no-binding exit 2 (V2:57, V2:84) | Exit 2, "binding cannot be established" (V3:165-166) | High: the same input gives 0 in two specs and 2 in one; Seed:63 says only "no `--run` and no `run-current` binding exits 2", which V3 reads literally | L3 |
| X-002 | Stalled (proved) with unknown fencing evidence | Not allowed: `unreadable` gives could not determine (V1:148, V1:59) | Allowed: rule 2 fires on `consumer_fenced is not True`, so `None` passes; rule 3's "fenced evidence not readable" path comes after rule 2 and cannot catch it (V2:150-151) | Not allowed: "Unreadable fencing/completion evidence defeats this rule" (V3:222) | High: V2 can label a live sweep row stalled without proof, against Seed:56 and V2's own FR-009 AC (V2:70) | L3 |
| X-003 | Whether the sweep or report recommends actions | "recommends none" (V1:240, V1:244) | Recommends stop-and-cancel, removal and a new Task as text (V2:228, V2:86, V2:294) | "recommends no stop, retry, release, merge or removal"; fixtures must contain none (V3:105, V3:335) | High: V2's FR-022 output fails V3's FR-017 AC | L2 |
| X-004 | Git verbs allowed | `rev-parse` allowed; `git log` and `git branch` forbidden (V1:200-202) | `git log` allowed; `rev-parse` forbidden (V2:200-203) | `rev-parse`, `log`, `branch` families allowed (V3:281) | High: the exact-allowlist test (Seed:64) cannot pass for all three; each forbids a verb another needs | L3 |
| X-005 | Does one status call answer GQ-101? | Yes, status alone gives active-package paths (V1:199) | Yes (V2:73) | No, needs a plain-read comparison against a fixed base tree and a base-reading argv not yet chosen (V3:246, V3:284-285) | Medium | L3 |
| X-006 | Does `archive-blocked` block worktree removal? | No by itself (V1:164) | Yes, states 1-4 block (V2:168) | Not in the blocker list; the list also omits interrupted archive (V3:251) | Medium | L3 |
| X-007 | Reachability of idle | Idle is rule 7, before the fallback, so it can fire (V1:153-154) | Idle is listed after rule 7 "anything else" under "first matching rule wins" (V2:145, V2:155-156): impossible sequence, idle is unreachable as written, yet FR-003's AC expects idle (V2:58) | Position unstated (V3:230-234) | Medium | L3 |
| X-008 | Is a periodic sweep required by WC-14? | "allowed by this text but not required" (V1:245, V1:314) | Not required; wake only (V2:228) | Required: "keeps a periodic sweep scheduled while work remains" (V3:327) | Medium | L3 |
| X-009 | Orca executable name in argv | `orca-ide` (V1:175) | `orca` (V2:175), while V2 also says "a missing `orca-ide` binary" (V2:84) | `orca-ide` (V3:267) | Medium: exact-argv tests differ; which name is correct is UNVERIFIED here | L2 |
| X-010 | Real git in tests | All real subprocess entry points patched to raise (V1:81, V1:93) | Real git in `tmp_path` for the control experiment; `subprocess.run` allows `git` (V2:98, V2:100) | Real subprocess entry points blocked (V3:119) | Medium: V2's NFR-002 test cannot exist under V1/V3's rule | L2 |
| X-011 | Non-ready `task-list --run <id> --json` | Allowed, source of the gate policy line (V1:190) | Allowed (V2:189) | Absent from the closed forms (V3:266-271), yet V3 needs blocked-gate policy (V3:202) | Medium | L3 |
| X-012 | JSON row key for the class | `class` (V1:234) | `cls` (V2:81) | Not named (V3:176) | Low | L1 |
| X-013 | `.gitignore` line on rollback | Keep until existing reports are dealt with (V1:330) | Remove the line (V2:310), while keeping reports (V2:311) | Revert only after deciding where reports go (V3:427) | Low | L2 |
| X-014 | Shift Brief section | Claims to copy header, Attention Ledger and Shift Brief (V1:208) but the section list has no Shift Brief (V1:223-230) | Included (V2:217) | Included (V3:306) | Medium: V1 conflicts with itself and with Seed:44 and Seed:88 | L2 |
| X-015 | Report lists "next action" per session | Sessions row holds dimensions, class, rule, safe-to-close, notes; no next-action column (V1:228) | "what to check next" in the ledger only (V2:210); other tables' columns unspecified (UNVERIFIED whether covered) | "next inspection" in Sessions (V3:303) | Medium: Seed:63 requires class, waiting-on and next action for every session | L2 |
| X-016 | Live check before release | None | None | Requires a "separately authorized disposable-Run check before release" (V3:403, V3:421) | Medium: conflicts with Seed:54 "no live Orca ... launch in tests or in this work" if the release is part of this work | L2 |
| X-017 | WC-14 pin phrase "it is never posted" | Present (V1:240, V1:248) | Present (V2:228, V2:231) | Absent: "Reports are dated local files, never posted" (V3:334) | Low: V3 text fails the V1/V2 pin set | L1 |
| X-018 | Settled row with guard-refused body and unreadable contract | Finished needs a parsed contract or a `guard refused:` body (V1:152) | Finished with note "partial" when `read_ok` is false (V2:154) | "Unreadable contract or transcript: Unknown evidence, not finished" (V3:352) | Low | L3 |
| X-019 | Two sweeps in the same second | Exact path `<YYYYMMDD-HHMMSS>-sweep.md`; AC checks "the dated path" (V1:67) | Exact path, "and nothing else" (V2:79) | Must produce separate files via a suffix or fail cleanly (V3:134, V3:181) | Low: V3's suffix breaks V1/V2's exact-path AC; V1/V2 leave overwrite behaviour unspecified | L3 |

## Unique Contributions

| # | Variant | Contribution | Value Assessment | Level |
|---|---------|-------------|-----------------|-------|
| U-001 | V1 | Extension-point table (rule table, read allowlist, sources, JSON) and a per-phase "extension point it will use" column (V1:35-41, V1:120-127) | Medium | L2 |
| U-002 | V1 | One-way dependency rule `commands -> {probes, classify, report} -> models` pinned by an AST import test (V1:114) | Medium | L2 |
| U-003 | V1 | Rule order pinned by name: test asserts `[r.name for r in RULES]` (V1:90) | Medium | L3 |
| U-004 | V1 | Read/write split: sweep package never holds a write verb; static test on `ALLOWED_ORCA` against a fixed forbidden list; Phase 2 gets its own seam and must re-collect (V1:71, V1:116) | High | L3 |
| U-005 | V1 | JSON additive-only within `schema_version: 1`, golden key-set test (V1:89) | Medium | L2 |
| U-006 | V1 | Renderer as a `SECTIONS` tuple of pure functions (V1:208) | Low | L2 |
| U-007 | V1 | Rename `test_never_as_worker_list_names_all_seven_commands` to a count-free name (V1:248) | Low | L1 |
| U-008 | V1 | Explicit could-not-determine result when gate policy is unreadable on a live blocked row (V1:147) | Medium | L3 |
| U-009 | V1 | `Budget` object passed into `collect`, never global, so tests set bounds per case (V1:178) | Low | L2 |
| U-010 | V1 | `unknown` package state for an unreadable ledger (V1:167) | Low | L3 |
| U-011 | V2 | Real-git control experiment proving the index is not rewritten, skipped as inconclusive if the control shows no rewrite (V2:98) | High | L3 |
| U-012 | V2 | Git version gate: older git makes every git source `unscanned: git too old` (V2:180) | Medium | L3 |
| U-013 | V2 | WC-14 sentence stating the lock-free guarantee (V2:228) | Medium | L1 |
| U-014 | V2 | Root-cause note: without the ignore line the sweep flags its own previous report as uncommitted (V2:262-265) | Medium | L2 |
| U-015 | V2 | Negative `git check-ignore` AC proving `.dev/tasks/` is not ignored (V2:93) | High | L3 |
| U-016 | V2 | Could-not-determine section placed before working rows because an unknown can hide a person-wait (V2:211) | Medium | L2 |
| U-017 | V2 | Unmerged-commit read via one bounded `git log` against the feature branch (V2:75) | Medium | L3 |
| U-018 | V2 | `--root` found by a plain path walk, no git call (V2:203) | Low | L2 |
| U-019 | V2 | No-new-dependency NFR; `yaml.safe_load` on the existing `pyyaml` (V2:64, V2:105) | Low | L2 |
| U-020 | V2 | Exact registration anchor in `cli/main.py` (V2:56; line numbers are the variant's claim, UNVERIFIED here) | Low | L2 |
| U-021 | V2 | Two-part root cause: no observation point plus no coordinator duty (V2:15-20) | Low | L1 |
| U-022 | V3 | Re-run idempotency contract: collision suffix, exclusive path reservation, never overwrite, no success JSON after failed write, "Report complete" footer (V3:179-187) | High | L3 |
| U-023 | V3 | Byte limits: 1 MiB contract/ledger, 256 KiB transcript tail, 8 MiB subprocess output (V3:137) | Medium | L3 |
| U-024 | V3 | Owner-only file mode for reports; no wholesale transcript copy (V3:143) | Medium | L3 |
| U-025 | V3 | Diagnostics carry stable reason codes and omit command output bodies (V3:146) | Low | L2 |
| U-026 | V3 | Duplicate Dispatch with contradictory state kept as one identity with a conflict reason; one plain re-read on input change (V3:196-197, V3:353-354) | Medium | L3 |
| U-027 | V3 | Unknown totals shown as lower bounds; visible, historical and omitted counts must reconcile (V3:114, V3:309) | Medium | L3 |
| U-028 | V3 | Open Tasks, explicit waits and unread-report candidates exempt from the activity window (V3:93, V3:237) | Medium | L3 |
| U-029 | V3 | Runtime non-consumption kept UNVERIFIED until a live release gate (V3:403, V3:421); see X-016 | Medium | L3 |
| U-030 | V3 | `--output` must not overlap input package or transcript dirs (V3:157) | Low | L3 |
| U-031 | V3 | Neutralize Markdown HTML; no active links from untrusted text (V3:317-318) | Low | L3 |
| U-032 | V3 | Header records the collection interval; the report is "not an atomic runtime snapshot" (V3:15, V3:197, V3:298) | Medium | L3 |
| U-033 | V3 | Rule-1 skip under `ask the coordinator` also applies to blocked-contract branches in rule 4, without erasing explicit waits (V3:225) | Low | L3 |

## Shared Assumptions

Agreement points held by all three variants. Precondition classes: STATED = the seed brief or at least one variant states it with a source; UNSTATED = no input states it; CONTRADICTED = an input states the opposite. Each UNSTATED precondition is promoted below to a synthetic diff point (A-101 onward) marked [SHARED-ASSUMPTION].

| # | Agreement point | Preconditions (class) | Level |
|---|-----------------|-----------------------|-------|
| A-001 | Option A1: Python CLI with pure `classify`, `probes` holding the only two seams, `report` as the only write, thin command and skill (V1:95-108, V2:107-120, V3:18-22) | Deferred Click registration in `cli/main.py` works (STATED, Seed:89); the skill can reach the CLI from PATH or `uv run` (STATED, V1:72, V2:90) | L2 |
| A-002 | Every `_git` argv carries `--no-optional-locks`, which stops the sweep taking `index.lock` (V1:176, V2:176, V3:279) | Installed git supports the flag (STATED, V2:180 only); disk readers never call git (STATED, V1:204); Orca's own read verbs do not run lock-taking git in worker worktrees (UNSTATED, promoted A-101) | L3 |
| A-003 | Run scope is `--run` or `run-current`; no `run-list` (V1:52, V2:57, V3:60) | `run-current` JSON form (STATED as UNVERIFIED, V2:186, V3:272); the binding is visible to the CLI subprocess started from the skill's Bash call (UNSTATED, promoted A-102) | L3 |
| A-004 | Could not determine is its own class; only Orca's `exited` proof yields stalled (V1:58, V2:70, V3:230) | WC-10 makes `exited` the only proof (STATED, Seed:45); Phase 1 cannot read fenced evidence on live rows (STATED, V1:134); some read reveals whether `worker_done` was sent (UNSTATED source, promoted A-103) | L3 |
| A-005 | Safe-to-close is two REVIEW values and never `yes` in Phase 1 (V1:62, V2:74, V3:253-254) | Result read, report read and open PR are not observable (STATED, V1:169, V2:74, V3:253) | L3 |
| A-006 | Person-started = transcript joined by the ccsession tab map to no Orca row; older ones go to Historical (V1:60, V2:65, V3:66) | Tab map readable as a file without the ccsession CLI and in a stable format (UNSTATED, promoted A-104; V3:288 only notes the CLI can migrate names); transcript project key derivable from the worktree path (UNSTATED, promoted A-105); transcript mtime marks last activity (UNSTATED, promoted A-106) | L3 |
| A-007 | Bounds 50 `worker-show`, 10 s per call, 90 s total; over-bound rows are could not determine (V1:70, V2:85, V3:124) | Bounds come from REPORT (STATED, Seed:41); a typical Run fits within 50 rows so most reports are complete (UNSTATED, promoted A-107) | L3 |
| A-008 | Report at `<root>/.dev/sweeps/<YYYYMMDD-HHMMSS>-sweep.md`, ignored by git (V1:67, V2:79, V3:181) | `.dev/sweeps/` in `.gitignore` (STATED, Seed:66); second-resolution names are unique per sweep (CONTRADICTED by V3:134; see X-019) | L3 |
| A-009 | Exit codes 0 / 1 / 2, allowlist miss is 1 (V1:68, V2:82, V3:161-164) | Click usage errors exit 2 (STATED as an assumption, V2:313) | L2 |
| A-010 | `sanitize()` strips controls and escapes the pipe (V1:66, V2:83, V3:317) | The Markdown viewer honours `\|` inside table cells (UNSTATED, promoted A-108) | L3 |
| A-011 | "Messages coverage: partial"; non-null `agentWait` and blocked contracts stand in for questions (V1:221, V2:209, V3:312) | No non-consuming question read exists (STATED, Seed:74) | L3 |
| A-012 | WC-14 after the fan-in rule; `/sc:sweep` on the never-as-worker list and outside unattended commands; gated on owner approval and PR #422 (V1:238-248, V2:223-231, V3:338-341) | Owner GQ-11 answer and #422 order (STATED, Seed:78) | L2 |
| A-013 | GQ-111 to GQ-113 carried without editing REPORT; cite GAPS line 138 counts (V1:302, V2:285, V3:390-394) | Counts 113 / 88 / 25 (STATED, Seed:79) | L1 |
| A-014 | Default window 6 h, `--window <N>h\|<N>d` positive integers (V1:53, V2:58, V3:153) | Topic fixes 6 h (STATED, Seed:77) | L3 |
| A-015 | Exactly one `git status --porcelain --branch` per worktree (V1:199, V2:75, V3:96) | GQ-110 (STATED, Seed:64) | L3 |
| A-016 | Coordinator-only is a contract rule, not a mechanical caller check (V1:246, V2:48, V3:339-340) | Workers follow the never-as-worker list (STATED, Seed:53) | L2 |
| A-017 | All tests mock the two seams; no live Orca, ccsession or Claude (V1:93, V2:100, V3:414-415) | Seam mocks cover every behaviour (STATED, Seed:59) | L2 |

### Promoted [SHARED-ASSUMPTION] diff points

| # | Assumption | Why it matters | Level |
|---|-----------|----------------|-------|
| A-101 | [SHARED-ASSUMPTION] Orca read verbs (`worktree ps`, `worker-show`) do not themselves run a plain `git status` in worker worktrees | If they do, the sweep can still take `index.lock` through Orca and trigger WC-9, and `--no-optional-locks` on `_git` does not prevent it | L3 |
| A-102 | [SHARED-ASSUMPTION] The `run-current` binding is visible to a child process started by the skill's Bash tool | If the binding is per-terminal or per-session, every skill-run sweep exits 2 | L3 |
| A-103 | [SHARED-ASSUMPTION] Some allowlisted read shows whether `worker_done` was sent | Rule 2 needs a positive "absent" value; without a source every exited row is could not determine | L3 |
| A-104 | [SHARED-ASSUMPTION] The ccsession tab map is a readable file with a stable format | Person-started detection and the Orca join depend on it | L3 |
| A-105 | [SHARED-ASSUMPTION] The transcript project key can be derived from each worktree path | Without it the sweep cannot find the transcripts that belong to the tree | L3 |
| A-106 | [SHARED-ASSUMPTION] Transcript mtime reflects last session activity | The window boundary for idle and Historical uses it | L3 |
| A-107 | [SHARED-ASSUMPTION] Typical Runs have 50 or fewer rows | Above 50, rows become could not determine and the success metric (Seed:47) degrades | L3 |
| A-108 | [SHARED-ASSUMPTION] The report viewer renders `\|` as a literal pipe inside a table cell | If not, GQ-107's fix still breaks table columns | L3 |

## Summary
- Total structural differences: 13
- Total content differences: 43
- Total contradictions: 19
- Total unique contributions: 33
- Total shared assumptions: 25 (17 agreement points plus 8 promoted [SHARED-ASSUMPTION] points)

| Category | Count | L3 | L2 | L1 |
|---|---|---|---|---|
| Structural (S) | 13 | 0 | 6 | 7 |
| Content (C) | 43 | 25 | 13 | 5 |
| Contradictions (X) | 19 | 10 | 7 | 2 |
| Unique (U) | 33 | 19 | 11 | 3 |
| Shared assumptions (A) | 25 | 19 | 5 | 1 |
| **All points** | **133** | **73** | **42** | **18** |

- **Convergence denominator (S + C + X + A): 13 + 43 + 19 + 25 = 100.** Unique contributions are not diff points and are excluded.
- **Substantially identical?** No. The variants differ by well over 10%: 19 contradictions, 33 single-variant ideas, and 3 of the 4 safety-critical topics (allowlist, Orca-down exit, stall rule) disagree.
- Highest-severity items:
  1. X-002: V2 rule 2 allows stalled (proved) when fencing evidence is unknown, against Seed:56 and V1/V3.
  2. X-001: Orca down with no `--run` exits 0 in V1/V2 and 2 in V3.
  3. X-004: the three git allowlists are mutually exclusive (`rev-parse` vs `log`), so no single exact-allowlist test fits all.
  4. X-003: V2's WC-14 lets the sweep recommend stop, removal and a new Task; V1 and V3 forbid any recommendation.
  5. C-018 / X-014: report section order differs in all three; V1 drops the Shift Brief it claims to copy.
  6. C-006 / X-006: package-state sets and whether `archive-blocked` blocks removal differ.
  7. C-007 / X-005: V3 needs a fixed-base comparison for GQ-101; V1 and V2 use the one status call.
