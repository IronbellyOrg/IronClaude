# Flags decision

- Decided by: user (taken as given)
- Depth: standard

| Field | Value | Reason |
|---|---|---|
| Mode | bug | User supplied bug. Agree: the reported default-effort request fails with HTTP 400 instead of recovering through the tier; unmatched errors return at `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:803`. |
| Type | skill | User supplied skill. Agree: `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py` belongs to the ccsession-tag skill. |
| Issue type | Bug | Agree: derived from bug mode regardless of area under `refs/labels.md`; the scout lists Bug. |
| Complexity | Medium | Agree: derived from the user's standard depth; the scout lists Medium. |
