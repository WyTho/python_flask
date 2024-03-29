from models.Schedule import ScheduleModel
from models.ScheduleDay import ScheduleDayModel
from models.ScheduledUsage import ScheduledUsageModel
from models.Error import Error
from tests.test_calls import test_get, test_post
import json
from datetime import datetime


def test_schedule_resource():
    print("####################   TESTING SCHEDULE RESOURCE   ####################")

    # GETTING ALL EVENT_CALLS
    print("TEST_1 --- GETTING ALL SCHEDULES")
    uri = "schedules"
    expected_result = {
        "schedules": []
    }
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # POSTING ONE EVENT_CALL
    print("TEST_2 --- POSTING ONE SCHEDULE")
    body = {
        "time": "18:00:00",
        "schedule_days": [1, 2, 3],
        "scheduled_usages": [
            {"usage_id": 1, "value": 1},
            {"usage_id": 2, "value": 1}
        ]
    }
    schedule_1 = ScheduleModel(datetime.strptime("18:00:00", "%H:%M:%S"))
    schedule_1_json = schedule_1.to_json()
    schedule_1_json['id'] = 1
    schedule_1_json['url'] = "127.0.0.1:5000/api/v1/schedules/1"

    schedule_days_1 = ScheduleDayModel(schedule_1_json['id'], 1)
    schedule_days_1_json = schedule_days_1.to_json()
    schedule_days_1_json['id'] = 1
    schedule_days_2 = ScheduleDayModel(schedule_1_json['id'], 2)
    schedule_days_2_json = schedule_days_2.to_json()
    schedule_days_2_json['id'] = 2
    schedule_days_3 = ScheduleDayModel(schedule_1_json['id'], 3)
    schedule_days_3_json = schedule_days_3.to_json()
    schedule_days_3_json['id'] = 3
    schedule_1_json['schedule_days'] = [schedule_days_1_json, schedule_days_2_json, schedule_days_3_json]

    scheduled_usage_1 = ScheduledUsageModel(1, 1, 1)
    scheduled_usage_1_json = scheduled_usage_1.to_json()
    scheduled_usage_1_json['id'] = 1
    scheduled_usage_2 = ScheduledUsageModel(1, 2, 1)
    scheduled_usage_2_json = scheduled_usage_2.to_json()
    scheduled_usage_2_json['id'] = 2
    schedule_1_json['scheduled_usages'] = [scheduled_usage_1_json, scheduled_usage_2_json]

    expected_result = schedule_1_json
    expected_status = 201
    uri = "schedules"
    test_post(uri, body, expected_result, expected_status)

    # GETTING ALL SCHEDULES
    print("TEST_3 --- GETTING ALL SCHEDULES")
    uri = "schedules"
    expected_result = {
        "schedules": [schedule_1_json]
    }
    expected_status = 200
    test_get(uri, expected_result, expected_status)

    # POSTING ONE ITEM
    print("TEST_4 --- POSTING ONE SCHEDULE - BAD REQUEST")
    body = {
        "time": "100:00:00",
        "schedule_days": [1, 2, 3],
        "scheduled_usages": [
            {"usage_id": 1, "value": 1},
            {"usage_id": 2, "value": 1}
        ]
    }
    expected_result = {"errors": [Error(
            "Invalid time format given, expected format is: '12:00:00'",
            "Invalid time format, expected format is: '%H:%M:%S'",
            422,
            "https://en.wikipedia.org/wiki/HTTP_422").to_json()]}
    expected_status = 422
    uri = "schedules"
    test_post(uri, body, expected_result, expected_status)

    # POSTING ONE ITEM
    print("TEST_5 --- POSTING ONE SCHEDULE - BAD REQUEST")
    body = {
        "time": "10:00:00",
        "schedule_days": [],
        "scheduled_usages": [
            {"usage_id": 1, "value": 1},
            {"usage_id": 2, "value": 1}
        ]
    }
    expected_result = {"errors": [Error(
                "No schedule days given.",
                "Expecting array of days",
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"
            ).to_json()]}
    expected_status = 422
    uri = "schedules"
    test_post(uri, body, expected_result, expected_status)

    # POSTING ONE ITEM
    print("TEST_6 --- POSTING ONE SCHEDULE - BAD REQUEST")
    body = {
        "time": "10:00:00",
        "scheduled_usages": [
            {"usage_id": 1, "value": 1},
            {"usage_id": 2, "value": 1}
        ]
    }
    expected_status = 422
    uri = "schedules"
    test_post(uri, body, expected_result, expected_status)

    # POSTING ONE ITEM
    print("TEST_7 --- POSTING ONE SCHEDULE - BAD REQUEST")
    body = {
        "time": "10:00:00",
        "schedule_days": [1, 2, 3],
        "scheduled_usages": [

        ]
    }
    expected_result = {"errors": [Error(
                "No schedule usages given.",
                "Expecting array of usages",
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"
            ).to_json()]}
    expected_status = 422
    uri = "schedules"
    test_post(uri, body, expected_result, expected_status)

    # POSTING ONE ITEM
    print("TEST_8 --- POSTING ONE SCHEDULE - BAD REQUEST")
    body = {
        "time": "10:00:00",
        "schedule_days": [1, 2, 3]
    }
    expected_result = {"errors": [Error(
                "No schedule usages given.",
                "Expecting array of usages",
                422,
                "https://en.wikipedia.org/wiki/HTTP_422"
            ).to_json()]}
    expected_status = 422
    uri = "schedules"
    test_post(uri, body, expected_result, expected_status)

    # POSTING ONE ITEM
    print("TEST_9 --- POSTING ONE SCHEDULE - BAD REQUEST")
    body = {
        "time": "10:00:00",
        "schedule_days": [1, 1, 2, 2],
        "scheduled_usages": [
            {"usage_id": 1, "value": 1},
            {"usage_id": 2, "value": 1}
        ]
    }
    expected_result = {"errors": [
        Error(
            "Duplicate day entry. {}".format(1),
            "Duplicate day entry. {}".format(1),
            422,
            "https://en.wikipedia.org/wiki/HTTP_422"
        ).to_json(),
        Error(
            "Duplicate day entry. {}".format(2),
            "Duplicate day entry. {}".format(2),
            422,
            "https://en.wikipedia.org/wiki/HTTP_422"
        ).to_json()]}
    expected_status = 422
    uri = "schedules"
    test_post(uri, body, expected_result, expected_status)

    # POSTING ONE ITEM
    print("TEST_10 --- POSTING ONE SCHEDULE - BAD REQUEST")
    body = {
        "time": "10:00:00",
        "schedule_days": [1, 2, 3],
        "scheduled_usages": [
            {"usage_id": 1, "value": 1},
            {"usage_id": 1, "value": 1}
        ]
    }
    expected_result = {"errors": [Error(
                            "Duplicate usage entry. {}".format(1),
                            "Duplicate usage entry. {}".format(1),
                            422,
                            "https://en.wikipedia.org/wiki/HTTP_422"
                        ).to_json()]}
    expected_status = 422
    uri = "schedules"
    test_post(uri, body, expected_result, expected_status)