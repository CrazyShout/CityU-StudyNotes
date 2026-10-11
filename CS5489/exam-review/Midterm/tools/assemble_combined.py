"""Derive the combined reading copy from the two authoritative manuscripts."""
from pathlib import Path
import argparse
import json
import re

ROOT = Path(__file__).resolve().parents[1]
APPENDIX = '<h2 id="source-differences">'


def question_blocks(text):
    return {match[1]: match[0].strip() for match in re.finditer(
        r'^## (MT\d{3}) · [^\n]*\n.*?(?=\n<a id="mt|\n<h2|\Z)', text, re.M | re.S)}


def combined_source(root=ROOT):
    questions = (root / 'Questions.md').read_text()
    answers = (root / 'Answers.md').read_text()
    index = json.loads((root / 'QuestionIndex.json').read_text())
    ids = [q['id'] for q in index['questions']]
    qb, ab = question_blocks(questions), question_blocks(answers)
    assert list(qb) == list(ab) == ids and len(ids) == 67
    toc = answers.split('## 目录\n', 1)[1].split('\n<a id="mt', 1)[0].strip()
    lines = [
        '<!-- Generated from Questions.md and Answers.md by tools/assemble_combined.py. -->',
        '# CS5489 · 期中题目与答案合订本 / Midterm Questions and Answers', '',
        '六套历年期中卷的78个原题位置，去重后共67题。每题依次给出完整英文原题、中文题意、English answer、中文对应答案和详细讲解，题目与答案连续阅读。', '',
        '各组沿用从基础到应用的阅读顺序，MT编号是稳定查题编号。每题另起一页，长题自然续页；目录、题间回指和册末原卷索引均指向本册页码。', '',
        '必要原题图保留在题目处，较长延伸标为选读。两道Gaussian Process题仍属于历史范围拓展。2021B*保留封面年份冲突说明；随卷答案差异见题后短注及册末勘误，2025A学生手写答案不作为标准答案。', '',
        '## 目录', '', toc, '',
    ]
    for question in index['questions']:
        qid = question['id']
        # The answer header supplies the common title/topic. Its repeated prompt
        # and figures are replaced by the complete bilingual question block.
        header = ab[qid].split('### 中文题意\n', 1)[0].strip()
        prompt = '### English question\n' + qb[qid].split('### English question\n', 1)[1]
        prompt = prompt.rsplit('\n[题目](', 1)[0].strip()
        answer = '### English answer\n' + ab[qid].split('### English answer\n', 1)[1]
        answer = answer.rsplit('\n[题目](', 1)[0].strip()
        assert prompt.count('### 中文题意\n') == 1
        assert '### 中文题意\n' not in answer
        lines += [f'<a id="{qid.lower()}"></a>']
        lines += [f'<a id="{alias.lower()}"></a>' for alias in question['legacy_ids']]
        lines += [header, '', prompt, '', answer, '',
                  f'[返回本题](Combined.md#{qid.lower()})', '']
    assert answers.count(APPENDIX) == 1
    lines += [APPENDIX + answers.split(APPENDIX, 1)[1].strip(), '',
              '## 原卷索引 / Original-paper index', '',
              '按原卷题号查找同一道题；不同年份的同题可能指向相同MT编号。2021B*按配套答案归档，题纸封面的年份冲突仍保留。', '']
    for paper in index['papers']:
        lines += [f"### {paper['label']}", '',
                  '| 原题 | 本册题号与页码 | 分值 |', '|---|---|---|']
        entries = [(occ, q) for q in index['questions'] for occ in q['occurrences'] if occ['paper'] == paper['id']]
        assert len(entries) == 13
        for occ, q in sorted(entries, key=lambda item: int(item[0]['question'][1:])):
            lines.append(f"| {occ['question']} | [{q['id']}](Combined.md#{q['id'].lower()}) | {occ['marks']} |")
        lines.append('')
    text = '\n'.join(lines).rstrip() + '\n'
    return re.sub(r'(?:Questions|Answers)\.md#(mt\d{3})', r'Combined.md#\1', text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Check the generated copy without writing')
    args = parser.parse_args()
    expected = combined_source()
    target = ROOT / 'Combined.md'
    if args.check:
        assert target.is_file() and target.read_text() == expected, 'Combined.md is stale; run tools/build_all.py'
    else:
        target.write_text(expected)
    print('Combined manuscript: 67 complete bilingual questions and answers; 78 original-paper positions.')


if __name__ == '__main__':
    main()
