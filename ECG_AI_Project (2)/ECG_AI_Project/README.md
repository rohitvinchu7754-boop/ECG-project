# CardioAI — AI-Based ECG Signal Analysis

A student-project starter website built with Flask, HTML/CSS, JavaScript, Chart.js and scikit-learn.

## Features
- Responsive medical-style dashboard
- Upload numeric ECG CSV files
- Plot the uploaded waveform
- Compute sample count, mean, standard deviation, minimum and maximum
- Optional local classifier integration through `model.pkl`
- Training script for a labeled, fixed-width CSV dataset

## Setup
Recommended: Python 3.10 or newer.

### Windows
```powershell
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser. Keep the terminal open.

## ECG CSV input format
For website signal preview, use one numeric sample per row in the first column, e.g.
```csv
0.02
0.03
0.01
-0.04
0.11
```
Use at least 100 samples. The app uses the first column and ignores nonnumeric rows.

## Training an ML model
Prepare `ecg_dataset.csv` in the project root:
- Each row is one labeled ECG segment/record.
- Columns 1..N are numeric signal samples.
- The last column is the class label.
- All signal rows must use the same number of sample columns.
- There should be multiple examples of each label.

Then run:
```bash
python train_model.py
```
This writes `model.pkl`. Restart the Flask app and upload a signal with the same underlying representation and preprocessing as the training data.

**Important:** The training script is a baseline demonstration. A production-quality ECG project needs carefully designed beat segmentation, filtering, patient-level train/test separation, class imbalance handling, external validation and clinically appropriate review. Do not interpret its prediction as a diagnosis. The displayed confidence is a model score, not a calibrated probability of disease.

## Suggested report/demo flow
1. Explain the problem statement and objectives.
2. Show the dataset and labels.
3. Explain preprocessing and the training/test split.
4. Upload an example CSV and show its waveform.
5. If a trained model is present, show the model output and metrics from a held-out test set.
6. Discuss limitations, false positives/negatives, and future work.

## Safety
This is an educational research prototype, not a medical device. Do not use it to make healthcare decisions or delay emergency care.
