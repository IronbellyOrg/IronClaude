### R1-1 Retry details allow 8 retries
The retry details section allows up to 8 retries with exponential backoff. The retry policy requirement allows at most 5 retries. Cited: spec lines 24, 55 (before version).
An implementer who follows the retry details builds a worker that retries up to 8 times and so exceeds the 5 retries the retry policy allows.
Protected requirement: line 24 (the retry policy cap must hold).
