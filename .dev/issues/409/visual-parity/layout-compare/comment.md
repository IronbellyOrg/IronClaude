## Stacked vs two columns: renders, debate and recommendation (owner decision D-1 / O-1)

The spec needs one owner answer before phases P4 and P5: adopt two columns at 160 and 116 (reversing `rendering-rules.md` lines 43 and 57), or keep one stacked column. Below are renders of both from the same real fixture data, a short debate between an advocate for each side, and my recommendation. At 80 columns both options are stacked, so only 160 and 116 are in question.

**How the images were made.** Prototype script `.dev/issues/409/visual-parity/layout-compare/proto_layouts.py` (not product code, the two-column layout is not built). It reads the observer's real view objects and arranges them with Rich panels in the mockup colours. In each image, A (top) is stacked and B (bottom) is two columns. Panel widths follow the spec (160: left 114, right 42; desk 76 and 80; 116: left 70, right 42; desk 66 and 46). The worker table, header and footer are left out of both. One fixture question carries a 64-hex-character hash and file paths (PR #591 consideration 8).

### Questions screen

160 columns:
![questions 160](https://raw.githubusercontent.com/IronbellyOrg/IronClaude/docs/606-layout-review-images/.dev/issues/409/visual-parity/layout-compare/questions-160.png)

116 columns:
![questions 116](https://raw.githubusercontent.com/IronbellyOrg/IronClaude/docs/606-layout-review-images/.dev/issues/409/visual-parity/layout-compare/questions-116.png)

### Decision Desk

160 columns:
![desk 160](https://raw.githubusercontent.com/IronbellyOrg/IronClaude/docs/606-layout-review-images/.dev/issues/409/visual-parity/layout-compare/desk-160.png)

116 columns:
![desk 116](https://raw.githubusercontent.com/IronbellyOrg/IronClaude/docs/606-layout-review-images/.dev/issues/409/visual-parity/layout-compare/desk-116.png)

80 columns (same in both options): [questions](https://raw.githubusercontent.com/IronbellyOrg/IronClaude/docs/606-layout-review-images/.dev/issues/409/visual-parity/layout-compare/questions-80.png), [desk](https://raw.githubusercontent.com/IronbellyOrg/IronClaude/docs/606-layout-review-images/.dev/issues/409/visual-parity/layout-compare/desk-80.png).

### Rows used (counted from the render data, frames included)

| Screen | A stacked | B two columns | Difference |
|---|---|---|---|
| Questions, 160 | 11 | 17 | B costs 6 more |
| Questions, 116 | 12 | 17 | B costs 5 more |
| Desk, 160 | 23 | 14 | B saves 9 |
| Desk, 116 | 23 | 18 | B saves 5 |

Rows matter because the live screen silently crops rows from the bottom when the terminal is too short, and the footer keys are the first thing lost.

### Debate (two advocates, one per layout, each had to concede where the other wins; files under `.dev/issues/409/visual-parity/layout-compare/debate/`)

**For stacked.** The caveat text is required in full and reads in one order. In two columns the same disclosure is split across three places (left pane, count tile, RETAIN CONTEXT), and the narrow 42-cell right column wraps the retention sentence into ragged short lines. At 116 the 70-cell left pane wraps the question to three or four lines and pushes `reason unknown` onto its own line, which is the text the reader came to read. RETAIN CONTEXT adds no fact; it moves lines. The big count tile repeats the count the left side already shows. Stacked code is needed at 80 anyway, so two columns adds a second layout path, more goldens and more height cases.

**For two columns.** It matches the mockups, and the count tile is the one element that pulls the eye (finding M-05). Question text leads in the left pane and the caveats drop to a dim box (M-07, M-14). On the Decision Desk the saving is real: the 12-row evidence block no longer sits between the question and the list, and the desk fits in 14 rows against 23.

**Where they ended up.** Both sides conceded the same points. Questions screen: stacked wins at 116 (both sides, 70 to 75 percent) and on height at 160. Decision Desk: two columns wins at 160 (both sides, 60 to 80 percent). Decision Desk at 116: two columns wins on height, but the 46-cell list pane breaks the long hash. In my prototype Rich cut it with an ellipsis; the product's `wrap` would hard-split it across two lines with nothing lost, so the real cost is a split hash, not a lost one. That should be checked in P0, because the spec's rule is that a hash which fits is never split.

### Recommendation

| Case | Recommendation | Why |
|---|---|---|
| Questions, 160 | **Stacked**, with a weighted count (see below) | B costs 6 more rows for no extra fact; the caveat text stays in one read order. Confidence about 65 percent: B wins on mockup parity only. |
| Questions, 116 | **Stacked** | B wraps the question text and orphans `reason unknown`, and the right column is cramped. Confidence about 75 percent. |
| Desk, 160 | **Two columns** | Saves 9 rows, matches the mockup, and nothing is lost. Confidence about 80 percent. |
| Desk, 116 | **Two columns**, if the list pane hard-splits the hash with nothing lost; otherwise stacked | Saves 5 rows; risk is the narrow list pane. Confidence about 60 percent. |
| 80 | Stacked (unchanged) | Both options agree. |

**What this means for the spec.**
- D-1 becomes a split answer: yes for the Decision Desk at 160 and 116, no for the questions screen.
- P4 keeps its goals but changes shape. M-05 (count weight) is met by a full-width cyan count strip with the block-glyph figure at 160 and 116, placed above the question list inside the stack, instead of a right-hand tile. M-14 (RETAIN CONTEXT) is met by a stacked slate pane at the bottom that groups the run line, caveat and retention sentence. M-07 (caveats outweigh questions) is met because those three lines leave the top of the list pane.
- P5 stays as written (two columns at 160 and 116, stacked at 80). `_two_columns` is still needed there.
- Consequence: the questions screen at 160 and 116 will differ from the attention-ledger mockup in arrangement. I would record that as an accepted divergence (new AD-8) with this comment as the evidence.
- Caveats: row counts are from a prototype with a three-question fixture; a real window of up to 100 questions changes the height picture for the list but not the comparison of the right column. The prototype is not the product renderer, so exact wrapping can differ by a row.

**Needs the owner:** reply with one of: (1) accept this split, (2) all two columns as originally specified, (3) all stacked. Until you answer, P0 to P3 and P6 can start; only P4 and P5 wait.
