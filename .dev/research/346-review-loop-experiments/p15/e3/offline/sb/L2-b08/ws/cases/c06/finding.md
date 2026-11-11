**F2. MAJOR, blocking. Expert: Wiegers (testability). A waiting backup is skipped**

- Grading sentence: an implementer who follows the stated text as written builds a scheduler that skips a due backup while the previous one runs, because `makes the next one wait until it finishes` (S:6), and the Sunday full backup is lost.
- Recommendation: none
- Priority: High. Quality impact: a waiting backup is skipped
