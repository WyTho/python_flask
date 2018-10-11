from flask_restful import Resource, request
from models.Graph import GraphModel


class GraphsResource(Resource):

    def get(self):
        all = GraphModel.find_all() or []
        all_in_json = [graph.to_json() for graph in all]
        return {"graphs": all_in_json}, 200


class GraphResource(Resource):

    def get(self, graph_id):
        graph = GraphModel.find_by_id(graph_id)
        return graph.to_json()
