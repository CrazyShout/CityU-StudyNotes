# 逐项修改前后对照

以下保留每次局部修订的原文、改文及理由。行号为实施该项修改时的位置；当前位置以逐节表为准。少数位置经过二读再次修订，最终内容以TeX主稿为准。自动生成的索引正文由模板和生成器决定。

## E001 · CS5489/course-notes/Lecture01.tex:227

恢复题面被旧转换吞掉的乘号；明确中英同一操作序列。

原文：
```tex
\textbf{Q / 题：} x=2，先执行x+=3再执行x\emph{=2，结果是什么？ / Starting with x=2, apply x+=3 and then x}=2.\\
```

改为：
```tex
\textbf{Q / 题：} 初始\StudyInline{x=2}，依次执行\StudyInline{x+=3}和\StudyInline{x*=2}，结果是什么？ / Starting with \StudyInline{x=2}, apply \StudyInline{x+=3} and then \StudyInline{x*=2}. What is the result?\\
```

## E002 · CS5489/course-notes/Lecture01.tex:197

去除来源注多余空格。

原文：
```tex
来源： Lecture1a，第1–14个单元、Lecture 1 Intro，第6页。
```

改为：
```tex
来源：Lecture1a，第1–14个单元、Lecture 1 Intro，第6页。
```

## E003 · CS5489/course-notes/Lecture01.tex:806

数据质量限制已在§1解释；修正后移表格留下的过时指向。

原文：
```tex
原Intro中的“More data is better”需结合数据质量、采样和评价方式理解。软件版本差异在对应段落说明；学习优先级的依据见开头表格。
```

改为：
```tex
软件版本差异在对应段落说明；学习优先级及其依据见\StudyRef{CS5489-Lecture01}{learning-priorities}{学习要求表}。
```

## E004 · CS5489/course-notes/Lecture01.tex:44

简化已由目录体现的顺序说明，保留检索入口。

原文：
```tex
学习目标、难度与材料依据集中在\StudyRef{CS5489-Lecture01}{learning-priorities}{文末学习要求表}；正文按原课顺序展开。
```

改为：
```tex
学习目标与难点见\StudyRef{CS5489-Lecture01}{learning-priorities}{文末学习要求表}。
```

## E005 · CS5489/course-notes/Lecture01.tex:180

标题直接定位本节关键概念。

原文：
```tex
4. Python and Jupyter｜一本有记忆的实验笔记
```

改为：
```tex
4. Python and Jupyter｜内核状态与执行顺序
```

## E006 · CS5489/course-notes/Lecture01.tex:239

用具体概念替代泛化包装，保留原英文检索标题。

原文：
```tex
6. Lists, tuples, strings, dictionaries, sets｜先选对装东西的方式
```

改为：
```tex
6. Lists, tuples, strings, dictionaries, sets｜容器的用途与操作
```

## E007 · CS5489/course-notes/Lecture01.tex:495

标题区分本节实际三种运算。

原文：
```tex
12. Brief linear algebra review｜同一个乘号前后可能是不同东西
```

改为：
```tex
12. Brief linear algebra review｜内积、外积与矩阵乘法
```

## E008 · CS5489/course-notes/Lecture02.tex:1625

为远处参数增加纸面页码入口，保留同一拟合值。

原文：
```tex
仍用第二部分的花瓣高斯参数，
```

改为：
```tex
沿用\StudyRef{CS5489-Lecture02}{gaussian-mle}{花瓣高斯参数表}，
```

## E009 · CS5489/course-notes/Lecture02.tex:1625

英文题干同步提供参数定位。

原文：
```tex
Use the petal-length Gaussians from Part 2 at 5 cm,
```

改为：
```tex
Use the \StudyRef{CS5489-Lecture02}{gaussian-mle}{fitted petal-length Gaussians} at 5 cm,
```

## E010 · CS5489/course-notes/Lecture02.tex:1661

为长讲末尾的独立变式提供数据回查页码。

原文：
```tex
使用第六部分固定词表、已拟合的平滑IDF、L1规则、alpha=1的词参数和相等先验，
```

改为：
```tex
使用\StudyRef{CS5489-Lecture02}{tfidf}{第六部分}的固定词表、已拟合的平滑IDF、L1规则、alpha=1的词参数和相等先验，
```

## E011 · CS5489/course-notes/Lecture02.tex:1661

英文同步保留同一数据入口。

原文：
```tex
Using Part 6's fixed vocabulary,
```

改为：
```tex
Using \StudyRef{CS5489-Lecture02}{tfidf}{Part 6}'s fixed vocabulary,
```

## E012 · CS5489/course-notes/Lecture02.tex:614

消除会随修订失效的时间称谓。

原文：
```tex
{本轮计算记录}
```

改为：
```tex
{计算记录}
```

## E013 · CS5489/course-notes/Lecture02.tex:1758

保留复算入口，把版本/哈希等维护细节留在链接记录。

原文：
```tex
TF-IDF的平滑IDF与NB的alpha作用不同：前者调整跨文档的词权重，后者平滑类别内的词参数。本文四文档演算与单个错分邮件的版本、输入哈希和交叉检查见\StudyRepoRef{docs/reviews/lecture02-2026-10-08/calculations.json}{}{计算记录}，重算方式见\StudyRepoRef{docs/reviews/lecture02-2026-10-08/README.md}{}{本轮说明}。
```

改为：
```tex
TF-IDF的平滑IDF与NB的alpha作用不同：前者调整跨文档的词权重，后者平滑类别内的词参数。四文档演算与错分邮件的\StudyRepoRef{docs/reviews/lecture02-2026-10-08/calculations.json}{}{计算记录}和\StudyRepoRef{docs/reviews/lecture02-2026-10-08/README.md}{}{复算说明}可用于核对结果。
```

## E014 · latex/exam/Lecture01-topics.tex.in:12

计数规则由随后口径段完整说明，去掉相邻重复。

原文：
```tex
题号和页码指向原题纸；同一考点在同卷出现多题仍只计一次。完整期中题答已按考点在本地另册维护；期末与QE题目可按下表回查原材料。
```

改为：
```tex
题号和页码指向原题纸。完整期中题答见独立题库；期末与QE题目可按下表回查原材料。
```

## E015 · latex/exam/Lecture01-topics.tex.in:24

当前已在讲末索引，删除指向自身的导航。

原文：
```tex
题号见\StudyRef{CS5489-Lecture01}{exam-topic-index}{讲末索引}，材料身份见\StudyRef{CS5489-ExamIndex}{root}{全册附录}。
```

改为：
```tex
按试卷查题及核对材料身份，见\StudyRef{CS5489-ExamIndex}{root}{全册附录}。
```

## E016 · latex/exam/Lecture03-topics.tex.in:12

计数规则由随后口径段完整说明，去掉相邻重复。

原文：
```tex
题号和页码指向原题纸；同一考点在同卷出现多题仍只计一次。完整期中题答已按考点在本地另册维护；期末与QE题目可按下表回查原材料。
```

改为：
```tex
题号和页码指向原题纸。完整期中题答见独立题库；期末与QE题目可按下表回查原材料。
```

## E017 · latex/exam/Lecture03-topics.tex.in:24

当前已在讲末索引，删除指向自身的导航。

原文：
```tex
题号见\StudyRef{CS5489-Lecture03}{exam-topic-index}{讲末索引}，材料身份见\StudyRef{CS5489-ExamIndex}{root}{全册附录}。
```

改为：
```tex
按试卷查题及核对材料身份，见\StudyRef{CS5489-ExamIndex}{root}{全册附录}。
```

## E018 · latex/exam/Lecture04-topics.tex.in:12

计数规则由随后口径段完整说明，去掉相邻重复。

原文：
```tex
题号和页码指向原题纸；同一考点在同卷出现多题仍只计一次。完整期中题答已按考点在本地另册维护；期末与QE题目可按下表回查原材料。
```

改为：
```tex
题号和页码指向原题纸。完整期中题答见独立题库；期末与QE题目可按下表回查原材料。
```

## E019 · latex/exam/Lecture04-topics.tex.in:24

当前已在讲末索引，删除指向自身的导航。

原文：
```tex
题号见\StudyRef{CS5489-Lecture04}{exam-topic-index}{讲末索引}，材料身份见\StudyRef{CS5489-ExamIndex}{root}{全册附录}。
```

改为：
```tex
按试卷查题及核对材料身份，见\StudyRef{CS5489-ExamIndex}{root}{全册附录}。
```

## E020 · latex/exam/Lecture05-topics.tex.in:12

计数规则由随后口径段完整说明，去掉相邻重复。

原文：
```tex
题号和页码指向原题纸；同一考点在同卷出现多题仍只计一次。完整期中题答已按考点在本地另册维护；期末与QE题目可按下表回查原材料。
```

改为：
```tex
题号和页码指向原题纸。完整期中题答见独立题库；期末与QE题目可按下表回查原材料。
```

## E021 · latex/exam/Lecture05-topics.tex.in:24

当前已在讲末索引，删除指向自身的导航。

原文：
```tex
题号见\StudyRef{CS5489-Lecture05}{exam-topic-index}{讲末索引}，材料身份见\StudyRef{CS5489-ExamIndex}{root}{全册附录}。
```

改为：
```tex
按试卷查题及核对材料身份，见\StudyRef{CS5489-ExamIndex}{root}{全册附录}。
```

## E022 · latex/exam/Lecture02-topics.tex.in:12

同卷计数在下一段说明，避免相邻重复。

原文：
```tex
各行保留原题号与原材料页码。同一卷在本表不同考点下出现，不会让该考点的卷数重复增加。材料文件、配套答案与版本差异见\StudyRef{CS5489-ExamIndex}{root}{按卷附录}。
```

改为：
```tex
各行保留原题号与原材料页码。材料文件、配套答案与版本差异见\StudyRef{CS5489-ExamIndex}{root}{按卷附录}。
```

## E023 · latex/exam/Lecture02-topics.tex.in:21

去掉索引内自指和同页重复附录入口，保留具体范围边界。

原文：
```tex
题号与出处见\StudyRef{CS5489-Lecture02}{exam-topic-index}{讲末考点索引}；按试卷查阅见\StudyRef{CS5489-ExamIndex}{root}{全册附录}。期末聚类是关联选做；QE参数后验不等于本讲的类别后验。
```

改为：
```tex
期末聚类是关联选做；QE参数后验不等于本讲的类别后验。
```

## E024 · scripts/build_exam_annotations.py:87

按完整分号子句去重同一考点的来源条件；台账文本不修改。

原文：
```tex
notes=list(dict.fromkeys(q['review_note'] for q in d['questions'] if t['id'] in q['topics'] and q.get('review_note')))
```

改为：
```tex
# A ledger note may contain several clauses repeated by other questions.
                notes=list(dict.fromkeys(clause.strip().rstrip('。') for q in d['questions']
                    if t['id'] in q['topics'] and q.get('review_note')
                    for clause in q['review_note'].split('；') if clause.strip().rstrip('。')))
```

