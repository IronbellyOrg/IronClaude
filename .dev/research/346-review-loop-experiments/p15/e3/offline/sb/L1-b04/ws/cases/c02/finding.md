**F-2 [BLOCKING] AC-0.4 step 3 cannot pass in P0.**
- Experts: Crispin (lead), Adzic.
- Text: `SPEC:194` says "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1." The pass condition of step 3 (`SPEC:182`) requires "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path." Both need the P1 contract. The exemption in `SPEC:194` names only step 4.
- Grading sentence: an implementer who runs AC-0.4 as written finds that step 3 has no contract status and no WC-4 path to check in P0, so step 3 cannot pass and the P0 gate cannot close.
- Recommendation: give step 3 a P0 variant that compares the outcome with the command's own report and checks the path of the file the command wrote.
- Priority: High.
