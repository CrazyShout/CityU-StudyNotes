# CS5489 · 期中题目册 / Midterm Questions

收录六套历年期中卷，78个原题位置按实质内容去重后为67题。同题跨年只排一次，全部出处保留；条件、选项或要求有实质区别时分别保留。

英文题干保留原题内容，数学符号按原卷核对排版；中文帮助理解。MT编号属于本题库，与原卷Q编号不同。2021B*存在封面年份冲突，按配套解答归档。

各组按概念、示范、判断与应用逐步展开，阅读次序不按MT编号大小排列。按一整套卷练习可用 [原卷索引](PaperIndex.md)。模拟题、期末题和QE不混入本册。旧题规则不代表本学期考试规定。

## 目录

**学习流程与模型诊断**

- [MT011 · 识别过拟合，并提出可操作的改进](#mt011)
- [MT004 · CV选完参数后，为什么还要重新训练？](#mt004)
- [MT028 · 训练误差低、测试误差高：可能原因](#mt028)
- [MT002 · 训练准、测试差：哪些改进值得尝试？](#mt002)
- [MT020 · 数据很多，训练和测试仍都差](#mt020)
- [MT022 · 五万客户、需要解释：选择哪种分类器？](#mt022)

**Bayes、Naive Bayes与模型比较**

- [MT040 · Bayes规则和Naive Bayes的关系](#mt040)
- [MT052 · 生成式分类器学了什么](#mt052)
- [MT046 · 完整讲出Gaussian NB](#mt046)
- [MT015 · NB的最优性、独立性与边界](#mt015)
- [MT032 · Bayesian classifier的性质](#mt032)
- [MT005 · NB的学习、不确定性和正则化](#mt005)
- [MT034 · 无限数据能消除分类错误吗](#mt034)
- [MT014 · 生成式与判别式的区别](#mt014)
- [MT033 · 用图像特征解释两种建模方式](#mt033)
- [MT059 · LR与共享方差Gaussian NB](#mt059)
- [MT021 · 同为线性分类器，学习原则有何不同](#mt021)
- [MT017 · 哪些模型能产生不同形状的边界](#mt017)
- [MT027 · 连续特征能否使用NB：混合选择题](#mt027)
- [MT058 · 智能笔上的文本NB如何改进](#mt058)

**逻辑回归与参数正则**

- [MT041 · Logistic的概率、多分类与最优解](#mt041)
- [MT047 · 解释Logistic目标中的两项](#mt047)
- [MT024 · 损失与正则项：α从哪里来？](#mt024)
- [MT018 · 为什么在线性分类器上加L2？](#mt018)
- [MT012 · L1逻辑回归：写目标并画边界](#mt012)
- [MT001 · Logistic训练：哪些说法不成立？](#mt001)
- [MT053 · LR与生成式模型：混合选择题](#mt053)

**SVM与核方法**

- [MT042 · SVM的基本特点](#mt042)
- [MT048 · 用一个例子讲清Kernel Trick](#mt048)
- [MT016 · 核SVM：变换、存储与非向量输入](#mt016)
- [MT031 · RBF距离与带宽：看近点和远点](#mt031)
- [MT055 · 判断五个候选核是否合法](#mt055)
- [MT060 · 二次核SVM：大C与小C的边界](#mt060)
- [MT054 · C、支持向量与RBF的零训练误差](#mt054)
- [MT043 · 核SVM怎样处理非线性？](#mt043)
- [MT029 · 哪些SVM说法错误？](#mt029)
- [MT010 · 同一张分布图，Gaussian Bayes与二次核SVM如何判断？](#mt010)
- [MT009 · 十万维特征、两千样本：SVM怎样提速？](#mt009)
- [MT061 · 预测内存：线性SVM与RBF SVM](#mt061)

**回归、特征选择与残差损失**

- [MT019 · Ridge、LASSO与零系数](#mt019)
- [MT045 · 特征选择：零系数、Ridge与OMP](#mt045)
- [MT030 · L1/L2回归的益处与措辞边界](#mt030)
- [MT057 · 同时使用L1与L2：Elastic Net](#mt057)
- [MT025 · 绝对残差损失对异常值有什么影响？](#mt025)
- [MT063 · Huber损失：画图并解释好处](#mt063)
- [MT013 · 残差L1＋权重L2，各自在做什么？](#mt013)
- [MT050 · 缺车比车多更糟：设计非对称损失](#mt050)
- [MT037 · 线性回归为何与均值预测器表现相近？](#mt037)

**集成学习**

- [MT006 · Bagging与Boosting的基本区别](#mt006)
- [MT044 · 随机森林与Boosting的用途](#mt044)
- [MT062 · 随机森林：树多了为什么仍有共同误差？](#mt062)
- [MT056 · 集成方法：树深、并行与后续轮次](#mt056)
- [MT038 · 100核部署：RF与AdaBoost如何并行预测？](#mt038)
- [MT049 · 在线更新AdaBoost：速度与异常值](#mt049)
- [MT064 · 综合题：Bagging/Boosting与Huber](#mt064)

**分类损失图与错误代价**

- [MT008 · 平方形分类损失为什么惩罚“太正确”？](#mt008)
- [MT026 · V形损失：最优点为何在z=1？](#mt026)
- [MT051 · 负间隔也零损失：分类器会放过什么？](#mt051)
- [MT039 · 饱和的非凸分类损失](#mt039)
- [MT065 · 比较Logistic、Hinge和Exponential损失](#mt065)
- [MT007 · 筛查任务：漏诊比误报更贵](#mt007)
- [MT023 · 1000名受试者中只有50名阳性](#mt023)
- [MT035 · 正常邮件被大量拦截怎么办？](#mt035)

**神经网络与链式法则**

- [MT067 · 链式求导与两层网络反传](#mt067)
- [MT066 · 梯度消失：为什么深度和激活函数有关？](#mt066)

**历史范围拓展：Gaussian Process**

- [MT003 · 历史拓展：Gaussian Process的假设](#mt003)
- [MT036 · 历史拓展：音乐地理回归，GP还是RF？](#mt036)

<a id="mt011"></a>
## MT011 · 识别过拟合，并提出可操作的改进

**考点：** 学习流程与模型诊断

**出处：** 2020B期中Quiz Q11，原卷第5页（10分）

### English question
What is overfitting? How do we know when it happens? Write down and describe several methods to address the problem of overfitting.

### 中文题意
什么是过拟合？怎样发现它？列举并说明几种解决过拟合的方法。

[题目](Questions.md#mt011) · [答案](Answers.md#mt011)

<a id="mt004"></a>
## MT004 · CV选完参数后，为什么还要重新训练？

**考点：** 学习流程与模型诊断

**出处：** 2020B期中Quiz Q4，原卷第2–3页（5分）

### English question
Which statements about cross-validation are correct? (select all that apply)

A) The validation set for cross-validation is a part of the training data.

B) The best parameters are found through comparing the performance on the testing set.

C) In logistic regression, the corresponding w and b of the best C in the cross-validation stage might be different from the w and b in the training stage with the best C.

D) If the final testing score is still low with the best parameters selected through cross- validation, the reason could be that the step for the parameter selection is too large.

### 中文题意
关于交叉验证，哪些说法正确？多选。

A）CV的验证部分来自训练数据。B）通过比较最终测试集表现选择最优参数。C）逻辑回归选出最佳C后，重训练得到的w、b可能与CV阶段不同。D）最佳CV设置的最终测试分数仍低，可能因为超参数搜索步长太大。

[题目](Questions.md#mt004) · [答案](Answers.md#mt004)

<a id="mt028"></a>
## MT028 · 训练误差低、测试误差高：可能原因

**考点：** 学习流程与模型诊断

**出处：** 2021B*期中 Q2，原卷第2页（5分）

### English question
Suppose you are working on a classification problem. Your classifier gives low training error but high testing error. The reasons could be: (select all that apply)

A) The training set is too small.

B) The testing set is too large.

C) The distributions of the training set and testing set are different.

D) The classifier is too strong and overfits on the training set.

E) The classifier is too weak to fit on the testing set.

### 中文题意
分类器训练误差低、测试误差高，可能的原因有哪些？多选。

A）训练集太小。B）测试集太大。C）训练与测试分布不同。D）分类器过强，过拟合训练集。E）分类器太弱，无法拟合测试集。

[题目](Questions.md#mt028) · [答案](Answers.md#mt028)

<a id="mt002"></a>
## MT002 · 训练准、测试差：哪些改进值得尝试？

**考点：** 学习流程与模型诊断

**出处：** 2020B期中Quiz Q2，原卷第2页（5分）

### English question
Suppose you have trained a classifier for binary classification task. It gives high accuracy on the training set, but the accuracy is low on the test set. Which methods could be adopted to improve the test accuracy? (select all that apply)

A) Delete some training samples randomly.

B) Employ more complex classifiers.

C) Increase the regularization.

D) Employ Cross-validation on the training set.

E) Train an ensemble of classifiers using bagging.

### 中文题意
二分类器训练集准确率高、测试集准确率低，哪些方法可能改善测试表现？多选。

A）随机删除训练样本。B）换更复杂的模型。C）加强正则。D）在训练集内部使用交叉验证。E）用bagging训练集成分类器。

[题目](Questions.md#mt002) · [答案](Answers.md#mt002)

<a id="mt020"></a>
## MT020 · 数据很多，训练和测试仍都差

**考点：** 学习流程与模型诊断

**出处：** 2021A期中 Q7，原卷第3页（10分）

### English question
Consider a situation where you have trained a linear classification model to diagnose mental disorders patients from symptom checklist data. You have 100,000 training examples, which is sufficient data for learning. However, your model performs poorly on both training and testing datasets. What is the main problem that cause this situation? How to correct the problem? List 2 potential solutions.

### 中文题意
用症状清单训练线性分类器诊断精神障碍。已有100,000个训练样本，题设认为数据量充分，但训练和测试表现都很差。主要问题可能是什么？提出两种解决办法。

[题目](Questions.md#mt020) · [答案](Answers.md#mt020)

<a id="mt022"></a>
## MT022 · 五万客户、需要解释：选择哪种分类器？

**考点：** 学习流程与模型诊断

**出处：** 2021A期中 Q9，原卷第3页（10分）

### English question
Suppose you are a global market analyst who needs to analyse a product line (a group of similar products with different prices) and get some insight. You want to classify your 50,000 clients according to the product they brought. You have collected 25 features on your clients, e.g. age, income, educational level, frequency of using the product, their scores on other similar products. Among Logistic Regression, kernel SVM and random forest, which classifier will you prefer to use? List 2 reasons for using your selected classifier, and 1 reason for each of the other unselected classifiers.

### 中文题意
市场分析任务有50,000名客户，每人25个特征，例如年龄、收入、教育程度、产品使用频率和对类似产品的评分。按购买的产品分类，并希望得到业务洞见。在逻辑回归、核SVM和随机森林中选择一种。说明两个选择理由，以及另两种各一个不选理由。

[题目](Questions.md#mt022) · [答案](Answers.md#mt022)

<a id="mt040"></a>
<a id="l2q05"></a>
## MT040 · Bayes规则和Naive Bayes的关系

**考点：** Bayes、Naive Bayes与模型比较

**出处：** 2023A期中 Q1，原卷第2页（5分）；2025A期中 Q1，原卷第2页（5分）

### English question
Which of the following statements accurately describe the relationship between the Bayesian decision rule and Naïve Bayes (NB) classifiers? (select all that apply)

A) Naïve Bayes classifiers are a specific implementation of the Bayesian decision rule.

B) For a binary classification task with feature $x$ and $y\in\{0,1\}$ as the class labels, according to Bayesian decision rule, if $p(x\mid y=0)>p(x\mid y=1)$, then choose Class 0.

C) Naïve Bayes classifiers assume each feature dimension is modeled independently.

D) The Bayesian decision rule is more computationally efficient than Naïve Bayes classifiers.

E) The Bayesian decision rule is only applicable to binary classification tasks.

### 中文题意
哪些说法准确描述Bayes决策规则与NB的关系？多选。

A）NB是Bayes决策规则的一种具体实现。B）二分类标签为0、1时，只要类0的类条件密度较大就选0。C）NB对各特征维独立建模。D）Bayes决策规则比NB计算更高效。E）Bayes决策规则只能用于二分类。

[题目](Questions.md#mt040) · [答案](Answers.md#mt040)

<a id="mt052"></a>
<a id="l2q01"></a>
## MT052 · 生成式分类器学了什么

**考点：** Bayes、Naive Bayes与模型比较

**出处：** 2023B期中 Q1，原卷第2页（5分）

### English question
Which statements about generative classification model are correct? (select all that apply)

A) They estimate probability distributions of features from each class.

B) It is hard to add prior knowledge to the classifier.

C) It can only work with binary classification problems.

D) Selecting different probability distributions can obtain different classification performance.

E) They predict the class with the largest class conditional densities.

### 中文题意
关于生成式分类模型，哪些说法正确？多选。

A）估计每一类中特征的概率分布。B）难以向分类器加入先验知识。C）只能处理二分类。D）选择不同分布可能得到不同分类表现。E）预测类条件密度最大的类别。

[题目](Questions.md#mt052) · [答案](Answers.md#mt052)

<a id="mt046"></a>
<a id="l2q09"></a>
## MT046 · 完整讲出Gaussian NB

**考点：** Bayes、Naive Bayes与模型比较

**出处：** 2023A期中 Q7，原卷第4页（10分）；2025A期中 Q11，原卷第8页（10分）

### English question
Consider the Naïve Bayes Gaussian classifier with feature vector $x\in\mathbb{R}^d$ and binary class label $y\in\{0,1\}$.

(a) What are the assumptions of this classification model?

(b) What are the probability distributions in this model, and what form do they have?

(c) Given a feature vector $x$, what is the rule for performing classification with this model?

### 中文题意
考虑特征向量$x\in\mathbb R^d$、类别$y\in\{0,1\}$的Gaussian NB分类器。（a）模型有什么假设？（b）涉及哪些概率分布，各自是什么形式？（c）给定$x$，怎样分类？

[题目](Questions.md#mt046) · [答案](Answers.md#mt046)

<a id="mt015"></a>
<a id="l2q08"></a>
## MT015 · NB的最优性、独立性与边界

**考点：** Bayes、Naive Bayes与模型比较

**出处：** 2021A期中 Q2，原卷第2页（5分）

### English question
Which of the following statements are correct about Naïve Bayes (NB) classifiers? (select all that apply)

A) NB classifiers will minimize the probability of making an error.

B) Because NB classifiers do not model correlations between features, the decision boundaries are always aligned with the axes.

C) NB classifiers do not directly learn the posterior probability of the class.

D) NB classifiers cannot overfit to the training data.

E) The NB classifier accuracy highly depends on the correct selection of the CCD.

### 中文题意
关于NB，哪些说法正确？多选。

A）NB会最小化出错概率。B）NB不建模特征相关性，所以边界总与坐标轴对齐。C）NB不直接学习类别后验。D）NB不会过拟合。E）NB的准确率很依赖类条件分布（CCD）的选择。

[题目](Questions.md#mt015) · [答案](Answers.md#mt015)

<a id="mt032"></a>
<a id="l2q06"></a>
## MT032 · Bayesian classifier的性质

**考点：** Bayes、Naive Bayes与模型比较

**出处：** 2021B*期中 Q6，原卷第3页（5分）

### English question
Which statements are true about Bayesian classifiers? (select all that apply)

A) Naïve Bayes classifiers can only model linear decision surfaces.

B) Bayesian classifiers explicitly define the posterior $p(y\mid x)$.

C) Bayesian classifiers cannot overfit the training data.

D) Bayesian classifiers minimize the probability of making a prediction error.

E) In Bayesian classifiers, the class probability $p(y)$ does not affect the classifier.

### 中文题意
关于Bayesian分类器，哪些说法正确？多选。

A）NB只能表示线性决策面。B）Bayesian分类器显式定义后验$p(y\mid x)$。C）Bayesian分类器不会过拟合。D）Bayesian分类器最小化预测错误概率。E）类别概率$p(y)$不影响分类器。

[题目](Questions.md#mt032) · [答案](Answers.md#mt032)

<a id="mt005"></a>
<a id="l2q07"></a>
## MT005 · NB的学习、不确定性和正则化

**考点：** Bayes、Naive Bayes与模型比较

**出处：** 2020B期中Quiz Q5，原卷第3页（5分）

### English question
Which statements about the naive Bayes classifiers are correct? (select all that apply)

A) Learning a Bayesian classifier is equivalent to estimating the posterior distribution.

B) A Bayes classifier that has a large prediction variance around the decision boundary has a good uncertainty property.

C) If the generative distribution is not Gaussian, the naive Bayesian classifier can be nonlinear.

D) Both naive Bayes classifier and logistic regression can learn model parameters by maximum likelihood estimation.

E) There is no regularization in a naive Bayes classifier.

### 中文题意
关于NB，哪些说法正确？多选。

A）学习Bayesian分类器等价于估计后验分布。B）在决策边界附近有较大预测方差，体现了合理的不确定性。C）生成分布非高斯时，NB可以是非线性分类器。D）NB与逻辑回归都可用最大似然估计参数。E）NB没有正则化。

[题目](Questions.md#mt005) · [答案](Answers.md#mt005)

<a id="mt034"></a>
<a id="l2q15"></a>
## MT034 · 无限数据能消除分类错误吗

**考点：** Bayes、Naive Bayes与模型比较

**出处：** 2021B*期中 Q8，原卷第3页（10分）

### English question
Consider the following statement: If we train a Bayes classifier using infinite training data that satisfies all of the modeling assumptions (e.g., data is from the class-conditional densities, and sampled independently), then it will achieve zero training error over these training examples.

Is this statement true or false? Give your reasons.

### 中文题意
判断并解释：若用无限多、符合模型假设的独立训练数据来训练Bayes分类器，它在这些训练样本上的错误率将为0。

[题目](Questions.md#mt034) · [答案](Answers.md#mt034)

<a id="mt014"></a>
<a id="l2q03"></a>
## MT014 · 生成式与判别式的区别

**考点：** Bayes、Naive Bayes与模型比较

**出处：** 2021A期中 Q1，原卷第2页（5分）

### English question
Which statements about generative and discriminative classifiers are not correct? (select all that apply)

A) New feature dimensions can be added to generative classifiers without re-training the model.

B) Generative classifiers are trained by learning the class-conditional and prior distributions.

C) Discriminative classifiers can learn from unlabelled training data.

D) Generative classifiers highly depend on prior probability distributions and Gaussian distribution is always better than other distributions when using Generative classifiers.

E) Bayes' classifier is a generative classifier, while SVM, logistic regression, AdaBoost, XGBoost and Random Forest are discriminative classifiers.

### 中文题意
关于生成式与判别式分类器，哪些说法不正确？多选。

A）生成式分类器增加新特征维度不需要重新训练。B）生成式分类器学习类条件分布与类别先验。C）判别式分类器可用无标签训练数据学习。D）生成式分类器高度依赖先验概率分布，而且高斯分布总比其他分布好。E）Bayes分类器属于生成式；SVM、逻辑回归、AdaBoost、XGBoost和随机森林属于判别式。

[题目](Questions.md#mt014) · [答案](Answers.md#mt014)

<a id="mt033"></a>
<a id="l2q04"></a>
## MT033 · 用图像特征解释两种建模方式

**考点：** Bayes、Naive Bayes与模型比较

**出处：** 2021B*期中 Q7，原卷第3页（10分）

### English question
Consider the classification problem of predicting a person's gender from an image of their face. Discuss the differences between adopting a discriminative classifier or a generative model for classification. How would you interpret the learned generative classifier and learned discriminative classifier?

### 中文题意
原题要求根据人脸图像预测题中记录的性别标签。比较采用判别式分类器与生成式模型的区别，并解释各自学到的模型表示什么。

[题目](Questions.md#mt033) · [答案](Answers.md#mt033)

<a id="mt059"></a>
<a id="l2q13"></a>
## MT059 · LR与共享方差Gaussian NB

**考点：** Bayes、Naive Bayes与模型比较

**出处：** 2023B期中 Q8，原卷第5页（10分）

### English question
Describe the major similarities and differences between logistic regression and naïve Bayes Gaussian classifier with shared variance parameter. List at least 5 similarities/differences (5 total).

### 中文题意
比较逻辑回归与共享方差参数的Gaussian NB，合计列出至少5项主要相同点或不同点。

[题目](Questions.md#mt059) · [答案](Answers.md#mt059)

<a id="mt021"></a>
<a id="l2q12"></a>
## MT021 · 同为线性分类器，学习原则有何不同

**考点：** Bayes、Naive Bayes与模型比较

**出处：** 2021A期中 Q8，原卷第3页（10分）

### English question
We have seen several types of linear classifiers, such as Logistic Regression, SVM, and Naïve Bayes with Gaussian CCDs with the same variance, which can all be expressed as learning the same function $f(x)=w^Tx+b$. How are these linear classifiers different? Which linear classifier is best in terms of accuracy?

### 中文题意
逻辑回归、SVM、各类共享方差的Gaussian NB都能写成学习$f(x)=w^Tx+b$。它们的区别是什么？哪一种的准确率最好？

[题目](Questions.md#mt021) · [答案](Answers.md#mt021)

<a id="mt017"></a>
<a id="l2q11"></a>
## MT017 · 哪些模型能产生不同形状的边界

**考点：** Bayes、Naive Bayes与模型比较

**出处：** 2021A期中 Q4，原卷第2页（5分）

### English question
For a binary classification problem with input feature dimension $d>2$, which of the following classifiers in principle could learn both linear and non-linear classification boundaries on different datasets? (select all that apply)

A) Naïve Bayes with the Gaussian distribution as the CCD.

B) SVM with the RBF kernel.

C) AdaBoost with the decision stump as the weak learner, and the number of weak learners is at least 3.

D) SVM with the polynomial kernel of degree=2, $k(x,x')=(x^Tx')^2$.

E) Logistic regression for some specific $\alpha$.

### 中文题意
二分类输入维数$d>2$。哪些模型原则上能在不同数据集上学出线性或非线性边界？多选。A）Gaussian NB；B）RBF核SVM；C）至少3个决策树桩的AdaBoost；D）齐次二次核$k(x,x')=(x^Tx')^2$的SVM；E）选取某个$\alpha$的逻辑回归。

[题目](Questions.md#mt017) · [答案](Answers.md#mt017)

<a id="mt027"></a>
<a id="l2q10"></a>
## MT027 · 连续特征能否使用NB：混合选择题

**考点：** Bayes、Naive Bayes与模型比较

**出处：** 2021B*期中 Q1，原卷第2页（5分）

### English question
Which statements are correct? (select all that apply)

A) One SVM model can be used for a three-class classification problem.

B) Logistic regression only forms a linear decision surface.

C) Normalization of features must be done before training a Logistic Regression.

D) Naive Bayes is not appropriate for continuous valued variables.

E) Lasso Regularization can be used for variable selection in Linear Regression.

### 中文题意
哪些说法正确？多选。A）一个SVM模型可用于三分类。B）逻辑回归只形成线性决策面。C）训练逻辑回归前必须归一化特征。D）NB不适合连续变量。E）线性回归中的LASSO可用于变量选择。

[题目](Questions.md#mt027) · [答案](Answers.md#mt027)

<a id="mt058"></a>
<a id="l2q16"></a>
## MT058 · 智能笔上的文本NB如何改进

**考点：** Bayes、Naive Bayes与模型比较

**出处：** 2023B期中 Q7，原卷第4页（10分）

### English question
You are working for a “smart pen” company, which can scan text using a handheld pen device. Your job is to build a model to classify the text the pen reads into different sentiment categories, such as “happy”, “sad”, “neutral”, which will then turn on different lights on the pen as a special effect. Because of the limited processing power on the pen, you will use a generative model classifier with bag-of-words model. A training set is provided, consisting of 5000 sentences and their class labels. Your initial classifier is Naïve Bayes Bernoulli model, but the performance is poor. How could you improve the model performance? (List 4 improvements)

### 中文题意
智能笔扫描文字后，要把它分成happy、sad、neutral等情绪类别，并点亮不同的灯。设备算力有限，采用词袋和生成式分类器。已有5000句带类别标签的训练文本，初始Bernoulli NB表现较差。提出4项改进。

[题目](Questions.md#mt058) · [答案](Answers.md#mt058)

<a id="mt041"></a>
## MT041 · Logistic的概率、多分类与最优解

**考点：** 逻辑回归与参数正则

**出处：** 2023A期中 Q2，原卷第2页（5分）；2025A期中 Q2，原卷第2页（5分）

### English question
Which statements are correct about the logistic regression? (select all that apply)

A) It estimates the probability of an input belonging to a particular class by dividing the likelihood of the class by the prior probability of the input.

B) The sigmoid function is commonly used in logistic regression to squeeze the output between 0 and 1.

C) In a "One-vs-Rest" (OVR) strategy for multiclass classification with three classes, only two decision boundaries are required to classify all three classes.

D) The output of logistic regression can be interpreted as a direct probability.

E) It is guaranteed that logistic regression will always converge to a unique solution for any dataset.

### 中文题意
关于逻辑回归，哪些说法正确？多选。

A）用类别似然除以输入的先验概率，估计类别概率。B）常用sigmoid将输出压到0与1之间。C）三分类的one-vs-rest只需两个分类边界。D）输出可解释为类别概率。E）对任何数据都保证收敛到唯一解。

[题目](Questions.md#mt041) · [答案](Answers.md#mt041)

<a id="mt047"></a>
## MT047 · 解释Logistic目标中的两项

**考点：** 逻辑回归与参数正则

**出处：** 2023A期中 Q8，原卷第5页（10分）；2025A期中 Q8，原卷第5页（10分）

### English question
For binary classification, the logistic regression model is trained using the following objective function:

$$
(w^*,b^*)=\arg\min_{w,b}\left\{\alpha w^Tw+
\sum_{i=1}^N\log(1+\exp[-y_i f(x_i)])\right\}.
$$

(a) Explain the purpose of each term in the objective function.

(b) Discuss the meaning of the hyperparameter α in logistic regression. How does varying α influence the values of weights w and the performance of the model?

### 中文题意
二分类逻辑回归的训练目标为

$$
(w^*,b^*)=\arg\min_{w,b}\left\{\alpha w^Tw+
\sum_{i=1}^N\log(1+\exp[-y_i f(x_i)])\right\}.
$$

(a) 分别解释每项的作用。(b) 解释α的意义及其变化对w和模型表现的影响。

[题目](Questions.md#mt047) · [答案](Answers.md#mt047)

<a id="mt024"></a>
## MT024 · 损失与正则项：α从哪里来？

**考点：** 逻辑回归与参数正则

**出处：** 2021A期中 Q11，原卷第4页（10分）

### English question
The goal of supervised training is to find the weights that best fit the training data (X,Y). To determine what we mean by best fit, we introduce a loss function L and the goal is to find the weights that minimize:

$$
\hat w=\arg\min_w\{L(X,Y)+\alpha\|w\|^2\}.
$$

(a) What is the purpose of the term $\|w\|^2$?

(b) How is α determined?

(c) Suppose we replace $\|w\|^2$ with $\|w\|_1$. What will be the effect when training the classifier?

### 中文题意
监督训练希望最小化

$$
\hat w=\arg\min_w\{L(X,Y)+\alpha\|w\|^2\}.
$$

(a) 平方范数项的目的是什么？(b) 怎样确定α？(c) 将平方范数换成 $\|w\|_1$，训练结果可能怎样变化？

[题目](Questions.md#mt024) · [答案](Answers.md#mt024)

<a id="mt018"></a>
## MT018 · 为什么在线性分类器上加L2？

**考点：** 逻辑回归与参数正则

**出处：** 2021A期中 Q5，原卷第3页（5分）

### English question
What is/are the purpose(s) of using L2 regularization on the weights in linear classifiers? (select all that apply)

A) L2 regularization will encourage some weights to be large.

B) L2 regularization will prevent overfitting.

C) In SVM, L2 regularization is equivalent to minimizing the margin distance.

D) In Logistic Regression, L2 regularization is equivalent to a Gaussian prior distribution on the weights.

E) L2 regularization is only used to stabilize the training, and it has no effects on the weights.

### 中文题意
在线性分类器权重上使用L2正则，有哪些目的？多选。

A）鼓励某些权重变大。B）防止过拟合。C）在SVM中等价于最小化间隔距离。D）在逻辑回归中等价于对权重施加高斯先验。E）只稳定训练，对权重没有影响。

[题目](Questions.md#mt018) · [答案](Answers.md#mt018)

<a id="mt012"></a>
## MT012 · L1逻辑回归：写目标并画边界

**考点：** 逻辑回归与参数正则

**出处：** 2020B期中Quiz Q12，原卷第6页（10分）

### English question
(a) Consider a logistic regression classifier using L1 regularization instead of L2 regularization? Write down the optimization problem for learning the classifier.

(b) Suppose we have the data in the figure below. Draw the most likely decision boundary for the L1-regularized logistic regression classifier. You can move/reshape the red line provided below. Explain why this should be the decision boundary.

![MT012 original question figure](assets/mt012-l1-boundary.png)

*原卷提供一条可调整红线；按题意自行移动或重画。 / The original supplies an adjustable red line.*

### 中文题意
(a) 将逻辑回归的L2正则换成L1，写出训练优化问题。

(b) 观察题图，画出最可能的L1正则逻辑回归边界，并解释。可以移动或调整图中给出的红线。

[题目](Questions.md#mt012) · [答案](Answers.md#mt012)

<a id="mt001"></a>
## MT001 · Logistic训练：哪些说法不成立？

**考点：** 逻辑回归与参数正则

**出处：** 2020B期中Quiz Q1，原卷第2页（5分）

### English question
Which statements are not true about Logistic Regression? (select all that apply)

A) When training a Logistic Regression model, we have only one local optimum solution.

B) When training a Logistic Regression model, we should fix the learning rate (η) to obtain the local optimum.

C) When training a Logistic Regression model with L2-norm regularization, while increasing the hyperparameter C, the training error will increase and testing error will decrease.

D) When performing classification with Logistic Regression, we can use different decision function (e.g., sigmoid, sign) in training and testing process.

### 中文题意
关于逻辑回归，选择所有不正确的说法。

A）训练时只有一个局部最优解。B）必须固定学习率 $\eta$ 才能取得局部最优。C）使用L2正则时，增大C会使训练错误率上升、测试错误率下降。D）训练和测试可使用不同的决策函数，例如训练用sigmoid、测试用sign。

[题目](Questions.md#mt001) · [答案](Answers.md#mt001)

<a id="mt053"></a>
<a id="l2q14"></a>
## MT053 · LR与生成式模型：混合选择题

**考点：** 逻辑回归与参数正则

**出处：** 2023B期中 Q2，原卷第2页（5分）

### English question
Which statements are correct about the logistic regression? (select all that apply)

A) Logistic regression has a closed-form solution based on the MLE formulation, and thus it can be efficiently solved.

B) To prevent overfitting, we can add a prior distribution on its parameters using a Gaussian distribution.

C) Logistic regression is used for modelling the class posterior probability, which is different from generative classifiers that model the class-conditional distribution.

D) The regularization parameter of the logistic regression function can be selected via cross-validation.

E) L2 regularization is only used to stabilize the training, and it has no effects on the weights.

### 中文题意
关于逻辑回归，哪些说法正确？多选。A）MLE有闭式解，因此求解高效。B）为抑制过拟合，可给参数加高斯先验。C）LR建模类别后验，而生成式分类器建模类条件分布。D）可用交叉验证选正则化参数。E）L2只稳定训练，不影响权重。

[题目](Questions.md#mt053) · [答案](Answers.md#mt053)

<a id="mt042"></a>
## MT042 · SVM的基本特点

**考点：** SVM与核方法

**出处：** 2023A期中 Q3，原卷第2页（5分）；2025A期中 Q3，原卷第2页（5分）

### English question
Which of the following are characteristics of Support Vector Machines (SVMs)? (select all that apply)

A) SVMs can work on non-separable data by adding slack variables.

B) SVMs find the hyperplane that maximizes the margin between classes.

C) SVMs are sensitive to outliers in the training data.

D) SVMs are unsuitable for high-dimensional data.

E) SVMs use k-means clustering to separate data.

### 中文题意
关于SVM，哪些说法成立？多选。

A）可通过松弛变量处理不可分数据。B）寻找最大间隔超平面。C）SVM对训练异常值敏感。D）SVM不适合高维数据。E）SVM用k-means聚类分开数据。

[题目](Questions.md#mt042) · [答案](Answers.md#mt042)

<a id="mt048"></a>
## MT048 · 用一个例子讲清Kernel Trick

**考点：** SVM与核方法

**出处：** 2023A期中 Q9，原卷第6页（10分）

### English question
Explain the concept of the "kernel trick" in Support Vector Machines (SVMs) and provide an intuitive example (e.g., using a figure).

### 中文题意
解释SVM中的kernel trick，并给一个直观例子，可以画图。

[题目](Questions.md#mt048) · [答案](Answers.md#mt048)

<a id="mt016"></a>
## MT016 · 核SVM：变换、存储与非向量输入

**考点：** SVM与核方法

**出处：** 2021A期中 Q3，原卷第2页（5分）

### English question
Which statements are true about kernel SVM? (select all that apply)

A) The kernel SVM is equivalent to learning a linear SVM on transformed inputs.

B) The training data is no longer necessary after learning the kernel SVM.

C) Any function that outputs positive values is a valid kernel function.

D) The kernel SVM can be applied to non-vector input data, like strings and sets.

E) The kernel trick can reduce both the memory and computation requirements, compared to an explicit transformation and inner-product.

### 中文题意
关于核SVM，哪些说法正确？多选。

A）等价于在变换后的输入上训练线性SVM。B）训练完成后不再需要训练数据。C）输出为正的任意函数都是合法核。D）可用于字符串、集合等非向量输入。E）相比显式变换再求内积，核技巧可能减少内存与计算。

[题目](Questions.md#mt016) · [答案](Answers.md#mt016)

<a id="mt031"></a>
## MT031 · RBF距离与带宽：看近点和远点

**考点：** SVM与核方法

**出处：** 2021B*期中 Q5，原卷第3页（5分）

### English question
Suppose we have the points x, y, and z below. We compute the Gaussian RBF kernel between the points, k(x,y) and k(x,z), using inverse bandwidth γ. Which statements are correct? (select all that apply)

A) For some choice of γ, both k(x,y) and k(x,z) will be close to 1.

B) For some choice of γ, both k(x,y) and k(x,z) will be close to 0.

C) For any choice of γ>0, $k(x,y)\ge k(x,z)$.

D) If k(x,y) is close to 1, then k(x,z) is also close to 1.

E) If k(x,y) is close to 0, then k(x,z) is also close to 0.

![MT031 original question figure](assets/mt031-rbf-points.png)

### 中文题意
题图中x离y较近、离z较远。用逆带宽γ计算Gaussian RBF核 $k(x,y)$ 和 $k(x,z)$，哪些说法正确？多选。

A）某些γ可使两者都接近1。B）某些γ可使两者都接近0。C）对任意γ>0都有 $k(x,y)\ge k(x,z)$。D）若前者接近1，后者也接近1。E）若前者接近0，后者也接近0。

[题目](Questions.md#mt031) · [答案](Answers.md#mt031)

<a id="mt055"></a>
## MT055 · 判断五个候选核是否合法

**考点：** SVM与核方法

**出处：** 2023B期中 Q4，原卷第3页（5分）

### English question
Which of the following are valid positive semi-definite kernel functions? (select all that apply)

A) $k(x,z)=x^Tz/(\|x\|\|z\|)$.

B) $k(x,y)=\int p(x\mid z)p(y\mid z)p(z)\,dz$, where $p(x\mid z)$ and $p(y\mid z)$ are conditional distributions, and $p(z)$ is a marginal distribution.

C) $k(x,y)=1$ if $-1<x^Ty<1$, and 0 otherwise.

D) $k(x,y)=\sin(x^Ty)$.

E) $k(x,y)=\tanh(x^Ty)$.

### 中文题意
下面哪些函数是合法的半正定核？多选。各输入是实向量。

A）$k(x,z)=x^Tz/(\|x\|\|z\|)$。

B）$k(x,y)=\int p(x\mid z)p(y\mid z)p(z)\,dz$，前两项为条件分布，$p(z)$为边缘分布。

C）当 $-1<x^Ty<1$ 时 $k(x,y)=1$，否则为0。

D）$k(x,y)=\sin(x^Ty)$。

E）$k(x,y)=\tanh(x^Ty)$。

[题目](Questions.md#mt055) · [答案](Answers.md#mt055)

<a id="mt060"></a>
## MT060 · 二次核SVM：大C与小C的边界

**考点：** SVM与核方法

**出处：** 2023B期中 Q9，原卷第6页（10分）

### English question
Consider the training data in the below figure, and the kernel SVM with quadratic polynomial kernel function. (a) Draw the decision boundary when C → ∞? (b) Draw the decision boundary for C → 0? (c) Which decision boundary would be better on the test data? For each part, give your reasons.

![MT060 original question figure](assets/mt060-data.png)

### 中文题意
给定题图训练点，使用二次多项式核SVM。(a) C趋于无穷时画边界。(b) C趋于0时画边界。(c) 哪个在测试数据上可能更好？每问说明理由。

[题目](Questions.md#mt060) · [答案](Answers.md#mt060)

<a id="mt054"></a>
## MT054 · C、支持向量与RBF的零训练误差

**考点：** SVM与核方法

**出处：** 2023B期中 Q3，原卷第2页（5分）

### English question
Which statements about support vector machines (SVMs) are correct? (select all that apply)

A) If the hyperparameter C is set to infinity, all the training points will be classified correctly if they are linearly separable.

B) Assuming there are three support vectors, the boundary will not change when one of the support vectors is moved.

C) If an SVM underfits the training data, then mapping the data to a lower-dimensional feature space will improve the classification performance.

D) The basic form of SVM is a convex quadratic programming problem.

E) The training data can always be correctly classified with a kernel SVM with RBF kernel function.

### 中文题意
关于SVM，哪些说法正确？多选。

A）线性可分时，C设为无穷可使训练点全部分类正确。B）三个支持向量之一移动，边界不会改变。C）欠拟合时，映射到更低维空间会改善表现。D）基本SVM是凸二次规划。E）RBF核SVM总能把训练数据完全分类正确。

[题目](Questions.md#mt054) · [答案](Answers.md#mt054)

<a id="mt043"></a>
## MT043 · 核SVM怎样处理非线性？

**考点：** SVM与核方法

**出处：** 2023A期中 Q4，原卷第3页（5分）；2025A期中 Q4，原卷第2页（5分）

### English question
Which statements about kernel support vector machines (SVMs) are correct? (select all that apply)

A) Support Vector Machines (SVM) can directly handle non-linearly separable data.

B) Radial basis functions are a commonly used type of kernel function.

C) Kernel methods can transform non-linear problem into a more efficient problem in the feature space.

