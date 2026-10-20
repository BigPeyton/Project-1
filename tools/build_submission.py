"""Build review PDFs from explicit Markdown sources; no financial recalculation.

Authoring dependencies only: reportlab, pypdf. The valuation app remains stdlib-only.
"""
import hashlib
import json
import re
from html import escape
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, Preformatted, CondPageBreak)
from pypdf import PdfReader, PdfWriter

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'deliverables'
TMP=ROOT/'tmp/pdfs'
ORIGINAL_HASH='50749a9b74b77cac f0176b1fb9e6e59f596117bc906f5b499cb72e0ef4c9683d'.replace(' ','')


def fonts():
    folder=Path('C:/Windows/Fonts')
    for name,file in [('Body','arial.ttf'),('Bold','arialbd.ttf'),('Italic','ariali.ttf'),('BoldItalic','arialbi.ttf'),('Code','consola.ttf')]:
        pdfmetrics.registerFont(TTFont(name,str(folder/file)))
    pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Italic',boldItalic='BoldItalic')


def styles(memo=False):
    s=getSampleStyleSheet(); size=10
    s.add(ParagraphStyle(name='Text',fontName='Body',fontSize=size,leading=size*1.36,spaceAfter=7,allowWidows=0,allowOrphans=0,textColor=colors.HexColor('#213547')))
    s.add(ParagraphStyle(name='TitleDoc',parent=s['Text'],fontName='Bold',fontSize=21,leading=25,spaceAfter=14,keepWithNext=True))
    s.add(ParagraphStyle(name='Section',parent=s['Text'],fontName='Bold',fontSize=12,leading=15,spaceBefore=10,spaceAfter=6,keepWithNext=True,textColor=colors.HexColor('#105575')))
    s.add(ParagraphStyle(name='Subsection',parent=s['Text'],fontName='Bold',fontSize=10.3,leading=14,spaceBefore=7,keepWithNext=True))
    s.add(ParagraphStyle(name='Cell',parent=s['Text'],fontSize=8.5,leading=11.5,spaceAfter=0))
    s.add(ParagraphStyle(name='CellHead',parent=s['Cell'],fontName='Bold',textColor=colors.white))
    s.add(ParagraphStyle(name='CodeBlock',fontName='Code',fontSize=7.8,leading=10.5,spaceAfter=8))
    s.add(ParagraphStyle(name='BulletText',parent=s['Text'],leftIndent=12,firstLineIndent=-9))
    return s


def inline(text):
    text=escape(text)
    def link(m):
        label,url=m.group(1),m.group(2)
        if url.startswith('https://'):
            return f'<link href="{url}" color="#075b87"><u>{label}</u></link>'
        # Repository-relative links may not survive a standalone upload: expose their location.
        return label+f' <font size="7.5">[repo: {url}]</font>'
    text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,text)
    text=re.sub(r'`([^`]+)`',r'<font name="Code">\1</font>',text)
    text=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',text)
    text=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<i>\1</i>',text)
    return text


