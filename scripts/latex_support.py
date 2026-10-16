"""Shared TeX support for saved notebook output and the one-time migration.

Formal teaching text is authored in .tex files. HTML handling is limited to
saved notebook MIME output and the explicitly invoked historical migration.
"""
from __future__ import annotations
from pathlib import Path
from urllib.parse import urlsplit, unquote
import hashlib
import copy
import re
from bs4 import BeautifulSoup, NavigableString, Comment, Tag

ROOT = Path(__file__).resolve().parents[1]
SPECIAL = {
    '\\': r'\textbackslash{}', '{': r'\{', '}': r'\}', '%': r'\%',
    '&': r'\&', '#': r'\#', '_': r'\_', '$': r'\$', '~': r'\textasciitilde{}',
    '^': r'\textasciicircum{}',
}
SYMBOLS = {
    '→': r'\to', '←': r'\leftarrow', '↔': r'\leftrightarrow', '⇒': r'\Rightarrow',
    '⇔': r'\Leftrightarrow', '≥': r'\ge', '≤': r'\le', '≠': r'\ne',
    '≈': r'\approx', '×': r'\times', '÷': r'\div', '±': r'\pm', '∞': r'\infty',
    '∑': r'\sum', '∏': r'\prod', '∈': r'\in', '∉': r'\notin', '⊥': r'\perp',
    '∇': r'\nabla', '√': r'\sqrt{\vphantom{x}}', '∂': r'\partial',
    'α': r'\alpha', 'β': r'\beta', 'γ': r'\gamma', 'δ': r'\delta',
    'ε': r'\epsilon', 'θ': r'\theta', 'λ': r'\lambda', 'μ': r'\mu',
    'µ': r'\mu', 'π': r'\pi', 'ρ': r'\rho', 'σ': r'\sigma', 'τ': r'\tau',
    'φ': r'\phi', 'ω': r'\omega', 'Σ': r'\Sigma', 'Δ': r'\Delta',
    'Θ': r'\Theta', 'Λ': r'\Lambda', 'Φ': r'\Phi', 'Ω': r'\Omega',
    '∅': r'\varnothing', 'ℝ': r'\mathbb{R}', 'ℓ': r'\ell', '⋅': r'\cdot',
    '∩': r'\cap', '∫': r'\int', '′': r'\prime', '″': r'\prime\prime',
    '∝': r'\propto', '≡': r'\equiv', '∼': r'\sim', '≪': r'\ll', '≫': r'\gg',
}
SUB = str.maketrans('₀₁₂₃₄₅₆₇₈₉ᵢⱼₖₙ', '0123456789ijkn')
SUP = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻', '0123456789+-')


def escape(text: str) -> str:
    out = []
    for c in text:
        if c in SPECIAL:
            out.append(SPECIAL[c])
        elif c in SYMBOLS:
            out.append(r'\ensuremath{' + SYMBOLS[c] + '}')
        elif c in '₀₁₂₃₄₅₆₇₈₉ᵢⱼₖₙ':
            out.append(r'\textsubscript{' + c.translate(SUB) + '}')
        elif c in '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻':
            out.append(r'\textsuperscript{' + c.translate(SUP) + '}')
        elif c == '−':
            out.append(r'\ensuremath{-}')
        elif c == '\u00a0':
            out.append('~')
        elif c in '\u200b\u200c\u200d\ufeff':
            continue
        else:
            out.append(c)
    return ''.join(out)


def math_tex(text: str) -> str:
    # The mathematical content and explicit tags remain native TeX.
    for c, command in SYMBOLS.items():
        text = text.replace(c, command + ' ')
    text = text.replace('−', '-')
    return text


