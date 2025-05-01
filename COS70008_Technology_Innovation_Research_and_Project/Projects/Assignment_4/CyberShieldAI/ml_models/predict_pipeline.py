# predict_pipeline.py

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

# Predict function
def predict_malware(sample_features: dict, historical_errors=None):
    """
    Predict malware using Autoencoder + Random Forest Hybrid Pipeline.
    """

    # Preprocessing
    # Arrange sample in feature order expected by scaler_rf1
    feature_order = scaler_rf1.feature_names_in_
    sample_list_full = [sample_features[feat] for feat in feature_order]
    X_full = np.array(sample_list_full).reshape(1, -1)
    X_full_scaled = scaler_rf1.transform(X_full)

    # Prepare AE input (7 features)
    sample_list_ae = [sample_features[feat] for feat in ae_features]
    X_ae = np.array(sample_list_ae).reshape(1, -1)
    X_ae_scaled = scaler_ae.transform(X_ae)

    # Autoencoder: Anomaly Detection
    reconstructed = autoencoder.predict(X_ae_scaled, verbose=0)
    reconstruction_error = np.mean(np.square(X_ae_scaled - reconstructed))
   
    threshold = 8
    is_anomalous = reconstruction_error > threshold
 
    
    # RF1: Benign vs Malware
    label = rf_binary.predict(X_full_scaled)[0]
    confidence_rf1 = rf_binary.predict_proba(X_full_scaled)[0][label]

    # RF2: Malware Type (only if detected as Malware)
    if label == 1:
        malware_type = rf_multiclass.predict(X_full_scaled)[0]
    else:
        malware_type = "N/A"

    # Risk Score Calculation
    if historical_errors and len(historical_errors) > 0:
        historical_avg_error = np.mean(historical_errors)
    else:
        historical_avg_error = 0.02  # Assume low default historical error if not available

    base_risk = 0.5 * reconstruction_error + 0.5 * historical_avg_error

    if is_anomalous:
        risk_score = (min(100, round((base_risk * 1.5) , 2)))/100
        prediction_accuracy_score = round(confidence_rf1, 2)
    else:
        risk_score = (min(100, round(base_risk, 2)))/100
        prediction_accuracy_score = max(0, round(confidence_rf1 * 0.8, 2))  # Penalize confidence

    # Malicious Behavior Score
    anomaly_score = min(100, round((reconstruction_error), 2))

    # Final result
    result = {
        "result": "malware" if label == 1 else "Benign",
        "malware_type": malware_type,
        "anomaly_detection_score": anomaly_score,
        "prediction_accuracy": prediction_accuracy_score,
        "future_risk_rating": risk_score,
    }

    return result


sample_input = {
     'pslist.nproc': 45,
    'pslist.nppid': 17,
    'pslist.avg_threads': 10.55555556,
    'pslist.nprocs64bit': 0,
    'pslist.avg_handlers': 202.8444444,
    'dlllist.ndlls': 1694,
    'dlllist.avg_dlls_per_proc': 38.5,
    'handles.nhandles': 9129,
    'handles.avg_handles_per_proc': 212.3023256,
    'handles.nport': 0,
    'handles.nfile': 670,
    'handles.nevent': 3161,
    'handles.ndesktop': 46,
    'handles.nkey': 716,
    'handles.nthread': 887,
    'handles.ndirectory': 104,
    'handles.nsemaphore': 671,
    'handles.ntimer': 125,
    'handles.nsection': 184,
    'handles.nmutant': 257,
    'ldrmodules.not_in_load': 53,
    'ldrmodules.not_in_init': 95,
    'ldrmodules.not_in_mem': 53,
    'ldrmodules.not_in_load_avg': 0.030372493,
    'ldrmodules.not_in_init_avg': 0.054441261,
    'ldrmodules.not_in_mem_avg': 0.030372493,
    'malfind.ninjections': 5,
    'malfind.commitCharge': 21,
    'malfind.protection': 30,
    'malfind.uniqueInjections': 1.25,
    'psxview.not_in_pslist': 2,
    'psxview.not_in_eprocess_pool': 0,
    'psxview.not_in_ethread_pool': 3,
    'psxview.not_in_pspcid_list': 2,
    'psxview.not_in_csrss_handles': 7,
    'psxview.not_in_session': 4,
    'psxview.not_in_deskthrd': 9,
    'psxview.not_in_pslist_false_avg': 0.042553191,
    'psxview.not_in_eprocess_pool_false_avg': 0.0,
    'psxview.not_in_ethread_pool_false_avg': 0.063829787,
    'psxview.not_in_pspcid_list_false_avg': 0.042553191,
    'psxview.not_in_csrss_handles_false_avg': 0.14893617,
    'psxview.not_in_session_false_avg': 0.085106383,
    'psxview.not_in_deskthrd_false_avg': 0.191489362,
    'modules.nmodules': 138,
    'svcscan.nservices': 389,
    'svcscan.kernel_drivers': 221,
    'svcscan.fs_drivers': 26,
    'svcscan.process_services': 24,
    'svcscan.shared_process_services': 116,
    'svcscan.interactive_process_services': 0,
    'svcscan.nactive': 121,
    'callbacks.ncallbacks': 87,
    'callbacks.nanonymous': 0,
    'callbacks.ngeneric': 8
}


# simulate historical error list (assume user did 2 previous scans)
historical_errors = [15, 56]

# run prediction
prediction = predict_malware(sample_input, historical_errors)


print(prediction)