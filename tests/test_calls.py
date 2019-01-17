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
    if resp.status != expected_status:
        assertion = "GOT STATUS TYPE {} INSTEAD. SERVERS RESPONDED WITH {}".format(resp.status, resp.reason)
        assert resp.status == expected_status, assertion
    json_content = json.loads(content)
    if resp.status == 400 or resp.status == 404:
        assertion = "Response did not match the expected response GOT: {}. EXPECTED: {}".format(json_content, expected_result)
        assert json_content == expected_result, assertion
    else:
        if json_content.keys() != expected_result.keys():
            assertion = "Keys did not match. Got: {}, Expected: {}".format(json_content.keys(), expected_result.keys())
            assert json_content.keys() == expected_result.keys(), assertion
        for key in expected_result.keys():
            if json_content[key] != expected_result[key]:
                assertion = 'Key: {}; response: {} expected: {}'.format(key, json_content[key], expected_result[key])
                assert json_content[key] == expected_result[key], assertion
    assert json.loads(content) == expected_result


def test_post(uri, body, expected_result, expected_status):
    h = httplib2.Http()
    h.follow_all_redirects = True
    resp, content = h.request(uri, "POST", json.dumps(body))
    if resp.status != expected_status:
        assertion = 'GOT STATUS TYPE {} INSTEAD OF {}. SERVER RESPONDED WITH {}. REASON BEING: {}'\
            .format(resp.status, expected_status, resp.reason, json.loads(content))
        assert resp.status == expected_status, assertion

    json_content = json.loads(content)

    if resp.status == 400 or resp.status == 404:
        assert json_content == expected_result, \
            "GOT RESPONSE: {} EXPECTED: {}".format(json_content, expected_result)
    else:
        if json_content.keys() != expected_result.keys():
            assert json_content.keys() == expected_result.keys(), \
                'GOT KEYS: {}. EXPECTED KEYS: {}'.format(json_content.keys(), expected_result.keys())
        for key in expected_result.keys():
            assert json_content[key] == expected_result[key], \
                'Key: {}; response: {} expected: {}'.format(key, json_content[key], expected_result[key])
        assert json.loads(content) == expected_result


def test_patch(uri, body, expected_result, expected_status):
    h = httplib2.Http()
    h.follow_all_redirects = True
    resp, content = h.request(uri, "PATCH", json.dumps(body))
    if resp.status != expected_status:
        assertion = 'GOT STATUS TYPE {} INSTEAD OF {}. SERVER RESPONDED WITH {}. REASON BEING: {}'\
            .format(resp.status, expected_status, resp.reason, json.loads(content))
        assert resp.status == expected_status, assertion

    json_content = json.loads(content)

    if resp.status == 400 or resp.status == 404:
        assert json_content == expected_result, \
            "GOT RESPONSE: {} EXPECTED: {}".format(json_content, expected_result)
    else:
        if json_content.keys() != expected_result.keys():
            assert json_content.keys() == expected_result.keys(), \
                'GOT KEYS: {}. EXPECTED KEYS: {}'.format(json_content.keys(), expected_result.keys())
        for key in expected_result.keys():
            assert json_content[key] == expected_result[key], \
                'Key: {}; response: {} expected: {}'.format(key, json_content[key], expected_result[key])
        assert json.loads(content) == expected_result


def test_put(uri, body, expected_result, expected_status):
    h = httplib2.Http()
    h.follow_all_redirects = True
    resp, content = h.request(uri, "PUT", json.dumps(body))
    assert resp.status == expected_status, \
        'GOT STATUS TYPE {} INSTEAD. SERVER RESPONDED WITH {}'.format(resp.status, resp.reason)
    json_content = json.loads(content)

    if json_content.keys() != expected_result.keys():
        assertion = "Keys did not match. GOT: {}. EXPECTED: {}".format(json_content.keys(), expected_result.keys())
        assert json_content.keys() == expected_result.keys(), assertion
    for key in expected_result.keys():
        assert json_content[key] == expected_result[key], \
            'GOT: {}={} EXPECTED: {}={}'.format(key, json_content[key], key, expected_result[key])
    assert json.loads(content) == expected_result


def test_delete(uri, body, expected_result, expected_status):
    h = httplib2.Http()
    h.follow_all_redirects = True
    resp, content = h.request(uri, "DELETE", json.dumps(body))
    assert resp.status == expected_status, "GOT STATUS TYPE {} INSTEAD OF EXPECTED {}. SERVER RESPONDED WITH {}"\
        .format(resp.status, expected_status, content)

    json_content = json.loads(content)
    if json_content != expected_result:
        assert content == expected_result, 'GOT RESPONSE: {} EXPECTED: {}'.format(json_content, expected_result)
