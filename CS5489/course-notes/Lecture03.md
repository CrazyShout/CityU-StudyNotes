# Lecture 3 · Discriminative Classifiers｜从概率分布走向分类边界

[课程目录](README.md) · [上一讲：Bayes](Lecture02.md) · [Tutorial 3](Tutorial03.ipynb) · [下一讲：回归](Lecture04.md)

植物园仍然要辨认鸢尾花。上一讲先为每种花建立测量值的分布，再用 Bayes 规则判断新花。这一讲换个问题：如果最后只需要判断类别，能不能直接学习“什么测量结果应该分在哪边”？老师按 **线性分类 → Logistic Regression → SVM → Kernel SVM → 特征与模型比较** 展开，本讲义保持这个顺序。

**基础复习（可跳过）**：看不懂点积、距离时先读[长度与投影](../../learning/foundation-notes/MathForML.md#projection)；求梯度、约束和乘子卡住时读[梯度与约束](../../learning/foundation-notes/MathForML.md#optimization)。Python 数组操作回到 [Lecture 1](Lecture01.md#arrays)。

<!-- EXAM:overview:START -->
<div class="exam-overview exam-overview-compact" markdown="1">
<a id="exam-review"></a>
## Exam focus｜这一讲怎样安排复习

本讲的历史题集中在Logistic目标、SVM与核方法，也经常要求根据应用代价或存储限制选择方法。复习时把“写出目标、说明条件、解释结果”连起来。

| 考点 | 复习动作 | 期中：直接／关联 | 期末：直接／关联 | QE记录 | 入口 |
|---|---|---|---|---|---|
| 生成式与判别式 | 说明两类方法到底学什么 | 3套／未见 | 未见／未见 | 未见 | [讲解](#linear) |
| 模型参数计数 | 写明先验与共享方差的约定 | 1套／未见 | 未见／未见 | 未见 | [讲解](#parameter-count) |
| Logistic似然与优化 | 走完一次梯度更新 | 6套／未见 | 未见／未见 | 未见 | [讲解](#logistic) |
| 正则化、MAP与CV | 先说明目标的缩放约定 | 5套／未见 | 未见／未见 | 未见 | [讲解](#regularization) |
| SVM间隔、松弛与对偶 | 掌握间隔条件与软间隔权衡 | 6套／未见 | 1套／未见 | 未见 | [讲解](#svm) |
| 核技巧与合法性 | 会算小Gram矩阵并辨认无效核 | 6套／未见 | 1套／1套 | 未见 | [讲解](#kernels) |
| 求解维度与预测存储 | 按给定维数和支持向量数计算 | 3套／未见 | 未见／未见 | 未见 | [讲解](#model-cost) |
| 不平衡、代价与阈值 | 先明确哪种错误更贵 | 5套／未见 | 未见／未见 | 未见 | [讲解](#cost-threshold) |
| 分类损失曲线 | 检查错分区是否仍被惩罚 | 5套／未见 | 未见／未见 | 未见 | [讲解](#loss-shapes) |

**口径：** 同一考点在同一独立试卷只计一次；题纸、答案和扫描副本不重复计。已辨识6套期中、3套期末；模拟题另列，2021B*保留封面年份冲突。同卷可同时有直接题和关联题，两列不相加。未见不等于不考，QE题段不换算为已确认卷数。

核PCA为期末关联知识，当前尚未展开。下面登记原题涉及的能力，不表示每份历史选择题的所有选项都已成为当前课程要求；具体答案中的简化见讲末注。

<div class="exam-legend" aria-label="考试类别"><span>标记：</span><span class="exam-badge exam-mid">期中</span><span class="exam-badge exam-final">期末</span><span class="exam-badge exam-qe">QE</span><span class="exam-legend-note">颜色区分考试类别；卷数与考查关系直接见标签文字。</span></div>

题号见[讲末索引](#exam-topic-index)，材料身份见[全册附录](ExamIndex.md)。
</div>
<!-- EXAM:overview:END -->

[TOC]

| 主题 | 优先级 | 理解难度与卡点 | 应达到的能力；判断依据 |
|---|---|---|---|
| 线性分数、sigmoid、logistic loss | 核心必会 | 中；标签编码、概率方向 | 手算分数、概率和损失；Lecture3a，第24–52个单元 |
| 正则化、CV、预处理 | 核心必会 | 中；训练/验证边界 | 能设计无泄漏实验；Lecture3a，第65–73个单元、Lecture3c，第7–15个单元、Tutorial 3 |
| margin、hard/soft SVM | 核心必会 | 中至高；距离与函数值 | 解释并计算间隔、slack；Lecture3b，第11–60个单元、SVM手写补充，第1–4页 |
| SVM dual、KKT | 核心必会 | 高；对谁求导、约束符号 | 跟完关键求导并解释乘子；Lecture3b，第37–44个单元、SVM手写补充，第2–4页 |
| 核、特征映射及参数 | 核心必会 | 中至高；隐式内积 | 手算小核矩阵、实现原任务；Lecture3b，第83–123个单元、Tutorial 3 |
| 多分类、编码、不平衡 | 常规掌握 | 中；机制与实现区分 | 选择表示与评估方法；Lecture3a，第74–99个单元、Lecture3c，第16–42个单元 |
| 强对偶的一般证明、核的一般谱理论 | 二读拓展 | 高；数学条件 | 理解适用条件；列为选读是整理者建议 |

优先级依据当前课件和Tutorial任务；历史考试记录另见讲末索引。

<a id="linear"></a>
## 1. Generative versus discriminative｜先弄懂我们换了什么目标
<!-- EXAM:focus-linear:START -->
<div class="exam-focus"><div class="exam-focus-title">考点：生成式与判别式</div><div class="exam-badges" aria-label="历史考查记录"><span class="exam-badge exam-mid">期中直接 · 3 套</span></div></div>
<!-- EXAM:focus-linear:END -->


生成式分类器学 $p(\mathbf x\mid y)$ 和 $p(y)$，再得到后验 $p(y\mid\mathbf x)$。判别式分类器直接学后验或分类分数。两者都使用带标签的训练数据；“判别式”不等于“不需要概率”，SVM 和 Logistic Regression 也不是同一种训练目标。

上一讲从花朵的测量分布计算后验；这次看看在什么条件下，同样的判断可以直接写成一个线性分数。假设两个类别各维条件独立，**所有类别、所有维度共享同一个方差$\sigma^2>0$**，均值分别为$\boldsymbol\mu,\boldsymbol\nu\in\mathbb R^d$，先验为$\pi_1,\pi_2>0$。

这里沿老师的约定，比较**第一类后验除以第二类后验**，记其log为$r(\mathbf x)$。它等于第一类log分数减第二类，与[上一讲的$\Delta$](Lecture02.md#gaussian-nb-boundary)方向相反：对同一模型，$r=-\Delta$。两类打平的位置相同；这里$r>0$选第一类，$r<0$选第二类，假定两类错分代价相同。

由Bayes公式，两类后验都除以同一个$p(\mathbf x)$，取比值后该分母消去。各维高斯的方差又完全相同，log密度中的归一化项也消去。留下的平方项可以沿用上一讲的方法展开：

$$
\begin{aligned}
r(\mathbf x)&=\log\frac{p(y=1\mid\mathbf x)}{p(y=2\mid\mathbf x)}\\
&=\log\frac{p(\mathbf x\mid y=1)}{p(\mathbf x\mid y=2)}
 +\log\frac{\pi_1}{\pi_2}\\
&=\sum_{j=1}^d\frac{(x_j-\nu_j)^2-(x_j-\mu_j)^2}{2\sigma^2}
 +\log\frac{\pi_1}{\pi_2}\\
&=\sum_{j=1}^d\frac{2(\mu_j-\nu_j)x_j+\nu_j^2-\mu_j^2}{2\sigma^2}
 +\log\frac{\pi_1}{\pi_2}\\
&=\sum_{j=1}^d\frac{\mu_j-\nu_j}{\sigma^2}x_j
 +\frac{\|\boldsymbol\nu\|^2-\|\boldsymbol\mu\|^2}{2\sigma^2}
 +\log\frac{\pi_1}{\pi_2}.
\end{aligned}\tag{3.1}
$$

每个$x_j^2$都与另一个同系数的$x_j^2$相减，因此只剩一次项。这里$\|\boldsymbol\mu\|^2=\sum_j\mu_j^2$，就是均值各分量的平方和。将一次项系数和常数分别记成：

$$
w_j=\frac{\mu_j-\nu_j}{\sigma^2},\qquad
b=\frac{\|\boldsymbol\nu\|^2-\|\boldsymbol\mu\|^2}{2\sigma^2}
 +\log\frac{\pi_1}{\pi_2}.
\tag{3.1a}
$$

这样$r(\mathbf x)=\mathbf w^T\mathbf x+b$。边界由这个分数等于0给出；接下来可以直接从数据学习$\mathbf w,b$，不用先估计两类的均值和方差。

[Lecture 2的逐特征推导](Lecture02.md#gaussian-nb-boundary)还允许不同特征使用不同的共享方差，同样能消去二次项；逐类完整协方差模型一般没有这个保证。

**English takeaway (整理表达):** Shared variances cancel the squared-input terms, giving $r(\mathbf x)=\nobreak\mathbf w^T\mathbf x+b$. This lecture reverses Lecture 2’s class order: under equal error costs, $r>0$ selects class 1.

来源：Lecture3a，第8–12、21–23个单元；比较方向与跨讲衔接为补充解释。

## 2. Linear classifier and separating hyperplane｜一张有方向的分界线

从 Lecture3a，第24个单元 开始，理论标签改成 $y\in\{-1,+1\}$，不再是前面的 1、2。输入 $\mathbf x\in\mathbb R^d$、权重 $\mathbf w\in\mathbb R^d$，偏置 $b$ 是一个数。$f>0$ 判 +1，$f<0$ 判 −1；$f=0$ 要约定平局处理。分数本身不是概率。

老师原例 $\mathbf w=(2,1)^T,b=0$：看见 $(2,-1)$ 就算 $2\times2-1=3$，判 +1；看见 $(-2,1)$ 得 −3，判 −1。边界 $2x_1+x_2=0$ 垂直于 $\mathbf w$。二维是线，三维是平面，$d$ 维叫超平面（hyperplane），维度为 $d-1$，要求 $\mathbf w\ne0$。

<img src="assets/lecture03-linear-sigmoid.png" alt="Linear scores and sigmoid probabilities" />

图左按原例重绘分类边界，右边显示同一分数经sigmoid转换后的概率。左图先判断落在线的哪侧，再沿右图查这个分数对应的模型概率。

**自测 / Check:** 若 $\mathbf w=(2,1)^T,b=-1,\mathbf x=(1,2)^T$，分数和预测是什么？ / For w=(2,1)ᵀ, b=−1 and x=(1,2)ᵀ, find the linear score and predicted class.

<details markdown="1"><summary>答案 / Answer</summary>

$f=2+2-1=3>0$，预测 +1。 / The score is 3; predict +1. 偏置移动边界，不增加一个观测维度。

</details>

<a id="logistic"></a>
## 3. Logistic regression｜把分数翻译成概率
<!-- EXAM:focus-logistic:START -->
<div class="exam-focus"><div class="exam-focus-title">考点：Logistic似然与优化</div><div class="exam-badges" aria-label="历史考查记录"><span class="exam-badge exam-mid">期中直接 · 6 套</span></div></div>
<!-- EXAM:focus-logistic:END -->


“分数为 3”不直接告诉我们有多确定。Logistic Regression 用 sigmoid：

$$
\begin{gathered}\sigma(z)=\frac1{1+e^{-z}},\\[3pt]
p(y=+1\mid\mathbf x)=\sigma(f(\mathbf x)),\\
p(y=-1\mid\mathbf x)=1-\sigma(f(\mathbf x)).\end{gathered}\tag{3.2}
$$

分数 0 对应 0.5；分数 2 对应约 0.8808；−2 对应约 0.1192。概率相加为 1。名称里虽然有 regression，这里做的是分类。Lecture3a，第36个单元 的一维原例 $f(x)=2x-4$，所以边界在 $x=2$，不是在 $x=0$。

现在反过来：给出训练数据，怎样找权重？每个样本希望模型给它的**真实类别**较高概率。利用 $1-\sigma(z)=\sigma(-z)$，两种标签合并为 $p(y\mid\mathbf x)=\sigma(yf(\mathbf x))$。这个写法只适用于 $y=\pm1$；不能直接把 0/1 标签代进去。

令 $z_i=y_i f(\mathbf x_i)$。它为正说明分对，负说明分错，零在边界。对N个独立样本，条件似然相乘，取对数后相加；最大化对数似然等价于最小化负对数：

$$
E(\mathbf w,b)=\sum_{i=1}^N\ell(z_i),\qquad \ell(z)=\log(1+e^{-z}).\tag{3.3}
$$

若真实标签 −1，分数却为 2，那么 $z=-2$、损失约 2.1269；同样标签配分数 −2，损失约 0.1269。损失是“对真实答案有多不买账”，不是错误样本的简单计数。即使分对但信心不足，损失仍不为零。

**English:** Logistic regression minimizes the negative conditional log-likelihood. The signed score $yf(x)$ distinguishes correct from incorrect predictions.

<a id="regularization"></a>
## 4. Regularization and optimization｜限制大权重，减少过拟合
<!-- EXAM:focus-regularization:START -->
<div class="exam-focus"><div class="exam-focus-title">考点：正则化、MAP与CV</div><div class="exam-badges" aria-label="历史考查记录"><span class="exam-badge exam-mid">期中直接 · 5 套</span></div></div>
<!-- EXAM:focus-regularization:END -->


模型可能靠很大的权重把训练点分得极其自信，但新数据稍有变化就出错。Lecture3a，第49–51个单元 给权重零均值高斯先验，协方差 $(C/2)I$，得到课堂目标：

$$
E=\frac1C\|\mathbf w\|^2+\sum_i\log(1+e^{-y_i(\mathbf w^T\mathbf x_i+b)}),\qquad C>0.\tag{3.4}
$$

第一项惩罚大权重，第二项拟合数据。**小 $C$：更强正则；大 $C$：更弱正则。** 为什么高斯先验会产生平方惩罚？前一讲已经学过高斯的指数项。均值为零、协方差为$(C/2)I$时，先验中与w有关的部分是$\exp(-\|w\|^2/C)$；取负log便得到$\|w\|^2/C$，其余是不随w变化的常数。最大后验估计（maximum a posteriori，MAP）同时考虑数据似然与这份先验，于是得到“数据损失＋平方惩罚”。偏置在这份公式里未被惩罚。库中的 $1/2$、求和/平均及 solver 约定可能不同，不应从同一个数值 C 推断不同软件必然输出同一模型。

老师说用迭代优化（Lecture3a，第52个单元）。补足最关键一步：对一个样本，

$$
\frac{d\ell}{dz}=-\frac1{1+e^z}=-\sigma(-z),\qquad
\nabla_{\mathbf w}\ell=-y\sigma(-yf)\mathbf x.\tag{3.5}
$$

第一式来自先求 $\log u$ 的导数再乘 $u=1+e^{-z}$ 的导数；第二式再乘 $z=y(\mathbf w^T\mathbf x+b)$ 对权重的导数。加上正则得到

$$
\begin{aligned}\nabla_{\mathbf w}E&=\frac2C\mathbf w-\sum_i y_i\sigma(-y_if_i)\mathbf x_i,\\[3pt]
\frac{\partial E}{\partial b}&=-\sum_i y_i\sigma(-y_if_i).\end{aligned}\tag{3.6}
$$

梯度下降把参数更新为 $\mathbf w\leftarrow\mathbf w-\eta\nabla E$，$\eta>0$ 是学习率。减号表示向局部下降方向走；步子过大仍会跨过谷底。

**补一步题 / Fill a step:** 单个样本 $x=2,y=+1,w=b=0$，无正则，$\eta=0.1$。一次同时更新得到什么？ / For one sample x=2, y=+1, initial w=b=0, no regularization and learning rate 0.1, compute one simultaneous update.

<details markdown="1"><summary>答案 / Answer</summary>

$f=0,\sigma(-yf)=0.5$，$\partial E/\partial w=-1$、$\partial E/\partial b=-0.5$。新 $w=0.1,b=0.05$，新分数 0.25，正确类别概率增加到约 0.5622。 / The updated parameters are w=0.1, b=0.05; the positive-class probability becomes about 0.5622.

</details>

### 换成L1惩罚，分类器会怎样变？

历史题还会把式（3.4）的平方惩罚换成绝对值惩罚。数据损失仍是logistic loss，改的是权重的代价：

$$
E=\sum_i\log(1+e^{-y_i f_i})+\lambda\sum_j|w_j|,\qquad\lambda>0.
\tag{3.6a}
$$

L1惩罚在零点有尖角，可以把某些权重推到恰好为0；为什么会这样，见[下一讲的LASSO手算](Lecture04.md#lasso)。如果二维模型学到$w=(0,2)^T,b=-4$，分数就是$2x_2-4$：$x_1$完全不参与判断，边界为$x_2=2$。L1改变了用到哪些特征，并没有让线性分数自动变成非线性函数。

**判断 / Check：** 改成$w=(3,0)^T,b=-6$，边界在哪里？只知道用了L1，能否断言必有一个零权重？ / For w=(3,0)ᵀ and b=−6, locate the boundary. Does using L1 alone guarantee a zero weight?

**答 / Answer：** 边界为$x_1=2$；不能保证，是否出现零系数取决于数据与惩罚强度。 / The boundary is x₁=2. L1 encourages sparsity but does not guarantee a zero coefficient for every dataset and penalty strength.

来源：2020B期中Q12的L1分类目标；数值与变式为教学补充。

<a id="finite-logistic-solution"></a>
### 凸目标不等于一定有唯一的有限解

判断优化结果时，需要区分目标是否凸、是否存在最优解，以及解是否唯一。最简单的反例只有一个点$x=1,y=+1$，固定$b=0$且不加正则：损失是$\log(1+e^{-w})$。w越大，损失越接近0，但任何有限w都不能使它恰好等于0。因此目标虽然凸，却没有有限的最小值点。线性可分数据的无正则logistic MLE也可能有这个问题。

正则化可以限制权重继续变大；解的存在性与唯一性还取决于惩罚了哪些参数、数据和秩条件，不能只凭“logistic regression”这个名称判断。

**独立判断 / Check：** 上述单点例中，w从2改成4，损失怎样变？是否已达到零？ / In the single-point example above, compare the losses at w=2 and w=4. Is either loss zero?

**答 / Answer：** 约0.1269降至0.01815，都大于0。 / It decreases from about 0.1269 to 0.01815; both are positive. 这是教学反例，用于澄清历史题中省略的存在性条件。

## 5. Iris example and cross-validation｜让验证集帮我们选 C

课堂用 iris2.csv 的两项测量，固定 `random_state=4487`，各一半训练与测试；`C=100` 学到一条边界。Lecture3a，第59个单元保存了该设置的系数。复现时还需对照求解器与版本；已有复算结果见文末记录。

课堂画几个 C 的测试表现属于课堂探索。正式选参应该在训练集内部做 K-fold cross-validation（CV）：将训练数据分 K 份，每次留一份验证，其他份训练；每个 C 得 K 个验证分数，取平均；选好后用**整个原训练集**重新拟合，最后才评估保留测试集。Lecture3a，第69个单元 的“all data”在这里应理解为所有训练数据，不包括用于最终评价的测试集。

如果还要标准化，`StandardScaler` 必须放在 `Pipeline` 里面，让每一折只用本折训练部分拟合均值与标准差。提前用整个训练集缩放再 CV，会把验证折的信息带进去。固定减 0.5 不依赖数据估计，性质不同。

```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000))
search = GridSearchCV(model, {'logisticregression__C':[0.1,1,10]}, cv=5)
search.fit(trainX, trainY)
# Only now evaluate search on the untouched testX, testY.
```

当前接口使用 `model_selection`；原文提到的 `cross_validation` 是旧模块名。`mean_test_score` 在 GridSearchCV 中指每折的验证分数，不是你保留的外部测试集成绩。

来源：Lecture3a，第54–73个单元；Pipeline与GridSearchCV示例为补充。


<a id="6-multiclass-classification-if"></a>
## 6. Multiclass classification｜从二类扩展到多类

One-vs-rest（OvR）为每一类训练“它 versus 其他类”分类器，然后比较各类分数/概率。三类要三个分类器。它们分别训练，原始 sigmoid 输出不必相加为 1；实现可进一步归一化。

Softmax 则一起训练 K 组权重，$f_c(\mathbf x)=\mathbf w_c^T\mathbf x$（偏置可加入或吸收到常数特征）：

$$
p_c=\frac{e^{f_c}}{\sum_{j=1}^K e^{f_j}},\qquad \ell=-\sum_{c=1}^K y_c\log p_c.\tag{3.7}
$$

$\mathbf y$ 是 one-hot 真实标签，仅真实类别的分量为 1，所以损失就是该类概率的负对数。分数 $(0,\log2,\log3)$ 对应概率 $(1/6,2/6,3/6)$；若真实类别为第 2 类，损失 $\log3\approx1.0986$。数值实现先减最大分数再指数，概率不变且更稳定。

原 `multi_class='ovr'` / `'multinomial'` 是旧接口写法。需要明确 OvR 时用 `OneVsRestClassifier(LogisticRegression(...))`；不要靠新版默认值猜老师在示范哪一种模型。


来源：Lecture3a，第74–85个单元；第86–99个单元。

<a id="svm"></a>

## 7. Maximum margin｜不仅分开，还想留出余地
<!-- EXAM:focus-svm:START -->
<div class="exam-focus"><div class="exam-focus-title">考点：SVM间隔、松弛与对偶</div><div class="exam-badges" aria-label="历史考查记录"><span class="exam-badge exam-mid">期中直接 · 6 套</span><span class="exam-badge exam-final">期末直接 · 1 套</span></div></div>
<!-- EXAM:focus-svm:END -->


从两团可分数据开始。有很多条线能分对训练数据，SVM 优先选离最近点也尽量远的线。这就像在两排桌子中间留通道：只要没碰桌子不代表通道已经够宽。

点到超平面距离为 $|\mathbf w^T\mathbf x+b|/\|\mathbf w\|$。分母不能省：同时把 $\mathbf w,b$ 乘 10，分界线没动，分数放大 10 倍，距离不能跟着放大。

线性可分、标签正确侧的前提下，选择归一化使最近点 $y_if_i=1$。一侧 margin 为 $1/\|\mathbf w\|$，两条支持平面间的**总宽度**为 $2/\|\mathbf w\|$。于是 hard-margin SVM：

$$
\min_{\mathbf w,b}\frac12\|\mathbf w\|^2\quad\text{s.t. } y_i(\mathbf w^T\mathbf x_i+b)\ge1\quad\forall i.\tag{3.8}
$$

目标让间隔大，约束保证所有点都在正确侧且不侵入间隔。单写 $|f_i|\ge1$ 不够，它也容许把标签全部分反；SVM手写补充，第1页 中绝对值中间式必须连着“正确分类”的前提读。

**完整小算例（补充）**：一维两点 $x_1=-1,y_1=-1$，$x_2=1,y_2=1$。约束为 $w-b\ge1$ 和 $w+b\ge1$，相加得 $w\ge1$。最小 $w^2/2$ 在 $w=1,b=0$，两点都是支持向量，一侧距离 1，总宽度 2。


来源：Lecture3b，第4–26个单元。

<a id="dual"></a>

## 8. Lagrangian and duality｜用样本乘子求解最大间隔

上一节直接求出了一条最大间隔分界线。接下来把每个样本与边界的关系写进求解过程：给第i条约束配一个非负数 $\alpha_i$，称为拉格朗日乘子（Lagrange multiplier）。最终哪些乘子非零，就能看出哪些样本直接参与了边界的表示。

先固定一种符号约定：把要求写成 $g_i\ge0$，拉格朗日函数写作 $L=f-\sum_i\alpha_i g_i$。当约束满足时，减去的是非负数，因此L不会超过原目标f。这一点会让我们得到原问题最优值的下界。若改写为 $h_i=-g_i\le0$，同一个式子便成为 $L=f+\sum_i\alpha_i h_i$；正负号来自约束的写法。

对 hard SVM，$g_i=y_i(\mathbf w^T\mathbf x_i+b)-1$：

$$
L(\mathbf w,b,\boldsymbol\alpha)=\frac12\mathbf w^T\mathbf w-\sum_i\alpha_i[y_i(\mathbf w^T\mathbf x_i+b)-1].\tag{3.9}
$$

先固定 $\alpha$，对原变量 $\mathbf w,b$ 取最小值。展开与求导：

$$
\begin{aligned}L&=\frac12\mathbf w^T\mathbf w-\mathbf w^T\sum_i\alpha_iy_i\mathbf x_i\\
&\quad-b\sum_i\alpha_i y_i+\sum_i\alpha_i.\end{aligned}\tag{3.10}
$$

$$
\begin{gathered}\nabla_{\mathbf w}L=\mathbf w-\sum_i\alpha_iy_i\mathbf x_i=0,\\[3pt]
\frac{\partial L}{\partial b}=-\sum_i\alpha_i y_i=0.\end{gathered}\tag{3.11}
$$

所以 $\mathbf w=\sum_i\alpha_i y_i\mathbf x_i$ 且 $\sum_i\alpha_i y_i=0$。后一条保证关于$b$的项为0；若它不成立，固定这些乘子后，总能沿一个方向改变$b$，让$L$降到负无穷。

下面把求出的权重代回，看看只含乘子的目标怎样出现。为少写一长串求和，暂记$\mathbf v=\sum_i\alpha_i y_i\mathbf x_i$，所以使$L$最小的权重就是$\mathbf w=\mathbf v$。式（3.10）的四项依次变为：

| 原来的一项 | 代回之后 | 原因 |
|---|---|---|
| $\tfrac12\mathbf w^T\mathbf w$ | $\tfrac12\mathbf v^T\mathbf v$ | 用$\mathbf v$替换权重 |
| $-\mathbf w^T\sum_i\alpha_i y_i\mathbf x_i$ | $-\mathbf v^T\mathbf v$ | 内积两边都等于$\mathbf v$ |
| $-b\sum_i\alpha_i y_i$ | $0$ | 乘子满足刚得到的等式约束 |
| $\sum_i\alpha_i$ | $\sum_i\alpha_i$ | 不含$\mathbf w,b$，保持原样 |

于是，对固定乘子取到的最小值为：

$$
\begin{aligned}
q(\boldsymbol\alpha)&=\min_{\mathbf w,b}L(\mathbf w,b,\boldsymbol\alpha)\\
&=\frac12\mathbf v^T\mathbf v-\mathbf v^T\mathbf v+\sum_i\alpha_i\\
&=\sum_i\alpha_i-\frac12\mathbf v^T\mathbf v.
\end{aligned}\tag{3.11a}
$$

负的$1/2$来自$1/2-1$。接下来展开$\mathbf v$的内积：左边求和选一个样本$i$，右边求和选一个样本$j$，每一对都要相乘，因此出现双重求和：

$$
\begin{aligned}
\mathbf v^T\mathbf v
&=\left(\sum_{i=1}^N\alpha_i y_i\mathbf x_i\right)^T
  \left(\sum_{j=1}^N\alpha_j y_j\mathbf x_j\right)\\
&=\sum_{i=1}^N\sum_{j=1}^N
  \alpha_i\alpha_j y_i y_j\mathbf x_i^T\mathbf x_j.
\end{aligned}\tag{3.11b}
$$

非负乘子给出的$q$是原最小值的下界；现在选择乘子，让这个下界尽可能大，得到对偶问题：

$$
\begin{gathered}\max_{\boldsymbol\alpha}\sum_i\alpha_i-\frac12\sum_{i,j}\alpha_i\alpha_jy_iy_j\mathbf x_i^T\mathbf x_j,\\
\sum_i\alpha_iy_i=0,\qquad\alpha_i\ge0.\end{gathered}\tag{3.12}
$$

原问题求$d$个权重和偏置$b$；对偶问题为每个训练样本求一个乘子$\alpha_i$，再用这些乘子恢复分类边界。

沿用前面的一维两点$(x_1,y_1)=(-1,-1)$、$(x_2,y_2)=(1,+1)$。等式约束是$-\alpha_1+\alpha_2=0$，因此记$\alpha_1=\alpha_2=a\ge0$。样本组合为$v=a(-1)(-1)+a(1)(1)=2a$，于是$q(a)=2a-\tfrac12(2a)^2=2a-2a^2$。令导数$2-4a=0$，得到$a=1/2$；二阶导数为$-4$，确为最大值。

恢复$w=2a=1$，由任一支持点得到$b=0$。两条约束都取等号；原目标$w^2/2=1/2$，对偶目标$2a-2a^2=1/2$，也相互吻合。

**English takeaway:** Substitute the minimizing weights into each term of the Lagrangian. The two weight terms combine as $\tfrac12\|v\|^2-\|v\|^2=-\tfrac12\|v\|^2$; expanding the squared norm produces a sum over all pairs of training samples. The dual maximizes a lower bound on the primal minimum.

来源：Lecture3b，第37–44个单元；逐项代回与两点计算为教学补充。

刚才的小例中，对偶问题与原问题得到相同答案。这需要成立条件支持。

<details markdown="1"><summary>二读：为什么这道SVM问题能通过对偶求解？</summary>

固定任意非负乘子时，对偶函数给出原最小值的一个下界，称为弱对偶（weak duality）；最大化这个下界，就是寻找尽可能紧的下界。当最好的下界恰好等于原最小值时，称为强对偶（strong duality）。

这里的目标是凸函数，约束是线性的。对于线性可分的hard-margin SVM，可以把一组正确分离的权重与偏置放大，使所有 $y_if_i>1$，即每条不等式都留有余量。这满足本题所需的严格可行条件。Soft-margin SVM也可以构造严格可行点。因此本讲可用对偶求解；一般凸优化的完整条件见进一步的优化课程。

</details>

## 9. KKT and support vectors｜乘子告诉我们哪条约束在起作用

回看两类样本：有些点远离分界线，约束已经留足余量；有些点恰好压在间隔边缘。我们希望区分这两种情况。Karush–Kuhn–Tucker（KKT）条件把它们与乘子联系起来：

1. 分界线满足原约束：$y_if_i\ge1$。
2. 每个乘子 $\alpha_i\ge0$。
3. 对权重和偏置求导为0，得到上一节的两条等式。
4. **互补松弛（complementary slackness）：** $\alpha_i(y_if_i-1)=0$。

最后一条最值得单独看。$y_if_i-1$是这条约束剩余的量：大于0表示点在间隔外，为0表示点恰好在间隔边缘。

若一个点满足 $y_if_i=2$，剩余量为1，乘积要为0便只能有 $\alpha_i=0$。反过来，若 $\alpha_i>0$，剩余量必须为0，即 $y_if_i=1$。

这两条推理不能任意倒过来：当剩余量为0时，乘积已经是0，乘子也可以为0。因而“点在间隔边缘”并不保证它有非零乘子；这种情况会在退化数据中出现。原课和手写补充中的简略箭头应按上述方向理解。

预测可写成 $\operatorname{sign}(\sum_i\alpha_i y_i\mathbf x_i^T\mathbf x_*+b)$，零乘子的点没有直接贡献。用一个合适的边界支持向量恢复 $b=y_i-\mathbf w^T\mathbf x_i$，数值程序常对多个合适点综合处理。

**变式 / Transfer:** 把两点移到 $x=\pm2$，标签仍为两侧 −1/+1。求 w、b、一侧 margin 和两个乘子。 / Use two one-dimensional samples (x,y)=(-2,-1) and (2,+1). Find the hard-margin w, b, one-sided margin and both multipliers.

<details markdown="1"><summary>答案 / Answer</summary>

等式约束仍令两个乘子均为$a$；此时$w=a(-1)(-2)+a(1)(2)=4a$。对偶目标为$q(a)=2a-\tfrac12(4a)^2=2a-8a^2$，求导得$a=1/8$。所以$w=1/2,b=0$，一侧margin为2；两点都满足$y_if_i=1$，原目标和对偶目标均为$1/8$。 / The equality constraint gives equal multipliers a. Then w=4a and q(a)=2a−8a², maximized at a=1/8. Thus w=0.5, b=0 and the one-sided margin is 2. Both constraints are tight; the primal and dual objectives equal 1/8.

</details>

## 10. Soft-margin SVM｜允许有代价的违规

有重叠/噪声时，强求所有点正确且留出间隔可能无解。为每点引入无量纲 slack $\xi_i\ge0$：

$$
\begin{gathered}\min_{\mathbf w,b,\boldsymbol\xi}\frac12\|\mathbf w\|^2+C\sum_i\xi_i,\\
y_if_i\ge1-\xi_i,\quad\xi_i\ge0,\quad C>0.\end{gathered}\tag{3.13}
$$

在最优解，对给定分数取最小允许 slack：$\xi_i=\max(0,1-y_if_i)$，即 hinge loss。$y_if_i=1.4$ 时 slack=0；0.4 时 slack=0.6，**仍分类正确**；−0.2 时 slack=1.2，才是错分。slack是分数上的缺口；当$\|w\|>0$时，换成几何长度还要除以$\|w\|$。

消去 slack 后为 $\frac12\|w\|^2+C\sum_i\max(0,1-y_if_i)$。整体除 C 得正则系数 $1/(2C)$。Lecture3b，第58个单元 写成 $1/C$ 时相当于重新定义了 C，不能在数值比较时无声跳过因子 2。

对 $\xi_i\ge0$ 引入另一个乘子 $\gamma_i$，$\partial L/\partial\xi_i=C-\alpha_i-\gamma_i=0$，故 $0\le\alpha_i\le C$。对偶目标形式不变，增加上界。还要同时满足两条互补松弛条件：

$$
\alpha_i(y_if_i-1+\xi_i)=0,\qquad (C-\alpha_i)\xi_i=0.
\tag{3.13a}
$$

第二式来自$\gamma_i\xi_i=0$和$\gamma_i=C-\alpha_i$。如果$\alpha_i<C$，它迫使$\xi_i=0$；如果还满足$\alpha_i>0$，第一式再迫使$y_if_i=1$。如果$\alpha_i=C$，第一式给出$y_if_i=1-\xi_i\le1$。这就得到下面三种情形：

| 最优乘子情形 | 可以可靠推出什么 |
|---|---|
| $\alpha_i=0$ | slack=0，$y_if_i\ge1$；不保证严格大于 |
| $0<\alpha_i<C$ | slack=0，$y_if_i=1$；适合恢复 b |
| $\alpha_i=C$ | $y_if_i\le1$；可以在边界、间隔内或错分 |

大 C 让违规更贵，小 C 更愿意牺牲部分训练拟合。即使用RBF核，把C增大也不能解决相同输入却贴着不同标签的冲突：同一个输入只能得到同一份预测。大C也不保证新数据表现更好。原`C=inf`用于示意硬间隔极限，程序接口要求有限C。对线性可分数据，**足够大的有限C可以得到与硬间隔相同的最优权重**：只要上界$\alpha_i\le C$没有排除硬间隔的一组最优乘子即可。前面$x=\pm1$、标签为−1／+1的两点例子中，硬间隔乘子均为$1/2$；当$C\ge1/2$时，$w=1,b=0$也就是软间隔的最优解。 / For linearly separable data, a finite C that admits a hard-margin dual optimum can recover the same optimal weights. In the two-point example x=±1 with labels −1/+1, both hard-margin multipliers are 1/2, so C≥1/2 gives w=1 and b=0.

来源：SVM手写补充，第3页。


<a id="kernels"></a>
## 11. Multiclass SVM and kernel trick｜直线不够，就改变表示
<!-- EXAM:focus-kernels:START -->
<div class="exam-focus"><div class="exam-focus-title">考点：核技巧与合法性</div><div class="exam-badges" aria-label="历史考查记录"><span class="exam-badge exam-mid">期中直接 · 6 套</span><span class="exam-badge exam-final">期末直接 · 1 套</span><span class="exam-badge exam-final">期末关联 · 1 套</span></div></div>
<!-- EXAM:focus-kernels:END -->


课堂将多类SVM用于Iris，并通过交叉验证比较模型。原 `SVC` 多类内部为 one-vs-one，K 类训练 $K(K-1)/2$ 个二分类器，再投票。输出分数呈 OvR 形状不意味着内部改成了 OvR 训练；需要 OvR 模型时显式使用包装器，其网格参数名为 `estimator__C`。

当两类数据呈XOR、中心与两侧或双月形分布时，直线可能不够用。XOR 的 $(1,1),(-1,-1)$ 一组，$(1,-1),(-1,1)$ 另一组，原平面没有一条直线能分开；补一个 $x_1x_2$ 特征，前组 +1、后组 −1，就能分。这个特征捕捉了两项输入是否同号。换特征应有这样的具体理由；来源：Lecture3b，第83–88个单元。

对偶里只用内积，所以可用 $k(\mathbf x,\mathbf x')=\Phi(\mathbf x)^T\Phi(\mathbf x')$ 直接算映射后的内积，省去显式构造巨大的 $\Phi$。这是 kernel trick。

核也可以接收文本等对象，不要求输入本来就是数值向量。例如用字符串s的词计数向量$\Phi(s)$定义$k(s,t)=\Phi(s)^T\Phi(t)$：输入两篇文本，输出一个内积。换成其他文本或图结构的相似度时，仍须满足下一节的合法核条件。来源：Lecture3c，第43个单元。

老师二次多项式原例采用重复交叉项：$\Phi(x_1,x_2)=(x_1^2,x_1x_2,x_2x_1,x_2^2)$，于是内积等于 $(\mathbf x^T\mathbf x')^2$。如果只保留一个交叉项，就要写 $\sqrt2x_1x_2$ 才等价。取 x=(1,2)、x′=(3,4)，核为 $11^2=121$；映射内积为 $1\times9+2\times12+2\times12+4\times16=121$。

核 SVM 用 $k(x_i,x_j)$ 替代内积；软间隔仍须保留 $0\le\alpha_i\le C$。非线性是在原输入空间说的，映射空间里的分类器仍然线性。

来源：Lecture3b，第61–100个单元。


<a id="model-cost"></a>
### 原始问题、对偶问题与预测存储
<!-- EXAM:focus-model-cost:START -->
<div class="exam-focus"><div class="exam-focus-title">考点：求解维度与预测存储</div><div class="exam-badges" aria-label="历史考查记录"><span class="exam-badge exam-mid">期中直接 · 3 套</span></div></div>
<!-- EXAM:focus-model-cost:END -->


原始线性SVM主要学习d个特征权重与一个偏置，对偶则给N个训练样本各一个乘子。d是特征维数，N是训练样本数。例如d=100000、N=2000时，对偶未知数较少；但它通常还需要处理N×N核矩阵，求解速度也取决于算法、稀疏性和数据。只比d与N，不能保证哪种实现一定更快。

训练结束后，线性SVM可把支持向量合成为一个w，只存d+1个数。非线性核SVM通常要保存$n_{SV}$个支持向量、每个向量的一个系数$\beta_i=\alpha_i y_i$以及偏置。若忽略核超参数及程序开销，需存$n_{SV}(d+1)+1$个数。d=100、$n_{SV}=20$时分别为101与2021。比较存储量应看实际支持向量数；改变C可能改变它，但没有普遍的单调增减保证。

**变式 / Transfer：** d=50，核模型有10个支持向量。按相同约定，线性与核模型分别保存多少个数？ / For d=50 and 10 kernel support vectors, count stored numbers under the same convention.

**答 / Answer：** 线性51；核模型$10\times51+1=511$。 / 51 for the linear model and 511 for the kernel model.

教学补充：对应历史题中的高维求解与设备存储比较。

## 12. RBF and custom kernels｜相似度也有尺度

RBF 核 $k(x,x')=\exp(-\gamma\|x-x'\|^2)$，$\gamma>0$。小 gamma 的相似度随距离下降较慢；大 gamma 更局部，可形成复杂边界，但实际效果还取决于 C 和数据。gamma 的单位要与平方距离相抵；改变特征尺度等于改变距离含义。

**完整小例（教学补充）：** 两个无量纲训练点为0和1，取$\gamma=\ln2$。自己与自己的距离为0，所以对角元素都是1；两点距离为1，非对角元素为$e^{-\ln2}=1/2$：

$$
K=\begin{pmatrix}1&1/2\\1/2&1\end{pmatrix}.\tag{3.14}
$$

K的行列对应训练点，不是输入特征。每格告诉我们这两个点在核定义下有多相似，行和不必为1。新点0.5分别与两个训练点比较，会得到两个相同值$e^{-(\ln2)/4}\approx0.8409$；这两个数正是预测所需的测试到训练核向量。

**变式 / Transfer：** 仍用0和1，把gamma改为ln4，核矩阵是什么？ / For training points 0 and 1, change gamma to ln4 and compute the RBF Gram matrix.

**答 / Answer：** 对角为1，非对角为1/4；更大的gamma使距离1的两点相似度更低。 / K=[[1,0.25],[0.25,1]]; the larger gamma lowers similarity at distance one.

课堂用20×20组参数、5折交叉验证比较RBF模型，共2000次候选拟合，再对选定方案重拟合。参数比较使用训练内部的验证分数。

**核的成立条件：** 一种相似度若要作为这里的实值核，必须对称，且由任意有限样本集合组成的核矩阵K都为半正定，即 $z^TKz\ge0$ 对所有实向量z成立。它保证K能表示某个特征空间里的内积。只检查手头的一张矩阵，可以发现当前实现错误，但不能证明这个函数对所有输入都成立。

来源：Lecture3b，第114个单元为参数搜索，第118个单元为核条件；其中positive definite应读作positive semidefinite。

矩阵中的数字全为正，还不足以保证它是合法的核矩阵。例如$K=\left(\begin{smallmatrix}1&2\\2&1\end{smallmatrix}\right)$，取$z=(1,-1)^T$，得到$z^TKz=-2$，违反半正定条件。半正定检查的是所有方向上的二次型，不是每一格的正负。

**判断 / Check：** 将上面的非对角元素从2改成0.5，得到的二点矩阵是否半正定？ / Replace both off-diagonal entries by 0.5. Is this two-point matrix positive semidefinite?

**答 / Answer：** 是，其特征值为1.5与0.5；也可直接验证$z^TKz=z_1^2+z_1z_2+z_2^2\ge0$。这只验证这一张矩阵。 / Yes: its eigenvalues are 1.5 and 0.5. This verifies this matrix, not a kernel function on every possible input.

历史题还用“构造特征”验证核：非零向量的余弦核就是归一化特征$x/\|x\|$的内积，必须先排除零向量。更一般的积分形式$k(x,x')=\int p(x\mid u)p(x'\mid u)p(u)\,du$，在相关积分有限时也满足半正定：任意系数的二次型可写成$\int[\sum_i a_i p(x_i\mid u)]^2p(u)\,du\ge0$。这里u是积分变量、$p(u)\ge0$是密度；这段是核条件的选读应用。

课堂的自定义核示例实际用 **Euclidean** 距离 $\exp(-\alpha\|x-x'\|_2)$；Tutorial3 明确改为 **L1** 距离 $\exp(-\alpha\sum_j|x_j-x'_j|)$。两者不能因为都叫 Laplacian 就混用。函数输入为 $(N_1,d),(N_2,d)$，输出必须为 $(N_1,N_2)$；预测时比较的是测试与训练，不是测试与测试。

**English:** A kernel represents an inner product in a feature space. Tune kernel parameters using training-only validation, and state the exact distance convention.


来源：Lecture3b，第119–123个单元。

<a id="preprocessing"></a>

## 13. Features, scaling and imbalance｜同一模型也会被表示方式影响

先看特征尺度。标准化 $\tilde x_j=(x_j-m_j)/s_j$，每个特征分别用训练均值与标准差；常数特征需要实现中的特殊处理，不能除零。Min-max 为 $2(x-\min)/(\max-\min)-1$，新样本超出训练范围时可以落到 [−1,1] 之外。这不是程序必然出错。

接着看特征的表示方式。把 cat/dog/horse 编成 0/1/2 会强加虚假的次序和距离，one-hot 避免这个问题，但不自动表达动物相似性。原 Lecture3c，第17个单元 的 cat×horse=2 是算术笔误，0×2=0；真正的问题是数字的内积没有所需语义。Binning 将连续值分箱再 one-hot，会丢掉箱内细节；PolynomialFeatures 增加一次、平方和交互项；log 变换压缩正数跨度，需说明定义域，不能对零或负数直接 log。

课堂的类别不平衡例子有 200 对 20 个样本。`class_weight='balanced'` 使用 $w_c=N/(K N_c)$，两权重为 0.55、5.5，让两类总权重相等；它改变损失，不会凭空生成新数据。Lecture3c，第35–42个单元 的垃圾邮件例子讨论的是**错误代价不同**：合法邮件被扔掉更严重。人为设权重 {0:0.2,1:5} 让 class1 的单个样本权重是另一类的 25 倍，需要先说清哪个标签代表什么。

**自测 / Check:** 1000封合法邮件、10封垃圾邮件，全部预测合法，accuracy 是否足以说明成功？ / A set contains 1000 legitimate messages and 10 spam messages. Is predicting every message as legitimate successful based on accuracy alone?

<details markdown="1"><summary>答案 / Answer</summary>

accuracy=1000/1010≈99.01%，但垃圾邮件召回率为0；两类 balanced accuracy=(1+0)/2=0.5。 / Accuracy is about 99.01%, spam recall is zero, and balanced accuracy is 0.5. 应按任务代价同时看各类表现。

</details>

来源：Lecture3c，第7–42个单元。


<a id="cost-threshold"></a>
### 改类别权重，与改预测阈值
<!-- EXAM:focus-cost-threshold:START -->
<div class="exam-focus"><div class="exam-focus-title">考点：不平衡、代价与阈值</div><div class="exam-badges" aria-label="历史考查记录"><span class="exam-badge exam-mid">期中直接 · 5 套</span></div></div>
<!-- EXAM:focus-cost-threshold:END -->


提高一类的训练权重，会改变要最小化的损失，通常需要重新训练。改变预测阈值，则使用已经训练好的概率，另设判成正类的门槛。例如三个样本的正类概率为0.2、0.4、0.8，以“概率至少达到阈值”判正：阈值0.5得到负、负、正；降到0.3变为负、正、正。它减少漏报的机会，同时也可能增加误报，效果要结合真实标签检查。

**变式 / Transfer：** 同样三个概率，把阈值改成0.7，哪些判正？能否仅由预测概率计算召回率？ / With probabilities (0.2,0.4,0.8), use threshold 0.7. Which samples are positive, and can recall be computed without their true labels?

**答 / Answer：** 只有第三个判正；没有真实标签就不能计算召回率。 / Only the third is positive; recall also requires the true labels.

阈值与权重都要在训练内部的验证资料上选择。误判代价不同不等于类别数量一定不平衡，两种原因应分别说明。

## 14. Classification summary｜把不同方法放在同一张地图

| 方法 | 训练在做什么 | 输出/优势 | 条件与代价 |
|---|---|---|---|
| Bayes / NB | 估计先验与类条件分布 | 可多类；结构假设降低估计负担 | 依赖分布/独立假设；边界可线性或非线性 |
| Logistic regression | 正则化条件似然 | 概率与线性分数 | 概率校准仍需检查，不是名称保证 |
| Linear SVM | 权衡间隔与 hinge 违规 | 高维线性判别 | 原始分数非概率；尺度/C有影响 |
| Kernel SVM | 在核特征空间做 SVM | 非线性与自定义相似度 | 核条件、调参、Gram矩阵开销 |

把这些模型的训练目标放在一起，可统一写为 $\sum_i L(y_i,f(x_i))+\lambda\Omega(f)$：数据拟合加模型复杂度惩罚。Logistic loss 对分对的点仍有非零惩罚，hinge 超过间隔后为0；原画图将 logistic loss 除以 log2 是视觉尺度调整，不能无声当成同一正则强度的目标。

<a id="loss-shapes"></a>
### 看损失曲线时，先看横轴
<!-- EXAM:focus-loss-shapes:START -->
<div class="exam-focus"><div class="exam-focus-title">考点：分类损失曲线</div><div class="exam-badges" aria-label="历史考查记录"><span class="exam-badge exam-mid">期中直接 · 5 套</span></div></div>
<!-- EXAM:focus-loss-shapes:END -->


本讲的分类损失横轴通常是有符号分数$z=yf(x)$：z<0代表分错，z>0代表分对。Logistic与hinge都希望把负分数推向正方向，但hinge在z≥1后停止惩罚，logistic仍继续平滑下降。若换成$\ell(z)=\max(0,-1-z)$，则z=−0.5明明分错，损失已经为0；优化它不必纠正这类错误。

**判断 / Check：** 对刚才的损失，z=−0.8与z=0.2的损失各是多少？哪一个分类正确？ / For this loss, evaluate z=−0.8 and z=0.2 and identify the correctly classified case.

**答 / Answer：** 两者损失都是0，只有z=0.2分类正确。 / Both losses are zero; only z=0.2 is correctly classified. 这个教学例子对应历史题的损失图辨读，不作为推荐训练目标。

指数损失$\ell(z)=e^{-z}$对非常负的z增长更快。用同一个有符号分数比较，z=−2时，Logistic、hinge、指数损失约为2.127、3、7.389；改成z=−4，分别约为4.018、5、54.598。最后一种会给远端错分点很大权重；若这些点是错标或异常点，就可能过度受它们影响。这是历史AdaBoost损失题的比较背景，更新算法仍属另一个问题。 / Exponential loss grows much faster on strongly negative margins, which can increase sensitivity to mislabeled outliers.

<a id="parameter-count"></a>
### 参数少，具体少在哪里
<!-- EXAM:focus-parameter-count:START -->
<div class="exam-focus"><div class="exam-focus-title">考点：模型参数计数</div><div class="exam-badges" aria-label="历史考查记录"><span class="exam-badge exam-mid">期中直接 · 1 套</span></div></div>
<!-- EXAM:focus-parameter-count:END -->


二分类、d维输入时，logistic regression学习d个权重和一个偏置，共d+1个参数。若Gaussian NB给两类各d个均值，并强制所有类、所有维度共用一个标量方差，则有2d+1个分布参数；类别先验若也从数据学习，还要加1个自由参数，共2d+2。不同维度或不同类别使用各自方差时，数量会变化。

**变式 / Transfer：** d=3，采用上述共享标量方差，并学习类别先验。两个模型分别有多少参数？ / For d=3, compare logistic regression with Gaussian NB using one shared scalar variance and a learned class prior.

**答 / Answer：** 4与8。 / Four and eight. 历史随卷答案有省略先验的计数，作答时应先写清采用的约定。

“No Free Lunch”提醒我们不存在对所有任务都占优的模型，不代表在特定数据与假设下无法比较模型。用一致划分、合适指标和验证设计比较，可以将本讲的算法放在同一条件下评价。

来源：Lecture3c，第44–50个单元。


## 15. Back to the tutorial and English self-test｜从本讲走向实践

[Tutorial 3](Tutorial03.ipynb) 将图像展平成特征，先比较 LR 与 linear SVM，再裁剪与使用 L1 核。它检验的是这讲的表示、CV、模型比较与权重解读，不是仅会调用 fit。

1. **Why does multiplying both w and b by a positive constant leave the boundary unchanged? / 为什么同时正比例放大 w、b 不改变边界？** 答：原来满足 $w^Tx+b=0$ 的点，整体乘一个正数后仍满足这个等式，所以分界线不变。距离公式的分子、分母放大相同倍数，距离也不变。 / The zero set is unchanged and the scale cancels in geometric distance.
2. **Does a point inside the margin have to be misclassified? / 间隔内必然错分吗？** 答：不是，$0\lt yf\lt 1$ 仍正确。 / No; a signed score between zero and one is correct but violates the margin.
3. **Why put scaling inside CV? / 为什么在每折内部缩放？** 答：验证折不能影响拟合的预处理参数。 / Validation data must not determine fitted preprocessing parameters.
4. **What is the difference between a decision score and a probability? / 分数与概率有什么区别？** 答：分数可任意实数，概率需在[0,1]且对类别归一。 / Scores need not be bounded or normalized; class probabilities do.

先复习已有卡 [M143、M144、M146：SVM间隔](https://crazyshout.github.io/micro-course/cards.html#CS5489-M143)、[M166：核技巧](https://crazyshout.github.io/micro-course/cards.html#CS5489-M166)；按卡号定位，卡组复习继续在 Markji。

<!-- EXAM:topics:START -->
<a id="exam-topic-index"></a>
## Historical exam map｜按考点查题源

题号和页码指向原题纸；多题出现只增加定位，不重复增加同一卷的次数。需要整题作答时，请按题号回查原卷；当前独立题答册只整理Lecture 2。

<div class="exam-topic-unit" markdown="1">
### 生成式与判别式

比较拟合对象与边界形式。

| 试卷 | 原题号／页码 | 关系与要求 |
|---|---|---|
| 2020B期中Quiz | Q10／5 | 直接：比较高斯Bayes与二次核SVM的边界表达 |
| 2021A期中 | Q1、Q8／2–3 | 直接：生成式与判别式学习对象及线性分类器比较 |
| 2021B*期中 | Q7／3 | 直接：用给定分类任务说明生成式与判别式 |
</div>

<div class="exam-topic-unit" markdown="1">
### 模型参数计数

按方差结构和是否学习先验计算自由参数。

| 试卷 | 原题号／页码 | 关系与要求 |
|---|---|---|
| 2023B期中 | Q8／5 | 直接：Logistic与共享标量方差Gaussian NB的参数计数 |

**题源条件：** 先说明是否学习类别先验。
</div>

<div class="exam-topic-unit" markdown="1">
### Logistic似然与优化

写出损失、求梯度并判断解的条件。

| 试卷 | 原题号／页码 | 关系与要求 |
|---|---|---|
| 2020B期中Quiz | Q1／2 | 直接：Logistic损失、优化、C与输出分数 |
| 2020B期中Quiz | Q12／6 | 直接：L1 Logistic目标与稀疏边界 |
| 2021A期中 | Q9／3 | 直接：按数据规模与解释需求选择分类模型 |
| 2021B*期中 | Q1／2 | 直接：多类SVM、Logistic和输入处理选项 |
| 2023A期中 | Q2／2 | 直接：Logistic概率、多类与有限解条件 |
| Mock Exam（复用2023A题面） | Q2／1 | 直接（样题）：Logistic概率、多类与有限解条件 |
| 2023A期中 | Q8／5 | 直接：损失与MAP正则参数解释 |
| Mock Exam（复用2023A题面） | Q8／4 | 直接（样题）：损失与MAP正则参数解释 |
| 2023B期中 | Q2／2 | 直接：条件MLE、MAP与交叉验证 |
| 2025A期中 | Q2／2 | 直接：Logistic学习目标与输出 |
| 2025A期中 | Q8／5 | 直接：Logistic目标中的损失与正则项 |

**题源条件：** 凸目标不自动保证唯一有限解；L1可能促零；不是每个数据集都只剩一个特征；题中f是分数；不能把分数与概率混用。
</div>

<div class="exam-topic-unit" markdown="1">
### 正则化、MAP与CV

比较惩罚与C并设计训练内验证。

| 试卷 | 原题号／页码 | 关系与要求 |
|---|---|---|
| 2020B期中Quiz | Q1／2 | 直接：Logistic损失、优化、C与输出分数 |
| 2020B期中Quiz | Q4／2–3 | 直接：CV、重拟合与超参数选择 |
| 2020B期中Quiz | Q12／6 | 直接：L1 Logistic目标与稀疏边界 |
| 2021A期中 | Q5、Q11／3–4 | 直接：L2、MAP、正则项及其强度选择 |
| 2023A期中 | Q8／5 | 直接：损失与MAP正则参数解释 |
| Mock Exam（复用2023A题面） | Q8／4 | 直接（样题）：损失与MAP正则参数解释 |
| 2023B期中 | Q2／2 | 直接：条件MLE、MAP与交叉验证 |
| 2025A期中 | Q8／5 | 直接：Logistic目标中的损失与正则项 |

**题源条件：** 凸目标不自动保证唯一有限解；L1可能促零；不是每个数据集都只剩一个特征；题中f是分数；不能把分数与概率混用。
</div>

<div class="exam-topic-unit" markdown="1">
### SVM间隔、松弛与对偶

解释支持向量、约束、C和对偶维度。

| 试卷 | 原题号／页码 | 关系与要求 |
|---|---|---|
| 2020B期中Quiz | Q9／4–5 | 直接：高维特征时原始与对偶变量数的比较 |
| 2021A期中 | Q3、Q4／2 | 直接：核条件、支持向量与线性／非线性模型 |
| 2021B*期中 | Q1／2 | 直接：多类SVM、Logistic和输入处理选项 |
| 2023A期中 | Q3／2 | 直接：SVM目标、松弛变量与间隔 |
| Mock Exam（复用2023A题面） | Q3／1 | 直接（样题）：SVM目标、松弛变量与间隔 |
| 2023B期中 | Q3／2 | 直接：C、RBF拟合能力及间隔 |
| 2023B期中 | Q9／6 | 直接：比较不同C的二次核边界与泛化 |
| 2025A期中 | Q3、Q4／2 | 直接：SVM间隔、核技巧与支持向量 |
| 2021B期末 | Q1／2 | 直接：期末回顾SVM间隔、松弛与核 |
| Question Samples（年份未载） | Q2／2 | 直接（样题）：样题辨认软间隔与核技巧 |

**题源条件：** 极大C不保证任意数据可零错，重复冲突标签是反例。
</div>

<div class="exam-topic-unit" markdown="1">
### 核技巧与合法性

从特征内积、核矩阵和距离解释非线性。

| 试卷 | 原题号／页码 | 关系与要求 |
|---|---|---|
| 2020B期中Quiz | Q10／5 | 直接：比较高斯Bayes与二次核SVM的边界表达 |
| 2021A期中 | Q3、Q4／2 | 直接：核条件、支持向量与线性／非线性模型 |
| 2021A期中 | Q9／3 | 直接：按数据规模与解释需求选择分类模型 |
| 2021B*期中 | Q3／2 | 直接：核方法、支持向量及样本规模开销 |
| 2021B*期中 | Q5／3 | 直接：从三个输入的相似关系辨认RBF尺度 |
| 2023A期中 | Q4／3 | 直接：核空间、非线性及支持向量 |
| Mock Exam（复用2023A题面） | Q4／2 | 直接（样题）：核空间、非线性及支持向量 |
| 2023A期中 | Q9／6 | 直接：解释核技巧及其作用 |
| Mock Exam（复用2023A题面） | Q9／5 | 直接（样题）：解释核技巧及其作用 |
| 2023B期中 | Q3／2 | 直接：C、RBF拟合能力及间隔 |
| 2023B期中 | Q4／3 | 直接：归一化内积与积分核的合法性 |
| 2023B期中 | Q9／6 | 直接：比较不同C的二次核边界与泛化 |
| 2025A期中 | Q3、Q4／2 | 直接：SVM间隔、核技巧与支持向量 |
| 2021B期末 | Q1／2 | 直接：期末回顾SVM间隔、松弛与核 |
| 2020B期末 | Q7／3 | 关联：比较KPCA后线性SVM与直接核SVM |
| Question Samples（年份未载） | Q2／2 | 直接（样题）：样题辨认软间隔与核技巧 |

**题源条件：** 极大C不保证任意数据可零错，重复冲突标签是反例；KPCA不在当前Lecture1–5；这里只支持核方法部分。
</div>

<div class="exam-topic-unit" markdown="1">
### 求解维度与预测存储

区分训练开销、支持向量数与部署内存。

| 试卷 | 原题号／页码 | 关系与要求 |
|---|---|---|
| 2020B期中Quiz | Q9／4–5 | 直接：高维特征时原始与对偶变量数的比较 |
| 2021B*期中 | Q3／2 | 直接：核方法、支持向量及样本规模开销 |
| 2023B期中 | Q10／7 | 直接：比较线性与核SVM预测内存 |

**题源条件：** 随卷解释把C与支持向量数写成单调关系；一般情况下不保证。
</div>

<div class="exam-topic-unit" markdown="1">
### 不平衡、代价与阈值

区分类权重、阈值与评价指标。

| 试卷 | 原题号／页码 | 关系与要求 |
|---|---|---|
| 2020B期中Quiz | Q7／3–4 | 直接：疾病筛查的误判代价、类别权重和阈值 |
| 2021A期中 | Q10／4 | 直接：类别不平衡与不同误判代价 |
| 2021B*期中 | Q9／4 | 直接：邮件误判代价、权重与阈值 |
| 2023A期中 | Q10／7 | 直接：疾病筛查的不平衡与不同误判代价 |
| Mock Exam（复用2023A题面） | Q10／6 | 直接（样题）：疾病筛查的不平衡与不同误判代价 |
| 2023B期中 | Q13／10 | 直接：代价敏感训练与阈值调整 |
</div>

<div class="exam-topic-unit" markdown="1">
### 分类损失曲线

由有符号分数解释正确性和惩罚。

| 试卷 | 原题号／页码 | 关系与要求 |
|---|---|---|
| 2020B期中Quiz | Q8／4 | 直接：辨读非标准分类损失曲线 |
| 2021A期中 | Q13／4 | 直接：给定分类损失的形状与性质 |
| 2021B*期中 | Q13／4 | 直接：非凸分类损失对远端错分点的作用 |
| 2023A期中 | Q13／10 | 直接：零损失区域仍含错分样本的反例 |
| Mock Exam（复用2023A题面） | Q13／9 | 直接（样题）：零损失区域仍含错分样本的反例 |
| 2025A期中 | Q9／6 | 直接：比较Logistic、hinge和指数损失对错分点的惩罚 |
</div>
<!-- EXAM:topics:END -->

## 16. 原课疑点与覆盖索引

主依据为当前 Lecture3a、Lecture3b、Lecture3c 及 SVM 手写补充。Notebook单元按原文件从1计数，手写补充按PDF页码计。补充推导与课件勘误在对应位置标注。

**已核对修正：** Lecture3b，第38个单元 不应对所有不等式乘子都强行令 $\partial L/\partial\lambda=0$；应使用KKT。Lecture3b，第40个单元强对偶需条件；Lecture3b，第41个单元/SVM手写补充，第4页的乘子关系需保留单向蕴含；SVM手写补充，第2页名称为 Karush 而非 Krause；SVM手写补充，第2页弱对偶用≤而不是总用&lt;；SVM手写补充，第3–4页的软间隔乘子边界取包含端点的解释；Lecture3b，第58个单元正则系数差2；Lecture3b，第86个单元扩维不保证可分；Lecture3b，第118个单元半正定非严格正定；Lecture3c，第17个单元乘法笔误。原件均未改动。

| 原位置（单元号从1起） | 本文对应 | 内容处理 |
|---|---|---|
| Lecture3a，第1–7个单元 | 开篇、§1 | 课程位置、生成式/判别式、设置 |
| Lecture3a，第8–23个单元 | §1 | 共享方差推导、iris2、后验图代码用途 |
| Lecture3a，第24–31个单元 | §2 | 线性函数、超平面、两半空间 |
| Lecture3a，第32–48个单元 | §3 | sigmoid、MLE、signed score、loss |
| Lecture3a，第49–52个单元 | §4 | 先验、正则、优化；补完整梯度 |
| Lecture3a，第53–64个单元 | §5 | 原Iris划分、系数、预测图与准确率 |
| Lecture3a，第65–73个单元 | §5 | C、CV、结果字段 |
| Lecture3a，第74–85个单元 | §6 | OvR及三类Iris演示 |
| Lecture3a，第86–100个单元 | §6、§14 | softmax、one-hot似然、交叉熵与总结；末空单元 |
| Lecture3b，第1–10个单元 | §7 | 设置、可分数据、多个候选边界 |
| Lecture3b，第11–30个单元 | §7 | margin图、参数/样本扰动直觉、距离 |
| Lecture3b，第31–36个单元 | §7 | 归一化、约束、硬间隔目标 |
| Lecture3b，第37–48个单元 | §8–9 | Lagrangian、dual、乘子、预测 |
| Lecture3b，第49–60个单元 | §10 | slack、C、hinge及图示 |
| Lecture3b，第61–82个单元 | §11、§5 | Iris、网格、测试、多类OvO/OvR |
| Lecture3b，第83–100个单元 | §11 | 非线性例子、映射、多项式核及边界 |
| Lecture3b，第101–117个单元 | §12 | RBF、gamma、Iris网格搜索 |
| Lecture3b，第118–124个单元 | §12、§14 | 合法核、Euclidean自定义核、总结 |
| Lecture3c，第1–6个单元 | §5、§13 | 数据与作图辅助函数 |
| Lecture3c，第7–24个单元 | §13 | 缩放、编码、binning、polynomial、log |
| Lecture3c，第25–42个单元 | §13 | 数量不平衡与错误代价 |
| Lecture3c，第43–53个单元 | §14–15 | 比较表、loss/regularization/SRM、应用与NFL |
| SVM手写补充，第1页 | §7 | 距离、归一化、硬间隔；原图与前提 |
| SVM手写补充，第2页 | §8–9 | 约束、KKT、弱/强对偶 |
| SVM手写补充，第3页 | §8、§10 | 硬对偶、软原问题及三组求导 |
| SVM手写补充，第4页 | §9–10 | 支持向量与乘子情形；修正退化边界 |

Notebook的重复绘图单元和辅助代码按概念合并。下方保留四页SVM手写补充，可放大对照原式，再回到§8–10的逐步解释。

<details markdown="1"><summary>SVM手写原图（四页）</summary>

![SVM supplement page 1](assets/svm-supplement-1.png)
![SVM supplement page 2](assets/svm-supplement-2.png)
![SVM supplement page 3](assets/svm-supplement-3.png)
![SVM supplement page 4](assets/svm-supplement-4.png)

</details>
