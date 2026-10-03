#!/usr/bin/env bash
# 安装 launchd 自启服务：Stash 图标集静态服务
#
#   bash tools/install-service.sh
#
# 装好后：
#   * 开机/登录后自动启动
#   * 进程崩溃自动拉起（KeepAlive）
#   * 用稳定的 Bonjour 主机名，路由器重新分配 IP 也不影响
#
# 卸载： bash tools/uninstall-service.sh

set -euo pipefail

LABEL="local.stash-icons"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLIST="$HOME/Library/LaunchAgents/${LABEL}.plist"
LOGDIR="$HOME/Library/Logs"
PORT="${PORT:-8787}"
BIND="${BIND:-0.0.0.0}"
UID_NUM="$(id -u)"

# ---- 选一个 python3：优先系统自带的（路径稳定，且已在防火墙放行名单里）----
PY=""
for c in /usr/bin/python3 /usr/local/bin/python3 \
         "$HOME/.dsh/dsh-runtimes/dsh-primary-runtime/dependencies/python/bin/python3"; do
  if [ -x "$c" ] && "$c" -c 'import sys; sys.exit(0 if sys.version_info>=(3,7) else 1)' 2>/dev/null; then
    PY="$c"; break
  fi
done
[ -n "$PY" ] || { echo "✗ 找不到 Python 3.7+"; exit 1; }

HOSTNAME_LOCAL="$(scutil --get LocalHostName 2>/dev/null || hostname -s)"
mkdir -p "$HOME/Library/LaunchAgents" "$LOGDIR"

echo "服务标签 : $LABEL"
echo "项目目录 : $ROOT"
echo "Python   : $PY ($("$PY" --version 2>&1))"
echo "监听     : ${BIND}:${PORT}"
echo "日志     : $LOGDIR/stash-icons.log"
echo

# ---- 若端口已被占用（例如之前用 serve.sh 或后台进程起的服务），先释放 ----
if command -v lsof >/dev/null 2>&1; then
  OLD_PIDS="$(lsof -ti "tcp:${PORT}" 2>/dev/null || true)"
  if [ -n "$OLD_PIDS" ]; then
    echo "· 端口 ${PORT} 被占用（PID: $(echo $OLD_PIDS | tr '\n' ' ')），正在释放…"
    kill $OLD_PIDS 2>/dev/null || true
    sleep 1
    OLD_PIDS="$(lsof -ti "tcp:${PORT}" 2>/dev/null || true)"
    if [ -n "$OLD_PIDS" ]; then
      kill -9 $OLD_PIDS 2>/dev/null || true
      sleep 1
    fi
  fi
fi

# ---- 若已加载，先卸掉旧版本 ----
launchctl bootout "gui/${UID_NUM}/${LABEL}" 2>/dev/null || \
  launchctl unload "$PLIST" 2>/dev/null || true

# ---- 写 plist ----
cat > "$PLIST" <<PLIST_EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${LABEL}</string>

    <key>ProgramArguments</key>
    <array>
        <string>${PY}</string>
        <string>${ROOT}/tools/server.py</string>
    </array>

    <key>EnvironmentVariables</key>
    <dict>
        <key>PORT</key><string>${PORT}</string>
        <key>BIND</key><string>${BIND}</string>
        <key>PYTHONUNBUFFERED</key><string>1</string>
    </dict>

    <key>WorkingDirectory</key>
    <string>${ROOT}</string>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <true/>

    <key>ProcessType</key>
    <string>Background</string>

    <key>StandardOutPath</key>
    <string>${LOGDIR}/stash-icons.log</string>

    <key>StandardErrorPath</key>
    <string>${LOGDIR}/stash-icons.log</string>
</dict>
</plist>
PLIST_EOF

plutil -lint "$PLIST" >/dev/null || { echo "✗ plist 格式错误"; exit 1; }
echo "✓ 已写入 $PLIST"

# ---- 加载（新老 launchctl 都兼容）----
if launchctl bootstrap "gui/${UID_NUM}" "$PLIST" 2>/dev/null; then
  echo "✓ launchctl bootstrap 成功"
else
  launchctl load -w "$PLIST"
  echo "✓ launchctl load 成功"
fi
launchctl enable "gui/${UID_NUM}/${LABEL}" 2>/dev/null || true
sleep 1

# ---- 验证 ----
echo
echo "=== 自检 ==="
if curl -sS -o /dev/null -w "" --max-time 8 "http://127.0.0.1:${PORT}/icons.json" 2>/dev/null; then
  echo "✓ 服务已在监听"
else
  echo "✗ 服务未响应，请查看日志： tail -30 $LOGDIR/stash-icons.log"
fi
launchctl print "gui/${UID_NUM}/${LABEL}" 2>/dev/null | grep -E '^\s*(state|pid) =' | sed 's/^/  /' || true

LAN_IP="$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || true)"

cat <<EOF

============================================================
装好了。填进 Stash 的【长期稳定地址】：

  http://${HOSTNAME_LOCAL}.local:${PORT}/icons-zh.json

  英文名版： http://${HOSTNAME_LOCAL}.local:${PORT}/icons.json
EOF
if [ -n "$LAN_IP" ]; then
cat <<EOF

若 .local 地址在你的网络下解析不了，用 IP 兜底：

  http://${LAN_IP}:${PORT}/icons-zh.json
EOF
fi
cat <<EOF

============================================================
常用命令：
  看状态   launchctl print gui/${UID_NUM}/${LABEL} | head -20
  看日志   tail -f $LOGDIR/stash-icons.log
  重启     launchctl kickstart -k gui/${UID_NUM}/${LABEL}
  卸载     bash tools/uninstall-service.sh

注意：Mac 休眠时服务会暂停。长期挂机请在
「系统设置 → 锁定屏幕」里把「无操作时关闭显示器/进入睡眠」设为「永不」，
或保持接通电源。
EOF
