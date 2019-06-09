from flask import Flask, request

import json
app = Flask(__name__)


@app.route('/get-list-of-user-ids')
def get_list_of_user_ids():
    return json.dumps([1, 2, 3, 4, 5])


@app.route('/process-user-ids', methods=['POST'])
def process_user_ids():
    user_ids = request.json.get('user_ids')

    if 1 in user_ids:
        result = {
            'status': 'Error',
            'user_ids_with_error': [1]
        }
    else:
        result = {
            'status': 'Success'
        }

    return json.dumps(result)
