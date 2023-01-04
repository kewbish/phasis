from flask import Flask, jsonify, request
from flask_cors import CORS
from sys import path
from flask_caching import Cache

path.append("../")

from phasis import gen_timeline, DIR

app = Flask(__name__)
app.config.from_object(__name__)
cache = Cache(config={"CACHE_TYPE": "SimpleCache"})
cache.init_app(app)

CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/timeline", methods=["GET"])
@cache.cached(timeout=300)
def json_timeline():
    return jsonify(gen_timeline(14, 10))


@app.route("/contents", methods=["GET"])
@cache.cached(timeout=300)
def json_contents():
    path = request.args.get("path")
    return jsonify({"contents": open(DIR + path).read() if path else ""})


if __name__ == "__main__":
    app.run()
