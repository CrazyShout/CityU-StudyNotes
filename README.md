# CityU StudyNotes

CS5489 机器学习与 CS5222 计算机网络的中文学习讲义，保留英文术语和双语题答。按老师实际授课顺序整理，面向需要补基础的同学；通过例子、推导和配套练习理解知识，再用自己的复习工具巩固。

## 阅读与打印

| 分册 | PDF | 可编辑讲义 |
|---|---|---|
| CS5489 | [下载 A4 PDF](pdf/CS5489-A4.pdf) | [Lecture、Tutorial、Assignment](CS5489/course-notes/README.md) |
| CS5222 | [下载 A4 PDF](pdf/CS5222-A4.pdf) | [Chapter、Tutorial、Assignment](CS5222/course-notes/README.md) |
| 基础补课 | [下载 A4 PDF](pdf/Foundations-A4.pdf) | [数学](learning/foundation-notes/MathForML.md) · [网络](learning/foundation-notes/NetworkBasics.md) |

[打印设置和逐篇页码](pdf/README.md)。每册先放理论，再放Tutorial和Assignment；基础独立成册。建议A4、100%实际大小、每张一页，双面长边翻转。答案已展开，可遮住答案自测。

## 一起修改

发现问题可提交 [Issue](https://github.com/CrazyShout/CityU-StudyNotes/issues)，写清课程、文件、章节或PDF页码；想直接改进内容，可以修改Markdown或Notebook后提交Pull Request。

**正文先把事情讲明白。** 保留老师的顺序、符号和原题条件；补充推导注明来源。来源写“Lecture2a，第12个单元”，放在解释后或文末，不让读者先猜编号。中文讲解与英文题答表达同一个意思。详细流程见[贡献指南](CONTRIBUTING.md)。

## 当前材料

以本学期已下载Canvas材料为准：CS5489为Lecture 1–5、Tutorial 1–4、Assignment 1–2；CS5222为Chapter 1–2及Chapter 3 part 1–2、Tutorial 1–5、Assignment 1和Research Report。后续材料到来再扩展。[来源与重难点判断](learning/foundation-notes/SourceEvidence.md)区分当前要求、历史样题和教学补充。

这个仓库是整讲讲义和A4版的唯一维护位置，不发布网页版。已有[微课与卡片预览](https://crazyshout.github.io/micro-course/)是独立项目。

## 本地生成 PDF

需要Python 3.12和Node.js 22：

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-build.txt
npm ci
npx playwright install chromium
python scripts/build.py
python scripts/validate.py
```

Linux另需Chromium运行库和中文字体：`npx playwright install --with-deps chromium`，并安装`fonts-noto-cjk`。Windows激活命令为`.venv\Scripts\activate`；已安装Chrome时可通过`CHROME_PATH`指定可执行文件。

构建只读取现有Notebook输出，不训练模型、不运行作业。HTML只是`.gitignore`排除的打印中间文件；最终PDF及页码索引在`pdf/`。也可在Actions手动运行 **Build PDFs** 下载构建产物，审核后更新仓库中的PDF。

Notebook的重跑方法与数据目录见[数据说明](docs/DATA.md)。原始整份课件、教材和个人作业不随仓库发布，现有题图及引用保留出处。[材料说明](docs/SOURCES.md) · [迁入记录](docs/MIGRATION.md)。