## E025 · scripts/build_exam_annotations.py:92

长期讲义不使用本轮时间称谓。

原文：
```tex
'本轮复习重点' if n==2 else '复习动作'
```

改为：
```tex
'复习重点' if n==2 else '复习动作'
```

## E026 · latex/exam/appendix.tex.in:13

所在位置由目录体现，删除制作时序说明。

原文：
```tex
本附录按独立试卷整理本轮已核对的对应题目，放在Assignment之后。
```

改为：
```tex
本附录按独立试卷整理已核对的对应题目。
```

## E027 · CS5489/course-notes/Lecture03.tex:47

保留定位入口，去掉目录已体现的顺序说明。

原文：
```tex
学习目标、难度与材料依据集中在\StudyRef{CS5489-Lecture03}{learning-priorities}{文末学习要求表}；正文按原课顺序展开。
```

改为：
```tex
学习目标与难点见\StudyRef{CS5489-Lecture03}{learning-priorities}{文末学习要求表}。
```

## E028 · CS5489/course-notes/Lecture03.tex:112

标题使用具体概念，修正一张线的生硬搭配。

原文：
```tex
2. Linear classifier and separating hyperplane｜一张有方向的分界线
```

改为：
```tex
2. Linear classifier and separating hyperplane｜线性分数与分类边界
```

## E029 · CS5489/course-notes/Lecture03.tex:178

用概率与损失的关系替代拟人修辞，保留非错误计数的实质区别。

原文：
```tex
损失是“对真实答案有多不买账”，不是错误样本的简单计数。即使分对但信心不足，损失仍不为零。
```

改为：
```tex
模型给真实类别的概率越低，负对数损失越大。即使分类正确，只要真实类别概率小于1，损失仍大于0。
```

## E030 · CS5489/course-notes/Lecture03.tex:204

把数学推导与软件目标缩放分段。

原文：
```tex
偏置在这份公式里未被惩罚。库中的
```

改为：
```tex
偏置在这份公式里未被惩罚。

实现中，库采用的
```

## E031 · CS5489/course-notes/Lecture03.tex:350

标题直接定位本节的距离尺度问题。

原文：
```tex
7. Maximum margin｜不仅分开，还想留出余地
```

改为：
```tex
7. Maximum margin｜间隔与距离归一化
```

## E032 · CS5489/course-notes/Lecture03.tex:796

比较表标题直接说明比较维度。

原文：
```tex
14. Classification summary｜把不同方法放在同一张地图
```

改为：
```tex
14. Classification summary｜比较训练目标、输出与条件
```

## E033 · CS5489/course-notes/Lecture04.tex:47

精简导航，保留学习要求入口。

原文：
```tex
学习目标、难度与材料依据集中在\StudyRef{CS5489-Lecture04}{learning-priorities}{文末学习要求表}；正文按原课顺序展开。
```

改为：
```tex
学习目标与难点见\StudyRef{CS5489-Lecture04}{learning-priorities}{文末学习要求表}。
```

## E034 · CS5489/course-notes/Lecture04.tex:59

避免竖直与垂直在同句中造成含混，保留残差与几何距离区别。

原文：
```tex
不是点到直线的最短垂直距离。
```

改为：
```tex
不是点到拟合直线的最短距离。
```

## E035 · CS5489/course-notes/Lecture04.tex:256

英文补齐中文已有的三点条件；答案和计算不变。

原文：
```tex
Add one to every output in the worked example; how do w, b and MSE change?
```

改为：
```tex
For the points (0,2), (1,3) and (2,3), find the OLS slope, intercept and MSE. How do they compare with the preceding example?
```

## E036 · CS5489/course-notes/Lecture04.tex:374

标题落在明确机制，不使用模糊强调。

原文：
```tex
6. LASSO｜有时需要真的把系数变成零
```

改为：
```tex
6. LASSO｜L1惩罚与零系数
```

## E037 · CS5489/course-notes/Lecture04.tex:549

分开图的实验条件与抽样概率推理。

原文：
```tex
成功仍依赖足够的一致点、合理模型与阈值。补充概率：
```

改为：
```tex
成功仍依赖足够的一致点、合理模型与阈值。

抽样成功率可以进一步计算：
```

## E038 · CS5489/course-notes/Lecture04.tex:700

由重复读图指令改为两图对应关系。

原文：
```tex
图左先看容忍带，图右看损失的平底。C决定违约代价，
```

改为：
```tex
图右损失曲线的平底对应左图的容忍带。C决定违约代价，
```

## E039 · CS5489/course-notes/Lecture04.tex:1019

标题明确结果身份，不用含混的哪些跑过。

原文：
```tex
16. Source coverage and execution boundary｜能回查，也能知道哪些跑过
```

改为：
```tex
16. Source coverage and execution boundary｜来源、保存结果与复算范围
```

## E040 · CS5489/course-notes/Lecture05.tex:21

简化通用导航，保留目标表。

原文：
```tex
学习目标、难度与材料依据集中在\StudyRef{CS5489-Lecture05}{learning-priorities}{文末学习要求表}；正文按原课顺序展开。
```

改为：
```tex
学习目标与难点见\StudyRef{CS5489-Lecture05}{learning-priorities}{文末学习要求表}。
```

## E041 · CS5489/course-notes/Lecture05.tex:117

修正吸收入输入的重复字词。

原文：
```tex
省略的偏置仍可吸收入输入。
```

改为：
```tex
省略的偏置仍可吸收入向量。
```

## E042 · CS5489/course-notes/Lecture05.tex:141

补齐变式原logits，避免题目单独读时缺少计算输入。

原文：
```tex
全部logit加100，概率改变吗？若全部乘2呢？ / What happens after adding 100 to every logit, or multiplying all logits by two?
```

改为：
```tex
原logits为(ln2,ln3,ln5)。全部加100，概率改变吗？若全部乘2呢？ / Starting from logits (ln2,ln3,ln5), what happens to the probabilities after adding 100 to every logit, or multiplying all logits by two?
```

## E043 · CS5489/course-notes/Lecture05.tex:235

英文补明确所求量，中英共同补齐已有概率与损失条件。

原文：
```tex
同样概率但真类2，logit梯度是什么？ / Change only the true label to class 2.
```

改为：
```tex
单样本softmax交叉熵，概率为(0.2,0.3,0.5)，真类为2，logit梯度是什么？ / For single-sample softmax cross-entropy with probabilities (0.2,0.3,0.5) and true class 2, find the logit gradient.
```

## E044 · CS5489/course-notes/Lecture05.tex:303

图注已定位两个坐标图；正文直接解释不可微点。

原文：
```tex
左图看响应值，右图看局部斜率。ReLU在0处
```

改为：
```tex
ReLU在0处
```

## E045 · CS5489/course-notes/Lecture05.tex:314

将英文已有的全连接/偏置条件补到中文题干。

原文：
```tex
4输入、3隐藏、2输出，参数多少？ / Count parameters
```

改为：
```tex
全连接网络有4个输入、3个隐藏节点、2个输出，隐藏层和输出层均带偏置。参数多少？ / Count parameters
```

## E046 · CS5489/course-notes/Lecture05.tex:650

自测补齐初始状态和参数，保留原更新约定而不泄露计算式。

原文：
```tex
在同样初值与参数下，两批梯度均为2，第二步后\ensuremath{\theta}是多少？ / With the same initial state, learning rate 0.1 and momentum 0.9, use gradients 2 and 2. What is \ensuremath{\theta} after two steps?
```

改为：
```tex
沿用本节动量更新约定，初始参数为1、初始速度为0，学习率0.1、动量系数0.9，两批梯度均为2。第二步后\ensuremath{\theta}是多少？ / Use this section\textquotesingle{}s momentum convention, initial parameter 1, initial velocity 0, learning rate 0.1 and momentum 0.9, with gradients 2 and 2. What is \ensuremath{\theta} after two steps?
```

## E047 · CS5489/course-notes/Tutorial01.tex:45

表内已有每项原任务依据，删除同义表后说明。

原文：
```tex
优先级依据上列原任务。


```

改为：
```tex

```

## E048 · CS5489/course-notes/Tutorial01.tex:104

标题定位实际技能。

原文：
```tex
2. Count factors｜先写人能逐行跟上的版本
```

改为：
```tex
2. Count factors｜循环范围与因子计数
```

## E049 · CS5489/course-notes/Tutorial01.tex:133

短答案补原题排除1和自身的条件，避免only divisor的错误概括。

原文：
```tex
9只有3，得到1；13为素数，得到0。 / 9 has only divisor 3, giving 1; 13 is prime, giving 0.
```

改为：
```tex
9除1和自身外只有正因子3，得到1；13为素数，得到0。 / The only positive divisor of 9 other than 1 and itself is 3, giving 1; 13 is prime, giving 0.
```

## E050 · CS5489/course-notes/Tutorial02.tex:21

学生说明给实际学习步骤，去掉代码维护表述。

原文：
```tex
复现时从头运行Notebook，独立尝试题在讲义中阅读，不阻断参考代码。
```

改为：
```tex
复现时从头运行Notebook，再完成讲义中的独立尝试题。
```

## E051 · CS5489/course-notes/Tutorial02.tex:61

表格已有当前任务依据；删除翻译过程自述。

原文：
```tex
优先级依据当前任务。英文题意为忠实整理，中文解释补足必要条件；代码、类别名称和原文件名不翻译。


```

改为：
```tex

```

## E052 · CS5489/course-notes/Tutorial02.tex:337

明确结果身份，避免指向正在执行的新实验。

原文：
```tex
本次固定样本的读法 / Reading the current examples
```

改为：
```tex
保存输出中的错分样本 / Errors in the saved outputs
```

## E053 · CS5489/course-notes/Tutorial02.tex:484

上一段已说明模板未定义平滑公式；选读集中解释概率依据。

原文：
```tex
它是本参考实现明确选用的补充约定，教师模板只提供alpha接口，没有指定该公式。后验均值与MAP是不同估计；
```

改为：
```tex
后验均值与MAP是不同估计；
```

## E054 · CS5489/course-notes/Tutorial02.tex:624

标题说明本节实际内容，不重复安排学习动作。

原文：
```tex
10. 回原课、练英文、再刷少量卡 / Return and recall
```

改为：
```tex
10. 英文自测与复习入口 / Return and recall
```

## E055 · CS5489/course-notes/Tutorial03.tex:11

标题用实验对象替代提醒式修辞。

原文：
```tex
从同一份数据比较模型，别让实验条件悄悄换了
```

改为：
```tex
线性分类、图像裁剪与核方法的对照实验
```

## E056 · CS5489/course-notes/Tutorial03.tex:242

英文补齐中文已有切片范围。

原文：
```tex
What dimension follows from this alternative crop, and can 396-dimensional weights be reused?
```

