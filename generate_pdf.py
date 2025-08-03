import fitz  # PyMuPDF

def create_final_pdf(name, spec, sum_assured, pi1, pi2, pi3, pp1, pp2, pp3):
    template_path = 'static/CoverPrime Bronchure (2).pdf'
    output_path = f'temp/Dr.{name}.pdf'

    doc = fitz.open(template_path)
    if len(doc) < 2:
        raise ValueError("Template must have at least 2 pages.")

    page = doc[1]

    font_size = 12
    fontname = "helv"
    color_black = (0, 0, 0)
    color_red = (1, 0, 0)
    color_dark_green = (0, 0.39, 0)

    def insert_bold_text(pos, text, size=font_size, color=color_black):
        x, y = pos
        for dx, dy in [(0,0), (0.3,0), (0,0.3)]:
            page.insert_text((x+dx, y+dy), text, fontsize=size, fontname=fontname, fill=color)

    def insert_price_and_savings(x, y, price, savings):
        insert_bold_text((x, y), f"₹ {price}/-")
        savings_value = float(savings)
        color = color_red if savings_value == 0 else color_dark_green
        insert_bold_text((x, y + 15), f"(Save ₹{savings}/-)", color=color)

    # 🔴 Header: Doctor Info
    insert_bold_text((65, 390), f"Dr. {name}")
    insert_bold_text((190, 390), "PROTECT PLUS")
    insert_bold_text((330, 390), spec)
    insert_bold_text((475, 390), sum_assured)

    # 🟢 PI row — amount + savings
    insert_price_and_savings(215, 1450, pi1[0], pi1[1])
    insert_price_and_savings(335, 1450, pi2[0], pi2[1])
    insert_price_and_savings(465, 1450, pi3[0], pi3[1])

    # 🟠 Protect Plus row — amount + savings
    insert_price_and_savings(215, 1515, pp1[0], pp1[1])
    insert_price_and_savings(335, 1515, pp2[0], pp2[1])
    insert_price_and_savings(465, 1515, pp3[0], pp3[1])

    doc.save(output_path)
    return output_path
