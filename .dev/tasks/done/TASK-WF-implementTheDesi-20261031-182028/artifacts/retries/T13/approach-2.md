Implementer claims (A1 + A2), not verified:
- A1: added Codex prose to the five refs: detection-contract.md (new "Codex evidence and selection" section), augment-poll.md (shared snapshot, wait-outcome table, merge table, absence rule), severity-routing.md (P0-P3 hint table, dedup max tier), finding-verify.md (per-finding verdicts in groups), troubleshoot-dispatch.md (group seed naming reviewers).
- A2 fix pass for F1.1: reworded the Codex disable rule (both identities must be blank) in detection-contract.md YAML comment and prose, the SKILL.md Wave 1 sentence and detection.py comments, and added one sentence describing what a single blank codex_bot_login does.
- Believed met: T13.AC1 (each ref names Codex) and T13.AC2 (static_grep, skill_parse, verify-sync).
- The A2 sentence about a single blank codex_bot_login checked only the PR 336 fixture (with Codex threads), not a thread-less PR.
