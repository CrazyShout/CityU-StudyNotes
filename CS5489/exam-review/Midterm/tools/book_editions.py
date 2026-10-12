"""Edition names and question selection shared by the midterm build tools."""

EDITION_FLAGS = {
    'Combined': '--combined',
    'Compact': '--compact',
    'MultipleChoice': '--multiple-choice',
    'WrittenResponse': '--written-response',
}
SPLIT_TYPES = {'MultipleChoice': 'multiple_select', 'WrittenResponse': 'written'}
CONCISE_KINDS = ('Compact', *SPLIT_TYPES)
ALL_KINDS = ('Questions', 'Answers', *EDITION_FLAGS)


def add_edition_arguments(parser):
    group = parser.add_mutually_exclusive_group()
    for kind, flag in EDITION_FLAGS.items():
        group.add_argument(flag, dest='edition', action='store_const', const=kind,
                           help=f'Use the {kind} edition and its independent page map')


def selected_questions(index, kind):
    questions = index['questions']
    if kind in SPLIT_TYPES:
        questions = [q for q in questions if q['response_type'] == SPLIT_TYPES[kind]]
    return questions
