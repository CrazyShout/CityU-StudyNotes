"""Generate ignored HTML intermediates for A4 printing from MD and saved notebook outputs, without executing code."""
from pathlib import Path
import html,re,os,json
from urllib.parse import urlsplit,urlunsplit,unquote,quote
import nbformat,markdown
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
OUT=Path(__file__).resolve().parents[1]
CODEXING=OUT.parents[1]
FOUNDATION=CODEXING/'learning/foundation-notes/MathForML.md'
REGISTRY=CODEXING/'learning/course-notes-documents.json'
RECORDS=json.loads(REGISTRY.read_text())['documents']
DOCUMENTS={ (CODEXING/item['source']).resolve():item for item in RECORDS }
PREVIEWS={p:p.with_suffix('.html') for p in DOCUMENTS}
STYLE="""
:root{color-scheme:light}*{box-sizing:border-box}body{margin:0;background:#fcfbf8;color:#253746;font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Noto Sans CJK SC",sans-serif;line-height:1.86;font-size:17px}
main{max-width:900px;margin:0 auto;padding:32px 32px 80px}nav{font-size:14px;border-bottom:1px solid #d9dedb;padding-bottom:16px}a{color:#236588;text-underline-offset:3px}h1{font-size:30px;line-height:1.4;margin:30px 0 18px}h2{font-size:25px;line-height:1.45;margin:46px 0 18px;padding-top:8px}h3{font-size:20px;margin-top:30px}p{margin:14px 0}strong{color:#1b3546}blockquote{border-left:3px solid #bb9a53;padding:3px 20px;margin:22px 0;background:#f5f2e8}
img{max-width:100%;height:auto}table{border-collapse:collapse;font-size:14px;width:100%;min-width:440px;margin:16px 0}th,td{padding:9px 12px;border-bottom:1px solid #d9dedb;vertical-align:top;text-align:left}th{background:#edf1ee}td p{margin:0}.table-scroll{overflow-x:auto;max-width:100%}
pre{padding:17px;background:#f0f3f3;font-size:13px;line-height:1.6;overflow:auto;border-left:2px solid #b3c5ca;white-space:pre}code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}pre code{white-space:pre}.code-input{margin:24px 0 6px}.cell-label{font-size:12px;color:#607580}.output{margin:6px 0 24px}.output pre{background:#fbfbf8;border-color:#d8d9ce}
details{margin:18px 0;padding:8px 0}summary{cursor:pointer;color:#236588;font-weight:600}.katex-display{overflow-x:auto;overflow-y:hidden;padding:5px 0}.katex{font-size:1.04em;position:relative}.katex-display>.katex{max-width:100%;overflow-x:auto;overflow-y:hidden}.arithmatex{overflow-x:auto}a,td,p{overflow-wrap:anywhere}.toc{font-size:15px;border-left:2px solid #d9dedb;padding-left:18px}.source-note{font-size:13px;color:#607580}
.table-scroll::before{display:none}th:first-child{min-width:84px}
@media(max-width:600px){main{padding:18px 17px 60px}body{font-size:16px}h1{font-size:25px}h2{font-size:22px}table{font-size:13px}.table-scroll::before{content:"宽表可左右滑动 / Swipe wide tables";display:block;font-size:11px;color:#607580}}
""" + HtmlFormatter().get_style_defs('.highlight')
STYLE += (CODEXING/'scripts/exam_markers.css').read_text()
def md(text):
    rendered=markdown.markdown(text,extensions=['tables','fenced_code','toc','md_in_html','pymdownx.arithmatex'],
           extension_configs={'pymdownx.arithmatex':{'generic':True}})
    # A raw comparison such as P<T or $0<yf<1$ can be mistaken for an
    # unfinished HTML tag before md_in_html runs. A visible formula alone
    # does not prove that the following answer/figure remains in details.
    if re.search(r'<details\b[^>]*\bmarkdown=',rendered) or re.search(r'<p>\s*<details\b',rendered):
        raise ValueError('Unparsed details block: use &lt; in prose or \\lt in TeX comparisons; inspect the following answer/figure.')
    return rendered
def relative_href(target, source):
    return quote(os.path.relpath(target, PREVIEWS[source].parent), safe='/')
def rewrite_href(href, source):
    parsed=urlsplit(html.unescape(href))
    if parsed.scheme or parsed.netloc or not parsed.path:
        return href
    target=(source.parent/unquote(parsed.path)).resolve()
    if target not in PREVIEWS:
        return href  # Original materials and unregistered files stay untouched.
    return html.escape(urlunsplit(parsed._replace(path=relative_href(PREVIEWS[target],source))),quote=True)
