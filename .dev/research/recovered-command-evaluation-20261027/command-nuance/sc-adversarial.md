# Command nuance: /sc:adversarial

Written 2026-10-27. Brief: `command-nuance/_brief.md`. Focus: flags by number and size of competing artifacts; the point at which a debate is worth its cost.

## 1. Status and role

- **Does:** "Structured adversarial debate, comparison, and merge pipeline for 2-10 artifacts" (`~/.claude/commands/sc/adversarial.md:3`). Five steps: diff, debate, scoring and base pick, refactor plan, merge (`adversarial.md:76`). Backing skill exists: `~/.claude/skills/sc-adversarial-protocol/SKILL.md` (2998 lines, 128,257 bytes) plus `refs/` (4 files). Loading it is mandatory (`adversarial.md:145-149`).
- **Phase and status:** Spec (choose between competing drafts; `HOW-WE-WORK.md:152`, routing row `compare-options` at `:314`). Standalone-invokable, NOT retired. Not in Ryan's pipelines or in any HOW-WE-WORK level 1-6. Also runs INSIDE other commands (see section 4).
- **Overlaps:** `/sc:spec-panel` (critique of one spec), `/sc:brainstorm` (calls it in Wave 3), `/sc:reflect` and `/sc:troubleshoot` (call it in Tier 2), `/sc:release-split` (calls it in Mode B), `bmad-review-adversarial-general` (name only). `adversarial.md:182` lists the retired `/sc:tasklist` as a related command: never route to it.

**Complexity here is not code size.** It is: how many competing artifacts (N), how big they are together, and how costly a wrong pick is. Scope is only a proxy.

## 2. Flags

Citation key (all under `~/.claude/`): **AD** = `commands/sc/adversarial.md`; **SK** = `skills/sc-adversarial-protocol/SKILL.md`; **DP** / **AS** / **SP** / **AT** = `skills/sc-adversarial-protocol/refs/` `debate-protocol.md` / `agent-specs.md` / `scoring-protocol.md` / `artifact-templates.md`. "Observed" = counted on disk in this checkout on 2026-10-27: 32 `debate-transcript.md` files, of which 31 are in the `adversarial/` layout and 1 is a roadmap-CLI look-alike (section 5).

### 2.1 Every flag and argument

