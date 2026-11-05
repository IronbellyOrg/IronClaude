# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 1 (Round 2 and 2.5 appended below as they run)
- Advocates: 3 (one per reviewer card; model sonnet; Mode A, default agent spec)
- Convergence threshold: 80%
- Focus areas: correctness, coverage, deviation-classification
- Persistence note: written by the orchestrator from the advocates' returned reports; tables and positions are kept, long evidence prose is shortened.

## Round 1: Advocate Statements

### Variant 1 Advocate (reviewer 1, analyzer)

Position: V1 is the only card that opened the skills that execute graph, impact and init-lite; it alone found the graph `init` ordering gap and the `-i` / `-o` aliases. Its blocking label on R1-01 is over-claimed; the real defect is a should-fix at the top of the list.

Steelman of V2: the only self-audit that read every command file's real headings, which caught the double boundaries headings (`brainstorm.md:145`/`:177`, `workflow.md:63`/`:78`, `cleanup-audit.md:87`/`:101`); R2-06 is a real spec delta (`spec:147` names only Invariant 3, Task 8 amends 2 and 3); R2-05 is a fair prompt for owner sign-off.

Steelman of V3: best citation accuracy (22 of 22); R3-02 states the init-lite gap sharper than R1-02 (Activation list at `init-lite.md:54-58`, no `--dry-run` writer named); R3-09 and R3-07 are unique and correct.

Concessions: R1-01 over-labelled (impact sub-claim wrong: `--output-dir` has a default at `impact SKILL.md:29` and step 10 always writes); R1-06 wrong in direction (`spec:142`); R1-09 unconfirmed; R1-02's forwarding risk is weak; R1-03 overstated; V1 missed C-006, C-007, R3-07, R3-09, R2-06.

