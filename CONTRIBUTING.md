# 贡献与维护

## 改哪里

- 讲义正文：两门课程`course-notes/`中的Markdown；可运行练习为Notebook。
- 共用补课：`learning/foundation-notes/`。只补相关先修，课堂算法仍在所属讲义讲完整。
- 图片：就近放入`assets/`；计算图保留脚本、数据含义、参数、坐标与单位。
- 顺序和日期：`learning/course-notes-documents.json`。登记顺序决定PDF的理论、Tutorial、Assignment顺序。
- PDF：从源稿生成后再提交，不直接改PDF文字。

## 一次修改

1. 建分支，先写清课程、章节、问题与拟采用的依据；批量修订先在`docs/reviews/`建立工作清单。
2. 优先改已有解释，保留清楚的段落。用小例子交代对象和任务，再引入术语与公式，补足决定性的计算步骤。
3. 保留原题条件、符号、单位、图和双语题答。按原文件完整单元顺序计数；注明教师材料、自己的推导或历史预习，不推测教师口头强调。
4. 只改Notebook说明时保持代码与输出。改了代码、参数或数据，则从干净内核运行对应Notebook，更新输出与解释；未运行的结果不能写成新成绩。
5. 运行`python scripts/validate.py`。影响正文或排版时运行`python scripts/build.py`，查看PDF的新页码、公式、长表、题图和跨页位置，随后提交源稿和对应PDF。
6. Pull Request说明改了什么、依据在哪里、实际检查了什么。合作者通过评论讨论，再合并。

中文负责讲懂，英文标题/术语和双语题答负责对照英语课堂。必要推理可以写长，重复提醒应合并；没有删字或加例子的配额。保持现有文件名和锚点，避免旧引用失效。

## 构建与实验分开

构建PDF使用`requirements-build.txt`，不需要Canvas数据，也不执行Notebook。运行实验另安装`requirements-notebooks.txt`并配置`COURSE_DATA_ROOT`，见[数据说明](docs/DATA.md)。不同系统的中文字体可能使分页变化，页码索引由最终PDF计算。

构建失败时先修源稿或依赖，保留上一次已验证PDF。不得用空白输出或假造图表绕过检查。
