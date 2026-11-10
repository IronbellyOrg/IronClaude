### F-19 (MINOR, MEDIUM): the plugin mirror of the commands is not covered by any phase check

- Location: spec line 279 (UNVERIFIED #8: how `plugins/superclaude/commands/` is kept in step); line 168 (P0 and AC-0.2 cover only HOW-WE-WORK mirrors); line 173 (AC-C2 covers only `.claude/` sync).
- Issue: each phase edits `src/superclaude/commands/`, and the plugin copies may drift. No AC checks them, and UNVERIFIED #8 says each phase's plan must resolve it first.
- Recommendation: make resolving UNVERIFIED #8 an explicit P0 deliverable, with an AC.
- Expert: Newman (copies that must stay in step).
