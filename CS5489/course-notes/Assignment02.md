# Assignment 2 · Backpropagation and Optimization
## 看懂每一块接口，再把梯度接起来

[Lecture 5](Lecture05.md) · [课程目录](README.md) · [批量梯度基础](../../learning/foundation-notes/MathForML.md#batch-gradients)

本作业有两条任务线：Section 1补齐NumPy网络的反向传播，Section 2观察不同优化器如何走过几种二维函数。前者检查“梯度是否算对”，后者检查“有了梯度后怎样更新”。梯度方向算错时，单纯调整学习率无法修正它，因此要先检查求导，再比较优化器。

依据Assignment2.ipynb（76个单元）及MLP Primer（4页）。本文提供推导、接口和调试方法，训练与轨迹实验按原任务自行完成。

**按需补课：** [指数与对数](../../learning/foundation-notes/MathForML.md#powers-logs)、[导数](../../learning/foundation-notes/MathForML.md#derivatives)、[矩阵梯度与广播](../../learning/foundation-notes/MathForML.md#batch-gradients)。先会对一个小批量检查形状，再读完整网络。

| 任务 | 优先级 | 难度与卡点 | 需要掌握／当前依据 |
|---|---|---|---|
| Hidden、Output反传 | 核心必会 | 高，平均、求和与更新时机 | 写出同形梯度并通过有限差分；Assignment2，第4–7个单元、Section1_MLP_Primer，第1–4页 |
| 可学习激活指数 | 核心必会 | 高，对输入和参数分别求导 | 解释标量指数如何汇总梯度；Assignment2，第4个单元、Assignment2，第7个单元 |
| Wine实验 | 常规掌握 | 中，数据预处理与公平比较 | 真实运行、报告曲线与误差；Assignment2，第8–27个单元 |
| 五种优化器 | 核心必会 | 中，状态变量与符号约定 | 手算一步、实现状态更新；Assignment2，第28–55个单元 |
| 轨迹实验 | 核心必会 | 中，控制变量 | 用指定函数回答学习率/鞍点/局部极值问题；Assignment2，第56–75个单元 |
| 一般收敛证明 | 二读拓展 | 高，条件与证明 | 当前任务不要求完整证明，不据此推断考试不考 |

评分比例、打包和身份字段回原任务及[课程信息栏](https://crazyshout.github.io/micro-course/notices.html)。下载文件未注明截止日期，以Canvas为准。

[TOC]

<a id="interfaces"></a>
## 1. 先沿前向过程把变量认全

一批B个样本，每行d个特征。隐藏宽度h，类别数C。原NumPy模板使用行样本：

$$X_{B\times d}\;\longmapsto\;U=XA+c\;\longmapsto\;H=\phi(U)
\;\longmapsto\;Z=HW+b\;\longmapsto\;L.$$

A是d×h，c是1×h；W是h×C，b是1×C。模板隐藏层属性叫`W`、输出层属性叫`w`；上式用A/W避免同名字母混淆。代码的`alpha`是正则系数，`learning_rate`才是更新步长；不要因为优化器公式也用alpha就混成同一个量。

`forward_pass`存下后面求导会用的值。`backward_pass`接收下游给来的梯度，算本层参数梯度，并返回上一层所需梯度。返回的是导数数组，不是分类标签，也不是更新后的特征。

**形状检查 / Check：** B=2、d=3、h=4、C=2时，U、Z、隐藏权重梯度各是什么形状？ / Give the shapes of U, Z and the hidden-weight gradient.

<details markdown="1"><summary>答案 / Answer</summary>

U为2×4，Z为2×2，隐藏权重梯度为3×4。梯度与被求导参数同形。 / (2,4), (2,2), and (3,4), respectively.

</details>

<a id="loss"></a>
## 2. Loss与Output：先统一“平均”的位置

原Loss.forward对B个样本取平均。对于one-hot标签矩阵Y，若P为softmax概率，应有 $G_Z=(P-Y)/B$。但Assignment2，第7个单元给定的Loss.backward返回未除B的P−Y。这是需要显式处理的接口约定，计算梯度时也需要与这个平均目标一致。

两种等价实施方式是：在链条入口除B一次，后续各层正常求和；或保持模板的未归一化上游，在每个参数梯度处统一按B平均。不要在每一层都缩小传回的梯度，否则深层会多除好几次。本学习推导固定采用**入口除一次**，所有有限差分按同一个平均目标验证。若提交要求只能填TODO，应在允许的计算位置落实同等缩放，并解释采用的约定。

正则目标为 $L=L_{data}+\frac\lambda2(\|A\|_F^2+\|W\|_F^2)$，偏置不在模板正则项中。Output所需三项为

$$\nabla_W L=H^TG_Z+\lambda W,\quad
\nabla_b L=\sum_i(G_Z)_{i,:},\quad
G_H=G_ZW^T.$$

广播的b影响所有样本，所以要沿batch轴求和并保持1×C形状。**先用更新前的W算$G_H$，再修改W。** 一边反传一边用刚更新的权重，会把同一次计算图里的参数版本混起来。

Primer的单样本式子 $\partial L/\partial b=\partial L/\partial z$ 可以帮助记方向，但直接搬到批量程序会少一次汇总。用单样本推导理解局部关系，用数组形状完成批量实现。

## 3. Hidden：ReLU和Leaky ReLU不能套错

Primer主要用ReLU，原Notebook的普通隐藏层实际用Leaky ReLU：正区斜率1，负区斜率0.01。零点不可微，固定实现约定即可；数值差分测试选离0有距离的输入。

$$G_U=G_H\odot\phi'(U),\quad
\nabla_A L=X^TG_U+\lambda A,\quad
\nabla_c L=\sum_i(G_U)_{i,:},\quad G_X=G_UA^T.$$

$\odot$为逐元素乘，不是矩阵乘。这里每个位置的激活只依赖同一位置的输入，所以将对应的两个导数相乘即可。若输出同时依赖多个输入，就需要把各条影响路径的贡献加起来。

**手算 / Worked：** U=(−2,3)，上游$G_H=(4,5)$。Leaky ReLU输出(−0.02,3)，反向$G_U=(0.04,5)$。若错用普通ReLU，第一项会变成0，改变了原模型。 / The leaky slope preserves a small negative-side gradient.

<a id="learnable-activation"></a>
## 4. 可学习指数：对数为什么突然出现？

原`Hidden_Vondrick`在正区用 $\phi(u,n)=u^n$，负区用0.01u；n是共享的一个标量参数，不是每个样本各有一个n。对u和n是两种不同的提问：

$$\frac{\partial\phi}{\partial u}=nu^{n-1},\qquad
\frac{\partial\phi}{\partial n}=u^n\log u\quad(u>0).$$

第二式来自$u^n=e^{n\log u}$：改变指数时，先对指数内部求导得到log u。负区对u的导数0.01，对n的导数0；u=0处依约定处理，不能对负数直接计算实数log。

共享指数收到所有位置的贡献：

$$\frac{\partial L}{\partial n}=\sum_{i,j}(G_H)_{ij}
\frac{\partial\phi(U_{ij},n)}{\partial n}.$$

计算正区时先用mask选出正数，再调用power/log；不要依靠`np.where`隐藏另一分支中的非法log，因为两侧表达式可能都先被求值。原模板对n投影到至少1.01，且该层权重/指数分别有硬编码步长0.0005/0.001；这两个硬编码步长没有跟随外部learning_rate一起变化。

**跟做 / Worked：** u=2、n=2、上游导数3。输出4；对u的损失导数为3×4=12，对n为$3\times4\ln2\approx8.3178$。 / Output 4, input gradient 12, exponent gradient about 8.3178.

**变式 / Transfer：** u=0.5、n=2、上游导数3，两个梯度的符号？ / Determine both gradient signs.

<details markdown="1"><summary>答案 / Answer</summary>

对u为3；对n为$0.75\ln0.5\approx-0.5199$。底数在0和1之间，指数增加会让输出变小。 / The input gradient is 3; the exponent gradient is negative because increasing the exponent shrinks a base below one.

</details>

## 5. 先检查小数值，再训练葡萄酒数据

调试顺序：核对层形状；检查一个样本；再检查两个样本的平均与偏置；最后逐项核验有限差分。对某参数$\theta_k$，用中心差分

$$g_k^{FD}=\frac{L(\theta+\varepsilon e_k)-L(\theta-\varepsilon e_k)}{2\varepsilon}$$

与解析梯度比较。double精度取例如$\varepsilon=10^{-6}$，避开激活拐点；正则项、平均方式、输入和随机状态要完全相同。先算梯度后更新，差分时不训练。对不同分支分别选小输入检查，例如同时包含激活的正区和负区。

原数据Wine CSV有1599行、11个输入字段，quality≥6映射1，否则0；855条映射为1。原外部划分为test_size=0.25、random_state=1。原题提到的约70%以上可作调试参考；实际训练与测试准确率应由你的运行结果计算。

对全数据fit_transform，Assignment2，第15个单元才划分。作为严格实验应先划分，在训练集拟合MinMaxScaler，再用同一变换处理验证/测试。这样可以避免测试集统计影响训练阶段的缩放。[scikit-learn官方说明](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage)（核对2026-10-02）

与sklearn MLPClassifier比较时记下架构、激活、正则、批量、训练轮数与种子；两者设定并不完全相同，所以差异不能自动归因于反传错误。先让一个很小的训练子集能被拟合，再看完整划分，是实用排错步骤。


来源：Assignment2，第11个单元。

<a id="optimizers"></a>

## 6. 五种优化器：同一条梯度，不同的走法

记当前位置为$\theta_t$、梯度为$g_t$，学习率为$\eta$。本题的SGD在二维函数梯度上加高斯噪声，模拟随机性；它没有真实小批量数据，不能把这段噪声模型当作所有真实SGD的精确分布。

| 方法 | 必要状态与更新 | 需要解释的行为 |
|---|---|---|
| GD | $\theta_{t+1}=\theta_t-\eta g_t$ | 步长过大可能越走越远 |
| 模拟SGD | 用$g_t+\xi_t$替代梯度 | 轨迹有波动，比较时记录噪声种子 |
| Momentum | $v_t=\gamma v_{t-1}+\eta\tilde g_t$；$\theta_{t+1}=\theta_t-v_t$ | v已经包含学习率，不再多乘一次 |
| AdaGrad | $s_t=s_{t-1}+\tilde g_t^2$；按$\eta/\sqrt{s_t+\epsilon}$缩放 | 累积平方梯度越大，有效步长越小 |
| Adam | 维护一阶、非中心二阶矩，零初始化偏差修正后更新 | t从1开始；两个状态与参数同形 |

这里AdaGrad的epsilon在根号内，沿用Assignment2，第48个单元；有些库放根号外，它们不是逐数值完全相同的实现。部分已有卡片采用根号外的约定；对照时先看epsilon的位置。

Adam沿原Assignment2，第52个单元：

$$m_t=\beta_1m_{t-1}+(1-\beta_1)\tilde g_t,\quad
v_t=\beta_2v_{t-1}+(1-\beta_2)\tilde g_t^2,$$

$$\hat m_t=m_t/(1-\beta_1^t),\quad\hat v_t=v_t/(1-\beta_2^t),\quad
\theta_{t+1}=\theta_t-\eta\hat m_t/(\sqrt{\hat v_t+\epsilon}).$$

第一个t不能取0，否则偏差修正分母为0。v是梯度平方的滑动平均，不是减去均值后的方差。原小标题写Adaptive Momentum Estimation，常用全称是Adaptive Moment Estimation；“best of all worlds”应当作宣传式概括，不能当任何任务都最好的定理。

**一步手算 / Worked：** 一维二次函数$f(\theta)=\theta^2$，θ=2，η=0.1。GD的梯度4，更新θ=1.6；若上一动量v=0.2、γ=0.9，则新v=0.58，新θ=1.42。 / Distinguish the velocity state from the gradient and the parameter.

Nesterov在Assignment2，第45–46个单元用于理解“向前看一点再求梯度”，题目不要求实现；RMSProp/AdaDelta在Assignment2，第50个单元仅作简要介绍。

<a id="experiments"></a>
## 7. 原题的函数与图该怎样比较

| 原任务 | 应固定／改变什么 | 结果解释 |
|---|---|---|
| Assignment2，第31–33个单元 画bowl、mult、monkey、matyas | 固定网格、标注x/y/f | 先认局部极值、平坦区与狭长谷 |
| Assignment2，第59–62个单元 学习率 | 同初值、函数、迭代数，改步长 | 比较慢、稳、发散，不以画面大小当收敛 |
| Assignment2，第63–65个单元 Momentum与Matyas | 同初值及学习率，改变优化器 | 看方向累积是否减少无效摆动 |
| Assignment2，第66–70个单元 monkey平坦区 | 按题目参数先演示；另做等步数对照 | 原推荐epoch并不相同，不能据终点直接排名 |
| Assignment2，第71–75个单元 mult多极值 | 包括Adam，至少三种方法 | 正文初值0.5与代码建议0.8冲突，报告选用哪一项 |

原公式：bowl为$x^2+y^2$；mult为$\sin(\sqrt{x^2+y^2})$；题中monkey写$x^3+3xy^2$；Matyas为$0.26(x^2+y^2)-0.48xy$。保留题面函数，不仅凭函数昵称替换成另一符号版本；mult在原点的可微性也需小心，原题建议的初值不在原点。

本指南对mult实验采用代码单元给定的(0.8,0.8)，把正文(0.5,0.5)列为原文不一致；若教师另有澄清，应以澄清为准。用静态等高线加完整轨迹、起点与终点即可支持网页和纸读；动画可用于自己观察，但不能让打印版只剩一块空白。

## 8. 原文核对与修正记录

| 原位置 | 问题 | 学习稿采用的解释 |
|---|---|---|
| Assignment2，第30个单元 凸性不等式 | 右侧漏掉f，输入与函数值混写 | $f(\theta x+(1-\theta)y)\le\theta f(x)+(1-\theta)f(y)$，且域凸、θ在[0,1] |
| Assignment2，第35个单元 收敛概括 | 没有步长等条件，且非凸不保证到局部最小 | 需说明平滑性、步长等假设；可能不收敛或停在驻点 |
| Assignment2，第47–48个单元 AdaGrad说明 | 不是按“特征值大小”分配步长，也不免去全局步长 | 按历史平方梯度缩放；仍选eta |
| Section1_MLP_Primer，第1–4页 与Assignment2，第4个单元/Assignment2，第7个单元 | PDF用ReLU，Notebook用Leaky/custom；单样本偏置式不等于批量式 | 按任务层定义分支，按batch汇总 |
| Assignment2，第7个单元 Loss接口 | mean forward与未归一化backward | 平均因子在整条链一致处理，有限差分核验 |
| Assignment2，第11个单元/Assignment2，第15个单元 | 全量缩放后划分 | 学习实验先划分、训练拟合变换 |
| Assignment2，第71个单元与Assignment2，第72–75个单元 | 初值0.5与0.8不一致 | 本指南采用代码建议并明确记录 |

凸性定义另核对[Boyd与Vandenberghe讲义](https://web.stanford.edu/~boyd/cvxbook/bv_cvxslides.pdf)第3.2页（PDF第46页）。上表为根据原公式和代码整理的勘误说明。

## 9. 完成前如何自查

能解释每层输入、输出和梯度形状；平均、正则和偏置一致；更新前保存反传所需权重；自定义激活只对正数取log；预测输出与原接口吻合；随机状态与数据划分记录；所有训练成绩和轨迹来自实际运行。尚未运行的实验标为“待运行”。

**English self-check:** Explain where the batch averaging occurs, why a shared exponent receives a summed gradient, how leakage is prevented, and which variables were held fixed in an optimizer comparison.

首轮复习沿用[M248前向/反向/更新](https://crazyshout.github.io/micro-course/cards.html#CS5489-M248)、[M251批量梯度](https://crazyshout.github.io/micro-course/cards.html#CS5489-M251)、[M266动量](https://crazyshout.github.io/micro-course/cards.html#CS5489-M266)、[M268 Adam](https://crazyshout.github.io/micro-course/cards.html#CS5489-M268)。可学习指数配合§4的手算例子复习。

## 来源覆盖索引

| 单元／页码 | 本文位置 |
|---|---|
| Assignment2，第1–5个单元 总任务、两类隐藏层、说明 | 开头、§1、§3–4 |
| Assignment2，第6–7个单元 NumPy层、Loss、NN接口与TODO | §1–5 |
| Assignment2，第8–18个单元 Wine输入、预处理、基线 | §5 |
| Assignment2，第19–27个单元 普通/自定义网络训练与评价 | §4–5、§9，未代跑作业 |
| Assignment2，第28–33个单元 函数与图 | §7–8 |
| Assignment2，第34–55个单元 GD、SGD、Momentum、Nesterov、AdaGrad、Adam与Optimizer | §6 |
| Assignment2，第56–75个单元 绘图助手与四组轨迹任务 | §7 |
| Assignment2，第76个单元 空单元 | 无教学内容 |
| Primer Section1_MLP_Primer，第1页前向，Section1_MLP_Primer，第2页 Loss/Output，Section1_MLP_Primer，第3–4页 Hidden/Jacobian | §1–4、补课；符号差异明确列出 |