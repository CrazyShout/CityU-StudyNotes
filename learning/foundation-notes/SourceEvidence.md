# Sources and priorities｜重难点判断凭什么

[CS5489目录](../../CS5489/course-notes/README.md) · [CS5222目录](../../CS5222/course-notes/README.md)

**核对日期：2026-10-03。** 学习优先级和理解难度分别标注：核心必会表示它支撑当前课程目标或配套任务；高难度表示需要更多推理台阶。复杂不自动等于高频考点，缺少历史题证据也不等于不考。

## 当前范围由哪些原件决定

CS5489目前下载到Lecture1–5、Tutorial1–4和Assignment1–2；网络课目前为Chapter1–2完整件、Chapter3的part1–2、Tutorial1–5、Assignment1和Research Report。整讲正文按当前源顺序，来源索引定位每个单元/页段。数据、代码、图片附件随所属任务归入，不独立算一讲。

9月23日核对的34份Notebook/PDF/PPT文件已登记路径、SHA-256和单元/页数于历史来源清单。网络part副本与完整PPT、Lecture2的Notebook与PDF按同一教学内容对应；重复副本不增加课程范围。

以下不计为当前已经有正文：CS5489 Lecture5对应Tutorial；CS5222 Chapter2早期目录中的独立FTP讲解；两门课后续尚未下载的章节与作业。Overview/Intro列出的学期路线只说明计划，不证明资料已提供。

## 历史资料能帮到哪里

| 证据 | 核对结果与可用位置 | 不能推断的结论 |
|---|---|---|
| ML sample_final_questions.docx | 封面明确CITY UNIVERSITY OF HONG KONG (DONGGUAN)、Semester A 2024/25、Sample Questions。Q2a问ridge优缺点，Q3a用正则LR学习曲线诊断，Q4a讨论不平衡，Q4b要求约束优化及dual；可辅助Lecture3/4英文解释与迁移训练 | 样题不是真实试卷；东莞不等于香港；不能推出“每年必考”或确认QE范围；该文件未直接确认教师姓名 |
| ML Home_Assignments_1.pdf | 上轮Lecture2已核对2024日期及Ex2分布/MLE迁移，教师/校区只由仓库上下文推测；复用旧核查记录 | 不把另一个分布的历史任务改成本学期新要求 |
| CS5222 review.docx | 是整理笔记，开头覆盖edge、交换、时延、分层，之后涉及应用协议；已核对这些相关部分。未在文件开头找到可确认年份、教师、校区的封面 | 不是官方考纲或评分答案，不能计入真题频率 |

重复副本视为同一份依据。版本与去重记录见来源清单及上方材料清单。

网络旧整理笔记对Zoom直接列HTTP/WebSocket/RTP，却没有在该段给足客户端/版本与技术来源；这些记录不足以确定不同Zoom部署的协议组合。当前作业指南转为按官方资料标明原生客户端、会议室互通、云/P2P/Mesh情境。

## 每项判断怎样写进讲义

- **当前依据**：具体原课单元、课堂题、Tutorial或Assignment；学习目标写成“解释/计算/推导/实现”。
- **历史依据**：明确是样题、作业还是复习笔记，写年份/校区已知与未知部分，不把副本次数当年份。
- **整理者建议**：为补基础、降低跳步、检查边界而增加的例子/变式，明确标为教学补充。
- **软件与协议补充**：给官方资料和查阅日期；本次实际执行/测量与原课保存输出分开。

Lecture1的Python/NumPy重点由当前Tutorial1使用频率与后续依赖决定，依据当前课程任务与先修关系判断。Lecture3的约束推导既有当前SVM补充，也有历史样题的迁移练习支持；一般强对偶证明仍列二读拓展。Lecture4的ridge/LASSO比较有原课完整流程，历史Q2a额外支持练优缺点表达；这不代表其他回归模型不重要。网络课Q&A、Tutorial和Assignment对当前Chapter1/2的直接练习支持强于无年份整理笔记。

## 交付与检查证据

Notebook保存真实执行输出；补充图保存计算脚本与参数；原题图旁给出条件，答案与推导可回查来源。本仓库维护源稿与A4 PDF，HTML仅为打印中间文件；迁入说明见[维护记录](../../docs/MIGRATION.md)。


2026-10-03补充：新增12份教学原件，Lecture5 HTML/ZIP不重复计覆盖。Chapter3两个part共70页，到RTT/timeout；完整后半章仍缺。Tutorial3官方解答确认现有DNS/HTTP计算；Tutorial4的DASH按v2一一配对解释N，任意组合N²作补充。Assignment2原模板的凸性公式、批量梯度及全量预处理需按讲义注明区别；原件保持。
