import json

from app.tools import (
    process_refund,
    query_billing_records,
    query_customer_db,
    search_known_issues,
    update_account_status,
)


def test_query_customer_db_found():
    result = json.loads(query_customer_db.run(customer_id="CUST001"))

    assert result["name"] == "Alice Johnson"
    assert result["tier"] == "premium"


def test_query_customer_db_not_found():
    result = json.loads(query_customer_db.run(customer_id="CUST999"))

    assert result == {"error": "Customer CUST999 not found"}


def test_search_known_issues_matches_known_issue():
    result = search_known_issues.run(issue_type="login")

    assert result == "Clear browser cache and cookies. If issue persists, reset password."


def test_search_known_issues_matches_substring():
    result = search_known_issues.run(issue_type="app crash on startup")

    assert result == "Update to latest version. Check system logs for error codes."


def test_search_known_issues_no_match_returns_generic_troubleshooting():
    result = search_known_issues.run(issue_type="something unexpected")

    assert "General troubleshooting" in result


def test_query_billing_records_found():
    result = json.loads(query_billing_records.run(customer_id="CUST001"))

    assert len(result) == 2
    assert result[0]["invoice"] == "INV-001"


def test_query_billing_records_not_found():
    result = json.loads(query_billing_records.run(customer_id="CUST999"))

    assert result == {"error": "No billing records found for CUST999"}


def test_process_refund():
    result = process_refund.run(customer_id="CUST001", invoice_id="INV-002", amount=149.99)

    assert "Refund of $149.99" in result
    assert "INV-002" in result
    assert "REF-002" in result


def test_update_account_status():
    result = update_account_status.run(customer_id="CUST002", new_status="suspended")

    assert result == "Account status for CUST002 has been updated to 'suspended'."
