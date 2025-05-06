from flask import Flask, request, jsonify
from sqlalchemy.orm import Session
from database import SessionLocal, User, ScanHistory
from predict_pipeline import predict_multiple_malwares
import datetime

app = Flask(__name__)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.route("/predict", methods=["POST"])
def predict_and_store():
    data = request.get_json()
    samples = data.get("samples")
    user_id = data.get("user_id")

    if not samples or not isinstance(samples, list):
        return jsonify({"error": "Invalid or missing sample data"}), 400

    if not user_id:
        return jsonify({"error": "Missing user ID"}), 400

    # Fetch last scan's historical_avg_error if available
    db: Session = next(get_db())
    latest_scan = db.query(ScanHistory).filter_by(user_id=user_id).order_by(ScanHistory.scan_id.desc()).first()
    historical_errors = []
    if latest_scan:
        try:
            historical_errors = sum(
                (float(latest_scan.risk_1) if latest_scan.risk_1 not in ["--", None] else 0),
                (float(latest_scan.risk_2) if latest_scan.risk_2 not in ["--", None] else 0),
                (float(latest_scan.risk_3) if latest_scan.risk_3 not in ["--", None] else 0),
            )
            
        except:
            historical_errors = 0.0

    # Perform prediction
    predictions = predict_multiple_malwares(samples, historical_errors)

    # Create ScanHistory entry
    scan_time = datetime.datetime.now()
    fields = {f"result_{i+1}": "--" for i in range(3)}
    fields.update({f"malware_type_{i+1}": "--" for i in range(3)})
    fields.update({f"anomaly_score_{i+1}": "--" for i in range(3)})
    fields.update({f"accuracy_{i+1}": "--" for i in range(3)})
    fields.update({f"risk_{i+1}": "--" for i in range(3)})

    total_risk = 0
    count = 0

    for i, result in enumerate(predictions):
        p = result["prediction"]
        idx = i + 1
        fields[f"result_{idx}"] = p["result"]
        fields[f"malware_type_{idx}"] = p["malware_type"]
        fields[f"anomaly_score_{idx}"] = p["anomaly_detection_score"] if p["result"] == "malware" else "--"
        fields[f"accuracy_{idx}"] = p["prediction_accuracy"]
        fields[f"risk_{idx}"] = p["future_risk_rating"] if p["result"] == "malware" else "--"

        if p["result"] == "malware" and isinstance(p["future_risk_rating"], (int, float)):
            total_risk += p["future_risk_rating"]
            count += 1

    avg_error = round(total_risk / count, 2) if count > 0 else 0.0

    scan = ScanHistory(
        user_id=user_id,
        scan_timestamp=scan_time,
        historical_avg_error=avg_error,
        **fields
    )
    db.add(scan)
    db.commit()

    # Return prediction result to client
    return jsonify({
        "user_id": user_id,
        "prediction_timestamp": scan_time.isoformat(),
        "predictions": predictions
    })

if __name__ == "__main__":
    app.run(debug=True)
