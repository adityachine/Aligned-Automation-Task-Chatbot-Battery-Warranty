from .rules import (
    apply_rule_1,
    apply_rule_2,
    apply_rule_3,
    apply_rule_4,
    apply_rule_5,
    apply_rule_6
)

def is_battery_issue(issue_type):
    return "battery" in issue_type.lower()

def is_warranty_valid(warranty_status):
    return warranty_status.lower() == "valid"

def is_replacement_required(symptom_description):
    return "replace" in symptom_description.lower()

def is_tech_direct_eligible(issue_type, warranty_status, symptom_description):
    return (
        is_battery_issue(issue_type)
        and is_warranty_valid(warranty_status)
        and is_replacement_required(symptom_description)
    )

def process_case(case_data):
    """
    Main decision engine function to process a case dictionary and return:
    - Decision (e.g., "Eligible", "Ineligible", etc.)
    - Matched rules for transparency
    """
    matched_rules = []

    # Apply Rules
    if apply_rule_1(case_data.get("Model", "")):
        matched_rules.append("Rule 1")

    if apply_rule_2(case_data.get("Part Quantity", 0)):
        matched_rules.append("Rule 2")

    if apply_rule_3(case_data.get("ePSA Result", "")):
        matched_rules.append("Rule 3")

    if apply_rule_4(case_data.get("Warranty Status", "")):
        matched_rules.append("Rule 4")

    if apply_rule_5(case_data.get("Hour Tag", 0)):
        matched_rules.append("Rule 5")

    if apply_rule_6(case_data.get("Customer Tag", ""), case_data.get("Actual Tag", "")):
        matched_rules.append("Rule 6")

    # Final decision based on rules and Tech Direct eligibility
    if is_tech_direct_eligible(
        case_data.get("Issue Type", ""),
        case_data.get("Warranty Status", ""),
        case_data.get("Symptom Description", "")
    ):
        decision = "Tech Direct Eligible"
    else:
        decision = "Manual Review Required"

    return decision, matched_rules
