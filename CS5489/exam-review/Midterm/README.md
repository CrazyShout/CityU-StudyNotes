# CS5489 · 期中题库与答案解析

六套独立期中卷的78个原题位置，按完整内容去重为67题。题目按考点组织，保留英文原题和中文题意；答案附完整中文题意与必要题图，先给简洁英文作答及逐点对应的中文答案，再用中文补基础、讲推理。较长延伸标为选读。

| 用途 | 入口 |
|---|---|
| 独立做题 | [题目PDF](Questions.pdf) · [旧题目入口](Questions.md) |
| 题目后直接读答案 | [题答合订PDF](Combined.pdf) · [旧版导航](Combined.md) |
| 快速核对中英题目与简答 | [精简双语PDF](Compact.pdf) · [旧版导航](Compact.md)，不含详细解析 |
| 单独练习选择题 | [选择题与答案PDF](MultipleChoice.pdf) · [旧版导航](MultipleChoice.md)，30道多选题 |
| 单独练习简答题 | [简答题与答案PDF](WrittenResponse.pdf) · [旧版导航](WrittenResponse.md)，37道简答题 |
| 补基础和核对答案 | [答案解析PDF](Answers.pdf) · [旧解析入口](Answers.md) |
| 按基础到应用的顺序学习 | [组内阅读顺序](ReadingOrder.md) |
| 按2025A等原卷顺序练习 | [原卷索引](PaperIndex.md) |
| 查旧L2Q题号 | [旧题号对照](LegacyMap.md) |
| 查来源及去重依据 | [材料说明](Materials.md) · [来源目录](SourceCatalog.json) |
| 查原解差异 | [勘误说明](Issues.md) |

第一次学习可顺着目录从各组的基本概念与完整示范开始，再做判断、比较和应用，沿中文题意与解析演算；复习时用题目册独立作答，再对照英文与中文答案，核对作答要点。两道Gaussian Process题保留在历史拓展组。本册不混入模拟专有题、期末或QE题，历史卷规则不代表本学期考试规则。

## A4与定位

题目册与答案解析册各自分页，最新页数见[构建清单](../../../latex/manifest.json)。两册按MT题号对应、独立分页。题目册每题另起一页；答案册与合订本在同一考点组内连续排题，各考点组另起页，长解析自然续页，避免一两行出处单独占一页。[原卷索引](PaperIndex.md)、PDF目录与题间回指提供实际页码。A4、100%实际大小，双面建议长边翻转；题目册留有草稿空间。MT010原图及MT060答案草图靠颜色区分类别，建议保留彩色。

合订本将每题的完整英文原题、中文题意、英文答案、中文对应答案和详细讲解连续编排，原题图与中文题意各保留一次。阅读顺序、MT编号、旧别名和勘误与分册一致；合订本使用自己的页码、目录和册末原卷索引，可以单独阅读或打印。

精简双语版每题只保留完整英文原题、中文题意、英文简答及中文对应答案，另保留必要题图、作答图、条件与原解差异。正文仍约11 pt，题目连续排版，短题尽量与答案同页，长题自然续页。目录、书签和原卷索引独立定位到本册，适合快速复习和核对作答。

精简版目录和题头标出30道多选题、37道简答题；MT001、MT014、MT029另标“选错”。简答题包括判断说明、比较、计算推导、作图和综合问答，标签表示作答方式，不表示难度。原题要求的理由、计算步骤和图仍须保留，不能因为删去详细讲解而省略。

选择题与简答题另有两个独立精简分册：两册分别维护自己的实际页码。两册均保留完整中英题干和中英答案，不含详细解析。各册沿用原来的主题与组内顺序，MT编号不变；目录、书签和原卷索引只定位本册题目。两册合起来恰好覆盖67题，没有重复或遗漏。

[本轮67题双语完整性核查](../../../docs/reviews/midterm-compact-alignment-2026-10-12/REVIEW.md)记录了逐题结果和补齐内容。

## 维护与构建

当前目录是题库唯一维护源。正式正文只编辑`items/MTxxx/`中的原生TeX组件：中英题干、英文答案、中文对应答案、详细推理、题源说明，以及精简版所需的作答图。`frontmatter/`维护导言和原解差异附录。`QuestionIndex.json`维护题号、分组、出处、旧别名、题型与选择方向。必要题图、条件和答案依据保持，完整原卷与个人批注另行保存。

六种版本由`latex/books/`中的入口共用上述组件；入口随构建自动生成，不手工复制题答。旧`Questions.md`、`Answers.md`等仅为自动兼容导航。`latex/manifest.json`绑定各PDF和实际TeX/图片/Notebook输入的哈希，`latex/page-maps.json`保存完整锚点页码；本目录原有`PageIndex.json`和各版`*PageIndex.json`继续提供MT题号页码。

按[根目录说明](../../../README.md)安装Python构建依赖、Cairo与XeLaTeX后，执行：

```sh
python CS5489/exam-review/Midterm/tools/build_all.py
python scripts/validate.py
```

根目录`python scripts/build.py`生成课堂三册和期中六种版本，重复编译直到目录、书签和跨册页码稳定。编译失败、缺字或未解析引用时保留既有PDF。首次构建运行根目录完整命令；不需要Node或Chrome，不运行课堂实验。

原有`--combined-only`、`--compact-only`、`--split-only`选择参数保留，分别构建合订、完整精简、两个题型分册；如果修改共享题答、模板或其他册的页码，应执行完整构建。普通验证核对九册、源稿绑定、题答结构、旧锚点、Notebook保护与数值结果。

普通校验不读取原卷；只有提供`python scripts/validate.py --source-only --source-dir <归档目录>`才核对按SourceCatalog ID命名的外部档案哈希。重新提取或绘制图片仍需可选的requirements-midterm-figures.txt及对应原件，参见[材料说明](Materials.md)。此前HTML构建的Validation报告移入本轮审阅目录留档，当前验收以原生TeX检查与本轮记录为准。

仅重画MT045的L1/L2教学图时，安装绘图依赖后运行 `python CS5489/exam-review/Midterm/tools/prepare_figures.py --teaching-only mt045`。此模式不需要原卷或Poppler，只更新该图及对应的图源记录；其他题图保持。

仅重画MT067前向简图时，运行 `python CS5489/exam-review/Midterm/tools/prepare_figures.py --redraw-only mt067`，同样只更新所选图和图源记录。该图保留原卷的前向节点、参数箭头及方形L节点，省略反向梯度提示；不判定被省略标注是印刷还是手写。

[迁入时的逐题复核](../../../docs/reviews/midterm-integration-2026-10-10/README.md) · [可读性修订与验证](../../../docs/reviews/midterm-readability-2026-10-10/WORKLIST.md) · [中英答案对照复核](../../../docs/reviews/midterm-bilingual-2026-10-11/WORKLIST.md) · [合订本构建核对](../../../docs/reviews/midterm-combined-2026-10-11/WORKLIST.md) · [原卷核查后的修订](../../../docs/reviews/midterm-source-fidelity-2026-10-12/WORKLIST.md) · [精简版内容与排版核对](../../../docs/reviews/midterm-compact-2026-10-12/WORKLIST.md) · [项目首页](../../../README.md)
