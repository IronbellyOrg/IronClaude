# Adversarial Debate Transcript

## Metadata

- Depth: standard
- Rounds completed: 2 (Round 1 parallel statements, Round 2 sequential rebuttals) plus Round 2.5 invariant probe
- Convergence achieved: 100% diff-point agreement (8 of 8), unanimous after Round 2; final status BLOCKED_BY_INVARIANTS (2 HIGH-severity UNADDRESSED invariants)
- Convergence threshold: 80%
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 3 (V1 sonnet:analyzer, V2 haiku:qa, V3 opus:refactorer)
- Model note: the pre-existing reviewer cards were the variants; each advocate was spawned on the model class that produced its card
- Advocate omissions of A-NNN responses: none (all three answered A-001 and A-002 in both rounds)

Round 1 and Round 2 statements below are condensed from each advocate's returned message (positions, evidence citations and per-point results preserved; prose shortened). Full originals were returned in conversation only.

## Round 1: Advocate Statements

### Variant 1 Advocate (sonnet:analyzer)

**Position.** V1 is the best card on correctness and coverage: only card with a real counterexample to the spec's blanket wording (a seed file that survives `--force`), only one that traced `force` through the code, and it flagged that acceptance criterion 2 can mis-fire.

**Steelman.** V2: a one-sentence spec really has no further requirement-bearing span, so "sound" is a legitimate outcome; its weakness is never testing the sentence's truth. V3: found the same wording gap with the same fix ("framework files"), is the only card to check fallout (installation.md:283/591, upgrading.md:56-60, README.md:75, tests); its anchor reasoning is correct.

**Strengths claimed.** (1) install_hooks.py:89-92 seed files deployed only when absent, "even with --force". (2) main.py:52 "--force is not forwarded" to the codegraph phase. (3) main.py:178-236 passes `force` to every installer; install_core.py:69 `if dest_file.exists() and not force`. (4) F3 partly valid. (5) Anchor lines right; README.md:75 redundant, not contradictory. (6) `git diff --word-diff -- README.md` check.

**Weaknesses in others.** V2 F2 calls criterion 2 falsifiable without testing it; V2 never checks the sentence's truth (self_confidence 0.97 vs blind 0.59). V3 F1 "leaves user-created files alone" is overbroad vs installation.md:593 (skill folders deleted and re-copied); V3 read docs only; V3 silent on criterion 2.

**Concessions.** install_hooks.py:250 does not support the "settings.json merged" claim (nearer line :404). "Files the installer does not manage are never touched" is imprecise given installation.md:593. F3's "staged .dev/tasks adds files to `git diff --stat`" is wrong as stated (unstaged diff does not list staged content). All three mislabel "none"-class findings `minor`.

**Per-point.** S-001 V1 55% | C-001 V1 65% | C-002 V1 70% | C-003 V1 90% | X-001 V1 70% | X-002 V1 70%.

**Shared assumptions.** A-001 QUALIFY (unstaged `git diff` misses staged/untracked content; scope the check). A-002 QUALIFY (only tests/docs/test_retired_docs_absent.py:39 reads README; assertions not read; run tests/docs after the edit).

### Variant 2 Advocate (haiku:qa)

**Position.** V2 is strongest on requirement coverage: the plan preserves every part of the request and its acceptance criteria describe observable checks. "Sound" is defensible as a coverage verdict but too strong as an overall correctness verdict: installer exceptions and the diff check's limits warrant notes, not invented missing requirements.

**Steelman.** V1: checked implementation behavior (install_core.py:66-75 copies when forced; install_hooks.py:89-95 preserves seed data) and the diff check's visibility. V3: keeps the remedy proportional ("framework files", README.md:75, upgrading.md:85-87) and avoids unnecessary changes elsewhere.

