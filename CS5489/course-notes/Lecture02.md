# Lecture 2 · Bayes Classifier & Naive Bayes Classifier
# 从花朵测量到文本分类：老师这一讲的完整路线

依据当前 Canvas 的 Lecture2a、Lecture2b 编写。

[配套 Tutorial 2](Tutorial02.ipynb) · [Assignment 1 方法指南](Assignment01.md) · [使用与运行说明](README.md)

**基础复习（可跳过）：** [按卡点选择：读公式与图像、概率、对数、导数、矩阵](../../learning/foundation-notes/MathForML.md#foundation-nav)。从四则运算和简单方程开始，每项附自查与图解；需要时再读，补完可返回本讲具体段落。

正文沿老师原课顺序展开，中文讲解配英文术语与简短英文要点。需要补齐的推导标为“补充解释”；课件或代码中的差异在相关位置说明。

<a id="intro"></a>
## 本讲先解决什么问题？

老师先给两种任务：收到一封邮件，判断是不是垃圾邮件；测量一朵鸢尾花，判断是哪一种。我们先沿用花朵，因为两个长度可以直接画出来；随后把同一套概率方法用于文字。

植物园已经记录一些花的种类、花瓣长度和萼片宽度。新来一朵花，我们能测长度，但不知道种类。训练数据中的标签是过去已知的信息；预测时不能偷看新花的标签。要做的是从已有记录学一个规则，输入测量值，输出类别。

上一讲的 Python、数组和概率在这里各有工作：数组保存记录，概率表达不确定性，程序把“估计参数”和“预测新样本”重复执行。本讲的路线由原课 Outline 和例子归纳：

> A：认识分类任务 → 用先验和类条件分布描述数据 → 从数据估计参数 → 用 Bayes 规则作决定。  
> B：把一个测量推广到多个测量 → 检查条件独立假设 → 用完整协方差建模 → 把邮件变成向量 → 选择适合文字表示的 NB 模型。

学完应能：解释 prior / likelihood / posterior 的区别；推导类别比例与高斯均值、方差的 MLE；手算一个 Bayes 决策；说明 NB 的条件独立和完整高斯的区别；把布尔、计数、TF-IDF 表示对应到实际代码；区分分类表现与模型假设是否成立。

### 阅读地图与优先级

“核心必会”是依据当前课程结构和任务给出的学习建议，不代表教师公布的必考清单。难度按从基础起步的学习者评估。

| 顺序与主题 | 学习优先级 | 难度：难在哪里 | 掌握要求 | 依据 |
|---|---|---|---|---|
| [分类与生成模型](Lecture02.md#classification) | 核心必会 | 低：区分输入与标签 | 解释任务和两部分概率模型 | Lecture2a，第4–12个单元 |
| [类别先验的 MLE](Lecture02.md#prior-mle) | 核心必会 | 中：从频数走到似然与求导 | 推导、计算、核对计数 | Lecture2a，第13–17个单元 |
| [高斯类条件与 MLE](Lecture02.md#gaussian-mle) | 核心必会 | 高：密度、对数、方差求导 | 解释分布并推均值/方差 | Lecture2a，第18–31个单元；历史 历史作业 Home_Assignments_1.pdf Ex2 为换分布推导 |
| [Bayes 决策与 log 分数](Lecture02.md#bayes-rule) | 核心必会 | 中：条件方向与归一化 | 手算类别和后验，说明适用条件 | Lecture2a，第32–48个单元 |
| [Gaussian NB 与测试](Lecture02.md#gaussian-nb) | 核心必会 | 中：给定类别后的独立 | 解释、计算、识别代码各步 | Lecture2b，第3–32个单元 |
| [完整协方差高斯](Lecture02.md#full-gaussian) | 核心必会 | 高：矩阵、距离、分布宽度 | 解释相关性，读懂得分与实现 | Lecture2b，第33–54个单元 |
| [词袋与 Bernoulli NB](Lecture02.md#bow) | 核心必会 | 中：文档数与词次数不同 | 建表示、手算出现/未出现证据 | Lecture2b，第55–79个单元；Tutorial 2 |
| [平滑、词解释、TF-IDF、Multinomial](Lecture02.md#smoothing) | 核心必会 | 中：分母与特征语义 | 计算、比较、避免数据泄漏 | Lecture2b，第80–97个单元；Tutorial 2；Assignment 1 |
| [其他预处理和词表示](Lecture02.md#extensions) | 常规掌握 | 低：知道解决什么问题 | 解释用途与限制 | Lecture2b，第99–100个单元 |
| 条件高斯分块证明、LDA 后验推导 | 二读拓展 | 高：配方与矩阵代数 | 本讲先认出假设差别，证明后读 | 历史 历史作业 Home_Assignments_1.pdf Ex3–4，非当前 Lecture 2 明列任务 |

先修只需补够本讲：乘法法则、条件概率、和为 1；自然对数把乘积变成和；一元导数的链式法则；向量、转置、矩阵乘法。正文会就近解释，并在需要的地方链接[可选数学补课](../../learning/foundation-notes/MathForML.md#foundation-nav)。课内主题也可沿[概率微课](https://crazyshout.github.io/micro-course/?lesson=ml05)、[参数估计微课](https://crazyshout.github.io/micro-course/?lesson=ml06)复习。

## Part A · Bayes Classifier

<a id="classification"></a>
## 1. Classification Examples / General Classification Problem｜先认清一条记录

可选补课：看不懂下标、列向量或数据形状时，先读[符号与函数](../../learning/foundation-notes/MathForML.md#symbols-functions)或[一条记录怎样变成向量](../../learning/foundation-notes/MathForML.md#vectors-covariance)。

老师用 petal length（花瓣长度）和 sepal width（萼片宽度）作特征。下图标出了花瓣和萼片的位置。

![老师原图：花瓣与萼片的部位标识](assets/Petal-sepal.jpg)

| 老师给的类别例图 | |
|---|---|
| ![原图：Iris versicolor](assets/iris-versicolor.jpg) | ![原图：Iris virginica](assets/iris-virginica.jpg) |
| Versicolor，标签 1 | Virginica，标签 2 |

图源：Lecture2a，第5个单元引用的原图片。

数学上，一朵花用列向量 $\mathbf{x}=(x_1,x_2)^T\in\mathbb{R}^2$ 表示；$x_1$ 是花瓣长度，$x_2$ 是萼片宽度，单位均为厘米。类别 $y\in\mathcal{Y}=\{1,2\}$，这些整数是名字，不表示 Virginica 比 Versicolor“大一倍”。

代码把很多样本堆在矩阵里：X 的每一行是一朵花，每一列是一项测量。因此 X.shape=(100,2)，y.shape=(100,)。单个数学向量习惯写成列，与程序按行存样本并不矛盾。

![按原 iris2.csv 重绘：每个点是一朵花，形状和颜色共同表示种类](assets/iris-measurements.png)

*按原iris2.csv的100条记录重绘，横纵轴单位均为厘米。*

两类的平均位置不同，但点有重叠。一个简单分界可能分对大多数，仍不能仅凭位置远近排除不确定性。这正是后面需要概率模型的原因。

**English takeaway — 整理后的表达：** A feature vector describes the measurements of one object. A class label identifies its category. Classification predicts the label of a new object from its observed features.


**来源与掌握要求：** Lecture2a，第4–8个单元，PDF 1–3页。

<a id="generative"></a>

## 2. Probabilistic model / Class model｜把“这朵花从哪里来”分成两部分

可选补课：如果竖线后的条件容易混淆，先用[100封邮件的人数表](../../learning/foundation-notes/MathForML.md#conditional-probability)把分母看清楚。

老师的 generative model（生成式模型）先描述类别出现的比例，再描述每类产生怎样的特征：

$$p(\mathbf{x},y)=p(y)\,p(\mathbf{x}\mid y).$$

这里的“生成”是概率建模方式，并不要求程序真的画出一朵花。

- $p(y=c)$ 是 **prior probability（先验概率）**：还没看这朵花的测量值，类别 c 有多常见。
- $p(\mathbf{x}\mid y=c)$ 是 **class-conditional distribution，CCD（类条件分布）**：已经知道种类是 c 时，怎样的测量值比较常见。
- 预测真正需要的是 **posterior probability（后验概率）** $p(y=c\mid\mathbf{x})$：已经看见测量值之后，各种类有多可信。

先验不是“随便猜一个数”，类条件分布也不是后验。它们的已知条件不同，就像“已知是猫，观察到胡子的可能性”和“观察到胡子，是猫的可能性”不能直接调换；后者还得考虑世界上有多少其他长胡子的对象。

先假设两类比例为 0.4、0.6，设参数 $\pi=p(y=1)$，可写：

$$p(y)=\pi^{\mathbb{1}(y=1)}(1-\pi)^{\mathbb{1}(y=2)}.$$

指示函数 $\mathbb{1}(q)$ 在条件 q 成立时取1，否则取0。若 y=1，式子留下 $\pi$；若 y=2，留下 $1-\pi$。这里的 $\pi$ 是待估先验参数；后面高斯常数中的 $2\pi$ 使用的是圆周率，含义由上下文区分。

**English takeaway：** A generative classifier models the class prior and the class-conditional distribution. Bayes' rule reverses the conditioning to obtain the posterior needed for prediction.


**来源与掌握要求：** Lecture2a，第9–12个单元，PDF 3–4页。核心必会；难度低；要求能解释模型分解。
来源：Lecture2a，第12个单元。

<a id="prior-mle"></a>

## 3. Learn from our data｜为什么类别比例是一个最大似然解？

可选补课：[乘积为何能变成对数之和](../../learning/foundation-notes/MathForML.md#log-products) · [从求导走到最大值](../../learning/foundation-notes/MathForML.md#maxima-mle)。补完后可直接返回这一节。

假设训练标签 $y_1,\ldots,y_N$ 独立采自同一类别分布。数出标签1有 $N_1$ 个、标签2有 $N_2$ 个，$N=N_1+N_2$。似然把**已经看到的数据固定**，让参数变化：

$$L(\pi)=\prod_{i=1}^N p(y_i;\pi)=\pi^{N_1}(1-\pi)^{N_2}.$$

Maximum Likelihood Estimation，**MLE（最大似然估计）**选择让这些观测最容易出现的参数。它不是“给参数本身计算一个后验”。

对数在正数上单调递增，不改变最大值的位置，并把乘积改成好处理的加法：

$$\ell(\pi)=\log L(\pi)=N_1\log\pi+N_2\log(1-\pi).$$

两类都出现时，在 $0<\pi<1$ 中求导：

$$\frac{d\ell}{d\pi}=\frac{N_1}{\pi}-\frac{N_2}{1-\pi}=0
\quad\Longrightarrow\quad N_1(1-\pi)=N_2\pi
\quad\Longrightarrow\quad\hat\pi=\frac{N_1}{N}.$$

**补充解释：为什么是最大值？** 二阶导数为 $-N_1/\pi^2-N_2/(1-\pi)^2<0$，函数向下弯。若某类完全没有出现，最大值在0或1的边界；不能继续把会除以零的内点推导硬套过去。

教学手算：10条标签中4条为1、6条为2，得到 $\hat\pi=0.4$。原 iris2.csv 两类各50条，因此 Lecture2a，第17个单元 的代码得到 [0.5,0.5]。**Lecture2a，第12个单元的0.4/0.6是说明先验的例子，Lecture2a，第17个单元的0.5/0.5才是该文件的经验比例。**

多类时同理：$\hat p(y=c)=N_c/N$。若训练集被人为按类抽样，这个比例反映抽样结果，不自动等于真实部署人群的类别比例。

**English takeaway：** Under independent sampling, the MLE of a class prior is its relative frequency in the training sample. An empirical training prior may differ from the deployment prior if sampling changes class proportions.


**来源与掌握要求：** Lecture2a，第13–17个单元，PDF 4–5页。核心必会；难度中；要求推导并核对计数。

<a id="observation"></a>

## 4. Observation model / Gaussian distribution｜从直方图到一条密度曲线

可选补课：[密度高度与区间面积](../../learning/foundation-notes/MathForML.md#density-area) · [均值、方差与标准差](../../learning/foundation-notes/MathForML.md#mean-variance)。

先只用花瓣长度 x。把两种花分别画直方图，可看到它们常出现在哪些长度附近。直接靠很多小柱子描述分布会比较零碎，于是老师选择高斯分布：

$$p(x\mid y=c)=\frac{1}{\sqrt{2\pi\sigma_c^2}}
\exp\!\left[-\frac{(x-\mu_c)^2}{2\sigma_c^2}\right].$$

$\mu_c$ 是类别 c 的平均长度，单位厘米；$\sigma_c$ 是标准差，单位厘米；$\sigma_c^2$ 是方差，单位平方厘米。每个类别有自己的参数。均值控制山峰位置，标准差控制展开宽度；前面的系数保证曲线下的面积为1。

连续变量的 $p(x\mid c)$ 是 **density（密度）**，单位为1/厘米。曲线高度不是“恰好这个长度的概率”，高度也不必小于1；一个长度区间的概率由区间下的面积给出。

**原课核对：** Lecture2a，第20个单元 没有设置 density=True，柱高实际是每箱计数，尽管纵轴标成了 p(x|y)。Lecture2a，第30个单元 才将直方图按密度归一化后与高斯曲线比较。读图要看代码如何统计，不能只看纵轴文字。

课堂用均值2.3、标准差1.5演示曲线；这是高斯形状示例，不是从 iris 数据估出的参数。一维正态分布在均值两侧两个标准差内约有95.45%的概率质量，原图“95%”是近似，不能把这个数直接搬到二维椭圆。

**English takeaway：** A Gaussian class-conditional model has a mean and variance for each class. For a continuous feature, the density height is not a point probability; probabilities are areas over intervals.


**来源与掌握要求：** Lecture2a，第18–25个单元，PDF 5–7页。核心必会；难度中；要求区分概率、频数和密度。
来源：Lecture2a，第24个单元。

<a id="gaussian-mle"></a>

## 5. MLE for Gaussian｜均值和方差不是凭经验塞进公式

可选补课：下面用到[求导规则](../../learning/foundation-notes/MathForML.md#derivative-rules)、[链式法则](../../learning/foundation-notes/MathForML.md#chain-rule)和[偏导时固定哪个变量](../../learning/foundation-notes/MathForML.md#partial-derivatives)，每项都有分步算例。

这一小节的 $\{x_i\}_{i=1}^N$ **都是某一个类别的观测**。这里 N 是该类样本数，不是前面两类相加的总数；以下先沿用原课记法，涉及多类时写 $N_c$。

在独立同分布、正方差的高斯模型下：

$$\ell(\mu,\sigma^2)=-\frac{N}{2}\log(2\pi\sigma^2)
-\frac{1}{2\sigma^2}\sum_{i=1}^N(x_i-\mu)^2.$$

先固定方差，对均值求导。平方残差外层求导后，还要乘内部 $x_i-\mu$ 对 $\mu$ 的导数 −1，两个负号抵消：

$$\frac{\partial\ell}{\partial\mu}
=\frac{1}{\sigma^2}\sum_i(x_i-\mu)=0
\quad\Rightarrow\quad
\hat\mu=\frac{1}{N}\sum_i x_i.$$

原课给出了方差结果，下面补中间步骤。令 $v=\sigma^2$，避免把“对方差求导”和“对标准差求导”混在一起：

$$\frac{\partial\ell}{\partial v}
=-\frac{N}{2v}+\frac{\sum_i(x_i-\mu)^2}{2v^2}=0
\quad\Rightarrow\quad
\hat\sigma^2=\frac{1}{N}\sum_i(x_i-\hat\mu)^2.$$

例如某类的三个教学测量为2、4、6厘米：均值4厘米，平方偏差和为8平方厘米，MLE方差 $8/3$ 平方厘米，标准差 $\sqrt{8/3}$ 厘米。无偏样本方差使用 N−1，此例得到4平方厘米；它回答的是另一种估计性质，不能把分母替换后仍称同一个MLE公式。

这些内点结论要求样本不是全部相同等退化情形。若全部观测相同，无约束正态似然会在方差趋向零时增大，不能把零方差当成正常的连续密度模型。

拟合代码中的 stats.norm.fit 返回 **mean 和 standard deviation**，不是方差；Lecture2a，第30个单元 的 scale 也接收标准差。变量名 G1std 与后面的平方根很容易混，应沿着单位检查。

本次对原花瓣长度数据重算得到：

| 类别 | 样本数 | 均值 μ（cm） | MLE标准差 σ（cm） |
|---|---:|---:|---:|
| Versicolor（1） | 50 | 4.2600 | 0.4652 |
| Virginica（2） | 50 | 5.5520 | 0.5463 |

这张表使用A部分的全体数据作分布说明；B部分的训练/测试实验会重新只用训练样本估参数，不能直接把这张表作为B的测试模型。

![原花瓣长度数据的拟合密度与后验，类别先验均为0.5](assets/iris-density-posterior.png)

*图左沿用 Lecture2a，第29个单元 的 MLE 思路，用原数据重算；图右将在下一节解释。两边横轴相同，纵轴含义不同。参数与重算记录见 source-manifest.json 和本地检查记录。*

**English takeaway：** For nondegenerate Gaussian observations, MLE gives the sample mean and the variance with denominator N. Standard deviation is the square root of variance. The N−1 covariance convention is a different estimator.


**来源与掌握要求：** Lecture2a，第26–31个单元，PDF 7–9页。核心必会；难度高；要求能推导、计算、解释分母。
来源：Lecture2a，第29个单元。

<a id="bayes-rule"></a>

## 6. Bayesian Decision Rule / Bayes' Rule｜终于给新花一个类别

现在已经有类别比例，也知道各类通常长什么样。给定新测量 x，先算每个类别的“支持分数”：

$$s_c=p(x\mid y=c)p(y=c),\qquad
p(y=c\mid x)=\frac{s_c}{\sum_{k\in\mathcal{Y}}s_k}.$$

分母 $p(x)=\sum_k p(x\mid k)p(k)$ 把所有候选归一化。它与候选类别 c 无关，但会随输入 x 改变。在 $p(x)>0$ 时，所有类别的后验和为1。

**教学手算 / Worked example**

中文题：某个新测量在两类下的密度为0.4、0.2，两个先验为0.25、0.75，采用相同错分代价。预测哪一类？两个后验是多少？

English question: The class-conditional densities at a new measurement are 0.4 and 0.2, and the priors are 0.25 and 0.75. With equal misclassification costs, which class is selected and what are the two posteriors?

答案：分子分别为 $0.4\times0.25=0.10$、$0.2\times0.75=0.15$。归一化得到0.4、0.6，选类2。只比密度会选类1，因此不能忘先验。分子的数值是密度乘概率，不应称为类别概率。

English answer: The two unnormalized scores are 0.10 and 0.15. Normalization gives posteriors 0.4 and 0.6, so class 2 is selected. Comparing densities alone would ignore the prior.

**补充解释：为什么选最大后验？** 选类 c，在该输入处猜错的概率是 $1-p(c\mid x)$；让它最小，就让后验最大。这个最优性结论针对真分布下的 **0–1 loss（所有错分代价相同）**。估出来的模型可能不准确；若漏报和误报的代价不同，则应比较期望损失，不能无条件使用同一门槛。

二类的决策边界位于后验相等处。上图右侧两条曲线交会时，各为0.5。曲线给出当前模型的后验；预测是否正确还要用真实标签评价。

**原课核对：** Lecture2a，第39个单元 用统计“类1后验更大”的网格点数找分界，隐含在所画区间里有一个按序交叉的条件。不同方差的高斯可以产生多个或没有交点；一般程序应查符号变化或解等分方程，不能只靠点数定位。

**English takeaway：** Under equal error costs and the true class probabilities, selecting the largest posterior minimizes conditional classification error. Estimated probabilities and unequal costs require separate care.


**来源与掌握要求：** Lecture2a，第32–40个单元，PDF 9–11页。核心必会；难度中；要求手算后验和决策。

<a id="log-scores"></a>

## 7. Bayes rule revisited｜为什么代码常常只算 log 分子？

可选补课：如果不熟悉负对数和连乘变求和，先读[指数与自然对数](../../learning/foundation-notes/MathForML.md#powers-logs)。

选谁最大时，所有类别都除以同一个正数，所以可以省略分母：

$$\hat y=\arg\max_c p(x\mid c)p(c)
=\arg\max_c\{\log p(x\mid c)+\log p(c)\}.$$

例如三个小概率相乘可能很小，高维文本更明显；对数把它们变成一串加法，不容易因下溢全变成0。但“为选类别省略分母”不等于“报告概率也不用归一化”。

设 log 分子组成向量 $z_c=\log p(x\mid c)+\log p(c)$，则

$$\log p(c\mid x)=z_c-\operatorname{logsumexp}(z),\qquad
\operatorname{logsumexp}(z)=m+\log\sum_c e^{z_c-m},\quad m=\max_c z_c.$$

减掉 m 后所有指数不超过1，再把 m 加回去；这个数值技巧不改变数学结果。比如 z=(−1001,−1000)，直接指数可能都变成0，但平移后是 $(e^{-1},1)$，后验约为(0.2689,0.7311)。

训练与预测的过程应能用英文复述：训练时分别估计每类的特征分布和类别比例；预测时对同一个新输入比较各类后验，或等价的 joint / log-joint scores。接下来更换的是“每一类的特征怎样分布”，估计参数和应用Bayes规则的过程仍然相同。

**English takeaway：** The posterior, joint score and log-joint score give the same argmax when defined consistently. Use log-sum-exp to recover normalized probabilities without numerical underflow.

**来源与掌握要求：** Lecture2a，第41–49个单元，PDF 11–13页。核心必会；难度中；要求辨认等价决策与归一化用途。
来源：Lecture2a，第48个单元。


## Part B · Naive Bayes Classifier

<a id="gaussian-nb"></a>
## 8. Naive Bayes Classifier / Learn Gaussian NB model｜把两项测量一起使用

可选补课：[按行数据与列向量](../../learning/foundation-notes/MathForML.md#vectors-covariance) · [独立假设何时允许相乘](../../learning/foundation-notes/MathForML.md#independence)。

一项测量丢掉了另一项信息。现在输入 $\mathbf{x}=(x_1,x_2)^T$，需要联合分布 $p(x_1,x_2\mid y)$。老师先用 **Naive Bayes（朴素贝叶斯）**简化：

$$p(\mathbf{x}\mid y=c)=\prod_{j=1}^{d}p(x_j\mid y=c).$$

“朴素”指**给定类别后，特征条件独立**，不是说混在一起的所有花瓣和萼片长度必须无条件独立。不同类别的混合本来就可能带来整体相关性。

Gaussian NB 让每一维都是一元高斯，每一类都有 d 个均值和 d 个方差：

$$\log p(\mathbf{x}\mid c)
=\sum_{j=1}^{d}\left[
-\frac12\log(2\pi\sigma_{c,j}^2)
-\frac{(x_j-\mu_{c,j})^2}{2\sigma_{c,j}^2}
\right].$$

它相当于多元高斯的对角协方差模型。等密度线是沿坐标轴方向的椭圆，不能随数据的倾斜方向旋转。

**课堂代码怎样对应公式**

~~~python
model = naive_bayes.GaussianNB()
model.fit(trainX, trainY)
model.class_prior_   # 每类先验
model.theta_         # shape: (类别数, 特征数)，均值
model.var_           # 同样形状，方差而非标准差
~~~

课堂实验使用50%训练、50%测试，random_state=4487。原代码未传 stratify，因此没有启用分层抽样；加入该参数会改变划分。Lecture2b，第5个单元 的全局种子100和 Lecture2b，第12个单元 的显式划分种子也承担不同角色。

估参数只能用训练集。Lecture2b，第17–24个单元的绘图代码则建立二维网格，把每个格点当新输入计算密度或后验，再恢复成图；图上密集的网格不是额外的训练花朵。椭圆绘图函数计算特征值来决定方向和轴长，第一遍读懂它在展示什么即可，不要求先背完整绘图实现。

**English takeaway：** Naive Bayes assumes feature independence conditional on the class. Gaussian NB estimates a mean and variance for every class–feature pair, giving an axis-aligned Gaussian model.


**来源与掌握要求：** Lecture2b，第1–24个单元，PDF 1–7页。核心必会；难度中；要求解释条件独立、读参数形状和训练流程。
来源：Lecture2b，第12个单元。

<a id="testing"></a>

## 9. View the Posterior / Evaluate on the test set｜看边界，也看它分错了谁

predict_proba 返回每条记录对各类的后验；predict 返回选中的类别。accuracy 是预测标签与真实标签相同的比例。数组里的第0列是什么类别，要结合 classes_ 或显式的类别映射确认，不能把“第一列”和“标签0”当同一件事。

图中用空心方框圈出测试错误。看这些点能检查错误是否集中在重叠区域，但“离边界远”仍可能错：模型的分布假设、数据质量或部署分布都可能出问题。

原课“边界附近后验降低”的准确理解是：二类等代价边界附近，两个后验接近0.5，**最大后验**不高；不是说两个类别的概率会一起接近0。

**English takeaway：** Fit on training data, predict labels for test data, and compare them with the true labels. A probability column must be matched to its class label, and a confident model prediction can still be wrong.


**来源与掌握要求：** Lecture2b，第25–32个单元，PDF 7–9页。核心必会；难度低；要求区分拟合、预测、评价。
来源：Lecture2b，第31个单元。

<a id="full-gaussian"></a>

## 10. Naive Bayes Assumption / Multivariate Gaussian｜为什么椭圆需要倾斜？

可选补课：先用[四条小数据算协方差](../../learning/foundation-notes/MathForML.md#covariance)，再认识[逆矩阵与行列式](../../learning/foundation-notes/MathForML.md#inverse-determinant)；[马氏距离分步计算](../../learning/foundation-notes/MathForML.md#gaussian-bridge)可帮助读下面的式子。

把同一种花单独拿出来，花瓣更长时萼片也可能更宽。独立模型把这种“一起变化”忽略了。完整高斯用一个矩阵把这些关系记下来：

$$\boldsymbol\mu_c\in\mathbb R^d,\qquad
\boldsymbol\Sigma_c\in\mathbb R^{d\times d},\qquad
p(\mathbf{x}\mid c)=
\frac{\exp[-\frac12(\mathbf{x}-\boldsymbol\mu_c)^T
\boldsymbol\Sigma_c^{-1}(\mathbf{x}-\boldsymbol\mu_c)]}
{(2\pi)^{d/2}|\boldsymbol\Sigma_c|^{1/2}}.$$

矩阵对角线是各维方差；非对角线是协方差。正协方差表示围绕均值同向变化的趋势，负协方差表示反向趋势。独立且二阶矩存在会得到零协方差；反过来一般不成立，联合高斯是零协方差可推出独立的重要特例。

![原课四个协方差矩阵的等密度形状重绘](assets/covariance-shapes.png)

*图：均值都是零，两维方差都是1，非对角元分别为0、0.5、0.9、−0.9；输入无量纲。画的是马氏距离平方等于4的轮廓；它与一维正态的约95%区间含义不同。*

公式里有两个容易跳过的部分：

1. **Mahalanobis distance（马氏距离）**修正“离均值多远”。在本来波动大的方向，偏离一点没有那么意外；在波动很小的方向，相同偏离更显眼。
2. **Determinant（行列式）**对应分布的尺度体积。一个到处摊得很宽的分布不能只因距离代价小就总占便宜，归一化系数也会降低密度高度。

分类时的 log 分数可写成

$$g_c(\mathbf{x})=
-\frac12(\mathbf{x}-\boldsymbol\mu_c)^T\boldsymbol\Sigma_c^{-1}(\mathbf{x}-\boldsymbol\mu_c)
-\frac12\log|\boldsymbol\Sigma_c|+\log\pi_c,$$

其中 $\pi_c=p(y=c)$；所有类共有的 $-\frac d2\log(2\pi)$ 可以在比较时省略。只比较“校正后的距离”仍可能漏掉分布宽度和先验。

**补充手算 / Worked bridge**

取无量纲 $\mathbf{x}=(1,1)^T$、均值零，比较 $\Sigma_A=I$ 与
$\Sigma_B=\begin{pmatrix}1&0.5\\0.5&1\end{pmatrix}$。A的距离平方为2。B的逆为
$\frac1{0.75}\begin{pmatrix}1&-0.5\\-0.5&1\end{pmatrix}$，所以距离平方为 $4/3$。点沿两个坐标一起增大的方向移动，符合B的正相关趋势。若要完成类别比较，还需行列式和类别先验，不能只停在这两个距离。

English check: With the same point and covariance matrices, which model gives a smaller squared Mahalanobis distance, and is that alone enough for classification?

English answer: Model B gives 4/3, compared with 2 under A. No: covariance determinants and class priors also enter the Gaussian classification score.

**English takeaway：** Full covariance models within-class feature dependence. Gaussian classification combines a covariance-adjusted distance, a normalization term involving the determinant, and the class prior.


**来源与掌握要求：** Lecture2b，第33–42个单元，PDF 9–11页。核心必会；难度高；要求解释协方差和读懂得分。

<a id="gaussian-code"></a>

## 11. Gaussian Bayes Classifier｜从公式读到老师的类实现

可选补课：[矩阵乘法与外积](../../learning/foundation-notes/MathForML.md#matrix-products) · [协方差公式怎样逐格计算](../../learning/foundation-notes/MathForML.md#covariance)。

对类别 c 的 $N_c$ 个训练样本，理论MLE为

$$\hat{\boldsymbol\mu}_c=\frac1{N_c}\sum_{i:y_i=c}\mathbf{x}_i,\qquad
\hat{\boldsymbol\Sigma}_c=\frac1{N_c}\sum_{i:y_i=c}
(\mathbf{x}_i-\hat{\boldsymbol\mu}_c)(\mathbf{x}_i-\hat{\boldsymbol\mu}_c)^T.$$

协方差可能奇异：样本少、某些特征完全重复或方向上没有变化。Lecture2b，第40个单元加入 $\alpha I$，给所有特征方向的方差增加正数；这能改善可逆性，但不是额外收集了数据。尺度不同的特征还需考虑这种惩罚的单位含义。

分类器的实现可以按五个动作读：

| 方法 | 输入与输出 | 对应数学工作 |
|---|---|---|
| fit | X为样本×特征，y为标签 | 按类别估均值、协方差、先验 |
| compute_logccd | 一批X、类别c → 每条样本一个值 | $\log p(\mathbf{x}\mid c)$ |
| compute_logjoint | X → 样本×类别 | 加 $\log\pi_c$ |
| predict_logproba / predict_proba | X → 样本×类别 | 用 logsumexp 归一化／再指数 |
| predict | X → 每条样本一个标签 | 对类别轴取最大分数 |

**原课核对：两个不能悄悄混用的约定。**

- Lecture2b，第39个单元 的MLE协方差分母是 $N_c$；Lecture2b，第44个单元 的 numpy.cov(Xc,rowvar=False) 默认分母是 $N_c-1$。要复现代码就保留默认；要严格实现该MLE公式，可指定 ddof=0。这里的公式与代码分别沿用上述约定。[NumPy 官方说明](https://numpy.org/doc/stable/reference/generated/numpy.cov.html)
- 原类用 K=max(y)+1，默认标签连续从0开始。Lecture2b，第46个单元传入 trainY−1，Lecture2b，第54个单元预测后再加1。忘掉这对映射，会把模型预测正确但编码不同误算成错误。

这是**每个类别独立估计完整协方差**；历史资料的 LDA 假设各类共享一个协方差矩阵，不能仅因都叫 Gaussian classifier 就视为相同。多估相关性会增加参数和数据需求，不保证在每个小数据集都更好。

![同一原课训练划分上的Gaussian NB和完整高斯决策边界](assets/iris-model-comparison.png)

*图：沿用原 Lecture2b，第12个单元 的50/50划分与种子4487，完整高斯保留原 numpy.cov 的 N_c−1 约定；点仅显示训练记录，虚线为两类后验相等处。测试集比较见下文；图中显示的是训练记录。*

按原Lecture2b，第12个单元划分与上述代码约定，本次重算得到Gaussian NB为42/50=84%，完整高斯为45/50=90%。这解释了Lecture2b，第53个单元在该例子里的比较；只是一份固定小划分的结果，不能据此宣布完整协方差在任何数据上更优。

**English takeaway：** The instructor's GaussianBayes estimates a separate covariance matrix for each class. Its covariance code uses the N−1 convention, while the displayed MLE formula uses N. The custom class also requires an explicit label mapping.


**来源与掌握要求：** Lecture2b，第39–54个单元，PDF 10–14页。核心必会；难度高；要求辨认估计器、标签映射和数值处理。
来源：Lecture2b，第44个单元。

<a id="bow"></a>

## 12. Naive Bayes Spam Classifier / Text Document Representation｜文字怎样进入同一套模型？

现在回到老师开头的邮件。概率模型需要特征，原始字符串还不是一组固定坐标。**Bag-of-Words，BoW（词袋）**先固定词表，每个位置对应一个词，再记录词出现多少次。

原例词表依次为 [this, test, spam, foo]。句子“This is a test document”得到 [1,1,0,0]：不在词表里的词不占坐标。词表顺序就是模型坐标顺序，不能训练时第一列表示this，预测时第一列忽然变spam。

![原课引用的词袋示意图，保留原文字](assets/tom-mitchell-bow.jpg)

“this is spam”和“is this spam”得到相同向量 [1,0,1,0]。BoW保留哪些词及其计数，丢掉语序。“not good”和“good”也可能因为停用词处理丢掉重要差别，所以预处理选择应跟任务一起验证。

**English takeaway：** Bag-of-words maps documents to a fixed vocabulary coordinate system. It retains word occurrences or counts but discards word order; words outside the vocabulary are ignored.


**来源与掌握要求：** Lecture2b，第55–58个单元，PDF 14–15页。核心必会；难度低；要求构造向量并说明信息损失。

<a id="vectorizer"></a>

## 13. Steps to make BoW｜词表只能从训练资料里学

读取数据时，从 email 子目录读取文本，各子目录对应一类。类别名称由 target_names 给出，别未经核对就假定数字1永远表示spam。随后Lecture2b，第61个单元用种子11做50/50划分。代码中的 replace 解码处理是读取策略，不是文本分类算法本身。

构造词向量的 CountVectorizer 使用英文停用词、最多100个常见词，并默认小写化：

~~~python
cntvect = feature_extraction.text.CountVectorizer(
    stop_words="english", max_features=100
)
trainX = cntvect.fit_transform(traintext)
testX = cntvect.transform(testtext)
~~~

fit 确定词表，transform 按既定词表编码新文本。测试集只做后者；如果也在测试集拟合，既改变了列的含义，又让测试信息参与表示选择。

输出矩阵是“文档数×实际词表大小”。大量零表示文档没出现该词；稀疏矩阵只存非零项，零仍然存在于模型的语义里。查看少量样本时可用 toarray，不能为了“看着方便”把任何规模的全文档矩阵都变成稠密数组。

原 showVocab 是显示辅助：它按词字符串排序，但打印每个词的真实索引；注释“sort by index”不精确。它还成对调用 next，奇数个待显示词时需要处理最后一个。读懂方法不要求背这段打印代码。

**English takeaway：** Fit the vocabulary on training text and reuse exactly that mapping for other splits. Sparse storage omits stored zeros, not the meaning of absent words.


**来源与掌握要求：** Lecture2b，第58–71个单元，PDF 15–20页。核心必会；难度中；要求读懂 fit / transform 与稀疏矩阵。
来源：Lecture2b，第59个单元。
来源：Lecture2b，第62/71个单元。

<a id="bernoulli"></a>

## 14. Naive Bayes model for Boolean vectors｜一个词没出现，也是一条证据

Bernoulli NB关心**出现还是没出现**。固定词j、类别c，令
$\pi_{j,c}=P(x_j=1\mid y=c)$，其中 $x_j\in\{0,1\}$。若该类有 $N_c$ 篇文档，其中 $N_{j,c}$ 篇含词j，无平滑MLE为 $\hat\pi_{j,c}=N_{j,c}/N_c$。

同一封邮件写五遍“free”，在这一模型里仍是一次“出现”；不能把5加到“含词文档数”中。其文档 log 分数是

$$\log p(c)+\sum_{j=1}^{V}
\big[x_j\log\pi_{j,c}+(1-x_j)\log(1-\pi_{j,c})\big].$$

第二项中的 $(1-x_j)$ 使未出现的词也贡献证据。可以把固定词表看作一份清单：每个词勾上或未勾上，分别对应公式中的出现项和未出现项。

课堂调用的 BernoulliNB 默认可将计数按是否大于0转成布尔。注意 alpha=0 可能遇到零或一的估计，导致对数无穷或某个样本在所有类别下都被判为不可能；这正是老师接着讲平滑的原因。不要把数值警告当成正常概率。

**English takeaway：** Bernoulli NB models document-level word presence. Both present and absent vocabulary terms contribute to the score; repeated occurrences do not increase a binary feature.


**来源与掌握要求：** Lecture2b，第72–79个单元，PDF 20–25页。核心必会；难度中；要求区分出现文档数与出现总次数。
来源：Lecture2b，第74个单元。

<a id="smoothing"></a>

## 15. Smoothing｜没有见过，不等于绝不可能

如果某类训练文档从未出现一个词，无平滑估计为0。它把有限样本里的“没见过”升级成了绝对禁令。老师给出的加法平滑为

$$\tilde\pi_{j,c}=\frac{N_{j,c}+\alpha}{N_c+2\alpha},\quad \alpha>0.$$

分母加 $2\alpha$，因为这个词的Bernoulli试验只有“出现／未出现”两种结果；不是因为词表只有两个词，也不是因为只有两个类别。$\alpha=1$通常叫 Laplace smoothing；其他正值是加法平滑。它改变估计，可能帮助泛化，不能保证任何一次测试分数都提高。

**教学手算 / Worked example**

中文题：两类各3篇文档，词表为 [free, meeting]。Spam里两个词分别出现在2、1篇，Ham里分别出现在0、2篇。取 $\alpha=1$、相等先验，新邮件的布尔向量是 [1,0]。求两类的类条件分数和Spam后验。

English question: Each class has three documents. In vocabulary [free, meeting], document-presence counts are [2,1] for Spam and [0,2] for Ham. Use alpha=1 and equal priors. For binary vector [1,0], find both conditional scores and the Spam posterior.

答案：Spam参数 [3/5,2/5]，Ham参数 [1/5,3/5]。新邮件出现free但不出现meeting，所以分数为 $(3/5)(3/5)=9/25$ 与 $(1/5)(2/5)=2/25$；相等先验消去后，Spam后验是 $9/11\approx0.8182$。漏掉未出现项会得到另一个答案。

English answer: Smoothed parameters are [3/5,2/5] and [1/5,3/5]. The conditional scores are 9/25 and 2/25, giving Spam posterior 9/11. The absent word contributes through its complementary probability.

**English takeaway：** Smoothing prevents unseen events from receiving an automatic zero estimate. The Bernoulli denominator adds two pseudo-count contributions because each feature has two possible outcomes.


**来源与掌握要求：** Lecture2b，第80–84个单元，PDF 25–26页。核心必会；难度中；要求会算平滑参数并解释分母。

<a id="words"></a>

## 16. Frequent words / Most informative words｜常见词不一定最能区分类别

在Spam中出现率很高的词，可能在Ham中也很常见。按单类的 feature_log_prob_ 排名前十，得到的是该类模型下的高概率词；要讨论区分性，还需看另一类。

老师比较 $\log p(w_j\mid y=1)-\log p(w_j\mid y=0)$。差为正说明该词出现更支持类1。对于Bernoulli完整文档分类，还要考虑词未出现的项和先验，不能把这一个排名直接当成全部决策公式。

**原课核对：** 平滑演示使用 bmodels，但Lecture2b，第86/88个单元仍读取之前的 bmodel。解读输出时必须说明在看哪个对象；要分析平滑结果，就应一致读取平滑模型。否则图、排名和结论可能来自不同实验。

**English takeaway：** A frequent word within one class need not distinguish that class from others. Compare class-specific scores and keep the model object consistent across plots, rankings and conclusions.


**来源与掌握要求：** Lecture2b，第85–88个单元，PDF 26–27页。常规掌握；难度中；要求解释词表排名的含义。

<a id="tfidf"></a>

## 17. Naive Bayes for Count Vectors / TF-IDF｜从是否出现，走到出现多少与多稀有

Boolean只问有没有；count记录出现次数；**term frequency，TF（词频）**还会按文档长度归一化。原课写

$$\mathrm{TF}_{j,D}=\frac{w_j}{|D|},\qquad
\mathrm{IDF}(j)=\log\frac{N}{N_j},\qquad
x_j=\mathrm{TF}_{j,D}\,\mathrm{IDF}(j).$$

这里 $w_j$ 是该词在当前文档D中的计数，$|D|$ 是文档词数；N是用于估计IDF的训练文档数，$N_j$ 是其中包含词j的文档数，**不是词j出现的总次数**。普遍出现在各文档中的词，区分文档的能力往往有限，因此IDF降低其权重。

补充小例：4篇训练文档中，“market”出现在1篇，课堂简式给IDF=log4；“news”出现在全部4篇，给IDF=0。两者都只按“哪些文档含它”计数，单篇反复出现不增加文档频数。

**原课核对：Lecture2b，第91个单元的库调用是另一个明确约定。** TfidfTransformer(use_idf=True,norm="l1") 默认使用平滑IDF：
$\log[(1+N)/(1+N_j)]+1$，然后将非零文档向量按L1归一化；全零行仍是零。它不等于逐字执行上一段简式。例中“news”的库IDF是1而非0。[官方参数与公式](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfTransformer.html)

IDF同样只能从训练数据拟合，测试数据用同一个transform。词表、IDF和分类器都是流程的一部分，不是只有最后一个fit才可能用到测试信息。

**English takeaway：** TF uses within-document frequency; IDF uses training-document frequency. The instructor's conceptual TF-IDF formula differs from the transformer's smoothed IDF and final normalization, so state which convention is used.


**来源与掌握要求：** Lecture2b，第89–92个单元，PDF 27–28页。核心必会；难度中；要求读懂权重并区分数学简式与库实现。

<a id="multinomial"></a>

## 18. Naive Bayes Multinomial｜模型里的“词概率”又换了含义

对原始计数向量 $\mathbf{x}$，总词数 $L=\sum_jx_j$ 固定时，多项式模型给出

$$p(\mathbf{x}\mid c,L)=\frac{L!}{\prod_j x_j!}\prod_{j=1}^{V}\pi_{j,c}^{x_j},
\qquad \sum_j\pi_{j,c}=1.$$

把同一类别的文档中的所有词放在一起，$\pi_{j,c}$ 表示从这一类的词分布中抽取一个词时，它是词j的概率。估计时看该词出现次数占全部词次数的比例。这与Bernoulli问“某篇文档有没有词j”不同：同一篇可以包含多个词，因此Bernoulli的各词出现概率不必相加等于1。

比较同一文档的类别时，阶乘项与c无关，于是得分只需

$$\log p(c)+\sum_jx_j\log\pi_{j,c}.$$

若 $T_{j,c}$ 是类别c里词j的总计数，加法平滑为

$$\tilde\pi_{j,c}=\frac{T_{j,c}+\alpha}{\sum_{k=1}^V T_{k,c}+V\alpha}.$$

分母是总词计数加 $V\alpha$，不是文档数加 $2\alpha$。同一个alpha名字在不同模型中作用于不同分布，不能照搬分母。

**教学手算 / Worked example**

中文题：词表仍为 [free, meeting]。两类的总词计数分别是 [6,2] 和 [1,7]，$\alpha=1$，先验相等。新文档计数为 [2,0]，求Spam后验。

English question: For vocabulary [free, meeting], total token counts are [6,2] for Spam and [1,7] for Ham. With alpha=1 and equal priors, find the Spam posterior for count vector [2,0].

答案：两类参数分别 [0.7,0.3]、[0.2,0.8]。该文档的类别相关项为 $0.7^2=0.49$ 与 $0.2^2=0.04$，Spam后验 $49/53\approx0.9245$。重复free增加了证据；未出现的meeting指数为0，没有Bernoulli那样的补概率项。

English answer: The parameters are [0.7,0.3] and [0.2,0.8]. The class-dependent factors are 0.49 and 0.04, so the Spam posterior is 49/53. Repeated occurrences affect the score, unlike binary presence.

**原课核对：TF-IDF与阶乘公式不能混为一谈。** Lecture2b，第93个单元同时写“归一化频率”和整数多项式PMF。严格的这个PMF定义在非负整数计数上；TF-IDF通常是分数权重。sklearn允许非负TF-IDF作为实用输入，仍使用加权log分数，但不能把这些权重逐项解释成整数计数的生成概率。Lecture2b，第94个单元的alpha=0.05是课堂邮件示例设置，不是适用于所有任务的固定答案。[模型实现说明](https://scikit-learn.org/stable/modules/naive_bayes.html)

**English takeaway：** Multinomial NB scores count or nonnegative weighted features using token-level parameters. Literal multinomial probabilities require integer counts; TF-IDF inputs are a practical weighted-feature use of the classifier.


**来源与掌握要求：** Lecture2b，第93–97个单元，PDF 29–30页。核心必会；难度中；要求比较模型与识别计数假设。

<a id="extensions"></a>

## 19. Summary / Other text preprocessing / Other word models｜本讲留下哪些取舍？

生成式分类把“怎样描述各类数据”变成主要建模选择。NB减少了参数数量，训练快、容易扩展到多类；有限数据时常是值得先做的基线。但课件“works with small amount of data”不是任何小样本任务都可靠的保证，分布假设不合适、样本不代表实际环境时仍会失败。预测标签不错，也不意味着后验数值已经校准。

老师最后点到的改进方向各有目的：

| 原英文名称 | 中文理解与例子 | 第一遍掌握边界 |
|---|---|---|
| Stemming | 按规则截取词干，例如 testing、tests → test | 知道会合并变体，也可能产生不自然词干 |
| Lemmatisation | 按语言规则归并词形，例如 went、going → go | 知道可能依赖词性与语言资源 |
| Removing numbers / punctuation | 对数字、标点做处理 | 先判断是否含任务信息；短信金额、链接符号未必该删 |
| N-grams | 用连续n个词的组合保留部分局部语序 | 能解释unigram与bigram；代价是词表扩大 |
| Word vectors | 用实向量表达词在上下文中的统计关系 | 知道向量相似与上下文有关，不把向量运算当必然成立的语义定律 |

这些是原课提供的后续方向。第一遍不需要为每个名字另读一整章模型教程；先能解释为什么当前词袋可能不够。

**English takeaway：** Generative and naive Bayes models offer efficient, interpretable baselines, but their assumptions and representation choices matter. Preprocessing, n-grams and word vectors change which information is retained.


**来源与掌握要求：** Lecture2b，第98–100个单元，PDF 30–31页。常规掌握；难度低；要求比较用途和限制。

<a id="comparison"></a>

## 20. 把整讲放回一张表｜What changes, and what stays the same?

所有模型都在比较“类条件支持×先验”；变的是特征表示和CCD假设。

| 模型 | 输入语义 | 各类学什么 | 主要条件或代价 |
|---|---|---|---|
| 一维 Gaussian Bayes | 一个连续测量 | 均值、方差、先验 | 每类一元高斯 |
| Gaussian NB | 多个连续测量 | 每维均值/方差、先验 | 给定类后独立，对角协方差 |
| 完整 Gaussian Bayes | 连续特征向量 | 均值向量、各类协方差、先验 | 建模相关性，参数与样本需求更高 |
| Bernoulli NB | 每词是否出现 | 每类每词的文档出现率 | 同时考虑出现和未出现 |
| Multinomial NB | 词计数；实现也接受非负权重 | 每类各词所占的概率 | 计数模型与TF-IDF实用输入须区分 |

Poisson NB是 **Tutorial 2** 引入的计数模型，先在本讲掌握“按类估参数—算特征的对数似然—加对数先验—归一化”，再在教程中更换分布；它不属于 Lecture2a/2b 新出现的一页。

<a id="self-check"></a>
## 21. 英文自测与少量卡片｜先解释，再检索

答案是最低合格要点的示例，不要求逐字背诵。

**Q1 中文：** 先验、类条件分布、后验各固定了什么？  
**Q1 English:** What is conditioned on in the prior, class-conditional distribution and posterior?  
**答：** 先验还未给定当前特征；类条件已知类别看特征；后验已知特征看类别。  
**Answer:** The prior is before observing the current features; the class-conditional distribution describes features given a class; the posterior describes classes given the observed features.

**Q2 中文：** 某类训练值为1、2、3。高斯MLE均值、方差是什么？无偏样本方差是否相同？  
**Q2 English:** A class has observations 1, 2 and 3. Find the Gaussian MLE mean and variance, and compare with the unbiased sample variance.  
**答：** 均值2，MLE方差2/3，无偏样本方差1；分母不同。  
**Answer:** The mean is 2, the MLE variance is 2/3, and the unbiased sample variance is 1.

**Q3 中文：** 似然相同、先验分别0.2/0.8，相同错分代价时选谁？  
**Q3 English:** With equal likelihoods, priors 0.2/0.8 and equal error costs, which class is selected?  
**答：** 第二类，后验与先验相同；若共同似然为0，不能这样归一化。  
**Answer:** Select the second class when the common likelihood is positive; the posterior equals the prior. A zero common likelihood makes this normalization undefined.

**Q4 中文：** 为什么给定类后的相关性会使 Gaussian NB 假设不成立？完整高斯是否一定测试更好？  
**Q4 English:** Why does within-class dependence challenge Gaussian NB, and must a full Gaussian perform better on test data?  
**答：** NB将类条件联合分布分解；完整模型允许协方差，但估计更多参数，有限数据时不保证更好。  
**Answer:** NB factorizes the class-conditional joint distribution. Full covariance permits dependence but estimates more parameters, so improvement is not guaranteed.

**Q5 中文：** free出现三次，Bernoulli NB和Multinomial NB怎样对待它？  
**Q5 English:** How do Bernoulli and multinomial NB treat three occurrences of “free”?  
**答：** Bernoulli将其变成一次出现；计数Multinomial使用计数3。  
**Answer:** Bernoulli represents presence as one; count-based multinomial NB uses the count three.

先用这几张卡复习本讲主线：
[先验MLE M052](https://crazyshout.github.io/micro-course/cards.html#CS5489-M052)、
[Bayes决策 M058](https://crazyshout.github.io/micro-course/cards.html#CS5489-M058)、
[Gaussian NB M061](https://crazyshout.github.io/micro-course/cards.html#CS5489-M061)、
[文本平滑 M081](https://crazyshout.github.io/micro-course/cards.html#CS5489-M081)。
这4张先检查主线；其余相关卡可在完成Tutorial练习后分批复习。

## 22. 重难点判断到底依赖什么？

| 证据 | 本讲可用的结论 | 不能推出的结论 |
|---|---|---|
| 当前Lecture2a／Lecture2b的目录、公式、原例与代码 | 本学期确实提供了哪些内容，前后需要什么基础 | 未提供录音时，不能声称老师口头反复强调 |
| 当前Tutorial 2 | 文本表示、NB比较、调参、解释错分、实现另一种CCD是实际训练目标 | 教程出现过不自动等于期末高频 |
| 当前Assignment 1 | 分类流程、评估、复现需要能应用 | 不证明所有高级模型都必须掌握 |
| 历史作业 Home_Assignments_1.pdf：2024历史Home_Assignments_1，Ex2 | 曾有“更换类条件分布并推MLE”的任务，支持练方法迁移 | 不能把旧题中的Laplacian分布当当前新增页 |
| 历史作业 Home_Assignments_1.pdf Ex3–4 | 历史资料涉及共享协方差LDA与条件高斯证明，难度较高 | 不据此把完整证明列为当前Lecture2核心 |
| 历史样题 sample_final_questions.docx：2024/25东莞Sample Questions，2b/3b | 样题涉及NB优缺点和MLE推导，可用来练英文回答 | 样题不是实际试卷，更不是香港本学期的高频统计 |

历史作业 Home_Assignments_1.pdf的封面/首页只有2024日期，教师与校区归属仅由历史资料库上下文判断，未在该文件首页直接确认；历史样题 sample_final_questions.docx封面明确“CITY UNIVERSITY OF HONG KONG (DONGGUAN) / Sample Questions”。两处仓库中的同内容副本按SHA-256去重，不算两年或两份独立证据。详见 source-manifest.json。

历史原件：历史作业 Home_Assignments_1.pdf；历史样题 sample_final_questions.docx。

<a id="coverage"></a>
## 23. 原课覆盖索引｜回到老师哪一页？

主要来源：Lecture2a Notebook / PDF，Lecture2b Notebook / PDF。cell 从文件第一个单元开始计数，包含 Markdown 和代码，不是执行次数 In[n]。PDF 页码从第一页计数。

下表覆盖全部149个Notebook单元，包括标题、设置、重复显示和空白收尾。连续范围中的代码与图片按教学目的合并解释。PDF分页是导出版定位辅助，Notebook cell是主要定位。

| 原位置 | PDF页 | 本讲义位置／处理 |
|---|---|---|
| Lecture2a，第1–3个单元 | 1 | 开头与学习地图；标题、Outline、导入设置 |
| Lecture2a，第4–8个单元 | 1–3 | §1 分类任务、原花图、数据坐标 |
| Lecture2a，第9–12个单元 | 3–4 | §2 生成模型、先验、指示函数 |
| Lecture2a，第13–17个单元 | 4–5 | §3 类别先验MLE与实计数 |
| Lecture2a，第18–25个单元 | 5–7 | §4 直方图、连续密度、正态示意 |
| Lecture2a，第26–31个单元 | 7–9 | §5 均值/方差MLE、拟合图 |
| Lecture2a，第32–40个单元 | 9–11 | §6 后验、Bayes决策、边界定位 |
| Lecture2a，第41–47个单元 | 11–13 | §7 joint / log-joint 等价与数值稳定 |
| Lecture2a，第48–49个单元 | 13 | §7总结；Lecture2a，第49个单元为空代码单元 |
| Lecture2b，第1–5个单元 | 1–2 | §8 Outline、条件独立、运行设置 |
| Lecture2b，第6–13个单元 | 2–4 | §8 数据、50/50划分、样本与网格区别 |
| Lecture2b，第14–24个单元 | 4–7 | §8 参数、二维/三维密度、椭圆和后验绘图函数 |
| Lecture2b，第25–32个单元 | 7–9 | §9 后验、测试、错分点 |
| Lecture2b，第33–38个单元 | 9–10 | §10 协方差、四个矩阵例子与图 |
| Lecture2b，第39–42个单元 | 10–11 | §11 MLE与正则；§10形状解释 |
| Lecture2b，第43–54个单元 | 11–14 | §11完整类实现、标签映射、预测比较 |
| Lecture2b，第55–58个单元 | 14–15 | §12 邮件任务、词袋原图与信息损失 |
| Lecture2b，第59–71个单元 | 15–20 | §13 读取、划分、词表、稀疏矩阵与显示辅助 |
| Lecture2b，第72–79个单元 | 20–25 | §14 Bernoulli拟合、词概率图、错分查看 |
| Lecture2b，第80–84个单元 | 25–26 | §15平滑与测试比较的解释 |
| Lecture2b，第85–88个单元 | 26–27 | §16 高频／区分性词排名、模型对象核对 |
| Lecture2b，第89–92个单元 | 27–28 | §17 TF-IDF与库约定 |
| Lecture2b，第93–97个单元 | 29–30 | §18 Multinomial、词参数、预测与排名 |
| Lecture2b，第98–100个单元 | 30–31 | §19总结、预处理、n-gram与词向量 |

数值和图由本地工具单独重算；原代码保留在原材料中。不同版本库的实际行为需结合随样板保存的环境版本核对。教学手算在正文中标为补充例题。