<!-- Provenance: produced by /sc:adversarial -->
<!-- Base: Variant 2 (proposal-B) -->
<!-- Merge date: 2026-11-14 -->
<!-- Incorporated: Variant 1 (proposal-A) facts and Q18 statement; Variant 3 (proposal-C) TUIBBS screen kept visible as a possible later reader; debate consensus on A-001, A-002, A-003, X-002. Plan: adversarial/refactor-plan.md (5 changes). -->

# Proposal B (merged): "TUI Panel" means `superclaude observe` (the #409 dashboard), single-host and read-only today; later readers not decided

<!-- Source: Variant 2 base, modified by Change 1 (converged reply line; Variant 1 facts ADJ E-01, glossary line 77; Variant 3 TUIBBS screen kept visible) and Change 2 (base qualifier on the meaning dropped) -->
## Answer

"TUI Panel" means `superclaude observe`, the #409 dashboard, built and merged (PRs #503, #514). Today it reads Orca on one host only and is read-only (ADJ E-01, line 127; glossary, line 92); the ADJ glossary already equates it with "the 'TUI panel' in the owner's wording" (ADJ glossary, line 77). This is recorded as the owner's meaning, with today's properties. The owner makes no statement now about whether single-host or read-only last, or about later readers: a TUIBBS screen reading the observer's snapshot stays a possible later reader, not decided. The Coder#477 reply says: "TUI Panel = `superclaude observe` (the #409 dashboard); single-host and read-only today; later readers, including a possible TUIBBS screen, not decided."

<!-- Source: Variant 2 base, modified by Change 2 (step 1), Change 1 and Change 4 (step 2, debate A-001, A-002), Change 3 (step 3, Variant 1 Q18 statement) -->
## What happens next if the owner picks it

1. The ledger records the owner's meaning, with today's properties, its date and the words "later readers not decided".
2. The owner sees the exact line before it is posted, because the reply is public in another repository. CO-01 then carries that line in the Coder#477 reply. The line names "the #409 dashboard" so that a wrong guess is visible to any reader.
3. Q3 is answered on its own merits, without using "single-host today" as the close test. Q18 stays at its recommended "not yet": "not before observer release R4 or an owner statement that a TUIBBS screen is planned" (`merged-requirements.md:545`). This answer is not such a statement and does not change Q18.
4. The question is re-asked when observer release R4 or a TUIBBS task package is proposed.

<!-- Source: Variant 2 base, bullets 1 and 2 adjusted for consistency with Change 1; last bullet appended by Change 5 (debate X-002, ADJ line 187) -->
## What it unlocks

- CO-01 can be posted with a true statement the owner can stand behind today, about a program that exists and is merged.
- It does not pre-decide Q3 or Q18: "today" scopes the host and read-only properties, and nothing in the reply rules a remote or TUIBBS reader in or out.
- It keeps the owner's 2026-11-08 direction ("the observer may become a TUIBBS module", "Background, not deciding") exactly as undecided as the owner left it.
- #409's Go lineage is not treated as TUIBBS intent: the #409 issue body preferred a Go stack "informed by TUIBBS-scp styling and components" (`.dev/issues/409/issue-body.md:25`), but the owner replaced that direction with Python plus Rich on 2026-11-08 (ADJ line 187), and the built observer is a `superclaude` CLI command (ADJ E-01).

<!-- Source: Variant 2 base, all three bullets rewritten for consistency with the Change 1 reply line and the Change 3 Q18 statement -->
## What it costs or risks

- The reply states only what is true today: a Coder#477 reader cannot tell from it whether the feature must later serve one host or several.
- Q3 still rests on its own merits: "single-host today" is a present-tense fact and cannot test the ADJ's close condition "the observer stays single-host and TUIBBS is not near" (ADJ line 283).
- A re-ask is expected only when observer release R4 or a TUIBBS task package is proposed.

<!-- Source: Variant 2 base, modified by Change 3 (Q18 at "not yet") and Change 4 (debate A-001: Coder-side panel not ruled out) -->
## What stays unresolved

- Whether single-host and read-only last beyond today: remote fleet is the observer's planned release R4, and the write behaviour of release R3 (Decision Desk) is UNVERIFIED.
- Whether a TUIBBS screen ever reads the observer's snapshot, and the transport for any later reader.
- Whether "TUI Panel" could mean a Coder-side panel: the phrase appears in no owner-written file, Coder#477 lists Coder template files, and nobody searched the Coder repository for the phrase (UNVERIFIED). Naming "the #409 dashboard" in the reply keeps a wrong guess visible.
- Q18 (at its recommended "not yet") and Q22.
