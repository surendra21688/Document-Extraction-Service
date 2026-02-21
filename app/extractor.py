import re

def extract_invoice_fields(text):
    data = {}

    vendor = re.search(r"Vendor\s*:\s*(.*)", text)
    inv_no = re.search(r"Invoice\s*(No\.?|Number)\s*:\s*(\S+)", text)
    inv_date = re.search(r"Invoice\s*Date\s*:\s*(.*)", text)

    data["vendor_name"] = vendor.group(1) if vendor else "Not Found"
    data["invoice_number"] = inv_no.group(2) if inv_no else "Not Found"
    data["invoice_date"] = inv_date.group(1) if inv_date else "Not Found"

    data["line_items"] = extract_line_items(text)

    return data


def extract_packing_fields(text):
    data = {}

    po = re.search(r"(PO\s*Number|Order\s*Number)\s*:\s*(\S+)", text)
    ship = re.search(r"Ship\s*To\s*:\s*(.*)", text)

    data["po_number"] = po.group(2) if po else "Not Found"
    data["ship_to_address"] = ship.group(1) if ship else "Not Found"
    data["line_items"] = extract_line_items(text)

    return data


def extract_line_items(text):
    lines = text.split("\n")
    items = []

    for line in lines:
        if any(char.isdigit() for char in line) and len(line.split()) > 2:
            items.append({"raw_line": line})

    return items