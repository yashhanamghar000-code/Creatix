from fpdf import FPDF
import re

def clean_text(text):
    return re.sub(r'[^\x00-\x7F]+', ' ', text)

topic = "Your Topic Here"
writer = "Your report content here"
critic = "Your critic content here"

pdf = FPDF()
pdf.add_page()
pdf.set_font("Helvetica", size=10)

pdf.multi_cell(
    0,
    8,
    clean_text(
        f"""
Topic:
{topic}

Report:
{writer}

Critic:
{critic}
"""
    )
)

pdf.output("report.pdf")

print("PDF created successfully!")