def markdown(source,memo=False):
    s=styles(memo); lines=source.splitlines(); flow=[]; i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line: i+=1; continue
        if line=='<!-- pagebreak -->': flow.append(PageBreak()); i+=1; continue
        if line.startswith('```'):
            i+=1; block=[]
            while i<len(lines) and not lines[i].startswith('```'): block.append(lines[i]); i+=1
            flow.append(Preformatted('\n'.join(block),s['CodeBlock'],maxLineLength=100)); i+=1; continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                values=[v.strip() for v in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?',v) for v in values): rows.append(values)
                i+=1
            n=len(rows[0]); widths={2:[145,371],3:[100,72,344],4:[112,133,133,138]}.get(n,[516/n]*n)
            data=[[Paragraph(inline(cell),s['CellHead' if j==0 else 'Cell']) for cell in row] for j,row in enumerate(rows)]
            t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
            t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#174d66')),('VALIGN',(0,0),(-1,-1),'TOP'),
                ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#f0f5f8'),colors.white]),
                ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
                ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
                ('LINEBELOW',(0,0),(-1,0),.5,colors.HexColor('#174d66'))]))
            # Keep a heading with the start of a table, not the entire multi-page table.
            # A normal keepWithNext can otherwise create a nearly empty preceding page.
            if flow and isinstance(flow[-1],Paragraph) and flow[-1].style.name in ('Section','Subsection'):
                flow[-1].keepWithNext=False
                flow.insert(len(flow)-1,CondPageBreak(135))
            flow.extend([t,Spacer(1,10)]); continue
        if line.startswith('#'):
            count=len(line)-len(line.lstrip('#')); style='TitleDoc' if count==1 else 'Section' if count==2 else 'Subsection'
            flow.append(Paragraph(inline(line[count:].strip()),s[style])); i+=1; continue
        if line.startswith('- '):
            flow.append(Paragraph('- '+inline(line[2:]),s['BulletText'])); i+=1; continue
        if re.match(r'^\d+\. ',line):
            flow.append(Paragraph(inline(line),s['BulletText'])); i+=1; continue
        if line.startswith('> '): line=line[2:]
        paragraph=[line]; i+=1
        while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|','```','- ','> ','<!--')) and not re.match(r'^\d+\. ',lines[i]):
            paragraph.append(lines[i].strip()); i+=1
        flow.append(Paragraph(inline(' '.join(paragraph)),s['Text']))
    return flow


def build(source,name,label,memo=False):
    dest=OUT/name
    def decorate(canvas,doc):
        canvas.saveState(); canvas.setStrokeColor(colors.HexColor('#c9d8e2')); canvas.line(48,752,564,752)
        canvas.setFont('Body',8); canvas.setFillColor(colors.HexColor('#526b7a'))
        canvas.drawString(48,762,'FIN 439 | PEYTON DOW | '+label.upper())
        canvas.drawString(48,29,'Review copy | October 19, 2026 | Evidence gaps disclosed')
        canvas.drawRightString(564,29,str(doc.page)); canvas.restoreState()
    doc=SimpleDocTemplate(str(dest),pagesize=(612,792),leftMargin=48,rightMargin=48,topMargin=53,bottomMargin=47,
                          title=label,author='Peyton Dow; AI-assisted preparation',subject='FIN 439 Project 1 - review copy')
    doc.build(markdown(source,memo),onFirstPage=decorate,onLaterPages=decorate)
    return dest


def main():
    OUT.mkdir(parents=True,exist_ok=True); TMP.mkdir(parents=True,exist_ok=True); fonts()
    original=(ROOT/'archive/Project-1-Edition-A-RKLB.md').read_bytes()
    if hashlib.sha256(original).hexdigest()!=ORIGINAL_HASH: raise ValueError('Original Edition A hash changed.')
    original_text=original.decode('utf-8')
    evolution=original_text+'\n\n<!-- pagebreak -->\n\n'+(ROOT/'docs/edition-a-addendum.md').read_text(encoding='utf-8')+'\n\n<!-- pagebreak -->\n\n'+(ROOT/'docs/edition-b.md').read_text(encoding='utf-8')
    (ROOT/'docs/research-evolution.md').write_text(evolution,encoding='utf-8')
    memo=(ROOT/'docs/decision-memo.md').read_text(encoding='utf-8')
    validation=(ROOT/'docs/validation-and-ai-use.md').read_text(encoding='utf-8')
    files=[build(memo,'Decision-Memo.pdf','Decision memo',True),
           build(evolution,'Research-Evolution.pdf','Research evolution'),
           build(validation,'Validation-and-AI-Use.pdf','Validation and AI use')]
    # Preserve the byte-identical original as an accessible PDF attachment as well as rendered text.
    evo=files[1]; writer=PdfWriter(); writer.clone_document_from_reader(PdfReader(evo))
    writer.add_attachment('Project-1-Edition-A-RKLB.md',original)
    writer.add_metadata({'/Title':'Research evolution: unchanged Edition A, dated addendum and Edition B','/Author':'Peyton Dow; AI-assisted preparation'})
    temp=TMP/'research-with-attachment.pdf'; writer.write(temp); evo.write_bytes(temp.read_bytes())
    pages={p.name:len(PdfReader(p).pages) for p in files}
    if pages['Decision-Memo.pdf']!=2: raise ValueError(f'Memo must be exactly two pages; got {pages}')
    attachment=PdfReader(evo).attachments['Project-1-Edition-A-RKLB.md'][0]
    if hashlib.sha256(attachment).hexdigest()!=ORIGINAL_HASH: raise ValueError('Embedded Edition A differs.')
    for p,dest in zip(files,['decision-memo.pdf','research-evolution.pdf','validation-and-ai-use.pdf']):
        (ROOT/'docs'/dest).write_bytes(p.read_bytes())
    manifest={p.name:dict(pages=pages[p.name],sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files}
    manifest['source_markdown_sha256']={name:hashlib.sha256((ROOT/'docs'/name).read_bytes()).hexdigest() for name in ['decision-memo.md','research-evolution.md','validation-and-ai-use.md']}
    manifest['original_edition_a_sha256']=ORIGINAL_HASH
    manifest['status']='Review PDFs; student locked exercise and recorded cold run absent; no submission receipt.'
    (OUT/'document-build.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(manifest,indent=2))


if __name__=='__main__': main()
