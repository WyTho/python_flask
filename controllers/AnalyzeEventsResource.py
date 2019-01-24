from flask_restful import Resource
from models.Error import Error
from processing.analysis.fake_events.analyzer import analyze_fake_event_data


class AnalyzeEventsResource(Resource):

    def get(self):

        results_array = analyze_fake_event_data()
        if results_array is None:
            print('here', 30, 'error')
            error = Error(
                "The analysis did not complete correctly."
                "The analysis went HAM and broke everything.",
                500,
                "https://en.wikipedia.org/wiki/HTTP_500"
            )
            return {"errors": error.to_json()}, 500
        else:
            return {"results": results_array}, 200

