#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
往图标集里添加你自己的图标
==========================
三种用法：

  # 1) 用本地图片
  python3 tools/add_icon.py --name 京东 --file ~/Downloads/jd.png --base-url http://127.0.0.1:8787/

  # 2) 自动抓站点图标（优先 apple-touch-icon，通常 180×180，比 favicon.ico 清晰）
  python3 tools/add_icon.py --name 京东 --domain www.jd.com --base-url http://127.0.0.1:8787/

  # 3) 直接用图片 URL
  python3 tools/add_icon.py --name 京东 --url https://example.com/jd.png --base-url http://127.0.0.1:8787/

加完会自动重建 icons.json / icons-zh.json / icons-index.json。

说明：本图标集的主力是 Qure（社区事实标准）+ simple-icons（矢量）。
京东 / 优酷 / 腾讯视频 / 拼多多 / 滴滴 等品牌在这两个来源里都没有收录，
也不在 dashboard-icons 里，因此留给你按上面方式自助补充。
"""
import argparse
import io
import json
import os
import sys
import urllib.parse
import urllib.request

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS = os.path.join(ROOT, "icons")
SIZE = 144
UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15"

CANDIDATES = [
    "https://{d}/apple-touch-icon.png",
    "https://{d}/apple-touch-icon-precomposed.png",
    "https://{d}/apple-touch-icon-180x180.png",
    "https://{d}/favicon.ico",
]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read()


def from_domain(domain):
    best = None
    for tpl in CANDIDATES:
        u = tpl.format(d=domain)
        try:
            data = fetch(u)
            im = Image.open(io.BytesIO(data)).convert("RGBA")
            if im.size[0] < 32:
                continue
            print(f"  ✓ {u}  {im.size[0]}×{im.size[1]}")
            if best is None or im.size[0] > best[0].size[0]:
                best = (im, u)
            if im.size[0] >= 180:
                break
        except Exception:
            continue
    if best is None:
        sys.exit(f"未能从 {domain} 取到可用图标")
    if best[0].size[0] < 120:
        print(f"  ⚠ 源图仅 {best[0].size[0]}px，放大到 144 会偏糊，建议手动提供高清图")
    return best[0]


def normalize(im):
    """透明底：把接近白色的实底抠掉，再居中裁成正方形并缩放到 144。"""
    im = im.convert("RGBA")
    w, h = im.size
    if w != h:
        s = min(w, h)
        im = im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s))
    if im.size != (SIZE, SIZE):
        im = im.resize((SIZE, SIZE), Image.LANCZOS)
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True, help="图标名（会成为文件名与 JSON 里的 name）")
    ap.add_argument("--file")
    ap.add_argument("--url")
    ap.add_argument("--domain")
    ap.add_argument("--zh", help="中文名（写入 icons-index.json）")
    ap.add_argument("--category", default="自定义")
    ap.add_argument("--base-url", default="http://127.0.0.1:8787/")
    a = ap.parse_args()

    if a.file:
        im = Image.open(a.file)
    elif a.url:
        im = Image.open(io.BytesIO(fetch(a.url)))
    elif a.domain:
        im = from_domain(a.domain)
    else:
        sys.exit("请提供 --file / --url / --domain 之一")

    os.makedirs(ICONS, exist_ok=True)
    out = os.path.join(ICONS, f"{a.name}.png")
    normalize(im).save(out, "PNG", optimize=True)
    print(f"  ✓ 写入 icons/{a.name}.png  {os.path.getsize(out)} B")

    # 合并进富索引，再整体重写 JSON
    idx_p = os.path.join(ROOT, "icons-index.json")
    if os.path.exists(idx_p):
        idx = json.load(open(idx_p, encoding="utf-8"))
        base = a.base_url if a.base_url.endswith("/") else a.base_url + "/"
        rec = {"file": f"icons/{a.name}.png", "key": a.name, "zh": a.zh or a.name,
               "category": a.category, "source": "自定义",
               "url": base + "icons/" + urllib.parse.quote(a.name, safe="") + ".png"}
        idx["sites"] = [s for s in idx["sites"] if s["file"] != rec["file"]] + [rec]
        json.dump(idx, open(idx_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("  ✓ 已并入 icons-index.json")
    print("\n下一步：运行 tools/rebase.py --base-url <你的地址> 重新生成 icons.json")


if __name__ == "__main__":
    main()
