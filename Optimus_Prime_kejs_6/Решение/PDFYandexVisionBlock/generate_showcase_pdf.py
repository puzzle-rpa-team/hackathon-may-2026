import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


BASE_DIR = Path(__file__).resolve().parent
DATA = json.loads((BASE_DIR / "showcase_expected_output.json").read_text(encoding="utf-8"))
OUTPUT_PATH = BASE_DIR / "showcase_input.pdf"


def u(value):
    return json.loads('"' + value + '"')


FONT_REGULAR = r"C:\Windows\Fonts\arial.ttf"
FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"


TITLE = u("\\u0423\\u041f\\u0414 / Universal Transfer Document")
SELLER_LABEL = u("\\u041f\\u043e\\u0441\\u0442\\u0430\\u0432\\u0449\\u0438\\u043a / Seller")
BUYER_LABEL = u("\\u041f\\u043e\\u043a\\u0443\\u043f\\u0430\\u0442\\u0435\\u043b\\u044c / Buyer")
CONTRACT_LABEL = u("\\u041e\\u0441\\u043d\\u043e\\u0432\\u0430\\u043d\\u0438\\u0435 / Contract")
PROJECT_LABEL = u("\\u041f\\u0440\\u043e\\u0435\\u043a\\u0442 / Project")
NOTE_LABEL = u("\\u041f\\u0440\\u0438\\u043c\\u0435\\u0447\\u0430\\u043d\\u0438\\u0435 / Note")
CONTINUED_LABEL = u("\\u041f\\u0440\\u043e\\u0434\\u043e\\u043b\\u0436\\u0435\\u043d\\u0438\\u0435 \\u0442\\u0430\\u0431\\u043b\\u0438\\u0446\\u044b / Continued table")
TABLE_HEADER = u("\\u041d\\u0430\\u0438\\u043c\\u0435\\u043d\\u043e\\u0432\\u0430\\u043d\\u0438\\u0435 / Description")
TOTALS_LABEL = u("\\u0418\\u0442\\u043e\\u0433\\u0438 / Totals")
TOTAL_PAYABLE_LABEL = u("\\u0412\\u0441\\u0435\\u0433\\u043e \\u043a \\u043e\\u043f\\u043b\\u0430\\u0442\\u0435 / Total payable")
CONTINUATION_PAGE_LABEL = u("\\u041f\\u0440\\u043e\\u0434\\u043e\\u043b\\u0436\\u0435\\u043d\\u0438\\u0435 \\u0441\\u043f\\u0435\\u0446\\u0438\\u0444\\u0438\\u043a\\u0430\\u0446\\u0438\\u0438 / Continuation of specification")


LINE_ITEMS = DATA["line_items"]
SELLER = DATA["counterparties"][0]
BUYER = DATA["counterparties"][1]
SUBTOTAL = sum(item["amount"] for item in LINE_ITEMS)
VAT = round(SUBTOTAL * 0.2, 2)
TOTAL = DATA["total_amount"]


def chunk_rows():
    return LINE_ITEMS[:3], LINE_ITEMS[3:]


def draw_page_header(pdf, page_no, subtitle):
    page_width, page_height = A4
    pdf.setFillColor(colors.HexColor("#F3F4F6"))
    pdf.rect(0, page_height - 70, page_width, 70, fill=1, stroke=0)
    pdf.setFillColor(colors.HexColor("#1F2937"))
    pdf.setFont("ArialCustomBold", 18)
    pdf.drawString(36, page_height - 34, TITLE)
    pdf.setFont("ArialCustom", 10)
    pdf.drawString(36, page_height - 52, subtitle)
    pdf.drawRightString(page_width - 36, page_height - 34, f"Page {page_no}")
    pdf.setFont("ArialCustomBold", 12)
    pdf.drawRightString(page_width - 36, page_height - 50, f"No: {DATA['document_number']}")
    pdf.setFont("ArialCustom", 11)
    pdf.drawRightString(page_width - 36, page_height - 64, f"Date: {DATA['document_date']}")


def draw_info_boxes(pdf):
    pdf.setStrokeColor(colors.HexColor("#D1D5DB"))
    pdf.roundRect(36, 610, 250, 110, 8, stroke=1, fill=0)
    pdf.roundRect(308, 610, 250, 110, 8, stroke=1, fill=0)

    pdf.setFillColor(colors.black)
    pdf.setFont("ArialCustomBold", 11)
    pdf.drawString(48, 700, SELLER_LABEL)
    pdf.drawString(320, 700, BUYER_LABEL)

    pdf.setFont("ArialCustom", 10)
    seller_lines = [
        SELLER["name"],
        f"{u('\\u0418\\u041d\\u041d')} {SELLER['inn']}   {u('\\u041a\\u041f\\u041f')} {SELLER['kpp']}",
        u("\\u041c\\u043e\\u0441\\u043a\\u0432\\u0430, \\u0443\\u043b. \\u041f\\u0440\\u043e\\u0435\\u043a\\u0442\\u043d\\u0430\\u044f, 12"),
        "sales@northwind.example",
    ]
    buyer_lines = [
        BUYER["name"],
        f"{u('\\u0418\\u041d\\u041d')} {BUYER['inn']}   {u('\\u041a\\u041f\\u041f')} {BUYER['kpp']}",
        u("\\u0421\\u0430\\u043d\\u043a\\u0442-\\u041f\\u0435\\u0442\\u0435\\u0440\\u0431\\u0443\\u0440\\u0433, \\u041d\\u0435\\u0432\\u0441\\u043a\\u0438\\u0439 48"),
        "finance@blueocean.example",
    ]

    y = 682
    for line in seller_lines:
        pdf.drawString(48, y, line)
        y -= 16

    y = 682
    for line in buyer_lines:
        pdf.drawString(320, y, line)
        y -= 16

    pdf.drawString(36, 590, f"{CONTRACT_LABEL}: C-77/2026 dated 15.05.2026")
    pdf.drawString(36, 574, f"{PROJECT_LABEL}: Puzzle RPA + Yandex Vision document automation showcase")
    pdf.drawString(36, 558, f"{NOTE_LABEL}: Mixed language, multi-page, table-heavy OCR demo")


