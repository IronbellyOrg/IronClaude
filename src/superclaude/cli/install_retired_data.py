"""GENERATED FILE. Do not edit by hand.

Written by ``scripts/gen_retired_install_data.py --tag v5.0.0``.
Commands, skills and agents that an earlier release shipped and the current
tree does not, with the sha256 of each file as shipped at that release's tag.
``install_retired_files`` removes an installed copy only when its content has
one of these hashes. Regenerate at release preparation with the previous tag.
"""

# fmt: off
SOURCE_TAGS = ("v5.0.0",)

# command name (without .md) -> sha256 of the file at the tag(s)
RETIRED_COMMANDS = {
    "build": ("10f986e1b8a0a5af1d597648786ae6c6cd3015b70b97e0ae78959be71a205f9a",),
    "cli-portify": ("48ffb39f20bc3574599f08f9efef74ee1e93293567a5c486d9f610421ad8b511",),
    "improve": ("1fe731f23535f00fcfca3fc3be2b968d3e0b4ed51da4a7cb7ae94389b9b5eb2d",),
    "index": ("5216061c2689ad8a08fe65e891c7dfd4be3ae807f5c0a845b8d8d8f927b804b3",),
    "index-repo": ("71562b60b41fbdd422f3a7d0458344ebedd46538e88f2535a02815b6327cf68d",),
    "load": ("83d32d7d3ef8f6e7f3573e8234f0b6b919ec813ae4053a8ce99e3eda384aae66",),
    "review-translation": ("ccfe5a2445465f308e19680e85e007395881f0dd3f1b2d4e975e6199fb313af8",),
    "roadmap": ("709622e169f864d15b77e855039087ae9346b46cce0f457b8f24f48b697d3a21",),
    "save": ("e3f8d4388f7d2f634557907bea6cd1c3b43f687e04bebae4d3ed3e48b8054bab",),
    "spawn": ("962c37cefe6c25d34e441a3ce0b26d725930d4b61438bd6375b3b8869561c1c7",),
    "tasklist": ("a4ca4273dd0e4859afe1137b7aefc8c2267808cf888974ed19f1a8a23eefce4d",),
    "validate-roadmap": ("621312a160e28abcab290a44fcdf3b93508e8beff5df0549e5952be1739da5c0",),
}

# agent name (without .md) -> sha256 of the file at the tag(s)
RETIRED_AGENTS = {}

# skill folder -> {path inside the folder: sha256 at the tag(s)}
RETIRED_SKILLS = {
    "sc-cli-portify-protocol": {
        "SKILL.md": ("bfd11d2c28bca5f22c6c09db04dc7af3a272e6921988f7b3c861937f689f9530",),
        "__init__.py": ("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",),
        "decisions.yaml": ("0d30d9722e281c5cc0eb868b880b9a0208976d301bae425f77677c35b0c30e00",),
        "refs/analysis-protocol.md": ("871e873f4981acb4593bc77e6b4753da0f88e8646fe16f91b807b6cb1d23b523",),
        "refs/code-templates.md": ("2e35bafdb315ee4b31b572eff8a898630009e303492d68450ef52f2c22da433b",),
        "refs/pipeline-spec.md": ("72e7c88b34f8b50a7bee921425fcac1a9612e4c48b2d2572d6fe5b99f7e197e9",),
    },
    "sc-review-translation-protocol": {
        "SKILL.md": ("61d14687bd884ad540fe33087082b3d79b3711977a51d0466030dac6559d43e2",),
    },
    "sc-roadmap-protocol": {
        "SKILL.md": ("d1659e9936d50252a0b9481498f0db71248b561ffc11df571ddfe96833622b73",),
        "__init__.py": ("ddf24d4b8d613798d7c9b4a618052cc8a2eaa817d6ee81d7bd104ede9c9df811",),
        "refs/adversarial-integration.md": ("d929977d5307809259451d0b0d91b61ee8a70dc944997cd4c047684340a06440",),
        "refs/extraction-pipeline.md": ("3880bfa1a06ce85777965af54125796e39db05cd6ded0843444de6a71e0943b7",),
        "refs/scoring.md": ("91d55da62844cec0bc91107d44d8f0355e25074fa2663422ea15ec3db41880fa",),
        "refs/templates.md": ("19f7b7cba97766cfed48e009f5ca37451e7d506c3e6552767fc7401ed9ea56d0",),
        "refs/validation.md": ("d242142ef9e2abed42015ce1788ebc9ecdf63823a2e5f631d9c70d9deb584037",),
    },
    "sc-tasklist-protocol": {
        "SKILL.md": ("54dee4bf537c1ef55f945dc27420916faa7edf0a741b8ee7f9a1dffd209faeff",),
        "__init__.py": ("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",),
        "rules/file-emission-rules.md": ("e2f0e766575d47bce5919541282b1dc487033549d2f958f6d5b0e7533a87c81c",),
        "rules/tier-classification.md": ("97fe5b80eb29226ca6ce91a50e73a984685637a51b99fd036539140162a600ab",),
        "templates/index-template.md": ("54afb7f565904a76a69e293f38d143f2b5d96faedc80da024d8f54ba602cd5e4",),
        "templates/phase-template.md": ("4d1a5a037c6b7f31fb41ac5e838a0441b8a5562147e810182c9fd23058192be2",),
    },
    "sc-validate-roadmap-protocol": {
        "SKILL.md": ("b423ad2a8da9480e6fb459b5ef518e1fc086b1ddf70f17da69eefcd273d155de",),
    },
}
# fmt: on
