# Round 1 — Advocate for Variant 2

## Evidence legend and decision rule

All paths below resolve from `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/`.

- `plan` = `.dev/tasks/to-do/TASK-WF-loosenBlockerCla-20261115-133045/TASK-WF-loosenBlockerCla-20261115-133045.md`.
- `spec` = `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md`.
- `plan-input` = `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/09-plan-input.md`.
- `V1` and `V2` = `variant-1-original.md` and `variant-2-original.md` in the ADV directory named in the common brief.
- Repository paths beginning `src/` are literal checkout paths, not directions for installed primitives.

I read the common brief, both cards, the diff analysis, the complete plan, relevant spec sections and the repository evidence identified below. The controlling test is the brief's line 15: following the plan must reach a wrong or impossible result that no later step catches, and the issue must not be wording. A missing explicit regression test alone does not establish a wrong result when the plan already prohibits the behavior. Conversely, a mandatory acceptance command with a nonexistent target is an execution defect, not a moved citation.

## A. Position summary

Variant 2 makes the stronger repository-grounded contribution: it identifies an over-broad merge scan, retained label-based FAIL rules, and a nonexistent acceptance-check path that are not addressed by the later tasks. It should supply those verified additions to a merged review, not displace Variant 1's valid registry, final-sweep, owner-checkpoint and fresh-evaluation findings. I defend Variant 2's concrete evidence while narrowing its claims about classifier enforcement, line movement and externally gated measurements.

## B. Steelman of Variant 1 — before critique

Variant 1's strongest argument is that a plan is an executable dependency chain, not just a list of intended components. Task 7 makes a canonical fenced digest, Task 11 omits its registry row, and Task 19 scans every fence holder; Tasks 30 and 35 then demand v2 states incompatible with the digest-equality test (`plan:101-104,146,237,361,416-419`). Those are direct contradictions without a later repair, not requests for more polish.

Variant 1 also follows behavioral reachability rather than accepting that building a helper means using it. Task 20 creates the sweep and Task 22 explicitly invokes it, but Task 21 never invokes it in the task skill (`plan:250,261,273`); the spec requires the last gate to retest every open Medium (`spec:653`). Its owner-checkpoint finding is equally concrete: the plan explicitly authorizes a one-pass transition (`plan:20`), while the scaffold entry requires the measured result and owner go (`spec:940,945`). Its fresh-data finding addresses selection bias not removed by re-splitting the original 318 (`plan-input:16`; `plan:54,66`). These are substantial findings that Variant 2 missed.

## C. Verified strengths of Variant 2

1. **It tests the declared scan against actual unrelated code.** Task 33 scans all tracked `src/` and `plugins/` for three phrases but describes its allow-list as Auggie plus the stage-4 merge carriers (`plan:394,399`). `src/superclaude/cli/pipeline/fmea_classifier.py:304,323` contains “highest severity”; `src/superclaude/cli/roadmap/remediate_parser.py:55,301` contains “higher severity wins”. The spec explicitly excludes those code-assigned families (`spec:845`). Correctly completing Tasks 27–30 does not remove these matches.

2. **It notices label-based rules outside the targeted digest and Rule 6.** `src/superclaude/agents/rf-qa-qualitative.md:239-240` says PASS requires no CRITICAL/IMPORTANT issues and FAIL follows any such issue. Task 28 changes the digest area, merge rule and Rule 6, but not these verdict pairs (`plan:340-345`), despite the general requirement to rewrite or explicitly map fixed FAIL triggers (`spec:275`). The Task 1 patterns do not include the pair's wording (`plan:32`). This is a real gap in removing label-driven failures, although V2's count is wrong: the Grep found eight pairs, not seven.

3. **It finds an unconditional broken command, not merely a moved reference.** Task 26 requires `grep -n "pragmatic" hooks/hooks.json` from the repository root (`plan:321`). Reading that root path returned “File does not exist”; the actual source registration is `src/superclaude/hooks/hooks.json:173`, naming the injector. The plugin has another hooks.json, so “only under src” would also be too strong. No later task fixes this acceptance command.

