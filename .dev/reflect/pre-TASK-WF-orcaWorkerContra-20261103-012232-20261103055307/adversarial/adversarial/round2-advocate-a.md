# Round 2 Rebuttal: Variant A advocate (reviewer card 1, analyzer)

Citation key as in `diff-analysis.md`: `A:N`, `B:N`, `C:N` are card lines; `TL:N` is the plan; `SRC:N` is `source.md`; `qa.md:N` and `SKILL.md:N` are the `sc-implement-protocol` executor files under `~/.claude/skills/`; `retry.md:N` is that skill's `refs/retry.md`. `R1-A`, `R1-B`, `R1-C` are the Round 1 statements. I opened every line I cite in this round. Checks I ran in this round are marked "(run today)".

Position in one line: the verdict stays FAIL with R3-F1 as the only blocking finding, and it is not over-graded. None of the three named candidates (R1-F4, R3-F3, R1-F2) reaches a halt that no repair can close. The finding nearest to a second blocker is one no one nominated: R1-F3/R3-F5 (Task 6's phase slot). It and R3-F2 should be fixed in the same plan revision as R3-F1.

## 1. Responses to criticisms of Variant A

**1.1 "A's PASS missed R3-F1; A never ran the Constraints-against-tasks check"** (R1-B Weakness 1, R1-C Weakness 2, diff-analysis X-001). **Conceded, as in Round 1.** One new fact makes the conflict sharper than any card said: Task 4 does not create a file inside the skill package, it overwrites one. `plugins/superclaude/skills/sc-recommend/` already holds `SKILL.md` and `refs/HOW-WE-WORK.md` (listed today), and the repo test says "the guide ships inside the plugin's sc-recommend skill as refs/HOW-WE-WORK.md" (`tests/commands/test_routing_plugin_parity.py:3-4`, opened today). So TL:90 orders an edit to an existing file in a skill package, and TL:21 says "P0 edits no command, skill or agent file". In plain words, "edits" fits that act.

**1.2 "A's calibrator saw the qa.md:52 route for R1-F1 and R1-F3, and A under-stated it"** (R1-B Weakness 1, quoting A:132). **Half conceded.** For R1-F3 the criticism is right, and section 2.5 shows the route is stronger than my card said. For R1-F1 it is weaker than it looks: a repair exists (section 2.3), so the route ends in a repair round, not a halt.

**1.3 "R1-F3 under-states the edge case: omit the phase and you breach the instruction, invent one and you write a false claim"** (R1-B Weakness 2). **Conceded and extended.** I checked the hits that have no converting phase (run today). Write verbs appear in `src/superclaude/agents/learning-guide.md` (an agent; no phase converts agents), `src/superclaude/skills/task-builder/SKILL.md` and `src/superclaude/skills/sc-crash-recovery/SKILL.md` (no command row converts them), and `src/superclaude/commands/git.md` (never a worker, SRC:61). There are also 25 read-only `gh pr view|list|checks` lines in the scan roots, which TL:125 puts on the list because it names `gh pr` as a verb. For each of these, TL:125's "the phase that converts its command" has no true value. Section 2.5 grades the result.

**1.4 "R1-F5 under-weights the precedent for a plugin core copy"** (R1-C Weakness 5). **Partly conceded.** The precedent is real: `tests/commands/test_impact_command.py:309` reads `plugins/superclaude/core/CODEGRAPH.md` (opened today), and SRC:252 excludes `plugins/superclaude/core/WORKER-CONTRACT.md` by name, so the spec allows a copy. The distribution evidence also stands: `scripts/build_superclaude_plugin.py:75` loops over `["agents", "commands", "hooks", "scripts", "skills"]` only (opened today), and the parity test says "Plugin installs never receive core/ files". Task 3 should cite both sides. I also withdraw my Round 1 proposal to fold R3-F4 into R1-F5 as a conditional clause. R3-F4 has a route inside this run: if Task 3 adds the copy and a later task edits the contract, then Task 3's `cmp` check (TL:74) fails at the end state. The managed FINAL returns `issues` when "a later change contradicts" an acceptance check (qa.md:310), and that ends as `E-ARCHIVE-BLOCKED` (qa.md:286). R3-F4 stands alone at should-fix.

**1.5 "A's reason format leaves the keying problem open"** (R1-C Weakness 6). **Conceded.** The merged fix uses my reason slots (A:65-66) and C's keys: path, verb and stripped line text, never line numbers (C:108-110).

**1.6 "Two tests pin the plugin core copy of CODEGRAPH.md"** (A:95). **Conceded in Round 1.** One test reads the copy (`test_impact_command.py:309`). It checks only that the copy is dollar-safe, not that it is byte-identical to the source.

**1.7 "A judged the routing-guide test risk not worth a finding"** (diff-analysis C-005, A:110-111). **Conceded, upgraded to should-fix.** In Round 1 I graded R3-F6 minor. That is not consistent with my grade for R1-F2, which also costs at most one repair round. `tests/core/test_how_we_work_routing_table.py:341` is the ASCII test, and line 1091 holds the `"### 3.14 "` to `"## 4. "` slice (both opened today). Should-fix, with C's citation corrected from 290 to 1091.

## 2. Stress test of the consensus

### 2.1 Is R3-F1 over-graded?

**The best case that it is over-graded.** (a) A halt needs a reviewer to answer yes on question 4 (qa.md:52, qa.md:339). That reviewer reads Task 4, which orders the copy (TL:90), and the Constraints, which allow "their plugin copies" to carry Orca text (TL:24). TL:21's parenthetical also names its source as "no command edits". (b) Nobody runs the copy as a skill. It is a byte mirror of a core document. (c) No card measured how often reviewers read constraints literally.

**Why the grade holds.**
1. **No repair closes it.** If the copy is dropped, AC-0.2's `cmp` (TL:93) is unmet, which is B1. If the copy is kept, the B4 breach stays. The ladder ends in `ladder-end` (qa.md:280). If the adviser disputes the contradictory AC instead (retry.md:72), the run ends in a `dispute` halt (retry.md:107, qa.md:281). The adviser also cannot call the finding "not supported by its own citations", because the quote is byte-present (qa.md:61).
2. **Every review is a fresh subagent.** Reviews run inline only when N≤3 (qa.md:314, SKILL.md:101). This plan has 8 tasks, so every Task 4 review is a fresh subagent working from the closed template, which says "Do not trust the implementer's report" (qa.md:331). That reviewer has not watched the executor reason through TL:24.
3. **Several readers each get a chance.** These include the Task 4 A1 review, any re-review, and the managed FINAL, which reads the Constraints afresh (qa.md:310). The literal reading needs only one yes from all of them.
4. **The literal reading is the plain one.** The target path contains `skills/`, the file already exists in that skill's folder, and the act is an edit (section 1.1).
5. **Expected cost against fix cost.** A yes costs up to five attempts, a halt, and a user Ruling. The fix is one reworded sentence (C:26-28), and it restores the spec's own wording at SRC:220.

**Verdict on 2.1:** not over-graded. The report should say "can halt", not "will halt", as R1-B Weakness 3 asked. Confidence 0.75.

### 2.2 R1-F4 (spec `src/` paths and evidence ids copied into an installed core file): not blocking

- **No gate in the run reads the rule.** It lives in repo `CLAUDE.md:72-87`, not in the plan's Constraints (TL:17-27). B4 fires only on plan Constraints and task instructions (qa.md:52, SKILL.md:93). B2 fires when a claim is "false against live source" (qa.md:50), but in this checkout `src/superclaude/cli/install_core.py:36` is a true pointer. The managed FINAL reads the plan's Constraints, not repo `CLAUDE.md` (qa.md:310). No test scans core files for `src/superclaude` paths: `tests/skills/test_primitive_dual_surface_lookup.py` has no match for "core" (run today). So the executor finishes cleanly and the defect ships.
- **That is why it is the top should-fix, not a blocker.** It is the only finding where the run passes and the output is wrong in other projects (`CLAUDE.md:74`: "run in OTHER projects, where `src/superclaude/` does not exist"). Two plan lines raise the odds of literal copying. TL:22 says the file "restates only what" sections 2.1-2.3 say. TL:104 makes Task 5 pin "a phrase quoted from `./source.md`" for each rule. Some of the rule text itself names `src/` and skill paths: SRC:59 cites `src/superclaude/cli/install_core.py:36,56,65-70`, and WC-9 lists by path the skills that defer staging (SRC:77, `sk/sc-implement-protocol/refs/managed-workspace.md:36` and others). A faithful restatement has to turn those into `~/.claude/skills/...` paths (`CLAUDE.md:80`).
- **One check outside the plan remains.** The owner reviews the commit before it is made (TL:20, TL:154). That is a human gate, not an executor gate, and nothing in the plan points the owner at this rule.
- **Grade:** should-fix, listed first. Fix: my Constraints line (A:84-85). That line makes the rule quotable, so B4 can then catch a breach.

### 2.3 R3-F3 with R1-F1 (Task 5's quoted-phrase rule, Tasks 1-2 paraphrase, the FINAL "later change contradicts" rule): not blocking

- **The fan-in instance is repairable.** TL:112 orders the assertion "at most 10" "(as written in section 2.3)". TL:104 orders a phrase quoted from source.md, and SRC:122 says "maximum of 10 inputs" and "never exceeds 10". The test can assert both phrases. TL:104 asks for "at least one" quoted phrase, so both instructions are met. The contract can carry both, because TL:22 forbids a new rule, not a second wording of the same rule. If the executor copies "(as written in section 2.3)" into a test comment, that is a false claim in delivered code (B2, qa.md:50). Rewording the comment closes it.
- **The general paraphrase case is repairable.** If Tasks 1-2 paraphrase a rule, Task 5 can add the spec phrase to the contract. Adding text breaks none of Tasks 1-2's acceptance checks (TL:45, TL:61), which ask for presence, not exact wording.
- **The FINAL route needs three conditions.** The paraphrase must happen, Task 3 must add a plugin copy (which the build-script evidence argues against, section 1.4), and Task 5 must edit the contract without re-copying it. Only then does Task 3's `cmp` (TL:74) fail at the end state (qa.md:310). R3-F4's byte-identity test removes even that route.
- **Grade:** should-fix, drift for the "at most 10" instance (the plan attributes to section 2.3 wording that SRC:122 lacks), none for the general mechanism.

### 2.4 R1-F2 (Task 8 evidence files): not blocking

TL:157 is an evidence-type acceptance check, unmet only when "the evidence artifact is absent" (qa.md:83-85). The Task 8 executor can save the missing outputs (AC-0.1's three commands, AC-0.2, AC-0.3, AC-C1, AC-C2), and nothing in TL:147-154 forbids it. If it does not, the A1 review raises B1, and the A2 fix pass closes it by saving the files. That costs at most one repair round, so it stays should-fix.

### 2.5 The nearest second blocker is one nobody nominated: R1-F3 with R3-F5 (Task 6 phase slot)

- **Its structure matches R3-F1.** TL:125 requires each allowlist entry to carry "a one-line reason and the phase that converts its command". For the phase-less hits verified in section 1.3, the executor has two options. It can leave the phase out, which a reviewer can flag as B4 by quoting TL:125. Or it can name one, which is B2 against SRC:61 and SRC:201 ("no `--unattended` mode and no Phase 4 changes"), and against SRC:224 (pr-submit converts only under D3 (b)). The plan also dropped the spec's third category: SRC:305 allows a hit that is "refused under `--unattended`", and TL:125 removes it ("At P0 no command is refused under `--unattended` yet").
- **Why I still grade it should-fix (confidence 0.6).** A truthful entry such as "no converting phase: never a worker (section 4)" answers a question whose premise is false. It does not ignore the instruction. Task 6's acceptance checks (TL:127-131) do not ask for a phase, and AC-0.9 asks only for "an explicit allowlist with a reason" (SRC:305). So a reviewer has a reading that reconciles the plan and the spec. R3-F1 has a weaker reconciling reading, because the act literally edits a file in a skill folder (section 2.1, point 4).
- **R3-F2 is in the same bundle.** Its mechanism is the same. Its cover is better for the section 3.1 flags: SRC:59 assigns the brief template to the file, SRC:84 brings in "every flag section 3 lists as required", and SRC:220 says "a coordinator brief template listing the section 3.1 flags". Its cover is weaker for the "from P1" marker, which TL:58 itself sources to section 6. Should-fix.
- **Consequence.** The plan has to be revised anyway because of R3-F1. That revision should also apply, in the same pass, R3-F2's added clause (C:46-47), the merged Task 6 reason format with its keys, the "at most 10" wording fix, and R1-F4's Constraints line. Each is one to three lines of plan text. If the panel prefers a strict rule (any unrepairable conflict that a reviewer can reach is blocking), then R1-F3/R3-F5 also qualifies, and I would not contest that upgrade.

## 3. Final severity for every finding

| Merged finding | Cards | Final severity | Class | Basis |
|---|---|---|---|---|
| Constraint TL:21 against the Task 4 skill-folder write (TL:90, TL:93) | R3-F1 | **blocking** | drift | Section 2.1. Fix: C:26-28 |
| Installed-path rule missing from the Constraints | R1-F4 | should-fix (fix first) | none | Section 2.2. Fix: A:84-85 |
| Task 6 phase slot, read-only hits, keying | R1-F3 + R3-F5 | should-fix (same revision as R3-F1) | drift | Sections 1.3 and 2.5. Fix: A:65-66 plus C:108-110 |
| Constraint TL:22 against the Task 2 template (3.1 flags, "from P1") | R3-F2 | should-fix (same revision) | drift | Section 2.5. Fix: C:46-47 |
| "at most 10" and the quoted-phrase rule | R1-F1 + R3-F3 | should-fix | drift (instance), none (mechanism) | Section 2.3 |
| Task 8 evidence files | R1-F2 | should-fix | none | Section 2.4 |
| An added plugin core copy has no sync check | R3-F4 | should-fix (conditional on Task 3 adding it) | none | Section 1.4; the qa.md:310 route inside this run |
| Routing-guide ASCII and heading-slice tests | R3-F6 | should-fix | none | Section 1.7; citation corrected to :341 and :1091 |
| Task 3 deciding evidence | R1-F5 + R2-3 | minor | none | Build script line 75 plus the precedent (section 1.4) |
| Phantom AC-0.8 in the Constraints | R2-1 | minor | drift | No gate reads it; B2 covers delivered text only (qa.md:50); B and C agree |
| Handoff to the live plan, re-staging | R2-2 + R3-F10 | minor | none | SRC:238, SRC:303-304 against TL:154; TL:19 partly covers re-staging |
| Hard-coded negative for `## Unattended mode` | R3-F7 | minor | none | TL:115 against SRC:306 |
| Template flags unchecked against command files | R3-F8 | minor | none | TL:58; precedent at the routing test's line 258 |
| Goal says "every copy" | R3-F9 | minor | none | TL:15 against TL:90 |
| No verify-sync baseline; tests/docs and tests/unit not covered | R3-F11 | minor | none | TL:33-35, TL:96 |
| Coverage-matrix omissions | B matrix_omissions | drop (keep as an appendix note) | none | Bookkeeping; B:61 |
| Task 7 environment (`/opt/Orca`, profile file) | A self-audit; B and C calibrators | drop (note only) | none | A:110-112 checked it, and R1-B Weakness 6 confirmed it again |

## 4. Shared assumptions A-009, A-010, A-011

- **A-009: ACCEPT (re-checked today).** `src/superclaude/cli/install_core.py:30-32` defines `install_core_files(target_path: Path = None, force: bool = False) -> Tuple[bool, str]`, which matches TL:72's `ok, msg = install_core_files(target_path=d)`. Line 36 says it copies every `.md` file in `core/`, so the new file needs no other registration in order to install. The `KNOWN_CORE_FILES` entry (lines 13-27) is a separate requirement, met by Task 1.
- **A-010: ACCEPT (re-checked today).** The merge base is `c118b5a59d365b894c5f2caa2270ec9986812934`. `git diff --numstat "$(git merge-base master HEAD)" -- src/superclaude/core/HOW-WE-WORK.md | awk '$2 != 0'` printed nothing. No task before Task 4 touches that file (TL:31-74).
- **A-011: ACCEPT, with one refinement (re-checked today).** The full SRC:246-253 pipeline printed nothing (stage exits `0 1 1 1 1 1`). The first stage does find hits, though, and they all sit in `src/superclaude/skills/ccsession-tag/` (`ccsession`, `models.py`, `README.md`), which line 249 excludes. So the scan is clean today only because of its exclusions. Any new hit can come only from this plan's edits outside the five excluded paths.

## 5. Still-contested points

| ID | My current position | Confidence |
|---|---|---|
| X-001 / S-001 (verdict) | FAIL, one blocking finding (R3-F1) | 0.85 |
| X-002 (is R3-F1 blocking, or over-graded?) | Blocking, recorded as "can halt"; not over-graded (section 2.1) | 0.75 |
| R1-F3 + R3-F5 (second blocker?) | Should-fix, fixed in the same revision; I would not contest an upgrade under a strict rule | 0.60 |
| X-003 / R3-F2 | Should-fix, fixed in the same revision | 0.65 |
| U-001 / R1-F4 | Should-fix, first priority; not blocking because no executor gate reads the rule | 0.80 |
| C-003 / R1-F1 + R3-F3 | Should-fix; repairable inside the run | 0.80 |
| U-002 / R1-F2 | Should-fix; one repair round at most | 0.75 |
| U-008 / R3-F4 | Standalone should-fix, conditional (my Round 1 fold withdrawn) | 0.70 |
| C-005 / R3-F6 | Should-fix (moved up from my Round 1 minor), citation :1091 | 0.65 |
| U-003 / R2-1 | Minor (C still says should-fix) | 0.75 |
| X-004 / C-002 / R1-F5 + R2-3 | Minor; Task 3 cites the build-script line and the precedent | 0.80 |
| A-011 | Accept, noting that the scan's exclusions do the work | 0.90 |
