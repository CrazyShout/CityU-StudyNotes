# 三册正式 A4 PDF 全量审计与优化台账（2026-11-26）

## 1. 范围与原则

- **目标交付物（三册正式合订本）**：
  1. `pdf/CS5489-A4.pdf`（CS5489 机器学习整讲、配套实验与历年真题索引）
  2. `pdf/CS5222-A4.pdf`（CS5222 计算机网络整章、12 次教程、3 次作业与开卷速查附录）
  3. `pdf/Foundations-A4.pdf`（零基础数学补课、网络单位与字节先修、全学期来源与证据边界）
  - 同步保持两份独立期末真题合订本（`CS5489/exam-review/Final/CS5489-Final-Combined.pdf` 与 `CS5222/exam-review/Final/CS5222-Final-2021A-Combined.pdf`）文字规范、公式编号完整，并在入口目录中建立可点击引用。
- **三项核心优化维度**：
  1. **文字的表达**：消除后半程冲刺口号（如 `必考`、`秒杀法`、`考前头号预警`、连续感叹号 `！`）与内部维护自注（如 `Python 已核验`、`见同目录 tools/verify_...`），恢复平实、重条件、先给小算例再引出定义的教材散文；保证全英文考试所需的双语术语与 `English answer` / `English takeaway` 对齐；`\[` 前零空行。
  2. **整体的叙事逻辑**：消除 Part 1 遗留的 10 月初过时声明（如“后续章节尚未下载”“完整 CNN 待后续课件”“Chapter 3 后半章仍缺”），打通 `Foundations` $\leftrightarrow$ `Part 1` $\leftrightarrow$ `Part 2` $\leftrightarrow$ `Tutorials / Assignments / ExamIndex` 的双向 `\StudyRef` 跳转与章节承接导言。
  3. **参考已有资料的全面性**：逐份核对 `/Users/atlas/work/Course/` 下 2026 Canvas 全学期文件与历史真题/实验解答，补齐缺失教学模块、遗漏英文题干与 A–D 选项、重绘缺失拓扑图，修正与官方标答冲突的结论，并严守 CS5222 开卷考试“严禁夹带教材原书页面截图”的合规红线。
- **保留无问题段落与迁移契约不变式**：
  - `CS5489` 的 `Lecture01`–`05` 主体教学散文、`Tutorial01`–`04`（含 40 个受 SHA-256 保护的 Notebook 代码单元）、`Assignment01`–`02`，`CS5222` 的 `Chapter01`–`03` 主体教学散文、`Tutorial01`–`05` 主体教学散文、`ResearchReportGuide`，以及 `Foundations` 原有 `§1`–`§10` / `§1`–`§4` 均保持稳定，仅修补过时范围语句与前向导航链接，严格保留 `migration-manifest.json` 锁定的全部锚点、图片路径、1,236 条基础公式及原 `\tag{...}` 序列。

---

## 2. 分册问题清单与整改进度

### A. `Foundations-A4.pdf`（`learning/foundation-notes/`，50 页）

| 编号 | 文件 | 维度 | 发现问题 | 整改措施 | 状态 |
|---|---|---|---|---|---|
| F-01 | `SourceEvidence.tex` | 叙事逻辑 / 资料全面性 | 范围停留在 `2026-10-03`（声称仅下载至 `CS5489 L1–5`、`CS5222 Ch1–3 part1–2`，未反映全学期课件、两门课期末真题去重及 CS5222 公告 `646525` 开卷规则） | 更新为 `2026-11-26` 全学期材料与历史证据边界说明，同步扩充 `docs/source-materials.json`（补入 90 份下半学期原始文件哈希） | 已完成 |
| F-02 | `MathForML.tex` | 资料全面性 / 叙事逻辑 | 仅衔接 `Lecture 1–5`；`Lecture 8` 承诺的“特征值分解、正交矩阵”在 `MathForML` 中缺失，且缺随机变量期望、方差可加性、KL 散度与 Jensen 下界（EM/VAE/DDPM/LLM 先修） | 新增 `§11 特征值、特征向量与奇异值分解` 与 `§12 期望、KL 散度与变分下界`，更新首尾导航表返回 `Lecture 6–12`（不新增 `\tag` 以守住旧契约） | 已完成 |
| F-03 | `MathForML.tex` | 文字表达 | `§9` 正文多处直接裸写英文字符串 `eta`、`lambda` | 统一替换为数学排印 `\ensuremath{\eta}`、`\ensuremath{\lambda}`（保留原 `\(...\)` 公式不变） | 已完成 |
| F-04 | `NetworkBasics.tex` | 资料全面性 / 叙事逻辑 | 停留在 `2026-09-23`（4 节、5 页），缺 Part 2 核心先修：跨字节边界 `/x` 子网掩码与最长前缀匹配（CIDR/LPM）、模 2 无进位异或算术与多项式比特串互转（CRC） | 新增 `§5 子网前缀、按位与掩码与最长前缀匹配` 与 `§6 模 2 异或无进位算术与多项式校验`，补齐至 `Ch4–7` 与 `Tut6–12` 的回链 | 已完成 |