D) The dual problem for SVM mainly involves selecting support vectors.

E) Using kernels can reduce the memory and computation requirements via explicit feature transformation and inner product calculations.

### 中文题意
关于核SVM，哪些说法成立？多选。

A）SVM可以直接处理线性不可分的数据。B）径向基函数是常用核。C）核方法把非线性问题变成特征空间里更高效的问题。D）SVM对偶问题主要涉及选择支持向量。E）通过显式特征变换和内积，核可以降低内存与计算。

[题目](Questions.md#mt043) · [答案](Answers.md#mt043)

<a id="mt029"></a>
## MT029 · 哪些SVM说法错误？

**考点：** SVM与核方法

**出处：** 2021B*期中 Q3，原卷第2页（5分）

### English question
Which statements about support vector machines are NOT correct? (select all that apply)

A) Kernel SVM cannot handle linearly separable data.

B) Data points lying around the regression tube boundary in support vector regression are called support vectors.

C) Kernel SVM can be interpreted as learning a linear classifier in a high-dimensional space.

D) The kernel function is limited to vector data only.

E) Because SVM only needs support vectors to estimate model parameters, it has good scalability to large datasets.

### 中文题意
关于SVM，选择所有不正确的说法。

A）核SVM不能处理线性可分数据。B）SVR中回归容忍带边界附近的点称为支持向量。C）核SVM可理解成在高维空间中学习线性分类器。D）核函数只能用于向量输入。E）SVM只需要支持向量估计模型参数，所以对大数据扩展性很好。

