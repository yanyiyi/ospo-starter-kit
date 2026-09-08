#!/usr/bin/env python3
"""產生 zh-TW 翻譯校對表 xlsx（給不用 Weblate 的校對者）。

日文原文 / 英文參考 / 中文初稿三欄並列，一列一個區塊，區塊序號與
l10n/po/ 的 PO 參照（`檔名:序號`）相同。用法：
  python3 l10n/build-translation-xlsx.py      # 需要 openpyxl
"""

import difflib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

import mdblocks
from l10n_files import (BASE, COMPONENTS, MSGID, SPINE, TARGET, component_files,
                        label_for, path_for)

OUT = os.path.join(BASE, "l10n", "ospo-starter-kit-zh-TW-translations.xlsx")

NAVY = "1F3864"; CREAM = "FFF2CC"; GREY = "D9D9D9"
HDR_FONT = Font(name="Arial", size=10, bold=True, color="FFFFFF")
BODY_FONT = Font(name="Arial", size=10)
HDR_FILL = PatternFill("solid", fgColor=NAVY)
CREAM_FILL = PatternFill("solid", fgColor=CREAM)
GREY_FILL = PatternFill("solid", fgColor=GREY)
WRAP_TOP = Alignment(wrap_text=True, vertical="top")
WRAP_CENTER = Alignment(wrap_text=True, vertical="center")

HEADERS = ["頁面", "區塊", "類型", "英文（原文）", "日文（參考）",
           "中文（機器初稿）", "中文（校對後）", "狀態", "備註"]
WIDTHS = [30, 6, 12, 58, 58, 58, 58, 10, 28]


