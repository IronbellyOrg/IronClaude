3939477e29cadc940a1cd304bdf78131bfa8653b
## family codex-disable-semantics
defect form: text says one empty/null Codex value disables Codex, while the core blanks keys one at a time and Codex stays on while either identity remains
command: grep -rn -i "disables Codex\|empty Codex identity\|disable Codex" src/superclaude/skills/sc-pr-submit-protocol/ src/superclaude/pr_submit/ src/superclaude/commands/pr-submit.md tests/pr_submit/*.py
before:
refs/detection-contract.md:31 (YAML comment), refs/detection-contract.md:80, SKILL.md:269, pr_submit/detection.py:46 and :149 (comments), tests/pr_submit/test_detection_contract.py:275 (docstring; test blanks both keys, accurate)
coupled sites: design section 18 A0 has the same ambiguous wording (specification, not edited)
after:
src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md:31:# shipped values; setting BOTH identities to "" disables Codex.
src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md:79:literal. An empty identity set disables Codex: it is never present. An override file that omits the
src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md:80:Codex keys keeps the shipped values. An explicit empty or null value blanks that one key; to disable
src/superclaude/pr_submit/detection.py:46:# empty or null value blanks that one identity, and Codex is disabled only when
src/superclaude/pr_submit/detection.py:140:    # from_yaml supply the real values. An empty identity set disables Codex.
src/superclaude/pr_submit/detection.py:150:        shipped Codex value; a present empty or null value blanks that identity.
