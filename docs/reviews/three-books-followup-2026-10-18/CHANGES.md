# 精确修订记录

只记录本轮变化；同一位置的后续压缩保留过程，最终以TeX为准。

## 1. F01 · learning/foundation-notes/MathForML.tex:270

原文：

```tex
\ensuremath{\sqrt{\vphantom{x}}}a
```

改文：

```tex
\(\sqrt{a}\)
```

## 2. F01 · learning/foundation-notes/MathForML.tex:270

原文：

```tex
\ensuremath{\sqrt{\vphantom{x}}}9=3
```

改文：

```tex
\(\sqrt{9}=3\)
```

## 3. F01 · learning/foundation-notes/MathForML.tex:522

原文：

```tex
\ensuremath{\sqrt{\vphantom{x}}}2
```

改文：

```tex
\(\sqrt{2}\)
```

## 4. F01 · learning/foundation-notes/MathForML.tex:998

原文：

```tex
s=\ensuremath{\sqrt{\vphantom{x}}}(8/3)\ensuremath{\approx}1.633 cm
```

改文：

```tex
\(s=\sqrt{8/3}\approx1.633\) cm
```

## 5. F01 · learning/foundation-notes/MathForML.tex:1172

原文：

```tex
\ensuremath{\sqrt{\vphantom{x}}}det(\ensuremath{\Sigma})
```

改文：

```tex
\(\sqrt{\det(\Sigma)}\)
```

## 6. F01 · CS5489/course-notes/Lecture01.tex:500

原文：

```tex
\ensuremath{\sqrt{\vphantom{x}}}(x\textsuperscript{T}x)
```

改文：

```tex
\(\sqrt{x^T x}\)
```

## 7. F01 · CS5489/course-notes/Lecture01.tex:532

原文：

```tex
\ensuremath{\sqrt{\vphantom{x}}}14
```

改文：

```tex
\(\sqrt{14}\)
```

## 8. F01 · CS5489/course-notes/Lecture01.tex:532

原文：

```tex
\ensuremath{\sqrt{\vphantom{x}}}6
```

改文：

```tex
\(\sqrt{6}\)
```

## 9. F01 · CS5489/course-notes/Tutorial01.tex:220

原文：

```tex
\ensuremath{\sqrt{\vphantom{x}}}2
```

改文：

```tex
\(\sqrt{2}\)
```

## 10. F01 · CS5489/course-notes/Lecture04.tex:467

原文：

```tex
\ensuremath{\sqrt{\vphantom{x}}}2
```

改文：

```tex
\(\sqrt{2}\)
```

## 11. F02 · CS5489/course-notes/Tutorial02.tex:341

原文：

```tex
两个模型后验接近。
```

改文：

```tex
同一MNB模型给Business与Sci/Tech的后验概率接近。
```

## 12. F03 · CS5489/course-notes/Tutorial04.tex:310

原文：

```tex
残差法保留旧季节形状，却也依赖“差值规律能迁移到后九个月”的假设。
```

改文：

```tex
残差法在旧预测上加修正，仍可能改变季节曲线，并依赖“差值规律能迁移到后九个月”的假设。
```

## 13. F04 · CS5222/course-notes/Chapter03.tex:454

原文：

```tex
Seven ACKs in each case; their final value differs.
```

改文：

```tex
GBN sends ACKs 0,1,2,3,4,5,5; SR sends 0,1,2,3,4,5,7. Each receiver sends seven ACKs because the lost packet never arrives.
```

## 14. F05 · CS5222/course-notes/Chapter02.tex:409

原文：

```tex
解释视频由连续图像组成；
```

改文：

```tex
视频由连续的图像帧组成；
```

## 15. F06 · CS5489/course-notes/Lecture01.tex:323

原文：

```tex
\StudyInline{[x*x for x in values if x\%2=\allowbreak{}=\allowbreak{}0]}
```

改文：

```tex
\StudyInline{[x*x for x in [1,2,3,4] if x\%2=\allowbreak{}=\allowbreak{}0]}
```

## 16. F02 · CS5489/course-notes/Tutorial02.tex:345

原文：

```tex
These observations suggest explanations to test; retain the supplied evaluation labels.
```

改文：

```tex
For index 14, Business and Sci/Tech have similar posterior probabilities under the same MNB model. These observations suggest explanations to test; retain the supplied evaluation labels.
```

## 17. F04 · CS5222/course-notes/Chapter03.tex:454

原文：

```tex
GBN sends ACKs 0,1,2,3,4,5,5; SR sends 0,1,2,3,4,5,7. Each receiver sends seven ACKs because the lost packet never arrives.
```

改文：

```tex
GBN: 0,1,2,3,4,5,5; SR: 0,1,2,3,4,5,7.
```

候选PDF中加长的英文说明使后页TCP图整幅后移；保留题目所求两串编号，省去重复计数解释。

## 18. F07 · learning/foundation-notes/MathForML.tex:306

原文：

```tex
平方和不是10\textsuperscript{2}。\\

\textbf{English answer:}
```

改文：

```tex
平方和不是10\textsuperscript{2}。

\textbf{English answer:}
```

基础册p.7短答案中英文被拆页；去掉段落分隔前重复的强制换行，保留完整题答。