改为：
```tex
For crop [17:41,8:32], what is the input dimension, and can 396-dimensional weights be reused?
```

## E057 · CS5489/course-notes/Tutorial03.tex:330

中英文同时明确其他像素不变。

原文：
```tex
What happens to the score if one pixel increases by 0.1?
```

改为：
```tex
What happens to the score if one pixel increases by 0.1 while all other pixels stay fixed?
```

## E058 · CS5489/course-notes/Tutorial03.tex:362

保存结果段已给完整身份，参数选择在§0说明，不在结尾重复。

原文：
```tex
上述结果来自本参考实现，参数和划分见§0。原题未指定唯一的最优参数。

```

改为：
```tex

```

## E059 · CS5489/course-notes/Tutorial04.tex:83

用数据对象替代戏剧化提醒。

原文：
```tex
2. Load and inspect｜不要把答案偷偷塞进输入
```

改为：
```tex
2. Load and inspect｜计数目标与输入特征
```

## E060 · CS5489/course-notes/Tutorial04.tex:91

直接解释可用信息与目标泄漏，去掉无关反面说法。

原文：
```tex
删除它们不是嫌数据多，是因为预测当天总量时不能先知道当天两类人的完整数量。
```

改为：
```tex
预测当天总量时，还不知道当天两类人的完整数量，因此须从输入中删除这两列。
```

## E061 · CS5489/course-notes/Tutorial04.tex:132

标题直接定位基线和评价单位。

原文：
```tex
3. A baseline and interpretable errors｜先问模型有没有赢过“每天报同一个数”
```

改为：
```tex
3. A baseline and interpretable errors｜常数基线与误差单位
```

## E062 · CS5489/course-notes/Tutorial04.tex:186

标题定位实际学习难点。

原文：
```tex
4. LASSO and OMP｜“重要特征”不是一份永久排行榜
```

改为：
```tex
4. LASSO and OMP｜相关特征与系数解释
```

## E063 · CS5489/course-notes/Tutorial04.tex:165

直接给坐标定义，去掉重复命令式开头。

原文：
```tex
读图先确认横轴！这里沿用老师Tutorial4，第32个单元的代码：
```

改为：
```tex
这里沿用老师Tutorial4，第32个单元的代码：
```

## E064 · CS5489/course-notes/Tutorial04.tex:171

英文与中文保存输出身份一致。

原文：
```tex
OLS slightly outperforms ridge in this run;
```

改为：
```tex
In the saved results, OLS slightly outperforms ridge;
```

## E065 · CS5489/course-notes/Tutorial04.tex:307

直接说明两个模型分工，删除没有帮助的比喻。

原文：
```tex
残差方法像给旧地图贴修订便签：旧模型负责已有规律，新模型学“还差多少”。
```

改为：
```tex
残差修正保留旧模型，由新模型预测旧模型尚未解释的差值。
```

## E066 · CS5489/course-notes/Tutorial04.tex:326

表格保留全部四组结果；正文只解释关键比较和平均残差，两种语言明确保存结果。

原文：
```tex
保存结果的同一275天测试集上，旧模型、新数据单独、合并、残差修正RMSE分别为2311.86、1281.87、1042.12、1832.61。合并方案最好；残差修正仍有明显过预测，平均真值减预测为\ensuremath{-}1362.37，提示早春的偏差规律未充分代表其余季节。 / Pooled retraining is best in this run; residual adaptation overpredicts the held-out months.
```

改为：
```tex
在保存结果的同一275天测试集上，合并重训的RMSE最低，为1042.12。残差修正仍整体高估，平均真值减预测为\ensuremath{-}1362.37，提示早春的偏差规律未充分代表其余季节。 / In the saved results for the same 275 held-out days, pooled retraining has the lowest RMSE (1042.12). Residual adaptation still overpredicts, with a mean truth-minus-prediction residual of -1362.37.
```

## E067 · CS5489/course-notes/Assignment01.tex:8

标题具体标出本指南的工作内容。

原文：
```tex
从课堂概率模型到一个可解释、可复现的短信分类实验
```

改为：
```tex
短信分类的数据、评价与验证流程
```

## E068 · CS5489/course-notes/Assignment01.tex:105

避免把已保存文件检查称为本轮新检查。

原文：
```tex
本次实际文件如下。
```

改为：
```tex
课程提供的文件如下。
```

## E069 · CS5489/course-notes/Assignment01.tex:568

删除全册来源说明已涵盖的反复自证，保留本任务依据。

原文：
```tex
本指南不把历史作业的做法当作这次作业要求；跨讲方法明确标来源。主要根据当前两份模板和实际文件，
```

改为：
```tex
本指南依据当前两份模板和所给数据文件，
```

## E070 · CS5489/course-notes/Assignment02.tex:164

中文与英文所求数值和符号一致。

原文：
```tex
u=0.5、n=2、上游导数3，两个梯度的符号？
```

改为：
```tex
u=0.5、n=2、上游导数3，求对输入和指数的两个梯度及其符号。
```

## E071 · CS5489/course-notes/Assignment02.tex:171

英文补中文已有关键数值，保持原算例。

原文：
```tex
The input gradient is 3; the exponent gradient is negative because increasing the exponent shrinks a base below one.
```

改为：
```tex
The input gradient is 3; the exponent gradient is approximately \ensuremath{-}0.5199. It is negative because increasing the exponent shrinks a base below one.
```

## E072 · CS5489/course-notes/Assignment02.tex:336

把原有四项英文自查对应为中英问题和完整短答案，补足数据/接口条件。

原文：
```tex
\textbf{English self-check:} Explain where the batch averaging occurs, why a shared exponent receives a summed gradient, how leakage is prevented, and which variables were held fixed in an optimizer comparison.
```

改为：
```tex
\textbf{Q1 / 题：} 本指南在何处计入批量平均？ / Where does this guide apply batch averaging?

\textbf{答 / Answer：} 在反传入口除以批量大小一次，后续各层传回已缩放的梯度。 / Divide by batch size once at the start of backpropagation; subsequent layers propagate the scaled gradients.

\textbf{Q2 / 题：} 共享指数为什么收到多个位置的梯度之和？ / Why does a shared exponent receive a sum of gradient contributions?

\textbf{答 / Answer：} 同一指数用于多个激活位置，按链式法则累加各位置对它的贡献；负区与指数无关，贡献为0。 / The same exponent is used at multiple activation positions, so their chain-rule contributions add. The negative branch does not depend on the exponent and contributes zero.

\textbf{Q3 / 题：} 怎样避免缩放时使用测试信息？ / How do you prevent test information from entering feature scaling?

\textbf{答 / Answer：} 先划分数据，只在相应训练部分拟合缩放量，再用同一变换处理验证和测试数据。 / Split first, fit scaling on the relevant training partition, then reuse that transform for validation and test data.

\textbf{Q4 / 题：} 额外设计受控优化器比较时，应固定哪些条件？ / Which conditions should be fixed in an additional controlled optimizer comparison?

\textbf{答 / Answer：} 固定目标函数、初值、迭代预算、学习率与噪声设置；研究其中某项时单独改变它。原题指定的不同迭代预算仍单独报告。 / Hold the objective, initial state, iteration budget, learning rate and noise settings fixed; vary one when studying its effect. Report the original exercise's unequal iteration budgets separately.
```

## E073 · scripts/build_exam_annotations.py:128

按卷附录使用同样的完整子句去重，不丢不同题源条件。

原文：
```tex
notes=list(dict.fromkeys(q.get('review_note','') for n,q,o in pairs if q.get('review_note')))
```

改为：
```tex
notes=list(dict.fromkeys(clause.strip().rstrip('。') for n,q,o in pairs
            if q.get('review_note') for clause in q['review_note'].split('；')
            if clause.strip().rstrip('。')))
```

## E074 · scripts/build_exam_annotations.py:131

去除会随修订失效的本轮称谓。

原文：
```tex
扫描手写作答不作为标准答案；本轮只记录印刷题面要求
```

改为：
```tex
扫描手写作答不作为标准答案；仅记录印刷题面要求
```

## E075 · scripts/build_exam_annotations.py:131

原卷身份和台账条件已经说明印刷题面/手写解答，删除额外重复声明。

原文：
```tex
        if p['id']=='M25A':notes.insert(0,'扫描手写作答不作为标准答案；仅记录印刷题面要求')

```

改为：
```tex

```

## E076 · scripts/build_exam_annotations.py:131

QE年份、覆盖和卷次身份已在表前/后完整说明；核对注只保留跨页与解答身份，避免近义条件反复堆叠。

原文：
```tex
        if notes:parts += [r'\textbf{核对说明：}'+escape('；'.join(notes)+'。')]
```

改为：
```tex
        if p['id']=='QE-U':
            # Year, coverage and independent-paper identity are stated before/after the table.
            notes=['部分图与问题跨两个原页，须一起读取；手写解答不作为标准答案']
        if notes:parts += [r'\textbf{核对说明：}'+escape('；'.join(notes)+'。')]
```

## E077 · CS5222/course-notes/Chapter01.tex:20

保留检索入口，精简重复顺序说明。

原文：
```tex
学习目标、难度与材料依据集中在\StudyRef{CS5222-Chapter01}{learning-priorities}{文末学习要求表}；正文按原课顺序展开。
```

改为：
```tex
学习目标与难点见\StudyRef{CS5222-Chapter01}{learning-priorities}{文末学习要求表}。
```

## E078 · CS5222/course-notes/Chapter02.tex:20

保留检索入口，精简重复顺序说明。

原文：
```tex
学习目标、难度与材料依据集中在\StudyRef{CS5222-Chapter02}{learning-priorities}{文末学习要求表}；正文按原课顺序展开。
```

改为：
```tex
学习目标与难点见\StudyRef{CS5222-Chapter02}{learning-priorities}{文末学习要求表}。
```

## E079 · CS5222/course-notes/Chapter03.tex:24

保留检索入口，精简重复顺序说明。

原文：
```tex
学习目标、难度与材料依据集中在\StudyRef{CS5222-Chapter03}{learning-priorities}{文末学习要求表}；正文按原课顺序展开。
```

改为：
```tex
学习目标与难点见\StudyRef{CS5222-Chapter03}{learning-priorities}{文末学习要求表}。
```

## E080 · CS5222/course-notes/Chapter01.tex:10

直接交代实际对象和路径，不先设置一个无关错误说法。

原文：
```tex
中间不是一条从电脑直达学校服务器的专属电线，而是许多设备、链路和网络共同协作。
```

改为：
```tex
请求通常经过多个设备、链路和网络才到达服务器。
```

## E081 · CS5222/course-notes/Chapter01.tex:78

已有DSL车道类比后回到网络对象。

原文：
```tex
后面的道路仍可能与别人共享。
```

改为：
```tex
后续链路仍可能与其他用户共享。
```

