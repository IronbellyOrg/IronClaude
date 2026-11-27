# Evidence validation (run 2)

Validator: `evidence-validator` agent (Read, Grep, Glob only), over `adversarial/adversarial/merged-output.md`. It re-read the cited files and returned a table; the orchestrator applied the corrections to `merged-output.md` (the validator cannot write).

Result: 0 citations dropped. 7 line corrections applied (PLAN:34 to 25; PLAN:74, 77 to 72, 75; PLAN:40 to 38, 42 in rows M-04 and M-13; PLAN:29 to 20 in row M-05; PLAN:306, 366 to 309, 369 in prior M-07). 4 weak citations annotated or narrowed (prior M-10 "regressed" reading, row M-07 scope without Task 19, row M-10 "Run with flag" table wording, DESIGN:186 dropped from the NFR-015 note). Row M-09 remains as written (its cases are real; the AC-16 and AC-19 tie is at PLAN:212 as well as 433).

Both Blocking rows hold on substance:

- M-01: PLAN:326 says "a reply that carries no key is not a resolution and the STOP is shown again"; DESIGN:387 (FR-122) says "a reply naming no key counts only when exactly one key was displayed"; REQ:606 carries the same exception; PLAN:20 records no override; PLAN:329 and 386 pin the stricter rule.
- M-02: the Constraint at PLAN:25 requires the plugin twin copy and `cmp` in the same task; Task 19 rewrites `src/superclaude/commands/git.md` (PLAN:234) with no copy or `cmp` (PLAN:234-238); the twin `plugins/superclaude/commands/git.md` exists; the copy is in Task 25 (PLAN:294).

Citation counts: about 132 citations in the merged output, all re-read (the validator covered every row), `citations_dropped: 0`.
