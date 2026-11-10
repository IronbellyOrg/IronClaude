### R1-1 Excess requests are held without telling the client
The excess request rule holds requests above the limit and answers them later, so the client gets no signal that it exceeded its limit. Cited: spec lines 19-20 (before version).
An implementer who follows RL-5 builds a server that holds excess requests without a rejection, so clients cannot back off.
Protected requirement: line 19 (the per-minute limit must hold).
