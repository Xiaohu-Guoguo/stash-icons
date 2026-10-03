# 来源与许可声明（NOTICE）

本图标集是**聚合产物**，图片版权归各自品牌方所有。以下按来源逐项说明。

---

## 1. Qure Color —— 网站 / 功能图标主力

- 仓库：https://github.com/Koolson/Qure
- 作者：[@Koolson](https://github.com/Koolson)
- 许可：**仓库未附 LICENSE 文件**
- 本图标集中的角色：`icons/` 目录下的绝大部分站点与策略组图标，以及 `regions/` 全部地区代码徽标
- 说明：Qure 是目前 Clash / Stash / Quantumult X 生态事实上的标准图标集。
  **Stash 自带的 `default.yaml` 官方示例即引用 Qure 图标**，其兼容性与风格一致性已被广泛验证。
  但该仓库未声明开源许可证，因此：
  - **个人自用、自建私有仓库：没有问题**
  - **公开再分发、商用、打包进产品：存在版权风险，请自行评估或联系原作者获取授权**

## 2. simple-icons —— 补齐 Qure 缺口的矢量图标

- 仓库：https://github.com/simple-icons/simple-icons
- 许可：**CC0-1.0（公共领域贡献）**
- 本图标集角色：`icons/` 中约 40 个补充图标（知乎、小红书、百度、快手、支付宝、
  Reddit、WhatsApp、Claude、Binance 等）
- 处理方式：读取官方 SVG 路径，填入 simple-icons 数据中标注的品牌色，栅格化为 144×144 PNG
- 说明：CC0 允许自由使用与再分发。商标权仍归各品牌方，图标仅用于标识对应服务。

## 3. lipis/flag-icons —— 国旗

- 仓库：https://github.com/lipis/flag-icons
- 作者：Panayiotis Lipiridis
- 许可：**MIT**
- 本图标集角色：`flags/` 与 `flags-square/` 的全部国旗
- 处理方式：取 `flags/4x3/*.svg` 标准旗面矢量，经 `sips` 栅格化为 640×480，
  再裁切/遮罩为圆形与圆角方形，输出 144×144 PNG
- 说明：MIT 允许自由使用、修改、再分发，需保留版权声明（即本文件）。

## 4. 明确排除的来源

- **lipis/flag-icons 的 `1x1` 变体**：实测存在渲染缺陷
  （美国国旗星区被放大且丢失星点、沙特国旗出现异常黑块），已弃用。
- **站点 favicon / apple-touch-icon 抓取**：实测多数只有 16–57px，
  放大到 144px 明显模糊，且部分站点返回同一张占位图。为保证画质，未纳入主集，
  仅保留 `tools/add_icon.py` 供按需自助补充。

---

## 使用建议

| 场景 | 建议 |
|---|---|
| 个人自用、私有仓库 | 直接使用，无需额外处理 |
| 公开 GitHub 仓库 | 建议保留本 NOTICE，并注明 Qure 部分无许可证 |
| 商业用途 / 产品集成 | 建议剔除 Qure 部分，仅使用 simple-icons + flag-icons（许可干净），或联系 Qure 作者授权 |

## 品牌商标

所有品牌图标、名称、商标归各自权利人所有。本图标集仅用于在网络代理配置中标识对应服务，
不表示与任何品牌方存在关联、赞助或背书关系。
