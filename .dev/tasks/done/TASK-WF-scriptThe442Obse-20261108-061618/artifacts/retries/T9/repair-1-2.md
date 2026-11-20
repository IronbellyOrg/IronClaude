a4bb361e1c6375fe1dedddd00ccf6192329f8a51

# repair-1-2.md (second repair round after the failing review r1-3)

family runbook-overclaim, one file: .dev/issues/442/observation-runbook.md (plus two cases in runbook-selftest.sh).
search command: sed -n "/^## 6\. Scripted path/,/^## Appendix/p" observation-runbook.md and the 4.2 bullets, read for every universal or absolute statement about what the scripts do (every, each, never, all, only, always).
hits before: the strict-mode and timeout sentence, the scratch sentence, the stub list in the tests sentence, the PENDING sentence, the evidence copy row ("after a secret scan"), the O-10 sentence.
after: the strict-mode/timeout/scratch sentence is replaced by "Their working state, logs and screens are under /tmp/ob (override with OB)"; the tests sentence says "stub commands in temporary directories and do not start a live session"; the PENDING sentence says the script stopped without recording that step, the line gives the reason, some name a screen file; the evidence row says copies only when a secret scan finds nothing; the O-10 sentence names the branch condition; the NEEDS_INPUT bullet names the scripts that print it as PENDING and setup-github.sh.
applied tree=121c5424c729cf6ef676ba86d228ecdf10e74ccb
