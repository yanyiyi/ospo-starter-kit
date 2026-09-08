# 正體中文（zh-TW）在地化

這個目錄放的是翻譯工具與翻譯檔，不是文件內容本身。譯文本體在 `contents/zh-TW/`。
文體規範與術語表見 [`../docs/chinese-style-guide.md`](../docs/chinese-style-guide.md)。

翻譯以 `contents/ja/` 為原文（msgid），`contents/en/` 為參考語言，兩種校對介面二選一：

| 路徑 | 用途 |
|------|------|
| `po/` | gettext PO / POT，可直接匯入 Weblate。7 個元件、698 筆去重後字串。 |
| `ospo-starter-kit-zh-TW-translations.xlsx` | 試算表校對表。815 列（未去重），日文／英文／中文三欄並列。 |

兩者由同一套區塊切法產生，PO 的 `#: 檔名:序號` 與 xlsx 的「頁面 + 區塊」欄位對得起來，
可以混用：一批人用 Weblate，一批人用 Google 試算表。

## 腳本

| 腳本 | 做什麼 |
|------|--------|
| `mdblocks.py` | 共用的 Markdown 區塊切法（標題／段落／清單／表格／引用／註解／程式碼／分隔線）。 |
| `l10n_files.py` | 元件與檔案的對應表。要增減檔案或元件改這裡。 |
| `po_io.py` | 極簡 PO 讀寫。 |
| `markdown-to-po.py` | `contents/` → `po/`。改完 Markdown 後重跑，更新 POT 與各語言 PO。 |
| `po-to-markdown.py` | `po/zh_Hant/` → `contents/zh-TW/`。Weblate 交回譯文後跑這個。`--check` 只比對不寫檔。 |
| `build-translation-xlsx.py` | 重新產生 xlsx 校對表（需要 `openpyxl`）。 |

寫回時以 `contents/ja/` 的原檔為骨架，逐區塊換上譯文，所以空行、縮排、區塊順序一定與
日文原檔一致；PO 裡未翻譯的區塊會保留日文原文，缺漏看得見。目前 `po-to-markdown.py --check`
的結果與 `contents/zh-TW/` 逐位元組相同。

## 匯入 Weblate

一個元件（component）= 一個 `.pot` + 每語言一個 `.po`。7 個元件與檔案的對應見
`l10n_files.py`。建元件時的設定：

| 欄位 | 值 |
|------|-----|
| 檔案格式（File format） | gettext PO file |
| 檔案遮罩（File mask） | `l10n/po/*/<元件>.po`，例如 `l10n/po/*/policy-articles.po` |
| 新翻譯的範本（Template for new translations） | `l10n/po/<元件>.pot` |
| 單語基準檔（Monolingual base language file） | 留空（這是雙語 PO） |
| 來源語言（Source language） | Japanese (`ja`) |
| 次要語言（Secondary language，專案設定） | English — 校對時會顯示英文版當對照 |
| 授權（Translation license） | CC0-1.0 |

想一次建好 7 個元件，可以只建第一個，然後掛「元件探索（Component discovery）」擴充功能，
比對規則用：

```text
l10n/po/(?P<language>[^/]*)/(?P<component>[^/]*)\.po
```

### Weblate 交回譯文之後

Weblate 只會提交 `po/zh_Hant/*.po`，**不會**自動更新 `contents/zh-TW/`。合併它的 PR 之後
（或在 CI 裡）跑：

```bash
python3 l10n/po-to-markdown.py
```

Hosted Weblate 不允許自訂 script 擴充功能，所以這一步請放在 CI（對 Weblate 的 PR 跑
`--check`，合併後跑寫回）或由維護者手動執行。自架 Weblate 才能用「執行 script」擴充功能
直接串起來。

## 校對規則

1. 只改譯文，不要增刪區塊——`contents/zh-TW/` 的檔案集合與區塊數必須與 `contents/ja/`
   完全相同，PO 以 `檔名:序號` 對位，增刪區塊會讓整份對照錯行。
2. 標成 `no-wrap` 的區塊（程式碼、分隔線）多數照抄原文即可；但目錄樹裡的中文註解要翻。
3. `[公司名稱]`、`［公司名稱］` 這類佔位符整份文件要一致，否則使用者做全域取代時會漏掉。
4. 條號與 `a. b. c.` 項次代號不可調換，條文之間會互相引用。選用條文的全形 `【】` 沿用日文。
5. 有新增或修訂的術語，一併更新 `docs/chinese-style-guide.md` 的術語表。

同一句日文在不同檔案出現時，PO 會去重成一筆（例如各範本開頭那段給 OSPO 承辦人的註解，
20 幾個檔案共用一筆）。`markdown-to-po.py` 若發現同一句原文有兩種中文譯法會報錯，請先統一。