| Flag | Values | Default | What it changes | Worth using | Avoid |
|---|---|---|---|---|---|
| `--compare`, `-c` (Mode A) | 2-10 file paths, comma separated | none | Files copied to `adversarial/variant-N-original.md` (SK:62-63). Count 2-10 enforced; non-`.md` only warns (SK:561-563, 567). One advocate per file (SK:1031-1033) | You already hold the competing drafts (HOW-WE-WORK:152) | Fewer than 2 files (AD:171). Near-identical files (see 2.3) |
| `--source`, `-s` (Mode B) | one file path | none | Source for variant generation (SK:68-71) | No drafts yet, want N generated from one source | Idea still vague: use `/sc:brainstorm`, which wraps this (`brainstorm.md:133`) |
| `--generate`, `-g` (Mode B) | artifact type word (roadmap, spec, design...) | none | Only labels the generated artifact; callers use `spec` for everything (`skills/sc-release-split-protocol/refs/adversarial-integration.md`: "the `--generate` value only controls artifact labeling") | With `--source` | Alone: all three Mode B flags are required together (SK:575) |
| `--agents`, `-a` (Mode B) | `model[:persona[:"instruction"]]`, 2-10 specs | none | Each spec generates one variant AND is that variant's advocate (AS:195-196). All agents dispatched in parallel (SK:2204-2206) | Want model or persona diversity | Mixing with `--compare`: SK:555 says STOP, yet SK:1032 and AS:191 say Mode A "defaults to current model if `--agents` not specified" (see U1) |
| `--pipeline` | inline `"generate:a,b -> compare"` or `@file.yaml` | none | Routes to the DAG meta-orchestrator (SK:538-549). Mutually exclusive with Mode A/B flags | Multi-stage generate-then-compare with checkpoints | Anything a single Mode A/B call does. Observed: zero `pipeline-manifest.yaml` on disk |
| `--pipeline-parallel` | integer 1-10 | `3` | Max concurrent phases per DAG level (SK:2722-2723, 2742-2746) | Wide generate stages | Without `--pipeline` (no effect) |
| `--pipeline-resume` | flag | `false` | Re-reads `pipeline-manifest.yaml`, skips phases whose SHA-256 still match (SK:2821-2852) | Pipeline died mid-way | Edited artifacts: mismatch re-runs that phase and all downstream |
| `--pipeline-on-error` | `halt`, `continue` | `halt` | Failed phase marks dependents `skipped`; `continue` lets independent branches run (SK:2943-2993) | `continue` when branches are independent | `continue` when a compare phase would get under 2 inputs (it fails) |
| `--depth`, `-d` | `quick`, `standard`, `deep` | `standard` | quick = Round 1 only; standard = Rounds 1+2 and Round 2.5 invariant probe; deep = adds Round 3 only if convergence is still under threshold after Round 2 (SK:1083, 1111-1112, 1361-1364; DP:148-152). Unknown value warns and uses standard (SK:595-598) | The main cost lever (2.2) | `deep` on small or consensus-heavy inputs: Round 3 is conditional, so it often adds nothing |
| `--convergence` | 0.50-0.99 | `0.80` (callers pass 0.75: `brainstorm.md:58`) | Agreement bar for stopping, for Round 3, and for the stable-majority exit (SK:1441-1444, 1361). Out of range warns and uses 0.80 (SK:599-602) | Raise for decisions that are expensive to reverse (J) | Tuning it at `--depth quick`: DP:150 says no convergence check at quick |
| `--interactive`, `-i` | flag | `false` | Four `AskUserQuestion` pauses: after diff, after debate, after base pick, after refactor plan (SK:1911-1955) | Large N or stakes where you want to override the base | Unattended or scheduled runs; runs started by `/sc:reflect` or `/sc:troubleshoot` (they pass only what they set) |
| `--output`, `-o` | directory | "Auto-derived from input file directory" (SK:605-606; AD:69 says "Auto") | Artifacts go to `<output>/adversarial/` (SK:371-385). Refuses `.claude/skills/`, `.claude/agents/`, `.claude/commands/` before any write (SK:41) | Always set it to a `.dev/` path so the footprint is findable and committable | Leaving the default: output lands next to the first input file |
| `--focus`, `-f` | comma list | all | Injected into each advocate prompt as "Focus on these areas" (SK:981). No step is skipped by it in the protocol text | Narrow big artifacts to the risks that matter, e.g. `correctness,risk,test-coverage` (`sc-troubleshoot-protocol/SKILL.md:437`) | Expecting it to cut calls or tokens (UNVERIFIED, U2) |
| `--blind` | flag | `false` | Strips model names from artifacts before compare phases (SK:2856-2886). Spelled out only inside pipeline artifact routing | Mode B variants from different models, to stop brand bias | Same-model variants, or reviewer cards. Effect outside `--pipeline` UNVERIFIED (U3). Observed: no `blind/` dir anywhere |
| `--auto-stop-plateau` | flag | `false` | Pipeline halts when convergence moves under 0.05 for 2 consecutive compare phases (SK:2899-2926) | Long multi-compare pipelines | Anything else. By the algorithm it needs 3 compare phases (derived from SK:2915-2922) |
| `--dry-run` / `--pipeline-dry-run` | flag | `false` | Pipeline only: validates the DAG, prints plan and "Estimated Token Costs", runs nothing (SK:2546-2547, 2575-2580). **Not in the AD option table (AD:56-72)** | Only built-in cost preview | Mode A/B: no dry run exists |
| `--suspect-source` | file list | none | Named by `sc-bare-review` as the next step (`sc-bare-review/SKILL.md:3,18,55`). **No definition in AD, SK, or refs** (grep for "suspect" found nothing there) | Do not use until defined | Always (U4) |

