from flask import Blueprint, jsonify
from database import SessionLocal, ScanHistory
from sqlalchemy import func
from datetime import datetime, timedelta
from collections import defaultdict, Counter

admin_analytics_bp = Blueprint("admin_analytics", __name__)

@admin_analytics_bp.route('/admin-analytics', methods=['GET'])
def get_admin_analytics():
    db = SessionLocal()
    try:
        scans = db.query(ScanHistory).all()

        # Totals by time unit
        now = datetime.utcnow()
        daily_counts = defaultdict(int)
        weekly_counts = defaultdict(int)
        monthly_counts = defaultdict(int)

        malware_counter = Counter()
        detection_sums = defaultdict(list)  # malware_type: [1, 1, 0]

        for scan in scans:
            ts = scan.scan_timestamp

            # Time-based buckets
            day = ts.strftime("%Y-%m-%d")
            week = ts.strftime("%Y-W%U")
            month = ts.strftime("%Y-%m")

            daily_counts[day] += 1
            weekly_counts[week] += 1
            monthly_counts[month] += 1

            # Each result/malware type
            for i in range(1, 4):
                result = getattr(scan, f"result_{i}")
                mtype = getattr(scan, f"malware_type_{i}")

                if result and result.lower() == "malware" and mtype and mtype.lower() != "n/a":
                    malware_counter[mtype] += 1
                    detection_sums[mtype].append(1)
                elif mtype and mtype.lower() != "n/a":
                    detection_sums[mtype].append(0)

        # Detection rate per type (%)
        avg_detection_rate = {
            mtype: round(100 * sum(vals) / len(vals), 2)
            for mtype, vals in detection_sums.items()
            if len(vals) > 0
        }

        # Malware type distribution (% of total detections)
        total_detections = sum(malware_counter.values())
        malware_distribution = {
            mtype: round(100 * count / total_detections, 2)
            for mtype, count in malware_counter.items()
        }

        return jsonify({
            "daily_counts": dict(sorted(daily_counts.items(), reverse=True)),
            "weekly_counts": dict(sorted(weekly_counts.items(), reverse=True)),
            "monthly_counts": dict(sorted(monthly_counts.items(), reverse=True)),
            "average_detection_rate_by_type": avg_detection_rate,
            "malware_distribution": malware_distribution
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
