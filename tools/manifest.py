# -*- coding: utf-8 -*-
"""
图标集清单（唯一数据源）
========================
改这里 → 重跑 `python3 tools/build.py` → 全套产物重新生成。

三个来源：
  QURE   : Koolson/Qure 的 Color 主题图标（社区事实标准，Stash 自带示例即用它）
  SI     : simple-icons（CC0-1.0），矢量、带官方品牌色，用于补齐 Qure 的缺口
  FLAGS  : lipis/flag-icons（MIT）的 4:3 标准旗面，栅格化后再裁成圆形/圆角方形
"""

# ---------------------------------------------------------------------------
# 1) Qure Color 图标
#    (Qure 文件名, 中文名, 分类)
# ---------------------------------------------------------------------------
QURE = [
    # ---- 策略组 / 功能（Stash proxy-groups 的 icon 最常用这一组）----
    ("Direct",             "直连",           "策略组"),
    ("Proxy",              "代理",           "策略组"),
    ("Reject",             "拒绝",           "策略组"),
    ("Final",              "兜底分流",       "策略组"),
    ("Global",             "全球",           "策略组"),
    ("Auto",               "自动选择",       "策略组"),
    ("Static",             "手动选择",       "策略组"),
    ("Available",          "故障转移",       "策略组"),
    ("Loop",               "负载均衡",       "策略组"),
    ("Speedtest",          "延迟测速",       "策略组"),
    ("Download",           "下载",           "策略组"),
    ("AdBlack",            "广告拦截",       "策略组"),
    ("Advertising",        "广告拦截(白)",   "策略组"),
    ("Hijacking",          "域名劫持",       "策略组"),
    ("Bypass",             "绕过",           "策略组"),
    ("Back",               "回国",           "策略组"),
    ("Area",               "地区",           "策略组"),
    ("Domestic",           "国内流量",       "策略组"),
    ("ForeignMedia",       "国外媒体",       "策略组"),
    ("DomesticMedia",      "国内媒体",       "策略组"),
    ("Media",              "媒体",           "策略组"),
    ("Game",               "游戏平台",       "策略组"),
    ("Streaming",          "国际流媒体",     "策略组"),
    ("StreamingCN",        "国内流媒体",     "策略组"),
    ("Unlock",             "解锁",           "策略组"),
    ("Music_Enhance",      "音乐解锁",       "策略组"),
    ("VIP",                "会员",           "策略组"),
    ("Server",             "服务器",         "策略组"),
    ("Airport",            "机场",           "策略组"),

    # ---- 苹果 ----
    ("Apple",              "苹果",           "苹果服务"),
    ("App_Store",          "App Store",      "苹果服务"),
    ("Apple_Music",        "Apple Music",    "苹果服务"),
    ("Apple_TV",           "Apple TV",       "苹果服务"),
    ("Apple_News",         "Apple News",     "苹果服务"),
    ("iCloud",             "iCloud",         "苹果服务"),
    ("Find_My",            "查找",           "苹果服务"),

    # ---- 谷歌 ----
    ("Google",             "谷歌",           "谷歌服务"),
    ("Gmail",              "Gmail",          "谷歌服务"),
    ("Google_Drive",       "谷歌云端硬盘",   "谷歌服务"),
    ("Google_Search",      "谷歌搜索",       "谷歌服务"),
    ("Google_Opinion_Rewards", "谷歌意见回报", "谷歌服务"),

    # ---- 微软 ----
    ("Microsoft",          "微软",           "微软服务"),
    ("Windows",            "Windows",        "微软服务"),
    ("Windows_11",         "Windows 11",     "微软服务"),
    ("OneDrive",           "OneDrive",       "微软服务"),
    ("Azure",              "Azure",          "微软服务"),
    ("Copilot",            "Copilot",        "微软服务"),
    ("Xbox",               "Xbox",           "微软服务"),

    # ---- 人工智能 / 开发 ----
    ("ChatGPT",            "ChatGPT",        "人工智能"),
    ("GitHub",             "GitHub",         "开发工具"),
    ("GitHub_Letter",      "GitHub 文字版",  "开发工具"),
    ("Notion",             "Notion",         "开发工具"),
    ("Cloudflare",         "Cloudflare",     "云服务"),

    # ---- 社交 ----
    ("Facebook",           "Facebook",       "社交媒体"),
    ("Instagram",          "Instagram",      "社交媒体"),
    ("Twitter",            "Twitter",        "社交媒体"),
    ("X",                  "X",              "社交媒体"),
    ("TikTok",             "TikTok",         "社交媒体"),
    ("Telegram",           "Telegram",       "社交媒体"),
    ("Telegram_X",         "Telegram X",     "社交媒体"),
    ("Linkedin",           "领英",           "社交媒体"),
    ("Discord",            "Discord",        "社交媒体"),
    ("Clubhouse",          "Clubhouse",      "社交媒体"),
    ("Line",               "LINE",           "社交媒体"),
    ("Kakao",              "KakaoTalk",      "社交媒体"),
    ("WeChat",             "微信",           "国内站点"),

    # ---- 国内站点 ----
    ("Weibo",              "微博",           "国内站点"),
    ("bilibili",           "哔哩哔哩",       "国内站点"),
    ("iQIYI",              "爱奇艺",         "国内站点"),
    ("Taobao",             "淘宝",           "国内站点"),
    ("Alibaba",            "阿里巴巴",       "国内站点"),
    ("Netease_Music",      "网易云音乐",     "国内站点"),
    ("QQ",                 "QQ",             "国内站点"),

    # ---- 音乐 ----
    ("Spotify",            "Spotify",        "音乐"),
    ("deezer",             "Deezer",         "音乐"),
    ("TIDAL",              "TIDAL",          "音乐"),
    ("Pandora",            "Pandora",        "音乐"),
    ("KKBOX",              "KKBOX",          "音乐"),
    ("JOOX",               "JOOX",           "音乐"),
    ("YouTube_Music",      "YouTube Music",  "音乐"),

    # ---- 流媒体 / 视频 ----
    ("YouTube",            "YouTube",        "流媒体"),
    ("Netflix",            "Netflix",        "流媒体"),
    ("Disney+",            "Disney+",        "流媒体"),
    ("HBO",                "HBO",            "流媒体"),
    ("HBO_Max",            "HBO Max",        "流媒体"),
    ("HBO_GO",             "HBO GO",         "流媒体"),
    ("Prime_Video",        "Prime Video",    "流媒体"),
    ("Hulu",               "Hulu",           "流媒体"),
    ("Peacock",            "Peacock",        "流媒体"),
    ("Paramount",          "Paramount+",     "流媒体"),
    ("Star+",              "Star+",          "流媒体"),
    ("STARZ",              "STARZ",          "流媒体"),
    ("ESPN+",              "ESPN+",          "流媒体"),
    ("DAZN",               "DAZN",           "流媒体"),
    ("Tubi",               "Tubi",           "流媒体"),
    ("discovery+",         "discovery+",     "流媒体"),
    ("Vimeo",              "Vimeo",          "流媒体"),

    # ---- 游戏 ----
    ("Steam",              "Steam",          "游戏"),
    ("PlayStation",        "PlayStation",    "游戏"),
    ("Nintendo",           "任天堂",         "游戏"),
    ("Epic_Games",         "Epic Games",     "游戏"),
    ("League_of_Legends",  "英雄联盟",       "游戏"),
    ("Twitch",             "Twitch",         "直播"),

    # ---- 亚洲媒体 ----
    ("niconico",           "niconico",       "亚洲媒体"),
    ("AbemaTV",            "AbemaTV",        "亚洲媒体"),
    ("AfreecaTV",          "AfreecaTV",      "亚洲媒体"),
    ("Bahamut",            "巴哈姆特",       "亚洲媒体"),
    ("KKTV",               "KKTV",           "亚洲媒体"),
    ("Viu",                "Viu",            "亚洲媒体"),
    ("ViuTV",              "ViuTV",          "亚洲媒体"),
    ("WeTV",               "腾讯视频 WeTV",  "亚洲媒体"),

    # ---- 欧美电视 ----
    ("BBC_iPlayer",        "BBC iPlayer",    "欧美电视"),
    ("ITV",                "ITV",            "欧美电视"),
    ("My5",                "My5",            "欧美电视"),
    ("All4",               "Channel 4",      "欧美电视"),
    ("FOX",                "FOX",            "欧美电视"),
    ("NBC",                "NBC",            "欧美电视"),
    ("NBA",                "NBA",            "欧美电视"),
    ("PBS",                "PBS",            "欧美电视"),
    ("Yahoo",              "Yahoo",          "欧美电视"),

    # ---- 电商 / 支付 ----
    ("Amazon",             "亚马逊",         "电商支付"),
    ("PayPal",             "PayPal",         "电商支付"),

    # ---- 媒体服务器 ----
    ("Emby",               "Emby",           "媒体服务器"),
    ("Infuse",             "Infuse",         "媒体服务器"),
    ("TestFlight",         "TestFlight",     "开发工具"),
]

