# ab6: A2 as a shadow seam only (A1 and A3 dropped)

Decision (owner, 2026-11-10): drop the A1 and A3 hints; build ab6 around A2 (acceptance-check observability) as a shadow seam. Shadow = the seam runs, its output is logged, and it never reaches a reviewer, a verifier or a reviser.

## What was built (this directory)
* `a2_observability.py`: code stage first (widened lint REF+PATH+PHASE, the D20/D21 pitfall regexes, execution of shell/grep/YAML check rows in a scratch copy with mutation probes), then a Jev `observability` question only on rows that pass the code stage. Output: up to 8 UNVERIFIED lines per spec, written to the log only.
* `replay.py` (A2 only), `score_gates.py` (A2 only), `seamlib.py` (privacy guard, budget reservation, journal, cache, strict answer validation: any error or `insufficient` is a fallback), `decision.toml`, 12 tests (mock transport, no key, all pass).
* The seam is a pure observer of spec text, so it is applied after the fact to the stored spec versions of any run (the replicate included) without touching the loop or holding the Jev key inside the monitor. Coordinator-only live call: `bash -c 'set -a; . $SP/.jev.env; set +a; python3 replay.py --seam a2 --live'`, then keyscan.
* Not included: the free tweaks F1-F4 (they change loop behaviour and are untested on the new best arms). Say if you want them as a separate arm.

## Live shadow run on 37 specs (original + the 36 finals of ab4, PN1, ab5 panel/full, PN1 cost-matched, PN1 doubled-Haiku): 992 Jev calls, $0.009, all usable, key scan clean
| measure | result |
|---|---|
| Jev flags (`cannot_pass`/`cannot_discriminate`) | 867 of 1,190 rows (73%) |
| flag rate on rows whose mapped defect is still present | 72% (508/705) |
| flag rate on rows whose mapped defects are all FIXED in that spec | 81% (60/74) |
| flag rate on rows that map to no ledger defect | 73% (299/411) |
| code-stage (no Jev) flagged rows that carry a residual defect | 93% (184/198), against 53% for unflagged rows |
| original gate (tail defects caught beyond controls, kill rule >= 3) | 12 tail defects: passes, but only because Jev flags nearly every row |

Reading: Jev's A2 flag does not discriminate (72% / 81% / 73% across the three row classes), so the earlier "tail catch" pass is an artefact of flagging almost everything. The deterministic code stage is the useful part (93% precision on its flags, lift 1.75 over the base rate). Recommendation: keep the code stage as the shadow signal; keep the Jev call in the shadow log only for data, with no path to a prompt, and treat promotion of any Jev-derived hint as not supported by this evidence.
