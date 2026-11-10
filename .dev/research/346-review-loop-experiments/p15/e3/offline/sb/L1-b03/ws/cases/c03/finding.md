**M4. The D1 example uses an `--output` flag that no inventory evidences for troubleshoot.** Expert: Cockburn (worked examples).
- D1 example: `/sc:troubleshoot "login fails" --unattended --output .dev/troubleshoot/login/` (SPEC:228).
- The troubleshoot row in section 3.1 lists "no `--fix`" as its only brief flag (SPEC:91). INV-B:242 names only the default output directory (`.dev/troubleshoot/<slug>-<timestamp>/`) and no output flag.
- Recommendation: drop `--output` from the example, or cite the flag.
- Priority: Medium.
