import json
from unittest.mock import MagicMock, patch

import pytest

from app import app


@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""

    return {
        "body": json.dumps({"customer_id": "CUST001", "message": "I can't log into my account"}),
        "resource": "/agent",
        "requestContext": {
            "resourceId": "123456",
            "apiId": "1234567890",
            "resourcePath": "/agent",
            "httpMethod": "POST",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "accountId": "123456789012",
            "identity": {
                "apiKey": "",
                "userArn": "",
                "cognitoAuthenticationType": "",
                "caller": "",
                "userAgent": "Custom User Agent String",
                "user": "",
                "cognitoIdentityPoolId": "",
                "cognitoIdentityId": "",
                "cognitoAuthenticationProvider": "",
                "sourceIp": "127.0.0.1",
                "accountId": "",
            },
            "stage": "prod",
        },
        "queryStringParameters": None,
        "headers": {},
        "pathParameters": None,
        "httpMethod": "POST",
        "stageVariables": None,
        "path": "/agent",
    }


def test_lambda_handler_success(apigw_event):
    fake_crew = MagicMock()
    fake_crew.kickoff.return_value = "Please clear your browser cache and cookies."

    with patch("app.app.create_manager_agent", return_value=MagicMock()) as mock_create_manager, \
            patch("app.app.create_support_crew", return_value=fake_crew) as mock_create_crew, \
            patch("app.app.create_support_task", return_value=MagicMock()) as mock_create_task:
        ret = app.lambda_handler(apigw_event, "")

    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert data["response"] == "Please clear your browser cache and cookies."
    mock_create_crew.assert_called_once_with(mock_create_manager.return_value)
    mock_create_task.assert_called_once_with("CUST001", "I can't log into my account")
    fake_crew.kickoff.assert_called_once()


def test_lambda_handler_missing_customer_id():
    event = {"body": json.dumps({"message": "I can't log in"})}

    ret = app.lambda_handler(event, "")

    assert ret["statusCode"] == 400
    assert "error" in json.loads(ret["body"])


def test_lambda_handler_missing_message():
    event = {"body": json.dumps({"customer_id": "CUST001"})}

    ret = app.lambda_handler(event, "")

    assert ret["statusCode"] == 400
    assert "error" in json.loads(ret["body"])


def test_lambda_handler_invalid_json_body():
    event = {"body": "not-valid-json"}

    ret = app.lambda_handler(event, "")

    assert ret["statusCode"] == 400
    assert "error" in json.loads(ret["body"])


def test_lambda_handler_empty_body():
    event = {"body": None}

    ret = app.lambda_handler(event, "")

    assert ret["statusCode"] == 400
    assert "error" in json.loads(ret["body"])


def test_lambda_handler_crew_failure(apigw_event):
    with patch("app.app.create_manager_agent", side_effect=RuntimeError("boom")):
        ret = app.lambda_handler(apigw_event, "")

    data = json.loads(ret["body"])

    assert ret["statusCode"] == 500
    assert "error" in data
