from flask import Blueprint, request, jsonify
from train_model import train_model_with_params
from flask_cors import CORS

train_api_bp = Blueprint('train_api_bp', __name__)
CORS(train_api_bp, origins=["http://localhost:5173"], methods=["POST", "GET", "OPTIONS"], allow_headers=["Content-Type"])

@train_api_bp.route('/retrain-model', methods=['POST'])
def retrain_model():
    try:
        data = request.get_json()
        epochs = int(data.get('epochs', 100))
        batch_size = int(data.get('batch_size', 32))
        learning_rate = float(data.get('learning_rate', 0.001))

        result = train_model_with_params(epochs, batch_size, learning_rate)

        return jsonify({
            "status": "success",
            "logs": result["logs"],
            "training_plot": result["plot_base64"]
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
