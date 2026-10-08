# 运行Notebook所需的数据

阅读与生成PDF不需要原始数据。Notebook已保存实际输出；重新做实验时，请从自己有权访问的Canvas课程下载对应附件。

设置`COURSE_DATA_ROOT`指向包含下面目录结构的文件夹；不设置时使用仓库根目录的`data/`，该目录被Git忽略。

| Notebook | 相对于数据根目录的文件 |
|---|---|
| Tutorial01 | `CS5489/Lecture1/Tutorial/data1.pickle` |
| Tutorial02 | `CS5489/Lecture2/Tutorial2/dataAG.json` |
| Tutorial03 | `CS5489/Lecture3/Tutorial3/photos-bw.zip` |
| Tutorial04 | `CS5489/Lecture4/Tutorial/Bike-Sharing-Dataset.zip` |

```sh
source .venv/bin/activate
python -m pip install -r requirements-notebooks.txt
export COURSE_DATA_ROOT=/path/to/your/course-data
python CS5489/course-notes/tools/execute_tutorial.py --notebook Tutorial01.ipynb
```

可选Tutorial01–04；不指定时仍运行Tutorial02。Windows PowerShell使用`$env:COURSE_DATA_ROOT='C:\path\to\course-data'`。路径里的示例文字需替换为实际目录。

缺文件会明确报错，不能替换成随机数据并沿用旧成绩。原种子、数据划分、标签含义、单位与词表实验条件见每份Notebook。只改文件位置不需要重跑训练；结果解释仍对应原记录的实验。

其他作业附件按各自任务从Canvas取得，作业指南提供方法与接口，不包含个人正式提交文件。

## Lecture 2 图示与算例

重新生成Lecture 2图示与计算记录时，在同一数据根目录下提供`CS5489/Lecture2/Lecture2/iris2.csv`、`Lecture2b.ipynb`及原`email/`子目录。

```sh
python CS5489/course-notes/tools/lecture02_examples.py
```

脚本只重算Lecture 2例子和两张图，不执行Tutorial；原Notebook的邮件实验成绩从保存输出读取并标明身份。原文件仍只读，缺少文件时明确报错。仅阅读和构建PDF不需要这些输入。