[题目](Questions.md#mt029) · [答案](Answers.md#mt029)

<a id="mt010"></a>
## MT010 · 同一张分布图，Gaussian Bayes与二次核SVM如何判断？

**考点：** SVM与核方法

**出处：** 2020B期中Quiz Q10，原卷第5页（10分）

### English question
Consider the data distribution shown in the figure below. If you train a Bayes Gaussian classifier, which class will be predicted for data point D? If we change the classifier to an SVM with polynomial kernel of degree 2, which class will be predicted? Explain why.

![MT010 original question figure](assets/mt010-distribution.png)

### 中文题意
依据题图的两类训练数据，Gaussian Bayes分类器会将点D判为哪一类？换成二次多项式核SVM后呢？分别解释。红点为+1，绿点为−1。

[题目](Questions.md#mt010) · [答案](Answers.md#mt010)

<a id="mt009"></a>
## MT009 · 十万维特征、两千样本：SVM怎样提速？

**考点：** SVM与核方法

**出处：** 2020B期中Quiz Q9，原卷第4页（10分）

### English question
Your friend is training a linear SVM on a patient data from a hospital. There are 2000 patients, and each patient has 100,000 features extracted from their time in the hospital. Your friend complains that training the linear SVM takes too long. What suggestions do you give your friend to speed up the training?

### 中文题意
医院数据有2000名患者，每人100,000维特征。朋友训练线性SVM很慢，你建议怎样提速？说明理由。

[题目](Questions.md#mt009) · [答案](Answers.md#mt009)

<a id="mt061"></a>
## MT061 · 预测内存：线性SVM与RBF SVM

**考点：** SVM与核方法

**出处：** 2023B期中 Q10，原卷第7页（10分）

### English question
Consider a binary classification problem where the input feature space is d=1,000 dimensions, and we have 2,000 training samples. Rank the following classifiers based on their memory usage (from lowest to highest) when implementing their respective prediction functions: linear SVM with C=0.1, linear SVM with C=1000, RBF kernel SVM with C=0.1, RBF kernel SVM with C=1000. Explain the reasons for your rankings.

### 中文题意
二分类输入1000维、训练样本2000条。按预测函数的内存从小到大排列：线性SVM(C=0.1)、线性SVM(C=1000)、RBF SVM(C=0.1)、RBF SVM(C=1000)。解释排序。

[题目](Questions.md#mt061) · [答案](Answers.md#mt061)

<a id="mt019"></a>
## MT019 · Ridge、LASSO与零系数

**考点：** 回归、特征选择与残差损失

**出处：** 2021A期中 Q6，原卷第3页（5分）

### English question
Which statements about linear regression are correct? (select all that apply)

A) Overfitting is more likely when you have large amount of training data.

B) Some of the weight coefficients will approach zero, but not absolutely zero, when applying very large penalty α in LASSO regression.

C) LASSO can be used for feature selection.

D) Some of the weight coefficients will approach zero, but not absolute zero, when applying very large penalty α in Ridge Regression.

