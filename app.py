from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# File to store JSON data
DATA_FILE = "data.json"


def load_data():
    """Load JSON list from file, or return empty list if file missing/empty."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_data(data_list):
    """Save JSON list to file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data_list, f, indent=4)


# -------- Save API (Append) --------
@app.route('/api/auction/save', methods=['POST'])
def save_entry():
    try:
        new_entry = request.get_json()

        if not new_entry:
            return jsonify({"error": "Invalid or empty JSON"}), 400

        data_list = load_data()
        data_list.append(new_entry)
        save_data(data_list)

        return jsonify({"message": "Entry added successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------- Read API --------
@app.route('/api/auction/data', methods=['GET'])
def read_entries():
    try:
        data_list = load_data()
        if not data_list:
            return jsonify({"message": "No data found", "data": []}), 200
        return jsonify(data_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------- Flush API --------
@app.route('/flush', methods=['DELETE'])
def flush_entries():
    try:
        save_data([])  # reset file with empty list
        return jsonify({"message": "All entries flushed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