**Strengths claimed.** (1) INF-001 quotes the whole request; no unmapped requirement (tier1-card.md:11-16, plan:19-30). (2) Checkability claim is literally correct: wrong placement, missing command text or extra README hunks fail the criteria (plan:29-30); an imperfect check is not an unfalsifiable one. (3) Broad wording originates in the request itself, so it is a correctness note, not a missing requirement or executor drift (source.md:1).

**Weaknesses in others.** V1/V3 overstate preservation: install_skill.py:46-52 deletes the skill directory before re-copy (installation.md:593). V1 mixes valid diff concerns with wrong supporting arguments (staged changes do not appear in unstaged diff; a -/+ pair is expected by "one changed line"). V1's README-only check cannot show that no other file changed. V3's test argument supports low risk, not immunity (test_retired_docs_absent.py:37-49 checks links only).

**Concessions.** V2 did not validate installer behavior; core overwriting is real, seed data and merged settings make unrestricted wording imprecise. V2 conflates observable criteria with sufficient verification. 0.97 confidence excessive. All three cards put `minor` on `none`-class findings.

**Per-point.** S-001 tie 98% | C-001 V1 96% | C-002 V1 92% | C-003 V1 99% | X-001 V1 91% | X-002 tie 99% (neither preservation claim survives directory deletion).

**Shared assumptions.** A-001 REJECT (clean tree not established by the plan; untracked workflow artifacts already exist). A-002 QUALIFY (low risk for a plain sentence; the README-reading test checks links, not wording; proportional manual verification).

### Variant 3 Advocate (opus:refactorer)

**Position.** V3 is the one card that checked what the new sentence could break around it (other install docs, tests that read README.md). Its fix ("framework files") is right and matches README.md:75 and main.py:38, but its claim that `--force` "leaves user-created files alone" is false, and on code depth V1 beats it.

**Steelman.** V1 read the code (main.py:178-236, install_core.py:69, install_hooks.py:89-95, main.py:52), tested criterion 2 and proposes `git diff --word-diff -- README.md`. V2 does its coverage job: the spec has one requirement and plan:15 / plan:26 cover every part; on a change this small, "sound" is reasonable.

**Strengths claimed.** (1) "framework files" wording is consistent with README.md:75, main.py:38, upgrading.md:85-87. (2) settings.json is merged (main.py:213 "additive settings.json merge"). (3) Placement correct (README.md:55, :64; Upgrading block untouched). (4) No contradiction with README.md:75. (5) Fallout check verified: installation.md:283/591 and upgrading.md:56-60 agree; the only test reading repo-root README is tests/docs/test_retired_docs_absent.py:39-49, which checks links to retired files, so a link-free sentence cannot trip it.

**Weaknesses in others.** V2 F2: `git diff --stat` misses untracked and staged-only changes (plan:30); V2 verdict/confidence too high and never checks the sentence's truth. V1 F1 "installer does not manage are never touched" is wrong the same way: install_skill.py:47-48 `shutil.rmtree` deletes each shipped skill folder before re-copy (installation.md:593). V1's codegraph point does not bear on this sentence. V1 F3 "one removed plus one added" overstates.

**Concessions.** V3 F1 "leaves user-created files alone" is false (install_skill.py:47-48; install_skills.py:92-97 removes leftover `sc-*` folders). Evidence for F1 was docs-only. Silent on criterion 2. F5 is filler. The planned sentence understates what `--force` can destroy, and no card flagged that.

**Per-point.** S-001 V1 60% | C-001 tie 55% | C-002 V1 80% | C-003 V1 85% | X-001 V1 75% | X-002 V1 55% (both claims false per install_skill.py:47-48 and installation.md:593).

**Shared assumptions.** A-001 QUALIFY (check must also see staged and untracked files: `git status --porcelain` plus `git diff HEAD -- README.md`). A-002 ACCEPT (the one README-reading test checks retired links; a backtick-only sentence cannot break it; run `uv run pytest tests/docs` if a link is added).

## Round 2: Rebuttals

### Variant 1 Advocate rebuttal (sonnet:analyzer)

