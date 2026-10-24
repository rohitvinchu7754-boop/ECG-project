from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import joblib
import io
import os

app = Flask(__name__)
MODEL_PATH = "model.pkl"

def load_signal(upload):
    name = (upload.filename or "").lower()
    if not name.endswith(".csv"):
        raise ValueError("Please upload a CSV file.")
    content = upload.read()
    if not content:
        raise ValueError("The uploaded file is empty.")
    # Accept one-column or multi-column numeric CSVs; use the first column.
    try:
        frame = pd.read_csv(io.BytesIO(content), header=None, comment="#")
        signal = pd.to_numeric(frame.iloc[:, 0], errors="coerce").dropna().to_numpy(dtype=float)
    except Exception as exc:
        raise ValueError("Could not read the CSV. Use numeric ECG samples.") from exc
    if len(signal) < 100:
        raise ValueError("Please provide at least 100 numeric ECG samples.")
    if not np.isfinite(signal).all():
        raise ValueError("The ECG signal contains invalid values.")
    return signal

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    upload = request.files.get("ecg_file")
    if not upload or not upload.filename:
        return jsonify({"error": "Choose an ECG CSV file first."}), 400
    try:
        signal = load_signal(upload)
        # Downsample only for display to keep responses compact.
        display_signal = signal[::max(1, len(signal) // 1200)].tolist()
        result = {
            "samples": int(len(signal)),
            "mean": round(float(np.mean(signal)), 5),
            "std": round(float(np.std(signal)), 5),
            "min": round(float(np.min(signal)), 5),
            "max": round(float(np.max(signal)), 5),
            "signal": display_signal,
            "prediction": None,
            "confidence": None,
            "model_status": "No trained model found. Signal statistics only."
        }

        if os.path.exists(MODEL_PATH):
            bundle = joblib.load(MODEL_PATH)
            model = bundle["model"]
            expected = int(bundle["n_features"])
            # Model training uses fixed-length beat/signal vectors.
            # Resample input to the same feature length before inference.
            x = np.interp(
                np.linspace(0, len(signal) - 1, expected),
                np.arange(len(signal)),
                signal
            ).reshape(1, -1)
            prediction = model.predict(x)[0]
            result["prediction"] = str(prediction)
            if hasattr(model, "predict_proba"):
                result["confidence"] = round(float(np.max(model.predict_proba(x))) * 100, 2)
            result["model_status"] = "Prediction produced by your locally trained model."
        return jsonify(result)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        app.logger.exception("ECG analysis failed")
        return jsonify({"error": "Analysis failed. Check the CSV format and model setup."}), 500

if __name__ == "__main__":
    # Debug mode is for local development only.
    app.run(debug=True)
