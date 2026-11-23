# Round 1 statement: Variant 2 advocate (sonnet:qa)

Persisted verbatim by the debate-orchestrator from the advocate's returned text.

**Position summary**

Variant 2 (QA) is the better coverage audit. It anchors its blocking claims to SPEC text the plan drops: the four-kind contract gate, T5's "cycle ends within the 15 s cycle budget", and T33. Variant 1 (R1) is the better design review. I verified R1-02 and R1-03 against source and they are real defects QA missed. After checking, I downgrade QA-03 and QA-04 to minor and narrow QA-08, QA-11 and QA-12.

**Steelman of Variant 1**

R1 found the defects that need reading source code, not just the SPEC. `_find_orca` at `install_user_setup.py:209` runs `subprocess.run([path, "skills", "list", "--json"], ... timeout=10 ...)`. That makes plan:23, "The only live Orca call is `worker-list --json ...`", false. It also means plan:105's T36 seam does not cover discovery. If discovery is not injectable, a fake-runner test on a machine without Orca returns `NOT AVAILABLE` and the fake runner never runs. Two candidates at 10 s each also cannot fit a 15 s cycle. R1-03 is also real. Plan:173 writes the snapshot "after each successful cycle", but SNAP:88 freezes `source.status` as "`OK`, `STALE` (older than 45 s), `ERROR` or `UNKNOWN`". As planned, `STALE` and `ERROR` can never be published. R1 also applies the severity definition more strictly than QA. It rates "unpinned detail with no wrong behaviour" as minor, where QA rated several of those as blocking.

**Strengths claimed**

1. QA-01 is unique. SPEC:215 says "Each data gate passes only on recorded, redacted samples of four kinds ... each pinned in a contract test. Without all four the gate stays closed." Plan:60 creates all four files. Plan:63-65 only checks that they exist and are redacted. The stale and contradictory files are consumed by no later task. Task 6 uses the success file, and Task 7 uses a fake clock. Task 5 (plan:86) checks missing fields by mutating the parsed success data, not by loading `worker_list_missing.json`.
2. QA-05 has the stronger evidence. SPEC:369 reads "T5: ... the cycle ends within the 15 s cycle budget". Plan:104 pins only "yields `FAILED (timeout)` and the child is killed". Plan:97 requires only `DEFAULT_TIMEOUT_S` below 15 and allows five calls. Plan:112 only reports overrun as "`cycle overran (Ns)`". Five calls just under the timeout give a cycle of about 70 s, which then reads as STALE (45 s).
3. QA-02 holds. SPEC:172 says the `empty` variant "must render `no observed items in this source window; not proof none exist`". SPEC:385 pins it as T33. Plan:75 builds the `empty` variant, but the plan's Task 8 test list (plan:126) omits T33. Neither string appears in plan:126, and plan:21 does not exclude it. R1 itself calls the text "required" in R1-06.
4. QA-07, QA-09 and QA-10 are accurate, cheap traceability catches. Plan:126 lists `cost unavailable` with no criterion. Plan:177 checks only option names. Plan:126 omits SPEC:355's `read k of N Runs since start`.

**Weaknesses identified in Variant 1**

1. R1-04 asks to "specify suppression or redaction" of `stage.detail` and `stage.activity`. SNAP:103 freezes those fields into the export, and plan:157 exports them. The fix would break the contract R1-03 defends. The real issue is that plan:25 says "printed", while plan:182 has the executor print a live ledger. That is a constraint-wording conflict, so minor.
2. R1-06 rates T33 minor, but the SPEC says "must render" (SPEC:172). That is a missing required deliverable by the severity definition.
3. R1-01 cites only plan:97 and never connects to SPEC T5 (SPEC:369).
4. R1 does not mention the four-kind gate (SPEC:215), T31, T45 or the unpinned T41 half. Seven findings leave much of the SPEC test list unexamined.
5. R1-02 slightly overstates. Reusing `_find_orca` with its probe is what SPEC:312 prescribes. The defect is plan:23's false "only" claim and the missing injection seam, not the reuse.

**Concessions**

- QA-04: plan:118 already says "A failed cycle keeps the previous snapshot readable". Only the shape-to-`FAILED (shape)` mapping and the two-envelope case are unpinned. Narrowed, minor.
- QA-08: plan:182 asserts `NOT AVAILABLE`, and plan:126 defines the STALE and FAILED strip cells. Plan:135 does cover the first half of T41 (baseline, no flags). Narrowed, minor.
- QA-11: plan:148 says "`STALE` and `unknown` appear as words in both", and plan:126 has a header `as of <HH:MM>`. Only the per-value `as of HH:MM:SS` qualifier is unbuilt. Narrowed, minor.
- QA-12: plan:33 gives the reason inline, "because switching to Textual changes the stack the owner confirmed". Owner-decisions item 5 supports it. The deviation half is rejected. Only the "spike criterion can pass on a recorded fail" point survives, as minor.
- QA-03 is over-rated. Plan:97 describes all three outcomes, so it is an unpinned detail, minor.
- I missed R1-02 and R1-03 entirely. I checked both and they are confirmed.

