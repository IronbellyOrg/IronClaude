# Command nuance: /sc:release-split

**Generated**: 2026-10-27 by nuance agent (read-only; only this file written). No command was run.
**Brief**: `command-nuance/_brief.md` (R = multi-feature release; `/sc:task` and `/sc:tasklist` retired; `/sc:implement` has no `--depth`).
**Protocol skill**: exists at `/home/coder/.claude/skills/sc-release-split-protocol/` (SKILL.md plus refs/adversarial-integration.md, phase-templates.md, verification-protocol.md). All four files read in full.
**Citation key** (all under `/home/coder/.claude` unless noted; line numbers from Read in this session):

| Tag | File |
|---|---|
| CMD | `commands/sc/release-split.md` |
| SK | `skills/sc-release-split-protocol/SKILL.md` |
| AI | `skills/sc-release-split-protocol/refs/adversarial-integration.md` |
| PT | `skills/sc-release-split-protocol/refs/phase-templates.md` |
| VP | `skills/sc-release-split-protocol/refs/verification-protocol.md` |
| ADV | `skills/sc-adversarial-protocol/SKILL.md` (grep only, depth lines) |
| HW | `HOW-WE-WORK.md` |
| TB | `skills/task-builder/SKILL.md` |
| CV | `command-value-by-phase.md` (brainstorm folder) |
| VF | `validation-feature-task-builder-vs-sc-workflow.md` (brainstorm folder) |
| SC | `scenarios.md` (brainstorm folder) |

<!-- SECTION 1 -->
## 1. Status and role
- **Does**: "Neutral two-phase release split analysis with adversarial validation and fidelity verification" (CMD:3). Four parts: Socratic discovery via `/sc:brainstorm`, competing proposals via `/sc:adversarial` Mode B, execution via `/sc:design` | `/sc:workflow` | `/sc:tasklist`, fidelity audit (CMD:64; SK:101-107). It never executes the resulting plans or touches git (CMD:122-123).
- **Phase and invocation**: Spec phase, after the PRD/TDD and before the roadmap or tasklist step; optional step 6 of the full-spec route (HW:70-72, HW:309). Standalone-invokable by a user (CMD:19); the protocol skill is loaded by the command only (SK:20). Not retired.
- **Overlaps**: `/sc:brainstorm` and `/sc:adversarial` (it calls both inside Parts 1-2), `/sc:reflect` (both are coverage checks, different inputs), `/roadmap` and `/task-builder` (downstream). **Retired neighbour**: `/sc:tasklist` is offered as a Part 3 option (CMD:136; SK:35, 105, 272). Never take that option. `/sc:task` is not referenced anywhere in the command or protocol (grep).

<!-- SECTION 2 -->
## 2. Flags
Every flag is in CMD:50-60 and in the SK argument-hint (SK:5). Short forms (`-o -d -i -a`) exist only in CMD, not in SK.

