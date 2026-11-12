import json


# ===========================================
# ELIGIBILITY AGENT
# ===========================================

def eligibility_agent(request):

    issues = []

    if request["amount_inr"] >= 25000:
        issues.append("Amount exceeds ₹25,000")

    if request["days_since_delivery"] > 30:
        issues.append("Return window exceeded (more than 30 days)")

    if not request["invoice_available"]:
        issues.append("Invoice not available")

    condition_ok = (
        request["item_condition"] == "UNOPENED"
        or (
            request["item_condition"] == "DAMAGED"
            and request["photo_evidence_available"]
        )
    )

    if not condition_ok:
        issues.append(
            "Item condition policy not satisfied"
        )

    if request["previous_returns_90_days"] >= 3:
        issues.append(
            "Customer has 3 or more previous returns"
        )

    eligible = len(issues) == 0

    return {
        "eligible": eligible,
        "issues": issues
    }


# ===========================================
# RISK AGENT
# ===========================================

def risk_agent(request):

    risk_level = "LOW"
    notes = []

    if request["amount_inr"] >= 25000:
        risk_level = "HIGH"
        notes.append("High-value item")

    if request["previous_returns_90_days"] >= 3:
        risk_level = "HIGH"
        notes.append("Frequent return history")

    if not request["invoice_available"]:
        risk_level = "HIGH"
        notes.append("Invoice missing")

    if (
        request["item_condition"] == "DAMAGED"
        and not request["photo_evidence_available"]
    ):
        risk_level = "HIGH"
        notes.append("Damaged item but photo evidence missing")

    if len(notes) == 0:
        notes.append("No significant risk identified")

    return {
        "risk_level": risk_level,
        "notes": notes
    }


# ===========================================
# APPROVAL GATEWAY
# ===========================================

def approval_gateway(eligibility_result, risk_result):

    auto_approve = (
        eligibility_result["eligible"]
        and risk_result["risk_level"] != "HIGH"
    )

    if auto_approve:
        return "AUTO_APPROVED", "Automatic"

    return None, "Human Review"


# ===========================================
# HUMAN IN LOOP
# ===========================================

def human_review(
        request,
        eligibility_result,
        risk_result
):

    print("\n" + "=" * 60)
    print("HUMAN REVIEW REQUIRED")
    print("=" * 60)

    print(f"Request ID : {request['request_id']}")
    print(f"Product    : {request['product']}")
    print(f"Amount     : ₹{request['amount_inr']}")

    print("\nEligibility Issues:")

    if eligibility_result["issues"]:
        for issue in eligibility_result["issues"]:
            print(f"- {issue}")
    else:
        print("None")

    print("\nRisk Assessment:")
    print(risk_result["risk_level"])

    for note in risk_result["notes"]:
        print(f"- {note}")

    while True:

        decision = input(
            "\nEnter approve or reject: "
        ).strip().lower()

        if decision == "approve":
            return "MANAGER_APPROVED"

        elif decision == "reject":
            return "MANAGER_REJECTED"

        else:
            print(
                "\nInvalid input."
                "\nPlease enter only approve or reject."
            )


# ===========================================
# CUSTOMER RESPONSE AGENT
# ===========================================

def customer_response_agent(request, decision):

    if decision in [
        "AUTO_APPROVED",
        "MANAGER_APPROVED"
    ]:

        return (
            f"Dear Customer,\n\n"
            f"Your {request['request_type']} request "
            f"for {request['product']} has been approved "
            f"for further processing.\n\n"
            f"This does not indicate that a refund "
            f"or replacement has already been completed."
        )

    return (
        f"Dear Customer,\n\n"
        f"After reviewing your request for "
        f"{request['product']}, we are unable "
        f"to approve it at this time."
    )


# ===========================================
# PROCESS REQUEST
# ===========================================

def process_request(request):

    eligibility_result = eligibility_agent(request)

    risk_result = risk_agent(request)

    decision, route = approval_gateway(
        eligibility_result,
        risk_result
    )

    if decision is None:

        decision = human_review(
            request,
            eligibility_result,
            risk_result
        )

    customer_message = customer_response_agent(
        request,
        decision
    )

    return {
        "request_id": request["request_id"],
        "order_id": request["order_id"],
        "product": request["product"],
        "requested_amount": request["amount_inr"],
        "eligibility_findings": eligibility_result,
        "risk_assessment": risk_result,
        "approval_route": route,
        "final_decision": decision,
        "customer_communication": customer_message
    }


# ===========================================
# MAIN
# ===========================================

def main():

    try:

        with open(
            "returns.json",
            "r",
            encoding="utf-8"
        ) as file:

            requests = json.load(file)

    except FileNotFoundError:

        print("returns.json not found.")
        return

    except Exception as e:

        print("Error reading JSON:", e)
        return

    all_results = []

    for request in requests:

        print(
            f"\nProcessing {request['request_id']}"
        )

        result = process_request(request)

        all_results.append(result)

    print("\n")
    print("=" * 80)
    print("FINAL OUTPUT")
    print("=" * 80)

    for result in all_results:

        print("\n")
        print("-" * 80)

        print(
            json.dumps(
                result,
                indent=4
            )
        )


if __name__ == "__main__":
    main()