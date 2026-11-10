**M6. AC-7.2 step 2 passes when Orca never looked.** Expert: Adzic (acceptance rule).
- Pass rule: `observation.agentWait` "is never non-null" (SPEC:181). CAPS:129 quotes `worker-show`: "Null means Orca looked and found no wait. An absent field means it never looked."
- An absent field satisfies "never non-null", so a run that Orca never observed passes the stall check. The check then cannot detect the stall it exists to catch.
- Recommendation: require `agentWait` to be present and null on each poll; treat absent as a fail.
- Priority: Medium.
