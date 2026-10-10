# 按先修关系阅读

题目册和答案册使用同一个顺序。MT编号是稳定的查题编号，与当前页码及阅读先后无关。各组末尾的跨模型应用可在完成相关专题后回看；按原卷练习仍使用[原卷索引](PaperIndex.md)。

## 学习流程与模型诊断

先认识过拟合并走完CV流程，再判断成因、选择改进，最后处理欠拟合与模型选型。

1. [MT011 · 识别过拟合，并提出可操作的改进](Answers.md#mt011)
2. [MT004 · CV选完参数后，为什么还要重新训练？](Answers.md#mt004)
3. [MT028 · 训练误差低、测试误差高：可能原因](Answers.md#mt028)
4. [MT002 · 训练准、测试差：哪些改进值得尝试？](Answers.md#mt002)
5. [MT020 · 数据很多，训练和测试仍都差](Answers.md#mt020)
6. [MT022 · 五万客户、需要解释：选择哪种分类器？](Answers.md#mt022)

## Bayes、Naive Bayes与模型比较

从决策规则和建模对象进入Gaussian NB完整示范，再看假设、局限、模型比较和文本应用。

1. [MT040 · Bayes规则和Naive Bayes的关系](Answers.md#mt040)
2. [MT052 · 生成式分类器学了什么](Answers.md#mt052)
3. [MT046 · 完整讲出Gaussian NB](Answers.md#mt046)
4. [MT015 · NB的最优性、独立性与边界](Answers.md#mt015)
5. [MT032 · Bayesian classifier的性质](Answers.md#mt032)
6. [MT005 · NB的学习、不确定性和正则化](Answers.md#mt005)
7. [MT034 · 无限数据能消除分类错误吗](Answers.md#mt034)
8. [MT014 · 生成式与判别式的区别](Answers.md#mt014)
9. [MT033 · 用图像特征解释两种建模方式](Answers.md#mt033)
10. [MT059 · LR与共享方差Gaussian NB](Answers.md#mt059)
11. [MT021 · 同为线性分类器，学习原则有何不同](Answers.md#mt021)
12. [MT017 · 哪些模型能产生不同形状的边界](Answers.md#mt017)
13. [MT027 · 连续特征能否使用NB：混合选择题](Answers.md#mt027)
14. [MT058 · 智能笔上的文本NB如何改进](Answers.md#mt058)

## 逻辑回归与参数正则

先认清分数与概率，再读训练目标及正则强度，随后处理L2/L1、优化性质和模型比较。

1. [MT041 · Logistic的概率、多分类与最优解](Answers.md#mt041)
2. [MT047 · 解释Logistic目标中的两项](Answers.md#mt047)
3. [MT024 · 损失与正则项：α从哪里来？](Answers.md#mt024)
4. [MT018 · 为什么在线性分类器上加L2？](Answers.md#mt018)
5. [MT012 · L1逻辑回归：写目标并画边界](Answers.md#mt012)
6. [MT001 · Logistic训练：哪些说法不成立？](Answers.md#mt001)
7. [MT053 · LR与生成式模型：混合选择题](Answers.md#mt053)

## SVM与核方法

先学间隔与核技巧，再练核性质、RBF和合法性；掌握C的取舍后，处理比较、求解速度与预测存储。

1. [MT042 · SVM的基本特点](Answers.md#mt042)
2. [MT048 · 用一个例子讲清Kernel Trick](Answers.md#mt048)
3. [MT016 · 核SVM：变换、存储与非向量输入](Answers.md#mt016)
4. [MT031 · RBF距离与带宽：看近点和远点](Answers.md#mt031)
5. [MT055 · 判断五个候选核是否合法](Answers.md#mt055)
6. [MT060 · 二次核SVM：大C与小C的边界](Answers.md#mt060)
7. [MT054 · C、支持向量与RBF的零训练误差](Answers.md#mt054)
8. [MT043 · 核SVM怎样处理非线性？](Answers.md#mt043)
9. [MT029 · 哪些SVM说法错误？](Answers.md#mt029)
10. [MT010 · 同一张分布图，Gaussian Bayes与二次核SVM如何判断？](Answers.md#mt010)
11. [MT009 · 十万维特征、两千样本：SVM怎样提速？](Answers.md#mt009)
12. [MT061 · 预测内存：线性SVM与RBF SVM](Answers.md#mt061)

## 回归、特征选择与残差损失

先分清Ridge/LASSO、特征选择与Elastic Net，再比较残差损失、设计代价，最后分析模型改进。

1. [MT019 · Ridge、LASSO与零系数](Answers.md#mt019)
2. [MT045 · 特征选择：零系数、Ridge与OMP](Answers.md#mt045)
3. [MT030 · L1/L2回归的益处与措辞边界](Answers.md#mt030)
4. [MT057 · 同时使用L1与L2：Elastic Net](Answers.md#mt057)
5. [MT025 · 绝对残差损失对异常值有什么影响？](Answers.md#mt025)
6. [MT063 · Huber损失：画图并解释好处](Answers.md#mt063)
7. [MT013 · 残差L1＋权重L2，各自在做什么？](Answers.md#mt013)
8. [MT050 · 缺车比车多更糟：设计非对称损失](Answers.md#mt050)
9. [MT037 · 线性回归为何与均值预测器表现相近？](Answers.md#mt037)

## 集成学习

先比较bagging/boosting并认识RF，再用方差公式解释树数与相关性，最后讨论并行、更新和综合题。

1. [MT006 · Bagging与Boosting的基本区别](Answers.md#mt006)
2. [MT044 · 随机森林与Boosting的用途](Answers.md#mt044)
3. [MT062 · 随机森林：树多了为什么仍有共同误差？](Answers.md#mt062)
4. [MT056 · 集成方法：树深、并行与后续轮次](Answers.md#mt056)
5. [MT038 · 100核部署：RF与AdaBoost如何并行预测？](Answers.md#mt038)
6. [MT049 · 在线更新AdaBoost：速度与异常值](Answers.md#mt049)
7. [MT064 · 综合题：Bagging/Boosting与Huber](Answers.md#mt064)

## 分类损失图与错误代价

从有符号分数和简单曲线起步，逐渐分析零损失区、饱和与标准损失比较，再处理错误代价应用。

1. [MT008 · 平方形分类损失为什么惩罚“太正确”？](Answers.md#mt008)
2. [MT026 · V形损失：最优点为何在z=1？](Answers.md#mt026)
3. [MT051 · 负间隔也零损失：分类器会放过什么？](Answers.md#mt051)
4. [MT039 · 饱和的非凸分类损失](Answers.md#mt039)
5. [MT065 · 比较Logistic、Hinge和Exponential损失](Answers.md#mt065)
6. [MT007 · 筛查任务：漏诊比误报更贵](Answers.md#mt007)
7. [MT023 · 1000名受试者中只有50名阳性](Answers.md#mt023)
8. [MT035 · 正常邮件被大量拦截怎么办？](Answers.md#mt035)

## 神经网络与链式法则

先沿计算图走完链式求导与反传，再用梯度连乘理解梯度消失。

1. [MT067 · 链式求导与两层网络反传](Answers.md#mt067)
2. [MT066 · 梯度消失：为什么深度和激活函数有关？](Answers.md#mt066)

## 历史范围拓展：Gaussian Process

先认清历史GPR设定，再做GP与RF的应用比较；继续保留历史拓展身份。

1. [MT003 · 历史拓展：Gaussian Process的假设](Answers.md#mt003)
2. [MT036 · 历史拓展：音乐地理回归，GP还是RF？](Answers.md#mt036)
