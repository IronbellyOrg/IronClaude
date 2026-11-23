# Round 1 visual parity review

- Model id: `gpt-6-astra` (session-provided runtime identity).
- Reviewer: astra.
- Date: 2026-11-17.
- Scope: independent comparison of the supplied observer renders with the supplied mockups, not a live Orca run; product code is read-only.
- Governing report structure: the dispatched brief's per-finding fields (id, mockup file/width/region, exact current evidence, category, class, severity, fix direction).
- Image capability: this model can inspect images supplied through the Read tool.
- Inputs used: all nine current text exports, all nine current ANSI exports (byte/escape inspection), and all nine mockup text exports, ANSI exports (byte/escape inspection) and PNGs under `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/`, covering ledger, questions and desk at widths 160, 116 and 80. The width-specific PNGs were viewed directly. The duplicate attachment PNGs were not needed.
- Reference sources read: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md`; `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/render.py`; `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/terminal.py`; the symbol outline of `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/view.py`; and `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/tools/render_current.py` (read, never executed).
- Classification boundary: this is a theme-parity review, not a claim that every difference violates the existing implementation contract. The rendering rules explicitly describe stacked question/desk blocks and leave the two-column composition and RETAIN CONTEXT as design reference. Findings about their appearance are PARITY-GAP for this comparison, not regressions or authorization to ignore that contract; any later implementation must reconcile its layout change with the approved specification. Source limitations and permanent interaction/safety constraints remain ACCEPTED-DIVERGENCE.
- Severity describes effect on theme parity, following the dispatched brief's High/Medium/Low scale. Accepted divergences are not fix requests. Quoted code blocks below contain exact current lines; where non-adjacent lines are collected in one block, each line is independently verbatim, not a claim of adjacency.

## Findings

### F-astra-01: The observed-question count has no visual weight

- Mockup: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/mockups/116/agent-focus-attention-ledger.txt`, width 116, right-top SEEN IS NOT RESOLVED tile. The corresponding 160-column PNG shows the same large amber count and separate caption.
- Current evidence: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/current/116/questions.txt`:
  ```text
  seen, not resolved: 3 | closed by evidence: unavailable (no source)
  no read marker in source: answered questions stay listed
  ```
  `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/current/160/questions.txt` has the same treatment:
  ```text
  seen, not resolved: 3 | closed by evidence: unavailable (no source)
  no read marker in source: answered questions stay listed
  ```
- Category: TYPOGRAPHY-EMPHASIS.
- Class: PARITY-GAP.
- Severity: High.
- Effect: an already-available, important number is visually indistinguishable from the surrounding caveats; the mockup's principal at-a-glance signal disappears. This is not a demand for a resolved/open count the source does not supply.
- Fix direction: give the existing seen-not-resolved count a distinct titled, high-emphasis treatment at wide widths, preserving the closure-unavailable qualification.

### F-astra-02: Retention context is scattered rather than grouped

- Mockup: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/mockups/116/agent-focus-attention-ledger.txt`, width 116, right-lower RETAIN CONTEXT panel.
- Current evidence: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/current/116/questions.txt`:
  ```text
  one Run only: run_14cfcbd8edf2
  no read marker in source: answered questions stay listed
  retention reset at 12:00; questions observed before this start are not retained
  ```
- Category: INFO-HIERARCHY.
- Class: PARITY-GAP.
- Severity: Medium.
- Effect: scope, retention lifetime and the missing closure signal sit in different unframed places around the questions instead of one supporting context region. The missing panel is confirmed, but copying all seven mockup attributes would invent unavailable information.
- Fix direction: group only supported scope, retention and closure-availability facts into a subordinate context panel, with unsupported attributes explicitly unavailable or omitted and no persistence of question text.

### F-astra-03: Caveats dominate the question list instead of supporting it

- Mockup: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/mockups/116/agent-focus-attention-ledger.txt`, width 116, left question blocks and right supporting regions.
- Current evidence: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/current/116/questions.txt`:
  ```text
  COORDINATOR QUESTIONS
  one Run only: run_14cfcbd8edf2
  question read: OK 0s
  bounded best effort; coverage unknown; at most 100 rows per read, not 100 questions; bursts over 100 rows between
  reads may be lost
  seen, not resolved: 3 | closed by evidence: unavailable (no source)
  no read marker in source: answered questions stay listed
    1h  Choose schema compatibility policy  reason unknown
    59m  Confirm deployment window  reason unknown
    59m  Name the release reviewer  reason unknown
  ```
- Category: INFO-HIERARCHY.
- Class: PARITY-GAP.
- Severity: High.
- Effect: seven title/metadata/caveat lines precede three tightly packed questions; no spacing, separators, bold question text or aligned age gutter distinguishes what needs reading from its limitations. The caveats themselves are required and must remain visible.
- Fix direction: separate question blocks with restrained spacing/rules, align and emphasize ages and question text, and visually subordinate but retain the scope and coverage disclosures.

### F-astra-04: Rich mode has no colour or weight styling

- Mockup: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/mockups/160/signal-bridge.png`, width 160, whole screen: cyan identity/activity, amber questions, muted supporting text and differentiated status colours. The attention-ledger and decision-desk PNGs at all three widths use the same visual language.
- Current evidence: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/current/160/ledger.txt`:
  ```text
  worker-list OK 0s  messages UNVERIFIED (not read)
  Human questions: source UNVERIFIED, 0 rows interpreted, not "no questions"
  worker-reported, not questions
  ```
- Category: THEME-COLOUR.
- Class: PARITY-GAP.
- Severity: High.
- Effect: all semantic emphasis is reduced to literal words and capitalization. Byte inspection found zero ESC bytes and zero SGR styling sequences in every one of the nine current ANSI exports; all nine mockup ANSI files contain SGR styling. This confirms the no-colour hypothesis for the supplied rich-mode outputs, not just their plain-text companions. The capture source explicitly disables neither colour nor Unicode, and the renderer constructs plain Text without styles.
- Fix direction: apply a restrained semantic ANSI palette and bold/dim hierarchy to existing truthful content, while retaining text labels and a working NO_COLOR path rather than requiring a fixed terminal background.

### F-astra-05: Region boundaries and titled panes are absent

- Mockup: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/mockups/160/decision-desk.txt`, width 160, HUMAN QUESTION, OTHER OBSERVED QUESTIONS and AFFECTED SESSION EVIDENCE frames; `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/mockups/80/signal-bridge.txt`, width 80, HUMAN QUESTION and SELECTED FLEET SLICE frames.
- Current evidence: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/current/160/desk.txt`:
  ```text
  DECISION DESK
  msg_000000000000  age 1h
  Choose schema compatibility policy
  dispatchId: w-001
  ```
  `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/current/80/ledger.txt`:
  ```text
  26 historical hidden (h)
  worker-reported, not questions
     none           w-001                                  10s
  ```
- Category: FRAME-PANE.
- Class: PARITY-GAP.
- Severity: High.
- Effect: the question region, selected-question evidence, source context and worker ledger run into one continuous text stream. All nine current screens lack enclosing titled panes; the full-width table's horizontal column rule is not a pane. Even the 80-column mockups keep grouping when columns collapse.
- Fix direction: add clearly titled, restrained frames or separators around the existing logical regions, with stronger emphasis for the selected question and ASCII-safe alternatives.

### F-astra-06: Wide Decision Desk never uses its available horizontal space

- Mockup: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/mockups/160/decision-desk.txt`, width 160, question/other-questions left and evidence right; `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/mockups/116/decision-desk.txt`, width 116, full-width selected question above two supporting columns.
- Current evidence: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/current/160/desk.txt`:
  ```text
  DECISION DESK
  msg_000000000000  age 1h
  Choose schema compatibility policy
  dispatchId: w-001
  workerState: running
  dispatchStatus: active
  terminalState: active
  outcome: none
  nextAction.kind: wait
  liveness: alive (terminal)
  evidence age: 3s
  resource.worktreeId: wt-1
  ```
- Category: LAYOUT.
- Class: PARITY-GAP.
- Severity: High.
- Effect: a short question and nine short evidence fields consume a tall one-column block at both wide widths, then the general worker ledger repeats the linked worker among unrelated rows. The eye cannot compare question and linked evidence side by side. Having only one verifiably linked worker does not require abandoning the two-region layout technique.
- Fix direction: use a responsive wide question/evidence composition with other questions subordinate, preserving the single-column version at 80 and never inventing additional affected sessions.

### F-astra-07: Compact worker rows lose their field labels

- Mockup: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/mockups/80/signal-bridge.txt`, width 80, SELECTED FLEET SLICE field legend; `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/mockups/116/signal-bridge.txt`, width 116, SESSION REGISTER field legend.
- Current evidence: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/current/80/ledger.txt`:
  ```text
  worker-reported, not questions
     none           w-001                                  10s
     review         w-002                                  13s
  ```
  `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/current/80/questions.txt`:
  ```text
  worker-reported, not questions
     wait           w-001                                  3s
     wait           w-002                                  6s
  ```
  `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/current/116/ledger.txt`:
  ```text
  worker-reported, not questions
     none               w-001                                                alive          10s
  ```
- Category: DEGRADED-WIDTH.
- Class: PARITY-GAP.
- Severity: Medium.
- Effect: at 116 and 80, in all three screens, the field headings disappear completely. A reader sees `wait`, `review`, `none` and an age without an on-screen explanation that these are next-action kinds and worker evidence ages, not worker states or question ages. Reducing the number of columns is acceptable; removing the remaining columns' meaning is not necessary.
- Fix direction: keep a compact field legend or short column headings for kind, dispatch identity, evidence age and, where present, liveness.

### F-astra-08: The 80-column ledger cuts off the quit instruction

- Mockup: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/mockups/80/signal-bridge.txt`, width 80, complete keyboard-help footer.
- Current evidence: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/current/80/ledger.txt`:
  ```text
  Up/Down j/k move  Enter detail  Esc back  / filter  h historical  m mark  e exp>
  shown 39/54 | collected 80 / reported 80
  ```
- Category: KEYS-FOOTER.
- Class: DEFECT.
- Severity: Medium.
- Effect: a supported terminal width displays an incomplete export action and no quit key. This is a discoverability bug independent of the mockup's exact keys. The question screens already wrap their help, so this failure is specific to the no-question ledger path rather than unavoidable lack of space.
- Fix direction: preserve every key/action pair by wrapping or compacting the ledger footer, reserving the needed line before fitting worker rows.

### F-astra-09: Wrapped keyboard hints split keys from their actions

- Mockup: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/mockups/116/agent-focus-attention-ledger.txt`, width 116, ruled footer with visually separated key/action groups; `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/mockups/80/decision-desk.txt`, width 80, footer.
- Current evidence: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/current/116/questions.txt`:
  ```text
  Up/Down j/k move workers  Enter detail  Esc back  / filter  h historical  m mark rows  e export all  q quit  n/p
  question
  shown 6/6 | collected 6 / reported 6
  ```
  `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/current/80/desk.txt`:
  ```text
  Up/Down j/k move workers  Enter detail  Esc back  / filter  h historical  m
  mark rows  e export all  q quit  n/p question
  shown 6/6 | collected 6 / reported 6
  ```
- Category: KEYS-FOOTER.
- Class: PARITY-GAP.
- Severity: Low.
- Effect: `n/p` and `question`, or `m` and `mark rows`, land on different lines. Unlike the ledger bug, the information is not lost, but the unruled prose footer is slower to scan and the second line can look detached from its key.
- Fix direction: lay out indivisible key/action groups with restrained separators and a clear footer boundary, wrapping between groups only.

### F-astra-10: The persistent read-only identity marker is missing

- Mockup: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/mockups/116/decision-desk.png`, width 116, upper-right SYNTHETIC / READ ONLY badge; the same badge appears at widths 160 and 80.
- Current evidence: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/current/116/desk.txt`:
  ```text
  ORCA OBSERVER  mode=live  scope=all  as of 12:00:00
  ```
  `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/current/160/ledger.txt`:
  ```text
  ORCA OBSERVER  mode=fixture  SYNTHETIC FIXTURE base, not Orca data  scope=all  as of 12:00:00
  ```
- Category: TYPOGRAPHY-EMPHASIS.
- Class: PARITY-GAP.
- Severity: Low.
- Effect: data mode and scope are present, but the on-screen identity never explicitly says read-only. This loses the mockup's immediate distinction between observing a question and answering or acting on it. The synthetic question fixture intentionally exercises the live-mode renderer; its `mode=live` text is not evidence of a production provenance bug.
- Fix direction: retain the honest existing data-mode labels and add a small persistent READ ONLY marker that survives width collapse without displacing scope or coverage.

### F-astra-11: Missing fleet bars and invented operational states are intentional

- Mockup: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/mockups/160/signal-bridge.txt`, width 160, SIGNALS bars plus owners/mapped-trees header and result/admission fields.
- Current evidence: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/current/160/ledger.txt`:
  ```text
  collected 80 / reported 80  scope=all  source counts: active 54 / reclaimable 0 / retained 13 / released 13  runs seen: 8  SETTLED unavailable (no source)
  POLICY FROZEN unavailable (no source)  cost unavailable
  Human questions: source UNVERIFIED, 0 rows interpreted, not "no questions"
  ```
- Category: INFO-HIERARCHY.
- Class: ACCEPTED-DIVERGENCE: real-data-only and source-honesty constraints prohibit substituting worker terminal accounting for settled/approved states, inventing owners or mapped trees, or making up human questions when that source is off. The rendering rules explicitly replace fleet bars with source counts and denominators.
- Severity: Low.
- Effect: the absence of these particular bars, labels and mock question content is not a defect. Their visual prominence can inspire treatment of supported facts, but their meanings cannot be copied.
- Fix direction: retain truthful source counts, unavailable markers and the question-source gap; style those instead of reintroducing unsupported fleet health or approval claims.

### F-astra-12: One linked worker is not an affected-fleet list

- Mockup: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/mockups/116/decision-desk.txt`, width 116, HUMAN QUESTION owner/scope metadata and multi-session AFFECTED SESSIONS ledger.
- Current evidence: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/current/116/desk.txt`:
  ```text
  dispatchId: w-001
  resource.worktreeId: wt-1
  worktree is evidence for this one session; other sessions in it are not inferred affected
  ```
- Category: LAYOUT.
- Class: ACCEPTED-DIVERGENCE: the authoritative link supplies one dispatch; a shared worktree does not establish that other sessions are affected, and no verified requester, acting human owner, approval or plan state is available for the mockup's richer metadata.
- Severity: Low.
- Effect: fewer evidence rows and omitted owner/requester fields are correct, not missing visual features. This does not excuse the missing wide layout technique in F-astra-06.
- Fix direction: preserve the one-dispatch scope and explicit non-inference note while improving the layout around the evidence actually available.

### F-astra-13: Different keyboard actions and narrow stacking are valid adaptations

- Mockup: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/mockups/80/decision-desk.txt`, width 80, stacked question/evidence/other-question regions and footer with `tab pane` and `p hold view`.
- Current evidence: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/current/80/desk.txt`:
  ```text
  DECISION DESK
  msg_000000000000  age 1h
  Choose schema compatibility policy
  ```
  ```text
  Up/Down j/k move workers  Enter detail  Esc back  / filter  h historical  m
  mark rows  e export all  q quit  n/p question
  ```
- Category: INTERACTION.
- Class: ACCEPTED-DIVERGENCE: the standing keyboard/read-only constraint and the rendering rules allow local worker inspection, local history/mark/export and question selection, prohibit multi-pane focus, and use `p` for the previous question. At 80 columns the reference itself collapses to one column; retaining that responsive technique is correct.
- Severity: Low.
- Effect: not copying tab-based pane focus or the mockup's hold shortcut is not a parity defect, and the 80-column desk should not be forced into two columns. These exports show affordances, not a tested keyboard session; they do not prove the actions work.
- Fix direction: keep the truthful supported key map and narrow stacking, improve only grouping/emphasis, and do not add reply, approval, mouse or Orca-mutating controls.


## Coverage and verification

### Nine-screen coverage

Each row was inspected against its same-width design, including the PNG. Cross-cutting findings are listed rather than duplicated with new IDs. Every combination has at least one finding, so no screen/width combination requires a `none found` exception.

| Screen | Width | Current text inspected | Applicable findings |
|---|---:|---|---|
| ledger | 160 | `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/current/160/ledger.txt` | F-astra-04, F-astra-05, F-astra-10, F-astra-11 |
| ledger | 116 | `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/current/116/ledger.txt` | F-astra-04, F-astra-05, F-astra-07, F-astra-10, F-astra-11 |
| ledger | 80 | `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/current/80/ledger.txt` | F-astra-04, F-astra-05, F-astra-07, F-astra-08, F-astra-10 |
| questions | 160 | `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/current/160/questions.txt` | F-astra-01, F-astra-02, F-astra-03, F-astra-04, F-astra-05, F-astra-10 |
| questions | 116 | `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/current/116/questions.txt` | F-astra-01, F-astra-02, F-astra-03, F-astra-04, F-astra-05, F-astra-07, F-astra-09, F-astra-10 |
| questions | 80 | `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/current/80/questions.txt` | F-astra-04, F-astra-05, F-astra-07, F-astra-09, F-astra-10 |
| desk | 160 | `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/current/160/desk.txt` | F-astra-04, F-astra-05, F-astra-06, F-astra-10, F-astra-12 |
| desk | 116 | `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/current/116/desk.txt` | F-astra-04, F-astra-05, F-astra-06, F-astra-07, F-astra-09, F-astra-10, F-astra-12 |
| desk | 80 | `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/current/80/desk.txt` | F-astra-04, F-astra-05, F-astra-07, F-astra-09, F-astra-10, F-astra-12, F-astra-13 |

### ANSI check

Read-only byte inspection used the existing files, without re-rendering or starting the observer. Every current ANSI file had **0 ESC bytes and 0 SGR sequences**. The corresponding mockup counts below are both the ESC and SGR count; they prove that the reference exports do preserve styling.

| Width | Current ledger/questions/desk ESC counts | Signal Bridge mockup | Attention Ledger mockup | Decision Desk mockup |
|---:|---|---:|---:|---:|
| 160 | 0 / 0 / 0 | 684 | 418 | 442 |
| 116 | 0 / 0 / 0 | 390 | 382 | 342 |
| 80 | 0 / 0 / 0 | 260 | 208 | 234 |

The no-style result agrees with the actual renderer's unstyled Text construction. It is not inferred from text exports or from a terminal screenshot stripped of colour.

### Known-hypothesis disposition

| Hypothesis | Result |
|---|---|
| No colour styling | Confirmed for all nine supplied rich-mode exports, F-astra-04. |
| No boxed titled panes | Confirmed for all nine screens, F-astra-05. |
| No two-column Decision Desk | Confirmed at 160 and 116, F-astra-06; stacking at 80 is accepted, F-astra-13. |
| No large SEEN IS NOT RESOLVED tile | Confirmed at 160 and 116, F-astra-01; a large tile is not demanded at 80. |
| No RETAIN CONTEXT panel | Confirmed at 160 and 116, F-astra-02; missing unsupported attributes remain accepted, not invented requirements. |

### Literal evidence check

Pending the final read-only mechanical check of every finding's quoted lines, mockup paths, categories, classes, severities and nine-screen coverage.

## Limits and final outcome

**Visual-parity verdict: FAIL.** The primary ANSI theme and grouping are absent, independently of unavailable source data. There are **13 findings: 9 PARITY-GAP, 1 DEFECT and 3 ACCEPTED-DIVERGENCE**. Five parity gaps are High, two are Medium and two are Low; the rendering defect is Medium. This verdict concerns the current screens, not whether the requested review was delivered.

The smallest useful direction is to style and group the existing truthful view, restore complete compact-width key help, and then adapt the wide question/desk composition. No new data source, inferred owner, inferred affected fleet, action control or persisted question text is needed to address the reported visual gaps.

Limits and negative evidence:

- No live observer, Orca data read through the observer, product test suite, keyboard session or terminal screenshot capture was run. Analysis is of the supplied synthetic renders and read-only source inspection. The coordinator messaging commands are separate from the observer and were used only as required by the dispatch.
- NO_COLOR and ASCII-specific current captures were not supplied. Source inspection shows the existing switches and glyph substitutions, but their runtime behaviour was not exercised; no claim that either mode passed is made. Plain-text exports being unstyled is expected and is not itself the colour finding. Styled mode must remain distinct from those fallbacks.
- All current text lines fit their declared width in the saved examples, and no accidental right-edge overflow was found. This does not cover long real question text, wide combining characters or terminal resize behaviour. The observed missing quit hint is still a real truncation defect despite fitting the width.
- The current capture source uses height 50; the reference text exports contain 49 rows at width 160 and 43 at widths 116/80 including blank padding. Exact bottom-row position and row density are therefore not treated as defects, nor is a missing fixed-height footer asserted from these exports.
- The narrow question/desk screens keep all displayed key text, while splitting some key/action pairs. Narrower-than-80 and short-height states were outside these supplied captures and were not tested.
- The other reviewer's files were not opened. No external publication, product edit, worktree creation, task-file mutation or Git operation was performed. The only authored file is this findings report.
- Initial environment discovery found none of the queried Orca override variables (printenv exit 1); the dispatched `orca` executable then successfully returned its version-matched guide and handled the required coordinator messages. No missing review input or failed evidence lookup blocked the review.

Independent acceptance of this report belongs to the coordinator's subsequent review step. The local evidence check below is a mechanical citation check, not a substitute for that independent review.
