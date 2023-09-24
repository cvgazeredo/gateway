from flask import jsonify


# Exceptions

# Errors handler
def handle_bad_request(error):
    response = jsonify(error="BAD REQUEST")
