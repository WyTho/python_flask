from flask_restful import Resource, request
from models.Graph import GraphModel
from processing.GraphProcessor import GraphProcessor


class GraphsResource(Resource):

    def get(self):
        all = GraphModel.find_all() or []
        all_in_json = [graph.to_json() for graph in all]
        return {"graphs": all_in_json}, 200


class GraphResource(Resource):

    def get(self, title):
        # Starting_date and ending_date are optional parameters. if neither is given then todays date will be used
        starting_date_timestamp = None
        ending_date_timestamp = None
        if 'starting_date_timestamp' in request.args.keys():
            starting_date_timestamp = int(request.args['starting_date_timestamp'])
        if 'ending_date_timestamp' in request.args.keys():
            ending_date_timestamp = int(request.args['ending_date_timestamp'])

        graph = GraphModel.find_by_title(title,
                                         starting_date_timestamp=starting_date_timestamp,
                                         ending_date_timestamp=ending_date_timestamp)

        return graph.to_json()

    def put(self, title):
        starting_date_timestamp = None
        ending_date_timestamp = None
        if 'starting_date_timestamp' in request.args.keys():
            starting_date_timestamp = request.args['starting_date_timestamp']
        elif 'ending_date_timestamp' in request.args.keys():
            ending_date_timestamp = request.args['ending_date_timestamp']

        graph = GraphModel.find_by_title(title,
                                         starting_date_timestamp=starting_date_timestamp,
                                         ending_date_timestamp=ending_date_timestamp)

        processor = GraphProcessor(graph)
        graph = processor.process()

        return graph.to_json()
