from crewai import Task


def create_support_task(customer_id: str, message: str) -> Task:
    """Creates the task describing a single customer support request."""
    return Task(
        description=(
            f"Customer {customer_id} has the following request:\n\n"
            f"{message}\n\n"
            "Identify which specialist(s) should handle it, gather the relevant "
            "information using the available tools, and resolve the request."
        ),
        expected_output="A clear, complete response addressed to the customer that resolves their request.",
    )