Shared assumptions: A-001 QUALIFY (tasks cite spec rows, so a gap is recoverable; per-task QA checks only each task's own criteria, so silent omissions are the risk). A-002 ACCEPT (each command says "Do NOT proceed ... using only this command file"; each skill fixes its own write scope: `impact SKILL.md:182`, `graph SKILL.md:158`, `init-lite SKILL.md:63`).

### Variant 2 Advocate (reviewer 2, qa)

Position: V2 is the most calibrated card but the least complete; it confirmed no finding that meets the blocking test and misses the real skill-level gaps V1 and V3 found.

Steelman of V1: the skill layer (closed flag tables `impact SKILL.md:19-30`, `graph SKILL.md:23-28`; contract only with `--output-dir` at `graph SKILL.md:64`/`:85`; commands pass flags unchanged `graph.md:42`, `impact.md:45`); static tests only grep text so the defect would surface at live AC-1.2.

Steelman of V3: best grounding; R3-02, R3-09, R3-07, R3-06 hold when checked.

Concessions: V2 raised none of C-001 to C-005 and C-009; weakest coverage (0.70); R2-01 miscounts keys and misses the trailing spaces on `business-panel.md:6` (a stripped line makes a fifth deletion and breaks the "at most 4" bound); R2-04's fix is weaker than dropping the unrelated test; R2-05 arguably minor; R2-03 severity debatable.

Shared assumptions: A-001 QUALIFY; A-002 QUALIFY (true for the three commands, but the plan edits the skills too, so it is incomplete skill edits, not command-only edits).

### Variant 3 Advocate (reviewer 3, refactorer)

Position: V3 is the best-grounded and best-calibrated card, with no blocking finding, which the advocate holds is correct. The graph and impact skill gap is a real should-fix that V1 explained better than V3 did.

Steelman of V1: only card that opened the skills; closed flag tables; static tests cannot catch it; R1-13, R1-10, R1-08 right.

Steelman of V2: cheapest card to act on; R2-03, R2-04, R2-05 real; nothing inflated.

Concessions: R3-06 count error (six, not seven); `t1_ref` note inconsistent; V3 missed the closed flag tables, R1-13, R1-10, R1-11, R2-06, R2-07; R3-03 narrower than the real defect; D-P1-4 unresolved (`spec:142`).

Shared assumptions: A-001 QUALIFY; A-002 QUALIFY.

### Per-point positions after Round 1

| Point | V1 advocate | V2 advocate | V3 advocate | Majority result |
|---|---|---|---|---|
| C-001 | V1 claim (blocking about 40 percent) | V3 severity, V1 substance (65) | V3 severity, V1 breadth (65) | should-fix; merge V1's flag-table edits into R3-03 |
| C-002 | V3 (65) | V1/V3 (75) | V3 (80) | V3 wording, should-fix |
| C-003 | V1 = V3 (80) | V1/V3 (75) | V1 = V3 (75) | should-fix |
| C-004 | V1 = V3 (60) | V1/V3, weak (60) | V1 = V3 (70) | should-fix |
| C-005 | V1 should-fix (55) | V3 minor (60) | V3 minor (65) | minor |
| C-006 | V3 minor (65) | V2 should-fix, narrowly (55) | V3 minor (70) | minor |
| C-007 | V3 minor (70) | V3 minor (60) | V3 minor (75) | minor; drop the test from Task 6 |
| C-008 | V1 minor (60) | V1 minor (55) | V1 minor (65) | minor |
| C-009 | V1 = V3 minor (75) | V1 = V3 minor (80) | minor (85) | minor |
| X-001 | none (55) | V3 non-blocking (70) | V3 (62) | not blocking |
| X-002 | V3 (65) | V2 narrowly (55) | V3 (70) | minor |
| X-003 | V3 (70) | V3 (60) | V3 (75) | minor |
| X-004 | V1 (55) | V3 (60) | V3 (65) | minor |
| X-005 | V1 (60) | V1 (55) | V1 (65) | minor |
| X-006 | V1 (70) | V1 (65) | V1 (60) | no UNVERIFIED entry needed |
| A-001 | QUALIFY | QUALIFY | QUALIFY | QUALIFY |
| A-002 | ACCEPT | QUALIFY | QUALIFY | QUALIFY (plan edits skills, edits incomplete) |

Taxonomy tags (auto, highest level wins): L1 surface = C-005, C-006, C-009; L2 structural = C-001, C-002, C-007, C-008; L3 state-mechanics = C-003 (a check that fails on a correct run), C-004 (a detection rule with no boundary), A-001, A-002. All three levels covered.

Omission check: every advocate answered A-001 and A-002. No omissions.

Convergence after Round 1: 17 of 20 diff points agreed (S-001 and S-002 not debated; A-003 is stated). 85 percent.

## Round 2: Rebuttals

### Variant 1 Advocate (Round 2)

- R1-01: conceded to should-fix (spec 3.1 gives graph and impact "Small fix: None", `spec:144-145`; a conformant brief passes `--output-dir`; impact's `--output-dir` has a default, `impact SKILL.md:29`, and step 10 always writes, `:49`). What survives: the `--report-dir`-only path in Task 5 is still unfulfillable because step 10 and the write-scope sentence (`SKILL.md:49`, `:182`) are not edited, so `<report-dir>/return-contract.yaml` is never written.
- R1-02: conceded; `init-lite SKILL.md:25` and `init-lite.md:54-58` enumerate five flags so the new flags would not be forwarded. V3's R3-02 wording wins.
- R1-04: settled at minor. The helper would be the only persistent Orca-name guard in the suite and would be vacuous as written (no `filterwarnings = error`, `pyproject.toml:107-116`); the Check SCAN grep runs after every task and in Task 15.
- R1-06: conceded (`spec:142` says "from P2"; D-P1-4 is disclosed scope creep). R1-09: conceded (matrix not read). R1-03: conceded as overstated; kept at should-fix for the missing detection rule (`plan:261` vs `plan:184`).
- Final edits proposed: Task 5 (flag-table sentence, step 10, write-scope sentence, where `impact.md` lands); Task 4 (G-O step and the "(only with `--output-dir`)" heading; `init` refused before the Skill call, the skill writes the failed contract); Task 1 (Python regex plus a negative case); Task 2 (`-i`, `-o`).
- New evidence: `graph.md:39-42` runs the Skill first and `:48` makes the guard step 1 of Init, so the plan's after-Init section can only refuse after the preflight; `graph SKILL.md:108` `refused_reason` enum has no unattended value; `adversarial.md:68-69` lists `-i` and `-o`.

### Variant 2 Advocate (Round 2)

- Conceded: V2 raised none of C-001 to C-005; the settled severities stand (should-fix for C-001 to C-004, minor for C-005). R2-01: `business-panel.md:6` ends in two spaces; stripping them makes a fifth deletion and breaks the "at most 4" bound, so "no fix needed" was wrong. R2-03 conceded to minor (plan:24's parenthetical names `## Boundaries` for every file except business-panel). R2-04 conceded: drop the test (`tests/test_cleanup_audit_structure.py:17` targets `cli/cleanup_audit`). R2-05 conceded to minor (Task 15 already reports it, plan:284).
- Final edits proposed: plan:24 "first `## Boundaries` heading (business-panel: `## CRITICAL BOUNDARIES`; index-repo: after `## Output Format`)"; delete the test from Task 6's pytest line (plan:147); reword D-P1-1's lead-in (two readings of WC-4, plan keeps the existing key, coordinator ratifies in the Task 15 report); add D-P1-11 (init-lite's contract is also written on `--dry-run`, so Safety Invariants 2 and 3 both admit it, `spec:147` names only 3); add the plugin-copy inventory line to Task 15; change plan:223 to "keys and values byte-for-byte unchanged, including trailing spaces".
- On V1's updated R1-01: agrees at should-fix; the `--report-dir`-only path is unfulfillable (impact step 10 `SKILL.md:49` and write scope `:182`; graph G-O and heading `SKILL.md:64`, `:85`). V1's Task 4 and 5 edits are enough; do not add "bad flags blocked" language because neither STOP column lists an unknown-flag stop.
- New evidence: `graph.md:48` init guard is step 1 of the after-skill Init steps, so it fires only after the Skill call at `graph.md:40` (confirms V1's ordering point); `graph.md:53` forwards only `--output-dir` on the post-init re-check.

### Variant 3 Advocate (Round 2)

- Conceded: missed the closed flag tables and R1-13 (`graph.md:40` calls the skill first; Init steps run after the preflight returned `init.form`, so a refusal placed after Init fires too late; `graph SKILL.md:108` `refused_reason` has no unattended value). R3-03 was narrower than the real defect: it missed that the `--report-dir`-only path cannot be met because impact step 10 and write scope (`SKILL.md:49`, `:182`) and graph's "(only with `--output-dir`)" heading (`SKILL.md:85`) are not edited. R3-06 count error (six, not seven). `t1_ref` note wrong (R3-01 carries F-001).
- Countered: R3-08 stays minor (plan:24 already gives the anchor in a parenthetical; V2 conceded minor).
- Final edits: R3-02 should-fix (Task 8: Activation bullets for both flags; skill consumes both and never forwards them to the CLI; skill writes `<report-dir>/return-contract.yaml` on every outcome including `--dry-run`). R3-03 merged into R1-01 at should-fix (Task 4: flag-table rows, G-O step, heading, Will Not write line `SKILL.md:158`; Task 5: same rows, step 10, write-scope sentence `:182`, where `impact.md` lands, worker contract at `<report-dir>` lists it in `artifacts`; a test that each skill's flag table names both flags; no "bad flags blocked" wording). R1-13 accepted at should-fix: add a STOP row to graph's flag table (positional `init` with `--unattended` gives `status: blocked`, reason "init runs only when the user types it"; the spec maps a flag-STOP `blocked` to `failed`, `spec:72`); a STOP yields no `init.form`, so the Init steps never run and no new enum value is needed. R3-04 should-fix (per-command `nested` list in `UNATTENDED_EXPECT`: brainstorm `[analyze, adversarial]`, workflow empty). R3-07 minor. R3-09 minor. R1-10 minor (name `-i` and `-o` in the adversarial section).
- New evidence: `graph.md:46` ("These steps run only for `init`, after the skill's preflight returned `init.form` ... and no refusal") shows a skill-side STOP row cuts off the Init steps with no change to the command's Init text; `adversarial.md:68-69` read directly.

## Round 2 close

Rounds completed: 2. All three advocates now agree on every diff point; no residual disagreement (convergence 100 percent over the debated points, 20 of 20). Final severities: should-fix = C-001 (R1-01 merged with R3-03), C-002 (R1-02/R3-02), C-003 (R3-01/R1-05), C-004 (R1-03/R3-04), R1-13; minor = everything else. Blocking = none.

## Round 2.5: Invariant probe (fault-finder, opus, read-only)

Persisted by the orchestrator from the returned report. The orchestrator re-read the cited lines for INV-1 to INV-6 (brainstorm `SKILL.md:105-108`, `:335`, `:385`; `graph SKILL.md:27`; `WORKER-CONTRACT.md:14`; `test.md:22`, `:106`; `analyze.md:100`; `design.md:99`; `brainstorm.md:59`; `handoff-routing.md:87-101`) and they match.

| Id | Severity (probe) | Claim | Status | Plan edit |
|---|---|---|---|---|
| INV-1 | HIGH | brainstorm creates its output dir with a `-N` suffix when the dir exists and is not empty (`SKILL.md:108`), so the worker contract can land in a dir the coordinator did not pass; the early STOPs (steps 1-7, `:95-107`) end before the contract is written (`:335`) | UNADDRESSED (plan:94, 96) | Task 3: under `--unattended` use the passed dir exactly, never suffixed; refuse a dir that already holds a `return-contract.yaml`; every STOP writes a `failed` worker contract |
| INV-2 | HIGH | `--report-dir` has none of the path rules the commands' own dir flags have (graph `.git`/`.codegraph` block, `graph SKILL.md:27`; adversarial forbidden prefixes, `SKILL.md:396-398`); the contract location for a rejected or unwritable report dir is undefined (a report dir under `.claude/skills/` would also break `make verify-sync`) | UNADDRESSED (plan:109, 124) | Skeleton (plan:24) and Tasks 2, 4, 5: `--report-dir` gets the same path rules; a rejected or unwritable report dir counts as "no report dir known", refusal printed in chat only (`WORKER-CONTRACT.md:14`) |
| INV-3 | MEDIUM | `init-lite.md:94` "Will Not: Write anything when `--dry-run` is set" contradicts Task 8 (same defect as R3-09) | UNADDRESSED | Task 8: "except the worker contract under `--unattended`" line next to `:94` |
| INV-4 | MEDIUM | brainstorm Wave 0 step 7 (`SKILL.md:105-107`) STOPs when the handoff skill is missing, before the plan's skip rule (Wave 4, plan:96) runs; `SKILL.md:385` says "User must choose" | UNADDRESSED | Task 3: under `--unattended`, step 7 is skipped and the skip recorded |
| INV-5 | MEDIUM | consent steps left open in commands called "no gate": `test.md:106` (via `--fix`, `:22`), `analyze.md:100`, `design.md:99` | UNADDRESSED (plan:201, 214) | New decision D-P1-12: consent is never given under `--unattended` (or `--fix` counts as the caller-supplied consent per WC-2 (b)); each section states the result |
| INV-6 | MEDIUM | brainstorm ref `handoff-routing.md:87-101` still passes `--output <output>/adversarial/` and forwards `--interactive`; Task 3 does not list it; `brainstorm.md:59` `-i` short form and `=` spellings not refused | UNADDRESSED (plan:92) | Task 3: add the ref with an `--unattended` block; refuse `-i` and the `=` spellings |

Probe result: 2 HIGH, 4 MEDIUM, all UNADDRESSED. Clean checks recorded by the probe: the write-verb audit matches text not line numbers (`tests/skills/test_worker_contract.py:543, 549`); the brief guard reads only the project and user copies (`WORKER-CONTRACT.md:16`); Check ADDITIVE merge-base is safe for the edited files; every contract-writing skill has `Write`; graph and impact verb regexes allow the planned wording.
