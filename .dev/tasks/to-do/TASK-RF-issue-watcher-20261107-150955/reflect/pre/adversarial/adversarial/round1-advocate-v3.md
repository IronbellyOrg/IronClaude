## Advocate: Variant 3 (opus:refactorer)

Abbreviations: TF = `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md`; D = `docs/designs/issue-watcher.md`; R06 = `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/research/06-gap-fill-decisions.md`; RSK = `src/superclaude/skills/sc-reflect-protocol/SKILL.md`. Every TF line cited below was re-read for this statement (read-only); no command other than read-only `sed`/`grep` was run, and lint was NOT run.

### Position Summary

Variant 3 is the most accurate card on blocking defects. It found the two defects that no later item in the plan can catch: the POST-reflect `--remediate` step (TF:864-866), which sits after every gate and the only commit, and the full-tree lint rule (TF:699/702 against TF:735/745), which cannot pass as written. Every one of its 20 citations still matches the task file. I concede that Variant 2's two coverage gaps (R2-001, R2-002) are real, that Variant 3 wrongly marked INF-146 and INF-138 as covered, and that R3-001's mechanism has to be narrowed: the reflect skill never edits source itself, so the risk comes from the runner being told to "apply" the remediation task the skill writes.

### Steelman: Variant 1

Variant 1 (analyzer, sonnet) checked more than 12 external claims against real repo files (install_user_setup.py, main.py, atomic.py, test.yml:29, .pre-commit-config.yaml), so its findings about the outside world are the best grounded of the three. It found the same POST-reflect hazard independently (R1-002, TF:864/875), which corroborates X-001. It is the only card that raised the withdrawn-commit argument gap (R1-003), the "exactly as test.yml:29" mechanism mismatch (R1-004, confirmed: `.github/workflows/test.yml:29` is `uv pip install -e ".[dev]" "pytest-xdist>=3.5,<4"`, while TF:611 uses `uv run --offline --with`), and the G-10 staged-change blind spot (R1-005, TF:723). It reports its reading limits openly (variant-1:155).

### Steelman: Variant 2

Variant 2 (qa, haiku) is the only card that tracks each AC-1..AC-25 through its implementation, test-writing and test-running items (variant-2:36-62), and it lists all 19 named test files (variant-2:121-141). Both of its findings hold on reading:
- R2-001: Step 6.2 requires that "a lost label, a voided approval or a changed Project status gives `revalidation_failed`" (TF:460). Step 6.7 tests only a closed issue, assignee changes, a timeout and a refused reserved call (TF:475). A grep of TF:475 for "label", "voided" and "Project status" finds none of the three revocation cases.
- R2-002: TF:460 implements "a failing save giving exit 6 `state_dir_unwritable` through `audit.stderr_fallback`", but Step 6.6 (TF:472) never injects an append failure or a save failure into `run_cycle`. The only fallback test is at the CLI level (TF:508).

Variant 2 also states the right principle: "Lexical matches were not accepted as proof" (variant-2:66).

### Key Strengths Claimed

1. **X-001 / R3-001 sits after every gate.** Step 10.6 passes `--mode post --remediate --diff <BASE SHA>..HEAD` (TF:864). Its item 3 says "apply the remediations the skill offers under `--remediate`" (TF:866). Step 10.7 then stages only `.dev/tasks`, with "no second commit" (TF:875), and R06:30 declares only that staging ("staging only; no second commit"). It does not declare `--remediate`; a grep of R06 for "remediat" returns nothing.
   - **Narrowed mechanism:** with `--depth deep`, the skill takes the MDTM route: "`task-builder` builds the MDTM task file; the user runs `/task <path>`" (RSK:321), and "reflect AUTHORS but NEVER runs `/task` or `/sc:implement`" (RSK:324). Acceptance is "interactive" or headless `--print` (RSK:324), and a `bypassPermissions` subagent is neither.
   - **Why it is still blocking:** item 3 can then only be read two ways. (a) The runner executes the authored task, editing source after the only commit with no G-1..G-11 re-run, and Step 10.7 marks Done. (b) The instruction cannot be executed as written. Either reading is blocking under the brief, and no lens, gate or verifier runs after Step 10.6.
2. **X-008 / R3-002: the lint gate has no passing path.** Step 9.7 requires "ensuring exit 0; a finding in a file this task did not touch (the local `uv run ruff` is not the pinned 0.15.20) is recorded and NOT fixed" (TF:699). Step 9.8 says the same (TF:702). Step 9.19 requires that "every row is PASS (a FAIL is fixed and its step re-run" (TF:735), and the Final gate agent counts "Any command that fails" as a finding (TF:745).
   - The parenthetical at TF:699 shows the plan's author expected findings in untouched files, because DF-09 records that bare `uv run ruff` resolves to 0.17.3 (R06, row DF-09). `make lint` runs `uv run ruff check .` (Makefile:49).
   - One such finding leaves the gate with no way to pass and no HALT rule. That is a deadlock, and no later in-plan lens can fix it, because the gate rule itself is the defect.
