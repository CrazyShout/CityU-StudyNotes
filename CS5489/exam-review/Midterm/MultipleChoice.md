<!-- Generated from Questions.md and Answers.md by tools/assemble_compact.py. -->
# CS5489 · 期中选择题与答案 / Multiple-Select Questions and Answers

30题：完整英文原题、中文题意、英文答案及中文对应答案。保留必要题图、作答图和成立条件，不收录详细解析。

均为多选；MT001、MT014、MT029要求选择不正确的选项，另标“选错”。

沿用MT编号和组内顺序，目录与原卷索引使用本册页码。Gaussian Process题仍为历史拓展。

## 目录

**学习流程与模型诊断**

- [MT004 · CV选完参数后，为什么还要重新训练？〔多选〕](#mt004)
- [MT028 · 训练误差低、测试误差高：可能原因〔多选〕](#mt028)
- [MT002 · 训练准、测试差：哪些改进值得尝试？〔多选〕](#mt002)

**Bayes、Naive Bayes与模型比较**

- [MT040 · Bayes规则和Naive Bayes的关系〔多选〕](#mt040)
- [MT052 · 生成式分类器学了什么〔多选〕](#mt052)
- [MT015 · NB的最优性、独立性与边界〔多选〕](#mt015)
- [MT032 · Bayesian classifier的性质〔多选〕](#mt032)
- [MT005 · NB的学习、不确定性和正则化〔多选〕](#mt005)
- [MT014 · 生成式与判别式的区别〔多选·选错〕](#mt014)
- [MT017 · 哪些模型能产生不同形状的边界〔多选〕](#mt017)
- [MT027 · 连续特征能否使用NB：混合选择题〔多选〕](#mt027)

**逻辑回归与参数正则**

- [MT041 · Logistic的概率、多分类与最优解〔多选〕](#mt041)
- [MT018 · 为什么在线性分类器上加L2？〔多选〕](#mt018)
- [MT001 · Logistic训练：哪些说法不成立？〔多选·选错〕](#mt001)
- [MT053 · LR与生成式模型：混合选择题〔多选〕](#mt053)

**SVM与核方法**

- [MT042 · SVM的基本特点〔多选〕](#mt042)
- [MT016 · 核SVM：变换、存储与非向量输入〔多选〕](#mt016)
- [MT031 · RBF距离与带宽：看近点和远点〔多选〕](#mt031)
- [MT055 · 判断五个候选核是否合法〔多选〕](#mt055)
- [MT054 · C、支持向量与RBF的零训练误差〔多选〕](#mt054)
- [MT043 · 核SVM怎样处理非线性？〔多选〕](#mt043)
- [MT029 · 哪些SVM说法错误？〔多选·选错〕](#mt029)

**回归、特征选择与残差损失**

- [MT019 · Ridge、LASSO与零系数〔多选〕](#mt019)
- [MT045 · 特征选择：零系数、Ridge与OMP〔多选〕](#mt045)
- [MT030 · L1/L2回归的益处与措辞边界〔多选〕](#mt030)
- [MT057 · 同时使用L1与L2：Elastic Net〔多选〕](#mt057)

**集成学习**

- [MT006 · Bagging与Boosting的基本区别〔多选〕](#mt006)
- [MT044 · 随机森林与Boosting的用途〔多选〕](#mt044)
- [MT056 · 集成方法：树深、并行与后续轮次〔多选〕](#mt056)

**历史范围拓展：Gaussian Process**

- [MT003 · 历史拓展：Gaussian Process的假设〔多选〕](#mt003)

<a id="mt004"></a>
## MT004 · CV选完参数后，为什么还要重新训练？

**题型：** 选择题（多选） / Multiple select

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

### English answer
**A, C and D.** Validation folds come from the training pool; the final test set is not used for tuning. After selecting C, refit on all training data, so coefficients can differ from fold-specific coefficients. A coarse candidate grid may miss a useful value, although poor test performance can have other causes.

### 中文对应答案
**A、C、D正确。** 验证折来自训练数据，最终测试集不用来调参。选定C后，要用全部训练数据重新拟合，因此得到的系数可能与各折训练出的系数不同。候选参数之间的间隔太大，可能漏掉合适的值；不过，测试表现差也可能有其他原因。

<a id="mt028"></a>
## MT028 · 训练误差低、测试误差高：可能原因

**题型：** 选择题（多选） / Multiple select

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

### English answer
**A, C and D.** Too little representative training data and excessive flexibility can cause overfitting; distribution shift can also cause a gap. A large test set does not itself worsen the expected generalization error. “Too weak” normally manifests as poor training fit as well, so E is not the intended explanation for the stated pattern.

### 中文对应答案
**A、C、D正确。** 有代表性的训练数据太少，或模型过于灵活，都可能导致过拟合；训练与测试的数据分布不同，也可能造成误差差距。测试集大本身不会增大预期泛化误差。模型“太弱”通常也会表现为训练拟合差，因此E不是题述现象所指的原因。

<a id="mt002"></a>
## MT002 · 训练准、测试差：哪些改进值得尝试？

**题型：** 选择题（多选） / Multiple select

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

### English answer
**C, D and E** are reasonable candidates. Stronger regularization can reduce excessive fitting; training-only cross-validation selects complexity; bagging can reduce the variance of unstable learners. These are possible remedies, not guaranteed improvements. Also check distribution shift and preprocessing differences.

### 中文对应答案
**C、D、E是合理的候选办法。** 加强正则化可以减轻过度拟合；在训练数据内部做交叉验证可以选择复杂度；bagging可以降低不稳定模型的方差。这些办法可能有效，但不保证一定改善表现。同时还应检查训练与测试的数据分布、预处理是否存在差异。

<a id="mt040"></a>
<a id="l2q05"></a>
## MT040 · Bayes规则和Naive Bayes的关系

**题型：** 选择题（多选） / Multiple select

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

A）NB是Bayes决策规则的一种具体实现。B）对特征为$x$、标签为$y\in\{0,1\}$的二分类任务，按Bayes决策规则，只要$p(x\mid y=0)>p(x\mid y=1)$，就选择类0。C）NB对各特征维独立建模。D）Bayes决策规则比NB计算更高效。E）Bayes决策规则只能用于二分类。

### English answer
**A and C.** C means independence **conditional on the class**. NB specifies class-conditional models and then applies the Bayes decision rule. B omits the priors: compare $p(x\mid c)p(c)$ under equal error costs. D compares a decision principle with a particular implementation; efficiency depends on the model. The rule applies to any finite number of classes, so E is false.

### 中文对应答案
**A、C正确。** C中的独立是指**给定类别后的条件独立**。NB先指定类条件模型，再应用Bayes决策规则。B漏掉了先验：错分代价相同时，应比较$p(x\mid c)p(c)$。D把一种决策原则与一种具体实现作效率比较，而计算效率取决于所用模型。该规则适用于任意有限个类别，所以E错误。

<a id="mt052"></a>
<a id="l2q01"></a>
## MT052 · 生成式分类器学了什么

**题型：** 选择题（多选） / Multiple select

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

### English answer
**A and D.** A generative classifier models $p(x\mid c)$ and the class prior $p(c)$. It predicts using $p(c\mid x)\propto p(x\mid c)p(c)$, so maximizing only the class-conditional density is generally insufficient. Priors can encode prior information, and the construction extends to multiple classes.

### 中文对应答案
**A、D正确。** 生成式分类器对类条件分布$p(x\mid c)$和类别先验$p(c)$建模，再利用$p(c\mid x)\propto p(x\mid c)p(c)$预测。因此，一般不能只选择类条件密度最大的类别。先验可以表达已有信息，这种建模方式也适用于多分类。

<a id="mt015"></a>
<a id="l2q08"></a>
## MT015 · NB的最优性、独立性与边界

**题型：** 选择题（多选） / Multiple select

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

### English answer
**A, C and E in the supplied key.** Under equal error costs, choosing a class with maximal true posterior minimizes classification error. Correct posterior estimates are sufficient, but not necessary if the maximizing class is unchanged. NB learns priors and class-conditional distributions; their choice affects accuracy. Independent features do not force axis-aligned decision boundaries, and fitted NB models can overfit.

### 中文对应答案
**随卷答案选A、C、E。** 错分代价相同时，选择真实后验概率最大的类别，可以使分类错误率最低。后验估计正确是充分条件；只要后验最大的类别没有改变，就不必要求估计值完全正确。NB学习先验和类条件分布，所选分布会影响准确率。特征独立不意味着决策边界一定与坐标轴平行；拟合出的NB模型也可能过拟合。

<a id="mt032"></a>
<a id="l2q06"></a>
## MT032 · Bayesian classifier的性质

**题型：** 选择题（多选） / Multiple select

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

### English answer
**The supplied answer key selects D.** The Bayes rule minimizes conditional error under equal misclassification costs when it uses the true posterior. A fitted model need not achieve this optimum if its probability estimates are wrong.

A, C and E are false: Gaussian NB may have quadratic boundaries, fitted distributions can overfit, and priors influence posterior scores. B is ambiguous. In the course's generative/discriminative distinction, a generative model directly specifies $p(x\mid y)$ and $p(y)$, and **derives** $p(y\mid x)$; it does not directly parameterize the conditional classifier.

### 中文对应答案
**随卷答案选D。** 错分代价相同时，使用真实后验的Bayes规则能使给定输入下的错误率最低。若拟合模型的概率估计有误，就未必能达到这个最优值。

A、C、E错误：Gaussian NB可能产生二次边界；拟合的分布可能过拟合；先验会影响后验分数。B有歧义。按课程对生成式与判别式的区分，生成式模型直接指定$p(x\mid y)$和$p(y)$，再**推导出**$p(y\mid x)$，并非直接为这个条件分类模型设定参数。

<a id="mt005"></a>
<a id="l2q07"></a>
## MT005 · NB的学习、不确定性和正则化

**题型：** 选择题（多选） / Multiple select

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

### English answer
**The supplied key selects A, B, C and D.** NB estimates priors and class-conditional distributions, then derives posteriors. For binary $Y\in\{0,1\}$, let $p=P(Y=1\mid x)$. Then $\operatorname{Var}(Y\mid x)=p(1-p)$ is largest at $p=1/2$, the usual equal-cost decision boundary. Non-Gaussian NB can be nonlinear, and NB/LR can use MLE. E is false because smoothing regularizes NB. A describes the resulting posterior, not direct discriminative training.

### 中文对应答案
**随卷答案选A、B、C、D。** NB先估计先验和类条件分布，再推导后验。对二分类标签$Y\in\{0,1\}$，令$p=P(Y=1\mid x)$，则$\operatorname{Var}(Y\mid x)=p(1-p)$在$p=1/2$时最大；这对应通常的等错分代价决策边界。非高斯的NB可以产生非线性边界，NB和逻辑回归都可以用最大似然估计训练。E错误，因为平滑可以对NB起到正则化作用。A描述的是最终得到的后验，并不表示NB直接采用判别式训练。

<a id="mt014"></a>
<a id="l2q03"></a>
## MT014 · 生成式与判别式的区别

**题型：** 选择题（多选） / Multiple select · 选不正确项 / Select incorrect statements

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

### English answer
**A, C and D are incorrect.** A new feature requires learning its class-conditional behaviour; a full joint model may also require new dependency parameters. Standard supervised discriminative training requires labels. Gaussian distributions are useful assumptions, not universally superior choices. B and E follow the course's generative/discriminative distinction.

### 中文对应答案
**A、C、D错误。** 加入新特征后，需要学习它在各类别下的分布；若使用完整联合模型，还可能需要学习新的依赖关系参数。标准的有监督判别式训练需要标签。高斯分布是一种有用的建模假设，但并非对所有任务都更好。B、E符合课程对生成式与判别式模型的区分。

<a id="mt017"></a>
<a id="l2q11"></a>
## MT017 · 哪些模型能产生不同形状的边界

**题型：** 选择题（多选） / Multiple select

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

### English answer
**A, B and C in the supplied key.** For Gaussian NB, shared class variances cancel the quadratic terms, giving a linear boundary; class-dependent variances generally leave quadratic terms. RBF SVMs and stump ensembles can represent simple separating surfaces as well as nonlinear ones.

D uses a **homogeneous** degree-2 kernel: its explicit features contain quadratic products, but no first-order terms. It does not supply the general affine boundary family. Do not replace it with $(x^Tx'+1)^2$, which is a different kernel. E remains linear in the given features; changing the regularization strength does not introduce nonlinear features.

### 中文对应答案
**随卷答案选A、B、C。** 对Gaussian NB，类间共享方差会使二次项抵消，得到线性边界；不同类别使用不同方差时，通常会留下二次项。RBF SVM和决策树桩集成既能表示简单的分隔面，也能表示非线性分隔面。

D使用的是**齐次二次核**：展开后的特征包含二次乘积，但没有一次项，因此不能覆盖一般的仿射边界。不能把它替换成$(x^Tx'+1)^2$，那是另一个核。E在给定特征上仍是线性的，改变正则化强度不会引入非线性特征。

<a id="mt027"></a>
<a id="l2q10"></a>
## MT027 · 连续特征能否使用NB：混合选择题

**题型：** 选择题（多选） / Multiple select

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

### English answer
**B and E in the supplied key.** D is false: Gaussian NB explicitly models continuous features with Gaussian densities.

A refers to the standard binary SVM taught in the course; multiclass wrappers or multiclass SVM formulations are separate constructions. B assumes logistic regression on the given, untransformed feature vector. C is too strong: scaling is often helpful, especially with regularization, but is not a mathematical prerequisite. E follows from the sparsity encouraged by the L1 penalty.

### 中文对应答案
**随卷答案选B、E。** D错误：Gaussian NB就是用高斯密度对连续特征建模的。

A指课程所讲的标准二分类SVM；要处理多分类，需要另外组合多个分类器，或采用多分类SVM形式。B假设逻辑回归直接使用给定、未经变换的特征向量。C说得过强：特征缩放通常有帮助，尤其是在加入正则化时，但它不是数学上的必要前提。E成立，是因为L1惩罚鼓励稀疏系数。

<a id="mt041"></a>
## MT041 · Logistic的概率、多分类与最优解

**题型：** 选择题（多选） / Multiple select

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

### English answer
**B and D.** Binary logistic regression models a conditional class probability through sigmoid. OvR with three classes fits three class-versus-rest classifiers. The probability is not computed by A's likelihood/prior division, and convexity does not guarantee a unique finite optimum for every dataset.

### 中文对应答案
**B、D正确。** 二分类逻辑回归通过sigmoid建模类别的条件概率。三分类的一对其余（OvR）方法训练三个“本类与其余类”的分类器。类别概率不是按A中的“似然除以先验”计算的；目标函数具有凸性，也不保证每个数据集都有唯一且有限的最优解。

<a id="mt018"></a>
## MT018 · 为什么在线性分类器上加L2？

**题型：** 选择题（多选） / Multiple select

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

### English answer
The course answer is **B and D**. L2 penalizes large weights and can reduce overfitting; a zero-mean Gaussian weight prior gives a quadratic penalty under MAP. In the normalized SVM formulation, minimizing the weight norm increases the geometric margin. A and E contradict the penalty's direct effect.

### 中文对应答案
课程答案为**B、D**。L2惩罚大权重，可以减轻过拟合；在最大后验估计（MAP）中，零均值高斯权重先验会产生二次惩罚。在规范化的SVM形式下，减小权重范数会增大几何间隔。A、E与这一惩罚的直接作用相反。

<a id="mt001"></a>
## MT001 · Logistic训练：哪些说法不成立？

**题型：** 选择题（多选） / Multiple select · 选不正确项 / Select incorrect statements

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

### English answer
The supplied key selects **B and C**. A fixed learning rate is not necessary; increasing C weakens the usual penalty and does not guarantee the stated changes in either error. Training may use sigmoid probabilities while prediction thresholds the score, making D valid. **A needs an additional qualification:** convexity rules out inferior local minima, but alone does not guarantee a unique finite minimizer.

### 中文对应答案
随卷答案选**B、C**。学习率不必固定；在常用约定下，增大C会减弱正则惩罚，但不能保证训练误差和测试误差一定按选项所说的方向变化。训练时可以使用sigmoid概率，预测时则对分数设阈值，因此D成立。**A还需要补充条件：** 凸性排除了比全局最优解更差的局部最小点，但仅凭凸性，不能保证存在唯一且有限的最小点。

<a id="mt053"></a>
<a id="l2q14"></a>
## MT053 · LR与生成式模型：混合选择题

**题型：** 选择题（多选） / Multiple select

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

### English answer
**B, C and D.** Logistic regression models $P(y\mid x)$ directly, whereas a generative classifier models $p(x\mid y)$ and $P(y)$ and derives $P(y\mid x)$ using Bayes' rule. Gaussian parameter priors correspond to L2 penalties in MAP training. Cross-validation can select their strength.

A is false for general logistic regression; numerical optimization is required. E is false because the penalty changes the optimized coefficients, typically shrinking their magnitudes.

### 中文对应答案
**B、C、D正确。** 逻辑回归直接建模$P(y\mid x)$；生成式分类器则先建模$p(x\mid y)$和$P(y)$，再通过Bayes规则推导$P(y\mid x)$。MAP训练中的高斯参数先验对应L2惩罚，可以通过交叉验证选择其强度。

A错误：一般的逻辑回归需要数值优化。E错误：惩罚项会改变优化得到的系数，通常会缩小它们的绝对值。

<a id="mt042"></a>
## MT042 · SVM的基本特点

**题型：** 选择题（多选） / Multiple select

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

### English answer
The supplied 2023A key selects **A and B**. Slack variables allow violations, and margin maximization is central to the objective. D and E are false. C is context-dependent: hard-margin or heavily penalized soft-margin SVMs can be sensitive to outliers, whereas the degree of sensitivity depends on C, the kernel and contamination; the bare statement is too broad to treat as a universal characteristic.

### 中文对应答案
2023A随卷答案选**A、B**。松弛变量允许样本违反间隔约束，最大化间隔是SVM目标的核心。D、E错误。C是否成立取决于具体设置：硬间隔SVM或对违反约束惩罚很重的软间隔SVM，可能对异常值敏感；敏感程度取决于C、核以及数据受到异常值影响的情况，不能把这句话当作所有SVM的普遍特点。

<a id="mt016"></a>
## MT016 · 核SVM：变换、存储与非向量输入

**题型：** 选择题（多选） / Multiple select

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

### English answer
**A, D and E**, with E interpreted as possible savings in memory and computation relative to explicitly constructing the feature map and taking its inner products. Nonlinear kernel prediction normally retains support vectors and coefficients, so B is false. A valid real kernel must produce symmetric positive-semidefinite Gram matrices, not merely positive entries.

### 中文对应答案
**A、D、E正确**，其中E应理解为：相对于显式构造特征映射再求内积，核技巧有可能节省内存与计算。非线性核模型在预测时通常仍要保存支持向量及其系数，因此B错误。合法的实值核必须产生对称、半正定的Gram矩阵，不能仅要求各个元素为正。

<a id="mt031"></a>
## MT031 · RBF距离与带宽：看近点和远点

**题型：** 选择题（多选） / Multiple select

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

### English answer
**A, B, C and E as printed.** For distinct points, both RBF similarities approach 1 as γ→0⁺ and 0 as γ→∞. The nearer point always has higher similarity, proving C and E. D fails: near similarity can be close to 1 while far similarity is not. The supplied key omits the true printed option C.

### 中文对应答案
**按印刷题面，A、B、C、E正确。** 对不同的点，当$\gamma\to0^+$时，两种RBF相似度都趋于1；当$\gamma\to\infty$时，都趋于0。近点的相似度始终高于远点，因此C、E成立。D不成立：近点的相似度可以接近1，而远点的相似度仍不接近1。随卷答案漏选了印刷题面中正确的C。

**原题差异 / Source note：** 配套答案列A、B、E；题纸的≥使C也成立，本解按题纸补C。 / The supplied key omits C, which is true as printed.

<a id="mt055"></a>
## MT055 · 判断五个候选核是否合法

**题型：** 选择题（多选） / Multiple select

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

### English answer
**A and B**, on appropriate domains. A is the inner product of normalized nonzero inputs. For B, assuming the integrals exist, any coefficients aᵢ give

$$
\sum_{i,j}a_i a_j k(x_i,x_j)
=\int\left[\sum_i a_i p(x_i\mid z)\right]^2p(z)\,dz\ge0.
$$

C fails on one-dimensional inputs 0 and 2: its Gram matrix is [[1,1],[1,0]], with negative determinant. D can have a negative diagonal, e.g. x=√(3π/2). For E, inputs 1 and 2 and coefficients (1,−1) give tanh(1)+tanh(4)−2tanh(2)≈−0.1671<0. Thus C–E are not valid on all real inputs.

### 中文对应答案
**在适当的定义域上，A、B合法。** A是非零输入归一化之后的内积。对B，假设相关积分存在，则任意系数$a_i$都满足

$$
\sum_{i,j}a_i a_j k(x_i,x_j)
=\int\left[\sum_i a_i p(x_i\mid z)\right]^2p(z)\,dz\ge0.
$$

C有反例：取一维输入0和2，Gram矩阵为$\begin{pmatrix}1&1\\1&0\end{pmatrix}$，行列式为负。D的对角元素可能为负，例如取$x=\sqrt{3\pi/2}$。对E，取输入1、2及系数$(1,-1)$，得到$\tanh(1)+\tanh(4)-2\tanh(2)\approx-0.1671<0$。因此，C、D、E都不能在所有实数输入上作为合法核。

<a id="mt054"></a>
## MT054 · C、支持向量与RBF的零训练误差

**题型：** 选择题（多选） / Multiple select

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

### English answer
The supplied key is **A, D and E**, but **E requires qualification**. For distinct finite inputs, an RBF kernel with positive bandwidth parameter permits interpolation in its feature space, and sufficiently strong fitting can achieve zero training error. Duplicate inputs with conflicting labels cannot be separated by any deterministic classifier, and an arbitrary finite C need not fit all labels. A refers to the separable hard-margin limit; B and C have no such guarantee.

### 中文对应答案
随卷答案为**A、D、E**，但**E需要加条件**。对于有限个互不相同的输入，带宽参数为正的RBF核允许在特征空间中插值；足够强地拟合数据时，可以达到零训练误差。若相同输入对应相互冲突的标签，任何确定性分类器都不能把它们分开；任意给定的有限C也不保证能拟合所有标签。A指可分数据的硬间隔极限；B、C没有相应保证。

<a id="mt043"></a>
## MT043 · 核SVM怎样处理非线性？

**题型：** 选择题（多选） / Multiple select

**考点：** SVM与核方法

**出处：** 2023A期中 Q4，原卷第3页（5分）；2025A期中 Q4，原卷第2页（5分）

*题头差异：2023A含“kernel”，2025A省略该词；以下采用2023A题头，两卷选项相同。 / The 2023A heading is used below; the 2025A heading omits “kernel”. The options are identical.*

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

### English answer
The supplied key is **B and D**. Interpret D as optimizing sample multipliers, whose nonzero values identify support vectors—not selecting them in advance. A is ambiguous under the kernel-SVM heading: nonlinear kernels can model nonlinear boundaries, whereas soft-margin tolerance alone does not make a linear SVM nonlinear. The supplied key nevertheless omits A. A feature-space reformulation does not automatically guarantee efficiency. The kernel trick avoids explicit feature construction, contrary to E's wording.

### 中文对应答案
随卷答案为**B、D**。D应理解为优化各样本的乘子，其中非零乘子对应支持向量，而不是提前选出支持向量。A放在“核SVM”题目下有歧义：非线性核能产生非线性边界，但仅靠软间隔允许违反约束，并不能让线性SVM变成非线性模型；随卷答案仍未选A。改写到特征空间并不自动保证计算更高效。核技巧避免显式构造特征，这与E的表述相反。

<a id="mt029"></a>
## MT029 · 哪些SVM说法错误？

**题型：** 选择题（多选） / Multiple select · 选不正确项 / Select incorrect statements

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

### English answer
**A, D and E** are the intended incorrect statements. Kernel models can also fit linearly separable data, and valid kernels can be defined on strings or sets. Support vectors are identified during fitting; training does not start by knowing which examples can be discarded. B is an informal description: nonzero dual coefficients define predictive support, and points outside the SVR tube can also be support vectors.

### 中文对应答案
本题预期的错误选项为**A、D、E**。核模型也可以拟合线性可分数据，合法核也可以定义在字符串或集合上。支持向量是在拟合过程中确定的，训练开始时并不知道哪些样本可以丢弃。B只是概括说法：预测中起作用的是非零对偶系数对应的样本，SVR容忍管道之外的点也可能是支持向量。

<a id="mt019"></a>
## MT019 · Ridge、LASSO与零系数

**题型：** 选择题（多选） / Multiple select

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

A）训练数据越多越容易过拟合。B）LASSO的惩罚α很大时，某些系数只接近零而不会恰为零。C）LASSO可用于特征选择。D）Ridge的惩罚α很大时，某些系数会接近零，但不会恰好为零。E）OLS是LASSO和Ridge的特殊情形。

### English answer
**C, D and E** under the usual interpretation. LASSO can produce exact zeros; ridge generally shrinks coefficients continuously. Setting the penalty to zero recovers the OLS objective. A is not a general relationship. D describes typical ridge behaviour, not a theorem that a ridge coefficient can never equal zero.

### 中文对应答案
**按通常的理解，C、D、E正确。** LASSO能使部分系数恰好为0；ridge通常连续地缩小系数。把惩罚强度设为0，就恢复普通最小二乘（OLS）的目标。A不是一般成立的关系。D描述的是ridge的典型行为，并不是说ridge系数在任何情况下都不可能为0。

<a id="mt045"></a>
## MT045 · 特征选择：零系数、Ridge与OMP

**题型：** 选择题（多选） / Multiple select

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

### English answer
**A and E.** A zero coefficient removes that feature's direct contribution; L1 geometry promotes such solutions. Ridge usually shrinks rather than exactly eliminates coefficients. OMP is greedy, not a general solver for the globally best subset. Different penalties/objectives can yield different weights even with the same feature list.

### 中文对应答案
**A、E正确。** 某个特征的系数为0，就去掉了它对预测的直接贡献；L1约束的几何形状有利于出现这类解。Ridge通常缩小系数，而不是让系数恰好为0。OMP采用贪心选择，不能一般性地求出全局最优的特征子集。即使使用相同的特征列表，不同的惩罚或目标函数也可能得到不同的权重。

<a id="mt030"></a>
## MT030 · L1/L2回归的益处与措辞边界

**题型：** 选择题（多选） / Multiple select

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

### English answer
The supplied key selects **D and E**. Read D carefully: both can shrink coefficients, but **automatic exact-zero selection is characteristic of L1**, not ordinary ridge. E describes a possible generalization benefit, not a guarantee. L2 can improve a least-squares system's conditioning; L1 is nonsmooth and does not provide the same inverse-matrix argument. Weight regularization alone is not a robust residual loss.

### 中文对应答案
随卷答案选**D、E**。D需要谨慎理解：两者都能缩小系数，但**自动产生恰好为0的系数是L1的特点**，并非普通ridge的特点。E说的是可能改善泛化，并不保证一定改善。L2可以改善最小二乘系统的条件数，使求解更稳定；L1不光滑，不能套用同样的矩阵求逆论证。仅对权重加正则，并不等于采用了对异常残差稳健的损失。

<a id="mt057"></a>
## MT057 · 同时使用L1与L2：Elastic Net

**题型：** 选择题（多选） / Multiple select

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

### English answer
**B and D in the supplied key.** L1 encourages exact zeros; L2 shrinks large weights. General Elastic Net requires numerical optimization, though special cases have explicit solutions. The same α and β are applied to every weight, but different weight magnitudes incur different penalties. Negative weights are allowed.

### 中文对应答案
**随卷答案选B、D。** L1鼓励系数恰好为0，L2抑制大权重。一般的Elastic Net需要数值优化，但特殊情形可以有显式解。各个权重都使用相同的α和β，但大小不同的权重受到的惩罚不同。权重可以为负。

<a id="mt006"></a>
## MT006 · Bagging与Boosting的基本区别

**题型：** 选择题（多选） / Multiple select

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

### English answer
**A and E.** Bagging aggregates learners fitted to resampled data; boosting builds learners sequentially to address the current ensemble's errors or weighted loss. Neither is restricted in principle to trees. More learners do not universally cause overfitting, and boosting does not mean computational acceleration.

### 中文对应答案
**A、E正确。** Bagging汇总在重采样数据上训练出的多个模型；boosting则依次训练模型，针对当前集成的错误或加权损失进行改进。两者原则上都不限于使用决策树。模型数量增加不一定导致过拟合，boosting也不表示计算加速。

<a id="mt044"></a>
## MT044 · 随机森林与Boosting的用途

**题型：** 选择题（多选） / Multiple select

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

### English answer
The course key selects **A and C**. Random forests use randomized feature candidates in their usual construction, and both ensemble families support regression as well as classification. Ordinary random forests do not use the boosting learning-rate parameter. A should not be read as requiring one permanently fixed feature subset for every split of a tree; feature sampling is commonly performed at each node.

### 中文对应答案
课程答案选**A、C**。随机森林的通常构造会随机选取候选特征；两类集成方法都可以用于回归和分类。普通随机森林不使用boosting中的学习率参数。A不能理解为一棵树的所有分裂都必须使用同一个固定特征子集；常见做法是在每个节点重新抽取候选特征。

<a id="mt056"></a>
## MT056 · 集成方法：树深、并行与后续轮次

**题型：** 选择题（多选） / Multiple select

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

### English answer
The supplied key selects **C and E**. Trees can be fitted and evaluated independently before aggregation. Averaging more randomized trees reduces finite-ensemble variance toward a correlation-dependent limit. There is no universal superiority in A; bagging benefits most from unstable/high-variance learners, so low cost alone does not establish B. Correctly classified AdaBoost samples may receive lower relative weight but are not permanently removed.

### 中文对应答案
随卷答案选**C、E**。各棵树可以独立训练和预测，之后再汇总结果。把更多随机树的输出取平均，可以降低集成的方差，但仍有一个由树间相关性决定的下限。A中的普遍优越性不成立；bagging主要有利于不稳定、方差高的模型，不能仅凭计算成本低就认定B成立。AdaBoost中已分类正确的样本，其相对权重可能降低，但不会被永久移除。

<a id="mt003"></a>
## MT003 · 历史拓展：Gaussian Process的假设

**题型：** 选择题（多选） / Multiple select

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

### English answer
**B and C under the course’s Gaussian-likelihood and RBF-kernel assumptions.** Gaussian noise gives the usual analytic posterior; RBF gives nearby inputs higher covariance. GP kernels need not be RBF, dense inference is costly, and inputs need not be i.i.d. B’s “only” and C are not universal GP definitions.

### 中文对应答案
**在课程采用的高斯似然与RBF核假设下，B、C正确。** 高斯噪声使通常的后验有解析形式；RBF核让相近输入具有更高的协方差。GP的核不必是RBF，精确稠密推断的计算成本较高，输入也不必独立同分布。B中的“只有”以及C都不是GP的普遍定义。

## 原卷索引 / Original-paper index

仅列本册题型在各原卷中的位置；未列题目在另一题型分册。按原卷题号查找本册位置；不同年份的重复题指向同一MT编号。2021B*保留题纸与配套答案的年份冲突。

### 2020B期中Quiz

| 原题 | 本册题号与页码 | 分值 |
|---|---|---|
| Q1 | [MT001](MultipleChoice.md#mt001) | 5 |
| Q2 | [MT002](MultipleChoice.md#mt002) | 5 |
| Q3 | [MT003](MultipleChoice.md#mt003) | 5 |
| Q4 | [MT004](MultipleChoice.md#mt004) | 5 |
| Q5 | [MT005](MultipleChoice.md#mt005) | 5 |
| Q6 | [MT006](MultipleChoice.md#mt006) | 5 |

### 2021A期中

| 原题 | 本册题号与页码 | 分值 |
|---|---|---|
| Q1 | [MT014](MultipleChoice.md#mt014) | 5 |
| Q2 | [MT015](MultipleChoice.md#mt015) | 5 |
| Q3 | [MT016](MultipleChoice.md#mt016) | 5 |
| Q4 | [MT017](MultipleChoice.md#mt017) | 5 |
| Q5 | [MT018](MultipleChoice.md#mt018) | 5 |
| Q6 | [MT019](MultipleChoice.md#mt019) | 5 |

### 2021B*期中

| 原题 | 本册题号与页码 | 分值 |
|---|---|---|
| Q1 | [MT027](MultipleChoice.md#mt027) | 5 |
| Q2 | [MT028](MultipleChoice.md#mt028) | 5 |
| Q3 | [MT029](MultipleChoice.md#mt029) | 5 |
| Q4 | [MT030](MultipleChoice.md#mt030) | 5 |
| Q5 | [MT031](MultipleChoice.md#mt031) | 5 |
| Q6 | [MT032](MultipleChoice.md#mt032) | 5 |

### 2023A期中

| 原题 | 本册题号与页码 | 分值 |
|---|---|---|
| Q1 | [MT040](MultipleChoice.md#mt040) | 5 |
| Q2 | [MT041](MultipleChoice.md#mt041) | 5 |
| Q3 | [MT042](MultipleChoice.md#mt042) | 5 |
| Q4 | [MT043](MultipleChoice.md#mt043) | 5 |
| Q5 | [MT044](MultipleChoice.md#mt044) | 5 |
| Q6 | [MT045](MultipleChoice.md#mt045) | 5 |

### 2023B期中

| 原题 | 本册题号与页码 | 分值 |
|---|---|---|
| Q1 | [MT052](MultipleChoice.md#mt052) | 5 |
| Q2 | [MT053](MultipleChoice.md#mt053) | 5 |
| Q3 | [MT054](MultipleChoice.md#mt054) | 5 |
| Q4 | [MT055](MultipleChoice.md#mt055) | 5 |
| Q5 | [MT056](MultipleChoice.md#mt056) | 5 |
| Q6 | [MT057](MultipleChoice.md#mt057) | 5 |

### 2025A期中

| 原题 | 本册题号与页码 | 分值 |
|---|---|---|
| Q1 | [MT040](MultipleChoice.md#mt040) | 5 |
| Q2 | [MT041](MultipleChoice.md#mt041) | 5 |
| Q3 | [MT042](MultipleChoice.md#mt042) | 5 |
| Q4 | [MT043](MultipleChoice.md#mt043) | 5 |
| Q5 | [MT044](MultipleChoice.md#mt044) | 5 |
| Q6 | [MT057](MultipleChoice.md#mt057) | 5 |
