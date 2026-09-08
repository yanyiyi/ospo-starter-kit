# 正體中文（zh-TW）在地化

這個目錄放的是翻譯工具與翻譯檔，不是文件內容本身。譯文本體在 `contents/zh-TW/`。
文體規範與術語表見 [`../docs/chinese-style-guide.md`](../docs/chinese-style-guide.md)。

翻譯以 `contents/ja/` 為原文（msgid），`contents/en/` 為參考語言，兩種校對介面二選一：

| 路徑 | 用途 |
|------|------|
| `po/` | gettext PO / POT，可直接匯入 Weblate。7 個組件、698 筆去重後字串。 |
| `build-translation-xlsx.py` 產生的 xlsx | 試算表校對表（不進版控，需要時再產）。815 列（未去重），日文／英文／中文三欄並列。 |

兩者由同一套區塊切法產生，PO 的 `#: 檔名:序號` 與 xlsx 的「頁面 + 區塊」欄位對得起來，
可以混用：一批人用 Weblate，一批人用 Google 試算表。

用詞：這份文件講的「組件」是 Weblate 的 component（介面中譯就是「組件」）。文件內容裡的
component（SBOM 的軟體元件）依術語表仍譯「元件」，兩者是不同概念。

## 腳本

| 腳本 | 做什麼 |
|------|--------|
| `mdblocks.py` | 共用的 Markdown 區塊切法（標題／段落／清單／表格／引用／註解／程式碼／分隔線）。 |
| `l10n_files.py` | 組件與檔案的對應表。要增減檔案或組件改這裡。 |
| `po_io.py` | 極簡 PO 讀寫。 |
| `markdown-to-po.py` | `contents/` → `po/`。改完 Markdown 後重跑，更新 POT 與各語言 PO。 |
| `po-to-markdown.py` | `po/zh_Hant/` → `contents/zh-TW/`。Weblate 交回譯文後跑這個。`--check` 只比對不寫檔。 |
| `build-translation-xlsx.py` | 重新產生 xlsx 校對表（需要 `openpyxl`）。 |

寫回時以 `contents/ja/` 的原檔為骨架，逐區塊換上譯文，所以空行、縮排、區塊順序一定與
日文原檔一致；PO 裡未翻譯的區塊會保留日文原文，缺漏看得見。目前 `po-to-markdown.py --check`
的結果與 `contents/zh-TW/` 逐位元組相同。

## 匯入 Weblate（translate.codeberg.org）

Codeberg Translate 只接受**放在 Codeberg 上的儲存庫**，而本專案的 remote 目前都在 GitHub，
所以要先把分支推到 Codeberg：

```bash
git remote add codeberg git@codeberg.org:<你的帳號>/ospo-starter-kit.git
git push -u codeberg main
```

Codeberg 的「pull mirror」不能用——鏡像是唯讀的，Weblate 需要往回推。校對完成後再從
Codeberg 這份開 PR 回 GitHub 的 upstream。

### 1. 建專案

用 Codeberg 帳號登入 <https://translate.codeberg.org/>，右上 **+** → **Add new translation
project**：

| 欄位 | 值 |
|------|-----|
| Project name（專案名稱） | OSPO Starter Kit |
| URL slug（URL 代稱） | `ospo-starter-kit` |
| Project website（專案網站） | Codeberg 儲存庫網址 |
| Translation instructions（翻譯說明） | `docs/chinese-style-guide.md` 的網址 |

### 2. 建第一個組件

**Add new translation component**。貼上儲存庫網址後 Weblate 會掃描並列出找到的翻譯檔，
可以從清單挑，不必手打：

| 欄位 | 值 |
|------|-----|
| Component name（組件名稱） | Policy articles |
| URL slug（URL 代稱） | `policy-articles` |
| Source code repository（原始碼儲存庫） | `git@codeberg.org:<你的帳號>/ospo-starter-kit.git`（要 Weblate 直接 push 就用 SSH 網址） |
| Repository branch（儲存庫分支） | `main` |
| File format（檔案格式） | gettext PO file |
| File mask（檔案遮罩） | `l10n/po/*/policy-articles.po` |
| Monolingual base language file（單語言基底語言檔案） | 留空（這是雙語 PO） |
| Template for new translations（新翻譯的範本） | `l10n/po/policy-articles.pot` |
| Edit base file（編輯基底檔案） | 不勾 |
| Source language（來源語言） | Japanese (`ja`) |
| Translation license（翻譯授權條款） | CC0-1.0 |

### 3. 其餘 6 個組件

介面的表單一次只能建一個，但不必手動建 7 次：掛 **Component discovery**（介面中譯
「組件探索」）附加元件，安裝當下就會把其餘的建出來，不用等下一次 push。

安裝位置要注意：**它只出現在「組件」的附加元件頁面，不在「專案」的附加元件頁面**
（Weblate 把它標記為 needs_component）。路徑是先點進組件（例如 `policy-articles`）→
**管理 Manage → 附加元件 Add-ons → 安裝**，網址長這樣：

```text
https://translate.codeberg.org/addons/ospo-starter-kit/policy-articles/
```

在專案層看到的清單會包含「更新 RESX 檔案」「格式化 Java properties 檔案」這類跟 PO 無關的
項目，卻沒有組件探索——那就是站在專案頁面的徵兆。欄位：

