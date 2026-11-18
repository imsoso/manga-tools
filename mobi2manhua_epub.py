#!/usr/bin/env python3
"""mobi → 「横竖屏适配」固定版式 epub（漫画用，iPad 阅读体验与既有卷册一致）

用法:
    python3 mobi2manhua_epub.py 书1.mobi [书2.mobi ...]

输出: 与 mobi 同目录，文件名 = 原名 + " - 横竖屏适配.epub"

依赖: 仅 Python 3 标准库 + 本目录 kindleunpack_lib（GPL 开源工具）
      产出与 KindleUnpack(mobiunpack) 提取 KF8 的固定版式相同：
      rendition:layout=pre-paginated, orientation=auto, spread=none
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_PKG = "kindleunpack_lib"


def patch_opf(text: str) -> str:
    # 横竖屏适配的关键：方向跟随设备（源文件通常固定为 portrait）
    text = re.sub(
        r'<meta property="rendition:orientation">[a-z]+</meta>',
        '<meta property="rendition:orientation">auto</meta>',
        text,
    )
    # 单页显示，不拼页（与参考版一致；缺失时补上）
    if "rendition:spread" not in text:
        text = text.replace(
            '<meta property="rendition:layout">pre-paginated</meta>',
            '<meta property="rendition:layout">pre-paginated</meta>\n'
            '<meta property="rendition:spread">none</meta>',
            1,
        )
    return text


def find_mobi8_epub(root: str) -> str | None:
    for dirpath, _, files in os.walk(root):
        if os.path.basename(dirpath) == "mobi8":
            for f in files:
                if f.endswith(".epub"):
                    return os.path.join(dirpath, f)
    return None


def convert(mobi: str) -> str:
    mobi = os.path.abspath(mobi)
    out = os.path.splitext(mobi)[0] + " - 横竖屏适配.epub"
    with tempfile.TemporaryDirectory() as td:
        proc = subprocess.run(
            [sys.executable, "-m", f"{LIB_PKG}.kindleunpack", "--epub_version=A", mobi, td],
            cwd=TOOL_DIR,
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            sys.stderr.write(proc.stdout[-800:] + proc.stderr[-800:])
            raise RuntimeError(f"kindleunpack 解包失败: {os.path.basename(mobi)}")

        src = find_mobi8_epub(td)
        if not src:
            raise RuntimeError(f"未找到 mobi8 输出(可能不是 KF8 漫画): {os.path.basename(mobi)}")

        with zipfile.ZipFile(src) as zin:
            entries = [(i.filename, zin.read(i.filename)) for i in zin.infolist()]

    pages = sum(1 for n, _ in entries if re.match(r"OEBPS/Text/part\d+\.xhtml$", n))
    with zipfile.ZipFile(out, "w") as zout:
        for name, data in entries:
            if name.endswith("content.opf"):
                data = patch_opf(data.decode("utf-8")).encode("utf-8")
            comp = zipfile.ZIP_STORED if name == "mimetype" else zipfile.ZIP_DEFLATED
            zout.writestr(name, data, comp)

    size_mb = os.path.getsize(out) / 1048576
    print(f"✓ {os.path.basename(mobi)} → {os.path.basename(out)} ({pages} 页, {size_mb:.0f}M)")
    return out


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    failed = []
    for mobi in sys.argv[1:]:
        try:
            convert(mobi)
        except Exception as e:
            print(f"✗ {os.path.basename(mobi)}: {e}")
            failed.append(mobi)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
