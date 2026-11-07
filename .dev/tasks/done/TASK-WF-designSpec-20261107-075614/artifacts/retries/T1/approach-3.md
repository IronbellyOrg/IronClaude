69f360d58d89456f559ad3de21ea75027cd72bb0
Implementer claims (not evidence):
- Rebuilt ./artifacts/pre-build-gate.md around the accepted base record, gate table, O1, O2, O4; replaced the hand-written O3 list with the output of ./artifacts/o3-pin-scan.py, pasted unedited between markers.
- Believed the scan complete by construction because it starts from the pr-submit file text and finds every test that reads it.
- The scan hides two things: path-like literals are filtered out, and rules held in helper asserts show only as test names or assert messages.
