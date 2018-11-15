from models.Item import ItemModel
from tests.test_calls import test_get, test_post

'''
    TEMPLATE FOR CALLS
    h = httplib2.Http()
    h.add_credentials(myname, mypasswd)
    h.follow_all_redirects = True
    headers = {'Content-Type': 'application/atom+xml'}
    body    = """<?xml version="1.0" ?>
        <entry xmlns="http://www.w3.org/2005/Atom">
          <title>Atom-Powered Robots Run Amok</title>
          <id>urn:uuid:1225c695-cfb8-4ebb-aaaa-80da344efa6a</id>
          <updated>2003-12-13T18:30:02Z</updated>
          <author><name>John Doe</name></author>
          <content>Some text.</content>
    </entry>
    """
    uri     = "http://www.example.com/collection/"
    resp, content = h.request(uri, "POST", body=body, headers=headers)
'''


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
    item_1_address = '0/0/4'
    item_1_comment = 'ETS import'
    item_1 = ItemModel(item_1_name, item_1_address, item_1_comment)
    body = {
        "name": item_1_name,
        "address": item_1_address,
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
    expected_result['address'] = '0/0/5'
    body = {
        'name': item_1.name,
        'address': '0/0/5',
        'comment': item_1.comment
    }
    expected_status = 200
    test_post(uri, body, expected_result, expected_status)
    item_1_json['address'] = '0/0/5'

    # GETTING ONE ITEM
    print("TEST_6 --- GETTING UPDATED ITEM")
    uri = 'http://127.0.0.1:5000/api/item/1'
    expected_result = item_1_json
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # COMMANDING ITEM
    # @todo test command endpoint (needs homelynk)


