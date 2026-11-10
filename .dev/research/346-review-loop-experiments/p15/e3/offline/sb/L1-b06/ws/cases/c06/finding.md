### M-8 No parsing rule for the `--unattended` token

- Severity label MINOR to MAJOR, graded Medium. Experts: Whittaker. Priority: Low. Impact: Clarity.
- Issue. D1 says the flag "cannot misfire on a person" (SPEC:228). A quoted topic containing the token (for example `/sc:research "what does --unattended do"`) is a sentinel collision (GC-3 row 5), and the spec never says the token counts only as a standalone argument outside quotes.
- Recommendation. Define the token match in the contract.