E) OLS is a special case of both LASSO and Ridge regression.

### 中文题意
关于线性回归，哪些说法正确？多选。

A）训练数据越多越容易过拟合。B）LASSO的惩罚α很大时，某些系数只接近零而不会恰为零。C）LASSO可用于特征选择。D）Ridge的惩罚α很大时，某些系数接近零但通常不精确为零。E）OLS是LASSO和Ridge的特殊情形。

[题目](Questions.md#mt019) · [答案](Answers.md#mt019)

<a id="mt045"></a>
## MT045 · 特征选择：零系数、Ridge与OMP

**考点：** 回归、特征选择与残差损失

**出处：** 2023A期中 Q6，原卷第3页（5分）

### English question
Which of the following statements is correct about linear regression and feature selection? (select all that apply)?

A) Feature selection can be achieved by encouraging some linear weights to go to zero.

B) Ridge regression is effective for feature selection because it uses L2 norm to regularize the weights.

C) Orthogonal matching pursuit (OMP) can find the global optimal set of features for a given sparsity level.

D) The same set of features will always give the same set of linear weights, regardless of the features selection method used with linear regression.

E) L1 regularization is good at encouraging sparse weights because of the “corners” in its contours.

### 中文题意
关于线性回归和特征选择，哪些说法正确？多选。