### 2.2 Does not exist (people may assume)

`--rounds`, `--measure-first`, `--verdict-per-claim` (named as fabricated in `sc-recommend/SKILL.md:337`); `--proposals` (that is `/sc:brainstorm`, `brainstorm.md:48`); a flag to stop after Step 3 or skip the merge (none in AD:56-72 or SK:332-344: every full run writes `refactor-plan.md` and a merged output); a similarity-threshold flag (the 10% skip is fixed, SK:406-409); `--model`; a size cap or chunking flag (no size limit in the protocol); `--dry-run` for Mode A/B.

### 2.3 Cost drivers, by number and size of artifacts (derived from the protocol; counts are JUDGMENT)

| Driver | Text | Effect |
|---|---|---|
| Protocol load | SKILL.md is 128,257 bytes (`ls`). `sc-recommend` rule: do not load a protocol over about 2000 tokens for under about 500 tokens of work (`delegation-vs-native-heuristics.md:50`) | Fixed entry cost before any debate. At 4 bytes per token (J) about 32k tokens |
| Round 1 | N advocates in parallel, each gets its variant + ALL other variants + diff-analysis (SK:1022-1029, 1049-1055), `max_turns` 5 | Input grows about N x (total size of all variants): quadratic in N at fixed artifact size |
| Round 2 | N advocates, sequential, each reads all Round 1 transcripts (SK:1086-1092) | N more calls and wall-clock grows with N. Skipped at quick |
| Round 2.5 | one fault-finder over the consensus (SK:1111-1116) | One call. Skipped at quick. Observed: 12 `invariant-probe.md` files; of the 9 with a readable depth line, 6 are standard and 3 are deep, none quick (3 have no readable depth line) |
| Round 3 | N sequential, only when `deep` and still under threshold (SK:1361-1364) | Rare. Observed: 3 deep runs of 26 with a readable depth line |
| Scoring | 30-criterion rubric per variant, run twice (forward and reverse), disagreements re-judged (SK:1750-1773) | Grows with N and with disagreement |
| Plan + merge | one plan, one `merge-executor` (`max_turns` 10, SK:1973) | Roughly fixed per run, grows with merge size |
| Failure | one retry, then continue with N-1 (SK:401-404) | Hidden extra cost on flaky agents |
| Budget guard | protocol lowers depth itself (deep to standard, standard to quick) if it judges the run over budget (SK:494, 2241) | A checker may see a lower depth than requested |

**Cost references on disk:** `/sc:troubleshoot` Tier 2 with adversarial is ~30-60k Claude tokens, 8-15 min, versus ~15-30k, 4-7 min without (`sc-troubleshoot-protocol/SKILL.md:656-657`); so adversarial adds roughly 15-30k tokens and 4-8 min on small fix files (subtraction, derived). `/sc:reflect` Tier 2 is "+15-60k tokens, +4-15 min" for the whole tier (`reflect.md:145`). No file gives a standalone figure (U6).

**Observed sizes:** quick, N=2: variants 2.0-9.6 KB total, transcript 1.3-6.5 KB (e.g. `.dev/reviews/story-1-4-approach-debate-20260911/adversarial`). Standard, N=3: variants 38.5-117.8 KB total, transcript 2.4-30.8 KB (e.g. `.dev/brainstorms/20261022T011827Z-orca-upstream-tracking/adversarial`). Deep, N=2: 4.5 KB, 9.6 KB, 52 KB. Depth tally (26 of 32 transcripts have a readable depth line): quick 16, standard 7, deep 3. Largest N seen: 3.

### 2.4 Settings by number and size of artifacts

Only the first column of evidence is from files; the setting itself is JUDGMENT unless a cite says otherwise.

