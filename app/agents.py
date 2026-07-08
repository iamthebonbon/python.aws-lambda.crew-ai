import os

from crewai import LLM, Agent

try:
    from app.tools import (
        process_refund,
        query_billing_records,
        query_customer_db,
        search_known_issues,
        update_account_status,
    )
except ImportError:  # pragma: no cover - flat layout used by the deployed Lambda
    from tools import (
        process_refund,
        query_billing_records,
        query_customer_db,
        search_known_issues,
        update_account_status,
    )


def _default_llm() -> LLM:
    return LLM(model=os.environ.get("CREW_MODEL", "gpt-4o-mini"))


def create_manager_agent() -> Agent:
    """Creates the manager agent that triages and delegates customer requests."""
    return Agent(
        role="Support Manager",
        goal="Understand each customer request and delegate it to the specialist best suited to resolve it.",
        backstory=(
            "A seasoned customer support manager who triages incoming requests and coordinates "
            "the technical, billing, account and escalation specialists to deliver the best resolution."
        ),
        allow_delegation=True,
        verbose=True,
        llm=_default_llm(),
    )


def create_technical_agent() -> Agent:
    """Creates the technical support agent."""
    return Agent(
        role="Technical Support Specialist",
        goal="Diagnose and resolve technical issues reported by customers.",
        backstory="An experienced engineer who has solved thousands of login, performance, crash and sync issues.",
        tools=[search_known_issues],
        allow_delegation=False,
        verbose=True,
        llm=_default_llm(),
    )


def create_billing_agent() -> Agent:
    """Creates the billing support agent."""
    return Agent(
        role="Billing Support Specialist",
        goal="Resolve billing questions, review invoices and process refunds when appropriate.",
        backstory="A meticulous billing expert who knows every customer's invoice history inside out.",
        tools=[query_billing_records, process_refund],
        allow_delegation=False,
        verbose=True,
        llm=_default_llm(),
    )


def create_account_agent() -> Agent:
    """Creates the account support agent."""
    return Agent(
        role="Account Support Specialist",
        goal="Answer account related questions and keep account status up to date.",
        backstory="An account specialist who understands customer tiers, spend history and account status.",
        tools=[query_customer_db, update_account_status],
        allow_delegation=False,
        verbose=True,
        llm=_default_llm(),
    )


def create_escalation_agent() -> Agent:
    """Creates the escalation agent for sensitive or high-priority cases."""
    return Agent(
        role="Escalation Specialist",
        goal="Handle sensitive or high-priority cases that require special care, such as premium or suspended accounts.",
        backstory="A senior specialist trusted with the most sensitive customer situations.",
        tools=[query_customer_db, query_billing_records],
        allow_delegation=False,
        verbose=True,
        llm=_default_llm(),
    )
