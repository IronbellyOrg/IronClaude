# Second-author review of recipes C1-C8 (swap test)

Scope: read only recipes/recipes.json, recipes/rl-block.txt, recipes/search-form.txt, recipes/README.md, neutral-table.txt. No recipe file was edited.
Limit: I did not open the ground-truth files, so "issue-specific" is judged from the wording alone. A word is listed only if it reads as taken from one defect. Words that are generic but worth a second look are marked "borderline" and are NOT counted as issue-specific.
Method per recipe: (1) replace domain nouns with <ITEM>/<FILE>/<CLAIM>, reread, check it still gives an executable procedure; (2) list issue-specific words; (3) check each step is a concrete action or concrete question.

## C1 (version 1)

Verdict: PASS
Issue-specific words: none. Borderline: the trigger list "found", "no remaining" (generic quantifier words, but "found" is an odd member of the list).
Placeholder, first sentence: "For each <CRITERION> that says <QUANTIFIER WORDS>: (1) write the finite check that would let a reviewer say yes, with its stopping rule;"
Swap test: reads correctly. Steps: write a finite check plus stopping rule (action), copy the instruction sentence and write what set each covers (action), mark PROBLEM if no finite check or sets differ (decision rule). All concrete.
Note: trigger words "all, every, each" overlap with C6; both can fire on the same sentence (wasted rows, not a defect).

## C2 (version 2)

Verdict: PASS
Issue-specific words: none. Borderline: "stops, fails or returns" and "a failure, an exit or a special case" lean toward program exit behavior, but they are generic trigger verbs and a generic priority order.
Placeholder, first sentence: "Split the <SOURCE DOC> into rules: one per sentence that contains <MODAL/OUTCOME WORDS>, or per table row."
Swap test: reads correctly. Steps: split into rules (action), take up to 6 and prefer failure/special-case ones (action), quote the carrying plan sentence (action), trace failure paths of the three most conditional rules to the governed output (action), PROBLEM when no sentence or the path ends elsewhere (decision rule). All concrete. "The output the rule governs" is the least concrete phrase but it is answerable per rule.
Note: README says it needs a source file; neutral-table.txt still says "Up to 10 rules but 6 rows" while the text now says 6 rules (stale maintainer note, not shown to reviewers).

## C3 (version 1)

Verdict: PASS (weakest recipe)
Issue-specific words: none. Borderline: "status mappings" (an example in the parenthesis, plausibly taken from one defect, but a generic category).
Placeholder, first sentence: "List every <VALUE> that a <ITEM> reads, maps or requires as the input to a decision (<LOOKUP TABLES>, <MAPPINGS>, conditions)."
Swap test: reads correctly. Steps: list inputs to decisions (action), find the writer row/task/step per case (action), PROBLEM when a case has no writer (decision rule).
Weakness: "every case the reader handles" and "decision" are not defined, so the reviewer must invent the case list. Executable, but the least checkable step in the set. README already calls the class weak.

## C4 (version 2)

Verdict: PASS
Issue-specific words: none. Borderline: "Bash" (names a tool, environment-specific, not defect-specific); "ordered text" (jargon for "text the task orders").
Placeholder, first sentence: "For each <CRITERION> that embeds a <COMMAND/PATTERN/SELECTOR/NAME>: write the exact <TEXT> the same <ITEM> tells the implementer to write or create."
Swap test: reads correctly. Steps: write the ordered text (action), apply the literal pattern to it, optionally on a scratch string (action), ask what the command selects on the current tree (question), PROBLEM rule, and a prohibition (do not treat the current tree as proof). All concrete; search-form.txt supplies the `printf | grep -c` form.
Note: step 3 (look at the current tree) and the last sentence (do not use it as proof) pull in opposite directions; the text does separate "what it selects" from "what the plan produces", so it is workable.

## C5 (version 2)

Verdict: PASS
Issue-specific words: none. Borderline: "root-level documents", "copies kept elsewhere" (read as a reaction to a missed root file or mirrored copy, but the README states root-level scope as a general rule); "Report it even if you think it is minor" (a severity nudge, not a defect fact).
Placeholder, first sentence: "For each <CHANGE> that alters a <LITERAL> that the repository may also state elsewhere: (1) write the old <LITERAL>; (2) run one search of the whole tree for it, ...; (3) list every hit the <PLAN> neither edits nor checks."
Swap test: reads correctly. Steps: write old literal (action), one whole-tree search (action; search-form.txt gives the grep), list unedited and unchecked hits (action), PROBLEM when the hit becomes false (decision rule). All concrete.

## C6 (version 2)

Verdict: PASS
Issue-specific words: none. Borderline: none.
Placeholder, first sentence: "For each <SENTENCE> the plan states or dictates that says <UNIVERSAL WORDS>: (1) name the <SET> it covers;"
Swap test: reads correctly. Steps: name the set (action), run one count or listing command (action; the README admits the model must invent the command), compare with other tasks and the enforcing test's scope, "what does that test skip or not read?" (concrete question), PROBLEM rule. All concrete.

## C7 (version 1)

Verdict: PASS
Issue-specific words: none. Borderline: none.
Placeholder, first sentence: "List every <CONSTRAINT>, one clause per line (split at semicolons and 'and')."
Swap test: reads correctly. Steps: split constraints into clauses (action), list dictated texts (action), tick each clause against each text on its topic (action), PROBLEM when a text omits or contradicts a clause (decision rule).
Weakness: the recipe does not say where constraints come from, and "on its topic" needs judgment. Executable, but a terse reviewer may skip the clause-by-text matrix. Splitting at every 'and' will over-split.

## C8 (version 2)

Verdict: PASS
Issue-specific words: none. Borderline: "pins the text or behavior" (jargon for "asserts on"); the `git grep` example assumes a git repository (search-form.txt has plain `grep -rlF` alternatives).
Placeholder, first sentence: "For each <FILE> the plan edits or creates, search the <PLACES> for its path and distinctive strings, with a literal-string search that lists matching files (for example `git grep -l -F '<STRING>' -- <PLACES>`)."
Swap test: reads correctly. Steps: literal-string search per edited file (action, command given), open each unnamed referencing file (action), decide whether it pins the changed text (question), PROBLEM if no task updates or runs it. All concrete. The version 2 text names no fixed folders, which fixes the hard-coded "tests scripts docs" of the older text still shown in neutral-table.txt (R-C8).

## Side notes (not recipe defects)

- neutral-table.txt is stale against recipes.json: its R-C8 is the version 1 text, C2 is described as "up to 10 rules", and its word counts predate version 2 (by hand, C2 now has 90 words, the table says 89). The table's own text ends in mid-sentence ("luna 1 (C1, C2, C3) is 216 words,").
- The `override` entries in recipes.json cite a path outside this folder (implement-report/recipe-review/review-1.md). I did not open it; it is provenance data, not recipe text.
- No recipe states an expected outcome; all end with "Write at most N rows." as README requires.

## Summary

| Recipe | PASS/FAIL | issue-specific words |
|---|---|---|
| C1 | PASS | none (borderline: "found", "no remaining") |
| C2 | PASS | none (borderline: "stops, fails or returns", "an exit") |
| C3 | PASS | none (borderline: "status mappings") |
| C4 | PASS | none (borderline: "Bash", "ordered text") |
| C5 | PASS | none (borderline: "root-level documents", "copies kept elsewhere", "even if you think it is minor") |
| C6 | PASS | none |
| C7 | PASS | none |
| C8 | PASS | none (borderline: "pins", `git grep`) |
