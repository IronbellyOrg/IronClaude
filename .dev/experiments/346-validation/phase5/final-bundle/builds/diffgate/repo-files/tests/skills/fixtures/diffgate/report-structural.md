# Spec panel critique (diffgate variant)

review: 2 of 3

The panel re-checked R1.1, R1.2 and R1.3 on the surface and raised R2.1, R2.2 and R2.3.

## Findings

1. R2.1 (MAJOR): "missing" is not defined for a null price.
2. R2.2 (MINOR): retention wording.

## Diffgate findings

PRIOR R1.1 resolved by=H2.1
PRIOR R1.2 resolved by=H2.2
PRIOR R1.3 open quote="names the field (R1.3)"
FINDING R2.1 sev=major at=12 hunk=H2.1 anchor="negative or missing with status 400" outcome="a widget sent with price null is stored" :: missing is not defined for null
FINDING R2.2 sev=minor at=19 hunk=H2.2 anchor="kept for thirty days so audits" :: retention wording
