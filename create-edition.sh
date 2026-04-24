#!/usr/bin/env bash
# Weekly The Busbar edition via Claude Code (non-interactive)
# Runs on Saturdays at 23:00 — edition date is the upcoming Monday.
#
# Crontab entry:
#   0 23 * * 6 /DATA/AppData/big-bear-code-server/projects/dc-news-agent/create-edition.sh >> /tmp/busbar-edition.log 2>&1

set -euo pipefail

cd /DATA/AppData/big-bear-code-server/projects/dc-news-agent

# Edition date = the upcoming Monday (Saturday + 2 days).
# "next monday" from Saturday gives Mon +2; cron only fires on Saturday so this is always correct.
EDITION_DATE=$(date -d "next monday" +%Y-%m-%d)

# Skip if this edition already exists
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
