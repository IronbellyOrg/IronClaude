## Label A
blocking: no
sentence: The finding itself says the sentence needs a guess about which reading wins (specific row over general rule for adversarial and workflow). The missing-directory case is a requirement the document never states.
evidence: document.md:62 WC-4 '<output-dir>/return-contract.yaml'; :83 adversarial '<output>/adversarial/return-contract.yaml'; :92 workflow '.dev/tasks/to-do/<id>/return-contract.yaml'; :87,:90 '--output <file>'
confidence: low

## Label B
blocking: no
sentence: The sentence needs a guess. For tdd and init-lite, <output-dir> is undefined because the flag is file-valued, and the missing-directory case is a requirement the document never states. For adversarial and workflow the reader must guess whether the specific row overrides WC-4.
evidence: L62: 'where <output-dir> is the directory the coordinator passed (--output / --output-dir)'; L87: 'init-lite ... --output <file>'; L90: 'tdd ... --output <file>'; L83: '<output>/adversarial/return-contract.yaml'; L92: '.dev/tasks/to-do/<id>/return-contract.yaml'.
confidence: high