| N | Combined size | Setting | Evidence |
|---|---|---|---|
| 1 | any | do not run | AD:171 minimum 2 |
| 2 | small (observed quick runs 2-10 KB) | `--depth quick --focus <the one question>` | 16 quick runs observed; `troubleshoot` uses quick when proposals share one diagnosis and differ only in mechanism (`sc-troubleshoot-protocol/SKILL.md:441`) |
| 2 | medium to large (observed 20-100 KB) | `--depth standard` (default) | observed standard runs: top9-issues unified 97 KB, architectural patch 71 KB |
| 2 | decision shapes several stories or has no clean winner | `standard`, `deep` only if standard ends under threshold; add `--interactive` | observed deep: `claudedocs/orca-consolidation` 52 KB, `head-to-head` 9.6 KB |
| 3 | small | `--depth quick`: one round, no rebuttal | observed: `i263/reflect-post` N=3 at 2 KB |
| 3 | medium to large (observed 38-118 KB) | `--depth standard`; this is the `/sc:brainstorm` default shape (3 proposals, opus/sonnet/haiku, `brainstorm.md:48,56`) | 5 brainstorm runs observed at N=3 |
| 4-7 | any | avoid by hand. Quadratic Round 1 input plus N sequential rebuttals. If forced, reduce to the best 3 first | `brainstorm.md:69-70` caps proposals at 2 for quick and 7 for deep ("cost guardrail"); no run above 3 observed |
| 8-10 | any | do not use | allowed by the protocol (SK:561-563); no run observed; never as a way to "get more opinions" |

### 2.5 When the debate is worth its cost

Run it only when ALL hold; otherwise do not (rules 1-3 are file statements, 4-5 are JUDGMENT):

1. Two or more genuinely competing artifacts exist or will be generated (AD:171; HOW-WE-WORK:152).
2. They disagree on substance. Under 10% difference the protocol skips the debate and scoring and keeps the first file as base (SK:406-409, 944-948, 2164-2171), so you paid the load and diff cost for no decision.
3. The caller's own rule: debate only when there are at least 2 competing strong proposals, never on consensus ("that wastes the debate", `sc-troubleshoot-protocol/SKILL.md:596`).
4. A wrong pick is costly to reverse: it sets an interface other stories build on, a release scope, or an architecture (J).
5. No cheaper tool answers it: one artifact to critique is `/sc:spec-panel`; a vague idea is `/sc:brainstorm` (J).

## 3. Scope x complexity matrix

**Precondition for every non-SKIP cell:** at least 2 genuinely competing artifacts exist or will be generated (AD:171). With fewer, every cell is SKIP. No file maps adversarial to scope or to the task-builder TCS (`task-builder/SKILL.md` ~2410-2441 drives `/sc:reflect --depth`, not this command). The matrix is therefore JUDGMENT throughout, anchored on the observed runs in 2.3.

**Bands (all thresholds JUDGMENT; anchors are observed sizes):**