3. **Citations hold.** All 20 Variant 3 citations were re-read and match: TF:330, 336, 384, 502, 520, 690, 699, 702, 735, 742, 745, 757, 778, 800, 864, 866 and 875; D:239 and D:791; Makefile lint (one line off: the command is at Makefile:49, under the `lint:` target at :47). Variant 3's T-2 note, "the attempts < 3 check is applied in run_cycle", is verified by TF:460: "a `failed` entry past backoff with attempts below 3".
4. **Its automatic-mapping corrections (X-009) are right.** They are corroborated independently by Variant 2's test-file table: INF-108 maps to 5.6-5.8, 6.9 and 8.2-8.8, and INF-153 maps to 8.6 (variant-2:129-141).
5. **Severity rule applied consistently.** A defect that an in-plan guard will catch later is minor; a defect downstream of every guard, or inside a gate's own pass rule, is blocking. This one rule separates X-001 and X-008 (blocking) from R1-001, R2-001 and R2-002 (minor, because the Final test-adequacy lens at TF:757 is told to flag "missing negative and boundary cases" for every "rule, table row, transition, reason, exit code").

### Weaknesses in Variant 1

- It rates R1-002 as only minor, although by its own account nothing re-gates the tree before Done ("No item re-runs G-1 to G-11 after remediation"). Its fix (variant-1:35) would add a HALT, which is a blocking-class remedy.
- Its claim "Gate commands executable as written" (variant-1:144) misses the TF:699/735 contradiction. It also did not read the Final gate items TF:737-837 (variant-1:155), which is exactly where the TF:745 no-carve-out rule sits.
- R1-001 is real but very small. `fail` abandons the entry at attempts 3 (TF:336), and `run_cycle` already applies "attempts below 3" (TF:460), so a `backoff_elapsed` without the conjunct behaves the same on every reachable state.
- R1-003 is partly a declared deviation. TF:848 points to OQ-51 for the working-tree case, so only the argument-text gap is left.

### Weaknesses in Variant 2

- It did not use the requested YAML format and used a non-binary MEDIUM severity (variant-2:1, :16), which makes it harder to merge.
- It cleared X-001 with "The checkpoint sequence captures BASE before the single commit" (variant-2:153). That is true, but it does not answer the question: the hazard is what happens after the commit, at TF:866/875.
- It judged INF-124 covered (variant-2:85) without noticing that the exit-0 rule contradicts the rule for untouched files (TF:699).
- It labelled pre-execution plan gaps "Drift", a post-execution category, which is the wrong vocabulary for a plan review.

### Concessions

1. R2-001 and R2-002 are valid. Variant 3 marked INF-138 "covered" and INF-146 "covered" (variant-3:200-235), and both should be partially_covered.
2. R3-001 overstated the mechanism: the skill does not edit source itself (RSK:324). The defect stands only through the runner's "apply" instruction at TF:866.
3. R3-002 depends on at least one lint finding in an untouched file existing. I did not run `make lint`, so this is inferred from TF:699 and DF-09, not observed.
4. R3-005 is partly disclosed in OQ-46 (TF:968: "who parses the store's own timestamps (`predicates.parse_utc` and `format_utc`)"). It is still not recorded as a departure from D:239.
5. R3-006 follows the design itself (D:791, "read through the dual surface"), so the conflict is with the lens rule, not with the design. Minor.
6. Variant 3 did not read the Gate D items or the bodies of 9.M4-9.M13 (variant-3:306).
7. The Makefile citation is one line off (:50 instead of :49).

### Shared Assumption Responses

- **A-001: ACCEPT.** I re-read about 25 cited lines (TF:330-875, D:239/479/791/879/887, R06:30, test.yml:29). Every excerpt exists at its cited line.
- **A-002: QUALIFY.** The skill never edits source; it only authors a corrective task file (RSK:321, :324). But TF:866 tells the runner to "apply the remediations", and the only way to apply them is a nested `/task` run, which would edit source after the commit. So X-001 stands on that instruction, not on the skill.
- **A-003: QUALIFY.** In-plan backstops (the TF:757 test-adequacy lens and Step 9.17) make test-scenario gaps minor. They cannot rescue defects that sit after every gate (TF:866) or inside a gate's own pass rule (TF:699/735/745).
- **A-004: REJECT.** The plan's own text anticipates findings in untouched files from the unpinned ruff (TF:699 parenthetical; DF-09: bare `uv run ruff` resolves to 0.17.3). A lint-clean tree was never verified and cannot be assumed.

### Point Positions