class Renderer:
    def __init__(self, source: Path, docid: str, registry: dict[str, str],
                 *, first_heading=True):
        self.source = source
        self.docid = docid
        self.registry = registry
        self.first_heading = first_heading
        self.events = []
        self.anchors = []
        self.pending = []
        self.images = []
        self.math = []
        self.tables = 0
        self.codes = []
        self.unknown = set()

    def event(self, kind, value):
        self.events.append([kind, value])

    def target(self, name):
        if name not in self.anchors:
            self.anchors.append(name)
            return r'\StudyTarget{' + self.docid + '__' + name + '}\n'
        return ''

    def flush_targets(self):
        out = ''.join(self.target(a) for a in self.pending)
        self.pending = []
        return out

    def children(self, node, cell=False):
        return ''.join(self.render(c, cell=cell) for c in node.children)

    def image(self, node, cell=False):
        src = node.get('src', '')
        parsed = urlsplit(src)
        if parsed.scheme == 'file':
            p = Path(unquote(parsed.path))
        elif not parsed.scheme:
            p = (self.source.parent / unquote(parsed.path)).resolve()
        else:
            raise ValueError(f'Remote image needs a local asset: {src}')
        if not p.is_relative_to(ROOT) or not p.is_file():
            raise ValueError(f'Missing/outside image: {p}')
        rel = p.relative_to(ROOT).as_posix()
        self.images.append(rel)
        self.event('image', rel)
        command = 'StudyCellImage' if cell else 'StudyImage'
        return '\\' + command + '{' + rel + '}' + ('' if cell else '\n\n')

    def table(self, node):
        rows = node.find_all('tr', recursive=False)
        if not rows:
            rows = [r for r in node.find_all('tr') if r.find_parent('table') is node]
        if not rows:
            return ''
        matrix = [r.find_all(['th', 'td'], recursive=False) for r in rows]
        n = max(len(r) for r in matrix)
        if any(len(r) != n for r in matrix):
            raise ValueError(f'Irregular table in {self.source}: {[len(r) for r in matrix]}')
        if n > 7:
            # Saved DataFrame output keeps every value and repeats its row index.
            # Column panels are more readable than shrinking seventeen columns.
            chunks=[]
            for start in range(1,n,5):
                columns=[0]+list(range(start,min(start+5,n)))
                soup=BeautifulSoup('<table></table>','html.parser')
                for cells in matrix:
                    row=soup.new_tag('tr')
                    for j in columns:row.append(copy.deepcopy(cells[j]))
                    soup.table.append(row)
                chunks.append(self.table(soup.table))
            return '\n'.join(chunks)
        # Widths follow content, with a floor for labels and a cap on dominance.
        scores = []
        for col in range(n):
            lengths = [min(100, len(r[col].get_text(' ', strip=True))) for r in matrix]
            score = max(5, sum(lengths) / len(lengths)) ** .55
            scores.append(score)
        weights = [s / sum(scores) for s in scores]
        spec = ''.join(
            r'>{\raggedright\arraybackslash}p{\dimexpr'
            + f'{w:.6f}' + r'\linewidth-' + f'{2*(n-1)/n:.5f}'
            + r'\tabcolsep\relax}' for w in weights)
        self.tables += 1
        self.event('table', [len(rows), n])
        lines = [r'\begingroup', r'\small\setlength{\tabcolsep}{3pt}',
                 r'\renewcommand{\arraystretch}{1.22}',
                 r'\begin{longtable}{@{}' + spec + '@{}}', r'\toprule']
        rendered = []
        for row in matrix:
            rendered.append(' & '.join(self.children(c, cell=True).strip() for c in row) + r' \\')
        header = bool(rows[0].find('th'))
        if header:
            lines.extend([rendered[0], r'\midrule\endfirsthead',
                          rendered[0], r'\midrule\endhead', r'\bottomrule\endfoot'])
            lines.extend(rendered[1:])
        else:
            lines.extend(rendered)
        if not header:lines.append(r'\bottomrule')
        lines.extend([r'\end{longtable}', r'\endgroup', ''])
        return '\n'.join(lines) + '\n'

    def render(self, node, *, cell=False):
        if isinstance(node, Comment):
            text = str(node).strip()
            if text.startswith('EXAM:'):
                return '% ' + text + '\n'
            return ''
        if isinstance(node, NavigableString):
            text = str(node)
            if not text.strip():
                return ' ' if cell else text
            self.event('text', text)
            return escape(text)
        if not isinstance(node, Tag):
            return ''
        name = node.name
        classes = node.get('class', [])
        if name in ['script', 'style', 'nav'] or any(c in classes for c in ['toc','reading-toc','source-note']):
            return ''
        if name == 'div' and 'notebook-code-reference' in classes:
            self.event('notebook-code', node['data-cell'])
            return self.flush_targets() + r'\StudyNotebookCell{' + node['data-notebook'] + '}{' + node['data-cell'] + '}\n\n'
        if 'arithmatex' in classes:
            raw = node.get_text()
            display = name == 'div'
            if raw.startswith((r'\(', r'\[')):
                raw = raw[2:-2]
            self.math.append({'display': display, 'tex': raw.strip()})
            self.event('math', raw.strip())
            return ('\n\\[\n' + math_tex(raw.strip()) + '\n\\]\n\n' if display
                    else r'\(' + math_tex(raw.strip()) + r'\)')
        if name == 'a' and node.has_attr('id') and not node.has_attr('href'):
            self.pending.append(node['id'])
            return self.children(node, cell=cell)
        if name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            title = self.children(node).strip()
            key = node.get('id', '')
            if name == 'h1' and self.first_heading:
                self.first_heading = False
                out = r'\StudyChapter{' + self.docid + '}{' + title + '}\n'
            else:
                level = min(4, max(1, int(name[1]) - 1))
                out = r'\StudyHeading{' + str(level) + '}{' + title + '}\n'
            if key:
                self.pending.append(key)
            return '\n' + out + self.flush_targets() + '\n'
        if name == 'img':
            return self.flush_targets() + self.image(node, cell)
        if name in ['strong', 'b']:
            return r'\textbf{' + self.children(node, cell) + '}'
        if name in ['em', 'i']:
            return r'\emph{' + self.children(node, cell) + '}'
        if name in ['del', 's']:
            return r'\sout{' + self.children(node, cell) + '}'
        if name == 'br':
            return r'\newline{} ' if cell else r'\\' + '\n'
        if name == 'sup':
            return r'\textsuperscript{' + self.children(node, cell) + '}'
        if name == 'sub':
            return r'\textsubscript{' + self.children(node, cell) + '}'
        if name == 'code' and node.find_parent('pre') is None:
            text = node.get_text()
            self.event('code-inline', text)
            return r'\StudyInline{' + ''.join(escape(c)+(r'\allowbreak{}' if c in '().,/=_:' else '') for c in text) + '}'
        if name == 'pre':
            text = node.get_text().rstrip('\n')
            self.codes.append(text)
            self.event('code', text)
            return '\n\\begin{StudyCode}\n' + text + '\n\\end{StudyCode}\n\n'
        if name == 'table':
            return self.flush_targets() + self.table(node)
        if name in ['ul', 'ol']:
            env = 'itemize' if name == 'ul' else 'enumerate'
            options = '[start=' + node.get('start', '1') + ']' if name == 'ol' else ''
            return '\n\\begin{' + env + '}' + options + '\n' + self.children(node) + '\\end{' + env + '}\n\n'
        if name == 'li':
            return '\\item ' + self.children(node).strip() + '\n'
        if name == 'blockquote':
            return '\n\\begin{quote}\n' + self.children(node) + '\\end{quote}\n\n'
        if name == 'details':
            summary = node.find('summary', recursive=False)
            title = self.children(summary).strip() if summary else '答案 / Answer'
            content = ''.join(self.render(c) for c in node.children if c is not summary)
            return '\n\\begin{StudySolution}{' + title + '}\n' + content + '\\end{StudySolution}\n\n'
        if name == 'summary':
            return ''
        if name == 'a' and node.has_attr('href'):
            label = self.children(node, cell).strip()
            href = node['href']
            parsed = urlsplit(href)
            if not parsed.scheme and not parsed.netloc:
                p = ((self.source.parent / unquote(parsed.path)).resolve()
                     if parsed.path else self.source)
                if p.suffix == '.html' and str(p.relative_to(ROOT)) not in self.registry:
                    for extension in ['.md', '.ipynb']:
                        if p.with_suffix(extension).is_file():
                            p = p.with_suffix(extension)
                            break
                rel = p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else None
                if rel in self.registry:
                    return r'\StudyRef{' + self.registry[rel] + '}{' + (unquote(parsed.fragment) or 'root') + '}{' + label + '}'
                if rel and p.exists():
                    return r'\StudyRepoRef{' + rel + '}{' + parsed.fragment + '}{' + label + '}'
                raise ValueError(f'Unresolved link in {self.source}: {href}')
            return r'\href{' + escape(href) + '}{' + label + '}'
        if name == 'hr':
            return '\n\\par\\smallskip\\noindent\\rule{\\linewidth}{.3pt}\\smallskip\\par\n'
        if name == 'span' and 'exam-badge' in classes:
            kind = next((c[5:] for c in classes if c.startswith('exam-') and c != 'exam-badge'), 'mid')
            return r'\StudyBadge{' + kind + '}{' + self.children(node, cell) + '} '
        if name == 'p':
            if node.find_parent(['td', 'th']):
                return self.children(node, True) + r'\newline{} '
            return self.flush_targets() + self.children(node).strip() + '\n\n'
        if name in ['div', 'span', 'main', 'section', 'figure', 'figcaption', 'font',
                    'html', 'body', 'center', 'thead', 'tbody', 'tfoot']:
            if node.has_attr('id'):
                self.pending.append(node['id'])
            return self.children(node, cell)
        self.unknown.add(name)
        raise ValueError(f'Unsupported HTML element {name} in {self.source}')

    def convert(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        content = soup.main or soup
        tex = self.children(content) + self.flush_targets()
        # A single source owns the prose; this metadata records counts/hashes only.
        report = {
            'source': self.source.relative_to(ROOT).as_posix(), 'docid': self.docid,
            'events': len(self.events), 'event_sha256': hashlib.sha256(
                repr(self.events).encode()).hexdigest(), 'anchors': self.anchors,
            'images': self.images, 'math': self.math, 'tables': self.tables,
            'code_blocks': len(self.codes), 'unknown_elements': sorted(self.unknown),
            'tex_sha256': hashlib.sha256(tex.encode()).hexdigest(),
        }
        return tex, report
