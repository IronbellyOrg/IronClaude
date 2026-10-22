# shellcheck shell=bash
# shellcheck disable=SC1090,SC1091
# =============================================================================
# /etc/skel/.bashrc  —  VSCode-AIDev02 template-shipped interactive bash rc
# T02.11 / D-0026 / R-026  —  RAD-6 five-section guarded layout
# -----------------------------------------------------------------------------
# Source of truth: templates/VSCode-AIDev02/workspace_defaults/.bashrc.
# COPY-installed at /etc/skel/.bashrc (0644 root:root); adduser copies it into
# each new user's $HOME at UID-1000 ownership. The template NEVER writes env
# vars here (FR18) — user overrides live in ~/.bashrc.local (FR23, T02.13).
#
# RAD-6 mandates exactly five sections, in this order, each delimited by an
# open/close guard-marker pair of the form (hash)(angles) aidev02:NAME
# (angles). The open markers are grep-asserted (test-7 startup-order gate);
# the count of open markers must be exactly five:
#   1. interactive-guard   non-interactive shells return early
#   2. osh-init            oh-my-bash bootstrap (FR22 theme + FR24 plugin floor)
#   3. env-block           design-tokens.sh -> .aienv -> .env (FR14/FR15 order)
#   4. fr24-hooks          FR24 history-search + extract(); starship/zoxide/fzf
#   5. bashrc-local        sources ~/.bashrc.local last (FR23, T02.13)
#
# Functional-line budget (per T02.11 deliverable): 6 lines —
#   3 sourcing  : design-tokens.sh, .aienv, .env            (env-block)
#   3 init      : starship, zoxide, fzf                      (fr24-hooks)
# The FR24 readline binds + extract() and the oh-my-bash loader are section
# scaffolding for their named requirements, not part of the 6-line budget.
# =============================================================================

# >>> aidev02:interactive-guard >>>
# Do nothing in non-interactive shells (scp/rsync/cron correctness).
case $- in
  *i*) ;;
  *) return ;;
esac
# <<< aidev02:interactive-guard <<<

# >>> aidev02:osh-init >>>
# oh-my-bash bootstrap. Tree ships read-only via /etc/skel/.oh-my-bash
# (T01.18, pinned SHA). FR22: default "font" theme. FR24 plugin floor:
# only upstream-present plugins are loaded here; the two non-upstream
# plugins (history-search-multi-word, extract) are substituted in
# aidev02:fr24-hooks per D-CL01.17.
export OSH="${HOME}/.oh-my-bash"
# These four are read by oh-my-bash.sh after it is sourced below; shellcheck
# cannot see that cross-file use, so SC2034 (unused) is suppressed here.
# shellcheck disable=SC2034
OSH_THEME="font"
# shellcheck disable=SC2034
completions=(git ssh)
# shellcheck disable=SC2034
aliases=(general)
# shellcheck disable=SC2034
plugins=(git bashmarks sudo)
[ -r "${OSH}/oh-my-bash.sh" ] && . "${OSH}/oh-my-bash.sh"
# T5 no-shadow contract (UX-spec T5 / .github/contract-tests/test-5-no-shadow.sh).
# oh-my-bash registers a lazy-init alias `ls=_omb_util_alias_init_ls` via
# `_omb_util_alias_delayed` (lib/utils.sh:515-524 at the pinned SHA), and the
# system-default /etc/bash.bashrc sets the Debian `alias grep='grep
# --color=auto --exclude-dir={.bzr,CVS,.git,.hg,.svn}'`. Both shadow the
# /usr/bin binaries and fail `type ls` / `type grep` resolution. Strip both
# after omb finishes loading so resolution falls through to PATH lookup.
# Kept inside the `aidev02:osh-init` section to preserve the RAD-6 five-section
# guard count enforced by test-7-startup-order (no new section added).
unalias ls 2>/dev/null || true
unalias grep 2>/dev/null || true
# <<< aidev02:osh-init <<<

# >>> aidev02:env-block >>>
# Shared FR14/FR15 loader: design tokens -> .aienv -> .env (user wins).
. /usr/local/lib/aidev/shell-env.sh
# ~/.env is optional now (the gateway key arrives as LITELLM_API_KEY); warn
# only when neither it nor a gateway key is there, i.e. AI tools cannot work.
if [ -z "${_AIDEV_WARNED_MISSING_ENV:-}" ] && [ ! -r "${HOME}/.env" ] \
  && [ -z "${LITELLM_API_KEY:-}${ANTHROPIC_API_KEY:-}${ANTHROPIC_AUTH_TOKEN:-}" ]; then
  printf 'WARN: no gateway key and no ~/.env: create it with coder secret create aienv --file ~/.env < .env  (then restart the workspace)\n' >&2
  _AIDEV_WARNED_MISSING_ENV=1