| Point | Verdict | Secondary | Evidence (path:line - verbatim excerpt, at most 25 words) | Conceded to |
|---|---|---|---|---|
| S-001 | YAML | - | variant-2:1 - "the reviewer returned markdown instead of the requested YAML" | - |
| S-002 | UNION | V2 AC table + V3 INF register | variant-2:36 - "Criterion \| Judgement \| Implementation items \| Test-writing items" | V2 (AC rows) |
| S-003 | BINARY | - | advocate-brief:18 - "Binary severity (decide from evidence, not from the reviewer's label)" | - |
| S-004 | ENUM | V2 "Drift" maps to coverage_gap | RSK:40 - "UC-2 (post-execution): input is completed agent work" (the taxonomy is for completed work) | - |
| C-001 | VALID-MINOR | OQ-51 declares the working-tree case | TF:848 - "run Step 10.6 over a base the owner names ... documented as an Open Question; see OQ-51" | V1 |
| C-002 | VALID-MINOR | - | TF:611 - "supplied ad hoc exactly as `.github/workflows/test.yml:29` does"; test.yml:29 - "uv pip install -e" | V1 |
| C-003 | VALID-MINOR | P10 allowlist backstop | TF:723 - "`git diff --exit-code pyproject.toml Makefile; echo \"EXIT=$?\"`" | V1 |
| C-004 | VALID-MINOR | - | TF:690 - "IF FAILED, fix the cause (never weaken an assertion) and re-run until PASSED" | - |
| C-005 | VALID-MINOR | - | TF:800 - "OUTPUT UNDER REVIEW: the FULL change set listed in ... final-change-set.md" | - |
| C-006 | VALID-MINOR | partly disclosed in OQ-46 | D:239 - "`predicates` (types only, for `Entry` fields that hold an issue number)"; TF:330 - "(`parse_utc`, `format_utc`, `valid_issue_number`)" | - |
| C-007 | VALID-MINOR | design mandates the dual surface | TF:384 - "the installed `~/.claude/skills/sc-issue-protocol/` copies also contain the marker" | - |
| C-008 | VALID-MINOR | - | TF:502 - "shows only these added lines"; TF:520 - "fix any finding inside those files" | - |
| C-009 | VALID-MINOR | - | TF:875 - "a failure of this staging command is logged in that section and never reverts the Done status" | - |
| C-010 | V3 | blocking: X-001, X-008; add R2-001 and R2-002 as minor | TF:735 - "every row is PASS (a FAIL is fixed and its step re-run" | V2 (two minor gaps) |
| C-011 | YES | - | variant-1:109 - "The Phase 3 items were not re-read in this session" | - |
| X-001 | VALID-BLOCKING | mechanism narrowed to the runner's "apply" | TF:866 - "apply the remediations the skill offers under `--remediate`"; RSK:324 - "reflect AUTHORS but NEVER runs `/task`" | V1 (co-finder) |
| X-002 | VALID-MINOR | T-2 covered | TF:460 - "a `failed` entry past backoff with attempts below 3 first checks the day cap" | - |
| X-003 | partially_covered | not a defect (declared DF-05) | TF:735 - "\"full suite: CI only\" (the whole `make test` run is left to CI, decision DF-05)" | - |
| X-004 | partially_covered | not a defect (DF-05) | TF:735 - "the whole `make test` run is left to CI, decision DF-05" | - |
| X-005 | covered | - | variant-3:291 - "No in-cycle or Orca retry is asserted; no daemon mode exists by construction." | - |
| X-006 | VALID-MINOR | INF-146 partially_covered | TF:460 - "a failing save giving exit 6 `state_dir_unwritable` through `audit.stderr_fallback`" (no cycle test at TF:472) | V2 |
| X-007 | VALID-MINOR | AC-6 partially_covered | TF:460 - "a lost label, a voided approval or a changed Project status gives `revalidation_failed`" (absent from TF:475) | V2 |
| X-008 | VALID-BLOCKING | - | TF:699 - "ensuring exit 0; a finding in a file this task did not touch ... is recorded and NOT fixed" | - |
| X-009 | YES | corroborated by V2 | variant-2:129-141 - test-file table names 5.6-5.8, 6.9, 8.2-8.8 as creating items | - |
| A-001 | ACCEPT | verified, not assumed | TF:864 - "--mode post --remediate --diff <BASE SHA>..HEAD" (matches every card's citation) | - |
| A-002 | QUALIFY | - | RSK:321 - "`--remediate --depth deep` → MDTM route: `task-builder` builds the MDTM task file; the user runs `/task <path>`" | V2 (in part) |
| A-003 | QUALIFY | - | TF:757 - "flag ... missing negative and boundary cases" | - |
| A-004 | REJECT | - | TF:699 - "(the local `uv run ruff` is not the pinned 0.15.20)" | - |
