review: 1 of 3

Two defects in the archive section. Both quotes are copied whole from the candidate, so they run past 200 characters.

## Findings block

```findings-v1
{"id": "F1", "severity": "CRITICAL", "blocking": true, "category": "contradiction", "anchor": "The nightly archive job copies every closed ticket older than ninety days into cold storage, verifies every copy against the stored checksum, and only then removes the original row from the live table, so a failed copy leaves the ticket where it was.", "refs": [], "claim": "the removal rule contradicts the retention limit stated in the summary section"}
{"id": "F2", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "Each archive run writes one summary file per night.", "anchor2": "A ticket stays visible in the live table until its copy has passed the checksum test, and the job never deletes a row whose copy failed, whatever the age of the ticket is, and it writes the failure into the nightly summary that the support lead reads at nine.", "refs": [], "claim": "the summary rule and the failure rule name different readers"}
```
