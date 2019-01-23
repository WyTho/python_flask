from models.Item import ItemModel
from models.Error import Error
from tests.test_calls import test_get, test_post, test_put


def test_item_resource():
    print("####################   TESTING ITEM RESOURCE   ####################")

    # GETTING ALL ITEMS
    print("TEST_1 --- GETTING ALL ITEMS")
    uri = "items"
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
    item_1_json['url'] = "127.0.0.1:5000/api/v1/items/1"
    expected_result = item_1_json
    expected_status = 201
    uri = "items"
    test_post(uri, body, expected_result, expected_status)

    # GETTING ALL ITEMS
    print("TEST_3 --- GETTING ALL ITEMS")
    uri = "items"
    expected_result = {
        "items": [item_1_json]
    }
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # GETTING ONE ITEM
    print("TEST_4 --- GETTING ONE ITEM")
    uri = "items/1"
    expected_result = item_1_json
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # UPDATING ONE ITEM
    print("TEST_5 --- UPDATING ONE ITEM")
    uri = 'items/1'
    expected_result = item_1_json
    expected_result['comment'] = 'new_comment'
    body = {
        'name': item_1.name,
        'comment': 'new_comment'
    }
    expected_status = 200
    test_put(uri, body, expected_result, expected_status)
    item_1_json['comment'] = 'new_comment'

    # GETTING ONE ITEM
    print("TEST_6 --- GETTING UPDATED ITEM")
    uri = 'items/1'
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
    expected_result = {"errors": [
        Error(
            "Name cannot be longer than 255 characters.",
            "Name parameter cannot be longer than 255 characters.",
            400,
            "https://en.wikipedia.org/wiki/HTTP_400").to_json()
    ]}
    expected_status = 422
    uri = "items"
    test_post(uri, body, expected_result, expected_status)

    # POSTING ONE ITEM
    print("TEST_8 --- POSTING ONE ITEM - BAD REQUEST")
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
    expected_result = {"errors": [
        Error(
            "Comment cannot be longer than 255 characters.",
            "Name parameter cannot be longer than 255 characters.",
            400,
            "https://en.wikipedia.org/wiki/HTTP_400").to_json()
    ]}
    expected_status = 422
    uri = "items"
    test_post(uri, body, expected_result, expected_status)

    # POSTING ONE ITEM
    print("TEST_9 --- POSTING ONE ITEM")
    item_2_name = 'Z04 Eetkamer lamp (SW)'
    item_2_comment = 'ETS import'
    item_2 = ItemModel(item_2_name, item_2_comment)
    body = {
        "name": item_2_name,
        "comment": item_2_comment
    }
    item_2_json = item_2.to_json()
    item_2_json['id'] = 2
    item_2_json['url'] = "127.0.0.1:5000/api/v1/items/2"
    expected_result = item_2_json
    expected_status = 201
    uri = "items"
    test_post(uri, body, expected_result, expected_status)

