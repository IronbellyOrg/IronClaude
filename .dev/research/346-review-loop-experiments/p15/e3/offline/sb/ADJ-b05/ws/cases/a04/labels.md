## Label A
blocking: yes
sentence: An implementer who follows the stated text as written builds a restore that overwrites the production database after one click, with no other check, and that is wrong because a misclick destroys all writes made since the selected backup (data loss). R13 confirms no other check exists.
evidence: L23 R12: 'A restore overwrites the production database with the selected backup after one confirmation click.'; L24 R13: 'The confirmation click is the only check before a restore starts.'
confidence: low

## Label B
blocking: yes
sentence: An implementer who follows R12 and R13 as written builds a restore that overwrites the production database with the selected backup after one confirmation click, with that click as the only check; this is wrong because the stated text itself causes data loss, since every write made after the selected backup is destroyed.
evidence: document.md:23 R12 'A restore overwrites the production database with the selected backup after one confirmation click.'; document.md:24 R13 'The confirmation click is the only check before a restore starts.'
confidence: medium