**Conceded.** F3's staged-files argument is wrong (plain `git diff` shows only unstaged changes; a one-line edit is always one insertion and one deletion, which "one changed line" expects). "Files the installer does not manage are never touched" is imprecise: install_skill.py:47-48 `shutil.rmtree` a shipped skill folder before re-copy (installation.md:593). install_hooks.py:250 does not support the "settings.json merged" claim (module docstring lines 4-5 and `_merge_settings` line 269 do).

**Rebutted.** C-002 still has a real defect in the opposite direction: plain `git diff --stat` cannot see staged or untracked changes, so the check can pass when another file changed; the repo rule says `.dev/tasks` is always staged. The F1 counterexample survives: seed data files are skipped when they exist even with `--force` (install_hooks.py:91-92, check at :554); settings are merged, not replaced (:188; :404 refreshes only framework-owned entries). V3 is wrong in the same way V1 was: "leaves user-created files alone" fails at install_skill.py:47-48; install_skills.py:92-97 also deletes stale `sc-*` folders whether or not `--force` is set.

**Planned sentence.** Not safe verbatim: it overstates (only shipped files are overwritten; seed data and settings.json are not) and understates (hides the skill-folder deletion and the lack of a backup, installation.md:593). V1 would accept: "`--force` overwrites the framework files it ships in `~/.claude` without a backup, and deletes and re-copies each shipped skill folder, so copy any edits first." Shortest acceptable form: "overwrites the framework files it ships in `~/.claude`" (matches README.md:75, omits the skill-folder deletion).

**Updated positions.** S-001 tie 60% | C-001 V1 55% | C-002 V1 60% | C-003 V1 90% | X-001 V1 55% | X-002 tie 65%. A-001 QUALIFY (cover staged and untracked files: `git status --porcelain` plus `git diff HEAD -- README.md`). A-002 QUALIFY (the real risk is a factually wrong sentence, which no test catches).

### Variant 2 Advocate rebuttal (haiku:qa)

**Conceded.** V2 never verified the sentence's truth: install_hooks.py skips existing seed data unconditionally even under `--force`; "sound" and 0.97 confidence were unjustified. Criterion 2 is insufficient: plain `git diff --stat` misses staged-only and untracked changes, so it can pass despite changes outside README.md; "checkable and falsifiable" hid that blind spot.

**Rebutted.** This is not a missing requirement: the request itself supplies the broad wording and the plan faithfully covers it; coverage and factual correctness are separate judgments. V1's original staged-files explanation was backwards, and a removal/addition pair is normal for an appended sentence. Neither preservation claim survives install_skill.py: forced installation deletes an existing shipped skill directory before copying it.

**Updated positions.** S-001 tie 99% | C-001 V1 96% | C-002 V1 95% | C-003 V1 99% | X-001 V1 95% | X-002 tie 99%. A-001 QUALIFY (before/after baseline covering staged, unstaged and untracked changes; separate existing workflow artifacts from task changes). A-002 QUALIFY (the README-reading test checks retired links, not sentence accuracy).

**Plan change.** Yes: change Task 1 and its first acceptance criterion to wording scoped to the framework files the installer ships. Yes: change criterion 2 to baseline-aware whole-tree verification plus inspection of the sentence-only README change.

### Variant 3 Advocate rebuttal (opus:refactorer)

**Conceded.** F1's "leaves user-created files alone" is false: install_skill.py:47-48 `shutil.rmtree` each shipped skill folder under `--force`; installation.md:593 says so (the docs were misread). Evidence was docs-only. Silent on criterion 2.

**Rebutted.** The "framework files" fix holds without the false clause: seed files skipped even with `--force` (install_hooks.py:85-92), settings.json merged not replaced. U-001 (other docs and tests) was not challenged. Correction for V3 and V1: install_skills.py:92-97 has no force check (stale `sc-*` folders are deleted on every install), so it does not belong in a sentence about `--force`.

