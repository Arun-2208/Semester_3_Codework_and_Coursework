from flask import Blueprint, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import os

dataset_bp = Blueprint("dataset_bp", __name__)
CORS(dataset_bp, origins=["http://localhost:5173"])

DATASET_PATH = "Dataset/RF_1_dataset.csv"

@dataset_bp.route('/get-dataset', methods=['GET'])
def get_dataset():
    try:
        return send_file(DATASET_PATH, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@dataset_bp.route('/upload-dataset', methods=['POST'])
def upload_dataset():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        file = request.files['file']
        if not file.filename.endswith('.csv'):
            return jsonify({"error": "Only CSV files are accepted"}), 400
        file.save(DATASET_PATH)
        return jsonify({"message": "Dataset uploaded and saved successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
