PAIRS = [
 ('On every coordinator wake, at most once every 5 minutes (the cadence of "The sweep." under `### Liveness supervision`), the coordinator runs `/sc:sweep` and reads its report before it acts. It keeps a periodic sweep scheduled while work remains.',
  'On every coordinator wake, the coordinator runs `/sc:sweep` and reads its report before it acts. It sweeps on every wake and keeps a periodic sweep scheduled while work remains.'),
 ('**Final text.** The SPEC section 10 text (lines 404-408) with three changes, all deviation D6: the heading is renumbered WC-16 (R4); the cadence clause of contract line 110 is added and "It sweeps on every wake" is dropped, because master already bounds the sweep to at most once every 5 minutes (R4); and one sentence is appended at the end (SP-27). WC-16 does not reword contract line 110 (the sweep) or line 151 (the L1 probe row):',
  '**Final text.** The SPEC section 10 text (lines 404-408), unchanged, with one sentence appended at the end (SP-27, deviation D6):'),
 ('| The same text renumbered WC-16, with master\'s cadence "at most once every 5 minutes" (contract line 110) in place of "It sweeps on every wake", and with one sentence appended: the coordinator records',
  '| The same text with one sentence appended: the coordinator records'),
]