A）鼓励部分权重为零可做特征选择。B）Ridge因使用L2而能有效自动选择特征。C）OMP能找到给定稀疏度下的全局最优特征集合。D）只要特征集合相同，无论选择方法如何都会得到同一组系数。E）L1等高线的尖角有利于产生稀疏权重。

[题目](Questions.md#mt045) · [答案](Answers.md#mt045)

<a id="mt030"></a>
## MT030 · L1/L2回归的益处与措辞边界

**考点：** 回归、特征选择与残差损失

**出处：** 2021B*期中 Q4，原卷第2页（5分）

### English question
What are the benefits of adding regularization terms (L1 or L2) to a linear regression model? (select all that apply)

A) Both L1 and L2 can make the regression model easier to optimize.

B) Both L1 and L2 can make the matrix inversion well-conditioned.

C) Both L1 and L2 make the regression model more robust to outliers.

D) Adding L1 or L2 term can encourage some weights to be close to zero so as to select features.

E) Both L1 and L2 can penalize the training loss of the regression model and prevent overfitting.

### 中文题意
给线性回归加L1或L2正则，哪些说法成立？多选。

A）两者都能让优化更容易。B）两者都能使矩阵求逆更良态。C）两者都使模型更抗异常值。D）两者可使某些权重接近零，从而选择特征。E）两者都可以为模型增加惩罚、抑制过拟合。

