# Assignment 1 · SMS Classification
# 从课堂概率模型到一个可解释、可复现的短信分类实验

本地方法指南 · 2026-09-22

[Lecture 2 整讲讲义](Lecture02.md) · [Tutorial 2 可运行示范](Tutorial02.ipynb) · [运行与文件说明](README.md)

本指南用手算例子解释评价指标，再给出短信实验的数据流程、代码接口和检查方法。实验由你按原任务完成；文中的教学算例和实际文件统计分别标注。

主要来源：Assignment1-Doc.ipynb（23个单元）、Assignment1-Final.ipynb（11个单元）。单元从原文件第一个单元开始计数。截止日期、评分与提交手续见[课程信息](https://crazyshout.github.io/micro-course/notices.html?course=CS5489)，本文件集中解释技术工作。

## 本作业怎样接上 Lecture 2？

Lecture 2教你把文字表示为向量，再估计每类的分布，用Bayes规则分类。Tutorial 2让你在新闻上跑过表示、模型、比较、错分和调参。Assignment 1把目标换成短信，并要求你自己选择一条可靠的流程、解释尝试过程、复现最终预测。

动手前需要接好这几个环节：标签是否一致，文本和Id是否对齐，哪份数据允许选参数，使用什么指标，以及最终Notebook能否从干净状态生成同样结果。

| 环节 | 学习优先级 | 难度与卡点 | 掌握要求 | 依据 |
|---|---|---|---|---|
| 数据、标签、Id与Usage | 核心必会 | 中：几份文件的角色不同 | 会对齐与验证，解释数据流 | Assignment1-Doc，第5–12个单元、Assignment1-Final，第5–6个单元及实际CSV |
| Balanced accuracy | 核心必会 | 中：宏平均与整体比例不同 | 手算、解释、用于选择 | Assignment1-Doc，第3个单元 Evaluation |
| 表示与NB基线 | 核心必会 | 中：预处理也要拟合 | 能连接Lecture2与Tutorial2 | Assignment1-Doc，第3个单元 Methodology、Lecture2b |
| 验证与受控比较 | 核心必会 | 高：测试不能参与反复选择 | 会制定协议并记录尝试 | Assignment1-Doc，第3个单元 Methodology/Evaluation |
| 错误分析与复现 | 核心必会 | 中：解释必须落到证据 | 会检查、定位、重跑 | Assignment1-Doc，第3个单元、Assignment1-Doc，第17–23个单元、Assignment1-Final，第3/8个单元 |
| 逻辑回归、SVM等候选 | 常规掌握 | 中到高：另有先修 | 需要时回Lecture3学习 | Assignment1-Doc，第3个单元允许自选方法；当前Lecture3 |

这些是整理者基于当前任务的学习优先级，不是往年题型频率或本学期考试预测。

<a id="task"></a>
## 1. Goal｜先把预测目标说清楚

一条输入是短信文本，输出只有一个标签：

| 标签 | 原英文名称 | 本任务中的含义 |
|---|---|---|
| 0 | normal | 正常短信 |
| 1 | spam | 垃圾短信 |
| 2 | smishing | 通过短信实施的钓鱼信息 |

Smishing是短信钓鱼，在本作业单列一类。不要因为它也具有垃圾信息特征，就把1和2合并；也不要在画图、编码和导出时更换标签顺序。模型的classes_与预测概率列必须明确对应。

**English takeaway：** The input is an SMS text and the output is one of three specified labels: normal, spam or smishing. Keep the same label mapping throughout preprocessing, evaluation and prediction output.


**来源与掌握要求：** Assignment1-Doc，第2–5个单元。核心必会；难度低；要求准确解释输入、输出与类别。

<a id="files"></a>

## 2. Load the Data｜三份数据文件分别承担什么工作？

本次实际文件如下。TXT的内容也按CSV规则读；文本里可能有逗号，不能简单用字符串split(",")拆每一行。

| 当前原文件 | 实际结构与规模 | 用途 |
|---|---|---|
| smishing_train.txt | 无表头，2985行；每行文本、标签两列 | 训练与训练内部验证 |
| smishing_val_test.txt | 无表头，2986行；每行只有文本 | 待预测的验证／测试文本，顺序须保留 |
| smishing_val_test.csv | 有表头Id、Prediction、Usage，共2986行 | 标签／用途元数据，通过Id与上一文件对应 |

训练标签数量为 normal 2454、spam 234、smishing 297，说明多数类明显更多。Usage有1493条val和1493条test；当前Id唯一且恰为1到2986。

**原课核对：** Assignment1-Doc，第5个单元文字提到smishing_test.txt，但当前代码Assignment1-Doc，第10个单元和实际下载文件使用smishing_val_test.txt。Assignment1-Doc，第5个单元又称标签CSV“only contains the SMS text”，也与实际三列表头不符。读取时以当前文件结构及代码为准。

Prediction这个列名在元数据中提供类别值，**并不是你刚训练出的模型预测**。当前文件的val和test部分都能读到类别数值；能看到不意味着可以用test标签选参数。保持老师明确区分的Usage含义。

建议在训练前完成以下检查：

~~~python
# 接口示意：此处不进行训练或写提交文件。
texts_train, labels_train = read_text_data(train_path)
texts_eval, _ = read_text_data(eval_text_path)
metadata = read_split_metadata(meta_path)

# 保留CSV里的Id；确认它确实对应原文本行号。
assert metadata["Id"].is_unique
assert metadata["Id"].tolist() == list(range(1, len(texts_eval) + 1))
assert set(metadata["Usage"]) == {"val", "test"}
assert len(metadata) == len(texts_eval)
~~~

若将来Id不连续，不能继续靠“数组第i个元素配Id=i+1”猜。先确认提供者的映射规则，再建立显式对应。重复文本也不应直接删掉：先检查是否跨划分、标签是否冲突；评价与最终输出仍需保持原题要求的记录集合和顺序。

**English takeaway：** The evaluation text file and metadata have different roles. Align them using the supplied IDs and preserve the original text order. Visible test labels must not be used for model selection.


**来源与掌握要求：** Assignment1-Doc，第5–10个单元、Assignment1-Final，第5–6个单元。核心必会；难度中；要求能画出训练与评估的数据流。

<a id="metric"></a>

## 3. Evaluation｜为什么普通accuracy不够？

如果大部分短信是normal，全部猜normal就能拿到看似不错的普通accuracy，却可能完全漏掉spam和smishing。老师因此指定 **balanced accuracy（平衡准确率）**。

在三类都有真实样本的普通多类分类中：

$$\mathrm{Recall}_c=\frac{\mathrm{TP}_c}{\text{真实属于类别c的样本数}},
\qquad
\mathrm{BalancedAccuracy}=\frac13\sum_{c=0}^{2}\mathrm{Recall}_c.$$

Recall（召回率）问“该类真实样本找回多少”。Accuracy是整体预测正确比例；precision是“预测成该类的记录中有多少是真的”。这三个英文词不能混译为同一种“准确”。

### 完整手算 / Worked example

下面用一张**教学混淆矩阵**演示计算。行是真实标签，列是预测标签：

English context: This synthetic matrix illustrates the calculation. Rows are true labels; columns are predicted labels.

| True \ Predicted | normal | spam | smishing | 该类真实数 |
|---|---:|---:|---:|---:|
| normal | 90 | 5 | 5 | 100 |
| spam | 10 | 5 | 5 | 20 |
| smishing | 4 | 2 | 4 | 10 |

中文题：求普通accuracy和balanced accuracy，再与全部猜normal比较。  
English question: Compute ordinary and balanced accuracy, then compare with predicting normal for every example.

1. 对角线正确数为90+5+4=99，总数130，普通accuracy为 $99/130\approx76.15\%$。
2. 三类召回率为90/100=0.90、5/20=0.25、4/10=0.40。
3. Balanced accuracy为 $(0.90+0.25+0.40)/3=0.5167$，约51.67%。
4. 全部猜normal时普通accuracy为100/130≈76.92%，反而略高；但三类召回率是1、0、0，balanced accuracy只有1/3≈33.33%。

English answer: Ordinary accuracy is 99/130≈76.15%, while balanced accuracy is (0.90+0.25+0.40)/3≈51.67%. The always-normal baseline has higher ordinary accuracy, 100/130≈76.92%, but balanced accuracy of only 1/3.

因此，这份作业应按指定的balanced accuracy选择方案。Balanced accuracy给每个类别相同的平均权重；它并不意味着已经显式定义了每一种误报／漏报的现实成本，也不能由此省略混淆矩阵。

### 独立变式 / Transfer

中文题：另一模型的三类召回率为0.8、0.5、0.6，真实类别数量仍是100、20、10。求两种accuracy。  
English question: Another model has recalls 0.8, 0.5 and 0.6 with the same true class counts 100, 20 and 10. Compute both accuracies.

答案：正确数80+10+6=96，普通accuracy=96/130≈73.85%；balanced accuracy=(0.8+0.5+0.6)/3≈63.33%。整体正确数少了一点，但少数类召回改善，故指定指标更高。  
English answer: There are 96 correct predictions, giving ordinary accuracy≈73.85% and balanced accuracy≈63.33%. Better minority-class recall improves the assigned metric despite fewer total correct predictions.

用分层训练内部验证尽量保证每一折都有三类。若某类没有真实样本，召回率分母为零，必须说明评价约定，此时该类召回率不能按这个分式计算。这里采用sklearn默认的未调整balanced accuracy，而不是adjusted=True。[官方指标定义](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.balanced_accuracy_score.html)

**English takeaway：** Balanced accuracy is the mean recall over classes in this setting. It limits majority-class dominance, but the confusion matrix is still needed to understand which errors remain.


**来源与掌握要求：** Assignment1-Doc，第3个单元 Evaluation。核心必会；难度中；要求手算并解释指标。

<a id="baseline"></a>

## 4. Methodology｜先跑通一条可信的基线

可以从Lecture 2和Tutorial 2的NB流程开始：

> 原训练短信 → 训练内部划分 → 词表与表示 → NB模型 → 验证预测 → balanced accuracy与混淆矩阵。

可以先比较“CountVectorizer＋BernoulliNB”和“词计数或TF-IDF＋MultinomialNB”。前者看词出现与未出现，后者看计数或非负权重。短信短、含数字和URL，所以新闻实验里的停用词、词表规模、最优alpha不能原封不动当成作业答案。

列出基线配置时至少写清：小写化、分词、是否删停用词、词或字符n-gram、词表上限、TF-IDF规范、模型与alpha。每一项都改变“模型看见什么”；例如清洗掉所有数字可能同时删掉无用编号与有用金额特征，需要验证，不凭直觉宣布一定更好。

为代码定义清楚接口，比把全部步骤塞进一个单元更容易复现：

~~~python
def load_inputs(data_dir):
    # 返回训练文本/标签、评估文本、Id/Usage元数据
    ...

def build_pipeline(config):
    # 返回表示+分类器的Pipeline；这里不在全量数据上提前fit
    ...

def evaluate_on_validation(pipeline, train_text, train_y,
                           val_text, val_y):
    # 训练、验证预测、指标和混淆矩阵；不使用test标签
    ...
~~~

这些接口需要你补充实现。具体NB调用可回看[Tutorial 2](Tutorial02.ipynb)，公式含义见[Lecture 2](Lecture02.md#comparison)。

**English takeaway：** Establish a reproducible baseline with explicit preprocessing and an aligned metric. Treat the vectorizer and any learned text transformation as part of the fitted model pipeline.


**来源与掌握要求：** Assignment1-Doc，第3个单元 Methodology、Assignment1-Doc，第17个单元。核心必会；难度中；要求能说明每一步输入输出。

<a id="validation"></a>

## 5. Validation｜每份数据什么时候能用？

可以按下面的顺序组织实验：

1. **开发候选：** 在smishing_train内部使用分层划分或分层交叉验证，选少量有理由的配置。样板建议5折、shuffle=True、random_state=42；原模板的全局随机种子为100，两者需明确记录，不混称同一次划分。
2. **每折独立拟合预处理：** 词表和IDF必须在该折训练部分拟合，不能先对全部2985条fit_transform再做CV。用Pipeline将预处理与分类器一起交给搜索器。
3. **按val检查与选择：** 使用Usage=="val"的记录执行原题的验证选择。若模型有迭代checkpoint，使用val决定保留哪一步；NB没有逐轮checkpoint，也仍有模型/参数选择。
4. **冻结方案：** 写下配置、训练数据使用范围、种子和依赖版本。若是否允许并入val重拟合没有明确规定，先保守地保持原训练集拟合，保留val/test用于指定的验证与最终评价。
5. **最后评价：** 方案固定后再使用test作最终报告。不能因test结果不满意而返回调参，并继续声称它是独立测试。

原任务要求生成评估文本的预测。即使最终输出覆盖val与test全部2986条，也不代表训练时可以使用全部对应标签。“预测哪些记录”和“用哪些记录选择模型”是两个不同问题。

**伪代码 / Pseudocode**

~~~text
load training texts and labels
load evaluation texts plus Id/Usage metadata
define a small candidate set
for each candidate:
    cross-validate the whole preprocessing/model pipeline inside training data
select promising candidates
fit each candidate on the permitted training data
compare on Usage == "val" using balanced accuracy
freeze the selected procedure
evaluate on Usage == "test" only after freezing
verify IDs and output schema when preparing the required final artifact
~~~

**English takeaway：** Validation selects the procedure; test data assess the fixed choice. All learned preprocessing belongs inside the training fold. Producing predictions for a record does not authorize using its true label for development.


**来源与掌握要求：** Assignment1-Doc，第3个单元 Evaluation/Methodology及Usage字段。核心必会；难度高；要求能解释选择与最终评价的边界。

<a id="compare"></a>

## 6. 怎样增加一个有理由的实验？
**依据：Assignment1-Doc，第3个单元允许自选方法并要求记录尝试。常规掌握；难度中；要求提出可检验假设。**

每次改动先写一句理由，例如“保留字符片段可能帮助识别拼写变体”，再说明怎样保持其他条件相同。不要同时换词表、模型、划分和评价指标，最后只说“新方案好”。

| 要比较什么 | 可以改变什么 | 应保持什么 | 需要记录什么 |
|---|---|---|---|
| 平滑强度 | alpha | 文本划分、表示、指标 | 各候选验证值，不只冠军 |
| 表示方式 | count / TF-IDF / binary | 尽可能相同的候选流程与评价协议 | 数值含义与模型是否兼容 |
| n-gram范围 | unigram / bigram等 | 数据、指标、搜索预算 | 特征规模和稀疏性变化 |
| 类别不平衡处理 | 适用模型的权重或采样策略 | 评价集合与标签定义 | 各类召回率，采样仅在训练折 |
| 模型家族 | NB / 逻辑回归 / SVM | 同一验证协议与可比预算 | 方法差别，不只参数名称 |

逻辑回归、线性SVM和核方法属于跨讲可选路径：分别回[ML10](https://crazyshout.github.io/micro-course/?lesson=ml10)、[ML12](https://crazyshout.github.io/micro-course/?lesson=ml12)、[ML14](https://crazyshout.github.io/micro-course/?lesson=ml14)。原作业允许选择其他算法，不等于必须把所有候选都训练一次。

每个实验记录一行即可：配置ID、数据协议、表示、模型、关键参数、验证balanced accuracy、三类recall、耗时和解释。尚未运行的配置标为“待运行”。

**English takeaway：** State a hypothesis for each change and compare candidates under the same validation protocol. Record unsuccessful attempts as well as improvements, without treating one score difference as proof of causation.

<a id="errors"></a>
## 7. Error analysis｜把“错了”变成下一步能查的线索
**依据：Assignment1-Doc，第3个单元 Documentation与原课错误查看。核心必会；难度中；要求用证据解释。**

先看哪一类召回最低、被错分到哪里，再抽取少量验证集错误。保留原文本、真值、预测、模型使用到的特征及对应分数；展示文本时只取判断所需片段，不把整份数据贴进报告。

对一条错误按顺序问：文本是否读取完整？列和Id是否对齐？关键信息是否被清洗或词表截断？这两个类别是否在词袋上很像？模型是否只靠一个常见词给出很高置信？若怀疑标签问题，记录证据，不为了提高分数直接改评价标签。

应把“观察”和“待验证解释”写成两句。例如：“三个smishing验证样本被预测为spam”是观察；“模型没有利用链接结构”是需要查特征和做对照的假设。**开发阶段**使用val或训练内部验证的错误来改进方法，避免反复依据test错误设计新规则。

**回到老师的明确要求：** Assignment1-Doc，第3个单元 的 Results and Visualization 还要求展示**测试集中的正确分类与错误分类样本**，并对错分提出解释。因此，冻结方案并完成最终测试后，再选取这两类样本解释模型的表现与局限；开发阶段的调参则使用val或训练内部验证。若据此产生新的改进想法，将它列作后续工作，并用新的未触碰数据检验。

**English takeaway：** Diagnose data alignment and representation before inventing a model story. Use validation errors for development. After freezing the procedure and evaluating it, the assignment also requires examples of both correctly and incorrectly classified test samples. Analyze them descriptively while reserving model development and tuning for validation data.

<a id="reproducibility"></a>
## 8. Final submission notebook｜换个干净内核，还能生成一样的预测吗？

Assignment1-Doc记录探索过程；Assignment1-Final负责重现最后的固定流程。探索Notebook里变量“碰巧存在”，不代表Final能独立运行。

原模板Assignment1-Doc，第14个单元随机选择标签，只演示Id,Prediction文件格式，不能用作训练好的基线或实验成绩。另一处实际问题是：**Assignment1-Final，第6个单元使用pd.read_csv，但Assignment1-Final，第4个单元没有导入pandas as pd**；如果之前没有在同一内核里运行Doc的导入，会出现未定义名称。自己的Final应显式包含需要的导入，不能依赖另一个Notebook。

准备最终结果时检查：

- 从干净内核运行，数据路径、文件编码和依赖均明确。
- 训练数据、划分、种子、配置与文档说明一致。
- 词表、IDF与分类器使用同一条固定流程。
- 报告包含方案冻结后的正确与错误测试样本及有边界的解释，满足Assignment1-Doc，第3个单元的结果分析要求。
- 每条评估文本恰有一个合法预测，取值只为0、1、2。
- Id唯一、覆盖范围和顺序正确；没有排序预测数组却忘记同步Id。
- 原模板writer按照位置产生i+1；仅在已确认当前位置对应这些Id时使用。
- 在相同环境中从头重跑，固定流程给出同样的预测；跨版本变化要重新检查。

预测CSV及提交格式要求见Canvas和[课程信息](https://crazyshout.github.io/micro-course/notices.html?course=CS5489)为准。

**English takeaway：** A reproducible final notebook must declare its own imports, data paths, preprocessing, parameters and random seeds. Correct predictions with incorrect ID alignment still produce an invalid output.


**来源与掌握要求：** Assignment1-Doc，第3个单元、Assignment1-Doc，第13–17个单元、Assignment1-Final，第3–8个单元。核心必会；难度中；要求解释并验证可复现性。

<a id="check"></a>

## 9. 合上指南，检查自己能否解释

**Q1 中文：** 为什么普通accuracy更高的模型，可能不符合这份作业的选择目标？  
**Q1 English:** Why might a model with higher ordinary accuracy be less suitable under the assignment metric?  
**答：** 多数类主导整体比例；balanced accuracy看三类recall的均值，因此要比较指定指标与每类表现。  
**Answer:** Majority-class performance can dominate ordinary accuracy. The assigned metric averages class recalls, so compare balanced accuracy and per-class results.

**Q2 中文：** 没用test标签，但把test文本放进词表拟合，是否仍影响独立评价？  
**Q2 English:** Does including test text in vocabulary fitting affect independent evaluation even without using its labels?  
**答：** 会，表示已经利用test信息；预处理也是拟合的一部分。  
**Answer:** Yes. Representation learning used test information; preprocessing is part of fitting.

**Q3 中文：** CSV中Id完整且预测都合法，能否证明文件正确？  
**Q3 English:** Do complete IDs and valid class values prove that a prediction file is correct?  
**答：** 不能，还要验证每个预测是否对应同Id的原短信，以及流程是否按允许的数据训练。  
**Answer:** No. Verify that each prediction matches the text with that ID and that the procedure used only permitted training data.

**Q4 中文：** 本文件的51.67%能否写进自己的作业实验结果？  
**Q4 English:** Can the 51.67% in this guide be reported as your assignment result?  
**答：** 不能，它是人为混淆矩阵的教学计算，没有训练短信分类器。  
**Answer:** No. It is a calculation from an artificial teaching matrix, not a trained SMS classifier's measured result.

已有卡片可配合：[M091类别不平衡](https://crazyshout.github.io/micro-course/cards.html#CS5489-M091)、[M092 balanced accuracy](https://crazyshout.github.io/micro-course/cards.html#CS5489-M092)、[M095数据泄漏](https://crazyshout.github.io/micro-course/cards.html#CS5489-M095)、[M099错误分析](https://crazyshout.github.io/micro-course/cards.html#CS5489-M099)。第一次先完成数据流与指标手算，再按需要复习实验方法卡。

## 10. 原任务覆盖与来源

| 原位置 | 本指南位置／处理 |
|---|---|
| Assignment1-Doc，第1–2个单元 | 标题与任务；Assignment1-Doc，第1个单元为空白单元 |
| Assignment1-Doc，第3个单元 Goal / Methodology / Evaluation | §1、3–7；明确任务、指标和实验流程 |
| Assignment1-Doc，第3个单元 What to hand in / Documentation / Grading | 技术复现见§8；行政清单链接课程信息 |
| Assignment1-Doc，第4–6个单元 | §2 数据文件与读取要求 |
| Assignment1-Doc，第7–12个单元 | §2、8 运行设置、读取函数、标签与元数据 |
| Assignment1-Doc，第13–14个单元 | §8 随机预测仅为格式示例 |
| Assignment1-Doc，第15–16个单元 | §2、7 数据查看；建议先转NumPy数组再做标签布尔索引 |
| Assignment1-Doc，第17–23个单元 | §4–8承接自行实现与记录；其余为空白代码槽 |
| Assignment1-Final，第1–3个单元 | §8最终复现任务；Assignment1-Final，第1个单元为空白 |
| Assignment1-Final，第4–6个单元 | §2、8 读取、导入和文件对齐 |
| Assignment1-Final，第7–11个单元 | §8固定流程接口与验收；实现由学习者完成 |

本指南不把历史作业的做法当作这次作业要求；跨讲方法明确标来源。主要根据当前两份模板和实际文件，指标定义另参考scikit-learn官方文档。普通概率分类的基础回到[Lecture02.md](Lecture02.md)，完整运行示范回到[Tutorial02.ipynb](Tutorial02.ipynb)。