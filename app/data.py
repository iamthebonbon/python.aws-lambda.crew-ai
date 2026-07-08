"""Hardcoded, in-memory "databases" used by the support crew tools.

This is a proof of concept: there is no persistence layer, all data lives in
these dictionaries and resets on every cold start.
"""

CUSTOMER_DB = {
    "CUST001": {
        "name": "Alice Johnson",
        "tier": "premium",
        "account_status": "active",
        "total_spent": 5000,
        "outstanding_balance": 0,
    },
    "CUST002": {
        "name": "Bob Smith",
        "tier": "standard",
        "account_status": "active",
        "total_spent": 500,
        "outstanding_balance": 150,
    },
    "CUST003": {
        "name": "Carol White",
        "tier": "premium",
        "account_status": "suspended",
        "total_spent": 8000,
        "outstanding_balance": 0,
    },
}

KNOWN_ISSUES = {
    "login": "Clear browser cache and cookies. If issue persists, reset password.",
    "slow_performance": "Check system requirements. Close unnecessary applications. Clear temp files.",
    "crash": "Update to latest version. Check system logs for error codes.",
    "sync": "Verify internet connection. Sign out and sign back in. Check sync settings.",
}

BILLING_RECORDS = {
    "CUST001": [
        {"invoice": "INV-001", "amount": 99.99, "status": "paid", "date": "2025-01-15"},
        {"invoice": "INV-002", "amount": 149.99, "status": "paid", "date": "2025-02-15"},
    ],
    "CUST002": [
        {"invoice": "INV-003", "amount": 49.99, "status": "paid", "date": "2025-01-20"},
        {"invoice": "INV-004", "amount": 149.99, "status": "overdue", "date": "2025-02-20"},
    ],
}
