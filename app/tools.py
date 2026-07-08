import json

from crewai.tools import tool

try:
    from app.data import BILLING_RECORDS, CUSTOMER_DB, KNOWN_ISSUES
except ImportError:  # pragma: no cover - flat layout used by the deployed Lambda
    from data import BILLING_RECORDS, CUSTOMER_DB, KNOWN_ISSUES


@tool("Query Customer Database")
def query_customer_db(customer_id: str) -> str:
    """
    Retrieves customer information from the database.
    Args:
        customer_id: The customer's unique identifier (e.g., CUST001)
    Returns:
        JSON string with customer information or error message
    """
    if customer_id in CUSTOMER_DB:
        return json.dumps(CUSTOMER_DB[customer_id])
    return json.dumps({"error": f"Customer {customer_id} not found"})


@tool("Search Known Issues")
def search_known_issues(issue_type: str) -> str:
    """
    Searches database of known technical issues and their solutions.
    Args:
        issue_type: Type of issue (login, performance, crash, sync, etc.)
    Returns:
        Solution steps if issue is known, otherwise generic troubleshooting
    """
    issue_lower = issue_type.lower()
    for key, solution in KNOWN_ISSUES.items():
        if key in issue_lower:
            return solution
    return (
        "No known issue matched. General troubleshooting: restart the application, "
        "check for updates, and contact support with error details if the problem persists."
    )


@tool("Query Billing Records")
def query_billing_records(customer_id: str) -> str:
    """
    Retrieves billing history for a customer.
    Args:
        customer_id: The customer's unique identifier
    Returns:
        JSON string with billing records or error message
    """
    if customer_id in BILLING_RECORDS:
        return json.dumps(BILLING_RECORDS[customer_id])
    return json.dumps({"error": f"No billing records found for {customer_id}"})


@tool("Process Refund")
def process_refund(customer_id: str, invoice_id: str, amount: float) -> str:
    """
    Processes a refund for a customer (simulation - no actual processing).
    Args:
        customer_id: Customer identifier
        invoice_id: Invoice to refund
        amount: Refund amount
    Returns:
        Confirmation message with reference number
    """
    reference = f"REF-{invoice_id[-3:]}"
    return (
        f"Refund of ${amount:.2f} for invoice {invoice_id} (customer {customer_id}) "
        f"has been processed. Reference: {reference}"
    )


@tool("Update Account Status")
def update_account_status(customer_id: str, new_status: str) -> str:
    """
    Updates customer account status (simulation - no actual update).
    Args:
        customer_id: Customer identifier
        new_status: New status (active, suspended, closed)
    Returns:
        Confirmation message
    """
    return f"Account status for {customer_id} has been updated to '{new_status}'."
