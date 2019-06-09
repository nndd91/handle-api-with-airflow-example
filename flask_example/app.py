from flask import Flask, request

import json
app = Flask(__name__)


@app.route('/api-call-example', methods=['POST'])
def api_call_example():
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