4. **It keeps two different measurement gaps visible.** The plan-input requires counts of rows with each code-supplied input (`plan-input:15`), whereas the classifier command promises a disagreement matrix but no such counts (`plan:203-208`). Separately, the spec demands fresh planted defects (`spec:680`) and explicitly says to size the planted set in the plan (`spec:987`); the plan only names seeded recall as an entry prerequisite (`plan:20`). These observations are valuable, but their blocking classification needs the qualifications in E and H(e).

5. **It checks offer reachability by carrier.** Task 21 ends with an offer, but Task 22 copies only the brief fields, ledger path, safety route and classifier call (`plan:261,273`); the spec explicitly requires both carriers to make the per-run offer (`spec:946`). The escalation-halt offer is also mandatory (`spec:323`; adopted in `plan:21`), but neither integration task names it. A reference document containing offer wording is not a call to show it.

## D. Weaknesses of Variant 1

1. **It misses the scan's actual false positives.** Task 33 promises a passing test after Tasks 27–30 (`plan:397`), yet the untouched code contains the trigger phrases (`src/superclaude/cli/pipeline/fmea_classifier.py:304`; `src/superclaude/cli/roadmap/remediate_parser.py:55`). These files are explicitly out of scope (`spec:845`); the final strict registry scan is a different test and does not repair Task 33's allow-list (`plan:459`).

2. **It does not inspect all label-driven verdict instructions in the qualitative agent.** The surviving FAIL condition at `src/superclaude/agents/rf-qa-qualitative.md:240` remains operative after Task 28's narrowly described edit (`plan:340`). Merely converting its common digest does not remove this more specific instruction; the general rewrite-or-map requirement is `spec:275`.

3. **Its positive classifier check is too broad for reporting completeness.** V1 is correct that code-input restrictions and no authority are explicit (`plan:23,197`), but that does not supply the required row-availability counts (`plan-input:15` versus command outputs at `plan:203`). The distinction matters: V1 establishes a behavioral constraint, not complete measurement coverage.

4. **It misses the carrier-specific offer omission and broken hook-check target.** The explicit task-skill offer does not appear in the tech-research integration (`plan:261,273`), and the root hook-check target is absent despite being mandatory (`plan:321`; actual registration `src/superclaude/hooks/hooks.json:173`). These are independent of V1's registry findings.

## E. Concessions about Variant 2

- **F3 overcounts incorrectly in the other direction:** it says seven PASS/FAIL pairs. The verified Grep returned eight pairs at 239/240, 290/291, 361/362, 428/429, 499/500, 566/567, 745/746 and 783/784 in `src/superclaude/agents/rf-qa-qualitative.md`. The retained-rule finding survives; the number must change.
- **F4 conflates absent acceptance checks with absent instructions.** `plan:23` explicitly binds every classifier task to code-supplied inputs and disables the “M or C is Y” row for every gate; `plan:135` carries the input restriction into the question reference; `plan:197` tests no authority. A compliant executor cannot freely ask unsupported questions just because Task 14's acceptance list omits another check. Missing availability counts are real, but the prediction of mandated polluted gate behavior is not established.
- **F6 is stronger as a planning/completeness concern than as a blocking finding under this run's strict rule.** The plan explicitly prevents Phase 4 until seeded recall is met (`plan:20`); this catches absent recall before the pilot. The spec still requires a planted-set size in the plan (`spec:987`) and an audit design (`spec:660-674`), but an acknowledged externally supplied entry result is not proof that the plan silently ships an unsafe pilot. The owner gate is not a waiver to skip recall.
- **F7's missing-path limb is certain; its line-shift limbs are not all inevitable.** Task 21 can add fields by extending existing lines, and Task 22 can extend an existing Gate 5 line, rather than necessarily inserting newlines (`plan:261,273`; existing task brief at `src/superclaude/skills/task/SKILL.md:248`; existing Gate 5 at `src/superclaude/skills/tech-research/SKILL.md:415-419`). Exact grep-output pins remain brittle. “Unchanged word for word” at `plan:320` can reasonably mean unchanged content, not permanent line coordinates.
- **F8 assumes an unconditional legacy pin that Task 24 does not require.** It twice limits the assertion to the shadow stage and “before Task 26” (`plan:295,299`). A stage/version-aware test honors that without any later retirement. Lack of an explicit Task 31 edit is not proof the pin must turn red.
- **F9 is not blocking.** Task 11 can mean exactly those eleven definition carriers plus the additional named carrier kinds (`plan:146,150`); the Task 34 trimming reference is loose, but retained allow-list entries do not themselves generate a failing scan once the corresponding phrases are removed (`plan:399,405-410`). Neither establishes a wrong delivery.
- **V2 omitted four useful V1 contributions.** The canonical-source registration, task sweep wiring, stage-1 owner go and fresh-findings evaluation all require attention (`plan:104,146,237,250-273,20,54-66`; `spec:945`; `plan-input:16`). Advocacy is not grounds to discard them.