## E082 · CS5222/course-notes/Chapter01.tex:120

标题直接概括两种机制。

原文：
```tex
4. Circuit versus packet switching｜预留座位，还是来了再排队
```

改为：
```tex
4. Circuit versus packet switching｜预留资源与按需共享
```

## E083 · CS5222/course-notes/Chapter01.tex:137

本段已说明按需共享与竞争排队，删除不增加机制的食堂比喻。

原文：
```tex
像食堂公共座位提高利用率，但午饭同时来的人多了还是要等，不能只记“共享比较好”。
```

改为：
```tex

```

## E084 · CS5222/course-notes/Chapter01.tex:175

删除作者对类比的评价，直接说明分布式条件。

原文：
```tex
导航规划与开到路口选出口的类比有帮助，但真实路由可能分布式更新，不必有一个中央导航员。
```

改为：
```tex
路由信息可以由多个设备协作更新，不必由一个中心统一计算。
```

## E085 · CS5222/course-notes/Chapter01.tex:369

前两句已经给出分层与接口作用，删除同义总结。

原文：
```tex
网络分层借助清楚的责任和接口组织复杂任务。
```

改为：
```tex

```

## E086 · CS5222/course-notes/Chapter02.tex:217

标题直接定位DNS对象，删除未展开的通讯录比喻。

原文：
```tex
7. DNS services and hierarchy｜通讯录不是只放在一台电脑上
```

改为：
```tex
7. DNS services and hierarchy｜分布式命名与查询层次
```

## E087 · CS5222/course-notes/Chapter02.tex:701

标题说明检索用途。

原文：
```tex
15. Source coverage and cautions｜每一页有去处
```

改为：
```tex
15. Source coverage and cautions｜来源覆盖与版本差异
```

## E088 · CS5222/course-notes/Chapter02.tex:349

补齐独立变式的数据及英文所求量，原计算不变。

原文：
```tex
同条件但各peer上传0，P2P下界？ / Set every peer upload rate to zero; keep all other parameters.
```

改为：
```tex
沿用本节理想容量模型：F=100 Mbit、N=4、服务器上传10 Mbps、各peer下载5 Mbps且不上传。P2P分发时间下界是多少？ / In the ideal capacity model, let F=100 Mbit and N=4, with server upload 10 Mbps, each peer downloading at 5 Mbps and uploading at zero. Find the P2P distribution-time lower bound.
```

## E089 · CS5222/course-notes/Chapter02.tex:388

中英补齐邻居持有集合，使变式不依赖远处例题。

原文：
```tex
保持上例，Alice仍缺A/B/C。P2离开后，A、B、C在剩余邻居中各有几份，下一请求是否唯一？若P3也离开，C是否仍可立即下载？ / Alice still lacks A, B and C. After P2 leaves, count the visible copies and identify the rarest candidates. If P3 also leaves, is C immediately available from the remaining neighbors?
```

改为：
```tex
Alice缺A/B/C三个块；P1持有A、B，P2持有A、B，P3持有A、C。P2离开后，各块在剩余邻居中各有几份，下一请求是否唯一？若P3也离开，C是否仍可立即下载？ / Alice lacks A, B and C. P1 and P2 each hold A and B; P3 holds A and C. After P2 leaves, count the visible copies and identify the rarest candidates. If P3 also leaves, is C immediately available from the remaining neighbors?
```

## E090 · CS5222/course-notes/Chapter02.tex:531

英文补齐中文消息内容和两个协议。

原文：
```tex
Run both transports with this message, then explain the two server-side TCP sockets.
```

改为：
```tex
Run UDP and TCP with the message course practice, then explain the two server-side TCP sockets.
```

## E091 · CS5222/course-notes/Chapter03.tex:15

删除没有增加协议机制的口语化反面说法。

原文：
```tex
；收到半段文件不能直接说“差不多齐了”。
```

改为：
```tex
。
```

## E092 · CS5222/course-notes/Chapter03.tex:63

标题定位实际端点标识。

原文：
```tex
2. Multiplexing and demultiplexing｜同一栋楼有许多门
```

改为：
```tex
2. Multiplexing and demultiplexing｜按地址与端口区分端点
```

## E093 · CS5222/course-notes/Chapter03.tex:100

标题对应服务与字段内容。

原文：
```tex
3. UDP｜少做承诺，也少保存状态
```

改为：
```tex
3. UDP｜数据报服务与首部
```

## E094 · CS5222/course-notes/Chapter03.tex:295

标题直接说明新增故障与机制。

原文：
```tex
6. rdt3.0｜坏消息会来，丢掉的消息可能一直不来
```

改为：
```tex
6. rdt3.0｜丢包后的超时与重传
```

## E095 · CS5222/course-notes/Chapter03.tex:388

中英完整说明原有计时条件与比较问题。

原文：
```tex
同样RTT与包长，R改为100Mbps，停等吞吐是否变为原来的十分之一？ / Recompute after reducing R to 100 Mbps.
```

改为：
```tex
包长8000 bit、RTT=30 ms，忽略ACK传输与处理，R从1 Gbps降到100 Mbps。停等吞吐是否降为原来的十分之一？ / For 8000-bit packets and RTT=30 ms, ignore ACK transmission and processing. Reduce R from 1 Gbps to 100 Mbps. Does stop-and-wait throughput fall to one tenth of its original value?
```

## E096 · CS5222/course-notes/Chapter03.tex:593

RTO变式写全平滑系数与新E约定，避免隐含依赖。

原文：
```tex
S改为80 ms，仍先更新E再更新D。求E、D、RTO。 / Restart from E=100 ms and D=10 ms, but use S=80 ms. Keep the same coefficients and update order. Find the new E, D and RTO.
```

改为：
```tex
S改为80 ms，alpha=0.125、beta=0.25，仍先更新E再更新D。求E、D、RTO。 / Restart from E=100 ms and D=10 ms, with S=80 ms, alpha=0.125 and beta=0.25. Update E first, then use the new E to update D. Find the new E, D and RTO.
```

## E097 · CS5222/course-notes/Chapter03.tex:613

保留原五问，逐题补中文题意与双语完整短答案，明确TCP四元组、重传身份、定时器条件和ACK单位。

原文：
```tex
英文自测：Why can different clients share server port 80? What ambiguity do sequence numbers solve? Why is a timer needed? Why can a delayed duplicate defeat alternating-bit assumptions? How do packet ACKs differ from TCP ACKs?


最低要点 / Key points：完整端点不同；分清新数据与重传；丢失时无反馈；旧编号可能被重用；TCP确认下一个字节。 / Different endpoint tuples; distinguish new data from retransmissions; loss may produce no feedback; old numbers can be reused; TCP acknowledges the next byte.
```

改为：
```tex
\textbf{Q1 / 题：} 不同客户端为什么可以共享服务器80端口？ / Why can different clients share server port 80?

\textbf{答 / Answer：} 已建立TCP连接按源IP、源端口、目的IP、目的端口四元组区分。服务器端口相同时，客户端地址或端口不同仍可区分连接。 / Established TCP connections use both address-port pairs. Different client addresses or ports distinguish connections that share server port 80.

\textbf{Q2 / 题：} 序号解决了什么歧义？ / What ambiguity do sequence numbers solve?

\textbf{答 / Answer：} 在本章rdt模型中，同一份数据重传时保留序号，新数据才换号，使接收方能辨认重复副本，避免再次交付。 / In the rdt models, retransmissions retain the data's sequence number, while new data use the next number. This lets the receiver recognize duplicates and avoid redelivery.

\textbf{Q3 / 题：} 为什么还需要定时器？ / Why is a timer needed?

\textbf{答 / Answer：} 数据或ACK丢失时可能没有任何反馈，定时器超时才能触发重传。超时也可能由延迟造成，本身不能证明包已丢失。 / Lost data or ACKs may produce no feedback, so timeout provides a retransmission trigger. A timeout can also result from delay and does not prove loss.

\textbf{Q4 / 题：} 长时间延迟的旧副本为什么可能破坏交替比特协议的可靠性？ / Why can a delayed duplicate defeat alternating-bit assumptions?

\textbf{答 / Answer：} 若旧0号包一直延迟到接收方又等待0号新数据时才到达，接收方可能把旧数据重新交付。因此可靠性需要限制旧副本的延迟或寿命，不能允许任意重排和长期滞留。 / An old packet 0 can arrive after the receiver again expects new data 0 and be delivered as new. Correctness therefore needs assumptions that prevent arbitrarily delayed duplicates from surviving until number reuse.

\textbf{Q5 / 题：} 本章的包ACK与TCP字节ACK有何区别？ / How do packet ACKs differ from TCP ACKs?

\textbf{答 / Answer：} GBN的ACK n累计确认截至n号包；SR的ACK n只确认n号包。TCP的ACK k表示下一个期待的字节，累计确认k之前连续收到的字节。 / GBN ACK n confirms all packets through n; SR ACK n confirms only packet n. TCP ACK k identifies the next expected byte and cumulatively acknowledges the contiguous bytes before k.
```

## E098 · CS5222/course-notes/Tutorial01.tex:36

表内已有逐题教师解答依据，删除同义尾注。

原文：
```tex
学习优先级依据当前原题与教师解答。


```

改为：
```tex

```

## E099 · CS5222/course-notes/Tutorial01.tex:89

独立题补包长、速率、转发与忽略项。

原文：
```tex
5个包、3条同速链路，同样忽略其他时延，多久？ / Five packets cross three equal-rate links under the same assumptions. Find completion time.
```

改为：
```tex
5个L-bit包连续经过3条R-bit/s链路，采用存储转发，忽略传播、排队和处理，全部到达要多久？ / Five L-bit packets are sent consecutively across three R-bit/s store-and-forward links. Ignore propagation, queueing and processing. Find the completion time.
```

## E100 · CS5222/course-notes/Tutorial01.tex:151

独立变式补拓扑与端点位置，原容量不变。

原文：
```tex
每边只有3条电路，全部A–C最多多少？ / With three circuits per link, what is the maximum for A–C connections only?
```

改为：
```tex
A、B、C、D顺时针构成四边环，每边3条电路，全部连接均为A到对角的C，最多多少条？ / A, B, C and D form a clockwise four-node ring with three circuits per link. What is the maximum number of simultaneous A-to-C connections?
```

## E101 · CS5222/course-notes/Tutorial01.tex:185

补齐原FDM分配和setup，不把待计算速率直接给成答案。

原文：
```tex
同电路发送320000bit、setup不变，总时间？ / Double the file size to 320000 bits without changing setup or circuit rate.
```

改为：
```tex
320000 bit文件使用12个等速FDM电路中的一个，总速率1.536 Mbps，建立需600 ms。只计建立和发送，总时间多少？ / Send 320000 bits using one of twelve equal-rate FDM circuits sharing 1.536 Mbps. Setup takes 600 ms. Counting only setup and transmission, find the total time.
```

