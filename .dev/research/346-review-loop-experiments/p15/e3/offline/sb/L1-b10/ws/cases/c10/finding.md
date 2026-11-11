**F3. MAJOR, blocking. Expert: Wiegers (testability). Exports never include activity logs**

- Grading sentence: an implementer who follows the stated text as written builds an export that never includes activity logs, because `Activity logs are included in an export only when the user asks for them.` (S:22), and that is wrong because users cannot get their logs.
- Recommendation: state that logs are included on request
- Priority: High. Quality impact: exports never include activity logs
