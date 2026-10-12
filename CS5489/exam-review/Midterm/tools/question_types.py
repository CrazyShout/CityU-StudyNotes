"""Question-format labels; classification follows the original task, not difficulty."""
import re
from collections import Counter

TASK_LABELS = {
    'explain': '解释', 'recommend': '提出办法', 'diagnose': '诊断问题',
    'compare': '比较', 'judge': '判断并说明', 'formulate': '列式',
    'draw': '作图', 'example': '举例', 'interpret': '读图或公式',
    'rank': '排序', 'design': '设计', 'derive': '计算推导',
}


def toc_marker(question):
    if question['response_type'] == 'written':
        return '简答'
    return '多选·选错' if question['select'] == 'incorrect' else '多选'


def type_label(question):
    if question['response_type'] == 'multiple_select':
        label = '选择题（多选） / Multiple select'
        if question['select'] == 'incorrect':
            label += ' · 选不正确项 / Select incorrect statements'
        return label
    tasks = [t for t in question['tasks'] if t != 'explain' or 'judge' not in question['tasks']]
    return '简答题 / Written response · ' + '、'.join(TASK_LABELS[t] for t in tasks)


def validate_types(index, blocks):
    counts = Counter()
    for question in index['questions']:
        qid = question['id']
        block = blocks[qid]
        english = block.split('### English question\n', 1)[1].split('### 中文题意\n', 1)[0]
        chinese = block.split('### 中文题意\n', 1)[1].split('\n[题目](', 1)[0]
        options = re.findall(r'^([A-E])\)', english, re.M)
        expected_type = 'multiple_select' if 'select all that apply' in english.lower() else 'written'
        assert question['response_type'] == expected_type, (qid, 'Question format differs from original prompt')
        counts[expected_type] += 1
        if expected_type == 'multiple_select':
            assert options == list('ABCDE'[:len(options)]) and len(options) in (4, 5), (qid, 'Options missing')
            assert re.findall(r'(?<![A-Za-z])([A-E])）', chinese) == options, (qid, 'Chinese options differ')
            direction = 'incorrect' if re.search(r'\bnot\s+(?:true|correct)\b', english, re.I) else 'correct'
            assert question['select'] == direction, (qid, 'Selection direction differs')
            assert 'tasks' not in question
        else:
            assert not options and 'select' not in question, (qid, 'Written task has a choice label')
            assert question['tasks'] and len(set(question['tasks'])) == len(question['tasks'])
            assert set(question['tasks']) <= set(TASK_LABELS), (qid, 'Unknown written-task label')
    assert counts == {'multiple_select': 30, 'written': 37}, counts
    return dict(counts)
