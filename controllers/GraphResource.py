from flask_restful import Resource, request
from models.Graph import GraphModel
from processing.CalculateHoulyAverages import RecalculateGraphValues


class GraphsResource(Resource):

    def get(self):
        all = GraphModel.find_all() or []
        all_in_json = [graph.to_json() for graph in all]
        return {"graphs": all_in_json}, 200


class GraphResource(Resource):

    def get(self, title):
        print(title)

        starting_date_timestamp = None
        ending_date_timestamp = None
        if 'starting_date_timestamp' in request.form.keys():
            starting_date_timestamp = request.form['starting_date_timestamp']
        elif 'ending_date_timestamp' in request.form.keys():
            ending_date_timestamp = request.form['ending_date_timestamp']

        graph = GraphModel.find_by_title(title,
                                         starting_date_timestamp=starting_date_timestamp,
                                         ending_date_timestamp=ending_date_timestamp)
        # @todo find proper threading for sql connections
        RecalculateGraphValues(graph)

        return graph.to_json()
