# Second-author review of recipes C1 to C8

Scope: read only recipes/recipes.json, recipes/rl-block.txt, recipes/search-form.txt, recipes/README.md and neutral-table.txt. No ground-truth file was opened, so "issue-specific" below means "reads like one concrete defect, judged from the recipe text alone". I cannot confirm any of it against a real defect list.

Method per recipe: swap every domain noun for a placeholder, reread, then answer (1) still reads and is executable, (2) issue-specific words, (3) every step is a concrete action or question.

Cross-cutting notes (apply to several recipes):
- rl-block.txt never defines "the grading check" (used by C5) or "the candidate" (used by C2). Only neutral-table.txt uses them.
- README.md says the recipe wording "needs no change" per target type, but its own table says test paths and command dialect change per target. That is false for C8 (hard-coded paths and command).

---

## C1 - PASS

Swap: "For each <CRITERION> that says <QUANTIFIER-WORDS>: (1) write the finite check that would let a reviewer say yes, with its stopping rule; (2) copy the <INSTRUCTION> the <CRITERION> checks and write what set each of the two covers; (3) if you cannot write a finite check, or the two sets differ, mark PROBLEM."
1. Reads correctly and is executable after the swap.
2. Issue-specific words: none. The trigger list (every, all, each, complete, exhaustive, found, covers, no remaining) is quantifier vocabulary, not one defect.
3. Every step is a concrete action (write a check, copy a sentence, list a set). Weak spot, not a fail: no rule for which 4 rows to keep when more than 4 criteria qualify.

First sentence, placeholder version: "For each <CRITERION> that says <QUANTIFIER-WORDS>: (1) write the finite check that would let a reviewer say yes, with its stopping rule; (2) copy the <INSTRUCTION-SENTENCE> the <CRITERION> checks and write what set each of the two covers; (3) if you cannot write a finite check, or the two sets differ, mark PROBLEM."

## C2 - FAIL

Swap: "Split the <DRIVING-DOC> into rules: one per sentence that contains <TRIGGER-WORDS>, or per table row. Take up to <N> rules ... quote the <CANDIDATE> sentence that carries it."
1. Not fully executable. It asks for up to 10 rules, a quote for each, but allows at most 6 rows, so rules 7 to 10 have no place to go. "the candidate" is never defined in the recipe or in rl-block.txt (every other recipe says "the plan"). README.md admits the 10 versus 6 mismatch as a known ambiguity.
2. Issue-specific words: "halts, reports or returns". Must, shall, never, only are ordinary rule words. Halts, reports and returns are run-time behaviour verbs that match one kind of defect (a program that stops or reports on failure) and miss specification wording such as stops, aborts, exits, fails. Related but weaker: "an exit".
3. Steps are concrete except "trace each failure path ... to the output the rule governs", which is a reasoning step with no stated method.

First sentence, placeholder version: "Split the <DRIVING-DOC> into rules: one per sentence that contains <TRIGGER-WORD-LIST>, or per table row."

## C3 - PASS

Swap: "List every <VALUE> that a <TASK> reads, maps or requires as the input to a decision (<EXAMPLES>). For each, find the <ROW-TASK-OR-STEP> that writes it, for every case the reader handles."
1. Reads correctly and is executable. Minor: "the reader" is not defined, but it can only mean the task that reads.
2. Issue-specific words: none. The examples (lookup tables, status mappings, conditions) are generic.
3. Concrete: list, find the writer, mark when there is none. Weak spot, not a fail: no rule for choosing which 4 values when there are many.

First sentence, placeholder version: "List every <VALUE-OR-FIELD-OR-STATE> that a <TASK> reads, maps or requires as the input to a decision (<EXAMPLES>)."

## C4 - FAIL

Swap: "For each <CRITERION> that embeds a <COMMAND-OR-PATTERN>: write the exact text the same <TASK> tells the implementer to write or create. Apply the literal pattern to that text, <MODIFIER> ..."
1. Reads and is executable (scratch string plus Bash is a concrete action).
2. Issue-specific words: "case included" (names one mismatch mode, upper versus lower case); "picks fewer or other checks than the criterion needs" (names one selector defect shape); "it may already contain finished work" (describes the review set-up where the plan was already carried out, not the checking task).
3. Steps are concrete. "ask what the command selects or matches on the current tree" is a question, but it is answerable by running the command.
The recipe does not just describe the class of check, it tells the reviewer which mismatches to find.

First sentence, placeholder version: "For each <CRITERION> that embeds a <COMMAND-PATTERN-SELECTOR-OR-TEST-NAME>: write the exact text the same <TASK> tells the implementer to write or create."

