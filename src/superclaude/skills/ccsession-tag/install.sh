#!/bin/bash
# install.sh — wire the ccsession skill into the user's environment.
#
# What this does:
#   1. Copies the skill folder to ~/.claude/skills/ccsession-tag/ (if not
#      already there), so the slash command is discovered in every workspace
#      and the install survives the source folder being deleted/moved.
#   2. Symlinks the shell wrapper into ~/.local/bin/ccsession, and Orca's
#      Claude command into ~/.local/bin/ccsession-orca, pointing at the
#      user-level copy.
#   3. Creates ~/.claude/ccsession.env from the template if it doesn't exist.
#   4. Registers the SessionStart, UserPromptSubmit and SessionEnd hooks in
#      ~/.claude/settings.json (idempotent merge — preserves existing hooks,
#      backs up before writing, safe on invalid JSON).
#
# Re-running is safe — files get refreshed, your env file is left untouched,
# and the hook is only added once.
# After install completes, the source folder you ran this from can be deleted.

set -e

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_SKILL_DIR="$HOME/.claude/skills/ccsession-tag"

echo "Installing ccsession skill"
echo "  source: $SKILL_DIR"
echo "  target: $TARGET_SKILL_DIR"
echo ""

# 1. Copy skill folder to user-level (idempotent)
if [ "$SKILL_DIR" = "$TARGET_SKILL_DIR" ]; then
  echo "[1/4] Source IS the user-level skill folder — skipping copy."
else
  mkdir -p "$(dirname "$TARGET_SKILL_DIR")"
  mkdir -p "$TARGET_SKILL_DIR"
  # Copy contents (incl. dotfiles) into the target; overwrite-on-conflict.
  cp -R "$SKILL_DIR"/. "$TARGET_SKILL_DIR"/
  echo "[1/4] Copied skill folder to: $TARGET_SKILL_DIR"
fi

# Remove the retired, unbuilt Serena context-save plan from older installations.
rm -f "$TARGET_SKILL_DIR/PLAN-context-save-load.md"

# Make sure scripts in the target are executable
chmod +x "$TARGET_SKILL_DIR/ccsession"
chmod +x "$TARGET_SKILL_DIR/ccsession-orca"
chmod +x "$TARGET_SKILL_DIR/hooks/session-start.sh"
chmod +x "$TARGET_SKILL_DIR/hooks/session-name.sh"
chmod +x "$TARGET_SKILL_DIR/install.sh"
echo ""

# 2. Symlink the shell wrapper from PATH → user-level skill copy
BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"
ln -sfn "$TARGET_SKILL_DIR/ccsession" "$BIN_DIR/ccsession"
# Orca's Claude command (Settings > Agents > Claude > Command).
ln -sfn "$TARGET_SKILL_DIR/ccsession-orca" "$BIN_DIR/ccsession-orca"
echo "[2/4] Linked shell wrappers:"
echo "      $BIN_DIR/ccsession -> $TARGET_SKILL_DIR/ccsession"
echo "      $BIN_DIR/ccsession-orca -> $TARGET_SKILL_DIR/ccsession-orca"
# Session names now belong to the repo; copy names saved per folder by older
# versions into their repo's list (copies only, safe to repeat).
"$TARGET_SKILL_DIR/ccsession" --migrate-names 2>/dev/null || true
echo ""

# 3. Env file (user secrets, kept outside the skill folder so it's never
# accidentally distributed)
ENV_TARGET="$HOME/.claude/ccsession.env"
mkdir -p "$(dirname "$ENV_TARGET")"
if [ ! -f "$ENV_TARGET" ]; then
  cp "$TARGET_SKILL_DIR/ccsession.env.example" "$ENV_TARGET"
  chmod 600 "$ENV_TARGET"
  echo "[3/4] Created env file (edit to add your proxy/auth values):"
  echo "      $ENV_TARGET"
else
  echo "[3/4] Env file already exists (leaving untouched):"
  echo "      $ENV_TARGET"
fi
# Save the workspace gateway address (Coder) into an unedited env file.
python3 "$TARGET_SKILL_DIR/seed-env.py" "$ENV_TARGET" "$TARGET_SKILL_DIR/ccsession.env.example" | sed 's/^/      /'
echo ""

# 4. Register the hooks in ~/.claude/settings.json (idempotent): SessionStart
# saves a session's name; UserPromptSubmit and SessionEnd pick up /rename.
HOOKS_DIR="$TARGET_SKILL_DIR/hooks"
SETTINGS="$HOME/.claude/settings.json"
echo "[4/4] Registering SessionStart, UserPromptSubmit and SessionEnd hooks:"
echo "      Scripts:  $HOOKS_DIR"
echo "      Settings: $SETTINGS"

python3 - "$SETTINGS" "$HOOKS_DIR" <<'PYEOF'
import json, os, sys, shutil

settings_path, hooks_dir = sys.argv[1], sys.argv[2]
# (event, matcher or None, script)
wanted = [
    ("SessionStart", "startup|resume", "session-start.sh"),
    ("UserPromptSubmit", None, "session-name.sh"),
    ("SessionEnd", None, "session-name.sh"),
]


def registration(matcher, script):
    reg = {"hooks": [{"type": "command",
                      "command": 'bash "%s/%s"' % (hooks_dir, script), "timeout": 5}]}
    if matcher:
        reg = {"matcher": matcher, **reg}
    return reg


# Load existing settings, or start fresh if absent.
data = {}
if os.path.exists(settings_path):
    try:
        with open(settings_path) as f:
            data = json.load(f)
    except Exception:
        print("      WARNING: settings.json is not valid JSON — leaving it untouched.")
        for event, matcher, script in wanted:
            print("      Add this manually under hooks.%s:" % event)
            print("        %s" % json.dumps(registration(matcher, script)))
        sys.exit(0)

if not isinstance(data, dict):
    print("      WARNING: settings.json top-level is not a JSON object — leaving untouched.")
    sys.exit(0)

hooks = data.setdefault("hooks", {})
if not isinstance(hooks, dict):
    print("      WARNING: settings.json 'hooks' is not an object — leaving untouched.")
    sys.exit(0)

added = []
for event, matcher, script in wanted:
    groups = hooks.setdefault(event, [])
    if not isinstance(groups, list):
        print("      WARNING: settings.json 'hooks.%s' is not a list — leaving it untouched." % event)
        continue
    # Match only our native or standalone command, not a user hook mentioning the path.
    path = "%s/%s" % (hooks_dir, script)
    ours = ('bash "%s"' % path, "bash '%s'" % path,
            "~/.claude/skills/ccsession-tag/hooks/%s" % script)
    if any(isinstance(h, dict) and h.get("command") in ours
           for group in groups if isinstance(group, dict)
           for h in group.get("hooks", []) if isinstance(group.get("hooks"), list)):
        continue
    groups.append(registration(matcher, script))
    added.append(event)

if not added:
    print("      Already registered — no change.")
    sys.exit(0)

# Back up an existing file before modifying it.
if os.path.exists(settings_path):
    shutil.copy2(settings_path, settings_path + ".bak")
    print("      Backed up existing settings to settings.json.bak")

os.makedirs(os.path.dirname(settings_path), exist_ok=True)
with open(settings_path, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")
print("      Registered %s hook%s." % (", ".join(added), "s" if len(added) > 1 else ""))
PYEOF
echo ""
echo "Install complete. The source folder ($SKILL_DIR)"
echo "can now be deleted — everything self-contained under ~/.claude/ and ~/.local/bin/."
echo ""
echo "Test with:"
echo "  ccsession --list"
echo "  ccsession --help"