# ---------------------------------------------------------------------------
# 2) simple-icons 补充（CC0-1.0）
#    (输出文件名, simple-icons 标题, 中文名, 分类)
# ---------------------------------------------------------------------------
SI = [
    # ---- 国内站点（Qure 缺失的主力）----
    ("Zhihu",          "Zhihu",               "知乎",         "国内站点"),
    ("Xiaohongshu",    "Xiaohongshu",         "小红书",       "国内站点"),
    ("Baidu",          "Baidu",               "百度",         "国内站点"),
    ("Kuaishou",       "Kuaishou",            "快手",         "国内站点"),
    ("Douban",         "Douban",              "豆瓣",         "国内站点"),
    ("Meituan",        "Meituan",             "美团",         "国内站点"),
    ("Alipay",         "Alipay",              "支付宝",       "电商支付"),
    ("Xiaomi",         "Xiaomi",              "小米",         "国内站点"),
    ("Huawei",         "Huawei",              "华为",         "国内站点"),
    ("Trip",           "Trip.com",            "携程",         "国内站点"),

    # ---- 国际社交（Qure 缺失）----
    ("WhatsApp",       "WhatsApp",            "WhatsApp",     "社交媒体"),
    ("Reddit",         "Reddit",              "Reddit",       "社交媒体"),
    ("Pinterest",      "Pinterest",           "Pinterest",    "社交媒体"),
    ("Snapchat",       "Snapchat",            "Snapchat",     "社交媒体"),
    ("Signal",         "Signal",              "Signal",       "社交媒体"),

    # ---- 工具 / 知识 ----
    ("Wikipedia",      "Wikipedia",           "维基百科",     "知识"),
    ("Zoom",           "Zoom",                "Zoom",         "办公"),
    ("Figma",          "Figma",               "Figma",        "开发工具"),
    ("Dropbox",        "Dropbox",             "Dropbox",      "云服务"),
    ("Bitwarden",      "Bitwarden",           "Bitwarden",    "隐私工具"),
    ("OnePassword",    "1Password",           "1Password",    "隐私工具"),

    # ---- 人工智能 ----
    ("Claude",         "Claude",              "Claude",       "人工智能"),
    ("Anthropic",      "Anthropic",           "Anthropic",    "人工智能"),
    ("Perplexity",     "Perplexity",          "Perplexity",   "人工智能"),
    ("HuggingFace",    "Hugging Face",        "Hugging Face", "人工智能"),

    # ---- 加密货币 / 金融 ----
    ("Binance",        "Binance",             "币安",         "加密货币"),
    ("Coinbase",       "Coinbase",            "Coinbase",     "加密货币"),
    ("OKX",            "OKX",                 "OKX",          "加密货币"),
    ("Stripe",         "Stripe",              "Stripe",       "电商支付"),
    ("Wise",           "Wise",                "Wise",         "电商支付"),

    # ---- 隐私 / 网络 ----
    ("ExpressVPN",     "ExpressVPN",          "ExpressVPN",   "隐私工具"),
    ("NordVPN",        "NordVPN",             "NordVPN",      "隐私工具"),
    ("ProtonMail",     "Proton Mail",         "Proton Mail",  "隐私工具"),

    # ---- 成人（Qure 已有 Pornhub，这里补齐 OnlyFans）----
    ("OnlyFans",       "OnlyFans",            "OnlyFans",     "成人"),

    # ---- 系统 / 硬件 / 开发 ----
    ("Docker",         "Docker",              "Docker",       "开发工具"),
    ("Ubuntu",         "Ubuntu",              "Ubuntu",       "操作系统"),
    ("Debian",         "Debian",              "Debian",       "操作系统"),
    ("RedHat",         "Red Hat",             "Red Hat",      "操作系统"),
    ("NVIDIA",         "NVIDIA",              "NVIDIA",       "硬件"),
    ("AMD",            "AMD",                 "AMD",          "硬件"),
    ("Intel",          "Intel",               "Intel",        "硬件"),
    ("Qualcomm",       "Qualcomm",            "高通",         "硬件"),
    ("Shopify",        "Shopify",             "Shopify",      "电商支付"),
    ("WordPress",      "WordPress",           "WordPress",    "开发工具"),
    ("Crunchyroll",    "Crunchyroll",         "Crunchyroll",  "流媒体"),
    ("Duolingo",       "Duolingo",            "多邻国",       "教育"),
    ("Coursera",       "Coursera",            "Coursera",     "教育"),
    ("Udemy",          "Udemy",               "Udemy",        "教育"),
    ("Starbucks",      "Starbucks",           "星巴克",       "生活"),
    ("KFC",            "KFC",                 "肯德基",       "生活"),
]

