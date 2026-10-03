#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stash 图标集静态服务
====================
比 `python -m http.server` 更适合长期运行：

  * 显式使用 ThreadingHTTPServer —— 避免 Stash 并发拉取 289 个图标时连接被重置
    （实测 `python -m http.server` 在 16 并发下会出现 Connection reset by peer）
  * 放大 accept 队列，抗瞬时并发
  * 按类型设置缓存头：图片长缓存、JSON 短缓存，更新能及时生效
  * 显式设置 Content-Type，避免个别系统上 .json 被识别成 text/plain

用法：
    python3 tools/server.py                 # 默认 0.0.0.0:8787
    PORT=9000 python3 tools/server.py
    BIND=127.0.0.1 python3 tools/server.py
"""
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(os.environ.get("PORT", "8787"))
BIND = os.environ.get("BIND", "0.0.0.0")

# 扩展名 -> (Content-Type, Cache-Control)
TYPES = {
    ".json": ("application/json; charset=utf-8", "public, max-age=300"),
    ".png":  ("image/png",  "public, max-age=86400"),
    ".jpg":  ("image/jpeg", "public, max-age=86400"),
    ".jpeg": ("image/jpeg", "public, max-age=86400"),
    ".svg":  ("image/svg+xml", "public, max-age=86400"),
    ".md":   ("text/markdown; charset=utf-8", "public, max-age=300"),
    ".yaml": ("text/yaml; charset=utf-8", "public, max-age=300"),
    ".yml":  ("text/yaml; charset=utf-8", "public, max-age=300"),
    ".txt":  ("text/plain; charset=utf-8", "public, max-age=300"),
}


class Handler(SimpleHTTPRequestHandler):
    server_version = "StashIcons/1.0"

    def __init__(self, *args, **kwargs):
        kwargs["directory"] = ROOT
        super().__init__(*args, **kwargs)

    def guess_type(self, path):
        ext = os.path.splitext(str(path))[1].lower()
        if ext in TYPES:
            return TYPES[ext][0]
        return super().guess_type(path)

    def end_headers(self):
        ext = os.path.splitext(self.path.split("?")[0])[1].lower()
        if ext in TYPES:
            self.send_header("Cache-Control", TYPES[ext][1])
        # 便于用浏览器/curl 确认服务身份
        self.send_header("X-Icon-Server", "stash-icons")
        super().end_headers()

    def log_message(self, fmt, *args):
        # launchd 会把 stderr 落盘，保持精简
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


class Server(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True
    request_queue_size = 128


def main():
    os.chdir(ROOT)
    httpd = Server((BIND, PORT), Handler)
    sys.stderr.write("stash-icons serving %s on http://%s:%d/\n" % (ROOT, BIND, PORT))
    sys.stderr.flush()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
