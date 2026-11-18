"""GENERATED FILE. Do not edit by hand.

Written by ``scripts/gen_retired_install_data.py --tag v5.0.0 --tag v6.0.0``.
Commands, skills and agents that an earlier release shipped and the current
tree does not, with the sha256 of each file as shipped at that release's tag.
``install_retired_files`` removes an installed copy only when its content has
one of these hashes. Regenerate at release preparation with the previous tag.
"""

# fmt: off
SOURCE_TAGS = ("v5.0.0", "v6.0.0",)

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
    "tdd": ("0714fb66672a5c3d89cbbd367a821286e425cf836e3202c2b229d6ece587538d", "cabb887f673aaaa96c4cea4f75f96da13592c3cb0f24de3fc742d84844e491fd",),
    "validate-roadmap": ("621312a160e28abcab290a44fcdf3b93508e8beff5df0549e5952be1739da5c0",),
}

# agent name (without .md) -> sha256 of the file at the tag(s)
RETIRED_AGENTS = {}

# skill folder -> {path inside the folder: sha256 at the tag(s)}
RETIRED_SKILLS = {
    "operational-guide": {
        "SKILL.md": ("e212e9a8a9d7cecc00deb38f84de83b165aa2f62bf35f8ad7bcc4437b2aaed97", "f6373aec75cc67ae773678f0ec0123506303e2312b9a29c0ce42cc1a51e977cc",),
    },
    "prd": {
        "SKILL.md": ("4805506f78a34187d835110e15f6925f8eeff2dd4495b1fd007d87f998e27c9d", "4e21f14b1ca495a0d7261c9d092439103f923fde9cb8e9e3c2775be89337676c",),
        "refs/agent-prompts.md": ("f2ab63d58fa74ae55ffef10d0b995714e61ced96acda83bbef86f4b8f3d1a54d",),
        "refs/build-request-template.md": ("1f48fa29cde5a8baca1edf156507c809ac4ed9e8549673ae397615a0c0cc3269", "abf3cb2992dc3b6fd6d3df6c62dea2972d3f45f3316473543c70e11ec74e0d1a",),
        "refs/operational-guidance.md": ("bfa8399b268f87fd59bd60f083c776453ddc2d873b97aec32bd38c1cea84c0e1",),
        "refs/synthesis-mapping.md": ("8ff80a1e196a78e8de6ac9377f4107a1c51d1cc870910a90702a704ba441e4f6",),
        "refs/validation-checklists.md": ("865e807cb4a01f3e766147a8338678d2f9225af86a27fabb55169936da33519b",),
    },
    "readme": {
        "SKILL.md": ("7825123de22c3135526aa5806b37de9fe02bcce676eb49626147d5a222aa952a", "efcbcc2e77db2cfaa774fb9df1d34d94b84a22bdbe964a4f8e89dd0369bb4d0e",),
    },
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
    "tdd": {
        "SKILL.md": ("c3e46525f1db5a095bbfca104d8f75c0149ece7d5c30786305358811aeb6cbdc", "e576e4368c61231e51c8325666831350ea2929e0d37dac4145dfba0c38e6cfd6",),
        "refs/agent-prompts.md": ("460dfc585f8e8f147088b3b7d43a27e50d6ed635540a9e80f23f0d94a7a60d84", "81618bde74f074aaa9071ce45be4a8670c32bcd057c90ae91bb67695ce5ec489",),
        "refs/build-request-template.md": ("d5d14a55e14de37f252c65984c07d893ec277a06c41ec068d9f6e40fddd43f72", "d7f7262452f6870cfb86ab8c93ba45bc56a26c8434521ac5006264a27faf68b6",),
        "refs/operational-guidance.md": ("c082e20853df4927b241176e137c560024fb041578372d7fe213af786a4dd087",),
        "refs/synthesis-mapping.md": ("a9668684b8f9a58f0ea35b89839464c8ca37a28b149ef1dea0b4a6ec5f1846b1",),
        "refs/validation-checklists.md": ("b11c7e737d6a4a097f22f20e8bc1197baf48d771cc0474fc819d53875442a53e", "dc932a6573482ab229053ef2296479ae55092ce0b42619dad358ba8af0d0f266",),
    },
    "tech-reference": {
        "SKILL.md": ("0a6f4bb53d548584acd9aef3340b072be4eeb4a6e3996081c779592f353c9b9d", "82bca4bbd3c5215120961225a97d1bfcecfae199ddd1b5d15d04af5cc04f1bfc",),
    },
    "tech-research": {
        "SKILL.md": ("874aec18630faa2a75128d913c8272e85e920bec87c9a813518f093e7e40b113", "9b9ed4dc12d06d2c6be64fae5f8a63e0c3e4bc837f284f6aacad06ed249e25d6",),
    },
}
# fmt: on
