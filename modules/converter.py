#!/usr/bin/env python3
import os
import markdown
import re


class Converter:
    def __init__(self):
        pass

    def convert_to_pdf(self, md_path, width=800):
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        html_body = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'toc'])
        
        html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {
    font-family: "Microsoft YaHei", "SimHei", "SimSun", sans-serif;
    color: #333333;
    font-size: 14px;
    line-height: 1.6;
}
h1 { color: #1a1a2e; border-bottom: 3px solid #e94560; padding-bottom: 10px; font-size: 24px; }
h2 { color: #16213e; border-bottom: 2px solid #0f3460; padding-bottom: 8px; margin-top: 30px; font-size: 20px; }
h3 { color: #0f3460; margin-top: 20px; font-size: 17px; }
table { border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 13px; }
th { background-color: #1a1a2e; color: white; padding: 8px 6px; text-align: left; font-weight: bold; }
td { padding: 6px; border: 1px solid #ddd; }
tr:nth-child(even) { background-color: #f8f9fa; }
strong { color: #e94560; }
blockquote { border-left: 4px solid #e94560; padding-left: 16px; color: #666; margin: 12px 0; }
hr { border: none; border-top: 2px solid #eee; margin: 20px 0; }
</style>
</head>
<body>
""" + html_body + """
</body>
</html>"""

        # Save HTML
        html_path = md_path.replace('.md', '.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print('HTML saved to', html_path)

        # Generate PDF from HTML
        pdf_path = md_path.replace('.md', '.pdf')
        try:
            self._generate_pdf_simple(md_content, pdf_path)
            print('PDF saved to', pdf_path)
        except Exception as e:
            print('PDF generation failed:', e)
            pdf_path = None

        return pdf_path

    def _generate_pdf_simple(self, md_content, pdf_path):
        """Generate PDF using reportlab with proper Chinese font support"""
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib.units import cm, mm
        from reportlab.lib import colors

        # Register Chinese fonts
        font_paths = [
            (r'C:\Windows\Fonts\msyh.ttc', 'MSYH'),
            (r'C:\Windows\Fonts\simhei.ttf', 'SimHei'),
            (r'C:\Windows\Fonts\simsun.ttc', 'SimSun'),
        ]
        
        font_name = 'Helvetica'
        for fp, fname in font_paths:
            try:
                pdfmetrics.registerFont(TTFont(fname, fp))
                font_name = fname
                break
            except:
                continue

        # Create styles
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name='CN',
            fontName=font_name,
            fontSize=9,
            leading=12,
            spaceAfter=4
        ))
        styles.add(ParagraphStyle(
            name='CNTitle',
            fontName=font_name,
            fontSize=16,
            leading=20,
            spaceAfter=10,
            alignment=1
        ))
        styles.add(ParagraphStyle(
            name='CNH1',
            fontName=font_name,
            fontSize=13,
            leading=16,
            spaceAfter=6,
            spaceBefore=10
        ))
        styles.add(ParagraphStyle(
            name='CNH2',
            fontName=font_name,
            fontSize=11,
            leading=14,
            spaceAfter=5,
            spaceBefore=8
        ))

        doc = SimpleDocTemplate(pdf_path, pagesize=A4, 
                               leftMargin=1.5*cm, rightMargin=1.5*cm,
                               topMargin=1.5*cm, bottomMargin=1.5*cm)
        
        story = []
        lines = md_content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                story.append(Spacer(1, 0.2*cm))
                continue
            
            # Clean markdown formatting
            clean_line = re.sub(r'\*\*(.*?)\*\*', r'\1', line)
            clean_line = re.sub(r'\*(.*?)\*', r'\1', clean_line)
            clean_line = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', clean_line)
            # Escape XML special chars
            clean_line = clean_line.replace('&', '&amp;')
            clean_line = clean_line.replace('<', '&lt;')
            clean_line = clean_line.replace('>', '&gt;')
            
            if line.startswith('# '):
                story.append(Paragraph(clean_line[2:], styles['CNTitle']))
            elif line.startswith('## '):
                story.append(Paragraph(clean_line[3:], styles['CNH1']))
            elif line.startswith('### '):
                story.append(Paragraph(clean_line[4:], styles['CNH2']))
            elif line.startswith('|') and '|' in line[1:]:
                # Table row - render as text
                if set(line.replace('|','').replace('-','').replace(' ','')) == set():
                    continue
                cells = [c.strip() for c in line.split('|')[1:-1]]
                if cells:
                    table_text = ' | '.join(cells)
                    story.append(Paragraph(table_text, styles['CN']))
            elif line.startswith('- '):
                story.append(Paragraph('  * ' + clean_line[2:], styles['CN']))
            elif line.startswith('> '):
                story.append(Paragraph(clean_line[2:], styles['CN']))
            elif line.startswith('---'):
                story.append(Spacer(1, 0.3*cm))
            else:
                story.append(Paragraph(clean_line, styles['CN']))
        
        doc.build(story)