- **LOW:** N=2, combined size under about 10 KB (observed quick runs), decision reversible inside one story, no shared interface, files nameable.
- **MEDIUM:** N=2-3, about 20-120 KB (observed standard runs), decision shapes a feature design or a spec, or touches an interface two stories share, a driving spec exists.
- **HIGH:** N=3 or more, or over about 100 KB (largest observed 118 KB), or "must not drift" / infrastructure / secrets / permissions risk (HOW-WE-WORK:18), or a standard debate ended under the convergence bar.

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| **T** one-off | SKIP (J) | SKIP (J) | N/A (weighing two designs is not a level-2 job, HOW-WE-WORK:22) |
| **B** bug fix | SKIP (J) | SKIP (J): `/sc:troubleshoot` Tier 2 runs the debate itself when it has 2+ competing strong fixes (`sc-troubleshoot-protocol/SKILL.md:425-427`) | OPTIONAL (J): `--compare fix-1.md,fix-2.md --depth standard --focus correctness,risk,test-coverage`, only if troubleshoot did not already debate them (`adversarial_invoked` false, SKILL:525) |
| **S** single story | SKIP (J) | OPTIONAL (J): `--depth quick --focus <the disputed acceptance criterion>`. Precedent: `.dev/reviews/story-1-4-approach-debate-20260911` (N=2, quick, 8.9 KB) | WORTH IT (J): `--depth standard`, N=2 |
| **F** multi-story feature | SKIP (J): a short agreed spec file is enough (HOW-WE-WORK routing row `feature-existing`, :307) | OPTIONAL (J): N=2, `--depth quick`, or `standard` if the drafts exceed about 20 KB | WORTH IT (J): `--depth standard`; `deep` plus `--interactive` only if standard ends under the bar |
| **R** multi-feature release (re-rated, see 7) | SKIP (J) | OPTIONAL (J): `--depth standard` when two release plans or scope cuts compete | WORTH IT (J): `--depth standard --interactive`; normally reached through `/sc:release-split`, which calls it in Mode B with default `opus:architect` + `haiku:analyzer` (`sc-release-split-protocol/refs/adversarial-integration.md`, "Default Agent Configuration") |
| **N** new product | OPTIONAL (J) | OPTIONAL (J): `--depth standard`, N=2-3 competing PRD/TDD/roadmap drafts. No standalone N-scope precedent found on disk; the nearest file, `_bmad-output/planning-artifacts/debate-transcript.md`, is a look-alike (see section 5) | WORTH IT (J): `--depth standard` or `deep`, `--interactive`; for a vague idea start at `/sc:brainstorm`, which runs the debate for you |

**Does the command vary by complexity?** Yes, but along N, size and stakes, not code size. Flags that change with the band: `--depth` (quick to standard to deep), `--interactive` (HIGH only), `--focus` (narrow it as size grows), `--agents` (diversity only when Mode B).

## 4. Choose this or the neighbour

| Neighbour | Rule by signal | Cite |
|---|---|---|
| `/sc:spec-panel` | One spec to critique: spec-panel (`--mode critique`). Two or more competing drafts to pick or merge: adversarial. After a panel, adversarial may be run on the competing revisions | HOW-WE-WORK:150-152, routing rows `compare-options` / `critique-spec` (:314-315); `adversarial.md:180` |
| `/sc:brainstorm` | No drafts yet, idea vague: brainstorm. It runs adversarial itself in Wave 3 (Mode B, 3 proposals default, 2-7, quick caps at 2). Drafts already exist: `adversarial --compare`. Do not run both on one question | `brainstorm.md:48,69-70,133`; `sc-brainstorm-protocol/SKILL.md:258-281` |
| `/sc:reflect` Tier 2 | Reflect debates its own 2-3 reviewer cards (`--depth standard`, `--focus correctness,coverage,deviation-classification`). Never run adversarial on those cards by hand | `sc-reflect-protocol/SKILL.md:699-714`; `reflect.md:145` |
| `/sc:troubleshoot` Tier 2 | Troubleshoot debates 2+ competing fixes itself (quick if one diagnosis, else standard). Run adversarial yourself only on fix files written by hand | `sc-troubleshoot-protocol/SKILL.md:425-441,596` |
| `/sc:release-split` | Release split question: use release-split (wraps Mode B, 2 agents). Do not call adversarial for it | `sc-release-split-protocol/refs/adversarial-integration.md` |
| `/sc:roadmap` | The `superclaude roadmap run` debate is one LLM step, not this command; skill delegation is "inference-only". A `/sc:roadmap` run is not an adversarial run | `sc-roadmap-protocol/refs/adversarial-integration.md:11,31,82` |
| `/sc:swarm-wizard` / `sc-bare-review` | Other-model reviews can feed a compare, but the named flag `--suspect-source` is not defined by this command (U4) | `sc-bare-review/SKILL.md:3,18,55` |
| `bmad-review-adversarial-general` | BMad lane: reviews ONE artifact cynically and reports findings; adversarial compares 2+ and merges. Different jobs despite the name | repo `.claude/skills/bmad-review-adversarial-general/SKILL.md:3,5-9` |
| `/sc:tasklist` (RETIRED) | Named in `adversarial.md:182` as "Pipeline output as sprint input". Never run it; a merged document goes to `/task-builder` or `/sc:workflow` | brief ruling 3 |
| `/task-builder` (`--spec`) | (J) The merged output can serve as the `--spec` for the next step; requirement-bearing merges carry requirement-level provenance tags (DP:346-358). Adversarial neither validates domain correctness nor executes the result (AD:167-168), so a reader still checks it | `adversarial.md:165-168` |