# ---------------------------------------------------------------------------
# 3) Qure 的地区代码徽标（圆角方形 + 双字母，非真实国旗）
# ---------------------------------------------------------------------------
REGIONS = [
    ("CN", "中国大陆"), ("HK", "香港"), ("TW", "台湾"), ("MO", "澳门"),
    ("JP", "日本"), ("KR", "韩国"), ("SG", "新加坡"), ("MY", "马来西亚"),
    ("TH", "泰国"), ("PH", "菲律宾"), ("IN", "印度"), ("AU", "澳大利亚"),
    ("US", "美国"), ("CA", "加拿大"), ("BR", "巴西"),
    ("UK", "英国"), ("DE", "德国"), ("FR", "法国"), ("RU", "俄罗斯"),
    ("FI", "芬兰"), ("UA", "乌克兰"), ("TR", "土耳其"),
    ("EG", "埃及"), ("EU", "欧盟"), ("UN", "联合国"),
]

# ---------------------------------------------------------------------------
# 4) 国旗（ISO 3166-1 alpha-2，小写）
#    (代码, 中文名, 英文名, 区域)
# ---------------------------------------------------------------------------
FLAGS = [
    # 东亚 / 东南亚 / 南亚
    ("cn", "中国",         "China",          "亚洲"),
    ("hk", "香港",         "Hong Kong",      "亚洲"),
    ("tw", "台湾",         "Taiwan",         "亚洲"),
    ("mo", "澳门",         "Macao",          "亚洲"),
    ("jp", "日本",         "Japan",          "亚洲"),
    ("kr", "韩国",         "South Korea",    "亚洲"),
    ("sg", "新加坡",       "Singapore",      "亚洲"),
    ("my", "马来西亚",     "Malaysia",       "亚洲"),
    ("th", "泰国",         "Thailand",       "亚洲"),
    ("vn", "越南",         "Vietnam",        "亚洲"),
    ("ph", "菲律宾",       "Philippines",    "亚洲"),
    ("id", "印度尼西亚",   "Indonesia",      "亚洲"),
    ("in", "印度",         "India",          "亚洲"),
    ("pk", "巴基斯坦",     "Pakistan",       "亚洲"),
    ("bd", "孟加拉国",     "Bangladesh",     "亚洲"),
    ("lk", "斯里兰卡",     "Sri Lanka",      "亚洲"),
    ("np", "尼泊尔",       "Nepal",          "亚洲"),
    ("kh", "柬埔寨",       "Cambodia",       "亚洲"),
    ("mm", "缅甸",         "Myanmar",        "亚洲"),
    ("mn", "蒙古",         "Mongolia",       "亚洲"),

    # 北美 / 南美
    ("us", "美国",         "United States",  "美洲"),
    ("ca", "加拿大",       "Canada",         "美洲"),
    ("mx", "墨西哥",       "Mexico",         "美洲"),
    ("br", "巴西",         "Brazil",         "美洲"),
    ("ar", "阿根廷",       "Argentina",      "美洲"),
    ("cl", "智利",         "Chile",          "美洲"),
    ("pe", "秘鲁",         "Peru",           "美洲"),
    ("co", "哥伦比亚",     "Colombia",       "美洲"),
    ("ve", "委内瑞拉",     "Venezuela",      "美洲"),
    ("pa", "巴拿马",       "Panama",         "美洲"),

    # 欧洲
    ("gb", "英国",         "United Kingdom", "欧洲"),
    ("ie", "爱尔兰",       "Ireland",        "欧洲"),
    ("fr", "法国",         "France",         "欧洲"),
    ("de", "德国",         "Germany",        "欧洲"),
    ("nl", "荷兰",         "Netherlands",    "欧洲"),
    ("be", "比利时",       "Belgium",        "欧洲"),
    ("lu", "卢森堡",       "Luxembourg",     "欧洲"),
    ("ch", "瑞士",         "Switzerland",    "欧洲"),
    ("at", "奥地利",       "Austria",        "欧洲"),
    ("it", "意大利",       "Italy",          "欧洲"),
    ("es", "西班牙",       "Spain",          "欧洲"),
    ("pt", "葡萄牙",       "Portugal",       "欧洲"),
    ("gr", "希腊",         "Greece",         "欧洲"),
    ("se", "瑞典",         "Sweden",         "欧洲"),
    ("no", "挪威",         "Norway",         "欧洲"),
    ("dk", "丹麦",         "Denmark",        "欧洲"),
    ("fi", "芬兰",         "Finland",        "欧洲"),
    ("is", "冰岛",         "Iceland",        "欧洲"),
    ("pl", "波兰",         "Poland",         "欧洲"),
    ("cz", "捷克",         "Czechia",        "欧洲"),
    ("sk", "斯洛伐克",     "Slovakia",       "欧洲"),
    ("hu", "匈牙利",       "Hungary",        "欧洲"),
    ("ro", "罗马尼亚",     "Romania",        "欧洲"),
    ("bg", "保加利亚",     "Bulgaria",       "欧洲"),
    ("hr", "克罗地亚",     "Croatia",        "欧洲"),
    ("rs", "塞尔维亚",     "Serbia",         "欧洲"),
    ("si", "斯洛文尼亚",   "Slovenia",       "欧洲"),
    ("ee", "爱沙尼亚",     "Estonia",        "欧洲"),
    ("lv", "拉脱维亚",     "Latvia",         "欧洲"),
    ("lt", "立陶宛",       "Lithuania",      "欧洲"),
    ("ua", "乌克兰",       "Ukraine",        "欧洲"),
    ("by", "白俄罗斯",     "Belarus",        "欧洲"),
    ("ru", "俄罗斯",       "Russia",         "欧洲"),
    ("tr", "土耳其",       "Turkey",         "欧洲"),
    ("md", "摩尔多瓦",     "Moldova",        "欧洲"),
    ("cy", "塞浦路斯",     "Cyprus",         "欧洲"),
    ("mt", "马耳他",       "Malta",          "欧洲"),

    # 大洋洲
    ("au", "澳大利亚",     "Australia",      "大洋洲"),
    ("nz", "新西兰",       "New Zealand",    "大洋洲"),

    # 非洲
    ("za", "南非",         "South Africa",   "非洲"),
    ("eg", "埃及",         "Egypt",          "非洲"),
    ("ng", "尼日利亚",     "Nigeria",        "非洲"),
    ("ke", "肯尼亚",       "Kenya",          "非洲"),
    ("ma", "摩洛哥",       "Morocco",        "非洲"),
    ("tz", "坦桑尼亚",     "Tanzania",       "非洲"),
    ("gh", "加纳",         "Ghana",          "非洲"),

    # 中东 / 中亚
    ("sa", "沙特阿拉伯",   "Saudi Arabia",   "中东"),
    ("ae", "阿联酋",       "United Arab Emirates", "中东"),
    ("il", "以色列",       "Israel",         "中东"),
    ("qa", "卡塔尔",       "Qatar",          "中东"),
    ("kw", "科威特",       "Kuwait",         "中东"),
    ("ir", "伊朗",         "Iran",           "中东"),
    ("iq", "伊拉克",       "Iraq",           "中东"),
    ("jo", "约旦",         "Jordan",         "中东"),
    ("lb", "黎巴嫩",       "Lebanon",        "中东"),
    ("kz", "哈萨克斯坦",   "Kazakhstan",     "中亚"),
    ("uz", "乌兹别克斯坦", "Uzbekistan",     "中亚"),

    # 超国家
    ("eu", "欧盟",         "European Union", "超国家"),
    ("un", "联合国",       "United Nations", "超国家"),
]

# ---------------------------------------------------------------------------
# 5) 输出文件名 / 集合元信息
# ---------------------------------------------------------------------------
SET_NAME = "Stash 彩色图标集"
SET_NAME_EN = "Stash Color Icons"
SET_DESC = ("主流国内外网站彩色图标（Qure + simple-icons）"
            "＋ 75 国国旗（圆形 / 圆角方形）。含中文别名与分类索引。")
