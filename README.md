# CityU StudyNotes

CS5489 机器学习与 CS5222 计算机网络的中文学习讲义，保留英文术语和双语题答。按老师实际授课顺序整理，面向需要补基础的同学；通过例子、推导和配套练习理解知识，再用自己的复习工具巩固。

## 阅读与打印

| 分册 | PDF | 可编辑讲义 |
|---|---|---|
| CS5489 | [下载 A4 PDF](pdf/CS5489-A4.pdf) | [Lecture、Tutorial、Assignment](CS5489/course-notes/README.md) |
| CS5222 | [下载 A4 PDF](pdf/CS5222-A4.pdf) | [Chapter、Tutorial、Assignment](CS5222/course-notes/README.md) |
| 基础补课 | [下载 A4 PDF](pdf/Foundations-A4.pdf) | [数学](learning/foundation-notes/MathForML.tex) · [网络](learning/foundation-notes/NetworkBasics.tex) · [来源与证据](learning/foundation-notes/SourceEvidence.tex) |
| CS5489期末真题合订 | [期末双语合订本](CS5489/exam-review/Final/CS5489-Final-Combined.pdf) | [TeX主稿](CS5489/exam-review/Final/CS5489-Final-Combined.tex)，2020B/2021B/2021A三套39题完整题答与勘误 |
| CS5222期末真题合订 | [期末双语合订本](CS5222/exam-review/Final/CS5222-Final-2021A-Combined.pdf) | [TeX主稿](CS5222/exam-review/Final/CS5222-Final-2021A-Combined.tex)，2021/22 Sem A完整题答与重绘拓扑 |
| CS5489期中题目 | [题目册](CS5489/exam-review/Midterm/Questions.pdf) | [共用TeX题答组件](CS5489/exam-review/Midterm/items/) |
| CS5489期中答案解析 | [解析册](CS5489/exam-review/Midterm/Answers.pdf) | [共用TeX题答组件](CS5489/exam-review/Midterm/items/) |
| CS5489期中题答合订 | [题答合订本](CS5489/exam-review/Midterm/Combined.pdf) | [共用TeX题答组件](CS5489/exam-review/Midterm/items/) |
| CS5489期中精简题答 | [精简双语版](CS5489/exam-review/Midterm/Compact.pdf) | [生成入口](latex/books/Compact.tex)，保留中英题目与简答，不含详细解析 |
| CS5489期中选择题 | [选择题与答案](CS5489/exam-review/Midterm/MultipleChoice.pdf) | [生成入口](latex/books/MultipleChoice.tex)，30道多选题的中英题目与答案 |
| CS5489期中简答题 | [简答题与答案](CS5489/exam-review/Midterm/WrittenResponse.pdf) | [生成入口](latex/books/WrittenResponse.tex)，37道简答题的中英题目与答案 |

[打印设置和逐篇页码](pdf/README.md)。每册先放理论，再放Tutorial和Assignment；基础独立成册。建议A4、100%实际大小、每张一页，双面长边翻转。答案已展开，可遮住答案自测。

[期中题库](CS5489/exam-review/Midterm/README.md)独立于课堂讲义，六套历史期中卷去重为67题，提供[按原卷查题](CS5489/exam-review/Midterm/PaperIndex.md)、必要题图、基础解释与勘误。可用分册独立练习，也可用合订本连续阅读每题的题目与答案。

## 一起修改

发现问题可提交 [Issue](https://github.com/CrazyShout/CityU-StudyNotes/issues)，写清课程、文件、章节或PDF页码；想直接改进内容，可以修改LaTeX主稿或Notebook实验代码后提交Pull Request。

**正文先把事情讲明白。** 保留老师的顺序、符号和原题条件；补充推导注明来源。来源写“Lecture2a，第12个单元”，放在解释后或文末，不让读者先猜编号。中文讲解与英文题答表达同一个意思。详细流程见[贡献指南](CONTRIBUTING.md)。

## 当前材料

按 2026 Semester A 全学期已发布 Canvas 材料整理：CS5489 覆盖 Lecture 1–12、Tutorial 1–9、Assignment 1–2 及全学期历史题源附录；CS5222 覆盖 Chapter 1–7、Tutorial 1–12、Assignment 1–3、Research Report 及开卷考纲与公式速查附录（遵循课程开卷合规要求，全册不含任何教材扫描截图，按考纲排除 Socket 编程与 Wireshark 操作题）。[来源与重难点判断](learning/foundation-notes/SourceEvidence.md)区分当前要求、历史真题与教学补充。

这个仓库是整讲讲义和A4版的唯一维护位置，不发布网页版。已有[微课与卡片预览](https://crazyshout.github.io/micro-course/)是独立项目。

## 本地生成 PDF

需要Python 3.12、TeX Live 2026 / MacTeX的XeLaTeX，以及Cairo。模板ElegantBook 4.7随仓库固定保存，许可与来源见[模板记录](latex/vendor/elegantbook/UPSTREAM.json)。先安装系统依赖；macOS可用`brew install cairo`，Debian/Ubuntu可安装`libcairo2`。已有完整TeX Live通常无需补包；BasicTeX使用下面的本地补包步骤：

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-build.txt
python scripts/setup_tex.py  # 仅在现有TeX Live缺包时需要
python scripts/build.py
python scripts/validate.py
```

Windows激活命令为`.venv\Scripts\activate`。补包工具复用已有TeX引擎，将缺包放入被Git忽略的`.build/texmf/`，对应字体映射生成在`.build/texmf-var/`；不会安装或替换整套发行版，也不依赖其他项目生成的用户字体映射。已有旧本地补包目录时，首次构建会自动补建这份项目映射。生成流程不依赖Node、Chrome或Canvas。

构建只读取现有Notebook输出，不训练模型、不运行作业。正式正文只维护`.tex`，旧Markdown和Notebook文字单元保留自动生成的定位入口；课堂三册在`pdf/`，期中六种版本及其索引在`CS5489/exam-review/Midterm/`，两门课的独立期末双语合订本可通过`python scripts/build_final_qa.py <tex-path>`单独重编。只构建期中题库可运行`python CS5489/exam-review/Midterm/tools/build_all.py`；加`--compact-only`只更新完整精简版，加`--split-only`只更新选择题和简答题两册。也可在Actions手动运行 **Build PDFs** 下载全部构建产物。

Notebook的重跑方法与数据目录见[数据说明](docs/DATA.md)。原始整份课件、教材和个人作业不随仓库发布，现有题图及引用保留出处。[材料说明](docs/SOURCES.md) · [迁入记录](docs/MIGRATION.md)。
