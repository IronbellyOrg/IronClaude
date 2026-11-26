# Requirements specification: panel process redesign (variant 1 of 3, architect lens)

Conventions used throughout:
- `BR` = `.dev/brainstorms/20261113-223124-panel-process-redesign`.
- `EVAL` = `.dev/eval-workspaces/tasklist-review-panel/20261111-a1`.
- `HO2` = `.dev/eval-workspaces/tasklist-review-panel/HANDOFF-review-panel-unification-run2.md`.
- Evidence files: `BR/seed-brief.md`, `BR/enrichment/investigation-generality.md` (IG), `BR/enrichment/research-external.md` (RE), `BR/enrichment/reused/investigation-designspec.md` (DS), `.../investigation-alias-control.md` (AC), `.../investigation-patterns.md` (PAT).
- "Found /14" counts the 14 issues of the two defect-rich packages. Nine of the ten missed issues sit in those 14: B1, B2, B5, I1, I4, I5, B6, B8, I6. The tenth, I7, sits in the control package, which is scored out of 2 and reported separately.
- Class labels for the ten (class names are defined in section 2): B1 and B2 are C1; B5 is C2; I1 is C3; I4 is C4; I5 is C5; B6 and B8 are C6; I6 is C7; I7 is C8.
- All timings and probabilities for the redesigns are estimates from the measured medians, not measurements. The validation experiment in section 5 replaces them with data.
- Where text says "per run", a run is one panel run on one package.

---

## 1. Theories

I keep all three theories from the seed, refine each one with numbers, and reject one rival. No theory is replaced.

### T1 (refined): verification stops at the surface the plan names

Cheap reviewers check the files and lines the plan or source names. They do not sweep for files or places that depend on what the plan changes.

| Evidence | Number | Source |
|---|---|---|
| Files touched that the plan does not name, per run | ember 0.8, luna 0.3, haiku 0.9, sonnet 3.1 | PAT section 1 |
| Runs that touched a test file the plan never names | ember 8%, luna 1%, haiku 0%, sonnet 35%, grok 33% | PAT section 1 |
| The control package's unnamed test file | opened in 0 of 176 cheap control runs; 7 of the 8 runs that opened it found I7; 0 of 225 others did | seed, PAT section 4 |
| Root changelog touched in design-spec runs | 1 of 233 runs; I5 found by no reviewer of any model | PAT section 4 |
| Search volume is not the variable | haiku searched `tests/` in 81% of runs yet opened the unnamed test in 0 of 25; the missing move is a reverse-dependency search | PAT sections 1 and 3 |
| Inventory-first move | the one run that found B8 began with two repo-wide inventory greps (AC section 3) | AC section 3 |

- **Explains:** I5, I7, B8 fully; B6 partly.
- **Does not explain:** B1, B2, I6, which sit inside the plan text.
- **What it implies:** "look wider" will not work. The sweep must be handed over as a concrete search, either run by a script or given as a recipe with the exact search form.

### T2 (refined): right place, one local question, and no enumeration stage

Reviewers anchor in the right region but ask one local question and stop. They list nothing and do not ask for a stopping rule or satisfiability. They also do not ask the same thing from the other direction or for another input case.

| Evidence | Number | Source |
|---|---|---|
| Findings on the I5 sentence | 16 (15 ember, 1 haiku), all asking whether a grep matches too much, none asking where else the claim lives | DS section 2c |
| Findings on the B5 sentence | 3, all tracing one input case (an "off" mode) | DS section 2c |
| Findings on the I1 row | 1, asking a different question | DS section 2c |
| Anchors on the B1 and B2 criterion | 0 in every cheap and non-cheap panel | DS sections 2c and 3 |
| Ember on the Task 1 region | anchored it in 52% of runs, matched B1 in 3% | PAT section 5 |
| I4 area findings | 0; the one ember that grepped the real file saw the repaired text and got a pass | DS section 2c |
| B6 | luna read the right file and graded the leftover as "unclear exemption" | AC section 3 |
| Finders succeeded by tabulating | the I1 finders built row-by-row coverage tables, but spent 190-1005 s against ember's 34 s median | DS section 3 |

- **Explains:** B1, B2, B5, I1, I4, I5, I6, and B6 partly.
- **What it implies:** an enumeration must be forced, and it must be made cheap. Tabulation works, but only when someone narrows it first. Either a script extracts the rows, or a short recipe confines the model to one class.

### T3 (refined): the evidence environment and grading rules suppress findings

I treat this as an enabler that explains part of the zeros, not as the main cause.

| Evidence | Number | Source |
|---|---|---|
| Sandbox is a post-implementation checkout | repaired code hides B5, I1, I4; I5 is the only one still visible | DS preamble |
| Reviewers saw the repaired sentence and did not compare | 44 of 98 alias reviewers saw the narrowed sentence next to the broader plan wording | AC section 2 |
| Source never opened | 156 of 665 valid runs; ember 81 of 209 (39%) | HO2 R14 |
| Merge drops findings | 80 reviewer-level cases, 49 blocking findings lost (ember 33, luna 30) | HO2 R20 |
| Rubric grades an unstated requirement Medium and has no missing-task category | all 7 true I7 finds were non-blocking; one grok run read the changelog hit and dropped it as "minor" | DS section 3, PAT section 4 |
| A leak file sits in the sandbox | 2 of the 9 I7 credits came after reading it | AC section 3 |

- **What it implies:** harness fixes H1-H4 plus brief edits. My estimate is that the four fixes alone lift the isolated panel by +0.2 to +0.7 of 14. This is a guess that arm A1 in section 5 will measure. The reason it is small: B1, B2, B6, I6 are never anchored and need no repo evidence, so no environment change reaches them.

### Rejected rival: reasoning budget

Median thinking tokens correlate with hits across models (rho 0.64). Within ember the hard-issue rate is flat (0.25 vs 0.22 per run, low vs high thinking half), and within luna it is flat (0.09 vs 0.09). Budget explains haiku's spread, not ember's or luna's ceiling (PAT section 6). Giving ember and luna more time does not help; giving them different questions might.

### Mapping of redesigns to theories

| Redesign | T1 | T2 | T3 |
|---|---|---|---|
| A: Probe Sheet (script pre-pass) | primary: the script runs the sweeps | primary: one forced question per item | shared base (3.0) |
| B: Lens Ledger (recipes plus forced enumeration) | secondary: recipes give exact search forms to the search lens | primary: enumeration before judgement | shared base (3.0) |

---

## 2. Defect classes and generality

Class names and definitions contain no package, task, file name or ground-truth wording. Counts are other documents with a recorded instance, from IG section 2 (phrase-search lower bounds; all one repository, one owner, one plan pipeline).

