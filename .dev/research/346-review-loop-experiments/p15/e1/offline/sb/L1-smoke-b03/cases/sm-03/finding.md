### R1-1 Purchase follow-ups ignore the opt-out
The purchase follow-up rule keeps sending marketing notifications to opted-out customers. It contradicts the opt-out rule, which says an opted-out customer receives none. Cited: spec lines 17, 19 (before version).
An implementer who follows NO-4 builds a sender that emails opted-out customers about their recent purchases.
Protected requirement: line 17 (the opt-out must hold).
