#!/usr/bin/env python3
"""把 Weblate 送回來的 PO 寫回 Markdown。

以 contents/ja/ 的原檔為骨架，逐區塊換上 PO 裡的譯文，因此空行、縮排、
區塊順序一定與日文原檔一致。PO 裡沒有或未翻譯的區塊，保留日文原文。

用法：
  python3 l10n/po-to-markdown.py               # 寫入 contents/zh-TW/
  python3 l10n/po-to-markdown.py --check       # 只比對差異，不寫檔（給 CI 用）
  python3 l10n/po-to-markdown.py --out /tmp/x  # 輸出到別的目錄
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import mdblocks
from l10n_files import BASE, COMPONENTS, component_files, label_for, path_for
from po_io import read_po

PO_DIR = os.path.join(BASE, "l10n", "po")
LANG = "zh_Hant"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只比對，不寫檔")
    ap.add_argument("--out", help="輸出根目錄（預設為倉庫根目錄）")
    args = ap.parse_args()
    root = args.out or BASE

    changed, untranslated, written = [], 0, 0
    for cid, _sheet, spec in COMPONENTS:
        po_path = os.path.join(PO_DIR, LANG, f"{cid}.po")
        if not os.path.exists(po_path):
            print(f"跳過 {cid}：找不到 {po_path}")
            continue
        catalog = read_po(po_path)
        for rel in component_files(spec):
            src = open(path_for(rel, "ja"), encoding="utf-8").read()
            blocks = mdblocks.segment(src)
            out = []
            for block in blocks:
                msgstr = catalog.get(block.text, "")
                if not msgstr:
                    untranslated += 1
                out.append(msgstr or None)
            text = mdblocks.rebuild(src, out)

            target = path_for(rel, LANG)
            dest = target if root == BASE else os.path.join(
                root, os.path.relpath(target, BASE))
            old = open(dest, encoding="utf-8").read() if os.path.exists(dest) else None
            if old != text:
                changed.append(os.path.relpath(dest, root))
            if not args.check:
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with open(dest, "w", encoding="utf-8") as fh:
                    fh.write(text)
                written += 1

    if untranslated:
        print(f"⚠ {untranslated} 個區塊未翻譯，已保留日文原文")
    if args.check:
        if changed:
            print(f"與 PO 不一致的檔案（{len(changed)}）：")
            for c in changed:
                print("  " + c)
            return 1
        print("contents/zh-TW/ 與 PO 一致")
        return 0
    print(f"寫入 {written} 個檔案，其中 {len(changed)} 個有變更")
    for c in changed:
        print("  " + c)
    return 0


if __name__ == "__main__":
    sys.exit(main())