## 5. What a scheduled checker can see

Footprint is real and committed: `git ls-files` lists 31 `adversarial/debate-transcript.md` files, equal to the 31 found in that layout, so they appear in PR diffs. Observed on 2026-10-27, not by running the command.

| Signal | Where | Cite / observation |
|---|---|---|
| Standard layout | `<output>/adversarial/` with `diff-analysis.md`, `debate-transcript.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md`, a merged output, and `variant-N-original.md` (Mode A) or `variant-N-<model>-<persona>.md` (Mode B) | SK:371-390; AT:1-346. Merged output is `merged-output.md` in most runs; the reflect runs write `merged-verdict.yaml` instead (`sc-reflect-protocol/SKILL.md:728`) |
| Default location | Next to the first input file when `--output` is not given | SK:605-606. So scan for `adversarial/debate-transcript.md` anywhere, not only under `.dev/`. Observed roots: `.dev/`, `claudedocs/`, `_bmad-output/brainstorming/` |
| Depth and N | `debate-transcript.md` metadata lines `- Depth:`, `- Rounds completed:`, `- Advocate count:`, `- Convergence achieved:` | AT:71-77; SK:1545-1553. Readable depth line in 26 of 32. Count `variant-*.md` for N. "Depth" is configured depth, "Rounds completed" is actual, so a budget downgrade (SK:494) shows as a mismatch |
| Depth proof | `invariant-probe.md` exists only for standard or deep | SK:1111-1112; observed 12 files, none from a readable quick run |
| Return contract | `return-contract.yaml` (fields `status`, `convergence_score`, `unresolved_conflicts`, `invocation_method`...) | SK:425-445 says it MUST be written; no file path is stated. Observed 14 files across 32 dirs, so absence proves nothing (U5). `convergence_score: null` is legal at quick (`story-1-4-approach-debate-20260911/adversarial/return-contract.yaml`) |
| Who invoked it | The parent folder | `.dev/brainstorms/<ts>-<slug>/adversarial/` = `/sc:brainstorm` Wave 3 (`brainstorm.md:193`); `.dev/troubleshoot/<name>-<ts>/adversarial/` = troubleshoot Wave 4 (`sc-troubleshoot-protocol/SKILL.md:438,443`); `.../reflect-pre/adversarial/` or `.../reflect-post/adversarial/` plus `merged-verdict.yaml` = reflect Tier 2 or a task-builder reflect gate. None of these is evidence that an engineer ran `/sc:adversarial` |
| Interactive use | `Approved by: auto` or `user` in `refactor-plan.md`; overrides recorded in the relevant artifact | AT:283; SK:1957-1959. Pauses themselves are transcript-only |
| Near-identical skip | Skip logged in `merge-log.md` | SK:2171 |
| Look-alike (do not count) | `_bmad-output/planning-artifacts/debate-transcript.md`, `base-selection.md`, `diff-analysis.md` | Sits beside `extraction.md`, `roadmap.md`, `roadmap-opus-architect.md`, `roadmap-sonnet-architect.md`; frontmatter `convergence_score` + `rounds_completed` matches the roadmap-CLI debate gate (`sc-roadmap-protocol/refs/adversarial-integration.md:49,57`); `base-selection.md` has `base_variant: B`, not the 50/50 scoring layout. So it is `superclaude roadmap run` output (inference, U9) |
| Pipeline mode | `pipeline-manifest.yaml` | SK:2753-2817. Observed: none |
| No footprint | Whether the command was merely considered and rejected; and `--blind`, `--focus`, `--agents` choices unless echoed in the transcript | transcript only |

## 6. Expected-step rule