[题目](Questions.md#mt030) · [答案](Answers.md#mt030)

<a id="mt057"></a>
## MT057 · 同时使用L1与L2：Elastic Net

**考点：** 回归、特征选择与残差损失

**出处：** 2023B期中 Q6，原卷第3页（5分）；2025A期中 Q6，原卷第3页（5分）

### English question
Considering linear regression using both L1 and L2 as regularization terms:

$$
\min_{w,b}\left\{\alpha\|w\|_1+\beta\|w\|_2^2+
\sum_{i=1}^N[y_i-f(x_i)]^2\right\}.
$$

Which properties does it have? (select all that apply)

A) It treats all weights equally.

B) The penalty term focuses more on reducing large weights.

C) It has a closed-form solution.

D) It can perform feature selection and shrinkage simultaneously.

E) The elements of w are always positive.

### 中文题意
线性回归采用

$$
\min_{w,b}\left\{\alpha\|w\|_1+\beta\|w\|_2^2+
\sum_{i=1}^N[y_i-f(x_i)]^2\right\}.
$$

它有哪些性质？多选。A）对所有权重一视同仁。B）惩罚更侧重压低大权重。C）存在闭式解。D）可同时做特征选择与收缩。E）w各元素总为正。

[题目](Questions.md#mt057) · [答案](Answers.md#mt057)

<a id="mt025"></a>
## MT025 · 绝对残差损失对异常值有什么影响？

**考点：** 回归、特征选择与残差损失

**出处：** 2021A期中 Q12，原卷第4页（10分）

### English question
Consider a linear regression function $f(x)=w^Tx+b$, which is trained on the data $(x_i,y_i)$, i=1,…,N, using the following optimization problem, where the absolute prediction error is the loss function:

$$
(\hat w,\hat b)=\arg\min_{w,b}\sum_{i=1}^N|f(x_i)-y_i|.
$$

What will be the effect of using this loss during training? Why?

### 中文题意
线性回归 $f(x)=w^Tx+b$ 在N条记录上最小化

$$
(\hat w,\hat b)=\arg\min_{w,b}\sum_{i=1}^N|f(x_i)-y_i|.
$$

使用这种损失会怎样影响训练？为什么？

[题目](Questions.md#mt025) · [答案](Answers.md#mt025)

<a id="mt063"></a>
## MT063 · Huber损失：画图并解释好处

**考点：** 回归、特征选择与残差损失

**出处：** 2023B期中 Q12，原卷第9页（10分）

### English question
Consider linear regression using the Huber loss function:

$$
L(f(x_i),y_i)=
\begin{cases}
\frac12[y_i-f(x_i)]^2,&|y_i-f(x_i)|<1,\\
|y_i-f(x_i)|-\frac12,&\text{otherwise}.
\end{cases}
$$

(a) Draw a plot of the loss function.

(b) Explain one benefit of using Huber loss for linear regression.

### 中文题意
令残差 $r=y_i-f(x_i)$，线性回归使用

$$
L(r)=\begin{cases}\frac12r^2,&|r|<1,\\|r|-\frac12,&\text{otherwise}.\end{cases}
$$

(a) 画出损失函数。(b) 解释使用Huber损失的一个好处。

[题目](Questions.md#mt063) · [答案](Answers.md#mt063)

<a id="mt013"></a>
## MT013 · 残差L1＋权重L2，各自在做什么？

**考点：** 回归、特征选择与残差损失

**出处：** 2020B期中Quiz Q13，原卷第6页（10分）

### English question
Your friend has designed a new regression algorithm that minimizes the L1 norm of the error and L2 norm of the weights, given by the following optimization problem:

$$
w^*=\arg\min_w\left\{\sum_{i=1}^N|w^Tx_i-y_i|+\lambda\|w\|_2^2\right\}.
$$

What properties would you expect this regression algorithm to have? Explain why.

### 中文题意
某回归方法同时最小化残差的L1范数与权重的L2平方：

$$
w^*=\arg\min_w\left\{\sum_{i=1}^N|w^Tx_i-y_i|+\lambda\|w\|_2^2\right\}.
$$

预期它有什么性质？解释原因。

[题目](Questions.md#mt013) · [答案](Answers.md#mt013)

<a id="mt050"></a>
## MT050 · 缺车比车多更糟：设计非对称损失

**考点：** 回归、特征选择与残差损失

**出处：** 2023A期中 Q12，原卷第9页（10分）；2025A期中 Q12，原卷第9页（10分）

### English question
You are working for a bike-sharing company, and your job is to predict the number of bicycles that will be borrowed from a popular bike-sharing station each day. This prediction will be used to inform the logistics team about how many bikes should be sent to the station. The CEO tells you that it is okay to have too many bikes sent to the station, but it is not good if the station runs out of bikes, since the customers will use other bike-sharing companies.

You have a training dataset $(x_i,y_i)$, i=1,…,N, of historical data that contains feature vectors $x_i$, and number of bikes borrowed $y_i$. Consider a linear regression function $f(x)=w^Tx+b$, which is trained with the following optimization problem:

$$
(\hat w,\hat b)=\arg\min_{w,b}\sum_{i=1}^N L(f(x_i),y_i).
$$

Design a loss function that can help you to do the regression according to the requirements, and draw a plot. Explain how your loss achieves the desired requirements.

### 中文题意
预测某共享单车站每天借车量，用于调度。公司认为多放一些车可以接受，但缺车会流失顾客。给定N条特征/借车量记录，线性模型 $f(x)=w^Tx+b$ 通过最小化损失和训练。设计符合要求的损失，画图并解释。

[题目](Questions.md#mt050) · [答案](Answers.md#mt050)

<a id="mt037"></a>
## MT037 · 线性回归为何与均值预测器表现相近？

**考点：** 回归、特征选择与残差损失

**出处：** 2021B*期中 Q11，原卷第4页（10分）

### English question
Your friend wants to predict the number of taxis used in HK in one hour from various features, such as weather, time of day, day of year, etc. Your friend uses linear regression to fit the data, but finds that the mean squared error (MSE) on the validation set is about the same as a “dummy” regressor that just predicts the mean of the training data. What two pieces of advice would you give to your friend to improve their regressor? Explain why.

### 中文题意
用天气、时段、日期等特征预测香港每小时出租车使用量。线性回归在验证集上的MSE与“永远输出训练集平均值”的基线相近。提出两个改进建议，并解释原因。

[题目](Questions.md#mt037) · [答案](Answers.md#mt037)

<a id="mt006"></a>
## MT006 · Bagging与Boosting的基本区别

**考点：** 集成学习

**出处：** 2020B期中Quiz Q6，原卷第3页（5分）

### English question
Which statements are true about bagging and boosting? (select all that apply)

A) Bagging and boosting are both ensemble methods.

B) Bagging is based on iteratively building classifiers, while boosting makes the classifiers faster.

C) Bagging and boosting are only based on decision trees or decision stumps.

D) Bagging and boosting both overfit when adding too many classifiers.

E) Bagging and boosting can be combined together.

### 中文题意
关于bagging和boosting，哪些说法正确？多选。

A）二者都是集成方法。B）bagging是迭代建分类器，boosting的作用是让分类器更快。C）二者只能使用树或树桩。D）二者都会因为增加太多分类器而过拟合。E）二者可以组合。

[题目](Questions.md#mt006) · [答案](Answers.md#mt006)

<a id="mt044"></a>
## MT044 · 随机森林与Boosting的用途

**考点：** 集成学习

**出处：** 2023A期中 Q5，原卷第3页（5分）；2025A期中 Q5，原卷第3页（5分）

### English question
Which of the following is/are true about Random Forest and Boosting ensemble methods? (select all that apply)

A) An individual tree in the random forest is built on a subset of the features.

B) Random forests use learning rate as of one of its hyperparameters.