## F. Diff-point decisions

“Winner” means the better-supported position on that diff point, not an endorsement of every sentence or severity in its card. Confidence is confidence in this adjudication, not classifier probability.

| Diff point | Winner | Confidence | Verified evidence and decision |
|---|---|---:|---|
| S-002 | V2 | 90% | Separating wording and execution failures is sound: `plan:150,399` do not by themselves establish a wrong delivery, unlike the missing target at `plan:321`. V2's actual seven-blocker classification still needs narrowing for F4 and F6. |
| C-001 | both | 99% | `plan:237` requires one digest for every v2 row; Task 30 demands a nonexistent task row without adding a digest (`plan:146,361`), and Task 35 allows a pointer-only file while setting its row to v2 (`plan:416,419`). Both cards correctly identify the same incompatible outputs. |
| C-002 | V1 | 98% | The canonical file must contain a fence (`plan:104`), is absent from Task 11's enumerated rows (`plan:146`), and is inside Task 19's reverse-scan scope (`plan:237`). Even if strict mode delays part of enforcement, Task 39 activates it without adding the canonical row (`plan:459`). |
| C-003 | V1 | 98% | The sweep is built at `plan:250`, explicitly called for tech-research at `plan:273`, and absent from the task integration at `plan:261,361`. GR7 explicitly requires the final-gate retest (`spec:653`); a unit test of the helper is not integration. |
| C-004 | V1 | 99% | “Can run in one pass” (`plan:20`) conflicts with the distinct measured-result-and-owner-go entry (`spec:940,945`). The later pilot owner go is a different transition and cannot retroactively authorize the scaffold. |
| C-005 | V1 | 96% | `plan-input:16` requires fresh findings outside the 318; `plan:54,66` regrade and split the historical table, adding retrospective minors. Fixture/property tests (`plan:192`) do not constitute the missing independently evaluated fresh round. |
| C-006 | V2 | 98% | Task 33's named allowed files (`plan:394,399`) omit trigger-bearing code at `src/superclaude/cli/pipeline/fmea_classifier.py:304,323` and `src/superclaude/cli/roadmap/remediate_parser.py:55,301`. The spec explicitly preserves those unrelated code families (`spec:845`), so the scan needs explicit scope/allow-list correction. |
| C-007 | V2 | 97% | The qualitative agent still says any CRITICAL/IMPORTANT issue makes FAIL (`src/superclaude/agents/rf-qa-qualitative.md:240`), while Task 28 only names the digest, merge and Rule 6 edits (`plan:340`). The finding survives with eight pairs rather than V2's seven; L6's general requirement is `spec:275`. |
| C-008 | both | 94% | V1 is right that `plan:23,135,197` restrict unsupported inputs and authority; V2 is right that availability counts required at `plan-input:15` are absent from command outputs at `plan:203`. Neither fact proves that a compliant implementation must execute the forbidden M/C rule. |
| C-009 | V2 | 97% | `spec:946` requires offers in both carriers, and `spec:323` requires them at escalation halts. `plan:273` copies an enumerated subset that excludes the offer, whereas `plan:261` expressly adds only an end-of-run offer to the task skill. |
| C-010 | V2 | 90% | V2 correctly observes the missing planted-set task/size (`spec:680,987`) and unscheduled audit procedure (`spec:660-674`). I reject its unconditional blocking label: `plan:20` explicitly catches absent recall before Phase 4, and requires the pilot audit window before Phase 5. |
| C-011 | V2 | 97% | `plan:321` requires a missing root hooks path; the source registration actually exists at `src/superclaude/hooks/hooks.json:173`. The exact `grep -n` pin at `plan:266` is brittle, but the claim that every permitted edit necessarily shifts lines is too strong. |
| C-012 | V1 | 92% | Task 24 says “unchanged in this stage” and “before Task 26” (`plan:295,299`). A legacy/stage-conditional assertion satisfies that instruction, so Task 31 need not retire it; an unconditional permanent pin would be an implementation choice, not forced by the plan. |
| C-013 | V2 | 91% | V2 usefully flags the eleven-carrier wording and Task 34 trimming reference (`plan:150,399`). They are non-blocking clarification opportunities: Task 11 explicitly lists the additional kinds (`plan:146`), and Task 34 removes the relevant phrases even without pruning their now-unused allowed entries (`plan:405-410`). |
| X-001 | V1 | 92% | The temporal boundary is explicit in `plan:299`, not inferred. F8 does not prove a permanent assertion, although an explicit version guard would make the intended test easier to implement. |
| X-002 | both | 94% | The instructions constrain all classifier tasks (`plan:23`), while Task 14's acceptance list lacks a specific input-availability test (`plan:183-186`) and Task 16 lacks availability reporting (`plan:203`). The constraint is real; reporting coverage is incomplete; mandatory wrong gate behavior is not established. |

