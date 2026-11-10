**F2. MAJOR, blocking. Expert: Wiegers (testability). Urgent notifications are queued until 07:00**

- Grading sentence: an implementer who follows the stated text as written builds a queue that holds urgent notifications created at 23:00 until 07:00, because `Notifications of other priorities created during quiet hours are queued and delivered at 07:00.` (S:10) is read next to `Urgent notifications are delivered at any hour.` (S:11), and an urgent alert arrives eight hours late.
- Recommendation: none
- Priority: High. Quality impact: urgent notifications are queued until 07:00