fi
export STARSHIP_CONFIG="${STARSHIP_CONFIG:-/etc/starship/starship.toml}"
export PATH="${HOME}/.local/bin:${HOME}/bin:${PATH}"
export AIDEV_HEARTBEAT_URL="${AIDEV_HEARTBEAT_URL:-}"
umask 022
ulimit -n 4096 2>/dev/null || true
NVM_DIR="/opt/nvm"
[ -s "${NVM_DIR}/nvm.sh" ] && . "${NVM_DIR}/nvm.sh"
[ -s "${NVM_DIR}/bash_completion" ] && . "${NVM_DIR}/bash_completion"
alias serena='uvx --from "git+https://github.com/oraios/serena" serena'
claude-code() {
  if [ -n "${ZELLIJ:-}" ]; then
    trap 'zellij action rename-pane --pane-id "${ZELLIJ_PANE_ID}" "$(basename "$PWD")" 2>/dev/null' EXIT
    zellij action rename-pane --pane-id "${ZELLIJ_PANE_ID}" "claude · $(basename "$PWD")" 2>/dev/null
  fi
  exec command claude "$@"
}
_aidev_record_sourced_version() {
  local version="${1:-unknown}" sha="${2:-}"
  local state_dir="${HOME}/.local/state/aidev"
  local log="${state_dir}/sourced-history.log"
  local ts boot boot8 prev chain hash tier entry probe _a _b _c _d _e _f _g
  TZ=UTC printf -v ts '%(%Y-%m-%dT%H:%M:%SZ)T' -1 2>/dev/null || ts="unknown"
  boot="unknown"
  [ -r /proc/sys/kernel/random/boot_id ] && read -r boot < /proc/sys/kernel/random/boot_id 2>/dev/null || true
  boot8="${boot:0:8}"
  mkdir -p "${state_dir}" 2>/dev/null || { AIDEV_STATE_LOG_TIER="C"; return 0; }
  if command -v flock >/dev/null 2>&1 && [ -w "${state_dir}" ]; then
    { exec 9>"${state_dir}/.sourced-history.lock"; } 2>/dev/null && flock -w 5 9 2>/dev/null || true
  fi
  prev="genesis"
  if [ -r "${log}" ]; then
    while IFS='	' read -r _a _b _c _d _e _f _g || [ -n "${_g}" ]; do
      [ -n "${_g}" ] && prev="${_g}"
    done < "${log}"
    [ -n "${prev}" ] || prev="genesis"
  fi
  tier="B"
  if command -v chattr >/dev/null 2>&1; then
    [ -e "${log}" ] || : > "${log}" 2>/dev/null || true
    if chattr +a "${log}" 2>/dev/null; then
      probe="${state_dir}/.ao-probe.$$"
      : > "${probe}" 2>/dev/null || true
      if chattr +a "${probe}" 2>/dev/null; then
        if : > "${probe}" 2>/dev/null; then
          tier="B"
          chattr -a "${log}" 2>/dev/null || true
        else
          tier="A"
        fi
        chattr -a "${probe}" 2>/dev/null || true
      else
        tier="B"
        chattr -a "${log}" 2>/dev/null || true
      fi
      rm -f "${probe}" 2>/dev/null || true
    fi
  fi
  chain="${prev}|${ts}|${version}|${sha:0:12}|$$|${tier}|${boot8}"
  hash="genesis"
  if command -v sha256sum >/dev/null 2>&1; then
    read -r hash _ < <(printf '%s' "${chain}" | sha256sum) 2>/dev/null || hash="genesis"
  fi
  entry="${ts}	${version}	${sha:0:12}	$$	${tier}	${boot8}	${hash}"
  if ! printf '%s\n' "${entry}" >> "${log}" 2>/dev/null; then
    tier="C"
    if [ -z "${_AIDEV_WARNED_STATELOG:-}" ]; then
      printf 'WARN: aidev state-log append failed: %s\n' "${log}" >&2
      _AIDEV_WARNED_STATELOG=1
    fi
  fi
  { exec 9>&-; } 2>/dev/null || true
  AIDEV_STATE_LOG_TIER="${tier}"
  return 0
}
_aidev_check_and_record_central_version() {
  local dir version_file sha_file current_version current_sha
  local log prev_seen _a version_col _rest
  dir="${AIDEV_AI_DEFAULTS_PATH:-/etc/aidev02/aienv.d/defaults.sh}"; dir="${dir%/*}"
  version_file="${dir}/VERSION"
  sha_file="${dir}/defaults.sha256"
  [ -r "${version_file}" ] || return 0
  read -r current_version < "${version_file}" 2>/dev/null || return 0
  [ -n "${current_version}" ] || return 0
  current_sha=""
  [ -r "${sha_file}" ] && read -r current_sha _ < "${sha_file}" 2>/dev/null || true
  log="${HOME}/.local/state/aidev/sourced-history.log"
  prev_seen=""
  if [ -r "${log}" ]; then
    while IFS='	' read -r _a version_col _rest || [ -n "${_a}" ]; do
      [ -n "${version_col:-}" ] && prev_seen="${version_col}"
    done < "${log}"
  fi
  _aidev_record_sourced_version "${current_version}" "${current_sha}"
  if [ -n "${prev_seen}" ] && [ "${prev_seen}" != "${current_version}" ] \
      && [ ! -e "${HOME}/.local/state/aidev/skip-update-notice" ]; then
    printf '%bAI env updated: version %s (run `refresh-env --changelog` for details)%b\n' \
      "${ANSI_FG_DEFAULT-}" "${current_version}" "${ANSI_RESET-}"
  fi
  return 0
}
_aidev_check_and_record_central_version
if [ -n "${AIDEV_HEARTBEAT_URL:-}" ] && [ -x /usr/local/lib/aidev/emit-heartbeat ]; then
  _aidev_hb_dir="${AIDEV_AI_DEFAULTS_PATH:-/etc/aidev02/aienv.d/defaults.sh}"; _aidev_hb_dir="${_aidev_hb_dir%/*}"
  _aidev_hb_ver=""; [ -r "${_aidev_hb_dir}/VERSION" ] && read -r _aidev_hb_ver < "${_aidev_hb_dir}/VERSION" 2>/dev/null || true
  _aidev_hb_sha=""; [ -r "${_aidev_hb_dir}/defaults.sha256" ] && read -r _aidev_hb_sha _ < "${_aidev_hb_dir}/defaults.sha256" 2>/dev/null || true
  _aidev_hb_boot="unknown"; [ -r /proc/sys/kernel/random/boot_id ] && read -r _aidev_hb_boot < /proc/sys/kernel/random/boot_id 2>/dev/null || true
  if [ -n "${_aidev_hb_ver}" ]; then
    mkdir -p "${HOME}/.aidev/logs" 2>/dev/null || true
    nohup setsid /usr/local/lib/aidev/emit-heartbeat "${AIDEV_HEARTBEAT_URL}" "${_aidev_hb_ver}" "${_aidev_hb_sha:0:12}" "${_aidev_hb_boot:0:8}" "$$" "${AIDEV_STATE_LOG_TIER:-C}" "${CODER_WORKSPACE_ID:-unknown}" "${USER:-unknown}" </dev/null >>"${HOME}/.aidev/logs/heartbeat.log" 2>&1 &
  fi
  unset _aidev_hb_dir _aidev_hb_ver _aidev_hb_sha _aidev_hb_boot
