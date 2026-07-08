from crewai import Agent, Crew, Process

try:
    from app.agents import (
        create_account_agent,
        create_billing_agent,
        create_escalation_agent,
        create_technical_agent,
    )
except ImportError:  # pragma: no cover - flat layout used by the deployed Lambda
    from agents import (
        create_account_agent,
        create_billing_agent,
        create_escalation_agent,
        create_technical_agent,
    )


def create_support_crew(manager_agent: Agent) -> Crew:
    """
    Creates the hierarchical support crew with all agents.

    Returns:
        Crew configured with hierarchical process
    """
    technical = create_technical_agent()
    billing = create_billing_agent()
    account = create_account_agent()
    escalation = create_escalation_agent()

    return Crew(
        agents=[technical, billing, account, escalation],
        tasks=[],
        process=Process.hierarchical,
        manager_agent=manager_agent,
        verbose=True,
    )
