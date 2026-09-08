from fpdf import FPDF

with open('week2_day1_writeup.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# Replace unicode chars with ASCII equivalents
replacements = {
    '\u2014': '--',
    '\u2013': '-',
    '\u2018': "'",
    '\u2019': "'",
    '\u201c': '"',
    '\u201d': '"',
    '\u2026': '...',
    '\u2713': '[OK]',
    '\u26a0': '[WARN]',
    '\u23f1': '[TIME]',
    '\u2705': '[DONE]',
    '\u27a1': '->',
    '\u2192': '->',
    '\u2265': '>=',
    '\u2264': '<=',
    '\u00b0': 'deg ',
    '\u2714': '[OK]',
}
for k, v in replacements.items():
    md_content = md_content.replace(k, v)

class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 10, 'Week 2 Day 1: Agent Foundations - Write-up', new_x='LMARGIN', new_y='NEXT', align='C')
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

pdf = PDF()
pdf.alias_nb_pages()
pdf.add_page()
pdf.set_font('Helvetica', '', 10)
pdf.set_auto_page_break(auto=True, margin=15)

lines = md_content.split('\n')
in_code = False
for line in lines:
    if line.startswith('```'):
        in_code = not in_code
        if in_code:
            pdf.set_font('Courier', '', 7)
        else:
            pdf.set_font('Helvetica', '', 10)
        continue
    if in_code:
        pdf.set_font('Courier', '', 7)
        # Truncate long lines
        if len(line) > 90:
            line = line[:90] + '...'
        try:
            pdf.multi_cell(0, 4, line)
        except:
            pass
        continue
    if line.startswith('# '):
        pdf.set_font('Helvetica', 'B', 14)
        pdf.multi_cell(0, 8, line[2:])
        pdf.ln(3)
    elif line.startswith('## '):
        pdf.set_font('Helvetica', 'B', 12)
        pdf.multi_cell(0, 7, line[3:])
        pdf.ln(2)
    elif line.startswith('### '):
        pdf.set_font('Helvetica', 'B', 11)
        pdf.multi_cell(0, 6, line[4:])
        pdf.ln(1)
    elif line.strip() == '':
        pdf.ln(2)
    else:
        pdf.set_font('Helvetica', '', 10)
        try:
            pdf.multi_cell(0, 5, line)
        except:
            pass
        pdf.ln(1)

pdf.output('week2_day1_writeup.pdf')
print('PDF created successfully')