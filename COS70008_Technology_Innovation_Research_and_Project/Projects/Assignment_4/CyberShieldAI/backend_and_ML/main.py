from flask import Flask
from flask_cors import CORS

# Import blueprints (these must be defined as Blueprint objects inside their respective files)
from login import login_bp
from register import register_bp
from predict import predict_bp
from scan_history import scan_history_bp
from admin_analytics import admin_analytics_bp
from train_api import train_api_bp
from dataset_api import dataset_bp


app = Flask(__name__)

# Explicit CORS setup for frontend on localhost:5173
CORS(app, origins=["http://localhost:5173"], methods=["POST", "GET", "OPTIONS"], allow_headers=["Content-Type"])

# Register all API blueprints
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(predict_bp)
app.register_blueprint(scan_history_bp)
app.register_blueprint(admin_analytics_bp)
app.register_blueprint(train_api_bp)
app.register_blueprint(dataset_bp)

# Optional health check route
@app.route("/health", methods=["GET"])
def health():
    return {"status": "running"}, 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