## C5 - FAIL

Swap: "For each <CHANGE> that alters a <LITERAL> that the repository may also state elsewhere: (1) write the old literal; (2) run one search of the whole tree for it, including <ROOT-DOCS>, <COPIES> and comments ..."
1. Steps 1 to 3 execute. The last two sentences do not stand alone: "Grade it with the grading check; never drop it" refers to a check that none of the files I was allowed to read defines.
2. Issue-specific words: "changelogs, readmes, guides" and "mirrored copies" (a list of document kinds that reads like the places a past defect hid). "never drop it" is an outcome instruction, not a procedure.
3. Steps (1) to (3) are concrete. The grading sentence is not an action the recipe can carry out.

First sentence, placeholder version: "For each <CHANGE> that alters a <NUMBER-NAME-COUNT-BEHAVIOR-OR-DEFAULT> that the repository may also state elsewhere: (1) write the old literal; (2) run one search of the whole tree for it, including <ROOT-DOCUMENTS>, <MIRRORED-COPIES> and comments, not only the files the plan names; (3) list every hit the plan neither edits nor checks."

## C6 - PASS

Swap: "For each <CLAIM-SENTENCE> the plan states or dictates that says <UNIVERSAL-WORDS>: (1) name the set it covers; (2) run one count or listing command for that set over the tree; (3) compare with the plan's other tasks and with the scope of the <TEST-OR-CHECK> said to enforce it (<QUESTION>)."
1. Reads correctly and is executable. The count or listing command is left to the reviewer, which is fine.
2. Issue-specific words: none. Watch item, not a fail: the fragment "or outside X nothing" is clumsy grammar; "what does that test skip or not read?" is a generic scope question.
3. Each step is a concrete action (name, run, compare) with a concrete question in the brackets.

First sentence, placeholder version: "For each <CLAIM-SENTENCE> the plan states or dictates that says <UNIVERSAL-WORDS>: (1) name the set it covers; (2) run one count or listing command for that set over the tree; (3) compare with the plan's other tasks and with the scope of the <TEST-OR-CHECK> said to enforce it (<SCOPE-QUESTION>)."

## C7 - PASS

Swap: "List every <CONSTRAINT>, one clause per line (split at <SEPARATORS>). List every <DICTATED-TEXT>. For each text and each constraint on its topic, tick each clause."
1. Reads correctly and is executable. Minor: it does not say where constraints come from, but "the plan" is the only reasonable source.
2. Issue-specific words: none. Semicolons and "and" are generic split points.
3. Concrete: list, list, tick each clause. Weak spot, not a fail: a text-by-clause matrix may exceed 4 rows, and no selection rule is given.

First sentence, placeholder version: "List every <CONSTRAINT>, one clause per line (split at <SEPARATORS>)."

## C8 - FAIL

Swap: "For each <FILE> the plan edits or creates, search <TEST-SCRIPT-DOC-DIRS> for its path and distinctive strings: `<SEARCH-COMMAND> '<STRING>' -- <DIRS>`. For each referencing file the plan never names, open it ..."
1. Executable only for one target. The command `git grep -l -F` and the folders `tests scripts docs` are hard-coded. README.md's own table gives different paths and a different command dialect for specifications and documentation, and lists root-level files for plans, which this recipe never searches (C5 does).
2. Issue-specific words (layout and tool, not a defect as such): "tests scripts docs", "git grep -l -F".
3. Steps are concrete (search, open, decide, mark). It also names an outcome rule ("If it does and no task updates or runs it, mark PROBLEM"), which is the same kind of decision rule the other recipes use.

First sentence, placeholder version: "For each <FILE> the plan edits or creates, search <TEST-SCRIPT-DOC-DIRS> for its path and distinctive strings: `<SEARCH-COMMAND> '<STRING>' -- <DIRS>`."

---

## Summary table

| Recipe | PASS/FAIL | issue-specific words |
|---|---|---|
| C1 | PASS | none |
| C2 | FAIL | "halts, reports or returns"; weaker: "an exit"; also undefined "the candidate" and 10 rules versus 6 rows |
| C3 | PASS | none |
| C4 | FAIL | "case included"; "picks fewer or other checks than the criterion needs"; "it may already contain finished work" |
| C5 | FAIL | "changelogs, readmes, guides"; "mirrored copies"; "never drop it"; undefined "the grading check" |
| C6 | PASS | none (watch: "or outside X nothing") |
| C7 | PASS | none |
| C8 | FAIL | "tests scripts docs"; "git grep -l -F" (hard-coded layout and tool) |
