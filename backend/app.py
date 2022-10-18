from flask import Flask, jsonify
from flask_cors import CORS
from sys import path

path.append("../")

from phasis import gen_timeline

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/timeline", methods=["GET"])
def json_timeline():
    return jsonify(gen_timeline(14, 10))


if __name__ == "__main__":
    app.run()
