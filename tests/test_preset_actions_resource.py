from models.PresetAction import PresetActionModel
from tests.test_calls import test_get, test_post, send_get, test_put, test_delete


def test_preset_actions_resource():
    print("####################   TESTING PRESET_ACTIONS RESOURCE   ####################")
    uri = "http://127.0.0.1:5000/api/groups/2/presets/3"
    preset_3 = send_get(uri)

    # GETTING ALL PRESET_ACTIONS
    print("TEST_1 --- GETTING ALL PRESETS_ACTIONS")
    uri = "http://127.0.0.1:5000/api/groups/{}/presets/{}/preset_actions".format(preset_3['group_id'], preset_3['id'])
    expected_result = {
        "preset_actions": []
    }
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # POSTING ONE PRESET_ACTION
    print("TEST_2 --- POSTING ONE PRESET ACTION")
    preset_action_1_usage_id = 1
    preset_action_1_value = 0
    body = {
        "usage_id": preset_action_1_usage_id,
        "value": preset_action_1_value
    }
    preset_action_1 = PresetActionModel(preset_3['id'], preset_action_1_usage_id, preset_action_1_value)
    preset_action_1_json = preset_action_1.to_json()
    preset_action_1_json['id'] = 1
    expected_result = preset_action_1_json
    expected_status = 201
    uri = "http://127.0.0.1:5000/api/groups/{}/presets/{}/preset_actions".format(preset_3['group_id'], preset_3['id'])
    test_post(uri, body, expected_result, expected_status)

    # POSTING ONE PRESET_ACTION
    print("TEST_3 --- POSTING ONE PRESET ACTION - BAD REQUEST")
    body = {
        "usage_id": 2,
        "value": preset_action_1_value
    }
    expected_result = "The item that usage with id 2 is attached to does not belong to group with id 2."
    expected_status = 400
    uri = "http://127.0.0.1:5000/api/groups/{}/presets/{}/preset_actions".format(preset_3['group_id'], preset_3['id'])
    test_post(uri, body, expected_result, expected_status)

    # POSTING ONE PRESET_ACTION
    print("TEST_4 --- POSTING ONE PRESET ACTION - BAD REQUEST")
    body = {
        "usage_id": 1,
        "value": 2
    }
    expected_result = "Given value is not in range of Usage values. (0 - 1) (2 given)"
    expected_status = 400
    uri = "http://127.0.0.1:5000/api/groups/{}/presets/{}/preset_actions".format(preset_3['group_id'], preset_3['id'])
    test_post(uri, body, expected_result, expected_status)

    # GETTING ALL PRESET_ACTIONS
    print("TEST_5 --- GETTING ALL PRESETS_ACTIONS")
    uri = "http://127.0.0.1:5000/api/groups/{}/presets/{}/preset_actions".format(preset_3['group_id'], preset_3['id'])
    expected_result = {
        "preset_actions": [preset_action_1_json]
    }
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # GETTING ONE PRESET_ACTION
    print("TEST_6 --- GETTING ONE PRESETS_ACTION")
    uri = "http://127.0.0.1:5000/api/groups/{}/presets/{}/preset_actions/{}"\
        .format(preset_3['group_id'], preset_3['id'], preset_action_1_json['id'])
    expected_result = preset_action_1_json

    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # GETTING ONE PRESET_ACTION
    print("TEST_7 --- GETTING ONE PRESETS_ACTION - BAD REQUEST")
    uri = "http://127.0.0.1:5000/api/groups/{}/presets/{}/preset_actions/{}"\
        .format(preset_3['group_id'], preset_3['id'], 2)
    expected_result = "Could not find preset action with id 2."

    expected_status = 404
    test_get(uri, expected_result, expected_status)

    # PUTTING ONE PRESET_ACTION
    print("TEST_8 --- PUTTING ONE PRESET_ACTION - BAD REQUEST")
    uri = "http://127.0.0.1:5000/api/groups/{}/presets/{}/preset_actions/{}"\
        .format(preset_3['group_id'], preset_3['id'], 2)
    expected_result = "Could not find preset action with id: 2."
    expected_status = 404
    body = {
        "usage_id": 1,
        "value": 0
    }
    test_put(uri, body, expected_result, expected_status)

    # PUTTING ONE PRESET_ACTION
    print("TEST_9 --- PUTTING ONE PRESET_ACTION - BAD REQUEST")
    uri = "http://127.0.0.1:5000/api/groups/{}/presets/{}/preset_actions/{}"\
        .format(preset_3['group_id'], 2, 1)
    expected_result = "The preset id of the preset action with id: 1 did not match the given preset id. " \
                      "Perhaps you are looking for a different preset action?"
    expected_status = 400
    body = {
        "usage_id": 1,
        "value": 0
    }
    test_put(uri, body, expected_result, expected_status)

    # PUTTING ONE PRESET_ACTION
    print("TEST_10 --- PUTTING ONE PRESET_ACTION - BAD REQUEST")
    uri = "http://127.0.0.1:5000/api/groups/{}/presets/{}/preset_actions/{}"\
        .format(preset_3['group_id'], preset_3['id'], 1)
    expected_result = "Could not find Usage with id: 15."
    expected_status = 404
    body = {
        "usage_id": 15,
        "value": 0
    }
    test_put(uri, body, expected_result, expected_status)

    # PUTTING ONE PRESET_ACTION
    print("TEST_11 --- PUTTING ONE PRESET_ACTION - BAD REQUEST")
    uri = "http://127.0.0.1:5000/api/groups/{}/presets/{}/preset_actions/{}"\
        .format(preset_3['group_id'], preset_3['id'], 1)
    expected_result = "Given value is not in range of Usage values. (0 - 1) (200 given)"
    expected_status = 400
    body = {
        "usage_id": 1,
        "value": 200
    }
    test_put(uri, body, expected_result, expected_status)

    # PUTTING ONE PRESET_ACTION
    print("TEST_12 --- PUTTING ONE PRESET_ACTION")
    uri = "http://127.0.0.1:5000/api/groups/{}/presets/{}/preset_actions/{}"\
        .format(preset_3['group_id'], preset_3['id'], 1)
    preset_action_1_json['value'] = 0
    expected_result = preset_action_1_json
    expected_status = 200
    body = {
        "usage_id": 1,
        "value": 0
    }
    test_put(uri, body, expected_result, expected_status)

    # GETTING ALL PRESET_ACTIONS
    print("TEST_13 --- GETTING ALL PRESET_ACTIONS")
    uri = "http://127.0.0.1:5000/api/groups/{}/presets/{}/preset_actions"\
        .format(preset_3['group_id'], preset_3['id'])
    expected_result = {"preset_actions": [
        preset_action_1_json
    ]}
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    print("TEST_14 --- POSTING ONE PRESET ACTION")
    preset_action_2_usage_id = 2
    preset_action_2_value = 1
    body = {
        "usage_id": preset_action_2_usage_id,
        "value": preset_action_2_value
    }
    preset_action_2 = PresetActionModel(1, preset_action_2_usage_id, preset_action_2_value)
    preset_action_2_json = preset_action_2.to_json()
    preset_action_2_json['id'] = 2
    expected_result = preset_action_2_json
    expected_status = 201
    uri = "http://127.0.0.1:5000/api/groups/1/presets/1/preset_actions"
    test_post(uri, body, expected_result, expected_status)

    # GETTING ALL PRESET_ACTIONS
    print("TEST_15 --- GETTING ALL PRESET_ACTIONS")
    uri = "http://127.0.0.1:5000/api/groups/{}/presets/{}/preset_actions"\
        .format(preset_3['group_id'], preset_3['id'])
    expected_result = {
        "preset_actions": [
            preset_action_1_json
        ]
    }
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # GETTING ALL PRESET_ACTIONS
    print("TEST_16 --- GETTING ALL PRESET_ACTIONS")
    uri = "http://127.0.0.1:5000/api/groups/1/presets/1/preset_actions"
    expected_result = {
        "preset_actions": [
            preset_action_2_json
        ]
    }
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # DELETING ONE PRESET_ACTION
    print("TEST_17 --- GETTING ALL PRESET_ACTIONS - BAD REQUEST")
    uri = "http://127.0.0.1:5000/api/groups/1/presets/1/preset_actions/12"
    expected_result = "Cannot find preset action with id: 12"
    expected_status = 404
    test_delete(uri, {}, expected_result, expected_status)

    # DELETING ONE PRESET_ACTION
    print("TEST_18 --- GETTING ALL PRESET_ACTIONS - BAD REQUEST")
    uri = "http://127.0.0.1:5000/api/groups/1/presets/2/preset_actions/2"
    expected_result = "The preset id of the preset action with id: 2 did not match the given preset id. " \
                      "Perhaps you are looking for a different preset action?"
    expected_status = 400
    test_delete(uri, {}, expected_result, expected_status)

    # DELETING ONE PRESET_ACTION
    print("TEST_19 --- GETTING ALL PRESET_ACTIONS - BAD REQUEST")
    uri = "http://127.0.0.1:5000/api/groups/1/presets/1/preset_actions/2"
    expected_result = "Preset action with id: 2 was successfully deleted."
    expected_status = 200
    test_delete(uri, {}, expected_result, expected_status)
