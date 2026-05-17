# PROTECTED-list Audit

| PROTECTED Entry | Filesystem Status | Action |
|-----------------|-------------------|--------|
| README.md | EXISTS | KEEP |
| README-ja.md | ABSENT | REMOVE |
| README-zh.md | ABSENT | REMOVE |
| BACKUP_GUIDE.md | ABSENT | REMOVE |
| MIGRATION_GUIDE.md | ABSENT | REMOVE |
| SECURITY.md | EXISTS | KEEP |
| CLAUDE.md | EXISTS | KEEP |
| LICENSE | EXISTS | KEEP |
| .gitignore | EXISTS | KEEP |
| .claude-plugin/marketplace.json | ABSENT | REMOVE |
| core/ | ABSENT | REMOVE |
| modes/ | ABSENT | REMOVE |

## REMOVE list (entries to drop from the PROTECTED array)
- `README-ja.md`
- `README-zh.md`
- `BACKUP_GUIDE.md`
- `MIGRATION_GUIDE.md`
- `.claude-plugin/marketplace.json`
- `core/`
- `modes/`

## KEEP list (entries to preserve)
- `README.md`
- `SECURITY.md`
- `CLAUDE.md`
- `LICENSE`
- `.gitignore`

Significantly broader audit than research-notes anticipated: 7 entries marked REMOVE (research notes called out only 3).