| Flag | Values | Default | What it changes (cited) | Worth using | Avoid |
|---|---|---|---|---|---|
| `<spec-file-path>` | path to spec, roadmap, tasklist or refactor plan (`.md/.yaml/.yml`) | required | STOP if missing, empty, or <3 extractable requirements; WARN if >500 lines (chunked) or if it looks like a tasklist (asks to confirm) (SK:77-88, 130). | Pass the release-level spec/TDD (HW:72 passes the TDD). | Passing a tasklist: the split comes after the work was already broken into steps. |
| `--output`, `-o` | directory | `<spec-dir>/release-split/` (CMD:53) | Where all artifacts go. Refused before any write if under `.claude/skills/`, `.claude/agents/`, `.claude/commands/` (SK:132). | Point it at the release's own folder, e.g. `.dev/releases/current/<release>/release-split/` (this repo keeps `.dev/releases/current/v2-m2/`). | The three forbidden prefixes. |
| `--depth`, `-d` | `quick` `standard` `deep` | `standard` (CMD:54) | Only documented effect: passed to `/sc:adversarial` in Part 2 (SK:205), where it sets debate rounds 1/2/3 (ADV:334) and `quick` skips Round 2 (ADV:1083). Retry after a Part 2 failure uses `quick` (SK:244). CMD:54 calls it "Analysis depth" but no text applies it to Part 1 (SK:161 passes only `--interactive` to brainstorm) or Part 4. | `deep` for R-HIGH (J); `quick` when the seam is already obvious (J). | Expecting it to deepen the fidelity audit: not stated anywhere. |
| `--interactive`, `-i` | bool | false | Pause after Part 1 (SK:180-182) and Part 2 (SK:256); prompt on NOT VERIFIED (SK:368); the only way to accept convergence 0.50-0.59, otherwise abort (SK:224, 436). Passed on to brainstorm and adversarial (SK:161, 206). | Always at R-MEDIUM and above: the split is a human decision and low convergence aborts without it (J). | Unattended or scheduled runs: it blocks on prompts. |
| `--resume-from` | path to a proposal | none | Skips Parts 1-2; the file is read as the validated proposal and Part 3 starts (SK:120; CMD:34). Only check is that the file exists and is readable (SK:138). | Restart after a crash, or after a human edited `split-proposal-final.md`. | Feeding a hand-written file as "validated": nothing verifies it was adversarially validated (UNVERIFIED gap). |
| `--no-split` | bool | false | Skips Parts 1-2; Part 3 writes a single-release validation spec; Part 4 audits it (SK:122). No split analysis happens at all. | Cheap path when the engineer already decided "one release" and wants a coverage audit. | Treating its output as evidence that a split was considered: no `split-proposal*.md` is produced (SK:50-55 lists them only for the analysed path). |
| `--r1-scope` | `fidelity-schema` `minimal-viable` `custom` | `fidelity-schema` (CMD:58) | Bias for what Release 1 contains (SK:175). Default means "planning fidelity and schema hardening only" (SK:63). `custom` prompts the user for guidance (SK:175). Matters only if a split is proposed. | `minimal-viable` for a feature release (smallest independently valuable subset) (J). | Leaving the default on a release that is not about planning or schemas: it was written for pipeline-planning releases (J, SK:33, 63). `custom` in unattended runs. |
| `--smoke-gate` | `r1` `r2` | `r2` (CMD:59) | Puts the smoke gate in Release 1 or Release 2 (SK:176, 285, 291). "Smoke gate" is not defined in any of the four files read. | `r1` only when a live post-deploy check is itself what R1 must prove (J). | Using it without agreeing what the gate is (UNVERIFIED meaning). |
| `--agents`, `-a` | `model[:persona[:"instruction"]]`, comma list | `opus:architect,sonnet:analyzer` (CMD:60; SK:92) | Number and mix of Part 2 variant generators; 2-10 allowed; unknown model stops the run (SK:134-136); presence selects adversarial Mode B (SK:94). Persona hints in PT:33-38 (`security`, `qa` listed). | Add `sonnet:security` when the split would divide auth, secrets or access changes (PT:37). | Going above the default without a reason: no cost data exists in the files. Conflict: AI:33 lists the default second agent as `haiku:analyzer`. |

**Does not exist** (not found in CMD, SK or the three refs): `--spec` (the artifact is positional), `--split` or any force-split (only `--no-split`), `--yes` or auto-approve of low convergence (needs `--interactive`), `--handoff` (Part 3 picks the command itself, SK:266-275), `--dry-run`, `--mode`, `--resume` (the flag is `--resume-from`).

<!-- SECTION 3 -->
## 3. Scope x complexity matrix
**Does the command vary by complexity?** Yes, but only where a release artifact with real seams exists (R, and the top of F and N). At T, B and S it does not vary: there is no release artifact, and the protocol STOPs under 3 extractable requirements (SK:83, 427). Per Ruling 2, a single feature's release is a phase inside S or F, so S never needs this command.

**Band definitions for this command** (no file gives thresholds; anchors are real, the cut-offs are JUDGMENT):

