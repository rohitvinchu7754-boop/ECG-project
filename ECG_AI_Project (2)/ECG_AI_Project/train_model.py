"""
Train a baseline classifier from a labeled CSV dataset.

Expected file: ecg_dataset.csv
Format:
  - One row per labeled ECG segment/record
  - Columns 1..N: numeric ECG samples (no header)
  - Last column: class label (e.g. Normal, AF, Arrhythmia)

All rows must have the same number of sample columns.
Use only a properly labeled, appropriately licensed dataset. Split data by
patient/record where possible to avoid leakage. This baseline is educational,
not a clinically validated diagnostic model.
"""
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

DATASET = "ecg_dataset.csv"
MODEL_OUT = "model.pkl"

df = pd.read_csv(DATASET, header=None)
if df.shape[1] < 3:
    raise SystemExit("Dataset needs at least 2 ECG sample columns plus a final label column.")

X = df.iloc[:, :-1].apply(pd.to_numeric, errors="coerce")
y = df.iloc[:, -1].astype(str)

# Remove rows without labels or with too little usable data.
valid = y.notna() & (X.notna().sum(axis=1) >= max(2, int(X.shape[1] * 0.8)))
X, y = X.loc[valid], y.loc[valid]
if y.nunique() < 2:
    raise SystemExit("At least two distinct class labels are required.")
if len(X) < 10:
    raise SystemExit("Not enough labeled rows. Add more training examples.")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
model = make_pipeline(
    SimpleImputer(strategy="median"),
    StandardScaler(),
    RandomForestClassifier(n_estimators=250, class_weight="balanced", random_state=42)
)
model.fit(X_train, y_train)
pred = model.predict(X_test)

print("Holdout accuracy:", round(accuracy_score(y_test, pred), 4))
print("\nClassification report:\n", classification_report(y_test, pred, zero_division=0))
print("\nConfusion matrix:\n", confusion_matrix(y_test, pred))

joblib.dump({"model": model, "n_features": X.shape[1]}, MODEL_OUT)
print(f"\nSaved model to {MODEL_OUT}")
print("Important: use patient-level separation and independent clinical validation before any real-world use.")
