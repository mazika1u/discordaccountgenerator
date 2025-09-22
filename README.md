# Discord Account Creator

使えるかは不明

⚠️ **重要な注意事項**

このリポジトリは **discordの規約に違反します、使用は自己責任** 

---

## 📌 概要

pw指定可能、proxy使用可能

- ランダムなユーザー名の生成
- ランダムな生年月日（18歳以上）の生成
- 設定ファイルからのpw・proxy読み込み
- 複数スレッドによる並列処理
- アカウント情報をファイルに保存

---

## ⚙️ 必要環境

- Python 3.8 以上
- `requests` ライブラリ
- `concurrent.futures`（標準ライブラリ）
- 任意で `proxy.txt` と `pass.txt` を用意可能

```bash
pip install requests
