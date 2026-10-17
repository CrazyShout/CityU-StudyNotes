# 逐节审阅记录

基线为`c805d278`。每行对应一个标题区段或开篇；标题使用审阅前名称，当前定位见源稿行号与PDF页。保留理由来自逐节阅读；原文、问题、处理详见相应修改编号。修改处与相邻段落已二读；未改段落仍保留原有推理，不以删字量作为验收。

图注、表格、图片与代码/输出另列于[组成部分审阅](COMPONENTS.md)。[逐项修改前后对照](CHANGES.md)保留准确原文。

## CS5489/course-notes/Lecture01.tex

| 区段与当前定位 | 问题／处理 | 保留内容与理由 |
|---|---|---|
| 00 · 开篇与导航<br>[源稿 L1](../../../CS5489/course-notes/Lecture01.tex#L1)；CS5489 p.7 | 保留（已审阅）；无须改写 | 章节身份与旧锚点保留；开篇内容在下一导读区段。 |
| 01 · 从“让机器学会认数字”，走到能读懂下一讲的代码<br>[源稿 L8](../../../CS5489/course-notes/Lecture01.tex#L8)；CS5489 p.7 | 保留（已审阅）；无须改写 | 保留输入、评价、数组轴与概率方向四项学习目标；可跳过的基础入口不扩展。 |
| 02 · Exam focus｜这一讲怎样安排复习<br>[源稿 L22](../../../CS5489/course-notes/Lecture01.tex#L22)；CS5489 p.7 | 修订并二读；E004 | 保留两行考点、来源计数与当前任务优先级；精简顺序套话。 |
| 03 · 1. What is Machine Learning?｜先把“学会了”说得可检验<br>[源稿 L51](../../../CS5489/course-notes/Lecture01.tex#L51)；CS5489 p.7 | 保留（已审阅）；无须改写 | 784像素图与T/E/P数字识别例衔接清楚；保留数据质量限制。 |
| 04 · 2. Topics in Machine Learning｜训练资料告诉了我们什么？<br>[源稿 L83](../../../CS5489/course-notes/Lecture01.tex#L83)；CS5489 p.8 | 保留（已审阅）；无须改写 | 分类/回归、无监督、强化学习用具体任务区分，双语题答有标签/反馈条件。 |
| 05 · 3. ML Training Pipeline｜先练习，再选方法，最后才验收<br>[源稿 L114](../../../CS5489/course-notes/Lecture01.tex#L114)；CS5489 p.9 | 保留（已审阅）；无须改写 | C的三候选验证例与独立变式完整；预处理也拟合、inference与evaluation不同是必要区分。 |
| 06 · 从训练和验证表现寻找下一步<br>[源稿 L145](../../../CS5489/course-notes/Lecture01.tex#L145)；CS5489 p.10 | 保留（已审阅）；无须改写 | 保留同总体与分布变化、收敛条件，避免仅凭两条错误率唯一诊断。 |
| 07 · 4. Python and Jupyter｜一本有记忆的实验笔记<br>[源稿 L180](../../../CS5489/course-notes/Lecture01.tex#L180)；CS5489 p.11 | 修订并二读；E002；E005 | 内核状态、Restart/Run All及旧locale环境边界保留；改标题便于查找。 |
| 08 · 5. Identifiers, variables and types｜变量像标签，先看贴在哪里<br>[源稿 L204](../../../CS5489/course-notes/Lecture01.tex#L204)；CS5489 p.11 | 修订并二读；E192 | 变量绑定、整除、对象身份清楚；修复双语自测的乘号丢失。 |
| 09 · 6. Lists, tuples, strings, dictionaries, sets｜先选对装东西的方式<br>[源稿 L239](../../../CS5489/course-notes/Lecture01.tex#L239)；CS5489 p.12 | 修订并二读；E006 | 容器表、右端排除与不可变对象条件保留；标题改为实际操作名称。 |
| 10 · 7. Conditional statements and loops｜把每轮变量变化写出来<br>[源稿 L284](../../../CS5489/course-notes/Lecture01.tex#L284)；CS5489 p.13 | 保留（已审阅）；无须改写 | 逐轮total和列表推导展开不删；原16倍代码勘误与偶数变式保留。 |
| 11 · 8. Functions and classes｜把动作封装，把状态放在对象里<br>[源稿 L333](../../../CS5489/course-notes/Lecture01.tex#L333)；CS5489 p.13 | 保留（已审阅）；无须改写 | MyList实例状态与类计数、print/return及原注释勘误保留；代码逐行保持。 |
| 12 · 9. File I/O, Pickle, exceptions and pandas｜读进来的是什么？<br>[源稿 L393](../../../CS5489/course-notes/Lecture01.tex#L393)；CS5489 p.14 | 保留（已审阅）；无须改写 | 读写模式、Pickle可信输入、异常分类及CSV表头各有操作意义，保留。 |
| 13 · 10. NumPy arrays｜先说清每根轴，再做计算<br>[源稿 L417](../../../CS5489/course-notes/Lecture01.tex#L417)；CS5489 p.15 | 保留（已审阅）；无须改写 | 四种数组属性、三维索引、行样本自测完整；不压缩成术语列表。 |
| 14 · 11. Shape manipulation and broadcasting｜形状对齐不靠猜<br>[源稿 L455](../../../CS5489/course-notes/Lecture01.tex#L455)；CS5489 p.15 | 保留（已审阅）；无须改写 | 广播两组形状与反例可独立推算；变式和答案保留。 |
| 15 · 12. Brief linear algebra review｜同一个乘号前后可能是不同东西<br>[源稿 L495](../../../CS5489/course-notes/Lecture01.tex#L495)；CS5489 p.16 | 修订并二读；E007 | 逐格乘积解释、两处原课勘误及改变B第二列的变式保留，标题点明运算。 |
| 16 · 13. Copies and views｜你改的是原件，还是副本？<br>[源稿 L542](../../../CS5489/course-notes/Lecture01.tex#L542)；CS5489 p.17 | 保留（已审阅）；无须改写 | 视图代码及shares_memory解释相互补充；保留预处理会改原数据的具体后果。 |
| 17 · 14. Visualizing data and probability｜图像和数字说同一句话<br>[源稿 L572](../../../CS5489/course-notes/Lecture01.tex#L572)；CS5489 p.17 | 保留（已审阅）；无须改写 | PMF/PDF图、Poisson观察区间、条件表与Bayes分母正条件保留；图注未取代公式讲解。 |
| 18 · 15. 合上讲义，检查自己能否讲明白<br>[源稿 L647](../../../CS5489/course-notes/Lecture01.tex#L647)；CS5489 p.20 | 保留（已审阅）；无须改写 | 三问分别检验预处理、数组与条件概率；复习图串联不同技能，有独立用途。 |
| 19 · 学习要求与难点回查<br>[源稿 L673](../../../CS5489/course-notes/Lecture01.tex#L673)；CS5489 p.20 | 保留（已审阅）；无须改写 | 主题表按掌握动作与难点定位，保留来源；课程要求边界留作表注。 |
| 20 · Historical exam map｜按考点查题源<br>[源稿 L698](../../../CS5489/course-notes/Lecture01.tex#L698)；CS5489 p.21 | 修订并二读；见相应源稿的修改与生成模板记录 | 生成模板去重复计数说明和自指链接；保留卷次冲突与QE身份。 |
| 21 · 训练、验证与最终评价<br>[源稿 L717](../../../CS5489/course-notes/Lecture01.tex#L717)；CS5489 p.21 | 保留（已审阅）；无须改写 | 保留原卷Q4的CV流程检索行，不改关联与题号。 |
| 22 · 训练与验证表现诊断<br>[源稿 L734](../../../CS5489/course-notes/Lecture01.tex#L734)；CS5489 p.21 | 修订并二读；见相应源稿的修改与生成模板记录 | 保留训练/验证诊断的各卷关系；生成题源条件应合并重复缺年份提醒。 |
| 23 · 原材料覆盖索引<br>[源稿 L765](../../../CS5489/course-notes/Lecture01.tex#L765)；CS5489 p.22 | 修订并二读；E003 | 覆盖表保留所有原单元定位；删去重复数据质量提醒并修正开头表格的旧指向。 |

## CS5489/course-notes/Lecture02.tex

| 区段与当前定位 | 问题／处理 | 保留内容与理由 |
|---|---|---|
| 00 · 开篇与导航<br>[源稿 L1](../../../CS5489/course-notes/Lecture02.tex#L1)；CS5489 p.23 | 保留（已审阅）；无须改写 | 花朵与邮件任务、前课关联、六段路线及先修入口清楚；保留连续学习顺序。 |
| 01 · Exam focus｜这一讲怎样安排复习<br>[源稿 L36](../../../CS5489/course-notes/Lecture02.tex#L36)；CS5489 p.23 | 修订并二读；见相应源稿的修改与生成模板记录 | 10类考点与卷数由原台账生成；不把缺证据写成不考。 |
| 02 · 1. From records to models｜从花朵记录到概率模型<br>[源稿 L66](../../../CS5489/course-notes/Lecture02.tex#L66)；CS5489 p.24 | 保留（已审阅）；无须改写 | 一级标题组织记录到模型；说明在下属三节展开，未额外加空泛导语。 |
| 03 · Features and labels｜先认清一条记录<br>[源稿 L74](../../../CS5489/course-notes/Lecture02.tex#L74)；CS5489 p.24 | 保留（已审阅）；无须改写 | 花部位图、两类照片与记录向量互补；列向量/行数据约定明确。 |
| 04 · Prior and class-conditional distribution｜分别描述类别和测量<br>[源稿 L127](../../../CS5489/course-notes/Lecture02.tex#L127)；CS5489 p.26 | 保留（已审阅）；无须改写 | 先验、类条件、后验先用任务区分，再引入指示函数，保留。 |
| 05 · Maximum likelihood estimation｜从记录估计类别比例<br>[源稿 L175](../../../CS5489/course-notes/Lecture02.tex#L175)；CS5489 p.27 | 保留（已审阅）；无须改写 | 4/6标签例解释独立乘积、log单调、二阶导及边界；抽样先验限制保留。 |
| 06 · 2. Gaussian observations｜用高斯描述一类花的测量<br>[源稿 L234](../../../CS5489/course-notes/Lecture02.tex#L234)；CS5489 p.27 | 保留（已审阅）；无须改写 | 高斯一级标题承接两小节，无需重复预告。 |
| 07 · From histograms to a density｜先看数据集中在哪里<br>[源稿 L241](../../../CS5489/course-notes/Lecture02.tex#L241)；CS5489 p.27 | 保留（已审阅）；无须改写 | 直方图密度尺度、cm逆单位、面积与单点概率完整；图文用途不同。 |
| 08 · Estimating mean and variance｜把高斯参数从数据里算出来<br>[源稿 L279](../../../CS5489/course-notes/Lecture02.tex#L279)；CS5489 p.28 | 保留（已审阅）；无须改写 | 均值/方差求导、2/4/6 cm示范、N与N-1及退化条件完整，原样保留。 |
| 09 · 3. Bayesian decision｜给一朵新花作判断<br>[源稿 L371](../../../CS5489/course-notes/Lecture02.tex#L371)；CS5489 p.30 | 保留（已审阅）；无须改写 | Bayes主题标签与下属完整演算保持，不机械新增总结。 |
| 10 · From a measurement to a posterior｜把5厘米代进模型<br>[源稿 L383](../../../CS5489/course-notes/Lecture02.tex#L383)；CS5489 p.30 | 保留（已审阅）；无须改写 | 5 cm演算由密度到后验，表格显示中间值；舍入身份、归一化与读图保留。 |
| 11 · Why the prior matters｜更常见的类别也会影响判断<br>[源稿 L449](../../../CS5489/course-notes/Lecture02.tex#L449)；CS5489 p.31 | 保留（已审阅）；无须改写 | 0.4/0.2密度例单独改变先验，解释等代价0-1损失的最大后验规则。 |
| 12 · Comparing log scores｜很多小数相乘时怎样算得稳<br>[源稿 L469](../../../CS5489/course-notes/Lecture02.tex#L469)；CS5489 p.31 | 保留（已审阅）；无须改写 | log平移用(-1001,-1000)解释下溢，零分数条件必要，保留。 |
| 13 · Where the boundary comes from｜两个类别在哪里打平<br>[源稿 L499](../../../CS5489/course-notes/Lecture02.tex#L499)；CS5489 p.32 | 修订并二读；E012 | 共享/不同方差两次展开和配平方推根都可跟算；图示预测区不替代推导。 |
| 14 · 4. Multiple features｜同时使用两项测量<br>[源稿 L621](../../../CS5489/course-notes/Lecture02.tex#L621)；CS5489 p.34 | 保留（已审阅）；无须改写 | 多特征主题按NB到完整高斯，保持层次。 |
| 15 · Gaussian Naive Bayes｜先分别看两项测量<br>[源稿 L634](../../../CS5489/course-notes/Lecture02.tex#L634)；CS5489 p.34 | 保留（已审阅）；无须改写 | 条件独立按类解释，表格参数/单位与train-only拟合及19/31先验完整。 |
| 16 · Shared variances and boundary shape｜两项测量的边界怎样连起来<br>[源稿 L705](../../../CS5489/course-notes/Lecture02.tex#L705)；CS5489 p.35 | 保留（已审阅）；无须改写 | 逐特征差值、C只加一次、共享方差范围及两维变式完整保留。 |
| 17 · Test results｜用没参与拟合的花检查模型<br>[源稿 L779](../../../CS5489/course-notes/Lecture02.tex#L779)；CS5489 p.36 | 保留（已审阅）；无须改写 | 点A的真值/后验与整体42/50区别明确；图例和错分解释保留。 |
| 18 · Full covariance｜两项测量会一起变化时<br>[源稿 L805](../../../CS5489/course-notes/Lecture02.tex#L805)；CS5489 p.37 | 保留（已审阅）；无须改写 | 四格协方差、四图、马氏距离及行列式各补不同理解台阶，保留。 |
| 19 · A complete Gaussian decision｜三项一起算完<br>[源稿 L868](../../../CS5489/course-notes/Lecture02.tex#L868)；CS5489 p.39 | 保留（已审阅）；无须改写 | 给定协方差完整求逆和三项分数，等先验/等代价、无量纲条件及答案保留。 |
| 20 · Learning and implementing the full model｜回到老师的GaussianBayes<br>[源稿 L932](../../../CS5489/course-notes/Lecture02.tex#L932)；CS5489 p.40 | 保留（已审阅）；无须改写 | 类内外积平均、正则单位、模型接口及N-1实现差异必要；不删测试对照。 |
| 21 · 5. Evidence from words｜把邮件变成分类证据<br>[源稿 L981](../../../CS5489/course-notes/Lecture02.tex#L981)；CS5489 p.41 | 保留（已审阅）；无须改写 | 邮件主题引入BoW，不额外堆说明。 |
| 22 · Bag-of-words｜给文字安排固定的位置<br>[源稿 L993](../../../CS5489/course-notes/Lecture02.tex#L993)；CS5489 p.41 | 保留（已审阅）；无须改写 | 固定词表与丢词序原例、not停用词反例具体；原词袋图保留。 |
| 23 · Fit and transform｜训练资料决定词表<br>[源稿 L1016](../../../CS5489/course-notes/Lecture02.tex#L1016)；CS5489 p.41 | 保留（已审阅）；无须改写 | fit/transform代码与稀疏零值含义互补，保留。 |
| 24 · Bernoulli NB｜一个词没出现，也是一条证据<br>[源稿 L1045](../../../CS5489/course-notes/Lecture02.tex#L1045)；CS5489 p.42 | 保留（已审阅）；无须改写 | 出现/未出现的两词乘积到完整log分数推理清楚，保留。 |
| 25 · Additive smoothing｜没有见过，不等于绝不可能<br>[源稿 L1083](../../../CS5489/course-notes/Lecture02.tex#L1083)；CS5489 p.42 | 保留（已审阅）；无须改写 | 2alpha分母与3篇/类完整手算有明确条件，双语答案一致。 |
| 26 · Frequent and informative words｜常见与能区分，是两件事<br>[源稿 L1124](../../../CS5489/course-notes/Lecture02.tex#L1124)；CS5489 p.43 | 保留（已审阅）；无须改写 | 0.9/0.9与0.6/0.1区分类内频率和区分性，非重复说明。 |
| 27 · A real misclassified message｜为什么手表广告被当成正常邮件<br>[源稿 L1144](../../../CS5489/course-notes/Lecture02.tex#L1144)；CS5489 p.43 | 保留（已审阅）；无须改写 | 原手表广告、全零向量与log贡献说明高后验错分，不删真实样本解释。 |
| 28 · 6. Counts and weights｜从词次数到文本权重<br>[源稿 L1180](../../../CS5489/course-notes/Lecture02.tex#L1180)；CS5489 p.44 | 保留（已审阅）；无须改写 | 计数与权重一级主题与前文Bernoulli衔接自然。 |
| 29 · TF and IDF｜先把一个向量完整算出来<br>[源稿 L1187](../../../CS5489/course-notes/Lecture02.tex#L1187)；CS5489 p.44 | 保留（已审阅）；无须改写 | 四篇短文贯穿TF/IDF，文档频数和词次数区分具体，保留数据表。 |
| 30 · The classroom transformer｜把同一例子接到老师的代码<br>[源稿 L1253](../../../CS5489/course-notes/Lecture02.tex#L1253)；CS5489 p.44 | 保留（已审阅）；无须改写 | 库IDF、L1以及课堂简式差异逐步落实到相同D1，保留。 |
| 31 · Multinomial NB｜先理解词计数模型<br>[源稿 L1331](../../../CS5489/course-notes/Lecture02.tex#L1331)；CS5489 p.45 | 保留（已审阅）；无须改写 | 文长条件、组合系数与总和约束解释齐全；新邮件完整题答保留。 |
| 32 · Weighted features in the same classifier｜小数权重怎样进入模型<br>[源稿 L1378](../../../CS5489/course-notes/Lecture02.tex#L1378)；CS5489 p.46 | 保留（已审阅）；无须改写 | 逐列累积权重、分母6和加权log分数可跟算，保留模型概率身份。 |
| 33 · Return to the classroom experiment｜老师的邮件比较说明什么<br>[源稿 L1431](../../../CS5489/course-notes/Lecture02.tex#L1431)；CS5489 p.47 | 保留（已审阅）；无须改写 | 64/72/68%三行是教师保存输出；比较两条完整流程与探索性测试限制保留。 |
| 34 · Other representations｜词袋之外还有哪些改法<br>[源稿 L1465](../../../CS5489/course-notes/Lecture02.tex#L1465)；CS5489 p.47 | 保留（已审阅）；无须改写 | 五类表示各有用途例子；模型校准限制直接关联输出，不删。 |
| 35 · Review｜把整讲串起来<br>[源稿 L1503](../../../CS5489/course-notes/Lecture02.tex#L1503)；CS5489 p.48 | 保留（已审阅）；无须改写 | 模型比较表汇总不同输入/参数/假设，有复习用途，保留。 |
| 36 · When more data still leaves errors｜为什么学得更准，仍会分错<br>[源稿 L1538](../../../CS5489/course-notes/Lecture02.tex#L1538)；CS5489 p.48 | 保留（已审阅）；无须改写 | 同分布0.5/0.5例与估计误差/失配/重叠区分是实质推理，保留。 |
| 37 · Explain in English｜五个短自测<br>[源稿 L1576](../../../CS5489/course-notes/Lecture02.tex#L1576)；CS5489 p.49 | 保留（已审阅）；无须改写 | 五问中英对象、数据、条件与答案一致；没有机械新增题。 |
| 38 · Try a changed condition｜三个独立变式<br>[源稿 L1618](../../../CS5489/course-notes/Lecture02.tex#L1618)；CS5489 p.50 | 修订并二读；E008；E009；E010；E011；E189 | 三道改变条件的题保留原数据；Q6/Q8补页码入口，Q7保留完整协方差与先验。 |
| 39 · Implementation details｜原代码使用说明（选读）<br>[源稿 L1684](../../../CS5489/course-notes/Lecture02.tex#L1684)；CS5489 p.51 | 保留（已审阅）；无须改写 | 选读只承接实现细节，理解主线所需步骤已在正文。 |
| 40 · Density plots and boundaries｜直方图与边界代码<br>[源稿 L1693](../../../CS5489/course-notes/Lecture02.tex#L1693)；CS5489 p.51 | 保留（已审阅）；无须改写 | 计数/密度原标注、95.45%范围和网格交点限制必要，保留。 |
| 41 · Log-sum-exp｜从log分数恢复概率<br>[源稿 L1707](../../../CS5489/course-notes/Lecture02.tex#L1707)；CS5489 p.51 | 保留（已审阅）；无须改写 | logsumexp补偿m与全负无穷条件完整；原编号不改。 |
| 42 · Split, covariance and labels｜划分、估计器与标签<br>[源稿 L1725](../../../CS5489/course-notes/Lecture02.tex#L1725)；CS5489 p.52 | 保留（已审阅）；无须改写 | 6项实现差异影响复现或理解，保留原随机种子、估计器、标签映射。 |
| 43 · Text code details｜文本读取、显示和模型对象<br>[源稿 L1748](../../../CS5489/course-notes/Lecture02.tex#L1748)；CS5489 p.52 | 修订并二读；E012；E013 | 模型对象误用和alpha版本边界保留；链接中的版本哈希说明收回维护记录。 |
| 44 · Priorities and sources｜重难点与依据<br>[源稿 L1765](../../../CS5489/course-notes/Lecture02.tex#L1765)；CS5489 p.52 | 保留（已审阅）；无须改写 | 难度和优先级表功能不同；当前/历史东莞材料身份保留。 |
| 45 · Historical exam map｜按考点查题源<br>[源稿 L1801](../../../CS5489/course-notes/Lecture02.tex#L1801)；CS5489 p.53 | 修订并二读；见相应源稿的修改与生成模板记录 | 生成模板合并计数口径及自指提示，保留卷次冲突、QE边界与附录入口。 |
| 46 · 生成式模型与概率分工<br>[源稿 L1817](../../../CS5489/course-notes/Lecture02.tex#L1817)；CS5489 p.53 | 保留（已审阅）；无须改写 | 保留8行生成式原题映射，样题与真卷分别标识。 |
| 47 · Bayes决策与先验作用<br>[源稿 L1841](../../../CS5489/course-notes/Lecture02.tex#L1841)；CS5489 p.53 | 保留（已审阅）；无须改写 | 保留先验决策的原卷题号与技能，不扩成新题。 |
| 48 · 条件独立与Gaussian NB<br>[源稿 L1864](../../../CS5489/course-notes/Lecture02.tex#L1864)；CS5489 p.54 | 保留（已审阅）；无须改写 | 保留Gaussian NB题源表与条件独立要求。 |
| 49 · MLE学习思想<br>[源稿 L1887](../../../CS5489/course-notes/Lecture02.tex#L1887)；CS5489 p.54 | 保留（已审阅）；无须改写 | 保留两套直接题与QE残题，条件未齐不计完整推导。 |
| 50 · 线性与非线性边界<br>[源稿 L1906](../../../CS5489/course-notes/Lecture02.tex#L1906)；CS5489 p.54 | 保留（已审阅）；无须改写 | 保留共享方差/边界题和聚类关联身份。 |
| 51 · 协方差与高斯形状<br>[源稿 L1927](../../../CS5489/course-notes/Lecture02.tex#L1927)；CS5489 p.55 | 保留（已审阅）；无须改写 | 保留协方差的期中/期末关联列表与页码。 |
| 52 · 平滑与正则化<br>[源稿 L1951](../../../CS5489/course-notes/Lecture02.tex#L1951)；CS5489 p.55 | 保留（已审阅）；无须改写 | 保留平滑题与样题标签，计数不改。 |
| 53 · 文本表示与NB改进<br>[源稿 L1970](../../../CS5489/course-notes/Lecture02.tex#L1970)；CS5489 p.55 | 保留（已审阅）；无须改写 | 保留表示改进原题映射；实际正文已有相应例子。 |
| 54 · 误差、不确定性与模型局限<br>[源稿 L1988](../../../CS5489/course-notes/Lecture02.tex#L1988)；CS5489 p.56 | 保留（已审阅）；无须改写 | 保留无限数据、失配与重叠原题关系。 |
| 55 · 参数后验与MAP（QE延伸）<br>[源稿 L2009](../../../CS5489/course-notes/Lecture02.tex#L2009)；CS5489 p.56 | 保留（已审阅）；无须改写 | 参数后验/MAP与类别后验区别必要；残题缺模型及先验说明保留。 |
| 56 · Source coverage｜回到老师的原课<br>[源稿 L2034](../../../CS5489/course-notes/Lecture02.tex#L2034)；CS5489 p.56 | 保留（已审阅）；无须改写 | 149原单元覆盖及PDF页索引保留；教师输出与教学算例身份明确。 |

## CS5489/course-notes/Lecture03.tex

| 区段与当前定位 | 问题／处理 | 保留内容与理由 |
|---|---|---|
| 00 · 开篇与导航<br>[源稿 L1](../../../CS5489/course-notes/Lecture03.tex#L1)；CS5489 p.58 | 保留（已审阅）；无须改写 | 花朵任务承接生成式到判别式，原课顺序及先修回链保留。 |
| 01 · Exam focus｜这一讲怎样安排复习<br>[源稿 L17](../../../CS5489/course-notes/Lecture03.tex#L17)；CS5489 p.58 | 修订并二读；E027 | 历史考点表全部计数和入口保留，精简导航套话。 |
| 02 · 1. Generative versus discriminative｜先弄懂我们换了什么目标<br>[源稿 L54](../../../CS5489/course-notes/Lecture03.tex#L54)；CS5489 p.59 | 保留（已审阅）；无须改写 | 共享标量方差、r=-Delta的方向和log比值展开完整；跨讲符号区别不能删。 |
| 03 · 2. Linear classifier and separating hyperplane｜一张有方向的分界线<br>[源稿 L112](../../../CS5489/course-notes/Lecture03.tex#L112)；CS5489 p.60 | 修订并二读；E028 | ±1标签、平局条件和超平面维度保留；标题去生硬搭配，图与自测不改。 |
| 04 · 3. Logistic regression｜把分数翻译成概率<br>[源稿 L149](../../../CS5489/course-notes/Lecture03.tex#L149)；CS5489 p.61 | 修订并二读；E029 | sigmoid到条件似然、±1限制和损失数值保留；不买账改为概率与损失关系。 |
| 05 · 4. Regularization and optimization｜限制大权重，减少过拟合<br>[源稿 L189](../../../CS5489/course-notes/Lecture03.tex#L189)；CS5489 p.61 | 修订并二读；E030 | MAP高斯先验到平方惩罚、两级链式求导和同步更新保留；软件缩放另起段。 |
| 06 · 换成L1惩罚，分类器会怎样变？<br>[源稿 L241](../../../CS5489/course-notes/Lecture03.tex#L241)；CS5489 p.62 | 保留（已审阅）；无须改写 | 两组线性权重说明稀疏不等于非线性；L1不保证零系数条件保留。 |
| 07 · 凸目标不等于一定有唯一的有限解<br>[源稿 L268](../../../CS5489/course-notes/Lecture03.tex#L268)；CS5489 p.62 | 保留（已审阅）；无须改写 | 单点无有限最优解反例完整，保留凸性/存在/唯一三个问题的区别。 |
| 08 · 5. Iris example and cross-validation｜让验证集帮我们选 C<br>[源稿 L286](../../../CS5489/course-notes/Lecture03.tex#L286)；CS5489 p.63 | 保留（已审阅）；无须改写 | 保留原划分、训练内CV、每折Pipeline及旧接口说明；代码不改。 |
| 09 · 6. Multiclass classification｜从二类扩展到多类<br>[源稿 L322](../../../CS5489/course-notes/Lecture03.tex#L322)；CS5489 p.63 | 保留（已审阅）；无须改写 | OvR独立训练与softmax共同分母、one-hot算例区分清楚，保留。 |
| 10 · 7. Maximum margin｜不仅分开，还想留出余地<br>[源稿 L351](../../../CS5489/course-notes/Lecture03.tex#L351)；CS5489 p.64 | 修订并二读；E031 | 距离归一化、单侧/总宽度与两点最优解保留；标题定位概念。 |
| 11 · 8. Lagrangian and duality｜用样本乘子求解最大间隔<br>[源稿 L388](../../../CS5489/course-notes/Lecture03.tex#L388)；CS5489 p.64 | 保留（已审阅）；无须改写 | 约束正负号、b下界、四项代回、双重求和与两点对偶复核不可删；强对偶选读保留。 |
| 12 · 9. KKT and support vectors｜乘子告诉我们哪条约束在起作用<br>[源稿 L504](../../../CS5489/course-notes/Lecture03.tex#L504)；CS5489 p.66 | 保留（已审阅）；无须改写 | KKT单向蕴含和退化边界、±2变式完整保留。 |
| 13 · 10. Soft-margin SVM｜允许有代价的违规<br>[源稿 L551](../../../CS5489/course-notes/Lecture03.tex#L551)；CS5489 p.67 | 保留（已审阅）；无须改写 | slack正确分类反例、因子2、三类乘子边界和有限C可等硬间隔的纠正项保留。 |
| 14 · 11. Multiclass SVM and kernel trick｜直线不够，就改变表示<br>[源稿 L617](../../../CS5489/course-notes/Lecture03.tex#L617)；CS5489 p.68 | 保留（已审阅）；无须改写 | OvO训练区别、XOR新特征、二次映射重复交叉项和核约束完整。 |
| 15 · 原始问题、对偶问题与预测存储<br>[源稿 L652](../../../CS5489/course-notes/Lecture03.tex#L652)；CS5489 p.69 | 保留（已审阅）；无须改写 | 训练未知数与部署存储分别计数，保留实际支持向量和忽略开销条件。 |
| 16 · 12. RBF and custom kernels｜相似度也有尺度<br>[源稿 L678](../../../CS5489/course-notes/Lecture03.tex#L678)；CS5489 p.69 | 保留（已审阅）；无须改写 | 核矩阵逐格示范、PSD反例和任意样本条件保留；Euclidean/L1差异不合并。 |
| 17 · 13. Features, scaling and imbalance｜同一模型也会被表示方式影响<br>[源稿 L737](../../../CS5489/course-notes/Lecture03.tex#L737)；CS5489 p.70 | 保留（已审阅）；无须改写 | 标准化定义、类别编码、数量不平衡与代价权重各有对象；原0/1含义不擅改。 |
| 18 · 改类别权重，与改预测阈值<br>[源稿 L774](../../../CS5489/course-notes/Lecture03.tex#L774)；CS5489 p.71 | 保留（已审阅）；无须改写 | 重训权重与预测阈值区别用三概率检验，真实标签条件保留。 |
| 19 · 14. Classification summary｜把不同方法放在同一张地图<br>[源稿 L797](../../../CS5489/course-notes/Lecture03.tex#L797)；CS5489 p.71 | 修订并二读；E032 | 比较表和统一损失说明各模型实际学习对象，标题去地图比喻。 |
| 20 · 看损失曲线时，先看横轴<br>[源稿 L829](../../../CS5489/course-notes/Lecture03.tex#L829)；CS5489 p.72 | 保留（已审阅）；无须改写 | 非标准loss零惩罚错分反例与指数损失数值保留。 |
| 21 · 参数少，具体少在哪里<br>[源稿 L855](../../../CS5489/course-notes/Lecture03.tex#L855)；CS5489 p.72 | 保留（已审阅）；无须改写 | 学习先验与共享方差参数计数条件明确；NFL说明只限定模型比较边界。 |
| 22 · 15. Back to the tutorial and English self-test｜从本讲走向实践<br>[源稿 L884](../../../CS5489/course-notes/Lecture03.tex#L884)；CS5489 p.73 | 保留（已审阅）；无须改写 | 四组双语自测与Tutorial3接续保留，答案包含必要条件。 |
| 23 · 学习要求与难点回查<br>[源稿 L908](../../../CS5489/course-notes/Lecture03.tex#L908)；CS5489 p.73 | 保留（已审阅）；无须改写 | 优先级/难度表为检索用，不再增正文预告。 |
| 24 · Historical exam map｜按考点查题源<br>[源稿 L934](../../../CS5489/course-notes/Lecture03.tex#L934)；CS5489 p.74 | 修订并二读；见相应源稿的修改与生成模板记录 | 模板删自指与重复口径；核PCA关联范围保留。 |
| 25 · 生成式与判别式<br>[源稿 L953](../../../CS5489/course-notes/Lecture03.tex#L953)；CS5489 p.74 | 保留（已审阅）；无须改写 | 保留三套生成/判别原题映射与直接关系。 |
| 26 · 模型参数计数<br>[源稿 L972](../../../CS5489/course-notes/Lecture03.tex#L972)；CS5489 p.74 | 保留（已审阅）；无须改写 | 原2023B Q8先验自由参数条件保留。 |
| 27 · Logistic似然与优化<br>[源稿 L991](../../../CS5489/course-notes/Lecture03.tex#L991)；CS5489 p.74 | 保留（已审阅）；无须改写 | 各卷logistic/MAP原题号保留，凸有限解和分数/概率勘误保留。 |
| 28 · 正则化、MAP与CV<br>[源稿 L1020](../../../CS5489/course-notes/Lecture03.tex#L1020)；CS5489 p.75 | 保留（已审阅）；无须改写 | 重复出现的同一原题属不同考点映射，不能为去冗余删行。 |
| 29 · SVM间隔、松弛与对偶<br>[源稿 L1046](../../../CS5489/course-notes/Lecture03.tex#L1046)；CS5489 p.75 | 保留（已审阅）；无须改写 | SVM多卷映射及极大C不能消除冲突标签的条件保留。 |
| 30 · 核技巧与合法性<br>[源稿 L1074](../../../CS5489/course-notes/Lecture03.tex#L1074)；CS5489 p.76 | 保留（已审阅）；无须改写 | 核题映射含期末关联KPCA，保留当前知识覆盖边界。 |
| 31 · 求解维度与预测存储<br>[源稿 L1108](../../../CS5489/course-notes/Lecture03.tex#L1108)；CS5489 p.77 | 保留（已审阅）；无须改写 | 存储原题及C/支持向量数不单调纠正保留。 |
| 32 · 不平衡、代价与阈值<br>[源稿 L1129](../../../CS5489/course-notes/Lecture03.tex#L1129)；CS5489 p.77 | 保留（已审阅）；无须改写 | 代价、数量与阈值六组原题定位保留。 |
| 33 · 分类损失曲线<br>[源稿 L1151](../../../CS5489/course-notes/Lecture03.tex#L1151)；CS5489 p.77 | 保留（已审阅）；无须改写 | 损失曲线原题检索表有不同历史题入口，原样保持。 |
| 34 · 16. 原课疑点与覆盖索引<br>[源稿 L1175](../../../CS5489/course-notes/Lecture03.tex#L1175)；CS5489 p.78 | 保留（已审阅）；无须改写 | 十项已确认勘误、全部原单元及四页手写图保留；图注明确原件疑点不作为正确公式。 |

## CS5489/course-notes/Lecture04.tex

| 区段与当前定位 | 问题／处理 | 保留内容与理由 |
|---|---|---|
| 00 · 开篇与导航<br>[源稿 L1](../../../CS5489/course-notes/Lecture04.tex#L1)；CS5489 p.81 | 保留（已审阅）；无须改写 | 房价任务、前课与Tutorial4连接和三个数学入口保留，未新增教学范围。 |
| 01 · Exam focus｜这一讲怎样安排复习<br>[源稿 L20](../../../CS5489/course-notes/Lecture04.tex#L20)；CS5489 p.81 | 修订并二读；E033 | 历史考点统计与技能动作保留；导航只留学习要求入口。 |
| 02 · 1. Regression and the housing example｜先弄清横纵轴的单位<br>[源稿 L54](../../../CS5489/course-notes/Lecture04.tex#L54)；CS5489 p.82 | 修订并二读；E034 | mode1/2单位、12维与行采样说明完整；竖直残差区别改得更明确。 |
| 03 · 2. Linear regression and OLS｜找一条总体偏差较小的线<br>[源稿 L97](../../../CS5489/course-notes/Lecture04.tex#L97)；CS5489 p.82 | 保留（已审阅）；无须改写 | 三点表到斜率/截距、SSE/MSE逐步演算保留，读者可独立跟算。 |
| 04 · 斜率和截距的公式从哪里来？<br>[源稿 L149](../../../CS5489/course-notes/Lecture04.tex#L149)；CS5489 p.83 | 保留（已审阅）；无须改写 | 固定斜率求截距、中心化求斜率、全相同输入反例及二阶条件保留。 |
| 05 · 3. Matrix solution｜先摆好矩阵，再求导<br>[源稿 L193](../../../CS5489/course-notes/Lecture04.tex#L193)；CS5489 p.84 | 修订并二读；E035 | 列样本与行代码、满行秩条件及同三点矩阵核对保留；英文变式补齐三点。 |
| 06 · 为什么要和“永远预测平均值”比较？<br>[源稿 L270](../../../CS5489/course-notes/Lecture04.tex#L270)；CS5489 p.85 | 保留（已审阅）；无须改写 | 同一训练集OLS不劣于均值基线的包含关系是关键解释，保留。 |
| 07 · 4. Housing coefficients and feature selection｜大权重必须配着单位读<br>[源稿 L290](../../../CS5489/course-notes/Lecture04.tex#L290)；CS5489 p.86 | 保留（已审阅）；无须改写 | 房价原输出身份、特征单位与相关性解释保留。 |
| 08 · 5. Ridge regression｜用平方惩罚稳定系数<br>[源稿 L307](../../../CS5489/course-notes/Lecture04.tex#L307)；CS5489 p.86 | 保留（已审阅）；无须改写 | 重复特征两种权重、无截距小算例和正定证明互补，保留alpha约定。 |
| 09 · 6. LASSO｜有时需要真的把系数变成零<br>[源稿 L374](../../../CS5489/course-notes/Lecture04.tex#L374)；CS5489 p.87 | 修订并二读；E036 | 图的约束接触、分段导数与软阈值保留；标题直接写L1和零系数。 |
| 10 · 7. Sparsity and OMP｜每次挑方向，但要回头一起重拟合<br>[源稿 L437](../../../CS5489/course-notes/Lecture04.tex#L437)；CS5489 p.89 | 保留（已审阅）；无须改写 | 归一化列的内积绝对值、两轮联合重拟合和负相关例保留。 |
| 11 · 选读：改残差的惩罚，与改权重的惩罚<br>[源稿 L474](../../../CS5489/course-notes/Lecture04.tex#L474)；CS5489 p.89 | 保留（已审阅）；无须改写 | 残差L1/Huber、非对称代价与Elastic Net分清惩罚对象，保留历史身份。 |
| 12 · 8. RANSAC｜用相互一致的数据点拟合<br>[源稿 L534](../../../CS5489/course-notes/Lecture04.tex#L534)；CS5489 p.90 | 修订并二读；E037 | 抽样条件、阈值单位、四点重拟合与变式完整；概率说明另起段便于跟读。 |
| 13 · 9. Polynomial regression｜对输入非线性，对参数仍线性<br>[源稿 L589](../../../CS5489/course-notes/Lecture04.tex#L589)；CS5489 p.92 | 保留（已审阅）；无须改写 | 输入非线性/参数线性、训练SSE嵌套条件和总次数笔误保留。 |
| 14 · 10. Kernel ridge regression｜用训练样本的核值预测<br>[源稿 L622](../../../CS5489/course-notes/Lecture04.tex#L622)；CS5489 p.92 | 保留（已审阅）；无须改写 | 样本系数从驻点推导、同一线性核双算法例与截距条件完整，保留。 |
| 15 · 11. Support vector regression｜在容忍带内不追究小误差<br>[源稿 L686](../../../CS5489/course-notes/Lecture04.tex#L686)；CS5489 p.93 | 修订并二读；E038 | 半宽/总宽、epsilon-insensitive原纠错保留；改图文重复为对应关系。 |
| 16 · 12. Trees and random forests｜把多棵回归树的预测取平均<br>[源稿 L707](../../../CS5489/course-notes/Lecture04.tex#L707)；CS5489 p.94 | 保留（已审阅）；无须改写 | bootstrap具体索引、回归平均与训练曲线身份保留。 |
| 17 · 选读：树很多，为什么仍有误差？<br>[源稿 L737](../../../CS5489/course-notes/Lecture04.tex#L737)；CS5489 p.95 | 保留（已审阅）；无须改写 | 等方差/等相关条件、协方差展开与极限变式完整，保留。 |
| 18 · 13. Boosting and XGBoost｜后一棵树接着修前面的误差<br>[源稿 L765](../../../CS5489/course-notes/Lecture04.tex#L765)；CS5489 p.95 | 保留（已审阅）；无须改写 | 正梯度减/负梯度加、一次数值更新、训练/预测并行区别保留。 |
| 19 · 14. Comparing regression methods｜模型、目标、假设一起记<br>[源稿 L791](../../../CS5489/course-notes/Lecture04.tex#L791)；CS5489 p.96 | 保留（已审阅）；无须改写 | 模型比较表与目标log反变换条件必要，保持。 |
| 20 · 15. English self-test and review｜解释清楚再复习<br>[源稿 L824](../../../CS5489/course-notes/Lecture04.tex#L824)；CS5489 p.97 | 保留（已审阅）；无须改写 | 四组英文自测与中文关键答案对应，不另加总结。 |
| 21 · 学习要求与难点回查<br>[源稿 L845](../../../CS5489/course-notes/Lecture04.tex#L845)；CS5489 p.97 | 保留（已审阅）；无须改写 | 学习动作、难点和原课依据表有检索作用，保留。 |
| 22 · Historical exam map｜按考点查题源<br>[源稿 L870](../../../CS5489/course-notes/Lecture04.tex#L870)；CS5489 p.97 | 修订并二读；见相应源稿的修改与生成模板记录 | 模板删除相邻重复及自指，历史额外方法边界保持。 |
| 23 · OLS与基线<br>[源稿 L889](../../../CS5489/course-notes/Lecture04.tex#L889)；CS5489 p.98 | 保留（已审阅）；无须改写 | OLS验证基线原题单行定位保留。 |
| 24 · Ridge、LASSO与特征选择<br>[源稿 L906](../../../CS5489/course-notes/Lecture04.tex#L906)；CS5489 p.98 | 保留（已审阅）；无须改写 | Ridge/LASSO/Elastic Net各原卷关系保留。 |
| 25 · 稳健与非对称残差损失<br>[源稿 L931](../../../CS5489/course-notes/Lecture04.tex#L931)；CS5489 p.98 | 保留（已审阅）；无须改写 | 损失分段与非对称成本原题表保留，不混为权重正则化。 |
| 26 · Bagging、RF与boosting<br>[源稿 L955](../../../CS5489/course-notes/Lecture04.tex#L955)；CS5489 p.99 | 保留（已审阅）；无须改写 | 分类/回归、GP关联与boosting预测并行的来源条件不可删。 |
| 27 · 树间相关性与平均方差<br>[源稿 L983](../../../CS5489/course-notes/Lecture04.tex#L983)；CS5489 p.99 | 保留（已审阅）；无须改写 | 等方差等相关历史题与正文公式匹配，保留。 |
| 28 · 核回归与SVR<br>[源稿 L1000](../../../CS5489/course-notes/Lecture04.tex#L1000)；CS5489 p.99 | 保留（已审阅）；无须改写 | SVR原题选项关系不扩展为新内容，保留。 |
| 29 · 16. Source coverage and execution boundary｜能回查，也能知道哪些跑过<br>[源稿 L1019](../../../CS5489/course-notes/Lecture04.tex#L1019)；CS5489 p.100 | 修订并二读；E039 | 原单元、数据身份、未重跑大型搜索和已确认勘误保留；标题明确复算范围。 |

## CS5489/course-notes/Lecture05.tex

| 区段与当前定位 | 问题／处理 | 保留内容与理由 |
|---|---|---|
| 00 · 开篇与导航<br>[源稿 L1](../../../CS5489/course-notes/Lecture05.tex#L1)；CS5489 p.101 | 保留（已审阅）；无须改写 | 书内章节身份和旧锚点保留。 |
| 01 · 从一条分类线，到能自己学特征的网络<br>[源稿 L8](../../../CS5489/course-notes/Lecture05.tex#L8)；CS5489 p.101 | 修订并二读；E040 | 花朵分类引出中间特征，先修入口与作业连接保持；只简化表格导航。 |
| 02 · Exam focus｜这一讲怎样安排复习<br>[源稿 L25](../../../CS5489/course-notes/Lecture05.tex#L25)；CS5489 p.101 | 保留（已审阅）；无须改写 | 历史激活/反传/优化题范围和计数保留，期中期末身份区分。 |
| 03 · 1. Perceptron｜先做一个会纠错的线性判断器<br>[源稿 L56](../../../CS5489/course-notes/Lecture05.tex#L56)；CS5489 p.102 | 保留（已审阅）；无须改写 | 感知机平局与原z<0代码区别、一次更新和可分条件保留。 |
| 04 · 2. Multiclass logistic regression｜三个分数，怎样成为三个概率？<br>[源稿 L112](../../../CS5489/course-notes/Lecture05.tex#L112)；CS5489 p.102 | 修订并二读；E042；E172 | softmax正值/归一化、稳定平移及接口说明完整；变式补原logits。 |
| 05 · 3. Cross-entropy and MLE｜惩罚给真类太少的概率<br>[源稿 L161](../../../CS5489/course-notes/Lecture05.tex#L161)；CS5489 p.104 | 保留（已审阅）；无须改写 | one-hot、真类概率与argmin对象区别完整，保留。 |
| 06 · 4. Chain rule｜先走完一个只有输出层的反向传播<br>[源稿 L190](../../../CS5489/course-notes/Lecture05.tex#L190)；CS5489 p.104 | 修订并二读；E043 | 商法则到p-y逐项求和不删；补一步题补齐两种语言的概率/损失条件。 |
| 07 · 5. Multi-layer perceptron｜把特征也变成可训练的<br>[源稿 L258](../../../CS5489/course-notes/Lecture05.tex#L258)；CS5489 p.105 | 修订并二读；E044；E045 | 激活表、不可微约定及输出损失匹配保留；删除重复读图句，中文参数计数题补偏置。 |
| 08 · 沿一条路径看梯度怎样变小<br>[源稿 L334](../../../CS5489/course-notes/Lecture05.tex#L334)；CS5489 p.106 | 保留（已审阅）；无须改写 | 单位权重与标量路径条件必要，梯度衰减不能只看层数，保留。 |
| 09 · 6. 把一层的梯度推给上一层<br>[源稿 L363](../../../CS5489/course-notes/Lecture05.tex#L363)；CS5489 p.107 | 保留（已审阅）；无须改写 | 逐分量到两次不同轴求和、矩阵转置与共享偏置完整保留；平均只计一次。 |
| 10 · 同一小网络，从输入一直算到两层梯度<br>[源稿 L479](../../../CS5489/course-notes/Lecture05.tex#L479)；CS5489 p.108 | 保留（已审阅）；无须改写 | 同一单位矩阵网络的全部前向/反向中间量与同步更新说明保留。 |
| 11 · 换一个输出权重，看看两条路径怎样相加<br>[源稿 L517](../../../CS5489/course-notes/Lecture05.tex#L517)；CS5489 p.109 | 保留（已审阅）；无须改写 | 换W区分两层梯度，完整独立变式及双语表格保持。 |
| 12 · 换成回归任务：tanh与平方误差怎样反传？<br>[源稿 L588](../../../CS5489/course-notes/Lecture05.tex#L588)；CS5489 p.110 | 保留（已审阅）；无须改写 | tanh回归与平方损失独立推导保留，不能照搬交叉熵梯度。 |
| 13 · 7. SGD、监控与早停｜从一次更新到选择训练时刻<br>[源稿 L627](../../../CS5489/course-notes/Lecture05.tex#L627)；CS5489 p.111 | 修订并二读；E173 | 批次/epoch、动量含学习率约定和零批梯度反例保留；自测补初始值。 |
| 14 · 训练曲线与早停<br>[源稿 L672](../../../CS5489/course-notes/Lecture05.tex#L672)；CS5489 p.111 | 保留（已审阅）；无须改写 | 原代码只退出、完整早停保存恢复的区别保留；曲线不唯一诊断。 |
| 15 · 8. Universal approximation｜能表示，不等于容易学会<br>[源稿 L711](../../../CS5489/course-notes/Lecture05.tex#L711)；CS5489 p.112 | 保留（已审阅）；无须改写 | 表示存在、优化找到与泛化三者边界清楚，保留紧致域解释。 |
| 16 · 9. MNIST｜看懂老师完整示范的每个接口<br>[源稿 L743](../../../CS5489/course-notes/Lecture05.tex#L743)；CS5489 p.112 | 保留（已审阅）；无须改写 | MNIST各架构参数数和教师保存准确率身份清楚，表格不改。 |
| 17 · 10. 回顾与英文自测<br>[源稿 L783](../../../CS5489/course-notes/Lecture05.tex#L783)；CS5489 p.113 | 保留（已审阅）；无须改写 | 五个短题中英条件和关键答案对应，已有完整理由保留。 |
| 18 · 学习要求与难点回查<br>[源稿 L833](../../../CS5489/course-notes/Lecture05.tex#L833)；CS5489 p.114 | 保留（已审阅）；无须改写 | 当前Assignment2任务及未提供Tutorial5范围保留。 |
| 19 · Historical exam map｜按考点查题源<br>[源稿 L859](../../../CS5489/course-notes/Lecture05.tex#L859)；CS5489 p.114 | 修订并二读；见相应源稿的修改与生成模板记录 | 生成模板去重口径与自指；CNN/QE未覆盖边界保留。 |
| 20 · 输出概率与交叉熵<br>[源稿 L878](../../../CS5489/course-notes/Lecture05.tex#L878)；CS5489 p.115 | 保留（已审阅）；无须改写 | 输出激活原图和log零边界条件保留，表格关系不改。 |
| 21 · 链式法则与反向传播<br>[源稿 L899](../../../CS5489/course-notes/Lecture05.tex#L899)；CS5489 p.115 | 保留（已审阅）；无须改写 | 反传真题与样题分开，保留印刷题/手写解答身份。 |
| 22 · 激活函数与梯度消失<br>[源稿 L920](../../../CS5489/course-notes/Lecture05.tex#L920)；CS5489 p.115 | 保留（已审阅）；无须改写 | 梯度消失原题列表及饱和区条件保留。 |
| 23 · MLP表达能力与深浅比较<br>[源稿 L943](../../../CS5489/course-notes/Lecture05.tex#L943)；CS5489 p.116 | 保留（已审阅）；无须改写 | 表达能力/深浅比较表与正文三种能力对应，保留。 |
| 24 · SGD、学习率与momentum<br>[源稿 L963](../../../CS5489/course-notes/Lecture05.tex#L963)；CS5489 p.116 | 保留（已审阅）；无须改写 | 优化器原题关系和单批零梯度限制保留。 |
| 25 · 正则化、曲线与早停<br>[源稿 L983](../../../CS5489/course-notes/Lecture05.tex#L983)；CS5489 p.116 | 保留（已审阅）；无须改写 | 训练诊断与具体CNN结构覆盖分开，生成时只去完全重复条件子句。 |
| 26 · 来源覆盖索引<br>[源稿 L1013](../../../CS5489/course-notes/Lecture05.tex#L1013)；CS5489 p.117 | 保留（已审阅）；无须改写 | 162原单元覆盖与保存输出身份保留，补充验证脚本位置不改。 |

## CS5489/course-notes/Tutorial01.tex

| 区段与当前定位 | 问题／处理 | 保留内容与理由 |
|---|---|---|
| 00 · 开篇与导航<br>[源稿 L1](../../../CS5489/course-notes/Tutorial01.tex#L1)；CS5489 p.118 | 保留（已审阅）；无须改写 | 章节与Notebook身份保留。 |
| 01 · 从变量变化，走到能验证的程序<br>[源稿 L11](../../../CS5489/course-notes/Tutorial01.tex#L11)；CS5489 p.118 | 修订并二读；E047 | 原五项任务顺序、输出身份与学习表保留；删重复表后说明。 |
| 02 · 0. Setup｜本地路径与输出位置<br>[源稿 L49](../../../CS5489/course-notes/Tutorial01.tex#L49)；CS5489 p.118 | 保留（已审阅）；无须改写 | 数据路径与输出目录指引直接服务运行，保留。 |
| 03 · 1. Notebook state｜屏幕顺序不等于执行顺序<br>[源稿 L69](../../../CS5489/course-notes/Tutorial01.tex#L69)；CS5489 p.119 | 保留（已审阅）；无须改写 | 变量状态轨迹、预期NameError及双语重启题保留。 |
| 04 · 2. Count factors｜先写人能逐行跟上的版本<br>[源稿 L104](../../../CS5489/course-notes/Tutorial01.tex#L104)；CS5489 p.120 | 修订并二读；E048；E049 | 12的循环跟做、两种图轴和99/25计数保留；因子答案明确排除1及自身。 |
| 05 · 3. Load and plot the supplied array｜先核对两根轴<br>[源稿 L164](../../../CS5489/course-notes/Tutorial01.tex#L164)；CS5489 p.123 | 保留（已审阅）；无须改写 | 数据形状120×2和取前三行的题答清楚；无单位标签不推测。 |
| 06 · 4. Gram–Schmidt｜拿走已有方向，剩下才是新信息<br>[源稿 L203](../../../CS5489/course-notes/Tutorial01.tex#L203)；CS5489 p.124 | 保留（已审阅）；无须改写 | 两列完整正交化、空间重建与依赖列反例齐全，保留。 |
| 07 · 5. Help and return｜最后练一次英文解释<br>[源稿 L266](../../../CS5489/course-notes/Tutorial01.tex#L266)；CS5489 p.128 | 保留（已审阅）；无须改写 | help与干净内核运行、为什么还需重建检查有明确用途，保留。 |
| 08 · 原文件覆盖索引<br>[源稿 L283](../../../CS5489/course-notes/Tutorial01.tex#L283)；CS5489 p.128 | 保留（已审阅）；无须改写 | 47单元任务覆盖及空单元身份保留；Notebook执行单元不改。 |

## CS5489/course-notes/Tutorial02.tex

| 区段与当前定位 | 问题／处理 | 保留内容与理由 |
|---|---|---|
| 00 · 开篇与导航<br>[源稿 L1](../../../CS5489/course-notes/Tutorial02.tex#L1)；CS5489 p.129 | 保留（已审阅）；无须改写 | 章节身份与Notebook入口保留。 |
| 01 · 按老师原任务，跑通新闻分类并解释结果<br>[源稿 L11](../../../CS5489/course-notes/Tutorial02.tex#L11)；CS5489 p.129 | 修订并二读；E050 | 按原任务给完整流程，保存结果/test探索边界集中说明；精简维护表述。 |
| 02 · 学习地图 / Goal<br>[源稿 L34](../../../CS5489/course-notes/Tutorial02.tex#L34)；CS5489 p.129 | 修订并二读；E051 | 原6项任务和独立评价补充有明确身份；删无信息翻译自述。 |
| 03 · 0. Setup｜只在这里改实验设置<br>[源稿 L65](../../../CS5489/course-notes/Tutorial02.tex#L65)；CS5489 p.130 | 保留（已审阅）；无须改写 | 数据说明、环境变量与参数位置完整，代码不改。 |
| 04 · 1. Load and inspect data｜先数清楚，再训练<br>[源稿 L87](../../../CS5489/course-notes/Tutorial02.tex#L87)；CS5489 p.131 | 保留（已审阅）；无须改写 | 2000/1000实际记录与原2034/1353差异保留；shape题两种语言完整。 |
| 05 · 2. Build document vectors｜把词表当成一把固定的尺子<br>[源稿 L132](../../../CS5489/course-notes/Tutorial02.tex#L132)；CS5489 p.132 | 保留（已审阅）；无须改写 | 固定词表、test仅transform、全零表示与不能重贴列名的解释必要。 |
| 06 · 3. Bernoulli Naive Bayes｜先问有没有，不问重复几次<br>[源稿 L171](../../../CS5489/course-notes/Tutorial02.tex#L171)；CS5489 p.134 | 保留（已审阅）；无须改写 | 每词出现率、alpha默认身份和1次/10次不变的题完整。 |
| 07 · 3.1 Bernoulli parameter comparison｜比较平滑与词表规模<br>[源稿 L219](../../../CS5489/course-notes/Tutorial02.tex#L219)；CS5489 p.136 | 保留（已审阅）；无须改写 | 两组单因素试验及默认重复行用于一致性核对，保留。 |
| 08 · 4. Multinomial Naive Bayes model｜让非负权重进入另一个模型<br>[源稿 L253](../../../CS5489/course-notes/Tutorial02.tex#L253)；CS5489 p.138 | 保留（已审阅）；无须改写 | 模型与表示同时变、TF-IDF非整数和参数归一含义保留。 |
| 09 · 5. Misclassified documents｜分错了什么？哪些解释只是猜想？<br>[源稿 L300](../../../CS5489/course-notes/Tutorial02.tex#L300)；CS5489 p.140 | 修订并二读；E052；E190 | 三个真实错分样本和观察/假设区分保留；改保存输出标题。 |
| 10 · 6. Effect of smoothing｜只改alpha，画一条能解释的曲线<br>[源稿 L351](../../../CS5489/course-notes/Tutorial02.tex#L351)；CS5489 p.143 | 保留（已审阅）；无须改写 | 曲线轴、参数范围与非单调可能性明确，不改保存结果。 |
| 11 · 7. Effect of vocabulary size｜更多词，真的提供更多有效证据吗？<br>[源稿 L391](../../../CS5489/course-notes/Tutorial02.tex#L391)；CS5489 p.144 | 保留（已审阅）；无须改写 | alpha固定不继承test最优、词表上限/实际列数区别保留。 |
| 12 · 8. Poisson Naive Bayes｜外框不变，换掉词计数的分布<br>[源稿 L428](../../../CS5489/course-notes/Tutorial02.tex#L428)；CS5489 p.146 | 保留（已审阅）；无须改写 | Poisson接口与原始计数任务条件完整。 |
| 13 · 8.1 参数估计与log分数<br>[源稿 L440](../../../CS5489/course-notes/Tutorial02.tex#L440)；CS5489 p.146 | 保留（已审阅）；无须改写 | 计数率定义、T=0边界及log阶乘/先验推导保留。 |
| 14 · 8.2 模板未定义的alpha：明确采用一个补充约定<br>[源稿 L469](../../../CS5489/course-notes/Tutorial02.tex#L469)；CS5489 p.147 | 修订并二读；E053 | 明确选用平滑率、Gamma后验均值及alpha=0分支；删重复身份自述。 |
| 15 · 8.3 先用四条小数据检查，再跑整份新闻<br>[源稿 L519](../../../CS5489/course-notes/Tutorial02.tex#L519)；CS5489 p.149 | 保留（已审阅）；无须改写 | 四条手算数据、10/20标签与库logpmf对照保留。 |
| 16 · 8.4 在原始新闻计数上运行 / Test the count model<br>[源稿 L541](../../../CS5489/course-notes/Tutorial02.tex#L541)；CS5489 p.150 | 保留（已审阅）；无须改写 | 用默认原始计数解释Poisson的等暴露假设，不从分数推断分布成立。 |
| 17 · 9. 如果要严格评价泛化，流程怎样改？ / A separate evaluation protocol<br>[源稿 L588](../../../CS5489/course-notes/Tutorial02.tex#L588)；CS5489 p.153 | 修订并二读；E178 | 训练内预处理/选择、未触碰test与3000条词表泄漏变式完整保留。 |
| 18 · 10. 回原课、练英文、再刷少量卡 / Return and recall<br>[源稿 L627](../../../CS5489/course-notes/Tutorial02.tex#L627)；CS5489 p.154 | 修订并二读；E054；E183 | 三问中英与分母关键答案对齐；标题集中于自测和入口。 |
| 19 · 原文件覆盖索引 / Source coverage<br>[源稿 L652](../../../CS5489/course-notes/Tutorial02.tex#L652)；CS5489 p.155 | 保留（已审阅）；无须改写 | 原36单元覆盖、库依据及Poisson补充身份保留。 |

## CS5489/course-notes/Tutorial03.tex

| 区段与当前定位 | 问题／处理 | 保留内容与理由 |
|---|---|---|
| 00 · 开篇与导航<br>[源稿 L1](../../../CS5489/course-notes/Tutorial03.tex#L1)；CS5489 p.156 | 保留（已审阅）；无须改写 | 章节和Notebook连接保持。 |
| 01 · 从同一份数据比较模型，别让实验条件悄悄换了<br>[源稿 L11](../../../CS5489/course-notes/Tutorial03.tex#L11)；CS5489 p.156 | 修订并二读；E055 | 保留给定标签身份、10图每错一张变10个百分点与完整任务表；标题改实际任务。 |
| 02 · 0. Parameters and provenance｜将实验约定写在最前面<br>[源稿 L50](../../../CS5489/course-notes/Tutorial03.tex#L50)；CS5489 p.156 | 保留（已审阅）；无须改写 | 原顺序、80/20划分与参考候选网格分清，保留。 |
| 03 · 1. Load and inspect｜一行不是一个像素，而是一张图<br>[源稿 L77](../../../CS5489/course-notes/Tutorial03.tex#L77)；CS5489 p.157 | 保留（已审阅）；无须改写 | 45×40到1800维、固定减0.5和同一索引必要，保留。 |
| 04 · 2. Logistic regression｜选C只看训练内部的验证表现<br>[源稿 L112](../../../CS5489/course-notes/Tutorial03.tex#L112)；CS5489 p.159 | 保留（已审阅）；无须改写 | 5折32/8与重拟合40张、并列候选顺序说明保留。 |
| 05 · 3. Weight image and errors｜权重回答的是“哪些像素推动分数”<br>[源稿 L137](../../../CS5489/course-notes/Tutorial03.tex#L137)；CS5489 p.160 | 保留（已审阅）；无须改写 | 权重随亮度的分数变化、平均图只展示与错分待验证解释保留。 |
| 06 · 4. Linear SVM｜换目标，保持数据不变<br>[源稿 L174](../../../CS5489/course-notes/Tutorial03.tex#L174)；CS5489 p.163 | 保留（已审阅）；无须改写 | 同一划分比较loss及色图尺度，保留。 |
| 07 · 5. Crop the same images｜先查尺寸，再解释性能<br>[源稿 L206](../../../CS5489/course-notes/Tutorial03.tex#L206)；CS5489 p.164 | 修订并二读；E056 | 22×18原掩码勘误、系数平方占比定义保留；英文变式补切片。 |
| 08 · 6. Custom kernel｜先用两个小向量检查，再接入SVM<br>[源稿 L249](../../../CS5489/course-notes/Tutorial03.tex#L249)；CS5489 p.167 | 保留（已审阅）；无须改写 | L1核的0.3679手算/矩阵形状、衰减条件及内层选择边界保留。 |
| 09 · 保存结果解读 / Interpreting the saved results<br>[源稿 L293](../../../CS5489/course-notes/Tutorial03.tex#L293)；CS5489 p.169 | 保留（已审阅）；无须改写 | 0.80/0.90、CV与小样本限制均来自保存输出；保留结果解读。 |
| 10 · 7. Independent explanation and source coverage｜合上代码，说清实验<br>[源稿 L317](../../../CS5489/course-notes/Tutorial03.tex#L317)；CS5489 p.170 | 修订并二读；E057；E058 | 四问补固定其他像素的英文条件；覆盖索引保留，删除重复结果身份句。 |

## CS5489/course-notes/Tutorial04.tex

| 区段与当前定位 | 问题／处理 | 保留内容与理由 |
|---|---|---|
| 00 · 开篇与导航<br>[源稿 L1](../../../CS5489/course-notes/Tutorial04.tex#L1)；CS5489 p.171 | 保留（已审阅）；无须改写 | 章节与Notebook入口保持。 |
| 01 · 去年的规律，今年还管用吗？<br>[源稿 L11](../../../CS5489/course-notes/Tutorial04.tex#L11)；CS5489 p.171 | 保留（已审阅）；无须改写 | 跨年需求任务、原2011/2012划分与五项学习要求保留。 |
| 02 · 1. Setup｜先固定实验条件<br>[源稿 L52](../../../CS5489/course-notes/Tutorial04.tex#L52)；CS5489 p.171 | 保留（已审阅）；无须改写 | 时间验证只用2011、五折和种子身份完整，不重跑实验。 |
| 03 · 2. Load and inspect｜不要把答案偷偷塞进输入<br>[源稿 L83](../../../CS5489/course-notes/Tutorial04.tex#L83)；CS5489 p.172 | 修订并二读；E059；E060 | 保留cnt组成、weekday勘误、yr恒定和编码解释；标题与泄漏说明改为直接表述。 |
| 04 · 3. A baseline and interpretable errors｜先问模型有没有赢过“每天报同一个数”<br>[源稿 L132](../../../CS5489/course-notes/Tutorial04.tex#L132)；CS5489 p.175 | 修订并二读；E061；E063；E064 | 基线、MSE/RMSE原课差异及散点轴/残差方向保留；英文改保存结果身份。 |
| 05 · 4. LASSO and OMP｜“重要特征”不是一份永久排行榜<br>[源稿 L186](../../../CS5489/course-notes/Tutorial04.tex#L186)；CS5489 p.177 | 修订并二读；E062 | 相关特征、编码单位和LASSO/OMP不同约束解释保留，标题去排行榜修辞。 |
| 06 · 5. Nonlinear regression｜让比较只改变模型<br>[源稿 L232](../../../CS5489/course-notes/Tutorial04.tex#L232)；CS5489 p.178 | 保留（已审阅）；无须改写 | 训练内选LASSO与事后测试RF最佳的区别必要，保留。 |
| 07 · 6. Test set bias｜先把新增数据的角色划清楚<br>[源稿 L278](../../../CS5489/course-notes/Tutorial04.tex#L278)；CS5489 p.180 | 修订并二读；E065；E175 | 91/275时间边界、四种方案和残差正负号保留；删地图比喻和整列数字重复，明确结果身份。 |
| 08 · 7. Return to the lecture｜把结果变成能解释的结论<br>[源稿 L332](../../../CS5489/course-notes/Tutorial04.tex#L332)；CS5489 p.183 | 保留（已审阅）；无须改写 | 四问及关键答案中英对应；77单元映射与复算设置保留。 |

## CS5489/course-notes/Assignment01.tex

| 区段与当前定位 | 问题／处理 | 保留内容与理由 |
|---|---|---|
| 00 · 开篇与导航<br>[源稿 L1](../../../CS5489/course-notes/Assignment01.tex#L1)；CS5489 p.184 | 保留（已审阅）；无须改写 | 章节身份保持。 |
| 01 · 从课堂概率模型到一个可解释、可复现的短信分类实验<br>[源稿 L8](../../../CS5489/course-notes/Assignment01.tex#L8)；CS5489 p.184 | 修订并二读；E067 | 方法指南范围与教学/实际文件身份清楚；标题改为实际流程。 |
| 02 · 本作业怎样接上 Lecture 2？<br>[源稿 L25](../../../CS5489/course-notes/Assignment01.tex#L25)；CS5489 p.184 | 保留（已审阅）；无须改写 | 连接Lecture2/Tutorial2、数据Id与评价五环节明确，保留学习表。 |
| 03 · 1. Goal｜先把预测目标说清楚<br>[源稿 L62](../../../CS5489/course-notes/Assignment01.tex#L62)；CS5489 p.185 | 保留（已审阅）；无须改写 | 三类标签及smishing独立类别条件明确，保留。 |
| 04 · 2. Load the Data｜三份数据文件分别承担什么工作？<br>[源稿 L100](../../../CS5489/course-notes/Assignment01.tex#L100)；CS5489 p.185 | 修订并二读；E068 | 三文件结构、元数据Prediction和Id对应是任务关键，保留；时间称谓改长期表达。 |
| 05 · 3. Evaluation｜为什么普通accuracy不够？<br>[源稿 L167](../../../CS5489/course-notes/Assignment01.tex#L167)；CS5489 p.186 | 保留（已审阅）；无须改写 | 先指出多数类问题再给balanced accuracy定义，保留三类都有样本条件。 |
| 06 · 完整手算 / Worked example<br>[源稿 L187](../../../CS5489/course-notes/Assignment01.tex#L187)；CS5489 p.186 | 保留（已审阅）；无须改写 | 人工混淆矩阵完整双语手算及always-normal反例保留。 |
| 07 · 独立变式 / Transfer<br>[源稿 L240](../../../CS5489/course-notes/Assignment01.tex#L240)；CS5489 p.187 | 保留（已审阅）；无须改写 | 独立召回变式、缺类别分母与adjusted约定保留。 |
| 08 · 4. Methodology｜先跑通一条可信的基线<br>[源稿 L267](../../../CS5489/course-notes/Assignment01.tex#L267)；CS5489 p.187 | 保留（已审阅）；无须改写 | NB基线与参数清单、代码接口只示意的范围明确，保留。 |
| 09 · 5. Validation｜每份数据什么时候能用？<br>[源稿 L323](../../../CS5489/course-notes/Assignment01.tex#L323)；CS5489 p.188 | 保留（已审阅）；无须改写 | train内部/val/test分工、预测范围不等于训练权限明确，保留。 |
| 10 · 6. 怎样增加一个有理由的实验？<br>[源稿 L381](../../../CS5489/course-notes/Assignment01.tex#L381)；CS5489 p.189 | 保留（已审阅）；无须改写 | 比较表按改变/保持/记录拆实验，具体而不泛泛，保留。 |
| 11 · 7. Error analysis｜把“错了”变成下一步能查的线索<br>[源稿 L421](../../../CS5489/course-notes/Assignment01.tex#L421)；CS5489 p.190 | 保留（已审阅）；无须改写 | 错误观察与假设、冻结后测试样本分析的原要求保留。 |
| 12 · 8. Final submission notebook｜换个干净内核，还能生成一样的预测吗？<br>[源稿 L445](../../../CS5489/course-notes/Assignment01.tex#L445)；CS5489 p.190 | 保留（已审阅）；无须改写 | Doc/Final分工、pandas导入勘误、Id对齐和重跑检查均有具体用途，保留。 |
| 13 · 9. 合上指南，检查自己能否解释<br>[源稿 L494](../../../CS5489/course-notes/Assignment01.tex#L494)；CS5489 p.191 | 修订并二读；E187 | 四问中英完整，51.67%教学数字身份是必要自测，保留。 |
| 14 · 10. 原任务覆盖与来源<br>[源稿 L543](../../../CS5489/course-notes/Assignment01.tex#L543)；CS5489 p.192 | 修订并二读；E069 | 23/11原单元索引与回链保留，删重复来源自证。 |

## CS5489/course-notes/Assignment02.tex

| 区段与当前定位 | 问题／处理 | 保留内容与理由 |
|---|---|---|
| 00 · 开篇与导航<br>[源稿 L1](../../../CS5489/course-notes/Assignment02.tex#L1)；CS5489 p.193 | 保留（已审阅）；无须改写 | 章节身份保持。 |
| 01 · 看懂每一块接口，再把梯度接起来<br>[源稿 L8](../../../CS5489/course-notes/Assignment02.tex#L8)；CS5489 p.193 | 保留（已审阅）；无须改写 | 反传与优化轨迹两条任务线清楚，原模板/Primer与自行实验边界保留。 |
| 02 · 1. 先沿前向过程把变量认全<br>[源稿 L52](../../../CS5489/course-notes/Assignment02.tex#L52)；CS5489 p.193 | 保留（已审阅）；无须改写 | 行样本形状、A/W与代码属性对应、返回梯度接口保留。 |
| 03 · 2. Loss与Output：先统一“平均”的位置<br>[源稿 L87](../../../CS5489/course-notes/Assignment02.tex#L87)；CS5489 p.194 | 保留（已审阅）；无须改写 | 入口除B约定与允许TODO位置、正则/偏置及更新时机保留。 |
| 04 · 3. Hidden：ReLU和Leaky ReLU不能套错<br>[源稿 L113](../../../CS5489/course-notes/Assignment02.tex#L113)；CS5489 p.194 | 保留（已审阅）；无须改写 | Leaky与ReLU分支、0处约定和正反向数字示范完整，保留。 |
| 05 · 4. 可学习指数：对数为什么突然出现？<br>[源稿 L136](../../../CS5489/course-notes/Assignment02.tex#L136)；CS5489 p.195 | 修订并二读；E070；E071 | 共享指数正区log、mask与硬编码步长说明必要；变式题答数值和符号中英对齐。 |
| 06 · 5. 先检查小数值，再训练葡萄酒数据<br>[源稿 L178](../../../CS5489/course-notes/Assignment02.tex#L178)；CS5489 p.195 | 保留（已审阅）；无须改写 | 有限差分公平比较、Wine标签/划分与原全量缩放缺陷保留。 |
| 07 · 6. 五种优化器：同一条梯度，不同的走法<br>[源稿 L207](../../../CS5489/course-notes/Assignment02.tex#L207)；CS5489 p.196 | 保留（已审阅）；无须改写 | 5种优化器状态、epsilon根号位置、moment偏差与一步动量完整，保留。 |
| 08 · 7. 原题的函数与图该怎样比较<br>[源稿 L269](../../../CS5489/course-notes/Assignment02.tex#L269)；CS5489 p.197 | 保留（已审阅）；无须改写 | 四函数、原初值冲突及不同epoch预算说明保留。 |
| 09 · 8. 原文核对与修正记录<br>[源稿 L300](../../../CS5489/course-notes/Assignment02.tex#L300)；CS5489 p.198 | 保留（已审阅）；无须改写 | 七项已确认公式/代码勘误原样保留，来源不改。 |
| 10 · 9. 完成前如何自查<br>[源稿 L329](../../../CS5489/course-notes/Assignment02.tex#L329)；CS5489 p.198 | 修订并二读；E180 | 自查中的四个原英文问题补为逐题中英短答案；原执行真实性检查保留。 |
| 11 · 来源覆盖索引<br>[源稿 L358](../../../CS5489/course-notes/Assignment02.tex#L358)；CS5489 p.199 | 保留（已审阅）；无须改写 | 76单元与Primer四页完整定位保留。 |

## CS5489/course-notes/ExamIndex.tex

| 区段与当前定位 | 问题／处理 | 保留内容与理由 |
|---|---|---|
| 00 · 开篇与导航<br>[源稿 L1](../../../CS5489/course-notes/ExamIndex.tex#L1)；CS5489 p.200 | 修订并二读；见相应源稿的修改与生成模板记录 | 按年/按知识点双入口及Lecture1–5映射范围清楚；删已由目录体现的放置顺序。 |
| 01 · 2020B期中Quiz<br>[源稿 L30](../../../CS5489/course-notes/ExamIndex.tex#L30)；CS5489 p.200 | 保留（已审阅）；无须改写 | 2020B Quiz封面与随卷答案身份保留，12行课程映射和凸有限解条件不改。 |
| 02 · 2021A期中<br>[源稿 L71](../../../CS5489/course-notes/ExamIndex.tex#L71)；CS5489 p.201 | 保留（已审阅）；无须改写 | 2021A题纸/答案双版本只算一卷，全部原题定位保留。 |
| 03 · 2021B*期中<br>[源稿 L116](../../../CS5489/course-notes/ExamIndex.tex#L116)；CS5489 p.201 | 保留（已审阅）；无须改写 | 2021B*封面冲突、原始文件名身份及GP关联边界保留。 |
| 04 · 2023A期中<br>[源稿 L163](../../../CS5489/course-notes/ExamIndex.tex#L163)；CS5489 p.202 | 保留（已审阅）；无须改写 | 2023A随卷答案与Mock同题对应保留；分数/概率、AdaBoost不同更新说明必要。 |
| 05 · 2023B期中<br>[源稿 L205](../../../CS5489/course-notes/ExamIndex.tex#L205)；CS5489 p.203 | 保留（已审阅）；无须改写 | 2023B原题映射与参数计数/C支持向量数勘误保留。 |
| 06 · 2025A期中<br>[源稿 L249](../../../CS5489/course-notes/ExamIndex.tex#L249)；CS5489 p.204 | 修订并二读；见相应源稿的修改与生成模板记录 | 2025A批注扫描身份保留；印刷题面和手写解答声明只保留已有一处。 |
| 07 · 2020B期末<br>[源稿 L290](../../../CS5489/course-notes/ExamIndex.tex#L290)；CS5489 p.204 | 保留（已审阅）；无须改写 | 2020B期末四页题号及GMM/KPCA关联范围保留。 |
| 08 · 2021A期末<br>[源稿 L330](../../../CS5489/course-notes/ExamIndex.tex#L330)；CS5489 p.205 | 保留（已审阅）；无须改写 | 2021A期末四页与Adam/训练噪声条件保留。 |
| 09 · 2021B期末<br>[源稿 L367](../../../CS5489/course-notes/ExamIndex.tex#L367)；CS5489 p.206 | 保留（已审阅）；无须改写 | 2021B期末五页及CNN未覆盖/输出激活边界保留。 |
| 10 · Question Samples（年份未载）<br>[源稿 L406](../../../CS5489/course-notes/ExamIndex.tex#L406)；CS5489 p.206 | 保留（已审阅）；无须改写 | 样题原Q1/Q2/Q7/Q4不重排，样题改选项需独立判断的身份保留。 |
| 11 · Mock Exam（复用2023A题面）<br>[源稿 L438](../../../CS5489/course-notes/ExamIndex.tex#L438)；CS5489 p.207 | 保留（已审阅）；无须改写 | Mock复用2023A且不增加真题卷数，表中原页码不同保持。 |
| 12 · CS5489 QE整理片段（年份未载）<br>[源稿 L480](../../../CS5489/course-notes/ExamIndex.tex#L480)；CS5489 p.207 | 修订并二读；见相应源稿的修改与生成模板记录 | QE表前缺年份/模型、表后片段不作卷数/CNN未覆盖已齐；核对注仅留跨页读取与非标准手写解答。 |

## CS5222/course-notes/Chapter01.tex

| 区段与当前定位 | 问题／处理 | 保留内容与理由 |
|---|---|---|
| 00 · 开篇与导航<br>[源稿 L1](../../../CS5222/course-notes/Chapter01.tex#L1)；CS5222 p.5 | 修订并二读；E077；E080 | 网页路径任务和原课身份/先修保留；开篇直接说请求经过多个网络。 |
| 01 · 1. What is the Internet?｜先分清“设备视角”和“服务视角”<br>[源稿 L24](../../../CS5222/course-notes/Chapter01.tex#L24)；CS5222 p.5 | 保留（已审阅）；无须改写 | 组成与服务两个视角、原图及RFC/IETF身份保留。 |
| 02 · 2. What is a protocol?｜格式、顺序、动作缺一不可<br>[源稿 L47](../../../CS5222/course-notes/Chapter01.tex#L47)；CS5222 p.6 | 保留（已审阅）；无须改写 | 问时间原例用于格式/顺序/动作，区别实际教学TCP流程，保留。 |
| 03 · 3. Network edge and access｜接入网把你带到第一个入口<br>[源稿 L71](../../../CS5222/course-notes/Chapter01.tex#L71)；CS5222 p.7 | 修订并二读；E081 | DSL不同频段、家庭盒子功能、介质表与历史速率身份保留。 |
| 04 · 4. Circuit versus packet switching｜预留座位，还是来了再排队<br>[源稿 L120](../../../CS5222/course-notes/Chapter01.tex#L120)；CS5222 p.9 | 修订并二读；E082；E083 | 电路预留/分组按需、FDM/TDM与流水线条件保留；去食堂重复类比。 |
| 05 · 共享带来的容量收益，有什么条件？<br>[源稿 L151](../../../CS5222/course-notes/Chapter01.tex#L151)；CS5222 p.11 | 保留（已审阅）；无须改写 | 35用户二项尾概率纠正0.0004243与独立假设保留。 |
| 06 · 5. Forwarding, routing and a network of networks｜路口动作与整条路线<br>[源稿 L171](../../../CS5222/course-notes/Chapter01.tex#L171)；CS5222 p.12 | 修订并二读；E084 | 0111查表事件、routing与forwarding区分及ISP互联保留；类比评价改具体分布式条件。 |
| 07 · 6. Delay and loss｜慢在哪一段，公式才选得对<br>[源稿 L207](../../../CS5222/course-notes/Chapter01.tex#L207)；CS5222 p.13 | 保留（已审阅）；无须改写 | 四类时延表、两次车队原例及rho条件完整保留。 |
| 08 · 从一次突发看见排队与丢包<br>[源稿 L254](../../../CS5222/course-notes/Chapter01.tex#L254)；CS5222 p.14 | 保留（已审阅）；无须改写 | 有限队列等待/服务位置、同时到达顺序、平均rho反例和双语变式保留。 |
| 09 · 7. Real delays and throughput｜测得的RTT不是某一条线的长度<br>[源稿 L327](../../../CS5222/course-notes/Chapter01.tex#L327)；CS5222 p.16 | 保留（已审阅）；无须改写 | RTT观察/推断、吞吐/容量与公平共享条件保留，独立题完整。 |
| 10 · 8. Layers and encapsulation｜把一件复杂的事拆成清楚的职责<br>[源稿 L364](../../../CS5222/course-notes/Chapter01.tex#L364)；CS5222 p.17 | 修订并二读；E085 | 航空原例、五层、无NAT逐设备封装表保留；删重复的分层泛泛总结。 |
| 11 · 9. Security and history｜知道威胁，也知道哪些数字属于当年<br>[源稿 L441](../../../CS5222/course-notes/Chapter01.tex#L441)；CS5222 p.19 | 保留（已审阅）；无须改写 | 安全术语与历史纠错保留来源/日期，不把旧数字改成当前情况。 |
| 12 · 10. Chapter 1 Q\&A｜直接对照老师的五道课堂题<br>[源稿 L464](../../../CS5222/course-notes/Chapter01.tex#L464)；CS5222 p.19 | 保留（已审阅）；无须改写 | 五道课堂题、原选项图与模型边界保留，答案身份明确。 |
| 13 · 11. 回顾、任务与来源索引<br>[源稿 L516](../../../CS5222/course-notes/Chapter01.tex#L516)；CS5222 p.22 | 保留（已审阅）；无须改写 | 请求链复述与任务入口有回顾功能，英文时延题保持。 |
| 14 · 学习要求与难点回查<br>[源稿 L529](../../../CS5222/course-notes/Chapter01.tex#L529)；CS5222 p.23 | 保留（已审阅）；无须改写 | 难度/优先级与实际任务依据分开，保留。 |
| 15 · 原材料覆盖<br>[源稿 L553](../../../CS5222/course-notes/Chapter01.tex#L553)；CS5222 p.5 | 保留（已审阅）；无须改写 | 完整/part页码关系及Q&A覆盖保留。 |

## CS5222/course-notes/Chapter02.tex

| 区段与当前定位 | 问题／处理 | 保留内容与理由 |
|---|---|---|
| 00 · 开篇与导航<br>[源稿 L1](../../../CS5222/course-notes/Chapter02.tex#L1)；CS5222 p.25 | 修订并二读；E078 | 应用请求任务、107页范围、缺FTP身份保留；精简导航。 |
| 01 · 1. Applications, processes and sockets｜先找到真正对话的双方<br>[源稿 L27](../../../CS5222/course-notes/Chapter02.tex#L27)；CS5222 p.25 | 保留（已审阅）；无须改写 | 进程/端点、socket接口与client/server角色解释完整，保留。 |
| 02 · 2. Service requirements｜“可靠”不等于“准时”<br>[源稿 L61](../../../CS5222/course-notes/Chapter02.tex#L61)；CS5222 p.26 | 保留（已审阅）；无须改写 | 时延/可靠/吞吐/安全是不同服务，旧SSL与TCP永久故障边界保留。 |
| 03 · 3. Web and HTTP｜拿到HTML不等于拿齐整页<br>[源稿 L84](../../../CS5222/course-notes/Chapter02.tex#L84)；CS5222 p.26 | 保留（已审阅）；无须改写 | HTML与对象、HTTP/1.x模型和HTTP/3边界保留。 |
| 04 · 连接可以复用，请求是否并行还要另问<br>[源稿 L96](../../../CS5222/course-notes/Chapter02.tex#L96)；CS5222 p.26 | 保留（已审阅）；无须改写 | 三种连接模型分别算6/4/3 RTT，双语独立题条件完整，保留。 |
| 05 · 读报文：把每一行与问题对应<br>[源稿 L120](../../../CS5222/course-notes/Chapter02.tex#L120)；CS5222 p.28 | 保留（已审阅）；无须改写 | 请求行/头/CRLF和版本布局边界保留，图用于字段定位。 |
| 06 · 4. Cookies and caches｜识别会话，与复用内容是两件事<br>[源稿 L141](../../../CS5222/course-notes/Chapter02.tex#L141)；CS5222 p.28 | 保留（已审阅）；无须改写 | cookie四环节与cache新鲜度不同，代理角色题保留。 |
| 07 · 5. Electronic mail and SMTP｜把“送到邮箱”和“打开邮箱”拆开<br>[源稿 L171](../../../CS5222/course-notes/Chapter02.tex#L171)；CS5222 p.29 | 保留（已审阅）；无须改写 | Alice到Bob投递链、SMTP事务/信封与消息头区别保留。 |
| 08 · 6. POP3, IMAP and webmail｜下载之后要不要留在服务器？<br>[源稿 L199](../../../CS5222/course-notes/Chapter02.tex#L199)；CS5222 p.30 | 保留（已审阅）；无须改写 | POP3提交删除/UIDL、IMAP与Webmail路径完整，保留。 |
| 09 · 7. DNS services and hierarchy｜通讯录不是只放在一台电脑上<br>[源稿 L217](../../../CS5222/course-notes/Chapter02.tex#L217)；CS5222 p.31 | 修订并二读；E086 | root/TLD/权威与zone说明具体；标题改命名与查询层次。 |
| 10 · 8. Recursive versus iterative DNS｜是“替我办完”，还是“告诉我下一站”<br>[源稿 L240](../../../CS5222/course-notes/Chapter02.tex#L240)；CS5222 p.31 | 保留（已审阅）；无须改写 | 递归/迭代原图、往返计数和TTL区别保留。 |
| 11 · 9. DNS records and messages｜名字、值、类型、有效时间要一起读<br>[源稿 L265](../../../CS5222/course-notes/Chapter02.tex#L265)；CS5222 p.32 | 保留（已审阅）；无须改写 | RR表、CNAME/A链与两个TTL变式、报文字段和原拼写疑点保留。 |
| 12 · 10. P2P file distribution｜新加入的人也可以带来上传能力<br>[源稿 L317](../../../CS5222/course-notes/Chapter02.tex#L317)；CS5222 p.33 | 修订并二读；E088 | 三项容量下界与原75页例完整；零上传变式补齐数据与所求。 |
| 13 · 11. BitTorrent｜先找邻居，再交换稀缺块<br>[源稿 L369](../../../CS5222/course-notes/Chapter02.tex#L369)；CS5222 p.34 | 修订并二读；E089 | 邻居集合计数与两种调度决定保留；变式写明初始持有集合。 |
| 14 · 12. Video, DASH and CDN｜边下边播，需要的不只是平均带宽<br>[源稿 L404](../../../CS5222/course-notes/Chapter02.tex#L404)；CS5222 p.35 | 保留（已审阅）；无须改写 | 编码率/吞吐、块大小与播放缓冲计算保留，不把CDN与DASH混同。 |
| 15 · 一次播放请求怎样找到视频块<br>[源稿 L428](../../../CS5222/course-notes/Chapter02.tex#L428)；CS5222 p.36 | 保留（已审阅）；无须改写 | DNS导向五步流程、DNS/内容服务器和两种导向实现条件完整。 |
| 16 · 保留服务器，只调码率，能否避免停顿？<br>[源稿 L464](../../../CS5222/course-notes/Chapter02.tex#L464)；CS5222 p.36 | 保留（已审阅）；无须改写 | 三档下载/停顿与匹配平均速率仍停顿的反例清楚，保留。 |
| 17 · 13. Socket programming｜把课堂的大写转换例子真正跑通<br>[源稿 L497](../../../CS5222/course-notes/Chapter02.tex#L497)；CS5222 p.37 | 修订并二读；E090 | UDP/TCP调用、UTF-8、换行分帧与运行命令保留；英文任务补消息。 |
| 18 · 14. Back to the course｜用一条请求链把本章连起来<br>[源稿 L548](../../../CS5222/course-notes/Chapter02.tex#L548)；CS5222 p.38 | 保留（已审阅）；无须改写 | 全章请求链及持久/流水线自测保留。 |
| 19 · 课堂 Q\&A：按原题判断并说明条件<br>[源稿 L565](../../../CS5222/course-notes/Chapter02.tex#L565)；CS5222 p.39 | 保留（已审阅）；无须改写 | Q&A原六题和答案为整理者解释的身份保留。 |
| 20 · 1. Transport service｜为应用选择传输服务<br>[源稿 L574](../../../CS5222/course-notes/Chapter02.tex#L574)；CS5222 p.39 | 保留（已审阅）；无须改写 | UDP适合场景按课堂时延模型回答，现代视频例外保留。 |
| 21 · 2. HTTP timing｜从HTML到两张图片<br>[源稿 L588](../../../CS5222/course-notes/Chapter02.tex#L588)；CS5222 p.39 | 保留（已审阅）；无须改写 | 非持久顺序与忽略开销条件保留，不假装原题说明并行。 |
| 22 · 3. Mail addressing｜目标主机与服务端口<br>[源稿 L602](../../../CS5222/course-notes/Chapter02.tex#L602)；CS5222 p.39 | 保留（已审阅）；无须改写 | SMTP投递端口25与提交/访问区别保留。 |
| 23 · 4. DNS records｜一个名字怎样对应多台服务器<br>[源稿 L616](../../../CS5222/course-notes/Chapter02.tex#L616)；CS5222 p.39 | 保留（已审阅）；无须改写 | 多A记录不保证精确均衡的边界保留。 |
| 24 · 5. BitTorrent｜找到谁、向谁下载<br>[源稿 L630](../../../CS5222/course-notes/Chapter02.tex#L630)；CS5222 p.40 | 保留（已审阅）；无须改写 | BitTorrent原四项、rarest-first与peer变化解释保留。 |
| 25 · 6. Socket services｜接口提供了什么<br>[源稿 L644](../../../CS5222/course-notes/Chapter02.tex#L644)；CS5222 p.40 | 保留（已审阅）；无须改写 | TCP服务/未连接UDP接口条件及并行变式完整保留。 |
| 26 · 学习要求与难点回查<br>[源稿 L677](../../../CS5222/course-notes/Chapter02.tex#L677)；CS5222 p.41 | 保留（已审阅）；无须改写 | 学习能力/难度表依当前任务，保留。 |
| 27 · 15. Source coverage and cautions｜每一页有去处<br>[源稿 L701](../../../CS5222/course-notes/Chapter02.tex#L701)；CS5222 p.41 | 修订并二读；E087 | 完整107页与part关系、旧版本边界保留；标题改检索用途。 |

## CS5222/course-notes/Chapter03.tex

| 区段与当前定位 | 问题／处理 | 保留内容与理由 |
|---|---|---|
| 00 · 开篇与导航<br>[源稿 L1](../../../CS5222/course-notes/Chapter03.tex#L1)；CS5222 p.43 | 保留（已审阅）；无须改写 | 章节身份保持。 |
| 01 · 数据到了电脑，还要交对进程、补齐缺口<br>[源稿 L8](../../../CS5222/course-notes/Chapter03.tex#L8)；CS5222 p.43 | 修订并二读；E079；E091 | 进程寻址到可靠传输、part1/2范围保留；删半段文件的修辞。 |
| 02 · 1. Transport service｜IP找到主机，传输层找到应用端点<br>[源稿 L32](../../../CS5222/course-notes/Chapter03.tex#L32)；CS5222 p.43 | 保留（已审阅）；E091 | 层间名称及TCP服务边界保留，题答说明到IP不等于到连接。 |
| 03 · 2. Multiplexing and demultiplexing｜同一栋楼有许多门<br>[源稿 L63](../../../CS5222/course-notes/Chapter03.tex#L63)；CS5222 p.43 | 修订并二读；E091；E092 | UDP普通接收/TCP四元组及回程端口示范保留；标题改端点标识。 |
| 04 · 3. UDP｜少做承诺，也少保存状态<br>[源稿 L100](../../../CS5222/course-notes/Chapter03.tex#L100)；CS5222 p.44 | 修订并二读；E091；E093 | UDP字段长度和不内建服务解释具体，标题与正文对应。 |
| 05 · 4. Internet checksum｜算得对不等于能发现一切错误<br>[源稿 L121](../../../CS5222/course-notes/Chapter03.tex#L121)；CS5222 p.44 | 保留（已审阅）；E091 | 16bit回卷、8bit简化例和漏检边界保留。 |
| 06 · 5. rdt1.0到rdt2.2｜每多一种故障，就多一项必要机制<br>[源稿 L155](../../../CS5222/course-notes/Chapter03.tex#L155)；CS5222 p.45 | 保留（已审阅）；E091 | 信息不对称引出数据/ACK故障，保留，不另加口号式总结。 |
| 07 · FSM的事件、条件与动作<br>[源稿 L164](../../../CS5222/course-notes/Chapter03.tex#L164)；CS5222 p.45 | 保留（已审阅）；E091 | FSM事件、状态、自环、Lambda规则完整可读，保留。 |
| 08 · rdt1.0：信道可靠，双方各一个状态<br>[源稿 L175](../../../CS5222/course-notes/Chapter03.tex#L175)；CS5222 p.45 | 保留（已审阅）；E091 | 可靠通道双单状态及无ACK/序号/timer原因明确，保留。 |
| 09 · rdt2.0：先解决数据损坏，再看反馈损坏<br>[源稿 L183](../../../CS5222/course-notes/Chapter03.tex#L183)；CS5222 p.45 | 保留（已审阅）；E091 | 发送端保存包、五行状态表与损坏反馈歧义保留。 |
| 10 · rdt2.1：序号记录的是这一轮数据身份<br>[源稿 L216](../../../CS5222/course-notes/Chapter03.tex#L216)；CS5222 p.46 | 修订并二读；E091 | 四/两状态、ACK损坏事件及原反馈不带序号条件保留。 |
| 11 · rdt2.2：让ACK带编号，便可去掉NAK<br>[源稿 L251](../../../CS5222/course-notes/Chapter03.tex#L251)；CS5222 p.47 | 修订并二读；E091；E193 | rdt2.2编号ACK规则、完整图与双语异常事件题完整，保留。 |
| 12 · 6. rdt3.0｜坏消息会来，丢掉的消息可能一直不来<br>[源稿 L297](../../../CS5222/course-notes/Chapter03.tex#L297)；CS5222 p.48 | 修订并二读；E091；E094 | rdt3.0坏ACK不立即重发、定时器和旧副本边界保留；标题改具体机制。 |
| 13 · 7. Stop-and-wait performance｜忙了8微秒，等了30毫秒<br>[源稿 L367](../../../CS5222/course-notes/Chapter03.tex#L367)；CS5222 p.49 | 修订并二读；E091；E095 | 停等利用率、3751窗口和理想条件保留；迁移题补包长/RTT。 |
| 14 · 8. GBN与Selective Repeat｜后面的包到了，要不要先收好？<br>[源稿 L410](../../../CS5222/course-notes/Chapter03.tex#L410)；CS5222 p.50 | 保留（已审阅）；E091 | GBN累计与SR逐包缓存定义互补，保留。 |
| 15 · 窗口怎样随ACK向前移动<br>[源稿 L422](../../../CS5222/course-notes/Chapter03.tex#L422)；CS5222 p.50 | 保留（已审阅）；E091 | N=4窗口前缀、同批丢1图、丢6独立题完整，保留。 |
| 16 · 9. TCP序号｜从“第几个包”切换到“下一个字节”<br>[源稿 L470](../../../CS5222/course-notes/Chapter03.tex#L470)；CS5222 p.52 | 保留（已审阅）；E091 | TCP第一字节序号与下一期待ACK、1000+500例保留。 |
| 17 · 沿课堂Telnet图算完三个报文段<br>[源稿 L485](../../../CS5222/course-notes/Chapter03.tex#L485)；CS5222 p.52 | 保留（已审阅）；E091 | 双向独立序列、Telnet三段与无SYN/FIN变式全部保持。 |
| 18 · 10. RTT与重传超时｜等多久才有理由怀疑包丢了？<br>[源稿 L556](../../../CS5222/course-notes/Chapter03.tex#L556)；CS5222 p.53 | 修订并二读；E091；E096 | RTO先新E后D约定及旧E差异保留；变式补系数，结果不改。 |
| 19 · 11. 回到老师的题目<br>[源稿 L608](../../../CS5222/course-notes/Chapter03.tex#L608)；CS5222 p.54 | 修订并二读；E091；E181 | 五个原英文自测逐题补中文与完整短答案，不新增题目。 |
| 20 · 学习要求与难点回查<br>[源稿 L638](../../../CS5222/course-notes/Chapter03.tex#L638)；CS5222 p.55 | 保留（已审阅）；无须改写 | 当前范围/难点与未下载后半章身份保留。 |
| 21 · 来源覆盖索引<br>[源稿 L663](../../../CS5222/course-notes/Chapter03.tex#L663)；CS5222 p.56 | 保留（已审阅）；E091 | 70页part覆盖及补充算例身份保持。 |

## CS5222/course-notes/Tutorial01.tex

| 区段与当前定位 | 问题／处理 | 保留内容与理由 |
|---|---|---|
| 00 · 开篇与导航<br>[源稿 L1](../../../CS5222/course-notes/Tutorial01.tex#L1)；CS5222 p.57 | 修订并二读；E098 | 保留四项任务/原题与教师身份、先修入口和学习表；删除重复依据句。 |
| 01 · Q1. Store-and-forward｜先等整包到，再转发<br>[源稿 L41](../../../CS5222/course-notes/Tutorial01.tex#L41)；CS5222 p.57 | 修订并二读；E099 | 逐跳与三包流水线表完整，保留全部图/选项；独立变式补齐模型条件。 |
| 02 · Q2. Circuit capacity｜数连接，也要数它消耗了几条边<br>[源稿 L106](../../../CS5222/course-notes/Tutorial01.tex#L106)；CS5222 p.59 | 修订并二读；E100 | 环路逐边上界与可达构造保留；变式补四节点拓扑。 |
| 03 · Q3. FDM and setup｜总速率不等于你的那一份<br>[源稿 L168](../../../CS5222/course-notes/Tutorial01.tex#L168)；CS5222 p.61 | 修订并二读；E101 | 12频带、建立/发送分工及单位易错保留；变式可独立求速率和总时间。 |
| 04 · Q4. Statistical multiplexing｜算人数前，先说是否独立<br>[源稿 L202](../../../CS5222/course-notes/Tutorial01.tex#L202)；CS5222 p.62 | 保留（已审阅）；无须改写 | 独立活动假设、120用户二项模型和严格超额定义保留。 |
| 05 · 回查与巩固<br>[源稿 L249](../../../CS5222/course-notes/Tutorial01.tex#L249)；CS5222 p.63 | 保留（已审阅）；无须改写 | 原题/教师页码覆盖与复算记录保持。 |

## CS5222/course-notes/Tutorial02.tex

| 区段与当前定位 | 问题／处理 | 保留内容与理由 |
|---|---|---|
| 00 · 开篇与导航<br>[源稿 L1](../../../CS5222/course-notes/Tutorial02.tex#L1)；CS5222 p.64 | 保留（已审阅）；无须改写 | 任务路线、原教师来源和单位约定保留。 |
| 01 · Q1. VoIP｜语音先攒成一包，还要算这段等待<br>[源稿 L22](../../../CS5222/course-notes/Tutorial02.tex#L22)；CS5222 p.64 | 修订并二读；E102 | 首位/可读取/同速播放三种事件条件完整保留；变式补所有速率与播放约定。 |
| 02 · Q2. Three store-and-forward links｜每一跳的发送与传播都要数<br>[源稿 L65](../../../CS5222/course-notes/Tutorial02.tex#L65)；CS5222 p.66 | 保留（已审阅）；无须改写 | 三段发送传播与两次处理表和64 ms保留。 |
| 03 · Q3. Immediate bit forwarding｜不用每个中间节点再等整包<br>[源稿 L110](../../../CS5222/course-notes/Tutorial02.tex#L110)；CS5222 p.67 | 修订并二读；E103 | 即时转发46 ms推理及不同速率边界保留；四链路题把忽略项写在题前。 |
| 04 · Q4. Queueing｜只算轮到你之前的等待<br>[源稿 L148](../../../CS5222/course-notes/Tutorial02.tex#L148)；CS5222 p.68 | 修订并二读；E104 | 已发部分与前方队列计算完整；75%变式补包长/速率/FIFO。 |
| 05 · Q5. Traceroute｜把真实测量和推断分开写<br>[源稿 L185](../../../CS5222/course-notes/Tutorial02.tex#L185)；CS5222 p.68 | 保留（已审阅）；无须改写 | 2026-09-23实测日期/参数/未到终点与星号解释保留，不改为新测量。 |
| 06 · 回查与巩固<br>[源稿 L221](../../../CS5222/course-notes/Tutorial02.tex#L221)；CS5222 p.69 | 保留（已审阅）；无须改写 | 3页原题与13页解答定位保留。 |

## CS5222/course-notes/Tutorial03.tex

| 区段与当前定位 | 问题／处理 | 保留内容与理由 |
|---|---|---|
| 00 · 开篇与导航<br>[源稿 L1](../../../CS5222/course-notes/Tutorial03.tex#L1)；CS5222 p.70 | 保留（已审阅）；无须改写 | 四题路线、教师解答/测量身份和优先级保留。 |
| 01 · Problem 1. Read an HTTP request｜不知道的就明确说不知道<br>[源稿 L22](../../../CS5222/course-notes/Tutorial03.tex#L22)；CS5222 p.70 | 修订并二读；E105 | 完整HTTP原字段与五问边界保留；标题直接说明字段取证。 |
| 02 · Problem 2. DNS resolution｜一对箭头才是一次往返<br>[源稿 L80](../../../CS5222/course-notes/Tutorial03.tex#L80)；CS5222 p.72 | 修订并二读；E107 | 8箭头合4往返与缓存位置保留；变式完整双语条件。 |
| 03 · Problem 3. A page with eight objects｜先取目录，再知道要取哪八件东西<br>[源稿 L118](../../../CS5222/course-notes/Tutorial03.tex#L118)；CS5222 p.74 | 修订并二读；E106；E108；E109 | 9对象串行/5并行/无流水线条件和原答案保留；6对象变式补全部必要参数。 |
| 04 · Problem 4. Nslookup and direct-IP browsing｜解析成功，不保证IP网址等于原站<br>[源稿 L167](../../../CS5222/course-notes/Tutorial03.tex#L167)；CS5222 p.76 | 保留（已审阅）；无须改写 | 日期明确的DNS查询及未执行直接IP访问边界保留。 |
| 05 · 来源与复习<br>[源稿 L185](../../../CS5222/course-notes/Tutorial03.tex#L185)；CS5222 p.76 | 保留（已审阅）；无须改写 | 原题/解答覆盖、标准查阅日期与复算入口保留。 |

## CS5222/course-notes/Tutorial04.tex

| 区段与当前定位 | 问题／处理 | 保留内容与理由 |
|---|---|---|
| 00 · 开篇与导航<br>[源稿 L1](../../../CS5222/course-notes/Tutorial04.tex#L1)；CS5222 p.77 | 保留（已审阅）；无须改写 | 章节身份保持。 |
| 01 · 先找谁供不动，再算怎样分得完<br>[源稿 L8](../../../CS5222/course-notes/Tutorial04.tex#L8)；CS5222 p.77 | 修订并二读；E110；E111 | 按下界/可达方案组织任务，来源和10进制单位保留；标题去供不动措辞。 |
| 02 · Problem 1. Construct a distribution scheme<br>[源稿 L49](../../../CS5222/course-notes/Tutorial04.tex#L49)；CS5222 p.77 | 修订并二读；E112 | 两种瓶颈给可行分配，不能仅写下界；中文变式补分配要求。 |
| 03 · Problem 2. 15 Gbit分给100人<br>[源稿 L89](../../../CS5222/course-notes/Tutorial04.tex#L89)；CS5222 p.78 | 修订并二读；E113 | CS/P2P三个容量约束及原符号勘误保留，10人变式补所有速率。 |
| 04 · Problem 3. 不上传的人，是否仍可能下载完成？<br>[源稿 L132](../../../CS5222/course-notes/Tutorial04.tex#L132)；CS5222 p.79 | 保留（已审阅）；无须改写 | optimistic unchoking、停留时间和多主机可能性条件保留。 |
| 05 · Problem 4. DASH到底存N份，还是N\textsuperscript{2}份？<br>[源稿 L166](../../../CS5222/course-notes/Tutorial04.tex#L166)；CS5222 p.80 | 修订并二读；E114 | N/N²/2N取决于配对，原题括号与v2解答保留；英文变式明确问文件数。 |
| 06 · 复习与来源索引<br>[源稿 L194](../../../CS5222/course-notes/Tutorial04.tex#L194)；CS5222 p.80 | 保留（已审阅）；无须改写 | 题面/解答页范围与教学图身份保留。 |

## CS5222/course-notes/Tutorial05.tex

| 区段与当前定位 | 问题／处理 | 保留内容与理由 |
|---|---|---|
| 00 · 开篇与导航<br>[源稿 L1](../../../CS5222/course-notes/Tutorial05.tex#L1)；CS5222 p.81 | 保留（已审阅）；无须改写 | 章节身份保持。 |
| 01 · 写清端点，算清位，再用反例检查协议假设<br>[源稿 L8](../../../CS5222/course-notes/Tutorial05.tex#L8)；CS5222 p.81 | 保留（已审阅）；无须改写 | 四题端点/校验/重排路线与未下载教师解答身份保留。 |
| 02 · Q1. How is a socket identified?<br>[源稿 L30](../../../CS5222/course-notes/Tutorial05.tex#L30)；CS5222 p.81 | 保留（已审阅）；无须改写 | UDP普通模型/TCP建立连接与实现差异保留。 |
| 03 · Q2. Server replies｜回程要把两端一起交换<br>[源稿 L53](../../../CS5222/course-notes/Tutorial05.tex#L53)；CS5222 p.82 | 修订并二读；E115；E116 | 完整回程表和IP/端口层次保留；英文原题和变式补端点。 |
| 04 · Q3. One's-complement checksum｜八位是题目的简化<br>[源稿 L105](../../../CS5222/course-notes/Tutorial05.tex#L105)；CS5222 p.83 | 保留（已审阅）；无须改写 | 三个8bit字的逐位加法、卷回变式与2bit相消反例保留。 |
| 05 · Q4. Alternating bit｜编号又回到0，旧包也可能叫0<br>[源稿 L151](../../../CS5222/course-notes/Tutorial05.tex#L151)；CS5222 p.84 | 修订并二读；E117；E118 | 四步旧包反例与英文答案保留；英文题干补协议和作图要求，序号变式明确2到4。 |
| 06 · 来源与复习<br>[源稿 L199](../../../CS5222/course-notes/Tutorial05.tex#L199)；CS5222 p.85 | 保留（已审阅）；无须改写 | 2页原题与Chapter3位置保留。 |

## CS5222/course-notes/Assignment01.tex

| 区段与当前定位 | 问题／处理 | 保留内容与理由 |
|---|---|---|
| 00 · 开篇与导航<br>[源稿 L1](../../../CS5222/course-notes/Assignment01.tex#L1)；CS5222 p.86 | 保留（已审阅）；无须改写 | 四任务范围、未提供教师解答与先修/难点保留。 |
| 01 · P6. Transmission and propagation｜最后一位刚出发，第一位可能已经到达<br>[源稿 L21](../../../CS5222/course-notes/Assignment01.tex#L21)；CS5222 p.86 | 修订并二读；E121 | P6七问时刻、单位与双语表及示意参数不同完整；变式补R/s。 |
| 02 · P31. Message segmentation｜像流水线一样，让不同链路同时工作<br>[源稿 L85](../../../CS5222/course-notes/Assignment01.tex#L85)；CS5222 p.88 | 修订并二读；E119；E122 | 三链路12s/4.01s与800包时间图保留；标题直接写流水线，变式补链路/开销。 |
| 03 · P17. POP3｜完成整次事务，不只补两行<br>[源稿 L135](../../../CS5222/course-notes/Assignment01.tex#L135)；CS5222 p.91 | 修订并二读；E120；E123 | POP3初始状态、两邮件、占位字节与CRLF条件保留；英文补已认证和RETR1。 |
| 04 · a. Download and delete / 下载并删除<br>[源稿 L151](../../../CS5222/course-notes/Assignment01.tex#L151)；CS5222 p.92 | 保留（已审阅）；无须改写 | 完整LIST/RETR/DELE/QUIT与成功提交条件保留，原代码块不改。 |
| 05 · b. Download and keep / 下载并保留<br>[源稿 L183](../../../CS5222/course-notes/Assignment01.tex#L183)；CS5222 p.92 | 保留（已审阅）；无须改写 | 保留两封下载和无DELE的keep事务，说明无KEEP命令有实际防错作用。 |
| 06 · c. Second keep-mode session / 五分钟后的第二次会话<br>[源稿 L211](../../../CS5222/course-notes/Assignment01.tex#L211)；CS5222 p.93 | 修订并二读；E124 | 第二会话与UIDL条件、编号不保证固定保留；变式补两邮件大小。 |
| 07 · Zoom. Apply protocol ideas with sources｜先说研究的是哪一种Zoom连接<br>[源稿 L266](../../../CS5222/course-notes/Assignment01.tex#L266)；CS5222 p.93 | 保留（已审阅）；无须改写 | Zoom明确2026-09-23原生云会议讨论范围和未实测边界，保留。 |
| 08 · a. 应用协议：产品生态的三项，与原生媒体路径分开<br>[源稿 L286](../../../CS5222/course-notes/Assignment01.tex#L286)；CS5222 p.94 | 保留（已审阅）；无须改写 | HTTPS/SIP/H.323各自部署情境与官方来源保留，不把房间互通当原生媒体。 |
| 09 · b. 架构 / Architecture<br>[源稿 L314](../../../CS5222/course-notes/Assignment01.tex#L314)；CS5222 p.94 | 保留（已审阅）；无须改写 | 云client-server与P2P/Mesh例外分别说明，保留。 |
| 10 · c. 传输 / Transport<br>[源稿 L328](../../../CS5222/course-notes/Assignment01.tex#L328)；CS5222 p.95 | 保留（已审阅）；无须改写 | UDP媒体/TCP回退与及时性理由保留，未声明重新核对当前版本。 |
| 11 · d. 老师电脑的IP / Lecturer's host IP<br>[源稿 L339](../../../CS5222/course-notes/Assignment01.tex#L339)；CS5222 p.95 | 保留（已审阅）；无须改写 | meeting ID不等于老师IP的具体寻址解释保留。 |
| 12 · 怎样整理成自己的作答<br>[源稿 L350](../../../CS5222/course-notes/Assignment01.tex#L350)；CS5222 p.95 | 保留（已审阅）；无须改写 | 证据类型区分帮助完成原调查题，保留。 |
| 13 · 来源与完成前自查<br>[源稿 L358](../../../CS5222/course-notes/Assignment01.tex#L358)；CS5222 p.95 | 保留（已审阅）；无须改写 | 原题四页、POP3完整性与复算/自查保持。 |

## CS5222/course-notes/ResearchReportGuide.tex

| 区段与当前定位 | 问题／处理 | 保留内容与理由 |
|---|---|---|
| 00 · 开篇与导航<br>[源稿 L1](../../../CS5222/course-notes/ResearchReportGuide.tex#L1)；CS5222 p.96 | 保留（已审阅）；无须改写 | 原任务范围Chapter1–7/排除安全、Rubric与课程入口保留。 |
| 01 · 1. 选题从一件事开始，不从一串热门缩写开始<br>[源稿 L36](../../../CS5222/course-notes/ResearchReportGuide.tex#L36)；CS5222 p.96 | 修订并二读；E125 | 实际经历到机制范围、课内DASH需新问题边界与英文framing保留；标题更直接。 |
| 02 · 2. 把问题、机制、效果连成一条可核查的解释<br>[源稿 L50](../../../CS5222/course-notes/ResearchReportGuide.tex#L50)；CS5222 p.97 | 修订并二读；E128；E129；E130；E131 | 问题到机制因果链和4秒缓冲例保留；变式补完整模型，合并限制说明。 |
| 03 · 3. 找来源时，为每一句重要话准备证据<br>[源稿 L82](../../../CS5222/course-notes/ResearchReportGuide.tex#L82)；CS5222 p.97 | 保留（已审阅）；无须改写 | 证据表、工作草稿表和AI/引用核查要求是原任务内容，保留。 |
| 04 · 4. 图要解释困难，不是给文字化妆<br>[源稿 L115](../../../CS5222/course-notes/ResearchReportGuide.tex#L115)；CS5222 p.98 | 修订并二读；E126 | 三类图各匹配实际问题，原创/改编/AI图身份要求保留；标题去化妆比喻。 |
| 05 · 5. 英文报告怎样组织才连贯<br>[源稿 L138](../../../CS5222/course-notes/ResearchReportGuide.tex#L138)；CS5222 p.98 | 修订并二读；E132 | 英文论证五部分、带条件示例和开放自查保留；不用虚构主题答案。 |
| 06 · 6. Reflection log｜写你真的经历过的理解变化<br>[源稿 L168](../../../CS5222/course-notes/ResearchReportGuide.tex#L168)；CS5222 p.98 | 修订并二读；E127 | 五个原反思问题与真实记录方式保持，标题简化。 |
| 07 · 7. 交付前的自查与来源覆盖<br>[源稿 L198](../../../CS5222/course-notes/ResearchReportGuide.tex#L198)；CS5222 p.99 | 保留（已审阅）；E133 | 原三页任务及Rubric覆盖保留，删重复泛泛收尾。 |

## learning/foundation-notes/MathForML.tex

| 区段与当前定位 | 问题／处理 | 保留内容与理由 |
|---|---|---|
| 00 · 开篇与导航<br>[源稿 L1](../../../learning/foundation-notes/MathForML.tex#L1)；Foundations p.3 | 修订并二读；E134；E135；E136；E137；E147；E159 | 先修范围、水箱/邮件/矩阵为教学补充身份保留；合并重复选读说明，去编辑日期。 |
| 01 · 先找到自己缺的那一级台阶<br>[源稿 L21](../../../learning/foundation-notes/MathForML.tex#L21)；Foundations p.3 | 修订并二读；E138；E144；E147；E159 | 10专题导航及5道带答案诊断题完整；中文抽样明确等可能。 |
| 02 · 1. Symbols, functions and graphs｜先让公式开口说人话<br>[源稿 L157](../../../learning/foundation-notes/MathForML.tex#L157)；Foundations p.5 | 修订并二读；E139 | 一级标题定位符号/函数/坐标，避免公式开口的包装。 |
| 03 · 1.1 水箱的账本：谁变了，谁跟着变？<br>[源稿 L163](../../../learning/foundation-notes/MathForML.tex#L163)；Foundations p.5 | 修订并二读；E140；E147；E159 | 水量表到V(t)、单位/定义域解释完整，保留实例。 |
| 04 · 1.2 图像就是把账本放到坐标上<br>[源稿 L206](../../../learning/foundation-notes/MathForML.tex#L206)；Foundations p.6 | 修订并二读；E141；E145；E146；E147；E159 | 图像与斜率配合清楚；完整水箱题中英补初始量/流速。 |
| 05 · 1.3 下标是编号，\ensuremath{\Sigma}和Π是压缩过的算术<br>[源稿 L244](../../../learning/foundation-notes/MathForML.tex#L244)；Foundations p.7 | 保留（已审阅）；E147；E159 | 下标、求和/连乘、括号及argmax表各有作用，保留。 |
| 06 · 2. Probability and density｜先说清楚在谁里面数<br>[源稿 L324](../../../learning/foundation-notes/MathForML.tex#L324)；Foundations p.8 | 保留（已审阅）；无须改写 | 概率/密度一级主题保持。 |
| 07 · 2.1 事件是条件，概率是满足它的机会<br>[源稿 L330](../../../learning/foundation-notes/MathForML.tex#L330)；Foundations p.8 | 保留（已审阅）；E147；E159 | 等可能抽样、补事件与重叠计数解释完整。 |
| 08 · 2.2 竖线后面的条件，会换掉分母<br>[源稿 L344](../../../learning/foundation-notes/MathForML.tex#L344)；Foundations p.8 | 修订并二读；E147；E148；E159 | 邮件表两种条件方向保留；删猫胡子比喻，修正人/邮件指代。 |
| 09 · 2.3 相乘也需要条件<br>[源稿 L411](../../../learning/foundation-notes/MathForML.tex#L411)；Foundations p.9 | 保留（已审阅）；E147；E159 | 独立与互斥、给定类独立的区别是必要条件，保留。 |
| 10 · 2.4 连续读数：高度是密度，面积才是概率<br>[源稿 L435](../../../learning/foundation-notes/MathForML.tex#L435)；Foundations p.9 | 修订并二读；E147；E149；E150；E151；E152；E159；E182 | 均匀密度单位、积分面积和单点限制保留；题干补区间，计数表加页码。 |
| 11 · 3. Powers and logarithms｜正着问乘多少，反着问几次方<br>[源稿 L509](../../../learning/foundation-notes/MathForML.tex#L509)；Foundations p.12 | 保留（已审阅）；无须改写 | 指数/对数一级主题保持，先正向再逆向符合先修。 |
| 12 · 3.1 从整数次幂到“反向提问”<br>[源稿 L515](../../../learning/foundation-notes/MathForML.tex#L515)；Foundations p.12 | 保留（已审阅）；E147；E159 | 整数到实数指数、对数定义域与底数限制保留。 |
| 13 · 3.2 e和ln：认识名字，再认识图像<br>[源稿 L536](../../../learning/foundation-notes/MathForML.tex#L536)；Foundations p.12 | 保留（已审阅）；E147；E159 | e/ln图像与负对数解释完整，保留。 |
| 14 · 3.3 为什么乘法会变成加法？<br>[源稿 L562](../../../learning/foundation-notes/MathForML.tex#L562)；Foundations p.13 | 保留（已审阅）；E147；E159 | 由指数乘法得到log乘法，反例ln(2+4)保留。 |
| 15 · 3.4 为什么最大值的位置没有变？<br>[源稿 L587](../../../learning/foundation-notes/MathForML.tex#L587)；Foundations p.14 | 保留（已审阅）；E147；E159 | argmax/max、独立证据算例与下溢/真实零概率区分保留。 |
| 16 · 4. Derivatives and maxima｜输入动一点，输出怎样动？<br>[源稿 L641](../../../learning/foundation-notes/MathForML.tex#L641)；Foundations p.15 | 保留（已审阅）；无须改写 | 导数一级主题与水量斜率衔接保持。 |
| 17 · 4.1 曲线上的斜率，不只一个<br>[源稿 L647](../../../learning/foundation-notes/MathForML.tex#L647)；Foundations p.15 | 保留（已审阅）；E147；E159 | 割线差商、h两侧趋近、有限步误差及图保持。 |
| 18 · 4.2 本讲需要的规则，从变化率理解<br>[源稿 L702](../../../learning/foundation-notes/MathForML.tex#L702)；Foundations p.16 | 保留（已审阅）；E147；E159 | 规则表、1/x差商、ln有向面积解释有实质作用，不压缩。 |
| 19 · 4.3 链式法则：变化经过了几道工序？<br>[源稿 L754](../../../learning/foundation-notes/MathForML.tex#L754)；Foundations p.17 | 保留（已审阅）；E147；E159 | 两段变化率、ln(1-p)负号与e导数验证完整保留。 |
| 20 · 4.4 偏导：这次只动一个旋钮<br>[源稿 L793](../../../learning/foundation-notes/MathForML.tex#L793)；Foundations p.18 | 修订并二读；E142；E147；E159 | 固定另一变量与高斯方差/标准差求导区别保留；标题改具体动作。 |
| 21 · 4.5 找山顶：导数为零只是候选条件<br>[源稿 L818](../../../learning/foundation-notes/MathForML.tex#L818)；Foundations p.18 | 修订并二读；E143；E147；E159 | 驻点反例、端点和4/6序列MLE最大值检查保留；标题去找山顶前缀。 |
| 22 · 5. Vectors, matrices and covariance｜先数格子，再看一起怎样变化<br>[源稿 L899](../../../learning/foundation-notes/MathForML.tex#L899)；Foundations p.21 | 保留（已审阅）；无须改写 | 矩阵一级主题与四条记录衔接保持。 |
| 23 · 5.1 一条记录是向量，很多条记录排成矩阵<br>[源稿 L905](../../../learning/foundation-notes/MathForML.tex#L905)；Foundations p.21 | 保留（已审阅）；E147；E159 | 行样本/列向量、转置与索引图清楚，保留。 |
| 24 · 5.2 乘法的每一格，都有明确算法<br>[源稿 L932](../../../learning/foundation-notes/MathForML.tex#L932)；Foundations p.21 | 修订并二读；E147；E153；E154；E159 | 两个正确公式保留，修正uᵀv到uuᵀ被称为交换顺序的误导。 |
| 25 · 5.3 平均数告诉你中心，方差告诉你散开多少<br>[源稿 L983](../../../learning/foundation-notes/MathForML.tex#L983)；Foundations p.22 | 保留（已审阅）；E147；E159 | 2/4/6 cm方差单位及N/N-1差异、平移/缩放检查保留。 |
| 26 · 5.4 两个特征一起动，怎样记账？<br>[源稿 L1014](../../../learning/foundation-notes/MathForML.tex#L1014)；Foundations p.23 | 保留（已审阅）；E147；E159 | 四条记录偏差乘积、外积和相关系数/独立反例完整，保留。 |
| 27 · 5.5 从共同变化到椭圆<br>[源稿 L1080](../../../learning/foundation-notes/MathForML.tex#L1080)；Foundations p.25 | 修订并二读；E147；E155；E159 | 原协方差图的条件与类别内估计保留，去已核查制作自述。 |
| 28 · 5.6 逆矩阵与行列式：能否倒回去，面积怎样变？<br>[源稿 L1097](../../../learning/foundation-notes/MathForML.tex#L1097)；Foundations p.25 | 保留（已审阅）；E147；E159 | 逆的恢复例、奇异矩阵与行列式面积图完整保留。 |
| 29 · 5.7 回到高斯公式：先看形状，再算一项<br>[源稿 L1137](../../../learning/foundation-notes/MathForML.tex#L1137)；Foundations p.27 | 保留（已审阅）；E147；E159 | 正定协方差、4/3距离和平方根行列式、三道独立变式保留。 |
| 30 · 6. Combinations and binomial probability｜先列小名单，再写大公式<br>[源稿 L1204](../../../learning/foundation-notes/MathForML.tex#L1204)；Foundations p.28 | 保留（已审阅）；E147；E159 | 3用户列举到二项公式、独立同p及严格超额条件保留。 |
| 31 · 7. Length, orthogonality and projection｜沿一个方向走，剩下多少走不到<br>[源稿 L1264](../../../learning/foundation-notes/MathForML.tex#L1264)；Foundations p.29 | 修订并二读；E147；E156；E159 | 投影由正交条件推出、数字检查和span保留，删除未引入手电筒类比的提醒。 |
| 32 · 8. Rank and pseudoinverse｜两条重复信息，不会变成两条独立线索<br>[源稿 L1325](../../../learning/foundation-notes/MathForML.tex#L1325)；Foundations p.31 | 修订并二读；E147；E157；E158；E159 | 重复列、无解到最小二乘、最小范数证明保留；明确A⁺是矩阵，变式补A。 |
| 33 · 9. Gradients and constraints｜下山之前，先看哪里允许走<br>[源稿 L1390](../../../learning/foundation-notes/MathForML.tex#L1390)；Foundations p.32 | 保留（已审阅）；E147；E159 | 梯度欧氏方向、步长过大反例、边界/KKT单向条件保留。 |
| 34 · 10. Batch gradients｜两行数据，为什么只更新一个偏置？<br>[源稿 L1460](../../../learning/foundation-notes/MathForML.tex#L1460)；Foundations p.33 | 修订并二读；E147；E159 | 共享b的两个贡献示意保留，删偷偷另建参数的重复说法。 |
| 35 · 10.1 从一行扩到两行<br>[源稿 L1478](../../../learning/foundation-notes/MathForML.tex#L1478)；Foundations p.34 | 保留（已审阅）；E147；E159 | 逐格计算XᵀG及偏置求和、形状检查完整，保留。 |
| 36 · 10.2 Jacobian是“一张影响关系表”<br>[源稿 L1506](../../../learning/foundation-notes/MathForML.tex#L1506)；Foundations p.34 | 保留（已审阅）；E147；E159 | Jacobian每格含义和两条路径数值完整，保留。 |
| 37 · 10.3 平均因子在哪里？<br>[源稿 L1523](../../../learning/foundation-notes/MathForML.tex#L1523)；Foundations p.35 | 保留（已审阅）；E147；E159 | 平均只计一次与正则标量目标说明有实际接口作用，保留。 |
| 38 · 10.4 指数也能是需要学习的数<br>[源稿 L1534](../../../learning/foundation-notes/MathForML.tex#L1534)；Foundations p.35 | 保留（已审阅）；E147；E159 | 可学习指数正域、数值与共享偏置变式完整保留。 |
| 39 · 这些补课从哪里来，学到哪里为止？<br>[源稿 L1567](../../../learning/foundation-notes/MathForML.tex#L1567)；Foundations p.35 | 修订并二读；E147；E159；E160 | 保留课程对应/脚本来源；补第10批量梯度已讲专题的遗漏索引行。 |

## learning/foundation-notes/NetworkBasics.tex

| 区段与当前定位 | 问题／处理 | 保留内容与理由 |
|---|---|---|
| 00 · 开篇与导航<br>[源稿 L1](../../../learning/foundation-notes/NetworkBasics.tex#L1)；Foundations p.37 | 修订并二读；E161 | 四个基础卡点与返回入口保留，开篇直接列对象。 |
| 01 · 1. Bit, byte and rate｜仓库有多少货，和每秒搬多少货，是两件事<br>[源稿 L38](../../../learning/foundation-notes/NetworkBasics.tex#L38)；Foundations p.37 | 修订并二读；E162；E164；E165；E174 | bit/B、十进制、发送/传播算例保留；图注定位，删除柱含义重复，带宽单位区别留正文。 |
| 02 · 2. Binary and octets｜位的位置，也在贡献数值<br>[源稿 L90](../../../learning/foundation-notes/NetworkBasics.tex#L90)；Foundations p.38 | 修订并二读；E166 | 位权表、IPv4/端口/hex解释保持，英文变式补两组数字。 |
| 03 · 3. Messages and bytes｜一段报文不是一整块没有边界的文字<br>[源稿 L145](../../../learning/foundation-notes/NetworkBasics.tex#L145)；Foundations p.39 | 修订并二读；E167 | HTTP字节、CRLF、UTF-8与消息分帧解释完整，标题改概念。 |
| 04 · 4. Timelines and pipelines｜先问“谁到哪了”，再问“用了多久”<br>[源稿 L194](../../../learning/foundation-notes/NetworkBasics.tex#L194)；Foundations p.40 | 修订并二读；E168 | 首位/末位图和3包2链路表保留，4包变式补转发条件。 |
| 05 · 来源与复算<br>[源稿 L252](../../../learning/foundation-notes/NetworkBasics.tex#L252)；Foundations p.41 | 保留（已审阅）；无须改写 | 原课程依据与脚本/计算结果、组合补课入口保持。 |

## learning/foundation-notes/SourceEvidence.tex

| 区段与当前定位 | 问题／处理 | 保留内容与理由 |
|---|---|---|
| 00 · 开篇与导航<br>[源稿 L1](../../../learning/foundation-notes/SourceEvidence.tex#L1)；Foundations p.42 | 保留（已审阅）；无须改写 | 当前材料核对日期、历史映射日期及难度/优先级区别保留。 |
| 01 · 当前范围由哪些原件决定<br>[源稿 L16](../../../learning/foundation-notes/SourceEvidence.tex#L16)；Foundations p.42 | 修订并二读；E169 | 课程范围/缺失材料与重复副本不增覆盖保留；版本信息改可读来源清单入口。 |
| 02 · 历史资料能帮到哪里<br>[源稿 L30](../../../learning/foundation-notes/SourceEvidence.tex#L30)；Foundations p.42 | 修订并二读；E170 | 样题校区、历史作业、复习笔记、6/3卷、2021B*和QE身份保持；去制作过程自述。 |
| 03 · 每项判断怎样写进讲义<br>[源稿 L64](../../../learning/foundation-notes/SourceEvidence.tex#L64)；Foundations p.43 | 修订并二读；E171 | 四类证据如何写进讲义与当前优先级保留，删本轮称谓。 |
| 04 · 怎样使用来源记录<br>[源稿 L89](../../../learning/foundation-notes/SourceEvidence.tex#L89)；Foundations p.43 | 保留（已审阅）；无须改写 | Notebook保存输出/补充图身份及2026-10-03新增材料界限保持，来源章不强套教学模板。 |