## G. Shared assumptions

- **A-001 — QUALIFY.** Mandatory acceptance commands are part of the executable plan, so a nonexistent target (`plan:321`) or contradictory digest equality (`plan:237,419`) can block. Do not extend “literal” into treating historical location hints or the explicitly stage-bound pin (`plan:295,299`) as necessarily permanent numeric assertions; the brief requires a forced wrong/impossible result, not the worst possible implementation.
- **A-002 — ACCEPT for this review.** I independently read the complete plan and checked the cited text, including `plan:237,261,273,295,361,394,416,419`; the attempted refresh reported the file unchanged. This is a checked snapshot claim, not a license to trust these coordinates after another edit.
- **A-003 — QUALIFY.** The plan expressly identifies the spec as its governing requirements and adopts recommended owner decisions unless changed (`plan:19,21`), so no documented approval authorizes bypassing `spec:945`. But the spec can itself contain defects: the canonical-fence/registry conflict follows directly from `spec:699,726`; fidelity to that conflict does not make the plan executable, and an acknowledged external entry condition (`plan:20`) is not automatically an unscheduled implementation task or permission to skip it.

## H. Explicit settlement of the five disputed points

### (a) Task 24 legacy pin versus Tasks 26 and 31

**Stance: Variant 1 is better supported; Variant 2 F8 is not a demonstrated red test.**

I read Task 24 (`plan:291-299`), Task 26 (`plan:312-322`) and Task 31 (`plan:368-377`), and the current source text at `src/superclaude/output-styles/pragmatic.md:225-231`. Task 24 says the legacy text is unchanged “in this stage”; its acceptance criterion explicitly says a change must fail **before Task 26**. Task 26 then deliberately replaces/moves those bullets. A test that asserts legacy text only while the carrier is legacy is consistent with both instructions; Task 26 already changes the registry version (`plan:316,319`), providing a natural observable boundary.

Task 31 does omit `test_review_brief_rests_on.py` from its rewrite list (`plan:372`). That omission would matter if Task 24 had required an unconditional forever-pin. It does not. F8 is at most a request to make the conditional implementation explicit, not evidence that following the plan forces a failure at Task 26. No task retires or re-pins that new test, but no retirement is needed for an assertion already bounded to the legacy stage.

### (b) Task 33 allow-list versus code containing the phrases

**Stance: yes, the expressly named allow-list omits real code matches; keep Variant 2 F1.**

