### R1-1 Cleanup deletes the delivery log at once
The cleanup section says that all delivery-log rows are deleted immediately when a delivery reaches the delivered state. The delivery log requirement keeps rows for 30 days. Cited: spec lines 17, 39 (before version).
An implementer who follows the cleanup section builds a worker that erases the delivery log of every delivered webhook at once, so customers can no longer see their deliveries.
Protected requirement: line 17 (the 30-day log retention must hold).
