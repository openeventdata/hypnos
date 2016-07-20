import os
import json
import requests
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


class ExtractAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('text', type=unicode, location='json')
        self.reqparse.add_argument('id', type=unicode, location='json')
        self.reqparse.add_argument('date', type=unicode, location='json')
        super(ExtractAPI, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        text = args['text']
        text = text.encode('utf-8')
        storyid = args['id']
        date = args['date']

        out = send_to_ccnlp(text)

        event_dict = process_corenlp(out, date, storyid)

        event_updated = send_to_petr(event_dict)

        return event_updated


def send_to_ccnlp(text):
    headers = {'Content-Type': 'application/json'}
    core_data = json.dumps({'text': text})
    ccnlp_url = 'http://ccnlp:5000/process'
    r = requests.post(ccnlp_url, data=core_data, headers=headers)
    out = r.json()

    return out


def send_to_petr(event_dict):
    headers = {'Content-Type': 'application/json'}
    events_data = json.dumps({'events': event_dict})
    petr_url = 'http://petrarch:5001/petrarch/code'
    events_r = requests.post(petr_url, data=events_data, headers=headers)
    event_updated = process_results(events_r.json())

    return event_updated


def process_corenlp(output, date, STORYID):
    event_dict = {STORYID: {}}
    event_dict[STORYID]['sents'] = {}
    event_dict[STORYID]['meta'] = {}
    event_dict[STORYID]['meta']['date'] = date
    for i, sent in enumerate(output['sentences']):
        sents = output['sentences']
        event_dict[STORYID]['sents'][str(i)] = {}
        event_dict[STORYID]['sents'][str(i)]['content'] = ' '.join(sents[i]['tokens'])
        event_dict[STORYID]['sents'][str(i)]['parsed'] = sents[i]['parse'].upper().replace(')', ' )')

    return event_dict


def process_results(event_dict):
    for s_id in event_dict:
        sents = event_dict[s_id]['sents']
        for sent in sents:
            if 'issues' not in sents[sent].keys():
                sents[sent]['issues'] = []
            if 'events' not in sents[sent].keys():
                sents[sent]['events'] = []

    return event_dict

api.add_resource(ExtractAPI, '/hypnos/extract')

if __name__ == '__main__':
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5002)
    IOLoop.instance().start()
