# Panel notes (shadow run, comboA-r2)

## findings_block_compliance_rate
- First parse (deterministic `review cluster` parser): 2/3 = 0.6667. reviewer-2's block was
  invalid: F2 carried coverage_rows ["INF-041"] (reviewer-3's slice). The orchestrator's own
  ad-hoc parse initially reported 3/3; the cluster parser's coverage-slice check is authoritative
  and found the defect. Recorded honestly.
- After ONE bounded re-ask (block only): 3/3 valid. Reviewer-2 returned F2 with coverage_rows: [].
- Re-ask attempt could not be recorded in the manifest (stage 'collected' already committed;
  OutOfOrder refused) — recorded here instead.

## calibration_coverage
- 13/13 after the re-ask (4 + 2 + 7 findings; before the re-ask the invalid block held its 2
  findings out of clustering, so the first pass printed 11/11).

## Identity (requested-pinned)
- reviewer-1: pin claude-sonnet-5-5 (alias claude-gw-tier1b[1m]); self-report "claude-gw-tier1b
  (Claude, Anthropic)" -> consistent with pin class. No mismatch.
- reviewer-2: pin claude-haiku-5-5 (resolution alias claude-gw-tier4[1m]); self-report "OpenAI GPT
  assistant" -> MISMATCH suspected (served model is a GPT model behind a claude-* alias; matches
  the combo-A design expectation HAIKU=tier2 and the workspace's 4th+ sighting pattern).
- reviewer-3: pin claude-opus-5-5 (alias claude-gw-tier1a[1m]); self-report "claude-gw-tier1a[1m]
  (Claude...)" -> consistent. No mismatch.
- identity_source: requested-pinned throughout (no transcript read of the served model id).
  While requested-pinned, no claim of verified independence is made for this panel.

## judge
- judge_identity: claude-gw-tier3 orchestrator session (inline sc-adversarial debate, skill-direct;
  no separate judge record in the adversarial contract) -> judge_class_collision: unknown per
  protocol (contract names no separate judge). The judge IS the tier3 orchestrator class, which is
  not any reviewer pin class (tier1b/tier4/tier1a), so no reviewer collision is observed, but this
  is orchestrator knowledge, not a contract field.

## verify-citations precheck
- 41 checked / 41 flagged, all `not-in-snapshot`: the run's input snapshot holds only the 2 frozen
  input files; reviewer citations point into input/ paths outside the snapshot and repo files.
  Expected for this corpus (same shape as comboA-r1's 62 flags). All 41 join the evidence-validator
  re-read set; the validator alone decides drops.

## orchestrator card-persistence incidents
- Reviewers are read-only (no Write tool) and return cards in-band; the orchestrator persists.
  While persisting reviewer-3's card, the orchestrator introduced 3 transcription corruptions
  (F2/F7 path strings, F4/F5 JSON mangling) and repaired them to the reviewer's actual output
  before any downstream consumer read the card. Recorded per the shadow14 memory lesson
  ("Read cards back after writing").