- **Never count `/sc:adversarial` as an expected step at any scope or complexity.** It is in none of Ryan's five pipelines and in no HOW-WE-WORK level; its only routing row is the optional `compare-options` (`HOW-WE-WORK.md:314`). Absence is always fine, including at HIGH.
- **Count it only as "done right or half-done":** if an `adversarial/` folder exists, expect `diff-analysis.md`, `debate-transcript.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md` and a merged output; `invariant-probe.md` too when the transcript says standard or deep. Variants present but no `base-selection.md`, or a contract `status: failed` / `partial` with `unresolved_conflicts` above 0 that nobody addressed, is a finding. A run on near-identical inputs that skipped the debate and scoring (Steps 2-3, then a minimal merge, SK:2164-2171) is legal, so a thin `debate-transcript.md` or a missing `base-selection.md` is explained by a "variants substantially identical" line in `merge-log.md`. An `adversarial/` folder under brainstorm, troubleshoot or reflect belongs to that parent command's own rule, not to this one.

## 7. Proposed changes to command-value-by-phase.md

Proposals only; that file is not edited. Line numbers are from the file as read on 2026-10-27. A single-cell rating below is the MEDIUM band; HIGH lifts S, F, R and N to WORTH IT (matrix in section 3).

| # | Where | Current text | Proposed text |
|---|---|---|---|
| 1 | Row `/sc:adversarial`, section 2.1 (line 71) | `SKIP \| SKIP \| SKIP \| OPTIONAL \| SKIP \| OPTIONAL \| Only when two or more competing designs exist` | `SKIP \| SKIP \| OPTIONAL \| OPTIONAL \| OPTIONAL \| OPTIONAL \| Needs 2+ competing artifacts or every cell is SKIP. Complexity = number of artifacts, size, cost of a wrong pick: quick for N=2 small, standard default, deep rare, WORTH IT at HIGH for S/F/R/N. Not in Ryan's pipelines. Also runs inside /sc:brainstorm, /sc:reflect Tier 2, /sc:troubleshoot Tier 2, /sc:release-split: do not stack a manual run on those.` |
| 2 | Same row, **S** cell | `SKIP` | `OPTIONAL` (J). Reason: a story-level approach debate has a precedent (`.dev/reviews/story-1-4-approach-debate-20260911`, N=2, quick) |
| 3 | Same row, **R** cell (re-rating under the multi-feature definition) | `SKIP` (consistent with the 2.4 reading that a release "assembles and ships work already built", line 139) | `OPTIONAL` (J) at MEDIUM, WORTH IT at HIGH. Changed because a multi-feature release has a planning step with competing release plans; the neighbouring `/sc:release-split` row (line 72) is already WORTH IT at R and calls this command in Mode B |
| 4 | Section 3, overlap O4 (line 230) | `/sc:adversarial is for choosing between two competing drafts, not for critique` | Append: `It also runs inside /sc:brainstorm (Wave 3), /sc:reflect Tier 2, /sc:troubleshoot Tier 2 and /sc:release-split; do not repeat it by hand there. 4 to 10 artifacts are allowed but no run above 3 exists on disk; each extra artifact adds a Round 1 and Round 2 call and grows Round 1 input.` |
| 5 | Section 4 footprint table (after line 265, `/sc:brainstorm`) | `.dev/brainstorms/<timestamp>-<name>/merged-requirements.md` | Add: `and adversarial/ (6 artifacts; brainstorm.md:193)` |
| 6 | Section 4 footprint table (new row) | no row for `/sc:adversarial` | `\| /sc:adversarial \| <output>/adversarial/{diff-analysis,debate-transcript,base-selection,refactor-plan,merge-log}.md`, a merged output, `variant-*.md`, `invariant-probe.md` (standard/deep only), sometimes `return-contract.yaml`; default location is next to the first input file \| SK:371-390, 605-606; observed 31 dirs \|` |
| 7 | Section 2.1 row `/sc:brainstorm` Notes (line 64) | `Guide: "only if the idea is still vague". --handoff task goes straight to a task file. ‡ with bmad-brainstorming` | Append: `Runs /sc:adversarial in Wave 3; --depth quick caps proposals at 2 (brainstorm.md:69).` |
| 8 | Section 2.2 rows `/sc:roadmap`, `/sc:tasklist` (lines 113-114) | no mention of the debate | Add to `/sc:roadmap`: `Its debate step is one LLM call inside superclaude roadmap run, not /sc:adversarial; its files (debate-transcript.md, base-selection.md) look like adversarial output but are not.` Note for `/sc:tasklist`: `adversarial.md:182` still lists it as a related command; it is retired (ruling 3). |
| 9 | Section 5 unverified list | n/a | Add the items from section 8 below that bear on the checker (U5, U9, U10) |

## 8. Unverified items

I read the command file, all of SKILL.md (2998 lines) and all four refs. I did not run the command or any other `sc:` command.

| # | Item | Why unverified / conflict | What resolves it |
|---|---|---|---|
| U1 | Can `--agents` be combined with `--compare`? | SK:555 says STOP on that combination; SK:1032 and AS:191 say Mode A advocates default to "current model if `--agents` not specified". Model diversity in Mode A is therefore unclear | Run once with a harmless pair of files, or ask the SuperClaude maintainers |
| U2 | Does `--focus` cut calls or tokens, or filter diff points? | Only the prompt injection (SK:981) and the interactive "prioritize" option (SK:1917-1920) are stated | Read a transcript from a run with and without it |
| U3 | What `--blind` does outside `--pipeline` | Procedure is written only for pipeline artifact routing (SK:2856-2886); the parameter table (SK:343) and AD:71 describe it generically | Same |
| U4 | `--suspect-source` | Named in `sc-bare-review/SKILL.md:3,18,55`; not defined in AD, SK or refs (no "suspect" hit) | Ask the maintainers, or drop the flag from the bare-review hand-off |
| U5 | When `return-contract.yaml` is written, and its path | SK:427 says MUST on every invocation but gives no path; 14 files exist for 32 transcripts. `invocation_method: manual` is undefined (SK:459) | Same |
| U6 | Standalone token and time cost | No file states one. About 32k tokens to load the protocol uses 4 bytes per token (J). The 15-30k troubleshoot delta is a subtraction of two table rows | Measure one run |
| U7 | Internal inconsistencies in the protocol | Rubric is 30 criteria in SK:1669,1740 and SP:178,226, but "25-criterion" in SK:1753,1756, DP:192 and AT:201; probe is 6 categories in SK:1110 but 5 in the artifact table at SK:1307; `--dry-run` is in SK:2546 but not in the AD option table; roadmap refs say "5+ agents triggers orchestrator" (`sc-roadmap-protocol/refs/adversarial-integration.md:218`) while SK always uses the `debate-orchestrator` (SK:464-469) and has no 5+ rule | Maintainers; none changes the advice above |
| U8 | `--convergence` and convergence reporting at quick | DP:150 says no convergence check at quick, yet observed quick runs report percentages (e.g. 88%) and one reports `null` (`story-1-4` return contract) | Read DP and SK together with one quick transcript |
| U9 | Look-alike classification | `_bmad-output/planning-artifacts/{debate-transcript,base-selection,diff-analysis}.md` are attributed to the roadmap CLI by inference (frontmatter plus neighbouring `extraction.md`, `roadmap*.md`); no file records the producer. Separately, `.dev/troubleshoot/fu10-saga-2026-05-24/adversarial` has only 4 files plus `positions/`, so the six-file layout is not guaranteed | Check git log for the producing commit |
| U10 | How representative the observed runs are | One checkout only: 31 dirs, max N=3, no pipeline manifest, no `--blind`. Other engineers' repos and their `~/.claude` copies (which may differ) were not observed | Compare across engineers |
| U11 | All size and N thresholds in 2.4 and the band definitions | JUDGMENT anchored on the observed sizes, not stated in any file | Team agreement |
