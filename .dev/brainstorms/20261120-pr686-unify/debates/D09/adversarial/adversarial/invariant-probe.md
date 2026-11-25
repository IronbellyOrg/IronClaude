# Invariant Probe Results

## Round 2.5: Fault-Finder Analysis

Source: independent fault-finder agent (agent id a6ee8bbdbf20ce8a2), read-only. Evidence marked "agent-reported" was not re-read by the moderator. Moderator verification is noted in the Status column.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | interaction_effects | A held issue leaves the hold when someone edits the body and then reaches launch | UNADDRESSED (moderator: addressed by owner rule R19/R36; edit voids approval, re-approval needed, fails closed; spec line required) | HIGH | Local `predicates.py:275-297` (`unchanged_since`), local `requirements.md:45` (R19) and `:62` (R36); agent-reported. Local branch has no hold code, ordering UNVERIFIED |
| INV-002 | sufficiency_challenge | "Master has no human approval gate; assignment is the only trigger" | UNADDRESSED (moderator: addressed by correction, VERIFIED) | HIGH | Master `cycle.py:883`, `:998` call `approval_of`; PR 686 head has 0 references (moderator grep). The no-gate tree is the PR 686 head and design 681, not master |
| INV-003 | state_variables | `issue.hold` grant is a per-repo switch and turning it off is a clean rollback | UNADDRESSED | MEDIUM | Grant is document-level (`pr-a/.../repos.py:94-115`), no-grant path skips at `cycle.py:1064-1070` and at the re-read `:1299-1300`; agent-reported. Moderator verified `cycle.py:1021-1027` and `test_hold.py:416-426` (no grant gives `hold_write_failed`) |
| INV-004 | sufficiency_challenge | Passing `plan_check` means the author wrote something under each heading | UNADDRESSED | MEDIUM | Moderator verified: `hold.py:69-70`, `:140` strip only HTML comments; the issue template `issue-bug-simple.md:43-62` has `<...>` placeholder lines under all three headings, so an unfilled template passes |
| INV-005 | collection_boundaries | Every issue a person wants worked has the three exact headings | UNADDRESSED | MEDIUM | `hold.py:105-119` exact heading match; repo issue forms have no plan fields; agent-reported |
| INV-006 | count_divergence | The call budget bounds repeated failed writes | UNADDRESSED | MEDIUM | `github.py:1035-1048` failure not remembered, `test_hold.py:410-413` no store entry, cap 35 minus 3 (`issue-watcher.md:361,391`); agent-reported, call order partly UNVERIFIED |
| INV-007 | guard_conditions | Reading the body for `plan_check` needs only an NG-2 amendment | UNADDRESSED | MEDIUM | Master `issue-watcher.md:226` and local `github.py:7-8`, `test_security_invariants.py:79,273-279,960` (NFR-002: no body in argv); agent-reported. A second rule changes: reading the body |
| INV-008 | state_variables | A label a person removes by hand stays removed | UNADDRESSED | MEDIUM | Per-workspace `holds` store (`cycle.py:1100-1119`, `:1130-1133`): a second workspace re-adds the label; agent-reported |
| INV-009 | collection_boundaries | The poll never creates labels; per-repo init does | UNADDRESSED | LOW | PR 686 `LabelWriter.ensure` creates (`github.py:1028-1048`, `test_hold.py:381`); owner init creates only the trigger label (`repo_init.py:1-5,108-116`); `hold:backlog` by hand conflicts with R17; agent-reported |
| INV-010 | guard_conditions | `plan_check` is cheap and safe on any body | UNADDRESSED | LOW | `_CLOSED_COMMENT` regex quadratic on unclosed `<!--` (agent timed 4.7 s on 64,000 characters, `hold.py:70`, `:102`); agent-reported |

## Summary

- **Total findings**: 10
- **ADDRESSED**: 0 by the debate; 2 (INV-001, INV-002) addressed afterwards by moderator resolution
- **UNADDRESSED (before moderator action)**: 10
  - HIGH: 2 (cleared by moderator resolution, see debate-transcript.md Round 2.5)
  - MEDIUM: 6 (warnings, do not block)
  - LOW: 2
- Checked and holding (agent-reported): baseline of already-assigned issues, live re-read before wake (`cycle.py:1279-1300`), dry-run shadow store, unlisted repos get no writes, a person-placed `hold:plan` on a complete issue is removed by the poll.
