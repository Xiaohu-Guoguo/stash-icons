#!/usr/bin/env bash
# 卸载 Stash 图标集自启服务

set -euo pipefail

LABEL="local.stash-icons"
PLIST="$HOME/Library/LaunchAgents/${LABEL}.plist"
UID_NUM="$(id -u)"

if launchctl bootout "gui/${UID_NUM}/${LABEL}" 2>/dev/null; then
  echo "✓ 已卸载（bootout）"
elif launchctl unload "$PLIST" 2>/dev/null; then
  echo "✓ 已卸载（unload）"
else
  echo "· 服务本来就没在运行"
fi

if [ -f "$PLIST" ]; then
  rm -f "$PLIST"
  echo "✓ 已删除 $PLIST"
fi

echo
echo "日志文件保留在 ~/Library/Logs/stash-icons.log，需要的话自行删除。"
echo "图标集文件本身没有任何改动。"