**Shared assumptions**

- A-001: QUALIFY. Plan:20-21 excludes R2, B, R3 and R4 items, so T7, T10-12, T19, T46, T47, T50 and T51 are rightly out. The R0/R1 tests that are not excluded (T31, T33, T45) are in scope per SPEC:222.
- A-002: QUALIFY. Owner-decisions line 9 leaves the gate "for the owner to say", SPEC:221 says "This gate has NOT passed", and I could read no file containing the 2026-11-10 message. The plan does disclose this at plan:22, but the authorization is unverifiable from files.
- A-003: REJECT. Plan:126 hides historical rows, while plan:157 says `export_text` has "every ledger row". SPEC:189 says historical rows are "never deleted from the snapshot". The plan does not pin which wins.
- A-004: QUALIFY. Plan:80 gives Task 5 `Depends on: Task 3` only, but plan:88 uses Task 4's variant. Sequential `/sc:implement` makes this harmless, but it breaks on reordering or per-task resume.

**X-001 and X-002**

- **X-001:** I hold T33 as blocking. Neither the instruction (plan:126) nor any criterion contains the empty-state strings, and the fixture built at plan:75 feeds no test.
- **X-002:** QUALIFY. Where the instruction describes the behaviour and only the criterion is missing, the item is minor. That is QA-03, QA-04, QA-07, R1-07 and QA-06. Where the instruction and the criterion are both absent and the SPEC names a gate or test, it is a missing deliverable and blocking. That is QA-01, QA-02 and QA-05. Under this rule R1-06 is blocking and QA-03 and QA-04 are minor.

**Per-finding table**

| id | holds? | severity | reason |
|---|---|---|---|
| R1-01 | confirmed | blocking | per-call timeouts do not bound the 15 s cycle (plan:97, SPEC:369) |
| R1-02 | confirmed | blocking | `_find_orca` (`install_user_setup.py:209`) is a live call that contradicts plan:23 and 105 |
| R1-03 | confirmed | blocking | plan:173 never publishes SNAP:88's `STALE` or `ERROR` |
| R1-04 | narrowed | minor | constraint wording versus the plan:182 live print; its fix breaks SNAP:103 |
| R1-05 | confirmed | minor | plan:80 omits Task 4, which plan:88 uses; numeric order hides it |
| R1-06 | confirmed gap | blocking | T33 text is neither built nor pinned (severity raised) |
| R1-07 | confirmed | minor | disclosure text is unpinned (SPEC:158) |
| QA-01 | confirmed | blocking | four-kind contract gate (SPEC:215) unpinned; missing kind is partly covered by the Task 5 mutation |
| QA-02 | confirmed | blocking | same as R1-06 |
| QA-03 | narrowed | minor | instruction at plan:97 describes the three outcomes (downgraded) |
| QA-04 | narrowed | minor | plan:118 covers snapshot retention; only the `FAILED (shape)` mapping is unpinned |
| QA-05 | confirmed | blocking | T5 "within the 15 s cycle budget" is not enforced or tested |
| QA-06 | confirmed | minor | long PARTIAL text and `(page k)` form are unbuilt |
| QA-07 | confirmed | minor | `cost unavailable` is named at plan:126 but unpinned |
| QA-08 | narrowed | minor | plan:182 and 126 cover NOT AVAILABLE and the strip cells; the rest holds |
| QA-09 | confirmed | minor | plan:177 checks option names only |
| QA-10 | confirmed | minor | `read k of N Runs` and T45 are neither built nor excluded |
| QA-11 | narrowed | minor | plan:148 renders STALE; only the per-value qualifier is missing |
| QA-12 | narrowed | minor | the deviation is reasoned at plan:33; only the non-failing spike criterion survives |

**Missed by both cards**

1. T16 (the scenario matrix and `x/y shown` arithmetic). SPEC:373 reads "T16: the scenario matrix {5, 8, 10 orchestrators} x {50, 80, 100 sessions} x {160, 116, 80 columns} (27 renders)". Plan:71 sizes `base` at "about 12 rows". No task cites T16 and the plan does not exclude it.
2. The `k duplicate rows ignored`, `order unknown` and `conflict (time went back)` texts. SPEC:375 (T22) requires `k duplicate rows ignored`. Plan:88 tests them only on the model, and plan:126 lists none of them as view output.
3. Export versus hidden rows (A-003). Plan:126 hides historical rows, plan:157 exports "every ledger row", and SPEC:189 says "never deleted from the snapshot". Which one `export_json(view)` follows is unpinned.
