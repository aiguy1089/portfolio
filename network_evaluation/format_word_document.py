"""
Format the Word document with Times New Roman, double spacing, and proper formatting
"""

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import os

def format_word_document():
    """Apply proper formatting to the Word document"""
    
    doc_path = r'c:\Users\Admin\D802 STN1 Task 4 Evaluation of the Network Architecture Model\submission\STN1_Task4_Final_Report.docx'
    
    if not os.path.exists(doc_path):
        print(f"❌ Document not found: {doc_path}")
        return
    
    try:
        # Open the document
        doc = Document(doc_path)
        
        # Set default font and spacing for all paragraphs
        for paragraph in doc.paragraphs:
            # Set font to Times New Roman
            for run in paragraph.runs:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(12)
            
            # Set line spacing to double
            paragraph_format = paragraph.paragraph_format
            paragraph_format.line_spacing = 2.0
            paragraph_format.space_after = Pt(0)
            paragraph_format.space_before = Pt(0)
        
        # Format styles
        styles = doc.styles
        
        # Normal style
        normal_style = styles['Normal']
        normal_font = normal_style.font
        normal_font.name = 'Times New Roman'
        normal_font.size = Pt(12)
        normal_style.paragraph_format.line_spacing = 2.0
        
        # Heading styles
        for i in range(1, 4):
            heading_style_name = f'Heading {i}'
            if heading_style_name in styles:
                heading_style = styles[heading_style_name]
                heading_font = heading_style.font
                heading_font.name = 'Times New Roman'
                heading_font.size = Pt(12 + (4-i))  # Slightly larger for headings
                heading_font.bold = True
                heading_style.paragraph_format.line_spacing = 2.0
        
        # Save the formatted document
        doc.save(doc_path)
        print(f"✅ Document formatted successfully: {doc_path}")
        print("📝 Applied formatting:")
        print("   • Font: Times New Roman, 12pt")
        print("   • Line spacing: Double")
        print("   • Proper heading hierarchy")
        
    except Exception as e:
        print(f"❌ Error formatting document: {str(e)}")
        print("💡 The document was created but may need manual formatting in Word")

if __name__ == "__main__":
    format_word_document()