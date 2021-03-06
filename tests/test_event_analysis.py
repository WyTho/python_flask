from tests.test_calls import test_get


def test_event_analysis():
    print("####################   TESTING EVENT ANALYSIS   ####################")

    # GETTING ALL USAGES
    print("TEST_1 --- GET ANALYSIS ON FAKE EVENT DATA")
    uri = "events/analyze"
    expected_result = {
        "results": [
            {"item_ids": [4, 5], "is_predicted_group_percentage": 58.8, "is_relevant_group_percentage": 59.27},
            {"item_ids": [5, 6], "is_predicted_group_percentage": 51.6, "is_relevant_group_percentage": 50.18},
            {"item_ids": [2, 7], "is_predicted_group_percentage": 45.6, "is_relevant_group_percentage": 36.49},
            {"item_ids": [4, 7], "is_predicted_group_percentage": 75.6, "is_relevant_group_percentage": 53.72},
            {"item_ids": [1, 5], "is_predicted_group_percentage": 50.4, "is_relevant_group_percentage": 51.28},
            {"item_ids": [6, 8], "is_predicted_group_percentage": 61.2, "is_relevant_group_percentage": 44.95},
            {"item_ids": [3, 6], "is_predicted_group_percentage": 51.6, "is_relevant_group_percentage": 43.14},
            {"item_ids": [7, 8], "is_predicted_group_percentage": 57.6, "is_relevant_group_percentage": 45.46},
            {"item_ids": [2, 5, 6], "is_predicted_group_percentage": 3.6, "is_relevant_group_percentage": 6.05},
            {"item_ids": [1, 4], "is_predicted_group_percentage": 57.6, "is_relevant_group_percentage": 56.56},
            {"item_ids": [2, 5], "is_predicted_group_percentage": 69.6, "is_relevant_group_percentage": 69.51},
            {"item_ids": [5, 7], "is_predicted_group_percentage": 57.6, "is_relevant_group_percentage": 35.25},
            {"item_ids": [2, 3], "is_predicted_group_percentage": 51.6, "is_relevant_group_percentage": 54.08},
            {"item_ids": [3, 4], "is_predicted_group_percentage": 63.6, "is_relevant_group_percentage": 52.86},
            {"item_ids": [1, 2], "is_predicted_group_percentage": 52.8, "is_relevant_group_percentage": 66.07},
            {"item_ids": [3, 4, 5], "is_predicted_group_percentage": 3.6, "is_relevant_group_percentage": 2.87},
            {"item_ids": [3, 5], "is_predicted_group_percentage": 63.6, "is_relevant_group_percentage": 76.52},
            {"item_ids": [1, 8], "is_predicted_group_percentage": 70.8, "is_relevant_group_percentage": 56.58},
            {"item_ids": [2, 3, 5], "is_predicted_group_percentage": 1.2, "is_relevant_group_percentage": 1.33},
            {"item_ids": [3, 6, 8], "is_predicted_group_percentage": 4.8, "is_relevant_group_percentage": 4.55},
            {"item_ids": [3, 4, 8], "is_predicted_group_percentage": 3.6, "is_relevant_group_percentage": 11.27},
            {"item_ids": [3, 6, 7], "is_predicted_group_percentage": 10.8, "is_relevant_group_percentage": 10.23},
            {"item_ids": [2, 6], "is_predicted_group_percentage": 46.8, "is_relevant_group_percentage": 43.03},
            {"item_ids": [2, 3, 6], "is_predicted_group_percentage": 2.4, "is_relevant_group_percentage": .7},
            {"item_ids": [1, 3], "is_predicted_group_percentage": 52.8, "is_relevant_group_percentage": 44.48},
            {"item_ids": [6, 7], "is_predicted_group_percentage": 63.6, "is_relevant_group_percentage": 56.54},
            {"item_ids": [5, 8], "is_predicted_group_percentage": 78, "is_relevant_group_percentage": 66.67},
            {"item_ids": [2, 8], "is_predicted_group_percentage": 63.6, "is_relevant_group_percentage": 32.62},
            {"item_ids": [1, 6], "is_predicted_group_percentage": 61.2, "is_relevant_group_percentage": 60.55},
            {"item_ids": [1, 7], "is_predicted_group_percentage": 52.8, "is_relevant_group_percentage": 55.89},
            {"item_ids": [2, 4], "is_predicted_group_percentage": 66, "is_relevant_group_percentage": 53.33},
            {"item_ids": [5, 6, 8], "is_predicted_group_percentage": 3.6, "is_relevant_group_percentage": 10.6},
            {"item_ids": [3, 5, 8], "is_predicted_group_percentage": 10.8, "is_relevant_group_percentage": 17.15},
            {"item_ids": [4, 8], "is_predicted_group_percentage": 51.6, "is_relevant_group_percentage": 57.75},
            {"item_ids": [1, 3, 6], "is_predicted_group_percentage": 7.2, "is_relevant_group_percentage": 4.44},
            {"item_ids": [3, 8], "is_predicted_group_percentage": 68.4, "is_relevant_group_percentage": 58.12},
            {"item_ids": [6, 7, 8], "is_predicted_group_percentage": 4.8, "is_relevant_group_percentage": 1.88},
            {"item_ids": [3, 7], "is_predicted_group_percentage": 45.6, "is_relevant_group_percentage": 35.3},
            {"item_ids": [3, 4, 6], "is_predicted_group_percentage": 4.8, "is_relevant_group_percentage": .63},
            {"item_ids": [4, 6], "is_predicted_group_percentage": 48, "is_relevant_group_percentage": 27.63},
            {"item_ids": [1, 2, 6], "is_predicted_group_percentage": 6, "is_relevant_group_percentage": 4.42},
            {"item_ids": [2, 3, 6, 8], "is_predicted_group_percentage": 0, "is_relevant_group_percentage": 0},
            {"item_ids": [2, 3, 4], "is_predicted_group_percentage": 3.6, "is_relevant_group_percentage": 1.25},
            {"item_ids": [1, 3, 4], "is_predicted_group_percentage": 3.6, "is_relevant_group_percentage": .82},
            {"item_ids": [3, 5, 6], "is_predicted_group_percentage": 2.4, "is_relevant_group_percentage": 1.37},
            {"item_ids": [2, 4, 6], "is_predicted_group_percentage": 2.4, "is_relevant_group_percentage": .63},
            {"item_ids": [3, 4, 7], "is_predicted_group_percentage": 6, "is_relevant_group_percentage": 2.27},
            {"item_ids": [1, 4, 5], "is_predicted_group_percentage": 2.4, "is_relevant_group_percentage": 1.33},
            {"item_ids": [1, 6, 7, 8], "is_predicted_group_percentage": 0, "is_relevant_group_percentage": 0},
            {"item_ids": [4, 6, 7], "is_predicted_group_percentage": 2.4, "is_relevant_group_percentage": 1.27},
            {"item_ids": [2, 4, 7, 8], "is_predicted_group_percentage": 1.2, "is_relevant_group_percentage": .94},
            {"item_ids": [4, 5, 7], "is_predicted_group_percentage": 3.6, "is_relevant_group_percentage": 2.21},
            {"item_ids": [1, 3, 5], "is_predicted_group_percentage": 3.6, "is_relevant_group_percentage": 2.03},
            {"item_ids": [1, 2, 7], "is_predicted_group_percentage": 1.2, "is_relevant_group_percentage": .66},
            {"item_ids": [4, 7, 8], "is_predicted_group_percentage": 4.8, "is_relevant_group_percentage": 3.41},
            {"item_ids": [1, 6, 8], "is_predicted_group_percentage": 3.6, "is_relevant_group_percentage": 1.61},
            {"item_ids": [2, 5, 8], "is_predicted_group_percentage": 4.8, "is_relevant_group_percentage": 5.86},
            {"item_ids": [1, 7, 8], "is_predicted_group_percentage": 3.6, "is_relevant_group_percentage": 1.96},
            {"item_ids": [1, 2, 5, 7], "is_predicted_group_percentage": 0, "is_relevant_group_percentage": 0},
            {"item_ids": [1, 2, 3], "is_predicted_group_percentage": 0, "is_relevant_group_percentage": 0},
            {"item_ids": [1, 2, 5], "is_predicted_group_percentage": 1.2, "is_relevant_group_percentage": .47},
            {"item_ids": [4, 5, 8], "is_predicted_group_percentage": 2.4, "is_relevant_group_percentage": .47},
            {"item_ids": [1, 4, 8], "is_predicted_group_percentage": 2.4, "is_relevant_group_percentage": .59},
            {"item_ids": [1, 5, 7], "is_predicted_group_percentage": 4.8, "is_relevant_group_percentage": 3.92},
            {"item_ids": [5, 7, 8], "is_predicted_group_percentage": 2.4, "is_relevant_group_percentage": .21},
            {"item_ids": [2, 3, 7], "is_predicted_group_percentage": 2.4, "is_relevant_group_percentage": 2.65},
            {"item_ids": [2, 5, 7, 8], "is_predicted_group_percentage": 1.2, "is_relevant_group_percentage": .08},
            {"item_ids": [1, 3, 7], "is_predicted_group_percentage": 0, "is_relevant_group_percentage": 0},
            {"item_ids": [1, 4, 7], "is_predicted_group_percentage": 1.2, "is_relevant_group_percentage": .06},
            {"item_ids": [2, 5, 7], "is_predicted_group_percentage": 3.6, "is_relevant_group_percentage": 3.28},
            {"item_ids": [1, 2, 3, 8], "is_predicted_group_percentage": 3.6, "is_relevant_group_percentage": .2},
            {"item_ids": [1, 4, 6, 8], "is_predicted_group_percentage": 0, "is_relevant_group_percentage": 0},
            {"item_ids": [1, 3, 8], "is_predicted_group_percentage": 2.4, "is_relevant_group_percentage": .63},
            {"item_ids": [3, 4, 5, 6], "is_predicted_group_percentage": 1.2, "is_relevant_group_percentage": .08},
            {"item_ids": [2, 6, 7], "is_predicted_group_percentage": 4.8, "is_relevant_group_percentage": 1.55},
            {"item_ids": [2, 6, 8], "is_predicted_group_percentage": 2.4, "is_relevant_group_percentage": .1},
            {"item_ids": [2, 4, 7], "is_predicted_group_percentage": 1.2, "is_relevant_group_percentage": .17},
            {"item_ids": [1, 2, 4], "is_predicted_group_percentage": 3.6, "is_relevant_group_percentage": 1.83},
            {"item_ids": [1, 2, 3, 6], "is_predicted_group_percentage": 1.2, "is_relevant_group_percentage": .06},
            {"item_ids": [2, 4, 5], "is_predicted_group_percentage": 3.6, "is_relevant_group_percentage": .61},
            {"item_ids": [1, 2, 4, 6], "is_predicted_group_percentage": 0, "is_relevant_group_percentage": 0},
            {"item_ids": [2, 7, 8], "is_predicted_group_percentage": 3.6, "is_relevant_group_percentage": .84},
            {"item_ids": [3, 4, 7, 8], "is_predicted_group_percentage": 0, "is_relevant_group_percentage": 0},
            {"item_ids": [2, 3, 8], "is_predicted_group_percentage": 4.8, "is_relevant_group_percentage": 1.15},
            {"item_ids": [1, 2, 4, 6, 8], "is_predicted_group_percentage": 0, "is_relevant_group_percentage": 0},
            {"item_ids": [3, 4, 5, 7], "is_predicted_group_percentage": 0, "is_relevant_group_percentage": 0},
            {"item_ids": [5, 6, 7, 8], "is_predicted_group_percentage": 0, "is_relevant_group_percentage": 0},
            {"item_ids": [1, 5, 6], "is_predicted_group_percentage": 1.2, "is_relevant_group_percentage": .33},
            {"item_ids": [3, 5, 7], "is_predicted_group_percentage": 2.4, "is_relevant_group_percentage": .18},
            {"item_ids": [1, 2, 8], "is_predicted_group_percentage": 2.4, "is_relevant_group_percentage": .53},
            {"item_ids": [1, 2, 3, 4], "is_predicted_group_percentage": 0, "is_relevant_group_percentage": 0},
            {"item_ids": [1, 4, 6], "is_predicted_group_percentage": 3.6, "is_relevant_group_percentage": .39},
            {"item_ids": [1, 5, 8], "is_predicted_group_percentage": 1.2, "is_relevant_group_percentage": .06},
            {"item_ids": [3, 7, 8], "is_predicted_group_percentage": 0, "is_relevant_group_percentage": 0},
            {"item_ids": [4, 6, 8], "is_predicted_group_percentage": 0, "is_relevant_group_percentage": 0},
            {"item_ids": [1, 2, 4, 7], "is_predicted_group_percentage": 0, "is_relevant_group_percentage": 0},
            {"item_ids": [1, 4, 5, 6, 8], "is_predicted_group_percentage": 0, "is_relevant_group_percentage": 0},
            {"item_ids": [2, 4, 5, 8], "is_predicted_group_percentage": 0, "is_relevant_group_percentage": 0},
            {"item_ids": [1, 2, 5, 6], "is_predicted_group_percentage": 0, "is_relevant_group_percentage": 0},
            {"item_ids": [4, 5, 6, 7], "is_predicted_group_percentage": 0, "is_relevant_group_percentage": 0},
            {"item_ids": [4, 5, 6], "is_predicted_group_percentage": 0, "is_relevant_group_percentage": 0},
            {"item_ids": [2, 4, 8], "is_predicted_group_percentage": 0, "is_relevant_group_percentage": 0},
            {"item_ids": [2, 3, 5, 8], "is_predicted_group_percentage": 0, "is_relevant_group_percentage": 0},
            {"item_ids": [5, 6, 7], "is_predicted_group_percentage": 0, "is_relevant_group_percentage": 0},
            {"item_ids": [2, 3, 4, 8], "is_predicted_group_percentage": 0, "is_relevant_group_percentage": 0}
        ]
    }
    expected_status = 200
    test_get(uri, expected_result, expected_status)

