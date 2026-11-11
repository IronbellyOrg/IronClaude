### R1-1 Reset links live too long
An earlier version let the reset link live for days. The lifetime rule is meant to keep the link short-lived. Cited: spec lines 17-18 (before version).
An implementer who follows PR-4 builds reset links that stay valid for days.
Protected requirement: line 17 (one-time use must hold).
