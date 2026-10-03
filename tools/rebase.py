#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把图标集切换到你的托管地址
==========================
图标集 JSON 里必须是**绝对 URL**（Stash 只能填 URL）。换托管方式时不用重新构建图片，
跑一下这个脚本即可：

    python3 tools/rebase.py --base-url https://cdn.jsdelivr.net/gh/你的用户名/你的仓库@main/

会重写：icons.json / icons-zh.json / icons-index.json，并重新生成 stash/*.yaml
"""
import argparse
import json
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def q(name):
    return urllib.parse.quote(name, safe="")


# 常用策略组 → 图标 key 的默认映射（可自行增删）
GROUP_ICONS = [
    ("🚀 节点选择",   "Proxy"),
    ("♻️ 自动选择",   "Auto"),
    ("🔯 故障转移",   "Available"),
    ("🔮 负载均衡",   "Loop"),
    ("🎯 全球直连",   "Direct"),
    ("🛑 广告拦截",   "AdBlack"),
    ("🐟 漏网之鱼",   "Final"),
    ("🌍 国外媒体",   "ForeignMedia"),
    ("🎬 国际流媒体", "Streaming"),
    ("📺 国内媒体",   "DomesticMedia"),
    ("🎵 音乐解锁",   "Music_Enhance"),
    ("🤖 人工智能",   "ChatGPT"),
    ("📱 电报消息",   "Telegram"),
    ("🎮 游戏平台",   "Game"),
    ("💳 支付服务",   "PayPal"),
    ("🍎 苹果服务",   "Apple"),
    ("🔍 谷歌服务",   "Google"),
    ("🪟 微软服务",   "Microsoft"),
    ("🐙 开发工具",   "GitHub"),
    ("🇨🇳 国内网站",  "Domestic"),
]

FLAG_GROUPS = [
    ("🇭🇰 香港节点", "hk"),
    ("🇹🇼 台湾节点", "tw"),
    ("🇯🇵 日本节点", "jp"),
    ("🇰🇷 韩国节点", "kr"),
    ("🇸🇬 新加坡节点", "sg"),
    ("🇺🇸 美国节点", "us"),
    ("🇬🇧 英国节点", "gb"),
    ("🇩🇪 德国节点", "de"),
]


def yaml_groups(base, icon_dir="icons", flag_dir="flags", sample=True):
    L = []
    L.append("# Stash 策略组图标片段")
    L.append(f"# 生成自图标集，base-url = {base}")
    L.append("# 用法：把下面每个策略组的 icon 字段复制到你自己的 proxy-groups 里")
    L.append("")
    L.append("proxy-groups:")
    for name, key in (GROUP_ICONS if sample else []):
        L.append(f"  - name: {name}")
        L.append("    type: select")
        L.append(f"    icon: {base}{icon_dir}/{q(key + '.png')}")
        L.append("    proxies: [DIRECT, REJECT]")
    if sample:
        L.append("")
        L.append("  # ---- 按地区分组的节点（国旗图标）----")
    for name, code in (FLAG_GROUPS if sample else []):
        L.append(f"  - name: {name}")
        L.append("    type: url-test")
        L.append(f"    icon: {base}{flag_dir}/{code}.png")
        L.append("    proxies: []")
        L.append("    interval: 300")
    L.append("")
    return "\n".join(L)


def yaml_override(base):
    return f"""# Stash 覆写配置示例（Override）
# 放到 iCloud/Stash/Override 或 App 内「覆写」目录，即可给订阅里的策略组自动挂图标。
# 文档：https://stash.wiki/configuration/proxy-group-icon
#
# base-url = {base}

proxy-groups:
  - name: "🚀 节点选择"
    type: select
    icon: {base}icons/{q("Proxy.png")}
    proxies:
      - "♻️ 自动选择"
      - DIRECT

  - name: "♻️ 自动选择"
    type: url-test
    icon: {base}icons/{q("Auto.png")}
    interval: 300

  - name: "🌍 国外媒体"
    type: select
    icon: {base}icons/{q("ForeignMedia.png")}
    proxies:
      - "🚀 节点选择"
      - DIRECT

  - name: "🛑 广告拦截"
    type: select
    icon: {base}icons/{q("AdBlack.png")}
    proxies:
      - REJECT
      - DIRECT
"""


def yaml_clash(base):
    return f"""# Clash Meta / mihomo 示例（DashBoard 支持 proxy-group 的 icon 字段）
# base-url = {base}

proxy-groups:
  - name: "🚀 节点选择"
    type: select
    icon: {base}icons/{q("Proxy.png")}
    proxies: [DIRECT]

  - name: "🇭🇰 香港节点"
    type: url-test
    icon: {base}flags/hk.png
    url: http://www.gstatic.com/generate_204
    interval: 300
    tolerance: 50

  - name: "🇺🇸 美国节点"
    type: url-test
    icon: {base}flags/us.png
    url: http://www.gstatic.com/generate_204
    interval: 300
    tolerance: 50
"""


def rebase(base):
    if not base.endswith("/"):
        base += "/"
    n = 0
    for fn in ("icons.json", "icons-zh.json", "icons-index.json"):
        p = os.path.join(ROOT, fn)
        if not os.path.exists(p):
            print(f"  跳过（不存在）: {fn}")
            continue
        data = json.load(open(p, encoding="utf-8"))

        def fix(u):
            # 先解码（兼容历史遗留的 icons%2Fxxx 写法），定位目录标记后按段重新编码
            dec = urllib.parse.unquote(u)
            for marker in ("/icons/", "/flags-square/", "/flags/", "/regions/"):
                i = dec.find(marker)
                if i != -1:
                    rel = dec[i + 1:]
                    return base + "/".join(q(x) for x in rel.split("/"))
            return u

        if "icons" in data and isinstance(data["icons"], list):
            for it in data["icons"]:
                it["url"] = fix(it["url"])
        for k in ("sites", "flags", "regions"):
            for it in data.get(k, []) or []:
                for uk in ("url", "square_url"):
                    if uk in it:
                        it[uk] = fix(it[uk])
        if "base_url" in data:
            data["base_url"] = base
        json.dump(data, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"  ✓ {fn}")
        n += 1

    sd = os.path.join(ROOT, "stash")
    os.makedirs(sd, exist_ok=True)
    open(os.path.join(sd, "icon-groups.yaml"), "w", encoding="utf-8").write(yaml_groups(base))
    open(os.path.join(sd, "override-example.yaml"), "w", encoding="utf-8").write(yaml_override(base))
    open(os.path.join(sd, "clash-meta-example.yaml"), "w", encoding="utf-8").write(yaml_clash(base))
    print("  ✓ stash/icon-groups.yaml")
    print("  ✓ stash/override-example.yaml")
    print("  ✓ stash/clash-meta-example.yaml")
    print(f"\n完成，共更新 {n} 个 JSON。新的图标集地址：\n  {base}icons.json")
    print(f"  {base}icons-zh.json   （中文名优先，方便在 Stash 里搜中文）")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", required=True,
                    help="例: https://cdn.jsdelivr.net/gh/用户名/仓库@main/")
    a = ap.parse_args()
    print(f"切换到 base-url: {a.base_url}\n")
    rebase(a.base_url)


if __name__ == "__main__":
    main()
