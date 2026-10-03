#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stash 彩色图标集 —— 构建脚本
============================
用法:
    python3 tools/build.py                          # 用默认 base-url 构建
    python3 tools/build.py --base-url https://cdn.jsdelivr.net/gh/USER/REPO@main/
    python3 tools/build.py --skip-download          # 只用已有缓存

产物:
    icons/  flags/  flags-square/  regions/
    icons.json  icons-zh.json  icons-index.json
    preview.png
    stash/*.yaml
    README.md  NOTICE.md

依赖: 仅需标准库 + Pillow + 系统自带 sips（用于 SVG 栅格化）。
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manifest import (QURE, SI, REGIONS, FLAGS,  # noqa: E402
                      SET_NAME, SET_NAME_EN, SET_DESC)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, ".cache")
ICONS = os.path.join(ROOT, "icons")
FLAGDIR = os.path.join(ROOT, "flags")
FLAGSQ = os.path.join(ROOT, "flags-square")
REGIONS_DIR = os.path.join(ROOT, "regions")

QURE_REPO = "https://github.com/Koolson/Qure.git"
SI_DATA = ("https://raw.githubusercontent.com/simple-icons/simple-icons/"
           "develop/data/simple-icons.json")
SI_SVG = ("https://raw.githubusercontent.com/simple-icons/simple-icons/"
          "develop/icons/{slug}.svg")
FLAG_SVG = ("https://raw.githubusercontent.com/lipis/flag-icons/main/"
            "flags/4x3/{code}.svg")
# 回退源：flagcdn 的定尺寸 4:3 PNG（同一作者 lipis 出品，与 flag-icons 同源）
FLAG_PNG = "https://flagcdn.com/256x192/{code}.png"

SIZE = 144
SUPERSAMPLE = 640
RING = 7            # 描边宽度（超采样坐标系下）
RING_COLOR = (0, 0, 0, 46)


# --------------------------------------------------------------------------
# 基础工具
# --------------------------------------------------------------------------
def log(msg):
    print(msg, flush=True)


def http_get(url, dest=None, binary=True):
    req = urllib.request.Request(url, headers={"User-Agent": "stash-icons-builder"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    if dest:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as f:
            f.write(data)
    return data


def svg_to_png(svg_path, png_path):
    """用 macOS 自带 sips 把 SVG 栅格化为 PNG（尊重 viewBox 尺寸）。"""
    if os.path.exists(png_path):
        return True
    r = subprocess.run(["sips", "-s", "format", "png", svg_path, "--out", png_path],
                       capture_output=True)
    return r.returncode == 0 and os.path.exists(png_path) and os.path.getsize(png_path) > 0


def ensure_dirs():
    for d in (ICONS, FLAGDIR, FLAGSQ, REGIONS_DIR, CACHE,
              os.path.join(ROOT, "stash")):
        os.makedirs(d, exist_ok=True)


# --------------------------------------------------------------------------
# 来源 1: Qure（稀疏克隆，只取 Color 目录）
# --------------------------------------------------------------------------
def ensure_qure(skip_download=False):
    dst = os.path.join(CACHE, "qure")
    color = os.path.join(dst, "IconSet", "Color")
    if os.path.isdir(color) and len(os.listdir(color)) > 300:
        log(f"[Qure] 缓存命中：{len(os.listdir(color))} 个图标")
        return color
    if skip_download:
        sys.exit("缺少 Qure 缓存，且指定了 --skip-download")
    log("[Qure] 稀疏克隆 Koolson/Qure ...")
    shutil.rmtree(dst, ignore_errors=True)
    subprocess.run(["git", "clone", "--depth", "1", "--filter=blob:none",
                    "--sparse", QURE_REPO, dst], check=True,
                   capture_output=True)
    subprocess.run(["git", "sparse-checkout", "set", "IconSet/Color"],
                   cwd=dst, check=True, capture_output=True)
    n = len(os.listdir(color))
    log(f"[Qure] 完成：{n} 个图标")
    return color


# --------------------------------------------------------------------------
# 来源 2: simple-icons（CC0）→ 带品牌色的 SVG → PNG
# --------------------------------------------------------------------------
def si_slug(title):
    """按 simple-icons 的官方 slug 规则生成文件名。

    规则：小写；'+'→'plus'；'.'→'dot'；'&'→'and'；其余非字母数字字符丢弃。
    例：'Trip.com' → 'tripdotcom'，'1Password' → '1password'，'Red Hat' → 'redhat'
    """
    s = title.lower()
    s = s.replace("+", "plus").replace(".", "dot").replace("&", "and")
    return "".join(ch for ch in s if ch.isalnum())


def si_hex_map(skip_download=False):
    p = os.path.join(CACHE, "simple-icons.json")
    if not os.path.exists(p):
        if skip_download:
            sys.exit("缺少 simple-icons 数据缓存")
        log("[simple-icons] 下载品牌数据 ...")
        http_get(SI_DATA, p)
    data = json.load(open(p, encoding="utf-8"))
    items = data["icons"] if isinstance(data, dict) else data
    out = {}
    for it in items:
        out[it["title"]] = it.get("hex", "000000")
    return out


def render_si_icon(title, hexcolor, out_png, cache):
    """把 simple-icons 的单路径 SVG 重写为品牌色 + 144×144，再栅格化。"""
    slug = si_slug(title)
    svg_cache = os.path.join(cache, "si_svg", f"{slug}.svg")
    if not os.path.exists(svg_cache):
        try:
            raw = http_get(SI_SVG.format(slug=slug)).decode("utf-8")
        except Exception as e:
            return False, f"下载失败 {slug}: {e}"
        os.makedirs(os.path.dirname(svg_cache), exist_ok=True)
        open(svg_cache, "w", encoding="utf-8").write(raw)
    raw = open(svg_cache, encoding="utf-8").read()

    import re
    m = re.search(r'<path\s+d="([^"]+)"', raw)
    if not m:
        return False, f"未找到 path: {slug}"

    # 留 9% 内边距，把 24×24 的图形放大到 144×144 画布
    inner = SIZE * 0.82
    scale = inner / 24.0
    off = (SIZE - inner) / 2.0
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE}" '
           f'height="{SIZE}" viewBox="0 0 {SIZE} {SIZE}">'
           f'<g transform="translate({off:.3f},{off:.3f}) scale({scale:.5f})">'
           f'<path d="{m.group(1)}" fill="#{hexcolor}"/></g></svg>')

    tmp = os.path.join(cache, "si_svg", f"{slug}.scaled.svg")
    open(tmp, "w", encoding="utf-8").write(svg)
    if os.path.exists(out_png):
        os.remove(out_png)
    if not svg_to_png(tmp, out_png):
        return False, f"sips 栅格化失败: {slug}"
    return True, None


# --------------------------------------------------------------------------
# 来源 3: 国旗（lipis/flag-icons, MIT）→ 圆形 / 圆角方形
# --------------------------------------------------------------------------
def _mask_circle(img, ring=RING):
    S = img.size[0]
    m = Image.new("L", (S, S), 0)
    ImageDraw.Draw(m).ellipse((0, 0, S - 1, S - 1), fill=255)
    img = img.copy()
    img.putalpha(m)
    d = ImageDraw.Draw(img)
    r = ring // 2
    d.ellipse((r, r, S - 1 - r, S - 1 - r), outline=RING_COLOR, width=ring)
    return img


def _mask_squircle(img, ring=RING, radius_ratio=0.115):
    W, H = img.size
    m = Image.new("L", (W, H), 0)
    rad = int(W * radius_ratio)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, W - 1, H - 1), radius=rad, fill=255)
    img = img.copy()
    img.putalpha(m)
    d = ImageDraw.Draw(img)
    r = ring // 2
    d.rounded_rectangle((r, r, W - 1 - r, H - 1 - r), radius=rad,
                        outline=RING_COLOR, width=ring)
    return img


def make_circle_flag(src_png, out_png):
    im = Image.open(src_png).convert("RGBA")
    w, h = im.size
    s = min(w, h)
    im = im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s))
    im = im.resize((SUPERSAMPLE, SUPERSAMPLE), Image.LANCZOS)
    im = _mask_circle(im)
    im.resize((SIZE, SIZE), Image.LANCZOS).save(out_png, "PNG", optimize=True)


def make_squircle_flag(src_png, out_png):
    im = Image.open(src_png).convert("RGBA")
    W = SUPERSAMPLE
    H = int(SUPERSAMPLE * 0.75)
    im = im.resize((W, H), Image.LANCZOS)
    im = _mask_squircle(im)
    flag = im.resize((SIZE, int(SIZE * 0.75)), Image.LANCZOS)
    canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    canvas.alpha_composite(flag, (0, (SIZE - flag.size[1]) // 2))
    canvas.save(out_png, "PNG", optimize=True)


# --------------------------------------------------------------------------
# 构建各目录
# --------------------------------------------------------------------------
def safe_name(name):
    """输出文件名净化：把 '+' 换成 'Plus'。

    原因：Disney+ / Star+ / ESPN+ / discovery+ 这类文件名在 URL 里必须写成
    Disney%2B.png，部分 CDN（含 jsDelivr）对路径中的 %2B 处理不一致。
    改成 Plus 后 URL 完全无歧义，而 JSON 里展示用的 name 仍是 "Disney+"。
    """
    return name.replace("+", "Plus")


def build_icons(qure_color, hexmap, cache, skip_download):
    made, missing = [], []
    for name, zh, cat in QURE:
        src = os.path.join(qure_color, f"{name}.png")
        if not os.path.exists(src):
            missing.append((name, "Qure 未收录"))
            continue
        im = Image.open(src).convert("RGBA")
        if im.size != (SIZE, SIZE):
            im = im.resize((SIZE, SIZE), Image.LANCZOS)
        out_name = safe_name(name)
        im.save(os.path.join(ICONS, f"{out_name}.png"), "PNG", optimize=True)
        made.append((f"{out_name}.png", name, zh, cat, "Qure"))
    log(f"[icons] Qure 输出 {len(made)} 个")

    ok = 0
    for fname, title, zh, cat in SI:
        out = os.path.join(ICONS, f"{safe_name(fname)}.png")
        hexc = hexmap.get(title)
        if hexc is None:
            missing.append((fname, f"simple-icons 无 {title}"))
            continue
        good, err = render_si_icon(title, hexc, out, cache)
        if good:
            made.append((f"{safe_name(fname)}.png", fname, zh, cat, "simple-icons"))
            ok += 1
        else:
            missing.append((fname, err))
    log(f"[icons] simple-icons 输出 {ok} 个")
    return made, missing


def build_regions(qure_color):
    n = 0
    for code, zh in REGIONS:
        src = os.path.join(qure_color, f"{code}.png")
        if os.path.exists(src):
            Image.open(src).convert("RGBA").resize((SIZE, SIZE), Image.LANCZOS) \
                 .save(os.path.join(REGIONS_DIR, f"{code}.png"), "PNG", optimize=True)
            n += 1
    log(f"[regions] 输出 {n} 个")
    return n


def flag_png_broken(png, white_th=0.92, black_th=0.92):
    """检测 SVG 栅格化是否失败。

    背景：macOS 的 sips 无法正确渲染 lipis 旗面里用 <use xlink:href> 组合的图形，
    实测委内瑞拉(ve) 渲染成空白、坦桑尼亚(tz) 渲染成近黑。
    判据：旗面中部采样中「近白」或「近黑」像素占比过高。
    注意塞浦路斯(cy) 是白底橙图，近白约 76%，低于阈值，不会被误判。
    """
    im = Image.open(png).convert("RGB")
    w, h = im.size
    px = [im.getpixel((x, y))
          for x in range(int(w * 0.08), int(w * 0.92), max(1, w // 40))
          for y in range(int(h * 0.08), int(h * 0.92), max(1, h // 30))]
    if not px:
        return False
    white = sum(1 for r, g, b in px if r > 235 and g > 235 and b > 235) / len(px)
    black = sum(1 for r, g, b in px if r < 25 and g < 25 and b < 25) / len(px)
    return white > white_th or black > black_th


def build_flags(cache, skip_download):
    svg_dir = os.path.join(cache, "flag_svg")
    os.makedirs(svg_dir, exist_ok=True)
    ok, fail, fallback = 0, [], []
    for code, zh, en, region in FLAGS:
        svg = os.path.join(svg_dir, f"{code}.svg")
        png = os.path.join(svg_dir, f"{code}.png")

        if not os.path.exists(svg) and not skip_download:
            try:
                http_get(FLAG_SVG.format(code=code), svg)
            except Exception as e:
                fail.append((code, f"矢量下载失败 {e}"))

        # 首选：矢量旗面（细节最锐利）
        rendered = False
        if os.path.exists(svg):
            if not os.path.exists(png):
                svg_to_png(svg, png)
            if os.path.exists(png):
                if flag_png_broken(png):
                    os.remove(png)          # 丢弃坏渲染，避免被缓存
                else:
                    rendered = True

        # 回退：flagcdn 定尺寸 PNG（256x192，4:3 统一）
        if not rendered:
            alt = os.path.join(svg_dir, f"{code}.flagcdn.png")
            if not os.path.exists(alt):
                if skip_download:
                    fail.append((code, "无可用缓存"))
                    continue
                try:
                    http_get(FLAG_PNG.format(code=code), alt)
                except Exception as e:
                    fail.append((code, f"回退源下载失败 {e}"))
                    continue
            png = alt
            fallback.append(code)

        make_circle_flag(png, os.path.join(FLAGDIR, f"{code}.png"))
        make_squircle_flag(png, os.path.join(FLAGSQ, f"{code}.png"))
        ok += 1

    log(f"[flags] 圆形 + 圆角方形 各 {ok} 个")
    if fallback:
        log(f"[flags] {len(fallback)} 个因矢量渲染缺陷改用 flagcdn PNG 回退: "
            f"{' '.join(fallback)}")
    if fail:
        log(f"[flags] 失败 {len(fail)}: {fail}")
    return ok


# --------------------------------------------------------------------------
# 生成 JSON 索引
# --------------------------------------------------------------------------
def q(name):
    """URL 路径编码：Disney+ → Disney%2B（Stash 官方示例同此写法）"""
    return urllib.parse.quote(name, safe="")


def build_json(made, base_url):
    base = base_url if base_url.endswith("/") else base_url + "/"

    def url(rel):
        # 只对文件名做编码，保留路径分隔符（否则 icons/x.png 会变成 icons%2Fx.png）
        return base + "/".join(q(part) for part in rel.split("/"))

    # ---- Stash 图标集（英文名，社区通用 schema）----
    icons = [{"name": key, "url": url(f"icons/{n}")}
             for n, key, _, _, _ in made]
    for code, zh, en, region in FLAGS:
        if os.path.exists(os.path.join(FLAGDIR, f"{code}.png")):
            icons.append({"name": f"{en} ({code.upper()})",
                          "url": url(f"flags/{code}.png")})
    for code, zh in REGIONS:
        if os.path.exists(os.path.join(REGIONS_DIR, f"{code}.png")):
            icons.append({"name": f"Region {code}",
                          "url": url(f"regions/{code}.png")})

    payload = {"name": SET_NAME, "description": SET_DESC, "icons": icons}
    with open(os.path.join(ROOT, "icons.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)

    # ---- 中文名优先版（方便 Stash 内搜中文）----
    zh_icons = [{"name": f"{zh} {key}", "url": url(f"icons/{n}")}
                for n, key, zh, _, _ in made]
    for code, zh, en, region in FLAGS:
        if os.path.exists(os.path.join(FLAGDIR, f"{code}.png")):
            zh_icons.append({"name": f"{zh}国旗 {code.upper()}",
                             "url": url(f"flags/{code}.png")})
    for code, zh in REGIONS:
        if os.path.exists(os.path.join(REGIONS_DIR, f"{code}.png")):
            zh_icons.append({"name": f"{zh}地区 {code}", "url": url(f"regions/{code}.png")})
    with open(os.path.join(ROOT, "icons-zh.json"), "w", encoding="utf-8") as f:
        json.dump({"name": SET_NAME + "（中文）", "description": SET_DESC,
                   "icons": zh_icons}, f, ensure_ascii=False, indent=1)

    # ---- 富索引：分类 / 中文别名 / 来源 / 圆角方形国旗 ----
    index = {
        "name": SET_NAME, "name_en": SET_NAME_EN, "description": SET_DESC,
        "base_url": base, "count": {"icons": len(made), "flags": len(FLAGS),
                                    "regions": len(REGIONS)},
        "sites": [
            {"file": f"icons/{n}", "key": key, "zh": zh, "category": cat,
             "source": src, "url": url(f"icons/{n}")}
            for n, key, zh, cat, src in made
        ],
        "flags": [
            {"file": f"flags/{code}.png", "square": f"flags-square/{code}.png",
             "code": code.upper(), "zh": zh, "en": en, "region": region,
             "url": url(f"flags/{code}.png"),
             "square_url": url(f"flags-square/{code}.png")}
            for code, zh, en, region in FLAGS
            if os.path.exists(os.path.join(FLAGDIR, f"{code}.png"))
        ],
        "regions": [
            {"file": f"regions/{code}.png", "code": code, "zh": zh,
             "url": url(f"regions/{code}.png")}
            for code, zh in REGIONS
            if os.path.exists(os.path.join(REGIONS_DIR, f"{code}.png"))
        ],
    }
    with open(os.path.join(ROOT, "icons-index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=1)
    log(f"[json] icons.json {len(icons)} 条 / icons-zh.json {len(zh_icons)} 条 "
        f"/ icons-index.json")


# --------------------------------------------------------------------------
# 预览图
# --------------------------------------------------------------------------
def build_preview(made):
    cell, cols = 104, 12
    picks = [m for m in made][:96]
    flags = [(c, zh) for c, zh, e, r in FLAGS
             if os.path.exists(os.path.join(FLAGDIR, f"{c}.png"))][:36]
    rows_i = (len(picks) + cols - 1) // cols
    rows_f = (len(flags) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell, (rows_i + rows_f) * cell + 20), (250, 250, 252))
    for i, (n, key, zh, cat, src) in enumerate(picks):
        im = Image.open(os.path.join(ICONS, n)).convert("RGBA").resize((cell - 14, cell - 14), Image.LANCZOS)
        bg = Image.new("RGBA", (cell, cell), (255, 255, 255, 255))
        bg.alpha_composite(im, (7, 7))
        sheet.paste(bg.convert("RGB"), ((i % cols) * cell, (i // cols) * cell))
    off = rows_i * cell + 20
    for i, (code, zh) in enumerate(flags):
        im = Image.open(os.path.join(FLAGDIR, f"{code}.png")).convert("RGBA").resize((cell - 14, cell - 14), Image.LANCZOS)
        bg = Image.new("RGBA", (cell, cell), (255, 255, 255, 255))
        bg.alpha_composite(im, (7, 7))
        sheet.paste(bg.convert("RGB"), ((i % cols) * cell, off + (i // cols) * cell))
    sheet.save(os.path.join(ROOT, "preview.png"), "PNG", optimize=True)
    log(f"[preview] preview.png {sheet.size}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default="http://127.0.0.1:8787/",
                    help="图标托管的根 URL（决定 JSON 里的绝对地址）")
    ap.add_argument("--skip-download", action="store_true")
    args = ap.parse_args()

    ensure_dirs()
    qure_color = ensure_qure(args.skip_download)
    hexmap = si_hex_map(args.skip_download)

    made, missing = build_icons(qure_color, hexmap, CACHE, args.skip_download)
    build_regions(qure_color)
    build_flags(CACHE, args.skip_download)
    build_json(made, args.base_url)
    build_preview(made)

    if missing:
        log("\n[注意] 以下条目未生成：")
        for n, why in missing:
            log(f"   - {n}: {why}")

    log(f"\n完成。base-url = {args.base_url}")
    log(f"图标 {len(made)} / 国旗 {len(FLAGS)} ×2 / 地区 {len(REGIONS)}")


if __name__ == "__main__":
    main()
