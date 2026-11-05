# Round 1: Variant 1 Advocate (sonnet, analyzer)

**Position summary.** Variant 1 is the only card that finds a verifiably false plan claim: plan:80 says bare `/ponytail` switches to `full`, but under the lite default it reports the level when on and switches to the default (lite) when off (`/tmp/ponytail-src-t14b/mode-tracker.js:109-119`). That false claim would ship in user docs, so `needs_revision` fits and `pass` does not. Variant 1 is narrower than Variant 3 on process hardening and its severity labels need adjusting.

**Steelman V2.** Audited all 16 spec units, traced owners, confirmed T5 fails on unfixed code (`install_user_setup.py:292,303,305`), showed unmapped rows are matcher artifacts, caught the unquoted goal span. Critique: "no false claims found" rests on taking upstream facts "as given"; `fully_adherent: 16` cannot stand with a false Task 3 claim.

**Steelman V3.** Widest scope; R3-1 extends isolation to `XDG_CONFIG_HOME` (`hooks_ponytail-config.js:55-56`, plan:79); R3-5 shows plan:89's AC cannot hold for claims outside the facts block (plan:80-83); R3-4/R3-8 are real process gaps. Critique: R3-5 names the defect class without finding the false instance; R3-1 graded unconditionally blocking although both variables are unset.

**Strengths claimed.** (1) R1-F1 verified true against upstream. (2) Only finding that prevents a wrong statement in shipped docs; plan:88/108/89 do not guard it. (3) Correct class (drift) with exact replacement wording. (4) CLAUDE_CONFIG_DIR finding grounded (`install_mcp.py:721`, `installation.md:362-366`, `hooks_ponytail-config.js:72-73`) and honestly conditional. (5) Breadth of confirmed claims, re-checked (292/303/305, `six plugins` only at installation.md:354).

**Weaknesses in others.** V2: false "no false claims"; R2-F3 rule too tight (`<= 4 ins, <= 3 del` prescribes one implementation); treats Task 2's list as owning tests/docs. V3: R3-1 over-graded; missed the factual error; low-value nits (R3-3, R3-6, R3-7).

**Concessions.** R1-F2 omits XDG_CONFIG_HOME and should be minor; R1-F3 misclassified as authorized (grounding gap is better; V3's bound better); R1-F4 duplicates R3-9; did not raise tests/docs (low impact: `test_retired_docs_absent.py:37-49` only checks a fixed retired-link list).

**Per-point positions.** S-001 equal; S-002 1 (3 close); C-001 1; C-002 3; C-003 3; C-004 3; C-005 2; C-006 3; C-007 equal; C-008 equal; C-009 3; C-010 3; C-011 3; X-001 1; X-002 3; X-003 equal.

**Shared assumptions.** A-001 QUALIFY: snapshot of 96608e07, unpinned (plan:30); record installed plugin version in docs/M1b. A-002 QUALIFY: premise holds (sc-workflow-protocol forbids plan edits from findings); the report must lead with R1-F1 as a required implementation-time correction with exact wording.
