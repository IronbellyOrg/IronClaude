**F2. MAJOR, blocking. Expert: Wiegers (testability). A retry overwrites a file that is never overwritten**

- Grading sentence: an implementer who follows the stated text as written builds a writer that never overwrites (`Existing files in the output directory are never overwritten; a numeric suffix is added to the new file name.`, S:7) and a retry that overwrites the partial file (`the retry reuses the file name of the failed attempt and overwrites the partial file`, S:12). The retry must add a suffix and reuse the name, so the retry test cannot pass.
- Recommendation: say that partial files are the exception
- Priority: High. Quality impact: a retry overwrites a file that is never overwritten
