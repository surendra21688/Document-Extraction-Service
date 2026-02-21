import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import json
from openpyxl import Workbook
import os

from classifier import classify_document
from extractor import extract_invoice_fields, extract_packing_fields


def extract_text_from_pdf(path):
    images = convert_from_path(
        path,
        poppler_path=r"C:\Program Files\poppler-25.12.0\Library\bin"
    )
    
    text = ""

    for img in images:
        text += pytesseract.image_to_string(img)

    return text


def save_json(data, filename):
    with open(f"output/{filename}.json", "w") as f:
        json.dump(data, f, indent=4)


def save_excel(data, filename):
    wb = Workbook()
    ws = wb.active

    for key, value in data.items():
        if key != "line_items":
            ws.append([key, value])

    ws.append(["Line Items"])

    for item in data["line_items"]:
        ws.append([item["raw_line"]])

    wb.save(f"output/{filename}.xlsx")


def process_document(path):
    text = extract_text_from_pdf(path)

    doc_type = classify_document(text)

    if doc_type == "Invoice":
        data = extract_invoice_fields(text)
    elif doc_type == "Packing List":
        data = extract_packing_fields(text)
    else:
        print("Unknown document type")
        return

    data["document_type"] = doc_type

    filename = os.path.basename(path).split(".")[0]

    save_json(data, filename)
    save_excel(data, filename)

    print("Processing Complete!")


if __name__ == "__main__":
    process_document("samples/invoice1.pdf")