**Updated positions.** S-001 tie 70% | C-001 V1 60% | C-002 V1 80% | C-003 V1 90% | X-001 V1 75% | X-002 tie 70%. A-001 QUALIFY (before/after baseline covering staged and untracked files). A-002 QUALIFY (changed from ACCEPT: no test can catch a factually wrong sentence).

**Proposed Task 1 sentence.** "Running `superclaude install --force` overwrites the framework files it ships that already exist in `~/.claude` without keeping a backup, and deletes and re-copies each shipped skill folder, so any file you added inside one is lost."

**Proposed criterion 2.** "Before the edit, record `git status --porcelain` and `git diff --cached --name-only`. After the edit, `git status --porcelain` differs from the baseline only by ` M README.md`, `git diff --cached --name-only` is unchanged, and `git diff --word-diff HEAD -- README.md` shows one hunk whose only change is the added sentence `{+...+}` at the end of the paragraph that starts 'This installs the package', with no `[-...-]` deletions."

Not checked by V3: the settings.json merge code itself; whether criterion 1 needs rewording.

## Round 2.5: Invariant Probe

See `invariant-probe.md`. 13 findings: 7 ADDRESSED, 6 UNADDRESSED (HIGH 2: INV-003, INV-012; MEDIUM 2: INV-001, INV-010; LOW 2: INV-007, INV-008). HIGH + UNADDRESSED items block convergence.

## Scoring Matrix

Winner per point after Round 2 (each advocate's final position; confidence is the mean of the three stated values, rounded):

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|------------|-------|--------|------------|------------------|
| S-001 | L1 | tie | 63% | All three label non-findings `minor`; no card is better structured on this point |
| C-001 | L2 | V1 | 70% | Seed-file counterexample is code-verified (install_hooks.py:89-95; main.py:52); V3 reaches the same wording fix from docs only |
| C-002 | L3 | V1 | 78% | Plain `git diff --stat` misses staged and untracked changes (V1 raised it; V2 and V3 conceded); V1's staged-files rationale was wrong and conceded |
| C-003 | L2 | V1 | 93% | main.py:178-236 and install_core.py:69 trace `force` to every installer; V3 relied on docs |
| X-001 | L3 | V1 | 75% | V2's "falsifiable" holds only trivially; V2 conceded in Round 2 |
| X-002 | L2 | tie | 78% | Both "left alone" claims fail: install_skill.py:47-48, installation.md:593 |
| A-001 | L3 | QUALIFY (3 of 3) | n/a | Check must see staged and untracked changes; V2's Round 1 REJECT moved to QUALIFY |
| A-002 | L2 | QUALIFY (3 of 3) | n/a | Only README-reading test checks links (tests/docs/test_retired_docs_absent.py:37-49); no test catches a wrong sentence; V3 moved from ACCEPT |

Positions moved in Round 2: V2 conceded it never tested the sentence's truth and that criterion 2 is insufficient; V3 conceded the false "leaves user-created files alone" claim; V1 conceded the staged-files argument and the "never touched" phrasing.

Not-converging flags: none on diff points. Oscillation: none.

## Convergence Assessment

- Points resolved: 8 of 8 (6 with a winner or a stated tie, 2 shared assumptions resolved to QUALIFY)
- Alignment: 100% (unanimous after Round 2)
- Threshold: 80%
- Taxonomy coverage: L1 = S-001; L2 = C-001, C-003, X-002, A-002; L3 = C-002, X-001, A-001. All levels covered.
- Invariant probe gate: **2 HIGH-severity UNADDRESSED invariants (INV-003, INV-012)**
- Status: **BLOCKED_BY_INVARIANTS**. Standard depth has no Round 3, so convergence is not declared. The refactor plan addresses INV-003 and INV-012 by construction, but no debate round tested that fix.
- Unresolved points: INV-003, INV-012 (HIGH); INV-001, INV-010 (MEDIUM, warning only)
