def classify_document(text):
    text_lower = text.lower()

    invoice_keywords = ["invoice number", "invoice no", "invoice date"]
    packing_keywords = ["packing list", "po number", "ship to"]

    if any(keyword in text_lower for keyword in invoice_keywords):
        return "Invoice"
    elif any(keyword in text_lower for keyword in packing_keywords):
        return "Packing List"
    else:
        return "Unknown"