fi
_aidev_boot_notice_check() {
  [ -r /proc/1/stat ] || return 0
  local boot last_shell
  boot=$(awk '{ s=$0; sub(/.*\) /,"",s); split(s,f," "); print f[20] }' /proc/1/stat 2>/dev/null) || return 0
  case "${boot}" in ''|*[!0-9]*) return 0 ;; esac
  last_shell=$(cat "${HOME}/.cache/aidev02/last-shell" 2>/dev/null) || true
  case "${last_shell}" in ''|*[!0-9]*) last_shell=0 ;; esac
  if [ "${boot}" -gt "${last_shell}" ]; then
    printf 'INFO: workspace restarted since last login; agent processes ended, scrollback preserved\n'
  fi
  return 0
}
_aidev_boot_notice_check
_aidev_record_shell_state() {
  command mkdir -p "${HOME}/.cache/aidev02" 2>/dev/null || return 0
  [ -r /proc/1/stat ] || return 0
  awk '{ s=$0; sub(/.*\) /,"",s); split(s,f," "); print f[20] }' /proc/1/stat > "${HOME}/.cache/aidev02/last-shell" 2>/dev/null || return 0
}
_aidev_record_shell_state
_aidev_motd_cache_init() {
  command mkdir -p "${HOME}/.cache/motd" 2>/dev/null || return 0
  : >> "${HOME}/.cache/motd/etag" 2>/dev/null
  : >> "${HOME}/.cache/motd/last-update" 2>/dev/null
  : >> "${HOME}/.cache/motd/last-attempt" 2>/dev/null
  : >> "${HOME}/.cache/motd/rejected.log" 2>/dev/null
  return 0
}
_aidev_motd_cache_init
_aidev_motd_trigger() {
  command -v motd-update >/dev/null 2>&1 || return 0
  # Split locals: bash expands ${cache} on the same `local` line before the
  # assignment, so `local cache=... last="${cache}/last-attempt"` opens
  # /last-attempt and /.motd-update.lock (issue #194).
  local cache last lock now attempt_epoch age
  cache="${HOME}/.cache/motd"
  last="${cache}/last-attempt"
  lock="${cache}/.motd-update.lock"
  now="$(date +%s 2>/dev/null)" || return 0
  attempt_epoch="$(cut -d' ' -f1 < "${last}" 2>/dev/null)" || true
  case "${attempt_epoch}" in ''|*[!0-9]*) attempt_epoch=0 ;; esac
  age=$(( now - attempt_epoch ))
  [ "${age}" -gt 86400 ] || return 0
  ( flock -n 9 2>/dev/null ) 9>"${lock}" 2>/dev/null || return 0
  ( motd-update --background </dev/null >/dev/null 2>&1 & ) >/dev/null 2>&1 || :
  return 0
}
_aidev_motd_trigger
# <<< aidev02:env-block <<<

