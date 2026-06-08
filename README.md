# WC26 Picks Data

世界杯 2026 比赛数据托管仓库。

本仓库通过 GitHub Pages 提供比赛数据 JSON 文件，供 WC26 Picks 应用使用。

## 数据结构

- `matches.json` - 比赛数据（自动更新）

## 数据来源

数据来自 [worldcup26.ir](https://worldcup26.ir/get/games) API，通过 GitHub Actions 每天自动更新。

## 使用方法

应用通过以下 URL 获取数据：

```
https://pangtongya.github.io/wc26picks-data/matches.json
```

## 自动更新

GitHub Actions 每天自动运行 `fetch-data.js` 脚本，从 worldcup26.ir 获取最新数据并推送到本仓库。