### B. `CS5222-A4.pdf`（`CS5222/course-notes/`，183 页）

| 编号 | 文件 | 维度 | 发现问题 | 整改措施 | 状态 |
|---|---|---|---|---|---|
| N-01 | `Assignment02.tex` + `verify_part2_examples.py` | 科学准确性（P0） | P22b 漏算超时重传前旧窗口尾包触发的重复确认 `ACK(k-5)`，误写为 4 个值 `{k-4..k-1}`；官方标答为 `[k-N-1, k-1] = {k-5..k-1}` 共 5 个值 | 修正为 `{k-5, k-4, k-3, k-2, k-1} (mod 1024)`，补充无乱序时间轴证明并同步更新校验脚本（66 条断言全过） | 已完成 |
| N-02 | `Assignment03.tex` | 科学准确性（P0） | P15(c) 因未画 `Figure 5.33` 漏看 Subnet 1 内部左侧交换机，误判 `S1` 会收到 `B->A` 单播 ARP 回复（官方标答为 **No**）；P8e 未列出官方教师手册标准 3 时隙非流水解 `2/3 msg/slot` | 重绘 `Figure 5.33`（标明 Subnet 1 内部交换机），修正 P15(c) 为 **No** 并解释自学习拦截机制；P8e 双列展示官方标准解 `2/3 msg/slot` 与跨轮流水线解 `1 msg/slot` | 已完成 |
| N-03 | `Chapter05.tex` + 配图 | 科学准确性（P0） | 将纯热土豆路由示例（S47）与完整 BGP 选路状态机（S46：`LOCAL_PREF` $\to$ 最短 `AS-PATH` $\to$ 热土豆 `NEXT-HOP`）混写，造成优先级自相矛盾 | 明确区分纯热土豆思想与完整 BGP 四步平局决胜顺序，重绘配图标题消除歧义 | 已完成 |
| N-04 | `Assignment01.tex` + `assets/assignment01-01..04.png` | 开卷合规 / 资料全面性 | `assignment01-01..04.png` 为带原书蓝色 `Figure 1.27` 题注的整页扫描截图，存在考场被误判为“教材打印节选”的风险；Zoom 题未对照已发布的 `Assignment 1 Solution.pdf`（含 `RTP/SRTP`、`WebRTC`、`TLS`） | 将 `assignment01-01..04.png` 替换为原创 Matplotlib 高清重绘原理图，在正文中排印完整英文题干并补充官方标答五项要点；标注公告 `646525` 免考范围 | 已完成 |
| N-05 | `Chapter02.tex`, `Chapter03.tex`, `Tutorial05.tex` | 叙事逻辑 | `Chapter03.tex` 仍写“流控、连接管理及拥塞控制待后续材料补充”；`Tutorial05.tex` 仍写“未下载教师解答”；缺跨半程跳转链接 | 清除过时待补声明，建立 `Chapter03` $\leftrightarrow$ `Chapter03Part3`、`Tutorial05` $\to$ `Tutorial06`、`Assignment01` $\to$ `Assignment02` 链接，标注 Socket/Wireshark 期末免考 | 已完成 |
| N-06 | `Chapter03Part3.tex`, `Chapter04`–`07.tex` | 文字表达 / 叙事逻辑 / 资料全面性 | 文风呈冲刺提纲（大量 `！`、`必考`、`秒杀法`、`Python 已核验`）；3 处课件页码错写分卷号（`6-49..54`, `7-23`, `7-13/14`）；缺 `Q&A_cha6_2025`（3 题）、`Q&A_cha3`/`cha4&5` 英文题干选项、Ch5 `2-1-7` 三节点 DV 多轮收敛表、CRC 多项式互转、Polling 轮询耗时、Ch6 §6 网页请求全栈总表、每章 `StudySolution` 自测变式、`English takeaway` 及来源覆盖表 | 全面改写为连续教材散文，补齐遗漏课堂问答、核心例题、重绘修正 `ch3p3-tcp-reno-cwnd.png` 等配图、补齐章末双语自测与来源覆盖表，并新增书末开卷速查附录 `ExamIndex.tex` | 已完成 |
| N-07 | `Tutorial06`–`12.tex`, `Assignment02`–`03.tex` | 文字表达 / 资料全面性 | 删去英文原题干与选择题 A–D 选项框，缺 `Tutorial10` P3（4-AS BGP）、`Tutorial12` P3（双子网 ARP）、`Assignment02` `Figure 4.30` 等核心拓扑图，缺英文标准答句与 `Tutorial11` 公式编号 | 补全全部英文原题干、A–D 选项框、精炼 `English answer`、原创重绘拓扑图与 `StudySolution` 独立变式 | 已完成 |

