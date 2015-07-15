import os
from petrarch import petrarch
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from flask import Flask, jsonify, make_response
from flask.ext.restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

cwd = os.path.abspath(os.path.dirname(__file__))


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)



class CodeAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('events', type=dict)
        super(CodeAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        event_dict = args['events']

        print(event_dict)
        event_dict_updated = petrarch.do_coding(event_dict, None)

        return event_dict_updated


api.add_resource(CodeAPI, '/petrarch/code')

if __name__ == '__main__':
    config = petrarch.utilities._get_data('data/config/', 'PETR_config.ini')
    print("reading config")
    petrarch.PETRreader.parse_Config(config)
    print("reading dicts")
    petrarch.read_dictionaries()

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5001)
    IOLoop.instance().start()
