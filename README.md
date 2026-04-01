# 井下敬翔 研究者ホームページ — セットアップガイド

## ファイル構成

```
your-website/
├── index.html      ← メインサイト（公開ページ）
├── admin.html      ← 管理画面（自分だけが使う）
├── photo.jpg       ← ★ 写真をここに置く（後で追加OK）
└── README.md
```

---

## 1. 写真を設定する

プロフィール写真を `photo.jpg`（または `photo.png`）という名前で、
`index.html` と同じフォルダに置くだけで自動で表示されます。

---

## 2. 管理画面の使い方

ブラウザで `admin.html` を開く（またはダブルクリック）

**初期パスワード: `keito2024`**（設定画面から変更できます）

### 管理できること
| 機能 | 説明 |
|------|------|
| 📢 News | お知らせを追加・削除 |
| ✍️ Column | 研究コラムを執筆・公開 |
| 📄 Publications | 論文を追加・管理 |
| 🏆 Awards | 受賞歴を追加・管理 |
| 💰 Grants | 研究資金を追加・管理 |
| 🎓 Activities | 査読・委員・講演を管理 |
| ⚙️ Settings | パスワード変更・フォーム設定・データ管理 |

### データの保存について
- データはブラウザのlocalStorageに保存されます
- 同じPC・ブラウザで管理する限り、データは保持されます
- **バックアップ推奨**: Settings > 「データをエクスポート」でJSONファイルに保存できます

---

## 3. お問い合わせフォームを実際に動かす

1. [Formspree.io](https://formspree.io) で無料アカウント作成
2. 「New Form」でフォームを作成し、URLをコピー（例: `https://formspree.io/f/xabcdefg`）
3. admin.html > Settings > Formspree URL に貼り付けて保存

---

## 4. インターネットに公開する方法（無料）

### 方法A: GitHub + Netlify（推奨・自動デプロイ）

1. [GitHub.com](https://github.com) でアカウント作成
2. 新しいリポジトリを作成（例: `keito-website`）
3. ファイルをアップロード（index.html, admin.html）
4. [Netlify.com](https://netlify.com) でアカウント作成
5. 「Import from Git」でGitHubリポジトリを連携
6. 自動的にURLが発行される（例: `https://keito-inoshita.netlify.app`）

**ファイルを更新するたびに**: GitHubにアップロードすれば自動でサイトが更新されます。

### 方法B: Netlify Drop（最も簡単）

1. [Netlify Drop](https://app.netlify.com/drop) を開く
2. フォルダをドラッグ＆ドロップ → 即座に公開URL発行
3. 更新時は再度ドロップするだけ

---

## 5. researchmapとの連携

論文数はresearchmap.jp/keito_inoshita から自動取得（JavaScriptで実行時に取得）。
researchmapを更新すると、次回ページを開いたときに論文数が自動更新されます。

Google Scholarのプロフィールページを設定すると、Contactページのリンクが有効になります。

---

## 注意事項

- `admin.html` はパスワードで保護されていますが、ローカルファイルのため他人がアクセスできる環境（共有PC等）では注意してください
- データはブラウザのlocalStorageに保存されるため、ブラウザを変えるか「データをクリア」するとリセットされます
- 定期的にSettings > 「データをエクスポート」でバックアップを取ることを推奨します
