## Label A
blocking: no
sentence: The contradiction needs assumptions: that the retry brief repeats the same --output dir, and that 'fresh output directory' in WC-6 cannot mean the directory the coordinator passes for that dispatch. The document never says the retry repeats the directory, so this is a missing requirement (distinct dir per dispatch), not two texts that conflict as written.
evidence: L62 WC-4: contract at '<output-dir>/return-contract.yaml, where <output-dir> is the directory the coordinator passed'; L64 WC-6: 'writes each run into a fresh output directory so a re-run starts clean'; L73 2.3: coordinator's brief states 'the output directory'. No text says a retry reuses the same directory.
confidence: low

## Label B
blocking: no
sentence: WC-4 fixes the contract in the directory the coordinator passed and WC-6 requires each run to use a fresh output directory; these agree when the coordinator passes a new directory on retry, and the document never states what a retry brief passes, so a conflict appears only under an added assumption that the retry repeats the same directory.
evidence: document.md:62 WC-4 '<output-dir>/return-contract.yaml, where <output-dir> is the directory the coordinator passed'; document.md:64 WC-6 'writes each run into a fresh output directory'; document.md:73 section 2.3 says nothing about retry directories.
confidence: low
