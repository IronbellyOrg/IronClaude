**F3. MAJOR, blocking. Expert: Wiegers (testability). Retries and the failed state disagree**

- Grading sentence: an implementer who follows the stated text as written builds a service that marks the charge failed after the first failed capture, because `After the third failed attempt the charge moves to state failed` (S:10) is read next to `The service retries a failed capture up to 3 times, with 10 minutes between attempts.` (S:9), and the charge is wrong because the retries never run.
- Recommendation: say that the retries run before the failed state
- Priority: High. Quality impact: retries and the failed state disagree
