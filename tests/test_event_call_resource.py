from models.EventCall import EventCallModel
from tests.test_calls import test_get, test_post
import json


def test_event_call_resource():
    print("####################   TESTING EVENT CALL RESOURCE   ####################")

    # GETTING ALL EVENT_CALLS
    print("TEST_1 --- GETTING ALL EVENT_CALLS")
    uri = "event_calls"
    expected_result = {
        "event_calls": []
    }
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # POSTING ONE EVENT_CALL
    print("TEST_2 --- POSTING ONE EVENT_CALL")
    body = {
        "name": "name",
        "is_module": "is_module",
    }
    event_call_1 = EventCallModel(str(json.dumps(body)))
    event_call_1_json = event_call_1.to_json()
    event_call_1_json['id'] = 1
    expected_result = event_call_1_json
    expected_status = 201
    uri = "event_calls"
    test_post(uri, body, expected_result, expected_status)

    # GETTING ALL EVENT_CALLS
    print("TEST_3 --- GETTING ALL EVENT_CALLS")
    uri = "event_calls"
    expected_result = {
        "event_calls": [event_call_1_json]
    }
    expected_status = 200
    test_get(uri, expected_result, expected_status)
