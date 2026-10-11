# CS5489 · 期中题库与答案解析

六套独立期中卷的78个原题位置，按完整内容去重为67题。题目按考点组织，保留英文原题和中文题意；答案附完整中文题意与必要题图，先给简洁英文作答及逐点对应的中文答案，再用中文补基础、讲推理。较长延伸标为选读。

| 用途 | 入口 |
|---|---|
| 独立做题 | [题目PDF](Questions.pdf) · [题目Markdown](Questions.md) |
| 补基础和核对答案 | [答案解析PDF](Answers.pdf) · [答案Markdown](Answers.md) |
| 按基础到应用的顺序学习 | [组内阅读顺序](ReadingOrder.md) |
| 按2025A等原卷顺序练习 | [原卷索引](PaperIndex.md) |
| 查旧L2Q题号 | [旧题号对照](LegacyMap.md) |
| 查来源及去重依据 | [材料说明](Materials.md) · [来源目录](SourceCatalog.json) |
| 查原解差异 | [勘误说明](Issues.md) |

第一次学习可顺着目录从各组的基本概念与完整示范开始，再做判断、比较和应用，沿中文题意与解析演算；复习时用题目册独立作答，再对照英文与中文答案，核对作答要点。两道Gaussian Process题保留在历史拓展组。本册不混入模拟专有题、期末或QE题，历史卷规则不代表本学期考试规则。

## A4与定位

题目册69页、答案解析册126页。两册按MT题号对应、独立分页，每题另起一页，长解析自然续页。[原卷索引](PaperIndex.md)、PDF目录与题间回指提供实际页码。A4、100%实际大小，双面建议长边翻转；题目册留有草稿空间。MT010原图及MT060答案草图靠颜色区分类别，建议保留彩色。

## 维护与构建

当前目录是题库唯一维护源。编辑Questions.md与Answers.md，QuestionIndex.json维护题号、分组、出处与旧别名；答案中的中文题意和必要图须与题目册一致。每题的中文对应答案须按英文顺序保留全部结论、理由及条件，详细讲解继续承担基础与推导。原卷与带批注文件由持有人另行保存，构建只使用已收录的干净题图。

在仓库根目录安装requirements-build.txt与npm依赖后，执行：

```sh
python CS5489/exam-review/Midterm/tools/build_all.py
python scripts/validate.py
```

根目录 `python scripts/build.py` 会生成三册课堂讲义及本题库两册。工具分别计算两册页码，重复构建直到稳定，再更新原卷索引；构建失败保留旧版完整输出。`CHROME_PATH`可指定已安装Chrome。

普通校验不依赖原卷；需核对另存归档时使用 `tools/validate_source.py --source-dir <归档目录>`，按SourceCatalog中的ID与扩展名命名。重新提取或绘制图片还需可选的requirements-midterm-figures.txt、Poppler和外部归档，参见[材料说明](Materials.md)。

仅重画MT045的L1/L2教学图时，安装绘图依赖后运行 `python CS5489/exam-review/Midterm/tools/prepare_figures.py --teaching-only mt045`。此模式不需要原卷或Poppler，只更新该图及对应的图源记录；其他题图保持。

[迁入时的逐题复核](../../../docs/reviews/midterm-integration-2026-10-10/README.md) · [可读性修订与验证](../../../docs/reviews/midterm-readability-2026-10-10/WORKLIST.md) · [中英答案对照复核](../../../docs/reviews/midterm-bilingual-2026-10-11/WORKLIST.md) · [项目首页](../../../README.md)
