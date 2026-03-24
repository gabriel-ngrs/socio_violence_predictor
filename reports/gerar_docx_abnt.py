"""
Gera relatório em formato DOCX seguindo as normas ABNT NBR 14724:2011.

Formatação ABNT:
- Fonte: Times New Roman 12pt (corpo), 14pt (capa), 10pt (citações longas, notas)
- Margens: superior 3cm, esquerda 3cm, inferior 2cm, direita 2cm
- Espaçamento entre linhas: 1,5 (corpo); simples (resumo, citações longas, referências)
- Parágrafo: recuo de 1,25cm na primeira linha
- Títulos numerados em caixa alta (nível 1) ou normal (nível 2+)
- Capa sem numeração; numeração começa a contar da capa mas aparece a partir da introdução
- Referências em ordem alfabética (ABNT NBR 6023:2018), sem numeração

Executar a partir da raiz do projeto:
    python3 reports/gerar_docx_abnt.py
"""

import re
from pathlib import Path
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

RELATORIO_MD = Path(__file__).parent / "relatorio.md"
OUTPUT_DOCX  = Path(__file__).parent / "relatorio_abnt.docx"


# ---------------------------------------------------------------------------
# Utilitários de formatação
# ---------------------------------------------------------------------------

def set_paragraph_spacing(para, before_pt=0, after_pt=0, line_rule=None, line_val=None):
    pf = para.paragraph_format
    pf.space_before = Pt(before_pt)
    pf.space_after  = Pt(after_pt)
    if line_rule and line_val:
        pf.line_spacing_rule = line_rule
        pf.line_spacing = line_val


def set_font(run, name="Times New Roman", size_pt=12, bold=False, italic=False):
    run.font.name = name
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.italic = italic


def add_run_formatted(para, text, bold=False, italic=False, size=12, name="Times New Roman"):
    run = para.add_run(text)
    set_font(run, name=name, size_pt=size, bold=bold, italic=italic)
    return run


def set_margins(doc, top_cm=3, left_cm=3, bottom_cm=2, right_cm=2):
    for section in doc.sections:
        section.top_margin    = Cm(top_cm)
        section.left_margin   = Cm(left_cm)
        section.bottom_margin = Cm(bottom_cm)
        section.right_margin  = Cm(right_cm)


def add_page_break(doc):
    para = doc.add_paragraph()
    run = para.add_run()
    br = OxmlElement('w:br')
    br.set(qn('w:type'), 'page')
    run._r.append(br)
    return para


def apply_body_paragraph_format(para, first_line_indent=True):
    """Formato padrão ABNT para parágrafos de corpo."""
    pf = para.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after  = Pt(0)
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    if first_line_indent:
        pf.first_line_indent = Cm(1.25)
    else:
        pf.first_line_indent = Cm(0)
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY


def apply_table_style(table, doc):
    """Aplica estilo de tabela com bordas simples."""
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement

    tbl = table._tbl
    tblPr = tbl.tblPr if tbl.tblPr is not None else OxmlElement('w:tblPr')

    tblBorders = OxmlElement('w:tblBorders')
    for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), '4')
        border.set(qn('w:space'), '0')
        border.set(qn('w:color'), '000000')
        tblBorders.append(border)
    tblPr.append(tblBorders)

    # Largura da tabela: 100%
    tblW = OxmlElement('w:tblW')
    tblW.set(qn('w:w'), '5000')
    tblW.set(qn('w:type'), 'pct')
    tblPr.append(tblW)


# ---------------------------------------------------------------------------
# Parser do Markdown
# ---------------------------------------------------------------------------

def parse_inline(text):
    """Converte markdown inline (**negrito**, *itálico*, `código`) em lista de tokens."""
    tokens = []
    pattern = re.compile(r'(\*\*(.+?)\*\*|\*(.+?)\*|`(.+?)`)')
    last = 0
    for m in pattern.finditer(text):
        if m.start() > last:
            tokens.append(('normal', text[last:m.start()]))
        full = m.group(0)
        if full.startswith('**'):
            tokens.append(('bold', m.group(2)))
        elif full.startswith('*'):
            tokens.append(('italic', m.group(3)))
        elif full.startswith('`'):
            tokens.append(('code', m.group(4)))
        last = m.end()
    if last < len(text):
        tokens.append(('normal', text[last:]))
    return tokens


def add_inline_text(para, text, base_size=12):
    """Adiciona texto com formatação inline ao parágrafo."""
    tokens = parse_inline(text)
    for kind, content in tokens:
        run = para.add_run(content)
        run.font.name = "Times New Roman"
        run.font.size = Pt(base_size)
        if kind == 'bold':
            run.font.bold = True
        elif kind == 'italic':
            run.font.italic = True
        elif kind == 'code':
            run.font.name = "Courier New"
            run.font.size = Pt(10)


