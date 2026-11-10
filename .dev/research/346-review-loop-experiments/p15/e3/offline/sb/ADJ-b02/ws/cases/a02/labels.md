## Label A
blocking: no
sentence: An implementer who follows AC-0.4 as written runs the three P0 smoke runs and finds step 3 asks for the WC-4 contract path that P0 cannot produce for troubleshoot, which is wrong because it gives a false P0 failure. The finding itself says this needs the guess that the step-4 carve-out was not meant to cover step 3. The document states the intent that the worker reports the named file until P1, so the worse reading is a guess.
evidence: L194 AC-0.4: 'steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1'; L182 step 3: 'its report path is the WC-4 contract path'; L91 troubleshoot report is REPORT.md; 3.1 intro: 'the worker reports the named file until Phase 1 adds the contract'.
confidence: low

## Label B
blocking: yes
sentence: An implementer who follows the text as written runs the P0 smoke runs and finds AC-0.4 step 3 unsatisfiable: step 3 requires the report path to be the WC-4 contract path, line 194 says the contract arrives only in P1 and that only step 4 uses the existing report file, and line 91 gives troubleshoot's report as REPORT.md; so the acceptance criterion 'steps 1-3 and 5-7 pass' cannot pass for troubleshoot, which is wrong because it forces a false P0 failure that 'reopens section 1'.
evidence: document.md:182 'its report path is the WC-4 contract path'; document.md:194 'steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1'; document.md:62 WC-4 contract; document.md:91 troubleshoot 'REPORT.md (report_path)'; document.md:158 P0 runs troubleshoot.
confidence: low
