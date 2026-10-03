#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
给 Stash 配置的 proxy-groups 批量挂图标
=======================================
采用**逐行插入**而非 YAML 重新序列化，因此：
  * 原有缩进、顺序、注释、emoji 全部原样保留
  * 只新增 `icon:` 一行，不改动任何既有配置
  * 幂等：已有 icon 的组会跳过，重复运行安全

用法：
    python3 tools/apply-icons.py <输入.yaml> <输出.yaml>
"""
import os
import re
import sys

BASE = "https://cdn.jsdelivr.net/gh/Xiaohu-Guoguo/stash-icons@main/"

# 策略组名（在配置文件里的原文） -> 图标相对路径
ICON_MAP = {
    "Ghelper":          "icons/Proxy.png",
    "🌐 全球智能":       "icons/Global.png",
    "🇭🇰 香港智能":      "flags/hk.png",
    "AI专用":           "icons/ChatGPT.png",
    "📹 YouTube":       "icons/YouTube.png",
    "🔍 谷歌":          "icons/Google.png",
    "✈️ Telegram":      "icons/Telegram.png",
    "🐦 推特X":          "icons/X.png",
    "📘 Meta":          "icons/Facebook.png",
    "🎬 Netflix":       "icons/Netflix.png",
    "🏰 Disney+":       "icons/DisneyPlus.png",
    "🐙 GitHub":        "icons/GitHub.png",
    "🪟 微软":          "icons/Microsoft.png",
    "🍎 苹果":          "icons/Apple.png",
    "🏠 苹果家庭":       "icons/iCloud.png",
    "🖱️ 罗技":          "icons/Logitech.png",
    "🏠 国内网站":       "icons/Domestic.png",
    "🤖 国外AI":        "icons/Claude.png",
    "🤖 中国AI":        "icons/DeepSeek.png",
    "🌍 国外其他网站":    "icons/Final.png",
}

NAME_RE = re.compile(r"^(\s*)(-\s+)?name:\s*(.+?)\s*$")
TOPKEY_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*:")


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, dst = sys.argv[1], sys.argv[2]
    lines = open(src, encoding="utf-8").read().split("\n")

    # 1) 定位 proxy-groups 段落
    start = None
    for i, ln in enumerate(lines):
        if ln.rstrip() == "proxy-groups:":
            start = i + 1
            break
    if start is None:
        sys.exit("✗ 没找到 proxy-groups: 段")
    end = len(lines)
    for i in range(start, len(lines)):
        if TOPKEY_RE.match(lines[i]):
            end = i
            break

    # 2) 逐行扫描，在每个 name 行后插入 icon
    out, hits, skipped, unknown = [], [], [], []
    i = 0
    while i < len(lines):
        ln = lines[i]
        out.append(ln)
        if start <= i < end:
            m = NAME_RE.match(ln)
            if m:
                indent, dash, name = m.group(1), m.group(2) or "", m.group(3)
                name = name.strip().strip('"').strip("'")
                # 组名行缩进：'- name:' 的情况后续键缩进 2 格
                keyindent = "  " if dash else indent
                rel = ICON_MAP.get(name)
                # 下一行是否已经是 icon（幂等检查）
                nxt = lines[i + 1] if i + 1 < len(lines) else ""
                if re.match(r"^\s*icon:", nxt):
                    skipped.append(name)
                elif rel:
                    out.append(f"{keyindent}icon: {BASE}{rel}")
                    hits.append((name, rel))
                else:
                    unknown.append(name)
        i += 1

    open(dst, "w", encoding="utf-8").write("\n".join(out))

    print(f"读取: {src}")
    print(f"写出: {dst}")
    print(f"proxy-groups 段: 第 {start+1} 行 ~ 第 {end} 行")
    print(f"\n已挂图标 {len(hits)} 个:")
    for name, rel in hits:
        print(f"  + {name:<18} -> {rel}")
    if skipped:
        print(f"\n跳过（已有 icon）{len(skipped)} 个: {', '.join(skipped)}")
    if unknown:
        print(f"\n⚠ 未在映射表中找到的组 {len(unknown)} 个（未改动）:")
        for n in unknown:
            print(f"    {n}")
    print(f"\n原文件行数 {len(lines)} -> 新文件 {len(out)} 行（+{len(out)-len(lines)}）")


if __name__ == "__main__":
    main()
