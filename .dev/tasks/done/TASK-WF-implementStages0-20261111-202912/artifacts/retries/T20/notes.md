ffc4ebc55616255cbba86f7c773dbc71e1f378ca
A1 r1-1 F1.1 minor scripts/reflect_shadow_exit.py:191 ac=scope n,n,n,n a shadow run with a manifest.json that does not parse is not counted, not listed and not failed; it is also left out of the legacy baseline
A1 r1-1 F1.2 minor scripts/reflect_shadow_exit.py:363 ac=scope n,n,n,n --required 0 prints OVERALL PASS (shadow runs 0 of 0) and exits 0; no lower bound check
A1 r1-1 F1.3 minor scripts/reflect_shadow_exit.py:186 ac=scope n,n,n,n parity maps model ids to classes with whichever tier file is found at aggregation time, not the one the run used (tiers_sha256 is not checked); gateway aliases in the legacy reviewer_models are not mapped
