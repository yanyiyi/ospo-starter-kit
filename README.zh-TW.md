# OSPO 入門套件　草案版

本套件是一套範本集，協助組織設立開放原始碼專案辦公室 (OSPO)，建立開放原始碼的策略性運用與適當的治理體制。

## ⚠️ 開發狀態與後續計畫

本套件目前為 **「草案版（未完成）」**。部分內容仍在評估中或製作途中，未來可能大幅更新。關於更新狀況，請參閱 [Releases
](https://github.com/japan-opensource-hub/ospo-starter-kit/releases)。

## 隨附檔案一覽與概要

本套件包含以下文件。

### A. OSS 政策（全公司規範）範本 (`oss-policy-templates/`)

這是一套範本，彙整了制定公司內部 OSS 政策（全公司規範）時可供參考的條文範例，以及其背景與客製化指引。每一條條文由「條文範例」「解說」「客製化的觀點與運作上的注意事項」三個小節構成。

- `introduction.md`：前言 ─ 本文件的使用方式
- `articles/00_preamble.md`：第 0 條 前言
- `articles/01_purpose.md`：第 1 條 目的
- `articles/02_definitions.md`：第 2 條 用語定義
- `articles/03_scope.md`：第 3 條 適用範圍
- `articles/04_ospo.md`：第 4 條 OSPO
- `articles/05_oss_usage.md`：第 5 條 OSS 的使用
- `articles/06_contribution.md`：第 6 條 對 OSS 專案的貢獻
- `articles/07_oss_release.md`：第 7 條 本公司著作以 OSS 形式發佈
- `articles/08_personal_oss_activity.md`：第 8 條 員工的個人 OSS 活動
- `articles/09_trademark_and_brand.md`：第 9 條 商標與品牌的處理
- `articles/10_license_violation_incident.md`：第 10 條 授權違規與事件的應對
- `articles/11_security_and_vulnerability.md`：第 11 條 資訊安全與弱點應對
- `articles/12_records_and_reporting.md`：第 12 條 紀錄與報告
- `articles/13_education_and_awareness.md`：第 13 條 教育與宣導
- `articles/14_employment_rules_relation.md`：第 14 條 與工作規則等的關係
- `articles/15_revision_and_enforcement.md`：第 15 條 修訂與施行


### B. 營運範本 (`operation-templates/`)

這是一套文件範本，用於刊載在公司內部入口網站（Wiki 或 SharePoint 等），向承辦人宣導。每份範本都附有「客製化檢核清單」與「客製化指南（寫在註解中）」。

關於範本的導入與客製化程序，請參閱 `how-to-use-templates-for-ospo.md`（給 OSPO 承辦人）與 `how-to-use-guide-for-users.md`（給使用者）。

- **基礎與組織** (`about/`)
  - `opensource-guide.md`：開放原始碼指南（入口）
  - `about-opensource.md`：關於開放原始碼
  - `benefits.md`：開放原始碼的效益
  - `ospo.md`：什麼是 OSPO
  - `innersource.md`：什麼是內源
  - `glossary.md`：詞彙表

- **授權合規** (`compliance/`)
  - `license-compliance.md`：開放原始碼授權合規
  - `what-is-a-license.md`：什麼是授權條款
  - `license-types.md`：授權條款的種類
  - `source-disclosure-licenses.md`：有原始碼提供義務的授權條款
  - `oss-with-commercial-license-options.md`：可選擇商用授權的 OSS
  - `license-faq.md`：授權條款常見問題

- **實務與 OSS 運用** (`using/`)
  - `using-oss.md`：使用 OSS
  - `finding-oss.md`：OSS 的尋找方式
  - `oss-inventory.md`：公司內部已導入 OSS 清單
  - `evaluation.md`：OSS 的評估方法
  - `supplier-procurement.md`：自供應商取得 OSS 的程序
  - `usage-faq.md`：OSS 使用常見問題

## 關於授權

本套件所含的文字與文件，以 **[CC0 1.0 Universal（提供至公眾領域）](https://creativecommons.org/publicdomain/zero/1.0/)** 提供。

- **拋棄著作權**：已拋棄著作權法上的權利，無論營利或非營利，都可以未經許可重製、修改與再散布。
- **不需標示出處**：不需要標示原作者的姓名（歸屬）。歡迎自由改寫，作為使用自家品牌與標誌的公司內部正式文件使用。

## 免責聲明（使用上的注意事項）

本套件依 CC0 授權，可在無著作權限制的情況下使用，但請留意以下幾點。

- **需要法務確認**：本套件所含的政策與授權解說均為一般性範本。實際運作時，請務必取得自家公司法務、智慧財產部門或專家的確認。
- **不提供任何保證**：本套件以「現狀」提供，不提供任何明示或默示的保證，包括可商用性、特定目的適用性與不侵權的保證。因使用本套件而產生任何損害時，提供者不負任何責任。

## 貢獻指南（暫行）

本指南會在運作過程中隨時更新，目前暫以下列內容為準。

- 較大的結構變更或方針變更，請先在 Issues 討論。
  - 例如：目錄結構的變更、範本的大幅改寫、運作規則的變更等
  - 改善建議請明確寫出背景與期待的效果。
- 小幅修正（錯字、輕微的措辭調整）可直接提出 Pull Request（以下稱 PR）。
- PR 的標題與說明中，請盡可能簡潔寫出「為什麼要這樣做」。
  - 建議在提交標題開頭加上 [add]、[fix]、[update] 等標籤。
- PR 處理
  - 須經一位以上審查後才合併。
  - 須確認測試與 linter 等自動審查已通過。

## 處理時間目標 (SLA: Service Level Agreement)

維運方以下列方針為目標，處理 Issue 與 Pull Request。

### 處理時間的目標

- Issue 的初次回應
  - 原則上於 **1～2 週內** 留言或加上標籤。
- Pull Request 的審查
  - 原則上於 **2 週內** 進行審查或留下進度留言。

以上僅為目標，可能因時期與狀況而延遲。

### 處理範圍的原則

維運方主要以下列項目為處理對象。

- 範本內容或結構的變更與改善
- 用語統一或措辭整理
- OSPO 入門套件整體方針與定位的調整

另一方面，下列內容原則上 **不在維運方的 SLA 範圍內**。

- 深入各組織特有情況的個別諮詢顧問服務
- 本儲存庫以外的系統設定、網路、認證相關的疑難排解
- OSPO 以外的全公司制度與治理設計本身的核准與決行
- 其他與範本內容無關的事項

### 工作日與處理時間的前提

- 工作日以 **平日（日本時間）** 為前提。
- 在忙季或活動應對期間，可能比上述目標延遲。

### SLA 的定位

- 此處所示內容僅為「維運方所欲達成的處理目標」，並非必然具法律拘束力的服務保證。
- SLA 的內容可能依實際運作狀況與資源而檢視、更新。

## 發行單位與聯絡方式

關於本套件內容的問題，請寄至以下電子郵件地址。

發行單位：獨立行政法人資訊處理推進機構 (IPA)

聯絡方式：IPA 數位與 AI 系統設計中心 (DADC) disc-info@ipa.go.jp

## 製作團隊與致謝

本套件的規劃與製作，主要由以下成員貢獻。所屬單位為初版（草案版）公開時的資訊。

- 規劃：今村 かずき（IPA 數位基盤中心 數位工程部 軟體工程小組）
- 撰稿：服部 佑樹（IPA 專門委員、GitHub Japan 合同會社） / 渡邊 歩（IPA 專門委員、Hitachi Solutions 股份有限公司） / 福地 弘行（IPA 數位基盤中心 數位工程部 軟體工程小組）
- 審查：大内 佳子（三菱電機股份有限公司） / 大和田 清志（Socionext 股份有限公司）

此外，也感謝提供回饋的 OSPO Level 1 建置工作坊各參與團隊。
