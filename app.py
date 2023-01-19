import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from search_query import search
from elasticsearch_dsl import Index

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=['GET'])
def index():
    return "Welcome to python server"


@app.route('/search', methods=['POST'])
@cross_origin()
def process_query():
    request_data = json.loads(request.data)
    query = request_data['query']
    metaphor = request_data['metaphor']
    if ('filter' in request_data):
        filter = request_data['filter']
        fields = request_data['fields']
    else:
        filter = False
        fields = []
    res = search(query, filter=filter, fields=fields, metaphor=metaphor)
    hits = res['hits']['hits']
    time = res['took']
    # aggs = res['aggregations']
    num_results = res['hits']['total']['value']

    return jsonify({'query': query, 'results': hits, 'total_results': num_results, 'time': time})


if __name__ == '__main__':
    app.run()