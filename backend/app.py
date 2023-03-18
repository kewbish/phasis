from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from sys import path
from flask_caching import Cache


path.append("../")

from phasis import gen_timeline, DIR, git_commit_diffs, fetch_from_chatgpt

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
@cache.cached(timeout=300, query_string=True)
def json_contents():
    path = request.args.get("path")
    return jsonify({"contents": open(path).read() if path else ""})


@app.route("/commits", methods=["Get"])
@cache.cached(timeout=300, query_string=True)
def json_commits():
    path = request.args.get("path")
    if not path:
        return jsonify({"error": "No path"})
    path = path.replace(DIR, "")
    date = request.args.get("date")
    return jsonify(
        {
            "diffs": [
                {"sha": diff.revision, "message": diff.message}
                for diff in git_commit_diffs(
                    DIR + path, 5, commit_date=datetime.fromtimestamp(int(date)) if date else None
                )
            ]
        }
    )


@app.route("/fetch_commit", methods=["Get"])
@cache.cached(timeout=300, query_string=True)
def fetch_content():
    path = request.args.get("path")
    commit = request.args.get("commit")
    if not path:
        return jsonify({"error": "No path"})
    path = path.replace(DIR, "")
    return jsonify({"message": fetch_from_chatgpt(git_commit_diffs(DIR + path, 1, commit)[0])})


if __name__ == "__main__":
    app.run()
