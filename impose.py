import pypdf
import reportlab
from reportlab.pdfgen import canvas

def impose_pdf_on_a3(input_pdf_path, output_pdf_path):
    with open(input_pdf_path, 'rb') as input_file, open(output_pdf_path, 'wb') as output_file:
        c = canvas.Canvas("cropmarks.pdf", pagesize=(1191, 842))
        x0 = (1191-998)/2
        y0 = (842-709)/2
        x1 = x0 + 998
        y1 = y0
        x2 = x1
        y2 = y1 + 709
        x3 = x0
        y3 = y2
        c.line(x0, y0, x0, y0 + 25)
        c.line(x0, y0, x0+25, y0)
        c.line(x1, y1, x1-25, y1)
        c.line(x1, y1, x1, y1 + 25)
        c.line(x2, y2, x2-25, y2)
        c.line(x2, y2, x2, y2 - 25)
        c.line(x3, y3, x3 + 25, y3)
        c.line(x3, y3, x3, y3 - 25)
        
        c.showPage()
        c.save()

        reader = pypdf.PdfReader(input_file)
        cropReader = pypdf.PdfReader("cropmarks.pdf")
        writer = pypdf.PdfWriter()

        # Check if the input PDF has exactly 8 pages
        if len(reader.pages) % 4 != 0:
            raise ValueError("Input PDF must n times 4 pages")

        # Create a new A3 page for each pair of B5 pages
        for i in range(0, 8, 2):
            page1 = reader.pages[i]
            page2 = reader.pages[i + 1]

            # Create an A3 page and adjust its dimensions
            a3_page = pypdf.PageObject.create_blank_page(width=1191, height=842)  # A3 dimensions in points
            page1.add_transformation(pypdf.Transformation().translate( x0, y0))
            page1.cropbox=pypdf.generic.RectangleObject([0,0,1191,842])
            a3_page.merge_page(page1, False)
            page2.add_transformation(pypdf.Transformation().translate( x0 + 499, y0))
            page2.cropbox=pypdf.generic.RectangleObject([0,0,1191,842])
            a3_page.merge_page(page2)
            if i % 4 == 2: a3_page.merge_page(cropReader.pages[0])
            writer.add_page(a3_page)
        writer.write(output_file)


# Example usage
impose_pdf_on_a3("2025-advent.pdf ", "2025-advent-kilott-a3.pdf")