| Class | Abstract definition | Recurrence outside the study | Strength (IG section 5) | Review targets |
|---|---|---|---|---|
| C1 | A criterion asks for a complete or exhaustive result over a set that has no stopping rule, or the criterion's set differs from the set its own instruction names | 3 documents, symptom level (new items every review round) | supported with caveat | plans, specs, test plans |
| C2 | A rule the source states is not carried into the derived text, so what is built from it breaks the rule | 6 documents, all plan-level | general | any derived document (plan from spec, tasklist from roadmap, doc from spec) |
| C3 | A value is read, mapped or required by one component and no row or task writes it | 3 documents (1 blocking, 1 inferred, 1 low) | weak | specs, plans with state or field tables |
| C4 | A criterion embeds a command, pattern or selector whose literal form cannot match or pass against the text or state the same document orders | 9 documents | general | plans, runbooks, CI docs, specs with verification rows |
| C5 | After a change, a count, claim or copy in another location is left stale because nothing enumerates that location | 9 documents | general | plans, release notes, documentation sets |
| C6 | A sentence with "all", "only", "never" or "outside X nothing" is contradicted by an inventory, by the document's other parts, or by the scope of the check said to enforce it | 12 documents | general (mostly delivered docs) | docs, guides, specs, plans that dictate text |
| C7 | Dictated text omits a clause of a constraint stated elsewhere in the same document (broad form: contradicts the document's own constraint or criterion) | broad 5 documents; narrow form 1 | broad form general, narrow form weak | plans, templates, policy-bound text |
| C8 | The document changes something that a check elsewhere pins, and no step updates or runs that check | 6 documents | general | plans that change code, refactoring specs |

Outside evidence that the classes are general (RE section 2):
- ISO/IEC/IEEE 29148 characteristics map onto them. An unsatisfiable criterion is "feasible" and "verifiable". A criterion with no stopping rule is "verifiable" and "complete". A universal claim contradicted elsewhere is "consistent". A missing task is "complete" for the set. A stale duplicate is "consistent" and "singular". A value read but never written is "complete", "consistent" and traceability.
- Requirements-smell work (59% precision, 82% recall) shows lexical detectors have high recall and mediocre precision, so detector output needs a judge.
- No catalogue entry names "universal claim unchecked against the corpus". C6's check is therefore not backed by a published smell and must be shown empirically.

Classes that recur but are not among the ten (IG section 3; registry candidates for v2): X1 check passes on old code (4 documents), X2 wrong or aged citation (4), X3 two source statements conflict (3), X4 task ordering or a gate with no consumer (3), X5 criterion depends on an uncaptured baseline (3), X6 failure path with no route (3), X7 count broken by a forced step (2, weak). The ten are not special; several other classes are as frequent.

Limits the spec must carry forward:
- Every document is from one repository and one plan pipeline.
- The records show a class exists, not that cheap panels miss it elsewhere. Only the hold-out run shows that.
- C1 and C3 must be claimed only in the weaker forms above. C7 only in the broad form.

---

## 3. The two redesigns

### 3.0 Shared scaffolding (not a redesign; both redesigns use it)

The architect rationale: the unit of generality is the defect-class card. Cards are written once, generically, and rendered by two different consumers. Adding a class, a target type or a reviewer model must not require editing the dispatcher.

**Class registry.** One card per class, validated against a schema.

| Field | Meaning |
|---|---|
| `id`, `name`, `version` | identity and version (the registry version is recorded in every run) |
| `definition` | target-neutral definition, as in section 2 |
| `recipe_text` | at most 120 words, imperative, used by Redesign B |
| `question_template` | one question with placeholders, used by Redesign A |
| `extractor` | name of a deterministic extractor, or null |
| `route` | `search` or `read`, which reviewer type suits it |
| `replicas` | 1 or 2 reviewers get each item or lens |
| `applies_to` | list of target kinds: plan, spec, doc |
| `instances` | at least 2 citations from material outside the study packages |
| `severity_guidance` | one line |
| `known_weakness` | one line, shown to maintainers, never to reviewers |

**Target adapter interface.** An adapter turns a document into typed blocks:

| Block kind | What it holds |
|---|---|
| `task` | an instruction unit |
| `criterion` | an acceptance or verification statement |
| `constraint` | a rule that binds other text |
| `dictated_text` | text the document orders to be written word for word |
| `edit_target` | a path the document says to change |
| `gate` | the checks the document runs at the end |

The plan adapter is v1. Specs and docs are v2 adapters (requirement ids and "shall" sentences; headings and factual claims). Only the adapter and the extractor patterns change for a new target; recipes and questions are target-neutral.

**Harness fixes H1-H4 (from the seed brief), as requirements:**

| Fix | What changes |
|---|---|
| H1 | the brief names the source document |
| H2 | the merge truncates over-long anchor and claim instead of dropping the finding (`src/superclaude/cli/review/findings.py`, the `_check_flat` calls for `anchor`, `anchor2` and `claim`) |
| H3 | the sandbox is checked out at the plan's base commit, before implementation |
| H4 | `.dev/reflect/` and every report about the package are removed from the sandbox |

**Brief edits CB1-CB4** (they change the brief file `src/superclaude/rules/prompts/document_review_loop_prompts.md` and the study copy in `tools/run-reviewer.sh`; the findings-v1 categories stay as they are):

> **CB1.** "The plan was written from this source document: {{SOURCE}}. Open it before you grade anything. A rule the source states and the plan leaves out, or restates differently, counts as stated text when you grade a finding."
>
> **CB2.** (replaces only the last clause of the Medium sentence) "Grade it Medium when the sentence needs a guess that the implementer picks the worse of two readings the text allows. A task the plan needs but does not contain (a test, copy, count or document that one of its own changes makes wrong) is a missing-requirement finding: Medium when nothing the plan requires fails without it, blocking when a step or criterion the plan requires would fail or be false without it."
>
> **CB3.** "Write one findings line for every mismatch you confirm. Low harm is a reason for MINOR, not a reason to leave it out. A confirmed mismatch left out of the block is lost."
>
> **CB4.** "The merge enforces these limits: anchor 12 to 200 characters, claim at most 300 characters, refs at most 8. Copy the shortest part of the text that identifies the problem."

**Class recipes (v1 draft wording).** Redesign B quotes these in full. Redesign A uses the same cards, rendered as the questions in 3.1(a). The wording uses generic moves and no ground-truth text.

| Class | Recipe text |
|---|---|
| C1 | "COMPLETENESS CHECK. For every criterion that says every, all, each, complete, exhaustive, found, none remaining or a similar set word: (1) write the set it covers; (2) write the finite check that proves the set is covered: a closed list, a search with a named scope, or a count; (3) write the set the same task's instruction names; (4) if step 2 has no answer, or steps 1 and 3 differ, report an unpassable-check finding, because a reviewer can always find one more item. If the check is a closed list, say so and move on." |
| C2 | "SOURCE RULE WALK. For each section of the source that a task cites, list its rule sentences (must, never, only, always, reports, halts, returns). For each rule write where the plan carries it, or NOT CARRIED. For a NOT CARRIED rule, trace one input where its condition holds through the plan's tasks and say what the built artifact does. Report it when the artifact breaks the rule." |
| C3 | "READ AND WRITE TABLE. For each value a task says a component reads, maps, matches or returns on (a field, status, flag or enum value), find the row, task or source line that writes that value. Write the pair. A value with no writer is a finding." |
| C4 | "LITERAL COMMAND CHECK. For each criterion that contains a command, pattern or test selector, copy the literal pattern. Copy the exact text the same task, or an earlier one, tells the implementer to write. Test the pattern against that text as written: run it on a string with printf; do not look at the current file, because it may already hold finished text. Report a pattern that cannot match, or a selector that selects fewer checks than the criterion names." |
| C5 | "SECOND LOCATION SWEEP. For each count, name, claim or default the plan changes, search the whole repository, root files included (changelogs, readmes, guides, mirrors), for the old value. List each hit that no task edits. A claim restated in a document that the change makes false is a missing-requirement finding." |
| C6 | "UNIVERSAL CLAIM CHECK. For each sentence the plan dictates or states with all, only, never, every, no other, or outside X nothing: (1) name the set; (2) run one search that counts members or exceptions; (3) read the plan's other tasks for the opposite statement; (4) find the test or check said to enforce it and write what it can fail on. Report the sentence when an exception exists or the enforcer is narrower than the claim." |
| C7 | "CONSTRAINT SWEEP. Split each constraint into its clauses. For every piece of text the plan dictates word for word, mark each clause carried or dropped. Report text that keeps some clauses and drops another." |
| C8 | "DEPENDENT CHECK SWEEP. For each file the plan edits, search the test tree and the repository for its path and its module or command name. Open every test file the plan never mentions. Report a test that pins text, counts or behaviour a task changes when no task updates or runs it." |

**Telemetry.** Every findings-v1 line may carry the extra keys `class` (C1-C8 or null) and `probe` (item id or null). Unknown keys are accepted silently by the parser, per HO2 section 5.2; a test must confirm this before relying on it. The merge contract is otherwise unchanged. A per-class yield table (found, wrong-blocker, time) is produced for every run.

**Graceful degradation.** If the pre-pass, the lens renderer or the ledger check fails, the harness runs the isolated panel with H1-H4 and CB1-CB4 and records the fallback.

**Messaging between reviewers is not used by either redesign.** Showing one model's conclusions to another causes herding (29-34% conformity, about +10 points of answer flips; RE section 4). Both redesigns keep reviewers blind to each other. An optional claims-only exchange is a documented extension seam (the registry already tags which class produced a finding) and is out of scope for the first test.

---

### 3.1 Redesign A: Probe Sheet (a script extracts typed items, a cheap model judges one item at a time)

#### (a) Mechanism, wording and order of steps

**Mechanism.** A deterministic, read-only helper `superclaude review probe` reads the plan, the source and the base checkout. It extracts typed items from the registry's extractors. Each item is a self-contained question with its evidence attached. Items are routed to reviewers by the card's `route` and `replicas`. Each reviewer answers its items in a table first, then reviews freely. The model keeps all judgement; the script only chooses what to ask and gathers the evidence.

**Extractors (v1)**

| Id | Class | What it extracts | Known blind spot |
|---|---|---|---|
| E1 | C1, C6 | Sentences in criteria and in dictated text that contain set words; the task's named scope (paths and globs named in the task body, or NONE); whether the sentence names a closed list, a glob or a count; for a sentence that says a test "enforces" it, the task that defines that test and its listed assertions | a set word with no bound that the model must judge as bounded elsewhere |
| E2 | C4 | The literal pattern or selector inside each backticked command in a criterion; the strings the same task and earlier tasks order to be written; strings that match after lowercasing and collapsing hyphens, spaces and underscores but not literally; the hit count of the command as written on the base checkout (information only) | commands with computed patterns |
| E3 | C8 (and C5 for non-test dependents) | Existing paths that carry an edit verb in a task; `grep -rlF` of each path and its stem over the test tree and the repository; test files that match and are named nowhere in the plan; the commands of the gate task | dependents that refer to the file only by an indirect name |
| E4 | C5 | From negative criteria ("no remaining", "none", "zero hits") and from "N to M" or count changes: the phrase or number plus noun; `grep -rnF` of it over the whole base checkout including root files; hits in files no task names | stale claims that use different wording than the plan |
| E5 | C2 | Rule sentences of the source sections each task cites (modal or universal verbs, or a backticked identifier with a report, return, halt or set verb); identifiers of each; identifiers missing from every citing task; ranked by missing count | rules carried in words, not identifiers |
| E6 (experimental) | C3 | Backticked literals in a read position ("keys on", "when", "==", "returns for") with no occurrence in a write position ("sets", "=", "gives") in the same document | high false-positive rate; low trust |
| E7 | C7 | Constraint clauses (split on semicolons, "and", commas); dictated-text blocks; distinctive tokens per clause; blocks that share two or more tokens with one clause and none with another clause of the same constraint | clauses with no distinctive token |

**Item format** (`probe.json`, deterministic: same input gives byte-identical output):

`{item_id, class, anchor_text (at most 200 characters, copied exactly), location, evidence: [{path, line, text at most 160 characters}], question, priority}`

**Question templates** (these are the card `question_template` wording, rendered from the extractor output):

| Class | Template |
|---|---|
| C1 | "Item {id}. Task {t} criterion: «{anchor}». The task's instruction names this scope: {scope or NONE}. (1) What finite check proves the criterion true? (2) Is the criterion's set the same as the instruction's set? Answer PROBLEM if (1) has no answer or (2) differs." |
| C2 | "Item {id}. The source says: «{rule}». Identifiers {list} appear in no task that cites this section. Where does the plan carry this rule? Trace one input where its condition holds through the plan and say what the artifact does. PROBLEM if the artifact breaks the rule." |
| C3 | "Item {id}. Text A reads or returns on the value «{value}»: «{quote A}». Does any row or task write that value? Quote it. PROBLEM if none does." |
| C4 | "Item {id}. Criterion pattern: «{pattern}». Text the task orders: «{string}». They differ only in {case/separator}. Does the pattern match the ordered text as written? PROBLEM if not." |
| C5 | "Item {id}. The plan changes «{old}». The same text appears at {hits}, which no task edits. Is the text at each hit made false or stale by the change? PROBLEM if yes." |
| C6 | "Item {id}. Dictated sentence: «{anchor}». Run one search that counts exceptions to the set it quantifies over. Name any task or file that contradicts it, and what the enforcing check, if any, can fail on. PROBLEM if an exception or a narrower check exists." |
| C7 | "Item {id}. Constraint clauses: «{c1}» and «{c2}». Dictated text: «{block}». Does the text keep both clauses? PROBLEM if one is dropped." |
| C8 | "Item {id}. The plan edits {path}. {test file} references it and no task names or runs that test. Open it. Does it pin text or behaviour a task changes? PROBLEM if yes." |

**Brief additions** (appended to CB1-CB4):

> "PROBE SHEET. A script, not a model, read the plan, the source and the repository and listed the items below. Each item is a question, not a finding; most will be fine. Do this first: write a table named `Probe responses` with one row per item: `item id | OK, PROBLEM or CANNOT TELL | one quote from each side of the problem, or the search you ran`. Answer PROBLEM only when you can quote the two texts, or show the search result, that prove it. Write one findings line for every PROBLEM row. Do not write a findings line for an OK row. Then spend the rest of your time on your own review of the plan."

**Order of steps (per package)**
1. Harness builds the sandbox at the plan's base commit and removes leak files (H3, H4). This is the same setup step as today, so it adds no time.
2. Harness runs `superclaude review probe` with a 12-second `timeout`. It writes `probe.json` and one routed sheet per reviewer. On timeout or error the panel falls back to the isolated brief.
3. Harness launches the reviewers in parallel with the base brief, CB1-CB4 and the routed sheet.
4. Each reviewer: (a) opens the plan and the source; (b) writes the probe table; (c) reviews freely; (d) writes the report with the findings-v1 block.
5. Harness runs a deterministic check: every PROBLEM row must have a findings line, and every quote must be a substring of the plan, the source, or the recorded tool output. Quotes that are not found demote the finding to non-blocking. A PROBLEM row with no findings line is promoted to a MINOR non-blocking finding using the item's `anchor_text`.
6. Merge runs unchanged (findings-v1).

#### (b) Model roles

| Panel | Ember | Luna 1 | Luna 2 | Other |
|---|---|---|---|---|
| ember + 2x luna (primary) | `search` items: E3, E4, E2, and E1's inventory count questions. About 10 items. Ember greps well and finishes in 41 s, so it carries the heaviest evidence work | `read` items: E1 (C1), E5 odd-numbered rules, E7. About 8 items | E1 (C1 replica), E5 even-numbered rules, E6. About 8 items | C6 items are replicated to ember and one luna |
| haiku + 2x luna | haiku takes the `search` items, limited to 8, and its free review is capped at 4 findings (its time is dominated by thinking, 233 s) | same as above | same as above | n/a |
| sonnet + 2x luna | sonnet takes `search` items and E5 and E6 (sonnet already opens unnamed files in 35% of runs; the sheet makes this reliable) | same as above | same as above | n/a |

Routing lives in the panel template as data (`route` and `replicas` per class), not in code.

#### (c) Time budget (seconds per package)

Baseline for the primary panel: slowest-reviewer median is 100-122 s per package (348 s over three packages, mean 116 s). Luna is the slowest and sets the elapsed time. Ember finishes at 41 s and idles.

Cap: +35% means at most 135 s (at baseline 100) or 164 s (at baseline 122). I write the hard limit for a package as D = floor(1.35 x b), where b is that package's baseline median.

Assumption for reviewer time: luna's output is about 4.9k tokens in 102 s (about 48 tokens/s, if generation-bound; UNVERIFIED). Extra output of 0.65k tokens costs about 14 s. Ember runs at about 256 tokens/s.

| Step | Actor | Baseline s | Redesign A expected s | Hard limit | Critical path? |
|---|---|---|---|---|---|
| Sandbox build (base commit instead of HEAD) | harness | same | same | none | no |
| Probe pre-pass | script | 0 | 6 (4-8) | 12 s by `timeout` | yes (serial before reviewers) |
| Sheet routing and brief rendering | script | 0 | <1 | none | yes |
| Ember reviewer | ember | 41 | 66 (extra 2.5k tokens is about 10 s, plus about 15 s for item greps) | D | no (slack of about 70 s) |
| Luna reviewers | luna | 100-122 | +12 expected, +30 worst | D | yes |
| Merge | script | unchanged | unchanged | none | no |

Critical path = pre-pass + slowest luna.

| Package baseline b | Expected (6 + b + 12) | Increase | Worst modelled (12 + b + 30) | Increase |
|---|---|---|---|---|
| 122 s | 140 s | +14.8% | 164 s | +34.4% |
| 100 s | 118 s | +18.0% | 142 s | +42.0% (would exceed D = 135) |
| Sum over 3 packages, 348 s | 348 + 3 x 18 = 402 s | +15.5% | 348 + 3 x 42 = 474 s | +36.2% (kill-limited) |

- **Enforced by timer or kill:** the 12-second probe `timeout`; the per-reviewer `timeout D`. A reviewer killed at D yields no findings block, so its findings are lost and the run is counted as a kill.
- **Only expected:** the 6 s probe time (not yet measured), the +12 s luna overhead, the kill rate (I expect 5% or less; UNVERIFIED).
- **Slack reallocation:** the idle time of the fast reviewer (ember, about 70 s) is used by giving ember the evidence-heavy items.
- **Other panels:** haiku + 2x luna (b = 220-238): 6 + b + 17 (haiku's extra 4k tokens at 231 tokens/s) gives +9.7% to +10.4%. sonnet + 2x luna (b = 259-302): 6 + b + 22 gives +9.3% to +10.8%.

#### (d) Defect-class coverage matrix

Probabilities are per run on the primary panel. "Why a cheap model reaches it" is the reason the model can then do it, tied to the evidence.

| Issue | Class | Class-level trigger | Why a cheap model then reaches it | p low-high | Slot |
|---|---|---|---|---|---|
| B1 | C1 | E1: a criterion with set words and no closed list, shown beside its task's scope | The question has a one-step answer ("what finite check?"). Luna and ember answer direct questions about a quoted line; they skipped it before only because nobody asked (0 anchors in every panel) | 0.25-0.45 | luna x2 (replica 2) |
| B2 | C1 | Same item; the criterion's set differs from the instruction's named scope | The scope sits next to the criterion, so the comparison is a read, not a search | 0.20-0.40 | luna x2 |
| B5 | C2 | E5: a source rule whose identifiers are missing from the citing task | The item gives the rule and asks for one input trace. Three cheap reviewers already analysed the exact sentence with a different case; the sheet supplies the other case. Needs a blocking grade (CB1) | 0.10-0.30 | luna |
| I1 | C3 | E6: a read value with no write occurrence (experimental) | Two quotes side by side make the absence checkable; hit rate of E6 is low | 0.05-0.20 | luna |
| I4 | C4 | E2: the pattern and the ordered text differ only by case or separator | A string comparison; no source or repo reasoning. H3 removes the repaired text that gave a false pass | 0.45-0.80 | ember |
| I5 | C5 | E4: a negative criterion with a number-plus-noun phrase; repo-wide hits in files no task names | The hit is handed over with its path; ember only judges "is this made false?". CB3 stops it being dropped as minor | 0.40-0.75 | ember |
| B6 | C6 | E1: a universal sentence plus the task that defines the enforcing test and its assertions | The question asks what the test can fail on and for one counting search; luna already read the right file once. Contradicting tasks are not scripted, so reach depends on luna | 0.10-0.30 | ember + one luna (replica 2) |
| B8 | C6 | E1: a universal sentence over a class of files; the item asks for one exception-counting search | Ember runs the search it is asked for (it does not run inventory greps on its own) | 0.10-0.30 | ember + one luna |
| I6 | C7 | E7: a constraint clause with no token overlap in a block that overlaps another clause | A clause-by-clause check on one block; narrow form, weak support | 0.05-0.20 | luna |
| I7 (control) | C8 | E3: a test file that references an edited path and is named nowhere in the plan | Seven of eight runs that opened the file found it; the item makes opening it the instruction | 0.55-0.85 | ember |

#### (e) Broad applicability

- **Other plans.** Plan blocks are recognised by headings and verbs (the plan adapter). Extractors use no package vocabulary: set words, backticked commands, edit verbs, "cites section N". Nothing in the items names a model, package or issue.
- **Specifications.** A spec adapter maps requirement ids and "shall" or "must" sentences to `criterion` blocks and verification rows to `gate` blocks. E1, E2 and E5 transfer directly (a spec's own rules versus its verification rows). E3 needs a spec-to-code mapping, so it is disabled for specs unless the spec names files.
- **Documentation.** A doc adapter maps factual claims (numbers, "only", "all", "never") to `criterion` blocks; E4 (stale claims) and E1 (universal claims) transfer. E3 becomes "which tests or docs mention this module".
- **Re-derive for each new target:** block recognition patterns, the command syntax to parse (grep, pytest, make, others), which paths count as "tests" and "root documents", and the severity guidance. Recipes and question wording do not change.
- **Anti-overfitting rules:**
  - (AO1) Recipe and question text is machine-linted against every `ground-truth.json`: no 4-word sequence from any `description` or `plan_quote`, no package, task or file names.
  - (AO2) Every card cites at least 2 instances from outside the study packages.
  - (AO3) Extractor patterns are tested on at least 3 plans that were not used to write them.
  - (AO4) Recipes and extractors are frozen by git tag before hold-out ground truth is written.
  - (AO5) Ground truth is never in the sandbox.
  - (AO6) Ablation: remove one class at a time and confirm the other classes' reach does not move.

#### (f) Expected gain in issues found out of 14, per run

| Component | Low | High | Basis |
|---|---|---|---|
| Baseline (isolated ember + 2x luna) | 1.83 | 1.83 | HO2 R4 |
| Harness fixes H1-H4 | +0.2 | +0.7 | estimate; measured by arm A1 |
| Redesign A, nine /14 issues | +1.70 | +3.70 | sum of the matrix rows above (without I7) |
| Displacement of baseline-found issues | -0.30 | -0.10 | the probe table takes time that free review used; B3, I2 and similar were found in most runs |
| **Redesign A net** | **+1.40** | **+3.60** | |
| **Total found /14** | **3.4** | **6.1** | the highest ever measured is 4/14, so the upper end is optimistic |

- Redesign share of the gain: +1.40 to +3.60. Harness fix share: +0.2 to +0.7. Overlap between them (I4, I1 and B5 are partly masked by the checkout) is not removed; this may double-count about 0.1.
- Control package: I7 +0.55 to +0.85 of 2.
- "Consistently" (per-run probability of at least 0.5 at the middle of the range): I4, I5 and I7 only. B1, B2, B5, B6 and B8 are "sometimes" (0.2-0.4). I1 and I6 stay weak.

#### (g) Token and elapsed overhead

| Panel | Baseline output tokens per package | Redesign A added | Increase | Elapsed |
|---|---|---|---|---|
| ember + 2x luna | 21.3k (64k over 3 packages) | +5.5k (ember +2.5k, each luna +1.5k) | +26% | +15% expected, at most +35% enforced |
| haiku + 2x luna | 63.7k (191k over 3) | +6k | +9% | +10% |
| sonnet + 2x luna | 46.3k (139k over 3) | +6k | +13% | +10% |

The pre-pass uses no model tokens. Input tokens grow by the sheet (1.2-2.5k per reviewer; UNVERIFIED).

#### (h) Implementation effort

| Item | Where | Rough lines |
|---|---|---|
| Extractors E1-E7 and item model | new `src/superclaude/cli/review/probe.py` | 450-600 |
| CLI entry and routing | new `probe_cmd.py`; routing keys added to the panel template data (`panel.py` reads them) | 60 + 30 |
| Quote verifier and auto-promotion | extend `findings.py` helper (shared with Redesign B) | 80 |
| Registry (8 cards, schema, loader, lint) | new data directory + loader + `tests/review/` lint | 280 + 60 |
| Brief edits | `document_review_loop_prompts.md`, `tools/run-reviewer.sh` | 60 |
| H2 (truncate) | `findings.py` | 20 + 40 test |
| Fixtures for extractors | `tests/review/fixtures/` (3 non-study plans, seeded defects) | 250 |
| **Total** | | about 1,300-1,500 |

#### (i) Failure modes

| Failure | Effect | Mitigation |
|---|---|---|
| Extractor misses (a defect has no trigger shape) | false confidence that the sheet is complete | sheet header says it is a list of questions, not a coverage claim; the free review stays; recall measured on fixtures (REQ-15) |
| Extractor over-extracts | cheap models answer PROBLEM to please | cap 12 items per reviewer; OK is the default; PROBLEM needs two quotes or a search result; evidence check demotes unsupported rows |
| Wrong blockers grow (luna already files 31% surface blockers; CB2 widens what can be blocking) | merge fails rounds on a single blocking finding from any reviewer | items may be blocking only with the grading sentence; unsupported PROBLEM rows are non-blocking; wrong-blocker rate is a decision-rule gate |
| Displacement of easy finds | B3, I2 and similar drop | the probe table is time-boxed (about 8 items); free review keeps its slot; displacement is measured |
| Probe time grows on a big repository | pre-pass misses the 12 s limit | timeout falls back to isolated brief; E3 and E4 restrict grep to tests and root documents plus paths named in the plan |
| Sheet anchors reviewers on items only | free-review findings fall | measured as "non-probe findings per run" (REQ-33); a free-review quota line can be added |
| Dictation-blind classes (C3, C7 narrow) stay low | the ten are not all reached | stated in the matrix; E6 is labelled experimental |
| Kills at D | lost reports | kill rate is a decision-rule gate (10% or less) |

---

### 3.2 Redesign B: Lens Ledger (class lenses, forced enumeration, second pass in idle time)

#### (a) Mechanism, wording and order of steps

**Mechanism.** No pre-pass script. Each reviewer gets a lens: a small set of class recipes (3.0) chosen to suit its model. The reviewer must write an enumeration ledger for each recipe before writing any finding, so it cannot skip the check. The fast reviewer (ember) runs two lenses back to back in two fresh sessions, using time that would otherwise be idle. A deterministic ledger check turns unreported mismatches into findings.

**Lenses**

| Lens | Classes | Reviewer type |
|---|---|---|
| Sweep lens | C8, C5 | search (ember, pass A) |
| Claim lens | C6, C4 | search (ember, pass B, a fresh session; luna 2 replicates C6) |
| Source lens | C2, C3 | read (luna 1) |
| Criteria lens | C1, C7, C6 (in-plan reading) | read (luna 2) |

**Brief additions** (after CB1-CB4):

> "YOUR LENS. Several reviewers review this plan; each has a different lens and none sees the others. Do your lens first, in the order given. For each check below write its ledger before any finding. A ledger row is one line: `L<n> | where (task and line) | what you compared | OK or MISMATCH | one quote from each side`. A check with no rows is unfinished: write `NONE FOUND` and the search or reading you did. Write one findings line for every MISMATCH row, even a small one. Stop lens work after about {{TURNS}} tool calls. Then, if time remains, review anything else."

The recipes for the lens's classes (section 3.0) are pasted under the wrapper. For search-lens reviewers the harness adds a generic search-form line:

> "Search forms you may adapt: `grep -rlF '<path>' <test dirs>`; `grep -rlF '<name without extension>' .`; `grep -rnF '<old value>' . --include='*.md'` (include root files); `printf '%s' '<ordered text>' | grep -c '<pattern>'`."

**Order of steps (per package)**
1. Harness builds the sandbox at the base commit and removes leak files (H3, H4).
2. Harness renders each lens brief from the registry (template fill, under 1 s).
3. Harness launches in parallel: ember pass A, luna 1, luna 2.
4. When ember pass A ends, the harness starts ember pass B only if A ended before 0.45 x D. Otherwise pass B's classes fall to luna 2 (the criteria lens already holds C6).
5. Each session: opens the plan and the source; fills ledgers; writes findings; optional free review; writes the report.
6. Harness runs `ledger-check`: every required check has at least one row or `NONE FOUND`; each MISMATCH row without a findings line is promoted to a MINOR non-blocking finding when its quote is a substring of the plan or source; otherwise the row stays in the report and in telemetry only.
7. Merge runs unchanged.

#### (b) Model roles

| Panel | Roles |
|---|---|
| ember + 2x luna (primary) | ember two sequential sessions (sweep lens, then claim lens); luna 1 source lens; luna 2 criteria lens |
| haiku + 2x luna | haiku one pass on the sweep and claim lenses together (it is the slowest, 233 s, with no slack); each luna runs two sequential sessions: luna 1 source lens then criteria lens part 1; luna 2 criteria lens part 2 then C7. Second pass only if first ended before 0.45 x D (about 134 s at D = 297) |
| sonnet + 2x luna | sonnet one pass on the sweep, claim and source lenses (it already searches widely, 99% opens the source); each luna runs criteria-lens halves; slack on the luna slots is used by a second session as above |

#### (c) Time budget (seconds per package)

| Step | Actor | Baseline s | Redesign B expected s | Hard limit | Critical path? |
|---|---|---|---|---|---|
| Sandbox build | harness | same | same | none | no |
| Lens rendering | script | 0 | <1 | none | no |
| Ember pass A | ember | 41 | 49 (narrower scope, ledger about 0.5k tokens, adds 8 s) | D | no |
| Ember pass B (second session, starts after A) | ember | 0 | 3 start + 49 | launch only if A ended before 0.45 x D; D | no (ember total about 101 s) |
| Luna 1 and 2 | luna | 100-122 | +15 expected (ledger about 0.65k tokens is 14 s), +35 worst | D | yes |
| Ledger check and promotion | script | 0 | <1 | none | no |

Critical path = slowest luna (ember total is about 101 s, below luna's 115-137 s).

| Package baseline b | Expected (b + 15) | Increase | Worst modelled (b + 35) | Increase |
|---|---|---|---|---|
| 122 s | 137 s | +12.3% | 157 s | +28.7% |
| 100 s | 115 s | +15.0% | 135 s | +35.0% (equals D) |
| Sum over 3 packages, 348 s | 348 + 45 = 393 s | +12.9% | 348 + 105 = 453 s | +30.2% |

- **Enforced by timer or kill:** `timeout D` on every session; the 0.45 x D rule for launching ember pass B.
- **Only expected:** the per-session durations, the ledger token counts, the kill rate.
- **Slack reallocation:** ember's idle time (41 s to about 101 s) is spent on a second lens. For the haiku and sonnet panels it is luna's idle time (about 105-117 s of a 220-300 s window).
- **Other panels:** haiku + 2x luna: critical path = max(haiku b + 11, luna 2 x about 112 + 3 = 227), giving 231-249 s, which is +4.6% to +5.0%. sonnet + 2x luna: sonnet b + 19 gives +6.3% to +7.3%.

#### (d) Defect-class coverage matrix

| Issue | Class | Class-level mechanism | Why a cheap model then reaches it | p low-high | Slot |
|---|---|---|---|---|---|
| B1 | C1 | Criteria lens step 1-4: write the set, the finite check, and the instruction's set | Writing "finite check: none" forces the answer; no search needed, but the model must pick the right criteria itself (set words are a lexical cue) | 0.15-0.40 | luna 2 |
| B2 | C1 | Same ledger, step 3 | Comparing two scopes in one row; the reviewer chooses which criteria to ledger | 0.10-0.35 | luna 2 |
| B5 | C2 | Source lens: walk the cited section's rules, write where carried or NOT CARRIED, trace one input | Luna reads whole files and handles a rule-by-rule table, but a section can have 15 or more rules and luna is terse, so some rules go unrecorded | 0.10-0.30 | luna 1 |
| I1 | C3 | Source lens table of read values versus writers | Needs luna to pick the read values itself; weakly supported class | 0.05-0.20 | luna 1 |
| I4 | C4 | Claim lens: copy the pattern, copy the ordered text, test with `printf` | Ember is a grep-checker and runs a one-line test; it must choose the criteria with commands itself | 0.25-0.60 | ember B |
| I5 | C5 | Sweep lens: for each changed claim, search the whole repo including root files | Ember runs the search it is given the form for; the weak step is picking which changed claim to search for | 0.15-0.40 | ember A |
| B6 | C6 | Claim lens and criteria lens: counting search, contradicting tasks, what the test can fail on | Two replicas; each needs to find the universal sentence itself | 0.10-0.30 | ember B + luna 2 |
| B8 | C6 | Same | Needs an inventory search whose form the model must invent | 0.10-0.30 | ember B + luna 2 |
| I6 | C7 | Criteria lens: clause-by-text matrix | A matrix over many blocks is hard for a terse model | 0.05-0.25 | luna 2 |
| I7 (control) | C8 | Sweep lens: search tests for each edited path and open unnamed files | Ember already greps; the recipe says "open every unnamed test file", which cheap models skipped (0 of 176) | 0.20-0.50 | ember A |

#### (e) Broad applicability

- **Other plans, specs and documents.** The recipes are target-neutral text. The adapter only decides which blocks are "criteria", "constraints" and "dictated text". Spec and doc lenses use the same recipe wording with the adapter's block names (for example "requirement" for "task").
- **Re-derive for each new target:** which lens each class belongs to for the models in use; the search forms for the repository layout; the `TURNS` budget; the ledger row vocabulary if the target has no "task and line" locations.
- **Anti-overfitting:** AO1-AO6 from 3.1(e), plus (AO7) the lens wrapper may not name a class's expected outcome; (AO8) ledger rows from the ten issues are never used as examples in a brief.
- **No script dependence.** Redesign B works on a target for which no extractor exists, at lower reach. This is its portability advantage.

#### (f) Expected gain in issues found out of 14, per run

| Component | Low | High | Basis |
|---|---|---|---|
| Baseline | 1.83 | 1.83 | HO2 R4 |
| Harness fixes H1-H4 | +0.2 | +0.7 | estimate; measured by arm A1 |
| Redesign B, nine /14 issues | +1.05 | +3.10 | sum of the matrix rows (without I7) |
| Displacement | -0.30 | -0.10 | ledger writing displaces free review |
| **Redesign B net** | **+0.75** | **+3.00** | |
| **Total found /14** | **2.8** | **5.5** | |

- Redesign share of the gain: +0.75 to +3.00. Harness share: +0.2 to +0.7.
- Control package: I7 +0.20 to +0.50 of 2.
- "Consistently" (middle of the range at least 0.5): none. I4 is the highest (0.42 at the middle).

#### (g) Token and elapsed overhead

| Panel | Baseline output tokens per package | Redesign B added | Increase | Elapsed |
|---|---|---|---|---|
| ember + 2x luna | 21.3k | +8.9k (ember two sessions of about 7.5k each is 15k, +4.5k over 10.5k; luna +2.2k each) | +42% | +13% expected, at most +35% enforced |
| haiku + 2x luna | 63.7k | +10.7k | +17% | +5% |
| sonnet + 2x luna | 46.3k | +10.7k | +23% | +7% |

#### (h) Implementation effort

| Item | Where | Rough lines |
|---|---|---|
| Lens renderer (cards, wrapper, search forms) | new `src/superclaude/cli/review/lens.py` | 100 |
| Ledger check and promotion | new `ledger_check.py`, shares the promotion helper | 150 |
| Launcher rule for the second ember session and `timeout D` | `tools/run-reviewer.sh` (study) and the panel launcher | 80 |
| Lens routing in the panel template data | `panel.py` reads it | 40 |
| Registry (cards, schema, loader, lint) | same as Redesign A (shared) | 340 |
| Brief edits, H2 | same as Redesign A (shared) | 120 |
| Tests | `tests/review/` | 150 |
| **Total** | | about 700-950 (about 450 if the shared scaffolding already exists) |

#### (i) Failure modes

| Failure | Effect | Mitigation |
|---|---|---|
| Cheap models skip or thin the ledger (compliance) | recipes act as a checklist, which human studies show is no better than ad hoc reading | the ledger check logs compliance; a missing ledger is recorded; the decision rule compares against a generic-checklist control arm (A4, section 5) |
| Terse luna writes few rows | classes C2 and C7 stay low | row cap guidance; a second session on slow-luna panels; measured by rows per run |
| Reviewer picks the wrong criteria to ledger | misses the trigger | recipe text starts with the lexical cue ("every, all, each ..."); this is the weakness a script (Redesign A) removes |
| Second ember session shares ember's bias | echo, not new coverage | the lens is different and the session is fresh; ledgers are blind to pass A |
| Wrong blockers grow | same as A | MISMATCH needs two quotes; auto-promoted rows are MINOR; wrong-blocker gate in section 5 |
| Time | luna's ledger tokens slow it | `timeout D`; ledger row cap; second ember pass guarded by 0.45 x D |
| Kills at D | lost reports | kill rate gate |

---

## 4. Comparison of the two redesigns

| Dimension | A: Probe Sheet | B: Lens Ledger |
|---|---|---|
| Core mechanism | script extracts items; model judges one item at a time | recipes force the model to enumerate before judging |
| Who finds the trigger text | the script | the model |
| Theories addressed | T1 and T2 primary; T3 shared | T2 primary; T1 secondary; T3 shared |
| Strong on | C4, C5, C8 (mechanical triggers) | none strong; best C4, C8 |
| Weak on | C3, C7 narrow form | C1, C2, C3, C7 (compliance by a terse model) |
| Expected total found /14 (low-high) | 3.4-6.1 | 2.8-5.5 |
| Redesign share of the gain | +1.40 to +3.60 | +0.75 to +3.00 |
| Control package I7 | +0.55 to +0.85 | +0.20 to +0.50 |
| Issues at "consistent" (at least 0.5, middle) | 3 (I4, I5, I7) | 0 |
| Elapsed (ember + 2x luna), expected / modelled worst | +15% / +36% (kill-limited at +35%) | +13% / +30% |
| Output tokens (ember + 2x luna) | +26% | +42% |
| Effort (new lines, with shared scaffolding) | about 1,300-1,500 | about 700-950 |
| Needs a deterministic component | yes (extractors, per target adapter) | only the ledger check |
| Portability to a target with no adapter | falls back to the isolated brief | works with a prompt-only change |
| Maintainability seam | extractor modules per class plus adapters; fixture-tested | recipe cards only; no code per class |
| Main risk | extractors miss or over-extract; sheet anchors reviewers | models do not comply; recall depends on model discipline |
| Wrong-blocker risk | moderate (items invite PROBLEM answers) | moderate (ledger rows invite MISMATCH answers) |

My recommendation to the debate: run both in the section 5 experiment. If forced to choose without data, A has the higher expected reach for the classes with mechanical triggers, and B is the cheaper fallback. The shared scaffolding in 3.0 is needed by both, so build it first.

---

## 5. Validation experiment (no reuse of the design data)

**Data not reused.** The ten issues came from three study packages. Those packages are the development set only. They are re-run for regression, and they are not evidence for adoption.

**Hold-out material** (from IG section 4; none from the three study packages):

| Hold-out | Content | Items | Work |
|---|---|---|---|
| H5 | docs-only plan | 11 | about 1 hour |
| H2 | plan | 4-8 | about 1 hour |
| H4 | plan | 12 | 1-2 hours |
| H3 | larger plan | 9 important | about half a day |
| H1 | spec with a validated 44-defect ledger (use the 20 blocking rows); depth on a spec target; tuned on by the earlier #346 designs but not by these designs | 20 | about 1 hour |
| H6 | sanity only; 3 items, same pipeline and period as a study package | 3 | low |

- The fast trio is H5 + H2 + H4 (about 25 items, 3-4 hours). Add H3 for volume and H1 for the spec target.
- Ground truth for each is written from the existing review reports and plan quotes, by a person or agent who has not seen this spec's recipes. Any recorded implementation outcome sets the `blocking` flag.

**Documentation arm.** Take the delivered documents that carried a false universal sentence and drew a blocking retry finding (IG section 2, C6 implementation cases, about 8). Review each at the commit before the fix. Ground truth is the recorded retry finding. Whether the pre-fix text can be recovered from git must be checked before use.

**Cautions (IG section 4).**
- Remove `.dev/reflect/`, the package's `artifacts/` and `progress.md` from every sandbox.
- Verify the plan reviewed equals the plan in the package (sha256 against the ledger line; not yet checked, UNVERIFIED).
- Ground truth from Tier-2 reports is capped at what those reviewers found, so "missed by cheap panels" must be measured by running the cheap panels.
- The class definitions came from the study packages, but IG section 2's recurrence evidence cites reports for H2-H5. Recipe wording must be frozen before the hold-out ground truth is written, and authors must not copy the wording of those reports.

**Arms (ember + 2x luna unless noted)**

| Arm | Description | Purpose |
|---|---|---|
| A0 | current harness, no fixes | context only (shows how much the fixes alone move) |
| A1 | isolated panel with H1-H4 and CB1-CB4 | **the control to beat** |
| A2 | Redesign A + fixes | test |
| A3 | Redesign B + fixes | test |
| A4 | A1 plus a one-paragraph generic checklist ("also check for every/all claims, commands that cannot match, stale copies, dependent tests, dropped source rules") with no recipes and no ledger | tests whether recipes and scaffolding beat a plain checklist |
| Stage 2 | the winning redesign on haiku + 2x luna and sonnet + 2x luna against A1 for the same models | adaptation |

**Runs per arm.** 6 runs per arm per package (as in the earlier replicate batches). Core arms A1-A4: 4 arms x 5 packages (H5, H2, H4, H3, H1) x 6 runs = 120 panel runs (about 360 reviewer sessions; Redesign B adds second ember sessions). A0: 3 packages x 6 runs. Documentation arm: 8 documents x 3 arms (A1, A2, A3) x 4 runs = 96 panel runs. Stage 2: 2 panels x 2 arms x 3 packages x 4 runs = 48 runs. One blind Opus judge per run-package against the ground truth, with a second judge on a 15% sample.

**How consistency is measured**
- Per item: reach rate = runs that found it / runs (6).
- **Consistent** = reached in 4 or more of 6 runs. **Usually** = 3 of 6.
- Primary consistency metric: the share of hold-out items that are consistent, per arm, plus per-class reach.
- Secondary: mean found fraction per run; share of runs that find at least half the items; run-to-run overlap (Jaccard) of the found sets; wrong blockers per run; judged-blocking precision; elapsed seconds; output tokens; kill rate; fallbacks used.
- Confidence: bootstrap over items and runs; Wilson intervals for item reach rates.

**Pre-registered decision rule** (file committed before the first run, with the registry tag, the analysis script and the ground-truth hashes):

| Gate | Criterion (versus A1, pooled over the hold-out packages) |
|---|---|
| G1 consistency | share of consistent items rises by 20 or more percentage points, and the 90% bootstrap lower bound is above 0 |
| G2 mean found fraction | gain of 8 or more points; paired permutation test over run-package units, one-sided p below 0.05 |
| G3 wrong blockers | wrong blockers per run at most A1 + 1.0; judged-blocking precision not more than 10 points below A1 |
| G4 time | median elapsed at most 1.35 x A1's median per package; 90th percentile at most 1.50 x; kill rate 10% or less |
| G5 beats the checklist | gain over A4 of 4 or more points on G2's metric; otherwise the recipe and script machinery is not justified and A4 wins |
| G6 no class regression | no class's reach rate more than 15 points below A1 |
| G7 documents and spec | on the documentation arm and on H1, G2 holds with the lower bound above 0; otherwise the redesign may be adopted for plans only and the broad-applicability claim is withdrawn |

Outcomes:
- If both A2 and A3 pass: adopt the one with the larger G2 gain (A2 if tied, because of the more consistent reach).
- If one passes: adopt that one.
- If neither passes: keep A1 and record the per-class results.
- Stage 2 runs only for the adopted redesign.

Development-set regression: re-run A1, A2, A3 on the three study packages. A result below A1 is treated as a bug, not as evidence.

---

## 6. Numbered, testable requirements

**Harness fixes and brief**

| # | Requirement | Test |
|---|---|---|
| REQ-01 | The review brief contains a `{{SOURCE}}` placeholder; the harness aborts if the source file is missing | render the brief; assert the path appears; run with a missing source and assert abort |
| REQ-02 | The merge truncates an over-long anchor (to 200 characters, still a substring of the candidate) and claim (to 300) instead of dropping the finding | unit test with a 250-character anchor and a 400-character claim; the finding survives |
| REQ-03 | The sandbox is checked out at the plan's base commit | assert a file created by the package's implementation is absent |
| REQ-04 | The sandbox holds no `.dev/reflect/`, `.dev/tasks/`, `.dev/eval-workspaces/`, no report about the package, and no ground-truth file | `find` and `grep -r` return nothing |
| REQ-05 | CB1-CB4 are present verbatim in the brief; the six findings categories are unchanged | string match; set equality of categories |

**Registry and scaffolding**

| # | Requirement | Test |
|---|---|---|
| REQ-06 | Every card validates against the schema; v1 has 8 cards; `recipe_text` is at most 120 words; each card has at least 2 `instances` outside the study packages | schema test and word count |
| REQ-07 | A lint step fails if any recipe, question or brief text contains a 4-word sequence from any `description` or `plan_quote` in any `ground-truth.json`, or a package, task or file name from the study | run on the real cards; run on a seeded leak and assert failure |
| REQ-08 | Rendered briefs contain no `src/superclaude/` path; cards are reached through the CLI | `grep` on rendered output |
| REQ-09 | A new class is added by one card (and optionally one extractor module) with no dispatcher change | add a fixture card; assert it appears in the sheet or lens |
| REQ-10 | Findings may carry `class` and `probe` keys; the existing merge and ledger tests still pass | run the existing test suite with extra keys |
| REQ-11 | If the probe, lens renderer or ledger check fails, the harness runs the isolated brief and records `fallback=true` | force an extractor exception and assert fallback |

**Redesign A**

| # | Requirement | Test |
|---|---|---|
| REQ-12 | The probe writes only to its output directory and runs no repository code | run under a read-only mount of the sandbox |
| REQ-13 | The probe finishes within 12 s on every hold-out package or is killed and falls back | time it; assert `timeout` behaviour with a sleep stub |
| REQ-14 | The probe output is deterministic and has at most 12 items per reviewer | run twice and compare bytes; count items |
| REQ-15 | On a fixture suite of at least 3 non-study plans with seeded defects, E1-E4 reach recall of 0.8 or more; item precision is reported | fixture test |
| REQ-16 | A PROBLEM row whose quotes are not substrings of the plan, the source or the recorded tool output is demoted to non-blocking | unit test |
| REQ-17 | A PROBLEM row with no findings line is promoted to a MINOR non-blocking finding using the item's `anchor_text` | unit test |

**Redesign B**

| # | Requirement | Test |
|---|---|---|
| REQ-18 | Lens routing and replicas are read from the panel template data (C1 and C6 have 2 replicas) | change the data; assert routing changes without a code change |
| REQ-19 | Each lens session must contain a ledger row or `NONE FOUND` per required check; non-compliance is logged | feed reports with and without ledgers |
| REQ-20 | Ember pass B launches only if pass A ended before 0.45 x D | stub reviewer with a controlled duration |
| REQ-21 | A MISMATCH row with no findings line becomes a MINOR non-blocking finding only if its quote is a substring of the plan or the source | unit test |

**Time**

| # | Requirement | Test |
|---|---|---|
| REQ-22 | Each reviewer session is killed at D = floor(1.35 x b) for its package, using the named baseline medians | stub reviewer that sleeps past D |
| REQ-23 | In the experiment, the median elapsed time of each redesign arm is at most 1.35 x A1's median per package, 90th percentile at most 1.50 x, kills at most 10% | measured over 6 or more runs per package |
| REQ-24 | The pre-pass and ledger-check wall times are measured and reported | timing log in every run |

**Contamination and overfitting**

| # | Requirement | Test |
|---|---|---|
| REQ-25 | Recipes, questions, extractors and the registry version are frozen by git tag before hold-out ground truth is written; the tag is in the pre-registration | tag date earlier than the ground-truth commit date |
| REQ-26 | Reviewers never receive ground truth, and the hold-out sandboxes exclude reflect reports | `grep -r` for ground-truth file names and report folders returns nothing |
| REQ-27 | Extractor patterns pass on at least 3 plans not used to write them | fixture test |
| REQ-28 | One leave-one-class-out ablation per class is run on the hold-out, and other classes' reach changes by at most 15 points | ablation report |

**Applicability**

| # | Requirement | Test |
|---|---|---|
| REQ-29 | A spec adapter and a documentation adapter exist with fixture tests; E1, E2 and E5 produce items on a spec fixture; E4 and E1 produce items on a documentation fixture | fixture tests |
| REQ-30 | The registry README lists, for each new target type, what must be re-derived (block patterns, command syntax, test and root-document paths, severity guidance) | review of the document |

**Safety and quality**

| # | Requirement | Test |
|---|---|---|
| REQ-31 | A finding derived from a probe item or ledger row can be blocking only with the grading sentence and two quotes or a search result | unit test on the check |
| REQ-32 | The reviewers stay read-only: edit tools are disallowed as today, and the probe is run by the harness | existing disallowed-tools list unchanged; probe invoked outside the reviewer session |
| REQ-33 | Non-probe findings per run, displacement of the easy finds (B3, I2 and similar) and wrong blockers per run are reported for every arm | analysis script output |

**Validation**

| # | Requirement | Test |
|---|---|---|
| REQ-34 | The arms, run counts, consistency definition and decision rule in section 5 are committed as a pre-registration before the first hold-out run | commit order |
| REQ-35 | Each run is judged blind by Opus against ground truth, with a second judge on a 15% sample; a judge API error is audited per batch | audit log |
| REQ-36 | The report states, for every class, the hold-out reach rate with its interval, and states plainly any class whose reach did not improve | report review |
| REQ-37 | A failed decision rule is reported as a negative result, and the isolated panel with harness fixes stays the default | report review |

---

Not checked: all probabilities, token rates (luna 48 tokens/s is derived from medians and not confirmed as generation-bound), and the 6 s pre-pass time are estimates. `claude --max-turns` was not found in `claude --help`, so the spec relies on `timeout` only. Whether unknown keys in findings-v1 are accepted comes from the hand-off notes, not from a test I ran.