## E102 · CS5222/course-notes/Tutorial02.tex:48

完整指定原同速播放模型及变更包长，不再只说其他不变。

原文：
```tex
包改128byte，其他条件不变，首位/同速播放时延？ / Double packet size to 128 bytes, keeping all rates and propagation unchanged.
```

改为：
```tex
语音以128 kbps生成，每128 byte成包，链路4 Mbps、传播8 ms；接收端收齐整包后以128 kbps顺序播放。各bit从生成到播放的时延是多少？ / Voice is generated at 128 kbps in 128-byte packets, sent over a 4-Mbps link with 8-ms propagation. After receiving each full packet, the receiver plays it sequentially at 128 kbps. Find generation-to-playout delay for each bit.
```

## E103 · CS5222/course-notes/Tutorial02.tex:131

把原答案才出现的忽略项前置到题干，中英对齐。

原文：
```tex
四条相同速率链路，每条传播2ms，源包发送3ms，即时转发和整包存储转发分别多久？ / Four equal-rate links each propagate for 2 ms; serialization takes 3 ms. Compare immediate bit forwarding with store-and-forward for one packet.
```

改为：
```tex
四条相同速率链路，每条传播2 ms，每包发送3 ms，忽略排队和处理。一个包采用即时逐位转发和整包存储转发，分别多久？ / Four equal-rate links each have 2-ms propagation and 3-ms serialization per packet. Ignore queueing and processing. Compare immediate bit forwarding with store-and-forward for one packet.
```

## E104 · CS5222/course-notes/Tutorial02.tex:168

独立题补原L/R/FIFO条件，仍只求等待。

原文：
```tex
同速同包长，当前包已发75\%，队列前面还有2包，新包排队多久？ / The current packet is 75\% transmitted and two packets are queued ahead. Find the new packet's queueing delay.
```

改为：
```tex
出口按FIFO服务，所有包均为1500 byte，R=2 Mbps。当前包已发75\%，另有2包在新包前等待，新包排队多久？ / A FIFO output transmits 1500-byte packets at 2 Mbps. The current packet is 75\% transmitted and two packets are queued ahead of the new packet. Find its queueing delay.
```

## E105 · CS5222/course-notes/Tutorial03.tex:22

标题改为具体阅读技能。

原文：
```tex
Problem 1. Read an HTTP request｜不知道的就明确说不知道
```

改为：
```tex
Problem 1. Read an HTTP request｜从请求字段确定信息
```

## E106 · CS5222/course-notes/Tutorial03.tex:118

HTML不是目录文件，标题改为准确任务对象。

原文：
```tex
Problem 3. A page with eight objects｜先取目录，再知道要取哪八件东西
```

改为：
```tex
Problem 3. A page with eight objects｜HTML与八个对象的请求顺序
```

## E107 · CS5222/course-notes/Tutorial03.tex:101

英文补数值与两种场景，中文补顺序及忽略项。

原文：
```tex
RTT\_L=4ms、RTT\_r=20ms，无缓存与local命中分别多久？ / Compute both cases for these RTTs.
```

改为：
```tex
client到local DNS的RTT\_L=4 ms，local到root/TLD/authoritative每次RTT\_r=20 ms，查询按顺序进行，忽略处理和传输大小。无缓存与local有效缓存命中分别多久？ / The client-local RTT is 4 ms and each local-to-root/TLD/authoritative RTT is 20 ms. Queries are sequential; ignore processing and message transmission time. Find the uncached and valid local-cache-hit times.
```

## E108 · CS5222/course-notes/Tutorial03.tex:150

变式补齐DNS、RTT、服务器与先HTML的原条件。

原文：
```tex
改为base HTML+6对象，非持久且最多4并行、其他条件不变，结果？ / Use six referenced objects and at most four parallel non-persistent connections.
```

改为：
```tex
先取base HTML，再请求同一服务器的6个小对象，采用非持久连接且最多4条并行。DNS耗时D，服务器往返为RTT\textsubscript{0}，忽略对象发送时间。总时间是多少？ / Fetch the base HTML first, then six small objects on the same server using at most four parallel non-persistent connections. DNS costs D and the server RTT is RTT\textsubscript{0}; ignore object transmission time. Find total time.
```

## E109 · CS5222/course-notes/Tutorial03.tex:137

长期正文不使用材料刚到的维护时间称谓。

原文：
```tex
新到Tutorial 3教师解答，第13张幻灯片明确
```

改为：
```tex
Tutorial 3教师解答，第13张幻灯片明确
```

## E110 · CS5222/course-notes/Tutorial04.tex:8

标题改为实际任务。

原文：
```tex
先找谁供不动，再算怎样分得完
```

改为：
```tex
上传能力与文件分发时间
```

## E111 · CS5222/course-notes/Tutorial04.tex:44

表格已列逐题来源，变式已有具名标签。

原文：
```tex
优先级依据当前原题；额外练习标为变式。


```

改为：
```tex

```

## E112 · CS5222/course-notes/Tutorial04.tex:72

中文所求与英文allocation/completion对齐。

原文：
```tex
F=100Mbit、N=4、\(u_s\)=20Mbps、每人下载8Mbps，多久？
```

改为：
```tex
F=100Mbit、N=4、\(u_s\)=20Mbps、每人下载8Mbps，按本节流体模型给出可行分配与完成时间。
```

## E113 · CS5222/course-notes/Tutorial04.tex:115

独立变式补齐原值及比较目标。

原文：
```tex
N改为10，其他条件不变，P2P会比client-server快吗？ / Recompute both bounds for ten clients.
```

改为：
```tex
F=15 Gbit、N=10、服务器上传30 Mbps、每人下载2 Mbps且上传0.7 Mbps。按本节理想模型，P2P会比client-server快吗？ / For F=15 Gbit and ten clients, use server upload 30 Mbps, each client download 2 Mbps and upload 0.7 Mbps. In the ideal model, compare P2P and client-server completion-time bounds.
```

## E114 · CS5222/course-notes/Tutorial04.tex:180

英文明确所求文件数，不只给关键词。

原文：
```tex
Four video versions and two audio versions: all pairs versus separate tracks.
```

改为：
```tex
With four video versions and two audio versions, how many files are needed when every pair is precombined, and when tracks are stored separately?
```

## E115 · CS5222/course-notes/Tutorial05.tex:58

英文补齐中文题干端点和所求字段。

原文：
```tex
Read all three return paths from the server to the client processes.
```

改为：
```tex
Server B uses port 80. Client C connects from ports 7532 and 26145; client A connects from port 26145. Give the source and destination ports, and the enclosing IP source and destination, for each server reply.
```

## E116 · CS5222/course-notes/Tutorial05.tex:88

英文独立题给端点与明确问题。

原文：
```tex
服务器改为8443，客户端C的7532仍不变，回程端口怎样写？ / Change only the server port to 8443.
```

改为：
```tex
服务器B改用8443端口，客户端C用7532端口，回程端口怎样写？ / Server B uses port 8443 and client C uses port 7532. Give the source and destination ports of the reply.
```

## E117 · CS5222/course-notes/Tutorial05.tex:156

原英文任务补齐中文协议范围、判定和画图要求。

原文：
```tex
Give a reordering counterexample with explicit packet and ACK numbers.
```

改为：
```tex
Does rdt3.0 with alternating 0/1 sequence numbers remain correct under message reordering? If not, draw a counterexample with the sender on the left, receiver on the right and time downward, labeling data packets and ACKs.
```

## E118 · CS5222/course-notes/Tutorial05.tex:185

中英文同样指定2到4的变更。

原文：
```tex
Does a larger finite sequence space eliminate arbitrarily delayed old duplicates?
```

改为：
```tex
Does increasing the sequence space from two values to four eliminate arbitrarily delayed old duplicates?
```

## E119 · CS5222/course-notes/Assignment01.tex:85

直接说本题的实际机制。

原文：
```tex
P31. Message segmentation｜像流水线一样，让不同链路同时工作
```

改为：
```tex
P31. Message segmentation｜消息分段与链路流水线
```

## E120 · CS5222/course-notes/Assignment01.tex:135

标题定位三种事务问题。

原文：
```tex
P17. POP3｜完成整次事务，不只补两行
```

改为：
```tex
P17. POP3｜下载、删除与会话状态
```

## E121 · CS5222/course-notes/Assignment01.tex:68

独立题补原速率/传播速度，保留两时延相等的目标。

原文：
```tex
L=240bit、R不变，要保持两时延相等，m如何变化？ / Double packet length while keeping R and s fixed; how must m change?
```

改为：
```tex
包长由120 bit改为240 bit，R=56 kbps、s=2.5\ensuremath{\times}10\textsuperscript{8} m/s不变。要保持发送与传播时延相等，距离m如何变化？ / Increase packet length from 120 to 240 bits, keeping R=56 kbps and s=2.5\ensuremath{\times}10\textsuperscript{8} m/s. How must distance m change to keep transmission and propagation delays equal?
```

## E122 · CS5222/course-notes/Assignment01.tex:118

变式写全原模型条件与英文所求量。

原文：
```tex
同消息改成400包，每包20000bit，其他不变，总多久？ / Use 400 packets of 20000 bits with the same path.
```

改为：
```tex
消息分成400包，每包20000 bit，连续经过3条2 Mbps存储转发链路，忽略传播、排队、处理和包头开销。全部到达要多久？ / Send 400 packets of 20000 bits across three 2-Mbps store-and-forward links. Ignore propagation, queueing, processing and header overhead. Find total completion time.
```

## E123 · CS5222/course-notes/Assignment01.tex:140

英文补中文已有初始事务状态、编号和已执行RETR1，不改变协议对话。

原文：
```tex
Two messages of 498 and 912 octets are present. Finish the full download-and-delete and download-and-keep transactions, then show a second keep-mode session five minutes later with no new mail.
```

改为：
```tex
Authentication is complete and the session is in the transaction state. LIST shows messages 1 and 2 of 498 and 912 octets; the supplied exchange has already retrieved message 1. Finish the download-and-delete and download-and-keep transactions, then show a second keep-mode session five minutes later with no new mail.
```

## E124 · CS5222/course-notes/Assignment01.tex:249

独立题补邮件大小与删除对象。

原文：
```tex
b中仅DELE1并成功QUIT，之后无新邮件，剩多少总字节？ / Delete only message1 in part b and successfully quit. How many message octets remain?
```

改为：
```tex
邮箱有两封邮件，分别为498和912 byte。仅对第一封执行DELE并成功QUIT，之后无新邮件，剩多少邮件字节？ / A mailbox contains messages of 498 and 912 octets. Mark only the first for deletion and successfully quit, with no new mail afterward. How many message octets remain?
```

## E125 · CS5222/course-notes/ResearchReportGuide.tex:36

标题直接说明选题动作。

原文：
```tex
1. 选题从一件事开始，不从一串热门缩写开始
```

