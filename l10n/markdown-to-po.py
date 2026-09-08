#!/usr/bin/env python3
"""由 contents/ 產生可匯入 Weblate 的 gettext PO 檔。

msgid 是日文原文（contents/ja/），msgstr 是譯文：
  l10n/po/<組件>.pot          範本（msgstr 全空）
  l10n/po/zh_Hant/<組件>.po   正體中文，取自 contents/zh-TW/
  l10n/po/en/<組件>.po        英文，取自 contents/en/（給 Weblate 當次要語言對照）

用法：python3 l10n/markdown-to-po.py
"""

import difflib
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import mdblocks
from l10n_files import BASE, COMPONENTS, LANGS, component_files, label_for, path_for
from po_io import write_po

PO_DIR = os.path.join(BASE, "l10n", "po")
PROJECT = "OSPO Starter Kit"
PLURALS = {"zh_Hant": "nplurals=1; plural=0;", "en": "nplurals=2; plural=(n != 1);"}
STRICT = {"zh_Hant"}   # 這些語言必須與日文原檔區塊數相同（要寫回 Markdown）



def header(lang):
    return [
        f"Project-Id-Version: {PROJECT}",
        "Report-Msgid-Bugs-To: ",
        f"POT-Creation-Date: {date.today().isoformat()}",
        "Last-Translator: ",
        "Language-Team: ",
        f"Language: {lang}",
        "MIME-Version: 1.0",
        "Content-Type: text/plain; charset=UTF-8",
        "Content-Transfer-Encoding: 8bit",
        "Plural-Forms: " + PLURALS.get(lang, "nplurals=1; plural=0;"),
        "X-Source-Language: ja",
        "X-Generator: ospo-starter-kit l10n/markdown-to-po.py",
    ]


def align(ja, other):
    """參考語言用：依區塊類型序列對位，回傳與 ja 等長的譯文 list。"""
    out = [""] * len(ja)
    matcher = difflib.SequenceMatcher(a=[b.kind for b in ja],
                                      b=[b.kind for b in other], autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag in ("equal", "replace"):
            for k in range(min(i2 - i1, j2 - j1)):
                out[i1 + k] = other[j1 + k].text
    return out


def collect(spec):
    """回傳 (順序保持的 entry list, 衝突清單)。entry 內含各語言譯文。"""
    entries, index, conflicts = [], {}, []
    for rel in component_files(spec):
        src = open(path_for(rel, "ja"), encoding="utf-8").read()
        ja = mdblocks.segment(src)
        others = {}
        for lang in LANGS:
            p = path_for(rel, lang)
            if not p or not os.path.exists(p):
                others[lang] = [""] * len(ja)
                continue
            blocks = mdblocks.segment(open(p, encoding="utf-8").read())
            if len(blocks) == len(ja):
                others[lang] = [b.text for b in blocks]
            elif lang in STRICT:
                raise SystemExit(f"區塊數不符：{p}（{len(blocks)} vs {len(ja)}），"
                                 "請先修正結構再產生 PO")
            else:
                # 參考語言（英文）容許結構不同，用 difflib 對位，對不上的留空
                others[lang] = align(ja, blocks)
        for i, block in enumerate(ja):
            ref = f"{label_for(rel)}:{i + 1}"
            hit = index.get(block.text)
            if hit is None:
                entry = {
                    "msgid": block.text,
                    "comments": [f"type: {block.kind}"],
                    "refs": [ref],
                    # no-wrap：不要重排；ignore-same：程式碼與分隔線多數照抄原文，
                    # 不要讓 Weblate 報「未修改的翻譯」
                    "flags": (["no-wrap", "ignore-same"]
                              if block.kind in mdblocks.NO_TRANSLATE else []),
                    "translations": {l: others[l][i] for l in LANGS},
                }
                index[block.text] = entry
                entries.append(entry)
            else:
                hit["refs"].append(ref)
                for lang in LANGS:
                    old, new = hit["translations"][lang], others[lang][i]
                    if old != new and new:
                        if not old:
                            hit["translations"][lang] = new
                        else:
                            conflicts.append((lang, ref, hit["refs"][0]))
    return entries, conflicts


def main():
    os.makedirs(PO_DIR, exist_ok=True)
    for lang in LANGS:
        os.makedirs(os.path.join(PO_DIR, lang), exist_ok=True)
    all_conflicts, total = [], 0
    for cid, sheet, spec in COMPONENTS:
        entries, conflicts = collect(spec)
        all_conflicts += conflicts
        total += len(entries)
        write_po(os.path.join(PO_DIR, f"{cid}.pot"), header(""),
                 [dict(e, msgstr="") for e in entries])
        for lang in LANGS:
            write_po(os.path.join(PO_DIR, lang, f"{cid}.po"), header(lang),
                     [dict(e, msgstr=e["translations"][lang]) for e in entries])
        print(f"{cid:22s} {len(entries):4d} 筆  （{sheet}）")
    print(f"合計 {total} 筆去重後字串 → {PO_DIR}")
    strict = [c for c in all_conflicts if c[0] in STRICT]
    loose = [c for c in all_conflicts if c[0] not in STRICT]
    if strict:
        print("\n⚠ 同一句原文有兩種譯文，PO 去重後只會留第一個。請統一後重跑：")
        for lang, ref, first in strict:
            print(f"  [{lang}] {ref} 與 {first} 不一致")
    if loose:
        print(f"\n（參考語言有 {len(loose)} 處同原文不同譯："
              f"{', '.join(f'{c[0]}:{c[1]}' for c in loose[:3])}"
              f"{' …' if len(loose) > 3 else ''}。只影響對照顯示，可忽略。）")
    return 1 if strict else 0


if __name__ == "__main__":
    sys.exit(main())
