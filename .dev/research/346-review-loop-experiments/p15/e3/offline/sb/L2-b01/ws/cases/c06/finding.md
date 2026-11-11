### F15. Medium. Section 1.4 item 2 states an unsupported fact
- Expert: Nygard.
- Evidence: SPEC:44 says a command's own `AskUserQuestion` "comes after readiness, so it does not fail `worker-start`". For Claude the task is passed on the command line (CAPS:47) and CAPS:53 says no interactive question may appear before the agent input is ready. Whether the first question of a command (for example the cli-eval suite menu, INV-A:44) lands before or after readiness is not in the evidence. WC-2 removes the gates anyway.
- Recommendation: mark the sentence UNVERIFIED and add it to the UNVERIFIED list (SPEC:271-285).
- Priority: Medium.
