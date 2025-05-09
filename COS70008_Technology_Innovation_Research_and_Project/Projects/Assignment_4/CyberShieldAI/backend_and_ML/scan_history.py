from flask import Blueprint, request, jsonify
from flask_cors import CORS
from database import SessionLocal, ScanHistory
from sqlalchemy.exc import SQLAlchemyError

# Define blueprint
scan_history_bp = Blueprint("scan_history", __name__)
CORS(scan_history_bp, origins=["http://localhost:5173"], methods=["GET"], allow_headers=["Content-Type"])

# Route 1: Fetch scan history list for a user
@scan_history_bp.route('/scan-history', methods=['GET'])
def fetch_scan_history():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    db = SessionLocal()
    try:
        scan_records = db.query(ScanHistory).filter(ScanHistory.user_id == user_id).order_by(ScanHistory.scan_id.desc()).all()
        result = []
        for scan in scan_records:
            types = [scan.malware_type_1, scan.malware_type_2, scan.malware_type_3]
            clean_types = [t for t in types if t and t != '--' and t != 'N/A']
            result_str = ', '.join(clean_types) if clean_types else 'Benign'
            result.append({
                "scan_id": scan.scan_id,
                "scan_timestamp": scan.scan_timestamp,
                "result_1": result_str
            })
        return jsonify(result)
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# Route 2: Fetch full scan details for PDF generation
@scan_history_bp.route('/scan-details/<int:scan_id>', methods=['GET'])
def fetch_scan_detail(scan_id):
    db = SessionLocal()
    try:
        scan = db.query(ScanHistory).filter(ScanHistory.scan_id == scan_id).first()
        if not scan:
            return jsonify({"error": "Scan not found"}), 404

        return jsonify({
            "scan_id": scan.scan_id,
            "user_id": scan.user_id,
            "scan_timestamp": scan.scan_timestamp,
            "result_1": scan.result_1,
            "malware_type_1": scan.malware_type_1,
            "anomaly_score_1": scan.anomaly_score_1,
            "accuracy_1": scan.accuracy_1,
            "risk_1": scan.risk_1,
            "result_2": scan.result_2,
            "malware_type_2": scan.malware_type_2,
            "anomaly_score_2": scan.anomaly_score_2,
            "accuracy_2": scan.accuracy_2,
            "risk_2": scan.risk_2,
            "result_3": scan.result_3,
            "malware_type_3": scan.malware_type_3,
            "anomaly_score_3": scan.anomaly_score_3,
            "accuracy_3": scan.accuracy_3,
            "risk_3": scan.risk_3,
            "historical_avg_error": scan.historical_avg_error
        })
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
