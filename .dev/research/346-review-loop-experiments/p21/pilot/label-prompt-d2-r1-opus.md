# Task: map review findings to a validated defect ledger

Files (read only these):
- Original spec: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p17/in/spec-original.md
- Ledger: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p17/score/ledger-blind.json (44 defects D01-D44 of the ORIGINAL spec, with quotes, spec lines, what goes wrong; ignore the I and N entries)
- Findings: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p21/pilot/label-in-d2-r1.json (78 findings, written by several independent reviewers of the original spec; `anchor`/`anchor2` quote the spec, `claim` says what is wrong)

For EACH finding decide which ledger defects it reports: the defect(s) whose `what_goes_wrong` the claim describes, at the place the anchors quote. Rules:
- A finding maps to a defect only if fixing that defect would resolve the finding's claim. Same section or same topic is not enough.
- A finding may map to more than one defect only when its claim really reports each of them; list the main one first.
- If the claim is a real problem not in the ledger, use "NEW". If it is not a real defect of the spec (wrong, a style note, a preference), use "NOT_DEFECT".
- Check each mapping against the spec text with grep when unsure.
- Do not look at other files, other runs or any merge output.

Write JSON to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p21/pilot/labels-d2-r1-opus.json:
{"<key>": {"defects": ["D07"], "other": null | "NEW" | "NOT_DEFECT", "confidence": 0.0-1.0}, ...} with every key. Validate it parses and has all 78 keys. Reply `DONE <path>` and one line of counts.
