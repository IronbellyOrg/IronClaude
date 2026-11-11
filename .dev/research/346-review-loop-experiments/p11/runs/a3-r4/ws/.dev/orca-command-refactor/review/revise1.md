# Revise round 1: Orca worker contract spec

Prompt followed: REVISE prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:49-51`. Values: candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, IDS = F-01 (the only id in the Reviser brief, `.dev/orca-command-refactor/review/round1.md:228`). Binding context read first: `.dev/orca-command-refactor/README.md`.

I did not award a PASS and did not run the spec-panel.

## Byte accounting

| Measure | Value |
|---|---|
| Size before | 57763 bytes (SHA-256 `d3cdbe57...5200d`, matches the reviewed hash at `round1.md:9`) |
| Size after | 57873 bytes (SHA-256 `92073bce9aa934458a66ff79344ce2e439141e3c08d2246944949c626f472a09`) |
| Net change | +110 bytes |
| F-01: bytes deleted | 19 (`in sections 3.1-3.2`) |
| F-01: bytes added | 129 (`named in the P1 row of section 6, except `load` (usage-line fix only, no report file, section 3.2 and the Decisions table; F-01),`) |
| Bytes changed for any other id | 0 |

The only changed line is the AC-1.1 row, `specs/orca-worker-contract-spec.md:195` (verified by `diff` against a copy taken before editing).

## One row per finding id

| Id | Disposition | Where | Reason |
|---|---|---|---|
| F-01 | Applied | `specs/orca-worker-contract-spec.md:195` (AC-1.1) | The test now asserts the `## Unattended mode` section only for the commands named in the P1 row of section 6 (`specs/orca-worker-contract-spec.md:159`: analyze, build, business-panel, design, document, explain, index, test, load, plus the fixed adversarial, cleanup-audit, index-repo, workflow), and exempts `load`. That removes the four contradictions listed at `round1.md:92-95`. See the sub-table below. |

### How each part of F-01 is now handled

| F-01 part (`round1.md`) | Result |
|---|---|
| 2. `load` has no report file (`specs/orca-worker-contract-spec.md:112`, `:265`) but AC-1.1 demanded a contract section | `load` is exempt in AC-1.1 itself. Rows 112 and 265 are untouched. |
| 3. brainstorm (`:84`) and init-lite (`:87`) are in no phase list, so P1 could not give them the section | AC-1.1 no longer asserts them, because it follows the P1 list. I did not add either to a phase: that would add a command to a phase, which `round1.md:97` forbids. Their `## Unattended mode` sections are therefore not tested by any phase check. That is a follow-up for the user, not a blocking item. |
| 4. pr-submit (`:114`) is demanded at P1 although D3(a) makes no pr-submit change (`:139-140`, `:240`) | pr-submit is not in the P1 list, so AC-1.1 does not ask for its section at P1. |
| 1. 37 commands asserted, 13 edited | AC-1.1 now matches the 13 edited in P1, so P1 can pass and the gate at `:154` no longer blocks P2 to P4 for this reason. |

## Not touched, and why

- `specs/orca-worker-contract-spec.md:159` (P1 sentence "the `--unattended` flag accepted by every command in sections 3.1 and 3.2"): left as written. F-01's recommendation (`round1.md:97`) is to narrow AC-1.1, not the P1 scope, and the narrowed AC-1.1 does not conflict with it: the flag may still be accepted by every command, but the section assertion is limited to the P1 list. This is a possible residual inconsistency for the re-reviewer to judge.
- `specs/orca-worker-contract-spec.md:112` and `:265` (`load` rows): unchanged.
- M-01 to M-11 and N-01 to N-06: left alone as the prompt requires (`document_review_loop_prompts.md:51`; `round1.md:205-216`).
- Citations: the spec's own grep and source citations remain UNVERIFIED in this sandbox, as stated at `round1.md:22`. The only evidence checked for this revision is the spec itself and `round1.md`.
