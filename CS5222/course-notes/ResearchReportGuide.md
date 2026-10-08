# Research Report Guide｜把一个真实问题解释清楚

[课程目录](README.md) · [Chapter1](Chapter01.md) · [Chapter2](Chapter02.md) · 原任务与Rubric · [课程信息栏](https://crazyshout.github.io/micro-course/notices.html)

这份指南帮助你选题、解释机制、核查资料和整理反思。原任务要求研究你在日常生活、新闻或工作中遇到的新网络技术，联系教材Chapter1–7，排除Chapter8安全主题；用自己的解释和图说明机制，并反思学习过程。格式、页数、评分与提交要求以链接的当前原任务为准。

按选题补基础：涉及码率/吞吐就回[网络单位](../../learning/foundation-notes/NetworkBasics.md#units)，涉及状态/时间就回[报文与时间轴](../../learning/foundation-notes/NetworkBasics.md#messages)。没有实际卡点便直接开始。

| 能力 | 优先级 | 难度与卡点 | 达标表现；依据 |
|---|---|---|---|
| 明确问题、解释机制 | 核心必会 | 中至高；不能只有名词 | 不看原文也能画出数据/控制流；原任务A |
| 来源核查与边界 | 核心必会 | 中；资料版本/适用场景 | 每个关键结论有对应证据；原任务p2 |
| 图文与英语表达 | 核心必会 | 中；精简与可读 | 图能帮助解释一个具体难点；原Rubric |
| 真实反思 | 核心必会 | 中；具体变化而非套话 | 记录自己确实做过的核查与困难；原任务B |
| 复杂数学/未用机制 | 按需拓展 | 可能高 | 只有支撑论点时补；整理者建议，不暗示不考 |

## 1. 选题从一件事开始，不从一串热门缩写开始

先记录你**确实遇到**的情况：某个应用在带宽变化时切画质、同一内容从不同地点下载速度不同、多人共享网络时服务突然卡顿。题目应围绕一个能解释的机制问题，例如“客户端怎样在吞吐波动时选择下一视频块的编码版本”。

接着用三道筛子缩小范围：这个问题属于网络吗？能对应教材哪一层/哪章？在本次篇幅内能用一幅图、一个小场景说明主要机制吗？“所有5G技术”往往太宽；“某种特定机制在什么条件下改善什么问题”更容易论证。选题的新意应落在具体变化、部署或问题上。若选DASH等课内基础，需说明你研究的具体新变化、部署或问题，不能只复述课件。

**English framing (整理表达):** *This report examines how [a specific mechanism] addresses [a concrete networking problem] under [a defined setting].* 方括号中填写你的具体问题、机制和调查情境。

## 2. 把问题、机制、效果连成一条可核查的解释

先写旧方法遇到什么限制，再写新机制改了哪一步，最后讨论收益与代价。不要“协议很先进，所以性能很好”这样跳过中间因果链。

以分块视频为**教学例**：播放每秒消耗编码数据 → 网络吞吐会变动 → 缓冲可能耗尽 → 客户端按估计吞吐/缓冲选择下一块 → 可能减少停顿，但画质也会变化。这里每条箭头都能被课程概念支持，而不是把“自适应”三个字当解释。

**完整补算 / Worked example:** 4秒片段编码2Mbps，数据量8Mbit；若稳定吞吐4Mbps，下载2秒。在缓冲足够、同时播放、忽略请求与解码开销时，缓冲净增加4−2=2秒。 / A four-second segment encoded at 2 Mbps contains 8 Mbit. At 4 Mbps throughput it downloads in two seconds, increasing the playable buffer by two seconds under the stated assumptions.

**变式 / Transfer:** 网络降至1Mbps，同一块需几秒？若开始时只缓冲3秒会发生什么？ / At 1 Mbps, how long does the same chunk take, and what if only three seconds are buffered initially?

<details markdown="1"><summary>答案 / Answer</summary>

下载8秒，已有缓冲只能撑3秒，理想模型中会停顿约5秒，等块到后才续播。 / Download takes eight seconds; under the simplified model, playback stalls for about five seconds. 这说明要考虑安全余量和估计误差，而不是平均值刚好够就万事大吉。

</details>

上面是理想模型的教学算例；实际停顿还取决于播放器策略和网络变化。

## 3. 找来源时，为每一句重要话准备证据

优先找协议标准、技术提供方文档、原始研究论文或可复核的测量报告。二手讲解和AI适合帮助形成问题，但需要回到原资料核对。阅读来源时，找到直接支持该结论的段落或数据。

| 写作中的主张 | 应找的证据 | 必须检查 |
|---|---|---|
| 协议怎样工作 | 规范/原设计文档 | 版本、消息顺序、可选项、条件 |
| 某产品使用此机制 | 官方当前产品文档 | 原生/浏览器/企业部署是否相同 |
| 性能提高多少 | 原实验/可重复测量 | 对比方法、数据、指标、环境 |
| 有哪些限制 | 规范限制、实验失败或设计分析 | 不把推断写成已测事实 |
| 为什么和课程有关 | 教材/当前课件定位 | 是当前已学，还是教材后续章节 |

可维护一张很小的工作表，放在你自己的研究草稿里：`Claim | Source/section | Version/date | Supports what | Does not support what`。用它检查每条主张与来源是否对应。

如引用AI输出，原任务要求说明使用并自行负责核查；图、引用也要查，不能只给一个模型名字就当技术来源。对论文核对题名、作者、年份、DOI/官方页面，打开原文确认所引结论和实验设置。查不到原文的来源标为待核查，确认后再引用。

## 4. 图要解释困难，不是给文字化妆

选择一种与你的核心问题匹配的图：

- 交互问题画时序图，标清参与者、请求、响应、时间方向；
- 架构问题画节点与数据/控制流，说明图中箭头是什么；
- 权衡问题画有单位的曲线，说明数据来自实测、论文还是教学计算。

画完问自己：读者通过这张图能更容易答出哪个问题？节点之间的箭头应说明数据从哪里来、到哪里去，以及每一步做什么。引用原图标来源，改编图标“Adapted from…”，自己计算的图保存脚本和输入。AI图同样要署明并逐条检查技术结构，不能因为好看就默认网络方向正确。

## 5. 英文报告怎样组织才连贯

建议采用内容驱动的小标题，而非每段中英对照：英文完成正式论证，中文草稿帮助自己先讲懂。术语第一次出现给全称与缩写，随后保持一致。可以按以下结构组织：

1. **Problem and context**：你实际怎样接触主题？问题是什么、研究范围到哪里？
2. **Background from the course**：挑真正用到的1–3个概念，解释它们为何必要。
3. **How the mechanism works**：沿一个具体请求/数据流走完步骤，配关键图。
4. **Benefits, limits and evidence**：哪项收益有证据，代价是什么，什么条件下不适用？
5. **Discussion**：你基于证据形成的判断、未解决问题与合理后续方向。

每段先给主张，再解释机制，再放证据与条件。比如 *The mechanism reduces repeated origin fetches when reusable content is available in cache* 比 *It greatly improves everything* 更可核查。不要把“可能”藏起来，也不用给每句话堆三个形容词。

**英文自测 / English self-check:** *What changes, why does it help, and under what conditions might it not help? / 改变了什么，为何有效，何时可能无效？* 若不能脱稿回答，正文还需要补机制，而非继续增加术语。

## 6. Reflection log｜写你真的经历过的理解变化

原任务的五个问题，可以分别对应一条具体记录：

| 原问题 | 真实记录的抓手 |
|---|---|
| What did you learn that you did not know before? | 原来怎么理解，哪个具体事实改变了它 |
| What was the most challenging part? | 一个真正卡住的机制/推导/资料冲突 |
| How did GenAI help or hinder? | 它帮你拆了哪一步，或给过什么误导 |
| How did you verify AI-generated information? | 打开了哪个原来源、比对哪句、做了什么检查 |
| What would you do differently next time? | 一个具体可实行的改进 |

可从现在开始记两三条带日期的研究记录，报告结束时据实整理。写清你做过什么、哪里卡住、怎样查证，以及理解发生了什么变化；工具使用情况按实际记录。

## 7. 交付前的自查与来源覆盖

读者应能复述你的问题与机制，认出它对应课程哪部分；一张图能独立读懂；数字都有单位、来源和条件；观点与已验证事实分开。英语表达、引用、AI使用说明、格式与评分要求逐项回查原任务及课程信息。

| 原任务位置 | 本指南对应 |
|---|---|
| p1 Goal、题目范围 | 开篇、§1 |
| p1 Format、提交构成 | 原任务/信息栏链接；不生成正式提交件 |
| p1 A：接触途径、机制、联系、动机/创新/挑战/观点 | §1–2、§5 |
| p1 自己的表达、图与清晰度 | §4–5 |
| p2 GenAI引用、图/参考核查责任 | §3–4 |
| p2 B：五个Reflection问题 | §6逐项对应 |
| p2 Evaluation、p3 Rubric | 开篇能力表、§7；具体权重以原页为准 |

确定主题后，再围绕核心问题补充必要基础、原始来源和图示。
