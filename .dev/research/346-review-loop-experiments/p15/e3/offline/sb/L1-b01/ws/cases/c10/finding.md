### M-14 Load: the P1 checks cannot be met as the row is written

- Severity label MINOR, graded Medium. Experts: Wiegers, Crispin. Priority: Low. Impact: Consistency.
- Issue. The load row says no report, no resume, use it inside another worker's brief, fix only the usage line (SPEC:112; SPEC:265 "a report file would be an unrequested addition"), and P1 lists "load (usage line only)" (SPEC:159). AC-1.1 requires a section naming `return-contract.yaml` in every 3.1/3.2 command (SPEC:195) and AC-1.2 runs the full live check, including `test -s <contract>`, on each P1 command (SPEC:196). §3's preamble also says every changed command gains the section (SPEC:76).
- Grading. Whether load counts as a "P1 command" for AC-1.2 needs a guess: Medium.
- Recommendation. Exclude load from AC-1.1/AC-1.2 explicitly, or give it a contract.
