Initial questions

Question: bot feature release and bug fixes are equally important
Question 2: Yes, all 4 in layers but those layers can be released over multiple releases in order to complete and test one before moving on to the others
Question 3: the simplest is not running make sync-dev after a release.  Meaning the global version is the old and the local is the new.  Another before an after scenario is a simple claude prompt like 'build me a tasklist for this roadmap versus using sc:workflow or sc:tasklist'
Question 4: Likely 2 separate commands that can share some of the same skills.  Ultimately we will want to move them out of claude code and have them be programmatically orchestrated via the CLI, at which point they will share even more infrastructure
Question 5: Consistent within a model is the biggest priority.  We don't necessarily need consistency across models at all, but testing across models is valuable to be able to score cheaper faster models and see if improvements to the skills or harnesses can improve those scores enough to enable a cheaper model to perform close enough to something like opus
Question 6: totally fine for now

 Each prompt file has 3 sections:

  1. Context section — Pre-loaded with:
    - Critical lessons (the rejection lesson, 12-steps-not-13,
  conditional stages)
    - Pipeline architecture facts
    - Placeholders for upstream prompt outputs (marked <!--
  PLACEHOLDER -->)
  2. The prompt itself — The refactored prompt from the
  adversarial debates
  3. Post-Run instructions — Tells the operator exactly what to
   append to the next prompt's context section after this
  prompt completes, with a structured template

  Context Flow Chain

  ┌─────────────┬─────────┬────────────────────────────────┐
  │   After     │ Append  │       Key data forwarded       │
  │ running...  │  to...  │                                │
  ├─────────────┼─────────┼────────────────────────────────┤
  │             │ P2 and  │ eval-spec path, AMBIGUITY      │
  │ P1          │ P3      │ count, dry-run result, files   │
  │             │         │ referenced                     │
  ├─────────────┼─────────┼────────────────────────────────┤
  │             │         │ Stage review summary, coverage │
  │ P2          │ P3      │  gaps, trivially-passing       │
  │             │         │ stages                         │
  ├─────────────┼─────────┼────────────────────────────────┤
  │             │         │ eval-e2e-design path, 3        │
  │ P3          │ P4      │ impacts, build status (scripts │
  │             │         │  vs design-only)               │
  ├─────────────┼─────────┼────────────────────────────────┤
  │             │         │ Validation status              │
  │ P4          │ P5      │ (PASS/BLOCKED), per-criterion  │
  │             │         │ results                        │
  ├─────────────┼─────────┼────────────────────────────────┤
  │             │         │ Scoring framework path, runs   │
  │ P5          │ P6      │ completed, timing, delta       │
  │             │         │ methodology                    │
  ├─────────────┼─────────┼────────────────────────────────┤
  │ P6          │ —       │ Final output (eval-report.md)  │
  └─────────────┴─────────┴────────────────────────────────┘

Key Questions:
1) Manual for now
2) Same interface
3) Both.  
4) Yes
5) Judge model
 ]