改为：
```tex
1. 从实际问题确定研究范围
```

## E126 · CS5222/course-notes/ResearchReportGuide.tex:115

标题列明图的三种具体用途。

原文：
```tex
4. 图要解释困难，不是给文字化妆
```

改为：
```tex
4. 用图说明交互、结构或权衡
```

## E127 · CS5222/course-notes/ResearchReportGuide.tex:168

保留真实反思要求，标题不再反复强调真实性。

原文：
```tex
6. Reflection log｜写你真的经历过的理解变化
```

改为：
```tex
6. Reflection log｜记录理解怎样改变
```

## E128 · CS5222/course-notes/ResearchReportGuide.tex:61

英文明确中文模型条件；补整块到齐约定使下一变式的停顿计算明确。

原文：
```tex
在缓冲足够、同时播放、忽略请求与解码开销时，缓冲净增加4\ensuremath{-}2=2秒。 / A four-second segment encoded at 2 Mbps contains 8 Mbit. At 4 Mbps throughput it downloads in two seconds, increasing the playable buffer by two seconds under the stated assumptions.
```

改为：
```tex
在初始缓冲足够、下载中同时播放、整块到齐后加入缓冲且忽略请求与解码开销时，缓冲净增加4\ensuremath{-}2=2秒。 / A four-second segment encoded at 2 Mbps contains 8 Mbit. At a constant 4-Mbps download rate it arrives in two seconds. With sufficient initial buffer, playback continuing during download, whole-chunk availability on arrival and no request or decoding overhead, playable buffer grows by two seconds.
```

## E129 · CS5222/course-notes/ResearchReportGuide.tex:65

独立变式完整说明数据与整块可用模型，保留原8秒/5秒结果。

原文：
```tex
网络降至1Mbps，同一块需几秒？若开始时只缓冲3秒会发生什么？ / At 1 Mbps, how long does the same chunk take, and what if only three seconds are buffered initially?
```

改为：
```tex
一个4秒视频块按2 Mbps编码，下载吞吐稳定为1 Mbps，开始时有3秒可播放缓冲。下载中继续播放，整块到齐才可播放，忽略其他开销。下载需要多久，会停顿多久？ / A four-second chunk encoded at 2 Mbps downloads at a constant 1 Mbps, starting with three seconds of playable buffer. Playback continues during download; the chunk becomes playable only when fully received. Ignore other overhead. Find download and stall times.
```

## E130 · CS5222/course-notes/ResearchReportGuide.tex:72

后段统一解释理想模型与实际条件，不在答案后再重复限制。

原文：
```tex
 缓冲余量和吞吐估计误差都会影响是否停顿。
```

改为：
```tex

```

## E131 · CS5222/course-notes/ResearchReportGuide.tex:78

算例身份已在开头注明，保留有用的实际条件。

原文：
```tex
上面是理想模型的教学算例；实际停顿还取决于播放器策略和网络变化。
```

改为：
```tex
播放器策略和实际吞吐变化会改变停顿时间。
```

## E132 · CS5222/course-notes/ResearchReportGuide.tex:161

直接说明写作要求，去掉刻意反面例子。

原文：
```tex
不要把“可能”藏起来，也不用给每句话堆三个形容词。
```

改为：
```tex
保留影响结论的条件和不确定性。
```

## E133 · CS5222/course-notes/ResearchReportGuide.tex:226

正文已分别完整说明选题、来源和图，不再附泛泛收尾。

原文：
```tex
确定主题后，再围绕核心问题补充必要基础、原始来源和图示。

```

改为：
```tex

```

## E134 · learning/foundation-notes/MathForML.tex:7

基础知识页不把旧编辑日期当学习信息；版本在审阅记录。

原文：
```tex
 · 扩展于2026-09-23
```

改为：
```tex

```

## E135 · learning/foundation-notes/MathForML.tex:13

直接说明补课内容和用途，删除对读者困难的猜测和重复台阶包装。

原文：
```tex
看到一长串公式时，困难有时并不是“机器学习太难”，而是同时遇到了五个不认识的符号。这份补课把这些台阶拆开：先知道符号在说什么，再用小数字算一次，最后回到老师的公式。
```

改为：
```tex
本篇按符号、概率、对数、求导和矩阵等常见卡点补充先修。各专题用小数字解释计算，再连接课程中的公式。
```

## E136 · learning/foundation-notes/MathForML.tex:16

删除制作方式自述，让实际题答体现对应关系。

原文：
```tex
正文中的英文术语帮助对照课堂，English takeaway 是整理后的表达，练习题答中英对齐。
```

改为：
```tex
英文术语用于对照课堂。
```

## E137 · learning/foundation-notes/MathForML.tex:19

前段已说明按需选择和节末返回，不再重复。

原文：
```tex
各专题可以单独阅读；学会当前需要的工具后，通过节末链接回到课程。


```

改为：
```tex

```

## E138 · learning/foundation-notes/MathForML.tex:21

标题直接定位概念和例子，旧锚点保持。

原文：
```tex
先找到自己缺的那一级台阶
```

改为：
```tex
按学习卡点选择专题
```

## E139 · learning/foundation-notes/MathForML.tex:157

标题直接定位概念和例子，旧锚点保持。

原文：
```tex
1. Symbols, functions and graphs｜先让公式开口说人话
```

改为：
```tex
1. Symbols, functions and graphs｜变量、函数与坐标
```

## E140 · learning/foundation-notes/MathForML.tex:163

标题直接定位概念和例子，旧锚点保持。

原文：
```tex
1.1 水箱的账本：谁变了，谁跟着变？
```

改为：
```tex
1.1 用水量变化表示函数
```

## E141 · learning/foundation-notes/MathForML.tex:206

标题直接定位概念和例子，旧锚点保持。

原文：
```tex
1.2 图像就是把账本放到坐标上
```

改为：
```tex
1.2 把时间与水量画在坐标上
```

## E142 · learning/foundation-notes/MathForML.tex:792

标题直接定位概念和例子，旧锚点保持。

原文：
```tex
4.4 偏导：这次只动一个旋钮
```

改为：
```tex
4.4 偏导：固定其他变量
```

## E143 · learning/foundation-notes/MathForML.tex:817

标题直接定位概念和例子，旧锚点保持。

原文：
```tex
4.5 找山顶：导数为零只是候选条件
```

改为：
```tex
4.5 导数为零只是候选条件
```

## E144 · learning/foundation-notes/MathForML.tex:76

中文明确与英文uniformly一致的抽样条件。

原文：
```tex
已知随机选中的邮件带附件，
```

改为：
```tex
已知等可能随机选中的邮件带附件，
```

## E145 · learning/foundation-notes/MathForML.tex:232

完整示范补前页水箱数据，纸上可独立使用。

原文：
```tex
中文题：保持水箱条件，求2.5分钟后的水量；如果想达到8 L，需要多久？
```

改为：
```tex
中文题：水箱初始1 L，以2 L/min匀速注水，不漏、不溢出。求2.5分钟后的水量；达到8 L需要多久？
```

## E146 · learning/foundation-notes/MathForML.tex:234

英文对应完整水箱条件。

原文：
```tex
English question: Under the same tank assumptions, find the volume after 2.5 minutes and the time needed to reach 8 L.
```

改为：
```tex
English question: A tank starts with 1 L and receives 2 L/min, without leakage or overflow. Find the volume after 2.5 minutes and the time needed to reach 8 L.
```

## E147 · learning/foundation-notes/MathForML.tex:387

同一邮件表已解释条件反转，删除突然引入的第二套比喻。

原文：
```tex
；“已知是猫，有胡子的比例”和“已知有胡子，是猫的比例”也有这个区别。
```

改为：
```tex
。
```

## E148 · learning/foundation-notes/MathForML.tex:401

修正邮件例中误用人的对象指代。

原文：
```tex
30/100的人被留下，在留下的人中取18/30
```

改为：
```tex
30/100的邮件被留下，再从中取18/30
```

## E149 · learning/foundation-notes/MathForML.tex:459

中文与英文已有区间条件对齐。

原文：
```tex
中文题：在上述均匀等待模型中，求0.1到0.3分钟之间的概率。
```

改为：
```tex
中文题：等待时间在0至0.5分钟之间均匀分布，求0.1到0.3分钟之间的概率。
```

## E150 · learning/foundation-notes/MathForML.tex:481

为较远的表格给纸面页码。

原文：
```tex
中文题：用上面的100封邮件表，
```

改为：
```tex
中文题：用\StudyRef{Foundations-MathForML}{conditional-probability}{100封邮件计数表}，
```

## E151 · learning/foundation-notes/MathForML.tex:481

变式补齐连续分布区间。

原文：
```tex
另用同一个均匀等待模型，
```

改为：
```tex
另设等待时间在0至0.5分钟间均匀分布，
```

## E152 · learning/foundation-notes/MathForML.tex:483

英文同样有数据页码及等待分布条件。

原文：
```tex
English question: Using the 100-message table, find P(spam | no free). In the same uniform waiting-time model,
```

改为：
```tex
English question: Using the \StudyRef{Foundations-MathForML}{conditional-probability}{100-message table}, find P(spam | no free). For a waiting time uniform on [0,0.5] minutes,
```

## E153 · learning/foundation-notes/MathForML.tex:942

前式是uᵀv，并非只交换了相同两个因子的顺序。

原文：
```tex
反过来u u\textsuperscript{T}是
```

改为：
```tex
用u与它自己的转置相乘，u u\textsuperscript{T}是
```

## E154 · learning/foundation-notes/MathForML.tex:950

解释两种运算作用，消除更换向量却声称只换顺序的误导。

原文：
```tex
交换乘法顺序，结果从一个数变成了一个矩阵。
```

改为：
```tex
内积把对应分量的乘积相加，得到一个数；外积保留各分量配对的乘积，得到一个矩阵。
```

## E155 · learning/foundation-notes/MathForML.tex:1086

图注保留来源与模型，不描述维护过程。

原文：
```tex
复用已核查的Lecture2b，第36个单元的矩阵图：
```

改为：
```tex
Lecture2b，第36个单元的协方差模型：
```

## E156 · learning/foundation-notes/MathForML.tex:1281

本文没有使用手电筒类比，删除无缘由的限制提醒；垂直条件已由向量解释。

原文：
```tex
类比手电筒投影时要注意：这里是垂直投影，不是任意灯光角度的影子。
```

改为：
```tex

```

## E157 · learning/foundation-notes/MathForML.tex:1350

明确A⁺是矩阵而非解向量，同时删去虚设的反面说法。

原文：
```tex
伪逆不是“给不存在的普通逆编一个值”，而是约定一个满足最小二乘/最小范数条件的解，记为 \(A^+\)。
```

改为：
```tex
伪逆矩阵记为 \(A^+\)；将它乘以目标向量，就得到最小范数的最小二乘解。
```

## E158 · learning/foundation-notes/MathForML.tex:1366

