# 日本 人口増減率マップ 2024

総務省の住民基本台帳データ（令和6年）をもとに、全国1,966市区町村の人口増減率をインタラクティブな地図で可視化するWebアプリです。

## デモ

GitHub Pagesでの公開後、以下のURLでアクセスできます：

```
https://<your-username>.github.io/<repository-name>/
```

---

## 使い方

### 地図の操作

| 操作 | 説明 |
|------|------|
| スクロール（ホイール） | 拡大・縮小 |
| ドラッグ | 地図の移動 |
| 市区町村にホバー | 詳細情報を左上パネルに表示 |
| `+` / `-` ボタン | 拡大・縮小（右上） |

### 色の見方

地図の色は**人口増減率**を表しています。

| 色 | 増減率 | 意味 |
|----|--------|------|
| 濃い青 | ＋3%以上 | 著しい人口増加 |
| 水色 | ＋1〜3% | 人口増加 |
| 薄い水色 | 0〜＋1% | 微増 |
| 薄い黄 | 0〜-1% | 微減 |
| 薄いオレンジ | -1〜-3% | 人口減少 |
| 橙赤 | -3〜-5% | 著しい人口減少 |
| 濃い赤 | -5%以下 | 急激な人口減少 |
| グレー | データなし | 境界データと一致しない地域 |

> **注意**: 増減率が±6%を超える自治体（能登半島地震の影響を受けた輪島市・珠洲市など）は色が飽和します。ホバーで正確な数値を確認してください。

### 表示データの切り替え（左下パネル）

地図左下の「表示データ」から3種類のデータを切り替えられます：

| 項目 | 説明 |
|------|------|
| **増減率（総合）** | 人口の総合的な増減率。転入出・出生・死亡をすべて含む |
| **自然増減率** | 出生数から死亡数を引いた増減率。少子化・高齢化の影響 |
| **社会増減率** | 転入数から転出数を引いた増減率。地域間移動の影響 |

### ホバー情報パネル（左上）

市区町村にマウスを当てると以下の情報が表示されます：

- 都道府県名・市区町村名
- 現在選択中のデータの増減率（色付き大文字）
- 総人口（2025年1月1日現在）
- 増減率・自然増減率・社会増減率の数値

---

## ローカルで実行する

```bash
git clone https://github.com/<your-username>/<repository-name>.git
cd <repository-name>
python3 -m http.server 8080
```

ブラウザで `http://localhost:8080` を開いてください。

> ※ `file://` プロトコルでは動作しません（JSON/GeoJSONの読み込みにHTTPが必要）。

---

## GitHub Pages へのデプロイ

1. GitHubにリポジトリを作成してpushする
2. リポジトリの **Settings → Pages** を開く
3. Source を **Deploy from a branch** に設定
4. Branch: `main`、Directory: `/ (root)` を選択して **Save**
5. 数分後に公開URLが表示される

---

## データソース・CSVの再変換

元データはCSVファイルで管理されています。CSVを更新した場合は以下を実行してください：

```bash
python3 scripts/build_data.py
```

`data/population.json` が再生成されます。

### データ出典

- **人口データ**: [総務省 住民基本台帳人口・世帯数及び人口動態](https://www.soumu.go.jp/main_sosiki/jichi_gyousei/daityo/jinkou_jinkoudoutai-setaisuu.html)（令和6年）
- **境界データ**: [国土数値情報](https://nlftp.mlit.go.jp/ksj/)（国土交通省） / [smartnews-smri/japan-topography](https://github.com/smartnews-smri/japan-topography)

---

## ファイル構成

```
map2locations/
├── index.html                  # メインアプリ
├── data/
│   ├── population.json         # 市区町村別人口データ（1,966件）
│   └── municipalities.geojson  # 市区町村境界データ
├── scripts/
│   └── build_data.py           # CSV→JSON変換スクリプト
└── 000892952 - 人口...csv       # 元データ（総務省）
```
