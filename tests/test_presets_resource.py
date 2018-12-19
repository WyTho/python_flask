from models.Preset import PresetModel
from tests.test_calls import test_get, test_post, test_delete
import json


def test_presets_resource():
    print("####################   TESTING PRESETS RESOURCE   ####################")

    # GETTING ALL PRESETS
    print("TEST_1 --- GETTING ALL PRESETS")
    uri = "http://127.0.0.1:5000/api/groups/1/presets"
    expected_result = {
        "presets": []
    }
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # POSTING ONE PRESET
    print("TEST_2 --- POSTING ONE PRESET")
    preset_1_group_id = 1
    preset_1_name = "name"
    body = {
        "name": preset_1_name,
    }
    preset_1 = PresetModel(preset_1_group_id, preset_1_name)
    preset_1_json = preset_1.to_json()
    preset_1_json['id'] = 1
    expected_result = preset_1_json
    expected_status = 201
    uri = "http://127.0.0.1:5000/api/groups/{}/presets".format(preset_1_group_id)
    test_post(uri, body, expected_result, expected_status)

    # POSTING ONE PRESET
    print("TEST_3 --- POSTING ONE PRESET - BAD REQUEST")
    body = {
        "name": "na",
    }
    expected_result = 'Name must be at least 3 characters long.'
    expected_status = 400
    uri = "http://127.0.0.1:5000/api/groups/{}/presets".format(preset_1_group_id)
    test_post(uri, body, expected_result, expected_status)

    # POSTING ONE PRESET
    print("TEST_4 --- POSTING ONE PRESET - BAD REQUEST")
    body = {
        "name": "namenamenamenamenamenamenamenamenamename",
    }
    expected_result = 'Name cannot be longer than 30 characters.'
    expected_status = 400
    uri = "http://127.0.0.1:5000/api/groups/{}/presets".format(preset_1_group_id)
    test_post(uri, body, expected_result, expected_status)

    # GETTING ALL PRESETS
    print("TEST_5 --- GETTING ALL PRESETS")
    uri = "http://127.0.0.1:5000/api/groups/{}/presets".format(preset_1_group_id)
    expected_result = {
        "presets": [preset_1_json]
    }
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # POSTING ONE PRESET
    print("TEST_6 --- POSTING ONE PRESET")
    preset_2_group_id = 1
    preset_2_name = "preset_22"
    body = {
        "name": preset_2_name,
    }
    preset_2 = PresetModel(preset_2_group_id, preset_2_name)
    preset_2_json = preset_2.to_json()
    preset_2_json['id'] = 2
    expected_result = preset_2_json
    expected_status = 201
    uri = "http://127.0.0.1:5000/api/groups/{}/presets".format(preset_2_group_id)
    test_post(uri, body, expected_result, expected_status)

    # GETTING ALL PRESETS
    print("TEST_7 --- GETTING ALL PRESETS")
    uri = "http://127.0.0.1:5000/api/groups/{}/presets".format(preset_1_group_id)
    expected_result = {
        "presets": [preset_1_json, preset_2_json]
    }
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # DELETING ONE PRESET
    print("TEST_8 --- DELETING ONE PRESET")
    uri = "http://127.0.0.1:5000/api/groups/{}/presets/{}".format(preset_1_group_id, preset_2_json['id'])
    expected_result = "Preset with id: {} was successfully deleted.".format(preset_2_json['id'])
    expected_status = 200
    test_delete(uri, {}, expected_result, expected_status)

    # GETTING ALL PRESETS
    print("TEST_9 --- GETTING ALL PRESETS")
    uri = "http://127.0.0.1:5000/api/groups/{}/presets".format(preset_1_group_id)
    expected_result = {
        "presets": [preset_1_json]
    }
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # UPDATING ONE PRESET
    print("TEST_10 --- UPDATING ONE PRESET")
    uri = "http://127.0.0.1:5000/api/groups/{}/presets/{}".format(preset_1_group_id, preset_1_json['id'])
    body = {
        "name": "preset_1"
    }
    preset_1_json['name'] = "preset_1"
    expected_status = 200
    test_post(uri, body, preset_1_json, expected_status)

    # GETTING ALL PRESETS
    print("TEST_11 --- GETTING ALL PRESETS")
    uri = "http://127.0.0.1:5000/api/groups/{}/presets".format(preset_1_group_id)
    expected_result = {
        "presets": [preset_1_json]
    }
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # POSTING ONE PRESET
    print("TEST_12 --- POSTING ONE PRESET")
    preset_3_group_id = 2
    preset_3_name = "preset_3"
    body = {
        "name": preset_3_name,
    }
    preset_3 = PresetModel(preset_3_group_id, preset_3_name)
    preset_3_json = preset_3.to_json()
    preset_3_json['id'] = 3
    expected_result = preset_3_json
    expected_status = 201
    uri = "http://127.0.0.1:5000/api/groups/{}/presets".format(preset_3_group_id)
    test_post(uri, body, expected_result, expected_status)