from flask import Blueprint, jsonify
from database import SessionLocal, ScanHistory
from datetime import datetime
from collections import defaultdict, Counter

admin_analytics_bp = Blueprint("admin_analytics", __name__)

@admin_analytics_bp.route('/admin-analytics', methods=['GET'])
def get_admin_analytics():
    db = SessionLocal()
    try:
        scans = db.query(ScanHistory).all()

        daily_counts = defaultdict(int)
        weekly_counts = defaultdict(int)
        monthly_counts = defaultdict(int)

        malware_counter = Counter()
        accuracy_totals = defaultdict(list)

        for scan in scans:
            ts = scan.scan_timestamp

            # Extract local date parts
            date_str = ts.date().isoformat()  # e.g., "2025-05-15"
            year, week_num, _ = ts.isocalendar()
            week_key = f"{year}-W{week_num:02d}"
            month_str = ts.strftime("%Y-%m")

            # Group counts
            daily_counts[date_str] += 1
            weekly_counts[week_key] += 1
            monthly_counts[month_str] += 1

            for i in range(1, 4):
                result = getattr(scan, f"result_{i}")
                mtype = getattr(scan, f"malware_type_{i}")
                acc = getattr(scan, f"accuracy_{i}")

                label = mtype if (mtype and mtype.lower() != 'n/a') else 'Benign'

                if result and result.lower() == "malware" and label.lower() != "benign":
                    malware_counter[label] += 1
                elif result and result.lower() == "benign":
                    malware_counter['Benign'] += 1

                try:
                    acc_val = float(acc)
                    if 0 <= acc_val <= 1:
                        accuracy_totals[label].append(acc_val * 100)
                except:
                    continue

        avg_detection_rate = {
            mtype: round(sum(vals) / len(vals), 2)
            for mtype, vals in accuracy_totals.items() if vals
        }

        total_detected = sum(malware_counter.values())
        malware_distribution = {
            mtype: round(100 * count / total_detected, 2)
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
