#!/usr/bin/env python3
"""把 Markdown 切成翻譯區塊。

`segment(text)` 回傳 `Block(kind, text, start, end)` 的 list，`text` 就是
`raw[start:end]`，因此把每個區塊換成譯文再貼回原字串，就能保留原檔所有
空行與縮排。三個 l10n 腳本共用這個切法，區塊序號才對得起來。
"""

import re
from collections import namedtuple

Block = namedtuple("Block", "kind text start end")

HR_RE = re.compile(r"^(-{3,}|\*{3,}|_{3,})\s*$")
HEADING_RE = re.compile(r"^#{1,6}\s")
LIST_RE = re.compile(r"^\s*([-*+]|\d+\.)\s")

CODE = "程式碼"
COMMENT = "註解"
HEADING = "標題"
HR = "分隔線"
TABLE = "表格"
QUOTE = "引用"
LIST = "清單"
PARAGRAPH = "段落"

# 這些區塊不翻譯：指令、路徑、目錄樹、分隔線
NO_TRANSLATE = {CODE, HR}


def segment(text):
    lines = text.split("\n")
    offsets, pos = [], 0
    for line in lines:
        offsets.append(pos)
        pos += len(line) + 1

    blocks = []
    n = len(lines)

    def push(kind, first, last):
        start, end = offsets[first], offsets[last] + len(lines[last])
        if text[start:end].strip():
            blocks.append(Block(kind, text[start:end], start, end))

    i = 0
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        first = i
        stripped = line.lstrip()

        if stripped.startswith("```"):
            i += 1
            while i < n:
                if lines[i].lstrip().startswith("```"):
                    i += 1
                    break
                i += 1
            push(CODE, first, i - 1)
            continue

        if stripped.startswith("<!--"):
            while i < n:
                if "-->" in lines[i]:
                    i += 1
                    break
                i += 1
            push(COMMENT, first, i - 1)
            continue

        if HEADING_RE.match(line):
            push(HEADING, first, first)
            i += 1
            continue

        if HR_RE.match(line):
            push(HR, first, first)
            i += 1
            continue

        if stripped.startswith("|"):
            while i < n and lines[i].lstrip().startswith("|"):
                i += 1
            push(TABLE, first, i - 1)
            continue

        if stripped.startswith(">"):
            while i < n and lines[i].strip():
                i += 1
            push(QUOTE, first, i - 1)
            continue

        if LIST_RE.match(line):
            while i < n and lines[i].strip():
                if HEADING_RE.match(lines[i]) or lines[i].lstrip().startswith("<!--"):
                    break
                i += 1
            push(LIST, first, i - 1)
            continue

        while i < n and lines[i].strip():
            nxt = lines[i]
            if (HEADING_RE.match(nxt) or nxt.lstrip().startswith("<!--")
                    or nxt.lstrip().startswith("```") or nxt.lstrip().startswith("|")
                    or HR_RE.match(nxt) or (i > first and LIST_RE.match(nxt))):
                break
            i += 1
        push(PARAGRAPH, first, i - 1)
    return blocks


def rebuild(source_text, replacements):
    """把 source_text 的每個區塊換成 replacements（與 segment 等長）後回傳。"""
    blocks = segment(source_text)
    if len(blocks) != len(replacements):
        raise ValueError(f"區塊數不符：{len(blocks)} vs {len(replacements)}")
    out, pos = [], 0
    for block, new in zip(blocks, replacements):
        out.append(source_text[pos:block.start])
        out.append(new if new else block.text)
        pos = block.end
    out.append(source_text[pos:])
    return "".join(out)
