# Lecture 4 · Regression｜从“分到哪一类”走向“预测多少”

[课程目录](README.md) · [上一讲：分类](Lecture03.md) · [数学补课：秩与伪逆](../../learning/foundation-notes/MathForML.md#rank-pseudoinverse)

上一讲给一朵花贴类别标签。这一讲老师换成房价：已知房屋面积、售出时的年龄等信息，希望预测一个数值。输出不再是有限几个标签，而是实数。我们沿着 **线性回归 → 特征选择 → 异常值 → 非线性回归 → 集成模型** 走一遍。下面用房价数据观察这些方法怎样拟合数值。

配套练习是[Tutorial 4：共享单车回归](Tutorial04.ipynb)，会把回归用于按年份变化的需求数据。原课文件及单元覆盖见文末。

基础复习可跳过：不熟悉函数和斜率，读[函数图像](../../learning/foundation-notes/MathForML.md#symbols-functions)；矩阵不满秩、不能直接求逆，读[秩与伪逆](../../learning/foundation-notes/MathForML.md#rank-pseudoinverse)；不熟悉向量导数，读[梯度](../../learning/foundation-notes/MathForML.md#optimization)。Python与数组回到[Lecture1](Lecture01.md#arrays)。

[TOC]

| 主题 | 优先级 | 难度与卡点 | 掌握要求与依据 |
|---|---|---|---|
| OLS、残差与矩阵解 | 核心必会 | 中至高；样本放行还是列 | 解释、手算、推导并判断可逆；Lecture4a，第13–34个单元 |
| Ridge、LASSO、OMP | 核心必会 | 高；缩小与精确为零不同 | 比较目标、选择特征、验证；Lecture4a，第35–88个单元 |
| RANSAC | 常规掌握 | 中；阈值与随机采样 | 解释并走完一次迭代；Lecture4b，第4–15个单元 |
| Polynomial、kernel ridge、SVR | 核心必会 | 中至高；模型与损失 | 计算小例，设计CV；Lecture4b，第16–72个单元 |
| Tree、RF、boosting | 常规掌握 | 中；模型怎样组合 | 解释机制、比较误差；Lecture4b，第73–100个单元 |
| 大规模网格与一般核理论 | 二读拓展 | 高；计算规模 | 能读流程和适用条件；Lecture4a／Lecture4b中的搜索示范 |

优先级依据当前课件及Tutorial4的回归任务。难度反映理解所需的步骤，考核范围仍以教师公布的要求为准。

<a id="data"></a>
## 1. Regression and the housing example｜先弄清横纵轴的单位

输入 $\mathbf x\in\mathbb R^d$，输出 $y\in\mathbb R$；希望学到 $\hat y=f(\mathbf x)$。误差 $r_i=y_i-\hat y_i$ 叫 residual（残差）。图上的点表示实际观测，线或曲面表示模型预测；两者的距离就是残差。

老师先用100个人工数据点展示斜率、截距和噪声，再用房屋的真实记录预测售价。下面保留课堂的数据字段和单位，这样系数才有明确含义。

老师 mode1 的处理必须连同单位一起保留：

| 原字段 | 处理后 | 单位与解释 |
|---|---|---|
| GrLivArea | 除100 | 100平方英尺（不是平方米） |
| YrSold、YearBuilt | 相减 | 售出时年龄，年 |
| SalePrice | 除1000 | 原数据价格单位的千元，图中标为美元千元 |
| 行采样 | `[::4]` | 每4行取1行，保留原顺序；不是随机抽样 |

mode2 取 GrLivArea、TotRmsAbvGrd、GarageArea、TotalBsmtSF、Fireplaces、BedroomAbvGr、FullBath、LotArea、LowQualFinSF、OverallQual、OverallCond、YrSold、YearBuilt，合并最后两列为 Age 后剩12维；这些面积列不统一除100。预测目标仍除1000。不同 mode 的系数不能直接比数值。

![Housing data and fitted two-feature model](assets/lecture04-housing.png)

看图时，找几栋面积接近的房屋：它们的售价仍然不同。面积能解释一部分价格差异，房龄等因素还可能提供更多信息。因此，我们寻找的是总体误差较小的预测关系。

## 2. Linear regression and OLS｜找一条总体偏差较小的线

一维 $\hat y=wx+b$，w是每增加一单位x的预测变化；b是在x=0的截距。多维 $\hat y=\mathbf w^T\mathbf x+b$，每个系数解释为**其他输入固定时模型的预测变化**，不是现实中强行改变该属性的因果效应。

Ordinary least squares（OLS，普通最小二乘）最小化平方残差和：

$$E(\mathbf w,b)=\sum_{i=1}^N[y_i-(\mathbf w^T\mathbf x_i+b)]^2.$$

为什么平方？正负残差不能相互抵消，偏离越远罚得越多，也形成方便求导的目标。代价是极端点的影响可能很大。MSE=E/N，RMSE=$\sqrt{E/N}$：MSE的单位是价格单位的平方，RMSE才回到价格单位。

**完整补算（教学例子）：** 三个观测点为 $(0,1),(1,2),(2,2)$。先求平均：$\bar x=(0+1+2)/3=1$，$\bar y=(1+2+2)/3=5/3$。一维最小二乘的斜率用下面的比值计算；下一节再从平方误差求导说明公式的来历。

| 点 | $x_i-\bar x$ | $y_i-\bar y$ | 两者乘积 | $(x_i-\bar x)^2$ |
|---|---:|---:|---:|---:|
| (0,1) | −1 | −2/3 | 2/3 | 1 |
| (1,2) | 0 | 1/3 | 0 | 0 |
| (2,2) | 1 | 1/3 | 1/3 | 1 |
| 合计 | | | 1 | 2 |

$$w=\frac{\sum_i(x_i-\bar x)(y_i-\bar y)}{\sum_i(x_i-\bar x)^2}=\frac12,
\qquad b=\bar y-w\bar x=\frac76.$$

把各个x代入 $\hat y=x/2+7/6$，预测为 $(7/6,5/3,13/6)$；真实值减预测值得残差 $(-1/6,1/3,-1/6)$。因此

$$\mathrm{SSE}=\frac1{36}+\frac19+\frac1{36}=\frac16,
\qquad\mathrm{MSE}=\frac{\mathrm{SSE}}3=\frac1{18}.$$

<a id="ols"></a>
## 3. Matrix solution｜先摆好矩阵，再求导

三点的计算可以一次写成矩阵运算。先沿用老师“每列一个样本”的约定：给每个输入补一个常数1，让偏置也能放进权重向量。记

$$\tilde x_i=(x_i^T,1)^T,\quad
X=[\tilde x_1,\ldots,\tilde x_N]\in\mathbb R^{(d+1)\times N},\quad
w\in\mathbb R^{d+1},\quad y\in\mathbb R^N.$$

这里d是每条记录的特征数，N是记录数；w最后一项是截距。$X^Tw$得到N个预测值，每个样本恰好对应一个。程序常把样本放在行上，此时数据矩阵应写成 $A=X^T$，预测为Aw。

展开目标：

$$E=\|y-X^Tw\|^2=y^Ty-2y^TX^Tw+w^TXX^Tw.$$

第一项不含w，导数0；第二项导数 $-2Xy$；因为 $XX^T$ 对称，第三项导数 $2XX^Tw$。令梯度为0：

$$XX^Tw=Xy.$$

方程能直接求逆的条件是X的各行相互独立，即**满行秩（full row rank）**。这时

$$w=(XX^T)^{-1}Xy.$$

在当前“样本放列”的约定下，每一行对应一项特征或常数1。若两项特征完全重复，便有两行相同，矩阵不能直接求逆。仅仅两条样本重复，并不足以断言所有行都不独立。

不能求逆时，最小二乘仍然有意义：仍可寻找误差最小的预测；若有多组系数做到同样好，伪逆会选长度最小的一组。具体数字见[秩与伪逆补课](../../learning/foundation-notes/MathForML.md#rank-pseudoinverse)。程序可用 `np.linalg.lstsq(A,y,rcond=None)`，等价写法是 $A^+y$。

**对照原课：** Lecture4a，第21个单元的 $(XX^T)^{-1}X$ 是 $X^T$ 的伪逆。数值程序通常通过解方程、QR或SVD求解，避免显式求逆；这些求解器细节可在二读时补充。

**变式 / Transfer:** 三点改成 $(0,2),(1,3),(2,3)$，w、b、MSE怎样变？ / Add one to every output in the worked example; how do w, b and MSE change?

<details markdown="1"><summary>答案 / Answer</summary>

w仍1/2，b变13/6，残差与MSE不变。 / The slope remains 0.5, the intercept becomes 13/6, and MSE remains 1/18. 整条线向上平移1。

</details>

## 4. Housing coefficients and feature selection｜大权重必须配着单位读

课堂分别用面积、年龄，以及两者共同拟合。原 Lecture4a，第34个单元 保存的文字系数“每100平方英尺增加8874、每年减少1048、截距82709”是**原课结果**。复算所用数据及结果见文末记录。

接着比较12个特征的散点/成对图。一个特征单独相关不代表加入其他特征后仍有同样贡献；面积、房间数可能彼此相关。想比较系数大小，先在训练数据上标准化，否则“美元/平方英尺”和“美元/年”不在同一尺度。标准化后系数对应输入改变一个训练标准差的预测差异。

来源：Lecture4a，第25–34个单元。
来源：Lecture4a，第35–41个单元。


## 5. Ridge regression｜给不稳定方向加一条“别太夸张”的限制

房屋面积和房间数往往一起增加，两项特征可能提供很相近的信息。此时，很多组系数都能拟合得差不多，数据稍有变化，系数却可能变很多。

看一个更极端的教学例子：把同一列面积重复输入两次。系数取 $(100,-99)$ 与 $(0.5,0.5)$ 时，预测相同，因为都只相当于面积乘1。前一组依赖两个大数互相抵消。Ridge在拟合误差之外，加上系数平方和作为代价：前一组是19801，后一组只有0.5，因此更偏好后一种分配。这里比较的是两组相同预测的系数；完整训练还会同时权衡预测误差。

$$E(w)=\sum_i(y_i-f(x_i))^2+\alpha\|w\|^2,\qquad\alpha\ge0.$$

第一项要求预测贴近数据，第二项限制系数大小。alpha越大，大系数的代价越高；它与上一讲分类器C的调节方向相反。常用实现只惩罚特征权重，不惩罚截距。

**一维手算（无截距）：** x=(1,2)，y=(1,2)，所以 $\sum x^2=\sum xy=5$。目标为 $5(1-w)^2+\alpha w^2$，求导得

$$10(w-1)+2\alpha w=0
\quad\Rightarrow\quad w=\frac5{5+\alpha}.$$

alpha=0时回到OLS的w=1；alpha=5时w=0.5。预测离训练点更远，但系数更小。这个例子展示了两项代价的取舍；是否改善新数据预测，要用验证数据判断。Ridge通常缩小系数，LASSO则可以直接得到零系数，下一节会比较。

<details markdown="1"><summary>进一步看矩阵：为什么加正则项后可以求解？</summary>

若w的所有分量都受惩罚，求导得到

$$(XX^T+\alpha I)w=Xy.$$

当 $\alpha>0$，对任意非零向量v，

$$v^T(XX^T+\alpha I)v=\|X^Tv\|^2+\alpha\|v\|^2>0.$$

即使某个方向满足 $X^Tv=0$，第二项仍大于0，所以矩阵可逆。直观上，原数据无法区分的系数组合，现在也要付出正则代价。若截距不受惩罚，应先中心化输入和目标、求特征权重，再恢复截距；也可以使用最后一个对角元素为0的惩罚矩阵。

</details>

**课堂实验与来源：** Lecture4a，第42–62个单元先展示近重复特征，再比较不同alpha。原划分为80/20、种子4487。课堂测试曲线用于探索；配套示范用训练内部交叉验证选alpha，并将标准化与模型放进同一个Pipeline，让每折只用该折训练数据估计缩放参数。

## 6. LASSO｜有时需要真的把系数变成零

LASSO（Least Absolute Shrinkage and Selection Operator）把平方惩罚换成绝对值：

$$E=\sum_i(y_i-f(x_i))^2+\alpha\sum_j|w_j|.$$

图中的椭圆表示相同拟合误差：越靠近椭圆中心，误差越小。圆或菱形表示允许的系数范围。寻找两者刚好接触的位置，就是在限制下尽量降低误差。L1的菱形尖角落在坐标轴上，接触点落到尖角时，一个系数恰好为0；L2的圆形边界没有这种尖角。这个图解释了LASSO为什么容易产生零系数，具体哪些系数为0仍取决于数据和alpha。

![Instructor L1 geometry](assets/source-l1.png)
![Instructor L2 geometry](assets/source-l2.png)

用一维计算看清“变成零”的过程。对无截距目标 $\sum_i(y_i-wx_i)^2+\alpha|w|$，记 $a=\sum_i x_i^2>0$、$t=\sum_i x_i y_i$。与w有关的部分是 $aw^2-2tw+\alpha|w|$。

- w>0时，$|w|=w$，导数为 $2aw-2t+\alpha$，候选解 $(t-\alpha/2)/a$ 必须为正。
- w<0时，$|w|=-w$，导数为 $2aw-2t-\alpha$，候选解 $(t+\alpha/2)/a$ 必须为负。
- 若 $|t|\le\alpha/2$，两侧都不能继续降低目标，最优点落在w=0的尖角上。

合起来得到

$$w=\frac{\operatorname{sign}(t)\max(|t|-\alpha/2,0)}a.$$

沿用a=t=5，alpha=4得w=0.6；alpha=10得0。这叫软阈值。sklearn Lasso把拟合项写成 $\|y-Aw\|^2/(2N)$，同名alpha与上式缩放不同；应先对齐目标再比较数字。

课堂用非零系数数目和CV选择alpha。原课特征列表是该数据/设置下的结果，不是宣告房间数等永远无用。相关变量可能互相替代；大alpha也可能丢掉真正有用的信号。

来源：Lecture4a，第69–80个单元。


## 7. Sparsity and OMP｜每次挑方向，但要回头一起重拟合

$\|w\|_0$表示非零个数，不是真正的范数。限制 $\|w\|_0\le K$ 是组合选择问题，一般难以穷举。Orthogonal Matching Pursuit（OMP）用贪心近似：从残差开始，选与残差最相关的未选特征，加入已经选中的特征集合，**对所有已选特征联合重做最小二乘**，再更新残差。

**对照原课：** Lecture4a，第83个单元的简写只计算新特征的系数；OMP还需要把所有已选特征一起重新拟合。比较各列与残差的相关程度前，应中心化并适当归一化，避免仅因某列数值更大就选中它。

**走完两轮（补充算例）：** 不设截距，两列特征都已归一化为长度1：$a_1=(1,0)^T$、$a_2=(1,1)^T/\sqrt2$，目标 $y=(1,2)^T$。

第一轮还没选特征，残差就是y。计算 $a_1^Ty=1$，$a_2^Ty=3/\sqrt2$，因此选a₂。它的系数为 $3/\sqrt2$，预测为 $(3/2,3/2)$，残差为 $(-1/2,1/2)$。

第二轮把a₁也选进来。现在一起求两个系数c₁、c₂：

$$c_1\begin{pmatrix}1\\0\end{pmatrix}
+\frac{c_2}{\sqrt2}\begin{pmatrix}1\\1\end{pmatrix}
=\begin{pmatrix}1\\2\end{pmatrix}.$$

第二行给 $c_2=2\sqrt2$，第一行给c₁=−1。两列合起来恰好重建y，残差为0。注意a₂的系数也从 $3/\sqrt2$ 改成了 $2\sqrt2$：这就是“联合重拟合”。如果固定旧系数，只计算新特征的贡献，就做不到这一步。Lecture4a，第84个单元调用的OMP包含这次联合更新。

<a id="ransac"></a>
## 8. RANSAC｜不是每个离群点都值得把直线拽过去

几个离群点就可能明显拉动拟合直线，课堂例子展示大残差如何支配平方误差。Ridge缩小权重，但仍平方惩罚残差，因此不是专门的异常值过滤器。RANSAC（Random Sample Consensus）反复：随机选足够拟合的小子集 → 拟合候选模型 → 按残差阈值找inliers → 保留较大一致集 → 对一致集重新拟合。

拟合二维图中的直线至少需要两个横坐标不同的点，不是任意两行都够。原手工示范Lecture4b，第9个单元有放回采样，可能抽中同一个点；学习时应检查退化样本并跳过。阈值T用y的单位，例如预测价格千元时T=15表示1.5万元，不是15%。inlier/outlier是相对于模型和阈值的判断，不自动代表真实数据好坏。

![OLS, ridge and RANSAC on the instructor synthetic outlier setup](assets/lecture04-ransac.png)

本轮重算保留Lecture4b，第5个单元的4487/447数据种子及Lecture4b，第13个单元的RANSAC种子1234。图中对照线说明稳健拟合的目的；成功仍依赖足够的一致点、合理模型与阈值。补充概率：每次独立取s个点、单点为inlier概率约q，k次至少一次全inlier概率约 $1-(1-q^s)^k$；近似假设应说明，不能当作任意数据都保证成功。

来源：Lecture4b，第4–15个单元。


## 9. Polynomial regression｜对输入非线性，对参数仍线性

把x变成 $(1,x,x^2,\ldots,x^p)$ 再线性拟合。曲线可以弯，但待估参数w仍线性进入。二元二次可含 $(1,x_1,x_2,x_1^2,x_1x_2,x_2^2)$；三次纯项为 $(x_1^3,x_1^2x_2,x_1x_2^2,x_2^3)$，原Lecture4b，第34个单元最后的 $x_3^3$ 是笔误。

给直线模型加上x²项后，新模型仍然能画出原来的直线：只要把x²的系数设成0即可。因此，在不加正则且精确求到最优解时，增加多项式阶数不会提高训练SSE。但多出来的弯曲也可能追着训练噪声跑，使新数据上的误差变大。用交叉验证选择阶数；阶数很高时，还需留意数值计算不稳定。

代码中的 `polyfeats__degree` 是Pipeline内多项式步骤的参数名。搜索器统一寻找更大的分数，所以 `neg_mean_squared_error` 返回MSE的负值；画误差图时再取负号恢复MSE。

**变式 / Transfer:** 二维输入(2,3)用含常数和一次项的二次映射，结果是什么？ / Give the degree-2 expansion including bias and linear terms for (2,3).

<details markdown="1"><summary>答案 / Answer</summary>

$(1,2,3,4,6,9)$，共6维。 / (1,2,3,4,6,9), six features. `include_bias=False`时去掉首项，若模型另估截距可避免重复常数列。

</details>

来源：Lecture4b，第16–39个单元。


## 10. Kernel ridge regression｜把线性代数搬到样本之间

给N个训练点，$K_{ij}=k(x_i,x_j)$ 为N×N核矩阵，$k_*=(k(x_1,x_*),…,k(x_N,x_*))^T$ 为N维向量：

$$a=(K+\alpha I)^{-1}y,\qquad \hat y_*=k_*^Ta.$$

字母a是每个训练样本的系数，和特征权重w、正则参数alpha区分。对有效半正定核、alpha>0可解。截距/中心化要另外约定；默认KernelRidge并非自动拟合不惩罚的截距。

完整小例：训练x=(0,1)，线性核 $k(x,z)=xz$，y=(0,2)，alpha=1、无截距。K=diag(0,1)，a=(0,1)，在x*=2时k*=(0,2)，预测2。它与同一特征和同一惩罚的ridge等价；**不等于任意PolynomialFeatures+无正则OLS**。Lecture4b，第41个单元的“same as”需要补这个条件。多项式核映射包含缩放权重，也未必等于库默认多项式特征的未经缩放内积。

RBF gamma控制距离尺度，alpha控制正则，二者作用不同。Lecture4b，第50个单元用10×10候选、5折，共500次候选拟合；保存的最佳CV分数是模型选择结果，不是独立测试证据。

## 11. Support vector regression｜在容忍带内不追究小误差

SVR在曲线两侧各留epsilon，**总带宽2epsilon**。残差的epsilon-insensitive loss为 $\max(0,|y-f(x)|-\epsilon)$。残差0.3、epsilon0.5时损失0；残差−1.2时损失0.7。这里是超出带的**绝对误差**，不是普通平方误差；原总结Lecture4b，第101个单元的“squared error”不对应前面讲的标准epsilon-SVR。

通常目标为 $\frac12\|w\|^2+C\sum_i\max(0,|r_i|-\epsilon)$。原Lecture4b，第57个单元使用 $1/C$正则写法时需对齐因子约定。带外和边界上的支持样本可能参与预测，退化情况不能把“在边界”与“非零系数”写成双向必然。

![Epsilon-insensitive loss and regression tube](assets/lecture04-svr-tube.png)

图左先看容忍带，图右看损失的平底。C决定违约代价，epsilon决定忽略多大误差，gamma决定RBF核尺度。Lecture4b，第70个单元同时搜索三者：10×10×10候选、5折，共5000次候选拟合。这一段说明原课的搜索流程；执行范围见文末。

## 12. Trees and random forests｜多位意见不同的“专家”怎样投票

回归树按阈值逐层分支，每个叶子输出其中训练目标的平均值（平方损失情形），所以形成台阶。单棵深树容易记住训练噪声。Random Forest通过bootstrap抽样，并在节点分裂时按设置随机选特征，让多棵树产生不同规则；最终预测是**各树预测的平均**，不是只找其中一棵树的叶子。

例如三棵树对同一房屋输出180、210、210（千元），森林输出200。增加树通常稳定随机波动，但不保证每增加一棵测试误差就降低。原Lecture4b，第91个单元画的是训练MSE随树数变化，不能读成测试泛化曲线。Lecture4b，第94个单元再用5折选树深度，这才把复杂度选择和验证联系起来。

![Instructor random forest diagram](assets/source-RF.jpg)

当前`RandomForestRegressor`默认`max_features=1.0`，即每个节点可考虑所有特征；若要演示特征子采样需显式设置。名称叫随机森林不意味着每份默认代码都有严格小于全部的候选特征数。叶子平均的树通常不擅长超出训练目标范围的外推；图看起来块状合理不等于已证明无数据区域预测正确。

## 13. Boosting and XGBoost｜后一棵树接着修前面的误差

Bagging让多棵树主要并行学习不同抽样，boosting让后一个模型针对当前组合的不足继续学习。平方损失的负梯度与残差方向一致，因此可拟合 $y-f_{t-1}(x)$，再作 $f_t=f_{t-1}+\eta h_t$。若h拟合的是正梯度，则用减号。Lecture4b，第97个单元采用正梯度/减号约定，不要同时翻两个号。

补算：当前预测(2,2)，真实值(3,1)，残差(1,−1)。若新弱学习器恰拟合残差，学习率0.5，新预测(2.5,1.5)，平方误差和从2降为0.5。这只验证一步机制，不表示每个实际弱学习器都能精确拟合。

XGBoost在梯度提升树中还使用正则化及二阶信息。Lecture4b，第98个单元搜索列采样、分裂gamma、树深、行采样、学习率、树数；这里的`gamma`是最小分裂损失收益，**不是RBF gamma**。`RandomizedSearchCV(n_iter=200,cv=5,random_state=4487)`共1000次候选拟合。学习率是每轮贡献，不是某种“准确率参数”。

按 [XGBoost官方参数说明](https://xgboost.readthedocs.io/en/stable/parameter.html#learning-task-parameters)（查阅2026-09-23），`reg:squarederror`为平方误差目标，`reg:gamma`使用Gamma回归且目标须为正；不应将任意含0的非负目标直接套进去。上面的手算展示了一次提升步骤；原200候选XGBoost搜索未在本讲重新执行。

## 14. Comparing regression methods｜模型、目标、假设一起记

| 方法 | 主要能力 | 关键代价/条件 |
|---|---|---|
| OLS | 线性平方误差拟合 | 异常值、共线性；解需秩条件 |
| Ridge | 缩小权重、稳定解 | 通常不精确选零特征；需尺度一致 |
| LASSO | 稀疏线性模型 | alpha约定、相关特征选择不稳定 |
| OMP | 贪心选择少数特征 | 需联合重拟合，不是一般全局L0最优 |
| RANSAC | 抗较多污染点 | 模型、阈值、采样成功概率 |
| Polynomial/KRR | 弯曲预测关系 | 复杂度、外推、核矩阵与正则 |
| SVR | 容忍带与稀疏样本系数 | epsilon/C/核调参，非平方损失 |
| RF/boosting trees | 组合规则捕捉交互 | 仍需验证，树规则呈分段常数 |

有时房价相差几个数量级，可以对目标取log。只有正目标能直接log；改变后最小化的是log空间误差，更看重相对比例。简单exp回转一般对应log预测的反变换，不自动等于原空间条件均值；最终评价需回到任务要求的单位/指标。相关回归练习见[Tutorial4](Tutorial04.ipynb)。

来源：Lecture4b，第103个单元。


## 15. English self-test and review｜解释清楚再复习

1. **Why does ridge help with collinear features? / 为什么ridge能缓解共线性？** 答：给正则化方向增加正对角项，限制不稳定大系数。 / It stabilizes penalized directions and discourages large unstable coefficients.
2. **Does LASSO prove that a zero-weight feature is useless? / LASSO的零权重证明特征没用吗？** 答：只说明当前表示、数据与正则设置未使用它。 / It is unused in this fitted model, not universally irrelevant.
3. **What does OMP refit after selecting a feature? / OMP新选特征后重拟合什么？** 答：全部已选特征的联合系数。 / All active coefficients jointly.
4. **Does lower training MSE imply better prediction? / 训练MSE更低就一定更好？** 答：不，需验证新数据表现与假设。 / No; assess generalization on appropriate validation data.

首轮可选[现有回归卡](https://crazyshout.github.io/micro-course/cards.html#CS5489-M187) **M187（OLS与残差）、M189（截距与设计矩阵）、M194（ridge）、M207（非线性输入与线性参数）**，按卡号进入Markji；其他模型按需要分次复习。参见[最小二乘微课](https://crazyshout.github.io/micro-course/?lesson=ml19)。

## 16. Source coverage and execution boundary｜能回查，也能知道哪些跑过

本讲依据 Lecture4a（88个单元）和 Lecture4b（104个单元），单元号包含Markdown与代码，从1起算。

**数据与复算记录：** 合成例保留 `bias=30, noise=10, random_state=4487`；房价使用OpenML `house_prices`，data ID 42165、version 1，字段与哈希见数据记录。关键手算、矩阵解、房价OLS及训练内部Ridge选择见计算脚本和[结果](lecture-examples-results.json)。大型kernel/SVR/XGBoost搜索保留原课流程与原输出说明，未在此讲义中重新运行。

| 原课单元 | 本文对应 |
|---|---|
| Lecture4a，第1–12个单元 | 开篇、§1：任务、原合成例、房价与散点/三维含义 |
| Lecture4a，第13–24个单元 | §2–3：一/多维线性、OLS、偏置、推导、绘图函数 |
| Lecture4a，第25–34个单元 | §1、§4：单/双特征房价、单位与原系数 |
| Lecture4a，第35–41个单元 | §4：12特征与成对图 |
| Lecture4a，第42–49个单元 | §5：shrinkage、ridge、病态矩阵演示 |
| Lecture4a，第50–62个单元 | §5：固定划分、缩放、alpha路径、CV、系数 |
| Lecture4a，第63–80个单元 | §6：L1/L2、LASSO路径、非零数、CV |
| Lecture4a，第81–88个单元 | §7：L0、OMP及与LASSO比较、末空单元 |
| Lecture4b，第1–15个单元 | §8：离群、OLS/Ridge、手工RANSAC、库实现 |
| Lecture4b，第16–33个单元 | §9：一维多项式、sin例、Age房价、Pipeline/CV |
| Lecture4b，第34–39个单元 | §9：二维多项式及课件笔误 |
| Lecture4b，第40–52个单元 | §10：KRR、多项式/RBF、alpha/gamma搜索 |
| Lecture4b，第53–72个单元 | §11：容忍带、损失、核SVR、三参数搜索 |
| Lecture4b，第73–85个单元 | §12：集成、树、森林及各树/树数图 |
| Lecture4b，第86–96个单元 | §12：房价、训练MSE、树深CV |
| Lecture4b，第97–100个单元 | §13：boosting/XGBoost机制与原搜索 |
| Lecture4b，第101–104个单元 | §14–16：比较、归一化、目标变换、末空单元 |

原课疑点集中记录：Lecture4a，第21个单元伪逆对象需转置；Lecture4a，第44个单元截距是否惩罚需约定；Lecture4a，第54个单元“shrink to0”通常是趋近；Lecture4a，第83个单元漏掉OMP联合重拟合；Lecture4b，第34个单元末项应$x_2^3$；Lecture4b，第41个单元核ridge与OLS不无条件等价；Lecture4b，第53个单元带宽应区分半宽；Lecture4b，第101个单元 SVR损失应为epsilon-insensitive绝对损失；Lecture4b，第103个单元目标反变换不自动是原空间均值。全部在所属解释处给出条件，原件保持不变。