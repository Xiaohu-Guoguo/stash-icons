#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成镜像版图标集 JSON
=====================
只替换 URL 的 scheme + host（保留路径，例如 jsDelivr 的 /gh/user/repo@main/ 属于路径），
因此同一份图标既能出 cdn.jsdelivr.net 版，也能出 fastly.jsdelivr.net 版。

用法：
    # jsDelivr 官方 CDN 的备用域名（Stash 自带 default.yaml 用的就是它）
    python3 tools/make-mirror.py --base-url https://fastly.jsdelivr.net --suffix fastly

    # 局域网 IP 兜底
    python3 tools/make-mirror.py --base-url http://192.168.4.107:8787 --suffix ip
"""
import argparse
import json
import os
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES = ("icons.json", "icons-zh.json")


def swap_host(url, new_base):
    a = urllib.parse.urlsplit(url)
    b = urllib.parse.urlsplit(new_base)
    netloc = b.netloc or a.netloc
    return urllib.parse.urlunsplit((b.scheme or a.scheme, netloc, a.path, a.query, a.fragment))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", required=True, help="新的 scheme+host，如 https://fastly.jsdelivr.net")
    ap.add_argument("--suffix", required=True, help="输出后缀，如 fastly → icons-fastly.json")
    ap.add_argument("--tag", default="", help="追加到 name 里的说明，如「Fastly 镜像」")
    a = ap.parse_args()

    n = 0
    for src in SOURCES:
        p = os.path.join(ROOT, src)
        if not os.path.exists(p):
            print(f"  跳过（不存在）: {src}")
            continue
        d = json.load(open(p, encoding="utf-8"))
        for it in d.get("icons", []):
            it["url"] = swap_host(it["url"], a.base_url)
        if a.tag:
            d["name"] = d.get("name", "") + f"（{a.tag}）"
        stem = src[:-5]                      # icons / icons-zh
        dst = os.path.join(ROOT, f"{stem}-{a.suffix}.json")
        json.dump(d, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"  ✓ {os.path.basename(dst)}  ({len(d.get('icons', []))} 条 → {a.base_url})")
        n += 1
    print(f"\n完成，共生成 {n} 个镜像文件。")


if __name__ == "__main__":
    main()
