from models.Group import GroupModel
from models.Error import Error
from tests.test_calls import test_get, test_post, test_put, send_get, test_delete


def test_group_resource():
    print("####################   TESTING GROUP RESOURCE   ####################")

    # GETTING ALL GROUPS
    print("TEST_1 --- GETTING ALL GROUPS")
    uri = "groups"
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
    group_1_json['url'] = "127.0.0.1:5000/api/v1/groups/1"
    expected_result = group_1_json
    expected_status = 201
    uri = "groups"
    test_post(uri, body, expected_result, expected_status)

    # GETTING ALL GROUPS
    print("TEST_3 --- GETTING ALL GROUPS")
    uri = "groups"
    expected_result = {
        "groups": [group_1_json]
    }
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # GETTING ONE GROUP
    print("TEST_4 --- GETTING ONE GROUP")
    uri = "groups/1"
    expected_result = group_1_json
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # ADDING ONE ITEM TO GROUP
    print("TEST_5 --- ADDING ONE ITEM TO GROUP")
    uri = "groups/1/items"
    item_1_json = send_get('items/1')
    body = {
        "item_id": item_1_json['id']
    }
    expected_result = group_1_json
    expected_result['items'] = [{
        "id": item_1_json['id'],
        "name": item_1_json['name'],
        "comment": item_1_json['comment'],
        "url": item_1_json['url']
    }]
    expected_status = 200
    test_post(uri, body, expected_result, expected_status)
    group_1_json['items'] = [{
        "id": item_1_json['id'],
        "name": item_1_json['name'],
        "comment": item_1_json['comment'],
        "url": item_1_json['url']
    }]

    # GETTING ONE GROUP
    print("TEST_6 --- GETTING ONE GROUP")
    uri = "groups/1"
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
    group_2_json['url'] = "127.0.0.1:5000/api/v1/groups/2"
    expected_result = group_2_json
    expected_status = 201
    uri = "groups"
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
    group_3_json['url'] = "127.0.0.1:5000/api/v1/groups/3"
    expected_result = group_3_json
    expected_status = 201
    uri = "groups"
    test_post(uri, body, expected_result, expected_status)

    # ADDING ONE ITEM TO GROUP
    print("TEST_9 --- ADDING ONE ITEM TO GROUP")
    uri = "groups/2/items"
    item_1_json = send_get('items/1')
    body = {
        "item_id": item_1_json['id']
    }
    expected_result = group_2_json
    expected_result['items'] = [{
        "id": item_1_json['id'],
        "name": item_1_json['name'],
        "comment": item_1_json['comment'],
        "url": item_1_json['url']
    }]
    expected_status = 200
    test_post(uri, body, expected_result, expected_status)
    group_2_json['items'] = [{
        "id": item_1_json['id'],
        "name": item_1_json['name'],
        "comment": item_1_json['comment'],
        "url": item_1_json['url']
    }]

    # ADDING ONE ITEM TO GROUP
    print("TEST_10 --- ADDING ONE ITEM TO SECOND MODULE")
    uri = "groups/3/items"
    item_1_json = send_get('items/1')
    body = {
        "item_id": item_1_json['id']
    }
    error = Error(
        "Item cannot be in two different modules",
        "item.is_in_module() returned True",
        422,
        "https://en.wikipedia.org/wiki/HTTP_422"
    )
    expected_result = {"errors": [error.to_json()]}
    expected_status = 422
    test_post(uri, body, expected_result, expected_status)

    # GETTING ONE ITEM
    print("TEST_11 --- GETTING ONE ITEM")
    uri = "items/1"
    expected_result = {
        "id": 1,
        "name": 'Z04 Gang lamp (SW)',
        "comment": 'new_comment',
        "last_use": None,
        "usages": [],
        "url": "127.0.0.1:5000/api/v1/items/1",
        "groups": [
            {"id": 1, "name": 'Huiskamer'},
            {"id": 2, "name": 'Verlichting'}
        ]
    }
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # ADDING ONE ITEM TO GROUP
    print("TEST_12 --- REMOVING ONE ITEM FROM GROUP")
    uri = "groups/1/items/1"
    item_1_json = send_get('items/1')
    body = {
        "item_id": item_1_json['id']
    }
    expected_result = group_1_json
    expected_result['items'] = []
    expected_status = 200
    test_delete(uri, body, expected_result, expected_status)
    group_1_json['items'] = []

    # GETTING ONE GROUP
    print("TEST_13 --- GETTING ONE GROUP")
    uri = "groups/1"
    expected_result = group_1_json
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # ADDING ONE ITEM TO NON EXISTING GROUP
    print("TEST_14 --- ADDING ITEM TO NON EXISTING GROUP")
    uri = "groups/5/items"
    item_1_json = send_get('items/1')
    body = {
        "item_id": item_1_json['id']
    }
    error = Error(
        "Could not find group with id: {}".format(5),
        "GroupModel.find_by_id({}) returned None".format(5),
        404,
        "https://en.wikipedia.org/wiki/HTTP_404")
    expected_result = {"errors": [error.to_json()]}
    expected_status = 422
    test_post(uri, body, expected_result, expected_status)
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
    error = Error(
        "Name cannot be longer than 255 characters.",
        "Name parameter cannot be longer than 255 characters.",
        400,
        "https://en.wikipedia.org/wiki/HTTP_400"
    )
    expected_result = {"errors": [error.to_json()]}
    expected_status = 400
    uri = "groups"
    test_post(uri, body, expected_result, expected_status)

    # DELETING ONE GROUP
    print("TEST_16 --- DELETING ONE GROUP")
    uri = "groups/3"
    body = {}
    expected_result = "Group with id: {} was successfully deleted.".format(3)
    expected_status = 200
    test_delete(uri, body, expected_result, expected_status)

    # CHECKING IF GROUP WAS DELETED
    print("TEST_17 --- GETTING ALL GROUPS")
    uri = "groups"
    expected_result = {
        "groups": [
            group_1_json, group_2_json
        ]
    }
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # ADDING ONE ITEM TO GROUP
    print("TEST_18 --- ADDING ONE ITEM TO GROUP")
    uri = "groups/1/items"
    item_2_json = send_get('items/2')
    body = {
        "item_id": 2
    }
    expected_result = group_1_json
    expected_result['items'] = [{
        "id": item_2_json['id'],
        "name": item_2_json['name'],
        "comment": item_2_json['comment'],
        "url": item_2_json['url']
    }]
    expected_status = 200
    test_post(uri, body, expected_result, expected_status)
    group_1_json['items'] = [{
        "id": item_2_json['id'],
        "name": item_2_json['name'],
        "comment": item_2_json['comment'],
        "url": item_2_json['url']
    }]
