"""Derive bilingual questions and concise answers without the explanatory sections."""
from pathlib import Path
import argparse
import json
import re
from assemble_combined import question_blocks
from question_types import toc_marker, type_label, validate_types
from book_editions import CONCISE_KINDS, SPLIT_TYPES, selected_questions

ROOT = Path(__file__).resolve().parents[1]
# These questions ask for a drawing or an intuitive example. Their answer figures
# are part of the answer; the MT045 explanatory geometry figure is not included.
ANSWER_FIGURES = {
    'MT048': ('answer-kernel-map.png', '答案示例图 / Answer example'),
    'MT050': ('answer-asymmetric-loss.png', '作图示例：图中 $b=c_-=4$、$a=c_+=1$。 / Example plot with $b=c_-=4$ and $a=c_+=1$.'),
    'MT051': ('answer-zero-loss-error.png', '答案示例图 / Answer example'),
    'MT060': ('answer-mt060-pair.png', '随卷答案草图：右图表示较小正$C$，不表示严格$C\\to0^+$。 / Supplied sketches: the right plot represents a smaller positive $C$, not the strict $C\\to0^+$ limit.'),
    'MT063': ('answer-huber.png', '按题干公式作图 / Plot of the given formula'),
    'MT064': ('answer-huber.png', '按题干公式作图 / Plot of the given formula'),
}


def concise_answer(block):
    return '### English answer\n' + block.split('### English answer\n', 1)[1].split('### 中文讲解\n', 1)[0].strip()


def compact_source(root=ROOT, kind='Compact'):
    assert kind in CONCISE_KINDS, kind
    questions = (root / 'Questions.md').read_text()
    answers = (root / 'Answers.md').read_text()
    index = json.loads((root / 'QuestionIndex.json').read_text())
    qb, ab = question_blocks(questions), question_blocks(answers)
    ids = [q['id'] for q in index['questions']]
    assert list(qb) == list(ab) == ids and len(ids) == 67
    validate_types(index, qb)
    selected = selected_questions(index, kind)
    toc = questions.split('## 目录\n', 1)[1].split('\n<a id="mt', 1)[0].strip()
    if kind in SPLIT_TYPES:
        parts = []
        for group in index['groups']:
            entries = [q for q in selected if q['group'] == group['id']]
            if entries:
                parts += ['**' + group['title'] + '**', '']
                parts += [f"- [{q['id']} · {q['title']}](#{q['id'].lower()})" for q in entries]
                parts.append('')
        toc = '\n'.join(parts).strip()
    for question in selected:
        toc = re.sub(r'(\[' + question['id'] + r' · [^\]]+)(\]\(#)',
                     lambda m: m[1] + '〔' + toc_marker(question) + '〕' + m[2], toc)
    lines = [
        '<!-- Generated from Questions.md and Answers.md by tools/assemble_compact.py. -->',
        '# CS5489 · 期中精简题答 / Concise Bilingual Questions and Answers', '',
        '67题：完整英文原题、中文题意、英文答案及中文对应答案。保留必要题图、作答图和成立条件，不收录详细解析。', '',
        '30道选择题均为多选；37道简答题包括判断说明、计算推导、作图和综合问答。题型表示作答方式，不表示难度；要求选择不正确选项的题另标“选错”。 / 30 multiple-select and 37 written-response questions; select-incorrect questions are marked separately.', '',
        '题目沿用基础到应用的顺序，MT编号与其他版本一致。两道Gaussian Process题为历史拓展；2021B*的年份冲突及原解差异按已有核查说明保留。目录和册末原卷索引均使用本册页码。', '',
        '## 目录', '', toc, '',
    ]
    if kind in SPLIT_TYPES:
        label, english = ('选择题', 'Multiple-Select Questions') if kind == 'MultipleChoice' else ('简答题', 'Written-Response Questions')
        intro = ('均为多选；MT001、MT014、MT029要求选择不正确的选项，另标“选错”。'
                 if kind == 'MultipleChoice' else
                 '简答包括判断说明、比较、计算推导、作图和综合问答；原题要求的理由、步骤与图均须作答。')
        lines = [
            '<!-- Generated from Questions.md and Answers.md by tools/assemble_compact.py. -->',
            f'# CS5489 · 期中{label}与答案 / {english} and Answers', '',
            f'{len(selected)}题：完整英文原题、中文题意、英文答案及中文对应答案。保留必要题图、作答图和成立条件，不收录详细解析。', '',
            intro, '',
            '沿用MT编号和组内顺序，目录与原卷索引使用本册页码。Gaussian Process题仍为历史拓展。', '',
            '## 目录', '', toc, '',
        ]
    for question in selected:
        qid = question['id']
        prompt = qb[qid].rsplit('\n[题目](', 1)[0].strip()
        title, body = prompt.split('\n', 1)
        prompt = title + '\n\n**题型：** ' + type_label(question) + '\n' + body
        answer = concise_answer(ab[qid])
        assert answer.count('### 中文对应答案\n') == 1
        lines += [f'<a id="{qid.lower()}"></a>']
        lines += [f'<a id="{alias.lower()}"></a>' for alias in question['legacy_ids']]
        lines += [prompt, '', answer, '']
        if qid in ANSWER_FIGURES:
            name, caption = ANSWER_FIGURES[qid]
            figure = next(m[0] for m in re.finditer(r'!\[[^\]]*\]\(assets/[^)]+\)', ab[qid]) if f'assets/{name})' in m[0])
            lines += [figure, '', f'*{caption}*', '']
        # MT043 already carries the heading-variant note in its question header.
        if '题头差异：' not in prompt:
            notes = re.findall(r'^\*\*原题差异 / Source note：\*\*[^\n]*', ab[qid], re.M)
            for note in notes:
                lines += [note, '']
    lines += ['## 原卷索引 / Original-paper index', '',
              ('仅列本册题型在各原卷中的位置；未列题目在另一题型分册。' if kind in SPLIT_TYPES else '') +
              '按原卷题号查找本册位置；不同年份的重复题指向同一MT编号。2021B*保留题纸与配套答案的年份冲突。', '']
    for paper in index['papers']:
        lines += [f"### {paper['label']}", '', '| 原题 | 本册题号与页码 | 分值 |', '|---|---|---|']
        entries = [(o, q) for q in selected for o in q['occurrences'] if o['paper'] == paper['id']]
        assert entries
        if kind == 'Compact':
            assert len(entries) == 13
        for occ, question in sorted(entries, key=lambda item: int(item[0]['question'][1:])):
            qid = question['id']
            lines.append(f"| {occ['question']} | [{qid}]({kind}.md#{qid.lower()}) | {occ['marks']} |")
        lines.append('')
    result = '\n'.join(lines).rstrip() + '\n'
    result = re.sub(r'(?:Questions|Answers)\.md#(mt\d{3})', kind + r'.md#\1', result)
    assert '### 中文讲解' not in result and '### 中文对应答案' in result
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--kind', choices=CONCISE_KINDS, default='Compact')
    args = parser.parse_args()
    expected = compact_source(kind=args.kind)
    target = ROOT / f'{args.kind}.md'
    if args.check:
        assert target.read_text() == expected, f'{target.name} is stale; run tools/build_all.py'
    else:
        target.write_text(expected)
    print(f'{args.kind}: complete bilingual questions and concise answers, without explanations.')
