### R1-1 Backups are overwritten every night
The overwrite rule replaces each backup with the next one, which contradicts the retention rule that keeps nightly backups for 35 days. Cited: spec lines 32-33 (before version).
An implementer who follows BK-4 builds a backup job that keeps a single copy, so an error that is found after one day cannot be restored.
Protected requirement: line 32 (the 35-day retention must hold).
