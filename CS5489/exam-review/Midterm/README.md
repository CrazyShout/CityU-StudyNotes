# CS5489 · 期中题库与答案解析

六套独立期中卷的78个原题位置，按完整内容去重为67题。题目按考点组织，保留英文原题和中文题意；答案附完整中文题意与必要题图，先给简洁英文作答及逐点对应的中文答案，再用中文补基础、讲推理。较长延伸标为选读。

| 用途 | 入口 |
|---|---|
| 独立做题 | [题目PDF](Questions.pdf) · [题目Markdown](Questions.md) |
| 题目后直接读答案 | [题答合订PDF](Combined.pdf) · [自动组合稿](Combined.md) |
| 快速核对中英题目与简答 | [精简双语PDF](Compact.pdf) · [自动组合稿](Compact.md)，不含详细解析 |
| 单独练习选择题 | [选择题与答案PDF](MultipleChoice.pdf) · [自动筛选稿](MultipleChoice.md)，30道多选题 |
| 单独练习简答题 | [简答题与答案PDF](WrittenResponse.pdf) · [自动筛选稿](WrittenResponse.md)，37道简答题 |
| 补基础和核对答案 | [答案解析PDF](Answers.pdf) · [答案Markdown](Answers.md) |
| 按基础到应用的顺序学习 | [组内阅读顺序](ReadingOrder.md) |
| 按2025A等原卷顺序练习 | [原卷索引](PaperIndex.md) |
| 查旧L2Q题号 | [旧题号对照](LegacyMap.md) |
| 查来源及去重依据 | [材料说明](Materials.md) · [来源目录](SourceCatalog.json) |
| 查原解差异 | [勘误说明](Issues.md) |

第一次学习可顺着目录从各组的基本概念与完整示范开始，再做判断、比较和应用，沿中文题意与解析演算；复习时用题目册独立作答，再对照英文与中文答案，核对作答要点。两道Gaussian Process题保留在历史拓展组。本册不混入模拟专有题、期末或QE题，历史卷规则不代表本学期考试规则。

## A4与定位

题目册69页、答案解析册128页。两册按MT题号对应、独立分页，每题另起一页，长解析自然续页。[原卷索引](PaperIndex.md)、PDF目录与题间回指提供实际页码。A4、100%实际大小，双面建议长边翻转；题目册留有草稿空间。MT010原图及MT060答案草图靠颜色区分类别，建议保留彩色。

额外的合订本共148页，将每题的完整英文原题、中文题意、英文答案、中文对应答案和详细讲解连续编排，原题图与中文题意各保留一次。阅读顺序、MT编号、旧别名和勘误与分册一致；合订本使用自己的页码、目录和册末原卷索引，可以单独阅读或打印。

精简双语版共74页，每题只保留完整英文原题、中文题意、英文简答及中文对应答案，另保留必要题图、作答图、条件与原解差异。正文仍约11 pt，题目连续排版，短题尽量与答案同页，长题自然续页。目录、书签和原卷索引独立定位到本册，适合快速复习和核对作答。

精简版目录和题头标出30道多选题、37道简答题；MT001、MT014、MT029另标“选错”。简答题包括判断说明、比较、计算推导、作图和综合问答，标签表示作答方式，不表示难度。原题要求的理由、计算步骤和图仍须保留，不能因为删去详细讲解而省略。

选择题与简答题另有两个独立精简分册：选择题33页，简答题43页。两册均保留完整中英题干和中英答案，不含详细解析。各册沿用原来的主题与组内顺序，MT编号不变；目录、书签和原卷索引只定位本册题目。两册合起来恰好覆盖67题，没有重复或遗漏。

[本轮67题双语完整性核查](../../../docs/reviews/midterm-compact-alignment-2026-10-12/REVIEW.md)记录了逐题结果和补齐内容。

## 维护与构建

当前目录是题库唯一维护源。编辑Questions.md与Answers.md，QuestionIndex.json维护题号、分组、出处与旧别名；答案中的中文题意和必要图须与题目册一致。每题的中文对应答案须按英文顺序保留全部结论、理由及条件，详细讲解继续承担基础与推导。原卷与带批注文件由持有人另行保存，构建只使用已收录的干净题图。

Combined.md由两份主稿自动组合，不单独修改正文。合订本的页码在CombinedPageIndex.json中，校验记录为CombinedValidation.json；原两册继续使用PageIndex.json与Validation.json。

Compact.md同样从Questions.md与Answers.md生成，只取题干和两段简答；不单独维护另一套答案。QuestionIndex.json的response_type、select和tasks记录题型、选择方向及简答任务，验证器对照英文题面检查，并核对PDF目录与题头标签。CompactPageIndex.json与CompactValidation.json记录本册页码及验证结果。同页多个题目使用各自的PDF目的地坐标，目录链接直接定位到题目标题。

MultipleChoice.md与WrittenResponse.md由同一个精简生成器按response_type筛选，不另行维护题答。它们分别使用同名前缀的PageIndex.json与Validation.json文件；校验器逐项检查所选题号、对应原卷位置和旧别名，只允许本册题目出现在目录与索引中。

在仓库根目录安装requirements-build.txt与npm依赖后，执行：

```sh
python CS5489/exam-review/Midterm/tools/build_all.py
python scripts/validate.py
```

根目录 `python scripts/build.py` 会生成三册课堂讲义及本题库六种版本。工具分别计算各版页码，重复构建直到稳定，再更新原卷索引；构建失败保留旧版完整输出。`CHROME_PATH`可指定已安装Chrome。

只更新合订本或精简版时，分别运行 `python CS5489/exam-review/Midterm/tools/build_all.py --combined-only` 或 `python CS5489/exam-review/Midterm/tools/build_all.py --compact-only`。只更新选择题与简答题两册时使用 `--split-only`。这些模式保留其他版本及其检查缓存。普通构建默认更新六种版本；`python scripts/validate.py`同时核对六个版本、原稿组合关系与全部链接。

普通校验不依赖原卷；需核对另存归档时使用 `tools/validate_source.py --source-dir <归档目录>`，按SourceCatalog中的ID与扩展名命名。重新提取或绘制图片还需可选的requirements-midterm-figures.txt、Poppler和外部归档，参见[材料说明](Materials.md)。

仅重画MT045的L1/L2教学图时，安装绘图依赖后运行 `python CS5489/exam-review/Midterm/tools/prepare_figures.py --teaching-only mt045`。此模式不需要原卷或Poppler，只更新该图及对应的图源记录；其他题图保持。

仅重画MT067前向简图时，运行 `python CS5489/exam-review/Midterm/tools/prepare_figures.py --redraw-only mt067`，同样只更新所选图和图源记录。该图保留原卷的前向节点、参数箭头及方形L节点，省略反向梯度提示；不判定被省略标注是印刷还是手写。

[迁入时的逐题复核](../../../docs/reviews/midterm-integration-2026-10-10/README.md) · [可读性修订与验证](../../../docs/reviews/midterm-readability-2026-10-10/WORKLIST.md) · [中英答案对照复核](../../../docs/reviews/midterm-bilingual-2026-10-11/WORKLIST.md) · [合订本构建核对](../../../docs/reviews/midterm-combined-2026-10-11/WORKLIST.md) · [原卷核查后的修订](../../../docs/reviews/midterm-source-fidelity-2026-10-12/WORKLIST.md) · [精简版内容与排版核对](../../../docs/reviews/midterm-compact-2026-10-12/WORKLIST.md) · [项目首页](../../../README.md)
