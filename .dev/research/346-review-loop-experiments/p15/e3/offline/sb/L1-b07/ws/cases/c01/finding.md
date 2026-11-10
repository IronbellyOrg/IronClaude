### F6. Medium. The `/sc:index` row tells the implementer to document a claim the inventory marks UNVERIFIED
- Expert: Wiegers.
- Evidence: SPEC:111 ("state that knowledge-base mode does not wait (whether it does is UNVERIFIED)"); INV-A:54 and INV-A:113 (the file does not say). Writing the statement without checking it can leave a command that claims not to wait and does.
- Recommendation: make the row "check whether it waits; if so, refuse the mode under `--unattended`" (same pattern as business-panel, SPEC:102).
- Priority: Medium.
