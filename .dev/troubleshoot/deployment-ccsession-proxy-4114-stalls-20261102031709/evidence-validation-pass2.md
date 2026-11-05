# Evidence Validation Report (pass 2)

**Report under validation**: .../REPORT.md.draft (revised after pass 1)
**Timestamp**: omitted by the validator (input_absent: now_iso)
**Source**: evidence-validator agent (persisted by the parent on receipt)
**Scope**: Evidence 13, every factual claim in the reworded Diagnosis paragraphs, tier1-observation.md O12
**Total**: 30  **Verified**: 22  **Dropped**: 3  **Passed through**: 5
**Suggested report status**: partial

## Verified (summary)

E13a-e (all four scrollback files hold the quoted reuse/start/stale lines); D1.1 ccsession-orca:81; D1.2 models.py:799 (wording fix: the port is computed at ccsession:1328 via `models.py shim-port`, before `setup_shim` at :1330); D1.3 ccsession:769-784; D1.4 ccsession:772-781 (no restart/watchdog code anywhere); D1.8 ccsession:741-747 + local-gateway-alias-proxy.py:530 (upstream mismatch => stale; inference); D2.1 SigIgn decode; D2.2 Orca chunk descendant walk + SIGTERM/SIGKILL, daemon-entry.js `terminateDescendants` on both kill paths; D2.3 reuse lines; D2.4 only one surviving "Starting ... 4114" (serve-46e81c2f; surviving scrollback only); D2.5 daemon.log:680-681; D2.6 daemon.log:666-667, 669, 671; D2.7 daemon.log:750-751; D2.8 daemon.log:745, 747, 750-751; D2.10 killed sessions' scrollback absent; D2.11 daemon.log:752-753; D2.12 local-gateway-alias-proxy.py:487 (`protocol_version = "HTTP/1.0"  # close-delimited`); D2.14 live-check/before.txt:2-4.

## Dropped

| # | Claim | Reason | Recommended action |
|---|---|---|---|
| 1 | "that is why the coordinator on 4013 never failed" | no run artifact ties a coordinator session to 4013 | reword to "the 4013 shim is still alive"; label the coordinator fact as coordinator-reported in Grounding Gaps |
| 2 | "ccsession.env modified 23:44:00, 24 s before the first 4114 shim's launch" | the 24 s is to the release-readiness terminal's creation (daemon.log:669), not an observed shim launch; mtime only in O12 | reword to "24 s before Orca created the release-readiness terminal (daemon.log:669), the inferred owner"; pass mtime through as captured output |
| 3 | "timeouts, single-threaded server, upstream drops, OOM, SIGHUP and port conflicts are ruled out (Evidence 11-12)" | SIGHUP is Evidence 8; upstream drops and port conflicts not covered; O12 shows 4013 has a different upstream, so it is no upstream control | cite Evidence 8, 11-12; justify upstream drop by mechanism (cuts one stream, leaves the port listening, cannot cause ECONNREFUSED; cuts coincide with session kills); port conflict by local-gateway-alias-proxy.py:857-870 and ccsession:762-764 |

## Passed through

pid/tree facts (O1-O3, live); coordinator-reported screen times and error strings; health sha prefixes (runtime only).

## Structural assertions

A1 no; A2 skipped (diff_path absent); A3 no (mtime clause skipped: artifact_mtimes absent); A4 no; A5 no; A6 skipped; A7 no; A8 no; A9 skipped; A10 no.

## Notes (validator)

- O12 match counts misworded (the regex returns 5 lines per file; the two relevant lines are quoted correctly).
- tier1-hypothesis.md:74 premise "4013 uses the same upstream" is contradicted by O12 (calibration predates O12).
- Elimination counts terminal creations, not ccsession launches; "best-fitting"/"inferred" wording is acceptable.
- Corroboration: surviving scrollbacks that reused 4013 all come from sessions created on or before 2026-10-31T14:47:45Z, before the env-file mtime and the first 4114 reuse.

## Parent disposition (step 3.25)

All three drops applied to the draft as recommended; reword items applied (port computation site, Summary partial sentence, Grounding Gaps for coordinator-reported strings and the stale card premise). Status contribution: partial (merged with pass 1: partial).
