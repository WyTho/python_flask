import httplib2
import json


def send_get(uri):
    h = httplib2.Http()
    h.follow_all_redirects = True
    resp, content = h.request(uri, "GET")
    return json.loads(content)


def test_get(uri, expected_result, expected_status):
    h = httplib2.Http()
    h.follow_all_redirects = True
    resp, content = h.request(uri, "GET")
    assert resp.status == expected_status, 'GOT STATUS TYPE {} INSTEAD. SERVER RESPONDED WITH {}'.format(resp.status, resp.reason)
    assert json.loads(content) == expected_result


def test_post(uri, body, expected_result, expected_status):
    h = httplib2.Http()
    h.follow_all_redirects = True
    resp, content = h.request(uri, "POST", json.dumps(body))
    assert resp.status == expected_status, 'GOT STATUS TYPE {} INSTEAD. SERVER RESPONDED WITH {}'.format(resp.status, resp.reason)
    assert json.loads(content) == expected_result


def test_put(uri, body, expected_result, expected_status):
    h = httplib2.Http()
    h.follow_all_redirects = True
    resp, content = h.request(uri, "PUT", json.dumps(body))
    assert resp.status == expected_status, 'GOT STATUS TYPE {} INSTEAD. SERVER RESPONDED WITH {}'.format(resp.status, resp.reason)
    assert json.loads(content) == expected_result
