import httplib2
import json
from models.Item import ItemModel

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
    print('testing item_resource')

    # GETTING ALL ITEMS
    uri = "http://127.0.0.1:5000/api/item"
    expected_result = {
        "items": []
    }
    send_get(uri, expected_result)

    # POSTING ONE ITEM
    item_1_name = 'Z04 Gang lamp (SW)'
    item_1_address = '0/0/4'
    item_1_comment = 'ETS import'
    item = ItemModel(item_1_name, item_1_address, item_1_comment)
    body = {
        "name": item_1_name,
        "address": item_1_address,
        "comment": item_1_comment
    }
    expected_result = item.to_json()
    expected_result['id'] = 1
    uri = "http://127.0.0.1:5000/api/item"
    send_post(uri, body, expected_result)


def send_get(uri, expected_result):
    h = httplib2.Http()
    h.follow_all_redirects = True
    resp, content = h.request(uri, "GET")
    assert resp.status == 200
    assert json.loads(content) == expected_result


def send_post(uri, body, expected_result):
    h = httplib2.Http()
    h.follow_all_redirects = True
    resp, content = h.request(uri, "POST", json.dumps(body))
    assert resp.status == 201
    assert json.loads(content) == expected_result

# ItemResource
# get | post

# ItemsResource
# get | post
# CommandResource
# post

