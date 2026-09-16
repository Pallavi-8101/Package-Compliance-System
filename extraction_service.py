import re


def find_pattern(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return match.group(1).strip()

    return None


def extract_information(text_lines):

    full_text = "\n".join(text_lines)

    information = {
        "product_name": None,
        "mrp": None,
        "net_quantity": None,
        "manufacturer": None,
        "address": None,
        "date_info": None,
        "consumer_care": None
    }

    # Product name
    if text_lines:
        information["product_name"] = text_lines[0]

    # MRP
    information["mrp"] = find_pattern(
        r"(?:MRP|M\.R\.P)[^₹0-9]*₹?\s*([0-9]+(?:\.[0-9]+)?)",
        full_text
    )

    # Net quantity
    information["net_quantity"] = find_pattern(
        r"(?:Net\s*(?:Qty|Quantity|Wt|Weight|Volume))\s*[:\-]?\s*([0-9]+(?:\.[0-9]+)?\s*(?:g|kg|mg|ml|l|L))",
        full_text
    )

    # Manufacturer
    information["manufacturer"] = find_pattern(
        r"(?:Manufactured\s*by|Manufacturer)\s*[:\-]?\s*(.+)",
        full_text
    )

    # Address
    information["address"] = find_pattern(
        r"(?:Address|Manufactured\s*at)\s*[:\-]?\s*(.+)",
        full_text
    )

    # Date / expiry / best before
    information["date_info"] = find_pattern(
        r"(?:Mfg|Manufacturing|Packed|PKD|Best\s*Before|Expiry|Exp)[^:\n]*[:\-]?\s*([A-Za-z0-9\/\-\s]+)",
        full_text
    )

    # Consumer care
    information["consumer_care"] = find_pattern(
        r"(?:Consumer\s*Care|Customer\s*Care|Toll\s*Free|Helpline)[^:\n]*[:\-]?\s*(.+)",
        full_text
    )

    return information