# ---------------------------------------------------------------------------
# Construção do documento
# ---------------------------------------------------------------------------

def build_capa(doc, lines):
    """Monta a capa do trabalho."""
    # Instituição
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p, before_pt=0, after_pt=6)
    add_run_formatted(p, "UNIVERSIDADE FEDERAL DA PARAÍBA", bold=True, size=12)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p, before_pt=0, after_pt=0)
    add_run_formatted(p, "Centro de Informática", size=12)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p, before_pt=0, after_pt=48)
    add_run_formatted(p, "Disciplina de Aprendizagem de Máquina", size=12)

    # Título
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p, before_pt=0, after_pt=48)
    add_run_formatted(p, "PREDIÇÃO DE VIOLÊNCIA MUNICIPAL COM INDICADORES SOCIOECONÔMICOS", bold=True, size=14)

    # Subtítulo / descrição
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p, before_pt=0, after_pt=72)
    add_run_formatted(p, "Relatório Final — Projeto da Disciplina", italic=True, size=12)

    # Autores (placeholder)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p, before_pt=0, after_pt=6)
    add_run_formatted(p, "Autores: (adicionar nomes do grupo)", size=12)

    # Professores
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p, before_pt=0, after_pt=6)
    add_run_formatted(p, "Professores: Bruno Jefferson de Sousa Pessoa e Gilberto Farias de Sousa Filho", size=12)

    # Local e data
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p, before_pt=72, after_pt=0)
    add_run_formatted(p, "João Pessoa — PB", size=12)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p, before_pt=0, after_pt=0)
    add_run_formatted(p, "Março de 2026", size=12)


def process_table(doc, lines, start_idx):
    """Processa uma tabela markdown a partir da linha start_idx."""
    table_lines = []
    i = start_idx
    while i < len(lines) and lines[i].strip().startswith('|'):
        table_lines.append(lines[i].strip())
        i += 1

    if len(table_lines) < 2:
        return i

    # Parse header
    header_cells = [c.strip() for c in table_lines[0].split('|') if c.strip()]
    # Skip separator line (index 1)
    data_rows = []
    for row_line in table_lines[2:]:
        cells = [c.strip() for c in row_line.split('|') if c.strip() != '']
        if cells:
            data_rows.append(cells)

    n_cols = len(header_cells)
    n_rows = 1 + len(data_rows)

    table = doc.add_table(rows=n_rows, cols=n_cols)
    apply_table_style(table, doc)

    # Header row
    hdr_row = table.rows[0]
    for j, cell_text in enumerate(header_cells):
        if j >= len(hdr_row.cells):
            break
        cell = hdr_row.cells[j]
        cell.text = ''
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_inline_text(p, cell_text, base_size=10)
        for run in p.runs:
            run.font.bold = True
        cell._tc.get_or_add_tcPr()

    # Data rows
    for r_idx, row_data in enumerate(data_rows):
        row = table.rows[r_idx + 1]
        for j in range(n_cols):
            if j >= len(row.cells):
                break
            cell = row.cells[j]
            cell.text = ''
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            cell_text = row_data[j] if j < len(row_data) else ''
            add_inline_text(p, cell_text, base_size=10)

    # Espaço após tabela
    sp = doc.add_paragraph()
    set_paragraph_spacing(sp, before_pt=6, after_pt=6)

    return i


