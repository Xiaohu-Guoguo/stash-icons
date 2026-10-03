#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
推送后在线自检
==============
验证图标集在 jsDelivr 上是否真的可用——不只看 JSON 能不能下载，
而是把 JSON 里的图标 URL 抽样/全量请求一遍。这才是「Stash 能不能显示图标」的真实判据。

用法：
    python3 tools/verify-online.py                    # 抽样 40 条，快
    python3 tools/verify-online.py --all              # 全量 289×4 条，慢但彻底
    python3 tools/verify-online.py --json icons-zh.json
"""
import argparse
import json
import os
import random
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALL_JSON = ("icons.json", "icons-zh.json", "icons-fastly.json", "icons-zh-fastly.json")


def head(url, timeout=20):
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": "stash-icons-check"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.headers.get("Content-Type", ""), len(r.read())
    except urllib.error.HTTPError as e:
        return e.code, "", 0
    except Exception as e:
        return "ERR", str(e), 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=None, help="只检查指定文件")
    ap.add_argument("--all", action="store_true", help="全量检查")
    ap.add_argument("--sample", type=int, default=40)
    a = ap.parse_args()

    files = [a.json] if a.json else list(ALL_JSON)
    overall_bad = 0

    for fn in files:
        p = os.path.join(ROOT, fn)
        if not os.path.exists(p):
            print(f"跳过（不存在）: {fn}")
            continue
        d = json.load(open(p, encoding="utf-8"))
        items = d["icons"]
        if not a.all and len(items) > a.sample:
            items = random.sample(items, a.sample)

        # 1) JSON 本身可达？
        st, ct, size = head(d["icons"][0]["url"])   # 先探一条，判断整个域名是否通

        bad = []
        t = time.time()
        for it in items:
            s, c, n = head(it["url"])
            if s != 200 or "image" not in (c or ""):
                bad.append((it["name"], it["url"], s, c))
        dur = time.time() - t

        status = "✓" if not bad else "✗"
        print(f"{status} {fn}: 抽查 {len(items)}/{len(d['icons'])} 条，"
              f"失败 {len(bad)}，耗时 {dur:.1f}s")
        for b in bad[:6]:
            print(f"     ✗ {b[0]}  HTTP={b[2]} {b[3]}")
            print(f"       {b[1]}")
        overall_bad += len(bad)

    print()
    if overall_bad == 0:
        print("全部通过 —— 可以直接填进 iPhone 的 Stash。")
    else:
        print(f"有 {overall_bad} 个失败。常见原因：")
        print("  1. 仓库不是 public（jsDelivr 只服务公开仓库）")
        print("  2. 分支不是 main，或文件还没推上去")
        print("  3. jsDelivr 还在回源缓存，等 1-2 分钟重试")
        print("  4. 刚更新过文件：jsDelivr 有约 12 小时缓存，可到")
        print("     https://www.jsdelivr.com/tools/purge 手动刷新")
    sys.exit(1 if overall_bad else 0)


if __name__ == "__main__":
    main()
