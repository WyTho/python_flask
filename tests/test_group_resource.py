from models.Group import GroupModel
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
        "comment": item_1_json['comment']
    }]
    expected_status = 200
    test_put(uri, body, expected_result, expected_status)
    group_1_json['items'] = [{
        "id": item_1_json['id'],
        "name": item_1_json['name'],
        "comment": item_1_json['comment']
    }]

    # GETTING ONE GROUP
    print("TEST_6 --- GETTING ONE GROUP")
    uri = "http://127.0.0.1:5000/api/group/1"
    expected_result = group_1_json
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # POSTING ONE GROUP
    print("TEST_7 --- POSTING ONE GROUP")
    group_2_name = 'Verlichting'
    group_2_is_module = False
    group_2 = GroupModel(group_2_name, group_2_is_module)
    body = {
        "name": group_2_name,
        "is_module": group_2_is_module,
    }
    group_2_json = group_2.to_json()
    group_2_json['id'] = 2
    expected_result = group_2_json
    expected_status = 201
    uri = "http://127.0.0.1:5000/api/group"
    test_post(uri, body, expected_result, expected_status)

    # POSTING ONE GROUP
    print("TEST_8 --- POSTING ONE GROUP")
    group_3_name = 'Badkamer'
    group_3_is_module = True
    group_3 = GroupModel(group_3_name, group_3_is_module)
    body = {
        "name": group_3_name,
        "is_module": group_3_is_module,
    }
    group_3_json = group_3.to_json()
    group_3_json['id'] = 3
    expected_result = group_3_json
    expected_status = 201
    uri = "http://127.0.0.1:5000/api/group"
    test_post(uri, body, expected_result, expected_status)

    # ADDING ONE ITEM TO GROUP
    print("TEST_9 --- ADDING ONE ITEM TO GROUP")
    uri = "http://127.0.0.1:5000/api/group/2"
    item_1_json = send_get('http://127.0.0.1:5000/api/item/1')
    body = {
        "item_id": item_1_json['id']
    }
    expected_result = group_2_json
    expected_result['items'] = [{
        "id": item_1_json['id'],
        "name": item_1_json['name'],
        "comment": item_1_json['comment']
    }]
    expected_status = 200
    test_put(uri, body, expected_result, expected_status)
    group_2_json['items'] = [{
        "id": item_1_json['id'],
        "name": item_1_json['name'],
        "comment": item_1_json['comment']
    }]

    # ADDING ONE ITEM TO GROUP
    print("TEST_10 --- ADDING ONE ITEM TO SECOND MODULE")
    uri = "http://127.0.0.1:5000/api/group/3"
    item_1_json = send_get('http://127.0.0.1:5000/api/item/1')
    body = {
        "item_id": item_1_json['id']
    }
    expected_result = "Item cannot be in two different modules"
    expected_status = 400
    test_put(uri, body, expected_result, expected_status)

    # GETTING ALL ITEMS
    print("TEST_11 --- GETTING ALL ITEMS")
    uri = "http://127.0.0.1:5000/api/item"
    expected_result = {
        "items": [{
            "id": 1,
            "name": 'Z04 Gang lamp (SW)',
            "comment": 'new_comment',
            "last_use": None,
            "usages": [],
            "groups": [
                {"id": 1, "name": 'Huiskamer'},
                {"id": 2, "name": 'Verlichting'}
            ]
        }],
    }
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # ADDING ONE ITEM TO GROUP
    print("TEST_12 --- REMOVING ONE ITEM FROM GROUP")
    uri = "http://127.0.0.1:5000/api/group/1"
    item_1_json = send_get('http://127.0.0.1:5000/api/item/1')
    body = {
        "item_id": item_1_json['id']
    }
    expected_result = group_1_json
    expected_result['items'] = []
    expected_status = 200
    test_put(uri, body, expected_result, expected_status)
    group_1_json['items'] = []

    # GETTING ONE GROUP
    print("TEST_13 --- GETTING ONE GROUP")
    uri = "http://127.0.0.1:5000/api/group/1"
    expected_result = group_1_json
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # ADDING ONE ITEM TO NON EXISTING GROUP
    print("TEST_14 --- ADDING ITEM TO NON EXISTING GROUP")
    uri = "http://127.0.0.1:5000/api/group/5"
    item_1_json = send_get('http://127.0.0.1:5000/api/item/1')
    body = {
        "item_id": item_1_json['id']
    }
    expected_result = "Cannot find group with id: 5"
    expected_status = 404
    test_put(uri, body, expected_result, expected_status)
    group_1_json['items'] = []

    # POSTING ONE GROUP
    print("TEST_15 --- POSTING ONE GROUP - BAD REQUEST")
    group_3_name = 'Badkamer _____________________________________________________________________' \
                   '______________________________________________________________________________' \
                   '______________________________________________________________________________' \
                   '______________________________________________________________________________'
    group_3_is_module = True
    body = {
        "name": group_3_name,
        "is_module": group_3_is_module,
    }
    expected_result = "Name cannot be longer than 255 characters."
    expected_status = 400
    uri = "http://127.0.0.1:5000/api/group"
    test_post(uri, body, expected_result, expected_status)


