# 井下敬翔 研究者ホームページ

## ファイル構成

```
keito-website/
├── index.html                        ← メインサイト
├── admin.html                        ← 管理画面（パスワード保護）
├── photo.jpg                         ← ★ 写真をここに置く
├── researchmap_data.json             ← GitHub Actionsが自動生成（触らない）
├── scripts/
│   └── fetch_researchmap.py          ← researchmap取得スクリプト
└── .github/
    └── workflows/
        └── sync-researchmap.yml      ← 毎朝自動実行

```

---

## データの仕組み

| データ種別 | 保存場所 | 更新方法 |
|-----------|---------|---------|
| researchmap の業績・受賞・資金等 | `researchmap_data.json` | GitHub Actionsが毎朝自動取得 |
| 手動追加の業績・お知らせ等 | ブラウザのlocalStorage (`ki_manual_*`) | admin.html から入力 |
| サイト設定（Scholar URL等） | localStorage (`ki_settings`) | admin.html > Settings |

**手動追加データはresearchmapの同期で絶対に消えません。** 別のキーで完全に分離しています。

---

## 写真の設定

`photo.jpg`（または `photo.png`）を `index.html` と同じフォルダに置くだけ。

---

## 管理画面

`admin.html` をブラウザで開く → パスワード **`keito2024`**（Settings から変更可）

### 各パネルの役割
| パネル | 説明 |
|--------|------|
| Dashboard | 同期状況の確認・クイックアクション |
| News | お知らせを追加・削除（手動） |
| Column | 研究コラムを執筆・公開（手動） |
| Publications | researchmap非公開の論文を手動追加 |
| Awards | 手動で受賞を追加（RM取得分も参照可） |
| Grants | 手動で研究課題を追加（RM取得分も参照可） |
| Activities | 査読・委員・講演を手動追加 |
| Settings | パスワード変更・フォーム・Scholar・CV設定 |

---

## GitHub Actions の設定

GitHubにアップロード後、以下を設定します：

1. GitHubリポジトリ → **Settings → Actions → General**
2. **Workflow permissions** → **Read and write permissions** を選択 → Save

これで毎朝 JST 5:00 に自動でresearchmapのデータが取得・更新されます。

**手動で今すぐ実行したい場合：**
GitHubリポジトリ → **Actions → Sync researchmap → Run workflow**

---

## Formspree（お問い合わせフォーム）設定

1. [formspree.io](https://formspree.io) で無料登録
2. New Form → メールアドレスを入力 → URL をコピー
3. admin.html > Settings > Formspree URL に貼り付けて保存

---

## Netlify 公開手順

1. GitHubにファイルを全てアップロード
2. [netlify.com](https://netlify.com) → Sign up with GitHub
3. Add new site → Import from GitHub → リポジトリを選択 → Deploy
4. 発行されたURLでアクセス可能に

---

## バックアップ

admin.html > Settings > 「エクスポート (JSON)」で手動追加データをバックアップできます。
定期的に実行することを推奨します。