I Grepped both named files and then Read their relevant source:

- `src/superclaude/cli/pipeline/fmea_classifier.py:304`: “Silent corruption from either signal = highest severity.” A second match is the comment at line 323.
- `src/superclaude/cli/roadmap/remediate_parser.py:55`: “Severity resolution: higher severity wins (BLOCKING > WARNING > INFO)”. Another match is the Step 2 docstring at line 301.

`plan:394` scans tracked `src/` and `plugins/`, not merely review instruction files, and describes the allowed rows as Auggie plus the stage-4 files; `plan:399` enumerates the six stage-4 files. None of Tasks 27–30 modifies the two code files. `spec:845` expressly identifies both as unrelated/out of scope. A permissive interpretation of “scale-map rows” might inspire an executor to add the code-assigned family to the allow-list, but the task's stated list does not tell them to do so; the required passing result at `plan:397` needs that scope correction, not edits to unrelated code.

### (c) Variant 2 F7: own-edit line movement and hooks path

**Stance: keep the missing-path defect as blocking; qualify the universal line-movement claim.**

The multiline digest is not a same-length replacement for the three legacy definition bullets: the full block is `spec:195-207`, with fence requirements at `spec:193`, while Task 26 replaces/moves the old bullets (`plan:316`). A straightforward edit shifts the old cap and own-model lines. However, `plan:320` says their words are unchanged; that can be checked by content rather than treating the historical numbers as array indexes. Likewise, Task 21's literal “grep ... prints lines 252 and 361” (`plan:266`) is an unnecessarily fragile numeric check, but the brief additions can be written on existing lines. Task 22's new Gate 5 step can be appended as text to an existing line; the actual cap-content check (`plan:277`) need not depend on final coordinates. Therefore V2 has not proved that all valid implementations must break all of these pins.

The root hooks path is different. I attempted to Read `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/hooks/hooks.json`: it does not exist. Glob found the source file and a plugin copy (plus generated/environment copies), not a root file. I Read `src/superclaude/hooks/hooks.json:169-175`; line 173 registers `node "$HOME/.claude/hooks/pragmatic-subagent.js"`. Thus the literal root-relative command required by `plan:321` fails regardless of how the Markdown is reflowed. The answer to “root or only src?” is **not at root; source and plugin copies exist**, not “only src”.

### (d) One-pass Phases 1–3 versus owner go before the scaffold

**Stance: yes, Variant 1 F5 establishes a blocking transition error.**

`plan:20` maps Phases 1, 2 and 3 to stages 0, 1 and 2, says they “can run in one pass”, and only tells the executor to wait for owner go before Phases 4 and 5. `spec:945` instead requires “stage 0 result written; owner go” before stage 1, and `spec:940` requires the owner to have seen the numbers before a stage starts. Phase 2 Task 6 depends on Task 5, with no owner stop (`plan:84-90`). The explicit one-pass authorization therefore permits creating the scaffold after measurement without the required informed owner approval. A later pilot approval does not catch or undo that already-crossed boundary; general adoption of recommendations at `plan:21` does not provide owner review of numbers that have not yet been produced.

### (e) Blocking findings from both cards under the brief's rule

These are **finding-level decisions**, with overlapping findings listed under both source cards but not counted twice as distinct defects.

#### Variant 1 — keep as blocking

