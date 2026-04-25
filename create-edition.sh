#!/usr/bin/env bash
# Weekly The Busbar edition via local Claude Code (non-interactive)
# Runs via system cron every Sunday at 00:40 server local time (Europe/Berlin).
# Edition date = the upcoming Monday.
#
# Crontab entry:
#   40 0 * * 0 /DATA/AppData/big-bear-code-server/projects/The_Busbar/create-edition.sh >> /tmp/busbar-edition.log 2>&1

set -euo pipefail

PROJECT=/DATA/AppData/big-bear-code-server/projects/The_Busbar
cd "$PROJECT"

# Edition date = the upcoming Monday.
# `date -d "next monday"` returns the next Monday relative to today —
# correct on both Saturday (+2) and Sunday (+1).
EDITION_DATE=$(date -d "next monday" +%Y-%m-%d)

# Skip if this edition already exists (manual run, retry, etc.)
if [ -f "src/editions/${EDITION_DATE}.md" ]; then
    echo "[$(date)] Edition ${EDITION_DATE} already exists, skipping."
    exit 0
fi

echo "[$(date)] Starting edition ${EDITION_DATE}..."

# Prepend the authoritative target date so Claude doesn't re-derive it from today's weekday
{
    echo "EDITION TARGET DATE: ${EDITION_DATE}"
    echo "This is the upcoming Monday. Use this as the edition date — do not recompute from today's weekday."
    echo "---"
    cat .claude/commands/new-edition.md
} | /home/lange-hegermann/.local/bin/claude -p \
    --allowedTools "Bash,Read,Write,Edit,Glob,Grep,WebSearch,WebFetch,Agent,Skill"

echo "[$(date)] Edition ${EDITION_DATE} done."