def process_markdown(doc, md_text):
    """Converte o markdown para elementos do documento DOCX."""
    lines = md_text.split('\n')
    i = 0
    in_code_block = False
    code_lines = []
    skip_capa = True  # O bloco inicial (título + metadados) é tratado como capa

    while i < len(lines):
        line = lines[i]

        # Bloco de código
        if line.strip().startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_lines = []
            else:
                in_code_block = False
                # Adicionar bloco de código com recuo e fonte mono
                for cline in code_lines:
                    p = doc.add_paragraph()
                    apply_body_paragraph_format(p, first_line_indent=False)
                    p.paragraph_format.left_indent = Cm(3)
                    p.paragraph_format.right_indent = Cm(3)
                    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
                    run = p.add_run(cline if cline else ' ')
                    run.font.name = "Courier New"
                    run.font.size = Pt(10)
            i += 1
            continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        # Linha horizontal (---)
        if re.match(r'^-{3,}$', line.strip()):
            i += 1
            continue

        # Tabela
        if line.strip().startswith('|'):
            i = process_table(doc, lines, i)
            continue

        # Títulos
        h1 = re.match(r'^# (.+)$', line)
        h2 = re.match(r'^## (.+)$', line)
        h3 = re.match(r'^### (.+)$', line)
        h4 = re.match(r'^#### (.+)$', line)

        if h1:
            title_text = h1.group(1)
            if skip_capa:
                # Capa separada
                build_capa(doc, lines)
                add_page_break(doc)
                skip_capa = False
                i += 1
                # Pular linhas de metadados
                while i < len(lines) and lines[i].strip().startswith('**'):
                    i += 1
                continue
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_paragraph_spacing(p, before_pt=24, after_pt=12)
            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
            run = p.add_run(title_text.upper())
            run.font.name = "Times New Roman"
            run.font.size = Pt(12)
            run.font.bold = True
            i += 1
            continue

        if h2:
            title_text = h2.group(1)
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            set_paragraph_spacing(p, before_pt=18, after_pt=6)
            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
            run = p.add_run(title_text.upper())
            run.font.name = "Times New Roman"
            run.font.size = Pt(12)
            run.font.bold = True
            i += 1
            continue

        if h3:
            title_text = h3.group(1)
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            set_paragraph_spacing(p, before_pt=12, after_pt=6)
            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
            run = p.add_run(title_text)
            run.font.name = "Times New Roman"
            run.font.size = Pt(12)
            run.font.bold = True
            i += 1
            continue

        if h4:
            title_text = h4.group(1)
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            set_paragraph_spacing(p, before_pt=6, after_pt=3)
            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
            run = p.add_run(title_text)
            run.font.name = "Times New Roman"
            run.font.size = Pt(12)
            run.font.italic = True
            i += 1
            continue

        # Linha vazia
        if not line.strip():
            i += 1
            continue

        # Bloco de citação (> ...)
        if line.strip().startswith('>'):
            text = line.strip().lstrip('> ').strip()
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.left_indent   = Cm(4)
            p.paragraph_format.right_indent  = Cm(0)
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
            p.paragraph_format.space_before  = Pt(6)
            p.paragraph_format.space_after   = Pt(6)
            add_inline_text(p, text, base_size=10)
            i += 1
            continue

        # Lista não ordenada (- item ou * item)
        if re.match(r'^[\-\*] ', line.strip()):
            text = re.sub(r'^[\-\*] ', '', line.strip())
            p = doc.add_paragraph()
            apply_body_paragraph_format(p, first_line_indent=False)
            p.paragraph_format.left_indent = Cm(1.25)
            p.paragraph_format.first_line_indent = Cm(-0.5)
            run = p.add_run('• ')
            run.font.name = "Times New Roman"
            run.font.size = Pt(12)
            add_inline_text(p, text, base_size=12)
            i += 1
            continue

        # Lista numerada (1. item)
        num_match = re.match(r'^(\d+)\. (.+)$', line.strip())
        if num_match:
            num   = num_match.group(1)
            text  = num_match.group(2)
            p = doc.add_paragraph()
            apply_body_paragraph_format(p, first_line_indent=False)
            p.paragraph_format.left_indent = Cm(1.25)
            p.paragraph_format.first_line_indent = Cm(-0.5)
            add_inline_text(p, f"{num}. {text}", base_size=12)
            i += 1
            continue

        # Parágrafo normal
        p = doc.add_paragraph()
        apply_body_paragraph_format(p, first_line_indent=True)
        add_inline_text(p, line.strip(), base_size=12)
        i += 1

    return doc


def add_page_numbers(doc):
    """Adiciona numeração de página no rodapé (canto direito)."""
    for section in doc.sections:
        footer = section.footer
        footer_para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        footer_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        footer_para.clear()

        run = footer_para.add_run()
        run.font.name = "Times New Roman"
        run.font.size = Pt(10)

        # Campo PAGE
        fldChar1 = OxmlElement('w:fldChar')
        fldChar1.set(qn('w:fldCharType'), 'begin')
        instrText = OxmlElement('w:instrText')
        instrText.text = 'PAGE'
        fldChar2 = OxmlElement('w:fldChar')
        fldChar2.set(qn('w:fldCharType'), 'end')

        run._r.append(fldChar1)
        run._r.append(instrText)
        run._r.append(fldChar2)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Gerando DOCX ABNT...")

    md_text = RELATORIO_MD.read_text(encoding="utf-8")

    doc = Document()
    set_margins(doc, top_cm=3, left_cm=3, bottom_cm=2, right_cm=2)

    # Estilo padrão do documento
    style = doc.styles['Normal']
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)
    style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE

    # Processar markdown
    process_markdown(doc, md_text)

    # Numeração de páginas
    add_page_numbers(doc)

    doc.save(OUTPUT_DOCX)
    print(f"✓ Salvo: {OUTPUT_DOCX}")
    print(f"  Parágrafos: {len(doc.paragraphs)}")
    print(f"  Tabelas:    {len(doc.tables)}")


if __name__ == "__main__":
    main()