独立变式补矩阵列数据。

原文：
```tex
同一个A，y=(4,8)。最小范数解、预测和残差？ / For the same A and y=(4,8), find the minimum-norm solution, prediction and residual.
```

改为：
```tex
A的两列均为(1,2)，y=(4,8)。最小范数解、预测和残差分别是什么？ / Both columns of A are (1,2), and y=(4,8). Find the minimum-norm solution, prediction and residual.
```

## E159 · learning/foundation-notes/MathForML.tex:1467

共享参数和两项贡献相加已说明，删除重复修辞。

原文：
```tex
；不能只留一天，也不能给每一天偷偷创建一个新的b。
```

改为：
```tex
。
```

## E160 · learning/foundation-notes/MathForML.tex:1592

补齐已有第10专题在来源覆盖表中的遗漏，不增加教学内容。

原文：
```tex
梯度与约束 & Lecture3a，第52个单元；Lecture3b，第37–44个单元；SVM.pdf第2–4页 & 展开原课求导与KKT前提，不代替SVM推导 \\
```

改为：
```tex
梯度与约束 & Lecture3a，第52个单元；Lecture3b，第37–44个单元；SVM.pdf第2–4页 & 展开原课求导与KKT前提，不代替SVM推导 \\
批量梯度 & Lecture5b，第15–21个单元；Assignment2，第4、7个单元 & 行样本、共享参数与平均因子的补充推导 \\
```

## E161 · learning/foundation-notes/NetworkBasics.tex:13

直接交代先修范围，避免用并非复杂而是台阶解释读者困难。

原文：
```tex
网络计算最常见的绊脚石，不是公式复杂，而是把字节当比特、把距离当速率、把“第一个到”当“整个都到了”。这份补课只拆这些台阶，协议机制仍在 Chapter 正文讲。小算例均为教学补充。
```

改为：
```tex
本篇补充网络计算中的单位、报文字节和时间轴：区分bit与byte、数据量与速率，以及首位和整包到达。协议机制见Chapter正文，小算例均为教学补充。
```

## E162 · learning/foundation-notes/NetworkBasics.tex:38

标题直接写三个量，不另引仓库类比。

原文：
```tex
1. Bit, byte and rate｜仓库有多少货，和每秒搬多少货，是两件事
```

改为：
```tex
1. Bit, byte and rate｜数据量、发送速率与传播速度
```

## E163 · learning/foundation-notes/NetworkBasics.tex:53

单位检验直接说明作用，删除报警器比喻。

原文：
```tex
单位“bit\ensuremath{\div}bit/s”最后剩s，是一个自带报警器：如果还剩米或字节，通常哪里没对齐。
```

改为：
```tex
用单位检验结果：“bit\ensuremath{\div}bit/s”得到s，表示所求的是时间。
```

## E164 · learning/foundation-notes/NetworkBasics.tex:61

图注只定位坐标与两条柱，不重复前面的除法解释。

原文：
```tex
发送与传播使用不同的“数量除以速率”：上条处理比特，下条处理距离。
```

改为：
```tex
横轴是时间（ms）；上条为发送时延，下条为传播时延。
```

## E165 · learning/foundation-notes/NetworkBasics.tex:64

删除与前文及图注重复的两条柱说明，保留带宽单位区别。

原文：
```tex
上条是“把多少bit送上路”，下条是“已经上路的bit走多远”。两个除法输出同为秒，但分子和分母的含义不同。带宽还可能在物理通信里指Hz频宽；本章说link bandwidth时通常指bit/s容量，要看上下文。
```

改为：
```tex
本章的link bandwidth通常指bit/s容量；物理通信中的带宽也可能指Hz频宽，需要结合单位区分。
```

## E166 · learning/foundation-notes/NetworkBasics.tex:122

英文补中文已有两组二进制数字。

原文：
```tex
Convert these two binary octets to decimal.
```

改为：
```tex
Convert binary octets 00001010 and 11000000 to decimal.
```

## E167 · learning/foundation-notes/NetworkBasics.tex:145

标题直接说明报文读取对象。

原文：
```tex
3. Messages and bytes｜一段报文不是一整块没有边界的文字
```

改为：
```tex
3. Messages and bytes｜字段、分隔符与消息边界
```

## E168 · learning/foundation-notes/NetworkBasics.tex:232

题干明确存储转发与连续发送等原条件。

原文：
```tex
同样条件，4个包、3条链路，每包发送2ms，总多久？ / Four packets cross three equal-rate links, with 2 ms transmission per packet and no other delays. Find the completion time.
```

改为：
```tex
4个等长包连续经过3条等速存储转发链路，每包发送2 ms，忽略传播、排队和处理，总多久？ / Four equal packets are sent consecutively across three equal-rate store-and-forward links, with 2-ms transmission per packet. Ignore propagation, queueing and processing. Find the completion time.
```

## E169 · learning/foundation-notes/SourceEvidence.tex:23

用可查入口代替编辑批次和哈希盘点；历史记录保留于基线与来源清单。

原文：
```tex
9月23日核对的34份Notebook/PDF/PPT文件已登记路径、SHA-256和单元/页数于历史来源清单。
```

改为：
```tex
Notebook/PDF/PPT的文件版本与单元或页数见\StudyRepoRef{docs/source-materials.json}{}{来源清单}。
```

## E170 · learning/foundation-notes/SourceEvidence.tex:45

保留年份与证据边界，去掉上轮复用的制作叙述。

原文：
```tex
上轮Lecture2已核对2024日期及Ex2分布/MLE迁移，教师/校区只由仓库上下文推测；复用旧核查记录
```

改为：
```tex
文件日期为2024年，Ex2用于练习更换分布后的MLE推导；教师/校区未由文件内信息确认
```

## E171 · learning/foundation-notes/SourceEvidence.tex:85

消除依赖当前维护轮次的时间称谓。

原文：
```tex
CS5222本轮依据当前Chapter、Q\&A、Tutorial与Assignment判断学习优先级，
```

改为：
```tex
CS5222依据已下载的Chapter、Q\&A、Tutorial与Assignment判断学习优先级，
```

## E172 · CS5489/course-notes/Lecture05.tex:117

二读将吸收偏置的说法落实为具体表示方法。

原文：
```tex
省略的偏置仍可吸收入向量。
```

改为：
```tex
给输入增加常数1后，偏置也可写进权重矩阵。
```

## E173 · CS5489/course-notes/Lecture05.tex:650

英文采用直接表达，减少不必要的引号宏。

原文：
```tex
Use this section\textquotesingle{}s momentum convention,
```

改为：
```tex
Use the momentum convention in this section,
```

## E174 · learning/foundation-notes/NetworkBasics.tex:53

单位除法把整个速率作为分母，避免运算顺序歧义。

原文：
```tex
“bit\ensuremath{\div}bit/s”得到s
```

改为：
```tex
“bit\ensuremath{\div}(bit/s)”得到s
```

## E175 · CS5489/course-notes/Tutorial04.tex:326

负数使用统一数学负号。

原文：
```tex
a mean truth-minus-prediction residual of -1362.37.
```

改为：
```tex
a mean truth-minus-prediction residual of \ensuremath{-}1362.37.
```

## E176 · scripts/build_exam_annotations.py:91

二读合并L1诊断考点的近义来源限制，保留优化/早停、CNN范围、年份和卷次全部条件。

原文：
```tex
                if notes:topic_parts+=[r'\textbf{题源条件：}'+escape('；'.join(notes)+'。')]
```

改为：
```tex
                if n==1 and t['id']=='diagnosis':
                    notes=['完整处理还需Lecture5的优化与早停',
                        '当前只映射通用训练/验证诊断，CNN结构设计属于后续内容',
                        'QE题段缺年份与独立原卷身份，不按片段数计卷数']
                if notes:topic_parts+=[r'\textbf{题源条件：}'+escape('；'.join(notes)+'。')]
```

## E177 · CS5489/course-notes/Lecture03.tex:148

标题与考点标签独占页底，正文落到下一页；为标题与首个公式预留空间

原文：
```tex
\StudyHeading{1}{3. Logistic regression｜把分数翻译成概率}
```

改为：
```tex
\Needspace{12\baselineskip}
\StudyHeading{1}{3. Logistic regression｜把分数翻译成概率}
```

## E178 · CS5489/course-notes/Tutorial02.tex:612

短迁移题的答案全部落到下一页；将题答一起起排

原文：
```tex
独立迁移题：某人在所有3000条新闻上先建词表
```

改为：
```tex
\Needspace{13\baselineskip}
独立迁移题：某人在所有3000条新闻上先建词表
```

## E179 · CS5489/course-notes/Assignment01.tex:517

英文答案单独落到下一页；保留整题的双语对应

原文：
```tex
\textbf{Q3 中文：} CSV中Id完整且预测都合法
```

改为：
```tex
\Needspace{13\baselineskip}
\textbf{Q3 中文：} CSV中Id完整且预测都合法
```

## E180 · CS5489/course-notes/Assignment02.tex:344

短题干留在页底，答案从下一页开始；局部预留题答空间

原文：
```tex
\textbf{Q3 / 题：} 怎样避免缩放时使用测试信息
```

改为：
```tex
\Needspace{8\baselineskip}
\textbf{Q3 / 题：} 怎样避免缩放时使用测试信息
```

## E181 · CS5222/course-notes/Chapter03.tex:617

短题干留在页底，答案从下一页开始；局部预留题答空间

原文：
```tex
\textbf{Q2 / 题：} 序号解决了什么歧义
```

改为：
```tex
\Needspace{7\baselineskip}
\textbf{Q2 / 题：} 序号解决了什么歧义
```

## E182 · learning/foundation-notes/MathForML.tex:458

密度短题的中英答案全部落到下一页；为完整示范预留空间

原文：
```tex
\begin{StudyBlock}{完整示范 / Worked example}{用面积计算等待概率}
```

改为：
```tex
\Needspace{17\baselineskip}
\begin{StudyBlock}{完整示范 / Worked example}{用面积计算等待概率}
```

## E183 · CS5489/course-notes/Tutorial02.tex:631

视觉二读发现三问及三答在PDF各挤为一段；逐题配对，保持原有条件与解释

原文：
```tex
用英文解释三个问题，再去Markji按卡号巩固：
- Why must the vocabulary and IDF be fitted on training data?
- Why do Bernoulli, multinomial and Poisson smoothing have different denominators?
- Why is the highest score in these test-set sweeps not an unbiased final result?


对应中文：为何词表/IDF只从训练数据拟合？三个模型的平滑分母为何不同？为何这次扫test得到的最高分不是独立最终成绩？


参考要点 / Key points：
1. 中文：词表和IDF会学习输入分布，因此也必须留在训练部分。English: Vocabulary and IDF learn from input data and must be fitted within the training split.
2. 中文：Bernoulli对每词的两种结果平滑；Multinomial对词表中的V种结果平滑；这里Poisson的额外约定向总词次数和文档数分别加alpha。English: Bernoulli smooths two feature outcomes; multinomial smooths V token outcomes; the stated Poisson convention adds alpha to the total word count and document count.
3. 中文：test表现参与了模型和参数选择，已提供开发反馈。English: The test scores influenced model and parameter selection, so they are development feedback rather than an untouched final evaluation.



```

