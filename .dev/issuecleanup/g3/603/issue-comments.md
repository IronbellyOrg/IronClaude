## Comment 0 | https://github.com/IronbellyOrg/IronClaude/issues/603#issuecomment-6955999091 | 2026-11-17T17:40:52Z

## Phase 2 findings: verdicts (both REFACTOR VALUABLE)

Produced by the Phase 2 agent (analysis only; no product file was changed). Source file in the working tree: `.dev/issues/603/phase2/verdicts.md` (not committed).

# Verdicts: spec-panel and the Review Panel for reviewing `/sc:design` output (issue #603, Phase 2)

Sources: `analyze-spec-panel.md`, `analyze-review-panel.md` and `design-review-phase.md` in this folder. Every `file:line` below was Read in this session. "Design" means a `/sc:design` output (HOW we build); "spec" means a requirements specification (WHAT we build); "plan" means an implementation plan.

## Verdict lines

- **`/sc:spec-panel`: REFACTOR VALUABLE**
- **Review Panel (`src/superclaude/cli/review/` + its data and briefs): REFACTOR VALUABLE**

Neither is NECESSARY for issue #603's acceptance criteria: the loop can run on a design today, fix blocking findings and stop at the cap (`design-review-phase.md` §6, §12). Neither is NO CHANGE NEEDED: both miss the defect class that matters most in a design (disagreement with the code), and the ledger cannot drop a wrong blocker without a person.

## `/sc:spec-panel`: reasons, ranked by consequence

1. **No check against the repository.** No step, expert or tool reads source code (`spec-panel.md:30-35`, `:91-97`, `:218-225`; MCP list `:6` has no codegraph); "Consistency" is "internal coherence" (`:446`); the first-review brief says "against the requirements it states" (`document_review_loop_prompts.md:32`). A design that names a wrong signature or a module that does not exist passes review.
2. **The grading the reviewers follow cannot make a code mismatch blocking.** The prompts file's three blocking cases are internal contradiction, data loss/safety, unpassable acceptance check (`document_review_loop_prompts.md:31`); the command's own wording is broader ("a concrete wrong outcome an implementer would produce", `spec-panel.md:259`). The prompts file is the hard gate (`spec-panel.md:266-268`), so the narrow list wins, and a coordinator cannot widen it by brief (`spec-panel.md:264`).
3. **Unattended TDD block.** A long design can score 5+ on the TDD detector (`spec-panel.md:36`) and then resolves as blocked without `--target-release` (`:463`). Worked around by the caller (`design-review-phase.md` §5), not fixed.
4. **Roster has no owner for data-model correctness, consumer impact, or migration/rollout/rollback** (`spec-panel.md:53-89`; Newman's "backward compatibility" `:61` is the nearest).
5. **What fits unchanged** (not a reason to refactor): the Review Loop (`:256-264`), Whittaker's attacks (`:76-80`), the Guard table (`:311-334`), Pipeline analysis (`:347-394`), Fowler/Nygard/Newman/Hohpe/Crispin lenses.

## Review Panel: reasons, ranked by consequence

1. **A wrong blocker cannot leave the ledger without a person.** Reviser-rejected rows stay `open` (`ledger.py:340-342`); prior lines never change status (`:259-272`); only the human `ledger defer` clears one (`:350-360`; `ledger_cmd.py:83-84`). Unattended design loops will end ESCALATE whenever one wrong blocker is not re-reported as non-blocking.
2. **OR-merge of blocking calls** (`ledger.py:187`, `:213-218`); `overlap` confidence is unused in the verdict (`:86-90`, `:99-104`). Combined with the measured ~70% wrong blocking rows on plans (`EXPERIMENT-REPORT.md:67`), more reviewers mean more false failures.
3. **No code grounding in the spec-panel merge path.** findings-v1 has only an anchor in the candidate (`findings.py:90-121`); the code-citation machinery (findings-v2 `source` citations, `verify-citations`) exists but only reflect uses it (`findings_v2.py:35-81`; `verify_cmd.py:1-12`; `merge_cmd.py:109` parses v1).
4. **A panel chooses models only; every reviewer gets the same brief** (`panel.py:37-46`; `document_review_loop_prompts.md:70`). The eval's recall gains came with seat lenses the product does not have (`EXPERIMENT-REPORT.md:14`, `:27`).
5. **What already allows a design configuration without code:** packaged templates selected by `@name` (`panel.py:430-454`; `panel_cmd.py:19-25`), tiers as data (`panel.py:1-7`), project/user override files (`panel.py:397-419`), coordinator-assigned personas by resolution order (precedent `sc-reflect-protocol/SKILL.md:341`).

## Gaps

| ID | Gap | Document type affected | Evidence | Consequence for reviewing a design |
|---|---|---|---|---|
| G-1 | No reviewer step, tool or expert checks the document against the repository | Design (also plans that cite code) | `spec-panel.md:30-35`, `:6`, `:446`; `document_review_loop_prompts.md:32` | Wrong names, signatures, files and layers pass review |
| G-2 | Blocking cases in the prompts file exclude "contradicts the code"; command and prompts disagree on the blocking definition | Design, spec, plan | `document_review_loop_prompts.md:31` vs `spec-panel.md:259` | A found code mismatch is graded Medium and never revised |
| G-3 | No finding category for code mismatch, consumer break or rollout | Design | `findings.py:15-22` | Such findings land in `other` / `missing-requirement`; no rule can treat them differently |
| G-4 | No expert or check for consumer impact / blast radius of a changed interface | Design | `spec-panel.md:56`, `:142-151` | Breaking changes to existing callers go unflagged |
| G-5 | No expert or check for data-model correctness (keys, constraints, migration of existing data) | Design (`--type database`) | `spec-panel.md:198`, `:210-216` cover state variables only | Schema defects are reviewed only if they create an internal contradiction |
| G-6 | Migration, rollout and rollback are not a lens; omissions are Medium by rule | Design | `spec-panel.md:61`, `:288`; `document_review_loop_prompts.md:31` | Missing rollback never blocks; acceptable if stated as a known limit, but no reviewer is asked to look |
| G-7 | Unattended TDD-detector block on long designs | Design | `spec-panel.md:36`, `:463` | Nested spec-panel returns blocked unless the caller passes `--target-release` |
| G-8 | Reviser-rejected blockers stay open; only a person clears them | Design, spec, plan | `ledger.py:340-342`, `:350-360` | Unattended loops escalate on wrong blockers |
| G-9 | OR-merge of blocking with unused agreement signal | Design, spec, plan | `ledger.py:187`, `:86-104` | False blockers scale with panel size |
| G-10 | Code-citation verification exists only on the reflect path | Design, plan | `findings_v2.py:35-81`; `verify_cmd.py:1-12`; `merge_cmd.py:109` | A reviewer's "X does not exist" is accepted unchecked |
| G-11 | Panel template has no lens/persona/brief field; all reviewers share one brief | Design, spec, plan | `panel.py:37-46`; `document_review_loop_prompts.md:70` | Reviewer diversity is model-only |
| G-12 | Pinning a second specific model needs a one-model tier plus a gateway alias | All | `panel.py:245-246`, `:544-547`; `review-panel.live7.json:5` | The eval's "anchor + accurate seat" rule needs data and ops work |
| G-13 | In anthropic-only the default resolves Sonnet + 3 Haiku (soft distinctness) | All | probe 2026-11-17; `panel.py:539-543`; `review-tiers.default.json:31-35` | "Four different models" holds only on the gateway |
| G-14 | No evaluation on design documents | Design | `EXPERIMENT-REPORT.md:13`; `RESULTS.md:40` ("plans only") | Every model-mix choice for designs is unmeasured |

## Not verified

- Recall and wrong-blocker rates of any panel on design documents (no runs exist). UNVERIFIED; it did not drive either verdict.
- That the product default template shares the eval's ~70% wrong-blocker rate: the eval panels used different models (`muse-ember-1.0` is not in the product tier file, `review-tiers.default.json:12-17`) and seat lenses (`EXPERIMENT-REPORT.md:14`). UNVERIFIED; used only as context for G-9.
- How often real `/sc:design` outputs trip the TDD detector (rule read, not run). UNVERIFIED.
- Whether reviewer Agents have the Augment code-search tool, and whether they open source files unprompted. UNVERIFIED.
- Gateway availability of the models and aliases a design template would name (`review-tiers.default.json:26`). UNVERIFIED.

## Questions a brainstorm must settle

1. Is the repository a "stated truth" a design can contradict, so that a code mismatch with a verified `file:line` is blocking (G-1, G-2)? If yes, does the rule live in spec-panel (a design focus) or only in the `/sc:design` coordinator?
2. Who checks the code: a dedicated reviewer lens, the coordinator after the merge (`design-review-phase.md` §7.1), or a mechanical pre-merge citation check (G-10)?
3. How does a wrong blocker leave the ledger in an unattended run: a `withdrawn` prior status, "reviser rejected + next reviewer agrees", a quorum rule using `overlap`, or never (G-8, G-9)?
4. Which new finding categories are worth a schema change (G-3), and does any of them change grading?
5. Are omissions of rollback, migration or failure handling ever blocking in a design, or always Medium (G-6), given the #346 growth problem?
6. Design panel shape: how many reviewers, which tiers, which lens per seat, and does a re-review keep one reviewer (G-11, G-12)?
7. What evidence is required before changing a default: a design answer key and an interleaved test like `RESULTS.md`, or ship a data-only `@design` template as opt-in first (G-14)?
8. Does `/sc:design`'s review phase ship before these answers (using today's spec-panel and default panel), or wait for them (`design-review-phase.md` Q-7)?
9. Should spec-panel's unattended TDD gate apply only with `--improve` (G-7)?