C) Both methods can be used for the regression task.

D) Random Forest is only used for regression whereas gradient boosting is only used for classification.

E) None of the above.

### 中文题意
关于随机森林与boosting，哪些说法正确？多选。

A）随机森林的单棵树基于部分特征建立。B）随机森林有学习率超参数。C）两者都可用于回归。D）RF只用于回归，gradient boosting只用于分类。E）以上均不对。

[题目](Questions.md#mt044) · [答案](Answers.md#mt044)

<a id="mt062"></a>
## MT062 · 随机森林：树多了为什么仍有共同误差？

**考点：** 集成学习

**出处：** 2023B期中 Q11，原卷第8页（10分）

### English question
For a random forest F of n trees, suppose the variance of the error of a decision tree f is $\sigma^2$, and the correlation coefficient between the errors of two trees is ρ. We will have the error variance of F as:

$$
\operatorname{var}(F)=\operatorname{var}\left(\frac1n\sum_{i=1}^nf_i\right)
=\frac{\sigma^2}{n}+\frac{n-1}{n}\rho\sigma^2.
$$

(a) Explain the relationship between the number of trees and the correlation coefficient and the ability of F to reduce overfitting.

(b) For a fixed number of trees n, explain some concrete methods to reduce the error variance of F.

### 中文题意
随机森林F由n棵树组成。每棵树误差方差为σ²，任意两棵不同树的误差相关系数均为ρ。题目给出

$$
\operatorname{Var}(F)=\frac{\sigma^2}{n}
+\frac{n-1}{n}\rho\sigma^2.
$$

(a) 树数与相关性怎样影响减少过拟合的能力？(b) 固定n时，有哪些具体降低误差方差的方法？

[题目](Questions.md#mt062) · [答案](Answers.md#mt062)

<a id="mt056"></a>
## MT056 · 集成方法：树深、并行与后续轮次

**考点：** 集成学习

**出处：** 2023B期中 Q5，原卷第3页（5分）

### English question
Which statements are true about ensemble methods? (select all that apply)

A) Using fewer decision trees with higher depth is better than using more “stumps” for weak learners in Adaboost.

B) Using linear classifiers like logistic regression for bagging is a good choice because they have low computation cost.

C) Random Forest can be parallelized in both training and testing.

D) In the Adaboost training process, once a data point is correctly classified in the weak learner ht(x), it will be neglected by the successive weak learners ht+1, ht+2, …

E) For a random forest model, increasing the number of decision trees generally helps with reduce overfitting.

### 中文题意
关于集成方法，哪些说法正确？多选。

A）AdaBoost用更少的深树一定优于更多树桩。B）LR计算便宜，所以是bagging的好选择。C）随机森林训练和预测都可以并行。D）AdaBoost中某点一旦被一轮分对，后续轮次就忽略它。E）增加RF树数通常有助于减少过拟合。

