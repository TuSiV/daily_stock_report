#!/usr/bin/env python3
import os
import markdown
import re

class Converter:
    def __init__(self):
        pass

    def convert_to_png_pdf(self, md_path, width=800):
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        html_body = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'toc'])
        html_parts = []
        html_parts.append('<!DOCTYPE html><html><head><meta charset="utf-8"><style>')
        html_parts.append('@page { size: ' + str(width) + 'px auto; margin: 0; }')
        html_parts.append('body { font-family: "Microsoft YaHei", "SimHei", "SimSun", sans-serif; max-width: ' + str(width) + 'px; margin: 0 auto; padding: 30px 20px; background: #fff; color: #333; font-size: 14px; line-height: 1.6; }')
        html_parts.append('h1 { color: #1a1a2e; border-bottom: 3px solid #e94560; padding-bottom: 10px; font-size: 24px; }')
        html_parts.append('h2 { color: #16213e; border-bottom: 2px solid #0f3460; padding-bottom: 8px; margin-top: 30px; font-size: 20px; }')
        html_parts.append('h3 { color: #0f3460; margin-top: 20px; font-size: 17px; }')
        html_parts.append('table { border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 13px; }')
        html_parts.append('th { background-color: #1a1a2e; color: white; padding: 8px 6px; text-align: left; font-weight: bold; }')
        html_parts.append('td { padding: 6px; border: 1px solid #ddd; }')
        html_parts.append('tr:nth-child(even) { background-color: #f8f9fa; }')
        html_parts.append('strong { color: #e94560; }')
        html_parts.append('blockquote { border-left: 4px solid #e94560; padding-left: 16px; color: #666; margin: 12px 0; }')
        html_parts.append('hr { border: none; border-top: 2px solid #eee; margin: 20px 0; }')
        html_parts.append('</style></head><body>')
        html_parts.append(html_body)
        html_parts.append('</body></html>')
        html = ''.join(html_parts)

        # Save HTML
        html_path = md_path.replace('.md', '.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print('HTML saved to', html_path)

        # Generate PDF using reportlab with Chinese font
        pdf_path = md_path.replace('.md', '.pdf')
        try:
            self._generate_pdf_reportlab(md_content, pdf_path)
            print('PDF saved to', pdf_path)
        except Exception as e:
            print('PDF generation failed:', e)
            pdf_path = None

        # Generate PNG
        png_path = md_path.replace('.md', '.png')
        try:
            from pdf2image import convert_from_path
            from PIL import Image
            if pdf_path and os.path.exists(pdf_path):
                images = convert_from_path(pdf_path, dpi=300)
                if len(images) == 1:
                    images[0].save(png_path, 'PNG')
                else:
                    total_height = sum(img.height for img in images)
                    max_width = max(img.width for img in images)
                    combined = Image.new('RGB', (max_width, total_height), 'white')
                    y_offset = 0
                    for img in images:
                        combined.paste(img, (0, y_offset))
                        y_offset += img.height
                    combined.save(png_path, 'PNG')
                print('PNG saved to', png_path)
            else:
                print('No PDF for PNG conversion')
                png_path = None
        except Exception as e:
            print('PNG generation failed:', e)
            png_path = None

        return png_path, pdf_path

    def _clean_text(self, text):
        """Clean markdown formatting for PDF"""
        # Remove markdown bold
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        # Remove markdown italic
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        # Remove markdown links
        text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
        # Escape HTML special chars for reportlab
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        return text

    def _generate_pdf_reportlab(self, md_content, pdf_path):
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib.units import cm

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

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name='CN',
            fontName=font_name,
            fontSize=10,
            leading=14,
            spaceAfter=6
        ))
        styles.add(ParagraphStyle(
            name='CNTitle',
            fontName=font_name,
            fontSize=18,
            leading=22,
            spaceAfter=12,
            alignment=1
        ))
        styles.add(ParagraphStyle(
            name='CNH1',
            fontName=font_name,
            fontSize=14,
            leading=18,
            spaceAfter=8,
            spaceBefore=12
        ))
        styles.add(ParagraphStyle(
            name='CNH2',
            fontName=font_name,
            fontSize=12,
            leading=16,
            spaceAfter=6,
            spaceBefore=10
        ))

        doc = SimpleDocTemplate(pdf_path, pagesize=A4, 
                               leftMargin=2*cm, rightMargin=2*cm,
                               topMargin=2*cm, bottomMargin=2*cm)
        
        story = []
        lines = md_content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                story.append(Spacer(1, 0.3*cm))
                continue
            
            cleaned = self._clean_text(line)
            
            if line.startswith('# '):
                story.append(Paragraph(cleaned[2:], styles['CNTitle']))
            elif line.startswith('## '):
                story.append(Paragraph(cleaned[3:], styles['CNH1']))
            elif line.startswith('### '):
                story.append(Paragraph(cleaned[4:], styles['CNH2']))
            elif line.startswith('|') and '|' in line[1:]:
                if set(line.replace('|','').replace('-','').replace(' ','')) == set():
                    continue
                cells = [c.strip() for c in line.split('|')[1:-1]]
                if cells:
                    cleaned_cells = [self._clean_text(c) for c in cells]
                    story.append(Paragraph(' | '.join(cleaned_cells), styles['CN']))
            elif line.startswith('- '):
                story.append(Paragraph('  * ' + cleaned[2:], styles['CN']))
            elif line.startswith('> '):
                story.append(Paragraph(cleaned[2:], styles['CN']))
            elif line.startswith('---'):
                story.append(Spacer(1, 0.5*cm))
            else:
                story.append(Paragraph(cleaned, styles['CN']))
        
        doc.build(story)
