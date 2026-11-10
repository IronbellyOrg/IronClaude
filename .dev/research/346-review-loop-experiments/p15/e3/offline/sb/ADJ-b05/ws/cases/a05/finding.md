**F4. MAJOR, blocking. Expert: Wiegers (testability). Security alerts are dropped when the SMS limit is reached**

- Grading sentence: an implementer who follows the stated text as written builds a limiter that drops a security alert once the hourly SMS limit is reached (`security alerts are dropped like any other notification under R8`, S:24), so a user under attack loses the alert, which is wrong because it breaks a safety boundary.
- Recommendation: exempt security alerts from the limit
- Priority: High. Quality impact: security alerts are dropped when the sms limit is reached