[题目](Questions.md#mt056) · [答案](Answers.md#mt056)

<a id="mt038"></a>
## MT038 · 100核部署：RF与AdaBoost如何并行预测？

**考点：** 集成学习

**出处：** 2021B*期中 Q12，原卷第4页（10分）

### English question
You are working for Tesla on their self-driving car software for their new model. Your goal is to classify objects from the radar scanner. After extensive testing, you find that AdaBoost and Random Forest classifiers both perform equally well at the task. They also both use equal amount of computation (flops). The Random Forest uses 10 trees with depth 10, while Adaboost has 100 weak learners. The new Tesla model has a special 100-core processor for running the self-driving car software. Which classifier do you recommend for implementation in the new car? Explain why.

### 中文题意
雷达目标分类中，RF与AdaBoost准确率相同、总计算量相同。RF有10棵深度10的树，AdaBoost有100个弱学习器；部署芯片有100个核心。推荐哪种？解释理由。

[题目](Questions.md#mt038) · [答案](Answers.md#mt038)

<a id="mt049"></a>
## MT049 · 在线更新AdaBoost：速度与异常值

**考点：** 集成学习

**出处：** 2023A期中 Q11，原卷第8页（10分）

### English question
You are working on an online self-driving system that employs the Adaboost model for real-time decision making. The Adaboost model will be updated with newly collected data in the real-world while the system is running, which requires the model to converge fast. (a) How would you adjust the model or hyperparameters to make this real-time system? (b) Is using Adaboost a good choice in this situation? Why or why not?

### 中文题意
自动驾驶系统用AdaBoost实时决策，运行期间还要用新采集数据更新模型，因此希望快速收敛。(a) 怎样调整模型或超参数？(b) AdaBoost是否适合这种情境？解释。

[题目](Questions.md#mt049) · [答案](Answers.md#mt049)

<a id="mt064"></a>
## MT064 · 综合题：Bagging/Boosting与Huber

**考点：** 集成学习

**出处：** 2025A期中 Q7，原卷第4页（10分）

### English question
(a) [5 marks] Explain the association and difference between boosting and bagging.

(b) [5 marks] Consider linear regression using the Huber loss function:

$$
L(f(x_i),y_i)=
\begin{cases}
\frac12[y_i-f(x_i)]^2,&|y_i-f(x_i)|<1,\\
|y_i-f(x_i)|-\frac12,&\text{otherwise}.
\end{cases}
$$

Draw a plot of the loss function and answer whether the loss is robust to outliers with reason.

### 中文题意
(a) [5分] 解释boosting与bagging的联系和区别。

(b) [5分] 线性回归使用Huber损失：当 $|y_i-f(x_i)|<1$ 时为 $\frac12[y_i-f(x_i)]^2$，否则为 $|y_i-f(x_i)|-\frac12$。画图，判断是否对异常值稳健并说明理由。

[题目](Questions.md#mt064) · [答案](Answers.md#mt064)

<a id="mt008"></a>
## MT008 · 平方形分类损失为什么惩罚“太正确”？

**考点：** 分类损失图与错误代价

**出处：** 2020B期中Quiz Q8，原卷第4页（10分）

### English question
Consider a classifier with the loss function in the below figure. Using this loss function, describe some expected properties of this classifier and explain why. Will this be a good classifier or a bad classifier? Why?

![MT008 original question figure](assets/mt008-loss.png)

### 中文题意
观察题图中的分类损失。描述使用这种损失训练的分类器会有什么性质，并解释原因。你认为它是好的还是不好的分类损失？图中横轴为 $z_i=y_i f(x_i)$。

[题目](Questions.md#mt008) · [答案](Answers.md#mt008)

<a id="mt026"></a>
## MT026 · V形损失：最优点为何在z=1？

**考点：** 分类损失图与错误代价

**出处：** 2021A期中 Q13，原卷第4页（10分）

### English question
Consider the following classification loss function. Describe the properties of the classifier learned with this loss function. Will this be a good classifier? Why or why not? Note: z = y*f(x).

![MT026 original question figure](assets/mt026-loss.png)

### 中文题意
读题图中的分类损失，描述所得分类器的性质。它是好的分类器吗？说明理由。横轴 $z=yf(x)$，图中两侧均为直线，在z=1处达到最小值。

[题目](Questions.md#mt026) · [答案](Answers.md#mt026)

<a id="mt051"></a>
## MT051 · 负间隔也零损失：分类器会放过什么？

**考点：** 分类损失图与错误代价

**出处：** 2023A期中 Q13，原卷第10页（10分）

### English question
Consider the following classification loss function. Describe the properties of the classifier learned with this loss function. Will this be a good classifier? Why or why not? Draw a figure of an example of a linear classifier trained with this loss. Note: z = y*f(x).

![MT051 original question figure](assets/mt051-loss.png)

### 中文题意
描述题图所示分类损失训练出的分类器性质，判断它是否合适并说明理由。再画一幅采用此损失的线性分类器例子。横轴 $z=yf(x)$；曲线在z=−1处降至0，之后为0。

[题目](Questions.md#mt051) · [答案](Answers.md#mt051)

<a id="mt039"></a>
## MT039 · 饱和的非凸分类损失

**考点：** 分类损失图与错误代价

**出处：** 2021B*期中 Q13，原卷第4页（10分）

### English question
Consider the following classification loss function. Describe the properties of the classifier learned with this loss function. Note: z = y*f(x).

![MT039 original question figure](assets/mt039-loss.png)

### 中文题意
描述题图所示损失训练出来的分类器会有哪些性质。横轴 $z=yf(x)$；z≥1后损失为0，向很负的z方向，曲线逐渐变平。

[题目](Questions.md#mt039) · [答案](Answers.md#mt039)

<a id="mt065"></a>
## MT065 · 比较Logistic、Hinge和Exponential损失

**考点：** 分类损失图与错误代价

**出处：** 2025A期中 Q9，原卷第6页（10分）

### English question
Logistic Regression and Support Vector Machine (SVM), and Adaboost are all commonly used classifiers.

1. What is the key difference in the optimization objective of Logistic Regression and SVM? [6 marks]

2. Given this picture, please describe the three algorithms' sensitivity to outliers in descending order, and explain why. [4 marks]

![MT065 original question figure](assets/mt065-loss-comparison.png)

*按原卷曲线重绘并去掉手写批注；保留原图中LR的相对缩放，比较以题图为准。 / Clean redraw preserving the displayed relative scaling.*

### 中文题意
Logistic Regression、SVM和AdaBoost都是常见分类器。

1. [6分] LR与SVM的优化目标主要有什么区别？
2. [4分] 根据题图，将三种算法对异常点的敏感程度从高到低排序，并解释。图中横轴为有符号分数z，负值表示错分，正值表示分对。

[题目](Questions.md#mt065) · [答案](Answers.md#mt065)

<a id="mt007"></a>
## MT007 · 筛查任务：漏诊比误报更贵

**考点：** 分类损失图与错误代价

**出处：** 2020B期中Quiz Q7，原卷第3页（10分）；2023B期中 Q13，原卷第10页（10分）

### English question
You have been asked to build a classifier for an early screening test for diagnosing cancer. After the screening test, a more expensive advanced test will be used to confirm the result. For the screening test, you are given a feature vector, and the goal is to predict whether or not the person has cancer (positive or negative). Since it is a screening test, the classifier should classify all people with cancer as positive, while it is okay for some people without cancer to be misclassified as positive. Discuss two methods for getting this desired behavior from the classifier.

### 中文题意
设计癌症早期筛查二分类器。输入是特征向量，输出阳性或阴性；阳性者还会做更昂贵的确诊检查。目标是将所有癌症患者判为阳性，不漏掉病例，允许部分健康者被误报。讨论两种达到这种偏好的方法。

[题目](Questions.md#mt007) · [答案](Answers.md#mt007)

<a id="mt023"></a>
## MT023 · 1000名受试者中只有50名阳性

**考点：** 分类损失图与错误代价

**出处：** 2021A期中 Q10，原卷第4页（10分）；2023A期中 Q10，原卷第7页（10分）

### English question
You are working for a hospital to build a classifier as a cost-effective screening test for a lung disease based on the patient’s demographic data and saliva sample. If the classifier predicts positive, then the patient will do a follow-up CT scan that is more costly and very accurate. You have collected a dataset of 1000 patients, of which 50 have the lung disease. What are the key issues to consider when training and testing your classifier? How do you address these key issues during training and testing?

### 中文题意
医院用人口信息和唾液样本做肺病筛查，阳性者再做更贵且准确的CT。数据共1000人，50人患病。训练和测试应考虑哪些关键问题？怎样处理？

[题目](Questions.md#mt023) · [答案](Answers.md#mt023)

<a id="mt035"></a>
## MT035 · 正常邮件被大量拦截怎么办？

**考点：** 分类损失图与错误代价

**出处：** 2021B*期中 Q9，原卷第4页（10分）

### English question
You have been asked to build a classifier for detecting junk email. You are given a training dataset, which has more junk email than regular email. You trained the model with logistic regression. However, your classification model predicts most emails as spam, so that you will hardly receive any email at all. What are two approaches to fix this problem? Give reasons why these approaches will work.

### 中文题意
邮件分类训练集中垃圾邮件多于正常邮件。逻辑回归把大多数邮件都判成垃圾，几乎收不到邮件。提出两种修复方法并说明理由。

[题目](Questions.md#mt035) · [答案](Answers.md#mt035)

<a id="mt067"></a>
## MT067 · 链式求导与两层网络反传

**考点：** 神经网络与链式法则

**出处：** 2025A期中 Q13，原卷第10页（10分）

### English question
(a) Warm-up question (you need to give detailed steps; you may define intermediate variables accordingly): calculate the derivative of y with respect to x using the chain rule.

$$
y=\left(1+e^{\sqrt[3]{3x^2}+\tan(5x)}\right)^{-1}.
$$

(b) Please first explain the forward process with respect to the graph below and then calculate

$$
\frac{\partial L}{\partial a_i},\qquad
\frac{\partial L}{\partial g_1},\qquad
\frac{\partial L}{\partial w_j}.
$$

Hint: $A\in\mathbb R^{m\times m}$ and $W\in\mathbb R^{m\times n}$ are matrices; $a_i$ and $w_j$ are general representations of each weight vector in A and W, respectively. For $g_1\to z$ and $g_2\to f$, any proper functions are fine.

![MT067 original question figure](assets/mt067-network.png)

*按原卷印刷计算图重绘；去除了学生手写梯度及批改，保留所有前向节点与参数箭头。 / Redrawn from the printed graph, preserving its nodes and parameter arrows.*

### 中文题意
(a) 用链式法则求下式对x的导数，给出详细步骤，可定义中间变量：

$$
y=\left(1+e^{\sqrt[3]{3x^2}+\tan(5x)}\right)^{-1}.
$$

(b) 解释题图的前向过程，然后求 $\partial L/\partial a_i$、$\partial L/\partial g_1$ 和 $\partial L/\partial w_j$。题设 $A\in\mathbb R^{m\times m}$、$W\in\mathbb R^{m\times n}$；$a_i,w_j$分别表示相应矩阵中的权重向量。允许为 $g_1\to z$、$g_2\to f$ 选择合适函数。

[题目](Questions.md#mt067) · [答案](Answers.md#mt067)

<a id="mt066"></a>
## MT066 · 梯度消失：为什么深度和激活函数有关？

**考点：** 神经网络与链式法则

**出处：** 2025A期中 Q10，原卷第7页（10分）

### English question
(a) [4 marks] Explain what is the “vanishing gradient” problem.

(b) [3 marks] Explain mathematically why “deeper” networks are more prone to this problem. You may use equations or a mathematical description.

(c) [3 marks] Compared with the Sigmoid activation function, why can the ReLU activation function alleviate this problem?

### 中文题意
(a) [4分] 解释梯度消失问题。(b) [3分] 用数学说明为什么更深网络更容易出现这个问题。(c) [3分] 相比Sigmoid，ReLU为什么能缓解它？

[题目](Questions.md#mt066) · [答案](Answers.md#mt066)

<a id="mt003"></a>
## MT003 · 历史拓展：Gaussian Process的假设

**考点：** 历史范围拓展：Gaussian Process

**出处：** 2020B期中Quiz Q3，原卷第2页（5分）

历史期中原题；需要高斯过程背景，不作为当前Lecture 1–5已完整讲授的内容。

### English question
Which statements about Gaussian Process regression (GPR) are correct? (select all that apply)

A) GPR is defined as the Bayesian linear regression whose linear kernel is replaced by the Gaussian/RBF kernel.

B) GPR only has a closed form solution when the observation noise is Gaussian.

C) One assumption in the Gaussian process prior is that two function values are more correlated when the corresponding inputs are close together.

D) The reason why GPR is not good for large datasets is that it only has a few parameters and thus limited model complexity.

E) GPR assumes the input data points are i.i.d. (independently and identically distributed).

### 中文题意
关于高斯过程回归GPR，哪些说法正确？多选。

A）GPR被定义为：将贝叶斯线性回归的线性核换成Gaussian/RBF核。B）只有观测噪声为高斯时，GPR才有闭式解。C）高斯过程先验的一个假设是，输入越近，对应函数值的相关性越高。D）GPR不适合大数据是因为参数少、模型复杂度有限。E）GPR假设输入数据点独立同分布。

[题目](Questions.md#mt003) · [答案](Answers.md#mt003)

<a id="mt036"></a>
## MT036 · 历史拓展：音乐地理回归，GP还是RF？

**考点：** 历史范围拓展：Gaussian Process

**出处：** 2021B*期中 Q10，原卷第4页（10分）

历史期中原题；GPR属于本轮讲义主线之外的背景。

### English question
Geographical origins of music are related to the audio features in music. Suppose we have 10,597 music segments from different regions of the world, where each audio segment is represented by a 68-dimensional vector, and the region is denoted by latitude and longitude coordinates. We know there are some outliers in the dataset and some regions have apparently more music data than others. Suppose we want to choose Gaussian process regression or random forest regression to predict the region coordinates from the audio feature vector. For this specific regression task, what are the advantages and disadvantages of using these Gaussian process regression or random forest regression?

### 中文题意
共有10,597段世界各地音乐，每段68维音频特征，目标是经纬度。存在异常值，且部分地区样本远多于其他地区。比较Gaussian Process Regression与Random Forest Regression在这个任务中的优缺点。

[题目](Questions.md#mt036) · [答案](Answers.md#mt036)
