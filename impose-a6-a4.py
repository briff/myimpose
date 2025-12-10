import pypdf
import reportlab
from reportlab.pdfgen import canvas

def impose_pdf_a6_a4(input_pdf_path, output_pdf_path):

    # A4 size in points (portrait)
    a4_width, a4_height = 595, 842
    # A6 size in points
    a6_width, a6_height = 298, 419

    with open(input_pdf_path, 'rb') as input_file, open(output_pdf_path, 'wb') as output_file:
        reader = pypdf.PdfReader(input_file)
        writer = pypdf.PdfWriter()

        # Check if the input PDF has exactly 8 pages
        if len(reader.pages) % 4 != 0:
            raise ValueError("Input PDF must n times 4 pages")

        # Generate booklet page order (imposition)
        n = len(reader.pages)
        booklet_indexes = []
        for i in range(n // 4):
            booklet_indexes.extend([
                n - 1 - i * 2,      # last, second-last, ...
                i * 2,              # first, second, ...
                i * 2 + 1,          # second, third, ...
                n - 2 - i * 2       # second-last-1, third-last-1, ...
            ])

        # Create a new A3 page for each pair of B5 pages
        # Use the booklet_indexes to select pages in imposed order, two at a time
        for i in range(0, len(booklet_indexes), 2):
            page1 = reader.pages[booklet_indexes[i]]
            page2 = reader.pages[booklet_indexes[i + 1]]

            # Create an A4 page and adjust its dimensions
            a4_page = pypdf.PageObject.create_blank_page(width=a4_width, height=a4_height)  # A4 dimensions in points
            page1.cropbox=pypdf.generic.RectangleObject([0,0,a4_width,a4_height])
            a4_page.merge_page(page1, False)
            page1.add_transformation(pypdf.Transformation().translate( 0, a4_height/2))
            a4_page.merge_page(page1, False)
            page2.add_transformation(pypdf.Transformation().translate( a4_width/2, 0))
            page2.cropbox=pypdf.generic.RectangleObject([0,0,a4_width,a4_height])
            a4_page.merge_page(page2, False)
            page2.add_transformation(pypdf.Transformation().translate( 0, a4_height/2))
            a4_page.merge_page(page2, False)
            writer.add_page(a4_page)
        writer.write(output_file)


# Example usage
impose_pdf_a6_a4("advent-2025-fuzet-oldalak.pdf ", "advent-2025-fuzet-kilott-a4.pdf")