def draw_table(pdf, start_y, rows):
    x = [36, 70, 350, 410, 480, 558]
    pdf.setFillColor(colors.HexColor("#F9FAFB"))
    pdf.rect(36, start_y - 22, 522, 22, fill=1, stroke=0)
    pdf.setStrokeColor(colors.HexColor("#9CA3AF"))
    pdf.rect(36, start_y - 22, 522, 22, fill=0, stroke=1)
    for vx in x[1:-1]:
        pdf.line(vx, start_y - 22, vx, start_y)

    pdf.setFillColor(colors.black)
    pdf.setFont("ArialCustomBold", 10)
    pdf.drawCentredString((x[0] + x[1]) / 2, start_y - 15, "#")
    pdf.drawString(x[1] + 4, start_y - 15, TABLE_HEADER)
    pdf.drawCentredString((x[2] + x[3]) / 2, start_y - 15, "Qty")
    pdf.drawCentredString((x[3] + x[4]) / 2, start_y - 15, "Price")
    pdf.drawCentredString((x[4] + x[5]) / 2, start_y - 15, "Amount")

    current_y = start_y - 22
    pdf.setFont("ArialCustom", 10)
    for idx, row in enumerate(rows, start=1):
        number = row.get("_row_no", str(idx))
        description = row["name"]
        quantity = f"{row['quantity']:.1f}".rstrip("0").rstrip(".")
        price = f"{row['price']:.2f}"
        amount = f"{row['amount']:.2f}"

        lines = [description]
        if len(description) > 34:
            split_at = description.rfind(" ", 0, 34)
            split_at = split_at if split_at > 12 else 34
            lines = [description[:split_at].rstrip(), description[split_at:].lstrip()]

        row_height = 34 if len(lines) == 1 else 46
        pdf.rect(36, current_y - row_height, 522, row_height, fill=0, stroke=1)
        for vx in x[1:-1]:
            pdf.line(vx, current_y - row_height, vx, current_y)

        pdf.drawCentredString((x[0] + x[1]) / 2, current_y - 18, number)
        text_y = current_y - 15
        for line in lines:
            pdf.drawString(x[1] + 4, text_y, line)
            text_y -= 14
        pdf.drawCentredString((x[2] + x[3]) / 2, current_y - 18, quantity)
        pdf.drawRightString(x[4] - 6, current_y - 18, price)
        pdf.drawRightString(x[5] - 6, current_y - 18, amount)
        current_y -= row_height

    return current_y


def main():
    if not Path(FONT_REGULAR).exists() or not Path(FONT_BOLD).exists():
        raise FileNotFoundError("Arial fonts not found in C:\\Windows\\Fonts")

    pdfmetrics.registerFont(TTFont("ArialCustom", FONT_REGULAR))
    pdfmetrics.registerFont(TTFont("ArialCustomBold", FONT_BOLD))

    pdf = canvas.Canvas(str(OUTPUT_PATH), pagesize=A4)
    pdf.setTitle("Puzzle RPA Yandex Vision Showcase")

    first_rows, second_rows = chunk_rows()
    for index, item in enumerate(first_rows, start=1):
        item["_row_no"] = str(index)
    for index, item in enumerate(second_rows, start=4):
        item["_row_no"] = str(index)

    draw_page_header(pdf, 1, "Document Type: Invoice + delivery data")
    draw_info_boxes(pdf)
    end_y = draw_table(pdf, 530, first_rows)
    pdf.setFont("ArialCustom", 10)
    pdf.drawString(36, end_y - 18, "Delivery window: 25.05.2026 - 27.05.2026")
    pdf.drawString(36, end_y - 34, f"{CONTINUED_LABEL}: page 2")
    pdf.showPage()

    draw_page_header(pdf, 2, CONTINUATION_PAGE_LABEL)
    end_y = draw_table(pdf, 730, second_rows)

    pdf.setStrokeColor(colors.HexColor("#D1D5DB"))
    pdf.roundRect(308, end_y - 102, 250, 94, 8, stroke=1, fill=0)
    pdf.setFont("ArialCustomBold", 11)
    pdf.drawString(320, end_y - 24, TOTALS_LABEL)
    pdf.setFont("ArialCustom", 10)
    pdf.drawString(320, end_y - 44, f"Subtotal: {SUBTOTAL:.2f} RUB")
    pdf.drawString(320, end_y - 60, f"VAT 20%: {VAT:.2f} RUB")
    pdf.setFont("ArialCustomBold", 11)
    pdf.drawString(320, end_y - 82, f"{TOTAL_PAYABLE_LABEL}: {TOTAL:.2f} RUB")

    pdf.setFont("ArialCustom", 10)
    pdf.drawString(36, end_y - 26, "Payment terms: 7 banking days")
    pdf.drawString(36, end_y - 42, "Responsible manager: Elena Petrova, +7 999 123-45-67")
    pdf.drawString(36, end_y - 58, "Contact email: docs@northwind.example")
    pdf.drawString(36, end_y - 74, "Demo note: Russian + English content for OCR stress test")
    pdf.save()

    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()
