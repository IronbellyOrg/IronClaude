# Spec panel critique

review: 3 of 3

Re-review of surface-r3.md.

## Diffgate findings

PRIOR R2.1 resolved by=H3.1
PRIOR R2.2 resolved by=H3.2
PRIOR R2.3 resolved by=H3.3
PRIOR R2.4 resolved by=H3.4
FINDING R3.1 sev=critical at=5 hunk=H3.1 anchor="refused before launch" :: launch is not a defined step
FINDING R3.2 sev=major at=9 hunk=H3.2 anchor="escalated to the person who owns" outcome="nobody owns an unattended run" :: owner undefined
FINDING R3.3 sev=major at=13 hunk=H3.3 anchor="rejected by worker_done with exit 2" outcome="exit 2 collides with the usage error" :: exit code clash
FINDING R3.4 sev=critical at=17 hunk=H3.4 anchor="kept under its own attempt number" :: numbering source undefined
FINDING R3.5 sev=major at=5 hunk=H3.1 anchor="without a report path is refused" outcome="-" :: wording overlaps R3.1
