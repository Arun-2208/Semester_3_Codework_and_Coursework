# Full updated predict_pipeline.py with final logic

import numpy as np
import pickle
import tensorflow as tf
import os

# Paths
MODEL_DIR = 'ml_models/saved_models/'

# Load Autoencoder
autoencoder = tf.keras.models.load_model(os.path.join(MODEL_DIR, 'autoencoder_model.h5'))

# Load Scalers
with open(os.path.join(MODEL_DIR, 'scaler_rf1.pkl'), 'rb') as f:
    scaler_rf1 = pickle.load(f)

with open(os.path.join(MODEL_DIR, 'scaler_ae.pkl'), 'rb') as f:
    scaler_ae = pickle.load(f)

# Load Random Forest Models
with open(os.path.join(MODEL_DIR, 'rf_binary.pkl'), 'rb') as f:
    rf_binary = pickle.load(f)

with open(os.path.join(MODEL_DIR, 'rf_multiclass.pkl'), 'rb') as f:
    rf_multiclass = pickle.load(f)

# Define AE feature set
ae_features = [
    'pslist.nproc',
    'pslist.avg_threads',
    'dlllist.ndlls',
    'handles.nhandles',
    'handles.nport',
    'ldrmodules.not_in_load_avg',
    'malfind.ninjections'
]

def predict_malware(sample_features: dict, historical_errors=None):
    """
    Predict malware using Autoencoder + Random Forest Hybrid Pipeline.
    """

    # Preprocessing
    # Arrange sample in feature order expected by scaler_rf1
    feature_order = scaler_rf1.feature_names_in_
    sample_list_full = [sample_features.get(feat, 0.0) for feat in feature_order]
    X_full = np.array(sample_list_full).reshape(1, -1)
    X_full_scaled = scaler_rf1.transform(X_full)

    # Prepare AE input (7 features)
    sample_list_ae = [sample_features.get(feat, 0.0) for feat in ae_features]
    X_ae = np.array(sample_list_ae).reshape(1, -1)
    X_ae_scaled = scaler_ae.transform(X_ae)

    # Autoencoder: Anomaly Detection
    reconstructed = autoencoder.predict(X_ae_scaled, verbose=0)
    reconstruction_error = np.mean(np.square(X_ae_scaled - reconstructed))
   
    threshold = 15
    is_anomalous = reconstruction_error > threshold
 
    
    # RF1: Benign vs Malware
    label = rf_binary.predict(X_full_scaled)[0]
    confidence_rf1 = rf_binary.predict_proba(X_full_scaled)[0][label]

    # RF2: Malware Type (only if detected as Malware)
    if label == 1:
        malware_type = rf_multiclass.predict(X_full_scaled)[0]
    else:
        malware_type = "N/A"
        anomaly_score = "--"
        risk_score = "--"
        prediction_accuracy_score = round(confidence_rf1, 2)

    # Risk Score Calculation
    historical_avg_error = historical_errors if isinstance(historical_errors, (int, float)) else 0.02
    base_risk = 0.5 * reconstruction_error + 0.5 * historical_avg_error

    if is_anomalous:
        risk_score = (max(100, round((base_risk * 1.5) , 2)))/100
        prediction_accuracy_score = round(confidence_rf1 *0.85, 2)
    else:
        risk_score = (max(100, round(base_risk, 2)))/100
        prediction_accuracy_score = max(0, round(confidence_rf1, 2))  # Penalize confidence

    # Malicious Behavior Score

    anomaly_score = (round(reconstruction_error,2))

    # Final result
    result = {
        "result": "malware" if label == 1 else "Benign",
        "malware_type": malware_type,
        "anomaly_detection_score": anomaly_score,
        "prediction_accuracy": prediction_accuracy_score,
        "future_risk_rating": risk_score if label ==1 else "--",
    }

    return result

# Predict multiple samples
def predict_multiple_malwares(samples: list, historical_errors=None):
    if not isinstance(samples, list):
        raise ValueError("Input must be a list of dictionaries.")

    results = []
    for i, sample in enumerate(samples):
        result = predict_malware(sample, historical_errors)
        results.append({
            "sample_id": i + 1,
            "prediction": result
        })
    return results