| 欄位 | 值 |
|------|-----|
| Regular expression to match translation files against（用來比對出翻譯檔案的正規表達式） | `l10n/po/(?P<language>[^/.]*)/(?P<component>[^/]*)\.po` |
| File format（檔案格式） | **gettext PO 檔案**（不要選「gettext PO 檔案（單語言）」） |
| Customize the component name（自訂組件名稱） | `{{ component }}` |
| Define the monolingual base filename（定義單語言的基礎檔案名稱） | **留空**（雙語 PO 沒有單語基底檔） |
| Define the base file for new translations（定義新翻譯的基礎檔案） | `l10n/po/{{ component }}.pot` |
| Language filter（語言篩選） | `^[^.]+$`（Weblate 預設值，**必填、不能留空**） |
| Remove components for inexistent files（移除無相關檔案的組件） | 看需求；勾了之後刪檔會連帶刪組件 |

比對規則會被 Weblate 補上 `^` 和 `$` 當完整比對，所以 `.pot` 不會被誤抓成翻譯檔。
「語言篩選」是必填欄位（留空會被驗證擋下），填 Weblate 的預設 `^[^.]+$` 就好——它的意思是
「語言代碼不含點」，我們的 `en`、`zh_Hant` 都符合，將來有人加 `ko` 也自動收得到。表單若有
「folder per language」之類的預設組態可挑，值幾乎一樣，只差我們的路徑多了 `l10n/po/` 前綴。

兩個「基礎檔案」欄位的中文標籤很像，別填錯：**定義單語言的基礎檔案名稱**（monolingual
base，只有單語言格式才要填）留空，**定義新翻譯的基礎檔案**（new base）才是填 `.pot`。
如果檔案格式誤選成「gettext PO 檔案（單語言）」，留空就會被擋下來，錯誤訊息是
「您不用基底檔案就不能作單語言翻譯。」——改回「gettext PO 檔案」即可。

安裝時會先列出比對到的檔案讓你確認，應該是 7 個組件 × 2 個語言（`en`、`zh_Hant`），
其中主組件已存在不會重複建。discovery 產生的組件用 `weblate://` 內部網址串在主組件上，
所以 7 個組件共用同一份 git checkout。建完檢查一下各組件的 Source language 是不是 `ja`。

若在組件頁面也找不到組件探索，那就是站方沒啟用這個附加元件（`WEBLATE_ADDONS` 設定），
只能手動建 6 個。手動建時 **Source code repository 要填
`weblate://ospo-starter-kit/policy-articles`**，否則會 clone 7 份。

組件 id 與檔案的對應見 `l10n_files.py`：`policy-articles`、`policy-intro`、`operation-root`、
`operation-about`、`operation-compliance`、`operation-using`、`readme`。

### 4. 讓 Weblate 推得回來

二選一：

- **Gitea pull request**：組件的 Version control system 選 `Gitea pull request`，Weblate 會開 PR。
- **直接 push**：VCS 留 `Git`，用 SSH 網址，並在 Codeberg 儲存庫的 Collaborators 加入 `translate`
  這個帳號（給 Write 權限）。可另外指定 push branch，例如 `weblate-zh-hant`。

再到 Codeberg 儲存庫 Settings → Webhooks 加一個 **Gitea** webhook，Target URL 填
`https://translate.codeberg.org/hooks/gitea`，這樣你 push 之後 Weblate 會自動抓新原文。

### 5. 幾個會踩到的點

- `en/` 會被自動辨識成一個翻譯語言（因為遮罩是 `l10n/po/*/`），這是刻意的——它是對照用的
  參考語言，顯示 93% 是正常的（英文版有 4 個區塊結構對不上、README 沒有英文版）。翻譯者請到
  個人 **Preferences → Languages**（偏好設定 → 語言）把 English 設成 secondary language（第二語言），校對時就會並排顯示。
  若用組件的 Language filter 排掉 `en`，英文對照也會跟著消失。
- Weblate 會改寫 PO 表頭（加上自己的 `X-Generator`、`PO-Revision-Date`），首次提交會有一段
  表頭 diff，正常。
- **腳本的執行順序**：Weblate 交回譯文後先跑 `po-to-markdown.py` 把譯文寫進
  `contents/zh-TW/`，之後才跑 `markdown-to-po.py`（只在日文原文有更動時需要）。反過來跑會用
  舊的 Markdown 蓋掉 Weblate 上的新譯文。
- Hosted 的 Codeberg Translate 不給跑自訂 script 附加元件，所以寫回 Markdown 這一步請放 CI
  （對 Weblate 的 PR 跑 `po-to-markdown.py --check`）或由維護者手動執行。

## 校對規則

1. 只改譯文，不要增刪區塊——`contents/zh-TW/` 的檔案集合與區塊數必須與 `contents/ja/`
   完全相同，PO 以 `檔名:序號` 對位，增刪區塊會讓整份對照錯行。
2. 標成 `no-wrap` 的區塊（程式碼、分隔線）多數照抄原文即可；但目錄樹裡的中文註解要翻。
3. `[公司名稱]`、`［公司名稱］` 這類佔位符整份文件要一致，否則使用者做全域取代時會漏掉。
4. 條號與 `a. b. c.` 項次代號不可調換，條文之間會互相引用。選用條文的全形 `【】` 沿用日文。
5. 有新增或修訂的術語，一併更新 `docs/chinese-style-guide.md` 的術語表。

同一句日文在不同檔案出現時，PO 會去重成一筆（例如各範本開頭那段給 OSPO 承辦人的註解，
20 幾個檔案共用一筆）。`markdown-to-po.py` 若發現同一句原文有兩種中文譯法會報錯，請先統一。
