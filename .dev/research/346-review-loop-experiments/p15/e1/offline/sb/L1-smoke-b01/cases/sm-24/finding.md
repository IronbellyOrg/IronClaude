### R1-1 The nightly job never looks for duplicate numbers
The duplicate check rule says the job does not look for duplicate invoice numbers, although the gap check next to it relies on the numbers being trustworthy. Cited: spec lines 33-34 (before version).
An implementer who follows IN-5 builds a reconciliation job that never reports two invoices with the same number.
Protected requirement: line 33 (the gap check must hold).
