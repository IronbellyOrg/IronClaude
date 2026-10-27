 The failure is not simply “Claude used Write instead of stdout.”
  The stronger, validated root cause is:

  - adversarial-merge is gated against validate/validation-report.md, which is
  populated only from subprocess stdout via ClaudeProcess in
  src/superclaude/cli/pipeline/process.py:114-120.
  - The merge step runs Claude with --print --output-format text --tools default
   from src/superclaude/cli/pipeline/process.py:73-90.
  - If Claude’s final action is a tool call and it emits no trailing assistant
  text, stdout is effectively empty/newline-only.
  - That causes the STRICT gate on validation-report.md to fail in
  src/superclaude/cli/pipeline/gates.py:32-74.
  - After that, the degraded report overwrites validation-report.md in
  src/superclaude/cli/roadmap/validate_executor.py:417-429.

  Why this is validated

  - reflect-merge.md and reflect-merged.md are valid-looking side-effect
  artifacts.
  - validation-report.err is empty, so the subprocess did not crash.
  - I reproduced the critical CLI behavior: with --print --output-format text,
  if Claude ends on a Write tool call with no trailing text, stdout is
  essentially empty.
  - That exactly matches the downstream gate failure mode.

 2. Prompt hardening

  Status: useful, but not sufficient alone.

  Refined version:
  - Update build_merge_prompt() in
  src/superclaude/cli/roadmap/validate_prompts.py:78-126 to explicitly require:
    - final report must be emitted in final assistant text
    - do not rely on Write/Edit for the canonical artifact

  Recommendation:
  - Keep as defense-in-depth only.
  - Do not rely on it as the main fix.

  3. Restrict tools for validation merge

  Status: directionally good, but should be narrowly scoped.

  Refined version:
  - Apply only to the validate adversarial-merge step in
  src/superclaude/cli/roadmap/validate_executor.py:252-261.
  - Do not broadly change all pipeline subprocesses.
  - Best paired with prompt hardening.

  Recommendation:
  - Strong candidate as the main behavioral fix, if implemented narrowly.
-  Proposed build_merge_prompt() tightening steps

  Do not implement yet.

  Prompt changes to add

  1. Add an explicit canonical output instruction near the top:
    - “Your final deliverable is the text printed in your final assistant
  response.”
    - “Do not create files for the final report.”
  2. Add an explicit prohibition:
    - “Do NOT use Write, Edit, or any file-creation tool to produce the
  validation report.”
  3. Add a completion rule:
    - “The task is not complete until the full report appears in your final
  assistant text output.”
  4. Reinforce frontmatter position:
    - “Your final assistant response must begin immediately with YAML
  frontmatter.”
  5. Reinforce no trailing tool-only completion:
    - “Do not end your work on a tool call. End with the full final report as
  plain text.”
  6. Add canonical artifact wording:
    - “The canonical validation artifact is the final emitted report text, not
  any side-effect file.”
  7. Keep the existing format contract, but make it final-message specific:
    - agreement table
    - consolidated findings
    - summary
    - required frontmatter fields

  Suggested prompt intent

  This should make the model treat stdout text as the required artifact, while
  reducing the chance it treats file-writing as acceptable completion.

  Important caveat

  This is only a guardrail. It should not be treated as the sole fix for the
  validated root cause.