from flask import Blueprint, request, jsonify
from flask_cors import CORS
from sqlalchemy.orm import Session
from database import SessionLocal, User, ScanHistory
from predict_pipeline import predict_multiple_malwares
import datetime

# Define blueprint
predict_bp = Blueprint('predict_bp', __name__)
CORS(predict_bp, origins=["http://localhost:5173"], methods=["POST", "GET", "OPTIONS"], allow_headers=["Content-Type"], supports_credentials=True)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@predict_bp.route("/predict", methods=["POST"])
def predict_and_store():
    data = request.get_json()
    samples = data.get("samples")
    user_id = data.get("user_id")

    if not samples or not isinstance(samples, list):
        return jsonify({"error": "Invalid or missing sample data"}), 400
    if not user_id:
        return jsonify({"error": "Missing user ID"}), 400

    db: Session = next(get_db())
    latest_scan = db.query(ScanHistory).filter_by(user_id=user_id).order_by(ScanHistory.scan_id.desc()).first()

    try:
        if latest_scan:
            risks = []
            for i in range(1, 4):
                val = getattr(latest_scan, f"risk_{i}", "--")
                if val not in ["--", None]:
                    risks.append(float(val))
            historical_errors = sum(risks) / len(risks) if risks else 0.0
        else:
            historical_errors = 0.0
    except:
        historical_errors = 0.0

    predictions = predict_multiple_malwares(samples, historical_errors)

    fields = {f"result_{i+1}": "--" for i in range(3)}
    fields.update({f"malware_type_{i+1}": "--" for i in range(3)})
    fields.update({f"anomaly_score_{i+1}": "--" for i in range(3)})
    fields.update({f"accuracy_{i+1}": "--" for i in range(3)})
    fields.update({f"risk_{i+1}": "--" for i in range(3)})

    total_risk = 0.0
    risk_count = 0

    for i, result in enumerate(predictions[:3]):
        pred = result["prediction"]
        fields[f"result_{i+1}"] = pred["result"]
        fields[f"malware_type_{i+1}"] = pred["malware_type"]
        fields[f"anomaly_score_{i+1}"] = pred["anomaly_detection_score"] if pred["result"] == "malware" else "--"
        fields[f"accuracy_{i+1}"] = pred["prediction_accuracy"]
        fields[f"risk_{i+1}"] = pred["future_risk_rating"] if pred["result"] == "malware" else "--"

        if pred["result"] == "malware" and isinstance(pred["future_risk_rating"], (float, int)):
            total_risk += pred["future_risk_rating"]
            risk_count += 1

    avg_error = round(total_risk / risk_count, 2) if risk_count else 0.0

    new_scan = ScanHistory(
        user_id=user_id,
        scan_timestamp=datetime.datetime.now(),
        historical_avg_error=avg_error,
        **fields
    )
    db.add(new_scan)
    db.commit()

    return jsonify({
        "user_id": user_id,
        "prediction_timestamp": new_scan.scan_timestamp.isoformat(),
        "predictions": predictions
    })
