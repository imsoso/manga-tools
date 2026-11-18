# manga-tools 📖

中文 | [English](#english)

> Convert Kindle manga MOBI → fixed-layout EPUB (full-page, auto orientation) in one command — **no Calibre needed**.
>
> 一键把 Kindle 漫画 mobi 转成 iPad 友好的**固定版式 EPUB**（竖屏整页铺满），不装 Calibre。

## 为什么做这个

用 Calibre 把漫画 mobi 转 epub，得到的是**重排版式**：漫画页被塞进可变文本流，竖屏看又小又模糊。

而且 Calibre 是为「管理你全部的电子书」设计的：安装包几百 MB，界面和概念一大堆。如果目标只是把手里几本漫画放上 iPad，装一整套软件实在不成比例——所以这个工具反着来：**不依赖任何第三方软件**，一个脚本 + Python 标准库（macOS/Linux 自带），拷过去就能用。

其实 mobi 里的 KF8 漫画流本来就是「每页一张图 + 固定版式」——把它**原样提取**出来，竖屏就能整页铺满屏幕。这个工具干的就是这件事，也顺手修好两个 Kindle 遗留问题：

| 处理 | 效果 |
|---|---|
| `rendition:orientation` → `auto` | 竖屏/横屏都跟随设备 |
| 补 `rendition:spread = none` | 单页显示，不会拼页 |

## 用法

```bash
python3 mobi2manhua_epub.py "阿拉蕾(完全版) - 第01卷.mobi"
# → 阿拉蕾(完全版) - 第01卷 - 横竖屏适配.epub
```

- 支持一次传多个文件
- 输出与 mobi 同目录，自动加「横竖屏适配」后缀
- 传到 iPad：AirDrop → 「图书」App 打开即可

## 依赖

- Python 3.10+（3.13+ 也没问题：内置了被官方移除的 `imghdr` 兼容垫片）
- 无其他依赖，纯标准库；Windows / macOS / Linux 通用

## 原理

```
mobi ──KindleUnpack(--epub_version=A)──▶ 固定版式 EPUB3 骨架
     ──补丁 orientation=auto / spread=none──▶ 重打包 ──▶ 成品
```

核心提取能力来自开源项目 [KindleUnpack](https://github.com/kevinhendricks/KindleUnpack)（GPL-3.0），本仓库对其做了 Python 3.13+ 兼容，并加上补丁与打包流水线。

## 适用范围

- 含 KF8 流的 Kindle 漫画 mobi（主流漫画资源基本都带）
- 排版类文字书不适用（那类请用 Calibre）

## 💡 接受定制

有类似的电子书处理、格式转换、批处理脚本或其他小工具的定制需求？欢迎[提 Issue](../../issues/new) 描述你的场景，一般 48h 内回复。

## License

[GPL-3.0](./LICENSE)（继承上游 KindleUnpack 的许可证）

---

## English

> Convert Kindle manga MOBI → fixed-layout EPUB (full-page, auto orientation) in one command — **no Calibre needed**.

### Why

Converting a manga MOBI with Calibre gives you a **reflowable** EPUB: each page image gets squeezed into a variable text flow, so reading in portrait looks tiny and blurry.

Worse, Calibre is built to manage your *entire* e-book library — a several-hundred-MB install, a dense UI, and a pile of concepts to learn. If the goal is just to put a few manga volumes on your iPad, that's a terrible trade. So this tool goes the opposite way: **no third-party software at all**. One script plus the Python standard library (already on macOS/Linux) — copy it and run.

The KF8 comic stream inside a MOBI is already "one image per page + fixed layout". Extract it as-is and every page fills the screen in portrait. The tool also fixes two Kindle leftovers:

| Fix | Effect |
|---|---|
| `rendition:orientation` → `auto` | Follows device orientation (portrait & landscape) |
| Adds `rendition:spread = none` | One page per screen, no two-up spreads |

### Usage

```bash
python3 mobi2manhua_epub.py "Manga-vol01.mobi"
# → Manga-vol01 - 横竖屏适配.epub
```

- Multiple files supported
- Output lands next to the input with a suffix
- To iPad: AirDrop → open in the Books app

### Requirements

- Python 3.10+ (works on 3.13+: bundled `imghdr` shim for the stdlib module Apple removed)
- No other dependencies; Windows / macOS / Linux

### How it works

```
mobi --KindleUnpack(--epub_version=A)--> fixed-layout EPUB3 skeleton
    --patch orientation=auto / spread=none--> repackage --> done
```

Extraction is powered by [KindleUnpack](https://github.com/kevinhendricks/KindleUnpack) (GPL-3.0); this repo adds Python 3.13+ compatibility plus the patch & packaging pipeline.

### Scope

- MOBI files containing a KF8 comic stream (most manga MOBIs)
- Not for text-heavy books (use Calibre for those)

### 💡 Custom work available

Need similar e-book processing, format conversion, batch pipelines, or other small tools built? [Open an issue](../../issues/new) describing your use case — I usually reply within 48h.

### License

[GPL-3.0](./LICENSE) (inherited from upstream KindleUnpack)
