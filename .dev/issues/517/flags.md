# Flags decision

- Decided by: user (taken as given)
- Depth: standard

| Field | Value | Reason |
|---|---|---|
| Mode | bug | Agree: a valid default-effort tier request receives HTTP 400 without recovery; the reported failure follows the unmatched-error return in `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:803`. |
| Type | skill | Agree: the affected proxy is distributed inside the ccsession-tag skill at `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py`, not the CLI package or an agent definition. |
| Issue type | Bug | Agree: bug in any area maps to Bug under `refs/labels.md`; Bug is available in the scout's issue types. |
| Complexity | Medium | Agree: standard depth maps to Medium; the scout confirms that option exists. |