<!-- sc:issue-603:verdicts -->


## Comment 1 | https://github.com/IronbellyOrg/IronClaude/issues/603#issuecomment-6955999726 | 2026-11-17T17:40:53Z

## Phase 2 findings: analysis of /sc:spec-panel for reviewing designs

Produced by the Phase 2 agent (analysis only; no product file was changed). Source file in the working tree: `.dev/issues/603/phase2/analyze-spec-panel.md` (not committed).

# Analysis: does `/sc:spec-panel` review a technical design (HOW) as well as a specification (WHAT)?

**Command:** `/sc:analyze src/superclaude/commands/spec-panel.md src/superclaude/rules/prompts/document_review_loop_prompts.md --focus quality --depth deep`
**Date:** 2026-11-17. **Scope:** `spec-panel.md` (491 lines), `document_review_loop_prompts.md` (75 lines), the finding schema it feeds (`src/superclaude/cli/review/findings.py`), the ledger rules that act on its findings (`ledger.py`), and the rf-qa Fix Cycle it defers to (`src/superclaude/agents/rf-qa.md:381-393`). Every `file:line` below was Read in this run.

Codegraph: index_state=fresh, checked_at=2026-11-17T17:34:46Z; degraded: none (the two targets are Markdown, which codegraph does not index, so every claim comes from Read and Grep).

---

## 1. Answer in one paragraph

Spec-panel can run on a `/sc:design` document today and will catch what any careful reader catches: two parts of the document that contradict each other, a stated step that loses data or breaks a safety boundary, an acceptance check that cannot pass, and (with `--focus correctness`) unguarded edge cases and count mismatches in data flows. It is **not** built to check the things that make a HOW document wrong in practice: whether the names, signatures, files and layering it describes exist in the repository; what a proposed change to an existing interface breaks; whether a data model is correct; and whether migration, rollout and rollback are covered. Nothing in the command or the prompts tells a reviewer to open the repository, no expert owns those checks, the finding schema has no category for them, and the grading rule the reviewers follow makes "the design disagrees with the code" and "the design leaves out a failure mode or a rollback" non-blocking by construction. The review loop mechanics (cap, re-review scope, reviser contract) fit a design document unchanged.

## 2. What spec-panel says it reviews

| Evidence | What it shows |
|---|---|
| `spec-panel.md:14-17` (Triggers: "Specification quality review", "Requirements analysis and completeness verification") | The command's stated object is a specification of requirements |
| `spec-panel.md:30-35` (Behavioral Flow: Analyze specification, Assemble experts, Review, Collaborate, Synthesize, Improve) | No step reads anything other than the document |
| `spec-panel.md:490` ("After review, incorporate feedback into spec, then use `/sc:design` for architecture") | The command places itself *before* `/sc:design` in the workflow, not after it |
| `spec-panel.md:284-290` (Output when input is a TDD: covers §6 Architecture, §7 Data Models, §8 API Specifications, §13 Security, §15 Testing, §20 Risks) | Spec-panel has *some* design-document awareness, but only for the `/tdd` template, detected by template-specific signals (`spec-panel.md:36`), and its purpose there is to scope a release spec for `/sc:roadmap` (`:288`) |
| `spec-panel.md:6` (`mcp-servers: [litellm, context7]`), `:91-97` (MCP Integration: Context7 "for specification patterns, documentation standards") | No codegraph; the code-search tool behind `litellm` is never mentioned; Context7 is used for generic patterns, not for this repository |
| `spec-panel.md:218-225` (Tool Coordination: Read the specification, Grep "cross-reference validation and consistency checking") | Grep is listed, but its target is not named and no step uses it against source code |
| `spec-panel.md:446` (Quality Metrics: Clarity, Completeness, Testability, Consistency "internal coherence") | Consistency means internal coherence only |

## 3. Expert roster and lenses against design-document concerns

| Expert (`spec-panel.md` line) | Lens as written | Useful for a HOW document? |
|---|---|---|
| Wiegers (53, 103) | SMART criteria, testability of requirements | Partly: the design's acceptance checks |
| Adzic (54, 104) | Given/When/Then examples | Partly: behaviour examples of an interface |
| Cockburn (55, 105) | Use cases, primary actor, business goal | Little: a design inherits these from its spec |
| Fowler (56, 106) | Interface segregation, bounded contexts, refactoring | Yes: interface and boundary quality, *as described in the document* |
| Nygard (60, 107) | Failure modes, circuit breakers, monitoring, recovery | Yes: failure-mode coverage |
| Whittaker (71-85, 108) | Zero/empty, divergence, sentinel, sequence, accumulation attacks on stated invariants | Yes for stateful designs; scope is "specification correctness" only (`:85`) |
| Newman (61, 109) | Service decomposition, API versioning, backward compatibility | Yes: API evolution; the nearest thing to a migration lens |
| Hohpe (62, 110) | Message exchange, ordering, delivery guarantees | Yes for integration designs |
| Crispin (66, 111), Gregory (67, 112) | Test strategy, edge cases; workshops, three amigos | Crispin yes (testability); Gregory little (team process) |
| Hightower (89, 113) | Cloud-native deployment, operational observability | Partly: deployment and observability |

Missing from the roster, with no expert, focus area or attack covering them:

1. **Consistency with the existing code**: does each named module, class, function, file path and signature exist and match? No expert, no step, no tool (section 2).
2. **Dependency and blast radius**: who calls the interface the design changes, and what breaks. Fowler's lens is interface *quality*, not consumer impact.
3. **Data-model correctness**: keys, constraints, normalisation, nullability, ownership, migration of existing rows. No data-modelling expert; FR-14.1 (state assumptions, `:198`) and the State Variable Registry (`:210-216`) cover in-memory state variables, not schemas.
4. **Migration, rollout and rollback**: ordering of deploy steps, feature flags, reversibility, coexistence of old and new versions. Newman's "service evolution" (`:61`) touches API versioning only; the TDD output mentions a "migration plan from TDD §19" only as an extraction target for a release spec (`:288`).
5. **Security of the design**: only under `--focus compliance` ("Security specifications and threat modeling", `:170`), led by a requirements expert (`:166`).
6. **Performance and capacity**: "Scalability and maintainability characteristics" is one bullet of the architecture focus (`:149`); no expert owns it.

## 4. Review criteria and grading rules

### 4.1 The two blocking definitions disagree, and the narrower one is the one reviewers follow

- Command, Review Loop bullet 2 (`spec-panel.md:259`): a MAJOR or FR-8/FR-9 finding is blocking "only if it names a **concrete wrong outcome an implementer would produce** or a security, data-loss or safety-boundary risk".
- Prompts file, FIRST-REVIEW grading check (`document_review_loop_prompts.md:31`): blocking needs "**two stated texts that contradict each other**, a stated text that causes data loss or breaks a security or safety boundary, or a stated text that an acceptance criterion cannot pass"; a finding that is "a requirement the document never states (a missing restriction, an undefined state, an unspecified edge case) rather than a stated text that does harm" is Medium.

The prompts file is a hard gate the reviewer must follow step by step (`spec-panel.md:266-268`), so its three-case list is what reviewers apply. The command's wording would admit "the design names `foo(a, b)` but the code has `foo(a)`: an implementer builds a call that fails" as blocking; the prompts file's list does not contain it (the code is not a "stated text" of the document, and it is not data loss, safety or an acceptance check unless the design happens to state one). The finding schema mirrors the narrow list: `category` is one of contradiction, unpassable-check, data-loss, safety, missing-requirement, other (`findings.py:15-22`; `document_review_loop_prompts.md:60`).

### 4.2 Fit of the critique grading to a design document

