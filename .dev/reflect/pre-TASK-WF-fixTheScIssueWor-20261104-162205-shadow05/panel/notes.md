# Panel notes (shadow run)

## Identity (step 9)
- identity_source: requested-pinned (the orchestrator knows only the model it asked for; no transcript read-back of the resolved model id)
- reviewer-1 pin t1b/sonnet; self-report "claude-gw-tier1b" — match
- reviewer-2 pin t4/haiku; self-report "claude-gw-tier1b (haiku-class reviewer)" — MISMATCH
- reviewer-3 pin t1a/opus; self-report "claude-gw-tier1b (Claude, opus-class per the brief)" — MISMATCH
- identity_mismatch_suspected: true. While identity is requested-pinned, no claim of verified independence is made. shadow03 observed the same self-report drift (2/3), so this is a recurring gateway artifact, not new.

## Judge identity (step 7, recorded after the debate)
- judge_identity: unknown (sc-adversarial-protocol's return contract names no judge model)
- judge_class_collision: unknown (never false)

## Findings-block normalization (step 4)
- First cluster pass listed all 3 cards invalid: reviewer cards used severity INFO (schema allows CRITICAL/MAJOR/MINOR), ad-hoc categories (allowed: contradiction, unpassable-check, data-loss, safety, missing-requirement, other), and two claims over 300 chars, plus one "lense" typo and missing line_end keys.
- Normalization was mechanical (INFO->MINOR, category vocabulary map, claim trims that removed no facts, line_end completion); card bodies and calibrations unchanged. Final pass: 10/10 calibrated, cluster_agreement 1.0, 19 citations checked, 0 flagged.
- Root cause: the reviewer spawn prompts did not state the findings-v2 schema vocabulary (severity enum, category enum, 300-char claim cap). The shadow03 run presumably hit this too (its cards carry CRITICAL/MAJOR/MINOR only). Action for the panel work: embed the schema enum in the reviewer-brief findings-block instruction line.

## Parity (step 2)
- panel_parity: true — resolution.json (analyzer/t1b, qa/t4, refactorer/t1a) matches the legacy rotation as it ran (analyzer/sonnet, qa/haiku, refactorer/opus).