| Finding | Why it meets the rule; later-step check |
|---|---|
| **V1 F1** | Task 7's mandatory canonical fence (`plan:104`) lacks a Task 11 row (`plan:146`), so the reverse scan rejects it (`plan:237`); strict final activation (`plan:459`) does not register or exempt it. This is an unsatisfiable final acceptance requirement as written. |
| **V1 F2** | Task 35 explicitly permits a pointer-only v2 carrier (`plan:416,419`) while T1 requires its digest (`plan:237`). No later task inserts that missing source digest before the mandatory final T1 run (`plan:459,462`). |
| **V1 F3** | Task 30 requires updating a task-skill row absent from Task 11 and prescribes no digest insertion (`plan:146,361`). Adding a row alone cannot satisfy T1 (`plan:237`), and no later task supplies both missing pieces. |
| **V1 F4** | An enabled task-skill final sweep has no call in its integration (`plan:250,261,361`), unlike tech-research (`plan:273`). The helper unit test at `plan:253` does not catch missing task-skill reachability, so an open Medium entering the final decision basis can escape the required GR7 promotion (`spec:653`). |
| **V1 F5** | The one-pass instruction crosses the stage-1 owner boundary before approval (`plan:20`; `spec:940,945`); later pilot/propagation gates do not repair that earlier unauthorized transition. |
| **V1 F6** | The required fresh-findings evaluation (`plan-input:16`) has no producing task: Tasks 3–4 use the historical table and retrospective minor sample (`plan:54,66`), and the classifier tests are fixtures/properties (`plan:192`). New shadow disagreements are not an independently scored fresh evaluation, and no later task requires producing that second result. |

#### Variant 2 — keep as blocking, narrowed where stated

| Finding | Why it meets the rule; later-step check |
|---|---|
| **V2 F1** | The Task 33 scan must pass (`plan:397`) but its named allowed files omit preserved trigger-bearing code (`plan:394,399`; `src/superclaude/cli/pipeline/fmea_classifier.py:304`; `src/superclaude/cli/roadmap/remediate_parser.py:55`). Later tasks do not add those code files to the allow-list or remove their out-of-scope phrases. |
| **V2 F2** | Same verified registry/digest contradictions as V1 F2 and F3 (`plan:146,237,361,416,419`), not a third distinct defect. |
| **V2 F3**, count corrected | Specific label-based FAIL instructions remain after the qualitative agent's v2 edit (`src/superclaude/agents/rf-qa-qualitative.md:240`; `plan:340`). The inventory does not match their wording (`plan:32`), and Task 32 re-pins Rule 6 rather than these verdict pairs (`plan:383`); neither necessarily catches their over-blocking behavior. |
| **V2 F5** | The tech-research offer and both carriers' escalation-halt offer are not wired (`plan:261,273`) despite explicit requirements (`spec:323,946`; adoption `plan:21`). No later integration task adds them, so following the listed edits can finish or halt without the required offer. |
| **V2 F7**, missing-path limb only | The mandatory Task 26 root-relative hook grep names a nonexistent target (`plan:321`); the real source registration is `src/superclaude/hooks/hooks.json:173`. No later task repairs that executable acceptance command. |

#### Variant 2 — do not keep as blocking under this rule

- **F4:** keep the missing input-availability counts as a non-blocking completeness finding; do not claim mandatory unsupported M/C/E calls or classifier authority when `plan:23,135,197` explicitly forbid them. Lack of one additional acceptance check does not force the wrong behavior described by the card.
- **F6:** keep the unassigned recall/audit work and missing planted-set sizing as a qualified handoff concern, not proof of an uncaught unsafe pilot. `plan:20` already blocks Phase 4 when recall is absent and Phase 5 before the pilot audit window. This differs from V1 F6: the missing fresh classifier evaluation has no equivalent explicit later stop. A complete operational handoff should identify who supplies the externally gated recall/audit evidence; the current card should not recast that prerequisite as an automatic waiver or guaranteed false pass.
- **F8:** not demonstrated; the Task 24 assertion is explicitly stage-bound (`plan:295,299`).
- **F9:** wording and unused allow-list cleanup (`plan:150,399,405-410`), not a forced wrong result.

## Closing position

Use Variant 2's repository-grounded additions together with Variant 1's dependency-chain findings. Preserve the explicit stage boundary in Task 24, distinguish content preservation from numeric grep pins, and do not treat missing extra tests as proof that a compliant executor violates an existing constraint. The merged blocking set is the two tables above, with the registry overlap de-duplicated and V2 F3's count corrected to eight pairs.

Verification limits: this was a static Read/Grep/Glob review; I ran no tests and changed only this statement. Claims about future agents' observed compliance or actual pilot metric values are not established here; V2's prediction that M12 necessarily shows no change is [UNVERIFIED].
