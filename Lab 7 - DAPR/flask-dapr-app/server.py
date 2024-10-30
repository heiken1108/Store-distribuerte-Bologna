from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
DAPR_STATE_URL = "http://localhost:3500/v1.0/state/statestore"


# Store an item in the DAPR state store
@app.route("/items/<string:key>", methods=["PUT"])
def store_item(key):
    value = request.json.get("value")
    data = [{"key": key, "value": value}]
    response = requests.post(DAPR_STATE_URL, json=data)
    return jsonify({"status": "Item stored"}), response.status_code


# Retrieve an item from the DAPR state store
@app.route("/items/<string:key>", methods=["GET"])
def get_item(key):
    response = requests.get(f"{DAPR_STATE_URL}/{key}")
    if response.status_code == 204:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(response.json()), 200


# Delete an item from the DAPR state store
@app.route("/items/<string:key>", methods=["DELETE"])
def delete_item(key):
    response = requests.delete(f"{DAPR_STATE_URL}/{key}")
    return jsonify({"status": "Item deleted"}), response.status_code


if __name__ == "__main__":
    app.run(port=5000)
