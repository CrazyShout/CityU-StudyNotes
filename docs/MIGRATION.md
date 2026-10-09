# 独立协作仓库迁入记录

2026-10-08从已有整讲讲义迁入。此后本仓库维护讲义源稿、图片、生成工具和PDF；旧Course目录中的讲义保留为历史快照。微课与卡片继续由独立的micro-course项目维护。

迁入内容包含当前两门课21份主要文档、数学/网络/来源三份共用说明及所需图片。顺序保持理论在前、Tutorial和Assignment在后。迁入前的PDF已经完成可读性修订与纸读检查。

迁入只调整资料组织、相对链接、Notebook的数据位置配置与可移植构建，不改课程理论、参数网格或数值结果。原课件链接保留为可读出处，完整文件由读者从Canvas取得。原数据、个人作业、凭证、旧构建缓存和逐次检查截图没有复制进仓库。

当前讲义范围、使用方式和构建入口以README为准；后续修改通过分支和Pull Request进行。

## 2026-10-09 · 其余讲义教学与打印修订

Lecture2的规范复核已随PR #3合并。其余现有文档本轮按相同原则审阅：补足关键示范与变式，完善双语条件、来源位置和公式编号；CS5489历史考点扩展到Lecture1–5，CS5222暂不做考试统计。[本轮问题与处理记录](reviews/all-notes-improvement-2026-10-09/WORKLIST.md)列出逐文档结果。

维护时运行`python scripts/build_exam_annotations.py`更新标注，`--check`仅比对；新增数学例子用`scripts/verify_revision_examples.py`复算，`--check`不写文件。它使用Notebook环境中的NumPy、SciPy、Matplotlib、scikit-learn，只计算明确列出的小例子，不读取原数据或重跑课堂实验。然后按贡献指南生成三册并验收。

## 2026-10-09 · CS5489 Lecture 2–5期中前复核

按用户提供的四讲范围再次逐段检查，Lecture2保留，Lecture3–5补足少量推理、条件及迁移例题。[复核记录](reviews/cs5489-midterm-lecture02-05-2026-10-09/README.md)和[考前自查表](reviews/cs5489-midterm-lecture02-05-2026-10-09/MIDTERM_CHECKLIST.md)分开维护。新增子公式不改旧编号，公开台账与试卷计数保持；未新增本次考试日期或题型结论。复核期间PR #4已合并；本轮补充另交新的PR，等待审阅。