def align(spine, other):
    """英文版結構偶爾與日文不同，依區塊類型序列對位，對不上的留空。"""
    if other is None:
        return [""] * len(spine)
    if len(spine) == len(other):
        return [b.text for b in other]
    out = [""] * len(spine)
    matcher = difflib.SequenceMatcher(a=[b.kind for b in spine],
                                     b=[b.kind for b in other], autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag in ("equal", "replace"):
            for k in range(min(i2 - i1, j2 - j1)):
                out[i1 + k] = other[j1 + k].text
    return out


def read_blocks(path):
    if not path or not os.path.exists(path):
        return None
    return mdblocks.segment(open(path, encoding="utf-8").read())


wb = openpyxl.Workbook()
info = wb.active
info.title = "說明"

totals = []
for cid, sheet, spec in COMPONENTS:
    ws = wb.create_sheet(sheet)
    for i, (h, w) in enumerate(zip(HEADERS, WIDTHS), 1):
        c = ws.cell(row=1, column=i, value=h)
        c.font = HDR_FONT; c.fill = HDR_FILL; c.alignment = WRAP_CENTER
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[1].height = 30

    r = 2
    for rel in component_files(spec):
        spine = read_blocks(path_for(rel, SPINE))
        en = align(spine, read_blocks(path_for(rel, MSGID)))
        zh = align(spine, read_blocks(path_for(rel, TARGET)))
        for idx, block in enumerate(spine, 1):
            # 只有「原文與譯文完全相同的程式碼／分隔線」才鎖起來；
            # 程式碼區塊裡的註解有時是要翻的（例如目錄樹的說明）。
            locked = block.kind in mdblocks.NO_TRANSLATE and zh[idx - 1] == block.text
            note = None if en[idx - 1] else "英文版無對應區塊，不進 Weblate"
            vals = [label_for(rel), idx, block.kind, en[idx - 1], block.text,
                    zh[idx - 1], None, "—" if locked else "待校", note]
            for ci, v in enumerate(vals, 1):
                c = ws.cell(row=r, column=ci, value=v)
                c.font = BODY_FONT; c.alignment = WRAP_TOP
                if locked and ci in (4, 5, 6, 7):
                    c.fill = GREY_FILL
                elif ci in (7, 9):
                    c.fill = CREAM_FILL
            r += 1

    last = r - 1
    ws.freeze_panes = "D2"
    ws.auto_filter.ref = f"A1:I{last}"
    dv = DataValidation(type="list", formula1='"待譯,待校,OK,已修改,—"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"H2:H{last}")
    totals.append((sheet, last - 1))

# ---- 說明分頁 ----
T = Font(name="Arial", size=16, bold=True, color=NAVY)
H = Font(name="Arial", size=12, bold=True, color=NAVY)
B = Font(name="Arial", size=10, bold=True)
N = Font(name="Arial", size=10)


def put(row, col, val, font=None, wrap=False):
    c = info.cell(row=row, column=col, value=val)
    c.font = font or N
    c.alignment = Alignment(wrap_text=wrap, vertical="top")
    return c


for col, w in zip("ABCDEFG", [34, 16, 14, 14, 46, 20, 12]):
    info.column_dimensions[col].width = w

grand = sum(n for _, n in totals)
put(1, 1, "OSPO 入門套件 正體中文（zh-TW）翻譯校對表", T); info.row_dimensions[1].height = 20
put(3, 1, f"37 頁文件（含 README）切成 {grand} 個區塊（標題／段落／清單／表格／引用／註解／程式碼）。"
          "原始語言是英文，日文是 IPA 權威原文供對照，中文欄已填入初稿待母語者校對。", wrap=True)
info.row_dimensions[3].height = 42
put(4, 1, "匯入 Google 試算表：檔案 → 匯入 → 上傳此檔 → 選「插入新的試算表」，各分頁會自動成為獨立工作表。", wrap=True)
info.row_dimensions[4].height = 32
put(5, 1, "偏好 Weblate 的話用 l10n/po/ 的 PO 檔，內容與本表相同（`檔名:序號` 對得起來）。", wrap=True)

put(7, 1, "欄位說明", H)
put(8, 1, "欄位", B); put(8, 2, "說明", B); put(8, 5, "如何處理", B)
FIELDS = [
    ("頁面", "來源檔案（相對於 contents/），用來定位。", "唯讀"),
    ("區塊", "該檔案中的第幾個區塊。與 contents/zh-TW/ 的同名檔案、PO 的 `檔名:序號` 一一對應。", "唯讀"),
    ("類型", "標題／段落／清單／表格／引用／註解／程式碼／分隔線。", "唯讀"),
    ("英文（原文）", "原始語言（contents/en/），也是 PO 的 msgid。少數區塊英文版沒有，該欄留空。", "唯讀"),
    ("日文（參考）", "IPA 的日文原文（contents/ja/），決定區塊順序。英文版語意有疑慮時以它為準。", "唯讀"),
    ("中文（機器初稿）", "目前 contents/zh-TW/ 實際使用的譯文。", "唯讀，保留供比對"),
    ("中文（校對後）", "只在你要改動時填寫；維持原譯就留空。", "★ 請填這欄"),
    ("狀態", "待譯 / 待校 / OK / 已修改 / —（下拉選單）。", "★ 請更新"),
    ("備註", "疑問或給其他校對者的說明。", "★ 自由填寫"),
]
row = 9
for f, d, how in FIELDS:
    put(row, 1, f); put(row, 2, d, wrap=True); put(row, 5, how)
    info.row_dimensions[row].height = 28
    row += 1

row += 1
put(row, 1, "填寫範例", H); row += 1
put(row, 1, "假設你認為 05_oss_usage.md 的「軟體物料清單」應改成「軟體組成清單」，該列會長這樣：", wrap=True); row += 1
put(row, 1, "頁面", B); put(row, 2, "中文（機器初稿）", B); put(row, 3, "中文（校對後）", B)
put(row, 4, "狀態", B); put(row, 5, "備註", B); row += 1
put(row, 1, "articles/05_oss_usage.md"); put(row, 2, "軟體物料清單（SBOM）")
put(row, 3, "軟體組成清單（SBOM）"); put(row, 4, "已修改"); put(row, 5, "台灣業界多用「組成」", wrap=True); row += 2

put(row, 1, "四條絕對不能違反的規則", H); row += 1
RULES = [
    ("① 灰底的列不要動",
     "指令、路徑、目錄樹、分隔線一字都不能改。那些列的日文／英文／中文欄都鎖成灰底，只是讓你看到它在原文中的位置，狀態欄填「—」。"),
    ("② Markdown 語法與佔位符保留",
     "標題的 # 數量、清單符號、`- [ ]` 檢核方塊、表格的 | 與對齊標記、圖片與連結語法都照原樣。表格內的 \\| 轉義也要留。"
     "`[公司名稱]`、`［公司名稱］` 這類佔位符要維持整份文件用同一個寫法，否則使用者做全域取代時會漏掉。"),
    ("③ 條號與項次代號不可調換",
     "第 5 條、a. b. c. 這些編號在條文之間會互相引用（例如「前條」「第 12 條」）。可以改用詞，不能改順序或代號；"
     "選用條文的全形方括號【】也要留（英文版轉成 []，中文不跟隨）。"),
    ("④ 不能增刪列",
     "contents/zh-TW/ 的檔案集合與區塊數必須與 contents/ja/ 完全相同。你只需填「中文（校對後）」，永遠不要新增或刪除任何一列。"),
]
for t, d in RULES:
    put(row, 1, t, B); put(row, 2, d, wrap=True)
    info.row_dimensions[row].height = 56
    row += 1

row += 1
put(row, 1, "另外：授權識別碼（Apache-2.0、MIT）、SPDX／CycloneDX 欄位名、法規與規格縮寫（SBOM、OSI、CVE、CVSS）、"
            "檔案路徑、URL、GitHub 操作名詞（fork、Pull Request、Issue）一律保留英文。", wrap=True)
info.row_dimensions[row].height = 32; row += 1
put(row, 1, "完整術語表、台灣用語對照與文體規範見原始碼中的 docs/chinese-style-guide.md。"); row += 2

put(row, 1, "校對進度", H); row += 1
put(row, 1, "下列數字為公式，會隨各分頁的「狀態」欄自動更新。"); row += 1
for i, h in enumerate(["分頁", "總列數", "待譯", "待校", "OK", "已修改", "免翻譯", "完成率"], 1):
    put(row, i, h, B)
info.column_dimensions["H"].width = 12
row += 1
first_data = row
for name, n in totals:
    put(row, 1, name)
    put(row, 2, n)
    for i, st in enumerate(["待譯", "待校", "OK", "已修改", "—"], 3):
        put(row, i, f"=COUNTIF('{name}'!$H:$H,\"{st}\")")
    put(row, 8, f"=IF($B{row}=0,0,($E{row}+$F{row}+$G{row})/$B{row})").number_format = "0%"
    row += 1
put(row, 1, "合計", B)
put(row, 2, f"=SUM(B{first_data}:B{row - 1})", B)
for col in "CDEFG":
    put(row, "ABCDEFGH".index(col) + 1, f"=SUM({col}{first_data}:{col}{row - 1})", B)
put(row, 8, f"=IF($B{row}=0,0,($E{row}+$F{row}+$G{row})/$B{row})", B).number_format = "0%"

os.makedirs(os.path.dirname(OUT), exist_ok=True)
wb.save(OUT)
print("wrote", OUT)
print("blocks per sheet:", totals, "total", grand)
