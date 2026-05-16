# D-0010 — Implementation Notes

## Design choices

**Step numbering (2a vs renumber-everything):** The guard was inserted as Prerequisites step 2a (not a new step 3) so the existing numeric sequence (1, 2, 3, 4, 5, 6) is preserved and downstream references to step numbers remain valid. The 2a label also matches the task spec verbatim ("step 2a").

**Behaviour-cited, not file-path-cited refusal message:** Per R-04 mitigation guidance in `notes-Roadmap-Audit.md`, the refusal message names the three forbidden *prefixes* (the behaviour being enforced) rather than concrete file paths inside `.claude/skills/`. This survives refactors of any individual skill or command.

**Why mention `.dev/README.md` in the refusal:** Operators who hit this guard need a single canonical pointer to learn the project convention. The override addendum in `CLAUDE.md` already names `.dev/README.md` as the authoritative source.

**Why also add an Error Handling row:** Two-layer documentation inside the skill — one in the imperative Prerequisites flow ("when this happens, STOP"), one in the descriptive Error Handling table — so a reader scanning either section discovers the policy.

**Options-table policy clause embedded in the `--output` row:** Rather than introducing a new "Policy" row that has no `Flag` / `Short` columns to populate, the policy text was appended to the Description column of the existing `--output` row. This keeps the table well-formed Markdown.

## Verification strategy

`sc-release-split-protocol` is a Claude Code skill, not a standalone CLI; "invocation" verification is therefore behavioural — the SKILL.md instructs Claude to refuse before any write, and the test is to confirm that the refusal text exists in step 2a and that the guard executes BEFORE Part 1 begins. Evidence is captured by grep-extracting the step 2a clause and the Options-table policy entry from the on-disk files post-sync.

## DEP-005 SOFT dependency on M2

`make verify-sync` is exercised in this task only as a sync check (`✅ All components in sync.`). The M2 D2.1 / D2.2 "redirect message" probes belong to T02.01 / T02.02 evidence. M4 is not gated on M2 message correctness — only on `make verify-sync` exiting 0, which it does.

## Out of scope (re-noted)

- T04.02 (sibling skills) — separate task; T04.01 does not block its scheduling.
- Hook-layer enforcement — Phase 1 / M1.
- CI gate redirect message — Phase 2 / M2.
