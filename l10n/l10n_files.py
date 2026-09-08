#!/usr/bin/env python3
"""哪些檔案屬於哪個組件（Weblate component）。三個 l10n 腳本共用。

一個組件 = Weblate 的一個 component = 一個 .pot + 每語言一個 .po，
分組方式與翻譯校對表 xlsx 的分頁一致。
"""

import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MSGID = "en"                                       # msgid（原始語言）取自 contents/en/
SPINE = "ja"                                       # 區塊骨架：日文原檔決定區塊順序與排版
LANGS = {"ja": "ja", "zh_Hant": "zh-TW"}           # 要產生 PO 的語言 → contents/ 目錄名
TARGET = "zh_Hant"                                 # 唯一會被寫回 Markdown 的語言
SOURCE = SPINE                                     # 相容舊用法：path_for(rel, "ja")

# (組件 id, xlsx 分頁名, 來源目錄或檔案)
COMPONENTS = [
    ("policy-articles", "政策-條文", "oss-policy-templates/articles"),
    ("policy-intro", "政策-根目錄", ["oss-policy-templates/introduction.md"]),
    ("operation-root", "營運-根目錄", ["operation-templates/how-to-use-templates-for-ospo.md",
                                       "operation-templates/how-to-use-guide-for-users.md"]),
    ("operation-about", "營運-about", "operation-templates/about"),
    ("operation-compliance", "營運-compliance", "operation-templates/compliance"),
    ("operation-using", "營運-using", "operation-templates/using"),
    ("readme", "README", None),                    # 特例：倉庫根目錄的 README
]

README = {"ja": "README.md", "en": "README.en.md", "zh_Hant": "README.zh-TW.md"}


def component_files(spec):
    """回傳該組件的相對路徑 list（相對於 contents/<lang>/）。"""
    if spec is None:
        return [None]                              # README 特例
    if isinstance(spec, list):
        return list(spec)
    d = os.path.join(BASE, "contents", SOURCE, spec)
    return [spec + "/" + f for f in sorted(os.listdir(d)) if f.endswith(".md")]


def path_for(rel, lang):
    """rel=None 代表 README；lang 用 PO 語言碼或 'ja'。"""
    if rel is None:
        name = README[lang]
        return os.path.join(BASE, name) if name else None
    sub = "ja" if lang == "ja" else ("en" if lang == "en" else LANGS[lang])
    return os.path.join(BASE, "contents", sub, rel)


def label_for(rel):
    return README["ja"] if rel is None else rel
