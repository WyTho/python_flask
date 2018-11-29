from models.Item import ItemModel
from tests.test_calls import test_get, test_post


def test_item_resource():
    print("####################   TESTING ITEM RESOURCE   ####################")

    # GETTING ALL ITEMS
    print("TEST_1 --- GETTING ALL ITEMS")
    uri = "http://127.0.0.1:5000/api/item"
    expected_result = {
        "items": []
    }
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # POSTING ONE ITEM
    print("TEST_2 --- POSTING ONE ITEM")
    item_1_name = 'Z04 Gang lamp (SW)'
    item_1_comment = 'ETS import'
    item_1 = ItemModel(item_1_name, item_1_comment)
    body = {
        "name": item_1_name,
        "comment": item_1_comment
    }
    item_1_json = item_1.to_json()
    item_1_json['id'] = 1
    expected_result = item_1_json
    expected_status = 201
    uri = "http://127.0.0.1:5000/api/item"
    test_post(uri, body, expected_result, expected_status)

    # GETTING ALL ITEMS
    print("TEST_3 --- GETTING ALL ITEMS")
    uri = "http://127.0.0.1:5000/api/item"
    expected_result = {
        "items": [item_1_json]
    }
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # GETTING ONE ITEM
    print("TEST_4 --- GETTING ONE ITEM")
    uri = "http://127.0.0.1:5000/api/item/1"
    expected_result = item_1_json
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # UPDATING ONE ITEM
    print("TEST_5 --- UPDATING ONE ITEM")
    uri = 'http://127.0.0.1:5000/api/item/1'
    expected_result = item_1_json
    expected_result['comment'] = 'new_comment'
    body = {
        'name': item_1.name,
        'comment': 'new_comment'
    }
    expected_status = 200
    test_post(uri, body, expected_result, expected_status)
    item_1_json['comment'] = 'new_comment'

    # GETTING ONE ITEM
    print("TEST_6 --- GETTING UPDATED ITEM")
    uri = 'http://127.0.0.1:5000/api/item/1'
    expected_result = item_1_json
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # POSTING ONE ITEM
    print("TEST_7 --- POSTING ONE ITEM - BAD REQUEST")
    item_1_name = 'Z04 Gang lamp (SW)_______________________________________________________________' \
                  '_________________________________________________________________________________' \
                  '_________________________________________________________________________________' \
                  '_________________________________________________________________________________'
    item_1_comment = 'ETS import'
    item_1 = ItemModel(item_1_name, item_1_comment)
    body = {
        "name": item_1_name,
        "comment": item_1_comment
    }
    item_1_json = item_1.to_json()
    item_1_json['id'] = 2
    expected_result = "Name cannot be longer than 255 characters."
    expected_status = 400
    uri = "http://127.0.0.1:5000/api/item"
    test_post(uri, body, expected_result, expected_status)

    # POSTING ONE ITEM
    print("TEST_9 --- POSTING ONE ITEM - BAD REQUEST")
    item_1_name = 'Z04 Gang lamp (SW)'
    item_1_comment = 'ETS import_______________________________________________________________' \
                     '_________________________________________________________________________________' \
                     '_________________________________________________________________________________' \
                     '_________________________________________________________________________________'
    item_1 = ItemModel(item_1_name, item_1_comment)
    body = {
        "name": item_1_name,
        "comment": item_1_comment
    }
    item_1_json = item_1.to_json()
    item_1_json['id'] = 2
    expected_result = "Comment cannot be longer than 255 characters."
    expected_status = 400
    uri = "http://127.0.0.1:5000/api/item"
    test_post(uri, body, expected_result, expected_status)

    # COMMANDING ITEM
    # @todo test command endpoint (needs homelynk)