def wrap(title,body,source):
    # Notebook markdown cells each generate their own heading IDs. Preserve the
    # first occurrence (and old deep links), suffix only later collisions.
    seen={}
    def unique_id(match):
        key=match.group(1);seen[key]=seen.get(key,0)+1
        return ' id="'+key+('' if seen[key]==1 else '-'+str(seen[key]))+'"'
    body=re.sub(r' id="([^"]+)"',unique_id,body)
    body=re.sub(r'(href=")([^"]+)(")',lambda m:m.group(1)+rewrite_href(m.group(2),source)+m.group(3),body)
    body=re.sub(r'(<table\b[\s\S]*?</table>)',r'<div class="table-scroll" tabindex="0" role="region" aria-label="可横向滚动的表格 / Horizontally scrollable table">\1</div>',body)
    # Long article navigation is optional on screen; print assembly expands details.
    body=re.sub(r'(<div class="toc">[\s\S]*?</div>)', r'<details class="reading-toc"><summary>本页目录 / Contents</summary>\1</details>', body)
    # Reuse the already-vendored KaTeX files; no external scripts or services.
    prefix=relative_href(CODEXING/'vendor/katex',source)+'/'
    nav=' · '.join('<a href="'+relative_href(PREVIEWS.get(p,p),source)+'">'+label+'</a>' for p,label in [
        (CODEXING/'CS5489/course-notes/README.md','CS5489目录'),
        (CODEXING/'CS5222/course-notes/README.md','CS5222目录'),
        (FOUNDATION,'数学基础'),(FOUNDATION.with_name('NetworkBasics.md'),'网络基础')])
    style=STYLE
    if source==OUT/'Lecture02.md':
        # The fixed-right KaTeX tag can cover a long equation on a phone.
        # Place it on its own line in this reading preview; A4 styles are separate.
        style+='@media screen and (max-width:600px){.katex-display>.katex>.katex-html>.tag{position:static;display:block;text-align:right;margin-top:8px}.katex-display>.katex>.katex-html>.tag>.strut{display:none}}'
    return ('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
      '<title>'+html.escape(title)+'</title><link rel="stylesheet" href="'+prefix+'katex.min.css"><style>'+style+'</style></head><body><main>'
      '<nav>本地学习讲义　 '+nav+'</nav>'
      +body+'<p class="source-note">本地阅读版 · <a href="'+relative_href(source,source)+'">打开作者源文件</a></p></main><script src="'+prefix+'katex.min.js"></script><script src="'+prefix+'contrib/auto-render.min.js"></script>'
      '<script>renderMathInElement(document.body,{delimiters:[{left:"\\\\[",right:"\\\\]",display:true},{left:"\\\\(",right:"\\\\)",display:false}],throwOnError:false});</script></body></html>')
def notebook_body(source):
    nb=nbformat.read(source,as_version=4);nbformat.validate(nb);blocks=[]
    for index,cell in enumerate(nb.cells,1):
        blocks.append('<section id="cell-'+str(index)+'">')
        if cell.cell_type=='markdown':blocks.append(md(cell.source))
        elif cell.cell_type=='code':
            count=cell.execution_count
            if count is None:raise RuntimeError(f'{source.name}: unexecuted code cell {index}')
            blocks.append('<div class="code-input"><div class="cell-label">In ['+str(count)+']</div>'+highlight(cell.source,PythonLexer(),HtmlFormatter())+'</div>')
            for o in cell.get('outputs',[]):
                if o.output_type=='error':raise RuntimeError('Notebook contains error output')
                if o.output_type=='stream':body='<pre>'+html.escape(o.text)+'</pre>'
                else:
                    data=o.get('data',{})
                    if 'image/png' in data:body='<img alt="Executed '+source.stem+' figure, cell '+str(index)+'" src="data:image/png;base64,'+data['image/png']+'">'
                    elif 'text/html' in data:body=data['text/html']
                    elif 'text/markdown' in data:body=md(data['text/markdown'])
                    elif 'text/plain' in data:body='<pre>'+html.escape(data['text/plain'])+'</pre>'
                    else:body=''
                blocks.append('<div class="output">'+body+'</div>')
        blocks.append('</section>')
    return '\n'.join(blocks)
def build():
    for source,record in DOCUMENTS.items():
        if not source.is_file():raise FileNotFoundError(source)
        if source.suffix=='.ipynb':
            nb=nbformat.read(source,as_version=4);opening=nb.cells[0].source
            body=notebook_body(source)
        else:opening=source.read_text();body=md(opening)
        title=next((s.lstrip('# ').strip() for s in opening.splitlines() if s.startswith('# ')),source.stem)
        PREVIEWS[source].write_text(wrap(title,body,source))
    print(f'Generated {len(PREVIEWS)} explicitly registered local HTML previews ({sum(bool(r.get("major")) for r in RECORDS)} major documents); no execution or publication.')
if __name__=='__main__':build()
