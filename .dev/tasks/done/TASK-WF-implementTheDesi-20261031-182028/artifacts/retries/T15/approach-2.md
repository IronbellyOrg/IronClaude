Implementer claims (A1 + A2), not verified:
- A1: changed only the pr-submit sentences of CLAUDE.md:50, docs/user-guide/commands.md:361 and the two release guides (Augment app or Codex connector), and added a CHANGELOG Unreleased entry listing Codex support, fail-open detection, P0-P3 mapping, dedup, per-reviewer re-trigger and the UNVERIFIED marker update.
- A2 fix pass: qualified the reviewer_incomplete sentence (other reviewer's result used only when it completes; terminal_timeout when none completes) and replaced "write-ahead" with "appended right after its successful post".
- Believed met: T15.AC1 (grep finds no Augment-only pr-submit sentence) and T15.AC2 (make lint, named pytest set).
- The CHANGELOG re-trigger line was written from the Wave 6 review-fix path only; the Wave 8 CI-fix push (no re-trigger) was not checked.
