**F1. MAJOR, blocking. Expert: Wiegers (testability). A failed channel is never retried over another channel, except for security alerts**

- Grading sentence: an implementer who follows the stated text as written builds a sender that never uses a second channel (`If the preferred channel fails, the notification is not sent over another channel.`, S:6) and falls back to email for a failed SMS security alert (`If SMS delivery fails for a security alert, the service falls back to email.`, S:19). A failed SMS security alert must stay unsent and be sent by email, so the fallback test cannot pass.
- Recommendation: state the exception in R3
- Priority: High. Quality impact: a failed channel is never retried over another channel, exce