| Band | Signals (all (J) cut-offs) | Anchor |
|---|---|---|
| LOW | 2-3 features, one subsystem, files nameable up front, independent features, release artifact short, no risk class touched, no open decisions. | HW:17, TB:2410-2441 (subsystem = first 2 path segments) |
| MEDIUM | 3+ features across 2+ subsystems, or shared interfaces between features; multi-session; a driving spec/TDD exists; part of it could be proven live before the rest. | HW:18; TB:2410-2441 (TCS 13-34) |
| HIGH | Cross-subsystem plus risk (secrets, permissions, infrastructure, paths), drift-sensitive, release artifact over 500 lines (the protocol's own chunking WARN, SK:87), live validation costly or hard to undo, or any constituent task file at TCS >= 35. | SK:87; TB:2410-2441; HW:22 |

**Matrix** (`(J)` = my judgment, not a file's statement; flags in brackets):

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | SKIP | SKIP | SKIP |
| B bug fix | SKIP | SKIP | SKIP |
| S single story | SKIP | SKIP | SKIP |
| F multi-story feature | SKIP (J) | SKIP (J): phases inside the task file already sequence the work | OPTIONAL (J) [`--interactive --r1-scope minimal-viable`] only when a full spec exists (HW:20, 70) and there is a foundation-versus-application seam (SK:159) |
| R multi-feature release | SKIP (J): ship the features as separate F items | WORTH IT (J) [`--interactive --r1-scope minimal-viable`] | WORTH IT (J) [`--depth deep --interactive --r1-scope minimal-viable`; add `--agents opus:architect,sonnet:analyzer,sonnet:security` if auth/secrets split] |
| N new product | SKIP (J) | OPTIONAL (J) | OPTIONAL (J) [`--interactive`; run on the first release's spec]: `/roadmap` phases are already "independently deployable" (HW:75) |

No cell is REQUIRED: HW calls the step optional (HW:309 step 6, "(optional)"; HW:70), the protocol itself says "do not split" is always valid (SK:31, 61), and no file marks it required. REQUIRED would make a checker flag every legitimate "keep it as one release" decision that skipped the command.

<!-- SECTION 4 -->
## 4. Choose this or the neighbour
| Neighbour | Choose `/sc:release-split` when | Choose the neighbour when | Source |
|---|---|---|---|
| `/sc:brainstorm` | The question is "should this release be split, and where". Part 1 already runs brainstorm on that question (SK:149-161). | The idea or requirements are still unclear (HW:151). Do not run brainstorm first on the same split question. | HW:310; SK:149 |
| `/sc:adversarial` | You have one release artifact and want a decision. Part 2 runs adversarial Mode B itself (SK:190). | You already hold two or more competing drafts: `/sc:adversarial --compare a,b` (HW:314). | HW:152, 314 |
| `/sc:spec-panel` | The spec is already agreed and the question is shape. | The spec quality is the question. Release-split does not critique; Part 4 only checks the split outputs against the original (SK:330-363). Run spec-panel first (HW:309 steps 3 and 5). | HW:309 |
| `/sc:reflect --mode pre` | Input is a release spec and output is two specs (spec versus spec fidelity, VP:11-141). | Input is a tasklist or task file and the question is spec coverage (HW:192-194). Neither replaces the other. After a split, `/task-builder --spec <release-1-spec>` produces its own `reflect_pre` (VF:92-95). | VP; HW:192 |
| `/roadmap`, `/task-builder` | Never as a substitute: this command ends at specs and an audit (CMD:123). | Always next. If split: the Release 1 spec replaces the TDD in the roadmap step and Release 2 is not planned until Release 1 is built and validated (HW:72; SK:65, 290). If not split: continue with the original or `release-spec-validated.md`. | HW:72-77 |
| `/sc:design` (Part 3 default) | Part 3 needs release specs: this is the protocol's default (SK:268-275). | `/sc:design` is a single-pass draft of one interface (HW:244; CV:65). For a full release spec, a person or `/tdd` is the better author (J). Protocol fallback is writing the specs inline (SK:430). | SK:268-275; HW:244 |
| `/sc:workflow` (Part 3 option "execution workflow") | Do not pick it for a multi-feature release. | Not eligible as the minimum tasklist step for a multi-story feature (VF:11); use `/task-builder --spec`. | SK:270; VF:11 |
| `/sc:tasklist` (Part 3 option "tasklists") | **Never.** Retired (Ruling 3). The protocol names it at SK:272 and CMD:136, but SK:275 already says not to use it unless the proposal says so. | Tasklist step after the split: `/task-builder` per feature (or `/roadmap`). | SK:272, 275; brief Ruling 3 |
| BMad milestone planning (`bmad-correct-course`, `_bmad-output/planning-artifacts/roadmap.md`) | Task-file lane releases. | BMad lane. This repo shows the milestone route in use: `.dev/releases/current/v2-m3/00-revised-plan.md` (method `bmad-correct-course`) re-scoped a milestone. A milestone plan is a recorded split decision made without this command (J). | observed on disk |
| `/sc:post-release` | Before the tag: decides how to cut the release. | After the tag: documents and e2e-tests what shipped (CV:186). Release 2's gate (R1 "passed real-world validation", SK:290) may use the same evidence (J). | CV:186 |

<!-- SECTION 5 -->
## 5. What a scheduled checker can see
All paths below come from the protocol's own templates. Nothing was observed by running it. **Observed absence**: a search of this worktree (`.dev/`, `docs/`, and the whole repo for `split-proposal*`) found no `release-split/` folder and no split-proposal file, and no mention of the command in `.dev/releases`, `.dev/plans` or `docs/`. So the footprint has never been seen in this repo.

Output folder: `<spec-dir>/release-split/` by default (CMD:53; HW:72 example `docs/billing/release-split/`), or `--output`. It is not under `.dev/tasks/`, and the command does not manage git (CMD:123), so files are untracked until a person commits them.

| Run shape | Files present | Key markers | Source |
|---|---|---|---|
| Any complete run | `fidelity-audit.md`, `release-split-report.md` | `## Verdict:` in the audit is `VERIFIED` / `VERIFIED WITH REQUIRED REMEDIATION` / `NOT VERIFIED` (VP:198); the report's `## Verdict: [SPLIT / NO SPLIT]` (SK:381). | SK:370-402; VP:193-248 |
| Analysed path (default) | `split-proposal.md`, `split-proposal-final.md` | Final proposal frontmatter `adversarial:` with `agents`, `convergence_score`, `base_variant`, `artifacts_dir`, `unresolved_conflicts`, `fallback_mode` (SK:232-242). `convergence_score >= 0.6` passes. | SK:178, 252 |
| Split outcome | `release-1-spec.md`, `release-2-spec.md`, `boundary-rationale.md` | Spec frontmatter `release: 1\|2`, `parent-spec`, `split-proposal`, `scope`, `status: draft`; Release 2 carries `validation-gate: blocked until R1 real-world validation passes` and a "Planning Gate" section (PT:124-132, 165-171). | SK:41-48, 306-310 |
| No-split outcome | `release-spec-validated.md` | Frontmatter `split-analysis: "no-split-recommended"`, `status: validated` (PT:211-217). | SK:50-55, 312-314 |
| `--no-split` or `--resume-from` | No `split-proposal*.md` from this run | Parts 1-2 were skipped (SK:120-122). | SK:120-122 |
| Debate evidence | Adversarial artifacts folder | Location "inferred from `--output`" (AI:98); exact path UNVERIFIED. | AI:98 |
| Transcript only | Skill calls `sc:release-split-protocol`, `sc:brainstorm`, `sc:adversarial-protocol`, then `sc:design` and/or `sc:analyze` | Visible only in a session log. | SK:105-107 |

Count mismatch for a parser: CMD:64 says 4-6 artifacts; SK:41-55 lists 6 (split) or 4 (no split) but SK:402 also writes `release-split-report.md`, so a complete run has 7 or 5 files. A checker should key on the verdict headings, not on a file count.

<!-- SECTION 6 -->
## 6. Expected-step rule
**Rule (J except where cited):**
- T, B, S, F-LOW, F-MEDIUM, R-LOW, N-LOW: never expected. Its absence is never a skipped step.
- R-MEDIUM, R-HIGH (and F-HIGH, N-MEDIUM, N-HIGH, weaker): expected is "a recorded split or no-split decision", not necessarily this command. Accept any of: `release-split/` outputs, a milestone or revised-plan document that states the scope cut (this repo's `v2-m3/00-revised-plan.md` is one), or an explicit one-release statement in the release plan. If none exists at R-MEDIUM or above, report it as informational, not as a failed step: no file makes the command required (HW:309 "optional"; SK:31).
- If the command did run: expect `fidelity-audit.md` with a verdict. `NOT VERIFIED` means the split should be revised or abandoned (SK:366; VP:77), so a roadmap or task-builder run on the output without a fix is a finding.

**What "do not split" means for expected steps** (the ask in the lead's message):

| Outcome | Steps of the command itself | Downstream expectation | What the checker must not flag |
|---|---|---|---|
| Ran, result "do not split" (valid at every part, CMD:64; SK:61) | All four parts still happened; five files exist (`split-proposal.md`, `split-proposal-final.md`, `release-spec-validated.md`, `fidelity-audit.md`, report). | The release continues as one release: every feature in it follows its own F pipeline (spec, `/task-builder --spec`, `/task`, commit, `/code-review`, push), then release-level review and `/sc:pr-submit`. "No split" shortens nothing downstream. | Missing `release-1-spec.md` / `release-2-spec.md`; missing `boundary-rationale.md`. |
| Ran, result "split" | Seven files (SK:41-48, 402). | Two sequential releases, each its own R-sized (or smaller) piece of work. Release 1 goes down the normal pipeline using its spec in place of the TDD (HW:72). Release 2 must not have a roadmap or tasklist until Release 1 is built, validated and reviewed (SK:65, 290; VP:108-121). | Release 2 pipeline artifacts absent for days or weeks after Release 1 ships. A checker window must not time out Release 2. |
| Ran with `--no-split` | Parts 3-4 only; no proposal files. | As "do not split", but no split analysis exists. | Missing split-proposal files. Do not count it as evidence a split was considered (J). |
| Did not run | None. | Same as "do not split" if the engineer kept one release; same as "split" if the plan shows two releases (milestones). | Absence (see rule above). |

**Violation the checker can look for**: a Release 2 roadmap, task file or tasklist whose date precedes the Release 1 validation evidence. Detect via Release 2 spec frontmatter `validation-gate` (PT:131) and the dates of Release 1 validation artifacts. How Release 1 validation evidence is recorded is UNVERIFIED (see Section 8).

<!-- SECTION 7 -->
## 7. Proposed changes to command-value-by-phase.md
Line numbers are in CV. Proposals only; CV was not edited.

**R re-rating summary.** Headline R stays WORTH IT, but it changes in meaning and now depends on complexity. Old reading (CV:139): "a release assembles and ships work already built at story or feature size", which makes R a thin wrap-up of three commands (CV:256). New reading (Ruling 2): R is a multi-feature release with its own plan, implementation and push. Under that reading this command is not a late add-on: it sits at the head of the R lane, before any tasklist is written, and answers the question "one release or two". Band effect: R-LOW SKIP, R-MEDIUM and R-HIGH WORTH IT (all (J)). Not raised to REQUIRED: no file makes it so (HW:309, SK:31).

| # | CV location | Current | Proposed | Why |
|---|---|---|---|---|
| 1 | CV:72 `/sc:release-split` row, R cell | `WORTH IT` | `WORTH IT` (R-MEDIUM and R-HIGH); `SKIP` at R-LOW (J) | Section 3 |
| 2 | CV:72, F cell | `OPTIONAL` | `OPTIONAL` only at F-HIGH with a full spec and a foundation-versus-application seam; `SKIP` otherwise (J) | A single feature's release is a phase inside F (Ruling 2); HW:70 targets "work too big for one release"; SK:159 |
| 3 | CV:72, N cell | `OPTIONAL` | `OPTIONAL` at MEDIUM/HIGH, `SKIP` at LOW (J) | `/roadmap` phases are already independently deployable (HW:75) |
| 4 | CV:72, Notes | `Guide step 6 of full-spec: optional; "do not split" is a normal answer. Judgment: WORTH IT only at release size` | `Spec-phase step 6 of full-spec (HW:309), optional. Input is a release spec/TDD/roadmap (not a tasklist). Runs brainstorm and adversarial itself: do not run them first for the split question. Output in <spec-dir>/release-split/. If split: R1 spec replaces the TDD in the roadmap step and R2 is not planned until R1 is validated (HW:72). Part 3 may offer /sc:tasklist (retired) and /sc:workflow (not the F minimum): take specs only. "Do not split" is a valid result and counts as the command having run. Use --interactive at R-MEDIUM and above.` | Sections 1, 2, 4 |
| 5 | CV:256 R row, "WORTH IT additions" | `/sc:release-split, /task-builder / /roadmap for release steps, ...` listed after the three-step minimum | Move `/sc:release-split` out of the tail and put it at the start of the R path as "optional step 0 (R-MEDIUM+): record a split or no-split decision". Note that the three-step R minimum (reflect post, code-review, pr-submit) assumes already-built work (CV:139) and must be rebuilt for the new R definition: per-feature F pipelines plus release-level review and push. That rebuild is outside this command | Ruling 2; Section 6 |
| 6 | CV:257 N row, "WORTH IT additions" | lists `/sc:release-split` | Add "(run on the first release's spec; R1 spec replaces the TDD in `/roadmap`)" | HW:72 |
| 7 | CV:114 `/sc:tasklist` Notes | "Same separate pipeline. `superclaude` is on PATH here ..." | Add: "Also offered as a Part 3 option by `/sc:release-split` (SK:105, 272; CMD:136). Retired: do not take that option." | Ruling 3; a second programmatic mention beyond Stage 9 |
| 8 | CV:110 `/sc:workflow` Notes | "... ‡ with `/task-builder`" | Add: "Also offered as a Part 3 option by `/sc:release-split` (SK:270): not eligible for a multi-feature release." | VF:11 |
| 9 | CV:266-276 footprint table | no row for release-split | Add row: `<spec-dir>/release-split/`: `split-proposal.md`, `split-proposal-final.md` (frontmatter `adversarial:`), then `release-1-spec.md` + `release-2-spec.md` + `boundary-rationale.md` (split) or `release-spec-validated.md` (no split); always `fidelity-audit.md` (`## Verdict:`) and `release-split-report.md`. Source: PT/VP/SK templates; never observed (none found in this repo) | Section 5 |
| 10 | CV:298 U14 "Whether the team tags versions" | UNVERIFIED | Partly resolved: `git tag -l` shows `aidev02-v1.0` (2026-06-22) and `aidev02-v2-m2` (2026-07-09), and `.dev/releases/current/v2-m2/post-release/` holds a `post-release-report.md`, so tagging and `/sc:post-release` are in use here. No release-split output exists anywhere in the repo | observed on disk this session |
| 11 | CV:229 area, or new O-row | none | New overlap row "Decide one release or two": `/sc:release-split` (task-file lane) versus milestone planning (`bmad-correct-course`, `roadmap.md`, BMad lane; this repo's `v2-m3/00-revised-plan.md`). Pick by lane (J) | Section 4 |
| 12 | `scenarios.md:40-41` (outside CV, for the merge step) | S6 lists "release split" among phases that run, "Allowed to skip: none" | Conflicts with HW:309 ("optional") and with CV. Change to "release split or an equivalent recorded split decision; skipping is fine for R-LOW" | HW:309; SC:40-41 |

<!-- SECTION 8 -->
## 8. Unverified items
| # | Item | Why unverified | What would resolve it |
|---|---|---|---|
| 1 | Every cell and band marked (J) | No file gives thresholds for this command (the TCS bands, TB:2410-2441, are for task-file audit depth, not for release splitting). | Team ruling |
| 2 | Footprint (Section 5) | Taken from templates; command never run (read-only) and no output exists in this repo. | One real run, or another engineer's output folder |
| 3 | Prerequisite 4 checks `src/superclaude/skills/sc-adversarial-protocol/SKILL.md` (SK:137) | That path does not exist in this repo (ls failed). The installed copy is at `~/.claude/skills/sc-adversarial-protocol/SKILL.md` (exists). A literal check would STOP "not installed"; how the agent resolves it is unknown. The check also has no condition, so it would apply to `--no-split` and `--resume-from`, which never call adversarial. | Run once |
| 4 | Default agents conflict | CMD:60 and SK:92 say `opus:architect,sonnet:analyzer`; AI:33 says the second default is `haiku:analyzer`. | Maintainers |
| 5 | Part 4 checklist size | SK:332 says "6-point"; VP:9 defines 8 checks (7 exact-contract strings, 8 intra-release ordering exist only in VP). SK:324 says `/sc:analyze` or inline; which is used is unspecified. | Run once |
| 6 | `--depth` outside Part 2 | No text applies it to Part 1 or Part 4 (SK:161 passes only `--interactive`). | Run once |
| 7 | `--no-split` path | Part 3 "No Split" reads "the no-split rationale" (SK:301), which does not exist when Parts 1-2 are skipped. Behaviour unknown. | Run once |
| 8 | "Smoke gate" | Used in `--smoke-gate` and four places in SK/AI, never defined. | Maintainers |
| 9 | Convergence thresholds | SK:223 uses 0.6; `sc-roadmap-protocol/refs/templates.md:321` lists `sc:release-split -> (0.7, 0.5)` and calls itself forward-looking with no consumer. Which wins at run time is not shown. | Run once |
| 10 | Whether `/sc:design` can author a whole release spec | CV:65 and HW:244 describe it as a single-pass draft of one interface. The protocol makes it the Part 3 default (SK:268-275). | Run once |
| 11 | Check 6 versus this repo's validation model | VP:123-140 rejects unit or integration tests and "automated test suites alone" as validation; repo `CLAUDE.md` says validation goes through `.github` Actions. Whether a CI live-validate run (workspace boot matrix, per `docs/generated/PROJECT_INDEX.md`) satisfies Check 6 or yields a false NOT VERIFIED is unknown. | Run once on a real release spec |
| 12 | How Release 1 "real-world validation" evidence is recorded for the Release 2 gate | The gate text exists (PT:165-171, VP:108-121) but no file says where evidence lives or who signs. | Maintainers; look at a real Release 2 spec |
| 13 | Which single artifact an engineer passes for a multi-feature release | HW:72 passes the TDD. This repo's release folders hold briefing, research, planning and TDD files (`.dev/releases/current/v2-m2/`) and no single release spec; BMad lane uses `epics`/`roadmap.md`. | Ruling on the input artifact per lane |
| 14 | Cost and agent count | No file states time, tokens or total agents (brainstorm agents plus at least 2 variants plus debate plus analysis). | Run once |
| 15 | Per-machine copies | Command and skill live in each engineer's `~/.claude` (Ruling 1); only this machine's copy was read. | Compare installs |

**Coverage statement.** Read in full: CMD, SK, AI, PT, VP, HW, CV, VF, `_brief.md`, SC (first 120 lines, which is the whole file's relevant part). Grep only: ADV (depth lines), `sc-brainstorm` command (flag lines), `sc-roadmap-protocol/refs/templates.md` (one line), task-builder TCS section (about 40 lines). Repo checks: `git tag -l`, `.dev/releases` listing, searches for `release-split` and `split-proposal*` (none found). No sc: command was run and no environment values were read.