# >>> aidev02:fr24-hooks >>>
# FR24 history-search (substitute for missing-upstream
# history-search-multi-word plugin, D-CL01.17): Up/Down search history
# by the prefix already typed.
bind '"\e[A":history-search-backward' 2>/dev/null
bind '"\e[B":history-search-forward' 2>/dev/null
# FR24 extract() (substitute for missing-upstream extract plugin).
extract() {
  if [ -z "$1" ] || [ ! -f "$1" ]; then
    printf 'extract: not a file: %s\n' "${1:-}" >&2
    return 2
  fi
  case "$1" in
    *.tar.gz | *.tgz) tar xzf "$1" ;;
    *.tar.bz2 | *.tbz2) tar xjf "$1" ;;
    *.tar.xz | *.txz) tar xJf "$1" ;;
    *.tar.zst) tar --use-compress-program=unzstd -xf "$1" ;;
    *.tar) tar xf "$1" ;;
    *.gz) gunzip -k "$1" ;;
    *.bz2) bunzip2 -k "$1" ;;
    *.xz) unxz -k "$1" ;;
    *.zst) unzstd -k "$1" ;;
    *.zip) unzip "$1" ;;
    *.7z) 7z x "$1" ;;
    *.rar) unrar x "$1" ;;
    *) printf 'extract: unsupported archive: %s\n' "$1" >&2; return 2 ;;
  esac
}
# Interactive tool init (prompt, dir-jump, fuzzy-find). Each is guarded so a
# missing tool degrades silently instead of breaking the shell.
command -v starship >/dev/null && eval "$(starship init bash)"
command -v zoxide >/dev/null && eval "$(zoxide init bash)"
command -v fzf >/dev/null && eval "$(fzf --bash 2>/dev/null)"
# Shared FR11 attach stays after tool init and before status/late local overrides.
. /usr/local/lib/aidev/shell-zellij.sh
# T-14 / T08.08 status-surface scaffolding (named requirement -- NOT part of
# the 6-line budget). Registers a PROMPT_COMMAND hook that surfaces hints for
# ~/.aidev/status/<name> indicator files (gh-auth-missing; startup-summary
# warn/fail via T08.09). Sourced AFTER starship/zoxide/fzf so
# the appended PROMPT_COMMAND segment runs last per prompt redraw.
[ -r /usr/local/lib/aidev/status-surface.sh ] && . /usr/local/lib/aidev/status-surface.sh
# ccsession auto-start: asks a person opening a terminal for a session name at
# the first prompt (after ~/.bashrc.local). CCSESSION_AUTOSTART=0 turns it off.
[ -r /usr/local/lib/aidev/ccsession-autostart.sh ] && . /usr/local/lib/aidev/ccsession-autostart.sh
# <<< aidev02:fr24-hooks <<<

# >>> aidev02:bashrc-local >>>
# User overrides, sourced LAST so they win (FR23). The template must never
# write below this line; reviewer-PR rejects template writes (T02.13).
[ -r "$HOME/.bashrc.local" ] && . "$HOME/.bashrc.local"
# <<< aidev02:bashrc-local <<<

# Added by codebase-memory-mcp install
export PATH="/home/coder/.local/bin:$PATH"