| Design defect class | How the grading treats it | Fit |
|---|---|---|
| Two sections of the design contradict (sequence says A then B, API table says B then A) | Blocking (contradiction) | Good |
| A step loses data or opens a security hole (migration drops a column before copying) | Blocking (data-loss / safety) | Good |
| A stated acceptance check cannot pass | Blocking (unpassable-check) | Good, when the design states checks; `/sc:design` output is not required to |
| Design contradicts the existing code (wrong signature, non-existent module, wrong layer) | No category; not in the three-case list; at best `other`, graded Medium | **Poor**: the most consequential HOW-document defect cannot fail a review |
| A change breaks existing consumers the design does not mention | "A requirement the document never states" → Medium | **Poor** |
| Missing failure mode, missing rollback, missing migration step | Omission → Medium by rule (`prompts:31`) | **Poor**: in a design these omissions are where outages come from, but the rule is deliberate (it stopped reviews from failing on additions, #346) |
| Wrong data model (missing unique key that the design's own flow relies on) | Blocking only if two stated texts conflict; else Medium | Mixed |
| Dimensional mismatch in a stated pipeline | CRITICAL, so blocking (FR-19, `:370-372`; CRITICAL is blocking, `:259`) | Good |
| Guard with unspecified behaviour | FR-8/FR-9 finding, graded by `:259` / `:332-333` | Good, but FR-10 makes the full table a hard gate (`:334`), which is heavy on a design with many timeouts and thresholds |

The omission rule is right for the loop's purpose (it keeps revisers from growing the document), so the gap is not "grade omissions as blocking". The gap is that a design has a second source of truth, the repository, and a contradiction with it is a stated text that does harm; the grading list has no way to say so.

### 4.3 FR-n rules and mandatory artifacts

- FR-2.1 to FR-2.5 Whittaker attacks (`:76-80`) and the Guard Condition Boundary Table (`:311-334`) probe *stated invariants and guards*. They transfer to stateful designs (retry counts, timeouts, queue limits) unchanged.
- FR-14 correctness shifts (`:194-208`) and the State Variable Registry (`:210-216`) are written for "stateful specifications" (`:180`) and fit a design's state machines.
- Pipeline Dimensional Analysis (`:347-394`) fits data-flow designs well.
- None of the FR rules references code, consumers, schemas or rollout.

## 5. What a reviewer is actually told

- First-review brief (`document_review_loop_prompts.md:32`): "Review the candidate ... **against the requirements it states** ... Inspect behavior and **the dependencies it touches**." The second sentence is the only opening for a code check, and it is undefined: dependencies of the document, of the behaviour, or of the code? Nothing names the repository, codegraph, Grep or a `file:line` evidence rule.
- Re-review brief (`:48`): "for inherited text, cite the changed line it depends on" (a line of the document, not of the code).
- Precedence (`spec-panel.md:264`; `prompts:72-74`): a brief "may narrow this scope; it may not widen it". A coordinator such as `/sc:design` therefore cannot legitimately add "check every signature against the repository" to the brief: that widens the review past what the command defines. A code check has to live in the command (or in the coordinator outside the review, as `design-review-phase.md` section 7.1 does).
- Re-check of prior blockers defers to rf-qa's Fix Cycle steps 1-5 (`spec-panel.md:262`; `rf-qa.md:386-393`), which are document-agnostic and fit designs.
- Contrast inside this repo: the `/tdd` skill, the repo's heavier design path, does not use spec-panel and states that "every claim [goes] through codebase verification" (`src/superclaude/skills/tdd/SKILL.md:20`). The repository's own design tooling treats code verification as the core check that spec-panel lacks.

## 6. Other quality findings

| ID | Severity | Finding | Evidence |
|---|---|---|---|
| SP-Q1 | High | Under `--unattended`, a design document that scores 5+ on the TDD detector resolves as blocked unless `--target-release` is passed, although the release scoping only matters to the Improve step | `spec-panel.md:36` (detector: numbered `## N.` headings up to +3, "Data Models" / "API Specifications" / "Component Inventory" +1 each), `:463` |
| SP-Q2 | High | The two blocking definitions differ (section 4.1); reviewers follow the narrower | `spec-panel.md:259` vs `document_review_loop_prompts.md:31` |
| SP-Q3 | High | No instruction, tool or expert for checking a document against the repository | sections 2, 3, 5 |
| SP-Q4 | Medium | No finding category for a code mismatch, consumer break or rollout gap; they collapse into `other` / `missing-requirement`, which the ledger cannot tell apart from document-only defects | `findings.py:15-22` |
| SP-Q5 | Medium | Critique output buckets are named `=== REQUIREMENTS ANALYSIS ===`, `=== ARCHITECTURE ANALYSIS ===` (`:123`); a design gets a requirements bucket it mostly cannot fill, and no bucket for code consistency or rollout | `spec-panel.md:123` |
| SP-Q6 | Medium | When the Improve step runs (attended first review), it writes an "enhanced specification" (`:35`), not a revised design; the loop's reviser contract is the safer path for a design | `spec-panel.md:35`, `:463`, `:263` |
| SP-Q7 | Low | "Next Step" sends the user to `/sc:design` after a review (`:490`); for a design reviewed after `/sc:design` this is circular | `spec-panel.md:490` |
| SP-Q8 | Low | "Quality Assurance Features" and "Advanced Features" (`:443-453`) list capabilities (recommendation effectiveness tracking, CI/CD validation, custom quality criteria) that no step implements | `spec-panel.md:443-453` |

## 7. What fits unchanged

- The Review Loop: one review per run, `review: N of 3`, the cap "at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings", re-review limited to changed lines plus prior blockers, the Reviser brief and contract (`spec-panel.md:256-264`).
- The prompt set, findings block and fix map formats (`document_review_loop_prompts.md:27-66`): they anchor on exact quotes of the candidate, which works for any Markdown document.
- Nygard, Fowler, Newman, Hohpe, Whittaker and Crispin, as reviewers of what the design *says*.

## 8. Recommendations (smallest first)

1. **Pass `--target-release` from any coordinator under `--unattended`** (no spec-panel change), or narrow `spec-panel.md:463` to runs with `--improve`. Fixes SP-Q1.
2. **Make the command and the prompts file say the same thing about blocking** (SP-Q2). If the repository counts as a source of stated truth for a design, add one case to `prompts:31`: "a stated name, path or signature that contradicts the code at a cited `file:line`". This is a one-line rule change plus one category value (`code-mismatch`) in `findings.py:15-22` (which `findings_v2.py` imports) and the prompts file's category list (`:60`).
3. **A design lens, not a panel of new experts:** a `--focus design` that keeps Fowler, Nygard, Newman, Whittaker and Crispin, drops Cockburn and Gregory, and adds three checks with a tool rule: code consistency (codegraph or Grep, `file:line` required), consumer impact, rollout/rollback. Owned by the command, so the "brief may not widen" rule (`:264`) is respected.
4. **Keep code re-grounding in the coordinator** until 2 and 3 exist: `/sc:design` already has the codegraph machinery (`design.md:51-74`), and `design-review-phase.md` section 7.1 uses it on revised lines.

## 9. Not verified

- Whether spec-panel reviewers in practice open source files on their own when given a design: no run of spec-panel on a `/sc:design` output was found or performed (UNVERIFIED).
- How often a real `/sc:design` output reaches a TDD-detector score of 5 (UNVERIFIED; the detector rule is read, not run).
- Whether the `litellm` server in a reviewer's context exposes the Augment code-search tool to spec-panel runs (it does in this session; not checked for reviewer Agents).


<!-- sc:issue-603:analyze-spec-panel -->


## Comment 2 | https://github.com/IronbellyOrg/IronClaude/issues/603#issuecomment-6956000132 | 2026-11-17T17:40:54Z

## Phase 2 findings: analysis of the Review Panel and its configuration

Produced by the Phase 2 agent (analysis only; no product file was changed). Source file in the working tree: `.dev/issues/603/phase2/analyze-review-panel.md` (not committed).

# Analysis: would a design-specific Review Panel configuration review `/sc:design` output better?

**Command:** `/sc:analyze src/superclaude/cli/review/ src/superclaude/cli/review/data/ src/superclaude/rules/prompts/document_review_loop_prompts.md src/superclaude/commands/spec-panel.md --focus architecture --depth deep`
**Date:** 2026-11-17. **Scope:** `panel.py`, `panel_cmd.py`, `findings.py`, `findings_v2.py`, `ledger.py`, `ledger_cmd.py`, `merge_cmd.py`, `fixcheck.py`, `fixcheck_cmd.py`, `verify_cmd.py`, `__init__.py`; `data/review-panel.{default,live7,reflect-pre}.json`, `data/review-tiers.default.json`; the reviewer brief section of the prompts file; the evaluation reports `.dev/eval-workspaces/tasklist-review-panel/20261116-stronger-panel/EXPERIMENT-REPORT.md` and `20261117-confirm/RESULTS.md`. Every `file:line` below was Read in this run or in the earlier parts of this session's work (same files, unchanged).

Codegraph: index_state=error, checked_at=2026-11-17T17:37:54Z; degraded: graph:parse_failed (the status call answered "Changes since index: unknown (measurement timed out or failed)", which matches no fresh/stale pattern, so this run stayed on Glob, Grep and Read; the caller lists for `load_panel` and `merge_round` quoted below were taken at 17:30:20Z when the index reported fresh).

---

## 1. Answer in one paragraph

Yes, probably, but only one part of the improvement is a panel configuration. The Review Panel as built chooses **models** and nothing else; every reviewer gets the same brief, and the merge marks a finding blocking if **any** reviewer did. The evaluation found that the model mix moved recall more than four families of process changes, that about 70% of every panel's blocking rows were wrong, and that eight of 36 known defects were found by no panel; all of it was measured on implementation **plans**, with eval-harness seats and lenses that the product does not have, and with models (`muse-ember-1.0`) that the product tier file does not list. A design-specific *model mix* is a data file and can ship today with `--template @design`. The parts most likely to matter for a design document, a code-grounding check and different reviewer lenses, are not panel data: lenses can be assigned by the coordinator without code (the reflect skill already does it by resolution order), while a code-grounding step that changes grading, a code-mismatch finding category, and a way for a wrong blocker to be dismissed without a person all need code. Whether any of this reviews designs better is UNVERIFIED: no panel has been run on a design document with an answer key.

## 2. Architecture as built

```text
data/review-tiers.default.json      data/review-panel.<name>.json  (or a project/user file, or $SUPERCLAUDE_REVIEW_PANEL)
   aliases -> ordered model lists       slots: tier, count, strategy (fixed | random | round_robin), seed
            \                          /
             panel.resolve(panel, tiers, env, run_id, kind)  ->  review-panel-resolution/1 JSON (reviewers, model, launch)
                                  |
     coordinator dispatches one reviewer per row, SAME brief for all (prompts file, "Review panel")
                                  |
     reviewer reports, each ending in a findings-v1 block (id, severity, blocking, category, anchor, refs, claim)
                                  |
     merge_cmd -> ledger.merge_round: annotate (anchor -> span, section, fingerprint) -> cluster -> match ledger rows
                  row.blocking = any reviewer blocking ; verdict = FAIL if any blocking row open/regressed
                  decision = PASS | REVISE | ESCALATE (cap)
                                  |
     reviser -> fixmap-v1 -> ledger revise (applied + hunk touched -> resolved_check) ; fixcheck on edited lines

Side path, used by sc:reflect only: findings-v2 (citations with role plan/spec/source/test/diff/artifact, lens,
channel incl. grounding-gap) -> review cluster (cluster_v2) -> review verify-citations (advisory) -> manifest
```

| Fact | Evidence |
|---|---|
| A template has only `schema, template_id, version, description, distinct_across_slots, apply_to, slots`; a slot only `slot_id, tier, count, strategy, seed` | `panel.py:37-46`; unknown keys rejected at `:174-176`, `:214-216` |
| So a panel chooses models (through tier aliases), never a lens, persona or brief | same; tier entries are `alias` + `models` (`panel.py:271-302`) |
| Product default when nothing is given: the hard-coded packaged file name `review-panel.default.json` | `panel.py:455-460` |
| Lookup order: `--template` path or `@name`; `$SUPERCLAUDE_REVIEW_PANEL`; `<project>/.superclaude/review-panel.json`; `~/.superclaude/review-panel.json`; packaged default | `panel.py:397-419`, `:447-467` |
| `@name` selects `data/review-panel.<name>.json`; a new packaged template is a data file plus nothing else | `panel.py:430-444`; `panel_cmd.py:19-25` |
| Default template: Tier 1b fixed anchor, 1 x Tier 2 random, 2 x Tier 3 random, `apply_to: ["first"]` | `review-panel.default.json:5-12` |
| A re-review resolves only the fixed anchor | `panel.py:600-605` |
| Exactly one fixed slot; 1 to 8 reviewers; count 1 to 4 per slot | `panel.py:229-248` |
| Distinctness is soft: when every candidate is taken, a repeat is re-admitted | `panel.py:539-543` |
| Probe, this checkout: `--kind first --env anthropic-only` resolves Sonnet 5.5 + Haiku 5.5 x 3 (all three stand-ins); `--kind re-review --env gateway` resolves the anchor only | `superclaude review panel resolve` run, 2026-11-17 |
| Tier 2 lists sol, glm, grok, qwen, muse-wonder, muse-spark; Tier 3 lists glm and qwen; `gpt-6-luna` is in Tier 4; no `muse-ember-1.0` anywhere | `review-tiers.default.json:5-10`, `:12-17` |
| Same brief for every reviewer; merged verdict from scripts only | `document_review_loop_prompts.md:70` |
| A ledger row is blocking when any member finding is blocking | `ledger.py:187`, `:213-218` |
| `confidence` (`overlap` vs `single`) is recorded but plays no part in the verdict | `ledger.py:86-90`, `:99-104`, `:273-275` |
| A row the reviser rejects stays `open`; only `resolved_check` rows clear; prior lines never change a status; only the human `ledger defer` removes an open blocker | `ledger.py:340-342`, `:254-258`, `:259-272`, `:350-360`; `ledger_cmd.py:83-84` ("Human command") |
| Finding categories are a fixed tuple | `findings.py:15-22`; reused by `findings_v2.py:15-22` |
| findings-v2 adds citations to repo files (role `source`, `test`, ...), lenses `spec`, `reflect-pre`, `reflect-post`, channel `grounding-gap` | `findings_v2.py:35-40`, `:59-81` |
| `verify-citations` checks each v2 citation's file, line range and quote; advisory, drops nothing | `verify_cmd.py:1-12` |
| The merge used by the spec-panel loop parses findings-v1 only | `merge_cmd.py:109` -> `ledger.py:128` (`fnd.parse_block`) |
| Personas per reviewer exist only as coordinator text: reflect assigns analyzer, qa, refactorer "by resolution order" | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:340-341` |
| `fixcheck` verifies `"quote" path:line` cites on edited lines only | `fixcheck.py:1-12`, `:123-141` |

## 3. What the evaluation shows, and what it does not

| Claim | Evidence | Transfer to `/sc:design` output |
|---|---|---|
| Model mix moved recall more than process changes | Process redesigns (collaboration, sweep sheet, Recipe Ledger, narrowed severity) gave no recall gain (`EXPERIMENT-REPORT.md:9`, `:113`); model arms reached +0.12 to +0.24 registered, +0.14 to +0.17 item-weighted for the Sonnet arms (`:37-61`) | UNVERIFIED for designs |
| The best single result did not confirm | wonsol lead +0.099 / +0.109, lower bounds -0.004 / -0.006, bar not met (`RESULTS.md:7-14`) | n/a |
| About 70% of blocking rows are wrong | 281 judged runs (`EXPERIMENT-REPORT.md:67`); control B 1.10 wrong blockers vs 0.50 blocking found per run (`:39`) | UNVERIFIED for designs; it is the property that most affects a fix loop (section 4) |
| Some defects are found by no panel | 8 of 36, including 3 blocking (`EXPERIMENT-REPORT.md:93`) | The missed classes are not labelled ("no usable defect class labels", `:101`) |
| Per-model profiles | Sonnet broad and slow, most unique finds, 77% wrong blockers in the S seat; sol most accurate (19-29% wrong in L seats), finds little others miss; luna terse and duplicates itself (`EXPERIMENT-REPORT.md:85-91`) | Profiles are model properties and may transfer; seat effects are confounded with eval lenses (`:92`) |
| Documents were plans | "Plans and answer key" (`EXPERIMENT-REPORT.md:13`); "one arm, one mix of models, plans only" (`RESULTS.md:40`) | Designs differ: their main external truth is the code, not a spec |
| The eval panels are not the product panel | Eval seats S/L1/L2 with lens sets C1-C8 and table caps (`EXPERIMENT-REPORT.md:14`); lens table code "accepts exactly three roles" (`:27`); the product has no lens field (section 2) | Any eval result about seats or lenses does not describe the product panel |

## 4. Architectural findings

| ID | Severity | Finding | Evidence | Consequence for a design review loop |
|---|---|---|---|---|
| RP-A1 | High | **A wrong blocker cannot leave the ledger without a person.** If the reviser rejects it (correctly), the row stays `open`; prior lines cannot change it; only a reviewer re-reporting it as non-blocking, or the human `ledger defer`, clears it | `ledger.py:340-342`, `:213-218`, `:259-272`, `:350-360` | With about one wrong blocker per run (eval figure, UNVERIFIED for designs), an unattended `/sc:design` loop tends to run all 3 reviews and end ESCALATE even when the design is sound |
| RP-A2 | High | **OR-merge of blocking calls.** One reviewer's blocking mark makes the row blocking; `overlap` confidence is not used | `ledger.py:187`, `:86-90`, `:99-104` | Adding reviewers (for recall) adds wrong blockers linearly; the 4-reviewer default inherits the worst reviewer's false-alarm rate |
| RP-A3 | High | **No code grounding in the loop's path.** The v1 merge carries only an anchor in the candidate; no field cites the repository, no step checks one | `findings.py:90-121`; `merge_cmd.py:109` | A design's contradiction with the code is neither required nor verifiable in a finding; a claim that "function X does not exist" is accepted unchecked |
| RP-A4 | Medium | **Grounding exists, in the other path.** findings-v2 citations with role `source` and `verify-citations` are used by reflect only | `findings_v2.py:35-81`; `verify_cmd.py:1-12`; `SKILL.md:340-347` | The design loop could reuse them, but only after the merge accepts v2 or a pre-merge filter is added (code) |
| RP-A5 | Medium | **Panel = models only; diversity = models only.** Same brief for all reviewers; no lens or persona field | `panel.py:37-46`; `prompts:70` | Four reviewers with one brief re-find the same classes; the eval's recall gains came with distinct seat lenses that the product lacks |
| RP-A6 | Medium | **Re-reviews use one reviewer.** `apply_to: ["first"]` | `review-panel.default.json:7`; `panel.py:600-605` | Cheap, and it limits wrong blockers at reviews 2-3; it also means a regressed fix is judged by the anchor model alone |
| RP-A7 | Medium | **In the anthropic-only environment the default panel is Sonnet + 3 Haiku.** Distinctness is soft | probe; `panel.py:539-543`; `review-tiers.default.json:31-35` | The "4 different models" description (`review-panel.default.json:5`) holds only on the gateway |
| RP-A8 | Low | **Pinning a second model needs a one-model tier.** Exactly one fixed slot is allowed; random picks from the whole tier list | `panel.py:245-246`, `:544-547` | "Anchor Sonnet + sol for accuracy" (the eval's design rule, `EXPERIMENT-REPORT.md:111`) needs a new tier alias in the tier file and a matching gateway alias (`review-panel.live7.json:5` notes the same for `tier2b`) |
| RP-A9 | Low | **Category set is closed in code.** | `findings.py:15-22` | A `code-mismatch` or `rollout` category is a code change plus tests |

## 5. What a design-specific configuration would contain

| Part | Content | Mechanism today | Needs code? |
|---|---|---|---|
| Panel template `review-panel.design.json` | Anchor Tier 1b (Sonnet first: broadest, most unique finds); one accuracy seat (sol); one breadth seat (wonder or Tier 3); `apply_to: ["first"]`; 3 reviewers, not 4, to limit OR-merge noise (RP-A2) | packaged data file, `--template @design` (`panel.py:430-454`) | No. A dedicated sol tier needs a tier-file alias and a gateway alias (RP-A8): data plus ops |
| Reviewer lenses | Seat 1 "code consistency" (names, signatures, files, layering, consumers; cite `file:line`), seat 2 "failure, data and rollout" (failure modes, data model, migration, rollback), seat 3 "internal correctness" (contradictions, guards, sequences, the spec-panel FR rules) | Coordinator assigns by resolution order, as reflect does (`SKILL.md:340-341`) | No, if the lens text lives in the coordinator or the prompts file; a lens field in the template would be code (`panel.py:46`) |
| Brief | A DESIGN-REVIEW prompt: candidate + repository root + codegraph state; "a stated name, path or signature that contradicts the code at a cited `file:line`" as a blocking case | Prompts file (Markdown) | No code, but spec-panel's "a brief may not widen" rule (`spec-panel.md:264`) means the case must be added to the command's own grading, not only to a brief |
| Finding categories | `code-mismatch`, `consumer-break`, `rollout` | `findings.py:15-22` | Yes (small), plus tests in `tests/review/` |
| Grading | Blocking = existing three cases + code-mismatch with a verified citation; an unverified code claim is demoted to Medium | — | Yes: a pre-merge step that reads v2 citations and the `verify-citations` result, or a v2-aware merge |
| Code-grounding step | Before merge: run `verify-citations` on the reviewers' source citations; after merge: coordinator re-grounds rows on changed lines (`design-review-phase.md` §7.1) | `verify_cmd.py` exists; coordinator step needs none | Wiring v2 into the spec-panel merge: yes |
| Wrong-blocker exit | A reviewer status `withdrawn` (with reason) on a prior line, or "reviser rejected + next reviewer agrees" clears a row | — | Yes: `PRIOR_STATUSES` (`findings.py:23`), `ledger.merge_round` (`:259-272`) |

## 6. Would it review better than the default plus the spec-panel lenses?

- **Code-consistency defects:** today nothing in the panel or spec-panel looks for them (`analyze-spec-panel.md` §3-5; RP-A3). Any configuration that sends one reviewer to the repository with a citation rule can only add coverage here. Expected better; size UNVERIFIED.
- **Wrong blockers:** a 3-seat panel with an accurate seat is the eval's best-supported accuracy lever (sol 19-29% wrong vs 70-78%, `EXPERIMENT-REPORT.md:88`; wonsol 0.20 vs 0.52 wrong blockers per run on new plans, `RESULTS.md:24`). That is the one measured result most likely to carry over, because it is a model property. But RP-A1 and RP-A2 are in the ledger, not in the panel: a better mix lowers their rate and does not remove them.
- **Recall in general:** the eval's recall gains did not confirm (`RESULTS.md:7`) and were measured with lenses the product lacks. A design template alone, without lenses, is not shown to find more.
- **Defects nobody found:** unlabelled (`EXPERIMENT-REPORT.md:101`), so it cannot be said whether design lenses would reach them.

Net: the configuration most likely to help is "fewer, more accurate reviewers, each with a distinct lens, one of which must cite the code, plus a way to dismiss a wrong blocker". About half of that is data or coordinator text; the grading, category and ledger parts are code.

## 7. Recommendations

1. Ship `/sc:design`'s review phase on the default panel first only if RP-A1 is acceptable as "ends ESCALATE more often"; otherwise fix RP-A1 first (smallest code change of the list: a `withdrawn` prior status or a reviser-reject-plus-agree rule, with tests in `tests/review/test_review_ledger.py`).
2. Add `review-panel.design.json` (data) and coordinator-assigned lenses (text) together, so a model choice and a lens choice are tested as one configuration.
3. Wire findings-v2 source citations and `verify-citations` into the spec-panel merge path before letting a code-mismatch finding block.
4. Before choosing models for designs, build a small answer key on 3-5 real `/sc:design` outputs (the eval harness already exists under `.dev/eval-workspaces/tasklist-review-panel/`) and run default vs design configuration interleaved, as `RESULTS.md` did for plans.

## 8. Not verified

- Any panel's recall or wrong-blocker rate on design documents (no runs exist).
- That the product default template has the eval's ~70% wrong-blocker rate: the eval panels used different models and seats (`EXPERIMENT-REPORT.md:14-27`).
- Gateway availability of models and aliases named in section 5 (the tier file says the gateway "dispatch mechanism per model [is] not defined yet", `review-tiers.default.json:26`).


<!-- sc:issue-603:analyze-review-panel -->


## Comment 3 | https://github.com/IronbellyOrg/IronClaude/issues/603#issuecomment-6956000613 | 2026-11-17T17:40:55Z

## Phase 2 findings: design document for the review phase of /sc:design

Produced by the Phase 2 agent (analysis only; no product file was changed). Source file in the working tree: `.dev/issues/603/phase2/design-review-phase.md` (not committed).

# Design: a "review, QA and enrichment" phase at the end of `/sc:design` (issue #603)

**Status:** design only. Nothing in `src/`, `tests/`, `docs/` or `plugins/` is changed by this document.
**Produced by:** `/sc:design phase "review, QA and enrichment" for sc:design --type component --format spec` (Phase 2 agent, 2026-11-17).
**Component:** the `/sc:design` command (`src/superclaude/commands/design.md`), with `/sc:spec-panel --mode critique` and the `superclaude review` CLI as reused parts.

Grounding: index_state: fresh (checked_at 2026-11-17T17:30:20Z, projectPath /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel); codegraph tools used: codegraph_status, codegraph_callers (load_panel, merge_round), codegraph_node (ledger_cmd.py symbolsOnly). Markdown command files are not indexed, so every command-file claim below comes from Read.

---

## 1. Purpose and scope

`/sc:design` ends today with a self-check (Validate) and a write (Document); no independent reviewer reads the design and nothing revises it (`design.md:28-34`). Its unattended section records `Nested invocations. None.` (`design.md:125`). The repo already has a capped document review loop in `/sc:spec-panel` (`spec-panel.md:256-264`), fixed reviewer and reviser prompts (`document_review_loop_prompts.md:27-66`), and scripts that resolve a reviewer panel, merge reports into a ledger and compute the verdict (`src/superclaude/cli/review/`).

This design adds one step, **6. Review**, after Document. It makes `/sc:design` the *coordinator* of a spec-panel critique loop on the design document it just wrote, adds a code re-grounding check on revised text, and appends a review record to the document.

Out of scope (carried, not decided, per the issue's Out of Scope): whether spec-panel and the Review Panel need a design-specific configuration (lenses, brief, panel template). That question is answered separately in `analyze-spec-panel.md`, `analyze-review-panel.md` and `verdicts.md` in this folder. This design works with spec-panel and the panel exactly as they are, and names the two seams (section 10) where a later design-specific configuration would plug in without changing this flow.

## 2. Binding constraints (read from the files)

| # | Constraint | Source |
|---|---|---|
| C1 | Cap text, verbatim: "at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings"; no other cap number for a review loop anywhere in `src/` or `plugins/` | `spec-panel.md:261`; `tests/skills/test_review_severity_rule.py:215`, regex at `:288-292`, scan at `:320-337` |
| C2 | Each spec-panel run is one review; the coordinator keeps the review count, the prior-findings file and the saved copy; without them the run is a first review | `spec-panel.md:261` |
| C3 | Before writing or accepting any review or revise brief, read `~/.claude/rules/prompts/document_review_loop_prompts.md` in full; if unreadable, return `incomplete` and review nothing | `spec-panel.md:266-268` |
| C4 | A brief may narrow scope, never widen it past changed lines and prior blockers, never regrade a minor finding as blocking, never say "apply all findings" | `spec-panel.md:264`; `document_review_loop_prompts.md:72-74` |
| C5 | Panel: reviewers from `superclaude review panel resolve`, each in a fresh context with the same brief; merge with `superclaude review merge`; record the reviser with `superclaude review ledger revise`; one reviewer if `superclaude` is not installed | `document_review_loop_prompts.md:68-70` |
| C6 | Under `--unattended`, a TDD input without `--target-release` resolves as blocked | `spec-panel.md:463` |
| C7 | Nested propagation: pass `--unattended` plus `<caller report-dir>/nested/<command>-<n>/`; list each nested contract in `artifacts`; read nested results by the nested-result rule | `src/superclaude/core/WORKER-CONTRACT.md:24-25` |
| C8 | `/sc:design` writes a file only when `--output` is passed; under `--unattended` `--report-dir` is required and `report_path` is the `--output` file or `<report-dir>/design-report.md` | `design.md:26`, `:122-123` |
| C9 | `/sc:design` generates no implementation code and changes no existing architecture without approval | `design.md:124`, `:136-140` |
| C10 | `tests/skills/test_worker_contract.py` pins design's unattended phrases (`design-report.md`, `no gate`, `consent is never given`) and an empty nested list; `EXPECTED_NESTING` must equal every command's nested list | `test_worker_contract.py:558-561`, `:1617-1632` |

## 3. Where the step sits

```text
1 Analyze -> 2 Plan -> 3 Design -> 4 Validate -> 5 Document -> 6 Review (new)
                                                              |
                                  6a Review loop (spec-panel critique, panel, ledger)
                                  6b QA: code re-grounding + mechanical checks on revised lines
                                  6c Enrichment: Review record appended to the design document
```

- Step 6 runs only when step 5 wrote the design to a file (`--output`, or `<report-dir>/design-report.md` under `--unattended`). A standalone run without `--output` prints the design in chat, as today, and prints one line: `Review skipped: no design file (pass --output <file> to review it).` Reason: spec-panel's loop needs a file to hash, diff and anchor findings in (`spec-panel.md:258`, `findings.py:276-304`).
- Step 6 never re-enters steps 1-4. The only text that changes in step 6 is text a blocking finding names (C4).
- The Behavioral Flow list in `design.md` gains item 6; the Usage line is unchanged (no new flag; see Q-1 for an opt-out).

## 4. Roles and files

`/sc:design` is the coordinator. It never reviews its own document.

| Role | Who | Gets | Writes |
|---|---|---|---|
| Coordinator | the `/sc:design` run | everything below | loop dir, baselines, ledger (via CLI), Review record |
| Reviewer | one fresh Agent per resolved reviewer, model = the reviewer's `launch` value | the candidate path, FIRST-REVIEW or RE-REVIEW brief filled from the prompts file | one review report |
| Reviser | one fresh Agent on the run's own model | the merged report's `Reviser brief` ids, REVISE brief | edits to the design file, fix map |
| Scripts | `superclaude review panel resolve`, `merge`, `ledger revise`, `ledger verdict`, `fixcheck` | as below | resolution JSON, ledger, merged report |

The reviser is a fresh Agent, not the authoring context, because the failure #346 recorded was revisers adding mechanisms (`docs/designs/spec-panel-review-loop.md:15`); a fresh reviser sees only the brief and the report.

**Loop directory** (`<loop>`): under `--unattended`, `<report-dir>/review/`; otherwise `<output dir>/<output stem>.review/` (next to its source, user rule 5). Contents:

```text
<loop>/
  loop.json                 # loop_id, review count, candidate path, model per reviewer (coordinator state, C2)
  resolution-<N>.json       # panel resolve output for review N
  r<N>/<reviewer_id>.md     # one report per reviewer
  merged-<N>.md             # merge output: verdict, ledger table, Reviser brief
  baseline-<N>.md           # copy of the design file saved before fix cycle N
  revise-<N>.md             # reviser output with the fixmap-v1 block
  ledger.json               # superclaude review ledger (review-ledger/1)
```

`loop_id` = `design-<target slug>-<UTC YYYYMMDDTHHMMSSZ>`; it seeds the random panel slots (`panel.py:606-610`).

## 5. What is passed to spec-panel

Every reviewer runs `/sc:spec-panel` with these arguments (reviewer side), plus the brief from the prompts file (C3):

| Review | Arguments |
|---|---|
| 1 (first) | `@<design file> --mode critique --focus <focus> --target-release <TR> --output <loop>/r1/<reviewer_id>.md` |
| N = 2, 3 (re-review) | `@<design file> --mode critique --focus <focus> --target-release <TR> --re-review <loop>/merged-<N-1>.md --baseline <loop>/baseline-<N-1>.md --output <loop>/r<N>/<reviewer_id>.md` |

- `--mode critique`: the only mode with a verdict line and findings block (`spec-panel.md:258-260`; `document_review_loop_prompts.md:56-62`).
- `--focus`: `architecture` always (Fowler, Newman, Hohpe, Nygard; `spec-panel.md:142-151`); add `correctness` when the design document defines mutable state, guard thresholds or a multi-stage pipeline, the same trigger spec-panel itself uses for its advisory suggestion (`spec-panel.md:192`). The coordinator decides once at the start of step 6 and records it in `loop.json`; re-reviews use the same focus.
- `--target-release <TR>`: always passed, `TR` = `design-review` (a label, not a release). Reason: a long design document can score 5 or more on spec-panel's TDD detector (numbered `## N.` headings plus "Data Models" / "API Specifications" / "Component Inventory" headings, `spec-panel.md:36`), and under `--unattended` that input without `--target-release` resolves as blocked (C6). The value only scopes the Improve step, which step 6 never runs. See Q-3.
- `--re-review` points at the *merged* report of the prior round, not at one reviewer's report: the merged report carries the `review: N of 3` header and the ledger's ids that the reviser was briefed on (`ledger.py:408-493`).
- Never passed: `--improve` (step 6 never asks spec-panel to write an improved spec; the reviser does the bounded edit), `--iterations` (ignored with `--re-review` anyway, `spec-panel.md:261`), `--experts` (keeps the critique roster as written; a design-specific roster is the separate follow-up).

## 6. The review loop (step 6a)

```text
N = 1
loop:
  resolve   superclaude review panel resolve --run-id <loop_id> --kind (first if N==1 else re-review) > resolution-N.json
  review    one fresh Agent per reviewer, same brief, none sees another's report
  merge     superclaude review merge --ledger ledger.json --doc <design file> --round N
              --report <id>=r<N>/<id>.md ... --resolution resolution-N.json --out merged-N.md
            -> JSON {verdict, decision, brief ids}; decision is PASS, REVISE or ESCALATE (ledger.py:93-96)
  PASS      -> stop, go to 6b
  ESCALATE  -> stop (N == 3), escalate with the open blocking findings (section 8)
  REVISE    -> copy design file to baseline-N.md
               reviser Agent: REVISE brief with {{IDS}} = the brief ids only -> edits design file, writes revise-N.md
               superclaude review ledger revise --ledger ledger.json --old baseline-N.md --new <design file> --fixmap revise-N.md
               6b QA on the lines this revision changed
               N = N + 1
```

Rules, each restating an existing source:

- **Blocking findings only.** Only rows that are blocking and `open` or `regressed` reach the reviser (`ledger.py:99-104`). Medium and minor findings never trigger a revision, never fail a review and never appear in the Reviser brief (`spec-panel.md:259`).
- **Cap.** The loop runs at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings (C1). The ledger is created with `--cap 3` (the merge default, `merge_cmd.py:64-69`), so round 3 with a blocker yields `decision: ESCALATE` and no Reviser brief (`ledger.py:476-485`).
- **Reviser contract.** The reviser repairs only the listed ids, prefers deleting or narrowing, adds no rule, mechanism or section a listed finding does not call for, cites the finding id on every addition, reports bytes before/after and per id, ends with a `fixmap-v1` block, and does not award itself a PASS (`spec-panel.md:263`; `document_review_loop_prompts.md:51-54`, `:64-66`). The reviser may not change any file other than the design file.
- **Re-review scope.** Review 2 and 3 cover the prior blocking findings and the lines changed against the baseline only; a clean re-review ends `scoped PASS: changed lines + prior blockers` (`spec-panel.md:262`). The Review record (6c) states that scope; step 6 does not run a fourth, whole-document review.
- **Panel size.** The packaged default template resolves four reviewers for a first review and only its fixed anchor for a re-review, because `apply_to` is `["first"]` (`review-panel.default.json:7-12`; `panel.py:600-605`). Probe on this checkout: `superclaude review panel resolve --run-id design-603-probe --kind first --env anthropic-only` gave `t1b-1` claude-sonnet-5-5 plus three claude-haiku-5-5 stand-ins; `--kind re-review --env gateway` gave `t1b-1` claude-sonnet-5-5 only.
- **Verdict source.** The merge script's verdict decides, never a reviewer's prose (`document_review_loop_prompts.md:70`). A missing or ambiguous verdict counts as FAIL (`spec-panel.md:260`).
- **Follow-up candidates.** Medium and minor findings are listed in the Review record under `follow-up candidates`. In an attended run the coordinator asks the user once per loop whether to open an issue for them and creates none without the answer (`spec-panel.md:260`); under `--unattended` it only records the list.

## 7. QA (step 6b) and enrichment (step 6c)

### 7.1 QA after each revision

Run on the lines the reviser changed (`fixcheck.edited_lines`, `fixcheck.py:46-53`), never on the whole document:

1. **Mechanical checks:** `superclaude review fixcheck --file <design file> --base <loop>/baseline-N.md` (options at `fixcheck_cmd.py:39-43`). It checks table pipes, a `"quote"` followed by a `path:line` cite being present on the cited line, `N rows` counts and relative links (`fixcheck.py:1-12`). A failed check is passed to the next re-review as part of the brief's evidence; it does not by itself fail the loop and it never edits the file.
2. **Code re-grounding:** for every symbol, file path or signature that appears on a changed line, repeat the Validate-step lookup of the design command's Code-graph grounding table (`design.md:59-65`): `codegraph_search` / `codegraph_node` when `index_state` is `fresh`, else Grep and Read; re-Read any `file:line` before keeping it. A name that does not exist, or a signature that does not match, is reported to the next re-review as a finding candidate quoted from the changed line. Step 6b never edits the design file; only the reviser does.
3. **Grounding line:** no new readiness check (the once-per-run rule, `design.md:55`). Tokens from 6b (`graph:empty`, `graph:unresolved`, ...) are appended to the existing `Grounding:` line.

Why here: spec-panel's reviewers are told to review "against the requirements it states" (`document_review_loop_prompts.md:32`) and are given no instruction to open the repository, while `/sc:design` already holds the code-grounding machinery. A revision is the moment a design can drift from the code it was grounded on.

### 7.2 Enrichment: the Review record

What enrichment adds is a record, not new design content. After the loop ends (any outcome), the coordinator appends one section to the design file:

```markdown
## Review record

- Loop: <loop_id>; reviews run: <N> of 3; final decision: PASS | ESCALATE | INCOMPLETE
- Scope of the final verdict: whole document (review 1) | scoped PASS: changed lines + prior blockers
- Panel: <reviewer_id>=<model> per review (from resolution-<N>.json); one-reviewer fallback: yes/no
- Blocking findings: resolved <ids>; open <ids, each with its one-sentence claim>
- Follow-up candidates (Medium and minor, not acted on): <ledger ids and claims>
- QA: fixcheck failures <count>; code re-grounding misses <count> (names listed)
- Files: <loop dir path>
```

Not done in enrichment, deliberately: spec-panel's Improve step, filling gaps a Medium finding names, adding examples, diagrams or sections. Each would add text no blocking finding calls for, which the reviser contract forbids and which is the growth #346 recorded (57,763 to 92,194 bytes over three rounds, `docs/designs/spec-panel-review-loop.md:15`). Whether the issue's word "enrichment" was meant to include gap filling is Q-2.

## 8. Escalation and outcomes

| Loop end | Attended run | `--unattended` run (`worker_status`) |
|---|---|---|
| PASS at review 1, 2 or 3 | design file final; Review record says PASS and its scope | `succeeded` |
| Review 3 still FAIL | stop; print the open blocking findings (id, claim, anchor) and the Review record path; no fourth review | `partial`; open ids in the Review record; the merged report is `report_path`'s companion in `artifacts` |
| Review could not run (section 9) | design file kept as written by step 5; Review record says INCOMPLETE and why | `partial` |
| No design file written | unchanged from today | `failed` (unchanged) |

The existing contract sentence "The run is succeeded when the design document is written, and failed otherwise" (`design.md:123`) becomes: succeeded when the design document is written and its review loop ends PASS; partial when it is written but the loop escalates or cannot run; failed when no design document is written. `partial` is an allowed worker status (`WORKER-CONTRACT.md:33`, WC-4 field list).

## 9. Failure and fallback

| Failure | Detected by | Behaviour |
|---|---|---|
| Prompts file unreadable | Read of `~/.claude/rules/prompts/document_review_loop_prompts.md` fails | Loop does not start (C3); Review record INCOMPLETE |
| `superclaude` CLI not installed or `panel resolve` fails (`NoModelAvailable`, `ExclusionExhausted`, invalid template; `panel_cmd.py:104-107`) | non-zero exit | One reviewer on the run's own model, no ledger; the verdict is that report's last `verdict:` line; Review record says "one-reviewer fallback" (`document_review_loop_prompts.md:70`) |
| No reviewer produced a valid findings block | `merge` refuses the round, ledger unchanged (`ledger.py:150-157`) | Re-run that review once with the same resolution; a second refusal stops the loop as INCOMPLETE |
| Some reviewers invalid | merge warning; their parsable findings kept (`ledger.py:112-113`) | Continue; list the invalid reviewers in the Review record |
| A reviewer Agent fails or times out | no report file | Treated as an invalid reviewer for that round |
| spec-panel returns `incomplete` (unreadable input, hash failure; `spec-panel.md:258`) | report or contract says so | Same as an invalid reviewer |
| Nested contract `blocked` (unattended; expected only from C6, which `--target-release` prevents) | nested-result rule | Stop; write own contract `blocked` with `blocked_question` prefixed `/sc:spec-panel:` (C7) |
| Reviser output missing or no `fixmap-v1` block | `ledger revise` falls back to a table of `applied` rows (`findings.py:205-223`); exit status | If the file changed and a fallback map exists, continue; otherwise restore the design file from `baseline-N.md` and stop as INCOMPLETE |
| Reviser edited another file | coordinator compares `git status` of the repo before and after the reviser | Stop as INCOMPLETE and name the file; never revert files the run did not create |
| codegraph not fresh | the once-per-run state | 6b uses Grep/Read; token on the Grounding line; never stops the run |
| Reviser rejects a blocking finding as wrong | fix map `rejected` | Known limit, not fixed here: the ledger keeps a rejected row `open` (`ledger.py:340-342`) and only the human `superclaude review ledger defer` clears it (`ledger.py:350-360`), unless a later reviewer re-reports it as non-blocking (`ledger.py:213-218`). The loop therefore runs on and ends ESCALATE; the Review record lists rejected ids with the reviser's reason. See Q-8 |

## 10. `--unattended` and `--output`

- **`--output`** keeps its meaning: the design file. Step 6 revises that file in place (it is the run's own output, so C9 and spec-panel's "never modifies the input" rule are not touched: spec-panel never edits it; the reviser does, under the coordinator). Without `--output` in an attended run, step 6 is skipped (section 3).
- **`--unattended`** adds the nested propagation. Every reviewer call receives `--unattended --report-dir <report-dir>/nested/spec-panel-<n>/` and no `--output` (spec-panel's report then lands at `<report-dir>/nested/spec-panel-<n>/spec-panel-report.md`, `spec-panel.md:461`); `<n>` counts every spec-panel call of the run from 1, across reviewers and rounds, and is never reused (a re-run takes the next number). The coordinator copies or points `merge --report <id>=<path>` at those report paths.
- **Contract listing.** Each nested `return-contract.yaml` is listed in `artifacts`, also when the call failed (C7); so are `<loop>/merged-<N>.md`, `<loop>/ledger.json` and `<loop>/resolution-<N>.json`. The worker contract gets no new field (WC-4 has none for nesting; nested contracts travel in `artifacts`).
- **Gates.** One new attended-only question (the follow-up-candidates issue offer, section 6). Under `--unattended` it is recorded, not asked. The escalation at review 3 is not a gate under `--unattended`: it ends the run `partial` (section 8), because WC-2 forbids a person-blocking step.
- **Reviser and reviewers are Agents, not `/sc:` commands invoked by design**, except that each reviewer Agent runs `/sc:spec-panel`. Precedent for running spec-panel as a nested command: `/sc:cli-eval` (`cli-eval.md:86`), which also states spec-panel is command-only and is run as a command, not through the Skill tool. Whether a reviewer Agent calls it through the Skill tool (where Claude Code lists it) or by reading the command file is Q-4.

New text for the design command's unattended section (replaces `design.md:125`):

> - **Nested invocations.** Step 6 runs each reviewer's `/sc:spec-panel` call with `--unattended --report-dir <report-dir>/nested/spec-panel-<n>/`, `<n>` counting every spec-panel call from 1 and never reused (a retry takes the next number); each contract is listed in `artifacts`, also when the call failed. A nested contract is read by the nested-result rule of `~/.claude/WORKER-CONTRACT.md`.

**Seams for a later design-specific configuration** (not used now): (a) the `--template` argument of `panel resolve` (`panel_cmd.py:19-25`) accepts `@<name>` for a packaged template (`panel.py:430-454`), so a `review-panel.design.json` data file needs no code to be selected; (b) the reviewer brief is filled from the prompts file, so a design lens would be a new prompt there plus a spec-panel change. Both are evaluated in `analyze-review-panel.md` and `analyze-spec-panel.md`.

## 11. Files that would change

| File | Change | Why |
|---|---|---|
| `src/superclaude/commands/design.md` | Behavioral Flow item 6; a `## Review phase` section (sections 3-9 condensed); Tool Coordination gains `Agent` and `Bash` for the `superclaude review` commands; Unattended: Contract sentence (section 8), Gates (one attended question), Nested invocations (section 10); Boundaries: "Will" gains the review loop, "Will Not" gains "edit text no blocking finding names" | the feature |
| `plugins/superclaude/commands/design.md` | Same edits | The mirror already lags `src` (no codegraph section, `diff` shows lines 6, 23, 26-27, 30, 33, 46-75); whether to sync it in full or only add step 6 is Q-5 |
| `tests/skills/test_worker_contract.py` | `UNATTENDED_EXPECT["design"]["nested"]` = `["spec-panel"]` (`:558-561`); `EXPECTED_NESTING["design"] = ["spec-panel"]` (`:1617-1627`); replace the phrase `"no gate"` with the new gate wording if the sentence changes | pinned today; would fail otherwise |
| `tests/commands/test_design_review_phase.py` (new) | Text-presence test: step 6 in the flow; the canonical cap text (C1); `--mode critique`, `--re-review`, `--baseline`, `--target-release`; `superclaude review merge` and `ledger revise`; no `--improve` | same pattern as the #346 design's test |
| `tests/skills/test_review_severity_rule.py` | No edit expected; it must still pass (no old cap number may appear in design.md) | regression guard (C1) |
| `tests/skills/test_codegraph_adoption.py` | No edit expected; its design.md pins (`:324-400`) must still hold, so the Code-graph grounding section text stays byte-identical | regression guard |
| `docs/user-guide/commands.md` | `/sc:design` row (`:59`, "Report only") and section (`:1048-1070`): describe step 6, the review folder and the extra cost | user-facing |
| `src/superclaude/core/HOW-WE-WORK.md` | Rows at `:247` and `:298` say design is "a single pass" with no reviewers; update; copy byte-for-byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (project CLAUDE.md rule) | routing text would become false |
| `.claude/commands/sc/design.md` | Regenerated by `make sync-dev`; never staged | project rule |

Not changed: `spec-panel.md`, the prompts file, and every file under `src/superclaude/cli/review/`; this design uses them as they are.

## 12. Acceptance checks (map to the issue)

| Issue AC | Check |
|---|---|
| Review phase runs after Document and blocking findings are fixed and re-reviewed | A run with `--output` on a fixture target produces `<loop>/merged-1.md`; when it is FAIL, `baseline-1.md`, `revise-1.md` and `merged-2.md` exist and the ledger shows the brief ids moved to `resolved_check` then `resolved` |
| At most 2 fix cycles (3 reviews), then escalation | `ledger.json` never has more than 3 rounds; a round-3 FAIL yields `decision: ESCALATE` and the attended run prints the open blocking ids; `superclaude review ledger verdict` exits 11 (`ledger_cmd.py:13`, `:101-109`) |
| design.md documents the phase and its nested spec-panel call | New text test (section 11) and the updated worker-contract pins pass |

## 13. Cost

UNVERIFIED estimate, not measured for design documents: the eval panel runs on plans took a median 85 to 289 s per panel round (`.dev/eval-workspaces/tasklist-review-panel/20261116-stronger-panel/EXPERIMENT-REPORT.md:39-45`). With up to 3 rounds plus 2 reviser passes, step 6 can add several minutes and several reviewer contexts to every `/sc:design` run that writes a file.

## 14. Open questions

- **Q-1.** Should `/sc:design` get an opt-out flag (for example `--no-review`) for quick drafts? Not added here (scope discipline); the cost in section 13 is the argument for it.
- **Q-2.** Does "enrichment" in the issue mean only the Review record and code re-grounding (this design), or also filling gaps that Medium findings name? The latter conflicts with the reviser contract.
- **Q-3.** Is `--target-release design-review` an acceptable way to keep spec-panel's TDD detector from blocking an unattended run, or should spec-panel's gate (`spec-panel.md:463`) apply only when `--improve` is passed?
- **Q-4.** Do reviewer Agents run spec-panel through the Skill tool or by reading the command file? `cli-eval.md:86` says command, never Skill tool; a project memory note says a worker that only reads a command file does not satisfy WC-7 (UNVERIFIED for reviewer Agents, which are not Orca workers).
- **Q-5.** Sync the lagging `plugins/` mirror of design.md in full, or add only step 6?
- **Q-6.** Is the attended escalation a stop (this design) or an offer to keep the design and open an issue with the open blockers?
- **Q-7.** Should step 6 wait for the design-specific configuration (verdicts in `verdicts.md`) rather than ship with spec-panel's spec-oriented lenses and the default panel?
- **Q-8.** In an attended run, should the coordinator offer `ledger defer` for a blocker the reviser rejected (a person decides), and should the ledger get an automatic exit for it (see `analyze-review-panel.md` RP-A1)?


<!-- sc:issue-603:design-review-phase -->


## Comment 4 | https://github.com/IronbellyOrg/IronClaude/issues/603#issuecomment-6956187181 | 2026-11-17T17:48:42Z

## Next step: run this brainstorm FIRST, then `/sc:workflow` to turn its result into a tasklist

Phase 2 rated both `/sc:spec-panel` and the Review Panel **REFACTOR VALUABLE** for reviewing `/sc:design` output (verdicts, analyses and the design of the new phase are in the comments above). The work is not yet scoped. The order is:

1. **Brainstorm (run first).** It turns the Phase 2 findings into merged requirements: every change to `/sc:spec-panel` and the Review Panel, grouped by component, tied to the gaps it closes, with priority, dependencies, the evidence needed and a recommended sequence. No code.
2. **`/sc:workflow` (run second, only after step 1 ends with status PASS or PARTIAL).** It turns the merged requirements into a phased implementation plan (a workflow plan package under `.dev/tasks/to-do/`, with its advisory review). Read the printed plan path and the review result before anything is built.
3. **Implementation (separate order, after the plan is read).** `/sc:implement <printed plan path>`, on a new branch from `origin/master` made through an Orca worktree, with the pull request opened only by `/sc:pr-submit --monitor 3` to IronbellyOrg/IronClaude (never SuperClaude-Org).

### Step 1: brainstorm command

```text
/sc:brainstorm @/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/issues/603/brainstorm-topic.md --depth deep --proposals 5 --codebase --handoff none --output /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/brainstorms/20261117-issue-603-design-review-panel
```

Flags: `--depth deep` and `--proposals 5` because the request is for all changes and maximum value (use `--depth standard` for a cheaper first pass); `--codebase` forces code context; `--handoff none` stops at merged requirements; no `--interactive`, so the topic file is the context. The merged requirements are written to `/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/brainstorms/20261117-issue-603-design-review-panel/merged-requirements.md`. If the brainstorm ends FAIL (convergence below 0.50) do not run step 2: re-run with a narrower topic or a deeper depth.

The topic file is in the working tree of the worktree named above and is not committed. If you run this from another worktree, save the prompt text below to a file there and point the command at it.

### Step 2: workflow command

```text
/sc:workflow @/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/brainstorms/20261117-issue-603-design-review-panel/merged-requirements.md --depth standard --handoff none
```

The workflow writes a new package (it never edits an existing one), runs its own advisory review, and prints the plan path and the review result. Fix blocking findings by writing a new plan, not by editing this one.

### The brainstorm prompt (topic file text)

~~~text
Brainstorm every change and addition that /sc:spec-panel and the Review Panel need so that the planned review, QA and enrichment phase at the end of /sc:design (GitHub issue #603, IronbellyOrg/IronClaude) reviews technical designs well, and drive as much value as possible. Brainstorm only: produce merged requirements, not code.

CONTEXT. /sc:design produces HOW-we-build documents (architecture, component interfaces, data models, API contracts, migration and rollout, failure modes). Today it validates only by its own self-check and invokes nothing (src/superclaude/commands/design.md:28-34, :125). Issue #603 adds a final phase that runs /sc:spec-panel --mode critique on the generated design, revises only blocking findings, re-reviews, and stops at 2 fix cycles and 3 reviews. /sc:spec-panel and the Review Panel (src/superclaude/cli/review/, its data templates and tiers, the reviewer briefs, the finding ledger) were built to review WHAT-we-build specifications. The Phase 2 analysis rated both REFACTOR VALUABLE (neither is needed for issue #603's acceptance criteria; neither is fit for designs as they are).

READ FIRST (all under .dev/issues/603/, also posted as comments on the issue): issue-body.md; phase2/verdicts.md (verdicts, gaps G-1 to G-14 with file:line evidence, what could not be verified, nine open questions); phase2/analyze-spec-panel.md; phase2/analyze-review-panel.md; phase2/design-review-phase.md (the design of the new /sc:design phase). Prior evidence on the Review Panel: .dev/eval-workspaces/tasklist-review-panel/20261116-stronger-panel/EXPERIMENT-REPORT.md and 20261117-confirm/RESULTS.md (these tested PLANS, never designs).

KEY FINDINGS TO BUILD ON. (1) Neither spec-panel nor the Review Panel checks a design against the real repository; a wrong signature or a missing module can only be a non-blocking warning because the blocking cases in src/superclaude/rules/prompts/document_review_loop_prompts.md:31 exclude it (G-1, G-2, G-3, G-10). (2) A wrong blocking finding cannot leave the ledger without a person: reviser-rejected rows stay open and only the manual `ledger defer` clears one (src/superclaude/cli/review/ledger.py:340-360), so unattended design loops will often escalate at review 3 (G-8); blocking calls are OR-merged with the agreement signal unused (G-9). (3) The expert roster has no owner for consumer impact, data-model correctness or migration, rollout and rollback (G-4, G-5, G-6). (4) A long design can trip the unattended TDD-detector block (G-7). (5) A panel template chooses models only; every reviewer gets the same brief (G-11, G-12, G-13). (6) Nobody has measured any panel on designs (G-14).

BRAINSTORM THESE AREAS, each with options, trade-offs and a recommendation: (a) spec-panel changes for design documents: code grounding, expert and lens roster, blocking rules and who owns the rule, the TDD-detector block, whether a design focus or mode is better than editing the critique mode; (b) Review Panel changes: a design-specific panel template and configuration, which models and seats, lenses and briefs per seat, finding categories (code mismatch, consumer break, rollout), how a wrong blocker leaves the ledger without a person, whether OR-merge of blocking calls should change, mechanical code-citation verification (the findings-v2 and verify-citations machinery that only the reflect path uses today); (c) what already works as data only (templates selected with @name, tier files, project and user overrides) versus what needs code; (d) the evidence needed before any default changes: a design answer key, a design test set, an interleaved control, the rule for calling a change confirmed, and what to ship as opt-in first; (e) sequencing: whether the /sc:design phase ships first on today's spec-panel and default panel with the known limits stated, or waits, and the order of the other changes with dependencies; (f) risks, including the review-loop growth problem of closed issue #346 (revisers adding mechanisms), cost and time of a deeper panel, and the effect on other callers of spec-panel and the Review Panel.

SETTLE THE NINE OPEN QUESTIONS in phase2/verdicts.md, or say why one cannot yet be settled and what evidence would settle it.

OUTPUT WANTED: merged requirements grouped by component (spec-panel, Review Panel, /sc:design phase), each tied to the gap ids it closes, with priority, dependencies, the evidence or test needed, and whether it is data-only or code; a recommended sequence; and the unresolved questions. Delivery constraint to carry into any later work: the changes land on a new branch from origin/master made through an Orca worktree, with a pull request opened only by /sc:pr-submit --monitor 3 to IronbellyOrg/IronClaude, never to SuperClaude-Org.
~~~

<!-- sc:issue-603:brainstorm-prompt -->


