"""
Sample app
"""
import os
from functools import wraps

from flask import Flask, abort, request

app = Flask(__name__)

def require_appkey(view_function):
    """
    Decorator function to check API Key
    """

    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        key = os.environ.get("API_KEY")
        if request.headers.get("x-api-key") and request.headers.get("x-api-key") == key:
            return view_function(*args, **kwargs)
        abort(401)
        # This line is to just conform pylint
        return None

    return decorated_function


@app.route("/json/", methods=["POST"])
@require_appkey
def put_user():
    """
    No logic here as yet
    """
    return "Posted JSON!"


@app.route("/")
def hello_world():
    """[summary]
    Just a hello world, nothing special :)
    Returns:
        str: hardcoded string
    """
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=False / True)
