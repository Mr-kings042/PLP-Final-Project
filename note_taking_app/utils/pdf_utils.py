from fpdf import FPDF

def generate_pdf(title, content):
    file_path = f"{title}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=title, ln=True, align="C")
    pdf.ln(10)
    pdf.multi_cell(0, 10, content)
    pdf.output(file_path)
    return file_path
