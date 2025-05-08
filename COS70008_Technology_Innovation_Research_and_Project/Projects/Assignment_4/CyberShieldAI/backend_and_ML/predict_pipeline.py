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
    if historical_errors and historical_errors > 0:
        historical_avg_error = np.mean(historical_errors)
    else:
        historical_avg_error = 0.02  # Assume low default historical error if not available

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

import pprint

# Optional simulated error history
historical_errors = [15, 56,68,89,15,64]

# Sample inputs (3 entries)
sample_inputs = [
    {
        'pslist.nproc': 32, 'pslist.nppid': 13, 'pslist.avg_threads': 13.5, 'pslist.nprocs64bit': 0, 'pslist.avg_handlers': 264.28,
        'dlllist.ndlls': 1445, 'dlllist.avg_dlls_per_proc': 45.16, 'handles.nhandles': 8457, 'handles.avg_handles_per_proc': 264.28,
        'handles.nport': 0, 'handles.nfile': 630, 'handles.nevent': 2961, 'handles.ndesktop': 36, 'handles.nkey': 654,
        'handles.nthread': 792, 'handles.ndirectory': 83, 'handles.nsemaphore': 567, 'handles.ntimer': 127,
        'handles.nsection': 186, 'handles.nmutant': 242, 'ldrmodules.not_in_load': 31, 'ldrmodules.not_in_init': 62,
        'ldrmodules.not_in_mem': 31, 'ldrmodules.not_in_load_avg': 0.02148, 'ldrmodules.not_in_init_avg': 0.04297,
        'ldrmodules.not_in_mem_avg': 0.02148, 'malfind.ninjections': 2, 'malfind.commitCharge': 2,
        'malfind.protection': 12, 'malfind.uniqueInjections': 1, 'psxview.not_in_pslist': 0,
        'psxview.not_in_eprocess_pool': 0, 'psxview.not_in_ethread_pool': 0, 'psxview.not_in_pspcid_list': 0,
        'psxview.not_in_csrss_handles': 4, 'psxview.not_in_session': 2, 'psxview.not_in_deskthrd': 6,
        'psxview.not_in_pslist_false_avg': 0.0, 'psxview.not_in_eprocess_pool_false_avg': 0.0,
        'psxview.not_in_ethread_pool_false_avg': 0.0, 'psxview.not_in_pspcid_list_false_avg': 0.0,
        'psxview.not_in_csrss_handles_false_avg': 0.125, 'psxview.not_in_session_false_avg': 0.0625,
        'psxview.not_in_deskthrd_false_avg': 0.1875, 'modules.nmodules': 138, 'svcscan.nservices': 395,
        'svcscan.kernel_drivers': 222, 'svcscan.fs_drivers': 26, 'svcscan.process_services': 27,
        'svcscan.shared_process_services': 118, 'svcscan.interactive_process_services': 0, 'svcscan.nactive': 120,
        'callbacks.ncallbacks': 88, 'callbacks.nanonymous': 0, 'callbacks.ngeneric': 8
    },
    {
        'pslist.nproc': 37, 'pslist.nppid': 15, 'pslist.avg_threads': 10.14, 'pslist.nprocs64bit': 0, 'pslist.avg_handlers': 214.65,
        'dlllist.ndlls': 1445, 'dlllist.avg_dlls_per_proc': 39.05, 'handles.nhandles': 7942, 'handles.avg_handles_per_proc': 214.65,
        'handles.nport': 0, 'handles.nfile': 630, 'handles.nevent': 2809, 'handles.ndesktop': 40, 'handles.nkey': 666,
        'handles.nthread': 662, 'handles.ndirectory': 92, 'handles.nsemaphore': 594, 'handles.ntimer': 113,
        'handles.nsection': 160, 'handles.nmutant': 230, 'ldrmodules.not_in_load': 42, 'ldrmodules.not_in_init': 78,
        'ldrmodules.not_in_mem': 42, 'ldrmodules.not_in_load_avg': 0.02883, 'ldrmodules.not_in_init_avg': 0.05353,
        'ldrmodules.not_in_mem_avg': 0.02883, 'malfind.ninjections': 3, 'malfind.commitCharge': 3,
        'malfind.protection': 18, 'malfind.uniqueInjections': 1, 'psxview.not_in_pslist': 0,
        'psxview.not_in_eprocess_pool': 0, 'psxview.not_in_ethread_pool': 0, 'psxview.not_in_pspcid_list': 0,
        'psxview.not_in_csrss_handles': 4, 'psxview.not_in_session': 2, 'psxview.not_in_deskthrd': 6,
        'psxview.not_in_pslist_false_avg': 0.0, 'psxview.not_in_eprocess_pool_false_avg': 0.0,
        'psxview.not_in_ethread_pool_false_avg': 0.0, 'psxview.not_in_pspcid_list_false_avg': 0.0,
        'psxview.not_in_csrss_handles_false_avg': 0.10811, 'psxview.not_in_session_false_avg': 0.05405,
        'psxview.not_in_deskthrd_false_avg': 0.16216, 'modules.nmodules': 138, 'svcscan.nservices': 389,
        'svcscan.kernel_drivers': 221, 'svcscan.fs_drivers': 26, 'svcscan.process_services': 24,
        'svcscan.shared_process_services': 116, 'svcscan.interactive_process_services': 0, 'svcscan.nactive': 119,
        'callbacks.ncallbacks': 87, 'callbacks.nanonymous': 0, 'callbacks.ngeneric': 8
    },
    {
        'pslist.nproc': 39, 'pslist.nppid': 16, 'pslist.avg_threads': 9.87, 'pslist.nprocs64bit': 0, 'pslist.avg_handlers': 210.10,
        'dlllist.ndlls': 1504, 'dlllist.avg_dlls_per_proc': 38.56, 'handles.nhandles': 8195, 'handles.avg_handles_per_proc': 215.66,
        'handles.nport': 0, 'handles.nfile': 635, 'handles.nevent': 2880, 'handles.ndesktop': 41, 'handles.nkey': 698,
        'handles.nthread': 685, 'handles.ndirectory': 95, 'handles.nsemaphore': 617, 'handles.ntimer': 116,
        'handles.nsection': 165, 'handles.nmutant': 237, 'ldrmodules.not_in_load': 45, 'ldrmodules.not_in_init': 82,
        'ldrmodules.not_in_mem': 45, 'ldrmodules.not_in_load_avg': 0.02961, 'ldrmodules.not_in_init_avg': 0.05395,
        'ldrmodules.not_in_mem_avg': 0.02961, 'malfind.ninjections': 3, 'malfind.commitCharge': 3,
        'malfind.protection': 18, 'malfind.uniqueInjections': 1, 'psxview.not_in_pslist': 0,
        'psxview.not_in_eprocess_pool': 0, 'psxview.not_in_ethread_pool': 1, 'psxview.not_in_pspcid_list': 0,
        'psxview.not_in_csrss_handles': 5, 'psxview.not_in_session': 2, 'psxview.not_in_deskthrd': 7,
        'psxview.not_in_pslist_false_avg': 0.0, 'psxview.not_in_eprocess_pool_false_avg': 0.0,
        'psxview.not_in_ethread_pool_false_avg': 0.02564, 'psxview.not_in_pspcid_list_false_avg': 0.0,
        'psxview.not_in_csrss_handles_false_avg': 0.12821, 'psxview.not_in_session_false_avg': 0.05128,
        'psxview.not_in_deskthrd_false_avg': 0.17949, 'modules.nmodules': 138, 'svcscan.nservices': 389,
        'svcscan.kernel_drivers': 221, 'svcscan.fs_drivers': 26, 'svcscan.process_services': 24,
        'svcscan.shared_process_services': 116, 'svcscan.interactive_process_services': 0, 'svcscan.nactive': 119,
        'callbacks.ncallbacks': 86, 'callbacks.nanonymous': 0, 'callbacks.ngeneric': 8
    }
]

# Run predictions on all
results = predict_multiple_malwares(sample_inputs, historical_errors)

# Print results
for res in results:
    print(f"\n🧪 Sample {res['sample_id']}:")
    for k, v in res['prediction'].items():
        print(f"   {k}: {v}")
