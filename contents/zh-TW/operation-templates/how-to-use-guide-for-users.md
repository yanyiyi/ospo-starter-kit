# 給使用者・指南的使用方式

## 先從這裡開始讀

- 公司內部開放原始碼運用的入口
  - → [[公司名稱] 開放原始碼指南](./about/opensource-guide.md)

## 認識 OSS

- 什麼是 OSS、為什麼要使用
  - → [關於開放原始碼](./about/about-opensource.md)
- 使用 OSS 的好處
  - → [開放原始碼的效益](./about/benefits.md)
- 在公司內部推動 OSS 活動的組織（OSPO）
  - → [什麼是 OSPO](./about/ospo.md)
- 在公司內部活用開放原始碼的做法（內源）
  - → [什麼是內源](./about/innersource.md)

## OSS 運用流程實務指南

- 涵蓋 OSS 運用流程、評估、授權確認到導入的實務指南
  - → [使用 OSS](./using/using-oss.md)

## 尋找 OSS

- 能否用既有的 OSS 解決
- 從哪裡尋找
- [公司內部已導入 OSS 清單](./using/oss-inventory.md)／推薦的 OSS
  - → [OSS 的尋找方式](./using/finding-oss.md)

## 評估 OSS

- 技術上是否可用
- 授權條款上是否有問題（粗略判斷）
- 弱點與維護狀況（更新頻率、應對態度）
- 相依性（間接相依）
  - → [OSS 的評估方法](./using/evaluation.md)

## 理解授權條款的基本觀念

- OSS 附帶條件
- 散布、SaaS、公司內部使用的差異
- 使用形態（公司內部使用／散布／SaaS）
- 授權合規的整體樣貌
  - → [開放原始碼授權合規](./compliance/license-compliance.md)
- 什麼是授權條款
  - → [什麼是授權條款](./compliance/what-is-a-license.md)
- 授權條款的種類與分類
  - → [授權條款的種類](./compliance/license-types.md)

## 需要注意的情況

- 會產生原始碼公開義務的情況
- 需要商用契約的情況
- 「看起來像 OSS，但其實不是 OSS」
- → [有原始碼提供義務的授權條款](./compliance/source-disclosure-licenses.md) / [可選擇商用授權的 OSS](./compliance/oss-with-commercial-license-options.md)

## 在開發與採購中使用 OSS

- 自行開發
- 供應商交付
- 委外與共同開發時，在契約階段就 OSS 相關事項做出約定（提交 OSS 清單、SBOM、更正處理等）
- 記錄所使用 OSS 的資訊（清單、評估結果、判斷結果）
- 購買其他公司產品／SDK／中介軟體等，內嵌到自家產品後銷售的情況
  - 確認採購品中是否含有 OSS（屬於提交與確認 OSS 資訊的對象）
  - → [自供應商取得 OSS 的程序](./using/supplier-procurement.md)

## 出貨、提供前的確認

- 遵守授權條款
- 隨附文件（LICENSE / NOTICE）
- 確定產出物
- 記錄出貨物所含 OSS 清單、評估結果與判斷結果
- 依需要提供原始碼、明示修改處
- 疑似有授權違規、資訊外洩、弱點等情況時
- 確保產出物的真實性與來歷（簽章、SBOM、來源證明等）
- 確認契約條件
  - （例如：EULA／契約上的限制與 OSS 條件是否相容、LGPL 等可能要求確保使用者一方的權利、確認 OSS 授權條款的優先適用未受妨礙）

## 出貨後（於運作與維護階段處理）

- 應對原始碼提供要求（要求受理窗口、提供程序、提供範圍）
- 弱點與程式錯誤應對（影響評估→修正／緩解→宣導→防止再發生的流程）
- 更正出貨後才發現的 OSS 混入與授權問題（依需要進行更新或通知）
- 更新相依性、更新 SBOM 等持續性維護

## 遇到問題時查詢與諮詢

- [OSS 使用常見問題](./using/usage-faq.md)
- [授權條款常見問題](./compliance/license-faq.md)
- [詞彙表](./about/glossary.md)
- [什麼是 OSPO](./about/ospo.md)
- 涉及對外部 OSS 貢獻或簽署 CLA 的情況

## 發佈 OSS 的程序

- 發佈申請／確認事項／官方儲存庫／變更管理
  - → 開放原始碼的發佈　※截至 2026 年 4 月尚未建置

## 對外部 OSS 貢獻的程序

- 事前核准／確認事項／CLA 與 DCO 處理／概括許可
  - → 對開放原始碼的貢獻　※截至 2026 年 4 月尚未建置

## 個人 OSS 活動指南

- 保密／公司資源／名義與所屬標示範本

## 事件／弱點的回報與初期處理

- 包含疑似有授權違規、資訊外洩、弱點等情況
