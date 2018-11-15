from models.Group import GroupModel
from models.Item import ItemModel
from tests.test_calls import test_get, test_post, test_put, send_get


def test_group_resource():
    print("####################   TESTING GROUP RESOURCE   ####################")

    # GETTING ALL GROUPS
    print("TEST_1 --- GETTING ALL GROUPS")
    uri = "http://127.0.0.1:5000/api/group"
    expected_result = {
        "groups": []
    }
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # POSTING ONE GROUP
    print("TEST_2 --- POSTING ONE GROUP")
    group_1_name = 'Huiskamer'
    group_1_is_module = True
    group_1 = GroupModel(group_1_name, group_1_is_module)
    body = {
        "name": group_1_name,
        "is_module": group_1_is_module,
    }
    group_1_json = group_1.to_json()
    group_1_json['id'] = 1
    expected_result = group_1_json
    expected_status = 201
    uri = "http://127.0.0.1:5000/api/group"
    test_post(uri, body, expected_result, expected_status)

    # GETTING ALL GROUPS
    print("TEST_3 --- GETTING ALL GROUPS")
    uri = "http://127.0.0.1:5000/api/group"
    expected_result = {
        "groups": [group_1_json]
    }
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # GETTING ONE GROUP
    print("TEST_4 --- GETTING ONE GROUP")
    uri = "http://127.0.0.1:5000/api/group/1"
    expected_result = group_1_json
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # ADDING ONE ITEM TO GROUP
    print("TEST_5 --- ADDING ONE ITEM TO GROUP")
    uri = "http://127.0.0.1:5000/api/group/1"
    item_1_json = send_get('http://127.0.0.1:5000/api/item/1')
    body = {
        "item_id": item_1_json['id']
    }
    expected_result = group_1_json
    expected_result['items'] = [{
        "id": item_1_json['id'],
        "name": item_1_json['name'],
        "address": item_1_json['address'],
        "comment": item_1_json['comment']
    }]
    expected_status = 200
    test_put(uri, body, expected_result, expected_status)
    group_1_json['items'] = [{
        "id": item_1_json['id'],
        "name": item_1_json['name'],
        "address": item_1_json['address'],
        "comment": item_1_json['comment']
    }]

    # GETTING ONE GROUP
    print("TEST_6 --- GETTING ONE GROUP")
    uri = "http://127.0.0.1:5000/api/group/1"
    expected_result = group_1_json
    expected_status = 200
    test_get(uri, expected_result, expected_status)