### C. `CS5489-A4.pdf`（`CS5489/course-notes/`，301 页）

| 编号 | 文件 | 维度 | 发现问题 | 整改措施 | 状态 |
|---|---|---|---|---|---|
| M-01 | 新增 `Tutorial05.tex`–`Tutorial09.tex` | 资料全面性 | Canvas 已提供 `Tutorial 5`（MLP 人脸检测与增强）、`Tutorial 6`（CNN 滑窗人脸检测）、`Tutorial 7`（ResNet50 深度特征与迁移学习蛋糕分类）、`Tutorial 8`（Olivetti 人脸 PCA/NMF/KPCA 识别与 PSNR 去噪）、`Tutorial 9`（Lab 颜色+空间坐标聚类图像分割与 ARI），但 `CS5489-A4.pdf` 仅收录 `Tutorial 1–4` | 编写原生 LaTeX 教程讲义 `Tutorial05.tex`–`Tutorial09.tex`，注册入双清单并与 `Lecture 5–9` 建立双向 `\StudyRef` | 已完成 |
| M-02 | `Lecture04.tex`, `Lecture05.tex`, `ExamIndex.tex`（及模板/脚本） | 叙事逻辑 / 资料全面性 | `Lecture05.tex` 仍写“暂未提供 Tutorial 5”“完整 CNN 仍待后续课件”；`ExamIndex.tex` 仅映射 `Lecture 1–5` 并写“其余题不计入当前讲义覆盖” | 更新 `Lecture04/05` 前向链接与状态说明；更新 `latex/exam/*.tex.in` 与 `scripts/build_exam_annotations.py`，在 `ExamIndex` 中补充 `Lecture 6–12` 全卷期末真题与东莞 2024/25 样题（`1a/1b/1c`）映射总表 | 已完成 |
| M-03 | `Lecture06.tex`–`Lecture12.tex` | 文字表达 / 叙事逻辑 / 资料全面性 | 文末残留内部脚本说明 `见同目录 tools/verify_...`；局部含 `绝对必争之地`、`背熟` 等口号及感叹号；缺指向 `Foundations-MathForML`（`§11` 特征值/SVD、`§12` 期望/KL/ELBO）与 `Tutorial 5–9`、`CS5489-Final-Combined.pdf` 的链接；补充 `Home_Assignments_4` 离散卷积定理衔接 | 清理维护自注与冲刺口号，补齐先修/实验/真题合订本链接，完善各讲过渡、自测变式与 `English takeaway` | 已完成 |
