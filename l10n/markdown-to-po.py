#!/usr/bin/env python3
"""由 contents/ 產生可匯入 Weblate 的 gettext PO 檔。

原始語言（msgid）是英文，取自 contents/en/：
  l10n/po/<組件>.pot          範本（msgstr 全空）
  l10n/po/zh_Hant/<組件>.po   正體中文，取自 contents/zh-TW/（要翻譯的語言）
  l10n/po/ja/<組件>.po        日文，取自 contents/ja/（給 Weblate 當第二語言對照）

區塊順序以日文原檔（contents/ja/）為骨架——它是 IPA 的權威原文，決定每個檔案切成幾個
區塊、以及寫回 Markdown 時的排版。英文版目前逐區塊與日文對齊；萬一日後英文版又把段落
併掉，那些區塊會沒有 msgid，中文譯文改存到 l10n/frozen-zh-TW.json 並在此列出。

用法：python3 l10n/markdown-to-po.py
"""

import difflib
import json
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import mdblocks
from l10n_files import (BASE, COMPONENTS, LANGS, MSGID, SPINE, component_files,
                        label_for, path_for)
from po_io import write_po

PO_DIR = os.path.join(BASE, "l10n", "po")
FROZEN = os.path.join(BASE, "l10n", "frozen-zh-TW.json")
PROJECT = "OSPO Starter Kit"
PLURALS = {"zh_Hant": "nplurals=1; plural=0;", "ja": "nplurals=1; plural=0;"}
STRICT = {"zh_Hant"}   # 這些語言必須與骨架區塊數相同（要寫回 Markdown）


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
        f"X-Source-Language: {MSGID}",
        "X-Generator: ospo-starter-kit l10n/markdown-to-po.py",
    ]


def align(spine, other):
    """依區塊類型序列對位，回傳與 spine 等長的區塊 list，對不上的填 None。"""
    out = [None] * len(spine)
    matcher = difflib.SequenceMatcher(a=[b.kind for b in spine],
                                      b=[b.kind for b in other], autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag in ("equal", "replace"):
            for k in range(min(i2 - i1, j2 - j1)):
                out[i1 + k] = other[j1 + k]
    return out


def texts_for(rel, spine, lang):
    """回傳與 spine 等長的該語言區塊文字 list（對不上的是空字串）。"""
    path = path_for(rel, lang)
    if not path or not os.path.exists(path):
        return [""] * len(spine)
    blocks = mdblocks.segment(open(path, encoding="utf-8").read())
    if len(blocks) == len(spine):
        return [b.text for b in blocks]
    if lang in STRICT:
        raise SystemExit(f"區塊數不符：{path}（{len(blocks)} vs {len(spine)}），"
                         "請先修正結構再產生 PO")
    return [b.text if b else "" for b in align(spine, blocks)]


def collect(spec):
    """回傳 (entry list, 衝突清單, 沒有英文原文的區塊, 跳過的檔案)。"""
    entries, index, conflicts, orphans, skipped = [], {}, [], {}, []
    for rel in component_files(spec):
        if not path_for(rel, MSGID) or not os.path.exists(path_for(rel, MSGID)):
            skipped.append(label_for(rel))
            continue
        spine = mdblocks.segment(open(path_for(rel, SPINE), encoding="utf-8").read())
        source = texts_for(rel, spine, MSGID)
        others = {lang: texts_for(rel, spine, lang) for lang in LANGS}
        for i, block in enumerate(spine):
            ref = f"{label_for(rel)}:{i + 1}"
            if not source[i]:
                # 英文版沒有這個區塊，無法給它 msgid；中文譯文另外凍結保存
                orphans[ref] = others["zh_Hant"][i]
                continue
            hit = index.get(source[i])
            if hit is None:
                entry = {
                    "msgid": source[i],
                    "comments": [f"type: {block.kind}"],
                    "refs": [ref],
                    # no-wrap：不要重排；ignore-same：程式碼與分隔線多數照抄原文，
                    # 不要讓 Weblate 報「未修改的翻譯」
                    "flags": (["no-wrap", "ignore-same"]
                              if block.kind in mdblocks.NO_TRANSLATE else []),
                    "translations": {l: others[l][i] for l in LANGS},
                }
                index[source[i]] = entry
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
    return entries, conflicts, orphans, skipped


def main():
    os.makedirs(PO_DIR, exist_ok=True)
    for lang in LANGS:
        os.makedirs(os.path.join(PO_DIR, lang), exist_ok=True)
    all_conflicts, all_orphans, all_skipped, total = [], {}, [], 0
    for cid, sheet, spec in COMPONENTS:
        entries, conflicts, orphans, skipped = collect(spec)
        all_conflicts += conflicts
        all_orphans.update(orphans)
        all_skipped += skipped
        if not entries:
            print(f"{cid:22s}   ——  沒有英文原文，跳過（{sheet}）")
            continue
        total += len(entries)
        write_po(os.path.join(PO_DIR, f"{cid}.pot"), header(""),
                 [dict(e, msgstr="") for e in entries])
        for lang in LANGS:
            write_po(os.path.join(PO_DIR, lang, f"{cid}.po"), header(lang),
                     [dict(e, msgstr=e["translations"][lang]) for e in entries])
        print(f"{cid:22s} {len(entries):4d} 筆  （{sheet}）")
    print(f"合計 {total} 筆去重後字串 → {PO_DIR}")

    if all_orphans:
        frozen = {
            "_readme": "英文版沒有對應區塊、因此不進 Weblate 的中文譯文。"
                       "key 是「檔案:區塊序號」，序號以 contents/ja/ 的區塊為準。"
                       "由 markdown-to-po.py 產生，po-to-markdown.py 寫回時使用。"
                       "要讓這些區塊也能在 Weblate 校對，就得補上英文版的對應段落。",
        }
        frozen.update(dict(sorted(all_orphans.items())))
        with open(FROZEN, "w", encoding="utf-8") as fh:
            json.dump(frozen, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        print(f"\n英文版沒有對應區塊、已凍結的中文譯文 {len(all_orphans)} 筆 → "
              f"{os.path.relpath(FROZEN, BASE)}")
        for ref in sorted(all_orphans):
            print("  " + ref)
    elif os.path.exists(FROZEN):
        os.remove(FROZEN)
        print(f"\n所有區塊都有英文原文，已移除 {os.path.relpath(FROZEN, BASE)}")
    if all_skipped:
        print(f"\n沒有英文原文、完全跳過的檔案：{', '.join(all_skipped)}")

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
