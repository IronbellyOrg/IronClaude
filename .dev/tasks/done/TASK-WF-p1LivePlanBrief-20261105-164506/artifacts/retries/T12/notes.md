5007175a9c567394bc1cef67837aaab5baa8219f
A1 r1-1 F1.1 note ./artifacts/lc11-turn-1.json:6 ac=scope chk=n,n,n,n step 3 says to read worker-read after a wait turn that ends with no message; turn 1 ended with no message and no worker-read output was saved before turn 2, which delivered worker_done (outcome unaffected). The driver now saves a worker-read transcript after every empty turn (from lc12 on).
A1 r1-1 F1.2 note ./artifacts/lc11-step4.txt:3 ac=scope chk=n,n,n,n step 4 file shows a label for the yaml assertion instead of the full command text; the contract satisfies every assertion.
