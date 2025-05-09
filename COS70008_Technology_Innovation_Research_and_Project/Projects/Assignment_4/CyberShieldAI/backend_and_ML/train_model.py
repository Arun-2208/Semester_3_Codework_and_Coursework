import pandas as pd
import numpy as np
import os
import pickle
import matplotlib.pyplot as plt
from io import BytesIO
import base64

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import MeanSquaredError

# Constants
AE_DATA_PATH = 'Dataset/autoencoder_dataset.csv'
RF1_DATA_PATH = 'Dataset/RF_1_dataset.csv'
RF2_DATA_PATH = 'Dataset/RF_2_dataset.csv'
MODEL_DIR = 'ml_models/saved_models'

os.makedirs(MODEL_DIR, exist_ok=True)

def train_model_with_params(epochs=100, batch_size=32, learning_rate=0.001):
    output_log = []

    # ---- Autoencoder ----
    df_ae = pd.read_csv(AE_DATA_PATH)
    ae_features = [
        'pslist.nproc', 'pslist.avg_threads', 'dlllist.ndlls',
        'handles.nhandles', 'handles.nport',
        'ldrmodules.not_in_load_avg', 'malfind.ninjections'
    ]
    X_ae = df_ae[ae_features].copy()
    for col in ae_features:
        upper_limit = X_ae[col].quantile(0.99)
        X_ae.loc[:, col] = np.where(X_ae[col] > upper_limit, upper_limit, X_ae[col])

    scaler_ae = StandardScaler()
    X_ae_scaled = scaler_ae.fit_transform(X_ae)
    with open(os.path.join(MODEL_DIR, 'scaler_ae.pkl'), 'wb') as f:
        pickle.dump(scaler_ae, f)

    X_train_ae, X_val_ae = train_test_split(X_ae_scaled, test_size=0.2, random_state=42)

    autoencoder = Sequential([
        Dense(4, activation='relu', input_shape=(7,)),
        Dense(2, activation='relu'),
        Dense(4, activation='relu'),
        Dense(7, activation='linear')
    ])
    autoencoder.compile(optimizer=Adam(learning_rate=learning_rate), loss=MeanSquaredError())
    early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

    history = autoencoder.fit(
        X_train_ae, X_train_ae,
        validation_data=(X_val_ae, X_val_ae),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=[early_stop],
        verbose=1
    )

    ae_model_path = os.path.join(MODEL_DIR, 'autoencoder_model.h5')
    if os.path.exists(ae_model_path):
        os.remove(ae_model_path)
    autoencoder.save(ae_model_path)
    output_log.append(" Autoencoder model trained and saved.")

    # ---- Training Loss Plot ----
    plt.figure(figsize=(6, 4))
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Val Loss')
    plt.title("Autoencoder Training Loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
    plt.grid(True)
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    base64_plot = base64.b64encode(buf.read()).decode('utf-8')

    # ---- RF1 ----
    df_rf1 = pd.read_csv(RF1_DATA_PATH)
    X_rf1 = df_rf1.drop(columns=['Class']).copy()
    y_rf1 = df_rf1['Class'].apply(lambda x: 0 if x == 'Benign' else 1)
    for col in X_rf1.columns:
        upper = X_rf1[col].quantile(0.99)
        X_rf1.loc[:, col] = np.where(X_rf1[col] > upper, upper, X_rf1[col])
    scaler_rf1 = StandardScaler()
    X_rf1_scaled = scaler_rf1.fit_transform(X_rf1)
    with open(os.path.join(MODEL_DIR, 'scaler_rf1.pkl'), 'wb') as f:
        pickle.dump(scaler_rf1, f)
    X_train_rf1, _, y_train_rf1, _ = train_test_split(X_rf1_scaled, y_rf1, test_size=0.3, random_state=42, stratify=y_rf1)
    rf_binary = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_binary.fit(X_train_rf1, y_train_rf1)
    with open(os.path.join(MODEL_DIR, 'rf_binary.pkl'), 'wb') as f:
        pickle.dump(rf_binary, f)
    output_log.append(" Random Forest (binary) trained and saved.")

    # ---- RF2 ----
    df_rf2 = pd.read_csv(RF2_DATA_PATH)
    X_rf2 = df_rf2.drop(columns=['Category']).copy()
    y_rf2 = df_rf2['Category']
    for col in X_rf2.columns:
        upper = X_rf2[col].quantile(0.99)
        X_rf2.loc[:, col] = np.where(X_rf2[col] > upper, upper, X_rf2[col])
    X_rf2_scaled = scaler_rf1.transform(X_rf2)  # reuse scaler
    X_train_rf2, _, y_train_rf2, _ = train_test_split(X_rf2_scaled, y_rf2, test_size=0.3, random_state=42, stratify=y_rf2)
    rf_multi = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_multi.fit(X_train_rf2, y_train_rf2)
    with open(os.path.join(MODEL_DIR, 'rf_multiclass.pkl'), 'wb') as f:
        pickle.dump(rf_multi, f)
    output_log.append(" Random Forest (multi-class) trained and saved.")

    output_log.append(" All models trained and saved successfully.")
    return {
        "message": "Model training completed.",
        "logs": output_log,
        "plot_base64": base64_plot
    }

# CLI usage
if __name__ == '__main__':
    result = train_model_with_params()
    for line in result['logs']:
        print(line)