改为：
```tex
\textbf{Q1 / 题：} 为何词表和IDF只能从训练数据拟合？ / Why must the vocabulary and IDF be fitted on training data?

\textbf{答 / Answer：} 词表和IDF会学习输入分布，因此也必须留在训练部分。 / Vocabulary and IDF learn from input data and must be fitted within the training split.

\textbf{Q2 / 题：} Bernoulli、Multinomial和Poisson的平滑分母为何不同？ / Why do Bernoulli, multinomial and Poisson smoothing have different denominators?

\textbf{答 / Answer：} Bernoulli对每词的两种结果平滑；Multinomial对词表中的V种结果平滑；这里Poisson的额外约定向总词次数和文档数分别加alpha。 / Bernoulli smooths two feature outcomes; multinomial smooths V token outcomes; the stated Poisson convention adds alpha to the total word count and document count.

\textbf{Q3 / 题：} 为何这次扫test得到的最高分不是独立的最终成绩？ / Why is the highest score in these test-set sweeps not an unbiased final result?

\textbf{答 / Answer：} test表现参与了模型和参数选择，已提供开发反馈。 / The test scores influenced model and parameter selection, so they are development feedback rather than an untouched final evaluation.



```

## E184 · scripts/build_exam_annotations.py:35

审阅过的语义合并只作用于已知子句，保留台账以后新增或更改的条件

原文：
```tex


def build():
```

改为：
```tex


def compact_review_notes(notes, known, replacement):
    """Condense reviewed clauses while retaining any later ledger additions."""
    if not known <= set(notes):
        return notes
    return replacement + [note for note in notes if note not in known]


def build():
```

## E185 · scripts/build_exam_annotations.py:99

避免讲末摘要覆盖未来新增题源条件；当前生成文字保持

原文：
```tex
                    notes=['完整处理还需Lecture5的优化与早停',
                        '当前只映射通用训练/验证诊断，CNN结构设计属于后续内容',
                        'QE题段缺年份与独立原卷身份，不按片段数计卷数']
```

改为：
```tex
                    notes=compact_review_notes(notes, {
                        '完整处理还需Lecture5的优化与早停', 'CNN结构不在当前Lecture1–5范围',
                        '缺年份与独立原卷身份', 'CNN设计另需后续课', '缺年份',
                        '不把片段数量计为卷数', '只映射一般诊断能力'}, [
                        '完整处理还需Lecture5的优化与早停',
                        '当前只映射通用训练/验证诊断，CNN结构设计属于后续内容',
                        'QE题段缺年份与独立原卷身份，不按片段数计卷数'])
```

## E186 · scripts/build_exam_annotations.py:148

避免试卷摘要覆盖未来新增题源条件；当前生成文字保持

原文：
```tex
            notes=['部分图与问题跨两个原页，须一起读取；手写解答不作为标准答案']
```

改为：
```tex
            notes=compact_review_notes(notes, {
                '缺年份与独立原卷身份', 'CNN设计另需后续课', '缺年份',
                '不把片段数量计为卷数', '只映射一般诊断能力', 'CNN架构未在当前讲义覆盖',
                '题段年份与卷次待定', '仅映射通用训练诊断', '图与问题跨两个原页',
                '不使用扫描手写解答', '缺年份和独立原卷身份'}, [
                '部分图与问题跨两个原页，须一起读取；手写解答不作为标准答案'])
```

## E187 · CS5489/course-notes/Assignment01.tex:499

移除自测段落末多余的强制换行，保留常规段距并按题预留空间；避免来源表单行溢到空页

原文：
```tex
\textbf{Q1 中文：} 为什么普通accuracy更高的模型，可能不符合这份作业的选择目标？\\

\textbf{Q1 English:} Why might a model with higher ordinary accuracy be less suitable under the assignment metric?\\

\textbf{答：} 多数类主导整体比例；balanced accuracy看三类recall的均值，因此要比较指定指标与每类表现。\\

\textbf{Answer:} Majority-class performance can dominate ordinary accuracy. The assigned metric averages class recalls, so compare balanced accuracy and per-class results.


\textbf{Q2 中文：} 没用test标签，但把test文本放进词表拟合，是否仍影响独立评价？\\

\textbf{Q2 English:} Does including test text in vocabulary fitting affect independent evaluation even without using its labels?\\

\textbf{答：} 会，表示已经利用test信息；预处理也是拟合的一部分。\\

\textbf{Answer:} Yes. Representation learning used test information; preprocessing is part of fitting.


\Needspace{13\baselineskip}
\textbf{Q3 中文：} CSV中Id完整且预测都合法，能否证明文件正确？\\

\textbf{Q3 English:} Do complete IDs and valid class values prove that a prediction file is correct?\\

\textbf{答：} 不能，还要验证每个预测是否对应同Id的原短信，以及流程是否按允许的数据训练。\\

\textbf{Answer:} No. Verify that each prediction matches the text with that ID and that the procedure used only permitted training data.


\textbf{Q4 中文：} 本文件的51.67\%能否写进自己的作业实验结果？\\

\textbf{Q4 English:} Can the 51.67\% in this guide be reported as your assignment result?\\

\textbf{答：} 不能，它是人为混淆矩阵的教学计算，没有训练短信分类器。\\

\textbf{Answer:} No. It is a calculation from an artificial teaching matrix, not a trained SMS classifier's measured result.



```

改为：
```tex
\Needspace{11\baselineskip}
\textbf{Q1 中文：} 为什么普通accuracy更高的模型，可能不符合这份作业的选择目标？

\textbf{Q1 English:} Why might a model with higher ordinary accuracy be less suitable under the assignment metric?

\textbf{答：} 多数类主导整体比例；balanced accuracy看三类recall的均值，因此要比较指定指标与每类表现。

\textbf{Answer:} Majority-class performance can dominate ordinary accuracy. The assigned metric averages class recalls, so compare balanced accuracy and per-class results.


\Needspace{9\baselineskip}
\textbf{Q2 中文：} 没用test标签，但把test文本放进词表拟合，是否仍影响独立评价？

\textbf{Q2 English:} Does including test text in vocabulary fitting affect independent evaluation even without using its labels?

\textbf{答：} 会，表示已经利用test信息；预处理也是拟合的一部分。

\textbf{Answer:} Yes. Representation learning used test information; preprocessing is part of fitting.


\Needspace{9\baselineskip}
\textbf{Q3 中文：} CSV中Id完整且预测都合法，能否证明文件正确？

\textbf{Q3 English:} Do complete IDs and valid class values prove that a prediction file is correct?

\textbf{答：} 不能，还要验证每个预测是否对应同Id的原短信，以及流程是否按允许的数据训练。

\textbf{Answer:} No. Verify that each prediction matches the text with that ID and that the procedure used only permitted training data.


\Needspace{9\baselineskip}
\textbf{Q4 中文：} 本文件的51.67\%能否写进自己的作业实验结果？

\textbf{Q4 English:} Can the 51.67\% in this guide be reported as your assignment result?

\textbf{答：} 不能，它是人为混淆矩阵的教学计算，没有训练短信分类器。

\textbf{Answer:} No. It is a calculation from an artificial teaching matrix, not a trained SMS classifier's measured result.



```

## E188 · CS5489/course-notes/Lecture01.tex:227

让行内代码与句末标点保持相连，避免英文句号单独落到下一行

原文：
```tex
\StudyInline{x*=2}. What is the result?
```

改为：
```tex
\StudyInline{x*=2}\nobreak. What is the result?
```

## E189 · CS5489/course-notes/Lecture02.tex:1638

英文题干直接给出原协方差条件，不依赖只出现在中文题干的矩阵

原文：
```tex
zero means, the above covariances and A/B priors 0.8/0.2
```

改为：
```tex
zero means, identity covariance for A, unit variances and covariance 0.5 for B, and A/B priors 0.8/0.2
```

## E190 · CS5489/course-notes/Tutorial02.tex:338

三个错分样本仍保留旧Markdown的行首短横，PDF挤成一段；改成原生列表，样本、标签和解释不变

原文：
```tex
- Index 1描述飓风造成的保险损失，原标签Business、预测World，仅保留4个词。灾害事件与经济损失共用同一短文，可以提出“主题边界与词表截断影响判断”的假设；尚未用受控实验验证。
- Index 3讨论消费者信心和就业，原标签World、预测Business。经济主题词使这个预测值得理解，但不能只凭主题印象把原标签改掉。
- Index 14讨论太阳帆航天器及项目资助，原标签Sci/Tech、预测Business；两个模型后验接近。查看保留词可以帮助区分表示损失、主题重叠和模型限制这几种解释。
```

改为：
```tex
\begin{itemize}
\item Index 1描述飓风造成的保险损失，原标签Business、预测World，仅保留4个词。灾害事件与经济损失共用同一短文，可以提出“主题边界与词表截断影响判断”的假设；尚未用受控实验验证。
\item Index 3讨论消费者信心和就业，原标签World、预测Business。经济主题词使这个预测值得理解，但不能只凭主题印象把原标签改掉。
\item Index 14讨论太阳帆航天器及项目资助，原标签Sci/Tech、预测Business；两个模型后验接近。查看保留词可以帮助区分表示损失、主题重叠和模型限制这几种解释。
\end{itemize}
```

## E191 · CS5222/course-notes/Chapter03.tex:250

渲染核对发现rdt2.2标题孤留页底；为标题及开头状态解释预留空间

原文：
```tex
\StudyHeading{2}{rdt2.2：让ACK带编号，便可去掉NAK}
```

改为：
```tex
\Needspace{10\baselineskip}
\StudyHeading{2}{rdt2.2：让ACK带编号，便可去掉NAK}
```

## E192 · CS5489/course-notes/Lecture01.tex:227

局部不换行指令没有消除行首句号；缩短英文起句以使标点自然跟随代码，操作及条件不变

原文：
```tex
Starting with \StudyInline{x=2}, apply \StudyInline{x+=3} and then \StudyInline{x*=2}\nobreak. What is the result?
```

改为：
```tex
From \StudyInline{x=2}, apply \StudyInline{x+=3} and then \StudyInline{x*=2}. What is the result?
```

## E193 · CS5222/course-notes/Chapter03.tex:273

标题移到正文同页后，再让紧随状态图的短题答从同一页起排

原文：
```tex
\textbf{独立题 / Check：} rdt2.2中A(0)已正确交付
```

改为：
```tex
\Needspace{12\baselineskip}
\textbf{独立题 / Check：} rdt2.2中A(0)已正确交付
```
