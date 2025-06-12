def apply_rule_1(model_desc):
    """
    Rule 1: Check if model description matches known Dell enterprise products.
    """
    keywords = ["PowerEdge", "Dell Storage", "Equallogic", "Power Connect", "DSSD Product"]
    return any(kw.lower() in model_desc.lower() for kw in keywords)


def apply_rule_2(part_quantity):
    """
    Rule 2: Check if more than one part is being requested.
    """
    try:
        return int(part_quantity) > 1
    except (ValueError, TypeError):
        return False


def apply_rule_3(ePSA_result):
    """
    Rule 3: Check if ePSA diagnostic result indicates a failure.
    """
    if not isinstance(ePSA_result, str):
        return False
    return "epsa" in ePSA_result.lower() and "fail" in ePSA_result.lower()


def apply_rule_4(warranty_status):
    """
    Rule 4: Check if system is out of warranty.
    """
    if not isinstance(warranty_status, str):
        return False
    return "out of warranty" in warranty_status.lower()


def apply_rule_5(hour_tag):
    """
    Rule 5: Check if the support request was made after 8 business hours.
    """
    try:
        return float(hour_tag) > 8
    except (ValueError, TypeError):
        return False


def apply_rule_6(customer_tag, actual_tag):
    """
    Rule 6: Detect a mismatch between customer-reported and actual system tag.
    """
    if not all(isinstance(tag, str) for tag in [customer_tag, actual_tag]):
        return False
    return customer_tag.strip().lower() != actual_tag.strip().lower()
