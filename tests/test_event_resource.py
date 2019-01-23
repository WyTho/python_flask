from models.Event import EventModel
from models.UnitEnum import UnitEnum
from models.Error import Error
from tests.test_calls import test_get, test_post, send_get
from datetime import datetime


def test_event_resource():
    print("####################   TESTING EVENT RESOURCE   ####################")

    # GETTING ALL USAGES
    print("TEST_1 --- GETTING ALL EVENTS")
    uri = "events"
    expected_result = {
        "events": []
    }
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # POST ONE EVENT
    print("TEST_2 --- POSTING ONE EVENT")
    uri = "events"
    usage_1 = send_get('usages/1')
    event_1 = EventModel(usage_1['id'], 'True', round(datetime.now().timestamp()))
    event_1_json = event_1.to_json()
    event_1_json['id'] = 1
    body = {
        "usage_id": usage_1['id'],
        "data_type": UnitEnum.TOGGLE.value,
        "data": 'True'
    }

    expected_result = event_1_json
    expected_status = 201

    test_post(uri, body, expected_result, expected_status)

    # GETTING ONE EVENT
    print("TEST_3 --- GETTING ONE EVENT")
    uri = "events/1"
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # GETTING ALL EVENTS
    print("TEST_4 --- GETTING ALL EVENTS")
    uri = "events"
    expected_result = {
        "events": [event_1_json]
    }
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # POST ONE EVENT
    print("TEST_5 --- POSTING ONE EVENT - BAD REQUEST")
    uri = "events"
    body = {
        "usage_id": 17,
        "data_type": UnitEnum.TOGGLE.value,
        "data": 'True'
    }
    error = Error(
                "Cannot find usage with id: {}".format(17),
                "UsageModel.find_by_id({}) returns None".format(17),
                404,
                "https://en.wikipedia.org/wiki/HTTP_404")
    expected_result = {"errors": [error.to_json()]}
    expected_status = 422
    test_post(uri, body, expected_result, expected_status)

    # POST ONE EVENT
    print("TEST_6 --- POSTING ONE EVENT - BAD REQUEST")
    uri = "events"
    body = {
        "usage_id": 1,
        "data_type": "KILO WHAT?",
        "data": 'True'
    }
    error = Error(
                '"{}" is not a valid unit type.'.format("KILO WHAT?"),
                "UnitEnum.has_value({}) returned False".format("KILO WHAT?"), 400,
                "https://en.wikipedia.org/wiki/HTTP_400"
            )
    expected_result = {"errors": [error.to_json()]}
    expected_status = 422
    test_post(uri, body, expected_result, expected_status)
