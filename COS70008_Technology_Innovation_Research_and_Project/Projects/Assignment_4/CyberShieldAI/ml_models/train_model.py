# train_model.py

# General libraries
import pandas as pd
import numpy as np
import os
import pickle

# Sklearn libraries
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Tensorflow and Keras libraries
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam

# -------------------------------
# Step 0: Setup Directories
# -------------------------------

# Create model save directory if it does not exist
os.makedirs('ml_models/saved_models', exist_ok=True)

# Define paths
AE_DATA_PATH = 'Dataset/autoencoder_dataset.csv' 
RF1_DATA_PATH = 'Dataset/RF_1_dataset.csv'
RF2_DATA_PATH = 'Dataset/RF_2_dataset.csv'
MODEL_DIR = 'ml_models/saved_models/'

# -------------------------------
# Step 1: Train Autoencoder
# -------------------------------

# Load Autoencoder benign dataset
df_ae = pd.read_csv(AE_DATA_PATH)

# Select 7 important features
ae_features = [
    'pslist.nproc',
    'pslist.avg_threads',
    'dlllist.ndlls',
    'handles.nhandles',
    'handles.nport',
    'ldrmodules.not_in_load_avg',
    'malfind.ninjections'
]
X_ae = df_ae[ae_features]

# Cap outliers at 99th percentile
for col in ae_features:
    upper_limit = X_ae[col].quantile(0.99)
    X_ae[col] = np.where(X_ae[col] > upper_limit, upper_limit, X_ae[col])

# Scale AE data
scaler_ae = StandardScaler()
X_ae_scaled = scaler_ae.fit_transform(X_ae)

# Save the AE scaler
with open(os.path.join(MODEL_DIR, 'scaler_ae.pkl'), 'wb') as f:
    pickle.dump(scaler_ae, f)

# Split into training and validation
X_train_ae, X_val_ae = train_test_split(X_ae_scaled, test_size=0.2, random_state=42)

# Define Autoencoder model
autoencoder = Sequential([
    Dense(4, activation='relu', input_shape=(7,)),
    Dense(2, activation='relu'),
    Dense(4, activation='relu'),
    Dense(7, activation='linear')
])

# Compile Autoencoder with proper loss object (important for loading later)
autoencoder.compile(
    optimizer=Adam(learning_rate=0.001),
    loss=tf.keras.losses.MeanSquaredError()
)

# Setup EarlyStopping
early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True
)

# Train Autoencoder
autoencoder.fit(
    X_train_ae,
    X_train_ae,
    epochs=100,
    batch_size=32,
    validation_data=(X_val_ae, X_val_ae),
    callbacks=[early_stopping],
    verbose=1
)

# Save Autoencoder model
autoencoder.save(os.path.join(MODEL_DIR, 'autoencoder_model.h5'))

print("✅ Autoencoder training completed and saved.")

# -------------------------------
# Step 2: Train Random Forest 1 - Binary Classification
# -------------------------------

# Load RF1 dataset (Benign + Malware)
df_rf1 = pd.read_csv(RF1_DATA_PATH)

X_rf1 = df_rf1.drop(columns=['Class'])
y_rf1 = df_rf1['Class'].apply(lambda x: 0 if x == 'Benign' else 1)

# Cap outliers at 99th percentile
for col in X_rf1.columns:
    upper_limit = X_rf1[col].quantile(0.99)
    X_rf1[col] = np.where(X_rf1[col] > upper_limit, upper_limit, X_rf1[col])

# Scale RF1 features
scaler_rf1 = StandardScaler()
X_rf1_scaled = scaler_rf1.fit_transform(X_rf1)

# Save RF1 scaler
with open(os.path.join(MODEL_DIR, 'scaler_rf1.pkl'), 'wb') as f:
    pickle.dump(scaler_rf1, f)

# Train/test split for RF1
X_train_rf1, X_test_rf1, y_train_rf1, y_test_rf1 = train_test_split(
    X_rf1_scaled, y_rf1, test_size=0.3, random_state=42, stratify=y_rf1
)

# Define and train RF1
rf_binary = RandomForestClassifier(
    n_estimators=100,
    max_depth=None,
    criterion='gini',
    random_state=42
)
rf_binary.fit(X_train_rf1, y_train_rf1)

# Save RF1 model
with open(os.path.join(MODEL_DIR, 'rf_binary.pkl'), 'wb') as f:
    pickle.dump(rf_binary, f)

print("✅ Random Forest Binary Classifier training completed and saved.")

# -------------------------------
# Step 3: Train Random Forest 2 - Multi-Class Malware Subtype Classification
# -------------------------------

# Load RF2 malware-only dataset
df_rf2 = pd.read_csv(RF2_DATA_PATH)

X_rf2 = df_rf2.drop(columns=['Category'])
y_rf2 = df_rf2['Category']

# Cap outliers at 99th percentile
for col in X_rf2.columns:
    upper_limit = X_rf2[col].quantile(0.99)
    X_rf2[col] = np.where(X_rf2[col] > upper_limit, upper_limit, X_rf2[col])

# Scale RF2 features (reuse scaler_rf1 to keep consistent feature scaling)
X_rf2_scaled = scaler_rf1.transform(X_rf2)

# Train/test split for RF2
X_train_rf2, X_test_rf2, y_train_rf2, y_test_rf2 = train_test_split(
    X_rf2_scaled, y_rf2, test_size=0.3, random_state=42, stratify=y_rf2
)

# Define and train RF2
rf_multiclass = RandomForestClassifier(
    n_estimators=100,
    max_depth=None,
    criterion='gini',
    random_state=42
)
rf_multiclass.fit(X_train_rf2, y_train_rf2)

# Save RF2 model
with open(os.path.join(MODEL_DIR, 'rf_multiclass.pkl'), 'wb') as f:
    pickle.dump(rf_multiclass, f)

print("✅ Random Forest Multi-Class Malware Classifier training completed and saved.")

# -------------------------------
print("\n🎯 All models successfully trained and saved!")
