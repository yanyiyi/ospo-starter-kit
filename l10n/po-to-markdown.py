#!/usr/bin/env python3
"""把 Weblate 送回來的 PO 寫回 Markdown（只寫 contents/zh-TW/）。

以 contents/ja/ 的原檔為骨架，逐區塊查 PO 換上中文，因此空行、縮排、區塊順序一定與
日文原檔一致。查表的鍵是英文原文（msgid），所以要先用 contents/en/ 對位。

- PO 裡沒有或未翻譯的區塊，保留日文原文，缺漏看得見。
- 英文版若有沒對應到的區塊（不進 Weblate），改用 l10n/frozen-zh-TW.json 的譯文。
- contents/ja/ 與 contents/en/ 是上游內容，本腳本永不寫入。

用法：
  python3 l10n/po-to-markdown.py               # 寫入 contents/zh-TW/
  python3 l10n/po-to-markdown.py --check       # 只比對差異，不寫檔（給 CI 用）
  python3 l10n/po-to-markdown.py --out /tmp/x  # 輸出到別的目錄
"""

import argparse
import difflib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import mdblocks
from l10n_files import (BASE, COMPONENTS, MSGID, SPINE, TARGET, component_files,
                        label_for, path_for)
from po_io import read_po

PO_DIR = os.path.join(BASE, "l10n", "po")
FROZEN = os.path.join(BASE, "l10n", "frozen-zh-TW.json")


def align(spine, other):
    out = [None] * len(spine)
    matcher = difflib.SequenceMatcher(a=[b.kind for b in spine],
                                      b=[b.kind for b in other], autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag in ("equal", "replace"):
            for k in range(min(i2 - i1, j2 - j1)):
                out[i1 + k] = other[j1 + k]
    return out


def source_texts(rel, spine):
    """與 spine 等長的英文原文 list（對不上的是空字串）。"""
    path = path_for(rel, MSGID)
    blocks = mdblocks.segment(open(path, encoding="utf-8").read())
    if len(blocks) == len(spine):
        return [b.text for b in blocks]
    return [b.text if b else "" for b in align(spine, blocks)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只比對，不寫檔")
    ap.add_argument("--out", help="輸出根目錄（預設為倉庫根目錄）")
    args = ap.parse_args()
    root = args.out or BASE

    frozen = {}
    if os.path.exists(FROZEN):
        frozen = {k: v for k, v in json.load(open(FROZEN, encoding="utf-8")).items()
                  if not k.startswith("_")}

    changed, written, untranslated, skipped = [], 0, [], []
    for cid, _sheet, spec in COMPONENTS:
        po_path = os.path.join(PO_DIR, TARGET, f"{cid}.po")
        if not os.path.exists(po_path):
            skipped.append(cid)
            continue
        catalog = read_po(po_path)
        for rel in component_files(spec):
            src_path = path_for(rel, MSGID)
            if not src_path or not os.path.exists(src_path):
                continue
            spine_text = open(path_for(rel, SPINE), encoding="utf-8").read()
            spine = mdblocks.segment(spine_text)
            source = source_texts(rel, spine)

            out = []
            for i in range(len(spine)):
                ref = f"{label_for(rel)}:{i + 1}"
                msgstr = catalog.get(source[i], "") if source[i] else frozen.get(ref, "")
                if not msgstr:
                    untranslated.append(ref)
                out.append(msgstr or None)
            text = mdblocks.rebuild(spine_text, out)

            target = path_for(rel, TARGET)
            allowed = ("/contents/zh-TW/" in target
                       or target == os.path.join(BASE, "README.zh-TW.md"))
            assert allowed, f"拒絕寫入非目標路徑：{target}"
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

    if skipped:
        print(f"沒有 PO、跳過的組件：{', '.join(skipped)}")
    if untranslated:
        print(f"⚠ {len(untranslated)} 個區塊未翻譯，已保留日文原文：")
        for ref in untranslated[:10]:
            print("  " + ref)
        if len(untranslated) > 10:
            print(f"  …另外 {len(untranslated) - 10} 個")
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
