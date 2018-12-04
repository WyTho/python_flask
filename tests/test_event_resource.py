from models.Event import EventModel
from models.DataTypeEnum import DataTypeEnum
from tests.test_calls import test_get, test_post, send_get
from datetime import datetime


def test_event_resource():
    print("####################   TESTING EVENT RESOURCE   ####################")

    # GETTING ALL USAGES
    print("TEST_1 --- GETTING ALL EVENTS")
    uri = "http://127.0.0.1:5000/api/event"
    expected_result = {
        "events": []
    }
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # POST ONE EVENT
    print("TEST_2 --- POSTING ONE EVENT")
    uri = "http://127.0.0.1:5000/api/event"
    usage_1 = send_get('http://127.0.0.1:5000/api/usage/1')
    event_1 = EventModel(usage_1['id'], DataTypeEnum.KILOWATT, 'True', round(datetime.now().timestamp()))
    event_1_json = event_1.to_json()
    event_1_json['id'] = 1
    body = {
        "usage_id": usage_1['id'],
        "data_type": DataTypeEnum.KILOWATT.value,
        "data": 'True'
    }

    expected_result = event_1_json
    expected_status = 201

    test_post(uri, body, expected_result, expected_status)

    # GETTING ONE EVENT
    print("TEST_3 --- GETTING ONE EVENT")
    uri = "http://127.0.0.1:5000/api/event/1"
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # GETTING ALL EVENTS
    print("TEST_4 --- GETTING ALL EVENTS")
    uri = "http://127.0.0.1:5000/api/event"
    expected_result = {
        "events": [event_1_json]
    }
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # POST ONE EVENT
    print("TEST_5 --- POSTING ONE EVENT - BAD REQUEST")
    uri = "http://127.0.0.1:5000/api/event"
    body = {
        "usage_id": 17,
        "data_type": DataTypeEnum.KILOWATT.value,
        "data": 'True'
    }

    expected_result = "Could not find usage with id: 17"
    expected_status = 404
    test_post(uri, body, expected_result, expected_status)

    # POST ONE EVENT
    print("TEST_6 --- POSTING ONE EVENT - BAD REQUEST")
    uri = "http://127.0.0.1:5000/api/event"
    body = {
        "usage_id": 1,
        "data_type": "KILO WHAT?",
        "data": 'True'
    }

    expected_result = '"KILO WHAT?" is not a valid data type.'
    expected_status = 400
    test_post(uri, body, expected_result, expected_status)
