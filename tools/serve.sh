#!/usr/bin/env bash
# 本地 HTTP 托管图标集（用于先在本机验证，或让同一局域网的 iPhone 直接引用）
#
#   bash tools/serve.sh            # 默认 8787 端口
#   bash tools/serve.sh 9000       # 自定义端口
#
# 启动后：
#   Mac 自身   → http://127.0.0.1:8787/icons.json
#   同局域网 iPhone → http://<Mac局域网IP>:8787/icons.json
#
# 注意：Stash 运行在 iOS/iPadOS 上时，127.0.0.1 指向的是手机自己，必须用 Mac 的局域网 IP。

set -euo pipefail

PORT="${1:-8787}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

LAN_IP="$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo '')"

echo "图标集根目录: $ROOT"
echo "端口:         $PORT"
echo
echo "图标集 JSON 地址："
echo "  Mac 本机     : http://127.0.0.1:${PORT}/icons.json"
echo "  中文名优先版 : http://127.0.0.1:${PORT}/icons-zh.json"
if [ -n "$LAN_IP" ]; then
  echo "  局域网(iPhone): http://${LAN_IP}:${PORT}/icons.json"
else
  echo "  （未探测到局域网 IP，请在「系统设置 → 网络」中确认）"
fi
echo
echo "按 Ctrl+C 停止。"
echo

python3 -m http.server "$PORT" --bind 0.0.0.0
