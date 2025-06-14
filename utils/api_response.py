import json

def send_api_response(code, data):
    return json.dumps({
        "status" : "success",
        "data" : data
    }), code