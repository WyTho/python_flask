from models.Usage import UsageModel
from models.UnitEnum import UnitEnum
from tests.test_calls import test_get, test_post, send_get
from models.UsageTypeEnum import UsageTypeEnum


def test_usage_resource():
    print("####################   TESTING USAGE RESOURCE   ####################")

    # GETTING ALL USAGES
    print("TEST_1 --- GETTING ALL USAGES")
    uri = "http://127.0.0.1:5000/api/usages"
    expected_result = {
        "usages": []
    }
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # POSTING ONE USAGE
    print("TEST_2 --- POSTING ONE USAGE")
    item_1 = send_get('http://127.0.0.1:5000/api/items/1')
    usage_1_item_id = item_1['id']
    usage_1_external_item_id = 1
    usage_1_consumption_type = UsageTypeEnum.KILOWATT
    usage_1_consumption_amount = 5
    usage_1_address = "http://127.0.0.1:5000/usages/1"
    usage_1_unit = UnitEnum.TOGGLE
    usage_1_min_value = 0
    usage_1_max_value = 1

    usage_1 = UsageModel(usage_1_item_id,
                         usage_1_external_item_id,
                         usage_1_consumption_type,
                         usage_1_consumption_amount,
                         usage_1_address,
                         usage_1_unit,
                         usage_1_min_value,
                         usage_1_max_value)
    body = {
        "item_id": usage_1_item_id,
        "external_item_id": usage_1_external_item_id,
        "consumption_type": usage_1_consumption_type.value,
        "consumption_amount": usage_1_consumption_amount,
        "address": usage_1_address,
        "unit": "TOGGLE",
        "min_value": usage_1_min_value,
        "max_value": usage_1_max_value
    }
    usage_1_json = usage_1.to_json()
    usage_1_json['id'] = 1
    expected_result = usage_1_json
    expected_status = 201
    uri = "http://127.0.0.1:5000/api/usages"
    test_post(uri, body, expected_result, expected_status)

    # GETTING ALL USAGES
    print("TEST_3 --- GETTING ALL USAGES")
    uri = "http://127.0.0.1:5000/api/usages"
    expected_result = {
        "usages": [usage_1_json]
    }
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # GETTING ONE USAGE
    print("TEST_4 --- GETTING ONE USAGE")
    uri = "http://127.0.0.1:5000/api/usages/1"
    expected_result = usage_1_json
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # UPDATING ONE USAGE
    print("TEST_5 --- UPDATING ONE USAGE")
    uri = 'http://127.0.0.1:5000/api/usages/1'
    expected_result = usage_1_json
    expected_result['address'] = '127.0.0.1:5000/api/usages/7'
    body = expected_result
    expected_status = 200
    test_post(uri, body, expected_result, expected_status)
    usage_1_json['address'] = '127.0.0.1:5000/api/usages/7'

    # GETTING ONE USAGE
    print("TEST_6 --- GETTING ONE USAGE")
    uri = "http://127.0.0.1:5000/api/usages/1"
    expected_result = usage_1_json
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # POSTING ONE USAGE - BAD REQUEST
    print("TEST_7 --- POSTING ONE USAGE - BAD REQUEST")
    item_1 = send_get('http://127.0.0.1:5000/api/items/1')
    usage_1_item_id = item_1['id']
    usage_1_external_item_id = item_1['id']
    usage_1_consumption_type = UsageTypeEnum.KILOWATT
    usage_1_consumption_amount = 5
    usage_1_address = "http://127.0.0.1:5000/usage/1"
    usage_1_min_value = 0
    usage_1_max_value = 1

    body = {
        "item_id": usage_1_item_id,
        "external_item_id": usage_1_external_item_id,
        "consumption_type": usage_1_consumption_type.value,
        "consumption_amount": usage_1_consumption_amount,
        "address": usage_1_address,
        "unit": "FOGGLE",
        "min_value": usage_1_min_value,
        "max_value": usage_1_max_value
    }
    expected_result = "FOGGLE is not a valid unit option."
    expected_status = 400
    uri = "http://127.0.0.1:5000/api/usages"
    test_post(uri, body, expected_result, expected_status)

    # POSTING ONE USAGE - BAD REQUEST
    print("TEST_8 --- POSTING ONE USAGE - BAD REQUEST")
    body['unit'] = usage_1_unit.value
    body['consumption_type'] = 'KILO WHAT?'
    expected_result = "KILO WHAT? is not a valid consumption type."
    expected_status = 400
    uri = "http://127.0.0.1:5000/api/usages"
    test_post(uri, body, expected_result, expected_status)

    # POSTING ONE USAGE - BAD REQUEST
    print("TEST_9 --- POSTING ONE USAGE - BAD REQUEST")
    body['consumption_type'] = usage_1_consumption_type.value
    body['address'] = '12'
    expected_result = "Address must be at least 3 characters long."
    expected_status = 400
    uri = "http://127.0.0.1:5000/api/usages"
    test_post(uri, body, expected_result, expected_status)

    # POSTING ONE USAGE - BAD REQUEST
    print("TEST_10 --- POSTING ONE USAGE - BAD REQUEST")
    body['address'] = "________________________________________________________________________________________" \
                      "________________________________________________________________________________________" \
                      "________________________________________________________________________________________" \
                      "________________________________________________________________________________________" \
                      "________________________________________________________________________________________" \
                      "________________________________________________________________________________________" \
                      "________________________________________________________________________________________"
    expected_result = "Address cannot be longer than 255 characters."
    expected_status = 400
    uri = "http://127.0.0.1:5000/api/usages"
    test_post(uri, body, expected_result, expected_status)

    # POSTING ONE USAGE - BAD REQUEST
    print("TEST_11 --- POSTING ONE USAGE - BAD REQUEST")
    body['address'] = usage_1_address
    body['consumption_amount'] = -1
    expected_result = "Consumption amount cannot be below 0."
    expected_status = 400
    uri = "http://127.0.0.1:5000/api/usages"
    test_post(uri, body, expected_result, expected_status)

    # POSTING ONE USAGE - BAD REQUEST
    print("TEST_12 --- POSTING ONE USAGE - BAD REQUEST")
    body['consumption_amount'] = usage_1_consumption_amount
    body['min_value'] = None
    expected_result = "If either min or max value is given, both should be given."
    expected_status = 400
    uri = "http://127.0.0.1:5000/api/usages"
    test_post(uri, body, expected_result, expected_status)

    # POSTING ONE USAGE - BAD REQUEST
    print("TEST_13 --- POSTING ONE USAGE - BAD REQUEST")
    body['min_value'] = usage_1_min_value
    body['max_value'] = None
    expected_result = "If either min or max value is given, both should be given."
    expected_status = 400
    uri = "http://127.0.0.1:5000/api/usages"
    test_post(uri, body, expected_result, expected_status)

    # EXECUTING COMMAND - BAD REQUEST
    print("TEST 14 --- POSTING COMMAND - BAD REQUEST")
    body = {}
    uri = "http://127.0.0.1:5000/api/usages/1/command/2"
    expected_result = "New value does not fall within the expected range. (0 - 1)"
    expected_status = 400
    test_post(uri, body, expected_result, expected_status)

    # POSTING ONE USAGE
    print("TEST_15 --- POSTING ONE USAGE")
    item_2 = send_get('http://127.0.0.1:5000/api/items/2')
    usage_2_item_id = item_2['id']
    usage_2_external_item_id = 1
    usage_2_consumption_type = UsageTypeEnum.KILOWATT
    usage_2_consumption_amount = 5
    usage_2_address = "http://127.0.0.1:5000/usages/2"
    usage_2_unit = UnitEnum.TOGGLE
    usage_2_min_value = 0
    usage_2_max_value = 1

    usage_2 = UsageModel(usage_2_item_id,
                         usage_2_external_item_id,
                         usage_2_consumption_type,
                         usage_2_consumption_amount,
                         usage_2_address,
                         usage_2_unit,
                         usage_2_min_value,
                         usage_2_max_value)
    body = {
        "item_id": usage_2_item_id,
        "external_item_id": usage_2_external_item_id,
        "consumption_type": usage_2_consumption_type.value,
        "consumption_amount": usage_2_consumption_amount,
        "address": usage_2_address,
        "unit": "TOGGLE",
        "min_value": usage_2_min_value,
        "max_value": usage_2_max_value
    }
    usage_2_json = usage_2.to_json()
    usage_2_json['id'] = 2
    expected_result = usage_2_json
    expected_status = 201
    uri = "http://127.0.0.1:5000/api/usages"
    test_post(uri, body, expected_result, expected_status)