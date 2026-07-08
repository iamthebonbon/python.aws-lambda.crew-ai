import json
import logging

try:
    from app.agents import create_manager_agent
    from app.crew import create_support_crew
    from app.tasks import create_support_task
except ImportError:  # pragma: no cover - flat layout used by the deployed Lambda
    from agents import create_manager_agent
    from crew import create_support_crew
    from tasks import create_support_task

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """Customer support agent entry point.

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format. The JSON body must contain
        `customer_id` and `message`.

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return _response(400, {"error": "Request body must be valid JSON"})

    customer_id = body.get("customer_id")
    message = body.get("message")

    if not customer_id or not message:
        return _response(400, {"error": "Both 'customer_id' and 'message' are required"})

    try:
        manager_agent = create_manager_agent()
        support_crew = create_support_crew(manager_agent)
        support_crew.tasks = [create_support_task(customer_id, message)]

        result = support_crew.kickoff()
    except Exception as exc:
        logger.exception("Failed to run support crew")
        return _response(500, {"error": "Failed to process the support request", "details": str(exc)})

    return _response(200, {"response": str(result)})


def _response(status_code: int, payload: dict) -> dict:
    return {
        "statusCode": status_code,
        "body": json.dumps(payload),
    }
