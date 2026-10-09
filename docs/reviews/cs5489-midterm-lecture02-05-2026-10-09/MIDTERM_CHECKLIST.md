# Lecture 2–5：考前用“能做出来”检查一遍

先遮住讲义答案，独立写关键步骤；卡在某一行时再沿链接回读。下表按你提供的四讲范围整理，不代表今年题型或分值预测。历史补充不取代当前课件。

| 讲次 | 能独立完成的任务 | 回读位置与最容易混淆的地方 |
|---|---|---|
| 2 | 从某类观测推均值、方差MLE，并说明分母 | [高斯MLE](../../../CS5489/course-notes/Lecture02.md#gaussian-mle)：MLE除N；无偏样本方差除N−1 |
| 2 | 密度×先验→后验→类别；先验改变后重算 | [Bayes决策](../../../CS5489/course-notes/Lecture02.md#bayes-rule)：密度不是“恰好取这个值的概率” |
| 2 | 判断共享/不同方差时哪些二次项抵消 | [边界](../../../CS5489/course-notes/Lecture02.md#decision-boundaries)：条件独立不等于边界线性 |
| 2 | 区分出现篇数、词次数、TF-IDF权重，再平滑 | [Bernoulli](../../../CS5489/course-notes/Lecture02.md#bernoulli)、[Multinomial](../../../CS5489/course-notes/Lecture02.md#multinomial)：分母分别是N_c+2α与总词数+Vα |
| 3 | 写LR目标和梯度，解释C/L1/L2及一次更新 | [Logistic](../../../CS5489/course-notes/Lecture03.md#logistic)、[正则](../../../CS5489/course-notes/Lecture03.md#regularization)：小C为强正则；标签±1与0/1不能混代 |
| 3 | 从约束解释间隔、slack、乘子三种情形 | [SVM](../../../CS5489/course-notes/Lecture03.md#svm)、[对偶](../../../CS5489/course-notes/Lecture03.md#dual)：间隔内仍可能分类正确；α=C不等于必定错分 |
| 3 | 算核矩阵，解释合法性、存储与调参 | [核](../../../CS5489/course-notes/Lecture03.md#kernels)：矩阵元素全为正不等于半正定；测试集不用于选参 |
| 4 | 写OLS矩阵形状与正规方程，和均值基线比较 | [OLS](../../../CS5489/course-notes/Lecture04.md#ols)：秩亏仍有最优解；训练集结论不自动适用于验证集 |
| 4 | 比较Ridge、LASSO、OMP及历史Elastic Net | [Ridge](../../../CS5489/course-notes/Lecture04.md#ridge)、[LASSO](../../../CS5489/course-notes/Lecture04.md#lasso)：权重惩罚与残差损失分开；OMP联合重拟合 |
| 4 | 算残差损失，解释RF平均与boosting更新 | [损失](../../../CS5489/course-notes/Lecture04.md#regression-losses)、[集成](../../../CS5489/course-notes/Lecture04.md#ensembles)：r=y−ŷ时正残差代表低估；相关树仍有共同波动 |
| 5 | 感知机更新、softmax概率、交叉熵与p−y | [感知机](../../../CS5489/course-notes/Lecture05.md#perceptron)、[反传](../../../CS5489/course-notes/Lecture05.md#backprop)：零分数规则写清；p−y有特定损失/输出组合 |
| 5 | 换成tanh与平方误差，重新列局部导数 | [标量回归反传](../../../CS5489/course-notes/Lecture05.md#scalar-regression-backprop)：因子2、输出权重、激活导数、输入都不能漏 |
| 5 | 两层矩阵反传与参数计数；解释批量、动量与早停 | [两层例题](../../../CS5489/course-notes/Lecture05.md#worked-two-layer)、[训练](../../../CS5489/course-notes/Lecture05.md#training)：只除一次批量数，先算完梯度再同时更新，恢复最佳验证参数 |

最后用英文独立解释四件事：Why can Naive Bayes make errors with unlimited data? What does a nonzero SVM multiplier tell us? How do a loss and a regularizer differ? Why is backpropagation not the same operation as a parameter update?

这些问题的关键要点分别是分布重叠/假设失配、对应KKT条件、残差或分类拟合与参数代价、计算导数与沿梯度改参数。能说清条件，比只背算法名称更有用。
