#!/usr/bin/env python3
"""極簡 gettext PO 讀寫。只支援本專案需要的子集：無複數、無 msgctxt。"""

import re

ESCAPES = {"\\": "\\\\", '"': '\\"', "\t": "\\t", "\r": "\\r"}


def _quote(s):
    out = []
    for ch in s:
        out.append(ESCAPES.get(ch, ch))
    return "".join(out)


def po_string(value):
    """把字串寫成 PO 的多行形式（每個 \\n 斷一行，方便 diff）。"""
    if value == "":
        return '""'
    parts = value.split("\n")
    lines = []
    for i, part in enumerate(parts):
        last = i == len(parts) - 1
        if last and part == "":
            continue
        lines.append('"%s%s"' % (_quote(part), "" if last else "\\n"))
    if len(lines) == 1:
        return lines[0]
    return "\"\"\n" + "\n".join(lines)


def write_po(path, header, entries):
    """entries: list of dict(msgid, msgstr, comments=[], refs=[], flags=[])"""
    out = ['msgid ""', 'msgstr ""']
    for line in header:
        out.append('"%s\\n"' % _quote(line))
    out.append("")
    for e in entries:
        for c in e.get("comments", []):
            out.append("#. " + c)
        for r in e.get("refs", []):
            out.append("#: " + r)
        if e.get("flags"):
            out.append("#, " + ", ".join(e["flags"]))
        out.append("msgid " + po_string(e["msgid"]))
        out.append("msgstr " + po_string(e["msgstr"]))
        out.append("")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out).rstrip("\n") + "\n")


_UNESCAPE = re.compile(r'\\(.)')
_MAP = {"n": "\n", "t": "\t", "r": "\r", '"': '"', "\\": "\\"}


def _unquote(line):
    body = line.strip()
    body = body[body.index('"') + 1:body.rindex('"')]
    return _UNESCAPE.sub(lambda m: _MAP.get(m.group(1), m.group(1)), body)


def read_po(path):
    """回傳 {msgid: msgstr}，不含表頭那筆。"""
    entries = {}
    key = None
    buf = {"msgid": [], "msgstr": []}
    field = None
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            if line.startswith("#") or not line.strip():
                continue
            if line.startswith("msgid "):
                if field:
                    entries["".join(buf["msgid"])] = "".join(buf["msgstr"])
                buf = {"msgid": [_unquote(line)], "msgstr": []}
                field = "msgid"
            elif line.startswith("msgstr "):
                buf["msgstr"] = [_unquote(line)]
                field = "msgstr"
            elif line.lstrip().startswith('"') and field:
                buf[field].append(_unquote(line))
    if field:
        entries["".join(buf["msgid"])] = "".join(buf["msgstr"])
    entries.pop("", None)
    return entries
