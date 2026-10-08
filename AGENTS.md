# CityU-StudyNotes 项目入口

先读README.md、CONTRIBUTING.md及docs/MIGRATION.md。此仓库是整讲讲义和A4 PDF的唯一编辑源；旧Course/codexing中的讲义只是迁移前快照，不再双向同步或从那里覆盖本仓库。

- 受众从基础开始学习，中文连续解释、英文术语、双语题答；按当前Canvas顺序，历史材料标明身份。
- 先讲例子、对象与推理，后给来源。引用采用完整材料名和单元/页数；正文不以A12、B4–15等简称开头。
- 理论Lecture/Chapter在前，Tutorial、Assignment/Research Report在后；正文小例题留在知识点旁。
- 大规模修改先在docs/reviews/登记问题与进度，保留无问题段落；不以删字比例验收。
- 保留题目条件、符号、图片、锚点。只改Notebook说明时不动代码与输出；代码变化需重跑受影响实验，真实报告结果。
- 修改主稿，不直接修改PDF；scripts/build.py生成三册并稳定页码。HTML是打印中间物，不建设网页或Pages。
- 原始Canvas文件和实验数据从本地data/或COURSE_DATA_ROOT读取；它们及个人提交文件、凭证、执行缓存不得加入Git。
- 微课和Markji属于另一项目；本仓库不维护卡片、不生成APKG、不操作Markji。
- 发布前执行scripts/validate.py并检查生成PDF。只提交任务相关内容，保留他人修改。
