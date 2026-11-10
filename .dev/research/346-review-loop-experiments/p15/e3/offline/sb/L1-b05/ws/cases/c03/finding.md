**F2. MAJOR, blocking. Expert: Wiegers (testability). The refund window is 90 days in one requirement and 30 days in another**

- Grading sentence: an implementer who follows the stated text as written builds a refund check that accepts a refund 60 days after capture because `A refund may be issued for any captured charge within 90 days of the capture date.` (S:13), and also rejects the same request because `A refund request older than 30 days after capture is rejected with the error code REFUND_EXPIRED.` (S:15). No implementation can satisfy both for a request 60 days after capture, and the acceptance test for refunds cannot be written.
- Recommendation: keep one window and delete the other
- Priority: High. Quality impact: the refund window is 90 days in one requirement and 30 days 
