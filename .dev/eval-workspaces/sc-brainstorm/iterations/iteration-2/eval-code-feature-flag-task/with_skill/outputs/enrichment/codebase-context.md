# Codebase Context — Feature Flags

- No existing feature-flag framework is assumed in the current package structure.
- Implementation should land behind a small core module rather than coupling to slash-command definitions.
- Existing project conventions prefer source-of-truth files under `src/superclaude/` and generated/dev copies only after sync.
- Tests should use UV and project pytest conventions.
